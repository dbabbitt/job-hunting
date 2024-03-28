#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



# cd C:\Users\daveb\OneDrive\Documents\GitHub\posting-hunting\tests
# python -m unittest test_pdu.TestPduMethods.test_update_model

import unittest

class TestPduMethods(unittest.TestCase):
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
        
        from is_posting_date_sgd_classifier import IsPostingDateSgdClassifier
        self.pdu = IsPostingDateSgdClassifier(ha=ha, cu=cu, verbose=False)
        
        import warnings
        warnings.filterwarnings('ignore')
    
    def test_make_prediction(self):
        train_data = [
            'This is a posting date', 'This is not a posting date'
        ]
        train_labels = [1, 0]
        self.pdu.train_model(train_data, train_labels, verbose=False)

        text1 = 'This is a posting date'
        text2 = 'This is not a posting date'
        text3 = 'Another posting date'
        text4 = 'Not a posting date'
        self.assertEqual(self.pdu.make_prediction(text1), [1])
        self.assertEqual(self.pdu.make_prediction(text2), [0])
        self.assertEqual(self.pdu.make_prediction(text3), [1])
        self.assertEqual(self.pdu.make_prediction(text4), [0])

    def test_update_model(self):
        train_data = [
            'This is a posting date', 'This is not a posting date'
        ]
        train_labels = [1, 0]
        self.pdu.train_model(train_data, train_labels, verbose=False)

        new_data = [
            'Yet another posting date', 'Definitely not a posting date'
        ]
        new_labels = [1, 0]
        self.pdu.update_model(new_data, new_labels, verbose=False)

        text1 = 'This is a posting date'
        text2 = 'This is not a posting date'
        text3 = 'Yet another posting date'
        text4 = 'Definitely not a posting date'
        
        self.assertEqual(self.pdu.make_prediction(text1), 1)
        self.assertEqual(self.pdu.make_prediction(text2), 0)
        self.assertEqual(self.pdu.make_prediction(text3), 1)
        self.assertEqual(self.pdu.make_prediction(text4), 0)

    def test_predict_percent_fit(self):
        train_data = [
            'This is a posting date', 'This is not a posting date'
        ]
        train_labels = [1, 0]
        self.pdu.train_model(train_data, train_labels, verbose=False)

        new_data = [
            'Yet another posting date', 'Definitely not a posting date'
        ]
        new_labels = [1, 0]
        self.pdu.update_model(new_data, new_labels, verbose=False)

        text1 = 'This is a posting date'
        text2 = 'This is not a posting date'
        text3 = 'Yet another posting date'
        text4 = 'Definitely not a posting date'
        
        self.assertAlmostEqual(self.pdu.predict_percent_fit(text1), 1, places=0)
        self.assertAlmostEqual(self.pdu.predict_percent_fit(text2), 0, places=0)
        self.assertAlmostEqual(self.pdu.predict_percent_fit(text3), 1, places=0)
        self.assertAlmostEqual(self.pdu.predict_percent_fit(text4), 0, places=0)
    
if __name__ == '__main__':
    unittest.main()