# Hardware Components

## PLC System
| Component | Model | Notes |
|---|---|---|
| PLC Rack | DirectLOGIC 205 D2-09B-1 | 9-slot base unit |
| CPU | H2-DM1E | Built-in Ethernet, executes ladder logic |
| Discrete Input | D2-08ND3 | 8-ch 24VDC digital inputs, sourcing (Slot 2) |
| Analog Input | F2-08AD-1 | 8-ch current input 4–20mA; CH1 = VFD VO motor-current monitor (Slot 3) |
| RTD Input | F2-04RTD | 4-ch PT100/PT1000 temp, all channels spare (Slot 4) |
| Relay Output | D2-08TR | 8-ch relay (dry contact), sinking, common to PSU −V (Slot 5) |
| Analog Output | F2-08DA-2 | 8-ch voltage output 0–10V; CH1 = VFD VI speed reference (Slot 6) |
| Fill Panels | D2-Fill | Slots 7, 8, 9 (reserved) |

## HMI
| Component | Model | Notes |
|---|---|---|
| Touch Panel | EA9-T6CL-R | 6" C-More color touch panel |
| HMI Power Supply | Rhino PSB12-030-P | DC supply for HMI |
| PLC–HMI Link | Serial (COM port) | Match baud/parity/stop bits on both ends |

## Power
| Component | Model | Notes |
|---|---|---|
| 24VDC Power Supply | Mean Well NDR-480-24 | Powers PLC I/O, contactor coil, pushbutton commons |
| Fuse Block (main) | MORSETTITALIA EURO S10H-5H | 25A for PSU branch, 1A for PLC branch |
| Pushbutton fuse | MORSETTITALIA EURO S4LH | 1A fast blow, distributed to pushbutton commons |

## Motor Control
| Component | Model | Notes |
|---|---|---|
| VFD | Huanyang HY02D211B-T | 0–10V speed command via F2-08DA-2 +V1 → VFD VI; current monitor via VFD VO → F2-08AD-1 CH1 |
| Motor | GE 5KE182BC205B | Motor leads via colored 4mm banana sockets (U=blue, V=white, W=red) to T1/T2/T3 |
| Contactor | Mitsubishi SD-N35 | Coil A1 in E-stop safety chain (E22B1 NC → A1, A2 → PSU −V); switches VFD T (neutral) leg |
| Line breaker | Phoenix Contact TMC 8 3C 15A (2907618) | Feeds SD-N35 contactor pole on the VFD neutral leg |
| Brake Resistor | ATO APCS-300R30-AD | 300W, 30Ω dynamic braking resistor on VFD P+/PR |
| Error Indicator | Wamco model 525 | Panel LED (28VDC, 0.6W) driven by D2-08TR Y4 |

## Safety / Control
| Component | Notes |
|---|---|
| E-stop | Hardwired NC into safety circuit |
| Two-hand start | Forward + Deadman SW1 + Deadman SW2 buttons (24VDC, fused 1.5A) |
| Lid interlock | DI input to PLC |
| Status lights | Power on / Running / Fault (driven by discrete outputs) |

## Wiring Accessories
| Component | Model | Notes |
|---|---|---|
| ZipLink Terminal Block | ZL-RTB20-OUT | Output module field wiring interface |
| ZipLink Terminal Block | ZL-RTB20 | Analog output field wiring interface |
| Contactor fuse | DF103V 1/2A slow blow | Protects contactor coil branch |
| Power conductor | 12 AWG Cu (THHN/MTW) | Rated 20A/25A/30A at 60/75/90 °C (NEC 310.16); used for VFD branch and power runs (motor FLA 7.6A) |
| Control conductor | 16–18 AWG Cu | 24 VDC discrete/analog signal wiring; ferruled at terminal blocks |

## Overcurrent Sizing Convention
- Branch/component **fuses sized at 125% of the protected component's rated continuous load** (NEC 210.20(A)/215.3).
- Exception: the VFD motor branch breaker (30A C-curve) follows NEC 430.52 (higher multiple of FLC to ride through inrush); running overload is handled by the VFD's electronic motor-overload function.
