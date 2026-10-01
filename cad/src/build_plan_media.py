"""FlexHand prototype build plan pictures (FXH-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps|wiring ...]
A single picture can be drawn with, for example, `sheets 105` or `steps 3` or `joints 7`.
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/FXH-DWG-101 to 116        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level wiring with wire sizes (matplotlib)
The pictures show the right-hand device; a left-hand device is its mirror image.
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
import model  # noqa: E402
import svg_patch  # noqa: E402,F401  (skips degenerate SVG arcs)

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
M = model.build_parts()
C = M["c"]
D = M["d"]
CTX = M["context"]

COL = {"base": "#9CA3AF", "anchor": "#0E7490", "shell": "#4B5563", "liner": "#FBBF24", "strap": "#1F2937",
       "motor": "#6B7280", "spool": "#D4A017", "idler": "#94A3B8", "balance": "#F59E0B", "coupling": "#B91C1C",
       "cell": "#C2410C", "board": "#16A34A", "ctrl": "#0F766E", "tray": "#A3A3A3", "reg": "#7C3AED",
       "lid": "#E5E7EB", "estop": "#DC2626", "glove": "#93C5FD", "plate": "#374151", "cuff": "#14B8A6",
       "thimble": "#2DD4BF", "spacer": "#A78BFA", "sheath": "#111827", "tendon": "#B45309", "puck": "#BE185D",
       "gate": "#EA580C", "cover": "#155E75", "fix": "#111827", "insert": "#B45309", "hand": "#D6D3D1"}


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def S(*ks):
    return model._fuse([C[k] for k in ks])


def win(sh, x0, x1, y0, y1, z0, z1):
    return sh & model._box(x0, x1, y0, y1, z0, z1)


def hand(alpha=0.35):
    return part("Forearm and hand (for scale)", CTX, COL["hand"], alpha=alpha)


def handonly(alpha=0.3):
    return part("Hand form", win(CTX, -15, 200, -90, 90, -60, 60), COL["hand"], alpha=alpha)


# ----------------------------------------------------------------- named components, in build order
def made():
    return {
        "base": part("Pack base", C["pack_base"], COL["base"]),
        "anchor": part("Anchor block", C["anchor_body"], COL["anchor"]),
        "shell": part("Forearm cuff shell", C["cuff_shell"], COL["shell"]),
        "liner": part("Cuff liner", C["cuff_liner"], COL["liner"]),
        "straps": part("Straps (2)", C["straps"], COL["strap"]),
        "motors": part("Gearmotors (2)", C["gearmotors"], COL["motor"]),
        "spools": part("Spools (2)", C["spools"], COL["spool"]),
        "idlers": part("Idler bearings and pins (4)", S("idlers", "idler_pins"), COL["idler"]),
        "balance": part("Balance pulleys, springs, couplings", S("balance_pulleys", "balance_pins", "slack_springs", "couplings"), COL["balance"]),
        "cells": part("Cells (2)", C["cells"], COL["cell"]),
        "reg": part("5 V regulator", C["regulator"], COL["reg"]),
        "tray": part("Electronics tray", C["tray"], COL["tray"]),
        "boards": part("Controller, drivers, charger, BMS", S("controller", "drivers", "charger", "bms"), COL["board"]),
        "lid": part("Pack lid", C["pack_lid"], COL["lid"]),
        "estop": part("Emergency stop", C["estop"], COL["estop"]),
        "glove": part("Glove", C["glove"], COL["glove"]),
        "dplate": part("Dorsal plate", C["dorsal_plate"], COL["plate"]),
        "pplate": part("Palmar plate", C["palmar_plate"], COL["plate"]),
        "spacer": part("Thumb spacer", C["thumb_spacer"], COL["spacer"]),
        "cuffs": part("Finger cuffs (8)", S("finger_cuffs", "cuff_liners"), COL["cuff"]),
        "thimbles": part("Fingertip thimbles (4)", S("thimbles", "thimble_liners"), COL["thimble"]),
        "sheaths": part("Sheaths (8)", C["sheaths"], COL["sheath"]),
        "tendons": part("Tendons and stop beads (8)", S("tendons", "stop_beads"), COL["tendon"]),
        "pucks": part("Sheath pucks (4)", C["pucks"], COL["puck"]),
        "gate": part("Release plate", C["gate"], COL["gate"]),
        "cover": part("Cover", C["cover"], COL["cover"]),
    }


# ----------------------------------------------------------------- overview
def overview():
    Mk = made()
    off = {"base": (0, 0, 0), "anchor": (60, 0, 0), "shell": (0, 0, -110), "liner": (0, 0, -180),
           "straps": (0, 0, -250), "motors": (0, 0, 70), "spools": (25, 0, 70), "idlers": (35, 0, 110),
           "balance": (0, 0, 150), "cells": (0, 0, 110), "reg": (0, 0, 150), "tray": (0, 0, 160),
           "boards": (0, 0, 195), "lid": (0, 0, 240), "estop": (0, 0, 290),
           "glove": (160, 0, -60), "dplate": (160, 0, 0), "pplate": (160, 0, -130), "spacer": (60, -60, -160),
           "cuffs": (230, 0, -60), "thimbles": (280, 0, -60), "sheaths": (120, 0, -30), "tendons": (230, 0, -20),
           "pucks": (40, 0, 40), "gate": (40, 0, 80), "cover": (40, 0, 118)}
    order = ["base", "anchor", "shell", "liner", "straps", "motors", "spools", "idlers", "balance", "cells", "reg",
             "tray", "boards", "lid", "estop", "glove", "dplate", "pplate", "spacer", "cuffs", "thimbles",
             "sheaths", "tendons", "pucks", "gate", "cover"]
    parts = []
    for k in order:
        p = Mk[k]
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "FlexHand prototype: every component, pulled apart",
                       subtitle="Numbered in build order (right-hand device). Screws, inserts and pins are not numbered",
                       elev=24, azim=-60, size=(12, 8), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def coupling_detail():
    """One ball-detent breakaway coupling, drawn larger than in the model: a socket (on the pulley side)
    and a plug (on the tendon side), held together by two 2 mm balls that a spring-wire ring presses
    into a groove round the plug's stem."""
    b = model._B()
    r = D["coupling_d"] / 2
    sock = model._cyl_x(0, 6.0, 0, 0, r) - model._cyl_x(2.0, 7.0, 0, 0, 1.65) - model._cyl_x(-1, 3, 0, 0, 0.7)
    sock = sock - model._cyl_z(-4.0, 4.0, 4.0, 0, 1.03)                       # two ball holes, top and bottom
    sock = sock - (model._cyl_x(3.4, 4.6, 0, 0, r + 1) - model._cyl_x(3.3, 4.7, 0, 0, 3.0))   # ring groove
    plug = model._cyl_x(6.0, 10.0, 0, 0, r) + model._cyl_x(2.2, 6.0, 0, 0, 1.6)
    plug = plug - model._cyl_x(5.0, 11.0, 0, 0, 0.7)
    plug = plug - (model._cyl_x(3.4, 4.6, 0, 0, 1.7) - model._cyl_x(3.3, 4.7, 0, 0, 1.1))
    balls = b.Pos(4.0, 0, 2.1) * b.Sphere(1.0) + b.Pos(4.0, 0, -2.1) * b.Sphere(1.0)
    ring = model._cyl_x(3.6, 4.4, 0, 0, 3.4) - model._cyl_x(3.5, 4.5, 0, 0, 3.0)
    return sock, plug, balls + ring


def sheets(only=None):
    Mk = made()
    base = dict(project="FlexHand", date=DATE)
    out = []
    fg = D["finger_geom"]
    x0, x1 = D["pack_x"]
    ax0, ax1 = D["anchor_x"]

    def go(num, *a, **k):
        if only and str(num) not in only:
            return
        out.append(bv.component_sheet(*a, **k))

    go(101, Part("Pack base", C["pack_base"], COL["base"]), [Mk["shell"], Mk["anchor"], Mk["motors"], Mk["cells"]],
       dwg_no="FXH-DWG-101", title="FlexHand pack base: making sketch", material="PETG, 3D printed, 4 perimeters, 30 % infill",
       inset_view=(28, -60),
       notes=["Print open side up, 168 x 76 mm, 2 mm walls, 2.5 mm floor; supports only",
              "  under the three saddle ribs, which follow the cuff's curve.",
              "Inside, from the elbow end: two cell saddles, four tray posts, the stop",
              "  button well, the motor cradle, the 3 mm motor bulkhead, the idler",
              "  posts and shelves, then the front wall with eight exit and screw holes.",
              "Bulkhead: 8 mm shaft holes 13.5 mm each side of centre, 14 mm above the",
              "  floor; 3.4 mm holes 8.5 mm either side of each, countersunk at the front.",
              "Push in heat-set inserts (M3, 5 mm): six in the rib bosses from below,",
              "  four in the lid bosses from above.",
              "Fits: ribs sit on the cuff shell (six M3 screws); front wall carries the",
              "  anchor block (four M3 screws from inside); lid on the wall tops.",
              "Check: a motor slides into the cradle and its face sits flat on the",
              "  bulkhead; a 3 mm pin drops into each idler post."], **base)

    go(102, Part("Anchor block", C["anchor_body"], COL["anchor"]), [Mk["base"], Mk["gate"], Mk["cover"]],
       dwg_no="FXH-DWG-102", title="FlexHand anchor block: making sketch", material="PETG, 3D printed, 4 perimeters, 40 % infill",
       inset_view=(25, -35),
       notes=["Print standing on its back face (the face against the pack) so the four",
              "  channels print as upright tunnels; 53 long, 88 wide, 31 tall.",
              "Channels 15 wide x 7 tall, centred 31.25 mm each side of the centre line,",
              "  5.4 mm above and below the motor axis height; open at both ends.",
              "Lightening pocket underneath between the channels, open at the bottom.",
              "Inserts (M3, 5 mm): four in the back face (14 mm each side, 6 mm above",
              "  and below the axis) for the pack screws; four in the front face",
              "  (30 mm each side, 2.8 mm from the bottom and 2.5 mm from the top)",
              "  for the cover screws.",
              "Fits: back face flat on the pack front wall; channels line up with the",
              "  pack's exit holes. Release plate and cover go on the front face.",
              "Check: a 15 x 7 mm gauge slides the full length of every channel."], **base)

    go(103, Part("Forearm cuff shell", C["cuff_shell"], COL["shell"]), [Mk["base"], hand(1.0)],
       dwg_no="FXH-DWG-103", title="FlexHand forearm cuff shell: making sketch", material="PETG, 3D printed, 2 mm wall",
       inset_view=(20, -55),
       notes=["A half cone 174 mm long, 2 mm wall, inside radius 41 mm at the elbow end",
              "  and 35 mm at the wrist end (forearm plus the 4 mm liner); its edges",
              "  stop 8 mm below the forearm's centre line.",
              "Print on its back on tree supports; 12 mm holes on a grid every 17 mm",
              "  along and 25 degrees round (70 holes).",
              "Six 3.4 mm holes for the pack screws, 9 mm each side of the top line,",
              "  at 18.5, 86.5 and 154.5 mm from the elbow end, on the solid strips",
              "  between hole columns.",
              "Fits: pack ribs sit on its top; M3 button-head screws go up from inside",
              "  into the ribs' inserts; liner glued inside; straps go round outside.",
              "Check: sits on the forearm without rocking; the six screw holes line up",
              "  with the pack's rib bosses."], **base)

    go(104, Part("Cuff liner", C["cuff_liner"], COL["liner"]), [Mk["shell"]],
       dwg_no="FXH-DWG-104", title="FlexHand cuff liner: making sketch", material="EVA foam sheet 4 mm, self-adhesive back",
       inset_view=(-40, -150),
       notes=["Cut from 4 mm EVA foam: lay the shell on its side on the sheet and",
              "  trace inside it, rolling it over; the flat pattern is a curved band",
              "  174 mm wide. Cut 2 mm inside the line and check in the shell.",
              "Punch the 12 mm holes through the shell's holes once glued in place,",
              "  so they line up.",
              "Cut a 6.5 mm hole over each of the six screw heads so the foam lies flat.",
              "Fits: glued to the inside of the shell with its own adhesive back,",
              "  after the pack is screwed on (the screw heads sit in its holes).",
              "Check: no foam stands proud of the shell edges; no screw head can",
              "  be felt through the foam."], **base)

    sp = C["spools"] & model._box(-200, 0, 0, 100, 0, 100)
    go(105, Part("Spool", sp, COL["spool"]), [Mk["motors"], Mk["idlers"], Mk["base"]],
       dwg_no="FXH-DWG-105", title="FlexHand spool (make 2): making sketch", material="PA12, printed by a service (or PETG)",
       inset_view=(35, -40),
       notes=["Make two. 16 mm long: a 4 mm hub, then three 1.5 mm flanges of 14 mm",
              "  diameter with two 3.75 mm wide grooves on a 10 mm core between them.",
              "Bore: 4 mm D-shape to suit the motor shaft, through.",
              "Hub: drill 2.5 mm across and tap M3 for a set screw onto the shaft flat.",
              "Each groove: a 1 mm hole through the core near one flange to tie the",
              "  line: the rear groove for the extensor line, the front for the flexor.",
              "Fits: hub 0.5 mm in front of the bulkhead; set screw on the shaft flat.",
              "  The extensor line leaves the top of its groove and the flexor line",
              "  the bottom of its groove, both toward the side wall, to the idlers.",
              "Check: flanges run true; the spool slides on the shaft without play."], **base)

    sock, plug, ball = coupling_detail()
    go(106, Part("Breakaway couplings", C["couplings"], COL["coupling"]), [part("Pulleys and springs", S("balance_pulleys", "balance_pins", "slack_springs"), COL["balance"]), Mk["pucks"], Mk["gate"]],
       dwg_no="FXH-DWG-106", title="FlexHand breakaway coupling (make 8): making sketch",
       material="PA12 print service (or brass, turned); 2 mm steel balls; 0.4 mm spring wire",
       view_shape=sock + plug + ball, inset_view=(60, -60),
       notes=["Make eight. Each is 6.8 mm across and 10 mm long when joined.",
              "Socket (pulley side), 6 mm long: a 3.3 mm bore 4 mm deep from the",
              "  front, a 1.4 mm hole through the back for the pulley line, two",
              "  2.05 mm holes across it 4 mm from the back, and a groove 3 mm deep",
              "  round the outside over those holes.",
              "Plug (tendon side): a 6.8 mm head 4 mm long with a 1.4 mm hole for the",
              "  tendon, and a 3.2 mm stem 3.8 mm long with a groove round it.",
              "Two 2 mm steel balls sit in the holes; a ring of 0.4 mm spring wire in",
              "  the outside groove presses them into the stem's groove. The wire",
              "  sets the pull-out force: about 60 N, set and recorded at TRL 4.",
              "Fits: one on each finger line, just in front of its balance pulley.",
              "Check: the plug pulls out and clicks back by hand at the set force."], **base)

    go(107, Part("Electronics tray", C["tray"], COL["tray"]), [Mk["base"], Mk["cells"], Mk["boards"]],
       dwg_no="FXH-DWG-107", title="FlexHand electronics tray: making sketch", material="PETG, 3D printed, 2 mm, solid",
       inset_view=(40, -60),
       notes=["A flat plate 37.5 x 71 x 2 mm, printed flat.",
              "Four 2.2 mm holes, 4 mm in from each end and 34.5 mm each side of",
              "  the centre line, over the four tray posts in the pack base.",
              "Lay out the boards on top (stick them on with double-sided foam tape):",
              "  rear row, from the thumb side: charger (USB-C port to the rear wall),",
              "  controller, driver 1; front row: battery board, driver 2.",
              "Fits: rests on the four posts, 1 mm above the cells, with a 1 mm foam",
              "  pad between; four M2.2 self-tapping screws hold it and the cells.",
              "Check: the charger's USB-C port lines up with the rear wall opening."], **base)

    go(108, Part("Pack lid", C["pack_lid"], COL["lid"]), [Mk["base"], Mk["estop"]],
       dwg_no="FXH-DWG-108", title="FlexHand pack lid: making sketch", material="PETG, 3D printed, 2 mm, solid",
       inset_view=(35, -60),
       notes=["A plate 168 x 76 x 2 mm, printed flat, top face down.",
              "Stop button hole 19 mm, centred 51.2 mm from the elbow end on the",
              "  centre line.",
              "LED window 3 mm, over the controller's status LED.",
              "Four 3.4 mm screw holes over the lid bosses: 51 and 119 mm from the",
              "  elbow end, 32.5 mm each side of the centre line.",
              "Fits: on the wall tops, four M3 x 8 pan-head screws into the bosses.",
              "Check: the stop button's bezel sits flat and its nut tightens below."], **base)

    go(109, Part("Dorsal plate", C["dorsal_plate"], COL["plate"]), [Mk["glove"], Mk["sheaths"], Mk["tendons"]],
       dwg_no="FXH-DWG-109", title="FlexHand dorsal plate: making sketch", material="TPU 95A, 3D printed, 100 % infill",
       inset_view=(35, -60),
       notes=["Plate 50 x 60 x 2.5 mm with a stop block 8 x 56 x 6.5 mm standing on",
              "  its wrist edge; print plate side down.",
              "Block: four 5.2 mm seats 5 mm deep from the wrist face for the sheath",
              "  ends, with 1.6 mm tendon holes on through. Seats 24 and 8 mm to the",
              "  thumb side and 8 and 23 mm to the little-finger side of centre,",
              "  3.25 mm above the plate.",
              "Stitching holes 1.5 mm, 3 mm in from the edge, every 6 mm.",
              "Fits: stitched to the back of the glove over the hand, block toward",
              "  the wrist; the four extensor sheaths end in the seats.",
              "Check: a sheath ferrule pushes fully into each seat."], **base)

    go(110, Part("Palmar plate", C["palmar_plate"], COL["plate"]), [Mk["glove"], Mk["sheaths"], Mk["tendons"]],
       dwg_no="FXH-DWG-110", title="FlexHand palmar plate: making sketch", material="TPU 95A, 3D printed, 100 % infill",
       inset_view=(-35, -60),
       notes=["Plate 34 x 60 x 2.5 mm with a stop block 8 x 56 x 6.5 mm on its",
              "  wrist edge, on the outside face; print plate side down.",
              "Block: four 5.2 mm seats 5 mm deep for the flexor sheath ends, 1.6 mm",
              "  tendon holes on through, at the same spacing as the dorsal plate.",
              "Stitching holes 1.5 mm, 3 mm in from the edge, every 6 mm.",
              "Fits: stitched to the palm of the glove next to the wrist crease,",
              "  block toward the wrist; the four flexor sheaths end in the seats.",
              "Check: the palm still closes over a 40 mm tube with the plate on."], **base)

    go(111, Part("Thumb spacer", C["thumb_spacer"], COL["spacer"]), [Mk["glove"], Mk["pplate"], Mk["dplate"]],
       dwg_no="FXH-DWG-111", title="FlexHand thumb spacer: making sketch", material="TPU 95A, 3D printed, 100 % infill",
       inset_view=(15, 75),
       notes=["A ring 26 mm across, 12 mm long, sized to the thumb, joined to a web",
              "  block 14 x 9.5 x 14 mm whose inner face is shaped to the thumb.",
              "Print the ring axis upright with supports under the block.",
              "Four 1.5 mm stitching holes through the block's flat face.",
              "Fits: the block's flat face is stitched to the thumb side of the",
              "  glove at the web space; the ring slides over the thumb and holds it",
              "  out of the fingers' path.",
              "Check: the thumb sits in the ring without pressure marks after 10 min."], **base)

    i = 0
    f = fg[i]
    xa, xb = f["anchor_x"] - f["anchor_w"] / 2, f["anchor_x"] + f["anchor_w"] / 2
    one = C["finger_cuffs"] & model._box(xa - 1, xb + 1, f["y"] - 12.2, f["y"] + 15, -30, 30)
    oneL = C["cuff_liners"] & model._box(xa - 1, xb + 1, f["y"] - 12.2, f["y"] + 15, -30, 30)
    go(112, Part("Finger cuff", one + oneL, COL["cuff"]), [Mk["thimbles"], Mk["tendons"], Mk["glove"]],
       dwg_no="FXH-DWG-112", title="FlexHand finger cuffs (make 8): making sketch", material="TPU 95A, printed; 2 mm foam liner",
       view_shape=one + oneL, inset_view=(25, -50),
       notes=["Drawn: the index anchor cuff. Guide cuffs (proximal phalanges) are 12",
              "  wide; anchor cuffs (middle phalanges) are index 16.4, middle 18.6,",
              "  ring 17.0, little 12.2 wide. Bore = finger diameter (18, 18, 17, 15).",
              "Padded saddles top and bottom, 112 degrees each: 2.5 mm TPU over a",
              "  2 mm foam liner; 1 mm TPU side bands; a slit in one side band.",
              "Eyelet on top of every cuff and under every guide cuff: 2 mm hole.",
              "  Under each anchor cuff a tab with a 2 mm hole ends the flexor tendon.",
              "Print on end, no supports; glue the liners into the saddles.",
              "Fits: closed round the phalanx with a 6 mm hook-and-loop strip over",
              "  the slit, slit on the side away from the next finger where it can.",
              "Check: 3 mm clear of each joint crease; the finger bends fully."], **base)

    xa, xb = f["thimble_x"] - f["thimble_w"] / 2, f["thimble_x"] + f["thimble_w"] / 2
    th = (C["thimbles"] + C["thimble_liners"]) & model._box(xa - 1, xb + 1, f["y"] - 12.2, f["y"] + 15, -30, 30)
    go(113, Part("Fingertip thimble", th, COL["thimble"]), [Mk["cuffs"], Mk["tendons"], Mk["glove"]],
       dwg_no="FXH-DWG-113", title="FlexHand fingertip thimbles (make 4): making sketch", material="TPU 95A, printed; 2 mm foam liner",
       view_shape=th, inset_view=(25, -50),
       notes=["Drawn: the index thimble. Widths: index 17.0, middle 19.0, ring 17.5,",
              "  little 13.2 mm; bore = fingertip diameter.",
              "Open-tip band: padded saddles top and bottom (2 mm TPU over 2 mm",
              "  foam), 1 mm side bands, no slit; it slides on over the fingertip.",
              "Tab on top with a 2 mm hole where the extensor tendon ends.",
              "Print on end, no supports; glue the liners into the saddles.",
              "Fits: from 3 mm beyond the last finger crease to the tip.",
              "Check: slides on and off; the nail and tip stay uncovered."], **base)

    one_puck = C["pucks"] & model._box(-30, 0, 20, 45, D["line_z"][0] - 5, D["line_z"][0] + 5)
    go(114, Part("Sheath pucks", C["pucks"], COL["puck"]), [Mk["gate"], Mk["anchor"]],
       dwg_no="FXH-DWG-114", title="FlexHand sheath puck (make 4): making sketch", material="PETG, 3D printed, solid",
       view_shape=one_puck, inset_view=(25, 25),
       notes=["Make four. A block 5 long x 14 wide x 6 tall.",
              "Two 5.2 mm seats 3 mm deep from the front face, 8 mm apart, for the",
              "  sheath ferrules; 1.6 mm tendon holes on through to the back.",
              "Fits: sits in a pocket in the cover; its back bears on the release",
              "  plate, which carries the sheaths' push. When the plate is pulled",
              "  out the puck and both sheaths slide back into the channel and the",
              "  two tendons go slack.",
              "Check: the puck slides freely into a channel of the anchor block."], **base)

    go(115, Part("Release plate", C["gate"], COL["gate"]), [Mk["anchor"], Mk["pucks"], Mk["cover"]],
       dwg_no="FXH-DWG-115", title="FlexHand release plate: making sketch", material="PETG, 3D printed, 3 mm, solid; red",
       inset_view=(30, -30),
       notes=["A plate 3 mm thick, 20 mm tall and 84 mm wide, with an 18 mm tab on the",
              "  thumb side holding an 11 mm finger loop. Print it in red.",
              "Two slots 1.6 mm tall run in from the little-finger edge to 36 mm",
              "  past the centre, 5.4 mm above and below the motor axis height,",
              "  so the plate slides off all eight tendons at once.",
              "Fits: between the anchor block's front face and the cover, in the",
              "  3.4 mm gap the cover's four spacers leave; the pucks press it",
              "  against the block. Pull the loop toward the thumb side to free it.",
              "Check: with the cover screwed on, it slides out and back by hand."], **base)

    go(116, Part("Cover", C["cover"], COL["cover"]), [Mk["anchor"], Mk["gate"], Mk["pucks"], Mk["sheaths"]],
       dwg_no="FXH-DWG-116", title="FlexHand cover: making sketch", material="PETG, 3D printed, 40 % infill",
       inset_view=(25, -35),
       notes=["A plate 7.6 x 88 x 31 mm, printed front face down.",
              "Four pockets 15 x 7 x 5.6 mm in the back face, one in front of each",
              "  channel, for the pucks.",
              "Eight 4.5 mm holes through the 2 mm front wall for the sheaths, 4 mm",
              "  either side of each pocket's centre.",
              "Four 5 mm spacer bosses 3.4 mm long on the back face with 3.4 mm",
              "  holes, 30 mm each side of centre, top and bottom, for M3 x 16 screws.",
              "Fits: spacers on the anchor block's front face; the release plate",
              "  slides in the gap between them.",
              "Check: the release plate slides through the gap without catching."], **base)
    return out


# ----------------------------------------------------------------- joints
def joints(only=None):
    out = []
    mz = D["motor_z"]
    x0, x1 = D["pack_x"]
    ax0, ax1 = D["anchor_x"]
    fz = D["floor_z"]

    def J(n, parts, title, sub, **kw):
        if only and str(n) not in only:
            return
        out.append(bv.joint(parts, OUT / f"joint-{n:02d}.png", title, subtitle=sub, **kw))

    # 1 cuff shell, rib boss, insert and screw (cut on the screw line)
    xr = D["rib_x"][1]
    bx = (xr, xr + 12, -2, 22, 28, 50)
    J(1, [part("Forearm cuff shell", win(C["cuff_shell"], *bx), COL["shell"]),
          part("Cuff liner (hole over the screw head)", win(C["cuff_liner"], *bx), COL["liner"]),
          part("Pack base rib and boss", win(C["pack_base"], *bx), COL["base"]),
          part("Heat-set insert", win(C["inserts"], *bx), COL["insert"]),
          part("M3 x 8 button-head screw", win(C["cuff_screws"], *bx), COL["fix"]),
          part("Forearm", win(CTX, *bx), COL["hand"])],
      "Joint 1: pack rib on the cuff shell (middle rib, cut through one screw)",
      "Cut through the screw, seen from the elbow end. The screw goes up through the shell into an insert in the rib's boss", elev=6, azim=180, size=(8, 6))
    # 2 strap under the pack
    bx = (-215, -95, -50, 50, -45, 82)
    J(2, [part("Pack base", win(C["pack_base"], *bx), COL["base"]),
          part("Forearm cuff shell", win(C["cuff_shell"], *bx), COL["shell"]),
          part("Straps, through the gap under the pack", win(C["straps"], *bx), "#1D4ED8"),
          part("Forearm", win(CTX, *bx), COL["hand"], alpha=0.5)],
      "Joint 2: straps threaded under the pack, between its ribs",
      "Seen from the little-finger side and below. Each strap lies on the shell, then on the skin under the forearm",
      elev=-12, azim=-75, size=(9, 6))
    # 3 motor, bulkhead, spool (cut on the motor axis)
    bx = (-170, -78, D["motor_y"], 38, fz - 3, D["top_z"])
    J(3, [part("Pack base: cradle and bulkhead", win(C["pack_base"], *bx), COL["base"]),
          part("Gearmotor (cut in half)", win(C["gearmotors"], *bx), "#374151"),
          part("M3 x 6 countersunk screws", win(C["motor_screws"], *bx), COL["fix"]),
          part("Spool on the shaft", win(C["spools"], *bx), COL["spool"]),
          part("Idlers on their pins", win(S("idlers", "idler_pins"), *bx), COL["idler"])],
      "Joint 3: motor in its cradle and bulkhead, spool on the shaft (cut on the motor axis)",
      "Seen from the little-finger side. Two screws hold the gearbox face to the bulkhead", elev=20, azim=-80, size=(9, 6), cut=None)
    # 4 idlers (top view, lid off)
    bx = (-98.5, -70, 0, 35.9, fz - 3, D["top_z"] - 3)
    J(4, [part("Pack base: post, shelf, front wall", win(C["pack_base"], *bx), COL["base"]),
          part("Spool", win(C["spools"], *bx), COL["spool"]),
          part("Upper idler (extensor line)", win(C["idlers"], *bx) & model._box(-200, 0, 0, 50, D["line_z"][0] - 3, 100), COL["idler"]),
          part("Lower idler (flexor line)", win(C["idlers"], *bx) & model._box(-200, 0, 0, 50, -100, D["line_z"][1] + 3), "#64748B"),
          part("3 mm pins", win(C["idler_pins"], *bx), COL["fix"]),
          part("Anchor screw heads", win(C["anchor_screws"], *bx), "#57534E")],
      "Joint 4: the idlers turn each spool line forward to its exit hole (thumb side, lid off)",
      "Side wall cut away, seen from above and behind. Lower idler on a post from the floor, upper idler under a shelf from the wall",
      elev=55, azim=150, size=(9, 6))
    # 5 cells, saddles, tray (cut across)
    bx = (-238, -197, 20.0, 38, fz - 3, D["top_z"])
    J(5, [part("Pack base: saddles and tray posts", win(C["pack_base"], *bx), COL["base"]),
          part("Cells", win(C["cells"], *bx), COL["cell"]),
          part("Electronics tray", win(C["tray"], *bx), COL["tray"]),
          part("Boards", win(S("controller", "drivers", "charger", "bms"), *bx), COL["board"]),
          part("M2.2 tray screws", win(C["tray_screws"], *bx), COL["fix"])],
      "Joint 5: cells in their saddles, held down by the tray (cut through a saddle)",
      "Seen from the little-finger side and above. The tray rests on four posts, 1 mm over the cells",
      elev=22, azim=-70, size=(8, 6))
    # 6 anchor block on the pack front wall (cut on a screw)
    bx = (-90, -45, 14.0, 45, fz - 4, D["top_z"] + 1)
    J(6, [part("Pack front wall", win(C["pack_base"], *bx), COL["base"]),
          part("Anchor block", win(C["anchor_body"], *bx), COL["anchor"]),
          part("Inserts", win(C["inserts"], *bx), COL["insert"]),
          part("M3 x 8 cap screws from inside", win(C["anchor_screws"], *bx), COL["fix"]),
          part("Idlers", win(C["idlers"], *bx), COL["idler"])],
      "Joint 6: anchor block on the pack front wall (cut through two screws)",
      "Seen from the little-finger side and above. Each screw goes through the wall into an insert in the block",
      elev=25, azim=-60, size=(8, 6))
    # 7 channel contents, cut open from above at the extensor line
    lz = D["line_z"][0]
    bx = (-74, -2, 18, 47, fz - 4, lz + 0.01)
    J(7, [part("Anchor block (cut open)", win(C["anchor_body"], *bx), COL["anchor"]),
          part("Slack spring", win(C["slack_springs"], *bx), "#57534E"),
          part("Balance pulley", win(S("balance_pulleys", "balance_pins"), *bx), COL["balance"]),
          part("Breakaway couplings", win(C["couplings"], *bx), COL["coupling"]),
          part("Release plate", win(C["gate"], *bx), COL["gate"]),
          part("Sheath puck", win(C["pucks"], *bx), COL["puck"]),
          part("Cover", win(C["cover"], *bx), COL["cover"]),
          part("Sheaths", win(C["sheaths"], *bx), COL["sheath"]),
          part("Pack front wall", win(C["pack_base"], *bx), COL["base"])],
      "Joint 7: inside an extensor channel (thumb side, cut level with the line)",
      "Seen from above. Spool line, spring, pulley, one coupling per finger, release plate, puck, sheaths",
      elev=70, azim=-90, size=(9, 6))
    # 8 dorsal stop block with sheaths and tendons (cut through the index seat)
    ys = D["stop_y"][0]
    bx = (0, 40, ys - 1e-3, ys + 14, 14, 34)
    J(8, [part("Dorsal plate and stop block", win(C["dorsal_plate"], *bx), COL["plate"]),
          part("Glove", win(C["glove"], *bx), COL["glove"]),
          part("Extensor sheath", win(C["sheaths"], *bx), COL["sheath"]),
          part("Tendon and stop bead", win(S("tendons", "stop_beads"), *bx), COL["tendon"])],
      "Joint 8: an extensor sheath ends in the dorsal stop block (cut through the index seat)",
      "Seen from the little-finger side. The bead stops the tendon at the end of that finger's range",
      elev=8, azim=-90, size=(8, 6))
    # 9 cuffs and thimble on the index finger, tendons through the eyelets
    f = D["finger_geom"][0]
    bx = (95, 185, f["y"] - 13, f["y"] + 13, -30, 30)
    J(9, [part("Guide and anchor cuffs", win(S("finger_cuffs", "cuff_liners"), *bx), COL["cuff"]),
          part("Fingertip thimble", win(S("thimbles", "thimble_liners"), *bx), COL["thimble"]),
          part("Extensor (top) and flexor (bottom) tendons", win(C["tendons"], *bx), COL["tendon"]),
          part("Index finger", win(CTX, *bx), COL["hand"], alpha=0.6)],
      "Joint 9: cuffs and thimble on the index finger",
      "Seen from the thumb side. Extensor runs through two eyelets to the thimble tab; flexor ends at the anchor cuff",
      elev=12, azim=95, size=(9, 6))
    # 10 thumb spacer stitched to the glove
    P = model.PARAMS
    to, td, tl, tr = P["thumb_o"], P["thumb_d"], P["thumb_l"], P["thumb_r"]
    thumb = model._tube(to, tuple(to[i] + td[i] * tl for i in range(3)), tr)
    bx = (20, 75, 0, 75, -32, 5)
    J(10, [part("Glove (thumb side)", win(C["glove"], *bx), COL["glove"]),
           part("Thumb spacer: ring and stitched block", win(C["thumb_spacer"], *bx), COL["spacer"]),
           part("Palmar plate", win(C["palmar_plate"], *bx), COL["plate"])],
       "Joint 10: thumb spacer, its block stitched to the glove's thumb side",
       "Thumb not drawn; seen from the thumb side and below. The ring goes over the thumb and holds it out of the fingers' path",
       elev=-30, azim=80, size=(8, 6))
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    Mk = made()
    out = []

    def st(n, done, new, title, sub, **kw):
        if only and str(n) not in only:
            return
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    def mv(p, e):
        return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)

    ins = C["inserts"]
    rib_ins = part("Inserts in the rib bosses (6), from below", ins & model._box(-240, -72, -50, 50, 0, 60), COL["insert"])
    lid_ins = part("Inserts in the lid bosses (4), from above", ins & model._box(-240, -72, -50, 50, 60, 100), COL["insert"])
    anc_ins = part("Inserts in the anchor block (8)", ins & model._box(-72, 0, -50, 50, 0, 100), COL["insert"])
    st(1, [Mk["base"], Mk["anchor"]], [mv(rib_ins, (0, 0, -30)), mv(lid_ins, (0, 0, 30)), mv(anc_ins, (0, -60, 0))],
       "heat-set inserts into the pack base and anchor block",
       "Press each M3 insert in with a soldering iron at about 230 degrees C, square to the face. Seen from below",
       elev=-30, azim=-60, label_done=True)
    st(2, [Mk["base"]], [mv(Mk["anchor"], (50, 0, 0)), mv(part("M3 x 8 cap screws (4)", C["anchor_screws"], COL["fix"]), (-30, 0, 0))],
       "anchor block onto the pack front wall",
       "Four screws from inside the pack into the block's inserts; channels line up with the exit holes", elev=25, azim=-40)
    pk = [Mk["base"], Mk["anchor"]]
    st(3, pk, [mv(Mk["shell"], (0, 0, -60)), mv(part("M3 x 8 button-head screws (6)", C["cuff_screws"], COL["fix"]), (0, 0, -90))],
       "pack onto the cuff shell",
       "Six screws up through the shell into the rib inserts, snug; the shell's top must not crack", elev=-25, azim=-55, label_done=False)
    pk2 = pk + [Mk["shell"]]
    st(4, pk2, [mv(Mk["liner"], (0, 0, -60)), mv(Mk["straps"], (0, -80, 0))],
       "liner into the shell; straps under the pack",
       "Peel and press the liner in over the screw heads; thread each strap through the gap under the pack", elev=-25, azim=-55, label_done=False)
    pk3 = pk2 + [Mk["liner"], Mk["straps"]]
    st(5, pk3, [mv(Mk["motors"], (0, 0, 70)), mv(part("M3 x 6 countersunk screws (4)", C["motor_screws"], COL["fix"]), (40, 0, 0))],
       "gearmotors into the cradle and bulkhead",
       "Gearbox face flat on the bulkhead; two screws each from the front; a cable tie round each can", elev=55, azim=-125, label_done=False)
    pk4 = pk3 + [Mk["motors"]]
    st(6, pk4, [mv(Mk["spools"], (0, 0, 45))], "spools onto the motor shafts",
       "Hub 0.5 mm in front of the bulkhead; set screw tight on the shaft flat", elev=55, azim=-125, label_done=False)
    pk5 = pk4 + [Mk["spools"]]
    st(7, pk5, [mv(Mk["idlers"], (0, 0, 40))], "idler bearings on their pins",
       "Lower idlers on pins in the floor posts; upper idlers on pins pushed down through the wall shelves", elev=55, azim=-125, label_done=False)
    pk6 = pk5 + [Mk["idlers"]]
    st(8, pk6, [mv(Mk["balance"], (70, 0, 0))], "lines, springs, pulleys and couplings into the channels",
       "Tie each spool line, run it round its idler and out through its hole; slide its spring, pulley and couplings in from the front",
       elev=30, azim=35, label_done=False)
    pk7 = pk6 + [Mk["balance"]]
    st(9, pk7, [mv(Mk["cells"], (0, 0, 60)), mv(Mk["reg"], (0, 0, 60))], "cells and regulator",
       "Cells into their saddles (battery board not yet connected); regulator on foam tape beside the stop button well",
       elev=55, azim=-125, label_done=False)
    pk8 = pk7 + [Mk["cells"], Mk["reg"]]
    st(10, pk8, [mv(Mk["tray"], (0, 0, 50)), mv(Mk["boards"], (0, 0, 80))], "tray and boards; wiring",
       "Foam pad on the cells, tray on its posts with four screws, boards on foam tape, then wire as the wiring picture",
       elev=55, azim=-125, label_done=False)
    pk9 = pk8 + [Mk["tray"], Mk["boards"]]
    st(11, pk9, [mv(Mk["lid"], (0, 0, 60)), mv(Mk["estop"], (0, 0, 110))], "lid and emergency stop",
       "Stop button through the lid, nut below; lid on with four M3 x 8 pan-head screws", elev=30, azim=-55, label_done=False)
    st(12, [Mk["glove"]], [mv(Mk["dplate"], (0, 0, 40)), mv(Mk["pplate"], (0, 0, -40)), mv(Mk["spacer"], (0, 40, 0))],
       "plates and thumb spacer onto the glove",
       "Stitch each through its holes with strong polyester thread, glove on a hand form. Seen from the thumb side", context=[handonly()],
       elev=20, azim=55, label_done=False)
    hand_done = [Mk["glove"], Mk["dplate"], Mk["pplate"], Mk["spacer"]]
    st(13, hand_done, [mv(Mk["cuffs"], (0, 0, 40)), mv(Mk["thimbles"], (40, 0, 0)), mv(Mk["tendons"], (0, 0, 0))],
       "cuffs, thimbles and tendons",
       "Thread each tendon through its eyelets, tie it off at the thimble or anchor-cuff tab; crimp the stop beads loosely",
       context=[handonly()], elev=25, azim=-55, label_done=False)
    unit = pk9 + [Mk["lid"], Mk["estop"]]
    hand_full = hand_done + [Mk["cuffs"], Mk["thimbles"], Mk["tendons"]]
    st(14, unit + hand_full, [mv(Mk["sheaths"], (0, 0, 40))], "sheaths over the tendons",
       "Each sheath slides along its tendon, finger end into its stop block seat; extensors over the wrist, flexors down the side",
       context=[hand(0.3)], elev=25, azim=-60, label_done=False)
    st(15, unit + hand_full + [Mk["sheaths"]],
       [mv(Mk["pucks"], (40, 0, 0)), mv(Mk["gate"], (0, 100, 30)), mv(Mk["cover"], (70, 0, 0))],
       "pucks, release plate and cover",
       "Tie each tendon to its coupling plug; seat the sheath ends in the pucks; slide in the plate; screw on the cover",
       context=[hand(0.3)], elev=30, azim=-40, label_done=False)
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 7.2), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 72); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 70, "FlexHand prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 66.6, "Bought modules wired at block level; no circuit board is laid out. Stranded copper; heat shrink on every joint.",
            fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, "github.com/BoujeeEnjinia1701/flexhand", fontsize=7, color="#0F766E", ha="right", family="monospace")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.4, title, ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.3, sub, ha="center", va="top", fontsize=7.2, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7.2, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY = "#B91C1C", "#1D4ED8", "#6B7280"
    blk(3, 44, 15, 12, "USB-C charger", "2S, 5 V in;\ncharge only off the arm", "#7C3AED")
    blk(3, 22, 15, 12, "Cells (2)", "18650, 2S,\n7.4 V, 18 Wh", "#C2410C")
    blk(26, 32, 16, 13, "Battery board", "2S protection,\nfuse 3 A in\nthe pack lead", "#16A34A")
    blk(50, 44, 16, 12, "Stop button", "latching, normally\nclosed, motor supply", "#DC2626")
    blk(50, 20, 16, 12, "5 V regulator", "step-down,\n5 V 1 A", "#7C3AED")
    blk(74, 20, 16, 14, "Controller", "ESP32-S3 module;\nlimits, logging", "#0F766E")
    blk(74, 44, 16, 12, "Motor drivers (2)", "DRV8874, current\nsense output", "#16A34A")
    blk(100, 44, 16, 12, "Gearmotors (2)", "with encoders", "#6B7280")
    blk(100, 20, 16, 12, "Status LED", "under the lid\nwindow", "#0F766E")
    wire([(10.5, 44), (10.5, 38), (26, 38)], RED); lab(11.5, 41, "charge, 0.5 mm²", RED)
    wire([(18, 28), (22, 28), (22, 35), (26, 35)], RED); lab(19, 25.5, "cells, 0.75 mm²", RED)
    wire([(42, 40), (46, 40), (46, 50), (50, 50)], RED); lab(43, 47, "pack +, 0.75 mm²", RED)
    wire([(66, 50), (74, 50)], RED); lab(70, 53, "0.75 mm²", RED, "center")
    wire([(90, 50), (100, 50)], RED); lab(95, 53, "motor, 0.5 mm²", RED, "center")
    wire([(42, 36), (46, 36), (46, 26), (50, 26)], RED); lab(46.6, 31, "0.5 mm²", RED)
    wire([(66, 26), (74, 26)], RED); lab(70, 28.5, "5 V, 0.5 mm²", RED, "center")
    wire([(82, 34), (82, 44)], BLU); lab(82.6, 39, "PWM, current\nsense, 0.14 mm²", BLU)
    wire([(108, 44), (108, 38), (88, 38), (88, 34)], BLU); lab(96, 36, "encoders, 0.14 mm²", BLU)
    wire([(90, 26), (100, 26)], BLU); lab(95, 28.5, "0.14 mm²", BLU, "center")
    wire([(58, 44), (58, 41), (78, 41), (78, 34)], GRY, 1.2); lab(63, 41.8, "stop sense, 0.14 mm²", GRY)
    ax.text(3, 12.5, "Safety: battery board unconnected until safety stop S2; never charge while worn. The stop button opens the motor supply, not a",
            fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(3, 9.6, "firmware input. The controller only reads it so it can log the stop.", fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(3, 6.2, "Red: power. Blue: signal. Grey: sensing. All circuits are extra-low voltage: 8.4 V at most.", fontsize=7.2, color=MUT)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    what = [a for a in args if not a.isdigit()] or ["overview", "sheets", "joints", "steps", "wiring"]
    nums = [a for a in args if a.isdigit()] or None
    fns = {"overview": overview, "sheets": sheets, "joints": joints, "steps": steps, "wiring": wiring}
    for w in what:
        r = fns[w](nums) if w in ("sheets", "joints", "steps") else fns[w]()
        print(w, "->", r)
