
// Find quals that speak of clearances
MATCH (qs:QualificationStrings)
WHERE
    (qs.qualification_str =~ "^.*[Cc]learance.*$")
RETURN
    qs.is_qualified AS is_qualified,
    qs.qualification_str AS qualification_str
ORDER BY qualification_str;

// Get all unique properties across all QualificationStrings nodes
MATCH (qs:QualificationStrings)
WHERE
    (qs.qualification_str CONTAINS "learance")
WITH collect(keys(qs)) AS all_properties
WITH apoc.coll.toSet(apoc.coll.flatten(all_properties)) AS unique_properties
UNWIND unique_properties AS property
RETURN property
ORDER BY property;

// Find quals that really should be headers
MATCH (qs:QualificationStrings)
WHERE
    (qs.qualification_str =~ "^.+:</[a-z]+>$")
RETURN qs.qualification_str AS qualification_str;

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