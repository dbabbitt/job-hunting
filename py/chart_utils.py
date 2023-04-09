
#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



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

    def __init__(self, s=None, ha=None, cu=None, hc=None, crf=None, verbose=False):
        if s is None:
            from storage import Storage
            self.s = Storage()
        else:
            self.s = s
        if ha is None:
            from ha_utils import HeaderAnalysis
            self.ha = HeaderAnalysis(verbose=verbose)
        else:
            self.ha = ha
        if cu is None:
            
            from scrape_utils import WebScrapingUtilities
            wsu = WebScrapingUtilities()
            uri = wsu.secrets_json['neo4j']['connect_url']
            user =  wsu.secrets_json['neo4j']['username']
            password = wsu.secrets_json['neo4j']['password']
            
            from cypher_utils import CypherUtilities
            self.cu = CypherUtilities(uri=uri, user=user, password=password, driver=None, s=self.s, ha=self.ha)
            
        else:
            self.cu = cu
        if hc is None:
            from hc_utils import HeaderCategories
            self.hc = HeaderCategories(cu=self.cu, verbose=verbose)
        else:
            self.hc = hc
        if crf is None:
            from crf_utils import CrfUtilities
            self.crf = CrfUtilities(ha=self.ha, hc=self.hc, cu=self.cu, verbose=verbose)
        else:
            self.crf = crf
        self.verbose = verbose
        
        if self.s.pickle_exists('POS_DICT'):
            self.POS_DICT = self.s.load_object('POS_DICT')
        else:
            cypher_str = """
                MATCH (pos:PartsOfSpeech)-[r:SUMMARIZES]->(np:NavigableParents)
                RETURN
                    np.navigable_parent AS navigable_parent,
                    pos.pos_symbol AS pos_symbol;"""
            pos_df = pd.DataFrame(self.cu.get_execution_results(cypher_str, verbose=verbose))
            self.POS_DICT = pos_df.set_index('navigable_parent').pos_symbol.to_dict()
            self.s.store_objects(POS_DICT=self.POS_DICT, verbose=verbose)
    
    
    def visualize_cfr_child_str_predictions(self, file_name=None, use_explanation=False, verbose=False):
        # self.crf.slrcu.build_pos_logistic_regression_elements()
        if file_name is None:
            files_list = self.cu.get_files_list(verbose=verbose)
            file_name = random.choice(files_list)
        child_strs_list = self.cu.get_child_strs_from_file(file_name, verbose=verbose)
        child_tags_list = self.cu.get_child_tags_list(child_strs_list, verbose=verbose)
        feature_dict_list = self.cu.get_feature_dict_list(child_tags_list, child_strs_list, verbose=verbose)
        feature_tuple_list = [self.hc.get_feature_tuple(f, pos_lr_predict_single=self.crf.slrcu.predict_single, pos_crf_predict_single=None, pos_sgd_predict_single=None) for f in feature_dict_list]
        crf_list = self.crf.CRF.predict_single(self.crf.sent2features(feature_tuple_list))
        rgba_dict = self.get_pos_color_dictionary(verbose=verbose)
        html_str = ''
        for child_str, pos_symbol_pred in zip(child_strs_list, crf_list):
            if str(pos_symbol_pred) != 'nan':
                rgba = rgba_dict[pos_symbol_pred]
                hex_str = to_hex(rgba, keep_alpha=True)
                child_str = self.append_pos_symbol(child_str, pos_symbol_pred, use_explanation=use_explanation)
                html_str += f'<span style="color:{hex_str};">{child_str}</span><br />'
        display(HTML(html_str))
        
        return crf_list
    
    
    def visualize_basic_quals_section(self, ea=None, crf_list=None, child_strs_list=None, feature_tuple_list=None,
                                      feature_dict_list=None, child_tags_list=None, file_name=None, verbose=False):
        if ea is None:
            from html_analysis import ElementAnalysis
            ea = ElementAnalysis(ha=self.ha, hc=self.hc, verbose=verbose)
        if child_strs_list is None:
            if file_name is None:
                files_list = self.cu.get_files_list(verbose=verbose)
                file_name = random.choice(files_list)
            child_strs_list = self.cu.get_child_strs_from_file(file_name=file_name)
        if crf_list is None:
            if feature_tuple_list is None:
                if feature_dict_list is None:
                    if child_tags_list is None:
                        child_tags_list = self.cu.get_child_tags_list(child_strs_list, verbose=verbose)
                    feature_dict_list = self.cu.get_feature_dict_list(child_tags_list, child_strs_list, verbose=verbose)
                feature_tuple_list = []
                for feature_dict in feature_dict_list:
                    feature_tuple_list.append(self.hc.get_feature_tuple(feature_dict, pos_lr_predict_single=self.crf.slrcu.predict_single, pos_crf_predict_single=None, pos_sgd_predict_single=None))
            crf_list = self.crf.CRF.predict_single(self.crf.sent2features(feature_tuple_list))
        rq_initial_idx, rq_final_idx = ea.get_rq_section(crf_list)
        html_str = ''
        
        # Make an RGB dictionary of all the parts-of-speech symbols
        rgba_dict = self.get_pos_color_dictionary()
        
        for child_str, pos_symbol in zip(child_strs_list[rq_initial_idx:rq_final_idx], crf_list[rq_initial_idx:rq_final_idx]):
            rgba = rgba_dict[pos_symbol]
            hex_str = to_hex(rgba, keep_alpha=True)
            child_str = self.append_pos_symbol(child_str, pos_symbol, use_explanation=True)
            html_str += f'<span style="color:{hex_str};">{child_str}</span><br />'
        display(HTML(html_str))
        
        return rq_initial_idx, rq_final_idx