
MATCH (:NavigableParents)-[n:NEXT {file_name: "52f0f96e8b1f7618_GIS_Developer_Remote_Indeed_com.html"}]->(:NavigableParents)
RETURN n
ORDER BY n.sequence_order;