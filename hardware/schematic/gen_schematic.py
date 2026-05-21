#!/usr/bin/env python3
"""Generate a connected KiCad schematic from the netlist model in gen_netlist.py.
Connectivity = a global label (net name) placed exactly on each pin's connection point
(abs = ox, oy - py). Global labels join by name across the sheet. Pins are 'passive' to
minimise ERC pin-type noise. Aesthetics are secondary; goal = ERC-clean connectivity."""
import sys, os, uuid
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "netlist"))
import gen_netlist as g

ROOT = str(uuid.uuid4())
def u(): return str(uuid.uuid4())

PITCH = 2.54
BODY_W = 33.02            # 13*2.54, on-grid
COL_STEP = 96.52         # 38*2.54
COL_X0 = 50.8            # 20*2.54
ROW_Y0 = 30.48           # 12*2.54
COL_H = 558.8            # 220*2.54
MARGIN = 7.62            # 3*2.54

def sym_def(ref, value, pins):
    n = len(pins)
    lines = [f'\t\t(symbol "ual:{ref}"',
             '\t\t\t(exclude_from_sim no)(in_bom yes)(on_board yes)',
             '\t\t\t(pin_names (offset 0.508))',
             f'\t\t\t(property "Reference" "{ref[0] if ref[0].isalpha() else "U"}" (at 0 {PITCH*1.5:.2f} 0)(effects (font (size 1.27 1.27))))',
             f'\t\t\t(property "Value" "{value}" (at 0 {-(n*PITCH):.2f} 0)(effects (font (size 1.27 1.27))))',
             f'\t\t\t(property "Footprint" "" (at 0 0 0)(effects (font (size 1.27 1.27))(hide yes)))',
             f'\t\t\t(symbol "{ref}_0_1"',
             f'\t\t\t\t(rectangle (start 0 {PITCH:.2f})(end {BODY_W:.2f} {-(n*PITCH):.2f})(stroke (width 0.1524)(type default))(fill (type background)))',
             '\t\t\t)',
             f'\t\t\t(symbol "{ref}_1_1"']
    for i, (pinno, (pinname, _net)) in enumerate(pins):
        py = -i * PITCH
        lines.append(f'\t\t\t\t(pin passive line (at 0 {py:.2f} 0)(length 2.54)'
                     f'(name "{pinname}" (effects (font (size 1.0 1.0))))'
                     f'(number "{pinno}" (effects (font (size 0.8 0.8)))))')
    lines += ['\t\t\t)', '\t\t)']
    return "\n".join(lines)

def instance(ref, value, footprint, pins, ox, oy):
    out = [f'\t(symbol (lib_id "ual:{ref}")(at {ox:.2f} {oy:.2f} 0)(unit 1)'
           '(exclude_from_sim no)(in_bom yes)(on_board yes)(dnp no)',
           f'\t\t(uuid "{u()}")',
           f'\t\t(property "Reference" "{ref}" (at {ox+BODY_W/2:.2f} {oy+PITCH*1.5:.2f} 0)(effects (font (size 1.27 1.27))))',
           f'\t\t(property "Value" "{value}" (at {ox+BODY_W/2:.2f} {oy-(len(pins)*PITCH):.2f} 0)(effects (font (size 1.0 1.0))))',
           f'\t\t(property "Footprint" "{footprint}" (at {ox:.2f} {oy:.2f} 0)(effects (font (size 1.27 1.27))(hide yes)))']
    for pinno, _ in pins:
        out.append(f'\t\t(pin "{pinno}" (uuid "{u()}"))')
    out.append(f'\t\t(instances (project "urine_analyzer_lite" (path "/{ROOT}" (reference "{ref}")(unit 1))))')
    out.append('\t)')
    return "\n".join(out)

def labels(pins, ox, oy):
    out = []
    for i, (_pinno, (_pinname, net)) in enumerate(pins):
        ay = oy - (-i * PITCH)   # oy - py, py = -i*PITCH  => oy + i*PITCH
        out.append(f'\t(global_label "{net}" (shape input)(at {ox:.2f} {ay:.2f} 180)'
                   f'(effects (font (size 1.27 1.27))(justify right))(uuid "{u()}"))')
    return "\n".join(out)

def main():
    comps = g.COMPONENTS
    header = ['(kicad_sch', '\t(version 20250114)', '\t(generator "gen_sch.py")',
              '\t(generator_version "9.0")', f'\t(uuid "{ROOT}")', '\t(paper "A1")',
              '\t(lib_symbols']
    defs = [sym_def(ref, val, list(pins.items())) for ref, val, _fp, _d, pins in comps]
    body = ['\t)']
    ox, oy = COL_X0, ROW_Y0
    for ref, val, fp, _d, pins in comps:
        pl = list(pins.items())
        h = len(pl) * PITCH + MARGIN
        if oy + h > COL_H:
            ox += COL_STEP; oy = ROW_Y0
        body.append(instance(ref, val, fp, pl, ox, oy))
        body.append(labels(pl, ox, oy))
        oy += h
    footer = ['\t(sheet_instances', '\t\t(path "/" (page "1"))', '\t)', ')']
    txt = "\n".join(header + defs + body + footer) + "\n"
    here = os.path.dirname(os.path.abspath(__file__))
    open(os.path.join(here, "urine_analyzer_lite.kicad_sch"), "w").write(txt)
    print("wrote schematic")

if __name__ == "__main__":
    main()
