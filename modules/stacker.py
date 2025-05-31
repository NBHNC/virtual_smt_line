import csv
import os

class Stacker:
    def process(self, board):
        """Simulate stacking and finalize board log."""
        board.status = "COMPLETED"

        os.makedirs("logs", exist_ok=True)
        log_path = "logs/trace.csv"
        write_header = not os.path.exists(log_path)

        fieldnames = [
            "PCB Name", "Revision", "Barcode", "Datamatrix",
            "Required Profile", "Oven Profile", "SPI Result",
            "AOI Result", "Final Status"
        ]

        with open(log_path, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if write_header:
                writer.writeheader()

            writer.writerow({
                "PCB Name": board.pcb_name,
                "Revision": board.revision,
                "Barcode": board.barcode,
                "Datamatrix": board.datamatrix,
                "Required Profile": board.required_profile,
                "Oven Profile": board.oven_profile,
                "SPI Result": board.spi_result,
                "AOI Result": board.aoi_result,
                "Final Status": board.status
            })

        return board
