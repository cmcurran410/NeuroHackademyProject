# text_extraction.py extracts text from PDF files listed in the csv file created in previous step 
# and saves the text to individual .txt files, allowing for batch processing in later steps. 

import os
import pandas as pd
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
from io import StringIO

# set the test flag: 1 to extract text for the first 3 papers, 0 to process all papers
test = 0

def extract_text_from_pdf(pdf_path, laparams):
    try:
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        device = TextConverter(rsrcmgr, retstr, laparams=laparams)
        fp = open(pdf_path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp, caching=True, check_extractable=True):
            interpreter.process_page(page)
        text = retstr.getvalue()
        fp.close()
        device.close()
        retstr.close()
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        text = ""
    return text

def save_extracted_text(paper_name, text, save_dir='extracted_texts'):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    sanitized_name = "".join([c if c.isalnum() else "_" for c in paper_name])
    file_path = os.path.join(save_dir, f"{sanitized_name}.txt")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

def extract_texts_from_papers(papers_info_path, test):
    papers_info = pd.read_csv(papers_info_path)
    if test == 1:
        papers_info = papers_info.head(10)  # Only process the first 3 papers

    laparams = LAParams(char_margin=2.0, line_margin=0.5, word_margin=0.1, boxes_flow=0.5)
    
    for index, row in papers_info.iterrows():
        paper_name = row['pdf_name']
        pdf_path = row['pdf_path']
        if os.path.exists(pdf_path):
            print(f"Extracting text from {pdf_path}")
            text = extract_text_from_pdf(pdf_path, laparams)
            save_extracted_text(paper_name, text)
        else:
            print(f"PDF not found for paper {paper_name} at {pdf_path}")

if __name__ == "__main__":
    papers_info_path = 'papers/papers_info.csv'
    extract_texts_from_papers(papers_info_path, test)

