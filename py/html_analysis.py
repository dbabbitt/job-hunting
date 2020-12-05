
from IPython.display import HTML, display
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import pylab
import re

import storage
s = storage.Storage()

HTML_SCANNER_REGEX = re.compile(r'</?\w+|\w+[#\+]*|:|\.|\?')
def html_regex_tokenizer(corpus):
    
    return [match.group() for match in re.finditer(HTML_SCANNER_REGEX, corpus)]

QUALS_SCANNER_REGEX = re.compile(r'\b[1-9a-zA-Z][0-9a-zA-Z]*( *[#\+]{1,2}|\b)')
def quals_regex_tokenizer(corpus):
    
    return [match.group() for match in re.finditer(QUALS_SCANNER_REGEX, corpus)]

LT_REGEX = re.compile(r'\s+<')
GT_REGEX = re.compile(r'>\s+')
def clean_html_str(html_obj):
    html_str = str(html_obj)
    html_str = html_str.strip()
    html_str = LT_REGEX.sub('<', html_str)
    html_str = GT_REGEX.sub('>', html_str)
    
    return html_str

#CLF_NAME = 'LdaModel'
CLF_NAME = 'LogisticRegression'
def predict_percent_fit(navigable_parents_list):
    cs_cv_vocab = s.load_object('cs_cv_vocab')
    CS_CV = CountVectorizer(vocabulary=cs_cv_vocab)
    CS_CV._validate_vocabulary()
    CS_TT = s.load_object('CS_TT')
    CHILD_STR_CLF = s.load_object('child_str_clf')
    CRF = s.load_object('CRF')
    y_predict_proba_list = []
    for navigable_parent in navigable_parents_list:
        if(CLF_NAME == 'LdaModel'):
            X_test = HEADERS_DICTIONARY.doc2bow(html_regex_tokenizer(navigable_parent))
            result_list = LDA[X_test]
            if len(result_list) == 1:
                result_tuple = result_list[0]
            elif len(result_list) == 2:
                result_tuple = result_list[1]
                
            # Assume it's the probability of the smaller topic
            y_predict_proba = 1.0 - result_tuple[1]
        
        else:
            X_test = CS_TT.transform(CS_CV.transform(navigable_parents_list)).toarray()
            y_predict_proba = CHILD_STR_CLF.predict_proba(X_test)
        y_predict_proba_list.append(y_predict_proba)
    
    return y_predict_proba_list

def get_navigable_children(tag, result_list=[]):
    if type(tag) is not NavigableString:
        for child_tag in tag.children:
            result_list = get_navigable_children(child_tag, result_list)
    else:
        base_str = clean_html_str(tag)
        if base_str:
            tag_str = clean_html_str(tag.parent)
            if tag_str.count('<') > 2:
                tag_str = base_str
            result_list.append(tag_str)
    
    return result_list

SAVES_HTML_FOLDER = os.path.join(s.saves_folder, 'html')
def get_child_strs_from_file(file_name):
    child_strs_list = []
    file_path = os.path.join(SAVES_HTML_FOLDER, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        html_str = f.read()
        job_soup = BeautifulSoup(html_str, 'lxml')
        body_soup = job_soup.find_all(name='body')[0]
        child_strs_list = get_navigable_children(body_soup, [])
    
    return child_strs_list

CMAP = pylab.cm.get_cmap('coolwarm')
def html2text(html_str, prob_float):
    html_str = html_str.replace('<', '&lt;').replace('>', '&gt;')
    hex_str = '%02x%02x%02x' % CMAP(X=prob_float, bytes=True)[:-1]
    html_str = f'<span style="color:#{hex_str}">{html_str}</span>'
    
    return html_str