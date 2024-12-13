#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



# cd C:\Users\daveb\OneDrive\Documents\GitHub\interview-hunting\tests
# python -m unittest test_ipu.TestIpuMethods.test_update_model

import unittest

class TestIpuMethods(unittest.TestCase):
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
        
        from is_interview_procedure_sgd_classifier import IsInterviewProcedureSgdClassifier
        self.ipu = IsInterviewProcedureSgdClassifier(ha=ha, cu=cu, verbose=False)
        
        import warnings
        warnings.filterwarnings('ignore')
    
    def test_make_prediction(self):
        train_data = [
            'This is a interview procedure', 'This is not a interview procedure'
        ]
        train_labels = [1, 0]
        self.ipu.train_model(train_data, train_labels, verbose=False)

        text1 = 'This is a interview procedure'
        text2 = 'This is not a interview procedure'
        text3 = 'Another interview procedure'
        text4 = 'Not a interview procedure'
        self.assertEqual(self.ipu.make_prediction(text1), [1])
        self.assertEqual(self.ipu.make_prediction(text2), [0])
        self.assertEqual(self.ipu.make_prediction(text3), [1])
        self.assertEqual(self.ipu.make_prediction(text4), [0])

    def test_update_model(self):
        train_data = [
            'This is a interview procedure', 'This is not a interview procedure'
        ]
        train_labels = [1, 0]
        self.ipu.train_model(train_data, train_labels, verbose=False)

        new_data = [
            'Yet another interview procedure', 'Definitely not a interview procedure'
        ]
        new_labels = [1, 0]
        self.ipu.update_model(new_data, new_labels, verbose=False)

        text1 = 'This is a interview procedure'
        text2 = 'This is not a interview procedure'
        text3 = 'Yet another interview procedure'
        text4 = 'Definitely not a interview procedure'
        
        self.assertEqual(self.ipu.make_prediction(text1), 1)
        self.assertEqual(self.ipu.make_prediction(text2), 0)
        self.assertEqual(self.ipu.make_prediction(text3), 1)
        self.assertEqual(self.ipu.make_prediction(text4), 0)

    def test_predict_percent_fit(self):
        train_data = [
            'This is a interview procedure', 'This is not a interview procedure'
        ]
        train_labels = [1, 0]
        self.ipu.train_model(train_data, train_labels, verbose=False)

        new_data = [
            'Yet another interview procedure', 'Definitely not a interview procedure'
        ]
        new_labels = [1, 0]
        self.ipu.update_model(new_data, new_labels, verbose=False)

        text1 = 'This is a interview procedure'
        text2 = 'This is not a interview procedure'
        text3 = 'Yet another interview procedure'
        text4 = 'Definitely not a interview procedure'
        
        self.assertAlmostEqual(self.ipu.predict_percent_fit(text1), 1, places=0)
        self.assertAlmostEqual(self.ipu.predict_percent_fit(text2), 0, places=0)
        self.assertAlmostEqual(self.ipu.predict_percent_fit(text3), 1, places=0)
        self.assertAlmostEqual(self.ipu.predict_percent_fit(text4), 0, places=0)
    
if __name__ == '__main__':
    unittest.main()