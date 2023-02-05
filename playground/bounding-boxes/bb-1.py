from PIL import Image
import PyPDF2
import pytesseract
import cv2

# Path the PDF file
pdf_path = 'tests/test-files/Lesson_2_Memory_Mapping.pdf'

pdf_file = 

# Read the number of pages in PDF file by finding the length of the page list
numpages = len(PyPDF2.PdfReader(open('tests/test-files/Lesson_2_Memory_Mapping.pdf', 'rb')).pages)

# Initialize a list to store the bounding boxes
boxes = []

# Loop through each page of the PDF
for page_num in range(numpages):  
    # Extract the text and images from the page
    page = pdf_file.pages[page_num] 
    #text = pytesseract.image_to_data(Image.open(pdf_file), output_type='data.frame')
    text = pytesseract.image_to_data(Image.open(pdf_file))