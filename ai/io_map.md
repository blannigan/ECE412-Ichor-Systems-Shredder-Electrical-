# PLC I/O Map — DirectLOGIC 205 D2-09B-1

> As-built, synced to `PLC/Point_List.xlsx` (revision adding the 6 module sheets,
> 2026-05-29 merge). That workbook is the authoritative point-by-point reference;
> this file is the human-readable summary.

## Rack Slot Layout
| Slot | Module | Type | Points |
|---|---|---|---|
| L / N / G | — | 120 VAC service: L via EURO S10H-5H **1 A fast-blow** (PLC branch); N to neutral bus; G to ground bus | — |
| 1 | H2-DM1E | CPU / Ethernet | — |
| 2 | D2-08ND3 | 8-ch DI (24VDC, sourcing) | X0–X7 |
| 3 | F2-08AD-1 | 8-ch analog **current** input (4–20 mA) | CH1–CH8 |
| 4 | F2-04RTD | 4-ch RTD input | CH1–CH4 |
| 5 | D2-08TR | 8-ch **relay** output (dry contact, sinking, common to PSU −V) | Y0–Y7 |
| 6 | F2-08DA-2 | 8-ch analog **voltage** output (0–10 V) | +V1–+V8 |
| 7–9 | D2-Fill | Fill panels (reserved) | — |

Slot changes from the earlier design: Slot 3 F2-06AD-1 → **F2-08AD-1**, Slot 5
D2-08TD2 → **D2-08TR** (relay), Slot 6 F2-02DAS-2 → **F2-08DA-2**.

## CPU & HMI Communications (H2-DM1E, Slot 1)
The HMI is not an I/O point but is part of the point list (see the **HMI
(EA1-T4CL)** sheet and the CPU sheet's HMI row in `PLC/Point_List.xlsx`).

| Link | From | To | Notes |
|---|---|---|---|
| Operator interface | H2-DM1E CPU **serial COM port** | EA1-T4CL 4" C-More Micro-Graphic HMI COM port | Serial link. Carries operator commands to the PLC and status/data back to the panel. Match baud, parity, and stop bits on both ends. |
| HMI power | Mean Well NDR-480-24 (+V / −V) | HMI +VDC / 0VDC | Panel runs on the shared 24 VDC supply (replaces the former Rhino PSB12-030-P); 0V is the system DC common. |

## Discrete Inputs (D2-08ND3, Slot 2)

Module wired in sourcing mode. Input common (C) tied to PSU −V. Each X input reads
HIGH when +24V is applied through its source device. Shared +24V to the pushbuttons
comes from PSU +V through a **1 A fast-blow** fuse into the EURO S4LH distribution
terminal, which feeds X0/X1/X2/X3 (and X6 when wired). See
`electrical/Operator_Controls.md` for pushbutton part numbers.

| Address | Field Device | Source | Notes |
|---|---|---|---|
| X0 | **Forward pushbutton** | Autonics S2PR-P3G (green) + SA-CA NO contact + SA-LDG LED | +24V → NO contact → X0 |
| X1 | **Reverse pushbutton** | Autonics S2PR-P3Y (yellow) + SA-CA + SA-LDY | Same topology as X0 |
| X2 | **Run 1 / Deadman 1** | Autonics S2PR-P3B (blue) + SA-CA + SA-LDB | Same topology as X0 |
| X3 | **Run 2 / Deadman 2** | Autonics S2PR-P3B (blue) + SA-CA + SA-LDB | Same topology as X0 (confirmed against panel) |
| X4 | **E-stop button** (NC, monitored tap) | Cutler-Hammer / Eaton **E22B1** mushroom E-stop, NC contact | Wired in series with SD-N35 contactor coil A1. X4 taps the +24V line between the E-stop NC contact and A1. HIGH when E-stop is closed (coil energized, motor power available); LOW when E-stop is pressed (coil dropped, motor power removed). Fail-safe: any wire break or PSU failure in this chain reads LOW. A2 of the contactor returns directly to PSU −V. |
| X5 | **VFD fault relay** (FA + FC, NO active-high) | VFD internal SPDT relay (FA/FC/FB) programmed as fault indication via **PD052=02**. PSU +V → VFD FA; VFD FC → PLC X5. FB unused. | HIGH when VFD trips on any fault (over-torque, OV, UV, OH). When the relay closes, +24V on FA bridges to FC and reaches X5. |
| X6 | **Reserved — Reset pushbutton (planned)** | Autonics S2PR-P3R (red) + SA-CA + SA-LDR (red LED) | Currently unwired. Planned to receive the red illuminated pushbutton from the URS invoice. When pressed, the ladder will detect the rising edge of X6 and pulse Y5 to drive the VFD RST terminal (clearing any latched fault). Same +24V / 1 A fuse topology as X0–X3. |
| X7 | Spare | — | Currently unwired. Available for future expansion. |

Note: +24V to all buttons is shared through a single 1 A fast-blow fuse on the
EURO S4LH terminal block. If any button's circuit shorts, the fuse pops and all
buttons stop working (good diagnostic — all-buttons-dead = check that fuse first).

## Discrete / Relay Outputs (D2-08TR, Slot 5)

Relay (dry-contact) module wired in **sinking** mode: relay common (C) → PSU −V.
Each load's (+) sits on PSU +V; when a Y relay closes, it sinks that load's (−) to
−V, energizing it.

| Address | Load | Notes |
|---|---|---|
| Y0 | **Forward indicator LED** — SA-LDG (green) in S2PR-P3G | Lights green when forward selected (assembly also drives X0) |
| Y1 | **Reverse indicator LED** — SA-LDY (yellow) in S2PR-P3Y | Drives X1 assembly's LED |
| Y2 | **Run 1 / Deadman 1 LED** — SA-LDB (blue) | Drives X2 assembly's LED |
| Y3 | **Run 2 / Deadman 2 LED** — SA-LDB (blue) | Drives X3 assembly's LED |
| Y4 | **Error / fault indicator** — Wamco model 525 panel LED (28 VDC, 0.6 W) | 28V-rated indicator slightly under-driven at 24V (~21 mA, acceptable) |
| Y5 | **VFD RST** terminal | Fault-reset pulse (~500 ms) during the PLC unjam routine. Closing Y5 pulls RST to DCM (0V). |
| Y6 | **VFD FOR** terminal | Forward run command. Closing Y6 pulls FOR to DCM. |
| Y7 | **VFD REV** terminal | Reverse run command (used during unjam). Closing Y7 pulls REV to DCM. |

VFD FOR/REV/RST inputs are configured sinking (NPN). PSU −V is shared between the
D2-08TR relay common and VFD DCM (common 0V reference).

> **Changed from the previous design:** the SD-N35 contactor coil is no longer a
> PLC output (it used to be driven by D2-08TD2 Y0). As-built, the coil sits in the
> hardwired E-stop safety chain (see X4 and Power Distribution below). Also, FOR and
> REV swapped relays — as-built FOR = Y6, REV = Y7 (previously Y7/Y6).

## Analog Input (F2-08AD-1, Slot 3)
| Channel | Source | Signal |
|---|---|---|
| CH1+ | VFD **VO** terminal (configured via **PD054=1**) | 0–10 V proportional to motor output current — **motor current monitor** |
| CH2–CH8 | Spare | Unwired |

Module power: +24V/0V direct to PSU +V/−V (no fuse on the module-power branch).
Signal return shares PSU −V (VFD ACM also tied to −V).

## Analog Output (F2-08DA-2, Slot 6)
| Channel | Destination | Signal |
|---|---|---|
| +V1 | VFD **VI** terminal (requires **PD002=1**) | 0–10 V speed/frequency reference (0 V = 0 Hz, 10 V = max frequency) |
| +V2–+V8 | Spare | Unwired |

Single 0V terminal serves as both module-power return and analog signal reference
for all channels; shared with VFD ACM at PSU −V.

## RTD Input (F2-04RTD, Slot 4)
Module is installed and powered (+24V/0V to PSU +V/−V), but all four channels
(CH1–CH4) are **spare / unwired** in this build. Reserved for future RTD
temperature sensing.

## VFD — Huanyang HY02D211B-T (power + control terminals)

### Power terminals
| Terminal | Connection | Notes |
|---|---|---|
| R | AC hot via main disconnect + 30 A C-curve DIN-rail breaker | Black wire per NFPA 79 |
| T | AC neutral via Phoenix Contact **TMC 8 3C 15A** breaker (P/N 2907618) → SD-N35 contactor pole → VFD T | **AS-BUILT DEVIATION:** the *neutral* leg is switched by the contactor. NFPA 79 / NEC practice is to switch the **hot** leg. Flagged for final-report review. Pressing E-stop drops the SD-N35 coil → contact opens → VFD T loses neutral → VFD shuts down. |
| U / V / W | Motor phases via colored 4 mm banana sockets (U=blue, V=white, W=red) → GE **5KE182BC205B** motor T1/T2/T3 | Panel-mount quick-disconnect |
| P+ / PR | Brake resistor ATO **APCS-300R30-AD** (300 W, 30 Ω) | Dynamic braking |
| Ground | Panel ground bus | Green / green-yellow wire |

### Control terminals (programmed / wired)
| Terminal | To / From | Notes |
|---|---|---|
| VI | F2-08DA-2 +V1 | 0–10 V commanded-frequency reference (PD002=1) |
| VO | F2-08AD-1 CH1+ | 0–10 V motor-current monitor out (PD054=1) |
| FOR / REV / RST | D2-08TR Y6 / Y7 / Y5 | Sinking inputs, pulled to DCM when the relay closes |
| FA / FC | PSU +V / PLC X5 | Fault relay (PD052=02); FA-FC closes on any trip → +24V to X5. FB unused. |
| DCM / ACM | PSU −V | Shared digital / analog 0V reference |
| 10V, 5V, AI, SPH, SPM, SPL, UPF, DRV, RS± | Unused | Unwired (Modbus and multi-speed presets not used) |

## Power Distribution Summary
| Source | Destination | Protection |
|---|---|---|
| Wall AC line | EURO S10H-5H fuse block | 25 A slow-blow (PSU branch), 1 A fast-blow (PLC branch) |
| NDR-480-24 +V | Pushbutton commons (Forward, Reverse, Run 1/2, Reset) | 1 A fast-blow via EURO S4LH |
| NDR-480-24 +V | E22B1 E-stop NC → SD-N35 coil A1 | Direct (no fuse); X4 taps this line |
| NDR-480-24 +V | VFD FA (jam signal), indicator LED (+) commons, analog module power | Direct (no fuse) |
| NDR-480-24 −V | SD-N35 coil A2, D2-08ND3 C, D2-08TR C, analog/RTD module 0V, VFD DCM/ACM | Direct return |
| Wall AC (via power switch) | PLC L terminal | 1 A fast-blow |
| Wall AC (via power switch) | PSU L terminal | 25 A slow-blow |

**Motor disconnect / E-stop chain (as-built):** PSU +V → E22B1 NC → SD-N35 coil
A1; A2 → PSU −V. With E-stop released the coil is energized, closing the contactor
pole that feeds the VFD T (neutral) leg. Pressing E-stop drops the coil and removes
VFD power. PLC X4 monitors the A1 node for state.

## Conductor Sizing & Overcurrent Protection
- **Power conductors:** 12 AWG copper (THHN/MTW). Rated ampacity per NEC Table
  310.16: **20 A at 60 °C, 25 A at 75 °C, 30 A at 90 °C** column. Used for the VFD
  branch and other power-carrying runs; comfortably above the GE motor's 7.6 A FLA
  and the VFD input current.
- **Control conductors:** smaller-gauge (typ. 16–18 AWG) for the 24 VDC discrete
  and analog signal wiring; ferruled at all terminal blocks.
- **Fuse / OCPD sizing convention:** branch and component fuses are sized at
  **125 % of the protected component's rated (continuous) load current**, per NEC
  210.20(A) / 215.3 for continuous loads. Examples: the PSU branch and pushbutton
  commons are fused above their steady-state draw, and downstream control loads are
  individually fused at terminal blocks.
- **Motor-branch exception:** the VFD branch-circuit short-circuit / ground-fault
  device (the 30 A C-curve breaker) follows NEC 430.52, which permits a higher
  multiple of FLC than 125 % so the breaker can ride through VFD/VFD inrush
  without nuisance tripping. Running-overload protection (the 115–125 % rule) is
  handled separately by the VFD's electronic motor-overload function.

## Legacy / superseded sheets
The workbook still carries two sheets from an earlier design iteration that are
**not part of the as-built 9-slot rack** above; they are retained for history only:
- **Output Module (D2-08TA)** — AC relay scheme driving TX / BUS / F1 GH15-BN
  contactors and an RTD32-180 thermal overload. Superseded by the single SD-N35
  contactor + Phoenix Contact breaker arrangement.
- **Output Module (F2-02DAS-2)** — 2-ch analog output to a GS1-20P2 VFD AL terminal.
  Superseded by F2-08DA-2 (Slot 6) → Huanyang VFD VI terminal.
