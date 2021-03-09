
#!/usr/bin/env python
# coding: utf-8

from IPython.display import HTML, display
from cycler import cycler
from matplotlib.colors import to_hex
import html_analysis
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import sql_utlis
import storage

class ChartUtilities(object):
	"""Chart class."""

	def __init__(self, su=None, verbose=False):
		self.s = storage.Storage()
		if su is None:
			self.su = sql_utlis.SqlUtilities()
		else:
			self.su = su
		self.conn, self.cursor = self.su.get_jh_conn_cursor()
		# self.ea = html_analysis.ElementAnalysis()
		# self.hc = html_analysis.HeaderCategories()
		self.crf = html_analysis.CrfUtilities()
		if self.s.pickle_exists('POS_DICT'):
			self.POS_DICT = self.s.load_object('POS_DICT')
		else:
			sql_str = f'''
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
			pos_df = pd.DataFrame(self.su.get_execution_results(self.cursor, sql_str, verbose=False))
			self.POS_DICT = pos_df.set_index('navigable_parent')['pos_symbol'].to_dict()
			self.s.store_objects(POS_DICT=self.POS_DICT, verbose=verbose)
	
	
	def get_pos_color_dictionary(self, verbose=False):
		sql_str = '''
		SELECT pos.[pos_symbol]
		FROM [Jobhunting].[dbo].[PartsOfSpeech] pos
		WHERE pos.[is_header] = 1;'''
		pos_df = pd.DataFrame(self.su.get_execution_results(self.cursor, sql_str, verbose=verbose))
		color_cycler = cycler('color', plt.cm.tab20(np.linspace(0, 1, pos_df.shape[0])))
		header_pos_list = pos_df.pos_symbol.tolist()
		rgba_dict = {}
		for header_pos_symbol, face_color_dict in zip(header_pos_list, color_cycler()):
			face_color = face_color_dict['color']
			rgba_dict[header_pos_symbol] = face_color
		for header_pos_symbol, face_color in rgba_dict.copy().items():
			nonheader_pos_symbol = 'O-' + header_pos_symbol.split('-')[1]
			fc_array = face_color.copy()
			fc_array[-1] = 0.5
			rgba_dict[nonheader_pos_symbol] = fc_array
		rgba_dict['H'] = [0.0, 0.0, 0.0, 1.0]
		rgba_dict['O'] = [0.0, 0.0, 0.0, 0.5]
		
		return rgba_dict
	
	
	def visualize_cfr_child_str_predictions(self, file_name=None, verbose=False):
		if file_name is None:
			files_list = self.su.get_files_list(self.cursor, verbose=verbose)
			file_name = random.choice(files_list)
		HEADER_PATTERN_DICT = self.s.load_object('HEADER_PATTERN_DICT')
		child_strs_list = self.su.get_child_strs_from_file(self.cursor, file_name, verbose=verbose)
		if file_name in HEADER_PATTERN_DICT:
			y_true = []
			feature_dict_list = HEADER_PATTERN_DICT[file_name]
			for feature_dict in feature_dict_list:
				sent_str = feature_dict['child_str']
				if sent_str in self.POS_DICT:
					pos_symbol = self.POS_DICT[sent_str]
					y_true.append(pos_symbol)
				else:
					y_true.append(np.nan)
		else:
			y_true = [np.nan] * len(child_strs_list)
			child_tags_list = self.su.get_child_tags_list(self.cursor, child_strs_list)
			feature_dict_list = self.su.get_feature_dict_list(self.cursor, child_tags_list, child_strs_list)
		# feature_tuple_list = [self.hc.get_feature_tuple(feature_dict) for feature_dict in feature_dict_list]
		# y_pred = self.crf.CRF.predict_single(self.ea.sent2features(feature_tuple_list))
		y_pred = self.crf.CRF.predict_single(xseq=feature_dict_list)
		rgba_dict = self.get_pos_color_dictionary(verbose=verbose)
		html_str = ''
		for child_str, pos_symbol_pred, pos_symbol_true in zip(child_strs_list, y_pred, y_true):
			plotted = pos_symbol_true
			if str(plotted) == 'nan':
				plotted = pos_symbol_pred
			if str(plotted) != 'nan':
				rgba = rgba_dict[plotted]
				hex_str = to_hex(rgba, keep_alpha=True)
				html_str += f'<span style="color:{hex_str};">{child_str}</span> ({pos_symbol_pred})<br />'
		display(HTML(html_str))
		
		return y_pred