
// Export all nodes and relationships
UNWIND range(1,apoc.cypher.getNodeCount()) AS n
MATCH (n) OPTIONAL MATCH (n)-[r]->(m)
RETURN n, type(n), r, type(r), m;

// Export all constraints and indexes
CALL apoc.schema.export();