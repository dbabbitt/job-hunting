
#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
import pyodbc
import random
import sqlite3
import re
try:
	import html_analysis
except:
	import flaskr.html_analysis



class SqlUtilities(object):
	"""SQL class."""

	def __init__(self, s=None, ha=None):
		if s is None:
			try:
				import storage
			except:
				import flaskr.storage
			self.s = storage.Storage()
		else:
			self.s = s
		if ha is None:
			self.ha = html_analysis.HeaderAnalysis()
		else:
			self.ha = ha
		self.wc_rgx = re.compile(r'([%_\[^\-\\])')

		# File Names Table SQL
		# The email date is in the form of ISO8601 strings ("YYYY-MM-DD HH:MM:SS.SSS")
		self.create_filenames_table_sql_str = """
			CREATE TABLE FileNames(
				file_name_id INTEGER PRIMARY KEY,
				file_name CHAR(255) NOT NULL,
				percent_fit REAL NULL,
				is_opportunity_application_emailed BIT NULL,
				opportunity_application_email_date TEXT NULL,
				is_remote_delivery BIT NULL,
				manager_notes TEXT NULL
			);"""
		self.select_file_names_sql_str = """
			SELECT RTRIM(fn.[file_name]) AS file_name
			FROM [Jobhunting].[dbo].[FileNames] fn"""
		self.select_file_name_where_is_qualification_sql_str = """
			SELECT RTRIM(fn.[file_name]) AS file_name
			FROM
				[Jobhunting].[dbo].[FileNames] fn INNER JOIN
				[Jobhunting].[dbo].[NavigableParentSequence] nps ON
				fn.[file_name_id] = nps.[file_name_id] INNER JOIN
				[Jobhunting].[dbo].[NavigableParents] np ON
				nps.[navigable_parent_id] = np.[navigable_parent_id]
			WHERE
				np.[is_minimum_qualification] = 1 AND
				np.[is_header] = 1"""


		# Header Tags Table SQL
		self.create_headertags_table_sql_str = """
			CREATE TABLE HeaderTags(
				header_tag_id INTEGER PRIMARY KEY,
				header_tag CHAR(32) NOT NULL,
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
		self.insert_into_headertags_sql_str = """
			INSERT INTO HeaderTags (
				header_tag_id,
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
			VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""


		# Navigable Parents SQL strings
		self.create_navigableparents_table_sql_str = """
			CREATE TABLE NavigableParents (
				navigable_parent_id INTEGER PRIMARY KEY,
				navigable_parent NVARCHAR(MAX) NOT NULL,
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
		self.select_navigableparentid_sql_str = r"""
			SELECT navigable_parent_id FROM NavigableParents WHERE navigable_parent LIKE ? ESCAPE '\';"""
		self.select_navigable_parent_by_file_name_sql_str = """
			SELECT t.[navigable_parent]
			FROM
				[Jobhunting].[dbo].[NavigableParentSequence] s INNER JOIN
				[Jobhunting].[dbo].[NavigableParents] t ON
				s.[navigable_parent_id] = t.[navigable_parent_id] INNER JOIN
				[Jobhunting].[dbo].[FileNames] f ON
				s.[file_name_id] = f.[file_name_id]
			WHERE RTRIM(f.[file_name]) = ?
			ORDER BY s.[sequence_order] ASC;"""
		self.set_is_corporate_scope1_sql_str = r"""
			UPDATE NavigableParents
			SET is_header = 1, is_corporate_scope = 1
			WHERE (navigable_parent LIKE ? ESCAPE '\')"""
		self.set_is_header1_sql_str = r"""
			UPDATE NavigableParents
			SET is_header = 1
			WHERE (navigable_parent LIKE ? ESCAPE '\')"""
		self.set_is_header0_sql_str = r"""
			UPDATE NavigableParents
			SET is_header = 0
			WHERE (navigable_parent LIKE ? ESCAPE '\')"""
		self.set_is_qualification1_sql_str = r"""
			UPDATE NavigableParents
			SET is_qualification = 1
			WHERE (navigable_parent LIKE ? ESCAPE '\')"""
		self.set_is_qualification0_sql_str = r"""
			UPDATE NavigableParents
			SET is_qualification = 0
			WHERE (navigable_parent LIKE ? ESCAPE '\')"""
		self.set_is_task_scope1_sql_str = r"""
			UPDATE NavigableParents
			SET is_header = 1, is_task_scope = 1
			WHERE (navigable_parent LIKE ? ESCAPE '\')"""
		self.set_is_office_location1_sql_str = r"""
			UPDATE NavigableParents
			SET is_header = 1, is_office_location = 1
			WHERE (navigable_parent LIKE ? ESCAPE '\')"""
		self.set_is_minimum_qualification1_sql_str = r"""
			UPDATE NavigableParents
			SET is_header = 1, is_minimum_qualification = 1, is_qualification = 1
			WHERE (navigable_parent LIKE ? ESCAPE '\')"""
		self.set_is_supplemental_pay1_sql_str = r"""
			UPDATE NavigableParents
			SET is_header = 1, is_supplemental_pay = 1
			WHERE (navigable_parent LIKE ? ESCAPE '\')"""
		self.set_nonheader_is_supplemental_pay1_sql_str = r"""
			UPDATE NavigableParents
			SET is_header = 0, is_supplemental_pay = 1
			WHERE (navigable_parent LIKE ? ESCAPE '\')"""
		self.set_is_preferred_qualification1_sql_str = r"""
			UPDATE NavigableParents
			SET is_header = 1, is_preferred_qualification = 1
			WHERE (navigable_parent LIKE ? ESCAPE '\')"""
		self.set_is_legal_notification1_sql_str = r"""
			UPDATE NavigableParents
			SET is_header = 1, is_legal_notification = 1
			WHERE (navigable_parent LIKE ? ESCAPE '\')"""
		self.set_is_other1_sql_str = r"""
			UPDATE NavigableParents
			SET is_header = 1, is_other = 1
			WHERE (navigable_parent LIKE ? ESCAPE '\')"""
		self.set_is_educational_requirement1_sql_str = r"""
			UPDATE NavigableParents
			SET is_header = 1, is_educational_requirement = 1
			WHERE (navigable_parent LIKE ? ESCAPE '\')"""
		self.set_is_interview_procedure1_sql_str = r"""
			UPDATE NavigableParents
			SET is_header = 1, is_interview_procedure = 1
			WHERE (navigable_parent LIKE ? ESCAPE '\')"""
		self.set_is_posting_date1_sql_str = r"""
			UPDATE NavigableParents
			SET is_header = 1, is_posting_date = 1
			WHERE (navigable_parent LIKE ? ESCAPE '\')"""
		self.set_is_job_duration1_sql_str = r"""
			UPDATE NavigableParents
			SET is_header = 1, is_job_duration = 1
			WHERE (navigable_parent LIKE ? ESCAPE '\')"""
		self.set_is_job_title1_sql_str = r"""
			UPDATE NavigableParents
			SET is_header = 1, is_job_title = 1
			WHERE (navigable_parent LIKE ? ESCAPE '\')"""
		self.select_is_from_navigableparents_sql_str = r"""
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
			WHERE navigable_parent LIKE ? ESCAPE '\'"""
		self.select_navigable_parent_id_where_navigable_parent_sql_str = r"""
			SELECT
				navigable_parent_id,
				is_minimum_qualification
			FROM NavigableParents
			WHERE navigable_parent LIKE ? ESCAPE '\'"""
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


		# Header Tags Sequence SQL strings
		self.create_headertagsequence_table_sql_str = """
			CREATE TABLE HeaderTagSequence(
				header_tag_sequence_id INTEGER PRIMARY KEY,
				file_name_id INTEGER NOT NULL,
				header_tag_id INTEGER NOT NULL,
				sequence_order INTEGER NOT NULL
			);"""
		self.select_query_sql_str = """
			SELECT RTRIM(s.[file_name]) AS file_name
			FROM HeaderTagSequence s
				INNER JOIN #query q
				ON
					q.header_tag = s.header_tag AND
					q.sequence_order = s.sequence_order
			GROUP BY s.file_name
			HAVING Count(*) = (SELECT Count(*) FROM #query)"""
		
		# This assumes this sql server isn't taking more than one request at a time
		self.insert_header_tag_sequence_str = """
			SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
				BEGIN TRAN

					IF NOT EXISTS (
						SELECT *
						FROM dbo.HeaderTagSequence WITH (UPDLOCK)
						WHERE
							file_name_id = ? AND
							header_tag_id = ? AND
							sequence_order = ?)
						INSERT INTO dbo.HeaderTagSequence (
							header_tag_sequence_id,
							file_name_id,
							header_tag_id,
							sequence_order
						)
						VALUES (
							(SELECT ISNULL(MAX(header_tag_sequence_id) + 1, 0) FROM dbo.HeaderTagSequence),
							?,
							?,
							?
						);

				COMMIT"""


		# Navigable Parents Sequence SQL strings
		self.create_navigableparentsequence_table_sql_str = """
			CREATE TABLE NavigableParentSequence(
				navigable_parent_sequence_id INTEGER PRIMARY KEY,
				file_name_id INTEGER NOT NULL,
				navigable_parent_id INTEGER NOT NULL,
				sequence_order INTEGER NOT NULL,
				mrs_id INTEGER NOT NULL
			);"""
		self.insert_navigableparentsequence_table_sql_str = """
			INSERT INTO NavigableParentSequence (
				navigable_parent_sequence_id,
				file_name_id,
				navigable_parent_id,
				sequence_order,
				mrs_id
			)
			VALUES (?, ?, ?, ?, ?);"""
		self.select_filename_isheader_sql_str = """
			SELECT
				RTRIM(f.[file_name]) AS file_name,
				t.[is_header]
			FROM
				[Jobhunting].[dbo].[NavigableParentSequence] s INNER JOIN
				[Jobhunting].[dbo].[NavigableParents] t ON
				s.[navigable_parent_id] = t.[navigable_parent_id] INNER JOIN
				[Jobhunting].[dbo].[FileNames] f ON
				s.[file_name_id] = f.[file_name_id];"""


		# Parts of Speech SQL strings
		self.create_table_partsofspeech_sql_str = """
			CREATE TABLE PartsOfSpeech(
				pos_id INTEGER PRIMARY KEY,
				pos_symbol VARCHAR(4) NOT NULL,
				pos_explanation TEXT NOT NULL,
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
				is_other BIT NULL
			);"""
		self.insert_into_partsofspeech_sql_str = """
			INSERT INTO PartsOfSpeech (
				pos_id,
				pos_symbol,
				pos_explanation,
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
				is_other,
				is_qualification
			) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
			;"""


		# Minimum Requirements Section SQL strings
		self.create_table_minimumrequirementssection_sql_str = """
			CREATE TABLE MinimumRequirementsSection(
				mrs_id INTEGER PRIMARY KEY,
				mrs_symbol VARCHAR(4) NOT NULL,
				mrs_explanation TEXT NOT NULL
			);"""
		self.insert_into_minimumrequirementssection_sql_str = """
			INSERT INTO MinimumRequirementsSection (
				mrs_id,
				mrs_symbol,
				mrs_explanation
			) VALUES (?, ?, ?)
			;"""
		
		# Various SQL strings
		self.create_query_table_sql_str = """
			DROP TABLE IF EXISTS dbo.#query;
			CREATE TABLE #query(
				header_tag CHAR (32) NOT NULL,
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
		self.SAVES_HTML_FOLDER = os.path.join(self.s.saves_folder, 'html')



	def create_filenames_table(self, db, verbose=False):
		db.execute('DROP TABLE IF EXISTS FileNames;')
		db.execute(self.create_filenames_table_sql_str)
		db.commit()


	def populate_filenames_table(self, db, verbose=False):
		files_list = sorted([fn for fn in os.listdir(self.SAVES_HTML_FOLDER) if fn.endswith('html')])
		for i, file_name in enumerate(files_list):
			db.execute('INSERT INTO FileNames (file_name_id, file_name) VALUES (?, ?)', (i, file_name.strip(),))
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
		for i, child_tag in enumerate(child_tags_list):
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
			params_tuple = (i, child_tag, is_in_document_structure_elements_set, is_in_document_head_elements_set,
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
	
	
	def get_files_list(self, db, verbose=False):
		cursor_obj = db.execute(self.select_file_names_sql_str)
		columns_list = [c[0] for c in cursor_obj.description]
		row_objs_list = [dict(zip(columns_list, row)) for row in cursor_obj.fetchall()]
		files_list = [row_obj['file_name'].strip() for row_obj in row_objs_list]
		
		return files_list
	
	
	def populate_navigableparents_table(self, db, verbose=False):
		files_list = self.get_files_list(db, verbose=verbose)
		navigable_parent_set = set()
		for file_name in files_list:
			child_strs_list = self.ha.get_child_strs_from_file(file_name.strip())
			for child_str in child_strs_list:
				navigable_parent_set.add(child_str)
		child_strs_list = sorted(navigable_parent_set)
		child_tags_list = self.ha.get_child_tags_list(child_strs_list)
		for i, (child_str, child_tag) in enumerate(zip(child_strs_list, child_tags_list)):
			try:
				cursor_obj = db.execute("SELECT header_tag_id FROM HeaderTags WHERE header_tag = ?",
										(child_tag,))
			except Exception as e:
				print(str(e).strip())
				print("SELECT header_tag_id FROM HeaderTags WHERE header_tag = {}".format(child_tag))
				break
			columns_list = [c[0] for c in cursor_obj.description]
			params_dict = dict(zip(columns_list, list(cursor_obj.fetchone())))
			header_tag_id = params_dict['header_tag_id']
			db.execute('INSERT INTO NavigableParents (navigable_parent_id, navigable_parent, header_tag_id) VALUES (?, ?, ?)',
					   (i, child_str, header_tag_id))

		# Set the Corporate Scope is_header
		corp_scope_headers_list = self.s.load_object('corp_scope_headers_list')
		for navigable_parent in corp_scope_headers_list:
			db.execute(self.set_is_corporate_scope1_sql_str, (navigable_parent,))

		# Set the basic tags is_header
		NAVIGABLE_PARENT_IS_HEADER_DICT = self.s.load_object('NAVIGABLE_PARENT_IS_HEADER_DICT')
		for navigable_parent, is_header in NAVIGABLE_PARENT_IS_HEADER_DICT.items():
			if is_header:
				db.execute(self.set_is_header1_sql_str, (navigable_parent,))
			else:
				db.execute(self.set_is_header0_sql_str, (navigable_parent,))

		# Set the basic tags is_qual
		NAVIGABLE_PARENT_IS_QUAL_DICT = self.s.load_object('NAVIGABLE_PARENT_IS_QUAL_DICT')
		for navigable_parent, is_qualification in NAVIGABLE_PARENT_IS_QUAL_DICT.items():
			if is_qualification:
				db.execute(self.set_is_qualification1_sql_str, (navigable_parent,))
			else:
				db.execute(self.set_is_qualification0_sql_str, (navigable_parent,))

		# Set the Task Scope is_header
		task_scope_headers_list = self.s.load_object('task_scope_headers_list')
		for navigable_parent in task_scope_headers_list:
			db.execute(self.set_is_task_scope1_sql_str, (navigable_parent,))

		# Set the Office Location is_header
		office_loc_headers_list = self.s.load_object('office_loc_headers_list')
		for navigable_parent in office_loc_headers_list:
			db.execute(self.set_is_office_location1_sql_str, (navigable_parent,))

		# Set the Minimum Quals is_header
		req_quals_headers_list = self.s.load_object('req_quals_headers_list')
		for navigable_parent in req_quals_headers_list:
			db.execute(self.set_is_minimum_qualification1_sql_str, (navigable_parent,))
		if s.pickle_exists('O_RQ_DICT'):
			req_quals_nonheaders_dict = self.s.load_object('O_RQ_DICT')
			is_nonheader_minimum_qualification_sql_str = r"""
				UPDATE NavigableParents
				SET is_header = 0, is_minimum_qualification = 1, is_qualification = 1
				WHERE (navigable_parent LIKE ? ESCAPE '\')"""
			for navigable_parent, is_nonheader_minimum_qualification in req_quals_nonheaders_dict.items():
				if is_nonheader_minimum_qualification:
					db.execute(is_nonheader_minimum_qualification_sql_str, (navigable_parent,))
		if s.pickle_exists('H_RQ_DICT'):
			req_quals_headers_dict = self.s.load_object('H_RQ_DICT')
			is_header_minimum_qualification_sql_str = r"""
				UPDATE NavigableParents
				SET is_header = 1, is_minimum_qualification = 1, is_qualification = 1
				WHERE (navigable_parent LIKE ? ESCAPE '\')"""
			for navigable_parent, is_header_minimum_qualification in req_quals_headers_dict.items():
				if is_header_minimum_qualification:
					db.execute(is_header_minimum_qualification_sql_str, (navigable_parent,))

		# Set the Supplemental Pay is_header
		supp_pay_headers_list = self.s.load_object('supp_pay_headers_list')
		for navigable_parent in supp_pay_headers_list:
			db.execute(self.set_is_supplemental_pay1_sql_str, (navigable_parent,))

		# Set the Supplemental Pay non-header
		supp_pay_nonheaders_list = self.s.load_object('supp_pay_nonheaders_list')
		for navigable_parent in supp_pay_nonheaders_list:
			db.execute(self.set_nonheader_is_supplemental_pay1_sql_str, (navigable_parent,))

		# Set the Preferred Quals is_header
		preff_quals_headers_list = self.s.load_object('preff_quals_headers_list')
		for navigable_parent in preff_quals_headers_list:
			db.execute(self.set_is_preferred_qualification1_sql_str, (navigable_parent,))

		# Set the Legal Notifications is_header
		legal_notifs_headers_list = self.s.load_object('legal_notifs_headers_list')
		for navigable_parent in legal_notifs_headers_list:
			db.execute(self.set_is_legal_notification1_sql_str, (navigable_parent,))

		# Set the Other is_header
		other_headers_list = self.s.load_object('other_headers_list')
		for navigable_parent in other_headers_list:
			db.execute(self.set_is_other1_sql_str, (navigable_parent,))

		# Set the Education Requirements is_header
		educ_reqs_headers_list = self.s.load_object('educ_reqs_headers_list')
		for navigable_parent in educ_reqs_headers_list:
			db.execute(self.set_is_educational_requirement1_sql_str, (navigable_parent,))

		# Set the Interview Process is_header
		interv_proc_headers_list = self.s.load_object('interv_proc_headers_list')
		for navigable_parent in interv_proc_headers_list:
			db.execute(self.set_is_interview_procedure1_sql_str, (navigable_parent,))

		# Set the Posting Date is_header
		post_date_headers_list = self.s.load_object('post_date_headers_list')
		for navigable_parent in post_date_headers_list:
			db.execute(self.set_is_posting_date1_sql_str, (navigable_parent,))

		# Set the Job Duration is_header
		job_duration_headers_list = self.s.load_object('job_duration_headers_list')
		for navigable_parent in job_duration_headers_list:
			db.execute(self.set_is_job_duration1_sql_str, (navigable_parent,))

		# Set the Job Title is_header
		job_title_headers_list = self.s.load_object('job_title_headers_list')
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
		files_list = self.get_files_list(db, verbose=verbose)
		for file_name in files_list:
			file_name = file_name.strip()
			try:
				cursor_obj = db.execute('SELECT file_name_id FROM FileNames WHERE RTRIM(file_name) = ?', (file_name,))
				columns_list = [c[0] for c in cursor_obj.description]
				params_dict = dict(zip(columns_list, list(cursor_obj.fetchone())))
				file_name_id = params_dict['file_name_id']
			except Exception as e:
				print(str(e).strip())
				print(f'SELECT file_name_id FROM FileNames WHERE RTRIM(file_name) = "{file_name}"')
				break
			child_strs_list = self.ha.get_child_strs_from_file(file_name)
			child_tags_list = self.ha.get_child_tags_list(child_strs_list)
			for sequence_order, header_tag in enumerate(child_tags_list):
				cursor_obj = db.execute("SELECT header_tag_id FROM HeaderTags WHERE header_tag = ?",
										(header_tag,))
				columns_list = [c[0] for c in cursor_obj.description]
				params_dict = dict(zip(columns_list, list(cursor_obj.fetchone())))
				header_tag_id = params_dict['header_tag_id']
				if verbose:
					print(self.insert_header_tag_sequence_str.replace('?', '"{}"').format(file_name_id, header_tag_id, sequence_order,
																						  file_name_id, header_tag_id, sequence_order))
				try:
					db.execute(self.insert_header_tag_sequence_str,
							   (file_name_id, header_tag_id, sequence_order, file_name_id, header_tag_id, sequence_order))
				except Exception as e:
					print(str(e).strip())
					print(self.insert_header_tag_sequence_str.replace('?', '"{}"').format(file_name_id, header_tag_id, sequence_order,
																						  file_name_id, header_tag_id, sequence_order))
					break
		db.commit()
	
	
	def populate_header_tag_sequence_table(self, cursor, verbose=False):

		# Create the navigable html strings dataset
		header_tag_sequence_table_df = self.create_header_tag_sequence_table_dataframe(verbose=verbose)

		# Insert Dataframe into SQL Server:
		for row_index, row_series in header_tag_sequence_table_df.iterrows():
			if verbose:
				print(self.insert_header_tag_sequence_str.replace('?', '"{}"').format(row_series.file_name.strip(), row_series.header_tag,
																					  row_series.sequence_order, row_series.file_name.strip(),
																					  row_series.header_tag, row_series.sequence_order))
			try:
				cursor.execute(self.insert_header_tag_sequence_str,
							   (row_series.file_name.strip(), row_series.header_tag, row_series.sequence_order, row_series.file_name.strip(),
							    row_series.header_tag, row_series.sequence_order))
			except Exception as e:
				print(str(e).strip())
				print(self.insert_header_tag_sequence_str.replace('?', '"{}"').format(row_series.file_name.strip(), row_series.header_tag,
																					  row_series.sequence_order, row_series.file_name.strip(),
																					  row_series.header_tag, row_series.sequence_order))
				break
		cursor.commit()



	def create_navigableparentsequence_table(self, db, verbose=False):
		db.execute('DROP TABLE IF EXISTS NavigableParentSequence;')
		db.execute(self.create_navigableparentsequence_table_sql_str)
		db.commit()



	def populate_navigableparentsequence_table(self, db, verbose=False):
		files_list = self.get_files_list(db, verbose=verbose)
		counter = 0
		for file_name in files_list:
			file_name = file_name.strip()
			cursor_obj = db.execute('SELECT file_name_id FROM FileNames WHERE RTRIM(file_name) = ?', (file_name,))
			columns_list = [c[0] for c in cursor_obj.description]
			params_dict = dict(zip(columns_list, list(cursor_obj.fetchone())))
			file_name_id = params_dict['file_name_id']
			child_strs_list = self.ha.get_child_strs_from_file(file_name)
			for sequence_order, navigable_parent in enumerate(child_strs_list):
				try:
					cursor_obj = db.execute(self.select_navigableparentid_sql_str, (self.wc_rgx.sub(r'\\\g<1>', navigable_parent),))
					columns_list = [c[0] for c in cursor_obj.description]
					params_dict = dict(zip(columns_list, list(cursor_obj.fetchone())))
					navigable_parent_id = params_dict['navigable_parent_id']
				except Exception as e:
					print(str(e).strip())
					print(self.select_navigableparentid_sql_str.replace('?', '{}').format(self.wc_rgx.sub(r'\\\g<1>', navigable_parent)))
					break
				try:
					db.execute(self.insert_navigableparentsequence_table_sql_str,
							   (counter, file_name_id, navigable_parent_id, sequence_order, 0))
					counter += 1
				except Exception as e:
					print(str(e).strip())
					print(self.insert_navigableparentsequence_table_sql_str.replace('?',
																					'{}').format(counter, file_name_id, navigable_parent_id,
																								 sequence_order, 0))
					break
		db.commit()
	
	
	def create_partsofspeech_table(self, db, verbose=False):
		db.execute('DROP TABLE IF EXISTS PartsOfSpeech;')
		db.execute(self.create_table_partsofspeech_sql_str)
		db.commit()
	
	
	def populate_partsofspeech_table(self, db, verbose=False):
		pos_explanation_dict = self.s.load_object('pos_explanation_dict')
		count = 0
		for pos_symbol, pos_explanation in pos_explanation_dict.items():
			if pos_symbol.startswith('H-'):
				db.execute('INSERT INTO PartsOfSpeech (pos_id, pos_symbol, pos_explanation) VALUES (?, ?, ?)',
						   (count, pos_symbol, pos_explanation))
				count += 1
				db.execute('INSERT INTO PartsOfSpeech (pos_id, pos_symbol, pos_explanation) VALUES (?, ?, ?)',
						   (count, pos_symbol.replace('H-', 'O-'), pos_explanation.replace(' Header', ' Non-header')))
				count += 1
		db.commit()
		sql_str = """
			SELECT
				pos.[pos_symbol],
				pos.[pos_explanation]
			FROM [Jobhunting].[dbo].[PartsOfSpeech] pos;"""
		pos_df = pd.DataFrame(self.get_execution_results(db, sql_str, verbose=verbose))
		pos_df['is_header'] = pos_df.pos_symbol.map(lambda x: 'H-' in x)
		pos_df['is_task_scope'] = pos_df.pos_symbol.map(lambda x: '-TS' in x)
		pos_df['is_minimum_qualification'] = pos_df.pos_symbol.map(lambda x: '-RQ' in x)
		pos_df['is_preferred_qualification'] = pos_df.pos_symbol.map(lambda x: '-PQ' in x)
		pos_df['is_legal_notification'] = pos_df.pos_symbol.map(lambda x: '-LN' in x)
		pos_df['is_job_title'] = pos_df.pos_symbol.map(lambda x: '-JT' in x)
		pos_df['is_office_location'] = pos_df.pos_symbol.map(lambda x: '-OL' in x)
		pos_df['is_job_duration'] = pos_df.pos_symbol.map(lambda x: '-JD' in x)
		pos_df['is_supplemental_pay'] = pos_df.pos_symbol.map(lambda x: '-SP' in x)
		pos_df['is_educational_requirement'] = pos_df.pos_symbol.map(lambda x: '-ER' in x)
		pos_df['is_interview_procedure'] = pos_df.pos_symbol.map(lambda x: '-IP' in x)
		pos_df['is_corporate_scope'] = pos_df.pos_symbol.map(lambda x: '-CS' in x)
		pos_df['is_posting_date'] = pos_df.pos_symbol.map(lambda x: '-PD' in x)
		pos_df['is_other'] = pos_df.pos_symbol.map(lambda x: x in ['H-O', 'O-O'])
		for row_index, row_series in pos_df.iterrows():
			sql_str = """
				UPDATE PartsOfSpeech
				SET
					"""
			set_list = [f'{cn} = {int(cv)}' for cn, cv in row_series.iteritems() if cn not in ['pos_symbol', 'pos_explanation']]
			sql_str += """,
					""".join(set_list)
			sql_str += f"""
				WHERE pos_symbol = '{row_series.pos_symbol}';"""
			if verbose:
				print(sql_str)
			db.execute(sql_str)
		db.commit()
	
	
	def create_minimumrequirementssection_table(self, db, verbose=False):
		db.execute('DROP TABLE IF EXISTS MinimumRequirementsSection;')
		db.execute(self.create_table_minimumrequirementssection_sql_str)
		db.commit()
	
	
	def populate_minimumrequirementssection_table(self, db, verbose=False):
		mrs_explanation_dict = {'N': 'Not a part of the Minimum Requirements Section', 'B': 'Beginning of the Minimum Requirements Section',
								'M': 'Middle of the Minimum Requirements Section', 'E': 'End of the Minimum Requirements Section'}
		for count, (mrs_symbol, mrs_explanation) in enumerate(mrs_explanation_dict.items()):
			db.execute(self.insert_into_minimumrequirementssection_sql_str, (count, mrs_symbol, mrs_explanation))
		db.commit()
	
	
	def get_is_header_list(self, db, child_strs_list, verbose=False):
		is_header_list = []
		for navigable_parent in child_strs_list:
			cursor_obj = db.execute(r"SELECT is_header FROM NavigableParents WHERE navigable_parent LIKE ? ESCAPE '\'",
									(self.wc_rgx.sub(r'\\\g<1>', navigable_parent),))
			columns_list = [c[0] for c in cursor_obj.description]
			params_dict = dict(zip(columns_list, list(cursor_obj.fetchone())))
			is_header = params_dict['is_header']
			is_header_list.append(is_header)

		return is_header_list



	def get_child_strs_from_file(self, db, file_name, verbose=False):
		cursor_obj = db.execute(self.select_navigable_parent_by_file_name_sql_str, (file_name.strip(),))
		columns_list = [c[0] for c in cursor_obj.description]
		row_objs_list = [dict(zip(columns_list, row)) for row in cursor_obj.fetchall()]
		child_strs_list = [row_obj['navigable_parent'] for row_obj in row_objs_list]

		return child_strs_list



	def get_child_tags_list(self, db, child_strs_list, verbose=False):
		child_tags_list = []
		for navigable_parent in child_strs_list:
			cursor_obj = db.execute(r"SELECT header_tag_id FROM NavigableParents WHERE navigable_parent LIKE ? ESCAPE '\'",
									(self.wc_rgx.sub(r'\\\g<1>', navigable_parent),))
			columns_list = [c[0] for c in cursor_obj.description]
			params_dict = dict(zip(columns_list, list(cursor_obj.fetchone())))
			header_tag_id = params_dict['header_tag_id']
			cursor_obj = db.execute('SELECT header_tag FROM HeaderTags WHERE header_tag_id = ?',
									(header_tag_id,))
			columns_list = [c[0] for c in cursor_obj.description]
			params_dict = dict(zip(columns_list, list(cursor_obj.fetchone())))
			header_tag = params_dict['header_tag'].strip()
			child_tags_list.append(header_tag)

		return child_tags_list



	def get_feature_dict_list(self, db, child_tags_list, child_strs_list, verbose=False):
		feature_dict_list = []
		import numpy as np
		for tag, child_str in zip(child_tags_list, child_strs_list):
			feature_dict = {}
			feature_dict['initial_tag'] = tag
			if verbose:
				print(self.select_is_from_navigableparents_sql_str.replace('?', "'{}'").format(self.wc_rgx.sub(r'\\\g<1>', child_str)))
			cursor_obj = db.execute(self.select_is_from_navigableparents_sql_str, (self.wc_rgx.sub(r'\\\g<1>', child_str),))
			columns_list = [c[0] for c in cursor_obj.description]
			params_dict = dict(zip(columns_list, list(cursor_obj.fetchone())))
			if params_dict is not None:
				if params_dict['is_header'] is not None:
					feature_dict['is_header'] = params_dict['is_header']
				if params_dict['is_task_scope'] is not None:
					feature_dict['is_task_scope'] = params_dict['is_task_scope']
				if params_dict['is_minimum_qualification'] is not None:
					feature_dict['is_minimum_qualification'] = params_dict['is_minimum_qualification']
				if params_dict['is_preferred_qualification'] is not None:
					feature_dict['is_preferred_qualification'] = params_dict['is_preferred_qualification']
				if params_dict['is_legal_notification'] is not None:
					feature_dict['is_legal_notification'] = params_dict['is_legal_notification']
				if params_dict['is_job_title'] is not None:
					feature_dict['is_job_title'] = params_dict['is_job_title']
				if params_dict['is_office_location'] is not None:
					feature_dict['is_office_location'] = params_dict['is_office_location']
				if params_dict['is_job_duration'] is not None:
					feature_dict['is_job_duration'] = params_dict['is_job_duration']
				if params_dict['is_supplemental_pay'] is not None:
					feature_dict['is_supplemental_pay'] = params_dict['is_supplemental_pay']
				if params_dict['is_educational_requirement'] is not None:
					feature_dict['is_educational_requirement'] = params_dict['is_educational_requirement']
				if params_dict['is_interview_procedure'] is not None:
					feature_dict['is_interview_procedure'] = params_dict['is_interview_procedure']
				if params_dict['is_corporate_scope'] is not None:
					feature_dict['is_corporate_scope'] = params_dict['is_corporate_scope']
				if params_dict['is_posting_date'] is not None:
					feature_dict['is_posting_date'] = params_dict['is_posting_date']
				if params_dict['is_other'] is not None:
					feature_dict['is_other'] = params_dict['is_other']
			feature_dict['child_str'] = child_str
			feature_dict_list.append(feature_dict)

		return feature_dict_list



	def append_parts_of_speech_list(self, cursor, navigable_parent, pos_list=[], verbose=False):
		cursor_obj = cursor.execute(self.select_is_from_navigableparents_sql_str, (navigable_parent,))
		columns_list = [c[0] for c in cursor_obj.description]
		params_dict = dict(zip(columns_list, list(cursor_obj.fetchone())))
		if params_dict['is_header']:
			pos = 'H'
		else:
			pos = 'O'
		if params_dict['is_task_scope']:
			pos += '-TS'
		elif params_dict['is_minimum_qualification']:
			pos += '-RQ'
		elif params_dict['is_preferred_qualification']:
			pos += '-PQ'
		elif params_dict['is_legal_notification']:
			pos += '-LN'
		elif params_dict['is_job_title']:
			pos += '-JT'
		elif params_dict['is_office_location']:
			pos += '-OL'
		elif params_dict['is_job_duration']:
			pos += '-JD'
		elif params_dict['is_supplemental_pay']:
			pos += '-SP'
		elif params_dict['is_educational_requirement']:
			pos += '-ER'
		elif params_dict['is_interview_procedure']:
			pos += '-IP'
		elif params_dict['is_corporate_scope']:
			pos += '-CS'
		elif params_dict['is_posting_date']:
			pos += '-PD'
		elif params_dict['is_other']:
			pos += '-O'
		pos_list.append(pos)

		return pos_list



	def get_execution_results(self, cursor, sql_str, verbose=False):
		if verbose:
			print(sql_str)
		try:
			cursor_obj = cursor.execute(sql_str)
			columns_list = [c[0] for c in cursor_obj.description]
			row_objs_list = [dict(zip(columns_list, row)) for row in cursor_obj.fetchall()]
			cursor.commit()
		except Exception as e:
			print(str(e).strip())
			print(sql_str)
			row_objs_list = []

		return row_objs_list
	
	
	
	def build_child_strs_list_dictionary(self, cursor, verbose=False):
		self.CHILD_STRS_LIST_DICT = {}
		def f(df):
			mask_series = df.is_header.isnull()
			
			return df[mask_series].shape[0]
		isheaders_df = pd.DataFrame(self.get_execution_results(cursor, self.select_filename_isheader_sql_str, verbose=False))
		isheaders_series = isheaders_df.groupby('file_name').apply(f).sort_values()
		files_list = isheaders_series[isheaders_series==0].index.tolist()
		for file_name in files_list:
			file_name = file_name.strip()
			child_strs_list = self.get_child_strs_from_file(cursor, file_name)
			if file_name not in self.CHILD_STRS_LIST_DICT:
				self.CHILD_STRS_LIST_DICT[file_name] = child_strs_list
				self.s.store_objects(CHILD_STRS_LIST_DICT=self.CHILD_STRS_LIST_DICT, verbose=False)



	def create_header_pattern_dictionary(self, cursor, verbose=False):
		
		# Get the files in the child strings list
		sql_str = '''
			SELECT
				fn.[file_name_id],
				RTRIM(fn.[file_name]) AS file_name
			FROM [Jobhunting].[dbo].[FileNames] fn'''
		filenames_df = pd.DataFrame(self.get_execution_results(cursor, sql_str, verbose=verbose))
		CHILD_STRS_LIST_DICT = self.s.load_object('CHILD_STRS_LIST_DICT')
		mask_series = filenames_df.file_name.isin(list(CHILD_STRS_LIST_DICT.keys()))
		
		# Initialize and populate the header pattern dictionary
		HEADER_PATTERN_DICT = {}
		for row_index, row_series in filenames_df[mask_series].iterrows():
			file_name_id = row_series.file_name_id
			file_name = row_series.file_name.strip()
			
			# Get the child strings list for the file
			sql_str = '''
				SELECT np.[navigable_parent]
				FROM
					[Jobhunting].[dbo].[NavigableParentSequence] nps INNER JOIN
					[Jobhunting].[dbo].[NavigableParents] np ON
					nps.[navigable_parent_id] = np.[navigable_parent_id]
				WHERE nps.[file_name_id] = {}
				ORDER BY nps.[sequence_order] ASC'''.format(file_name_id)
			child_strs_list = pd.DataFrame(self.get_execution_results(cursor, sql_str, verbose=verbose)).navigable_parent.tolist()
			
			# Get the child tags list for the file
			sql_str = '''
				SELECT ht.[header_tag]
				FROM
					[Jobhunting].[dbo].[HeaderTagSequence] hts INNER JOIN
					[Jobhunting].[dbo].[HeaderTags] ht ON
					hts.[header_tag_id] = ht.[header_tag_id]
				WHERE hts.[file_name_id] = {}
				ORDER BY hts.[sequence_order] ASC'''.format(file_name_id)
			child_tags_list = [x.strip() for x in pd.DataFrame(self.get_execution_results(cursor, sql_str,
																						  verbose=verbose)).header_tag.tolist()]
			
			# Assume the is_header feature for each item in the sequence is not None
			item_sequence = self.get_feature_dict_list(cursor, child_tags_list, child_strs_list)
			
			HEADER_PATTERN_DICT[file_name] = item_sequence
			self.s.store_objects(HEADER_PATTERN_DICT=HEADER_PATTERN_DICT, verbose=verbose)
	
	
	def find_basic_quals_section(self, cursor, child_strs_list, hc=None, ea=None):
		if hc is None:
			hc = html_analysis.HeaderCategories()
		if ea is None:
			ea = html_analysis.ElementAnalysis()
		child_tags_list = self.get_child_tags_list(cursor, child_strs_list)
		is_header_list = self.get_is_header_list(cursor, child_strs_list)
		feature_dict_list = self.get_feature_dict_list(cursor, child_tags_list, child_strs_list)
		feature_tuple_list = [hc.get_feature_tuple(feature_dict) for feature_dict in feature_dict_list]
		
		crf_list = ea.CRF.predict_single(ea.sent2features(feature_tuple_list))
		pos_list = []
		for pos, feature_tuple, is_header in zip(crf_list, feature_tuple_list, is_header_list):
			navigable_parent = feature_tuple[1]
			if is_header:
				pos_list = self.append_parts_of_speech_list(cursor, navigable_parent, pos_list=[])
			else:
				pos_list.append(pos)
		consecutives_list = []
		from itertools import groupby
		for k, v in groupby(pos_list):
			consecutives_list.append((k, len(list(v))))

		return consecutives_list, pos_list



	def create_navigableparent_is_qual_dictionary(self, cursor, verbose=False):
		
		# Get the already-qualified html strings
		sql_str = '''
			SELECT
				np.[navigable_parent],
				np.[is_qualification]
			FROM [Jobhunting].[dbo].[NavigableParents] np
			WHERE np.[is_qualification] IS NOT NULL'''
		is_qualification_df = pd.DataFrame(self.get_execution_results(cursor, sql_str, verbose=verbose))
		is_qualification_df.is_qualification = is_qualification_df.is_qualification.astype('bool')
		
		# Initialize and populate the header pattern dictionary
		NAVIGABLE_PARENT_IS_QUAL_DICT = {}
		for row_index, row_series in is_qualification_df.iterrows():
			is_fit = row_series.is_qualification
			qualification_str = row_series.navigable_parent
			
			NAVIGABLE_PARENT_IS_QUAL_DICT[qualification_str] = is_fit
			self.s.store_objects(NAVIGABLE_PARENT_IS_QUAL_DICT=NAVIGABLE_PARENT_IS_QUAL_DICT, verbose=verbose)



	def create_navigableparent_is_header_dictionary(self, cursor, verbose=False):
		
		# Get the already-headered html strings
		sql_str = '''
			SELECT
				np.[navigable_parent],
				np.[is_header]
			FROM [Jobhunting].[dbo].[NavigableParents] np
			WHERE np.[is_header] IS NOT NULL'''
		is_header_df = pd.DataFrame(self.get_execution_results(cursor, sql_str, verbose=verbose))
		is_header_df.is_header = is_header_df.is_header.astype('bool')
		
		# Initialize and populate the navigable parent is header dictionary
		NAVIGABLE_PARENT_IS_HEADER_DICT = {}
		for row_index, row_series in is_header_df.iterrows():
			is_header = row_series.is_header
			child_str = row_series.navigable_parent
			
			NAVIGABLE_PARENT_IS_HEADER_DICT[child_str] = is_header
			self.s.store_objects(NAVIGABLE_PARENT_IS_HEADER_DICT=NAVIGABLE_PARENT_IS_HEADER_DICT, verbose=verbose)



	def create_header_tag_sequence_table_dataframe(self, save_as_csv=False, verbose=False):
		HEADER_PATTERN_DICT = self.s.load_object('HEADER_PATTERN_DICT')
		rows_list = []
		for file_name, feature_dict_list in HEADER_PATTERN_DICT.items():
			item_sequence = [feature_dict['initial_tag'] for feature_dict in feature_dict_list]
			for i, header_tag in enumerate(item_sequence):
				row_dict = {}
				row_dict['file_name'] = file_name.strip()
				row_dict['header_tag'] = header_tag
				row_dict['sequence_order'] = i
				rows_list.append(row_dict)
		header_tag_sequence_table_df = pd.DataFrame(rows_list)
		header_tag_sequence_table_df.index.name = 'header_tag_sequence_id'
		if save_as_csv:
			self.s.save_dataframes(include_index=True, verbose=verbose, header_tag_sequence_table_df=header_tag_sequence_table_df)

		return header_tag_sequence_table_df



	def get_jh_conn_cursor(self):
		conn = pyodbc.connect(
			driver='{SQL Server}',
			server='localhost\MSSQLSERVER01',
			database='Jobhunting',
			trusted_connection=True
		)
		cursor = conn.cursor()

		return conn, cursor



	def get_filenames_by_starting_sequence(self, cursor, sequence_list=[], verbose=False):

		# https://stackoverflow.com/questions/5160742/how-to-store-and-search-for-a-sequence-in-a-rdbms
		filenames_list = []
		if len(sequence_list):
			if verbose:
				print(self.create_query_table_sql_str)
			cursor.execute(self.create_query_table_sql_str)
			try:
				columns_list = [c[0] for c in cursor_obj.description]
				row_objs_list = [dict(zip(columns_list, row)) for row in cursor_obj.fetchall()]
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
					columns_list = [c[0] for c in cursor_obj.description]
					row_objs_list = [dict(zip(columns_list, row)) for row in cursor_obj.fetchall()]
				except:
					row_objs_list = []
			if verbose:
				print(self.select_query_sql_str)
			cursor.execute(self.select_query_sql_str)
			try:
				columns_list = [c[0] for c in cursor_obj.description]
				row_objs_list = [dict(zip(columns_list, row)) for row in cursor_obj.fetchall()]
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
					columns_list = [c[0] for c in cursor_obj.description]
					row_objs_list = [dict(zip(columns_list, row)) for row in cursor_obj.fetchall()]
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
						columns_list = [c[0] for c in cursor_obj.description]
						row_objs_list = [dict(zip(columns_list, row)) for row in cursor_obj.fetchall()]
						row_tuples_list = [tuple(row_obj) for row_obj in row_objs_list]
					except:
						row_tuples_list = []

				# Find sequence list by file name
				if verbose:
					print(self.select_query_sql_str)
				cursor.execute(self.select_query_sql_str)
				try:
					columns_list = [c[0] for c in cursor_obj.description]
					row_objs_list = [dict(zip(columns_list, row)) for row in cursor_obj.fetchall()]
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
	
	
	def create_task_scope_pickle(self, cursor, verbose=False):
		
		# Get the task scope headers
		sql_str = '''
			SELECT
				np.[navigable_parent],
				np.[is_task_scope]
			FROM [Jobhunting].[dbo].[NavigableParents] np
			WHERE np.[is_task_scope] IS NOT NULL'''
		task_scope_df = pd.DataFrame(self.get_execution_results(cursor, sql_str, verbose=verbose))
		task_scope_df.is_task_scope = task_scope_df.is_task_scope.astype('bool')
		
		# Initialize and populate the task scope list
		TASK_SCOPE_HEADERS_LIST = task_scope_df[task_scope_df.is_task_scope].navigable_parent.tolist()
		self.s.store_objects(TASK_SCOPE_HEADERS_LIST=TASK_SCOPE_HEADERS_LIST, verbose=verbose)
	
	
	def create_req_quals_pickle(self, cursor, verbose=False):
		
		# Get the req quals headers
		sql_str = '''
			SELECT
				np.[navigable_parent],
				np.[is_minimum_qualification]
			FROM [Jobhunting].[dbo].[NavigableParents] np
			WHERE np.[is_minimum_qualification] IS NOT NULL'''
		req_quals_df = pd.DataFrame(self.get_execution_results(cursor, sql_str, verbose=verbose))
		req_quals_df.is_minimum_qualification = req_quals_df.is_minimum_qualification.astype('bool')
		
		# Initialize and populate the req quals list
		REQ_QUALS_HEADERS_LIST = req_quals_df[req_quals_df.is_minimum_qualification].navigable_parent.tolist()
		self.s.store_objects(REQ_QUALS_HEADERS_LIST=REQ_QUALS_HEADERS_LIST, verbose=verbose)
	
	
	def create_o_rq_pickle(self, cursor, verbose=False):
		
		# Get the req quals non-headers
		sql_str = '''
			SELECT
				np.[navigable_parent],
				np.[is_minimum_qualification],
				np.[is_header]
			FROM [Jobhunting].[dbo].[NavigableParents] np
			WHERE
				np.[is_minimum_qualification] IS NOT NULL AND
				np.[is_header] IS NOT NULL;'''
		req_quals_df = pd.DataFrame(self.get_execution_results(cursor, sql_str, verbose=verbose))
		req_quals_df.is_minimum_qualification = req_quals_df.is_minimum_qualification.astype('bool')
		req_quals_df.is_header = req_quals_df.is_header.astype('bool')
		
		# Initialize and populate the req quals non-headers dictionary
		O_RQ_DICT = {}
		for row_index, row_series in req_quals_df.iterrows():
			is_minimum_qualification = row_series.is_minimum_qualification
			is_header = row_series.is_header
			navigable_parent = row_series.navigable_parent
			if is_minimum_qualification and not is_header:
				O_RQ_DICT[navigable_parent] = True
			else:
				O_RQ_DICT[navigable_parent] = False
	
	
	def create_h_rq_pickle(self, cursor, verbose=False):
		
		# Get the req quals headers
		sql_str = '''
			SELECT
				np.[navigable_parent],
				np.[is_minimum_qualification],
				np.[is_header]
			FROM [Jobhunting].[dbo].[NavigableParents] np
			WHERE
				np.[is_minimum_qualification] IS NOT NULL AND
				np.[is_header] IS NOT NULL;'''
		req_quals_df = pd.DataFrame(self.get_execution_results(cursor, sql_str, verbose=verbose))
		req_quals_df.is_minimum_qualification = req_quals_df.is_minimum_qualification.astype('bool')
		req_quals_df.is_header = req_quals_df.is_header.astype('bool')
		
		# Initialize and populate the req quals headers dictionary
		H_RQ_DICT = {}
		for row_index, row_series in req_quals_df.iterrows():
			is_minimum_qualification = row_series.is_minimum_qualification
			is_header = row_series.is_header
			navigable_parent = row_series.navigable_parent
			if is_minimum_qualification and is_header:
				H_RQ_DICT[navigable_parent] = True
			else:
				H_RQ_DICT[navigable_parent] = False
		
		self.s.store_objects(H_RQ_DICT=H_RQ_DICT, verbose=verbose)
	
	
	def create_preff_quals_pickle(self, cursor, verbose=False):
		
		# Get the preff quals headers
		sql_str = '''
			SELECT
				np.[navigable_parent],
				np.[is_preferred_qualification]
			FROM [Jobhunting].[dbo].[NavigableParents] np
			WHERE np.[is_preferred_qualification] IS NOT NULL'''
		preff_quals_df = pd.DataFrame(self.get_execution_results(cursor, sql_str, verbose=verbose))
		preff_quals_df.is_preferred_qualification = preff_quals_df.is_preferred_qualification.astype('bool')
		
		# Initialize and populate the preff quals list
		PREFF_QUALS_HEADERS_LIST = preff_quals_df[preff_quals_df.is_preferred_qualification].navigable_parent.tolist()
		self.s.store_objects(PREFF_QUALS_HEADERS_LIST=PREFF_QUALS_HEADERS_LIST, verbose=verbose)
	
	
	def create_legal_notifs_pickle(self, cursor, verbose=False):
		
		# Get the legal notifs headers
		sql_str = '''
			SELECT
				np.[navigable_parent],
				np.[is_legal_notification]
			FROM [Jobhunting].[dbo].[NavigableParents] np
			WHERE np.[is_legal_notification] IS NOT NULL'''
		legal_notifs_df = pd.DataFrame(self.get_execution_results(cursor, sql_str, verbose=verbose))
		legal_notifs_df.is_legal_notification = legal_notifs_df.is_legal_notification.astype('bool')
		
		# Initialize and populate the legal notifs list
		LEGAL_NOTIFS_HEADERS_LIST = legal_notifs_df[legal_notifs_df.is_legal_notification].navigable_parent.tolist()
		self.s.store_objects(LEGAL_NOTIFS_HEADERS_LIST=LEGAL_NOTIFS_HEADERS_LIST, verbose=verbose)
	
	
	def create_job_title_pickle(self, cursor, verbose=False):
		
		# Get the job title headers
		sql_str = '''
			SELECT
				np.[navigable_parent],
				np.[is_job_title]
			FROM [Jobhunting].[dbo].[NavigableParents] np
			WHERE np.[is_job_title] IS NOT NULL'''
		job_title_df = pd.DataFrame(self.get_execution_results(cursor, sql_str, verbose=verbose))
		job_title_df.is_job_title = job_title_df.is_job_title.astype('bool')
		
		# Initialize and populate the job title list
		JOB_TITLE_HEADERS_LIST = job_title_df[job_title_df.is_job_title].navigable_parent.tolist()
		self.s.store_objects(JOB_TITLE_HEADERS_LIST=JOB_TITLE_HEADERS_LIST, verbose=verbose)
	
	
	def create_office_loc_pickle(self, cursor, verbose=False):
		
		# Get the office loc headers
		sql_str = '''
			SELECT
				np.[navigable_parent],
				np.[is_office_location]
			FROM [Jobhunting].[dbo].[NavigableParents] np
			WHERE np.[is_office_location] IS NOT NULL'''
		office_loc_df = pd.DataFrame(self.get_execution_results(cursor, sql_str, verbose=verbose))
		office_loc_df.is_office_location = office_loc_df.is_office_location.astype('bool')
		
		# Initialize and populate the office location list
		OFFICE_LOC_HEADERS_LIST = office_loc_df[office_loc_df.is_office_location].navigable_parent.tolist()
		self.s.store_objects(OFFICE_LOC_HEADERS_LIST=OFFICE_LOC_HEADERS_LIST, verbose=verbose)
	
	
	def create_job_duration_pickle(self, cursor, verbose=False):
		
		# Get the job duration headers
		sql_str = '''
			SELECT
				np.[navigable_parent],
				np.[is_job_duration]
			FROM [Jobhunting].[dbo].[NavigableParents] np
			WHERE np.[is_job_duration] IS NOT NULL'''
		job_duration_df = pd.DataFrame(self.get_execution_results(cursor, sql_str, verbose=verbose))
		job_duration_df.is_job_duration = job_duration_df.is_job_duration.astype('bool')
		
		# Initialize and populate the job duration list
		JOB_DURATION_HEADERS_LIST = job_duration_df[job_duration_df.is_job_duration].navigable_parent.tolist()
		self.s.store_objects(JOB_DURATION_HEADERS_LIST=JOB_DURATION_HEADERS_LIST, verbose=verbose)
	
	
	def create_supp_pay_pickle(self, cursor, verbose=False):
		
		# Get the supp pay headers
		sql_str = '''
			SELECT
				np.[navigable_parent],
				np.[is_supplemental_pay]
			FROM [Jobhunting].[dbo].[NavigableParents] np
			WHERE np.[is_supplemental_pay] IS NOT NULL'''
		supp_pay_df = pd.DataFrame(self.get_execution_results(cursor, sql_str, verbose=verbose))
		supp_pay_df.is_supplemental_pay = supp_pay_df.is_supplemental_pay.astype('bool')
		
		# Initialize and populate the supplemental pay list
		SUPP_PAY_HEADERS_LIST = supp_pay_df[supp_pay_df.is_supplemental_pay].navigable_parent.tolist()
		self.s.store_objects(SUPP_PAY_HEADERS_LIST=SUPP_PAY_HEADERS_LIST, verbose=verbose)
	
	
	def create_educ_reqs_pickle(self, cursor, verbose=False):
		
		# Get the educ reqs headers
		sql_str = '''
			SELECT
				np.[navigable_parent],
				np.[is_educational_requirement]
			FROM [Jobhunting].[dbo].[NavigableParents] np
			WHERE np.[is_educational_requirement] IS NOT NULL'''
		educ_reqs_df = pd.DataFrame(self.get_execution_results(cursor, sql_str, verbose=verbose))
		educ_reqs_df.is_educational_requirement = educ_reqs_df.is_educational_requirement.astype('bool')
		
		# Initialize and populate the educational requirements list
		EDUC_REQS_HEADERS_LIST = educ_reqs_df[educ_reqs_df.is_educational_requirement].navigable_parent.tolist()
		self.s.store_objects(EDUC_REQS_HEADERS_LIST=EDUC_REQS_HEADERS_LIST, verbose=verbose)
	
	
	def create_interv_proc_pickle(self, cursor, verbose=False):
		
		# Get the interv proc headers
		sql_str = '''
			SELECT
				np.[navigable_parent],
				np.[is_interview_procedure]
			FROM [Jobhunting].[dbo].[NavigableParents] np
			WHERE np.[is_interview_procedure] IS NOT NULL'''
		interv_proc_df = pd.DataFrame(self.get_execution_results(cursor, sql_str, verbose=verbose))
		interv_proc_df.is_interview_procedure = interv_proc_df.is_interview_procedure.astype('bool')
		
		# Initialize and populate the interview procedure list
		INTERV_PROC_HEADERS_LIST = interv_proc_df[interv_proc_df.is_interview_procedure].navigable_parent.tolist()
		self.s.store_objects(INTERV_PROC_HEADERS_LIST=INTERV_PROC_HEADERS_LIST, verbose=verbose)
	
	
	def create_corp_scope_pickle(self, cursor, verbose=False):
		
		# Get the corp scope headers
		sql_str = '''
			SELECT
				np.[navigable_parent],
				np.[is_corporate_scope]
			FROM [Jobhunting].[dbo].[NavigableParents] np
			WHERE np.[is_corporate_scope] IS NOT NULL'''
		corp_scope_df = pd.DataFrame(self.get_execution_results(cursor, sql_str, verbose=verbose))
		corp_scope_df.is_corporate_scope = corp_scope_df.is_corporate_scope.astype('bool')
		
		# Initialize and populate the corporate scope list
		CORP_SCOPE_HEADERS_LIST = corp_scope_df[corp_scope_df.is_corporate_scope].navigable_parent.tolist()
		self.s.store_objects(CORP_SCOPE_HEADERS_LIST=CORP_SCOPE_HEADERS_LIST, verbose=verbose)
	
	
	def create_post_date_pickle(self, cursor, verbose=False):
		
		# Get the post date headers
		sql_str = '''
			SELECT
				np.[navigable_parent],
				np.[is_posting_date]
			FROM [Jobhunting].[dbo].[NavigableParents] np
			WHERE np.[is_posting_date] IS NOT NULL'''
		post_date_df = pd.DataFrame(self.get_execution_results(cursor, sql_str, verbose=verbose))
		post_date_df.is_posting_date = post_date_df.is_posting_date.astype('bool')
		
		# Initialize and populate the posting date list
		POST_DATE_HEADERS_LIST = post_date_df[post_date_df.is_posting_date].navigable_parent.tolist()
		self.s.store_objects(POST_DATE_HEADERS_LIST=POST_DATE_HEADERS_LIST, verbose=verbose)
	
	
	def create_other_pickle(self, cursor, verbose=False):
		
		# Get the other headers
		sql_str = '''
			SELECT
				np.[navigable_parent],
				np.[is_other]
			FROM [Jobhunting].[dbo].[NavigableParents] np
			WHERE np.[is_other] IS NOT NULL'''
		other_df = pd.DataFrame(self.get_execution_results(cursor, sql_str, verbose=verbose))
		other_df.is_other = other_df.is_other.astype('bool')
		
		# Initialize and populate the other list
		OTHER_HEADERS_LIST = other_df[other_df.is_other].navigable_parent.tolist()
		self.s.store_objects(OTHER_HEADERS_LIST=OTHER_HEADERS_LIST, verbose=verbose)