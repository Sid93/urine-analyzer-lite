# Freedom-to-Operate (FTO) — Preliminary Search — Urine Analyzer Lite

> Stage 0 Foundation document. Status: PRELIMINARY (2026-05-21).
> Scope: the **optical reading mechanism** (stated novelty: optics/hardware).
> **This is a self-service preliminary search, NOT a legal opinion.** Before commercial
> launch, commission a formal FTO/clearance search from a patent attorney, especially for
> any export market (US/EU).

## 1. Why this matters here
The stated competitive edge is "optics / hardware." That is exactly the area where this
device category is **most heavily patented**, so FTO risk is concentrated in the novelty.
Reflectance photometry of urine strips is a mature field (commercial readers since the
1980s — Bayer/Siemens Clinitek, Roche Urisys, etc.), so the *fundamental* reading method is
old and largely in the public domain / expired. Risk lives in **specific recent
implementations**: multi-wavelength imaging, interference correction, algorithmic
classification, and integrated sample/strip handling.

## 2. Search performed (2026-05-21)
Web/patent searches via Google Patents, Justia, and literature. Recommended next:
re-run on **Google Patents, Lens.org, Espacenet** with CPC class **G01N 33/493** (urine
analysis) and **G01N 21/25/.../78** (colorimetry/reflectance), plus full INPADOC family +
legal-status (expiry) checks.

Queries used: `optical reflectance urine reagent strip reader colorimetric automated`;
`urinalysis dipstick reader RGB color sensor strip transport`.

## 3. Patents/applications identified (preliminary — verify status & claims)

| Ref | Title | Relevance | Action needed |
|---|---|---|---|
| **US11307147B2** | Accurate colorimetric based test-strip reader system | Illuminate strip w/ selected spectra, capture images, compare to calibration curves, **correct for interference** | Read claims; our interference handling must avoid claimed method; check legal status & jurisdiction |
| **US20200124587 (A1)** | Urinalysis device and test strip for home & POC use | Multi-LED (R/G/B/White/Orange/IR/UV); per-pad image combinations by chemistry; integrated sample loading | Check if granted & claims; our single white-CRI-LED + RGB-sensor approach likely differs, but verify the UV/multi-wavelength angle |
| **KR20110042691A** | Portable Urine Analyzer | LED white source + **color-sensor array** + strip loader — closest architectural match to our TCS34725 + LED + motorized loader | Check status/family; likely older — possibly expired/abandoned (favorable if so) |
| **US20120208288A1** | Unitized point-of-care urine dipstick control device | POC dipstick handling/QC | Lower direct relevance; review |

## 4. Preliminary risk read
- **Core reflectance reading (white LED illuminates pad → RGB/color sensor → classify):**
  LOW FTO risk — decades-old, well-documented, foundational patents expired.
- **Specific algorithmic claims** (e.g. interference correction à la US11307147B2,
  multi-wavelength image combination à la US20200124587): MEDIUM — must read claims and
  design around; do not copy a claimed multi-spectral interference-correction method.
- **Integrated sample-loading / strip-transport mechanisms:** MEDIUM — several patents cover
  loaders; our N20 motorized tray should be checked against KR20110042691A and similar.
- **UV-C sterilization within a urine reader:** appears uncommon — possible novelty *and*
  possible standalone IP, but also the biggest safety/regulatory cost (see risk file H1).

## 5. Implications for the "optics is our novelty" strategy
Honest assessment: a white-LED + commodity RGB-sensor (TCS34725) reflectance head is **not
novel** on its own — it is the textbook approach and is already in the prior art (incl.
KR20110042691A). To make "optics/hardware" a real differentiator (and patentable), the edge
likely needs to be something more specific, e.g.:
- a genuinely better illumination/optical geometry that improves accuracy or cost,
- multi-angle / dual-sensor differential reading that demonstrably reduces a known error source,
- a self-calibration / ambient-compensation scheme that is novel and provable.
Recommend deciding *what specifically* is novel, then doing a focused FTO + a possible
provisional patent filing around that, rather than around "an optical urine reader" generally.

## 6. Next actions
- [ ] Re-run searches on Lens.org + Espacenet with CPC G01N33/493 & G01N21; pull INPADOC families.
- [ ] Check **legal status / expiry / jurisdiction** of each patent above (esp. India designations).
- [ ] Read the independent claims of US11307147B2 and US20200124587; document design-arounds.
- [ ] Define the specific, defensible optical novelty (see §5) → consider provisional filing.
- [ ] Commission formal attorney FTO before commercial launch / fundraising / export.
