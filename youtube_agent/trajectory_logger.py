import os
import json
import time

TRAJECTORY_DIR = (
    "youtube_agent/trajectories"
)

os.makedirs(
    TRAJECTORY_DIR,
    exist_ok=True
)

def log_step(
    episode_id,
    step,
    action,
    target,
    reward,
    success,

    x=None,
    y=None,

    confidence=None,

    class_name=None,

    bbox=None,

    state=None,
    action_id=None,
    next_state=None,
    done=False
):

    trajectory = {

        "episode_id": episode_id,

        "step": step,

        "action": action,

        "target": target,

        "reward": reward,

        "success": success,

        "timestamp": int(time.time()),

        "x": x,
        "y": y,

        "confidence": confidence,

        "class_name": class_name,

        "bbox": bbox,

        "state": state,

        "action_id": action_id,

        "next_state": next_state,

        "done": done
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

    print(
        f"\nTrajectory Saved:\n{save_path}"
    )

    return save_path