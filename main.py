import FreeSimpleGUI as sg
from modules.loader import Loader
from modules.printer import Printer
from modules.spi import SPI
from modules.pickplace import PickPlace
from modules.oven import Oven
from modules.aoi import AOI
from modules.stacker import Stacker

# ---------------------------
# Module instances / state
# ---------------------------
loader = Loader()
printer = Printer()
spi = SPI()
pickplace = PickPlace()
oven = Oven()
aoi = AOI()
stacker = Stacker()

rework_queue = []
hold_queue = []
rework_board = None
rework_stage = None  # None, "repair", "recheck"

completed_count = 0
scrap_count = 0
aoi_fail_count = 0
total_loaded_count = 0
first_pass_good_count = 0

MAIN_KEYS = ["Unload", "Printer", "SPI", "P&P", "Oven", "AOI"]

# ---------------------------
# GUI layout
# ---------------------------
layout = [
    [sg.Text("Virtual SMT Line Simulator", font=("Arial", 16))],

    [
        sg.Button("Unload Board", key="Unload", disabled=False),
        sg.Button("Paste Printer", key="Printer", disabled=True),
        sg.Button("SPI Inspection", key="SPI", disabled=True),
        sg.Button("Pick & Place", key="P&P", disabled=True),
        sg.Button("Reflow Oven", key="Oven", disabled=True),
        sg.Button("AOI Inspection", key="AOI", disabled=True),
        sg.Button("Start Rework", key="StartRework", disabled=True),
        sg.Button("Solder City", key="SolderCity", disabled=True),
        sg.Button("AOI Recheck", key="AOIRecheck", disabled=True),
        sg.Button("Exit"),
    ],

    [
    sg.Text("Rework Queue:", font=("Arial", 10, "bold")),
    sg.Text("0", key="-REWORK-QUEUE-", size=(5, 1)),

    sg.Text("Active Rework:", font=("Arial", 10, "bold")),
    sg.Text("None", key="-ACTIVE-REWORK-", size=(35, 1)),

    sg.Text("SPI Fail:", font=("Arial", 10, "bold")),
    sg.Text("0", key="-HOLD-COUNT-", size=(5, 1)),

    sg.Text("Completed:", font=("Arial", 10, "bold")),
    sg.Text("0", key="-COMPLETED-COUNT-", size=(5, 1)),

    sg.Text("Scrap:", font=("Arial", 10, "bold")),
    sg.Text("0", key="-SCRAP-COUNT-", size=(5, 1)),

    sg.Text("AOI Fail:", font=("Arial", 10, "bold")),
    sg.Text("0", key="-AOI-FAIL-COUNT-", size=(5, 1)),

    sg.Text("Line FPY:", font=("Arial", 10, "bold")),
    sg.Text("0.0%", key="-FPY-", size=(8, 1)),
],

    [sg.Multiline(size=(120, 24), key="-LOG-", autoscroll=True, write_only=True)],
]

window = sg.Window("SMT Line Simulator", layout, finalize=True)

# ---------------------------
# Helper functions
# ---------------------------
def log(message):
    window["-LOG-"].print(message)


def update_status_display():
    if total_loaded_count > 0:
        fpy = (first_pass_good_count / total_loaded_count) * 100
    else:
        fpy = 0.0

    window["-REWORK-QUEUE-"].update(str(len(rework_queue)))
    window["-HOLD-COUNT-"].update(str(len(hold_queue)))
    window["-COMPLETED-COUNT-"].update(str(completed_count))
    window["-SCRAP-COUNT-"].update(str(scrap_count))
    window["-AOI-FAIL-COUNT-"].update(str(aoi_fail_count))
    window["-FPY-"].update(f"{fpy:.1f}%")

    if rework_board is None:
        window["-ACTIVE-REWORK-"].update("None")
    else:
        window["-ACTIVE-REWORK-"].update(rework_board.datamatrix)


def set_main_step(next_step):
    for key in MAIN_KEYS:
        window[key].update(disabled=True)

    if next_step in MAIN_KEYS:
        window[next_step].update(disabled=False)


def refresh_rework_buttons():
    has_waiting_rework = len(rework_queue) > 0
    active_rework = rework_board is not None

    window["StartRework"].update(disabled=not (has_waiting_rework and not active_rework))
    window["SolderCity"].update(disabled=(rework_stage != "repair"))
    window["AOIRecheck"].update(disabled=(rework_stage != "recheck"))

    update_status_display()


def finish_board_cycle():
    set_main_step("Unload")
    refresh_rework_buttons()


# ---------------------------
# Initial button state
# ---------------------------
set_main_step("Unload")
refresh_rework_buttons()

# ---------------------------
# Event loop
# ---------------------------
while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, "Exit"):
        break

    # -----------------------
    # MAIN SMT FLOW
    # -----------------------
    elif event == "Unload":
        board = loader.load_board("SG201_S1")
        loader.current_board = board
        total_loaded_count += 1
        log(f"[UNLOADER] {board.datamatrix}")
        set_main_step("Printer")
        refresh_rework_buttons()

    elif event == "Printer":
        if loader.current_board is not None:
            board = printer.process(loader.current_board)
            loader.current_board = board
            log(f"[PRINTER] Printed board {board.datamatrix}")
            set_main_step("SPI")
            refresh_rework_buttons()

    elif event == "SPI":
        if loader.current_board is not None:
            board = spi.process(loader.current_board)
            loader.current_board = board
            log(f"[SPI] {board.pcb_name} REV:{board.revision} ({board.datamatrix}) - {board.spi_result}")

            if board.spi_result == "FAIL":
                board.status = "HOLD_SPI"
                board.spi_hold_released = False
                hold_queue.append(board)
                log(f"[HOLD] {board.datamatrix} failed SPI and was placed on HOLD")
                log("-" * 80)
                loader.current_board = None
                finish_board_cycle()
            else:
                set_main_step("P&P")
                refresh_rework_buttons()

    elif event == "P&P":
        if loader.current_board is not None:
            board = pickplace.process(loader.current_board)
            loader.current_board = board
            log(f"[P&P] {board.datamatrix} - {board.placement_result}")
            set_main_step("Oven")
            refresh_rework_buttons()

    elif event == "Oven":
        if loader.current_board is not None:
            board = oven.process(loader.current_board)
            loader.current_board = board
            match_status = "MATCH" if board.status == "OVEN_MATCH" else "MISMATCH"
            log(f"[OVEN] {board.datamatrix} reflowed using {board.oven_profile} ({match_status})")
            set_main_step("AOI")
            refresh_rework_buttons()

    elif event == "AOI":
        if loader.current_board is not None:
            board = aoi.process(loader.current_board)
            loader.current_board = board
            log(f"[AOI] {board.datamatrix} - {board.aoi_result}")

            if board.aoi_result == "FAIL":
                aoi_fail_count += 1
                if board not in rework_queue:
                    rework_queue.append(board)
                    log(f"[REWORK QUEUE] Added failed board: {board.datamatrix}")
            else:
                stacked_board = stacker.process(board)
                completed_count += 1
                first_pass_good_count += 1
                log(f"[STACKER] {stacked_board.datamatrix} stacked and logged ({stacked_board.status})")
                log("-" * 80)

            loader.current_board = None
            finish_board_cycle()

    # -----------------------
    # REWORK FLOW
    # Start Rework -> Solder City -> AOI Recheck
    # -----------------------
    elif event == "StartRework":
        if rework_board is None and rework_queue:
            rework_board = rework_queue.pop(0)

            if getattr(rework_board, "status", "") == "SCRAP":
                log(f"[REWORK] Cannot rework {rework_board.datamatrix} - board already scrapped")
                rework_board = None
                rework_stage = None
            else:
                rework_board.rework_count += 1
                rework_stage = "repair"
                log(f"[REWORK] Starting attempt {rework_board.rework_count} for {rework_board.datamatrix}")

        refresh_rework_buttons()

    elif event == "SolderCity":
        if rework_board is not None and rework_stage == "repair":
            log(f"[SOLDER CITY] {rework_board.datamatrix} sent for repair")
            rework_stage = "recheck"
        else:
            log("[ERROR] No active board ready for Solder City")

        refresh_rework_buttons()

    elif event == "AOIRecheck":
        if rework_board is not None and rework_stage == "recheck":
            rework_board = aoi.process(rework_board)
            log(f"[AOI-RECHECK] {rework_board.datamatrix} - {rework_board.aoi_result}")

            if rework_board.aoi_result == "PASS":
                rework_board.status = "REWORK_COMPLETED"
                stacked_board = stacker.process(rework_board)
                completed_count += 1
                log(f"[REWORK PASS] {stacked_board.datamatrix} passed AOI recheck and was stacked")
                log("-" * 80)
                rework_board = None
                rework_stage = None

            elif rework_board.rework_count >= 3:
                rework_board.status = "SCRAP"
                scrap_count += 1
                log(f"[SCRAP] {rework_board.datamatrix} scrapped after 3 failed AOI attempts")
                log("-" * 80)
                rework_board = None
                rework_stage = None

            else:
                rework_queue.append(rework_board)
                log(f"[REWORK LOOP] {rework_board.datamatrix} failed recheck and was returned to queue")
                rework_board = None
                rework_stage = None
        else:
            log("[ERROR] No active board ready for AOI recheck")

        refresh_rework_buttons()

window.close()