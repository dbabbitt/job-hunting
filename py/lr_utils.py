#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



from IPython.display import clear_output
from sklearn.exceptions import NotFittedError
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from storage import Storage
import gc
import numpy as np
import pandas as pd
import re

s = Storage()

class LrUtilities(object):
    """Logistic Regression utilities class."""

    def __init__(self, ha=None, cu=None, hc=None, verbose=False):
        if ha is None:
            from ha_utils import HeaderAnalysis
            self.ha = HeaderAnalysis(verbose=verbose)
        else:
            self.ha = ha
        if cu is None:
            from scrape_utils import WebScrapingUtilities
            wsu = WebScrapingUtilities()
            uri = wsu.secrets_json['neo4j']['connect_url']
            user =  wsu.secrets_json['neo4j']['username']
            password = wsu.secrets_json['neo4j']['password']

            from cypher_utils import CypherUtilities
            self.cu = CypherUtilities(uri=uri, user=user, password=password, driver=None, s=s, ha=ha)
        else:
            self.cu = cu
        if hc is None:
            from hc_utils import HeaderCategories
            self.hc = HeaderCategories(cu=self.cu, verbose=verbose)
        else:
            self.hc = hc
        self.verbose = verbose
        
        # Build the Logistic Regression elements
        # self.build_pos_logistic_regression_elements()
        # self.build_isheader_logistic_regression_elements()
        self.navigable_parent_cypher_str = '''
            MATCH (np:NavigableParents {{navigable_parent: '{}'}})
            RETURN
                np.navigable_parent AS navigable_parent,
                np.is_header AS is_header,
                np.is_task_scope AS is_task_scope,
                np.is_minimum_qualification AS is_minimum_qualification,
                np.is_preferred_qualification AS is_preferred_qualification,
                np.is_legal_notification AS is_legal_notification,
                np.is_job_title AS is_job_title,
                np.is_office_location AS is_office_location,
                np.is_job_duration AS is_job_duration,
                np.is_supplemental_pay AS is_supplemental_pay,
                np.is_educational_requirement AS is_educational_requirement,
                np.is_interview_procedure AS is_interview_procedure,
                np.is_corporate_scope AS is_corporate_scope,
                np.is_posting_date AS is_posting_date,
                np.is_other AS is_other;'''
    
    
    ###################################################
    ## Logistic Regression parts-of-speech functions ##
    ###################################################
    def build_pos_logistic_regression_elements(self, verbose=False):
        self.POS_LR_DICT = {}
        self.POS_PREDICT_PERCENT_FIT_DICT = {}

        # Train a model for each labeled POS symbol
        cypher_str = """
            MATCH (pos:PartsOfSpeech)-[r:SUMMARIZES]->(np:NavigableParents)
            RETURN
                np.navigable_parent AS navigable_parent, 
                pos.pos_symbol AS pos_symbol;"""
        pos_df = pd.DataFrame(self.cu.get_execution_results(cypher_str, verbose=False))

        # The shape of the Bag-of-words count vector here should be
        # `n` html strings * `m` unique parts-of-speech tokens
        sents_list = pos_df.navigable_parent.tolist()
        if verbose:
            print(f'I have {len(sents_list):,} hand-labeled html patterns in here')
        pos_symbol_list = pos_df.pos_symbol.unique().tolist()

        # Re-transform the bag-of-words and tf-idf from the new manual scores
        if s.pickle_exists('POS_CV'):
            self.POS_CV = s.load_object('POS_CV')
        else:
            self.POS_CV = CountVectorizer(analyzer='word', binary=False, decode_error='strict', lowercase=False, max_df=1.0,
                                          max_features=None, min_df=0.0, ngram_range=(1, 5), stop_words=None,
                                          strip_accents='ascii', tokenizer=self.ha.html_regex_tokenizer)
            s.store_objects(POS_CV=self.POS_CV)
        
        # Learn the vocabulary dictionary and return the document-term matrix
        bow_matrix = self.POS_CV.fit_transform(sents_list)

        # Tf-idf must get from Bag-of-words first
        if s.pickle_exists('POS_TT'):
            self.POS_TT = s.load_object('POS_TT')
        else:
            self.POS_TT = TfidfTransformer(norm='l1', smooth_idf=True, sublinear_tf=False, use_idf=True)
            s.store_objects(POS_TT=self.POS_TT)
        tfidf_matrix = self.POS_TT.fit_transform(bow_matrix)
        try:
            gc.collect()
            X = tfidf_matrix.toarray()
        except Exception as e:
            print(f'Got this {e.__class__} error in build_pos_logistic_regression_elements trying ',
                  f'to turn the pos_symbol TF-IDF matrix into a normal array: {str(e).strip()}')
            X = tfidf_matrix

        for pos_symbol in pos_symbol_list:

            # Train the classifier
            mask_series = (pos_df.pos_symbol == pos_symbol)
            y = mask_series.to_numpy()
            if pos_symbol not in self.POS_LR_DICT:
                self.POS_LR_DICT[pos_symbol] = LogisticRegression(C=375.0, class_weight='balanced', dual=False, 
                                                                  fit_intercept=True, intercept_scaling=1, 
                                                                  l1_ratio=None, max_iter=1000, 
                                                                  multi_class='auto', n_jobs=None, penalty='l1', 
                                                                  random_state=None, solver='liblinear', 
                                                                  tol=0.0001, verbose=False, warm_start=False)
            try:
                self.POS_LR_DICT[pos_symbol].fit(X, y)
                self.POS_PREDICT_PERCENT_FIT_DICT[pos_symbol] = self.build_pos_lr_predict_percent(pos_symbol, verbose=verbose)
            except ValueError as e:
                print(f'Fitting {pos_symbol} had this error: {str(e).strip()}')
                self.POS_LR_DICT.pop(pos_symbol, None)
                self.POS_PREDICT_PERCENT_FIT_DICT.pop(pos_symbol, None)
    
    def pos_lr_predict_single(self, html_str, verbose=False):
        tuple_list = []
        for pos_symbol, predict_percent_fit in self.POS_PREDICT_PERCENT_FIT_DICT.items():
            if predict_percent_fit is None:
                proba_tuple = (pos_symbol, 0.0)
                tuple_list.append(proba_tuple)
            else:
                proba_tuple = (pos_symbol, predict_percent_fit(html_str))
                tuple_list.append(proba_tuple)
        tuple_list.sort(reverse=True, key=lambda x: x[1])

        return tuple_list[0][0]
    
    def build_pos_lr_predict_percent(self, pos_symbol, verbose=False):
        predict_percent_fit = None
        if pos_symbol in self.POS_LR_DICT:
            
            # Re-calibrate the inference engine
            cv = CountVectorizer(vocabulary=self.POS_CV.vocabulary_)
            cv._validate_vocabulary()

            def predict_percent_fit(navigable_parent):

                X_test = self.POS_TT.transform(cv.transform([navigable_parent])).toarray()
                y_predict_proba = self.POS_LR_DICT[pos_symbol].predict_proba(X_test)[0][1]

                return y_predict_proba

        return predict_percent_fit
    
    
    #############################################
    ## Logistic Regression is-header functions ##
    #############################################
    def predict_isheader(self, child_str):
        probs_list = self.ISHEADER_PREDICT_PERCENT_FIT(child_str)
        idx = probs_list.index(max(probs_list))
        is_header = [True, False][idx]
        
        return is_header
    
    def retrain_isheader_classifier(self, header_df=None, tfidf_matrix=None, verbose=True):
        
        # Get all our header data
        if header_df is None:
            cypher_str = """
                MATCH (np:NavigableParents)
                WHERE np.is_header IS NOT NULL
                RETURN
                    np.navigable_parent AS navigable_parent, 
                    np.is_header AS is_header;"""
            header_df = pd.DataFrame(self.cu.get_execution_results(cypher_str, verbose=verbose))
            header_df.is_header = header_df.is_header.map(lambda x: {'True': True, 'False': False}[x])
        if verbose:
            print(f'I have {self.header_df.shape[0]:,} hand-labeled header htmls in here')
        
        if tfidf_matrix is None:
            
            # Get the new manual scores
            sents_list = header_df.navigable_parent.tolist()
            
            # Re-transform the bag-of-words from the new manual scores
            self.ISHEADER_CV = CountVectorizer(lowercase=True, tokenizer=self.ha.html_regex_tokenizer, ngram_range=(1, 3))
            
            # Learn the vocabulary dictionary and return the document-term matrix
            bow_matrix = self.ISHEADER_CV.fit_transform(sents_list)

            self.ISHEADER_VOCAB = self.ISHEADER_CV.vocabulary_
            s.store_objects(ISHEADER_VOCAB=self.ISHEADER_VOCAB, verbose=verbose)
            
            # Tf-idf must get from Bag-of-words first
            self.ISHEADER_TT = TfidfTransformer(norm='l1', smooth_idf=True, sublinear_tf=False, use_idf=True)
            tfidf_matrix = self.ISHEADER_TT.fit_transform(bow_matrix)
            s.store_objects(ISHEADER_TT=self.ISHEADER_TT, verbose=verbose)

        # Re-train the classifier
        y = header_df.is_header.values
        try:
            gc.collect()
            X = tfidf_matrix.toarray()
        except Exception as e:
            if verbose:
                print(f'Got this {e.__class__} error in build_isheader_logistic_regression_elements trying ',
                      f'to turn the is_header TF-IDF matrix into a normal array: {str(e).strip()}')
            X = tfidf_matrix
        self.ISHEADER_LR.fit(X, y)
        s.store_objects(ISHEADER_LR=self.ISHEADER_LR, verbose=verbose)

        # Re-calibrate the inference engine
        self.ISHEADER_PREDICT_PERCENT_FIT = self.build_isheader_lr_predict_percent(verbose=verbose)
        
        if verbose:
            print('Retraining complete')
    
    def build_isheader_logistic_regression_elements(self, verbose=False):
        
        # Get the data
        if not s.pickle_exists('ISHEADER_LR'):
            cypher_str = """
                MATCH (np:NavigableParents)
                WHERE np.is_header IS NOT NULL
                RETURN
                    np.navigable_parent AS navigable_parent, 
                    np.is_header AS is_header;"""
            np_df = pd.DataFrame(self.cu.get_execution_results(cypher_str, verbose=verbose))
            np_df.is_header = np_df.is_header.map(lambda x: {'True': True, 'False': False}[x])
        
        if s.pickle_exists('ISHEADER_CV'):
            self.ISHEADER_CV = s.load_object('ISHEADER_CV')
        else:
            self.ISHEADER_CV = CountVectorizer(analyzer='word', binary=False, decode_error='strict', lowercase=False, max_df=1.0,
                                          max_features=None, min_df=0.0, ngram_range=(1, 5), stop_words=None,
                                          strip_accents='ascii', tokenizer=self.ha.html_regex_tokenizer)
        
        if (not s.pickle_exists('ISHEADER_LR')) or (not s.pickle_exists('ISHEADER_CV')):
            
            # The shape of the Bag-of-words count vector here should be n html strings * m unique tokens
            sents_list = np_df.navigable_parent.tolist()
            
            # Re-transform the bag-of-words and tf-idf from the new manual scores
            # Learn the vocabulary dictionary and return the document-term matrix
            bow_matrix = self.ISHEADER_CV.fit_transform(sents_list)
            
            s.store_objects(ISHEADER_CV=self.ISHEADER_CV, verbose=verbose)
            if not hasattr(self.ISHEADER_CV, 'vocabulary_'):
                self.ISHEADER_CV._validate_vocabulary()
                if not self.ISHEADER_CV.fixed_vocabulary_:
                    raise NotFittedError('Vocabulary not fitted or provided')
            if len(self.ISHEADER_CV.vocabulary_) == 0:
                raise ValueError('Vocabulary is empty')
        if s.pickle_exists('ISHEADER_VOCAB'):
            self.ISHEADER_VOCAB = s.load_object('ISHEADER_VOCAB')
        else:
            self.ISHEADER_VOCAB = self.ISHEADER_CV.vocabulary_
            s.store_objects(ISHEADER_VOCAB=self.ISHEADER_VOCAB, verbose=verbose)
            
        if s.pickle_exists('ISHEADER_TT'):
            self.ISHEADER_TT = s.load_object('ISHEADER_TT')
        else:
            self.ISHEADER_TT = TfidfTransformer(norm='l1', smooth_idf=True, sublinear_tf=False, use_idf=True)
        
        if (not s.pickle_exists('ISHEADER_LR')) or not s.pickle_exists('ISHEADER_TT'):
            
            # Tf-idf must get from Bag-of-words first
            tfidf_matrix = self.ISHEADER_TT.fit_transform(bow_matrix)
            s.store_objects(ISHEADER_TT=self.ISHEADER_TT, verbose=verbose)
        
        if s.pickle_exists('ISHEADER_LR'):
            self.ISHEADER_LR = s.load_object('ISHEADER_LR')
        else:
            self.ISHEADER_LR = LogisticRegression(
                C=375.0, 
                class_weight='balanced', 
                dual=False, 
                fit_intercept=True, 
                intercept_scaling=1, 
                l1_ratio=None, 
                max_iter=1000, 
                multi_class='auto', 
                n_jobs=None, 
                penalty='l1', 
                random_state=None, 
                solver='liblinear', 
                tol=0.0001, 
                verbose=0, 
                warm_start=False)
            self.retrain_isheader_classifier(np_df, tfidf_matrix, verbose=verbose)
            
        self.ISHEADER_PREDICT_PERCENT_FIT = self.build_isheader_lr_predict_percent(verbose=verbose)
    
    def build_isheader_lr_predict_percent(self, verbose=False):
        
        # Re-calibrate the inference engine
        cv = CountVectorizer(vocabulary=self.ISHEADER_VOCAB)
        cv._validate_vocabulary()
        
        def predict_percent_fit(navigable_parent):
            '''
            probs_list = lru.ISHEADER_PREDICT_PERCENT_FIT(child_str)
            idx = probs_list.index(max(probs_list))
            is_header = [True, False][idx]
            '''

            X_test = self.ISHEADER_TT.transform(cv.transform([navigable_parent])).toarray()
            y_predict_proba = self.ISHEADER_LR.predict_proba(X_test).flatten().tolist()

            return y_predict_proba

        return predict_percent_fit
    
    
    ################################################
    ## Logistic Regression is-qualified functions ##
    ################################################
    def build_isqualified_logistic_regression_elements(self, verbose=False):
        
        # Get the data
        self.basic_quals_dict = s.load_object('basic_quals_dict')
        if not s.pickle_exists('ISQUALIFIED_LR'):
            rows_list = [{'qualification_str': qualification_str,
                          'is_qualified': is_fit} for qualification_str, is_fit in self.basic_quals_dict.items()]
            self.basic_quals_df = pd.DataFrame(rows_list)
            transform_dict = {'True': 1, 'False': 0, True: 1, False: 0, 1: 1, 0: 0}
            self.basic_quals_df.is_qualified = self.basic_quals_df.is_qualified.map(lambda x: transform_dict[x])
        
        if s.pickle_exists('ISQUALIFIED_CV'):
            self.ISQUALIFIED_CV = s.load_object('ISQUALIFIED_CV')
        else:
            self.ISQUALIFIED_CV = CountVectorizer(analyzer='word', binary=False, decode_error='strict', lowercase=False, max_df=1.0,
                                          max_features=None, min_df=0.0, ngram_range=(1, 5), stop_words=None,
                                          strip_accents='ascii', tokenizer=self.ha.html_regex_tokenizer)
        
        if (not s.pickle_exists('ISQUALIFIED_LR')) or (not s.pickle_exists('ISQUALIFIED_CV')):
            
            # The shape of the Bag-of-words count vector here should be n html strings * m unique tokens
            sents_list = self.basic_quals_df.qualification_str.tolist()
            
            # Re-transform the bag-of-words and tf-idf from the new manual scores
            # Learn the vocabulary dictionary and return the document-term matrix
            bow_matrix = self.ISQUALIFIED_CV.fit_transform(sents_list)
            
            s.store_objects(ISQUALIFIED_CV=self.ISQUALIFIED_CV, verbose=verbose)
            if not hasattr(self.ISQUALIFIED_CV, 'vocabulary_'):
                self.ISQUALIFIED_CV._validate_vocabulary()
                if not self.ISQUALIFIED_CV.fixed_vocabulary_:
                    raise NotFittedError('Vocabulary not fitted or provided')
            if len(self.ISQUALIFIED_CV.vocabulary_) == 0:
                raise ValueError('Vocabulary is empty')
        if s.pickle_exists('ISQUALIFIED_VOCAB'):
            self.ISQUALIFIED_VOCAB = s.load_object('ISQUALIFIED_VOCAB')
        else:
            self.ISQUALIFIED_VOCAB = self.ISQUALIFIED_CV.vocabulary_
            s.store_objects(ISQUALIFIED_VOCAB=self.ISQUALIFIED_VOCAB, verbose=verbose)
            
        if s.pickle_exists('ISQUALIFIED_TT'):
            self.ISQUALIFIED_TT = s.load_object('ISQUALIFIED_TT')
        else:
            self.ISQUALIFIED_TT = TfidfTransformer(norm='l1', smooth_idf=True, sublinear_tf=False, use_idf=True)
        
        if (not s.pickle_exists('ISQUALIFIED_LR')) or not s.pickle_exists('ISQUALIFIED_TT'):
            
            # Tf-idf must get from Bag-of-words first
            tfidf_matrix = self.ISQUALIFIED_TT.fit_transform(bow_matrix)
            s.store_objects(ISQUALIFIED_TT=self.ISQUALIFIED_TT, verbose=verbose)
        
        if s.pickle_exists('ISQUALIFIED_LR'):
            self.ISQUALIFIED_LR = s.load_object('ISQUALIFIED_LR')
        else:
            self.ISQUALIFIED_LR = LogisticRegression(
                C=375.0, 
                class_weight='balanced', 
                dual=False, 
                fit_intercept=True, 
                intercept_scaling=1, 
                l1_ratio=None, 
                max_iter=1000, 
                multi_class='auto', 
                n_jobs=None, 
                penalty='l1', 
                random_state=None, 
                solver='liblinear', 
                tol=0.0001, 
                verbose=0, 
                warm_start=False)
            self.refit_isqualified_lr(tfidf_matrix, verbose=verbose)

        # Re-calibrate the inference engine
        self.predict_job_hunt_percent_fit = self.build_isqualified_lr_predict_percent(verbose=verbose)
    
    def get_quals_str(self, prediction_list, quals_list):
        qual_count = 0
        quals_str = ''
        for pred_array, (i, qual_str) in zip(prediction_list, enumerate(quals_list)):
            if qual_str in self.basic_quals_dict:
                formatted_str = '\nquals_list[{}] = "{}" ({})'
                prediction = float(self.basic_quals_dict[qual_str])
            else:
                formatted_str = '\n*quals_list[{}] = "{}" ({})'
                prediction = pred_array[1]
            quals_str += formatted_str.format(i, qual_str, prediction)
            if prediction > 0.5:
                qual_count += 1
        
        return quals_str, qual_count
    
    def qual_sum(self, qual_str, verbose=False):
        if verbose:
            print(qual_str)
        results = '"{}"'.format(qual_str)
        if qual_str in self.basic_quals_dict:
            results = self.basic_quals_dict[qual_str]
        else:
            results = self.predict_job_hunt_percent_fit([qual_str])[0][1]
            if results > 0.5:
                results = 1.0
            else:
                results = 0.0
        
        return str(results)
    
    def print_loc_computation(self, row_index, quals_list, verbose=True):
        if verbose:
            print()
        numerator_str_list = []
        for qual_str in quals_list:
            if qual_str in self.basic_quals_dict:
                numerator_str_list.append(str(self.basic_quals_dict[qual_str]))
            else:
                numerator_str_list.append('000')
        numerator_str = '+'.join(numerator_str_list)
        if verbose:
            print("hunting_df.loc[{}, 'percent_fit'] = ({})/{}".format(row_index, numerator_str, len(quals_list)))
    
    def update_hunting(self, row_index, row_series, quals_list, verbose=True):
        percent_fit = eval(' + '.join(map(self.qual_sum, quals_list))) / len(quals_list)
        self.hunting_df.loc[row_index, 'percent_fit'] = percent_fit
        s.store_objects(hunting_df=self.hunting_df, verbose=False)
        
        def do_cypher_tx(tx, file_name, percent_fit, verbose=False):
            cypher_str = """
                MATCH (fn:FileNames {file_name: $file_name})
                SET fn.percent_fit = $percent_fit;"""
            if verbose:
                clear_output(wait=True)
                print(cypher_str.replace('$file_name', f'"{file_name}"').replace('$percent_fit', f'"{percent_fit}"'))
            parameter_dict = {'file_name': file_name, 'percent_fit': percent_fit}
            tx.run(query=cypher_str, parameters=parameter_dict)
        
        with self.cu.driver.session() as session:
            session.write_transaction(do_cypher_tx, file_name=row_series.file_name, percent_fit=percent_fit, verbose=verbose)
    
    def predict_isqualified(self, child_str):
        probs_list = self.predict_job_hunt_percent_fit(child_str)
        idx = probs_list.index(max(probs_list))
        is_qualified = [True, False][idx]
        
        return is_qualified
    
    def refit_isqualified_lr(self, tfidf_matrix, verbose=False):
            
        # Re-train the classifier
        y = self.basic_quals_df.is_qualified.to_numpy().astype(int)
        try:
            gc.collect()
            X = tfidf_matrix.toarray()
        except Exception as e:
            print(f'Got this {e.__class__} error in build_isqualified_logistic_regression_elements trying ',
                  f'to turn the is_qualified TF-IDF matrix into a normal array: {str(e).strip()}')
            X = tfidf_matrix
        self.ISQUALIFIED_LR.fit(X, y)
        s.store_objects(ISQUALIFIED_LR=self.ISQUALIFIED_LR, verbose=verbose)
    
    def build_isqualified_lr_predict_percent(self, verbose=False):
        
        # Re-calibrate the inference engine
        cv = CountVectorizer(vocabulary=self.ISQUALIFIED_VOCAB)
        cv._validate_vocabulary()
        
        def predict_percent_fit(quals_list):
            y_predict_proba = np.array([])
            
            # The TFIDF Vectorizer expects an array of strings
            if len(quals_list) and all([isinstance(qual_str, str) for qual_str in quals_list]):
                count_matrix = cv.transform(quals_list)
                
                # Transform the count matrix to a tf-idf representation
                X_test = self.ISQUALIFIED_TT.transform(count_matrix).toarray()
                
                y_predict_proba = self.ISQUALIFIED_LR.predict_proba(X_test)
            
            return y_predict_proba
            '''
        def predict_percent_fit(navigable_parent):
            probs_list = lru.predict_percent_fit(child_str)
            idx = probs_list.index(max(probs_list))
            is_qualified = [True, False][idx]
            count_matrix = cv.transform([navigable_parent])
            X_test = self.ISQUALIFIED_TT.transform(count_matrix).toarray()
            y_predict_proba = self.ISQUALIFIED_LR.predict_proba(X_test).flatten().tolist()

            return y_predict_proba
            '''

        return predict_percent_fit
    
    def retrain_isqualified_classifier(self, verbose=True):
        
        # Get all our file names data
        cypher_str = '''
            MATCH (fn:FileNames)
            RETURN fn;'''
        row_objs_list = self.cu.get_execution_results(cypher_str, verbose=False)
        self.hunting_df = pd.DataFrame([{k: v for k, v in row_obj['fn'].items()} for row_obj in row_objs_list])
        
        # Rebuild the dataframe from the dictionary
        self.basic_quals_dict = s.load_object('basic_quals_dict')
        rows_list = [{'qualification_str': qualification_str,
                      'is_qualified': is_fit} for qualification_str, is_fit in self.basic_quals_dict.items()]
        self.basic_quals_df = pd.DataFrame(rows_list)
        if verbose:
            print(f'I have {self.basic_quals_df.shape[0]:,} hand-labeled qualification strings in here')
        
        # Clean up the data
        mask_series = (self.basic_quals_df.is_qualified == True)
        self.basic_quals_df.loc[mask_series, 'is_qualified'] = 1
        mask_series = (self.basic_quals_df.is_qualified == False)
        self.basic_quals_df.loc[mask_series, 'is_qualified'] = 0
        s.store_objects(basic_quals_dict=self.basic_quals_df.set_index('qualification_str').is_qualified.to_dict(), verbose=False)
        s.store_objects(basic_quals_df=self.basic_quals_df, verbose=False)

        # Get the new manual scores
        sents_list = self.basic_quals_df.qualification_str.tolist()

        # Re-transform the bag-of-words from the new manual scores
        self.ISQUALIFIED_CV = CountVectorizer(lowercase=True, tokenizer=self.ha.html_regex_tokenizer, ngram_range=(1, 3))
        
        # Learn the vocabulary dictionary and return the document-term matrix
        bow_matrix = self.ISQUALIFIED_CV.fit_transform(sents_list)
        
        self.ISQUALIFIED_VOCAB = self.ISQUALIFIED_CV.vocabulary_
        s.store_objects(ISQUALIFIED_VOCAB=self.ISQUALIFIED_VOCAB, verbose=False)

        # Tf-idf must get from Bag-of-words first
        self.ISQUALIFIED_TT = TfidfTransformer(norm='l1', smooth_idf=True, sublinear_tf=False, use_idf=True)
        tfidf_matrix = self.ISQUALIFIED_TT.fit_transform(bow_matrix)
        s.store_objects(ISQUALIFIED_TT=self.ISQUALIFIED_TT, verbose=False)

        # Re-train the classifier
        self.refit_isqualified_lr(tfidf_matrix, verbose=False)
        
        # Re-calibrate the inference engine
        self.predict_job_hunt_percent_fit = self.build_isqualified_lr_predict_percent(verbose=False)
        if verbose:
            print('Retraining complete')
    
    def infer_from_hunting_dataframe(self, su=None, verbose=True):
        if su is None:
            from section_utils import SectionUtilities
            su = SectionUtilities(s=s, ha=self.ha, cu=self.cu, verbose=verbose)
        
        # Loop through all the unset %fit values, set them if you can, break for help if you can't
        mask_series = (self.hunting_df.percent_fit >= 0.0)
        quals_list = []
        file_name = None
        for row_index, row_series in self.hunting_df[~mask_series].iterrows():
            file_name = row_series.file_name
            quals_list, job_fitness = su.print_fit_job(row_index, row_series, lru=self)
            if job_fitness >= 2/3:
                if all(qual_str in self.basic_quals_dict for qual_str in quals_list):
                    self.update_hunting(row_index, row_series, quals_list)
                else:
                    break
            elif len(quals_list) and all([isinstance(qual_str, str) for qual_str in quals_list]):
                self.update_hunting(row_index, row_series, quals_list)
        if verbose:
            print('{}/{} = {}% completed'.format(self.hunting_df[mask_series].shape[0], self.hunting_df.shape[0],
                                                 int(100 * self.hunting_df[mask_series].shape[0] / self.hunting_df.shape[0])))
        
        return quals_list, file_name
    
    def display_hunting_dataframe_as_histogram(
        self, width_inches=18.0, height_inches=3.0, bin_count=10, verbose=False
    ):
        import matplotlib.pyplot as plt
        fig = plt.figure(figsize=(width_inches, height_inches))
        ax1 = fig.add_subplot(121)
        ax1.set_xlabel('Percentage of Qualified Minimum Requirements met per Job Posting')
        self.hunting_df.percent_fit.hist(
            cumulative=False, density=1, bins=bin_count, ax=ax1, align='mid', rwidth=.9
        )
        
        # Set x axis tick labels
        ax1.set_xticks([-0.2, 0., 0.2, 0.4, 0.6, 0.8, 1., 1.2])
        ax1.set_xticklabels(['', '0%', '20%', '40%', '60%', '80%', '100%', ''])
        
        ax2 = fig.add_subplot(122)
        ax2.set_xlabel('Cumulative Histogram')
        self.hunting_df.percent_fit.hist(cumulative=True, density=1, bins=bin_count, ax=ax2)
        mode = self.hunting_df.percent_fit.mode().squeeze()
        ax2.axvline(mode, linewidth=1.5, color='r', linestyle='-.')
        ax2.axhline(mode, linewidth=1.5, color='r', linestyle='-.')
        plt.tight_layout()