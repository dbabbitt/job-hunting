
MATCH (fn:FileNames)
WHERE
    fn.percent_fit IS NOT NULL AND
    fn.is_closed IS NULL AND
    fn.is_verfied IS NULL AND
    fn.is_opportunity_application_emailed IS NULL
RETURN
    fn.percent_fit AS percent_fit,
    fn.posting_url AS url,
    fn.file_name AS file_name
ORDER BY fn.percent_fit DESC;