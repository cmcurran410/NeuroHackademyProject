
# data_collection.py integrates sluslo with user's personal zotero library 
# and uses a local crawler to go through the zotero database and saves each
# paper's metadat to a csv file that will later be used to index and read the papers

import os
import pandas as pd
import random

# Flag to determine the number of files to process
test = 0  # Set to 0 to process all data, 1 to process only the first 10 cells

def fetch_papers_from_storage(storage_dir, test):
    papers_info = []
    
    for storage_key in os.listdir(storage_dir):
        key_path = os.path.join(storage_dir, storage_key)
        if os.path.isdir(key_path):
            for file_name in os.listdir(key_path):
                if file_name.endswith('.pdf'):
                    pdf_path = os.path.join(key_path, file_name)
                    paper_info = {
                        'storage_key': storage_key,
                        'pdf_name': file_name,
                        'pdf_path': pdf_path,
                        'label': random.choice([''])  
                    }
                    papers_info.append(paper_info)
                    # If test flag is set, limit the number of papers
                    if test == 1 and len(papers_info) >= 10:
                        return papers_info
    
    return papers_info

def save_papers_info(papers, save_dir='papers'):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    df = pd.DataFrame(papers)
    df.to_csv(os.path.join(save_dir, 'papers_info.csv'), index=False)

if __name__ == "__main__":
    storage_dir = "/Users/AydinTasevac/Zotero/storage"
    papers = fetch_papers_from_storage(storage_dir, test)
    save_papers_info(papers)








