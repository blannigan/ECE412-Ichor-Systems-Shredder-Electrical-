# Motor Nameplate

Reference data for the motor installed on Universal Plastic Shredder V2.0. Values read from the nameplate affixed to the motor housing.

> **Status:** The **IronHorse MTCP2-002** described below is the production motor on the as-built panel. Earlier in the project a GE 5KE182BC205B (3 HP, 7.6 A FLA) bench motor was used for control-system bring-up and is referenced in the historical Weekly Progress Reports and parts of the Final Report. The historical specs are retained at the bottom of this file for traceability.

## Identification

| Field | Value |
|---|---|
| Manufacturer | IronHorse (AutomationDirect) |
| Model | `MTCP2-002` |
| Part code on plate | `CC006A` / `259277` |
| Serial Number | `1093551V ZLJ` |
| Country of Origin | China |
| Date of Manufacture | 2025-12 |

## Electrical Ratings (60 Hz)

| Field | Value |
|---|---|
| Horsepower | **2 HP** |
| Voltage | **230 / 460 VAC** (dual-voltage) |
| Full Load Amps (FLA) | **5.93 A @ 230 V** / **2.97 A @ 460 V** |
| Frequency | 60 Hz |
| Phase | 3-phase |
| Synchronous Speed | 1800 RPM (4-pole) |
| Full Load Speed | **1735 RPM** |
| Service Factor — on line | 1.15 |
| Service Factor — on VFD | **1.0** (VFD-rated) |
| Nominal Efficiency (FL / 3/4) | **86.5 %** / 89.x % |
| NEMA Code Letter | L (locked rotor kVA range) |
| Insulation Class | F |
| Rating | 40 °C ambient continuous |

## Electrical Ratings (50 Hz — alternate)

| Field | Value |
|---|---|
| Horsepower | 2 HP |
| Voltage | 200 / 400 VAC |
| Full Load Amps (FLA) | 7.13 A / 3.56 A |
| Full Load Speed | 1450 RPM |
| Service Factor | 1.0 |

## VFD-rating Detail

The nameplate calls out an **adjustable-speed range** for VFD operation: `10:1 CT 20:1 VT, PWM VFD, 1.0 SF`. This means the motor will hold rated torque from 1/10 of base speed at constant torque or 1/20 of base speed at variable torque, with a service factor of 1.0 when fed from a PWM drive (vs. 1.15 on the line).

## Mechanical

| Field | Value |
|---|---|
| Frame | NEMA 145TC |
| NEMA Design | B |
| Enclosure | TEFC, IP55 |
| Shaft End Bearing | 6205ZZ C3 |
| Opposite End Bearing | 6205ZZ C3 |

## Hazardous-Location Listing

| Field | Value |
|---|---|
| Class I, Div. 2 Groups A B C D | T3C at 40 °C ambient (160 °C surface) |
| Class I, Zone 2 IIC | T3A at 55 °C ambient (180 °C surface) |

## VFD Configuration Notes

These nameplate values are programmed into the VFD (Huanyang HY02D211B-T) for correct V/Hz characteristics and accurate over-torque/over-current protection scaling. See [VFD_PD_Codes.pdf](VFD_PD_Codes.pdf) for the full parameter reference and [Overcurrent_Signal_Wiring.md](Overcurrent_Signal_Wiring.md) for jam-detection programming.

**Connection choice:** The motor is wired for **230 VAC** operation (low-voltage / parallel connection). The VFD output voltage must match.

**VFD motor parameters (Huanyang HY02D211B-T) — values for the as-built IronHorse motor:**

| VFD code | Parameter | Value | Source on nameplate |
|---|---|---|---|
| `PD141` | Motor Rated Voltage | **230 V** | low-voltage connection |
| `PD142` | Motor Rated Current | **5.93 A** | 230 V FLA |
| `PD143` | Number of Motor Poles | **4** | derived from 1735 RPM @ 60 Hz |
| `PD144` | Motor Rated Speed | **1735 RPM** | nameplate RPM |

Additional nameplate-derived reference values:

| Value | Source |
|---|---|
| Rated motor power: 2 HP (~1.5 kW) | HP field |
| Rated motor frequency: 60 Hz | HERTZ field |

The over-torque detect level (`PD124`, set to 150 % for production) scales against `PD142`. With `PD142 = 5.93 A`, the over-torque threshold trips at 5.93 × 1.50 = **8.9 A** actual motor current.

> **Programming note for handoff:** the VFD parameter set in the panel today still reflects the GE bench motor (`PD142 = 7.6 A`, `PD144 = 1750 RPM`). Reprogramming to the IronHorse values above is on the [Open Work punch list](../docs/term2_week11_Open_Work.md).

---

## Historical reference — GE bench motor

Used during control-system bring-up and across the Winter / Spring weekly progress reports. Replaced by the IronHorse for the as-built panel.

| Field | GE bench value |
|---|---|
| Manufacturer / Model | GE 5KE182BC205B |
| Serial | 33A309001 |
| HP | 3 |
| Voltage | 230 / 460 VAC |
| FLA @ 230 V | 7.6 A |
| Full Load Speed | 1750 RPM |
| Frame | NEMA 182T |
| Enclosure | TEFC |
