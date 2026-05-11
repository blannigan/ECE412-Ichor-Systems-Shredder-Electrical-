# Motor Nameplate

Reference data for the motor installed on Universal Plastic Shredder V2.0. Values read from the UL/CSA nameplate affixed to the motor housing.

## Identification

| Field | Value |
|---|---|
| Manufacturer | GE (General Electric AC Motor) |
| Model | `5KE182BC205B` |
| Serial Number | `33A309001` |
| Stock Number | `S219` |
| UL File | `E47088` |
| CSA File | `LR47826` |
| Country of Origin | Taiwan |

## Electrical Ratings

| Field | Value |
|---|---|
| Horsepower | **3 HP** |
| Voltage | **230 / 460 VAC** (dual-voltage, wye/delta or series/parallel reconfigurable) |
| Full Load Amps (FLA) | **7.6 A @ 230V** / **3.8 A @ 460V** |
| Frequency | 60 Hz |
| Phase | 3-phase |
| Synchronous Speed | 1800 RPM (4-pole) |
| Full Load Speed | **1750 RPM** |
| Service Factor | 1.15 |
| Power Factor | 85% |
| NEMA Nominal Efficiency | 87.5% |
| NEMA Code Letter | K (locked rotor kVA range) |
| Locked Rotor Amps (LRA) | 68 A @ 230V / 34 A @ 460V |
| Max KVAR | 1.3 |
| Rating | Continuous duty |

## Performance at Alternate Voltages

| Voltage / Frequency | Performance |
|---|---|
| 208 VAC, 60 Hz | Usable at 8.4 A (derated service-factor operation) |
| 190 / 380 VAC, 50 Hz | 3 HP at 6.20 A / 3.10 A (international 50 Hz spec) |

## Mechanical

| Field | Value |
|---|---|
| Frame | NEMA 182T |
| NEMA Design | A |
| Enclosure | TEFC (Totally Enclosed Fan Cooled) |
| Insulation Class | F |
| Max Ambient | 40°C |
| Shaft End Bearing | 6306ZZ |
| Opposite End Bearing | 6306ZZ |
| Weight | 95 lb |

## VFD Configuration Notes

These nameplate values must be programmed into the VFD (Huanyang HY series) for correct V/Hz characteristics and accurate over-torque/over-current protection scaling. See [VFD_PD_Codes.pdf](../vfd/VFD_PD_Codes.pdf) for the full parameter reference and [Overcurrent_Signal_Wiring.md](../vfd/Overcurrent_Signal_Wiring.md) for jam-detection programming.

**Connection choice:** The motor is wired for **230 VAC** operation (low-voltage / parallel connection). The VFD output voltage must be set to match.

**VFD motor parameters (Huanyang HY series) — verified programmed and matching this nameplate:**

| VFD code | Parameter | Programmed value | Source on nameplate |
|---|---|---|---|
| `PD141` | Motor Rated Voltage | **230 V** | VOLTS field (low-voltage connection) |
| `PD142` | Motor Rated Current | **7.6 A** | AMP field (230V value) |
| `PD143` | Number of Motor Poles | **4** | derived: 120 × 60 Hz / 1800 RPM synchronous |
| `PD144` | Motor Rated Speed | **1750 RPM** | RPM field |

Additional nameplate-derived reference values (not entered as separate parameters but used for sizing):

| Value | Source on nameplate |
|---|---|
| Rated motor power: 3 HP (~2.2 kW) | HP field |
| Rated motor frequency: 60 Hz | HERTZ field |

The over-torque detect level (`PD124`, set to 150% for production in the jam-detection wiring) is scaled against `PD142` (motor rated current). With `PD142 = 7.6 A` confirmed, the production over-torque threshold trips at 7.6 × 1.50 = **11.4 A** actual motor current. All other percentage-based protections (motor overload, stall prevention) also scale against this `PD142` value.
