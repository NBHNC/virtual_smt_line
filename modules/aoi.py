import random


class AOI:
    def __init__(self, normal_pass_rate=0.90, released_spi_fail_rate=0.75):
        self.normal_pass_rate = normal_pass_rate
        self.released_spi_fail_rate = released_spi_fail_rate

    def process(self, board):
        # Default rule for normal production boards
        pass_chance = self.normal_pass_rate
        fail_chance = 1.0 - self.normal_pass_rate
        board.aoi_rule = "STANDARD_90_PASS"

        # If the board was previously held at SPI and later released,
        # give it a much higher chance of AOI failure
        if getattr(board, "spi_hold_released", False):
            fail_chance = self.released_spi_fail_rate
            pass_chance = 1.0 - fail_chance
            board.aoi_rule = "SPI_HOLD_RELEASED_75_FAIL"

        board.aoi_result = "PASS" if random.random() < pass_chance else "FAIL"

        if board.aoi_result == "PASS":
            board.status = "AOI_PASS"
        else:
            board.status = "AOI_FAIL"

        board.aoi_pass_chance = round(pass_chance, 2)
        board.aoi_fail_chance = round(fail_chance, 2)

        return board