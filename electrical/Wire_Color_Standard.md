# Wire Color Standard

Wire color convention used throughout the Universal Plastic Shredder V2.0 electrical panel. Per **NFPA 79 §13.2** (Electrical Standard for Industrial Machinery).

## Color Code

| Wire Class | Color | Used for |
|---|---|---|
| AC line / load power | **Black** | 240 VAC mains, motor leads (U/V/W to motor), VFD power input (R/S/T) |
| AC control circuits | **Red** | 120 VAC control wiring (only if used — most of this panel runs on 24 VDC) |
| DC control circuits (ungrounded) | **Blue** | +24 VDC supply, all DC signal wires (PLC inputs, VFD control terminals, relay coils, sensor outputs) |
| DC control circuits (grounded return) | **Blue with white stripe** | 0 VDC return / common back to the DC supply |
| Foreign voltage (sourced outside the main disconnect) | **Yellow** | Signals fed from external sources not de-energized by the panel disconnect (rare on this build) |
| Equipment grounding | **Green** or **Green/Yellow** | Chassis ground, PE, equipment bonding |

## Notes on the DC return color

The strict NFPA 79 callout for DC return is **Blue with a white stripe**. Solid **white** is widely accepted in industry practice when striped wire is not stocked. Either is acceptable for this project. Do not use solid blue for the return — that creates ambiguity with the +24 V hot wires.

## Wire labels are the primary identifier for DC signals

Because every DC control wire on this panel is blue (NFPA 79 requires it), color alone does not distinguish individual signals. Each wire must be **labeled at both ends** with its function (e.g. `JAM`, `FOR`, `REV`, `RST`, `+24V-JAM`, `0V-COM`).

Use heat-shrink markers, printed wire-wrap labels, or industrial labeler tape. Hand-written sharpie marks are not durable enough for a permanent panel.

## Wire Gauge

Standard sizing for this panel:

| Application | Gauge | Notes |
|---|---|---|
| Motor power (U/V/W) | 12 AWG | Sized for 3 HP motor + VFD output rating |
| AC mains input | 12 AWG | Per breaker / fuse rating |
| Brake resistor leads (P, Pr) | 14 AWG | Handles braking pulse current |
| DC control (24V) and signal wires | 18 AWG stranded | Industry-standard control wire size |
| Ground / bonding | 12 AWG (or per breaker rating) | Per NEC 250 |

All control wires terminate with **crimped ferrules** at terminal blocks. Hand-twisted strands are not acceptable for any UL/CE-style panel build.

## Examples from this project

| Wire on this panel | Color | Label |
|---|---|---|
| +24V DC supply to VFD FB terminal (jam signal source, through 500 mA fuse) | Blue | `+24V-JAM` |
| VFD FC terminal to PLC X5 input | Blue | `JAM` |
| 0V DC return to PLC C terminal | Blue/White stripe (or White) | `0V-COM` |
| PLC Y0 output to VFD FOR input | Blue | `FOR` |
| PLC Y1 output to VFD REV input | Blue | `REV` |
| PLC Y2 output to VFD RST input | Blue | `RST` |
| Motor leads VFD output to motor | Black | `U`, `V`, `W` |
| AC mains from breaker to VFD | Black | `L1`, `L2`, `L3` (if 3-phase) |
| Chassis ground (PE) | Green or Green/Yellow | `PE` |
| E-stop loop wiring (24 VDC) | Blue | `ESTOP+`, `ESTOP-` |

## Related Documentation

- [VFD over-current signal wiring](../VFD/Overcurrent_Signal_Wiring.md) — full wiring table for the jam signal
- [Brake resistor wiring](../VFD/Brake_Resistor_Wiring.md) — P/Pr terminal wiring
- [Motor nameplate](../VFD/Motor_Nameplate.md) — motor identification and VFD parameter values
