class Board:
    def __init__(self, barcode, required_profile):
        self.barcode = barcode
        self.required_profile = required_profile

        self.pcb_name = ""
        self.revision = ""
        self.datamatrix = ""

        self.status = "UNLOADED"
        self.spi_result = None
        self.placement_result = None
        self.oven_profile = None
        self.aoi_result = None

        self.rework_count = 0
        self.is_rework = False

        # Future-use flag for boards that fail SPI,
        # are reviewed, and are later released forward
        self.spi_hold_released = False

        # Optional AOI debug fields
        self.aoi_rule = ""
        self.aoi_pass_chance = None
        self.aoi_fail_chance = None