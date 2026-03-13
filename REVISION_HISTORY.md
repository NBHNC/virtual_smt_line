# Revision History

---

<<<<<<< HEAD
### v1.3 – March 12, 2026

**Status:** Released

**Implemented:**
- Enforced full main SMT process flow:
  - Unload Board
  - Paste Printer
  - SPI Inspection
  - Pick & Place
  - Reflow Oven
  - AOI Inspection
- Enforced rework sequence:
  - Start Rework
  - Solder City
  - AOI Recheck
- Added AOI fail routing to rework queue
- Added rework retry logic:
  - PASS = sent to stacker
  - FAIL under 3 attempts = returned to rework queue
  - FAIL on 3rd attempt = SCRAP
- Added SPI hold logic:
  - boards that fail SPI are stopped before Pick & Place
  - SPI-failed boards do not continue through the rest of the line
- Added live production readouts to the GUI:
  - Total Attempted
  - Rework Queue
  - Active Rework
  - SPI Fail
  - Completed
  - Scrap
  - AOI Fail
  - Line FPY
- Added completed count tracking
- Added scrap count tracking
- Added AOI fail count tracking
- Added total attempted count tracking
- Added line FPY calculation
- Updated line yield logic so SPI failures are included in FPY
- Relabeled HOLD display to SPI Fail for clarity
- Migrated GUI dependency from PySimpleGUI to FreeSimpleGUI
- Updated README with setup and run instructions
- Cleaned project packaging and dependency structure for release

**Notes:**
- Boards that pass AOI on the first trip count toward Line FPY
- Boards that fail SPI count against Line FPY
- Boards that require rework may still complete successfully, but do not count as first-pass good

**Next Possible Enhancements:**
- Add dedicated SPI hold review / release workflow
- Add recipe or product selection from the GUI
- Add resettable counters
- Add exportable production summary / yield report
- Add operator dashboard improvements

---

### v1.2 – June 2025

**Status:** Rework Loop Functional

**Implemented:**
- Added AOI failure handling with rework queue
- Added manual rework flow:
  - Start Rework
  - Solder City
  - AOI Recheck
- Added rework count tracking
- Added scrap condition after repeated AOI recheck failures
- Expanded logging for rework events

**Next Possible Enhancements:**
- Enforce rework button restrictions
- Add visual queue/status indicators
- Add automatic status updates for reworked boards

---

### v1.1 – June 2025

**Status:** Traceability / Flow Improvements Added

**Implemented:**
- Improved board traceability using serialized DataMatrix-style identifiers
- Expanded log readability using board-specific identifiers
- Improved modular board handoff between stations
- Stabilized main SMT button sequencing
- Improved simulator structure for future repair-loop additions

**Next Possible Enhancements:**
- Rework queue and repair routing
- Better status visibility in GUI
- Additional process control logic

---

=======
>>>>>>> bc35b7922419b2af460b54502e19001a285198a8
### v1.0 – May 31, 2025

**Status:** Full SMT Line Simulation Functional

**Implemented:**
- All 7 SMT stations simulated:
  - Unloader
  - Paste Printer
  - SPI Inspection
  - Pick & Place
  - Reflow Oven
  - AOI Inspection
  - Stacker
- Modular structure using separate Python files
- GUI built using PySimpleGUI with manual board advancement
- Reflow oven profile matching logic
- SPI and AOI simulated with pass/fail outcomes
- Board traceability logging to CSV
- Git version control in place
<<<<<<< HEAD

**Next Possible Enhancements:**
- Alarm handling for failed inspections or oven mismatch
- Batch processing of multiple boards
- Summary dashboards or status panels
=======
>>>>>>> bc35b7922419b2af460b54502e19001a285198a8
