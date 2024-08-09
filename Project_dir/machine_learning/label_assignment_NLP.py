# NLP_label_assignment_train fine-tunes a NLP model (DistilBERT)for sequence classification, 
# categorizing text sequences (like sentences or paragraphs)into predefined labels. 
# After training on labeled paper texts, the model classifies new texts and updates the CSV with the predicted labels. 

import os
import pandas as pd
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import torch
from torch.utils.data import Dataset

class PapersDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )
        return {
            'text': text,
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

# Load data
csv_path = 'papers/papers_info.csv'
extracted_texts_dir = os.path.expanduser('~/Desktop/Sluslo/extracted_texts')
data = pd.read_csv(csv_path, encoding='ISO-8859-1')

# Only take the first 40 labeled papers
data = data.dropna(subset=['label']).iloc[:43]

# Read texts from .txt files for the first 40 labeled papers
texts = []
for filename in data['pdf_name']:
    sanitized_filename = "".join([c if c.isalnum() else "_" for c in filename])  # Ensure filename is sanitized
    file_path = os.path.join(extracted_texts_dir, f"{sanitized_filename}.txt")
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            texts.append(file.read())
    else:
        texts.append('')

# Encode labels
labels = data['label'].values
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(labels)

# Split the data
X_train, X_val, y_train, y_val = train_test_split(texts, labels, test_size=0.1, random_state=42)

# Load pre-trained model and tokenizer
model_name = "distilbert-base-uncased"
tokenizer = DistilBertTokenizer.from_pretrained(model_name)
model = DistilBertForSequenceClassification.from_pretrained(model_name, num_labels=len(label_encoder.classes_))

# Create datasets
train_dataset = PapersDataset(X_train, y_train, tokenizer, max_len=512)
val_dataset = PapersDataset(X_val, y_val, tokenizer, max_len=512)

# Training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    evaluation_strategy="steps",
    eval_steps=50,
    save_steps=50,
    load_best_model_at_end=True,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer
)

# Train the model
trainer.train()

# Save the model and tokenizer
model.save_pretrained('./model')
tokenizer.save_pretrained('./model')

##############################################################

from transformers import pipeline

# Load the fine-tuned model and tokenizer
model_name = "./model"
tokenizer = DistilBertTokenizer.from_pretrained(model_name)
model = DistilBertForSequenceClassification.from_pretrained(model_name)

# Create a classification pipeline
classifier = pipeline('text-classification', model=model, tokenizer=tokenizer, return_all_scores=True)

# Define the categories
categories = list(label_encoder.classes_)

# Function to classify text using the transformer model
def classify_text(text):
    outputs = classifier(text, truncation=True)
    scores = outputs[0]
    scores_dict = {categories[i]: scores[i]['score'] for i in range(len(scores))}
    
    # Sort categories by score
    sorted_scores = sorted(scores_dict.items(), key=lambda item: item[1], reverse=True)
    top_method, top_score = sorted_scores[0]
    second_method, second_score = sorted_scores[1] if len(sorted_scores) > 1 else (None, 0)

    if second_method and abs(top_score - second_score) <= 0.1:  # Adjust the threshold as needed
        return f"{top_method}/{second_method}"

    return top_method

# Set paths
extracted_texts_dir = os.path.expanduser('~/Desktop/Sluslo/extracted_texts')
csv_path = 'papers/papers_info.csv'

# Load metadata
data = pd.read_csv(csv_path, encoding='ISO-8859-1')

# Read texts from .txt files, classify and assign labels
labels = []
for index, row in data.iterrows():
    filename = row['pdf_name']
    sanitized_filename = "".join([c if c.isalnum() else "_" for c in filename])  # Ensure filename is sanitized
    file_path = os.path.join(extracted_texts_dir, f"{sanitized_filename}.txt")
    print(f"Processing file: {file_path}")  # Debug: Print file path
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                if pd.isna(row['label']):
                    label = classify_text(text)
                    labels.append(label)
                else:
                    labels.append(row['label'])
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            labels.append('Uncategorized')
    else:
        print(f"File does not exist: {file_path}")
        labels.append('Uncategorized')

# Add the labels to the DataFrame
data['label'] = labels

# Save the updated DataFrame back to CSV
data.to_csv(csv_path, index=False, encoding='ISO-8859-1')

# Check if the labels are correctly populated
print(data[['pdf_name', 'label']].head())
