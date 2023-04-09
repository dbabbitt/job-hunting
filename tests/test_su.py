
#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



# cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\tests
# cls
# python -m unittest test_su.TestSuMethods.test_find_basic_quals_section_indexes

import unittest

class TestSuMethods(unittest.TestCase):
    def setUp(self):
        import sys
        import os
        sys.path.insert(1, '../py')
        
        # Get the Neo4j driver
        from storage import Storage
        s = Storage(
            data_folder_path=os.path.abspath('../data'),
            saves_folder_path=os.path.abspath('../saves')
        )

        from ha_utils import HeaderAnalysis
        ha = HeaderAnalysis(s=s, verbose=False)

        from scrape_utils import WebScrapingUtilities
        wsu = WebScrapingUtilities(
            s=s,
            secrets_json_path=os.path.abspath('../data/secrets/jh_secrets.json')
        )
        uri = wsu.secrets_json['neo4j']['connect_url']
        user =  wsu.secrets_json['neo4j']['username']
        password = wsu.secrets_json['neo4j']['password']

        # Get the Neo4j object
        from cypher_utils import CypherUtilities
        cu = CypherUtilities(
            uri=uri, user=user, password=password, driver=None, s=s, ha=ha
        )

        from is_header_sgd_classifier import IsHeaderSgdClassifier
        ihu = IsHeaderSgdClassifier(ha=ha, cu=cu, verbose=False)

        try:
            version_str = cu.driver.get_server_info().agent
            print(f'======== {version_str} ========')
        except ServiceUnavailable as e:
            print('You need to start Neo4j as a console')
            raise
        except Exception as e:
            print(f'{e.__class__}: {str(e).strip()}')

        from hc_utils import HeaderCategories
        hc = HeaderCategories(cu=cu, verbose=False)

        from lr_utils import LrUtilities
        lru = LrUtilities(ha=ha, cu=cu, hc=hc, verbose=False)

        from section_classifier_utils import SectionLRClassifierUtilities, SectionSGDClassifierUtilities, SectionCRFClassifierUtilities
        slrcu = SectionLRClassifierUtilities(ha=ha, cu=cu, verbose=False)
        ssgdcu = SectionSGDClassifierUtilities(ha=ha, cu=cu, verbose=False)
        ssgdcu.build_pos_stochastic_gradient_descent_elements(sampling_strategy_limit=None, verbose=True)
        scrfcu = SectionCRFClassifierUtilities(cu=cu, ha=ha, verbose=False)
        scrfcu.build_pos_conditional_random_field_elements(verbose=True)

        from crf_utils import CrfUtilities
        crf = CrfUtilities(ha=ha, hc=hc, cu=cu, lru=lru, slrcu=slrcu, scrfcu=scrfcu, ssgdcu=ssgdcu, verbose=True)
        crf.build_pos_conditional_random_field_elements(verbose=True)

        from section_utils import SectionUtilities
        self.su = SectionUtilities(wsu=wsu, ihu=ihu, hc=hc, crf=crf, slrcu=slrcu, scrfcu=scrfcu, ssgdcu=ssgdcu, verbose=False)
        
        import warnings
        warnings.filterwarnings('ignore')
    
    
    def test_find_basic_quals_section_indexes(self):
        crf_list = None
        feature_tuple_list = None
        feature_dict_list = None
        test_child_strs_list = [
            '<b>The Role:</b>',
            "<p>As the Director of Data Science at Brightloom, you'll lead the data science " +
            "team and partner across the organization to help grow our data science capabilities. You'll be " +
            "taking business needs from product and engineering teams and creating a comprehensive data " +
            "science strategy around them. From there, you help prioritize the work for the data science " +
            "team, balancing the work for the team and helping the independent contributors be their best. " +
            "You will heavily engage with the application engineering, data engineering, and data science " +
            "technical leads to ensure that your data science strategies are operationalized effectively.</p>",
            "<p>You're a person who loves helping others work together to do interesting data science. You " +
            "can evangelize a data science idea to non-technical people, and you can deal with the " +
            "realities of a complex business and figure out how to have data science contribute in a " +
            "positive way. You enjoy leading data scientists so they can do strong work, and helping to " +
            "elevate the data scientist's concerns when they raise them.</p>",
            "<b>What you'll do:</b>",
            "<li>Lead the data science team as their manager - helping devise projects, removing blockers, " +
            "and engaging with independent contributors. You'll be hiring more data scientists and " +
            "eventually hire managers to do this part of the job for you.</li>",
            '<li>Represent the data science discipline throughout the organization. You will have a ' +
            'powerful voice in the company and represent data scientists across different parts of the ' +
            'business.</li>',
            '<li>Partner across Brightloom engineering groups; evangelizing our culture of using data to ' +
            'measure, understand, and improve our product and features.</li>',
            '<li>Be a strong leader - you will give team members clear feedback that helps them grow ' +
            'and inspires thought leadership. You will lead by example, have compassion for everyone in ' +
            'the company and their challenges, and will take controversial directions when necessary.</li>',
            '<li>Be an expert in interpreting data and understanding its conclusions - your team will ' +
            'be creating lots of powerful insights and you will be finding the valuable implications of ' +
            'that data.</li>',
            '<li>Own the data science technical roadmap - take the business priorities from the product ' +
            'team and turn them into a set of projects the data science team will focus on delivering.</li>',
            "<li>Be involved in new product development - as the product team thinks of new ways to take " +
            "customer feedback and create a better product, you'll be heavily involved with assessing " +
            "what is feasible from a data science perspective.</li>",
            '<b>About you:</b>',
            '<li>Demonstrated experience building and developing a team</li>',
            '<li>Demonstrated experience putting a data science product into market, ideally in a startup</li>',
            '<li>Experience in the marketing, retail, or restaurant domain</li>',
            '<li>Foundational understanding of the data science ecosystem</li>',
            '<b>About Us</b>',
            '<p>At Brightloom (formerly eatsa), we are working to revolutionize restaurants through ' +
            'innovative technology and design. We are disrupting an industry worth $900 billion globally ' +
            'with partnerships in North America, Asia, and soon other continents.</p>',
            '<p>Led by our CEO, industry veteran and former Starbucks and J.Crew executive Adam Brotman, our ' +
            'unique, world-class team combines software and hardware engineers, designers, and industry ' +
            'experts to push the boundaries on re-engineering every aspect of the restaurant experience.</p>',
            "<p>We believe any restaurant brand should be able to engage customers digitally using a " +
            "seamless combination of mobile, omni-channel ordering and loyalty offerings. Up until now, " +
            "only a select few brands could afford, or knew how to put together a top-notch digital " +
            "engagement and ordering platform. With key Starbucks technology components integrated into " +
            "our platform, Brightloom will now allow any restaurant brand to create their own version of a " +
            "world-class digital flywheel ecosystem. Brightloom's configurable technology suite combines " +
            "convenience (digital ordering channels), personal connection (personalized marketing) and " +
            "engagement (loyalty) for restaurant brands in today's new digital era.</p>",
            '<b>What We Offer</b>',
            '<li>Fun, creative and collaborative remote work environment</li>',
            '<li>Competitive pay and equity/stock options</li>',
            '<li>Health, Dental &amp; Vision Insurance Coverage</li>',
            '<li>Life Insurance, Short-Term Disability, Long-Term Disability</li>',
            '<li>Phone/Internet Reimbursement</li>',
            '<li>Home Office Refresh Reimbursement</li>',
            '<li>Employee Assistance Program</li>',
            '<li>Flexible Spending Account &amp; Health Savings Account</li>',
            '<li>Flexible Time Off</li>',
            '<li>401(k)</li>',
            '<p>Brightloom is an Equal Employment Opportunity Employer. All qualified applicants will ' +
            'receive consideration for employment without regard to race, color, religion, sex, national ' +
            'origin, sexual orientation, gender identity, disability and protected veterans status or any ' +
            'other characteristic protected by law.</p>'
        ]
        child_tags_list = None
        file_name = None
        verbose = False
        indices_list = self.su.find_basic_quals_section_indexes(
            crf_list=None, feature_tuple_list=None,
            feature_dict_list=None,
            child_strs_list=test_child_strs_list,
            child_tags_list=None, file_name=None,
            verbose=True
        )
        self.assertEqual(
            indices_list, list(range(30, 44))
        )
    def test_get_section1(self):
        pos_list = [
            'O-CS', 'O-IP', 'O-CS', 'O-TS', 'H-RQ',
            'O-TS', 'O-TS', 'O-RQ', 'O-TS', 'O-RQ',
            'O-TS', 'O-TS', 'O-RQ', 'O-RQ', 'H-RQ',
            'O-PQ', 'O-RQ', 'O-TS', 'O-TS', 'O-TS',
            'O-PQ', 'O-RQ', 'O-TS', 'O-TS', 'O-RQ',
            'O-RQ', 'O-RQ', 'O-TS', 'O-JD', 'H-TS',
            'O-CS', 'O-RQ', 'O-CS', 'O-RQ', 'O-CS',
            'O-RQ'
        ]
        indices_list = [
            7, 9, 12, 13, 16, 21, 24, 25, 26, 31,
            33, 35
        ]
        self.assertEqual(
            self.su.get_section(pos_list),
            indices_list
        )
    def test_get_section2(self):
        pos_list = ['O-RQ', 'H-TS', 'O-TS', 'O-TS', 'O-TS', 'O-RQ', 'O-TS', 'O-TS', 'O-TS', 'O-TS', 'O-TS', 'O-RQ', 'O-TS',
                    'H-RQ', 'O-ER', 'O-RQ', 'O-RQ', 'O-TS', 'H-TS', 'O-CS', 'O-RQ', 'O-RQ', 'O-TS', 'O-RQ', 'O-RQ', 'O-RQ',
                    'O-RQ', 'H-PQ', 'O-RQ', 'O-TS', 'O-RQ', 'H-CS', 'O-CS', 'O-SP', 'O-TS', 'O-LN', 'O-LN']
        indices_list = [14, 15, 16, 20, 21, 23, 24, 25, 26]
        self.assertEqual(self.su.get_section(pos_list), indices_list)
    def test_get_section3(self):
        crf_list = ['O-CS', 'O-TS', 'O-OL', 'O-OL', 'O-CS', 'O-CS', 'H-TS', 'O-PQ', 'O-RQ', 'O-RQ', 'O-TS', 'O-TS', 'O-TS', 'O-TS',
                    'O-TS', 'O-TS', 'O-TS', 'O-TS', 'H-TS', 'O-TS', 'O-TS', 'O-TS', 'O-TS', 'O-TS', 'O-TS', 'O-TS', 'O-TS', 'O-TS',
                    'O-CS', 'O-TS', 'O-RQ', 'O-PQ', 'O-PQ', 'O-RQ', 'O-ER', 'O-RQ', 'O-TS', 'O-RQ', 'O-RQ', 'O-RQ', 'O-RQ', 'O-CS',
                    'O-CS', 'O-RQ', 'O-RQ', 'O-RQ', 'O-LN', 'H-JD', 'O-CS', 'H-PQ', 'O-RQ', 'O-RQ', 'H-OL', 'O-CS']
        indices_list = [8, 9, 30, 33, 34, 35, 37, 38, 39, 40, 43, 44, 45]
        self.assertEqual(self.su.get_section(crf_list), indices_list)
    def test_get_section4(self):
        crf_list = ['O-CS', 'O-TS', 'O-OL', 'O-OL', 'O-CS', 'O-CS', 'H-TS', 'O-PQ', 'O-RQ', 'O-TS', 'O-RQ', 'O-RQ', 'O-RQ',
                    'O-TS', 'O-TS', 'O-TS', 'O-TS', 'O-TS', 'H-TS', 'O-TS', 'O-TS', 'O-TS', 'O-TS', 'O-TS', 'O-TS', 'O-TS',
                    'O-TS', 'O-TS', 'O-TS', 'O-TS', 'H-RQ', 'O-RQ', 'O-RQ', 'O-RQ', 'O-RQ', 'O-RQ', 'O-RQ', 'O-RQ', 'O-RQ',
                    'O-RQ', 'O-RQ', 'H-RQ', 'H-RQ', 'O-RQ', 'O-RQ', 'O-RQ', 'O-JD', 'H-JD', 'O-CS', 'H-RQ', 'O-RQ', 'O-RQ',
                    'H-OL', 'O-OL']
        pos_symbol = 'RQ'
        neg_symbol = 'PQ'
        nonheader_allows_list = ['O-RQ', 'O-ER']
        indices_list = [31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 43, 44, 45, 50, 51]
        self.assertEqual(self.su.get_section(crf_list, pos_symbol, neg_symbol, nonheader_allows_list), indices_list)
    # def test_get_pos_color_dictionary(self):
        # verbose = False
        # self.assertEqual(self.su.get_pos_color_dictionary(verbose), )
    # def test_append_pos_symbol(self):
        # child_str = ''
        # pos_symbol = ''
        # use_explanation = False
        # self.assertEqual(self.su.append_pos_symbol(child_str, pos_symbol, use_explanation), )
    # def test_visualize_basic_quals_section(self):
        # crf_list = None
        # feature_tuple_list = None
        # feature_dict_list = None
        # child_strs_list = None
        # child_tags_list = None
        # file_name = None
        # verbose = False
        # self.assertEqual(self.su.visualize_basic_quals_section(crf_list, feature_tuple_list, feature_dict_list, child_strs_list, child_tags_list, file_name, verbose), )

if __name__ == '__main__':
    unittest.main()