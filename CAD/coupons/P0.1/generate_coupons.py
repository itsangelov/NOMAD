"""P0.1 test coupons A (solar rail) and B (rear shell): parametric source, STL + OpenSCAD generator.

This file is the parametric master for the coupons in prototypes/P0.1/coupons/P01_test_coupons.md.
Standard library only. Each part is CSG: (union of added boxes/cylinders) minus (union of subtracted
boxes/cylinders), in PRINT orientation (Z = build direction, all coordinates >= 0).

Outputs (next to this file):
  stl/*.stl   binary STL, mm. Meshed on an axis-aligned cell grid: box faces are exact, round holes are
              stepped at FINE mm (0.1), which is below the 0.4 nozzle / 0.2 layer resolution. Watertight
              by construction and verified (every edge shared by exactly two faces, opposite direction).
  scad/*.scad the same CSG for OpenSCAD (independent re-render / cross-check; regenerate from here).

Usage:  py CAD/coupons/P0.1/generate_coupons.py [--rib-heights 6,8,11]
"""

import math
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FINE = 0.1                       # hole step size, mm

# ------------------------------------------------------------------ parameters (from P01_test_coupons.md)
# Coupon A: rail (test-critical unless marked FIXTURE)
RAIL_CHANNEL_LEN = 198.0         # V1+fix rail length = travel 158 + carriage 40
END_STOP = 2.0                   # closed end beyond the channel (keeps stowed carriage centre at X 178)
FLOOR, LIP_T, WALL = 2.5, 2.5, 2.5
CH_W, CH_H, SLOT_W = 22.6, 8.0, 17.6
RAIL_H = FLOOR + CH_H + LIP_T    # 13.0
EAR_W, PAD_LEN = 12.0, 28.5
INSERT_D, INSERT_DEPTH = 4.0, 7.0      # M3 heat-set insert hole (P0.2-HW): 4.0 = smallest common pilot (drill up per datasheet); 7.0 = 5.7 insert + melt relief
INSERT_X = (7.0, 21.5)
A2_WALL = 4.1                          # thickened side wall hosting the strip slot
STRIP_T, STRIP_H = 2.0, 10.0           # flat-strip envelope (10x2 Al; 10x1.5 steel also fits)
STRIP_CLR_T, STRIP_CLR_H = 0.3, 0.4
STRIP_Z0 = 1.3
# carriage + load hardware (FIXTURE except the fits)
CAR_LEN, CAR_CLR_Y, CAR_CLR_Z = 40.0, 0.3, 0.6
POST_CLR = 0.5
POST_H = 12.6                          # FIXTURE: rod clears the lips by 1.75 mm
LOAD_HOLE_D, LOAD_HOLE_BELOW_TOP = 5.5, 5.0
EDGE_RELIEF = 0.5
PLATFORM = (60.0, 60.0, 6.0)           # FIXTURE alternative load method (pocket fits over the post)
PLATFORM_POCKET_DEPTH, PLATFORM_CLR = 3.0, 0.3
# pad stub (FIXTURE except thickness 6.0 = bezel 2.5 + pad 3.5 and the free edge at the pad end)
PAD_BASE = (60.0, 70.0, 6.0)
PAD_CLAMP_LEN = 31.5                   # base extends this far outboard of the rail end (clamp zone)
PAD_Y_OFFSET = 21.0                    # rail ear outer face sits at base Y 9 (= 21 - EAR_W)
SCREW_CLEAR_D, CBORE_D, CBORE_DEPTH = 3.4, 6.5, 3.5
SURROGATE_A = (170.0, 30.0, 5.0)       # display surrogate (5.0 -> 1.0 mm gap under a 6.0 pad)

# Coupon B: rear shell
SPAN, BAND, STRIP_WIDTH = 202.0, 14.0, 90.0
PLATE_T = 2.5
FRAME_BASE_T, SHELF_H = 4.0, 10.0
B_SCREW_POS = [(7.0, 10.0), (7.0, 80.0)]                 # per band (mirrored to the other band)
RIB_T, RIB_Y = 2.0, (15.0, 45.0, 75.0)                   # longitudinal ribs across the strip width
RIB_X_TRANS = (BAND, BAND + SPAN / 2 + 0.0, BAND + SPAN) # transverse ribs: support edges + mid-span
RIB_HEIGHTS = [6.0, 8.0, 11.0]
CLEAR_BLOCK = (60.0, 60.0, SHELF_H - 1.0)                # top 1.0 mm below the plate seat
LOAD_PAD = (20.0, 20.0, 5.0)

BEDS = {"A": (220.0, 220.0), "B": (235.0, 95.0)}         # stated minimum bed per coupon family


# ------------------------------------------------------------------ CSG primitives
def box(x0, y0, z0, x1, y1, z1):
    return ("box", (x0, y0, z0, x1, y1, z1))


def cylz(cx, cy, d, z0, z1):
    return ("cylz", (cx, cy, d / 2, z0, z1))


def teardrop_y(cx, cz, d, y0, y1):
    """Horizontal hole along Y with a 45-degree roof point (prints without support)."""
    return ("tdy", (cx, cz, d / 2, y0, y1))


def inside(prim, p):
    k, a = prim
    x, y, z = p
    if k == "box":
        return a[0] < x < a[3] and a[1] < y < a[4] and a[2] < z < a[5]
    if k == "cylz":
        return a[3] < z < a[4] and (x - a[0]) ** 2 + (y - a[1]) ** 2 < a[2] ** 2
    if k == "tdy":
        cx, cz, r, y0, y1 = a
        if not y0 < y < y1:
            return False
        dx, dz = x - cx, z - cz
        if dx * dx + dz * dz < r * r:
            return True
        # triangle: apex (0, r*sqrt2), base corners (+-r/sqrt2, r/sqrt2)
        return dz > r / math.sqrt(2) and abs(dx) < r * math.sqrt(2) - dz
    raise ValueError(k)


class Part:
    def __init__(self, name, family, adds, subs, role):
        self.name, self.family, self.adds, self.subs, self.role = name, family, adds, subs, role

    def solid(self, p):
        return any(inside(a, p) for a in self.adds) and not any(inside(s, p) for s in self.subs)

    def bbox(self):
        bs = [a[1] for a in self.adds if a[0] == "box"]
        return tuple(min(b[i] for b in bs) for i in range(3)) + tuple(max(b[i + 3] for b in bs) for i in range(3))


# ------------------------------------------------------------------ parts
def rail(stiffener):
    wall = A2_WALL if stiffener else WALL
    w = CH_W + 2 * wall
    y0 = EAR_W                                   # rail body starts after the ear
    L = RAIL_CHANNEL_LEN + END_STOP
    lip = (w - SLOT_W) / 2
    adds = [box(0, y0, 0, L, y0 + w, RAIL_H), box(0, 0, 0, PAD_LEN, EAR_W, RAIL_H)]
    subs = [box(-1, y0 + wall, FLOOR, RAIL_CHANNEL_LEN, y0 + wall + CH_W, FLOOR + CH_H),       # channel
            box(-1, y0 + lip, FLOOR + CH_H - 0.01, RAIL_CHANNEL_LEN, y0 + lip + SLOT_W, RAIL_H + 1)]  # top slot
    subs += [cylz(x, EAR_W / 2, INSERT_D, -1, INSERT_DEPTH) for x in INSERT_X]
    if stiffener:
        st, sh = STRIP_T + STRIP_CLR_T, STRIP_H + STRIP_CLR_H
        for yw in (y0, y0 + w - wall):
            ys = yw + (wall - st) / 2
            subs.append(box(-1, ys, STRIP_Z0, RAIL_CHANNEL_LEN, ys + st, STRIP_Z0 + sh))
    name = "A2_rail_stiffener_slots" if stiffener else "A1_rail_printed"
    return Part(name, "A", adds, subs, "TEST: rail section, length, ear/pad interface" + (", strip slots" if stiffener else ""))


def carriage():
    bw, bh = CH_W - 2 * CAR_CLR_Y, CH_H - CAR_CLR_Z
    pw = SLOT_W - 2 * POST_CLR
    top = bh + POST_H
    e = EDGE_RELIEF
    adds = [box(0, 0, 0, CAR_LEN, bw, bh), box(0, (bw - pw) / 2, bh - 0.01, CAR_LEN, (bw + pw) / 2, top)]
    subs = [box(-1, -1, -1, CAR_LEN + 1, e, e), box(-1, bw - e, -1, CAR_LEN + 1, bw + 1, e),   # bottom edge reliefs
            box(-1, -1, bh - e, CAR_LEN + 1, e, bh + 1), box(-1, bw - e, bh - e, CAR_LEN + 1, bw + 1, bh + 1),
            teardrop_y(CAR_LEN / 2, top - LOAD_HOLE_BELOW_TOP, LOAD_HOLE_D, -1, bw + 1)]
    return Part("A_carriage_load_post", "A", adds, subs, "FIT: body/post clearances; FIXTURE: post height, load hole")


def platform():
    px, py, pz = PLATFORM
    pw = SLOT_W - 2 * POST_CLR + 2 * PLATFORM_CLR
    pl = CAR_LEN + 2 * PLATFORM_CLR
    adds = [box(0, 0, 0, px, py, pz)]
    subs = [box((px - pl) / 2, (py - pw) / 2, pz - PLATFORM_POCKET_DEPTH, (px + pl) / 2, (py + pw) / 2, pz + 1)]
    return Part("A_load_platform", "A", adds, subs, "FIXTURE: weight platform over the post (print pocket up)")


def pad_stub():
    bx, by, bz = PAD_BASE
    holes = [(PAD_CLAMP_LEN + x, PAD_Y_OFFSET - EAR_W / 2) for x in INSERT_X]
    subs = [cylz(x, y, SCREW_CLEAR_D, -1, bz + 1) for x, y in holes] + [cylz(x, y, CBORE_D, -1, CBORE_DEPTH) for x, y in holes]
    return Part("A_pad_stub", "A", [box(0, 0, 0, bx, by, bz)], subs,
                "TEST: 6.0 thickness (1.0 mm display gap), free edge at pad end; FIXTURE: clamp area")


def simple(name, fam, dims, role):
    return Part(name, fam, [box(0, 0, 0, *dims)], [], role)


def b_frame():
    L = SPAN + 2 * BAND
    top = FRAME_BASE_T + SHELF_H
    adds = [box(0, 0, 0, L, STRIP_WIDTH, FRAME_BASE_T), box(0, 0, FRAME_BASE_T - 0.01, BAND, STRIP_WIDTH, top),
            box(L - BAND, 0, FRAME_BASE_T - 0.01, L, STRIP_WIDTH, top)]
    subs = [cylz(x, y, INSERT_D, top - INSERT_DEPTH, top + 1) for x, y in b_screw_xy()]
    return Part("B_frame_supports", "B", adds, subs, "TEST: 202 clear span, 14 bands, shelf-top plane, insert positions")


def b_screw_xy():
    L = SPAN + 2 * BAND
    return B_SCREW_POS + [(L - x, y) for x, y in B_SCREW_POS]


def b_plate(rib_h):
    L = SPAN + 2 * BAND
    adds = [box(0, 0, 0, L, STRIP_WIDTH, PLATE_T)]
    if rib_h:
        for y in RIB_Y:
            adds.append(box(BAND, y - RIB_T / 2, PLATE_T - 0.01, BAND + SPAN, y + RIB_T / 2, PLATE_T + rib_h))
        for x in RIB_X_TRANS:
            adds.append(box(x - RIB_T / 2, 0, PLATE_T - 0.01, x + RIB_T / 2, STRIP_WIDTH, PLATE_T + rib_h))
    subs = [cylz(x, y, SCREW_CLEAR_D, -1, PLATE_T + (rib_h or 0) + 1) for x, y in b_screw_xy()]
    name = f"B2_plate_ribbed_h{int(rib_h):02d}" if rib_h else "B1_plate_plain_2p5"
    return Part(name, "B", adds, subs, "TEST: plate/skin 2.5, span, rib section" if rib_h else "TEST: plain 2.5 plate, span")


def all_parts(rib_heights):
    return [rail(False), rail(True), carriage(), platform(), pad_stub(),
            simple("A_display_surrogate", "A", SURROGATE_A, "TEST: 5.0 thickness (1.0 mm reference gap)"),
            b_frame(), simple("B_clearance_block", "B", CLEAR_BLOCK, "TEST: 9.0 height (1.0 mm reference gap)"),
            b_plate(0), *[b_plate(h) for h in rib_heights],
            simple("B_load_pad", "B", LOAD_PAD, "FIXTURE: spreads the centre load")]


# ------------------------------------------------------------------ meshing
def grid(part):
    b = part.bbox()
    axes = [set(), set(), set()]
    for kind, a in part.adds + part.subs:
        if kind == "box":
            for i in range(3):
                axes[i].update((a[i], a[i + 3]))
        else:
            if kind == "cylz":
                cx, cy, r, z0, z1 = a
                radial, axial, ax_i = ((0, cx), (1, cy)), (z0, z1), 2
            else:
                cx, cz, r, y0, y1 = a
                radial, axial, ax_i = ((0, cx), (2, cz)), (y0, y1), 1
                r_top = r * math.sqrt(2)
            axes[ax_i].update(axial)
            for ai, c in radial:
                hi = r_top if (kind == "tdy" and ai == 2) else r
                lo = -r
                n0, n1 = math.floor((c + lo) / FINE) - 1, math.ceil((c + hi) / FINE) + 1
                axes[ai].update(round(k * FINE, 6) for k in range(n0, n1 + 1))
    out = []
    for i in range(3):
        vals = sorted({round(v, 6) for v in axes[i] if b[i] - 1e-9 <= v <= b[i + 3] + 1e-9} | {b[i], b[i + 3]})
        out.append(vals)
    return out


def mesh(part):
    gx, gy, gz = grid(part)
    nx, ny, nz = len(gx) - 1, len(gy) - 1, len(gz) - 1
    cx = [(gx[i] + gx[i + 1]) / 2 for i in range(nx)]
    cy = [(gy[j] + gy[j + 1]) / 2 for j in range(ny)]
    cz = [(gz[k] + gz[k + 1]) / 2 for k in range(nz)]
    solid = [[[part.solid((cx[i], cy[j], cz[k])) for k in range(nz)] for j in range(ny)] for i in range(nx)]

    def s(i, j, k):
        return 0 <= i < nx and 0 <= j < ny and 0 <= k < nz and solid[i][j][k]

    tris = []

    def quad(p0, p1, p2, p3):
        tris.append((p0, p1, p2))
        tris.append((p0, p2, p3))

    for i in range(nx):
        x0, x1 = gx[i], gx[i + 1]
        for j in range(ny):
            y0, y1 = gy[j], gy[j + 1]
            for k in range(nz):
                if not solid[i][j][k]:
                    continue
                z0, z1 = gz[k], gz[k + 1]
                if not s(i - 1, j, k):
                    quad((x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0))
                if not s(i + 1, j, k):
                    quad((x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1))
                if not s(i, j - 1, k):
                    quad((x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1))
                if not s(i, j + 1, k):
                    quad((x0, y1, z0), (x0, y1, z1), (x1, y1, z1), (x1, y1, z0))
                if not s(i, j, k - 1):
                    quad((x0, y0, z0), (x0, y1, z0), (x1, y1, z0), (x1, y0, z0))
                if not s(i, j, k + 1):
                    quad((x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1))
    return tris, solid, (gx, gy, gz)


def write_stl(path, tris):
    with open(path, "wb") as f:
        f.write(b"NOMAD P0.1 coupon, mm, generated by generate_coupons.py".ljust(80, b" "))
        f.write(struct.pack("<I", len(tris)))
        for a, b, c in tris:
            u = [b[i] - a[i] for i in range(3)]
            v = [c[i] - a[i] for i in range(3)]
            n = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
            ln = math.sqrt(sum(t * t for t in n)) or 1.0
            f.write(struct.pack("<12fH", *[t / ln for t in n], *a, *b, *c, 0))


def manifold_report(tris):
    edges = {}
    for t in tris:
        for a, b in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
            edges[(a, b)] = edges.get((a, b), 0) + 1
    bad = sum(1 for (a, b), n in edges.items() if n != 1 or edges.get((b, a), 0) != 1)
    degenerate = sum(1 for a, b, c in tris if a == b or b == c or a == c)
    vol = sum((a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6
              for a, b, c in tris)
    return bad, degenerate, vol


def components(solid):
    nx, ny, nz = len(solid), len(solid[0]), len(solid[0][0])
    seen, comps = set(), 0
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                if solid[i][j][k] and (i, j, k) not in seen:
                    comps += 1
                    stack = [(i, j, k)]
                    seen.add((i, j, k))
                    while stack:
                        a, b, c = stack.pop()
                        for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                            n = (a + d[0], b + d[1], c + d[2])
                            if 0 <= n[0] < nx and 0 <= n[1] < ny and 0 <= n[2] < nz and solid[n[0]][n[1]][n[2]] and n not in seen:
                                seen.add(n)
                                stack.append(n)
    return comps


# ------------------------------------------------------------------ OpenSCAD export
def scad(part):
    def prim(p):
        k, a = p
        if k == "box":
            return f"translate([{a[0]:g},{a[1]:g},{a[2]:g}]) cube([{a[3] - a[0]:g},{a[4] - a[1]:g},{a[5] - a[2]:g}]);"
        if k == "cylz":
            return f"translate([{a[0]:g},{a[1]:g},{a[3]:g}]) cylinder(r={a[2]:g}, h={a[4] - a[3]:g}, $fn=64);"
        cx, cz, r, y0, y1 = a
        return (f"translate([0,{y0:g},0]) rotate([-90,0,0]) translate([0,0,0]) linear_extrude({y1 - y0:g}) "
                f"mirror([0,1,0]) hull() {{ translate([{cx:g},{cz:g}]) circle(r={r:g}, $fn=64); "
                f"translate([{cx:g},{cz + r * math.sqrt(2):g}]) square(0.01, center=true); }}")
    lines = [f"// {part.name} -- GENERATED by generate_coupons.py (edit parameters there, not here). mm, print orientation.",
             f"// role: {part.role}", "difference() {", "  union() {"]
    lines += [f"    {prim(a)}" for a in part.adds]
    lines += ["  }"] + [f"  {prim(s)}" for s in part.subs] + ["}"]
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------ sanity checks
def probes(parts):
    by = {p.name: p for p in parts}
    r1, r2, car = by["A1_rail_printed"], by["A2_rail_stiffener_slots"], by["A_carriage_load_post"]
    y1c = EAR_W + WALL + CH_W / 2
    y2c = EAR_W + A2_WALL + CH_W / 2
    checks = [
        ("A1 channel interior empty (mid-length)", not r1.solid((100, y1c, FLOOR + CH_H / 2))),
        ("A1 channel is 22.6 wide: wall solid just outside, empty just inside",
         r1.solid((100, EAR_W + WALL - 0.05, 5)) and not r1.solid((100, EAR_W + WALL + 0.05, 5))
         and not r1.solid((100, EAR_W + WALL + CH_W - 0.05, 5)) and r1.solid((100, EAR_W + WALL + CH_W + 0.05, 5))),
        ("A1 channel is 8.0 tall: floor solid below Z 2.5, empty below Z 10.5",
         r1.solid((100, y1c, FLOOR - 0.05)) and not r1.solid((100, y1c, FLOOR + CH_H - 0.05))),
        ("A1 top slot 17.6 open, retaining lips present both sides",
         not r1.solid((100, y1c - SLOT_W / 2 + 0.05, 12)) and not r1.solid((100, y1c + SLOT_W / 2 - 0.05, 12))
         and r1.solid((100, y1c - SLOT_W / 2 - 0.05, 12)) and r1.solid((100, y1c + SLOT_W / 2 + 0.05, 12))),
        ("A1 end stop solid beyond X 198, channel open at X 0",
         r1.solid((RAIL_CHANNEL_LEN + 1, y1c, 5)) and not r1.solid((0.05, y1c, 5))),
        (f"A1 ear insert holes open from below, blind at {INSERT_DEPTH:g}",
         all(not r1.solid((x, EAR_W / 2, 3)) and r1.solid((x, EAR_W / 2, INSERT_DEPTH + 0.5)) for x in INSERT_X)),
        ("A2 channel and slot same as A1 (22.6 x 8.0, 17.6)",
         not r2.solid((100, y2c, 6)) and not r2.solid((100, y2c + SLOT_W / 2 - 0.05, 12)) and r2.solid((100, y2c + SLOT_W / 2 + 0.05, 12))),
        ("A2 strip slots open at X 0 and run to X 198, closed by the end stop",
         all(not r2.solid((0.05, ys, STRIP_Z0 + 5)) and not r2.solid((RAIL_CHANNEL_LEN - 0.1, ys, STRIP_Z0 + 5))
             and r2.solid((RAIL_CHANNEL_LEN + 1, ys, STRIP_Z0 + 5))
             for ys in (EAR_W + A2_WALL / 2, EAR_W + A2_WALL + CH_W + A2_WALL / 2))),
        ("A2 strip slot fits 10x2 strip (slot 2.3 x 10.4)", STRIP_T + STRIP_CLR_T >= 2.0 and STRIP_H + STRIP_CLR_H >= 10.0),
        ("A2 skins around strip slot >= 0.8 mm", (A2_WALL - STRIP_T - STRIP_CLR_T) / 2 >= 0.8 and STRIP_Z0 >= 0.8
         and RAIL_H - (STRIP_Z0 + STRIP_H + STRIP_CLR_H) >= 0.8),
        ("carriage fits channel (measured from the parts: 0.3 per side in Y, 0.6 in Z)",
         abs((CH_W - car.bbox()[4]) / 2 - 0.3) < 1e-6 and abs(CH_H - (car.bbox()[5] - POST_H) - 0.6) < 1e-6
         and not any(r1.solid((100, EAR_W + WALL + (CH_W - car.bbox()[4]) / 2 + t, FLOOR + 0.05)) for t in (0.05, car.bbox()[4] / 2, car.bbox()[4] - 0.05))),
        ("post passes slot (0.5 per side) and carriage is retained by lips (engagement per side)",
         (CH_W - 2 * CAR_CLR_Y - SLOT_W) / 2 > 1.5 and SLOT_W - (SLOT_W - 2 * POST_CLR) == 2 * POST_CLR),
        ("load rod clears lip tops", FLOOR + (CH_H - CAR_CLR_Z) + POST_H - LOAD_HOLE_BELOW_TOP - LOAD_HOLE_D / 2 - RAIL_H > 1.0),
        ("load hole through post, teardrop apex inside post",
         not car.solid((CAR_LEN / 2, (CH_W - 2 * CAR_CLR_Y) / 2, (CH_H - CAR_CLR_Z) + POST_H - LOAD_HOLE_BELOW_TOP))
         and LOAD_HOLE_D / 2 * math.sqrt(2) < LOAD_HOLE_BELOW_TOP),
        ("stowed carriage centre at X 178 -> arm 149.5 from pad edge (X 28.5)",
         abs((RAIL_CHANNEL_LEN - CAR_LEN / 2) - PAD_LEN - 149.5) < 1e-9),
        ("pad stub gives 1.0 mm display gap (6.0 pad - 5.0 surrogate)", abs(PAD_BASE[2] - SURROGATE_A[2] - 1.0) < 1e-9),
        ("pad free edge at rail X 28.5", abs(PAD_BASE[0] - PAD_CLAMP_LEN - PAD_LEN) < 1e-9),
        ("B clear span 202 between 14 mm bands", abs((SPAN + 2 * BAND) - 2 * BAND - 202) < 1e-9),
        ("B clearance block top 1.0 mm below plate seat", abs((FRAME_BASE_T + SHELF_H) - (FRAME_BASE_T + CLEAR_BLOCK[2]) - 1.0) < 1e-9),
        ("B screws in rib-free bands (head r 2.75 clears transverse rib)",
         all(x + 2.75 < RIB_X_TRANS[0] - RIB_T / 2 for x, _ in B_SCREW_POS)),
        ("B insert bosses fit the 14 mm band (boss 8)", all(x - 4 >= 0 and x + 4 <= BAND for x, _ in B_SCREW_POS)),
    ]
    return checks


def main(argv):
    ribs = RIB_HEIGHTS
    if "--rib-heights" in argv:
        ribs = [float(v) for v in argv[argv.index("--rib-heights") + 1].split(",")]
    parts = all_parts(ribs)
    (HERE / "stl").mkdir(exist_ok=True)
    (HERE / "scad").mkdir(exist_ok=True)
    print(f"{'part':<28} {'bbox X x Y x Z (mm)':<24} {'tris':>7} {'open/nonmanifold edges':>22} {'comps':>5} {'vol cm3':>8}  bed")
    ok_all = True
    for p in parts:
        tris, solid, _ = mesh(p)
        bad, degen, vol = manifold_report(tris)
        comps = components(solid)
        b = p.bbox()
        dims = (b[3] - b[0], b[4] - b[1], b[5] - b[2])
        bed = BEDS[p.family]
        fits = (dims[0] <= bed[0] and dims[1] <= bed[1]) or (dims[1] <= bed[0] and dims[0] <= bed[1])
        ok = bad == 0 and degen == 0 and comps == 1 and fits
        ok_all &= ok
        write_stl(HERE / "stl" / f"{p.name}.stl", tris)
        (HERE / "scad" / f"{p.name}.scad").write_text(scad(p), encoding="utf-8")
        print(f"{p.name:<28} {dims[0]:>6.1f} x {dims[1]:>5.1f} x {dims[2]:>5.1f}   {len(tris):>7} {bad:>22} {comps:>5} {vol / 1000:>8.2f}  "
              f"{'OK' if fits else 'TOO BIG'} ({bed[0]:g}x{bed[1]:g})")
    print("\ngeometry probes:")
    for label, res in probes(parts):
        ok_all &= bool(res)
        print(f"  [{'PASS' if res else 'FAIL'}] {label}")
    print("\nALL CHECKS PASSED" if ok_all else "\nSOME CHECKS FAILED")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
