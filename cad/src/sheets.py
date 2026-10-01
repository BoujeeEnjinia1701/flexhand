"""FlexHand drawing sheets.

Run from the repo root:  python cad/src/sheets.py
Builds FXH-DWG-001 (general arrangement, Rev P3) in cad/drawings/ from cad/src/model.py.
FXH-DWG-010 is the concept sheet made by cad/src/concept_media.py.
"""
import copy
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(ROOT / "cad" / "src"))
from build123d import Compound, Plane, mirror  # noqa: E402
from drawing import Sheet, project_views  # noqa: E402
import model  # noqa: E402
import svg_patch  # noqa: E402,F401  (skips degenerate SVG arcs)

M = model.build_parts()
P, d = M["parts"], M["d"]
FOREARM_UNIT = ["forearm_cuff", "pack_base", "pack_lid", "gearmotors", "spools", "idlers", "cells", "controller",
                "drivers", "charger", "estop", "anchor_block", "balance_pulleys", "tray", "regulator", "fixings"]
unit = Compound(children=[copy.copy(P[k]) for k in FOREARM_UNIT])
device = Compound(children=[copy.copy(s) for s in P.values()])   # right hand, as in the media and build plan

work = ROOT / "cad" / "drawings" / "_views"
views = project_views(unit, work / "unit")
iso = project_views(device, work / "device")["iso"]

s = Sheet(project="FlexHand", title="Forearm unit general arrangement", dwg_no="FXH-DWG-001", rev="P3",
          author="Amish Chadha", date="2026-10-01", scale=0.5, concept=True,
          material="Pack and cuff PETG; plates and cuffs TPU 95A; bought parts per bom/bom.csv. "
                   "PRELIMINARY, NOT FOR FABRICATION",
          revisions=[("P1", "General arrangement for TRL 3 (FXH-CAL-001)", "2026-09-25", "AC"),
                     ("P2", "FXH-DDR-002: balance pulleys, 44 mm anchor block, perforated cuff, thimbles", "2026-09-25", "AC"),
                     ("P3", "FXH-DDR-003: constructable design", "2026-10-01", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(iso, 276, 32, 140, 70, label="Isometric view, whole device",
          sublabel="Right-hand device as modelled; a left-hand device is its mirror image; not to scale")
fg = d["finger_geom"]
s.add_notes("Main dimensions (mm)", [
    f"Pack {d['pack_l']:.0f} long x {d['pack_w']:.0f} wide; walls {d['wall']:.0f}, lid {d['lid_t']:.0f}",
    f"Pack top {d['pack_top']:.1f} above forearm axis; wrist to pack front {-d['pack_x'][1]:.0f}",
    f"Gearmotors 25 dia x {d['motor_l']:.0f}, axes along forearm at y = +/-{d['motor_y']:.1f}",
    f"Spools: core {d['spool_core_d']:.0f} dia, flanges {d['spool_flange_d']:.0f} dia, {d['spool_w']:.0f} wide",
    f"Tendon exits at y = +/-{d['line_y']:.2f}; idlers {d['idler_d']:.0f} dia (623ZZ class) on 3 mm pins",
    f"Cells 2 x 18650 across the pack at x = {d['cell_x'][0]:.0f}, {d['cell_x'][1]:.0f}",
    f"Forearm cuff {d['cuff_x'][1] - d['cuff_x'][0]:.0f} long; shell {d['cuff_t']:.0f}, liner {d['liner_t']:.0f}; {d['cuff_hole_d']:.0f} dia holes; straps {d['strap_w']:.0f} wide",
    f"Anchor block {d['anchor_l']:.0f} long x {d['anchor_w']:.0f} wide, {d['anchor_total_l']:.0f} with cover; pulleys {d['balance_d']:.0f} dia, {d['balance_travel']:.0f} travel",
    "Anchor cuffs (index, middle, ring, little): " + ", ".join(f"{f['anchor_w']:.1f}" for f in fg),
    "Thimbles (index, middle, ring, little): " + ", ".join(f"{f['thimble_w']:.1f}" for f in fg),
    f"Guide cuffs {d['guide_cuff_w']:.0f} wide; plates TPU {d['plate_t']:.1f} thick",
], x=276, y=118, width=140)
s.add_notes("Parts list (items match bom/bom.csv)", [
    "1 Forearm cuff with liner and straps",
    "2 Pack base",
    "3 Gearmotor with encoder (2)",
    "4 Antagonistic spool (2)",
    "5 Li-ion cells and 2S BMS",
    "6 Controller",
    "7 Motor driver (2)",
    "8 Pack lid",
    "9 Emergency stop",
    "10 Anchor block, release plate, cover",
], x=20, y=204, width=80)
s.add_notes("Parts list, continued", [
    "11 Bowden sheaths (8)",
    "12 to 17, 21 Hand side (iso only)",
    "18 USB-C charger",
    "19 Wiring (not shown)",
    "20 Idler bearings (4)",
    "22 Balance pulleys (4)",
    "23 Tray; 24 Fixings; 25 5 V regulator",
    "Not a medical device.",
    "Research use under supervision.",
    "Never charge while worn.",
], x=104, y=204, width=80)
s.save(ROOT / "cad" / "drawings" / "FXH-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("Wrote cad/drawings/FXH-DWG-001.svg, .pdf and .png")
