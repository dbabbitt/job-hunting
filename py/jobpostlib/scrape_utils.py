
#!/usr/bin/env python
# Utility Functions to Scrape Indeed.com.
# Dave Babbitt <dave.babbitt@gmail.com>
# Author: Dave Babbitt, Data Scientist
# coding: utf-8

# Soli Deo gloria

from . import nu
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
        page_soup = self.get_page_soup(file_path)
        
        # Make the job description text <div> the only tag in the <body>, if it exists
        div_soups_list = page_soup.find_all(name='div', id='jobDescriptionText')
        if div_soups_list:
            div_soup = div_soups_list[0]
            
            # Find the body tag
            body_tag = page_soup.find('body')
            
            # Clear the contents of the body tag
            body_tag.clear()
            
            # Append the div_soup to the body tag
            body_tag.append(div_soup)
        
        # Remove all style tags
        row_style_list = page_soup.find_all(name='style')
        for style_soup in row_style_list:
            style_soup.decompose()
        
        # Prettify the HTML and convert to a string
        from bs4.formatter import  HTMLFormatter
        formatter_obj = HTMLFormatter(indent=4)
        html_str = page_soup.prettify(formatter=formatter_obj)
        import re
        
        # Remove all empty tags
        empties_regex = re.compile(r'\s*<([a-z0-9]+)[^>]*>\s+</\1>')
        while empties_regex.search(html_str):
            html_str = empties_regex.sub('', html_str)
        
        # Tighten up the parent tags by removing unnecessary line breaks and indentation
        html_str = re.sub(
            r'<([^></ ]+)([^></]*)>[\r\n]+ +([^><\r\n]+)[\r\n]+ +</\1>',
            r'<\1\2>\3</\1>', html_str
        )
        
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
        if verbose: print('Getting the {} driver'.format(browser_name))
        log_dir = '../log'
        import os
        os.makedirs(name=log_dir, exist_ok=True)
        
        # Define the path for the service log
        if browser_name == 'FireFox': executable_name = 'geckodriver'
        elif browser_name == 'Chrome': executable_name = self.get_chrome_exe()
        service_log_path = os.path.join(log_dir, f'{executable_name}.log')
        
        # Initialize the driver
        from selenium import webdriver
        if browser_name == 'FireFox':
            
            # Download and configure GeckoDriver using webdriver_manager
            if verbose:
                import platform; print(f'platform.system() = {platform.system()}')
                print(f'os.name = {os.name}')
            try:
                from webdriver_manager.firefox import GeckoDriverManager
                gecko_driver_path = GeckoDriverManager().install()
                if verbose: print(f'gecko_driver_path = GeckoDriverManager().install() = {gecko_driver_path}')
                
                # Create a Service object with the downloaded path and the specified log path
                from selenium.webdriver.firefox.service import Service
                service = Service(executable_path=gecko_driver_path, log_path=service_log_path)
                
                # Launch Firefox using the created Service object
                options = webdriver.FirefoxOptions()
                # options.binary_location = gecko_driver_path
                driver = webdriver.Firefox(service=service, options=options, keep_alive=True)
                
            except Exception as e:
                print(f'{e.__class__.__name__} error getting the gecko_driver_path: {str(e).strip()}')
                gecko_driver_path = '/usr/local/bin/geckodriver'
                if verbose: print(f"gecko_driver_path = '/usr/local/bin/geckodriver' = {gecko_driver_path}")
                
                # Create a Service object with the downloaded path and the specified log path
                from selenium.webdriver.firefox.service import Service
                service = Service(executable_path=gecko_driver_path, log_path=service_log_path)
                
                # Launch Firefox using the created Service object
                options = webdriver.FirefoxOptions()
                options.binary_location = gecko_driver_path
                driver = webdriver.Firefox(service=service, options=options, keep_alive=True)
            
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
        self.fill_in_field(driver, field_name='email',
                           field_value=self.secrets_json['indeed']['email'],
                           input_css='#ifl-InputFormField-3',
                           verbose=verbose)
        # button_xpath = '/html/body/div/div[2]/main/div/div/div[2]/div/form/button'
        # self.click_by_xpath(driver, xpath=button_xpath, verbose=verbose)
        button_css = 'button.i-unmask > span:nth-child(1)'
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
        button_xpath = '/html/body/nav/div/a[2]'
        self.click_by_xpath(driver, xpath=button_xpath, verbose=verbose)
        
        # Fill in the name and password on one form
        self.fill_in_field(driver, field_name='session_key',
                           field_value=self.secrets_json['linkedin']['email'],
                           input_css='#username',
                           verbose=verbose)
        self.fill_in_field(driver, field_name='session_password',
                           field_value=self.secrets_json['linkedin']['password'],
                           input_css='#password', verbose=False)
        
        # Click the Sign in button
        button_xpath = '/html/body/div/main/div[2]/div[1]/form/div[3]/button'
        self.click_by_xpath(driver, xpath=button_xpath, verbose=verbose) 
        
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
    
    
    ### Module Functions ###
    
    
    @staticmethod
    def beep(frequency=440, duration=500, verbose=False):
        import subprocess
        
        # Script block with Beep function
        script_block = f'[System.Console]::Beep({frequency},{duration})'
        popenargs_list = ['powershell.exe', '-Command', script_block]
        if verbose: print(popenargs_list)
        
        # Call PowerShell with the script block
        subprocess.run(popenargs_list)
    
    
    @staticmethod
    def save_indeed_email_to_file(verbose=False):
        """
        Opens the Indeed HTML file with Notepad++ using PowerShell.
        
        Parameters:
            verbose (bool, optional): If True, print debug information (default is False).
        """
        import subprocess
        
        # Define the paths
        html_file_path = r'C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\data\html\indeed_email.html'
        notepad_path = r'C:\Program Files\Notepad++\notepad++.exe'
        
        # Script block with Notepad++ open function
        script_block = f'Start-Process "{notepad_path}" -ArgumentList "{html_file_path}"'
        popenargs_list = ['powershell.exe', '-ExecutionPolicy', 'Bypass', '-Command', script_block]
        if verbose: print(popenargs_list)
        
        # Call PowerShell with the script block
        subprocess.run(popenargs_list)
    
    
    @staticmethod
    def save_linkedin_email_to_file(verbose=False):
        """
        Opens the Linkedin HTML file with Notepad++ using PowerShell.
        
        Parameters:
            verbose (bool, optional): If True, print debug information (default is False).
        """
        import subprocess
        
        # Define the paths
        html_file_path = r'C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\data\html\linkedin_email.html'
        notepad_path = r'C:\Program Files\Notepad++\notepad++.exe'
        
        # Script block with Notepad++ open function
        script_block = f'Start-Process "{notepad_path}" -ArgumentList "{html_file_path}"'
        popenargs_list = ['powershell.exe', '-ExecutionPolicy', 'Bypass', '-Command', script_block]
        if verbose: print(popenargs_list)
        
        # Call PowerShell with the script block
        subprocess.run(popenargs_list)
    
    
    @staticmethod
    def save_dice_email_to_file(verbose=False):
        """
        Opens the Dice HTML file with Notepad++ using PowerShell.
        
        Parameters:
            verbose (bool, optional): If True, print debug information (default is False).
        """
        import subprocess
        
        # Define the paths
        html_file_path = r'C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\data\html\dice_email.html'
        notepad_path = r'C:\Program Files\Notepad++\notepad++.exe'
        
        # Script block with Notepad++ open function
        script_block = f'Start-Process "{notepad_path}" -ArgumentList "{html_file_path}"'
        popenargs_list = ['powershell.exe', '-ExecutionPolicy', 'Bypass', '-Command', script_block]
        if verbose: print(popenargs_list)
        
        # Call PowerShell with the script block
        subprocess.run(popenargs_list)
    
    
    @staticmethod
    def save_builtin_email_to_file(verbose=False):
        """
        Opens the built-in HTML file with Notepad++ using PowerShell.
        
        Parameters:
            verbose (bool, optional): If True, print debug information (default is False).
        """
        import subprocess
        
        # Define the paths
        html_file_path = r'C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\data\html\builtin_email.html'
        notepad_path = r'C:\Program Files\Notepad++\notepad++.exe'
        
        # Script block with Notepad++ open function
        script_block = f'Start-Process "{notepad_path}" -ArgumentList "{html_file_path}"'
        popenargs_list = ['powershell.exe', '-ExecutionPolicy', 'Bypass', '-Command', script_block]
        if verbose: print(popenargs_list)
        
        # Call PowerShell with the script block
        subprocess.run(popenargs_list)
    
    
    ### URL and Soup Functions ###
    
    