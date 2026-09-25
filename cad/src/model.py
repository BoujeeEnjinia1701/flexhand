"""FlexHand parametric model (build123d), TRL 3 massing-plus level.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl.

Axes (right forearm and hand, palm down): X runs from the elbow toward the fingertips with
the wrist at X = 0, Y is across the forearm with +Y on the thumb (radial) side, Z is dorsal (up).
A left-hand device is the mirror image about the XZ plane.

Detail level: correct interfaces and main dimensions (pack envelope, gearmotor and spool
positions, tendon exits and idlers, sheath stops, finger cuff widths, plates) with the forearm
and hand as context. Not fabrication detail. PRELIMINARY, NOT FOR FABRICATION.
"""
from math import pi
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # ---- context anthropometry (adult, medium glove size, hand length about 183 mm) ----
    "arm_l": 270.0, "r_elbow": 38.0, "r_wrist": 29.0,
    "palm_l": 95.0, "palm_w": 80.0, "palm_t": 28.0,
    # finger (lateral y, length from MCP, radius); index, middle, ring, little
    "fingers": [(29.0, 80.0, 9.0), (9.5, 88.0, 9.0), (-10.0, 82.0, 8.5), (-29.0, 65.0, 7.5)],
    "phalanx_frac": (0.47, 0.28, 0.25),   # proximal, middle, distal share of finger length (assumed)
    "thumb_o": (15.0, 38.0, -6.0), "thumb_d": (0.83, 0.5, -0.25), "thumb_l": 62.0, "thumb_r": 10.5,
    # ---- forearm cuff (item 1) ----
    "cuff_x": (-222.0, -48.0), "cuff_t": 2.0, "liner_t": 4.0, "strap_w": 38.0, "strap_x": (-200.0, -75.0),
    # ---- motor pack (items 2 to 10, 18, 20) ----
    "pack_x": (-215.0, -55.0),    # rear and front wall outer faces
    "pack_w": 76.0,               # outer width across the forearm
    "floor_z": 44.0,              # top of the pack floor (cavity bottom)
    "wall": 2.0, "floor_t": 2.5, "lid_t": 2.0,
    "motor_d": 25.0, "motor_l": 71.0,          # 25D x 71L gearmotor with encoder (Pololu 4869 class)
    "shaft_l": 12.5, "shaft_d": 4.0,
    "motor_y": 15.0,                            # motor axes at y = +/- motor_y (axes along X)
    "motor_x0": -150.0,                         # rear end of the motor bodies
    "spool_core_d": 10.0, "spool_flange_d": 20.0, "spool_w": 12.0, "tendon_d": 0.8,
    "idler_d": 10.0, "idler_w": 4.0,            # 623ZZ-class bearings used as idlers, axis Z
    "cell_d": 18.4, "cell_l": 65.0, "cell_x": (-201.0, -181.0),   # two 18650 cells, axes across (Y)
    "estop_x": -161.0, "estop_d": 18.0, "estop_depth": 18.0, "estop_cap_d": 24.0,
    # ---- anchor block (item 10) and sheaths (item 11) ----
    "anchor_l": 12.0, "anchor_h": 26.0,
    "sheath_od": 4.0, "sheath_slack": 1.2,      # cut length = neutral path x slack factor
    # ---- hand side (items 12 to 17) ----
    "glove_t": 2.5, "plate_t": 2.5,
    "guide_cuff_w": 12.0,                       # proximal (guide) cuff width
    "anchor_cuff_w_max": 20.0,                  # D4: 20 mm anchor cuffs where the phalanx allows
    "joint_clear": 3.0,                         # clearance from each joint crease to a cuff edge
    "cuff_t": 2.5, "cuff_liner_t": 2.0,
    "contact_arc_frac": 0.62,                   # share of finger circumference in contact under load
}


def derived(p=None):
    """Derived dimensions used by the model, the drawing and the calculation note."""
    p = dict(PARAMS if p is None else p)
    d = dict(p)
    x0, x1 = p["pack_x"]
    d["pack_l"] = x1 - x0
    d["top_z"] = p["floor_z"] + 1.5 + p["motor_d"] + 2.0          # top of base walls
    d["pack_top"] = d["top_z"] + p["lid_t"]
    d["motor_z"] = p["floor_z"] + 1.5 + p["motor_d"] / 2
    d["motor_x1"] = p["motor_x0"] + p["motor_l"]                    # gearbox face
    d["spool_x"] = d["motor_x1"] + 0.5 + p["spool_w"] / 2           # spool center on the shaft
    d["spool_r_eff"] = p["spool_core_d"] / 2 + p["tendon_d"] / 2    # first-layer effective radius
    d["inner_w"] = p["pack_w"] - 2 * p["wall"]
    fP, fM, fD = p["phalanx_frac"]
    mcp = p["palm_l"] - 4.0
    fingers = []
    for (y, L, r) in p["fingers"]:
        lp, lm, ld = fP * L, fM * L, fD * L
        usable = lm - 2 * p["joint_clear"]
        w = min(p["anchor_cuff_w_max"], usable)
        fingers.append(dict(y=y, L=L, r=r, lp=lp, lm=lm, ld=ld, mcp_x=mcp, pip_x=mcp + lp, dip_x=mcp + lp + lm,
                            guide_x=mcp + lp / 2, anchor_x=mcp + lp + lm / 2, anchor_w=w, usable=usable,
                            arc=p["contact_arc_frac"] * 2 * pi * r))
    d["finger_geom"] = fingers
    d["hand_length"] = p["palm_l"] - 4.0 + max(L for _, L, _ in p["fingers"])
    return d


def build_parts(params=None):
    """Return {'parts': {name: shape}, 'context': shape, 'sheath_paths': [...], 'd': derived}."""
    from build123d import Box, Cone, Cylinder, Sphere, Pos, Rot, Solid, Plane, Vector

    d = derived(params)
    p = d

    def along_x(s):
        return Rot(0, 90, 0) * s

    def along_y(s):
        return Rot(90, 0, 0) * s

    def arm_r(x):
        return p["r_wrist"] + (p["r_elbow"] - p["r_wrist"]) * (-x) / p["arm_l"]

    def cone_x(xa, xb, ra, rb):
        return Pos((xa + xb) / 2, 0, 0) * along_x(Cone(ra, rb, xb - xa))

    def tube(a, b, r):
        a = Vector(*a); b = Vector(*b); v = b - a
        return Solid.make_cylinder(r, v.length, Plane(origin=a, z_dir=v.normalized()))

    def path(pts, r):
        s = None
        for a, b in zip(pts[:-1], pts[1:]):
            seg = tube(a, b, r)
            s = seg if s is None else s + seg
        for q in pts[1:-1]:
            s = s + Pos(*q) * Sphere(r)
        return s

    def plen(pts):
        return sum(((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2 + (b[2] - a[2]) ** 2) ** 0.5
                   for a, b in zip(pts[:-1], pts[1:]))

    # ---------------- context: forearm and hand ----------------
    forearm = cone_x(-p["arm_l"], 0, p["r_elbow"], p["r_wrist"])
    PL, PW, PT = p["palm_l"], p["palm_w"], p["palm_t"]
    palm = Pos(PL / 2, 0, 0) * Box(PL, PW, PT)
    digits = None
    for y, L, r in p["fingers"]:
        dg = Pos(PL + L / 2 - 4, y, 0) * along_x(Cylinder(r, L)) + Pos(PL + L - 4, y, 0) * Sphere(r)
        digits = dg if digits is None else digits + dg
    to, td, tl, tr = p["thumb_o"], p["thumb_d"], p["thumb_l"], p["thumb_r"]
    thumb_end = tuple(to[i] + td[i] * tl for i in range(3))
    thumb = tube(to, thumb_end, tr) + Pos(*thumb_end) * Sphere(tr)
    context = forearm + palm + digits + thumb

    parts = {}

    # ---------------- 1 forearm cuff: half shell with foam liner and two straps ----------------
    cx0, cx1 = p["cuff_x"]
    lt, ct = p["liner_t"], p["cuff_t"]
    shell = (cone_x(cx0, cx1, arm_r(cx0) + lt + ct, arm_r(cx1) + lt + ct)
             - cone_x(cx0 - 1, cx1 + 1, arm_r(cx0 - 1) + lt, arm_r(cx1 + 1) + lt))
    liner = (cone_x(cx0, cx1, arm_r(cx0) + lt, arm_r(cx1) + lt)
             - cone_x(cx0 - 1, cx1 + 1, arm_r(cx0 - 1) + 0.2, arm_r(cx1 + 1) + 0.2))
    keep_top = Pos(0, 0, 60 - 8) * Box(1000, 200, 120)
    sub = {"cuff_shell": shell & keep_top, "cuff_liner": liner & keep_top}
    cuff = sub["cuff_shell"] + sub["cuff_liner"]
    sw = p["strap_w"]
    straps = None
    for xs in p["strap_x"]:
        st = (cone_x(xs - sw / 2, xs + sw / 2, arm_r(xs - sw / 2) + 1.8, arm_r(xs + sw / 2) + 1.8)
                       - cone_x(xs - sw / 2 - 1, xs + sw / 2 + 1, arm_r(xs - sw / 2 - 1) + 0.2,
                                arm_r(xs + sw / 2 + 1) + 0.2))
        straps = st if straps is None else straps + st
    sub["cuff_straps"] = straps
    parts["forearm_cuff"] = cuff + straps
    cuff_outer = cone_x(cx0 - 20, cx1 + 20, arm_r(cx0 - 20) + lt + ct, arm_r(cx1 + 20) + lt + ct)

    # ---------------- 2 pack base: open box, floor, saddle ribs, tendon exit slots ----------------
    x0, x1 = p["pack_x"]; L = d["pack_l"]; W = p["pack_w"]; wl = p["wall"]
    fz, tz = p["floor_z"], d["top_z"]
    xc = (x0 + x1) / 2
    box_bot = fz - p["floor_t"]
    base = Pos(xc, 0, (box_bot + tz) / 2) * Box(L, W, tz - box_bot)
    base = base - Pos(xc, 0, (fz + tz + 2) / 2) * Box(L - 2 * wl, W - 2 * wl, tz + 2 - fz)
    for xr in (x0 + 8, xc, x1 - 8):                   # saddle ribs down to the cuff
        base = base + Pos(xr, 0, (box_bot + 20) / 2) * Box(4, W - 6, box_bot - 20)
    base = base - cuff_outer
    mz = d["motor_z"]; re_ = d["spool_r_eff"]
    for sgn in (1, -1):                                # tendon exit slots in the front wall
        base = base - Pos(x1 - wl / 2, sgn * 31.0, mz) * Box(wl + 2, 6, 2 * re_ + 4)
    parts["pack_base"] = base

    # ---------------- 3 gearmotors (axes along X), 4 spools, 20 idlers ----------------
    motors = spools = idlers = None
    mx0, mx1 = p["motor_x0"], d["motor_x1"]
    for sgn in (1, -1):
        y = sgn * p["motor_y"]
        m = (Pos((mx0 + mx1) / 2, y, mz) * along_x(Cylinder(p["motor_d"] / 2, p["motor_l"]))
             + Pos(mx1 + p["shaft_l"] / 2, y, mz) * along_x(Cylinder(p["shaft_d"] / 2, p["shaft_l"])))
        motors = m if motors is None else motors + m
        sx, swd = d["spool_x"], p["spool_w"]
        fr, cr = p["spool_flange_d"] / 2, p["spool_core_d"] / 2
        s = (Pos(sx, y, mz) * along_x(Cylinder(cr, swd))
             + Pos(sx - swd / 2 + 0.75, y, mz) * along_x(Cylinder(fr, 1.5))
             + Pos(sx, y, mz) * along_x(Cylinder(fr, 1.5))
             + Pos(sx + swd / 2 - 0.75, y, mz) * along_x(Cylinder(fr, 1.5)))
        spools = s if spools is None else spools + s
        # two grooves (flexor, extensor); each tendon pair leaves the spool top or bottom toward
        # the outer wall and turns forward on an idler (axis Z)
        for gx, gz in ((sx - swd / 4, mz + re_), (sx + swd / 4, mz - re_)):
            ic = (gx + p["idler_d"] / 2, sgn * (31.0 - p["idler_d"] / 2), gz)
            idl = Pos(*ic) * Cylinder(p["idler_d"] / 2, p["idler_w"])
            idlers = idl if idlers is None else idlers + idl
    parts["gearmotors"] = motors
    parts["spools"] = spools
    parts["idlers"] = idlers

    # ---------------- 5 cells, 6 controller, 7 drivers, 18 charger (rear bay) ----------------
    cz = fz + 1.0 + p["cell_d"] / 2
    cells = None
    for cxp in p["cell_x"]:
        c = Pos(cxp, 0, cz) * along_y(Cylinder(p["cell_d"] / 2, p["cell_l"]))
        cells = c if cells is None else cells + c
    tray_z = fz + 1.0 + p["cell_d"] + 1.0
    rx = x0 + wl + 1.0
    bms = Pos(rx + 14 + 3 + 7, -14, tray_z + 2) * Box(14, 40, 4)
    parts["cells"] = cells + bms
    parts["controller"] = Pos(rx + 9, -24, tray_z + 2.5) * Box(18, 21, 5)
    parts["drivers"] = (Pos(rx + 7.5, 0, tray_z + 2) * Box(15, 20, 4)
                        + Pos(rx + 7.5 + 17, 20, tray_z + 2) * Box(15, 20, 4))
    parts["charger"] = Pos(rx + 7.5, 24, tray_z + 2) * Box(15, 20, 4) + Pos(x0 + 1, 24, tray_z + 2) * Box(3, 9, 3.5)

    # ---------------- 8 lid, 9 emergency stop ----------------
    lid = Pos(xc, 0, tz + p["lid_t"] / 2) * Box(L, W, p["lid_t"])
    lid = lid - Pos(p["estop_x"], 0, tz + p["lid_t"] / 2) * Cylinder(p["estop_d"] / 2 + 0.5, p["lid_t"] + 2)
    parts["pack_lid"] = lid
    ex, top = p["estop_x"], d["pack_top"]
    parts["estop"] = (Pos(ex, 0, top - p["estop_depth"] / 2) * Cylinder(p["estop_d"] / 2, p["estop_depth"])
                      + Pos(ex, 0, top + 4) * Cylinder(8, 8)
                      + Pos(ex, 0, top + 9.5) * Cylinder(p["estop_cap_d"] / 2, 5))

    # ---------------- 10 sheath anchor block (front of pack) ----------------
    ax0 = x1; ax1 = x1 + p["anchor_l"]
    az0 = fz; az1 = fz + p["anchor_h"]
    anchor = Pos((ax0 + ax1) / 2, 0, (az0 + az1) / 2) * Box(p["anchor_l"], W - 4, p["anchor_h"])
    lever = Pos(ax1 - 3, 0, az1 + 3) * Box(6, 50, 6)
    parts["anchor_block"] = anchor + lever

    # ---------------- hand-side geometry ----------------
    GT = p["glove_t"]
    gz = PT / 2 + GT
    glove = (Pos(PL / 2 - 3, 0, 0) * Box(PL + 4, PW + 2 * GT, PT + 2 * GT)
             - Pos(PL / 2 - 3, 0, 0) * Box(PL + 6, PW, PT))
    parts["glove"] = glove
    pt = p["plate_t"]
    parts["dorsal_plate"] = Pos(38, 0, gz + pt / 2) * Box(50, 60, pt)
    parts["palmar_plate"] = Pos(24, 0, -gz - pt / 2) * Box(34, 60, pt)

    # sheaths: extensors over the back of the wrist, flexors around the radial (index, middle)
    # and ulnar (ring, little) sides to the palmar plate
    ext_end_y = [21.0, 7.0, -7.0, -21.0]
    sheaths, sheath_paths = None, []
    so = p["sheath_od"] / 2
    for k in range(4):
        side = 1 if k < 2 else -1
        ya = side * (31.0 - 3.0 * (k % 2))
        e_pts = [(ax1, ya, mz + re_ + 2), (-8, ya * 0.7, 40), (15, ext_end_y[k], gz + pt + so)]
        j = k % 2
        f_pts = [(ax1, side * (31.0 + 3.0 * j), mz - re_ - 2), (-22, side * (40.0 + 2 * j), 18),
                 (-2, side * (36.0 + 2 * j), -16), (12, side * (24.0 + 4 * j), -gz - pt - so)]
        sheath_paths += [("ext", k, plen(e_pts)), ("flex", k, plen(f_pts))]
        s = path(e_pts, so) + path(f_pts, so)
        sheaths = s if sheaths is None else sheaths + s
    parts["sheaths"] = sheaths

    # finger cuffs (guide on the proximal phalanx, anchor on the middle phalanx) and tendons
    cuffs = tendons = None
    cuff_tpu_v = cuff_liner_v = 0.0
    tr_ = 1.0   # tendon drawn oversize so it reads at this scale
    ct2 = p["cuff_t"] + p["cuff_liner_t"]
    for i, fg in enumerate(d["finger_geom"]):
        y, r = fg["y"], fg["r"]
        for xcuf, w in ((fg["guide_x"], p["guide_cuff_w"]), (fg["anchor_x"], fg["anchor_w"])):
            c = Pos(xcuf, y, 0) * along_x(Cylinder(r + ct2, w) - Cylinder(r, w + 1))
            cuff_tpu_v += pi * ((r + ct2) ** 2 - (r + p["cuff_liner_t"]) ** 2) * w
            cuff_liner_v += pi * ((r + p["cuff_liner_t"]) ** 2 - r ** 2) * w
            cuffs = c if cuffs is None else cuffs + c
        h = r + ct2 + tr_
        t = (path([(40, ext_end_y[i] * 1.1, gz + pt + 1), (fg["guide_x"], y, h), (fg["anchor_x"], y, h)], tr_)
             + path([(30, y * 0.9, -gz - pt - 1), (fg["guide_x"], y, -h), (fg["anchor_x"], y, -h)], tr_))
        tendons = t if tendons is None else tendons + t
    parts["finger_cuffs"] = cuffs
    parts["tendons"] = tendons

    # 17 thumb abduction spacer
    s_ring = 34.0
    rc = tuple(to[i] + td[i] * s_ring for i in range(3))
    ring = Solid.make_cylinder(tr + 2.5, 12, Plane(origin=Vector(*rc) - Vector(*td) * 6, z_dir=Vector(*td)))
    ring = ring - Solid.make_cylinder(tr, 14, Plane(origin=Vector(*rc) - Vector(*td) * 7, z_dir=Vector(*td)))
    parts["thumb_spacer"] = ring + Pos(40, 45.5, -8) * Box(14, 8, 12)

    sub["finger_cuff_tpu_mm3"] = cuff_tpu_v
    sub["finger_cuff_liner_mm3"] = cuff_liner_v
    return {"parts": parts, "context": context, "sheath_paths": sheath_paths, "d": d, "sub": sub}


# BOM line for each modeled part (matches bom/bom.csv and the exploded view)
BOM_LINE = {"forearm_cuff": 1, "pack_base": 2, "gearmotors": 3, "spools": 4, "cells": 5, "controller": 6,
            "drivers": 7, "pack_lid": 8, "estop": 9, "anchor_block": 10, "sheaths": 11, "glove": 12,
            "dorsal_plate": 13, "palmar_plate": 14, "finger_cuffs": 15, "tendons": 16, "thumb_spacer": 17,
            "charger": 18, "idlers": 20}


def build(params=None):
    """Device assembly (no context) as one compound."""
    from build123d import Compound
    return Compound(children=list(build_parts(params)["parts"].values()))


def export(out=None):
    from build123d import Compound, export_step, export_stl
    out = Path(out) if out else Path(__file__).resolve().parents[1]
    (out / "step").mkdir(parents=True, exist_ok=True); (out / "stl").mkdir(parents=True, exist_ok=True)
    m = build_parts()
    parts = m["parts"]
    import copy
    asm = Compound(children=[copy.copy(v) for v in parts.values()])
    export_step(asm, str(out / "step" / "flexhand-assembly.step"))
    export_stl(asm, str(out / "stl" / "flexhand-assembly.stl"))
    export_step(Compound(children=[copy.copy(v) for v in parts.values()] + [copy.copy(m["context"])]),
                str(out / "step" / "flexhand-on-forearm.step"))
    for name in ("pack_base", "pack_lid", "spools", "anchor_block", "forearm_cuff", "dorsal_plate",
                 "palmar_plate", "finger_cuffs", "thumb_spacer"):
        export_step(parts[name], str(out / "step" / f"flexhand-{name.replace('_', '-')}.step"))
        export_stl(parts[name], str(out / "stl" / f"flexhand-{name.replace('_', '-')}.stl"))
    return m


if __name__ == "__main__":
    m = export()
    d = m["d"]
    print(f"Pack envelope {d['pack_l']:.0f} x {d['pack_w']:.0f} mm, top {d['pack_top']:.1f} mm above forearm axis")
    for name, s in m["parts"].items():
        print(f"{name:14s} volume {s.volume / 1000:8.2f} cm3")
    for kind, k, Lp in m["sheath_paths"]:
        print(f"sheath {kind} {k}: {Lp:.0f} mm neutral path")
    print("Wrote cad/step/*.step and cad/stl/*.stl")
