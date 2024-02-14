from PIL import Image
from pdf2image import convert_from_path
import pytesseract

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Adjust this path based on your system

# Input PDF file path
pdf_path = './Designer/Multazam_Siddiqui_CV.PDF'

# Convert PDF to images
images = convert_from_path(pdf_path, 300)  # 300 DPI, adjust as needed

output_text_file = './Designer-Text/multazim-siddiqui.txt'

# Perform OCR on each image
with open(output_text_file, 'w') as file:
    for i, img in enumerate(images):
        # Perform OCR on the image
        text = pytesseract.image_to_string(img)
        
        # Write the extracted text to the file for each page
        file.write(f"Extracted Text (Page {i + 1}):\n")
        file.write(text)
        file.write('\n\n')
