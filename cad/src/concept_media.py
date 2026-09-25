"""FlexHand concept media from the TRL 3 parametric model.

Run from the repo root:  python cad/src/concept_media.py
Geometry comes from cad/src/model.py; not for fabrication.

The model is built as a right forearm and hand, palm down (X from elbow to fingertips, Z dorsal,
+Y thumb side). For the media it is mirrored about the XZ plane (a left hand) so the thumb side
and the radial flexor sheaths face the standard camera. The grey forearm and hand are context
parts shown only in the hero render and the isometric view of the blueprint.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(ROOT / "cad" / "src"))
sys.path.insert(0, str(ROOT / "docs" / "04-calcs"))
from build123d import Plane, mirror  # noqa: E402
from concept import Part, render_all  # noqa: E402
import model  # noqa: E402

M = model.build_parts()
P = M["parts"]

SPEC = [  # (key, label, color, exploded offset in right-hand coordinates)
    ("forearm_cuff", "Forearm cuff", "#4B5563", (0, 0, -45)),
    ("pack_base", "Pack base", "#D1D5DB", (0, 0, 0)),
    ("gearmotors", "Gearmotor (2)", "#6B7280", (0, 0, 50)),
    ("spools", "Spool (2)", "#D4A017", (30, 0, 50)),
    ("cells", "Li-ion pack, 2S", "#C2410C", (0, 0, 35)),
    ("controller", "Controller", "#0F766E", (0, 0, 70)),
    ("drivers", "Motor drivers (2)", "#115E59", (0, 0, 70)),
    ("pack_lid", "Pack lid", "#E5E7EB", (0, 0, 115)),
    ("estop", "Emergency stop", "#DC2626", (0, 0, 140)),
    ("anchor_block", "Sheath anchor block", "#0E7490", (30, 0, 20)),
    ("sheaths", "Bowden sheaths (8)", "#1F2937", (0, 0, 0)),
    ("glove", "Base glove", "#93C5FD", (0, 0, 0)),
    ("dorsal_plate", "Dorsal plate", "#374151", (0, 0, 30)),
    ("palmar_plate", "Palmar plate", "#374151", (0, 0, -35)),
    ("finger_cuffs", "Finger cuffs (8)", "#14B8A6", (45, 0, 0)),
    ("tendons", "Tendons (8)", "#B45309", (45, 0, 40)),
    ("thumb_spacer", "Thumb spacer", "#A78BFA", (0, 35, -20)),
    ("charger", "USB-C charger", "#7C3AED", (0, 0, 70)),
    ("idlers", "Idler bearings (4)", "#9CA3AF", (30, 0, 75)),
]

parts = [Part(label, mirror(P[k], Plane.XZ), color, model.BOM_LINE[k], (e[0], -e[1], e[2]))
         for k, label, color, e in SPEC]
context = [Part("Forearm and hand", mirror(M["context"], Plane.XZ), "#C8CDD3")]

if __name__ == "__main__":
    import sizing  # noqa: E402  (numbers on the sheet come from FXH-CAL-001)
    R = sizing.compute()
    render_all(
        parts, project="FlexHand", title="Tendon-driven finger exoskeleton concept", dwg_no="FXH-DWG-010",
        key_figures=["2 gearmotors drive 4 fingers; thumb held passively",
                     f"30 N extensor tendon force per finger; {R['T_peak']:.2f} N m peak at the spool",
                     f"About {R['cycles_per_h']:.0f} cycles per hour at design load (FXH-CAL-001)",
                     f"About {R['sessions']:.1f} sessions of 60 min per 18 Wh charge",
                     f"Pack about {R['m_pack']:.0f} g, hand parts about {R['m_hand']:.0f} g",
                     f"About ${R['bom_total']:.0f} in parts (BOM, indicative)"],
        scale_figure=False, context=context,
        # the cutaway shows the motor pack only; the hand-side parts have nothing inside
        cut_exclude=("Forearm cuff", "Bowden sheaths (8)", "Base glove", "Dorsal plate", "Palmar plate",
                     "Finger cuffs (8)", "Tendons (8)", "Thumb spacer"),
        flow={"title": "energy per 60 min session at design load (Wh, estimates from FXH-CAL-001)", "unit": "Wh",
              "stages": [("2S Li-ion pack", round(R["E_session_Wh"], 2)),
                         ("Motors (electrical)", round(R["E_motor_Wh"], 2)),
                         ("Spool shafts", round(R["E_shaft_Wh"], 2)),
                         ("Finger joints", round(R["E_finger_Wh"], 2))],
              "losses": [(0, "Controller and drivers", round(R["E_ctrl_Wh"], 2)),
                         (1, "Motor and gearbox", round(R["E_motor_Wh"] - R["E_shaft_Wh"], 2)),
                         (2, "Sheath and idler friction", round(R["E_shaft_Wh"] - R["E_finger_Wh"], 2))]},
    )
    for f in ("_views", "_views_fig"):
        shutil.rmtree(ROOT / "media" / f, ignore_errors=True)
    print("Media written to media/")
