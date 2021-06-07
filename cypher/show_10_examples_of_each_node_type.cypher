
CALL {
  MATCH (x:FileNames)
  RETURN x
  LIMIT 10
UNION
  MATCH (x:HeaderTags)
  RETURN x
  LIMIT 10
UNION
  MATCH (x:HeaderTagSequence)
  RETURN x
  LIMIT 10
UNION
  MATCH (x:MinimumRequirementsSection)
  RETURN x
  LIMIT 10
UNION
  MATCH (x:NavigableParents)
  RETURN x
  LIMIT 10
UNION
  MATCH (x:NavigableParentSequence)
  RETURN x
  LIMIT 10
UNION
  MATCH (x:PartsOfSpeech)
  RETURN x
  LIMIT 10
}
RETURN x;