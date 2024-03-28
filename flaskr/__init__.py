#!/usr/bin/env python
# coding: utf-8

# Soli Deo gloria

from flask import Flask, redirect, render_template, request, url_for, jsonify
from datetime import datetime
from neo4j.exceptions import ServiceUnavailable
import humanize
import os
import sys
import time
import warnings
import winsound
import openai

warnings.filterwarnings('ignore')
duration = 1000  # milliseconds
freq = 880  # Hz

def create_app(test_config=None):
    '''Create and configure an instance of the Flask application.'''
    openai.api_key = os.getenv('OPENAI_API_KEY')

    # Relative filenames for loading the config are assumed to be
    # relative to the instance path instead of the application root
    app = Flask('flaskr', instance_relative_config=True)
    app.config.from_mapping(
        # A default secret that should be overridden by instance config
        SECRET_KEY='dev',
        # Store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    config_obj = app.config

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.update(test_config)

    # Ensure the instance folder exists
    os.makedirs(name=app.instance_path, exist_ok=True)
    
    lru = crf = None
    
    def load_needed_libraries():
        nonlocal lru, crf
        import sys
        sys.path.insert(1, '../py')
        from jobpostlib import (crf, cu, datetime, duration, hau, hc, humanize, ihu, lru, nu, osp, scrfcu, slrcu, ssgdcu, su, t0, time, winsound, wsu)
        import os
        from pandas import DataFrame
        
        freq = 990
        
        print('\nCheck if the slrcu has built its parts-of-speech logistic regression elements')
        t1 = time.time()
        if not hasattr(slrcu, 'pos_predict_percent_fit_dict'):
            slrcu.build_pos_logistic_regression_elements(sampling_strategy_limit=None, verbose=True)
        duration_str = humanize.precisedelta(time.time() - t1, minimum_unit='seconds', format='%0.0f')
        print(f'Parts-of-speech logistic regression elements built in {duration_str}')

        print('\nCheck if the scrfcu has built its parts-of-speech conditional random field elements')
        t1 = time.time()
        if not hasattr(scrfcu, 'pos_symbol_crf'):
            scrfcu.build_pos_conditional_random_field_elements(verbose=True)
        duration_str = humanize.precisedelta(time.time() - t1, minimum_unit='seconds', format='%0.0f')
        print(f'Parts-of-speech conditional random field elements built in {duration_str}')
        
        print('\nCheck if the ssgdcu has built its parts-of-speech stochastic gradient decent elements')
        t1 = time.time()
        if not hasattr(ssgdcu, 'pos_predict_percent_fit_dict'):
            ssgdcu.build_pos_stochastic_gradient_descent_elements(
                sampling_strategy_limit=None, verbose=True
            )
        duration_str = humanize.precisedelta(time.time() - t1, minimum_unit='seconds', format='%0.0f')
        print(f'Parts-of-speech stochastic gradient decent elements built in {duration_str}')

        winsound.Beep(freq, duration)
        print(f'\nLast run on {datetime.now()}')
        duration_str = humanize.precisedelta(
            time.time() - t0, minimum_unit='seconds', format='%0.0f'
        )
        print(f'Running load_needed_libraries took {duration_str} to complete')
    
    def train_pos_classifier():
        nonlocal crf
        t0 = time.time()
        load_needed_libraries()
        
        print('\nBuild the conditional random field classifier')
        t1 = time.time()
        crf.build_pos_conditional_random_field_elements(verbose=True)
        duration_str = humanize.precisedelta(time.time() - t1, minimum_unit='seconds', format='%0.0f')
        print(f'POS classifier trained in {duration_str}')
        
        winsound.Beep(freq, duration)
        print(f'\nLast run on {datetime.now()}')
        duration_str = humanize.precisedelta(
            time.time() - t0, minimum_unit='seconds', format='%0.0f'
        )
        print(f'Running train_pos_classifier took {duration_str} to complete')
    
    # Register the load_needed_libraries command
    @app.route('/load_needed_libraries')
    def load_needed_libraries_command():
        t0 = time.time()
        load_needed_libraries()
        duration_str = humanize.precisedelta(
            time.time() - t0, minimum_unit='seconds', format='%0.0f'
        )
        
        return f'Running the load_needed_libraries command took {duration_str} to complete'
    
    # Register the train_pos_classifier command
    @app.route('/train_pos_classifier')
    def train_pos_classifier_command():
        t0 = time.time()
        train_pos_classifier()
        duration_str = humanize.precisedelta(
            time.time() - t0, minimum_unit='seconds', format='%0.0f'
        )
        
        return f'Running the train_pos_classifier command took {duration_str} to complete'

    # Define a new endpoint with a string parameter
    @app.route('/new_endpoint/<string_parameter>')
    def new_endpoint(string_parameter):

        # Access the value of the string parameter and implement as a message dictionary
        data = {'message': string_parameter}

        # Return a JSON response
        return jsonify(data)
    
    @app.route('/pos_crf_predict_single', methods=['POST'])
    def pos_crf_predict_single():
        
        # Code to handle JSON data
        data_dict = request.get_json()
        navigable_parent = data_dict['navigable_parent']
        y_pred = crf.pos_crf_predict_single(navigable_parent)
        
        response = {'y_pred': y_pred}
        
        return jsonify(response)
    
    @app.route('/pos_lr_predict_single', methods=['POST'])
    def pos_lr_predict_single():
        
        # Code to handle JSON data
        data_dict = request.get_json()
        navigable_parent = data_dict['navigable_parent']
        
        y_pred = slrcu.predict_single(navigable_parent)
        
        response = {'y_pred': y_pred}
        
        return jsonify(response)

    @app.route('/', methods=('GET', 'POST'))
    def index():
        if request.method == 'POST':
            animal = request.form['animal']
            response = openai.Completion.create(
                model='text-davinci-003',
                prompt=generate_prompt(animal),
                temperature=0.6,
            )
            return redirect(url_for('index', result=response.choices[0].text))

        result = request.args.get('result')

        return render_template('index.html', result=result)

    def generate_prompt(animal):
        prompt_str = 'Suggest three names for an animal that is a superhero.'
        prompt_str += '\n\n\n\nAnimal: Cat\n\nNames: Captain Sharpclaw, Agent Fluffball, The Incredible Feline'
        prompt_str += '\n\nAnimal: Dog\n\nNames: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot\n\nAnimal: {}\n\nNames:'
        
        return prompt_str.format(animal.capitalize())

    return app