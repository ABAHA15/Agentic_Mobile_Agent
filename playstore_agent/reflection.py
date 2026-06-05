from playstore_agent.ocr_utils import (
    extract_full_screen_text
)

# ============================================
# SCREENSHOT PATH
# ============================================

SCREENSHOT_PATH = (
    "playstore_agent/screenshots/current_screen.png"
)

# ============================================
# VERIFY SEARCH BAR OPENED
# ============================================

def verify_search_bar_opened():

    screen_text = extract_full_screen_text(
        SCREENSHOT_PATH
    )

    screen_text = screen_text.lower()

    verification_targets = [

        "search apps",
        "search apps & games",
        "search for apps",
        "search"
    ]

    for target in verification_targets:

        if target in screen_text:

            return True

    return False

# ============================================
# VERIFY QUERY TYPED
# ============================================

def verify_query_typed(app_name):

    screen_text = extract_full_screen_text(
        SCREENSHOT_PATH
    )

    screen_text = screen_text.lower()

    app_name = app_name.lower()

    return app_name in screen_text

# ============================================
# VERIFY APP PAGE OPENED
# ============================================

def verify_app_page_opened(app_name):

    screen_text = extract_full_screen_text(
        SCREENSHOT_PATH
    )

    screen_text = screen_text.lower()

    app_name = app_name.lower()

    install_keywords = [

        "install",
        "update",
        "open"
    ]

    app_visible = (
        app_name in screen_text
    )

    install_visible = False

    for keyword in install_keywords:

        if keyword in screen_text:

            install_visible = True
            break

    return (

        app_visible and
        install_visible
    )

# ============================================
# VERIFY INSTALL STARTED
# ============================================

def verify_install_started():

    screen_text = extract_full_screen_text(
        SCREENSHOT_PATH
    )

    screen_text = screen_text.lower()

    verification_targets = [

        "pending",
        "installing",
        "cancel",
        "open"
    ]

    for target in verification_targets:

        if target in screen_text:

            return True

    return False

# ============================================
# COMPUTE REWARD
# ============================================

def compute_reward(

    action,
    success
):

    if not success:

        return -5

    # ============================================
    # HIGH VALUE ACTIONS
    # ============================================

    if action == "tap_install":

        return 25

    if action == "open_app_page":

        return 15

    if action == "type_app_name":

        return 10

    if action == "tap_search_bar":

        return 10

    if action == "press_enter":

        return 10

    return 5