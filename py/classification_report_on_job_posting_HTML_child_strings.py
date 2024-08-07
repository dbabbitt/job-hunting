#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



# From Anaconda Prompt (anaconda3), type:
# conda activate "C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\jh_env"
# cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\py
# cls
# python classification_report_on_job_posting_HTML_child_strings.py

# From Ubuntu WSL, type:
# conda activate "/mnt/c/Users/daveb/OneDrive/Documents/GitHub/job-hunting/jh_env"; cd /mnt/c/Users/daveb/OneDrive/Documents/GitHub/job-hunting/py; clear; python.exe classification_report_on_job_posting_HTML_child_strings.py
# TODO: Replace humanize with a linux replacement


from jobpostlib import (datetime, nu, humanize, time)
from pandas import DataFrame
from sklearn.metrics import classification_report
from sklearn.preprocessing import MultiLabelBinarizer
from tqdm import tqdm
from transformers import BertForSequenceClassification, BertTokenizer
import torch

# 1. Data Preparation:
#    - Ensuring my dataset consists of HTML text snippets with their corresponding parent tags.

if nu.pickle_exists('file_tags_mapping'):
    file_tags_mapping = nu.load_object('file_tags_mapping')
model_path = '../saves/models/sequence_classification.model'
tokenizer_path = '../saves/tokenizers/sequence_classification.tokenizer'

# Now that I've trained and saved my model and tokenizer, I can use them for inference on new data. Here's how I load and use my saved model and tokenizer:
print('Compute the classification report')

# 1. First, I load the saved model and tokenizer:

# Load the saved model
model = BertForSequenceClassification.from_pretrained(model_path)

# Load the saved tokenizer
tokenizer = BertTokenizer.from_pretrained(tokenizer_path)

# Move the model to GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Set the model to evaluation mode
model.eval()


# 2. I create a function to predict the label for a given text:
reverse_mapping = {v: k for k, v in file_tags_mapping.items()}
def predict_label(text, max_length=128):
    
    # Tokenize the input text
    inputs = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=max_length,
        padding='max_length',
        truncation=True,
        return_attention_mask=True,
        return_tensors='pt'
    )
    
    # Move inputs to the same device as the model
    input_ids = inputs['input_ids'].to(device)
    attention_mask = inputs['attention_mask'].to(device)
    
    # Get the model's prediction
    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.logits
    
    # Get the predicted class
    predicted_class = torch.argmax(logits, dim=1).item()
    
    # Map the predicted class back to its label
    predicted_label = reverse_mapping[predicted_class]
    
    return predicted_label

# Prepare the actual and predicted data; use tqdm for a progress bar
t1 = time.time()
part_of_speech_dict = pos_html_strs_df.set_index('text').pos_symbol.to_dict()
y_actual = [(pos_symbol, ) for pos_symbol in part_of_speech_dict.values()]
navigable_parents_list = list(part_of_speech_dict.keys())
num_navigable_parents = len(navigable_parents_list)
progress_bar = tqdm(
    navigable_parents_list, total=num_navigable_parents, desc="Predict Label"
)
y_predicted = [(predict_label(navigable_parent), ) for navigable_parent in progress_bar]
duration_str = humanize.precisedelta(time.time() - t1, minimum_unit='seconds', format='%0.0f')
print(f'Predicted labels created in {duration_str}')

print(f'y_predicted[-2:]: {y_predicted[-2:]}')
print(f'y_actual[-2:]: {y_actual[-2:]}')

# Create the MultiLabelBinarizer object
mlb = MultiLabelBinarizer()

# Fit and transform the y_test and y_pred sequences
y_test_transformed = mlb.fit_transform(y_actual)
y_pred_transformed = mlb.transform(y_predicted)
print(f'mlb.classes_: {mlb.classes_}')

# Compute the classification report
classification_report_df = DataFrame.from_dict(
    classification_report(
        y_test_transformed, y_pred_transformed, target_names=mlb.classes_,
        zero_division=0, output_dict=True
    ), orient='index'
)
classification_report_df.index.name = 'pos_symbol'
nu.store_objects(classification_report_df=classification_report_df)
print(classification_report_df.sort_values('recall', ascending=False))

speech_str = f'\n\nLast run on {datetime.now()}\n\n'; print(speech_str)