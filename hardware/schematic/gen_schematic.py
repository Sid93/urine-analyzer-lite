#!/usr/bin/env python3
"""Generate an ERC-validated KiCad schematic for Urine Analyzer Lite (Design A).

Single source of truth: ../netlist/gen_netlist.py (components/pins/nets) + ../footprints.py
(real KiCad footprints + pad map). Jellybean discretes use REAL KiCad library symbols
(Device:R/C/C_Polarized/LED/Battery_Cell/Thermistor, Switch:SW_Push) embedded from KiCad's
shared symbol libs; modules/MOSFET use generic rectangles (no stock symbol exists). Real
footprints are written into every symbol's Footprint property so they flow to the PCB.

Connectivity = a global label (net name) on each pin's connection point
(abs = ox + px, oy - py). Validate: kicad-cli sch erc / export netlist.

Run: python3 gen_schematic.py
"""
import sys, os, re, uuid

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "netlist"))
sys.path.insert(0, os.path.join(HERE, ".."))
import gen_netlist as g
import footprints as F

KICAD_SYM = "/Applications/KiCad.app/Contents/SharedSupport/symbols"
ROOT = str(uuid.uuid4())
def u(): return str(uuid.uuid4())

PITCH = 2.54
BODY_W = 33.02
COL_STEP = 96.52
COL_X0 = 50.8
ROW_Y0 = 30.48
COL_H = 558.8
MARGIN = 7.62

# Refs that use a real library symbol: ref -> (lib, symname, {pin_id: sym_pin_number})
REAL_SYM = {
    **{r: ("Device", "R", {"1": "1", "2": "2"}) for r in ("R1", "R2", "R3", "R4", "R5")},
    "C3":  ("Device", "C", {"1": "1", "2": "2"}),
    "C1":  ("Device", "C_Polarized", {"1": "1", "2": "2"}),
    "C2":  ("Device", "C_Polarized", {"1": "1", "2": "2"}),
    "RT1": ("Device", "Thermistor", {"1": "1", "2": "2"}),
    "D1":  ("Device", "LED", {"K": "1", "A": "2"}),
    "BT1": ("Device", "Battery_Cell", {"1": "1", "2": "2"}),
    "SW1": ("Switch", "SW_Push", {"1": "1", "2": "2"}),
    "SW2": ("Switch", "SW_Push", {"1": "1", "2": "2"}),
    "SW3": ("Switch", "SW_Push", {"1": "1", "2": "2"}),
}

def extract_symbol_block(lib, symname):
    """Return (block_text_with_lib_id, {pin_number: (x, y)}) for a library symbol."""
    txt = open(os.path.join(KICAD_SYM, lib + ".kicad_sym")).read()
    start = txt.find(f'(symbol "{symname}"')
    assert start >= 0, f"{lib}:{symname} not found"
    depth = 0; i = start; end = len(txt)
    while i < len(txt):
        if txt[i] == "(": depth += 1
        elif txt[i] == ")":
            depth -= 1
            if depth == 0:
                end = i + 1; break
        i += 1
    block = txt[start:end]
    block = block.replace(f'(symbol "{symname}"', f'(symbol "{lib}:{symname}"', 1)
    pins = {}
    for m in re.finditer(r'\(pin \w+ \w+\s*\(at ([-\d.]+) ([-\d.]+) \d+\)\s*\(length [\d.]+\).*?\(number "([^"]*)"', block, re.S):
        pins[m.group(3)] = (float(m.group(1)), float(m.group(2)))
    return block, pins

def custom_def(ref, value, pins):
    n = len(pins)
    out = [f'\t\t(symbol "ual:{ref}"',
           '\t\t\t(exclude_from_sim no)(in_bom yes)(on_board yes)(pin_names (offset 0.508))',
           f'\t\t\t(property "Reference" "{ref[0] if ref[0].isalpha() else "U"}" (at 0 {PITCH*1.5:.2f} 0)(effects (font (size 1.27 1.27))))',
           f'\t\t\t(property "Value" "{value}" (at 0 {-(n*PITCH):.2f} 0)(effects (font (size 1.27 1.27))))',
           '\t\t\t(property "Footprint" "" (at 0 0 0)(effects (font (size 1.27 1.27))(hide yes)))',
           f'\t\t\t(symbol "{ref}_0_1"',
           f'\t\t\t\t(rectangle (start 0 {PITCH:.2f})(end {BODY_W:.2f} {-(n*PITCH):.2f})(stroke (width 0.1524)(type default))(fill (type background)))',
           '\t\t\t)', f'\t\t\t(symbol "{ref}_1_1"']
    geo = {}
    for i, (pin_id, (pinname, _net)) in enumerate(pins):
        pad = F.pad_of(ref, pin_id, i + 1)
        label = f"{pad}:{pinname}" if pinname != pin_id else pad
        out.append(f'\t\t\t\t(pin passive line (at 0 {-i*PITCH:.2f} 0)(length 2.54)'
                   f'(name "{pinname}" (effects (font (size 1.0 1.0))))(number "{pad}" (effects (font (size 0.8 0.8)))))')
        geo[pin_id] = (0.0, -i * PITCH, pad)
    out += ['\t\t\t)', '\t\t)']
    return "\n".join(out), geo

def instance(lib_id, ref, value, footprint, oxy, pinmap_numbers):
    ox, oy = oxy
    out = [f'\t(symbol (lib_id "{lib_id}")(at {ox:.2f} {oy:.2f} 0)(unit 1)'
           '(exclude_from_sim no)(in_bom yes)(on_board yes)(dnp no)',
           f'\t\t(uuid "{u()}")',
           f'\t\t(property "Reference" "{ref}" (at {ox+BODY_W/2:.2f} {oy+PITCH*2:.2f} 0)(effects (font (size 1.27 1.27))))',
           f'\t\t(property "Value" "{value}" (at {ox+BODY_W/2:.2f} {oy-PITCH*2:.2f} 0)(effects (font (size 1.0 1.0))))',
           f'\t\t(property "Footprint" "{footprint}" (at {ox:.2f} {oy:.2f} 0)(effects (font (size 1.27 1.27))(hide yes)))']
    for pn in pinmap_numbers:
        out.append(f'\t\t(pin "{pn}" (uuid "{u()}"))')
    out.append(f'\t\t(instances (project "urine_analyzer_lite" (path "/{ROOT}" (reference "{ref}")(unit 1))))')
    out.append('\t)')
    return "\n".join(out)

def main():
    comps = g.COMPONENTS
    real_defs, real_pins = {}, {}
    for lib, sym, _ in REAL_SYM.values():
        key = f"{lib}:{sym}"
        if key not in real_defs:
            block, pins = extract_symbol_block(lib, sym)
            real_defs[key] = block; real_pins[key] = pins

    header = ['(kicad_sch', '\t(version 20250114)', '\t(generator "gen_schematic.py")',
              '\t(generator_version "9.0")', f'\t(uuid "{ROOT}")', '\t(paper "A1")', '\t(lib_symbols']
    libsyms = ["\t\t" + d if not d.startswith("\t") else d for d in real_defs.values()]
    body, custom_geo = [], {}
    ox, oy = COL_X0, ROW_Y0
    placements = []
    for ref, val, _fp, _d, pins in comps:
        pl = list(pins.items())
        h = len(pl) * PITCH + MARGIN
        if oy + h > COL_H:
            ox += COL_STEP; oy = ROW_Y0
        placements.append((ref, val, pl, (ox, oy)))
        if ref not in REAL_SYM:
            cdef, geo = custom_def(ref, val, pl)
            libsyms.append(cdef); custom_geo[ref] = geo
        oy += h

    for ref, val, pl, (ox, oy) in placements:
        fp = F.footprint_of(ref)
        if ref in REAL_SYM:
            lib, sym, idmap = REAL_SYM[ref]
            key = f"{lib}:{sym}"; symbol_pins = real_pins[key]
            numbers = [idmap[pid] for pid, _ in pl]
            body.append(instance(key, ref, val, fp, (ox, oy), numbers))
            for pid, (pname, net) in pl:
                spn = idmap[pid]; px, py = symbol_pins[spn]
                body.append(f'\t(global_label "{net}" (shape input)(at {ox+px:.2f} {oy-py:.2f} 0)'
                            f'(effects (font (size 1.27 1.27))(justify left))(uuid "{u()}"))')
        else:
            geo = custom_geo[ref]
            numbers = [geo[pin_id][2] for pin_id, _ in pl]
            body.append(instance(f"ual:{ref}", ref, val, fp, (ox, oy), numbers))
            for pin_id, (pname, net) in pl:
                px, py, _pad = geo[pin_id]
                body.append(f'\t(global_label "{net}" (shape input)(at {ox+px:.2f} {oy-py:.2f} 180)'
                            f'(effects (font (size 1.27 1.27))(justify right))(uuid "{u()}"))')

    footer = ['\t(sheet_instances', '\t\t(path "/" (page "1"))', '\t)', ')']
    txt = "\n".join(header + libsyms + ['\t)'] + body + footer) + "\n"
    open(os.path.join(HERE, "urine_analyzer_lite.kicad_sch"), "w").write(txt)
    print(f"wrote schematic: {len(comps)} components ({len(REAL_SYM)} real-symbol, rest custom)")

if __name__ == "__main__":
    main()
