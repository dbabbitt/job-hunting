
MATCH (fn:FileNames {file_name: "464b66ce20a2adc0_Data_Architect_100_Remote_Remote_Indeed_com.html"})
SET fn.is_remote = false, fn.is_verified = true
RETURN fn

MATCH (fn:FileNames {file_name: "464b66ce20a2adc0_Data_Architect_100_Remote_Remote_Indeed_com.html"})
SET fn.is_opportunity_application_emailed = true, fn.opportunity_application_email_date = date()
RETURN fn

MATCH (fn:FileNames {file_name: "1008006392357_Data_Science_Analyst.html"})
SET fn.is_closed = true
RETURN fn

MATCH (fn:FileNames)
WHERE
    fn.percent_fit >= 0.8 AND
    ((fn.is_closed IS NULL) OR (fn.is_closed = false)) AND
    ((fn.is_verified IS NULL) OR (fn.is_verified = false)) AND
    ((fn.is_opportunity_application_emailed IS NULL) OR
    (fn.is_opportunity_application_emailed = false))
RETURN
    fn.percent_fit AS percent_fit,
    fn.file_name AS file_name,
    fn.posting_url AS posting_url
ORDER BY fn.percent_fit DESC
LIMIT 2;

MATCH (fn:FileNames)
WHERE fn.file_name = "MN_6jbmPJD6EoG7_Ld9Q_Senior_Python_Engineer_VanderHouwen_Beaverton_OR_Remote.html"
SET fn.is_opportunity_application_emailed = true, fn.opportunity_application_email_date = date()
RETURN fn