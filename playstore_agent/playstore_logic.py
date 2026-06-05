import time

from adb_controller import (
    capture_phone_screen,
    tap,
    type_text,
    press_enter
)

from playstore_agent.ocr_utils import (
    find_text_element,
    verify_text_exists
)

from playstore_agent.planner import (
    create_playstore_plan
)

from playstore_agent.rl.reward_utils import (
    calculate_reward
)

from playstore_agent.trajectory_logger import (
    log_step
)

# ============================================
# SCREENSHOT PATH
# ============================================

SCREENSHOT_PATH = (
    "playstore_agent/screenshots/current_screen.png"
)

# ============================================
# OPEN PLAYSTORE
# ============================================

def open_playstore():

    capture_phone_screen()

    print("\nSearching For Play Store App")

    match = find_text_element(
        SCREENSHOT_PATH,
        "play"
    )

    if not match:

        print("\nPlay Store Not Found")

        return False

    x, y = match["coordinate"]

    print("\nOCR Match:")
    print(match["text"])
    print((x, y))

    tap(x, y)

    time.sleep(2)

    capture_phone_screen()

    return True

# ============================================
# TAP BOTTOM SEARCH
# ============================================

def tap_bottom_search():

    capture_phone_screen()

    print("\nSearching For Bottom Search Tab")

    matches = find_text_element(
        SCREENSHOT_PATH,
        "search",
        return_all=True
    )

    if not matches:

        return False

    best_match = None

    for match in matches:

        x, y = match["coordinate"]

        # Bottom navigation region
        if y > 2000:

            best_match = match
            break

    if not best_match:

        return False

    x, y = best_match["coordinate"]

    print("\nBottom Search Coordinate:")
    print((x, y))

    tap(x, y)

    time.sleep(1)

    capture_phone_screen()

    return verify_text_exists(
        SCREENSHOT_PATH,
        "search apps"
    )

# ============================================
# TAP TOP SEARCH FIELD
# ============================================

def tap_top_search():

    capture_phone_screen()

    print("\nSearching For Top Search Field")

    matches = find_text_element(
        SCREENSHOT_PATH,
        "search",
        return_all=True
    )

    if not matches:

        return False

    best_match = None

    for match in matches:

        x, y = match["coordinate"]

        # Top search bar region
        if y < 500:

            best_match = match
            break

    if not best_match:

        return False

    x, y = best_match["coordinate"]

    print("\nTop Search Coordinate:")
    print((x, y))

    tap(x, y)

    time.sleep(1)

    capture_phone_screen()

    return True

# ============================================
# TYPE QUERY
# ============================================

def type_app_name(app_name):

    print("\nTyping Query")

    type_text(app_name)

    time.sleep(1)

    capture_phone_screen()

    return verify_text_exists(
        SCREENSHOT_PATH,
        app_name.lower()
    )

# ============================================
# OPEN APP PAGE
# ============================================

def open_app_page(app_name):

    capture_phone_screen()

    print("\nSearching For App Result")

    matches = find_text_element(
        SCREENSHOT_PATH,
        app_name,
        return_all=True
    )

    if not matches:

        print("\nApp Result Not Found")

        return False

    valid_match = None

    for match in matches:

        x, y = match["coordinate"]

        # Ignore top search bar area
        if y < 400:

            continue

        valid_match = match
        break

    if not valid_match:

        print("\nNo Valid App Card Found")

        return False

    x, y = valid_match["coordinate"]

    print("\nApp Coordinate:")
    print((x, y))

    tap(x, y)

    time.sleep(2)

    capture_phone_screen()

    if verify_text_exists(
        SCREENSHOT_PATH,
        "install"
    ):

        return True

    if verify_text_exists(
        SCREENSHOT_PATH,
        "open"
    ):

        return True

    return False

# ============================================
# TAP INSTALL
# ============================================

def tap_install():

    capture_phone_screen()

    print("\nSearching For Install Button")

    matches = find_text_element(
        SCREENSHOT_PATH,
        "install",
        return_all=True
    )

    if not matches:

        return False

    best_match = None

    for match in matches:

        x, y = match["coordinate"]

        # Ignore keyboard region
        if y < 1800:

            best_match = match
            break

    if not best_match:

        return False

    x, y = best_match["coordinate"]

    print("\nInstall Coordinate:")
    print((x, y))

    tap(x, y)

    time.sleep(2)

    capture_phone_screen()

    return (

        verify_text_exists(
            SCREENSHOT_PATH,
            "cancel"
        )

        or

        verify_text_exists(
            SCREENSHOT_PATH,
            "open"
        )
    )

# ============================================
# MAIN AGENT
# ============================================

def run_playstore_agent(app_name):

    print("\n===================")
    print("PLAYSTORE AGENT")
    print("===================")

    print("\nCapturing Current Screen")

    capture_phone_screen()

    success = open_playstore()

    if not success:

        print("\nFailed To Open Play Store")

        return

    print("\nOpening Play Store")

    plan = create_playstore_plan(
        app_name
    )

    print("\nPLAN:")
    print(plan)

    episode_id = int(time.time())

    for step_id, step in enumerate(plan):

        print("\n===================")
        print(f"STEP {step_id + 1}")
        print("===================")

        action = step["action"]
        target = step["target"]

        print("\nAction:")
        print(action)

        print("\nTarget:")
        print(target)

        success = False

        # ====================================
        # ACTIONS
        # ====================================

        if action == "open_playstore":

            success = True

        elif action == "tap_bottom_search":

            success = tap_bottom_search()

        elif action == "tap_top_search":

            success = tap_top_search()

        elif action == "type_app_name":

            success = type_app_name(
                target
            )

        elif action == "press_enter":

            press_enter()

            time.sleep(2)

            success = True

        elif action == "open_app_page":

            success = open_app_page(
                target
            )

        elif action == "tap_install":

            success = tap_install()

        reward = calculate_reward(
            success
        )

        print("\nSUCCESS:")
        print(success)

        print("\nReward:")
        print(reward)

        trajectory_path = log_step(

            episode_id=episode_id,
            step=step_id + 1,
            action=action,
            target=target,
            reward=reward,
            success=success
        )

        print("\nTrajectory Saved:")
        print(trajectory_path)

    print("\n===================")
    print("PROCESS COMPLETED")
    print("===================")