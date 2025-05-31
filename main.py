import PySimpleGUI as sg
from modules.loader import Loader
from modules.printer import Printer
from modules.spi import SPI
from modules.pickplace import PickPlace
from modules.oven import Oven
from modules.aoi import AOI
from modules.stacker import Stacker

loader = Loader()
printer = Printer()
spi = SPI()
pickplace = PickPlace()
oven = Oven()
aoi = AOI()
stacker = Stacker()

layout = [
    [sg.Text("Virtual SMT Line Simulator", font=("Arial", 16))],

    [sg.Button("Unload Board"),
     sg.Button("Paste Printer"),
     sg.Button("SPI Inspection"),
     sg.Button("Pick & Place"),
     sg.Button("Reflow Oven"),
     sg.Button("AOI Inspection"),
     sg.Button("Stacker"),
     sg.Button("Exit")],

    [sg.Multiline(size=(80, 20), key="-LOG-", autoscroll=True)],
]

window = sg.Window("SMT Line Simulator", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    elif event == "Unload Board":
        board = loader.load_board()
        loader.current_board = board
        window["-LOG-"].print(f"[UNLOADER] {board.datamatrix}")


    elif event == "Paste Printer":
        if loader.current_board:
            board = printer.process(loader.current_board)
            window["-LOG-"].print(f"[PRINTER] Printed board {board.datamatrix}")
        else:
            window["-LOG-"].print("[ERROR] No board available for printing")

    elif event == "SPI Inspection":
        if loader.current_board:
            board = spi.process(loader.current_board)
            window["-LOG-"].print(f"[SPI] {board.pcb_name} REV:{board.revision} ({board.datamatrix}) - {board.spi_result}")
        else:
            window["-LOG-"].print("[ERROR] No board available for SPI")

    elif event == "Pick & Place":
        if loader.current_board:
            board = pickplace.process(loader.current_board)
            window["-LOG-"].print(f"[P&P] {board.datamatrix} components placed")
        else:
            window["-LOG-"].print("[ERROR] No board available for P&P")

    elif event == "Reflow Oven":
        if loader.current_board:
            board = oven.process(loader.current_board)
            match_status = "MATCH" if board.status == "OVEN_MATCH" else "MISMATCH"
            window["-LOG-"].print(f"[OVEN] {board.datamatrix} reflowed using {board.oven_profile} ({match_status})")
        else:
            window["-LOG-"].print("[ERROR] No board available for oven")

    elif event == "AOI Inspection":
        if loader.current_board:
            board = aoi.process(loader.current_board)
            window["-LOG-"].print(f"[AOI] {board.datamatrix} - {board.aoi_result}")
        else:
            window["-LOG-"].print("[ERROR] No board available for AOI")

    elif event == "Stacker":
        if loader.current_board:
            board = stacker.process(loader.current_board)
            window["-LOG-"].print(f"[STACKER] {board.datamatrix} stacked and logged ({board.status})")
            loader.current_board = None
        else:
            window["-LOG-"].print("[ERROR] No board to stack")

window.close()
