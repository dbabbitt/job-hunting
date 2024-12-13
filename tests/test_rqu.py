#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



# cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\tests
# python -m unittest test_rqu.TestRquMethods.test_update_model

import unittest

class TestRquMethods(unittest.TestCase):
    def setUp(self):
        import sys
        import os
        if (osp.join(os.pardir, 'py') not in sys.path): sys.path.insert(1, osp.join(os.pardir, 'py'))
        
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
        
        from is_minimum_qualification_sgd_classifier import IsRequiredQualificationSgdClassifier
        self.rqu = IsRequiredQualificationSgdClassifier(ha=ha, cu=cu, verbose=False)
        
        import warnings
        warnings.filterwarnings('ignore')
    
    def test_make_prediction(self):
        train_data = [
            'This is a minimum qualification', 'This is not a minimum qualification'
        ]
        train_labels = [1, 0]
        self.rqu.train_model(train_data, train_labels, verbose=False)

        text1 = 'This is a minimum qualification'
        text2 = 'This is not a minimum qualification'
        text3 = 'Another minimum qualification'
        text4 = 'Not a minimum qualification'
        self.assertEqual(self.rqu.make_prediction(text1), [1])
        self.assertEqual(self.rqu.make_prediction(text2), [0])
        self.assertEqual(self.rqu.make_prediction(text3), [1])
        self.assertEqual(self.rqu.make_prediction(text4), [0])

    def test_update_model(self):
        train_data = [
            'This is a minimum qualification', 'This is not a minimum qualification'
        ]
        train_labels = [1, 0]
        self.rqu.train_model(train_data, train_labels, verbose=False)

        new_data = [
            'Yet another minimum qualification', 'Definitely not a minimum qualification'
        ]
        new_labels = [1, 0]
        self.rqu.update_model(new_data, new_labels, verbose=False)

        text1 = 'This is a minimum qualification'
        text2 = 'This is not a minimum qualification'
        text3 = 'Yet another minimum qualification'
        text4 = 'Definitely not a minimum qualification'
        
        self.assertEqual(self.rqu.make_prediction(text1), 1)
        self.assertEqual(self.rqu.make_prediction(text2), 0)
        self.assertEqual(self.rqu.make_prediction(text3), 1)
        self.assertEqual(self.rqu.make_prediction(text4), 0)

    def test_predict_percent_fit(self):
        train_data = [
            'This is a minimum qualification', 'This is not a minimum qualification'
        ]
        train_labels = [1, 0]
        self.rqu.train_model(train_data, train_labels, verbose=False)

        new_data = [
            'Yet another minimum qualification', 'Definitely not a minimum qualification'
        ]
        new_labels = [1, 0]
        self.rqu.update_model(new_data, new_labels, verbose=False)

        text1 = 'This is a minimum qualification'
        text2 = 'This is not a minimum qualification'
        text3 = 'Yet another minimum qualification'
        text4 = 'Definitely not a minimum qualification'
        
        self.assertAlmostEqual(self.rqu.predict_percent_fit(text1), 1, places=0)
        self.assertAlmostEqual(self.rqu.predict_percent_fit(text2), 0, places=0)
        self.assertAlmostEqual(self.rqu.predict_percent_fit(text3), 1, places=0)
        self.assertAlmostEqual(self.rqu.predict_percent_fit(text4), 0, places=0)
    
if __name__ == '__main__':
    unittest.main()