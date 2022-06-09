
MATCH (np:NavigableParents)<-[s:SUMMARIZES]-(ht)
WITH tail(COLLECT(s)) as butfirst
foreach(x in butfirst | DELETE x);