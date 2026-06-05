import os
import json
import time

# ============================================
# TRAJECTORY DIRECTORY
# ============================================

TRAJECTORY_DIR = (
    "playstore_agent/trajectories"
)

os.makedirs(

    TRAJECTORY_DIR,
    exist_ok=True
)

# ============================================
# SAVE STEP LOG
# ============================================

def log_step(

    episode_id,
    step,
    action,
    target,
    reward,
    success
):

    trajectory = {

        "episode_id": episode_id,

        "step": step,

        "action": action,

        "target": target,

        "reward": reward,

        "success": success,

        "timestamp": int(time.time())
    }

    filename = (

        f"episode_{episode_id}"
        f"_step_{step}.json"
    )

    save_path = os.path.join(

        TRAJECTORY_DIR,
        filename
    )

    with open(

        save_path,
        "w"
    ) as f:

        json.dump(

            trajectory,
            f,
            indent=4
        )

    return save_path