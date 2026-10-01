"""FlexHand parametric model (build123d), constructable design (FXH-DDR-003).

Run from the repo root:
    python cad/src/model.py            export STEP and STL into cad/step and cad/stl
    python cad/src/model.py --check    run the constructability checks (overlaps, contacts, fixings)

Axes (right forearm and hand, palm down): X runs from the elbow toward the fingertips with
the wrist at X = 0, Y is across the forearm with +Y on the thumb (radial) side, Z is dorsal (up).
A left-hand device is the mirror image about the XZ plane.

Every part is modelled as it is made: printed parts with their holes, bosses and pockets, bought
parts at their catalogue sizes, and the fixings that join them. The forearm and hand are context.
components() returns the parts one by one (for the build plan pictures and the checks);
build_parts() groups them by bill of materials line (for the media, drawings and calculations).
PRELIMINARY, NOT FOR FABRICATION.
"""
from math import cos, pi, radians, sin, sqrt
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # ---- context anthropometry (adult, medium glove size, hand length about 183 mm) ----
    "arm_l": 270.0, "r_elbow": 38.0, "r_wrist": 29.0,
    "palm_l": 95.0, "palm_w": 80.0, "palm_t": 28.0,
    # finger (lateral y, length from MCP, radius); index, middle, ring, little.
    # DDR-003 C9: fingers held slightly spread by the glove so the cuffs of neighbouring fingers clear
    "fingers": [(36.0, 80.0, 9.0), (12.0, 88.0, 9.0), (-12.0, 82.0, 8.5), (-34.5, 65.0, 7.5)],
    "phalanx_frac": (0.47, 0.28, 0.25),   # proximal, middle, distal share of finger length (assumed)
    "thumb_o": (15.0, 38.0, -6.0), "thumb_d": (0.83, 0.5, -0.25), "thumb_l": 62.0, "thumb_r": 10.5,
    # ---- forearm cuff (item 1) ----
    "cuff_x": (-242.0, -68.0), "cuff_t": 2.0, "liner_t": 4.0, "strap_w": 38.0, "strap_x": (-189.5, -121.5),
    "strap_t": 1.8, "cuff_edge_z": -8.0,
    # perforated cuff shell and liner (N4): radial holes on a grid (x start, x end, x step; angles from dorsal)
    "cuff_hole_d": 12.0, "cuff_hole_x": (-232.0, -78.0, 17.0), "cuff_hole_ang": (-75.0, -50.0, -25.0, 0.0, 25.0, 50.0, 75.0),
    # pack saddle ribs sit on the solid webs between hole columns; two M3 screws per rib (C1)
    "rib_x": (-223.5, -155.5, -87.5), "rib_t": 4.0, "rib_boss_y": 9.0, "rib_boss_d": 8.0,
    # ---- motor pack (items 2 to 10, 18, 20, 23, 25) ----
    "pack_x": (-239.0, -71.0),    # rear and front wall outer faces (C2)
    "pack_w": 76.0,               # outer width across the forearm
    "floor_z": 48.0,              # top of the pack floor (cavity bottom); raised 4 mm (C1)
    "wall": 2.0, "floor_t": 2.5, "lid_t": 2.0,
    "motor_d": 25.0, "motor_l": 71.0,          # 25D x 71L gearmotor with encoder (Pololu 4869 class)
    "shaft_l": 12.5, "shaft_d": 4.0, "face_hole_pitch": 17.0,   # two M3 holes in the gearbox face
    "motor_y": 13.5,                            # motor axes at y = +/- motor_y (C3)
    "motor_x0": -172.8,                         # rear end of the motor bodies
    "cable_gap": 6.0,                           # room behind the motors for the encoder cable
    "bulkhead_t": 3.0,                          # motor bulkhead printed in the pack base (C3)
    "spool_core_d": 10.0, "spool_flange_d": 14.0, "spool_w": 12.0, "spool_hub_l": 4.0, "tendon_d": 0.8,
    "flange_t": 1.5,
    "idler_d": 10.0, "idler_w": 4.0, "idler_bore": 3.0,   # 623ZZ-class bearings used as idlers, axis Z
    "line_y": 31.25,                            # where each spool line leaves its idler and the pack (C4)
    "cell_d": 18.4, "cell_l": 65.0, "cell_x": (-226.8, -207.8),   # two 18650 cells, axes across (Y) (C5)
    "estop_x": -187.8, "estop_d": 18.0, "estop_depth": 18.0, "estop_cap_d": 24.0,
    "lid_boss_x": (-188.0, -120.0), "lid_boss_y": 32.5,
    # ---- anchor block (item 10) and sheaths (item 11) (C6, C7) ----
    "anchor_l": 53.0, "anchor_h": 26.0, "anchor_w": 88.0,
    "gate_t": 3.0, "cover_l": 7.6, "puck": (5.0, 14.0, 6.0),
    "chan_w": 15.0, "chan_h": 7.0,
    "balance_d": 8.0, "balance_w": 4.0,         # 693ZZ-class bearings used as floating balance pulleys, axis Z
    "balance_y": 31.25,
    "coupling_d": 6.8, "coupling_l": 10.0, "spring_l": 4.0,
    "sheath_od": 4.0, "sheath_slack": 1.2,      # cut length = neutral path x slack factor
    # ---- hand side (items 12 to 17, 21) ----
    "glove_t": 2.5, "plate_t": 2.5,
    "guide_cuff_w": 12.0,                       # proximal (guide) cuff width
    "anchor_cuff_w_max": 20.0,                  # D4: 20 mm anchor cuffs where the phalanx allows
    "thimble_w_max": 20.0,                      # N2 (DDR-002): open-tip fingertip thimble on the distal phalanx
    "thimble_t": 2.0,                           # thimble TPU wall (liner as for the cuffs)
    "joint_clear": 3.0,                         # clearance from each joint crease to a cuff edge
    "cuff_t": 2.5, "cuff_liner_t": 2.0,
    "contact_arc_frac": 0.62,                   # share of finger circumference in contact under load
    "side_band_t": 1.0,                         # thin TPU side band between the padded saddles (C9)
    "stop_y": (24.0, 8.0, -8.0, -23.0),         # sheath stops on the hand plates, index to little
}


def derived(p=None):
    """Derived dimensions used by the model, the drawings, the pictures and the calculation note."""
    p = dict(PARAMS if p is None else p)
    d = dict(p)
    x0, x1 = p["pack_x"]
    d["pack_l"] = x1 - x0
    d["box_bot"] = p["floor_z"] - p["floor_t"]
    d["top_z"] = p["floor_z"] + 1.5 + p["motor_d"] + 2.0          # top of base walls
    d["pack_top"] = d["top_z"] + p["lid_t"]
    d["motor_z"] = p["floor_z"] + 1.5 + p["motor_d"] / 2
    d["motor_x1"] = p["motor_x0"] + p["motor_l"]                    # gearbox face
    d["bulk_x"] = (d["motor_x1"], d["motor_x1"] + p["bulkhead_t"])
    sb = d["bulk_x"][1] + 0.5                                       # spool back face
    d["spool_x0"] = sb
    d["spool_x1"] = sb + p["spool_hub_l"] + p["spool_w"]
    ft = p["flange_t"]
    gw = (p["spool_w"] - 3 * ft) / 2
    g1 = sb + p["spool_hub_l"] + ft + gw / 2
    g2 = g1 + gw + ft
    d["groove_w"] = gw
    d["groove_x"] = (g1, g2)                                        # upper (extensor) and lower (flexor) grooves
    d["spool_x"] = sb + p["spool_hub_l"] + p["spool_w"] / 2         # spool body centre
    d["spool_r_eff"] = p["spool_core_d"] / 2 + p["tendon_d"] / 2    # first-layer effective radius
    d["inner_w"] = p["pack_w"] - 2 * p["wall"]
    d["idler_y"] = p["line_y"] - p["idler_d"] / 2
    d["idler_x"] = (g1 + p["idler_d"] / 2, g2 + p["idler_d"] / 2)
    mz = d["motor_z"]; re_ = d["spool_r_eff"]
    d["line_z"] = (mz + re_, mz - re_)                              # extensor line high, flexor line low
    d["tray_z"] = p["floor_z"] + 1.0 + p["cell_d"] + 1.0
    d["anchor_x"] = (x1, x1 + p["anchor_l"])
    d["gate_x"] = (d["anchor_x"][1], d["anchor_x"][1] + p["gate_t"])
    d["cover_x"] = (d["gate_x"][1] + 0.4, d["gate_x"][1] + 0.4 + p["cover_l"])
    d["anchor_front"] = d["cover_x"][1]
    d["anchor_total_l"] = d["anchor_front"] - x1
    # balance pulley travel in its channel: channel length less spring, pulley, coupling and 1 mm
    d["balance_travel"] = p["anchor_l"] - p["spring_l"] - p["balance_d"] - p["coupling_l"] - 1.0
    fP, fM, fD = p["phalanx_frac"]
    mcp = p["palm_l"] - 4.0
    fingers = []
    for (y, L, r) in p["fingers"]:
        lp, lm, ld = fP * L, fM * L, fD * L
        usable = lm - 2 * p["joint_clear"]
        w = min(p["anchor_cuff_w_max"], usable)
        tw = min(p["thimble_w_max"], ld - p["joint_clear"])        # band from the DIP crease clearance to the tip
        fingers.append(dict(y=y, L=L, r=r, lp=lp, lm=lm, ld=ld, mcp_x=mcp, pip_x=mcp + lp, dip_x=mcp + lp + lm,
                            guide_x=mcp + lp / 2, anchor_x=mcp + lp + lm / 2, anchor_w=w, usable=usable,
                            thimble_w=tw, thimble_x=mcp + L - tw / 2,
                            arc=p["contact_arc_frac"] * 2 * pi * r))
    d["finger_geom"] = fingers
    d["hand_length"] = p["palm_l"] - 4.0 + max(L for _, L, _ in p["fingers"])
    d["saddle_half_deg"] = p["contact_arc_frac"] * 180.0 / 2          # each padded saddle spans this either side
    return d


def arm_r(x, p=PARAMS):
    return p["r_wrist"] + (p["r_elbow"] - p["r_wrist"]) * (-x) / p["arm_l"]


# ------------------------------------------------------------------ shape helpers
def _B():
    import build123d as b
    return b


def _box(x0, x1, y0, y1, z0, z1):
    b = _B()
    return b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0)


def _cyl_x(x0, x1, y, z, r):
    b = _B()
    return b.Pos((x0 + x1) / 2, y, z) * b.Rot(0, 90, 0) * b.Cylinder(r, x1 - x0)


def _cyl_y(y0, y1, x, z, r):
    b = _B()
    return b.Pos(x, (y0 + y1) / 2, z) * b.Rot(90, 0, 0) * b.Cylinder(r, y1 - y0)


def _cyl_z(z0, z1, x, y, r):
    b = _B()
    return b.Pos(x, y, (z0 + z1) / 2) * b.Cylinder(r, z1 - z0)


def _cone_x(xa, xb, ra, rb):
    b = _B()
    return b.Pos((xa + xb) / 2, 0, 0) * b.Rot(0, 90, 0) * b.Cone(ra, rb, xb - xa)


def _tube(a, c, r):
    b = _B()
    a = b.Vector(*a); c = b.Vector(*c); v = c - a
    return b.Solid.make_cylinder(r, v.length, b.Plane(origin=a, z_dir=v.normalized()))


def _path(pts, r):
    b = _B()
    s = None
    for a, c in zip(pts[:-1], pts[1:]):
        seg = _tube(a, c, r)
        s = seg if s is None else s + seg
    for q in pts[1:-1]:
        s = s + b.Pos(*q) * b.Sphere(r)
    return s


def _plen(pts):
    return sum(sqrt(sum((c[i] - a[i]) ** 2 for i in range(3))) for a, c in zip(pts[:-1], pts[1:]))


def _fuse(shapes):
    out = None
    for s in shapes:
        if s is None:
            continue
        out = s if out is None else out + s
    return out


def _sector(x0, x1, y, r_in, r_out, a0, a1):
    """Ring sector about an axis along X at (y, 0): radii r_in..r_out, angles a0..a1 in degrees measured
    from +Z (dorsal) toward +Y."""
    b = _B()
    R = r_out + 5
    pts = [(0.0, 0.0)]
    n = max(2, int(abs(a1 - a0) / 10) + 1)
    for i in range(n + 1):
        a = radians(a0 + (a1 - a0) * i / n)
        pts.append((R * sin(a) / cos(radians((a1 - a0) / (2 * n))), R * cos(a) / cos(radians((a1 - a0) / (2 * n)))))
    with b.BuildPart() as bp:
        with b.BuildSketch(b.Plane.YZ.offset(x0)):
            b.Polygon(*pts, align=None)
        b.extrude(amount=x1 - x0)
    wedge = b.Pos(0, y, 0) * bp.part
    ring = _cyl_x(x0, x1, y, 0, r_out) - _cyl_x(x0 - 1, x1 + 1, y, 0, r_in)
    return ring & wedge


def sheath_routes(d):
    """Neutral paths of the eight Bowden sheaths, from the puck seats to the hand stop blocks:
    [(kind, finger index, points)], kind 'ext' (over the back of the wrist) or 'flex' (down the side
    of the wrist and under the palm)."""
    p = d
    by = p["balance_y"]
    gx1 = d["gate_x"][1]
    seat = gx1 + p["puck"][0] - 3.0
    fx = d["anchor_front"]
    gz = p["palm_t"] / 2 + p["glove_t"]
    zsd = gz + p["plate_t"] + 3.25
    zsp = -zsd
    zu_, zl_ = d["line_z"]
    out = []
    order = [(1, 4.0), (1, -4.0), (-1, 4.0), (-1, -4.0)]      # index, middle, ring, little: (side, offset)
    for k, (sg, oy) in enumerate(order):
        ya = sg * by + oy
        outer = abs(ya) > by
        ys = p["stop_y"][k]
        e_pts = [(seat, ya, zu_), (fx + 3, ya, zu_), (1.0, ya * 0.95, zu_ - 12), (6.0, ys * 1.05, zsd + 8),
                 (10.0, ys, zsd + 0.8), (17.0, ys, zsd)]
        if outer:     # index and little: down the side first, then under the palm at the stop height
            f_pts = [(seat, ya, zl_), (fx + 3, ya, zl_), (-3.0, sg * 50.0, 22.0), (-4.5, sg * 50.0, -12.0), (-4.0, sg * 46.0, -20.0),
                     (-1.5, sg * (abs(ys) + 10.0), zsp), (3.0, ys, zsp), (11.0, ys, zsp)]
        else:         # middle and ring: down the side nearer the hand, then under the outer sheath, deeper
            f_pts = [(seat, ya, zl_), (fx + 3, ya, zl_), (2.0, sg * 45.5, 22.0), (2.0, sg * 45.5, -12.0), (3.5, sg * 44.5, -20.0),
                     (4.0, sg * 30.0, zsp - 5.25), (4.0, sg * (abs(ys) + 6.0), zsp - 4.25), (4.5, ys, zsp), (11.0, ys, zsp)]
        out += [("ext", k, e_pts), ("flex", k, f_pts)]
    return out


# ------------------------------------------------------------------ the parts, one by one
def components(params=None):
    """Return {'c': {key: shape}, 'context': shape, 'sheath_paths': [...], 'd': derived, 'sub': {...}}."""
    b = _B()
    from build123d import Box, Cylinder, Pos, Rot, Solid, Plane, Vector, Sphere
    d = derived(params)
    p = d
    C = {}
    sub = {}
    ar = lambda x: arm_r(x, p)  # noqa: E731

    # ---------------- context: forearm and hand ----------------
    forearm = _cone_x(-p["arm_l"], 0, p["r_elbow"], p["r_wrist"])
    PL, PW, PT = p["palm_l"], p["palm_w"], p["palm_t"]
    palm = Pos(PL / 2, 0, 0) * Box(PL, PW, PT)
    digits = None
    for y, L, r in p["fingers"]:
        dg = _cyl_x(PL - 4, PL - 4 + L, y, 0, r) + Pos(PL + L - 4, y, 0) * Sphere(r)
        digits = dg if digits is None else digits + dg
    to, td, tl, tr = p["thumb_o"], p["thumb_d"], p["thumb_l"], p["thumb_r"]
    thumb_end = tuple(to[i] + td[i] * tl for i in range(3))
    thumb = _tube(to, thumb_end, tr) + Pos(*thumb_end) * Sphere(tr)
    context = forearm + palm + digits + thumb

    # ---------------- 1 forearm cuff: perforated half shell, foam liner, two straps ----------------
    cx0, cx1 = p["cuff_x"]
    lt, ct = p["liner_t"], p["cuff_t"]
    ez = p["cuff_edge_z"]
    keep_top = _box(-1000, 1000, -100, 100, ez, 200)
    shell = (_cone_x(cx0, cx1, ar(cx0) + lt + ct, ar(cx1) + lt + ct)
             - _cone_x(cx0 - 1, cx1 + 1, ar(cx0 - 1) + lt, ar(cx1 + 1) + lt)) & keep_top
    liner = (_cone_x(cx0, cx1, ar(cx0) + lt, ar(cx1) + lt)
             - _cone_x(cx0 - 1, cx1 + 1, ar(cx0 - 1), ar(cx1 + 1))) & keep_top
    hx0, hx1, hstep = p["cuff_hole_x"]
    holes = []
    xh = hx0
    while xh <= hx1 + 1e-6:
        for a in p["cuff_hole_ang"]:
            holes.append(Pos(xh, 0, 0) * Rot(a, 0, 0) * Pos(0, 0, 50) * Cylinder(p["cuff_hole_d"] / 2, 60))
        xh += hstep
    holes = b.Compound(children=holes)
    sub["cuff_shell_solid"] = shell
    # screw holes for the pack: 3.4 mm through the shell, 6 mm countersink pocket on the inside face
    by_ = p["rib_boss_y"]
    cs_holes = []
    cuff_screws = []
    liner_holes = []
    inserts = []
    for xr in p["rib_x"]:
        r_in = ar(xr) + lt
        for sy in (by_, -by_):
            z_in = sqrt(r_in ** 2 - sy ** 2)
            zs = sqrt((r_in + ct) ** 2 - sy ** 2)
            cs_holes.append(_cyl_z(z_in - 3, z_in + 10, xr, sy, 1.7))
            liner_holes.append(_cyl_z(z_in - 9, z_in + 1, xr, sy, 3.2))
            head = _cyl_z(z_in - 1.7, z_in + 1.5, xr, sy, 2.85) & _cone_x(xr - 5, xr + 5, ar(xr - 5) + lt, ar(xr + 5) + lt)
            cuff_screws.append(head + _cyl_z(z_in - 0.5, zs + 5.0, xr, sy, 1.5))
            inserts.append(_cyl_z(zs + 0.7, zs + 5.0, xr, sy, 2.0) - _cyl_z(zs - 1, zs + 6, xr, sy, 1.5))
    C["cuff_shell"] = shell - holes - b.Compound(children=cs_holes)
    C["cuff_liner"] = liner - holes - b.Compound(children=liner_holes)
    C["cuff_screws"] = _fuse(cuff_screws)
    sw, st = p["strap_w"], p["strap_t"]
    straps = []
    for xs in p["strap_x"]:
        xa, xb = xs - sw / 2, xs + sw / 2
        top = (_cone_x(xa, xb, ar(xa) + lt + ct + st, ar(xb) + lt + ct + st)
               - _cone_x(xa - 1, xb + 1, ar(xa - 1) + lt + ct, ar(xb + 1) + lt + ct)) & keep_top
        under = (_cone_x(xa, xb, ar(xa) + st, ar(xb) + st) - _cone_x(xa - 1, xb + 1, ar(xa - 1), ar(xb + 1))) \
            & _box(-1000, 1000, -100, 100, -200, ez)
        step = (_cone_x(xa, xb, ar(xa) + lt + ct + st, ar(xb) + lt + ct + st)
                - _cone_x(xa - 1, xb + 1, ar(xa - 1), ar(xb + 1))) & _box(-1000, 1000, -100, 100, ez - st, ez)
        straps.append(top + under + step)
    C["straps"] = _fuse(straps)
    cuff_outer = _cone_x(cx0 - 20, cx1 + 20, ar(cx0 - 20) + lt + ct, ar(cx1 + 20) + lt + ct)

    # ---------------- 2 pack base ----------------
    x0, x1 = p["pack_x"]; W = p["pack_w"]; wl = p["wall"]; iw = W / 2 - wl
    fz, tz, bb = p["floor_z"], d["top_z"], d["box_bot"]
    mz = d["motor_z"]
    base = _box(x0, x1, -W / 2, W / 2, bb, tz) - _box(x0 + wl, x1 - wl, -iw, iw, fz, tz + 1)
    # saddle ribs with screw bosses, down to the cuff
    for xr in p["rib_x"]:
        base = base + _box(xr - p["rib_t"] / 2, xr + p["rib_t"] / 2, -(W / 2 - 3), W / 2 - 3, 18, bb)
        for sy in (by_, -by_):
            base = base + _cyl_z(18, bb, xr, sy, p["rib_boss_d"] / 2)
    base = base - cuff_outer
    ins = []
    for xr in p["rib_x"]:
        r_out = ar(xr) + lt + ct
        for sy in (by_, -by_):
            zs = sqrt(r_out ** 2 - sy ** 2)
            ins.append(_cyl_z(zs - 1, zs + 5.5, xr, sy, 2.0))          # heat-set insert hole from below
    # motor cradle (a cross rib with two seats and cable-tie slots)
    xc = p["motor_x0"] + 12.0
    cradle = _box(xc - 2, xc + 2, -iw, iw, fz, mz)
    for sg in (1, -1):
        cradle = cradle - _cyl_x(xc - 3, xc + 3, sg * p["motor_y"], mz, p["motor_d"] / 2)
        for dy in (-9.0, 9.0):
            cradle = cradle - _box(xc - 3, xc + 3, sg * p["motor_y"] + dy - 0.75, sg * p["motor_y"] + dy + 0.75, fz - 0.1, fz + 2.0)
    base = base + cradle
    # bulkhead with shaft clearance holes and countersunk M3 holes for the gearbox face
    bx0, bx1 = d["bulk_x"]
    bulk = _box(bx0, bx1, -iw, iw, fz, tz)
    for sg in (1, -1):
        y = sg * p["motor_y"]
        bulk = bulk - _cyl_x(bx0 - 1, bx1 + 1, y, mz, 4.0)
        for dy in (-p["face_hole_pitch"] / 2, p["face_hole_pitch"] / 2):
            bulk = bulk - _cyl_x(bx0 - 1, bx1 + 1, y + dy, mz, 1.7) - _cyl_x(bx1 - 1.7, bx1 + 1, y + dy, mz, 3.0)
    base = base + bulk
    # cell saddles
    cz = fz + 1.0 + p["cell_d"] / 2
    for cxp in p["cell_x"]:
        for sy in (20.0, -20.0):
            s = _box(cxp - 7, cxp + 7, sy - 4, sy + 4, fz, cz) - _cyl_y(sy - 5, sy + 5, cxp, cz, p["cell_d"] / 2)
            base = base + s
    # tray ledges along the side walls in the rear bay
    tzr = d["tray_z"]
    tray_x = (x0 + wl, p["estop_x"] - p["estop_d"] / 2 - 2.7)
    for sg in (1, -1):        # four tray posts against the side walls, clear of the cells
        for tx in (tray_x[0] + 4, tray_x[1] - 4):
            base = base + (_cyl_z(fz, tzr, tx, sg * 34.8, 2.0) & _box(tx - 3, tx + 3, -iw, iw, fz, tzr))
    # idler supports: a post from the floor for the lower idler, a shelf from the side wall for the upper one
    ix_u, ix_l = d["idler_x"]
    iy = d["idler_y"]
    zu, zl = d["line_z"]
    iwd = p["idler_w"]
    for sg in (1, -1):
        y = sg * iy
        base = base + _cyl_z(fz, zl - iwd / 2 - 0.3, ix_l, y, 3.5)
        y0s, y1s = sorted((sg * (iy - 4.5), sg * iw))
        base = base + _box(ix_u - 4.5, ix_u + 4.5, y0s, y1s, zu + iwd / 2 + 0.3, zu + iwd / 2 + 3.3)
    # lid bosses on the side walls
    for lx in p["lid_boss_x"]:
        for sg in (1, -1):
            y = sg * p["lid_boss_y"]
            base = base + (_cyl_z(fz, tz, lx, y, 3.5) & _box(lx - 4, lx + 4, -iw, iw, fz, tz))
            ins.append(_cyl_z(tz - 6, tz + 1, lx, y, 2.0))
            inserts.append(_cyl_z(tz - 5, tz, lx, y, 2.0) - _cyl_z(tz - 6, tz + 1, lx, y, 1.5))
    # holes: pins, exits, anchor screws, USB-C, tray screws
    pin_holes = []
    for sg in (1, -1):
        y = sg * iy
        pin_holes.append(_cyl_z(fz + 2, zl, ix_l, y, p["idler_bore"] / 2))
        pin_holes.append(_cyl_z(zu, zu + iwd / 2 + 3.4, ix_u, y, p["idler_bore"] / 2))
        for lz in d["line_z"]:
            pin_holes.append(_cyl_x(x1 - wl - 1, x1 + 1, sg * p["line_y"], lz, 1.5))
        for az in (mz + 6.0, mz - 6.0):
            pin_holes.append(_cyl_x(x1 - wl - 1, x1 + 1, sg * 14.0, az, 1.7))
        for tx in (tray_x[0] + 4, tray_x[1] - 4):
            pin_holes.append(_cyl_z(tzr - 8, tzr + 1, tx, sg * 34.5, 0.8))
    pin_holes.append(_box(x0 - 1, x0 + wl + 1, 18.0, 28.0, tzr + 2.3, tzr + 6.3))     # USB-C opening
    C["pack_base"] = base - b.Compound(children=ins + pin_holes)
    sub["pack_inserts"] = len(ins)

    # ---------------- 3 gearmotors, 4 spools, 20 idlers and pins ----------------
    mx0, mx1 = p["motor_x0"], d["motor_x1"]
    motors, spools, idlers, ipins, mscrews = [], [], [], [], []
    for sg in (1, -1):
        y = sg * p["motor_y"]
        m = _cyl_x(mx0, mx1, y, mz, p["motor_d"] / 2) + _cyl_x(mx1, mx1 + p["shaft_l"], y, mz, p["shaft_d"] / 2)
        for dy in (-p["face_hole_pitch"] / 2, p["face_hole_pitch"] / 2):
            m = m - _cyl_x(mx1 - 4, mx1 + 0.01, y + dy, mz, 1.5)
            mscrews.append(_cyl_x(mx1 - 3, bx1 - 1.7, y + dy, mz, 1.5) + _cyl_x(bx1 - 1.7, bx1, y + dy, mz, 3.0))
        motors.append(m)
        sx0 = d["spool_x0"]; hub = p["spool_hub_l"]; ft = p["flange_t"]; gw = d["groove_w"]
        fr, cr = p["spool_flange_d"] / 2, p["spool_core_d"] / 2
        s = _cyl_x(sx0, sx0 + hub, y, mz, cr)
        xx = sx0 + hub
        for seg, rr in ((ft, fr), (gw, cr), (ft, fr), (gw, cr), (ft, fr)):
            s = s + _cyl_x(xx, xx + seg, y, mz, rr)
            xx += seg
        s = s - _cyl_x(sx0 - 1, xx + 1, y, mz, p["shaft_d"] / 2)
        spools.append(s)
        for ix, lz in zip(d["idler_x"], d["line_z"]):
            ring = _cyl_z(lz - iwd / 2, lz + iwd / 2, ix, sg * iy, p["idler_d"] / 2) \
                - _cyl_z(lz - iwd, lz + iwd, ix, sg * iy, p["idler_bore"] / 2)
            idlers.append(ring)
        ipins.append(_cyl_z(fz + 2, zl + iwd / 2, ix_l, sg * iy, 1.5))
        ipins.append(_cyl_z(zu - iwd / 2, zu + iwd / 2 + 3.3, ix_u, sg * iy, 1.5))
    C["gearmotors"] = _fuse(motors)
    C["motor_screws"] = _fuse(mscrews)
    C["spools"] = _fuse(spools)
    C["idlers"] = _fuse(idlers)
    C["idler_pins"] = _fuse(ipins)

    # ---------------- 5 cells, 6 controller, 7 drivers, 18 charger, 23 tray, 25 regulator ----------------
    cells = [_cyl_y(-p["cell_l"] / 2, p["cell_l"] / 2, cxp, cz, p["cell_d"] / 2) for cxp in p["cell_x"]]
    C["cells"] = _fuse(cells)
    tray = _box(tray_x[0], tray_x[1], -(iw - 0.5), iw - 0.5, tzr, tzr + 2.0)
    for sg in (1, -1):
        for tx in (tray_x[0] + 4, tray_x[1] - 4):
            tray = tray - _cyl_z(tzr - 1, tzr + 3, tx, sg * 34.5, 1.1)
    C["tray"] = tray
    tt = tzr + 2.0
    rx = x0 + wl
    C["bms"] = _box(rx + 22, rx + 36, -11, 29, tt, tt + 4)
    C["controller"] = _box(rx + 1, rx + 19, -10, 11, tt, tt + 5)
    C["drivers"] = _box(rx + 1, rx + 16, -33, -13, tt, tt + 4) + _box(rx + 21, rx + 36, -33, -13, tt, tt + 4)
    C["charger"] = _box(rx + 1, rx + 16, 13, 33, tt, tt + 4) + _box(x0, rx + 2, 18.5, 27.5, tt + 0.5, tt + 4.0)
    C["tray_screws"] = _fuse([_cyl_z(tzr - 6, tt + 1.0, tx, sg * 34.5, 0.8) for sg in (1, -1)
                              for tx in (tray_x[0] + 4, tray_x[1] - 4)])
    C["regulator"] = _box(p["estop_x"] - 8, p["estop_x"] + 9, 14, 26, fz, fz + 4)

    # ---------------- 8 lid, 9 emergency stop ----------------
    lid = _box(x0, x1, -W / 2, W / 2, tz, tz + p["lid_t"])
    lid = lid - _cyl_z(tz - 1, tz + 3, p["estop_x"], 0, p["estop_d"] / 2 + 0.5)
    lid = lid - _cyl_z(tz - 1, tz + 3, rx + 10, 0.5, 1.5)                       # status LED window
    lscr = []
    for lx in p["lid_boss_x"]:
        for sg in (1, -1):
            lid = lid - _cyl_z(tz - 1, tz + 3, lx, sg * p["lid_boss_y"], 1.7)
            lscr.append(_cyl_z(tz + p["lid_t"], tz + p["lid_t"] + 1.8, lx, sg * p["lid_boss_y"], 2.75)
                        + _cyl_z(tz + p["lid_t"] - 8.0, tz + p["lid_t"], lx, sg * p["lid_boss_y"], 1.5))
    C["pack_lid"] = lid
    C["lid_screws"] = _fuse(lscr)
    ex, top = p["estop_x"], d["pack_top"]
    C["estop"] = (_cyl_z(top - p["estop_depth"], tz, ex, 0, p["estop_d"] / 2)
                  + _cyl_z(tz, top, ex, 0, p["estop_d"] / 2)
                  + _cyl_z(top, top + 1.0, ex, 0, 12.0)
                  + _cyl_z(top + 1.0, top + 8, ex, 0, 8)
                  + _cyl_z(top + 7, top + 12, ex, 0, p["estop_cap_d"] / 2))

    # ---------------- 10 anchor block: body, release plate, cover, pucks ----------------
    ax0, ax1 = d["anchor_x"]
    AW = p["anchor_w"] / 2
    az0, az1 = bb, tz                              # full pack height, so the block meets the whole front wall
    by, cw, ch = p["balance_y"], p["chan_w"], p["chan_h"]
    chans = []
    for sg in (1, -1):
        for lz in d["line_z"]:
            chans.append(_box(ax0 - 1, ax1 + 1, sg * by - cw / 2, sg * by + cw / 2, lz - ch / 2, lz + ch / 2))
    body = _box(ax0, ax1, -AW, AW, az0, az1) - b.Compound(children=chans)
    bholes = []
    cs_pts = [(sg * 30.0, cz_) for sg in (1, -1) for cz_ in (az0 + 2.8, az1 - 2.5)]
    d["cover_screw_pts"] = cs_pts
    for sg in (1, -1):
        for az in (mz + 6.0, mz - 6.0):
            bholes.append(_cyl_x(ax0 - 1, ax0 + 6, sg * 14.0, az, 2.0))           # inserts for the pack screws
            inserts.append(_cyl_x(ax0, ax0 + 5, sg * 14.0, az, 2.0) - _cyl_x(ax0 - 1, ax0 + 6, sg * 14.0, az, 1.5))
    for (yy, zz) in cs_pts:
        bholes.append(_cyl_x(ax1 - 6, ax1 + 1, yy, zz, 2.0))                     # inserts for the cover screws
        inserts.append(_cyl_x(ax1 - 5, ax1, yy, zz, 2.0) - _cyl_x(ax1 - 6, ax1 + 1, yy, zz, 1.5))
    # lightening pocket, open underneath, between the two pairs of channels
    pocket = _box(ax0 + 9.0, ax1 - 9.0, -(by - cw / 2 - 2.5), by - cw / 2 - 2.5, az0 - 1, az1 - 3.0)
    C["anchor_body"] = body - pocket - b.Compound(children=bholes)
    # release plate: slides out toward the thumb side when its loop is pulled; one horizontal slot per
    # row of tendons, open at the far edge, lets it slide off all eight tendons at once
    gx0, gx1 = d["gate_x"]
    gz0, gz1 = d["line_z"][1] - ch / 2 - 2.1, d["line_z"][0] + ch / 2 + 0.1
    d["gate_z"] = (gz0, gz1)
    gate = _box(gx0, gx1, -(AW - 4.25), AW, gz0, gz1) + _box(gx0, gx1, AW, AW + 18.0, gz0 + 2.0, gz1 - 2.0)
    for lz in d["line_z"]:
        gate = gate - _box(gx0 - 1, gx1 + 1, -AW - 1, by + 4.0 + 0.8, lz - 0.8, lz + 0.8)
    gate = gate - _cyl_x(gx0 - 1, gx1 + 1, AW + 10.0, (gz0 + gz1) / 2, 5.5)       # finger loop
    C["gate"] = gate
    d["gate_pull"] = 2 * AW + 4.0
    # cover: puck pockets behind a front wall with the sheath holes; four spacer bosses carry the cover screws
    cx0_, cx1_ = d["cover_x"]
    cover = _box(cx0_, cx1_, -AW, AW, az0, az1)
    for (yy, zz) in cs_pts:
        cover = cover + _cyl_x(gx0, cx0_, yy, zz, 2.5)
    pk = []
    sheath_holes = []
    for sg in (1, -1):
        for lz in d["line_z"]:
            pk.append(_box(cx0_ - 1, cx1_ - 2.0, sg * by - cw / 2, sg * by + cw / 2, lz - ch / 2, lz + ch / 2))
            for oy in (-4.0, 4.0):
                sheath_holes.append(_cyl_x(cx1_ - 3, cx1_ + 1, sg * by + oy, lz, 2.25))
    for (yy, zz) in cs_pts:
        sheath_holes.append(_cyl_x(gx0 - 1, cx1_ + 1, yy, zz, 1.7))
    C["cover"] = cover - b.Compound(children=pk + sheath_holes)
    pl_, pw_, ph_ = p["puck"]
    pucks, cscr = [], []
    for sg in (1, -1):
        for lz in d["line_z"]:
            pu = _box(gx1, gx1 + pl_, sg * by - pw_ / 2, sg * by + pw_ / 2, lz - ph_ / 2, lz + ph_ / 2)
            for oy in (-4.0, 4.0):
                pu = pu - _cyl_x(gx1 + pl_ - 3, gx1 + pl_ + 1, sg * by + oy, lz, 2.6) \
                    - _cyl_x(gx1 - 1, gx1 + pl_ + 1, sg * by + oy, lz, 0.8)
            pucks.append(pu)
    for (yy, zz) in cs_pts:
        cscr.append(_cyl_x(cx1_, cx1_ + 2.0, yy, zz, 2.75) + _cyl_x(ax1 - 5.0, cx1_, yy, zz, 1.5))
    C["pucks"] = _fuse(pucks)
    C["cover_screws"] = _fuse(cscr)
    C["inserts"] = _fuse(inserts)

    # ---------------- 22 balance pulleys with their line hardware, at mid travel ----------------
    bal, bpin, coup, spr = [], [], [], []
    bd, bw = p["balance_d"], p["balance_w"]
    bxc = ax0 + p["spring_l"] + bd / 2 + d["balance_travel"] / 2
    for sg in (1, -1):
        for lz in d["line_z"]:
            y = sg * by
            bal.append(_cyl_z(lz - bw / 2, lz + bw / 2, bxc, y, bd / 2) - _cyl_z(lz - bw, lz + bw, bxc, y, 1.5))
            bpin.append(_cyl_z(lz - 3.25, lz + 3.25, bxc, y, 1.5))
            spr.append(_cyl_x(bxc - bd / 2 - p["spring_l"], bxc - bd / 2 - 0.5, y, lz, 1.5))
            for oy in (-4.0, 4.0):
                c0 = bxc + bd / 2 + 1.0
                coup.append(_cyl_x(c0, c0 + p["coupling_l"], y + oy, lz, p["coupling_d"] / 2))
    C["balance_pulleys"] = _fuse(bal)
    C["balance_pins"] = _fuse(bpin)
    C["couplings"] = _fuse(coup)
    C["slack_springs"] = _fuse(spr)
    C["anchor_screws"] = _fuse([_cyl_x(x1 - wl - 3.0, x1 - wl, sg * 14.0, az, 2.75) + _cyl_x(x1 - wl, x1 + 6.0, sg * 14.0, az, 1.5)
                                for sg in (1, -1) for az in (mz + 6.0, mz - 6.0)])

    # ---------------- hand side ----------------
    GT, pt = p["glove_t"], p["plate_t"]
    gz = PT / 2 + GT
    mcp = PL - 4.0
    glove = _box(0, mcp, -(PW / 2 + GT), PW / 2 + GT, -gz, gz) - _box(-1, mcp + 1, -PW / 2, PW / 2, -PT / 2, PT / 2)
    glove = glove - (_tube(to, thumb_end, tr) + Pos(*thumb_end) * Sphere(tr))
    C["glove"] = glove
    stitch = lambda x0_, x1_, y0_, y1_, z0_, z1_, skip=None: [  # noqa: E731
        _cyl_z(z0_ - 1, z1_ + 1, xx, yy, 0.75)
        for xx, yy in ([(x0_ + 3 + 6 * i, y) for i in range(int((x1_ - x0_ - 6) // 6) + 1) for y in (y0_ + 3, y1_ - 3)]
                       + [(x, y0_ + 3 + 6 * i) for i in range(1, int((y1_ - y0_ - 6) // 6)) for x in (x0_ + 3, x1_ - 3)])
        if skip is None or not skip(xx)]
    # dorsal plate with the extensor sheath stop block (13)
    dp = _box(13, 63, -30, 30, gz, gz + pt)
    dp = dp - b.Compound(children=stitch(13, 63, -30, 30, gz, gz + pt, skip=lambda xx: xx < 23))
    zsd = gz + pt + 3.25
    blk = _box(13, 21, -28, 28, gz + pt, gz + pt + 6.5)
    for ys in p["stop_y"]:
        blk = blk - _cyl_x(12, 18, ys, zsd, 2.6) - _cyl_x(12, 22, ys, zsd, 0.8)
    C["dorsal_plate"] = dp + blk
    pp = _box(7, 41, -30, 30, -gz - pt, -gz)
    pp = pp - b.Compound(children=stitch(7, 41, -30, 30, -gz - pt, -gz, skip=lambda xx: xx < 17))
    zsp = -(gz + pt + 3.25)
    blk = _box(7, 15, -28, 28, -gz - pt - 6.5, -gz - pt)
    for ys in p["stop_y"]:
        blk = blk - _cyl_x(6, 12, ys, zsp, 2.6) - _cyl_x(6, 16, ys, zsp, 0.8)
    C["palmar_plate"] = pp + blk

    # sheaths: from the pucks to the stop blocks; outer channel line is the index or little finger
    so = p["sheath_od"] / 2
    sheaths, sheath_paths = [], []
    fx = d["anchor_front"]
    seat = gx1 + pl_ - 3.0
    for kind, k, pts in sheath_routes(d):
        sheath_paths.append((kind, k, _plen(pts[1:])))
        sheaths.append(_path(pts, so))
    d["sheath_pts"] = [pts for _, _, pts in sheath_routes(d)]
    C["sheaths"] = _fuse(sheaths)

    # finger cuffs (guide on the proximal phalanx, anchor on the middle phalanx) and thimbles:
    # padded dorsal and palmar saddles over the contact arc, short end walls, thin side bands (C9)
    ha = d["saddle_half_deg"]
    sbt = p["side_band_t"]
    ct2 = p["cuff_t"] + p["cuff_liner_t"]
    cuffs_t, cuffs_l, th_t, th_l, tendons, beads = [], [], [], [], [], []
    tr_ = 0.6
    vol = dict(cuff_tpu=0.0, cuff_liner=0.0, th_tpu=0.0, th_liner=0.0)

    def cuff(x0_, x1_, y, r, liner, wall, dorsal_tab, palmar_tab, slit=True):
        ro = r + liner + wall
        parts_t = []
        for c0 in (0.0, 180.0):
            parts_t.append(_sector(x0_, x1_, y, r + liner, ro, c0 - ha, c0 + ha))
            for e0 in (c0 - ha - 4.0, c0 + ha):
                parts_t.append(_sector(x0_, x1_, y, r, ro, e0, e0 + 4.0))
        for c0 in (90.0, 270.0):
            band = _sector(x0_, x1_, y, r, r + sbt, c0 - (90 - ha - 4.0), c0 + (90 - ha - 4.0))
            if slit and c0 == 270.0:
                band = band - _box(x0_ - 1, x1_ + 1, y - r - 2, y - r + 2, -0.75, 0.75)
            parts_t.append(band)
        lin = [_sector(x0_, x1_, y, r, r + liner, c0 - ha, c0 + ha) for c0 in (0.0, 180.0)]
        tabs = []
        for on, sgn in ((dorsal_tab, 1), (palmar_tab, -1)):
            if on:
                we = min(8.0, x1_ - x0_)
                xm = (x0_ + x1_) / 2
                t = _box(xm - we / 2, xm + we / 2, y - 2.5, y + 2.5, *(sorted((sgn * (ro - 0.5), sgn * (ro + 3.0)))))
                t = t - _cyl_x(xm - we, xm + we, y, sgn * (ro + 1.5), 1.0)
                tabs.append(t)
        return _fuse(parts_t + tabs), _fuse(lin), sgn

    d["tendon_h"] = []
    for i, fg in enumerate(d["finger_geom"]):
        y, r = fg["y"], fg["r"]
        gxa, gxb = fg["guide_x"] - p["guide_cuff_w"] / 2, fg["guide_x"] + p["guide_cuff_w"] / 2
        axa, axb = fg["anchor_x"] - fg["anchor_w"] / 2, fg["anchor_x"] + fg["anchor_w"] / 2
        txa, txb = fg["thimble_x"] - fg["thimble_w"] / 2, fg["thimble_x"] + fg["thimble_w"] / 2
        for xa, xb in ((gxa, gxb), (axa, axb)):
            t, l_, _ = cuff(xa, xb, y, r, p["cuff_liner_t"], p["cuff_t"], True, True)
            cuffs_t.append(t); cuffs_l.append(l_)
        t, l_, _ = cuff(txa, txb, y, r, p["cuff_liner_t"], p["thimble_t"], True, False, slit=False)
        th_t.append(t); th_l.append(l_)
        hc = r + ct2 + 1.5
        ht = r + p["cuff_liner_t"] + p["thimble_t"] + 1.5
        d["tendon_h"].append(hc)
        ys = p["stop_y"][i]
        e = [(21.0 - 4.0, ys, zsd), (24.0, ys, zsd), (64.0, ys + (y - ys) * 0.6, gz + pt + 1.1), (91.0, y * 0.98, gz + tr_ + 1.0), (gxa - 2.0, y, hc), (gxb, y, hc),
             (axa - 1.0, y, hc), (axb, y, hc), (txa - 1.0, y, ht), (txb + 0.5, y, ht)]
        f = [(15.0 - 4.0, ys, zsp), (18.0, ys, zsp), (42.0, ys + (y - ys) * 0.35, -gz - pt - 1.1), (91.0, y * 0.98, -gz - tr_ - 1.0), (gxa - 2.0, y, -hc), (gxb, y, -hc),
             (axa - 1.0, y, -hc), (axb + 0.5, y, -hc)]
        tendons.append(_path(e, tr_)); tendons.append(_path(f, tr_))
        for (a_, c_) in ((e[1], e[2]), (f[1], f[2])):
            u = 0.12
            q = tuple(a_[j] + (c_[j] - a_[j]) * u for j in range(3))
            qa = tuple(q[j] - (c_[j] - a_[j]) / _plen([a_, c_]) * 1.5 for j in range(3))
            qb = tuple(q[j] + (c_[j] - a_[j]) / _plen([a_, c_]) * 1.5 for j in range(3))
            beads.append(_tube(qa, qb, 1.25) - _tube(tuple(2 * qa[j] - qb[j] for j in range(3)), tuple(2 * qb[j] - qa[j] for j in range(3)), tr_))
    C["finger_cuffs"] = _fuse(cuffs_t)
    C["cuff_liners"] = _fuse(cuffs_l)
    C["thimbles"] = _fuse(th_t)
    C["thimble_liners"] = _fuse(th_l)
    C["tendons"] = _fuse(tendons)
    C["stop_beads"] = _fuse(beads)

    # 17 thumb abduction spacer: a ring on the thumb and a web block stitched to the glove's side
    s_ring = 40.0
    rc = tuple(to[i] + td[i] * s_ring for i in range(3))
    ring = Solid.make_cylinder(tr + 2.5, 12, Plane(origin=Vector(*rc) - Vector(*td) * 6, z_dir=Vector(*td)))
    ring = ring - Solid.make_cylinder(tr, 14, Plane(origin=Vector(*rc) - Vector(*td) * 7, z_dir=Vector(*td)))
    yb = PW / 2 + GT
    web = _box(44, 58, yb, yb + 9.5, -16, -2)
    for xs_ in (47.0, 55.0):
        for zs_ in (-12.0, -5.0):
            web = web - _cyl_y(yb - 1, yb + 3, xs_, zs_, 0.75)
    C["thumb_spacer"] = (ring + web) - (_tube(to, thumb_end, tr) + Pos(*thumb_end) * Sphere(tr))

    sub["cuff_shell"] = C["cuff_shell"]
    sub["cuff_liner"] = C["cuff_liner"]
    sub["cuff_straps"] = C["straps"]
    return {"c": C, "context": context, "sheath_paths": sheath_paths, "d": d, "sub": sub}


# BOM line for each component (matches bom/bom.csv)
COMP_LINE = {"cuff_shell": 1, "cuff_liner": 1, "straps": 1, "cuff_screws": 24, "pack_base": 2, "gearmotors": 3,
             "motor_screws": 24, "spools": 4, "idlers": 20, "idler_pins": 24, "cells": 5, "bms": 5, "controller": 6,
             "drivers": 7, "charger": 18, "tray": 23, "tray_screws": 24, "regulator": 25, "pack_lid": 8,
             "lid_screws": 24, "estop": 9, "anchor_body": 10, "gate": 10, "cover": 10, "pucks": 10, "cover_screws": 24, "inserts": 24, "anchor_screws": 24, "balance_pulleys": 22, "balance_pins": 24,
             "couplings": 10, "slack_springs": 10, "sheaths": 11, "glove": 12, "dorsal_plate": 13, "palmar_plate": 14,
             "finger_cuffs": 15, "cuff_liners": 15, "tendons": 16, "stop_beads": 10, "thumb_spacer": 17,
             "thimbles": 21, "thimble_liners": 21}

# grouped parts for the media, drawings and calculations: name -> component keys
GROUPS = {
    "forearm_cuff": ["cuff_shell", "cuff_liner", "straps"],
    "pack_base": ["pack_base"],
    "gearmotors": ["gearmotors"],
    "spools": ["spools"],
    "cells": ["cells", "bms"],
    "controller": ["controller"],
    "drivers": ["drivers"],
    "pack_lid": ["pack_lid"],
    "estop": ["estop"],
    "anchor_block": ["anchor_body", "gate", "cover", "pucks", "couplings", "slack_springs"],
    "sheaths": ["sheaths"],
    "glove": ["glove"],
    "dorsal_plate": ["dorsal_plate"],
    "palmar_plate": ["palmar_plate"],
    "finger_cuffs": ["finger_cuffs", "cuff_liners"],
    "tendons": ["tendons", "stop_beads"],
    "thumb_spacer": ["thumb_spacer"],
    "charger": ["charger"],
    "idlers": ["idlers", "idler_pins"],
    "thimbles": ["thimbles", "thimble_liners"],
    "balance_pulleys": ["balance_pulleys", "balance_pins"],
    "tray": ["tray"],
    "fixings": ["cuff_screws", "motor_screws", "tray_screws", "lid_screws", "cover_screws", "anchor_screws", "inserts"],
    "regulator": ["regulator"],
}
BOM_LINE = {"forearm_cuff": 1, "pack_base": 2, "gearmotors": 3, "spools": 4, "cells": 5, "controller": 6,
            "drivers": 7, "pack_lid": 8, "estop": 9, "anchor_block": 10, "sheaths": 11, "glove": 12,
            "dorsal_plate": 13, "palmar_plate": 14, "finger_cuffs": 15, "tendons": 16, "thumb_spacer": 17,
            "charger": 18, "idlers": 20, "thimbles": 21, "balance_pulleys": 22, "tray": 23, "fixings": 24,
            "regulator": 25}

_CACHE = {}


def build_parts(params=None):
    """Return {'parts': {group: shape}, 'c': components, 'context', 'sheath_paths', 'd', 'sub'}."""
    key = id(params) if params is not None else None
    if key in _CACHE:
        return _CACHE[key]
    import os
    cache = os.environ.get("FLEXHAND_CACHE") if params is None else None
    if cache:   # optional on-disk cache for repeated picture runs, keyed on this file's source
        import hashlib, pickle
        h = hashlib.sha1(Path(__file__).read_bytes()).hexdigest()[:12]
        f = Path(cache) / f"flexhand-{h}"
        if (f / "meta.pkl").exists():
            from build123d import import_brep
            meta = pickle.loads((f / "meta.pkl").read_bytes())
            C = {k: import_brep(str(f / f"c-{k}.brep")) for k in meta["c"]}
            m = {"c": C, "context": import_brep(str(f / "context.brep")), "sheath_paths": meta["sheath_paths"],
                 "d": meta["d"], "sub": dict(meta["sub_num"], **{k: C[v] for k, v in meta["sub_ref"].items()})}
            m["sub"]["cuff_shell_solid"] = import_brep(str(f / "c-_shell_solid.brep"))
            m["parts"] = {g: _fuse([C[k] for k in ks]) for g, ks in GROUPS.items()}
            _CACHE[key] = m
            return m
    m = components(params)
    C = m["c"]
    parts = {g: _fuse([C[k] for k in ks]) for g, ks in GROUPS.items()}
    m["parts"] = parts
    _CACHE[key] = m
    if cache:
        from build123d import export_brep
        f.mkdir(parents=True, exist_ok=True)
        for k, v in C.items():
            export_brep(v, str(f / f"c-{k}.brep"))
        export_brep(m["context"], str(f / "context.brep"))
        ref = {"cuff_shell": "cuff_shell", "cuff_liner": "cuff_liner", "cuff_straps": "straps"}
        export_brep(m["sub"]["cuff_shell_solid"], str(f / "c-_shell_solid.brep"))
        (f / "meta.pkl").write_bytes(pickle.dumps({"c": list(C), "sheath_paths": m["sheath_paths"], "d": m["d"],
                                                   "sub_num": {k: v for k, v in m["sub"].items() if isinstance(v, (int, float))},
                                                   "sub_ref": ref}))
    return m


def build(params=None):
    """Device assembly (no context) as one compound."""
    from build123d import Compound
    return Compound(children=list(build_parts(params)["parts"].values()))


# ------------------------------------------------------------------ constructability checks
# pairs that must touch (distance under 0.05 mm): the joints of the build plan
CONTACTS = [
    ("cuff_shell", "cuff_liner", "liner glued inside the shell"),
    ("cuff_shell", "pack_base", "saddle ribs on the shell"),
    ("cuff_shell", "cuff_screws", "screw heads on the inside face of the shell"),
    ("cuff_screws", "inserts", "screws in the heat-set inserts"), ("inserts", "pack_base", "inserts in the bosses"),
    ("lid_screws", "inserts", ""), ("anchor_screws", "inserts", ""), ("cover_screws", "inserts", ""),
    ("inserts", "anchor_body", "inserts in the block"),
    ("cuff_shell", "straps", "straps over the shell"),
    ("gearmotors", "pack_base", "gearbox face on the bulkhead, can in the cradle"),
    ("motor_screws", "pack_base", "screws countersunk in the bulkhead"),
    ("spools", "gearmotors", "spool on the shaft"),
    ("idlers", "idler_pins", "bearing on its pin"),
    ("idler_pins", "pack_base", "pins in the post and shelf"),
    ("cells", "pack_base", "cells in their saddles"),
    ("tray", "pack_base", "tray on its posts"),
    ("tray_screws", "pack_base", "tray screws in the posts"),
    ("controller", "tray", "boards on the tray"), ("drivers", "tray", ""), ("bms", "tray", ""), ("charger", "tray", ""),
    ("regulator", "pack_base", "regulator on the floor"),
    ("pack_lid", "pack_base", "lid on the walls"),
    ("lid_screws", "pack_lid", "lid screw heads on the lid"),
    ("estop", "pack_lid", "stop button through the lid"),
    ("anchor_body", "pack_base", "block against the pack front wall"),
    ("anchor_screws", "pack_base", "screw heads inside the front wall"),
    ("gate", "anchor_body", "gate against the block front face"),
    ("cover", "anchor_body", "cover spacers against the block front face"),
    ("pucks", "gate", "pucks bear on the gate"),
    ("cover_screws", "cover", "cover screw heads"),
    ("balance_pulleys", "balance_pins", "pulley on its pin"),
    ("glove", "dorsal_plate", "plate stitched to the glove"),
    ("glove", "palmar_plate", "plate stitched to the glove"),
    ("glove", "thumb_spacer", "spacer stitched to the glove"),
    ("finger_cuffs", "cuff_liners", "liners glued in the saddles"),
    ("thimbles", "thimble_liners", "liners glued in the saddles"),
]
# pairs that must not touch, with the least gap (mm)
CLEARANCES = [
    ("spools", "idlers", 0.5), ("spools", "pack_base", 0.3), ("idlers", "pack_base", 0.2),
    ("gearmotors", "estop", 5.0), ("gearmotors", "pack_lid", 1.0), ("cells", "estop", 1.0),
    ("tray", "estop", 1.0), ("regulator", "estop", 1.0), ("controller", "pack_lid", 0.5),
    ("straps", "pack_base", 1.0), ("anchor_screws", "spools", 2.0), ("anchor_screws", "idlers", 2.0),
    ("balance_pulleys", "anchor_body", 0.5), ("couplings", "anchor_body", 0.0), ("sheaths", "glove", 0.3),
    ("pucks", "cover", 0.2),
]


def check(params=None, verbose=True):
    """Constructability checks: no two parts overlap, each joint touches, each clearance holds,
    every component carries a fixing or sits in a pocket. Returns (passed, failed) counts."""
    import itertools
    m = build_parts(params)
    C = dict(m["c"])
    ctx = m["context"]
    keys = list(C)
    ok = bad = 0
    lines = []

    def vol(s_):
        try:
            return 0.0 if s_ is None else s_.volume
        except Exception:
            return 0.0

    def bbo(a, b_):
        A, B = a.bounding_box(), b_.bounding_box()
        return not (A.max.X < B.min.X - 0.1 or B.max.X < A.min.X - 0.1 or A.max.Y < B.min.Y - 0.1
                    or B.max.Y < A.min.Y - 0.1 or A.max.Z < B.min.Z - 0.1 or B.max.Z < A.min.Z - 0.1)
    for a, c in itertools.combinations(keys, 2):
        if not bbo(C[a], C[c]):
            continue
        v = vol(C[a] & C[c])
        if v > 0.5:
            bad += 1; lines.append(f"FAIL overlap {a} x {c}: {v:.1f} mm3")
        else:
            ok += 1
    soft = {"glove", "straps", "cuff_liner", "cuff_liners", "thimble_liners", "finger_cuffs", "thimbles",
            "thumb_spacer", "tendons"}
    for a in keys:
        if a in soft or not bbo(C[a], ctx):
            continue
        v = vol(C[a] & ctx)
        if v > 0.5:
            bad += 1; lines.append(f"FAIL {a} inside the forearm or hand: {v:.1f} mm3")
        else:
            ok += 1
    for a in soft:
        v = vol(C[a] & ctx)
        if v > 0.5:
            bad += 1; lines.append(f"FAIL {a} inside the forearm or hand: {v:.1f} mm3")
        else:
            ok += 1
    for a, c, why in CONTACTS:
        dd = C[a].distance_to(C[c])
        if dd < 0.05:
            ok += 1
        else:
            bad += 1; lines.append(f"FAIL {a} should touch {c} ({why}): gap {dd:.2f} mm")
    for a, c, gap in CLEARANCES:
        dd = C[a].distance_to(C[c])
        v = vol(C[a] & C[c])
        if dd >= gap - 1e-6 and v < 0.5:
            ok += 1
        else:
            bad += 1; lines.append(f"FAIL {a} to {c}: {dd:.2f} mm, needs {gap} mm")
    # release: the plate must slide out toward the thumb side, clear of everything but the pucks it carries
    from build123d import Pos
    d = m["d"]
    sweep = _fuse([Pos(0, t, 0) * C["gate"] for t in (5.0, 20.0, 40.0, 60.0, d["gate_pull"])])
    for k in ("anchor_body", "cover", "cover_screws", "pack_base", "pack_lid", "sheaths", "balance_pulleys", "couplings"):
        v = vol(sweep & C[k])
        if v > 0.5:
            bad += 1; lines.append(f"FAIL release plate path blocked by {k}: {v:.1f} mm3")
        else:
            ok += 1
    for k in keys:
        n = len(C[k].solids())
        lines.append(f"     {k:16s} {n:3d} solid(s), {C[k].volume / 1000:8.2f} cm3")
    if verbose:
        for ln in lines:
            print(ln)
        print(f"Constructability checks: {ok} passed, {bad} failed")
    return ok, bad


def export(out=None):
    from build123d import Compound, export_step, export_stl
    import copy
    out = Path(out) if out else Path(__file__).resolve().parents[1]
    (out / "step").mkdir(parents=True, exist_ok=True); (out / "stl").mkdir(parents=True, exist_ok=True)
    m = build_parts()
    parts = m["parts"]
    asm = Compound(children=[copy.copy(v) for v in parts.values()])
    export_step(asm, str(out / "step" / "flexhand-assembly.step"))
    export_stl(asm, str(out / "stl" / "flexhand-assembly.stl"), tolerance=0.05, angular_tolerance=0.3)
    export_step(Compound(children=[copy.copy(v) for v in parts.values()] + [copy.copy(m["context"])]),
                str(out / "step" / "flexhand-on-forearm.step"))
    C = m["c"]
    made = {"cuff-shell": C["cuff_shell"], "pack-base": C["pack_base"], "pack-lid": C["pack_lid"],
            "electronics-tray": C["tray"], "spools": C["spools"], "anchor-body": C["anchor_body"],
            "release-plate": C["gate"], "cover": C["cover"], "pucks": C["pucks"],
            "dorsal-plate": C["dorsal_plate"], "palmar-plate": C["palmar_plate"], "finger-cuffs": C["finger_cuffs"],
            "thimbles": C["thimbles"], "thumb-spacer": C["thumb_spacer"]}
    for name, s in made.items():
        export_step(s, str(out / "step" / f"flexhand-{name}.step"))
        export_stl(s, str(out / "stl" / f"flexhand-{name}.stl"), tolerance=0.05, angular_tolerance=0.3)
    return m


if __name__ == "__main__":
    import sys
    if "--check" in sys.argv:
        _, nbad = check()
        sys.exit(1 if nbad else 0)
    m = export()
    d = m["d"]
    print(f"Pack envelope {d['pack_l']:.0f} x {d['pack_w']:.0f} mm, top {d['pack_top']:.1f} mm above forearm axis")
    print(f"Anchor block {d['anchor_total_l']:.1f} long x {d['anchor_w']:.0f} wide, front at x = {d['anchor_front']:.1f}")
    for name, s in m["parts"].items():
        print(f"{name:16s} volume {s.volume / 1000:8.2f} cm3")
    for kind, k, Lp in m["sheath_paths"]:
        print(f"sheath {kind} {k}: {Lp:.0f} mm neutral path")
    print("Wrote cad/step/*.step and cad/stl/*.stl")
