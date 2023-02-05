import pytesseract
import os
from pdf2image import convert_from_path
from PIL import Image

def extract_text(image):
    return pytesseract.image_to_string(image)

def is_figure(image):
    # Perform OCR on the image
    text = pytesseract.image_to_string(image, config='--psm 6')
    
    # If the OCR result is not empty, the image is considered text
    if text:
        return False
    else:
        return True

# Convert the PDF to a list of images
pages = convert_from_path("tests/test-files/Lesson_2_Memory_Mapping.pdf")

# Initialize the counters for text and figures
text_counter = 0
figure_counter = 0

# Iterate over each page
for i, page in enumerate(pages):
    # Save the page as a PNG image
    page.save(f"tests/test-output/page_{i}.png", "PNG")
    
    # Load the image using the Image library
    image = Image.open(f"tests/test-output/page_{i}.png")
    
    # Determine if the image is a figure or text
    if is_figure(image):
        # Increment the figure counter
        figure_counter += 1
        
        # Save the figure
        image.save(f"tests/test-output/figure_{figure_counter}.png")
    else:
        # Increment the text counter
        text_counter += 1
        
        # Save the text
        text = extract_text(image)
        with open(f"tests/test-output/text_{text_counter}.txt", "w") as file:
            file.write(text)
    
    # Delete the PNG image
    #os.remove(f"tests/test-output/page_{i}.png")