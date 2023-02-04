from PIL import Image
import pytesseract
import cv2


def lib_usage(self):

    # If you don't have tesseract executable in your PATH, include the following:
    '''pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>''''
    # Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
    
    # Simple image to string
    print(pytesseract.image_to_string(Image.open('test.png')))

    # In order to bypass the image conversions of pytesseract, just use relative or absolute image path
    # NOTE: In this case you should provide tesseract supported images or tesseract will return error
    print(pytesseract.image_to_string('test.png'))

    # List of available languages
    print(pytesseract.get_languages(config=''))

    # French text image to string
    print(pytesseract.image_to_string(Image.open('test-european.jpg'), lang='fra'))

    # Batch processing with a single file containing the list of multiple image file paths
    print(pytesseract.image_to_string('images.txt'))

    # Timeout/terminate the tesseract job after a period of time
    try:
        print(pytesseract.image_to_string('test.jpg', timeout=2)) # Timeout after 2 seconds
        print(pytesseract.image_to_string('test.jpg', timeout=0.5)) # Timeout after half a second
    except RuntimeError as timeout_error:
        # Tesseract processing is terminated
        pass

    # Get bounding box estimates
    print(pytesseract.image_to_boxes(Image.open('test.png')))

    # Get verbose data including boxes, confidences, line and page numbers
    print(pytesseract.image_to_data(Image.open('test.png')))

    # Get information about orientation and script detection
    print(pytesseract.image_to_osd(Image.open('test.png')))

    # Get a searchable PDF
    pdf = pytesseract.image_to_pdf_or_hocr('test.png', extension='pdf')
    with open('test.pdf', 'w+b') as f:
        f.write(pdf) # pdf type is bytes by default

    # Get HOCR output
    hocr = pytesseract.image_to_pdf_or_hocr('test.png', extension='hocr')

    # Get ALTO XML output
    xml = pytesseract.image_to_alto_xml('test.png')

def opencv_numpy_support(self):
    img_cv = cv2.imread(r'/<path_to_image>/digits.png')

    # By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
    # we need to convert from BGR to RGB format/mode:
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    print(pytesseract.image_to_string(img_rgb))
    # OR
    img_rgb = Image.frombytes('RGB', img_cv.shape[:2], img_cv, 'raw', 'BGR', 0, 0)
    print(pytesseract.image_to_string(img_rgb))

def oem_psm_config(self):
    # If you need custom configuration like oem/psm, use the config keyword.
    # Example of adding any additional options
    image = '' #add
    custom_oem_psm_config = r'--oem 3 --psm 6'
    pytesseract.image_to_string(image, config=custom_oem_psm_config)

    # Example of using pre-defined tesseract config file with options
    cfg_filename = 'words'
    pytesseract.run_and_get_output(image, extension='txt', config=cfg_filename)

    # Add the following config, if you have tessdata error like: "Error opening data file..."
    # Example config: r'--tessdata-dir "C:\Program Files (x86)\Tesseract-OCR\tessdata"'
    # It's important to add double quotes around the dir path.
    tessdata_dir_config = r'--tessdata-dir "<replace_with_your_tessdata_dir_path>"'
    pytesseract.image_to_string(image, lang='chi_sim', config=tessdata_dir_config)
