import csv
import random
from modules.board import Board

class Loader:
    def __init__(self):
        self.board_table = self.load_board_table()
        self.current_board = None

    def load_board_table(self):
        with open("profiles/board_profiles.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)

    def load_board(self):
        entry = random.choice(self.board_table)
        self.current_board = Board(entry["barcode"], entry["required_profile"])
        return self.current_board