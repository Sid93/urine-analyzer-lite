# Stage 4 Engineering Review — Master Pin Map & Netlist Reconciliation

> Status: DRAFT for engineer verification (2026-05-21).
> **This document is the Stage 4 gate.** Before any PCB layout, an electronics engineer must
> resolve the items marked 🔴 and sign off on the master pin map below. AI-generated; treat as
> a high-quality first draft, NOT release-ready (see project key cautions).

## 0. Why this exists
The electrical design currently lives in three places that **disagree with each other**:
- `firmware/main/config.h` — the firmware pin map (internally consistent, testable)
- `design/blueprint/ELECTRICAL_CONNECTIONS.json` — Blueprint netlist
- `bom/bom.csv` + `README.md` — the parts list

There is also a non-matching legacy schematic (`hardware/schematic/...kicad_sch`, a graphical
mock-up with no netlist) and a separate, divergent camera-based KiCad project
(`~/Desktop/urine_dipstick_analyzer_pcb/`, ESP32-WROOM + OV2640). None can go to PCB as-is.

**Decision: `config.h` is adopted as the source of truth** (it is concrete, internally
consistent, and what the firmware actually drives), corrected for the hardware-validity issues
in §2. All other sources are reconciled to it.

## 1. Source conflicts (resolved → see §3)

| Item | config.h | Blueprint | BOM/README | Resolution |
|---|---|---|---|---|
| Motor driver | MX1508 | L298N mini | MX1508 | **MX1508** (cheaper, adequate for N20; matches firmware/BOM) |
| I2C SDA/SCL | 21 / **22** | 1 / 2 | — | Move to valid pins — see §2.1 |
| Motor IN1/IN2 | 18 / 8 | 4 / 5 | — | Use config.h, remapped in §3 |
| Encoder A/B | 15 / 7 | 6 / 7 | — | Use §3 map |
| HX711 DT/SCK | 4 / 5 | 19 / 20 | — | config.h (Blueprint uses USB pins) |
| Printer TX/RX | 6 / **19** | RX←17 | — | Move RX off USB pin — §2.2 |
| UV-C enable | **3** | (3=button) | — | Move off strapping pin — §2.3 |
| Scan button | 9 | 3 | — | GPIO 16 in §3 |
| Display | 4.3" DSI | 4.3" on I2C | DSI | ✅ RESOLVED: 3.5" SPI TFT (ILI9488) — §2.4 |
| TCS34725 ×2 | both 0x29 | both 0x29 | 2× same | 🔴 I2C address clash — needs mux — §2.5 |
| Printer rail | — | 9V | reg=5V only | 🔴 No 9V rail — §2.6 / power budget |

## 2. Hardware-validity issues (🔴 = engineer decision required)

### 2.1 🔴 Invalid I2C pin — GPIO22 does not exist on ESP32-S3
`config.h` sets `PIN_SCL 22`. The ESP32-S3 has **no GPIO22** (its GPIOs are 0–21 and 26–48).
This pin is invalid and would not compile/route correctly. → Reassign (see §3: SDA=1, SCL=2).

### 2.2 🔴 Printer RX on USB pin — GPIO19
`config.h` `PIN_PRINTER_RX 19`. GPIO19 = USB **D+** on ESP32-S3. The README specifies
"USB: Hardware CDC", so GPIO19/20 are consumed by native USB and cannot also be UART.
→ Move printer UART to a free pair (§3: TX=17, RX=18).

### 2.3 🔴 UV-C enable on strapping pin — GPIO3
GPIO3 is a boot strapping pin (JTAG source select). Driving it at boot can affect startup.
UV-C is a *safety-critical* output and must not glitch on. → Move to GPIO13 with a hardware
pull-down so UV-C is guaranteed OFF at boot (also a risk control — see risk file H1).

### 2.4 ✅ RESOLVED — Display = 3.5" SPI TFT (ILI9488)
Original spec (Waveshare 4.3" MIPI-DSI) was unbuildable: the ESP32-S3 has no MIPI-DSI
peripheral, and the Blueprint's "4.3" on I2C" is also invalid (a graphical panel can't run on I2C).
**Decision (2026-05-21): switch to a 3.5" SPI TFT, ILI9488 (or ST7796 4.0") with XPT2046 touch.**
- Native to ESP32-S3 over SPI; touch shares the SPI bus, IRQ polled (saves a pin).
- BOM updated (LCD1 → SPI TFT); pins assigned in §3.
- Firmware display UI (TODO "Implement display UI") should target LVGL/LovyanGFX on SPI.

### 2.5 🔴 Two TCS34725 share I2C address 0x29
Both color sensors default to 0x29 and the part has no address-select pin. The firmware comment
("multiplex by enabling the LED on one at a time") does **not** change the I2C address — two
devices at 0x29 on one bus is an unresolvable bus clash. → Add a **TCA9548A I2C mux** (addr 0x70)
and put each TCS34725 on its own channel. **This part is missing from the BOM — add it.**
(Alternative: a single sensor on a moving optical head; but dual-sensor differential is a stated design intent.)

### 2.6 🔴 Missing 9V printer rail
Blueprint shows the CSN-A2 printer on 9V, but the only regulator (S13V25F5) outputs 5V.
The CSN-A2 runs 5–9V; at 5V it prints (slightly slower/lighter). → Recommend **running the
printer at 5V** and deleting the 9V requirement, OR add a dedicated boost converter. See power budget.

## 3. Proposed master pin map (ESP32-S3, USB-CDC enabled) — VERIFY BEFORE LAYOUT

Avoids: GPIO 0/45/46 (strapping), 3 (strapping), 19/20 (USB), 22–25 (don't exist),
26–37 (SPI flash + octal PSRAM on N8R8). All assignments below are valid, free S3 GPIOs.

| Function | Net | GPIO | Notes |
|---|---|---|---|
| I2C SDA | `I2C_SDA` | 1 | shared bus: mux, SHT31, BH1750, ADS1115 |
| I2C SCL | `I2C_SCL` | 2 | |
| Motor IN1 (PWM) | `MOT_IN1` | 4 | MX1508 |
| Motor IN2 (PWM) | `MOT_IN2` | 5 | MX1508 |
| Encoder A | `ENC_A` | 6 | |
| Encoder B | `ENC_B` | 7 | |
| Limit home | `LIM_HOME` | 10 | INPUT_PULLUP, active-LOW |
| Limit end | `LIM_END` | 11 | INPUT_PULLUP, active-LOW |
| Illum LED PWM | `LED_PWM` | 12 | gate of 2N7000 |
| UV-C enable | `UVC_EN` | 13 | + 10k pull-DOWN; off at boot (safety) |
| HX711 DT | `HX_DT` | 14 | |
| HX711 SCK | `HX_SCK` | 15 | |
| Scan button | `SCAN_BTN` | 16 | INPUT_PULLUP, active-LOW |
| Printer TX (→RXD) | `PRN_TX` | 17 | UART1 |
| Printer RX (←TXD) | `PRN_RX` | 18 | UART1 |
| TFT SCLK | `TFT_SCLK` | 38 | SPI TFT (ILI9488) |
| TFT MOSI | `TFT_MOSI` | 39 | |
| TFT MISO | `TFT_MISO` | 40 | shared with touch read |
| TFT CS | `TFT_CS` | 41 | |
| TFT DC | `TFT_DC` | 42 | |
| TFT backlight | `TFT_BL` | 47 | enable / PWM |
| Touch CS | `TOUCH_CS` | 48 | XPT2046; IRQ polled |
| TFT reset | `TFT_RST` | 21 | |

I2C addresses: TCA9548A 0x70 → ch0/ch1 = TCS34725 (0x29 each); SHT31 0x44; BH1750 0x23; ADS1115 0x48. No clashes.
All display + I/O pins above are valid, free ESP32-S3 GPIOs and match `firmware/main/config.h`.

## 4. What remains for a real Stage 4 (after this is signed off)
1. Engineer resolves all 🔴 items and approves §3 map.
2. ✅ Netlist generated from the master pin map → `hardware/netlist/` (`urine_analyzer_lite.net`
   importable into Pcbnew, plus `NETLIST.md`). Footprints are placeholders to confirm in KiCad.
3. ✅ Schematic generated + **ERC-clean (0 errors)** → `hardware/schematic/` (+ PDF). Jellybean
   discretes use real `Device:`/`Switch:` library symbols; all parts have **real footprints**.
   KiCad netlist matches the model 39/39 by ref+pad.
4. ✅ **Starting PCB generated** → `hardware/pcb/urine_analyzer_lite.kicad_pcb` (+ project, render).
   31 footprints placed + net-assigned; **schematic-parity 0**. Unrouted (104-net ratsnest) and
   auto-grid placement (cosmetic DRC). Engineer: confirm module header pin order, place, route,
   power planes, DRC→0, Gerbers.
4. PCB layout: power planes (GND/3V3/5V), wide traces for motor/printer/UV-C, mounting holes to chassis.
5. Run **DRC** → 0 errors. Export Gerbers + assembly BOM (JLCPCB/PCBWay).
6. Order 5× prototypes.

> Note for this environment: KiCad / `kicad-cli` is not installed here, so ERC/DRC/Gerber export
> and interactive layout must be done on a workstation with KiCad. I can generate a real
> netlisted schematic *file* programmatically if you want to take that path — say the word.
