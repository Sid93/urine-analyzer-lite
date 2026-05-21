# Urine Analyzer Lite

> Compact, automated urine dipstick reader by **Levram Lifesciences**.  
> Single-strip, N20-motor-driven, ESP32-S3 based with thermal print output.

---

## Overview

The Urine Analyzer Lite reads standard 10-pad reagent dipsticks using dual TCS34725 RGB color sensors and classifies results for 10 analytes. A compact N20 gear motor steps the strip under the optical head at controlled speed. Results print via an integrated CSN-A2 thermal printer.

**Key specs:**

| Parameter | Value |
|---|---|
| MCU | ESP32-S3-DevKitC-1 (Xtensa dual-core 240 MHz, 8 MB flash) |
| Sensors | TCS34725 ×2, SHT31, BH1750, ADS1115, HX711 |
| Display | 3.5" SPI TFT (ILI9488) + XPT2046 touch — see `hardware/ENGINEERING_REVIEW.md` |
| Motor | GA12-N20 6V 200RPM with Hall encoder + MX1508 H-bridge |
| Printer | CSN-A2 58mm thermal (ESC/POS) |
| Power | 3.7V 2000mAh LiPo → TP4056 USB-C charger → S13V25F5 5V regulator |
| Sterilization | 275nm UV-C LED (10s cycle post-scan) |
| Analytes | Leukocytes, Nitrites, Urobilinogen, Protein, pH, Blood, Specific Gravity, Ketones, Bilirubin, Glucose |
| Estimated BOM | ~$387 per unit (prototype); target <$250 at 50-unit volume |

---

## Repository Structure

```
urine-analyzer-lite/
├── hardware/
│   ├── schematic/
│   │   ├── gen_schematic.py          # KiCad schematic generator
│   │   └── urine_analyzer_lite.kicad_sch
│   └── cad/
│       └── main_chassis.scad         # OpenSCAD enclosure (all 3D-printed parts)
├── firmware/
│   └── main/
│       ├── main.ino                  # Arduino sketch (state machine)
│       ├── config.h                  # Pin map and tunable constants
│       ├── sensors.h                 # All sensor drivers
│       ├── motor.h                   # N20 motion control + homing
│       ├── analysis.h                # HSV pad classification (10 analytes)
│       └── printer.h                 # ESC/POS thermal print
├── bom/
│   └── bom.csv                       # Full bill of materials (~40 items)
├── TODO.md                           # Project checklist
└── README.md
```

---

## Hardware

### Schematic
Open in KiCad 7+:
```
File → Open → hardware/schematic/urine_analyzer_lite.kicad_sch
```
To regenerate after edits:
```bash
cd hardware/schematic && python3 gen_schematic.py
```

### CAD
Open in OpenSCAD ≥ 2021.01:
```
hardware/cad/main_chassis.scad
```
All 3D-printable parts are exported from one file. Render individual modules:
```
openscad -o chassis_base.stl main_chassis.scad
```

**Print settings:**

| Part | Material | Infill | Layer |
|---|---|---|---|
| Chassis base, MCU tray, dipstick tray | PLA | 20% | 0.2 mm |
| Optical chamber, UV-C shield | Black PLA | 100% | 0.1 mm |
| Sensor mounts, printer bracket, belt parts | PETG | 30% | 0.2 mm |

---

## Firmware

### Requirements
- Arduino IDE ≥ 2.3 with ESP32 board package ≥ 2.0.14
- Board: **ESP32S3 Dev Module** — Flash: 8MB, PSRAM: OPI, USB: Hardware CDC

### Libraries (Arduino Library Manager)
```
Adafruit TCS34725      >= 1.4.2
Adafruit ADS1X15       >= 2.5.0
Adafruit SHT31         >= 2.2.2
BH1750 by Christopher Laws >= 1.3.0
HX711 by bogde         >= 0.7.5
```

### Flash
1. Open `firmware/main/main.ino` in Arduino IDE  
2. Select board and port  
3. Upload

### Calibration (required before first use)
1. **White standard** — place Spectralon pad under optical head; record R/G/B values in `config.h` (`CAL_R/G/B_WHITE`)
2. **Scale** — place known weight on scale platform; adjust `scale.set_scale()` factor in `sensors.h`
3. **Motor steps** — measure real pad pitch with calipers; adjust `TICKS_PER_PAD` in `config.h`
4. **Hue ranges** — run known positive/negative strips; refine `PAD_TABLE[]` in `analysis.h`

---

## Operation

1. Insert dipstick tray with strip face-up
2. Place sample cup on weight sensor (minimum 1 g detected)
3. Press scan button
4. Device homes, steps across all 10 pads, classifies, prints report
5. UV-C sterilization cycle runs automatically (10 s)
6. Remove strip; device returns to IDLE

---

## Bill of Materials

See [`bom/bom.csv`](bom/bom.csv) — estimated prototype total: **$387 USD**.

---

## License

Hardware and firmware © Levram Lifesciences. All rights reserved.  
*For clinical use by qualified personnel only.*
