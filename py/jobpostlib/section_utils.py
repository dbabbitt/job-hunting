
#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria

from . import nu, wsu, hau, cu, hc, lru, ssgdcu, scrfcu, crf
from IPython.display import clear_output
from matplotlib.colors import to_hex
from nltk.tokenize import sent_tokenize
import os
import re

class SectionUtilities(object):
    """Section class."""

    def __init__(
        self, verbose=False
    ):
        self.ascii_regex = re.compile('[^A-Za-z0-9]+')
    
    
    def get_section(self, crf_list, pos_symbol='RQ', neg_symbol='PQ', nonheader_allows_list=['O-RQ', 'O-ER'], verbose=False):
        
        # Remove the Preferred Qualifications section
        neg_list = []
        if f'H-{neg_symbol}' in crf_list:
            neg_idx = len(crf_list) - crf_list[::-1].index(f'H-{neg_symbol}') - 1
            while (len(crf_list) > neg_idx) and (crf_list[neg_idx] == f'H-{neg_symbol}'):
                neg_idx += 1
            while (neg_idx < len(crf_list)) and (crf_list[neg_idx].split('-')[0] == 'O'):
                neg_list.append(neg_idx)
                neg_idx += 1
            
        indices_list = [i for i, x in enumerate(crf_list) if (x in nonheader_allows_list) and (i not in neg_list)]
        
        return indices_list
    
    
    def get_pos_color_dictionary(self, verbose=False):
        cypher_str = """
            MATCH (pos:PartsOfSpeech {is_header: true})
            RETURN pos.pos_symbol as pos_symbol
            ORDER BY pos.pos_symbol;"""
        from pandas import DataFrame
        pos_df = DataFrame(cu.get_execution_results(cypher_str, verbose=verbose))
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
            pos_symbol = pos_symbol + ' ' + hc.POS_EXPLANATION_DICT[pos_symbol]
        suffix = f' ({pos_symbol})'
        idx = child_str.rfind('<')
        if idx == -1:
            child_str += suffix
        else:
            child_str = child_str[:idx] + suffix + child_str[idx:]

        return child_str


    def find_basic_quals_section_indexes(
        self, crf_list=None, feature_tuple_list=None, feature_dict_list=None,
        child_strs_list=None, child_tags_list=None, file_name=None, verbose=False
    ):
        if crf_list is None:
            if feature_tuple_list is None:
                if feature_dict_list is None:
                    if child_strs_list is None:
                        if file_name is None:
                            files_list = sorted([fn for fn in os.listdir(cu.SAVES_HTML_FOLDER) if fn.endswith('.html')])
                            file_name = random.choice(files_list)
                        child_strs_list = hau.get_child_strs_from_file(file_name=file_name)
                    if child_tags_list is None:
                        child_tags_list = hau.get_child_tags_list(child_strs_list)
                    feature_dict_list = cu.get_feature_dict_list(
                        child_tags_list, child_strs_list, verbose=verbose
                    )
                feature_tuple_list = []
                
                # Seek a SectionLRClassifierUtilities object
                from . import slrcu
                if hasattr(slrcu, 'pos_predict_percent_fit_dict'):
                    pos_lr_predict_single = slrcu.predict_single
                    if verbose: print('slrcu.predict_single is now available')
                else: pos_lr_predict_single = None
                
                # Seek a SectionCRFClassifierUtilities object
                pos_crf_predict_single = scrfcu.predict_single
                if verbose: print('scrfcu.predict_single is now available')
                
                # Seek a SectionSGDClassifierUtilities object
                pos_sgd_predict_single = ssgdcu.predict_single
                if verbose: print('ssgdcu.predict_single is now available')
                
                for feature_dict in feature_dict_list:
                    feature_tuple = hc.get_feature_tuple(
                        feature_dict, pos_lr_predict_single=pos_lr_predict_single,
                        pos_crf_predict_single=pos_crf_predict_single,
                        pos_sgd_predict_single=pos_sgd_predict_single
                    )
                    if len(feature_tuple) < 3:
                        print(feature_dict)
                    feature_tuple_list.append(feature_tuple)
            crf_list = crf.CRF.predict_single(
                crf.sent2features(feature_tuple_list)
            )
        db_pos_list = []
        for navigable_parent in child_strs_list:
            db_pos_list = cu.append_parts_of_speech_list(navigable_parent, pos_list=db_pos_list)
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
                db_pos_list = cu.append_parts_of_speech_list(
                    navigable_parent, pos_list=db_pos_list
                )
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
    
    def print_fit_job(self, row_index, row_series, fitness_threshold=2/3, verbose=True):
        job_fitness = 0.0
        file_name = row_series.file_name
        child_strs_list = hau.get_child_strs_from_file(file_name=file_name)
        indices_list = self.find_basic_quals_section_indexes(
            child_strs_list=child_strs_list, file_name=file_name, verbose=verbose
        )
        assert indices_list, f"""Something is wrong:\nfile_name = '{file_name}'\ncu.delete_filename_node(file_name, verbose=True)\n## OR, edit the file directly: ##\nfile_path = osp.join(hau.SAVES_HTML_FOLDER, file_name)\ncommand_str = fr'"C:\\Program Files\\Notepad++\\notepad++.exe" {{file_path}}'\nprint(command_str)\n!{{command_str}}\n## then run this: ##\ncu.rebuild_filename_node(file_name, navigable_parent=None, verbose=True)"""
        prequals_list = [child_str for i, child_str in enumerate(child_strs_list) if i in indices_list]
        sentence_regex = re.compile(r'[•➢\*]|\.(?!\w)')
        quals_set = set()
        fake_stops_list = ['e.g.', 'etc.', 'M.S.', 'B.S.', 'Ph.D.', '(ex.', '(Ex.',
                           'U.S.', 'i.e.', '&amp;', 'E.g.', 'Bsc.', 'MSc.', 'incl.']
        replacements_list = ['eg', 'etc', 'MS', 'BS', 'PhD', '(eg', '(eg', 'US',
                             'ie', '&', 'eg', 'BS', 'MS', 'including']
        for qual in prequals_list:
            qual = re.sub('<([a-z][a-z0-9]*)[^<>]*>', r'<\g<1>>', qual.strip(), 0, re.MULTILINE)
            for fake_stop, replacement in zip(fake_stops_list, replacements_list):
                qual = qual.replace(fake_stop, replacement)
            concatonated_quals_list = sentence_regex.split(qual)
            if len(concatonated_quals_list) > 2:
                for q1 in sent_tokenize(qual):
                    for q2 in sentence_regex.split(q1):
                        q2 = q2.strip()
                        
                        # Don't add HTML tags or blanks
                        if q2 and not re.search('^<[^><]+>$', q2):
                            quals_set.add(q2)
            else: quals_set.add(qual)
        quals_list = list(quals_set)
        assert all([isinstance(qual_str, str) for qual_str in quals_list]), f'Error in print_fit_job:\nquals_list = {quals_list}\nrow_series:\n{row_series}'
        prediction_list = list(lru.predict_job_hunt_percent_fit(
            quals_list, verbose=verbose
        ))
        quals_str, qual_count = lru.get_quals_str(prediction_list, quals_list)
        if len(prediction_list):
            job_fitness = qual_count/len(prediction_list)
            if job_fitness >= fitness_threshold:
                import enchant
                d = enchant.Dict('en_US')
                job_title = ' '.join([w for w in file_name.replace('.html', '').replace('_Indeed_com', '').split('_') if d.check(w)])
                # job_title = re.sub(r'(_-_Indeed.com)?(_[a-z0-9]{16})?\.html$', '', file_name).replace('_', ' ')
                if verbose:
                    clear_output(wait=True)
                    print(f'Basic Qualifications for {job_title}:{quals_str}')
                    print(f'{job_fitness:.2%}')
                    lru.print_loc_computation(row_index, quals_list, verbose=verbose)
        
        return quals_list, job_fitness
    
    def load_indeed_posting_url(
        self, viewjob_url, driver=None, jk_str=None, files_list=[], close_notices=True, slowed_for_readability=True, verbose=True
    ):
        file_node_dict = {}
        if jk_str is None:
            from urllib.parse import urlparse, parse_qs
            jk_str = parse_qs(urlparse(viewjob_url).query).get('jk', [''])[0]
        
        if driver is not None:
            wsu.driver_get_url(driver, viewjob_url, verbose=verbose)
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By
            from selenium.webdriver.common.keys import Keys
            import time
            
            # Close the login warning
            if close_notices:
                try:
                    
                    # Switch to the iframe with a generalized CSS selector
                    iframe_css_selector = 'iframe[src^="https://accounts.google.com/gsi/iframe/select?"]'
                    iframe = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((
                        By.CSS_SELECTOR, iframe_css_selector
                    )))
                    
                    # Perform actions inside the iframe
                    close_css = '#close'
                    close_tag = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, close_css))
                        )
                    close_tag.click()
                    
                    # Switch back to the parent HTML
                    driver.switch_to.default_content()
                    
                except Exception as e: print(f'{e.__class__.__name__} error closing login warning: {str(e).strip()}')
            
            # Close the cookie privacy notice
            if close_notices:
                try:
                    close_css = '.gnav-CookiePrivacyNoticeButton'
                    close_tag = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, close_css))
                        )
                    close_tag.click()
                except Exception as e: print(f'{e.__class__.__name__} error closing cookie privacy notice: {str(e).strip()}')
            
            # Scroll down the page so you can read it
            if slowed_for_readability:
                diffs_list = [4, 2, 0, 2, 4]
                for diff in diffs_list:
                    time.sleep(7 - diff)
                    driver.execute_script('window.scrollTo(0, window.scrollY + 800);')
        
        # Get the page soup
        from urllib.error import HTTPError, URLError
        try: page_soup = wsu.get_page_soup(viewjob_url, driver)
        except HTTPError as e:
            print(f'Got an HTTPError with {viewjob_url}: {str(e).strip()}')
        except URLError as e:
            print(f'Got an URLError with {viewjob_url}: {str(e).strip()}')
        except Exception as e:
            print(f'Got an {e.__class__.__name__} error with {viewjob_url}: {str(e).strip()}')
        
        # Get the div rows
        row_div_list = page_soup.find_all(name='div', attrs={'class': ['jobsearch-JobComponent-description']})
        
        # Write to file and update the file node dictionary
        if row_div_list:
            page_title = page_soup.find('title').string.strip()
            file_name = re.sub(r'[^A-Za-z0-9]+', ' ', page_title).strip().replace(' ', '_')
            if len(jk_str):
                file_name = f'{jk_str}_{file_name}.html'
            else:
                file_name = f'{file_name}.html'
            file_path = os.path.join(cu.SAVES_HTML_FOLDER, file_name)
            file_node_dict['file_name'] = file_name
            if not os.path.isfile(file_path):
                
                # Save the HTML to the file
                with open(file_path, 'w', encoding=nu.encoding_type) as f:
                    if verbose: print(f'Saving to {file_path}')
                    f.write('<html><head><title>')
                    f.write(page_title)
                    f.write('</title></head><body>')
                    
                    # Assume the second div is redundant
                    f.write(str(row_div_list[0]))
                    
                    f.write('</body></html>')
                
                # Delete the svg tags for easier viewing
                with open(file_path, 'r', encoding=nu.encoding_type) as f:
                    html_str = f.read()
                html_str = re.sub('<svg[^>]*>(<path[^>]*></path>)+</svg>', '', html_str)
                with open(file_path, 'w', encoding=nu.encoding_type) as f:
                    f.write(html_str)
                
                files_list.append(file_name)
            cu.ensure_filename(file_name, verbose=False)
            file_node_dict.update(cu.set_posting_url(file_name, viewjob_url, verbose=verbose))
        
        return file_node_dict, files_list
    
    def load_dice_posting_url(self, viewjob_url, driver, files_list=[], verbose=True):
        file_node_dict = {}
        from selenium.webdriver.common.by import By
        tags_list = driver.find_elements(By.CSS_SELECTOR, 'h1.pull-left')
        if not tags_list:
            title_divs_list = driver.find_elements(By.CSS_SELECTOR, 'h1[id="jt"]')
            if not title_divs_list:
                title_divs_list = driver.find_elements(By.CSS_SELECTOR, 'h1[data-cy="jobTitle"]')
            job_title_str = title_divs_list[0].text
            org_objs_list = driver.find_elements(
                By.CSS_SELECTOR, 'span[id="hiringOrganizationName"]'
            )
            if not org_objs_list:
                org_objs_list = driver.find_elements(
                    By.CSS_SELECTOR, 'a[data-cy="companyNameLink"]'
                )
            job_org_str = org_objs_list[0].text
            location_objs_list = driver.find_elements(
                By.CSS_SELECTOR, 'li[class="location"]'
            )
            if not location_objs_list:
                location_objs_list = driver.find_elements(
                    By.CSS_SELECTOR, 'li[data-cy="companyLocation"]'
                )
            job_location_str = location_objs_list[0].text
            page_title = f'{job_title_str} {job_org_str} {job_location_str}'
            file_name = self.ascii_regex.sub(' ', page_title).strip().replace(' ', '_')
            file_name = f'{file_name}.html'
            file_path = os.path.join(cu.SAVES_HTML_FOLDER, file_name)
            file_node_dict['file_name'] = file_name
            if not os.path.isfile(file_path):
                with open(file_path, 'w', encoding=nu.encoding_type) as f:
                    print(f'Saving to {file_path}')
                    f.write('<html><head><title>')
                    f.write(page_title)
                    f.write('</title></head><body><div id="jobDescriptionText">')
                    web_objs_list = driver.find_elements(
                        By.CSS_SELECTOR, 'div[id="jobdescSec"]'
                    )
                    if not web_objs_list:
                        web_objs_list = driver.find_elements(
                            By.CSS_SELECTOR, 'div[data-cy="jobDescription"]'
                        )
                    web_obj = web_objs_list[0]
                    article_str = web_obj.get_attribute('innerHTML').strip()
                    f.write(article_str)
                    f.write('</div></body></html>')
                files_list.append(file_name)
            cu.ensure_filename(file_name, verbose=False)
            file_node_dict.update(cu.set_posting_url(file_name, viewjob_url, verbose=verbose))
        
        return file_node_dict, files_list