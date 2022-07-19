
#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



from matplotlib.colors import to_hex
import re
from nltk.tokenize import sent_tokenize
import os

class SectionUtilities(object):
    """Section class."""

    def __init__(self, s=None, ha=None, wsu=None, cu=None, hc=None, verbose=False):
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
        if wsu is None:
            from scrape_utils import WebScrapingUtilities
            self.wsu = WebScrapingUtilities()
        else:
            self.wsu = wsu
        if cu is None:
            from cypher_utils import CypherUtilities
            uri = self.wsu.secrets_json['neo4j']['connect_url']
            user =  self.wsu.secrets_json['neo4j']['username']
            password = self.wsu.secrets_json['neo4j']['password']
            self.cu = CypherUtilities(uri=uri, user=user, password=password, driver=None, s=self.s, ha=self.ha)
            
        else:
            self.cu = cu
        if hc is None:
            from hc_utils import HeaderCategories
            self.hc = HeaderCategories(cu=self.cu, verbose=verbose)
        else:
            self.hc = hc
    
    
    def get_section(self, crf_list, pos_symbol='RQ', neg_symbol='PQ', nonheader_allows_list=['O-RQ', 'O-ER'], verbose=False):
        
        # Remove the Preferred Qualifications section
        neg_list = []
        if f'H-{neg_symbol}' in crf_list:
            neg_idx = len(crf_list) - crf_list[::-1].index(f'H-{neg_symbol}') - 1
            while (crf_list[neg_idx] == f'H-{neg_symbol}'):
                neg_idx += 1
            while (neg_idx < len(crf_list)) and (crf_list[neg_idx].split('-')[0] == 'O'):
                neg_list.append(neg_idx)
                neg_idx += 1
            
        indices_list = [i for i, x in enumerate(crf_list) if (x in nonheader_allows_list) and (i not in neg_list)]
        
        return indices_list
    
    
    def get_pos_color_dictionary(self, verbose=False):
        cypher_str = """
            MATCH (pos:PartsOfSpeech {is_header: 'True'})
            RETURN pos.pos_symbol as pos_symbol
            ORDER BY pos.pos_symbol;"""
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
        # indices_list = self.get_section(pos_list)
        indices_list = [i for i, x in enumerate(pos_list) if (x in ['O-RQ', 'O-ER'])]

        return indices_list
    
    
    def visualize_basic_quals_section(self, crf_list, child_strs_list, db_pos_list=None, verbose=True):

        # Make an RGB dictionary of all the parts-of-speech symbols
        rgba_dict = self.get_pos_color_dictionary()

        html_str = ''
        pos_list = []
        if db_pos_list is None:
            db_pos_list = []
            for navigable_parent in child_strs_list:
                db_pos_list = self.cu.append_parts_of_speech_list(navigable_parent, pos_list=db_pos_list)
        for i, (crf_symbol, db_symbol) in enumerate(zip(crf_list, db_pos_list)):
            if db_symbol in [None, 'O', 'H']:
                pos_list.append(crf_symbol)
            else:
                pos_list.append(db_symbol)
        if verbose:
            print(pos_list)
        indices_list = self.get_section(pos_list)
        if verbose:
            print(indices_list)
        for i, (child_str, pos_symbol) in enumerate(zip(child_strs_list, pos_list)):
            rgba = rgba_dict[pos_symbol]
            hex_str = to_hex(rgba, keep_alpha=True)
            if len(indices_list) and (i == min(indices_list)):
                html_str += '<hr />'
            child_str = self.append_pos_symbol(child_str, pos_symbol, use_explanation=True)
            html_str += f'{i+0} {pos_symbol}) <span style="color:{hex_str};">{child_str}</span><br />'
            if len(indices_list) and (i == max(indices_list)):
                html_str += '<hr />'
        from IPython.display import HTML, display
        display(HTML(html_str))
        if verbose:
            print(indices_list)
        
        return pos_list, indices_list
    
    def print_fit_job(self, row_index, row_series, lru=None, verbose=True):
        job_fitness = 0.0
        file_name = row_series.file_name
        child_strs_list = self.ha.get_child_strs_from_file(file_name=file_name)
        indices_list = self.find_basic_quals_section_indexes(child_strs_list=child_strs_list, file_name=file_name)
        assert indices_list, f"Something is wrong:\nfile_name = '{file_name}'\ncu.delete_filename_node(file_name, verbose=True)"
        prequals_list = [child_str for i, child_str in enumerate(child_strs_list) if i in indices_list]
        sentence_regex = re.compile(r'[\.;•]')
        quals_set = set()
        fake_stops_list = ['e.g.', 'etc.', 'M.S.', 'B.S.', 'Ph.D.', '(ex.', '(Ex.', 'U.S.']
        replacements_list = ['eg', 'etc', 'MS', 'BS', 'PhD', '(eg', '(eg', 'US']
        for qual in prequals_list:
            for fake_stop, replacement in zip(fake_stops_list, replacements_list):
                qual = qual.replace(fake_stop, replacement)
            concatonated_quals_list = sentence_regex.split(qual)
            if len(concatonated_quals_list) > 2:
                for q1 in sent_tokenize(qual):
                    for q2 in q1.split('•'):
                        quals_set.add(q2)
            else:
                quals_set.add(qual)
        quals_list = list(quals_set)
        assert all([isinstance(qual_str, str) for qual_str in quals_list]), f'Error in print_fit_job:\nquals_list = {quals_list}\nrow_series:\n{row_series}'
        if lru is None:
            from lr_utils import LrUtilities
            lru = LrUtilities(ha=self.ha, hc=self.hc, cu=self.cu, verbose=verbose)
        prediction_list = list(lru.predict_job_hunt_percent_fit(quals_list))
        quals_str, qual_count = lru.get_quals_str(prediction_list, quals_list)
        if len(prediction_list):
            job_fitness = qual_count/len(prediction_list)
            if job_fitness > 0.8:
                job_title = re.sub(r'(_-_Indeed.com)?(_[a-z0-9]{16})?\.html$', '', file_name).replace('_', ' ')
                if verbose:
                    print()
                    print(f'Basic Qualifications for {job_title}:{quals_str}')
                    print(job_fitness)
                    lru.print_loc_computation(row_index, quals_list, verbose=verbose)
        
        return quals_list, job_fitness
    
    def load_indeed_posting_url(self, viewjob_url, jk_str=None, files_list=[], verbose=True):
        file_node_dict = {}
        if jk_str is None:
            from urllib.parse import urlparse, parse_qs
            jk_str = parse_qs(urlparse(viewjob_url).query).get('jk', [''])[0]
        from urllib.error import HTTPError, URLError
        try:
            page_soup = self.wsu.get_page_soup(viewjob_url)
            page_title = page_soup.find('title').string.strip()
            file_name = re.sub(r'[^A-Za-z0-9]+', ' ', page_title).strip().replace(' ', '_')
            if len(jk_str):
                file_name = f'{jk_str}_{file_name}.html'
            else:
                # file_name = datetime.now().strftime('%Y%m%d%H%M%S%f') + f'_{file_name}.html'
                file_name = f'{file_name}.html'
            file_path = os.path.join(self.cu.SAVES_HTML_FOLDER, file_name)
            file_node_dict['file_name'] = file_name
            if not os.path.isfile(file_path):
                with open(file_path, 'w', encoding=self.s.encoding_type) as f:
                    if verbose:
                        print(f'Saving to {file_path}')
                    f.write('<html><head><title>')
                    f.write(page_title)
                    f.write('</title></head><body>')
                    row_div_list = page_soup.find_all(name='div', attrs={'class': ['jobsearch-JobComponent-description']})
                    for div_soup in row_div_list:
                        f.write(str(div_soup))
                    f.write('</body></html>')
                files_list.append(file_name)
                self.cu.ensure_filename(file_name, verbose=False)

            def do_cypher_tx(tx, file_name, viewjob_url, verbose=False):
                cypher_str = """
                    MATCH (fn:FileNames {file_name: $file_name})
                    SET fn.posting_url = $viewjob_url
                    RETURN fn;"""
                if verbose:
                    from IPython.display import clear_output
                    clear_output(wait=True)
                    print(cypher_str.replace('$file_name', f'"{file_name}"').replace('$viewjob_url', f'"{viewjob_url}"'))
                parameter_dict = {'file_name': file_name, 'viewjob_url': viewjob_url}
                rows_list = []
                for record in tx.run(query=cypher_str, parameters=parameter_dict):
                    row_dict = {k: v for k, v in dict(record.items())['fn'].items()}
                    rows_list.append(row_dict)
                from pandas import DataFrame
                df = DataFrame(rows_list).T
                
                return df

            with self.cu.driver.session() as session:
                df = session.write_transaction(do_cypher_tx, file_name=file_name, viewjob_url=viewjob_url, verbose=False)
                if df.shape[1]:
                    file_node_dict = df[0].to_dict()
        except HTTPError as e:
            print(f'Got an HTTPError with {viewjob_url}: {str(e).strip()}')
        except URLError as e:
            print(f'Got an URLError with {viewjob_url}: {str(e).strip()}')
        except Exception as e:
            print(f'Got an {e.__class__} error with {viewjob_url}: {str(e).strip()}')

        return file_node_dict, files_list