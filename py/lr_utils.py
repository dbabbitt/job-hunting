
#!/usr/bin/env python
# coding: utf-8

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
import pandas as pd
from storage import Storage

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
        pos_df = pd.DataFrame(self.cu.get_execution_results(cypher_str, verbose=verbose))

        # The shape of the Bag-of-words count vector here should be n html strings * m unique tokens
        sents_list = pos_df.navigable_parent.tolist()
        pos_symbol_list = pos_df.pos_symbol.unique().tolist()

        # Re-transform the bag-of-words and tf-idf from the new manual scores
        if s.pickle_exists('POS_CV'):
            self.POS_CV = s.load_object('POS_CV')
        else:
            self.POS_CV = CountVectorizer(analyzer='word', binary=False, decode_error='strict', lowercase=False, max_df=1.0,
                                          max_features=None, min_df=0.0, ngram_range=(1, 5), stop_words=None,
                                          strip_accents='ascii', tokenizer=self.ha.html_regex_tokenizer)
            s.store_objects(POS_CV=self.POS_CV)
        bow_matrix = self.POS_CV.fit_transform(sents_list)

        # Tf-idf must get from Bag-of-words first
        if s.pickle_exists('POS_TT'):
            self.POS_TT = s.load_object('POS_TT')
        else:
            self.POS_TT = TfidfTransformer(norm='l1', smooth_idf=True, sublinear_tf=False, use_idf=True)
            s.store_objects(POS_TT=self.POS_TT)
        tfidf_matrix = self.POS_TT.fit_transform(bow_matrix)
        try:
            import gc
            
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
                                                                  tol=0.0001, verbose=verbose, warm_start=False)
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
    
    def refit_isheader_lr(self, np_df, tfidf_matrix, verbose=False):
            
        # Re-train the classifier
        y = np_df.is_header.values
        try:
            import gc
            
            gc.collect()
            X = tfidf_matrix.toarray()
        except Exception as e:
            print(f'Got this {e.__class__} error in build_isheader_logistic_regression_elements trying ',
                  f'to turn the is_header TF-IDF matrix into a normal array: {str(e).strip()}')
            X = tfidf_matrix
        self.ISHEADER_LR.fit(X, y)
        s.store_objects(ISHEADER_LR=self.ISHEADER_LR)
    
    def build_isheader_logistic_regression_elements(self, verbose=False):
        
        # Get the data
        if not s.pickle_exists('ISHEADER_LR'):
            cypher_str = """
                MATCH (np:NavigableParents)
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
            bow_matrix = self.ISHEADER_CV.fit_transform(sents_list)
            s.store_objects(ISHEADER_CV=self.ISHEADER_CV)
            if not hasattr(self.ISHEADER_CV, 'vocabulary_'):
                self.ISHEADER_CV._validate_vocabulary()
                if not self.ISHEADER_CV.fixed_vocabulary_:
                    from sklearn.exceptions import NotFittedError
                    raise NotFittedError('Vocabulary not fitted or provided')
            if len(self.ISHEADER_CV.vocabulary_) == 0:
                raise ValueError('Vocabulary is empty')
        if s.pickle_exists('ISHEADER_VOCAB'):
            self.ISHEADER_VOCAB = s.load_object('ISHEADER_VOCAB')
        else:
            self.ISHEADER_VOCAB = self.ISHEADER_CV.vocabulary_
            s.store_objects(ISHEADER_VOCAB=self.ISHEADER_VOCAB)
            
        if s.pickle_exists('ISHEADER_TT'):
            self.ISHEADER_TT = s.load_object('ISHEADER_TT')
        else:
            self.ISHEADER_TT = TfidfTransformer(norm='l1', smooth_idf=True, sublinear_tf=False, use_idf=True)
        
        if (not s.pickle_exists('ISHEADER_LR')) or not s.pickle_exists('ISHEADER_TT'):
            
            # Tf-idf must get from Bag-of-words first
            tfidf_matrix = self.ISHEADER_TT.fit_transform(bow_matrix)
            s.store_objects(ISHEADER_TT=self.ISHEADER_TT)
        
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
            self.refit_isheader_lr(np_df, tfidf_matrix, verbose=verbose)
            
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
    def predict_isqualified(self, child_str):
        probs_list = self.ISQUALIFIED_PREDICT_PERCENT_FIT(child_str)
        idx = probs_list.index(max(probs_list))
        is_qualified = [True, False][idx]
        
        return is_qualified
    
    def refit_isqualified_lr(self, np_df, tfidf_matrix, verbose=False):
            
        # Re-train the classifier
        y = np_df.is_qualified.values
        try:
            import gc
            
            gc.collect()
            X = tfidf_matrix.toarray()
        except Exception as e:
            print(f'Got this {e.__class__} error in build_isqualified_logistic_regression_elements trying ',
                  f'to turn the is_qualified TF-IDF matrix into a normal array: {str(e).strip()}')
            X = tfidf_matrix
        self.ISQUALIFIED_LR.fit(X, y)
        s.store_objects(ISQUALIFIED_LR=self.ISQUALIFIED_LR)
    
    def build_isqualified_logistic_regression_elements(self, verbose=False):
        
        # Get the data
        if not s.pickle_exists('ISQUALIFIED_LR'):
            cypher_str = """
                MATCH (np:NavigableParents)
                RETURN
                    np.navigable_parent AS navigable_parent, 
                    np.is_qualified AS is_qualified;"""
            np_df = pd.DataFrame(self.cu.get_execution_results(cypher_str, verbose=verbose))
            np_df.is_qualified = np_df.is_qualified.map(lambda x: {'True': True, 'False': False}[x])
        
        if s.pickle_exists('ISQUALIFIED_CV'):
            self.ISQUALIFIED_CV = s.load_object('ISQUALIFIED_CV')
        else:
            self.ISQUALIFIED_CV = CountVectorizer(analyzer='word', binary=False, decode_error='strict', lowercase=False, max_df=1.0,
                                          max_features=None, min_df=0.0, ngram_range=(1, 5), stop_words=None,
                                          strip_accents='ascii', tokenizer=self.ha.html_regex_tokenizer)
        
        if (not s.pickle_exists('ISQUALIFIED_LR')) or (not s.pickle_exists('ISQUALIFIED_CV')):
            
            # The shape of the Bag-of-words count vector here should be n html strings * m unique tokens
            sents_list = np_df.navigable_parent.tolist()
            
            # Re-transform the bag-of-words and tf-idf from the new manual scores
            bow_matrix = self.ISQUALIFIED_CV.fit_transform(sents_list)
            s.store_objects(ISQUALIFIED_CV=self.ISQUALIFIED_CV)
            if not hasattr(self.ISQUALIFIED_CV, 'vocabulary_'):
                self.ISQUALIFIED_CV._validate_vocabulary()
                if not self.ISQUALIFIED_CV.fixed_vocabulary_:
                    from sklearn.exceptions import NotFittedError
                    raise NotFittedError('Vocabulary not fitted or provided')
            if len(self.ISQUALIFIED_CV.vocabulary_) == 0:
                raise ValueError('Vocabulary is empty')
        if s.pickle_exists('ISQUALIFIED_VOCAB'):
            self.ISQUALIFIED_VOCAB = s.load_object('ISQUALIFIED_VOCAB')
        else:
            self.ISQUALIFIED_VOCAB = self.ISQUALIFIED_CV.vocabulary_
            s.store_objects(ISQUALIFIED_VOCAB=self.ISQUALIFIED_VOCAB)
            
        if s.pickle_exists('ISQUALIFIED_TT'):
            self.ISQUALIFIED_TT = s.load_object('ISQUALIFIED_TT')
        else:
            self.ISQUALIFIED_TT = TfidfTransformer(norm='l1', smooth_idf=True, sublinear_tf=False, use_idf=True)
        
        if (not s.pickle_exists('ISQUALIFIED_LR')) or not s.pickle_exists('ISQUALIFIED_TT'):
            
            # Tf-idf must get from Bag-of-words first
            tfidf_matrix = self.ISQUALIFIED_TT.fit_transform(bow_matrix)
            s.store_objects(ISQUALIFIED_TT=self.ISQUALIFIED_TT)
        
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
            self.refit_isqualified_lr(np_df, tfidf_matrix, verbose=verbose)
            
        self.ISQUALIFIED_PREDICT_PERCENT_FIT = self.build_isqualified_lr_predict_percent(verbose=verbose)
    
    def build_isqualified_lr_predict_percent(self, verbose=False):
        
        # Re-calibrate the inference engine
        cv = CountVectorizer(vocabulary=self.ISQUALIFIED_VOCAB)
        cv._validate_vocabulary()
        
        def predict_percent_fit(navigable_parent):
            '''
            probs_list = lru.ISQUALIFIED_PREDICT_PERCENT_FIT(child_str)
            idx = probs_list.index(max(probs_list))
            is_qualified = [True, False][idx]
            '''

            X_test = self.ISQUALIFIED_TT.transform(cv.transform([navigable_parent])).toarray()
            y_predict_proba = self.ISQUALIFIED_LR.predict_proba(X_test).flatten().tolist()

            return y_predict_proba

        return predict_percent_fit