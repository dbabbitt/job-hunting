
#!/usr/bin/env python
# coding: utf-8

# From Anaconda Prompt (anaconda3), type:
# conda activate jh
# cd C:\Users\dev\Documents\Repositories\job-hunting\py
# python grid_search_text_feature_extraction.py
# conda deactivate



# Author: Olivier Grisel <olivier.grisel@ensta.org>
#         Peter Prettenhofer <peter.prettenhofer@gmail.com>
#         Mathieu Blondel <mathieu@mblondel.org>
# License: BSD 3 clause

from pprint import pprint
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.utils import Bunch
from time import time
import logging
import os
import pandas as pd
import pickle
import re
import sys



# Display progress logs on stdout
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')



saves_folder = r'../saves/'
saves_pickle_folder = os.path.join(saves_folder, 'pickle')
os.makedirs(name=saves_pickle_folder, exist_ok=True)
saves_csv_folder = os.path.join(saves_folder, 'csv')
os.makedirs(name=saves_csv_folder, exist_ok=True)
encoding_type = ['latin1', 'iso8859-1', 'utf-8'][2]



def load_object(obj_name, download_url=None):
	pickle_path = os.path.join(saves_pickle_folder, '{}.pickle'.format(obj_name))
	if not os.path.isfile(pickle_path):
		print('No pickle exists at {} - attempting to load as csv.'.format(os.path.abspath(pickle_path)))
		csv_path = os.path.join(saves_csv_folder, '{}.csv'.format(obj_name))
		if not os.path.isfile(csv_path):
			print('No csv exists at {} - attempting to download from URL.'.format(os.path.abspath(csv_path)))
			object = pd.read_csv(download_url, low_memory=False,
								 encoding=encoding_type)
		else:
			object = pd.read_csv(csv_path, low_memory=False,
								 encoding=encoding_type)
		if isinstance(object, pd.DataFrame):
			attempt_to_pickle(object, pickle_path, raise_exception=False)
		else:
			with open(pickle_path, 'wb') as handle:
			
				# Protocal 4 is not handled in python 2
				if sys.version_info.major == 2:
					pickle.dump(object, handle, 2)
				elif sys.version_info.major == 3:
					pickle.dump(object, handle, pickle.HIGHEST_PROTOCOL)
	else:
		try:
			object = pd.read_pickle(pickle_path)
		except:
			with open(pickle_path, 'rb') as handle:
				object = pickle.load(handle)
	
	return(object)



def attempt_to_pickle(df, pickle_path, raise_exception=False, verbose=True):
	try:
		if verbose:
			print('Pickling to {}'.format(os.path.abspath(pickle_path)))
	
		# Protocal 4 is not handled in python 2
		if sys.version_info.major == 2:
			df.to_pickle(pickle_path, protocol=2)
		elif sys.version_info.major == 3:
			df.to_pickle(pickle_path, protocol=pickle.HIGHEST_PROTOCOL)
	
	except Exception as e:
		os.remove(pickle_path)
		if verbose:
			print(e, ": Couldn't save {:,} cells as a pickle.".format(df.shape[0]*df.shape[1]))
		if raise_exception:
			raise



SCANNER_REGEX = re.compile(r'</?\w+|\w+[#\+]*|:|\.')
def regex_tokenizer(corpus):
    
    return [match.group() for match in re.finditer(SCANNER_REGEX, corpus)]



basic_tags_dict = load_object('basic_tags_dict')
rows_list = [{'navigable_parent': navigable_parent, 'is_header': is_header} for navigable_parent, is_header in basic_tags_dict.items()]
child_str_df = pd.DataFrame(rows_list)
data = Bunch(data=child_str_df.navigable_parent.tolist(), target=child_str_df.is_header.to_numpy())



# #############################################################################
# Define a pipeline combining a text feature extractor with a simple
# classifier
fit_estimators_dict = load_object('fit_estimators_dict')
pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', LogisticRegression()),
    #('clf', fit_estimators_dict['LogisticRegression']),
])



'''
                       # Used in Indeed Header Classifier Scores
                       LogisticRegression(C=7.5, class_weight='balanced', dual=True, fit_intercept=False, max_iter=64,
                                          solver='liblinear', tol=1e-09)
                       LogisticRegression(**{'C': 7.5, 'class_weight': 'balanced', 'dual': True, 'fit_intercept': False, 'max_iter': 64,
                                             'penalty': 'l2', 'solver': 'liblinear', 'tol': 1e-09}),
                       # Default
                       LogisticRegression(**{'C': 1.0, 'class_weight': None, 'dual': False, 'fit_intercept': True, 'intercept_scaling': 1,
                                             'l1_ratio': None, 'max_iter': 100, 'multi_class': 'auto', 'n_jobs': None, 'penalty': 'l2',
                                             'random_state': None, 'solver': 'lbfgs', 'tol': 0.0001, 'verbose': 0, 'warm_start': False}),
'''
'''
scoring='f1'
Best score: 0.881
Best parameters set:
        clf__C: 375.0
        clf__class_weight: 'balanced'
        clf__dual: False
        clf__fit_intercept: True
        clf__max_iter: 4
        clf__penalty: 'l1'
        clf__solver: 'liblinear'
        clf__tol: 7e-07
        tfidf__norm: 'l1'
        tfidf__smooth_idf: True
        tfidf__sublinear_tf: False
        tfidf__use_idf: True
        vect__analyzer: 'word'
        vect__binary: False
        vect__decode_error: 'strict'
        vect__lowercase: False
        vect__max_df: 1.0
        vect__max_features: None
        vect__min_df: 0.0
        vect__ngram_range: (1, 2)
        vect__stop_words: None
        vect__strip_accents: 'ascii'
        vect__tokenizer: <function regex_tokenizer at 0x0000015A9516E430>
'''
'''
    'clf__C': (0.85, 8.5, 85.0, 850.0),
    'clf__class_weight': (None, 'balanced'),
    'clf__dual': (False, True),
    'clf__fit_intercept': (True, False),
    'clf__max_iter': (6, 35, 64),
    'clf__penalty': ('l1', 'l2', 'elasticnet', 'none',),
    'clf__solver': ('sag', 'liblinear'),
    'clf__tol': (1e-07, 1e-08, 1e-09),
    'tfidf__norm': ('l1', 'l2'),
    'tfidf__smooth_idf': (True, False),
    'tfidf__sublinear_tf': (False, True),
    'tfidf__use_idf': (True, False),
    'vect__analyzer': ('word', 'char', 'char_wb'),
    'vect__binary': (False, True),
    'vect__decode_error': ('strict', 'ignore', 'replace'),
    'vect__lowercase': (False, True),
    'vect__max_df': (0.0, 0.5, 1.0),
    'vect__max_features': (None, 1, 10, 100),
    'vect__min_df': (0.0, 0.5, 1.0),
    'vect__ngram_range': ((1, 1), (1, 2), (1, 3)),
    'vect__stop_words': ('english', None),
    'vect__strip_accents': ('ascii', 'unicode', None),
'''
parameters = {
    'clf__C': (375.0, 400.0, 425.0,),
    'clf__class_weight': ('balanced',),
    'clf__dual': (False,),
    'clf__fit_intercept': (True,),
    'clf__max_iter': (4, 5, 6,),
    'clf__penalty': ('l1',),
    'clf__solver': ('liblinear',),
    'clf__tol': (1e-06, 3e-06, 7e-07,),
    'tfidf__norm': ('l1',),
    'tfidf__smooth_idf': (True,),
    'tfidf__sublinear_tf': (False,),
    'tfidf__use_idf': (True,),
    'vect__analyzer': ('word',),
    'vect__binary': (False,),
    'vect__decode_error': ('strict',),
    'vect__lowercase': (False,),
    'vect__max_df': (1.0,),
    'vect__max_features': (None,),
    'vect__min_df': (0.0,),
    'vect__ngram_range': ((1, 2),),
    'vect__stop_words': (None,),
    'vect__strip_accents': ('ascii',),
    'vect__tokenizer': (regex_tokenizer,),
}



# Find the best parameters for both the feature extraction and the
# classifier
grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1, scoring='f1')



print("Performing grid search...")
print("pipeline:", [name for name, _ in pipeline.steps])
print("parameters:")
pprint(parameters)
t0 = time()
grid_search.fit(data.data, data.target)
print("done in %0.3fs" % (time() - t0))
print()



print("Best score: %0.3f" % grid_search.best_score_)
print("Best parameters set:")
best_parameters = grid_search.best_estimator_.get_params()
for param_name in sorted(parameters.keys()):
    print("\t%s: %r" % (param_name, best_parameters[param_name]))