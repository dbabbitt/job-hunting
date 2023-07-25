#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria


from pos_symbol_sgd_classifiers import PosSymbolSgdClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier

##############################################
## SGDClassifier is-qualification functions ##
##############################################
class IsQualificationSgdClassifier(PosSymbolSgdClassifier):
    def __init__(self, ha, cu, verbose=False):
        super().__init__(ha, cu, verbose=False)
        self.tf_dict = {'true': 1, 'false': 0, True: 1, False: 0}

    def prepare_training_data(self, verbose=False):
        cypher_str = """
            MATCH (np:NavigableParents)
            WHERE
                ((np.is_preferred_qualification = true) OR
                (np.is_minimum_qualification = true) OR
                (np.is_educational_requirement = true)) AND
                ((np.is_qualification IS NULL) OR
                (np.is_qualification = false))
            SET np.is_qualification = true
            RETURN COUNT(np);"""
        with self.cu.driver.session() as session:
            session.write_transaction(self.cu.do_cypher_tx, cypher_str)
        cypher_str = """
            MATCH (np:NavigableParents)
            WHERE (np.is_qualification IS NOT NULL)
            RETURN
                np.is_qualification AS is_qualification,
                np.navigable_parent AS navigable_parent;"""
        from pandas import DataFrame
        df = DataFrame(
            self.cu.get_execution_results(cypher_str, verbose=False)
        )
        df.is_qualification = df.is_qualification.map(lambda x: self.tf_dict.get(x, x))
        if verbose:
            print(f'I have {df.shape[0]:,} hand-labeled qualification htmls prepared')
        train_data_list = df.navigable_parent.tolist()
        train_labels_list = df.is_qualification.values
        
        return train_data_list, train_labels_list