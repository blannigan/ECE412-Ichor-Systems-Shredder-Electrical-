# Test Plan v1.0 — Universal Plastic Shredder V2.0 Electrical System

**Course:** ECE 412 Senior Project Development, Portland State University  
**Sponsor:** MME / Ichor Systems (Bridget Lannigan)  
**Team:** Bao Nguyen, Fearghus Tyler, Yaqoub Rabiah, Fox Kang  
**Date of Test:** ___________  
**Tester:** ___________

---

## Purpose

To verify the electrical control system of the Universal Plastic Shredder V2.0 against its requirements, using both top-down (full-system operational) and bottom-up (subsystem-by-subsystem) test methods.

---

## Equipment Needed

### System Equipment
- Shredder electrical enclosure (PLC, VFD, contactor, fuse blocks, PSU, wiring complete)
- EA1-T4CL C-More Micro-Graphic HMI touch panel (mounted, cabled)
- 3–5 HP motor + gearbox (ME interface, mechanically coupled)
- E-stop button, two-hand start buttons (Fwd, Deadman SW1/SW2), lid interlock switch
- Status indicator lights (Power / Running / Fault)
- AC power cord/supply (120 VAC or 208–240 VAC, as applicable)

### Test Equipment
- Digital multimeter (voltage, continuity, current clamp)
- Tachometer or optical RPM sensor (to verify shaft speed)
- Clamp-on ammeter (motor current)
- Laptop with DirectSOFT5 (PLC programming software) and USB-to-serial adapter
- C-More programming cable + EA-MG-PGM-CBL software cable (for HMI)
- Sample plastic pieces: PVC, PP, or LDPE sheet, 0.25–0.5" thick, 4–12" wide

### Other Equipment
- Personal protective equipment: safety glasses, hearing protection
- Fire extinguisher (Class C, electrical)
- Second person present for all powered tests (safety requirement for industrial equipment)

---

## Pre-Test Setup

1. Confirm the area around the shredder is clear of loose material.
2. Confirm the lid interlock switch is functional: manually actuate it and verify the NC contact opens/closes with a multimeter before powering on.
3. Set the AC power supply to match the system's rated input voltage. Verify with a multimeter before connecting.
4. Confirm all wiring terminations are secure (no loose lugs, no exposed conductors).
5. Confirm fuses are seated: 25A (PSU branch), 1A (PLC branch), 1.5A (pushbutton commons), 1/2A slow-blow (contactor coil fuse DF103V).
6. Connect DirectSOFT5 laptop to the H2-DM1E CPU via Ethernet or serial — confirm communication before starting tests.
7. Confirm the VFD (HY02D211B-T) is powered off and the contactor (SD-N35) is open before initial power-on.
8. Place test plastic material near the input chute but do not feed until instructed.

---

## Part 1: Top-Down Test

*Tests M1, M2, M4, M6, M7, M9, S1, S3*

### Top-Down Test Steps

**Phase 1 — Power On**

1. Switch on main AC disconnect / power switch.
   - **Power indicator light** (status light) should illuminate. ☐  *Tests: S1 (power indicator)*
   - Measure 24VDC at PSU output terminals. Should be 24 ± 2 VDC. Reading: _______ V  
   - PLC CPU (H2-DM1E) should boot — RUN LED on CPU should go green within ~5 seconds. ☐

2. Observe HMI display (EA1-T4CL).
   - Display should power on and show **"IDLE / READY"** state screen. ☐  *Tests: M9 (HMI powers on)*
   - Confirm system state shown on HMI reads: **Idle** ☐  *Tests: M9 (state display)*

**Phase 2 — Safety Pre-check (lid open, no start)**

3. Confirm lid interlock is triggered (lid open or switch manually held open).
   - Attempt to press Forward button.
   - Motor must NOT start. ☐  *Tests: M6 (lid interlock prevents run)*
   - HMI should display fault or interlock message. ☐

4. Close lid (or release interlock switch). HMI should return to Ready/Idle state. ☐

**Phase 3 — Normal Start Sequence**

5. With lid closed, press and hold both Deadman SW1 and SW2 simultaneously, then press Forward.
   - Contactor (SD-N35) should close (audible click). ☐
   - Motor should begin spinning. ☐
   - **Running indicator light** should illuminate. ☐  *Tests: S1 (running indicator)*
   - HMI should display **"Running"** state and current motor speed (RPM or Hz). ☐  *Tests: M9 (running state display)*

6. Allow motor to reach steady-state speed (~5 seconds). Measure output shaft RPM with tachometer.
   - Reading: _______ RPM. Should be 70–90 RPM. ☐  *Tests: M7 (speed in range)*
   - If speed is outside range, note VFD frequency command and adjust as needed.

**Phase 4 — Shred Test**

7. With motor running at target speed, hand-feed one plastic test piece (0.25–0.5" thick, 4–12" wide) into the input chute.
   - Shredder should accept and process the piece without stalling or faulting. ☐
   - Collect output — pieces should be approximately 1" in size. ☐  *Tests: M1 (shreds to ~1")*
   - Motor should return to target RPM after piece clears. ☐

**Phase 5 — Normal Stop**

8. Release one or both Deadman buttons (or press Stop if available on HMI).
   - Motor should stop (contactor opens). ☐
   - Running light should extinguish. ☐
   - HMI should return to **"Idle"** state. ☐

**Phase 6 — Emergency Stop**

9. Restart motor per Step 5. Confirm motor is running.
10. Press E-stop button.
    - Motor must stop immediately (contactor drops out). ☐  *Tests: M4 (E-stop shuts down)*
    - Running light should extinguish. ☐
    - HMI should display **"Fault / E-stop"** state. ☐  *Tests: M9 (fault state display)*
    - **Fault indicator light** should illuminate. ☐  *Tests: S1 (fault indicator)*

11. Twist/release E-stop button to reset.
    - Confirm system returns to Idle (motor does not auto-restart). ☐  *Tests: M4 (no auto-restart after E-stop)*

**Phase 7 — Power Off**

12. Switch off main AC disconnect.
    - All lights should extinguish. HMI should power off. Motor (if running) should stop. ☐

### Top-Down Test Conclusions

| Requirement | Result | Notes |
|---|---|---|
| M1 — Shreds to ~1" | ☐ Pass ☐ Fail | |
| M2 — VFD used and controllable | ☐ Pass ☐ Fail | |
| M4 — E-stop shuts down safely | ☐ Pass ☐ Fail | |
| M6 — Lid interlock prevents run | ☐ Pass ☐ Fail | |
| M7 — 70–90 RPM shaft speed | ☐ Pass ☐ Fail | Measured: _____ RPM |
| M9 — HMI shows state and control | ☐ Pass ☐ Fail | |
| S1 — Status/fault lights work | ☐ Pass ☐ Fail | |
| S3 — Controls clearly labeled | ☐ Pass ☐ Fail | |

---

## Part 2: Bottom-Up Test

---

### Test Case BU-01: AC Power Input and Fuse Block

| | |
|---|---|
| **Test ID** | BU-01 |
| **Test Case Name** | AC Power Input and Fuse Distribution |
| **Description** | Verify AC power reaches the fuse block and distributes correctly to the PSU and PLC branches. |
| **Type** | Black box |
| **Tester** | |
| **Date** | |
| **HW/SW Version** | 1.0 |
| **Setup** | Main disconnect OFF. Multimeter set to AC voltage. |

| # | Input | Expected Output | Pass | Fail | N/A | Comments |
|---|---|---|---|---|---|---|
| 1 | Main disconnect ON | AC line voltage present at EURO S10H-5H fuse block input (measure L and N terminals) | ☐ | ☐ | ☐ | Reading: _____ VAC |
| 2 | Main disconnect ON | 25A fuse branch: AC present at PSU input terminals | ☐ | ☐ | ☐ | |
| 3 | Main disconnect ON | 1A fuse branch: AC present at PLC L terminal | ☐ | ☐ | ☐ | |
| 4 | Pull 25A fuse (disconnect first) | AC removed from PSU branch; PLC branch unaffected | ☐ | ☐ | ☐ | |
| 5 | Reinstate 25A fuse | Normal distribution restored | ☐ | ☐ | ☐ | |

**Overall BU-01 Result:** ☐ Pass ☐ Fail

---

### Test Case BU-02: 24VDC Power Supply

| | |
|---|---|
| **Test ID** | BU-02 |
| **Test Case Name** | 24VDC PSU Output (Mean Well NDR-480-24) |
| **Description** | Verify the PSU outputs correct 24VDC to PLC I/O, contactor coil, and pushbutton commons. |
| **Type** | Black box |
| **Tester** | |
| **Date** | |
| **HW/SW Version** | 1.0 |
| **Setup** | AC power ON. Multimeter set to DC voltage. |

| # | Input | Expected Output | Pass | Fail | N/A | Comments |
|---|---|---|---|---|---|---|
| 1 | AC applied to PSU | +V terminal: 24 ± 2 VDC at PSU output | ☐ | ☐ | ☐ | Reading: _____ VDC |
| 2 | AC applied to PSU | –V terminal: 0V (return) | ☐ | ☐ | ☐ | |
| 3 | AC applied | 1.5A fused pushbutton commons: 24VDC at each common (Fwd, Rev, DM1, DM2) | ☐ | ☐ | ☐ | |
| 4 | AC applied | Contactor coil A2 terminal: 0VDC (contactor open at rest) | ☐ | ☐ | ☐ | |

**Overall BU-02 Result:** ☐ Pass ☐ Fail

---

### Test Case BU-03: PLC Boot and Communication

| | |
|---|---|
| **Test ID** | BU-03 |
| **Test Case Name** | PLC Rack Initialization (DirectLOGIC 205) |
| **Description** | Verify the PLC CPU boots, all modules are recognized, and DirectSOFT5 can read I/O status. |
| **Type** | White box |
| **Tester** | |
| **Date** | |
| **HW/SW Version** | 1.0 |
| **Setup** | AC power ON. DirectSOFT5 open on laptop and connected to H2-DM1E via Ethernet. |

| # | Input | Expected Output | Pass | Fail | N/A | Comments |
|---|---|---|---|---|---|---|
| 1 | Power on PLC | CPU RUN LED: solid green within 10 seconds | ☐ | ☐ | ☐ | |
| 2 | DirectSOFT5 connect | PLC goes online; no I/O errors reported | ☐ | ☐ | ☐ | |
| 3 | DirectSOFT5 data view | All discrete inputs X0–X7 readable (0 or 1) | ☐ | ☐ | ☐ | |
| 4 | DirectSOFT5 data view | All discrete outputs Y0–Y7 readable (0 at startup) | ☐ | ☐ | ☐ | |
| 5 | DirectSOFT5 data view | Analog input F2-06AD-1 registers readable | ☐ | ☐ | ☐ | |
| 6 | DirectSOFT5 data view | RTD input F2-04RTD registers readable; ambient temp reasonable (15–30 °C) | ☐ | ☐ | ☐ | Reading: _____ °C |
| 7 | Ladder logic running | No ladder logic errors or fault codes in CPU status | ☐ | ☐ | ☐ | |

**Overall BU-03 Result:** ☐ Pass ☐ Fail

---

### Test Case BU-04: Emergency Stop Circuit

| | |
|---|---|
| **Test ID** | BU-04 |
| **Test Case Name** | E-Stop Hardware Safety Circuit |
| **Description** | Verify the E-stop button breaks the safety circuit and drops all motor-related outputs. Tests M4. |
| **Type** | Black box |
| **Tester** | |
| **Date** | |
| **HW/SW Version** | 1.0 |
| **Setup** | AC power ON, PLC running ladder logic. Motor is NOT running. Multimeter on safety circuit nodes. |

| # | Input | Expected Output | Pass | Fail | N/A | Comments |
|---|---|---|---|---|---|---|
| 1 | E-stop released (normal) | Safety circuit continuity: confirmed (multimeter, or circuit logic per deadman_logic2.pdf) | ☐ | ☐ | ☐ | |
| 2 | Press E-stop | Safety circuit opens immediately | ☐ | ☐ | ☐ | |
| 3 | Press E-stop while motor running (from BU-07 run) | Contactor (SD-N35) drops out within 1 second | ☐ | ☐ | ☐ | |
| 4 | Press E-stop | Y0 (contactor coil output) = 0 in DirectSOFT5 | ☐ | ☐ | ☐ | |
| 5 | Release E-stop (twist/pull) | System does NOT auto-restart motor | ☐ | ☐ | ☐ | |
| 6 | Release E-stop, then re-initiate two-hand start | Motor can restart normally after E-stop reset | ☐ | ☐ | ☐ | |

**Overall BU-04 Result:** ☐ Pass ☐ Fail

---

### Test Case BU-05: Two-Hand Start / Deadman Circuit

| | |
|---|---|
| **Test ID** | BU-05 |
| **Test Case Name** | Two-Hand Start (Deadman) Safety Logic |
| **Description** | Verify the motor only runs when both deadman buttons are held simultaneously with Forward. Tests M6. |
| **Type** | Black box |
| **Tester** | |
| **Date** | |
| **HW/SW Version** | 1.0 |
| **Setup** | AC power ON, PLC running, E-stop released, lid closed. Per deadman_logic2.pdf. |

| # | Input | Expected Output | Pass | Fail | N/A | Comments |
|---|---|---|---|---|---|---|
| 1 | Press Forward only (no deadman) | Motor does NOT start | ☐ | ☐ | ☐ | |
| 2 | Press SW1 only (no Forward) | Motor does NOT start | ☐ | ☐ | ☐ | |
| 3 | Press SW2 only (no Forward) | Motor does NOT start | ☐ | ☐ | ☐ | |
| 4 | Press SW1 + SW2 (no Forward) | Motor does NOT start | ☐ | ☐ | ☐ | |
| 5 | Press Forward + SW1 only | Motor does NOT start | ☐ | ☐ | ☐ | |
| 6 | Press Forward + SW2 only | Motor does NOT start | ☐ | ☐ | ☐ | |
| 7 | Press Forward + SW1 + SW2 simultaneously | Contactor closes, motor starts | ☐ | ☐ | ☐ | |
| 8 | While running: release SW1 | Motor stops immediately | ☐ | ☐ | ☐ | |
| 9 | While running: release SW2 | Motor stops immediately | ☐ | ☐ | ☐ | |

**Overall BU-05 Result:** ☐ Pass ☐ Fail

---

### Test Case BU-06: Lid Interlock

| | |
|---|---|
| **Test ID** | BU-06 |
| **Test Case Name** | Lid Interlock Safety Input |
| **Description** | Verify the lid interlock switch (discrete input to PLC) prevents motor from running when triggered. Tests M6. |
| **Type** | Black box |
| **Tester** | |
| **Date** | |
| **HW/SW Version** | 1.0 |
| **Setup** | AC power ON, PLC running, E-stop released. Interlock switch accessible. |

| # | Input | Expected Output | Pass | Fail | N/A | Comments |
|---|---|---|---|---|---|---|
| 1 | Lid closed (interlock normal) | PLC discrete input for interlock reads correct state in DirectSOFT5 (note address: ___) | ☐ | ☐ | ☐ | |
| 2 | Open lid (trigger interlock) | Interlock DI changes state in PLC | ☐ | ☐ | ☐ | |
| 3 | Lid open, attempt two-hand start | Motor does NOT start | ☐ | ☐ | ☐ | |
| 4 | Motor running, then open lid | Motor stops within 1 second | ☐ | ☐ | ☐ | |
| 5 | Close lid, reset, re-initiate start | Motor starts normally | ☐ | ☐ | ☐ | |

**Overall BU-06 Result:** ☐ Pass ☐ Fail

---

### Test Case BU-07: VFD Control and Motor Speed

| | |
|---|---|
| **Test ID** | BU-07 |
| **Test Case Name** | VFD Speed Command and Motor RPM (HY02D211B-T) |
| **Description** | Verify PLC analog output CH1 commands correct VFD speed and output shaft reaches 70–90 RPM. Tests M2, M7, M8. |
| **Type** | White box |
| **Tester** | |
| **Date** | |
| **HW/SW Version** | 1.0 |
| **Setup** | AC power ON, PLC running, safety circuits clear, motor mechanically coupled. Tachometer and multimeter ready. |

| # | Input | Expected Output | Pass | Fail | N/A | Comments |
|---|---|---|---|---|---|---|
| 1 | Motor stopped | Measure AO CH1 voltage at VFD terminal AL: ~0V | ☐ | ☐ | ☐ | Reading: _____ V |
| 2 | Initiate two-hand start | Contactor (SD-N35) closes (audible click, LED if present) | ☐ | ☐ | ☐ | |
| 3 | Motor running | AO CH1 voltage at VFD AL terminal: 0–10VDC, nonzero | ☐ | ☐ | ☐ | Reading: _____ V |
| 4 | Motor running at steady state | Tachometer at output shaft: 70–90 RPM | ☐ | ☐ | ☐ | Reading: _____ RPM |
| 5 | Motor running | Clamp ammeter on motor leads: within motor nameplate FLA (Full Load Amps) | ☐ | ☐ | ☐ | Reading: _____ A |
| 6 | Motor running | VFD keypad display: no fault codes (Er.xxx) | ☐ | ☐ | ☐ | |
| 7 | Normal stop (release deadman) | VFD ramps down; shaft stops within _____ seconds | ☐ | ☐ | ☐ | |

**Overall BU-07 Result:** ☐ Pass ☐ Fail

---

### Test Case BU-08: Overcurrent and Overload Protection

| | |
|---|---|
| **Test ID** | BU-08 |
| **Test Case Name** | Overcurrent / Overload Protection (M5) |
| **Description** | Verify the Phoenix Contact motor overload (TMC 83C 15A) and thermal overload (RTD32-180) respond to fault conditions. Tests M5. |
| **Type** | Black box |
| **Tester** | |
| **Date** | |
| **HW/SW Version** | 1.0 |
| **Setup** | AC power ON. Do NOT intentionally overload the motor to destruction; use the trip test button if the overload relay has one, or verify NC contact behavior with multimeter. |

| # | Input | Expected Output | Pass | Fail | N/A | Comments |
|---|---|---|---|---|---|---|
| 1 | Motor stopped | Phoenix Contact TMC 83C NC contact: closed (continuity) | ☐ | ☐ | ☐ | |
| 2 | Press trip/test button on TMC 83C (if available) | NC contact opens; motor contactor cannot close | ☐ | ☐ | ☐ | |
| 3 | Reset TMC 83C | NC contact closes; system restores | ☐ | ☐ | ☐ | |
| 4 | Motor running at rated load | Clamp ammeter: motor current ≤ rated FLA | ☐ | ☐ | ☐ | Reading: _____ A |
| 5 | RTD32-180 thermal overload (OUT3 path) | Verify NC contact (95→96) is in series with F2 contactor coil per wiring diagram | ☐ | ☐ | ☐ | |
| 6 | Simulate thermal trip (if test mode available) | OUT3 drives thermal overload trip; motor stops | ☐ | ☐ | ☐ | |

**Overall BU-08 Result:** ☐ Pass ☐ Fail

---

### Test Case BU-09: HMI Display and State Feedback

| | |
|---|---|
| **Test ID** | BU-09 |
| **Test Case Name** | HMI Operator Interface (EA1-T4CL C-More Micro-Graphic) |
| **Description** | Verify the HMI displays correct system state, speed, and faults, and that operator inputs on HMI are reflected in the system. Tests M9. |
| **Type** | Black box |
| **Tester** | |
| **Date** | |
| **HW/SW Version** | 1.0 |
| **Setup** | AC power ON, PLC running, HMI powered (via shared Mean Well NDR-480-24 24VDC supply). HMI-to-PLC serial link active. |

| # | Input | Expected Output | Pass | Fail | N/A | Comments |
|---|---|---|---|---|---|---|
| 1 | Power on | HMI shows system state: Idle or Ready | ☐ | ☐ | ☐ | |
| 2 | Motor running (via two-hand start) | HMI shows: Running state | ☐ | ☐ | ☐ | |
| 3 | Motor running | HMI displays current motor speed or VFD Hz | ☐ | ☐ | ☐ | |
| 4 | Press E-stop | HMI shows: Fault / E-stop state | ☐ | ☐ | ☐ | |
| 5 | Trigger lid interlock | HMI shows interlock fault or warning | ☐ | ☐ | ☐ | |
| 6 | Reset E-stop | HMI returns to Idle (no auto-restart) | ☐ | ☐ | ☐ | |
| 7 | HMI Stop (if implemented) | Motor stops when Stop pressed on HMI | ☐ | ☐ | ☐ | N/A if not implemented |

**Overall BU-09 Result:** ☐ Pass ☐ Fail

---

### Test Case BU-10: Status Indicator Lights

| | |
|---|---|
| **Test ID** | BU-10 |
| **Test Case Name** | Status Indicator Lights (Power / Running / Fault) |
| **Description** | Verify the three status lights illuminate in the correct system states. Tests S1. |
| **Type** | Black box |
| **Tester** | |
| **Date** | |
| **HW/SW Version** | 1.0 |
| **Setup** | AC power ON, PLC running. |

| # | System State | Power Light | Running Light | Fault Light | Pass | Fail | Comments |
|---|---|---|---|---|---|---|---|
| 1 | Power ON, Idle | ON | OFF | OFF | ☐ | ☐ | |
| 2 | Motor Running | ON | ON | OFF | ☐ | ☐ | |
| 3 | E-stop active | ON | OFF | ON | ☐ | ☐ | |
| 4 | Lid interlock fault | ON | OFF | ON | ☐ | ☐ | |
| 5 | Power OFF | OFF | OFF | OFF | ☐ | ☐ | |

**Overall BU-10 Result:** ☐ Pass ☐ Fail

---

## Requirements Coverage Summary

| Req ID | Requirement | BU Test(s) | Top-Down | Result |
|---|---|---|---|---|
| M1 | Shreds plastic to ~1" | — | Phase 4 | ☐ Pass ☐ Fail |
| M2 | Controllable VFD | BU-07 | Phase 3 | ☐ Pass ☐ Fail |
| M3 | NFPA-70 (NEC) design | BU-01, BU-02 (inspect wiring) | — | ☐ Pass ☐ Fail |
| M4 | E-stop safe shutdown | BU-04 | Phase 6 | ☐ Pass ☐ Fail |
| M5 | Overcurrent/overload protection | BU-08 | — | ☐ Pass ☐ Fail |
| M6 | Safety interlock (lid + two-hand) | BU-05, BU-06 | Phase 2 | ☐ Pass ☐ Fail |
| M7 | 70–90 RPM shaft speed | BU-07 | Phase 3 | ☐ Pass ☐ Fail |
| M8 | VFD supports 3–5 HP motor | BU-07 | — | ☐ Pass ☐ Fail |
| M9 | HMI for control and status | BU-09 | Phase 1, 3, 6 | ☐ Pass ☐ Fail |
| M10 | Total cost ≤ $3,000 | BOM review | — | ☐ Pass ☐ Fail |
| S1 | Status/fault indicator lights | BU-10 | Phase 1, 3, 6 | ☐ Pass ☐ Fail |
| S2 | NEMA enclosure practices | Visual inspection | — | ☐ Pass ☐ Fail |
| S3 | Controls clearly labeled | Visual inspection | — | ☐ Pass ☐ Fail |

---

## Post-Test Teardown

1. Press E-stop (if not already active).
2. Switch off main AC disconnect.
3. Wait 60 seconds for VFD DC bus capacitors to discharge before opening enclosure.
4. Disconnect laptop from PLC.
5. Remove any test plastic material from input chute and output collection area.
6. Cover or secure enclosure.

---

## Test Notes / Discussion

*(Record any anomalies, deviations from expected results, or items requiring follow-up here.)*
