# Virtual SMT Line Simulator

## Purpose
This project simulates a full SMT production line virtually. It allows simulation of barcode scanning, profile validation, and board movement through virtual modules such as printer, SPI, Pick Place, oven, AIO.

## Features
- Modular architecture (printer, SPI, Pick Place, oven, AIO)
- GUI using PySimpleGUI
- Traceability via board barcode and required profile
- Logs and exports data for each board

## Setup

### 1. Clone or Extract
Ensure all files and folders are placed in a single directory.

### 2. Setup Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run
```bash
python main.py
```

## Roadmap
- [x] Printer Simulation
- [ ] SPI, Pick Place, AOI
- [ ] Profile validation logic for Oven
- [ ] Defect generation and rework
- [ ] Exportable process log

## Requirements
- Python 3.10+
- pandas
- PySimpleGUI

## License
MIT (or proprietary if internal)