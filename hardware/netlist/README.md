# Netlist — Urine Analyzer Lite (Design A)

Generated from the `config.h` master pin map (see `../ENGINEERING_REVIEW.md §3`).

## Files
- `gen_netlist.py` — generator (single source of truth: the `COMPONENTS` model).
- `urine_analyzer_lite.net` — KiCad legacy netlist. **Import path to PCB layout.**
- `NETLIST.md` — human-readable component + net table for review.

## Regenerate
```bash
python3 gen_netlist.py
```

## How the engineer uses this (Stage 4 verification → layout)
1. **Review** `NETLIST.md` against `ENGINEERING_REVIEW.md` and the firmware `config.h`.
2. In KiCad, create a project; **Pcbnew → File → Import Netlist → `urine_analyzer_lite.net`**.
   This brings in all components + the ratsnest (connectivity) for layout.
3. **Assign real footprints** — the footprints in the netlist are descriptive placeholders.
   Map each to a verified KiCad footprint (or a custom one for the dev-board/module headers).
4. Alternatively, draw the schematic in KiCad's Eeschema from `NETLIST.md`, annotate, and run
   **ERC** — this is the formal Stage 4 schematic-verification step.
5. Then PCB: power planes (GND / +5V / +3V3), wide traces for motor/printer/UV-C, mounting
   holes to the chassis stand-offs, **DRC → 0 errors**, export Gerbers + assembly BOM.

## Known notes for the engineer
- **VBUS** is a single-node net by design: 5V USB input lives on the TP4056 module's own
  USB-C connector; not separately modeled.
- **Footprints are placeholders.** Most parts here are breakout boards / dev modules wired via
  pin headers — expect to create header footprints rather than use bare-IC footprints.
- **Decoupling:** bulk caps (C1/C2 at +5V, C3 at +3V3) are included for the printer/motor
  pulse loads; add per-module 100 nF decoupling at layout as standard practice.
- **Power sequencing constraint** (from `POWER_BUDGET.md`): firmware must keep printer / UV-C /
  heavy-motor phases sequential so peak 5V load stays within the regulator rating.
- This netlist is a **first-draft for verification**, not a released design. An electronics
  engineer must confirm pin mappings, footprints, and run ERC/DRC before fabrication.
