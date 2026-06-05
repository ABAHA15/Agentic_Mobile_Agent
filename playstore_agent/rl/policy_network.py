import random

# ============================================
# POLICY NETWORK
# ============================================

class PolicyNetwork:

    def __init__(self):

        self.memory = {}

    # ============================================
    # UPDATE POLICY
    # ============================================

    def update(

        self,

        target,

        reward,

        base_coordinate=None,

        refined_coordinate=None
    ):

        if target not in self.memory:

            self.memory[target] = []

        self.memory[target].append({

            "reward": reward,

            "base_coordinate":
            base_coordinate,

            "refined_coordinate":
            refined_coordinate
        })

    # ============================================
    # GET MEMORY
    # ============================================

    def get_memory(self):

        return self.memory