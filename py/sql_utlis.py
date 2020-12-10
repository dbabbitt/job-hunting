#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import random
import pyodbc

import storage
s = storage.Storage()

import html_analysis
ha = html_analysis.HeaderAnalysis()

class SqlUtilities(object):
	"""SQL class."""
	
	def __init__(self, database_name='Jobhunting'):
		self.sql_server_name = 'localhost\MSSQLSERVER01'
		self.server_driver = '{SQL Server}'
		self.database_name = database_name
		
		# Various SQL strings
		self.create_database_sql_str = f'''
IF (EXISTS (
	SELECT * FROM master.dbo.sysdatabases
	WHERE name = N'{self.database_name}'
	))
	BEGIN
		SELECT 'DATABASE already EXISTS' AS Message
	END
ELSE
	BEGIN
		CREATE DATABASE [{self.database_name}];
		SELECT * FROM master.dbo.sysdatabases
		WHERE name = N'{self.database_name}'
	END;'''
		self.create_table_sql_str = '''
IF (EXISTS (
	SELECT * FROM INFORMATION_SCHEMA.TABLES
	WHERE TABLE_NAME = N'HeaderTagSequence'
	))
	BEGIN
		SELECT 'TABLE_NAME already EXISTS' AS Message
	END
ELSE
	BEGIN
		CREATE TABLE HeaderTagSequence(
			header_tag_sequence_id INT PRIMARY KEY,
			file_name VARCHAR (255) NOT NULL,
			header_tag NVARCHAR (2224) NOT NULL,
			sequence_order INT NOT NULL
		);
		SELECT * FROM INFORMATION_SCHEMA.TABLES
		WHERE TABLE_NAME = N'HeaderTagSequence'
	END;'''
		self.insert_columns_sql_str = '''
SET QUOTED_IDENTIFIER OFF
SET ANSI_NULLS ON
IF (EXISTS (
	SELECT * FROM HeaderTagSequence WHERE
		file_name = ? AND
		sequence_order = ?
	))
	BEGIN
		SELECT 'Row already EXISTS' AS Message
	END
ELSE
	BEGIN
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
		);
		SELECT * FROM HeaderTagSequence WHERE
			file_name = ? AND
			sequence_order = ?
	END;'''
		self.create_query_table_sql_str = '''
CREATE TABLE #query(
	header_tag NVARCHAR (2224) NOT NULL,
	sequence_order INT NOT NULL
);'''
		self.insert_query_rows_sql_str = '''
INSERT INTO #query (
	header_tag,
	sequence_order
) values(
	?,
	?
);'''
		self.select_query_sql_str = '''
SELECT file_name
FROM HeaderTagSequence s
	INNER JOIN #query q
	ON
		q.header_tag = s.header_tag AND
		q.sequence_order = s.sequence_order
GROUP BY s.file_name
HAVING Count(*) = (SELECT Count(*) FROM #query)'''
		
		# Indexes for database_cursor.columns(table=table_name)
		self.table_cat_idx = 0
		self.table_schem_idx = 1
		self.table_name_idx = 2
		self.column_name_idx = 3
		self.data_type_idx = 4
		self.type_name_idx = 5
		self.column_size_idx = 6
		self.buffer_length_idx = 7
		self.decimal_digits_idx = 8
		self.num_prec_radix_idx = 9
		self.nullable_idx = 10
		self.remarks_idx = 11
		self.column_def_idx = 12
		self.sql_data_type_idx = 13
		self.sql_datetime_sub_idx = 14
		self.char_octet_length_idx = 15
		self.ordinal_position_idx = 16
		self.is_nullable_idx = 17



	def get_jh_conn_cursor(self):
		conn = pyodbc.connect(
			driver=self.server_driver,
			server=self.sql_server_name,
			database=self.database_name,
			trusted_connection=True
		)
		cursor = conn.cursor()
		
		return conn, cursor



	def get_execution_results(self, sql_str, database='Jobhunting', verbose=False):
		if database == self.database_name:
			conn, cursor = self.get_jh_conn_cursor()
		else:
			conn = pyodbc.connect(
				driver=self.server_driver,
				server=self.sql_server_name,
				database=database,
				trusted_connection=True
			)
			cursor = conn.cursor()
		if verbose:
			print(sql_str)
		cursor.execute(sql_str)
		try:
			row_objs_list = cursor.fetchall()
			row_tuples_list = [tuple(row_obj) for row_obj in row_objs_list]
		except:
			row_tuples_list = []
		conn.commit()
		cursor.close()
		
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



	def create_header_tag_sequence_table(self, verbose=False):
		row_tuples_list = self.get_execution_results(self.create_database_sql_str, database='master', verbose=verbose)
		row_tuples_list = self.get_execution_results(self.create_table_sql_str, verbose=verbose)
		
		# Create the navigable html strings dataset
		header_tag_sequence_table_df = self.create_header_tag_sequence_table_dataframe(verbose=verbose)
		
		# Insert Dataframe into SQL Server:
		conn, cursor = self.get_jh_conn_cursor()
		for row_index, row_series in header_tag_sequence_table_df.iterrows():
			if verbose:
				print(self.insert_columns_sql_str.replace('?', '"{}"').format(row_series.file_name, row_series.sequence_order,
																			  row_index, row_series.file_name,
																			  row_series.header_tag, row_series.sequence_order,
																			  row_series.file_name, row_series.sequence_order))
			try:
				cursor.execute(self.insert_columns_sql_str, row_series.file_name, row_series.sequence_order, row_index,
							   row_series.file_name, row_series.header_tag, row_series.sequence_order, row_series.file_name,
							   row_series.sequence_order)
			except Exception as e:
				print(str(e).strip())
				print(self.insert_columns_sql_str.replace('?', '"{}"').format(row_series.file_name, row_series.sequence_order,
																			  row_index, row_series.file_name,
																			  row_series.header_tag, row_series.sequence_order,
																			  row_series.file_name, row_series.sequence_order))
				break
			try:
				row_objs_list = cursor.fetchall()
			except:
				row_objs_list = []
		conn.commit()
		cursor.close()



	def get_filenames_by_starting_sequence(self, sequence_list=[], verbose=False):
	
		# https://stackoverflow.com/questions/5160742/how-to-store-and-search-for-a-sequence-in-a-rdbms
		
		# Insert sequence list into SQL Server:
		if len(sequence_list):
			conn, cursor = self.get_jh_conn_cursor()
			start_num = 0
			row_tuples_list = []
			while start_num < len(sequence_list) or not len(row_tuples_list):
				if len(row_tuples_list):
					break
				start_num += 1
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
			conn.commit()
			cursor.close()
			filenames_list = [filename_tuple[0] for filename_tuple in row_tuples_list]
			
			return filenames_list



	def get_filenames_by_sequence(self, sequence_list=[], verbose=False):
		
		# Insert sequence list into SQL Server:
		if len(sequence_list):
			conn, cursor = self.get_jh_conn_cursor()
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
			conn.commit()
			cursor.close()
			filenames_list = [filename_tuple[0] for filename_tuple in row_tuples_list]
			
			return filenames_list