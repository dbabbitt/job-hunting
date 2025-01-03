
#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria

from . import nu, wsu, hau, cu, hc, lru, ssgdcu, scrfcu, crf, time, speech_engine
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
    
    
    def get_section(self, pos_symbol_predictions_list, pos_symbol='RQ', neg_symbol='PQ', nonheader_allows_list=['O-RQ', 'O-ER'], verbose=False):
        
        # Remove the Preferred Qualifications section
        neg_list = []
        if f'H-{neg_symbol}' in pos_symbol_predictions_list:
            neg_idx = len(pos_symbol_predictions_list) - pos_symbol_predictions_list[::-1].index(f'H-{neg_symbol}') - 1
            while (len(pos_symbol_predictions_list) > neg_idx) and (pos_symbol_predictions_list[neg_idx] == f'H-{neg_symbol}'):
                neg_idx += 1
            while (neg_idx < len(pos_symbol_predictions_list)) and (pos_symbol_predictions_list[neg_idx].split('-')[0] == 'O'):
                neg_list.append(neg_idx)
                neg_idx += 1
            
        indices_list = [i for i, x in enumerate(pos_symbol_predictions_list) if (x in nonheader_allows_list) and (i not in neg_list)]
        
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
            pos_symbol = pos_symbol + ' ' + hc.POS_EXPLANATION_DICT.get(pos_symbol, 'Unknown')
        suffix = f' ({pos_symbol})'
        idx = child_str.rfind('<')
        if idx == -1:
            child_str += suffix
        else:
            child_str = child_str[:idx] + suffix + child_str[idx:]

        return child_str


    def find_basic_quals_section_indexes(
        self, pos_symbol_predictions_list=None, child_strs_list=None,
        file_name=None, verbose=False
    ):
        if file_name is None:
            files_list = sorted([fn for fn in os.listdir(cu.SAVES_HTML_FOLDER) if fn.endswith('.html')])
            file_name = random.choice(files_list)
        if child_strs_list is None:
            child_strs_list = hau.get_navigable_children_from_file(file_name=file_name)
        if pos_symbol_predictions_list is None:
            
            # Seek a SectionLRClassifierUtilities object
            from . import slrcu
            assert hasattr(slrcu, 'pos_predict_percent_fit_dict'), 'slrcu.predict_single needs to be available'
            
            pos_symbol_predictions_list = [slrcu.predict_single(sent_str) for sent_str in child_strs_list]
        db_pos_list = []
        for navigable_parent in child_strs_list:
            db_pos_list = cu.append_parts_of_speech_list(navigable_parent, pos_list=db_pos_list)
        pos_list = []
        for predicted_symbol, db_symbol in zip(pos_symbol_predictions_list, db_pos_list):
            if db_symbol in [None, 'O', 'H']:
                pos_list.append(predicted_symbol)
            else:
                pos_list.append(db_symbol)
        # indices_list = self.get_section(pos_list)
        indices_list = [i for i, x in enumerate(pos_list) if (x in ['O-RQ', 'O-ER'])]

        return indices_list
    
    
    def visualize_basic_quals_section(self, pos_symbol_predictions_list, child_strs_list, db_pos_list=None, verbose=True):

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
        for i, (crf_symbol, db_symbol) in enumerate(zip(pos_symbol_predictions_list, db_pos_list)):
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
    
    
    @staticmethod
    def get_job_title_from_file_name(file_name, verbose=True):
        import enchant
        
        # job_title = re.sub(r'(_-_Indeed.com)?(_[a-z0-9]{16})?\.html$', '', file_name).replace('_', ' ')
        d = enchant.Dict('en_US')
        job_title = ' '.join([w for w in file_name.replace('.html', '').replace('_Indeed_com', '').split('_') if w and d.check(w)])
        
        return job_title
    
    
    def clean_qualification_string(self, child_str, attributes_to_keep=['pos']):
        
        # 1. Remove beginning and ending asterisks
        # 2. Clip child strings beginning with (3) or some other number
        # 3. Replace child strings beginning with <orq> and a number and ending in </orq>
        for pattern in [r'^\*([^<]+)\*$', r'^\(\d+\) (.+)', r'<orq>\d+ - ([^<]+)</orq>']:
            child_str = re.sub(pattern, r'\g<1>', str(child_str)).strip()
        
        # Replace child strings beginning with <tag> and ending with </tag>
        for tag in ['li', 'div', 'p', 'b', 'i', 'span', 'em', 'orq', 'strong']:
            pattern = f'<{tag}[^>]*>(.+)</{tag}>'
            child_str = re.sub(pattern, r'\g<1>', child_str).strip()
        
        # Replace child strings containing prefix_str
        prefix_strs_list = [
            ' ', '- ', '· ', '• ', '•', ', ', r'\? ', r'\*\*', r'\* ', '— ', r'\+ ',
            '" ', '-', ': ', '– ', r'\\"', r'\ufeff', r'\|', r'\)', r'\*'
        ]
        for prefix_str in prefix_strs_list:
            pattern = '^' + prefix_str
            try:
                child_str = re.sub(pattern, '', child_str).strip()
            except Exception as e:
                print(
                    f'\n{e.__class__} error in clean_qualification_string:'
                    f' {str(e).strip()}\n\npattern ='
                    f' "{pattern}"\n\nchild_str:\n{child_str}'
                )
                raise
        
        # Fix various abbreviations, et al
        fake_stops_list = [
            'e.g.', 'etc.', 'M.S.', 'B.S.', 'Ph.D.', '(ex.', '(Ex.', 'U.S.', 'i.e.',
            '&amp;', 'E.g.', 'Bsc.', 'MSc.', 'incl.', ',...)', '.).', 'Approx. ', 'approx. ',
            ' lbs. ', 'C.S.'
        ]
        replacements_list = [
            'eg', 'etc', 'MS', 'BS', 'PhD', '(eg', '(eg', 'US', 'ie', '&', 'eg', 'BS',
            'MS', 'including', ')', '.)', 'Approximately ', 'approximately ', ' lbs ',
            'CS'
        ]
        for fake_stop, replacement in zip(fake_stops_list, replacements_list):
            child_str = child_str.replace(fake_stop, replacement)
        
        # Remove all attributes from child string's tag except for attributes to keep
        from bs4 import BeautifulSoup as bs
        soup = bs(child_str, 'html.parser')
        
        # Find the first tag with attributes, regardless of what it is
        tag = soup.find()
        if tag and tag.attrs:
            
            # Remove all attributes except the ones in the list
            for attribute in list(tag.attrs):
                if attribute not in attributes_to_keep:
                    del tag.attrs[attribute]
            
            # Output the modified tag as a string
            child_str = str(tag)
        
        return child_str
    
    
    def print_fit_job(self, row_index, row_series, fitness_threshold=2/3, verbose=True):
        job_fitness = 0.0
        file_name = row_series.file_name
        child_strs_list = hau.get_navigable_children_from_file(file_name=file_name)
        indices_list = self.find_basic_quals_section_indexes(
            child_strs_list=child_strs_list, file_name=file_name, verbose=verbose
        )
        assert indices_list, f"""Run this code:\nfile_name = '{file_name}'\n#cu.delete_filename_node(file_name, verbose=True)\n## OR, edit the file directly: ##\ntext_editor_path = r'C:\\Program Files\\Notepad++\\notepad++.exe'\nfile_path = osp.abspath(osp.join(hau.SAVES_HTML_FOLDER, file_name))\nwsu.clean_job_posting(file_path)\ntry: pyperclip.copy(re.sub("((?:<li>([^><]+)</li>\\n)+)", "<ul>\\n\\1</ul>\\n", '\\n'.join(child_strs_list), 0, re.MULTILINE))\nexcept: pass\n!"{{text_editor_path}}" "{{file_path}}"\n## then run this: ##\n#cu.rebuild_filename_node(file_name, navigable_parent=None, verbose=True)"""
        prequals_list = [child_str for i, child_str in enumerate(child_strs_list) if i in indices_list]
        sentence_regex = re.compile(r'[•➢\*]|\.(?!\w)')
        quals_set = set()
        for qual in prequals_list:
            qual = self.clean_qualification_string(qual)
            concatonated_quals_list = sentence_regex.split(qual)
            if len(concatonated_quals_list) > 2:
                for q1 in sent_tokenize(qual):
                    for q2 in sentence_regex.split(q1):
                        q2 = q2.strip()
                        
                        # Don't add HTML tags or blanks
                        if q2 and not re.search('^</?[^><]+>$', q2):
                            quals_set.add(q2)
            else: quals_set.add(qual)
        quals_list = list(quals_set)
        assert all([isinstance(qual_str, str) for qual_str in quals_list]), f'Error in print_fit_job:\nquals_list = {quals_list}\nrow_series:\n{row_series}'
        # import random
        # random.shuffle(quals_list)
        prediction_list = list(lru.predict_job_hunt_percent_fit(
            quals_list, verbose=verbose
        ))
        quals_str, qual_count = lru.get_quals_str(prediction_list, quals_list, verbose=False)
        if len(prediction_list):
            job_fitness = qual_count/len(prediction_list)
            if job_fitness >= fitness_threshold:
                job_title = self.get_job_title_from_file_name(file_name)
                if verbose:
                    clear_output(wait=True)
                    print(f'Basic Qualifications for {job_title}:{quals_str}')
                    print(f'{job_fitness:.2%}')
                    lru.print_loc_computation(row_index, quals_list, verbose=verbose)
        
        return quals_list, job_fitness
    
    def load_indeed_posting_url(
        self, viewjob_url, driver=None, jk_str=None, files_list=[], close_notices=True, slowed_for_readability=True, search_type='Indeed Unknown', verbose=True
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
            
            # Close the login warning
            if close_notices:
                iframe_css_selector = 'iframe[src^="https://accounts.google.com/gsi/iframe/select?"]'
                if wsu.check_presence_by_css(driver, iframe_css_selector, wait=1, verbose=False):
                    try:
                        
                        # Switch to the iframe with a generalized CSS selector
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
                close_css = '.gnav-CookiePrivacyNoticeButton'
                if wsu.check_presence_by_css(driver, close_css, wait=1, verbose=False):
                    try:
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
            print(f'Got a URLError with {viewjob_url}: {str(e).strip()}')
        except Exception as e:
            print(f'Got an {e.__class__.__name__} error with {viewjob_url}: {str(e).strip()}')
        
        # Get the div rows
        row_div_list = page_soup.find_all(name='div', attrs={'class': ['jobsearch-JobComponent-description']})
        
        # Write to file and update the file node dictionary
        if row_div_list:
            page_title = page_soup.find('title').string.strip()
            file_name = self.ascii_regex.sub(' ', page_title).strip().replace(' ', '_')
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
                    f.write('<html>\n    <head>\n        <title>')
                    f.write(page_title)
                    f.write('</title>\n    </head>\n    <body>')
                    
                    # Assume the second div is redundant
                    body_soup = row_div_list[0]
                    
                    # Find all div elements with class "jobsearch-JobComponent-description"
                    divs = body_soup.find_all('div', class_='jobsearch-JobComponent-description')
                    
                    # Remove all other classes from these divs
                    for div in divs:
                        div['class'] = ['jobsearch-JobComponent-description']
                    
                    f.write(body_soup.prettify())
                    f.write('</body></html>')
                
                # Delete the svg tags for easier viewing
                with open(file_path, 'r', encoding=nu.encoding_type) as f:
                    html_str = f.read()
                html_str = re.sub('<svg[^>]*>(<path[^>]*></path>)+</svg>', '', html_str)
                with open(file_path, 'w', encoding=nu.encoding_type) as f:
                    f.write(html_str)
                
                files_list.append(file_name)
            cu.ensure_filename(file_name, verbose=False)
            
            # Store the file attributes and update the file node dictionary
            file_node_dict.update(cu.set_posting_url(file_name, viewjob_url, verbose=verbose))
            file_node_dict.update(cu.set_search_type(file_name, search_type, verbose=verbose))
        
        return file_node_dict, files_list
    
    
    def store_omnijobs_file_attributes(
        self, driver, viewjob_url, files_list=[], search_type='OmniJobs Unknown', verbose=True
    ):
        file_node_dict = {}
        wsu.driver_get_url(driver, viewjob_url, verbose=verbose)
        time.sleep(4)
        viewjob_url = driver.current_url
        
        from urllib.parse import urlparse
        trackingId = urlparse(viewjob_url).path.split('/')[-1]
        
        # Create the file name out of the job title and subtitle
        from selenium.webdriver.common.by import By
        titles_list = driver.find_elements(By.CSS_SELECTOR, '.text-4xl')
        assert titles_list, "Missing a job title"
        job_title_str = titles_list[0].text
        job_subtitle_str = driver.find_elements(By.CSS_SELECTOR, 'a.hover\:text-white')[0].text
        page_title = f'{job_title_str} {job_subtitle_str}'
        file_name = self.ascii_regex.sub(' ', page_title).strip().replace(' ', '_')
        
        if len(trackingId):
            file_name = f'{trackingId}_{file_name}.html'
        else:
            file_name = f'{file_name}.html'
        file_path = os.path.join(cu.SAVES_HTML_FOLDER, file_name)
        file_node_dict['file_name'] = file_name
        if not os.path.isfile(file_path):
            
            # Save the HTML to the file
            with open(file_path, 'w', encoding=nu.encoding_type) as f:
                print(f'Saving to {file_path}')
                f.write('<html>\n    <head>\n        <title>')
                f.write(page_title)
                f.write(
                    '</title>\n    </head>\n    <body>\n        <div id="jobDescriptionText">\n'
                )
                
                # Get the page soup
                web_obj = driver.find_elements(By.CSS_SELECTOR, 'div.leading-relaxed > div:nth-child(1)')[0]
                article_str = web_obj.get_attribute('innerHTML').strip()
                
                # Prettify the HTML
                from bs4.formatter import HTMLFormatter
                formatter_obj = HTMLFormatter(indent=4)
                from bs4 import BeautifulSoup as bs
                page_soup = bs(article_str, 'html.parser')
                html_str = page_soup.prettify(formatter=formatter_obj)
                
                f.write(re.sub('^', '            ', html_str, 0, re.MULTILINE).rstrip())
                f.write('\n        </div>\n    </body>\n</html>')
            
            # Delete the svg tags, remove class attributes from various tags, and tighten up the parent tag for easier viewing
            wsu.clean_job_posting(file_path)
            
            files_list.append(file_name)
        cu.ensure_filename(file_name, verbose=False)
        
        # Store the file attributes and update the file node dictionary
        file_node_dict.update(cu.set_posting_url(file_name, viewjob_url, verbose=verbose))
        file_node_dict.update(cu.set_search_type(file_name, search_type, verbose=verbose))
        
        return file_node_dict, files_list
    
    
    def store_earnbetter_file_attributes(
        self, driver, viewjob_url, files_list=[], search_type='EarnBetter Unknown', verbose=True
    ):
        file_node_dict = {}
        wsu.driver_get_url(driver, viewjob_url, verbose=verbose)
        time.sleep(4)
        viewjob_url = driver.current_url
        
        # Get what hopefully is the tracking ID
        from urllib.parse import urlparse
        query_dict = {pair[0]: pair[1] for pair in (pair.split("=") for pair in urlparse(viewjob_url).query.split("&"))}
        tracking_id = query_dict.get('tsid', '')
        
        # Create the file name out of the job title and subtitle
        page_title = driver.title
        file_name = self.ascii_regex.sub(' ', page_title).strip().replace(' ', '_')
        
        if len(tracking_id):
            file_name = f'{tracking_id}_{file_name}.html'
        else:
            file_name = f'{file_name}.html'
        file_path = os.path.join(cu.SAVES_HTML_FOLDER, file_name)
        file_node_dict['file_name'] = file_name
        if not os.path.isfile(file_path):
            
            # Save the HTML to the file
            with open(file_path, 'w', encoding=nu.encoding_type) as f:
                if verbose: print(f'Saving to {file_path}')
                f.write('<html>\n    <head>\n        <title>')
                f.write(page_title)
                f.write(
                    '</title>\n    </head>\n    <body>\n        <div id="jobDescriptionText">\n'
                )
                
                # Get the page soup
                web_obj = driver.find_elements(By.CSS_SELECTOR, 'div.leading-relaxed > div:nth-child(1)')[0]
                article_str = web_obj.get_attribute('innerHTML').strip()
                
                # Prettify the HTML
                from bs4.formatter import HTMLFormatter
                formatter_obj = HTMLFormatter(indent=4)
                from bs4 import BeautifulSoup as bs
                page_soup = bs(article_str, 'html.parser')
                html_str = page_soup.prettify(formatter=formatter_obj)
                
                f.write(re.sub('^', '            ', html_str, 0, re.MULTILINE).rstrip())
                f.write('\n        </div>\n    </body>\n</html>')
            
            # Delete the svg tags, remove class attributes from various tags, and tighten up the parent tag for easier viewing
            wsu.clean_job_posting(file_path)
            
            files_list.append(file_name)
        cu.ensure_filename(file_name, verbose=False)
        
        # Store the file attributes and update the file node dictionary
        file_node_dict.update(cu.set_posting_url(file_name, viewjob_url, verbose=verbose))
        file_node_dict.update(cu.set_search_type(file_name, search_type, verbose=verbose))
        
        return file_node_dict, files_list
    
    
    def store_linkedin_file_attributes(
        self, driver, url_str, search_type, files_list=[], verbose=False
    ):
        wsu.driver_get_url(driver, url_str, verbose=False)
        time.sleep(4)
        viewjob_url = driver.current_url
        
        from urllib.parse import parse_qs, urlparse
        trackingId = self.ascii_regex.sub(
            ' ', parse_qs(urlparse(viewjob_url).query).get('trackingId', [''])[0]
        ).strip().replace(' ', '_')
        
        # Create the file name out of the job title and subtitle
        from selenium.webdriver.common.by import By
        titles_list = driver.find_elements(By.CSS_SELECTOR, 'h1.t-24')
        if not titles_list:
            titles_list = driver.find_elements(By.CSS_SELECTOR, '#ember130 > h2:nth-child(1)')
        assert titles_list, "You probably forgot to enter the verification code"
        job_title_str = titles_list[0].text
        job_subtitle_str = driver.find_elements(
            By.CSS_SELECTOR, 'span.tvm__text:nth-child(1)'
        )[0].text
        page_title = f'{job_title_str} {job_subtitle_str}'
        file_name = self.ascii_regex.sub(' ', page_title).strip().replace(' ', '_')
        
        if len(trackingId):
            file_name = f'{trackingId}_{file_name}.html'
        else:
            file_name = f'{file_name}.html'
        file_path = os.path.join(cu.SAVES_HTML_FOLDER, file_name)
        if not os.path.isfile(file_path):
            
            # Save the HTML to the file
            with open(file_path, 'w', encoding=nu.encoding_type) as f:
                print(f'Saving to {file_path}')
                f.write('<html>\n    <head>\n        <title>')
                f.write(page_title)
                head_str = '</title>\n    </head>\n    <body>\n        <div class="jobsearc'
                head_str += 'h-JobComponent-description" id="jobDescriptionText">\n'
                f.write(head_str)
                
                # Get the page soup
                overlay_tag = driver.find_elements(
                    By.CSS_SELECTOR, '.global-nav__content'
                )[0]
                driver.execute_script(
                    "arguments[0].setAttribute('style','display:none;');", overlay_tag
                )
                wsu.click_by_xpath(driver, '/html/body//footer/button', verbose=False)
                web_obj = driver.find_elements(By.CSS_SELECTOR, '#job-details')[0]
                article_str = web_obj.get_attribute('innerHTML').strip()
                
                # Prettify the HTML
                from bs4.formatter import HTMLFormatter
                formatter_obj = HTMLFormatter(indent=4)
                from bs4 import BeautifulSoup as bs
                page_soup = bs(article_str, 'html.parser')
                html_str = page_soup.prettify(formatter=formatter_obj)
                
                f.write(re.sub('^', '            ', html_str, 0, re.MULTILINE).rstrip())
                f.write('\n        </div>\n    </body>\n</html>')
            
            # Delete the svg tags, remove class attributes from various tags, and tighten up the parent tag for easier viewing
            wsu.clean_job_posting(file_path)
            
            files_list.append(file_name)
        cu.ensure_filename(file_name, verbose=False)
        
        # Store the file attributes
        cu.set_posting_url(file_name, viewjob_url, verbose=False)
        cu.set_search_type(file_name, search_type, verbose=False)
        
        return files_list
    
    
    @staticmethod
    def get_final_url(url_str, verbose=False):
        """
        Get the final URL after following any redirects from the initial URL.
        
        Parameters:
            url_str (str): The initial URL as a string.
        
        Returns:
            str: The final URL after redirects.
        """
        import urllib.request
        
        # Open the URL and follow redirects
        try:
            with urllib.request.urlopen(url_str) as response:
                final_url = response.geturl()
            
            return final_url
        
        # Handle URL errors, such as connection issues
        except urllib.error.URLError as e:
            if verbose: print(f"URL Error: {e.reason}")
            
            return url_str
        
        # Handle HTTP errors
        except urllib.error.HTTPError as e:
            if verbose: print(f"HTTP Error: {e.code} - {e.reason}")
            
            return url_str
        
        # Handle other unexpected exceptions
        except Exception as e:
            if verbose: print(f"An error occurred: {str(e)}")
            
            return url_str
    
    
    def clean_indeed_url(self, url_str, driver=None, verbose=False):
        from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
        if driver is None:
            url_str = self.get_final_url(url_str)
        else:
            wsu.driver_get_url(driver, url_str, verbose=verbose)
            url_str = driver.current_url
        
        # Parse the URL
        parsed_url = urlparse(url_str)
        
        # Parse the query parameters
        query_params = parse_qs(parsed_url.query)
        
        # Remove the junk parameters if they exist
        for param in ['xpse', 'xfps', 'ad', 'sjdu', 'acatk']:
            if param in query_params:
                del query_params[param]
        
        # Rebuild the query string
        new_query_string = urlencode(query_params, doseq=True)
        
        # Rebuild the URL without the junk parameters
        new_url = urlunparse(parsed_url._replace(query=new_query_string))
        
        return(new_url)
    
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
    
    def populate_postings(self, driver, postings_count, files_list=[], verbose=True):
        t1 = time.time()
        try: driver.close()
        except Exception as e: print(f'{e.__class__.__name__} error: {str(e).strip()}')
        cu.ensure_navigableparent('END', verbose=False)
        from tqdm import tqdm
        progress_bar = tqdm(
            files_list, total=len(files_list), desc="Populate the Child Strings"
        )
        for file_name in progress_bar:
            file_path = os.path.join(cu.SAVES_HTML_FOLDER, file_name)
            
            # Delete each of the previous siblings of the target_div that are <div> elements
            wsu.clean_job_posting(file_path)
            
            page_soup = wsu.get_page_soup(file_path)
            row_div_list = page_soup.find_all(name='div', id='jobDescriptionText')
            assert row_div_list, f'{file_name} is missing <div id="jobDescriptionText">'
            for div_soup in row_div_list:
                child_strs_list = hau.get_navigable_children(div_soup, [])
                assert child_strs_list, f'{file_name} is missing its child strings'
                cu.populate_from_child_strings(child_strs_list, file_name, verbose=False)
        if verbose:
            import humanize
            duration_str = humanize.precisedelta(
                time.time() - t1, minimum_unit='seconds', format='%0.0f'
            )
            speech_str = f'Populating {len(files_list)} out of {postings_count} postings'
            speech_str += f' completed in {duration_str}'
            speech_engine.say(speech_str); speech_engine.runAndWait()
        
        return files_list