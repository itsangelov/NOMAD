"""Round E finding F3: hub bracket vs solar rail floor. NON-PRODUCTION diagnostic (analysis only).

F3 (E2 validation): the B.1 hub-bracket envelope (Ø5 pin + WALL_THICKNESS below it) reaches 1.0 mm into the solar
rail channel floor wherever the bracket is inside the rail length.

This script characterises the interference and evaluates fix variants by rebuilding the exact E2 lid model
(e_lid_layout.py, imported READ-ONLY) in memory with explicit what-if overrides, then re-running the E2 checks
(moving parts over the E2 pose matrix, fine slide sweep, lid sweep 0-135 vs the base, rear-plug conflict, table
clearance). It writes nothing: not nomad.yaml, not the FeatureScript files, not Onshape.

  py CAD/tools/f3_investigation.py

STUDY INPUTS PINNED (2026-09-26, F3 implemented as option B): nomad.yaml now carries the option-B axis (-5.5) and the
e_lid_layout.py carriage now has the slot boss. The investigation's baseline and the variants measured against it are
pinned to the pre-F3 E2 axis (PRE_F3) and the E2 carriage, so the published report reproduces; part E checks that the
production layout now equals variant B exactly.

Evidence levels: geometry = modeled (the E2 X-prism machinery, which matched the Onshape kernel exactly at E2);
structural numbers = inferred (hand estimates under the stated load assumptions; no FEA, nothing tested).
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e_lid_layout as el  # noqa: E402
from yaml_to_featurescript import _eval_formula  # noqa: E402

P = el.P
MIN_GAP, CLR, WALL, MIN_WALL = P["MIN_GAP"], P["CLEARANCE"], P["WALL_THICKNESS"], P["MIN_WALL"]
PIN = P["SOLAR_HUB_PIN_DIAMETER"]
EPS = 1e-6

# What-if load cases for the structural estimates (inferred: the cassette and panel are not selected).
CASSETTE_MASS = 0.25    # kg: 200 x 147.5 x 8 PETG tray (~80-120 g) + a thin panel (~50-120 g), rounded up
TIP_LOAD = 10.0         # N: handling / gust at the cassette outboard edge, perpendicular to the tilt axis
GRAV = 9.81
PETG_UTS = (45.0, 25.0)  # MPa, nominal PETG tensile strength in-layer / across layers (typical datasheet order)


# ------------------------------------------------------------------ variant construction (in memory only)
def carriage_prims(rc, side, mode):
    if mode == "e2":        # E2: 22.6 x 8 body centred on the hub axis
        prims = [el.box("body", "KX0", f"{rc} - CW2", "HZ - CH2", "KX1", f"{rc} + CW2", "HZ + CH2")]
    else:                   # "boss": body fixed to the channel interior + a boss up through the slot to the rail top
        prims = [el.box("body", "KX0", f"{rc} - CW2", "ZR0 + WALL_THICKNESS", "KX1", f"{rc} + CW2", "ZR1 - WALL_THICKNESS"),
                 el.box("boss", "KX0", f"{rc} - BW2", "ZR1 - WALL_THICKNESS", "KX1", f"{rc} + BW2", "ZR1")]
    return prims if side > 0 else el.mirror(prims)


def grooved_rail(rc, side, depth):
    """E2 rail with a relief groove (bracket width + MIN_GAP each side) cut `depth` into the floor top."""
    prims = el.rail(rc, 1)
    c = prims[0][2]
    g0, g1 = f"{rc} - BW2 - MIN_GAP", f"{rc} + BW2 + MIN_GAP"
    floor = [el.box("floor_a", c[0], c[1], c[2], c[3], g0, c[5]),
             el.box("floor_groove", c[0], g0, c[2], c[3], g1, f"ZR0 + WALL_THICKNESS - {depth}"),
             el.box("floor_b", c[0], g1, c[2], c[3], c[4], c[5])]
    prims = floor + prims[1:]
    return prims if side > 0 else el.mirror(prims)


def parts_for(carriage="e2", groove=None):
    """E2 parts with the carriage rebuilt explicitly ("e2" = pre-F3 box on the axis, "boss" = option B)."""
    out = []
    for name, disp, g, key, adds, subs in el.PARTS_E2:
        side = 1 if name.endswith("_R") else -1
        rc = "RCR" if side > 0 else "RCL"
        if name.startswith("SOLAR_CARRIAGE_"):
            adds = carriage_prims(rc, side, carriage)
        elif name.startswith("SOLAR_RAIL_") and groove:
            adds = grooved_rail(rc, side, groove)
        out.append((name, disp, g, key, adds, subs))
    return out


def build(over=None, derived=None, parts=None):
    env = dict(P)
    env.update(over or {})
    for name, expr in el.DERIVED:
        expr = (derived or {}).get(name, expr)
        env[name] = _eval_formula(expr, name, lambda k: env[k])

    def ev(e, w):
        return _eval_formula(str(e), w, lambda k: env[k])

    def prims(lst, w):
        return [(k, lab, [ev(x, f"{w}.{lab}") for x in c]) for k, lab, c in lst]

    pts = [(n, d, g, key, prims(a, n), prims(s, n)) for n, d, g, key, a, s in (parts or el.PARTS_E2)]
    return env, pts, prims(el.BASE_POCKETS, "pockets")


def adds_of(parts, name):
    return next(a for n, _, _, _, a, _ in parts if n == name)


def prim(parts, name, label):
    return next(v for _, lab, v in adds_of(parts, name) if lab == label)


# ------------------------------------------------------------------ A. the interference itself
def characterise():
    env, parts, _ = build(PRE_F3, parts=parts_for())
    S = env["SOLAR_SLIDE_TRAVEL"]
    b = prim(parts, "SOLAR_HUB_BRACKET_R", "bracket")
    f = prim(parts, "SOLAR_RAIL_R", "floor")
    depth = f[5] - b[2]
    yov = min(b[4], f[4]) - max(b[1], f[1])
    full_until = f[3] - b[3]                  # slide at which the bracket's outboard face reaches the rail end
    clear_from = f[3] - b[0]                  # slide at which the bracket's inboard face passes the rail end
    print("A. F3 INTERFERENCE (E2 geometry, right side; the left side is its mirror image)")
    print(f"  hub axis Z {env['HZ']:g}; pin dia {PIN:g} -> pin bottom Z {env['HZ'] - PIN / 2:g}")
    print(f"  bracket envelope X {b[0]:g}..{b[3]:g} (stowed), Y {b[1]:g}..{b[4]:g}, Z {b[2]:g}..{b[5]:g} "
          f"(bottom = hub - pin radius {PIN / 2:g} - WALL {WALL:g})")
    print(f"  rail floor X {f[0]:g}..{f[3]:g}, Y {f[1]:g}..{f[4]:g}, Z {f[2]:g}..{f[5]:g} (floor top = channel bottom)")
    print(f"  intersecting surfaces: bracket bottom face Z {b[2]:g} vs floor top face Z {f[5]:g} -> penetration {depth:.2f} mm, "
          f"over the full bracket width {yov:g} mm")
    fl = el.to_prisms([("box", "floor", f)], [])
    br0 = el.to_prisms([("box", "bracket", b)], [])
    rows = []
    for s in (0, 50, 100, full_until, (full_until + clear_from) / 2, clear_from, S):
        xov = max(0.0, min(b[3] + s, f[3]) - max(b[0] + s, f[0]))
        c = el.clear([(x0 + s, x1 + s, p) for x0, x1, p in br0], fl)
        rows.append(f"slide {s:6.1f}: X overlap {xov:5.2f}, kernel-model clearance {c:+.3f}, volume {xov * yov * max(depth, 0):6.1f} mm3")
    print("  along the travel (penetration depth is constant; only the overlapped length changes):")
    for r in rows:
        print("    " + r)
    print(f"  -> interference over slide 0..{clear_from:g} of {S:g} mm ({100 * clear_from / S:.0f}% of the travel): full 10 mm "
          f"overlap to {full_until:g}, tapering to zero at {clear_from:g}; clear for the last {S - clear_from:g} mm "
          f"(= the hub link) and when deployed. No tilt occurs inside the rail (the cassette is captured by the lid slot).")
    # other rail features around the bracket (stowed)
    feats = {lab: el.to_prisms([("box", lab, v)], []) for _, lab, v in adds_of(parts, "SOLAR_RAIL_R")}
    print("  bracket vs the other rail features (stowed): " + ", ".join(f"{k} {el.clear(br0, v):+.2f}" for k, v in feats.items()))
    # a round-bottomed hub boss (r = pin/2 + WALL) instead of the square envelope
    r = PIN / 2 + WALL
    h = f[5] - (env["HZ"] - r)
    chord = 2 * math.sqrt(r * r - (r - h) ** 2)
    seg = r * r * math.acos((r - h) / r) - (r - h) * math.sqrt(2 * r * h - h * h)
    print(f"  a round-bottomed boss (r {r:g}) still penetrates {h:.2f} mm at its lowest line, over a {chord:.1f} mm chord "
          f"({seg * 10:.0f} mm3 per 10 mm): rounding or chamfering the envelope cannot remove F3.")
    return env


# ------------------------------------------------------------------ B. vertical budget below the tilt axis
def budget(env):
    avail = env["HZ"] - (env["ZR0"] + WALL)
    need = PIN / 2 + WALL + MIN_GAP
    need_c = PIN / 2 + WALL + CLR
    print("\nB. VERTICAL BUDGET BELOW THE TILT AXIS (the whole of F3)")
    print(f"  available: hub axis Z {env['HZ']:g} - floor top Z {env['ZR0'] + WALL:g} = {avail:g} mm "
          f"(= SOLAR_CARRIAGE_HEIGHT / 2, because the E2 axis is at the rail-layer mid-height)")
    print(f"  needed:    pin radius {PIN / 2:g} + bracket wall {WALL:g} + running gap MIN_GAP {MIN_GAP:g} = {need:g} mm "
          f"(with a CLEARANCE {CLR:g} fit instead: {need_c:g})")
    print(f"  deficit:   {need - avail:g} mm to MIN_GAP ({need_c - avail:g} to CLEARANCE; {PIN / 2 + WALL - avail:g} to mere contact)")
    print("  Every fix must recover this deficit in the one vertical stack below the axis: less material under the pin,")
    print("  a higher axis, a lower floor, or a smaller pin. Lateral moves, asymmetry, chamfers and radii do not act on it.")
    top_room = (env["ZC0"] - MIN_GAP) - (env["HZ"] + PIN / 2)
    print(f"  room above the pin before the OTHER stowed cassette (Z {env['ZC0']:g} - MIN_GAP): {top_room:g} mm "
          f"-> the axis may rise at most {top_room:g} mm (the right link/pin runs under the left cassette when stowed)")
    return need - avail


# ------------------------------------------------------------------ C. variants through the full E2 checks
def full_check(env, parts, pockets):
    grp = el.groups(parts)
    base = el.base_prisms(pockets)
    pr0 = el.pose(parts, env)
    rigid = el.rigid_group_checks(parts, pr0)
    solar = [n for n in pr0 if grp[n] not in ("lid", "baseHinge")]
    unexpected, brail, ground = set(), math.inf, {}

    def run(pr, tag):
        nonlocal brail
        v, _, m = el.moving_pairs_check(pr, grp)
        # the bracket-rail pair is reported separately (brail / bfloor), as in the published investigation
        unexpected.update(tag + x for x in v if "SOLAR_HUB_BRACKET" not in x[0] + x[1] or "SOLAR_RAIL" not in x[0] + x[1])
        for s in "RL":
            key = frozenset((f"SOLAR_HUB_BRACKET_{s}", f"SOLAR_RAIL_{s}"))
            brail = min(brail, m.get(key, math.inf))

    for lid in (0.0, 105.0, 120.0, 135.0):
        for e in ((0, 0), (1, 0), (0, 1), (1, 1)):
            run(el.pose(parts, env, lid, e), (lid, e, 0))
        for t in (0, 15, -15, 30, -30, 45, -45, 60, -60, 75, -75):
            for tt in ((t, t), (t, -t)):
                pr = el.pose(parts, env, lid, (1, 1), tt)
                run(pr, (lid, "both", tt))
                ground[(lid, tt)] = el.zmin(pr, [n for n in solar if not n.startswith("KEEPOUT")])
    for side in (0, 1):
        for other in (0, 1):
            for i in range(41):
                e = [0.0, 0.0]
                e[side], e[1 - side] = i / 40, other
                run(el.pose(parts, env, 105.0, tuple(e)), (105.0, tuple(e), 0))
    # bracket vs rail floor over the whole travel, 0.1 mm steps (the relation is rigid in the lid frame)
    S = env["SOLAR_SLIDE_TRAVEL"]
    bfloor = math.inf
    for s, sign in (("R", 1), ("L", -1)):
        floor = el.to_prisms([p for p in adds_of(parts, f"SOLAR_RAIL_{s}") if p[1].startswith("floor")], [])
        b = pr0[f"SOLAR_HUB_BRACKET_{s}"]
        for i in range(0, int(S * 10) + 1):
            dx = sign * i / 10
            bfloor = min(bfloor, el.clear([(x0 + dx, x1 + dx, p) for x0, x1, p in b], floor))
    # lid sweep vs the base, rear plugs
    lvb, worst, plug = 0, math.inf, {}
    for a in range(0, 136):
        pr = el.pose(parts, env, float(a))
        v, pl = el.lid_vs_base(pr, grp, base)
        lvb += len(v)
        worst = min(worst, min(el.clear(pr[n], base["BASE_SHELL"][1]) for n in pr
                               if grp[n] != "baseHinge" and not n.startswith("KEEPOUT")))
        plug[a] = min(c for _, _, c in pl)
    first = min((a for a, c in plug.items() if c < MIN_GAP - EPS), default=None)
    # stowed clearances to the other side's cassette (the right link runs under the left cassette)
    lips = el.to_prisms([p for p in adds_of(parts, "SOLAR_RAIL_R") if p[1].startswith("lip")], [])
    other = {n: el.clear(pr0[f"{n}_R"], pr0["SOLAR_CASSETTE_L"]) for n in ("SOLAR_HUB_PIN", "SOLAR_CARRIAGE", "KEEPOUT_SOLAR_CABLE_RUN")}
    car = adds_of(parts, "SOLAR_CARRIAGE_R")
    ctop = max(v[5] for _, _, v in car)
    return {
        "rigid": rigid, "unexpected": sorted(unexpected, key=str), "brail": brail, "bfloor": bfloor, "lvb": lvb,
        "worst_base": worst, "plug": plug, "first_plug": first, "ground": ground, "other": other,
        "boss_lip": el.clear(pr0["SOLAR_CARRIAGE_R"], lips),
        "T": env["ZS1"] - env["ZF"], "closed": env["ZS1"], "HZ": env["HZ"],
        "brk_wall": env["HZ"] - PIN / 2 - env["BZ0"],
        "car_below": env["HZ"] - PIN / 2 - (env["ZR0"] + WALL), "car_above": ctop - (env["HZ"] + PIN / 2),
        "notch_strip": env["NZ0"] - env["ZF"], "drop": env["ZC0"] - env["HZ"],
        "cable_below": env["HZ"] - env["CD2"] - (env["ZR0"] + WALL), "cable_above": ctop - (env["HZ"] + env["CD2"]),
    }


def rlh_over(ch):
    rlh = ch + 2 * WALL
    return {"SOLAR_CARRIAGE_HEIGHT": ch, "SOLAR_RAIL_LAYER_HEIGHT": rlh,
            "SOLAR_HUB_AXIS_OFFSET_Z": -(MIN_GAP + rlh / 2),
            "LID_THICKNESS": P["LID_THICKNESS"] - P["SOLAR_RAIL_LAYER_HEIGHT"] + rlh}


RLH = P["SOLAR_RAIL_LAYER_HEIGHT"]
PRE_F3 = {"SOLAR_HUB_AXIS_OFFSET_Z": -(MIN_GAP + RLH / 2)}     # pinned: the E2 (B.1 rail mid-height) axis, -7.5
VARIANTS = [
    ("E2", "E2 baseline (F3 present)", PRE_F3, {}, {}),
    ("A1", "(a) bracket wall under the pin 1.5", PRE_F3, {"BZ0": "HZ - SOLAR_HUB_PIN_DIAMETER / 2 - 1.5"}, {}),
    ("A2", "(a') bracket wall under the pin 0.5 (the MIN_GAP value)", PRE_F3, {"BZ0": "HZ - SOLAR_HUB_PIN_DIAMETER / 2 - 0.5"}, {}),
    ("B", "(b) axis +2.0 (offset -7.5 -> -5.5) + carriage slot boss",
     {"SOLAR_HUB_AXIS_OFFSET_Z": 2 * WALL + PIN / 2 - RLH}, {}, {"carriage": "boss"}),
    ("C1", "(c) channel +2 (carriage 10, rail layer 15), pin centred", rlh_over(10.0), {}, {}),
    ("C2", "(c') channel +4 (carriage 12, rail layer 17), pin centred", rlh_over(12.0), {}, {}),
    ("D", "(d) floor relief groove 2.0 deep under the bracket path", PRE_F3, {}, {"groove": 2.0}),
    ("E", "(e) pin clamped in a saddle bracket (no bore wall below the pin)", PRE_F3,
     {"BZ0": "HZ - SOLAR_HUB_PIN_DIAMETER / 2"}, {}),
    ("B20", "(b) + bracket length 10 -> 20 (related observation O1; NOT part of the F3 fix)",
     {"SOLAR_HUB_AXIS_OFFSET_Z": 2 * WALL + PIN / 2 - RLH, "SOLAR_BRACKET_LENGTH": 20.0}, {}, {"carriage": "boss"}),
]


def run_variants():
    print("\nC. VARIANTS THROUGH THE FULL E2 CHECK SET (modeled)")
    print("  checks: rigid groups; moving parts over lid 0/105/120/135 x stowed/R/L/both, tilts +-75 step 15 (same and opposite),")
    print("  slides 0..1 in 1/40 steps; bracket-floor every 0.1 mm of travel; lid sweep 0..135 vs base; rear plugs; table")
    res = {}
    for key, label, over, der, opts in VARIANTS:
        env, parts, pockets = build(over, der, parts_for(**opts))
        r = full_check(env, parts, pockets)
        res[key] = r
        g0 = r["ground"]
        print(f"\n  [{key}] {label}")
        print(f"    bracket-floor min over travel {r['bfloor']:+.2f} | bracket-rail min (incl. 0.3 slot fit) {r['brail']:+.2f} | "
              f"carriage boss/lips {r['boss_lip']:+.2f}")
        print(f"    rigid overlaps {r['rigid'] or 'none'} | unexpected moving violations {len(r['unexpected'])}"
              + (f", e.g. {r['unexpected'][:3]}" if r["unexpected"] else ""))
        print(f"    lid T {r['T']:.1f}, closed height {r['closed']:.1f}; lid sweep violations {r['lvb']}, min to BASE_SHELL {r['worst_base']:.3f}; "
              f"rear plugs 105 {r['plug'][105]:+.2f} / 120 {r['plug'][120]:+.2f} / 135 {r['plug'][135]:+.2f}, first < MIN_GAP at {r['first_plug']} deg")
        print(f"    hub axis Z {r['HZ']:g} ({r['drop']:g} below the cassette); walls around the pin: bracket below {r['brk_wall']:g}, "
              f"carriage below {r['car_below']:g} / above {r['car_above']:g}; cable channel in carriage below {r['cable_below']:g} / above {r['cable_above']:g}")
        print(f"    side-wall strip under the notch {r['notch_strip']:g}; stowed clearance to the other cassette: "
              + ", ".join(f"{k.split('_')[-1].lower()} {v:.2f}" for k, v in r["other"].items()))
        print("    table (lid 0 / 105 / 135; tilt +30, -45, +75, -75): " + " | ".join(
            "/".join(f"{g0[(lid, (t, t))]:.1f}" for t in (30, -45, 75, -75)) for lid in (0.0, 105.0, 135.0))
            + f"; lowest over all tilts at lid 105-135: {min(v for (lid, _), v in g0.items() if lid >= 105):.1f}")
    return res


# ------------------------------------------------------------------ D. structural estimates (inferred)
def section(rects):
    A = sum((y1 - y0) * (z1 - z0) for y0, y1, z0, z1 in rects)
    yc = sum((y1 - y0) * (z1 - z0) * (y0 + y1) / 2 for y0, y1, z0, z1 in rects) / A
    zc = sum((y1 - y0) * (z1 - z0) * (z0 + z1) / 2 for y0, y1, z0, z1 in rects) / A
    iy = sum((y1 - y0) * (z1 - z0) ** 3 / 12 + (y1 - y0) * (z1 - z0) * ((z0 + z1) / 2 - zc) ** 2 for y0, y1, z0, z1 in rects)
    iz = sum((z1 - z0) * (y1 - y0) ** 3 / 12 + (y1 - y0) * (z1 - z0) * ((y0 + y1) / 2 - yc) ** 2 for y0, y1, z0, z1 in rects)
    j = sum(max(y1 - y0, z1 - z0) * min(y1 - y0, z1 - z0) ** 3 / 3 for y0, y1, z0, z1 in rects)
    return A, iy, iz, j


def rail_rects(rlh, groove=None):
    rw, sw = P["SOLAR_RAIL_WIDTH"], P["SOLAR_RAIL_SLOT_WIDTH"]
    lip = (rw - sw) / 2
    floor = [(0, rw, 0, WALL)]
    if groove:
        g0, g1, t = groove
        floor = [(0, g0, 0, WALL), (g0, g1, 0, t), (g1, rw, 0, WALL)]
    return floor + [(0, WALL, WALL, rlh - WALL), (rw - WALL, rw, WALL, rlh - WALL),
                    (0, lip, rlh - WALL, rlh), (rw - lip, rw, rlh - WALL, rlh)]


def structure(env):
    print("\nD. STRUCTURAL ESTIMATES (inferred; hand calculations, not FEA; for comparing variants)")
    W = CASSETTE_MASS * GRAV
    WC, BL = P["SOLAR_CASSETTE_WIDTH"], P["SOLAR_BRACKET_LENGTH"]
    link = P["SOLAR_HUB_LINK_LENGTH"]
    print(f"  load cases: G = cassette weight {W:.2f} N ({CASSETTE_MASS:g} kg, inferred) at the cassette centre; "
          f"H = {TIP_LOAD:g} N at the outboard edge (handling / gust)")
    cases = {"G": (W, WC / 2), "H": (TIP_LOAD, WC)}
    # bracket bore: moment about the bore mid-length, couple over the bore length (triangular bearing)
    print(f"  hub bracket bore (length {BL:g}, pin dia {PIN:g}): the bracket is the ONLY cassette-to-pin connection when deployed")
    for c, (F, x) in cases.items():
        M = F * (x - BL / 2)
        Fend = 1.5 * M / BL
        p = 6 * M / (PIN * BL ** 2)
        walls = ", ".join(f"t {t:g}: {1.5 * Fend / t ** 2:5.1f}" for t in (2.5, 1.5, 1.2, 0.5))
        print(f"    case {c}: M {M:6.0f} Nmm, end reaction {Fend:5.1f} N, peak bore pressure {p:4.1f} MPa; "
              f"bore-wall bending index (MPa) {walls}")
        if c == "H":
            L2 = 20.0
            Fend2 = 1.5 * F * (x - L2 / 2) / L2
            print(f"      (same case with a {L2:g} mm bore: end reaction {Fend2:5.1f} N, peak bore pressure "
                  f"{6 * F * (x - L2 / 2) / (PIN * L2 ** 2):4.1f} MPa, index at t 2.5: {(Fend2 * PIN / 4) / (L2 / 2 * 2.5 ** 2 / 6):4.1f} MPa)")
    print(f"    PETG reference strength (nominal): {PETG_UTS[0]:g} MPa in-layer, {PETG_UTS[1]:g} MPa across layers. The index scales "
          f"with 1/t^2: t 1.5 = {(2.5 / 1.5) ** 2:.1f}x, t 1.2 = {(2.5 / 1.2) ** 2:.1f}x, t 0.5 = {(2.5 / 0.5) ** 2:.0f}x the 2.5 wall.")
    # pin bending at the carriage exit (deployed)
    print("  hub pin bending at the carriage exit (deployed; lever from the carriage outboard face):")
    for c, (F, x) in cases.items():
        M = F * (link + x)
        print(f"    case {c}: M {M:6.0f} Nmm -> sigma " + ", ".join(f"dia {d:g} {M / (math.pi * d ** 3 / 32):5.0f} MPa" for d in (5, 4, 3)))
    # rail sections
    rw = P["SOLAR_RAIL_WIDTH"]
    gbox = (rw / 2 - P["SOLAR_BRACKET_WIDTH"] / 2 - MIN_GAP, rw / 2 + P["SOLAR_BRACKET_WIDTH"] / 2 + MIN_GAP, WALL - 2.0)
    hy_rel = env["HYR"] - (env["RCR"] - rw / 2)
    rb = PIN / 2 + WALL + MIN_GAP
    half = math.sqrt(rb ** 2 - (env["HZ"] - (env["ZR0"] + WALL)) ** 2)
    ground = (hy_rel - half, hy_rel + half, WALL - 2.0)
    base = section(rail_rects(RLH))
    rows = [("E2 / B (unchanged rail)", rail_rects(RLH), None),
            ("D, groove under the square bracket", rail_rects(RLH, gbox), gbox),
            ("D, groove under a round boss only", rail_rects(RLH, ground), ground),
            ("C1 (rail layer 15)", rail_rects(RLH + 2), None),
            ("C2 (rail layer 17)", rail_rects(RLH + 4), None)]
    interior = rw - 2 * WALL
    print(f"  rail cross-section (per rail; Iy = bending from loads normal to the lid, Iz = in-plane, J = open-section torsion):")
    for name, rects, g in rows:
        A, iy, iz, j = section(rects)
        bear = interior - (min(g[1], rw - WALL) - max(g[0], WALL)) if g else interior
        tmin = g[2] if g else WALL
        print(f"    {name:38s} A {A:6.1f} mm2  Iy {iy:7.0f} ({iy / base[1]:4.2f}x)  Iz {iz:7.0f} ({iz / base[2]:4.2f}x)  "
              f"J {j:6.0f} ({j / base[3]:4.2f}x)  min floor {tmin:g}  carriage bearing width {bear:4.1f} of {interior:g}")


def implemented():
    """E. The production layout (nomad.yaml + e_lid_layout.py as they are now) must equal variant B exactly."""
    # the E2 / F3 layer of the production layout (the D-009 index lock, Round E, is layered on top in el.PARTS)
    envp, partsp, _, _ = el.evaluate(el.PARTS_E2)
    envb, partsb, _ = build({"SOLAR_HUB_AXIS_OFFSET_Z": 2 * WALL + PIN / 2 - RLH}, None, parts_for(carriage="boss"))
    diffs = []
    for (n, _, _, _, a, s), (_, _, _, _, ab, sb) in zip(partsp, partsb):
        for (k, lab, v), (_, _, vb) in zip(a + s, ab + sb):
            if len(v) != len(vb) or any(abs(x - y) > 1e-9 for x, y in zip(v, vb)):
                diffs.append(f"{n}.{lab}")
        if len(a) != len(ab) or len(s) != len(sb):
            diffs.append(f"{n} (primitive count)")
    print()
    print(f"E. IMPLEMENTED MODEL (nomad.yaml + e_lid_layout.py) vs VARIANT B: hub axis Z {envp['HZ']:g} (B {envb['HZ']:g}); "
          + ("IDENTICAL geometry (all parts, all primitives)" if not diffs else f"DIFFERENT: {diffs[:8]}"))
    return not diffs


def main():
    env = characterise()
    budget(env)
    run_variants()
    structure(env)
    implemented()
    print("\nNothing was written (NON-PRODUCTION diagnostic).")


if __name__ == "__main__":
    main()
