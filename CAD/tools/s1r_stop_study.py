"""D-009 S1-R hard-stop feasibility study (NON-PRODUCTION, read-only): journaled metal stop yoke.

The S1-R candidate is built IN MEMORY on top of the D-009 E-lid model (e_lid_layout.py); nothing is written.

Architecture (right side; X stowed; dy/dz from the tilt axis):
- carriage side, clamped on the extended pin-tip double-D by the M2 tip screw:
  index plate (unchanged, X 11-12.5) | stainless journal bushing (X 12.5-15.8, OD 6) | stainless stop plate (X 15.8-18.3,
  radial stop faces at 210 / 330 deg).
- cassette side: a machined 17-4PH stop yoke:
  - ring (bore 6.1, OD 10) journaled on the bushing (X 13.0-15.5);
  - a stop lobe (faces 50 / 130 deg) reaching X 18.3;
  - a drive arm lying in a slot in the tray (0.3 float all round).
  The arm is driven only tangentially by a Ø3 dowel along X at R_k 25 (radially slotted, so the yoke floats radially
  on its ring).
- Load path at the stop: the contact force closes stop plate -> yoke -> ring -> bushing -> pin (metal). Only the
  drive force T / R_k reaches the PETG tray and bracket.
Imports the S1 helpers (regression, stop sweep) from s1_stop_study (their S1 entries are harmless here).
Usage: py CAD/tools/s1r_stop_study.py
"""
import math
import sys

import e_lid_layout as el
import s1_stop_study as s1

R1_INPUTS = [
    ("R1_STOP", "80"), ("R1_HB", "40"), ("R1_TSP", "2.5"), ("R1_LIG", "1.0"), ("R1_TY", "2.5"), ("R1_AX", "0.3"),
    ("R1_FLOAT", "0.3"), ("R1_BUSH_OD", "6.0"), ("R1_BORE_CL", "0.1"), ("R1_NECK", "3.0"), ("R1_RK", "25"),
    ("R1_ARME", "2.5"), ("R1_ARMY1", "3.0"), ("R1_DD", "3.0"), ("R1_TOPSKIN", "2.0"),
]
R1_DERIVED = [
    ("R1_RH", "KR + R1_LIG"),
    ("R1_RIN", "R1_RH + MIN_GAP"),
    ("R1_RS", "-BLY / cos(R1_HB + R1_STOP - 90)"),
    ("R1_RS_TRAY", "(TRB - MIN_GAP) / cos(R1_HB)"),
    ("R1_PHI1", "90 - R1_HB"), ("R1_PHI2", "90 + R1_HB"),
    ("R1_FA", "R1_PHI2 + R1_STOP"), ("R1_FB", "R1_PHI1 - R1_STOP"),
    ("R1_FLA", "180 * DEG + asin(-FLZ / R1_RS)"), ("R1_FLB", "360 * DEG - asin(-FLZ / R1_RS)"),
    ("R1_YX0", "GX1"),                                  # yoke inboard face (tray groove outboard wall)
    ("R1_YX1", "R1_YX0 + R1_TY"),                       # yoke plate / ring outboard face
    ("R1_SX0", "R1_YX1 + R1_AX"),                       # bushing end = stop plate inboard face
    ("R1_SX1", "R1_SX0 + R1_TSP"),                      # stop plate outboard face = extended pin tip
    ("R1_RRO", "-FLZ"),                                 # ring outer radius (hub-zone floor)
    ("R1_NZ0", "sqrt(R1_RRO * R1_RRO - R1_NECK * R1_NECK)"),
    ("R1_LOBEZ", "TRB - R1_FLOAT"),                     # lobe top (float gap below the tray)
    ("R1_ARMZ0", "TRB + R1_FLOAT"),
    ("R1_ARMZ1", "TRB + SOLAR_CASSETTE_THICKNESS - R1_TOPSKIN"),
    ("R1_DZ", "(R1_ARMZ0 + R1_ARMZ1) / 2"),             # drive dowel height
    ("R1_LW", "R1_LOBEZ * tan(R1_HB)"),                 # lobe half-width at its top
]
el.DERIVED_LOCK += R1_INPUTS + R1_DERIVED

SPN, BUN, YON, DDN = "SOLAR_STOP_PLATE_{}", "SOLAR_HUB_BUSHING_{}", "SOLAR_STOP_YOKE_{}", "SOLAR_YOKE_DOWEL_{}"


def r1_prims(side):
    h = el._Hub(side)
    pt = lambda r, a: (f"{r} * cos({a})", f"{r} * sin({a})")    # noqa: E731
    sp_outline = [h.arc("R1_RH", "R1_FB", "R1_FA"),
                  h.line(pt("R1_RH", "R1_FA"), pt("R1_RS", "R1_FA")),
                  h.arc("R1_RS", "R1_FA", "R1_FLA"),
                  h.line(("R1_RS * cos(R1_FLA)", "FLZ"), ("R1_RS * cos(R1_FLB)", "FLZ")),
                  h.arc("R1_RS", "R1_FLB", "R1_FB + 360 * DEG"),
                  h.line(pt("R1_RS", "R1_FB"), pt("R1_RH", "R1_FB"))]
    lobe = [h.arc("R1_RIN", "R1_PHI1", "R1_PHI2"),
            h.line(pt("R1_RIN", "R1_PHI2"), ("-R1_LW", "R1_LOBEZ")),
            h.line(("-R1_LW", "R1_LOBEZ"), ("R1_LW", "R1_LOBEZ")),
            h.line(("R1_LW", "R1_LOBEZ"), pt("R1_RIN", "R1_PHI1"))]
    ya, yb = "-R1_RK - (R1_DD / 2 + R1_FLOAT)", "-R1_RK + R1_DD / 2 + R1_FLOAT"      # radial float
    za, zb = "R1_DZ - R1_DD / 2 - 0.01", "R1_DZ + R1_DD / 2 + 0.01"                   # tangential drive fit
    slot = h.poly([(ya, za), (yb, za), (yb, zb), (ya, zb)])
    out = {
        "stop_plate": ([el.prof("plate", "R1_SX0", "R1_SX1", sp_outline)], [el.prof("key_hole", "R1_SX0", "R1_SX1", h.key())]),
        "bushing": ([h.cyl("bushing", "0", "0", "R1_BUSH_OD", "PX1", "R1_SX0")], [el.prof("key_hole", "PX1", "R1_SX0", h.key())]),
        "yoke": ([h.cyl("ring", "0", "0", "2 * R1_RRO", "R1_YX0", "R1_YX1"),
                  h.box("neck", "R1_YX0", "-R1_NECK", "R1_NZ0", "R1_YX1", "R1_NECK", "R1_ARMZ0"),
                  el.prof("lobe", "R1_YX0", "R1_SX1", lobe),
                  h.box("arm", "R1_YX0", "-R1_RK - R1_ARME", "R1_ARMZ0", "R1_YX1", "R1_ARMY1", "R1_ARMZ1")],
                 [h.cyl("bore", "0", "0", "R1_BUSH_OD + R1_BORE_CL", "R1_YX0", "R1_YX1"),
                  el.prof("drive_slot", "R1_YX0", "R1_YX1", slot)]),
        "dowel": ([h.cyl("dowel", "-R1_RK", "R1_DZ", "R1_DD", "XI + 0.5", "GDX1")], []),
        "tray_subs": [h.box("r1_slot", "R1_YX0", "-R1_RK - R1_ARME - R1_FLOAT", "TRB", "R1_YX1 + R1_FLOAT", "R1_ARMY1 + R1_FLOAT",
                            "R1_ARMZ1 + R1_FLOAT"),
                      h.cyl("r1_dowel_bore", "-R1_RK", "R1_DZ", "R1_DD", "XI", "GDX1")],
        "pin_tip": [el.prof("key_tip", "PX0", "R1_SX1", h.key())],
        "screw_tip": [h.cyl("washer", "0", "0", "SOLAR_HUB_WASHER_DIAMETER", "R1_SX1", "R1_SX1 + SOLAR_HUB_WASHER_THICKNESS"),
                      h.cyl("head", "0", "0", "SOLAR_HUB_SCREW_HEAD_DIAMETER", "R1_SX1 + SOLAR_HUB_WASHER_THICKNESS",
                            "R1_SX1 + SOLAR_HUB_WASHER_THICKNESS + SOLAR_HUB_SCREW_HEAD_HEIGHT")],
    }
    if side < 0:
        out = {k: ((el.mirror(v[0]), el.mirror(v[1])) if isinstance(v, tuple) else el.mirror(v)) for k, v in out.items()}
    return out


def r1_table():
    add = {("R" if sd > 0 else "L"): r1_prims(sd) for sd in (1, -1)}
    out = []
    for n, disp, g, key, a, sub in el.PARTS:
        s = n[-1]
        if n == f"SOLAR_HUB_PIN_{s}":
            a = [p for p in a if p[1] != "key_tip"] + add[s]["pin_tip"]
        elif n == f"SOLAR_HUB_SCREW_TIP_{s}":
            a = add[s]["screw_tip"]
        elif n == f"SOLAR_CASSETTE_{s}":
            sub = list(sub) + add[s]["tray_subs"]
        out.append((n, disp, g, key, a, sub))
        if n == f"SOLAR_INDEX_PLATE_{s}":
            out.append((BUN.format(s), "bushing [S1-R STUDY]", f"car{s}", "stainless", *add[s]["bushing"]))
            out.append((SPN.format(s), "stop plate [S1-R STUDY]", f"car{s}", "stainless", *add[s]["stop_plate"]))
        if n == f"SOLAR_CASSETTE_{s}":
            out.append((YON.format(s), "stop yoke [S1-R STUDY]", f"cas{s}", "stainless", *add[s]["yoke"]))
            out.append((DDN.format(s), "yoke drive dowel [S1-R STUDY]", f"cas{s}", "hardware", *add[s]["dowel"]))
    return out


for _s in "RL":
    el.GUIDED[frozenset((SPN.format(_s), YON.format(_s)))] = 0.0                                  # designed stop pair
    el.GUIDED[frozenset((YON.format(_s), f"SOLAR_INDEX_PLATE_{_s}"))] = el.P["SOLAR_INDEX_GROOVE_CLEARANCE"]
    el.GUIDED[frozenset((YON.format(_s), BUN.format(_s)))] = 0.05                                   # journal (radial)
    el.GUIDED[frozenset((YON.format(_s), f"SOLAR_HUB_PIN_{_s}"))] = 0.5                             # through the bushing
    el.GUIDED[frozenset((YON.format(_s), f"SOLAR_RAIL_{_s}"))] = el.P["CLEARANCE"]                   # rides the slot like the bracket


def service(parts, env):
    pr0 = el.pose(parts, env)
    grp = el.groups(parts)
    s = "R"
    cas = [n for n in pr0 if grp[n] == "cas" + s]
    rep = []
    w1 = min(el.clear(el._sx(pr0[SPN.format(s)], i / 4), pr0[n]) for i in range(0, 81) for n in cas)
    rep.append(f"(1) tip screw off; stop plate slid +X 0..20 off the pin at tilt 0 (cassette stays on): min to the cassette group {w1:.3f}")
    w2 = min(el.clear(el._sx(pr0[BUN.format(s)], i / 4), pr0[n]) for i in range(0, 101) for n in cas)
    rep.append(f"(2) bushing slid +X 0..25 out of the yoke ring and off the pin: min to the cassette group {w2:.3f} (0.05 = journal)")
    ext = el.pose(parts, env, 105.0, (1, 0))
    moving = cas + [f"SOLAR_INDEX_PLATE_{s}"]
    fixed = [f"SOLAR_HUB_PIN_{s}", f"SOLAR_CARRIAGE_{s}", f"SOLAR_ANTIROT_PLATE_{s}", f"SOLAR_RAIL_{s}", "LID_FRAME"]
    w3 = min(el.clear(el._sx(ext[m], i / 2), ext[f]) for i in range(0, 121) for m in moving for f in fixed)
    rep.append(f"(3) deployed; cassette + index plate (groove) + yoke + drive dowel slid +X 0..60 off the pin: min to pin / carriage / "
               f"rail / lid {w3:.3f} (0 = designed sliding fits)")
    return rep, (w1, w2, w3)


# ------------------------------------------------------------------ loads
T_D = 1260.0
SY = {"303": 415.0, "17-4 H1025": 1000.0, "301h": 758.0}
Z_R, ZP_R, Z_DD, ZT_DD = math.pi * 125 / 32, math.pi * 125 / 16, 6.6, 12.9
PETG_B = 30.0


def lobe_section(env, fdir):
    """Second moment of the lobe section about the centroidal axis normal to the force direction (grid integration)."""
    rin, zt, hb = env["R1_RIN"], env["R1_LOBEZ"], env["R1_HB"]
    pts, h = [], 0.02
    y = -8.0
    while y <= 8.0:
        z = 0.0
        while z <= zt:
            r = math.hypot(y, z)
            a = math.degrees(math.atan2(z, y))
            if r >= rin and 90 - hb <= a <= 90 + hb:
                pts.append((y, z))
            z += h
        y += h
    A = len(pts) * h * h
    ux, uz = fdir
    c = sum(p[0] * ux + p[1] * uz for p in pts) / len(pts)
    I = sum((p[0] * ux + p[1] * uz - c) ** 2 for p in pts) * h * h
    cmax = max(abs(p[0] * ux + p[1] * uz - c) for p in pts)
    return A, I, I / cmax


def pin_tip_moment(F, x_sp, x0, x1, xs):
    """Pin moment at section xs from: +F at the stop plate (x_sp) and the bushing reaction over [x0, x1] (linear
    distribution) equilibrating it (net ~0 inboard of x0: the pair closes in metal)."""
    Lb = x1 - x0
    xc = (x0 + x1) / 2
    Mb = F * (x_sp - xc)                                  # bushing must also carry this moment
    a, b = -F / Lb, -12 * Mb / Lb ** 3
    m = F * max(0.0, x_sp - xs)
    lo = max(xs, x0)
    n = 400
    for i in range(n):
        if lo >= x1:
            break
        x = lo + (x1 - lo) * (i + 0.5) / n
        m += (x - xs) * (a + b * (x - xc)) * (x1 - lo) / n
    return m


def loads(env):
    rin, rs, rh, tsp = env["R1_RIN"], env["R1_RS"], env["R1_RH"], env["R1_TSP"]
    rc = (rin + rs) / 2
    x_sp = (env["R1_SX0"] + env["R1_SX1"]) / 2
    lc = env["R1_SX1"] - env["R1_SX0"]
    wf = 2 * math.sqrt(2.5 ** 2 - (2.5 - (5 - env["SOLAR_HUB_PIN_KEY_ACROSS_FLATS"]) / 2) ** 2)
    rk = env["R1_RK"]
    x_ring = (env["R1_YX0"] + env["R1_YX1"]) / 2
    lines = [f"contact band R {rin:.3f}..{rs:.3f} (centroid {rc:.3f}), axial {lc:g} (X {env['R1_SX0']:g}-{env['R1_SX1']:g}); "
             f"ring X {env['R1_YX0']:g}-{env['R1_YX1']:g}; bushing X {env['PX1']:g}-{env['R1_SX0']:g}; drive R_k {rk:g} at X {x_ring:g}"]
    fdir = (math.cos(math.radians(env["R1_PHI2"] - 90)), math.sin(math.radians(env["R1_PHI2"] - 90)))
    A, I, Zl = lobe_section(env, (-fdir[1], fdir[0]))
    table = {}
    for tag, k in (("T_d 1.26", 1.0), ("T_acc 2.52", 2.0)):
        T = T_D * k
        F = T / rc
        K = T / rk
        mu = 0.2
        rows = []
        estar = 193000.0 / (2 * (1 - 0.09))
        rows.append(("contact, crowned R10 face (Hertz line)", math.sqrt((F / lc) * estar / (math.pi * 10.0)), None, "hardened 17-4 H900 / H1025 faces"))
        rows.append(("stop plate key A/F 3.0 (t 2.5)", 6 * T / (tsp * wf * wf), SY["301h"], "301 1/2-hard"))
        rows.append(("stop plate sector shear", F / (tsp * (rs - rh)), 0.58 * SY["301h"], "301 1/2-hard"))
        rows.append(("yoke lobe root bending (cantilever from the ring plate)", F * (x_sp - env["R1_YX1"]) / Zl, SY["17-4 H1025"], "17-4 H1025"))
        Mr = F * (x_sp - x_ring)
        rows.append(("yoke ring edge bearing on the bushing (force + moment)", F / (env["R1_BUSH_OD"] * env["R1_TY"]) +
                     6 * Mr / (env["R1_BUSH_OD"] * env["R1_TY"] ** 2), 1.5 * SY["17-4 H1025"], "17-4 H1025 (bearing ~1.5 sy)"))
        wr = env["R1_RRO"] - (env["R1_BUSH_OD"] + env["R1_BORE_CL"]) / 2
        rm = (env["R1_RRO"] + (env["R1_BUSH_OD"] + env["R1_BORE_CL"]) / 2) / 2
        rows.append(("yoke ring bending (0.318 F Rm, section t x wall)", 0.318 * F * rm / (env["R1_TY"] * wr ** 2 / 6), SY["17-4 H1025"], "17-4 H1025"))
        mt = max(abs(pin_tip_moment(F, x_sp, env["PX1"], env["R1_SX0"], env["PX1"] + i * (env["R1_SX0"] - env["PX1"]) / 40)) for i in range(41))
        for mat in ("303", "17-4 H1025"):
            rows.append((f"hub pin tip double-D (local stop couple {mt:.0f} N.mm + torsion)", math.sqrt((mt / Z_DD) ** 2 + 3 * (T / ZT_DD) ** 2), SY[mat], mat))
        m_in = abs(pin_tip_moment(F, x_sp, env["PX1"], env["R1_SX0"], env["PX1"] - 1.0))
        rows.append((f"hub pin inboard of the bushing: residual stop moment {m_in:.1f} N.mm (closes in metal)", 0.0, None, ""))
        for mat in ("303", "17-4 H1025"):
            rows.append(("hub pin root (handling bending x k + torsion; stop adds nothing)", math.sqrt((k * 2176.0 / Z_R) ** 2 + 3 * (T / ZP_R) ** 2), SY[mat], mat))
            rows.append(("hub pin inboard double-D torsion", math.sqrt(3) * T / ZT_DD, SY[mat], mat))
        Vb = K * (1 + mu)
        Mb = Vb * (x_ring - 5.5)
        rows.append((f"PETG bracket bore, stop only: V {Vb:.0f} N (drive T/R_k + 20 % friction), M {Mb:.0f} N.mm",
                     Vb / 50 + 6 * Mb / 500, PETG_B, "PETG RT (hot /2)"))
        beta = (2500.0 / (4 * 193000.0 * math.pi * 3 ** 4 / 64)) ** 0.25
        rows.append(("drive dowel in the tray (foundation bound)", K * beta / 3, PETG_B, "PETG RT (hot /2)"))
        armh = env["R1_ARMZ1"] - env["R1_ARMZ0"]
        rows.append(("yoke drive arm bending", K * (rk - 3) / (env["R1_TY"] * armh ** 2 / 6), SY["17-4 H1025"], "17-4 H1025"))
        rows.append(("anti-rotation plate key (D-009 path, unchanged)", 6 * T / (1.5 * wf * wf), SY["301h"], "301 1/2-hard"))
        rows.append(("carriage PETG under the dowel, bound (D-009 path, unchanged)", 12.7 * k, PETG_B, "PETG RT (hot /2)"))
        table[tag] = (F, K, rows)
        lines.append(f"-- {tag} N.m: stop force {F:.0f} N at R {rc:.2f}; drive force {K:.0f} N at R_k {rk:g}")
        for name, s, allow, mat in rows:
            lines.append(f"   {name}: " + (f"{s:.1f} MPa" if s else "") + (f" -> SF {allow / s:.2f} ({mat})" if allow and s else (f" ({mat})" if mat else "")))
    lines.append(f"   (lobe section: area {A:.1f} mm^2, Z {Zl:.1f} mm^3 normal to the contact force)")
    s1_bore = 245.3 / 50 + 6 * 245.3 * 8.75 / 500
    lines.append(f"transverse force into the PETG bracket at T_d: S1 {245:.0f} N with moment {245 * 8.75:.0f} N.mm (bore {s1_bore:.1f} MPa) -> "
                 f"S1-R {table['T_d 1.26'][1] * 1.2:.0f} N with moment {table['T_d 1.26'][1] * 1.2 * (x_ring - 5.5):.0f} N.mm")
    lines.append("R_k sensitivity (T_d, stop-only bore peak / SF): " + "; ".join(
        f"R_k {r:g}: {T_D / r * 1.2 / 50 + 6 * T_D / r * 1.2 * (x_ring - 5.5) / 500:.1f} MPa / "
        f"{PETG_B / (T_D / r * 1.2 / 50 + 6 * T_D / r * 1.2 * (x_ring - 5.5) / 500):.2f}" for r in (15, 20, 25, 30, 35)))
    return lines, rc


def tolerance(env, rc):
    rk = env["R1_RK"]
    wf = 2 * math.sqrt(2.5 ** 2 - (2.5 - (5 - env["SOLAR_HUB_PIN_KEY_ACROSS_FLATS"]) / 2) ** 2)
    d = lambda mm, r: math.degrees(mm / r)            # noqa: E731
    items = [  # name, as specified (D-009 key fits, printed-then-reamed bores), metal-referenced (tight keys, jig-reamed)
        ("stop plate faces vs its key (wire EDM +-0.02)", d(0.02, rc), d(0.02, rc)),
        ("stop plate key clocking (A/F clearance 0.04 | 0.02)", math.degrees(0.04 / wf), math.degrees(0.02 / wf)),
        ("index plate key clocking (A/F clearance 0.04 | 0.02)", math.degrees(0.04 / wf), math.degrees(0.02 / wf)),
        ("index hole true position (+-0.03 at r 10)", d(0.03, 10), d(0.03, 10)),
        ("index pin in its hole (0.05 radial)", d(0.05, 10), d(0.05, 10)),
        ("index pin bores in the tray vs drive-dowel bore (printed + reamed +-0.10 | one metal jig +-0.03)", d(0.10, 10), d(0.03, 10)),
        ("drive dowel bore in the tray (+-0.10 | jig +-0.03, at R_k)", d(0.10, rk), d(0.03, rk)),
        ("yoke lobe faces vs yoke bore / drive slot (EDM +-0.02)", d(0.02, rc) + d(0.02, rk), d(0.02, rc) + d(0.02, rk)),
        ("drive slot tangential fit (0.01)", d(0.01, rk), d(0.01, rk)),
        ("yoke bore on the bushing (0.05 | H7/g6 0.02 radial)", d(0.05, rc), d(0.02, rc)),
        ("bracket bore clearance: cassette shift 0.05 (index pin at r 10, drive at R_k)", d(0.05, 10) + d(0.05, rk), d(0.05, 10) + d(0.05, rk)),
    ]
    wa, wb = sum(i[1] for i in items), sum(i[2] for i in items)
    ra, rb = math.sqrt(sum(i[1] ** 2 for i in items)), math.sqrt(sum(i[2] ** 2 for i in items))
    k_chain = 1.0 / (1 / 80.0 + 1 / 466.0 + 1 / 9300.0) * 1000.0      # N.mm/rad: pin torsion, dowel foundation, drive
    defl = [math.degrees(t / k_chain) for t in (T_D, 2 * T_D)]
    return items, (wa, ra), (wb, rb), defl, k_chain


def main():
    parts = r1_table()
    env, eparts, pockets, _ = el.evaluate(parts)
    print("D-009 S1-R stop-yoke study (NON-PRODUCTION; modeled in memory; nothing written)")
    assert env["R1_RS"] <= env["R1_RS_TRAY"] + 1e-9
    for k in ("R1_STOP", "R1_PHI1", "R1_PHI2", "R1_FA", "R1_FB", "R1_RH", "R1_RIN", "R1_RS", "R1_RRO", "R1_YX0", "R1_YX1", "R1_SX0",
              "R1_SX1", "R1_LOBEZ", "R1_LW", "R1_ARMZ0", "R1_ARMZ1", "R1_RK", "R1_DZ", "R1_TSP", "R1_TY"):
        print(f"  {k} = {env[k]:.4f}")
    print(f"  hub pin length {env['R1_SX1'] - env['ARX0']:.1f} (D-009 53.5); pin tip double-D X {env['PX0']:g}-{env['R1_SX1']:g}")

    fails = []
    f, rep, _ = s1.regression(eparts, env, pockets)
    fails += f
    print("\nRegression (E2 / D-009 check set on the S1-R table):")
    for line in rep:
        print("  " + line)
    f, rep, _ = s1.stop_sweep(eparts, env, sp_t=SPN, sb_t=YON)
    fails += f
    print("\nHard-stop sweep:")
    for line in rep:
        print("  " + line)
    rep, w = service(eparts, env)
    print("\nService / assembly paths (removal; assembly is the reverse):")
    for line in rep:
        print("  " + line)
    fails += ["service path"] if min(w) < -1e-6 else []

    print("\nLoads (inferred):")
    lines, rc = loads(env)
    for line in lines:
        print("  " + line)
    items, a, b, defl, kc = tolerance(env, rc)
    print(f"\nTolerance stack (stop angle relative to the +-75 index position; 5 deg = {math.radians(5) * rc:.2f} mm at R {rc:.2f}):")
    for name, x, y in items:
        print(f"  +-{x:.2f} | +-{y:.2f}  {name}")
    print(f"  D-009 fits, printed-then-reamed bores: worst +-{a[0]:.2f}, RSS +-{a[1]:.2f} deg")
    print(f"  metal-referenced (tight keys, jig-reamed bores): worst +-{b[0]:.2f}, RSS +-{b[1]:.2f} deg")
    print(f"  chain stiffness ~{kc / 1000:.0f} N.m/rad -> elastic over-travel {defl[0]:.1f} deg at 1.26, {defl[1]:.1f} deg at 2.52 N.m; "
          f"window: first contact >= 75.5 and contact + deflection <= 85 -> -4.5 / +{5 - defl[0]:.1f} deg")
    inertia = 0.35 * ((200 ** 2 + 8 ** 2) / 12 + math.hypot(14.3, 9.5) ** 2) * 1e-6
    print(f"\nImpact sensitivity (I {inertia * 1e6:.0f} kg mm^2): peak T = w sqrt(I k):")
    for kk in (40.0, kc / 1000, 120.0):
        print(f"  k {kk:.0f} N.m/rad: w 2/4/6/8 rad/s -> " + " / ".join(f"{w_ * math.sqrt(inertia * kk):.2f}" for w_ in (2, 4, 6, 8)) + " N.m")
    print("\nS1-R GEOMETRY: " + ("PASS" if not fails else f"FAIL {fails}"))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
