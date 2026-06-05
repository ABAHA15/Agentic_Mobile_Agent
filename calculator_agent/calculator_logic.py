import time
import cv2
import easyocr

from adb_controller import (
    capture_screenshot,
    tap_on_phone
)

from calculator_agent.detector import (
    find_calculator_app,
    build_button_cache
)

from calculator_agent.planner import (
    create_plan
)

from calculator_agent.rl.rl_agent import (
    RLAgent
)

from calculator_agent.trajectory_logger import (
    log_step
)

# ============================================
# OCR READER
# ============================================

reader = easyocr.Reader(
    ['en'],
    gpu=False
)

# ============================================
# EXTRACT SCREEN TEXT
# ============================================

def extract_screen_text():

    image_path = (
        "calculator_agent/screenshots/current_screen.png"
    )

    image = cv2.imread(image_path)

    results = reader.readtext(
        image
    )

    combined_text = ""

    for result in results:

        _, text, _ = result

        combined_text += text + " "

    combined_text = combined_text.strip()

    return combined_text

# ============================================
# VERIFY SCREEN STATE
# ============================================

def verify_expression(expected_expression):

    observed_text = extract_screen_text()

    observed_text = (
        observed_text.replace(" ", "")
    )

    expected_expression = (
        expected_expression.replace(" ", "")
    )

    print("\nOBSERVED SCREEN TEXT:")
    print(observed_text)

    print("\nEXPECTED:")
    print(expected_expression)

    return expected_expression in observed_text

# ============================================
# MAIN AGENT
# ============================================

def run_calculator_agent(expression):

    print("\n===================")
    print("CALCULATOR AGENT")
    print("===================")

    agent = RLAgent()

    # ============================================
    # INITIAL SCREEN
    # ============================================

    print("\nCapturing Current Screen")

    capture_screenshot()

    # ============================================
    # FIND CALCULATOR APP
    # ============================================

    print("\nSearching For Calculator App")

    app_coordinate = find_calculator_app()

    if app_coordinate is None:

        print("\nCalculator App Not Found")

        return

    print("\nOpening Calculator")

    tap_on_phone(

        app_coordinate[0],
        app_coordinate[1]
    )

    # ============================================
    # WAIT FOR APP OPEN
    # ============================================

    time.sleep(2)

    # ============================================
    # CAPTURE CALCULATOR UI
    # ============================================

    capture_screenshot()

    print("\nCalculator UI Captured")

    # ============================================
    # BUILD BUTTON CACHE
    # ============================================

    button_cache = build_button_cache()

    print("\nFINAL BUTTON CACHE:")
    print(button_cache.keys())

    # ============================================
    # CREATE PLAN
    # ============================================

    plan = create_plan(expression)

    print("\nPLAN:")
    print(plan)

    episode_id = int(time.time())

    current_expression = ""

    # ============================================
    # EXECUTION LOOP
    # ============================================

    for step_index, step in enumerate(plan):

        print("\n===================")
        print(f"STEP {step_index + 1}")
        print("===================")

        target = step["target"]

        print("\nTarget:")
        print(target)

        # ============================================
        # TARGET CHECK
        # ============================================

        if target not in button_cache:

            print("\nTarget Not In Cache")

            reward = -10

            success = False

            print("\nPenalty Reward:")
            print(reward)

            trajectory_path = log_step(

                episode_id=episode_id,

                step=step_index + 1,

                action="tap",

                target=target,

                reward=reward,

                success=success
            )

            print("\nTrajectory Saved:")
            print(trajectory_path)

            continue

        # ============================================
        # GET COORDINATE
        # ============================================

        coordinate = button_cache[target]

        print("\nCached Coordinate:")
        print(coordinate)

        # ============================================
        # RL REFINEMENT
        # ============================================

        try:

            refined_coordinate = (
                agent.get_refined_coordinate(
                    coordinate
                )
            )

        except:

            refined_coordinate = (

                coordinate[0] + 1,
                coordinate[1] + 1
            )

        print("\nPredicted Coordinate:")
        print(refined_coordinate)

        # ============================================
        # EXECUTE TAP
        # ============================================

        tap_on_phone(

            refined_coordinate[0],
            refined_coordinate[1]
        )

        # ============================================
        # WAIT FOR UI UPDATE
        # ============================================

        time.sleep(1)

        # ============================================
        # CAPTURE UPDATED SCREEN
        # ============================================

        capture_screenshot()

        print("\nUpdated Screen Captured")

        # ============================================
        # EXPECTED OUTPUT
        # ============================================

        if target != "=":

            current_expression += target

            expected_expression = (
                current_expression
            )

        else:

            try:

                expected_expression = str(
                    eval(current_expression)
                )

            except:

                expected_expression = (
                    current_expression
                )

        # ============================================
        # VERIFY RESULT
        # ============================================

        success = verify_expression(
            expected_expression
        )

        # ============================================
        # REWARD
        # ============================================

        if success:

            reward = 10

            if target == "=":

                reward = 15

            print("\nACTION SUCCESS")

        else:

            reward = -5

            print("\nACTION FAILED")

        print("\nReward:")
        print(reward)

        # ============================================
        # RL UPDATE
        # ============================================

        try:

            agent.update_policy(
                reward=reward
            )

        except:
            pass

        # ============================================
        # SAVE TRAJECTORY
        # ============================================

        trajectory_path = log_step(

            episode_id=episode_id,

            step=step_index + 1,

            action="tap",

            target=target,

            reward=reward,

            success=success
        )

        print("\nTrajectory Saved:")
        print(trajectory_path)

    print("\n===================")
    print("PROCESS COMPLETED")
    print("===================")