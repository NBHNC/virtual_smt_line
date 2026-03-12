# Virtual SMT Line Simulator

## Purpose
This project simulates a virtual SMT production line with process enforcement, board traceability, inspection results, hold handling, rework routing, and final stacking through a desktop GUI.

## Features

- Sequential SMT flow:
  - Unload -> Paste Printer -> SPI -> Pick & Place -> Reflow Oven -> AOI
- Button-based process enforcement so steps can only run in the correct order
- SPI hold logic:
  - boards that fail SPI are placed on HOLD and do not continue through the line
- AOI failure handling with a rework queue
- Enforced rework sequence:
  - Start Rework -> Solder City -> AOI Recheck
- Rework outcomes:
  - pass = stack
  - fail under 3 attempts = requeue
  - fail on 3rd attempt = scrap
- Automatic stacking for boards that pass AOI
- Live on-screen status display for:
  - rework queue count
  - active rework board
  - SPI hold count
- GUI event log for board-by-board traceability
- CSV log output to `logs/trace.csv`

## Project Structure

```text
virtual_smt_line/
│
├── main.py
├── requirements.txt
├── README.md
├── LICENSE
├── CHANGELOG.md
├── REVISION_HISTORY.md
├── SOW.md
├── barcode_state.json
├── profiles/
│   └── board_profiles.csv
├── logs/
│   └── trace.csv
└── modules/
    ├── __init__.py
    ├── aoi.py
    ├── barcode_generator.py
    ├── board.py
    ├── loader.py
    ├── oven.py
    ├── pickplace.py
    ├── printer.py
    ├── spi.py
    ├── stacker.py
    └── unloader.py
```

## Requirements

- Python 3.10 or newer
- Windows PowerShell or another terminal
- Packages listed in `requirements.txt`

## How to Run

### 1. Open the project folder

Open PowerShell and move into the project directory:

```powershell
cd C:\Users\Collin\Documents\virtual_smt_line
```

### 2. Create a virtual environment (first time only)

```powershell
python -m venv venv
```

### 3. Activate the virtual environment

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

When the environment is active, your prompt should start with `(venv)`.

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Launch the simulator

```powershell
python main.py
```

The Virtual SMT Line Simulator GUI should open.

## Flow Summary

### Main SMT flow
Unload -> Printer -> SPI -> Pick & Place -> Oven -> AOI

### SPI failure behavior
If a board fails SPI:
- it is placed on HOLD
- it does not continue to Pick & Place, Oven, or AOI
- the SPI hold counter increases

### AOI failure behavior
If a board fails AOI:
- it is added to the rework queue
- it can then enter the rework loop

### Rework flow
Start Rework -> Solder City -> AOI Recheck

### Rework outcomes
- PASS -> sent to stacker
- FAIL under 3 attempts -> returned to rework queue
- FAIL on 3rd attempt -> SCRAP

## Current Status

Working now:
- Main SMT flow enforcement
- SPI hold logic
- AOI fail to rework routing
- Enforced rework button sequence
- 3-attempt rework scrap logic
- Live queue/status display
- CSV trace logging

Possible next improvements:
- Dedicated hold review / release workflow
- Board selection from the GUI instead of a fixed board name
- Expanded traceability and reporting
- Export options for logs and summaries

## Notes

- Main entry point: `main.py`
- GUI library used: `FreeSimpleGUI`
- Board profiles are read from `profiles/board_profiles.csv`
- The simulator writes trace records to `logs/trace.csv`
