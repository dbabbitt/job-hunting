
#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria

from . import nu, cu
import pandas as pd

class HeaderCategories(object):
    """Header categories class."""
    
    def __init__(self, verbose=False):
        self.verbose = verbose

        # Get the task scope headers
        cypher_str = """
            MATCH (np:NavigableParents {is_task_scope: true, is_header: true})
            RETURN np.navigable_parent AS navigable_parent;"""
        df = pd.DataFrame(cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the task scope list
        self.TASK_SCOPE_HEADERS_LIST = df.navigable_parent.tolist()
        if not len(self.TASK_SCOPE_HEADERS_LIST):
            if nu.pickle_exists('TASK_SCOPE_HEADERS_LIST'):
                self.TASK_SCOPE_HEADERS_LIST = nu.load_object('TASK_SCOPE_HEADERS_LIST')
            else:
                self.TASK_SCOPE_HEADERS_LIST = ['<b>Where You Come In:</b>', '<b>Responsibilities:</b>', '<b>Primary Responsibilities:</b>', '<h2 class="jobsearch-JobDescriptionSection-jobDescriptionTitle icl-u-xs-my--md" id="jobDescriptionTitle">Full Job Description</h2>', '<b>What will you do?</b>', '<b>What does your success look like in the first 90 days?</b>', '<b>Job Summary</b>', '<b>Core Responsibilities</b>', '<b>Duties included but not limited to:</b>', 'Translate / Interpret:', 'Measure / Quantify / Expand:', 'Explore / Enlighten:', '<b>Responsibilities</b>', '<div>Key responsibilities in this role include:</div>', 'Overview:', 'Responsibilities:', '<b>This means you will:</b>', '<b>ROLE SUMMARY</b>', '<b>ROLE RESPONSIBILITIES</b>', '<b>Key Responsibilities</b>', '<b>Description</b>', '<b>Overview</b>', '<b>Summary</b>', '<b>Principal Duties &amp; Responsibilities</b>']
                nu.store_objects(TASK_SCOPE_HEADERS_LIST=self.TASK_SCOPE_HEADERS_LIST, verbose=verbose)

        # Get the req quals headers
        cypher_str = """
            MATCH (np:NavigableParents {is_minimum_qualification: true, is_header: true})
            RETURN np.navigable_parent AS navigable_parent;"""
        df = pd.DataFrame(cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the req quals list
        self.MINIMUM_QUALIFICATION_HEADERS_LIST = df.navigable_parent.tolist()
        if not len(self.MINIMUM_QUALIFICATION_HEADERS_LIST):
            if nu.pickle_exists('MINIMUM_QUALIFICATION_HEADERS_LIST'):
                self.MINIMUM_QUALIFICATION_HEADERS_LIST = nu.load_object('MINIMUM_QUALIFICATION_HEADERS_LIST')
            else:
                self.MINIMUM_QUALIFICATION_HEADERS_LIST = ['<b>What it Takes to Succeed:</b>', '<b>A candidate must:</b>', '<b>Position Requirements:</b>', '<p>Experience:</p>', '<b>Qualifications:</b>', '<b>Required Qualifications:</b>', '<b>What skills, experiences, and education are required?</b>', '<b>Qualifying Experience</b>', '<b>Requirements:</b>', '<b>Qualifications</b>', 'Qualifications:', 'Minimum Skill Qualifications', '<b>To do that, this mean you have:</b>', '<b>QUALIFICATIONS</b>', '<b>Job Qualifications</b>', '<b>Work Experience</b>', '<b>License and Certifications</b>', '<b>Skills, Abilities &amp; Competencies</b>']
                nu.store_objects(MINIMUM_QUALIFICATION_HEADERS_LIST=self.MINIMUM_QUALIFICATION_HEADERS_LIST, verbose=verbose)

        # Get the preff quals headers
        cypher_str = """
            MATCH (np:NavigableParents {is_preferred_qualification: true, is_header: true})
            RETURN np.navigable_parent AS navigable_parent;"""
        df = pd.DataFrame(cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the preff quals list
        self.PREFERRED_QUALIFICATION_HEADERS_LIST = df.navigable_parent.tolist()
        if not len(self.PREFERRED_QUALIFICATION_HEADERS_LIST):
            if nu.pickle_exists('PREFERRED_QUALIFICATION_HEADERS_LIST'):
                self.PREFERRED_QUALIFICATION_HEADERS_LIST = nu.load_object('PREFERRED_QUALIFICATION_HEADERS_LIST')
            else:
                self.PREFERRED_QUALIFICATION_HEADERS_LIST = ['<b>Preferred Qualifications:</b>', '<b>What are we looking for?</b>', '<b>The Ideal Candidate will:</b>', '<p>You are...</p>', '<b>And we love people who:</b>', '<b>A strong candidate will also have</b>']
                nu.store_objects(PREFERRED_QUALIFICATION_HEADERS_LIST=self.PREFERRED_QUALIFICATION_HEADERS_LIST, verbose=verbose)

        # Get the legal notifs headers
        cypher_str = """
            MATCH (np:NavigableParents {is_legal_notification: true, is_header: true})
            RETURN np.navigable_parent AS navigable_parent;"""
        df = pd.DataFrame(cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the legal notifs list
        self.LEGAL_NOTIFICATION_HEADERS_LIST = df.navigable_parent.tolist()
        if not len(self.LEGAL_NOTIFICATION_HEADERS_LIST):
            if nu.pickle_exists('LEGAL_NOTIFICATION_HEADERS_LIST'):
                self.LEGAL_NOTIFICATION_HEADERS_LIST = nu.load_object('LEGAL_NOTIFICATION_HEADERS_LIST')
            else:
                self.LEGAL_NOTIFICATION_HEADERS_LIST = ['<div>CCPA Privacy Notice</div>', '<p>Application Question:</p>', '<b>EOE Statement:</b>', '<b>Sunshine Act</b>', '<b>EEO &amp; Employment Eligibility</b>', '<b>EEO Statement</b>']
                nu.store_objects(LEGAL_NOTIFICATION_HEADERS_LIST=self.LEGAL_NOTIFICATION_HEADERS_LIST, verbose=verbose)

        # Get the job title headers
        cypher_str = """
            MATCH (np:NavigableParents {is_job_title: true, is_header: true})
            RETURN np.navigable_parent AS navigable_parent;"""
        df = pd.DataFrame(cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the job title list
        self.JOB_TITLE_HEADERS_LIST = df.navigable_parent.tolist()
        if not len(self.JOB_TITLE_HEADERS_LIST):
            if nu.pickle_exists('JOB_TITLE_HEADERS_LIST'):
                self.JOB_TITLE_HEADERS_LIST = nu.load_object('JOB_TITLE_HEADERS_LIST')
            else:
                self.JOB_TITLE_HEADERS_LIST = ['<b>Position</b>']
                nu.store_objects(JOB_TITLE_HEADERS_LIST=self.JOB_TITLE_HEADERS_LIST, verbose=verbose)

        # Get the office loc headers
        cypher_str = """
            MATCH (np:NavigableParents {is_office_location: true, is_header: true})
            RETURN np.navigable_parent AS navigable_parent;"""
        df = pd.DataFrame(cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the office location list
        self.OFFICE_LOCATION_HEADERS_LIST = df.navigable_parent.tolist()
        if not len(self.OFFICE_LOCATION_HEADERS_LIST):
            if nu.pickle_exists('OFFICE_LOCATION_HEADERS_LIST'):
                self.OFFICE_LOCATION_HEADERS_LIST = nu.load_object('OFFICE_LOCATION_HEADERS_LIST')
            else:
                self.OFFICE_LOCATION_HEADERS_LIST = ['<b>Location</b>', '<p>Work Remotely:</p>', '<p>Work Location:</p>', '<b>Location and Travel:</b>', '<b>Travel :</b>', '<b>Working Conditions</b>', '<b>Primary Location</b>', '<b>Work Locations</b>']
                nu.store_objects(OFFICE_LOCATION_HEADERS_LIST=self.OFFICE_LOCATION_HEADERS_LIST, verbose=verbose)

        # Get the job duration headers
        cypher_str = """
            MATCH (np:NavigableParents {is_job_duration: true, is_header: true})
            RETURN np.navigable_parent AS navigable_parent;"""
        df = pd.DataFrame(cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the job duration list
        self.JOB_DURATION_HEADERS_LIST = df.navigable_parent.tolist()
        if not len(self.JOB_DURATION_HEADERS_LIST):
            if nu.pickle_exists('JOB_DURATION_HEADERS_LIST'):
                self.JOB_DURATION_HEADERS_LIST = nu.load_object('JOB_DURATION_HEADERS_LIST')
            else:
                self.JOB_DURATION_HEADERS_LIST = ['<b>Duration</b>', '<p>Schedule:</p>', '<b>Employee Status :</b>', '<b>Shift :</b>']
                nu.store_objects(JOB_DURATION_HEADERS_LIST=self.JOB_DURATION_HEADERS_LIST, verbose=verbose)

        # Get the supp pay headers
        cypher_str = """
            MATCH (np:NavigableParents {is_supplemental_pay: true, is_header: true})
            RETURN np.navigable_parent AS navigable_parent;"""
        df = pd.DataFrame(cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the supplemental pay list
        self.SUPPLEMENTAL_PAY_HEADERS_LIST = df.navigable_parent.tolist()
        if not len(self.SUPPLEMENTAL_PAY_HEADERS_LIST):
            if nu.pickle_exists('SUPPLEMENTAL_PAY_HEADERS_LIST'):
                self.SUPPLEMENTAL_PAY_HEADERS_LIST = nu.load_object('SUPPLEMENTAL_PAY_HEADERS_LIST')
            else:
                self.SUPPLEMENTAL_PAY_HEADERS_LIST = ['<b>Benefits</b>', '<p>Supplemental Pay:</p>', '<p>Benefit Conditions:</p>', '<b>Options</b>', '<p>Our Benefits Include:</p>', '<p>Benefits:</p>']
                nu.store_objects(SUPPLEMENTAL_PAY_HEADERS_LIST=self.SUPPLEMENTAL_PAY_HEADERS_LIST, verbose=verbose)

        # Get the educ reqs headers
        cypher_str = """
            MATCH (np:NavigableParents {is_educational_requirement: true, is_header: true})
            RETURN np.navigable_parent AS navigable_parent;"""
        df = pd.DataFrame(cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the educational requirements list
        self.EDUCATIONAL_REQUIREMENT_HEADERS_LIST = df.navigable_parent.tolist()
        if not len(self.EDUCATIONAL_REQUIREMENT_HEADERS_LIST):
            if nu.pickle_exists('EDUCATIONAL_REQUIREMENT_HEADERS_LIST'):
                self.EDUCATIONAL_REQUIREMENT_HEADERS_LIST = nu.load_object('EDUCATIONAL_REQUIREMENT_HEADERS_LIST')
            else:
                self.EDUCATIONAL_REQUIREMENT_HEADERS_LIST = ['<p>Education:</p>', '<b>Education</b>']
                nu.store_objects(EDUCATIONAL_REQUIREMENT_HEADERS_LIST=self.EDUCATIONAL_REQUIREMENT_HEADERS_LIST, verbose=verbose)

        # Get the interv proc headers
        cypher_str = """
            MATCH (np:NavigableParents {is_interview_procedure: true, is_header: true})
            RETURN np.navigable_parent AS navigable_parent;"""
        df = pd.DataFrame(cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the interview procedure list
        self.INTERVIEW_PROCEDURE_HEADERS_LIST = df.navigable_parent.tolist()
        if not len(self.INTERVIEW_PROCEDURE_HEADERS_LIST):
            if nu.pickle_exists('INTERVIEW_PROCEDURE_HEADERS_LIST'):
                self.INTERVIEW_PROCEDURE_HEADERS_LIST = nu.load_object('INTERVIEW_PROCEDURE_HEADERS_LIST')
            else:
                self.INTERVIEW_PROCEDURE_HEADERS_LIST = ['<p>COVID-19 Precaution(nu):</p>']
                nu.store_objects(INTERVIEW_PROCEDURE_HEADERS_LIST=self.INTERVIEW_PROCEDURE_HEADERS_LIST, verbose=verbose)

        # Get the corp scope headers
        cypher_str = """
            MATCH (np:NavigableParents {is_corporate_scope: true, is_header: true})
            RETURN np.navigable_parent AS navigable_parent;"""
        df = pd.DataFrame(cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the corporate scope list
        self.CORPORATE_SCOPE_HEADERS_LIST = df.navigable_parent.tolist()
        if not len(self.CORPORATE_SCOPE_HEADERS_LIST):
            if nu.pickle_exists('CORPORATE_SCOPE_HEADERS_LIST'):
                self.CORPORATE_SCOPE_HEADERS_LIST = nu.load_object('CORPORATE_SCOPE_HEADERS_LIST')
            else:
                self.CORPORATE_SCOPE_HEADERS_LIST = ['<b>Careers with Optum.</b>', '<b>Why LPL?</b>', '<b>Information on Interviews:</b>', "<p>Company'nu website:</p>", '<b>Patients First | Innovation | Winning Culture | Heart Recovery</b>', '<b>Cogito Business Intelligence Developer, Enterprise Data &amp; Digital Health</b>']
                nu.store_objects(CORPORATE_SCOPE_HEADERS_LIST=self.CORPORATE_SCOPE_HEADERS_LIST, verbose=verbose)

        # Get the post date headers
        cypher_str = """
            MATCH (np:NavigableParents {is_posting_date: true, is_header: true})
            RETURN np.navigable_parent AS navigable_parent;"""
        df = pd.DataFrame(cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the posting date list
        self.POSTING_DATE_HEADERS_LIST = df.navigable_parent.tolist()
        if not len(self.POSTING_DATE_HEADERS_LIST):
            if nu.pickle_exists('POSTING_DATE_HEADERS_LIST'):
                self.POSTING_DATE_HEADERS_LIST = nu.load_object('POSTING_DATE_HEADERS_LIST')
            else:
                self.POSTING_DATE_HEADERS_LIST = ['<b>Job Posting :</b>']
                nu.store_objects(POSTING_DATE_HEADERS_LIST=self.POSTING_DATE_HEADERS_LIST, verbose=verbose)
        
        # Get the other headers
        cypher_str = """
            MATCH (np:NavigableParents {is_other: true, is_header: true})
            RETURN np.navigable_parent AS navigable_parent;"""
        df = pd.DataFrame(cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the other list
        self.OTHER_HEADERS_LIST = df.navigable_parent.tolist()
        if not len(self.OTHER_HEADERS_LIST):
            if nu.pickle_exists('OTHER_HEADERS_LIST'):
                self.OTHER_HEADERS_LIST = nu.load_object('OTHER_HEADERS_LIST')
            else:
                self.OTHER_HEADERS_LIST = ['<div>Share</div>']
                nu.store_objects(OTHER_HEADERS_LIST=self.OTHER_HEADERS_LIST, verbose=verbose)
        
        # Get the parts-of-speech explanations
        cypher_str = """
            MATCH (pos:PartsOfSpeech)
            WHERE pos.pos_explanation IS NOT NULL
            RETURN
                pos.pos_symbol AS pos_symbol,
                pos.pos_explanation AS pos_explanation;"""
        df = pd.DataFrame(cu.get_execution_results(cypher_str, verbose=verbose))
        
        # Initialize and populate the parts-of-speech dictionary
        self.POS_EXPLANATION_DICT = df.set_index('pos_symbol').pos_explanation.to_dict()
        self.POS_EXPLANATION_DICT.update({'O': 'Non-header', 'H': 'Header'})
        if not (len(self.POS_EXPLANATION_DICT.keys()) >= 14):
            if nu.pickle_exists('POS_EXPLANATION_DICT'):
                self.POS_EXPLANATION_DICT = nu.load_object('POS_EXPLANATION_DICT')
            else:
                self.POS_EXPLANATION_DICT = {}
                self.POS_EXPLANATION_DICT['H-TS'] = 'Task Scope Header'
                self.POS_EXPLANATION_DICT['H-RQ'] = 'Required Qualifications Header'
                self.POS_EXPLANATION_DICT['H-PQ'] = 'Preferred Qualifications Header'
                self.POS_EXPLANATION_DICT['H-Q'] = 'Qualifications Header'
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
                nu.store_objects(POS_EXPLANATION_DICT=self.POS_EXPLANATION_DICT, verbose=verbose)
    
    def append_parts_of_speech_list(self, navigable_parent, pos_list=[]):
        for column_name, symbol_suffix in cu.subtypes_dict.items():
            if navigable_parent in eval(f"self.{column_name.replace('is_', '').upper()}_HEADERS_LIST"):
                pos_list.append(f'H-{symbol_suffix}')
                
                return pos_list
        pos_list.append('O')

        return pos_list
    
    def get_pos_symbol(
        self, params_dict, verbose=False
    ):
        pos_symbol = None
        
        # Convert the values of params_dict to only True and False values
        params_dict = {
            k: True if v in [1, true, True] else False
            for k, v in params_dict.items()
        }
        
        is_header = params_dict.get('is_header')
        for subtype in cu.subtypes_list:
            exec(f"{subtype} = params_dict.get('{subtype}')")
        
        params_list = [is_header] + cu.subtypes_list
        assert not any(eval(param) is None for param in params_list), f"You have passed a dictionary which is missing some of these: {params_list}"
        
        pos_symbol = ['O-', 'H-'][is_header]
        for column_name, symbol_suffix in cu.subtypes_dict.items():
            if eval(column_name):
                pos_symbol += symbol_suffix
                break
        
        return pos_symbol

    
    def get_feature_tuple(
        self, feature_dict, pos_lr_predict_single=None, pos_crf_predict_single=None,
        pos_sgd_predict_single=None
    ):
        def try_to_guess(default_symbol='O-O'):
            if not (
                pos_crf_predict_single is None or
                pos_lr_predict_single is None or
                pos_sgd_predict_single is None
            ):
                import statistics
                mode = statistics.mode([
                    pos_crf_predict_single(feature_dict['child_str']),
                    pos_lr_predict_single(feature_dict['child_str']),
                    pos_sgd_predict_single(feature_dict['child_str'])
                ])
                feature_list.append(mode)
            
            # Seek a SectionCRFClassifierUtilities object
            elif pos_crf_predict_single is not None:
                feature_list.append(pos_crf_predict_single(feature_dict['child_str']))
            
            # Seek a SectionLRClassifierUtilities object
            elif pos_lr_predict_single is not None:
                feature_list.append(pos_lr_predict_single(feature_dict['child_str']))
            
            # Seek a SectionSGDClassifierUtilities object
            elif pos_sgd_predict_single is not None:
                feature_list.append(
                    pos_sgd_predict_single(feature_dict['child_str'])
                )
            
            else:
                feature_list.append(default_symbol)
        
        feature_list = [feature_dict['initial_tag'], feature_dict['child_str']]
        is_header = feature_dict.get('is_header')
        symbol_prefix = 'O-'
        if type(is_header) == bool:
            if is_header:
                symbol_prefix = 'H-'
            if all(feature_dict.get(param) is None for param in cu.subtypes_list):
                try_to_guess(default_symbol=f'{symbol_prefix}O')
            elif all(feature_dict.get(param, False) is False for param in cu.subtypes_list):
                try_to_guess(default_symbol=f'{symbol_prefix}O')
            else:
                for column_name, symbol_suffix in cu.subtypes_dict.items():
                    if feature_dict.get(column_name, False):
                        feature_list.append(symbol_prefix+symbol_suffix)
                        break
        elif str(is_header) == 'nan':
            try_to_guess()
        else:
            try_to_guess(default_symbol=f'{symbol_prefix}O')

        return tuple(feature_list)
    
    
    def get_feature_dict_list(self, child_tags_list, is_header_list, child_strs_list):
        sql_dict = {False: None, True: 1}
        feature_dict_list = []
        for tag, is_header, child_str in zip(
            child_tags_list, is_header_list, child_strs_list
        ):
            feature_dict = {
                'initial_tag': tag, 'is_header': is_header, 'child_str': child_str
            }
            for subtype in cu.subtypes_list:
                eval_str = f"child_str in self.{subtype.replace('is_', '').upper()}"
                eval_str += "_HEADERS_LIST"
                feature_dict.update({subtype: sql_dict[eval(eval_str)]})
            feature_dict_list.append(feature_dict)

        return feature_dict_list