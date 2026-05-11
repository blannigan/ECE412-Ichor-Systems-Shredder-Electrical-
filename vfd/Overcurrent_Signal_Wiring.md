# Overcurrent (Jam) Signal Wiring

This document describes how the VFD's over-torque detection output is wired into the PLC so the control logic can detect a jam, run the auto-clear routine (forward/reverse cycling), and lock out after three attempts within a single operator session.

The wiring uses a **fail-safe NC convention**: the PLC input reads HIGH when everything is working, and LOW when a jam is detected OR when any failure occurs in the signal chain (broken wire, dead VFD, failed relay, loose terminal). The PLC reacts the same way to a real jam and to any signal-path failure — both safely stop the machine.

## Overview

The Huanyang HY-series VFD has a single internal SPDT relay on its control terminal block (terminals FA, FB, FC). This relay is programmed via parameter `PD052 = 12` to fire on over-torque detection, meaning the relay coil energizes when motor output current exceeds the configured threshold for the configured time.

We use the **NC contact pair (FB + FC)** so that:
- When the relay is idle (no fault), FB-FC is closed, +24V flows through to PLC X5 → X5 reads HIGH = "healthy, no jam"
- When the relay energizes (over-torque detected), FB-FC opens, +24V is interrupted → X5 reads LOW = "jam detected"
- If any failure occurs in the signal chain (broken wire, dead VFD, etc.), X5 reads LOW = treated the same as a jam → safe state

## VFD Relay Terminals (FA, FB, FC)

The VFD exposes three terminals for one internal SPDT relay. The labels come from standard relay-contact terminology:

| Terminal | Role | Behavior | Used? |
|---|---|---|---|
| **FA** | **F**orm **A** contact, Normally Open (NO) | Open when idle, closes when the relay energizes | No — left empty |
| **FB** | **F**orm **B** contact, Normally Closed (NC) | Closed when idle, opens when the relay energizes | **Yes — +24V wire** |
| **FC** | **F**orm **C** common, the shared armature pole | Always one end of the circuit; the other end is FA or FB | **Yes — wire to PLC X5** |

Definitions:
- *Form A* = SPST normally open contact (one pair, opens and closes)
- *Form B* = SPST normally closed contact (one pair, opens and closes)
- *Form C* = SPDT changeover contact (NO + NC + common in one device — this is the kind the VFD has)

The relay is physically one switch inside the VFD. To use it, pick a pair of terminals:

- **FC + FA** for active-high behavior (closes on trigger): X5 LOW at idle, HIGH on event. *Not used here.*
- **FC + FB** for active-low / fail-safe behavior (opens on trigger): X5 HIGH at idle, LOW on event. **Used in this design.**

## Why Fail-Safe NC Instead of Active-High NO

Industry convention (NFPA 79 §13.2 for industrial machinery) reserves NC fail-safe wiring for signals where missing the event would create a hazard. For a shredder jam-detection signal, fail-safe is appropriate because:

1. **A missed jam is dangerous.** Without jam detection, the motor will continue applying torque against a blocked blade, potentially damaging the mechanism, shearing pins, or burning out the motor windings before the VFD's own protections engage.
2. **A false jam from a broken wire is only an inconvenience.** It causes a nuisance lockout that requires a maintenance reset. The operator can investigate and find the wiring fault.
3. **The cost of NC wiring is zero.** Same number of wires, same VFD relay, just one different terminal screw.

Failure modes that all drive the system to a safe state with NC wiring:

| Failure | What PLC sees | Result |
|---|---|---|
| Real over-torque jam | X5 LOW | Unjam routine, eventually lockout |
| Wire breaks anywhere | X5 LOW | Same — lockout, operator investigates |
| Loose terminal screw | X5 LOW | Same |
| VFD loses power | X5 LOW | Same |
| VFD relay coil burns out | X5 LOW | Same |
| 24V supply drops | X5 LOW | Same |

The trade-off is that any signal-path failure causes a nuisance lockout. That is the correct behavior — better to nuisance-lockout from a broken wire than miss a real jam.

## Fuse Sizing (500 mA, Fast-Blow)

A 500 mA fast-blow fuse is installed in series with the +24V wire feeding the VFD's FB terminal.

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

With this configuration and the jam signal wired through FB + FC (NC), the PLC ladder reads the input as:
- `[ X5 ]` = TRUE → +24V present at X5 → system healthy, no jam, signal path intact
- `[ NOT X5 ]` = TRUE → no +24V at X5 → jam detected OR signal path failure

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

**Wire gauge: 18 AWG stranded with ferrules** on all terminal ends. 18 AWG is standard for control and signal wiring in industrial panels — handles ~10 A continuous (well above the 8.5 mA signal current), has enough mechanical strength to resist breakage at terminal blocks, and is the default size most panel-builders stock.

## Wiring Table

| From | To | Wire color | Wire label |
|---|---|---|---|
| +24V DC supply | 500 mA fast-blow fuse (input side) | Blue | `+24V` |
| 500 mA fuse (output side) | VFD **`FB`** terminal | Blue | `+24V-JAM` |
| VFD `FC` terminal | PLC `X5` input on D2-08ND3 | Blue | `JAM` |
| 0V DC supply | PLC `C` (input common on D2-08ND3) | Blue/White stripe (or solid White) | `0V-COM` |

All four wires are 18 AWG stranded with crimped ferrules at each terminal. Each wire is labeled at both ends with the wire label shown above (heat-shrink markers or printed wire labels). Since all four signal-side wires are the same color (Blue), the labels are the primary means of identification — do not rely on color alone.

**Terminal block layout reminder.** The VFD's control terminal block bottom row reads left-to-right: `FA  FC  FB  24V  DCM ...`. FB is the **third terminal from the left**, FC is the **second** (middle). Easy to mix up — verify visually before powering on.

## Required VFD Parameter Settings

These must be programmed via the VFD keypad before the jam signal will function. Without these, the relay defaults to fault indication and will not fire on over-torque events.

| Code | Original value | New value | Meaning |
|---|---|---|---|
| `PD052` | `02` | `12` | FA-FB-FC relay function. Original `02` = fault indication (relay closes on any VFD fault). New `12` = over-torque detect (relay closes when motor current exceeds threshold) |
| `PD123` | `0` | `0` | Over-torque detect mode. No change. `0` = detect only after reaching set frequency, which masks startup inrush so normal motor ramp-up does not false-trigger |
| `PD124` | `0` | `150` | Over-torque level. Original `0` = detection disabled. New `150` = trigger at 150% of motor rated current. With `PD142 = 7.6 A`, this trips at 11.4 A actual. Tune empirically: lower if real jams are missed, higher if hard cuts cause nuisance triggers |
| `PD125` | `2.0` | `3.0` | Over-torque detect time. Increased from 2.0 s to 3.0 s to give the PLC ladder a longer reaction window. Relay closes at half-time (1.5 s); VFD self-trips at full time (3.0 s) as a safety backup |

Motor nameplate values (`PD141`–`PD144`) must also be programmed correctly so that percentage-based protections scale against actual motor current. See [Motor_Nameplate.md](../motor/Motor_Nameplate.md) for those values.

To program: press `PRGM` / `PRG/ESC` to enter programming mode, navigate to each parameter, press `ENT` / `SET` to edit, change the value, press `ENT` / `SET` to save. Press `PRGM` / `PRG/ESC` twice to exit.

## PLC Startup Mask Requirement

Because the PLC typically boots faster than the VFD (PLC ready in ~1 second, VFD takes 3-5 seconds to initialize and energize its internal relays), the PLC will momentarily see X5 LOW during boot — there is no +24V flowing yet because the VFD's NC contact has not yet engaged.

**Without a startup mask, the PLC would latch a jam lockout on every power-up.**

The ladder logic must include a startup timer that ignores the X5 state for the first ~5 seconds after the PLC begins running:

```
On first scan: start a 5-second timer (e.g., TMR T0 K50)
Jam detection rung: [ NOT T0 ] AND [ NOT X5 ] → counts as jam
                       ↑              ↑
                       │              X5 LOW (jam or fault)
                       Timer has finished (startup window over)
```

The exact syntax depends on the CPU (H2-DM1E Do-more vs DL205). The principle: the jam-detection logic should be gated behind "system has been on for at least N seconds" so VFD startup does not false-trigger.

## Bench Test Procedure

Before connecting the motor to the shredder mechanism, the jam signal path is validated end-to-end by lowering the over-torque threshold so that running the motor unloaded is enough to trigger the alarm. This verifies the VFD detection logic, the relay, the wiring to the PLC, the PLC input, and the ladder logic together.

### Test parameter values

Temporarily reprogram these via the VFD keypad. Production values are listed for restoration after testing.

| Code | Production value | Test value | Why the test value |
|---|---|---|---|
| `PD052` | `12` | `12` | No change — relay function stays as over-torque detect |
| `PD123` | `0` | `2` | Detect during running including ramp-up — removes "did motor reach commanded freq?" ambiguity during bench testing |
| `PD124` | `150` | `6` | 6% × 7.6 A = 0.46 A trip threshold. Just slightly below typical no-load magnetizing current (~0.5 A), so over-torque triggers reliably when motor runs unloaded |
| `PD125` | `3.0` | `20.0` | 20.0 s detect time (max allowed). Relay activates at 10 s; VFD self-trips at 20 s. Plenty of window to observe X5 LED change state |

### Procedure

1. **Decouple the motor from any mechanical load.** Motor shaft must be free to spin. Verify nothing is connected to the output shaft.
2. **Program the test values** above into the VFD via the keypad. Confirm each value after entering by reading it back.
3. **Power up the PLC** and confirm ladder logic is loaded and running.
4. **Verify the idle state.** With nothing happening, **X5 LED should be ON** (NC contact closed, +24V flowing). If X5 LED is OFF at idle, the wiring is broken, the VFD is not powered, or the polarity is wrong.
5. **Command motor to run forward at low frequency** (10-15 Hz).
6. **Watch the X5 LED.** After ~10 seconds (half of `PD125`), the relay should energize and open the NC contact → **X5 LED turns OFF.** This is the jam signal.
7. **Listen for an audible click from inside the VFD** at the same moment the LED drops.
8. **Hit STOP immediately** when X5 LED turns off — do not wait for the full 20 s VFD self-trip.
9. **After motor stops**, X5 LED should return to ON (relay back to idle, NC contact closed again).
10. **Verify the PLC ladder behavior:**
    - First jam: motor stops, unjam routine runs (REV pulse, return to FOR)
    - Second jam: same as first, jam counter increments
    - Third jam: lockout latches, motor stops permanently, fault lamp on, operator controls disabled
    - Releasing deadman for >30 s resets the jam counter
11. **Restore production values when testing is complete** (see table below).

### Restoration after testing

| Code | Restore to |
|---|---|
| `PD123` | `0` |
| `PD124` | `150` |
| `PD125` | `3.0` |

(`PD052` was not changed during testing.)

### Safety notes

- **Run at low frequency only** (10-15 Hz). Full motor torque is available even at low speed, but shaft RPM is slow enough to react if needed.
- **Keep the E-stop within reach throughout the test.** If shaft behavior becomes unexpected, hit E-stop immediately.
- **The VFD will self-trip at full `PD125` time** (20.0 s during testing, 3.0 s in production) regardless of what the PLC does. This is the independent safety backup — do not disable it by setting `PD125 = 0`.
- **Do not skip the restore step.** Leaving test values in production will cause the shredder to false-trigger on the first piece of plastic.

## Behavior Summary

| State / Event | What Happens | What PLC Sees / Does |
|---|---|---|
| VFD off, OR PLC just powered on (within ~5 s startup mask) | No +24V flowing through relay yet | X5 = LOW, but startup mask suppresses jam detection |
| Normal operation, no jam | Relay idle, FB-FC closed, +24V flows to X5 | **X5 = HIGH** → "system healthy" |
| Motor current rises above 150% rated (`PD124 × PD142` = 11.4 A actual) | VFD starts over-torque timer (`PD125` = 3.0 s window) | X5 still HIGH (relay not yet fired) |
| Sustained over-current reaches 1.5 s (half of `PD125`) | Relay coil energizes, FB-FC opens, +24V interrupted | **X5 = LOW** → falling edge detected → jam counter +1 → unjam routine starts |
| Unjam routine running | PLC drops FOR output, waits, pulses REV for ~2 s, returns to FOR | Motor stops, reverses, resumes forward |
| Each new over-current event | New falling edge of X5 | Jam counter increments by 1 |
| 3 jam events within one session | PLC latches `LOCKOUT` | Motor stops permanently, fault lamp on, operator controls disabled until manual reset |
| Deadman released >30 s continuously | Session reset timer fires | Jam counter resets to 0 (fresh session) |
| Over-current persists past 3.0 s (full `PD125`) | VFD self-protects, motor stops, `dT` fault displayed | Independent safety backup (PLC may or may not have acted first) |
| Wire break, dead VFD, failed relay coil, loose terminal | +24V no longer reaches X5 | X5 = LOW → treated as jam → eventually lockout → operator investigates |
