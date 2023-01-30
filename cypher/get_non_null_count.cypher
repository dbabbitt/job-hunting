
MATCH (np:NavigableParents)
RETURN
    COUNT(*) AS total_count,
    COUNT(np.is_header) AS non_null_count;