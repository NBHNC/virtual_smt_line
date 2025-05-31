import random

class SPI:
    def process(self, board):
        """Simulate Solder Paste Inspection."""
        board.spi_result = random.choices(["PASS", "FAIL"], weights=[90, 10])[0]
        board.status = f"SPI_{board.spi_result}"
        return board
