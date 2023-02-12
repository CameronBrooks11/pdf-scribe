import os
import cv2
import pytesseract as pytess
import numpy as np
from pdf2image import convert_from_path
import tkinter as tk
from tkinter import filedialog
from mdutils.mdutils import MdUtils

file_path = ''
outputpath = 'playground/opencv/output/' 
temppath = 'playground/opencv/temp/'
# tempfile = self.outputdir + f'tempimage-{num}.png'

def convert(inputfile):
    pages = convert_from_path(inputfile)

    for num, page in enumerate(pages):
            image = imagedir + '/' + imagedir_name + f'-{num}.png'
            page.save(image, 'PNG')

def process():
    i=0
    j=1
    finish = False

    while(not finish):
        currpage = imagedir + '/' + imagedir_name + f'-{i}.png'
        # Read image
        im = cv2.imread(currpage)
        cv2.imshow("Image", im)
        key1 = cv2.waitKey(0)

        if key1 == ord('c'):
            r = cv2.selectROI("Image", im, fromCenter= False)            # Select ROI 
            
            key2 = cv2.waitKey(0)

            if key2 == ord('t'):
                imCrop = im[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
                text = pytess.image_to_string(imCrop)
                mdFile.new_paragraph(text)

            if key2 == ord('f'):
                imCrop = im[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
                cv2.imwrite(outputdir+'/'+f'figure-{j}.png', imCrop)
                mdFile.new_inline_image(f"Figure {j}", outputdir+'/'+f'figure-{j}')
        if key1 == ord('q'):
            finish = True
    mdFile.create_md_file()

def prompt():
    root = tk.Tk()
    root.withdraw()
    global file_path
    file_path = filedialog.askopenfilename()

prompt()

imagedir_name = os.path.basename(file_path).replace(".pdf","")
imagedir = 'playground/opencv/images/' + imagedir_name

outputdir = os.path.dirname(file_path)
mdfile_name = os.path.basename(file_path).replace(".pdf",".md")
mdfilepath = outputdir + '/' + mdfile_name
if(not os.path.exists(mdfilepath)):
    mdFile = MdUtils(file_name=imagedir_name, title=imagedir_name)


if(os.path.exists(imagedir)):
    process()
else: 
    os.mkdir(imagedir)
    convert(file_path)
    process()

