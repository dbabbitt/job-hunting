#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



# From Anaconda Prompt (anaconda3), type:
# conda activate "C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\jh_env"; cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\py; cls; python quals_queue_flask_api.py

from flask import Flask, jsonify, request
from queue import Queue

app = Flask(__name__)

# Initialize a queue to store qualification strings
qualification_queue = Queue()

@app.route('/add_qualification', methods=['POST'])
def add_qualification():
    data = request.json
    qualification_str = data.get('qualification_str')
    if qualification_str:
        qualification_queue.put(qualification_str)
        return jsonify({'status': 'success', 'message': 'Qualification string added to queue'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'No qualification string provided'}), 400

@app.route('/get_qualification', methods=['GET'])
def get_qualification():
    if not qualification_queue.empty():
        qualification_str = qualification_queue.get()
        return jsonify({'qualification_str': qualification_str}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Queue is empty'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)