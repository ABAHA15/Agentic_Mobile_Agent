# Methodology

The proposed Agentic Mobile Automation Framework combines computer vision, optical character recognition, reinforcement learning, and Android device control to enable autonomous interaction with mobile applications.

## Vision-Language Reasoning

High-level task understanding and planning are performed using Qwen2-VL. User instructions are converted into executable actions, enabling the agent to determine the next interaction required on the mobile interface.

## GUI Element Detection

A fine-tuned YOLOv8s model is used to detect mobile GUI elements such as buttons, icons, search bars, and interactive components. The detector provides bounding box coordinates and confidence scores for each detected element.

## Text Recognition

EasyOCR is employed to extract textual information from screenshots. The OCR module returns both recognized text and corresponding bounding box coordinates, allowing the agent to identify text-based interface elements.

## Semantic Grounding

Grounding DINO serves as a fallback semantic grounding module. When GUI elements cannot be reliably detected using YOLO or OCR, Grounding DINO localizes interface elements based on textual prompts and visual context.

## Mobile Interaction

Android Debug Bridge (ADB) is used to execute actions on the device. The framework supports tap, swipe, scroll, text input, and navigation commands through coordinate-based interactions.

## Reinforcement Learning

A Double Deep Q-Network (Double DQN) is incorporated to refine coordinate selection and improve interaction accuracy. The agent learns from execution feedback and updates its policy based on observed rewards.

## Memory and Reflection

A lightweight memory mechanism stores information about recurring screen layouts and previous actions. Reflection modules analyze execution outcomes and help the agent recover from failed interactions.
