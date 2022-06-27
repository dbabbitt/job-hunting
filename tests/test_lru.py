
#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



# cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\tests
# python -m unittest test_lru.TestLruMethods.test_build_pos_logistic_regression_elements

import unittest

class TestLruMethods(unittest.TestCase):
    def setUp(self):
        import sys
        import os
        sys.path.insert(1, '../py')
        
        from ha_utils import HeaderAnalysis
        self.ha = HeaderAnalysis(verbose=False)
        
        from scrape_utils import WebScrapingUtilities
        wsu = WebScrapingUtilities()
        uri = wsu.secrets_json['neo4j']['connect_url']
        user =  wsu.secrets_json['neo4j']['username']
        password = wsu.secrets_json['neo4j']['password']
        
        from storage import Storage
        self.s = Storage()
        
        from cypher_utils import CypherUtilities
        self.cu = CypherUtilities(uri=uri, user=user, password=password, driver=None, s=self.s, ha=self.ha)
        
        from hc_utils import HeaderCategories
        self.hc = HeaderCategories(cu=self.cu, verbose=False)
        
        from lr_utils import LrUtilities
        self.lru = LrUtilities(ha=self.ha, hc=self.hc, cu=self.cu, verbose=False)
        self.lru.build_pos_logistic_regression_elements()
        
        import warnings
        warnings.filterwarnings('ignore')
    
    def test_build_pos_logistic_regression_elements(self):
        self.assertAlmostEqual(self.lru.POS_PREDICT_PERCENT_FIT_DICT['H-TS']('<b>The Role:</b>'), 1.0)
    
    def test_build_isheader_logistic_regression_elements(self):
        self.lru.build_isheader_logistic_regression_elements()
        self.assertAlmostEqual(self.lru.ISHEADER_PREDICT_PERCENT_FIT('<b>The Role:</b>'), 0.9999999998502525)
    
    def test_isheader_lr_predict_percent(self):
        navigable_parent = '<i>Identify problems and proactively seek solutions with urgency</i>'
        self.assertAlmostEqual(self.lru.ISHEADER_PREDICT_PERCENT_FIT(navigable_parent), 0.08396069036423434)
    
    def test_pos_lr_predict_single(self):
        html_str = '<b>The Role:</b>'
        self.assertEqual(self.lru.pos_lr_predict_single(html_str), 'H-TS')
    
if __name__ == '__main__':
    unittest.main()