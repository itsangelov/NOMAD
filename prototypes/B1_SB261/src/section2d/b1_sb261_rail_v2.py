"""SCRATCH (not project CAD): B1 solar-leaf hinge rail concept around TorqMaster SB-188-SB-261.
Y-Z section model in the closed-lid frame of CAD/tools/d010_phase2_study.py (imported read-only, patched in memory only):
y = 0 lid top edge .. 235 display hinge, z = 42 display face .. 61 lid back .. 67-71 panel .. 73 leaf top.
Bodies are unions of solids (convex adds minus convex cuts); clearance by dense boundary sampling + spatial hash
(resolution ~0.05 mm). The leaf rotates about the hinge axis (AY, AZ) by psi (right hand about +X, as in the study)."""
import math, sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "CAD" / "tools"))  # repo CAD/tools (made repo-relative at checkpoint)
import d010_phase2_study as S

IN = 25.4
# ---- SB-188-SB-261 (TorqMaster drawing Rev A, published)
RB = 3.524             # band OD radius (IGES; drawing R .14 = 3.556)
RS = 2.381             # shaft radius = band ID (IGES) -> flag inner face tangent to the shaft
TF = 0.045 * IN         # flag thickness 1.143
REACH = 0.50 * IN       # axis -> flag tip 12.7
HOLE = 7.950           # axis -> hole (IGES; drawing .31 = 7.874)
SEG = 0.29 * IN         # segment / flag width 7.366
LOA = 1.33 * IN         # overall 33.78
SEND = 0.06 * IN        # shaft end 1.524
# ---- standard M3 hardware
HEAD_D, HEAD_K = 5.7, 1.65          # ISO 7380 M3 button head
INS_LID = (4.0, 5.7)                # heat-set insert hole dia / length, lid side (standard M3)
INS_LEAF = (4.0, 4.0)               # short M3 insert, leaf side
CAB_D, CAB_R = 4.0, 12.0            # cable (study CABLE_B) and minimum bend radius
SLEEVE_OD = 7.5

# ---- existing B1 stack (study values)
ZF, ZB, ZP0, ZP1, ZTOP, D, PY = S.ZF, S.ZC_B1, S.B1_Z_LEAF0, S.B1_Z_LEAF0 + 4.0, S.ZF + S.B1_LID_T, S.D, 223.0

# ---- DESIGN (scratch proposal)
P = dict(AY=4.0, AZ=63.5, PE=9.0, LF=9.0, CH=8.0, LCH=3.0, RG=RB + 0.5, RP=15.0, ZPF=57.3, BEAM=9.0, BLOCK=13.5)


def rect(y0, z0, y1, z1):
    return ("poly", [(y0, z0), (y1, z0), (y1, z1), (y0, z1)])


def disc(c, r):
    return ("disc", c, r)


def poly_inside(pts, p, tol):
    n = len(pts)
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        cr = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
        if cr < tol:      # CCW polygons; tol > 0 = strict interior
            return False
    return True


def prim_inside(pr, p, tol=1e-6):
    if pr[0] == "disc":
        return math.dist(pr[1], p) < pr[2] - tol
    return poly_inside(pr[1], p, tol)


def ccw(pts):
    a = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))
    return pts if a > 0 else pts[::-1]


def prim_samples(pr, h=0.05):
    out = []
    if pr[0] == "disc":
        n = max(24, int(2 * math.pi * pr[2] / h))
        return [(pr[1][0] + pr[2] * math.cos(2 * math.pi * k / n), pr[1][1] + pr[2] * math.sin(2 * math.pi * k / n)) for k in range(n)]
    pts = pr[1]
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        n = max(1, int(math.dist(a, b) / h))
        out += [(a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n) for k in range(n)]
    return out


class Body:
    """Union of solids; solid = (adds, cuts); inside = inside any add and outside all cuts of that solid."""
    def __init__(self, solids):
        self.solids = [([self._fix(a) for a in adds], [self._fix(c) for c in cuts]) for adds, cuts in solids]

    @staticmethod
    def _fix(pr):
        return ("poly", ccw(pr[1])) if pr[0] == "poly" else pr

    def inside(self, p, tol=1e-6):
        for adds, cuts in self.solids:
            if any(prim_inside(a, p, tol) for a in adds) and not any(prim_inside(c, p, -tol) for c in cuts):
                return True
        return False

    def boundary(self, centre, rmax, h=0.05):
        out = []
        for si, (adds, cuts) in enumerate(self.solids):
            for pr in adds:
                for p in prim_samples(pr, h):
                    if math.dist(p, centre) > rmax:
                        continue
                    if any(prim_inside(c, p, -1e-6) for c in cuts):
                        continue
                    if any(prim_inside(a, p) for a in adds if a is not pr):
                        continue
                    if any(self._solid_inside(sj, p) for sj in range(len(self.solids)) if sj != si):
                        continue
                    out.append(p)
            for pr in cuts:
                for p in prim_samples(pr, h):
                    if math.dist(p, centre) > rmax:
                        continue
                    if not any(prim_inside(a, p) for a in adds):
                        continue
                    if any(prim_inside(c, p) for c in cuts if c is not pr):
                        continue
                    if any(self._solid_inside(sj, p) for sj in range(len(self.solids)) if sj != si):
                        continue
                    out.append(p)
        return out

    def _solid_inside(self, si, p):
        adds, cuts = self.solids[si]
        return any(prim_inside(a, p) for a in adds) and not any(prim_inside(c, p, -1e-6) for c in cuts)


def rot(p, psi, ax):
    c, s = math.cos(math.radians(psi)), math.sin(math.radians(psi))
    dy, dz = p[0] - ax[0], p[1] - ax[1]
    return (ax[0] + c * dy - s * dz, ax[1] + s * dy + c * dz)


class Hash:
    def __init__(self, pts, cell=1.0):
        self.c, self.g = cell, {}
        for p in pts:
            self.g.setdefault((int(math.floor(p[0] / cell)), int(math.floor(p[1] / cell))), []).append(p)

    def near(self, p, rmax=6.0):
        k = max(1, int(math.ceil(rmax / self.c)))
        i0, j0 = int(math.floor(p[0] / self.c)), int(math.floor(p[1] / self.c))
        best = rmax
        for i in range(i0 - k, i0 + k + 1):
            for j in range(j0 - k, j0 + k + 1):
                for q in self.g.get((i, j), ()):
                    d = math.dist(p, q)
                    if d < best:
                        best = d
        return best


def bnd(body, ax, rmax, h=0.1):
    c = body.__dict__.setdefault("_bc", {})
    k = (ax, rmax, h)
    if k not in c:
        c[k] = body.boundary(ax, rmax, h)
    return c[k]


def clearance(lid, leaf, psi, ax, rmax=32.0, cap=4.0):
    """Signed min clearance (negative = penetration depth estimate) between the lid and the leaf rotated by psi."""
    lb = bnd(lid, ax, rmax)
    c = lid.__dict__.setdefault("_hc", {})
    if (ax, rmax, cap) not in c:
        c[(ax, rmax, cap)] = Hash(lb, cap)
    hl = c[(ax, rmax, cap)]
    fb = [rot(p, psi, ax) for p in bnd(leaf, ax, rmax)]
    hf = Hash(fb, cap)
    pen = 0.0
    for p in fb:
        if lid.inside(p):
            pen = max(pen, hl.near(p, cap))
    for q in lb:
        if leaf.inside(rot(q, -psi, ax)):
            pen = max(pen, hf.near(q, cap))
    if pen > 0:
        return -pen
    return min(min((hl.near(p, cap) for p in fb), default=cap), cap)


# ---------------------------------------------------------------------------------------------------------------------
def build(P):
    AY, AZ, PE, LF, CH = P["AY"], P["AZ"], P["PE"], P["LF"], P["CH"]
    ax = (AY, AZ)
    fz0, fz1 = AZ - RB, AZ - RS                          # flag band from the IGES: outer face on the band OD tangent, inner face on the shaft tangent
    core = ("poly", [(0.0, ZF), (D, ZF), (D, ZB), (CH, ZB), (0.0, ZB - CH)])     # lid core + 45 deg top-edge chamfer
    panel = rect(PE, ZP0, PE + PY, ZP1)
    beam = rect(LF, ZB, LF + P["BEAM"], ZP0)             # leaf front beam under the panel front edge
    groove = disc(ax, P["RG"])
    hy0, hy1 = AY + HOLE - HEAD_D / 2, AY + HOLE + HEAD_D / 2
    # pocket for the rotating flags/blocks: disc RP above the floor ZPF (convex polygon approximation)
    arc = [(AY + P["RP"] * math.cos(t), AZ + P["RP"] * math.sin(t)) for t in [2 * math.pi * k / 180 for k in range(180)]]
    pocket = ("poly", [p for p in arc if p[1] >= P["ZPF"]] + [(AY - math.sqrt(P["RP"] ** 2 - (P["ZPF"] - AZ) ** 2), P["ZPF"]),
                                                              (AY + math.sqrt(P["RP"] ** 2 - (P["ZPF"] - AZ) ** 2), P["ZPF"])])
    pocket = ("poly", sorted(pocket[1], key=lambda p: math.atan2(p[1] - AZ, p[0] - AY)))
    cab_c = (AY, AZ)                                      # cable / sleeve on the axis
    slices = {
        "general (front beam + panel)": (Body([([core], [])]), Body([([panel, beam], [])])),
        "leaf side wall (full height from LF)": (Body([([core], [])]), Body([([("poly", [(LF, ZB), (D, ZB), (D, ZTOP), (LF + P["LCH"], ZTOP), (LF, ZTOP - P["LCH"])])], [])])),
        "hinge, lid-flag segment": (
            Body([([core], [groove, rect(AY - 1, fz0, AY + REACH + 0.5, ZB + 1)]),       # flag seat cut into the rail
                  ([disc(ax, RB)], []),                                                   # fixed barrel segment
                  ([rect(AY, fz0, AY + REACH, fz1)], []),                                 # fixed flag
                  ([rect(hy0, fz1, hy1, fz1 + HEAD_K)], [])]),                            # M3 button head (screw from above)
            Body([([panel, rect(LF, fz1 + HEAD_K + 1.0, LF + P["BEAM"], ZP0)], [])])),   # beam stepped over the heads
        "hinge, leaf-flag segment": (
            Body([([core], [groove, pocket])]),
            Body([([panel, disc(ax, RB), rect(AY, fz0, AY + REACH, fz1),                 # rotating barrel segment + flag
                    rect(AY, fz1, AY + P["BLOCK"], ZP0),                                  # leaf block (short insert above flag)
                    rect(hy0, fz0 - HEAD_K, hy1, fz0), beam], [])])),                     # M3 head below the flag
        "sleeve / twist zone": (
            Body([([core], [disc(ax, SLEEVE_OD / 2 + 0.5)]), ([disc(ax, SLEEVE_OD / 2)], [])]),
            Body([([panel, beam], [])])),
        "cable, leaf exit (leaf-attached cable)": (
            Body([([core], [])]),
            Body([([panel, disc(cab_c, CAB_D / 2), rect(AY, AZ - CAB_D / 2, 40.0, AZ + CAB_D / 2)], [])])),
        "cable, lid exit (lid-fixed cable)": (
            Body([([core], []), ([disc(cab_c, CAB_D / 2), rect(AY, AZ - CAB_D / 2, 22.0, AZ + CAB_D / 2)], [])]),
            Body([([panel], [])])),
    }
    return ax, slices


def sweep(P, psis=range(2, 191, 2), lift=10):
    ax, slices = build(P)
    res = {}
    for name, (lid, leaf) in slices.items():
        g = {k: clearance(lid, leaf, k, ax) for k in psis}
        for k in (1, 189, 190):
            g[k] = clearance(lid, leaf, k, ax)
        mn = min((v, k) for k, v in g.items() if k >= lift)
        mn_all = min((v, k) for k, v in g.items())
        stop = None
        for k in range(191, 241):
            if clearance(lid, leaf, k, ax) < 0:
                stop = k
                break
        res[name] = (mn, mn_all, stop, g)
    return res


if __name__ == "__main__":
    import json
    mode = sys.argv[1] if len(sys.argv) > 1 else "run"
    if mode == "chamfer":
        for ch in (0.0, 2.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0):
            Q = dict(P, CH=ch)
            ax, sl = build(Q)
            worst = []
            for name in ("general (front beam + panel)", "leaf side wall (full height from LF)", "hinge, lid-flag segment"):
                lid, leaf = sl[name]
                worst.append((min(clearance(lid, leaf, k, ax) for k in range(150, 191, 2)), name))
            print(f"CH {ch:4.1f}: " + " | ".join(f"{n[:22]} {v:+.2f}" for v, n in worst))
    else:
        r = sweep(P)
        for name, (mn, mn_all, stop, g) in r.items():
            print(f"{name:40s} min(psi>=10) {mn[0]:+6.2f} @ {mn[1]:3d} | min(all) {mn_all[0]:+6.2f} @ {mn_all[1]:3d} | "
                  f"psi1 {g[1]:+.2f} psi90 {g[90]:+.2f} psi180 {g[180]:+.2f} psi190 {g[190]:+.2f} | first contact >190: {stop}")
