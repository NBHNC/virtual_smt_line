import random

class Oven:
    def __init__(self):
        self.available_profiles = ["38cpmPB-FREE_STANDARD", "LEAD_STANDARD", "HIGH_TEMP"]
        self.current_profile = "38cpmPB-FREE_STANDARD"

    def process(self, board):
        """Simulate reflow oven behavior and profile match check."""
        board.oven_profile = self.current_profile

        if board.required_profile == self.current_profile:
            board.status = "OVEN_MATCH"
            board.oven_result = "PASS"
        else:
            board.status = "OVEN_MISMATCH"
            board.oven_result = "FAIL"

        return board
