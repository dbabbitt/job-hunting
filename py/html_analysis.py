
#!/usr/bin/env python
# coding: utf-8

from IPython.display import HTML, display
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
import numpy as np
import os
import pandas as pd
import pylab
import re

try:
    import storage
    s = storage.Storage()
except:
    from flaskr.storage import Storage
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
        if len(self.TASK_SCOPE_HEADERS_LIST):
            s.store_objects(TASK_SCOPE_HEADERS_LIST=self.TASK_SCOPE_HEADERS_LIST, verbose=verbose)
        elif s.pickle_exists('TASK_SCOPE_HEADERS_LIST'):
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
        if len(self.REQ_QUALS_HEADERS_LIST):
            s.store_objects(REQ_QUALS_HEADERS_LIST=self.REQ_QUALS_HEADERS_LIST, verbose=verbose)
        elif s.pickle_exists('REQ_QUALS_HEADERS_LIST'):
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
        if len(self.PREFF_QUALS_HEADERS_LIST):
            s.store_objects(PREFF_QUALS_HEADERS_LIST=self.PREFF_QUALS_HEADERS_LIST, verbose=verbose)
        elif s.pickle_exists('PREFF_QUALS_HEADERS_LIST'):
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
        if len(self.LEGAL_NOTIFS_HEADERS_LIST):
            s.store_objects(LEGAL_NOTIFS_HEADERS_LIST=self.LEGAL_NOTIFS_HEADERS_LIST, verbose=verbose)
        elif s.pickle_exists('LEGAL_NOTIFS_HEADERS_LIST'):
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
        if len(self.JOB_TITLE_HEADERS_LIST):
            s.store_objects(JOB_TITLE_HEADERS_LIST=self.JOB_TITLE_HEADERS_LIST, verbose=verbose)
        elif s.pickle_exists('JOB_TITLE_HEADERS_LIST'):
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
        if len(self.OFFICE_LOC_HEADERS_LIST):
            s.store_objects(OFFICE_LOC_HEADERS_LIST=self.OFFICE_LOC_HEADERS_LIST, verbose=verbose)
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
        if len(self.JOB_DURATION_HEADERS_LIST):
            s.store_objects(JOB_DURATION_HEADERS_LIST=self.JOB_DURATION_HEADERS_LIST, verbose=verbose)
        elif s.pickle_exists('JOB_DURATION_HEADERS_LIST'):
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
        if len(self.SUPP_PAY_HEADERS_LIST):
            s.store_objects(SUPP_PAY_HEADERS_LIST=self.SUPP_PAY_HEADERS_LIST, verbose=verbose)
        elif len(self.SUPP_PAY_HEADERS_LIST):
            s.store_objects(SUPP_PAY_HEADERS_LIST=self.SUPP_PAY_HEADERS_LIST, verbose=verbose)
        elif s.pickle_exists('SUPP_PAY_HEADERS_LIST'):
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
        if len(self.EDUC_REQS_HEADERS_LIST):
            s.store_objects(EDUC_REQS_HEADERS_LIST=self.EDUC_REQS_HEADERS_LIST, verbose=verbose)
        elif s.pickle_exists('EDUC_REQS_HEADERS_LIST'):
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
        if len(self.INTERV_PROC_HEADERS_LIST):
            s.store_objects(INTERV_PROC_HEADERS_LIST=self.INTERV_PROC_HEADERS_LIST, verbose=verbose)
        elif s.pickle_exists('INTERV_PROC_HEADERS_LIST'):
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
        if len(self.CORP_SCOPE_HEADERS_LIST):
            s.store_objects(CORP_SCOPE_HEADERS_LIST=self.CORP_SCOPE_HEADERS_LIST, verbose=verbose)
        elif s.pickle_exists('CORP_SCOPE_HEADERS_LIST'):
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
        if len(self.POST_DATE_HEADERS_LIST):
            s.store_objects(POST_DATE_HEADERS_LIST=self.POST_DATE_HEADERS_LIST, verbose=verbose)
        elif s.pickle_exists('POST_DATE_HEADERS_LIST'):
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
        if len(self.OTHER_HEADERS_LIST):
            s.store_objects(OTHER_HEADERS_LIST=self.OTHER_HEADERS_LIST, verbose=verbose)
        elif s.pickle_exists('OTHER_HEADERS_LIST'):
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
        if len(self.POS_EXPLANATION_DICT.keys()) >= 14:
            s.store_objects(POS_EXPLANATION_DICT=self.POS_EXPLANATION_DICT, verbose=verbose)
        elif s.pickle_exists('POS_EXPLANATION_DICT'):
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
        is_header = feature_dict['is_header']
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

class HeaderAnalysis(object):
    """Header analysis class."""

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.HTML_SCANNER_REGEX = re.compile(r'</?\w+|\w+[#\+]*|:|\.|\?')
        self.LT_REGEX = re.compile(r'\s+<')
        self.GT_REGEX = re.compile(r'>\s+')
        self.CLF_NAME = 'LogisticRegression'
        self.SAVES_HTML_FOLDER = os.path.join(s.saves_folder, 'html')
        self.CMAP = pylab.cm.get_cmap('coolwarm')
        if s.pickle_exists('CHILDLESS_TAGS_LIST'):
            self.CHILDLESS_TAGS_LIST = s.load_object('CHILDLESS_TAGS_LIST')
        else:
            self.CHILDLESS_TAGS_LIST = ['template', 'script']
            s.store_objects(CHILDLESS_TAGS_LIST=self.CHILDLESS_TAGS_LIST)
        if s.pickle_exists('NAVIGABLE_PARENT_IS_HEADER_DICT'):
            self.NAVIGABLE_PARENT_IS_HEADER_DICT = s.load_object('NAVIGABLE_PARENT_IS_HEADER_DICT')
        else:
            assert False, "You're in deep doodoo: you lost your basic tags dictionary"
            self.NAVIGABLE_PARENT_IS_HEADER_DICT = {}
            s.store_objects(NAVIGABLE_PARENT_IS_HEADER_DICT=self.NAVIGABLE_PARENT_IS_HEADER_DICT)
        if s.pickle_exists('NAVIGABLE_PARENT_IS_QUAL_DICT'):
            self.NAVIGABLE_PARENT_IS_QUAL_DICT = s.load_object('NAVIGABLE_PARENT_IS_QUAL_DICT')
        else:
            self.NAVIGABLE_PARENT_IS_QUAL_DICT = {}
            s.store_objects(NAVIGABLE_PARENT_IS_QUAL_DICT=self.NAVIGABLE_PARENT_IS_QUAL_DICT)

    def html_regex_tokenizer(self, corpus):

        return [match.group() for match in re.finditer(self.HTML_SCANNER_REGEX, corpus)]

    def clean_html_str(self, html_obj):
        html_str = str(html_obj)
        html_str = html_str.strip()
        html_str = self.LT_REGEX.sub('<', html_str)
        html_str = self.GT_REGEX.sub('>', html_str)

        return html_str

    def store_unique_list(self, list_name, tag_str):
        if s.pickle_exists(list_name):
            list_obj = s.load_object(list_name)
        else:
            list_obj = []
        list_obj.append(tag_str)
        list_obj = list(set(list_obj))
        s.store_objects(**{list_name: list_obj})

    def store_true_or_false_dictionary(self, dict_name, tag_str, true_or_false=False):
        if s.pickle_exists(dict_name):
            dict_obj = s.load_object(dict_name)
        else:
            dict_obj = {}
        dict_obj[tag_str] = true_or_false
        s.store_objects(**{dict_name: dict_obj})

    def get_navigable_children(self, tag, result_list=[]):
        if (type(tag) is not NavigableString):
            if hasattr(tag, 'children'):
                for child_tag in tag.children:
                    result_list = self.get_navigable_children(child_tag, result_list)
            elif tag.name is not None:
                self.store_unique_list('CHILDLESS_TAGS_LIST', tag.name)
        else:
            base_str = self.clean_html_str(tag)
            if re.search('[\r\n]+', base_str):
                for line_str in re.split('[\r\n]+', base_str, 0):
                    result_list.append(line_str.strip())
            elif base_str:
                tag_str = self.clean_html_str(tag.parent)
                if tag_str.count('<') > 2:
                    tag_str = base_str
                result_list.append(tag_str)

        return result_list

    def get_body_soup(self, html_str):
        page_soup = BeautifulSoup(html_str, 'lxml')
        body_soup = page_soup.find_all(name='body')[0]
        for tag in self.CHILDLESS_TAGS_LIST:
            for s in body_soup.select(tag):
                s.extract()

        return body_soup

    def get_child_strs_from_file(self, file_name):
        child_strs_list = []
        file_path = os.path.join(self.SAVES_HTML_FOLDER, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                html_str = f.read()
                body_soup = self.get_body_soup(html_str)
                child_strs_list = self.get_navigable_children(body_soup, [])
            except UnicodeDecodeError as e:
                print(f'UnicodeDecodeError error in {file_path}: {str(e).strip()}')
            except Exception as e:
                print(f'{e.__class__} error in {file_path}: {str(e).strip()}')

        return child_strs_list

    def html2text(self, html_str, prob_float):
        html_str = html_str.replace('<', '&lt;').replace('>', '&gt;')
        hex_str = '%02x%02x%02x' % self.CMAP(X=prob_float, bytes=True)[:-1]
        html_str = f'<span style="color:#{hex_str}">{html_str}</span>'

        return html_str

    def get_child_tags_list(self, child_strs_list):
        child_tags_list = []
        for navigable_parent in child_strs_list:
            tokenized_sent = self.html_regex_tokenizer(navigable_parent)
            try:
                first_token = tokenized_sent[0]
                if first_token[0] == '<':
                    child_tags_list.append(first_token[1:])
                else:
                    child_tags_list.append('plaintext')
            except:
                child_tags_list.append('plaintext')

        return child_tags_list

    def get_is_header_list(self, child_strs_list):
        is_header_list = []
        for navigable_parent in child_strs_list:
            if navigable_parent in self.NAVIGABLE_PARENT_IS_HEADER_DICT:
                is_header = self.NAVIGABLE_PARENT_IS_HEADER_DICT[navigable_parent]
            else:
                is_header = None
            is_header_list.append(is_header)

        return is_header_list

class LdaUtilities(object):
    """Latent Dirichlet Allocation utilities class."""

    def __init__(self, ha=None, hc=None, cu=None, verbose=False):
        if ha is None:
            self.ha = HeaderAnalysis()
        else:
            self.ha = ha
        if hc is None:
            self.hc = HeaderCategories()
        else:
            self.hc = hc
        if cu is None:
            import cypher_utils
            self.cu = cypher_utils.CypherUtilities()
        else:
            self.cu = cu
        self.verbose = verbose

        # Build the LDA elements
        if not s.pickle_exists('NAVIGABLE_PARENT_IS_HEADER_DICT'):
            self.cu.build_child_strs_list_dictionary(verbose=verbose)
        self.NAVIGABLE_PARENT_IS_HEADER_DICT = s.load_object('NAVIGABLE_PARENT_IS_HEADER_DICT')
        self.stopwords_list = ['U', 'A', 'S', 'a', '1', 'u', 's', 'to', 'my', 'by', 'an', 'we', '00', 'or', 'as', 're', 'in', 'be', 'on', 'of', 'do', 'is', '19', 'any', 'out', 'for', 'the', 'are', 'and', 'long', 'each', 'have', 'with', 'more', 'will', 'into', 'that', 'this', 'your', 'from', 'their', 'class', 'about', 'other', 'place', '.']
        self.tokenized_sents_list = self.get_tokenized_sents_list()

        if s.pickle_exists('LDA_DICTIONARY'):
            self.LDA_DICTIONARY = s.load_object('LDA_DICTIONARY')
        else:
            self.build_dictionary(verbose=verbose)

        if s.pickle_exists('LDA_CORPUS'):
            self.LDA_CORPUS = s.load_object('LDA_CORPUS')
        else:
            self.build_corpus(verbose=verbose)

        if s.pickle_exists('TOPIC_MODEL'):
            self.TOPIC_MODEL = s.load_object('TOPIC_MODEL')
            # You'll have to eyeball this to get the dictionary correct
            self.topic_dict = {0: 'O', 1: 'H'}
        else:
            self.build_topic_model(verbose=verbose)
            self.topic_dict = {}
        
        if s.pickle_exists('HEADERS_DICTIONARY'):
            self.HEADERS_DICTIONARY = s.load_object('HEADERS_DICTIONARY')
        else:
            self.build_headers_dictionary()
        
        if s.pickle_exists('HEADERS_CORPUS'):
            self.HEADERS_CORPUS = s.load_object('HEADERS_CORPUS')
        else:
            self.build_headers_corpus()
        
        if s.pickle_exists('HEADERS_TOPIC_MODEL'):
            self.HEADERS_TOPIC_MODEL = s.load_object('HEADERS_TOPIC_MODEL')
            # You'll have to eyeball this to get the dictionary correct
            topic_dict = {0: 'O-SP', 1: 'O-TS', 2: 'O-SP'}
        else:
            self.build_lda()
            topic_dict = {}
        
        self.lda_predict_single = self.build_lda_predict_single()
        self.lda_predict_percent = self.build_lda_predict_percent()

    ###########################################
    ## Latent Dirichlet Allocation functions ##
    ###########################################

    def get_tokenized_sents_list(self):

        # Build model with tokenized words
        sents_list = list(self.NAVIGABLE_PARENT_IS_HEADER_DICT.keys())
        tokenized_sents_list = [self.ha.html_regex_tokenizer(sent_str) for sent_str in sents_list]

        # Remove stop words
        for i in reversed(range(len(tokenized_sents_list))):
            for j in reversed(range(len(tokenized_sents_list[i]))):
                if tokenized_sents_list[i][j] in self.stopwords_list:
                    del tokenized_sents_list[i][j]

        return tokenized_sents_list

    def build_dictionary(self, verbose=False):

        # Create a corpus from a list of texts
        from gensim.corpora.dictionary import Dictionary
        self.LDA_DICTIONARY = Dictionary(self.tokenized_sents_list)
        self.LDA_DICTIONARY.filter_extremes(no_below=100, no_above=0.5, keep_n=8_500, keep_tokens=[':', '<b', '</b'])
        s.store_objects(LDA_DICTIONARY=self.LDA_DICTIONARY, verbose=verbose)

    def build_headers_dictionary(self):
        
        # Create a corpus from a list of texts
        tokenized_sents_list = self.get_tokenized_sents_list()
        from gensim.corpora.dictionary import Dictionary
        self.HEADERS_DICTIONARY = Dictionary(tokenized_sents_list)
        # self.HEADERS_DICTIONARY.filter_extremes(no_below=5, no_above=0.5, keep_n=100000, keep_tokens=None)
        s.store_objects(HEADERS_DICTIONARY=self.HEADERS_DICTIONARY)

    def build_corpus(self, verbose=False):

        # Create a corpus from a list of texts
        self.LDA_CORPUS = [self.LDA_DICTIONARY.doc2bow(tag_str) for tag_str in self.tokenized_sents_list]

        s.store_objects(LDA_CORPUS=self.LDA_CORPUS, verbose=verbose)

    def build_headers_corpus(self, verbose=False):
        
        # Create a corpus from a list of texts
        tokenized_sents_list = self.get_tokenized_sents_list()
        self.HEADERS_CORPUS = [self.HEADERS_DICTIONARY.doc2bow(tag_str) for tag_str in tokenized_sents_list]
        
        s.store_objects(HEADERS_CORPUS=self.HEADERS_CORPUS, verbose=verbose)

    def build_topic_model(self, num_topics=2, chunksize=50, passes=75, alpha=None, decay=0.6, iterations=29, gamma_threshold=1e-10, 
                          minimum_probability=0.001, verbose=False):

        # Train the model on the corpus
        id2word = {v: k for k, v in self.LDA_DICTIONARY.token2id.items()}
        if num_topics is None:
            num_topics = self.get_pos_count(verbose=verbose)

        # Get ratio of headers to non-headers
        if alpha is None:
            import numpy as np
            cypher_str = """
                MATCH (np:NavigableParents {is_header: 'True'})
                RETURN COUNT(np.navigable_parent) AS header_count;"""
            is_header_df = pd.DataFrame(self.cu.get_execution_results(self.cursor, cypher_str))
            header_count = is_header_df.header_count.squeeze()
            cypher_str = """
                MATCH (np:NavigableParents {is_header: 'False'})
                RETURN COUNT(np.navigable_parent) AS nonheader_count;"""
            is_nonheader_df = pd.DataFrame(self.cu.get_execution_results(self.cursor, cypher_str))
            nonheader_count = is_nonheader_df.nonheader_count.squeeze()
            nonheader_fraction = nonheader_count/(header_count + nonheader_count)
            header_fraction = header_count/(header_count + nonheader_count)
            alpha = np.array([nonheader_fraction, header_fraction], dtype=np.float32)

        from gensim.models.ldamodel import LdaModel
        self.TOPIC_MODEL = LdaModel(corpus=self.LDA_CORPUS, num_topics=num_topics, id2word=id2word, chunksize=chunksize, passes=passes, 
                                    alpha=alpha, decay=decay, iterations=iterations, gamma_threshold=gamma_threshold, 
                                    minimum_probability=minimum_probability)
        s.store_objects(TOPIC_MODEL=self.TOPIC_MODEL, verbose=verbose)

    def build_lda(self, verbose=False):
        
        # Get the parts-of-speech count to use as number of topics
        cypher_str = '''
            MATCH (pos:PartsOfSpeech)
            UNWIND pos.pos_symbol as s
            RETURN count(DISTINCT s) AS num_topics;'''
        num_topics = self.cu.get_execution_results(cypher_str, verbose=verbose)[0]['num_topics']
        
        # Train the model on the corpus
        id2word = {v: k for k, v in self.HEADERS_DICTIONARY.token2id.items()}
        from gensim.models.ldamodel import LdaModel
        self.HEADERS_TOPIC_MODEL = LdaModel(corpus=self.HEADERS_CORPUS, num_topics=num_topics, id2word=id2word, passes=4, 
                                            alpha='auto', eta='auto')
        s.store_objects(HEADERS_TOPIC_MODEL=self.HEADERS_TOPIC_MODEL)

    def build_lda_predict_single(self):

        # Define a predictor
        def lda_predict_single(sent_str):
            tokens_list = self.ha.html_regex_tokenizer(sent_str)
            X_test = self.LDA_DICTIONARY.doc2bow(tokens_list)
            result_list = sorted(self.TOPIC_MODEL[X_test], key=lambda x: x[1], reverse=False)
            topic_number = result_list[0][0]

            return self.topic_dict[topic_number]

        return lda_predict_single

    def build_lda_predict_percent(self):
        
        # Define a predictor
        def predict_percent_fit(navigable_parent):
            X_test = self.HEADERS_DICTIONARY.doc2bow(self.ha.html_regex_tokenizer(navigable_parent))
            result_list = self.HEADERS_TOPIC_MODEL[X_test]
            result_list = sorted(result_list, key=lambda x: x[1], reverse=True)
            result_tuple = result_list[0]

            # Just return the topic number
            y_predict_proba = result_tuple[0]

            return y_predict_proba
        
        return predict_percent_fit

    def get_pos_count(self, verbose=False):

        # Get the parts-of-speech count to use as number of topics
        cypher_str = 'SELECT pos_symbol, pos_explanation FROM PartsOfSpeech'
        pos_df = pd.DataFrame(self.cu.get_execution_results(cypher_str, verbose=False))
        cypher_prefix = """
                MATCH (np:NavigableParents {is_header: '"""
        self.pos_symbols_list = []
        for pos_symbol in pos_df.pos_symbol:
            if pos_symbol.startswith('H-'):
                cypher_str = cypher_prefix + "True', "
            elif pos_symbol.startswith('O-'):
                cypher_str = cypher_prefix + "False', "
            if pos_symbol.endswith('-TS'):
                cypher_str += "is_task_scope: 'True'"
            elif pos_symbol.endswith('-RQ'):
                cypher_str += "is_minimum_qualification]: 'True'"
            elif pos_symbol.endswith('-PQ'):
                cypher_str += "is_preferred_qualification]: 'True'"
            elif pos_symbol.endswith('-LN'):
                cypher_str += "is_legal_notification]: 'True'"
            elif pos_symbol.endswith('-JT'):
                cypher_str += "is_job_title]: 'True'"
            elif pos_symbol.endswith('-OL'):
                cypher_str += "is_office_location]: 'True'"
            elif pos_symbol.endswith('-JD'):
                cypher_str += "is_job_duration]: 'True'"
            elif pos_symbol.endswith('-SP'):
                cypher_str += "is_supplemental_pay]: 'True'"
            elif pos_symbol.endswith('-ER'):
                cypher_str += "is_educational_requirement]: 'True'"
            elif pos_symbol.endswith('-IP'):
                cypher_str += "is_interview_procedure]: 'True'"
            elif pos_symbol.endswith('-CS'):
                cypher_str += "is_corporate_scope]: 'True'"
            elif pos_symbol.endswith('-PD'):
                cypher_str += "is_posting_date]: 'True'"
            elif pos_symbol.endswith('-O'):
                cypher_str += "is_other]: 'True'"
            cypher_str += '})\nRETURN COUNT(np) AS row_count'
            count_df = pd.DataFrame(self.cu.get_execution_results(cypher_str, verbose=False))
            if count_df.row_count.squeeze() > 0:
                self.pos_symbols_list.append(pos_symbol)
        num_topics = len(self.pos_symbols_list)

        return num_topics

class CrfUtilities(object):
    """Conditional Random Fields utilities class."""

    def __init__(self, ha=None, hc=None, cu=None, verbose=False):
        if ha is None:
            self.ha = HeaderAnalysis()
        else:
            self.ha = ha
        if hc is None:
            self.hc = HeaderCategories()
        else:
            self.hc = hc
        if cu is None:
            import cypher_utils
            self.cu = cypher_utils.CypherUtilities()
        else:
            self.cu = cu
        self.verbose = verbose
        self.document_structure_elements_set = set(['body', 'head', 'html'])
        self.document_head_elements_set = set(['base', 'basefont', 'isindex', 'link', 'meta', 'object', 'script', 'style', 'title'])
        self.document_body_elements_set = set(['a', 'abbr', 'acronym', 'address', 'applet', 'area', 'article', 'aside', 'audio', 'b', 'bdi', 'bdo', 'big', 'blockquote', 'br', 'button', 'canvas', 'caption', 'center', 'cite', 'code', 'col', 'colgroup', 'data', 'datalist', 'dd', 'del', 'dfn', 'dir', 'div', 'dl', 'dt', 'em', 'embed', 'fieldset', 'figcaption', 'figure', 'font', 'footer', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header', 'hr', 'i', 'img', 'input', 'ins', 'isindex', 'kbd', 'keygen', 'label', 'legend', 'li', 'main', 'map', 'mark', 'menu', 'meter', 'nav', 'noscript', 'object', 'ol', 'optgroup', 'option', 'output', 'p', 'param', 'pre', 'progress', 'q', 'rb', 'rp', 'rt', 'rtc', 'ruby', 's', 'samp', 'script', 'section', 'select', 'small', 'source', 'span', 'strike', 'strong', 'sub', 'sup', 'table', 'tbody', 'td', 'template', 'textarea', 'tfoot', 'th', 'thead', 'time', 'tr', 'track', 'tt', 'u', 'ul', 'var', 'video', 'wbr'])
        self.block_elements_set = set(['address', 'article', 'aside', 'blockquote', 'center', 'dd', 'del', 'dir', 'div', 'dl', 'dt', 'figcaption', 'figure', 'footer', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header', 'hr', 'ins', 'li', 'main', 'menu', 'nav', 'noscript', 'ol', 'p', 'pre', 'script', 'section', 'ul'])
        self.basic_text_set = set(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p'])
        self.section_headings_set = set(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        self.lists_set = set(['dd', 'dir', 'dl', 'dt', 'li', 'ol', 'ul'])
        self.other_block_elements_set = set(['address', 'article', 'aside', 'blockquote', 'center', 'del', 'div', 'figcaption', 'figure', 'footer', 'header', 'hr', 'ins', 'main', 'menu', 'nav', 'noscript', 'pre', 'script', 'section'])
        self.inline_elements_set = set(['a', 'abbr', 'acronym', 'b', 'bdi', 'bdo', 'big', 'br', 'cite', 'code', 'data', 'del', 'dfn', 'em', 'font', 'i', 'ins', 'kbd', 'mark', 'q', 'rb', 'rp', 'rt', 'rtc', 'ruby', 's', 'samp', 'script', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'template', 'time', 'tt', 'u', 'var', 'wbr'])
        self.anchor_set = set(['a'])
        self.phrase_elements_set = set(['abbr', 'acronym', 'b', 'big', 'code', 'dfn', 'em', 'font', 'i', 'kbd', 's', 'samp', 'small', 'strike', 'strong', 'tt', 'u', 'var'])
        self.general_set = set(['abbr', 'acronym', 'dfn', 'em', 'strong'])
        self.computer_phrase_elements_set = set(['code', 'kbd', 'samp', 'var'])
        self.presentation_set = set(['b', 'big', 'font', 'i', 's', 'small', 'strike', 'tt', 'u'])
        self.span_set = set(['span'])
        self.other_inline_elements_set = set(['bdi', 'bdo', 'br', 'cite', 'data', 'del', 'ins', 'mark', 'q', 'rb', 'rp', 'rt', 'rtc', 'ruby', 'script', 'sub', 'sup', 'template', 'time', 'wbr'])
        self.images_and_objects_set = set(['applet', 'area', 'audio', 'canvas', 'embed', 'img', 'map', 'object', 'param', 'source', 'track', 'video'])
        self.forms_set = set(['button', 'datalist', 'fieldset', 'form', 'input', 'isindex', 'keygen', 'label', 'legend', 'meter', 'optgroup', 'option', 'output', 'progress', 'select', 'textarea'])
        self.tables_set = set(['caption', 'col', 'colgroup', 'table', 'tbody', 'td', 'tfoot', 'th', 'thead', 'tr'])
        self.frames_set = set(['frame', 'frameset', 'iframe', 'noframes'])
        self.historic_elements_set = set(['listing', 'nextid', 'plaintext', 'xmp'])
        self.non_standard_elements_set = set(['blink', 'layer', 'marquee', 'nobr', 'noembed'])

        # Build the CRF elements
        if s.pickle_exists('CRF'):
            self.CRF = s.load_object('CRF')
        else:
            import sklearn_crfsuite
            self.CRF = sklearn_crfsuite.CRF(algorithm='lbfgs', c1=0.1, c2=0.1, max_iterations=100, all_possible_transitions=True)
            HEADER_PATTERN_DICT = s.load_object('HEADER_PATTERN_DICT')
            X_train = []
            y_train = []
            for file_name, feature_dict_list in HEADER_PATTERN_DICT.items():
                feature_tuple_list = [self.hc.get_feature_tuple(feature_dict) for feature_dict in feature_dict_list]
                pos_list = [feature_tuple[2] for feature_tuple in feature_tuple_list]
                y_train.append(pos_list)
                X_train.append(self.sent2features(feature_tuple_list))
            try:
                self.CRF.fit(X_train, y_train)
            except Exception as e:
                print(f'Error in CrfUtilities init trying to self.CRF.fit(X_train, y_train): {str(e).strip()}')
                with open('../saves/txt/X_train.txt', 'w', encoding='utf-8') as f:
                    print(X_train, file=f)
                with open('../saves/txt/y_train.txt', 'w', encoding='utf-8') as f:
                    print(y_train, file=f)
                raise
            s.store_objects(CRF=self.CRF, verbose=verbose)

    #########################################
    ## Conditional Random Fields functions ##
    #########################################


    def word2features(self, sent, i):
        from itertools import groupby
        if not hasattr(self, 'lu'):
            self.lu = LrUtilities(ha=self.ha, hc=self.hc, cu=self.cu, verbose=self.verbose)
        null_element = 'plaintext'
        this_sent = sent[i]
        tag = this_sent[0]
        child_str = this_sent[1]
        postag = this_sent[2]

        features = {
            'bias': 1.0, 
            'child_str.pos_lr_predict_single': self.lu.pos_lr_predict_single(child_str), 
            'position': i+1, 
            'postag': postag, 
            'tag.basic_text_set': tag in self.basic_text_set, 
            'tag.block_elements_set': tag in self.block_elements_set, 
            'tag.document_body_elements_set': tag in self.document_body_elements_set, 
            'tag.inline_elements_set': tag in self.inline_elements_set, 
            'tag.lists_set': tag in self.lists_set, 
            'tag.null_element': tag == null_element, 
            'tag.other_block_elements_set': tag in self.other_block_elements_set, 
            'tag.phrase_elements_set': tag in self.phrase_elements_set, 
            'tag.presentation_set': tag in self.presentation_set, 
            'tag.section_headings_set': tag in self.section_headings_set, 
        }
        if i > 0:
            tag1 = sent[i-1][0]
            postag1 = sent[i-1][2]
            features.update({
                '-1:postag': postag1, 
                '-1:previous==tag': tag1 == tag, 
                '-1:tag.basic_text_set': tag1 in self.basic_text_set, 
                '-1:tag.block_elements_set': tag1 in self.block_elements_set, 
                '-1:tag.document_body_elements_set': tag1 in self.document_body_elements_set, 
                '-1:tag.inline_elements_set': tag1 in self.inline_elements_set, 
                '-1:tag.lists_set': tag1 in self.lists_set, 
                '-1:tag.null_element': tag1 == null_element, 
                '-1:tag.other_block_elements_set': tag1 in self.other_block_elements_set, 
                '-1:tag.phrase_elements_set': tag1 in self.phrase_elements_set, 
                '-1:tag.presentation_set': tag1 in self.presentation_set, 
                '-1:tag.section_headings_set': tag1 in self.section_headings_set, 
            })
        else:
            features['BOS'] = True

        if i < len(sent)-1:
            tag1 = sent[i+1][0]
            postag1 = sent[i+1][2]
            features.update({
                '+1:postag': postag1, 
                '+1:tag.basic_text_set': tag1 in self.basic_text_set, 
                '+1:tag.block_elements_set': tag1 in self.block_elements_set, 
                '+1:tag.document_body_elements_set': tag1 in self.document_body_elements_set, 
                '+1:tag.inline_elements_set': tag1 in self.inline_elements_set, 
                '+1:tag.lists_set': tag1 in self.lists_set, 
                '+1:tag.null_element': tag1 == null_element, 
                '+1:tag.other_block_elements_set': tag1 in self.other_block_elements_set, 
                '+1:tag.phrase_elements_set': tag1 in self.phrase_elements_set, 
                '+1:tag.presentation_set': tag1 in self.presentation_set, 
                '+1:tag.section_headings_set': tag1 in self.section_headings_set, 
                '+1:tag==previous': tag1 == tag, 
            })
        else:
            features['EOS'] = True

        if i < len(sent)-2:
            tag1 = sent[i+1][0]
            tag2 = sent[i+2][0]
            postag2 = sent[i+2][2]
            labels_list = self.sent2labels(sent)[i:]
            consecutives_list = []
            for k, v in groupby(labels_list):
                consecutives_list.append((k, len(list(v))))
            if (consecutives_list[0][1] > 1):
                consecutive_next_tags = 0
            else:
                consecutive_next_tags = consecutives_list[1][1]
            features.update({
                '+2:postag': postag2, 
                '+2:tag.basic_text_set': tag2 in self.basic_text_set, 
                '+2:tag.block_elements_set': tag2 in self.block_elements_set, 
                '+2:tag.document_body_elements_set': tag2 in self.document_body_elements_set, 
                '+2:tag.inline_elements_set': tag2 in self.inline_elements_set, 
                '+2:tag.lists_set': tag2 in self.lists_set, 
                '+2:tag.null_element': tag2 == null_element, 
                '+2:tag.other_block_elements_set': tag2 in self.other_block_elements_set, 
                '+2:tag.phrase_elements_set': tag2 in self.phrase_elements_set, 
                '+2:tag.presentation_set': tag2 in self.presentation_set, 
                '+2:tag.section_headings_set': tag2 in self.section_headings_set, 
                '+2:tag==previous': tag2 == tag1, 
                'tag.consecutive_next_tags': consecutive_next_tags, 
            })

        if i < len(sent)-3:
            tag2 = sent[i+2][0]
            tag3 = sent[i+3][0]
            postag3 = sent[i+3][2]
            features.update({
                '+3:postag': postag3, 
                '+3:tag.basic_text_set': tag3 in self.basic_text_set, 
                '+3:tag.block_elements_set': tag3 in self.block_elements_set, 
                '+3:tag.document_body_elements_set': tag3 in self.document_body_elements_set, 
                '+3:tag.inline_elements_set': tag3 in self.inline_elements_set, 
                '+3:tag.lists_set': tag3 in self.lists_set, 
                '+3:tag.null_element': tag3 == null_element, 
                '+3:tag.other_block_elements_set': tag3 in self.other_block_elements_set, 
                '+3:tag.phrase_elements_set': tag3 in self.phrase_elements_set, 
                '+3:tag.presentation_set': tag3 in self.presentation_set, 
                '+3:tag.section_headings_set': tag3 in self.section_headings_set, 
                '+3:tag==previous': tag3 == tag2, 
            })

        return features

    def sent2features(self, sent):

        return [self.word2features(sent, i) for i in range(len(sent))]

    def sent2labels(self, sent):

        return [label for token, child_str, label in sent]

    def sent2tokens(self, sent):

        return [token for token, child_str, label in sent]

class LrUtilities(object):
    """Logistic Regression utilities class."""

    def __init__(self, ha=None, hc=None, cu=None, verbose=False):
        if ha is None:
            self.ha = HeaderAnalysis()
        else:
            self.ha = ha
        if hc is None:
            self.hc = HeaderCategories()
        else:
            self.hc = hc
        if cu is None:
            import cypher_utils
            self.cu = cypher_utils.CypherUtilities()
        else:
            self.cu = cu
        self.verbose = verbose

        # Build the Logistic Regression elements
        self.build_pos_logistic_regression_elements()
        self.build_isheader_logistic_regression_elements()

    ###################################
    ## Logistic Regression functions ##
    ###################################
    def build_pos_logistic_regression_elements(self, verbose=False):
        self.POS_LR_DICT = {}
        self.POS_PREDICT_PERCENT_FIT_DICT = {}

        # Train a model for each labeled POS symbol
        cypher_str = """
            MATCH (pos:PartsOfSpeech)-[r:SUMMARIZES]->(np:NavigableParents)
            RETURN
                np.navigable_parent AS navigable_parent, 
                pos.pos_symbol AS pos_symbol;"""
        pos_df = pd.DataFrame(self.cu.get_execution_results(cypher_str, verbose=verbose))

        # The shape of the Bag-of-words count vector here should be n html strings * m unique tokens
        sents_list = pos_df.navigable_parent.tolist()
        pos_symbol_list = pos_df.pos_symbol.unique().tolist()

        # Re-transform the bag-of-words and tf-idf from the new manual scores
        if s.pickle_exists('POS_CV'):
            try:
                self.POS_CV = s.load_object('POS_CV')
            except:
                self.POS_CV = CountVectorizer(analyzer='word', binary=False, decode_error='strict', lowercase=False, max_df=1.0,
                                              max_features=None, min_df=0.0, ngram_range=(1, 5), stop_words=None,
                                              strip_accents='ascii', tokenizer=ha.html_regex_tokenizer)
                s.store_objects(POS_CV=self.POS_CV)
        else:
            self.POS_CV = CountVectorizer(analyzer='word', binary=False, decode_error='strict', lowercase=False, max_df=1.0,
                                          max_features=None, min_df=0.0, ngram_range=(1, 5), stop_words=None,
                                          strip_accents='ascii', tokenizer=self.ha.html_regex_tokenizer)
            s.store_objects(POS_CV=self.POS_CV)
        bow_matrix = self.POS_CV.fit_transform(sents_list)

        # Tf-idf must get from Bag-of-words first
        if s.pickle_exists('POS_TT'):
            self.POS_TT = s.load_object('POS_TT')
        else:
            self.POS_TT = TfidfTransformer(norm='l1', smooth_idf=True, sublinear_tf=False, use_idf=True)
            s.store_objects(POS_TT=self.POS_TT)
        tfidf_matrix = self.POS_TT.fit_transform(bow_matrix)
        X = tfidf_matrix.toarray()

        for pos_symbol in pos_symbol_list:

            # Train the classifier
            mask_series = (pos_df.pos_symbol == pos_symbol)
            y = mask_series.to_numpy()
            if pos_symbol not in self.POS_LR_DICT:
                self.POS_LR_DICT[pos_symbol] = LogisticRegression(C=375.0, class_weight='balanced', dual=False, 
                                                              fit_intercept=True, intercept_scaling=1, 
                                                              l1_ratio=None, max_iter=1000, 
                                                              multi_class='auto', n_jobs=None, penalty='l1', 
                                                              random_state=None, solver='liblinear', 
                                                              tol=0.0001, verbose=verbose, warm_start=False)
            try:
                self.POS_LR_DICT[pos_symbol].fit(X, y)
                self.POS_PREDICT_PERCENT_FIT_DICT[pos_symbol] = self.build_pos_lr_predict_percent(pos_symbol, verbose=verbose)
            except ValueError as e:
                print(f'Fitting {pos_symbol} had this error: {str(e).strip()}')
                self.POS_LR_DICT.pop(pos_symbol, None)
                self.POS_PREDICT_PERCENT_FIT_DICT.pop(pos_symbol, None)
    
    def build_isheader_logistic_regression_elements(self, verbose=False):
        if s.pickle_exists('ISHEADER_CV'):
            try:
                self.ISHEADER_CV = s.load_object('ISHEADER_CV')
            except:
                self.ISHEADER_CV = CountVectorizer(analyzer='word', binary=False, decode_error='strict', lowercase=False, max_df=1.0,
                                              max_features=None, min_df=0.0, ngram_range=(1, 5), stop_words=None,
                                              strip_accents='ascii', tokenizer=ha.html_regex_tokenizer)
                s.store_objects(ISHEADER_CV=self.ISHEADER_CV)
        else:
            self.ISHEADER_CV = CountVectorizer(analyzer='word', binary=False, decode_error='strict', lowercase=False, max_df=1.0,
                                          max_features=None, min_df=0.0, ngram_range=(1, 5), stop_words=None,
                                          strip_accents='ascii', tokenizer=self.ha.html_regex_tokenizer)
            s.store_objects(ISHEADER_CV=self.ISHEADER_CV)
        if s.pickle_exists('ISHEADER_TT'):
            self.ISHEADER_TT = s.load_object('ISHEADER_TT')
        else:
            self.ISHEADER_TT = TfidfTransformer(norm='l1', smooth_idf=True, sublinear_tf=False, use_idf=True)
            s.store_objects(ISHEADER_TT=self.ISHEADER_TT)
        if s.pickle_exists('ISHEADER_LR'):
            self.ISHEADER_LR = s.load_object('ISHEADER_LR')
        else:
            self.ISHEADER_LR = LogisticRegression(
                C=375.0, 
                class_weight='balanced', 
                dual=False, 
                fit_intercept=True, 
                intercept_scaling=1, 
                l1_ratio=None, 
                max_iter=1000, 
                multi_class='auto', 
                n_jobs=None, 
                penalty='l1', 
                random_state=None, 
                solver='liblinear', 
                tol=0.0001, 
                verbose=0, 
                warm_start=False)
            
            # Train a model
            cypher_str = """
                MATCH (np:NavigableParents)
                RETURN
                    np.navigable_parent AS navigable_parent, 
                    np.is_header AS is_header;"""
            np_df = pd.DataFrame(self.cu.get_execution_results(cypher_str, verbose=verbose))
            np_df.is_header = np_df.is_header.astype('bool')

            # The shape of the Bag-of-words count vector here should be n html strings * m unique tokens
            sents_list = np_df.navigable_parent.tolist()

            # Re-transform the bag-of-words and tf-idf from the new manual scores
            bow_matrix = self.ISHEADER_CV.fit_transform(sents_list)

            # Tf-idf must get from Bag-of-words first
            tfidf_matrix = self.ISHEADER_TT.fit_transform(bow_matrix)
            
            # Re-train the classifier
            if verbose:
                print('Attempting to re-train the is_header classifier')
            y = np_df.is_header.values
            try:
                import gc
                
                gc.collect()
                X = tfidf_matrix.toarray()
            except Exception as e:
                print(f'Got this {e.__class__} error in build_isheader_logistic_regression_elements trying ' +
                'to turn the is_header TF-IDF matrix into a normal array: {str(e).strip()}')
                X = tfidf_matrix
            self.ISHEADER_LR.fit(X, y)
            s.store_objects(ISHEADER_LR=self.ISHEADER_LR)
            
        self.ISHEADER_PREDICT_PERCENT_FIT = self.build_isheader_lr_predict_percent(verbose=verbose)
    
    def pos_lr_predict_single(self, html_str, verbose=False):
        tuple_list = []
        for pos_symbol, predict_percent_fit in self.POS_PREDICT_PERCENT_FIT_DICT.items():
            if predict_percent_fit is None:
                proba_tuple = (pos_symbol, 0.0)
                tuple_list.append(proba_tuple)
            else:
                proba_tuple = (pos_symbol, predict_percent_fit(html_str))
                tuple_list.append(proba_tuple)
        tuple_list.sort(reverse=True, key=lambda x: x[1])

        return tuple_list[0][0]
    
    def build_pos_lr_predict_percent(self, pos_symbol, verbose=False):
        predict_percent_fit = None
        if pos_symbol in self.POS_LR_DICT:
            
            # Re-calibrate the inference engine
            cv = CountVectorizer(vocabulary=self.POS_CV.vocabulary_)
            cv._validate_vocabulary()

            def predict_percent_fit(navigable_parent):

                X_test = self.POS_TT.transform(cv.transform([navigable_parent])).toarray()
                y_predict_proba = self.POS_LR_DICT[pos_symbol].predict_proba(X_test)[0][1]

                return y_predict_proba

        return predict_percent_fit
    
    def build_isheader_lr_predict_percent(self, verbose=False):
        
        # Re-calibrate the inference engine
        vocabulary = getattr(self.ISHEADER_CV, 'vocabulary_', None)
        cv = CountVectorizer(vocabulary=vocabulary)
        cv._validate_vocabulary()
        
        def predict_percent_fit(navigable_parent):

            X_test = self.ISHEADER_TT.transform(cv.transform([navigable_parent])).toarray()
            y_predict_proba = self.ISHEADER_LR.predict_proba(X_test)[0][1]

            return y_predict_proba

        return predict_percent_fit

class ElementAnalysis(object):
    """Element analysis class."""

    def __init__(self, ha=None, hc=None, verbose=False):
        if ha is None:
            self.ha = HeaderAnalysis()
        else:
            self.ha = ha
        if hc is None:
            self.hc = HeaderCategories()
        else:
            self.hc = hc
        self.verbose = verbose

    def get_idx_list(self, items_list, item_str):
        item_count = items_list.count(item_str)
        idx_list = []
        idx = -1
        while len(idx_list) < item_count:
            idx = items_list.index(item_str, idx+1)
            idx_list.append(idx)

        return idx_list

    def find_basic_quals_section(self, child_strs_list, cu=None, crf=None, verbose=False):
        if cu is None:
            from scrape_utils import WebScrapingUtilities
            wsu = WebScrapingUtilities()
            uri = wsu.secrets_json['neo4j']['connect_url']
            user =  wsu.secrets_json['neo4j']['username']
            password = wsu.secrets_json['neo4j']['password']
            from cypher_utils import CypherUtilities
            cu = CypherUtilities(uri=uri, user=user, password=password, driver=None, s=s, ha=self.ha)
        if crf is None:
            from html_analysis import CrfUtilities
            crf = CrfUtilities(ha=self.ha, hc=self.hc, cu=cu, verbose=verbose)
        child_tags_list = self.ha.get_child_tags_list(child_strs_list)
        is_header_list = self.ha.get_is_header_list(child_strs_list)

        feature_dict_list = self.hc.get_feature_dict_list(child_tags_list, is_header_list, child_strs_list)
        feature_tuple_list = [self.hc.get_feature_tuple(feature_dict) for feature_dict in feature_dict_list]
        
        crf_list = crf.CRF.predict_single(crf.sent2features(feature_tuple_list))
        pos_list = []
        for pos, feature_tuple, is_header in zip(crf_list, feature_tuple_list, is_header_list):
            navigable_parent = feature_tuple[1]
            if is_header:
                pos_list = self.hc.append_parts_of_speech_list(navigable_parent, pos_list=pos_list)
            else:
                pos_list.append(pos)
        consecutives_list = []
        
        from itertools import groupby
        for k, v in groupby(pos_list):
            consecutives_list.append((k, len(list(v))))

        return consecutives_list, pos_list

    def display_basic_requirements(self, child_strs_list):
        consecutives_list, pos_list = self.find_basic_quals_section(child_strs_list)
        rq_idx_list = self.get_idx_list(pos_list, 'H-RQ')

        # Display the Requirements sections in their own HTML
        if len(rq_idx_list):
            consecutives_idx_list = self.get_idx_list(consecutives_list, ('H-RQ', 1))
            for rq_idx, consecutives_idx in zip(rq_idx_list, consecutives_idx_list):
                o_count = consecutives_list[consecutives_idx+1][1]
                display(HTML(''.join(child_strs_list[rq_idx:rq_idx+o_count+1])))

    def display_reqs_from_url(self, page_url):
        import requests
        from itertools import groupby

        site_page = requests.get(url=page_url)
        body_soup = self.ha.get_body_soup(site_page.content)
        child_strs_list = self.ha.get_navigable_children(body_soup, [])
        self.display_basic_requirements(child_strs_list)

    #####################
    ## Other functions ##
    #####################