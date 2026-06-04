# VFD Programmed Parameters

As-built list of every PD parameter programmed into the Huanyang HY02D211B-T VFD on this build. Use this as the master reference for the VFD configuration; the other VFD docs explain specific subsystems but this doc records the actual values in use.

## Motor Parameters

These should match the motor nameplate. The as-built production motor is the **IronHorse MTCP2-002** (2 HP, 230 V low-voltage connection, 5.93 A FLA, 4-pole, 1735 RPM). See [`Motor_Nameplate.md`](Motor_Nameplate.md) for full ratings and derivation.

> **As-programmed today (bench values):** the panel was last commissioned against the GE bench motor (5KE182BC205B, 7.6 A FLA, 1750 RPM) and the VFD still carries those values. Re-programming to the IronHorse values is on the [Open Work punch list](../docs/term2_week11_Open_Work.md).

| Code | Production value (IronHorse) | Currently programmed (GE bench) | Meaning |
|---|---|---|---|
| `PD141` | `230` | `230` | Motor rated voltage (V) — low-voltage connection |
| `PD142` | `5.93` | `7.6` | Motor rated current (A) — used as 100% reference for over-torque and overload protections |
| `PD143` | `4` | `4` | Motor poles — derived from synchronous speed (120 × 60 Hz / 1800 RPM) |
| `PD144` | `1735` | `1750` | Motor rated speed (RPM) at full load |

## Over-Current / Over-Torque Detection (Jam Signal)

These configure the relay output that drives the PLC's jam-detect input (X5). See [`Overcurrent_Signal_Wiring.md`](Overcurrent_Signal_Wiring.md) for the wiring and rationale.

| Code | Value | Meaning |
|---|---|---|
| `PD052` | `02` | FA-FB-FC relay function = Fault Indication. Relay closes on any VFD fault (over-torque, overvoltage, undervoltage, overheat). Function `12` (Over-torque Detect) was tested and does not actuate the relay on this firmware revision; `02` works as the production workaround. |
| `PD123` | `3` | Over-torque detect mode = detect during running, stop motor on detect. Triggers `dT` fault that fires the relay. |
| `PD124` | `150` | Over-torque trip level (% of `PD142`). With the IronHorse motor (`PD142 = 5.93 A`) the trip current is 150% × 5.93 = **8.9 A**. With the GE bench motor currently programmed (`PD142 = 7.6 A`) the trip is 150% × 7.6 = 11.4 A. Tune lower if real jams are missed, higher if hard cuts cause nuisance trips. |
| `PD125` | `3.0` | Over-torque detect time (s). Motor current must exceed `PD124` for this duration before the VFD trips. |

## Analog Output (VO Terminal — Motor Current Monitor)

This configures the VFD's analog output going to the PLC's F2-08AD-1 analog input module (CH1+) for monitoring.

| Code | Value | Meaning |
|---|---|---|
| `PD054` | `1` | VO terminal outputs motor current. Signal is 0-10V scaled to motor current (0 V = 0 A, 10 V = full-scale). PLC F2-08AD-1 reads this on CH1+. |
| `PD055` | `0` (default) | VO output gain factor. Left at default (100%). |

## Safety Configuration

These keep the VFD from auto-restarting after a fault. NFPA 79 §7.5 requires intentional operator action to resume after a stop.

| Code | Value | Meaning |
|---|---|---|
| `PD155` | `0` | Auto-restart attempts after fault = 0 (disabled). PLC handles all restart logic. |
| `PD153` | `0` | Auto-restart after instantaneous power loss = 0 (disabled). Operator must press deadman after power restore. |

## Other Operational Parameters

| Code | Value | Meaning |
|---|---|---|
| `PD001` | (TBD — verify) | Source of run command. `1` for external terminals (PLC drives FOR/REV via Y6/Y7 on D2-08TR). |
| `PD002` | (TBD — verify) | Source of frequency reference. `1` for analog voltage input (VI), driven by PLC F2-08DA-2 CH1 (+V1) 0-10V signal. |
| `PD003` | (TBD) | Acceleration time (s). |
| `PD004` | (TBD) | Deceleration time (s). |
| `PD006` | (TBD) | Upper frequency limit (Hz). |
| `PD007` | (TBD) | Lower frequency limit (Hz). |
| `PD120` | `0` | Stall prevention at constant speed = disabled. Confirmed correct so the over-torque detection can fire without stall prevention masking it. |

## Related Documentation

- [Overcurrent (Jam) Signal Wiring](Overcurrent_Signal_Wiring.md) — relay output wiring and bench-test procedures
- [Control Terminal Reference](Control_Terminal_Reference.md) — every VFD control terminal, generic reference
- [Brake Resistor Wiring](Brake_Resistor_Wiring.md) — P/Pr terminals and braking parameters
- [Motor Nameplate](../VFD/Motor_Nameplate.md) — motor specs that justify `PD141`-`PD144` values
- [PLC I/O Map](../ai/io_map.md) — PLC-side connections to VFD terminals
- [VFD parameter codes manual](VFD_PD_Codes.pdf) — full Huanyang HY-series parameter reference
