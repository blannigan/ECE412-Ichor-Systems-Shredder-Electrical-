# Ichor Systems Shredder — EE Capstone Quick Reference

**Project:** Universal Plastic Shredder V2.0 — Electrical System
**Course:** ECE 412/413, PSU, Winter–Spring 2026
**Sponsor:** MME / Ichor Systems (Bridget Lannigan)
**Advisors:** Prof. Andrew Greenberg, Dr. Jonathan Bird (EE), Robert Paxton (ME)

## Team
| Name | Email |
|---|---|
| Bao Nguyen | baon@pdx.edu |
| Fearghus Tyler | fearghus@pdx.edu |
| Yaqoub Rabiah | yrabiah@pdx.edu |
| Fox Kang | foxkang@pdx.edu |

## Scope
EE team owns: VFD motor control, PLC ladder logic, HMI, safety circuits (E-stop, two-hand start, lid interlock, overload), wiring, enclosure.
ME team owns: mechanical frame, cutting blades, gearbox.

## Key Specs
- Motor: 3–5 HP, target 70–90 RPM shaft output
- Plastics: PVC / PP / LDPE, 0.25–0.5" thick, 4–12" wide
- Power: 120 VAC or 208–240 VAC facility supply
- Budget: $3,000 total (EE ~$1,000)
- Standards: NFPA 70 (NEC), NEMA enclosure guidance

## Repo Structure
```
CLAUDE.md           ← this file (AI quick reference)
ai/                 ← detailed AI reference files
  components.md     ← all hardware with model numbers
  io_map.md         ← PLC I/O point assignments
  requirements.md   ← must/should/may requirements
docs/               ← numbered project documents (01_Project_Proposal → 07_Final_Report)
BOM/                ← bill of materials spreadsheets
CAD/                ← Inventor parts (Part1–10) + CAPSTONE_CAD.zip
electrical/         ← circuit logic and deadman logic PDFs
PLC/                ← ladder logic (.dmd), point list (.xlsx + .pdf)
HMI/                ← HMI project file (.mgp)
```

## Detailed References
See `ai/components.md` for full hardware list with model numbers.
See `ai/io_map.md` for PLC rack layout and I/O assignments.
See `ai/requirements.md` for full requirements list.
