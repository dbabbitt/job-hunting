
#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria

from . import nu
import re
import os

class HeaderAnalysis(object):
    """Header analysis class."""

    def __init__(self, verbose=False):
        self.verbose = verbose
        
        self.HTML_SCANNER_REGEX = re.compile(r'</?\w+|\w+[#\+]*|:|\.|\?')
        self.LT_REGEX = re.compile(r'\s+<')
        self.GT_REGEX = re.compile(r'>\s+')
        self.CLF_NAME = 'LogisticRegression'
        self.SAVES_HTML_FOLDER = os.path.join(nu.saves_folder, 'html')
        import matplotlib
        self.CMAP = matplotlib.colormaps.get_cmap('coolwarm')
        if nu.pickle_exists('CHILDLESS_TAGS_LIST'):
            self.CHILDLESS_TAGS_LIST = nu.load_object('CHILDLESS_TAGS_LIST')
        else:
            self.CHILDLESS_TAGS_LIST = ['template', 'script']
            nu.store_objects(CHILDLESS_TAGS_LIST=self.CHILDLESS_TAGS_LIST)
        if nu.pickle_exists('NAVIGABLE_PARENT_IS_HEADER_DICT'):
            self.NAVIGABLE_PARENT_IS_HEADER_DICT = nu.load_object('NAVIGABLE_PARENT_IS_HEADER_DICT')
        else:
            assert False, "You're in deep doodoo: you lost your basic tags dictionary"
            self.NAVIGABLE_PARENT_IS_HEADER_DICT = {}
            nu.store_objects(NAVIGABLE_PARENT_IS_HEADER_DICT=self.NAVIGABLE_PARENT_IS_HEADER_DICT)
        if nu.pickle_exists('NAVIGABLE_PARENT_IS_QUAL_DICT'):
            self.NAVIGABLE_PARENT_IS_QUAL_DICT = nu.load_object('NAVIGABLE_PARENT_IS_QUAL_DICT')
        else:
            self.NAVIGABLE_PARENT_IS_QUAL_DICT = {}
            nu.store_objects(NAVIGABLE_PARENT_IS_QUAL_DICT=self.NAVIGABLE_PARENT_IS_QUAL_DICT)

    def html_regex_tokenizer(self, corpus):

        return [match.group() for match in re.finditer(self.HTML_SCANNER_REGEX, corpus)]

    def clean_html_str(self, html_obj):
        html_str = str(html_obj)
        html_str = html_str.strip()
        html_str = self.LT_REGEX.sub('<', html_str)
        html_str = self.GT_REGEX.sub('>', html_str)

        return html_str

    def store_unique_list(self, list_name, tag_str):
        if nu.pickle_exists(list_name):
            list_obj = nu.load_object(list_name)
        else:
            list_obj = []
        list_obj.append(tag_str)
        list_obj = list(set(list_obj))
        nu.store_objects(**{list_name: list_obj})

    def store_true_or_false_dictionary(self, dict_name, tag_str, true_or_false=False):
        if nu.pickle_exists(dict_name):
            dict_obj = nu.load_object(dict_name)
        else:
            dict_obj = {}
        dict_obj[tag_str] = true_or_false
        nu.store_objects(**{dict_name: dict_obj})

    def get_navigable_children(self, tag, result_list=[]):
        from bs4.element import NavigableString
        if (type(tag) is not NavigableString):
            if hasattr(tag, 'children'):
                for child_tag in tag.children:
                    result_list = self.get_navigable_children(child_tag, result_list)
            # elif (type(tag) is not str) and (tag.name is not None):
                # self.store_unique_list('CHILDLESS_TAGS_LIST', tag.name)
        else:
            base_str = self.clean_html_str(tag)
            if re.search('[\r\n]+', base_str):
                for line_str in re.split('[\r\n]+', base_str, 0):
                    result_list.append(line_str.strip())
            elif base_str:
                tag_str = self.clean_html_str(tag.parent)
                if tag_str.count('<') > 2:
                    tag_str = base_str
                result_list.append(tag_str)

        return result_list

    def get_body_soup(self, html_str):
        from bs4 import BeautifulSoup
        page_soup = BeautifulSoup(html_str, 'lxml')
        
        # Assume at least on body tag
        body_soup = page_soup.find_all(name='body')[0]
        
        for tag in self.CHILDLESS_TAGS_LIST:
            for nu in body_soup.select(tag):
                nu.extract()

        return body_soup
    
    
    
    def get_navigable_children_from_file(self, file_name, verbose=False):
        """
        Reads an HTML file, extracts its body content, and retrieves navigable children elements.
        
        Parameters:
            file_name : str
                The name of the HTML file to be processed. It is expected to exist in the directory 
                specified by `self.SAVES_HTML_FOLDER`.
            verbose : bool, optional
                If True, additional debug information will be printed (default is False).
        
        Returns:
            list of str
                A list of strings representing the navigable children elements from the HTML file. 
                Returns an empty list if the file cannot be processed.
        
        Raises:
            AssertionError
                If the specified file does not exist in the `SAVES_HTML_FOLDER` directory.
            UnicodeDecodeError
                If the file cannot be decoded using UTF-8.
            Exception
                For other unexpected errors encountered while reading or processing the file.
        
        Notes:
            - This function assumes the existence of `self.SAVES_HTML_FOLDER`, a directory path 
              where the HTML files are stored.
            - The function also assumes the existence of `self.get_body_soup` and
              `self.get_navigable_children`, 
              which are methods for parsing the HTML content and extracting children, respectively.
        """
        
        # Initialize an empty list to store the navigable children strings
        child_strs_list = []
        
        # Construct the full file path by joining the folder path and the file name
        file_path = os.path.join(self.SAVES_HTML_FOLDER, file_name)
        
        # Assert that the file exists; raise an error with a helpful message if it doesn't
        assert os.path.isfile(file_path), (
            f"Run this and resume from the Training cell:\nfile_name = '{file_name}'\n"
            "cu.delete_filename_node(file_name, verbose=True)"
        )
        
        # Attempt to open and process the file
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                
                # Read the HTML content from the file
                html_str = f.read()
                
                # Parse the body content
                body_soup = self.get_body_soup(html_str)
                
                # Use another helper method to extract navigable children elements
                child_strs_list = self.get_navigable_children(body_soup, [])
            
            # Handle encoding errors (e.g., if the file is not UTF-8 encoded)
            except UnicodeDecodeError as e:
                print(f'UnicodeDecodeError error in {file_path}: {str(e).strip()}')
            
            # Handle any other unexpected errors and print the error message
            except Exception as e:
                print(f'{e.__class__.__name__} error in {file_path}: {str(e).strip()}')
        
        # Return the list of navigable children strings (or an empty list if an error occurred)
        return child_strs_list
    
    
    
    def html2text(self, html_str, prob_float):
        html_str = html_str.replace('<', '&lt;').replace('>', '&gt;')
        hex_str = '%02x%02x%02x' % self.CMAP(X=prob_float, bytes=True)[:-1]
        html_str = f'<span style="color:#{hex_str}">{html_str}</span>'

        return html_str

    def construct_child_tags_list(self, child_strs_list):
        child_tags_list = []
        for navigable_parent in child_strs_list:
            tokenized_sent = self.html_regex_tokenizer(navigable_parent)
            try:
                first_token = tokenized_sent[0]
                if first_token[0] == '<':
                    child_tags_list.append(first_token[1:])
                else:
                    child_tags_list.append('plaintext')
            except:
                child_tags_list.append('plaintext')

        return child_tags_list

    def construct_is_header_list(self, child_strs_list):
        is_header_list = []
        for navigable_parent in child_strs_list:
            if navigable_parent in self.NAVIGABLE_PARENT_IS_HEADER_DICT:
                is_header = self.NAVIGABLE_PARENT_IS_HEADER_DICT[navigable_parent]
            else:
                is_header = None
            is_header_list.append(is_header)

        return is_header_list