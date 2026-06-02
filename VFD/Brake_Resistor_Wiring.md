# Brake Resistor Wiring

This document describes how the dynamic braking resistor is wired to the Huanyang HY-series VFD and how it is sized for the shredder application.

## Why a Brake Resistor is Needed

When the VFD decelerates the motor (commanded stop, reversal, or normal slowdown), the motor acts briefly as a generator. The kinetic energy stored in the rotating mass of the motor, shaft, gearbox, and shredder blades flows back into the VFD as electrical energy. This energy charges the VFD's DC bus capacitors, raising the bus voltage above its normal level.

If nothing dissipates this regenerative energy, the bus voltage keeps climbing until the VFD trips on an **overvoltage fault (`Ou-1` / `Ou-2`)** to protect itself. The motor then coasts to a stop instead of decelerating under control, which defeats the purpose of the commanded stop.

A brake resistor solves this. The VFD contains an internal brake transistor (chopper) that switches the resistor across the DC bus whenever the bus voltage rises above the braking threshold. The regenerative energy flows into the resistor and is dissipated as heat. The bus voltage stays in range and the deceleration proceeds normally.

### Why this matters for the shredder

The shredder application generates regenerative energy in three situations:

1. **Normal stop (operator releases deadman)** — the motor decelerates the inertia of the shaft and blades.
2. **Auto-clear forward/reverse cycling during jam recovery** — each direction reversal first decelerates the motor to zero, then accelerates in the opposite direction. The deceleration half of each cycle dumps regenerative energy.
3. **E-stop trip** — fastest possible deceleration, largest regenerative pulse.

Without a brake resistor, frequent forward/reverse cycling (jam recovery) will reliably trip the VFD on overvoltage every time, breaking the auto-clear feature. The brake resistor is not optional for this application.

## VFD Terminals (P and Pr)

The brake resistor connects to two terminals on the VFD's **main circuit (power) terminal block** — not the control terminal block where the FA/FB/FC and FOR/REV terminals live. The brake resistor terminals are on the same row as the main AC input (R/S/T) and motor output (U/V/W) terminals.

| Terminal | Function |
|---|---|
| **P** | Positive DC bus terminal — one end of the brake resistor |
| **Pr** | Brake chopper output — other end of the brake resistor |

The terminal label on the VFD is typically printed as `P.Pr` indicating these two terminals work as a pair.

Some larger VFDs also have separate `P` and `N` terminals for connecting an *external* braking unit (a standalone chopper + resistor module used when the internal chopper cannot handle the regenerative power). For the 3 HP shredder, the VFD's internal chopper is sufficient and the resistor connects directly to **P and Pr**.

## Resistor Sizing

Two specifications matter: **resistance (ohms)** and **power dissipation (watts)**.

### Resistance value

The resistance value sets the peak current the brake transistor must handle. **Too low** = excessive current = brake transistor damage (`bt` fault). **Too high** = poor braking performance.

For the HY-series 220V class VFD driving a 3 HP / 2.2 kW motor:

| Motor / VFD class | Typical brake resistor resistance |
|---|---|
| 1-2 HP, 220V class | 100-200 Ω |
| **3 HP, 220V class** | **50-100 Ω (recommended: 75 Ω)** |
| 5 HP, 220V class | 30-50 Ω |
| 7.5 HP, 220V class | 25-40 Ω |

Confirm the minimum allowable resistance with the VFD's specific datasheet before ordering. Going below the minimum will damage the internal brake transistor.

### Power rating (watts)

The power rating sets how much continuous heat the resistor can dissipate without overheating. Higher = more headroom for frequent braking.

Sizing depends on braking duty cycle:

| Braking duty | Wattage for 3 HP shredder |
|---|---|
| Occasional stops only (no reversing) | 300 W |
| **Frequent stops, occasional reversals** | **500 W (recommended starting point)** |
| Heavy reversing duty (jam-clear cycles every minute) | 750-1000 W |

For the shredder, the auto-clear feature triples the braking duty during jam events. A **500 W resistor** is the recommended starting point — it provides headroom for typical use and the auto-clear routine, but is not so oversized that cost becomes excessive.

If lockouts from frequent `Ou` (overvoltage) faults appear during jam-clear cycles, upgrade to a 750 W or 1000 W resistor.

### Recommended part

| Spec | Value |
|---|---|
| Resistance | 75 Ω |
| Power rating | 500 W |
| Form factor | Aluminum-clad chassis-mount or open wire-wound |
| Voltage rating | ≥ 400 VDC |

Common sources: Vishay, Ohmite, Mouser/Digikey generic. Search "75 ohm 500W braking resistor VFD."

## Wiring Table

The brake resistor has only two terminals and no polarity — either end can connect to P or Pr.

| From | To | Wire color | Wire label |
|---|---|---|---|
| VFD `P` terminal (main power terminal block) | Brake resistor terminal 1 | Black | `BR-P` |
| VFD `Pr` terminal (main power terminal block) | Brake resistor terminal 2 | Black | `BR-Pr` |

**Wire gauge: 14 AWG stranded minimum** (12 AWG preferred). The brake resistor handles brief pulses of high current — a few amps continuous but tens of amps peak during heavy braking. Undersized wire heats up and adds resistance in series with the resistor, reducing braking effectiveness.

**Wire color:** NFPA 79 §13.2 specifies **Black for power-class wiring at line voltage**, which is the correct class for the DC bus connection at P and Pr (DC bus voltage on a 220V VFD runs ~300-400 VDC during braking).

**Wire length: as short as possible** — ideally under 1 meter (3 feet) between VFD and resistor. Long brake resistor wires add inductance, which causes voltage spikes that can damage the brake transistor. If the resistor must be mounted further from the VFD, use twisted-pair routing to cancel inductance.

## Physical Mounting

The brake resistor gets **hot** — easily 200-400°C surface temperature during heavy braking. Mounting requirements:

1. **Mount outside the VFD enclosure** if possible, or in a dedicated vented section away from electronics. The heat will cook nearby components if confined.
2. **Provide free airflow** around the resistor on all sides. Aluminum-clad resistors are typically rated assuming free convection — boxing them in derates the wattage by 50% or more.
3. **Keep flammable materials at least 6 inches away** — wire insulation, plastic conduit, paper labels, anything combustible.
4. **Use heat-rated wire near the resistor** — the last 12 inches of brake wire should be silicone-insulated or fiberglass-sleeved if the resistor is open-frame.
5. **Mechanically isolate from sensitive components** — vibration and thermal expansion can loosen terminals over time.
6. **Label clearly** — "HOT SURFACE" placard near the resistor warns maintenance staff. NFPA 79 requires hazard labeling for components above 60°C surface temperature.

## Required VFD Parameter Settings

The HY series enables dynamic braking automatically when a resistor is connected — no parameter changes are strictly required. However, two related parameters can be tuned:

| Code | Default | Description |
|---|---|---|
| `PD118` | `1` | Over-voltage stall prevention. `1` = enabled. Keep enabled — this is a backup that delays deceleration if the bus voltage rises despite the brake resistor (e.g., resistor disconnected or too small). |
| `PD031` | `2.0` | DC braking voltage level at start/stop. This is for the *DC injection braking* function (zero-frequency holding), separate from the dynamic braking that uses the resistor. Leave at default for shredder. |

The brake transistor switches automatically when DC bus voltage exceeds the internal braking threshold (factory-set, not user-adjustable on most HY revisions). The user does not need to configure when to brake — only ensure the resistor is connected and correctly sized.

## Optional: Brake Resistor Monitoring

The VFD's multi-function outputs include function code `32: Braking Resistor Act` — when assigned, the corresponding output closes whenever the brake transistor is firing. This can be wired to a PLC input or panel lamp for monitoring brake activity, useful for verifying the resistor is working and for diagnosing why deceleration is or is not happening as expected.

For example, assigning `PD053 = 32` would activate the KA-KB relay (if present on this VFD revision) every time the brake fires. Not required for normal operation — only useful for diagnostics or research.

## Behavior Summary

| Event | Internal Action | Result |
|---|---|---|
| Motor commanded to decelerate (stop, reverse, slowdown) | Motor acts as generator, regenerates energy into DC bus | Bus voltage rises |
| Bus voltage exceeds internal braking threshold | Brake transistor switches the resistor across the DC bus | Regenerative energy dissipated as heat in resistor |
| Bus voltage drops back below threshold | Brake transistor turns off | Deceleration continues |
| Deceleration ramp ongoing | Brake transistor cycles rapidly (PWM-style) | Bus voltage stays in range until motor reaches commanded speed |
| Brake resistor missing or undersized | Bus voltage rises uncontrolled | VFD trips on `Ou-1` / `Ou-2` (overvoltage); motor coasts instead of decelerating |
| Brake resistor wire shorted, or resistance too low | Brake transistor draws excessive current | VFD trips on `bt` (braking transistor damage); permanent damage possible |

## Safety Notes

- The brake resistor terminals (P and Pr) sit on the **DC bus at ~300-400 VDC during operation and for up to 5 minutes after power-off** (until bus capacitors discharge). Always wait for the VFD's POWER LED to fully extinguish before touching these terminals.
- The resistor itself can reach **200-400°C surface temperature**. Allow 15+ minutes cool-down before any maintenance.
- Brake resistor mounting location should be **inaccessible to operators during normal operation** — behind guards, inside the panel, or shielded.
- Never run the shredder without a brake resistor connected if the auto-clear routine is enabled. The repeated forward/reverse cycling will trip the VFD on overvoltage every time, breaking the feature.
