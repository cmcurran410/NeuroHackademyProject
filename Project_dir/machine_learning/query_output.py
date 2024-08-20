# This script cleans and processes paper summaries, turns them into numerical values using 
# TF-IDF (Term Frequency-Inverse Document Frequency), and lets you search through these 
# summaries by finding the most similar ones to your query.

# TF-IDF is a way to measure how important a word is in a document compared to how often 
# it appears in all documents. It helps focus on the unique words that stand out in a specific 
# document rather than common words found everywhere.


import os
import pandas as pd
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize lemmatizer and stop words
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Set paths
csv_path = 'papers/papers_info.csv'

# Load metadata with specified encoding
data = pd.read_csv(csv_path, encoding='latin1')  # Change 'latin1' to 'iso-8859-1' if needed

# Text preprocessing function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return ' '.join(words)

# Preprocess summaries
data['processed_summary'] = data['summary'].apply(preprocess_text)

# Function to vectorize text using TF-IDF
def vectorize_text(texts):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(texts)
    return vectorizer, vectors

# Vectorize summaries
vectorizer, summary_vectors = vectorize_text(data['processed_summary'])

# Function to search for papers matching a query
def search_papers(query, top_n=5):
    # Preprocess the query
    processed_query = preprocess_text(query)
    
    # Vectorize the query
    query_vector = vectorizer.transform([processed_query])
    
    # Calculate cosine similarity between the query and all summaries
    similarity_scores = cosine_similarity(query_vector, summary_vectors).flatten()
    
    # Get the top N most similar papers
    top_indices = np.argsort(similarity_scores)[-top_n:][::-1]
    
    # Return the top matching papers
    return data.iloc[top_indices][['pdf_name', 'summary', 'label']]

# example
query = "neural correlates of event boundaries"
results = search_papers(query, top_n=5)

print("Top matching papers:")
print(results)

