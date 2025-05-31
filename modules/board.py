class Board:
    def __init__(self, barcode, required_profile):
        self.barcode = barcode
        self.required_profile = required_profile
        self.status = "LOADED"