#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



# From Anaconda Prompt (anaconda3), type:
# conda activate "C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\jh_env"; cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\py; cls; python data_generation_flask_api.py

from flask import Flask, jsonify
import random
import time
import threading

app = Flask(__name__)

# Global variables to store the latest values
temperature_values = []
pressure_values = []
injecting_time_values = []

def generate_data():
    global temperature_values, pressure_values, injecting_time_values
    while True:
        # Generate temperature values
        temperature_values = [random.uniform(0, 90) for _ in range(5)]
        time.sleep(5)

        # Generate pressure values
        pressure_values = [random.uniform(100, 200) for _ in range(5)]
        time.sleep(10)

        # Generate injecting time values
        injecting_time_values = [random.uniform(0.2, 1.5) for _ in range(3)]
        time.sleep(2)

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify({
        'temperature': temperature_values,
        'pressure': pressure_values,
        'injecting_time': injecting_time_values
    })

if __name__ == '__main__':
    # Start the data generation in a separate thread
    threading.Thread(target=generate_data, daemon=True).start()
    app.run(debug=True, port=5000)