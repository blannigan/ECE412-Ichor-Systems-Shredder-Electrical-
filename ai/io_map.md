# PLC I/O Map — DirectLOGIC 205 D2-09B-1

## Rack Slot Layout
| Slot | Module | Type | Points |
|---|---|---|---|
| 1 | H2-DM1E | CPU / Ethernet | — |
| 2 | D2-08ND3 | 8-ch DI (24VDC) | X0–X7 |
| 3 | F2-06AD-1 | 6-ch AI (4–20mA / 0–10V) | — |
| 4 | F2-04RTD | 4-ch RTD input | — |
| 5 | D2-08TD2 | 8-ch DO (12–24VDC sourcing) | Y0–Y7 |
| 6 | F2-02DAS-2 | 2-ch AO (4–20mA / 0–10V) | — |
| 7–9 | D2-Fill | Reserved | — |

## Discrete Inputs (D2-08ND3, Slot 2)

Module wired in sourcing mode. Input common (C) tied to PSU -V. Each X input reads HIGH when +24V is applied through its source device. See `electrical/Operator_Controls.md` for pushbutton part numbers.

| Address | Field Device | Source | Notes |
|---|---|---|---|
| X0 | **Forward pushbutton** | Autonics S2PR-P3G (green) + SA-CA NO contact + SA-LDG LED | +24V through 1A fuse (EURO S4LH) → NO contact → X0 |
| X1 | **Reverse pushbutton** | Autonics S2PR-P3Y (yellow) + SA-CA + SA-LDY | Same topology as X0 |
| X2 | **Deadman 1** | Autonics S2PR-P3B (blue) + SA-CA + SA-LDB | Same topology as X0 |
| X3 | Deadman 2 (likely) | Autonics S2PR-P3B (blue) + SA-CA + SA-LDB | TBD — confirm against panel |
| X4 | **E-stop button** (NC, monitored tap) | Cutler-Hammer / Eaton **E22B1** mushroom E-stop, NC contact | Wired in series with SD-N35 contactor coil A1. X4 taps the +24V line between the E-stop NC contact and A1. HIGH when E-stop is closed (coil energized, motor power available); LOW when E-stop is pressed (coil dropped, motor power removed). Fail-safe: any wire break or PSU failure in this chain reads LOW. A2 of the contactor returns directly to PSU -V. |
| X5 | **VFD fault relay** (FA + FC, NO active-high) | +24V from PSU through 500 mA fuse → VFD FA terminal. VFD FC terminal → PLC X5 directly. | HIGH when VFD trips on any fault (over-torque, OV, UV, OH). When relay closes, +24V on FA bridges to FC and reaches X5. See `vfd/Overcurrent_Signal_Wiring.md`. |
| X6 | **Reserved — Reset pushbutton (operator input, planned)** | Autonics S2PR-P3R (red) + SA-CA + SA-LDR (red LED) | Currently unwired. Planned to receive the red illuminated pushbutton from the URS invoice. When pressed, PLC ladder will detect rising edge of X6 and pulse Y5 to drive the VFD's RST terminal (clearing any latched VFD fault). Same +24V/1A fuse topology as X0-X3. |
| X7 | Unused / spare | — | Currently unwired. Available for future expansion. |

Note: +24V to all four buttons is shared through a single 1 A fast-blow fuse on the EURO S4LH terminal block. If any button's circuit shorts, the fuse pops and all four buttons stop working (good diagnostic — all-buttons-dead = check that fuse first).

## Discrete Outputs (D2-08TD2, Slot 5)
| Address | Load | Notes |
|---|---|---|
| Y0 | Mitsubishi SD-N35 Contactor coil A1 | +24VDC via DF103V 1/2A fuse |

## VFD Digital Control Outputs (D2-08TR relay module, common to PSU −V)
| Address | Load | Notes |
|---|---|---|
| Y5 | VFD `RST` terminal | Fault reset pulse (~500 ms during PLC unjam routine). Sinking output pulls RST to DCM (0V) when active. |
| Y6 | VFD `REV` terminal | Reverse run command. Sinking output. |
| Y7 | VFD `FOR` terminal | Forward run command. Sinking output. |

VFD digital inputs (FOR, REV, RST) configured in sinking (NPN) input mode. PSU −V connects to D2-08TR relay common AND VFD DCM (shared 0V reference). See `vfd/Overcurrent_Signal_Wiring.md`.

## Analog Output (F2-02DAS-2, Slot 6)
| Channel | Destination | Signal |
|---|---|---|
| CH1 | VFD HY02D211B-T terminal AL | 0–10V speed command via ZipLink ZL-RTB20 |

## Output Module — AC Relay (D2-08TA, separate)
| Address | Load | Notes |
|---|---|---|
| OUT0 | TX Contactor (GH15-BN) coil A1 | Via ZipLink, 120VAC common fused 1A slow blow |
| OUT1 | BUS Contactor (GH15-BN) coil A1 | Via ZipLink |
| OUT2 | F1 Contactor (GH15-BN) coil A1 | Via ZipLink |
| OUT3 | Thermal Overload RTD32-180 NC (95→96) | Feeds F2 contactor coil |

## Power Distribution Summary
| Source | Destination | Protection |
|---|---|---|
| Wall AC Line | EURO S10H-5H fuse block | 25A (PSU branch), 1A (PLC branch) |
| NDR-480-24 +V | Pushbutton commons (Forward, Reverse, Deadman 1, Deadman 2, Reset) | 1 A fast blow via EURO S4LH |
| NDR-480-24 –V | Contactor A2, D2-08TD2 COM, D2-08ND3 COM, D2-04RTD COM | Direct return |
| Wall AC (via power switch) | PLC L terminal | 1A fast blow |
| Wall AC (via power switch) | PSU L terminal | 25A slow blow |
