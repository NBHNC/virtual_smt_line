from modules.board import Board
from modules.barcode_generator import BarcodeGenerator
import pandas as pd
from datetime import datetime

class Loader:
    def __init__(self):
        self.generator = BarcodeGenerator()
        self.current_board = None
        self.profile_df = pd.read_csv("profiles/board_profiles.csv")

    def load_board(self):
        barcode = self.generator.generate_barcode()
        pcb_name = "SG201_S1"
        revision = "A"

        # Lookup profile
        profile_row = self.profile_df[self.profile_df["board_name"] == pcb_name]
        if profile_row.empty:
            raise ValueError(f"No profile found for board: {pcb_name}")

        required_profile = profile_row.iloc[0]["required_profile"]

        # Generate simulated datamatrix payload
        datamatrix = f"PCB:{pcb_name} REV:{revision} PN:{barcode}"

        self.current_board = Board(barcode, required_profile)
        self.current_board.pcb_name = pcb_name
        self.current_board.revision = revision
        self.current_board.datamatrix = datamatrix

        return self.current_board
