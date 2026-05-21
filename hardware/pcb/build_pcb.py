#!/usr/bin/env python3
"""Build a starting KiCad PCB for Urine Analyzer Lite from the netlist model.

Loads the real footprints (footprints.py), assigns nets to pads from the model
(gen_netlist.build_nets), arranges parts on a grid, and adds a board outline.
Components are PLACED but UNROUTED — the engineer does placement refinement + routing.

Run with KiCad's bundled Python (has the pcbnew module):
  /Applications/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 build_pcb.py
"""
import sys, os, math
import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "netlist"))
sys.path.insert(0, os.path.join(HERE, ".."))
import gen_netlist as g
import footprints as F

FP_BASE = "/Applications/KiCad.app/Contents/SharedSupport/footprints"

def mm(v):  # mm -> internal units
    return pcbnew.FromMM(v)

def main():
    board = pcbnew.CreateEmptyBoard()

    # (ref, pad) -> net name
    padnet = {}
    for net, nodes in g.build_nets().items():
        for ref, pad, _name in nodes:
            padnet[(ref, pad)] = net

    nets = {}
    def get_net(name):
        if name not in nets:
            ni = pcbnew.NETINFO_ITEM(board, name)
            board.Add(ni)
            nets[name] = ni
        return nets[name]

    # grid placement
    cols = 6
    dx, dy = 42.0, 42.0
    x0, y0 = 30.0, 30.0
    placed = 0
    for i, (ref, val, _fp, _desc, _pins) in enumerate(g.COMPONENTS):
        fp = F.footprint_of(ref)
        nick, name = fp.split(":")
        mod = pcbnew.FootprintLoad(os.path.join(FP_BASE, nick + ".pretty"), name)
        if mod is None:
            print("MISSING FP", ref, fp); continue
        mod.SetReference(ref)
        mod.SetValue(val)
        col, row = i % cols, i // cols
        mod.SetPosition(pcbnew.VECTOR2I(mm(x0 + col * dx), mm(y0 + row * dy)))
        board.Add(mod)
        for p in mod.Pads():
            key = (ref, p.GetNumber())
            if key in padnet:
                p.SetNet(get_net(padnet[key]))
        placed += 1

    # board outline (Edge.Cuts) around the placement grid
    rows = math.ceil(len(g.COMPONENTS) / cols)
    w = x0 + cols * dx + 10
    h = y0 + rows * dy + 10
    pts = [(10, 10), (w, 10), (w, h), (10, h), (10, 10)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        seg = pcbnew.PCB_SHAPE(board)
        seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
        seg.SetStart(pcbnew.VECTOR2I(mm(ax), mm(ay)))
        seg.SetEnd(pcbnew.VECTOR2I(mm(bx), mm(by)))
        seg.SetLayer(pcbnew.Edge_Cuts)
        seg.SetWidth(mm(0.15))
        board.Add(seg)

    out = os.path.join(HERE, "urine_analyzer_lite.kicad_pcb")
    pcbnew.SaveBoard(out, board)
    print(f"wrote PCB: {placed} footprints, {len(nets)} nets, outline {w:.0f}x{h:.0f} mm")

if __name__ == "__main__":
    main()
