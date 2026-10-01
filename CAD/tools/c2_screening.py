"""Round C.2 architectural screening (analysis only): lid/hinge/port feasibility map + side-port scan.

Task 1: rear-port feasibility over lid thickness x hinge-axis height x maximum opening angle, using the
D-006 rear-edge hinge geometry (axis inset HINGE_AXIS_OFFSET = 0, height h above the base top), the
working 2.0 closed gap, MIN_GAP, and the Round C rear plug zone (Z PORT_PANEL_BOTTOM..+HEIGHT, 45 mm
behind the rear face). A combination is geometrically feasible when, over the whole sweep 0..theta_max:
lid-to-plug-zone clearance >= MIN_GAP, lid-to-base-envelope clearance >= MIN_GAP, lid above ground.

Task 2: side-port scan along both side walls (and the rear-face corners) against the Round C base parts,
the lid sweep and the B.1 V1 solar cassettes (with the B.1 minimal fixes: stowed, partially and fully
deployed, tilted) plus a hand-access gap. Solar geometry is NOT changed.

  py CAD/tools/c2_screening.py [--csv OUT.csv]

Evidence level: modeled (exact 2D/2.5D envelope geometry on working values); hand-access threshold inferred.
"""

import csv
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import base_v01_layout as bl  # noqa: E402
import hinge_feasibility_2d as hm  # noqa: E402
import solar_v1_feasibility as sv  # noqa: E402

P = bl.PARAMS
ENV, PARTS = bl.evaluate()
D, H, G, W = P["BODY_DEPTH"], P["BODY_HEIGHT"], P["LID_CLOSED_GAP"], P["BODY_WIDTH"]
MIN_GAP, PLUG = P["MIN_GAP"], P["PLUG_KEEPOUT_LENGTH"]
PZ0, PZ1 = ENV["PZ0"], ENV["PZ1"]
INSET = P["HINGE_AXIS_OFFSET"]

THICK = [25, 27.5, 30, 31.5, 35, 40, 42.5, 45]
HEIGHTS = [0, 2, 4, 6, 8, 10, 12]
ANGLES = [105, 115, 120, 125, 130, 135]
STEP = 0.5
HAND_GAP = 60.0      # ASSUMPTION (inferred): free height above a port for fingers + plug body


# ---------------------------------------------------------------- Task 1
BASE = hm.rect(0, D, 0, H)
ZONE = hm.rect(D, D + PLUG, PZ0, PZ1)


def sweep_state(T, h, ang):
    axis = (D - INSET, H + h)
    lid = hm.rotate(hm.rect(0, D, H + G, H + G + T), axis, ang)
    return hm.signed_clearance(lid, ZONE), hm.signed_clearance(lid, BASE), min(z for _, z in lid)


def feasibility(T, h):
    """Walk the sweep; return per-angle running minima and the max feasible opening."""
    port_min, base_min, ground_min = math.inf, math.inf, math.inf
    max_ok, running = None, {}
    a = 0.0
    while a <= 180.0 + 1e-9:
        pc, bc, gz = sweep_state(T, h, a)
        port_min, base_min, ground_min = min(port_min, pc), min(base_min, bc), min(ground_min, gz)
        ok = port_min >= MIN_GAP - 1e-9 and base_min >= MIN_GAP - 1e-9 and ground_min >= -1e-9
        if ok:
            max_ok = a
        running[round(a, 1)] = (port_min, base_min, ok)
        if not ok:
            break
        a += STEP
    # keep filling running minima past the first failure for the reported angles
    while a <= 180.0 + 1e-9:
        pc, bc, _ = sweep_state(T, h, a)
        port_min, base_min = min(port_min, pc), min(base_min, bc)
        running[round(a, 1)] = (port_min, base_min, False)
        a += STEP
    return max_ok, running


# ---------------------------------------------------------------- Task 2
SOLAR = sv.config(fix=True)          # B.1 V1 with its minimal fixes (lid 31.5); geometry unchanged here
SOLAR_LIDS = [0, 60, 90, 105, 120, 135]
TILTS = [-75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75]
EXTS = [0.0, 0.25, 0.5, 0.75, 1.0]


def solar_world(ext, tilt, lid):
    parts = {}
    for s in (1, -1):
        for k, v in sv.solar_side(SOLAR, s, ext, tilt if ext == 1 else 0).items():
            if k[0] != "R":                   # fixed rail stays inside the lid
                parts[k] = v
    return sv.to_world(parts, lid)


SOLAR_STATES = [(e, t, l) for l in SOLAR_LIDS for e in EXTS for t in (TILTS if e == 1 else [0])]
SOLAR_CACHE = [(st, solar_world(*st)) for st in SOLAR_STATES]


def side_slice_checks(side, y0, y1):
    """Side wall at X = side * W/2, port slice Y y0..y1, Z PZ0..PZ1, plug zone PLUG outward."""
    xo0, xo1 = (W / 2, W / 2 + PLUG) if side > 0 else (-W / 2 - PLUG, -W / 2)
    zone = hm.rect(y0, y1, PZ0, PZ1)
    # solar: plug clearance (min over states) and hand gap above the zone (deployed states only)
    plug_min, hand_min, worst, plug_open = math.inf, math.inf, None, math.inf
    for (ext, tilt, lid), world in SOLAR_CACHE:
        for k, (x0, x1, poly) in world.items():
            if x1 <= xo0 or x0 >= xo1:
                continue
            c = hm.signed_clearance(poly, zone)
            if c < plug_min:
                plug_min, worst = c, (k, ext, tilt, lid)
            if lid >= 60 or ext == 0:
                plug_open = min(plug_open, c)
            if ext == 1 and lid >= 90:
                # lowest solar Z over the slice's Y range (clip the polygon to y0..y1)
                zs = _clip_min_z(poly, y0, y1)
                if zs is not None:
                    hand_min = min(hand_min, zs - PZ1)
    # internal: connector keep-out behind the wall vs Round C parts (A placement)
    kx0, kx1 = (ENV["IX"] - P["PORT_KEEPOUT_DEPTH"], ENV["IX"]) if side > 0 else (-ENV["IX"], -ENV["IX"] + P["PORT_KEEPOUT_DEPTH"])
    keep = ("box", "side_ports", [kx0, y0, PZ0, kx1, y1, PZ1])
    hits = []
    for name, cat, prims in PARTS:
        if cat == "X" or name.startswith("KEEPOUT_PORTS"):
            continue
        for p in prims:
            if name == "BASE_SHELL" and p[1] in ("wall_left", "wall_right"):
                continue                      # the wall itself gets the port notch
            d, ov = bl.prim_dist(keep, p)
            need = 0.0 if name in ("SERVICE_PANEL_MAIN", "BATTERY_DOOR") else MIN_GAP
            if ov or d < need - 1e-9:
                hits.append(name if name != "BASE_SHELL" else p[1])
    return plug_min, hand_min, worst, sorted(set(hits)), plug_open


def _clip_min_z(poly, y0, y1):
    zs, n = [], len(poly)
    for i in range(n):
        (ya, za), (yb, zb) = poly[i], poly[(i + 1) % n]
        for y, z in ((ya, za), (yb, zb)):
            if y0 <= y <= y1:
                zs.append(z)
        for yc in (y0, y1):
            if (ya - yc) * (yb - yc) < 0:
                zs.append(za + (yc - ya) / (yb - ya) * (zb - za))
    return min(zs) if zs else None


def merge(slices):
    out, cur = [], None
    for y0, y1, ok in slices:
        if ok and cur and abs(cur[1] - y0) < 1e-9:
            cur = (cur[0], y1)
        elif ok:
            if cur:
                out.append(cur)
            cur = (y0, y1)
        else:
            if cur:
                out.append(cur)
            cur = None
    if cur:
        out.append(cur)
    return out


def main(argv):
    # ---- Task 1
    rows = []
    print("== TASK 1: rear-port feasibility (D-006 rear-edge hinge, inset 0; gap 2; zone Z "
          f"{PZ0:g}-{PZ1:g}, plug {PLUG:g}; MIN_GAP {MIN_GAP:g}) ==")
    print("  cell = min rear-plug clearance over 0..theta_max (mm); '*' = infeasible (port < MIN_GAP, lid-base < MIN_GAP or ground)")
    print(f"  {'T':>5} {'h':>3} {'max open':>8} | " + " ".join(f"{a:>7}" for a in ANGLES) + " | lid-base min @135")
    for T in THICK:
        for h in HEIGHTS:
            max_ok, run = feasibility(T, h)
            cells = []
            for a in ANGLES:
                pc, bc, ok = run[float(a)]
                cells.append(f"{pc:6.2f}{' ' if ok else '*'}")
                rows.append({"T": T, "h": h, "theta_max": a, "port_clearance": round(pc, 3),
                             "lid_base_clearance": round(bc, 3), "feasible": ok, "max_feasible_opening": max_ok})
            print(f"  {T:5.1f} {h:3d} {('%.1f' % max_ok) if max_ok is not None else '--':>8} | " + " ".join(cells)
                  + f" | {run[135.0][1]:6.2f}")
    print("  closed form (plug long enough, theta > 90): port clearance ~ H + h + (G + T - h) cos(theta) - port top")
    if "--csv" in argv:
        out = Path(argv[argv.index("--csv") + 1])
        with out.open("w", newline="", encoding="utf-8") as f:
            wr = csv.DictWriter(f, fieldnames=list(rows[0]))
            wr.writeheader()
            wr.writerows(rows)
        print(f"  wrote {out}")

    # ---- Task 2
    print("\n== TASK 2: side-port scan (Round C base A placement; B.1 V1 solar with fixes, lid 31.5; "
          f"{len(SOLAR_STATES)} solar states) ==")
    print(f"  lid sweep: the lid spans X +/-{W / 2:g} = base width, so it never enters a side plug zone (|X| > {W / 2:g})")
    step = 5.0
    for side, label in ((1, "RIGHT"), (-1, "LEFT")):
        ext_slices, int_slices, detail, open_slices = [], [], [], []
        y = ENV["IY0"]
        while y + step <= ENV["IY1"] + 1e-9:
            pm, hg, wst, hits, po = side_slice_checks(side, y, y + step)
            ext_slices.append((y, y + step, pm >= MIN_GAP - 1e-9))
            open_slices.append((y, y + step, po >= MIN_GAP - 1e-9))
            int_slices.append((y, y + step, not hits))
            detail.append((y, y + step, pm, hg, hits, wst))
            y += step
        print(f"  {label} side wall (X {side * W / 2:+g}), zone Z {PZ0:g}-{PZ1:g}, plug {PLUG:g} outward:")
        bad = [d for d in detail if d[2] < MIN_GAP - 1e-9]
        if bad:
            w = min(bad, key=lambda d: d[2])
            print(f"    solar interference: worst {w[2]:.2f} at Y {w[0]:g}-{w[1]:g} by {w[5][0]} (ext {w[5][1]}, tilt {w[5][2]}, lid {w[5][3]} deg)")
            states = sorted({(d[5][1], d[5][3]) for d in bad})
            print(f"    interfering (ext, lid) states seen as worst: {states}")
        ext_ok = merge(ext_slices)
        print("    EXTERNALLY clear Y ranges (solar all states >= MIN_GAP; lid never enters): "
              + (", ".join(f"{a:g}-{b:g}" for a, b in ext_ok) if ext_ok else "none"))
        open_ok = merge(open_slices)
        print("    EXTERNALLY clear if cassettes are never deployed with the lid below 60 deg: "
              + ", ".join(f"{a:g}-{b:g}" for a, b in open_ok))
        for a, b in ext_ok:
            hg = min(d[3] for d in detail if d[0] >= a - 1e-9 and d[1] <= b + 1e-9)
            print(f"      Y {a:g}-{b:g}: min deployed-cassette height above the zone {hg:.1f} "
                  f"({'>=' if hg >= HAND_GAP else '<'} {HAND_GAP:g} assumed for hand access)")
        blocked = {}
        for y0, y1, pm, hg, hits, wst in detail:
            for hname in hits:
                blocked.setdefault(hname, []).append((y0, y1))
        print("    INTERNAL conflicts with the Round C (concept A) layout:")
        for hname, spans in blocked.items():
            m = merge([(a, b, True) for a, b in spans])
            print(f"      {hname}: Y " + ", ".join(f"{a:g}-{b:g}" for a, b in m))
        both = merge([(e[0], e[1], e[2] and i[2]) for e, i in zip(ext_slices, int_slices)])
        print("    feasible with today's internal layout: " + (", ".join(f"{a:g}-{b:g}" for a, b in both) if both else "none"))
    # rear-face corners (outside the Round C port panels): internal + Task 1 constraint
    print("  REAR-FACE CORNERS (X 110-148): internal conflicts:")
    for side in (1, -1):
        x0, x1 = (110.0, ENV["IX"]) if side > 0 else (-ENV["IX"], -110.0)
        keep = ("box", "corner_ports", [x0, ENV["TRY1"], PZ0, x1, ENV["IY1"], PZ1])
        hits = sorted({(n if n != "BASE_SHELL" else p[1]) for n, c, pr in PARTS if c != "X" and not n.startswith("KEEPOUT_PORTS") and not n.startswith("PORT_PANEL")
                       for p in pr if (n != "BASE_SHELL" or p[1].startswith("boss")) and
                       (bl.prim_dist(keep, p)[1] or bl.prim_dist(keep, p)[0] < MIN_GAP - 1e-9)})
        print(f"    {'right' if side > 0 else 'left'}: {hits}; external: same lid-sweep constraint as Task 1")


if __name__ == "__main__":
    main(sys.argv[1:])
