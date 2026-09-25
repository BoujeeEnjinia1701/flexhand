"""FlexHand concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. Built as a right forearm and hand, palm down: X runs from elbow to fingertips,
Z is dorsal (up), +Y is the thumb (radial) side, wrist at X = 0. The finished model is mirrored
about the XZ plane (a left hand) so the thumb side and flexor sheaths face the standard camera.
Either hand is made by mirroring.
The forearm and hand are grey context parts shown only in the hero render.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cone, Cylinder, Sphere, Pos, Rot, Solid, Plane, Vector, mirror
from concept import Part, render_all

# ---------------- anthropometry (adult right hand, medium) ----------------
ARM_L = 270.0                 # modeled forearm length, elbow side to wrist
R_ELBOW, R_WRIST = 38.0, 29.0
PALM_L, PALM_W, PALM_T = 95.0, 80.0, 28.0
# finger: (lateral y, length, radius); index to little
FINGERS = [(29.0, 80.0, 9.0), (9.5, 88.0, 9.0), (-10.0, 82.0, 8.5), (-29.0, 65.0, 7.5)]
THUMB_O, THUMB_D, THUMB_L, THUMB_R = (15.0, 38.0, -6.0), (0.83, 0.5, -0.25), 62.0, 10.5

# ---------------- device parameters ----------------
PACK_X0, PACK_X1 = -205.0, -58.0   # motor pack along the forearm
PACK_W = 90.0
FLOOR, TOP = 42.0, 70.0            # pack cavity floor and top of base walls
MOTOR_R, MOTOR_L = 12.5, 64.0      # 25D gearmotor with encoder
MOTOR_X = (-120.0, -88.0)
SPOOL_R, SPOOL_W = 9.0, 14.0       # flange radius; 5 mm core radius
TUBE_R = 2.0                       # Bowden sheath outer radius
TENDON_R = 1.0                     # drawn oversize so it reads at this scale


def arm_r(x):
    """Forearm radius at x (x <= 0)."""
    return R_WRIST + (R_ELBOW - R_WRIST) * (-x) / ARM_L


def along_x(solid):
    return Rot(0, 90, 0) * solid


def tube(a, b, r):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def path(pts, r):
    s = None
    for a, b in zip(pts[:-1], pts[1:]):
        seg = tube(a, b, r)
        s = seg if s is None else s + seg
    for p in pts[1:-1]:
        s = s + Pos(*p) * Sphere(r)
    return s


def cone_x(x0, x1, r0, r1):
    """Truncated cone along X from x0 (radius r0) to x1 (radius r1)."""
    return Pos((x0 + x1) / 2, 0, 0) * along_x(Cone(r0, r1, x1 - x0))


# ---------------- context: forearm and hand ----------------
forearm = cone_x(-ARM_L, 0, R_ELBOW, R_WRIST)
palm = Pos(PALM_L / 2, 0, 0) * Box(PALM_L, PALM_W, PALM_T)
digits = None
for y, L, r in FINGERS:
    d = Pos(PALM_L + L / 2 - 4, y, 0) * along_x(Cylinder(r, L)) + Pos(PALM_L + L - 4, y, 0) * Sphere(r)
    digits = d if digits is None else digits + d
tx, ty, tz = THUMB_O
dx, dy, dz = THUMB_D
thumb_end = (tx + dx * THUMB_L, ty + dy * THUMB_L, tz + dz * THUMB_L)
thumb = tube(THUMB_O, thumb_end, THUMB_R) + Pos(*thumb_end) * Sphere(THUMB_R)
context = [Part("Forearm and hand", forearm + palm + digits + thumb, "#C8CDD3")]

# ---------------- 1 forearm cuff (half shell plus two straps) ----------------
cx0, cx1 = -212.0, -52.0
shell = cone_x(cx0, cx1, arm_r(cx0) + 4.0, arm_r(cx1) + 4.0) - cone_x(cx0 - 1, cx1 + 1, arm_r(cx0 - 1) + 0.5, arm_r(cx1 + 1) + 0.5)
cuff = shell & (Pos(0, 0, 60 - 8) * Box(1000, 200, 120))           # keep z > -8
for xs in (-190.0, -75.0):
    cuff = cuff + (cone_x(xs - 14, xs + 14, arm_r(xs - 14) + 2.0, arm_r(xs + 14) + 2.0)
                   - cone_x(xs - 15, xs + 15, arm_r(xs - 15) + 0.3, arm_r(xs + 15) + 0.3))
cuff_outer = cone_x(cx0 - 20, cx1 + 20, arm_r(cx0 - 20) + 4.0, arm_r(cx1 + 20) + 4.0)

# ---------------- 2 motor pack base ----------------
L = PACK_X1 - PACK_X0
base = Pos((PACK_X0 + PACK_X1) / 2, 0, (28 + TOP) / 2) * Box(L, PACK_W, TOP - 28)
base = base - Pos((PACK_X0 + PACK_X1) / 2, 0, (FLOOR + TOP + 2) / 2) * Box(L - 6, PACK_W - 6, TOP + 2 - FLOOR)
base = base - cuff_outer

# ---------------- 3 gearmotors, 4 spools (axis across the forearm) ----------------
mz = FLOOR + 1.5 + MOTOR_R
motors = spools = None
for mx in MOTOR_X:
    m = Pos(mx, -42 + 3 + MOTOR_L / 2, mz) * Rot(90, 0, 0) * Cylinder(MOTOR_R, MOTOR_L)
    motors = m if motors is None else motors + m
    sy = -39 + MOTOR_L + 2 + SPOOL_W / 2
    s = (Pos(mx, sy, mz) * Rot(90, 0, 0) * Cylinder(5.0, SPOOL_W)
         + Pos(mx, sy - SPOOL_W / 2 + 1, mz) * Rot(90, 0, 0) * Cylinder(SPOOL_R, 2)
         + Pos(mx, sy, mz) * Rot(90, 0, 0) * Cylinder(SPOOL_R, 1.5)
         + Pos(mx, sy + SPOOL_W / 2 - 1, mz) * Rot(90, 0, 0) * Cylinder(SPOOL_R, 2))
    spools = s if spools is None else spools + s

# ---------------- 5 Li-ion pack, 6 controller, 7 motor drivers ----------------
bz = FLOOR + 1 + 9
cells = (Pos(-167, -24, bz) * along_x(Cylinder(9, 65)) + Pos(-167, -4, bz) * along_x(Cylinder(9, 65))
         + Pos(-167, 16, FLOOR + 5) * Box(60, 14, 8))              # 2S BMS board beside the cells
controller = Pos(-185, -12, bz + 13) * Box(24, 21, 5)
drivers = Pos(-152, -14, bz + 12.5) * Box(26, 34, 4)

# ---------------- 8 lid, 9 emergency stop ----------------
lid = Pos((PACK_X0 + PACK_X1) / 2, 0, TOP + 2) * Box(L, PACK_W, 4)
estop = Pos(-182, 22, TOP + 4 + 5) * Cylinder(11, 10) + Pos(-182, 22, TOP + 4 + 1) * Cylinder(8, 2)

# ---------------- 10 sheath anchor and breakaway block ----------------
anchor = Pos(-53, 26, 54) * Box(10, 34, 24)

# ---------------- 11 Bowden sheaths ----------------
DORSAL_END_Y = [21.0, 7.0, -7.0, -21.0]
sheaths = None
for k in range(4):
    sy = 38 - 6 * k
    s = path([(-48, sy, 60), (-5, sy * 0.6, 40), (15, DORSAL_END_Y[k], 21)], TUBE_R)   # extensor side
    f = path([(-48, 40, 46 + 4 * k), (-16 + 5 * k, 38, -24), (10 + 8 * k, 26, -19)], TUBE_R)  # flexor side
    s = s + f
    sheaths = s if sheaths is None else sheaths + s

# ---------------- 12 base glove (fingerless sleeve over the palm) ----------------
GT = 2.5
glove = (Pos(PALM_L / 2 - 3, 0, 0) * Box(PALM_L + 4, PALM_W + 2 * GT, PALM_T + 2 * GT)
         - Pos(PALM_L / 2 - 3, 0, 0) * Box(PALM_L + 6, PALM_W, PALM_T))
gz = PALM_T / 2 + GT

# ---------------- 13 dorsal and 14 palmar anchor plates ----------------
dorsal_plate = Pos(42, 0, gz + 2) * Box(56, 64, 4)
palmar_plate = Pos(25, 4, -gz - 2) * Box(40, 58, 4)

# ---------------- 15 finger cuffs, 16 tendons ----------------
cuffs = tendons = None
for i, (y, Lf, r) in enumerate(FINGERS):
    xp, xm = PALM_L + 0.22 * Lf, PALM_L + 0.60 * Lf
    for xc in (xp, xm):
        c = Pos(xc, y, 0) * along_x(Cylinder(r + 2.5, 12) - Cylinder(r, 13))
        cuffs = c if cuffs is None else cuffs + c
    h = r + 2.5 + TENDON_R
    t = (path([(66, DORSAL_END_Y[i] * 1.2, gz + 4), (xp, y, h), (xm, y, h)], TENDON_R)
         + path([(43, y * 0.9, -gz - 4), (xp, y, -h), (xm, y, -h)], TENDON_R))
    tendons = t if tendons is None else tendons + t

# ---------------- 17 thumb abduction spacer ----------------
s_ring = 34.0
ring_c = (tx + dx * s_ring, ty + dy * s_ring, tz + dz * s_ring)
ring = Solid.make_cylinder(THUMB_R + 2.5, 12, Plane(origin=Vector(*ring_c) - Vector(*THUMB_D) * 6, z_dir=Vector(*THUMB_D)))
ring = ring - Solid.make_cylinder(THUMB_R, 14, Plane(origin=Vector(*ring_c) - Vector(*THUMB_D) * 7, z_dir=Vector(*THUMB_D)))
spacer = ring + Pos(40, 45.5, -8) * Box(14, 8, 12)

parts = [
    Part("Forearm cuff", cuff, "#4B5563", 1, (0, 0, -45)),
    Part("Pack base", base, "#D1D5DB", 2, (0, 0, 0)),
    Part("Gearmotor (2)", motors, "#6B7280", 3, (0, -30, 55)),
    Part("Spool (2)", spools, "#D4A017", 4, (0, 25, 55)),
    Part("Li-ion pack, 2S", cells, "#C2410C", 5, (0, 0, 45)),
    Part("Controller", controller, "#0F766E", 6, (0, 0, 95)),
    Part("Motor drivers (2)", drivers, "#115E59", 7, (0, 0, 75)),
    Part("Pack lid", lid, "#E5E7EB", 8, (0, 0, 125)),
    Part("Emergency stop", estop, "#DC2626", 9, (0, 0, 150)),
    Part("Sheath anchor block", anchor, "#0E7490", 10, (25, 30, 25)),
    Part("Bowden sheaths (8)", sheaths, "#1F2937", 11, (0, 0, 0)),
    Part("Base glove", glove, "#93C5FD", 12, (0, 0, 0)),
    Part("Dorsal plate", dorsal_plate, "#374151", 13, (0, 0, 30)),
    Part("Palmar plate", palmar_plate, "#374151", 14, (0, 0, -35)),
    Part("Finger cuffs (8)", cuffs, "#14B8A6", 15, (45, 0, 0)),
    Part("Tendons (8)", tendons, "#B45309", 16, (45, 0, 40)),
    Part("Thumb spacer", spacer, "#A78BFA", 17, (0, 35, -20)),
]

# mirror to a left hand so the thumb side faces the camera; flip Y in exploded offsets too
parts = [Part(p.name, mirror(p.shape, Plane.XZ), p.color, p.bom, (p.explode[0], -p.explode[1], p.explode[2]))
         for p in parts]
context = [Part(c.name, mirror(c.shape, Plane.XZ), c.color) for c in context]

if __name__ == "__main__":
    render_all(
        parts, project="FlexHand", title="Tendon-driven finger exoskeleton concept", dwg_no="FXH-DWG-010",
        key_figures=["2 gearmotors drive 4 fingers; thumb held passively",
                     "Target 30 N extensor tendon force per finger",
                     "About 6 cycles per min at design load (estimate)",
                     "About 3 sessions of 60 min per charge (estimate)",
                     "Pack about 510 g, hand parts about 90 g (estimate)",
                     "About $280 in parts (indicative)"],
        scale_figure=False, context=context,
        # the cutaway shows the motor pack only; the hand-side parts have nothing inside
        cut_exclude=("Forearm cuff", "Bowden sheaths (8)", "Base glove", "Dorsal plate", "Palmar plate",
                     "Finger cuffs (8)", "Tendons (8)", "Thumb spacer"),
        flow={"title": "energy per 60 min session at design load (Wh, all values estimates)", "unit": "Wh",
              "stages": [("2S Li-ion pack", 4.7), ("Motors (electrical)", 4.3), ("Spool shafts", 1.1),
                         ("Finger joints", 0.8)],
              "losses": [(0, "Controller and drivers", 0.4), (1, "Motor and gearbox", 3.2),
                         (2, "Bowden friction", 0.3)]},
    )
