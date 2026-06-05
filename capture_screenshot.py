import os
import time
import subprocess
from datetime import datetime

# ======================================
# APP CONFIGURATION
# ======================================

APP_NAME = "flipkart"

# Options:
# google
# calculator
# flipkart

CAPTURE_INTERVAL = 1

# ======================================
# ADB PATH
# ======================================

ADB_PATH = r"C:\Users\user\Downloads\platform-tools\adb.exe"

# ======================================
# SAVE DIRECTORY
# ======================================

SAVE_DIR = os.path.join(
    "mobile_gui_dataset",
    "raw_images",
    APP_NAME
)

os.makedirs(SAVE_DIR, exist_ok=True)

print(f"\nSaving screenshots to:")
print(SAVE_DIR)

print("\nPress CTRL + C to stop.\n")

count = 0

try:

    while True:

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S_%f"
        )

        filename = f"{APP_NAME}_{timestamp}.png"

        device_path = "/sdcard/temp_screen.png"

        local_path = os.path.join(
            SAVE_DIR,
            filename
        )

        # ======================================
        # Capture screenshot on phone
        # ======================================

        subprocess.run([
            ADB_PATH,
            "shell",
            "screencap",
            "-p",
            device_path
        ])

        # ======================================
        # Pull screenshot to laptop
        # ======================================

        subprocess.run([
            ADB_PATH,
            "pull",
            device_path,
            local_path
        ])

        count += 1

        print(f"[{count}] Saved: {filename}")

        time.sleep(CAPTURE_INTERVAL)

except KeyboardInterrupt:

    print("\nStopped screenshot collection.")