
CALL {
  MATCH (a)-[r: IS_CONTAINED_IN]->(b)
  RETURN a, b
  ORDER BY rand()
  LIMIT 15
UNION
  MATCH (a)-[r: IS_PART_OF]->(b)
  RETURN a, b
  ORDER BY rand()
  LIMIT 15
UNION
  MATCH (a)-[r: SUMMARIZES]->(b)
  RETURN a, b
  ORDER BY rand()
  LIMIT 15
}
RETURN a, b;