import easyocr

# ============================================
# EASYOCR READER
# ============================================

reader = easyocr.Reader(
    ['en'],
    gpu=False
)

# ============================================
# FIND TEXT ELEMENT
# ============================================

def find_text_element(

    image_path,
    target_text,
    return_all=False
):

    results = reader.readtext(image_path)

    matches = []

    target = target_text.lower().strip()

    for detection in results:

        bbox, text, confidence = detection

        detected = text.lower().strip()

        # ====================================
        # PARTIAL MATCH
        # ====================================

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

    results = reader.readtext(image_path)

    target = target_text.lower().strip()

    for detection in results:

        _, text, _ = detection

        detected = text.lower().strip()

        if target in detected:

            return True

    return False