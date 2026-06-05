import cv2
import easyocr

# ============================================
# EASYOCR READER
# ============================================

reader = easyocr.Reader(
    ['en'],
    gpu=False
)

# ============================================
# PREPROCESS IMAGE
# ============================================

def load_image(image_path):

    image = cv2.imread(image_path)

    if image is None:

        raise ValueError(
            f"Failed To Load Image: {image_path}"
        )

    return image

# ============================================
# FIND TEXT ELEMENT
# ============================================

def find_text_element(

    image_path,
    target_text,
    return_all=False
):

    image = load_image(image_path)

    results = reader.readtext(image)

    matches = []

    target = target_text.lower().strip()

    for detection in results:

        bbox, text, confidence = detection

        detected = text.lower().strip()

        if target in detected:

            x = int(
                (bbox[0][0] + bbox[2][0]) / 2
            )

            y = int(
                (bbox[0][1] + bbox[2][1]) / 2
            )

            matches.append({

                "text": text,

                "coordinate": (x, y),

                "confidence": confidence
            })

    if return_all:

        return matches

    if len(matches) > 0:

        return matches[0]

    return None

# ============================================
# VERIFY TEXT EXISTS
# ============================================

def verify_text_exists(

    image_path,
    target_text
):

    image = load_image(image_path)

    results = reader.readtext(image)

    target = target_text.lower().strip()

    for detection in results:

        _, text, _ = detection

        detected = text.lower().strip()

        if target in detected:

            return True

    return False

# ============================================
# EXTRACT FULL SCREEN TEXT
# ============================================

def extract_full_screen_text(
    image_path
):

    image = load_image(image_path)

    results = reader.readtext(image)

    collected_text = []

    for detection in results:

        _, text, _ = detection

        collected_text.append(text)

    return " ".join(collected_text)