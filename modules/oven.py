import random

class Oven:
    def __init__(self):
        self.available_profiles = ["Standard"]

    def process(self, board):
        """Simulate reflow oven behavior and profile match check."""
        current_profile = random.choice(self.available_profiles)
        board.oven_profile = current_profile

        if current_profile == board.required_profile:
            board.status = "OVEN_MATCH"
        else:
            board.status = "OVEN_MISMATCH"

        return board
