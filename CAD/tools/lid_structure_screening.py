"""P0.1 Round B.2: structural / printability screening of three lid concepts for V1 + fixes.

Modeled only. Stiffness numbers are SCREENING ESTIMATES from simple beam formulas (one-way plate
strips, cantilevers), not FEA. Nothing here chooses V1 or a lid concept.

Concepts (all keep the V1 + fixes solar geometry, cassettes, 13 mm rail layer, loops, corridor):
  A  one-piece lid, back plate stiffened by external ribs
  B  one-piece lid, structural perimeter frame (edge beams + posts) with a thinner central panel
  C  two-piece structural lid: front frame (display, rails, hinge interface, solar loads)
     + rear shell (ribbed back plate), joined by M3 screws into heat-set inserts

Usage:  py CAD/tools/lid_structure_screening.py
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hinge_feasibility_2d as hm  # noqa: E402
import solar_skeleton_model as sk  # noqa: E402
import solar_v1_feasibility as v1  # noqa: E402

C = v1.config(True)                       # V1 + the four provisional fixes
D, H, G, W, WALL, MIN_GAP = sk.D, sk.H, sk.G, sk.W, sk.WALL, sk.MIN_GAP
HC, TC, XW = sk.HC, sk.TC, sk.X_WALL_IN
box = sk.box

# ---- screening assumptions (provisional; not design values, not in nomad.yaml) ----
E_PETG = 2000.0        # MPa, nominal
RHO = 1.27e-3          # g/mm^3, PETG solid
P1 = 20.0              # N, hand press at mid-bay (LC1)
Q2 = 0.001             # MPa (= 1 kPa) uniform, e.g. packed in a bag (LC2)
SPAN = HC + 2 * MIN_GAP                 # cassette bay clear span in Y between edge supports
B_EFF = SPAN / 2                        # effective width for a point load on a one-way plate (conservative)
RIB_T, RIB_S = 2.0, 30.0                # rib thickness, rib spacing (FDM-practical)
PANEL_B = 1.6                           # concept B thinner central panel
SAND_SKIN = 1.0                         # printed sandwich skin (core shear ignored -> optimistic)
CASSETTE_MASS = 0.30                    # kg per cassette, screening only (no panel selected)
SHOCK = 3.0                             # handling/drop factor for screening
INSERT = {"od": 4.5, "len": 5.7, "boss": 8.0}   # typical M3 heat-set insert envelope (provisional)
SCREW_X = [-140, -70, 0, 70, 140]       # rear-shell screw stations along each edge band


def i_ribbed(skin, h, t=RIB_T, s=RIB_S):
    """Second moment per mm width: skin plate with external ribs of height h (T-section per rib)."""
    if h <= 0:
        return skin ** 3 / 12
    af, yf = s * skin, skin / 2
    aw, yw = t * h, skin + h / 2
    yb = (af * yf + aw * yw) / (af + aw)
    return (s * skin ** 3 / 12 + af * (yf - yb) ** 2 + t * h ** 3 / 12 + aw * (yw - yb) ** 2) / s


def i_sandwich(total, skin=SAND_SKIN):
    d = (total - skin) / 2
    return 2 * (skin ** 3 / 12 + skin * d ** 2)


def deflections(iw):
    d1 = P1 * SPAN ** 3 / (48 * E_PETG * iw * B_EFF)
    d2 = 5 * Q2 * SPAN ** 4 / (384 * E_PETG * iw)
    return d1, d2


def min_rib(skin, allow):
    h = 0.0
    while h <= 40:
        if max(deflections(i_ribbed(skin, h))) <= allow:
            return h
        h += 0.5
    return None


def min_sandwich(allow):
    t = 2.0
    while t <= 40:
        if max(deflections(i_sandwich(t))) <= allow:
            return t
        t += 0.5
    return None


def rail_section():
    """Rail C-channel (open top slot) second moment for bending toward the display, and area."""
    w, h, cw, ch, slot = C["rail_w"], C["rail_h"], C["cw"], C["ch"], C["slot_w"]
    pieces = [(w, WALL, WALL / 2),                                   # floor
              (WALL, ch, WALL + ch / 2), (WALL, ch, WALL + ch / 2),  # side walls
              ((w - slot) / 2, WALL, h - WALL / 2), ((w - slot) / 2, WALL, h - WALL / 2)]  # top lips
    a = sum(b * t for b, t, _ in pieces)
    yb = sum(b * t * y for b, t, y in pieces) / a
    i = sum(b * t ** 3 / 12 + b * t * (y - yb) ** 2 for b, t, y in pieces)
    return i, a


def rail_cantilever():
    """Stowed cassette weight on the carriage at the rail's inboard end; rail fixed only at its outboard pad."""
    i, a = rail_section()
    pad_in = sk.DISP_W / 2 + MIN_GAP                        # pad starts 1 mm outside the display edge
    carriage_c = sk.XI - C["link"] - sk.L / 2               # stowed carriage centre (right side)
    arm = pad_in - carriage_c
    p = CASSETTE_MASS * 9.81
    d = p * arm ** 3 / (3 * E_PETG * i)
    return i, arm, d, d * SHOCK


def deployed_loads():
    """Screening moment at the carriage from a deployed cassette: weight + wind (10 and 20 m/s)."""
    xi = sk.XI + C["S"]
    arm = (xi + sk.WC / 2) - (xi - C["link"] - sk.L / 2)
    area = sk.WC * HC * 1e-6
    out = {}
    for v in (10, 20):
        fw = 0.5 * 1.2 * v ** 2 * 1.2 * area
        f = CASSETTE_MASS * 9.81 + fw
        m = f * arm / 1000
        out[v] = (fw, m, m / (sk.L / 1000))           # N, N*m, N (end reaction couple over the carriage)
    return arm, out


# ------------------------------------------------------------------ concept geometry (lid frame)
def concept_parts(kind, rib_h):
    """Static structure added on top of the V1 lid parts. Names start with 'W' (lid structure)."""
    back = C["back"]
    extra = {}
    if kind in "ABC":        # edge beams in the cassette-layer bands (shelves), all concepts
        extra["Wh0"] = (-XW, XW, box(WALL, C["cy0"] - MIN_GAP, C["cz0"] - MIN_GAP, back))
        extra["Wh1"] = (-XW, XW, box(C["cy0"] + HC + MIN_GAP, D - WALL, C["cz0"] - MIN_GAP, back))
    if kind in "AC" and rib_h > 0:
        top = C["T"]
        for i, x in enumerate(range(-135, 136, int(RIB_S))):
            extra[f"Wg{i:02d}"] = (x - RIB_T / 2, x + RIB_T / 2, box(0, D, top, top + rib_h))
        for j, y in enumerate((C["cy0"] - MIN_GAP - 7, D / 2, C["cy0"] + HC + MIN_GAP + 7)):
            extra[f"Wt{j}"] = (-W / 2, W / 2, box(y - RIB_T / 2, y + RIB_T / 2, top, top + rib_h))
    if kind == "C":          # rail-module pads on the bezel beside the display
        for s in (1, -1):
            rc = C["rc"][s]
            x0, x1 = sk.DISP_W / 2 + MIN_GAP, XW - MIN_GAP
            xa, xb = (x0, x1) if s > 0 else (-x1, -x0)
            extra[f"Wp{'R' if s > 0 else 'L'}"] = (xa, xb, box(rc - C["rail_w"] / 2, rc + C["rail_w"] / 2, WALL, C["rz0"]))
    return extra


def parts_for(kind, rib_h, eR, eL, tilt):
    p = v1.all_parts(C, eR, eL, tilt)
    p.update(concept_parts(kind, rib_h))
    if kind == "B":          # thinner central panel, outer face flush with the frame top
        p["Wb"] = (-W / 2, W / 2, box(0, D, C["T"] - PANEL_B, C["T"]))
    return p


def keepouts():
    """Static keep-outs the structure must not invade: service loops, cable corridor, controller zone, display."""
    lp = v1.loops(C)
    ly = [y for y, _ in lp["LR"][2]]
    rail_top = C["rz0"] + C["rail_h"]
    corridor = (C["rc"][-1] + C["rail_w"] / 2, C["rc"][1] - C["rail_w"] / 2)
    overlap_x = -(sk.XI - C["link"] - sk.L) + v1.CABLE_D / 2 + MIN_GAP      # both rails present within +/- this
    return {
        "LR": lp["LR"], "LL": lp["LL"],
        "corridor": (-overlap_x, overlap_x, box(corridor[0], corridor[1], C["rz0"], rail_top)),
        "controller(provisional)": (-XW, XW, box(max(ly) + MIN_GAP, D - WALL, C["rz0"], rail_top)),
    }


def static_conflicts(kind, rib_h):
    new = concept_parts(kind, rib_h)
    base_lid = v1.lid_parts(C)
    bad = []
    for kn, kp in {**keepouts(), "D": base_lid["D"]}.items():
        for n, p in new.items():
            c = sk.clearance(kp, p)
            if c < 0:
                bad.append((n, kn, "OVERLAP", round(c, 2)))
            elif c < MIN_GAP - 1e-6:
                bad.append((n, kn, "touching boundary", round(c, 2)))
    return bad


def motion_check(kind, rib_h):
    worst, ground = {}, {}
    for lid in sk.LID_ANGLES:
        for eR in (0, 0.5, 1):
            for eL in (0, 0.5, 1):
                viol, _, _ = v1.check(v1.to_world(parts_for(kind, rib_h, eR, eL, 0), lid))
                for p, c in viol:
                    worst[p] = min(worst.get(p, 9e9), c)
        for t in v1.TILTS_REPORT:
            viol, zmin, _ = v1.check(v1.to_world(parts_for(kind, rib_h, 1, 1, t), lid))
            ground[(lid, t)] = zmin
            for p, c in viol:
                worst[p] = min(worst.get(p, 9e9), c)
    return worst, ground


def hinge_ground(T_total):
    lid = hm.rect(0, D, H + G, H + G + T_total)
    worst = min(hm.signed_clearance(hm.rotate(lid, sk.HINGE, a), hm.BASE) for a in hm.angles(hm.STEP))
    lowest = {a: min(z for _, z in hm.rotate(lid, sk.HINGE, a)) for a in sk.LID_ANGLES}
    ov = {a: max(y for y, _ in hm.rotate(lid, sk.HINGE, a)) - D for a in sk.LID_ANGLES[1:]}
    return worst, lowest, ov


def mass_back(kind, rib_h):
    plate = (W * D * (PANEL_B if kind == "B" else WALL))
    ribs = 0.0
    if kind in "AC" and rib_h > 0:
        ribs = len(range(-135, 136, int(RIB_S))) * RIB_T * D * rib_h + 3 * RIB_T * W * rib_h
    return (plate + ribs) * RHO


def mass_frame():
    shelves = 2 * (2 * XW) * (C["cy0"] - MIN_GAP - WALL) * (C["back"] - C["cz0"] + MIN_GAP)
    return shelves * RHO


def main():
    gap = C["back"] - (C["cz0"] + TC)
    allow = gap / 2
    print("=== Screening basis (NOT FEA) ===")
    print(f"back plate spans the cassette bay one-way: L = {SPAN:g} mm between edge beams (no internal supports possible; "
          f"side edges are open slots). E = {E_PETG:g} MPa. LC1 {P1:g} N point at mid-bay on b_eff {B_EFF:g}; "
          f"LC2 {Q2 * 1000:g} kPa uniform. Criterion: deflection <= half the cassette clearance = {allow:g} mm.")
    print("\nrib height sweep (skin 2.5, ribs 2.0 thick @ 30 mm, external):")
    for h in (0, 2, 4, 6, 8, 10, 12, 14):
        d1, d2 = deflections(i_ribbed(WALL, h))
        print(f"  h {h:>2}: LC1 {d1:6.2f} mm  LC2 {d2:6.2f} mm  lid T {C['T'] + h:g}  back-plate mass {mass_back('A', h):4.0f} g")
    for t in (1.2, 1.6, 2.0, 2.5, 4.0):
        d1, d2 = deflections(t ** 3 / 12)
        print(f"  plain {t:>3} plate: LC1 {d1:6.2f}  LC2 {d2:6.2f}")
    print("\nminimum stiffening to meet the criterion, versus cassette clearance (thickness = 28 + gap + plate):")
    for g in (1.0, 2.0, 3.0):
        h = min_rib(WALL, g / 2)
        t = min_sandwich(g / 2)
        print(f"  clearance {g:g}: ribs {h:g} mm on 2.5 skin -> lid T {28 + g + WALL + h:g};  "
              f"printed sandwich {t:g} mm (core shear ignored, optimistic) -> lid T {28 + g + t:g}")
    hA = min_rib(WALL, allow)
    dB = deflections(PANEL_B ** 3 / 12)
    need_gap_B = 2 * max(dB)
    print(f"\nconcept B central panel {PANEL_B:g} (no ribs): LC1 {dB[0]:.1f} mm, LC2 {dB[1]:.1f} mm -> would need ~{need_gap_B:.0f} mm "
          f"clearance to stay off the cassettes; frame cannot shorten the {SPAN:g} mm span (bay is clear, side edges slotted)")

    ri, rarm, rd, rds = rail_cantilever()
    print(f"\nrail cantilever (all concepts): printed C-channel I = {ri:.0f} mm^4; stowed carriage {rarm:.0f} mm from the outboard pad; "
          f"{CASSETTE_MASS:g} kg cassette -> {rd:.2f} mm static, {rds:.2f} mm at {SHOCK:g} g toward the display (1.0 mm clearance)")
    for e, lbl in ((70000, "aluminium bar insert (E 70 GPa, same section share ~30%)"),):
        print(f"  with a metal stiffener ({lbl}): roughly x{1 + 0.3 * e / E_PETG:.0f} stiffer -> {rds / (1 + 0.3 * e / E_PETG):.2f} mm at {SHOCK:g} g (inferred)")
    arm, dl = deployed_loads()
    print(f"deployed cassette on its carriage (arm {arm:.0f} mm): " +
          "; ".join(f"wind {v} m/s: wind force {fw:.1f} N, moment {m:.2f} N*m, carriage end reactions ~{r:.0f} N" for v, (fw, m, r) in dl.items()))

    for kind, rib_h, label in (("A", hA, "A  one-piece, external ribs"), ("B", 0, "B  one-piece, perimeter frame + 1.6 panel"),
                               ("C", hA, "C  two-piece: front frame + ribbed rear shell")):
        T_total = C["T"] + (rib_h if kind in "AC" else 0)
        worst, ground = motion_check(kind, rib_h)
        stat = static_conflicts(kind, rib_h)
        hw, low, ov = hinge_ground(T_total)
        d = deflections(i_ribbed(WALL, rib_h)) if kind in "AC" else dB
        gmin = {lid: min(z for (l, t), z in ground.items() if l == lid) for lid in sk.LID_ANGLES}
        print(f"\n--- {label} ---")
        print(f"lid thickness {T_total:g} (closed stack {H + G + T_total:g}); back deflection LC1 {d[0]:.2f} / LC2 {d[1]:.2f} mm "
              f"vs allowed {allow if kind != 'B' else (C['T'] - PANEL_B - C['cz0'] - TC) / 2:.2f}; back-plate(+ribs) mass {mass_back(kind, rib_h):.0f} g, "
              f"edge beams {mass_frame():.0f} g")
        print(f"motion/stowed collisions (all lid angles, extensions, tilts): {sorted(worst.items()) or 'none'}")
        print(f"static conflicts with loops/corridor/controller keep-out/display: {stat or 'none'}")
        print(f"hinge: min lid/base clearance over 0-135 {hw:.2f}; lid lowest z at 0/105/135: "
              f"{', '.join(f'{low[a]:.1f}' for a in sk.LID_ANGLES)}; rear overhang 105/135: {ov[105.0]:.1f}/{ov[135.0]:.1f}; "
              f"solar lowest z (deployed tilts) at 0/105/135: {', '.join(f'{gmin[a]:.0f}' for a in sk.LID_ANGLES)}")
    print("\nC joint: M3 heat-set inserts (typ. envelope "
          f"{INSERT['od']:g} x {INSERT['len']:g}, boss {INSERT['boss']:g}) in the tops of the two edge beams (band width "
          f"{C['cy0'] - MIN_GAP - WALL:g}), {len(SCREW_X)} per band = {2 * len(SCREW_X)} screws, "
          f"M3 x ~{math.ceil(WALL + INSERT['len']):g} through the {WALL:g} rear shell from outside; "
          f"LC2 total {Q2 * SPAN * (2 * XW):.0f} N -> {Q2 * SPAN * (2 * XW) / (2 * len(SCREW_X)):.0f} N per screw")


if __name__ == "__main__":
    main()
