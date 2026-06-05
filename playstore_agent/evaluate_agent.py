import os
import json
import glob

import pandas as pd
import matplotlib.pyplot as plt

# ====================================
# DIRECTORIES
# ====================================

TRAJECTORY_DIR = (
    "playstore_agent/trajectories"
)

OUTPUT_DIR = (
    "playstore_agent/output"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# ====================================
# LOAD TRAJECTORIES
# ====================================

def load_trajectories():

    files = glob.glob(

        os.path.join(
            TRAJECTORY_DIR,
            "*.json"
        )
    )

    data = []

    for file in files:

        try:

            with open(
                file,
                "r"
            ) as f:

                item = json.load(f)

                data.append(item)

        except Exception as e:

            print(
                f"Error reading {file}: {e}"
            )

    return data

# ====================================
# BUILD DATAFRAME
# ====================================

def build_dataframe(data):

    rows = []

    for item in data:

        success_value = item.get(
            "success",
            False
        )

        if success_value is None:
            success_value = False

        row = {

            "episode_id":
            item.get("episode_id", 0),

            "step":
            item.get("step", 0),

            "action":
            item.get("action", ""),

            "target":
            item.get("target", ""),

            "reward":
            item.get("reward", 0),

            "success":
            success_value,

            "timestamp":
            item.get("timestamp", 0)
        }

        rows.append(row)

    df = pd.DataFrame(rows)

    return df

# ====================================
# METRICS
# ====================================

def compute_metrics(df):

    total_steps = len(df)

    successful_steps = (

        df["success"] == True

    ).sum()

    failed_steps = (

        df["success"] == False

    ).sum()

    accuracy = (

        successful_steps
        /
        total_steps

    ) * 100 if total_steps > 0 else 0

    avg_reward = (
        df["reward"].mean()
    )

    metrics = {

        "total_steps":
        int(total_steps),

        "successful_steps":
        int(successful_steps),

        "failed_steps":
        int(failed_steps),

        "accuracy":
        round(accuracy, 2),

        "average_reward":
        round(avg_reward, 2)
    }

    return metrics

# ====================================
# SAVE METRICS
# ====================================

def save_metrics(metrics):

    output_path = os.path.join(

        OUTPUT_DIR,

        "metrics.json"
    )

    with open(
        output_path,
        "w"
    ) as f:

        json.dump(

            metrics,

            f,

            indent=4
        )

    print("\nMetrics Saved:")
    print(output_path)

# ====================================
# REWARD TREND
# ====================================

def plot_reward_trend(df):

    plt.figure(figsize=(10, 5))

    plt.plot(
        df.index,
        df["reward"]
    )

    plt.xlabel("Step")

    plt.ylabel("Reward")

    plt.title("Reward Trend")

    save_path = os.path.join(

        OUTPUT_DIR,

        "reward_trend.png"
    )

    plt.savefig(save_path)

    print("\nSaved:")
    print(save_path)

    plt.close()

# ====================================
# SUCCESS FAILURE
# ====================================

def plot_success_failure(df):

    success_count = (

        df["success"] == True

    ).sum()

    failure_count = (

        df["success"] == False

    ).sum()

    plt.figure(figsize=(6, 6))

    plt.pie(

        [success_count, failure_count],

        labels=[
            "Success",
            "Failure"
        ],

        autopct="%1.1f%%"
    )

    plt.title(
        "Success vs Failure"
    )

    save_path = os.path.join(

        OUTPUT_DIR,

        "success_failure.png"
    )

    plt.savefig(save_path)

    print("\nSaved:")
    print(save_path)

    plt.close()

# ====================================
# ACTION DISTRIBUTION
# ====================================

def plot_action_distribution(df):

    counts = df[
        "action"
    ].value_counts()

    plt.figure(figsize=(10, 5))

    counts.plot(
        kind="bar"
    )

    plt.xlabel("Action")

    plt.ylabel("Frequency")

    plt.title(
        "Action Distribution"
    )

    save_path = os.path.join(

        OUTPUT_DIR,

        "action_distribution.png"
    )

    plt.savefig(save_path)

    print("\nSaved:")
    print(save_path)

    plt.close()

# ====================================
# SUCCESS OVER TIME
# ====================================

def plot_success_over_time(df):

    success_numeric = (

        df["success"]

        .fillna(False)

        .astype(bool)

        .astype(int)
    )

    cumulative_accuracy = (

        success_numeric.cumsum()

        /

        range(1, len(df) + 1)

    ) * 100

    plt.figure(figsize=(10, 5))

    plt.plot(cumulative_accuracy)

    plt.xlabel("Step")

    plt.ylabel("Cumulative Accuracy (%)")

    plt.title(
        "Learning Curve"
    )

    save_path = os.path.join(

        OUTPUT_DIR,

        "learning_curve.png"
    )

    plt.savefig(save_path)

    print("\nSaved:")
    print(save_path)

    plt.close()

# ====================================
# MOVING AVERAGE REWARD
# ====================================

def plot_moving_average_reward(df):

    moving_avg = df[
        "reward"
    ].rolling(
        window=5,
        min_periods=1
    ).mean()

    plt.figure(figsize=(10, 5))

    plt.plot(moving_avg)

    plt.xlabel("Step")

    plt.ylabel("Moving Avg Reward")

    plt.title(
        "Moving Average Reward"
    )

    save_path = os.path.join(

        OUTPUT_DIR,

        "moving_average_reward.png"
    )

    plt.savefig(save_path)

    print("\nSaved:")
    print(save_path)

    plt.close()

# ====================================
# ACTION SUCCESS RATE
# ====================================

def plot_action_success_rate(df):

    grouped = df.groupby(
        "action"
    )["success"].mean()

    grouped = grouped * 100

    plt.figure(figsize=(10, 5))

    grouped.plot(
        kind="bar"
    )

    plt.ylabel(
        "Success Rate (%)"
    )

    plt.title(
        "Action Success Rate"
    )

    save_path = os.path.join(

        OUTPUT_DIR,

        "action_success_rate.png"
    )

    plt.savefig(save_path)

    print("\nSaved:")
    print(save_path)

    plt.close()

# ====================================
# MAIN
# ====================================

def main():

    data = load_trajectories()

    if len(data) == 0:

        print(
            "No trajectories found"
        )

        return

    df = build_dataframe(data)

    metrics = compute_metrics(df)

    print("\n===================")
    print("PERFORMANCE METRICS")
    print("===================")

    for key, value in metrics.items():

        print(f"{key}: {value}")

    save_metrics(metrics)

    # =================================
    # GENERATE PLOTS
    # =================================

    plot_reward_trend(df)

    plot_success_failure(df)

    plot_action_distribution(df)

    plot_success_over_time(df)

    plot_moving_average_reward(df)

    plot_action_success_rate(df)

    print("\n===================")
    print("EVALUATION COMPLETE")
    print("===================")

# ====================================
# ENTRY
# ====================================

if __name__ == "__main__":

    main()