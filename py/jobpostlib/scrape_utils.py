
#!/usr/bin/env python
# Utility Functions to Scrape Indeed.com.
# Dave Babbitt <dave.babbitt@gmail.com>
# Author: Dave Babbitt, Data Scientist
# coding: utf-8

# Soli Deo gloria

from . import nu, osp
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
# from shutil import copyfile
# from urllib.request import urlretrieve
# import math
# import numpy as np
# import pandas as pd
# import random

import warnings
warnings.filterwarnings("ignore")

class WebScrapingUtilities(object):
    """
    This class implements the core of the utility functions
    needed to scrape the web mp3s.
    
    Examples
    --------
    
    >>> from jobpostlib import wsu
    """
    
    def __init__(self, secrets_json_path=None, verbose=False):
        
        # Get secrets json
        if secrets_json_path is None:
            self.secrets_json_path = osp.join(nu.data_folder, 'secrets', 'jh_secrets.json')
        else:
            self.secrets_json_path = secrets_json_path
        with open(self.secrets_json_path, 'r') as f:
            import json
            self.secrets_json = json.load(f)
        
        # Obscuration error and url patterns
        import re
        self.obscure_regex = re.compile('<([^ ]+)[^>]*class="([^"]+)"[^>]*>')
        self.url_regex = re.compile(r'\b(https?|file)://[-A-Z0-9+&@#/%?=~_|$!:,.;]*[A-Z0-9+&@#/%=~_|$]', re.IGNORECASE)
        
        # Indeed.com URL
        self.indeed_url = 'https://secure.indeed.com/account/login?hl=en_US&co=US&continue='
        self.indeed_url += 'https%3A%2F%2Fwww.indeed.com%2Fjobs%3Fq%3Ddata%2Bscientist%2B%2524100%252C000%26'
        self.indeed_url += 'forceLocation%3D032b3046-06a3-4876-8dfd-474eb5e7ed11%26remotejob%3D032b3046-06a3-4876-8dfd-474eb5e7ed11%26'
        self.indeed_url += 'from%3Dgnav-util-jobsearch--jasx&tmpl=desktop&service=my&'
        self.indeed_url += 'from=gnav-util-jobsearch--jasx&_ga=2.217171294.930897774.1613412371-1243588806.1612290936'
        
        self.linkedin_url = 'https://www.linkedin.com/home'
        self.dice_url = 'https://www.dice.com/dashboard/logout'
        
        # Local paths
        self.html_folder = osp.abspath(osp.join(nu.data_folder, 'html'))
        self.notepad_path = r'C:\Program Files\Notepad++\notepad++.exe'
    
    
    
    def get_page_soup(self, page_url_or_filepath, driver=None, verbose=False):
        match_obj = self.url_regex.search(page_url_or_filepath)
        if match_obj:
            if driver is None:
                import urllib
                with urllib.request.urlopen(page_url_or_filepath) as response:
                    page_html = response.read()
            else:
                page_html = driver.page_source
        else:
            with open(page_url_or_filepath, 'r', encoding='utf-8') as f:
                page_html = f.read()
        from bs4 import BeautifulSoup as bs
        page_soup = bs(page_html, 'html.parser')
        
        return page_soup
    
    
    
    def clean_job_posting(self, file_path):
        
        # Get the Document Object Model
        page_soup = self.get_page_soup(file_path)
        
        # Make the job description text <div> the only tag in the <body>, if it exists
        div_soups_list = page_soup.find_all(name='div', id='jobDescriptionText')
        if div_soups_list:
            div_soup = div_soups_list[0]
            
            # Find the body tag
            body_tag = page_soup.find('body')
            if body_tag:
                
                # Clear the contents of the body tag
                body_tag.clear()
                
                # Append the div_soup to the body tag
                body_tag.append(div_soup)
        
        # Remove all style tags
        row_style_list = page_soup.find_all(name='style')
        for style_soup in row_style_list:
            style_soup.decompose()
        
        # Remove the comments
        import bs4
        for comment in page_soup.find_all(text=lambda text: isinstance(text, bs4.Comment)):
            comment.extract()
        
        # Remove <span> and <em> tags only if they are the parent of another tag
        for tag_name in ['span', 'em']:
            for tag_obj in page_soup.find_all(tag_name):
                if tag_obj.children:
                    tag_obj.unwrap()
        
        # Remove class attributes from various tags
        for tag_name in ['p', 'ul', 'li', 'strong']:
            for tag_obj in page_soup.find_all(tag_name):
                if 'class' in tag_obj.attrs:
                    del tag_obj.attrs['class']
        
        # Collect all <a> tags and replace them with their text
        a_tags = page_soup.find_all('a')
        link_texts = [a_tag.text.strip() for a_tag in a_tags]
        parent_tags = [a_tag.parent for a_tag in a_tags if a_tag.parent]
        
        # Replace the <a> tag with its text
        for a_tag, link_text in zip(a_tags, link_texts):
            a_tag.replace_with(link_text)
            
        # Clean up whitespace in the parent of the replaced <a> tag
        for parent in parent_tags:
                
            # Join the strings in the parent to remove extraneous whitespace
            parent.string = ' '.join(parent.stripped_strings)
        
        # Prettify the HTML and convert to a string
        from bs4.formatter import HTMLFormatter
        formatter_obj = HTMLFormatter(indent=4)
        html_str = page_soup.prettify(formatter=formatter_obj)
        
        # Remove all empty tags
        import re
        empties_regex = re.compile(r'\s*<([a-z0-9]+)[^>]*>\s+</\1>')
        while empties_regex.search(html_str):
            html_str = empties_regex.sub('', html_str)
        
        # Remove empty <span> tags
        html_str = re.sub('[\r\n]+ +<span>[\r\n]+ +<br/>[\r\n]+ +</span>', '', html_str)
        
        # Tighten up the parent tags by removing unnecessary line breaks and indentation
        html_str = re.sub(
            r'<([^></ ]+)([^></]*)>[\r\n]+ +([^><\r\n]+)[\r\n]+ +</\1>',
            r'<\1\2>\3</\1>', html_str
        )
        
        # Fix badly-styled colons
        html_str = re.sub(r'(?<!:)</(\w+)>[\r\n]+( +):', r':</\1>\n\2', html_str)
        html_str = re.sub(r'(?<!:)</(\w+)>\s+<\1>:', ':', html_str)
        
        # Strip any leading/trailing whitespace and save the cleaned HTML back to the file
        with open(file_path, 'w', encoding=nu.encoding_type) as f:
            print(html_str.strip(), file=f)
    
    
    
    def replace_phrase_elements_in_block_elements(self, file_path, block_elements_set, phrase_elements_set={'b', 'strong'}, verbose=False):
        
        # Get the Document Object Model
        page_soup = self.get_page_soup(file_path)
        
        # Find all <b> and <strong> tags
        b_tags = page_soup.find_all(phrase_elements_set)
        b_texts = [b_tag.text.strip() for b_tag in b_tags]
        
        # List to track parents that need whitespace cleanup
        cleanup_list = []
        
        # Iterate over each <b> tag
        for b_tag, b_text in zip(b_tags, b_texts):
            parent_tag = b_tag.parent
            
            # Check if the parent of the <b> tag is a block element
            if parent_tag and parent_tag.name in block_elements_set:
                
                # Replace the <b> tag with its text
                b_tag.replace_with(b_text)
                
                # Add parent to cleanup list
                cleanup_list.append(parent_tag)
            
        # Clean up whitespace in the parents of the replaced <b> tags without affecting <br />
        from bs4 import BeautifulSoup
        from bs4.element import Tag
        for parent in cleanup_list:
                
            # Collect content parts, preserving <br /> tags
            p_contents = [p for p in parent.contents if (isinstance(p, str) and p.strip()) or isinstance(p, Tag)]
            contents = []
            for element in parent.contents:
                if element.name == 'br':
                    contents.append(str(element))  # Preserve <br /> as a string
                else:
                    contents.append(element.strip() if isinstance(element, str) else element.text.strip())
            
            # Join them with a space while ensuring <br /> tags are preserved
            html_str = ' '.join(contents)
            
            # Tighten up the gaps
            for suffix in [' ', ',']:
                html_str = html_str.replace(' ' + suffix, suffix)
            
            parent.clear()  # Clear existing content
            parent.append(BeautifulSoup(html_str, 'html.parser'))
        
        # Prettify the HTML and convert to a string
        from bs4.formatter import HTMLFormatter
        formatter_obj = HTMLFormatter(indent=4)
        html_str = page_soup.prettify(formatter=formatter_obj)
        
        # Strip any leading/trailing whitespace and save the cleaned HTML back to the file
        with open(file_path, 'w', encoding=nu.encoding_type) as f:
            print(html_str.strip(), file=f)
    
    
    
    def convert_p_b_to_h3(self, file_path, basic_text_set={'p'}, phrase_elements_set={'b', 'strong'}, verbose=False):
        """
        Convert <p> tags containing exactly one phrase_elements_set tag to <h3> tags with specific attributes.
        
        Parameters:
            file_path (str): The file path to the HTML content to parse and modify.
            basic_text_set (set): the tag set, defaulting to {'p'}, that is the parent tag we are referring to as the <p> tag
            phrase_elements_set (set): the tag name, like 'b' or 'strong', that we are looking for inside the <p> tag
        
        Returns:
            None
        """
        
        # Get the Document Object Model
        page_soup = self.get_page_soup(file_path)
        
        # Find all <p> tags
        p_tags = page_soup.find_all(basic_text_set)
        
        from bs4 import BeautifulSoup
        from bs4.element import Tag
        for p_tag in p_tags:
            p_contents = [p for p in p_tag.contents if (isinstance(p, str) and p.strip()) or (isinstance(p, Tag) and p.name in phrase_elements_set)]
            
            # Check if the <p> tag contains exactly one <b> tag as its only content
            if len(p_contents) == 1 and isinstance(p_contents[0], Tag) and p_contents[0].name in phrase_elements_set:
                b_tag = p_contents[0]
                
                # Get the stripped text of the <b> tag
                b_text = b_tag.text.strip()
                
                # Ensure that the text ends with a colon
                if not any(map(lambda x: b_text.endswith(x), [':', '?', '!', '.', '*'])):
                    b_text += ':'
                
                # Create a new <h3> tag with the desired attributes
                h3_tag = page_soup.new_tag('h3', **{'class': 'jobSectionHeader', 'pos': 'H-XX'})
                
                # Set the text of the new <h3> tag
                h3_tag.string = b_text
                
                # Replace the <p> tag with the new <h3> tag
                p_tag.replace_with(h3_tag)
        
        # Check the modified page_soup to ensure the <p> tag has been replaced
        if verbose:
            print("After replacement:")
            for tag in page_soup.find_all('h3'):
                print(str(tag))  # This will show the new <h3> tags in the page_soup
        
        # Prettify the HTML and convert to a string
        from bs4.formatter import HTMLFormatter
        formatter_obj = HTMLFormatter(indent=4)
        html_str = page_soup.prettify(formatter=formatter_obj)
        if verbose:
            print(html_str)
        
        # Try converting <p> tags containing exactly one <b> tag to <h3> tags with regex
        import re
        pattern = r'<p>\s+<(' + '|'.join(phrase_elements_set) + r')>\s*([^><\r\n]+):?\s*</\1>\s+</p>'
        repl = r'<h3 class="jobSectionHeader" pos="H-O">\2:</h3>'
        html_str = re.sub(pattern, repl, html_str).strip() # Strip any leading/trailing white space
        if verbose:
            print(pattern)
            print(repl)
            print(html_str)
        
        # Save the cleaned HTML back to the file
        with open(file_path, 'w', encoding=nu.encoding_type) as f:
            print(html_str, file=f)

    
    
    def replace_single_child_tags_in_li(self, file_path, verbose=False):
        """
        Replace child tags with their text content if the parent is an
        <li> tag and it contains only that single child tag.

        Parameters:
            file_path (str): The file path to the HTML content to parse and modify.

        Returns:
            None
        """
        
        # Get the Document Object Model
        page_soup = self.get_page_soup(file_path)
        
        # Find all <li> tags
        li_tags = page_soup.find_all('li')
        
        from bs4.element import Tag
        for li_tag in li_tags:
            
            # Check if the <li> tag contains exactly one child that is a tag
            child_tags = [c for c in li_tag.contents if (isinstance(c, Tag) or (isinstance(c, str) and c.strip()))]
            if len(child_tags) == 1:
                child_tag = child_tags[0]
                if isinstance(child_tag, Tag):
                    
                    # Replace the child tag with its text content
                    li_tag.string = child_tag.text.strip()
                    # child_tag.replace_with(child_tag.text.strip())
        
        # Prettify the HTML and convert to a string
        from bs4.formatter import HTMLFormatter
        formatter_obj = HTMLFormatter(indent=4)
        html_str = page_soup.prettify(formatter=formatter_obj)
        
        # Strip any leading/trailing whitespace and save the cleaned HTML back to the file
        with open(file_path, 'w', encoding=nu.encoding_type) as f:
            print(html_str.strip(), file=f)
    
    
    
    def get_dupes(self, strings_list, verbose=False):
        seen_dict = {}
        dupes_list = []
        for list_item in strings_list:
            if list_item not in seen_dict:
                seen_dict[list_item] = 1
            else:
                if seen_dict[list_item] == 1:
                    dupes_list.append(list_item)
                seen_dict[list_item] += 1
        if verbose:
            print(f'Maximum duplication level: {max(seen_dict.values())}')
        
        return dupes_list
    
    
    
    def conjunctify_nouns(self, noun_list):
        if len(noun_list) > 2:
            last_noun_str = noun_list[-1]
            but_last_nouns_str = ', '.join(noun_list[:-1])
            list_str = ', and '.join([but_last_nouns_str, last_noun_str])
        elif len(noun_list) == 2:
            list_str = ' and '.join(noun_list)
        elif len(noun_list) == 1:
            list_str = noun_list[0]
        else:
            list_str = ''
        
        return list_str

    def check_presence_by_css(self, driver, element_css, wait=10, verbose=False):
        """
        Check if an element with the given CSS selector is present on the page.
        
        Params:
            self: The instance of the class (if this is a method in a class)
            driver: Selenium WebDriver instance
            element_css (str): CSS selector of the element to check
            wait (int): Maximum time to wait for the element (default 10 seconds)
            verbose (bool): If True, print status messages (default False)
        
        Returns:
            bool: True if the element is present, False otherwise
        """
        try:
            # Wait for up to 'wait' seconds for the element to be present
            element = WebDriverWait(driver, wait).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, element_css))
            )
            if verbose:
                print(f"The element with CSS selector '{element_css}' is present on the page.")
            return True
        except:
            if verbose:
                print(f"The element with CSS selector '{element_css}' is not present on the page.")
            return False
    
    
    
    def move_to_element_by_css(self, driver, move_css, wait=10, verbose=False):
        if verbose:
            print('Moving to {}'.format(move_css))
        
        # Wait for element to show up
        web_element = WebDriverWait(driver, wait).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, move_css))
            )
        
        # Move to where it is
        driver.execute_script('arguments[0].scrollIntoView();', web_element)
        ActionChains(driver).move_to_element(web_element).perform()
        
        return web_element
    
    
    
    def click_by_css(self, driver, click_css, wait=10, verbose=False):
        if verbose:
            print('Clicking {}'.format(click_css))
        
        # Move to where it is, then click it
        from selenium.common.exceptions import ElementClickInterceptedException, MoveTargetOutOfBoundsException
        try:
            click_obj = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, click_css))
                )
            driver.execute_script('arguments[0].scrollIntoView();', click_obj)
        except (ElementClickInterceptedException, MoveTargetOutOfBoundsException):
            pass
        #web_element = self.move_to_element_by_css(driver, click_css, wait=wait)
        web_element = WebDriverWait(driver, wait).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, click_css))
            )
        web_element.click()
        
        return web_element
    
    
    def get_web_element_text_css(self, driver, text_css, wait=10, verbose=False):
        if verbose:
            print('Getting the text of {}'.format(text_css))
        web_element_str = ''
        try:
            web_element = WebDriverWait(driver, wait).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, text_css))
                )
            web_element_str = web_element.text.strip()
        except Exception as e:
            message = str(e).strip()
            print('Waiting for the web element to show up: {}'.format(message))
        
        return web_element_str
    
    
    
    
    def enter_text_by_css(self, driver, field_value, input_css, verbose=True):
        if verbose:
            print('Moving to {} and entering {}'.format(input_css, field_value))
        
        # Move to where it is, then enter text into it
        try:
            web_element = self.move_to_element_by_css(driver, input_css)
            web_element.send_keys(field_value)
            web_element.send_keys(Keys.ENTER)
        except Exception as e:
            message = str(e).strip()
            raise Exception('Waiting for input field to show up: {}'.format(message))
    
    
    
    
    def fill_in_field(self, driver, field_name, field_value, input_css=None, verbose=True):
        if verbose:
            print('Filling in the {} field with {}'.format(field_name, field_value))
        if input_css is None:
            input_css = 'input[name="{}"]'.format(field_name)
        try:
            input_tag = self.click_by_css(driver, input_css)
            self.select_all(driver)
            input_tag.send_keys(field_value)
            
        except Exception as e:
            message = str(e).strip()
            raise Exception('Waiting for input field to show up: {}'.format(message))
    
    
    
    def click_by_xpath(self, driver, xpath, verbose=True):
        if verbose:
            print('Clicking {}'.format(xpath))
        try:
            web_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
                )
            ActionChains(driver).move_to_element(web_element).perform()
            web_element.click()
        except Exception as e:
            message = str(e).strip()
            if verbose:
                print('Waiting for the web element to be visible: {}'.format(message))
            if ('obscures' in message) or ('Other element would receive the click' in message):
                tag_list = self.obscure_regex.findall(message)
                while len(tag_list) == 2:
                    self.unobscure_element(driver, tag_list[1])
                    try:
                        web_element = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, xpath))
                            )
                        ActionChains(driver).move_to_element(web_element).perform()
                        web_element.click()
                        message = ''
                    except Exception as e:
                        message = str(e).strip()
                        if verbose:
                            print('Waiting for the web element to be visible (unobscured): {}'.format(message))
                    tag_list = self.obscure_regex.findall(message)
    
    
    
    
    def driver_get_url(self, driver, url_str, verbose=True):
        if verbose:
            print('Getting URL: {}'.format(url_str))
        finished = 0
        fails = 0
        while (finished == 0) and (fails < 8):
            try:
                
                # Message: Timeout loading page after 100000ms
                driver.set_page_load_timeout(300)
                
                driver.get(url_str)
                finished = 1
            except Exception as e:
                message = str(e).strip()
                if verbose:
                    print(message)
                fails += 1
                
                # Wait for 10 seconds
                self.wait_for(10, verbose=verbose)
    
    
    
    
    def select_all(self, driver):
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
    
    
    
    def get_contains_list(self, div_class_list):
        
        return ["contains(@class, '{}')".format(c) for c in div_class_list]
    
    
    
    def get_div(self, div_class_str):
        
        return 'div[{}]'.format(' and '.join(self.get_contains_list(div_class_str.split(' '))))
    
    
    
    def get_chrome_exe(self, file_path=r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'):
        version_num = 0
        try:
            from win32com.client import Dispatch
            parser = Dispatch('Scripting.FileSystemObject')
            version_str = parser.GetFileVersion(file_path)
            version_num = int(version_str.split('.')[0])
        except Exception as e:
            print(f'Error getting chrome version: {str(e).strip()}')

        return f'chromedriver{version_num}'
    
    
    
    def get_driver(self, browser_name='FireFox', verbose=False):
        if verbose: print(f'Getting the {browser_name} driver')
        
        # Define the path for the service log
        log_dir = '../log'
        import os
        os.makedirs(name=log_dir, exist_ok=True)
        if browser_name == 'FireFox': executable_name = 'geckodriver'
        elif browser_name == 'Chrome': executable_name = self.get_chrome_exe()
        service_log_path = os.path.join(log_dir, f'{executable_name}.log')
        
        # Initialize the driver
        from selenium import webdriver
        from selenium.webdriver.firefox.service import Service
        from selenium.webdriver.firefox.options import Options
        from webdriver_manager.firefox import GeckoDriverManager
        
        if browser_name == 'FireFox':
            if verbose:
                import platform
                print(f'platform.system() = {platform.system()}')
                print(f'os.name = {os.name}')
            
            # Download and configure gecko driver using manager
            try:
                gecko_driver_path = GeckoDriverManager().install()
                if verbose:
                    print(
                        'gecko_driver_path = GeckoDriverManager().install()'
                        f' = {gecko_driver_path}'
                    )
                
                # Specify the path to the Firefox binary
                # options = webdriver.FirefoxOptions()
                options = Options()
                firefox_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"
                assert_str = f"Firefox not found at {firefox_path}."
                assert_str += " Please specify the correct path."
                assert os.path.exists(firefox_path), assert_str
                options.binary_location = firefox_path
                
                # Create a Service object with the downloaded path and
                # the specified log path
                service = Service(
                    executable_path=gecko_driver_path, log_path=service_log_path
                )
                
                # Launch Firefox using the created Service object
                driver = webdriver.Firefox(
                    service=service, options=options, keep_alive=True
                )
                
            except Exception as e:
                print(
                    f'{e.__class__.__name__} error getting'
                    f' the gecko_driver_path: {str(e).strip()}'
                )
                gecko_driver_path = '/usr/local/bin/geckodriver'
                if verbose:
                    print(
                    "gecko_driver_path = '/usr/local/bin/geckodriver'"
                    f" = {gecko_driver_path}"
                    )
                
                # Create a Service object with the downloaded path and
                # the specified log path
                service = Service(
                    executable_path=gecko_driver_path, log_path=service_log_path
                )
                
                # Launch Firefox using the created Service object
                options = webdriver.FirefoxOptions()
                options.binary_location = gecko_driver_path
                driver = webdriver.Firefox(
                    service=service, options=options, keep_alive=True
                )
            
        elif browser_name == 'Chrome':
            co = webdriver.ChromeOptions()
            co.add_argument('--no-sandbox')
            driver = webdriver.Chrome(
                chrome_options=None,
                keep_alive=True,
                options=co,
                port=0,
                service_log_path=service_log_path,
            )
        
        # Set timeout information and maximize
        driver.set_page_load_timeout(20)
        driver.maximize_window()
        
        return driver
    
    
    
    def get_last_sunday(self, today=None):
        if today is None:
            from datetime import datetime
            today = datetime.now()
        from datetime import timedelta
        start = today - timedelta((today.weekday() + 1) % 7)
        from dateutil import relativedelta
        
        return start + relativedelta.relativedelta(weekday=relativedelta.SU(-1))
    
    
    
    def get_web_element(self, driver, xpath):
        try:
            web_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, xpath))
                )
            
            return web_element
            
        except Exception as e:
            message = str(e).strip()
            print('Waiting for the web_element to show up: {}'.format(message))
    
    
    
    def key_in_search(self, driver, input_xpath, field_value, verbose=True):
        if verbose:
            print('Searching for: {}'.format(field_value))
        input_tag = self.get_web_element(driver, input_xpath)
        input_tag.click()
        self.select_all(driver)
        input_tag.send_keys(field_value)
        ActionChains(driver).key_down(Keys.ENTER).perform()
    
    
    def log_into_indeed(self, driver, verbose=True):
        self.driver_get_url(driver, self.indeed_url, verbose=verbose)
        self.fill_in_field(
            driver, field_name='email',
            field_value=self.secrets_json['indeed']['email'],
            input_css='#ifl-InputFormField-ihl-useId-passport-webapp-1',
            verbose=verbose
        )
        # button_xpath = '/html/body/div/div[2]/main/div/div/div[2]/div/form/button'
        # self.click_by_xpath(driver, xpath=button_xpath, verbose=verbose)
        button_css = 'button.dd-privacy-allow > span:nth-child(1)'
        self.click_by_css(driver, button_css, wait=10, verbose=verbose)
        
        # Look for password field
        link_xpath = '//*[@id="auth-page-google-password-fallback"]'
        self.click_by_xpath(driver, xpath=link_xpath, verbose=verbose)
        try:
            self.fill_in_field(driver, field_name='password',
                               field_value=self.secrets_json['indeed']['password'],
                               input_css='#ifl-InputFormField-121', verbose=verbose)
            button_xpath = '/html/body/div/div[2]/main/div/div/div[2]/div/form[1]/button'
            self.click_by_xpath(driver, xpath=button_xpath, verbose=verbose)
        except Exception as e:
            print(f'Error trying to fill in the password field: {str(e).strip()}')
        
        # Stall for time while looking for the error message
        indeed_xpath = '/html/body/main/div/ul'
        indeed_error_tag = self.get_web_element(driver, indeed_xpath)
        
        return indeed_error_tag
    
    
    def log_into_linkedin(self, driver, verbose=True):
        self.driver_get_url(driver, self.linkedin_url, verbose=verbose)
        
        # Click the Sign in button
        # button_xpath = '/html/body/nav/div/a[2]'
        # self.click_by_xpath(driver, xpath=button_xpath, verbose=verbose)
        click_css = '.sign-in-form__sign-in-cta'
        self.click_by_css(driver, click_css, wait=10, verbose=verbose)
        
        # Click the Sign In link
        click_css = 'a[href^="https://www.linkedin.com/uas/login"]'
        if self.check_presence_by_css(driver, click_css, wait=1, verbose=False):
            self.click_by_css(driver, click_css, wait=10, verbose=verbose)
        
        # Fill in the name and password on one form
        self.fill_in_field(driver, field_name='session_key',
                           field_value=self.secrets_json['linkedin']['email'],
                           input_css='#username',
                           verbose=verbose)
        self.fill_in_field(driver, field_name='session_password',
                           field_value=self.secrets_json['linkedin']['password'],
                           input_css='#password', verbose=False)
        
        # Click the Sign in button
        # button_xpath = '/html/body/div/main/div[2]/div[1]/form/div[3]/button'
        # self.click_by_xpath(driver, xpath=button_xpath, verbose=verbose)
        click_css = '.btn__primary--large'
        self.click_by_css(driver, click_css, wait=10, verbose=verbose)
        
        # Stall for time while looking for the error message
        # linkedin_xpath = '/html/body/main/div/ul'
        # linkedin_error_tag = self.get_web_element(driver, linkedin_xpath)
        
        # return linkedin_error_tag
    
    
    def log_into_dice(self, driver, verbose=True):
        self.driver_get_url(driver, self.dice_url, verbose=verbose)
        
        # Fill in the name and click the button on one form
        # <input aria-labelledby="react-aria538911564-:r1:" aria-required="true" autocomplete="email" placeholder="Please enter your email" inputmode="email" data-rac="" type="email" value="" name="email">
        self.fill_in_field(driver, field_name='email',
                           field_value=self.secrets_json['dice']['email'],
                           input_css='div.mb-2 > input[type="email"]',
                           verbose=verbose)
        
        # Click the Sign In button
        button_xpath = '/html/body/div[3]/div/div/div[2]/div/form/button'
        self.click_by_xpath(driver, xpath=button_xpath, verbose=verbose)
        
        # Fill in the password and click the button on the next form
        # <input aria-labelledby="react-aria160671220-:r6:" autocomplete="current-password" placeholder="Enter Password" data-rac="" type="password" value="" name="password">
        self.fill_in_field(driver, field_name='password',
                           field_value=self.secrets_json['dice']['password'],
                           input_css='div.mb-2 > input[type="password"]', verbose=False)
        
        # Click the Submit Password button
        button_xpath = '/html/body/div[3]/div/div/div[2]/div/form/button'
        self.click_by_xpath(driver, xpath=button_xpath, verbose=verbose)
    
    
    
    def similar(self, a, b):
        from difflib import SequenceMatcher
        
        return SequenceMatcher(None, str(a), str(b)).ratio()
    
    
    
    def unobscure_element(self, driver, match_tuple):
        tag_name = match_tuple[0]
        class_str = '.'.join([cn for cn in match_tuple[1].split(' ') if cn != 'hidden'])
        overlay_css = '{}.{}'.format(tag_name, class_str)
        try:
            
            # Wait for overlay div to show up
            overlay_tag = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, overlay_css))
                )
            print('Hiding <{}'.format(overlay_tag.get_attribute('outerHTML').split('<')[1]))
            driver.execute_script("arguments[0].setAttribute('style','display:none;');", overlay_tag)
        
        except Exception as e:
            message = str(e).strip()
            print('Waiting for {} {} to show up before hiding it: {}'.format(class_str, tag_name, message))
            driver.refresh()
    
    
    
    def wait_for(self, wait_count, verbose=True):
        if verbose:
            print('Waiting for {} seconds'.format(wait_count))
        import time
        time.sleep(wait_count)



    def fill_in_textarea(self, driver, field_name, field_value):
        print('Filling in the {} field with {}'.format(field_name, field_value))
        input_css = 'textarea[name="{}"]'.format(field_name)
        try:
            input_tag = self.click_by_css(driver, input_css)
            self.select_all(driver)
            input_tag.send_keys(field_value)
        except Exception as e:
            message = str(e).strip()
            raise Exception('Waiting for textarea field to show up: {}'.format(message))



    def get_chatgpt_rephrasing(
        self, driver, original_phrase, part_of_speech='minimum requirement', verbose=True
    ):
        youchat_text = ''
        youchat_str = f'Rewrite this sentence so it sounds like a {part_of_speech}: "{original_phrase}"'
        from urllib.parse import quote_plus
        youchat_url = f'https://you.com/search?q={quote_plus(youchat_str)}&fromSearchBar=true&tbm=youchat'
        self.driver_get_url(driver, youchat_url, verbose=False)
        if verbose:
            print(youchat_str)
        div_css = 'div[data-testid="youchat-text"]'
        # from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException
        try:
            div_obj = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, div_css))
            )
            
            # Wait for the div to be in its final state
            self.wait_for(2, verbose=False)
            
            # Assume its finished writing the answer
            div_obj = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, div_css))
            )
            
            youchat_text = div_obj.text
            if verbose:
                print(youchat_text)
        # except NoSuchElementException as e:
            # pass
        except Exception as e:
            print(f'{e.__class__.__name__} error: {str(e).strip()}')
            raise
        
        return youchat_text
    
    
    ### List Functions ###
    
    
    ### Storage Functions ###
    
    
    ### Subprocess Functions ###
    
    
    @staticmethod
    def beep(frequency=440, duration=500, verbose=False):
        import subprocess
        
        # Script block with Beep function
        script_block = f'[System.Console]::Beep({frequency},{duration})'
        popenargs_list = ['powershell.exe', '-Command', script_block]
        if verbose: print(popenargs_list)
        
        # Call PowerShell with the script block
        subprocess.run(popenargs_list)
    
    
    def save_email_to_file(self, filename_prefix, verbose=False):
        """
        Opens the HTML file with Notepad++ using PowerShell.
        
        Parameters:
            verbose (bool, optional): If True, print debug information (default is False).
        """
        import subprocess
        
        # Define the paths
        html_file_path = osp.join(self.html_folder, f'{filename_prefix}_email.html')
        
        # Script block with Notepad++ open function
        script_block = f'Start-Process "{self.notepad_path}" -ArgumentList "{html_file_path}"'
        popenargs_list = ['powershell.exe', '-ExecutionPolicy', 'Bypass', '-Command', script_block]
        if verbose: print(popenargs_list)
        
        # Call PowerShell with the script block
        subprocess.run(popenargs_list)
    
    
    ### URL and Soup Functions ###
    
    