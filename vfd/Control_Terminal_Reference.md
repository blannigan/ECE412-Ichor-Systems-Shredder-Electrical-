# VFD Control Terminal Reference

Reference guide for every terminal on the Huanyang HY02D211B-T VFD's control terminal block. Documents what each terminal does and its electrical specification.

The VFD has two rows of terminals on a single green plug-in connector. Order matches what is printed on the terminal block label.

## Top Row (left to right)

| Terminal | Function | Type | Electrical Spec |
|---|---|---|---|
| `UPF` | Multi-Function Output 2 (PD051) — open-collector optocoupler | Digital output | NPN, 24 VDC, max 100 mA sinking |
| `DRV` | Multi-Function Output 1 (PD050) — open-collector optocoupler | Digital output | NPN, 24 VDC, max 100 mA sinking |
| `DCM` | Digital Common — 0V reference for all digital inputs (FOR, REV, RST, SPL, SPM, SPH) and digital outputs (UPF, DRV) | Reference / common | 0 V (tied to internal logic ground) |
| `SPL` | Multi-Input 6 — Low Speed select (factory default function) | Digital input | Sinking, activates when pulled to DCM |
| `SPM` | Multi-Input 5 — Middle Speed select | Digital input | Sinking, activates when pulled to DCM |
| `SPH` | Multi-Input 4 — High Speed select | Digital input | Sinking, activates when pulled to DCM |
| `RST` | Multi-Input 3 — Fault Reset | Digital input | Sinking, activates when pulled to DCM |
| `REV` | Multi-Input 2 — Reverse Run command | Digital input | Sinking, activates when pulled to DCM |
| `FOR` | Multi-Input 1 — Forward Run command | Digital input | Sinking, activates when pulled to DCM |
| `ACM` | Analog Common — 0V reference for analog inputs (AI, VI) and analog output (VO) | Reference / common | 0 V (tied to internal analog ground; internally connected to bottom-row ACM) |
| `VO` | Analog Output (0–10 V) | Analog output | 0–10 V proportional to selected signal (PD054 selects: 0=frequency, 1=current, 2=voltage, 3=DC bus); current depends on load (typically max ~5 mA) |
| `10V` | +10 V reference output | Reference / supply | +10 V, ~10 mA max. Used to power an external speed potentiometer if manual override is desired |

## Bottom Row (left to right)

| Terminal | Function | Type | Electrical Spec |
|---|---|---|---|
| `FA` | Multi-Function Output 3 — Form A (NO) contact of internal SPDT relay | Relay output | Dry contact, 3 A @ 250 VAC or 3 A @ 30 VDC |
| `FC` | Multi-Function Output 3 — Form C (common) of internal SPDT relay | Relay output | Dry contact (common pole) |
| `FB` | Multi-Function Output 3 — Form B (NC) contact of internal SPDT relay | Relay output | Dry contact, 3 A @ 250 VAC or 3 A @ 30 VDC |
| `24V` | +24 V auxiliary supply output (onboard supply, useful for installations without an external 24 V source) | Supply / power | +24 V, max 200 mA |
| `DCM` | Digital Common — duplicate of top-row DCM (internally tied) | Reference / common | 0 V |
| `(blank)` | Reserved / not connected | — | — |
| `5V` | +5 V reference output | Reference / supply | +5 V, low current |
| `ACM` | Analog Common — duplicate of top-row ACM (internally tied) | Reference / common | 0 V |
| `AI` | Analog Current Input — speed reference from 4–20 mA source | Analog input | 4–20 mA input |
| `VI` | Analog Voltage Input — speed reference from 0–10 V source | Analog input | 0–10 V input, 250 kΩ impedance |
| `RS-` | RS-485 Modbus Communication — negative line | Communication | RS-485 differential |
| `RS+` | RS-485 Modbus Communication — positive line | Communication | RS-485 differential |

## Multi-Function Output Programming

The three multi-function outputs (`UPF`, `DRV`, and `FA`/`FB`/`FC` relay) are assigned a function via parameters:

| Output terminal(s) | Parameter | Default function | Common alternate functions |
|---|---|---|---|
| `DRV` (optocoupler) | `PD050` | `01` (In Run) | `02` Fault Indication, `10` Inverter Overload, `12` Over-torque Detect |
| `UPF` (optocoupler) | `PD051` | `05` (Set Frequency Reached) | Same options as PD050 |
| `FA`/`FB`/`FC` (relay) | `PD052` | `02` (Fault Indication) | `12` Over-torque Detect (firmware-quirk on this revision, see Overcurrent_Signal_Wiring.md), `01` In Run, etc. |

Full list of multi-function output function codes (0–32) is in [`VFD_PD_Codes.pdf`](VFD_PD_Codes.pdf) under PD050 description.

## Multi-Function Input Programming

The four standard multi-inputs `SPL`, `SPM`, `SPH`, and (some other inputs depending on revision) are programmable to different functions:

| Input | Parameter | Default function |
|---|---|---|
| `FOR` | (fixed) | Forward run |
| `REV` | (fixed) | Reverse run |
| `RST` | (fixed) | Fault reset |
| `SPH` | `PD044` | High-speed multi-step frequency select |
| `SPM` | `PD045` | Middle-speed multi-step frequency select |
| `SPL` | `PD046` | Low-speed multi-step frequency select |

These multi-step inputs can be reassigned via their PD parameters to other functions (jog, external control, counter input, etc.) — see PD parameter manual.

## Analog Output (VO) Programming

The `VO` terminal can output different VFD operating values via parameter `PD054`:

| `PD054` | What VO outputs |
|---|---|
| `0` (default) | Output frequency (0–10 V = 0 to max frequency) |
| `1` | Output current |
| `2` | Output voltage |
| `3` | DC bus voltage |

A gain factor `PD055` adjusts the output range (default 100 = no gain change).

## Related Documentation

- [Overcurrent (Jam) Signal Wiring](Overcurrent_Signal_Wiring.md) — detailed FA/FB/FC and RST wiring with fuse sizing and parameter settings
- [Brake Resistor Wiring](Brake_Resistor_Wiring.md) — P/Pr power-circuit terminals (separate from the control terminals documented here)
- [VFD parameter codes (HY-series manual)](VFD_PD_Codes.pdf) — full PD parameter reference
- [PLC I/O Map](../ai/io_map.md) — PLC-side wiring and addresses
