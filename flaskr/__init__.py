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
        
        print('Load needed libraries and functions')
        t0 = time.time()
        nonlocal lru, crf
        
        # Insert at 1, 0 is the script path (or '' in REPL)
        sys.path.insert(1, 'py')

        print('Get the Neo4j driver')
        from storage import Storage
        s = Storage(
            data_folder_path=os.path.abspath('data'),
            saves_folder_path=os.path.abspath('saves')
        )

        from ha_utils import HeaderAnalysis
        ha = HeaderAnalysis(s=s, verbose=False)

        from scrape_utils import WebScrapingUtilities
        wsu = WebScrapingUtilities(
            s=s,
            secrets_json_path=os.path.abspath('data/secrets/jh_secrets.json')
        )
        uri = wsu.secrets_json['neo4j']['connect_url']
        user =  wsu.secrets_json['neo4j']['username']
        password = wsu.secrets_json['neo4j']['password']

        print('Get the neo4j object')
        from cypher_utils import CypherUtilities
        cu = CypherUtilities(
            uri=uri, user=user, password=password, driver=None, s=s, ha=ha
        )

        try:
            version_str = cu.driver.get_server_info().agent
            print(f'======== {version_str} ========')
        except ServiceUnavailable as e:
            print('You need to start Neo4j as a console')
            raise
        except Exception as e:
            print(f'{e.__class__}: {str(e).strip()}')
        
        from hc_utils import HeaderCategories
        hc = HeaderCategories(cu=cu, verbose=False)
        
        from lr_utils import LrUtilities
        lru = LrUtilities(ha=ha, cu=cu, hc=hc, verbose=False)
        
        from crf_utils import CrfUtilities
        crf = CrfUtilities(ha=ha, hc=hc, cu=cu, lru=lru, verbose=True)
        
        from section_utils import SectionUtilities
        su = SectionUtilities(s=s, ha=ha, wsu=wsu, cu=cu, crf=crf, verbose=False)
        
        duration_str = humanize.precisedelta(time.time() - t0, minimum_unit='seconds', format='%0.0f')
        winsound.Beep(freq, duration)
        print(f'Utility libraries created in {duration_str}')

        print('\nCheck if the lru has built its parts-of-speech logistic regression elements')
        t0 = time.time()
        if not hasattr(lru, 'POS_PREDICT_PERCENT_FIT_DICT'):
            lru.build_pos_logistic_regression_elements(sampling_strategy_limit=None, verbose=True)#6_400
        duration_str = humanize.precisedelta(time.time() - t0, minimum_unit='seconds', format='%0.0f')
        print(f'Parts-of-speech logistic regression elements built in {duration_str}')

        print('\nCheck if the crf has built its parts-of-speech classifier')
        t0 = time.time()
        if not hasattr(crf, 'pos_crf_predict_single'):
            crf.build_pos_conditional_random_field_elements(verbose=True)
        duration_str = humanize.precisedelta(time.time() - t0, minimum_unit='seconds', format='%0.0f')
        print(f'Parts-of-speech CRF elements built in {duration_str}')

        print('\nCheck if the lru has built its is-qualified classifier')
        t0 = time.time()
        if not hasattr(lru, 'ISQUALIFIED_LR'):
            lru.build_isqualified_logistic_regression_elements(sampling_strategy_limit=5_000, verbose=True)
        duration_str = humanize.precisedelta(time.time() - t0, minimum_unit='seconds', format='%0.0f')
        print(f'Is-qualified LR elements built in {duration_str}')

        print('\nCheck if the lru has retrained its is-header classifier')
        t0 = time.time()
        if not hasattr(lru, 'ISHEADER_PREDICT_PERCENT_FIT'):
            if not hasattr(lru, 'ISHEADER_LR'):
                lru.build_isheader_logistic_regression_elements(verbose=True)
            lru.retrain_isheader_classifier(verbose=True)
        duration_str = humanize.precisedelta(time.time() - t0, minimum_unit='seconds', format='%0.0f')
        print(f'Is-header classifier retrained in {duration_str}')

        winsound.Beep(freq, duration)
        print(f'\nLast run on {datetime.now()}')
    
    # Register the commands
    @app.route('/load_needed_libraries')
    def hello():
        load_needed_libraries()
        
        return 'Hello, World!'

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
        y_pred = lru.pos_lr_predict_single(navigable_parent)
        
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