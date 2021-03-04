
#!/usr/bin/env python
# coding: utf-8

import html_analysis
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import sql_utlis
import storage

class ChartUtilities(object):
	"""Chart class."""

	def __init__(self):
		self.s = storage.Storage()
		self.su = sql_utlis.SqlUtilities()
		self.conn, self.cursor = self.su.get_jh_conn_cursor()
		self.ea = html_analysis.ElementAnalysis()
		self.hc = html_analysis.HeaderCategories()
	
	
	def plot_child_str_predictions(self, file_name=None, verbose=False):
		if file_name is None:
			files_list = self.su.get_files_list(self.cursor, verbose=verbose)
			file_name = random.choice(files_list)
		HEADER_PATTERN_DICT = self.s.load_object('HEADER_PATTERN_DICT')
		NAVIGABLE_PARENT_IS_HEADER_DICT = self.s.load_object('NAVIGABLE_PARENT_IS_HEADER_DICT')
		child_strs_list = self.su.get_child_strs_from_file(self.cursor, file_name, verbose=verbose)
		if file_name in HEADER_PATTERN_DICT:
			feature_dict_list = HEADER_PATTERN_DICT[file_name]
			feature_tuple_list = [self.hc.get_feature_tuple(feature_dict) for feature_dict in feature_dict_list]
			prediction_dict_list = self.ea.CRF.predict_marginals_single(self.ea.sent2features(feature_tuple_list))
		else:
			prediction_dict_list = []
			for child_str in child_strs_list:
				H = self.ea.lda_predict_percent(child_str) / 13
				prediction_dict = {'H': H}
				prediction_dict_list.append(prediction_dict)
		rows_list = []
		for child_str, marginals_dict in zip(child_strs_list, prediction_dict_list):
			row_dict = {'probability': marginals_dict['H']}
			if child_str in NAVIGABLE_PARENT_IS_HEADER_DICT:
				row_dict['actual'] = NAVIGABLE_PARENT_IS_HEADER_DICT[child_str] * 1.0
			else:
				row_dict['actual'] = np.nan
			rows_list.append(row_dict)
		ax = plt.figure(figsize=(18, 2.5)).add_subplot(1, 1, 1)
		AxesSubplot_obj = pd.DataFrame(rows_list).plot.line(ax=ax)
		ax.axis('off')
		for x, child_str in enumerate(child_strs_list):
			y = rows_list[x]['probability']
			if str(y) == 'nan':
				y = rows_list[x]['actual']
			if str(y) != 'nan':
				ax.annotate(f'{child_str[:20]}...', (x, y), ha='left', rotation=90)