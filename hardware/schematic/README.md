# Schematic — Urine Analyzer Lite (Design A)

`urine_analyzer_lite.kicad_sch` is a **machine-generated, ERC-validated** schematic produced
from the same netlist model as `../netlist/` (single source of truth = `config.h` master pin map).

## Files
- `gen_schematic.py` — generator. Imports `../netlist/gen_netlist.py` (the component/pin/net model).
- `urine_analyzer_lite.kicad_sch` — the schematic (KiCad 9/10, format 20250114).
- `urine_analyzer_lite_schematic.pdf` — rendered view (open without KiCad).
- `ERC_report.txt` — KiCad ERC output.

## Validation (done with KiCad 10.0.3 `kicad-cli`)
- **Netlist cross-check:** KiCad's exported netlist matches the intended model **39/39 nets, 0 mismatches**.
- **ERC:** **0 errors**, 59 warnings — all benign and expected:
  - `lib_symbol_issues (ual)` — symbols are *embedded* in the file (generic rectangles, one per
    component); the source library just isn't registered. Render fine.
  - `footprint_link_issues` — footprints are **placeholders**; the engineer assigns real ones.
  - `isolated_pin_label: VBUS` — expected single-node net (USB 5V input on the TP4056 module).

## How connectivity is represented
Each component is a generic rectangular symbol with named/numbered pins. Every pin carries a
**global label = its net name**, placed exactly on the pin's connection point. KiCad joins global
labels by name across the sheet, so the netlist is exact. There are intentionally **no drawn
wires** — this is a connection-by-label schematic, valid and ERC-clean, but visually it's a
net-label list rather than a hand-drawn ratsnest.

## What the engineer does next
1. Open in KiCad 9/10. Review nets against `../ENGINEERING_REVIEW.md` and `config.h`.
2. **Swap generic symbols for proper library symbols** where preferred, and **assign real
   footprints** (placeholders listed in `../netlist/NETLIST.md`).
3. Optionally redraw with wires for readability (connectivity won't change — it's label-driven).
4. Re-run ERC, then proceed to PCB layout → DRC → Gerbers (see `../netlist/README.md`).

> This is an AI-generated first draft for verification, not a released design. It is electrically
> correct per the model, but symbol/footprint choices and the physical design need engineer sign-off.

## Regenerate
```bash
python3 gen_schematic.py            # rewrites urine_analyzer_lite.kicad_sch
# then, with KiCad installed:
kicad-cli sch erc urine_analyzer_lite.kicad_sch
kicad-cli sch export pdf -o urine_analyzer_lite_schematic.pdf urine_analyzer_lite.kicad_sch
```
