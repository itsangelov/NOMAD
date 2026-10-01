"""P0.2 physical risk coupon package: new geometry (sandwich plates + two small fixtures) and expected values.

The P0.2 package REUSES the P0.1 coupons unchanged (rails A1/A2, pad stub, carriage, display surrogate,
load platform, B frame, B1 plate, load pad; see CAD/coupons/P0.1/). This tool only adds what P0.1 lacks:

  B_S30_sandwich          sandwich plate, 2 interior webs (bays ~27.9 = the bridge the inner skin must span)
  B_S20_sandwich          sandwich plate, 3 interior webs (bays ~20.4)
  B_INFILL_plate          solid-envelope plate; its core is made by slicer infill (settings in the test plan)
  B_clearance_block_2p0   reference block, top 2.0 below the plate seat (D.1 cassette-back gap)
  B_load_bar              full-width line-load spreader at mid-span

All new plates use the P0.1 B frame (230 x 90, 202 clear span, 14 mm bands, M3 inserts at (7/223, 10/80)).
Machinery (CSG, STL/SCAD writer, watertight checks) is imported from CAD/coupons/P0.1/generate_coupons.py.

  py CAD/tools/generate_p02_coupons.py                     # write CAD/coupons/P0.2/{stl,scad}, checks, expected values
  py CAD/tools/generate_p02_coupons.py --expect            # expected values only (no files written)
  py CAD/tools/generate_p02_coupons.py --expect --E 1700 --strip steel,1.5,10.0

Evidence levels: geometry = modeled; expected values = analytical screening (beam formulas, NOT FEA) with
nominal PETG E = 2000 MPa; bounds for the single-strip asymmetry, bridged-skin knockdown and infill-core
shear are inferred. Nothing here is physically tested. Study values are provisional; nomad.yaml is untouched.
"""

import argparse
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "coupons" / "P0.1"))
import generate_coupons as g  # noqa: E402

OUT = ROOT / "coupons" / "P0.2"
RHO = 1.27e-3                  # g/mm^3 PETG (solid)
NU = 0.37

# ------------------------------------------------------------------ sandwich plate parameters (provisional)
L_PLATE = g.SPAN + 2 * g.BAND          # 230, same as P0.1 B plates
W_PLATE = g.STRIP_WIDTH                # 90
SKIN, CORE = 1.2, 4.2                  # D.1 class A nominal: 1.2 / 4.2 / 1.2 = 6.6 (6 + 21 + 6 layers at 0.2)
T_PLATE = 2 * SKIN + CORE
WEB_T, EDGE_T = 2.0, 1.2               # interior webs; edge closures (make the outer bays printable)
INTERIOR_WEBS = {"S30": 2, "S20": 3}   # -> equal bays of 27.9 and 20.4 (NOMAD targets 28 and 18)
BLOCK_2P0 = (60.0, 60.0, g.SHELF_H - 2.0)   # 8.0 tall: top 2.0 below the plate seat
LOAD_BAR = (20.0, W_PLATE, 8.0)        # X (along span) x Y (full width) x Z
BEDS = {"B": (235.0, 95.0)}


def bays(n):
    """Interior web Y-intervals and the bay (bridge) width for n interior webs."""
    bay = (W_PLATE - 2 * EDGE_T - n * WEB_T) / (n + 1)
    cells, webs, y = [], [], EDGE_T
    for i in range(n + 1):
        cells.append((y, y + bay))
        y += bay
        if i < n:
            webs.append((y, y + WEB_T))
            y += WEB_T
    return webs, cells, bay


def holes():
    return [g.cylz(x, y, g.SCREW_CLEAR_D, -1, T_PLATE + 1) for x, y in g.b_screw_xy()]


def sandwich(kind):
    """Print orientation: OUTER skin on the bed (Z 0-1.2), core Z 1.2-5.4, INNER skin Z 5.4-6.6 bridges the cells.
    Cells are closed voids over the span X 14-216 only; the end bands X 0-14 / 216-230 are solid (screw zones)."""
    _, cells, bay = bays(INTERIOR_WEBS[kind])
    subs = [g.box(g.BAND, y0, SKIN, g.BAND + g.SPAN, y1, SKIN + CORE) for y0, y1 in cells] + holes()
    return g.Part(f"B_{kind}_sandwich", "B", [g.box(0, 0, 0, L_PLATE, W_PLATE, T_PLATE)], subs,
                  f"TEST: sandwich stiffness + bridged inner skin (bays {bay:.1f}); outer skin on bed")


def infill_plate():
    return g.Part("B_INFILL_plate", "B", [g.box(0, 0, 0, L_PLATE, W_PLATE, T_PLATE)], holes(),
                  "TEST: slicer-infill core sandwich (geometry = envelope; core from slicer settings)")


def new_parts():
    return [sandwich("S30"), sandwich("S20"), infill_plate(),
            g.simple("B_clearance_block_2p0", "B", BLOCK_2P0, "TEST: 8.0 height (2.0 mm reference gap = D.1 cassette-back gap)"),
            g.simple("B_load_bar", "B", LOAD_BAR, "FIXTURE: full-width line load at mid-span")]


def probes(parts):
    by = {p.name: p for p in parts}
    out = []
    for kind in ("S30", "S20"):
        p = by[f"B_{kind}_sandwich"]
        webs, cells, bay = bays(INTERIOR_WEBS[kind])
        yc = (cells[0][0] + cells[0][1]) / 2
        out += [
            (f"{kind}: cell void at mid-core, outer and inner skins solid above/below it",
             not p.solid((115, yc, SKIN + CORE / 2)) and p.solid((115, yc, SKIN / 2)) and p.solid((115, yc, T_PLATE - SKIN / 2))),
            (f"{kind}: cells closed (solid end bands, edge closures, both skins)",
             all(p.solid(pt) for pt in [(g.BAND - 0.05, yc, 3), (g.BAND + g.SPAN + 0.05, yc, 3), (115, EDGE_T - 0.05, 3),
                                        (115, W_PLATE - EDGE_T + 0.05, 3), (115, yc, SKIN - 0.05), (115, yc, SKIN + CORE + 0.05)])),
            (f"{kind}: interior webs solid through the core ({len(webs)} x {WEB_T:g})",
             all(p.solid((115, (a + b) / 2, SKIN + CORE / 2)) for a, b in webs)),
            (f"{kind}: bridge (bay) width {bay:.2f}", bay > 0 and all(abs((c1 - c0) - bay) < 1e-9 for c0, c1 in cells)),
            (f"{kind}: end bands solid at the screw zone", p.solid((5, 45, 3)) and p.solid((225, 45, 3))),
        ]
    for name in ("B_S30_sandwich", "B_S20_sandwich", "B_INFILL_plate"):
        p = by[name]
        out.append((f"{name}: 4 clearance holes on the P0.1 B-frame insert pattern (X 7/223, Y 10/80)",
                    all(not p.solid((x, y, 3)) and p.solid((x + 3, y, 3)) for x, y in g.b_screw_xy())))
    out += [
        ("layer alignment: skins and core are multiples of 0.2", all(abs(v / 0.2 - round(v / 0.2)) < 1e-9 for v in (SKIN, CORE))),
        ("S30 bay >= 27.5 (NOMAD S30 bridge 28) and S20 bay <= 21 (NOMAD S20 bridge 18)",
         27.5 <= bays(2)[2] <= 28.5 and bays(3)[2] <= 21.0),
        ("2.0 block: top 2.0 below the plate seat on the P0.1 B frame",
         abs((g.FRAME_BASE_T + g.SHELF_H) - (g.FRAME_BASE_T + BLOCK_2P0[2]) - 2.0) < 1e-9),
        ("load bar spans the full plate width", abs(LOAD_BAR[1] - W_PLATE) < 1e-9),
    ]
    return out


def write_parts(parts):
    (OUT / "stl").mkdir(parents=True, exist_ok=True)
    (OUT / "scad").mkdir(parents=True, exist_ok=True)
    ok_all = True
    vols = {}
    print(f"{'part':<24} {'bbox X x Y x Z (mm)':<24} {'tris':>7} {'bad edges':>9} {'comps':>5} {'vol cm3':>8}  bed")
    for p in parts:
        tris, solid, _ = g.mesh(p)
        bad, degen, vol = g.manifold_report(tris)
        comps = g.components(solid)
        b = p.bbox()
        dims = (b[3] - b[0], b[4] - b[1], b[5] - b[2])
        bed = BEDS[p.family]
        fits = (dims[0] <= bed[0] and dims[1] <= bed[1]) or (dims[1] <= bed[0] and dims[0] <= bed[1])
        ok = bad == 0 and degen == 0 and comps == 1 and fits
        ok_all &= ok
        g.write_stl(OUT / "stl" / f"{p.name}.stl", tris)
        (OUT / "scad" / f"{p.name}.scad").write_text(g.scad(p).replace("generate_coupons.py", "generate_p02_coupons.py"), encoding="utf-8")
        vols[p.name] = vol / 1000
        print(f"{p.name:<24} {dims[0]:>6.1f} x {dims[1]:>5.1f} x {dims[2]:>5.1f}   {len(tris):>7} {bad:>9} {comps:>5} {vol / 1000:>8.2f}  "
              f"{'OK' if fits else 'TOO BIG'} ({bed[0]:g}x{bed[1]:g})")
    print("\ngeometry probes:")
    for label, res in probes(parts):
        ok_all &= bool(res)
        print(f"  [{'PASS' if res else 'FAIL'}] {label}")
    return ok_all, vols


# ------------------------------------------------------------------ expected values: rail (coupon A)
STRIPS = {"al": 69000.0, "steel": 200000.0}
ARM = g.RAIL_CHANNEL_LEN - g.CAR_LEN / 2 - g.PAD_LEN          # 149.5 pad edge -> stowed carriage centre
STATIONS = {30: 1.5, 100: 71.5, 150: 121.5, 178: 149.5, 196: 167.5}   # rail X -> distance from the pad edge


def rail_rects(walls, slotted=(False, False), strips=None, strip_dims=None):
    """Rail cross-section rectangles (y0, y1, z0, z1, E). y = 0 at the ear-side (corridor-side) outer face."""
    e = g_e()
    wa, wb = walls
    w = g.CH_W + wa + wb
    lip_in = (g.CH_W - g.SLOT_W) / 2
    r = [(0, w, 0, g.FLOOR, e), (0, wa, g.FLOOR, g.FLOOR + g.CH_H, e), (w - wb, w, g.FLOOR, g.FLOOR + g.CH_H, e),
         (0, wa + lip_in, g.RAIL_H - g.LIP_T, g.RAIL_H, e), (w - wb - lip_in, w, g.RAIL_H - g.LIP_T, g.RAIL_H, e)]
    st, sh = g.STRIP_T + g.STRIP_CLR_T, g.STRIP_H + g.STRIP_CLR_H
    for side, (y0, wall) in enumerate(((0.0, wa), (w - wb, wb))):
        if slotted[side]:
            ys = y0 + (wall - st) / 2
            r.append((ys, ys + st, g.STRIP_Z0, g.STRIP_Z0 + sh, -e))
            if strips and strips[side]:
                es, t, h = strips[side]
                yc = ys + st / 2
                r.append((yc - t / 2, yc + t / 2, g.STRIP_Z0, g.STRIP_Z0 + h, es))     # shimmed: sits on the slot floor
    return r, w


def ei_of(rects, ylo=-1e9, yhi=1e9):
    parts = []
    for y0, y1, z0, z1, e in rects:
        a, b = max(y0, ylo), min(y1, yhi)
        if b > a:
            parts.append((b - a, z1 - z0, (z0 + z1) / 2, e))
    ea = sum(e * bb * t for bb, t, _, e in parts)
    zb = sum(e * bb * t * z for bb, t, z, e in parts) / ea
    return sum(e * (bb * t ** 3 / 12 + bb * t * (z - zb) ** 2) for bb, t, z, e in parts)


def cantilever(ei, mass_kg, x):
    p = mass_kg * 9.81
    a = ARM
    if x <= a:
        return p * x * x * (3 * a - x) / (6 * ei)
    return p * a ** 3 / (3 * ei) + p * a * a / (2 * ei) * (x - a)


_E = [2000.0]


def g_e():
    return _E[0]


def rail_configs(strip_override=None):
    s_al = (STRIPS["al"], 2.0, 10.0)
    s_st = (STRIPS["steel"], 1.5, 10.0)
    s_st2 = (STRIPS["steel"], 2.0, 10.0)
    cfg = {
        "A1 printed (coupon + NOMAD baseline)": dict(walls=(g.WALL, g.WALL)),
        "A2 empty": dict(walls=(g.A2_WALL, g.A2_WALL), slotted=(True, True)),
        "A2 + 1 Al 10x2 (loop-side wall)": dict(walls=(g.A2_WALL, g.A2_WALL), slotted=(True, True), strips=(None, s_al), single=True),
        "A2 + 1 steel 10x1.5 (loop-side wall)": dict(walls=(g.A2_WALL, g.A2_WALL), slotted=(True, True), strips=(None, s_st), single=True),
        "A2 + 1 steel 10x2 (loop-side wall)": dict(walls=(g.A2_WALL, g.A2_WALL), slotted=(True, True), strips=(None, s_st2), single=True),
        "A2 + 2 Al 10x2": dict(walls=(g.A2_WALL, g.A2_WALL), slotted=(True, True), strips=(s_al, s_al)),
        "A2 + 2 steel 10x1.5": dict(walls=(g.A2_WALL, g.A2_WALL), slotted=(True, True), strips=(s_st, s_st)),
        "NOMAD 1-strip rail ref. (walls 2.5 / 4.1, steel 10x1.5)": dict(walls=(g.WALL, g.A2_WALL), slotted=(False, True), strips=(None, s_st), single=True),
    }
    if strip_override:
        cfg[f"A2 + 1 user strip {strip_override}"] = dict(walls=(g.A2_WALL, g.A2_WALL), slotted=(True, True),
                                                           strips=(None, strip_override), single=True)
    return cfg


def rail_expect(strip_override=None):
    tol = 0.35                                  # D.1 display-gap tolerance RSS (frame-mounted rails)
    lim1, lim3 = 0.50, 1.0 - tol
    print(f"\n== RAIL (coupon A), E {g_e():g} MPa; load at the stowed carriage centre (X 178, arm {ARM:g}); deflection toward the display ==")
    print(f"   analytical limits (D.1, not tightened): R1 0.3 kg <= {lim1:.2f}; R2 0.9 kg (3 g) <= {lim3:.2f} (= 1.0 gap - {tol} tolerance RSS);"
          f" evaluated at the rail TIP (X 196, lowest point over the display), also shown at the carriage (X 178, the D.1 evaluation point)")
    print(f"   {'configuration':<58} {'EI e6':>6} | R1 0.3 kg: X100 / X178 / X196 | R2 0.9 kg: X100 / X178 / X196 | tip verdict")
    rows = {}
    for name, c in rail_configs(strip_override).items():
        rects, w = rail_rects(c["walls"], c.get("slotted", (False, False)), c.get("strips"))
        ei = ei_of(rects)
        r1 = [cantilever(ei, 0.3, STATIONS[x]) for x in (100, 178, 196)]
        r3 = [cantilever(ei, 0.9, STATIONS[x]) for x in (100, 178, 196)]
        verdict = "meets" if r1[2] <= lim1 and r3[2] <= lim3 else ("R2 fails" if r1[2] <= lim1 else "R1 and R2 fail")
        rows[name] = (ei, r1, r3, w, rects)
        print(f"   {name:<58} {ei / 1e6:6.1f} | {r1[0]:5.2f} / {r1[1]:5.2f} / {r1[2]:5.2f}   | {r3[0]:5.2f} / {r3[1]:5.2f} / {r3[2]:5.2f}   | {verdict}")
        if c.get("single"):
            ya, yb = ei_of(rects, 0, w / 2), ei_of(rects, w / 2, w)
            soft = min(ya, yb)
            d_soft = cantilever(soft, 0.45, STATIONS[196])     # equal split: half the 0.9 kg into the soft half
            print(f"   {'':<58}        single-strip asymmetry (rough bounds, inferred): soft-edge tip at 3 g between "
                  f"{r3[2]:.2f} (fully coupled) and {d_soft:.2f} (walls uncoupled, load split equally); halves EI {ya / 1e6:.1f} / {yb / 1e6:.1f}e6")
    play_tip = g.STRIP_CLR_H + g.STRIP_CLR_H / g.PAD_LEN * STATIONS[196]
    print(f"   UNSHIMMED strip (slot {g.STRIP_H + g.STRIP_CLR_H:g} for a {g.STRIP_H:g} strip): the strip only engages after ~{play_tip:.1f} mm of tip "
          f"deflection (0.4 gap + root rotation 0.4/{g.PAD_LEN:g} over {STATIONS[196]:g}); below that it behaves as A2 empty (inferred)")
    return rows


# ------------------------------------------------------------------ expected values: sandwich (coupon B frame)
def plate_section(kind, inner_eff=None, core_g=None):
    """Whole-width EI (N*mm2) and shear stiffness GA (N) of a 90 mm plate over the 202 span."""
    e, gm = g_e(), g_e() / (2 * (1 + NU))
    if kind == "B1":
        t = g.PLATE_T
        return e * W_PLATE * t ** 3 / 12, math.inf
    if kind.startswith("B2"):
        h = float(kind.split("h")[1])
        pcs = [(W_PLATE, g.PLATE_T, g.PLATE_T / 2)] + [(g.RIB_T, h, g.PLATE_T + h / 2)] * len(g.RIB_Y)
        ga = gm * len(g.RIB_Y) * g.RIB_T * h
    else:
        t_in = SKIN if inner_eff is None else inner_eff
        if kind == "INFILL":
            webs_w = 2 * 0.9                                    # two perimeters at the plate edges (slicer)
            ga = gm * webs_w * CORE + (core_g or 0.05) * gm * (W_PLATE - webs_w) * CORE
        else:
            n = INTERIOR_WEBS[kind]
            webs_w = n * WEB_T + 2 * EDGE_T
            ga = gm * webs_w * CORE
        pcs = [(W_PLATE, SKIN, SKIN / 2), (webs_w, CORE, SKIN + CORE / 2), (W_PLATE, t_in, SKIN + CORE + t_in / 2)]
    a = sum(b * t for b, t, _ in pcs)
    zb = sum(b * t * z for b, t, z in pcs) / a
    return e * sum(b * t ** 3 / 12 + b * t * (z - zb) ** 2 for b, t, z in pcs), ga


def plate_defl(ei, ga, p_n, uniform=False):
    L = g.SPAN
    if uniform:
        return 5 * p_n * L ** 3 / (384 * ei) + p_n * L / (8 * ga)
    return p_n * L ** 3 / (48 * ei) + p_n * L / (4 * ga)


def sandwich_expect():
    p1 = 20.0 * W_PLATE / 101.0                     # LC1 (20 N on b_eff 101) scaled to the 90 mm coupon width
    q2 = 0.001 * g.SPAN * W_PLATE                   # LC2 1 kPa over the coupon span x width
    print(f"\n== SANDWICH / PLATES on the P0.1 B frame (simply supported model, span {g.SPAN:g}, width {W_PLATE:g}, E {g_e():g}) ==")
    print(f"   S1 = LC1-equivalent line load {p1:.1f} N ({p1 / 9.81:.2f} kg on the load bar); S1b = LC2 uniform {q2:.1f} N ({q2 / 9.81:.2f} kg spread); "
          f"S2 = 20 N reference ({20 / 9.81:.2f} kg). Analytical limit (D.1, gap 2): S1 and S1b <= 1.00")
    print(f"   {'plate':<36} {'EI e6':>6} | S1 nominal / inner 0.8 / inner 0.6 | S1b   | S2    | verdict S1 (nominal)")
    for name, kind in (("B-S30 (webs: 2 x 2.0 + edges 1.2)", "S30"), ("B-S20 (webs: 3 x 2.0 + edges 1.2)", "S20")):
        ei, ga = plate_section(kind)
        d = [plate_defl(*plate_section(kind, ie), p1) for ie in (None, 0.8, 0.6)]
        print(f"   {name:<36} {ei / 1e6:6.2f} | {d[0]:5.2f} / {d[1]:5.2f} / {d[2]:5.2f}            | {plate_defl(ei, ga, q2, True):5.2f} | "
              f"{plate_defl(ei, ga, 20.0):5.2f} | {'meets' if d[0] <= 1.0 else 'FAILS'}")
    for f in (0.10, 0.05, 0.02):
        ei, ga = plate_section("INFILL", core_g=f)
        print(f"   {'B-INFILL, core G = ' + format(f * 100, 'g') + '% G_PETG':<36} {ei / 1e6:6.2f} | {plate_defl(ei, ga, p1):5.2f} (skins as printed)       | "
              f"{plate_defl(ei, ga, q2, True):5.2f} | {plate_defl(ei, ga, 20.0):5.2f} | {'meets' if plate_defl(ei, ga, p1) <= 1.0 else 'FAILS'}")
    ei, ga = plate_section("B1")
    print(f"   {'B1 plain 2.5 (E calibration)':<36} {ei / 1e6:6.2f} | at 1 N {plate_defl(ei, ga, 1.0):.2f}, 2 N {plate_defl(ei, ga, 2.0):.2f} (stop at 5 mm) | "
          f"not a pass/fail part")
    ei, ga = plate_section("B2h8")
    print(f"   {'B2 h 8 (optional, class C proxy)':<36} {ei / 1e6:6.2f} | {plate_defl(ei, ga, p1):5.2f}                         | "
          f"{plate_defl(ei, ga, q2, True):5.2f} | {plate_defl(ei, ga, 20.0):5.2f} | reference only (class C criterion differs)")
    print("   Screwed bands add partial end fixity: measured screwed deflection should be BELOW these simply supported values; "
          "the unscrewed (resting) run is the model-calibration case (inferred)")
    print("\n   Measured-to-predicted S1 ratio (unscrewed run) -> sandwich depth needed for the D.1 criterion -> class A lid T (lip 1, gap 2):")
    row = []
    for k in (0.7, 0.85, 1.0, 1.15, 1.3, 1.6):
        depth = 2 * SKIN + 0.5
        while depth < 20:
            core = depth - 2 * SKIN
            ei, ga = sandwich_section_depth(core)
            if plate_defl(ei / k, ga / k, p1) <= 1.0:
                break
            depth += 0.1
        row.append(f"x{k:g}: depth {depth:.1f} -> T {29 + 2 + depth:.1f}")
    print("   " + "; ".join(row) + "  (ratio > 1 = softer than predicted; webs 2 x 2.0 @ S30 layout, skins 1.2)")


def sandwich_section_depth(core):
    """S30-layout plate section with a given core height (for the required-depth mapping)."""
    e, gm = g_e(), g_e() / (2 * (1 + NU))
    webs_w = INTERIOR_WEBS["S30"] * WEB_T + 2 * EDGE_T
    pcs = [(W_PLATE, SKIN, SKIN / 2), (webs_w, core, SKIN + core / 2), (W_PLATE, SKIN, SKIN + core + SKIN / 2)]
    a = sum(b * t for b, t, _ in pcs)
    zb = sum(b * t * z for b, t, z in pcs) / a
    return e * sum(b * t ** 3 / 12 + b * t * (z - zb) ** 2 for b, t, z in pcs), gm * webs_w * core


# ------------------------------------------------------------------ package quantities
def package(vols_new):
    """Volumes/masses of the P0.2 order: reused P0.1 parts (meshed from the P0.1 master) + new P0.2 parts."""
    p01 = {p.name: p for p in g.all_parts([8.0])}
    reuse = {"A1_rail_printed": 1.0, "A2_rail_stiffener_slots": 1.0, "A_pad_stub": 1.0, "A_carriage_load_post": 0.6,
             "A_display_surrogate": 0.6, "A_load_platform": 0.6, "B_frame_supports": 0.6, "B1_plate_plain_2p5": 1.0,
             "B_load_pad": 0.6, "B2_plate_ribbed_h08": 1.0}
    vols = {}
    for n in reuse:
        tris, _, _ = g.mesh(p01[n])
        vols[n] = g.manifold_report(tris)[2] / 1000
    vols.update(vols_new)
    core_void = (W_PLATE - 1.8) * g.SPAN * CORE / 1000 + (W_PLATE - 1.8) * 2 * g.BAND * CORE / 1000
    fill = {**reuse, "B_S30_sandwich": 1.0, "B_S20_sandwich": 1.0, "B_clearance_block_2p0": 0.6, "B_load_bar": 0.6}
    mass = {n: vols[n] * 1000 * RHO * fill[n] for n in fill}
    mass["B_INFILL_plate"] = (vols["B_INFILL_plate"] - core_void * 0.8) * 1000 * RHO     # 20 % core
    sets = {
        "absolute minimum": ["A2_rail_stiffener_slots", "A_pad_stub", "A_carriage_load_post", "A_display_surrogate",
                             "B_frame_supports", "B_S30_sandwich", "B_S20_sandwich", "B_clearance_block_2p0", "B_load_bar"],
    }
    sets["recommended"] = sets["absolute minimum"] + ["A1_rail_printed", "B_INFILL_plate", "B1_plate_plain_2p5",
                                                      "A_load_platform", "B_load_pad"]
    sets["recommended + optional class C proxy"] = sets["recommended"] + ["B2_plate_ribbed_h08"]
    print("\n== PACKAGE quantities (solid volume from the meshes; mass at the stated infill; rough) ==")
    for n in fill | {"B_INFILL_plate": 0}:
        print(f"   {n:<28} solid {vols[n]:6.1f} cm3  -> ~{mass[n]:5.0f} g at {('20 % core' if n == 'B_INFILL_plate' else format(fill[n] * 100, 'g') + ' % of solid')}")
    for s, names in sets.items():
        m = sum(mass[n] for n in names)
        print(f"   {s}: {len(names)} parts, ~{m:.0f} g PETG, ~{m / 14:.0f} h print time at ~14 g/h (inferred), largest part 230 x 90")
    return sets, mass, vols


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--expect", action="store_true")
    ap.add_argument("--E", type=float, default=2000.0)
    ap.add_argument("--strip", help="material,thickness,height of a measured strip, e.g. steel,1.5,10.0")
    a = ap.parse_args(argv)
    _E[0] = a.E
    override = None
    if a.strip:
        m, t, h = a.strip.split(",")
        override = (STRIPS[m], float(t), float(h))
    ok = True
    vols = {}
    if not a.expect:
        ok, vols = write_parts(new_parts())
    rail_expect(override)
    sandwich_expect()
    if not a.expect:
        package(vols)
        print("\nALL CHECKS PASSED" if ok else "\nSOME CHECKS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
