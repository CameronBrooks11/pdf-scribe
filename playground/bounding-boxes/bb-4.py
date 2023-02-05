import cv2
import numpy as np
from pdf2image import convert_from_path

# Path the PDF file
pdf_inputpath = 'tests/test-files/Lesson_2_Memory_Mapping.pdf'
outputpath = 'tests/test-output' 

# List to hold extracted page data
page_data = []

images = convert_from_path(pdf_inputpath)

for i in range(len(images)):        
    # Load image, grayscale, Gaussian blur, Otsu's threshold
    target = images[i]
    image = cv2.imread(target)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7,7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Create rectangular structuring element and dilate
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    # Find contours and draw rectangle
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)

    #cv2.imshow('thresh', thresh) # Show Otsu's threshold to obtain a binary image
    #cv2.imshow('dilate', dilate) # Show the dilation of the paragraph section to connect adjacent words
    #cv2.imshow('image', image) # Show the resulting image with the drawn on rectangles

    cv2.

    # Allows users to display a window for given milliseconds waitkey(5000) 
    # or until any key is pressed waitKey() 
    cv2.waitKey() 