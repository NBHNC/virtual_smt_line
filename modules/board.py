class Board:
    def __init__(self, barcode, required_profile):
        self.barcode = barcode
        self.required_profile = required_profile
        self.status = "UNLOADED"
        self.spi_result = None
        self.aoi_result = None
        self.oven_profile = None
        self.process_log = []  # Optional: Track step-by-step events
