
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

MATCH (fn:FileNames {file_name: "48e1fa9d2fbdbff2_Data_Scientist_Remote_Indeed_com.html"})
SET fn.is_opportunity_application_emailed = true, fn.opportunity_application_email_date = date()
RETURN fn;

MATCH (fn:FileNames)
WHERE
    fn.file_name = "54c63703090b13c0_AI_Engineer_Walnut_Creek_CA_Indeed_com.html"
RETURN
    fn.percent_fit AS percent_fit,
    fn.file_name AS file_name,
    fn.posting_url AS posting_url
ORDER BY fn.percent_fit DESC;

MATCH (np1:NavigableParents)-[r:NEXT]->(np2:NavigableParents)
WHERE r.file_name = "f74391cece289324_Senior_Performance_Engineer_Cloud_Infrastructure_Remote_Indeed_com.html"
RETURN
    LEFT(np1.navigable_parent, 50) AS navigable_parent1,
    np1.is_header AS is_header1,
    np1.is_task_scope AS is_task_scope1,
    np1.is_minimum_qualification AS is_minimum_qualification1,
    np1.is_preferred_qualification AS is_preferred_qualification1,
    np1.is_educational_requirement AS is_educational_requirement1,
    np1.is_legal_notification AS is_legal_notification1,
    np1.is_other AS is_other1,
    np1.is_corporate_scope AS is_corporate_scope1,
    np1.is_job_title AS is_job_title1,
    np1.is_office_location AS is_office_location1,
    np1.is_job_duration AS is_job_duration1,
    np1.is_supplemental_pay AS is_supplemental_pay1,
    np1.is_interview_procedure AS is_interview_procedure1,
    np1.is_posting_date AS is_posting_date1
ORDER BY r.sequence_order;

MATCH (fn:FileNames {file_name: "39ad8c2d1627717d_Quality_Assurance_Engineer_Manhattan_KS_66506_Indeed_com.html"})
SET fn.is_closed = true
RETURN fn;

MATCH (np:NavigableParents)
WHERE (np.is_qualification IS NOT NULL)
RETURN count(*);

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