#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



# From Anaconda Prompt (anaconda3), type:
# conda activate "C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\jh_env"; cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\tests; cls; python -m unittest test_dash_app.py

import unittest
from dash.testing.application_runners import ProcessRunner
from dash.testing.browser import Browser
from selenium.webdriver.common.by import By

import sys
import os.path as osp
executable_path = sys.executable
scripts_folder = osp.join(osp.dirname(executable_path), 'Scripts')
py_folder = osp.abspath(osp.join(os.pardir, 'py')); ffmpeg_folder = r'C:\ffmpeg\bin'
if (scripts_folder not in sys.path): sys.path.insert(1, scripts_folder)
if (py_folder not in sys.path): sys.path.insert(1, py_folder)
if (ffmpeg_folder not in sys.path): sys.path.insert(1, ffmpeg_folder)

class TestDashApp(unittest.TestCase):
    def setUp(self):
        self.runner = ProcessRunner()
        # self.runner.tmp_app_path = '../py/data_visualization_dash_app.py'

    def tearDown(self):
        # Stop the Dash app server after tests
        self.runner.stop()

    def test_temperature_chart(self):
        import data_visualization_dash_app
        with self.runner.start(app_module='../py/data_visualization_dash_app.py') as dash:
            dash.wait_for_element('#temperature-card')
            temperature_card = dash.find_element('#temperature-card')
            self.assertIn('Temperature (°C)', temperature_card.text)

    def test_pressure_chart(self):
        import data_visualization_dash_app
        with self.runner.start(app_module='../py/data_visualization_dash_app.py') as dash:
            dash.wait_for_element('#pressure-card')
            pressure_card = dash.find_element('#pressure-card')
            self.assertIn('Pressure (psi)', pressure_card.text)

    def test_injecting_time_display(self):
        import data_visualization_dash_app
        with self.runner.start(app_module='../py/data_visualization_dash_app.py') as dash:
            dash.wait_for_element('#injecting-time-card')
            injecting_time_card = dash.find_element('#injecting-time-card')
            self.assertIn('Injecting Time:', injecting_time_card.text)

    def test_layout_structure(self):
        import data_visualization_dash_app
        with self.runner.start(app_module='../py/data_visualization_dash_app.py') as dash:
            row_div = dash.find_element(By.CSS_SELECTOR, 'div[style*="display: flex"]')
            self.assertIsNotNone(row_div)

if __name__ == '__main__':
    unittest.main()