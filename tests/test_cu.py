
#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



# cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\tests
# python -m unittest test_cu.TestCuMethods.test_clean_text

import unittest
import os

class TestCuMethods(unittest.TestCase):
    def setUp(self):
        import sys
        import os
        sys.path.insert(1, '../py')
        
        from ha_utils import HeaderAnalysis
        self.ha = HeaderAnalysis(s=s, verbose=False)
        
        from scrape_utils import WebScrapingUtilities
        self.wsu = WebScrapingUtilities()
        uri = self.wsu.secrets_json['neo4j']['connect_url']
        user =  self.wsu.secrets_json['neo4j']['username']
        password = self.wsu.secrets_json['neo4j']['password']
        
        from storage import Storage
        self.s = Storage()
        
        from cypher_utils import CypherUtilities
        self.cu = CypherUtilities(
            uri=uri, user=user, password=password, driver=None, s=self.s, ha=self.ha
        )
        
        from hc_utils import HeaderCategories
        self.hc = HeaderCategories(cu=self.cu, verbose=False)
        
        import warnings
        warnings.filterwarnings('ignore')
    
        self.test_child_strs_list1 = ['<h2 class="jobsearch-JobDescriptionSection-title--main icl-u-textBold" id="jobDetails" ' + 'tabindex="-1">Job details</h2>', '<div class="jobsearch-JobDescriptionSection-sectionItemKey icl-u-textBold">Job Type</div>', '<div>Full-time</div>', 'Benefits', '<div class="css-brixrz e1wnkr790">Pulled from the full job description</div>', '<div class="css-tvvxwd ecydgvn1">401(k)</div>', '<div class="css-tvvxwd ecydgvn1">401(k) matching</div>', '<div class="css-tvvxwd ecydgvn1">AD&amp;D insurance</div>', '<div class="css-tvvxwd ecydgvn1">Cell phone reimbursement</div>', '<div class="css-tvvxwd ecydgvn1">Commuter assistance</div>', '<div class="css-tvvxwd ecydgvn1">Dental insurance</div>', '<span class="css-1ysvuef e1wnkr790">Show 7 more benefits</span>', '<h2 class="jobsearch-JobDescriptionSection-jobDescriptionTitle">Indeed\'s salary guide</h2>', '<li class="css-vktqis eu4oa1w0">Not provided by employer</li>', "$71.7K - $90.7K a year is Indeed's estimated salary for this role in Remote.", '<h2 class="jobsearch-JobDescriptionSection-jobDescriptionTitle icl-u-xs-my--md" ' + 'id="jobDescriptionTitle">Full Job Description</h2>', '<p>Help us grow into an ever-evolving marketplace! We are seeking an experienced and detail-oriented ' + 'Data/Business Analyst to help guide data-driven business and product decisions through analytics!</p>', '<b>WHAT WE DO</b>', "<p>Betterview is the Property Intelligence &amp; Risk Management Platform that leading P&amp;C " + "insurance companies depend on to identify and mitigate risk, improve operational and inspection " + "efficiency, and build a more transparent customer experience throughout the policy lifecycle. By " + "empowering insurers to automate pricing, underwriting, and renewal while focusing strategic action " + "on critical properties, Betterview is transforming the insurance industry from Repair and Replace to " + "Predict and Prevent. Combining continuously evolving AI, predictive analytics, computer vision, and " + "customizable workflows to geospatial imagery with " + "commercial, private, and public data, Betterview supports each business's unique needs through " + "transparent, actionable property insights.</p>", '<p>Every day, our diverse team is focused on the needs of our customers. We strive to earn their ' + 'trust by providing valuable, accurate insight that is important to their businesses. We provide our ' + 'customers with information that is not only useful to their business decisions but is easy to use. ' + 'We combine high quality human interactions with sleek, intuitive design and are pioneers on the ' + 'journey alongside our customers, who are transforming the way they do business with data-driven ' + 'decision-making.</p>', '<b>THE OPPORTUNITY</b>', '<p>In this exciting position, you will have the opportunity to provide support that ultimately ' + 'guides Betterview in improving products, services and software through analytics. You will focus on ' + 'performing detailed requirements analysis, documenting processes and some level of performance ' + 'testing. Your excellent communication and collaboration skills will come in handy as you will engage ' + 'with a cross functional team and customers to determine and evaluate business metrics to meet ' + 'ongoing organizational or customer information needs. You will also be responsible for giving ' + 'presentations, internally and externally, using industry expertise to develop impactful metrics and ' + 'statistics on custom data sets.</p>', '<b>WHAT YOU WILL BE DOING</b>', '<li>Analyzing and reporting complex data to meet customer needs; communicating complex data in ' + 'comprehensible ways;</li>', '<li>Merging, consolidating, cleansing data from multiple non-standardized sources to perform ' + 'analytics combined with internal datasets;</li>', '<li>Analyzing trends in customer issues to facilitate product improvement;</li>', '<li>Developing expertise in product knowledge to facilitate Customer workshop preparation;</li>', '<li>Critically evaluating information from multiple sources and clearly indicating quality of final ' + 'analysis;</li>', '<li>Performing requirements analysis; documenting results;</li>', '<li>Conducting insurance industry retros; identifying flags based on book analysis and retro ' + 'results;</li>', '<li>Applying insurance industry knowledge to projects to add value within graphical and analytical ' + 'results.</li>', '<b>Requirements</b>', '<b>WHAT YOU WILL BRING TO OUR COMPANY</b>', "<li>Bachelor's degree required.</li>", '<li>3+ years’ experience in business analysis or related field.</li>', '<li>Advanced technical skills with SQL, Excel, BI.</li>', '<li>Excellent presentation building skills using PowerPoint/keynotes and graphic design skills.</li>', '<li>Experience in creating detailed reports and presentations while being able to work independently ' + 'to deliver in-depth insights based on varying requirements.</li>', '<li>Property Insurance domain knowledge and experience in the industry – especially around data and ' + 'analytics – is highly desired.</li>', '<li>Light Python/Jupyter Notebooks knowledge is a plus.</li>', '<i>THE SUCCESSFUL CANDIDATE</i>', '<li>Has the ability to merge, consolidate, cleanse data from multiple non-standardized sources to ' + 'perform analytics combined with internal datasets.</li>', '<li>Can identify flags based on book analysis and retro results.</li>', '<li>Has in depth analytical and conceptual thinking skills.</li>', '<li>Has the ability/willingness to travel up to 10%.</li>', '<b>Benefits</b>', '<b>WHAT WE PROVIDE</b>', '<li>Compensation commensurate with experience.</li>', 'Generous health benefits – medical, dental and vision.', '<li>Medical offerings include PPO, HMO, and HDHP options through Kaiser, Anthem Blue Cross, Sharp ' + 'Health, and Sutter Health.</li>', '<li>Betterview covers 75% of the sponsored medical plan employee premium, 60% of dependents.</li>', '<li>For dental and vision, Betterview covers 75% of the employee premium, 50% of dependents.</li>', '401(k) Retirement Plan.', '<li>Betterview matches 100% of employee contributions up to the first 3% of pay, then 50% of ' + 'employee contributions on the next 2% of pay.</li>', '<li>FSA and HSA.</li>', '<li>10 paid ' + 'holidays.</li>', '<li>Full-time employees receive 160 hours per year of paid time off; part-time employees accrue PTO ' + 'on a pro-rated basis.</li>', '<li>Paid parental leave, up to 12 weeks of maternity / 4 weeks of paternity leave.</li>', '<li>Basic life and AD&amp;D insurance. Betterview pays 100% of the premium. Employees receive a ' + 'benefit amount of $50,000.</li>', '<li>Shortterm disability. Betterview pays for 100% of the plan premium.</li>', '<li>Charity contribution match, up to $100.</li>', '<li>Cell phone reimbursement.</li>', '<li>Professional development reimbursement.</li>', '<li>Commuter benefits.</li>', '<i>COVID Vaccine is required as a condition of employment with Betterview. Reasonable accommodations ' + 'will be considered.</i>', '<p>Betterview provides equal employment opportunities (EEO) to all employees and applicants for ' + 'employment without regard to age, color, religion, sex, sexual orientation, gender identity, ' + 'national origin, disability, genetics, veteran status, or other legally protected characteristics. ' + 'In addition to federal law requirements, Betterview complies with applicable state and local laws ' + 'governing nondiscrimination in employment in every location in which the company has facilities. ' + 'This policy applies to all terms and conditions of employment, including recruiting, hiring, ' + 'placement, promotion, termination, layoff, recall, transfer, leaves of absence, compensation, and ' + 'training.</p>', '<p>Betterview will not discriminate or retaliate against applicants who inquire about, disclose, or ' + 'discuss their compensation or that of other applicants.</p>', '<p>Betterview will consider for employment all qualified applicants with criminal histories in a ' + 'manner consistent with applicable law. If you’re applying for a position in San Francisco, review ' + 'the guidelines applicable in your area.</p>', '<p>Betterview expressly prohibits any form of workplace harassment based on race, color, religion, ' + 'gender, sexual orientation, gender identity or expression, national origin, age, genetic ' + 'information, disability, or veteran status. Improper interference with the ability of Betterview ' + 'employees to perform their job duties may result in discipline up to and including discharge.</p>', '<p>If you have a disability or special need that requires accommodation to complete this ' + 'application, please let us know by contacting HR(at)Betterview(dot)com.</p>', '<p>_____________</p>', '<p>#LI-PS1</p>', '<h2 class="jobsearch-HiringInsights-header">Hiring Insights</h2>', '<h4 class="jobsearch-HiringInsights-subheader">Job activity</h4>', '<span class="jobsearch-HiringInsights-entry--text">Posted 3 days ago</span>']
        self.test_child_strs_list2 = ['<p>Patrick is a national engineering and design, construction, management services, and technology firm. Since 1979, we have been providing services to local, state, and federal government agencies; private and public utilities; and FORTUNE 500 companies. Having worked in all 50 states, six different countries and proven ourselves as a trusted partner, clients turn to us for the entire process of project delivery - from planning through construction to operation and maintenance. Patrick accomplishes this with a full suite of engineering disciplines, experienced construction managers, program management and project controls experts, and GIS and asset management technology specialists. We serve clients in the transportation, utility and renewable, industrial infrastructure, and federal and institutional markets. We take pride knowing the projects we work on have a positive effect on the community, society, and the environment.</p>', 'We have the following position available:', '<b>GIS Developer</b>', '<i>(while this role is remote, residence in the U.S. is required)</i>', '<b>Job Summary</b>', 'The GIS Developer is responsible for building out architectures and software solutions solving a variety of geospatial business problems for customers utilizing modern tooling and technologies. The GIS Developer provides geospatial technology support for problems of moderate scope and complexity and is responsible for developing, configuring, testing, implementing, and maintaining geospatial systems in close collaboration with the Development team. The Developer at this level may perform multiple concurrent assignments and may lead a small project of limited scope.', '<b>Duties and Responsibilities</b>', '<li>Develop and/or customize geospatial applications using comprehensive geospatial knowledge, project requirements, and an understanding of client needs</li>', '<li>Participate in the Software Development Life Cycle (SDLC) process in collaboration with other team members and provide GIS customization support on projects</li>', '<li>Participate in requirements gathering and analysis, functional specification, software design, testing, and deployment</li>', '<li>Participate in code reviews; deliver code focused on scalability, testability, supportability, and maintainability</li>', '<li>Maintain code integrity and organization</li>', '<li>Assist Analysts and/or Consultants with business development activities by participating in the creation of work plans, pricing estimates, and risk assessments for projects</li>', '<li>Recommend enhancements or changes to technology, methodology, and process standards</li>', '<li>Other duties as assigned</li>', '<b>Professional Requirements</b>', '<li>Bachelor’s degree in Computer Science, Geography/GIS, or other closely related field of study</li>', '<li>Typically 3+ years of experience developing GIS applications with development experience for web, mobile, and desktop applications</li>', '<li>Knowledge of standard methodologies, concepts, best practices, and procedures within a software development environment or complimentary GIS background</li>', '<li>Proficient using modern frameworks for either front end (e.g., Angular, Vue, React or scripting languages (e.g. Jupyter Notebooks, ArcGIS Pro Python Interpreter)</li>', '<li>Experience with either web mapping JavaScript APIs or Python spatial analysis packages such as arcpy</li>', '<li>Experience with back-end database technology such as Oracle, SQL Server, or PostGreSQL</li>', '<li>Familiarity with version control tools such as Git</li>', '<li>Knowledge of Esri ArcGIS development libraries (ArcGIS JavaScript API, ArcGIS Runtime SDKs, ArcGIS API for Python, ArcGIS REST API) preferred</li>', '<li>Strong written and oral communication skills</li>', '<li>Proficiency with Microsoft Office applications</li>', '<i>Patrick does not accept unsolicited resumes from search firms or agencies. Any resume submitted to any employee of Patrick without a prior written search agreement will be considered unsolicited and the property of Patrick. Please, no phone calls or emails.</i>', '<b>Equal Employment Opportunity / Affirmative Action Policy Statement</b>', 'It is the policy of Patrick Engineering Inc. (“Patrick”) to provide equal employment opportunity to all individuals regardless of their race, color, religion, sex (including pregnancy), national origin, age, disabilities, marital status, sexual orientation, gender identity, genetics, military status, disabled veterans, recently separated veterans, other protected veterans (veterans who served during a war or in a campaign or expedition for which a badge has been authorized), and Armed Forces service medal veteran, or any other characteristic protected by state or federal law. We are strongly committed to this policy and believe in the concept and spirit of the law.', '<p>Job Type: Full-time</p>']
        self.test_file_name1 = 'test.html'
        self.test_file_name2 = '52f0f96e8b1f7618_GIS_Developer_Remote_Indeed_com.html'
        self.test_file_path = os.path.join(self.ha.SAVES_HTML_FOLDER, self.test_file_name1)
        self.test_pre_str = '<html><head><title>test</title></head>'
        self.test_pre_str += '<body><div class="jobsearch-jobDescriptionText" id="jobDescriptionText">'
        self.test_post_str = '</div></body></html>'
    
    def tearDown(self):
        if os.path.isfile(self.test_file_path):
            os.remove(self.test_file_path)
    
    def test_get_child_tags_list1(self):
        self.assertEqual(
            self.cu.get_child_tags_list(self.test_child_strs_list1),
            self.ha.get_child_tags_list(self.test_child_strs_list1)
        )
        
    def test_get_child_tags_list2(self):
        self.assertEqual(
            self.cu.get_child_tags_list(self.test_child_strs_list2),
            self.ha.get_child_tags_list(self.test_child_strs_list2)
        )
    
    def test_get_is_header_list1(self):
        self.assertEqual(
            self.cu.get_is_header_list(self.test_child_strs_list1),
            self.ha.get_is_header_list(self.test_child_strs_list1)
        )
        
    def test_get_is_header_list2(self):
        self.assertEqual(
            self.cu.get_is_header_list(self.test_child_strs_list2),
            self.ha.get_is_header_list(self.test_child_strs_list2)
        )
    
    def test_get_feature_dict_list1(self):
        child_tags_list1 = self.cu.get_child_tags_list(self.test_child_strs_list1)
        is_header_list1 = self.cu.get_is_header_list(self.test_child_strs_list1)
        self.assertEqual(
            self.cu.get_feature_dict_list(child_tags_list1, self.test_child_strs_list1),
            self.hc.get_feature_dict_list(
                child_tags_list1, is_header_list1, self.test_child_strs_list1
            )
        )
        
    def test_get_feature_dict_list2(self):
        child_tags_list2 = self.cu.get_child_tags_list(self.test_child_strs_list2)
        is_header_list2 = self.cu.get_is_header_list(self.test_child_strs_list2)
        self.assertEqual(
            self.cu.get_feature_dict_list(child_tags_list2, self.test_child_strs_list2),
            self.hc.get_feature_dict_list(
                child_tags_list2, is_header_list2, self.test_child_strs_list2
            )
        )
        
    def test_get_child_strs_from_file2(self):
        file_path = os.path.join(self.cu.SAVES_HTML_FOLDER, self.test_file_name2)
        # import sys
        # sys.path.insert(1, '../load_magic')
        # from dataframes import get_page_soup
        # page_soup = get_page_soup(file_path)
        page_soup = self.wsu.get_page_soup(file_path)
        row_div_list = page_soup.find_all(name='div', id='jobDescriptionText')
        child_strs_list = self.ha.get_navigable_children(row_div_list[0], [])
        self.assertEqual(
            self.cu.get_child_strs_from_file(file_name=self.test_file_name2), child_strs_list
        )
    
    # def test_ensure_navigableparents_relationship(self):
        # navigable_parent1 = 
        # navigable_parent2 = 
        # file_name = 
        # sequence_order = 
        # self.assertEqual(self.cu.ensure_navigableparents_relationship(navigable_parent1, navigable_parent2, file_name, sequence_order), )

    # def test_ensure_headertags_relationship(self):
        # header_tag1 = 
        # header_tag2 = 
        # file_name = 
        # sequence_order = 
        # self.assertEqual(self.cu.ensure_headertags_relationship(header_tag1, header_tag2, file_name, sequence_order), )

    # def test_find_basic_quals_section(self):
        # child_strs_list = 
        # hc = 
        # ea = 
        # cu = 
        # self.assertEqual(self.su.find_basic_quals_section_indexes(child_strs_list, hc, ea, cu), )
    
    # def test_get_headertagsequence_id(self):
        # file_name = 
        # header_tag_id = 
        # sequence_order = 
        # self.assertEqual(self.cu.get_headertagsequence_id(file_name, header_tag_id, sequence_order), )
    
    # def test_do_cypher_tx(self):
        # tx = 
        # cypher = 
        # self.assertEqual(self.cu.do_cypher_tx(tx, cypher), )
    
    # def test_ensure_headertag_navigableparent_relationship(self):
        # header_tag = 
        # navigable_parent = 
        # self.assertEqual(self.cu.ensure_headertag_navigableparent_relationship(header_tag, navigable_parent), )
    
    # def test_append_parts_of_speech_list(self):
        # navigable_parent = 
        # pos_list = 
        # self.assertEqual(self.cu.append_parts_of_speech_list(navigable_parent, pos_list), )
    
    # def test_get_execution_results(self):
        # cypher_str = 
        # self.assertEqual(self.cu.get_execution_results(cypher_str), )
    
    def test_clean_text(self):
        dirty_text = 'Senior_Data_Scientist–Statistics_and_Machine_Learning_b7c10bcd03f70654.html'
        self.assertEqual(self.cu.clean_text(dirty_text), dirty_text)
    
    # def test_convert_str_to_hash(self):
        # unhashed_str = 
        # self.assertEqual(self.cu.convert_str_to_hash(unhashed_str), )
    
    # def test_get_filename_id(self):
        # file_name = 
        # self.assertEqual(self.cu.get_filename_id(file_name), )
    
    # def test_ensure_filename(self):
        # file_name = 
        # self.assertEqual(self.cu.ensure_filename(file_name), )
    
    # def test_get_headertag_id(self):
        # header_tag = 
        # self.assertEqual(self.cu.get_headertag_id(header_tag), )
    
    # def test_get_headertag(self):
        # header_tag_id = 
        # self.assertEqual(self.cu.get_headertag(header_tag_id), )
    
    # def test_ensure_headertag(self):
        # header_tag = 
        # self.assertEqual(self.cu.ensure_headertag(header_tag), )
    
    # def test_ensure_navigableparent(self):
        # navigable_parent = 
        # self.assertEqual(self.cu.ensure_navigableparent(navigable_parent), )
    
    # def test_ensure_headertagsequence_filename_relationship(self):
        # file_name = 
        # self.assertEqual(self.cu.ensure_headertagsequence_filename_relationship(file_name), )
    
    # def test_ensure_headertagsequence_headertag_relationship(self):
        # header_tag_id = 
        # self.assertEqual(self.cu.ensure_headertagsequence_headertag_relationship(header_tag_id), )
    
    # def test_create_header_tag_sequence_table_dataframe(self):
        # save_as_csv = 
        # self.assertEqual(self.cu.create_header_tag_sequence_table_dataframe(save_as_csv), )
    
    # def test_get_filenames_by_starting_sequence(self):
        # sequence_list = 
        # self.assertEqual(self.cu.get_filenames_by_starting_sequence(sequence_list), )
    
    # def test_get_filenames_by_sequence(self):
        # sequence_list = 
        # self.assertEqual(self.cu.get_filenames_by_sequence(sequence_list), )
    
    # def test_create_filenames_table(self):
        # self.assertEqual(self.cu.create_filenames_table(), )
    
    # def test_populate_filenames_table(self):
        # self.assertEqual(self.cu.populate_filenames_table(), )
    
    # def test_get_files_list(self):
        # self.assertEqual(self.cu.get_files_list(), )
    
    # def test_get_all_filenames(self):
        # self.assertEqual(self.cu.get_all_filenames(), )
    
    # def test_create_headertags_table(self):
        # self.assertEqual(self.cu.create_headertags_table(), )
    
    # def test_populate_headertags_table(self):
        # self.assertEqual(self.cu.populate_headertags_table(), )
    
    # def test_create_navigableparents_table(self):
        # self.assertEqual(self.cu.create_navigableparents_table(), )
    
    # def test_populate_navigableparents_table(self):
        # self.assertEqual(self.cu.populate_navigableparents_table(), )
    
    # def test_create_headertagsequence_table(self):
        # self.assertEqual(self.cu.create_headertagsequence_table(), )
    
    # def test_populate_headertagsequence_table(self):
        # self.assertEqual(self.cu.populate_headertagsequence_table(), )
    
    # def test_delete_navigableparentsequence_nodes(self):
        # self.assertEqual(self.cu.delete_navigableparentsequence_nodes(), )
    
    # def test_populate_navigableparent_sequences(self):
        # self.assertEqual(self.cu.populate_navigableparent_sequences(), )
    
    # def test_create_partsofspeech_table(self):
        # self.assertEqual(self.cu.create_partsofspeech_table(), )
    
    # def test_populate_partsofspeech_table(self):
        # self.assertEqual(self.cu.populate_partsofspeech_table(), )
    
    # def test_delete_minimumrequirementssection_nodes(self):
        # self.assertEqual(self.cu.delete_minimumrequirementssection_nodes(), )
    
    # def test_populate_minimumrequirementssection_table(self):
        # self.assertEqual(self.cu.populate_minimumrequirementssection_table(), )
    
    # def test_populate_relationships(self):
        # self.assertEqual(self.cu.populate_relationships(), )
    
    # def test_build_child_strs_list_dictionary(self):
        # self.assertEqual(self.cu.build_child_strs_list_dictionary(), )
    
    # def test_create_header_pattern_dictionary(self):
        # self.assertEqual(self.cu.create_header_pattern_dictionary(), )
    
    # def test_create_navigableparent_is_qual_dictionary(self):
        # self.assertEqual(self.cu.create_navigableparent_is_qual_dictionary(), )
    
    # def test_create_navigableparent_is_header_dictionary(self):
        # self.assertEqual(self.cu.create_navigableparent_is_header_dictionary(), )
    
    # def test_ensure_navigableparent_is_header_from_dictionary(self):
        # self.assertEqual(self.cu.ensure_navigableparent_is_header_from_dictionary(), )
    
    # def test_create_task_scope_pickle(self):
        # self.assertEqual(self.cu.create_task_scope_pickle(), )
    
    # def test_create_req_quals_pickle(self):
        # self.assertEqual(self.cu.create_req_quals_pickle(), )
    
    # def test_create_o_rq_pickle(self):
        # self.assertEqual(self.cu.create_o_rq_pickle(), )
    
    # def test_create_h_rq_pickle(self):
        # self.assertEqual(self.cu.create_h_rq_pickle(), )
    
    # def test_create_preff_quals_pickle(self):
        # self.assertEqual(self.cu.create_preff_quals_pickle(), )
    
    # def test_create_legal_notifs_pickle(self):
        # self.assertEqual(self.cu.create_legal_notifs_pickle(), )
    
    # def test_create_job_title_pickle(self):
        # self.assertEqual(self.cu.create_job_title_pickle(), )
    
    # def test_create_office_loc_pickle(self):
        # self.assertEqual(self.cu.create_office_loc_pickle(), )
    
    # def test_create_job_duration_pickle(self):
        # self.assertEqual(self.cu.create_job_duration_pickle(), )
    
    # def test_create_supp_pay_pickle(self):
        # self.assertEqual(self.cu.create_supp_pay_pickle(), )
    
    # def test_create_educ_reqs_pickle(self):
        # self.assertEqual(self.cu.create_educ_reqs_pickle(), )
    
    # def test_create_interv_proc_pickle(self):
        # self.assertEqual(self.cu.create_interv_proc_pickle(), )
    
    # def test_create_corp_scope_pickle(self):
        # self.assertEqual(self.cu.create_corp_scope_pickle(), )
    
    # def test_create_post_date_pickle(self):
        # self.assertEqual(self.cu.create_post_date_pickle(), )
    
    # def test_create_other_pickle(self):
        # self.assertEqual(self.cu.create_other_pickle(), )

if __name__ == '__main__':
    unittest.main()