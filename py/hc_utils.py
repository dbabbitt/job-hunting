
#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



import pandas as pd
from storage import Storage

s = Storage()

class HeaderCategories(object):
    """Header categories class."""
    
    def __init__(self, cu=None, verbose=False):
        if cu is None:
            import cypher_utils
            self.cu = cypher_utils.CypherUtilities()
        else:
            self.cu = cu
        self.verbose = verbose

        # Get the task scope headers
        cypher_str = """
            MATCH (np:NavigableParents {is_task_scope: 'True', is_header: 'True'})
            RETURN np.navigable_parent AS navigable_parent;"""
        df = pd.DataFrame(self.cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the task scope list
        self.TASK_SCOPE_HEADERS_LIST = df.navigable_parent.tolist()
        if not len(self.TASK_SCOPE_HEADERS_LIST):
            if s.pickle_exists('TASK_SCOPE_HEADERS_LIST'):
                self.TASK_SCOPE_HEADERS_LIST = s.load_object('TASK_SCOPE_HEADERS_LIST')
            else:
                self.TASK_SCOPE_HEADERS_LIST = ['<b>Where You Come In:</b>', '<b>Responsibilities:</b>', '<b>Primary Responsibilities:</b>', '<h2 class="jobsearch-JobDescriptionSection-jobDescriptionTitle icl-u-xs-my--md" id="jobDescriptionTitle">Full Job Description</h2>', '<b>What will you do?</b>', '<b>What does your success look like in the first 90 days?</b>', '<b>Job Summary</b>', '<b>Core Responsibilities</b>', '<b>Duties included but not limited to:</b>', 'Translate / Interpret:', 'Measure / Quantify / Expand:', 'Explore / Enlighten:', '<b>Responsibilities</b>', '<div>Key responsibilities in this role include:</div>', 'Overview:', 'Responsibilities:', '<b>This means you will:</b>', '<b>ROLE SUMMARY</b>', '<b>ROLE RESPONSIBILITIES</b>', '<b>Key Responsibilities</b>', '<b>Description</b>', '<b>Overview</b>', '<b>Summary</b>', '<b>Principal Duties &amp; Responsibilities</b>']
                s.store_objects(TASK_SCOPE_HEADERS_LIST=self.TASK_SCOPE_HEADERS_LIST, verbose=verbose)

        # Get the req quals headers
        cypher_str = """
            MATCH (np:NavigableParents {is_minimum_qualification: 'True', is_header: 'True'})
            RETURN np.navigable_parent AS navigable_parent;"""
        df = pd.DataFrame(self.cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the req quals list
        self.REQ_QUALS_HEADERS_LIST = df.navigable_parent.tolist()
        if not len(self.REQ_QUALS_HEADERS_LIST):
            if s.pickle_exists('REQ_QUALS_HEADERS_LIST'):
                self.REQ_QUALS_HEADERS_LIST = s.load_object('REQ_QUALS_HEADERS_LIST')
            else:
                self.REQ_QUALS_HEADERS_LIST = ['<b>What it Takes to Succeed:</b>', '<b>A candidate must:</b>', '<b>Position Requirements:</b>', '<p>Experience:</p>', '<b>Qualifications:</b>', '<b>Required Qualifications:</b>', '<b>What skills, experiences, and education are required?</b>', '<b>Qualifying Experience</b>', '<b>Requirements:</b>', '<b>Qualifications</b>', 'Qualifications:', 'Minimum Skill Qualifications', '<b>To do that, this mean you have:</b>', '<b>QUALIFICATIONS</b>', '<b>Job Qualifications</b>', '<b>Work Experience</b>', '<b>License and Certifications</b>', '<b>Skills, Abilities &amp; Competencies</b>']
                s.store_objects(REQ_QUALS_HEADERS_LIST=self.REQ_QUALS_HEADERS_LIST, verbose=verbose)

        # Get the preff quals headers
        cypher_str = """
            MATCH (np:NavigableParents {is_preferred_qualification: 'True', is_header: 'True'})
            RETURN np.navigable_parent AS navigable_parent;"""
        df = pd.DataFrame(self.cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the preff quals list
        self.PREFF_QUALS_HEADERS_LIST = df.navigable_parent.tolist()
        if not len(self.PREFF_QUALS_HEADERS_LIST):
            if s.pickle_exists('PREFF_QUALS_HEADERS_LIST'):
                self.PREFF_QUALS_HEADERS_LIST = s.load_object('PREFF_QUALS_HEADERS_LIST')
            else:
                self.PREFF_QUALS_HEADERS_LIST = ['<b>Preferred Qualifications:</b>', '<b>What are we looking for?</b>', '<b>The Ideal Candidate will:</b>', '<p>You are...</p>', '<b>And we love people who:</b>', '<b>A strong candidate will also have</b>']
                s.store_objects(PREFF_QUALS_HEADERS_LIST=self.PREFF_QUALS_HEADERS_LIST, verbose=verbose)

        # Get the legal notifs headers
        cypher_str = """
            MATCH (np:NavigableParents {is_legal_notification: 'True', is_header: 'True'})
            RETURN np.navigable_parent AS navigable_parent;"""
        df = pd.DataFrame(self.cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the legal notifs list
        self.LEGAL_NOTIFS_HEADERS_LIST = df.navigable_parent.tolist()
        if not len(self.LEGAL_NOTIFS_HEADERS_LIST):
            if s.pickle_exists('LEGAL_NOTIFS_HEADERS_LIST'):
                self.LEGAL_NOTIFS_HEADERS_LIST = s.load_object('LEGAL_NOTIFS_HEADERS_LIST')
            else:
                self.LEGAL_NOTIFS_HEADERS_LIST = ['<div>CCPA Privacy Notice</div>', '<p>Application Question:</p>', '<b>EOE Statement:</b>', '<b>Sunshine Act</b>', '<b>EEO &amp; Employment Eligibility</b>', '<b>EEO Statement</b>']
                s.store_objects(LEGAL_NOTIFS_HEADERS_LIST=self.LEGAL_NOTIFS_HEADERS_LIST, verbose=verbose)

        # Get the job title headers
        cypher_str = """
            MATCH (np:NavigableParents {is_job_title: 'True', is_header: 'True'})
            RETURN np.navigable_parent AS navigable_parent;"""
        df = pd.DataFrame(self.cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the job title list
        self.JOB_TITLE_HEADERS_LIST = df.navigable_parent.tolist()
        if not len(self.JOB_TITLE_HEADERS_LIST):
            if s.pickle_exists('JOB_TITLE_HEADERS_LIST'):
                self.JOB_TITLE_HEADERS_LIST = s.load_object('JOB_TITLE_HEADERS_LIST')
            else:
                self.JOB_TITLE_HEADERS_LIST = ['<b>Position</b>']
                s.store_objects(JOB_TITLE_HEADERS_LIST=self.JOB_TITLE_HEADERS_LIST, verbose=verbose)

        # Get the office loc headers
        cypher_str = """
            MATCH (np:NavigableParents {is_office_location: 'True', is_header: 'True'})
            RETURN np.navigable_parent AS navigable_parent;"""
        df = pd.DataFrame(self.cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the office location list
        self.OFFICE_LOC_HEADERS_LIST = df.navigable_parent.tolist()
        if not len(self.OFFICE_LOC_HEADERS_LIST):
            if s.pickle_exists('OFFICE_LOC_HEADERS_LIST'):
                self.OFFICE_LOC_HEADERS_LIST = s.load_object('OFFICE_LOC_HEADERS_LIST')
            else:
                self.OFFICE_LOC_HEADERS_LIST = ['<b>Location</b>', '<p>Work Remotely:</p>', '<p>Work Location:</p>', '<b>Location and Travel:</b>', '<b>Travel :</b>', '<b>Working Conditions</b>', '<b>Primary Location</b>', '<b>Work Locations</b>']
                s.store_objects(OFFICE_LOC_HEADERS_LIST=self.OFFICE_LOC_HEADERS_LIST, verbose=verbose)

        # Get the job duration headers
        cypher_str = """
            MATCH (np:NavigableParents {is_job_duration: 'True', is_header: 'True'})
            RETURN np.navigable_parent AS navigable_parent;"""
        df = pd.DataFrame(self.cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the job duration list
        self.JOB_DURATION_HEADERS_LIST = df.navigable_parent.tolist()
        if not len(self.JOB_DURATION_HEADERS_LIST):
            if s.pickle_exists('JOB_DURATION_HEADERS_LIST'):
                self.JOB_DURATION_HEADERS_LIST = s.load_object('JOB_DURATION_HEADERS_LIST')
            else:
                self.JOB_DURATION_HEADERS_LIST = ['<b>Duration</b>', '<p>Schedule:</p>', '<b>Employee Status :</b>', '<b>Shift :</b>']
                s.store_objects(JOB_DURATION_HEADERS_LIST=self.JOB_DURATION_HEADERS_LIST, verbose=verbose)

        # Get the supp pay headers
        cypher_str = """
            MATCH (np:NavigableParents {is_supplemental_pay: 'True', is_header: 'True'})
            RETURN np.navigable_parent AS navigable_parent;"""
        df = pd.DataFrame(self.cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the supplemental pay list
        self.SUPP_PAY_HEADERS_LIST = df.navigable_parent.tolist()
        if not len(self.SUPP_PAY_HEADERS_LIST):
            if s.pickle_exists('SUPP_PAY_HEADERS_LIST'):
                self.SUPP_PAY_HEADERS_LIST = s.load_object('SUPP_PAY_HEADERS_LIST')
            else:
                self.SUPP_PAY_HEADERS_LIST = ['<b>Benefits</b>', '<p>Supplemental Pay:</p>', '<p>Benefit Conditions:</p>', '<b>Options</b>', '<p>Our Benefits Include:</p>', '<p>Benefits:</p>']
                s.store_objects(SUPP_PAY_HEADERS_LIST=self.SUPP_PAY_HEADERS_LIST, verbose=verbose)

        # Get the educ reqs headers
        cypher_str = """
            MATCH (np:NavigableParents {is_educational_requirement: 'True', is_header: 'True'})
            RETURN np.navigable_parent AS navigable_parent;"""
        df = pd.DataFrame(self.cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the educational requirements list
        self.EDUC_REQS_HEADERS_LIST = df.navigable_parent.tolist()
        if not len(self.EDUC_REQS_HEADERS_LIST):
            if s.pickle_exists('EDUC_REQS_HEADERS_LIST'):
                self.EDUC_REQS_HEADERS_LIST = s.load_object('EDUC_REQS_HEADERS_LIST')
            else:
                self.EDUC_REQS_HEADERS_LIST = ['<p>Education:</p>', '<b>Education</b>']
                s.store_objects(EDUC_REQS_HEADERS_LIST=self.EDUC_REQS_HEADERS_LIST, verbose=verbose)

        # Get the interv proc headers
        cypher_str = """
            MATCH (np:NavigableParents {is_interview_procedure: 'True', is_header: 'True'})
            RETURN np.navigable_parent AS navigable_parent;"""
        df = pd.DataFrame(self.cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the interview procedure list
        self.INTERV_PROC_HEADERS_LIST = df.navigable_parent.tolist()
        if not len(self.INTERV_PROC_HEADERS_LIST):
            if s.pickle_exists('INTERV_PROC_HEADERS_LIST'):
                self.INTERV_PROC_HEADERS_LIST = s.load_object('INTERV_PROC_HEADERS_LIST')
            else:
                self.INTERV_PROC_HEADERS_LIST = ['<p>COVID-19 Precaution(s):</p>']
                s.store_objects(INTERV_PROC_HEADERS_LIST=self.INTERV_PROC_HEADERS_LIST, verbose=verbose)

        # Get the corp scope headers
        cypher_str = """
            MATCH (np:NavigableParents {is_corporate_scope: 'True', is_header: 'True'})
            RETURN np.navigable_parent AS navigable_parent;"""
        df = pd.DataFrame(self.cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the corporate scope list
        self.CORP_SCOPE_HEADERS_LIST = df.navigable_parent.tolist()
        if not len(self.CORP_SCOPE_HEADERS_LIST):
            if s.pickle_exists('CORP_SCOPE_HEADERS_LIST'):
                self.CORP_SCOPE_HEADERS_LIST = s.load_object('CORP_SCOPE_HEADERS_LIST')
            else:
                self.CORP_SCOPE_HEADERS_LIST = ['<b>Careers with Optum.</b>', '<b>Why LPL?</b>', '<b>Information on Interviews:</b>', "<p>Company's website:</p>", '<b>Patients First | Innovation | Winning Culture | Heart Recovery</b>', '<b>Cogito Business Intelligence Developer, Enterprise Data &amp; Digital Health</b>']
                s.store_objects(CORP_SCOPE_HEADERS_LIST=self.CORP_SCOPE_HEADERS_LIST, verbose=verbose)

        # Get the post date headers
        cypher_str = """
            MATCH (np:NavigableParents {is_posting_date: 'True', is_header: 'True'})
            RETURN np.navigable_parent AS navigable_parent;"""
        df = pd.DataFrame(self.cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the posting date list
        self.POST_DATE_HEADERS_LIST = df.navigable_parent.tolist()
        if not len(self.POST_DATE_HEADERS_LIST):
            if s.pickle_exists('POST_DATE_HEADERS_LIST'):
                self.POST_DATE_HEADERS_LIST = s.load_object('POST_DATE_HEADERS_LIST')
            else:
                self.POST_DATE_HEADERS_LIST = ['<b>Job Posting :</b>']
                s.store_objects(POST_DATE_HEADERS_LIST=self.POST_DATE_HEADERS_LIST, verbose=verbose)
        
        # Get the other headers
        cypher_str = """
            MATCH (np:NavigableParents {is_other: 'True', is_header: 'True'})
            RETURN np.navigable_parent AS navigable_parent;"""
        df = pd.DataFrame(self.cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the other list
        self.OTHER_HEADERS_LIST = df.navigable_parent.tolist()
        if not len(self.OTHER_HEADERS_LIST):
            if s.pickle_exists('OTHER_HEADERS_LIST'):
                self.OTHER_HEADERS_LIST = s.load_object('OTHER_HEADERS_LIST')
            else:
                self.OTHER_HEADERS_LIST = ['<div>Share</div>']
                s.store_objects(OTHER_HEADERS_LIST=self.OTHER_HEADERS_LIST, verbose=verbose)
        
        # Get the parts-of-speech explanations
        cypher_str = """
            MATCH (pos:PartsOfSpeech)
            RETURN
                pos.pos_symbol AS pos_symbol,
                pos.pos_explanation AS pos_explanation;"""
        df = pd.DataFrame(self.cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the parts-of-speech dictionary
        self.POS_EXPLANATION_DICT = df.set_index('pos_symbol').pos_explanation.to_dict()
        self.POS_EXPLANATION_DICT.update({'O': 'Non-header', 'H': 'Header'})
        if not (len(self.POS_EXPLANATION_DICT.keys()) >= 14):
            if s.pickle_exists('POS_EXPLANATION_DICT'):
                self.POS_EXPLANATION_DICT = s.load_object('POS_EXPLANATION_DICT')
            else:
                self.POS_EXPLANATION_DICT = {}
                self.POS_EXPLANATION_DICT['H-TS'] = 'Task Scope Header'
                self.POS_EXPLANATION_DICT['H-RQ'] = 'Required Qualifications Header'
                self.POS_EXPLANATION_DICT['H-PQ'] = 'Preferred Qualifications Header'
                self.POS_EXPLANATION_DICT['H-LN'] = 'Legal Notifications Header'
                self.POS_EXPLANATION_DICT['H-JT'] = 'Job Title Header'
                self.POS_EXPLANATION_DICT['H-OL'] = 'Office Location Header'
                self.POS_EXPLANATION_DICT['H-JD'] = 'Job Duration Header'
                self.POS_EXPLANATION_DICT['H-SP'] = 'Supplemental Pay Header'
                self.POS_EXPLANATION_DICT['H-ER'] = 'Education Requirements Header'
                self.POS_EXPLANATION_DICT['H-IP'] = 'Interview Procedures Header'
                self.POS_EXPLANATION_DICT['H-CS'] = 'Corporate Scope Header'
                self.POS_EXPLANATION_DICT['H-PD'] = 'Post Date Header'
                self.POS_EXPLANATION_DICT['H-O'] = 'Other Header'
                self.POS_EXPLANATION_DICT['O'] = 'Non-header'
                s.store_objects(POS_EXPLANATION_DICT=self.POS_EXPLANATION_DICT, verbose=verbose)
    
    def append_parts_of_speech_list(self, navigable_parent, pos_list=[]):
        if navigable_parent in self.TASK_SCOPE_HEADERS_LIST:
            pos_list.append('H-TS')
        elif navigable_parent in self.REQ_QUALS_HEADERS_LIST:
            pos_list.append('H-RQ')
        elif navigable_parent in self.PREFF_QUALS_HEADERS_LIST:
            pos_list.append('H-PQ')
        elif navigable_parent in self.LEGAL_NOTIFS_HEADERS_LIST:
            pos_list.append('H-LN')
        elif navigable_parent in self.JOB_TITLE_HEADERS_LIST:
            pos_list.append('H-JT')
        elif navigable_parent in self.OFFICE_LOC_HEADERS_LIST:
            pos_list.append('H-OL')
        elif navigable_parent in self.JOB_DURATION_HEADERS_LIST:
            pos_list.append('H-JD')
        elif navigable_parent in self.SUPP_PAY_HEADERS_LIST:
            pos_list.append('H-SP')
        elif navigable_parent in self.EDUC_REQS_HEADERS_LIST:
            pos_list.append('H-ER')
        elif navigable_parent in self.INTERV_PROC_HEADERS_LIST:
            pos_list.append('H-IP')
        elif navigable_parent in self.CORP_SCOPE_HEADERS_LIST:
            pos_list.append('H-CS')
        elif navigable_parent in self.POST_DATE_HEADERS_LIST:
            pos_list.append('H-PD')
        elif navigable_parent in self.OTHER_HEADERS_LIST:
            pos_list.append('H-O')
        else:
            pos_list.append('O')

        return pos_list

    def get_feature_tuple(self, feature_dict, pos_lr_predict_single=None):
        feature_list = [feature_dict['initial_tag'], feature_dict['child_str']]
        is_header = feature_dict.get('is_header')
        if (is_header == True):
            if feature_dict.get('is_task_scope', False):
                feature_list.append('H-TS')
            elif feature_dict.get('is_minimum_qualification', False):
                feature_list.append('H-RQ')
            elif feature_dict.get('is_preferred_qualification', False):
                feature_list.append('H-PQ')
            elif feature_dict.get('is_legal_notification', False):
                feature_list.append('H-LN')
            elif feature_dict.get('is_job_title', False):
                feature_list.append('H-JT')
            elif feature_dict.get('is_office_location', False):
                feature_list.append('H-OL')
            elif feature_dict.get('is_job_duration', False):
                feature_list.append('H-JD')
            elif feature_dict.get('is_supplemental_pay', False):
                feature_list.append('H-SP')
            elif feature_dict.get('is_educational_requirement', False):
                feature_list.append('H-ER')
            elif feature_dict.get('is_interview_procedure', False):
                feature_list.append('H-IP')
            elif feature_dict.get('is_corporate_scope', False):
                feature_list.append('H-CS')
            elif feature_dict.get('is_posting_date', False):
                feature_list.append('H-PD')
            elif feature_dict.get('is_other', False):
                feature_list.append('H-O')
            else:
                if pos_lr_predict_single is None:
                    feature_list.append('H')
                else:
                    feature_list.append(pos_lr_predict_single(feature_dict['child_str']))
        elif (is_header == False):
            if feature_dict.get('is_task_scope', False):
                feature_list.append('O-TS')
            elif feature_dict.get('is_minimum_qualification', False):
                feature_list.append('O-RQ')
            elif feature_dict.get('is_preferred_qualification', False):
                feature_list.append('O-PQ')
            elif feature_dict.get('is_legal_notification', False):
                feature_list.append('O-LN')
            elif feature_dict.get('is_job_title', False):
                feature_list.append('O-JT')
            elif feature_dict.get('is_office_location', False):
                feature_list.append('O-OL')
            elif feature_dict.get('is_job_duration', False):
                feature_list.append('O-JD')
            elif feature_dict.get('is_supplemental_pay', False):
                feature_list.append('O-SP')
            elif feature_dict.get('is_educational_requirement', False):
                feature_list.append('O-ER')
            elif feature_dict.get('is_interview_procedure', False):
                feature_list.append('O-IP')
            elif feature_dict.get('is_corporate_scope', False):
                feature_list.append('O-CS')
            elif feature_dict.get('is_posting_date', False):
                feature_list.append('O-PD')
            elif feature_dict.get('is_other', False):
                feature_list.append('O-O')
            else:
                if pos_lr_predict_single is None:
                    feature_list.append('O')
                else:
                    feature_list.append(pos_lr_predict_single(feature_dict['child_str']))
        elif str(is_header) == 'nan':
            if pos_lr_predict_single is None:
                feature_list.append('O')
            else:
                feature_list.append(pos_lr_predict_single(feature_dict['child_str']))
        else:
            if pos_lr_predict_single is None:
                feature_list.append('O')
            else:
                feature_list.append(pos_lr_predict_single(feature_dict['child_str']))

        return tuple(feature_list)
    
    
    def get_feature_dict_list(self, child_tags_list, is_header_list, child_strs_list):
        # print('In ha.get_feature_dict_list:')
        # print(f'child_tags_list=>{child_tags_list}')
        # print(f'is_header_list=>{is_header_list}')
        # print(f'child_strs_list=>{child_strs_list}')
        sql_dict = {False: None, True: 1}
        feature_dict_list = [{'initial_tag': tag, 'is_header': is_header, 
                              'is_task_scope': sql_dict[(child_str in self.TASK_SCOPE_HEADERS_LIST)], 
                              'is_minimum_qualification': sql_dict[(child_str in self.REQ_QUALS_HEADERS_LIST)], 
                              'is_preferred_qualification': sql_dict[(child_str in self.PREFF_QUALS_HEADERS_LIST)], 
                              'is_legal_notification': sql_dict[(child_str in self.LEGAL_NOTIFS_HEADERS_LIST)], 
                              'is_job_title': sql_dict[(child_str in self.JOB_TITLE_HEADERS_LIST)], 
                              'is_office_location': sql_dict[(child_str in self.OFFICE_LOC_HEADERS_LIST)], 
                              'is_job_duration': sql_dict[(child_str in self.JOB_DURATION_HEADERS_LIST)], 
                              'is_supplemental_pay': sql_dict[(child_str in self.SUPP_PAY_HEADERS_LIST)], 
                              'is_educational_requirement': sql_dict[(child_str in self.EDUC_REQS_HEADERS_LIST)], 
                              'is_interview_procedure': sql_dict[(child_str in self.INTERV_PROC_HEADERS_LIST)], 
                              'is_corporate_scope': sql_dict[(child_str in self.CORP_SCOPE_HEADERS_LIST)], 
                              'is_posting_date': sql_dict[(child_str in self.POST_DATE_HEADERS_LIST)], 
                              'is_other': sql_dict[(child_str in self.OTHER_HEADERS_LIST)], 
                              'child_str': child_str} for tag, is_header, child_str in zip(child_tags_list, is_header_list, 
                                                                                           child_strs_list)]

        return feature_dict_list