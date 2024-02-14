import os
import nltk
from PyPDF2 import PdfReader
from nltk import pos_tag, ne_chunk
from nltk.tokenize import word_tokenize, sent_tokenize

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def convert_pdfs_to_text(input_directory, output_directory):
    # ... (unchanged code)
     # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # List all PDF files in the input directory
    pdf_files = [file for file in os.listdir(input_directory) if file.lower().endswith('.pdf')]

    for pdf_file in pdf_files:
        pdf_file_path = os.path.join(input_directory, pdf_file)

        # Read the PDF and extract text
        text = read_pdf(pdf_file_path)

        # Use NLTK for named entity recognition
        named_entities = extract_named_entities(text)

        # Replace names with 'REDACTED_NAME'
        filtered_text = filter_named_entities(text, named_entities)

         # Create a text file with the same name in the output directory
        text_file_path = os.path.join(output_directory, os.path.splitext(pdf_file)[0] + '.txt')

        # Write the extracted text to the text file
        with open(text_file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(text)

        print(f"Converted {pdf_file} to {os.path.basename(text_file_path)}")

def extract_named_entities(text):
    sentences = sent_tokenize(text)
    named_entities = []

    for sentence in sentences:
        words = word_tokenize(sentence)
        pos_tags = pos_tag(words)
        tree = ne_chunk(pos_tags, binary=True)

        for subtree in tree:
            if isinstance(subtree, nltk.Tree):
                entity = " ".join([word for word, tag in subtree.leaves()])
                named_entities.append(entity)

    return named_entities

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        num_pages = len(pdf_reader.pages)

        text = ""
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    return text

def filter_named_entities(text, named_entities):
    filtered_text = text
    for entity in named_entities:
        filtered_text = filtered_text.replace(entity, 'REDACTED_NAME')

    return filtered_text

# Example usage
input_directory = './Developers'
output_directory = './Developers-Parsed-NER'

convert_pdfs_to_text(input_directory, output_directory)
