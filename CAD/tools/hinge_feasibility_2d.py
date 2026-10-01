"""P0.1 hinge-axis feasibility map (exact 2D side-view model of the envelope geometry).

The base and lid envelopes share the same X extent and the hinge axis is parallel to X, so
every clearance between them lies in the Y-Z plane. This computes, for each hinge-axis grid
point, the signed clearance between the rotating lid envelope and the fixed base envelope
(positive = gap, negative = penetration depth by separating-axis minimum translation) over the
lid sweep, plus overhang, height and ground checks. Inputs come from nomad.yaml (working values
where TBD). Output is modeled geometry, not a hinge decision.

Usage:  py CAD/tools/hinge_feasibility_2d.py OUT.csv [CLOSED_GAP ...]
  CLOSED_GAP values override LID_CLOSED_GAP for what-if maps (MIN_GAP stays the requirement).
"""

import csv
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from yaml_to_featurescript import YAML_PATH, flatten, parse_restricted_yaml, resolve  # noqa: E402

P, _ = resolve(flatten(parse_restricted_yaml(YAML_PATH.read_text(encoding="utf-8"))))
V = {k: v for k, (v, _) in P.items()}
D, H, G = V["BODY_DEPTH"], V["BODY_HEIGHT"], V["LID_CLOSED_GAP"]
# STUDY INPUT PINNED (2026-09-26, Round E0.5): Rounds A.1 / A.2 / A.2b were run with the Round A lid placeholder
# LID_THICKNESS = 25. nomad.yaml now derives LID_THICKNESS from the Round D.1 stack (37.6); pinning keeps this
# study's report (hinge_feasibility_map.md, closed_gap_sweep.md) reproducible. Current-lid hinge checks: c2_screening.py.
T = 25.0
MIN_GAP = V["MIN_GAP"]
ANG_NOM, ANG_MAX = V["LID_ANGLE_NOMINAL"], V["LID_ANGLE_MAX"]

INSETS = [-6, -4, -2, 0, 2, 4, 6, 8, 10]           # HINGE_AXIS_OFFSET, mm (negative = behind rear face)
HEIGHTS = list(range(-4, 27, 2))                   # HINGE_AXIS_HEIGHT above base top, mm
STEP = 5.0                                         # sweep sampling, deg (as A.1)
FINE_STEP = 0.1                                    # sensitivity check only


def rect(y0, y1, z0, z1):
    return [(y0, z0), (y1, z0), (y1, z1), (y0, z1)]


BASE = rect(0, D, 0, H)
KEYBOARD = rect(V["BASE_FRONT_MARGIN"] + V["TRACKPAD_DEPTH"] + V["TRACKPAD_KEYBOARD_GAP"],
                V["BASE_FRONT_MARGIN"] + V["TRACKPAD_DEPTH"] + V["TRACKPAD_KEYBOARD_GAP"] + V["KEYBOARD_DEPTH"],
                H - V["KEYBOARD_TOP_RECESS"] - V["KEYBOARD_THICKNESS"], H - V["KEYBOARD_TOP_RECESS"])
TRACKPAD = rect(V["BASE_FRONT_MARGIN"], V["BASE_FRONT_MARGIN"] + V["TRACKPAD_DEPTH"],
                H - V["TRACKPAD_TOP_RECESS"] - V["TRACKPAD_THICKNESS"], H - V["TRACKPAD_TOP_RECESS"])
_dc = D / 2 - V["DISPLAY_VERTICAL_OFFSET"]


def lid_polys(gap):
    """Closed-pose lid envelope and display, resting `gap` (LID_CLOSED_GAP) above the base top."""
    return (rect(0, D, H + gap, H + gap + T),
            rect(_dc - V["DISPLAY_HEIGHT"] / 2, _dc + V["DISPLAY_HEIGHT"] / 2, H + gap, H + gap + V["DISPLAY_THICKNESS"]))


def rotate(poly, axis, deg):
    """Lid opening rotation about an X-parallel axis; positive angle raises the free (front) edge."""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    ay, az = axis
    return [(ay + (y - ay) * c + (z - az) * s, az - (y - ay) * s + (z - az) * c) for y, z in poly]


def _axes(poly):
    for i in range(len(poly)):
        (y0, z0), (y1, z1) = poly[i], poly[(i + 1) % len(poly)]
        ny, nz = -(z1 - z0), y1 - y0
        n = math.hypot(ny, nz)
        yield ny / n, nz / n


def _seg_dist(p, a, b):
    ay, az = a
    dy, dz = b[0] - ay, b[1] - az
    t = max(0.0, min(1.0, ((p[0] - ay) * dy + (p[1] - az) * dz) / (dy * dy + dz * dz)))
    return math.hypot(p[0] - (ay + t * dy), p[1] - (az + t * dz))


def signed_clearance(pa, pb):
    """Gap between convex polygons if separated; minus the penetration depth if overlapping."""
    mtd = math.inf
    for ny, nz in list(_axes(pa)) + list(_axes(pb)):
        a = [y * ny + z * nz for y, z in pa]
        b = [y * ny + z * nz for y, z in pb]
        overlap = min(max(a), max(b)) - max(min(a), min(b))
        if overlap <= 1e-12:
            break
        mtd = min(mtd, overlap)
    else:
        return -mtd
    d = math.inf
    for P1, P2 in ((pa, pb), (pb, pa)):
        for p in P1:
            for i in range(len(P2)):
                d = min(d, _seg_dist(p, P2[i], P2[(i + 1) % len(P2)]))
    return d


def angles(step):
    n = int(round(ANG_MAX / step))
    return [i * step for i in range(n + 1)]


def evaluate(inset, height, gap=G):
    LID, DISPLAY = lid_polys(gap)
    axis = (D - inset, H + height)
    res = {"closed_gap": gap, "inset": inset, "height": height, "axis_y": axis[0], "axis_z": axis[1]}
    worst, worst_ang, worst_open, worst_open_ang = math.inf, None, math.inf, None
    ground_min, other_min = math.inf, math.inf
    for ang in angles(STEP):
        lid, disp = rotate(LID, axis, ang), rotate(DISPLAY, axis, ang)
        s = signed_clearance(lid, BASE)
        if s < worst:
            worst, worst_ang = s, ang
        if ang > 0 and s < worst_open:
            worst_open, worst_open_ang = s, ang
        ground_min = min(ground_min, min(z for _, z in lid))
        other_min = min(other_min, signed_clearance(disp, KEYBOARD), signed_clearance(disp, TRACKPAD))
    fine = min(signed_clearance(rotate(LID, axis, a), BASE) for a in angles(FINE_STEP))
    res.update(min_clear=worst, min_clear_angle=worst_ang, min_clear_open=worst_open,
               min_clear_open_angle=worst_open_ang, max_intrusion=max(0.0, -worst),
               min_clear_fine=fine, ground_min_z=ground_min, display_kbd_tp_min=other_min)
    for tag, ang in (("105", ANG_NOM), ("135", ANG_MAX)):
        lid = rotate(LID, axis, ang)
        res[f"overhang_{tag}"] = max(D, max(y for y, _ in lid)) - D
        res[f"height_{tag}"] = max(H, max(z for _, z in lid))
    res["feasible"] = worst >= MIN_GAP - 1e-6 and ground_min >= -1e-6
    return res


def main(out, gaps):
    rows = [evaluate(i, h, g) for g in gaps for h in HEIGHTS for i in INSETS]
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        for r in rows:
            w.writerow({k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()})
    print(f"wrote {out}: {len(rows)} rows, closed gaps {gaps} "
          f"(D={D} H={H} T={T} MIN_GAP={MIN_GAP}, sweep 0-{ANG_MAX} deg step {STEP})")
    if G not in gaps:
        return
    rows = [r for r in rows if r["closed_gap"] == G]
    for ref in ((0, 0), (8, 0)):
        r = next(x for x in rows if (x["inset"], x["height"]) == ref)
        print(f"  check {ref}: min {r['min_clear']:.3f} @ {r['min_clear_angle']} deg, "
              f"105 o{r['overhang_105']:.1f} z{r['height_105']:.1f}, 135 o{r['overhang_135']:.1f} z{r['height_135']:.1f}")
    r = evaluate(8, G + T / 2)
    print(f"  check (8, {G + T / 2}): min {r['min_clear']:.3f} @ {r['min_clear_angle']} deg, "
          f"105 o{r['overhang_105']:.1f} z{r['height_105']:.1f}, 135 o{r['overhang_135']:.1f} z{r['height_135']:.1f}")


if __name__ == "__main__":
    # Optional extra args: closed-gap values (LID_CLOSED_GAP what-ifs). Default: the YAML value.
    main(sys.argv[1], [float(a) for a in sys.argv[2:]] or [G])
