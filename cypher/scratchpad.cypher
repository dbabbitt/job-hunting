
MATCH (fn:FileNames)
WHERE fn.file_name IN ["'b82af252adf198ab_Data_Scientist_US_Remote_Remote_Indeed_com.html'"]
SET fn.is_closed = true
RETURN fn;

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

MATCH (fn:FileNames)
WHERE fn.file_name IN ["99ff2ff0f6339645_Data_Scientist_South_San_Francisco_CA_Indeed_com.html"]
SET fn.is_opportunity_application_emailed = true, fn.opportunity_application_email_date = date()
RETURN fn;

MATCH (fn:FileNames)
WHERE
    fn.file_name IN ["99ff2ff0f6339645_Data_Scientist_South_San_Francisco_CA_Indeed_com.html"]
    AND fn.opportunity_application_email_date IS NOT NULL
    AND fn.rejection_email_date IS NULL
RETURN
    fn.opportunity_application_email_date AS email_date,
    fn.file_name AS file_name,
    fn.posting_url AS posting_url,
    fn.rejection_email_text,
    fn.rejection_email_date,
    fn.is_closed
ORDER BY fn.opportunity_application_email_date DESC;

MATCH (fn:FileNames)
WHERE fn.file_name IN ["99ff2ff0f6339645_Data_Scientist_South_San_Francisco_CA_Indeed_com.html"]
SET
    fn.rejection_email_text = "We recognize this news is disappointing, but we have made the decision not to move forward with your candidacy for the position at this time.",
    fn.rejection_email_date = date("2023-05-23"),
    fn.is_closed = true
RETURN fn;

MATCH (fn:FileNames)
WHERE
    (fn.rejection_email_text IS NOT NULL)
    AND (fn.rejection_email_date IS NOT NULL)
SET fn.is_closed = true
RETURN fn;

MATCH (np:NavigableParents)
WHERE (np.navigable_parent STARTS WITH "<li>7 - ")
SET
    np.is_header = false,
    np.is_task_scope = false,
    np.is_minimum_qualification = true,
    np.is_preferred_qualification = false,
    np.is_educational_requirement = false,
    np.is_legal_notification = false,
    np.is_other = false,
    np.is_corporate_scope = false,
    np.is_job_title = false,
    np.is_office_location = false,
    np.is_job_duration = false,
    np.is_supplemental_pay = false,
    np.is_interview_procedure = false,
    np.is_posting_date = false
RETURN COUNT(*);

MATCH (fn:FileNames)
WHERE
    fn.rejection_email_text IS NOT NULL
RETURN
    fn.percent_fit AS percent_fit,
    fn.rejection_email_text AS rejection_email_text,
    fn.file_name AS file_name,
    fn.opportunity_application_email_date AS email_date
ORDER BY
    fn.percent_fit DESC,
    fn.opportunity_application_email_date DESC;

MATCH (np1:NavigableParents)-[r:NEXT]->(np2:NavigableParents)
WHERE r.file_name = "654489b978b139f8_Sr_Engineers_SDET_Bellevue_WA_98006_Indeed_com.html"
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

MATCH (np:NavigableParents)
WHERE (np.is_qualification IS NOT NULL)
RETURN count(*);

MATCH (fn:FileNames)
WHERE (fn.opportunity_application_email_date IS NOT NULL)
SET fn.opportunity_application_email_date = date(fn.opportunity_application_email_date)
RETURN fn;

MATCH (fn:FileNames)
WHERE
    (fn.opportunity_application_email_date = date("2023-03-01"))
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
WHERE np.is_qualification = true
RETURN np.navigable_parent;

MATCH (np:NavigableParents {navigable_parent: "<li>GIS: 3 years (Required)</li>"})
SET np.is_minimum_qualification = true;

MATCH (np:NavigableParents {navigable_parent: "<li>Python: 10 years (Preferred)</li>"})
SET np.is_preferred_qualification = true;

MATCH (np:NavigableParents {navigable_parent: "Hope you are doing safe and fine amidst pandemic!"})
SET np.is_qualification = NULL;

//"<b>Have deep finance experience.</b>"
MATCH (np:NavigableParents)
WHERE
    (
        np.is_qualification = true
        AND np.is_minimum_qualification IS NULL
        AND np.is_preferred_qualification IS NULL
        )
    OR (
        np.is_qualification = true
        AND np.is_minimum_qualification = false
        AND np.is_preferred_qualification = false
        )
RETURN np.navigable_parent;

MATCH (np:NavigableParents {navigable_parent: "<b>based products and applications.</b>"})
SET np.is_qualification = NULL;

// Find the navigable parents that are "about the job" and what POS symbol they are tagged with
MATCH (pos:PartsOfSpeech)-[r:SUMMARIZES]->(np:NavigableParents)
WHERE
    np.navigable_parent CONTAINS "About the job"
RETURN
    pos.pos_symbol AS pos_symbol,
    np.navigable_parent AS navigable_parent;

MATCH (np:NavigableParents {navigable_parent: "<b>Have deep finance experience.</b>"})-[n:NEXT]->(:NavigableParents)
RETURN n
ORDER BY n.sequence_order;

MATCH (np:NavigableParents)-[r:NEXT]->(:NavigableParents)
WHERE
    np.is_header IS NULL
    AND np.is_task_scope IS NULL
    AND np.is_minimum_qualification IS NULL
    AND np.is_preferred_qualification IS NULL
    AND np.is_educational_requirement IS NULL
    AND np.is_legal_notification IS NULL
    AND np.is_other IS NULL
    AND np.is_corporate_scope IS NULL
    AND np.is_job_title IS NULL
    AND np.is_office_location IS NULL
    AND np.is_job_duration IS NULL
    AND np.is_supplemental_pay IS NULL
    AND np.is_interview_procedure IS NULL
    AND np.is_posting_date IS NULL
WITH
    r.file_name AS file_name,
    COUNT(r) AS edge_count,
    COUNT(np) AS np_count
RETURN np_count, edge_count, file_name
ORDER BY edge_count DESC;

MATCH (:NavigableParents)-[r:NEXT]->(:NavigableParents)
WHERE r.file_name = "212ea9dc068b2bf3_Data_Engineer_I_New_York_NY_Indeed_com.html"
DELETE r;

MATCH (np1:NavigableParents)-[r:NEXT]->(np2:NavigableParents)
WITH np1, np2, collect(r) AS nexts
WHERE size(nexts) > 1
RETURN np1, np2, nexts
LIMIT 1;

MATCH (ht:HeaderTags)-[r:SUMMARIZES]->(np:NavigableParents)
WITH ht, np, collect(r) AS summarizes
WHERE size(summarizes) > 1
RETURN ht, np, summarizes
LIMIT 1;

MATCH (np1:NavigableParents)-[r:NEXT]->(np2:NavigableParents)
WHERE r.file_name = "212ea9dc068b2bf3_Data_Engineer_I_New_York_NY_Indeed_com.html"
RETURN np1, r, np2;

MATCH (np1:NavigableParents)-[r:SUMMARIZES]->(np2:NavigableParents)
RETURN np1, r, np2;

MATCH (a)-[r:SUMMARIZES]->(np:NavigableParents)
RETURN
    DISTINCT LABELS(a) AS a_type_name,
    COUNT(*) AS a_type_count;

MATCH (np:NavigableParents)
WHERE
   NOT EXISTS {
        MATCH (:PartsOfSpeech)-[:SUMMARIZES]->(np)
    }
    AND NOT (
        np.is_header IS NULL
        AND np.is_task_scope IS NULL
        AND np.is_minimum_qualification IS NULL
        AND np.is_preferred_qualification IS NULL
        AND np.is_educational_requirement IS NULL
        AND np.is_legal_notification IS NULL
        AND np.is_other IS NULL
        AND np.is_corporate_scope IS NULL
        AND np.is_job_title IS NULL
        AND np.is_office_location IS NULL
        AND np.is_job_duration IS NULL
        AND np.is_supplemental_pay IS NULL
        AND np.is_interview_procedure IS NULL
        AND np.is_posting_date IS NULL
    )
RETURN
    COUNT(*) AS np_count;
    //np.navigable_parent AS navigable_parent;

MATCH (pos:PartsOfSpeech)-[r:SUMMARIZES]->(np:NavigableParents)
WITH pos, r, np, collect(pos) as nodes
WHERE size(nodes) > 1
RETURN pos, r, np;

MATCH (np:NavigableParents)
WHERE NOT EXISTS {
    MATCH (:PartsOfSpeech)-[:SUMMARIZES]->(np)
}
RETURN np.navigable_parent AS navigable_parent;

MATCH (a)-[r:SUMMARIZES]->(np:NavigableParents)
RETURN
    DISTINCT LABELS(a) AS a_type_name,
    COUNT(*) AS a_type_count;

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

MATCH (pos:PartsOfSpeech)-[r:SUMMARIZES]->(np:NavigableParents)
WHERE
    np.is_qualification = true
    AND np.is_minimum_qualification = false
    AND np.is_preferred_qualification = false
RETURN
    pos.pos_symbol AS pos_symbol,
    np.navigable_parent AS navigable_parent;

MATCH (ht:HeaderTags)-[r:SUMMARIZES]->(np:NavigableParents)
WITH ht, np, collect(r) AS summarizes
WHERE size(summarizes) > 1
RETURN ht, np, summarizes
LIMIT 1;

MATCH (fn:FileNames)
WHERE fn.file_name IN [""]
SET fn.percent_fit = 0.5
RETURN fn;

// Try to connect all unconnected child strings to their obvious parts-of-speech
MATCH (np:NavigableParents)
WHERE
   NOT EXISTS {
        MATCH (:PartsOfSpeech)-[:SUMMARIZES]->(np:NavigableParents)
    }
    AND NOT (
        np.is_header IS NULL
        AND np.is_task_scope IS NULL
        AND np.is_minimum_qualification IS NULL
        AND np.is_preferred_qualification IS NULL
        AND np.is_educational_requirement IS NULL
        AND np.is_legal_notification IS NULL
        AND np.is_other IS NULL
        AND np.is_corporate_scope IS NULL
        AND np.is_job_title IS NULL
        AND np.is_office_location IS NULL
        AND np.is_job_duration IS NULL
        AND np.is_supplemental_pay IS NULL
        AND np.is_interview_procedure IS NULL
        AND np.is_posting_date IS NULL
    )
WITH
    np.is_header AS np_is_header,
    np.is_task_scope AS np_is_task_scope,
    np.is_minimum_qualification AS np_is_minimum_qualification,
    np.is_preferred_qualification AS np_is_preferred_qualification,
    np.is_educational_requirement AS np_is_educational_requirement,
    np.is_legal_notification AS np_is_legal_notification,
    np.is_other AS np_is_other,
    np.is_corporate_scope AS np_is_corporate_scope,
    np.is_job_title AS np_is_job_title,
    np.is_office_location AS np_is_office_location,
    np.is_job_duration AS np_is_job_duration,
    np.is_supplemental_pay AS np_is_supplemental_pay,
    np.is_interview_procedure AS np_is_interview_procedure,
    np.is_posting_date AS np_is_posting_date
    MATCH
        (pos:PartsOfSpeech {
            is_header: np_is_header,
            is_task_scope: np_is_task_scope,
            is_minimum_qualification: np_is_minimum_qualification,
            is_preferred_qualification: np_is_preferred_qualification,
            is_educational_requirement: np_is_educational_requirement,
            is_legal_notification: np_is_legal_notification,
            is_other: np_is_other,
            is_corporate_scope: np_is_corporate_scope,
            is_job_title: np_is_job_title,
            is_office_location: np_is_office_location,
            is_job_duration: np_is_job_duration,
            is_supplemental_pay: np_is_supplemental_pay,
            is_interview_procedure: np_is_interview_procedure,
            is_posting_date: np_is_posting_date
        }),
        (np2:NavigableParents {
            is_header: np_is_header,
            is_task_scope: np_is_task_scope,
            is_minimum_qualification: np_is_minimum_qualification,
            is_preferred_qualification: np_is_preferred_qualification,
            is_educational_requirement: np_is_educational_requirement,
            is_legal_notification: np_is_legal_notification,
            is_other: np_is_other,
            is_corporate_scope: np_is_corporate_scope,
            is_job_title: np_is_job_title,
            is_office_location: np_is_office_location,
            is_job_duration: np_is_job_duration,
            is_supplemental_pay: np_is_supplemental_pay,
            is_interview_procedure: np_is_interview_procedure,
            is_posting_date: np_is_posting_date
        })
    //MERGE (pos)-[r:SUMMARIZES]->(np2)
    RETURN pos, np2
    LIMIT 1;

CALL db.schema.nodeTypeProperties() YIELD nodeType
RETURN DISTINCT nodeType;

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

// Get all the duplicate file names
MATCH (f1:FileNames), (f2:FileNames)
WHERE f1.file_name = f2.file_name AND id(f1) < id(f2)
RETURN f1.file_name, collect(DISTINCT id(f1)), collect(DISTINCT id(f2))

// Find quals that really should be headers
MATCH (qs:QualificationStrings)
WHERE
    (qs.qualification_str =~ "^.+:</[a-z]+>$")
RETURN qs.qualification_str AS qualification_str;

// Fix HTML that really should be headers
MATCH (np:NavigableParents)
WHERE
    (np.navigable_parent =~ "^.+:</[a-z]+>$")
    AND NOT (np.is_header = true)
SET np.is_header = true
RETURN
    np.is_header AS is_header,
    np.navigable_parent AS navigable_parent;

// Fix HTML that really should be an interview procedure
MATCH (np:NavigableParents)
WHERE
    (np.navigable_parent =~ "^(<[^><]+>)?Learn more at .+$")
    AND NOT (np.is_interview_procedure = true)
SET np.is_interview_procedure = true
RETURN
    np.is_header AS is_interview_procedure,
    np.navigable_parent AS navigable_parent;

// Get all the parts-of-speech relationships that haven`t been populated
MATCH (np:NavigableParents)
WHERE
    (NOT (np)<-[:SUMMARIZES]-(:PartsOfSpeech))
    AND (np.is_header IS NOT NULL)
    AND (np.is_task_scope IS NOT NULL)
    AND (np.is_minimum_qualification IS NOT NULL)
    AND (np.is_preferred_qualification IS NOT NULL)
    AND (np.is_legal_notification IS NOT NULL)
    AND (np.is_job_title IS NOT NULL)
    AND (np.is_office_location IS NOT NULL)
    AND (np.is_job_duration IS NOT NULL)
    AND (np.is_supplemental_pay IS NOT NULL)
    AND (np.is_educational_requirement IS NOT NULL)
    AND (np.is_interview_procedure IS NOT NULL)
    AND (np.is_corporate_scope IS NOT NULL)
    AND (np.is_posting_date IS NOT NULL)
    AND (np.is_other IS NOT NULL)
RETURN np;

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

// Get all possible paths
MATCH path = (np:NavigableParents)-[rels:NEXT*]->(np2:NavigableParents)

// Check that the property is uniform and
// the first node is a minqual header
WHERE
    np.is_minimum_qualification = true AND
    np.is_header = true AND
    ALL(r in rels WHERE rels[0]["file_name"] = r.file_name)
RETURN rels[0]["file_name"] AS file_name;

// Set all the HTML that are strangely marked as a header to NULL
MATCH (np:NavigableParents)
WHERE
    (np.is_header IS NOT NULL)
    AND (np.is_task_scope IS NULL)
    AND (np.is_minimum_qualification IS NULL)
    AND (np.is_preferred_qualification IS NULL)
    AND (np.is_legal_notification IS NULL)
    AND (np.is_job_title IS NULL)
    AND (np.is_office_location IS NULL)
    AND (np.is_job_duration IS NULL)
    AND (np.is_supplemental_pay IS NULL)
    AND (np.is_educational_requirement IS NULL)
    AND (np.is_interview_procedure IS NULL)
    AND (np.is_corporate_scope IS NULL)
    AND (np.is_posting_date IS NULL)
    AND (np.is_other IS NULL)
SET np.is_header = NULL
RETURN COUNT(np);

// Define the input date range as a string
WITH "Sunday, 04/02/2023 - Saturday, 04/08/2023" AS date_range
// Split the input string into two parts, one for the start date and one for the end date
WITH split(date_range, " - ") AS dates
// Split the start and end dates into their components
WITH
    split(dates[0], ", ") AS start_components,
    split(dates[1], ", ") AS end_components
// Reassemble the start date components into a
// format that the date() function can recognize
WITH
    [item in split(start_components[1], "/") | toInteger(item)] AS start_components,
    [item in split(end_components[1], "/") | toInteger(item)] AS end_components
// Convert the integer date parts into Neo4j date objects using the date() function
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
// Find all FileNames nodes and filter them by opportunity_application_email_date property
MATCH (fn:FileNames)
WHERE
    (fn.opportunity_application_email_date >= date_start) AND
    (fn.opportunity_application_email_date <= date_end)
// Return the filtered nodes
RETURN fn;

// Find all properties with a name like "is_qual"
MATCH (np:NavigableParents)
UNWIND keys(np) AS property
WITH np, property
WHERE property =~ "^is_.*qual.+$"
RETURN DISTINCT property;

// Record the recruiter screen calender invite date
MATCH (fn:FileNames)
WHERE fn.file_name IN ["8fc0ed7481ff426b_Data_Scientist_Gainesville_FL_Indeed_com.html"]
SET fn.recruiter_screen_date = date("2023-03-23")
RETURN fn;

// Delete all but one of the duplicate HeaderTags
// nodes based on the header_tag property
MATCH (ht:HeaderTags)
WITH
    ht.header_tag AS header_tag,
    collect(ht) AS nodes,
    count(*) AS tag_count
WHERE tag_count > 1
UNWIND tail(nodes) AS node
DETACH DELETE node;

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

// Replace "True" with true and "False" with false
MATCH (n)
SET n.property = CASE n.property
  WHEN "False" THEN false
  WHEN "True" THEN true
  ELSE n.property
END;