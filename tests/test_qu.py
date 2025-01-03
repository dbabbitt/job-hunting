#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



# cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\tests
# python -m unittest test_qu.TestQuMethods.test_update_model

import unittest

class TestQuMethods(unittest.TestCase):
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
        
        from is_qualification_sgd_classifier import IsQualificationSgdClassifier
        self.qu = IsQualificationSgdClassifier(ha=ha, cu=cu, verbose=False)
        
        import warnings
        warnings.filterwarnings('ignore')
    
    def test_make_prediction(self):
        train_data = ['This is a qualification', 'This is not a qualification']
        train_labels = [1, 0]
        self.qu.train_model(train_data, train_labels, verbose=False)

        text1 = 'This is a qualification'
        text2 = 'This is not a qualification'
        text3 = 'Another qualification'
        text4 = 'Not a qualification'
        self.assertEqual(self.qu.make_prediction(text1), [1])
        self.assertEqual(self.qu.make_prediction(text2), [0])
        self.assertEqual(self.qu.make_prediction(text3), [1])
        self.assertEqual(self.qu.make_prediction(text4), [0])

    def test_update_model(self):
        train_data = ['This is a qualification', 'This is not a qualification']
        train_labels = [1, 0]
        self.qu.train_model(train_data, train_labels, verbose=False)

        new_data = ['Yet another qualification', 'Definitely not a qualification']
        new_labels = [1, 0]
        self.qu.update_model(new_data, new_labels, verbose=False)

        text1 = 'This is a qualification'
        text2 = 'This is not a qualification'
        text3 = 'Yet another qualification'
        text4 = 'Definitely not a qualification'
        
        self.assertEqual(self.qu.make_prediction(text1), 1)
        self.assertEqual(self.qu.make_prediction(text2), 0)
        self.assertEqual(self.qu.make_prediction(text3), 1)
        self.assertEqual(self.qu.make_prediction(text4), 0)

    def test_predict_percent_fit(self):
        train_data = ['This is a qualification', 'This is not a qualification']
        train_labels = [1, 0]
        self.qu.train_model(train_data, train_labels, verbose=False)

        new_data = ['Yet another qualification', 'Definitely not a qualification']
        new_labels = [1, 0]
        self.qu.update_model(new_data, new_labels, verbose=False)

        text1 = 'This is a qualification'
        text2 = 'This is not a qualification'
        text3 = 'Yet another qualification'
        text4 = 'Definitely not a qualification'
        
        self.assertAlmostEqual(self.qu.predict_percent_fit(text1), 1, places=0)
        self.assertAlmostEqual(self.qu.predict_percent_fit(text2), 0, places=0)
        self.assertAlmostEqual(self.qu.predict_percent_fit(text3), 1, places=0)
        self.assertAlmostEqual(self.qu.predict_percent_fit(text4), 0, places=0)
    
if __name__ == '__main__':
    unittest.main()