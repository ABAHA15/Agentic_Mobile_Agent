import cv2
import easyocr

# ============================================
# OCR READER
# ============================================

reader = easyocr.Reader(
    ['en'],
    gpu=False
)

# ============================================
# OCR EXTRACTION
# ============================================

def extract_text_from_image(image_path):

    image = cv2.imread(image_path)

    if image is None:

        return ""

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    results = reader.readtext(
        gray
    )

    extracted_text = ""

    for result in results:

        _, text, score = result

        extracted_text += (
            text + " "
        )

    return extracted_text.strip()