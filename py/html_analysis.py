
#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



import pandas as pd
from storage import Storage
from functools import wraps

s = Storage()

def with_test_context(func):
    """Wraps a callback in print statements:
    
    @with_test_context
    def needs_decorator(self):
        print('Needs a decorator')
    """
    
    def decorator(*args, **kwargs):
        crf = args[0]
        print([f'crf.{fn}' for fn in dir(crf) if not fn.startswith('_')])
        print([f'args.{fn}' for fn in args])
        print([f'{k}: "{v}"' for k, v in kwargs.items()])
        func(*args, **kwargs)

    return decorator

def with_test_init_context(init_func):
    """Wraps an class init function in print statements:
    
    @with_test_init_context
    def __init_(self):
        print('Needs a decorator')
    """
    
    def _decorator(*args, **kwargs):
        crf = args[0]
        print([f'crf.{fn}' for fn in dir(crf) if not fn.startswith('_')])
        print([f'args.{fn}' for fn in args])
        print([f'{k}: "{v}"' for k, v in kwargs.items()])
        return init_func(*args, **kwargs)

    return wraps(init_func)(_decorator)

def with_lru_pos_context(init_func):
    """
    Wraps a init function so that it's guaranteed to be executed
    with the script's Logistic Regression Part-of-speech context.
    """
    
    def _decorator(*args, **kwargs):
        from lr_utils import LrUtilities
        args[0].lru = LrUtilities(ha=kwargs['ha'], hc=kwargs['hc'], cu=kwargs['cu'], verbose=kwargs['verbose'])
        # args[0].slrcu.build_pos_logistic_regression_elements()
        return init_func(*args, **kwargs)

    return wraps(init_func)(_decorator)

class LdaUtilities(object):
    """Latent Dirichlet Allocation utilities class."""

    def __init__(self, ha=None, hc=None, cu=None, verbose=False):
        if ha is None:
            self.ha = HeaderAnalysis()
        else:
            self.ha = ha
        if hc is None:
            self.hc = HeaderCategories()
        else:
            self.hc = hc
        if cu is None:
            import cypher_utils
            self.cu = cypher_utils.CypherUtilities()
        else:
            self.cu = cu
        self.verbose = verbose

        # Build the LDA elements
        if not s.pickle_exists('NAVIGABLE_PARENT_IS_HEADER_DICT'):
            self.cu.build_child_strs_list_dictionary(verbose=verbose)
        self.NAVIGABLE_PARENT_IS_HEADER_DICT = s.load_object('NAVIGABLE_PARENT_IS_HEADER_DICT')
        self.stopwords_list = ['U', 'A', 'S', 'a', '1', 'u', 's', 'to', 'my', 'by', 'an', 'we', '00', 'or', 'as', 're', 'in', 'be', 'on', 'of', 'do', 'is', '19', 'any', 'out', 'for', 'the', 'are', 'and', 'long', 'each', 'have', 'with', 'more', 'will', 'into', 'that', 'this', 'your', 'from', 'their', 'class', 'about', 'other', 'place', '.']
        self.tokenized_sents_list = self.get_tokenized_sents_list()

        if s.pickle_exists('LDA_DICTIONARY'):
            self.LDA_DICTIONARY = s.load_object('LDA_DICTIONARY')
        else:
            self.build_dictionary(verbose=verbose)

        if s.pickle_exists('LDA_CORPUS'):
            self.LDA_CORPUS = s.load_object('LDA_CORPUS')
        else:
            self.build_corpus(verbose=verbose)

        if s.pickle_exists('TOPIC_MODEL'):
            self.TOPIC_MODEL = s.load_object('TOPIC_MODEL')
            
            # You'll have to eyeball this to get the dictionary correct
            self.topic_dict = {0: 'O', 1: 'H'}
            
        else:
            self.build_topic_model(verbose=verbose)
            self.topic_dict = {}
        
        if s.pickle_exists('HEADERS_DICTIONARY'):
            self.HEADERS_DICTIONARY = s.load_object('HEADERS_DICTIONARY')
        else:
            self.build_headers_dictionary()
        
        if s.pickle_exists('HEADERS_CORPUS'):
            self.HEADERS_CORPUS = s.load_object('HEADERS_CORPUS')
        else:
            self.build_headers_corpus()
        
        if s.pickle_exists('HEADERS_TOPIC_MODEL'):
            self.HEADERS_TOPIC_MODEL = s.load_object('HEADERS_TOPIC_MODEL')
            
            # You'll have to eyeball this to get the dictionary correct
            topic_dict = {0: 'O-SP', 1: 'O-TS', 2: 'O-SP'}
            
        else:
            self.build_lda()
            topic_dict = {}
        
        self.lda_predict_single = self.build_lda_predict_single()
        self.lda_predict_percent = self.build_lda_predict_percent()

    ###########################################
    ## Latent Dirichlet Allocation functions ##
    ###########################################

    def get_tokenized_sents_list(self):

        # Build model with tokenized words
        sents_list = list(self.NAVIGABLE_PARENT_IS_HEADER_DICT.keys())
        tokenized_sents_list = [self.ha.html_regex_tokenizer(sent_str) for sent_str in sents_list]
        
        # Remove stop words
        for i in reversed(range(len(tokenized_sents_list))):
            for j in reversed(range(len(tokenized_sents_list[i]))):
                if tokenized_sents_list[i][j] in self.stopwords_list:
                    del tokenized_sents_list[i][j]

        return tokenized_sents_list

    def build_dictionary(self, verbose=False):

        # Create a corpus from a list of texts
        from gensim.corpora.dictionary import Dictionary
        self.LDA_DICTIONARY = Dictionary(self.tokenized_sents_list)
        self.LDA_DICTIONARY.filter_extremes(no_below=100, no_above=0.5, keep_n=8_500, keep_tokens=[':', '<b', '</b'])
        s.store_objects(LDA_DICTIONARY=self.LDA_DICTIONARY, verbose=verbose)

    def build_headers_dictionary(self):
        
        # Create a corpus from a list of texts
        tokenized_sents_list = self.get_tokenized_sents_list()
        from gensim.corpora.dictionary import Dictionary
        self.HEADERS_DICTIONARY = Dictionary(tokenized_sents_list)
        # self.HEADERS_DICTIONARY.filter_extremes(no_below=5, no_above=0.5, keep_n=100000, keep_tokens=None)
        s.store_objects(HEADERS_DICTIONARY=self.HEADERS_DICTIONARY)

    def build_corpus(self, verbose=False):

        # Create a corpus from a list of texts
        self.LDA_CORPUS = [self.LDA_DICTIONARY.doc2bow(tag_str) for tag_str in self.tokenized_sents_list]

        s.store_objects(LDA_CORPUS=self.LDA_CORPUS, verbose=verbose)

    def build_headers_corpus(self, verbose=False):
        
        # Create a corpus from a list of texts
        tokenized_sents_list = self.get_tokenized_sents_list()
        self.HEADERS_CORPUS = [self.HEADERS_DICTIONARY.doc2bow(tag_str) for tag_str in tokenized_sents_list]
        
        s.store_objects(HEADERS_CORPUS=self.HEADERS_CORPUS, verbose=verbose)

    def build_topic_model(self, num_topics=2, chunksize=50, passes=75, alpha=None, decay=0.6, iterations=29, gamma_threshold=1e-10, 
                          minimum_probability=0.001, verbose=False):
        import numpy as np

        # Train the model on the corpus
        id2word = {v: k for k, v in self.LDA_DICTIONARY.token2id.items()}
        if num_topics is None:
            num_topics = self.get_pos_count(verbose=verbose)

        # Get ratio of headers to non-headers
        if alpha is None:
            import numpy as np
            cypher_str = """
                MATCH (np:NavigableParents {is_header: true})
                RETURN COUNT(np.navigable_parent) AS header_count;"""
            is_header_df = pd.DataFrame(self.cu.get_execution_results(self.cursor, cypher_str))
            header_count = is_header_df.header_count.squeeze()
            cypher_str = """
                MATCH (np:NavigableParents {is_header: false})
                RETURN COUNT(np.navigable_parent) AS nonheader_count;"""
            is_nonheader_df = pd.DataFrame(self.cu.get_execution_results(self.cursor, cypher_str))
            nonheader_count = is_nonheader_df.nonheader_count.squeeze()
            nonheader_fraction = nonheader_count/(header_count + nonheader_count)
            header_fraction = header_count/(header_count + nonheader_count)
            alpha = np.array([nonheader_fraction, header_fraction], dtype=np.float32)

        from gensim.models.ldamodel import LdaModel
        self.TOPIC_MODEL = LdaModel(corpus=self.LDA_CORPUS, num_topics=num_topics, id2word=id2word, chunksize=chunksize, passes=passes, 
                                    alpha=alpha, decay=decay, iterations=iterations, gamma_threshold=gamma_threshold, 
                                    minimum_probability=minimum_probability)
        s.store_objects(TOPIC_MODEL=self.TOPIC_MODEL, verbose=verbose)

    def build_lda(self, verbose=False):
        
        # Get the parts-of-speech count to use as number of topics
        cypher_str = '''
            MATCH (pos:PartsOfSpeech)
            UNWIND pos.pos_symbol as s
            RETURN count(DISTINCT s) AS num_topics;'''
        num_topics = self.cu.get_execution_results(cypher_str, verbose=verbose)[0]['num_topics']
        
        # Train the model on the corpus
        id2word = {v: k for k, v in self.HEADERS_DICTIONARY.token2id.items()}
        from gensim.models.ldamodel import LdaModel
        self.HEADERS_TOPIC_MODEL = LdaModel(corpus=self.HEADERS_CORPUS, num_topics=num_topics, id2word=id2word, passes=4, 
                                            alpha='auto', eta='auto')
        s.store_objects(HEADERS_TOPIC_MODEL=self.HEADERS_TOPIC_MODEL)

    def build_lda_predict_single(self):

        # Define a predictor
        def lda_predict_single(sent_str):
            tokens_list = self.ha.html_regex_tokenizer(sent_str)
            X_test = self.LDA_DICTIONARY.doc2bow(tokens_list)
            result_list = sorted(self.TOPIC_MODEL[X_test], key=lambda x: x[1], reverse=False)
            topic_number = result_list[0][0]

            return self.topic_dict[topic_number]

        return lda_predict_single

    def build_lda_predict_percent(self):
        
        # Define a predictor
        def predict_percent_fit(navigable_parent):
            X_test = self.HEADERS_DICTIONARY.doc2bow(self.ha.html_regex_tokenizer(navigable_parent))
            result_list = self.HEADERS_TOPIC_MODEL[X_test]
            result_list = sorted(result_list, key=lambda x: x[1], reverse=True)
            result_tuple = result_list[0]

            # Just return the topic number
            y_predict_proba = result_tuple[0]

            return y_predict_proba
        
        return predict_percent_fit

    def get_pos_count(self, verbose=False):

        # Get the parts-of-speech count to use as number of topics
        cypher_str = 'SELECT pos_symbol, pos_explanation FROM PartsOfSpeech'
        pos_df = pd.DataFrame(self.cu.get_execution_results(cypher_str, verbose=False))
        cypher_prefix = """
                MATCH (np:NavigableParents {is_header: '"""
        self.pos_symbols_list = []
        for pos_symbol in pos_df.pos_symbol:
            if pos_symbol.startswith('H-'):
                cypher_str = cypher_prefix + "True', "
            elif pos_symbol.startswith('O-'):
                cypher_str = cypher_prefix + "False', "
            if pos_symbol.endswith('-TS'):
                cypher_str += "is_task_scope: true"
            elif pos_symbol.endswith('-RQ'):
                cypher_str += "is_minimum_qualification]: true"
            elif pos_symbol.endswith('-PQ'):
                cypher_str += "is_preferred_qualification]: true"
            elif pos_symbol.endswith('-LN'):
                cypher_str += "is_legal_notification]: true"
            elif pos_symbol.endswith('-JT'):
                cypher_str += "is_job_title]: true"
            elif pos_symbol.endswith('-OL'):
                cypher_str += "is_office_location]: true"
            elif pos_symbol.endswith('-JD'):
                cypher_str += "is_job_duration]: true"
            elif pos_symbol.endswith('-SP'):
                cypher_str += "is_supplemental_pay]: true"
            elif pos_symbol.endswith('-ER'):
                cypher_str += "is_educational_requirement]: true"
            elif pos_symbol.endswith('-IP'):
                cypher_str += "is_interview_procedure]: true"
            elif pos_symbol.endswith('-CS'):
                cypher_str += "is_corporate_scope]: true"
            elif pos_symbol.endswith('-PD'):
                cypher_str += "is_posting_date]: true"
            elif pos_symbol.endswith('-O'):
                cypher_str += "is_other]: true"
            cypher_str += '})\nRETURN COUNT(np) AS row_count'
            count_df = pd.DataFrame(self.cu.get_execution_results(cypher_str, verbose=False))
            if count_df.row_count.squeeze() > 0:
                self.pos_symbols_list.append(pos_symbol)
        num_topics = len(self.pos_symbols_list)

        return num_topics

class ElementAnalysis(object):
    """Element analysis class."""

    def __init__(self, ha=None, hc=None, verbose=False):
        if ha is None:
            from ha_utils import HeaderAnalysis
            self.ha = HeaderAnalysis(verbose=verbose)
        else:
            self.ha = ha
        if hc is None:
            from hc_utils import HeaderCategories
            self.hc = HeaderCategories(cu=None, verbose=verbose)
        else:
            self.hc = hc
        self.verbose = verbose

    def get_idx_list(self, items_list, item_str):
        item_count = items_list.count(item_str)
        idx_list = []
        idx = -1
        while len(idx_list) < item_count:
            idx = items_list.index(item_str, idx+1)
            idx_list.append(idx)

        return idx_list
    
    def get_rq_section_from_tuples(self, consecutives_list):
        for rq_initial_idx, pos_tuple in enumerate(consecutives_list):
            if pos_tuple[0].split('-')[1] == 'RQ':
                break
        for rq_final_idx, pos_tuple in enumerate(consecutives_list[::-1]):
            if pos_tuple[0].split('-')[1] == 'RQ':
                break
        rq_final_idx = len(consecutives_list) - rq_final_idx
        
        return consecutives_list[rq_initial_idx:rq_final_idx]
    
    def display_basic_requirements(self, child_strs_list):
        consecutives_list, pos_list = su.find_basic_quals_section_indexes(child_strs_list)
        rq_idx_list = self.get_idx_list(pos_list, 'H-RQ')

        # Display the Requirements sections in their own HTML
        if len(rq_idx_list):
            consecutives_idx_list = self.get_idx_list(consecutives_list, ('H-RQ', 1))
            from IPython.display import HTML, display
            for rq_idx, consecutives_idx in zip(rq_idx_list, consecutives_idx_list):
                o_count = consecutives_list[consecutives_idx+1][1]
                display(HTML('<br />'.join(child_strs_list[rq_idx:rq_idx+o_count+1])))

    def display_reqs_from_url(self, page_url):
        import requests
        from itertools import groupby

        site_page = requests.get(url=page_url)
        body_soup = self.ha.get_body_soup(site_page.content)
        child_strs_list = self.ha.get_navigable_children(body_soup, [])
        self.display_basic_requirements(child_strs_list)

    #####################
    ## Other functions ##
    #####################