from modules.board import Board
from modules.barcode_generator import BarcodeGenerator
import pandas as pd

class Loader:
    def __init__(self):
        self.generator = BarcodeGenerator()
        self.current_board = None
        self.profile_df = pd.read_csv("profiles/board_profiles.csv")
        self.available_boards = self.profile_df["board_name"].dropna().unique().tolist()

    def load_board(self, pcb_name):
        barcode = self.generator.generate_barcode()
        revision = "A"

        # Lookup required profile
        profile_row = self.profile_df[self.profile_df["board_name"] == pcb_name]
        if profile_row.empty:
            raise ValueError(f"No profile found for board: {pcb_name}")
        required_profile = profile_row.iloc[0]["required_profile"]

        datamatrix = f"PCB:{pcb_name} REV:{revision} PN:{barcode}"

        self.current_board = Board(barcode, required_profile)
        self.current_board.pcb_name = pcb_name
        self.current_board.revision = revision
        self.current_board.datamatrix = datamatrix

        return self.current_board
