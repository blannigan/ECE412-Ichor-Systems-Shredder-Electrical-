# Overcurrent (Jam) Signal Wiring

This document describes how the VFD's over-current detection output is wired into the PLC so the control logic can detect a jam, run the auto-clear routine (RST + forward/reverse cycling), and lock out after three attempts within a single operator session.

## Background and Design Notes

The original design called for the VFD to fire an "over-torque alarm" relay while continuing to run, so the PLC could handle the unjam routine without the VFD itself tripping. This proved not to work on the specific Huanyang HY02D211B-T firmware revision used in this build: setting the relay to function `12` (Over-torque Detect) with `PD123 = 2` (continue running) does not actuate the relay coil at all. Only when the VFD self-trips does the relay fire.

The working configuration documented here uses the relay's **Fault Indication** function (`PD052 = 02`) combined with `PD123 = 3` (stop motor on over-torque detected). The over-torque condition triggers a `dT` fault, the VFD trips, the fault relay fires, and the PLC reads the trip and runs the unjam routine. This adds the requirement that the PLC must pulse the VFD's `RST` input to clear the fault between retry attempts, but the end-to-end behavior is functionally equivalent to the original design.

## VFD Relay Terminals (FA, FB, FC)

The VFD exposes three terminals for one internal SPDT relay:

| Terminal | Role | Behavior | Used? |
|---|---|---|---|
| **FA** | **F**orm **A** contact, Normally Open (NO) | Open when idle, closes when the relay energizes | **Yes — wired to +24V through fuse** |
| FB | **F**orm **B** contact, Normally Closed (NC) | Closed when idle, opens when the relay energizes | No — left empty |
| **FC** | **F**orm **C** common, the shared armature pole | Always one end of the circuit; the other end is FA or FB | **Yes — wired to PLC X5** |

Definitions:
- *Form A* = SPST normally open contact
- *Form B* = SPST normally closed contact
- *Form C* = SPDT changeover contact (NO + NC + common in one device — this is the kind the VFD has)

We use the **NO contact pair (FC + FA)** so the PLC sees an active-high signal when the VFD trips on a fault. PLC ladder logic reads `[ X5 ]` directly (no inversion needed) to detect a jam.

The NC alternative (FC + FB, fail-safe) was considered but not chosen for this build. NC wiring would require a 5-second startup mask in the ladder logic to prevent boot-time false trips, and the current setup uses redundant safety paths (hardwired E-stop loop, motor contactor) that handle wire-break failures at the safety-circuit level rather than depending on the jam signal.

## VFD Digital Input Mode (Sinking / NPN)

The VFD's digital control inputs (FOR, REV, RST) are configured for **sinking (NPN) input mode**. This means the VFD has internal pull-ups on these inputs, and they activate when the input is externally pulled down to DCM (0V). The PLC's D2-08TR relay output module (with relay common wired to PSU `-V`) drives these inputs by closing a relay contact that completes the path from the input pin to DCM.

This is opposite of the sourcing (PNP) topology where the PLC would push +24V to activate the inputs. Both topologies are valid; the choice depends on the output module type. For the D2-08TR with common on `-V`, sinking input mode is the correct match.

## Fuse Sizing (500 mA, Fast-Blow)

A 500 mA fast-blow fuse is installed in series with the +24V wire feeding the VFD's FA terminal.

The NEC 125% rule (Article 430) applies to motor branch circuits; for low-current signal circuits like this one, the fuse is sized to satisfy three constraints:

1. **Well above normal load to avoid nuisance trips.** The D2-08ND3 input draws ~8.5 mA at 24V. A 500 mA fuse provides ~60× headroom.
2. **Well below the lowest-rated downstream component.** The VFD relay contact is rated 3 A @ 250 VAC; signal wire (18 AWG) is rated ~10 A. A 500 mA fuse will open long before either is stressed.
3. **A commonly stocked standard size.** 500 mA fast-blow is a standard 5×20 mm glass fuse value.

Fast-blow (F) type is correct here. Slow-blow (T) is for inrush loads (motors, capacitive supplies); this is a steady-state signal circuit.

Suggested part numbers:
- Bussmann GMA-500mA (fast-blow, 5×20 mm)
- Littelfuse 0217.500MXP (fast-blow, 5×20 mm)

## D2-08ND3 Input Module Connection

The jam signal lands on input **X5** of the D2-08ND3 discrete input module (Slot 2).

The module is wired in **sourcing mode** (input common `C` to PSU `-V`), so each input pin reads HIGH (logic ON) when +24V is applied.

With the FA+FC (NO) wiring (+24V on FA, signal out FC to X5):
- Relay idle (no fault): FA-FC open → no +24V at X5 → **X5 = LOW** ("no jam")
- Relay energized (fault): FA-FC closed → +24V flows FA → FC → X5 → **X5 = HIGH** ("jam detected")

PLC ladder reads `[ X5 ]` to detect jam events (no inversion).

## Wire Colors and Gauge

Per **NFPA 79 §13.2**:

| NFPA 79 wire class | Color | Used for |
|---|---|---|
| AC line / load power | Black | Mains, motor leads |
| AC control circuits | Red | 120 VAC control (none used here) |
| **DC control circuits (ungrounded)** | **Blue** | **+24 VDC and all DC signal wires** |
| **DC control circuits (grounded return)** | **Blue with white stripe** | **0 VDC return / common** |
| Foreign voltage | Yellow | (none used here) |
| Equipment grounding | Green or Green/Yellow | Chassis ground |

Solid white is widely accepted in practice for DC return when Blue/W stripe is not stocked.

**Wire gauge: 18 AWG stranded with ferrules** at all terminal ends. 18 AWG is standard for control and signal wiring in industrial panels.

## Wiring Tables

### Jam Signal (VFD relay → PLC input)

| From | To | Wire color | Wire label |
|---|---|---|---|
| Mean Well +V (PSU) | 500 mA fast-blow fuse (input side) | Blue | `+24V` |
| 500 mA fuse (output side) | VFD `FA` terminal | Blue | `+24V-JAM` |
| VFD `FC` terminal | PLC `X5` (D2-08ND3 Slot 2) | Blue | `JAM` |
| Mean Well -V (PSU) | PLC `C` (D2-08ND3 input common) | Blue/W stripe (or White) | `0V-COM` |

### VFD Digital Control (PLC outputs → VFD inputs)

The PLC's D2-08TR relay output module drives the VFD's control inputs in sinking mode. The relay module's common (`C` terminal) is wired to PSU `-V`, so each Y output sinks to 0V when its relay closes.

| From | To | Wire label | Function |
|---|---|---|---|
| PLC Y7 (D2-08TR) | VFD `FOR` | `FOR` | Forward run command |
| PLC Y6 (D2-08TR) | VFD `REV` | `REV` | Reverse run command |
| PLC Y5 (D2-08TR) | VFD `RST` | `RST` | Fault reset pulse |
| PSU -V | D2-08TR relay common AND VFD `DCM` | `0V-CTRL` | Shared 0V reference for sinking inputs |

When a Y output is energized, its relay closes and pulls the corresponding VFD input to DCM (0V), activating the input via the VFD's internal pull-up to its own +24V rail.

## Required VFD Parameter Settings

These must be programmed via the VFD keypad. Power-cycle the VFD after changing values if they don't appear to take effect immediately.

| Code | Value | Meaning |
|---|---|---|
| `PD052` | `02` | FA-FB-FC relay function = Fault Indication (relay closes on any VFD fault). Note: `12` (Over-torque Detect) was tested and does not actuate the relay on this firmware revision when `PD123 = 2`. |
| `PD123` | `3` | Over-torque detect mode = detect during running, stop on detect. This triggers a `dT` fault when over-torque is detected, which fires the fault relay configured by `PD052 = 02`. |
| `PD124` | `150` | Over-torque level = 150% of motor rated current. With `PD142 = 7.6 A`, trips at 11.4 A actual. Tune lower if real jams are missed, higher if hard cuts cause nuisance trips. |
| `PD125` | `3.0` | Over-torque detect time = 3.0 seconds. Motor must draw current above `PD124` threshold continuously for 3.0 seconds before the VFD trips. |
| `PD155` | `0` | Auto-restart attempts = 0 (disabled). The PLC handles all restart logic to maintain the 3-strike lockout. Do not enable VFD auto-restart for safety reasons (NFPA 79 §7.5). |

Motor parameters (`PD141`–`PD144`) must also be programmed per the motor nameplate. See [`VFD/Motor_Nameplate.md`](../VFD/Motor_Nameplate.md).

To program: press `PRGM` to enter programming mode, navigate with arrows, press `SET` to edit, change value, press `SET` to save. Press `PRGM` twice to exit.

## Guaranteed Trip Verification

First-pass test to confirm the VFD trip mechanism and the relay-to-PLC signal chain work end-to-end. The aggressive threshold guarantees the VFD will trip on any motor activity.

### Test parameter values

| Code | Production value | Guaranteed-trip test value |
|---|---|---|
| `PD052` | `02` | `02` (no change) |
| `PD123` | `3` | `3` (no change) |
| `PD124` | `150` | `5` (5% × 7.6 A = 0.38 A trip threshold) |
| `PD125` | `3.0` | `5.0` (5-second window) |

### Procedure

1. Decouple motor from any mechanical load (shaft must spin freely).
2. Program the test values and confirm each on the keypad.
3. Power up the PLC.
4. Verify idle state: with motor stopped, X5 LED should be OFF on the D2-08ND3. If it is ON at idle, the wiring is wrong (e.g., wires on FB instead of FA, or short circuit).
5. Command motor to run forward at 10–15 Hz.
6. Within ~5 seconds the VFD should trip with `dT` fault. At trip:
   - Motor stops
   - VFD display shows fault code
   - Fault relay fires → X5 LED comes ON on the D2-08ND3
7. Verify the PLC ladder logic reacts (drops Y7, starts unjam routine).
8. Press the VFD STOP button (or pulse Y5/RST) to clear the fault.
9. After fault clears, X5 LED should turn OFF again.

### What it proves

- VFD over-torque detection works
- `dT` fault triggers fault relay (PD052 = 02 functions correctly)
- FA-FC contact closes when fault occurs
- +24V reaches X5 through the wiring
- PLC reads X5 correctly
- Ladder logic responds to the rising edge of X5

### Failure-mode troubleshooting

| Symptom | Likely cause |
|---|---|
| X5 LED ON at idle (before test starts) | Wires on FB instead of FA (NC instead of NO), or short circuit between FA and FC |
| Motor runs forever, no trip | `PD124` not actually saved at low value, or VFD in latched fault state — check `PD180` for last fault |
| Motor stops with fault code but X5 LED stays OFF | Wire break between FC and PLC X5, fuse blown, or PSU -V not connected to PLC C terminal |
| Motor stops but display shows fault other than `dT` (e.g., `OC-1`, `OC-2`) | Hardware overcurrent triggered before over-torque firmware timer — raise `PD124` to a less aggressive value |

### Restoration after testing

| Code | Restore to |
|---|---|
| `PD124` | `150` |
| `PD125` | `3.0` |

(`PD052` and `PD123` were not changed during testing.)

## Behavior Summary

| State / Event | What Happens | What PLC Sees |
|---|---|---|
| VFD off or PLC just powered on | No +24V flowing through relay | X5 = LOW |
| Normal operation, no jam | Relay idle, FA-FC open | X5 = LOW → "system healthy" |
| Motor current rises above 11.4 A (150% of 7.6 A FLA) | VFD starts over-torque timer (3.0 s window) | X5 still LOW |
| Sustained over-current reaches 3.0 s | VFD self-trips with `dT` fault → motor stops → fault relay fires → FA-FC closes (+24V from FA flows through to FC) | X5 = HIGH → rising edge → jam counter +1 → unjam routine begins |
| PLC unjam routine | Drops Y7 (FOR), pulses Y5 (RST, 500 ms), waits, pulses Y6 (REV, 2 s), pulses Y5 again, re-engages Y7 | Y5/Y6/Y7 cycle through the recovery sequence |
| Each new over-current event | New `dT` trip, new fault relay fire | New rising edge of X5, jam counter increments |
| 3 jam events within one session | PLC latches `LOCKOUT` | Motor stops permanently, fault lamp on, operator controls disabled until manual reset |
| Deadman released >30 s continuously | Session reset timer fires | Jam counter resets to 0 |
| Motor runs cleanly for >30 s after a jam | Clean-run reset timer fires | Jam counter resets to 0 |
| Operator presses Reset button | LOCKOUT clears | Jam counter resets, normal operation resumes |
| Brake resistor missing/undersized during reversal | VFD may trip on `Ou-1` / `Ou-2` overvoltage | X5 = HIGH (fault relay fires on any fault) → PLC treats as jam |

## Related Documentation

- [Motor nameplate](../VFD/Motor_Nameplate.md) — motor specs and required VFD motor parameters
- [Brake resistor wiring](Brake_Resistor_Wiring.md) — P/Pr terminal wiring for regenerative braking
- [VFD parameter codes](VFD_PD_Codes.pdf) — full HY-series parameter manual
- [Wire color standard](../electrical/Wire_Color_Standard.md) — panel-wide NFPA 79 color conventions
