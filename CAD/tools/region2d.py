"""Exact 2-D region geometry for the Round E lid checks (Y-Z cross-sections of X-prisms).

Edges:   ("L", (y0, z0), (y1, z1))             straight segment
         ("A", (cy, cz), r, a0, a1)            circular arc, counter-clockwise from a0 to a1 (degrees, a0 < a1 <= a0 + 360)
Region:  Reg(outer loop, hole loops)           material = inside the outer loop and outside every hole loop

Used by e_lid_layout.py for the solar index-lock parts (index plate hole pattern, double-D keys, profiled carriage slab,
bores). Boxes and circles without holes keep their original exact code paths in e_lid_layout.py. Everything here is
exact for lines and arcs (no polygonisation), so the local model can be compared with the Onshape kernel.
Evidence level of results: modeled.
"""

import math

TOL = 1e-9
_PERTURB = 1.234567e-7          # ray-cast offset so vertices never sit exactly on the ray


class Reg:
    __slots__ = ("outer", "holes", "_bb")

    def __init__(self, outer, holes=()):
        self.outer = list(outer)
        self.holes = [list(h) for h in holes]
        self._bb = None

    def edges(self):
        out = list(self.outer)
        for h in self.holes:
            out += h
        return out

    def bbox(self):
        if self._bb is None:
            bbs = [edge_bbox(e) for e in self.outer]
            self._bb = (min(b[0] for b in bbs), min(b[1] for b in bbs), max(b[2] for b in bbs), max(b[3] for b in bbs))
        return self._bb


# ------------------------------------------------------------------ constructors
def from_poly(poly):
    n = len(poly)
    return Reg([("L", tuple(poly[i]), tuple(poly[(i + 1) % n])) for i in range(n)])


def from_circle(c, r):
    return Reg([("A", tuple(c), r, 0.0, 360.0)])


def loop_circle(c, r):
    return [("A", tuple(c), r, 0.0, 360.0)]


# ------------------------------------------------------------------ angles and points
def _ang(p, c):
    return math.degrees(math.atan2(p[1] - c[1], p[0] - c[0])) % 360.0


def in_sweep(a, a0, a1, tol=1e-9):
    span = a1 - a0
    if span >= 360.0 - tol:
        return True
    d = (a - a0) % 360.0
    return d <= span + tol or d >= 360.0 - tol


def _strict_sweep(a, a0, a1, tol=1e-7):
    span = a1 - a0
    if span >= 360.0 - 1e-9:
        return True
    d = (a - a0) % 360.0
    return tol < d < span - tol


def arc_pt(c, r, a):
    return (c[0] + r * math.cos(math.radians(a)), c[1] + r * math.sin(math.radians(a)))


def edge_ends(e):
    if e[0] == "L":
        return e[1], e[2]
    return arc_pt(e[1], e[2], e[3]), arc_pt(e[1], e[2], e[4])


def edge_bbox(e):
    if e[0] == "L":
        (y0, z0), (y1, z1) = e[1], e[2]
        return (min(y0, y1), min(z0, z1), max(y0, y1), max(z0, z1))
    c, r, a0, a1 = e[1], e[2], e[3], e[4]
    pts = [arc_pt(c, r, a0), arc_pt(c, r, a1)]
    for q in (0.0, 90.0, 180.0, 270.0):
        if in_sweep(q, a0, a1):
            pts.append(arc_pt(c, r, q))
    return (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))


def _bb_dist(a, b):
    dy = max(0.0, max(a[0], b[0]) - min(a[2], b[2]))
    dz = max(0.0, max(a[1], b[1]) - min(a[3], b[3]))
    return math.hypot(dy, dz)


# ------------------------------------------------------------------ point / edge distances
def _pt_seg(p, a, b):
    dy, dz = b[0] - a[0], b[1] - a[1]
    L2 = dy * dy + dz * dz
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((p[0] - a[0]) * dy + (p[1] - a[1]) * dz) / L2))
    return math.hypot(p[0] - (a[0] + t * dy), p[1] - (a[1] + t * dz))


def _pt_arc(p, c, r, a0, a1):
    d = math.hypot(p[0] - c[0], p[1] - c[1])
    if d < 1e-15:
        return r
    if in_sweep(_ang(p, c), a0, a1):
        return abs(d - r)
    return min(math.dist(p, arc_pt(c, r, a0)), math.dist(p, arc_pt(c, r, a1)))


def pt_edge(p, e):
    if e[0] == "L":
        return _pt_seg(p, e[1], e[2])
    return _pt_arc(p, e[1], e[2], e[3], e[4])


def _orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _seg_seg(a, b, c, d):
    o1, o2, o3, o4 = _orient(a, b, c), _orient(a, b, d), _orient(c, d, a), _orient(c, d, b)
    if ((o1 > 0) != (o2 > 0)) and ((o3 > 0) != (o4 > 0)) and o1 * o2 < 0 and o3 * o4 < 0:
        return 0.0
    return min(_pt_seg(a, c, d), _pt_seg(b, c, d), _pt_seg(c, a, b), _pt_seg(d, a, b))


def _line_circle(a, b, c, r):
    """Parameters t (on a->b) where the infinite line meets the circle; [] if it misses; tangent gives one."""
    dy, dz = b[0] - a[0], b[1] - a[1]
    fy, fz = a[0] - c[0], a[1] - c[1]
    A = dy * dy + dz * dz
    B = 2 * (fy * dy + fz * dz)
    C = fy * fy + fz * fz - r * r
    disc = B * B - 4 * A * C
    if A == 0 or disc < -1e-12:
        return [], disc
    s = math.sqrt(max(0.0, disc))
    return [(-B - s) / (2 * A), (-B + s) / (2 * A)], disc


def _seg_arc(a, b, c, r, a0, a1):
    ts, _ = _line_circle(a, b, c, r)
    dy, dz = b[0] - a[0], b[1] - a[1]
    for t in ts:
        if -1e-12 <= t <= 1 + 1e-12:
            q = (a[0] + t * dy, a[1] + t * dz)
            if in_sweep(_ang(q, c), a0, a1):
                return 0.0
    best = min(_pt_arc(a, c, r, a0, a1), _pt_arc(b, c, r, a0, a1),
               _pt_seg(arc_pt(c, r, a0), a, b), _pt_seg(arc_pt(c, r, a1), a, b))
    L2 = dy * dy + dz * dz
    if L2 > 0:
        t = ((c[0] - a[0]) * dy + (c[1] - a[1]) * dz) / L2
        if 0.0 <= t <= 1.0:
            f = (a[0] + t * dy, a[1] + t * dz)
            h = math.hypot(f[0] - c[0], f[1] - c[1])
            if h > 1e-15 and in_sweep(_ang(f, c), a0, a1):
                best = min(best, abs(h - r))
    return best


def _circle_circle(c1, r1, c2, r2):
    d = math.dist(c1, c2)
    if d < 1e-15 or d > r1 + r2 + 1e-12 or d < abs(r1 - r2) - 1e-12:
        return []
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(max(0.0, r1 * r1 - a * a))
    my, mz = c1[0] + a * (c2[0] - c1[0]) / d, c1[1] + a * (c2[1] - c1[1]) / d
    oy, oz = -(c2[1] - c1[1]) / d * h, (c2[0] - c1[0]) / d * h
    return [(my + oy, mz + oz), (my - oy, mz - oz)]


def _arc_arc(c1, r1, a0, a1, c2, r2, b0, b1):
    for q in _circle_circle(c1, r1, c2, r2):
        if in_sweep(_ang(q, c1), a0, a1) and in_sweep(_ang(q, c2), b0, b1):
            return 0.0
    best = min(_pt_arc(arc_pt(c1, r1, a0), c2, r2, b0, b1), _pt_arc(arc_pt(c1, r1, a1), c2, r2, b0, b1),
               _pt_arc(arc_pt(c2, r2, b0), c1, r1, a0, a1), _pt_arc(arc_pt(c2, r2, b1), c1, r1, a0, a1))
    d = math.dist(c1, c2)
    if d < 1e-12:
        for q in (a0, a1):
            if in_sweep(q, b0, b1):
                best = min(best, abs(r1 - r2))
        for q in (b0, b1):
            if in_sweep(q, a0, a1):
                best = min(best, abs(r1 - r2))
        return best
    u = ((c2[0] - c1[0]) / d, (c2[1] - c1[1]) / d)
    for s1 in (1, -1):
        p = (c1[0] + s1 * r1 * u[0], c1[1] + s1 * r1 * u[1])
        if not in_sweep(_ang(p, c1), a0, a1):
            continue
        for s2 in (1, -1):
            q = (c2[0] + s2 * r2 * u[0], c2[1] + s2 * r2 * u[1])
            if in_sweep(_ang(q, c2), b0, b1):
                best = min(best, math.dist(p, q))
    return best


def edge_dist(e, f):
    if e[0] == "L" and f[0] == "L":
        return _seg_seg(e[1], e[2], f[1], f[2])
    if e[0] == "L":
        return _seg_arc(e[1], e[2], f[1], f[2], f[3], f[4])
    if f[0] == "L":
        return _seg_arc(f[1], f[2], e[1], e[2], e[3], e[4])
    return _arc_arc(e[1], e[2], e[3], e[4], f[1], f[2], f[3], f[4])


# ------------------------------------------------------------------ proper (transversal) crossings
def edge_cross(e, f):
    if e[0] == "L" and f[0] == "L":
        a, b, c, d = e[1], e[2], f[1], f[2]
        o1, o2, o3, o4 = _orient(a, b, c), _orient(a, b, d), _orient(c, d, a), _orient(c, d, b)
        s = 1e-12 * max(1.0, math.dist(a, b) * math.dist(c, d))
        return o1 * o2 < -s * s and o3 * o4 < -s * s
    if e[0] == "A" and f[0] == "L":
        e, f = f, e
    if e[0] == "L":
        a, b = e[1], e[2]
        c, r, a0, a1 = f[1], f[2], f[3], f[4]
        ts, disc = _line_circle(a, b, c, r)
        if disc <= 1e-10 * max(1.0, r * r):
            return False                                  # tangent / miss
        dy, dz = b[0] - a[0], b[1] - a[1]
        for t in ts:
            if 1e-9 < t < 1 - 1e-9:
                q = (a[0] + t * dy, a[1] + t * dz)
                if _strict_sweep(_ang(q, c), a0, a1):
                    return True
        return False
    c1, r1, a0, a1 = e[1], e[2], e[3], e[4]
    c2, r2, b0, b1 = f[1], f[2], f[3], f[4]
    d = math.dist(c1, c2)
    if not (abs(r1 - r2) + 1e-9 < d < r1 + r2 - 1e-9):
        return False
    for q in _circle_circle(c1, r1, c2, r2):
        if _strict_sweep(_ang(q, c1), a0, a1) and _strict_sweep(_ang(q, c2), b0, b1):
            return True
    return False


# ------------------------------------------------------------------ containment
def _in_loop(p, loop):
    py, pz = p[0], p[1] + _PERTURB
    n = 0
    for e in loop:
        if e[0] == "L":
            (y0, z0), (y1, z1) = e[1], e[2]
            if (z0 > pz) != (z1 > pz):
                y = y0 + (pz - z0) * (y1 - y0) / (z1 - z0)
                if y > py:
                    n += 1
        else:
            c, r, a0, a1 = e[1], e[2], e[3], e[4]
            h = pz - c[1]
            if abs(h) < r:
                w = math.sqrt(r * r - h * h)
                for y in (c[0] - w, c[0] + w):
                    if y > py and in_sweep(_ang((y, pz), c), a0, a1, tol=0.0):
                        n += 1
    return n % 2 == 1


def in_region(p, R):
    if not _in_loop(p, R.outer):
        return False
    return not any(_in_loop(p, h) for h in R.holes)


def _edge_samples(e, fracs=(0.1, 0.5, 0.9)):
    out = []
    if e[0] == "L":
        (y0, z0), (y1, z1) = e[1], e[2]
        L = math.hypot(y1 - y0, z1 - z0)
        if L == 0:
            return []
        n = (-(z1 - z0) / L, (y1 - y0) / L)
        for f in fracs:
            out.append(((y0 + f * (y1 - y0), z0 + f * (z1 - z0)), n))
    else:
        c, r, a0, a1 = e[1], e[2], e[3], e[4]
        for f in fracs:
            a = a0 + f * (a1 - a0)
            p = arc_pt(c, r, a)
            out.append((p, ((p[0] - c[0]) / r, (p[1] - c[1]) / r)))
    return out


def _inward_samples(R, off=1e-6):
    out = []
    for e in R.edges():
        for p, n in _edge_samples(e):
            q1 = (p[0] + off * n[0], p[1] + off * n[1])
            q2 = (p[0] - off * n[0], p[1] - off * n[1])
            if in_region(q1, R):
                out.append(q1)
            elif in_region(q2, R):
                out.append(q2)
    return out


def _depth(A, B):
    """Rough penetration estimate for reporting only (the harness compares signs / states, never overlap depths)."""
    best = 0.0
    for X, Y in ((A, B), (B, A)):
        pts = [q for e in X.edges() for q in edge_ends(e)] + _inward_samples(X, off=1e-3)
        for p in pts:
            if in_region(p, Y):
                best = max(best, min(pt_edge(p, e) for e in Y.edges()))
    return max(best, 1e-6)


def clearance(A, B):
    """Signed clearance of two regions: gap if disjoint, 0 if touching, minus a penetration estimate if overlapping."""
    EA, EB = A.edges(), B.edges()
    bbA = [edge_bbox(e) for e in EA]
    bbB = [edge_bbox(e) for e in EB]
    d = math.inf
    for ea, ba in zip(EA, bbA):
        for eb, bb in zip(EB, bbB):
            if _bb_dist(ba, bb) > d:
                continue
            dd = edge_dist(ea, eb)
            if dd <= 1e-9 and edge_cross(ea, eb):
                return -_depth(A, B)
            d = min(d, dd)
    if d > 1e-9:
        pa = _edge_samples(A.outer[0], (0.5,))[0][0]
        pb = _edge_samples(B.outer[0], (0.5,))[0][0]
        if in_region(pa, B) or in_region(pb, A):
            return -_depth(A, B)
        return d
    if any(in_region(p, B) for p in _inward_samples(A)) or any(in_region(p, A) for p in _inward_samples(B)):
        return -_depth(A, B)
    return 0.0


# ------------------------------------------------------------------ motion
def rotate(R, axis, deg):
    """Same convention as hinge_feasibility_2d.rotate: y' = ay + dy c + dz s, z' = az - dy s + dz c (rotation by -deg)."""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    ay, az = axis

    def rp(p):
        return (ay + (p[0] - ay) * c + (p[1] - az) * s, az - (p[0] - ay) * s + (p[1] - az) * c)

    def re(e):
        if e[0] == "L":
            return ("L", rp(e[1]), rp(e[2]))
        a0 = e[3] - deg
        return ("A", rp(e[1]), e[2], a0, a0 + (e[4] - e[3]))

    return Reg([re(e) for e in R.outer], [[re(e) for e in h] for h in R.holes])


def zmin(R):
    return R.bbox()[1]
