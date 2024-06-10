
// Get all node types that have a file property defined
CALL db.schema.nodeTypeProperties() YIELD nodeType, propertyName
WHERE propertyName CONTAINS "file"
RETURN DISTINCT nodeType;

// Export the whole database to a GraphML file
CALL apoc.export.graphml.all("apoc_export_graphml_all_job_hunting.graphml", {})

// Export everything to job_hunting.csv
CALL apoc.export.csv.all("apoc_export_csv_all_job_hunting.csv", {})

// Export everything to job_hunting.json
CALL apoc.export.json.all("apoc_export_json_all_job_hunting.json", {})

// Export five examples of each relationship type to apoc_export_csv_query_examplerelationships.csv
WITH "
    CALL {
        MATCH (a)-[r: IS_CONTAINED_IN]->(b)
        RETURN a, b
        ORDER BY rand()
        LIMIT 5
    UNION
        MATCH (a)-[r: IS_PART_OF]->(b)
        RETURN a, b
        ORDER BY rand()
        LIMIT 5
    UNION
        MATCH (a)-[r: SUMMARIZES]->(b)
        RETURN a, b
        ORDER BY rand()
        LIMIT 5
    }
    RETURN a, b;" AS query
CALL apoc.export.csv.query(query, "apoc_export_csv_query_examplerelationships.csv", {})
YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data
RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data;

// Export five examples of each relationship type to apoc_export_json_query_examplerelationships.json
WITH "
    CALL {
        MATCH (a)-[r: IS_CONTAINED_IN]->(b)
        RETURN a, b
        ORDER BY rand()
        LIMIT 5
    UNION
        MATCH (a)-[r: IS_PART_OF]->(b)
        RETURN a, b
        ORDER BY rand()
        LIMIT 5
    UNION
        MATCH (a)-[r: SUMMARIZES]->(b)
        RETURN a, b
        ORDER BY rand()
        LIMIT 5
    }
    RETURN a, b;" AS query
CALL apoc.export.json.query(query, "apoc_export_json_query_examplerelationships.json", {})
YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data
RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data;

// Export five examples of each relationship type to apoc_export_graphml_query_examplerelationships.graphml
WITH "
    CALL {
        MATCH (a)-[r: IS_CONTAINED_IN]->(b)
        RETURN a, b
        ORDER BY rand()
        LIMIT 5
    UNION
        MATCH (a)-[r: IS_PART_OF]->(b)
        RETURN a, b
        ORDER BY rand()
        LIMIT 5
    UNION
        MATCH (a)-[r: SUMMARIZES]->(b)
        RETURN a, b
        ORDER BY rand()
        LIMIT 5
    }
    RETURN a, b;" AS query
CALL apoc.export.graphml.query(query, "apoc_export_graphml_query_examplerelationships.graphml", {})
YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data
RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data;

MATCH (a)-[r:SUMMARIZES]->(b)
RETURN
    DISTINCT LABELS(b) AS b_type_name,
    COUNT(*) AS b_type_count;

MATCH (a)-[r:SUMMARIZES]->(b)
RETURN
    DISTINCT LABELS(a) AS a_type_name,
    COUNT(*) AS a_type_count;

// Get relationship types and their counts
MATCH (a)-[r]-(b)
RETURN
    DISTINCT TYPE(r) AS type_name,
    COUNT(*) AS type_count;

// Get all distinct node types
CALL db.schema.nodeTypeProperties() YIELD propertyName
RETURN DISTINCT propertyName;

// Get all distinct node types
CALL db.schema.nodeTypeProperties() YIELD nodeType
RETURN DISTINCT nodeType;

// Set all the javascript beginner quals to true
MATCH (qs:QualificationStrings)
WHERE
    (qs.qualification_str CONTAINS "Java Scripted Page")
    AND (
        (qs.qualification_str CONTAINS "Intermediate")
        OR (qs.qualification_str CONTAINS "Beginner")
    )
SET qs.is_qualified = 1
RETURN qs;

// Find quals that really should be headers
MATCH (qs:QualificationStrings)
WHERE
    (qs.qualification_str =~ "^.+:</[a-z]+>$")
RETURN qs.qualification_str AS qualification_str;

// Get all node types that have the is_qualified property defined
CALL db.schema.nodeTypeProperties() YIELD nodeType, propertyName
WHERE propertyName = "is_qualified"
RETURN DISTINCT nodeType;

// Delete all but one of the duplicate HeaderTags
// nodes based on the header_tag property
MATCH (ht:HeaderTags)
WITH
    ht.header_tag AS header_tag,
    collect(ht) AS nodes,
    count(*) AS tag_count
WHERE tag_count > 1
UNWIND tail(nodes) AS node
DETACH DELETE node;

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

// Replace "True" with true and "False" with false
MATCH (n)
SET n.property = CASE n.property
  WHEN "False" THEN false
  WHEN "True" THEN true
  ELSE n.property
END;