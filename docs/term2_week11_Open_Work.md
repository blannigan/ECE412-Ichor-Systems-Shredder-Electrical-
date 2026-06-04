# Open Work — Handover Punch List

End-of-term handover note for the sponsor and any future team that
picks the project back up.

**State at handover:** the entire control panel is fully wired
(operator face, VFD, PLC rack, HMI, 24 VDC supply, contactor, fused
terminal blocks, the analog VFD-feedback path, X7 input interface).
The single exception is the CTSI capacitive-touch module, which
needs a replacement board before its harness can be reconnected.

**What's left is configuration / firmware / calibration, not
hardware.** None of the items below require new wiring; they all
sit inside the PLC ladder program, the VFD parameter set, or the
HMI project file.

---

## 1. CTSI module — replacement and re-wire

| | |
|---|---|
| Status | Hardware destroyed during bench bring-up |
| Where it lives | `Capacitive_touch_code/`, ladder rung 28 |
| What's still in the panel | The X7 PLC input, the optocoupler interface, and the 24 V → 3.3 V buck converter slot |

What needs to happen:

1. Build / source a replacement capacitive-touch module on the
   same architecture (ESP32 + LM2596 24 V → 3.3 V buck +
   optocoupler driving panel `X7`).
2. Land its output on the existing optocoupler input; verify
   `X7 = HIGH` on touch and `LOW` on release with the PLC in
   monitor mode.
3. Bench-test the rung-28 response: touching the electrode
   should latch `Y4` (fault LED), `C15` (`STOP_MOTOR`),
   `C21` (`CTSI_TRIG`), and `C22` (`CHANGE_SCREEN`)
   simultaneously and independently of the deadman / E-stop
   chain.
4. Repeat once the mechanical prototype is delivered so the
   trip-zone geometry can be tuned.

---

## 2. Jam-count telemetry — surface on HMI

| | |
|---|---|
| Status | Counter increments correctly in the PLC; not visible on the HMI |
| Where it lives | `PLC/src/Shredder_Ladder_Logic_v1.dmd` (CT0 → N0), `HMI/HMI_413.mgp` |

What needs to happen:

1. In the HMI project (`HMI_413.mgp`), bind the `JAM_COUNTER`
   tag (PLC address `N0`, BCD int 16) to a numeric display on
   the Test screen (or wherever the operator should see live
   strike count).
2. Confirm the count increments visibly each time `JAM_LATCH`
   fires while `T2` is not done.
3. Confirm the count resets when `ERROR_RESET` (C18) is pulsed
   from the HMI fault-reset path.

---

## 3. Voltage / current / derived telemetry on Screen 2

| | |
|---|---|
| Status | Wired and scaled, but the displayed values are unstable / inaccurate |
| Where it lives | VFD parameters PD052–PD125, F2-08AD-1 channel 1, ladder rung 3, HMI Screen 2 |

The plan from day one was to take **frequency** and
**motor-current** out of the VFD's analog output and back-calculate
the derived voltage, RPM, and run-status fields shown on Screen 2.
The path

```
VFD VO  →  F2-08AD-1 CH1  →  WX0  →  SCALE (rung 3)  →  V3000  →  HMI CURRENT
```

is fully wired and the ladder math is in place, but the live values
don't settle to something usable.

What needs to happen:

1. Re-verify the VFD analog-output parameters:
   - `PD054` (VO function) is set to current output.
   - The 0–10 V range on VO actually corresponds to 0–FLA × N as
     documented in the Huanyang manual; bench-measure with a DVM
     against a known load to confirm the slope.
2. Recheck the F2-08AD-1 voltage / current selection jumpers
   match what `WX0` is being scaled against.
3. Replay the rung-3 `SCALE` constants against the verified
   analog range. Right now they assume 0–4095 raw → 0–140; that
   needs to be re-derived once step 1 lands.
4. Once `CURRENT` reads true, fill in the derived `VOLTAGE`,
   `RPM`, and `STATUS` fields on Screen 2 from the same primary
   measurement plus the commanded frequency.

> Note: a Modbus link to the VFD would replace this whole analog
> path with a clean digital readout but the Modbus add-on module
> exceeds the \$1,000 EE-team budget. The analog path stays as
> the in-budget answer.

---

## 4. Reprogram VFD for the production motor

The production motor (IronHorse **MTCP2-002**, 2 HP, 230 V,
**5.93 A** FLA, 4-pole, **1735 RPM**, VFD-rated 1.0 SF) is on the
machine. The VFD, however, still carries the GE bench-motor
parameter set from initial commissioning:
`PD141 = 230 V`, `PD142 = 7.6 A`, `PD143 = 4`, `PD144 = 1750 RPM`.

What needs to happen:

1. Re-program the four motor-nameplate codes to the IronHorse
   values: `PD141 = 230`, `PD142 = 5.93`, `PD143 = 4`,
   `PD144 = 1735`. Full nameplate in
   [`VFD/Motor_Nameplate.md`](../VFD/Motor_Nameplate.md).
2. Recheck over-torque calibration. `PD124 = 150%` of the new
   `PD142` is **8.9 A** trip current (was 11.4 A under the bench
   value). Tune `PD124` / `PD125` against real jam current once
   the ME team's loaded shred test is available (see item 5).
3. Confirm the analog motor-current scaling (rung 3, F2-08AD-1
   CH1) still tracks correctly against the new FLA — `WX0`
   constants may need a re-derive.

---

## 5. Full machine integration

Pending ME team delivery of the mechanical shredder prototype:

1. Mount the panel to the frame; route U/V/W through the
   panel-mount banana sockets to the motor.
2. Run a full loaded shred test against representative PVC / PP
   / LDPE sheet stock.
3. Tune `PD124` (over-torque threshold) and `PD125`
   (over-torque detect time) against the real jam current
   instead of the bench estimate.
4. Confirm the unjam reverse stroke (`T1`, 2 s) actually clears
   typical jams; lengthen or shorten the stroke if needed.
5. Mount the CTSI electrode at the safety zone defined by the
   ME team and re-validate `X7` trips at the intended distance.

---

## Where to look in the repo

- Ladder program — `PLC/src/Shredder_Ladder_Logic_v1.dmd`
- Point list — `PLC/Point_List.pdf` (or `PLC/src/Point_List.xlsx`)
- HMI project — `HMI/HMI_413.mgp`
- VFD parameter set — Section 5.2 of the Final Report, plus
  `VFD/Programmed_Parameters.md`
- CTSI code stub — `Capacitive_touch_code/`
- AutoCAD electrical drawings —
  `electrical/PLC_and_HMI.dwg`, `VFD_and_Motor.dwg`,
  `Power_Distribution_Capstone.dwg`

— Bao Nguyen
Repository maintainer on behalf of the team
baon@pdx.edu
