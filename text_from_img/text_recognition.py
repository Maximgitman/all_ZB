from PIL import Image
import pytesseract


# init class for inference
def ocr_text(filename):
    text = pytesseract.image_to_string(Image.open(filename))
    return text