import torch
import torch.nn as nn

# ============================================
# DQN MODEL
# ============================================

class DQN(nn.Module):

    def __init__(self):

        super().__init__()

        self.net = nn.Sequential(

            nn.Linear(
                4,
                512
            ),

            nn.ReLU(),

            nn.BatchNorm1d(
                512
            ),

            nn.Dropout(
                0.30
            ),

            nn.Linear(
                512,
                256
            ),

            nn.ReLU(),

            nn.BatchNorm1d(
                256
            ),

            nn.Dropout(
                0.25
            ),

            nn.Linear(
                256,
                128
            ),

            nn.ReLU(),

            nn.Linear(
                128,
                64
            ),

            nn.ReLU(),

            nn.Linear(
                64,
                32
            ),

            nn.ReLU(),

            nn.Linear(
                32,
                9
            )
        )

    def forward(
        self,
        x
    ):

        return self.net(x)

# ============================================
# RL AGENT
# ============================================

class RLAgent:

    def __init__(self):

        self.device = torch.device(

            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        self.model = DQN().to(
            self.device
        )

        self.model.load_state_dict(

            torch.load(

                "youtube_agent/rl/best_youtube_dqn.pth",

                map_location=self.device
            )
        )

        self.model.eval()

        self.action_map = {

            0: (-20, -20),
            1: (-20, 0),
            2: (-20, 20),

            3: (0, -20),
            4: (0, 0),
            5: (0, 20),

            6: (20, -20),
            7: (20, 0),
            8: (20, 20)
        }

    # ============================================
    # GET REFINED COORDINATE
    # ============================================

    def get_refined_coordinate(

        self,
        target,
        base_coordinate,
        confidence=0.5,
        step=1
    ):

        x, y = base_coordinate

        state = torch.tensor(

            [
                [
                    float(x),
                    float(y),
                    float(confidence),
                    float(step)
                ]
            ],

            dtype=torch.float32

        ).to(self.device)

        with torch.no_grad():

            q_values = self.model(
                state
            )

            action = torch.argmax(
                q_values
            ).item()

        dx, dy = self.action_map[
            action
        ]

        refined_x = int(
            x + dx
        )

        refined_y = int(
            y + dy
        )

        print(
            f"\nRL Action: {action}"
        )

        print(
            f"Offset: ({dx},{dy})"
        )

        return (

            refined_x,
            refined_y,
            action
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

        pass