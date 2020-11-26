
#!/usr/bin/env python
# coding: utf-8

# From Anaconda Prompt (anaconda3), type:
# cd C:\Users\dev\Documents\Repositories\job-hunting\py
# conda activate jh
# clear
# python grid_search_text_feature_extraction.py
# conda deactivate



# Author: Olivier Grisel <olivier.grisel@ensta.org>
#         Peter Prettenhofer <peter.prettenhofer@gmail.com>
#         Mathieu Blondel <mathieu@mblondel.org>
# License: BSD 3 clause

from pprint import pprint
from sklearn.ensemble import AdaBoostClassifier, BaggingClassifier, ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.ensemble import StackingClassifier, VotingClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
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
clf_params_dict = {}
clf_params_dict['AdaBoostClassifier'] = """
        'clf__algorithm': ('SAMME.R',),
		'clf__base_estimator': (None,),
        'clf__learning_rate': (1.0,),
        'clf__n_estimators': (5,),
		'clf__random_state': (None,),"""
clf_params_dict['BaggingClassifier'] = """
        'clf__base_estimator': (None,),
        'clf__bootstrap': (True,),
        'clf__bootstrap_features': (False,),
        'clf__max_features': (0.5,),
        'clf__max_samples': (0.75,),
        'clf__n_estimators': (10,),
        'clf__n_jobs': (-1,),
        'clf__oob_score': (False,),
        'clf__random_state': (None,),
        'clf__verbose': (0,),
        'clf__warm_start': (False,),"""
clf_params_dict['ExtraTreesClassifier'] = """
        'clf__bootstrap': (False,),
        'clf__ccp_alpha': (0.0,),
        'clf__class_weight': (None,),
        'clf__criterion': ('gini',),
        'clf__max_depth': (100,),
        'clf__max_features': ('sqrt',),
        'clf__max_leaf_nodes': (None,),
        'clf__max_samples': (None,),
        'clf__min_impurity_decrease': (0.0,),
        'clf__min_samples_leaf': (1,),
        'clf__min_samples_split': (2,),
        'clf__min_weight_fraction_leaf': (0.0,),
        'clf__n_estimators': (100,),
        'clf__n_jobs': (-1,),
		'clf__oob_score': (False,),
		'clf__random_state': (None,),
		'clf__verbose': (0,),
		'clf__warm_start': (False,),"""
clf_params_dict['GradientBoostingClassifier'] = """
		'clf__ccp_alpha': (0.0,),
		'clf__criterion': ('friedman_mse', 'mse', 'mae',),
		'clf__init': (None, 'zero',),
		'clf__learning_rate': (0.01, 0.1, 0.5, 1.0,),
		'clf__loss': ('deviance', 'exponential',),
		'clf__max_depth': (3, 30,),
		'clf__max_features': (None, 'sqrt', 'log2'),
		'clf__max_leaf_nodes': (None,),
		'clf__min_impurity_decrease': (0.0,),
		'clf__min_samples_leaf': (1, 2, 0.05,),
		'clf__min_samples_split': (2, 4, 0.1,),
		'clf__min_weight_fraction_leaf': (0.0,),
		'clf__n_estimators': (10, 100, 1000,),
		'clf__n_iter_no_change': (None,),
		'clf__random_state': (None,),
		'clf__subsample': (1.0, 0.9),
		'clf__tol': (0.0001,),
		'clf__validation_fraction': (0.1,),
		'clf__verbose': (0,),
		'clf__warm_start': (False,),"""
clf_params_dict['RandomForestClassifier'] = """
		'clf__bootstrap': (True,),
		'clf__ccp_alpha': (0.0,),
		'clf__class_weight': (None,),
		'clf__criterion': ('gini',),
		'clf__max_depth': (None,),
		'clf__max_features': ('auto',),
		'clf__max_leaf_nodes': (None,),
		'clf__max_samples': (None,),
		'clf__min_impurity_decrease': (0.0,),
		'clf__min_impurity_split': (None,),
		'clf__min_samples_leaf': (1,),
		'clf__min_samples_split': (2,),
		'clf__min_weight_fraction_leaf': (0.0,),
		'clf__n_estimators': (100,),
		'clf__n_jobs': (None,),
		'clf__oob_score': (False,),
		'clf__random_state': (None,),
		'clf__verbose': (0,),
		'clf__warm_start': (False,),"""
clf_params_dict['LogisticRegression'] = """
		'clf__C': (1.0,),
		'clf__class_weight': (None,),
		'clf__dual': (False,),
		'clf__fit_intercept': (True,),
		'clf__intercept_scaling': (1,),
		'clf__l1_ratio': (None,),
		'clf__max_iter': (100,),
		'clf__multi_class': ('auto',),
		'clf__n_jobs': (None,),
		'clf__penalty': ('l2',),
		'clf__random_state': (None,),
		'clf__solver': ('lbfgs',),
		'clf__tol': (0.0001,),
		'clf__verbose': (0,),
		'clf__warm_start': (False,),"""
clf_params_dict['SVC'] = """
		'clf__C': (1.0,),
		'clf__break_ties': (False,),
		'clf__cache_size': (200,),
		'clf__class_weight': (None,),
		'clf__coef0': (0.0,),
		'clf__decision_function_shape': ('ovr',),
		'clf__degree': (3,),
		'clf__gamma': ('scale',),
		'clf__kernel': ('rbf',),
		'clf__max_iter': (-1,),
		'clf__probability': (False,),
		'clf__random_state': (None,),
		'clf__shrinking': (True,),
		'clf__tol': (0.001,),
		'clf__verbose': (False,),"""
score_file_path = os.path.join(saves_folder, 'txt', 'estimators_scores.txt')
os.makedirs(name=os.path.dirname(score_file_path), exist_ok=True)
with open(score_file_path, 'w') as f:
	print('', file=f)

# ##################################################################
# Define a pipeline combining a text feature extractor with a simple
# classifier
# ##################################################################
estimators_list = [AdaBoostClassifier(),
				   BaggingClassifier(),
				   ExtraTreesClassifier(),
				   GradientBoostingClassifier(),
				   RandomForestClassifier(),
				   LogisticRegression(),
				   SVC()]
for estimator in estimators_list:
	steps_list = [
		('vect', CountVectorizer()),
		('tfidf', TfidfTransformer()),
		('clf', estimator),
	]
	pipeline = Pipeline(steps_list)
	clf_name = str(estimator.__class__).split('.')[-1].split("'")[0]
	params_dict = eval(f'{{{clf_params_dict[clf_name]}}}')
	params_dict.update({
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
		'vect__ngram_range': ((1, 5),),
		'vect__stop_words': (None,),
		'vect__strip_accents': ('ascii',),
		'vect__tokenizer': (regex_tokenizer,),
	})



	# Find the best parameters for both the feature extraction and the
	# classifier
	grid_search = GridSearchCV(pipeline, params_dict, n_jobs=-1, verbose=1, scoring='f1')
	
	# Add inital pipeline parameters
	with open(score_file_path, 'a') as f:
		print('', file=f)
		print('_'*len(clf_name), file=f)
		print(clf_name, file=f)
		print('^'*len(clf_name), file=f)
		print("Performing grid search...", file=f)
		print("pipeline:", [name for name, _ in pipeline.steps], file=f)
		print("parameters:", file=f)
		print('{', file=f)
		for key, value in params_dict.items():
			print(f"""        '{key}': {str(value)},""", file=f)
		print('}', file=f)
	
	# Add scores
	t0 = time()
	grid_search.fit(data.data, data.target)
	with open(score_file_path, 'a') as f:
		print("done in %0.3fs" % (time() - t0), file=f)
		print('', file=f)
		print("Best score: %0.3f" % grid_search.best_score_, file=f)
		print("Best parameters set:", file=f)
	best_parameters_dict = grid_search.best_estimator_.get_params()
	for param_name in sorted(params_dict.keys()):
		with open(score_file_path, 'a') as f:
			#print("\t%s: %r" % (param_name, best_parameters_dict[param_name]), file=f)
			value = best_parameters_dict[param_name]
			if type(params_dict[param_name][0]) == str:
				value_str = f"'{str(value)}'"
			elif hasattr(params_dict[param_name][0], '__call__'):
				value_str = params_dict[param_name][0].__name__
			else:
				value_str = str(value)
			print(f"        '{param_name}': ({value_str},),", file=f)
	with open(score_file_path, 'a') as f:
		print('', file=f)
	
	# Add function signatures
	for step_tuple in steps_list:
		step_prefix = step_tuple[0]
		step_name = str(step_tuple[1].__class__).split('.')[-1].split("'")[0]
		function_str = f'{step_name}('
		signature_list = []
		for param_name in sorted(params_dict.keys()):
			if param_name.startswith(step_prefix) and (param_name in best_parameters_dict):
				value = best_parameters_dict[param_name]
				if type(params_dict[param_name][0]) == str:
					value_str = f"'{str(value)}'"
				elif hasattr(params_dict[param_name][0], '__call__'):
					value_str = params_dict[param_name][0].__name__
				else:
					value_str = str(value)
				signature_list.append(f'{param_name[len(step_prefix)+2:]}={value_str}')
		function_str += ', '.join(signature_list)
		function_str += '),'
		with open(score_file_path, 'a') as f:
			print(function_str, file=f)
	
	# # Add a vect function signature
	# function_str = 'CountVectorizer('
	# signature_list = []
	# for param_name in sorted(params_dict.keys()):
		# if param_name.startswith('vect__') and (param_name in best_parameters_dict):
			# signature_list.append(f'{param_name[6:]}={best_parameters_dict[param_name]}')
	# function_str += ', '.join(signature_list)
	# function_str += ')'
	# with open(score_file_path, 'a') as f:
		# print(function_str, file=f)
	
	# # Add a tfidf function signature
	# function_str = 'TfidfTransformer('
	# signature_list = []
	# for param_name in sorted(params_dict.keys()):
		# if param_name.startswith('tfidf__') and (param_name in best_parameters_dict):
			# signature_list.append(f'{param_name[6:]}={best_parameters_dict[param_name]}')
	# function_str += ', '.join(signature_list)
	# function_str += ')'
	# with open(score_file_path, 'a') as f:
		# print(function_str, file=f)
	
	# # Add a clf function signature
	# function_str = f'{clf_name}('
	# signature_list = []
	# for param_name in eval(f'{{{clf_params_dict[clf_name]}}}').keys():
		# if param_name in best_parameters_dict:
			# signature_list.append(f'{param_name[5:]}={best_parameters_dict[param_name]}')
	# function_str += ', '.join(signature_list)
	# function_str += ')'
	# with open(score_file_path, 'a') as f:
		# print(function_str, file=f)