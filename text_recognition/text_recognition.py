from PIL import Image
import pytesseract


def ocr_text(filename):
    predicted_text = pytesseract.image_to_string(Image.open(filename))
    assert isinstance(predicted_text, object)
    return predicted_text
