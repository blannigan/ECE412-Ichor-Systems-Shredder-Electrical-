# Universal Plastic Shredder V2.0 — Electrical System

**ECE 412 Senior Project Development I/II · Portland State University · Winter–Spring 2026**

Repository owner: **MME / Ichor Systems** ([@blannigan](https://github.com/blannigan)) — transferred from the EE team at the end of term for long-term stewardship.

Industry Sponsor: **MME / Ichor Systems** (Bridget Lannigan)
Faculty Advisors: Prof. Andrew Greenberg, Dr. Jonathan Bird (EE), Robert Paxton (ME)

**Team "I'm so Shredded inc." — original authors, retained as collaborators with write access:**

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
- HMI operator interface (AutomationDirect EA1-T4CL C-more Micro-Graphic touch panel, serial to the PLC)
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
- Stay within the **$1,000 EE-team budget** (the overall $3,000 project budget is split across ME and EE; EE owns $1,000)

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
docs/           Numbered project documents (term1_week04_Project_Proposal → term2_week10_Final_Report)
BOM/            Bill of materials and component selection spreadsheets
CAD/            Mechanical CAD zip archive and Inventor part files (Part1–Part10)
electrical/     Circuit logic diagrams and deadman circuit documentation
PLC/            Shredder ladder logic program and point list (.xlsx / .pdf)
HMI/            HMI project file (MagicPanel .mgp)
```

---

## Final Report

The EE final report lives in `docs/term2_week10_Final_Report/`:

- **`docs/term2_week10_Final_Report/Final_Report.pdf`** — the built report (PSU MCECS style).
- **`docs/term2_week10_Final_Report/src/Final_Report.tex`** — LaTeX source.
- **[`docs/term2_week10_Final_Report/Report_Setup.md`](docs/term2_week10_Final_Report/Report_Setup.md)** — **how to build, edit, and
  regenerate the report** (toolchain, packages, compile steps, and how to
  rebuild the point-list appendix from `PLC/Point_List.xlsx`). Start here if you
  want to work on the report.
- `docs/term2_week10_Final_Report/src/appendix_pointlist.tex` / `docs/term2_week10_Final_Report/src/gen_pointlist.py` — the auto-generated
  point-list appendix and its generator.

---

## System Architecture

**Hardware subsystems:**
- AC power input → main disconnect (PowerTec 71008) → branch fuses / breakers
- 24 VDC supply (Mean Well NDR-480-24) for control wiring
- Mitsubishi SD-N35 motor contactor (E-stop hardwired in series with the coil)
- VFD (Huanyang HY02D211B-T), motor speed and direction driven by a 0–10 V analog command from the PLC and a hardwired RUN_FWD / RUN_REV / RESET trio
- 3–5 HP motor + gearbox (ME interface)
- AutomationDirect EA1-T4CL C-more Micro-Graphic HMI (operator interface)
- Safety circuit: two-hand start (deadman) buttons, E-stop, motor contactor, capacitive-touch safety input (wired to PLC X7)

**PLC (DirectLOGIC 205 rack with H2-DM1E CPU):**
The PLC is the system controller. All run-permit logic, jam recovery, the
3-strike lockout, and the HMI screen-change behavior live in the ladder
program (see Section 6 of the Final Report and `PLC/Point_List.pdf` for the
full I/O map). Modules in the rack:

| Slot | Module       | Role |
|------|--------------|------|
| 0    | H2-DM1E      | CPU + Ethernet |
| 1    | D2-08ND3     | 8-point DC discrete input (pushbuttons, E-stop monitor, VFD fault, cap touch) |
| 2    | F2-08AD-1    | 8-channel analog current input (VFD motor current monitor) |
| 3    | F2-04RTD     | 4-channel RTD input (motor temperature, future) |
| 4    | D2-08TR      | 8-point relay output (VFD RUN_FWD / RUN_REV / RESET, panel LEDs) |
| 5    | F2-08DA-2    | 8-channel analog voltage output (0–10 V speed reference to VFD VI) |

Program file: `PLC/src/Shredder_Ladder_Logic_v1.dmd`
Industrial standard: the entire control program and the operator interface
are built on AutomationDirect DirectLOGIC / Do-more / C-more hardware
rather than a hobby-grade microcontroller stack. ESP32 / Arduino were
considered for the HMI early on and rejected: the sponsor build needs an
industrial-rated touch panel and a PLC-based control program for
maintainability, safety review, and alignment with NFPA 79 / NEMA practice.

**HMI (EA1-T4CL C-more Micro-Graphic, `HMI/HMI_413.mgp`):**
Four screens, 27 PLC tags. The HMI is a display + button panel only; all
logic runs in the PLC ladder program. Screens:

  1. MOTOR CONTROL  — forward / reverse / stop, speed adjust (V2000)
  2. MOTOR TELEMETRY — frequency, current, voltage, RPM read-back
  3. ERROR (red backlight) — jam, capacitive trip, and E-stop indicators
  4. TEST — engineering / commissioning screen (soft deadman, soft jam)

**Operator workflow:**
1. Power on → safety check
2. Press two-hand start buttons simultaneously to run motor
3. Hand-feed plastic sheets into shredder
4. Normal stop via Stop button, or E-stop if needed
5. Collect shredded output (~1-inch pieces)

---

## Prior Work

A 2023–2024 PSU capstone team built a working 2 HP plastic shredder for the EPL that shredded household plastics with basic VFD, two-hand start, and E-stop. This project scales to industrial-grade plastics and adds motor current monitoring, automatic jam-clearing (auto forward/reverse), thermal shutdown, improved safety interlocks, a proper contactor, and a full HMI.
