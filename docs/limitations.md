# Limitations

Despite demonstrating successful mobile GUI automation, the current framework has several limitations.

## Grounding Accuracy

Grounding DINO may struggle with fine-grained user interface components, particularly when multiple visually similar elements are present on the screen.

## Coordinate Precision

Accurate coordinate prediction remains challenging due to differences in screen resolutions, device layouts, and dynamic interface changes.

## General-Purpose Vision-Language Model

Qwen2-VL is a general-purpose Vision-Language Model and is not specifically optimized for mobile GUI reasoning. Consequently, some planning decisions may not fully align with application-specific workflows.

## Computational Constraints

Training and experimentation were performed under limited cloud GPU resources. This required separating certain training and execution processes and restricted large-scale reinforcement learning experiments.

## Reinforcement Learning Scalability

Effective reinforcement learning requires a large number of interaction episodes. Generating high-quality trajectories and training robust policies remains computationally expensive.
