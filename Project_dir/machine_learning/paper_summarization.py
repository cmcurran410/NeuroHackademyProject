import os
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from transformers import pipeline

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize lemmatizer and stop words
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Set paths
extracted_texts_dir = os.path.expanduser('~/Desktop/Sluslo/extracted_texts')
csv_path = 'papers/papers_info.csv'

# Flag for testing
test = 1  # Set to 1 to process only the first 10 papers, set to 0 to process all papers

# Load metadata with specified encoding
data = pd.read_csv(csv_path, encoding='latin1')  # Change 'latin1' to 'iso-8859-1' if needed

# Limit the number of papers to process if in test mode
if test == 1:
    data = data.head(15)

# Text preprocessing function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return ' '.join(words)

# Function to extract the abstract or summary section
def extract_abstract(text):
    # Try to find the abstract/summary section
    abstract_match = re.search(r'(abstract|summary)\s*[:\-]?\s*(.*?)(introduction|background|methods|results|discussion)', text, re.IGNORECASE | re.DOTALL)
    if abstract_match:
        return abstract_match.group(2).strip()
    else:
        return "Abstract/summary not found."

# Read texts from .txt files, extract abstracts, preprocess, and add to DataFrame
abstracts = []
for filename in data['pdf_name']:
    sanitized_filename = "".join([c if c.isalnum() else "_" for c in filename])
    file_path = os.path.join(extracted_texts_dir, f"{sanitized_filename}.txt")
    print(f"Trying to read file: {file_path}")
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                raw_text = file.read()
                abstract_text = extract_abstract(raw_text)
                preprocessed_text = preprocess_text(abstract_text)
                abstracts.append(preprocessed_text)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            abstracts.append('')
    else:
        print(f"File does not exist: {file_path}")
        abstracts.append('')

# Add the abstracts to the DataFrame
data['abstract'] = abstracts

# Initialize the summarization pipeline using BART, specifying the device
summarizer = pipeline('summarization', model='facebook/bart-large-cnn', device=0)  # Use device=0 for GPU if available

# Function to summarize the abstract in one to two sentences
def summarize_abstract(text):
    try:
        # Summarize the abstract with appropriate max_length and min_length
        summary = summarizer(text, max_length=50, min_length=20, do_sample=False)
        clean_summary = re.sub(r'\s+', ' ', summary[0]['summary_text']).strip()
        return clean_summary
    except Exception as e:
        print(f"Error summarizing abstract: {e}")
        return "Error in summarization"

# Apply summarization to each abstract
data['summary'] = data['abstract'].apply(summarize_abstract)

# Display the DataFrame with summaries
print(data[['pdf_name', 'summary']])

data.to_csv(csv_path, index=False)


