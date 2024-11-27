#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



# From Anaconda Prompt (anaconda3), type:
# conda activate "C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\jh_env"; cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\tests; cls; python -m unittest test_flask_api.py

import unittest
import requests
import time

class TestFlaskAPI(unittest.TestCase):

    BASE_URL = 'http://127.0.0.1:5000/data'

    def test_temperature_values(self):
        # Allow some time for data generation
        time.sleep(5)
        response = requests.get(self.BASE_URL)
        data = response.json()
        temperature_values = data['temperature']
        
        # Check that we have 5 temperature values
        self.assertEqual(len(temperature_values), 5)
        
        # Check that each value is within the expected range
        for value in temperature_values:
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 90)

    def test_pressure_values(self):
        time.sleep(10)
        response = requests.get(self.BASE_URL)
        data = response.json()
        pressure_values = data['pressure']
        
        # Check that we have 5 pressure values
        self.assertEqual(len(pressure_values), 5)

        # Check that each value is within the expected range
        for value in pressure_values:
            self.assertGreaterEqual(value, 100)
            self.assertLessEqual(value, 200)

    def test_injecting_time_values(self):
        time.sleep(2)
        response = requests.get(self.BASE_URL)
        data = response.json()
        injecting_time_values = data['injecting_time']
        
        # Check that we have 3 injecting time values
        self.assertEqual(len(injecting_time_values), 3)

        # Check that each value is within the expected range
        for value in injecting_time_values:
            self.assertGreaterEqual(value, 0.2)
            self.assertLessEqual(value, 1.5)


if __name__ == '__main__':
    unittest.main()