# Overcurrent (Jam) Signal Wiring

This document describes how the VFD's over-torque detection output is wired into the PLC so the control logic can detect a jam, run the auto-clear routine (forward/reverse cycling), and lock out after three attempts within a single operator session.

## Overview

The Huanyang HY-series VFD has a single internal SPDT relay on its control terminal block (terminals FA, FB, FC). This relay is programmed via parameter `PD052 = 12` to fire on over-torque detection, meaning the relay closes when motor output current exceeds the configured threshold for the configured time.

When the relay closes, +24V is delivered through the NO contact into input X5 of the PLC's discrete input module (D2-08ND3). The PLC ladder logic reads this as a jam event and initiates the auto-clear sequence (forward/reverse cycling, three-strike lockout).

## VFD Relay Terminals (FA, FB, FC)

The VFD exposes three terminals for one internal SPDT relay. The labels come from standard relay-contact terminology:

| Terminal | Role | Behavior |
|---|---|---|
| **FA** | **F**orm **A** contact, Normally Open (NO) | Open when idle, closes when the relay energizes |
| **FB** | **F**orm **B** contact, Normally Closed (NC) | Closed when idle, opens when the relay energizes |
| **FC** | **F**orm **C** common, the shared armature pole | Always one end of the circuit; the other end is FA or FB |

Definitions:
- *Form A* = SPST normally open contact (one pair, opens and closes)
- *Form B* = SPST normally closed contact (one pair, opens and closes)
- *Form C* = SPDT changeover contact (NO + NC + common in one device — this is the kind the VFD has)

The relay is physically one switch inside the VFD. To use it, pick a pair of terminals:

- **FC + FA** for active-high behavior (closes on trigger)
- **FC + FB** for active-low / fail-safe behavior (opens on trigger)

For the jam signal we use **FC + FA (NO pair)**. This delivers +24V to the PLC only during an over-torque event, giving an active-high signal that matches the PLC ladder convention (`[ X5 ]` reads true when jammed, no logical inversion required).

The NC pair (FC + FB) is reserved by industrial convention for safety signals where a broken wire must trip the system (E-stop chains, guard interlocks, hard-fault outputs). Jam detection is a process feature, not a safety function — the VFD's own self-protection trip (at full `PD125` time) provides the safety backup, so fail-safe wiring is not required for this signal.

## Fuse Sizing (500 mA, Fast-Blow)

A 500 mA fast-blow fuse is installed in series with the +24V wire feeding the VFD's FA terminal.

The NEC 125% rule (Article 430) is the standard for sizing overcurrent protection on motor branch circuits: the protective device is rated at 125% of full-load current. That rule does not map directly to low-current signal circuits like this one. 125% of the ~8.5 mA input current would be roughly 10 mA, which is not a standard fuse size. Instead, signal-circuit fuses are sized to satisfy three constraints:

1. **Well above normal load to avoid nuisance trips.** The D2-08ND3 input draws ~8.5 mA at 24V. A 500 mA fuse provides ~60× headroom over normal current.
2. **Well below the lowest-rated downstream component.** The VFD's internal relay contact is rated 3 A @ 250 VAC; signal wire (18 AWG) is rated ~10 A. A 500 mA fuse will open long before either is stressed.
3. **A commonly stocked standard size** so replacement is easy. 500 mA fast-blow is a standard 5×20 mm glass fuse value.

Fast-blow (F) type is correct for this circuit. Slow-blow (T) is intended for loads with inrush current (motors, capacitive power supplies); this is a steady-state signal circuit with no inrush.

Suggested part numbers:
- Bussmann GMA-500mA (fast-blow, 5×20 mm)
- Littelfuse 0217.500MXP (fast-blow, 5×20 mm)
- Any 5×20 mm 500 mA fast-blow fuse rated ≥ 24 VDC (250 VAC ratings are acceptable)

## D2-08ND3 Input Module Connection

The jam signal lands on input **X5** of the D2-08ND3 discrete input module.

The module is wired in **sourcing mode**: the input common (`C` terminal) is connected to the 0V rail. In this configuration, each input pin reads ON (logic high) when +24V is applied to it.

Sourcing mode is the conventional configuration for dry-contact field devices like this. With the module in sourcing mode and the jam signal wired through FC + FA, the PLC ladder reads the input as `[ X5 ]` = true when jammed, with no inversion required.

The D2-08ND3 has a single common shared by all 8 inputs, so the sourcing/sinking choice applies to the entire module. All other field devices on this module (E-stop, two-hand start buttons, lid interlock, reset) should also be wired in sourcing mode for consistency.

## Wire Colors and Gauge

Per **NFPA 79 §13.2** (Electrical Standard for Industrial Machinery), control wiring uses the following color code:

| NFPA 79 wire class | Color | Used for |
|---|---|---|
| AC line / load power | Black | Mains, motor leads |
| AC control circuits | Red | 120 VAC control |
| **DC control circuits (ungrounded)** | **Blue** | **+24 VDC and all DC signal wires** |
| **DC control circuits (grounded return)** | **Blue with white stripe** | **0 VDC return / common** |
| Foreign voltage (from outside disconnect) | Yellow | Interlocks from external sources |
| Equipment grounding | Green or Green/Yellow | Chassis ground |

Solid **white** is widely accepted in practice for DC return when Blue/White stripe is not stocked, though Blue/White stripe is the strict NFPA 79 callout.

**Wire gauge: 18 AWG stranded with ferrules** on all terminal ends. 18 AWG is standard for control and signal wiring in industrial panels — handles ~10 A continuous (well above the 8.5 mA signal current), has enough mechanical strength to resist breakage at terminal blocks, and is the default size most panel-builder stock.

## Wiring Table

| From | To | Wire color | Wire label |
|---|---|---|---|
| +24V DC supply | 500 mA fast-blow fuse (input side) | Blue | `+24V` |
| 500 mA fuse (output side) | VFD `FA` terminal | Blue | `+24V-JAM` |
| VFD `FC` terminal | PLC `X5` input on D2-08ND3 | Blue | `JAM` |
| 0V DC supply | PLC `C` (input common on D2-08ND3) | Blue/White stripe (or solid White) | `0V-COM` |

All four wires are 18 AWG stranded with crimped ferrules at each terminal. Each wire is labeled at both ends with the wire label shown above (heat-shrink markers or printed wire labels). Since all four signal-side wires are the same color (Blue), the labels are the primary means of identification — do not rely on color alone.

## Required VFD Parameter Settings

These must be programmed via the VFD keypad before the jam signal will function. Without these, the relay defaults to fault indication and will not fire on over-torque events.

| Code | Original value | New value | Meaning |
|---|---|---|---|
| `PD052` | `02` | `12` | FA-FB-FC relay function. Original `02` = fault indication (relay closes on any VFD fault). New `12` = over-torque detect (relay closes when motor current exceeds threshold) |
| `PD123` | `0` | `0` | Over-torque detect mode. No change. `0` = detect only after reaching set frequency, which masks startup inrush so normal motor ramp-up does not false-trigger |
| `PD124` | `0` | `150` | Over-torque level. Original `0` = detection disabled. New `150` = trigger at 150% of motor rated current. Tune empirically: lower if real jams are missed, higher if hard cuts cause nuisance triggers |
| `PD125` | `2.0` | `3.0` | Over-torque detect time. Increased from 2.0 s to 3.0 s to give the PLC ladder a longer reaction window. Relay closes at half-time (1.5 s); VFD self-trips at full time (3.0 s) as a safety backup |

To program: press `PRG/ESC` to enter programming mode, navigate to each parameter, press `ENT` to edit, change the value, press `ENT` to save. Press `PRG/ESC` twice to exit.

## Behavior Summary

- Motor current below 150% rated → relay open → X5 = LOW → no PLC action
- Motor current rises above 150% → VFD watches the current for 1.5 s (half of `PD125`)
- Sustained over-current at 1.5 s → relay closes → +24V applied to X5 → PLC ladder sees rising edge → jam counter increments → unjam routine begins
- PLC drops FOR output, waits briefly, pulses REV for ~2 s, returns to FOR
- Each new over-current event (rising edge of X5) increments the counter
- After 3 jam events within one operator session (deadman switches held continuously, or with releases shorter than 30 s), PLC latches `LOCKOUT`, stops the motor, lights the fault lamp, and disables the operator controls until a manual reset
- If the deadman switches are released for more than 30 s continuously, the jam counter resets to 0 (fresh session)
- If the PLC fails to react and over-current persists past 3.0 s (full `PD125`) → VFD self-trips on its own → motor stops as an independent safety backup
