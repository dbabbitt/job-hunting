
#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



# cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\tests
# python -m unittest test_hc.TestHcMethods.test_get_feature_tuple3

import unittest

class TestHcMethods(unittest.TestCase):
    def setUp(self):
        import sys
        import os
        if ('../py' not in sys.path): sys.path.insert(1, '../py')
        
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
        self.hc = HeaderCategories(cu=cu, verbose=False)

        from section_classifier_utils import SectionLRClassifierUtilities, SectionSGDClassifierUtilities, SectionCRFClassifierUtilities
        self.slrcu = SectionLRClassifierUtilities(ha=ha, cu=cu, verbose=False)
        self.slrcu.build_pos_logistic_regression_elements(
            sampling_strategy_limit=None, verbose=True
        )
        self.ssgdcu = SectionSGDClassifierUtilities(ha=ha, cu=cu, verbose=False)
        self.ssgdcu.build_pos_stochastic_gradient_descent_elements(
            sampling_strategy_limit=None, verbose=True
        )
        self.scrfcu = SectionCRFClassifierUtilities(cu=cu, ha=ha, verbose=False)
        self.scrfcu.build_pos_conditional_random_field_elements(verbose=True)
        
        import warnings
        warnings.filterwarnings('ignore')
        
        self.test_child_strs_list = ['<b>The Role:</b>', "<p>As the Director of Data Science at Brightloom, you'll lead the data science team and " + "partner across the organization to help grow our data science capabilities. You'll be " + "taking business needs from product and engineering teams and creating a comprehensive data " + "science strategy around them. From there, you help prioritize the work for the data science " + "team, balancing the work for the team and helping the independent contributors be their best. " + "You will heavily engage with the application engineering, data engineering, and data science " + "technical leads to ensure that your data science strategies are operationalized effectively.</p>", "<p>You're a person who loves helping others work together to do interesting data science. You " + "can evangelize a data science idea to non-technical people, and you can deal with the " + "realities of a complex business and figure out how to have data science contribute in a " + "positive way. You enjoy leading data scientists so they can do strong work, and helping to " + "elevate the data scientist's concerns when they raise them.</p>", "<b>What you'll do:</b>", "<li>Lead the data science team as their manager - helping devise projects, removing blockers, " + "and engaging with independent contributors. You'll be hiring more data scientists and " + "eventually hire managers to do this part of the job for you.</li>", '<li>Represent the data science discipline throughout the organization. You will have a ' + 'powerful voice in the company and represent data scientists across different parts of the ' + 'business.</li>', '<li>Partner across Brightloom engineering groups; evangelizing our culture of using data to ' + 'measure, understand, and improve our product and features.</li>', '<li>Be a strong leader - you will give team members clear feedback that helps them grow ' + 'and inspires thought leadership. You will lead by example, have compassion for everyone in ' + 'the company and their challenges, and will take controversial directions when necessary.</li>', '<li>Be an expert in interpreting data and understanding its conclusions - your team will ' + 'be creating lots of powerful insights and you will be finding the valuable implications of ' + 'that data.</li>', '<li>Own the data science technical roadmap - take the business priorities from the product ' + 'team and turn them into a set of projects the data science team will focus on delivering.</li>', "<li>Be involved in new product development - as the product team thinks of new ways to take " + "customer feedback and create a better product, you'll be heavily involved with assessing " + "what is feasible from a data science perspective.</li>", '<b>About you:</b>', '<li>Demonstrated experience building and developing a team</li>', '<li>Demonstrated experience putting a data science product into market, ideally in a startup</li>', '<li>Experience in the marketing, retail, or restaurant domain</li>', '<li>Foundational understanding of the data science ecosystem</li>', '<b>About Us</b>', '<p>At Brightloom (formerly eatsa), we are working to revolutionize restaurants through ' + 'innovative technology and design. We are disrupting an industry worth $900 billion globally ' + 'with partnerships in North America, Asia, and soon other continents.</p>', '<p>Led by our CEO, industry veteran and former Starbucks and J.Crew executive Adam Brotman, our ' + 'unique, world-class team combines software and hardware engineers, designers, and industry ' + 'experts to push the boundaries on re-engineering every aspect of the restaurant experience.</p>', "<p>We believe any restaurant brand should be able to engage customers digitally using a " + "seamless combination of mobile, omni-channel ordering and loyalty offerings. Up until now, " + "only a select few brands could afford, or knew how to put together a top-notch digital " + "engagement and ordering platform. With key Starbucks technology components integrated into " + "our platform, Brightloom will now allow any restaurant brand to create their own version of a " + "world-class digital flywheel ecosystem. Brightloom's configurable technology suite combines " + "convenience (digital ordering channels), personal connection (personalized marketing) and " + "engagement (loyalty) for restaurant brands in today's new digital era.</p>", '<b>What We Offer</b>', '<li>Fun, creative and collaborative remote work environment</li>', '<li>Competitive pay and equity/stock options</li>', '<li>Health, Dental &amp; Vision Insurance Coverage</li>', '<li>Life Insurance, Short-Term Disability, Long-Term Disability</li>', '<li>Phone/Internet Reimbursement</li>', '<li>Home Office Refresh Reimbursement</li>', '<li>Employee Assistance Program</li>', '<li>Flexible Spending Account &amp; Health Savings Account</li>', '<li>Flexible Time Off</li>', '<li>401(k)</li>', '<p>Brightloom is an Equal Employment Opportunity Employer. All qualified applicants will ' + 'receive consideration for employment without regard to race, color, religion, sex, national ' + 'origin, sexual orientation, gender identity, disability and protected veterans status or any ' + 'other characteristic protected by law.</p>']
        self.test_child_str = self.test_child_strs_list[-1]
    
    def test_get_feature_tuple_slrcu_obj_scrfcu_obj_ssgdcu_obj(self):
        feature_dict = {
            'initial_tag': 'p', 'is_header': False,
            'child_str': self.test_child_str,
            'is_task_scope': None, 'is_minimum_qualification': None,
            'is_preferred_qualification': None, 'is_legal_notification': None,
            'is_job_title': None, 'is_office_location': None, 'is_job_duration': None,
            'is_supplemental_pay': None, 'is_educational_requirement': None,
            'is_interview_procedure': None, 'is_corporate_scope': None,
            'is_posting_date': None, 'is_other': None
        }
        feature_tuple = self.hc.get_feature_tuple(
            feature_dict, pos_lr_predict_single=self.slrcu.predict_single,
            pos_crf_predict_single=self.scrfcu.predict_single,
            pos_sgd_predict_single=self.ssgdcu.predict_single
        )
        self.assertEqual(
            feature_tuple,
            ('p', self.test_child_str, 'O-LN')
        )
    
    def test_get_feature_tuple_slrcu_obj_scrfcu_obj_ssgdcu_none(self):
        feature_dict = {
            'initial_tag': 'p', 'is_header': False,
            'child_str': self.test_child_str,
            'is_task_scope': None, 'is_minimum_qualification': None,
            'is_preferred_qualification': None, 'is_legal_notification': None,
            'is_job_title': None, 'is_office_location': None, 'is_job_duration': None,
            'is_supplemental_pay': None, 'is_educational_requirement': None,
            'is_interview_procedure': None, 'is_corporate_scope': None,
            'is_posting_date': None, 'is_other': None
        }
        feature_tuple = self.hc.get_feature_tuple(
            feature_dict, pos_lr_predict_single=self.slrcu.predict_single,
            pos_crf_predict_single=self.scrfcu.predict_single,
            pos_sgd_predict_single=None
        )
        self.assertEqual(
            feature_tuple,
            ('p', self.test_child_str, 'O-LN')
        )

    
    def test_get_feature_tuple_slrcu_obj_scrfcu_none_ssgdcu_obj(self):
        feature_dict = {
            'initial_tag': 'p', 'is_header': False,
            'child_str': self.test_child_str,
            'is_task_scope': None, 'is_minimum_qualification': None,
            'is_preferred_qualification': None, 'is_legal_notification': None,
            'is_job_title': None, 'is_office_location': None, 'is_job_duration': None,
            'is_supplemental_pay': None, 'is_educational_requirement': None,
            'is_interview_procedure': None, 'is_corporate_scope': None,
            'is_posting_date': None, 'is_other': None
        }
        feature_tuple = self.hc.get_feature_tuple(
            feature_dict, pos_lr_predict_single=self.slrcu.predict_single,
            pos_crf_predict_single=None,
            pos_sgd_predict_single=self.ssgdcu.predict_single
        )
        self.assertEqual(
            feature_tuple,
            ('p', self.test_child_str, 'O-LN')
        )

    
    def test_get_feature_tuple_slrcu_obj_scrfcu_none_ssgdcu_none(self):
        feature_dict = {
            'initial_tag': 'p', 'is_header': False,
            'child_str': self.test_child_str,
            'is_task_scope': None, 'is_minimum_qualification': None,
            'is_preferred_qualification': None, 'is_legal_notification': None,
            'is_job_title': None, 'is_office_location': None, 'is_job_duration': None,
            'is_supplemental_pay': None, 'is_educational_requirement': None,
            'is_interview_procedure': None, 'is_corporate_scope': None,
            'is_posting_date': None, 'is_other': None
        }
        feature_tuple = self.hc.get_feature_tuple(
            feature_dict, pos_lr_predict_single=self.slrcu.predict_single,
            pos_crf_predict_single=None,
            pos_sgd_predict_single=None
        )
        self.assertEqual(
            feature_tuple,
            ('p', self.test_child_str, 'O-LN')
        )

    
    def test_get_feature_tuple_slrcu_none_scrfcu_obj_ssgdcu_obj(self):
        feature_dict = {
            'initial_tag': 'p', 'is_header': False,
            'child_str': self.test_child_str,
            'is_task_scope': None, 'is_minimum_qualification': None,
            'is_preferred_qualification': None, 'is_legal_notification': None,
            'is_job_title': None, 'is_office_location': None, 'is_job_duration': None,
            'is_supplemental_pay': None, 'is_educational_requirement': None,
            'is_interview_procedure': None, 'is_corporate_scope': None,
            'is_posting_date': None, 'is_other': None
        }
        feature_tuple = self.hc.get_feature_tuple(
            feature_dict, pos_lr_predict_single=None,
            pos_crf_predict_single=self.scrfcu.predict_single,
            pos_sgd_predict_single=self.ssgdcu.predict_single
        )
        self.assertEqual(
            feature_tuple,
            ('p', self.test_child_str, 'O-LN')
        )

    
    def test_get_feature_tuple_slrcu_none_scrfcu_obj_ssgdcu_none(self):
        feature_dict = {
            'initial_tag': 'p', 'is_header': False,
            'child_str': self.test_child_str,
            'is_task_scope': None, 'is_minimum_qualification': None,
            'is_preferred_qualification': None, 'is_legal_notification': None,
            'is_job_title': None, 'is_office_location': None, 'is_job_duration': None,
            'is_supplemental_pay': None, 'is_educational_requirement': None,
            'is_interview_procedure': None, 'is_corporate_scope': None,
            'is_posting_date': None, 'is_other': None
        }
        feature_tuple = self.hc.get_feature_tuple(
            feature_dict, pos_lr_predict_single=None,
            pos_crf_predict_single=self.scrfcu.predict_single,
            pos_sgd_predict_single=None
        )
        self.assertEqual(
            feature_tuple,
            ('p', self.test_child_str, 'O-LN')
        )

    
    def test_get_feature_tuple_slrcu_none_scrfcu_none_ssgdcu_obj(self):
        feature_dict = {
            'initial_tag': 'p', 'is_header': False,
            'child_str': self.test_child_str,
            'is_task_scope': None, 'is_minimum_qualification': None,
            'is_preferred_qualification': None, 'is_legal_notification': None,
            'is_job_title': None, 'is_office_location': None, 'is_job_duration': None,
            'is_supplemental_pay': None, 'is_educational_requirement': None,
            'is_interview_procedure': None, 'is_corporate_scope': None,
            'is_posting_date': None, 'is_other': None
        }
        feature_tuple = self.hc.get_feature_tuple(
            feature_dict, pos_lr_predict_single=None,
            pos_crf_predict_single=None,
            pos_sgd_predict_single=self.ssgdcu.predict_single
        )
        self.assertEqual(
            feature_tuple,
            ('p', self.test_child_str, 'O-LN')
        )

    
    def test_get_feature_tuple_slrcu_none_scrfcu_none_ssgdcu_none(self):
        feature_dict = {
            'initial_tag': 'p', 'is_header': False,
            'child_str': self.test_child_str,
            'is_task_scope': None, 'is_minimum_qualification': None,
            'is_preferred_qualification': None, 'is_legal_notification': None,
            'is_job_title': None, 'is_office_location': None, 'is_job_duration': None,
            'is_supplemental_pay': None, 'is_educational_requirement': None,
            'is_interview_procedure': None, 'is_corporate_scope': None,
            'is_posting_date': None, 'is_other': None
        }
        feature_tuple = self.hc.get_feature_tuple(
            feature_dict, pos_lr_predict_single=None,
            pos_crf_predict_single=None,
            pos_sgd_predict_single=None
        )
        self.assertEqual(
            feature_tuple,
            ('p', self.test_child_str, 'O-LN')
        )
    
    def test_append_parts_of_speech_list(self):
        test_pos_list = []
        for navigable_parent in self.test_child_strs_list:
            test_pos_list = self.hc.append_parts_of_speech_list(navigable_parent, test_pos_list)
        self.assertEqual(test_pos_list, ['H-TS', 'O', 'O', 'H-TS', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'H-RQ', 'O', 'O', 'O', 'O',
                                         'H-CS', 'O', 'O', 'O', 'H-SP', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'])
    def test_get_feature_tuple1(self):
        feature_dict = {'initial_tag': 'h2', 'is_header': True, 'is_task_scope': True, 'is_minimum_qualification': False, 'is_preferred_qualification': False, 'is_legal_notification': False, 'is_job_title': False, 'is_office_location': False, 'is_job_duration': False, 'is_supplemental_pay': False, 'is_educational_requirement': False, 'is_interview_procedure': False, 'is_corporate_scope': False, 'is_posting_date': False, 'is_other': False, 'child_str': '<h2 class="jobsearch-JobDescriptionSection-jobDescriptionTitle icl-u-xs-my--md" id="jobDescriptionTitle">Full Job Description</h2>'}
        pos_lr_predict_single = None
        self.assertEqual(self.hc.get_feature_tuple(feature_dict, pos_lr_predict_single),
                         ('h2',
                          '<h2 class="jobsearch-JobDescriptionSection-jobDescriptionTitle icl-u-xs-my--md" id="jobDescriptionTitle">' +
                          'Full Job Description</h2>', 'H-TS'))
    
    def test_get_feature_tuple2(self):
        feature_dict = {
            'initial_tag': 'p', 'is_header': True, 'is_task_scope': False, 'is_req_quals': False,
            'is_preff_quals': False, 'is_legal_notifs': False, 'is_job_title': False,
            'is_office_location': True, 'is_job_duration': False, 'is_supp_pay': False,
            'is_educ_reqs': False, 'is_interv_proc': False, 'is_corp_scope': False,
            'is_post_date': False, 'is_other': False,
            'child_str': '<p>Work Remotely:</p>'
            }
        self.assertEqual(self.hc.get_feature_tuple(feature_dict, pos_lr_predict_single=None, pos_crf_predict_single=None, pos_sgd_predict_single=None), ('p', '<p>Work Remotely:</p>', 'H-OL'))
    
    def test_get_feature_dict_list(self):
        child_tags_list = ['b', 'p', 'p', 'b', 'li', 'li', 'li', 'li', 'li', 'li', 'li', 'b', 'li', 'li',
                           'li', 'li', 'b', 'p', 'p', 'p', 'b', 'li', 'li', 'li', 'li', 'li', 'li', 'li', 'li', 'li', 'li', 'p']
        is_header_list = [True, False, False, True, False, False, False, False, False, False, False,
                          True, False, False, False, False, True, False, False, False, True, False,
                          False, False, False, False, False, False, False, False, False, False]
        feature_dict_list = [{'initial_tag': 'b', 'is_header': True, 'is_task_scope': 1, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': '<b>The Role:</b>'}, {'initial_tag': 'p', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': "<p>As the Director of Data Science at Brightloom, you'll lead the data science team and partner across the organization to help grow our data science capabilities. You'll be taking business needs from product and engineering teams and creating a comprehensive data science strategy around them. From there, you help prioritize the work for the data science team, balancing the work for the team and helping the independent contributors be their best. You will heavily engage with the application engineering, data engineering, and data science technical leads to ensure that your data science strategies are operationalized effectively.</p>"}, {'initial_tag': 'p', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': "<p>You're a person who loves helping others work together to do interesting data science. You can evangelize a data science idea to non-technical people, and you can deal with the realities of a complex business and figure out how to have data science contribute in a positive way. You enjoy leading data scientists so they can do strong work, and helping to elevate the data scientist's concerns when they raise them.</p>"}, {'initial_tag': 'b', 'is_header': True, 'is_task_scope': 1, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': "<b>What you'll do:</b>"}, {'initial_tag': 'li', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': "<li>Lead the data science team as their manager - helping devise projects, removing blockers, and engaging with independent contributors. You'll be hiring more data scientists and eventually hire managers to do this part of the job for you.</li>"}, {'initial_tag': 'li', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': '<li>Represent the data science discipline throughout the organization. You will have a powerful voice in the company and represent data scientists across different parts of the business.</li>'}, {'initial_tag': 'li', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': '<li>Partner across Brightloom engineering groups; evangelizing our culture of using data to measure, understand, and improve our product and features.</li>'}, {'initial_tag': 'li', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': '<li>Be a strong leader - you will give team members clear feedback that helps them grow and inspires thought leadership. You will lead by example, have compassion for everyone in the company and their challenges, and will take controversial directions when necessary.</li>'}, {'initial_tag': 'li', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': '<li>Be an expert in interpreting data and understanding its conclusions - your team will be creating lots of powerful insights and you will be finding the valuable implications of that data.</li>'}, {'initial_tag': 'li', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': '<li>Own the data science technical roadmap - take the business priorities from the product team and turn them into a set of projects the data science team will focus on delivering.</li>'}, {'initial_tag': 'li', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': "<li>Be involved in new product development - as the product team thinks of new ways to take customer feedback and create a better product, you'll be heavily involved with assessing what is feasible from a data science perspective.</li>"}, {'initial_tag': 'b', 'is_header': True, 'is_task_scope': None, 'is_minimum_qualification': 1, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': '<b>About you:</b>'}, {'initial_tag': 'li', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': '<li>Demonstrated experience building and developing a team</li>'}, {'initial_tag': 'li', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': '<li>Demonstrated experience putting a data science product into market, ideally in a startup</li>'}, {'initial_tag': 'li', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': '<li>Experience in the marketing, retail, or restaurant domain</li>'}, {'initial_tag': 'li', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': '<li>Foundational understanding of the data science ecosystem</li>'}, {'initial_tag': 'b', 'is_header': True, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': 1, 'is_posting_date': None, 'is_other': None, 'child_str': '<b>About Us</b>'}, {'initial_tag': 'p', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': '<p>At Brightloom (formerly eatsa), we are working to revolutionize restaurants through innovative technology and design. We are disrupting an industry worth $900 billion globally with partnerships in North America, Asia, and soon other continents.</p>'}, {'initial_tag': 'p', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': '<p>Led by our CEO, industry veteran and former Starbucks and J.Crew executive Adam Brotman, our unique, world-class team combines software and hardware engineers, designers, and industry experts to push the boundaries on re-engineering every aspect of the restaurant experience.</p>'}, {'initial_tag': 'p', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': "<p>We believe any restaurant brand should be able to engage customers digitally using a seamless combination of mobile, omni-channel ordering and loyalty offerings. Up until now, only a select few brands could afford, or knew how to put together a top-notch digital engagement and ordering platform. With key Starbucks technology components integrated into our platform, Brightloom will now allow any restaurant brand to create their own version of a world-class digital flywheel ecosystem. Brightloom's configurable technology suite combines convenience (digital ordering channels), personal connection (personalized marketing) and engagement (loyalty) for restaurant brands in today's new digital era.</p>"}, {'initial_tag': 'b', 'is_header': True, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': 1, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': '<b>What We Offer</b>'}, {'initial_tag': 'li', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': '<li>Fun, creative and collaborative remote work environment</li>'}, {'initial_tag': 'li', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': '<li>Competitive pay and equity/stock options</li>'}, {'initial_tag': 'li', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': '<li>Health, Dental &amp; Vision Insurance Coverage</li>'}, {'initial_tag': 'li', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': '<li>Life Insurance, Short-Term Disability, Long-Term Disability</li>'}, {'initial_tag': 'li', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': '<li>Phone/Internet Reimbursement</li>'}, {'initial_tag': 'li', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': '<li>Home Office Refresh Reimbursement</li>'}, {'initial_tag': 'li', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': '<li>Employee Assistance Program</li>'}, {'initial_tag': 'li', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': '<li>Flexible Spending Account &amp; Health Savings Account</li>'}, {'initial_tag': 'li', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': '<li>Flexible Time Off</li>'}, {'initial_tag': 'li', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': '<li>401(k)</li>'}, {'initial_tag': 'p', 'is_header': False, 'is_task_scope': None, 'is_minimum_qualification': None, 'is_preferred_qualification': None, 'is_legal_notification': None, 'is_job_title': None, 'is_office_location': None, 'is_job_duration': None, 'is_supplemental_pay': None, 'is_educational_requirement': None, 'is_interview_procedure': None, 'is_corporate_scope': None, 'is_posting_date': None, 'is_other': None, 'child_str': '<p>Brightloom is an Equal Employment Opportunity Employer. All qualified applicants will receive consideration for employment without regard to race, color, religion, sex, national origin, sexual orientation, gender identity, disability and protected veterans status or any other characteristic protected by law.</p>'}]
        self.assertEqual(self.hc.get_feature_dict_list(child_tags_list, is_header_list, self.test_child_strs_list), feature_dict_list)

if __name__ == '__main__':
    unittest.main()