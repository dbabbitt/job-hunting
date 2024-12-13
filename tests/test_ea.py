
#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



# cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\tests
# python -m unittest test_ea.TestEaMethods.test_get_idx_list

import unittest

class TestEaMethods(unittest.TestCase):
    def setUp(self):
        import sys
        import os
        if (osp.join(os.pardir, 'py') not in sys.path): sys.path.insert(1, osp.join(os.pardir, 'py'))
        
        from ha_utils import HeaderAnalysis
        self.ha = HeaderAnalysis(s=s, verbose=False)
        
        from scrape_utils import WebScrapingUtilities
        wsu = WebScrapingUtilities()
        uri = wsu.secrets_json['neo4j']['connect_url']
        user =  wsu.secrets_json['neo4j']['username']
        password = wsu.secrets_json['neo4j']['password']
        
        from storage import Storage
        self.s = Storage()
        
        from cypher_utils import CypherUtilities
        self.cu = CypherUtilities(uri=uri, user=user, password=password, driver=None, s=self.s, ha=self.ha)
        
        from hc_utils import HeaderCategories
        self.hc = HeaderCategories(cu=self.cu, verbose=False)
        
        from html_analysis import ElementAnalysis
        self.ea = ElementAnalysis(ha=self.ha, hc=self.hc, verbose=False)
        
        from crf_utils import CrfUtilities
        self.crf = CrfUtilities(ha=self.ha, hc=self.hc, cu=self.cu, verbose=False)
        
        import warnings
        warnings.filterwarnings('ignore')
        
        self.test_child_strs_list = ['<h2 class="jobsearch-JobDescriptionSection-title--main icl-u-textBold" id="jobDetails" ' + 'tabindex="-1">Job details</h2>', '<div class="jobsearch-JobDescriptionSection-sectionItemKey icl-u-textBold">Job Type</div>', '<div>Full-time</div>', 'Benefits', '<div class="css-brixrz e1wnkr790">Pulled from the full job description</div>', '<div class="css-tvvxwd ecydgvn1">401(k)</div>', '<div class="css-tvvxwd ecydgvn1">401(k) matching</div>', '<div class="css-tvvxwd ecydgvn1">AD&amp;D insurance</div>', '<div class="css-tvvxwd ecydgvn1">Cell phone reimbursement</div>', '<div class="css-tvvxwd ecydgvn1">Commuter assistance</div>', '<div class="css-tvvxwd ecydgvn1">Dental insurance</div>', '<span class="css-1ysvuef e1wnkr790">Show 7 more benefits</span>', '<h2 class="jobsearch-JobDescriptionSection-jobDescriptionTitle">Indeed\'s salary guide</h2>', '<li class="css-vktqis eu4oa1w0">Not provided by employer</li>', "$71.7K - $90.7K a year is Indeed's estimated salary for this role in Remote.", '<h2 class="jobsearch-JobDescriptionSection-jobDescriptionTitle icl-u-xs-my--md" ' + 'id="jobDescriptionTitle">Full Job Description</h2>', '<p>Help us grow into an ever-evolving marketplace! We are seeking an experienced and detail-oriented ' + 'Data/Business Analyst to help guide data-driven business and product decisions through analytics!</p>', '<b>WHAT WE DO</b>', "<p>Betterview is the Property Intelligence &amp; Risk Management Platform that leading P&amp;C " + "insurance companies depend on to identify and mitigate risk, improve operational and inspection " + "efficiency, and build a more transparent customer experience throughout the policy lifecycle. By " + "empowering insurers to automate pricing, underwriting, and renewal while focusing strategic action " + "on critical properties, Betterview is transforming the insurance industry from Repair and Replace to " + "Predict and Prevent. Combining continuously evolving AI, predictive analytics, computer vision, and " + "customizable workflows to geospatial imagery with " + "commercial, private, and public data, Betterview supports each business's unique needs through " + "transparent, actionable property insights.</p>", '<p>Every day, our diverse team is focused on the needs of our customers. We strive to earn their ' + 'trust by providing valuable, accurate insight that is important to their businesses. We provide our ' + 'customers with information that is not only useful to their business decisions but is easy to use. ' + 'We combine high quality human interactions with sleek, intuitive design and are pioneers on the ' + 'journey alongside our customers, who are transforming the way they do business with data-driven ' + 'decision-making.</p>', '<b>THE OPPORTUNITY</b>', '<p>In this exciting position, you will have the opportunity to provide support that ultimately ' + 'guides Betterview in improving products, services and software through analytics. You will focus on ' + 'performing detailed requirements analysis, documenting processes and some level of performance ' + 'testing. Your excellent communication and collaboration skills will come in handy as you will engage ' + 'with a cross functional team and customers to determine and evaluate business metrics to meet ' + 'ongoing organizational or customer information needs. You will also be responsible for giving ' + 'presentations, internally and externally, using industry expertise to develop impactful metrics and ' + 'statistics on custom data sets.</p>', '<b>WHAT YOU WILL BE DOING</b>', '<li>Analyzing and reporting complex data to meet customer needs; communicating complex data in ' + 'comprehensible ways;</li>', '<li>Merging, consolidating, cleansing data from multiple non-standardized sources to perform ' + 'analytics combined with internal datasets;</li>', '<li>Analyzing trends in customer issues to facilitate product improvement;</li>', '<li>Developing expertise in product knowledge to facilitate Customer workshop preparation;</li>', '<li>Critically evaluating information from multiple sources and clearly indicating quality of final ' + 'analysis;</li>', '<li>Performing requirements analysis; documenting results;</li>', '<li>Conducting insurance industry retros; identifying flags based on book analysis and retro ' + 'results;</li>', '<li>Applying insurance industry knowledge to projects to add value within graphical and analytical ' + 'results.</li>', '<b>Requirements</b>', '<b>WHAT YOU WILL BRING TO OUR COMPANY</b>', "<li>Bachelor's degree required.</li>", '<li>3+ years’ experience in business analysis or related field.</li>', '<li>Advanced technical skills with SQL, Excel, BI.</li>', '<li>Excellent presentation building skills using PowerPoint/keynotes and graphic design skills.</li>', '<li>Experience in creating detailed reports and presentations while being able to work independently ' + 'to deliver in-depth insights based on varying requirements.</li>', '<li>Property Insurance domain knowledge and experience in the industry – especially around data and ' + 'analytics – is highly desired.</li>', '<li>Light Python/Jupyter Notebooks knowledge is a plus.</li>', '<i>THE SUCCESSFUL CANDIDATE</i>', '<li>Has the ability to merge, consolidate, cleanse data from multiple non-standardized sources to ' + 'perform analytics combined with internal datasets.</li>', '<li>Can identify flags based on book analysis and retro results.</li>', '<li>Has in depth analytical and conceptual thinking skills.</li>', '<li>Has the ability/willingness to travel up to 10%.</li>', '<b>Benefits</b>', '<b>WHAT WE PROVIDE</b>', '<li>Compensation commensurate with experience.</li>', 'Generous health benefits – medical, dental and vision.', '<li>Medical offerings include PPO, HMO, and HDHP options through Kaiser, Anthem Blue Cross, Sharp ' + 'Health, and Sutter Health.</li>', '<li>Betterview covers 75% of the sponsored medical plan employee premium, 60% of dependents.</li>', '<li>For dental and vision, Betterview covers 75% of the employee premium, 50% of dependents.</li>', '401(k) Retirement Plan.', '<li>Betterview matches 100% of employee contributions up to the first 3% of pay, then 50% of ' + 'employee contributions on the next 2% of pay.</li>', '<li>FSA and HSA.</li>', '<li>10 paid ' + 'holidays.</li>', '<li>Full-time employees receive 160 hours per year of paid time off; part-time employees accrue PTO ' + 'on a pro-rated basis.</li>', '<li>Paid parental leave, up to 12 weeks of maternity / 4 weeks of paternity leave.</li>', '<li>Basic life and AD&amp;D insurance. Betterview pays 100% of the premium. Employees receive a ' + 'benefit amount of $50,000.</li>', '<li>Shortterm disability. Betterview pays for 100% of the plan premium.</li>', '<li>Charity contribution match, up to $100.</li>', '<li>Cell phone reimbursement.</li>', '<li>Professional development reimbursement.</li>', '<li>Commuter benefits.</li>', '<i>COVID Vaccine is required as a condition of employment with Betterview. Reasonable accommodations ' + 'will be considered.</i>', '<p>Betterview provides equal employment opportunities (EEO) to all employees and applicants for ' + 'employment without regard to age, color, religion, sex, sexual orientation, gender identity, ' + 'national origin, disability, genetics, veteran status, or other legally protected characteristics. ' + 'In addition to federal law requirements, Betterview complies with applicable state and local laws ' + 'governing nondiscrimination in employment in every location in which the company has facilities. ' + 'This policy applies to all terms and conditions of employment, including recruiting, hiring, ' + 'placement, promotion, termination, layoff, recall, transfer, leaves of absence, compensation, and ' + 'training.</p>', '<p>Betterview will not discriminate or retaliate against applicants who inquire about, disclose, or ' + 'discuss their compensation or that of other applicants.</p>', '<p>Betterview will consider for employment all qualified applicants with criminal histories in a ' + 'manner consistent with applicable law. If you’re applying for a position in San Francisco, review ' + 'the guidelines applicable in your area.</p>', '<p>Betterview expressly prohibits any form of workplace harassment based on race, color, religion, ' + 'gender, sexual orientation, gender identity or expression, national origin, age, genetic ' + 'information, disability, or veteran status. Improper interference with the ability of Betterview ' + 'employees to perform their job duties may result in discipline up to and including discharge.</p>', '<p>If you have a disability or special need that requires accommodation to complete this ' + 'application, please let us know by contacting HR(at)Betterview(dot)com.</p>', '<p>_____________</p>', '<p>#LI-PS1</p>', '<h2 class="jobsearch-HiringInsights-header">Hiring Insights</h2>', '<h4 class="jobsearch-HiringInsights-subheader">Job activity</h4>', '<span class="jobsearch-HiringInsights-entry--text">Posted 3 days ago</span>']
        self.test_consecutives_list = [('O', 1), ('H-JT', 1), ('O', 13), ('H-TS', 1), ('O', 15),
                                       ('H-RQ', 1), ('O', 13), ('H-SP', 1), ('O', 29)]
        self.test_pos_list = [
            'O', 'H-JT', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',
            'H-TS', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',
            'O', 'H-RQ', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',
            'H-SP', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',
            'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'
        ]
    
    def test_get_idx_list(self):
        items_list = ['H', 'O', 'H-RQ', 'O', 'O', 'O', 'O', 'O', 'O-RQ', 'O', 'O', 'O', 'O', 'O', 'O-JD', 'O-SP',
                      'H-SP', 'O-SP', 'O', 'O', 'O', 'O', 'O', 'H-JD', 'O', 'O-OL', 'H-RQ', 'O', 'O-PQ', 'O', 'H-OL',
                      'O', 'H-OL', 'O', 'H-OL', 'O', 'H-IP', 'O']
        item_str = 'H-RQ'
        self.assertEqual(self.ea.get_idx_list(items_list, item_str), [2, 26])

    def test_find_basic_quals_section1(self):
        test_child_strs_list = ['<b>The Role:</b>', "<p>As the Director of Data Science at Brightloom, you'll lead the data science " + "team and partner across the organization to help grow our data science capabilities. You'll be " + "taking business needs from product and engineering teams and creating a comprehensive data " + "science strategy around them. From there, you help prioritize the work for the data science " + "team, balancing the work for the team and helping the independent contributors be their best. " + "You will heavily engage with the application engineering, data engineering, and data science " + "technical leads to ensure that your data science strategies are operationalized effectively.</p>", "<p>You're a person who loves helping others work together to do interesting data science. You " + "can evangelize a data science idea to non-technical people, and you can deal with the " + "realities of a complex business and figure out how to have data science contribute in a " + "positive way. You enjoy leading data scientists so they can do strong work, and helping to " + "elevate the data scientist's concerns when they raise them.</p>", "<b>What you'll do:</b>", "<li>Lead the data science team as their manager - helping devise projects, removing blockers, " + "and engaging with independent contributors. You'll be hiring more data scientists and " + "eventually hire managers to do this part of the job for you.</li>", '<li>Represent the data science discipline throughout the organization. You will have a ' + 'powerful voice in the company and represent data scientists across different parts of the ' + 'business.</li>', '<li>Partner across Brightloom engineering groups; evangelizing our culture of using data to ' + 'measure, understand, and improve our product and features.</li>', '<li>Be a strong leader - you will give team members clear feedback that helps them grow ' + 'and inspires thought leadership. You will lead by example, have compassion for everyone in ' + 'the company and their challenges, and will take controversial directions when necessary.</li>', '<li>Be an expert in interpreting data and understanding its conclusions - your team will ' + 'be creating lots of powerful insights and you will be finding the valuable implications of ' + 'that data.</li>', '<li>Own the data science technical roadmap - take the business priorities from the product ' + 'team and turn them into a set of projects the data science team will focus on delivering.</li>', "<li>Be involved in new product development - as the product team thinks of new ways to take " + "customer feedback and create a better product, you'll be heavily involved with assessing " + "what is feasible from a data science perspective.</li>", '<b>About you:</b>', '<li>Demonstrated experience building and developing a team</li>', '<li>Demonstrated experience putting a data science product into market, ideally in a startup</li>', '<li>Experience in the marketing, retail, or restaurant domain</li>', '<li>Foundational understanding of the data science ecosystem</li>', '<b>About Us</b>', '<p>At Brightloom (formerly eatsa), we are working to revolutionize restaurants through ' + 'innovative technology and design. We are disrupting an industry worth $900 billion globally ' + 'with partnerships in North America, Asia, and soon other continents.</p>', '<p>Led by our CEO, industry veteran and former Starbucks and J.Crew executive Adam Brotman, our ' + 'unique, world-class team combines software and hardware engineers, designers, and industry ' + 'experts to push the boundaries on re-engineering every aspect of the restaurant experience.</p>', "<p>We believe any restaurant brand should be able to engage customers digitally using a " + "seamless combination of mobile, omni-channel ordering and loyalty offerings. Up until now, " + "only a select few brands could afford, or knew how to put together a top-notch digital " + "engagement and ordering platform. With key Starbucks technology components integrated into " + "our platform, Brightloom will now allow any restaurant brand to create their own version of a " + "world-class digital flywheel ecosystem. Brightloom's configurable technology suite combines " + "convenience (digital ordering channels), personal connection (personalized marketing) and " + "engagement (loyalty) for restaurant brands in today's new digital era.</p>", '<b>What We Offer</b>', '<li>Fun, creative and collaborative remote work environment</li>', '<li>Competitive pay and equity/stock options</li>', '<li>Health, Dental &amp; Vision Insurance Coverage</li>', '<li>Life Insurance, Short-Term Disability, Long-Term Disability</li>', '<li>Phone/Internet Reimbursement</li>', '<li>Home Office Refresh Reimbursement</li>', '<li>Employee Assistance Program</li>', '<li>Flexible Spending Account &amp; Health Savings Account</li>', '<li>Flexible Time Off</li>', '<li>401(k)</li>', '<p>Brightloom is an Equal Employment Opportunity Employer. All qualified applicants will ' + 'receive consideration for employment without regard to race, color, religion, sex, national ' + 'origin, sexual orientation, gender identity, disability and protected veterans status or any ' + 'other characteristic protected by law.</p>']
        test_consecutives_list = [('H-TS', 1), ('O', 2), ('H-TS', 1), ('O', 7),
                                  ('H-RQ', 1), ('O', 4), ('H-CS', 1), ('O', 3), ('H-SP', 1), ('O', 11)]
        test_pos_list = ['H-TS', 'O', 'O', 'H-TS', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'H-RQ',
                         'O', 'O', 'O', 'O', 'H-CS', 'O', 'O', 'O', 'H-SP', 'O', 'O', 'O', 'O',
                         'O', 'O', 'O', 'O', 'O', 'O', 'O']
        consecutives_list, pos_list = self.su.find_basic_quals_section_indexes(test_child_strs_list, verbose=False
        )
        self.assertEqual(test_consecutives_list, consecutives_list)
        self.assertEqual(test_pos_list, pos_list)
    
    def test_find_basic_quals_section2(self):
        consecutives_list, pos_list = self.su.find_basic_quals_section_indexes(self.test_child_strs_list, verbose=False)
        self.assertEqual(self.test_consecutives_list, consecutives_list)
        self.assertEqual(self.test_pos_list, pos_list)
    
if __name__ == '__main__':
    unittest.main()