
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
WHERE fn.file_name IN ["a7f9b8bd279918d6_Junior_Data_Analyst_Engineer_Remote_Indeed_com.html"]
SET fn.is_opportunity_application_emailed = true, fn.opportunity_application_email_date = date()
RETURN fn;

MATCH (fn:FileNames)
WHERE fn.file_name IN ["5baf40a03d54df24_Data_Scientist_Senior_Remote_Indeed_com.html"]
SET
    fn.rejection_email_text = "Hi Dave – unfortunately this role has been filled.",
    fn.rejection_email_date = date(),
    fn.is_closed = true
RETURN fn;

MATCH (fn:FileNames)
WHERE
    (fn.rejection_email_text IS NOT NULL)
    AND (fn.rejection_email_date IS NOT NULL)
SET fn.is_closed = true
RETURN fn;

MATCH (fn:FileNames)
WHERE fn.file_name IN ["4671458_0_COUCHE_TARD_INC_Splunk_Data_Engineering_PM.html", "4671459_0_COUCHE_TARD_INC_Splunk_Senior_Developer.html"]
SET fn.is_closed = true
RETURN fn;

MATCH (np:NavigableParents)
WHERE (np.navigable_parent STARTS WITH "<li>7 - ")
SET
    np.is_header = 'False',
    np.is_task_scope = 'False',
    np.is_minimum_qualification = 'True',
    np.is_preferred_qualification = 'False',
    np.is_educational_requirement = 'False',
    np.is_legal_notification = 'False',
    np.is_other = 'False',
    np.is_corporate_scope = 'False',
    np.is_job_title = 'False',
    np.is_office_location = 'False',
    np.is_job_duration = 'False',
    np.is_supplemental_pay = 'False',
    np.is_interview_procedure = 'False',
    np.is_posting_date = 'False'
RETURN COUNT(*);

MATCH (fn:FileNames)
WHERE
    fn.file_name IN ["74a69d9b894f9ee2_Sr_Data_Scientist_Chicago_IL_Indeed_com.html", "74b13d50b9b61b64_Sr_Machine_Learning_Engineer_Chicago_IL_Indeed_com.html", "9021c8bf5ab1a757_Lead_Data_Scientist_Chicago_IL_Indeed_com.html", "9021c8bf5ab1a757_Lead_Machine_Learning_Data_Scientist_Chicago_IL_Indeed_com.html", "25806f11c7b36408_Sr_Data_Scientist_Chicago_IL_Indeed_com.html", "e7cafbf808c2ba69_Lead_Data_Scientist_Chicago_IL_Indeed_com.html"]
    AND fn.opportunity_application_email_date IS NOT NULL
RETURN
    fn.file_name AS file_name,
    fn.opportunity_application_email_date AS email_date
ORDER BY fn.opportunity_application_email_date DESC;

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
    (
        np.is_qualification = 'True'
        AND np.is_minimum_qualification IS NULL
        AND np.is_preferred_qualification IS NULL
        )
    OR (
        np.is_qualification = 'True'
        AND np.is_minimum_qualification = 'False'
        AND np.is_preferred_qualification = 'False'
        )
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
    np.is_qualification = 'True'
    AND np.is_minimum_qualification = 'False'
    AND np.is_preferred_qualification = 'False'
RETURN
    pos.pos_symbol AS pos_symbol,
    np.navigable_parent AS navigable_parent;

MATCH (ht:HeaderTags)-[r:SUMMARIZES]->(np:NavigableParents)
WITH ht, np, collect(r) AS summarizes
WHERE size(summarizes) > 1
RETURN ht, np, summarizes
LIMIT 1;

MATCH (fn:FileNames)
WHERE fn.file_name IN ["4712948_0_SYNEOS_HEALTH_Data_Governance_AD.html", "4712958_0_SYNEOS_HEALTH_Data_Governance_AM.html"]
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
    AND NOT (np.is_header = "True")
SET np.is_header = "True"
RETURN
    np.is_header AS is_header,
    np.navigable_parent AS navigable_parent;

// Fix HTML that really should be an interview procedure
MATCH (np:NavigableParents)
WHERE
    (np.navigable_parent =~ "^(<[^><]+>)?Learn more at .+$")
    AND NOT (np.is_interview_procedure = "True")
SET np.is_interview_procedure = "True"
RETURN
    np.is_header AS is_interview_procedure,
    np.navigable_parent AS navigable_parent;