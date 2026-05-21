# PCB — Urine Analyzer Lite (Design A)

A **starting board** generated from the netlist model via KiCad's `pcbnew` Python API.
All 31 footprints are placed and net-assigned; the board is **not yet routed**.

## Files
- `build_pcb.py` — generator (run with KiCad's bundled Python; needs `pcbnew`).
- `urine_analyzer_lite.kicad_pcb` — the board (31 footprints, real footprints, nets assigned).
- `urine_analyzer_lite.kicad_pro` — project file (open this in KiCad).
- `urine_analyzer_lite_render_top.png` — 3D render (top).
- `DRC_report.txt` / `drc.json` — DRC output.

## Validation (KiCad 10.0.3)
- **Schematic parity: 0 mismatches** — the board's connectivity matches the schematic exactly.
- **104 unconnected items** — this is the **unrouted ratsnest** (expected; the engineer routes it).
- **214 DRC violations** — all are **placement-density cosmetics** from the auto-grid layout:
  `silk_over_copper`/`silk_overlap` (ref-text overlap), `courtyards_overlap`,
  `pth_inside_courtyard`, a few `clearance`/`solder_mask_bridge`. They disappear once parts are
  spread out and routed. **None are structural / netlist errors.**

## What the engineer does
1. Open the project in KiCad 10. **Confirm footprints** — modules are generic 2.54mm pin
   headers; verify each header's **pin ORDER against the module datasheet/silkscreen**
   (the auto-assignment uses the netlist order, see `footprints.py` + `../netlist/NETLIST.md`).
2. Re-place parts sensibly (optical chamber sensors together, printer/motor power near the
   regulator, keep UV-C/printer high-current away from sensor analog lines).
3. Add **power planes** (GND / +5V / +3V3), route — wide traces for motor/printer/UV-C per
   `../POWER_BUDGET.md`. Add mounting holes to the chassis stand-offs.
4. **DRC → 0**, then export Gerbers + drill + position:
   ```
   kicad-cli pcb export gerbers -o gerbers/ urine_analyzer_lite.kicad_pcb
   kicad-cli pcb export drill   -o gerbers/ urine_analyzer_lite.kicad_pcb
   ```

## Regenerate
```bash
/Applications/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 build_pcb.py
```

> Starting board for engineer verification, not a finished layout. Placement, routing, footprint
> confirmation (esp. module pin order), stackup, and DRC sign-off are the engineer's.
