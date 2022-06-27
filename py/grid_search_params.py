
#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



# From Anaconda Prompt (anaconda3), type:
# cd C:\Users\dev\Documents\GitHub\job-hunting\py
# conda activate jh
# clear
# python grid_search_params.py
# conda deactivate

from sklearn.experimental import enable_hist_gradient_boosting
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from sklearn.calibration import CalibratedClassifierCV
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import StackingClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.feature_selection import RFE
from sklearn.feature_selection import RFECV
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LogisticRegressionCV
from sklearn.linear_model import SGDClassifier
from sklearn.mixture import BayesianGaussianMixture
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.multiclass import OneVsRestClassifier
from sklearn.multioutput import ClassifierChain
from sklearn.multioutput import MultiOutputClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import CategoricalNB
from sklearn.naive_bayes import ComplementNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import RadiusNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.semi_supervised import LabelPropagation
from sklearn.semi_supervised import LabelSpreading
from sklearn.svm import NuSVC
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import ExtraTreeClassifier

from sklearn.utils import Bunch
import logging
import numpy as np
import os
import pandas as pd
import pickle
import re
import sys
import time



# Display progress logs on stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')



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
			print(e, ': Couldn\'t save {:,} cells as a pickle.'.format(df.shape[0]*df.shape[1]))
		if raise_exception:
			raise



SCANNER_REGEX = re.compile(r'</?\w+|\w+[#\+]*|:|\.')
def regex_tokenizer(corpus):
	
	return [match.group() for match in re.finditer(SCANNER_REGEX, corpus)]



def get_value_str(best_parameters_dict, params_dict, param_name):
	value = best_parameters_dict[param_name]
	example_param_obj = params_dict[param_name][0]
	if type(example_param_obj) == str:
		value_str = f"'{str(value)}'"
	elif hasattr(example_param_obj, '__call__'):
		value_str = example_param_obj.__name__
	else:
		value_str = str(value)
	
	return value_str



navigable_parent_is_header_dict = load_object('navigable_parent_is_header_dict')
rows_list = [{'navigable_parent': navigable_parent,
			  'is_header': is_header} for navigable_parent, is_header in navigable_parent_is_header_dict.items()]
child_str_df = pd.DataFrame(rows_list)
data = Bunch(data=child_str_df.navigable_parent.tolist(), target=child_str_df.is_header.to_numpy())



clf_params_dict = {}
clf_params_dict['AdaBoostClassifier'] = {
		'clf__algorithm': ('SAMME.R',),
		'clf__base_estimator': (None,),
		'clf__learning_rate': (1.0,),
		'clf__n_estimators': (5,),
		'clf__random_state': (None,),
	}
clf_params_dict['BaggingClassifier'] = {
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
		'clf__warm_start': (False,),
	}
clf_params_dict['BayesianGaussianMixture'] = {
		'clf__covariance_prior': (None,),
		'clf__covariance_type': ('full',),
		'clf__degrees_of_freedom_prior': (None,),
		'clf__init_params': ('kmeans',),
		'clf__max_iter': (100,),
		'clf__mean_precision_prior': (None,),
		'clf__mean_prior': (None,),
		'clf__n_components': (1,),
		'clf__n_init': (1,),
		'clf__random_state': (None,),
		'clf__reg_covar': (1e-06,),
		'clf__tol': (0.001,),
		'clf__verbose': (0,),
		'clf__verbose_interval': (10,),
		'clf__warm_start': (False,),
		'clf__weight_concentration_prior': (None,),
		'clf__weight_concentration_prior_type': ('dirichlet_process',),
	}
clf_params_dict['BernoulliNB'] = {
		'clf__alpha': (1.0,),
		'clf__binarize': (0.0,),
		'clf__class_prior': (None,),
		'clf__fit_prior': (True,),
	}
clf_params_dict['CalibratedClassifierCV'] = {
		'clf__base_estimator': (None,),
		'clf__cv': (None,),
		'clf__method': ('sigmoid',),
	}
clf_params_dict['CategoricalNB'] = {
		'clf__alpha': (1.0,),
		'clf__class_prior': (None,),
		'clf__fit_prior': (True,),
	}
clf_params_dict['ClassifierChain'] = {
		'clf__cv': (None,),
		'clf__order': (None,),
		'clf__random_state': (None,),
	}
clf_params_dict['ComplementNB'] = {
		'clf__alpha': (1.0,),
		'clf__class_prior': (None,),
		'clf__fit_prior': (True,),
		'clf__norm': (False,),
	}
clf_params_dict['DecisionTreeClassifier'] = {
		'clf__ccp_alpha': (0.0,),
		'clf__class_weight': (None,),
		'clf__criterion': ('gini',),
		'clf__max_depth': (None,),
		'clf__max_features': (None,),
		'clf__max_leaf_nodes': (None,),
		'clf__min_impurity_decrease': (0.0,),
		'clf__min_impurity_split': (None,),
		'clf__min_samples_leaf': (1,),
		'clf__min_samples_split': (2,),
		'clf__min_weight_fraction_leaf': (0.0,),
		'clf__presort': ('deprecated',),
		'clf__random_state': (None,),
		'clf__splitter': ('best',),
	}
clf_params_dict['DummyClassifier'] = {
		'clf__constant': (None,),
		'clf__random_state': (None,),
		'clf__strategy': ('warn',),
	}
clf_params_dict['ExtraTreeClassifier'] = {
		'clf__ccp_alpha': (0.0,),
		'clf__class_weight': (None,),
		'clf__criterion': ('gini',),
		'clf__max_depth': (None,),
		'clf__max_features': ('auto',),
		'clf__max_leaf_nodes': (None,),
		'clf__min_impurity_decrease': (0.0,),
		'clf__min_impurity_split': (None,),
		'clf__min_samples_leaf': (1,),
		'clf__min_samples_split': (2,),
		'clf__min_weight_fraction_leaf': (0.0,),
		'clf__random_state': (None,),
		'clf__splitter': ('random',),
	}
clf_params_dict['ExtraTreesClassifier'] = {
		'clf__bootstrap': (False,),
		'clf__ccp_alpha': (0.0,),
		'clf__class_weight': (None,),
		'clf__criterion': ('gini',),
		'clf__max_depth': (100,),
		'clf__max_features': ('sqrt',),
		'clf__max_leaf_nodes': (None,),
		'clf__max_samples': (None,),
		'clf__min_impurity_decrease': (0.0,),
		'clf__min_impurity_split': (None,),
		'clf__min_samples_leaf': (1,),
		'clf__min_samples_split': (2,),
		'clf__min_weight_fraction_leaf': (0.0,),
		'clf__n_estimators': (100,),
		'clf__n_jobs': (-1,),
		'clf__oob_score': (False,),
		'clf__random_state': (None,),
		'clf__verbose': (0,),
		'clf__warm_start': (False,),
	}
clf_params_dict['GaussianMixture'] = {
		'clf__covariance_type': ('full',),
		'clf__init_params': ('kmeans',),
		'clf__max_iter': (100,),
		'clf__means_init': (None,),
		'clf__n_components': (1,),
		'clf__n_init': (1,),
		'clf__precisions_init': (None,),
		'clf__random_state': (None,),
		'clf__reg_covar': (1e-06,),
		'clf__tol': (0.001,),
		'clf__verbose': (0,),
		'clf__verbose_interval': (10,),
		'clf__warm_start': (False,),
		'clf__weights_init': (None,),
	}
clf_params_dict['GaussianNB'] = {
		'clf__priors': (None,),
		'clf__var_smoothing': (1e-09,),
	}
clf_params_dict['GaussianProcessClassifier'] = {
		'clf__copy_X_train': (True,),
		'clf__kernel': (None,),
		'clf__max_iter_predict': (100,),
		'clf__multi_class': ('one_vs_rest',),
		'clf__n_jobs': (None,),
		'clf__n_restarts_optimizer': (0,),
		'clf__optimizer': ('fmin_l_bfgs_b',),
		'clf__random_state': (None,),
		'clf__warm_start': (False,),
	}
clf_params_dict['GradientBoostingClassifier'] = {
		'clf__ccp_alpha': (0.0,),
		'clf__criterion': ('friedman_mse',),
		'clf__init': ('zero',),
		'clf__learning_rate': (1.0,),
		'clf__loss': ('deviance',),
		'clf__max_depth': (3,),
		'clf__max_features': (None,),
		'clf__max_leaf_nodes': (None,),
		'clf__min_impurity_decrease': (0.0,),
		'clf__min_impurity_split': (None,),
		'clf__min_samples_leaf': (1,),
		'clf__min_samples_split': (2,),
		'clf__min_weight_fraction_leaf': (0.0,),
		'clf__n_estimators': (1000,),
		'clf__n_iter_no_change': (None,),
		'clf__presort': ('deprecated',),
		'clf__random_state': (None,),
		'clf__subsample': (1.0,),
		'clf__tol': (0.0001,),
		'clf__validation_fraction': (0.1,),
		'clf__verbose': (0,),
		'clf__warm_start': (False,),
	}
clf_params_dict['GridSearchCV'] = {
		'clf__cv': (None,),
		'clf__error_score': (np.nan,),
		'clf__iid': ('deprecated',),
		'clf__n_jobs': (None,),
		'clf__pre_dispatch': ('2*n_jobs',),
		'clf__refit': (True,),
		'clf__return_train_score': (False,),
		'clf__scoring': (None,),
		'clf__verbose': (0,),
	}
clf_params_dict['HistGradientBoostingClassifier'] = {
		'clf__early_stopping': ('auto',),
		'clf__l2_regularization': (0.0,),
		'clf__learning_rate': (0.1,),
		'clf__loss': ('auto',),
		'clf__max_bins': (255,),
		'clf__max_depth': (None,),
		'clf__max_iter': (100,),
		'clf__max_leaf_nodes': (31,),
		'clf__min_samples_leaf': (20,),
		'clf__monotonic_cst': (None,),
		'clf__n_iter_no_change': (10,),
		'clf__random_state': (None,),
		'clf__scoring': ('loss',),
		'clf__tol': (1e-07,),
		'clf__validation_fraction': (0.1,),
		'clf__verbose': (0,),
		'clf__warm_start': (False,),
	}
clf_params_dict['KNeighborsClassifier'] = {
		'clf__algorithm': ('auto',),
		'clf__leaf_size': (30,),
		'clf__metric': ('minkowski',),
		'clf__metric_params': (None,),
		'clf__n_jobs': (None,),
		'clf__n_neighbors': (5,),
		'clf__p': (2,),
		'clf__weights': ('uniform',),
	}
clf_params_dict['LabelPropagation'] = {
		'clf__gamma': (20,),
		'clf__kernel': ('rbf',),
		'clf__max_iter': (1000,),
		'clf__n_jobs': (None,),
		'clf__n_neighbors': (7,),
		'clf__tol': (0.001,),
	}
clf_params_dict['LabelSpreading'] = {
		'clf__alpha': (0.2,),
		'clf__gamma': (20,),
		'clf__kernel': ('rbf',),
		'clf__max_iter': (30,),
		'clf__n_jobs': (None,),
		'clf__n_neighbors': (7,),
		'clf__tol': (0.001,),
	}
clf_params_dict['LinearDiscriminantAnalysis'] = {
		'clf__n_components': (None,),
		'clf__priors': (None,),
		'clf__shrinkage': (None,),
		'clf__solver': ('svd',),
		'clf__store_covariance': (False,),
		'clf__tol': (0.0001,),
	}
clf_params_dict['LogisticRegression'] = {
		'clf__C': (10.0,),
		'clf__class_weight': ('balanced',),
		'clf__dual': (False,),
		'clf__fit_intercept': (True,),
		'clf__intercept_scaling': (1,),
		'clf__l1_ratio': (None,),
		'clf__max_iter': (100,),
		'clf__multi_class': ('auto',),
		'clf__n_jobs': (None,),
		'clf__penalty': ('l1',),
		'clf__random_state': (None,),
		'clf__solver': ('liblinear',),
		'clf__tol': (0.0001,),
		'clf__verbose': (0,),
		'clf__warm_start': (False,),
	}
clf_params_dict['LogisticRegressionCV'] = {
		'clf__Cs': (10,),
		'clf__class_weight': (None,),
		'clf__cv': (None,),
		'clf__dual': (False,),
		'clf__fit_intercept': (True,),
		'clf__intercept_scaling': (1.0,),
		'clf__l1_ratios': (None,),
		'clf__max_iter': (100,),
		'clf__multi_class': ('auto',),
		'clf__n_jobs': (None,),
		'clf__penalty': ('l2',),
		'clf__random_state': (None,),
		'clf__refit': (True,),
		'clf__scoring': (None,),
		'clf__solver': ('lbfgs',),
		'clf__tol': (0.0001,),
		'clf__verbose': (0,),
	}
clf_params_dict['MLPClassifier'] = {
		'clf__activation': ('relu',),
		'clf__alpha': (0.0001,),
		'clf__batch_size': ('auto',),
		'clf__beta_1': (0.9,),
		'clf__beta_2': (0.999,),
		'clf__early_stopping': (False,),
		'clf__epsilon': (1e-08,),
		'clf__hidden_layer_sizes': ((100,),),
		'clf__learning_rate': ('constant',),
		'clf__learning_rate_init': (0.001,),
		'clf__max_fun': (15000,),
		'clf__max_iter': (200,),
		'clf__momentum': (0.9,),
		'clf__n_iter_no_change': (10,),
		'clf__nesterovs_momentum': (True,),
		'clf__power_t': (0.5,),
		'clf__random_state': (None,),
		'clf__shuffle': (True,),
		'clf__solver': ('adam',),
		'clf__tol': (0.0001,),
		'clf__validation_fraction': (0.1,),
		'clf__verbose': (False,),
		'clf__warm_start': (False,),
	}
clf_params_dict['MultiOutputClassifier'] = {
		'clf__n_jobs': (None,),
	}
clf_params_dict['MultinomialNB'] = {
		'clf__alpha': (1.0,),
		'clf__class_prior': (None,),
		'clf__fit_prior': (True,),
	}
clf_params_dict['NuSVC'] = {
		'clf__break_ties': (False,),
		'clf__cache_size': (200,),
		'clf__class_weight': (None,),
		'clf__coef0': (0.0,),
		'clf__decision_function_shape': ('ovr',),
		'clf__degree': (3,),
		'clf__gamma': ('scale',),
		'clf__kernel': ('rbf',),
		'clf__max_iter': (-1,),
		'clf__nu': (0.5,),
		'clf__probability': (False,),
		'clf__random_state': (None,),
		'clf__shrinking': (True,),
		'clf__tol': (0.001,),
		'clf__verbose': (False,),
	}
clf_params_dict['OneVsRestClassifier'] = {
		'clf__n_jobs': (None,),
	}
clf_params_dict['Pipeline'] = {
		'clf__memory': (None,),
		'clf__verbose': (False,),
	}
clf_params_dict['QuadraticDiscriminantAnalysis'] = {
		'clf__priors': (None,),
		'clf__reg_param': (0.0,),
		'clf__store_covariance': (False,),
		'clf__tol': (0.0001,),
	}
clf_params_dict['RFE'] = {
		'clf__n_features_to_select': (None,),
		'clf__step': (1,),
		'clf__verbose': (0,),
	}
clf_params_dict['RFECV'] = {
		'clf__cv': (None,),
		'clf__min_features_to_select': (1,),
		'clf__n_jobs': (None,),
		'clf__scoring': (None,),
		'clf__step': (1,),
		'clf__verbose': (0,),
	}
clf_params_dict['RadiusNeighborsClassifier'] = {
		'clf__algorithm': ('auto',),
		'clf__leaf_size': (30,),
		'clf__metric': ('minkowski',),
		'clf__metric_params': (None,),
		'clf__n_jobs': (None,),
		'clf__outlier_label': (None,),
		'clf__p': (2,),
		'clf__radius': (1.0,),
		'clf__weights': ('uniform',),
	}
clf_params_dict['RandomForestClassifier'] = {
		'clf__bootstrap': (True,),
		'clf__ccp_alpha': (0.0,),
		'clf__class_weight': (None,),
		'clf__criterion': ('entropy',),
		'clf__max_depth': (None,),
		'clf__max_features': (None,),
		'clf__max_leaf_nodes': (None,),
		'clf__max_samples': (None,),
		'clf__min_impurity_decrease': (0.0,),
		'clf__min_impurity_split': (None,),
		'clf__min_samples_leaf': (2,),
		'clf__min_samples_split': (2,),
		'clf__min_weight_fraction_leaf': (0.0,),
		'clf__n_estimators': (1000,),
		'clf__n_jobs': (None,),
		'clf__oob_score': (False,),
		'clf__random_state': (None,),
		'clf__verbose': (0,),
		'clf__warm_start': (False,),
	}
clf_params_dict['RandomizedSearchCV'] = {
		'clf__cv': (None,),
		'clf__error_score': (np.nan,),
		'clf__iid': ('deprecated',),
		'clf__n_iter': (10,),
		'clf__n_jobs': (None,),
		'clf__pre_dispatch': ('2*n_jobs',),
		'clf__random_state': (None,),
		'clf__refit': (True,),
		'clf__return_train_score': (False,),
		'clf__scoring': (None,),
		'clf__verbose': (0,),
	}
clf_params_dict['SGDClassifier'] = {
		'clf__alpha': (0.0001,),
		'clf__average': (False,),
		'clf__class_weight': (None,),
		'clf__early_stopping': (False,),
		'clf__epsilon': (0.1,),
		'clf__eta0': (0.0,),
		'clf__fit_intercept': (True,),
		'clf__l1_ratio': (0.15,),
		'clf__learning_rate': ('optimal',),
		'clf__loss': ('hinge',),
		'clf__max_iter': (1000,),
		'clf__n_iter_no_change': (5,),
		'clf__n_jobs': (None,),
		'clf__penalty': ('l2',),
		'clf__power_t': (0.5,),
		'clf__random_state': (None,),
		'clf__shuffle': (True,),
		'clf__tol': (0.001,),
		'clf__validation_fraction': (0.1,),
		'clf__verbose': (0,),
		'clf__warm_start': (False,),
	}
clf_params_dict['SVC'] = {
		'clf__C': (10.0,),
		'clf__break_ties': (False,),
		'clf__cache_size': (200,),
		'clf__class_weight': (None,),
		'clf__coef0': (0.0,),
		'clf__decision_function_shape': ('ovr',),
		'clf__degree': (3,),
		'clf__gamma': ('scale',),
		'clf__kernel': ('linear',),
		'clf__max_iter': (-1,),
		'clf__probability': (False,),
		'clf__random_state': (None,),
		'clf__shrinking': (True,),
		'clf__tol': (0.001,),
		'clf__verbose': (False,),
	}
clf_params_dict['StackingClassifier'] = {
		'clf__cv': (None,),
		'clf__final_estimator': (None,),
		'clf__n_jobs': (None,),
		'clf__passthrough': (False,),
		'clf__stack_method': ('auto',),
		'clf__verbose': (0,),
	}
clf_params_dict['VotingClassifier'] = {
		'clf__flatten_transform': (True,),
		'clf__n_jobs': (None,),
		'clf__verbose': (False,),
		'clf__voting': ('hard',),
		'clf__weights': (None,),
	}

score_file_path = os.path.join(saves_folder, 'txt', 'new_estimators_scores.txt')
os.makedirs(name=os.path.dirname(score_file_path), exist_ok=True)
with open(score_file_path, 'w') as f:
	print('', file=f)

# ##################################################################
# Define a pipeline combining a text feature extractor with a simple
# classifier
# ##################################################################
estimators_list = [
				   # done in xxxx
				   # Best score: xxxx
				   AdaBoostClassifier(),

				   # done in xxxx
				   # Best score: xxxx
				   BaggingClassifier(),

				   # done in xxxx
				   # Best score: xxxx
				   #BayesianGaussianMixture(),

				   # done in xxxx
				   # Best score: xxxx
				   BernoulliNB(),

				   # done in xxxx
				   # Best score: xxxx
				   CalibratedClassifierCV(),

				   # done in xxxx
				   # Best score: xxxx
				   #CategoricalNB(),

				   # done in xxxx
				   # Best score: xxxx
				   #ClassifierChain(base_estimator=LogisticRegression()),

				   # done in xxxx
				   # Best score: xxxx
				   ComplementNB(),

				   # done in xxxx
				   # Best score: xxxx
				   DecisionTreeClassifier(),

				   # done in xxxx
				   # Best score: xxxx
				   DummyClassifier(),

				   # done in xxxx
				   # Best score: xxxx
				   ExtraTreeClassifier(),

				   # done in xxxx
				   # Best score: xxxx
				   ExtraTreesClassifier(),

				   # done in xxxx
				   # Best score: xxxx
				   #GaussianMixture(),

				   # done in xxxx
				   # Best score: xxxx
				   #GaussianNB(),

				   # done in xxxx
				   # Best score: xxxx
				   #GaussianProcessClassifier(),

				   # done in xxxx
				   # Best score: xxxx
				   GradientBoostingClassifier(),

				   # done in xxxx
				   # Best score: xxxx
				   GridSearchCV(estimator=SVC(), param_grid={'C': (10.0,), 'kernel': ('linear',)}),

				   # done in xxxx
				   # Best score: xxxx
				   #HistGradientBoostingClassifier(),

				   # done in xxxx
				   # Best score: xxxx
				   KNeighborsClassifier(),

				   # done in xxxx
				   # Best score: xxxx
				   #LabelPropagation(),

				   # done in xxxx
				   # Best score: xxxx
				   #LabelSpreading(),

				   # done in xxxx
				   # Best score: xxxx
				   #LinearDiscriminantAnalysis(),

				   # done in xxxx
				   # Best score: xxxx
				   LogisticRegression(),

				   # done in xxxx
				   # Best score: xxxx
				   LogisticRegressionCV(),

				   # done in xxxx
				   # Best score: xxxx
				   MLPClassifier(),

				   # done in xxxx
				   # Best score: xxxx
				   #MultiOutputClassifier(estimator=SVC()),

				   # done in xxxx
				   # Best score: xxxx
				   MultinomialNB(),

				   # done in xxxx
				   # Best score: xxxx
				   #NuSVC(),

				   # done in xxxx
				   # Best score: xxxx
				   OneVsRestClassifier(estimator=SVC()),

				   # done in xxxx
				   # Best score: xxxx
				   Pipeline(steps=[('svc', SVC())]),

				   # done in xxxx
				   # Best score: xxxx
				   #QuadraticDiscriminantAnalysis(),

				   # done in xxxx
				   # Best score: xxxx
				   #RFE(estimator=SVC()),

				   # done in xxxx
				   # Best score: xxxx
				   #RFECV(estimator=SVC()),

				   # done in xxxx
				   # Best score: xxxx
				   RadiusNeighborsClassifier(),

				   # done in xxxx
				   # Best score: xxxx
				   RandomForestClassifier(),

				   # done in xxxx
				   # Best score: xxxx
				   RandomizedSearchCV(estimator=SVC(), param_distributions={'C': (10.0,)}),

				   # done in xxxx
				   # Best score: xxxx
				   SGDClassifier(),

				   # done in xxxx
				   # Best score: xxxx
				   SVC(),

				   # done in xxxx
				   # Best score: xxxx
				   StackingClassifier(estimators=[('svc', SVC(),),]),

				   # done in xxxx
				   # Best score: xxxx
				   VotingClassifier(estimators=[('svc', SVC(),),])
				   ]

for estimator in estimators_list:
	steps_list = [
		('vect', CountVectorizer()),
		('tfidf', TfidfTransformer()),
		('clf', estimator),
	]
	pipeline = Pipeline(steps_list)
	clf_name = str(estimator.__class__).split('.')[-1].split("'")[0]
	params_dict = clf_params_dict[clf_name]
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
		print('Performing grid search...', file=f)
		print('pipeline:', [name for name, _ in pipeline.steps], file=f)
		print('parameters:', file=f)
		print('{', file=f)
		for key, value in params_dict.items():
			print(f"""        '{key}': {str(value)},""", file=f)
		print('}', file=f)
	
	# Add scores
	t0 = time.time()
	print()
	print(time.ctime(t0))
	print(clf_name)
	grid_search.fit(data.data, data.target)
	with open(score_file_path, 'a') as f:
		print('done in %0.3fs' % (time.time() - t0), file=f)
		print('', file=f)
		print(f'Best {clf_name} score: {round(grid_search.best_score_, 2)}', file=f)
		print('Best parameters set:', file=f)
	best_parameters_dict = grid_search.best_estimator_.get_params()
	for param_name in sorted(params_dict.keys()):
		with open(score_file_path, 'a') as f:
			#print(('    %s: %r' % (param_name, best_parameters_dict[param_name])), file=f)
			value_str = get_value_str(best_parameters_dict, params_dict, param_name)
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
				value_str = get_value_str(best_parameters_dict, params_dict, param_name)
				signature_list.append(f'{param_name[len(step_prefix)+2:]}={value_str}')
		function_str += ', '.join(signature_list)
		function_str += '),'
		with open(score_file_path, 'a') as f:
			print(function_str, file=f)
