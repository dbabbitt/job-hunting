
// Find the navigable parents that are chained to another (and what POS symbol they are tagged with)
MATCH (pos1:PartsOfSpeech)-[r1:SUMMARIZES]->(np1:NavigableParents)-[r2:NEXT]->(np2:NavigableParents)
RETURN
    pos1,
    r1,
    np1,
    r2
LIMIT 10;

// Find the navigable parents that are "about the job" and what POS symbol they are tagged with
MATCH (pos:PartsOfSpeech)-[r:SUMMARIZES]->(np:NavigableParents)
WHERE
    np.navigable_parent CONTAINS "About the job"
RETURN
    pos.pos_symbol AS pos_symbol,
    np.navigable_parent AS navigable_parent;

// Get the HTML bits of a specific file
MATCH (np1:NavigableParents)-[r:NEXT]->(np2:NavigableParents)
WHERE r.file_name = "654489b978b139f8_Sr_Engineers_SDET_Bellevue_WA_98006_Indeed_com.html"
RETURN
    LEFT(np1.navigable_parent, 50) AS navigable_parent1,
    np1.is_header AS is_header1,
    np1.is_task_scope AS is_task_scope1,
    np1.is_minimum_qualification AS is_minimum_qualification1,
    np1.is_preferred_qualification AS is_preferred_qualification1,
    np1.is_educational_requirement AS is_educational_requirement1,
    np1.is_legal_notification AS is_legal_notification1,
    np1.is_other AS is_other1,
    np1.is_corporate_scope AS is_corporate_scope1,
    np1.is_job_title AS is_job_title1,
    np1.is_office_location AS is_office_location1,
    np1.is_job_duration AS is_job_duration1,
    np1.is_supplemental_pay AS is_supplemental_pay1,
    np1.is_interview_procedure AS is_interview_procedure1,
    np1.is_posting_date AS is_posting_date1
ORDER BY r.sequence_order;

// Get the file names of HTML strings that are Job Titles
MATCH (np1:NavigableParents)-[r:NEXT]->(np2:NavigableParents)
WHERE
    ((np1.is_header = false) AND (np1.is_job_title = true))
    OR ((np2.is_header = false) AND (np2.is_job_title = true))
RETURN
    r.file_name,
    LEFT(np1.navigable_parent, 50) AS left_navigable_parent,
    LEFT(np2.navigable_parent, 50) AS right_navigable_parent;

// Export all nodes with the :NavigableParents label where the is_job_title property is true to the file jobtitles.csv
MATCH (np:NavigableParents)
WHERE (np.is_job_title = true)
WITH collect(np) AS jobtitles
CALL apoc.export.csv.data(jobtitles, [], "apoc_export_csv_data_jobtitles.csv", {})
YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data
RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data;

// Get all node types that have the is_job_title property defined
CALL db.schema.nodeTypeProperties() YIELD nodeType, propertyName
WHERE propertyName = "is_job_title"
RETURN DISTINCT nodeType;

MATCH (np:NavigableParents)
WHERE (np.is_job_title = true)
RETURN
    LEFT(np.navigable_parent, 50) AS navigable_parent_head;

MATCH (np:NavigableParents)
WHERE (np.navigable_parent STARTS WITH "<li>7 - ")
SET
    np.is_header = false,
    np.is_task_scope = false,
    np.is_minimum_qualification = true,
    np.is_preferred_qualification = false,
    np.is_educational_requirement = false,
    np.is_legal_notification = false,
    np.is_other = false,
    np.is_corporate_scope = false,
    np.is_job_title = false,
    np.is_office_location = false,
    np.is_job_duration = false,
    np.is_supplemental_pay = false,
    np.is_interview_procedure = false,
    np.is_posting_date = false
RETURN COUNT(*);

MATCH (np:NavigableParents)
WHERE (np.is_qualification IS NOT NULL)
RETURN count(*);

MATCH (np:NavigableParents)
WHERE np.is_qualification = true
RETURN np.navigable_parent;

MATCH (np:NavigableParents {navigable_parent: "<li>GIS: 3 years (Required)</li>"})
SET np.is_minimum_qualification = true;

MATCH (np:NavigableParents {navigable_parent: "<li>Python: 10 years (Preferred)</li>"})
SET np.is_preferred_qualification = true;

MATCH (np:NavigableParents {navigable_parent: "Hope you are doing safe and fine amidst pandemic!"})
SET np.is_qualification = NULL;

// Get all the HQs
MATCH (np:NavigableParents)
WHERE (
    np.is_qualification = true
    AND ((np.is_minimum_qualification IS NULL) OR (np.is_minimum_qualification = false))
    AND ((np.is_preferred_qualification IS NULL) OR (np.is_preferred_qualification = false))
    )
RETURN np.navigable_parent;

MATCH (np:NavigableParents {navigable_parent: "<b>based products and applications.</b>"})
SET np.is_qualification = NULL;

MATCH (np:NavigableParents {navigable_parent: "<b>Have deep finance experience.</b>"})-[n:NEXT]->(:NavigableParents)
RETURN n
ORDER BY n.sequence_order;

// Get the edge and node counts for each unexamined file, tag-agnostic
MATCH (np:NavigableParents)-[r:NEXT]->(:NavigableParents)
WHERE
    np.is_header IS NULL
    AND np.is_task_scope IS NULL
    AND np.is_minimum_qualification IS NULL
    AND np.is_preferred_qualification IS NULL
    AND np.is_educational_requirement IS NULL
    AND np.is_legal_notification IS NULL
    AND np.is_other IS NULL
    AND np.is_corporate_scope IS NULL
    AND np.is_job_title IS NULL
    AND np.is_office_location IS NULL
    AND np.is_job_duration IS NULL
    AND np.is_supplemental_pay IS NULL
    AND np.is_interview_procedure IS NULL
    AND np.is_posting_date IS NULL
WITH
    r.file_name AS file_name,
    COUNT(r) AS edge_count,
    COUNT(np) AS np_count
RETURN np_count, edge_count, file_name
ORDER BY edge_count DESC;

MATCH (:NavigableParents)-[r:NEXT]->(:NavigableParents)
WHERE r.file_name = "212ea9dc068b2bf3_Data_Engineer_I_New_York_NY_Indeed_com.html"
DELETE r;

MATCH (np1:NavigableParents)-[r:NEXT]->(np2:NavigableParents)
WITH np1, np2, collect(r) AS nexts
WHERE size(nexts) > 1
RETURN np1, np2, nexts
LIMIT 1;

MATCH (ht:HeaderTags)-[r:SUMMARIZES]->(np:NavigableParents)
WITH ht, np, collect(r) AS summarizes
WHERE size(summarizes) > 1
RETURN ht, np, summarizes
LIMIT 1;

MATCH (np1:NavigableParents)-[r:NEXT]->(np2:NavigableParents)
WHERE r.file_name = "212ea9dc068b2bf3_Data_Engineer_I_New_York_NY_Indeed_com.html"
RETURN np1, r, np2;

MATCH (np1:NavigableParents)-[r:SUMMARIZES]->(np2:NavigableParents)
RETURN np1, r, np2;

MATCH (a)-[r:SUMMARIZES]->(np:NavigableParents)
RETURN
    DISTINCT LABELS(a) AS a_type_name,
    COUNT(*) AS a_type_count;

MATCH (np:NavigableParents)
WHERE
   NOT EXISTS {
        MATCH (:PartsOfSpeech)-[:SUMMARIZES]->(np)
    }
    AND NOT (
        np.is_header IS NULL
        AND np.is_task_scope IS NULL
        AND np.is_minimum_qualification IS NULL
        AND np.is_preferred_qualification IS NULL
        AND np.is_educational_requirement IS NULL
        AND np.is_legal_notification IS NULL
        AND np.is_other IS NULL
        AND np.is_corporate_scope IS NULL
        AND np.is_job_title IS NULL
        AND np.is_office_location IS NULL
        AND np.is_job_duration IS NULL
        AND np.is_supplemental_pay IS NULL
        AND np.is_interview_procedure IS NULL
        AND np.is_posting_date IS NULL
    )
RETURN
    COUNT(*) AS np_count;
    //np.navigable_parent AS navigable_parent;

MATCH (pos:PartsOfSpeech)-[r:SUMMARIZES]->(np:NavigableParents)
WITH pos, r, np, collect(pos) as nodes
WHERE size(nodes) > 1
RETURN pos, r, np;

MATCH (np:NavigableParents)
WHERE NOT EXISTS {
    MATCH (:PartsOfSpeech)-[:SUMMARIZES]->(np)
}
RETURN np.navigable_parent AS navigable_parent;

MATCH (a)-[r:SUMMARIZES]->(np:NavigableParents)
RETURN
    DISTINCT LABELS(a) AS a_type_name,
    COUNT(*) AS a_type_count;

MATCH (a)-[r:SUMMARIZES]->(b)
RETURN
    DISTINCT LABELS(b) AS b_type_name,
    COUNT(*) AS b_type_count;

MATCH (a)-[r:SUMMARIZES]->(b)
RETURN
    DISTINCT LABELS(a) AS a_type_name,
    COUNT(*) AS a_type_count;

MATCH (a)-[r]-(b)
RETURN
    DISTINCT TYPE(r) AS type_name,
    COUNT(*) AS type_count;

MATCH (pos:PartsOfSpeech)-[r:SUMMARIZES]->(np:NavigableParents)
WHERE
    np.is_qualification = true
    AND np.is_minimum_qualification = false
    AND np.is_preferred_qualification = false
RETURN
    pos.pos_symbol AS pos_symbol,
    np.navigable_parent AS navigable_parent;

MATCH (ht:HeaderTags)-[r:SUMMARIZES]->(np:NavigableParents)
WITH ht, np, collect(r) AS summarizes
WHERE size(summarizes) > 1
RETURN ht, np, summarizes
LIMIT 1;

// Try to connect all unconnected child strings to their obvious parts-of-speech
MATCH (np:NavigableParents)
WHERE
   NOT EXISTS {
        MATCH (:PartsOfSpeech)-[:SUMMARIZES]->(np:NavigableParents)
    }
    AND NOT (
        np.is_header IS NULL
        AND np.is_task_scope IS NULL
        AND np.is_minimum_qualification IS NULL
        AND np.is_preferred_qualification IS NULL
        AND np.is_educational_requirement IS NULL
        AND np.is_legal_notification IS NULL
        AND np.is_other IS NULL
        AND np.is_corporate_scope IS NULL
        AND np.is_job_title IS NULL
        AND np.is_office_location IS NULL
        AND np.is_job_duration IS NULL
        AND np.is_supplemental_pay IS NULL
        AND np.is_interview_procedure IS NULL
        AND np.is_posting_date IS NULL
    )
WITH
    np.is_header AS np_is_header,
    np.is_task_scope AS np_is_task_scope,
    np.is_minimum_qualification AS np_is_minimum_qualification,
    np.is_preferred_qualification AS np_is_preferred_qualification,
    np.is_educational_requirement AS np_is_educational_requirement,
    np.is_legal_notification AS np_is_legal_notification,
    np.is_other AS np_is_other,
    np.is_corporate_scope AS np_is_corporate_scope,
    np.is_job_title AS np_is_job_title,
    np.is_office_location AS np_is_office_location,
    np.is_job_duration AS np_is_job_duration,
    np.is_supplemental_pay AS np_is_supplemental_pay,
    np.is_interview_procedure AS np_is_interview_procedure,
    np.is_posting_date AS np_is_posting_date
    MATCH
        (pos:PartsOfSpeech {
            is_header: np_is_header,
            is_task_scope: np_is_task_scope,
            is_minimum_qualification: np_is_minimum_qualification,
            is_preferred_qualification: np_is_preferred_qualification,
            is_educational_requirement: np_is_educational_requirement,
            is_legal_notification: np_is_legal_notification,
            is_other: np_is_other,
            is_corporate_scope: np_is_corporate_scope,
            is_job_title: np_is_job_title,
            is_office_location: np_is_office_location,
            is_job_duration: np_is_job_duration,
            is_supplemental_pay: np_is_supplemental_pay,
            is_interview_procedure: np_is_interview_procedure,
            is_posting_date: np_is_posting_date
        }),
        (np2:NavigableParents {
            is_header: np_is_header,
            is_task_scope: np_is_task_scope,
            is_minimum_qualification: np_is_minimum_qualification,
            is_preferred_qualification: np_is_preferred_qualification,
            is_educational_requirement: np_is_educational_requirement,
            is_legal_notification: np_is_legal_notification,
            is_other: np_is_other,
            is_corporate_scope: np_is_corporate_scope,
            is_job_title: np_is_job_title,
            is_office_location: np_is_office_location,
            is_job_duration: np_is_job_duration,
            is_supplemental_pay: np_is_supplemental_pay,
            is_interview_procedure: np_is_interview_procedure,
            is_posting_date: np_is_posting_date
        })
    //MERGE (pos)-[r:SUMMARIZES]->(np2)
    RETURN pos, np2
    LIMIT 1;

CALL db.schema.nodeTypeProperties() YIELD nodeType
RETURN DISTINCT nodeType;

// Fix HTML that really should be headers
MATCH (np:NavigableParents)
WHERE
    (np.navigable_parent =~ "^.+:</[a-z]+>$")
    AND NOT (np.is_header = true)
SET np.is_header = true
RETURN
    np.is_header AS is_header,
    np.navigable_parent AS navigable_parent;

// Fix HTML that really should be an interview procedure
MATCH (np:NavigableParents)
WHERE
    (np.navigable_parent =~ "^(<[^><]+>)?Learn more at .+$")
    AND NOT (np.is_interview_procedure = true)
SET np.is_interview_procedure = true
RETURN
    np.is_header AS is_interview_procedure,
    np.navigable_parent AS navigable_parent;

// Get all the parts-of-speech relationships that haven`t been populated
MATCH (np:NavigableParents)
WHERE
    (NOT (np)<-[:SUMMARIZES]-(:PartsOfSpeech))
    AND (np.is_header IS NOT NULL)
    AND (np.is_task_scope IS NOT NULL)
    AND (np.is_minimum_qualification IS NOT NULL)
    AND (np.is_preferred_qualification IS NOT NULL)
    AND (np.is_legal_notification IS NOT NULL)
    AND (np.is_job_title IS NOT NULL)
    AND (np.is_office_location IS NOT NULL)
    AND (np.is_job_duration IS NOT NULL)
    AND (np.is_supplemental_pay IS NOT NULL)
    AND (np.is_educational_requirement IS NOT NULL)
    AND (np.is_interview_procedure IS NOT NULL)
    AND (np.is_corporate_scope IS NOT NULL)
    AND (np.is_posting_date IS NOT NULL)
    AND (np.is_other IS NOT NULL)
RETURN np;

// Get all node types that have the is_qualified property defined
CALL db.schema.nodeTypeProperties() YIELD nodeType, propertyName
WHERE propertyName = "is_qualified"
RETURN DISTINCT nodeType;

// Get all possible paths
MATCH path = (np:NavigableParents)-[rels:NEXT*]->(np2:NavigableParents)

// Check that the property is uniform and
// the first node is a min qual header
WHERE
    np.is_minimum_qualification = true AND
    np.is_header = true AND
    ALL(r in rels WHERE rels[0]["file_name"] = r.file_name)
RETURN rels[0]["file_name"] AS file_name;

// Set all the HTML that are strangely marked as a header to NULL
MATCH (np:NavigableParents)
WHERE
    (np.is_header IS NOT NULL)
    AND (np.is_task_scope IS NULL)
    AND (np.is_minimum_qualification IS NULL)
    AND (np.is_preferred_qualification IS NULL)
    AND (np.is_legal_notification IS NULL)
    AND (np.is_job_title IS NULL)
    AND (np.is_office_location IS NULL)
    AND (np.is_job_duration IS NULL)
    AND (np.is_supplemental_pay IS NULL)
    AND (np.is_educational_requirement IS NULL)
    AND (np.is_interview_procedure IS NULL)
    AND (np.is_corporate_scope IS NULL)
    AND (np.is_posting_date IS NULL)
    AND (np.is_other IS NULL)
SET np.is_header = NULL
RETURN COUNT(np);

// Find all properties with a name like "is_qual"
MATCH (np:NavigableParents)
UNWIND keys(np) AS property
WITH np, property
WHERE property =~ "^is_.*qual.+$"
RETURN DISTINCT property;

// Get all node types that have the file_name property defined
CALL db.schema.nodeTypeProperties() YIELD nodeType, propertyName
WHERE propertyName = "file_name"
RETURN DISTINCT nodeType as node_type;

// Get all relationship types
CALL db.relationshipTypes() YIELD relationshipType
RETURN DISTINCT relationshipType;

// Find all the relationship types in the graph with a file_name property
MATCH (nt1)-[r:NEXT]-(nt2)
WHERE exists(r.file_name)
RETURN DISTINCT labels(nt1) AS nt1_types;

// Find all properties with a value of "False"
CALL db.propertyKeys() YIELD propertyKey AS prop_name
MATCH (n)
WHERE n[prop_name] = "False"
WITH DISTINCT prop_name, labels(n)[0] AS node_name
RETURN prop_name, node_name;