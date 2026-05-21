# Target Product Profile — Urine Analyzer Lite

> Stage 0 Foundation document. Owner: Levram Lifesciences. Status: DRAFT (2026-05-21).
> This TPP is the reference against which all design, validation, and regulatory work is judged.
> Changing any row here may invalidate downstream validation — treat as a controlled document.

## 1. Intended Use Statement (draft)

> The Urine Analyzer Lite is an automated reflectance photometer intended for the
> semi-quantitative *in vitro* measurement of the following analytes in human urine,
> using compatible urine reagent test strips: leukocytes, nitrite, urobilinogen, protein,
> pH, blood, specific gravity, ketones, bilirubin, and glucose. It is intended for use by
> trained healthcare personnel at the point of care (clinics, physician offices, small
> labs). Results are intended as an aid to diagnosis and must be interpreted by a
> qualified clinician in the context of other clinical findings. Not for home/self-testing
> in the current configuration. Not for screening of blood or other body fluids.

## 2. Profile

| Attribute | Target | Notes |
|---|---|---|
| Product type | Automated urine reagent-strip reader (reflectance photometer) | Instrument; strips are a separate consumable |
| Analytes | 10-pad panel (leuko, nitrite, urobilinogen, protein, pH, blood, SG, ketones, bilirubin, glucose) | Matches standard commercial strip layout |
| Result type | Semi-quantitative (grades / concentration bands per analyte) | Not a true quantitative analyzer |
| Measurement principle | Optical reflectance; dual TCS34725 RGB sensors + high-CRI LED; HSV classification | See `analysis.h` |
| Sample | Human urine, applied to strip by operator | Device does not aspirate/handle free liquid beyond the wetted strip |
| Intended user | Trained healthcare personnel (nurse / technician / physician) | Drives IEC 62366 use spec; NOT lay user (see open issue) |
| Use environment | Clinic / point-of-care, indoor, 15–35 °C, 20–80% RH | Matches firmware environmental envelope |
| Throughput | Single strip per cycle | "Lite" positioning |
| Output | On-screen result + 58 mm thermal printout | ESC/POS |
| Connectivity | Optional Wi-Fi/BT result upload (roadmap) | If added, triggers cybersecurity assessment (Stage 8) |
| Power | Internal LiPo, USB-C charge | Portable |
| Strip compatibility | **OPEN ISSUE** — current design reads a standard commercial strip; business intent is a Levram-proprietary strip | Must resolve; see §4 |
| Shelf life (instrument) | Target ≥ 3 years | Reliability/Stage 7 |
| Target cost | <$250/unit at 50-unit volume (prototype ~₹387/$) | Per BOM |
| Market | India first (CDSCO); export (CE/510(k)) later | |

## 3. Performance targets (to be confirmed against predicate)

These are placeholders to be locked after a predicate-device benchmark and refined in Stage 6.

| Metric | Target | How verified |
|---|---|---|
| Agreement vs. visual read (per analyte) | ≥ 90% within ±1 grade | CLSI method comparison |
| Agreement vs. predicate analyzer | ≥ 90% concordance | Method comparison study |
| Repeatability (same strip lot, same sample) | ≥ 95% identical grade | CLSI EP05 |
| Carryover between strips | None detectable | Bench protocol |
| Reportable range | Per strip manufacturer's bands | |

## 4. Open issues blocking TPP sign-off

1. **Strip strategy (CRITICAL).** README/firmware currently read *standard commercial* strips,
   but stated business intent is to *develop a proprietary Levram strip*. These are different
   products with different scope, IFU, and regulatory dossiers. Decide before Stage 1.
   - If reading commercial strips: must declare compatible strip brand(s)/lot and calibrate to them; you do not control their chemistry or supply.
   - If proprietary strips: adds a full reagent-development + ISO 23640 stability + separate IVD registration track.
2. **User population.** TPP assumes trained personnel (POC clinic). If home use is ever
   in scope, usability/risk and possibly device class change.
3. **Quantitative vs semi-quantitative claim.** Keep semi-quantitative unless you can
   support a quantitative claim with validation — over-claiming is a regulatory risk.
