# Universal Plastic Shredder V2.0 — Electrical System

**ECE 412 Senior Project Development I/II · Portland State University · Winter–Spring 2026**

Industry Sponsor: **MME / Ichor Systems** (Bridget Lannigan)
Faculty Advisors: Prof. Andrew Greenberg, Dr. Jonathan Bird (EE), Robert Paxton (ME)

**Team "I'm so Shredded inc.":**

| Name | Email |
|---|---|
| Bao Nguyen | baon@pdx.edu |
| Fearghus Tyler | fearghus@pdx.edu |
| Yaqoub Rabiah | yrabiah@pdx.edu |
| Fox Kang | foxkang@pdx.edu |

---

## Project Overview

Ichor Systems generates significant plastic waste (PVC, polypropylene, LDPE) during semiconductor equipment manufacturing. Existing commercial shredders are either too expensive or underpowered for their thick-material needs (0.25–0.5" rigid sheets). This project designs and builds the **electrical control and power system** for a new industrial-grade plastic shredder — Universal Plastic Shredder V2.0.

The mechanical structure and cutting blades are handled by a separate ME team. The EE team is responsible for:

- VFD-based motor control (3–5 HP, target 70–90 RPM output shaft speed)
- HMI operator interface (ESP32 with display, RS485/MODBUS to VFD)
- Safety systems: two-hand start, emergency stop, lid interlock, overload/overcurrent protection
- PLC ladder logic for control sequencing (DirectLogic 205 / Direct Automation)
- Status indicator lights (Power, Running, Fault)
- Electrical protection: fuses, breakers, motor contactor, thermal shutdown

Design follows **NFPA 70 (NEC)** guidance and **NEMA enclosure** practices. Total project budget is $3,000 (EE portion ~$1,000).

---

## Requirements Summary

**Must:**
- Shred plastic into ~1-inch pieces when integrated with ME system
- Use a controllable VFD; support 3–5 HP motor at 70–90 RPM
- Follow NFPA-70 (NEC) electrical design guidance
- Include emergency stop, overcurrent/overload protection, and at least one safety interlock
- Include an HMI for operator control and status display
- Stay within $3,000 total project budget

**Should:**
- Include clear status and fault indicator lights
- Follow NEMA enclosure guidelines
- Have clearly labeled controls

**May (if time/budget allow):**
- Wireless monitoring (read-only)
- Data logging
- Additional safety sensing (capacitive touch, thermal)

---

## Repository Structure

```
docs/           Project proposal, team contract, HMI options matrix, and the final report
BOM/            Bill of materials and component selection spreadsheets
CAD/            Mechanical CAD zip archive and Inventor part files (Part1–Part10)
electrical/     Circuit logic diagrams and deadman circuit documentation
PLC/            Shredder ladder logic program and point list (.xlsx / .pdf)
HMI/            HMI project file (MagicPanel .mgp)
```

---

## Final Report

The EE final report lives in `docs/`:

- **`docs/Final_Report_Rough_Draft.pdf`** — the built report (PSU MCECS style).
- **`docs/Final_Report_Rough_Draft.tex`** — LaTeX source.
- **[`docs/REPORT_SETUP.md`](docs/REPORT_SETUP.md)** — **how to build, edit, and
  regenerate the report** (toolchain, packages, compile steps, and how to
  rebuild the point-list appendix from `PLC/Point List.xlsx`). Start here if you
  want to work on the report.
- `docs/appendix_pointlist.tex` / `docs/gen_pointlist.py` — the auto-generated
  point-list appendix and its generator.

---

## System Architecture

**Hardware subsystems:**
- AC power input → disconnect → fuses/breakers
- VFD (motor speed and direction control via MODBUS/RS485)
- 3–5 HP motor + gearbox (ME interface)
- ESP32 HMI display (operator interface)
- Safety circuit: two-hand start buttons, E-stop, lid interlock, motor contactor

**PLC (DirectLogic 205 rack — Direct Automation):**
- Ladder logic controls motor run/stop sequencing and safety interlocks
- Program file: `PLC/Shredder_Ladder_logic_v1.dmd`

**Software (Arduino/C++ on ESP32):**
- HMI: displays Ready / Running / Fault state, motor speed, fault messages
- Safety input handling: continuously monitors E-stop, interlocks, two-hand start
- Control logic: manages system states (Idle → Ready → Running → Fault)
- VFD interface: sends run/stop/speed commands, reads fault signals via MODBUS

**Operator workflow:**
1. Power on → safety check
2. Press two-hand start buttons simultaneously to run motor
3. Hand-feed plastic sheets into shredder
4. Normal stop via Stop button, or E-stop if needed
5. Collect shredded output (~1-inch pieces)

---

## Prior Work

A 2023–2024 PSU capstone team built a working 2 HP plastic shredder for the EPL that shredded household plastics with basic VFD, two-hand start, and E-stop. This project scales to industrial-grade plastics and adds motor current monitoring, automatic jam-clearing (auto forward/reverse), thermal shutdown, improved safety interlocks, a proper contactor, and a full HMI.
