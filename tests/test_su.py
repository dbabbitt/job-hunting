
#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



# cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\tests
# cls
# python -m unittest test_su.TestSuMethods.test_get_section3

import unittest

class TestSuMethods(unittest.TestCase):
    def setUp(self):
        import sys
        import os
        sys.path.insert(1, '../py')
        
        from storage import Storage
        self.s = Storage()
        
        from ha_utils import HeaderAnalysis
        self.ha = HeaderAnalysis(s=s, verbose=False)
        
        from scrape_utils import WebScrapingUtilities
        wsu = WebScrapingUtilities()
        uri = wsu.secrets_json['neo4j']['connect_url']
        user =  wsu.secrets_json['neo4j']['username']
        password = wsu.secrets_json['neo4j']['password']
        
        from cypher_utils import CypherUtilities
        self.cu = CypherUtilities(uri=uri, user=user, password=password, driver=None, s=self.s, ha=self.ha)
        
        from hc_utils import HeaderCategories
        self.hc = HeaderCategories(cu=self.cu, verbose=False)
        
        from section_utils import SectionUtilities
        self.su = SectionUtilities(s = self.s, ha=self.ha, cu=self.cu, hc=self.hc, verbose=False)
        
        import warnings
        warnings.filterwarnings('ignore')
    

    def test_get_section1(self):
        pos_list = ['O-CS', 'O-IP', 'O-CS', 'O-TS', 'H-RQ', 'O-TS', 'O-TS', 'O-RQ', 'O-TS', 'O-RQ', 'O-TS', 'O-TS', 'O-RQ',
                    'O-RQ', 'H-RQ', 'O-PQ', 'O-RQ', 'O-TS', 'O-TS', 'O-TS', 'O-PQ', 'O-RQ', 'O-TS', 'O-TS', 'O-RQ', 'O-RQ',
                    'O-RQ', 'O-TS', 'O-JD', 'H-TS', 'O-CS', 'O-RQ', 'O-CS', 'O-RQ', 'O-CS', 'O-RQ']
        indices_list = [7, 9, 12, 13, 16, 21, 24, 25, 26, 31, 33, 35]
        self.assertEqual(self.su.get_section(pos_list), indices_list)
    def test_get_section2(self):
        pos_list = ['O-RQ', 'H-TS', 'O-TS', 'O-TS', 'O-TS', 'O-RQ', 'O-TS', 'O-TS', 'O-TS', 'O-TS', 'O-TS', 'O-RQ', 'O-TS',
                    'H-RQ', 'O-ER', 'O-RQ', 'O-RQ', 'O-TS', 'H-TS', 'O-CS', 'O-RQ', 'O-RQ', 'O-TS', 'O-RQ', 'O-RQ', 'O-RQ',
                    'O-RQ', 'H-PQ', 'O-RQ', 'O-TS', 'O-RQ', 'H-CS', 'O-CS', 'O-SP', 'O-TS', 'O-LN', 'O-LN']
        indices_list = [14, 15, 16, 20, 21, 23, 24, 25, 26]
        self.assertEqual(self.su.get_section(pos_list), indices_list)
    def test_get_section3(self):
        crf_list = ['O-CS', 'O-TS', 'O-OL', 'O-OL', 'O-CS', 'O-CS', 'H-TS', 'O-PQ', 'O-RQ', 'O-RQ', 'O-TS', 'O-TS', 'O-TS', 'O-TS',
                    'O-TS', 'O-TS', 'O-TS', 'O-TS', 'H-TS', 'O-TS', 'O-TS', 'O-TS', 'O-TS', 'O-TS', 'O-TS', 'O-TS', 'O-TS', 'O-TS',
                    'O-CS', 'O-TS', 'O-RQ', 'O-PQ', 'O-PQ', 'O-RQ', 'O-ER', 'O-RQ', 'O-TS', 'O-RQ', 'O-RQ', 'O-RQ', 'O-RQ', 'O-CS',
                    'O-CS', 'O-RQ', 'O-RQ', 'O-RQ', 'O-LN', 'H-JD', 'O-CS', 'H-PQ', 'O-RQ', 'O-RQ', 'H-OL', 'O-CS']
        indices_list = [8, 9, 30, 33, 34, 35, 37, 38, 39, 40, 43, 44, 45]
        self.assertEqual(self.su.get_section(crf_list), indices_list)
    def test_get_section4(self):
        crf_list = ['O-CS', 'O-TS', 'O-OL', 'O-OL', 'O-CS', 'O-CS', 'H-TS', 'O-PQ', 'O-RQ', 'O-TS', 'O-RQ', 'O-RQ', 'O-RQ',
                    'O-TS', 'O-TS', 'O-TS', 'O-TS', 'O-TS', 'H-TS', 'O-TS', 'O-TS', 'O-TS', 'O-TS', 'O-TS', 'O-TS', 'O-TS',
                    'O-TS', 'O-TS', 'O-TS', 'O-TS', 'H-RQ', 'O-RQ', 'O-RQ', 'O-RQ', 'O-RQ', 'O-RQ', 'O-RQ', 'O-RQ', 'O-RQ',
                    'O-RQ', 'O-RQ', 'H-RQ', 'H-RQ', 'O-RQ', 'O-RQ', 'O-RQ', 'O-JD', 'H-JD', 'O-CS', 'H-RQ', 'O-RQ', 'O-RQ',
                    'H-OL', 'O-OL']
        pos_symbol = 'RQ'
        neg_symbol = 'PQ'
        nonheader_allows_list = ['O-RQ', 'O-ER']
        indices_list = [31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 43, 44, 45, 50, 51]
        self.assertEqual(self.su.get_section(crf_list, pos_symbol, neg_symbol, nonheader_allows_list), indices_list)
    # def test_get_pos_color_dictionary(self):
        # verbose = False
        # self.assertEqual(self.su.get_pos_color_dictionary(verbose), )
    # def test_append_pos_symbol(self):
        # child_str = ''
        # pos_symbol = ''
        # use_explanation = False
        # self.assertEqual(self.su.append_pos_symbol(child_str, pos_symbol, use_explanation), )
    # def test_find_basic_quals_section_indexes(self):
        # crf_list = None
        # feature_tuple_list = None
        # feature_dict_list = None
        # child_strs_list = None
        # child_tags_list = None
        # file_name = None
        # verbose = False
        # self.assertEqual(self.su.find_basic_quals_section_indexes(crf_list, feature_tuple_list, feature_dict_list, child_strs_list, child_tags_list, file_name, verbose), )
    # def test_visualize_basic_quals_section(self):
        # crf_list = None
        # feature_tuple_list = None
        # feature_dict_list = None
        # child_strs_list = None
        # child_tags_list = None
        # file_name = None
        # verbose = False
        # self.assertEqual(self.su.visualize_basic_quals_section(crf_list, feature_tuple_list, feature_dict_list, child_strs_list, child_tags_list, file_name, verbose), )

if __name__ == '__main__':
    unittest.main()