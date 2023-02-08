import cv2
import numpy as np
from pdf2image import convert_from_path
import os
import shutil

# Control parameters
iterations = 6
visualizebb = False

# Varaibles 
centers = []

# Paths to the necessary directories
pdf_inputpath = 'tests/test-files/Lesson_2_Memory_Mapping.pdf'
temppath = 'playground/bounding-boxes/temp/'
outputpath = 'tests/test-output/bb/' 

# Clear all files from a directory
def cleardir(pathname):
    for root, dirs, files in os.walk(pathname):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

def processimage():
    pages = convert_from_path(pdf_inputpath)

    for num, page in enumerate(pages):
        tempfile = temppath + f'/tempimage-{num}.png'
        page.save(tempfile, 'PNG')


    for i in range(len(pages)):        
        # Load image, grayscale, Gaussian blur, Otsu's threshold
        target = temppath + f'/tempimage-{i}.png'
        image = cv2.imread(target)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7,7), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Create rectangular structuring element and dilate
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
        dilate = cv2.dilate(thresh, kernel, iterations=iterations)

        # Find contours and draw rectangle
        cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for cnt in cnts:
            centers = list(get_centeroid(cnt))

        h, w, c = image.shape
        count = 0

        for row in get_rows(image, centers, 4, h):
            cv2.polylines(image, [row], False, (255, 0, 255), 2)
            for x, y in row:
                count += 1
                cv2.circle(image, (x, y), 10, (0, 0, 255), -1)  
                cv2.putText(image, str(count), (x - 10, y + 5), 1, cv2.FONT_HERSHEY_PLAIN, (0, 255, 255), 2)

        cv2.imshow("Ordered", image)
        cv2.waitKey(0)
    #cv2.imshow('thresh', thresh) # Show Otsu's threshold to obtain a binary image
    #cv2.imshow('dilate', dilate) # Show the dilation of the paragraph section to connect adjacent words
    #cv2.imshow('image', image) # Show the resulting image with the drawn on rectangles
    
    #imagepath = outputpath + f'testimage-{i}.png'
    #cv2.imwrite(imagepath, image)

def get_centeroid(cnt):
    length = len(cnt)
    sum_x = np.sum(cnt[..., 0])
    sum_y = np.sum(cnt[..., 1])
    return int(sum_x / length), int(sum_y / length)

def get_centers(img):
    contours, hierarchies = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        if cv2.contourArea(cnt) > 100:
            yield get_centeroid(cnt)

def get_rows(image, centers, row_amt, row_h):
    centers = np.array(centers)
    d = row_h / row_amt
    for i in range(row_amt):
        f = centers[:, 1] - d * i
        a = centers[(f < d) & (f > 0)]
        yield a[a.argsort(0)[:, 0]]

def savebounding(cnts, image):
    ROI_number = 0
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        ROI = image[y:y+h, x:x+w]
        bbimage = outputpath + f'ROI-{i}_{ROI_number}.png'
        cv2.imwrite(bbimage, ROI)
        if(visualizebb):
            cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
        ROI_number += 1

# Clear the temp directory and output directory
cleardir(temppath)
cleardir(outputpath)

processed = processimage()

