import pytesseract
from pdf2image import convert_from_path

inputfile='test-files/Lesson_2_Memory_Mapping.pdf'
outputfile_name=inputfile.replace('.pdf', '.txt')

# convert PDF to image
images = convert_from_path(inputfile)
# Extract text from image
ocr_text = pytesseract.image_to_string(images[0])

# Write resulting text to an output file
outputfile=open(outputfile_name,'w')
outputfile.write(ocr_text)
outputfile.close()