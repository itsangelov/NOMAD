"""P0.1 Round B: solar-cassette kinematic skeleton model (exact prism model, modeled only).

Every moving part rotates about an X-parallel axis (lid about the hinge, cassette about its hub)
or translates along X (slide), so each body is an X-interval times a convex Y-Z polygon. The
clearance between two such prisms is exact: overlapping in both -> -min(penetration); otherwise
hypot(X gap, Y-Z gap). Reuses the Onshape-validated 2D code from hinge_feasibility_2d.py.

Layouts (all keep the D-004 kinematics: lateral slide out of the lid, tilt about an axis along
the slide direction, rail carries the load, a hub pin on the carriage carries rotation):
  V0  current working values: hub axis at the cassette mid-plane (SOLAR_HUB_AXIS_OFFSET_Y/Z),
      rail coaxial with the hub, both sides mirrored.
  V1  rail layer stacked between display and cassettes; left/right rails staggered in Y.
  V2  rails in Y edge bands beside the cassettes (right rail rear band, left rail front band).
V1/V2 are evaluated at the lid thickness / cassette height they require; they are what-ifs,
not decisions.

Usage:  py CAD/tools/solar_skeleton_model.py [--crosscheck]
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hinge_feasibility_2d as hm  # noqa: E402

V = hm.V
D, H, T0, G, W = V["BODY_DEPTH"], V["BODY_HEIGHT"], V["LID_THICKNESS"], V["LID_CLOSED_GAP"], V["BODY_WIDTH"]
WALL, MIN_GAP = V["WALL_THICKNESS"], V["MIN_GAP"]
WC, HC, TC = V["SOLAR_CASSETTE_WIDTH"], V["SOLAR_CASSETTE_HEIGHT"], V["SOLAR_CASSETTE_THICKNESS"]
S, L, LINK = V["SOLAR_SLIDE_TRAVEL"], V["SOLAR_RAIL_ENGAGEMENT"], V["SOLAR_HUB_LINK_LENGTH"]
CW, CH, PIN = V["SOLAR_CARRIAGE_WIDTH"], V["SOLAR_CARRIAGE_HEIGHT"], V["SOLAR_HUB_PIN_DIAMETER"]
HUB_Y, HUB_Z = V["SOLAR_HUB_AXIS_OFFSET_Y"], V["SOLAR_HUB_AXIS_OFFSET_Z"]
TILT_MAX, INDEX = V["SOLAR_ROTATION_LIMIT"]["max"], V["SOLAR_INDEX_STEP"]
DISP_T, DISP_W, DISP_H = V["DISPLAY_THICKNESS"], V["DISPLAY_WIDTH"], V["DISPLAY_HEIGHT"]
HINGE = (D - V["HINGE_AXIS_OFFSET"], H + V["HINGE_AXIS_HEIGHT"])
LID_ANGLES = [0.0, V["LID_ANGLE_NOMINAL"], V["LID_ANGLE_MAX"]]
XI = MIN_GAP / 2                      # stowed cassette inboard edge (centre gap = MIN_GAP)
RAIL_W, RAIL_H = CW + 2 * WALL, CH + 2 * WALL
X_WALL_IN = W / 2 - WALL              # lid side wall inner face
TILTS = [t for t in range(-int(TILT_MAX), int(TILT_MAX) + 1, 5)]
rect = hm.rect


def box(y0, y1, z0, z1):
    return rect(min(y0, y1), max(y0, y1), min(z0, z1), max(z0, z1))


def layout(variant, T=T0, hc=HC):
    zb = H + G                         # lid display face, closed pose
    back = zb + T - WALL               # lid back plate inner face
    if variant == "V0":
        cz0, cy0 = back - MIN_GAP - TC, (D - hc) / 2
        hub = {s: (cy0 + HUB_Y, cz0 + HUB_Z) for s in (1, -1)}
    elif variant == "V1":
        rz0 = zb + DISP_T + MIN_GAP
        cz0, cy0 = rz0 + RAIL_H + MIN_GAP, (D - hc) / 2
        off = RAIL_W / 2 + MIN_GAP / 2
        hub = {1: (D / 2 + off, rz0 + RAIL_H / 2), -1: (D / 2 - off, rz0 + RAIL_H / 2)}
    elif variant == "V2":
        cz0, cy0 = back - MIN_GAP - TC, WALL + RAIL_W + MIN_GAP
        rzc = min(cz0 + TC / 2, back - RAIL_H / 2)
        hub = {1: (D - WALL - RAIL_W / 2, rzc), -1: (WALL + RAIL_W / 2, rzc)}
    return {"variant": variant, "zb": zb, "back": back, "T": T, "hc": hc, "cz0": cz0, "cy0": cy0, "hub": hub}


def xint(s, a, b):
    return (a, b) if s > 0 else (-b, -a)


def solar_side(lay, s, ext, tilt):
    tag = "R" if s > 0 else "L"
    xi = XI + ext * S
    hy, hz = lay["hub"][s]
    cass = box(lay["cy0"], lay["cy0"] + lay["hc"], lay["cz0"], lay["cz0"] + TC)
    if tilt:
        cass = hm.rotate(cass, (hy, hz), tilt)
    kx1 = xi - LINK
    return {
        "C" + tag: (*xint(s, xi, xi + WC), cass),
        "P" + tag: (*xint(s, kx1, xi), box(hy - PIN / 2, hy + PIN / 2, hz - PIN / 2, hz + PIN / 2)),
        "K" + tag: (*xint(s, kx1 - L, kx1), box(hy - CW / 2, hy + CW / 2, hz - CH / 2, hz + CH / 2)),
        "R" + tag: (*xint(s, XI - LINK - L, XI + S - LINK), box(hy - RAIL_W / 2, hy + RAIL_W / 2, hz - RAIL_H / 2, hz + RAIL_H / 2)),
    }


def lid_parts(lay):
    zb, back, top = lay["zb"], lay["back"], lay["zb"] + lay["T"]
    dy0 = D / 2 - V["DISPLAY_VERTICAL_OFFSET"] - DISP_H / 2
    return {
        "D": (-DISP_W / 2, DISP_W / 2, box(dy0, dy0 + DISP_H, zb, zb + DISP_T)),
        "Wb": (-X_WALL_IN, X_WALL_IN, box(0, D, back, top)),
        "Wf": (-X_WALL_IN, X_WALL_IN, box(0, WALL, zb, back)),
        "Wr": (-X_WALL_IN, X_WALL_IN, box(D - WALL, D, zb, back)),
        "SR": (X_WALL_IN, W / 2, box(0, D, zb, top)),
        "SL": (-W / 2, -X_WALL_IN, box(0, D, zb, top)),
    }


def clearance(a, b):
    xo = min(a[1], b[1]) - max(a[0], b[0])
    s = hm.signed_clearance(a[2], b[2])
    if xo > 1e-9 and s < 0:
        return -min(xo, -s)
    return math.hypot(max(0.0, -xo), max(0.0, s))


def excluded(a, b):
    """Pairs that are attached by design, or side-wall crossings that define the wall opening."""
    if a[-1] == b[-1] and {a[0], b[0]} in ({"P", "K"}, {"P", "R"}, {"K", "R"}, {"P", "C"}):
        return True
    if {a, b} & {"SR", "SL"} and ({a[0], b[0]} & {"C", "P"}):
        return True
    if {a[0], b[0]} == {"R", "W"}:     # the fixed rail may be integral with the lid walls
        return True
    return a[0] in "DWS" and b[0] in "DWS"


def state(lay, lid, eR, eL, tilt=0.0):
    parts = {**lid_parts(lay), **solar_side(lay, 1, eR, tilt if eR == 1 else 0),
             **solar_side(lay, -1, eL, tilt if eL == 1 else 0)}
    world = {k: (x0, x1, hm.rotate(p, HINGE, lid)) for k, (x0, x1, p) in parts.items()}
    world["B"] = (-W / 2, W / 2, box(0, D, 0, H))
    return world


def check(world, cassette_only=False):
    """Violations (< MIN_GAP) and the solar parts' minimum world z (the table is z = 0)."""
    names = sorted(world)
    viol, allc = [], {}
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if excluded(a, b) or (a == "B" and b[0] in "DWS") or (b == "B" and a[0] in "DWS"):
                continue
            if cassette_only and "C" not in (a[0], b[0]):
                continue
            c = clearance(world[a], world[b])
            allc[a + "-" + b] = c
            if c < MIN_GAP - 1e-6:
                viol.append((a + "-" + b, c))
    zmin = min(min(z for _, z in p) for k, (_, _, p) in world.items() if k[0] in "CPKR")
    return viol, zmin, allc


def extents(world, keys=None):
    ks = keys or [k for k in world]
    xs = [v for k in ks for v in world[k][:2]]
    ys = [y for k in ks for y, _ in world[k][2]]
    zs = [z for k in ks for _, z in world[k][2]]
    return (max(xs) - min(xs), min(ys), max(ys), min(zs), max(zs))


def opening(lay):
    """Y-Z bounding box (lid frame) of cassette + pin crossing a side wall during the slide, + MIN_GAP."""
    ys, zs = [], []
    for ext in [i / 20 for i in range(21)]:
        for k, (x0, x1, p) in solar_side(lay, 1, ext, 0).items():
            if k[0] in "CP" and x1 > X_WALL_IN and x0 < W / 2:
                ys += [y for y, _ in p]
                zs += [z for _, z in p]
    return (max(ys) - min(ys) + 2 * MIN_GAP, max(zs) - min(zs) + 2 * MIN_GAP, min(zs) - MIN_GAP - H - G)


def report(variant, **kw):
    lay = layout(variant, **kw)
    print(f"\n=== {variant}  (lid T={lay['T']:g}, cassette {WC:g} x {lay['hc']:g} x {TC:g}) ===")
    hub = lay["hub"]
    print(f"hub axis (lid frame y, z above display face): R {hub[1][0]:.1f}, {hub[1][1] - lay['zb']:.1f}   "
          f"L {hub[-1][0]:.1f}, {hub[-1][1] - lay['zb']:.1f};  cassette z {lay['cz0'] - lay['zb']:.1f}-{lay['cz0'] - lay['zb'] + TC:.1f}, "
          f"y {lay['cy0']:.1f}-{lay['cy0'] + lay['hc']:.1f};  lid inner z 0-{lay['back'] - lay['zb']:.1f}")
    op = opening(lay)
    print(f"side-wall opening needed (each side): {op[0]:.1f} (Y) x {op[1]:.1f} (Z), from z {op[2]:.1f} above display face")
    slide = {}
    for lid in LID_ANGLES:
        for eR in (0, 0.25, 0.5, 0.75, 1):
            for eL in (0, 0.25, 0.5, 0.75, 1):
                viol, zmin, _ = check(state(lay, lid, eR, eL))
                for p, c in viol:
                    k = (p, lid)
                    slide[k] = min(slide.get(k, 9e9), c)
    if slide:
        worst = {}
        for (p, lid), c in slide.items():
            worst[p] = min(worst.get(p, 9e9), c)
        print("slide/stowed violations (pair: worst clearance, mm):",
              ", ".join(f"{p} {c:+.1f}" for p, c in sorted(worst.items(), key=lambda x: x[1])))
    else:
        print("slide/stowed violations: none (all lid angles, extensions 0..1 in quarters, both sides)")
    for lid in LID_ANGLES:
        ok, bad, zmins = [], [], {}
        for t in TILTS:
            viol, zmin, allc = check(state(lay, lid, 1, 1, t), cassette_only=True)
            zmins[t] = zmin
            (bad if viol or zmin < 0 else ok).append(t)
        lo = hi = 0
        while lo - 5 in ok:
            lo -= 5
        while hi + 5 in ok:
            hi += 5
        idx = [t for t in range(lo, hi + 1, 5) if t % INDEX == 0] if 0 in ok else []
        vs = sorted({p for t in bad for p, _ in check(state(lay, lid, 1, 1, t), cassette_only=True)[0]})
        print(f"lid {lid:5.1f}: reachable tilt from 0 = {lo}..{hi} deg "
              f"(index positions ok: {idx}); solar min z over sweep {min(zmins.values()):+.1f}, at 0 deg {zmins[0]:+.1f}; "
              f"cassette collisions: {vs or 'none (ground only)' if bad else 'none'}")
    w0 = state(lay, LID_ANGLES[1], 0, 0)
    w1 = state(lay, LID_ANGLES[1], 1, 1)
    e0, e1 = extents(w0), extents(w1)
    print(f"extents at lid {LID_ANGLES[1]:g}: stowed overall X {e0[0]:.1f}; deployed overall X {e1[0]:.1f} "
          f"(cassette outer edges at +/-{XI + S + WC:.1f})")
    return lay


def travel_budget():
    need = S
    rail_needed = S + L
    own_half = X_WALL_IN - MIN_GAP - XI
    print("=== Travel budget (single-stage carriage, any layout) ===")
    print(f"required cassette travel S = {need:g} (cassette fully outside lid + {V['SOLAR_DEPLOY_CLEARANCE']:g} clearance)")
    print(f"carriage always sits inboard of the cassette by engagement {L:g} + link {LINK:g} = {L + LINK:g}")
    print(f"rail length needed per side = {rail_needed:g} (x {XI - LINK - L:g} .. {XI + S - LINK:g})")
    print(f"rail length available inside own half = {own_half:g}  ->  available carriage travel {own_half - L:g} "
          f"vs required {need:g}: shortfall {rail_needed - own_half:g}; each rail must cross the centreline by {-(XI - LINK - L):g}")


CROSSCHECK = [  # (label, lid angle, eR, eL, tilt) for the Onshape kernel cross-check
    ("S", 105.0, 0, 0, 0), ("D", 105.0, 1, 1, 0), ("a", 0.0, 1, 1, 30), ("b", 0.0, 1, 1, 45),
    ("c", 135.0, 1, 1, 75), ("d", 135.0, 1, 1, -75),
]
XC_KEYS = ["CR", "CL", "RR", "RL", "KR", "KL", "PR", "PL", "D", "B"]


def crosscheck():
    lay = layout("V0")
    out = ["X"]
    for label, lid, eR, eL, t in CROSSCHECK:
        w = state(lay, lid, eR, eL, t)
        w = {k: v for k, v in w.items() if k in XC_KEYS}
        viol, zmin, _ = check(w)
        pairs = "".join(sorted(p.replace("-", "") for p, c in viol if c < 0))
        out.append(f"{label}:{pairs or '-'}z{zmin:.1f}")
    print(" ".join(out))


if __name__ == "__main__":
    if "--crosscheck" in sys.argv:
        crosscheck()
        sys.exit()
    travel_budget()
    report("V0")
    v1 = layout("V1")
    t1 = T0 + (v1["cz0"] + TC + MIN_GAP) - v1["back"]
    print(f"\nV1 needs lid thickness >= {t1:g} (current {T0:g}); V2 needs cassette height <= "
          f"{D - 2 * (WALL + RAIL_W + MIN_GAP):g} (current {HC:g})")
    report("V1", T=t1)
    report("V2", hc=D - 2 * (WALL + RAIL_W + MIN_GAP))
