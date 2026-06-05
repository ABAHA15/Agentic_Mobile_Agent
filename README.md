# Agentic Mobile Automation Framework

A lightweight multimodal mobile GUI automation framework that combines Computer Vision, OCR, Reinforcement Learning, and Android Debug Bridge (ADB) to autonomously interact with Android applications.

The framework integrates YOLOv8, EasyOCR, Grounding DINO, and Double DQN Reinforcement Learning to understand mobile interfaces, locate GUI elements, and execute actions without predefined automation scripts.

---

# Overview

Modern mobile applications contain complex graphical user interfaces that are difficult to automate using traditional rule-based approaches.

This project proposes an Agentic Mobile Automation Framework capable of:

* Understanding mobile screens
* Detecting GUI elements
* Extracting textual information
* Grounding visual targets
* Executing Android actions
* Learning interaction strategies

The framework was evaluated on multiple Android applications including Calculator, Play Store, and YouTube.

---

# System Architecture

```text
Android Device
      │
      ▼
Screenshot Capture (ADB)
      │
      ▼
YOLOv8 GUI Detection
      │
      ▼
EasyOCR Text Extraction
      │
      ▼
Grounding DINO Fallback
      │
      ▼
Task Planning
      │
      ▼
Double DQN Policy Refinement
      │
      ▼
ADB Action Execution
      │
      ▼
Feedback & Reflection
```

---

# Core Components

| Component         | Purpose                 |
| ----------------- | ----------------------- |
| YOLOv8s           | GUI Element Detection   |
| EasyOCR           | Text Recognition        |
| Grounding DINO    | Semantic Grounding      |
| ADB               | Android Device Control  |
| Double DQN        | Coordinate Optimization |
| Reflection Module | Failure Recovery        |
| Trajectory Logger | Interaction Logging     |

---

# Agents

## Calculator Agent

Performs arithmetic operations by:

* Detecting calculator buttons
* Localizing coordinates
* Executing tap actions
* Validating numerical outputs

---

## Play Store Agent

Automates application search tasks by:

* Detecting search interfaces
* Entering search queries
* Navigating search results
* Recording interaction trajectories

---

## YouTube Agent

Performs video search and navigation tasks while integrating Double DQN-based coordinate refinement.

Capabilities include:

* Search execution
* Result selection
* Coordinate optimization
* Reward-driven learning

---

# YOLOv8 Fine-Tuning

YOLOv8s was fine-tuned on the Mobile GUI Dataset.

### Performance

| Metric    | Value  |
| --------- | ------ |
| Precision | 0.8044 |
| Recall    | 0.8018 |
| mAP50     | 0.8504 |
| mAP50-95  | 0.6915 |

The detector successfully localized buttons, icons, search bars, and other interactive GUI elements.

---

# Reinforcement Learning

The framework incorporates Double Deep Q-Network (Double DQN) learning for coordinate refinement.

### Training Configuration

* Epochs: 20
* Optimizer: AdamW
* Learning Rate: 1e-4
* Batch Size: 512
* Discount Factor (γ): 0.90
* Loss Function: Huber Loss

Double DQN reduces Q-value overestimation by separating action selection and action evaluation networks.

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd Agentic-Mobile-Agent
```

## Install Dependencies

```bash
pip install -r requirements.txt
pip install git+https://github.com/IDEA-Research/GroundingDINO.git
```

---

# Android Setup

Enable:

* Developer Options
* USB Debugging

Verify connection:

```bash
adb devices
```

---

# Running Agents

## Calculator Agent

```bash
python -m calculator_agent.main
```

## Play Store Agent

```bash
python -m playstore_agent.main
```

## YouTube Agent

```bash
python -m youtube_agent.main
```

---

# Repository Structure


Agentic-Mobile-Agent/
│
├── adb_controller.py
├── best.pt
├── README.md
├── requirements.txt
│
├── calculator_agent/
├── playstore_agent/
├── youtube_agent/
│
├── docs/
│   ├── methodology.md
│   ├── limitations.md
│   └── future_work.md
│
└── policies/


---

# Current Limitations

* Fine-grained GUI grounding remains challenging.
* Dynamic UI layouts can affect localization accuracy.
* Reinforcement learning requires additional interaction data.
* Generalization to unseen applications remains an open problem.

---

# Future Work

* GUI-specific grounding models
* PPO and A2C integration
* Real-time screen streaming
* Larger trajectory datasets
* End-to-end policy learning

---

# Author

**Abaha Mondal**

Master's in Big Data Analytics

Ramakrishna Mission Vivekananda Educational and Research Institute

---

# Disclaimer

This project is an academic research prototype developed for studying mobile GUI automation through multimodal perception and reinforcement learning.
