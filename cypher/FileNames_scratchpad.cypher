
// Update File Names node with rejection email text
MATCH (fn:FileNames)
WHERE (fn.file_name IN ["7f1ec2d01345f3a8_Data_Scientist_I_Payment_Integrity_New_York_NY_Indeed_com.html"])
SET
    fn.rejection_email_text = "We appreciate your interest in Oscar Health and the time you’ve invested in applying for the Data Scientist II role. We recently closed this role and are no longer reviewing candidates for the position. We encourage you to keep an eye on our website and apply to any positions that you may be interested in. We will keep your resume on file and may reach out if a role opens that matches your skills and experience.",
    fn.rejection_email_date = date("2024-11-26"),
    fn.is_closed = true
RETURN
    fn.opportunity_application_email_date AS application_date,
    fn.is_closed AS is_closed,
    fn.percent_fit AS percent_fit,
    fn.rejection_email_date AS rejection_email_date,
    fn.file_name AS file_name,
    fn.posting_url AS posting_url
ORDER BY fn.opportunity_application_email_date DESC;

// Check for application duplicates or unrejected postings
MATCH (fn:FileNames)
WHERE (fn.file_name IN ["3d87bc8fcd2a66b5_Sr_Data_Scientist_II_Alpharetta_GA_30005_Indeed_com.html", "6cd512fc61cd4572_Data_Scientist_II_JR14367_Remote_Indeed_com.html", "9f3b46174986d905_Data_Scientist_II_Remote_Indeed_com.html", "40f70f73663d2525_Data_Scientist_II_Remote_Indeed_com.html", "40f8709b20021987_Data_Scientist_II_Washington_DC_Indeed_com.html", "80b9c9a85f452959_Data_Scientist_III_Raleigh_NC_27606_Indeed_com.html", "91a9d1584bd3ea76_Data_Scientist_III_Remote_Indeed_com.html", "3749f33483ea1253_Data_Scientist_III_Remote_Indeed_com.html", "80168c7a079d6fa4_Data_Scientist_II_Remote_Indeed_com.html", "532002b34707356c_Data_Scientist_III_Remote_Indeed_com.html", "1338794_Data_Scientist_III_Availity.html", "1509255_Data_Scientist_II_Elsevier_BV_Company.html", "1537294f4c1e0417_CPAESS_Associate_Data_Scientist_II_Boulder_CO_80305_Indeed_com.html", "1669614_Data_Scientist_Music_Monetisation_Spotify.html", "a2214d95d916ff08_Sr_Data_Scientist_II_Alpharetta_GA_Indeed_com.html", "b36ec850cce3d36b_Data_Scientist_II_Remote_Remote_Indeed_com.html", "c2c6ffc0b75e0f99_Sr_Data_Scientist_II_Boston_MA_Indeed_com.html", "c2840f1b33525c57_Data_Scientist_II_AI_ML_Remote_Indeed_com.html", "d1149aa75b7c4498_Data_Scientist_III_Marlborough_MA_01752_Indeed_com.html", "Data_Scientist_II,_Economic_Data_-_Remote_Position_Data_Scientist_II,_Economic_Data_-_Remote_Position_a3569c3f5c6cffdc.html.html", "Data_Scientist_II_Remote.html", "Data_Scientist_II_Remote_Indeed_com.html", "Data_Scientist_III,_Business_Analytics_-_California_-_Indeed.com_88f5d9a70576ec2a.html", "df96c283373514e1_Data_Scientist_III_Remote_Indeed_com.html", "e2440208975cf80a_Data_Scientist_II_Remote_Remote_Indeed_com.html", "ea15987ed6bc3ee2_Data_Scientist_II_Remote_Indeed_com.html", "ecf20170b88c7b71_Data_Scientist_II_Remote_Indeed_com.html", "f39dd8ab67a6a98e_Data_Scientist_II_Outcomes_Research_Chicago_IL_Indeed_com.html", "u1w5o1yiSJHlpBAwN4O9Rw_Data_Scientist_III_Myriad_Genetics_United_States_Remote.html"])
RETURN
    fn.opportunity_application_email_date AS application_date,
    fn.is_closed AS is_closed,
    fn.percent_fit AS percent_fit,
    fn.rejection_email_date AS rejection_email_date,
    fn.file_name AS file_name,
    fn.posting_url AS posting_url
ORDER BY fn.opportunity_application_email_date DESC;

// Find all work search activities for the date range
WITH "Sunday, 11/17/2024 - Saturday, 11/23/2024" AS date_range
WITH split(date_range, " - ") AS dates
WITH
    split(dates[0], ", ") AS start_components,
    split(dates[1], ", ") AS end_components
WITH
    [item in split(start_components[1], "/") | toInteger(item)] AS start_components,
    [item in split(end_components[1], "/") | toInteger(item)] AS end_components
WITH
    date({
        day: start_components[1],
        month: start_components[0],
        year: start_components[2]
    }) AS date_start,
    date({
        day: end_components[1],
        month: end_components[0],
        year: end_components[2]
    }) AS date_end
MATCH (fn:FileNames)
WHERE
    (fn.opportunity_application_email_date >= date_start) AND
    (fn.opportunity_application_email_date <= date_end)
RETURN
    fn.file_name AS file_name,
    fn.opportunity_application_email_date AS opportunity_application_email_date,
    fn.posting_url AS posting_url,
    fn.recruiter_screen_completion_date AS recruiter_screen_completion_date,
    fn.rejection_email_date AS rejection_email_date,
    fn.tech_interview_completion_date AS tech_interview_completion_date;

// Count applications by search type
MATCH (fn:FileNames)
WHERE fn.search_type IS NOT NULL
WITH
    fn.search_type AS search_type,
    COUNT(CASE WHEN fn.opportunity_application_email_date IS NOT NULL THEN 1 END) AS successful_count,
    COUNT(CASE WHEN fn.opportunity_application_email_date IS NULL THEN 1 END) AS unsuccessful_count,
    COUNT(fn) AS total_count
RETURN
    search_type, 
    successful_count, 
    unsuccessful_count,
    CASE WHEN total_count > 0 THEN ROUND((successful_count * 100.0 / total_count) * 10) / 10 ELSE 0 END AS percentage_successful
ORDER BY
    percentage_successful DESC,
    unsuccessful_count DESC;

// Get all the rejection sentences
MATCH (fn:FileNames)
WHERE (fn.rejection_email_text IS NOT NULL)
RETURN fn.rejection_email_text AS rejection_email_text;

// Update File Names node with phone screen date
MATCH (fn:FileNames)
WHERE fn.file_name IN ["e90e83851650a0d3_AI_ML_NLP_Trainer_for_Part_Time_Freelance_100_Remote_Work_From_Home_Remote_Indeed_com.html"]
SET fn.is_recruiter_screen_completed = true, fn.recruiter_screen_completion_date = date()
RETURN fn;

// Get all apoc procedures
SHOW PROCEDURES YIELD name, description, signature
RETURN name, description, signature
ORDER BY name;

// Get all unique properties across all FileNames nodes
MATCH (fn:FileNames)
WITH collect(keys(fn)) AS all_properties
UNWIND all_properties AS property_list
UNWIND property_list AS property
RETURN DISTINCT property
ORDER BY property;

// Get all unique node types and their properties, including node types without properties
MATCH (n)
WITH DISTINCT labels(n) AS nodeLabels, keys(n) AS nodeProperties
UNWIND nodeLabels AS label
WITH DISTINCT label, nodeProperties
UNWIND nodeProperties AS property
RETURN DISTINCT label AS node_type, property AS unique_property
ORDER BY node_type, unique_property
UNION
MATCH (n)
WHERE size(keys(n)) = 0
WITH DISTINCT labels(n) AS nodeLabels
UNWIND nodeLabels AS label
RETURN DISTINCT label AS node_type, null AS unique_property
ORDER BY node_type;

// Get all unique node and relationship labels that have a file_name or sequence_order property
CALL db.labels() YIELD label
WITH label
MATCH (n)
WHERE label IN labels(n) AND (exists(n.file_name) OR exists(n.sequence_order))
RETURN DISTINCT label AS unique_label
UNION
CALL db.relationshipTypes() YIELD relationshipType
WITH relationshipType
MATCH ()-[r]->()
WHERE type(r) = relationshipType AND (exists(r.file_name) OR exists(r.sequence_order))
RETURN DISTINCT relationshipType AS unique_label
ORDER BY unique_label;

// Find all File Names nodes with search types
MATCH (fn:FileNames)
WHERE fn.search_type IS NOT NULL
RETURN
    fn.search_type AS search_type,
    fn.file_name AS file_name,
    fn.opportunity_application_email_date AS opportunity_application_email_date,
    fn.posting_url AS posting_url,
    fn.recruiter_screen_completion_date AS recruiter_screen_completion_date,
    fn.rejection_email_date AS rejection_email_date,
    fn.tech_interview_completion_date AS tech_interview_completion_date
ORDER BY fn.search_type;

// Show rejection info on selected postings
MATCH (fn:FileNames)
WHERE
    (fn.file_name IN ["2MTx8MH_Qi2lXNRyK8p4eQ_Senior_Data_Scientist_Electric_Load_Forecasting_Waltham_MA.html", "c0ZxaPJOVkBXO_mvv81t0w_Senior_Data_Scientist_Electric_Load_Forecasting_Waltham_MA.html", "CDPQnexg1o1I50qz_3Pu0A_Senior_Data_Scientist_Electric_Load_Forecasting_Waltham_MA.html", "HZzUjJEw48m6d_fUeeIOfA_Senior_Data_Scientist_Electric_Load_Forecasting_Waltham_MA.html", "lczt6KSA9MU6qm_jBjagrA_Senior_Data_Scientist_Electric_Load_Forecasting_Waltham_MA.html", "m5ZwHrLY6Kc2HmseMji3Pw_Senior_Data_Scientist_Electric_Load_Forecasting_Waltham_MA.html", "upKoUNAylsvorTHBA2XThw_Senior_Data_Scientist_Electric_Load_Forecasting_Waltham_MA.html", "upUqAPz09NaTfzXPJrXW_A_Senior_Data_Scientist_Electric_Load_Forecasting_Waltham_MA.html", "WSvFXPuNIKBNPwD8F_M5sg_Senior_Data_Scientist_Electric_Load_Forecasting_Waltham_MA.html", "wvoi4RlIKeM15G9x9_MTNw_Senior_Data_Scientist_Electric_Load_Forecasting_Waltham_MA.html"]) AND
    ((fn.is_closed IS NULL) OR (fn.is_closed = false)) AND
    (fn.rejection_email_text IS NULL) AND
    (fn.rejection_email_date IS NULL) AND
    (fn.opportunity_application_email_date IS NOT NULL)
RETURN
    fn.opportunity_application_email_date AS application_date,
    fn.percent_fit AS percent_fit,
    fn.file_name AS file_name,
    fn.posting_url AS posting_url
ORDER BY fn.opportunity_application_email_date DESC;

// Get all unique node labels
CALL db.labels() YIELD label
WITH label AS node_label
RETURN node_label
ORDER BY node_label;

// Update File Names node with technical interview date
MATCH (fn:FileNames)
WHERE fn.file_name IN ["Amazon_Machine_Learning_Engineer_Boston_MA.html"]
SET fn.is_technical_interview_set = true, fn.technical_interview_dates = [date("2024-08-08")]
RETURN fn;

// Get the properties (not the entire node) for FileNames nodes
// where any property contains the string "interview"
MATCH (fn:FileNames)
WITH fn, [key IN keys(fn) WHERE key CONTAINS 'interview' | key] AS interview_properties
WHERE size(interview_properties) > 0
RETURN interview_properties;

// Rename the tech_interview_completion_date properties in the FileNames nodes
// to technical_interview_dates and convert their date values into a list of one date
MATCH (fn:FileNames)
WHERE fn.tech_interview_completion_date IS NOT NULL
SET fn.technical_interview_dates = [fn.tech_interview_completion_date]
REMOVE fn.tech_interview_completion_date;

// Replace the "phone" in phone_screen_completion_date and is_phone_screen_completed to "recruiter"
MATCH (fn:FileNames)
SET
    fn.recruiter_screen_completion_date = CASE WHEN exists(fn.phone_screen_completion_date) THEN fn.phone_screen_completion_date ELSE NULL END,
    fn.is_recruiter_screen_completed = CASE WHEN exists(fn.is_phone_screen_completed) THEN fn.is_phone_screen_completed ELSE NULL END
REMOVE
    fn.phone_screen_completion_date,
    fn.is_phone_screen_completed
RETURN fn;

// Update File Names node with tech interview date
MATCH (fn:FileNames)
WHERE fn.file_name IN ["a549539bc1bfd45d_Data_Analyst_Management_Data_Analysis_Northborough_MA_01532_Indeed_com.html"]
SET fn.is_tech_interview_completed = true, fn.tech_interview_completion_date = date("2024-8-16")
RETURN fn;

// Get the tagged node counts for each file
MATCH (pos:PartsOfSpeech)-[r1:SUMMARIZES]->(np1:NavigableParents)-[r2:NEXT]->(np2:NavigableParents)
WITH
    r2.file_name AS file_name,
    COUNT(r1) AS tagged_count,
    COUNT(r2) AS edge_count,
    COUNT(np1) AS np_count
RETURN np_count, tagged_count, edge_count, file_name
ORDER BY edge_count DESC;

// Get the edge and node counts for each file, tag-agnostic
MATCH (np1:NavigableParents)-[r:NEXT]->(np2:NavigableParents)
WITH
    r.file_name AS file_name,
    COUNT(r) AS edge_count,
    COUNT(np1) AS np_count
RETURN np_count, edge_count, file_name
ORDER BY edge_count DESC;

// Find all file names that have every one of their child strings tagged with a POS symbol
MATCH (pos:PartsOfSpeech)-[r:SUMMARIZES]->(np:NavigableParents)
WHERE np.file_name IN ["e6d285d80e2af44c_Quantitative_Engineer_Model_Implementation_Remote_Indeed_com.html"]

// Show job hunting activity since last day of work
MATCH (fn:FileNames)
WHERE
    ((fn.rejection_email_date <= date()) AND (fn.rejection_email_date >= date("2024-06-13"))) OR
    ((fn.opportunity_application_email_date <= date()) AND (fn.opportunity_application_email_date >= date("2024-06-13")))
RETURN
    fn.opportunity_application_email_date AS application_date,
    fn.rejection_email_date AS rejection_date,
    fn.percent_fit AS percent_fit,
    fn.file_name AS file_name,
    fn.posting_url AS posting_url
ORDER BY fn.percent_fit DESC;

// Count job hunting activity since last day of work
CALL {
    MATCH (fn:FileNames)
    WHERE ((fn.rejection_email_date <= date()) AND (fn.rejection_email_date >= date("2024-06-13")))
    RETURN
        fn.rejection_email_date AS action_date,
        0 AS application_count,
        COUNT(fn.rejection_email_date) AS rejection_count
    UNION
    MATCH (fn:FileNames)
    WHERE ((fn.opportunity_application_email_date <= date()) AND (fn.opportunity_application_email_date >= date("2024-06-13")))
    RETURN
        fn.opportunity_application_email_date AS action_date,
        COUNT(fn.opportunity_application_email_date) AS application_count,
        0 AS rejection_count
}
WITH action_date, SUM(application_count) AS total_applications, SUM(rejection_count) AS total_rejections
RETURN
    action_date,
    total_applications,
    total_rejections
ORDER BY action_date ASC;

// Unset the the percent fit for a specific file name
MATCH (fn:FileNames)
WHERE fn.file_name IN ["8293a1ad80a4160c_Data_Scientist_Remote_Indeed_com.html"]
SET
    fn.percent_fit = NULL
RETURN fn;

// Get job application links for jobs you should apply for
MATCH (fn:FileNames)
WHERE
    (fn.percent_fit >= 0.8) AND
    ((fn.is_closed IS NULL) OR (fn.is_closed = false)) AND
    ((fn.is_opportunity_application_emailed IS NULL) OR (fn.is_opportunity_application_emailed = false))
RETURN
    fn.percent_fit AS percent_fit,
    fn.file_name AS file_name,
    fn.posting_url AS posting_url
ORDER BY fn.percent_fit DESC;

// Regiater your application to a job
MATCH (fn:FileNames)
WHERE fn.file_name IN ["437d829a52879548_Machine_Learning_Engineer_Remote_Indeed_com.html"]
SET fn.is_opportunity_application_emailed = true, fn.opportunity_application_email_date = date()
RETURN fn;

// Show rejection info on selected postings
MATCH (fn:FileNames)
WHERE
    fn.file_name IN ["99ff2ff0f6339645_Data_Scientist_South_San_Francisco_CA_Indeed_com.html"]
    AND fn.opportunity_application_email_date IS NOT NULL
    AND fn.rejection_email_date IS NULL
RETURN
    fn.opportunity_application_email_date AS application_date,
    fn.file_name AS file_name,
    fn.posting_url AS posting_url,
    fn.rejection_email_text,
    fn.rejection_email_date,
    fn.is_closed
ORDER BY fn.opportunity_application_email_date DESC;

MATCH (fn:FileNames)
WHERE
    (fn.rejection_email_text IS NOT NULL)
    AND (fn.rejection_email_date IS NOT NULL)
SET fn.is_closed = true
RETURN fn;

MATCH (fn:FileNames)
WHERE
    fn.rejection_email_text IS NOT NULL
RETURN
    fn.percent_fit AS percent_fit,
    fn.rejection_email_text AS rejection_email_text,
    fn.file_name AS file_name,
    fn.opportunity_application_email_date AS application_date
ORDER BY
    fn.percent_fit DESC,
    fn.opportunity_application_email_date DESC;

MATCH (fn:FileNames)
WHERE
    (fn.opportunity_application_email_date = date("2023-03-01"))
RETURN fn;

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

MATCH (a)-[r:SUMMARIZES]->(b)
RETURN
    DISTINCT LABELS(b) AS b_type_name,
    COUNT(*) AS b_type_count;

MATCH (a)-[r:SUMMARIZES]->(b)
RETURN
    DISTINCT LABELS(a) AS a_type_name,
    COUNT(*) AS a_type_count;

MATCH (a)-[r]-(b)
RETURN
    DISTINCT TYPE(r) AS type_name,
    COUNT(*) AS type_count;

MATCH (fn:FileNames)
WHERE fn.file_name IN [""]
SET fn.percent_fit = 0.5
RETURN fn;

// Get all the duplicate file names
MATCH (f1:FileNames), (f2:FileNames)
WHERE f1.file_name = f2.file_name AND id(f1) < id(f2)
RETURN f1.file_name, collect(DISTINCT id(f1)), collect(DISTINCT id(f2))

// Get all node types that have the is_qualified property defined
CALL db.schema.nodeTypeProperties() YIELD nodeType, propertyName
WHERE propertyName = "is_qualified"
RETURN DISTINCT nodeType;

// Get all node types that have the file_name property defined
CALL db.schema.nodeTypeProperties() YIELD nodeType, propertyName
WHERE propertyName = "file_name"
RETURN DISTINCT nodeType as node_type;

// Get all relationship types
CALL db.relationshipTypes() YIELD relationshipType
RETURN DISTINCT relationshipType;

// Find all the relationship types in the graph with a file_name property
MATCH (nt1)-[r:NEXT]-(nt2)
WHERE exists(r.file_name)
RETURN DISTINCT labels(nt1) AS nt1_types;

// Find all properties with a value of "False"
CALL db.propertyKeys() YIELD propertyKey AS prop_name
MATCH (n)
WHERE n[prop_name] = "False"
WITH DISTINCT prop_name, labels(n)[0] AS node_name
RETURN prop_name, node_name;