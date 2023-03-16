
#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



from functools import wraps
import sklearn_crfsuite
import requests

def with_lru_pos_context(init_func):
    """
    Wraps a init function so that it's guaranteed to be executed
    with the script's Logistic Regression Part-of-speech context.
    """

    def _decorator(*args, **kwargs):
        from lr_utils import LrUtilities
        args[0].lru = LrUtilities(ha=kwargs['ha'], hc=kwargs['hc'], cu=kwargs['cu'], verbose=kwargs['verbose'])
        # args[0].lru.build_pos_logistic_regression_elements()

        return init_func(*args, **kwargs)

    return wraps(init_func)(_decorator)

class CrfUtilities(object):
    """Conditional Random Fields utilities class."""

    @with_lru_pos_context
    def __init__(self, ha=None, hc=None, cu=None, lru=None, verbose=False):
        if ha is None:
            from storage import Storage
            s = Storage()
            self.ha = HeaderAnalysis(s=s, verbose=False)
        else:
            self.ha = ha
        self.s = ha.s
        if hc is None:
            self.hc = HeaderCategories()
        else:
            self.hc = hc
        if cu is None:
            from scrape_utils import WebScrapingUtilities
            wsu = WebScrapingUtilities()
            uri = wsu.secrets_json['neo4j']['connect_url']
            user =  wsu.secrets_json['neo4j']['username']
            password = wsu.secrets_json['neo4j']['password']

            from cypher_utils import CypherUtilities
            self.cu = CypherUtilities(uri=uri, user=user, password=password, driver=None, s=self.s, ha=self.ha)
        else:
            self.cu = cu
        self.lru = lru

        # Build the CRF elements
        if self.s.pickle_exists('CRF'):
            self.CRF = self.s.load_object('CRF')
        else:
            self.CRF = sklearn_crfsuite.CRF(algorithm='lbfgs', c1=0.1, c2=0.1, max_iterations=100, all_possible_transitions=True)
            HEADER_PATTERN_DICT = self.s.load_object('HEADER_PATTERN_DICT')
            if verbose:
                print(f'I have {len(HEADER_PATTERN_DICT):,} hand-labeled parts-of-speech patterns in here')
            X_train = []
            y_train = []
            if hasattr(self.lru, 'POS_PREDICT_PERCENT_FIT_DICT'):
                pos_lr_predict_single = self.lru.pos_lr_predict_single
            else:
                pos_lr_predict_single = self.get_pos_lr_predict_single_from_api
            if hasattr(self, 'pos_crf_predict_single'):
                pos_crf_predict_single = self.pos_crf_predict_single
            else:
                pos_crf_predict_single = self.get_pos_crf_predict_single_from_api
            for file_name, feature_dict_list in HEADER_PATTERN_DICT.items():
                feature_tuple_list = [self.hc.get_feature_tuple(
                    feature_dict, pos_lr_predict_single=pos_lr_predict_single,
                    pos_crf_predict_single=pos_crf_predict_single
                ) for feature_dict in feature_dict_list]
                pos_list = [feature_tuple[2] for feature_tuple in feature_tuple_list]
                y_train.append(pos_list)
                X_train.append(self.sent2features(feature_tuple_list))
            try:
                self.CRF.fit(X_train, y_train)
            except Exception as e:
                print(f'Error in CrfUtilities init trying to self.CRF.fit(X_train, y_train): {str(e).strip()}')
                with open('../saves/txt/X_train.txt', 'w', encoding='utf-8') as f:
                    print(X_train, file=f)
                with open('../saves/txt/y_train.txt', 'w', encoding='utf-8') as f:
                    print(y_train, file=f)
                raise
            self.s.store_objects(CRF=self.CRF, verbose=verbose)
        self.flask_port = 5000
        self.flask_url = f'http://localhost:{self.flask_port}'

    #################################################
    ## Application Programming Interface functions ##
    #################################################
    def is_flask_running(self, url=None):
        return_bool = False
        if url is None:
            url = self.flask_url
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return_bool = True
            else:
                return_bool = False
        except requests.exceptions.RequestException:
            return_bool = False
        
        return return_bool

    def get_pos_crf_predict_single_from_api(self, child_str):
        data_dict = {'navigable_parent': child_str}
        response = requests.post(f'{self.flask_url}/pos_crf_predict_single', json=data_dict)
        response_dict = response.json()
        
        return response_dict['y_pred']
    
    
    def get_pos_lr_predict_single_from_api(self, child_str):
        data_dict = {'navigable_parent': child_str}
        response = requests.post(f'{self.flask_url}/pos_lr_predict_single', json=data_dict)
        response_dict = response.json()
        
        return response_dict['y_pred']

    #########################################
    ## Conditional Random Fields functions ##
    #########################################
    def build_pos_conditional_random_field_elements(
        self, sampling_strategy_limit=None, verbose=False
    ):
        
        # Get the labeled training data
        cypher_str = '''
            // Filter for NavigableParents nodes with an unambiguous SUMMARIZES relationship
            MATCH (np:NavigableParents)
            WHERE size((np)<-[:SUMMARIZES]-(:PartsOfSpeech)) = 1

            // Find all NavigableParents nodes in the graph with an incoming SUMMARIZES relationship to a PartsOfSpeech node
            WITH np
            MATCH (np)<-[r:SUMMARIZES]-(pos:PartsOfSpeech)

            // Return the navigable parent and its parts-of-speech symbol
            RETURN
                pos.pos_symbol AS pos_symbol,
                np.navigable_parent AS navigable_parent;'''
        row_objs_list = []
        with self.cu.driver.session() as session:
            row_objs_list = session.write_transaction(self.cu.do_cypher_tx, cypher_str)
        from pandas import DataFrame
        pos_df = DataFrame(row_objs_list)
        
        # Rebalance the data with the sampling strategy limit
        if sampling_strategy_limit is not None:
            pos_df = self.lru.rebalance_data(pos_df, name_column='navigable_parent', value_column='pos_symbol', sampling_strategy_limit=sampling_strategy_limit, verbose=verbose)
        
        # Define features to be used in the CRF model
        def word2features(sent, i):
            word = sent[i][0]
            postag = sent[i][1]
            features = {
                'word': word,
                'postag': postag
            }

            return features
        def sent2features(sent):

            return [word2features(sent, i) for i in range(len(sent))]
        def sent2labels(pos_symbol, sent):

            return [pos_symbol] * len(sent)
        
        # Sentences to parse
        sentences_list = pos_df.navigable_parent.tolist()
        if verbose:
            print(f'I have {len(sentences_list):,} labeled parts of speech in here')
        
        # Create the tokenizer
        import re
        HTML_SCANNER_REGEX = re.compile(r'</?\w+|\w+[#\+]*|:|\.|\?')
        def html_regex_tokenizer(corpus):

            return [match.group() for match in re.finditer(HTML_SCANNER_REGEX, corpus)]
        
        # Tokenize the sentences
        tokens_list = [html_regex_tokenizer(sentence) for sentence in sentences_list]
        
        # Get the parts of speech
        from nltk import pos_tag
        pos_tags_list = [pos_tag(tokens) for tokens in tokens_list]
        
        # Labels to apply
        pos_symbols_list = pos_df.pos_symbol.tolist()
        
        # Prepare the training and test data
        X = [sent2features(pos_tags) for pos_tags in pos_tags_list]
        y = [sent2labels(pos_symbol, pos_tag) for pos_tag, pos_symbol in zip(pos_tags_list, pos_symbols_list)]
        
        # Create the CRF model
        self.pos_symbol_crf = sklearn_crfsuite.CRF()
        
        # Train the model
        self.pos_symbol_crf.fit(X, y)
        
        # Predict the labels for the input data
        def predict_pos_symbol(navigable_parent):
            y_pred = navigable_parent
            tokens_list = [html_regex_tokenizer(navigable_parent)]
            if tokens_list != [[]]:
                pos_tags_list = [pos_tag(tokens) for tokens in tokens_list]
                X = [sent2features(pos_tags) for pos_tags in pos_tags_list]
                y_pred = self.pos_symbol_crf.predict(X)[0][0]

            return y_pred
        self.pos_crf_predict_single = predict_pos_symbol


    def retrain_pos_classifier(self, header_pattern_dict=None, verbose=False):

        # Get all the header pattern data
        if header_pattern_dict is None:
            header_pattern_dict = self.cu.create_header_pattern_dictionary(verbose=verbose)
        if verbose:
            print(f'I have {len(header_pattern_dict):,} hand-labeled parts-of-speech patterns in here')

        X_train = []
        y_train = []
        if hasattr(self.lru, 'POS_PREDICT_PERCENT_FIT_DICT'):
            pos_lr_predict_single = self.lru.pos_lr_predict_single
        else:
            pos_lr_predict_single = self.get_pos_lr_predict_single_from_api
        if hasattr(self, 'pos_crf_predict_single'):
            pos_crf_predict_single = self.pos_crf_predict_single
        else:
            pos_crf_predict_single = self.get_pos_crf_predict_single_from_api
        for file_name, feature_dict_list in header_pattern_dict.items():
            feature_tuple_list = [self.hc.get_feature_tuple(
                feature_dict, pos_lr_predict_single=pos_lr_predict_single,
                pos_crf_predict_single=pos_crf_predict_single
            ) for feature_dict in feature_dict_list]
            pos_list = [feature_tuple[2] for feature_tuple in feature_tuple_list]
            y_train.append(pos_list)
            X_train.append(self.sent2features(feature_tuple_list))
        self.CRF = sklearn_crfsuite.CRF(
            algorithm='lbfgs', c1=0.1, c2=0.1, max_iterations=100,
            all_possible_transitions=True
        )
        try:
            if verbose:
                print(f'Training the Conditional Random Fields model with {len(y_train):,} parts-of-speech labels')
            self.CRF.fit(X_train, y_train)
        except Exception as e:
            print(f'Error in CrfUtilities init trying to self.CRF.fit(X_train, y_train): {str(e).strip()}')
            with open('../saves/txt/X_train.txt', 'w', encoding='utf-8') as f:
                print(X_train, file=f)
            with open('../saves/txt/y_train.txt', 'w', encoding='utf-8') as f:
                print(y_train, file=f)
            raise
        self.s.store_objects(CRF=self.CRF, verbose=verbose)
        if verbose:
            print('Retraining complete')


    def retrain_pos_classifier_from_dictionary(self, verbose=False):

        # Get all the header pattern data
        if self.s.pickle_exists('HEADER_PATTERN_DICT'):
            header_pattern_dict = self.s.load_object('HEADER_PATTERN_DICT')
        else:
            header_pattern_dict = None

        self.retrain_pos_classifier(header_pattern_dict=header_pattern_dict, verbose=verbose)

    
    def word2features(self, feature_tuples_list, i):
        from itertools import groupby
        null_element = 'plaintext'
        this_feature_tuple = feature_tuples_list[i]
        child_str = this_feature_tuple[1]
        this_pos = this_feature_tuple[2]
        
        features = {
            'postag': this_pos,
        }
        if hasattr(self.lru, 'POS_PREDICT_PERCENT_FIT_DICT'):
            features.update({
                'child_str.pos_lr_predict_single': self.lru.pos_lr_predict_single(child_str),
            })
        else:
            features.update({
                'child_str.pos_lr_predict_single': self.get_pos_lr_predict_single_from_api(child_str),
            })
        if hasattr(self, 'pos_crf_predict_single'):
            features.update({
                'child_str.pos_crf_predict_single': self.pos_crf_predict_single(child_str),
            })
        else:
            features.update({
                'child_str.pos_crf_predict_single': self.get_pos_crf_predict_single_from_api(child_str),
            })
        if i > 0:
            previous_tag = feature_tuples_list[i-1][0]
            previous_pos = feature_tuples_list[i-1][2]
            features.update({
                '-1:postag': previous_pos,
                '-1:tag.basic_text_set': previous_tag in self.cu.basic_text_set,
                '-1:tag.inline_elements_set': previous_tag in self.cu.inline_elements_set,
                '-1:tag.null_element': previous_tag == null_element,
                '-1:tag.other_block_elements_set': previous_tag in self.cu.other_block_elements_set,
                '-1:tag.section_headings_set': previous_tag in self.cu.section_headings_set,
            })
        else:
            features['BOS'] = True

        if i < len(feature_tuples_list)-1:
            next_pos = feature_tuples_list[i+1][2]
            features.update({
                '+1:postag': next_pos,
            })
        else:
            features['EOS'] = True

        if i < len(feature_tuples_list)-2:
            next_tag = feature_tuples_list[i+1][0]
            third_tag = feature_tuples_list[i+2][0]
            labels_list = self.sent2labels(feature_tuples_list)[i:]
            consecutives_list = []
            for k, v in groupby(labels_list):
                consecutives_list.append((k, len(list(v))))
            if (consecutives_list[0][1] > 1):
                consecutive_next_tags = 0
            else:
                consecutive_next_tags = consecutives_list[1][1]
            features.update({
                '+2:tag.basic_text_set': third_tag in self.cu.basic_text_set,
                '+2:tag.inline_elements_set': third_tag in self.cu.inline_elements_set,
                '+2:tag.lists_set': third_tag in self.cu.lists_set,
                '+2:tag.null_element': third_tag == null_element,
                '+2:tag.other_block_elements_set': third_tag in self.cu.other_block_elements_set,
                '+2:tag.presentation_set': third_tag in self.cu.presentation_set,
                '+2:tag.section_headings_set': third_tag in self.cu.section_headings_set,
                '+2:tag==previous': third_tag == next_tag,
                'tag.consecutive_next_tags': consecutive_next_tags,
            })

        if i < len(feature_tuples_list)-3:
            third_tag = feature_tuples_list[i+2][0]
            fourth_tag = feature_tuples_list[i+3][0]
            features.update({
                '+3:tag.basic_text_set': fourth_tag in self.cu.basic_text_set,
                '+3:tag.block_elements_set': fourth_tag in self.cu.block_elements_set,
                '+3:tag.document_body_elements_set': fourth_tag in self.cu.document_body_elements_set,
                '+3:tag.inline_elements_set': fourth_tag in self.cu.inline_elements_set,
                '+3:tag.lists_set': fourth_tag in self.cu.lists_set,
                '+3:tag.null_element': fourth_tag == null_element,
                '+3:tag.other_block_elements_set': fourth_tag in self.cu.other_block_elements_set,
                '+3:tag.phrase_elements_set': fourth_tag in self.cu.phrase_elements_set,
                '+3:tag.presentation_set': fourth_tag in self.cu.presentation_set,
                '+3:tag.section_headings_set': fourth_tag in self.cu.section_headings_set,
                '+3:tag==previous': fourth_tag == third_tag,
            })

        return features

    def sent2features(self, sent):

        return [self.word2features(sent, i) for i in range(len(sent))]

    def sent2labels(self, sent):

        return [label for token, child_str, label in sent]

    def sent2tokens(self, sent):

        return [token for token, child_str, label in sent]