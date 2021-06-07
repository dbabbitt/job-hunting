
CALL {
  MATCH (pos:PartsOfSpeech {pos_symbol: 'H-TS'})-->(np:NavigableParents)
  RETURN pos, np
  LIMIT 1
UNION
  MATCH (pos:PartsOfSpeech {pos_symbol: 'O-TS'})-->(np:NavigableParents)
  RETURN pos, np
  LIMIT 1
UNION
  MATCH (pos:PartsOfSpeech {pos_symbol: 'H-RQ'})-->(np:NavigableParents)
  RETURN pos, np
  LIMIT 1
UNION
  MATCH (pos:PartsOfSpeech {pos_symbol: 'O-RQ'})-->(np:NavigableParents)
  RETURN pos, np
  LIMIT 1
UNION
  MATCH (pos:PartsOfSpeech {pos_symbol: 'H-PQ'})-->(np:NavigableParents)
  RETURN pos, np
  LIMIT 1
UNION
  MATCH (pos:PartsOfSpeech {pos_symbol: 'O-PQ'})-->(np:NavigableParents)
  RETURN pos, np
  LIMIT 1
UNION
  MATCH (pos:PartsOfSpeech {pos_symbol: 'H-LN'})-->(np:NavigableParents)
  RETURN pos, np
  LIMIT 1
UNION
  MATCH (pos:PartsOfSpeech {pos_symbol: 'O-LN'})-->(np:NavigableParents)
  RETURN pos, np
  LIMIT 1
UNION
  MATCH (pos:PartsOfSpeech {pos_symbol: 'H-JT'})-->(np:NavigableParents)
  RETURN pos, np
  LIMIT 1
UNION
  MATCH (pos:PartsOfSpeech {pos_symbol: 'O-JT'})-->(np:NavigableParents)
  RETURN pos, np
  LIMIT 1
UNION
  MATCH (pos:PartsOfSpeech {pos_symbol: 'H-OL'})-->(np:NavigableParents)
  RETURN pos, np
  LIMIT 1
UNION
  MATCH (pos:PartsOfSpeech {pos_symbol: 'O-OL'})-->(np:NavigableParents)
  RETURN pos, np
  LIMIT 1
UNION
  MATCH (pos:PartsOfSpeech {pos_symbol: 'H-JD'})-->(np:NavigableParents)
  RETURN pos, np
  LIMIT 1
UNION
  MATCH (pos:PartsOfSpeech {pos_symbol: 'O-JD'})-->(np:NavigableParents)
  RETURN pos, np
  LIMIT 1
UNION
  MATCH (pos:PartsOfSpeech {pos_symbol: 'H-SP'})-->(np:NavigableParents)
  RETURN pos, np
  LIMIT 1
UNION
  MATCH (pos:PartsOfSpeech {pos_symbol: 'O-SP'})-->(np:NavigableParents)
  RETURN pos, np
  LIMIT 1
UNION
  MATCH (pos:PartsOfSpeech {pos_symbol: 'H-ER'})-->(np:NavigableParents)
  RETURN pos, np
  LIMIT 1
UNION
  MATCH (pos:PartsOfSpeech {pos_symbol: 'O-ER'})-->(np:NavigableParents)
  RETURN pos, np
  LIMIT 1
UNION
  MATCH (pos:PartsOfSpeech {pos_symbol: 'H-IP'})-->(np:NavigableParents)
  RETURN pos, np
  LIMIT 1
UNION
  MATCH (pos:PartsOfSpeech {pos_symbol: 'O-IP'})-->(np:NavigableParents)
  RETURN pos, np
  LIMIT 1
UNION
  MATCH (pos:PartsOfSpeech {pos_symbol: 'H-CS'})-->(np:NavigableParents)
  RETURN pos, np
  LIMIT 1
UNION
  MATCH (pos:PartsOfSpeech {pos_symbol: 'O-CS'})-->(np:NavigableParents)
  RETURN pos, np
  LIMIT 1
UNION
  MATCH (pos:PartsOfSpeech {pos_symbol: 'H-PD'})-->(np:NavigableParents)
  RETURN pos, np
  LIMIT 1
UNION
  MATCH (pos:PartsOfSpeech {pos_symbol: 'O-PD'})-->(np:NavigableParents)
  RETURN pos, np
  LIMIT 1
UNION
  MATCH (pos:PartsOfSpeech {pos_symbol: 'H-O'})-->(np:NavigableParents)
  RETURN pos, np
  LIMIT 1
UNION
  MATCH (pos:PartsOfSpeech {pos_symbol: 'O-O'})-->(np:NavigableParents)
  RETURN pos, np
  LIMIT 1
}
RETURN pos, np;