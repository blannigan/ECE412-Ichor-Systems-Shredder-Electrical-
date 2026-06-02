# Operator Controls — Pushbutton Bill of Materials

Reference for the operator pushbutton assemblies and panel wire duct used in the shredder control panel. Sourced from URS Electronics (Portland, OR), Invoice #828759, ordered 2026-05-15.

## Pushbutton Stations

All pushbuttons use the **Autonics S2PR series**: 22 mm panel-mount, illuminated, momentary push-to-make, spring return. Each pushbutton assembly is built from three modular components: a colored button head, an LED indicator block, and a NO contact block.

### Pushbutton Components (per assembly)

| Component | Part Number | Description |
|---|---|---|
| Pushbutton head (color-specific) | `S2PR-P3X` | 22 mm illuminated raised momentary head. `X` is replaced by color code: `G`/`Y`/`B`/`R`/`W`. |
| LED indicator block (color-specific) | `SA-LDX` | LED modular block, 12-24 VDC/VAC, color-matched to button. `X` is replaced by color code: `G`/`Y`/`B`/`R`/`W`. |
| Contact block (color-independent) | `SA-CA` | 1 NO contact block, finger-safe, 110 VAC / 10 A, 220 VAC / 5 A. Old P/N MC22-UA. |

### Buttons Used on This Panel

| Color | Head | LED Block | Contact | Function | PLC Input |
|---|---|---|---|---|---|
| **Green** | `S2PR-P3G` | `SA-LDG` | `SA-CA` | Forward (start shredding) | X0 |
| **Yellow** | `S2PR-P3Y` | `SA-LDY` | `SA-CA` | Reverse (manual reversal) | X1 |
| **Blue** (×2) | `S2PR-P3B` | `SA-LDB` | `SA-CA` | Deadman 1 and Deadman 2 (two-hand control) | X2 and X3 |
| **Red** | `S2PR-P3R` | `SA-LDR` | `SA-CA` | Reset / Clear lockout (tentative) | X6 (TBD) |

### Wiring Topology (all buttons)

Each button is wired the same way — sourcing input topology, +24 VDC switched through the NO contact:

```
   PSU +V ── 1 A fuse (EURO S4LH) ──┬── Button NO contact ── PLC X input
                                     │
                                     └── LED block + terminal ── (illumination)
   
   PSU -V ──── PLC D2-08ND3 common terminal (C)
   PSU -V ──── LED block - terminal (return for illumination)
```

When the button is pressed, the NO contact closes and +24V appears at the PLC input. The PLC reads the input HIGH while the button is held. The LED illuminates whenever +24V is present at the button (signals to the operator that the panel is energized and the button circuit is alive).

## Wire Duct

| Component | Part Number | Description | Quantity |
|---|---|---|---|
| Slotted wire duct | Panduit `G1X1LG6` | 1" W × 1" H, light gray, 6 ft lengths, PVC, Type G wide-finger slots | 6 ft |
| Duct cover | Panduit `C1LG6` | 1" W duct cover, light gray, 6 ft lengths | 6 ft |

Type G "wide finger" slotted duct is the standard for control panel wire management. Wires drop into the slots from outside, slots flex to retain them, and the snap-on cover keeps everything contained. Allows for easy modification and addition of wires without removing existing runs.

## Ferrules

| Component | Part Number | Description | Quantity |
|---|---|---|---|
| Insulated crimp ferrules | Z+F `V30AE000055` | 12 AWG, 10 mm length, gray, DIN/Z+F color code, polypropylene insulated | 500 pack |

Note: this is the 12 AWG size (gray per DIN 46228-4 color coding). For 18 AWG control wiring, a different size is needed — typically 14-16 AWG ferrules color-coded blue or black per DIN.

## Invoice Reference

- Vendor: URS Electronics, Inc.
- Address: 123 NE 7th Ave, Portland, OR 97232
- Invoice #: 828759
- Order #: 478075
- Order date: 2026-05-15
- Subtotal: $85.28
- Total: $85.28 (paid via Visa)

## Related Documentation

- [PLC I/O Map](../ai/io_map.md) — Maps each pushbutton to a specific PLC input address
- [Wire Color Standard](Wire_Color_Standard.md) — NFPA 79 wire colors used throughout the panel
- [VFD Control Terminal Reference](../VFD/Control_Terminal_Reference.md) — VFD digital input wiring (separate from operator buttons)
