import PySimpleGUI as sg
from modules.loader import Loader
from modules.printer import Printer
from modules.spi import SPI

loader = Loader()
printer = Printer()
spi = SPI()

layout = [
    [sg.Text("Virtual SMT Line Simulator", font=("Arial", 16))],
    [sg.Button("Inject Board"), sg.Button("Process Printer"), sg.Button("Process SPI"), sg.Button("Exit")],
    [sg.Multiline(size=(80, 20), key="-LOG-", autoscroll=True)],
]

window = sg.Window("SMT Line Simulator", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    elif event == "Inject Board":
        board = loader.load_board()
        window["-LOG-"].print(f"[LOADER] Injected board {board.barcode}")
    elif event == "Process Printer":
        if loader.current_board:
            board = printer.process(loader.current_board)
            window["-LOG-"].print(f"[PRINTER] Processed board {board.barcode}")
        else:
            window["-LOG-"].print("[ERROR] No board in loader")
    elif event == "Process SPI":
        if loader.current_board:
            board = spi.process(loader.current_board)
            window["-LOG-"].print(f"[SPI] {board.barcode} - {board.spi_result}")
        else:
            window["-LOG-"].print("[ERROR] No board in loader to inspect at SPI")

window.close()
