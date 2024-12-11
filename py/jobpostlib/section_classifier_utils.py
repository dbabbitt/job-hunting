#!/usr/bin/env python
# coding: utf-8


# Soli Deo gloria

from . import nu, hau, cu
from pandas import DataFrame
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from nltk import pos_tag

def rebalance_data(
    unbalanced_df: DataFrame,
    name_column: str,
    value_column: str,
    sampling_strategy_limit: int,
    verbose: bool = False,
):
    """
    Rebalances the given unbalanced DataFrame by under-sampling the majority
    class(es) to the specified sampling_strategy_limit.
    
    Parameters:
        unbalanced_df (pandas.DataFrame): The unbalanced DataFrame to rebalance.
        name_column (str): The name of the column containing the class labels.
        value_column (str): The name of the column containing the values associated
            with each class label.
        sampling_strategy_limit (int): The maximum number of samples to keep for
            each class label.
        verbose (bool, optional): Whether to print debug output during the
            rebalancing process. Defaults to False.
    
    Returns:
        pandas.DataFrame: A rebalanced DataFrame with an undersampled majority class.
    """
    
    # Step 1: Create the random under-sampler
    if verbose: print("Creating the random under-sampler...")
    
    counts_dict = unbalanced_df.groupby(value_column).count()[name_column].to_dict()
    sampling_strategy = {k: min(sampling_strategy_limit, v) for k, v in counts_dict.items()}
    
    from imblearn.under_sampling import RandomUnderSampler
    rus = RandomUnderSampler(sampling_strategy=sampling_strategy)
    
    # Step 2: Define the tuple of arrays
    if verbose: print("Resampling the data...")
    
    data = rus.fit_resample(
        unbalanced_df[name_column].values.reshape(-1, 1),
        unbalanced_df[value_column].values.reshape(-1, 1),
    )
    
    # Step 3: Recreate the Pandas DataFrame
    if verbose: print("Converting data to Pandas DataFrame...")
    
    rebalanced_df = DataFrame(data[0], columns=[name_column])
    rebalanced_df[value_column] = data[1]
    
    return rebalanced_df

class HtmlVectorizer:
    """
    Convert a collection of HTML documents to a matrix of token counts.

    This class uses the CountVectorizer from scikit-learn to vectorize HTML documents
    into a matrix of token counts, considering n-grams in the specified range.

    Parameters:
        verbose (bool, optional): Whether to print debug output during the vectorization process. Defaults to False.

    Attributes:
        verbose (bool): Flag indicating whether to print verbose output.
        count_vect (CountVectorizer): The scikit-learn CountVectorizer configured for HTML tokenization.
        pos_relationships_vocab (dict): Vocabulary mapping words to indices after fitting.

    Methods:
        fit_transform(corpus): Fit the count_vect to the corpus and transform it.
        transform(corpus): Transform a given corpus using the already fitted count_vect.
        restore_vocabulary(): Restore the vocabulary using the stored pos_relationships_vocab.
        validate_and_restore_vocab(): Validate and restore the vocabulary if needed.
    """
    pos_relationships_vocab = None

    def __init__(self):
        """
        Constructs an HtmlVectorizer instance.

        Parameters:
            verbose (bool, optional): Whether to print debug output during the vectorization process. Defaults to False.
        """
        self.count_vect = CountVectorizer(
            lowercase=True, tokenizer=hau.html_regex_tokenizer,
            ngram_range=(1, 3)
        )
    
    def fit_transform(self, corpus, verbose=False):
        """
        Fits the count_vect to the given corpus and transforms the corpus into a document-term matrix.

        Parameters:
            corpus (list[str]): A list of HTML documents.

        Returns:
            scipy.sparse.csr_matrix: Transformed matrix of token counts.
        """
        if verbose: print(dir(self))
        self.count_vect.fit(corpus)
        HtmlVectorizer.pos_relationships_vocab = self.count_vect.vocabulary_
        
        return self.count_vect.transform(corpus)
    
    def transform(self, corpus):
        """
        Transform a given corpus using the already fitted count_vect.

        Parameters:
            corpus (list[str]): A list of HTML documents.

        Returns:
            scipy.sparse.csr_matrix: Transformed matrix of token counts.
        """
        
        return self.count_vect.transform(corpus)

    @classmethod
    def restore_vocabulary(cls):
        """
        Restores the vocabulary from a previously trained count_vect.

        Raises:
            ValueError: If the vocabulary has not been trained yet.

        Returns:
            CountVectorizer: A CountVectorizer instance with the restored vocabulary.
        """
        if cls.pos_relationships_vocab is None: raise ValueError('Vocabulary has not been trained yet')
        count_vect = CountVectorizer(
            lowercase=True, tokenizer=hau.html_regex_tokenizer,
            ngram_range=(1, 3), vocabulary=cls.pos_relationships_vocab
        )
        
        return count_vect

    def validate_and_restore_vocab(self):
        """
        Validates and restores the vocabulary if necessary.

        Raises:
            ValueError: If the vocabulary is empty or has not been trained yet.
        """
        if not hasattr(self.count_vect, 'vocabulary_'):
            self.count_vect._validate_vocabulary()
            if not self.count_vect.fixed_vocabulary_: self.count_vect = HtmlVectorizer.restore_vocabulary()
        if len(self.count_vect.vocabulary_) == 0: raise ValueError('Vocabulary is empty')


###################################################
## Logistic Regression parts-of-speech functions ##
###################################################
class SectionLRClassifierUtilities(object):
    '''
    A class for all the job-posting-section logistic regression predictive models
    
    Parameters:
        verbose (bool, optional): Whether to print debug output (default: False)
    
    Attributes:
        verbose (bool): If True, print debug output during processing.
    '''
    def __init__(self, verbose=False):
        '''
        Constructor for the SectionLRClassifierUtilities class
        
        Initialize class attributes:
            verbose (bool, optional): Whether to print debug output (default: False)
        '''
        self.verbose = verbose
    
    
    def build_pos_logistic_regression_elements(
        self, sampling_strategy_limit=None, verbose=False
    ):
        '''
        Train a model for each labeled POS symbol.
        
        Parameters:
            sampling_strategy_limit (int or None, optional): Limit for sampling
                strategy, by default None.
            verbose (bool, optional): If True, print additional information during
                execution, by default False.
        '''
        if verbose:
            from tqdm import tqdm
            import sys
        
        # Check if count_vect has been saved and load it, otherwise create a new one
        if nu.pickle_exists('slrcu.count_vect'):
            self.count_vect = nu.load_object('slrcu.count_vect')
        else:
            self.count_vect = HtmlVectorizer()
        
        # Load or create the TF-IDF transformer
        if nu.pickle_exists('slrcu.tfidf_transformer'):
            self.tfidf_transformer = nu.load_object('slrcu.tfidf_transformer')
        else:
            self.tfidf_transformer = TfidfTransformer(
                norm='l1', smooth_idf=True, sublinear_tf=False, use_idf=True
            )
        
        # Load or create the logistic regression classifiers
        if nu and nu.pickle_exists('slrcu_classifier_dict'):
            self.classifier_dict = nu.load_object('slrcu_classifier_dict')
            is_already_fitted = True
        else:
            self.classifier_dict = {}
            is_already_fitted = False
        
        # Initialize the percent-fit dictionary
        self.pos_predict_percent_fit_dict = {}
        
        # Get the labeled training data
        pos_df = cu.get_pos_relationships(verbose=False)
        
        # Rebalance the data with the sampling strategy limit if necessary
        if sampling_strategy_limit is not None:
            pos_df = self.rebalance_data(
                pos_df, name_column='navigable_parent', value_column='pos_symbol',
                sampling_strategy_limit=sampling_strategy_limit, verbose=verbose
            )
        
        # Fit-transform the Bag-of-words from these hand-labeled HTML strings
        sents_list = pos_df.navigable_parent.tolist()
        if verbose:
            print(f'I have {len(sents_list):,} labeled parts of speech in here', file=sys.stderr)
        
        # Learn the vocabulary dictionary
        bow_matrix = self.count_vect.fit_transform(sents_list)
        
        # Note: the shape of the Bag-of-words count vector here should be
        #       html strings count * unique parts-of-speech tokens count
        assert bow_matrix.shape[0] == len(sents_list), "The first dimension of the Bag-of-words count vector does not match the html strings count"
        assert len(self.count_vect.pos_relationships_vocab) == bow_matrix.shape[1], "The second dimension of the Bag-of-words count vector does not match the unique POS tokens count"
        
        # Fit the TF-IDF transformer
        X_train_tfidf = self.tfidf_transformer.fit_transform(bow_matrix)
        
        # Define a function to fit the classifier and store the results
        from sklearn.linear_model import LogisticRegression
        def fit_classifier_dict(pos_symbol, X_train_tfidf, train_data_list):
            try:
                
                # Train on initial data
                self.classifier_dict[pos_symbol].fit(X_train_tfidf, train_data_list)
                if nu:
                    nu.store_objects(
                        slrcu_classifier_dict=self.classifier_dict, verbose=False
                    )
                
                # Build and store the prediction function
                inference_func = self.build_predict_percent_fit_function(
                    pos_symbol, verbose=verbose
                )
                self.pos_predict_percent_fit_dict[pos_symbol] = inference_func
            except ValueError as e:
                import sys
                print(f'Fitting {pos_symbol} had this error: {str(e).strip()}', file=sys.stderr)
                self.classifier_dict.pop(pos_symbol, None)
                self.pos_predict_percent_fit_dict.pop(pos_symbol, None)
        
        # Iterate over unique POS symbols in the training data
        pos_symbols = pos_df.pos_symbol.unique()
        if verbose:
            progress_bar = tqdm(
                pos_symbols, total=pos_symbols.shape[0],
                desc="Train the POS Classifiers"
            )
        else:
            progress_bar = pos_symbols
        for pos_symbol in progress_bar:
            
            # Train the classifier
            mask_series = (pos_df.pos_symbol == pos_symbol)
            train_data_list = mask_series.to_numpy()
            if pos_symbol not in self.classifier_dict:
                
                # Create a new logistic regression classifier
                self.classifier_dict[pos_symbol] = LogisticRegression(
                    C=375.0, class_weight='balanced', max_iter=1000, penalty='l1',
                    solver='liblinear', verbose=False, warm_start=True
                )
                
                fit_classifier_dict(pos_symbol, X_train_tfidf, train_data_list)
            elif not is_already_fitted:
                fit_classifier_dict(pos_symbol, X_train_tfidf, train_data_list)
            else:
                try:
                    
                    # Build and store the prediction function if not already fitted
                    inference_func = self.build_predict_percent_fit_function(
                        pos_symbol, verbose=verbose
                    )
                    self.pos_predict_percent_fit_dict[pos_symbol] = inference_func
                    
                except ValueError as e:
                    import sys
                    print(f'Fitting {pos_symbol} had this error: {str(e).strip()}', file=sys.stderr)
                    self.pos_predict_percent_fit_dict.pop(pos_symbol, None)
    
    
    def predict_single(self, html_str, verbose=False):
        '''
        Predict the labels for the input data
        '''
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
                try:
                    y_predict_proba = self.classifier_dict[pos_symbol].predict_proba(X_test)[0][1]
                except ValueError as e:
                    message = str(e).strip()
                    print(f"{e.__class__.__name__} error in predict_percent_fit: {message}")
                    if "LogisticRegression" in message:
                        print("Try deleting the slrcu_classifier_dict pickle")
                        raise ValueError(f"Try deleting the slrcu_classifier_dict pickle: {navigable_parent}") from e

                return y_predict_proba

        return predict_percent_fit


###########################################################
## Stochastic Gradient Descent parts-of-speech functions ##
###########################################################
class SectionSGDClassifierUtilities(object):
    '''
    A class for all the job-posting-section stochastic gradient descent predictive models
    '''
    def __init__(self, verbose=False):
        pass
    
    
    def build_pos_stochastic_gradient_descent_elements(
        self, sampling_strategy_limit=None, verbose=False
    ):
        '''Train a model for each labeled POS symbol'''
        self.count_vect = HtmlVectorizer()
        self.tfidf_transformer = TfidfTransformer(
            norm='l1', smooth_idf=True, sublinear_tf=False, use_idf=True
        )
        self.classifier_dict = {}
        self.pos_predict_percent_fit_dict = {}
        
        # Get the labeled training data
        pos_df = cu.get_pos_relationships(verbose=False)

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
                    loss='log_loss', warm_start=True
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
    def __init__(self, verbose=False):
        pass
    
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
        if nu and nu.pickle_exists('scrfcu_pos_symbol_crf'):
            self.pos_symbol_crf = nu.load_object('scrfcu_pos_symbol_crf')
            is_already_fitted = True
        else:
            import sklearn_crfsuite
            self.pos_symbol_crf = sklearn_crfsuite.CRF()
            is_already_fitted = False
        
        # Get the labeled training data
        pos_df = cu.get_pos_relationships(verbose=False)
        
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
            tokens_list = [hau.html_regex_tokenizer(sentence) for sentence in sents_list]
            
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
            if nu:
                nu.store_objects(scrfcu_pos_symbol_crf=self.pos_symbol_crf)
        
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
        tokens_list = [hau.html_regex_tokenizer(html_str)]
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
            tokens_list = [hau.html_regex_tokenizer(html_str)]
            if tokens_list != [[]]:
                pos_tags_list = [pos_tag(tokens) for tokens in tokens_list]
                X = [self.sent2features(pos_tags) for pos_tags in pos_tags_list]
                symbols_dicts_list = self.pos_symbol_crf.predict_marginals(X)[0]
                y_pred = np.mean([symbol_dict[pos_symbol] for symbol_dict in symbols_dicts_list])
            
            return y_pred
        
        return predict_percent_fit