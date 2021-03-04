
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
import sql_utlis

try:
	import storage
	s = storage.Storage()
except:
	from flaskr.storage import Storage
	s = Storage()

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

	def get_feature_tuple(self, feature_dict, lr_predict_single=None):
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
				if lr_predict_single is None:
					feature_list.append('H')
				else:
					feature_list.append(lr_predict_single(feature_dict['child_str']))
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
				if lr_predict_single is None:
					feature_list.append('O')
				else:
					feature_list.append(lr_predict_single(feature_dict['child_str']))
		elif str(is_header) == 'nan':
			if lr_predict_single is None:
				feature_list.append('O')
			else:
				feature_list.append(lr_predict_single(feature_dict['child_str']))
		else:
			if lr_predict_single is None:
				feature_list.append('O')
			else:
				feature_list.append(lr_predict_single(feature_dict['child_str']))

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

	def store_true_or_false_dict(self, dict_name, tag_str, true_or_false=False):
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
				is_header = None
			is_header_list.append(is_header)
		
		return is_header_list

class LdaUtilities(object):
	"""Latent Dirichlet Allocation utilities class."""
	
	def __init__(self, ha=None, hc=None, su=None, verbose=False):
		if ha is None:
			self.ha = HeaderAnalysis()
		else:
			self.ha = ha
		if hc is None:
			self.hc = HeaderCategories()
		else:
			self.hc = hc
		if su is None:
			self.su = sql_utlis.SqlUtilities()
		else:
			self.su = su
		
		# Build the LDA elements
		self.conn, self.cursor = self.su.get_jh_conn_cursor()
		if not s.pickle_exists('NAVIGABLE_PARENT_IS_HEADER_DICT'):
			self.su.build_child_strs_list_dictionary(self.cursor, verbose=verbose)
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
		
		self.lda_predict_single = self.build_lda_predict_single()
	
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

	def build_corpus(self, verbose=False):
		
		# Create a corpus from a list of texts
		self.LDA_CORPUS = [self.LDA_DICTIONARY.doc2bow(tag_str) for tag_str in self.tokenized_sents_list]
		
		s.store_objects(LDA_CORPUS=self.LDA_CORPUS, verbose=verbose)
	
	def build_topic_model(self, num_topics=2, chunksize=50, passes=75, alpha=None, decay=0.6, iterations=29, gamma_threshold=1e-10,
						  minimum_probability=0.001, verbose=False):
		
		# Train the model on the corpus
		id2word = {v: k for k, v in self.LDA_DICTIONARY.token2id.items()}
		if num_topics is None:
			num_topics = self.get_pos_count(verbose=verbose)
			
		# Get ratio of headers to non-headers
		if alpha is None:
			import numpy as np
			sql_str = '''
				SELECT COUNT(np.[navigable_parent]) AS header_count
				FROM [Jobhunting].[dbo].[NavigableParents] np
				WHERE np.[is_header] = 1'''
			is_header_df = pd.DataFrame(this.su.get_execution_results(this.cursor, sql_str))
			header_count = is_header_df.header_count.squeeze()
			sql_str = '''
				SELECT COUNT(np.[navigable_parent]) AS nonheader_count
				FROM [Jobhunting].[dbo].[NavigableParents] np
				WHERE np.[is_header] = 0'''
			is_nonheader_df = pd.DataFrame(this.su.get_execution_results(this.cursor, sql_str))
			nonheader_count = is_nonheader_df.nonheader_count.squeeze()
			nonheader_fraction = nonheader_count/(header_count + nonheader_count)
			header_fraction = header_count/(header_count + nonheader_count)
			alpha = np.array([nonheader_fraction, header_fraction], dtype=np.float32)
		
		from gensim.models.ldamodel import LdaModel
		self.TOPIC_MODEL = LdaModel(corpus=self.LDA_CORPUS, num_topics=num_topics, id2word=id2word, chunksize=chunksize, passes=passes,
									alpha=alpha, decay=decay, iterations=iterations, gamma_threshold=gamma_threshold,
									minimum_probability=minimum_probability)
		s.store_objects(TOPIC_MODEL=self.TOPIC_MODEL, verbose=verbose)

	def build_lda_predict_single(self):
		
		# Define a predictor
		def lda_predict_single(sent_str):
			tokens_list = self.ha.html_regex_tokenizer(sent_str)
			X_test = self.LDA_DICTIONARY.doc2bow(tokens_list)
			result_list = sorted(self.TOPIC_MODEL[X_test], key=lambda x: x[1], reverse=False)
			topic_number = result_list[0][0]
			
			return self.topic_dict[topic_number]
		
		return lda_predict_single

	def get_pos_count(self, verbose=False):
		
		# Get the parts-of-speech count to use as number of topics
		sql_str = 'SELECT pos_symbol, pos_explanation FROM PartsOfSpeech'
		pos_df = pd.DataFrame(self.su.get_execution_results(self.cursor, sql_str, verbose=False))
		sql_prefix = '''
			SELECT COUNT(*) AS row_count
			FROM [Jobhunting].[dbo].[NavigableParents] np
			WHERE
				np.[is_header] = '''
		self.pos_symbols_list = []
		for pos_symbol in pos_df.pos_symbol:
			if pos_symbol.startswith('H-'):
				sql_str = sql_prefix + '1'
			elif pos_symbol.startswith('O-'):
				sql_str = sql_prefix + '0'
			sql_str += ' AND\n\t\t\t\tnp.['
			if pos_symbol.endswith('-TS'):
				sql_str += 'is_task_scope] = 1;'
			elif pos_symbol.endswith('-RQ'):
				sql_str += 'is_minimum_qualification] = 1;'
			elif pos_symbol.endswith('-PQ'):
				sql_str += 'is_preferred_qualification] = 1;'
			elif pos_symbol.endswith('-LN'):
				sql_str += 'is_legal_notification] = 1;'
			elif pos_symbol.endswith('-JT'):
				sql_str += 'is_job_title] = 1;'
			elif pos_symbol.endswith('-OL'):
				sql_str += 'is_office_location] = 1;'
			elif pos_symbol.endswith('-JD'):
				sql_str += 'is_job_duration] = 1;'
			elif pos_symbol.endswith('-SP'):
				sql_str += 'is_supplemental_pay] = 1;'
			elif pos_symbol.endswith('-ER'):
				sql_str += 'is_educational_requirement] = 1;'
			elif pos_symbol.endswith('-IP'):
				sql_str += 'is_interview_procedure] = 1;'
			elif pos_symbol.endswith('-CS'):
				sql_str += 'is_corporate_scope] = 1;'
			elif pos_symbol.endswith('-PD'):
				sql_str += 'is_posting_date] = 1;'
			elif pos_symbol.endswith('-O'):
				sql_str += 'is_other] = 1;'
			count_df = pd.DataFrame(self.su.get_execution_results(self.cursor, sql_str, verbose=False))
			if count_df.row_count.squeeze() > 0:
				self.pos_symbols_list.append(pos_symbol)
		num_topics = len(self.pos_symbols_list)
		
		return num_topics

class CrfUtilities(object):
	"""Conditional Random Fields utilities class."""
	
	def __init__(self, ha=None, hc=None, su=None, verbose=False):
		if ha is None:
			self.ha = HeaderAnalysis()
		else:
			self.ha = ha
		if hc is None:
			self.hc = HeaderCategories()
		else:
			self.hc = hc
		if su is None:
			self.su = sql_utlis.SqlUtilities()
		else:
			self.su = su
		
		# Build the CRF elements
		if s.pickle_exists('CRF'):
			self.CRF = s.load_object('CRF')
		else:
			import sklearn_crfsuite
			self.CRF = sklearn_crfsuite.CRF(algorithm='lbfgs',c1=0.1,c2=0.1,max_iterations=100,all_possible_transitions=True)
			HEADER_PATTERN_DICT = s.load_object('HEADER_PATTERN_DICT')
			X_train = []
			y_train = []
			for file_name, feature_dict_list in HEADER_PATTERN_DICT.items():
				X_train.append(feature_dict_list)
				pos_list = [self.hc.get_feature_tuple(feature_dict)[2] for feature_dict in feature_dict_list]
				y_train.append(pos_list)
			try:
				self.CRF.fit(X_train, y_train)
			except Exception as e:
				print(str(e).strip())
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
		null_element = 'plaintext'
		this_sent = sent[i]
		tag = this_sent[0]
		child_str = this_sent[1]
		postag = this_sent[2]
		
		features = {
			'bias': 1.0,
			'child_str.lr_predict_single': self.lr_predict_single(child_str),
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

class LrUtilities(object):
	"""Logistic Regression utilities class."""
	
	def __init__(self, ha=None, hc=None, su=None, verbose=False):
		if ha is None:
			self.ha = HeaderAnalysis()
		else:
			self.ha = ha
		if hc is None:
			self.hc = HeaderCategories()
		else:
			self.hc = hc
		if su is None:
			self.su = sql_utlis.SqlUtilities()
		else:
			self.su = su
		
		# Build the Logistic Regression elements
		self.conn, self.cursor = self.su.get_jh_conn_cursor()
		self.LR_DICT = {}
		self.PREDICT_PERCENT_FIT_DICT = {}
		
		# Train a model for each labeled POS symbol
		sql_str = '''
			SELECT
				np.[navigable_parent],
				pos.[pos_symbol]
			FROM
				[Jobhunting].[dbo].[NavigableParents] np INNER JOIN
				[Jobhunting].[dbo].[PartsOfSpeech] pos ON
					pos.[is_header] = np.[is_header] AND
					pos.[is_task_scope] = np.[is_task_scope] AND
					pos.[is_minimum_qualification] = np.[is_minimum_qualification] AND
					pos.[is_preferred_qualification] = np.[is_preferred_qualification] AND
					pos.[is_legal_notification] = np.[is_legal_notification] AND
					pos.[is_job_title] = np.[is_job_title] AND
					pos.[is_office_location] = np.[is_office_location] AND
					pos.[is_job_duration] = np.[is_job_duration] AND
					pos.[is_supplemental_pay] = np.[is_supplemental_pay] AND
					pos.[is_educational_requirement] = np.[is_educational_requirement] AND
					pos.[is_interview_procedure] = np.[is_interview_procedure] AND
					pos.[is_corporate_scope] = np.[is_corporate_scope] AND
					pos.[is_posting_date] = np.[is_posting_date] AND
					pos.[is_other] = np.[is_other];'''
		pos_df = pd.DataFrame(self.su.get_execution_results(self.cursor, sql_str, verbose=verbose))
		
		# The shape of the Bag-of-words count vector here should be n html strings * m unique tokens
		sents_list = pos_df.navigable_parent.tolist()
		pos_symbol_list = pos_df.pos_symbol.unique().tolist()
		
		# Re-transform the bag-of-words and tf-idf from the new manual scores
		self.CV = CountVectorizer(analyzer='word', binary=False, decode_error='strict', lowercase=False, max_df=1.0, max_features=None,
								  min_df=0.0, ngram_range=(1, 5), stop_words=None, strip_accents='ascii', tokenizer=self.ha.html_regex_tokenizer)
		bow_matrix = self.CV.fit_transform(sents_list)
		
		# Tf-idf must get from Bag-of-words first
		self.TT = TfidfTransformer(norm='l1', smooth_idf=True, sublinear_tf=False, use_idf=True)
		tfidf_matrix = self.TT.fit_transform(bow_matrix)
		X = tfidf_matrix.toarray()
		
		for pos_symbol in pos_symbol_list:
			
			# Train the classifier
			mask_series = (pos_df.pos_symbol == pos_symbol)
			y = mask_series.to_numpy()
			if pos_symbol not in self.LR_DICT:
				self.LR_DICT[pos_symbol] = LogisticRegression(C=375.0, class_weight='balanced', dual=False,
															  fit_intercept=True, intercept_scaling=1,
															  l1_ratio=None, max_iter=1000,
															  multi_class='auto', n_jobs=None, penalty='l1',
															  random_state=None, solver='liblinear',
															  tol=0.0001, verbose=verbose, warm_start=False)
			try:
				self.LR_DICT[pos_symbol].fit(X, y)
				self.PREDICT_PERCENT_FIT_DICT[pos_symbol] = self.build_lr_predict_percent(pos_symbol, verbose=verbose)
			except ValueError as e:
				print(f'{pos_symbol} had this error: {str(e).strip()}')
				self.LR_DICT.pop(pos_symbol, None)
				self.PREDICT_PERCENT_FIT_DICT.pop(pos_symbol, None)
	
	###################################
	## Logistic Regression functions ##
	###################################
	def lr_predict_single(self, html_str, verbose=False):
		tuple_list = []
		for pos_symbol, predict_percent_fit in self.PREDICT_PERCENT_FIT_DICT.items():
			if predict_percent_fit is None:
				proba_tuple = (pos_symbol, 0.0)
				tuple_list.append(proba_tuple)
			else:
				proba_tuple = (pos_symbol, predict_percent_fit(html_str))
				tuple_list.append(proba_tuple)
		tuple_list.sort(reverse=True, key=lambda x: x[1])
		
		return tuple_list[0][0]
	
	def build_lr_predict_percent(self, pos_symbol, verbose=False):
		predict_percent_fit = None
		if pos_symbol in self.LR_DICT:
			
			def predict_percent_fit(navigable_parent):
				
				# Re-calibrate the inference engine
				cv = CountVectorizer(vocabulary=self.CV.vocabulary_)
				cv._validate_vocabulary()
				
				X_test = self.TT.transform(cv.transform([navigable_parent])).toarray()
				y_predict_proba = self.LR_DICT[pos_symbol].predict_proba(X_test)[0][1]

				return y_predict_proba
		
		return predict_percent_fit
	
	def build_lr_predict_percent_is_header(self):
		from sklearn.feature_extraction.text import CountVectorizer
		from sklearn.feature_extraction.text import TfidfTransformer
		from sklearn.linear_model import LogisticRegression
		
		# Re-transform the bag-of-words and tf-idf from the new manual scores
		rows_list = [{'navigable_parent': navigable_parent,
					  'is_header': is_header} for navigable_parent, is_header in self.ha.NAVIGABLE_PARENT_IS_HEADER_DICT.items()]
		child_str_df = pd.DataFrame(rows_list)
		child_str_df.is_header = child_str_df.is_header.astype('bool')
		
		# The shape of the Bag-of-words count vector here should be n sentences * m unique words
		sents_list = child_str_df.navigable_parent.tolist()
		bow_matrix = self.CV.fit_transform(sents_list)
		
		# Tf-idf must get from Bag-of-words first
		tfidf_matrix = self.TT.fit_transform(bow_matrix)
		
		# Re-train the classifier
		X = tfidf_matrix.toarray()
		y = child_str_df.is_header.to_numpy()
		self.CHILD_STR_CLF.fit(X, y)
		s.store_objects(CHILD_STR_CLF=self.CHILD_STR_CLF)
		
		# Re-calibrate the inference engine
		cv = CountVectorizer(vocabulary=self.CS_CV.vocabulary_)
		cv._validate_vocabulary()
		
		def predict_percent_fit(navigable_parent):
			X_test = self.TT.transform(cv.transform([navigable_parent])).toarray()
			y_predict_proba = self.CHILD_STR_CLF.predict_proba(X_test)[0][1]
			
			return y_predict_proba
		
		return predict_percent_fit

class ElementAnalysis(object):
	"""Element analysis class."""
	
	def __init__(self, ha=None, hc=None):
		if ha is None:
			self.ha = HeaderAnalysis()
		else:
			self.ha = ha
		if hc is None:
			self.hc = HeaderCategories()
		else:
			self.hc = hc
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

	def get_idx_list(self, items_list, item_str):
		item_count = items_list.count(item_str)
		idx_list = []
		idx = -1
		while len(idx_list) < item_count:
			idx = items_list.index(item_str, idx+1)
			idx_list.append(idx)

		return idx_list
	
	def find_basic_quals_section(self, child_strs_list):
		try:
			import sql_utlis
			su = sql_utlis.SqlUtilities()
		except:
			from flaskr.sql_utlis import SqlUtilities
			su = SqlUtilities()
		child_tags_list = su.get_child_tags_list(db, child_strs_list)
		is_header_list = su.get_is_header_list(db, child_strs_list)
		
		feature_dict_list = su.get_feature_dict_list(db, child_tags_list, child_strs_list)
		feature_tuple_list = [self.hc.get_feature_tuple(feature_dict) for feature_dict in feature_dict_list]
		
		crf_list = self.CRF.predict_single(self.sent2features(feature_tuple_list))
		pos_list = []
		for pos, feature_tuple, is_header in zip(crf_list, feature_tuple_list, is_header_list):
			navigable_parent = feature_tuple[1]
			if is_header:
				pos_list = su.append_parts_of_speech_list(db, navigable_parent, pos_list=[])
			else:
				pos_list.append(pos)
		db.close()
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