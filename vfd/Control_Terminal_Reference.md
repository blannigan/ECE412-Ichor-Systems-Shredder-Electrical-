# VFD Control Terminal Reference

Reference guide for every terminal on the Huanyang HY02D211B-T VFD's control terminal block. Documents what each terminal does, electrical specs, and how it is used (or not used) in this build.

The VFD has two rows of terminals on a single green plug-in connector. Order matches what is printed on the terminal block label.

## Top Row (left to right)

| Terminal | Function | Type | Electrical Spec | Used in this build? |
|---|---|---|---|---|
| `UPF` | Multi-Function Output 2 (PD051) — open-collector optocoupler | Digital output | NPN, 24 VDC, max 100 mA sinking | No (unused) |
| `DRV` | Multi-Function Output 1 (PD050) — open-collector optocoupler | Digital output | NPN, 24 VDC, max 100 mA sinking | No (unused) |
| `DCM` | Digital Common — 0V reference for all digital inputs (FOR, REV, RST, SPL, SPM, SPH) and digital outputs (UPF, DRV) | Reference / common | 0 V (tied to internal logic ground) | **Yes** — wired to PSU −V for shared 0V reference with PLC |
| `SPL` | Multi-Input 6 — Low Speed select (factory default function) | Digital input | Sinking, activates when pulled to DCM | No (unused) |
| `SPM` | Multi-Input 5 — Middle Speed select | Digital input | Sinking, activates when pulled to DCM | No (unused) |
| `SPH` | Multi-Input 4 — High Speed select | Digital input | Sinking, activates when pulled to DCM | No (unused) |
| `RST` | Multi-Input 3 — Fault Reset | Digital input | Sinking, activates when pulled to DCM | **Yes** — driven by PLC Y5 (D2-08TR relay output) to clear VFD faults |
| `REV` | Multi-Input 2 — Reverse Run command | Digital input | Sinking, activates when pulled to DCM | **Yes** — driven by PLC Y6 (D2-08TR relay output) for reverse direction during unjam routine |
| `FOR` | Multi-Input 1 — Forward Run command | Digital input | Sinking, activates when pulled to DCM | **Yes** — driven by PLC Y7 (D2-08TR relay output) for forward shredding operation |
| `ACM` | Analog Common — 0V reference for analog inputs (AI, VI) and analog output (VO) | Reference / common | 0 V (tied to internal analog ground; internally connected to bottom-row ACM) | **Yes** — wired to PLC F2-08DA-2 module's 0V terminal for the speed command signal return |
| `VO` | Analog Output (0–10 V) | Analog output | 0–10 V proportional to selected signal; current depends on load (typically max ~5 mA) | **Yes (planned)** — outputs motor current (`PD054 = 1`) to PLC F2-06AD-1 analog input for monitoring and display |
| `10V` | +10 V reference output | Reference / supply | +10 V, ~10 mA max | No (unused) — would feed an external speed potentiometer if manual override was needed |

## Bottom Row (left to right)

| Terminal | Function | Type | Electrical Spec | Used in this build? |
|---|---|---|---|---|
| `FA` | Multi-Function Output 3 — Form A (NO) contact of internal SPDT relay | Relay output | Dry contact, 3 A @ 250 VAC or 3 A @ 30 VDC | **Yes** — wired to PLC X5 input on D2-08ND3 to signal VFD fault state (active-high when VFD trips) |
| `FC` | Multi-Function Output 3 — Form C (common) of internal SPDT relay | Relay output | Dry contact (common pole) | **Yes** — wired to +24V (Mean Well +V) through 500 mA fast-blow fuse |
| `FB` | Multi-Function Output 3 — Form B (NC) contact of internal SPDT relay | Relay output | Dry contact, 3 A @ 250 VAC or 3 A @ 30 VDC | No (left empty in active-high NO wiring configuration) |
| `24V` | +24 V auxiliary supply output | Supply / power | +24 V, max 200 mA | No (unused) — onboard supply intentionally not used; panel 24V comes from Mean Well NDR-480-24 |
| `DCM` | Digital Common — duplicate of top-row DCM (internally tied) | Reference / common | 0 V | Available alternate landing point if top-row DCM screw is full |
| `(blank)` | Reserved / not connected | — | — | — |
| `5V` | +5 V reference output | Reference / supply | +5 V, low current | No (unused) |
| `ACM` | Analog Common — duplicate of top-row ACM (internally tied) | Reference / common | 0 V | Available alternate landing point for analog returns |
| `AI` | Analog Current Input — speed reference from 4–20 mA source | Analog input | 4–20 mA input | No (unused) — speed command uses VI (voltage) instead |
| `VI` | Analog Voltage Input — speed reference from 0–10 V source | Analog input | 0–10 V input, 250 kΩ impedance | **Yes** — receives speed command from PLC F2-08DA-2 `+V1` (0–10 V proportional to commanded frequency) |
| `RS-` | RS-485 Modbus Communication — negative line | Communication | RS-485 differential | No (unused) — this build uses analog speed reference and digital I/O instead of Modbus |
| `RS+` | RS-485 Modbus Communication — positive line | Communication | RS-485 differential | No (unused) |

## Summary of Active Connections

Quick visual of which terminals are wired in this build:

```
Top row:    UPF  DRV  DCM  SPL  SPM  SPH  RST  REV  FOR  ACM  VO   10V
                       ✓               ✓    ✓    ✓    ✓    ✓
                                       │    │    │    │    │
                                       Y5   Y6   Y7   F2-08DA-2 0V
                                       │    │    │         (analog speed
                                       │    │    │          return)
                                       │    │    │
                                       │    │    └─ Forward (D2-08TR sinking)
                                       │    └────── Reverse (D2-08TR sinking)
                                       └─────────── Reset   (D2-08TR sinking)

Bottom row: FA   FC   FB   24V  DCM  ___  5V   ACM  AI   VI   RS-  RS+
            ✓    ✓                                            ✓
            │    │                                            │
            X5   +24V                                         F2-08DA-2 +V1
                 (fused 500 mA)                               (analog speed
                                                               command in)
```

Active wires:
- 4 control inputs from PLC: FOR (Y7), REV (Y6), RST (Y5), DCM common (PSU −V)
- 1 fault relay to PLC: FA → X5, FC → +24V (fused), DCM common shared
- 1 analog speed command from PLC: VI ← F2-08DA-2 +V1, ACM ← F2-08DA-2 0V
- 1 analog monitoring back to PLC (planned): VO → F2-06AD-1 CH+, ACM ← F2-06AD-1 CH−

## Related Documentation

- [Overcurrent (Jam) Signal Wiring](Overcurrent_Signal_Wiring.md) — detailed FA/FB/FC and RST wiring with fuse sizing
- [Brake Resistor Wiring](Brake_Resistor_Wiring.md) — P/Pr power-circuit terminals (separate from the control terminals documented here)
- [VFD parameter codes (HY-series manual)](VFD_PD_Codes.pdf) — full PD parameter reference
- [PLC I/O Map](../ai/io_map.md) — PLC-side wiring and addresses
