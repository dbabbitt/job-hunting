#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



# cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\tests
# python -m unittest test_jtu.TestJtuMethods.test_update_model

import unittest

class TestJtuMethods(unittest.TestCase):
    def setUp(self):
        import sys
        import os
        sys.path.insert(1, '../py')
        
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
        
        from is_job_title_sgd_classifier import IsJobTitleSgdClassifier
        self.jtu = IsJobTitleSgdClassifier(ha=ha, cu=cu, verbose=False)
        
        import warnings
        warnings.filterwarnings('ignore')
    
    def test_make_prediction(self):
        train_data = [
            'This is a job title', 'This is not a job title'
        ]
        train_labels = [1, 0]
        self.jtu.train_model(train_data, train_labels, verbose=False)

        text1 = 'This is a job title'
        text2 = 'This is not a job title'
        text3 = 'Another job title'
        text4 = 'Not a job title'
        self.assertEqual(self.jtu.make_prediction(text1), [1])
        self.assertEqual(self.jtu.make_prediction(text2), [0])
        self.assertEqual(self.jtu.make_prediction(text3), [1])
        self.assertEqual(self.jtu.make_prediction(text4), [0])

    def test_update_model(self):
        train_data = [
            'This is a job title', 'This is not a job title'
        ]
        train_labels = [1, 0]
        self.jtu.train_model(train_data, train_labels, verbose=False)

        new_data = [
            'Yet another job title', 'Definitely not a job title'
        ]
        new_labels = [1, 0]
        self.jtu.update_model(new_data, new_labels, verbose=False)

        text1 = 'This is a job title'
        text2 = 'This is not a job title'
        text3 = 'Yet another job title'
        text4 = 'Definitely not a job title'
        
        self.assertEqual(self.jtu.make_prediction(text1), 1)
        self.assertEqual(self.jtu.make_prediction(text2), 0)
        self.assertEqual(self.jtu.make_prediction(text3), 1)
        self.assertEqual(self.jtu.make_prediction(text4), 0)

    def test_predict_percent_fit(self):
        train_data = [
            'This is a job title', 'This is not a job title'
        ]
        train_labels = [1, 0]
        self.jtu.train_model(train_data, train_labels, verbose=False)

        new_data = [
            'Yet another job title', 'Definitely not a job title'
        ]
        new_labels = [1, 0]
        self.jtu.update_model(new_data, new_labels, verbose=False)

        text1 = 'This is a job title'
        text2 = 'This is not a job title'
        text3 = 'Yet another job title'
        text4 = 'Definitely not a job title'
        
        self.assertAlmostEqual(self.jtu.predict_percent_fit(text1), 1, places=0)
        self.assertAlmostEqual(self.jtu.predict_percent_fit(text2), 0, places=0)
        self.assertAlmostEqual(self.jtu.predict_percent_fit(text3), 1, places=0)
        self.assertAlmostEqual(self.jtu.predict_percent_fit(text4), 0, places=0)
    
if __name__ == '__main__':
    unittest.main()