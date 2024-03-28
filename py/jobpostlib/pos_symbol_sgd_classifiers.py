#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria

from . import hau, cu
from section_classifier_utils import HtmlVectorizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.exceptions import NotFittedError

##########################################
## SGDClassifier parent class functions ##
##########################################
class PosSymbolSgdClassifier:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.count_vect = HtmlVectorizer(hau, verbose=verbose)
        self.tfidf_transformer = TfidfTransformer(
            norm='l1', smooth_idf=True, sublinear_tf=False, use_idf=True
        )
        self.classifier = SGDClassifier(loss='log', warm_start=True)
        self.total_trained = 0
        self.tf_dict = {'true': 1, 'false': 0, True: 1, False: 0}
    
    def prepare_updating_data(self, new_data_list, new_labels_list, verbose=False):
        new_labels_list = [self.tf_dict.get(x, x) for x in new_labels_list]
        
        return new_data_list, new_labels_list

    def update_model(self, new_data_list, new_labels_list, verbose=False):
        
        # Get the new vocabulary to be used in the count
        # vectorizer in the predict_percent_fit function
        self.count_vect.validate_and_restore_vocab()
        X_new_counts = self.count_vect.transform(new_data_list)
        
        X_new_tfidf = self.tfidf_transformer.transform(X_new_counts)
        self.classifier.partial_fit(X_new_tfidf, new_labels_list, classes=[0, 1])
        self.total_trained += len(new_data_list)
        if verbose:
            print(
                f'{self.classifier.n_iter_:,} iterations seen during updating fit',
                f'for a total of {self.total_trained:,} records trained'
            )

    def retrain_classifier(
        self, new_data_list, new_labels_list, verbose=False
    ):
        # Ensure the variables are lists
        if not isinstance(new_data_list, list):
            new_data_list = [new_data_list]
        if not isinstance(new_labels_list, list):
            new_labels_list = [new_labels_list]

        # Re-train the classifier
        new_data_list, new_labels_list = self.prepare_updating_data(
            new_data_list, new_labels_list, verbose=verbose
        )
        self.update_model(new_data_list, new_labels_list, verbose=verbose)
    
    
    def train_model(self, train_data_list, train_labels_list, verbose=False):
        X_train_counts = self.count_vect.fit_transform(train_data_list)
        X_train_tfidf = self.tfidf_transformer.fit_transform(X_train_counts)
        
        # Train on initial data
        self.classifier.fit(X_train_tfidf, train_labels_list)
        self.total_trained += len(train_data_list)
        if verbose:
            print(
                f'{self.classifier.n_iter_:,} iterations seen during training fit',
                f'for a total of {self.total_trained:,} records trained'
            )
    
    def build_pos_stochastic_gradient_descent_elements(self, verbose=False):
        train_data, train_labels = self.prepare_training_data(verbose=verbose)
        self.train_model(train_data, train_labels, verbose=verbose)
    
    def make_prediction(self, navigable_parent, verbose=False):
        
        # Get the new vocabulary to be used in the count
        # vectorizer in the predict_percent_fit function
        self.count_vect.validate_and_restore_vocab()
        X_counts = self.count_vect.transform([navigable_parent])
        
        X_tfidf = self.tfidf_transformer.transform(X_counts)
        
        return self.classifier.predict(X_tfidf)[0]
    
    def predict_percent_fit(self, navigable_parent, verbose=False):
        
        # Get the new vocabulary to be used in the count
        # vectorizer in the predict_percent_fit function
        self.count_vect.validate_and_restore_vocab()
        X_counts = self.count_vect.transform([navigable_parent])
        
        # Validate the vocabulary using the _check_vocabulary method
        self.count_vect._check_vocabulary()
        
        X_tfidf = self.tfidf_transformer.transform(X_counts)
        X_test = X_tfidf.toarray()
        y_predict_proba = self.classifier.predict_proba(X_test).flatten().tolist()

        return y_predict_proba[-1]