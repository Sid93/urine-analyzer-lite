"""Real KiCad footprint assignment for Urine Analyzer Lite components.
Footprint nickname = the .pretty directory name in KiCad's shared footprints.
Modules/breakouts use 2.54mm pin headers sized to their wired-pin count: the engineer
must confirm the physical pin ORDER against each module's datasheet/silkscreen.
Discretes (R/C/LED/Q/NTC/battery) use real device footprints.
"""

HDR = "Connector_PinHeader_2.54mm"

FOOTPRINTS = {
    "U1":  f"{HDR}:PinHeader_2x22_P2.54mm_Vertical",         # ESP32-S3-DevKitC-1 board header
    "BT1": "Connector_JST:JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal",
    "U2":  f"{HDR}:PinHeader_1x06_P2.54mm_Vertical",          # TP4056
    "U3":  f"{HDR}:PinHeader_1x04_P2.54mm_Vertical",          # S13V25F5
    "U12": "Package_TO_SOT_SMD:SOT-223-3_TabPin2",            # AMS1117-3.3
    "C1":  "Capacitor_THT:CP_Radial_D10.0mm_P5.00mm",
    "C2":  "Capacitor_THT:CP_Radial_D8.0mm_P3.50mm",
    "C3":  "Capacitor_SMD:C_0805_2012Metric",
    "U11": f"{HDR}:PinHeader_1x12_P2.54mm_Vertical",          # TCA9548A breakout
    "U4":  f"{HDR}:PinHeader_1x04_P2.54mm_Vertical",          # TCS34725 #1
    "U5":  f"{HDR}:PinHeader_1x04_P2.54mm_Vertical",          # TCS34725 #2
    "U6":  f"{HDR}:PinHeader_1x05_P2.54mm_Vertical",          # SHT31
    "U7":  f"{HDR}:PinHeader_1x05_P2.54mm_Vertical",          # BH1750
    "U8":  f"{HDR}:PinHeader_1x06_P2.54mm_Vertical",          # ADS1115
    "RT1": "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal",
    "R1":  "Resistor_SMD:R_0805_2012Metric",
    "U9":  f"{HDR}:PinHeader_1x06_P2.54mm_Vertical",          # MX1508
    "M1":  f"{HDR}:PinHeader_1x06_P2.54mm_Vertical",          # N20 motor + encoder
    "SW1": f"{HDR}:PinHeader_1x02_P2.54mm_Vertical",
    "SW2": f"{HDR}:PinHeader_1x02_P2.54mm_Vertical",
    "D1":  "LED_THT:LED_D5.0mm_Clear",
    "R2":  "Resistor_SMD:R_0805_2012Metric",
    "Q1":  "Package_TO_SOT_THT:TO-92_Inline",
    "R3":  "Resistor_SMD:R_0805_2012Metric",
    "R4":  "Resistor_SMD:R_0805_2012Metric",
    "D2":  f"{HDR}:PinHeader_1x03_P2.54mm_Vertical",          # UV-C module
    "R5":  "Resistor_SMD:R_0805_2012Metric",
    "U10": f"{HDR}:PinHeader_1x04_P2.54mm_Vertical",          # HX711
    "PR1": f"{HDR}:PinHeader_1x04_P2.54mm_Vertical",          # CSN-A2 printer
    "LCD1": f"{HDR}:PinHeader_1x13_P2.54mm_Vertical",         # SPI TFT + touch
    "SW3": f"{HDR}:PinHeader_1x02_P2.54mm_Vertical",
}

# Pin-id -> pad-number overrides (where pad != position-in-order).
PAD_OVERRIDE = {
    "D1": {"A": "2", "K": "1"},          # LED_D5.0mm: pad1=K, pad2=A
    "Q1": {"S": "1", "G": "2", "D": "3"},# 2N7000 TO-92 (verify orientation)
}

def footprint_of(ref):
    return FOOTPRINTS.get(ref, "")

def pad_of(ref, pin_id, position):
    """position is 1-based index in the component's pin order."""
    ov = PAD_OVERRIDE.get(ref)
    if ov and pin_id in ov:
        return ov[pin_id]
    return str(position)
