import cv2
import easyocr

from ultralytics import YOLO

from calculator_agent.grounding_module import (
    detect_ui_element
)

# ============================================
# OCR
# ============================================

reader = easyocr.Reader(
    ['en'],
    gpu=False
)

# ============================================
# YOLO
# ============================================

model = YOLO(
    "best.pt"
)

# ============================================
# VALID SYMBOLS
# ============================================

VALID_SYMBOLS = [

    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",

    "+",
    "-",
    "*",
    "/",
    "="
]

# ============================================
# NORMALIZE SYMBOLS
# ============================================

def normalize_symbol(text):

    text = text.strip()

    replacements = {

        "x": "*",
        "X": "*",

        "÷": "/",

        "—": "-",
        "_": "-",

        "plus": "+",

        "equals": "="
    }

    if text in replacements:

        text = replacements[text]

    return text

# ============================================
# FIND CALCULATOR APP
# ============================================

def find_calculator_app():

    image_path = (
        "calculator_agent/screenshots/current_screen.png"
    )

    image = cv2.imread(image_path)

    results = reader.readtext(image)

    for result in results:

        bbox, text, score = result

        text_lower = text.lower().strip()

        if "calculator" in text_lower:

            x = int(
                (bbox[0][0] + bbox[2][0]) / 2
            )

            y = int(
                (bbox[0][1] + bbox[2][1]) / 2
            )

            print("\nOCR Match:")
            print(text)

            print((x, y))

            return (x, y)

    grounding_coordinate = detect_ui_element(

        image_path=image_path,

        text_prompt="calculator app icon"
    )

    if grounding_coordinate is not None:

        print("\nGroundingDINO Match:")
        print(grounding_coordinate)

        return grounding_coordinate

    return None

# ============================================
# OCR PREPROCESS
# ============================================

def preprocess_for_ocr(image):

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    gray = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    thresh = cv2.adaptiveThreshold(

        gray,

        255,

        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,

        cv2.THRESH_BINARY,

        11,

        2
    )

    return thresh

# ============================================
# RELATIVE OPERATOR REGIONS
# ============================================

def generate_relative_operator_regions(width, height):

    return {

        "+": (
            int(width * 0.87),
            int(height * 0.79)
        ),

        "-": (
            int(width * 0.87),
            int(height * 0.69)
        ),

        "*": (
            int(width * 0.87),
            int(height * 0.60)
        ),

        "/": (
            int(width * 0.87),
            int(height * 0.50)
        ),

        "=": (
            int(width * 0.87),
            int(height * 0.91)
        )
    }

# ============================================
# BUILD BUTTON CACHE
# ============================================

def build_button_cache():

    image_path = (
        "calculator_agent/screenshots/current_screen.png"
    )

    image = cv2.imread(image_path)

    height, width = image.shape[:2]

    print("\nBuilding Hybrid Button Cache")

    processed = preprocess_for_ocr(
        image
    )

    results = reader.readtext(

        processed,

        detail=1,

        paragraph=False
    )

    button_cache = {}

    # ============================================
    # OCR DIGITS
    # ============================================

    for result in results:

        bbox, text, score = result

        clean_text = normalize_symbol(
            text
        )

        if clean_text not in VALID_SYMBOLS:
            continue

        # only digits from OCR

        if clean_text.isdigit():

            x = int(
                (bbox[0][0] + bbox[2][0]) / 2
            )

            y = int(
                (bbox[0][1] + bbox[2][1]) / 2
            )

            button_cache[clean_text] = (
                x,
                y
            )

            print("\nCached Symbol:")
            print(clean_text)

            print("Coordinate:")
            print((x, y))

    # ============================================
    # RELATIVE OPERATORS
    # ============================================

    operator_regions = (

        generate_relative_operator_regions(
            width,
            height
        )
    )

    for symbol, coordinate in operator_regions.items():

        button_cache[symbol] = coordinate

    # ============================================
    # YOLO GUI CONTEXT
    # ============================================

    try:

        yolo_results = model(image_path)

        print("\nYOLO GUI Context:")

        for r in yolo_results:

            names = r.names

            classes = r.boxes.cls.cpu().numpy()

            for cls_id in classes:

                cls_name = names[int(cls_id)]

                print(cls_name)

    except Exception as e:

        print("\nYOLO Context Failed")
        print(e)

    print("\nFINAL BUTTON CACHE:")
    print(button_cache.keys())

    return button_cache