import csv
import random
from modules.board import Board

class Unloader:
    def __init__(self):
        self.board_table = self.load_board_table()

    def load_board_table(self):
        """Load barcode/profile table from CSV."""
        with open("profiles/board_profiles.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)

    def process(self):
        """Simulate unloading a new board into the line."""
        entry = random.choice(self.board_table)
        board = Board(entry["barcode"], entry["required_profile"])
        board.status = "UNLOADED"
        return board
