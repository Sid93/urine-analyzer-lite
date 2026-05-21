# Stage 4 Power Budget & Rail Analysis — Urine Analyzer Lite

> Status: DRAFT for engineer verification (2026-05-21). Numbers are estimates from datasheets/
> typical modules; confirm against actual parts before regulator/battery sizing is frozen.

## 1. Power tree (as designed)

```
LiPo 3.7V 2000mAh ──► TP4056 (USB-C charge only) ──► (LiPo discharges directly)
                                                  │
                              ┌───────────────────┴───────────────────┐
                              ▼                                        
                    S13V25F5 buck-boost  ──►  5V rail (rated 2.5 A max)
                              │
                              ├─► 5V: MCU (5V pin), illum LED, UV-C LED, printer*, motor driver, display
                              └─► 3.3V: ??? (see §3 — no dedicated 3.3V regulator in BOM)
```
\* Blueprint claimed printer on 9V — no 9V rail exists (see Engineering Review §2.6).

## 2. Load estimate (peak)

| Load | Rail | Typical | Peak | Notes |
|---|---|---|---|---|
| ESP32-S3 DevKit | 5V→3V3 | 0.15 A | ~0.5 A | WiFi/BT bursts if enabled |
| High-CRI illum LED | 5V | 0.1 A | 0.1 A | PWM |
| **UV-C 275 nm LED** | 5V | — | ~0.5 A | only during 10 s sterilize |
| **N20 motor (GA12-N20)** | 5V | 0.15 A | ~0.8–1.5 A | stall current; running ~150 mA |
| **CSN-A2 thermal printer** | 5V | 0.5 A | **~1.5–2.0 A** | dominant load; heavy during black print |
| 4.3" display (if kept) | 5V | 0.2 A | ~0.5 A | backlight dominated |
| Sensors (TCS×2, SHT31, BH1750, ADS1115, mux) | 3.3V | <0.05 A | <0.05 A | negligible |
| HX711 + load cell | 3.3V | <0.01 A | <0.01 A | |

## 3. 🔴 Findings (engineer decisions)

1. **No dedicated 3.3V rail.** Sensors are 3.3V but the only regulator outputs 5V. Currently
   they'd draw from the DevKit's onboard 3V3 pin (LDO from 5V/USB), which is limited (~few
   hundred mA) and not meant to power an external sensor bus reliably. → Add a small **3.3V
   regulator** (e.g. AMS1117-3.3 or a buck) fed from 5V, sized for the sensor bus. The legacy
   PCB already used an AMS1117-3.3 — reuse that choice.

2. **Regulator headroom is marginal.** Worst-case *coincident* 5V load:
   printer 2.0 A + motor 0.8 A + MCU 0.5 A + display 0.5 A + LED 0.1 A ≈ **3.9 A**, which
   **exceeds the S13V25F5's 2.5 A rating.** Mitigations:
   - **Sequence high loads** (the state machine already does: SCAN → PRINT → STERILIZE are
     sequential, so printer/UV-C/heavy-motor rarely coincide). Document this as a hard firmware
     constraint, not just current behavior.
   - If coincidence is possible, **up-rate the regulator** (≥4 A) or split rails.

3. **Battery discharge rate.** ~3.9 A peak from a 3.7 V cell ≈ a 2000 mAh pouch at ~**2C**.
   Confirm the cell's continuous + pulse C-rating; add bulk capacitance (e.g. 1000 µF) near the
   printer to absorb print pulses. Under-rated cells will sag and brown-out the MCU.

4. **TP4056 is a charger, not a system-power-path IC.** It does not provide load-sharing /
   power-path management. While charging, simultaneous heavy load can confuse charge
   termination. → Consider a power-path charger (e.g. a TP4056-with-protection + ideal-diode,
   or an IP5306/BQ24074-class IC) if the device must operate while charging.

5. **Brown-out protection.** Enable ESP32-S3 brown-out detector and gate the printer/UV-C so a
   sagging rail can't trigger a mid-cycle reset that leaves UV-C on (safety, risk file H1/H7).

## 4. Recommended actions before layout
- [ ] Add 3.3V regulator (AMS1117-3.3 or buck) to BOM + schematic.
- [ ] Add TCA9548A I2C mux to BOM (from Engineering Review §2.5).
- [ ] Decide printer rail: run at 5V (preferred) or add 9V boost.
- [ ] Confirm LiPo C-rating ≥ peak draw; add bulk caps at printer + motor.
- [ ] Decide regulator sizing vs. enforced load-sequencing; document the sequencing constraint.
- [ ] Resolve display (Engineering Review §2.4) — affects pin count and 5V budget.
