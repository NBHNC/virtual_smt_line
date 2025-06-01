import csv
import os

class Stacker:
    def __init__(self):
        self.rework_queue = []

    def process(self, board):
        """Simulate stacking and finalize board log."""
        if board.placement_result == "FAIL" or board.aoi_result == "FAIL":
            board.status = "FAILED"
            self.rework_queue.append(board)
        else:
            board.status = "COMPLETED"

        os.makedirs("logs", exist_ok=True)
        log_path = "logs/trace.csv"
        write_header = not os.path.exists(log_path)

        with open(log_path, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=[
                "PCB Name",
                "Revision",
                "Barcode",
                "Datamatrix",
                "Required Profile",
                "Oven Profile",
                "SPI Result",
                "Placement Result",
                "AOI Result",
                "Final Status"
            ])
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
                "Placement Result": board.placement_result,
                "AOI Result": board.aoi_result,
                "Final Status": board.status
            })

        return board
