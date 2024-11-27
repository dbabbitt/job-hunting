#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



# From Anaconda Prompt (anaconda3), type:
# conda activate "C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\jh_env"; cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\py; cls; python unscored_quals_flask_api.py

from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# Sample qualification strings
qualification_strings = {
    "short": "R",
    "long": (
        ", OR have at least 1 year of specialized experience equivalent to the GL-9 level which is defined as experience in, "
        "or related to planning and conducting complex criminal investigations to determine violations of Federal laws and regulations; "
        "collecting and assembling facts to identify logical conclusion; gathering, analyzing, and evaluating evidence or data; "
        "conducting interviews and interrogations; making arrests; conducting searches and seizures; taking responsibility for own actions "
        "and those of team members to ensure the goals and deadlines for the team are met; partnering with or leveraging networks or "
        "relationships from outside the organization, experience managing complex projects including setting priorities and determining "
        "resource requirements; OR a combination of specialized experience, as described above, and related graduate level education, "
        "beyond the first full year of doctoral level study"
    )
}

@app.route('/get_qualification', methods=['GET'])
def get_qualification():
    # q_type = request.args.get('type', 'short')  # default to 'short'
    # qualification_str = qualification_strings.get(q_type, qualification_strings['short'])
    
    # Cypher for unset or missing qualification strings
    quals_list, file_name = lru.infer_from_hunting_dataframe(fitness_threshold=3/4, verbose=False)
    quals_str = '", "'.join(quals_list)
    cypher_str = f'''
        // List of qualification strings to check
        WITH ["{quals_str}"] AS inputList
        
        // Match nodes with qualification strings in the list
        MATCH (qs:QualificationStrings)
        WHERE qs.qualification_str IN inputList
        
        // Collect existing qualification strings
        WITH inputList, collect(qs.qualification_str) AS existingStrings
        
        // Find strings that are not in the database
        UNWIND inputList AS qual
        WITH qual, existingStrings
        WHERE NOT qual IN existingStrings
        
        RETURN qual AS missingQualificationStrings
        
        UNION
        
        // Get all the unset qual strings from the list
        WITH ["{quals_str}"] AS inputList
        MATCH (qs:QualificationStrings)
        WHERE qs.qualification_str IN inputList AND qs.is_qualified IS NULL
        RETURN qs.qualification_str AS missingQualificationStrings;'''
    # pyperclip.copy(cypher_str)
    row_objs_list = []
    with cu.driver.session() as session:
        row_objs_list = session.write_transaction(cu.do_cypher_tx, cypher_str)
    assert row_objs_list, "You are not getting any qualification strings"
    qualification_strings_df = DataFrame(row_objs_list)
    # print(qualification_strings_df.shape)
    # display(qualification_strings_df)
    qualification_str = random.choice(qualification_strings_df.missingQualificationStrings)
    
    return jsonify({'qualification_str': qualification_str})

if __name__ == '__main__':
    app.run(debug=True, port=5000)