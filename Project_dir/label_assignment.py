# label_assignment.py categorizes research papers by analyzing the text content of their extracted `.txt` files, assigning labels 
# based on the presence and frequency of predefined keywords across three categories (Behavioral, Neuroimaging, Computational) 
# then saves the labeled data back to a CSV file.
# Written because the training dataset for the NLP label assignment approach was too messy for accurate training

import os
import pandas as pd

# Define the keywords for each category
keywords = {
    'Behavioral': ['eye-tracking', 'narrative analysis', 'reaction time', 'behavioral', 'psychophysics', 'task performance', 'response time', 'response accuracy', 'behavioral measures', 'psychological', 'task', 'performance', 'cognitive task', 'decision making', 'response inhibition', 'motor response', 'error rate', 'accuracy', 'learning task', 'attention', 'memory recall', 'working memory', 'reinforcement', 'stimulus-response', 'reaction time variability', 'performance monitoring', 'behavior analysis', 'cognitive control', 'task switching', 'response selection', 'motor learning', 'task accuracy', 'performance error'],
    'Neuroimaging': ['MRI', 'fMRI', 'MEG', 'dTI', 'Amygdala', 'structural', 'diffusion tensor imaging', 'brain imaging', 'neuroimaging', 'voxel-based morphometry','multivariate pattern analysis','bold signal', 'connectivity analysis', 'eeg', 'ieeg', 'electroencephalography', 'intracranial eeg', 'event-related potentials', 'brainwaves', 'brain oscillations', 'neural synchrony', 'spectral analysis', 'cortical recordings', 'neurophysiological', 'neural'],
    'Computational': ['computational modeling', 'neural networks', 'artificial intelligence', 'machine learning', 'deep learning', 'simulations', 'computational theory', 'algorithms', 'computational analysis', 'mathematical modeling', 'predictive modeling', 'neural computation', 'cognitive modeling', 'computational', 'modeling', 'simulation']
}

# Set the threshold for the minimum number of keyword occurrences
threshold = 2  # Adjusted to be less conservative

# Function to label the paper based on its text content
def label_paper(text):
    method_counts = {key: 0 for key in keywords.keys()}
    for key, terms in keywords.items():
        for term in terms:
            if term.lower() in text.lower():
                method_counts[key] += 1

    # Determine the label based on counts
    relevant_methods = {k: v for k, v in method_counts.items() if v >= threshold}

    if not relevant_methods:
        return 'Uncategorized'

    if len(relevant_methods) == 1:
        return list(relevant_methods.keys())[0]

    # If there are multiple categories with sufficient counts, find the two highest
    sorted_methods = sorted(relevant_methods.items(), key=lambda item: item[1], reverse=True)
    top_method, top_count = sorted_methods[0]
    second_method, second_count = sorted_methods[1] if len(sorted_methods) > 1 else (None, 0)

    if second_method and abs(top_count - second_count) <= 1:
        return f"{top_method}/{second_method}"

    return top_method

# Set paths
extracted_texts_dir = os.path.expanduser('~/Desktop/Sluslo/extracted_texts')
csv_path = 'papers/papers_info.csv'

# Load metadata
data = pd.read_csv(csv_path, encoding='ISO-8859-1')

# Read texts from .txt files, evaluate and assign labels
labels = []
for filename in data['pdf_name']:
    sanitized_filename = "".join([c if c.isalnum() else "_" for c in filename])  # Ensure filename is sanitized
    file_path = os.path.join(extracted_texts_dir, f"{sanitized_filename}.txt")
    print(f"Processing file: {file_path}")  # Debug: Print file path
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                label = label_paper(text)
                labels.append(label)
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
