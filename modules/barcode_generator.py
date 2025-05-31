import json
import os
from datetime import datetime

STATE_FILE = "barcode_state.json"

class BarcodeGenerator:
    def __init__(self):
        self.today = datetime.now().strftime("%m%d%Y")
        self.weekday = datetime.now().weekday()  # Monday = 0
        self.seq = 1
        self._load_state()

    def _load_state(self):
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r") as f:
                state = json.load(f)
            last_date = state.get("date")
            last_seq = state.get("seq", 0)

            if last_date == self.today and self.weekday != 0:
                self.seq = last_seq + 1
            elif self.weekday == 0 and last_date != self.today:
                self.seq = 1
            else:
                self.seq = last_seq + 1

    def _save_state(self):
        with open(STATE_FILE, "w") as f:
            json.dump({"date": self.today, "seq": self.seq}, f)

    def generate_barcode(self):
        barcode = f"{self.today}-{self.seq:03d}"
        self._save_state()
        self.seq += 1
        return barcode
