# Urine Analyzer Lite — Project TODO

> **Legend:** ✅ Done &nbsp;|&nbsp; 🔲 Pending &nbsp;|&nbsp; 🔄 In Progress

---

## Hardware — PCB / Schematic

> ⚠️ STAGE 4 GATE: see `hardware/ENGINEERING_REVIEW.md` + `hardware/POWER_BUDGET.md`.
> The existing `.kicad_sch` is a graphical mock-up with NO netlist. config.h / Blueprint / BOM
> disagree on motor driver, I2C pins, motor/HX711/printer pins, display, and the 9V rail.
> Resolve all 🔴 items + sign off the master pin map before any layout.

- 🔲 **Engineer: resolve 🔴 items + approve master pin map (ENGINEERING_REVIEW §3)**
- 🔲 **Fix config.h: SCL≠GPIO22 (invalid on S3), printer RX off GPIO19 (USB), UV-C off GPIO3 (strap)**
- 🔲 **Add TCA9548A I2C mux + 3.3V regulator to BOM (two TCS34725 clash at 0x29; no 3V3 rail)**
- 🔲 **Decide display: ESP32-S3 cannot drive MIPI-DSI — pick SPI TFT / RGB / OLED / new host**
- ✅ Netlist generated from master pin map → `hardware/netlist/` (.net + NETLIST.md)
- ✅ Schematic regenerated + ERC-clean (0 errors), netlist 39/39 → `hardware/schematic/` (+ PDF)
- 🔲 Engineer: swap generic symbols for library parts + assign real footprints, re-run ERC
- 🔲 Engineer: import to Pcbnew → PCB layout → DRC → Gerbers
- 🔲 Open schematic in KiCad EDA and visually verify all nets
- 🔲 Assign real KiCad symbol library parts to each component
- 🔲 Add ERC (Electrical Rules Check) violations resolution
- 🔲 Design custom PCB layout in KiCad PCB editor
- 🔲 Add power planes (GND, 3V3, 5V)
- 🔲 Route high-current traces for motor and printer (≥1 mm width)
- 🔲 Add mounting holes (4× M3) aligned to chassis stand-offs
- 🔲 Run DRC (Design Rules Check) — target 0 errors
- 🔲 Export Gerber files and BOM for fabrication (JLCPCB / PCBWay)
- 🔲 Order 5× prototype PCBs

---

## Hardware — CAD / Mechanical

- ✅ OpenSCAD source file (`hardware/cad/main_chassis.scad`)
- 🔲 Render all modules to STL (`openscad -o part.stl main_chassis.scad -D 'part="chassis_base"'` etc.)
- 🔲 Review prints for dimensional accuracy against component datasheets
- 🔲 Verify ESP32-S3-DevKitC-1 footprint fits MCU tray (68.6 × 28.8 mm)
- 🔲 Verify CSN-A2 fits printer bracket (57.5 × 37 × 40 mm)
- 🔲 Test fit belt tensioner with 625ZZ idler bearing
- 🔲 Confirm limit switch bracket adjustability range ≥ 10 mm
- 🔲 Print optical chamber in black PLA — light-tight test with torch
- 🔲 Glue or press-fit frosted acrylic diffuser into chamber slot
- 🔲 Print dipstick tray — verify 6 mm strip fits without play
- 🔲 Print final chassis with PETG; install heat-set inserts
- 🔲 Add 2° draft angles to all vertical walls for injection-mould readiness

---

## Firmware

- ✅ `config.h` — all pin assignments and tunable constants
- ✅ `sensors.h` — TCS34725, ADS1115, SHT31, BH1750, HX711 drivers
- ✅ `motor.h` — N20 encoder-based motion control + homing
- ✅ `analysis.h` — HSV-based pad classification (10 analytes)
- ✅ `printer.h` — CSN-A2 ESC/POS thermal printer output
- ✅ `main.ino` — state machine: IDLE → HOMING → SCANNING → PRINTING → STERILIZING
- 🔲 Flash firmware to hardware and test boot
- 🔲 Calibrate HX711 scale factor with known weight
- 🔲 Calibrate TCS34725 against Spectralon white standard (update `CAL_R/G/B_WHITE`)
- 🔲 Calibrate `TICKS_PER_PAD` with physical dipstick (measure real pad pitch)
- 🔲 Validate HSV hue ranges in `analysis.h` using positive/negative reference strips
- 🔲 Implement display UI (LVGL or LovyanGFX on DSI LCD)
- 🔲 Add Bluetooth/Wi-Fi result upload (optional)
- 🔲 Implement OTA firmware update
- 🔲 Add watchdog timer and brownout detection
- 🔲 Write unit tests for `rgb_to_hsv()` and `classify_pad()`

---

## BOM / Procurement

- ✅ BOM CSV (`bom/bom.csv`) — 40 line items, estimated total ≈ $387 per unit
- 🔲 Obtain quotes from Indian distributors (Rhydo, Robocraze, Electronicscomp)
- 🔲 Source TCS34725 from Adafruit or equivalent (check availability)
- 🔲 Procure Labsphere Spectralon calibration standard (long lead time)
- 🔲 Verify CSN-A2 printer stock and 58mm paper availability locally
- 🔲 Confirm Waveshare 4.3in DSI LCD DSI compatibility with ESP32-S3
- 🔲 Bulk pricing target: < $250 per unit at 50-unit volume

---

## Integration & Testing

- 🔲 Power-on test: verify 3V3 and 5V rails under load
- 🔲 I2C scan — confirm all 5 devices at expected addresses
- 🔲 Motor homing test — both limit switches trigger correctly
- 🔲 Full scan cycle with blank dipstick — no crashes, 10 pads detected
- 🔲 Full scan cycle with positive control strip — correct analyte results
- 🔲 Thermal print output matches on-screen report
- 🔲 UV-C sterilization cycle runs for 10 s and shuts off
- 🔲 Weight sensor detects cup placement > 1 g threshold
- 🔲 Environmental envelope test: 15–35 °C, 20–80% RH

---

## Documentation

- ✅ Assembly guide template (`hardware/schematic/` + `GUIDE.md` in source data)
- 🔲 Write complete assembly guide with photos
- 🔲 Write calibration SOP (white standard → pad validation)
- 🔲 Write operator quick-start card (print on 58mm paper)
- 🔲 Add troubleshooting section (I2C errors, motor faults, print jams)
- 🔲 Create block diagram image for README

---

## Regulatory / Quality — Stage 0 Foundation (see `regulatory/`)

- ✅ Target Product Profile + Intended Use (`regulatory/00_...`)
- ✅ CDSCO classification & pathway — best-guess Class B (`regulatory/01_...`)
- ✅ Applicable standards matrix (`regulatory/02_...`)
- ✅ ISO 14971 risk management file — skeleton (`regulatory/03_...`)
- ✅ Preliminary FTO patent search — optics (`regulatory/04_...`)
- 🔲 **DECIDE: proprietary strips vs commercial strips** (gates scope)
- 🔲 **Confirm CDSCO class via regulatory consultant pre-submission**
- 🔲 **DECIDE: keep or drop UV-C sterilization** (IEC 62471 burden vs benefit)
- 🔲 Identify predicate device(s)
- 🔲 ISO 13485 QMS alignment checklist
- 🔲 Re-run FTO on Lens.org/Espacenet + check patent legal status/expiry
- 🔲 CE / 510(k) pathway assessment (export, later)
