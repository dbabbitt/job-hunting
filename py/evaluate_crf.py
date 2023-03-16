
#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



# From Anaconda Prompt (anaconda3), type:
# conda activate C:\Users\dev\Documents\GitHub\job-hunting\jh
# cd C:\Users\dev\Documents\GitHub\job-hunting\py
# cls
# python evaluate_crf.py

from collections import Counter
from sklearn.metrics import make_scorer
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
from sklearn_crfsuite import metrics
import html_analysis
import scipy.stats
import sklearn_crfsuite
import sql_utlis
import storage



s = storage.Storage()
su = sql_utlis.SqlUtilities()
hc = html_analysis.HeaderCategories()
assert s.pickle_exists('HEADER_PATTERN_DICT')
HEADER_PATTERN_DICT = s.load_object('HEADER_PATTERN_DICT')



X = []
y = []
for file_name, feature_dict_list in HEADER_PATTERN_DICT.items():
    X.append(feature_dict_list)
    pos_list = [hc.get_feature_tuple(feature_dict, pos_lr_predict_single=None, pos_crf_predict_single=None)[2] for feature_dict in feature_dict_list]
    y.append(pos_list)
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.75, random_state=101)


print('## Hyperparameter Optimization')
# 
print('To improve quality try to select regularization parameters using randomized search and 3-fold cross-validation.')
# 
print('It takes quite a lot of CPU time and RAM (we\'re fitting a model ``50 * 3 = 150`` times), so grab a tea and be patient,')
print('or reduce n_iter in Randomized Search CV, or fit model only on a subset of training data.')



print('Define fixed parameters and parameters to search')
crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs', 
    max_iterations=100, 
    all_possible_transitions=True
)
params_space = {
    'c1': scipy.stats.expon(scale=0.5),
    'c2': scipy.stats.expon(scale=0.05),
}

print('Use the same metric for evaluation')
crf.fit(X_train, y_train)
labels = list(crf.classes_)
f1_scorer = make_scorer(metrics.flat_f1_score, 
                        average='weighted', labels=labels)

print('Search')
rs = RandomizedSearchCV(crf, params_space, 
                        cv=3, 
                        verbose=1, 
                        n_jobs=-1, 
                        n_iter=50, 
                        scoring=f1_scorer)
rs.fit(X_train, y_train)


print('crf = rs.best_estimator_')
print('best params:', rs.best_params_)
print('best CV score:', rs.best_score_)
print('model size: {:0.2f}M'.format(rs.best_estimator_.size_ / 1000000))


print('### Check parameter space')
try:
	s.store_objects(rs=rs, verbose=True)
except Exception as e:
	print(f'Unable to store rs: {str(e).strip()}')


print('## Check best estimator on our test data')
# 
print('As you can see, quality is improved.')


crf = rs.best_estimator_
y_pred = crf.predict(X_test)
print(metrics.flat_classification_report(
    y_test, y_pred, labels=sorted_labels, digits=3
))


print('## Let\'s check what classifier learned')


def print_transitions(trans_features):
    for (label_from, label_to), weight in trans_features:
        print('%-6s -> %-7s %0.6f' % (label_from, label_to, weight))

print('Top likely transitions:')
print_transitions(Counter(crf.transition_features_).most_common(20))

print('\nTop unlikely transitions:')
print_transitions(Counter(crf.transition_features_).most_common()[-20:])


print('We can see that, for example, it is very likely that the beginning of an organization name (B-ORG) will be followed by a token inside organization name (I-ORG), but transitions to I-ORG from tokens with other labels are penalized.')
# 
print('Check the state features:')


def print_state_features(state_features):
    for (attr, label), weight in state_features:
        print('%0.6f %-8s %s' % (weight, label, attr))    

print('Top positive:')
print_state_features(Counter(crf.state_features_).most_common(30))

print('\nTop negative:')
print_state_features(Counter(crf.state_features_).most_common()[-30:])