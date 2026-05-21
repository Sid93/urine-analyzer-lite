# Risk Management File (ISO 14971) — Urine Analyzer Lite

> Stage 0 Foundation document. Status: DRAFT skeleton (2026-05-21).
> This is the seed of the living risk file. Populate severity/probability against a defined
> scale, link each control to a verification, and close the file at design freeze (Stage 5)
> before validation. Per the project hard-gate: validating an unfrozen design = repeat work.

## 1. Risk policy (to define)
- [ ] Define severity scale (e.g. 1 Negligible → 5 Catastrophic)
- [ ] Define probability scale (e.g. 1 Improbable → 5 Frequent)
- [ ] Define risk acceptability matrix and overall residual-risk acceptance criteria

## 2. Intended use & reasonably foreseeable misuse (from TPP)
- Intended: trained personnel, clinic POC, semi-quantitative urinalysis aid to diagnosis.
- Foreseeable misuse: expired/wrong strip, mis-timed read, wet/contaminated optics,
  ambient light ingress, reading a non-compatible strip, lay use outside intended population.

## 3. Hazard analysis / preliminary FMEA

> S/P/RPN left blank — to be scored against the policy scale. "→" = required risk control.

| # | Hazard / cause | Potential harm | Risk control (→) | Verify in |
|---|---|---|---|---|
| H1 | **UV-C (275 nm) exposure** to operator eyes/skin (lid open, interlock fails) | Photokeratitis, skin burn | → Mechanical interlock so UV-C cannot fire unless chamber closed; shielding; IEC 62471 assessment; consider removing UV-C | Stage 7/8 |
| H2 | **Incorrect analyte result** (mis-calibration, drift, lighting, wrong hue table) | Missed/incorrect diagnosis | → White-standard calibration SOP; internal reference/QC strip; ambient-light sensor compensation (BH1750); reportable-range limits; IFU "aid to diagnosis only" | Stage 6 |
| H3 | **Reading an incompatible / expired strip** | Wrong result | → Strip compatibility declared in IFU; (optional) strip-type detection; expiry warning in workflow | Stage 6/11 |
| H4 | **Ambient light / optical contamination** (fingerprints, urine on optics) | Result error | → Light-tight chamber (black PLA, verified); cleaning SOP; self-check on white standard each session | Stage 5/6 |
| H5 | **Biohazard** — urine contamination of device/operator | Infection exposure | → Disposable strip handling; cleanable surfaces; decontamination SOP; no free-liquid handling | Stage 8/11 |
| H6 | **Electrical safety** — LiPo fault, charger fault, mains (if any) | Burn/fire/shock | → TP4056 protection + protected cell; IEC 61010-1 compliance; fusing; thermal cutoff | Stage 7 |
| H7 | **LiPo thermal runaway** (charge fault, heat near printer/UV) | Fire | → Protected cell, charge temp limits, physical separation from heat sources, brownout/thermal monitoring | Stage 7 |
| H8 | **Mechanical pinch / motor** (N20 strip transport) | Minor injury | → Enclosed transport, low-torque motor, limit switches, no exposed moving parts | Stage 5/8 |
| H9 | **Thermal printer burn** (printhead hot) | Minor burn | → Enclosure, IFU warning | Stage 7 |
| H10 | **Software failure** — hang, misclassification, silent wrong result | Wrong/no result without operator awareness | → Watchdog + brownout (in TODO); IEC 62304 process; unit tests for `rgb_to_hsv`/`classify_pad`; result plausibility checks; fail-safe = no result rather than wrong result | Stage 4/8 |
| H11 | **Use error** — mis-timed read, wrong strip orientation | Wrong result | → Guided UI workflow; fixed motorized timing (removes manual timing error); IEC 62366 study | Stage 8 |
| H12 | **Cybersecurity** (if Wi-Fi/BT added) | Data integrity/privacy | → If connectivity added: threat model, secure OTA, no PII in transit without protection | Stage 8 (conditional) |

## 4. Notable design-level observations
- The **motorized fixed-timing read is a safety strength** — it removes the operator-timing
  error that plagues manual visual dipstick reading. Capture this as a risk-reducing feature.
- **UV-C (H1) is the highest-novelty hazard** and the main reason to reconsider that feature.
- **Fail-safe principle to adopt:** on any sensor/calibration/plausibility failure, the device
  must *withhold* a result (and say so), never print a guessed one.

## 5. Next
- [ ] Score all hazards; compute initial vs residual risk.
- [ ] Link each control to a specific verification/test (traceability).
- [ ] Add overall residual-risk / benefit-risk conclusion at design freeze.
