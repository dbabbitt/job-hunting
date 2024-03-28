
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
        if ('../py' not in sys.path): sys.path.insert(1, '../py')
        
        from storage import Storage
        s = Storage(
            data_folder_path=os.path.abspath('../data'),
            saves_folder_path=os.path.abspath('../saves')
        )
        
        from ha_utils import HeaderAnalysis
        ha = HeaderAnalysis(s=s, verbose=False)
        
        from scrape_utils import WebScrapingUtilities
        wsu = WebScrapingUtilities()
        uri = wsu.secrets_json['neo4j']['connect_url']
        user =  wsu.secrets_json['neo4j']['username']
        password = wsu.secrets_json['neo4j']['password']
        
        from cypher_utils import CypherUtilities
        cu = CypherUtilities(uri=uri, user=user, password=password, driver=None, s=s, ha=ha)
        
        from hc_utils import HeaderCategories
        hc = HeaderCategories(cu=cu, verbose=False)
        
        from lr_utils import LrUtilities
        self.lru = LrUtilities(ha=ha, hc=hc, cu=cu, verbose=False)
        self.lru.build_isqualified_logistic_regression_elements(
            sampling_strategy_limit=None, verbose=True
        )
        
        import warnings
        warnings.filterwarnings('ignore')
    
    def test_build_pos_logistic_regression_elements(self):
        self.assertAlmostEqual(self.slrcu.pos_predict_percent_fit_dict['H-TS']('<b>The Role:</b>'), 1.0)
    
    def test_pos_lr_predict_single(self):
        html_str = '<b>The Role:</b>'
        self.assertEqual(self.slrcu.predict_single(html_str), 'H-TS')
    
    def test_sync_basic_quals_dict(self):
        pass
    
    def test_retrain_isqualified_classifier(self):
        pass
    
    def test_infer_from_hunting_dataframe(self):
        pass
    
    def test_display_hunting_dataframe_as_histogram(self):
        pass
    
if __name__ == '__main__':
    unittest.main()