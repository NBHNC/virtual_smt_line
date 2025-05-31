import random

class SPI:
    def process(self, board):
        """Randomly mark board as passed or failed SPI."""
        board.spi_result = random.choice(["PASS", "FAIL"])
        board.status = f"SPI_{board.spi_result}"
        return board
