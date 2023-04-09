#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria


from pos_symbol_sgd_classifiers import PosSymbolSgdClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier

##########################################
## SGDClassifier is-job-title functions ##
##########################################
class IsJobTitleSgdClassifier(PosSymbolSgdClassifier):
    def __init__(self, ha, cu, verbose=False):
        super().__init__(ha, cu, verbose=False)

    def prepare_training_data(self, verbose=False):
        cypher_str = """
            MATCH (np:NavigableParents)
            WHERE (np.is_job_title IS NOT NULL)
            RETURN
                np.is_job_title AS is_job_title,
                np.navigable_parent AS navigable_parent;"""
        from pandas import DataFrame
        df = DataFrame(
            self.cu.get_execution_results(cypher_str, verbose=False)
        )
        df.is_job_title = df.is_job_title.map(
            lambda x: {'True': 1, 'False': 0, True: 1, False: 0}.get(x, x)
        )
        if verbose:
            print(
                f'I have {df.shape[0]:,} hand-labeled',
                'job title htmls prepared'
            )
        train_data_list = df.navigable_parent.tolist()
        train_labels_list = df.is_job_title.values
        
        return train_data_list, train_labels_list