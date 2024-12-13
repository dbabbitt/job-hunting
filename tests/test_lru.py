
#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria


# cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\tests
# python -m unittest test_lru.TestLruMethods.test_sync_basic_quals_dict

import unittest

class TestLruMethods(unittest.TestCase):
    def setUp(self):
        import sys
        import os
        if (osp.join(os.pardir, 'py') not in sys.path): sys.path.insert(1, osp.join(os.pardir, 'py'))
        
        from storage import Storage
        self.s = Storage(
            data_folder_path=os.path.abspath('../data'),
            saves_folder_path=os.path.abspath('../saves')
        )
        
        from ha_utils import HeaderAnalysis
        ha = HeaderAnalysis(s=self.s, verbose=False)
        
        from scrape_utils import WebScrapingUtilities
        wsu = WebScrapingUtilities()
        uri = wsu.secrets_json['neo4j']['connect_url']
        user =  wsu.secrets_json['neo4j']['username']
        password = wsu.secrets_json['neo4j']['password']
        
        from cypher_utils import CypherUtilities
        self.cu = CypherUtilities(
            uri=uri, user=user, password=password, driver=None, s=self.s, ha=ha
        )
        
        from hc_utils import HeaderCategories
        hc = HeaderCategories(cu=self.cu, verbose=False)
        
        from lr_utils import LrUtilities
        self.lru = LrUtilities(ha=ha, hc=hc, cu=self.cu, verbose=False)
        
        import warnings
        warnings.filterwarnings('ignore')
    
    # def test_build_isqualified_logistic_regression_elements(self):
        # self.lru.build_isqualified_logistic_regression_elements(
            # sampling_strategy_limit=None, verbose=True
        # )
        # pass
    
    def test_sync_basic_quals_dict(self):
        qualification_str = "<li>Must have a bachelor’s degree or above in a related field (Masters or PhD preferred).</li>"
        
        # Remove this particular child string from the quals dictionary
        basic_quals_dict = self.s.load_object('basic_quals_dict')
        basic_quals_dict.pop(qualification_str, None)
        self.s.store_objects(basic_quals_dict=basic_quals_dict)
        
        # Assert that this particular child string is not in the quals dictionary
        basic_quals_dict = self.s.load_object('basic_quals_dict')
        self.assertFalse(
            qualification_str in basic_quals_dict,
            msg=f'"{qualification_str}" should not be in basic_quals_dict'
        )
        
        # Remove this particular child string from the database
        def do_cypher_tx(tx, qualification_str, verbose=False):
            cypher_str = '''
                MATCH (qs:QualificationStrings {qualification_str: $qualification_str})
                DETACH DELETE qs;
                '''
            results_list = tx.run(query=cypher_str, parameters={'qualification_str': qualification_str})

            return [dict(record.items()) for record in results_list]
        with self.cu.driver.session() as session:
            row_objs_list = session.write_transaction(do_cypher_tx, qualification_str=qualification_str, verbose=False)
        
        # Assert this particular child string is not in the database
        def do_cypher_tx(tx, qualification_str, verbose=False):
            cypher_str = '''
                MATCH (qs:QualificationStrings {qualification_str: $qualification_str})
                RETURN qs;
                '''
            results_list = tx.run(query=cypher_str, parameters={'qualification_str': qualification_str})

            return [dict(record.items()) for record in results_list]
        with self.cu.driver.session() as session:
            row_objs_list = session.write_transaction(do_cypher_tx, qualification_str=qualification_str, verbose=False)
        self.assertEquals(
            len(row_objs_list), 0,
            msg=f"There should be no MATCH for {qualification_str} in qs:QualificationStrings)"
        )
        
        # Manually label the unscored qual
        basic_quals_dict = self.s.load_object('basic_quals_dict')
        basic_quals_dict[qualification_str] = 1
        self.s.store_objects(basic_quals_dict=basic_quals_dict)
        
        # Sync the database with the dictionary
        self.lru.sync_basic_quals_dict(sampling_strategy_limit=None, verbose=False)
        
        # Assert that this particular child string is still in the quals dictionary
        basic_quals_dict = self.s.load_object('basic_quals_dict')
        self.assertTrue(
            qualification_str in basic_quals_dict,
            msg=f'"{qualification_str}" should still be in basic_quals_dict'
        )
        
        # Assert this particular child string is back in the database
        def do_cypher_tx(tx, qualification_str, verbose=False):
            cypher_str = '''
                MATCH (qs:QualificationStrings {qualification_str: $qualification_str})
                RETURN qs;
                '''
            results_list = tx.run(query=cypher_str, parameters={'qualification_str': qualification_str})

            return [dict(record.items()) for record in results_list]
        with self.cu.driver.session() as session:
            row_objs_list = session.write_transaction(do_cypher_tx, qualification_str=qualification_str, verbose=False)
        self.assertEquals(len(row_objs_list), 1, msg=f"There should be one MATCH for {qualification_str} in qs:QualificationStrings)")
    
    # def test_retrain_isqualified_classifier(self):
        # self.lru.build_isqualified_logistic_regression_elements(
            # sampling_strategy_limit=None, verbose=True
        # )
        # pass
    
    # def test_infer_from_hunting_dataframe(self):
        # self.lru.build_isqualified_logistic_regression_elements(
            # sampling_strategy_limit=None, verbose=True
        # )
        # pass
    
    # def test_display_hunting_dataframe_as_histogram(self):
        # self.lru.build_isqualified_logistic_regression_elements(
            # sampling_strategy_limit=None, verbose=True
        # )
        # pass
    
if __name__ == '__main__':
    unittest.main()
# ['self.assertAlmostEqual', 'self.assertAlmostEquals', 'self.assertCountEqual', 'self.assertDictContainsSubset', 'self.assertDictEqual', 'self.assertEqual', 'self.assertEquals', 'self.assertFalse', 'self.assertGreater', 'self.assertGreaterEqual', 'self.assertIn', 'self.assertIs', 'self.assertIsInstance', 'self.assertIsNone', 'self.assertIsNot', 'self.assertIsNotNone', 'self.assertLess', 'self.assertLessEqual', 'self.assertListEqual', 'self.assertLogs', 'self.assertMultiLineEqual', 'self.assertNoLogs', 'self.assertNotAlmostEqual', 'self.assertNotAlmostEquals', 'self.assertNotEqual', 'self.assertNotEquals', 'self.assertNotIn', 'self.assertNotIsInstance', 'self.assertNotRegex', 'self.assertNotRegexpMatches', 'self.assertRaises', 'self.assertRaisesRegex', 'self.assertRaisesRegexp', 'self.assertRegex', 'self.assertRegexpMatches', 'self.assertSequenceEqual', 'self.assertSetEqual', 'self.assertTrue', 'self.assertTupleEqual', 'self.assertWarns', 'self.assertWarnsRegex', 'self.assert_']