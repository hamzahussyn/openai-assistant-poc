import os
import docx
from PyPDF2 import PdfReader

def convert_files_to_text(input_directory, output_directory):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # List all files in the input directory
    files = [file for file in os.listdir(input_directory)]

    for file_name in files:
        file_path = os.path.join(input_directory, file_name)

        # Check if the file is a PDF
        if file_name.lower().endswith('.pdf'):
            # Read the PDF and extract text
            text = read_pdf(file_path)

        # Check if the file is a DOCX
        elif file_name.lower().endswith('.docx'):
            # Read the DOCX and extract text
            text = read_docx(file_path)

        else:
            print(f"Unsupported file format: {file_name}")
            continue

        # Create a text file with the same name in the output directory
        text_file_path = os.path.join(output_directory, os.path.splitext(file_name)[0] + '.txt')

        # Write the extracted text to the text file
        with open(text_file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(text)

        print(f"Converted {file_name} to {os.path.basename(text_file_path)}")

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        num_pages = len(pdf_reader.pages)

        text = ""
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    return text

def read_docx(file_path):
    doc = docx.Document(file_path)
    paragraphs = [paragraph.text for paragraph in doc.paragraphs]
    text = "\n".join(paragraphs)
    return text

# Example usage
input_directory = './Developers'
output_directory = './Developers-Parsed'

convert_files_to_text(input_directory, output_directory)
