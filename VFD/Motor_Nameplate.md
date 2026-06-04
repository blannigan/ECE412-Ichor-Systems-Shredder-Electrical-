# Motor Nameplate

Reference data for the motor installed on Universal Plastic Shredder V2.0. Values read from the UL/CSA/CE nameplate affixed to the motor housing.

> **As-built note (2026-06):** the installed motor is an **AutomationDirect IronHorse MTCP2-002** inverter-duty motor. This replaces the GE 5KE182BC205B that earlier revisions of this document described. The VFD motor parameters below have been re-derived from this nameplate — most importantly the rated current (now **5.93 A**, was 7.6 A), which all percentage-based protections (over-torque/jam, overload) scale against.

## Identification

| Field | Value |
|---|---|
| Manufacturer | IronHorse (AutomationDirect) |
| Model | `MTCP2-002-…` (full suffix partially illegible on plate — verify; MTCP2 = inverter-duty series, `-002` = 2 HP) |
| Serial Number | `1093551V ZLJ` |
| Date of Manufacture | 2025.12 |
| Catalog / CC | `CC006A` |
| Country of Origin | China |

## Electrical Ratings

| Field | Value |
|---|---|
| Horsepower | **2 HP** (~1.5 kW) |
| Voltage | **230 / 460 VAC** (dual-voltage, 9-lead wye, series/parallel reconfigurable) |
| Full Load Amps (FLA) | **5.93 A @ 230V** / **2.97 A @ 460V** |
| Frequency | 60 Hz |
| Phase | 3-phase |
| Synchronous Speed | 1800 RPM (4-pole) |
| Full Load Speed | **1735 RPM** |
| NEMA Nominal Efficiency | 86.5% (FL) |
| NEMA Design | B |
| NEMA Code Letter | L (locked-rotor kVA range) |
| Rating | 40 °C ambient, continuous duty |

## Inverter / VFD Duty Rating

This motor is **explicitly inverter-duty rated** (lower nameplate block), which makes it well-suited to drive the shredder's constant-torque cutting load on a VFD:

| Field | Value |
|---|---|
| Speed range (constant torque) | **10:1 CT** |
| Speed range (variable torque) | **20:1 VT** |
| Drive type | PWM VFD |
| Inverter-duty service factor | 1.0 SF (on VFD) |

## Performance at 50 Hz (international spec)

| Voltage / Frequency | Performance |
|---|---|
| 200 / 400 VAC, 50 Hz | 2 HP at 7.13 A / 3.56 A, 1450 RPM, S.F. 1.0 |

## Mechanical / Environmental

| Field | Value |
|---|---|
| Frame | NEMA **145TC** |
| Enclosure | TEFC (Totally Enclosed Fan Cooled), **IP55** |
| Insulation Class | F |
| Motor Type | BJPE |
| Max Ambient | 40 °C |
| Drive-End Bearing | 6205ZZ C3 |
| Opposite-Drive-End Bearing | 6205ZZ C3 |
| Hazardous-location rating | Class I Div 2 Groups A/B/C/D; Class I Zone 2 IIC; T3C (160 °C) @ 40 °C amb / T3A (180 °C) @ 55 °C amb |

## Motor Lead Connection (9-lead, T1–T9)

The motor has nine leads (`T1`–`T9`) plus a ground. It is a standard NEMA dual-voltage **wye** motor. **The installed Huanyang HY02D211B-T VFD is a 230 V-class drive, so the motor is wired for its LOW-voltage (230 V) parallel-wye connection.** Do **not** use the 460 V connection on this drive — the motor would be severely under-fluxed and overheat.

**Low voltage — 230 V (parallel wye) — AS WIRED:**

| Connect to VFD output | Motor leads |
|---|---|
| `U` (drive T1) | T1 + T7 |
| `V` (drive T2) | T2 + T8 |
| `W` (drive T3) | T3 + T9 |
| (floating star point — tie & insulate, no external connection) | T4 + T5 + T6 |
| Ground (PE) | green/yellow lead → VFD ⏚ |

To reverse rotation, swap any two output groups at the VFD (e.g. U↔V); do not rewire inside the motor.

**High voltage — 460 V (series wye) — NOT USED on this build (reference only):**
T1→L1, T2→L2, T3→L3; pair T4+T7, T5+T8, T6+T9.

## VFD Configuration Notes

These nameplate values must be programmed into the VFD (Huanyang HY series) for correct V/Hz characteristics and accurate over-torque/over-current protection scaling. See [VFD_PD_Codes.pdf](../VFD/VFD_PD_Codes.pdf) for the full parameter reference and [Overcurrent_Signal_Wiring.md](../VFD/Overcurrent_Signal_Wiring.md) for jam-detection programming.

**Connection choice:** The motor is wired for **230 VAC** operation (low-voltage / parallel-wye connection). The VFD output voltage must be set to match.

**VFD motor parameters (Huanyang HY series) — derived from this nameplate:**

| VFD code | Parameter | Value | Source on nameplate |
|---|---|---|---|
| `PD141` | Motor Rated Voltage | **230 V** | VOLTAGE field (low-voltage connection) |
| `PD142` | Motor Rated Current | **5.93 A** | AMPS field (230 V value) |
| `PD143` | Number of Motor Poles | **4** | derived: 120 × 60 Hz / 1800 RPM synchronous |
| `PD144` | Motor Rated Speed | **1735 RPM** | RPM field |

Additional nameplate-derived reference values (used for sizing, not entered as separate parameters):

| Value | Source on nameplate |
|---|---|
| Rated motor power: 2 HP (~1.5 kW) | HP field |
| Rated motor frequency: 60 Hz | Hz field |

**Drive sizing check:** the Huanyang HY02D211B-T is a 2.2 kW (3 HP) drive feeding a 2 HP / 1.5 kW motor — adequately sized (slightly oversized), which is acceptable.

The over-torque detect level (`PD124`, set to 150% for production in the jam-detection wiring) is scaled against `PD142` (motor rated current). With `PD142 = 5.93 A`, the production over-torque threshold trips at 5.93 × 1.50 = **8.9 A** actual motor current. All other percentage-based protections (motor overload, stall prevention) also scale against this `PD142` value.
