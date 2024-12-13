
#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria

from . import nu, hau, cu, hc, slrcu, crf
from IPython.display import HTML, display
from cycler import cycler
from matplotlib.colors import to_hex
import html_analysis
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random

class ChartUtilities(object):
    """Chart class."""

    def __init__(self, verbose=False):
        self.verbose = verbose
        
        if nu.pickle_exists('POS_DICT'):
            self.POS_DICT = nu.load_object('POS_DICT')
        else:
            cypher_str = """
                MATCH (pos:PartsOfSpeech)-[r:SUMMARIZES]->(np:NavigableParents)
                RETURN
                    np.navigable_parent AS navigable_parent,
                    pos.pos_symbol AS pos_symbol;"""
            pos_df = pd.DataFrame(cu.get_execution_results(cypher_str, verbose=verbose))
            self.POS_DICT = pos_df.set_index('navigable_parent').pos_symbol.to_dict()
            nu.store_objects(POS_DICT=self.POS_DICT, verbose=verbose)
    
    
    def visualize_cfr_child_str_predictions(self, file_name=None, use_explanation=False, verbose=False):
        # slrcu.build_pos_logistic_regression_elements()
        if file_name is None:
            files_list = cu.get_files_list(verbose=verbose)
            file_name = random.choice(files_list)
        child_strs_list = cu.get_navigable_parents_from_next_relationships(file_name, verbose=verbose)
        child_tags_list = cu.query_child_tags_list(child_strs_list, verbose=verbose)
        feature_dict_list = cu.query_feature_dict_list(child_tags_list, child_strs_list, verbose=verbose)
        feature_tuple_list = [hc.get_feature_tuple(f, pos_lr_predict_single=slrcu.predict_single, pos_crf_predict_single=None, pos_sgd_predict_single=None) for f in feature_dict_list]
        pos_symbol_predictions_list = crf.CRF.predict_single(crf.sentence_to_crf_features(feature_tuple_list))
        rgba_dict = self.get_pos_color_dictionary(verbose=verbose)
        html_str = ''
        for child_str, pos_symbol_pred in zip(child_strs_list, pos_symbol_predictions_list):
            if str(pos_symbol_pred) != 'nan':
                rgba = rgba_dict[pos_symbol_pred]
                hex_str = to_hex(rgba, keep_alpha=True)
                child_str = self.append_pos_symbol(child_str, pos_symbol_pred, use_explanation=use_explanation)
                html_str += f'<span style="color:{hex_str};">{child_str}</span><br />'
        display(HTML(html_str))
        
        return pos_symbol_predictions_list