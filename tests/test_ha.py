
#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



# cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\tests
# python -m unittest test_ha.TestHaMethods.test_find_basic_quals_section

import unittest
import os
from bs4 import BeautifulSoup
# import shutil, tempfile

class TestHaMethods(unittest.TestCase):
    def setUp(self):
        import sys
        if (osp.join(os.pardir, 'py') not in sys.path): sys.path.insert(1, osp.join(os.pardir, 'py'))
        
        from storage import Storage
        self.s = Storage()
        
        from ha_utils import HeaderAnalysis
        self.ha = HeaderAnalysis(verbose=True)
        
        import warnings
        warnings.filterwarnings('ignore')
        
        # Create a temporary directory
        # self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        # Remove the directory after the test
        # shutil.rmtree(self.test_dir)
        
        file_name = 'test.html'
        file_path = os.path.join(self.ha.SAVES_HTML_FOLDER, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
        
        list_name = 'test_list'
        if self.s.pickle_exists(list_name):
            pickle_path = os.path.join(self.s.saves_pickle_folder, f'{list_name}.pkl')
            os.remove(pickle_path)
    
    def test_clean_html_str(self):
        soup = BeautifulSoup('''
            <p>
                Hello <i> World </i> !
            </p>\t''', 'html.parser')
        self.assertEqual(self.ha.clean_html_str(soup), '<p>Hello<i>World</i>!</p>')

    def test_get_body_soup(self):
        from bs4.element import Tag
        html_str = '<html><head><title>Hello World!</title></head><body><template>//Not this!!'
        html_str += '</template><script>a = 5;</script><p>Hello <i>World</i>!</p></body><body>Not this!!</body></html>'
        body_soup = self.ha.get_body_soup(html_str)
        self.assertEqual(type(body_soup), Tag)
        self.assertEqual(str(body_soup), '<body><p>Hello <i>World</i>!</p></body>')

    def test_get_child_strs_from_file(self):
        file_name = 'test.html'
        file_path = os.path.join(self.ha.SAVES_HTML_FOLDER, file_name)
        html_str = '<html><head><title>Hello World!</title></head><body><template>//Not this!!'
        html_str += '</template><script>a = 5;</script><p>Hello <i>World</i>!</p></body><body>Not this!!</body></html>'
        with open(file_path, 'w', encoding='utf-8') as f:
            print(html_str, file=f)
        self.assertEqual(self.ha.get_navigable_children_from_file(file_name), ['Hello', '<i>World</i>', '!'])

    def test_get_child_tags_list(self):
        child_strs_list = ['Hello', '<i>World</i>', '!']
        self.assertEqual(self.ha.construct_child_tags_list(child_strs_list), ['plaintext', 'i', 'plaintext'])

    def test_get_is_header_list(self):
        child_strs_list = ['<li>Expertise with GCP and AWS including Docker containers and Kubernetes</li>',
                           "<b>What you'll have:</b>",
                           '<div>Experience with SaaS applications in the cloud and a solid understanding of cloud technologies ' +
                           '(AWS preferably)</div>']
        self.assertEqual(self.ha.construct_is_header_list(child_strs_list), [False, True, False])

    def test_html_regex_tokenizer(self):
        corpus = '<li>Experience in one of more programming languages – Python, .Net, Java, C++, R, etc.</li>'
        tokens_list = ['<li', 'Experience', 'in', 'one', 'of', 'more', 'programming', 'languages', 'Python', '.',
                       'Net', 'Java', 'C++', 'R', 'etc', '.', '</li']
        self.assertEqual(self.ha.html_regex_tokenizer(corpus), tokens_list)

    def test_html2text(self):
        html_str_in = '<p>Hello <i>World</i>!</p>'
        prob_float = 0.5
        html_str_out = '<span style="color:#dddcdb">&lt;p&gt;Hello &lt;i&gt;World&lt;/i&gt;!&lt;/p&gt;</span>'
        self.assertEqual(self.ha.html2text(html_str_in, prob_float), html_str_out)

    def test_store_unique_list(self):
        tag_str1 = 'test_tag1'
        tag_str2 = 'test_tag2'
        list_name = 'test_list'
        if self.s.pickle_exists(list_name):
            pickle_path = os.path.join(self.s.saves_pickle_folder, f'{list_name}.pkl')
            os.remove(pickle_path)
        self.ha.store_unique_list(list_name, tag_str1)
        self.assertTrue(self.s.pickle_exists(list_name))
        test_list = self.s.load_object('test_list')
        self.assertTrue(tag_str1 in test_list)
        self.ha.store_unique_list(list_name, tag_str2)
        test_list = self.s.load_object('test_list')
        self.assertTrue(tag_str2 in test_list)

    def test_get_navigable_children(self):
        html_str = '<body><template>//Not this!!</template><script>a = 5;</script><p>Hello <i>World</i>!</p></body>'
        tag = BeautifulSoup(html_str)
        result_list = []
        child_strs_list = self.ha.get_navigable_children(tag, result_list)
        self.assertEqual(child_strs_list, ['Hello', '<i>World</i>', '!'])

    def test_store_true_or_false_dictionary(self):
        tag_str1 = 'test_tag1'
        tag_str2 = 'test_tag2'
        dict_name = 'test_dict'
        if self.s.pickle_exists(dict_name):
            pickle_path = os.path.join(self.s.saves_pickle_folder, f'{dict_name}.pkl')
            os.remove(pickle_path)
        self.ha.store_true_or_false_dictionary(dict_name, tag_str1, true_or_false=True)
        self.assertTrue(self.s.pickle_exists(dict_name))
        test_dict = self.s.load_object('test_dict')
        self.assertTrue(tag_str1 in test_dict)
        self.assertTrue(test_dict[tag_str1])
        self.ha.store_true_or_false_dictionary(dict_name, tag_str2, true_or_false=False)
        test_dict = self.s.load_object('test_dict')
        self.assertTrue(tag_str2 in test_dict)
        self.assertFalse(test_dict[tag_str2])

if __name__ == '__main__':
    unittest.main()