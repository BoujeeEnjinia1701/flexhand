"""FlexHand sizing calculations (FXH-CAL-001 v0.3: decisions of FXH-DDR-002 and the constructable design of FXH-DDR-003).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md, tagged [A1], [B2] and so on.
Geometry comes from cad/src/model.py; costs come from bom/bom.csv; the budget from project.yaml.
First-principles estimates for a paper proof of concept (TRL 3). Not a test result.
"""
import csv
import sys
from math import exp, pi, radians, degrees
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))

# ---------------- assumptions (see Table 1 of the note) ----------------
F_DESIGN = 30.0          # N, extensor tendon force per finger at full extension (R2, D5)
F_START = 3.0            # N, per finger at the start of extension (friction, slack spring)
F_FLEX = 5.0             # N, per finger while flexing (extensor passive tone, slack spring, cuff friction)
FINGERS_PER_MOTOR = 2    # D2: one motor per finger pair
R_MCP, R_PIP = 10.0, 8.0         # mm, dorsal (extensor) moment arms
R_MCP_F, R_PIP_F = 11.0, 8.0     # mm, palmar (flexor) moment arms
ROM_MCP, ROM_PIP = 70.0, 90.0    # deg, R1 range
COMPLIANCE = 5.0                 # mm, cuff and liner take-up at design load, added to the stroke
MU, BEND = 0.10, pi              # sheath friction coefficient and total bend (rad), neutral wrist
MU_HI, BEND_HI = 0.15, 1.5 * pi  # pessimistic case: worn liner, flexed wrist
ETA_IDLER = 0.95                 # one idler bearing per tendon line
ETA_BALANCE = 0.95               # N3 (DDR-002): one floating balance pulley per spool line
STROKE_MIN_DESIGN = 4.0          # s, N5 (DDR-002): lower stroke-time limit at design load (R5)
DWELL = 1.0                      # s at each end
# Gearmotor: Pololu 4869, 227:1 25D MP 12 V with 48 CPR encoder (datasheet at 12 V)
V_RATED, I_STALL, I_NL, RPM_NL, T_STALL = 12.0, 1.8, 0.10, 35.0, 24 * 0.0980665   # T in N·m
T_CONT, T_INT = 4 * 0.0980665, 8 * 0.0980665          # recommended continuous and intermittent load
M_MOTOR = 107.0                                         # g, datasheet
V_BUS = 7.2              # V, 2S pack under load, less driver drop
P_CTRL = 0.40            # W, ESP32-S3, drivers idle, LED, regulator
CELL_WH = 2.5 * 3.6      # Wh per 18650 cell (2,500 mAh, 3.6 V)
N_CELLS, USABLE = 2, 0.80
HOLD_AT_EXTENSION = True # conservative: hold full torque with current during the extended dwell
# Stiffness of post-stroke fingers, Heung et al. 2020 (Front. Bioeng. Biotechnol. 8:111)
K_MAS1P = (0.089, 0.092)     # N·m/rad, MCP and PIP, subject with MAS 1+
K_MAS3 = (0.631, 0.753)      # N·m/rad, MCP and PIP, subject with MAS 3
# Contact pressure
P_LIMIT = 50.0           # kPa, R11
# Densities (g/cm3) and bought-part masses (g)
RHO_PETG, RHO_TPU, RHO_PA12, RHO_EVA, RHO_LINER = 1.27, 1.21, 1.01, 0.07, 0.20
RHO_STEEL, RHO_BRASS = 7.85, 8.5
FILL_BLOCK = 0.40        # infill share for the solid-looking anchor block
MASS = {"cell": 45.0, "bms": 5.0, "controller": 3.0, "driver": 3.0, "charger": 4.0, "estop": 20.0,
        "idler": 1.5, "balance": 1.5, "coupling": 2.0,   # N4: ball-detent breakaway (magnetic was 7.0 g)
        "coupling_magnetic": 7.0, "slack_spring": 1.0, "strap": 8.0, "wiring": 15.0, "regulator": 3.0,
        "stop_bead": 0.1,
        "glove": 40.0, "sheath_g_per_m": 25.0, "ferrule": 0.5, "tendon_g_per_m": 0.45}
BYTES_PER_SESSION, FLASH_LOG_BYTES = 32, 1_000_000


def motor_model(v):
    """Output-shaft DC model from the 12 V datasheet points. Returns (R, kt, ke, stall torque at v)."""
    R = V_RATED / I_STALL
    kt = T_STALL / (I_STALL - I_NL)                       # N·m per A above no-load current
    ke = (V_RATED - I_NL * R) / (RPM_NL * 2 * pi / 60)     # V per rad/s at the output
    return R, kt, ke, (v / R - I_NL) * kt


def stroke(force_fn, travel_mm, eta, r_m, v=V_BUS, n=400):
    """Full-voltage stroke. force_fn(s) gives force per finger at travel s (mm). Returns dict."""
    R, kt, ke, _ = motor_model(v)
    t = e_el = e_shaft = e_fing = 0.0
    tq = []
    ds = travel_mm / n
    for i in range(n):
        s = (i + 0.5) * ds
        f = FINGERS_PER_MOTOR * force_fn(s)             # N at the fingers
        T = f / eta * r_m                              # N·m at the spool
        I = I_NL + T / kt
        w = (v - I * R) / ke                           # rad/s
        dt = (ds / 1000) / (w * r_m)
        t += dt; e_el += v * I * dt; e_shaft += T * w * dt; e_fing += f * ds / 1000
        tq.append((T, dt))
    return dict(t=t, e_el=e_el, e_shaft=e_shaft, e_fing=e_fing, tq=tq)


def compute():
    import model
    m = model.build_parts()
    d, parts, sub = m["d"], m["parts"], m["sub"]
    R = {}

    # ---- A. Excursion (R1) ----
    ext = R_MCP * radians(ROM_MCP) + R_PIP * radians(ROM_PIP)
    flx = R_MCP_F * radians(ROM_MCP) + R_PIP_F * radians(ROM_PIP)
    travel = ext + COMPLIANCE
    r_eff = d["spool_r_eff"] / 1000
    cap = 2 * pi * d["spool_r_eff"] * (d["spool_w"] / 2 - 1.5) / (d["tendon_d"] * 2)   # one layer, per line
    R.update(ext=ext, flx=flx, mismatch=flx - ext, travel=travel, spool_turns=travel / (2 * pi * d["spool_r_eff"]),
             groove_cap=cap)

    # ---- B. Design load against published stiffness (R2 basis) ----
    def need(k):
        return max(k[0] * radians(ROM_MCP) / (R_MCP / 1000), k[1] * radians(ROM_PIP) / (R_PIP / 1000))
    R.update(F_mas1p=need(K_MAS1P), F_mas3=need(K_MAS3),
             k_cover=F_DESIGN * (R_PIP / 1000) / radians(ROM_PIP))

    # ---- C. Transmission and torque (R2) ----
    eta = exp(-MU * BEND) * ETA_IDLER * ETA_BALANCE
    eta_hi = exp(-MU_HI * BEND_HI) * ETA_IDLER * ETA_BALANCE
    F_spool = FINGERS_PER_MOTOR * F_DESIGN / eta
    T_peak = F_spool * r_eff
    T_peak_hi = FINGERS_PER_MOTOR * F_DESIGN / eta_hi * r_eff
    Rm, kt, ke, T_st = motor_model(V_BUS)
    R.update(eta=eta, eta_hi=eta_hi, F_spool=F_spool, T_peak=T_peak, T_peak_hi=T_peak_hi, T_cont=T_CONT,
             T_int=T_INT, T_stall_bus=T_st, Rm=Rm, kt=kt, ke=ke)

    # ---- D. Speed, cycle and dose (R4, R5) ----
    ext_fn = lambda s: F_START + (F_DESIGN - F_START) * min(s / travel, 1.0)
    se = stroke(ext_fn, travel, eta, r_eff)
    sf = stroke(lambda s: F_FLEX, travel, eta, r_eff)
    se_hi = stroke(ext_fn, travel, eta_hi, r_eff)
    cycle = se["t"] + sf["t"] + 2 * DWELL
    w_nl = (V_BUS - I_NL * Rm) / ke
    R.update(t_ext=se["t"], t_flex=sf["t"], t_ext_hi=se_hi["t"], cycle=cycle, cycles_per_min=60 / cycle,
             cycles_per_h=3600 / cycle, rpm_nl_bus=w_nl * 60 / (2 * pi), v_tendon_nl=w_nl * r_eff * 1000,
             t_noload=travel / (w_nl * r_eff * 1000), mcp_speed=ROM_MCP / se["t"], pip_speed=ROM_PIP / se["t"],
             max_stroke_for_R4=(3600 / 300 - 2 * DWELL) / 2,
             cycles_per_h_min=3600 / (2 * STROKE_MIN_DESIGN + 2 * DWELL))
    # RMS spool torque over a cycle (hold at extension counted at peak torque)
    num = sum(T * T * dt for T, dt in se["tq"] + sf["tq"]) + (T_peak ** 2) * DWELL
    R["T_rms"] = (num / cycle) ** 0.5

    # ---- E. Force limit (R3) ----
    T_lim_pair = FINGERS_PER_MOTOR * 40.0 / eta * r_eff
    I_lim = I_NL + T_lim_pair / kt
    f_est_lo, f_est_hi = 40.0 * eta_hi / eta, 40.0 * exp(-0.05 * pi) * ETA_IDLER * ETA_BALANCE / eta
    # N3: the balance pulley keeps both tendons of a pair at the same tension, so the pair limit is also
    # the per-finger limit (was: one finger up to the whole pair force, 80 N, with the partner slack)
    R.update(I_lim=I_lim, T_lim_pair=T_lim_pair, I_peak=I_NL + T_peak / kt,
             F_single_at_limit=T_lim_pair / r_eff * eta / FINGERS_PER_MOTOR,
             F_single_no_balance=FINGERS_PER_MOTOR * 40.0, f_est_lo=f_est_lo, f_est_hi=f_est_hi,
             balance_travel=d["balance_travel"], travel_free=FINGERS_PER_MOTOR * travel)

    # ---- F. Energy (R6) ----
    I_hold = I_NL + T_peak / kt
    e_hold = V_BUS * I_hold * DWELL if HOLD_AT_EXTENSION else 0.0
    e_cycle_motor = se["e_el"] + sf["e_el"] + e_hold
    cyc = R["cycles_per_h"]
    E_motor = 2 * e_cycle_motor * cyc / 3600          # Wh per 60 min session, both motors
    E_shaft = 2 * (se["e_shaft"] + sf["e_shaft"]) * cyc / 3600
    E_finger = 2 * (se["e_fing"] + sf["e_fing"]) * cyc / 3600
    E_ctrl = P_CTRL * 1.0
    E_session = E_motor + E_ctrl
    pack_wh = N_CELLS * CELL_WH
    R.update(e_ext=se["e_el"], e_flex=sf["e_el"], e_hold=e_hold, I_hold=I_hold, E_motor_Wh=E_motor,
             E_shaft_Wh=E_shaft, E_finger_Wh=E_finger, E_ctrl_Wh=E_ctrl, E_session_Wh=E_session,
             P_avg=E_session, pack_Wh=pack_wh, usable_Wh=pack_wh * USABLE,
             sessions=pack_wh * USABLE / E_session, I_avg=E_session / V_BUS)

    # ---- G. Mass (R7) ----
    v = lambda s: s.volume / 1000.0          # cm3
    C = m["c"]
    sheath_len = sum(Lp for _, _, Lp in m["sheath_paths"]) * d["sheath_slack"] / 1000   # m
    m_sheaths = sheath_len * MASS["sheath_g_per_m"] + 16 * MASS["ferrule"]
    steel = sum(v(C[k]) for k in ("cuff_screws", "motor_screws", "tray_screws", "lid_screws", "cover_screws",
                                    "anchor_screws", "idler_pins", "balance_pins"))
    m_fix = steel * RHO_STEEL + v(C["inserts"]) * RHO_BRASS
    pack = {
        "Forearm cuff shell (PETG)": v(sub["cuff_shell"]) * RHO_PETG,
        "Cuff liner (EVA foam)": v(sub["cuff_liner"]) * RHO_EVA,
        "Straps (2)": 2 * MASS["strap"],
        "Pack base (PETG)": v(C["pack_base"]) * RHO_PETG,
        "Pack lid (PETG)": v(C["pack_lid"]) * RHO_PETG,
        "Electronics tray (PETG)": v(C["tray"]) * RHO_PETG,
        "Gearmotors (2)": 2 * M_MOTOR,
        "Spools (2, PA12)": v(C["spools"]) * RHO_PA12,
        "Idler bearings (4)": 4 * MASS["idler"],
        "Cells (2) and BMS": N_CELLS * MASS["cell"] + MASS["bms"],
        "Controller, drivers, charger, regulator": MASS["controller"] + 2 * MASS["driver"] + MASS["charger"] + MASS["regulator"],
        "Emergency stop": MASS["estop"],
        "Anchor block, release plate, cover, pucks": (v(C["anchor_body"]) * FILL_BLOCK + v(C["gate"]) + v(C["cover"])
                                                       + v(C["pucks"])) * RHO_PETG,
        "Couplings (8) and slack springs (4)": 8 * MASS["coupling"] + 4 * MASS["slack_spring"],
        "Balance pulleys (4)": 4 * MASS["balance"],
        "Wiring": MASS["wiring"],
        "Screws, inserts and pins": m_fix,
        "Sheaths, half": m_sheaths / 2,
    }
    tendon_len = 8 * 0.40 + 4 * 0.03          # extensors run on about 30 mm to the thimble
    hand = {
        "Base glove (bought)": MASS["glove"],
        "Dorsal and palmar plates with stop blocks (TPU)": (v(C["dorsal_plate"]) + v(C["palmar_plate"])) * RHO_TPU,
        "Finger cuffs (8, TPU)": v(C["finger_cuffs"]) * RHO_TPU,
        "Cuff liners": v(C["cuff_liners"]) * RHO_LINER,
        "Fingertip thimbles (4, TPU)": v(C["thimbles"]) * RHO_TPU,
        "Thimble liners": v(C["thimble_liners"]) * RHO_LINER,
        "Thumb spacer (TPU)": v(C["thumb_spacer"]) * RHO_TPU,
        "Tendons and stop beads": tendon_len * MASS["tendon_g_per_m"] + 8 * MASS["stop_bead"],
        "Sheaths, half": m_sheaths / 2,
    }
    R.update(mass_pack=pack, mass_hand=hand, m_pack=sum(pack.values()), m_hand=sum(hand.values()),
             sheath_len=sheath_len, m_sheaths=m_sheaths, m_motors=2 * M_MOTOR, m_fix=m_fix,
             m_couplings=8 * MASS["coupling"], m_couplings_saved=8 * (MASS["coupling_magnetic"] - MASS["coupling"]),
             m_cuff_perf_saved=(v(sub["cuff_shell_solid"]) - v(sub["cuff_shell"])) * RHO_PETG,
             cuff_open_frac=1 - v(sub["cuff_shell"]) / v(sub["cuff_shell_solid"]))

    # ---- H. Cuff pressure (R11) and fit (R10) ----
    rows = []
    names = ["Index", "Middle", "Ring", "Little"]
    # N2: the extensor load is shared by the middle-phalanx anchor cuff and the fingertip thimble;
    # assumed shared in proportion to contact area (equal mean pressure), to check at TRL 4
    for nm, fg in zip(names, d["finger_geom"]):
        area = fg["anchor_w"] * fg["arc"]
        rows.append(dict(name=nm, lm=fg["lm"], usable=fg["usable"], w=fg["anchor_w"], arc=fg["arc"],
                         tw=fg["thimble_w"], ld=fg["ld"],
                         p_cuff=F_DESIGN / area * 1000, p20=F_DESIGN / (20 * fg["arc"]) * 1000,
                         p=F_DESIGN / ((fg["anchor_w"] + fg["thimble_w"]) * fg["arc"]) * 1000))
    R["cuffs"] = rows
    R["p12"] = F_DESIGN / (12 * 25) * 1000                       # TRL 2 basis: 12 mm x 25 mm
    R["hand_length"] = d["hand_length"]
    sizes = {}
    for sz, hl in (("S", 170.0), ("M", d["hand_length"]), ("L", 205.0)):
        k = hl / d["hand_length"]
        lit = d["finger_geom"][3]
        usable = lit["lm"] * k - 2 * d["joint_clear"]
        tw = min(d["thimble_w_max"], lit["ld"] * k - d["joint_clear"])
        arc = lit["arc"] * k
        sizes[sz] = dict(k=k, little_usable=usable, little_tw=tw,
                         little_p_cuff=F_DESIGN / (min(20, usable) * arc) * 1000,
                         little_p=F_DESIGN / ((min(20, usable) + tw) * arc) * 1000)
    R["sizes"] = sizes

    # ---- I. Stop (R9) ----
    C_bulk, dV = 100e-6, V_BUS
    R["t_holdup_ms"] = C_bulk * dV / (2 * I_hold) * 1000
    R["t_bounce_ms"] = 5.0
    R["t_stop_ms"] = R["t_holdup_ms"] + R["t_bounce_ms"] + 5.0      # plus 5 ms rotor run-down (estimate)

    # ---- J. Cost (R12) ----
    with (ROOT / "bom" / "bom.csv").open() as fh:
        bom = list(csv.DictReader(fh))
    R["bom_lines"] = len(bom)
    R["bom_total"] = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in bom)
    import yaml
    R["budget"] = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])

    # ---- K. Log (R13) ----
    R["log_days"] = FLASH_LOG_BYTES / (BYTES_PER_SESSION * 3)
    return R


def status_table(R):
    c = {r["name"]: r for r in R["cuffs"]}
    worst = max(r["p"] for r in R["cuffs"])
    worst_all = max(max(r["p"] for r in R["cuffs"]), max(s["little_p"] for s in R["sizes"].values()))
    st = lambda ok, bad="not met": "met" if ok else bad
    return [
        ("R1", "Finger range (tendon excursion)", f"{R['ext']:.1f} mm needed; {R['travel']:.1f} mm stroke", "25 mm for MCP 70°, PIP 90°", "met"),
        ("R2", "Extend against mild flexor tone", f"30 N covers {R['F_mas1p']:.0f} N needed at MAS 1+; {R['T_peak']:.3f} N·m peak, {R['T_rms']:.3f} N·m RMS at the spool", f"30 N per finger (MAS 1 to 1+); gearbox {T_CONT:.2f} N·m continuous, {T_INT:.2f} N·m intermittent", "at risk" if R['T_peak'] > T_CONT else "met"),
        ("R3", "Limit force on the hand", f"{R['I_lim']:.2f} A trip; balance pulley holds each finger to {R['F_single_at_limit']:.0f} N; friction spread {R['f_est_lo']:.0f} to {R['f_est_hi']:.0f} N", "40 N per finger (software); 60 N breakaway", "at risk"),
        ("R4", "Repetition dose", f"{R['cycles_per_h']:.0f} cycles per hour at full speed; {R['cycles_per_h_min']:.0f} at {STROKE_MIN_DESIGN:.0f} s strokes", "300 or more per 60 min", st(R['cycles_per_h_min'] >= 300)),
        ("R5", "Slow, smooth, adjustable stroke", f"fastest {R['t_ext']:.1f} s at design load ({R['t_ext_hi']:.1f} s pessimistic), {R['t_noload']:.1f} s unloaded", f"{STROKE_MIN_DESIGN:.0f} to 15 s at design load", st(R['t_ext_hi'] <= STROKE_MIN_DESIGN, "at risk")),
        ("R6", "Sessions per charge", f"{R['sessions']:.1f} sessions ({R['E_session_Wh']:.2f} Wh each)", "3 or more", "met"),
        ("R7", "Mass", f"hand {R['m_hand']:.0f} g; pack {R['m_pack']:.0f} g", "hand 120 g or less; pack 450 g or less", st(R['m_hand'] <= 120 and R['m_pack'] <= 450)),
        ("R8", "Donning and removal time", "not calculable", "5 min on, 1 min off", "not verifiable at TRL 3"),
        ("R9", "Stop and release", f"power cut in about {R['t_stop_ms']:.0f} ms; release by design", "100 ms; release in 10 s", "not verifiable at TRL 3"),
        ("R10", "Fit adult hands", "S, M, L glove sizes scaled from the model", "hand length 170 to 205 mm", "met"),
        ("R11", "Cuff contact pressure", f"cuff and thimble: {worst:.0f} kPa worst on the medium hand (little finger); index {c['Index']['p']:.0f}, middle {c['Middle']['p']:.0f}, ring {c['Ring']['p']:.0f}; {worst_all:.0f} kPa worst over S to L", "50 kPa or less", st(worst_all <= P_LIMIT)),
        ("R12", "Parts cost", f"USD {R['bom_total']:.2f}", f"value-engineering target USD {R['budget']:.0f}",
         f"under the target by USD {R['budget'] - R['bom_total']:.2f}" if R['bom_total'] <= R['budget'] else f"over the target by USD {R['bom_total'] - R['budget']:.2f}"),
        ("R13", "Session log", f"about {R['log_days']:,.0f} days of summaries in 1 MB of flash", "time, cycles, peak current; locked limits", "not verifiable at TRL 3"),
    ]


def main():
    R = compute()
    p = print
    p("FlexHand sizing (FXH-CAL-001)\n")
    p(f"[A1] extensor excursion {R['ext']:.1f} mm; flexor excursion {R['flx']:.1f} mm; mismatch {R['mismatch']:.1f} mm")
    p(f"[A2] stroke with {COMPLIANCE:.0f} mm compliance {R['travel']:.1f} mm = {R['spool_turns']:.2f} spool turns; one-layer groove capacity about {R['groove_cap']:.0f} mm per line")
    p(f"[B1] tendon force to extend fully: MAS 1+ finger {R['F_mas1p']:.1f} N; MAS 3 finger {R['F_mas3']:.1f} N")
    p(f"[B2] 30 N covers PIP stiffness up to {R['k_cover']:.3f} N·m/rad ({R['k_cover'] / K_MAS1P[1]:.1f} x the MAS 1+ value)")
    p(f"[C1] transmission efficiency {R['eta']:.3f} (mu {MU}, {degrees(BEND):.0f}° bend, idler {ETA_IDLER}, balance pulley {ETA_BALANCE}); pessimistic {R['eta_hi']:.3f}")
    p(f"[C2] spool tension {R['F_spool']:.1f} N; r_eff {R['T_peak'] / R['F_spool'] * 1000:.1f} mm; peak torque {R['T_peak']:.3f} N·m ({R['T_peak'] / T_CONT * 100:.0f} % of continuous, {R['T_peak'] / T_INT * 100:.0f} % of intermittent); pessimistic {R['T_peak_hi']:.3f} N·m")
    p(f"[C3] motor model at {V_BUS} V: R {R['Rm']:.2f} ohm, kt {R['kt']:.3f} N·m/A, ke {R['ke']:.3f} V·s/rad, stall {R['T_stall_bus']:.2f} N·m (peak is {R['T_peak'] / R['T_stall_bus'] * 100:.0f} % of stall)")
    p(f"[C4] RMS spool torque over a cycle {R['T_rms']:.3f} N·m ({R['T_rms'] / T_CONT * 100:.0f} % of continuous)")
    p(f"[D1] no-load {R['rpm_nl_bus']:.1f} rpm, {R['v_tendon_nl']:.1f} mm/s; unloaded stroke {R['t_noload']:.2f} s")
    p(f"[D2] extension {R['t_ext']:.2f} s (pessimistic friction {R['t_ext_hi']:.2f} s); flexion {R['t_flex']:.2f} s; dwell 2 x {DWELL:.0f} s; cycle {R['cycle']:.2f} s")
    p(f"[D3] {R['cycles_per_min']:.2f} cycles per min, {R['cycles_per_h']:.0f} per hour; R4 holds for strokes up to {R['max_stroke_for_R4']:.1f} s")
    p(f"[D4] joint speed at fastest extension: MCP {R['mcp_speed']:.1f} °/s, PIP {R['pip_speed']:.1f} °/s")
    p(f"[D5] at the {STROKE_MIN_DESIGN:.0f} s lower stroke limit (N5): {R['cycles_per_h_min']:.0f} cycles per hour")
    p(f"[E1] 40 N per finger on a pair = {R['T_lim_pair']:.3f} N·m, trip current {R['I_lim']:.3f} A; peak design current {R['I_peak']:.3f} A")
    p(f"[E2] with the balance pulley each finger carries half the spool line: {R['F_single_at_limit']:.0f} N per finger at the trip (without it one finger could carry {R['F_single_no_balance']:.0f} N)")
    p(f"[E3] friction spread: a 40 N current setting means {R['f_est_lo']:.0f} to {R['f_est_hi']:.0f} N at the fingers (mu 0.15 flexed wrist to mu 0.05)")
    p(f"[E4] balance pulley free travel {R['balance_travel']:.0f} mm against the {R['travel']:.1f} mm stroke; a free finger could move up to {R['travel_free']:.1f} mm if its partner is blocked, so each finger tendon carries a stop bead set to its own range")
    p(f"[F1] per motor per cycle: extension {R['e_ext']:.2f} J, flexion {R['e_flex']:.2f} J, hold {R['e_hold']:.2f} J ({R['I_hold']:.2f} A)")
    p(f"[F2] per 60 min session: motors {R['E_motor_Wh']:.2f} Wh, shafts {R['E_shaft_Wh']:.2f} Wh, fingers {R['E_finger_Wh']:.2f} Wh, controller {R['E_ctrl_Wh']:.2f} Wh; total {R['E_session_Wh']:.2f} Wh (average {R['P_avg']:.2f} W, {R['I_avg']:.2f} A)")
    p(f"[F3] pack {R['pack_Wh']:.0f} Wh, usable {R['usable_Wh']:.1f} Wh: {R['sessions']:.1f} sessions per charge")
    p("[G1] forearm pack mass by part (g):")
    for k, val in R["mass_pack"].items():
        p(f"       {k:48s} {val:6.1f}")
    p(f"[G2] forearm pack total {R['m_pack']:.0f} g (motors {R['m_motors']:.0f} g, couplings {R['m_couplings']:.0f} g, screws, inserts and pins {R['m_fix']:.0f} g); sheaths {R['sheath_len']:.2f} m, {R['m_sheaths']:.0f} g")
    p(f"[G5] N4 savings: ball-detent couplings {R['m_couplings_saved']:.0f} g; perforated cuff shell {R['m_cuff_perf_saved']:.1f} g ({R['cuff_open_frac'] * 100:.0f} % open)")
    p("[G3] hand-side mass by part (g):")
    for k, val in R["mass_hand"].items():
        p(f"       {k:40s} {val:6.1f}")
    p(f"[G4] hand-side total {R['m_hand']:.0f} g")
    p(f"[H1] TRL 2 basis, 12 mm x 25 mm patch: {R['p12']:.0f} kPa")
    p("[H2] anchor cuff on the middle phalanx plus fingertip thimble (medium hand):")
    for r in R["cuffs"]:
        p(f"       {r['name']:7s} middle phalanx {r['lm']:.1f} mm, cuff {r['w']:.1f} mm; distal {r['ld']:.1f} mm, thimble {r['tw']:.1f} mm; arc {r['arc']:.1f} mm -> {r['p']:.0f} kPa (cuff alone {r['p_cuff']:.0f} kPa; a 20 mm cuff alone {r['p20']:.0f} kPa)")
    for sz, s in R["sizes"].items():
        p(f"[H3] size {sz} (scale {s['k']:.2f}): little finger cuff {min(20, s['little_usable']):.1f} mm + thimble {s['little_tw']:.1f} mm -> {s['little_p']:.0f} kPa (cuff alone {s['little_p_cuff']:.0f} kPa)")
    p(f"[I1] stop: bulk capacitor hold-up {R['t_holdup_ms']:.1f} ms + contact {R['t_bounce_ms']:.0f} ms + run-down 5 ms = about {R['t_stop_ms']:.0f} ms")
    p(f"[J1] BOM {R['bom_lines']} lines, estimated cost USD {R['bom_total']:.2f}; value-engineering target USD {R['budget']:.0f}; "
      f"{'under' if R['bom_total'] <= R['budget'] else 'over'} the target by USD {abs(R['budget'] - R['bom_total']):.2f}")
    p(f"[K1] session log: {BYTES_PER_SESSION} B per session, 3 sessions a day: {R['log_days']:,.0f} days in {FLASH_LOG_BYTES / 1e6:.0f} MB")
    p("\nRequirement status:")
    for row in status_table(R):
        p("  " + " | ".join(row))


if __name__ == "__main__":
    main()
