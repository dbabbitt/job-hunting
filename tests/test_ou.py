#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



# cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\tests
# python -m unittest test_ou.TestOuMethods.test_update_model

import unittest

class TestOuMethods(unittest.TestCase):
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
        
        from is_other_sgd_classifier import IsOtherSgdClassifier
        self.ou = IsOtherSgdClassifier(ha=ha, cu=cu, verbose=False)
        
        import warnings
        warnings.filterwarnings('ignore')
    
    def test_make_prediction(self):
        train_data = [
            'This is a other', 'This is not a other'
        ]
        train_labels = [1, 0]
        self.ou.train_model(train_data, train_labels, verbose=False)

        text1 = 'This is a other'
        text2 = 'This is not a other'
        text3 = 'Another other'
        text4 = 'Not a other'
        self.assertEqual(self.ou.make_prediction(text1), [1])
        self.assertEqual(self.ou.make_prediction(text2), [0])
        self.assertEqual(self.ou.make_prediction(text3), [1])
        self.assertEqual(self.ou.make_prediction(text4), [0])

    def test_update_model(self):
        train_data = [
            'This is a other', 'This is not a other'
        ]
        train_labels = [1, 0]
        self.ou.train_model(train_data, train_labels, verbose=False)

        new_data = [
            'Yet another other', 'Definitely not a other'
        ]
        new_labels = [1, 0]
        self.ou.update_model(new_data, new_labels, verbose=False)

        text1 = 'This is a other'
        text2 = 'This is not a other'
        text3 = 'Yet another other'
        text4 = 'Definitely not a other'
        
        self.assertEqual(self.ou.make_prediction(text1), 1)
        self.assertEqual(self.ou.make_prediction(text2), 0)
        self.assertEqual(self.ou.make_prediction(text3), 1)
        self.assertEqual(self.ou.make_prediction(text4), 0)

    def test_predict_percent_fit(self):
        train_data = [
            'This is a other', 'This is not a other'
        ]
        train_labels = [1, 0]
        self.ou.train_model(train_data, train_labels, verbose=False)

        new_data = [
            'Yet another other', 'Definitely not a other'
        ]
        new_labels = [1, 0]
        self.ou.update_model(new_data, new_labels, verbose=False)

        text1 = 'This is a other'
        text2 = 'This is not a other'
        text3 = 'Yet another other'
        text4 = 'Definitely not a other'
        
        self.assertAlmostEqual(self.ou.predict_percent_fit(text1), 1, places=0)
        self.assertAlmostEqual(self.ou.predict_percent_fit(text2), 0, places=0)
        self.assertAlmostEqual(self.ou.predict_percent_fit(text3), 1, places=0)
        self.assertAlmostEqual(self.ou.predict_percent_fit(text4), 0, places=0)
    
if __name__ == '__main__':
    unittest.main()