import os
import time

# ============================================
# SCREENSHOT
# ============================================

def capture_phone_screen():

    # ========================================
    # CREATE DIRECTORIES
    # ========================================

    os.makedirs(
        "calculator_agent/screenshots",
        exist_ok=True
    )

    os.makedirs(
        "google_agent/screenshots",
        exist_ok=True
    )

    os.makedirs(
        "playstore_agent/screenshots",
        exist_ok=True
    )

    os.makedirs(
        "youtube_agent/screenshots",
        exist_ok=True
    )

    # ========================================
    # CAPTURE SCREENSHOT ON DEVICE
    # ========================================

    os.system(
        "adb shell screencap -p /sdcard/current_screen.png"
    )

    time.sleep(0.5)

    # ========================================
    # COPY TO CALCULATOR AGENT
    # ========================================

    os.system(

        "adb pull /sdcard/current_screen.png "
        "calculator_agent/screenshots/current_screen.png"
    )

    # ========================================
    # COPY TO GOOGLE AGENT
    # ========================================

    os.system(

        "adb pull /sdcard/current_screen.png "
        "google_agent/screenshots/current_screen.png"
    )

    # ========================================
    # COPY TO PLAYSTORE AGENT
    # ========================================

    os.system(

        "adb pull /sdcard/current_screen.png "
        "playstore_agent/screenshots/current_screen.png"
    )

    # ========================================
    # COPY TO YOUTUBE AGENT
    # ========================================

    os.system(

        "adb pull /sdcard/current_screen.png "
        "youtube_agent/screenshots/current_screen.png"
    )

    return (
        "/sdcard/current_screen.png"
    )

# ============================================
# BACKWARD COMPATIBILITY
# ============================================

def capture_screenshot():

    return capture_phone_screen()

# ============================================
# TAP
# ============================================

def tap(x, y):

    os.system(
        f"adb shell input tap {x} {y}"
    )

# backward compatibility

def tap_on_phone(x, y):

    tap(x, y)

def tap_on_screen(x, y):

    tap(x, y)

# ============================================
# SWIPE
# ============================================

def swipe(
    x1,
    y1,
    x2,
    y2,
    duration=300
):

    os.system(

        f"adb shell input swipe "
        f"{x1} {y1} {x2} {y2} {duration}"
    )

# backward compatibility

def swipe_on_screen(
    x1,
    y1,
    x2,
    y2,
    duration=300
):

    swipe(
        x1,
        y1,
        x2,
        y2,
        duration
    )

# ============================================
# SWIPE UP
# ============================================

def swipe_up():

    swipe(
        540,
        1800,
        540,
        400,
        300
    )

# ============================================
# SWIPE DOWN
# ============================================

def swipe_down():

    swipe(
        540,
        400,
        540,
        1800,
        300
    )

# ============================================
# SWIPE LEFT
# ============================================

def swipe_left():

    swipe(
        900,
        1200,
        200,
        1200,
        300
    )

# ============================================
# SWIPE RIGHT
# ============================================

def swipe_right():

    swipe(
        200,
        1200,
        900,
        1200,
        300
    )

# ============================================
# TYPE TEXT
# ============================================

def type_text(text):

    text = text.replace(
        " ",
        "%s"
    )

    os.system(
        f'adb shell input text "{text}"'
    )

# ============================================
# KEY EVENTS
# ============================================

def press_enter():

    os.system(
        "adb shell input keyevent 66"
    )

# backward compatibility

def press_enter_key():

    press_enter()

# ============================================
# PRESS BACK
# ============================================

def press_back():

    os.system(
        "adb shell input keyevent 4"
    )

# ============================================
# PRESS HOME
# ============================================

def press_home():

    os.system(
        "adb shell input keyevent 3"
    )