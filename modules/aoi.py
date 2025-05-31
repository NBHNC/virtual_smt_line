import random

class AOI:
    def process(self, board):
        """Simulate Automated Optical Inspection."""
        # If SPI already failed, AOI fails automatically
        if board.spi_result == "FAIL":
            board.aoi_result = "FAIL"
        else:
            # 90% chance to pass, 10% fail
            board.aoi_result = random.choices(["PASS", "FAIL"], weights=[90, 10])[0]
        
        board.status = f"AOI_{board.aoi_result}"
        return board
