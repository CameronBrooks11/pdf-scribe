import PyPDF2
import io
from PIL import Image
import pytesseract

# Open the PDF file
pdf_file = PyPDF2.PdfReader(open("tests/test-files/Lesson_2_Memory_Mapping.pdf", "rb"))

# Initialize the counter
counter = 1

# Loop through each page of the PDF
for page_num in range(len(pdf_file.pages)): 
    page = pdf_file.pages[page_num]
    contents = page.extract_text().strip().split("\n")

    # Loop through each line of text on the page
    for content in contents:
        if "/Image" in content:
            # Extract and save the image
            page_images = page["/Resources"]["/XObject"].getObject()
            for img_id, img in page_images.items():
                if img_id in content:
                    size = (img["/Width"], img["/Height"])
                    data = io.BytesIO(img._data)
                    img = Image.open(data)
                    text = pytesseract.image_to_string(img)
                    img.save(f"tests/test-output/image_{counter}.png")
                    counter += 1
        else:
            # Save the text as a separate file
            with open(f"tests/test-output/text_{counter}.txt", "w") as f:
                f.write(content)
                counter += 1
