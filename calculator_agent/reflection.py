import cv2
import easyocr

# -----------------------------------
# OCR
# -----------------------------------

reader = easyocr.Reader(["en"])

# -----------------------------------
# DISPLAY OCR ONLY
# -----------------------------------

def verify_action_success(

    screenshot_path,
    expected_expression

):

    image = cv2.imread(
        screenshot_path
    )

    h, w, _ = image.shape

    # -----------------------------------
    # TOP DISPLAY REGION ONLY
    # -----------------------------------

    display_region = image[
        0:int(h * 0.30),
        0:w
    ]

    gray = cv2.cvtColor(
        display_region,
        cv2.COLOR_BGR2GRAY
    )

    results = reader.readtext(
        gray
    )

    observed_text = ""

    for item in results:

        _, text, _ = item

        observed_text += (
            text + " "
        )

    observed_text = observed_text.strip()

    print("\nDISPLAY OCR:")
    print(observed_text)

    print("\nEXPECTED:")
    print(expected_expression)

    if expected_expression in observed_text:

        print("\nACTION SUCCESS")

        return True

    print("\nACTION FAILED")

    return False