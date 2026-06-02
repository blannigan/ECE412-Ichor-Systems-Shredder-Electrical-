# Universal Plastic Shredder V2.0 — Weekly Progress Reports

**Course:** ECE 412/413 (Spring 2026) · **Sponsor:** MME / Ichor Systems
**Team:** Bao Nguyen, Fearghus Tyler, Yaqoub Rabiah, Fox Kang

---

## 🔑 Key hardware referenced

| System | Part | Role / interface |
|---|---|---|
| **VFD** | Huanyang **HY02D211B-T** | Motor drive. Speed ref on **VI** (0–10 V, `PD002=1`), current monitor on **VO** (`PD054=1`), fault relay **FA/FC** (`PD052=02`), run inputs **FOR/REV/RST** (sinking to DCM). |
| **Motor** | GE **5KE182BC205B** (bench) / **PE145TC-2-4** (production cand.) | 3-phase, FLA ≈ 7.6 A. Phases **U/V/W → T1/T2/T3** via 4 mm banana sockets. |
| **PLC** | DirectLOGIC 205, **H2-DM1E** CPU | DI **X0–X7** (`D2-08ND3`), relay out **Y0–Y7** (`D2-08TR`), current-in **F2-08AD-1**, 0–10 V out **F2-08DA-2**. |
| **HMI** | C-More **EA1-T4CL** | 4" touch panel, serial link to CPU. |
| **Contactor** | Mitsubishi **SD-N35** | In the hardwired E-stop chain (coil **A1/A2**); switches the VFD feed. |
| **E-stop** | Eaton **E22B1** (NC) | Drops the contactor coil; state monitored on PLC **X4**. |
| **Braking resistor** | ATO **APCS-300R30-AD** | 300 W / 30 Ω on VFD **P+/PR**. |

## 🗂️ Report index

**Winter term**

| Date | Focus |
|---|---|
| 2025-12-17 | Kickoff coordination meeting; component research begins |
| 2026-01-03 | Compare motors / HMIs / safety sensors |
| 2026-01-09 | Sponsor + advisor goal/budget review |
| 2026-01-16 | Motor-control & safety strategy; first motor+VFD bench test |
| 2026-01-23 | Electrical design starts; BOM for initial purchases; AutoCAD setup |
| 2026-02-02 | Prototype build; safety-sensor circuit |
| 2026-02-06 | Schematic + ME coordination |
| 2026-02-13 | Advisor coordination meeting |
| 2026-02-27 | Documentation & presentation prep; BOM revision |
| 2026-03-06 | Parts arrived — fit & wire the prototype |
| 2026-03-13 | VFD/motor bring-up; HMI GUI |
| 2026-03-16 | Finalize documentation before spring break |

**Spring term**

| Wk | Date | Focus |
|---|---|---|
| 1 | 2026-04-03 | Post-break reset; points list; E-stop → contactor |
| 2 | 2026-04-10 | PLC ↔ circuit integration; cap-touch (small scale) |
| 3 | 2026-04-17 | Relay-module fix; analog modules; HMI scaling |
| 4 | 2026-04-24 | Current → voltage (0–10 V) control swap; VFD reprogram |
| 5 | 2026-05-01 | Presentation; cap-touch prototype; braking resistor sizing |
| 6 | 2026-05-08 | Midterm week (light); documentation |
| 7 | 2026-05-15 | Enclosure panel build; overcurrent-signal logic |
| 8 | 2026-05-22 | Panel wiring; ME parts hand-off |
| 9 | 2026-05-30 | Documentation push (report, manual, schematics) |
| 10 | 2026-06-06 | Final report & capstone demo |

---

# Winter Term (Dec 2025 – Mar 2026)

## Report date: 2025-12-17

### ✅ Last week  ·  _hours in parentheses_

**Team Review**
- The electrical and mechanical teams held the first coordination meeting for the shredder project.
- We discussed the overall system design, safety systems, and motor-control ideas.
- The team also set up communication tools and began researching components.

**Bao Nguyen**
- Created Discord server for team communication. (1)
- Attended coordination meeting with ME team. (1)
- Began researching HMI display options. (3)

**Fearghus Tyler**
- Discussed motor requirements with mechanical team. (2)
- Attended coordination meeting with ME team. (1)
- Researched possible motor options. (2)

**Yaqoub Rabiah**
- Started researching VFD motor-control systems. (3)
- Attended coordination meeting with ME team. (1)

**Fox Kang**
- Started researching safety sensors and safety concepts. (3)
- Attended coordination meeting with ME team. (1)

### 🎯 Next week

**Team Plan**
- Continue researching components and begin building comparison tables for motors, sensors, and control systems.

**Bao Nguyen**
- Research HMI options and telemetry display ideas. (3)

**Fearghus Tyler**
- Begin creating preliminary electrical BOM. (3)

**Yaqoub Rabiah**
- Research VFD telemetry and monitoring features. (3)

**Fox Kang**
- Continue researching safety detection methods. (3)

### 🚧 Blocked

**Bao Nguyen**
- Waiting for motor requirements from mechanical team.

**Fearghus Tyler**
- Waiting for gearbox specifications.

**Yaqoub Rabiah**
- Waiting for VFD model.

**Fox Kang**
- None.

---

## Report date: 2026-01-03

### ✅ Last week  ·  _hours in parentheses_

**Team Review**
- The team continued researching electrical components for the shredder system.
- Motors, HMIs, and safety sensors were compared.
- Early ideas for the electrical control system were discussed.

**Bao Nguyen**
- Researched HMI display options. (3)
- Reviewed possible telemetry information to display. (2)

**Fearghus Tyler**
- Began building the electrical BOM for the initial test setup — motor, VFD, contactor, PLC rack + modules, HMI, breaker, power switch, and 12/10 AWG wire. (3)

**Yaqoub Rabiah**
- Compared VFD options and specifications. (3)

**Fox Kang**
- Continued safety-sensor research. (3)

### 🎯 Next week

**Team Plan**
- Narrow down hardware options and begin planning electrical architecture.

**Bao Nguyen**
- Work on system block diagram. (3)

**Fearghus Tyler**
- Expand electrical BOM. (3)

**Yaqoub Rabiah**
- Research PLC integration with VFD. (3)

**Fox Kang**
- Continue researching safety interlocks. (3)

### 🚧 Blocked

**Bao Nguyen**
- Waiting for enclosure dimensions.

**Fearghus Tyler**
- Waiting for torque specifications.

**Yaqoub Rabiah**
- Waiting for PLC to arrive.

**Fox Kang**
- Stuck on figuring out the type of technology for the safety sensor.

---

## Report date: 2026-01-09

### ✅ Last week  ·  _hours in parentheses_

**Team Review**
- The team met with the faculty advisor and industry sponsor to review project goals.
- Budget, motor power, and safety requirements were discussed.

**Bao Nguyen**
- Attended sponsor meeting. (1)
- Researched HMI communication options. (3)

**Fearghus Tyler**
- Continued the electrical BOM — added the Huanyang HY02D211B-T VFD, contactor, push buttons, PLC rack + modules, C-More EA1-T4CL HMI, circuit breaker, power switch, and 12/10 AWG wire. (3)
- Attended sponsor meeting. (1)

**Yaqoub Rabiah**
- Researched VFD control and monitoring options. (4)

**Fox Kang**
- Continued researching safety sensors. (3)

### 🎯 Next week

**Team Plan**
- Start developing electrical system architecture.

**Bao Nguyen**
- Work on system layout diagram. (3)

**Fearghus Tyler**
- Continue updating BOM. (3)

**Yaqoub Rabiah**
- Compare VFD options. (3)

**Fox Kang**
- Research safety-sensor placement. (3)

### 🚧 Blocked

**Bao Nguyen**
- Waiting for motor specs.

**Fearghus Tyler**
- Waiting for gearbox decision.

**Yaqoub Rabiah**
- Waiting on PLC.

**Fox Kang**
- Waiting on HMI.

---

## Report date: 2026-01-16

### ✅ Last week  ·  _hours in parentheses_

**Team Review**
- The electrical team reviewed motor-control strategies and safety systems.
- Design ideas for the electrical system were discussed.

**Bao Nguyen**
- Tested small motor and VFD setup. (4)

**Fearghus Tyler**
- Worked with mechanical team on gearbox ideas. (3)

**Yaqoub Rabiah**
- Reviewed VFD specifications. (3)

**Fox Kang**
- Created accident-scenario safety flow chart. (3)

### 🎯 Next week

**Team Plan**
- Continue developing electrical control-system design.

**Bao Nguyen**
- Work on electrical control-circuit layout. (3)

**Fearghus Tyler**
- Update electrical BOM. (3)

**Yaqoub Rabiah**
- Continue VFD research. (3)

**Fox Kang**
- Continue safety-system research. (3)

### 🚧 Blocked

**Bao Nguyen**
- Waiting for gearbox decision.

**Fearghus Tyler**
- Waiting for enclosure size.

**Yaqoub Rabiah**
- Waiting on equipment to program PLC.

**Fox Kang**
- Choosing the correct parts for the safety sensors.

---

## Report date: 2026-01-23

### ✅ Last week  ·  _hours in parentheses_

**Team Review**
- The team began developing the electrical design and continued coordination with the mechanical team.

**Bao Nguyen**
- Worked on electrical system design. (3)

**Fearghus Tyler**
- Updated the electrical BOM for the first round of purchases (VFD, contactor, PLC rack/modules, HMI). (3)
- Set up the AutoCAD schematic drawings per these specs — learning the workflow: creating reusable component blocks, transferring blocks between drawings, and setting up the sheet / title-block templates.

**Yaqoub Rabiah**
- Began PLC control-logic planning. (3)

**Fox Kang**
- Continued safety-system research. (3)

### 🎯 Next week

**Team Plan**
- Start building prototype circuits and system diagrams.

**Bao Nguyen**
- Design electrical circuit diagram. (3)

**Fearghus Tyler**
- Continue component sourcing. (3)

**Yaqoub Rabiah**
- Develop PLC logic structure. (3)

**Fox Kang**
- Develop safety-system concept. (3)

### 🚧 Blocked

**Bao Nguyen**
- Waiting for motor specs.

**Fearghus Tyler**
- None.

**Yaqoub Rabiah**
- None.

**Fox Kang**
- None.

---

## Report date: 2026-02-02

### ✅ Last week  ·  _hours in parentheses_

**Team Review**
- The team worked on prototype development and safety-system concepts.

**Bao Nguyen**
- Began building electrical test rig. (4)

**Fearghus Tyler**
- Worked on the electrical schematic in AutoCAD — built out component blocks and the power-distribution sheet. (3)

**Yaqoub Rabiah**
- Developed PLC control logic. (3)

**Fox Kang**
- Requested capacitive-sensor samples. (2)

### 🎯 Next week

**Team Plan**
- Continue prototype testing and system development.

**Bao Nguyen**
- Continue test-rig development. (3)

**Fearghus Tyler**
- Improve schematic design. (3)

**Yaqoub Rabiah**
- Continue PLC programming. (3)

**Fox Kang**
- Develop safety-sensor circuit. (3)

### 🚧 Blocked

**Bao Nguyen**
- Waiting for some parts to arrive.

**Fearghus Tyler**
- None.

**Yaqoub Rabiah**
- None.

**Fox Kang**
- Waiting for sensor samples.

---

## Report date: 2026-02-06

### ✅ Last week  ·  _hours in parentheses_

**Team Review**
- Continued electrical design work and coordination with the mechanical team.

**Bao Nguyen**
- Worked on wiring prototype components. (3)

**Fearghus Tyler**
- Updated the AutoCAD schematic diagrams (block edits and layer cleanup). (3)

**Yaqoub Rabiah**
- Continued PLC logic work. (3)

**Fox Kang**
- Worked on safety-system design. (3)

### 🎯 Next week

**Team Plan**
- Continue system testing and design improvements.

**Bao Nguyen**
- Continue prototype wiring. (3)

**Fearghus Tyler**
- Review schematic design. (3)

**Yaqoub Rabiah**
- Continue PLC programming. (3)

**Fox Kang**
- Continue safety-system research. (3)

### 🚧 Blocked
- None.

---

## Report date: 2026-02-13

### ✅ Last week  ·  _hours in parentheses_

**Team Review**
- The team met with the advisor to discuss project coordination and integration with the mechanical design.

**Bao Nguyen**
- Attended advisor meeting. (1)
- Worked on electrical layout planning. (2)

**Fearghus Tyler**
- Continued the AutoCAD schematic design — refining component blocks and wiring out the control sheet. (3)
- Attended advisor meeting. (1)

**Yaqoub Rabiah**
- Worked on PLC logic improvements. (3)
- Attended advisor meeting. (1)

**Fox Kang**
- Updated safety documentation. (3)
- Attended advisor meeting. (1)

### 🎯 Next week

**Team Plan**
- Continue electrical design and documentation work.

**Bao Nguyen**
- Continue planning the panel/electrical layout — place the VFD, contactor, 24 V PSU, and branch breakers, and rough out control-wire routing for the cabinet.

**Fearghus Tyler**
- Continue the wiring schematics; finalize the power-distribution and control sheets once the updated enclosure CAD arrives from the ME team.

**Yaqoub Rabiah**
- Continue refining the PLC ladder logic — deadman permissive, start/stop, and I/O mapping against the points list.

**Fox Kang**
- Continue the safety-system documentation and evaluate capacitive-sensor options for the operator-presence interlock.

### 🚧 Blocked

**Bao Nguyen**
- Panel/electrical layout depends on the ME enclosure dimensions, still pending.

**Fearghus Tyler**
- Waiting for updated CAD from ME team.

**Yaqoub Rabiah**
- PLC I/O scaling depends on the final analog-module / VFD decision, still pending.

**Fox Kang**
- Still selecting the capacitive-sensor technology before ordering parts.

---

## Report date: 2026-02-27

### ✅ Last week  ·  _hours in parentheses_

**Team Review**
- The team focused on preparing documentation and presentation materials.

**Bao Nguyen**
- Updated electrical design diagrams. (3)

**Fearghus Tyler**
- Reviewed component selections and revised the BOM — switched the production-motor candidate to a PE145TC-2-4 (2 HP, 145TC, 1800 RPM, 3-phase TEFC) and added the NBE7 circuit breaker. (3)

**Yaqoub Rabiah**
- Reviewed PLC logic. (3)

**Fox Kang**
- Updated safety documentation. (3)

### 🎯 Next week

**Team Plan**
- Continue preparing final presentation materials.

**Bao Nguyen**
- Finalize the electrical design diagrams (system block diagram and control-circuit layout) for the presentation.

**Fearghus Tyler**
- Finalize the component-selection list / BOM (VFD, PLC, HMI, contactor, breakers, PSU) for the presentation.

**Yaqoub Rabiah**
- Finalize the PLC control-logic write-up and clean up the ladder comments for the presentation.

**Fox Kang**
- Finalize the safety documentation — E-stop chain, interlocks, and the accident-scenario flow chart — for the presentation.

### 🚧 Blocked
- None.

---

## Report date: 2026-03-06

### ✅ Last week  ·  _hours in parentheses_

**Team Review**
- The team finally got the parts they requested.

**Bao Nguyen**
- Fit parts to our prototype and wire it. (3)

**Fearghus Tyler**
- Fit parts to our prototype and wire it. (3)

**Yaqoub Rabiah**
- Started figuring out C-more to program the HMI. (3)

**Fox Kang**
- Cargo delay; exploring backup plans. (2)

### 🎯 Next week

**Team Plan**
- Try figuring out the VFD phases to have a working motor.

**Bao Nguyen**
- Continue wiring the prototype and bring up the VFD + motor combo — verify phase wiring and get the motor spinning under VFD control.

**Fearghus Tyler**
- Continue fitting and landing the newly arrived parts on the protoboard and tidy up the control wiring.

**Yaqoub Rabiah**
- Continue learning C-more and building out the HMI screens (Ready/Running/Fault, start/stop, status display).

**Fox Kang**
- Pursue a capacitive-touch backup approach while waiting on the chip — breadboard a simple touch sensor and sketch the X7 stop interface.

### 🚧 Blocked

**Bao Nguyen**
- Waiting on E-stop switch.

**Fearghus Tyler**
- Schematic finalization waiting on the ME team's enclosure dimensions.

**Yaqoub Rabiah**
- Still getting C-more set up to program the HMI.

**Fox Kang**
- Cargo delay on capacitive-touch parts.

---

## Report date: 2026-03-13

### ✅ Last week  ·  _hours in parentheses_

**Team Review**
- Started wiring up our prototype and getting the VFD to work.

**Bao Nguyen**
- Work on the VFD and motor combo. (3)

**Fearghus Tyler**
- Work on the VFD and motor combo. (3)

**Yaqoub Rabiah**
- Continued developing the HMI GUI. (3)

**Fox Kang**
- Get the capacitive-touch chip and prepare for the demo. (3)

### 🎯 Next week

**Team Plan**
- Finalize the documentation before spring break.

**Bao Nguyen**
- Continue VFD/motor bring-up — tune the basic run parameters — and document the wiring/parameter setup before spring break.

**Fearghus Tyler**
- Continue the VFD/motor wiring and update the schematics to match the as-built prototype.

**Yaqoub Rabiah**
- Continue developing the HMI GUI — refine the screen layout and link the tags to the PLC.

**Fox Kang**
- Prepare the capacitive-touch chip for the demo — wire it up and verify a basic touch trip.

### 🚧 Blocked
- None.

---

## Report date: 2026-03-16

### ✅ Last week  ·  _hours in parentheses_

**Team Review**
- The team finalized project documentation and presentation materials.

**Bao Nguyen**
- Updated diagrams and documentation. (3)

**Fearghus Tyler**
- Reviewed schematic documentation. (2)

**Yaqoub Rabiah**
- Reviewed PLC control-logic documentation. (2)

**Fox Kang**
- Reviewed safety documentation. (2)

### 🎯 Next week

**Team Plan**
- Use connectors to make it easy for the ME team to install onto the shredder.
- With the extra time we have, we can implement other kinds of safety sensors.

**Bao Nguyen**
- Add quick-connect connectors at the panel boundary so the ME team can plug in the electrical system during shredder install.

**Fearghus Tyler**
- Update the schematics and wiring diagrams to show the connectorized field/cabinet interface.

**Yaqoub Rabiah**
- Continue the PLC/HMI documentation and keep the points list in sync with the logic.

**Fox Kang**
- Use the extra time to explore additional safety sensors (e.g., lid interlock, light curtain) beyond the capacitive touch.

### 🚧 Blocked
- None.

---

> _Spring break between 2026-03-16 and 2026-04-03._

---

# Spring Term (April – June 2026)

## Week 1 — Report date: 2026-04-03

### ✅ Last week  ·  _hours in parentheses_

**Team Review**
- Refocused on getting back on track after spring break (3 hours)

**Bao Nguyen (4)**
- Redoing the points list in the sponsor's preferred style — `PLC/Point_List.xlsx` is the source of truth for every X/Y and analog point. (4)
- Installed and wired the E-stop button (Eaton **E22B1** NC mushroom) in series with the **SD-N35** contactor coil A1 (A2 → PSU −V); PLC **X4** taps the A1 node to monitor the chain. (1)

**Fearghus Tyler**
- Continued the AutoCAD wiring schematics/model to match the points list — keeping the component blocks in sync with the I/O map. (2)
- Continued support in wiring and design aspects of the protoboard. (1)
- Revised 3D model to accommodate sponsor feedback. (1)

**Yaqoub Rabiah**
- Figured out a rework of the HMI GUI. Concept wasn't liked by the sponsor. Made it sleeker in concept. (3 hours)

**Fox Kang**
- Working on capacitive-touch concept.
- Researched capacitive-sensing approaches for the operator-presence safety feature using an ESP32; scoped a touch-to-stop interlock that drops the run command via PLC input **X7**. (3 hours)

### 🎯 Next week

**Team Plan**
- Start integrating the PLC, VFD, and HMI together for our demo.
- Start materializing the final report.
- Start prototyping the capacitive-touch feature.

**Bao Nguyen**
- Start integrating PLC with the circuit to turn on and control the VFD.

**Fearghus Tyler**
- Set up the VFD to work using the analog and digital inputs instead of the default factory settings (0–10 V).
- Coordinated with the industry sponsor controls team to confirm preferred termination conventions.
- Cross-reference motor data against VFD.

**Yaqoub Rabiah**
- Start integrating PLC with the circuit to turn on and control the VFD.

**Fox Kang**
- Editing code comments and preparing connecting the module to the PLC.

### 🚧 Blocked

**Bao Nguyen**
- PLC 24 V module not suitable for contactor and LED control — need to find a relay module instead.

**Fearghus Tyler**
- Need to know where the connections will be before finishing the schematics.

**Yaqoub Rabiah**
- VFD speed-reference/RPM control wiring pending the analog-module configuration.

**Fox Kang**
- Capacitive-touch concept still pending feedback from Ichor's EE/controls team before parts selection.

---

## Week 2 — Report date: 2026-04-10

### ✅ Last week  ·  _hours in parentheses_

**Team Review**
- Made progress towards the capacitive-touch feature; works on a small scale. (5 hours)
- Integrated the PLC to the circuit. Contactor turns on with deadman switches, as well as the VFD. (8 hours)

**Bao Nguyen**
- Rewired the PLC and contactor for clean integration — moved the **SD-N35** coil out of the PLC output into the hardwired E-stop chain (previously driven by D2-08TD2 Y0). (4 hours)
- Identified the problematic module — the **F2-06AD-1** 4–20 mA current-input on the speed-reference path wasn't behaving; flagged it for a swap. (4 hours)

**Fearghus Tyler**
- Tested the protoboard with the analog and digital inputs. Ready to test with HMI. (2)
- Created some 2D wiring diagrams of different versions for field vs. internal cabinet wiring. (2)

**Yaqoub Rabiah**
- Reprogrammed the logic code for the PLC, ensuring the bits corresponded to the physical circuit. (2 hours)
- Debugged the deadman and start/stop functions to specs while integrating the PLC. (4 hours)
- Laid the foundation for the weekly progress reports. (3 hours)

**Fox Kang**
- Prototyped the ESP32 capacitive-touch sensor on a breadboard; confirmed it triggers reliably on a small test surface. (5 hours)
- Began wiring the module output toward the PLC **X7** input for the touch-to-stop interlock.

### 🎯 Next week

**Team Plan**
- Continue integrating the PLC, VFD, and HMI together for our demo.
- Start materializing the final report.

**Bao Nguyen**
- Continue integrating PLC with the circuit to turn on the VFD.

**Fearghus Tyler**
- Work with the industry sponsor to schedule a controls-team review of our materials.
- Investigated VFD behavior under current control vs. voltage control. Documented the odd current readings off the module (possibly broken?).

**Yaqoub Rabiah**
- Continue reworking the logic and HMI design for further integration.

**Fox Kang**
- Tune sensitivity and debounce on the cap-touch prototype; reduce false triggers before PLC integration.

### 🚧 Blocked

**Bao Nguyen**
- Waiting on the relay module to properly interface the PLC output with the contactor and indicator LEDs.

**Fearghus Tyler**
- Need to know their final motor specs.

**Yaqoub Rabiah**
- RPM control is acting weird.

**Fox Kang**
- Cap-touch prototype gets false triggers from electrical noise near the panel; needs filtering before PLC integration.

---

## Week 3 — Report date: 2026-04-17

### ✅ Last week  ·  _hours in parentheses_

**Team Review**
- Integrating PLC, HMI, VFD and motor. (8 hours)

**Bao Nguyen**
- Investigated why the 12–24 VDC transistor output module (**D2-08TD2**) was not behaving like a proper on/off switch. Discovered that although it functions as a switch, the lowest output voltage is still too high to reliably control devices that require a clean digital signal, such as the contactor. (4)
- Located a **D2-08TR** 8-ch relay-output module (dry contact, sinking, common to PSU −V) in the Power Lab and wired it in to properly interface the PLC output with external loads. Tested it using the on-module indicator lights to confirm correct switching. (2)
- Began studying the analog modules — **F2-08AD-1** (4–20 mA current in, Slot 3) and **F2-08DA-2** (0–10 V out, Slot 6) — to work out their wiring, scaling, and integration method. (6)

**Fearghus Tyler**
- Proposed switching from current control to voltage control (0–10 V) to the team and sponsor. (1)
- Updated 2D schematic to reflect planned analog module swap. (2)
- Revised 3D control-panel model to show new voltage-module placement and wire routing.

**Yaqoub Rabiah**
- Integrated a scale for RPM control from the HMI to the PLC. (2 hours)
- Added forward and reverse capabilities into PLC logic and integrated it into the HMI. (5 hours)
- Reworked the numerical displays on the HMI main page — a voltage / current / frequency / RPM read-out section (some fields not yet operational, pending the analog/telemetry scaling). (2 hours)
- Debugged the connection between the PLC and HMI. The protocols weren't matching. (2 hours)
- Found a problem with the current-control module and tried to debug. (4 hours)

**Fox Kang**
- Continued bench prototyping of the cap-touch module; worked on suppressing false triggers from electrical noise near the panel. (4 hours)

### 🎯 Next week

**Team Plan**
- Figure out the problem of the low amperage variance in the current-control module.

**Bao Nguyen**
- Continue studying the analog module — determine the correct field wiring and the PLC scaling so the VFD speed reference and motor-current feedback read correctly.

**Fearghus Tyler**
- Reprogrammed VFD parameters from current-control to voltage-control (0–10 V) following the analog-module swap — `PD002=1` for the **VI** 0–10 V speed reference, motor-current monitor on **VO** via `PD054=1`. (3)
- Bench-tested VFD response to 0–10 V signal from PLC; verified linear RPM control within expected range. (2)
- Updated schematics and 2D wiring diagrams to reflect final analog module configuration and E-stop logic paths. (3)
- Generated updated 3D enclosure model for ICHOR's final design package. (2)

**Yaqoub Rabiah**
- Fix logic for the cc module.

**Fox Kang**
- Prepare cap-touch module output for wiring to PLC X7 and test the touch-trip stop.

### 🚧 Blocked

**Bao Nguyen**
- Currently working on understanding how the analog module is wired and configured within the PLC system. Still determining the correct wiring for the analog inputs/outputs and how the signals should be scaled and interpreted by the PLC. Further testing and documentation review are needed before integration with the rest of the system.

**Fearghus Tyler**
- Troubleshooting current-controlled VFD motor control; running into issues with ranges.

**Yaqoub Rabiah**
- Can't seem to program the current-control module such that the range is more than 0–0.3 mA.

**Fox Kang**
- Can't wire the cap-touch module to X7 until the PLC integration is sorted out.

---

## Week 4 — Report date: 2026-04-24

### ✅ Last week  ·  _hours in parentheses_

**Team Review**
- Swapped current control with voltage control module, thus ending current-control confusion.

**Bao Nguyen**
- Swapped the current-input module for the **F2-08DA-2** 0–10 V analog-output module (drives VFD **VI**) and read the configuration docs. Found the V-memory bits holding the scaled RPM from the Do-more scaling instruction (with Yaqoub). (4)
- Working with Fearghus on reprogramming the VFD. (2)

**Fearghus Tyler**
- Tested and reprogrammed the VFD to match the move from the current-controlled to the voltage-controlled module — set `PD002=1` and verified 0 V = 0 Hz, 10 V = max frequency on **VI**. (4)
- Prepare any remaining VFD/PLC/HMI integration specs before demo.

**Yaqoub Rabiah**
- Reprogrammed the PLC to accommodate the new module. (2 hours)
- Added LED logic — **Y0** green (forward) / **Y1** yellow (reverse) — and swapped bits for easier wiring (VFD **FOR=Y6, REV=Y7, RST=Y5**, sinking to DCM). (1 hour)
- Added E-stop logic (monitored on **X4**) and a warning-light output (**Y4** → Wamco 525, 28 VDC) for safety. (1 hour)

**Fox Kang**
- Refined cap-touch firmware/code comments and prepped the module for hand-off to PLC integration. (3 hours)

### 🎯 Next week

**Team Plan**
- Do the presentation.

**Bao Nguyen**
- Support presentation prep and start sourcing the remaining parts — relay module, enclosure, and braking resistor.

**Fearghus Tyler**
- Figure out any last-minute parts we could integrate.
- Investigate braking resistor.

**Yaqoub Rabiah**
- Get ready for presentation.

**Fox Kang**
- Prepare cap-touch demo material for the presentation.

### 🚧 Blocked

**Bao Nguyen**
- None — presentation week, no blockers.

**Fearghus Tyler**
- None.

**Yaqoub Rabiah**
- None.

**Fox Kang**
- Awaiting the final cap-touch parts/relay before the full PLC hand-off.

---

## Week 5 — Report date: 2026-05-01

### ✅ Last week  ·  _hours in parentheses_

**Team Review**
- Did presentation. (2 hours)
- Prototyped capacitive touch. (2 hours)

**Bao Nguyen**
- Worked with Fox to tune and build a prototype of the CTSI capacitive-touch safety interface. (2)
- Identified new parts needed — a dynamic braking resistor (ATO **APCS-300R30-AD**, 300 W / 30 Ω on VFD **P+/PR**) and the enclosure.

**Fearghus Tyler**
- Sized the dynamic braking resistor (~30 Ω, 300 W for VFD **P+/PR**) — landed on the ATO **APCS-300R30-AD**. (1)
- Got started on a user manual. (2)
- Receiving final supplies from industry sponsors (enclosure, braking resistor, relay for integrating capacitive touch). (1)

**Yaqoub Rabiah**
- Worked on presentation slides. (1 hour)

**Fox Kang**
- Worked with Bao to tune the ESP32 CTSI capacitive-touch prototype (still on a breadboard); confirmed the touch-to-stop concept on the bench. Started planning the move to a soldered, enclosed module. (2 hours)

### 🎯 Next week

**Team Plan**
- Work on enclosure.

**Bao Nguyen**
- Continue identifying and ordering remaining parts (braking resistor, enclosure, relay) and help start the enclosure build.

**Fearghus Tyler**
- Build and test.

**Yaqoub Rabiah**
- Try integrating overcurrent signal.

**Fox Kang**
- Continue developing the CTSI capacitive-touch module toward panel integration — finalize the sensor circuit and the X7 interface.

### 🚧 Blocked

**Bao Nguyen**
- Can't progress on the enclosure build until the enclosure and remaining parts (braking resistor, relay) arrive from the sponsor.

**Fearghus Tyler**
- We can't test a lot of the functionality we had aimed for due to no shredder prototype built yet.

**Yaqoub Rabiah**
- Waiting for parts.

**Fox Kang**
- Waiting on the relay for integrating capacitive touch.

---

## Week 6 — Report date: 2026-05-08

### ✅ Last week  ·  _hours in parentheses_

**Team Review**
- Not much (midterm exam week).

**Bao Nguyen**
- Nothing — exam week.

**Fearghus Tyler**
- Midterm exams took priority; we mostly worked on documentation.
- Minor schematic changes based on the PLC logic for switching.

**Yaqoub Rabiah**
- Not much also (exam week).

**Fox Kang**
- Exam week — minimal progress; reviewed cap-touch integration plan.

### 🎯 Next week

**Team Plan**
- Work on enclosure setup.

**Bao Nguyen**
- Resume parts sourcing and enclosure prep after exams.

**Fearghus Tyler**
- Get the last parts from Ichor Systems.

**Yaqoub Rabiah**
- Try integrating overcurrent signal.

**Fox Kang**
- Resume cap-touch integration once the relay arrives.

### 🚧 Blocked

**Bao Nguyen**
- Exam week — no project time; also waiting for parts.

**Fearghus Tyler**
- Waiting for parts.

**Yaqoub Rabiah**
- Waiting for parts.

**Fox Kang**
- Waiting for parts.

---

## Week 7 — Report date: 2026-05-15

### ✅ Last week  ·  _hours in parentheses_

**Team Review**
- Set up the control panel to go inside the enclosure. (5 hours)
- Worked on the overcurrent-signal integration. (10 hours)

**Bao Nguyen**
- Helped lay out and wire the control panel into the enclosure — landed 12 AWG THHN power runs (rated 20/25/30 A at 60/75/90 °C per NEC 310.16; motor FLA ≈ 7.6 A) and ferruled 16–18 AWG control wiring; supported the overcurrent signal into **X5**. (12 hours)

**Fearghus Tyler**
- We got our enclosure, so I worked on the CAD designs for the panel design and additional panel DWGs. (4)
- Did a lot of troubleshooting and design changes for a clean enclosure. (3)
- Helped Fox periodically with the cap-touch module. (1)

**Yaqoub Rabiah**
- Wrote logic that takes the overcurrent signal and runs an unjam algorithm to clear the shredder — VFD fault relay **FA/FC** programmed `PD052=02` → +24 V into PLC **X5**; the routine pulses **Y5 → VFD RST** (~500 ms) with a 3-strike lockout. (10 hours)
- Helped design the enclosure layout. (1 hour)
- Drilled holes on the panel that holds the major components (VFD, contactor, circuit breakers, etc.). (1 hour)
- Helped wire the components in the enclosure. (2 hours)

**Fox Kang**
- Worked on the ESP32 CTSI module with Fearghus's help toward wiring it into panel **X7**; hit a bug where it works powered from a PC (USB) but bugs out standalone on the wall-outlet supply — a grounding / clean-power issue. Began soldering the module off the breadboard. (4 hours)

### 🎯 Next week

**Team Plan**
- Finish up the enclosure setup and make sure it works — plug 'n' play.

**Bao Nguyen**
- Continue enclosure wiring and verify panel integration — confirm relay-driven contactor switching and the overcurrent signal into the PLC.

**Fearghus Tyler**
- Work on the final documentation / user manual / designs.

**Yaqoub Rabiah**
- Finish enclosure setup.
- Make sure logic works.
- Set up cap touch.

**Fox Kang**
- Integrate and test the cap-touch module on X7 in the enclosure.

### 🚧 Blocked

**Bao Nguyen**
- Can't validate the overcurrent trip threshold without a real shredding load — no shredder prototype to test on yet.

**Fearghus Tyler**
- Still no prototype shredder to test on.

**Yaqoub Rabiah**
- Overcurrent-clear algorithm can't be tuned against real jam currents until a prototype exists; limited to bench simulation.

**Fox Kang**
- CTSI module works on PC USB but bugs out on the standalone wall supply (grounding/noise); needs a stable supply before it can trip **X7** reliably.

---

## Week 8 — Report date: 2026-05-22

### ✅ Last week  ·  _hours in parentheses_

**Team Review**
- Continued enclosure wiring and panel troubleshooting; coordinated parts hand-off with the mechanical team.
- Roughly 20 team-hours this week.

**Bao Nguyen**
- Continued wiring/troubleshooting the control panel and verifying PLC I/O against the points list. (14 hours)

**Fearghus Tyler**
- Worked on wiring the panel / troubleshooting. (5)
- Helped the mech team get their parts (at long last). (3)

**Yaqoub Rabiah**
- Continued debugging PLC logic against the wired panel; verified overcurrent-clear routine behavior. (6 hours)

**Fox Kang**
- Built up the CTSI module — received the 24 V→3 V converter (to run the ESP32 off the panel 24 V), an optocoupler to isolate the output into **X7**, and an enclosure box; soldering it together off the breadboard. Accidentally fed 24 V into the ESP32 while wiring and fried it; sourced and installed a replacement. (4 hours)

### 🎯 Next week

**Team Plan**
- Finish the panel/enclosure wiring and shift focus to final documentation — final report, user manual, and schematics.

**Bao Nguyen**
- Finalize the as-built wiring documentation and points list, and wrap up any remaining panel work.

**Fearghus Tyler**
- Help assemble the first edition of the shredder.

**Yaqoub Rabiah**
- Document the PLC control logic and HMI, and verify the logic on the bench setup.

**Fox Kang**
- Finalize and document the capacitive-touch module and bench-test the touch trip.

### 🚧 Blocked

**Bao Nguyen**
- Integrated/load testing still blocked — no completed shredder; work limited to bench checks and documentation.

**Fearghus Tyler**
- Waiting on the ME team to finish the shredder frame before final install and testing.

**Yaqoub Rabiah**
- Can't validate the control logic under real motor load without the mechanical prototype.

**Fox Kang**
- Replacement ESP32 in and powered via the 24 V→3 V converter; still finishing the soldered/enclosed build and verifying the optocoupler trips **X7** cleanly.

---

## Week 9 — Report date: 2026-05-30

### ✅ Last week  ·  _hours in parentheses_

**Team Review**
- Focused on documentation — drafting the final report, the user manual, and exporting the final schematics/diagrams for the report appendix.

**Bao Nguyen**
- Wrote the EE sections of the final report (wiring, sizing, safety) and finalized the as-built wiring documentation and points list. (16 hours)

**Fearghus Tyler**
- Continued the final documentation and user manual; exported the final schematics and the 3D enclosure model for the design package. (8 hours)

**Yaqoub Rabiah**
- Documented the PLC control logic and HMI screens; wrote up the control-logic section of the report. (8 hours)

**Fox Kang**
- Finished the soldered, enclosed CTSI module (ESP32 + 24 V→3 V converter + optocoupler to **X7**) and documented its design for the report. (6 hours)

### 🎯 Next week

**Team Plan**
- Finish and submit the final report, complete the user manual, and prepare the end-of-term demo/poster.

**Bao Nguyen**
- Finalize the wiring documentation (as-built diagrams, points list) and complete the EE sections of the final report.

**Fearghus Tyler**
- Finish user manual and export final schematics/DWGs for the report appendix.

**Yaqoub Rabiah**
- Finalize PLC/HMI documentation and write up the control-logic section.

**Fox Kang**
- Document the cap-touch module and write up its section.

### 🚧 Blocked

**Bao Nguyen**
- Final end-to-end/load testing still not possible — no completed shredder; report documents bench results only.

**Fearghus Tyler**
- Mechanical prototype still not built, so the install-and-test parts of the user manual are based on the bench setup.

**Yaqoub Rabiah**
- Can't capture real run/jam data for the report without a working shredder; the analog current monitor (VFD **VO** → **F2-08AD-1** CH1) is wired but still needs scaling/calibration.

**Fox Kang**
- Couldn't demonstrate the cap-touch trip on the full machine — only on the bench.

---

## Week 10 — Report date: 2026-06-06

### ✅ Last week  ·  _hours in parentheses_

**Team Review**
- Completed and submitted the final report and user manual, and presented at the capstone demo/expo.

**Bao Nguyen**
- Completed EE report sections (wiring, sizing, safety) and supported the final demo. (12 hours)

**Fearghus Tyler**
- Finalized the user manual and design package; delivered final schematics and 3D enclosure model. (8 hours)

**Yaqoub Rabiah**
- Finalized PLC/HMI control documentation and supported the demo. (8 hours)

**Fox Kang**
- Finalized the capacitive-touch module documentation and demonstrated the touch-to-stop safety feature. (6 hours)

### 🎯 Next week

**Team Plan**
- Term complete — project handed off to the sponsor.

**Bao Nguyen**
- N/A — end of term.

**Fearghus Tyler**
- N/A — end of term.

**Yaqoub Rabiah**
- N/A — end of term.

**Fox Kang**
- N/A — end of term.

### 🚧 Blocked

**Bao Nguyen**
- None — end of term; full-load testing left for a future build phase with the ME prototype.

**Fearghus Tyler**
- None — end of term.

**Yaqoub Rabiah**
- Telemetry was never fully implemented: the HMI has a voltage / current / frequency / RPM read-out section, but some fields are non-operational. The analog motor-current monitor (VFD **VO** → **F2-08AD-1** CH1) is wired but only partially working — still needs scaling/calibration. Ran out of time; documented as future work.

**Fox Kang**
- None — end of term.
