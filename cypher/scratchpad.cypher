
MATCH (fn:FileNames {file_name: "50085e4eb4f424bb_Junior_Data_Scientist_Remote_Indeed_com.html"})
SET fn.is_closed = true
RETURN fn

MATCH (fn:FileNames)
WHERE (fn.opportunity_application_email_date IS NOT NULL)
SET fn.opportunity_application_email_date = date(fn.opportunity_application_email_date)
RETURN fn;

MATCH (fn:FileNames)
WHERE
    (fn.opportunity_application_email_date < date("2022-08-14")) AND
    (fn.opportunity_application_email_date >= date("2022-08-07"))
RETURN fn;

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
ORDER BY fn.percent_fit DESC;

MATCH (fn:FileNames {file_name: "TTDJNNQubjvrY7upcwO_2Q_Senior_Data_Scientist_Demandbase_United_States_Remote.html"})
SET fn.is_opportunity_application_emailed = true, fn.opportunity_application_email_date = date()
RETURN fn;

MATCH (fn:FileNames)
WHERE (fn.file_name CONTAINS "Fidelity")
RETURN fn
ORDER BY fn.percent_fit DESC;

MATCH (fn:FileNames {file_name: "Hybrid_Process_Engineer_Data_Scientist_Primary_Talent_Partners_Devens_MA_01434.html"})
SET
    fn.is_opportunity_application_emailed = true,
    fn.opportunity_application_email_date = "2022-08-03",
    fn.rtr_name = "Primary Talent Partners",
    fn.job_requisition_number = "49556",
    fn.recruiter_email = "devonj@primarytalentpartners.com",
    fn.recruiter_name = "Devon Jain"
RETURN fn;

MATCH (fn:FileNames)
WHERE
    (fn.file_name CONTAINS "Senior") AND
    (fn.file_name CONTAINS "Data") AND
    (fn.file_name CONTAINS "Analyst")
RETURN
    fn.percent_fit AS percent_fit,
    fn.is_closed AS is_closed,
    fn.is_opportunity_application_emailed AS email
ORDER BY fn.percent_fit DESC;

MATCH (fn:FileNames {file_name: "464b66ce20a2adc0_Data_Architect_100_Remote_Remote_Indeed_com.html"})
SET fn.is_remote = false, fn.is_verified = true
RETURN fn

MATCH (fn:FileNames)
WHERE fn.file_name = "MN_6jbmPJD6EoG7_Ld9Q_Senior_Python_Engineer_VanderHouwen_Beaverton_OR_Remote.html"
SET fn.is_opportunity_application_emailed = true, fn.opportunity_application_email_date = date()
RETURN fn