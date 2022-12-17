
MATCH (fn:FileNames)
WHERE
    fn.percent_fit >= 0.8 AND
    ((fn.is_closed IS NULL) OR (fn.is_closed = false)) AND
    ((fn.is_opportunity_application_emailed IS NULL) OR
    (fn.is_opportunity_application_emailed = false))
RETURN
    fn.percent_fit AS percent_fit,
    fn.file_name AS file_name,
    fn.posting_url AS posting_url
ORDER BY fn.percent_fit DESC;

MATCH (np:NavigableParents)
WHERE (np.is_qualification IS NOT NULL)
RETURN count(*);

MATCH (fn:FileNames {file_name: "Python_and_SQL_Developer_Remote_Indeed_com.html"})
SET fn.is_opportunity_application_emailed = true, fn.opportunity_application_email_date = date()
RETURN fn;

MATCH (fn:FileNames {file_name: "aMDl94_HegifUiq3Yt7f3Q_Data_Integration_Specialist_Manager_PwC_Boston_MA_Remote.html"})
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

MATCH (np:NavigableParents)
WHERE np.is_qualification = 'True'
RETURN np.navigable_parent;

MATCH (np:NavigableParents {navigable_parent: "<li>GIS: 3 years (Required)</li>"})
SET np.is_minimum_qualification = 'True';

MATCH (np:NavigableParents {navigable_parent: "<li>Python: 10 years (Preferred)</li>"})
SET np.is_preferred_qualification = 'True';

MATCH (np:NavigableParents {navigable_parent: "Hope you are doing safe and fine amidst pandemic!"})
SET np.is_qualification = NULL;

//"<b>Have deep finance experience.</b>"
MATCH (np:NavigableParents)
WHERE
    np.is_qualification = 'True'
    AND np.is_minimum_qualification IS NULL
    AND np.is_preferred_qualification IS NULL
RETURN np.navigable_parent;

//"<b>Have deep finance experience.</b>"
MATCH (np:NavigableParents)
WHERE
    np.is_qualification = 'True'
    AND np.is_minimum_qualification = 'False'
    AND np.is_preferred_qualification = 'False'
RETURN np.navigable_parent;

MATCH (np:NavigableParents {navigable_parent: "<b>based products and applications.</b>"})
SET np.is_qualification = NULL;

MATCH (pos:PartsOfSpeech)-[r:SUMMARIZES]->(np:NavigableParents)
WHERE
    np.is_qualification = 'True'
    AND np.is_minimum_qualification = 'False'
    AND np.is_preferred_qualification = 'False'
RETURN
    pos.pos_symbol AS pos_symbol,
    np.navigable_parent AS navigable_parent;

MATCH (np:NavigableParents {navigable_parent: "<b>Have deep finance experience.</b>"})-[n:NEXT]->(:NavigableParents)
RETURN n
ORDER BY n.sequence_order;