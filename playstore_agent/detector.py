import cv2

from ultralytics import YOLO

from playstore_agent.ocr_utils import (

    find_text_element,
    extract_full_screen_text
)

from playstore_agent.grounding_module import (

    detect_ui_element
)

# ============================================
# LOAD YOLO GUI MODEL
# ============================================

yolo_model = YOLO("best.pt")

# ============================================
# PLAYSTORE SCREENSHOT PATH
# ============================================

SCREENSHOT_PATH = (
    "playstore_agent/screenshots/current_screen.png"
)

# ============================================
# FIND PLAY STORE APP
# ============================================

def find_playstore_app():

    print("\nSearching For Play Store App")

    result = find_text_element(

        SCREENSHOT_PATH,
        "Play Store"
    )

    if result is not None:

        print("\nOCR Match:")
        print(result["text"])

        print(result["coordinate"])

        return result["coordinate"]

    print("\nOCR Failed")

    # ============================================
    # GROUNDING FALLBACK
    # ============================================

    print("\nGroundingDINO Fallback")

    coordinate = detect_ui_element(

        SCREENSHOT_PATH,
        "Play Store app icon"
    )

    return coordinate

# ============================================
# FIND SEARCH BAR
# ============================================

def find_search_bar():

    print("\nSearching For Search Bar")

    # ============================================
    # OCR PRIMARY
    # ============================================

    possible_targets = [

        "Search apps",
        "Search for apps",
        "Search apps & games",
        "Search"
    ]

    for target in possible_targets:

        result = find_text_element(

            SCREENSHOT_PATH,
            target
        )

        if result is not None:

            print("\nOCR Search Bar Match:")
            print(result["text"])

            print(result["coordinate"])

            return result["coordinate"]

    # ============================================
    # YOLO GUI CONTEXT
    # ============================================

    print("\nYOLO GUI Context")

    image = cv2.imread(SCREENSHOT_PATH)

    results = yolo_model(image)

    for result in results:

        boxes = result.boxes

        for box in boxes:

            cls = int(box.cls[0])

            label = (
                yolo_model.names[cls]
            )

            print(label)

    # ============================================
    # GROUNDING FALLBACK
    # ============================================

    print("\nGroundingDINO Fallback")

    coordinate = detect_ui_element(

        SCREENSHOT_PATH,
        "search bar"
    )

    return coordinate

# ============================================
# FIND INSTALL BUTTON
# ============================================

def find_install_button():

    print("\nSearching For Install Button")

    possible_targets = [

        "Install",
        "Update",
        "Open"
    ]

    for target in possible_targets:

        result = find_text_element(

            SCREENSHOT_PATH,
            target
        )

        if result is not None:

            print("\nOCR Button Match:")
            print(result["text"])

            print(result["coordinate"])

            return result["coordinate"]

    # ============================================
    # YOLO GUI SEMANTICS
    # ============================================

    print("\nYOLO GUI Context")

    image = cv2.imread(SCREENSHOT_PATH)

    results = yolo_model(image)

    for result in results:

        boxes = result.boxes

        for box in boxes:

            cls = int(box.cls[0])

            label = (
                yolo_model.names[cls]
            )

            print(label)

    # ============================================
    # GROUNDING FALLBACK
    # ============================================

    print("\nGroundingDINO Fallback")

    coordinate = detect_ui_element(

        SCREENSHOT_PATH,
        "install button"
    )

    return coordinate

# ============================================
# FIND APP SEARCH RESULT
# ============================================

def find_app_result(app_name):

    print("\nSearching For App Result")

    result = find_text_element(

        SCREENSHOT_PATH,
        app_name
    )

    if result is not None:

        print("\nOCR App Match:")
        print(result["text"])

        print(result["coordinate"])

        return result["coordinate"]

    # ============================================
    # GROUNDING FALLBACK
    # ============================================

    print("\nGroundingDINO Fallback")

    coordinate = detect_ui_element(

        SCREENSHOT_PATH,
        f"{app_name} app card"
    )

    return coordinate

# ============================================
# VERIFY INSTALL STARTED
# ============================================

def verify_installation_started():

    full_text = extract_full_screen_text(
        SCREENSHOT_PATH
    )

    full_text = full_text.lower()

    verification_targets = [

        "cancel",
        "installing",
        "pending",
        "open"
    ]

    for target in verification_targets:

        if target in full_text:

            return True

    return False