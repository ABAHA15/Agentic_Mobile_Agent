import random


class ReplayBuffer:

    def __init__(self):

        self.buffer = []

    def add(
        self,
        transition
    ):

        self.buffer.append(
            transition
        )

    def sample(
        self,
        batch_size
    ):

        return random.sample(
            self.buffer,
            min(
                batch_size,
                len(self.buffer)
            )
        )

    def size(self):

        return len(self.buffer)