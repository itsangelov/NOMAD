"""D-009 S1 hard-stop feasibility study (NON-PRODUCTION, read-only).

Builds the S1 candidate (variant B: separate stainless stop plate keyed on an extended hub-pin tip + steel stop
block in a pocket under the cassette tray) IN MEMORY on top of the D-009 E-lid model of e_lid_layout.py, then runs
the E2 / D-009 regression, a fine hard-stop sweep, service-path checks, the tolerance stack, the load path at the
design and acceptance torques, an impact sensitivity table, the variant A (formed flange) comparison, and the
transverse-reaction check of the already-approved index lock.

Nothing is written: nomad.yaml, the spec, NOMAD_E_Prototype.fs and the harness are untouched. The S1 inputs below
are STUDY values (proposed names), not approved parameters. Usage: py CAD/tools/s1_stop_study.py
Evidence: geometry modeled (exact 2-D regions extruded along X); loads inferred (hand models of the approved reports).
"""
import math
import sys

import e_lid_layout as el

# ------------------------------------------------------------------ S1 study inputs (proposed; NOT in nomad.yaml)
S1_INPUTS = [
    ("S1_STOP", "80"),                                   # target hard-stop angle, +-, deg
    ("S1_HB", "40"),                                     # stop block half-angle about the tray-normal direction, deg
    ("S1_TSP", "3.0"),                                   # stop plate thickness (3 mm stainless)
    ("S1_LIG", "1.0"),                                   # stop plate hub ligament above the double-D key arc
    ("S1_LOBE", "3.0"),                                  # stop block lobe length along X
    ("S1_EMB", "1.0"),                                   # stop block embedment in the tray pocket
    ("S1_BWE", "4.5"),                                   # embedded part half-width (clear of the index guide bore)
]
S1_DERIVED = [
    ("S1_RH", "KR + S1_LIG"),                            # stop plate hub radius (key R 2.5 + ligament)
    ("S1_RIN", "S1_RH + MIN_GAP"),                       # stop block inner radius (MIN_GAP to the hub ring)
    ("S1_RS", "-BLY / cos(S1_HB + S1_STOP - 90)"),       # stop plate outer radius: corner at the hub-band edge dy = BLY
    ("S1_RS_TRAY", "(TRB - MIN_GAP) / cos(S1_HB)"),      # ... and MIN_GAP below the tray at the stop (must be >= S1_RS)
    ("S1_PHI1", "90 - S1_HB"),                           # stop block faces (cassette frame, tilt 0)
    ("S1_PHI2", "90 + S1_HB"),
    ("S1_FA", "S1_PHI2 + S1_STOP"),                      # stop plate face met at +STOP
    ("S1_FB", "S1_PHI1 - S1_STOP"),                      # stop plate face met at -STOP
    ("S1_FLA", "180 * DEG + asin(-FLZ / S1_RS)"),        # stop plate floor clip (hub-zone floor dz = FLZ)
    ("S1_FLB", "360 * DEG - asin(-FLZ / S1_RS)"),
    ("S1_SX1", "PX1 + S1_TSP"),                          # stop plate outboard face = extended pin tip
    ("S1_BX0", "GX1"),                                   # stop block inboard face = tray groove outboard wall
    ("S1_BX1", "S1_BX0 + S1_LOBE"),
    ("S1_BX2", "GDX1 - MIN_GAP"),                        # stop block tab end (MIN_GAP of tray before the spring channel)
    ("S1_BW", "TRB * tan(S1_HB)"),                       # stop block half-width at the tray bottom
]
el.DERIVED_LOCK += S1_INPUTS + S1_DERIVED                # in-process only (never emitted)

SP, SB = "SOLAR_STOP_PLATE_{}", "SOLAR_STOP_BLOCK_{}"


def s1_prims(side):
    """S1 variant B primitives for one side (right built in the hub frame, left mirrored in X like side_parts)."""
    h = el._Hub(side)
    pt = lambda r, a: (f"{r} * cos({a})", f"{r} * sin({a})")    # noqa: E731
    sp_outline = [h.arc("S1_RH", "S1_FB", "S1_FA"),
                  h.line(pt("S1_RH", "S1_FA"), pt("S1_RS", "S1_FA")),
                  h.arc("S1_RS", "S1_FA", "S1_FLA"),
                  h.line(("S1_RS * cos(S1_FLA)", "FLZ"), ("S1_RS * cos(S1_FLB)", "FLZ")),
                  h.arc("S1_RS", "S1_FLB", "S1_FB + 360 * DEG"),
                  h.line(pt("S1_RS", "S1_FB"), pt("S1_RH", "S1_FB"))]
    lobe = [h.arc("S1_RIN", "S1_PHI1", "S1_PHI2"),
            h.line(pt("S1_RIN", "S1_PHI2"), ("-S1_BW", "TRB")),
            h.line(("-S1_BW", "TRB"), ("-S1_BWE", "TRB")),
            h.line(("-S1_BWE", "TRB"), ("-S1_BWE", "TRB + S1_EMB")),
            h.line(("-S1_BWE", "TRB + S1_EMB"), ("S1_BWE", "TRB + S1_EMB")),
            h.line(("S1_BWE", "TRB + S1_EMB"), ("S1_BWE", "TRB")),
            h.line(("S1_BWE", "TRB"), ("S1_BW", "TRB")),
            h.line(("S1_BW", "TRB"), pt("S1_RIN", "S1_PHI1"))]
    out = {
        "stop_plate": ([el.prof("plate", "PX1", "S1_SX1", sp_outline)], [el.prof("key_hole", "PX1", "S1_SX1", h.key())]),
        "stop_block": ([el.prof("lobe", "S1_BX0", "S1_BX1", lobe),
                        h.box("tab", "S1_BX1", "-S1_BWE", "TRB", "S1_BX2", "S1_BWE", "TRB + S1_EMB")], []),
        "pocket": [h.box("s1_pocket", "S1_BX0", "-S1_BWE", "TRB", "S1_BX2", "S1_BWE", "TRB + S1_EMB")],
        "pin_tip": [el.prof("key_tip", "PX0", "S1_SX1", h.key())],
        "screw_tip": [h.cyl("washer", "0", "0", "SOLAR_HUB_WASHER_DIAMETER", "S1_SX1", "S1_SX1 + SOLAR_HUB_WASHER_THICKNESS"),
                      h.cyl("head", "0", "0", "SOLAR_HUB_SCREW_HEAD_DIAMETER", "S1_SX1 + SOLAR_HUB_WASHER_THICKNESS",
                            "S1_SX1 + SOLAR_HUB_WASHER_THICKNESS + SOLAR_HUB_SCREW_HEAD_HEIGHT")],
    }
    if side < 0:
        out = {k: ((el.mirror(v[0]), el.mirror(v[1])) if isinstance(v, tuple) else el.mirror(v)) for k, v in out.items()}
    return out


def s1_table():
    """The D-009 part table with S1 variant B: pin tip extended, tip screw moved outboard, stop plate + stop block
    added, stop-block pocket cut in the cassette tray."""
    out = []
    add = {}
    for side in (1, -1):
        s = "R" if side > 0 else "L"
        add[s] = s1_prims(side)
    for n, disp, g, key, a, sub in el.PARTS:
        s = n[-1]
        if n == f"SOLAR_HUB_PIN_{s}":
            a = [p for p in a if p[1] != "key_tip"] + add[s]["pin_tip"]
        elif n == f"SOLAR_HUB_SCREW_TIP_{s}":
            a = add[s]["screw_tip"]
        elif n == f"SOLAR_CASSETTE_{s}":
            sub = list(sub) + add[s]["pocket"]
        out.append((n, disp, g, key, a, sub))
        if n == f"SOLAR_INDEX_PLATE_{s}":
            out.append((SP.format(s), f"{SP.format(s)} [S1 STUDY: 3 stainless stop plate]", f"car{s}", "stainless", *add[s]["stop_plate"]))
        if n == f"SOLAR_CASSETTE_{s}":
            out.append((SB.format(s), f"{SB.format(s)} [S1 STUDY: steel stop block]", f"cas{s}", "stainless", *add[s]["stop_block"]))
    return out


for _s in "RL":
    el.GUIDED[frozenset((SP.format(_s), SB.format(_s)))] = 0.0                                   # designed stop pair
    el.GUIDED[frozenset((SB.format(_s), f"SOLAR_INDEX_PLATE_{_s}"))] = el.P["SOLAR_INDEX_GROOVE_CLEARANCE"]  # axial, like the groove


# ------------------------------------------------------------------ geometry checks
def regression(parts, env, pockets):
    """The e_lid_layout main() check set on the S1 table (no file output). Returns (fails, lines)."""
    grp = el.groups(parts)
    fails, rep = [], []
    base = el.base_prisms(pockets)
    pr0 = el.pose(parts, env)
    rb = el.rigid_group_checks(parts, pr0)
    rep.append(f"rigid groups (structure must not overlap): {rb or 'ok'}")
    fails += ["rigid overlap"] if rb else []
    lids, tilts = [0.0, 105.0, 120.0, 135.0], [0, 15, -15, 30, -30, 45, -45, 60, -60, 75, -75]
    exts = {"stowed": (0, 0), "R deployed": (1, 0), "L deployed": (0, 1), "both deployed": (1, 1)}
    unexpected, fits = set(), {}
    for lid in lids:
        for label, e in exts.items():
            v, k, _ = el.moving_pairs_check(el.pose(parts, env, lid, e), grp, fast=True)
            unexpected |= {(lid, label, 0) + x for x in v}
            for a, b, c in k:
                fits[(a, b)] = min(fits.get((a, b), math.inf), c)
        for t in tilts:
            for tt in ((t, t), (t, -t)):
                v, k, _ = el.moving_pairs_check(el.pose(parts, env, lid, (1, 1), tt), grp, fast=True)
                unexpected |= {(lid, tt) + x for x in v}
                for a, b, c in k:
                    fits[(a, b)] = min(fits.get((a, b), math.inf), c)
    for side in (0, 1):
        for other in (0, 1):
            for i in range(21):
                e = [0.0, 0.0]
                e[side], e[1 - side] = i / 20, other
                v, _, _ = el.moving_pairs_check(el.pose(parts, env, 105.0, tuple(e)), grp, fast=True)
                unexpected |= {(105.0, f"slide {e}") + x for x in v}
    rep.append(f"moving-part checks (lid 0/105/120/135 x stowed / R / L / both; tilts +-75 step 15; slides 0..1): "
               f"{len(unexpected)} unexpected violations" + (f" e.g. {sorted(unexpected, key=str)[:4]}" if unexpected else ""))
    fails += ["moving-part violations"] if unexpected else []
    fitmin = {}
    for (a, b), c in fits.items():
        k = " / ".join(sorted(x[:-2] for x in (a, b)))
        fitmin[k] = min(fitmin.get(k, math.inf), c)
    rep.append("guided / running fits (min over the pose matrix): " + "; ".join(f"{k} {v:.3f}" for k, v in sorted(fitmin.items())))
    bf = el.bracket_floor_sweep(parts, pr0, env)
    rep.append(f"F3 bracket vs rail floor over the full travel: {bf:.3f}")
    fails += ["F3 bracket-floor"] if bf < el.MIN_GAP - el.EPS else []
    lf, lrep = el.lock_checks(parts, env, grp, pr0)
    for line in lrep:
        if line.startswith("B "):
            line = line.split(" -> no geometric hard stop")[0] + " (step 2.5; the S1 stop itself is resolved by the fine sweep below)"
        rep.append("D-009 " + line)
    fails += lf
    worst, plug, lvb = (math.inf, None), {}, 0
    for a10 in range(0, 1351, 10):
        lid = a10 / 10
        pr = el.pose(parts, env, lid)
        v, pl = el.lid_vs_base(pr, grp, base, fast=True)
        lvb += len(v)
        plug[lid] = min(c for _, _, c in pl)
    rep.append(f"lid sweep 0..135 step 1 vs base: {'no violations' if not lvb else f'{lvb} violations'}; rear-plug clearance at 135 "
               f"{plug[135.0]:.3f} (known OPEN CONFLICT, unchanged)")
    fails += ["lid-base"] if lvb else []
    return fails, rep, pr0


def _pose_side(parts, env, s, lid, a):
    return el.pose(parts, env, lid, (1, 1), (a, 0.0) if s == "R" else (0.0, a))


def stop_sweep(parts, env, step=0.5, sp_t=None, sb_t=None):
    """Retracted index pin; each side, lid 105 and 135, tilt 0 -> +-90. Exact first-contact angle of the stop pair
    (bisection), any other violation before it, stop-pair gap at +-75, and the minimum clearance of the stop plate /
    stop block to every other part over 0..stop. Returns (fails, lines, contact angles)."""
    prt = el.retracted(parts, env)
    grp = el.groups(parts)
    others = [n for n, *_ in parts if grp[n] in ("lid", "baseHinge")]
    fails, rep, angles, mins, pre = [], [], {}, {}, []
    for s in "RL":
        names = [n for n, *_ in parts if n.endswith("_" + s) and grp[n] in ("car" + s, "cas" + s)] + others
        sp, sb = (sp_t or SP).format(s), (sb_t or SB).format(s)
        for lid in (105.0, 135.0):
            for d in (1, -1):
                prev, found, before = 0.0, None, []
                a = 0.0
                while a <= 90.0 + 1e-9:
                    pr = _pose_side(prt, env, s, lid, d * a)
                    c = el.clear(pr[sp], pr[sb])
                    if c < -1e-9:
                        lo, hi = prev, a
                        for _ in range(40):
                            mid = (lo + hi) / 2
                            pm = _pose_side(prt, env, s, lid, d * mid)
                            (lo, hi) = (mid, hi) if el.clear(pm[sp], pm[sb]) >= -1e-12 else (lo, mid)
                        found = lo
                        break
                    v, _, _ = el.moving_pairs_check(pr, grp, names, fast=True)
                    before += [(d * a,) + x for x in v]
                    for p in (sp, sb):
                        for q in names:
                            if q in (sp, sb) or grp[q] == grp[p]:
                                continue
                            cc = el.clear(pr[p], pr[q], 6.0)
                            key = (p[:-2], q[:-2] if q.endswith(("_R", "_L")) else q)
                            mins[key] = min(mins.get(key, math.inf), cc)
                    prev = a
                    a = round(a + step, 6)
                angles[(s, lid, d)] = found
                pre += before
                if found is None or before:
                    fails.append(f"stop sweep {s} lid {lid} dir {d:+d}: contact {found}, earlier violations {before[:3]}")
        for d in (1, -1):
            pr = _pose_side(prt, env, s, 105.0, d * env["SOLAR_INDEX_RANGE"])
            angles[(s, "gap75", d)] = el.clear(pr[sp], pr[sb])
    rep.append(f"hard-stop contact angle ({(sp_t or SP)[:-3]} vs {(sb_t or SB)[:-3]}, first contact by bisection; retracted pin): " +
               "; ".join(f"{s} lid {lid:g} {'+' if d > 0 else '-'}: {angles[(s, lid, d)]:.4f}" for s in "RL" for lid in (105.0, 135.0) for d in (1, -1)))
    rep.append("violations of any other pair before the stop (0.5 deg steps, both sides, both directions, lid 105/135): "
               + ("none" if not pre else f"{len(pre)}, e.g. {pre[:4]}"))
    rep.append("stop-pair gap at the last index position +-{:g} (lid 105): ".format(env["SOLAR_INDEX_RANGE"]) +
               ", ".join(f"{s}{'+' if d > 0 else '-'} {angles[(s, 'gap75', d)]:.3f}" for s in "RL" for d in (1, -1)))
    rows = sorted(mins.items(), key=lambda kv: kv[1])
    rep.append("minimum clearance over 0..stop, both sides (stop plate / stop block vs other groups; >= 6 shown as 6+): " +
               "; ".join(f"{a} x {b} {'6+' if c >= 6 else f'{c:.3f}'}" for (a, b), c in rows))
    return fails, rep, angles


def service_paths(parts, env):
    """(1) stop plate slid off the extended tip (+X, tilt 0) past the stop block; (2) cassette group together with the
    index plate slid off the pin (+X) after the tip screw and stop plate are removed; (3) stop block out of its
    pocket (-Z, cassette removed)."""
    pr0 = el.pose(parts, env)
    grp = el.groups(parts)
    rep = []
    s = "R"
    sp = pr0[SP.format(s)]
    cas_names = [n for n in pr0 if grp[n] == "cas" + s]
    w1 = min(el.clear(el._sx(sp, i / 4), pr0[n]) for i in range(0, 81) for n in cas_names)
    rep.append(f"S1 service (1): stop plate off the pin tip, +X 0..20 mm at tilt 0, min clearance to the cassette group {w1:.3f}")
    moving = cas_names + [f"SOLAR_INDEX_PLATE_{s}"]
    fixed = [f"SOLAR_HUB_PIN_{s}", f"SOLAR_CARRIAGE_{s}", f"SOLAR_ANTIROT_PLATE_{s}", f"SOLAR_ANTIROT_DOWEL_{s}",
             f"SOLAR_HUB_SCREW_IN_{s}", f"SOLAR_RAIL_{s}", "LID_FRAME"]
    ext = el.pose(parts, env, 105.0, (1, 0))
    w2 = min(el.clear(el._sx(ext[m], i / 2), ext[f]) for i in range(0, 121) for m in moving for f in fixed)
    rep.append(f"S1 service (2): deployed, cassette + index plate (in its groove) slid +X 0..60 mm off the pin after removing "
               f"the tip screw and stop plate; min clearance to pin / carriage / rail / lid {w2:.3f} (0 = sliding fits: bore and key)")
    sb = pr0[SB.format(s)]
    cas = pr0[f"SOLAR_CASSETTE_{s}"]
    w3 = el.clear(sb, cas)
    rep.append(f"S1 service (3): stop block seats in an open pocket in the tray bottom (touching {w3:.3f}); the pocket is open "
               f"downward, so the block drops out -Z once its two screws are removed (cassette off the pin)")
    return rep, (w1, w2)


# ------------------------------------------------------------------ loads (inferred)
T_H, T_D = 630.0, 1260.0                 # N.mm (approved load basis)
SY = {"303": 415.0, "301h": 758.0, "17-4 H1150": 725.0, "17-4 H1025": 1000.0, "17-4 H900": 1170.0}
PETG = {"RT": 30.0, "hot": 15.0}
Z_ROUND, ZP_ROUND = math.pi * 5 ** 3 / 32, math.pi * 5 ** 3 / 16
Z_DD, ZT_DD = 6.6, 12.9                  # double-D A/F 3.0, anti-rotation check s.5.1 (numerical)
M_CORNER, M_GRAV = 795.0, 293.0          # handling moment parts at the pin root (hub load check s.4): 5 N x 159, 3.43 N x 85.25
MB_CORNER, MB_GRAV = 712.5, 236.0        # at the bracket bore mid-length: 5 x 142.5, 3.43 x 68.75
BORE_D, BORE_L, BORE_XC = 5.0, 10.0, 5.5  # hub bracket bore (X 0.5-10.5)


def vm(s, t):
    return math.sqrt(s * s + 3 * t * t)


def combine(m_corner, m_grav, m_c, cosang):
    """Worst in-plane sum of the handling corner moment (along +-panel normal), gravity (any direction) and a
    reaction couple m_c whose force makes angle acos(cosang) with the panel normal."""
    return math.sqrt(m_corner ** 2 + m_c ** 2 + 2 * m_corner * m_c * abs(cosang)) + m_grav


def bore_p(v, m):
    return v / (BORE_D * BORE_L) + 6 * m / (BORE_D * BORE_L ** 2)


def loads(env, rc, xc):
    lines = []
    tsp = env["S1_TSP"]
    wf = 2 * math.sqrt(2.5 ** 2 - (2.5 - (5 - env["SOLAR_HUB_PIN_KEY_ACROSS_FLATS"]) / 2) ** 2)
    rs, rin, rh = env["S1_RS"], env["S1_RIN"], env["S1_RH"]
    lc = min(env["S1_SX1"], env["S1_BX1"]) - max(env["PX1"], env["S1_BX0"])      # axial contact length
    # angle between the stop force on the pin side and the panel normal at the stop: plate face at PHI2 + STOP, force
    # tangential there (direction PHI2 + STOP + 90); panel normal at 90 + STOP -> angle PHI2 (and PHI1 at -STOP)
    cos_stop = abs(math.cos(math.radians(env["S1_PHI2"])))
    cos_lock = abs(math.cos(math.radians(env["SOLAR_INDEX_PIN_ANGLE"])))
    lines.append(f"inputs: contact band R {rin:.3f}..{rs:.3f} (centroid {rc:.3f}), axial contact {lc:.2f} (X {max(env['PX1'], env['S1_BX0']):g}.."
                 f"{min(env['S1_SX1'], env['S1_BX1']):g}, centre {xc:g}); bracket bore centre X {BORE_XC}; |cos(stop force, panel normal)| "
                 f"{cos_stop:.3f}; index lock {cos_lock:.3f}")
    res = {}
    for tag, k in (("T_d 1.26", 1.0), ("T_acc 2.52", 2.0)):
        T = T_D * k
        F = T / rc
        r = {}
        r["contact flat (aligned)"] = (F / (lc * (rs - rin)), None, "")
        for rcrown in (5.0, 10.0):
            estar = 193000.0 / (2 * (1 - 0.3 ** 2))
            r[f"contact crowned R{rcrown:g} (Hertz line)"] = (math.sqrt((F / lc) * estar / (math.pi * rcrown)), None, "")
        r["stop plate key A/F 3.0 (t 3)"] = (6 * T / (tsp * wf * wf), SY["301h"], "301 1/2-hard")
        r["stop plate sector shear"] = (F / (tsp * (rs - rh)), 0.58 * SY["301h"], "301 1/2-hard (shear yield)")
        m_tip = F * (xc - env["PX0"])
        r["pin tip double-D at X 11 (bending + torsion)"] = (vm(m_tip / Z_DD, T / ZT_DD), SY["303"], "303")
        m_c = F * (xc - BORE_XC)
        r["pin root, stop couple only"] = (vm(m_c / Z_ROUND, T / ZP_ROUND), SY["303"], "303")
        mr = combine(k * 2 * M_CORNER, k * 2 * M_GRAV, m_c, cos_stop)
        r["pin root, stop couple + design handling bending"] = (vm(mr / Z_ROUND, T / ZP_ROUND), SY["303"], "303")
        r["bracket bore PETG, stop only"] = (bore_p(F, m_c), PETG["RT"], "PETG RT")
        mb = combine(k * 2 * MB_CORNER, k * 2 * MB_GRAV, m_c, cos_stop)
        r["bracket bore PETG, stop + design handling"] = (bore_p(F + k * 2 * 8.43, mb), PETG["RT"], "PETG RT")
        fy = F * math.sin(math.radians(env["S1_PHI2"]))
        r["stop block -> tray: 2 x M2 insert bearing (OD 3.2 x 4)"] = (fy / (2 * 3.2 * 4.0), PETG["RT"], "PETG RT (hot: /2)")
        r["stop block -> tray: 1 mm pocket wall only"] = (fy / (1.0 * (env["S1_BX2"] - env["S1_BX0"])), PETG["RT"], "PETG RT")
        r["anti-rotation plate key (unchanged path)"] = (6 * T / (1.5 * wf * wf), SY["301h"], "301 1/2-hard")
        r["pin inboard double-D torsion (unchanged path)"] = (vm(0, T / ZT_DD), SY["303"], "303")
        r["carriage dowel bearing, bound (unchanged path)"] = (12.7 * k, PETG["RT"], "PETG RT (hot: /2)")
        res[tag] = (F, r)
        lines.append(f"-- {tag} N.m: stop force F = T / R = {F:.0f} N")
        for name, (sig, allow, mat) in r.items():
            sf = f"SF {allow / sig:.2f} ({mat})" if allow else ""
            lines.append(f"   {name}: {sig:.1f} MPa {sf}")
    return lines, res


def lock_couple(env):
    """Transverse reaction of the APPROVED index lock (pre-existing D-009 item): index pin force F = T / r at the plate
    (X PX0..PX1) is reacted by the bracket bore -> extra couple at the pin root and moment on the bore."""
    xc = (env["PX0"] + env["PX1"]) / 2
    cosl = abs(math.cos(math.radians(env["SOLAR_INDEX_PIN_ANGLE"])))
    out = []
    for tag, k, T in (("handling 0.63", 0.5, T_H), ("design 1.26", 1.0, T_D)):
        F = T / env["SOLAR_INDEX_RADIUS"]
        m_c = F * (xc - BORE_XC)
        mr0 = k * 2 * (M_CORNER + M_GRAV)
        mr = combine(k * 2 * M_CORNER, k * 2 * M_GRAV, m_c, cosl)
        root0, root = vm(mr0 / Z_ROUND, T / ZP_ROUND), vm(mr / Z_ROUND, T / ZP_ROUND)
        b0 = bore_p(k * 2 * 8.43, k * 2 * (MB_CORNER + MB_GRAV))
        b = bore_p(F + k * 2 * 8.43, combine(k * 2 * MB_CORNER, k * 2 * MB_GRAV, m_c, cosl))
        out.append(f"{tag} N.m: index force {F:.0f} N at X {xc:g}, couple {m_c:.0f} N.mm; pin root vM {root0:.0f} -> {root:.0f} MPa "
                   f"(303 SF {SY['303'] / root0:.2f} -> {SY['303'] / root:.2f}); bracket bore peak {b0:.1f} -> {b:.1f} MPa "
                   f"(PETG RT SF {30 / b0:.2f} -> {30 / b:.2f})")
    return out


def tolerance(env, rc):
    """Stop angle relative to the +-75 index position (both are set by different parts): worst case and RSS, deg."""
    r10 = env["SOLAR_INDEX_RADIUS"]
    wf = 2 * math.sqrt(2.5 ** 2 - (2.5 - (5 - env["SOLAR_HUB_PIN_KEY_ACROSS_FLATS"]) / 2) ** 2)
    key = math.degrees(0.04 / wf)
    d = lambda mm, r: math.degrees(mm / r)            # noqa: E731
    items = [
        ("stop plate face vs its key (laser +-0.10 | wire EDM / CNC +-0.02)", d(0.10, rc), d(0.02, rc)),
        ("stop plate key clocking on the pin (A/F clearance <= 0.04)", key, key),
        ("index plate key clocking on the pin (same)", key, key),
        ("index hole true position (dia 0.06 -> +-0.03 at r 10)", d(0.03, r10), d(0.03, r10)),
        ("index pin in its hole (0.05 radial at r 10)", d(0.05, r10), d(0.05, r10)),
        ("index pin bores in the printed tray vs bracket bore (+-0.10 at r 10)", d(0.10, r10), d(0.10, r10)),
        ("stop block face vs bracket bore: FDM-located (+-0.20 + 0.05) | metal-referenced (+-0.05 + 0.05)", d(0.25, rc), d(0.10, rc)),
        ("PETG shrink / scale on the pocket-to-bore distance (0.5 % of 5 mm)", d(0.025, rc), 0.0),
        ("bracket bore clearance on the pin (0.05 radial: stop face + index pin)", d(0.05, rc) + d(0.05, r10), d(0.05, rc) + d(0.05, r10)),
    ]
    wc_a, wc_b = sum(a for _, a, _ in items), sum(b for _, _, b in items)
    rs_a, rs_b = math.sqrt(sum(a * a for _, a, _ in items)), math.sqrt(sum(b * b for _, _, b in items))
    k_chain = 52.0e3                                  # N.mm/rad (see the report: pin torsion, dowel, block interface in series)
    defl = [math.degrees(t / k_chain) for t in (T_D, 2 * T_D)]
    return items, (wc_a, rs_a), (wc_b, rs_b), defl


def impact():
    m, h, t, dcg = 0.35, 200.0, 8.0, math.hypot(14.3, 9.5)
    inertia = m * ((h * h + t * t) / 12 + dcg * dcg) * 1e-6          # kg m^2
    rows = []
    for k in (25.0, 52.0, 100.0):                                      # N m / rad
        rows.append((k, [w * math.sqrt(inertia * k) for w in (2.0, 4.0, 6.0, 8.0)]))
    return inertia, rows


def main():
    parts = s1_table()
    env, eparts, pockets, _ = el.evaluate(parts)
    print("D-009 S1 hard-stop study (NON-PRODUCTION; variant B modeled in memory; nothing written)")
    assert env["S1_RS"] <= env["S1_RS_TRAY"] + 1e-9, "stop plate radius exceeds the tray MIN_GAP limit"
    rc = (env["S1_RIN"] + env["S1_RS"]) / 2
    xc = (max(env["PX1"], env["S1_BX0"]) + min(env["S1_SX1"], env["S1_BX1"])) / 2
    print("\nS1 geometry (right side; X stowed, dy/dz from the tilt axis):")
    for k in ("S1_STOP", "S1_HB", "S1_PHI1", "S1_PHI2", "S1_FA", "S1_FB", "S1_TSP", "S1_RH", "S1_RIN", "S1_RS", "S1_RS_TRAY",
              "S1_FLA", "S1_FLB", "PX1", "S1_SX1", "S1_BX0", "S1_BX1", "S1_BX2", "S1_BW", "S1_BWE", "S1_EMB", "TRB", "FLZ", "BLY"):
        print(f"  {k} = {env[k]:.4f}")
    print(f"  hub pin length {env['S1_SX1'] - env['ARX0']:.1f} (was {env['PX1'] - env['ARX0']:.1f}); contact centroid R {rc:.3f}, X {xc:g}")

    fails = []
    f, rep, pr0 = regression(eparts, env, pockets)
    fails += f
    print("\nRegression (E2 / D-009 check set on the S1 table):")
    for line in rep:
        print("  " + line)
    f, rep, ang = stop_sweep(eparts, env)
    fails += f
    print("\nHard-stop sweep:")
    for line in rep:
        print("  " + line)
    rep, _ = service_paths(eparts, env)
    print("\nService / assembly paths:")
    for line in rep:
        print("  " + line)

    print("\nTolerance stack (stop angle relative to the +-75 index position; nominal margin 5 deg = "
          f"{math.radians(5) * rc:.2f} mm at R {rc:.2f}):")
    items, a, b, defl = tolerance(env, rc)
    for name, x, y in items:
        print(f"  +-{x:.2f} | +-{y:.2f}  {name}")
    print(f"  as modeled (laser plate, FDM-located block): worst +-{a[0]:.2f}, RSS +-{a[1]:.2f} deg")
    print(f"  improved (EDM/CNC plate, metal-referenced block): worst +-{b[0]:.2f}, RSS +-{b[1]:.2f} deg")
    print(f"  elastic over-travel under load (chain ~52 N.m/rad): {defl[0]:.1f} deg at 1.26, {defl[1]:.1f} deg at 2.52 N.m")
    print("  window (assumed): first contact >= 75.5 (index pin seats, no preload at +-75) and contact + deflection <= 85 "
          f"-> error allowed -4.5 / +{85 - 80 - defl[0]:.1f} deg at 1.26 N.m")

    print("\nLoads (inferred; approved models; SF = allowable / stress):")
    lines, res = loads(env, rc, xc)
    for line in lines:
        print("  " + line)
    print("\nApproved index lock, transverse reaction (pre-existing D-009 item, not caused by S1):")
    for line in lock_couple(env):
        print("  " + line)
    inertia, rows = impact()
    print(f"\nImpact sensitivity: cassette inertia about the tilt axis {inertia * 1e6:.0f} kg mm^2 (0.35 kg envelope); peak torque "
          "T = w * sqrt(I k) for a rigid cassette into a linear stop:")
    for k, ts in rows:
        print(f"  k {k:g} N.m/rad: w 2/4/6/8 rad/s -> " + " / ".join(f"{t:.2f}" for t in ts) + " N.m")
    print("\nS1 VARIANT B GEOMETRY: " + ("PASS" if not fails else f"FAIL {fails}"))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
