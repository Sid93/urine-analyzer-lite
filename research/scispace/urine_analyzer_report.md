# Manufacturing a Benchtop Urine Dipstick Analyzer (2P & 10P) for the Indian Market
## A Comprehensive Technical, Manufacturing & Commercial Guide

**Prepared for:** Levram Life Sciences  
**Date:** May 2026  
**Benchmarks:** Siemens Clinitek Series | Mission Urine Analyzers  
**Classification:** Confidential – Internal R&D & Business Development Document

---

## Table of Contents

1. Executive Summary
2. Technology Overview & Principles
3. Strip Chemistry – 2P and 10P Parameters
4. Optical & Electronic System Design
5. Mechanical Design & Housing
6. Bill of Materials (BOM) with Estimated Costs
7. Manufacturing Process – Step by Step
8. Calibration & Quality Control
9. Infrastructure & Equipment Required
10. Regulatory Pathway in India (CDSCO / MDR 2017)
11. Indian Market Analysis & Competitive Landscape
12. Go-to-Market Strategy
13. Cost of Goods & Pricing Strategy
14. References

---

## 1. Executive Summary

Urinalysis is one of the most frequently ordered diagnostic tests globally, serving as a front-line screening tool for urinary tract infections (UTIs), diabetes, kidney disease, liver disorders, and metabolic conditions. In India, the urinalysis market is expanding rapidly, driven by rising diabetes and chronic kidney disease (CKD) prevalence, expansion of diagnostic laboratories, and the government's Ayushman Bharat program, which has accelerated diagnostics penetration into Tier 2, 3, and rural markets.

The current benchtop urine analyzer market in India is dominated by imported instruments from Siemens (Clinitek series), Mission Diagnostics, Roche (Cobas), and Dirui. These instruments are priced between ₹50,000–₹2,50,000 and rely on expensive proprietary reagent strips. There is a significant unmet need for a high-quality, economical, India-manufactured benchtop urine dipstick analyzer that can compete on accuracy, reliability, and after-sales service while offering strips at a lower cost.

This report provides a complete technical and commercial blueprint for Levram Life Sciences to develop, manufacture, and commercialize a 2-parameter (2P) and 10-parameter (10P) benchtop urine dipstick analyzer. The product leverages proven reflectance photometry technology, commercially available electronic components, and a modular design philosophy to achieve a target instrument manufacturing cost of ₹8,000–₹14,000 (2P) and ₹18,000–₹28,000 (10P), enabling retail pricing of ₹25,000–₹35,000 (2P) and ₹55,000–₹80,000 (10P) — well below the Siemens and Mission benchmarks.

---

## 2. Technology Overview & Principles

### 2.1 The Measurement Principle: Reflectance Photometry

Benchtop urine dipstick analyzers operate on the principle of **diffuse reflectance photometry**. When a urine dipstick is dipped into a urine sample and removed, the reagent pads undergo colorimetric reactions proportional to the concentration of the analyte. The analyzer illuminates each reagent pad with light of a defined wavelength and measures the intensity of light reflected back from the pad surface. The degree of color change on the pad alters the reflectance, which is then converted to a semiquantitative result.

The fundamental relationship is described by the **Kubelka-Munk (K-M) equation**:

```
F(R) = (1 - R)² / 2R = K/S
```

Where:
- **R** = measured reflectance (ratio of reflected to incident light)
- **K** = absorption coefficient of the colored product
- **S** = scattering coefficient of the pad matrix
- **F(R)** = K-M remission function, linearly related to analyte concentration

In practice, instruments measure a **reflectance ratio** (sample pad reflectance vs. reference pad or direct light channel) and apply a calibration curve to map the ratio to a semiquantitative category (e.g., Negative / Trace / 1+ / 2+ / 3+) or a numerical concentration range.

### 2.2 Why Reflectance Photometry is Preferred

| Feature | Reflectance Photometry | Transmission Photometry |
|---|---|---|
| Works with opaque matrices | Yes | No |
| Suitable for dry chemistry | Yes | No |
| Low-cost implementation | Yes | Moderate |
| Robust to strip-to-strip variation | Moderate | Low |
| Used in Siemens Clinitek | Yes | — |

### 2.3 Optical Architecture Options

Three main optical architectures are used in commercial and research analyzers:

**Architecture A – Direct LED-to-Photodetector (Single Point)**
- Simplest design; LED illuminates pad at fixed angle (typically 45°)
- Photodetector at complementary angle collects reflected light
- Used in low-cost portable readers
- Sensitive to strip placement variation

**Architecture B – Optical Fiber Bundle (Preferred for Benchtop)**
- LED light is conducted to the measurement zone via illumination fiber bundle
- Reflected light is collected by a separate detection fiber bundle
- Greatly reduces sensitivity to ambient light and strip placement
- Used in commercial benchtop analyzers including Siemens Clinitek 50/100
- Recommended for Levram's design

**Architecture C – Image Sensor / Camera Based**
- CMOS/CCD camera captures full-color image of all pads simultaneously
- RGB or HSV analysis via embedded processor
- Higher cost; used in high-throughput analyzers
- Not recommended for first-generation economical product

### 2.4 Multispectral Illumination

Different reagent pads absorb at different wavelengths. A single white LED is insufficient for optimal signal-to-noise across all 10 parameters. The solution is **tri-chromatic or multispectral illumination**:

| LED Color | Wavelength | Target Analytes |
|---|---|---|
| Green | 525–565 nm | Hemoglobin, Bilirubin, Urobilinogen |
| Red/Orange | 620–660 nm | Glucose, Protein, Leukocytes |
| Blue | 430–470 nm | Nitrite, pH |
| Infrared | 850 nm | Specific Gravity (reference) |

The analyzer cycles LEDs sequentially (or uses optical filters) and records the photodetector response for each wavelength per pad. This enables accurate discrimination across all analytes.

### 2.5 Signal Processing Chain

```
Urine Strip → LED Illumination → Pad Reflectance → Photodetector → 
Transimpedance Amplifier → ADC → MCU (Dark Subtraction + Reference 
Ratioing + Temperature Compensation) → Calibration Curve Lookup → 
Semiquantitative Result → Display / Print / LIS Export
```

---

## 3. Strip Chemistry – 2P and 10P Parameters

### 3.1 The 2-Parameter Strip (2P)

The 2P strip is designed for high-volume, rapid screening — primarily for glucose and protein, the two most commonly screened analytes in India for diabetes monitoring and kidney disease screening.

| Parameter | Reagent Chemistry | Color Change | Detection Range |
|---|---|---|---|
| **Glucose** | Glucose oxidase / peroxidase / chromogen (e.g., tetramethylbenzidine, TMB) | Yellow → Green → Blue | Negative to ≥2000 mg/dL |
| **Protein** | Tetrabromophenol blue (TBPB) with citrate buffer (protein error of indicators) | Yellow → Blue-Green | Negative to ≥500 mg/dL |

**Strip Construction (2P):**
- Polystyrene backing strip: 5 mm wide × 70–75 mm long
- Two reagent pads (each ~5 × 5 mm), separated by 3–4 mm
- One reference/blank pad (white cellulose) for background correction
- Pads are cellulose fiber matrices impregnated with reagents and dried

### 3.2 The 10-Parameter Strip (10P)

The 10P strip is the standard clinical tool for comprehensive urinalysis. It measures:

| # | Parameter | Reagent Chemistry | Color Range | Clinical Significance |
|---|---|---|---|---|
| 1 | **Glucose** | Glucose oxidase + peroxidase + TMB | Yellow → Green → Blue | Diabetes, renal glycosuria |
| 2 | **Protein** | Tetrabromophenol blue (TBPB), citrate buffer | Yellow → Blue-green | Nephritis, nephrotic syndrome |
| 3 | **pH** | Methyl red + bromothymol blue | Orange → Yellow → Green → Blue | Acid-base disorders, UTI |
| 4 | **Specific Gravity** | Bromothymol blue + poly(methyl vinyl ether/maleic acid) | Blue → Yellow-green | Hydration, renal concentration |
| 5 | **Ketones** | Sodium nitroprusside + glycine (Legal's reaction) | Buff → Maroon | Diabetic ketoacidosis, starvation |
| 6 | **Bilirubin** | 2,4-Dichloroaniline diazonium salt | Buff → Tan-Brown | Liver disease, biliary obstruction |
| 7 | **Urobilinogen** | p-Dimethylaminobenzaldehyde (Ehrlich's reagent) | Colorless → Pink-Red | Hemolytic anemia, liver disease |
| 8 | **Blood/Hemoglobin** | Tetramethylbenzidine (TMB) + peroxidase | Yellow → Green → Blue | Hematuria, hemoglobinuria |
| 9 | **Nitrite** | Griess reaction (sulfanilamide + NED) | White → Pink | Bacterial UTI (gram-negative) |
| 10 | **Leukocytes** | Indoxyl ester + diazonium salt (esterase reaction) | Buff → Purple | UTI, pyuria |

### 3.3 Strip Procurement Strategy for India

**Option A – Source Finished Strips (Recommended for Phase 1):**
- Source OEM strips from Chinese manufacturers (e.g., Dirui, URIT, Analyticon)
- Validate strip-analyzer compatibility with your optical system
- Cost: ₹3–₹8 per strip (10P), ₹1.5–₹3 per strip (2P) at bulk volumes
- Rebrand under Levram label (check regulatory requirements for strip registration)

**Option B – Manufacture Strips In-House (Phase 2/3):**
- Requires reagent chemistry expertise, impregnation equipment, and lamination machinery
- Capital investment: ₹40–₹80 lakh for strip manufacturing line
- Enables full cost control and margin maximization
- Requires separate CDSCO registration for the strip as an IVD reagent

**Key Strip Suppliers (India-compatible):**
- Dirui Industrial Co., Ltd. (China) – widely validated
- URIT Medical Electronic Co. (China) – cost-effective
- Analyticon Biotechnologies (Germany) – premium quality
- Erba Mannheim (Czech Republic/India distribution)
- Tulip Diagnostics (India) – domestic option

---

## 4. Optical & Electronic System Design

### 4.1 Optical Module Design

#### LED Selection

| LED | Wavelength | Part Example | Cost (INR) |
|---|---|---|---|
| Green LED | 525 nm | Osram LT CPDP | ₹8–₹15 |
| Red LED | 660 nm | Vishay VLCS5830 | ₹8–₹15 |
| Blue LED | 450 nm | Cree C503B-BAS | ₹10–₹18 |
| IR LED | 850 nm | Osram SFH 4545 | ₹8–₹12 |
| White LED (reference) | Broadband | Nichia NSPW500GS | ₹5–₹10 |

- LEDs are driven by constant-current drivers (e.g., Texas Instruments OPT101 or discrete BJT circuits)
- PWM control via MCU timer allows intensity adjustment and sequential switching
- LED lifetime: >100,000 hours — essentially maintenance-free

#### Photodetector Selection

| Component | Type | Part Example | Cost (INR) |
|---|---|---|---|
| Primary detector | Silicon photodiode | Hamamatsu S1087-01 | ₹80–₹150 |
| Reference detector | Silicon photodiode | Hamamatsu S1087 | ₹80–₹150 |
| Optional: array | TSL2591 light-to-digital | AMS TSL2591 | ₹60–₹100 |

**Recommended configuration:**
- Two photodiodes: one for reflected light (measurement), one for direct/incident light (reference)
- Ratiometric measurement: R_measured / R_reference eliminates LED intensity drift
- Optical bandpass filters (10 nm FWHM) placed in front of detectors for wavelength selectivity

#### Optical Fiber Bundle

- **Material:** Plastic optical fiber (POF), PMMA core, 0.5–1.0 mm diameter
- **Configuration:** Bifurcated bundle — one arm to LED, one arm to photodetector, common end at measurement zone
- **Numerical Aperture:** 0.5 NA for maximum light collection
- **Length:** 50–100 mm
- **Cost:** ₹200–₹500 per bundle (custom order, Chinese suppliers)
- Fiber bundles eliminate alignment sensitivity and ambient light interference

#### Optical Path Geometry

```
[LED Array] → [Collimating Lens] → [Illumination Fiber Bundle]
                                              ↓
                                    [Strip Measurement Zone]
                                              ↓
                               [Detection Fiber Bundle] → [Optical Filter] → [Photodetector]
                                              ↓
                               [Reference Fiber] → [Reference Photodetector]
```

### 4.2 Analog Front-End Circuit

#### Transimpedance Amplifier (TIA)

The photodiode generates a current proportional to incident light. A TIA converts this to a measurable voltage:

```
V_out = I_photo × R_feedback
```

- **Op-Amp:** Texas Instruments OPA2134 (low noise, low offset) or OPA2340
- **Feedback resistor:** 1–10 MΩ (sets gain and bandwidth)
- **Feedback capacitor:** 1–10 pF (stability compensation)
- **Power supply:** ±5V or single 3.3V with rail-to-rail op-amp
- **Cost per TIA stage:** ₹25–₹60

#### Signal Conditioning

- Low-pass filter (RC, fc ~100 Hz) to remove high-frequency noise
- Instrumentation amplifier for differential measurement where needed
- Voltage reference: **Texas Instruments REF3030** or **LM4132A-3.0** (3.0V, 0.05% accuracy) for ADC reference stability

#### Analog-to-Digital Conversion

| Parameter | Specification |
|---|---|
| Resolution | 16-bit (preferred) or 12-bit minimum |
| Sampling rate | 1–10 ksps (more than sufficient) |
| Input range | 0–3.3V or 0–5V |
| Channels | 8–16 (for multi-LED, multi-detector) |
| Part example | ADS1115 (16-bit, I2C, ₹80–₹120) or STM32 internal 12-bit ADC |

### 4.3 Microcontroller Unit (MCU)

**Recommended MCU: STM32F103C8T6 (Blue Pill) or STM32F407VGT6**

| Feature | STM32F103 (2P model) | STM32F407 (10P model) |
|---|---|---|
| Core | ARM Cortex-M3, 72 MHz | ARM Cortex-M4, 168 MHz |
| Flash | 64 KB | 1 MB |
| RAM | 20 KB | 192 KB |
| ADC | 12-bit, 10 channels | 12-bit, 24 channels |
| UART/USB | Yes | Yes + USB OTG |
| Cost (INR) | ₹120–₹200 | ₹350–₹600 |
| SPI/I2C | Yes | Yes |

**MCU Firmware Functions:**
1. LED sequential switching via GPIO/PWM timers
2. ADC sampling with averaging (16–64 samples per reading)
3. Dark current subtraction (reading with LEDs off)
4. Ratiometric calculation (sample/reference channels)
5. Temperature compensation using NTC thermistor data
6. Calibration curve lookup (stored in flash as polynomial coefficients or lookup tables)
7. Result classification to semiquantitative categories
8. UART/USB communication to display module or PC
9. Strip detection via IR sensor or mechanical switch
10. Self-test and error flagging routines

### 4.4 Display & User Interface

**2P Model:**
- 2.4" TFT LCD (ILI9341 driver, SPI interface) — ₹250–₹400
- 4 tactile buttons (Start, Print, Menu, Power)
- LED status indicators (Ready, Error, Processing)

**10P Model:**
- 3.5" or 4.3" TFT LCD with touch (ILI9488 or RA8875 driver) — ₹400–₹700
- On-screen keyboard for patient ID entry
- Optional: thermal printer integration (58mm paper, Bluetooth or serial) — ₹800–₹1,500

### 4.5 Power Supply

- Input: 100–240V AC, 50/60 Hz (India standard)
- SMPS module: 5V/2A + 12V/1A output — ₹200–₹400
- Onboard 3.3V LDO regulator (AMS1117-3.3) for MCU and analog circuits
- Optional Li-ion battery backup (18650, 2000 mAh) for portable use — ₹300–₹600
- Fuse + EMI filter on AC input for safety compliance

### 4.6 Communication Interfaces

| Interface | Purpose | Implementation |
|---|---|---|
| USB Type-B | PC connectivity, data export | CH340G USB-UART, ₹20–₹40 |
| RS-232 | LIS/HIS connectivity | MAX232 level shifter, ₹15–₹25 |
| Bluetooth 4.0 | Wireless data to mobile app | HC-05 or HM-10 module, ₹80–₹150 |
| SD Card | Local result storage | SPI SD card slot, ₹30–₹60 |
| Optional: WiFi | Cloud connectivity | ESP8266/ESP32, ₹80–₹200 |

---

## 5. Mechanical Design & Housing

### 5.1 Housing Design Principles

The housing must:
- Protect optical components from ambient light contamination
- Allow easy strip insertion and removal
- Be easy to clean (smooth surfaces, no crevices)
- Look professional and clinical
- Be manufacturable in India via injection molding or CNC

**Recommended Material:** ABS plastic (Acrylonitrile Butadiene Styrene)
- Medical-grade, UV-resistant, easy to injection mold
- Available in white/off-white for clinical aesthetic
- Cost: ₹800–₹2,000 per housing (injection molded, 500+ units)

### 5.2 Key Mechanical Subsystems

#### Strip Insertion Channel
- A guided channel (slot) that positions the strip precisely under the optical head
- Tolerance: ±0.2 mm lateral, ±0.5 mm longitudinal
- Strip detection: IR break-beam sensor or mechanical microswitch triggers measurement sequence
- For 10P: motorized strip transport (small DC gearmotor, ₹150–₹300) for automated advancement

#### Optical Head Assembly
- Black anodized aluminum optical block houses fiber terminations, LED holders, and filter slots
- Machined to ±0.05 mm tolerance for repeatable fiber-to-strip distance (typically 2–5 mm)
- Black felt/foam light seal around strip channel eliminates stray light

#### Thermal Management
- NTC thermistor (10 kΩ) mounted near optical block for temperature logging
- Passive ventilation slots; no active cooling needed for low-power LED system
- Operating range: 15–35°C (standard lab environment)

### 5.3 Dimensional Targets

| Model | Dimensions (L × W × H) | Weight |
|---|---|---|
| 2P Analyzer | 180 × 120 × 80 mm | ~600 g |
| 10P Analyzer | 280 × 180 × 120 mm | ~1.2 kg |

### 5.4 Industrial Design Reference

Benchmark the Siemens Clinitek Status+ (handheld) and Mission U120 for:
- Strip channel design
- Display placement
- Button ergonomics
- Cable routing

---

## 6. Bill of Materials (BOM) with Estimated Costs

### 6.1 BOM – 2-Parameter (2P) Analyzer

| Category | Component | Qty | Unit Cost (INR) | Total (INR) |
|---|---|---|---|---|
| **Optical** | Green LED 525nm | 2 | ₹12 | ₹24 |
| | Red LED 660nm | 2 | ₹12 | ₹24 |
| | Silicon Photodiode (measurement) | 1 | ₹120 | ₹120 |
| | Silicon Photodiode (reference) | 1 | ₹120 | ₹120 |
| | Optical fiber bundle (bifurcated) | 1 | ₹350 | ₹350 |
| | Optical bandpass filters (2 wavelengths) | 2 | ₹200 | ₹400 |
| | Optical block (machined aluminum) | 1 | ₹600 | ₹600 |
| **Electronics** | STM32F103C8T6 MCU | 1 | ₹160 | ₹160 |
| | OPA2134 Op-Amp (TIA) | 2 | ₹45 | ₹90 |
| | ADS1115 16-bit ADC | 1 | ₹100 | ₹100 |
| | LM4132A voltage reference | 1 | ₹35 | ₹35 |
| | NTC Thermistor 10kΩ | 1 | ₹10 | ₹10 |
| | PCB (custom, 2-layer, 100×80mm) | 1 | ₹250 | ₹250 |
| | Passive components (R, C, L) | Lot | — | ₹150 |
| | Connectors, headers | Lot | — | ₹80 |
| | USB-UART (CH340G) | 1 | ₹30 | ₹30 |
| **Display/UI** | 2.4" TFT LCD (ILI9341) | 1 | ₹320 | ₹320 |
| | Tactile buttons × 4 | 4 | ₹5 | ₹20 |
| | LED indicators × 3 | 3 | ₹3 | ₹9 |
| **Power** | SMPS 5V/2A module | 1 | ₹280 | ₹280 |
| | AMS1117-3.3 LDO | 2 | ₹8 | ₹16 |
| | Power connector, fuse, switch | Lot | — | ₹60 |
| **Mechanical** | ABS housing (injection molded) | 1 | ₹900 | ₹900 |
| | Strip channel guide (machined) | 1 | ₹200 | ₹200 |
| | IR strip sensor | 1 | ₹25 | ₹25 |
| | Screws, standoffs, labels | Lot | — | ₹80 |
| **Miscellaneous** | Thermal pad, foam seals | Lot | — | ₹50 |
| | Packaging (box, foam, manual) | 1 | ₹180 | ₹180 |
| | **TOTAL BOM (2P)** | | | **≈ ₹4,283** |
| | Assembly labor (2 hours @ ₹200/hr) | | | ₹400 |
| | Testing & QC | | | ₹300 |
| | **Total COGS (2P)** | | | **≈ ₹4,983** |

> **Note:** At 1,000 unit production volumes, economies of scale reduce BOM by ~15–20%, bringing COGS to approximately ₹4,200–₹4,500 per unit.

### 6.2 BOM – 10-Parameter (10P) Analyzer

| Category | Component | Qty | Unit Cost (INR) | Total (INR) |
|---|---|---|---|---|
| **Optical** | Multi-LED array (Green, Red, Blue, IR) | 4 | ₹14 | ₹56 |
| | Silicon Photodiodes (measurement + reference) | 4 | ₹120 | ₹480 |
| | Optical fiber bundles (10 channels) | 10 | ₹400 | ₹4,000 |
| | Optical bandpass filters (4 wavelengths) | 4 | ₹220 | ₹880 |
| | Precision optical block (machined) | 1 | ₹1,800 | ₹1,800 |
| | LED driver ICs (constant current) | 2 | ₹60 | ₹120 |
| **Electronics** | STM32F407VGT6 MCU | 1 | ₹500 | ₹500 |
| | OPA2134 Op-Amp (TIA ×4 stages) | 4 | ₹45 | ₹180 |
| | ADS1115 16-bit ADC ×2 | 2 | ₹100 | ₹200 |
| | REF3030 voltage reference | 1 | ₹50 | ₹50 |
| | NTC Thermistor | 2 | ₹10 | ₹20 |
| | Custom PCB (4-layer, 150×120mm) | 1 | ₹600 | ₹600 |
| | Passive components (R, C, L) | Lot | — | ₹350 |
| | Connectors, FFC cables | Lot | — | ₹200 |
| | USB-UART + RS232 (CH340G + MAX232) | 1 | ₹60 | ₹60 |
| | Bluetooth module (HC-05) | 1 | ₹120 | ₹120 |
| | SD card module | 1 | ₹50 | ₹50 |
| **Display/UI** | 4.3" TFT LCD touch (ILI9488) | 1 | ₹650 | ₹650 |
| | Thermal printer module (58mm) | 1 | ₹1,200 | ₹1,200 |
| | Tactile buttons × 6 | 6 | ₹5 | ₹30 |
| **Power** | SMPS 5V/2A + 12V/1A | 1 | ₹380 | ₹380 |
| | AMS1117 LDO regulators | 3 | ₹8 | ₹24 |
| | Battery backup (Li-ion 18650 + charger IC) | 1 | ₹550 | ₹550 |
| **Mechanical** | ABS housing (larger, injection molded) | 1 | ₹1,800 | ₹1,800 |
| | Strip transport motor + mechanism | 1 | ₹450 | ₹450 |
| | Strip channel + guides | 1 | ₹350 | ₹350 |
| | IR sensors × 2 | 2 | ₹25 | ₹50 |
| | Screws, standoffs, labels, cable ties | Lot | — | ₹150 |
| **Miscellaneous** | Thermal pads, foam seals, light baffles | Lot | — | ₹120 |
| | Packaging (box, foam, accessories, manual) | 1 | ₹350 | ₹350 |
| | **TOTAL BOM (10P)** | | | **≈ ₹15,520** |
| | Assembly labor (4 hours @ ₹200/hr) | | | ₹800 |
| | Testing & QC (extended) | | | ₹600 |
| | **Total COGS (10P)** | | | **≈ ₹16,920** |

> **Note:** At 500+ unit volumes, COGS for 10P reduces to approximately ₹14,000–₹15,500 per unit.

---

## 7. Manufacturing Process – Step by Step

### 7.1 Phase 1: PCB Design & Fabrication

**Step 1.1 – Schematic Design**
- Use KiCad (free) or Altium Designer for schematic capture
- Design analog front-end, MCU connections, power rails, LED drivers
- Include test points on all critical nodes

**Step 1.2 – PCB Layout**
- Separate analog and digital ground planes with single-point connection
- Keep TIA circuits away from digital switching noise
- Place decoupling capacitors (100 nF) at every IC power pin
- Use 4-layer board for 10P model (signal, ground, power, signal)
- Export Gerber files

**Step 1.3 – PCB Fabrication & Assembly**
- Send Gerbers to PCB manufacturer: JLCPCB, PCBWay (China) or Sunshine Circuits (India)
- Cost: ₹150–₹600 per board at 100-piece MOQ
- SMT assembly: use JLCPCB's SMT service or local EMS in Pune/Bangalore
- Through-hole components: hand-soldered in-house

**Step 1.4 – PCB Testing**
- In-circuit test (ICT) with bed-of-nails fixture for production
- Functional test: verify power rails, MCU boot, ADC readings, LED switching

### 7.2 Phase 2: Optical Module Assembly

**Step 2.1 – Optical Block Machining**
- CNC machine optical block from black anodized aluminum (6061-T6)
- Drill fiber holes to ±0.05 mm tolerance
- Tap LED mounting holes (M2 threads)
- Source from local machine shops (Pune, Coimbatore, Ludhiana) — ₹600–₹1,800 per block

**Step 2.2 – Fiber Bundle Preparation**
- Cut fiber bundles to required length
- Polish fiber ends with 1 µm lapping film (critical for light transmission efficiency)
- Epoxy fiber ends into SMA or custom ferrules
- Test transmission with optical power meter

**Step 2.3 – LED & Filter Installation**
- Press-fit or epoxy LEDs into optical block
- Install bandpass filters in filter slots with optical cement
- Connect LED leads to PCB via flexible wire or ZIF connector

**Step 2.4 – Photodetector Mounting**
- Mount photodiodes on PCB with precise alignment to fiber detection ports
- Apply optical coupling gel (refractive index matching) between fiber end and photodiode active area
- Shield with black felt to prevent cross-talk

**Step 2.5 – Optical Module Characterization**
- Measure dark current (LEDs off): should be <1 nA
- Measure signal-to-noise ratio with reference white tile
- Verify linearity with neutral density filters (0.1–2.0 OD range)
- Record baseline reflectance values for calibration

### 7.3 Phase 3: Mechanical Assembly

**Step 3.1 – Housing Preparation**
- Inspect injection-molded housing for warpage, sink marks, flash
- Apply EMI shielding paint inside housing if required for regulatory compliance
- Install rubber feet, cable grommets, and ventilation grilles

**Step 3.2 – Strip Channel Assembly**
- Install strip channel guide with alignment pins
- Mount IR strip-detection sensor with precise positioning
- Test strip insertion/detection with reference strips

**Step 3.3 – Main Assembly**
- Mount PCB to housing with M3 standoffs (4 points)
- Mount optical module to housing with alignment pins and 4 screws
- Route and secure all cables with cable ties
- Install display module with foam tape + screws
- Install SMPS with strain relief on AC cable
- Install front panel buttons and status LEDs

**Step 3.4 – Final Mechanical Inspection**
- Check all screw torques
- Verify strip channel alignment with optical head
- Inspect for light leaks (test in darkened room with LED on)
- Verify all external ports are accessible and labeled

### 7.4 Phase 4: Firmware Development & Loading

**Step 4.1 – Firmware Architecture**
```
main.c
├── init.c          (hardware initialization)
├── led_control.c   (LED PWM/GPIO driver)
├── adc_driver.c    (ADC sampling, averaging, DMA)
├── optical.c       (dark subtraction, ratiometry)
├── temp_comp.c     (temperature compensation)
├── calibration.c   (curve storage, lookup)
├── classify.c      (result classification to categories)
├── display.c       (LCD driver, UI state machine)
├── comm.c          (USB, Bluetooth, RS232)
├── storage.c       (SD card, result logging)
└── selftest.c      (startup diagnostics)
```

**Step 4.2 – Calibration Data Embedding**
- Calibration coefficients (polynomial or lookup table) for each analyte/wavelength combination
- Derived from validation experiments with known concentration standards
- Stored in MCU flash as const arrays

**Step 4.3 – Firmware Loading**
- Use ST-Link V2 programmer (₹300–₹600) via SWD interface
- Production programming: gang programmer for batch flashing
- Lock flash memory after programming to protect IP

### 7.5 Phase 5: Calibration & Validation

*(See Section 8 for detailed calibration protocol)*

### 7.6 Phase 6: Final QC & Packaging

- Run full self-test routine
- Test with 3 known-concentration urine control samples (Negative, Low, High)
- Verify all 10 parameters (10P model) or 2 parameters (2P model) against expected results
- Record serial number, lot number, calibration date in instrument memory
- Apply CE/BIS labels, serial number sticker
- Pack with power adapter, USB cable, quick-start guide, user manual, 5 test strips

---

## 8. Calibration & Quality Control

### 8.1 Calibration Philosophy

Calibration maps the raw reflectance signal (R) to a semiquantitative result category. It must account for:
1. **Lot-to-lot strip variation** (different reagent batches absorb differently)
2. **Instrument-to-instrument optical variation** (LED intensity, fiber transmission)
3. **Temperature effects** (reaction rates change with temperature)
4. **Aging effects** (LED intensity drift over time)

### 8.2 Factory Calibration Protocol

**Step 1 – White Reference Calibration**
- Measure reflectance of a NIST-traceable white ceramic tile (R = 100%)
- Set this as the 100% reflectance baseline for all channels
- Store as factory calibration constant in MCU flash

**Step 2 – Dark Reference**
- Measure photodetector output with all LEDs off
- Store as dark offset; subtract from all subsequent measurements

**Step 3 – Multilevel Calibration with Aqueous Standards**
- Prepare 5–7 concentration levels for each analyte (using certified reference materials)
- Measure reflectance at each level
- Fit polynomial calibration curve: R = f(concentration)
- Store polynomial coefficients in MCU flash

**Step 4 – Strip Lot Calibration**
- Each new lot of dipstick strips comes with a calibration code (printed on bottle or barcode)
- Operator scans/enters lot code; instrument loads appropriate calibration offset
- This compensates for inter-lot reagent variation (critical for accuracy)

**Step 5 – Temperature Compensation**
- Measure instrument response at 15°C, 25°C, 35°C
- Derive linear temperature correction coefficients for each analyte
- Apply in firmware: Corrected_R = Measured_R × (1 + α × (T – T_ref))

### 8.3 Field Calibration (User-Level)

- **Daily QC:** Run one Negative control and one Positive control strip each morning
- **Lot calibration:** Enter new lot code when opening a new strip bottle
- **Annual calibration:** Factory service or calibration kit with certified standards

### 8.4 Quality Control Program

| QC Level | Frequency | Method | Pass Criteria |
|---|---|---|---|
| Daily QC | Every day of use | Negative + Positive control strips | All parameters within ±1 grade |
| Lot-to-Lot | Each new strip lot | Run 3 controls from new lot | CV <10% vs. previous lot |
| Linearity | Monthly | 5-point dilution series (glucose, protein) | R² > 0.99 |
| Precision | Weekly | Repeat 10× on same control | CV <5% |
| Accuracy | Quarterly | Compare vs. reference lab (Cobas/Clinitek) | ≥90% agreement |
| Instrument QC | Annual | Full factory recalibration | Per manufacturer specs |

### 8.5 Analytical Performance Specifications (Target)

| Parameter | Sensitivity | Specificity | Precision (CV) |
|---|---|---|---|
| Glucose | ≥95% | ≥90% | <8% |
| Protein | ≥90% | ≥85% | <10% |
| Blood | ≥95% | ≥88% | <8% |
| Nitrite | ≥90% | ≥95% | <10% |
| Leukocytes | ≥85% | ≥90% | <12% |
| pH | ±0.5 pH units | — | <5% |
| Specific Gravity | ±0.005 SG units | — | <5% |

---

## 9. Infrastructure & Equipment Required

### 9.1 Manufacturing Facility

**Minimum Space Requirements:**
- Total area: 500–800 sq ft (can be expanded as production scales)
- Clean assembly area: 200 sq ft (dust-controlled, positive pressure preferred)
- PCB storage and components area: 100 sq ft
- Testing & QC lab: 150 sq ft
- Packaging & dispatch: 100 sq ft

**Environmental Controls:**
- Temperature: 20–25°C (air conditioning)
- Humidity: 40–60% RH (dehumidifier if needed)
- ESD protection: anti-static flooring, wrist straps, ESD mats

### 9.2 Equipment List

| Equipment | Purpose | Estimated Cost (INR) |
|---|---|---|
| Soldering station (Hakko FX-888D or equivalent) | PCB assembly | ₹8,000–₹15,000 |
| Hot air rework station | SMD rework | ₹5,000–₹12,000 |
| Digital multimeter (Fluke 87V) | Testing | ₹12,000–₹18,000 |
| Oscilloscope (100 MHz, 2-channel) | Electronics debug | ₹15,000–₹35,000 |
| ST-Link V2 programmer | Firmware loading | ₹400–₹600 |
| Optical power meter | Fiber/LED characterization | ₹8,000–₹20,000 |
| CNC milling machine (small desktop) | Optical block prototyping | ₹50,000–₹1,50,000 |
| 3D printer (FDM, Creality Ender 3) | Prototype housings | ₹15,000–₹25,000 |
| Spectrophotometer (UV-Vis) | Reagent/strip validation | ₹40,000–₹80,000 |
| Analytical balance (0.1 mg) | Reagent preparation | ₹20,000–₹40,000 |
| pH meter (calibrated) | Strip chemistry QC | ₹5,000–₹12,000 |
| Refrigerator (4°C) | Strip/reagent storage | ₹12,000–₹20,000 |
| Laptop + KiCad/Altium license | PCB design | ₹60,000–₹1,20,000 |
| LCR meter | Component QC | ₹8,000–₹15,000 |
| Lapping/polishing kit | Fiber end polishing | ₹3,000–₹6,000 |
| ESD workstations × 3 | Assembly | ₹15,000–₹25,000 |
| **Total Equipment Investment** | | **₹2,76,400 – ₹5,93,600** |

### 9.3 Human Resources

| Role | Qualification | Number | Monthly Salary (INR) |
|---|---|---|---|
| Electronics Engineer | B.E./B.Tech Electronics | 1 | ₹35,000–₹55,000 |
| Embedded Firmware Developer | B.E. + C/C++ experience | 1 | ₹40,000–₹65,000 |
| Mechanical/Optical Engineer | B.E. Mechanical/Optical | 1 | ₹30,000–₹50,000 |
| QC Technician | B.Sc. / Diploma | 1 | ₹18,000–₹28,000 |
| Assembly Technician | ITI / Diploma | 2 | ₹12,000–₹18,000 each |
| Regulatory Affairs Executive | M.Sc./M.Pharm + RA experience | 1 | ₹30,000–₹45,000 |
| **Total Monthly Payroll** | | **8 people** | **₹1,77,000–₹2,79,000** |

### 9.4 Software & Development Tools

| Tool | Purpose | Cost |
|---|---|---|
| KiCad (EDA) | PCB schematic + layout | Free |
| STM32CubeIDE | Firmware development | Free |
| SolidWorks / FreeCAD | Mechanical design | ₹0–₹2,50,000/year |
| MATLAB / Python | Calibration algorithm development | Free (Python) |
| LabVIEW / Python | Test automation | Free (Python) |
| Git + GitHub | Version control | Free |

---

## 10. Regulatory Pathway in India (CDSCO / MDR 2017)

### 10.1 Regulatory Classification

Under the **Medical Devices Rules (MDR) 2017** and its amendments, a urine dipstick analyzer is classified as an **In Vitro Diagnostic (IVD) device**.

**Classification:**
- **Instrument (Analyzer):** Class B IVD device (moderate risk)
- **Reagent Strips:** Class B IVD device (moderate risk)
- Both require CDSCO registration before manufacturing and sale

### 10.2 Regulatory Pathway for Indian Manufacturer

**Step 1 – Obtain Manufacturing License**
- Apply to State Licensing Authority (SLA) under Form MD-3 (for Class B devices)
- Requires GMP-compliant manufacturing facility inspection
- Fee: ~₹3,000–₹5,000 (state-level)
- Timeline: 3–6 months

**Step 2 – CDSCO Registration of the Device**
- File application on SUGAM portal (cdsco.gov.in)
- Required documents:
  - Device Master File (DMF): design, specifications, manufacturing process
  - Risk Management File (per ISO 14971)
  - Performance Evaluation Data (analytical validation)
  - Biocompatibility data (ISO 10993)
  - Labeling and IFU (Instructions for Use)
  - Quality Management System certificate (ISO 13485 preferred)
- Form: MD-7 (for new device registration by Indian manufacturer)
- Fee: ₹2,500 per device (Class B)
- Timeline: 6–12 months (CDSCO review)

**Step 3 – ISO 13485 Certification (Recommended)**
- Quality Management System for medical devices
- Required for export and preferred by large institutional buyers
- Certification body: BSI, TÜV SÜD, Bureau Veritas
- Cost: ₹3–₹8 lakh (initial audit + certification)
- Timeline: 6–12 months

**Step 4 – BIS Certification (If Applicable)**
- Bureau of Indian Standards (BIS) mark may be required for certain electronic medical devices
- Check current mandatory BIS list for IVD devices
- Apply under IS/IEC 61010-1 (safety for lab equipment)

**Step 5 – Labeling Requirements**
Per MDR 2017 Schedule V, labels must include:
- Device name, model number, lot number, serial number
- Manufacturer name and address
- Manufacturing date and shelf life
- "For In Vitro Diagnostic Use Only"
- CDSCO registration number
- Storage conditions
- Symbols per ISO 15223-1

### 10.3 Regulatory Timeline Summary

| Activity | Duration | Cost (approx.) |
|---|---|---|
| Manufacturing license (SLA) | 3–6 months | ₹5,000–₹15,000 |
| CDSCO device registration | 6–12 months | ₹25,000–₹75,000 (incl. documentation) |
| ISO 13485 QMS certification | 6–12 months | ₹3–₹8 lakh |
| Performance validation studies | 3–6 months | ₹2–₹5 lakh |
| **Total Regulatory Timeline** | **12–24 months** | **₹6–₹14 lakh** |

### 10.4 Post-Market Requirements
- Maintain vigilance and adverse event reporting
- Annual renewal of manufacturing license
- Periodic device re-registration (as per CDSCO timelines)
- Maintain complaint log and corrective action records

---

## 11. Indian Market Analysis & Competitive Landscape

### 11.1 Market Overview

The Indian urinalysis market is one of the fastest-growing segments in the IVD diagnostics space:

- **Market Size (2024):** ~₹450–₹600 crore (instruments + strips)
- **Growth Rate:** ~14–16% CAGR (driven by diabetes, CKD, UTI burden)
- **Key Drivers:**
  - India has 101 million diabetics (IDF 2021) — largest in the world
  - CKD affects ~17% of Indian adults
  - Ayushman Bharat PM-JAY expanding diagnostics access
  - Growing diagnostic lab chains (Dr. Lal Path Labs, SRL, Thyrocare, Metropolis)
  - Increasing hospital-based lab automation

- **Key End-Users:**
  - Hospital laboratories (tertiary, secondary)
  - Standalone diagnostic laboratories
  - Clinics and nursing homes (Tier 2/3 cities)
  - Government health centers (PHC, CHC under NHM)
  - Corporate health screening programs

### 11.2 Competitive Landscape

| Competitor | Model | Technology | Price (INR) | Strip Cost | Market Position |
|---|---|---|---|---|---|
| **Siemens** | Clinitek Status+, Clinitek Advantus | Reflectance photometry, 10P | ₹1,20,000–₹2,50,000 | ₹25–₹45/strip | Premium, dominant in large hospitals |
| **Mission Diagnostics** | U120, U500 | Reflectance photometry, 10P | ₹45,000–₹1,20,000 | ₹12–₹22/strip | Mid-market, strong in India |
| **Roche** | Cobas u 411 | Reflectance photometry, 10P | ₹1,80,000–₹3,00,000 | ₹30–₹55/strip | Premium, large hospitals |
| **Dirui** | H-100, H-500 | Reflectance photometry, 10P | ₹30,000–₹80,000 | ₹8–₹15/strip | Budget segment, growing |
| **URIT** | URIT-500B | Reflectance photometry, 10P | ₹25,000–₹60,000 | ₹6–₹12/strip | Budget segment |
| **Erba Mannheim** | UriScan Pro | Reflectance photometry, 10P | ₹50,000–₹1,00,000 | ₹10–₹20/strip | Mid-market |
| **Levram (Target)** | 2P/10P Benchtop | Reflectance photometry | ₹25,000–₹80,000 | ₹5–₹10/strip | Value-for-money, India-made |

### 11.3 Levram's Competitive Advantages

1. **"Make in India" Positioning:** Growing preference for domestic products in government tenders (GeM portal)
2. **Lower Strip Cost:** By sourcing OEM strips from China and rebranding, or eventually manufacturing in-house, Levram can undercut imported strip prices by 30–50%
3. **Service Network:** Existing distribution network enables faster after-sales service vs. imported brands
4. **Customization:** Can offer vernacular language UI, India-specific report formats, and integration with local HIS/LIS systems
5. **Price Point:** Target pricing 30–50% below Siemens/Mission for comparable performance

### 11.4 Target Segments (Priority Order)

1. **Small-to-medium diagnostic labs** (Tier 2/3 cities) — highest volume, price-sensitive
2. **Nursing homes and clinics** — need simple, reliable 2P or 10P device
3. **Government health centers** — GeM portal procurement, tender-driven
4. **Corporate health screening** — bulk purchase, annual contracts
5. **Large hospital labs** — longer sales cycle, need ISO 13485 and performance data

---

## 12. Go-to-Market Strategy

### 12.1 Distribution Strategy

Levram's existing distribution network is the primary competitive moat. The recommended approach:

**Tier 1 – Direct Distribution (Existing Network)**
- Leverage current distributor relationships in your territory
- Train distributors on product demonstration, installation, and basic troubleshooting
- Provide demo units to top 5 distributors in each region
- Offer 20–25% distributor margin on instruments, 30–35% on strips

**Tier 2 – Reagent Rental Model (Recommended for Market Penetration)**
- Offer the instrument free or at subsidized cost (₹5,000–₹10,000 deposit)
- Lock customer to minimum monthly strip purchase (e.g., 200 strips/month)
- Revenue model: ₹7–₹12 per strip × 200 strips × 12 months = ₹16,800–₹28,800/year per customer
- This model is used successfully by Siemens and Mission in India

**Tier 3 – Government/Tender Sales**
- Register on GeM (Government e-Marketplace) portal
- Target CMSS (Central Medical Services Society) tenders
- State-level NHM procurement for PHC/CHC labs
- Requires CDSCO registration and ISO 13485

### 12.2 Pricing Strategy

| Model | Instrument MRP | Strip MRP (per strip) | Strip MRP (per 100 strips) |
|---|---|---|---|
| 2P Analyzer | ₹24,999 | ₹4.50 | ₹399 |
| 10P Analyzer | ₹64,999 | ₹9.50 | ₹899 |

**Comparison vs. Benchmark:**
- Siemens Clinitek Status+ 10P: ₹1,80,000 instrument + ₹35/strip
- Mission U120 10P: ₹75,000 instrument + ₹18/strip
- Levram 10P: ₹64,999 instrument + ₹9.50/strip → **47% cheaper strips than Mission**

### 12.3 Launch Plan

| Phase | Timeline | Activities |
|---|---|---|
| **Phase 1: Development** | Month 1–12 | Prototype development, firmware, optical validation |
| **Phase 2: Regulatory** | Month 6–18 | CDSCO filing, ISO 13485, performance studies |
| **Phase 3: Pilot Launch** | Month 18–24 | 50 units to key accounts, gather clinical feedback |
| **Phase 4: Commercial Launch** | Month 24–30 | Full distribution rollout, GeM registration, marketing |
| **Phase 5: Scale-Up** | Month 30+ | In-house strip manufacturing, export markets |

### 12.4 Marketing & Promotion

- **KOL Engagement:** Partner with pathologists and lab directors in Tier 2/3 cities for clinical validation and endorsement
- **CME Programs:** Sponsor continuing medical education events for lab technicians and pathologists
- **Trade Shows:** Exhibit at MEDLAB India, Lab Asia, and NABL-accredited lab conferences
- **Digital Marketing:** LinkedIn, WhatsApp groups for lab professionals, YouTube demo videos
- **NABL Labs:** Target NABL-accredited labs first — they need documented, validated equipment

---

## 13. Cost of Goods & Pricing Strategy

### 13.1 Financial Summary

| Metric | 2P Model | 10P Model |
|---|---|---|
| COGS per unit (100 units) | ₹5,500 | ₹18,500 |
| COGS per unit (500 units) | ₹4,800 | ₹16,000 |
| COGS per unit (1,000 units) | ₹4,200 | ₹14,500 |
| Target MRP | ₹24,999 | ₹64,999 |
| Distributor price (40% discount) | ₹14,999 | ₹38,999 |
| Gross margin at distributor price | ~68% | ~59% |
| Strip COGS (10P, 1000-strip MOQ) | ₹3.50 | — |
| Strip MRP | ₹9.50 | — |
| Strip gross margin | ~63% | — |

### 13.2 Break-Even Analysis

**Fixed Costs (Annual):**
- Staff salaries: ₹25–₹35 lakh
- Facility rent + utilities: ₹5–₹10 lakh
- Regulatory + certification: ₹8–₹14 lakh (amortized over 3 years: ₹3–₹5 lakh/year)
- Equipment depreciation: ₹3–₹5 lakh/year
- **Total Fixed Costs: ~₹36–₹55 lakh/year**

**Break-Even Volume (10P model at distributor price ₹38,999, COGS ₹16,000):**
- Contribution per unit = ₹38,999 – ₹16,000 = ₹22,999
- Break-even units = ₹45,00,000 / ₹22,999 ≈ **196 units/year**

This is a very achievable target — even 20 distributors selling 10 units each per year achieves break-even.

### 13.3 Recurring Revenue (Strips)

The real profitability in this business is in consumables (strips), not instruments:

- A lab running 20 tests/day × 300 days = 6,000 strips/year
- At ₹9.50 MRP and ₹3.50 COGS: **gross profit of ₹36,000/year per installed instrument**
- With 500 installed instruments: **₹1.8 crore/year in strip revenue**
- This is the "razor-and-blade" model used by Siemens and Mission

---

## 14. References

1. Cabo, J., & Favresse, J. (2023). Application of analytical performance specifications for urine test strip methods: importance of reflectance signals. *Clinica Chimica Acta*, 548, 117534. https://doi.org/10.1016/j.cca.2023.117534

2. Liu, G., Hu, N., Ma, Z., et al. (2018). A portable analyzer based on a novel optical structure for urine dry-chemistry analysis. *Journal of Instrumentation*, 13(7), T07002. https://doi.org/10.1088/1748-0221/13/07/T07002

3. Liu, G. (2016). Optical fiber-based dry chemical analyzing device and analyzing method for urine. Patent Publication. https://scispace.com/papers/optical-fiber-based-dry-chemical-analyzing-device-and-4zykhn8o3y

4. Liu, G. (2016). Urine dry-chemistry analysis device and analysis method based on multiple monochromatic light rays and optical fibers. Patent Publication. https://scispace.com/papers/urine-dry-chemistry-analysis-device-and-analysis-method-5diiyqnm3b

5. Lee, D.-S., Jung, M. Y., Jeon, B. G., et al. (2010). Novel optical absorbance-based multi-analytes detection module using a tri-chromatic LED, PDs and plastic optical fibers and its application to a palm-sized urine test strip reader. *IEEE Sensors Conference*. https://doi.org/10.1109/ICSENS.2010.5690509

6. Ziegler, F. (2003). Reflection-photometric analytical system. Patent US6590651B2. https://scispace.com/papers/reflection-photometric-analytical-system-4nh36qfa7m

7. Ko, C.-H., Tadesse, A. B., & Kabiso, A. C. (2024). Spectrochip-based Calibration Curve Modeling (CCM) for Rapid and Accurate Multiple Analytes Quantification in Urinalysis. *Heliyon*, 10(18), e37722. https://doi.org/10.1016/j.heliyon.2024.e37722

8. Chen, L., Liu, G., Hu, N., et al. (2014). Study on a new urine analysis core module based on semi-reflection mirror. *Chinese Journal of Biomedical Engineering*. https://doi.org/10.7507/1001-5515.20140244

9. Clemens, A. H., & Hurtle, R. L. (1972). Automatic System for Urine Analysis. I. System Design and Development. *Clinical Chemistry*, 18(8), 789–796. https://doi.org/10.1093/CLINCHEM/18.8.789

10. Neeley, W. E., & Zettner, A. (1983). Reflectance digital matrix photometry. *Clinical Chemistry*, 29(6), 1038–1042. https://doi.org/10.1093/CLINCHEM/29.6.1038

11. Nagel, D., & Seiler, D. (1995). Urinalysis with the new fully automated analyzer Supertron. *Journal of Clinical Chemistry and Clinical Biochemistry*, 33(3), 183–188.

12. Dosmann, A. J., Howard, W., & Zembrod, A. (1988). Improved reflectance photometer. US Patent 4,792,689.

13. Kight, E. C., Hussain, I., & Bowden, A. K. (2021). Low-Cost, Volume-Controlled Dipstick Urinalysis for Home-Testing. *Journal of Visualized Experiments*, 171, e61406. https://doi.org/10.3791/61406

14. Siu, V., Lu, M., & Hsieh, K. Y. (2022). Toward a Quantitative Colorimeter for Point-of-Care Nitrite Detection. *ACS Omega*, 7(13), 11076–11085. https://doi.org/10.1021/acsomega.1c07205

15. Wikipedia. (2024). Urine test strip. Retrieved from https://en.wikipedia.org/wiki/Urine_test_strip

16. International Diabetes Federation. (2021). IDF Diabetes Atlas, 10th edition. Brussels, Belgium. https://www.diabetesatlas.org

17. Ministry of Health and Family Welfare, Government of India. (2017). Medical Devices Rules, 2017. Gazette of India Extraordinary, Part II, Section 3(i).

18. CDSCO. (2023). Guidance document for classification of IVD devices. Central Drugs Standard Control Organisation, New Delhi. https://cdsco.gov.in

19. Valenzuela, I., Amado, T. M., & Orillo, J. W. (2016). Urine test strip analysis using image processing for mobile application. *Jurnal Teknologi*, 78(6-5). https://doi.org/10.11113/JT.V78.8720

20. Optimizing the u411 automated urinalysis instrument for veterinary use. (2020). *Veterinary Clinical Pathology*, 49(1). https://doi.org/10.1111/vcp.12818

---

*This document is prepared for internal R&D and business planning purposes at Levram Life Sciences. All cost estimates are indicative and subject to market conditions as of May 2026. Regulatory timelines are approximate and subject to CDSCO processing. Consult a qualified regulatory affairs professional before filing.*

---
**End of Report**
