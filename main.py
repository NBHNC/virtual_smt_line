import PySimpleGUI as sg
from modules.loader import Loader
from modules.printer import Printer

loader = Loader()
printer = Printer()

layout = [
    [sg.Text("Virtual SMT Line Simulator", font=("Arial", 16))],
    [sg.Button("Inject Board"), sg.Button("Process Printer"), sg.Button("Exit")],
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
            loader.current_board = None
        else:
            window["-LOG-"].print("[ERROR] No board in loader")

window.close()