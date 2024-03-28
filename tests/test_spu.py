#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



# cd C:\Users\daveb\OneDrive\Documents\GitHub\supplemental-hunting\tests
# python -m unittest test_spu.TestSpuMethods.test_update_model

import unittest

class TestSpuMethods(unittest.TestCase):
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
        cu = CypherUtilities(
            uri=uri, user=user, password=password, driver=None, s=s, ha=ha
        )
        
        from is_supplemental_pay_sgd_classifier import IsSupplementalPaySgdClassifier
        self.spu = IsSupplementalPaySgdClassifier(ha=ha, cu=cu, verbose=False)
        
        import warnings
        warnings.filterwarnings('ignore')
    
    def test_make_prediction(self):
        train_data = [
            'This is a supplemental pay', 'This is not a supplemental pay'
        ]
        train_labels = [1, 0]
        self.spu.train_model(train_data, train_labels, verbose=False)

        text1 = 'This is a supplemental pay'
        text2 = 'This is not a supplemental pay'
        text3 = 'Another supplemental pay'
        text4 = 'Not a supplemental pay'
        self.assertEqual(self.spu.make_prediction(text1), [1])
        self.assertEqual(self.spu.make_prediction(text2), [0])
        self.assertEqual(self.spu.make_prediction(text3), [1])
        self.assertEqual(self.spu.make_prediction(text4), [0])

    def test_update_model(self):
        train_data = [
            'This is a supplemental pay', 'This is not a supplemental pay'
        ]
        train_labels = [1, 0]
        self.spu.train_model(train_data, train_labels, verbose=False)

        new_data = [
            'Yet another supplemental pay', 'Definitely not a supplemental pay'
        ]
        new_labels = [1, 0]
        self.spu.update_model(new_data, new_labels, verbose=False)

        text1 = 'This is a supplemental pay'
        text2 = 'This is not a supplemental pay'
        text3 = 'Yet another supplemental pay'
        text4 = 'Definitely not a supplemental pay'
        
        self.assertEqual(self.spu.make_prediction(text1), 1)
        self.assertEqual(self.spu.make_prediction(text2), 0)
        self.assertEqual(self.spu.make_prediction(text3), 1)
        self.assertEqual(self.spu.make_prediction(text4), 0)

    def test_predict_percent_fit(self):
        train_data = [
            'This is a supplemental pay', 'This is not a supplemental pay'
        ]
        train_labels = [1, 0]
        self.spu.train_model(train_data, train_labels, verbose=False)

        new_data = [
            'Yet another supplemental pay', 'Definitely not a supplemental pay'
        ]
        new_labels = [1, 0]
        self.spu.update_model(new_data, new_labels, verbose=False)

        text1 = 'This is a supplemental pay'
        text2 = 'This is not a supplemental pay'
        text3 = 'Yet another supplemental pay'
        text4 = 'Definitely not a supplemental pay'
        
        self.assertAlmostEqual(self.spu.predict_percent_fit(text1), 1, places=0)
        self.assertAlmostEqual(self.spu.predict_percent_fit(text2), 0, places=0)
        self.assertAlmostEqual(self.spu.predict_percent_fit(text3), 1, places=0)
        self.assertAlmostEqual(self.spu.predict_percent_fit(text4), 0, places=0)
    
if __name__ == '__main__':
    unittest.main()