# Scope of Work (SOW) – Virtual SMT Line Simulator

## Project Title
Virtual SMT Line Simulator

## Purpose
Develop a modular, GUI-based software tool to simulate the process flow of a surface-mount technology (SMT) production line.

## Objective
- Validate barcode-to-profile matching logic
- Train users on SMT process flow virtually
- Simulate basic error conditions (wrong profile, failed SPI, etc.)

## Deliverables
- GUI for operating each SMT station module
- Simulated barcode and board profile table
- Board traceability and logging
- Configurable board input and flow rates

## Timeline
- Phase 1: Loader and Printer (Weekend)
- Phase 2: Add SPI, AOI, Oven modules (Next iteration)
- Phase 3: Logging, config system, failure simulation

## Out-of-Scope
- Real-time physical equipment interaction
- Full SCADA or PLC integration

## Risks
- Overengineering for a simulation
- Performance limitations of Python GUI for complex UIs

## Stakeholders
- Developer: Collin
- Reviewer: Self
- Audience: Engineering, ATQ (potentially)