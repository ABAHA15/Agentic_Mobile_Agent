import os
import json
import time

# ============================================
# TRAJECTORY DIRECTORY
# ============================================

TRAJECTORY_DIR = (
    "calculator_agent/trajectories"
)

os.makedirs(
    TRAJECTORY_DIR,
    exist_ok=True
)

# ============================================
# LOG STEP
# ============================================

def log_step(

    episode_id,

    step,

    action,

    target,

    reward,

    success
):

    filename = (

        f"episode_{episode_id}"
        f"_step_{step}.json"
    )

    save_path = os.path.join(
        TRAJECTORY_DIR,
        filename
    )

    data = {

        "episode_id":
        episode_id,

        "step":
        step,

        "action":
        action,

        "target":
        target,

        "reward":
        reward,

        "success":
        success,

        "timestamp":
        int(time.time())
    }

    with open(
        save_path,
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )

    return save_path