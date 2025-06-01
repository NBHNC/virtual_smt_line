# Virtual SMT Line Simulator

## Purpose
This project simulates a full SMT production line virtually. It allows simulation of barcode scanning, profile validation, and board movement through virtual modules such as printer, SPI, Pick Place, oven, AOI.

## Features

- Simulates sequential flow through an SMT line:
  - Unloader → Paste Printer → SPI → Pick & Place → Reflow Oven → AOI
- Enforces step-by-step process with GUI button enabling/disabling
- AOI failure handling with rework queue
- Manual rework loop:
  - Start Rework → Solder City → AOI Recheck
  - 3 attempts before SCRAP
- Automatic stacking for passed boards
- GUI built with PySimpleGUI
- Full traceability via serialized DataMatrix codes
- Logs all events to GUI console


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

- [x] Printer, SPI, Pick & Place, AOI module integration
- [x] Profile validation logic for Reflow Oven
- [x] Defect generation via AOI with fail routing
- [x] Rework queue with 3-strike SCRAP logic
- [x] GUI process control via enabled/disabled buttons
- [ ] Rework loop enforcement (Start Rework → Solder City → AOI Recheck)
- [ ] Exportable process log (CSV/JSON)


## Requirements
- Python 3.10+
- pandas
- PySimpleGUI

---------------------------------------------
## Current Status

All mainline functionality is working correctly:
- Step-by-step flow is enforced through button states.
- Boards that pass AOI go to the stacker automatically.
- Boards that fail AOI are routed to rework.

Outstanding:
- Rework loop steps (Start Rework → Solder City → AOI Recheck) are **not yet enforced** through button enable/disable logic.


## License
MIT (or proprietary if internal)
