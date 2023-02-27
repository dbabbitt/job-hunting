
#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



from functools import wraps
import sklearn_crfsuite

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
            self.ha = HeaderAnalysis()
        else:
            self.ha = ha
        if hc is None:
            self.hc = HeaderCategories()
        else:
            self.hc = hc
        from storage import Storage
        self.s = Storage()
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
            for file_name, feature_dict_list in HEADER_PATTERN_DICT.items():
                feature_tuple_list = [self.hc.get_feature_tuple(feature_dict, self.lru.pos_lr_predict_single) for feature_dict in feature_dict_list]
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

    #########################################
    ## Conditional Random Fields functions ##
    #########################################
    def retrain_pos_classifier(self, header_pattern_dict=None, verbose=False):
        
        # Get all the header pattern data
        if header_pattern_dict is None:
            header_pattern_dict = self.cu.create_header_pattern_dictionary(verbose=verbose)
        if verbose:
            print(f'I have {len(header_pattern_dict):,} hand-labeled parts-of-speech patterns in here')
        
        X_train = []
        y_train = []
        for file_name, feature_dict_list in header_pattern_dict.items():
            feature_tuple_list = [self.hc.get_feature_tuple(feature_dict, self.lru.pos_lr_predict_single) for feature_dict in feature_dict_list]
            pos_list = [feature_tuple[2] for feature_tuple in feature_tuple_list]
            y_train.append(pos_list)
            X_train.append(self.sent2features(feature_tuple_list))
        self.CRF = sklearn_crfsuite.CRF(algorithm='lbfgs', c1=0.1, c2=0.1, max_iterations=100, all_possible_transitions=True)
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


    def word2features(self, sent, i):
        from itertools import groupby
        null_element = 'plaintext'
        this_sent = sent[i]
        tag = this_sent[0]
        child_str = this_sent[1]
        postag = this_sent[2]

        features = {
            'bias': 1.0, 
            'child_str.pos_lr_predict_single': self.lru.pos_lr_predict_single(child_str), 
            'position': i+1, 
            'postag': postag, 
            'tag.basic_text_set': tag in self.cu.basic_text_set, 
            'tag.block_elements_set': tag in self.cu.block_elements_set, 
            'tag.document_body_elements_set': tag in self.cu.document_body_elements_set, 
            'tag.inline_elements_set': tag in self.cu.inline_elements_set, 
            'tag.lists_set': tag in self.cu.lists_set, 
            'tag.null_element': tag == null_element, 
            'tag.other_block_elements_set': tag in self.cu.other_block_elements_set, 
            'tag.phrase_elements_set': tag in self.cu.phrase_elements_set, 
            'tag.presentation_set': tag in self.cu.presentation_set, 
            'tag.section_headings_set': tag in self.cu.section_headings_set, 
        }
        if i > 0:
            tag1 = sent[i-1][0]
            postag1 = sent[i-1][2]
            features.update({
                '-1:postag': postag1, 
                '-1:previous==tag': tag1 == tag, 
                '-1:tag.basic_text_set': tag1 in self.cu.basic_text_set, 
                '-1:tag.block_elements_set': tag1 in self.cu.block_elements_set, 
                '-1:tag.document_body_elements_set': tag1 in self.cu.document_body_elements_set, 
                '-1:tag.inline_elements_set': tag1 in self.cu.inline_elements_set, 
                '-1:tag.lists_set': tag1 in self.cu.lists_set, 
                '-1:tag.null_element': tag1 == null_element, 
                '-1:tag.other_block_elements_set': tag1 in self.cu.other_block_elements_set, 
                '-1:tag.phrase_elements_set': tag1 in self.cu.phrase_elements_set, 
                '-1:tag.presentation_set': tag1 in self.cu.presentation_set, 
                '-1:tag.section_headings_set': tag1 in self.cu.section_headings_set, 
            })
        else:
            features['BOS'] = True

        if i < len(sent)-1:
            tag1 = sent[i+1][0]
            postag1 = sent[i+1][2]
            features.update({
                '+1:postag': postag1, 
                '+1:tag.basic_text_set': tag1 in self.cu.basic_text_set, 
                '+1:tag.block_elements_set': tag1 in self.cu.block_elements_set, 
                '+1:tag.document_body_elements_set': tag1 in self.cu.document_body_elements_set, 
                '+1:tag.inline_elements_set': tag1 in self.cu.inline_elements_set, 
                '+1:tag.lists_set': tag1 in self.cu.lists_set, 
                '+1:tag.null_element': tag1 == null_element, 
                '+1:tag.other_block_elements_set': tag1 in self.cu.other_block_elements_set, 
                '+1:tag.phrase_elements_set': tag1 in self.cu.phrase_elements_set, 
                '+1:tag.presentation_set': tag1 in self.cu.presentation_set, 
                '+1:tag.section_headings_set': tag1 in self.cu.section_headings_set, 
                '+1:tag==previous': tag1 == tag, 
            })
        else:
            features['EOS'] = True

        if i < len(sent)-2:
            tag1 = sent[i+1][0]
            tag2 = sent[i+2][0]
            postag2 = sent[i+2][2]
            labels_list = self.sent2labels(sent)[i:]
            consecutives_list = []
            for k, v in groupby(labels_list):
                consecutives_list.append((k, len(list(v))))
            if (consecutives_list[0][1] > 1):
                consecutive_next_tags = 0
            else:
                consecutive_next_tags = consecutives_list[1][1]
            features.update({
                '+2:postag': postag2, 
                '+2:tag.basic_text_set': tag2 in self.cu.basic_text_set, 
                '+2:tag.block_elements_set': tag2 in self.cu.block_elements_set, 
                '+2:tag.document_body_elements_set': tag2 in self.cu.document_body_elements_set, 
                '+2:tag.inline_elements_set': tag2 in self.cu.inline_elements_set, 
                '+2:tag.lists_set': tag2 in self.cu.lists_set, 
                '+2:tag.null_element': tag2 == null_element, 
                '+2:tag.other_block_elements_set': tag2 in self.cu.other_block_elements_set, 
                '+2:tag.phrase_elements_set': tag2 in self.cu.phrase_elements_set, 
                '+2:tag.presentation_set': tag2 in self.cu.presentation_set, 
                '+2:tag.section_headings_set': tag2 in self.cu.section_headings_set, 
                '+2:tag==previous': tag2 == tag1, 
                'tag.consecutive_next_tags': consecutive_next_tags, 
            })

        if i < len(sent)-3:
            tag2 = sent[i+2][0]
            tag3 = sent[i+3][0]
            postag3 = sent[i+3][2]
            features.update({
                '+3:postag': postag3, 
                '+3:tag.basic_text_set': tag3 in self.cu.basic_text_set, 
                '+3:tag.block_elements_set': tag3 in self.cu.block_elements_set, 
                '+3:tag.document_body_elements_set': tag3 in self.cu.document_body_elements_set, 
                '+3:tag.inline_elements_set': tag3 in self.cu.inline_elements_set, 
                '+3:tag.lists_set': tag3 in self.cu.lists_set, 
                '+3:tag.null_element': tag3 == null_element, 
                '+3:tag.other_block_elements_set': tag3 in self.cu.other_block_elements_set, 
                '+3:tag.phrase_elements_set': tag3 in self.cu.phrase_elements_set, 
                '+3:tag.presentation_set': tag3 in self.cu.presentation_set, 
                '+3:tag.section_headings_set': tag3 in self.cu.section_headings_set, 
                '+3:tag==previous': tag3 == tag2, 
            })

        return features

    def sent2features(self, sent):

        return [self.word2features(sent, i) for i in range(len(sent))]

    def sent2labels(self, sent):

        return [label for token, child_str, label in sent]

    def sent2tokens(self, sent):

        return [token for token, child_str, label in sent]