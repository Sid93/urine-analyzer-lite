# Applicable Standards Matrix — Urine Analyzer Lite

> Stage 0 Foundation document. Status: DRAFT (2026-05-21).
> Tailored to: benchtop/portable IVD reflectance reader, mains-or-battery powered,
> no patient body contact, software-controlled, point-of-care clinic use.

## Applicable

| Standard | Scope | Why it applies | How addressed / stage |
|---|---|---|---|
| **ISO 13485** | QMS for medical devices | Mandatory for CDSCO licensing & design controls | QMS setup, Stage 9 |
| **ISO 14971** | Risk management | Required for any medical device; central risk file | `03_risk_management_iso14971.md`, ongoing |
| **IEC 61010-1** | Safety of electrical equipment for measurement/lab use | Device is lab/measurement electrical equipment, NOT patient-contacting | Stage 7 (NABL test) |
| **IEC 61010-2-101** | Particular requirements for IVD medical equipment | Direct match: IVD instrument | Stage 7 |
| **IEC 61326-2-6** | EMC — particular requirements for IVD equipment | Electronic device with sensors/motor/RF | Stage 7 EMC |
| **IEC 62304** | Medical device software life cycle | Firmware (ESP32-S3) drives measurement & classification | Stage 4/8; assign software safety class |
| **IEC 62366-1** | Usability engineering | Operator-in-the-loop steps (strip load, sample, read) | Stage 8 use spec + formative/summative |
| **ISO 18113 (series)** | IVD — information supplied by manufacturer (labels/IFU) | IVD labeling & instructions for use | Stage 11 |
| **ISO 15223-1** | Symbols for medical device labels | Label symbols | Stage 11 |
| **CLSI EP05** | Precision evaluation | Repeatability/reproducibility claims | Stage 6 |
| **CLSI EP06** | Linearity | Reportable-range support (semi-quant bands) | Stage 6 |
| **CLSI EP07** | Interference | Urine matrix interferents (color, turbidity, ascorbic acid) | Stage 6 |
| **CLSI EP17** | Detection capability (LoB/LoD/LoQ) | Detection limits per analyte | Stage 6 |
| **CLSI EP09 / method comparison** | Comparison with predicate / reference | Agreement vs predicate analyzer & visual read | Stage 6 |
| **IEC 62471** | Photobiological safety of lamps/LEDs | **275 nm UV-C LED** sterilization — eye/skin hazard | Stage 7/8; must show interlock/shielding |

## Conditionally applicable

| Standard | Applies if... |
|---|---|
| **ISO 23640** | IVD reagent stability — applies to the **strips** if Levram develops proprietary strips |
| **IEC 81001-5-1 / cybersecurity guidance** | Wi-Fi/BT result upload is added |
| **ISO 20916** | A clinical performance study is run for the IVD |
| **ISTA / ASTM D4169** | Transport/packaging once distribution defined (Stage 11) |
| **AERB / UV-C regulatory** | Confirm any Indian requirement for UV-C emitting consumer/medical product |

## Explicitly NOT applicable (and why)

| Standard | Why excluded |
|---|---|
| **ISO 10993 (biocompatibility)** | Device has no contact with patient body/tissue; only the strip contacts urine |
| **IEC 60601 series** | That's for *medical electrical equipment with patient contact*; this is lab/IVD equipment → 61010 governs |
| **ISO 15197** | Specific to *blood* glucose monitoring; not urine analytes |

## Open item
- **UV-C is the standout safety/regulatory item.** A 275 nm source is a genuine eye/skin
  hazard and an unusual feature for this device class. Decide whether UV-C sterilization is
  worth the added IEC 62471 burden + interlock design, or drop it for a simpler decontamination
  instruction. Flag for risk file and TPP.
