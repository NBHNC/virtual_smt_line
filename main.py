import PySimpleGUI as sg
from modules.loader import Loader
from modules.printer import Printer
from modules.spi import SPI
from modules.pickplace import PickPlace
from modules.oven import Oven
from modules.aoi import AOI
from modules.stacker import Stacker

rework_queue = []
rework_board = None
loader = Loader()
printer = Printer()
spi = SPI()
pickplace = PickPlace()
oven = Oven()
aoi = AOI()
stacker = Stacker()

layout = [
    [sg.Text("Virtual SMT Line Simulator", font=("Arial", 16))],
    [sg.Button("Unload Board", key="Unload", disabled=False),
     sg.Button("Paste Printer", key="Printer", disabled=True),
     sg.Button("SPI Inspection", key="SPI", disabled=True),
     sg.Button("Pick & Place", key="P&P", disabled=True),
     sg.Button("Reflow Oven", key="Oven", disabled=True),
     sg.Button("AOI Inspection", key="AOI", disabled=True),
     sg.Button("Start Rework", key="StartRework"),
     sg.Button("Solder City", key="SolderCity"),
     sg.Button("AOI Recheck", key="AOIRecheck"),
     sg.Button("Exit")],
    [sg.Multiline(size=(80, 20), key="-LOG-", autoscroll=True)],
]

window = sg.Window("SMT Line Simulator", layout, finalize=True)

def set_step_state(step):
    states = {
        "Unload": ["Printer"],
        "Printer": ["SPI"],
        "SPI": ["P&P"],
        "P&P": ["Oven"],
        "Oven": ["AOI"],
        "AOI": ["Unload"],
    }
    for key in ["Unload", "Printer", "SPI", "P&P", "Oven", "AOI"]:
        window[key].update(disabled=True)
    for key in states.get(step, []):
        window[key].update(disabled=False)

# Initial state
for key in ["Unload", "Printer", "SPI", "P&P", "Oven", "AOI"]:
    window[key].update(disabled=True)
window["Unload"].update(disabled=False)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    elif event == "Unload":
        board = loader.load_board("SG201_S1")
        loader.current_board = board
        window["-LOG-"].print(f"[UNLOADER] {board.datamatrix}")
        set_step_state("Unload")

    elif event == "Printer":
        if loader.current_board:
            board = printer.process(loader.current_board)
            window["-LOG-"].print(f"[PRINTER] Printed board {board.datamatrix}")
            set_step_state("Printer")
        else:
            window["-LOG-"].print("[ERROR] No board available for printing")

    elif event == "SPI":
        if loader.current_board:
            board = spi.process(loader.current_board)
            window["-LOG-"].print(f"[SPI] {board.pcb_name} REV:{board.revision} ({board.datamatrix}) - {board.spi_result}")
            set_step_state("SPI")
        else:
            window["-LOG-"].print("[ERROR] No board available for SPI")

    elif event == "P&P":
        if loader.current_board:
            board = pickplace.process(loader.current_board)
            window["-LOG-"].print(f"[P&P] {board.datamatrix} - {board.placement_result}")
            set_step_state("P&P")
        else:
            window["-LOG-"].print("[ERROR] No board available for P&P")

    elif event == "Oven":
        if loader.current_board:
            board = oven.process(loader.current_board)
            match_status = "MATCH" if board.status == "OVEN_MATCH" else "MISMATCH"
            window["-LOG-"].print(f"[OVEN] {board.datamatrix} reflowed using {board.oven_profile} ({match_status})")
            set_step_state("Oven")
        else:
            window["-LOG-"].print("[ERROR] No board available for oven")

    elif event == "AOI":
        if loader.current_board:
            board = aoi.process(loader.current_board)
            window["-LOG-"].print(f"[AOI] {board.datamatrix} - {board.aoi_result}")
            if board.aoi_result == "FAIL":
                if board not in rework_queue:
                    rework_queue.append(board)
                    window["-LOG-"].print(f"[REPAIR] Sent to Solder City: {board.datamatrix}")
                loader.current_board = None
            else:
                board = stacker.process(loader.current_board)
                window["-LOG-"].print(f"[STACKER] {board.datamatrix} stacked and logged ({board.status})")
                window["-LOG-"].print("-" * 80)
                loader.current_board = None
            set_step_state("AOI")

    elif event == "StartRework":
        if rework_queue:
            if rework_board is None:
                rework_board = rework_queue.pop(0)
                rework_board.rework_count += 1
                window["-LOG-"].print(f"[REWORK] Starting rework attempt {rework_board.rework_count} for {rework_board.datamatrix}")
            else:
                window["-LOG-"].print("[ERROR] A board is already being reworked")
        else:
            window["-LOG-"].print("[REWORK] No failed boards to rework")

    elif event == "SolderCity":
        if rework_board:
            window["-LOG-"].print(f"[SOLDER CITY] {rework_board.datamatrix} sent for repair")
        else:
            window["-LOG-"].print("[ERROR] No active rework board to send to Solder City")

    elif event == "AOIRecheck":
        if rework_board:
            rework_board = aoi.process(rework_board)
            window["-LOG-"].print(f"[AOI-RECHECK] {rework_board.datamatrix} - {rework_board.aoi_result}")
            if rework_board.aoi_result == "PASS":
                rework_board.status = "REWORK_COMPLETED"
                stacker.process(rework_board)
                window["-LOG-"].print(f"[REWORK] {rework_board.datamatrix} passed AOI and sent to stacker")
                window["-LOG-"].print("-" * 80)
                rework_board = None
            elif rework_board.rework_count >= 3:
                rework_board.status = "SCRAP"
                window["-LOG-"].print(f"[SCRAP] {rework_board.datamatrix} scrapped after 3 failed AOI attempts")
                window["-LOG-"].print("-" * 80)
                rework_board = None
            else:
                rework_queue.append(rework_board)
                window["-LOG-"].print(f"[REWORK LOOP] {rework_board.datamatrix} requeued for another repair round")
                rework_board = None
        else:
            window["-LOG-"].print("[ERROR] No board in AOI recheck")

window.close()
