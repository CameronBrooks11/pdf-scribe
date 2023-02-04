import pytesseract
from pdf2image import convert_from_path

inputfile='tests/test-files/Lesson_2_Memory_Mapping.pdf'
outputfile_name=inputfile.replace('.pdf', '.txt')
outputfile_name=outputfile_name.replace('test-files', 'test-output')

images = convert_from_path(inputfile)
ocr_text = ''

for i in range(len(images)):        
    page_content = pytesseract.image_to_string(images[i])
    page_content = '***PDF Page {}***\n'.format(i+1) + page_content
    ocr_text = ocr_text + ' ' + page_content

# Write resulting text to an output file
outputfile=open(outputfile_name,'w')
outputfile.write(ocr_text)
outputfile.close()