#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria


from . import cu
from .pos_symbol_sgd_classifiers import PosSymbolSgdClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier

#######################################
## SGDClassifier is-header functions ##
#######################################
class IsHeaderSgdClassifier(PosSymbolSgdClassifier):
    def __init__(self, verbose=False):
        super().__init__(verbose=False)

    def prepare_training_data(self, verbose=False):
        cypher_str = """
            MATCH (np:NavigableParents)
            WHERE np.is_header IS NOT NULL
            RETURN
                np.is_header AS is_header,
                np.navigable_parent AS navigable_parent;"""
        from pandas import DataFrame
        df = DataFrame(
            cu.get_execution_results(cypher_str, verbose=False)
        )
        df.is_header = df.is_header.map(
            lambda x: {'True': 1, 'False': 0, True: 1, False: 0}.get(x, x)
        )
        if verbose:
            print(f'I have {df.shape[0]:,} hand-labeled header htmls prepared')
        train_data_list = df.navigable_parent.tolist()
        train_labels_list = df.is_header.values
        
        return train_data_list, train_labels_list