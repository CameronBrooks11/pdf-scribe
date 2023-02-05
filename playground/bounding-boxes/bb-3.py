import PyPDF2
import pytesseract
import cv2
from pdf2image import convert_from_path
import tempfile
import numpy as np

# Path the PDF file
pdf_inputpath = 'tests/test-files/Lesson_2_Memory_Mapping.pdf'
pdf_outputpath = 'tests/test-output' 

# List to hold extracted page data
page_data = []

images = convert_from_path(pdf_inputpath)

for i in range(len(images)):        
    data = pytesseract.image_to_data(images[i])
    page_data.append(data)

