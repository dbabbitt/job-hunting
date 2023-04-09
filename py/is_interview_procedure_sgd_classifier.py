#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria


from pos_symbol_sgd_classifiers import PosSymbolSgdClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier

####################################################
## SGDClassifier is-interview-procedure functions ##
####################################################
class IsInterviewProcedureSgdClassifier(PosSymbolSgdClassifier):
    def __init__(self, ha, cu, verbose=False):
        super().__init__(ha, cu, verbose=False)

    def prepare_training_data(self, verbose=False):
        cypher_str = """
            MATCH (np:NavigableParents)
            WHERE (np.is_interview_procedure IS NOT NULL)
            RETURN
                np.is_interview_procedure AS is_interview_procedure,
                np.navigable_parent AS navigable_parent;"""
        from pandas import DataFrame
        df = DataFrame(
            self.cu.get_execution_results(cypher_str, verbose=False)
        )
        df.is_interview_procedure = df.is_interview_procedure.map(
            lambda x: {'True': 1, 'False': 0, True: 1, False: 0}.get(x, x)
        )
        if verbose:
            print(
                f'I have {df.shape[0]:,} hand-labeled',
                'interview procedure htmls prepared'
            )
        train_data_list = df.navigable_parent.tolist()
        train_labels_list = df.is_interview_procedure.values
        
        return train_data_list, train_labels_list