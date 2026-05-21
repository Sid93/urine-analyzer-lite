# CDSCO Classification & Regulatory Pathway — Urine Analyzer Lite

> Stage 0 Foundation document. Status: DRAFT (2026-05-21).
> **This class must be confirmed by a CDSCO regulatory consultant via pre-submission
> BEFORE any validation data is generated.** Wrong class = wrong tests = repeated studies.

## 1. Regulatory framework
- **Medical Devices Rules, 2017 (MDR 2017)**, as amended, administered by **CDSCO** (Central
  Drugs Standard Control Organisation). IVDs are notified medical devices.
- IVDs are risk-classified **A / B / C / D** (low → high), per the IVD classification rules
  in MDR 2017 Schedule and CDSCO's published IVD classification lists.
- Submissions are made through the **CDSCO MD Online (SUGAM) portal**.

## 2. Classification analysis

The product is an **instrument (reagent-strip reader)**, not the reagent itself.

| Factor | Assessment |
|---|---|
| Analytes | Routine urinalysis params (glucose, protein, pH, etc.) — established, low individual risk |
| Risk if wrong result | Moderate: aids diagnosis, not sole basis; confirmatory testing standard of care |
| Public health risk | Not for blood screening / infectious-disease confirmation / self-testing |
| Precedent | Urine chemistry analyzers / urinalysis reagent-strip readers generally listed **Class B** |

**Best-guess class: B (low–moderate risk)** for the reader instrument.

> Caveats that could move it:
> - The **reagent strips** (if Levram-proprietary) are a *separate* IVD with their own
>   classification — per-analyte, often **B**, but some analytes can pull to **C**.
>   Glucose/blood/protein urine strips are typically B in India.
> - A **home/self-test** claim typically raises class and adds lay-user usability burden.

## 3. Pathway (assuming Class B, India-manufactured)

1. **Pre-submission meeting** with CDSCO (via consultant) to confirm class and test scope. *(do first)*
2. **ISO 13485 QMS** in place (mandatory foundation for licensing).
3. **Test Licence** to manufacture for test/evaluation/clinical performance:
   - Form **MD-12** application → Licence **MD-13**.
4. **Manufacturing Licence** (Class B → State Licensing Authority):
   - Form **MD-3** application → Licence **MD-5** (Class A/B).
   - *(Class C/D would be MD-7 → MD-9 via Central Licensing Authority — note in case strips push to C.)*
5. **Clinical performance evaluation** as required for the IVD (extent depends on class &
   novelty); register study (CTRI) and capture data under controls (e.g. REDCap) if applicable.
6. **Test reports** from a CDSCO-recognized / NABL lab against the standards matrix.
7. Post-licence: **PMS, vigilance (MvPI), complaint/CAPA** obligations (Stage 12).

## 4. Predicate strategy
- Identify 1–2 legally-marketed predicate urinalysis readers in India (e.g. established
  semi-automated strip readers) to anchor intended use, claims, and method-comparison studies.
- Document predicates here once selected.

## 5. Immediate action
- [ ] Engage CDSCO regulatory consultant for pre-submission (class lock).
- [ ] Confirm whether strips are in-scope (separate registration) — see TPP §4.
- [ ] Identify predicate device(s).
