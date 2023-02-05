from PIL import Image
import PyPDF2
import pytesseract
import cv2
import numpy as np

# Path the PDF file
pdf_file = 'tests/test-files/Lesson_2_Memory_Mapping.pdf'

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
    images = page.extract_images()
    
    # Find the bounding boxes for each paragraph in the page
    para_bboxes = []
    for i in range(len(text)):
        if text.conf[i] > 0:
            (x, y, w, h) = (text.left[i], text.top[i], text.width[i], text.height[i])
            para_bboxes.append((x, y, x + w, y + h))
    # Group the paragraph bounding boxes into page-level bounding boxes
    para_bboxes = cv2.groupRectangles(para_bboxes, 0.1, 0.5)
    for (x1, y1, x2, y2) in para_bboxes:
        boxes.append(('paragraph', x1, y1, x2, y2))
        
    # Find the bounding boxes for each image in the page
    for img in images:
        image = img[0]
        (x1, y1, x2, y2) = img[1]
        boxes.append(('image', x1, y1, x2, y2))

# Sort the bounding boxes in logical reading order
boxes.sort(key=lambda x: (x[1], x[2]))

# Enumerate the bounding boxes
for i, box in enumerate(boxes):
    box = (i+1,) + box[1:]
    boxes[i] = box