import random

class PickPlace:
    def process(self, board):
        """Simulate component placement with pass/fail."""
        board.placement_result = random.choices(["PASS", "FAIL"], weights=[95, 5])[0]
        board.status = f"P&P_{board.placement_result}"
        return board
