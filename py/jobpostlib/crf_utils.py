
#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria

from . import nu, cu, slrcu, ssgdcu, scrfcu
from functools import wraps
import sklearn_crfsuite
import requests

class CrfUtilities(object):
    """Conditional Random Fields utilities class."""
    def __init__(
        self, verbose=False
    ):
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

    def get_pos_sgd_predict_single_from_api(self, child_str):
        data_dict = {'navigable_parent': child_str}
        response = requests.post(
            f'{self.flask_url}/pos_sgd_predict_single', json=data_dict
        )
        response_dict = response.json()
        
        return response_dict['y_pred']

    def get_pos_crf_predict_single_from_api(self, child_str):
        data_dict = {'navigable_parent': child_str}
        response = requests.post(
            f'{self.flask_url}/pos_crf_predict_single', json=data_dict
        )
        response_dict = response.json()
        
        return response_dict['y_pred']
    
    
    def get_pos_lr_predict_single_from_api(self, child_str):
        data_dict = {'navigable_parent': child_str}
        response = requests.post(
            f'{self.flask_url}/pos_lr_predict_single', json=data_dict
        )
        response_dict = response.json()
        
        return response_dict['y_pred']

    #########################################
    ## Conditional Random Fields functions ##
    #########################################
    def build_pos_conditional_random_field_elements(self, verbose=False):
        '''Train a model for each labeled POS symbol'''
        
        # Create the CRF model
        if nu and nu.pickle_exists('crf_CRF'):
            self.CRF = nu.load_object('crf_CRF')
        else:
            if nu and nu.pickle_exists('HEADER_PATTERN_DICT'):
                header_pattern_dict = nu.load_object('HEADER_PATTERN_DICT')
            else:
                header_pattern_dict = None
            self.retrain_pos_classifier(header_pattern_dict=header_pattern_dict, verbose=verbose)


    def retrain_pos_classifier(self, header_pattern_dict=None, verbose=False):

        # Get all the header pattern data
        if header_pattern_dict is None:
            header_pattern_dict = cu.create_header_pattern_dictionary(verbose=verbose)
        if verbose:
            from IPython.display import clear_output
            clear_output(wait=True)
            print(
                f'I have {len(header_pattern_dict):,}',
                'hand-labeled parts-of-speech patterns in here'
            )

        X_train = []
        y_train = []
        
        # Seek a SectionLRClassifierUtilities object
        if hasattr(slrcu, 'pos_predict_percent_fit_dict'):
            pos_lr_predict_single = slrcu.predict_single
            if verbose:
                print('slrcu.predict_single is now available')
        # elif self.is_flask_running():
            # pos_lr_predict_single = self.get_pos_lr_predict_single_from_api
        else:
            pos_lr_predict_single = None
        
        # Seek a SectionCRFClassifierUtilities object
        pos_crf_predict_single = scrfcu.predict_single
        if verbose: print('scrfcu.predict_single is now available')
        
        # Seek a SectionSGDClassifierUtilities object
        pos_sgd_predict_single = ssgdcu.predict_single
        if verbose: print('ssgdcu.predict_single is now available')
        
        from tqdm import tqdm
        di = tqdm(header_pattern_dict.items()) if verbose else header_pattern_dict.items()
        from . import hc
        for file_name, feature_dict_list in di:
            feature_tuple_list = [hc.get_feature_tuple(
                feature_dict, pos_lr_predict_single=pos_lr_predict_single,
                pos_crf_predict_single=pos_crf_predict_single,
                pos_sgd_predict_single=pos_sgd_predict_single
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
        nu.store_objects(crf_CRF=self.CRF, verbose=verbose)

    
    def word2features(self, feature_tuples_list, i):
        """
        This function works with the crf_CRF_20230402.pkl
        """
        from itertools import groupby
        null_element = 'plaintext'
        token_count = len(feature_tuples_list)
        this_feature_tuple = feature_tuples_list[i]
        this_tag = this_feature_tuple[0]
        child_str = this_feature_tuple[1]
        this_symbol = this_feature_tuple[2]
        # compiled_fdl = [
            # 'postag', 'child_str.pos_lr_predict_single',
            # 'child_str.pos_crf_predict_single', 'child_str.pos_sgd_predict_single', 'BOS',
            # '+1:postag', '+2:tag.basic_text_set', '+2:tag.inline_elements_set',
            # '+2:tag.lists_set', '+2:tag.null_element', '+2:tag.other_block_elements_set',
            # '+2:tag.presentation_set', '+2:tag.section_headings_set', '+2:tag==previous',
            # 'tag.consecutive_next_tags', '+3:tag.basic_text_set',
            # '+3:tag.block_elements_set', '+3:tag.document_body_elements_set',
            # '+3:tag.inline_elements_set', '+3:tag.lists_set', '+3:tag.null_element',
            # '+3:tag.other_block_elements_set', '+3:tag.phrase_elements_set',
            # '+3:tag.presentation_set', '+3:tag.section_headings_set', '+3:tag==previous'
        # ]
        
        features = {
            'position': i+1,
            'postag': this_symbol,
            'tag.null_element': this_tag == null_element,
        }
        for es in cu.elements_sets_list:
            feature_key = f'tag.{es}'
            # if feature_key in compiled_fdl:
            var_set = eval(f'cu.{es}')
            features.update({
                feature_key: this_tag in var_set,
            })

        # Seek a SectionLRClassifierUtilities object
        if hasattr(slrcu, 'pos_predict_percent_fit_dict'):
            features.update({
                'child_str.pos_lr_predict_single': slrcu.predict_single(child_str),
            })
        # elif self.is_flask_running():
            # features.update({
                # 'child_str.pos_lr_predict_single': self.get_pos_lr_predict_single_from_api(child_str),
            # })

        # Seek a SectionCRFClassifierUtilities object
        if hasattr(scrfcu, 'pos_symbol_crf'):
            features.update({
                'child_str.pos_crf_predict_single': scrfcu.predict_single(child_str),
            })

        # Seek a SectionSGDClassifierUtilities object
        features.update({
            'child_str.pos_sgd_predict_single': ssgdcu.predict_single(
                child_str
            ),
        })
        if i == 0:
            features['BOS'] = True
        if i == (token_count - 1):
            features['EOS'] = True
        
        # for word_offset in range(1, 4):
        for word_offset in range(-3, 4):
            if token_count > (word_offset + i) >= 0:
                previous_tag = feature_tuples_list[i+word_offset-1][0]
                offset_tag = feature_tuples_list[i+word_offset][0]
                offset_symbol = feature_tuples_list[i+word_offset][2]
                labels_list = self.sent2labels(feature_tuples_list)[i:]
                consecutives_list = []
                for k, v in groupby(labels_list):
                    consecutives_list.append((k, len(list(v))))
                consecutive_previous_tags = 0
                try:
                    consecutive_previous_tags = consecutives_list[1][1]
                except:
                    # print(token_count, word_offset, consecutives_list)
                    pass
                feature_key = f'{"+" if word_offset >= 0 else "-"}{abs(word_offset)}:postag'
                # if feature_key in compiled_fdl:
                features.update({
                    feature_key: offset_symbol,
                })
                feature_key = f'{"+" if word_offset >= 0 else "-"}{abs(word_offset)}:tag.null_element'
                # if feature_key in compiled_fdl:
                features.update({
                    feature_key: offset_tag == null_element,
                })
                feature_key = f'{"+" if word_offset >= 0 else "-"}{abs(word_offset)}:previous==tag'
                # if feature_key in compiled_fdl:
                features.update({
                    feature_key: offset_tag == this_tag,
                })
                features.update({
                    'tag.consecutive_previous_tags': consecutive_previous_tags,
                })
                for es in cu.elements_sets_list:
                    feature_key = f'{"+" if word_offset >= 0 else "-"}{abs(word_offset)}:tag.{es}'
                    # if feature_key in compiled_fdl:
                    var_set = eval(f'cu.{es}')
                    features.update({
                        feature_key: offset_tag in var_set,
                    })

        return features

    def sent2features(self, sent):

        return [self.word2features(sent, i) for i in range(len(sent))]

    def sent2labels(self, sent):

        return [label for token, child_str, label in sent]

    def sent2tokens(self, sent):

        return [token for token, child_str, label in sent]