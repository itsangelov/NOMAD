"""D-010 solar architecture comparison (NON-PRODUCTION, read-only, estimates).

A = current sliding / tilting solar wings (D-009 baseline).
B1 = solar lid, single leaf hinged at the lid top edge.
B2 = solar lid, tri-fold (full-width centre leaf + two half-width side leaves folded onto it).

Every number is labelled in the report as calculated (from the model below), estimated or assumed.
Nothing here is authoritative. Envelope values come from nomad.yaml through e_lid_layout.
Writes concept-view SVGs to prototypes/P0.1/d010/ (study artifacts only).
Usage: py CAD/tools/d010_solar_architecture_study.py
"""
import math
import sys
from pathlib import Path

import e_lid_layout as el

ENV = el.evaluate()[0]
W, D, H = ENV["BODY_WIDTH"], ENV["BODY_DEPTH"], ENV["BODY_HEIGHT"]
HINGE = (D - ENV["HINGE_AXIS_OFFSET"], H + ENV["HINGE_AXIS_HEIGHT"])   # (y, z) world; y 0 = front
G = 9.81
OUT = Path(__file__).resolve().parents[2] / "prototypes" / "P0.1" / "d010"

# ------------------------------------------------------------------ assumptions (ASSUMED / ESTIMATED; see report)
PV_W_PER_M2 = (150.0, 170.0, 190.0)       # nameplate per module area, small mono ETFE panels (low / typ / high)
REAL_FACTOR = (0.55, 0.70)                # real-world / nameplate at best orientation, clear midday
ETFE_KG_M2 = 2.5                          # flexible ETFE laminate areal mass
TRAY_KG_M2 = 70e-3 / (0.1475 * 0.200)     # printed PETG tray (hub load check: 70 g for one cassette)
BASE = {"light": (1.15, 118.0, 18.0), "nominal": (1.45, 120.0, 18.0), "heavy": (1.80, 115.0, 17.0)}  # kg, y, z


def rot_open(p, phi):
    """Closed-lid frame point (y, z) -> world, lid opened by phi about the hinge."""
    dy, dz = p[0] - HINGE[0], p[1] - HINGE[1]
    c, s = math.cos(math.radians(phi)), math.sin(math.radians(phi))
    return (HINGE[0] + c * dy + s * dz, HINGE[1] - s * dy + c * dz)


def rot_vec(v, phi):
    c, s = math.cos(math.radians(phi)), math.sin(math.radians(phi))
    return (c * v[0] + s * v[1], -s * v[0] + c * v[1])


def elev(n):
    """Elevation of a normal in the Y-Z plane: 0 = horizontal toward the rear, 90 = up, 180 = horizontal front."""
    return math.degrees(math.atan2(n[1], n[0]))


# ------------------------------------------------------------------ architectures
def arch_A():
    cas_w, cas_h = ENV["SOLAR_CASSETTE_WIDTH"], ENV["SOLAR_CASSETTE_HEIGHT"]
    mod = (cas_w - 12) * (cas_h - 10)                       # module area per cassette (6 / 5 mm frame margins)
    panel = ETFE_KG_M2 * cas_w * cas_h * 1e-6               # laminate covers the cassette face
    per_side = {"PV laminate": panel, "printed cassette tray": 0.070, "printed rail (C-channel, 198 mm)": 0.045,
                "printed carriage": 0.008, "hub pin, plates, index pin, sleeve, spring, screws": 0.025,
                "S1-R stop hardware (yoke, bushing, stop plate, dowel)": 0.012, "wiring + connector": 0.015}
    extra = {"deeper lid frame for the rail layer (13 + gaps)": 0.070, "side-wall slot / notch reinforcement": 0.020}
    return {"name": "A sliding wings", "module_cm2": 2 * mod / 100, "stowed_cm2": 0.0, "n_panels": 2,
            "mass": {**{f"{k} (x2)": 2 * v for k, v in per_side.items()}, **extra},
            "lid_T": ENV["LID_THICKNESS"], "sail_m2": 2 * cas_w * cas_h * 1e-6}


def arch_B(n_layers):
    leaf_w, leaf_h = W - 6.0, D - 6.0                      # leaf envelope inside a 3 mm lid margin
    mod1 = (leaf_w - 16) * (leaf_h - 14)                    # centre leaf module (frame, hinge edge)
    mass = {"PV laminate, centre leaf": ETFE_KG_M2 * mod1 * 1e-6 * 1.08, "printed leaf tray (ribbed)": TRAY_KG_M2 * leaf_w * leaf_h * 1e-6,
            "leaf hinges (2) + steel pins": 0.020, "angle lock (friction hinge or strut with detents)": 0.025,
            "stow latch": 0.010, "wiring + connector + hinge loop": 0.020,
            "air-gap standoffs / vented rear shell (net)": 0.015}
    mod = mod1
    if n_layers == 2:
        mod2 = 2 * ((leaf_w / 2 - 12) * (leaf_h - 14))
        mass.update({"PV laminate, 2 side leaves": ETFE_KG_M2 * mod2 * 1e-6 * 1.08, "printed side-leaf trays (2)": TRAY_KG_M2 * leaf_w * leaf_h * 1e-6,
                     "side-leaf hinges (4) + pins": 0.030, "side-leaf latches": 0.010, "side-leaf jumpers": 0.010})
        mod += mod2
    core = ENV["DISPLAY_BEZEL_LIP"] + ENV["DISPLAY_THICKNESS"] + 1.0 + 8.0 + 4.0    # lip, display, gap, controller zone, thin shell
    lid_T = core + 4.0 + 6.0 * n_layers                                             # vented gap + leaf (tray 3.5 + laminate 2.5) per layer
    return {"name": "B1 solar lid, single leaf" if n_layers == 1 else "B2 solar lid, tri-fold", "module_cm2": mod / 100,
            "stowed_cm2": mod1 / 100, "n_panels": 1 if n_layers == 1 else 3, "mass": mass, "lid_T": lid_T, "core": core,
            "leaf": (leaf_w, leaf_h), "layers": n_layers, "sail_m2": (1 if n_layers == 1 else 2) * leaf_w * leaf_h * 1e-6}


def lid_parts(arch, phi, psi=None):
    """Lid-side point masses (kg, world y, z) for a pose. A: everything at the lid mid-length; B: leaf rotated by psi
    about the lid top edge (psi 0 = stowed on the lid back)."""
    zc0 = ENV["ZF"]
    out = []
    if arch["name"].startswith("A"):
        m_solar = sum(arch["mass"].values())
        out += [("display", 0.15, (117.5, zc0 + 3.5)), ("lid frame + rear shell", 0.45, (117.5, zc0 + 20.0)),
                ("solar (rails, carriages, cassettes)", m_solar, (117.5, zc0 + 22.0))]
    else:
        core = arch["core"]
        out += [("display", 0.15, (117.5, zc0 + 3.5)), ("lid frame + thin shell (no rail layer)", 0.33, (117.5, zc0 + core * 0.55))]
        m_leaf = sum(arch["mass"].values())
        zh = zc0 + core + 4.0 + 3.0 * arch["layers"]                  # leaf mid-plane (closed frame)
        r = 117.5
        if psi is None:
            psi = 0.0
        c, s = math.cos(math.radians(psi)), math.sin(math.radians(psi))
        out.append(("solar leaf pack", m_leaf, (0.0 + r * c, zh + r * s)))          # hinge at the lid front edge (top when open)
    return [(n, m, rot_open(p, phi)) for n, m, p in out]


def cog(parts):
    m = sum(p[1] for p in parts)
    return m, (sum(p[1] * p[2][0] for p in parts) / m, sum(p[1] * p[2][1] for p in parts) / m)


def stability(arch, phi, psi, base, wind_v=0.0, sail=None):
    """Static tipping about the rear bottom edge (y = D) and the lid-hinge gravity torque. Wind from the front pushes
    rearward on the given sails [(area m2, centre z mm)]."""
    lp = lid_parts(arch, phi, psi)
    mb, yb, zb = BASE[base]
    allp = lp + [("base", mb, (yb, zb))]
    m, (y, z) = cog(allp)
    restore = m * G * (D - y) / 1000                                  # N.m (positive = stable)
    q = 0.5 * 1.2 * wind_v ** 2
    over = sum(1.2 * q * a * zc / 1000 for a, zc in (sail or []))
    lid_torque = sum(p[1] * G * (p[2][0] - HINGE[0]) / 1000 for p in lp)   # + = tends to open further (fall back)
    return m, (y, z), restore, over, lid_torque


def sails(arch, phi, psi):
    """(area m2, centre height mm) presented to a horizontal wind, worst case (surfaces taken normal to the wind)."""
    lid_c = rot_open((117.5, ENV["ZF"] + 15), phi)
    out = [(W * D * 1e-6, lid_c[1])]
    if arch["name"].startswith("A"):
        out.append((arch["sail_m2"], lid_c[1]))
    else:
        leaf = [p for p in lid_parts(arch, phi, psi) if p[0] == "solar leaf pack"][0]
        out.append((arch["sail_m2"], leaf[2][1]))
    return out


def tip_wind(arch, phi, psi, base):
    m, c, restore, _, _ = stability(arch, phi, psi, base)
    sl = sails(arch, phi, psi)
    k = sum(1.2 * 0.5 * 1.2 * a * zc / 1000 for a, zc in sl)
    return math.sqrt(restore / k) if restore > 0 else 0.0


def orientation(arch, phi_range=(100.0, 125.0), psi_max=150.0):
    """Best cosine factor vs sun elevation, sun behind the device (rear) or in front (behind the user); the user picks
    the lid angle in phi_range and the device azimuth. Returns rows (elev, rear, front)."""
    rows = []
    for s in (10, 20, 30, 45, 60, 75, 90):
        best_r = best_f = 0.0
        for phi in range(int(phi_range[0]), int(phi_range[1]) + 1, 5):
            if arch["name"].startswith("A"):
                lo, hi = 90 - phi - 75, 90 - phi + 75
            else:
                lo, hi = 90 - phi, 90 - phi + psi_max
            for target, key in ((s, "r"), (180 - s, "f")):
                mis = 0.0 if lo <= target <= hi else min(abs(target - lo), abs(target - hi))
                f = max(0.0, math.cos(math.radians(mis)))
                if key == "r":
                    best_r = max(best_r, f)
                else:
                    best_f = max(best_f, f)
        rows.append((s, best_r, best_f))
    return rows


def thermal():
    """Steady cell / surface temperature rise above ambient, full sun 1000 W/m2, alpha 0.9 (ESTIMATES)."""
    q = 900.0
    rows = [("exposed dark PETG lid shell (A stowed; B deployed lid back)", q / 20.0, q / 13.0),
            ("B stowed, laminate bonded / in contact with the lid (back insulated), idle", q / 21.0, q / 14.0),
            ("B stowed, 4-6 mm vented air gap (both faces convect), idle", q / 26.0, q / 18.0),
            ("lid shell under a vented B leaf (shaded; radiation + gap air)", 0.25 * q / 26.0 + 5, 0.4 * q / 18.0 + 8),
            ("deployed panel, free both sides (A wing / B leaf), charging (~18 % extracted)", 0.82 * q / 30.0, 0.82 * q / 20.0)]
    return rows


# ------------------------------------------------------------------ concept views (SVG)
def svg(path, w, h, body):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / path).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" '
                            f'font-family="sans-serif" font-size="7"><rect width="{w}" height="{h}" fill="white"/>{body}</svg>\n',
                            encoding="utf-8")


def side_views():
    """Side view (Y right = rear, Z up) of base + lid + solar for several states."""
    def poly(pts, fill, stroke="#333"):
        return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{fill}" stroke="{stroke}" stroke-width="0.6"/>'

    def panel(ox, oy, pts, fill):
        return poly([(ox + p[0], oy - p[1]) for p in pts], fill)

    def lid_rect(phi, T, z0):
        return [rot_open(p, phi) for p in ((0, z0), (D, z0), (D, z0 + T), (0, z0 + T))]

    out = []
    frames = []
    A, B1 = arch_A(), arch_B(1)
    states = [("A stowed / wings out (side view unchanged), lid 110", A, 110, None),
              ("A wing tilt +75 (rear-up)", A, 110, "tilt+"), ("A wing tilt -75", A, 110, "tilt-"),
              ("B1 stowed, lid 110", B1, 110, 0.0), ("B1 leaf 60 deg", B1, 110, 60.0),
              ("B1 leaf horizontal-ish (overhead sun)", B1, 110, 105.0), ("B1 visor (sun behind user)", B1, 110, 150.0)]
    cw, ch = 330, 520
    for i, (title, arch, phi, st) in enumerate(states):
        ox, oy = 20 + (i % 4) * cw, 480 + (i // 4) * ch
        body = [panel(ox, oy, [(0, 0), (D, 0), (D, H), (0, H)], "#cfd4da")]
        T = arch["lid_T"]
        body.append(panel(ox, oy, lid_rect(phi, T if arch["name"].startswith("A") else arch["core"], ENV["ZF"]), "#8a9099"))
        if arch["name"].startswith("A"):
            z0 = ENV["ZF"] + 21
            axis = rot_open((ENV["HYR"], ENV["HZ"]), phi)
            ang = {None: 0, "tilt+": 75, "tilt-": -75}[st]
            pts = [rot_open(p, phi) for p in ((ENV["CY0"], z0), (ENV["CY0"] + 200, z0), (ENV["CY0"] + 200, z0 + 8), (ENV["CY0"], z0 + 8))]
            if ang:
                c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
                pts = [(axis[0] + c * (p[0] - axis[0]) - s * (p[1] - axis[1]), axis[1] + s * (p[0] - axis[0]) + c * (p[1] - axis[1])) for p in pts]
            body.append(panel(ox, oy, pts, "#27466e"))
        else:
            core = arch["core"]
            zh = ENV["ZF"] + core + 4
            c, s = math.cos(math.radians(st)), math.sin(math.radians(st))
            leaf = [(0 + c * a - s * b, zh + s * a + c * b) for a, b in ((0, 0), (D - 6, 0), (D - 6, 6), (0, 6))]
            body.append(panel(ox, oy, [rot_open(p, phi) for p in leaf], "#27466e"))
        mb, (yb, zb) = BASE["nominal"][0], BASE["nominal"][1:]
        m, (y, z), *_ = stability(arch, phi, st if not arch["name"].startswith("A") else None, "nominal")
        body.append(f'<circle cx="{ox + y:.1f}" cy="{oy - z:.1f}" r="3" fill="red"/>')
        body.append(f'<line x1="{ox + D}" y1="{oy}" x2="{ox + D}" y2="{oy - 300}" stroke="red" stroke-dasharray="2,2" stroke-width="0.4"/>')
        body.append(f'<text x="{ox}" y="{oy + 12}">{title}</text>')
        body.append(f'<text x="{ox}" y="{oy + 21}">CoG y {y:.0f} (tip edge {D:.0f}); front = left, rear = right</text>')
        frames.append("".join(body))
    out.append("".join(frames))
    out.append('<text x="20" y="14" font-size="9">D-010 concept side views (NON-PRODUCTION envelopes; mm; red dot = combined CoG, dashed = rear tipping edge)</text>')
    svg("d010_side_views.svg", 4 * cw + 20, 2 * ch + 40, "".join(out))


def front_views():
    """Front view (X right, Z up) with the lid at 110: A stowed / deployed; B1 / B2 deployed (leaf at 105)."""
    def rect(x0, z0, x1, z1, fill, ox, oy):
        return f'<rect x="{ox + x0:.1f}" y="{oy - z1:.1f}" width="{x1 - x0:.1f}" height="{z1 - z0:.1f}" fill="{fill}" stroke="#333" stroke-width="0.6"/>'
    phi = 110
    lid_top = rot_open((0, ENV["ZF"]), phi)[1]
    lid_bot = rot_open((D, ENV["ZF"]), phi)[1]
    body = []
    cols = [("A stowed", 0), ("A both wings deployed (612 span)", 1), ("B1 leaf deployed (horizontal, seen from front)", 2), ("B2 tri-fold deployed", 3)]
    for j, (title, k) in enumerate(cols):
        ox, oy = 340 + 0, 330 + j * 330
        body.append(rect(-W / 2, 0, W / 2, H, "#cfd4da", ox, oy))
        body.append(rect(-W / 2, lid_bot, W / 2, lid_top, "#8a9099", ox, oy))
        if k == 1:
            zc0 = rot_open((ENV["CY0"], ENV["ZF"]), phi)[1]
            zc1 = rot_open((ENV["CY0"] + 200, ENV["ZF"]), phi)[1]
            for sgn in (1, -1):
                x0, x1 = sorted((sgn * 158.5, sgn * 306))
                body.append(rect(x0, min(zc0, zc1), x1, max(zc0, zc1), "#27466e", ox, oy))
        if k in (2, 3):
            ww = W - 6 if k == 2 else 2 * (W - 6)
            body.append(rect(-ww / 2, lid_top, ww / 2, lid_top + 12, "#27466e", ox, oy))
        body.append(f'<text x="{ox - W:.0f}" y="{oy + 14}">{title}</text>')
    body.append('<text x="20" y="14" font-size="9">D-010 concept front views, lid 110 deg (NON-PRODUCTION; mm)</text>')
    svg("d010_front_views.svg", 700, 4 * 330 + 40, "".join(body))


# ------------------------------------------------------------------ report
def main():
    A, B1, B2 = arch_A(), arch_B(1), arch_B(2)
    print("D-010 solar architecture comparison (NON-PRODUCTION; calculated from stated estimates)")
    print(f"envelope: body {W:g} x {D:g} x {H:g}; lid hinge at the rear face (y {HINGE[0]:g}, z {HINGE[1]:g}); current lid (A) {ENV['LID_THICKNESS']:g} thick")

    print("\n== solar area and power (nameplate from module area x 150/170/190 W/m2; real = x0.55..0.70)")
    for a in (A, B1, B2):
        m2 = a["module_cm2"] / 1e4
        pn = [m2 * k for k in PV_W_PER_M2]
        print(f"  {a['name']}: panels {a['n_panels']}, module area {a['module_cm2']:.0f} cm2 (stowed exposed {a['stowed_cm2']:.0f} cm2); "
              f"nameplate {pn[0]:.1f} / {pn[1]:.1f} / {pn[2]:.1f} W; real best-orientation {pn[1] * REAL_FACTOR[0]:.1f}..{pn[1] * REAL_FACTOR[1]:.1f} W")

    print("\n== mass (estimates)")
    for a in (A, B1, B2):
        tot = sum(a["mass"].values())
        print(f"  {a['name']}: solar assembly {tot * 1000:.0f} g; lid thickness {a['lid_T']:.1f} mm")
        for k, v in a["mass"].items():
            print(f"      {k}: {v * 1000:.0f} g")

    print("\n== CoG, tipping (rear edge) and lid-hinge gravity torque; base nominal 1.45 kg unless stated (all estimates)")
    cases = [(A, 110, None, "A lid 110 (stowed or wings out: same side view)"), (A, 125, None, "A lid 125"),
             (B1, 110, 0.0, "B1 stowed, lid 110"), (B1, 110, 60.0, "B1 leaf 60"), (B1, 110, 105.0, "B1 leaf ~horizontal"),
             (B1, 125, 105.0, "B1 lid 125, leaf ~horizontal"), (B1, 110, 150.0, "B1 visor"), (B2, 110, 105.0, "B2 ~horizontal"),
             (B2, 125, 105.0, "B2 lid 125 ~horizontal")]
    for arch, phi, psi, lab in cases:
        m, (y, z), restore, _, lt = stability(arch, phi, psi, "nominal")
        v = {b: tip_wind(arch, phi, psi, b) for b in BASE}
        mb = BASE["nominal"][0]
        lever = y - D
        print(f"  {lab}: total {m:.2f} kg, CoG y {y:.0f} z {z:.0f} (behind tip edge by {lever:+.0f}); static restoring {restore:.2f} N.m; "
              f"lid-hinge gravity torque {lt:+.2f} N.m; front-wind tipping speed light/nominal/heavy base "
              f"{v['light']:.1f} / {v['nominal']:.1f} / {v['heavy']:.1f} m/s")

    print("\n== wind (q = 0.5 rho v^2, Cd 1.2, surfaces normal to the wind; estimates)")
    for v in (5.0, 10.0, 15.0):
        q = 0.5 * 1.2 * v * v
        fa = 1.2 * q * A["sail_m2"]
        fb1 = 1.2 * q * B1["sail_m2"]
        fb2 = 1.2 * q * B2["sail_m2"]
        leafc = [p for p in lid_parts(B1, 110, 105.0) if p[0] == "solar leaf pack"][0][2]
        print(f"  {v:g} m/s (q {q:.0f} Pa): A wings {fa:.1f} N total (per-wing hub torque <= {fa / 2 * 0.1:.2f} N.m, lid-hinge moment "
              f"~{fa * 0.12:.2f} N.m); B1 leaf {fb1:.1f} N (leaf-hinge moment {fb1 * 0.1175:.2f} N.m, lid-hinge moment "
              f"~{fb1 * (leafc[1] - HINGE[1]) / 1000:.2f} N.m); B2 {fb2:.1f} N")

    print("\n== orientation: best cosine factor (user picks lid 100-125 and azimuth); B leaf range psi 0..150")
    print("   sun elev | A rear | A front | B rear | B front")
    for (s, ar, af), (_, br, bf) in zip(orientation(A), orientation(B1)):
        print(f"   {s:8d} | {ar:6.2f} | {af:7.2f} | {br:6.2f} | {bf:7.2f}")

    print("\n== thermal: temperature rise above ambient, full sun (estimates; low / still-air)")
    for name, lo, hi in thermal():
        print(f"  {name}: +{lo:.0f} .. +{hi:.0f} K")

    print("\n== cable (estimates)")
    print("  A per side: base -> lid hinge pass -> lid (~250) -> slide service loop (158 travel, R20) -> carriage -> 11.5 mm link "
          "(twists +-80 deg about the pin at R 6.5: end displacement ~13 mm in 11.5 mm) -> bracket -> cassette; ~500 mm; "
          "2 moving sections (slide loop, hub twist); 2 x 2 = 4 moving sections total")
    print("  B1: leaf -> leaf-hinge loop (1 axis, ~150 deg, R>=20 loop or along the hinge axis) -> lid (~235) -> display-lid hinge "
          "pass (shared with the display cable) -> base; ~500 mm; 2 moving sections (leaf hinge, lid hinge)")
    print("  B2: + 2 side-leaf hinge jumpers (4 moving sections, all single-axis folds)")
    side_views()
    front_views()
    print(f"\nconcept views written: {OUT / 'd010_side_views.svg'}, {OUT / 'd010_front_views.svg'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
