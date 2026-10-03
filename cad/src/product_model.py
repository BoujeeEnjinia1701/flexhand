"""FlexHand product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: a filleted motor pack with a parting line, aluminium lid screws,
a clear window over the spools, a guarded emergency stop, a start button and a lit status LED; a
perforated forearm cuff with foam liner and hook-and-loop straps; a filleted sheath anchor block (four channels, cover with
four screws and sheath pucks, red pull-out release plate with finger loop); swept Bowden sheaths with metal ferrules; a knit fingerless glove with
TPU dorsal and palmar plates; padded saddle finger cuffs with thin side bands, fingertip thimbles and a thumb spacer; and
visible tendon line. APPEARANCE MODEL ONLY: no tolerances, no fabrication detail.
CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface of the motor pack, anchor block and sheath ends comes from
PARAMS and derived() in model.py. The soft hand-side parts and the forearm cuff are fitted to the
shared clay forearm and hand (.kit/context_parts.py) so they sit on it plausibly; widths and
thicknesses stay as model.py (see docs/REVIEW.md, session 2026-09-26).

Axes as model.py (right forearm and hand, palm down): X from the elbow toward the fingertips with
the wrist at X = 0, +Y on the thumb (radial) side, Z dorsal (up).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from math import cos, radians, sin
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / ".kit"))

from build123d import (Align, Axis, Box, Circle, Cylinder, Ellipse, Plane, Pos, RectangleRounded, Rot,  # noqa: E402
                       Polygon, SlotOverall, Solid, Spline, Text, Vector, extrude, fillet, loft, sweep)
from model import PARAMS, build_parts, derived  # noqa: E402

TITLE = "FlexHand: tendon-driven finger exoskeleton for continuous passive motion"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); worn on a right "
             "forearm and hand, motor pack on the forearm, tendons along the fingers"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): motor pack lid, "
             "gearmotors and spools, battery and electronics, pack base, anchor block, sheaths, forearm "
             "cuff and straps, glove and plates, finger cuffs, thimbles and tendons"},
    {"name": "detail", "groups": ["shell", "internal", "context"], "explode": False, "el": 24, "az": 50,
     "note": "Thumb-side view from the back right and above (about 24 deg elevation): thumb spacer, radial "
             "flexor sheaths wrapping the wrist to the palmar plate, and the clear window over the spools"},
]

# Colours (restrained product palette; accent from the kit)
C_ACCENT = "#0F766E"
C_LID = "#E8EAED"
C_BASE = "#B9C0C8"
C_GRAPHITE = "#5B6571"
C_DARK = "#23272E"
C_FOAM = "#C9CDD2"
C_STRAP = "#262B32"
C_GLOVE = "#4A525D"
C_KNIT = "#2F353D"
C_PLATE = "#DDE1E5"
C_CUFF = C_ACCENT
C_THIMBLE = "#138A80"
C_TENDON = "#E08A1E"
C_SHEATH = "#1C1F24"
C_METAL = "#B8BEC6"
C_METAL_DK = "#7C838C"
C_RED = "#C62828"
C_YELLOW = "#E9B824"
C_WINDOW = "#DCEBF5"
C_LED = "#34D399"
C_PCB_GREEN = "#166534"
C_PCB_BLACK = "#1A1D21"
C_PCB_BLUE = "#1E3A8A"
C_CELL = "#2C4A7A"
C_SPOOL = "#EDEBE6"
C_CLAY = "#A9ADB2"

# Appearance-only detail sizes (mm)
PACK_R = 8.0            # plan corner radius of the pack and lid
WIN = (-96.0, -63.0, 27.0, 4.0)   # clear spool window: x0, x1, half width, corner radius
BUTTON_XY = (-128.0, 0.0)          # start and pause button (appearance)
LED_XY = (-112.0, 0.0)             # status LED light pipe
TENDON_R = 0.6          # tendon drawn a little oversize (0.8 mm line) so it reads in renders
SHEATH_R = 2.0

# Shared clay hand constants (copied from .kit/context_parts.py, side="left" puts the thumb at +Y)
ARM_SECS = [(-250.0, 78, 68), (-175.0, 80, 66), (-87.5, 70, 52), (0.0, 60, 40)]
PALM_SECS = [(0.0, 60, 40), (25, 76, 34), (60, 84, 30), (88, 82, 26)]
CLAY_FINGERS = [(+0.33, 76, 9.2, 4), (+0.11, 84, 9.4, 1), (-0.11, 80, 9.0, -2), (-0.33, 64, 8.0, -6)]
SEGS = (0.45, 0.30, 0.25)


# ---------------------------------------------------------------- helpers
def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _prism(L, W, r, z0, h, x=0.0, y=0.0):
    r = max(min(r, min(L, W) / 2 - 0.01), 0.01)
    return Pos(x, y, z0) * extrude(RectangleRounded(L, W, r), amount=h)


def _top_edges(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom_edges(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _v(p):
    return Vector(*p)


def _frame(origin, d, up=(0, 0, 1)):
    """Plane at origin with z along d and x toward `up` (perpendicular part)."""
    d = _v(d).normalized()
    u = _v(up)
    n = (u - d * u.dot(d))
    n = n.normalized() if n.length > 1e-6 else Vector(1, 0, 0)
    return Plane(origin=_v(origin), x_dir=n, z_dir=d)


def _tube(pl, r_in, r_out, w):
    """Ring of width w centred on plane pl (axis along pl z)."""
    base = Plane(origin=pl.origin - pl.z_dir * (w / 2), x_dir=pl.x_dir, z_dir=pl.z_dir)
    ring = Solid.make_cylinder(r_out, w, base)
    if r_in > 0:
        inner = Plane(origin=base.origin - base.z_dir * 1.0, x_dir=pl.x_dir, z_dir=pl.z_dir)
        ring = ring - Solid.make_cylinder(r_in, w + 2.0, inner)
    return ring


def _saddle(pl, ri, ro, w, ha, sbt=1.0):
    """Finger cuff as built in model.py: padded dorsal and palmar saddles over the contact arc, joined by
    thin side bands (FXH-DDR-003, C9). Cross-section plane pl, axis along its z."""
    ring = _tube(pl, ri, ro, w)
    ring = _fillet_try(ring, ring.edges(), [0.8, 0.5])
    k = 3.0 * ro / max(sin(radians(ha)), 0.3)
    base = Plane(origin=pl.origin - pl.z_dir * (w / 2 + 1.0), x_dir=pl.x_dir, z_dir=pl.z_dir)
    outer = _tube(pl, ri + sbt, ro + 3.0, w + 2.0)
    for sgn in (1, -1):
        pts = [(0, 0), (k * cos(radians(ha)), sgn * k * sin(radians(ha))), (-k * cos(radians(ha)), sgn * k * sin(radians(ha)))]
        wedge = extrude(base * Polygon(*pts, align=None), amount=w + 2.0)
        try:
            ring = ring - (wedge & outer)
        except Exception:
            pass
    return ring


def _rod(a, b, r):
    a, b = _v(a), _v(b)
    return Solid.make_cylinder(r, (b - a).length, Plane(origin=a, z_dir=(b - a).normalized()))


def _polyline_tube(pts, r):
    s = None
    for a, b in zip(pts[:-1], pts[1:]):
        seg = _rod(a, b, r)
        s = seg if s is None else s + seg
    for q in pts[1:-1]:
        s = s + Pos(*q) * Solid.make_sphere(r)
    return s


def _swept(pts, r, t0=(1, 0, 0), t1=(1, 0, 0)):
    """Circle of radius r swept along a spline through pts; falls back to a polyline of rods."""
    try:
        path = Spline(*[_v(p) for p in pts], tangents=[_v(t0), _v(t1)])
        prof = Plane(origin=path @ 0, z_dir=path % 0) * Circle(r)
        s = sweep(prof, path=path)
        s = s.solids()[0] if hasattr(s, "solids") else s
        if s.is_valid and s.volume > 0:
            return s
    except Exception:
        pass
    return _polyline_tube(pts, r)


def _ring_offset_loft(secs, off, x0, x1):
    """Loft of the clay sections offset outward by `off`, trimmed to x0..x1 (elliptical approximation)."""
    wires = []
    for x, a, b in secs:
        pl = Plane(origin=(x, 0, 0), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
        wires.append(pl * Ellipse(a / 2 + off, b / 2 + off))
    body = loft(wires)
    return body & Pos((x0 + x1) / 2, 0, 0) * Box(x1 - x0, 400, 400)


# ---------------------------------------------------------------- clay hand axes (from context_parts)
def _clay_fingers():
    """Axis polylines and radii of the clay fingers (index to little) and thumb, as context_parts builds them."""
    out = []
    for yf, L, r, spread in CLAY_FINGERS:
        base = Vector(86, yf * 80 * 0.95, -2.0)
        out.append(_chain(base, L, r, spread, (8, 10, 8)))
    thumb = _chain(Vector(22, 34, -6.0), 62, 10.5, 38, (20, 12, 10))
    return out, thumb


def _chain(base, L, r, spread, curl):
    pts, ang, yaw = [base], 0.0, radians(spread)
    for s, c in zip(SEGS, curl):
        ang += radians(c)
        step = L * s
        pts.append(pts[-1] + Vector(step * cos(ang) * cos(yaw), step * cos(ang) * sin(yaw), -step * sin(ang)))
    radii = [(r * (1 - 0.08 * i), r * (1 - 0.08 * (i + 1))) for i in range(3)]
    return {"pts": pts, "radii": radii}


def _on_seg(f, i, t):
    """Point, unit direction and local radius at distance t along segment i of a clay finger."""
    a, b = f["pts"][i], f["pts"][i + 1]
    d = (b - a)
    L = d.length
    d = d.normalized()
    r0, r1 = f["radii"][i]
    return a + d * t, d, r0 + (r1 - r0) * t / L, L


# ---------------------------------------------------------------- product parts
def product_parts(P=PARAMS):
    D = derived(P)
    M = build_parts(P)
    mp = M["parts"]
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    x0, x1 = P["pack_x"]
    L, W, wl = D["pack_l"], P["pack_w"], P["wall"]
    xc = (x0 + x1) / 2
    fz, tz, top = P["floor_z"], D["top_z"], D["pack_top"]
    box_bot = fz - P["floor_t"]
    mz, re_ = D["motor_z"], D["spool_r_eff"]
    lt, ct = P["liner_t"], P["cuff_t"]
    cx0, cx1 = P["cuff_x"]

    # ================= forearm cuff (BOM 1), fitted to the clay forearm =================
    keep_top = Pos(0, 0, 60 - 8) * Box(1000, 200, 120)      # as model.py: upper half plus 8 mm
    hx0, hx1, hstep = P["cuff_hole_x"]
    holes, xh = [], hx0
    while xh <= hx1 + 1e-6:
        for a in P["cuff_hole_ang"]:
            holes.append(Pos(xh, 0, 0) * Rot(a, 0, 0) * Pos(0, 0, 50) * Cylinder(P["cuff_hole_d"] / 2, 60))
        xh += hstep
    holes = _union(holes)
    o_in, o_mid, o_out = 0.2, lt, lt + ct
    shell = (_ring_offset_loft(ARM_SECS, o_out, cx0, cx1) - _ring_offset_loft(ARM_SECS, o_mid, cx0 - 1, cx1 + 1)) & keep_top
    shell = _fillet_try(shell, [e for e in shell.edges() if e.bounding_box().size.X < 0.5], [0.8, 0.5])
    shell -= holes
    liner = (_ring_offset_loft(ARM_SECS, o_mid, cx0, cx1) - _ring_offset_loft(ARM_SECS, o_in, cx0 - 1, cx1 + 1)) & keep_top
    liner -= holes
    add("Forearm cuff shell (perforated PETG)", shell, C_GRAPHITE, "plastic", 1, "shell", (0, 0, -55))
    add("Forearm cuff liner (EVA foam)", liner, C_FOAM, "rubber", 1, "shell", (0, 0, -32))
    cuff_outer = _ring_offset_loft(ARM_SECS, o_out, cx0 - 20, cx1 + 20)

    # hook-and-loop straps: over the cuff on top, on the skin underneath, with a buckle and pull tab
    sw = P["strap_w"]
    straps, buckles, tabs = [], [], []
    for xs in P["strap_x"]:
        a0, a1 = xs - sw / 2, xs + sw / 2
        upper = (_ring_offset_loft(ARM_SECS, o_out + 1.8, a0, a1) - _ring_offset_loft(ARM_SECS, o_out + 0.1, a0 - 1, a1 + 1)) & keep_top
        lower = (_ring_offset_loft(ARM_SECS, 1.8, a0, a1) - _ring_offset_loft(ARM_SECS, 0.2, a0 - 1, a1 + 1)) \
            & Pos(0, 0, -8 - 60) * Box(1000, 200, 120)
        lip = (_ring_offset_loft(ARM_SECS, o_out + 1.8, a0, a1) - _ring_offset_loft(ARM_SECS, 0.2, a0 - 1, a1 + 1)) \
            & Pos(0, 0, -9.0) * Box(1000, 200, 2.0)
        straps.append(upper + lower + lip)
        # buckle on the ulnar (-Y) side, just above the cuff edge
        halfw = upper.bounding_box().max.Y
        yb = -(halfw + 1.6)
        bk = Pos(xs, yb, 1.0) * Box(sw + 5, 2.4, 11.0)
        bk -= Pos(xs, yb, 1.0) * Box(sw + 1, 5.0, 3.0)
        bk = _fillet_try(bk, bk.edges().filter_by(Axis.Y), [1.2, 0.8, 0.4])
        buckles.append(bk)
        tab = Pos(xs + sw / 2 + 5.0, yb - 1.2, 1.0) * Box(12.0, 1.0, 8.0)
        tab = _fillet_try(tab, tab.edges().filter_by(Axis.Y), [2.5, 1.5])
        tabs.append(tab)
    add("Forearm straps (hook and loop)", _union(straps), C_STRAP, "fabric", 1, "shell", (0, 0, -85))
    add("Strap buckles", _union(buckles), C_DARK, "plastic", 1, "shell", (0, -14, -85))
    add("Strap pull tabs", _union(tabs), C_ACCENT, "fabric", 1, "shell", (0, -14, -85))
    strap_env = _union([_ring_offset_loft(ARM_SECS, o_out + 2.0, xs - sw / 2 - 0.5, xs + sw / 2 + 0.5)
                        for xs in P["strap_x"]])

    # ================= pack base (BOM 2) =================
    base = _prism(L, W, PACK_R, box_bot, tz - box_bot, x=xc)
    base = _fillet_try(base, _bottom_edges(base), [3.0, 2.0, 1.0])
    base = _fillet_try(base, _top_edges(base), [0.8, 0.5])            # half of the parting-line groove
    base -= _prism(L - 2 * wl, W - 2 * wl, PACK_R - wl, fz, tz - fz + 2, x=xc)
    ribs = []
    for xr in P["rib_x"]:                                               # three saddle ribs as model.py (3 mm)
        rb = Pos(xr, 0, (box_bot + 18) / 2 + 0.01) * Box(P["rib_t"], W - 6, box_bot - 18)
        ribs.append(rb)
    ribs = _union(ribs) - cuff_outer - strap_env
    base = base + ribs
    for sgn in (1, -1):                                                 # tendon exit slots, as model.py
        base -= Pos(x1 - wl / 2, sgn * 31.0, mz) * Box(wl + 2, 6, 2 * re_ + 4)
    # USB-C charge port through the rear wall at the charger (BOM 18)
    tray_z = fz + 1.0 + P["cell_d"] + 1.0
    usb_z = tray_z + 2.0
    base -= Pos(x0 - 2, 24.0, usb_z) * extrude(Plane.YZ * SlotOverall(9.4, 3.6), amount=wl + 4)
    # shallow grip texture: horizontal ribs on both long sides, toward the rear
    for k in range(6):
        z = box_bot + 8.0 + 3.0 * k
        for sgn in (1, -1):
            base -= Pos(x0 + 32, sgn * W / 2, z) * Box(36.0, 1.0, 1.2)
    add("Pack base (PETG)", base, C_BASE, "plastic", 2, "shell", (0, 0, 0))
    ins = Pos(x0 + 0.2, 24.0, usb_z) * extrude(Plane.YZ * SlotOverall(9.0, 3.3), amount=2.5)
    ins -= Pos(x0 - 0.1, 24.0, usb_z) * extrude(Plane.YZ * SlotOverall(8.0, 2.4), amount=1.2)
    ins += Pos(x0 + 1.2, 24.0, usb_z) * Box(1.0, 6.4, 0.7)
    add("USB-C port insert", ins, C_DARK, "plastic", 18, "shell", (-20, 0, 60))

    # ================= pack lid (BOM 8) with window, stop, button, LED, screws, marking =================
    lt_ = P["lid_t"]
    lid = _prism(L, W, PACK_R, tz, lt_, x=xc)
    lid = _fillet_try(lid, _top_edges(lid), [1.5, 1.0, 0.6])
    lid = _fillet_try(lid, _bottom_edges(lid), [0.6, 0.4])
    wx0, wx1, wy, wr = WIN
    lid -= _prism(wx1 - wx0 + 3, 2 * wy + 3, wr + 1.5, top - 0.8, 2.0, x=(wx0 + wx1) / 2)
    lid -= _prism(wx1 - wx0, 2 * wy, wr, tz - 1, lt_ + 2, x=(wx0 + wx1) / 2)
    lid -= Pos(P["estop_x"], 0, tz + lt_ / 2) * Cylinder(P["estop_d"] / 2 + 0.5, lt_ + 2)
    lid -= Pos(*BUTTON_XY, tz + lt_ / 2) * Cylinder(6.6, lt_ + 2)
    lid -= Pos(*LED_XY, tz + lt_ / 2) * Cylinder(1.8, lt_ + 2)
    screw_xy = [(lx_, sy * P["lid_boss_y"]) for lx_ in P["lid_boss_x"] for sy in (1, -1)]   # over the lid bosses
    for (sx_, sy_) in screw_xy:
        lid -= Pos(sx_, sy_, top - 0.4) * Cylinder(3.1, 0.9)
        lid -= Pos(sx_, sy_, tz + lt_ / 2) * Cylinder(1.7, lt_ + 2)
    try:
        mark = Pos(x0 + 22.0, 0, top) * Rot(0, 0, 90) * extrude(Text("FLEXHAND", 6.5, align=(Align.CENTER, Align.CENTER)), amount=0.35)
        if not mark.is_valid:
            raise ValueError
        lid += mark
    except Exception:
        pass
    # thin accent line along the lid, ulnar side (marking)
    add("Pack lid (PETG)", lid, C_LID, "plastic", 8, "shell", (0, 0, 110))
    stripe = _prism(L - 30, 1.6, 0.8, top, 0.3, x=xc + 5, y=-(W / 2 - 6.0))
    for lx_ in P["lid_boss_x"]:
        stripe -= Pos(lx_, -P["lid_boss_y"], top) * Cylinder(3.6, 2.0)
    add("Lid accent line", stripe, C_ACCENT, "painted", 8, "shell", (0, 0, 110))
    glass = _prism(wx1 - wx0 + 2.6, 2 * wy + 2.6, wr + 1.3, top - 0.8, 0.6, x=(wx0 + wx1) / 2)
    add("Spool window (clear)", glass, C_WINDOW, "clear", 8, "shell", (0, 0, 122))
    btn = Pos(*BUTTON_XY, tz + 1.3) * Cylinder(6.0, 3.4)
    btn = _fillet_try(btn, _top_edges(btn), [1.2, 0.8, 0.4])
    btn -= Pos(*BUTTON_XY, top + 1.0 + 0.3) * Box(1.0, 5.0, 0.8)       # pause mark, two bars
    add("Start and pause button", btn, C_ACCENT, "rubber", 6, "shell", (0, 0, 132))
    led = Pos(*LED_XY, tz + 1.2) * Cylinder(1.6, 2.6)
    led = _fillet_try(led, _top_edges(led), [0.6, 0.3])
    add("Status LED (lit)", led, C_LED, "emissive", 6, "shell", (0, 0, 132))
    screws = []
    for (sx_, sy_) in screw_xy:
        h = Pos(sx_, sy_, top - 0.9 + 0.7) * Cylinder(2.8, 1.4)
        h = _fillet_try(h, _top_edges(h), [0.6, 0.4])
        h -= Pos(sx_, sy_, top + 0.2) * Rot(0, 0, 15) * Box(2.2, 2.2, 1.0)
        h += Pos(sx_, sy_, top - 0.9 - 4.0) * Cylinder(1.5, 8.0)
        screws.append(h)
    add("Lid screws (4, aluminium)", _union(screws), C_METAL, "metal", 19, "shell", (0, 0, 150))

    # ================= emergency stop (BOM 9) =================
    ex = P["estop_x"]
    collar = Pos(ex, 0, top + 0.75) * (Cylinder(15.0, 1.5) - Cylinder(P["estop_d"] / 2 + 0.3, 2.0))
    collar = _fillet_try(collar, _top_edges(collar), [0.6, 0.4])
    add("Emergency stop collar", collar, C_YELLOW, "plastic", 9, "shell", (0, 0, 150))
    body = Pos(ex, 0, top - P["estop_depth"] / 2) * Cylinder(P["estop_d"] / 2, P["estop_depth"])
    add("Emergency stop body", body, C_DARK, "plastic", 9, "internal", (0, 0, 150))
    cap = Pos(ex, 0, top + 4) * Cylinder(8, 8)
    head = Pos(ex, 0, top + 9.5) * Cylinder(P["estop_cap_d"] / 2, 5)
    head = _fillet_try(head, _top_edges(head), [2.5, 1.8, 1.0])
    head = _fillet_try(head, _bottom_edges(head), [0.8, 0.5])
    for k in range(16):
        a = 360.0 * k / 16
        head -= Pos(ex, 0, top + 9.0) * Rot(0, 0, a) * Pos(P["estop_cap_d"] / 2, 0, 0) * Box(1.2, 1.2, 3.2)
    add("Emergency stop mushroom", cap + head, C_RED, "plastic", 9, "shell", (0, 0, 175))

    # ================= sheath anchor block (BOM 10): block, release plate, cover, pucks =================
    ax0, ax1 = x1, x1 + P["anchor_l"]
    az0, az1 = box_bot, tz                         # full pack height, as model.py
    AW = P["anchor_w"] / 2
    by, bd, bw = P["balance_y"], P["balance_d"], P["balance_w"]
    anc = Pos((ax0 + ax1) / 2, 0, (az0 + az1) / 2) * Box(P["anchor_l"], 2 * AW, az1 - az0)
    anc = _fillet_try(anc, anc.edges().filter_by(Axis.Z), [4.0, 3.0, 2.0])
    anc = _fillet_try(anc, _top_edges(anc), [1.5, 1.0])
    for sgn in (1, -1):
        for lz in D["line_z"]:
            anc -= Pos((ax0 + ax1) / 2, sgn * by, lz) * Box(P["anchor_l"] + 2, P["chan_w"], P["chan_h"])
    anc -= Pos((ax0 + ax1) / 2, 0, az0 + (az1 - az0) / 2 - 1.5) * Box(P["anchor_l"] - 14.0, 2 * (by - P["chan_w"] / 2 - 2.0), az1 - az0 - 2.5)
    add("Sheath anchor block (PETG)", anc, C_LID, "plastic", 10, "shell", (45, 0, 0))
    Cm = M["c"]
    add("Release plate with pull loop", Cm["gate"], C_RED, "plastic", 10, "shell", (62, 0, 0))
    add("Sheath pucks (4)", Cm["pucks"], C_DARK, "plastic", 10, "shell", (78, 0, 0))
    add("Anchor cover (PETG)", Cm["cover"], C_LID, "plastic", 10, "shell", (95, 0, 0))
    add("Cover screws (4, aluminium)", Cm["cover_screws"], C_METAL, "metal", 24, "shell", (112, 0, 0))
    bal = []
    for sgn in (1, -1):
        for zc in D["line_z"]:
            c = Pos(ax0 + wl + bd / 2 + D["balance_travel"] / 2, sgn * by, zc)
            ring = c * (Cylinder(bd / 2, bw) - Cylinder(bd / 2 - 1.0, bw + 1))
            bal.append(ring + c * Cylinder(bd / 2 - 1.0, bw - 0.4) + c * Cylinder(1.5, bw + 2.0))
    add("Balance pulleys (4)", _union(bal), C_METAL, "metal", 22, "internal", (45, 0, 55))

    # ================= gearmotors (BOM 3), spools (BOM 4), idlers (BOM 20), pack tendon runs =================
    mx0, mx1 = P["motor_x0"], D["motor_x1"]
    mr = P["motor_d"] / 2
    cans, gearboxes, encoders, shafts = [], [], [], []
    for sgn in (1, -1):
        y = sgn * P["motor_y"]

        def seg(xa, xb, r, y=y):
            return Pos((xa + xb) / 2, y, mz) * Rot(0, 90, 0) * Cylinder(r, xb - xa)
        enc = seg(mx0, mx0 + 11.0, mr - 0.3)
        enc = _fillet_try(enc, enc.faces().sort_by(Axis.X)[0].edges(), [1.5, 1.0])
        encoders.append(enc)
        can = seg(mx0 + 11.0, mx0 + 43.0, mr)
        can = _fillet_try(can, can.edges(), [0.8, 0.5])
        cans.append(can)
        gb = seg(mx0 + 43.0, mx1, mr - 0.2)
        gb -= Pos(mx0 + 52.0, y, mz) * Rot(0, 90, 0) * (Cylinder(mr + 1, 1.0) - Cylinder(mr - 0.9, 2.0))
        gb = _fillet_try(gb, gb.faces().sort_by(Axis.X)[-1].edges(), [1.2, 0.8])
        gearboxes.append(gb)
        shafts.append(seg(mx1, mx1 + P["shaft_l"], P["shaft_d"] / 2) + seg(mx1, mx1 + 2.5, 5.5))
    add("Gearmotor encoder caps", _union(encoders), C_DARK, "plastic", 3, "internal", (0, 0, 50))
    add("Gearmotor cans", _union(cans), C_METAL, "metal", 3, "internal", (0, 0, 50))
    add("Gearboxes", _union(gearboxes), C_METAL_DK, "metal", 3, "internal", (0, 0, 50))
    add("Output shafts", _union(shafts), C_METAL, "metal", 3, "internal", (0, 0, 50))

    sx, swd = D["spool_x"], P["spool_w"]
    fr, cr = P["spool_flange_d"] / 2, P["spool_core_d"] / 2
    spools, wraps, idl, idl_sh, runs = [], [], [], [], []
    for sgn in (1, -1):
        y = sgn * P["motor_y"]
        s = Pos(sx, y, mz) * Rot(0, 90, 0) * Cylinder(cr, swd)
        for xf in (sx - swd / 2 + 0.75, sx, sx + swd / 2 - 0.75):
            fl = Pos(xf, y, mz) * Rot(0, 90, 0) * Cylinder(fr, 1.5)
            fl = _fillet_try(fl, fl.edges(), [0.5, 0.3])
            s += fl
        s -= Pos(sx, y, mz) * Rot(0, 90, 0) * Cylinder(P["shaft_d"] / 2, swd + 2)
        spools.append(s)
        for gx in (sx - swd / 4, sx + swd / 4):
            wraps.append(Pos(gx, y, mz) * Rot(0, 90, 0) * (Cylinder(cr + 1.6, 3.6) - Cylinder(cr - 0.2, 4.0)))
        for gx, gz in ((sx - swd / 4, mz + re_), (sx + swd / 4, mz - re_)):
            ic = (gx + P["idler_d"] / 2, sgn * (31.0 - P["idler_d"] / 2), gz)
            ring = Pos(*ic) * (Cylinder(P["idler_d"] / 2, P["idler_w"]) - Cylinder(P["idler_d"] / 2 - 1.2, P["idler_w"] + 1))
            idl.append(ring + Pos(*ic) * Cylinder(1.5, P["idler_w"] + 4.0))
            idl_sh.append(Pos(*ic) * (Cylinder(P["idler_d"] / 2 - 1.2, P["idler_w"] - 0.4) - Cylinder(1.6, P["idler_w"])))
            yo = sgn * 31.0
            pts = [(gx, y, gz), (gx, sgn * (31.0 - P["idler_d"] / 2), gz),
                   (gx + P["idler_d"] / 2 * (1 - 0.7071), sgn * (31.0 - P["idler_d"] / 2 * (1 - 0.7071)), gz),
                   (gx + P["idler_d"] / 2, yo, gz), (ax0 + 6.0, yo, gz)]
            runs.append(_polyline_tube(pts, TENDON_R))
    add("Spools (PA12)", _union(spools), C_SPOOL, "plastic", 4, "internal", (28, 0, 50))
    add("Tendon windings", _union(wraps), C_TENDON, "plastic", 16, "internal", (28, 0, 50))
    add("Idler bearings (4)", _union(idl), C_METAL, "metal", 20, "internal", (28, 0, 72))
    add("Idler bearing shields", _union(idl_sh), C_DARK, "plastic", 20, "internal", (28, 0, 72))
    add("Tendon runs in the pack", _union(runs), C_TENDON, "plastic", 16, "internal", (28, 0, 50))

    # ================= cells (BOM 5), electronics (BOM 6, 7, 18) =================
    cz = fz + 1.0 + P["cell_d"] / 2
    cl, crr = P["cell_l"], P["cell_d"] / 2
    wrapc, capc = [], []
    for cxp in P["cell_x"]:
        w_ = Pos(cxp, 0, cz) * Rot(90, 0, 0) * Cylinder(crr, cl - 1.4)
        w_ = _fillet_try(w_, w_.edges(), [0.6, 0.3])
        wrapc.append(w_)
        for sy in (1, -1):
            capc.append(Pos(cxp, sy * (cl / 2 - 0.35), cz) * Rot(90, 0, 0) * Cylinder(crr - 0.8, 0.7))
    add("18650 cells (2)", _union(wrapc), C_CELL, "painted", 5, "internal", (0, 0, 32))
    add("Cell end caps", _union(capc), C_METAL, "metal", 5, "internal", (0, 0, 32))
    rx = x0 + wl + 1.0
    pcb_t = 1.2
    tray = _prism(36.0, W - 6, 2.0, tray_z - 1.5, 1.5, x=x0 + wl + 18.5)
    add("Electronics tray", tray, C_DARK, "plastic", 19, "internal", (0, 0, 62))
    bms = _prism(14, 40, 1.0, tray_z, pcb_t, x=rx + 24, y=-14)
    bms_c = Pos(rx + 24, -24, tray_z + pcb_t + 0.6) * Box(5, 5, 1.2) + Pos(rx + 24, -8, tray_z + pcb_t + 0.5) * Box(4, 6, 1.0)
    add("2S protection board", bms, C_PCB_GREEN, "plastic", 5, "internal", (0, 0, 62))
    ctrl = _prism(18, 21, 1.0, tray_z, pcb_t, x=rx + 9, y=-24)
    ctrl_can = Pos(rx + 9, -22, tray_z + pcb_t + 1.0) * Box(12, 12, 2.0)
    add("Controller board (ESP32-S3)", ctrl, C_PCB_BLACK, "plastic", 6, "internal", (0, 0, 76))
    drv = _prism(15, 20, 1.0, tray_z, pcb_t, x=rx + 7.5, y=0) + _prism(15, 20, 1.0, tray_z, pcb_t, x=rx + 24.5, y=20)
    drv_c = Pos(rx + 7.5, 0, tray_z + pcb_t + 0.5) * Box(5, 5, 1.0) + Pos(rx + 24.5, 20, tray_z + pcb_t + 0.5) * Box(5, 5, 1.0)
    add("Motor driver boards (2)", drv, C_PCB_GREEN, "plastic", 7, "internal", (0, 0, 76))
    chg = _prism(15, 20, 1.0, tray_z, pcb_t, x=rx + 7.5, y=24)
    chg_c = Pos(x0 + 1 + 2.5, 24, usb_z) * Box(7.0, 9.0, 3.2)
    add("USB-C charger board", chg, C_PCB_BLUE, "plastic", 18, "internal", (0, 0, 76))
    add("Board components", _union([bms_c, ctrl_can, drv_c]), C_PCB_BLACK, "plastic", 6, "internal", (0, 0, 76))
    add("USB-C receptacle", chg_c, C_METAL, "metal", 18, "internal", (0, 0, 76))

    # ================= hand side, fitted to the clay hand =================
    fingers, thumb = _clay_fingers()
    GT, pt = P["glove_t"], P["plate_t"]

    # base glove (BOM 12): knit shell over the palm from the wrist to the knuckles
    def palm_band(off, xa, xb):
        arm_part = _ring_offset_loft(ARM_SECS, off, max(xa, -250), min(xb, 0.0)) if xa < 0 else None
        palm_part = _ring_offset_loft(PALM_SECS, off, max(xa, 0.0), xb) if xb > 0 else None
        return _union([s for s in (arm_part, palm_part) if s is not None])

    glove = palm_band(GT, -14.0, 84.0) - palm_band(0.0, -16.0, 86.0)
    t0 = thumb["pts"][0]
    t_dir = (thumb["pts"][1] - t0).normalized()
    glove -= Solid.make_cylinder(12.0, 40.0, Plane(origin=t0 - t_dir * 12.0, z_dir=t_dir))
    add("Base glove (knit)", glove, C_GLOVE, "fabric", 12, "shell", (80, 0, 0))
    hem = palm_band(GT + 0.8, -14.0, -6.0) - palm_band(GT - 0.2, -16.0, -4.0)
    bind = palm_band(GT + 0.6, 79.0, 84.0) - palm_band(GT - 0.2, 77.0, 86.0)
    add("Glove cuff and binding", hem + bind, C_KNIT, "fabric", 12, "shell", (80, 0, 0))

    # dorsal (BOM 13) and palmar (BOM 14) plates follow the glove surface
    def plate(xm, lx, zsign):
        shellp = palm_band(GT + pt, xm - lx / 2 - 2, xm + lx / 2 + 2) - palm_band(GT - 0.05, xm - lx / 2 - 3, xm + lx / 2 + 3)
        region = Pos(xm, 0, 0) * extrude(RectangleRounded(lx, 60.0, 8.0), amount=60.0 * zsign)
        return shellp & region

    dplate = plate(38.0, 50.0, 1)
    pplate = plate(24.0, 34.0, -1)

    def surf_z(x, y, zsign, off):
        """Height of the offset palm surface above (or below) the axis at (x, y), by ray cast on the band."""
        band = palm_band(off, x - 0.5, x + 0.5)
        probe = band & Pos(x, y, zsign * 40) * Box(0.6, 0.6, 80)
        bb = probe.bounding_box()
        return bb.max.Z if zsign > 0 else bb.min.Z

    ext_end_y = [21.0, 7.0, -7.0, -21.0]
    so = P["sheath_od"] / 2
    stops_d, stops_p, sheaths, ferrules, tend = [], [], [], [], []
    ax_end = D["anchor_front"]
    order = [(1, 4.0), (1, -4.0), (-1, 4.0), (-1, -4.0)]
    zu_, zl_ = D["line_z"]
    for k in range(4):
        side = 1 if k < 2 else -1
        j = k % 2
        ya = order[k][0] * by + order[k][1]
        # extensor sheath: anchor block front face to the dorsal plate stop
        zt = surf_z(15.0, ext_end_y[k], 1, GT + pt)
        e_end = (15.0, ext_end_y[k], zt + so)
        e_pts = [(ax_end, ya, zu_), (-8, ya * 0.7, 40), e_end]
        sheaths.append(_swept(e_pts, SHEATH_R, (1, 0, -0.2), (1, 0, -0.35)))
        st = Pos(19.0, ext_end_y[k], zt + so - 0.5) * Box(9.0, 6.5, 2 * so + 1.0)
        st = _fillet_try(st, _top_edges(st), [1.5, 1.0])
        stops_d.append(st & (palm_band(GT + pt + 20, 10, 30) - palm_band(GT + pt - 1.0, 10, 30)))
        # flexor sheath: around the side of the wrist to the palmar plate stop
        zb = surf_z(14.0, side * (24.0 + 4 * j), -1, GT + pt)
        f_end = (14.0, side * (24.0 + 4 * j), zb - so)
        f_pts = [(ax_end, ya, zl_), (ax_end + 5, side * (40.5 + 2 * j), 17),
                 (3, side * (37.0 + 2 * j), -15), f_end]
        sheaths.append(_swept(f_pts, SHEATH_R, (1, 0, -0.3), (1, 0, 0.3)))
        sp = Pos(18.0, f_end[1], zb - so + 0.5) * Box(8.0, 6.5, 2 * so + 1.0)
        sp = _fillet_try(sp, _bottom_edges(sp), [1.5, 1.0])
        stops_p.append(sp & (palm_band(GT + pt + 20, 8, 28) - palm_band(GT + pt - 1.0, 8, 28)))
        for (a, b) in ((e_pts[0], (1, 0, 0)), (f_pts[0], (1, 0, 0))):
            ferrules.append(Solid.make_cylinder(so + 0.5, 6.0, Plane(origin=_v(a) - Vector(1, 0, 0), z_dir=_v(b))))
        for endp in (e_end, f_end):
            ferrules.append(Solid.make_cylinder(so + 0.5, 5.0, Plane(origin=_v(endp) - Vector(4.5, 0, 0), z_dir=(1, 0, 0))))

    dplate = _union([dplate] + stops_d)
    pplate = _union([pplate] + stops_p)
    add("Dorsal plate (TPU)", dplate, C_PLATE, "rubber", 13, "shell", (80, 0, 34))
    add("Palmar plate (TPU)", pplate, C_PLATE, "rubber", 14, "shell", (80, 0, -34))
    add("Bowden sheaths (8)", _union(sheaths), C_SHEATH, "rubber", 11, "shell", (112, 0, 0))
    add("Sheath ferrules (16)", _union(ferrules), C_METAL, "metal", 11, "shell", (112, 0, 0))

    # finger cuffs (BOM 15), thimbles (BOM 21) and tendons (BOM 16) on the clay fingers
    cl_t, cu_t, th_t = P["cuff_liner_t"], P["cuff_t"], P["thimble_t"]
    cuffs, liners, thimbles, eyelets, tendons = [], [], [], [], []
    for i, (fg, f) in enumerate(zip(D["finger_geom"], fingers)):
        tops, bots = [], []
        spots = [(0, None, P["guide_cuff_w"], cu_t), (1, None, fg["anchor_w"], cu_t)]
        dist_len = (f["pts"][3] - f["pts"][2]).length
        for seg_i, _, w, wall in spots:
            p, d, r, Ls = _on_seg(f, seg_i, (f["pts"][seg_i + 1] - f["pts"][seg_i]).length / 2)
            pl = _frame(p, d)
            rin = r + 0.3
            ring = _saddle(pl, rin + cl_t, rin + cl_t + wall, w, D["saddle_half_deg"], P["side_band_t"])
            cuffs.append(ring)
            liners.append(_tube(pl, rin, rin + cl_t, w - 0.6))
            ro = rin + cl_t + wall
            ey = pl.location * (Pos(ro + 0.6, 0, 0) * Box(2.6, 4.5, w * 0.6))
            ey -= Solid.make_cylinder(TENDON_R + 0.3, w + 4, Plane(origin=p + pl.x_dir * (ro + 1.2) - d * (w / 2 + 2), z_dir=d))
            eb = pl.location * (Pos(-(ro + 0.6), 0, 0) * Box(2.6, 4.5, w * 0.6))
            eb -= Solid.make_cylinder(TENDON_R + 0.3, w + 4, Plane(origin=p - pl.x_dir * (ro + 1.2) - d * (w / 2 + 2), z_dir=d))
            eyelets += [ey, eb]
            tops.append(p + pl.x_dir * (ro + 1.2))
            bots.append(p - pl.x_dir * (ro + 1.2))
        tw = min(fg["thimble_w"], dist_len - 0.5)
        p, d, r, Ls = _on_seg(f, 2, dist_len - tw / 2)
        pl = _frame(p, d)
        rin = r + 0.3
        th = _saddle(pl, rin + cl_t, rin + cl_t + th_t, tw, D["saddle_half_deg"], P["side_band_t"])
        thimbles.append(th)
        liners.append(_tube(pl, rin, rin + cl_t, tw - 0.6))
        ro = rin + cl_t + th_t
        tt = p + pl.x_dir * (ro + 0.9)
        tabk = pl.location * (Pos(ro + 0.3, 0, 0) * Box(1.8, 5.0, 5.0))
        eyelets.append(tabk)
        # extensor: dorsal plate front, over the knuckle, through both cuff eyelets to the thimble
        zp = surf_z(40.0, ext_end_y[i] * 1.1, 1, GT + pt)
        e = [(15.0, ext_end_y[i], zp + 1.0), (40.0, ext_end_y[i] * 1.1, zp + TENDON_R + 0.2),
             (74.0, (ext_end_y[i] * 1.1 + fg["y"]) / 2, surf_z(74.0, ext_end_y[i] * 1.1, 1, GT) + TENDON_R + 0.4)]
        e += [tuple(v) for v in tops] + [tuple(tt)]
        tendons.append(_polyline_tube(e, TENDON_R))
        zq = surf_z(30.0, fg["y"] * 0.9, -1, GT + pt)
        fpts = [(14.0, fg["y"] * 0.85, zq - 1.0), (30.0, fg["y"] * 0.9, zq - TENDON_R - 0.2)]
        fpts += [tuple(v) for v in bots]
        tendons.append(_polyline_tube(fpts, TENDON_R))
    add("Finger cuffs (8, TPU)", _union(cuffs), C_CUFF, "rubber", 15, "shell", (125, 0, 0))
    add("Cuff and thimble liners", _union(liners), C_FOAM, "rubber", 15, "shell", (125, 0, 0))
    add("Tendon eyelets and tip tabs", _union(eyelets), C_DARK, "plastic", 15, "shell", (125, 0, 0))
    add("Fingertip thimbles (4, TPU)", _union(thimbles), C_THIMBLE, "rubber", 21, "shell", (160, 0, 0))
    add("Tendons (8, UHMWPE)", _union(tendons), C_TENDON, "plastic", 16, "shell", (100, 0, 48))

    # thumb spacer (BOM 17): ring on the thumb and a web block toward the palm
    s_ring = 34.0
    seg0 = (thumb["pts"][1] - thumb["pts"][0]).length
    p, d, r, _ = _on_seg(thumb, 1, s_ring - seg0)
    pl = _frame(p, d)
    ring = _tube(pl, r + 0.3, r + 2.8, 12.0)
    ring = _fillet_try(ring, ring.edges(), [0.8, 0.5])
    inward = Vector(0, -1, 0.3).normalized()
    wb_c = p + inward * (r + 2.8 + 3.0)
    web = Plane(origin=wb_c, x_dir=d, z_dir=inward).location * Box(14.0, 12.0, 8.0)
    web = _fillet_try(web, web.edges(), [2.0, 1.2, 0.6])
    web -= Solid.make_cylinder(r + 0.3, 40.0, Plane(origin=p - d * 20.0, z_dir=d))
    add("Thumb spacer (TPU)", ring + web, C_GRAPHITE, "rubber", 17, "shell", (80, 45, -20))

    # ================= context: shared clay forearm and hand =================
    from context_parts import forearm_hand
    arm = forearm_hand(side="left", pose="flat")      # thumb at +Y, palm down, wrist at the origin
    add("Forearm and hand (clay)", arm, C_CLAY, "clay", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:38s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:7.2f} cm3")
