#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria

from . import nu, hau, cu, time, t0
from IPython.display import clear_output
from .section_classifier_utils import HtmlVectorizer
from sklearn.exceptions import NotFittedError
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
import gc
import numpy as np
import pandas as pd
import re

class LrUtilities(object):
    """Logistic Regression utilities class."""

    def __init__(
        self, sampling_strategy_limit=50, verbose=False
    ):
        self.sampling_strategy_limit = sampling_strategy_limit
        self.verbose = verbose
        
        # Build the Logistic Regression elements
        # from . import slrcu
        # slrcu.build_pos_logistic_regression_elements()
        self.navigable_parent_cypher_str = """
            MATCH (np:NavigableParents {{navigable_parent: '{}'}})
            RETURN
                np.navigable_parent AS navigable_parent,
                np.is_header AS is_header,
                np.""" + """,
                np.""".join([f'{subtype} AS {subtype}' for subtype in cu.subtypes_list]) + """;"""
    
    
    ################################################
    ## Logistic Regression is-qualified functions ##
    ################################################
    def get_to_be_trained_quals(self, basic_quals_dict=None, verbose=False):
        
        # Get the dictionaried quals
        if basic_quals_dict is None:
            self.basic_quals_dict = nu.load_object('basic_quals_dict')
        else:
            self.basic_quals_dict = basic_quals_dict
        rows_list = [
            {
                'qualification_str': qualification_str,
                'is_qualified': is_fit
            } for qualification_str, is_fit in self.basic_quals_dict.items()
        ]
        from pandas import DataFrame
        dictionaried_set = set(DataFrame(rows_list).qualification_str)
        
        # Get the databased quals
        cypher_str = '''
            MATCH (qs:QualificationStrings)
            RETURN qs;'''
        row_objs_list = cu.get_execution_results(cypher_str, verbose=False)
        databased_quals_df = pd.DataFrame(
            [{k: v for k, v in row_obj['qs'].items()} for row_obj in row_objs_list]
        )
        databased_set = set(databased_quals_df.qualification_str)
        
        # Get the qualifications that need to be trained on
        new_qualification_strs_set = dictionaried_set - databased_set
        
        return new_qualification_strs_set
    
    def sync_basic_quals_dict(
        self, sampling_strategy_limit=None, basic_quals_dict=None, verbose=False
    ):
        
        # Get the dictionaried quals
        if basic_quals_dict is None:
            if nu.pickle_exists('basic_quals_dict'):
                self.basic_quals_dict = nu.load_object('basic_quals_dict')
            else:
                self.basic_quals_dict = None
        else:
            self.basic_quals_dict = basic_quals_dict
        if self.basic_quals_dict is None:
            rows_list = []
            qual_dict_set = set()
        else:
            rows_list = [
                {
                    'qualification_str': qualification_str,
                    'is_qualified': is_fit
                } for qualification_str, is_fit in self.basic_quals_dict.items()
            ]
            qual_dict_set = set(self.basic_quals_dict.keys())
        
        # Get the databased quals
        cypher_str = '''
            // Get all qualification strings in the database
            MATCH (qs:QualificationStrings)
            RETURN qs;'''
        row_objs_list = cu.get_execution_results(cypher_str, verbose=False)
        self.basic_quals_df = pd.DataFrame(
            [{k: v for k, v in row_obj['qs'].items()} for row_obj in row_objs_list]
        )
        qual_db_set = set(self.basic_quals_df.qualification_str)
        
        # Get the missing set
        # missing_from_dict_set = qual_db_set - qual_dict_set
        missing_from_db_set = qual_dict_set - qual_db_set
        
        # Ensure that everything in the pickle is also in the database
        def f(tx, qualification_str, is_qualified, verbose=False):
            cypher_str = '''
                MERGE (:QualificationStrings {
                    qualification_str: $qualification_str,
                    is_qualified: $is_qualified
                    });'''
            if verbose:
                clear_output(wait=True)
                print(
                    cypher_str.replace('$qualification_str', f'"{qualification_str}"').replace('$is_qualified', f'"{is_qualified}"')
                )
            parameter_dict = {'qualification_str': qualification_str, 'is_qualified': is_qualified}
            rows_list = []
            for record in tx.run(query=cypher_str, parameters=parameter_dict):
                row_dict = {k: v for k, v in dict(record.items())['fn'].items()}
                rows_list.append(row_dict)
            df = pd.DataFrame(rows_list)

            return df
        for row_dict in rows_list:
            qualification_str = row_dict['qualification_str']
            if qualification_str in missing_from_db_set:
                qual = re.sub(
                    '</?[^<>]*>', r'', qualification_str.strip(), 0, re.MULTILINE
                ).strip()
                if (not qual.endswith(':')):
                    with cu.driver.session() as session:
                        df = session.write_transaction(
                            f, qualification_str=qualification_str,
                            is_qualified=row_dict['is_qualified'], verbose=verbose
                        )
        
        # Get the updated databased quals
        cypher_str = '''
            MATCH (qs:QualificationStrings)
            RETURN qs;'''
        row_objs_list = cu.get_execution_results(cypher_str, verbose=False)
        self.basic_quals_df = pd.DataFrame(
            [{k: v for k, v in row_obj['qs'].items()} for row_obj in row_objs_list]
        )
        
        # Rebuild the dataframe from the database
        if sampling_strategy_limit is not None:
            self.basic_quals_df = nu.rebalance_data(
                self.basic_quals_df, name_column='qualification_str',
                value_column='is_qualified',
                sampling_strategy_limit=sampling_strategy_limit, verbose=verbose
            )
        
        # Clean up the data
        mask_series = (self.basic_quals_df.is_qualified == True)
        self.basic_quals_df.loc[mask_series, 'is_qualified'] = 1
        mask_series = (self.basic_quals_df.is_qualified == False)
        self.basic_quals_df.loc[mask_series, 'is_qualified'] = 0
        nu.store_objects(basic_quals_df=self.basic_quals_df, verbose=False)
        self.basic_quals_dict = self.basic_quals_df.set_index(
            'qualification_str'
        ).is_qualified.to_dict()
        nu.store_objects(basic_quals_dict=self.basic_quals_dict, verbose=False)
    
    def build_isqualified_logistic_regression_elements(
        self, sampling_strategy_limit=None, verbose=False
    ):
        
        # Sync the basic qualifications data
        self.sync_basic_quals_dict(
            sampling_strategy_limit=sampling_strategy_limit, verbose=False
        )
        
        self.ISQUALIFIED_CV = CountVectorizer(
            analyzer='word', binary=False, decode_error='strict', lowercase=False, max_df=1.0,
            max_features=None, min_df=0.0, ngram_range=(1, 5), stop_words=None,
            strip_accents='ascii', tokenizer=hau.html_regex_tokenizer
        )
            
        if nu.pickle_exists('ISQUALIFIED_TT'):
            self.ISQUALIFIED_TT = nu.load_object('ISQUALIFIED_TT')
        else:
            self.ISQUALIFIED_TT = TfidfTransformer(
                norm='l1', smooth_idf=True, sublinear_tf=False, use_idf=True
            )
        
        # The shape of the Bag-of-words count vector here should be n html strings * m unique tokens
        rows_list = [{
                        'qualification_str': qualification_str,
                        'is_qualified': is_fit
                      } for qualification_str, is_fit in self.basic_quals_dict.items()]
        self.basic_quals_df = pd.DataFrame(rows_list)
        transform_dict = {'True': 1, 'False': 0, True: 1, False: 0, 1: 1, 0: 0, 2: 1}
        self.basic_quals_df.is_qualified = self.basic_quals_df.is_qualified.map(
            lambda x: transform_dict[x]
        )
        sents_list = self.basic_quals_df.qualification_str.tolist()
            
        # Tf-idf must get from Bag-of-words first
        tfidf_matrix = self.get_isqualified_tfidf_matrix(sents_list=sents_list, verbose=verbose)
            
        if nu.pickle_exists('ISQUALIFIED_VOCAB'):
            self.ISQUALIFIED_VOCAB = nu.load_object('ISQUALIFIED_VOCAB')
        else:
            self.ISQUALIFIED_VOCAB = self.ISQUALIFIED_CV.vocabulary_
            nu.store_objects(ISQUALIFIED_VOCAB=self.ISQUALIFIED_VOCAB, verbose=verbose)
        
        if nu.pickle_exists('ISQUALIFIED_LR'):
            self.ISQUALIFIED_LR = nu.load_object('ISQUALIFIED_LR')
        else:
            self.ISQUALIFIED_LR = LogisticRegression(
                C=375.0, class_weight='balanced', dual=False, fit_intercept=True, 
                intercept_scaling=1, l1_ratio=None, max_iter=1000,
                multi_class='auto', n_jobs=None, penalty='l1', random_state=None,
                solver='liblinear', tol=0.0001, verbose=False, warm_start=True
            )
            self.refit_isqualified_lr(tfidf_matrix, verbose=verbose)

        # Re-calibrate the inference engine
        self.predict_job_hunt_percent_fit = self.build_isqualified_lr_predict_percent(
            verbose=verbose
        )
    
    def get_quals_str(self, prediction_list, quals_list, verbose=True):
        qual_count = 0
        quals_str = ''
        if verbose:
            from tqdm import tqdm
            progress_bar = tqdm(
                zip(prediction_list, enumerate(quals_list)), total=len(quals_list),
                desc="List Predictions of Qualifications"
            )
        else:
            progress_bar = zip(prediction_list, enumerate(quals_list))
        for pred_array, (i, qual_str) in progress_bar:
            if qual_str in self.basic_quals_dict:
                formatted_str = '\nquals_list[{}] = "{}" ({})'
                prediction = round(float(self.basic_quals_dict[qual_str]), 4)
            else:
                formatted_str = '\n*quals_list[{}] = "{}" ({})'
                prediction = round(float(pred_array[1]), 4)
            quals_str += formatted_str.format(i, re.sub(r'\s+<', '<', re.sub(r'>\s+', '>', qual_str)), prediction)
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
        nu.store_objects(hunting_df=self.hunting_df, verbose=False)
        
        def f(tx, file_name, percent_fit, verbose=False):
            cypher_str = """
                MATCH (fn:FileNames {file_name: $file_name})
                SET fn.percent_fit = $percent_fit;"""
            if verbose:
                clear_output(wait=True)
                print(cypher_str.replace('$file_name', f'"{file_name}"').replace('$percent_fit', f'"{percent_fit}"'))
            parameter_dict = {'file_name': file_name, 'percent_fit': percent_fit}
            tx.run(query=cypher_str, parameters=parameter_dict)
        
        with cu.driver.session() as session:
            session.write_transaction(f, file_name=row_series.file_name, percent_fit=percent_fit, verbose=verbose)
    
    def predict_isqualified(self, child_str):
        if not isinstance(child_str, list):
            child_str = [child_str]
        
        probs_array = self.predict_job_hunt_percent_fit(child_str)
        
        # If probs_array is 2D (multiple inputs), we need to handle each row
        # Assume 1 is the "qualified" class
        if probs_array.ndim == 2:
            is_qualified_list = []
            for probs in probs_array:
                idx = np.argmax(probs)
                is_qualified = (idx == 1)
                is_qualified_list.append(is_qualified)
            
            return is_qualified_list
        
        # If it's 1D (single input)
        else:
            idx = np.argmax(probs_array)
            is_qualified = (idx == 1)
            
            return is_qualified
    
    def get_isqualified_tfidf_matrix(
        self, sents_list=None, bow_matrix=None, verbose=False
    ):
        '''Learn the vocabulary dictionary and return the document-term matrix'''
        if sents_list is None:
            
            # The shape of the Bag-of-words count vector here
            # should be n html strings * m unique tokens
            sents_list = self.basic_quals_df.qualification_str.tolist()
            
        if bow_matrix is None:
            
            # Re-transform the bag-of-words and tf-idf from the new manual scores
            bow_matrix = self.ISQUALIFIED_CV.fit_transform(sents_list)
            
            # Get the new vocabulary to be used in the count
            # vectorizer in the predict_percent_fit function
            if not hasattr(self.ISQUALIFIED_CV, 'vocabulary_'):
                self.ISQUALIFIED_CV._validate_vocabulary()
                if not self.ISQUALIFIED_CV.fixed_vocabulary_:
                    raise NotFittedError('Vocabulary not fitted or provided')
            if len(self.ISQUALIFIED_CV.vocabulary_) == 0:
                raise ValueError('Vocabulary is empty')
            self.ISQUALIFIED_VOCAB = self.ISQUALIFIED_CV.vocabulary_
        
        # Tf-idf must get from Bag-of-words first
        tfidf_matrix = self.ISQUALIFIED_TT.fit_transform(bow_matrix)
        nu.store_objects(ISQUALIFIED_TT=self.ISQUALIFIED_TT, verbose=False)
        
        return tfidf_matrix
    
    def refit_isqualified_lr(self, X, y=None, verbose=False):
        
        # Re-train the classifier
        if y is None:
            y = self.basic_quals_df.is_qualified.to_numpy().astype(int)
        self.ISQUALIFIED_LR.fit(X, y)
        nu.store_objects(ISQUALIFIED_LR=self.ISQUALIFIED_LR, verbose=verbose)
    
    def build_isqualified_lr_predict_percent(self, verbose=False):
        if verbose:
            print(f'I have {len(self.ISQUALIFIED_VOCAB):,} is-qualified vocabulary tokens in here')
        
        # Re-calibrate the inference engine
        INFERENCE_CV = CountVectorizer(vocabulary=self.ISQUALIFIED_VOCAB)
        INFERENCE_CV._validate_vocabulary()
        
        f = None
        def f(quals_list, verbose=False):
            y_predict_proba = np.array([])
            
            # The TFIDF Vectorizer expects an array of strings
            if len(quals_list) and all([isinstance(qual_str, str) for qual_str in quals_list]):
                count_matrix = INFERENCE_CV.transform(quals_list)
                
                # Transform the count matrix to a tf-idf representation
                X_test = self.ISQUALIFIED_TT.transform(count_matrix).toarray()
                
                y_predict_proba = self.ISQUALIFIED_LR.predict_proba(X_test)
            
            return y_predict_proba
        
        return f
    
    def retrain_isqualified_classifier(self, verbose=False):

        # Get all our file names data
        cypher_str = '''
            MATCH (fn:FileNames)
            RETURN fn;'''
        row_objs_list = cu.get_execution_results(cypher_str, verbose=False)
        self.hunting_df = pd.DataFrame(
            [{k: v for k, v in row_obj['fn'].items()} for row_obj in row_objs_list]
        )
        self.max_togo = self.hunting_df.shape[0] - self.hunting_df[self.hunting_df.percent_fit >= 0.0].shape[0]
        
        # Get everything in the dictionary
        rows_list = [
            {
                'qualification_str': qualification_str,
                'is_qualified': is_fit
            } for qualification_str, is_fit in self.basic_quals_dict.items()
        ]
        self.basic_quals_df = pd.DataFrame(rows_list)
        
        if verbose:
            print(f'I have {self.basic_quals_df.shape[0]:,} hand-labeled qualification strings in here')

        # Get the new manual scores
        sents_list = self.basic_quals_df.qualification_str.tolist()
        tfidf_matrix = self.get_isqualified_tfidf_matrix(sents_list=sents_list, verbose=verbose)

        # Re-train the classifier
        self.refit_isqualified_lr(tfidf_matrix, verbose=False)

        # Re-calibrate the inference engine
        self.predict_job_hunt_percent_fit = self.build_isqualified_lr_predict_percent(verbose=verbose)
    
    def infer_from_hunting_dataframe(self, fitness_threshold=2/3, verbose=True):
        
        # Loop through all the unset %fit values, set them if you can,
        # break for help if you can't
        mask_series = (self.hunting_df.percent_fit >= 0.0)
        quals_list = []
        file_name = None
        from . import su
        for row_index, row_series in self.hunting_df[~mask_series].iterrows():
            file_name = row_series.file_name
            quals_list, job_fitness = su.print_fit_job(
                row_index, row_series, fitness_threshold=fitness_threshold, verbose=verbose
            )
            if job_fitness >= fitness_threshold:
                if all(qual_str in self.basic_quals_dict for qual_str in quals_list):
                    self.update_hunting(row_index, row_series, quals_list)
                else: break
            elif len(quals_list) and all(
                [isinstance(qual_str, str) for qual_str in quals_list]
            ):
                self.update_hunting(row_index, row_series, quals_list)
        if verbose:
            processed_count = self.hunting_df[mask_series].shape[0]
            total_postings = self.hunting_df.shape[0]
            percent_completed = 100 * processed_count / total_postings
            mpp = round(((time.time() - t0)//60)/self.max_togo, 1) if self.max_togo else "N/A"
            print(
                '{} left to go: {}/{} = {}% completed (taking about {} minutes per post)'.format(
                    total_postings - processed_count, processed_count, total_postings,
                    round(percent_completed, 2), mpp
                )
            )
        
        return quals_list, file_name
    
    def display_hunting_dataframe_as_histogram(
        self, width_inches=18.0, height_inches=3.0, show_second_plot=False, verbose=False
    ):
        import matplotlib.pyplot as plt
        fig = plt.figure(figsize=(width_inches, height_inches))
        if show_second_plot:
            ax1 = fig.add_subplot(121)
        else:
            ax1 = fig.add_subplot(111)
        ax1.set_xlabel('Percentage of Minimum Requirements qualified-for (met) per Job Posting')
        self.hunting_df.percent_fit.hist(
            cumulative=False, density=1, bins=11, ax=ax1, align='mid', rwidth=.9
        )
        
        # Set x axis tick labels
        numbers_list = [-0.1] + [0.05 + 0.09 * i for i in range(11)] + [1.1]
        labels_list = [''] + [f'{i*10}%' for i in range(11)] + ['']
        ax1.set_xticks(numbers_list)
        ax1.set_xticklabels(labels_list)
        if verbose:
            print(numbers_list)
            print(pd.Series(numbers_list).diff().tolist())
        
        # Add the record count text in the upper left quadrant
        n_value = self.hunting_df.shape[0]
        ax1.text(
            x=0.07, y=0.9, s=f'$n = {n_value:,}$',
            transform=ax1.transAxes, fontsize=12, verticalalignment='top'
        )
        
        # Turn off the grid
        ax1.grid(False)
        
        # Turn off the y ticks
        ax1.set_yticks([])
        
        # Turn off the y tick labels
        ax1.set_yticklabels([])
        
        if show_second_plot:
            ax2 = fig.add_subplot(122)
            ax2.set_xlabel('Cumulative Histogram')
            self.hunting_df.percent_fit.hist(cumulative=True, density=1, bins=11, ax=ax2)
            xy = self.hunting_df.percent_fit.mode().squeeze()
            ax2.axvline(xy, linewidth=1.5, color='r', linestyle='-.')
            ax2.axhline(xy, linewidth=1.5, color='r', linestyle='-.')
            
            # Turn off the grid
            ax2.grid(False)
            
            # Turn off the y ticks
            ax2.set_yticks([])
            
            # Turn off the y tick labels
            ax2.set_yticklabels([])
        
        plt.tight_layout()