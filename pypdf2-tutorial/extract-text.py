import PyPDF2
from PyPDF2 import PdfReader
import fitz as PyMuPDF

inputfile='test-files/Lesson_2_Memory_Mapping.pdf'
outputfile_name=inputfile.replace('.pdf', '.txt')

reader = PdfReader(inputfile)

page = reader.pages[0]
rawtext = page.extract_text()

outputfile=open(outputfile_name,'w')
outputfile.write(rawtext)
outputfile.close()