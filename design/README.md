# Design (Stage 3) — Blueprint export

Device design iteration exported from **Blueprint** (lite / single-strip variant).
This is the design-intent source that the hardware (`../hardware/`) and BOM (`../bom/`)
are derived from.

## Contents (`blueprint/`)
- `CONFIG.json` — full device configuration (components, parameters)
- `ELECTRICAL_CONNECTIONS.json` — wiring / net definitions
- `MECHANICAL_CONNECTIONS.json` — mechanical assembly relationships
- `PARTS.csv` — parts list with categories, quantities, costs, source URLs
- `GUIDE.md` — fabrication / wiring / bring-up / assembly checklist
- `VISUAL.png` — rendered layout

> A second, fuller Blueprint export (10P / larger variant) exists outside the repo at
> `~/Desktop/Sids Gdrive/urine_dipstick_analyzer_files (1)/`. Not imported here — this repo
> tracks the **lite** design. Import it if the project consolidates on that variant.
