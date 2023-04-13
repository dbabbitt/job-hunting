#!/usr/bin/env python
# coding: utf-8


# Soli Deo gloria

# from section_classifier_utils import (
    # rebalance_data, SectionLRClassifierUtilities, HtmlVectorizer,
    # SectionSGDClassifierUtilities, SectionCRFClassifierUtilities
# )

from pandas import DataFrame
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from nltk import pos_tag

def rebalance_data(
    unbalanced_df, name_column, value_column, sampling_strategy_limit, verbose=False
):
    
    # Create the random under-sampler
    counts_dict = unbalanced_df.groupby(value_column).count()[name_column].to_dict()
    sampling_strategy = {k: min(sampling_strategy_limit, v) for k, v in counts_dict.items()}
    from imblearn.under_sampling import RandomUnderSampler
    rus = RandomUnderSampler(sampling_strategy=sampling_strategy)
    
    # Define the tuple of arrays
    data = rus.fit_resample(
        unbalanced_df[name_column].values.reshape(-1, 1),
        unbalanced_df[value_column].values.reshape(-1, 1)
    )
    
    # Recreate the Pandas DataFrame
    rebalanced_df = DataFrame(data[0], columns=[name_column])
    rebalanced_df[value_column] = data[1]
    
    return rebalanced_df

class HtmlVectorizer:
    pos_relationships_vocab = None

    def __init__(self, ha, verbose=False):
        self.ha = ha
        self.verbose = verbose
        self.vectorizer = CountVectorizer(
            lowercase=True, tokenizer=self.ha.html_regex_tokenizer,
            ngram_range=(1, 3)
        )
    
    def fit_transform(self, corpus):
        self.vectorizer.fit(corpus)
        HtmlVectorizer.pos_relationships_vocab = self.vectorizer.vocabulary_
        
        return self.vectorizer.transform(corpus)
    
    def transform(self, corpus):
        
        return self.vectorizer.transform(corpus)

    @classmethod
    def restore_vocabulary(cls):
        if cls.pos_relationships_vocab is None:
            raise ValueError('Vocabulary has not been trained yet')
        vectorizer = CountVectorizer(
            lowercase=True, tokenizer=self.ha.html_regex_tokenizer,
            ngram_range=(1, 3), vocabulary=cls.pos_relationships_vocab
        )
        
        return vectorizer

    def validate_and_restore_vocab(self):
        if not hasattr(self.vectorizer, 'vocabulary_'):
            self.vectorizer._validate_vocabulary()
            if not self.vectorizer.fixed_vocabulary_:
                self.vectorizer = HtmlVectorizer.restore_vocabulary()
        if len(self.vectorizer.vocabulary_) == 0:
            raise ValueError('Vocabulary is empty')


###################################################
## Logistic Regression parts-of-speech functions ##
###################################################
class SectionLRClassifierUtilities(object):
    '''A class for all the job-posting-section logistic regression predictive models'''
    def __init__(self, ha, cu, verbose=False):
        self.ha = ha
        self.cu = cu
        self.verbose = verbose
        
        # Seek a Storage object
        if self.cu and hasattr(self.cu, 's'):
            self.s = self.cu.s
        elif self.ha and hasattr(self.ha, 's'):
            self.s = self.ha.s
        else:
            self.s = None

    
    def build_pos_logistic_regression_elements(
        self, sampling_strategy_limit=None, verbose=False
    ):
        '''Train a model for each labeled POS symbol'''
        if self.s and self.s.pickle_exists('slrcu.count_vect'):
            self.count_vect = self.s.load_object('slrcu.count_vect')
        else:
            self.count_vect = HtmlVectorizer(ha=self.ha, verbose=verbose)
        if self.s and self.s.pickle_exists('slrcu.tfidf_transformer'):
            self.tfidf_transformer = self.s.load_object('slrcu.tfidf_transformer')
        else:
            self.tfidf_transformer = TfidfTransformer(
                norm='l1', smooth_idf=True, sublinear_tf=False, use_idf=True
            )
        if self.s and self.s.pickle_exists('slrcu_classifier_dict'):
            self.classifier_dict = self.s.load_object('slrcu_classifier_dict')
            is_already_fitted = True
        else:
            self.classifier_dict = {}
            is_already_fitted = False
        self.pos_predict_percent_fit_dict = {}
        
        # Get the labeled training data
        pos_df = self.cu.get_pos_relationships(verbose=False)

        # Rebalance the data with the sampling strategy limit
        if sampling_strategy_limit is not None:
            pos_df = self.rebalance_data(
                pos_df, name_column='navigable_parent', value_column='pos_symbol',
                sampling_strategy_limit=sampling_strategy_limit, verbose=verbose
            )

        # Fit-transform the Bag-of-words from these hand-labeled HTML strings
        sents_list = pos_df.navigable_parent.tolist()
        if verbose:
            print(f'I have {len(sents_list):,} labeled parts of speech in here')

        # The shape of the Bag-of-words count vector here should be
        # `n` html strings * `m` unique parts-of-speech tokens
        # Learn the vocabulary dictionary
        bow_matrix = self.count_vect.fit_transform(sents_list)

        # Document-term matrix has as input the Bag-of-words
        X_train_tfidf = self.tfidf_transformer.fit_transform(bow_matrix)
        
        from sklearn.linear_model import LogisticRegression
        def fit_classifier_dict(pos_symbol, X_train_tfidf, train_data_list):
            try:
                
                # Train on initial data
                self.classifier_dict[pos_symbol].fit(X_train_tfidf, train_data_list)
                if self.s:
                    self.s.store_objects(
                        slrcu_classifier_dict=self.classifier_dict, verbose=False
                    )
                
                inference_func = self.build_predict_percent_fit_function(
                    pos_symbol, verbose=verbose
                )
                self.pos_predict_percent_fit_dict[pos_symbol] = inference_func
            except ValueError as e:
                print(f'Fitting {pos_symbol} had this error: {str(e).strip()}')
                self.classifier_dict.pop(pos_symbol, None)
                self.pos_predict_percent_fit_dict.pop(pos_symbol, None)
        for pos_symbol in pos_df.pos_symbol.unique():

            # Train the classifier
            mask_series = (pos_df.pos_symbol == pos_symbol)
            train_data_list = mask_series.to_numpy()
            if pos_symbol not in self.classifier_dict:
                self.classifier_dict[pos_symbol] = LogisticRegression(
                    C=375.0, class_weight='balanced', max_iter=1000, penalty='l1',
                    solver='liblinear', verbose=False, warm_start=True
                )
                fit_classifier_dict(pos_symbol, X_train_tfidf, train_data_list)
            elif not is_already_fitted:
                fit_classifier_dict(pos_symbol, X_train_tfidf, train_data_list)
            else:
                try:
                    inference_func = self.build_predict_percent_fit_function(
                        pos_symbol, verbose=verbose
                    )
                    self.pos_predict_percent_fit_dict[pos_symbol] = inference_func
                except ValueError as e:
                    print(f'Fitting {pos_symbol} had this error: {str(e).strip()}')
                    self.pos_predict_percent_fit_dict.pop(pos_symbol, None)
    
    def predict_single(self, html_str, verbose=False):
        '''Predict the labels for the input data'''
        tuple_list = []
        for pos_symbol, predict_percent_fit in self.pos_predict_percent_fit_dict.items():
            if predict_percent_fit is None:
                proba_tuple = (pos_symbol, 0.0)
                tuple_list.append(proba_tuple)
            else:
                proba_tuple = (pos_symbol, predict_percent_fit(html_str))
                tuple_list.append(proba_tuple)
        tuple_list.sort(reverse=True, key=lambda x: x[1])

        return tuple_list[0][0]

    def build_predict_percent_fit_function(self, pos_symbol, verbose=False):
        predict_percent_fit = None
        if pos_symbol in self.classifier_dict:

            def predict_percent_fit(navigable_parent):

                X_test = self.tfidf_transformer.transform(
                    self.count_vect.transform([navigable_parent])
                ).toarray()
                y_predict_proba = self.classifier_dict[pos_symbol].predict_proba(X_test)[0][1]

                return y_predict_proba

        return predict_percent_fit


###########################################################
## Stochastic Gradient Descent parts-of-speech functions ##
###########################################################
class SectionSGDClassifierUtilities(object):
    '''
    A class for all the job-posting-section stochastic gradient descent predictive models
    '''
    def __init__(self, ha, cu, verbose=False):
        self.ha = ha
        self.cu = cu
    
    
    def build_pos_stochastic_gradient_descent_elements(
        self, sampling_strategy_limit=None, verbose=False
    ):
        '''Train a model for each labeled POS symbol'''
        self.count_vect = HtmlVectorizer(ha=self.ha, verbose=verbose)
        self.tfidf_transformer = TfidfTransformer(
            norm='l1', smooth_idf=True, sublinear_tf=False, use_idf=True
        )
        self.classifier_dict = {}
        self.pos_predict_percent_fit_dict = {}
        
        # Get the labeled training data
        pos_df = self.cu.get_pos_relationships(verbose=False)

        # Rebalance the data with the sampling strategy limit
        if sampling_strategy_limit is not None:
            pos_df = self.rebalance_data(
                pos_df, name_column='navigable_parent', value_column='pos_symbol',
                sampling_strategy_limit=sampling_strategy_limit, verbose=verbose
            )

        # Fit-transform the Bag-of-words from these hand-labeled HTML strings
        sents_list = pos_df.navigable_parent.tolist()
        if verbose:
            print(f'I have {len(sents_list):,} labeled parts of speech in here')

        # The shape of the Bag-of-words count vector here should be
        # `n` html strings * `m` unique parts-of-speech tokens
        # Learn the vocabulary dictionary
        bow_matrix = self.count_vect.fit_transform(sents_list)

        # Document-term matrix has as input the Bag-of-words
        X_train_tfidf = self.tfidf_transformer.fit_transform(bow_matrix)
        
        from sklearn.linear_model import SGDClassifier
        for pos_symbol in pos_df.pos_symbol.unique():

            # Train the classifier
            mask_series = (pos_df.pos_symbol == pos_symbol)
            train_data_list = mask_series.to_numpy()
            if pos_symbol not in self.classifier_dict:
                self.classifier_dict[pos_symbol] = SGDClassifier(
                    loss='log', warm_start=True
                )
            try:
                
                # Train on initial data
                self.classifier_dict[pos_symbol].fit(X_train_tfidf, train_data_list)
                
                inference_func = self.build_predict_percent_fit_function(
                    pos_symbol, verbose=verbose
                )
                self.pos_predict_percent_fit_dict[pos_symbol] = inference_func
            except ValueError as e:
                print(f'Fitting {pos_symbol} had this error: {str(e).strip()}')
                self.classifier_dict.pop(pos_symbol, None)
                self.pos_predict_percent_fit_dict.pop(pos_symbol, None)

    def predict_single(self, html_str, verbose=False):
        '''Predict the labels for the input data'''
        tuple_list = []
        for pos_symbol, predict_percent_fit in self.pos_predict_percent_fit_dict.items():
            if predict_percent_fit is None:
                proba_tuple = (pos_symbol, 0.0)
                tuple_list.append(proba_tuple)
            else:
                proba_tuple = (pos_symbol, predict_percent_fit(html_str))
                tuple_list.append(proba_tuple)
        tuple_list.sort(reverse=True, key=lambda x: x[1])

        return tuple_list[0][0]
    
    def build_predict_percent_fit_function(self, pos_symbol, verbose=False):
        predict_percent_fit = None
        if pos_symbol in self.classifier_dict:

            def predict_percent_fit(navigable_parent):

                X_test = self.tfidf_transformer.transform(
                    self.count_vect.transform([navigable_parent])
                ).toarray()
                y_predict_proba = self.classifier_dict[pos_symbol].predict_proba(X_test)

                return y_predict_proba.flatten().tolist()[-1]

        return predict_percent_fit

#########################################################
## Conditional Random Fields parts-of-speech functions ##
#########################################################
class SectionCRFClassifierUtilities(object):
    '''
    A class for all the job-posting-section conditional random fields predictive models
    '''
    def __init__(self, cu, ha=None, verbose=False):
        self.cu = cu
        
        # Seek a HeaderAnalysis object
        if self.cu and hasattr(self.cu, 'ha'):
            self.ha = self.cu.ha
        else:
            self.ha = ha
        
        # Seek a Storage object
        if self.cu and hasattr(self.cu, 's'):
            self.s = self.cu.s
        elif self.ha and hasattr(self.ha, 's'):
            self.s = self.ha.s
        else:
            self.s = None
    
    # Define features to be used in the CRF model
    def word2features(self, sent, i):
        word = sent[i][0]
        postag = sent[i][1]
        features = {
            'word': word,
            'postag': postag
        }

        return features
    
    
    def sent2features(self, sent):

        return [self.word2features(sent, i) for i in range(len(sent))]
    
    
    def sent2labels(self, pos_symbol, sent):

        return [pos_symbol] * len(sent)
    
    
    def build_pos_conditional_random_field_elements(
        self, sampling_strategy_limit=None, verbose=False
    ):
        '''Train a model for each labeled POS symbol'''
        
        self.pos_predict_percent_fit_dict = {}
        
        # Create the CRF model
        if self.s and self.s.pickle_exists('scrfcu_pos_symbol_crf'):
            self.pos_symbol_crf = self.s.load_object('scrfcu_pos_symbol_crf')
            is_already_fitted = True
        else:
            import sklearn_crfsuite
            self.pos_symbol_crf = sklearn_crfsuite.CRF()
            is_already_fitted = False
        
        # Get the labeled training data
        pos_df = self.cu.get_pos_relationships(verbose=False)
        
        # Rebalance the data with the sampling strategy limit
        if sampling_strategy_limit is not None:
            pos_df = rebalance_data(
                pos_df, name_column='navigable_parent', value_column='pos_symbol',
                sampling_strategy_limit=sampling_strategy_limit, verbose=verbose
            )
        
        if not is_already_fitted:
            
            # Sentences to parse
            sents_list = pos_df.navigable_parent.tolist()
            if verbose:
                print(f'I have {len(sents_list):,} labeled parts of speech in here')
            
            # Tokenize the sentences
            tokens_list = [self.ha.html_regex_tokenizer(sentence) for sentence in sents_list]
            
            # Get the parts of speech
            pos_tags_list = [pos_tag(tokens) for tokens in tokens_list]
            
            # Labels to apply
            pos_symbols_list = pos_df.pos_symbol.tolist()
            
            # Prepare the training and test data
            feature_dicts_list = [self.sent2features(pos_tags) for pos_tags in pos_tags_list]
            y = [self.sent2labels(pos_symbol, pos_tag) for pos_tag, pos_symbol in zip(
                pos_tags_list, pos_symbols_list
            )]
            
            # Train on initial data
            self.pos_symbol_crf.fit(feature_dicts_list, y)
            if self.s:
                self.s.store_objects(scrfcu_pos_symbol_crf=self.pos_symbol_crf)
        
        for pos_symbol in pos_df.pos_symbol.unique():
            try:
                percent_fit = self.build_predict_percent_fit_function(
                    pos_symbol, verbose=verbose
                )
                self.pos_predict_percent_fit_dict[pos_symbol] = percent_fit
            except ValueError as e:
                print(f'Fitting {pos_symbol} had this error: {str(e).strip()}')
                self.pos_predict_percent_fit_dict.pop(pos_symbol, None)

    def predict_single(self, html_str, verbose=False):
        '''Predict the labels for the input data'''
        y_pred = 'O-O'
        tokens_list = [self.ha.html_regex_tokenizer(html_str)]
        if tokens_list != [[]]:
            pos_tags_list = [pos_tag(tokens) for tokens in tokens_list]
            feature_dicts_list = [self.sent2features(pos_tags) for pos_tags in pos_tags_list]
            y_pred = self.pos_symbol_crf.predict(feature_dicts_list)[0][0]

        return y_pred
    
    def build_predict_percent_fit_function(self, pos_symbol, verbose=False):
        predict_percent_fit = None
        import numpy as np
        
        def predict_percent_fit(html_str):
            y_pred = 0.0
            tokens_list = [self.ha.html_regex_tokenizer(html_str)]
            if tokens_list != [[]]:
                pos_tags_list = [pos_tag(tokens) for tokens in tokens_list]
                X = [self.sent2features(pos_tags) for pos_tags in pos_tags_list]
                symbols_dicts_list = self.pos_symbol_crf.predict_marginals(X)[0]
                y_pred = np.mean([symbol_dict[pos_symbol] for symbol_dict in symbols_dicts_list])
            
            return y_pred
        
        return predict_percent_fit