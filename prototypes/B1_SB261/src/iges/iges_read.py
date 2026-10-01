"""SCRATCH: minimal IGES 5.3 B-rep reader (std lib) for the TorqMaster SB-188-SB-261 assembly.
Reads D/P sections, resolves 308/408 subfigure placement + 124 transforms, and reports each solid (186) instance:
bounding box from vertices (502), and its analytic faces (190 plane, 192 cylinder, 194 cone, 198 torus) in mm."""
import math, sys
from collections import defaultdict

IN = 25.4
FN = "TORQMASTER-HINGE-ASSEMBLY-SB-188-SB-261-REV-A.igs"


def load(fn=FN):
    lines = open(fn, encoding="latin-1").read().splitlines()
    D = [l for l in lines if len(l) >= 73 and l[72] == "D"]
    Pl = [l for l in lines if len(l) >= 73 and l[72] == "P"]
    ents = {}
    for i in range(0, len(D), 2):
        a, b = D[i], D[i + 1]
        f1 = [a[k:k + 8] for k in range(0, 72, 8)]
        f2 = [b[k:k + 8] for k in range(0, 72, 8)]
        de = i + 1
        ents[de] = dict(type=int(f1[0]), pptr=int(f1[1]), xf=int(f1[6] or 0), status=f1[8], color=int(f2[2] or 0),
                        pcount=int(f2[3]), form=int(f2[4] or 0), label=f2[7].strip(), sub=f2[8].strip())
    # parameter text per DE (columns 1-64 data, 66-72 DE pointer)
    ptxt = defaultdict(str)
    for l in Pl:
        ptxt[int(l[64:72])] += l[:64]
    for de, e in ents.items():
        e["p"] = parse_params(ptxt[de])
    return ents


def parse_params(s):
    out, i, n = [], 0, len(s)
    tok = ""
    while i < n:
        c = s[i]
        if c in ",;":
            out.append(tok.strip())
            tok = ""
            if c == ";":
                break
            i += 1
            continue
        if c == "H" and tok.strip().isdigit():
            k = int(tok.strip())
            out.append(s[i + 1:i + 1 + k])
            i += 1 + k
            tok = ""
            # skip following delimiter
            while i < n and s[i] == " ":
                i += 1
            if i < n and s[i] in ",;":
                if s[i] == ";":
                    break
                i += 1
            continue
        tok += c
        i += 1
    return out


def num(x):
    x = x.replace("D", "E")
    return float(x) if any(ch in x for ch in ".Ee") else int(x)


# ---------------- transforms (3x4)
I3 = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0))


def mat(ents, de):
    if not de:
        return I3
    e = ents[de]
    p = [num(v) for v in e["p"][1:13]]
    M = ((p[0], p[1], p[2], p[3]), (p[4], p[5], p[6], p[7]), (p[8], p[9], p[10], p[11]))
    if e["xf"]:
        M = mul(mat(ents, e["xf"]), M)
    return M


def mul(A, B):
    R = []
    for r in range(3):
        row = [sum(A[r][k] * B[k][c] for k in range(3)) for c in range(3)]
        row.append(sum(A[r][k] * B[k][3] for k in range(3)) + A[r][3])
        R.append(tuple(row))
    return tuple(R)


def ap(M, p):
    return tuple(M[r][0] * p[0] + M[r][1] * p[1] + M[r][2] * p[2] + M[r][3] for r in range(3))


def av(M, v):
    return tuple(M[r][0] * v[0] + M[r][1] * v[1] + M[r][2] * v[2] for r in range(3))


def point(ents, de, M):
    e = ents[de]
    p = tuple(num(v) for v in e["p"][1:4])
    return ap(mul(M, mat(ents, e["xf"])), p)


def direc(ents, de, M):
    e = ents[de]
    v = tuple(num(v) for v in e["p"][1:4])
    v = av(mul(M, mat(ents, e["xf"])), v)
    n = math.sqrt(sum(c * c for c in v))
    return tuple(c / n for c in v)


def surface(ents, de, M):
    e = ents[de]
    t, p = e["type"], e["p"]
    Mx = mul(M, mat(ents, e["xf"]))
    if t == 190:
        return ("plane", point(ents, int(p[1]), Mx), direc(ents, int(p[2]), Mx))
    if t == 192:
        return ("cyl", point(ents, int(p[1]), Mx), direc(ents, int(p[2]), Mx), num(p[3]))
    if t == 194:
        return ("cone", point(ents, int(p[1]), Mx), direc(ents, int(p[2]), Mx), num(p[3]), num(p[4]))
    if t == 198:
        return ("torus", point(ents, int(p[1]), Mx), direc(ents, int(p[2]), Mx), num(p[3]), num(p[4]))
    return ("other", t)


def solid_instances(ents):
    """Yield (instance path name, solid DE, placement matrix) for every 186 reachable through 308/408."""
    defs = {de: e for de, e in ents.items() if e["type"] == 308}
    out = []

    def walk_def(de, M, path):
        e = ents[de]
        p = e["p"]
        nm, ne = p[2], int(p[3])
        for k in range(ne):
            c = int(p[4 + k])
            ce = ents[c]
            if ce["type"] == 408:
                walk_inst(c, M, path + [nm])
            elif ce["type"] == 186:
                out.append(("/".join(path + [nm]), c, mul(M, mat(ents, ce["xf"]))))

    def walk_inst(de, M, path):
        e = ents[de]
        p = e["p"]
        d, x, y, z = int(p[1]), num(p[2]), num(p[3]), num(p[4])
        s = num(p[5]) if len(p) > 5 and p[5] != "" else 1.0
        T = ((s, 0, 0, x), (0, s, 0, y), (0, 0, s, z))
        Mi = mul(M, mul(mat(ents, e["xf"]), T))
        walk_def(d, Mi, path)

    # top-level instances: 408 whose status says independent (subordinate switch '00')
    for de, e in ents.items():
        if e["type"] == 408 and e["status"][2:4] == "00":
            walk_inst(de, I3, [])
    for de, e in ents.items():           # solids not in any subfigure
        if e["type"] == 186 and e["status"][2:4] == "00":
            out.append(("(top)", de, mat(ents, e["xf"])))
    return out


def solid_faces(ents, sde, M):
    sh = ents[int(ents[sde]["p"][1])]
    nf = int(sh["p"][1])
    faces = []
    for k in range(nf):
        fde = int(sh["p"][2 + 2 * k])
        f = ents[fde]
        faces.append((fde, surface(ents, int(f["p"][1]), M), int(f["p"][2])))
    return faces


def solid_vertices(ents, sde, M):
    """All vertices of vertex lists referenced by the solid's edges (approximate: all 502 lists whose points lie in it)."""
    sh = ents[int(ents[sde]["p"][1])]
    verts = set()
    nf = int(sh["p"][1])
    for k in range(nf):
        f = ents[int(sh["p"][2 + 2 * k])]
        nl = int(f["p"][2])
        for j in range(nl):
            lp = ents[int(f["p"][4 + j])]
            ne = int(lp["p"][1])
            q = 2
            for _ in range(ne):
                typ, edl, ei = int(lp["p"][q]), int(lp["p"][q + 1]), int(lp["p"][q + 2])
                npar = int(lp["p"][q + 4])
                q += 5 + 2 * npar
                el = ents[edl]
                if typ == 0:
                    base = 2 + 5 * (ei - 1)
                    for vl, vi in ((int(el["p"][base + 1]), int(el["p"][base + 2])), (int(el["p"][base + 3]), int(el["p"][base + 4]))):
                        verts.add((vl, vi))
    pts = []
    for vl, vi in verts:
        e = ents[vl]
        b = 2 + 3 * (vi - 1)
        p = (num(e["p"][b]), num(e["p"][b + 1]), num(e["p"][b + 2]))
        pts.append(ap(mul(M, mat(ents, e["xf"])), p))
    return pts


if __name__ == "__main__":
    ents = load()
    for de, e in ents.items():
        if e["type"] in (308, 408):
            print(de, e["type"], "status", e["status"], "label", e["label"], "params", e["p"][:8])
