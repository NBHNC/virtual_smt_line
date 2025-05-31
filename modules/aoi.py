import random

class AOI:
    def process(self, board):
        """Simulate Automated Optical Inspection."""
        if board.spi_result == "FAIL":
            board.aoi_result = "FAIL"
            board.status = "AOI_FAIL_SPI_DEPENDENT"
        else:
            board.aoi_result = random.choices(["PASS", "FAIL"], weights=[90, 10])[0]
            board.status = f"AOI_{board.aoi_result}"

        return board
