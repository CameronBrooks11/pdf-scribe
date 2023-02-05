import PyPDF2
import pytesseract
import cv2
import numpy as np

# Path the PDF file
pdf_path = 'tests/test-files/Lesson_2_Memory_Mapping.pdf'

# Load the PDF file
pdf_file = PyPDF2.PdfFileReader(open(pdf_path, 'rb'))

# Initialize variables for bounding box enumeration
box_index = 1
para_boxes = []
image_boxes = []

# Loop through each page of the PDF
for page_num in range(pdf_file.getNumPages()):
    # Extract the text and images from the page
    page = pdf_file.getPage(page_num)
        # text = pytesseract.image_to_data(page.extract_text(), output_type='data.frame')
    text = pytesseract.image_to_data(page)
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
        para_boxes.append((box_index, x1, y1, x2, y2))
        box_index += 1
        
    # Find the bounding boxes for each image in the page
    for img in images:
        image = img[0]
        (x1, y1, x2, y2) = img[1]
        image_boxes.append((box_index, x1, y1, x2, y2))
        box_index += 1

# Print the resulting bounding boxes for paragraphs and images
print("Paragraph bounding boxes:")
print(para_boxes)
print("Image bounding boxes:")
print(image_boxes)