import random

from calculator_agent.rl.policy_network import (
    PolicyNetwork
)

# ============================================
# RL AGENT
# ============================================

class RLAgent:

    def __init__(self):

        self.policy = PolicyNetwork()

    # ============================================
    # GET REFINED COORDINATE
    # ============================================

    def get_refined_coordinate(

        self,
        target,
        base_coordinate
    ):

        x, y = base_coordinate

        dx = random.randint(-5, 5)
        dy = random.randint(-5, 5)

        predicted_x = x + dx
        predicted_y = y + dy

        return (
            predicted_x,
            predicted_y
        )

    # ============================================
    # UPDATE POLICY
    # ============================================

    def update_policy(

        self,
        target,
        reward,
        base_coordinate,
        refined_coordinate
    ):

        self.policy.update(

            target=target,

            reward=reward,

            base_coordinate=base_coordinate,

            refined_coordinate=refined_coordinate
        )