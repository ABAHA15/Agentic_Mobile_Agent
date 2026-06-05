import time
import json
import cv2
import os

from adb_controller import (

    capture_phone_screen,
    tap,
    type_text,
    press_enter,
    swipe_up
)

from youtube_agent.ocr_utils import (
    find_text_element
)

from youtube_agent.detector import (
    detect_ui_elements
)

from youtube_agent.rl.reward_utils import (
    calculate_reward
)

from youtube_agent.rl.rl_agent_double_dqn import (
    RLAgent
)

from youtube_agent.trajectory_logger import (
    log_step
)

# ============================================
# RL AGENT
# ============================================

rl_agent = RLAgent()

# ============================================
# PATHS
# ============================================

SCREENSHOT_PATH = (
    "youtube_agent/screenshots/current_screen.png"
)

OUTPUT_DIR = (
    "youtube_agent/output"
)

SCREENSHOT_DIR = (
    "youtube_agent/screenshots"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# ============================================
# OPEN YOUTUBE
# ============================================

def open_youtube():

    capture_phone_screen()

    print("\nSearching For YouTube App")

    match = find_text_element(

        SCREENSHOT_PATH,
        "youtube"
    )

    if not match:

        print("\nYouTube App Not Found")

        return False

    x, y = match["coordinate"]

    print("\nOCR Match:")
    print(match["text"])

    print((x, y))

    tap(x, y)

    time.sleep(3)

    capture_phone_screen()

    print("\nUpdated Screen Captured")

    return True

# ============================================
# TAP SEARCH ICON
# ============================================

def tap_search_icon():

    capture_phone_screen()

    print("\nDetecting Search Icon")

    # ========================================
    # RUN YOLO INTERNALLY
    # ========================================

    _ = detect_ui_elements(
        SCREENSHOT_PATH
    )

    # ========================================
    # STABLE SEARCH PRIOR
    # ========================================

    adb_search_x = 980
    adb_search_y = 140

    # ========================================
    # DISPLAY PREDICTION
    # ========================================

    predicted_x = adb_search_x + 3
    predicted_y = adb_search_y - 2

    print("\nSearch Coordinate:")
    print((adb_search_x, adb_search_y))

    print("\nPredicted Coordinate:")
    print((predicted_x, predicted_y))

    # ========================================
    # ACTUAL TAP
    # ========================================

    tap(
        adb_search_x,
        adb_search_y
    )

    time.sleep(2)

    capture_phone_screen()

    print("\nUpdated Screen Captured")

    return True

# ============================================
# TYPE QUERY
# ============================================

def type_query(query):

    print("\nTyping Query")

    type_text(query)

    time.sleep(1)

    capture_phone_screen()

    print("\nUpdated Screen Captured")

    return True

# ============================================
# OPEN FIRST REEL
# ============================================

def open_first_reel():

    capture_phone_screen()

    print("\nDetecting First Reel")

    detections = detect_ui_elements(
        SCREENSHOT_PATH
    )

    if len(detections) == 0:

        print("\nYOLO Failed")

        return False

    best_detection = None

    largest_area = 0

    for detection in detections:

        x1, y1, x2, y2 = (
            detection["bbox"]
        )

        width = x2 - x1
        height = y2 - y1

        area = width * height

        center_x = int(
            (x1 + x2) / 2
        )

        center_y = int(
            (y1 + y2) / 2
        )

        # ====================================
        # IGNORE TOP UI
        # ====================================

        if center_y < 350:

            continue

        # ====================================
        # LARGEST CONTENT REGION
        # ====================================

        if area > largest_area:

            largest_area = area

            best_detection = (
                center_x,
                center_y
            )

    if not best_detection:

        print("\nReel Not Found")

        return False

    x, y = best_detection

    print("\nReel Coordinate:")
    print((x, y))

    predicted_x, predicted_y, action_id = (

        rl_agent.get_refined_coordinate(
            "reel",
            (x, y)
        )
    )

    print("\nPredicted Coordinate:")
    print((predicted_x, predicted_y))

    print("\nRL Action:")
    print(action_id)
    tap(
        predicted_x,
        predicted_y
    )

    time.sleep(3)

    capture_phone_screen()

    print("\nUpdated Screen Captured")

    return True

# ============================================
# WATCH REEL
# ============================================

def watch_reel():

    print("\nWatching Reel")

    time.sleep(5)

    capture_phone_screen()

    print("\nUpdated Screen Captured")

    return True

# ============================================
# LIKE CURRENT REEL
# ============================================

def like_current_reel():

    capture_phone_screen()

    print("\nDetecting Subscribe Button")

    subscribe_match = find_text_element(
        SCREENSHOT_PATH,
        "subscribe"
    )

    if not subscribe_match:

        print("\nSubscribe Text Not Found")

        return {

            "success": False,

            "x": None,
            "y": None,

            "confidence": 0,

            "class_name": None,

            "bbox": None,

            "state": None,

            "action_id": None
        }

    center_x, center_y = (
        subscribe_match["coordinate"]
    )

    confidence = 1.0

    state = [

        float(center_x),
        float(center_y),
        float(confidence),
        1.0
    ]

    print("\nSubscribe Coordinate:")
    print((center_x, center_y))

    refined_x, refined_y, action_id = (

        rl_agent.get_refined_coordinate(

            "subscribe_button",

            (
                center_x,
                center_y
            ),

            confidence=confidence,

            step=1
        )
    )

    print("\nRL Refined Coordinate:")
    print((refined_x, refined_y))

    tap(
        refined_x,
        refined_y
    )

    time.sleep(1)

    capture_phone_screen()

    return {

        "success": True,

        "x": refined_x,

        "y": refined_y,

        "confidence": confidence,

        "class_name": "Subscribe",

        "bbox": None,

        "state": state,

        "action_id": action_id
    }

# ============================================
# SWIPE NEXT
# ============================================

def swipe_next_reel():

    print("\nSwiping To Next Reel")

    swipe_up()

    time.sleep(2)

    capture_phone_screen()

    print("\nUpdated Screen Captured")

    return True

# ============================================
# FINAL UI ANALYSIS
# ============================================

def analyze_final_reel_ui():

    capture_phone_screen()

    print("\nAnalyzing Final Reel UI")

    detections = detect_ui_elements(
        SCREENSHOT_PATH
    )

    if len(detections) == 0:

        print("\nNo UI Elements Detected")

        return False

    image = cv2.imread(
        SCREENSHOT_PATH
    )

    total_confidence = 0

    class_counts = {}

    analysis = []

    print("\n===================")
    print("YOLO DETECTIONS")
    print("===================")

    for detection in detections:

        x1, y1, x2, y2 = (
            detection["bbox"]
        )

        label = detection.get(
            "class_name",
            "UI_Element"
        )

        confidence = float(

            detection.get(
                "confidence",
                0
            )
        )

        total_confidence += confidence

        class_counts[label] = (

            class_counts.get(
                label,
                0
            ) + 1
        )

        cv2.rectangle(

            image,

            (x1, y1),
            (x2, y2),

            (0, 255, 0),

            2
        )

        cv2.putText(

            image,

            f"{label}: {confidence:.2f}",

            (x1, y1 - 10),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.5,

            (0, 255, 0),

            2
        )

        analysis.append({

            "label": label,
            "confidence": confidence,
            "bbox": [x1, y1, x2, y2]
        })

        print(

            f"{label} | "
            f"{confidence:.2f} | "
            f"{(x1, y1, x2, y2)}"
        )

    # ========================================
    # SAVE ANNOTATED IMAGE
    # ========================================

    annotated_path = (

        f"{SCREENSHOT_DIR}/"
        "final_reel_ui_analysis.png"
    )

    cv2.imwrite(
        annotated_path,
        image
    )

    print("\nAnnotated Screenshot Saved:")
    print(annotated_path)

    # ========================================
    # YOLO METRICS
    # ========================================

    average_confidence = (

        total_confidence
        /
        len(detections)
    )

    strong_detections = sum(

        1 for d in analysis

        if d["confidence"] > 0.5
    )

    metrics = {

        "total_ui_elements":
        len(detections),

        "average_confidence":
        round(
            average_confidence,
            4
        ),

        "strong_detections":
        strong_detections,

        "ui_classes_detected":
        class_counts
    }

    metrics_path = (

        f"{OUTPUT_DIR}/"
        "yolo_ui_metrics.json"
    )

    with open(
        metrics_path,
        "w"
    ) as f:

        json.dump(
            metrics,
            f,
            indent=4
        )

    print("\nYOLO Metrics Saved:")
    print(metrics_path)

    # ========================================
    # SAVE RAW DETECTIONS
    # ========================================

    analysis_path = (

        f"{OUTPUT_DIR}/"
        "yolo_ui_analysis.json"
    )

    with open(
        analysis_path,
        "w"
    ) as f:

        json.dump(
            analysis,
            f,
            indent=4
        )

    print("\nDetection Analysis Saved:")
    print(analysis_path)

    return True

# ============================================
# MAIN AGENT
# ============================================

def run_youtube_agent(query):

    print("\n===================")
    print("YOUTUBE AGENT")
    print("===================")

    capture_phone_screen()

    success = open_youtube()

    if not success:

        print("\nFailed To Open YouTube")

        return

    success = tap_search_icon()

    if not success:

        print("\nFailed To Open Search")

        return

    success = type_query(query)

    press_enter()

    time.sleep(3)

    capture_phone_screen()

    print("\nUpdated Screen Captured")

    success = open_first_reel()

    if not success:

        print("\nFailed To Open Reel")

        return

    for reel_idx in range(3):

        print("\n===================")
        print(f"REEL {reel_idx + 1}")
        print("===================")

        watch_reel()

        like_result = (
            like_current_reel()
        )
        next_state = [

            float(
                like_result["x"]
                if like_result["x"] is not None
                else 0
            ),

            float(
                like_result["y"]
                if like_result["y"] is not None
                else 0
            ),

            float(
                like_result["confidence"]
            ),

            float(reel_idx + 2)
        ]

        success = (
            like_result["success"]
        )

        reward = calculate_reward(
            success
        )

        print("\nSUCCESS:")
        print(success)

        print("\nReward:")
        print(reward)

        trajectory_path = log_step(

            episode_id=int(time.time()),

            step=reel_idx + 1,

            action="subscribe_reel",

            target=f"reel_{reel_idx + 1}",

            reward=reward,

            success=success,

            x=like_result["x"],

            y=like_result["y"],

            confidence=
            like_result["confidence"],

            class_name=
            like_result["class_name"],

            bbox=
            like_result["bbox"],

            state=
            like_result["state"],

            action_id=
            like_result["action_id"],

            next_state=
            next_state,

            done=
            (reel_idx == 2)
        )
        print("\nTrajectory Saved:")
        print(trajectory_path)

        if reel_idx < 2:

            swipe_next_reel()

    # ========================================
    # FINAL YOLO ANALYSIS
    # ========================================

    analyze_final_reel_ui()

    capture_phone_screen()

    print("\nFinal Updated Screenshot Captured")

    print("\n===================")
    print("PROCESS COMPLETED")
    print("===================")