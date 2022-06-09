
#!/usr/bin/env python
# coding: utf-8

from matplotlib.colors import to_hex

class SectionUtilities(object):
    """Section class."""

    def __init__(self, s=None, ha=None, cu=None, hc=None, verbose=False):
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
    
    
    def get_section(self, crf_list, pos_symbol='RQ', neg_symbol='PQ', nonheader_allows_list=['O-RQ', 'O-ER'], verbose=False):
        
        # Remove the Preffered Qualifications section off the end
        idx_max = len(crf_list) - 1
        if f'H-{neg_symbol}' in crf_list:
            idx_max = len(crf_list) - crf_list[::-1].index(f'H-{neg_symbol}') - 1
        
        # Remove the duplicates from the beginning
        idx_min = 0
        if f'H-{pos_symbol}' in crf_list:
            idx_min = crf_list.index(f'H-{pos_symbol}')
            
        indices_list = [i for i, x in enumerate(crf_list) if (x in nonheader_allows_list) and (i >= idx_min) and (i <= idx_max)]
        
        return indices_list
    
    
    def get_pos_color_dictionary(self, verbose=False):
        cypher_str = """
            MATCH (pos:PartsOfSpeech {is_header: 'True'})
            RETURN pos.pos_symbol as pos_symbol;"""
        from pandas import DataFrame
        pos_df = DataFrame(self.cu.get_execution_results(cypher_str, verbose=verbose))
        from cycler import cycler
        from matplotlib.pyplot import cm
        from numpy import linspace
        color_cycler = cycler('color', cm.tab20(linspace(0, 1, pos_df.shape[0])))
        header_pos_list = pos_df.pos_symbol.tolist()
        rgba_dict = {}
        for header_pos_symbol, face_color_dict in zip(header_pos_list, color_cycler()):
            face_color = face_color_dict['color']
            rgba_dict[header_pos_symbol] = face_color
        for header_pos_symbol, face_color in rgba_dict.copy().items():
            nonheader_pos_symbol = 'O-' + header_pos_symbol.split('-')[1]
            fc_array = face_color.copy()
            fc_array[-1] = 0.5
            rgba_dict[nonheader_pos_symbol] = fc_array
        rgba_dict['H'] = [0.0, 0.0, 0.0, 1.0]
        rgba_dict['O'] = [0.0, 0.0, 0.0, 0.5]
        
        return rgba_dict
    
    
    def append_pos_symbol(self, child_str, pos_symbol, use_explanation=False):
        if use_explanation:
            pos_symbol = pos_symbol + ' ' + self.hc.POS_EXPLANATION_DICT[pos_symbol]
        suffix = f' ({pos_symbol})'
        idx = child_str.rfind('<')
        if idx == -1:
            child_str += suffix
        else:
            child_str = child_str[:idx] + suffix + child_str[idx:]

        return child_str


    def find_basic_quals_section_indexes(self, crf_list=None, feature_tuple_list=None, feature_dict_list=None, child_strs_list=None,
                                         child_tags_list=None, file_name=None, verbose=False):
        if crf_list is None:
            from hc_utils import HeaderCategories
            hc = HeaderCategories(cu=self.cu, verbose=False)
            if feature_tuple_list is None:
                from lr_utils import LrUtilities
                lru = LrUtilities(ha=self.ha, hc=hc, cu=self.cu, verbose=False)
                lru.build_isheader_logistic_regression_elements()
                lru.build_pos_logistic_regression_elements()
                if feature_dict_list is None:
                    if child_strs_list is None:
                        if file_name is None:
                            import os
                            files_list = files_list = sorted([fn for fn in os.listdir(self.cu.SAVES_HTML_FOLDER) if fn.endswith('.html')])
                            file_name = random.choice(files_list)
                        child_strs_list = self.ha.get_child_strs_from_file(file_name=file_name)
                    if child_tags_list is None:
                        child_tags_list = self.ha.get_child_tags_list(child_strs_list)
                    is_header_list = []
                    for is_header, child_str in zip(self.ha.get_is_header_list(child_strs_list), child_strs_list):
                        if is_header is None:
                            probs_list = lru.ISHEADER_PREDICT_PERCENT_FIT(child_str)
                            idx = probs_list.index(max(probs_list))
                            is_header = [True, False][idx]
                        is_header_list.append(is_header)
                    feature_dict_list = hc.get_feature_dict_list(child_tags_list, is_header_list, child_strs_list)
                feature_tuple_list = []
                for feature_dict in feature_dict_list:
                    feature_tuple_list.append(hc.get_feature_tuple(feature_dict, lru.pos_lr_predict_single))
            from crf_utils import CrfUtilities
            crf = CrfUtilities(ha=self.ha, hc=hc, cu=self.cu, verbose=False)
            crf_list = crf.CRF.predict_single(crf.sent2features(feature_tuple_list))
        db_pos_list = []
        for navigable_parent in child_strs_list:
            db_pos_list = self.cu.append_parts_of_speech_list(navigable_parent, pos_list=db_pos_list)
        pos_list = []
        for crf_symbol, db_symbol in zip(crf_list, db_pos_list):
            if db_symbol in [None, 'O', 'H']:
                pos_list.append(crf_symbol)
            else:
                pos_list.append(db_symbol)
        indices_list = self.get_section(pos_list)

        return indices_list
    
    
    def visualize_basic_quals_section(self, crf_list=None, feature_tuple_list=None, feature_dict_list=None, child_strs_list=None,
                                      child_tags_list=None, file_name=None, verbose=False):
        indices_list = self.find_basic_quals_section_indexes(crf_list=crf_list, feature_tuple_list=feature_tuple_list,
                                                             feature_dict_list=feature_dict_list,
                                                             child_strs_list=child_strs_list,
                                                             child_tags_list=child_tags_list, file_name=file_name)
        
        # Make an RGB dictionary of all the parts-of-speech symbols
        rgba_dict = self.get_pos_color_dictionary()
        
        html_str = ''
        indices_list.sort()
        child_strs_list = [child_strs_list[i] for i in indices_list]
        crf_list = [crf_list[i] for i in indices_list]
        for child_str, pos_symbol in zip(child_strs_list, crf_list):
            rgba = rgba_dict[pos_symbol]
            hex_str = to_hex(rgba, keep_alpha=True)
            child_str = self.append_pos_symbol(child_str, pos_symbol, use_explanation=True)
            html_str += f'<span style="color:{hex_str};">{child_str}</span><br />'
        from IPython.display import HTML, display
        display(HTML(html_str))
        
        return indices_list