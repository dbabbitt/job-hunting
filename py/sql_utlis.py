
#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import random
import sqlite3
import os

try:
	import storage
	s = storage.Storage()
except:
	from flaskr.storage import Storage
	s = Storage()

try:
	import html_analysis
	ha = html_analysis.HeaderAnalysis()
except:
	from flaskr.html_analysis import HeaderAnalysis
	ha = HeaderAnalysis()

class SqlUtilities(object):
	"""SQL class."""
	
	def __init__(self):
		
		# Various SQL strings
		self.create_table_sql_str = """
CREATE TABLE HeaderTagSequence(
	header_tag_sequence_id INT PRIMARY KEY,
	file_name VARCHAR (255) NOT NULL,
	header_tag NVARCHAR (2224) NOT NULL,
	sequence_order INT NOT NULL
);
SELECT * FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = N'HeaderTagSequence';"""
		self.insert_columns_sql_str = """
INSERT INTO HeaderTagSequence (
	header_tag_sequence_id,
	file_name,
	header_tag,
	sequence_order
) values(
	?,
	?,
	?,
	?
);"""
		self.create_query_table_sql_str = """
DROP TABLE IF EXISTS dbo.#query;
CREATE TABLE #query(
	header_tag NVARCHAR (2224) NOT NULL,
	sequence_order INT NOT NULL
);"""
		self.insert_query_rows_sql_str = """
INSERT INTO #query (
	header_tag,
	sequence_order
) values(
	?,
	?
);"""
		self.select_query_rows_sql_str = """
SELECT * FROM #query;"""
		self.select_query_sql_str = """
SELECT file_name
FROM HeaderTagSequence s
	INNER JOIN #query q
	ON
		q.header_tag = s.header_tag AND
		q.sequence_order = s.sequence_order
GROUP BY s.file_name
HAVING Count(*) = (SELECT Count(*) FROM #query)"""
		
		# The email date is field TEXT as ISO8601 strings ("YYYY-MM-DD HH:MM:SS.SSS")
		self.create_filenames_table_sql_str = """
CREATE TABLE FileNames(
	file_name_id INTEGER PRIMARY KEY AUTOINCREMENT,
	file_name TEXT NOT NULL,
	percent_fit REAL NULL,
	is_opportunity_application_emailed BIT NULL,
	opportunity_application_email_date TEXT NULL,
	is_remote_delivery BIT NULL,
	manager_notes TEXT NULL
);"""
		
		self.create_headertags_table_sql_str = """
CREATE TABLE HeaderTags(
	header_tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
	header_tag TEXT NOT NULL,
	is_in_document_structure_elements_set BIT NULL,
	is_in_document_head_elements_set BIT NULL,
	is_in_document_body_elements_set BIT NULL,
	is_in_block_elements_set BIT NULL,
	is_in_basic_text_set BIT NULL,
	is_in_section_headings_set BIT NULL,
	is_in_lists_set BIT NULL,
	is_in_other_block_elements_set BIT NULL,
	is_in_inline_elements_set BIT NULL,
	is_in_anchor_set BIT NULL,
	is_in_phrase_elements_set BIT NULL,
	is_in_general_set BIT NULL,
	is_in_computer_phrase_elements_set BIT NULL,
	is_in_presentation_set BIT NULL,
	is_in_span_set BIT NULL,
	is_in_other_inline_elements_set BIT NULL,
	is_in_images_and_objects_set BIT NULL,
	is_in_forms_set BIT NULL,
	is_in_tables_set BIT NULL,
	is_in_frames_set BIT NULL,
	is_in_historic_elements_set BIT NULL,
	is_in_non_standard_elements_set BIT NULL
);"""
		self.create_navigableparents_table_sql_str = """
CREATE TABLE NavigableParents (
	navigable_parent_id INTEGER PRIMARY KEY AUTOINCREMENT,
	navigable_parent TEXT NOT NULL,
	header_tag_id INTEGER NULL,
	is_header BIT NULL,
	is_task_scope BIT NULL,
	is_minimum_qualification BIT NULL,
	is_preferred_qualification BIT NULL,
	is_legal_notification BIT NULL,
	is_job_title BIT NULL,
	is_office_location BIT NULL,
	is_job_duration BIT NULL,
	is_supplemental_pay BIT NULL,
	is_educational_requirement BIT NULL,
	is_interview_procedure BIT NULL,
	is_corporate_scope BIT NULL,
	is_posting_date BIT NULL,
	is_other BIT NULL,
	is_qualification BIT NULL
);"""
		self.create_headertagsequence_table_sql_str = """
CREATE TABLE HeaderTagSequence(
	header_tag_sequence_id INTEGER PRIMARY KEY AUTOINCREMENT,
	file_name_id INTEGER NOT NULL,
	header_tag_id INTEGER NOT NULL,
	sequence_order INTEGER NOT NULL
);"""
		self.create_navigableparentsequence_table_sql_str = """
CREATE TABLE NavigableParentSequence(
	navigable_parent_sequence_id INTEGER PRIMARY KEY AUTOINCREMENT,
	file_name_id INTEGER NOT NULL,
	navigable_parent_id INTEGER NOT NULL,
	sequence_order INTEGER NOT NULL
);"""
		self.set_is_corporate_scope1_sql_str = """
UPDATE NavigableParents
SET is_header = 1, is_corporate_scope = 1
WHERE (navigable_parent = ?)"""
		self.set_is_header1_sql_str = """
UPDATE NavigableParents
SET is_header = 1
WHERE (navigable_parent = ?)"""
		self.set_is_header0_sql_str = """
UPDATE NavigableParents
SET is_header = 0
WHERE (navigable_parent = ?)"""
		self.set_is_qualification1_sql_str = """
UPDATE NavigableParents
SET is_qualification = 1
WHERE (navigable_parent = ?)"""
		self.set_is_qualification0_sql_str = """
UPDATE NavigableParents
SET is_qualification = 0
WHERE (navigable_parent = ?)"""
		self.set_is_task_scope1_sql_str = """
UPDATE NavigableParents
SET is_header = 1, is_task_scope = 1
WHERE (navigable_parent = ?)"""
		self.set_is_office_location1_sql_str = """
UPDATE NavigableParents
SET is_header = 1, is_office_location = 1
WHERE (navigable_parent = ?)"""
		self.set_is_minimum_qualification1_sql_str = """
UPDATE NavigableParents
SET is_header = 1, is_minimum_qualification = 1
WHERE (navigable_parent = ?)"""
		self.set_is_supplemental_pay1_sql_str = """
UPDATE NavigableParents
SET is_header = 1, is_supplemental_pay = 1
WHERE (navigable_parent = ?)"""
		self.set_nonheader_is_supplemental_pay1_sql_str = """
UPDATE NavigableParents
SET is_header = 0, is_supplemental_pay = 1
WHERE (navigable_parent = ?)"""
		self.set_is_preferred_qualification1_sql_str = """
UPDATE NavigableParents
SET is_header = 1, is_preferred_qualification = 1
WHERE (navigable_parent = ?)"""
		self.set_is_legal_notification1_sql_str = """
UPDATE NavigableParents
SET is_header = 1, is_legal_notification = 1
WHERE (navigable_parent = ?)"""
		self.set_is_other1_sql_str = """
UPDATE NavigableParents
SET is_header = 1, is_other = 1
WHERE (navigable_parent = ?)"""
		self.set_is_educational_requirement1_sql_str = """
UPDATE NavigableParents
SET is_header = 1, is_educational_requirement = 1
WHERE (navigable_parent = ?)"""
		self.set_is_interview_procedure1_sql_str = """
UPDATE NavigableParents
SET is_header = 1, is_interview_procedure = 1
WHERE (navigable_parent = ?)"""
		self.set_is_posting_date1_sql_str = """
UPDATE NavigableParents
SET is_header = 1, is_posting_date = 1
WHERE (navigable_parent = ?)"""
		self.set_is_job_duration1_sql_str = """
UPDATE NavigableParents
SET is_header = 1, is_job_duration = 1
WHERE (navigable_parent = ?)"""
		self.set_is_job_title1_sql_str = """
UPDATE NavigableParents
SET is_header = 1, is_job_title = 1
WHERE (navigable_parent = ?)"""
		self.create_table_partsofspeech_sql_str = """
CREATE TABLE PartsOfSpeech(
	pos_id INTEGER PRIMARY KEY AUTOINCREMENT,
	pos_symbol TEXT NOT NULL,
	pos_explanation TEXT NOT NULL
);"""
		self.insert_into_headertags_sql_str = """
INSERT INTO HeaderTags (
	header_tag, 
	is_in_document_structure_elements_set, 
	is_in_document_head_elements_set, 
	is_in_document_body_elements_set, 
	is_in_block_elements_set, 
	is_in_basic_text_set, 
	is_in_section_headings_set, 
	is_in_lists_set, 
	is_in_other_block_elements_set, 
	is_in_inline_elements_set, 
	is_in_anchor_set, 
	is_in_phrase_elements_set, 
	is_in_general_set, 
	is_in_computer_phrase_elements_set, 
	is_in_presentation_set, 
	is_in_span_set, 
	is_in_other_inline_elements_set, 
	is_in_images_and_objects_set, 
	is_in_forms_set, 
	is_in_tables_set, 
	is_in_frames_set, 
	is_in_historic_elements_set, 
	is_in_non_standard_elements_set
	) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
		self.select_is_from_navigableparents_sql_str = """
SELECT
	is_header,
	is_task_scope,
	is_minimum_qualification,
	is_preferred_qualification,
	is_legal_notification,
	is_job_title,
	is_office_location,
	is_job_duration,
	is_supplemental_pay,
	is_educational_requirement,
	is_interview_procedure,
	is_corporate_scope,
	is_posting_date,
	is_other
FROM NavigableParents
WHERE navigable_parent = ?"""
		self.select_file_name_where_is_qualification_sql_str = """
SELECT file_name 
FROM FileNames 
WHERE file_name_id IN (
	SELECT file_name_id 
	FROM NavigableParentSequence 
	WHERE navigable_parent_id IN (
		SELECT navigable_parent_id 
		FROM NavigableParents 
		WHERE
			is_minimum_qualification = 1 AND
			is_header = 1
		)
	)"""
		self.select_navigable_parent_id_where_navigable_parent_sql_str = """
SELECT
	navigable_parent_id,
	is_minimum_qualification
FROM NavigableParents
WHERE navigable_parent = ?"""
		self.set_secondary_column0_formatted_sql_str = """
UPDATE NavigableParents
SET {} = 0
WHERE
	{} = 1 AND
	{} IS NULL;"""
		self.set_is_qualification1_or_sql_str = """
UPDATE NavigableParents
SET is_qualification = 1
WHERE
	is_minimum_qualification = 1 OR
	is_preferred_qualification = 1;"""
		self.select_navigable_parent_by_file_name_sql_str = """
SELECT navigable_parent
FROM NavigableParents
WHERE navigable_parent_id in (
	SELECT navigable_parent_id
	FROM NavigableParentSequence
	WHERE file_name_id = (
		SELECT file_name_id
		FROM FileNames
		WHERE file_name = ?
		)
	ORDER BY sequence_order ASC
	);"""
	
	
	
	def create_filenames_table(self, db, verbose=False):
		db.execute('DROP TABLE IF EXISTS FileNames;')
		db.execute(self.create_filenames_table_sql_str)
		db.commit()
	
	
	
	def populate_filenames_table(self, db, verbose=False):
		files_list = os.listdir(ha.SAVES_HTML_FOLDER)
		for file_name in files_list:
			if file_name.endswith('html'):
				db.execute('INSERT INTO FileNames (file_name) VALUES (?)', (file_name,))
		db.commit()
	
	
	
	def create_headertags_table(self, db, verbose=False):
		db.execute('DROP TABLE IF EXISTS HeaderTags;')
		db.execute(self.create_headertags_table_sql_str)
		db.commit()
	
	
	
	def populate_headertags_table(self, db, verbose=False):
		document_structure_elements_set = set(['body','head','html'])
		document_head_elements_set = set(['base','basefont','isindex','link','meta','object','script','style','title'])
		document_body_elements_set = set(['a','abbr','acronym','address','applet','area','article','aside','audio','b','bdi','bdo','big','blockquote','br','button','canvas','caption','center','cite','code','col','colgroup','data','datalist','dd','del','dfn','dir','div','dl','dt','em','embed','fieldset','figcaption','figure','font','footer','form','h1','h2','h3','h4','h5','h6','header','hr','i','img','input','ins','isindex','kbd','keygen','label','legend','li','main','map','mark','menu','meter','nav','noscript','object','ol','optgroup','option','output','p','param','pre','progress','q','rb','rp','rt','rtc','ruby','s','samp','script','section','select','small','source','span','strike','strong','sub','sup','table','tbody','td','template','textarea','tfoot','th','thead','time','tr','track','tt','u','ul','var','video','wbr'])
		block_elements_set = set(['address','article','aside','blockquote','center','dd','del','dir','div','dl','dt','figcaption','figure','footer','h1','h2','h3','h4','h5','h6','header','hr','ins','li','main','menu','nav','noscript','ol','p','pre','script','section','ul'])
		basic_text_set = set(['h1','h2','h3','h4','h5','h6','p'])
		section_headings_set = set(['h1','h2','h3','h4','h5','h6'])
		lists_set = set(['dd','dir','dl','dt','li','ol','ul'])
		other_block_elements_set = set(['address','article','aside','blockquote','center','del','div','figcaption','figure','footer','header','hr','ins','main','menu','nav','noscript','pre','script','section'])
		inline_elements_set = set(['a','abbr','acronym','b','bdi','bdo','big','br','cite','code','data','del','dfn','em','font','i','ins','kbd','mark','q','rb','rp','rt','rtc','ruby','s','samp','script','small','span','strike','strong','sub','sup','template','time','tt','u','var','wbr'])
		anchor_set = set(['a'])
		phrase_elements_set = set(['abbr','acronym','b','big','code','dfn','em','font','i','kbd','s','samp','small','strike','strong','tt','u','var'])
		general_set = set(['abbr','acronym','dfn','em','strong'])
		computer_phrase_elements_set = set(['code','kbd','samp','var'])
		presentation_set = set(['b','big','font','i','s','small','strike','tt','u'])
		span_set = set(['span'])
		other_inline_elements_set = set(['bdi','bdo','br','cite','data','del','ins','mark','q','rb','rp','rt','rtc','ruby','script','sub','sup','template','time','wbr'])
		images_and_objects_set = set(['applet','area','audio','canvas','embed','img','map','object','param','source','track','video'])
		forms_set = set(['button','datalist','fieldset','form','input','isindex','keygen','label','legend','meter','optgroup','option','output','progress','select','textarea'])
		tables_set = set(['caption','col','colgroup','table','tbody','td','tfoot','th','thead','tr'])
		frames_set = set(['frame','frameset','iframe','noframes'])
		historic_elements_set = set(['listing','nextid','plaintext','xmp'])
		non_standard_elements_set = set(['blink','layer','marquee','nobr','noembed'])
		union_set = set().union(document_structure_elements_set, document_head_elements_set, document_body_elements_set, block_elements_set, basic_text_set, section_headings_set, lists_set, other_block_elements_set, inline_elements_set, anchor_set, phrase_elements_set, general_set, computer_phrase_elements_set, presentation_set, span_set, other_inline_elements_set, images_and_objects_set, forms_set, tables_set, frames_set, historic_elements_set, non_standard_elements_set)
		child_tags_list = sorted(union_set)
		for child_tag in child_tags_list:
			is_in_document_structure_elements_set = (child_tag in document_structure_elements_set)
			is_in_document_head_elements_set = (child_tag in document_head_elements_set)
			is_in_document_body_elements_set = (child_tag in document_body_elements_set)
			is_in_block_elements_set = (child_tag in block_elements_set)
			is_in_basic_text_set = (child_tag in basic_text_set)
			is_in_section_headings_set = (child_tag in section_headings_set)
			is_in_lists_set = (child_tag in lists_set)
			is_in_other_block_elements_set = (child_tag in other_block_elements_set)
			is_in_inline_elements_set = (child_tag in inline_elements_set)
			is_in_anchor_set = (child_tag in anchor_set)
			is_in_phrase_elements_set = (child_tag in phrase_elements_set)
			is_in_general_set = (child_tag in general_set)
			is_in_computer_phrase_elements_set = (child_tag in computer_phrase_elements_set)
			is_in_presentation_set = (child_tag in presentation_set)
			is_in_span_set = (child_tag in span_set)
			is_in_other_inline_elements_set = (child_tag in other_inline_elements_set)
			is_in_images_and_objects_set = (child_tag in images_and_objects_set)
			is_in_forms_set = (child_tag in forms_set)
			is_in_tables_set = (child_tag in tables_set)
			is_in_frames_set = (child_tag in frames_set)
			is_in_historic_elements_set = (child_tag in historic_elements_set)
			is_in_non_standard_elements_set = (child_tag in non_standard_elements_set)
			params_tuple = (child_tag, is_in_document_structure_elements_set, is_in_document_head_elements_set,
							is_in_document_body_elements_set, is_in_block_elements_set, is_in_basic_text_set,
							is_in_section_headings_set, is_in_lists_set, is_in_other_block_elements_set,
							is_in_inline_elements_set, is_in_anchor_set, is_in_phrase_elements_set,
							is_in_general_set, is_in_computer_phrase_elements_set, is_in_presentation_set,
							is_in_span_set, is_in_other_inline_elements_set, is_in_images_and_objects_set, is_in_forms_set,
							is_in_tables_set, is_in_frames_set, is_in_historic_elements_set, is_in_non_standard_elements_set)
			db.execute(self.insert_into_headertags_sql_str, params_tuple)
		db.commit()
	
	
	
	def create_navigableparents_table(self, db, verbose=False):
		db.execute('DROP TABLE IF EXISTS NavigableParents;')
		db.execute(self.create_navigableparents_table_sql_str)
		db.commit()
	
	
	
	def populate_navigableparents_table(self, db, verbose=False):
		files_list = os.listdir(ha.SAVES_HTML_FOLDER)
		navigable_parent_set = set()
		for file_name in files_list:
			child_strs_list = ha.get_child_strs_from_file(file_name)
			for child_str in child_strs_list:
				navigable_parent_set.add(child_str)
		child_strs_list = sorted(navigable_parent_set)
		child_tags_list = ha.get_child_tags_list(child_strs_list)
		for child_str, child_tag in zip(child_strs_list, child_tags_list):
			header_tag_id = db.execute('SELECT header_tag_id FROM HeaderTags WHERE header_tag = ?',
									   (child_tag,)).fetchone()['header_tag_id']
			db.execute('INSERT INTO NavigableParents (navigable_parent, header_tag_id) VALUES (?, ?)',
					   (child_str, header_tag_id))
		
		# Set the Corporate Scope is_header
		corp_scope_headers_list = s.load_object('corp_scope_headers_list')
		for navigable_parent in corp_scope_headers_list:
			db.execute(self.set_is_corporate_scope1_sql_str, (navigable_parent,))
		
		# Set the basic tags is_header
		NAVIGABLE_PARENT_IS_HEADER_DICT = s.load_object('NAVIGABLE_PARENT_IS_HEADER_DICT')
		for navigable_parent, is_header in NAVIGABLE_PARENT_IS_HEADER_DICT.items():
			if is_header:
				db.execute(self.set_is_header1_sql_str, (navigable_parent,))
			else:
				db.execute(self.set_is_header0_sql_str, (navigable_parent,))
		
		# Set the basic tags is_qual
		NAVIGABLE_PARENT_IS_QUAL_DICT = s.load_object('NAVIGABLE_PARENT_IS_QUAL_DICT')
		for navigable_parent, is_qualification in NAVIGABLE_PARENT_IS_QUAL_DICT.items():
			if is_qualification:
				db.execute(self.set_is_qualification1_sql_str, (navigable_parent,))
			else:
				db.execute(self.set_is_qualification0_sql_str, (navigable_parent,))
		
		# Set the Task Scope is_header
		task_scope_headers_list = s.load_object('task_scope_headers_list')
		for navigable_parent in task_scope_headers_list:
			db.execute(self.set_is_task_scope1_sql_str, (navigable_parent,))
		
		# Set the Office Location is_header
		office_loc_headers_list = s.load_object('office_loc_headers_list')
		for navigable_parent in office_loc_headers_list:
			db.execute(self.set_is_office_location1_sql_str, (navigable_parent,))
		
		# Set the Minimum Quals is_header
		req_quals_headers_list = s.load_object('req_quals_headers_list')
		for navigable_parent in req_quals_headers_list:
			db.execute(self.set_is_minimum_qualification1_sql_str, (navigable_parent,))
		
		# Set the Supplemental Pay is_header
		supp_pay_headers_list = s.load_object('supp_pay_headers_list')
		for navigable_parent in supp_pay_headers_list:
			db.execute(self.set_is_supplemental_pay1_sql_str, (navigable_parent,))
		
		# Set the Supplemental Pay non-header
		supp_pay_nonheaders_list = s.load_object('supp_pay_nonheaders_list')
		for navigable_parent in supp_pay_nonheaders_list:
			db.execute(self.set_nonheader_is_supplemental_pay1_sql_str, (navigable_parent,))
		
		# Set the Preferred Quals is_header
		preff_quals_headers_list = s.load_object('preff_quals_headers_list')
		for navigable_parent in preff_quals_headers_list:
			db.execute(self.set_is_preferred_qualification1_sql_str, (navigable_parent,))
		
		# Set the Legal Notifications is_header
		legal_notifs_headers_list = s.load_object('legal_notifs_headers_list')
		for navigable_parent in legal_notifs_headers_list:
			db.execute(self.set_is_legal_notification1_sql_str, (navigable_parent,))
		
		# Set the Other is_header
		other_headers_list = s.load_object('other_headers_list')
		for navigable_parent in other_headers_list:
			db.execute(self.set_is_other1_sql_str, (navigable_parent,))
		
		# Set the Education Requirements is_header
		educ_reqs_headers_list = s.load_object('educ_reqs_headers_list')
		for navigable_parent in educ_reqs_headers_list:
			db.execute(self.set_is_educational_requirement1_sql_str, (navigable_parent,))
		
		# Set the Interview Process is_header
		interv_proc_headers_list = s.load_object('interv_proc_headers_list')
		for navigable_parent in interv_proc_headers_list:
			db.execute(self.set_is_interview_procedure1_sql_str, (navigable_parent,))
		
		# Set the Posting Date is_header
		post_date_headers_list = s.load_object('post_date_headers_list')
		for navigable_parent in post_date_headers_list:
			db.execute(self.set_is_posting_date1_sql_str, (navigable_parent,))
		
		# Set the Job Duration is_header
		job_duration_headers_list = s.load_object('job_duration_headers_list')
		for navigable_parent in job_duration_headers_list:
			db.execute(self.set_is_job_duration1_sql_str, (navigable_parent,))
		
		# Set the Job Title is_header
		job_title_headers_list = s.load_object('job_title_headers_list')
		for navigable_parent in job_title_headers_list:
			db.execute(self.set_is_job_title1_sql_str, (navigable_parent,))
		
		# SET other subtypes as 0; assume 0 rows affected if primary and secondary columns are the same
		subtypes_list = ['is_task_scope', 'is_minimum_qualification', 'is_preferred_qualification', 'is_legal_notification',
						 'is_job_title', 'is_office_location', 'is_job_duration', 'is_supplemental_pay',
						 'is_educational_requirement', 'is_interview_procedure', 'is_corporate_scope', 'is_posting_date',
						 'is_other']
		for primary_column in subtypes_list:
			for secondary_column in subtypes_list:
				db.execute(self.set_secondary_column0_formatted_sql_str.format(secondary_column, primary_column, secondary_column))
		
		# Set the is_qualification if the other qual columns are set
		db.execute(self.set_is_qualification1_or_sql_str)
		
		db.commit()
	
	
	
	def create_headertagsequence_table(self, db, verbose=False):
		db.execute('DROP TABLE IF EXISTS HeaderTagSequence;')
		db.execute(self.create_headertagsequence_table_sql_str)
		db.commit()
	
	
	
	def populate_headertagsequence_table(self, db, verbose=False):
		files_list = os.listdir(ha.SAVES_HTML_FOLDER)
		for file_name in files_list:
			file_name_id = db.execute('SELECT file_name_id FROM FileNames WHERE file_name = ?', (file_name,)).fetchone()['file_name_id']
			child_strs_list = ha.get_child_strs_from_file(file_name)
			child_tags_list = ha.get_child_tags_list(child_strs_list)
			for sequence_order, header_tag in enumerate(child_tags_list):
				header_tag_id = db.execute('SELECT header_tag_id FROM HeaderTags WHERE header_tag = ?', (header_tag,)).fetchone()['header_tag_id']
				db.execute('INSERT INTO HeaderTagSequence (file_name_id, header_tag_id, sequence_order) VALUES (?, ?, ?)',
						   (file_name_id, header_tag_id, sequence_order))
		db.commit()
	
	
	
	def create_navigableparentsequence_table(self, db, verbose=False):
		db.execute('DROP TABLE IF EXISTS NavigableParentSequence;')
		db.execute(self.create_navigableparentsequence_table_sql_str)
		db.commit()
	
	
	
	def populate_navigableparentsequence_table(self, db, verbose=False):
		files_list = os.listdir(ha.SAVES_HTML_FOLDER)
		for file_name in files_list:
			file_name_id = db.execute('SELECT file_name_id FROM FileNames WHERE file_name = ?', (file_name,)).fetchone()['file_name_id']
			child_strs_list = ha.get_child_strs_from_file(file_name)
			for sequence_order, navigable_parent in enumerate(child_strs_list):
				navigable_parent_id = db.execute('SELECT navigable_parent_id FROM NavigableParents WHERE navigable_parent = ?',
												 (navigable_parent,)).fetchone()['navigable_parent_id']
				db.execute('INSERT INTO NavigableParentSequence (file_name_id, navigable_parent_id, sequence_order) VALUES (?, ?, ?)',
						   (file_name_id, navigable_parent_id, sequence_order))
		db.commit()
	
	
	
	def create_partsofspeech_table(self, db, verbose=False):
		db.execute('DROP TABLE IF EXISTS PartsOfSpeech;')
		db.execute(self.create_table_partsofspeech_sql_str)
		db.commit()
	
	
	
	def populate_partsofspeech_table(self, db, verbose=False):
		pos_explanation_dict = s.load_object('pos_explanation_dict')
		for pos_symbol, pos_explanation in pos_explanation_dict.items():
			if pos_symbol.startswith('H-'):
				db.execute('INSERT INTO PartsOfSpeech (pos_symbol, pos_explanation) VALUES (?, ?)',
						   (pos_symbol, pos_explanation))
				db.execute('INSERT INTO PartsOfSpeech (pos_symbol, pos_explanation) VALUES (?, ?)',
						   (pos_symbol.replace('H-', 'O-'), pos_explanation.replace(' Header', ' Non-header')))
		db.commit()
	
	
	
	def get_is_header_list(self, db, child_strs_list, verbose=False):
		is_header_list = []
		for navigable_parent in child_strs_list:
			is_header = db.execute('SELECT is_header FROM NavigableParents WHERE navigable_parent = ?',
								   (navigable_parent,)).fetchone()['is_header']
			is_header_list.append(is_header)
		
		return is_header_list
	
	
	
	def get_child_strs_from_file(self, db, file_name, verbose=False):
		cursor_obj = db.execute(self.select_navigable_parent_by_file_name_sql_str, (file_name,))
		row_obj_list = cursor_obj.fetchall()
		child_strs_list = [row_obj['navigable_parent'] for row_obj in row_obj_list]
		
		return child_strs_list
	
	
	
	def get_child_tags_list(self, db, child_strs_list, verbose=False):
		child_tags_list = []
		for navigable_parent in child_strs_list:
			header_tag_id = db.execute('SELECT header_tag_id FROM NavigableParents WHERE navigable_parent = ?',
									   (navigable_parent,)).fetchone()['header_tag_id']
			header_tag = db.execute('SELECT header_tag FROM HeaderTags WHERE header_tag_id = ?',
									(header_tag_id,)).fetchone()['header_tag']
			child_tags_list.append(header_tag)
		
		return child_tags_list
	
	
	
	def get_feature_dict_list(self, db, child_tags_list, child_strs_list, verbose=False):
		feature_dict_list = []
		import numpy as np
		for tag, child_str in zip(child_tags_list, child_strs_list):
			feature_dict = {}
			feature_dict['initial_tag'] = tag
			if verbose:
				print(self.select_is_from_navigableparents_sql_str.replace('?', '"{}"').format(child_str))
			params_dict = db.execute(self.select_is_from_navigableparents_sql_str, (child_str,)).fetchone()
			if params_dict is None:
				params_dict = {'is_header': np.nan, 'is_task_scope': np.nan, 'is_minimum_qualification': np.nan,
							   'is_preferred_qualification': np.nan, 'is_legal_notification': np.nan,
							   'is_job_title': np.nan, 'is_office_location': np.nan, 'is_job_duration': np.nan,
							   'is_supplemental_pay': np.nan, 'is_educational_requirement': np.nan,
							   'is_interview_procedure': np.nan, 'is_corporate_scope': np.nan,
							   'is_posting_date': np.nan, 'is_other': np.nan}
			feature_dict['is_header'] = params_dict['is_header']
			feature_dict['is_task_scope'] = params_dict['is_task_scope']
			feature_dict['is_minimum_qualification'] = params_dict['is_minimum_qualification']
			feature_dict['is_preferred_qualification'] = params_dict['is_preferred_qualification']
			feature_dict['is_legal_notification'] = params_dict['is_legal_notification']
			feature_dict['is_job_title'] = params_dict['is_job_title']
			feature_dict['is_office_location'] = params_dict['is_office_location']
			feature_dict['is_job_duration'] = params_dict['is_job_duration']
			feature_dict['is_supplemental_pay'] = params_dict['is_supplemental_pay']
			feature_dict['is_educational_requirement'] = params_dict['is_educational_requirement']
			feature_dict['is_interview_procedure'] = params_dict['is_interview_procedure']
			feature_dict['is_corporate_scope'] = params_dict['is_corporate_scope']
			feature_dict['is_posting_date'] = params_dict['is_posting_date']
			feature_dict['is_other'] = params_dict['is_other']
			feature_dict['child_str'] = child_str
			feature_dict_list.append(feature_dict)
		
		return feature_dict_list
	
	
	
	def append_parts_of_speech_list(self, db, navigable_parent, pos_list=[], verbose=False):
		params_dict = db.execute(self.select_is_from_navigableparents_sql_str, (navigable_parent,)).fetchone()
		if params_dict['is_task_scope']:
			pos_list.append('H-TS')
		elif params_dict['is_minimum_qualification']:
			pos_list.append('H-RQ')
		elif params_dict['is_preferred_qualification']:
			pos_list.append('H-PQ')
		elif params_dict['is_legal_notification']:
			pos_list.append('H-LN')
		elif params_dict['is_job_title']:
			pos_list.append('H-JT')
		elif params_dict['is_office_location']:
			pos_list.append('H-OL')
		elif params_dict['is_job_duration']:
			pos_list.append('H-JD')
		elif params_dict['is_supplemental_pay']:
			pos_list.append('H-SP')
		elif params_dict['is_educational_requirement']:
			pos_list.append('H-ER')
		elif params_dict['is_interview_procedure']:
			pos_list.append('H-IP')
		elif params_dict['is_corporate_scope']:
			pos_list.append('H-CS')
		elif params_dict['is_posting_date']:
			pos_list.append('H-PD')
		elif params_dict['is_other']:
			pos_list.append('H-O')
		else:
			pos_list.append('H')
		
		return pos_list
	
	
	
	def get_execution_results(self, cursor, sql_str, verbose=False):
		if verbose:
			print(sql_str)
		cursor.execute(sql_str)
		try:
			row_objs_list = cursor.fetchall()
			row_tuples_list = [tuple(row_obj) for row_obj in row_objs_list]
		except:
			row_tuples_list = []
		cursor.commit()
		
		return row_tuples_list



	def create_header_tag_sequence_table_dataframe(self, save_as_csv=False, verbose=False):
		HEADER_PATTERN_DICT = s.load_object('HEADER_PATTERN_DICT')
		rows_list = []
		for file_name, feature_dict_list in HEADER_PATTERN_DICT.items():
			item_sequence = [feature_dict['initial_tag'] for feature_dict in feature_dict_list]
			for i, header_tag in enumerate(item_sequence):
				row_dict = {}
				row_dict['file_name'] = file_name
				row_dict['header_tag'] = header_tag
				row_dict['sequence_order'] = i
				rows_list.append(row_dict)
		header_tag_sequence_table_df = pd.DataFrame(rows_list)
		header_tag_sequence_table_df.index.name = 'header_tag_sequence_id'
		if save_as_csv:
			s.save_dataframes(include_index=True, verbose=verbose, header_tag_sequence_table_df=header_tag_sequence_table_df)
		
		return header_tag_sequence_table_df



	def create_header_tag_sequence_table(self, cursor, verbose=False):
		
		# Create the navigable html strings dataset
		header_tag_sequence_table_df = self.create_header_tag_sequence_table_dataframe(verbose=verbose)
		
		# Insert Dataframe into SQL Server:
		for row_index, row_series in header_tag_sequence_table_df.iterrows():
			if verbose:
				print(self.insert_columns_sql_str.replace('?', '"{}"').format(row_index, row_series.file_name,
																			  row_series.header_tag, row_series.sequence_order))
			try:
				cursor.execute(self.insert_columns_sql_str,
							   (row_index, row_series.file_name, row_series.header_tag, row_series.sequence_order))
			except Exception as e:
				print(str(e).strip())
				print(self.insert_columns_sql_str.replace('?', '"{}"').format(row_index, row_series.file_name,
																			  row_series.header_tag, row_series.sequence_order))
				break
		cursor.commit()



	def get_filenames_by_starting_sequence(self, cursor, sequence_list=[], verbose=False):
	
		# https://stackoverflow.com/questions/5160742/how-to-store-and-search-for-a-sequence-in-a-rdbms
		filenames_list = []
		if len(sequence_list):
			if verbose:
				print(self.create_query_table_sql_str)
			cursor.execute(self.create_query_table_sql_str)
			try:
				row_objs_list = cursor.fetchall()
				row_tuples_list = [tuple(row_obj) for row_obj in row_objs_list]
			except:
				row_tuples_list = []
			if verbose:
				print(row_tuples_list)
			
			# Insert sequence list into SQL Server:
			for sequence_order, header_tag in enumerate(sequence_list):
				if verbose:
					print(self.insert_query_rows_sql_str.replace('?', '"{}"').format(header_tag, sequence_order))
				try:
					cursor.execute(self.insert_query_rows_sql_str, header_tag, sequence_order)
				except Exception as e:
					print(str(e).strip())
					print(self.insert_query_rows_sql_str.replace('?', '"{}"').format(header_tag, sequence_order))
					break
				try:
					row_objs_list = cursor.fetchall()
				except:
					row_objs_list = []
			if verbose:
				print(self.select_query_sql_str)
			cursor.execute(self.select_query_sql_str)
			try:
				row_objs_list = cursor.fetchall()
				row_tuples_list = [tuple(row_obj) for row_obj in row_objs_list]
			except:
				row_tuples_list = []
			if verbose:
				print(row_tuples_list)
			cursor.commit()
			filenames_list = [filename_tuple[0] for filename_tuple in row_tuples_list]
		
		return filenames_list



	def get_filenames_by_sequence(self, cursor, sequence_list=[], verbose=False):
		all_filenames_list = []
		if len(sequence_list):
			start_num = 0
			header_tag_sequence_table_df = self.create_header_tag_sequence_table_dataframe()
			max_num = header_tag_sequence_table_df.sequence_order.max() - len(sequence_list) + 1
			while start_num < max_num:
				
				# Recreate temp table
				if verbose:
					print(self.create_query_table_sql_str)
				cursor.execute(self.create_query_table_sql_str)
				try:
					row_objs_list = cursor.fetchall()
					row_tuples_list = [tuple(row_obj) for row_obj in row_objs_list]
				except:
					row_tuples_list = []
				if verbose:
					print(row_tuples_list)
				
				# Insert sequence list into temp table
				for sequence_order, header_tag in enumerate(sequence_list):
					if verbose:
						print(self.insert_query_rows_sql_str.replace('?', '"{}"').format(header_tag, start_num + sequence_order))
					try:
						cursor.execute(self.insert_query_rows_sql_str, header_tag, start_num + sequence_order)
					except Exception as e:
						print(str(e).strip())
						print(self.insert_query_rows_sql_str.replace('?', '"{}"').format(header_tag, start_num + sequence_order))
						break
					try:
						row_objs_list = cursor.fetchall()
						row_tuples_list = [tuple(row_obj) for row_obj in row_objs_list]
					except:
						row_tuples_list = []
				
				# Find sequence list by file name
				if verbose:
					print(self.select_query_sql_str)
				cursor.execute(self.select_query_sql_str)
				try:
					row_objs_list = cursor.fetchall()
					row_tuples_list = [tuple(row_obj) for row_obj in row_objs_list]
				except:
					row_tuples_list = []
				if verbose:
					print(row_tuples_list)
				filenames_list = [filename_tuple[0] for filename_tuple in row_tuples_list]
				
				# Add these file names to the list
				all_filenames_list.extend(filenames_list)
				
				start_num += 1
			cursor.commit()
			
		return list(set(all_filenames_list))