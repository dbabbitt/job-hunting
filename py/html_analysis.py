#!/usr/bin/env python
# coding: utf-8

from IPython.display import HTML, display
from bs4 import BeautifulSoup
from bs4.element import NavigableString
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import pylab
import re

import storage
s = storage.Storage()

class HeaderCategories(object):
	"""Header analysis class."""
	
	def __init__(self):
		if s.pickle_exists('TASK_SCOPE_HEADERS_LIST'):
			self.TASK_SCOPE_HEADERS_LIST = s.load_object('TASK_SCOPE_HEADERS_LIST')
		else:
			self.TASK_SCOPE_HEADERS_LIST = ['<b>Where You Come In:</b>','<b>Responsibilities:</b>','<b>Primary Responsibilities:</b>','<h2 class="jobsearch-JobDescriptionSection-jobDescriptionTitle icl-u-xs-my--md" id="jobDescriptionTitle">Full Job Description</h2>','<b>What will you do?</b>','<b>What does your success look like in the first 90 days?</b>','<b>Job Summary</b>','<b>Core Responsibilities</b>','<b>Duties included but not limited to:</b>','Translate / Interpret:','Measure / Quantify / Expand:','Explore / Enlighten:','<b>Responsibilities</b>','<div>Key responsibilities in this role include:</div>','Overview:','Responsibilities:','<b>This means you will:</b>','<b>ROLE SUMMARY</b>','<b>ROLE RESPONSIBILITIES</b>','<b>Key Responsibilities</b>','<b>Description</b>','<b>Overview</b>','<b>Summary</b>','<b>Principal Duties &amp; Responsibilities</b>']
			s.store_objects(TASK_SCOPE_HEADERS_LIST=self.TASK_SCOPE_HEADERS_LIST)
		if s.pickle_exists('REQ_QUALS_HEADERS_LIST'):
			self.REQ_QUALS_HEADERS_LIST = s.load_object('REQ_QUALS_HEADERS_LIST')
		else:
			self.REQ_QUALS_HEADERS_LIST = ['<b>What it Takes to Succeed:</b>','<b>A candidate must:</b>','<b>Position Requirements:</b>','<p>Experience:</p>','<b>Qualifications:</b>','<b>Required Qualifications:</b>','<b>What skills, experiences, and education are required?</b>','<b>Qualifying Experience</b>','<b>Requirements:</b>','<b>Qualifications</b>','Qualifications:','Minimum Skill Qualifications','<b>To do that, this mean you have:</b>','<b>QUALIFICATIONS</b>','<b>Job Qualifications</b>','<b>Work Experience</b>','<b>License and Certifications</b>','<b>Skills, Abilities &amp; Competencies</b>']
			s.store_objects(REQ_QUALS_HEADERS_LIST=self.REQ_QUALS_HEADERS_LIST)
		if s.pickle_exists('PREFF_QUALS_HEADERS_LIST'):
			self.PREFF_QUALS_HEADERS_LIST = s.load_object('PREFF_QUALS_HEADERS_LIST')
		else:
			self.PREFF_QUALS_HEADERS_LIST = ['<b>Preferred Qualifications:</b>','<b>What are we looking for?</b>','<b>The Ideal Candidate will:</b>','<p>You are...</p>','<b>And we love people who:</b>','<b>A strong candidate will also have</b>']
			s.store_objects(PREFF_QUALS_HEADERS_LIST=self.PREFF_QUALS_HEADERS_LIST)
		if s.pickle_exists('LEGAL_NOTIFS_HEADERS_LIST'):
			self.LEGAL_NOTIFS_HEADERS_LIST = s.load_object('LEGAL_NOTIFS_HEADERS_LIST')
		else:
			self.LEGAL_NOTIFS_HEADERS_LIST = ['<div>CCPA Privacy Notice</div>','<p>Application Question:</p>','<b>EOE Statement:</b>','<b>Sunshine Act</b>','<b>EEO &amp; Employment Eligibility</b>','<b>EEO Statement</b>']
			s.store_objects(LEGAL_NOTIFS_HEADERS_LIST=self.LEGAL_NOTIFS_HEADERS_LIST)
		if s.pickle_exists('JOB_TITLE_HEADERS_LIST'):
			self.JOB_TITLE_HEADERS_LIST = s.load_object('JOB_TITLE_HEADERS_LIST')
		else:
			self.JOB_TITLE_HEADERS_LIST = ['<b>Position</b>']
			s.store_objects(JOB_TITLE_HEADERS_LIST=self.JOB_TITLE_HEADERS_LIST)
		if s.pickle_exists('OFFICE_LOC_HEADERS_LIST'):
			self.OFFICE_LOC_HEADERS_LIST = s.load_object('OFFICE_LOC_HEADERS_LIST')
		else:
			self.OFFICE_LOC_HEADERS_LIST = ['<b>Location</b>','<p>Work Remotely:</p>','<p>Work Location:</p>','<b>Location and Travel:</b>','<b>Travel :</b>','<b>Working Conditions</b>','<b>Primary Location</b>','<b>Work Locations</b>']
			s.store_objects(OFFICE_LOC_HEADERS_LIST=self.OFFICE_LOC_HEADERS_LIST)
		if s.pickle_exists('JOB_DURATION_HEADERS_LIST'):
			self.JOB_DURATION_HEADERS_LIST = s.load_object('JOB_DURATION_HEADERS_LIST')
		else:
			self.JOB_DURATION_HEADERS_LIST = ['<b>Duration</b>','<p>Schedule:</p>','<b>Employee Status :</b>','<b>Shift :</b>']
			s.store_objects(JOB_DURATION_HEADERS_LIST=self.JOB_DURATION_HEADERS_LIST)
		if s.pickle_exists('SUPP_PAY_HEADERS_LIST'):
			self.SUPP_PAY_HEADERS_LIST = s.load_object('SUPP_PAY_HEADERS_LIST')
		else:
			self.SUPP_PAY_HEADERS_LIST = ['<b>Benefits</b>','<p>Supplemental Pay:</p>','<p>Benefit Conditions:</p>','<b>Options</b>','<p>Our Benefits Include:</p>','<p>Benefits:</p>']
			s.store_objects(SUPP_PAY_HEADERS_LIST=self.SUPP_PAY_HEADERS_LIST)
		if s.pickle_exists('EDUC_REQS_HEADERS_LIST'):
			self.EDUC_REQS_HEADERS_LIST = s.load_object('EDUC_REQS_HEADERS_LIST')
		else:
			self.EDUC_REQS_HEADERS_LIST = ['<p>Education:</p>','<b>Education</b>']
			s.store_objects(EDUC_REQS_HEADERS_LIST=self.EDUC_REQS_HEADERS_LIST)
		if s.pickle_exists('INTERV_PROC_HEADERS_LIST'):
			self.INTERV_PROC_HEADERS_LIST = s.load_object('INTERV_PROC_HEADERS_LIST')
		else:
			self.INTERV_PROC_HEADERS_LIST = ['<p>COVID-19 Precaution(s):</p>']
			s.store_objects(INTERV_PROC_HEADERS_LIST=self.INTERV_PROC_HEADERS_LIST)
		if s.pickle_exists('CORP_SCOPE_HEADERS_LIST'):
			self.CORP_SCOPE_HEADERS_LIST = s.load_object('CORP_SCOPE_HEADERS_LIST')
		else:
			self.CORP_SCOPE_HEADERS_LIST = ['<b>Careers with Optum.</b>','<b>Why LPL?</b>','<b>Information on Interviews:</b>',"<p>Company's website:</p>",'<b>Patients First | Innovation | Winning Culture | Heart Recovery</b>','<b>Cogito Business Intelligence Developer, Enterprise Data &amp; Digital Health</b>']
			s.store_objects(CORP_SCOPE_HEADERS_LIST=self.CORP_SCOPE_HEADERS_LIST)
		if s.pickle_exists('POST_DATE_HEADERS_LIST'):
			self.POST_DATE_HEADERS_LIST = s.load_object('POST_DATE_HEADERS_LIST')
		else:
			self.POST_DATE_HEADERS_LIST = ['<b>Job Posting :</b>']
			s.store_objects(POST_DATE_HEADERS_LIST=self.POST_DATE_HEADERS_LIST)
		if s.pickle_exists('OTHER_HEADERS_LIST'):
			self.OTHER_HEADERS_LIST = s.load_object('OTHER_HEADERS_LIST')
		else:
			self.OTHER_HEADERS_LIST = ['<div>Share</div>']
			s.store_objects(OTHER_HEADERS_LIST=self.OTHER_HEADERS_LIST)
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
			s.store_objects(POS_EXPLANATION_DICT=self.POS_EXPLANATION_DICT)

	def get_feature_dict_list(self, child_tags_list, is_header_list, child_strs_list):
		feature_dict_list = [{'initial_tag': tag, 'is_header': is_header,
							  'is_task_scope': child_str in self.TASK_SCOPE_HEADERS_LIST,
							  'is_req_quals': child_str in self.REQ_QUALS_HEADERS_LIST,
							  'is_preff_quals': child_str in self.PREFF_QUALS_HEADERS_LIST,
							  'is_legal_notifs': child_str in self.LEGAL_NOTIFS_HEADERS_LIST,
							  'is_job_title': child_str in self.JOB_TITLE_HEADERS_LIST,
							  'is_office_loc': child_str in self.OFFICE_LOC_HEADERS_LIST,
							  'is_job_duration': child_str in self.JOB_DURATION_HEADERS_LIST,
							  'is_supp_pay': child_str in self.SUPP_PAY_HEADERS_LIST,
							  'is_educ_reqs': child_str in self.EDUC_REQS_HEADERS_LIST,
							  'is_interv_proc': child_str in self.INTERV_PROC_HEADERS_LIST,
							  'is_corp_scope': child_str in self.CORP_SCOPE_HEADERS_LIST,
							  'is_post_date': child_str in self.POST_DATE_HEADERS_LIST,
							  'is_other': child_str in self.OTHER_HEADERS_LIST,
							  'child_str': child_str} for tag, is_header, child_str in zip(child_tags_list, is_header_list,
																						   child_strs_list)]
		
		return feature_dict_list
	
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

	def get_feature_tuple(self, feature_dict):
		feature_list = [feature_dict['initial_tag'], feature_dict['child_str']]
		is_header = feature_dict['is_header']
		if (is_header == True):
			if feature_dict['is_task_scope']:
				feature_list.append('H-TS')
			elif feature_dict['is_req_quals']:
				feature_list.append('H-RQ')
			elif feature_dict['is_preff_quals']:
				feature_list.append('H-PQ')
			elif feature_dict['is_legal_notifs']:
				feature_list.append('H-LN')
			elif feature_dict['is_job_title']:
				feature_list.append('H-JT')
			elif feature_dict['is_office_loc']:
				feature_list.append('H-OL')
			elif feature_dict['is_job_duration']:
				feature_list.append('H-JD')
			elif feature_dict['is_supp_pay']:
				feature_list.append('H-SP')
			elif feature_dict['is_educ_reqs']:
				feature_list.append('H-ER')
			elif feature_dict['is_interv_proc']:
				feature_list.append('H-IP')
			elif feature_dict['is_corp_scope']:
				feature_list.append('H-CS')
			elif feature_dict['is_post_date']:
				feature_list.append('H-PD')
			elif feature_dict['is_other']:
				feature_list.append('H-O')
		elif str(is_header) == 'nan':
			feature_list.append(np.nan)
		else:
			feature_list.append('O')

		return tuple(feature_list)

class HeaderAnalysis(object):
	"""Header analysis class."""
	
	def __init__(self):
		self.HTML_SCANNER_REGEX = re.compile(r'</?\w+|\w+[#\+]*|:|\.|\?')
		self.QUALS_SCANNER_REGEX = re.compile(r'\b[1-9a-zA-Z][0-9a-zA-Z]*( *[#\+]{1,2}|\b)')
		self.LT_REGEX = re.compile(r'\s+<')
		self.GT_REGEX = re.compile(r'>\s+')
		self.CLF_NAME = 'LogisticRegression'
		self.SAVES_HTML_FOLDER = os.path.join(s.saves_folder, 'html')
		self.CMAP = pylab.cm.get_cmap('coolwarm')
		if s.pickle_exists('CHILDLESS_TAGS_LIST'):
			self.CHILDLESS_TAGS_LIST = s.load_object('CHILDLESS_TAGS_LIST')
		else:
			self.CHILDLESS_TAGS_LIST = ['template','script']
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
	
	def quals_regex_tokenizer(self, corpus):
		
		return [match.group() for match in re.finditer(self.QUALS_SCANNER_REGEX, corpus)]
	
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

	def get_navigable_children(self, tag, result_list=[]):
		if (type(tag) is not NavigableString):
			if hasattr(tag, 'children'):
				for child_tag in tag.children:
					result_list = self.get_navigable_children(child_tag, result_list)
			elif tag.name is not None:
				self.store_unique_list('CHILDLESS_TAGS_LIST', tag.name)
		else:
			base_str = self.clean_html_str(tag)
			if base_str:
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
			html_str = f.read()
			body_soup = self.get_body_soup(html_str)
			child_strs_list = self.get_navigable_children(body_soup, [])
		
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
				is_header = np.nan
			is_header_list.append(is_header)
		
		return is_header_list

class ElementAnalysis(object):
	"""Element analysis class."""
	
	def __init__(self):
		self.document_structure_elements_set = set(['body','head','html'])
		self.document_head_elements_set = set(['base','basefont','isindex','link','meta','object','script','style','title'])
		self.document_body_elements_set = set(['a','abbr','acronym','address','applet','area','article','aside','audio','b','bdi','bdo','big','blockquote','br','button','canvas','caption','center','cite','code','col','colgroup','data','datalist','dd','del','dfn','dir','div','dl','dt','em','embed','fieldset','figcaption','figure','font','footer','form','h1','h2','h3','h4','h5','h6','header','hr','i','img','input','ins','isindex','kbd','keygen','label','legend','li','main','map','mark','menu','meter','nav','noscript','object','ol','optgroup','option','output','p','param','pre','progress','q','rb','rp','rt','rtc','ruby','s','samp','script','section','select','small','source','span','strike','strong','sub','sup','table','tbody','td','template','textarea','tfoot','th','thead','time','tr','track','tt','u','ul','var','video','wbr'])
		self.block_elements_set = set(['address','article','aside','blockquote','center','dd','del','dir','div','dl','dt','figcaption','figure','footer','h1','h2','h3','h4','h5','h6','header','hr','ins','li','main','menu','nav','noscript','ol','p','pre','script','section','ul'])
		self.basic_text_set = set(['h1','h2','h3','h4','h5','h6','p'])
		self.section_headings_set = set(['h1','h2','h3','h4','h5','h6'])
		self.lists_set = set(['dd','dir','dl','dt','li','ol','ul'])
		self.other_block_elements_set = set(['address','article','aside','blockquote','center','del','div','figcaption','figure','footer','header','hr','ins','main','menu','nav','noscript','pre','script','section'])
		self.inline_elements_set = set(['a','abbr','acronym','b','bdi','bdo','big','br','cite','code','data','del','dfn','em','font','i','ins','kbd','mark','q','rb','rp','rt','rtc','ruby','s','samp','script','small','span','strike','strong','sub','sup','template','time','tt','u','var','wbr'])
		self.anchor_set = set(['a'])
		self.phrase_elements_set = set(['abbr','acronym','b','big','code','dfn','em','font','i','kbd','s','samp','small','strike','strong','tt','u','var'])
		self.general_set = set(['abbr','acronym','dfn','em','strong'])
		self.computer_phrase_elements_set = set(['code','kbd','samp','var'])
		self.presentation_set = set(['b','big','font','i','s','small','strike','tt','u'])
		self.span_set = set(['span'])
		self.other_inline_elements_set = set(['bdi','bdo','br','cite','data','del','ins','mark','q','rb','rp','rt','rtc','ruby','script','sub','sup','template','time','wbr'])
		self.images_and_objects_set = set(['applet','area','audio','canvas','embed','img','map','object','param','source','track','video'])
		self.forms_set = set(['button','datalist','fieldset','form','input','isindex','keygen','label','legend','meter','optgroup','option','output','progress','select','textarea'])
		self.tables_set = set(['caption','col','colgroup','table','tbody','td','tfoot','th','thead','tr'])
		self.frames_set = set(['frame','frameset','iframe','noframes'])
		self.historic_elements_set = set(['listing','nextid','plaintext','xmp'])
		self.non_standard_elements_set = set(['blink','layer','marquee','nobr','noembed'])
		if s.pickle_exists('CRF'):
			self.CRF = s.load_object('CRF')
		else:
			import sklearn_crfsuite
			self.CRF = sklearn_crfsuite.CRF(algorithm='lbfgs',c1=0.1,c2=0.1,max_iterations=100,all_possible_transitions=True)
			s.store_objects(CRF=self.CRF)
		if s.pickle_exists('CHILD_STRS_LIST_DICT'):
			self.CHILD_STRS_LIST_DICT = s.load_object('CHILD_STRS_LIST_DICT')
		else:
			self.build_child_strs_list_dictionary()
		self.lda_predict_percent = self.build_lda_predict_percent()
		if s.pickle_exists('CS_CV'):
			self.CS_CV = s.load_object('CS_CV')
		else:
			from sklearn.feature_extraction.text import CountVectorizer
			ha = HeaderAnalysis()
			self.CS_CV = CountVectorizer(analyzer='word',binary=False,decode_error='strict',lowercase=False,max_df=1.0,max_features=None,min_df=0.0,ngram_range=(1,5),stop_words=None,strip_accents='ascii',tokenizer=ha.html_regex_tokenizer)
			s.store_objects(CS_CV=self.CS_CV)
		if s.pickle_exists('CS_CV_VOCAB'):
			self.CS_CV_VOCAB = s.load_object('CS_CV_VOCAB')
		else:
			self.CS_CV_VOCAB = self.CS_CV.vocabulary_
			s.store_objects(CS_CV_VOCAB=self.CS_CV_VOCAB)
		if s.pickle_exists('CS_TT'):
			self.CS_TT = s.load_object('CS_TT')
		else:
			from sklearn.feature_extraction.text import TfidfTransformer
			self.CS_TT = TfidfTransformer(norm='l1',smooth_idf=True,sublinear_tf=False,use_idf=True)
			s.store_objects(CS_TT=self.CS_TT)
		if s.pickle_exists('FIT_ESTIMATORS_DICT'):
			self.FIT_ESTIMATORS_DICT = s.load_object('FIT_ESTIMATORS_DICT')
		else:
			from sklearn.linear_model import LogisticRegression
			self.FIT_ESTIMATORS_DICT = {}
			self.FIT_ESTIMATORS_DICT['LogisticRegression'] = LogisticRegression(C=375.0,class_weight='balanced',dual=False,fit_intercept=True,intercept_scaling=1,l1_ratio=None,max_iter=1000,multi_class='auto',n_jobs=None,penalty='l1',random_state=None,solver='liblinear',tol=0.0001,verbose=0,warm_start=False)
			s.store_objects(FIT_ESTIMATORS_DICT=self.FIT_ESTIMATORS_DICT)
		if s.pickle_exists('CHILD_STR_CLF'):
			self.CHILD_STR_CLF = s.load_object('CHILD_STR_CLF')
		else:
			if 'LogisticRegression' in self.FIT_ESTIMATORS_DICT:
				self.CHILD_STR_CLF = self.FIT_ESTIMATORS_DICT['LogisticRegression']
			else:
				self.CHILD_STR_CLF = LogisticRegression(C=375.0,class_weight='balanced',dual=False,fit_intercept=True,intercept_scaling=1,l1_ratio=None,max_iter=1000,multi_class='auto',n_jobs=None,penalty='l1',random_state=None,solver='liblinear',tol=0.0001,verbose=0,warm_start=False)
			s.store_objects(CHILD_STR_CLF=self.CHILD_STR_CLF)
		self.lr_predict_percent_is_header = self.build_lr_predict_percent_is_header()

	def build_child_strs_list_dictionary(self):
		self.CHILD_STRS_LIST_DICT = {}
		ha = HeaderAnalysis()
		files_list = os.listdir(ha.SAVES_HTML_FOLDER)
		for file_name in files_list:
			if file_name in self.CHILD_STRS_LIST_DICT:
				child_strs_list = self.CHILD_STRS_LIST_DICT[file_name]
			else:
				child_strs_list = self.get_child_strs_from_file(file_name)
			navigable_parent = child_strs_list[0]
			if navigable_parent not in ha.NAVIGABLE_PARENT_IS_HEADER_DICT:
				continue
			child_tags_list = []
			for navigable_parent in child_strs_list:
				if navigable_parent not in ha.NAVIGABLE_PARENT_IS_HEADER_DICT:
					break
				tokenized_sent = ha.html_regex_tokenizer(navigable_parent)
				try:
					first_token = tokenized_sent[0]
					if first_token[0] == '<':
						child_tags_list.append(first_token[1:])
					else:
						child_tags_list.append('plaintext')
				except:
					child_tags_list.append('plaintext')
			if len(child_tags_list) == len(child_strs_list):
				if file_name not in self.CHILD_STRS_LIST_DICT:
					self.CHILD_STRS_LIST_DICT[file_name] = child_strs_list
					s.store_objects(CHILD_STRS_LIST_DICT=self.CHILD_STRS_LIST_DICT)

	def build_lda_predict_percent(self):
		from gensim.corpora.dictionary import Dictionary
		from gensim.models.ldamodel import LdaModel
		ha = HeaderAnalysis()
		
		# Build model with tokenized words
		sents_list = [sent_str for sublist in self.CHILD_STRS_LIST_DICT.values() for sent_str in sublist]
		tokenized_sents_list = [ha.html_regex_tokenizer(sent_str) for sent_str in sents_list]
		
		# Create a corpus from a list of texts
		HEADERS_DICTIONARY = Dictionary(tokenized_sents_list)
		headers_corpus = [HEADERS_DICTIONARY.doc2bow(tag_str) for tag_str in tokenized_sents_list]
		
		# Train the model on the corpus
		LDA = LdaModel(corpus=headers_corpus, num_topics=2)
		
		# Define a predictor
		def predict_percent_fit(navigable_parent):
			X_test = HEADERS_DICTIONARY.doc2bow(ha.html_regex_tokenizer(navigable_parent))
			result_list = LDA[X_test]
			if len(result_list) == 1:
				result_tuple = result_list[0]
			elif len(result_list) == 2:
				result_tuple = result_list[1]

			# Assume it's the probability of the smaller topic
			y_predict_proba = result_tuple[1]

			return y_predict_proba
		
		return predict_percent_fit
	
	def build_lr_predict_percent_is_header(self):
		from sklearn.feature_extraction.text import CountVectorizer
		from sklearn.feature_extraction.text import TfidfTransformer
		from sklearn.linear_model import LogisticRegression
		ha = HeaderAnalysis()
		
		# Re-transform the bag-of-words and tf-idf from the new manual scores
		rows_list = [{'navigable_parent': navigable_parent,
					  'is_header': is_header} for navigable_parent, is_header in ha.NAVIGABLE_PARENT_IS_HEADER_DICT.items()]
		child_str_df = pd.DataFrame(rows_list)
		
		# The shape of the Bag-of-words count vector here should be n sentences * m unique words
		sents_list = child_str_df.navigable_parent.tolist()
		bow_matrix = self.CS_CV.fit_transform(sents_list)
		
		# Tf-idf must get from Bag-of-words first
		tfidf_matrix = self.CS_TT.fit_transform(bow_matrix)
		
		# Re-train the classifier
		X = tfidf_matrix.toarray()
		y = child_str_df.is_header.to_numpy()
		self.CHILD_STR_CLF.fit(X, y)
		s.store_objects(CHILD_STR_CLF=self.CHILD_STR_CLF)
		
		# Re-calibrate the inference engine
		cv = CountVectorizer(vocabulary=self.CS_CV.vocabulary_)
		cv._validate_vocabulary()
		
		def predict_percent_fit(navigable_parent):
			X_test = self.CS_TT.transform(cv.transform([navigable_parent])).toarray()
			y_predict_proba = self.CHILD_STR_CLF.predict_proba(X_test)[0][1]
			
			return y_predict_proba
		
		return predict_percent_fit
	
	def predict_percent_fit(self, navigable_parents_list):
		from sklearn.feature_extraction.text import CountVectorizer
		CS_CV = CountVectorizer(vocabulary=self.CS_CV_VOCAB)
		CS_CV._validate_vocabulary()
		y_predict_proba_list = []
		for navigable_parent in navigable_parents_list:
			if(self.CLF_NAME == 'LdaModel'):
				X_test = HEADERS_DICTIONARY.doc2bow(self.html_regex_tokenizer(navigable_parent))
				result_list = LDA[X_test]
				if len(result_list) == 1:
					result_tuple = result_list[0]
				elif len(result_list) == 2:
					result_tuple = result_list[1]
					
				# Assume it's the probability of the smaller topic
				y_predict_proba = 1.0 - result_tuple[1]
			
			else:
				X_test = self.CS_TT.transform(CS_CV.transform(navigable_parents_list)).toarray()
				y_predict_proba = self.CHILD_STR_CLF.predict_proba(X_test)
			y_predict_proba_list.append(y_predict_proba)
		
		return y_predict_proba_list

	def word2features(self, sent, i):
		from itertools import groupby
		null_element = 'plaintext'
		tag = sent[i][0]
		child_str = sent[i][1]
		postag = sent[i][2]
		
		features = {
			'bias': 1.0,
			'child_str.is_header_lr': self.lr_predict_percent_is_header(child_str),
			'child_str.lda': self.lda_predict_percent(child_str),
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

	def get_idx_list(self, items_list, item_str):
		item_count = items_list.count(item_str)
		idx_list = []
		idx = -1
		while len(idx_list) < item_count:
			idx = items_list.index(item_str, idx+1)
			idx_list.append(idx)

		return idx_list
	
	def find_basic_quals_section(self, child_strs_list):
		from itertools import groupby
		ha = HeaderAnalysis()
		hc = HeaderCategories()
		child_tags_list = ha.get_child_tags_list(child_strs_list)
		is_header_list = ha.get_is_header_list(child_strs_list)
		
		feature_dict_list = hc.get_feature_dict_list(child_tags_list, is_header_list, child_strs_list)
		feature_tuple_list = [hc.get_feature_tuple(feature_dict) for feature_dict in feature_dict_list]
		
		crf_list = self.CRF.predict_single(self.sent2features(feature_tuple_list))
		pos_list = []
		for pos, feature_tuple in zip(crf_list, feature_tuple_list):
			navigable_parent = feature_tuple[1]
			if navigable_parent in ha.NAVIGABLE_PARENT_IS_HEADER_DICT:
				pos_list = hc.append_parts_of_speech_list(navigable_parent, pos_list)
			else:
				pos_list.append(pos)
		consecutives_list = []
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
		ha = HeaderAnalysis()
		
		site_page = requests.get(url=page_url)
		body_soup = ha.get_body_soup(site_page.content)
		child_strs_list = ha.get_navigable_children(body_soup, [])
		self.display_basic_requirements(child_strs_list)