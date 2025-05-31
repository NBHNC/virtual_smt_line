import csv
import os

class Stacker:
    def process(self, board):
        """Simulate stacking and finalize board log."""
        board.status = "COMPLETED"

        os.makedirs("logs", exist_ok=True)
        log_path = "logs/trace.csv"
        write_header = not os.path.exists(log_path)

        with open(log_path, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            if write_header:
                writer.writerow([
                    "Barcode",
                    "Required Profile",
                    "SPI Result",
                    "Oven Profile",
                    "AOI Result",
                    "Final Status"
                ])
            writer.writerow([
                board.barcode,
                board.required_profile,
                board.spi_result,
                board.oven_profile,
                board.aoi_result,
                board.status
            ])

        return board
