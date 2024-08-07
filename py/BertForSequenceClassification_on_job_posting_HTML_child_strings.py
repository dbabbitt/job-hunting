#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



# From Anaconda Prompt (anaconda3), type:
# conda activate "C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\jh_env"
# cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\py
# cls
# python BertForSequenceClassification_on_job_posting_HTML_child_strings.py

# From Ubuntu WSL, type:
# conda activate "/mnt/c/Users/daveb/OneDrive/Documents/GitHub/job-hunting/jh_env"; cd /mnt/c/Users/daveb/OneDrive/Documents/GitHub/job-hunting/py; clear; python.exe BertForSequenceClassification_on_job_posting_HTML_child_strings.py
# TODO: Replace humanize with a linux replacement


from jobpostlib import (cu, datetime, nu, humanize, time)
from pandas import DataFrame
from sklearn.metrics import classification_report
from sklearn.preprocessing import MultiLabelBinarizer
from tqdm import tqdm
from transformers import BertForSequenceClassification, BertTokenizer, BertConfig
import os
import torch


# 
# How do I pretrain an encoder model that has for its labeled training data HTML text surrounded by its parent HTML tag (if any) labeled with one of these categories: Job Title, Corporate Scope, Task Scope, Educational Requirements, Minimum Qualifications, Preferred Qualifications, Supplemental Pay, Legal Notifications, Office Location, Job Duration, Interview Procedures, Other, and Posting Date (Header or Non-header)? For instance, the navigable_parent "&lt;li>Troubleshooting and triaging issues with multiple teams to drive towards root cause identification and resolution.&lt;/li>" would be labeled "O-TS" (Task Scope Non-header).

# 
# To pretrain an encoder model for this task, I follow these steps:
# 
# 1. Data Preparation:
#    - Ensuring my dataset consists of HTML text snippets with their corresponding parent tags.

if not (nu.pickle_exists('file_tags_df') and nu.pickle_exists('file_tags_mapping')):
    
    # Get tagged nodes data frame
    cypher_str = f'''
        // Get the tagged node counts for each file
        MATCH (pos:PartsOfSpeech)-[r1:SUMMARIZES]->(np1:NavigableParents)-[r2:NEXT]->(np2:NavigableParents)
        WITH
            r2.file_name AS file_name,
            COUNT(r1) AS tagged_count,
            COUNT(r2) AS edge_count,
            COUNT(np1) AS np_count
        RETURN np_count, tagged_count, edge_count, file_name
        ORDER BY edge_count DESC;'''
    row_objs_list = []
    with cu.driver.session() as session: row_objs_list = session.write_transaction(cu.do_cypher_tx, cypher_str)
    if row_objs_list:
        tagged_node_counts_df = DataFrame(row_objs_list)
        print(f'tagged_node_counts_df.shape: {tagged_node_counts_df.shape}') # (3972, 4)
    
    # Get all tagged HTML child strings
    filenames_list = tagged_node_counts_df.file_name.tolist()
    filenames_str = '", "'.join(filenames_list)
    cypher_str = f'''
        // Get child string and POS for each at-least-partially tagged file
        MATCH (pos:PartsOfSpeech)-[r1:SUMMARIZES]->(np1:NavigableParents)-[r2:NEXT]->(np2:NavigableParents)
        WHERE
            r2.file_name IN ["{filenames_str}"]
        RETURN
            np1.navigable_parent AS text,
            pos.pos_symbol AS pos_symbol;'''
    row_objs_list = []
    with cu.driver.session() as session: row_objs_list = session.write_transaction(cu.do_cypher_tx, cypher_str)
    if row_objs_list:
        pos_html_strs_df = DataFrame(row_objs_list).drop_duplicates()
        print(f'pos_html_strs_df.shape: {pos_html_strs_df.shape}') # (16239, 2)
        
        # Convert lables to numbers and get mapping
        sequence = pos_html_strs_df.pos_symbol.tolist()
        new_sequence, file_tags_mapping = nu.convert_strings_to_integers(sequence)
        pos_html_strs_df['label'] = new_sequence
        nu.store_objects(file_tags_df=pos_html_strs_df, file_tags_mapping=file_tags_mapping)

else:
    file_tags_mapping = nu.load_object('file_tags_mapping')
    pos_html_strs_df = nu.load_object('file_tags_df')

# 2. Tokenization:
#    - Use a tokenizer that can handle HTML tags (e.g., a custom tokenizer or adapt an existing one like BERT's tokenizer).
#    - Ensure the tokenizer preserves the HTML structure.

# Custom dataset class
class HTMLDataset(torch.utils.data.Dataset):
    def __init__(self, data, tokenizer, max_length):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data.iloc[idx]
        encoding = self.tokenizer.encode_plus(
            item['text'],
            add_special_tokens=True,
            max_length=self.max_length,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(item['label'], dtype=torch.long)
        }
model_path = '../saves/models/sequence_classification.model'
tokenizer_path = '../saves/tokenizers/sequence_classification.tokenizer'

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

def get_latest_epoch(model_path):
    epochs = []
    try:
        epochs = [int(d.split('-')[-1]) for d in os.listdir(model_path) if d.startswith('epoch-')]
    except:
        return 0
    return max(epochs) if epochs else 0

# Tokenizer setup
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# 3. Model Architecture:
#    - Choose a suitable encoder architecture (e.g., BERT, RoBERTa, or a custom transformer-based model).
#    - Modify the final layer to output predictions for your specific categories.

# Model setup
num_labels = len(file_tags_mapping)
config = BertConfig.from_pretrained('bert-base-uncased', num_labels=num_labels)

# 4. Pretraining Objective:
#    - For sequence classification, use the labeled data to train the model to predict the correct category.

# Dataset and DataLoader setup
dataset = HTMLDataset(pos_html_strs_df, tokenizer, max_length=128)
dataloader = torch.utils.data.DataLoader(dataset, batch_size=16, shuffle=True)

# Training loop
num_epochs = 10

# Get the latest epoch
last_completed_epoch = get_latest_epoch(model_path)

epoch = last_completed_epoch + 1

# Load the model from the latest snapshot or initialize if it's the first epoch
if last_completed_epoch > 0:
    model = BertForSequenceClassification.from_pretrained(f"{model_path}/epoch-{last_completed_epoch}")
    print(f"\nContinuing training up to {num_epochs} epochs...")
    print(f"Epoch {epoch}/{num_epochs}")
    print(f"Loaded model from epoch {last_completed_epoch}\n")
else:
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', config=config)
    print(f"\nStarting training for {num_epochs} epochs...")
    print(f"Epoch {epoch}/{num_epochs}")
    print("Initialized new model\n")

model.to(device)  # Move model to GPU if available
optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)

# 5. Training Process:
#    - Implement the training loop, including:
#      - Batching the data
#      - Computing loss for classification tasks
#      - Backpropagation and optimization
epoch_loss = 0.0
num_batches = len(dataloader)

# Use tqdm for a progress bar
progress_bar = tqdm(dataloader, total=num_batches, desc=f"Epoch {epoch}")

model.train()
t1 = time.time()
for batch in progress_bar:
    batch = {k: v.to(device) for k, v in batch.items()}  # Move batch to GPU if available
    outputs = model(**batch)
    loss = outputs.loss
    epoch_loss += loss.item()
    
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
    
    # Update progress bar description with current loss
    progress_bar.set_postfix({'loss': f'{loss.item():.4f}'})

# Print average loss for the epoch
avg_loss = epoch_loss / num_batches
print(f"Epoch {epoch} completed. Average loss: {avg_loss:.4f}")

duration_str = humanize.precisedelta(time.time() - t1, minimum_unit='seconds', format='%0.0f')
print(f'Trained epoch in {duration_str}')

# Save the model after each epoch
epoch_dir = f"{model_path}/epoch-{epoch}"
print(f"Saving model to {epoch_dir}")
model.save_pretrained(epoch_dir)
print("Model saved successfully.")

# Save the tokenizer
print(f"Saving tokenizer to {tokenizer_path}")
tokenizer.save_pretrained(tokenizer_path)
print("Tokenizer saved successfully.")

if epoch == 10:
    print("Training completed.")

print('-----------------\n\n')
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