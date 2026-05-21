# Schematic — Urine Analyzer Lite (Design A)

`urine_analyzer_lite.kicad_sch` is a **machine-generated, ERC-validated** schematic produced
from the same netlist model as `../netlist/` (single source of truth = `config.h` master pin map).

## Files
- `gen_schematic.py` — generator. Imports `../netlist/gen_netlist.py` (the component/pin/net model).
- `urine_analyzer_lite.kicad_sch` — the schematic (KiCad 9/10, format 20250114).
- `urine_analyzer_lite_schematic.pdf` — rendered view (open without KiCad).
- `ERC_report.txt` — KiCad ERC output.

## Validation (done with KiCad 10.0.3 `kicad-cli`)
- **Netlist cross-check:** KiCad's exported netlist matches the model **39/39 nets** by ref **and pad**.
- **ERC:** **0 errors**, ~18 warnings — all benign: `lib_symbol_issues (ual)` for the custom
  module symbols (embedded, render fine) and `isolated_pin_label: VBUS` (expected single-node
  USB input). Jellybean symbols + all footprints now resolve cleanly.

## Symbols & footprints
- **14 jellybean discretes** (R×5, C, C_Polarized×2, LED, Battery_Cell, Thermistor, SW_Push×3)
  use **real KiCad library symbols** (`Device:*`, `Switch:*`), embedded from KiCad's shared libs.
- **Modules + the MOSFET** use generic rectangular symbols (no stock symbol exists for dev-boards/
  breakouts). Their pins are numbered by **PCB pad** so schematic↔board align.
- **Every symbol has a real footprint** assigned (see `../footprints.py`), so "Update PCB from
  Schematic" carries footprints. Module footprints are 2.54mm pin headers — verify pin ORDER
  against each module's datasheet.

## How connectivity is represented
Every pin carries a **global label = its net name**, placed exactly on the pin's connection point.
KiCad joins global labels by name across the sheet, so the netlist is exact. There are
intentionally **no drawn wires** — a connection-by-label schematic, valid and ERC-clean, but
visually a net-label list rather than a hand-drawn ratsnest (the engineer can redraw with wires;
connectivity won't change).

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
