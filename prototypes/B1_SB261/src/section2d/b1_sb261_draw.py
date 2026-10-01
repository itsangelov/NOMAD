"""SCRATCH: draw the two SB-261 hinge-rail sections (closed + leaf ghosts) to SVG."""
import sys, math
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))  # this folder (made relative at checkpoint)
import b1_sb261_rail as M

P = M.P
AY, AZ, PE, LF, CH = P["AY"], P["AZ"], P["PE"], P["LF"], P["CH"]
ax = (AY, AZ)
fz0, fz1 = AZ - M.RB - M.TF, AZ - M.RB
hy0, hy1 = AY + M.HOLE - M.HEAD_D / 2, AY + M.HOLE + M.HEAD_D / 2
S_ = 9.0
Y0, Y1, Z0, Z1 = -34.0, 44.0, 44.0, 92.0
W, H = (Y1 - Y0) * S_, (Z1 - Z0) * S_


def X(p):
    return ((p[0] - Y0) * S_, (Z1 - p[1]) * S_)


def poly(pts, fill="none", stroke="#222", sw=1.0, dash=None):
    d = " ".join(f"{X(p)[0]:.1f},{X(p)[1]:.1f}" for p in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{da}/>'


def circ(c, r, fill="none", stroke="#222", sw=1.0):
    x, y = X(c)
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * S_:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def R(y0, z0, y1, z1):
    return [(y0, z0), (y1, z0), (y1, z1), (y0, z1)]


def rotp(pts, psi):
    return [M.rot(p, psi, ax) for p in pts]


def text(p, s, size=12, anchor="start", col="#111"):
    x, y = X(p)
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{col}" font-family="Segoe UI, Arial">{s}</text>'


LIDC, LEAFC, STEEL, CUTC = "#c9ccd1", "#9cc3e6", "#4a4f57", "#ffffff"
core = [(0.0, M.ZF), (Y1, M.ZF), (Y1, M.ZB), (CH, M.ZB), (0.0, M.ZB - CH)]
panel = R(PE, M.ZP0, Y1, M.ZP1)


def ghosts(leafpts_list):
    out = []
    for psi, col in ((90, "#3b78b8"), (180, "#7a4fb0"), (190, "#c0392b")):
        for pts in leafpts_list:
            out.append(poly(rotp(pts, psi), stroke=col, sw=1.2, dash="5,3"))
    return out


def pocket_clipped():
    rp, zf = P["RP"], P["ZPF"]
    pts = []
    for k in range(361):
        t = math.radians(-180 + k * 0.5)
        y, z = AY + rp * math.cos(t), AZ + rp * math.sin(t)
        if zf <= z <= M.ZB and y >= 0:
            pts.append((y, z))
    pts.sort(key=lambda p: math.atan2(p[1] - AZ, p[0] - AY))
    yb0 = AY - math.sqrt(rp ** 2 - (zf - AZ) ** 2)
    yb1 = AY + math.sqrt(rp ** 2 - (zf - AZ) ** 2)
    yt = AY + math.sqrt(rp ** 2 - (M.ZB - AZ) ** 2)
    return [(max(0.0, yb0), zf), (yb1, zf)] + [p for p in pts if p[0] > AY] + [(yt, M.ZB), (0.0, M.ZB), (0.0, zf)]


def view(kind, ox):
    g = [f'<g transform="translate({ox},0)">', f'<rect x="0" y="0" width="{W}" height="{H}" fill="#fff" stroke="#999"/>',
         poly(core, LIDC, "#555")]
    if kind == "fixed":
        g.append(circ(ax, P["RG"], CUTC, "#555", 0.8))
        g.append(poly(R(AY - 1, fz0, AY + M.REACH + 0.5, M.ZB), CUTC, "#555", 0.8))
        g.append(poly(R(AY + M.HOLE - 2.0, fz0 - 5.7, AY + M.HOLE + 2.0, fz0), "#d4a017", "#7a5a00", 0.8))
        g.append(circ(ax, M.RB, STEEL, "#111"))
        g.append(poly(R(AY, fz0, AY + M.REACH, fz1), STEEL, "#111"))
        g.append(poly(R(hy0, fz1, hy1, fz1 + M.HEAD_K), "#222", "#000"))
        g.append(poly(R(AY + M.HOLE - 1.5, fz0 - 4.86, AY + M.HOLE + 1.5, fz1), "#555", "#000", 0.5))
        leaf = [panel, R(LF, fz1 + M.HEAD_K + 1.0, LF + P["BEAM"], M.ZP0)]
        for pts in leaf:
            g.append(poly(pts, LEAFC, "#245"))
        g += ghosts(leaf)
        title = "A  Fixed-flag segment (flag on lid rail)"
        notes = ["M3x6 ISO 7380, screwed from above", "M3 heat-set insert L5.7 in lid rail", "flag seat 1.7 deep",
                 "leaf beam stepped 1.0 over the head"]
    else:
        g.append(poly(pocket_clipped(), CUTC, "#555", 0.8))
        g.append(circ(ax, P["RG"], CUTC, "#555", 0.8))
        leaf = [panel, R(LF, M.ZB, LF + P["BEAM"], M.ZP0), R(AY, fz1, AY + P["BLOCK"], M.ZP0)]
        for pts in leaf:
            g.append(poly(pts, LEAFC, "#245"))
        g.append(poly(R(AY + M.HOLE - 2.0, fz1, AY + M.HOLE + 2.0, fz1 + 4.0), "#d4a017", "#7a5a00", 0.8))
        g.append(circ(ax, M.RB, STEEL, "#111"))
        g.append(poly(R(AY, fz0, AY + M.REACH, fz1), STEEL, "#111"))
        g.append(poly(R(hy0, fz0 - M.HEAD_K, hy1, fz0), "#222", "#000"))
        g.append(poly(R(AY + M.HOLE - 1.5, fz0, AY + M.HOLE + 1.5, fz1 + 3.86), "#555", "#000", 0.5))
        g += ghosts([panel, R(AY, fz1, AY + P["BLOCK"], M.ZP0)])
        title = "B  Rotating-flag segment (flag on leaf block)"
        notes = ["M3x5 ISO 7380, screwed from below", "short M3 insert L4 in leaf block", "lid pocket R16, floor z 56.5",
                 "insert cap 2.6 to panel back"]
    g.append(circ(ax, 0.45, "#fff", "#fff"))
    g.append(text((Y0 + 1, Z1 - 3), title, 15))
    for i, s in enumerate(notes):
        g.append(text((Y0 + 1, Z1 - 7 - 3.2 * i), s, 11, col="#333"))
    g.append(text((AY - 4.5, AZ + 4.6), "axis y4 z64", 10))
    g.append(text((Y1 - 1, M.ZP1 + 1.0), "PV panel 223 (z 67-71), front edge y9", 10, "end", "#245"))
    g.append(text((Y1 - 1, M.ZB - 3), "lid hinge rail (lid core, display-free)", 10, "end", "#444"))
    g.append(text((-0.6, M.ZB - CH - 2.6), "8x45 lid edge chamfer", 10, "end", "#444"))
    g.append(text((Y0 + 1, Z0 + 3.5), "leaf ghosts: psi 90 (blue), 180 (purple), 190 (red)", 10, col="#333"))
    g.append(text((Y1 - 1, Z0 + 2), "display starts at y 42.5", 10, "end", "#666"))
    g.append(f'<line x1="{X((0, Z0))[0]:.1f}" y1="0" x2="{X((0, Z0))[0]:.1f}" y2="{H}" stroke="#aaa" stroke-dasharray="2,4"/>')
    g.append(text((0.4, Z1 - 30), "lid edge y 0", 9, col="#777"))
    g.append("</g>")
    return "\n".join(g)


svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{2 * W + 20:.0f}" height="{H + 30:.0f}" viewBox="0 0 {2 * W + 20:.0f} {H + 30:.0f}">',
       '<rect width="100%" height="100%" fill="#fff"/>', view("fixed", 0), view("rot", W + 20),
       f'<text x="8" y="{H + 22:.0f}" font-size="12" font-family="Segoe UI, Arial" fill="#333">SCRATCH concept: B1 hinge rail around TorqMaster SB-188-SB-261. Y-Z sections in the closed-lid frame, mm. Not project CAD.</text>',
       "</svg>"]
open(str(__import__("pathlib").Path(__file__).resolve().parents[2] / "figures" / "b1_sb261_sections.svg"), "w", encoding="utf-8").write("\n".join(svg))
print("written")
