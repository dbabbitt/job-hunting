
#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
import pyodbc
import random
from neo4j import GraphDatabase
import re
try:
    import html_analysis
except:
    import flaskr.html_analysis
import hashlib



class CypherUtilities(object):
    """CYPHER class."""

    def __init__(self, uri=None, user=None, password=None, driver=None, s=None, ha=None):
        if uri is None:
            self.uri = 'bolt://localhost:7687'
        else:
            self.uri = uri
        if user is None:
            self.user = 'neo4j'
        else:
            self.user = user
        if password is None:
            self.password = 'neo4j@WSXcde3'
        else:
            self.password = password
        if driver is None:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        else:
            self.driver = driver
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

        # File Names Table CYPHER
        # The email date is in the form of ISO8601 strings ("YYYY-MM-DD HH:MM:SS.SSS")
        self.create_filenames_table_cypher_str = """
            LOAD CSV WITH HEADERS FROM 'file:///FileNames.csv' AS row
            WITH
                toInteger(row.file_name_id) AS file_name_id,
                row.file_name AS file_name,
                row.percent_fit AS percent_fit,
                row.is_opportunity_application_emailed AS is_opportunity_application_emailed,
                row.opportunity_application_email_date AS opportunity_application_email_date,
                row.is_remote_delivery AS is_remote_delivery,
                row.manager_notes AS manager_notes
            MERGE (fn:FileNames {file_name_id: file_name_id}) SET
                fn.file_name = file_name,
                fn.percent_fit = percent_fit,
                fn.is_opportunity_application_emailed = is_opportunity_application_emailed,
                fn.opportunity_application_email_date = opportunity_application_email_date,
                fn.is_remote_delivery = is_remote_delivery,
                fn.manager_notes = manager_notes;"""
        self.select_file_names_cypher_str = """
            MATCH (fn:FileNames)
            RETURN fn;"""
        self.select_file_name_where_is_qualification_cypher_str = """
            MATCH (fn:FileNames)<--(nps:NavigableParentSequence)<--(np:NavigableParents)
            WHERE
                np.is_minimum_qualification = 'True' AND
                np.is_header = 'True'
            RETURN fn.file_name;"""


        # Header Tags Table CYPHER
        self.create_headertags_table_cypher_str = """
            LOAD CSV WITH HEADERS FROM 'file:///HeaderTags.csv' AS row
            WITH
                toInteger(row.header_tag_id) AS header_tag_id,
                row.is_in_document_structure_elements_set AS is_in_document_structure_elements_set,
                row.is_in_document_head_elements_set AS is_in_document_head_elements_set,
                row.is_in_document_body_elements_set AS is_in_document_body_elements_set,
                row.is_in_block_elements_set AS is_in_block_elements_set,
                row.is_in_basic_text_set AS is_in_basic_text_set,
                row.is_in_section_headings_set AS is_in_section_headings_set,
                row.is_in_lists_set AS is_in_lists_set,
                row.is_in_other_block_elements_set AS is_in_other_block_elements_set,
                row.is_in_inline_elements_set AS is_in_inline_elements_set,
                row.is_in_anchor_set AS is_in_anchor_set,
                row.is_in_phrase_elements_set AS is_in_phrase_elements_set,
                row.is_in_general_set AS is_in_general_set,
                row.is_in_computer_phrase_elements_set AS is_in_computer_phrase_elements_set,
                row.is_in_presentation_set AS is_in_presentation_set,
                row.is_in_span_set AS is_in_span_set,
                row.is_in_other_inline_elements_set AS is_in_other_inline_elements_set,
                row.is_in_images_and_objects_set AS is_in_images_and_objects_set,
                row.is_in_forms_set AS is_in_forms_set,
                row.is_in_tables_set AS is_in_tables_set,
                row.is_in_frames_set AS is_in_frames_set,
                row.is_in_historic_elements_set AS is_in_historic_elements_set,
                row.is_in_non_standard_elements_set AS is_in_non_standard_elements_set,
                row.header_tag AS header_tag
            MERGE (ht:HeaderTags {header_tag_id: header_tag_id}) SET
                ht.is_in_document_structure_elements_set = is_in_document_structure_elements_set,
                ht.is_in_document_head_elements_set = is_in_document_head_elements_set,
                ht.is_in_document_body_elements_set = is_in_document_body_elements_set,
                ht.is_in_block_elements_set = is_in_block_elements_set,
                ht.is_in_basic_text_set = is_in_basic_text_set,
                ht.is_in_section_headings_set = is_in_section_headings_set,
                ht.is_in_lists_set = is_in_lists_set,
                ht.is_in_other_block_elements_set = is_in_other_block_elements_set,
                ht.is_in_inline_elements_set = is_in_inline_elements_set,
                ht.is_in_anchor_set = is_in_anchor_set,
                ht.is_in_phrase_elements_set = is_in_phrase_elements_set,
                ht.is_in_general_set = is_in_general_set,
                ht.is_in_computer_phrase_elements_set = is_in_computer_phrase_elements_set,
                ht.is_in_presentation_set = is_in_presentation_set,
                ht.is_in_span_set = is_in_span_set,
                ht.is_in_other_inline_elements_set = is_in_other_inline_elements_set,
                ht.is_in_images_and_objects_set = is_in_images_and_objects_set,
                ht.is_in_forms_set = is_in_forms_set,
                ht.is_in_tables_set = is_in_tables_set,
                ht.is_in_frames_set = is_in_frames_set,
                ht.is_in_historic_elements_set = is_in_historic_elements_set,
                ht.is_in_non_standard_elements_set = is_in_non_standard_elements_set,
                ht.header_tag = header_tag;"""
        self.insert_into_headertags_cypher_str = """
            CREATE ({}:HeaderTags {{
                header_tag: '{}',
                is_in_document_structure_elements_set: '{}',
                is_in_document_head_elements_set: '{}',
                is_in_document_body_elements_set: '{}',
                is_in_block_elements_set: '{}',
                is_in_basic_text_set: '{}',
                is_in_section_headings_set: '{}',
                is_in_lists_set: '{}',
                is_in_other_block_elements_set: '{}',
                is_in_inline_elements_set: '{}',
                is_in_anchor_set: '{}',
                is_in_phrase_elements_set: '{}',
                is_in_general_set: '{}',
                is_in_computer_phrase_elements_set: '{}',
                is_in_presentation_set: '{}',
                is_in_span_set: '{}',
                is_in_other_inline_elements_set: '{}',
                is_in_images_and_objects_set: '{}',
                is_in_forms_set: '{}',
                is_in_tables_set: '{}',
                is_in_frames_set: '{}',
                is_in_historic_elements_set: '{}',
                is_in_non_standard_elements_set: '{}'
                }});"""
        self.select_header_tag_id_where_header_tag_cypher_str = """
            MATCH (ht:HeaderTags {{header_tag: '{}'}})
            RETURN ht.header_tag_id AS header_tag_id;"""
        self.select_header_tag_where_header_tag_id_cypher_str = """
            MATCH (ht:HeaderTags {{header_tag_id: '{}'}})
            RETURN ht.header_tag AS header_tag;"""
        self.select_header_tag_where_navigable_parent_cypher_str = """
            MATCH (np:NavigableParents {{navigable_parent: '{}'}})<-[s:SUMMARIZES]-(ht)
            RETURN ht.header_tag AS header_tag;"""


        # Navigable Parents CYPHER strings
        self.create_navigableparents_table_cypher_str = """
            LOAD CSV WITH HEADERS FROM 'file:///NavigableParents.csv' AS row
            WITH
                toInteger(row.navigable_parent_id) AS navigable_parent_id,
                toInteger(row.header_tag_id) AS header_tag_id,
                row.navigable_parent AS navigable_parent,
                row.is_header AS is_header,
                row.is_task_scope AS is_task_scope,
                row.is_minimum_qualification AS is_minimum_qualification,
                row.is_preferred_qualification AS is_preferred_qualification,
                row.is_legal_notification AS is_legal_notification,
                row.is_job_title AS is_job_title,
                row.is_office_location AS is_office_location,
                row.is_job_duration AS is_job_duration,
                row.is_supplemental_pay AS is_supplemental_pay,
                row.is_educational_requirement AS is_educational_requirement,
                row.is_interview_procedure AS is_interview_procedure,
                row.is_corporate_scope AS is_corporate_scope,
                row.is_posting_date AS is_posting_date,
                row.is_other AS is_other,
                row.is_qualification AS is_qualification
            MERGE (x:NavigableParents {navigable_parent_id: navigable_parent_id}) SET
                x.header_tag_id = header_tag_id,
                x.navigable_parent = navigable_parent,
                x.is_header = is_header,
                x.is_task_scope = is_task_scope,
                x.is_minimum_qualification = is_minimum_qualification,
                x.is_preferred_qualification = is_preferred_qualification,
                x.is_legal_notification = is_legal_notification,
                x.is_job_title = is_job_title,
                x.is_office_location = is_office_location,
                x.is_job_duration = is_job_duration,
                x.is_supplemental_pay = is_supplemental_pay,
                x.is_educational_requirement = is_educational_requirement,
                x.is_interview_procedure = is_interview_procedure,
                x.is_corporate_scope = is_corporate_scope,
                x.is_posting_date = is_posting_date,
                x.is_other = is_other,
                x.is_qualification = is_qualification;"""
        self.insert_into_navigableparents_table_cypher_str = """
            CREATE ({}:NavigableParents {{
                navigable_parent_id: '{}',
                navigable_parent: '{}',
                header_tag_id: '{}',
                is_header: '{}',
                is_task_scope: '{}',
                is_minimum_qualification: '{}',
                is_preferred_qualification: '{}',
                is_legal_notification: '{}',
                is_job_title: '{}',
                is_office_location: '{}',
                is_job_duration: '{}',
                is_supplemental_pay: '{}',
                is_educational_requirement: '{}',
                is_interview_procedure: '{}',
                is_corporate_scope: '{}',
                is_posting_date: '{}',
                is_other: '{}',
                is_qualification: '{}'
                }});"""
        self.select_navigableparentid_cypher_str = """
            MATCH (np:NavigableParents {{navigable_parent: '{}'}})
            RETURN np.navigable_parent_id;"""
        self.select_navigable_parent_by_file_name_cypher_str = '''
            MATCH (fn:FileNames)<--(nps:NavigableParentSequence)<--(np:NavigableParents)
            WHERE fn.file_name = "{}"
            RETURN np.navigable_parent as navigable_parent
            ORDER BY nps.sequence_order;'''
        self.set_is_corporate_scope1_cypher_str = """
            MATCH (np:NavigableParents {{navigable_parent: '{}'}})
            SET np.is_header = 'True', np.is_corporate_scope = 'True';"""
        self.set_is_header1_cypher_str = """
            MATCH (np:NavigableParents {{navigable_parent: '{}'}})
            SET np.is_header = 'True';"""
        self.set_is_header0_cypher_str = """
            MATCH (np:NavigableParents {{navigable_parent: '{}'}})
            SET np.is_header = 'False';"""
        self.set_is_qualification1_cypher_str = """
            MATCH (np:NavigableParents {{navigable_parent: '{}'}})
            SET np.is_qualification = 'True';"""
        self.set_is_qualification0_cypher_str = """
            MATCH (np:NavigableParents {{navigable_parent: '{}'}})
            SET np.is_qualification = 'False';"""
        self.set_is_task_scope1_cypher_str = """
            MATCH (np:NavigableParents {{navigable_parent: '{}'}})
            SET np.is_header = 'True', np.is_task_scope = 'True';"""
        self.set_is_office_location1_cypher_str = """
            MATCH (np:NavigableParents {{navigable_parent: '{}'}})
            SET np.is_header = 'True', np.is_office_location = 'True';"""
        self.set_is_minimum_qualification1_cypher_str = """
            MATCH (np:NavigableParents {{navigable_parent: '{}'}})
            SET np.is_header = 'True', np.is_minimum_qualification = 'True', np.is_qualification = 'True';"""
        self.set_is_supplemental_pay1_cypher_str = """
            MATCH (np:NavigableParents {{navigable_parent: '{}'}})
            SET np.is_header = 'True', np.is_supplemental_pay = 'True';"""
        self.set_nonheader_is_supplemental_pay1_cypher_str = """
            MATCH (np:NavigableParents {{navigable_parent: '{}'}})
            SET np.is_header = 'False', np.is_supplemental_pay = 'True';"""
        self.set_is_preferred_qualification1_cypher_str = """
            MATCH (np:NavigableParents {{navigable_parent: '{}'}})
            SET np.is_header = 'True', np.is_preferred_qualification = 'True';"""
        self.set_is_legal_notification1_cypher_str = """
            MATCH (np:NavigableParents {{navigable_parent: '{}'}})
            SET np.is_header = 'True', np.is_legal_notification = 'True';"""
        self.set_is_other1_cypher_str = """
            MATCH (np:NavigableParents {{navigable_parent: '{}'}})
            SET np.is_header = 'True', np.is_other = 'True';"""
        self.set_is_educational_requirement1_cypher_str = """
            MATCH (np:NavigableParents {{navigable_parent: '{}'}})
            SET np.is_header = 'True', np.is_educational_requirement = 'True';"""
        self.set_is_interview_procedure1_cypher_str = """
            MATCH (np:NavigableParents {{navigable_parent: '{}'}})
            SET np.is_header = 'True', np.is_interview_procedure = 'True';"""
        self.set_is_posting_date1_cypher_str = """
            MATCH (np:NavigableParents {{navigable_parent: '{}'}})
            SET np.is_header = 'True', np.is_posting_date = 'True';"""
        self.set_is_job_duration1_cypher_str = """
            MATCH (np:NavigableParents {{navigable_parent: '{}'}})
            SET np.is_header = 'True', np.is_job_duration = 'True';"""
        self.set_is_job_title1_cypher_str = """
            MATCH (np:NavigableParents {{navigable_parent: '{}'}})
            SET np.is_header = 'True', np.is_job_title = 'True';"""
        self.select_is_from_navigableparents_cypher_str = """
            MATCH (np:NavigableParents {{navigable_parent: '{}'}})
            RETURN
                np.is_header AS is_header,
                np.is_task_scope AS is_task_scope,
                np.is_minimum_qualification AS is_minimum_qualification,
                np.is_preferred_qualification AS is_preferred_qualification,
                np.is_legal_notification AS is_legal_notification,
                np.is_job_title AS is_job_title,
                np.is_office_location AS is_office_location,
                np.is_job_duration AS is_job_duration,
                np.is_supplemental_pay AS is_supplemental_pay,
                np.is_educational_requirement AS is_educational_requirement,
                np.is_interview_procedure AS is_interview_procedure,
                np.is_corporate_scope AS is_corporate_scope,
                np.is_posting_date AS is_posting_date,
                np.is_other AS is_other;"""
        self.select_navigable_parent_id_where_navigable_parent_cypher_str = """
            MATCH (np:NavigableParents {{navigable_parent: '{}'}})
            RETURN
                np.navigable_parent_id,
                np.is_minimum_qualification;"""
        self.set_secondary_column0_formatted_cypher_str = """
            MATCH (np:NavigableParents {{{}: 'True'}})
            WHERE NOT EXISTS(np.{})
            SET np.{} = 'False';"""
        self.set_is_qualification1_or_cypher_str = """
            MATCH (np:NavigableParents)
            WHERE
                np.is_minimum_qualification = 'True' OR
                np.is_preferred_qualification = 'True'
            SET np.is_qualification = 'True';"""


        # Header Tags Sequence CYPHER strings
        self.create_headertagsequence_table_cypher_str = """
            LOAD CSV WITH HEADERS FROM 'file:///HeaderTagSequence.csv' AS row
            WITH
                toInteger(row.header_tag_sequence_id) AS header_tag_sequence_id,
                toInteger(row.file_name_id) AS file_name_id,
                toInteger(row.header_tag_id) AS header_tag_id,
                toInteger(row.sequence_order) AS sequence_order
            MERGE (hts:HeaderTagSequence {header_tag_sequence_id: header_tag_sequence_id}) SET
                hts.file_name_id = file_name_id,
                hts.header_tag_id = header_tag_id,
                hts.sequence_order = sequence_order;"""
        self.insert_header_tag_sequence_str = """
            CREATE (HeaderTagSequence {{
                header_tag_sequence_id: '{}',
                file_name_id: '{}',
                header_tag_id: '{}',
                sequence_order: '{}'
                }});"""


        # Navigable Parents Sequence CYPHER strings
        self.create_navigableparentsequence_table_cypher_str = """
            LOAD CSV WITH HEADERS FROM 'file:///NavigableParentSequence.csv' AS row
            WITH
                toInteger(row.navigable_parent_sequence_id) AS navigable_parent_sequence_id,
                toInteger(row.file_name_id) AS file_name_id,
                toInteger(row.navigable_parent_id) AS navigable_parent_id,
                toInteger(row.sequence_order) AS sequence_order,
                toInteger(row.mrs_id) AS mrs_id
            MERGE (nps:NavigableParentSequence {navigable_parent_sequence_id: navigable_parent_sequence_id}) SET
                nps.file_name_id = file_name_id,
                nps.navigable_parent_id = navigable_parent_id,
                nps.sequence_order = sequence_order,
                nps.mrs_id = mrs_id;"""
        self.insert_navigableparentsequence_table_cypher_str = """
            CREATE (NavigableParentSequence {{
                navigable_parent_sequence_id: '{}',
                file_name_id: '{}',
                navigable_parent_id: '{}',
                sequence_order: '{}',
                mrs_id: '{}'
                }});"""
        self.select_filename_isheader_cypher_str = """
            MATCH (np:NavigableParents)-[ipo:IS_PART_OF]->(nps:NavigableParentSequence)-[ici:IS_CONTAINED_IN]->(fn:FileNames)
            RETURN
                np.navigable_parent AS navigable_parent,
                np.is_header AS is_header,
                nps.sequence_order AS sequence_order,
                fn.file_name AS file_name
            ORDER BY
                fn.file_name,
                nps.sequence_order;"""


        # Parts of Speech CYPHER strings
        self.create_table_partsofspeech_cypher_str = """
            LOAD CSV WITH HEADERS FROM 'file:///PartsOfSpeech.csv' AS row
            WITH
                toInteger(row.pos_id) AS pos_id,
                row.is_header AS is_header,
                row.is_task_scope AS is_task_scope,
                row.is_minimum_qualification AS is_minimum_qualification,
                row.is_preferred_qualification AS is_preferred_qualification,
                row.is_legal_notification AS is_legal_notification,
                row.is_job_title AS is_job_title,
                row.is_office_location AS is_office_location,
                row.is_job_duration AS is_job_duration,
                row.is_supplemental_pay AS is_supplemental_pay,
                row.is_educational_requirement AS is_educational_requirement,
                row.is_interview_procedure AS is_interview_procedure,
                row.is_corporate_scope AS is_corporate_scope,
                row.is_posting_date AS is_posting_date,
                row.is_other AS is_other,
                row.pos_symbol AS pos_symbol,
                row.pos_explanation AS pos_explanation
            MERGE (pos:PartsOfSpeech {pos_id: pos_id}) SET
                pos.is_header = is_header,
                pos.is_task_scope = is_task_scope,
                pos.is_minimum_qualification = is_minimum_qualification,
                pos.is_preferred_qualification = is_preferred_qualification,
                pos.is_legal_notification = is_legal_notification,
                pos.is_job_title = is_job_title,
                pos.is_office_location = is_office_location,
                pos.is_job_duration = is_job_duration,
                pos.is_supplemental_pay = is_supplemental_pay,
                pos.is_educational_requirement = is_educational_requirement,
                pos.is_interview_procedure = is_interview_procedure,
                pos.is_corporate_scope = is_corporate_scope,
                pos.is_posting_date = is_posting_date,
                pos.is_other = is_other,
                pos.pos_symbol = pos_symbol,
                pos.pos_explanation = pos_explanation;"""
        self.insert_into_partsofspeech_cypher_str = """
            CREATE ({}:PartsOfSpeech {{
                pos_id: '{}',
                pos_symbol: '{}',
                pos_explanation: '{}',
                is_header: '{}',
                is_task_scope: '{}',
                is_minimum_qualification: '{}',
                is_preferred_qualification: '{}',
                is_legal_notification: '{}',
                is_job_title: '{}',
                is_office_location: '{}',
                is_job_duration: '{}',
                is_supplemental_pay: '{}',
                is_educational_requirement: '{}',
                is_interview_procedure: '{}',
                is_corporate_scope: '{}',
                is_posting_date: '{}',
                is_other: '{}',
                is_qualification: '{}'
                }});"""


        # Minimum Requirements Section CYPHER strings
        self.create_table_minimumrequirementssection_cypher_str = """
            CREATE TABLE MinimumRequirementsSection(
                mrs_id: '{}',
                mrs_symbol: '{}',
                mrs_explanation: '{}',
            );"""
        self.insert_into_minimumrequirementssection_cypher_str = """
            CREATE ({}:MinimumRequirementsSection {{
                mrs_id: '{}',
                mrs_symbol: '{}',
                mrs_explanation: '{}',
                }});"""

        # CYPHER strings for Various Relationships
        self.create_relationship_filenames_headertagsequence_cypher_str = """
            MATCH (a:FileNames), (b:HeaderTagSequence)
               WHERE a.file_name_id = b.file_name_id
            CREATE (b)-[r: IS_CONTAINED_IN]->(a);"""
        self.create_relationship_filenames_navigableparentsequence_cypher_str = """
            MATCH (a:FileNames), (b:NavigableParentSequence)
               WHERE a.file_name_id = b.file_name_id
            MERGE (b)-[r: IS_CONTAINED_IN]->(a);"""
        self.create_relationship_navigableparents_navigableparentsequence_cypher_str = """
            MATCH (a:NavigableParents), (b:NavigableParentSequence)
               WHERE a.navigable_parent_id = b.navigable_parent_id
            MERGE (a)-[r: IS_PART_OF]->(b);"""
        self.create_relationship_headertags_headertagsequence_cypher_str = """
            MATCH (a:HeaderTags), (b:HeaderTagSequence)
               WHERE a.header_tag_id = b.header_tag_id
            CREATE (a)-[r: IS_PART_OF]->(b);"""
        self.create_relationship_headertags_navigableparents_cypher_str = """
            MATCH (a:HeaderTags), (b:NavigableParents)
               WHERE a.header_tag_id = b.header_tag_id
            CREATE (a)-[r: SUMMARIZES]->(b);"""
        self.create_relationship_minimumrequirementssection_navigableparentsequence_cypher_str = """
            MATCH (a:MinimumRequirementsSection), (b:NavigableParentSequence) 
               WHERE a.mrs_id = b.mrs_id
            CREATE (a)-[r: SUMMARIZES]->(b);"""

        # Various CYPHER strings
        self.SAVES_HTML_FOLDER = os.path.join(self.s.saves_folder, 'html')
        self.BACKSLASH = chr(92)
        self.SINGLE_QUOTE = chr(39)
        self.DOUBLE_QUOTE = chr(34)



    # Utility functions
    def do_cypher_tx(self, tx, cypher, verbose=False):
        results_list = tx.run(cypher.strip())
        values_list = []
        for record in results_list:
            values_list.append(dict(record.items()))

        return values_list
    def get_execution_results(self, cypher_str, verbose=False):
        if verbose:
            print(cypher_str)
        try:
            with self.driver.session() as session:
                row_objs_list = session.read_transaction(self.do_cypher_tx, cypher_str)
        except Exception as e:
            print(str(e).strip())
            print(cypher_str)
            row_objs_list = []

        return row_objs_list
    def clean_text(self, dirty_text):
        clean_text = dirty_text.replace(self.SINGLE_QUOTE, self.BACKSLASH + self.SINGLE_QUOTE)
        clean_text = clean_text.replace(self.BACKSLASH + self.BACKSLASH + self.SINGLE_QUOTE, self.BACKSLASH + self.SINGLE_QUOTE)
        clean_text = clean_text.replace(self.DOUBLE_QUOTE, self.BACKSLASH + self.DOUBLE_QUOTE)
        clean_text = clean_text.replace(self.BACKSLASH + self.BACKSLASH + self.DOUBLE_QUOTE, self.BACKSLASH + self.DOUBLE_QUOTE)

        return clean_text
    def convert_str_to_hash(self, unhashed_str):
        hash_object = hashlib.md5(unhashed_str.encode())

        # Format MD5 hash to hex
        md5_hash = hash_object.hexdigest()

        return(md5_hash)



    # File Names Table functions
    def create_filenames_table(self, verbose=False):
        cypher_str = """
            MATCH (fn:FileNames)
            DETACH DELETE fn;"""
        with self.driver.session() as session:
            session.write_transaction(self.do_cypher_tx, cypher_str)
            session.write_transaction(self.do_cypher_tx, self.create_filenames_table_cypher_str)
    def populate_filenames_table(self, verbose=False):
        files_list = sorted([fn for fn in os.listdir(self.SAVES_HTML_FOLDER) if fn.endswith('.html')])
        for file_name in files_list:
            cypher_str = f'''MERGE (fn:FileNames {{file_name: "{file_name}"}})'''
            with self.driver.session() as session:
                session.write_transaction(self.do_cypher_tx, cypher_str)
    def get_files_list(self, verbose=False):
        row_objs_list = self.get_execution_results(self.select_file_names_cypher_str, verbose=verbose)
        files_list = [row_obj['fn'].get('file_name', '').strip() for row_obj in row_objs_list]

        return files_list
    def get_filename_id(self, file_name, verbose=False):
        file_name = self.clean_text(file_name)
        cypher_str = f'''MERGE (fn:FileNames {{file_name: "{file_name}"}})
            RETURN fn.file_name_id;'''
        if verbose:
            print(cypher_str)
        with self.driver.session() as session:
            row_objs_list = session.write_transaction(self.do_cypher_tx, cypher_str)
        file_name_id = row_objs_list[0]['fn.file_name_id']
        if file_name_id is None:
            file_name_id = self.convert_str_to_hash(file_name)
            cypher_str = f'''
                MERGE (fn:FileNames {{file_name: "{file_name}"}}) SET
                    fn.file_name_id = "{file_name_id}"
                RETURN fn.file_name_id;'''
            if verbose:
                print(cypher_str)
            with self.driver.session() as session:
                row_objs_list = session.write_transaction(self.do_cypher_tx, cypher_str)
            file_name_id = row_objs_list[0]['fn.file_name_id']

        return file_name_id
    def get_all_filenames(self, verbose=False):
        cypher_str = f"""
            MATCH (fn:FileNames)
            RETURN
                fn.file_name_id,
                fn.file_name;"""
        row_objs_list = self.get_execution_results(cypher_str, verbose=verbose)

        return row_objs_list



    # Header Tags Table functions
    def create_headertags_table(self, verbose=False):
        cypher_str = """
            MATCH (ht:HeaderTags)
            DETACH DELETE ht;"""
        with self.driver.session() as session:
            session.write_transaction(self.do_cypher_tx, cypher_str)
            session.write_transaction(self.do_cypher_tx, self.create_headertags_table_cypher_str)
    def populate_headertags_table(self, verbose=False):
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
            cypher_str = self.insert_into_headertags_cypher_str.format(child_tag, child_tag, is_in_document_structure_elements_set, is_in_document_head_elements_set,
                                                                   is_in_document_body_elements_set, is_in_block_elements_set, is_in_basic_text_set,
                                                                   is_in_section_headings_set, is_in_lists_set, is_in_other_block_elements_set,
                                                                   is_in_inline_elements_set, is_in_anchor_set, is_in_phrase_elements_set,
                                                                   is_in_general_set, is_in_computer_phrase_elements_set, is_in_presentation_set,
                                                                   is_in_span_set, is_in_other_inline_elements_set, is_in_images_and_objects_set, is_in_forms_set,
                                                                   is_in_tables_set, is_in_frames_set, is_in_historic_elements_set, is_in_non_standard_elements_set)
            with self.driver.session() as session:
                session.write_transaction(self.do_cypher_tx, cypher_str)
    def get_headertag_id(self, header_tag, verbose=False):
        row_objs_list = self.get_execution_results(self.select_header_tag_id_where_header_tag_cypher_str.format(header_tag), verbose=False)
        header_tag_id = [row_obj.get('header_tag_id') for row_obj in row_objs_list][0]

        return header_tag_id
    def get_headertag(self, header_tag_id, verbose=False):
        row_objs_list = self.get_execution_results(self.select_header_tag_where_header_tag_id_cypher_str.format(header_tag_id), verbose=verbose)
        header_tag = [row_obj['fn'].get('header_tag') for row_obj in row_objs_list][0]

        return header_tag



    # Navigable Parents Table functions
    def create_navigableparents_table(self, verbose=False):
        cypher_str = """
            MATCH (np:NavigableParents)
            DETACH DELETE np;"""
        with self.driver.session() as session:
            session.write_transaction(self.do_cypher_tx, cypher_str)
            session.write_transaction(self.do_cypher_tx, self.create_navigableparents_table_cypher_str)
    def populate_navigableparents_table(self, verbose=False):
        files_list = self.get_files_list(verbose=verbose)
        navigable_parent_set = set()
        for file_name in files_list:
            child_strs_list = self.ha.get_child_strs_from_file(file_name.strip())
            for child_str in child_strs_list:
                navigable_parent_set.add(child_str)
        child_strs_list = sorted(navigable_parent_set)
        child_tags_list = self.ha.get_child_tags_list(child_strs_list)
        for i, (child_str, child_tag) in enumerate(zip(child_strs_list, child_tags_list)):
            header_tag_id = self.get_headertag_id(child_tag, verbose=verbose)
            child_str = self.clean_text(child_str)
            cypher_str = f"""
                MERGE (np:NavigableParents {{navigable_parent_id: '{i}', navigable_parent: '{child_str}', header_tag_id: '{header_tag_id}'}});"""
            with self.driver.session() as session:
                session.write_transaction(self.do_cypher_tx, cypher_str)

        # Set the Corporate Scope is_header
        corp_scope_headers_list = self.s.load_object('corp_scope_headers_list')
        for navigable_parent in corp_scope_headers_list:
            navigable_parent = self.clean_text(navigable_parent)
            cypher_str = self.set_is_corporate_scope1_cypher_str.format(navigable_parent)
            with self.driver.session() as session:
                session.write_transaction(self.do_cypher_tx, cypher_str)

        # Set the basic tags is_header
        self.ensure_navigableparent_is_header_from_dictionary(verbose=verbose)

        # Set the basic tags is_qual
        NAVIGABLE_PARENT_IS_QUAL_DICT = self.s.load_object('NAVIGABLE_PARENT_IS_QUAL_DICT')
        for navigable_parent, is_qualification in NAVIGABLE_PARENT_IS_QUAL_DICT.items():
            navigable_parent = self.clean_text(navigable_parent)
            if is_qualification:
                cypher_str = self.set_is_qualification1_cypher_str.format(navigable_parent)
                with self.driver.session() as session:
                    session.write_transaction(self.do_cypher_tx, cypher_str)
            else:
                cypher_str = self.set_is_qualification0_cypher_str.format(navigable_parent)
                with self.driver.session() as session:
                    session.write_transaction(self.do_cypher_tx, cypher_str)

        # Set the Task Scope is_header
        task_scope_headers_list = self.s.load_object('task_scope_headers_list')
        for navigable_parent in task_scope_headers_list:
            navigable_parent = self.clean_text(navigable_parent)
            cypher_str = self.set_is_task_scope1_cypher_str.format(navigable_parent)
            with self.driver.session() as session:
                session.write_transaction(self.do_cypher_tx, cypher_str)

        # Set the Office Location is_header
        office_loc_headers_list = self.s.load_object('office_loc_headers_list')
        for navigable_parent in office_loc_headers_list:
            navigable_parent = self.clean_text(navigable_parent)
            cypher_str = self.set_is_office_location1_cypher_str.format(navigable_parent)
            with self.driver.session() as session:
                session.write_transaction(self.do_cypher_tx, cypher_str)

        # Set the Minimum Quals is_header
        req_quals_headers_list = self.s.load_object('req_quals_headers_list')
        for navigable_parent in req_quals_headers_list:
            navigable_parent = self.clean_text(navigable_parent)
            cypher_str = self.set_is_minimum_qualification1_cypher_str.format(navigable_parent)
            with self.driver.session() as session:
                session.write_transaction(self.do_cypher_tx, cypher_str)
        if self.s.pickle_exists('O_RQ_DICT'):
            req_quals_nonheaders_dict = self.s.load_object('O_RQ_DICT')
            is_nonheader_minimum_qualification_cypher_str = """
                MATCH (np:NavigableParents {{navigable_parent: '{}'}})
                SET
                    np.is_header = 'False',
                    np.is_minimum_qualification = 'True',
                    np.is_qualification = 'True';"""
            for navigable_parent, is_nonheader_minimum_qualification in req_quals_nonheaders_dict.items():
                if is_nonheader_minimum_qualification:
                    navigable_parent = self.clean_text(navigable_parent)
                    cypher_str = is_nonheader_minimum_qualification_cypher_str.format(navigable_parent)
                    with self.driver.session() as session:
                        session.write_transaction(self.do_cypher_tx, cypher_str)
        if self.s.pickle_exists('H_RQ_DICT'):
            req_quals_headers_dict = self.s.load_object('H_RQ_DICT')
            is_header_minimum_qualification_cypher_str = """
                MATCH (np:NavigableParents {{navigable_parent: '{}'}})
                SET
                    np.is_header = 'True',
                    np.is_minimum_qualification = 'True',
                    np.is_qualification = 'True';"""
            for navigable_parent, is_header_minimum_qualification in req_quals_headers_dict.items():
                if is_header_minimum_qualification:
                    cypher_str = is_header_minimum_qualification_cypher_str.format(navigable_parent)
                    with self.driver.session() as session:
                        session.write_transaction(self.do_cypher_tx, cypher_str)

        # Set the Supplemental Pay is_header
        supp_pay_headers_list = self.s.load_object('supp_pay_headers_list')
        for navigable_parent in supp_pay_headers_list:
            navigable_parent = self.clean_text(navigable_parent)
            cypher_str = self.set_is_supplemental_pay1_cypher_str.format(navigable_parent)
            with self.driver.session() as session:
                session.write_transaction(self.do_cypher_tx, cypher_str)

        # Set the Supplemental Pay non-header
        supp_pay_nonheaders_list = self.s.load_object('supp_pay_nonheaders_list')
        for navigable_parent in supp_pay_nonheaders_list:
            navigable_parent = self.clean_text(navigable_parent)
            cypher_str = self.set_nonheader_is_supplemental_pay1_cypher_str.format(navigable_parent)
            with self.driver.session() as session:
                session.write_transaction(self.do_cypher_tx, cypher_str)

        # Set the Preferred Quals is_header
        preff_quals_headers_list = self.s.load_object('preff_quals_headers_list')
        for navigable_parent in preff_quals_headers_list:
            navigable_parent = self.clean_text(navigable_parent)
            cypher_str = self.set_is_preferred_qualification1_cypher_str.format(navigable_parent)
            with self.driver.session() as session:
                session.write_transaction(self.do_cypher_tx, cypher_str)

        # Set the Legal Notifications is_header
        legal_notifs_headers_list = self.s.load_object('legal_notifs_headers_list')
        for navigable_parent in legal_notifs_headers_list:
            navigable_parent = self.clean_text(navigable_parent)
            cypher_str = self.set_is_legal_notification1_cypher_str.format(navigable_parent)
            with self.driver.session() as session:
                session.write_transaction(self.do_cypher_tx, cypher_str)

        # Set the Other is_header
        other_headers_list = self.s.load_object('other_headers_list')
        for navigable_parent in other_headers_list:
            navigable_parent = self.clean_text(navigable_parent)
            cypher_str = self.set_is_other1_cypher_str.format(navigable_parent)
            with self.driver.session() as session:
                session.write_transaction(self.do_cypher_tx, cypher_str)

        # Set the Education Requirements is_header
        educ_reqs_headers_list = self.s.load_object('educ_reqs_headers_list')
        for navigable_parent in educ_reqs_headers_list:
            navigable_parent = self.clean_text(navigable_parent)
            cypher_str = self.set_is_educational_requirement1_cypher_str.format(navigable_parent)
            with self.driver.session() as session:
                session.write_transaction(self.do_cypher_tx, cypher_str)

        # Set the Interview Process is_header
        interv_proc_headers_list = self.s.load_object('interv_proc_headers_list')
        for navigable_parent in interv_proc_headers_list:
            navigable_parent = self.clean_text(navigable_parent)
            cypher_str = self.set_is_interview_procedure1_cypher_str.format(navigable_parent)
            with self.driver.session() as session:
                session.write_transaction(self.do_cypher_tx, cypher_str)

        # Set the Posting Date is_header
        post_date_headers_list = self.s.load_object('post_date_headers_list')
        for navigable_parent in post_date_headers_list:
            navigable_parent = self.clean_text(navigable_parent)
            cypher_str = self.set_is_posting_date1_cypher_str.format(navigable_parent)
            with self.driver.session() as session:
                session.write_transaction(self.do_cypher_tx, cypher_str)

        # Set the Job Duration is_header
        job_duration_headers_list = self.s.load_object('job_duration_headers_list')
        for navigable_parent in job_duration_headers_list:
            navigable_parent = self.clean_text(navigable_parent)
            cypher_str = self.set_is_job_duration1_cypher_str.format(navigable_parent)
            with self.driver.session() as session:
                session.write_transaction(self.do_cypher_tx, cypher_str)

        # Set the Job Title is_header
        job_title_headers_list = self.s.load_object('job_title_headers_list')
        for navigable_parent in job_title_headers_list:
            navigable_parent = self.clean_text(navigable_parent)
            cypher_str = self.set_is_job_title1_cypher_str.format(navigable_parent)
            with self.driver.session() as session:
                session.write_transaction(self.do_cypher_tx, cypher_str)

        # SET other subtypes as False; assume 0 rows affected if primary and secondary columns are the same
        subtypes_list = ['is_task_scope', 'is_minimum_qualification', 'is_preferred_qualification', 'is_legal_notification',
                         'is_job_title', 'is_office_location', 'is_job_duration', 'is_supplemental_pay',
                         'is_educational_requirement', 'is_interview_procedure', 'is_corporate_scope', 'is_posting_date',
                         'is_other']
        for primary_column in subtypes_list:
            for secondary_column in subtypes_list:
                cypher_str = self.set_secondary_column0_formatted_cypher_str.format(secondary_column, primary_column, secondary_column)
                if verbose:
                    print(cypher_str)
                with self.driver.session() as session:
                    session.write_transaction(self.do_cypher_tx, cypher_str)

        # Set the is_qualification if the other qual columns are set
        cypher_str = self.set_is_qualification1_or_cypher_str
        with self.driver.session() as session:
            session.write_transaction(self.do_cypher_tx, cypher_str)
    
    def get_navigableparent_id(self, navigable_parent, verbose=False):
        navigable_parent = self.clean_text(navigable_parent)
        cypher_str = f'''MERGE (np:NavigableParents {{navigable_parent: "{navigable_parent}"}})
            RETURN np.navigable_parent_id;'''
        if verbose:
            print(cypher_str)
        with self.driver.session() as session:
            row_objs_list = session.write_transaction(self.do_cypher_tx, cypher_str)
        navigable_parent_id = row_objs_list[0]['np.navigable_parent_id']
        if navigable_parent_id is None:
            navigable_parent_id = self.convert_str_to_hash(navigable_parent)
            cypher_str = f'''
                MERGE (np:NavigableParents {{navigable_parent: "{navigable_parent}"}}) SET
                    np.navigable_parent_id = "{navigable_parent_id}"
                RETURN np.navigable_parent_id;'''
            if verbose:
                print(cypher_str)
            with self.driver.session() as session:
                row_objs_list = session.write_transaction(self.do_cypher_tx, cypher_str)
            navigable_parent_id = row_objs_list[0]['np.navigable_parent_id']

        return navigable_parent_id



    # Header Tag Sequence Table functions
    def create_headertagsequence_table(self, verbose=False):
        cypher_str = """
            MATCH (hts:HeaderTagSequence)
            DETACH DELETE hts;"""
        with self.driver.session() as session:
            session.write_transaction(self.do_cypher_tx, cypher_str)
        cypher_str = self.create_headertagsequence_table_cypher_str
        with self.driver.session() as session:
            session.write_transaction(self.do_cypher_tx, cypher_str)
    def populate_headertagsequence_table(self, verbose=False):
        files_list = self.get_files_list(verbose=verbose)
        for file_name in files_list:
            file_name = file_name.strip()
            file_name_id = self.get_filename_id(file_name, verbose=verbose)
            child_strs_list = self.ha.get_child_strs_from_file(file_name)
            child_tags_list = self.ha.get_child_tags_list(child_strs_list)
            for sequence_order, header_tag in enumerate(child_tags_list):
                header_tag_id = self.get_headertag_id(header_tag, verbose=verbose)
                cypher_str = self.insert_header_tag_sequence_str.format(header_tag_id, sequence_order,
                                                                        file_name_id, header_tag_id, sequence_order)
                if verbose:
                    print(cypher_str)
                with self.driver.session() as session:
                    session.write_transaction(self.do_cypher_tx, cypher_str)
    def get_child_tags_list(self, file_name_id, verbose=False):

        # Get the child tags list for the file
        cypher_str = f"""
            MATCH (ht:HeaderTags) --> (hts:HeaderTagSequence {{file_name_id: {file_name_id}}})
            RETURN
                ht.header_tag,
                hts.sequence_order;"""
        row_objs_list = self.get_execution_results(cypher_str, verbose=verbose)
        df = pd.DataFrame(row_objs_list).sort_values('sequence_order')
        child_tags_list = [x.strip() for x in df.header_tag.tolist()]

        return child_tags_list
    def populate_header_tag_sequence_table(self, verbose=False):

        # Create the navigable html strings dataset
        header_tag_sequence_table_df = self.create_header_tag_sequence_table_dataframe(verbose=verbose)

        # Insert Dataframe into CYPHER Server:
        for row_index, row_series in header_tag_sequence_table_df.iterrows():
            cypher_str = self.insert_header_tag_sequence_str.format(row_series.header_tag,
                                                                    row_series.sequence_order, row_series.file_name.strip(),
                                                                    row_series.header_tag, row_series.sequence_order)
            if verbose:
                print(cypher_str)
            with self.driver.session() as session:
                session.write_transaction(self.do_cypher_tx, cypher_str)



    # Navigable Parent Sequence Table functions
    def create_navigableparentsequence_table(self, verbose=False):
        cypher_str = """
            MATCH (np:NavigableParentSequence)
            DETACH DELETE np;"""
        with self.driver.session() as session:
            session.write_transaction(self.do_cypher_tx, cypher_str)
            session.write_transaction(self.do_cypher_tx, self.create_navigableparentsequence_table_cypher_str)
    
    def populate_navigableparentsequence_table(self, verbose=False):
        files_list = self.get_files_list(verbose=verbose)
        counter = 0
        for file_name in files_list:
            file_name = file_name.strip()
            file_name_id = self.get_filename_id(file_name, verbose=verbose)
            child_strs_list = self.ha.get_child_strs_from_file(file_name)
            for sequence_order, navigable_parent in enumerate(child_strs_list):
                navigable_parent_id = self.get_navigableparent_id(navigable_parent, verbose=verbose)
                cypher_str = self.insert_navigableparentsequence_table_cypher_str.format(counter, file_name_id, navigable_parent_id, sequence_order, 0)
                if verbose:
                    print(cypher_str)
                with self.driver.session() as session:
                    session.write_transaction(self.do_cypher_tx, cypher_str)
                counter += 1
    
    def get_navigableparentsequence_id(self, file_name_id, navigable_parent_id, sequence_order, verbose=False):
        cypher_str = f'''MERGE (nps:NavigableParentSequence {{
                file_name_id: "{file_name_id}",
                navigable_parent_id: "{navigable_parent_id}",
                sequence_order: "{sequence_order}"}})
            RETURN nps.navigable_parent_sequence_id;'''
        if verbose:
            print(cypher_str)
        with self.driver.session() as session:
            row_objs_list = session.write_transaction(self.do_cypher_tx, cypher_str)
        navigable_parent_sequence_id = row_objs_list[0]['nps.navigable_parent_sequence_id']
        if navigable_parent_sequence_id is None:
            unhashed_str = str(file_name_id) + str(navigable_parent_id) + str(sequence_order)
            navigable_parent_sequence_id = self.convert_str_to_hash(unhashed_str)
            cypher_str = f'''
                MERGE (nps:NavigableParentSequence {{
                    file_name_id: "{file_name_id}",
                    navigable_parent_id: "{navigable_parent_id}",
                    sequence_order: "{sequence_order}"}}) SET
                    nps.navigable_parent_sequence_id = "{navigable_parent_sequence_id}"
                RETURN nps.navigable_parent_sequence_id;'''
            if verbose:
                print(cypher_str)
            with self.driver.session() as session:
                row_objs_list = session.write_transaction(self.do_cypher_tx, cypher_str)
            navigable_parent_sequence_id = row_objs_list[0]['nps.navigable_parent_sequence_id']
        
        return navigable_parent_sequence_id
    
    def ensure_navigableparentsequence_filename_relationship(self, file_name_id, verbose=False):
        cypher_str = f'''MATCH (fn:FileNames {{file_name_id: "{file_name_id}"}}), (nps:NavigableParentSequence {{file_name_id: "{file_name_id}"}})
            MERGE (nps)-[r:IS_CONTAINED_IN]->(fn);'''
        if verbose:
            print(cypher_str)
        with self.driver.session() as session:
            session.write_transaction(self.do_cypher_tx, cypher_str)
    
    def ensure_navigableparentsequence_navigableparent_relationship(self, navigable_parent_id, verbose=False):
        cypher_str = f'''MATCH
            (np:NavigableParents {{navigable_parent_id: "{navigable_parent_id}"}}),
            (nps:NavigableParentSequence {{navigable_parent_id: "{navigable_parent_id}"}})
            MERGE (np)-[r:IS_PART_OF]->(nps);'''
        if verbose:
            print(cypher_str)
        with self.driver.session() as session:
            session.write_transaction(self.do_cypher_tx, cypher_str)



    # Parts of Speech Table functions
    def create_partsofspeech_table(self, verbose=False):
        cypher_str = """
            MATCH (pos:PartsOfSpeech)
            DETACH DELETE pos;"""
        with self.driver.session() as session:
            session.write_transaction(self.do_cypher_tx, cypher_str)
            session.write_transaction(self.do_cypher_tx, self.create_table_partsofspeech_cypher_str)
    def populate_partsofspeech_table(self, verbose=False):
        pos_explanation_dict = self.s.load_object('pos_explanation_dict')
        count = 0
        for pos_symbol, pos_explanation in pos_explanation_dict.items():
            if pos_symbol.startswith('H-'):
                cypher_str = f"""MERGE (pos:PartsOfSpeech {{pos_id: '{count}', pos_symbol: '{pos_symbol}', pos_explanation: '{pos_explanation}'}})"""
                with self.driver.session() as session:
                    session.write_transaction(self.do_cypher_tx, cypher_str)
                count += 1
                pos_symbol = pos_symbol.replace('H-', 'O-')
                pos_explanation = pos_explanation.replace(' Header', ' Non-header')
                cypher_str = f"""MERGE (pos:PartsOfSpeech {{pos_id: '{count}', pos_symbol: '{pos_symbol}', pos_explanation: '{pos_explanation}'}})"""
                with self.driver.session() as session:
                    session.write_transaction(self.do_cypher_tx, cypher_str)
                count += 1
        cypher_str = """
            MATCH (pos:PartsOfSpeech)
            RETURN
                pos.pos_symbol AS pos_symbol,
                pos.pos_explanation AS pos_explanation;"""
        row_objs_list = self.get_execution_results(cypher_str, verbose=verbose)
        pos_df = pd.DataFrame(row_objs_list)
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
            cypher_str = f"""
                MERGE (pos:PartsOfSpeech {{pos_symbol: '{row_series.pos_symbol}'}}) SET
                    """
            set_list = [f'pos.{cn} = "{bool(cv)}"' for cn, cv in row_series.iteritems() if cn not in ['pos_symbol', 'pos_explanation']]
            cypher_str += """,
                    """.join(set_list)
            cypher_str += ';'
            if verbose:
                print(cypher_str)
            with self.driver.session() as session:
                session.write_transaction(self.do_cypher_tx, cypher_str)



    # Minimum Requirements Section Table functions
    def create_minimumrequirementssection_table(self, verbose=False):
        cypher_str = """
            MATCH (mrs:MinimumRequirementsSection)
            DETACH DELETE mrs;"""
        with self.driver.session() as session:
            session.write_transaction(self.do_cypher_tx, cypher_str)
            session.write_transaction(self.do_cypher_tx, self.create_table_minimumrequirementssection_cypher_str)
    def populate_minimumrequirementssection_table(self, verbose=False):
        mrs_explanation_dict = {'N': 'Not a part of the Minimum Requirements Section', 'B': 'Beginning of the Minimum Requirements Section',
                                'M': 'Middle of the Minimum Requirements Section', 'E': 'End of the Minimum Requirements Section'}
        for count, (mrs_symbol, mrs_explanation) in enumerate(mrs_explanation_dict.items()):
            cypher_str = self.insert_into_minimumrequirementssection_cypher_str.format(count, mrs_symbol, mrs_explanation)
            with self.driver.session() as session:
                session.write_transaction(self.do_cypher_tx, cypher_str)



    # Relationships functions
    def populate_relationships(self, verbose=False):
        cypher_str = """
            MATCH ()-[r]->()
            DETACH DELETE r;"""
        with self.driver.session() as session:
            session.write_transaction(self.do_cypher_tx, cypher_str)
            session.write_transaction(self.do_cypher_tx, self.create_relationship_filenames_headertagsequence_cypher_str)
            session.write_transaction(self.do_cypher_tx, self.create_relationship_filenames_navigableparentsequence_cypher_str)
            session.write_transaction(self.do_cypher_tx, self.create_relationship_headertags_headertagsequence_cypher_str)
            session.write_transaction(self.do_cypher_tx, self.create_relationship_headertags_navigableparents_cypher_str)
            session.write_transaction(self.do_cypher_tx, self.create_relationship_minimumrequirementssection_navigableparentsequence_cypher_str)
            for a in ['True', 'False']:
                for b in ['is_task_scope', 'is_minimum_qualification', 'is_preferred_qualification', 'is_legal_notification', 'is_job_title',
                          'is_office_location', 'is_job_duration', 'is_supplemental_pay', 'is_educational_requirement', 'is_interview_procedure',
                          'is_corporate_scope', 'is_posting_date', 'is_other']:
                    cypher_str = f"""
                        MATCH (pos:PartsOfSpeech {{is_header: '{a}', {b}: 'True'}}), (np:NavigableParents {{is_header: '{a}', {b}: 'True'}})
                        CREATE (pos)-[r: SUMMARIZES]->(np);"""
                    if verbose:
                        print(cypher_str)
                    session.write_transaction(self.do_cypher_tx, cypher_str)


    def get_is_header_list(self, child_strs_list, verbose=False):
        is_header_list = []
        for navigable_parent in child_strs_list:
            navigable_parent = self.clean_text(navigable_parent)
            cypher_str = self.select_is_from_navigableparents_cypher_str.format(navigable_parent)
            row_objs_list = self.get_execution_results(cypher_str, verbose=verbose)
            is_header = pd.DataFrame(row_objs_list).is_header.squeeze()
            is_header_list.append(is_header)

        return is_header_list



    def get_child_strs_from_file(self, file_name, verbose=False):
        cypher_str = self.select_navigable_parent_by_file_name_cypher_str.format(file_name.strip())
        row_objs_list = self.get_execution_results(cypher_str, verbose=verbose)
        child_strs_list = [row_obj.get('np.navigable_parent') for row_obj in row_objs_list]

        return child_strs_list



    def get_child_tags_list(self, child_strs_list, verbose=False):
        child_tags_list = []
        for navigable_parent in child_strs_list:
            navigable_parent = self.clean_text(navigable_parent)
            row_objs_list = self.get_execution_results(self.select_header_tag_where_navigable_parent_cypher_str.format(navigable_parent), verbose=verbose)
            header_tag = [row_obj['fn'].get('header_tag') for row_obj in row_objs_list][0]
            child_tags_list.append(header_tag)

        return child_tags_list



    def get_feature_dict_list(self, child_tags_list, child_strs_list, verbose=False):
        feature_dict_list = []
        import numpy as np
        for tag, child_str in zip(child_tags_list, child_strs_list):
            feature_dict = {}
            feature_dict['initial_tag'] = tag
            child_str = self.clean_text(child_str)
            cypher_str = self.select_is_from_navigableparents_cypher_str.format(child_str)
            if verbose:
                print(cypher_str)
            row_objs_list = self.get_execution_results(cypher_str, verbose=verbose)
            params_dict = row_objs_list[0]
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



    def append_parts_of_speech_list(self, navigable_parent, pos_list=[], verbose=False):
        navigable_parent = self.clean_text(navigable_parent)
        row_objs_list = self.get_execution_results(self.select_is_from_navigableparents_cypher_str.format(navigable_parent, verbose=verbose))
        params_dict = pd.DataFrame(row_objs_list).squeeze().to_dict()
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



    def build_child_strs_list_dictionary(self, verbose=False):
        self.CHILD_STRS_LIST_DICT = {}
        def f(df):
            mask_series = df.is_header.isnull()

            return df[mask_series].shape[0]
        isheaders_df = pd.DataFrame(self.get_execution_results(self.select_filename_isheader_cypher_str, verbose=verbose))
        isheaders_series = isheaders_df.groupby('file_name').apply(f).sort_values()
        files_list = isheaders_series[isheaders_series==0].index.tolist()
        for file_name in files_list:
            file_name = file_name.strip()
            child_strs_list = self.get_child_strs_from_file(file_name)
            if file_name not in self.CHILD_STRS_LIST_DICT:
                self.CHILD_STRS_LIST_DICT[file_name] = child_strs_list
                self.s.store_objects(CHILD_STRS_LIST_DICT=self.CHILD_STRS_LIST_DICT, verbose=False)



    def create_header_pattern_dictionary(self, verbose=False):

        # Get the files in the child strings list
        row_objs_list = self.get_all_filenames(verbose=verbose)
        filenames_df = pd.DataFrame(row_objs_list)
        CHILD_STRS_LIST_DICT = self.s.load_object('CHILD_STRS_LIST_DICT')
        mask_series = filenames_df.file_name.isin(list(CHILD_STRS_LIST_DICT.keys()))

        # Initialize and populate the header pattern dictionary
        HEADER_PATTERN_DICT = {}
        for row_index, row_series in filenames_df[mask_series].iterrows():
            file_name_id = row_series.file_name_id
            file_name = row_series.file_name.strip()

            # Get the child strings list for the file
            cypher_str = """
                MATCH (nps:NavigableParentSequence {{file_name_id: {}}})<--(np:NavigableParents)
                RETURN
                    np.navigable_parent,
                    nps.sequence_order;""".format(file_name_id)
            child_strs_list = pd.DataFrame(self.get_execution_results(cypher_str, verbose=verbose)).navigable_parent.tolist()

            # Get the child tags list for the file
            child_tags_list = self.get_child_tags_list(file_name_id, verbose=verbose)

            # Assume the is_header feature for each item in the sequence is not None
            item_sequence = self.get_feature_dict_list(child_tags_list, child_strs_list)

            HEADER_PATTERN_DICT[file_name] = item_sequence
            self.s.store_objects(HEADER_PATTERN_DICT=HEADER_PATTERN_DICT, verbose=verbose)


    def find_basic_quals_section(self, child_strs_list, hc=None, ea=None, verbose=False):
        if hc is None:
            hc = html_analysis.HeaderCategories()
        if ea is None:
            ea = html_analysis.ElementAnalysis()
        child_tags_list = self.get_child_tags_list(child_strs_list)
        is_header_list = self.get_is_header_list(child_strs_list)
        feature_dict_list = self.get_feature_dict_list(child_tags_list, child_strs_list, verbose=False)
        feature_tuple_list = [hc.get_feature_tuple(feature_dict) for feature_dict in feature_dict_list]

        crf = html_analysis.CrfUtilities(ha=None, hc=hc, cu=self, verbose=verbose)
        crf_list = crf.CRF.predict_single(crf.sent2features(feature_tuple_list))
        pos_list = []
        for pos, feature_tuple, is_header in zip(crf_list, feature_tuple_list, is_header_list):
            navigable_parent = feature_tuple[1]
            if is_header:
                pos_list = self.append_parts_of_speech_list(navigable_parent, pos_list=[])
            else:
                pos_list.append(pos)
        consecutives_list = []
        from itertools import groupby
        for k, v in groupby(pos_list):
            consecutives_list.append((k, len(list(v))))

        return consecutives_list, pos_list



    def create_navigableparent_is_qual_dictionary(self, verbose=False):

        # Get the already-qualified html strings
        cypher_str = """
            MATCH (np:NavigableParents)
            WHERE EXISTS(np.is_qualification)
            RETURN
                np.navigable_parent,
                np.is_qualification;"""
        is_qualification_df = pd.DataFrame(self.get_execution_results(cypher_str, verbose=verbose))
        is_qualification_df.is_qualification = is_qualification_df.is_qualification.astype('bool')

        # Initialize and populate the header pattern dictionary
        NAVIGABLE_PARENT_IS_QUAL_DICT = {}
        for row_index, row_series in is_qualification_df.iterrows():
            is_fit = row_series.is_qualification
            qualification_str = row_series.navigable_parent

            NAVIGABLE_PARENT_IS_QUAL_DICT[qualification_str] = is_fit
            self.s.store_objects(NAVIGABLE_PARENT_IS_QUAL_DICT=NAVIGABLE_PARENT_IS_QUAL_DICT, verbose=verbose)



    def create_navigableparent_is_header_dictionary(self, verbose=False):

        # Get the already-headered html strings
        cypher_str = """
            MATCH (np:NavigableParents)
            WHERE EXISTS(np.is_header)
            RETURN
                np.navigable_parent,
                np.is_header;"""
        is_header_df = pd.DataFrame(self.get_execution_results(cypher_str, verbose=verbose))
        is_header_df.is_header = is_header_df.is_header.astype('bool')

        # Initialize and populate the navigable parent is header dictionary
        NAVIGABLE_PARENT_IS_HEADER_DICT = {}
        for row_index, row_series in is_header_df.iterrows():
            is_header = row_series.is_header
            child_str = row_series.navigable_parent

            NAVIGABLE_PARENT_IS_HEADER_DICT[child_str] = is_header
            self.s.store_objects(NAVIGABLE_PARENT_IS_HEADER_DICT=NAVIGABLE_PARENT_IS_HEADER_DICT, verbose=verbose)



    def ensure_navigableparent_is_header_from_dictionary(self, verbose=False):
        NAVIGABLE_PARENT_IS_HEADER_DICT = self.s.load_object('NAVIGABLE_PARENT_IS_HEADER_DICT')
        for navigable_parent, is_header in NAVIGABLE_PARENT_IS_HEADER_DICT.items():
            navigable_parent = self.clean_text(navigable_parent)
            if is_header:
                cypher_str = self.set_is_header1_cypher_str.format(navigable_parent)
            else:
                cypher_str = self.set_is_header0_cypher_str.format(navigable_parent)
            if verbose:
                print(cypher_str)
            with self.driver.session() as session:
                session.write_transaction(self.do_cypher_tx, cypher_str)



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



    def get_filenames_by_starting_sequence(self, sequence_list=[], verbose=False):

        # https://stackoverflow.com/questions/5160742/how-to-store-and-search-for-a-sequence-in-a-rdbms
        filenames_list = []
        if len(sequence_list):
            if verbose:
                print(self.create_query_table_cypher_str)
            row_objs_list = self.get_execution_results(self.create_query_table_cypher_str, verbose=verbose)
            try:
                row_tuples_list = [tuple(row_obj) for row_obj in row_objs_list]
            except:
                row_tuples_list = []
            if verbose:
                print(row_tuples_list)

            # Insert sequence list into CYPHER Server:
            for sequence_order, header_tag in enumerate(sequence_list):
                if verbose:
                    print(self.insert_query_rows_cypher_str.format(header_tag, sequence_order))
                try:
                    row_objs_list = self.get_execution_results(self.insert_query_rows_cypher_str, header_tag, sequence_order, verbose=verbose)
                except Exception as e:
                    print(str(e).strip())
                    print(self.insert_query_rows_cypher_str.format(header_tag, sequence_order))
                    break
            if verbose:
                print(self.select_query_cypher_str)
            row_objs_list = self.get_execution_results(self.select_query_cypher_str, verbose=verbose)
            try:
                row_tuples_list = [tuple(row_obj) for row_obj in row_objs_list]
            except:
                row_tuples_list = []
            if verbose:
                print(row_tuples_list)
            filenames_list = [filename_tuple[0] for filename_tuple in row_tuples_list]

        return filenames_list



    def get_filenames_by_sequence(self, sequence_list=[], verbose=False):
        all_filenames_list = []
        if len(sequence_list):
            start_num = 'False'
            header_tag_sequence_table_df = self.create_header_tag_sequence_table_dataframe()
            max_num = header_tag_sequence_table_df.sequence_order.max() - len(sequence_list) + 1
            while start_num < max_num:

                # Recreate temp table
                if verbose:
                    print(self.create_query_table_cypher_str)
                row_objs_list = self.get_execution_results(self.create_query_table_cypher_str, verbose=verbose)
                try:
                    row_tuples_list = [tuple(row_obj) for row_obj in row_objs_list]
                except:
                    row_tuples_list = []
                if verbose:
                    print(row_tuples_list)

                # Insert sequence list into temp table
                for sequence_order, header_tag in enumerate(sequence_list):
                    if verbose:
                        print(self.insert_query_rows_cypher_str.format(header_tag, start_num + sequence_order))
                    try:
                        row_objs_list = self.get_execution_results(self.insert_query_rows_cypher_str, header_tag, start_num + sequence_order, verbose=verbose)
                    except Exception as e:
                        print(str(e).strip())
                        print(self.insert_query_rows_cypher_str.format(header_tag, start_num + sequence_order))
                        break
                    try:
                        row_tuples_list = [tuple(row_obj) for row_obj in row_objs_list]
                    except:
                        row_tuples_list = []

                # Find sequence list by file name
                if verbose:
                    print(self.select_query_cypher_str)
                row_objs_list = self.get_execution_results(self.select_query_cypher_str, verbose=verbose)
                try:
                    row_tuples_list = [tuple(row_obj) for row_obj in row_objs_list]
                except:
                    row_tuples_list = []
                if verbose:
                    print(row_tuples_list)
                filenames_list = [filename_tuple[0] for filename_tuple in row_tuples_list]

                # Add these file names to the list
                all_filenames_list.extend(filenames_list)

                start_num += 1

        return list(set(all_filenames_list))


    def create_task_scope_pickle(self, verbose=False):

        # Get the task scope headers
        cypher_str = """
            MATCH (np:NavigableParents)
            WHERE EXISTS(np.is_task_scope)
            RETURN
                np.navigable_parent,
                np.is_task_scope;"""
        task_scope_df = pd.DataFrame(self.get_execution_results(cypher_str, verbose=verbose))
        task_scope_df.is_task_scope = task_scope_df.is_task_scope.astype('bool')

        # Initialize and populate the task scope list
        TASK_SCOPE_HEADERS_LIST = task_scope_df[task_scope_df.is_task_scope].navigable_parent.tolist()
        self.s.store_objects(TASK_SCOPE_HEADERS_LIST=TASK_SCOPE_HEADERS_LIST, verbose=verbose)


    def create_req_quals_pickle(self, verbose=False):

        # Get the req quals headers
        cypher_str = """
            MATCH (np:NavigableParents)
            WHERE EXISTS(np.is_minimum_qualification)
            RETURN
                np.navigable_parent,
                np.is_minimum_qualification;"""
        req_quals_df = pd.DataFrame(self.get_execution_results(cypher_str, verbose=verbose))
        req_quals_df.is_minimum_qualification = req_quals_df.is_minimum_qualification.astype('bool')

        # Initialize and populate the req quals list
        REQ_QUALS_HEADERS_LIST = req_quals_df[req_quals_df.is_minimum_qualification].navigable_parent.tolist()
        self.s.store_objects(REQ_QUALS_HEADERS_LIST=REQ_QUALS_HEADERS_LIST, verbose=verbose)


    def create_o_rq_pickle(self, verbose=False):

        # Get the req quals non-headers
        cypher_str = """
            MATCH (np:NavigableParents)
            WHERE
                EXISTS(np.is_minimum_qualification) AND
                EXISTS(np.is_header)
            RETURN
                np.navigable_parent,
                np.is_minimum_qualification,
                np.is_header;"""
        req_quals_df = pd.DataFrame(self.get_execution_results(cypher_str, verbose=verbose))
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


    def create_h_rq_pickle(self, verbose=False):

        # Get the req quals headers
        cypher_str = """
            MATCH (np:NavigableParents)
            WHERE
                EXISTS(np.is_minimum_qualification) AND
                EXISTS(np.is_header)
            RETURN
                np.navigable_parent,
                np.is_minimum_qualification,
                np.is_header;"""
        req_quals_df = pd.DataFrame(self.get_execution_results(cypher_str, verbose=verbose))
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


    def create_preff_quals_pickle(self, verbose=False):

        # Get the preff quals headers
        cypher_str = """
            MATCH (np:NavigableParents)
            WHERE EXISTS(np.is_preferred_qualification)
            RETURN
                np.navigable_parent,
                np.is_preferred_qualification;"""
        preff_quals_df = pd.DataFrame(self.get_execution_results(cypher_str, verbose=verbose))
        preff_quals_df.is_preferred_qualification = preff_quals_df.is_preferred_qualification.astype('bool')

        # Initialize and populate the preff quals list
        PREFF_QUALS_HEADERS_LIST = preff_quals_df[preff_quals_df.is_preferred_qualification].navigable_parent.tolist()
        self.s.store_objects(PREFF_QUALS_HEADERS_LIST=PREFF_QUALS_HEADERS_LIST, verbose=verbose)


    def create_legal_notifs_pickle(self, verbose=False):

        # Get the legal notifs headers
        cypher_str = """
            MATCH (np:NavigableParents)
            WHERE EXISTS(np.is_legal_notification)
            RETURN
                np.navigable_parent,
                np.is_legal_notification;"""
        legal_notifs_df = pd.DataFrame(self.get_execution_results(cypher_str, verbose=verbose))
        legal_notifs_df.is_legal_notification = legal_notifs_df.is_legal_notification.astype('bool')

        # Initialize and populate the legal notifs list
        LEGAL_NOTIFS_HEADERS_LIST = legal_notifs_df[legal_notifs_df.is_legal_notification].navigable_parent.tolist()
        self.s.store_objects(LEGAL_NOTIFS_HEADERS_LIST=LEGAL_NOTIFS_HEADERS_LIST, verbose=verbose)


    def create_job_title_pickle(self, verbose=False):

        # Get the job title headers
        cypher_str = """
            MATCH (np:NavigableParents)
            WHERE EXISTS(np.is_job_title)
            RETURN
                np.navigable_parent,
                np.is_job_title;"""
        job_title_df = pd.DataFrame(self.get_execution_results(cypher_str, verbose=verbose))
        job_title_df.is_job_title = job_title_df.is_job_title.astype('bool')

        # Initialize and populate the job title list
        JOB_TITLE_HEADERS_LIST = job_title_df[job_title_df.is_job_title].navigable_parent.tolist()
        self.s.store_objects(JOB_TITLE_HEADERS_LIST=JOB_TITLE_HEADERS_LIST, verbose=verbose)


    def create_office_loc_pickle(self, verbose=False):

        # Get the office loc headers
        cypher_str = """
            MATCH (np:NavigableParents)
            WHERE EXISTS(np.is_office_location)
            RETURN
                np.navigable_parent,
                np.is_office_location;"""
        office_loc_df = pd.DataFrame(self.get_execution_results(cypher_str, verbose=verbose))
        office_loc_df.is_office_location = office_loc_df.is_office_location.astype('bool')

        # Initialize and populate the office location list
        OFFICE_LOC_HEADERS_LIST = office_loc_df[office_loc_df.is_office_location].navigable_parent.tolist()
        self.s.store_objects(OFFICE_LOC_HEADERS_LIST=OFFICE_LOC_HEADERS_LIST, verbose=verbose)


    def create_job_duration_pickle(self, verbose=False):

        # Get the job duration headers
        cypher_str = """
            MATCH (np:NavigableParents)
            WHERE EXISTS(np.is_job_duration)
            RETURN
                np.navigable_parent,
                np.is_job_duration;"""
        job_duration_df = pd.DataFrame(self.get_execution_results(cypher_str, verbose=verbose))
        job_duration_df.is_job_duration = job_duration_df.is_job_duration.astype('bool')

        # Initialize and populate the job duration list
        JOB_DURATION_HEADERS_LIST = job_duration_df[job_duration_df.is_job_duration].navigable_parent.tolist()
        self.s.store_objects(JOB_DURATION_HEADERS_LIST=JOB_DURATION_HEADERS_LIST, verbose=verbose)


    def create_supp_pay_pickle(self, verbose=False):

        # Get the supp pay headers
        cypher_str = """
            MATCH (np:NavigableParents)
            WHERE EXISTS(np.is_supplemental_pay)
            RETURN
                np.navigable_parent,
                np.is_supplemental_pay;"""
        supp_pay_df = pd.DataFrame(self.get_execution_results(cypher_str, verbose=verbose))
        supp_pay_df.is_supplemental_pay = supp_pay_df.is_supplemental_pay.astype('bool')

        # Initialize and populate the supplemental pay list
        SUPP_PAY_HEADERS_LIST = supp_pay_df[supp_pay_df.is_supplemental_pay].navigable_parent.tolist()
        self.s.store_objects(SUPP_PAY_HEADERS_LIST=SUPP_PAY_HEADERS_LIST, verbose=verbose)


    def create_educ_reqs_pickle(self, verbose=False):

        # Get the educ reqs headers
        cypher_str = """
            MATCH (np:NavigableParents)
            WHERE EXISTS(np.is_educational_requirement)
            RETURN
                np.navigable_parent,
                np.is_educational_requirement;"""
        educ_reqs_df = pd.DataFrame(self.get_execution_results(cypher_str, verbose=verbose))
        educ_reqs_df.is_educational_requirement = educ_reqs_df.is_educational_requirement.astype('bool')

        # Initialize and populate the educational requirements list
        EDUC_REQS_HEADERS_LIST = educ_reqs_df[educ_reqs_df.is_educational_requirement].navigable_parent.tolist()
        self.s.store_objects(EDUC_REQS_HEADERS_LIST=EDUC_REQS_HEADERS_LIST, verbose=verbose)


    def create_interv_proc_pickle(self, verbose=False):

        # Get the interv proc headers
        cypher_str = """
            MATCH (np:NavigableParents)
            WHERE EXISTS(np.is_interview_procedure)
            RETURN
                np.navigable_parent,
                np.is_interview_procedure;"""
        interv_proc_df = pd.DataFrame(self.get_execution_results(cypher_str, verbose=verbose))
        interv_proc_df.is_interview_procedure = interv_proc_df.is_interview_procedure.astype('bool')

        # Initialize and populate the interview procedure list
        INTERV_PROC_HEADERS_LIST = interv_proc_df[interv_proc_df.is_interview_procedure].navigable_parent.tolist()
        self.s.store_objects(INTERV_PROC_HEADERS_LIST=INTERV_PROC_HEADERS_LIST, verbose=verbose)


    def create_corp_scope_pickle(self, verbose=False):

        # Get the corp scope headers
        cypher_str = """
            MATCH (np:NavigableParents)
            WHERE EXISTS(np.is_corporate_scope)
            RETURN
                np.navigable_parent,
                np.is_corporate_scope;"""
        corp_scope_df = pd.DataFrame(self.get_execution_results(cypher_str, verbose=verbose))
        corp_scope_df.is_corporate_scope = corp_scope_df.is_corporate_scope.astype('bool')

        # Initialize and populate the corporate scope list
        CORP_SCOPE_HEADERS_LIST = corp_scope_df[corp_scope_df.is_corporate_scope].navigable_parent.tolist()
        self.s.store_objects(CORP_SCOPE_HEADERS_LIST=CORP_SCOPE_HEADERS_LIST, verbose=verbose)


    def create_post_date_pickle(self, verbose=False):

        # Get the post date headers
        cypher_str = """
            MATCH (np:NavigableParents)
            WHERE EXISTS(np.is_posting_date)
            RETURN
                np.navigable_parent,
                np.is_posting_date;"""
        post_date_df = pd.DataFrame(self.get_execution_results(cypher_str, verbose=verbose))
        post_date_df.is_posting_date = post_date_df.is_posting_date.astype('bool')

        # Initialize and populate the posting date list
        POST_DATE_HEADERS_LIST = post_date_df[post_date_df.is_posting_date].navigable_parent.tolist()
        self.s.store_objects(POST_DATE_HEADERS_LIST=POST_DATE_HEADERS_LIST, verbose=verbose)


    def create_other_pickle(self, verbose=False):

        # Get the other headers
        cypher_str = """
            MATCH (np:NavigableParents)
            WHERE EXISTS(np.is_other)
            RETURN
                np.navigable_parent,
                np.is_other;"""
        other_df = pd.DataFrame(self.get_execution_results(cypher_str, verbose=verbose))
        other_df.is_other = other_df.is_other.astype('bool')

        # Initialize and populate the other list
        OTHER_HEADERS_LIST = other_df[other_df.is_other].navigable_parent.tolist()
        self.s.store_objects(OTHER_HEADERS_LIST=OTHER_HEADERS_LIST, verbose=verbose)