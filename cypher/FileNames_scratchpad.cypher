
// Update File Names node with phone screen date
MATCH (fn:FileNames)
WHERE fn.file_name IN ["Decision_Scientist_Machine_Learning_NLP_LLM_with_Indeed_com.html"]
SET fn.is_recruiter_screen_completed = true, fn.recruiter_screen_completion_date = date()
RETURN fn;

// Update File Names node with rejection email text
MATCH (fn:FileNames)
WHERE fn.file_name IN ["68cf2d512fc03664_Security_Analyst_CSIRT_Remote_Indeed_com.html"]
SET
    fn.rejection_email_text = "While this is never easy news to share, we've decided not to move forward with your candidacy.",
    fn.rejection_email_date = date("2024-09-09"),
    fn.is_closed = true
RETURN fn;

// 1. Define the input date range as a string
WITH "Sunday, 09/01/2024 - Saturday, 09/07/2024" AS date_range
// 2. Split the input string into two parts, one for the start date and one for the end date
WITH split(date_range, " - ") AS dates
// 3. Split the start and end dates into their components
WITH
    split(dates[0], ", ") AS start_components,
    split(dates[1], ", ") AS end_components
// 4. Reassemble the start date components into a format that the date() function can recognize
WITH
    [item in split(start_components[1], "/") | toInteger(item)] AS start_components,
    [item in split(end_components[1], "/") | toInteger(item)] AS end_components
// 5. Convert the integer date parts into Neo4j date objects using the date() function
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
// 6. Find all FileNames nodes and filter them by opportunity_application_email_date property
MATCH (fn:FileNames)
WHERE
    (fn.opportunity_application_email_date >= date_start) AND
    (fn.opportunity_application_email_date <= date_end)
// 7. Return the filtered nodes
RETURN
    fn.file_name AS file_name,
    fn.opportunity_application_email_date AS opportunity_application_email_date,
    fn.posting_url AS posting_url,
    fn.recruiter_screen_completion_date AS recruiter_screen_completion_date,
    fn.rejection_email_date AS rejection_email_date,
    fn.tech_interview_completion_date AS tech_interview_completion_date;

// Show rejection info on selected postings
MATCH (fn:FileNames)
WHERE
    (fn.file_name IN ["0a518ebbd8a94252_Data_Engineer_New_York_NY_Indeed_com.html", "0e312efb8c3d8fe8_Senior_Data_Engineer_New_York_NY_Indeed_com.html", "6HkrJ4RwkS27gfCFq_5hZQ_Data_Infrastructure_Engineer_Headway_United_States_Remote.html", "4532e7ff248454cc_Senior_Data_Engineer_Remote_Indeed_com.html"]) AND
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

// Step 1: Get all unique relationship types
MATCH ()-[r]->()
WITH DISTINCT type(r) AS relType
// Step 2: Check each relationship type for the 'file_name' property
MATCH ()-[r]->()
WHERE type(r) = relType AND exists(r.file_name)
WITH DISTINCT relType
// Step 3: Return the relationship types that have the 'file_name' property
RETURN relType AS relationshipType

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

// Rename the technical_interview_date properties in the FileNames nodes
// to technical_interview_dates and convert their date values into a list of one date
MATCH (fn:FileNames)
WHERE fn.technical_interview_date IS NOT NULL
SET fn.technical_interview_dates = [fn.technical_interview_date]
REMOVE fn.technical_interview_date;

// Record the recruiter screen calender invite date
MATCH (fn:FileNames)
WHERE fn.file_name IN ["8fc0ed7481ff426b_Data_Scientist_Gainesville_FL_Indeed_com.html"]
SET fn.recruiter_screen_completion_date = date("2023-03-23")
RETURN fn;

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