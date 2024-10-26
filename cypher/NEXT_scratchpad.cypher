
// Get all unique node types and relationship types
MATCH (n1)-[r]->(n2)
WITH DISTINCT labels(n1) AS node1Labels, type(r) AS relType, labels(n2) AS node2Labels
UNWIND node1Labels AS label1
WITH DISTINCT label1, relType, node2Labels
UNWIND node2Labels AS label2
WITH DISTINCT label1, relType, label2
RETURN DISTINCT label1 AS node1_type, relType AS relationship_type, label2 AS node2_type
ORDER BY node1_type, relationship_type, node2_type;

// Get all unique relationship types and their properties, including relationship types without properties
MATCH ()-[r]->()
WITH DISTINCT type(r) AS relType, keys(r) AS relProperties
UNWIND relProperties AS property
RETURN DISTINCT relType AS relationship_type, property AS unique_property
ORDER BY relationship_type, unique_property
UNION
MATCH ()-[r]->()
WHERE size(keys(r)) = 0
WITH DISTINCT type(r) AS relType
RETURN relType AS relationship_type, null AS unique_property
ORDER BY relationship_type;

// Get all unique relationship types
MATCH ()-[r]->()
WITH DISTINCT type(r) AS relType, keys(r) AS properties
UNWIND properties AS property
RETURN relType AS relationship_type, DISTINCT property AS unique_property
ORDER BY relationship_type, unique_property;

// Get all unique relationship types
MATCH ()-[r]->()
WITH DISTINCT type(r) AS relType
RETURN relType AS relationshipType;

// Get all unique relationship types that have the 'file_name' property
MATCH ()-[r]->()
WITH DISTINCT type(r) AS relType
MATCH ()-[r]->()
WHERE type(r) = relType AND exists(r.file_name)
WITH DISTINCT relType
RETURN relType AS relationshipType;

// Get all unique properties across all NEXT relationships
MATCH ()-[r:NEXT]->()
WITH keys(r) AS properties
UNWIND properties AS property
RETURN DISTINCT property AS unique_property
ORDER BY unique_property;