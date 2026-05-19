#!/usr/bin/env python3
"""
KiCad schematic generator for Urine Analyzer Lite.
Components: ESP32-S3, TCS34725 x2, SHT31, BH1750, ADS1115, N20+MX1508,
            TP4056, LiPo, S13V25F5, HX711, CSN-A2 printer, DSI LCD, UV-C LED.
Run: python3 gen_schematic.py
Output: urine_analyzer_lite.kicad_sch
"""

import uuid, datetime

def uid(): return str(uuid.uuid4())

W = 25.4  # mm to mils factor (not used directly; KiCad 6+ uses mm natively)

# ── Schematic wire/label helpers ──────────────────────────────────────────────

def wire(x1, y1, x2, y2):
    return f"""  (wire (pts (xy {x1} {y1}) (xy {x2} {y2}))
    (stroke (width 0) (type default))
    (uuid "{uid()}"))"""

def pwr_symbol(name, x, y, rot=0):
    return f"""  (power "{name}" (at {x} {y} {rot})
    (fields_autoplaced yes)
    (uuid "{uid()}")
    (property "Reference" "#PWR" (at {x} {y-2} 0) (effects (font (size 1 1)) hide))
    (property "Value" "{name}" (at {x} {y-3.5} 0) (effects (font (size 1 1))))
    (property "Footprint" "" (at {x} {y} 0) (effects (font (size 1 1)) hide))
    (pin "1" (uuid "{uid()}"))
  )"""

def label(name, x, y, rot=0):
    return f"""  (global_label "{name}" (shape input) (at {x} {y} {rot})
    (effects (font (size 1.27 1.27)))
    (uuid "{uid()}")
    (property "Intersheet References" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
  )"""

def net_label(name, x, y, rot=0):
    return f"""  (net_tie_pad_groups "")
  (label "{name}" (at {x} {y} {rot})
    (effects (font (size 1.27 1.27)))
    (uuid "{uid()}"))"""

# ── Component block builder ───────────────────────────────────────────────────

def box_component(ref, val, x, y, width, height, pins_left, pins_right,
                  pins_top=None, pins_bottom=None, color=""):
    """Draws a rectangular component with labeled pins."""
    lines = []
    lines.append(f'  ; ── {ref} : {val} ──')

    # Border rectangle via 4 wires
    x2, y2 = x + width, y + height
    for sx, sy, ex, ey in [(x, y, x2, y), (x2, y, x2, y2),
                            (x2, y2, x, y2), (x, y2, x, y)]:
        lines.append(f'  (wire (pts (xy {sx} {sy}) (xy {ex} {ey}))'
                     f' (stroke (width 0.25) (type default)) (uuid "{uid()}"))')

    # Reference label
    lines.append(f'  (text "{ref}" (at {x + 0.5} {y + 0.8} 0)'
                 f' (effects (font (size 1 1) bold)) (uuid "{uid()}"))')
    lines.append(f'  (text "{val}" (at {x + 0.5} {y + 2} 0)'
                 f' (effects (font (size 0.9 0.9))) (uuid "{uid()}"))')

    pin_step = 2.54
    # Left pins
    for i, (pin_name, net) in enumerate(pins_left):
        py = y + 4 + i * pin_step
        lines.append(f'  (text "{pin_name}" (at {x + 0.5} {py} 0)'
                     f' (effects (font (size 0.9 0.9)) (justify left)) (uuid "{uid()}"))')
        lines.append(wire(x - 5, py, x, py))
        lines.append(f'  (label "{net}" (at {x - 5} {py} 180)'
                     f' (effects (font (size 1 1))) (uuid "{uid()}"))')

    # Right pins
    for i, (pin_name, net) in enumerate(pins_right):
        py = y + 4 + i * pin_step
        lines.append(f'  (text "{pin_name}" (at {x2 - 0.5} {py} 0)'
                     f' (effects (font (size 0.9 0.9)) (justify right)) (uuid "{uid()}"))')
        lines.append(wire(x2, py, x2 + 5, py))
        lines.append(f'  (label "{net}" (at {x2 + 5} {py} 0)'
                     f' (effects (font (size 1 1))) (uuid "{uid()}"))')

    return '\n'.join(lines)


# ── Main schematic builder ────────────────────────────────────────────────────

def build_schematic():
    parts = []

    # ── ESP32-S3 DevKitC-1 ─────────────────────────── col 0 row 0 ──
    parts.append(box_component(
        'U1', 'ESP32-S3-DevKitC-1',
        x=10, y=10, width=30, height=70,
        pins_left=[
            ('3V3',    '3V3'),
            ('GND',    'GND'),
            ('GPIO21',  'I2C_SDA'),
            ('GPIO22',  'I2C_SCL'),
            ('GPIO1',   'ADC_ALERT'),
            ('GPIO4',   'HX711_DT'),
            ('GPIO5',   'HX711_SCK'),
            ('GPIO16',  'UART1_TX'),
            ('GPIO17',  'UART1_RX'),
            ('GPIO18',  'MOTOR_IN1'),
            ('GPIO8',   'MOTOR_IN2'),
            ('GPIO15',  'ENC_A'),
            ('GPIO7',   'ENC_B'),
        ],
        pins_right=[
            ('GPIO2',   'LED_PWM'),
            ('GPIO3',   'UVC_EN'),
            ('GPIO9',   'SCAN_BTN'),
            ('GPIO10',  'LIMIT_HOME'),
            ('GPIO11',  'LIMIT_END'),
            ('GPIO12',  'DSI_CLK'),
            ('GPIO13',  'DSI_D0P'),
            ('GPIO14',  'DSI_D0N'),
            ('GPIO6',   'PRINTER_TX'),
            ('GPIO19',  'PRINTER_RX'),
            ('5V',      '5V'),
            ('GND',     'GND'),
        ],
    ))

    # ── Power: TP4056 USB-C charger ─────────────────── col 1 row 0 ──
    parts.append(box_component(
        'U2', 'TP4056 USB-C Charger',
        x=60, y=10, width=22, height=26,
        pins_left=[
            ('USB_IN+', 'VUSB'),
            ('USB_IN-', 'GND'),
        ],
        pins_right=[
            ('B+',  'LIPO_P'),
            ('B-',  'GND'),
            ('OUT+','VREG_IN'),
            ('OUT-','GND'),
        ],
    ))

    # ── Power: LiPo 3.7V 2000mAh ────────────────────── col 1 row 1 ──
    parts.append(box_component(
        'BT1', '3.7V 2000mAh LiPo',
        x=60, y=50, width=22, height=14,
        pins_left=[
            ('B+', 'LIPO_P'),
            ('B-', 'GND'),
        ],
        pins_right=[],
    ))

    # ── Power: S13V25F5 Buck-Boost ───────────────────── col 1 row 2 ──
    parts.append(box_component(
        'U3', 'S13V25F5 5V Reg',
        x=60, y=78, width=22, height=18,
        pins_left=[
            ('VIN', 'VREG_IN'),
            ('GND', 'GND'),
            ('EN',  '3V3'),
        ],
        pins_right=[
            ('VOUT', '5V'),
            ('GND',  'GND'),
        ],
    ))

    # ── I2C Bus: TCS34725 RGB Sensor #1 ─────────────── col 2 row 0 ──
    parts.append(box_component(
        'U4', 'TCS34725 RGB #1',
        x=110, y=10, width=22, height=18,
        pins_left=[
            ('VCC',  '3V3'),
            ('GND',  'GND'),
            ('SCL',  'I2C_SCL'),
            ('SDA',  'I2C_SDA'),
        ],
        pins_right=[
            ('INT', 'ADC_ALERT'),
        ],
    ))

    # ── I2C Bus: TCS34725 RGB Sensor #2 ─────────────── col 2 row 1 ──
    parts.append(box_component(
        'U5', 'TCS34725 RGB #2',
        x=110, y=40, width=22, height=18,
        pins_left=[
            ('VCC',  '3V3'),
            ('GND',  'GND'),
            ('SCL',  'I2C_SCL'),
            ('SDA',  'I2C_SDA'),
            ('LED',  'LED_PWM'),
        ],
        pins_right=[],
    ))

    # ── I2C Bus: SHT31 Temp/Humidity ────────────────── col 2 row 2 ──
    parts.append(box_component(
        'U6', 'SHT31-D Env Sensor',
        x=110, y=70, width=22, height=18,
        pins_left=[
            ('VIN', '3V3'),
            ('GND', 'GND'),
            ('SCL', 'I2C_SCL'),
            ('SDA', 'I2C_SDA'),
        ],
        pins_right=[],
    ))

    # ── I2C Bus: BH1750 Ambient Light ───────────────── col 2 row 3 ──
    parts.append(box_component(
        'U7', 'BH1750 Light Sensor',
        x=110, y=100, width=22, height=18,
        pins_left=[
            ('VCC',  '3V3'),
            ('GND',  'GND'),
            ('SCL',  'I2C_SCL'),
            ('SDA',  'I2C_SDA'),
            ('ADDR', 'GND'),
        ],
        pins_right=[],
    ))

    # ── I2C Bus: ADS1115 16-bit ADC ─────────────────── col 2 row 4 ──
    parts.append(box_component(
        'U8', 'ADS1115 ADC',
        x=110, y=130, width=22, height=18,
        pins_left=[
            ('VDD',  '3V3'),
            ('GND',  'GND'),
            ('SCL',  'I2C_SCL'),
            ('SDA',  'I2C_SDA'),
            ('ADDR', 'GND'),
        ],
        pins_right=[
            ('ALRT', 'ADC_ALERT'),
            ('AIN0', 'NTC_SIGNAL'),
        ],
    ))

    # ── NTC Thermistor ──────────────────────────────── col 3 row 4 ──
    parts.append(box_component(
        'RT1', 'NTC Thermistor 10k',
        x=160, y=130, width=18, height=10,
        pins_left=[
            ('T1', 'NTC_SIGNAL'),
            ('T2', 'GND'),
        ],
        pins_right=[],
    ))

    # ── Motor: N20 + MX1508 H-Bridge ────────────────── col 3 row 0 ──
    parts.append(box_component(
        'U9', 'MX1508 H-Bridge',
        x=160, y=10, width=22, height=22,
        pins_left=[
            ('VCC',  '5V'),
            ('GND',  'GND'),
            ('IN1',  'MOTOR_IN1'),
            ('IN2',  'MOTOR_IN2'),
        ],
        pins_right=[
            ('OUT1', 'MOTOR_A'),
            ('OUT2', 'MOTOR_B'),
        ],
    ))
    parts.append(box_component(
        'M1', 'N20 DC Motor+Encoder',
        x=200, y=10, width=22, height=22,
        pins_left=[
            ('M+',   'MOTOR_A'),
            ('M-',   'MOTOR_B'),
            ('VCC',  '3V3'),
            ('GND',  'GND'),
            ('ENC_A','ENC_A'),
            ('ENC_B','ENC_B'),
        ],
        pins_right=[],
    ))

    # ── Limit Switches ──────────────────────────────── col 3 row 1 ──
    parts.append(box_component(
        'SW1', 'KW12-3 Home Limit',
        x=160, y=45, width=20, height=10,
        pins_left=[
            ('COM', 'GND'),
            ('NO',  'LIMIT_HOME'),
        ],
        pins_right=[],
    ))
    parts.append(box_component(
        'SW2', 'KW12-3 End Limit',
        x=160, y=65, width=20, height=10,
        pins_left=[
            ('COM', 'GND'),
            ('NO',  'LIMIT_END'),
        ],
        pins_right=[],
    ))

    # ── High-CRI LED + MOSFET ───────────────────────── col 3 row 2 ──
    parts.append(box_component(
        'Q1', '2N7000 N-Ch MOSFET',
        x=160, y=85, width=20, height=14,
        pins_left=[
            ('G', 'LED_PWM'),
            ('S', 'GND'),
        ],
        pins_right=[
            ('D', 'LED_K'),
        ],
    ))
    parts.append(box_component(
        'D1', 'High-CRI LED 95+ CRI',
        x=190, y=85, width=18, height=10,
        pins_left=[
            ('A', '3V3'),
            ('K', 'LED_K'),
        ],
        pins_right=[],
    ))

    # ── UV-C LED ────────────────────────────────────── col 3 row 3 ──
    parts.append(box_component(
        'D2', '275nm UVC LED',
        x=160, y=110, width=18, height=10,
        pins_left=[
            ('EN',  'UVC_EN'),
            ('GND', 'GND'),
        ],
        pins_right=[],
    ))

    # ── HX711 Load Cell ─────────────────────────────── col 4 row 0 ──
    parts.append(box_component(
        'U10', 'HX711 Load Cell Amp',
        x=240, y=10, width=22, height=22,
        pins_left=[
            ('VCC', '3V3'),
            ('GND', 'GND'),
            ('DT',  'HX711_DT'),
            ('SCK', 'HX711_SCK'),
        ],
        pins_right=[
            ('E+', 'CELL_EP'),
            ('E-', 'CELL_EN'),
            ('A+', 'CELL_AP'),
            ('A-', 'CELL_AN'),
        ],
    ))
    parts.append(box_component(
        'FS1', 'Load Cell 1kg',
        x=275, y=10, width=18, height=18,
        pins_left=[
            ('E+', 'CELL_EP'),
            ('E-', 'CELL_EN'),
            ('A+', 'CELL_AP'),
            ('A-', 'CELL_AN'),
        ],
        pins_right=[],
    ))

    # ── Thermal Printer CSN-A2 ──────────────────────── col 4 row 1 ──
    parts.append(box_component(
        'PR1', 'CSN-A2 Thermal Printer',
        x=240, y=45, width=22, height=18,
        pins_left=[
            ('VH',  '5V'),
            ('GND', 'GND'),
            ('TX',  'PRINTER_RX'),
            ('RX',  'PRINTER_TX'),
        ],
        pins_right=[],
    ))

    # ── Scan Button ─────────────────────────────────── col 4 row 2 ──
    parts.append(box_component(
        'SW3', 'Scan Button 6x6mm',
        x=240, y=75, width=18, height=10,
        pins_left=[
            ('P1', '3V3'),
            ('P2', 'SCAN_BTN'),
        ],
        pins_right=[],
    ))

    # ── 4.3" DSI LCD ────────────────────────────────── col 4 row 3 ──
    parts.append(box_component(
        'LCD1', 'Waveshare 4.3in DSI LCD',
        x=240, y=100, width=24, height=18,
        pins_left=[
            ('VCC',   '3V3'),
            ('GND',   'GND'),
            ('DCLK',  'DSI_CLK'),
            ('D0+',   'DSI_D0P'),
            ('D0-',   'DSI_D0N'),
        ],
        pins_right=[],
    ))

    # ── Assemble ─────────────────────────────────────────────────────
    header = f"""(kicad_sch (version 20230121) (generator "urine_analyzer_lite_gen")

  (uuid "{uid()}")

  (paper "A1")

  (title_block
    (title "Urine Analyzer Lite — Schematic")
    (date "{datetime.date.today()}")
    (rev "1.0")
    (company "Levram Lifesciences")
  )

"""
    footer = "\n)\n"
    body = '\n\n'.join(parts)
    return header + body + footer


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == '__main__':
    import os
    out = os.path.join(os.path.dirname(__file__), 'urine_analyzer_lite.kicad_sch')
    content = build_schematic()
    with open(out, 'w') as f:
        f.write(content)
    print(f"Written: {out}  ({len(content):,} bytes)")
