#!/usr/bin/env python3
"""
Netlist generator for Urine Analyzer Lite (Design A: ESP32-S3 + dual TCS34725).

Single source of truth = the master pin map in firmware/main/config.h
(documented in hardware/ENGINEERING_REVIEW.md §3). Emits:
  - urine_analyzer_lite.net   KiCad legacy netlist (File > Import Netlist in Pcbnew)
  - NETLIST.md                human-readable connection table for review

NOTE: This describes intended connectivity for engineer verification. Real KiCad footprints
are assigned via footprints.py (modules use 2.54mm pin headers — verify pin ORDER against each
module datasheet). Decoupling/bulk caps are included where load behavior demands them; add
per-rail 100 nF at layout as standard practice.

Run: python3 gen_netlist.py
"""

import datetime, sys, os

# ── Component model ───────────────────────────────────────────────────────────
# Each component: ref, value, footprint(placeholder), description, and pins:
#   { pin_number: (pin_name, net_name) }
# Nets are inferred by grouping all (ref, pin) that share a net_name.

COMPONENTS = [
    ("U1", "ESP32-S3-DevKitC-1", "Module:ESP32-S3-DevKitC-1_header_2x22",
     "Main MCU (USB-CDC enabled)", {
        "5V":   ("5V",     "+5V"),
        "GND1": ("GND",    "GND"),
        "GND2": ("GND",    "GND"),
        "1":    ("GPIO1",  "I2C_SDA"),
        "2":    ("GPIO2",  "I2C_SCL"),
        "4":    ("GPIO4",  "MOT_IN1"),
        "5":    ("GPIO5",  "MOT_IN2"),
        "6":    ("GPIO6",  "ENC_A"),
        "7":    ("GPIO7",  "ENC_B"),
        "10":   ("GPIO10", "LIM_HOME"),
        "11":   ("GPIO11", "LIM_END"),
        "12":   ("GPIO12", "LED_PWM"),
        "13":   ("GPIO13", "UVC_EN"),
        "14":   ("GPIO14", "HX_DT"),
        "15":   ("GPIO15", "HX_SCK"),
        "16":   ("GPIO16", "SCAN_BTN"),
        "17":   ("GPIO17", "PRN_TX"),
        "18":   ("GPIO18", "PRN_RX"),
        "21":   ("GPIO21", "TFT_RST"),
        "38":   ("GPIO38", "TFT_SCLK"),
        "39":   ("GPIO39", "TFT_MOSI"),
        "40":   ("GPIO40", "TFT_MISO"),
        "41":   ("GPIO41", "TFT_CS"),
        "42":   ("GPIO42", "TFT_DC"),
        "47":   ("GPIO47", "TFT_BL"),
        "48":   ("GPIO48", "TOUCH_CS"),
     }),

    # ── Power path ──
    ("BT1", "LiPo 3.7V 2000mAh", "Connector:JST_PH_2pin", "Main battery", {
        "1": ("+", "VBAT"), "2": ("-", "GND")}),
    ("U2", "TP4056 USB-C", "Module:TP4056_USBC", "LiPo charger (charge path only)", {
        "1": ("VBUS",  "VBUS"),
        "2": ("GND",   "GND"),
        "3": ("BAT+",  "VBAT"),
        "4": ("BAT-",  "GND"),
        "5": ("OUT+",  "VSYS"),
        "6": ("OUT-",  "GND")}),
    ("U3", "S13V25F5 buck-boost", "Module:Pololu_S13V25Fx", "5V 2.5A regulator", {
        "1": ("VIN",  "VSYS"),
        "2": ("GND",  "GND"),
        "3": ("VOUT", "+5V"),
        "4": ("EN",   "+5V")}),   # EN tied high (always on); engineer may gate
    ("U12", "AMS1117-3.3", "Package_TO_SOT_223:SOT-223-3_TabPin2", "3.3V LDO for sensor bus", {
        "1": ("GND",  "GND"),
        "2": ("VOUT", "+3V3"),
        "3": ("VIN",  "+5V")}),
    ("C1", "1000uF/10V", "CP_Radial_D10.0mm_P5.00mm", "Bulk cap at 5V (printer pulse)", {
        "1": ("+", "+5V"), "2": ("-", "GND")}),
    ("C2", "470uF/10V", "CP_Radial_D8.0mm_P3.50mm", "Bulk cap at motor driver", {
        "1": ("+", "+5V"), "2": ("-", "GND")}),
    ("C3", "10uF/10V", "Capacitor_SMD:C_0805", "AMS1117 output cap", {
        "1": ("1", "+3V3"), "2": ("2", "GND")}),

    # ── I2C mux + sensors ──
    ("U11", "TCA9548A", "Package_SO:TSSOP-24_4.4x7.8mm_P0.65mm", "I2C mux (addr 0x70)", {
        "VCC":  ("VCC",  "+3V3"),
        "GND":  ("GND",  "GND"),
        "SDA":  ("SDA",  "I2C_SDA"),
        "SCL":  ("SCL",  "I2C_SCL"),
        "RST":  ("RESET","+3V3"),
        "A0":   ("A0",   "GND"),
        "A1":   ("A1",   "GND"),
        "A2":   ("A2",   "GND"),
        "SD0":  ("SD0",  "TCS1_SDA"),
        "SC0":  ("SC0",  "TCS1_SCL"),
        "SD1":  ("SD1",  "TCS2_SDA"),
        "SC1":  ("SC1",  "TCS2_SCL")}),
    ("U4", "TCS34725", "Module:Adafruit_TCS34725", "RGB sensor #1 (mux ch0)", {
        "VIN": ("VIN", "+3V3"), "GND": ("GND", "GND"),
        "SDA": ("SDA", "TCS1_SDA"), "SCL": ("SCL", "TCS1_SCL")}),
    ("U5", "TCS34725", "Module:Adafruit_TCS34725", "RGB sensor #2 (mux ch1)", {
        "VIN": ("VIN", "+3V3"), "GND": ("GND", "GND"),
        "SDA": ("SDA", "TCS2_SDA"), "SCL": ("SCL", "TCS2_SCL")}),
    ("U6", "SHT31-D", "Module:SHT31_breakout", "Temp/humidity (0x44)", {
        "VIN": ("VIN", "+3V3"), "GND": ("GND", "GND"),
        "SDA": ("SDA", "I2C_SDA"), "SCL": ("SCL", "I2C_SCL"), "ADR": ("ADR", "GND")}),
    ("U7", "BH1750", "Module:BH1750_breakout", "Ambient light (0x23)", {
        "VCC": ("VCC", "+3V3"), "GND": ("GND", "GND"),
        "SDA": ("SDA", "I2C_SDA"), "SCL": ("SCL", "I2C_SCL"), "ADDR": ("ADDR", "GND")}),
    ("U8", "ADS1115", "Module:ADS1115_breakout", "16-bit ADC (0x48)", {
        "VDD":  ("VDD",  "+3V3"), "GND": ("GND", "GND"),
        "SDA":  ("SDA",  "I2C_SDA"), "SCL": ("SCL", "I2C_SCL"),
        "ADDR": ("ADDR", "GND"), "A0": ("A0", "NTC_SENSE")}),
    ("RT1", "NTC 10k B3950", "Resistor_THT:R_Axial_DIN0207", "Optical chamber temp", {
        "1": ("1", "+3V3"), "2": ("2", "NTC_SENSE")}),
    ("R1", "10k", "Resistor_SMD:R_0805", "NTC divider lower leg", {
        "1": ("1", "NTC_SENSE"), "2": ("2", "GND")}),

    # ── Motor + encoder ──
    ("U9", "MX1508", "Module:MX1508_driver", "Dual H-bridge (one channel used)", {
        "VCC": ("VCC", "+5V"), "GND": ("GND", "GND"),
        "IN1": ("IN1", "MOT_IN1"), "IN2": ("IN2", "MOT_IN2"),
        "OUT1": ("OUT1", "MOTOR_A"), "OUT2": ("OUT2", "MOTOR_B")}),
    ("M1", "GA12-N20 6V 200RPM +enc", "Motor:GA12-N20_encoder", "Strip transport motor", {
        "M1": ("M1", "MOTOR_A"), "M2": ("M2", "MOTOR_B"),
        "VCC": ("VCC", "+3V3"), "GND": ("GND", "GND"),
        "C1": ("C1", "ENC_A"), "C2": ("C2", "ENC_B")}),

    # ── Limit switches (NO; other side to GND, MCU uses INPUT_PULLUP) ──
    ("SW1", "KW12-3", "Button_Switch_THT:SW_Limit", "Home limit (active-LOW)", {
        "1": ("COM", "GND"), "2": ("NO", "LIM_HOME")}),
    ("SW2", "KW12-3", "Button_Switch_THT:SW_Limit", "End limit (active-LOW)", {
        "1": ("COM", "GND"), "2": ("NO", "LIM_END")}),

    # ── Illumination LED + MOSFET ──
    ("D1", "High-CRI 95+ LED", "LED_THT:LED_D5.0mm", "Pad illumination", {
        "A": ("A", "+5V"), "K": ("K", "LED_NODE")}),
    ("R2", "100R", "Resistor_SMD:R_0805", "LED current limit", {
        "1": ("1", "LED_NODE"), "2": ("2", "LED_DRAIN")}),
    ("Q1", "2N7000", "Package_TO_SOT_THT:TO-92", "LED PWM low-side switch", {
        "G": ("G", "LED_GATE"), "D": ("D", "LED_DRAIN"), "S": ("S", "GND")}),
    ("R3", "220R", "Resistor_SMD:R_0805", "MOSFET gate series", {
        "1": ("1", "LED_PWM"), "2": ("2", "LED_GATE")}),
    ("R4", "100k", "Resistor_SMD:R_0805", "MOSFET gate pulldown", {
        "1": ("1", "LED_GATE"), "2": ("2", "GND")}),

    # ── UV-C sterilization LED module (assumed integral CC driver) ──
    ("D2", "275nm UVC module", "Module:UVC_LED_module", "Tray sterilization", {
        "VIN": ("VIN", "+5V"), "GND": ("GND", "GND"), "EN": ("EN", "UVC_EN")}),
    ("R5", "100k", "Resistor_SMD:R_0805", "UV-C EN pulldown (OFF at boot)", {
        "1": ("1", "UVC_EN"), "2": ("2", "GND")}),

    # ── Load cell amp ──
    ("U10", "HX711 1kg kit", "Module:HX711_breakout", "Sample weight", {
        "VCC": ("VCC", "+3V3"), "GND": ("GND", "GND"),
        "DT": ("DT", "HX_DT"), "SCK": ("SCK", "HX_SCK")}),

    # ── Thermal printer (5V; see ENGINEERING_REVIEW §2.6) ──
    ("PR1", "CSN-A2 thermal", "Connector:Printer_TTL_3pin", "Report printout", {
        "VH":  ("VH",  "+5V"),
        "GND": ("GND", "GND"),
        "RX":  ("RX",  "PRN_TX"),   # printer RX <- MCU TX
        "TX":  ("TX",  "PRN_RX")}), # printer TX -> MCU RX

    # ── Display: SPI TFT (ILI9488) + XPT2046 touch on shared SPI ──
    ("LCD1", "3.5in SPI TFT ILI9488 +touch", "Connector:TFT_SPI_14pin", "UI display", {
        "VCC":  ("VCC",  "+5V"),
        "GND":  ("GND",  "GND"),
        "CS":   ("CS",   "TFT_CS"),
        "RESET":("RESET","TFT_RST"),
        "DC":   ("DC",   "TFT_DC"),
        "SDI":  ("SDI",  "TFT_MOSI"),
        "SCK":  ("SCK",  "TFT_SCLK"),
        "LED":  ("LED",  "TFT_BL"),
        "SDO":  ("SDO",  "TFT_MISO"),
        "T_CLK":("T_CLK","TFT_SCLK"),
        "T_CS": ("T_CS", "TOUCH_CS"),
        "T_DIN":("T_DIN","TFT_MOSI"),
        "T_DO": ("T_DO", "TFT_MISO")}),

    # ── Scan button ──
    ("SW3", "Tactile 6x6", "Button_Switch_THT:SW_PUSH_6mm", "Scan trigger (active-LOW)", {
        "1": ("1", "SCAN_BTN"), "2": ("2", "GND")}),
]


sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import footprints as F

def build_nets():
    """net -> list of (ref, pad_number, pin_name). Pad numbers come from footprints.py
    so the netlist matches the schematic pin numbers and the PCB pads."""
    nets = {}
    for ref, _val, _fp, _desc, pins in COMPONENTS:
        for i, (pin_id, (pin_name, net)) in enumerate(pins.items()):
            pad = F.pad_of(ref, pin_id, i + 1)
            nets.setdefault(net, []).append((ref, pad, pin_name))
    return dict(sorted(nets.items()))


def emit_kicad_net(path):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    out = []
    out.append("(export (version D)")
    out.append('  (design (source "config.h master pin map") '
               f'(date "{ts}") (tool "gen_netlist.py"))')
    # components
    out.append("  (components")
    for ref, val, _fp, desc, _pins in COMPONENTS:
        out.append(f'    (comp (ref "{ref}")')
        out.append(f'      (value "{val}")')
        out.append(f'      (footprint "{F.footprint_of(ref)}")')
        out.append(f'      (description "{desc}"))')
    out.append("  )")
    # nets
    nets = build_nets()
    out.append("  (nets")
    for i, (net, nodes) in enumerate(nets.items(), start=1):
        out.append(f'    (net (code "{i}") (name "{net}")')
        for ref, pin_no, _pin_name in nodes:
            out.append(f'      (node (ref "{ref}") (pin "{pin_no}"))')
        out.append("    )")
    out.append("  )")
    out.append(")")
    with open(path, "w") as f:
        f.write("\n".join(out) + "\n")


def emit_markdown(path):
    nets = build_nets()
    lines = []
    lines.append("# Netlist — Urine Analyzer Lite (Design A)")
    lines.append("")
    lines.append("> Auto-generated by `gen_netlist.py` from the `config.h` master pin map.")
    lines.append("> For engineer verification. Footprints are placeholders — confirm in KiCad.")
    lines.append("")
    lines.append("## Components")
    lines.append("")
    lines.append("| Ref | Value | Footprint | Description |")
    lines.append("|---|---|---|---|")
    for ref, val, _fp, desc, _pins in COMPONENTS:
        lines.append(f"| {ref} | {val} | `{F.footprint_of(ref)}` | {desc} |")
    lines.append("")
    lines.append("## Nets")
    lines.append("")
    lines.append("| Net | Connections (ref.pin = name) |")
    lines.append("|---|---|")
    for net, nodes in nets.items():
        conns = ", ".join(f"{r}.{p} ({n})" for r, p, n in nodes)
        lines.append(f"| **{net}** | {conns} |")
    lines.append("")
    lines.append(f"_Total: {len(COMPONENTS)} components, {len(nets)} nets._")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    emit_kicad_net(os.path.join(here, "urine_analyzer_lite.net"))
    emit_markdown(os.path.join(here, "NETLIST.md"))
    nets = build_nets()
    print(f"Wrote netlist: {len(COMPONENTS)} components, {len(nets)} nets.")
