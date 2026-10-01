"""D-010 Phase 2: solar architecture engineering study, A (sliding wings) vs B1 (solar-lid leaf).

NON-PRODUCTION. Reads nomad.yaml (through base_v01_layout / e_lid_layout) and never writes it. Every result is an
estimate from the explicit INPUTS below; each input carries an evidence tag:
  YAML    nomad.yaml working value (provisional, not validated)
  VENDOR  vendor web data, retrieved 2026-09-28, not measured by us
  EST     engineering estimate (ranges given where they matter)
  ASSUMED assumption with no data behind it (owner / test must confirm)
Outputs are CALCULATED from those inputs. Nothing here is measured or physically tested.

Frames (same as the NOMAD E prototype): WORLD origin at the base bottom-front edge on the centreline, +X right,
+Y rear (toward the display hinge), +Z up. The lid is described in its CLOSED frame; opening by phi rotates it about
the D-006 hinge axis (X-parallel through y = HAY, z = HAZ). Architecture A cassettes slide along X and tilt about
X-parallel hub axes; the B1 leaf rotates about an X-parallel axis on the lid's free edge. All motions are rotations
about X-parallel axes plus X translations.

  py CAD/tools/d010_phase2_study.py            full report tables (stdout)
  py CAD/tools/d010_phase2_study.py --emit     also regenerate the data block in NOMAD_D010_Concepts.fs
"""
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import base_v01_layout as bl  # noqa: E402
import e_lid_layout as el  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
FS_PATH = ROOT / "CAD" / "featurescript" / "NOMAD_D010_Concepts.fs"
ENV = el.evaluate()[0]
BENV, BPARTS = bl.evaluate()
G = 9.81
DEG = math.pi / 180

# =====================================================================================================================
# INPUTS
# =====================================================================================================================
# ---- envelope (YAML)
W, D, H = ENV["BODY_WIDTH"], ENV["BODY_DEPTH"], ENV["BODY_HEIGHT"]
HAY, HAZ = ENV["HAY"], ENV["HAZ"]                  # display-lid hinge axis (D-006)
ZF = ENV["ZF"]                                      # closed lid display-side face
FOOT_H = 4.0          # ASSUMED rubber-foot height; the table plane is z = -FOOT_H
FOOT_INSET = 8.0      # ASSUMED foot centre inset from the base outline (support rectangle)
LID_A = ENV["LID_THICKNESS"]                        # A: class A lid 37.6 (YAML working value)

# ---- B1 lid stack (EST: Phase 1 core + this study's leaf design)
B1_CORE = 19.0        # EST lip 1 + display 5 + gap 1 + controller zone 8 + thin shell 4 (display area thinner)
B1_GAP = 6.0          # design value studied 0 / 4 / 6 (thermal section); 6 = recommended
B1_LEAF_T = 6.0       # EST panel 4 (VENDOR) seated in a frame, 2 mm frame lip proud of the panel face
B1_LID_T = B1_CORE + B1_GAP + B1_LEAF_T
B1_AXIS = (4.0, ZF + B1_LID_T - 4.0)               # leaf hinge axis (closed lid frame y, z): barrel inside the envelope
B1_LEAF_W = 289.0     # leaf outline X: panel 273 + 2 x 8 frame
B1_LEAF_D = D         # leaf outline Y (0 .. 235)
PSI_MAX = 190.0       # leaf range 0 (stowed on the lid back) .. 190 (upright above the lid, cells to the front)

# ---- panels
PANELS = {
    # VENDOR (voltaicsystems.com, 2026-09-28): catalog rigid ETFE panels on 2.0 mm FR4, 4 mm thick.
    "P108": {"desc": "Voltaic P108 ETFE 18 V (catalog)", "x": 273.0, "y": 223.0, "t": 4.0, "kg": 0.328, "W": (9.5, 10.9),
             "src": "VENDOR"},
    "P126": {"desc": "Voltaic P126 ETFE 6 V (catalog)", "x": 136.0, "y": 112.0, "t": 4.0, "kg": 0.079, "W": (2.6, 2.6),
             "src": "VENDOR"},
}
CUSTOM_W_M2 = (150.0, 170.0, 190.0)    # ASSUMED nameplate per laminate area, custom-size mono ETFE laminate
CUSTOM_KG_M2 = (2.5, 3.2)              # ASSUMED semi-flexible ETFE laminate areal mass (needs a backing plate)
REAL_FACTOR = (0.55, 0.70)             # ASSUMED real / nameplate at best aim, clear midday (temp, soiling, MPPT, cable)
PEAK_SUN_H = (2.0, 5.0)                # ASSUMED peak-sun-hours/day, winter overcast .. clear summer (energy illustration)

# ---- mass items: (label, kg nominal, kg low, kg high, body, (x, y, z) body frame, tag)
# body: base | lid | A_rail_R/L (lid-fixed) | A_car_R/L (slides) | A_cas_R/L (slides + tilts) | leaf | stay


def _centroid(name):
    for n, _, prims in BPARTS:
        if n == name:
            v = prims[0][2]
            return ((v[0] + v[3]) / 2, (v[1] + v[4]) / 2, (v[2] + v[5]) / 2)
    raise KeyError(name)


BASE_ITEMS = [
    ("base printed structure (shell, deck, trays, panels, doors)", 0.56, 0.42, 0.70, "base", (0.0, D / 2, 18.0), "EST"),
    ("keyboard module", 0.25, 0.18, 0.35, "base", _centroid("ENV_KEYBOARD"), "EST"),
    ("trackpad module", 0.06, 0.04, 0.09, "base", _centroid("ENV_TRACKPAD"), "EST"),
    ("Pi 5 + cooler + NVMe HAT", 0.11, 0.08, 0.14, "base", _centroid("ENV_PI_STACK"), "EST"),
    ("compute power (buck)", 0.03, 0.02, 0.04, "base", _centroid("ENV_COMPUTE_POWER"), "EST"),
    ("power electronics (BMS, MPPT, charger)", 0.08, 0.05, 0.12, "base", _centroid("ENV_POWER_ELECTRONICS"), "EST"),
    ("battery pack (NOT CHOSEN)", 0.26, 0.20, 0.33, "base", _centroid("ENV_BATTERY_BAY"), "ASSUMED"),
    ("GNSS module", 0.025, 0.02, 0.03, "base", _centroid("ENV_GNSS_MODULE"), "EST"),
    ("wiring, inserts, screws, feet", 0.06, 0.04, 0.09, "base", (0.0, D / 2, 10.0), "EST"),
    ("display-hinge hardware, base half (2)", 0.03, 0.02, 0.05, "base", (0.0, HAY - 12, HAZ - 10), "EST"),
]
LID_COMMON = [
    ("display panel", 0.15, 0.12, 0.19, "lid", (0.0, ENV["DYC"], (ENV["ZD0"] + ENV["ZD1"]) / 2), "EST"),
    ("display controller + FPC", 0.03, 0.02, 0.04, "lid", ((ENV["CBX0"] + ENV["CBX1"]) / 2, (ENV["CBY0"] + ENV["IY1"]) / 2, (ENV["ZFR"] + ENV["CBZ1"]) / 2), "EST"),
    ("display-hinge hardware, lid half (2)", 0.03, 0.02, 0.05, "lid", (0.0, HAY - 12, ZF + 6), "EST"),
]
A_LID = [("A lid structure, class A 37.6 (frame, walls, sandwich rear shell)", 0.435, 0.35, 0.52, "lid", (0.0, D / 2, 64.3), "EST"),
         ("A side-wall slot reinforcement", 0.02, 0.015, 0.03, "lid", (0.0, D / 2, (ENV["ZC0"] + ENV["ZC1"]) / 2), "EST")]


def a_side(sd):
    """Architecture A items for one side (R: +X, L: mirrored). Phase 1 masses (EST); custom laminate on the cassette."""
    sg = 1 if sd == "R" else -1
    hy = ENV["HYR"] if sd == "R" else ENV["HYL"]
    rc = ENV["RCR"] if sd == "R" else ENV["RCL"]
    zr = (ENV["ZR0"] + ENV["ZR1"]) / 2
    zc = (ENV["ZC0"] + ENV["ZC1"]) / 2
    cas_x = sg * (ENV["XI"] + ENV["SOLAR_CASSETTE_WIDTH"] / 2)
    return [
        (f"A{sd} rail (C-channel)", 0.045, 0.035, 0.06, f"A_rail_{sd}", (sg * (ENV["KX0"] + ENV["RX1"]) / 2, rc, zr), "EST"),
        (f"A{sd} carriage", 0.008, 0.006, 0.012, f"A_car_{sd}", (sg * (ENV["KX0"] + ENV["KX1"]) / 2, rc, zr), "EST"),
        (f"A{sd} hub pin, plates, index lock, sleeve, spring, screws", 0.025, 0.02, 0.035, f"A_car_{sd}", (sg * ENV["KX1"], hy, ENV["HZ"]), "EST"),
        (f"A{sd} S1-R stop yoke, bushing, stop plate, dowel", 0.012, 0.008, 0.016, f"A_car_{sd}", (sg * (ENV["KX1"] - 4), hy, ENV["HZ"]), "EST"),
        (f"A{sd} cassette tray", 0.07, 0.055, 0.085, f"A_cas_{sd}", (cas_x, (ENV["CY0"] + ENV["CY1"]) / 2, zc), "EST"),
        (f"A{sd} PV laminate (custom 147.5 x 200)", 0.074, 0.074, 0.094, f"A_cas_{sd}", (cas_x, (ENV["CY0"] + ENV["CY1"]) / 2, ENV["ZC1"] - 1), "ASSUMED"),
        (f"A{sd} wiring (moving part) + connector", 0.008, 0.006, 0.012, f"A_car_{sd}", (sg * ENV["KX0"], rc, zr), "EST"),
        (f"A{sd} wiring (lid run + loop)", 0.012, 0.008, 0.016, "lid", (sg * -40.0, rc, zr), "EST"),
    ]


A_ITEMS = LID_COMMON + A_LID + a_side("R") + a_side("L")

# B1: panel centre / frame in the CLOSED lid frame at psi = 0 (leaf body frame == lid frame at psi 0)
B1_Z_LEAF0 = ZF + B1_CORE + B1_GAP          # leaf underside (panel back plane)
B1_ITEMS = LID_COMMON + [
    ("B1 lid structure, core 19 (frame, walls, thin ribbed back shell)", 0.33, 0.27, 0.40, "lid", (0.0, D / 2, ZF + 10.8), "EST"),
    ("B1 air-gap spacers / vent grilles on lid back", 0.012, 0.008, 0.02, "lid", (0.0, D / 2, ZF + B1_CORE + 1), "EST"),
    ("B1 PV panel (catalog P108, 223 x 273 x 4, FR4-backed)", 0.328, 0.30, 0.345, "leaf", (0.0, D / 2, B1_Z_LEAF0 + 2.0), "VENDOR"),
    ("B1 leaf frame (open-back, 2 printed halves, ASA/PETG)", 0.09, 0.07, 0.12, "leaf", (0.0, D / 2, B1_Z_LEAF0 + 2.5), "EST"),
    ("B1 friction hinges x2, leaf half", 0.02, 0.012, 0.03, "leaf", (0.0, B1_AXIS[0], B1_AXIS[1]), "EST"),
    ("B1 friction hinges x2, lid half", 0.02, 0.012, 0.03, "lid", (0.0, B1_AXIS[0] + 4, B1_AXIS[1] - 6), "EST"),
    ("B1 hollow cable knuckle + tube", 0.008, 0.005, 0.012, "lid", (105.0, B1_AXIS[0], B1_AXIS[1]), "EST"),
    ("B1 stow latch (leaf + lid halves)", 0.01, 0.006, 0.015, "leaf", (0.0, D - 8, B1_Z_LEAF0 + 2), "EST"),
    ("B1 wiring leaf side + connector", 0.01, 0.007, 0.014, "leaf", (40.0, 14, B1_Z_LEAF0 + 1), "EST"),
    ("B1 wiring lid run", 0.012, 0.008, 0.016, "lid", (141.0, D / 2, ZF + 11), "EST"),
]
# B1 rear outrigger stay (chosen concept, see stay section): 2 stainless flat bars + 2 pivot screws + detents
STAY_ARM = {"x": 125.0, "y0": 222.0, "L": 105.0, "root": 12.0, "section": (3.0, 16.0)}   # pivot in the rear hinge-mount corner;
# stowed pointing FORWARD along the side under the base (y 117..234, x 117..133, clear of the feet), deployed rearward
STAY_ITEMS = [("B1 stay: 2 stainless arms 3x16x130 + 2 M4 shoulder screws + detent", 0.105, 0.09, 0.12, "stay", (0.0, STAY_ARM["y0"], -FOOT_H / 2), "EST")]

# ---- material / aero / thermal constants
PETG = {"rho": 1.27, "E": 1.9e3, "sig_xy": 40.0, "sig_z": 25.0, "HDT_045": 70.0, "Tg": 80.0}   # EST (MPa, g/cm3, degC)
ASA = {"HDT_045": 95.0, "Tg": 100.0}                                                           # EST
RHO_AIR = 1.2
CN_MAX, CN_SLOPE = 1.2, 2.5          # ASSUMED low-aspect flat plate normal-force coefficient: min(CN_MAX, CN_SLOPE * alpha_rad)
WIND_INCL = (-10.0, 0.0, 10.0)       # ASSUMED gust inclination to horizontal, deg (worst taken)
HANDLING_PUSH = 5.0                  # N, same handling basis as D-009 (finger push at the highest point)
SOLAR_G = 1000.0                     # W/m2 design irradiance
ALPHA_PV, ALPHA_DARK, ALPHA_LIGHT = 0.90, 0.90, 0.50   # EST absorptance
H_TOP = {"still air": 14.0, "light wind ~1 m/s": 22.0}  # EST front convection + radiation; 22 matches insulated-back PV
                                                         # field behaviour (~+40 K at 1000 W/m2), 14 = hot still day
K_AIR, EPS_DARK, EPS_FOIL = 0.026, 0.90, 0.10
T_AMB = 35.0                          # ASSUMED hot field day, degC

# ---- cables
# R = static installed bend radius (3 x d, ASSUMED silicone-jacket practice); R_dyn = repeated-flex minimum (6 x d, ASSUMED)
CABLE_A = {"d": ENV["SOLAR_CABLE_DIAMETER"], "R": 3 * ENV["SOLAR_CABLE_DIAMETER"], "R_dyn": 6 * ENV["SOLAR_CABLE_DIAMETER"],
           "loop_R": ENV["SOLAR_CABLE_BEND_RADIUS"]}                     # YAML d 6, loop radius 20
CABLE_B = {"d": 4.0, "R": 12.0, "R_dyn": 24.0}                          # ASSUMED 2 x 0.5 mm2 silicone
TWIST_OK_DEG_PER_MM = 3.5            # ASSUMED acceptable axial twist rate for fine-stranded 2-core (~0.3 % conductor strain)


# =====================================================================================================================
# KINEMATICS
# =====================================================================================================================
def rot_x(p, a_deg, yc, zc):
    """Rotate (x, y, z) about the X-parallel axis through (yc, zc) by a (right-hand about +X)."""
    c, s = math.cos(a_deg * DEG), math.sin(a_deg * DEG)
    dy, dz = p[1] - yc, p[2] - zc
    return (p[0], yc + c * dy - s * dz, zc + s * dy + c * dz)


def rot_vx(v, a_deg):
    c, s = math.cos(a_deg * DEG), math.sin(a_deg * DEG)
    return (v[0], c * v[1] - s * v[2], s * v[1] + c * v[2])


def pose(phi=0.0, sR=0.0, tR=0.0, sL=0.0, tL=0.0, psi=0.0, stay=False):
    return {"phi": phi, "sR": sR, "tR": tR, "sL": sL, "tL": tL, "psi": psi, "stay": stay}


def to_world(body, p, ps):
    """Body-frame point (closed / stowed) -> world."""
    x, y, z = p
    if body in ("base", "stay"):
        return p
    trav = ENV["SOLAR_SLIDE_TRAVEL"]
    if body.startswith("A_car_") or body.startswith("A_loop_") or body.startswith("A_cas_"):
        sd = body[-1]
        s = ps["s" + sd]
        sg = 1 if sd == "R" else -1
        frac = 0.5 if body.startswith("A_loop_") else 1.0
        if body.startswith("A_cas_"):
            hy = ENV["HYR"] if sd == "R" else ENV["HYL"]
            x, y, z = rot_x((x, y, z), ps["t" + sd], hy, ENV["HZ"])
        x += sg * s * trav * frac
    elif body == "leaf":
        x, y, z = rot_x((x, y, z), ps["psi"], B1_AXIS[0], B1_AXIS[1])
    return rot_x((x, y, z), -ps["phi"], HAY, HAZ)


def to_world_vec(body, v, ps):
    if body in ("base", "stay"):
        return v
    if body.startswith("A_cas_"):
        v = rot_vx(v, ps["t" + body[-1]])
    elif body == "leaf":
        v = rot_vx(v, ps["psi"])
    return rot_vx(v, -ps["phi"])


def items_for(arch, ps, case="nom", with_base=True):
    base = BASE_ITEMS if with_base else []
    lst = base + (A_ITEMS if arch == "A" else B1_ITEMS + STAY_ITEMS)
    k = {"nom": 1, "lo": 2, "hi": 3}[case]
    out = []
    for it in lst:
        body = it[4]
        if body == "stay":
            pt = (it[5][0], it[5][1] + (STAY_ARM["L"] / 2 if ps["stay"] else 0.0), it[5][2])
        else:
            pt = to_world(body, it[5], ps)
        out.append((it[0], it[k], pt, body))
    return out


def cog(items):
    m = sum(i[1] for i in items)
    return m, tuple(sum(i[1] * i[2][j] for i in items) / m for j in range(3))


# =====================================================================================================================
# STATES (named poses shown in Onshape; phi = display angle, s = wing extension 0..1, t = wing tilt, psi = leaf)
# =====================================================================================================================
NORMAL_SUN_ELEV = 45.0     # ASSUMED "normal" aim: sun behind the device at 45 deg elevation
STATES = {
    "A": [("STOWED", pose()),
          ("DISPLAY_OPEN", pose(phi=110)),
          ("PARTIAL", pose(phi=110, sR=0.5, sL=0.5)),
          ("NORMAL", pose(phi=110, sR=1, tR=NORMAL_SUN_ELEV - (90 - 110), sL=1, tL=NORMAL_SUN_ELEV - (90 - 110))),
          ("MAX", pose(phi=125, sR=1, tR=75, sL=1, tL=75)),
          ("ONE_WING", pose(phi=110, sR=1, tR=65))],
    "B1": [("STOWED", pose()),
           ("DISPLAY_OPEN", pose(phi=110)),
           ("PARTIAL", pose(phi=110, psi=30)),
           ("NORMAL", pose(phi=110, psi=NORMAL_SUN_ELEV - (90 - 110))),
           ("MAX", pose(phi=110, psi=PSI_MAX, stay=True)),
           ("STAY_DEPLOYED", pose(phi=110, psi=110, stay=True))],
}


# =====================================================================================================================
# WIND / TIPPING (general support-polygon edges, 3-D forces)
# =====================================================================================================================
def plates(arch, ps):
    """Wind plates: (label, area m2, centre world, unit normal world)."""
    out = []
    zc = ZF + (LID_A if arch == "A" else B1_CORE) / 2
    out.append(("base front/rear face", W * H * 1e-6, (0.0, D / 2, H / 2), (0.0, 1.0, 0.0)))
    out.append(("base side face", D * H * 1e-6, (0.0, D / 2, H / 2), (1.0, 0.0, 0.0)))
    out.append(("display lid", W * D * 1e-6, to_world("lid", (0.0, D / 2, zc), ps), to_world_vec("lid", (0, 0, 1), ps)))
    if arch == "A":
        for sd in ("R", "L"):
            if ps["s" + sd] > 0.05:
                sg = 1 if sd == "R" else -1
                c = (sg * (ENV["XI"] + ENV["SOLAR_CASSETTE_WIDTH"] / 2), (ENV["CY0"] + ENV["CY1"]) / 2, (ENV["ZC0"] + ENV["ZC1"]) / 2)
                a = ENV["SOLAR_CASSETTE_WIDTH"] * ENV["SOLAR_CASSETTE_HEIGHT"] * 1e-6 * min(1.0, ps["s" + sd] * ENV["SOLAR_SLIDE_TRAVEL"] / ENV["SOLAR_CASSETTE_WIDTH"])
                out.append((f"wing {sd}", a, to_world(f"A_cas_{sd}", c, ps), to_world_vec(f"A_cas_{sd}", (0, 0, 1), ps)))
    elif ps["psi"] > 8.0:
        c = (0.0, D / 2, B1_Z_LEAF0 + B1_LEAF_T / 2)
        out.append(("leaf", B1_LEAF_W * B1_LEAF_D * 1e-6, to_world("leaf", c, ps), to_world_vec("leaf", (0, 0, 1), ps)))
    return out


def cn(alpha):
    return min(CN_MAX, CN_SLOPE * abs(alpha))


def wind_forces(arch, ps, v, beta_deg, incl_deg):
    """Forces [(point mm, F N)] for wind speed v travelling toward azimuth beta (0 = toward +Y, i.e. wind from the
    front / user side; 90 = toward +X) with inclination incl (+ = upward)."""
    b, g = beta_deg * DEG, incl_deg * DEG
    w = (math.cos(g) * math.sin(b), math.cos(g) * math.cos(b), math.sin(g))
    q = 0.5 * RHO_AIR * v * v
    out = []
    for _, a, c, n in plates(arch, ps):
        dn = sum(w[i] * n[i] for i in range(3))
        alpha = math.asin(max(-1.0, min(1.0, abs(dn))))
        f = q * a * cn(alpha) * (1 if dn >= 0 else -1)
        out.append((c, tuple(f * n[i] for i in range(3))))
    return out


def hull(pts):
    pts = sorted(set(pts))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def support(stay=None):
    """Support polygon (CCW) on the table plane. stay: None or (x_abs, y_foot) for two mirrored feet."""
    xi, y0, y1 = W / 2 - FOOT_INSET, FOOT_INSET, D - FOOT_INSET
    pts = [(-xi, y0), (xi, y0), (xi, y1), (-xi, y1)]
    if stay:
        pts += [(-stay[0], stay[1]), (stay[0], stay[1])]
    return hull(pts)


def edges(poly):
    """(label, point, outward normal) per support edge."""
    out = []
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        ex, ey = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(ex, ey)
        m = (ey / ln, -ex / ln)          # CCW polygon -> outward normal is (ey, -ex)
        lab = "rear" if m[1] > 0.7 else "front" if m[1] < -0.7 else "right" if m[0] > 0.7 else "left" if m[0] < -0.7 else "corner"
        out.append((lab, a, m))
    return out


def tip_moment(point, force, e, m):
    """Moment (N.m) tending to tip about the support edge through e (table plane) with outward normal m."""
    r = (point[0] - e[0], point[1] - e[1], point[2] + FOOT_H)
    t = (-m[1], m[0], 0.0)               # t = z x m
    cr = (r[1] * force[2] - r[2] * force[1], r[2] * force[0] - r[0] * force[2], r[0] * force[1] - r[1] * force[0])
    return (t[0] * cr[0] + t[1] * cr[1]) / 1000.0


def stability(arch, ps, case="nom", stay_geom=None):
    """Per edge: gravity moment (<0 stable), CG margin to the edge, wind speed to tip (worst beta/incl pointing
    across that edge), handling push that tips. Returns dict and the CG."""
    its = items_for(arch, ps, case)
    m, c = cog(its)
    geom = stay_geom if stay_geom is not None else ((STAY_ARM["x"], STAY_ARM["y0"] + STAY_ARM["L"]) if ps["stay"] else None)
    poly = support(geom)
    top = geometric_top(arch, ps)
    res = {}
    for lab, e, mvec in edges(poly):
        mg = tip_moment(c, (0.0, 0.0, -m * G), e, mvec)
        margin = -mg / (m * G) * 1000.0          # mm, horizontal distance CG -> edge (positive = inside)
        best = None
        beta0 = math.degrees(math.atan2(mvec[0], mvec[1]))
        for db in (-30.0, -15.0, 0.0, 15.0, 30.0):
            for inc in WIND_INCL:
                mw = sum(tip_moment(p, f, e, mvec) for p, f in wind_forces(arch, ps, 1.0, beta0 + db, inc))
                if mw > 1e-9 and mg < 0:
                    v = math.sqrt(-mg / mw)
                    best = v if best is None else min(best, v)
        push = (-mg / ((top + FOOT_H) / 1000.0)) if mg < 0 else 0.0
        key = lab if lab not in res else lab + "2"
        res[key] = {"margin": margin, "mg": mg, "v_tip": best if mg < 0 else 0.0, "push": push}
    return m, c, res, top


def geometric_top(arch, ps):
    """Highest point of the lid / leaf / wings (mm) for the handling-push lever."""
    zs = []
    T = LID_A if arch == "A" else B1_CORE
    for y in (0.0, D):
        for z in (ZF, ZF + T):
            zs.append(to_world("lid", (0.0, y, z), ps)[2])
    if arch == "B1":
        for y in (0.0, D):
            for z in (B1_Z_LEAF0, B1_Z_LEAF0 + B1_LEAF_T):
                zs.append(to_world("leaf", (0.0, y, z), ps)[2])
    else:
        for sd in ("R", "L"):
            for y in (ENV["CY0"], ENV["CY1"]):
                for z in (ENV["ZC0"], ENV["ZC1"]):
                    zs.append(to_world(f"A_cas_{sd}", (0.0, y, z), ps)[2])
    return max(zs)


def worst(res, keys=("rear", "front", "left", "right")):
    return {k: min((v for kk, v in res.items() if kk.startswith(k)), key=lambda r: r["v_tip"] if r["v_tip"] is not None else 99)
            for k in keys if any(kk.startswith(k) for kk in res)}


# =====================================================================================================================
# HINGE TORQUES
# =====================================================================================================================
def lid_hinge_torque(arch, ps, v_wind=0.0, case="nom"):
    """Gravity (+ optional front-wind) torque about the display hinge, N.m; + = tends to open further (fall back)."""
    its = [i for i in items_for(arch, ps, case, with_base=False) if i[3] not in ("stay",)]
    tg = sum(i[1] * G * (i[2][1] - HAY) / 1000 for i in its)
    tw = 0.0
    if v_wind:
        for p, f in wind_forces(arch, ps, v_wind, 0.0, 0.0):
            if p[1] > HAY - 1 or p[2] > H + 1:                   # lid-side plates only
                if abs(p[2] - H / 2) > 1e-6:
                    tw += ((p[2] - HAZ) * f[1] - (p[1] - HAY) * f[2]) / 1000
    return tg, tw


def leaf_hinge_torque(ps, v_wind=0.0, case="nom"):
    """Gravity (+ wind) torque about the leaf axis, N.m (magnitude of the holding demand)."""
    ax = to_world("lid", (0.0, B1_AXIS[0], B1_AXIS[1]), ps)
    its = [i for i in items_for("B1", ps, case, with_base=False) if i[3] == "leaf"]
    tg = sum(i[1] * G * (i[2][1] - ax[1]) / 1000 for i in its)
    tw = 0.0
    if v_wind:
        q = 0.5 * RHO_AIR * v_wind ** 2
        tw = q * B1_LEAF_W * B1_LEAF_D * 1e-6 * CN_MAX * (B1_LEAF_D / 2 - B1_AXIS[0]) / 1000
    return tg, tw


# =====================================================================================================================
# CABLE ROUTES (anchor lists; the same lists drive the Onshape tubes)
# =====================================================================================================================
def _loop_apex():
    """Rolling service loop (A), apex INBOARD at stow (consistent with the E2 band LPX0 = KX0 - 2R): the apex sits at the
    band's inboard end and moves outboard at half the carriage speed."""
    return ENV["LPX0"] + CABLE_A["d"] / 2


# Route anchors: (body, (x, y, z) body frame, tag of the segment that STARTS here). Tags: "" static, "sbend" hub-link
# offset bend (moving), "hop" carriage -> loop transition (crosses the rail wall: UNRESOLVED), "loop" rolling loop,
# "twist" axial twist zone on a hinge axis (moving).
def a_route(sd):
    """Architecture A cable. Right: crosses the display hinge through the RIGHT hinge knuckle (its fixed end is near it).
    Left: its loop band is in the front half, so it detours in front of the band, crosses both rail bands where they
    end (x = +95 / -95, via the 12 mm gap between the rail bands) and crosses the hinge in the centre pass."""
    sg = 1 if sd == "R" else -1
    hy = ENV["HYR"] if sd == "R" else ENV["HYL"]
    cy = hy + sg * ENV["CRO"]                               # cable centre line through the link (cable side)
    zr = (ENV["ZR0"] + ENV["ZR1"]) / 2
    d2 = CABLE_A["d"] / 2
    if sd == "R":
        ym, yf = ENV["LRY0"] + d2, ENV["LRY1"] - d2
    else:
        ym, yf = ENV["LLY1"] - d2, ENV["LLY0"] + d2
    apex = _loop_apex()
    xf = 115.0
    cas, car, loop = f"A_cas_{sd}", f"A_car_{sd}", f"A_loop_{sd}"

    def X(v):
        return sg * v
    pts = [(cas, (X(40.0), (ENV["CY0"] + ENV["CY1"]) / 2, ENV["ZC0"] + 2), ""),        # panel junction on the cassette
           (cas, (X(ENV["XI"] + 7.5), cy, ENV["HZ"]), "sbend"),                          # link: cable at CRO from the tilt axis
           (car, (X(ENV["KX1"] - 2), cy, ENV["HZ"]), ""),
           (car, (X(ENV["KX0"] + 11), cy, zr), "hop"),                                   # leaves the carriage through the rail wall
           (car, (X(ENV["KX0"] - 11), ym, zr), "loop"),
           (loop, (X(apex), ym, zr), "loop"), (loop, (X(apex), yf, zr), "loop"),
           ("lid", (X(xf), yf, zr), "")]
    if sd == "R":
        pts += [("lid", (134.0, 206.0, 57.0), ""), ("lid", (134.0, 224.0, 52.0), ""), ("lid", (134.0, HAY, HAZ), "twist"),
                ("base", (115.0, HAY, HAZ), ""), ("base", (115.0, 222.0, 20.0), ""), ("base", (115.0, 205.0, 8.5), "")]
    else:
        pts += [("lid", (-136.0, yf, zr), ""), ("lid", (-136.0, ENV["IY0"] + 3.5, zr), ""), ("lid", (95.0, ENV["IY0"] + 3.5, zr), ""),
                ("lid", (95.0, D / 2, zr), ""), ("lid", (-95.0, D / 2, zr), ""), ("lid", (-95.0, 214.0, 56.0), ""),
                ("lid", (-80.0, HAY, HAZ), "twist"), ("base", (-8.0, HAY, HAZ), ""), ("base", (-5.0, 226.0, 16.0), ""),
                ("base", (-5.0, 205.0, 8.5), "")]
    pe = _centroid("ENV_POWER_ELECTRONICS")
    pts += [("base", (pe[0], 197.5, 8.5), ""), ("base", (pe[0], BENV["PEY1"] + 2, 8.5), "")]
    return pts


def b1_route():
    """B1: panel junction (behind the panel, in the vented gap) -> leaf front bar -> hollow knuckle on the leaf axis
    (twist zone) -> lid side channel -> lid band between display and controller -> centre display-hinge pass (axis
    twist zone shared with the display cable) -> base riser -> trunk -> power electronics."""
    ax_y, ax_z = B1_AXIS
    zl = B1_Z_LEAF0 - 3.0                                    # in the air gap / frame front bar
    zi = ZF + 11.0                                           # lid interior run height (above the display back)
    pe = _centroid("ENV_POWER_ELECTRONICS")
    return [("leaf", (0.0, 40.0, zl), ""), ("leaf", (30.0, 16.0, zl), ""), ("leaf", (52.0, 14.0, zl), ""),
            ("leaf", (72.0, ax_y, ax_z), "twist"),            # leaf end of the knuckle twist zone (on the axis)
            ("lid", (141.0, ax_y, ax_z), ""),                 # lid end
            ("lid", (141.0, 32.0, zi), ""), ("lid", (141.0, 193.5, zi), ""), ("lid", (-78.0, 193.5, zi), ""),
            ("lid", (-82.0, 215.0, ZF + 14.0), ""), ("lid", (-75.0, HAY, HAZ), ""),
            ("lid", (-44.0, HAY, HAZ), "twist"),              # lid fixing point on the display-hinge axis
            ("base", (5.0, HAY, HAZ), ""), ("base", (5.0, 227.0, 16.0), ""), ("base", (5.0, 205.0, 8.5), ""),
            ("base", (pe[0], 197.5, 8.5), ""), ("base", (pe[0], BENV["PEY1"] + 2, 8.5), "")]


def fillet_path(pts, R):
    """Polyline -> (length, min radius achieved, list of flags). Radius reduced where segments are too short."""
    n = len(pts)
    length, rmin, flags = 0.0, R, []
    tang = [0.0] * n
    geo = []
    for i in range(1, n - 1):
        a, b, c = pts[i - 1], pts[i], pts[i + 1]
        u1 = [b[k] - a[k] for k in range(3)]
        u2 = [c[k] - b[k] for k in range(3)]
        l1, l2 = math.sqrt(sum(x * x for x in u1)), math.sqrt(sum(x * x for x in u2))
        if l1 < 1e-9 or l2 < 1e-9:
            geo.append((0, R))
            continue
        cosang = max(-1.0, min(1.0, sum(u1[k] * u2[k] for k in range(3)) / (l1 * l2)))
        th = math.acos(cosang)
        if th < 1e-4:
            geo.append((0, R))
            continue
        tmax = min(l1 * (1 if i == 1 else 0.5), l2 * (1 if i == n - 2 else 0.5))
        t = R * math.tan(th / 2)
        r = R if t <= tmax else tmax / math.tan(th / 2)
        tang[i] = min(t, tmax)
        geo.append((th, r))
        if r < R - 1e-6:
            flags.append((i, r))
        rmin = min(rmin, r)
    for i in range(n - 1):
        seg = math.dist(pts[i], pts[i + 1])
        length += seg - tang[i] - (tang[i + 1] if i + 1 < n else 0)
    for th, r in geo:
        length += th * r
    return length, rmin, flags


def route_world(route, ps):
    return [to_world(b, p, ps) for b, p, _ in route]


def moving_sections(route):
    """[(tag, index, segment length in the stowed frame)] for the tagged moving segments."""
    return [(tag, i, math.dist(route[i][1], route[i + 1][1])) for i, (_, _, tag) in enumerate(route) if tag and i + 1 < len(route)]


# =====================================================================================================================
# THERMAL (1-D resistance networks per m2 of lid area; ESTIMATES for spotting obvious problems)
# =====================================================================================================================
SIGMA = 5.67e-8


def h_rad_gap(eps1, eps2, T=340.0):
    return 4 * SIGMA * T ** 3 / (1 / eps1 + 1 / eps2 - 1)


def h_chimney(g_mm, L_mm=D, dT=35.0):
    """Elenbaas vertical parallel-plate channel (symmetric isothermal), per face. g = gap."""
    if g_mm <= 0:
        return 0.0
    g, L = g_mm / 1000, L_mm / 1000
    beta, nu, al = 1 / 320.0, 1.7e-5, 2.4e-5
    ra = G * beta * dT * g ** 3 / (nu * al)
    ras = ra * g / L
    nu_ = ras / 24 * (1 - math.exp(-35 / ras)) ** 0.75
    return nu_ * K_AIR / g


def solve(A, b):
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c:
                f = M[r][c] / M[c][c]
                for k in range(c, n + 1):
                    M[r][k] -= f * M[c][k]
    return [M[i][n] / M[i][i] for i in range(n)]


R_CORE_B = 0.0125 + 1 / (K_AIR / 0.009 + h_rad_gap(0.9, 0.9)) + 0.005    # shell + 9 mm lid interior air + display: EST
R_MID_A = 0.11 + 1 / (K_AIR / 0.002 + h_rad_gap(0.9, 0.9)) + 0.03 + 1 / (K_AIR / 0.013 + h_rad_gap(0.9, 0.9)) + 0.04
R_BASE = 0.20        # EST display -> ambient downward through the closed base (base walls lose heat laterally)
R_FACE = 0.10        # EST open lid: display -> shaded front face -> ambient


def thermal_case(arch, gap, foil, scenario, htop, charging=False):
    """Returns (T_top rise, T_lid-shell rise, T_display rise) in K. scenario 'closed_flat' (sun normal to the closed
    top) or 'open_back_sun' (lid open, sun normal to the lid back, display side shaded)."""
    q = (ALPHA_PV if arch == "B1" else ALPHA_DARK) * SOLAR_G
    if charging:
        q -= 0.15 * SOLAR_G
    r_below = R_BASE if scenario == "closed_flat" else R_FACE
    if arch == "A":
        # top = lid shell outer skin; (Tt - Td)/R_mid = (Td - Ta)/R_below
        r = R_MID_A + r_below
        tt = q / (htop + 1 / r)
        qd = tt / r
        return tt, tt, qd * r_below
    vent = scenario == "open_back_sun"
    hch = h_chimney(gap) if (vent and gap > 0) else 0.0
    if gap <= 0:
        hpl = 1 / 0.01                                                   # bonded / contact: FR4 + tray
    else:
        hpl = K_AIR / (gap / 1000) + h_rad_gap(EPS_DARK, EPS_FOIL if foil else EPS_DARK)
    # unknowns: Tp, Tl, Td (rises)
    A = [[htop + hch + hpl, -hpl, 0.0],
         [-hpl, hpl + hch + 1 / R_CORE_B, -1 / R_CORE_B],
         [0.0, -1 / R_CORE_B, 1 / R_CORE_B + 1 / r_below]]
    tp, tl, td = solve(A, [q, 0.0, 0.0])
    return tp, tl, td


# =====================================================================================================================
# ORIENTATION (panel normal range and cosine factor; operator / lid shading by ray casting)
# =====================================================================================================================
def normal_range(arch, phi):
    """Achievable panel-normal elevations (deg, measured in the Y-Z plane from +Y rear-horizontal toward up)."""
    if arch == "A":
        return 90 - phi - ENV["SOLAR_INDEX_RANGE"], 90 - phi + ENV["SOLAR_INDEX_RANGE"]
    return 90 - phi, 90 - phi + PSI_MAX


def sun_vec(where, el_deg):
    e = el_deg * DEG
    return {"front (behind user)": (0.0, -math.cos(e), math.sin(e)), "rear (behind device)": (0.0, math.cos(e), math.sin(e)),
            "right": (math.cos(e), 0.0, math.sin(e)), "left": (-math.cos(e), 0.0, math.sin(e))}[where]


def best_aim(arch, s, phis=(100, 105, 110, 115, 120, 125)):
    best = (0.0, None, None)
    for phi in phis:
        lo, hi = normal_range(arch, phi)
        lo, hi = max(lo, 0.0), min(hi, 180.0)                 # cells facing at or above the horizon only
        e = lo
        while e <= hi + 1e-9:
            n = (0.0, math.cos(e * DEG), math.sin(e * DEG))
            f = sum(n[i] * s[i] for i in range(3))
            if f > best[0]:
                best = (f, phi, e)
            e += 1.0
    return best


def ray_box(o, d, bmin, bmax):
    t0, t1 = 1e-6, 1e9
    for i in range(3):
        if abs(d[i]) < 1e-12:
            if o[i] < bmin[i] or o[i] > bmax[i]:
                return False
        else:
            a, b = (bmin[i] - o[i]) / d[i], (bmax[i] - o[i]) / d[i]
            t0, t1 = max(t0, min(a, b)), min(t1, max(a, b))
            if t0 > t1:
                return False
    return True


def ray_obb(o, d, body, ps, bmin, bmax):
    """Ray vs a body-frame box transformed by the pose (rotations about X only): invert the transform on the ray."""
    phi = ps["phi"]
    o2 = rot_x(o, phi, HAY, HAZ)
    d2 = rot_vx(d, phi)
    if body == "leaf":
        o2 = rot_x(o2, -ps["psi"], B1_AXIS[0], B1_AXIS[1])
        d2 = rot_vx(d2, -ps["psi"])
    elif body.startswith("A_cas_"):
        sd = body[-1]
        sg = 1 if sd == "R" else -1
        o2 = (o2[0] - sg * ps["s" + sd] * ENV["SOLAR_SLIDE_TRAVEL"], o2[1], o2[2])
        hy = ENV["HYR"] if sd == "R" else ENV["HYL"]
        o2 = rot_x(o2, -ps["t" + sd], hy, ENV["HZ"])
        d2 = rot_vx(d2, -ps["t" + sd])
    return ray_box(o2, d2, bmin, bmax)


OPERATOR = ((-230.0, -520.0, -300.0), (230.0, -300.0, 480.0))   # ASSUMED seated operator torso + head box, table z = 0


def shaded_fraction(arch, ps, s, n_samp=9):
    """Fraction of the panel sample points whose ray toward the sun hits the lid, base, other wing or operator."""
    lid_box = ((-W / 2, 0.0, ZF), (W / 2, D, ZF + (LID_A if arch == "A" else B1_CORE)))
    base_box = ((-W / 2, 0.0, 0.0), (W / 2, D, H))
    if arch == "A":
        panels = []
        for sd in ("R", "L"):
            sg = 1 if sd == "R" else -1
            x0, x1 = sorted((sg * ENV["XI"], sg * (ENV["XI"] + ENV["SOLAR_CASSETTE_WIDTH"])))
            panels.append((f"A_cas_{sd}", (x0, ENV["CY0"], ENV["ZC0"]), (x1, ENV["CY1"], ENV["ZC1"])))
    else:
        panels = [("leaf", (-B1_LEAF_W / 2, 0.0, B1_Z_LEAF0), (B1_LEAF_W / 2, D, B1_Z_LEAF0 + B1_LEAF_T))]
    tot = hit = 0
    for body, bmin, bmax in panels:
        for i in range(n_samp):
            for j in range(n_samp):
                p = (bmin[0] + (i + 0.5) / n_samp * (bmax[0] - bmin[0]), bmin[1] + (j + 0.5) / n_samp * (bmax[1] - bmin[1]), bmax[2] + 0.01)
                o = to_world(body, p, ps)
                tot += 1
                blocked = ray_obb(o, s, "lid", ps, *lid_box) or ray_box(o, s, *base_box) or ray_box(o, s, *OPERATOR)
                if not blocked and arch == "A":
                    for b2, mn, mx in panels:
                        if b2 != body and ray_obb(o, s, b2, ps, mn, mx):
                            blocked = True
                if blocked:
                    hit += 1
    return hit / tot


# =====================================================================================================================
# B1 COLLISION SWEEP (Y-Z sections are exact: full-width parts, all motions about X-parallel axes)
# =====================================================================================================================
def poly_world(body, rect, ps):
    y0, z0, y1, z1 = rect
    return [to_world(body, (0.0, y, z), ps)[1:] for y, z in ((y0, z0), (y1, z0), (y1, z1), (y0, z1))]


def seg_dist(p, a, b):
    ab = (b[0] - a[0], b[1] - a[1])
    t = max(0.0, min(1.0, ((p[0] - a[0]) * ab[0] + (p[1] - a[1]) * ab[1]) / (ab[0] ** 2 + ab[1] ** 2)))
    return math.hypot(p[0] - a[0] - t * ab[0], p[1] - a[1] - t * ab[1])


def convex_gap(P, Q):
    """Signed clearance between convex polygons (negative = penetration depth estimate via SAT)."""
    best = -1e9
    for poly in (P, Q):
        for i in range(len(poly)):
            a, b = poly[i], poly[(i + 1) % len(poly)]
            n = (b[1] - a[1], -(b[0] - a[0]))
            ln = math.hypot(*n)
            n = (n[0] / ln, n[1] / ln)
            pa = [x[0] * n[0] + x[1] * n[1] for x in P]
            qa = [x[0] * n[0] + x[1] * n[1] for x in Q]
            best = max(best, min(qa) - max(pa), min(pa) - max(qa))
    if best < 0:
        return best
    return min(min(seg_dist(p, Q[i], Q[(i + 1) % len(Q)]) for p in P for i in range(len(Q))),
               min(seg_dist(q, P[i], P[(i + 1) % len(P)]) for q in Q for i in range(len(P))))


ZC_B1 = ZF + B1_CORE                       # lid back = leaf frame underside (the frame bars rest on it)
RELIEF = (4.0, ZC_B1 + 2.3)               # front-bottom corner relief: y < 4 and z < zc + 2.3 removed (points behind the axis stay within R7: 1 mm clearance)


def leaf_poly(ps):
    """Leaf frame section (convex hull incl. the relief chamfer) in world Y-Z."""
    pts = [(0.0, RELIEF[1]), (RELIEF[0], ZC_B1), (D, ZC_B1), (D, ZF + B1_LID_T), (0.0, ZF + B1_LID_T)]
    return [to_world("leaf", (0.0, y, z), ps)[1:] for y, z in pts]


def b1_sweep():
    """Leaf vs lid core, base, table and the rear plug keep-outs over phi x psi; lid (B1 / A) vs plug keep-out."""
    core = (0.0, ZF, D, ZF + B1_CORE)
    base = (0.0, 0.0, D, H)
    plug = (D, 4.0, D + ENV["PLUG_KEEPOUT_LENGTH"], 19.0)
    table = (-400.0, -FOOT_H - 50, 900.0, -FOOT_H)
    rows = []
    for phi in (0, 90, 110, 125, 135):
        for psi in (0, 10, 20, 30, 45, 60, 90, 110, 135, 160, 190):
            ps = pose(phi=phi, psi=psi)
            L = leaf_poly(ps)
            g_core = convex_gap(L, poly_world("lid", core, ps)) if psi > 0 else 0.0
            g_base = convex_gap(L, poly_world("base", base, ps))
            g_plug = convex_gap(L, poly_world("base", plug, ps))
            g_tab = convex_gap(L, poly_world("base", table, ps))
            rows.append((phi, psi, g_core, g_base, g_plug, g_tab))
    lidp = []
    for T, lab in ((LID_A, "A 37.6"), (B1_LID_T, f"B1 {B1_LID_T:g}")):
        for phi in (110, 120, 125, 130, 135):
            g = convex_gap(poly_world("lid", (0.0, ZF, D, ZF + T), pose(phi=phi)), poly_world("base", plug, pose()))
            lidp.append((lab, phi, g))
    return rows, lidp


def leaf_axis_relief():
    """Leaf underside front corner vs the core top over psi 0..190, square corner vs relieved corner."""
    ax = B1_AXIS
    r_core = ax[1] - ZC_B1
    out = []
    for corner in ((0.0, ZC_B1), (0.0, RELIEF[1]), RELIEF[:1] + (ZC_B1,)):
        w = 1e9
        for k in range(1, 191):
            p = rot_x((0.0, corner[0], corner[1]), k, *ax)
            if p[1] > 0:
                w = min(w, p[2] - ZC_B1)
        out.append(w)
    return r_core, out


# =====================================================================================================================
# REPORT
# =====================================================================================================================
def fmt_m(v):
    return f"{v * 1000:.0f} g"


def section(t):
    print("\n" + "=" * 118 + f"\n{t}\n" + "=" * 118)


def main(argv):
    print("D-010 PHASE 2 — A (sliding wings) vs B1 (solar-lid leaf). NON-PRODUCTION; CALCULATED from the tagged inputs.")
    print(f"envelope (YAML): base {W:g} x {D:g} x {H:g}; display hinge (y {HAY:g}, z {HAZ:g}); A lid {LID_A:g}; "
          f"B1 lid {B1_LID_T:g} (core {B1_CORE:g} EST + gap {B1_GAP:g} + leaf {B1_LEAF_T:g}); B1 leaf axis (y {B1_AXIS[0]:g}, z {B1_AXIS[1]:g}); "
          f"feet {FOOT_H:g} high, inset {FOOT_INSET:g} (ASSUMED)")

    section("1. SOLAR AREA AND POWER")
    cas_a = ENV["SOLAR_CASSETTE_WIDTH"] * ENV["SOLAR_CASSETTE_HEIGHT"]
    a_lam = (ENV["SOLAR_CASSETTE_WIDTH"] - 12) * (ENV["SOLAR_CASSETTE_HEIGHT"] - 10)
    p108, p126 = PANELS["P108"], PANELS["P126"]
    b_max = B1_LEAF_W * B1_LEAF_D
    b_lam = (B1_LEAF_W - 12) * (B1_LEAF_D - 12)
    rows = [("A max physical (2 cassette faces)", 2 * cas_a, None, "CALC (YAML)"),
            ("A custom laminate 2 x 135.5 x 190", 2 * a_lam, tuple(2 * a_lam * 1e-6 * k for k in CUSTOM_W_M2), "ASSUMED laminate"),
            ("A catalog: 1 x P126 per cassette (largest catalog fit)", 2 * p126["x"] * p126["y"], (2 * p126["W"][0],) * 3, "VENDOR"),
            ("B1 max physical (leaf outline)", b_max, None, "CALC"),
            ("B1 catalog: 1 x P108 (fits the leaf)", p108["x"] * p108["y"], (p108["W"][0], sum(p108["W"]) / 2, p108["W"][1]), "VENDOR"),
            ("B1 custom laminate 277 x 223", b_lam, tuple(b_lam * 1e-6 * k for k in CUSTOM_W_M2), "ASSUMED laminate")]
    for lab, a, pw, src in rows:
        extra = ""
        if pw:
            extra = (f"nameplate {pw[0]:.1f} / {pw[1]:.1f} / {pw[2]:.1f} W; real at best aim {pw[1] * REAL_FACTOR[0]:.1f}..{pw[1] * REAL_FACTOR[1]:.1f} W; "
                     f"day {pw[1] * REAL_FACTOR[0] * PEAK_SUN_H[0]:.0f}..{pw[1] * REAL_FACTOR[1] * PEAK_SUN_H[1]:.0f} Wh")
        print(f"  {lab}: {a / 100:.0f} cm2  {extra}  [{src}]")
    print(f"  fit: P105 (148 x 221) does NOT fit A's 147.5 x 200 cassette; P108 (273 x 223) fits B1's leaf with 8 / 6 mm frame "
          f"margins. Stowed exposed PV: A 0 cm2 (inside the lid), B1 {p108['x'] * p108['y'] / 100:.0f} cm2 (charges closed).")

    section("2. MASS (nominal, low..high; tags per item in the report)")
    tot = {}
    for arch in ("A", "B1"):
        lst = BASE_ITEMS + (A_ITEMS if arch == "A" else B1_ITEMS + STAY_ITEMS)
        groups = {}
        for it in lst:
            if it[4] == "base":
                g = "base (common)"
            elif it in LID_COMMON:
                g = "display + controller + hinge (common)"
            elif it[0].startswith("A lid") or it[0].startswith("B1 lid") or "spacers" in it[0]:
                g = "lid structure"
            else:
                g = "solar subsystem"
            groups.setdefault(g, [0.0, 0.0, 0.0])
            for k in range(3):
                groups[g][k] += it[1 + k]
        tot[arch] = [sum(it[1 + k] for it in lst) for k in range(3)]
        print(f"  {arch}: total {tot[arch][0]:.2f} kg ({tot[arch][1]:.2f}..{tot[arch][2]:.2f})")
        for g, v in groups.items():
            print(f"      {g}: {v[0] * 1000:.0f} g ({v[1] * 1000:.0f}..{v[2] * 1000:.0f})")
    print("  A solar items:")
    for it in a_side("R"):
        print(f"      {it[0]} x2: {2 * it[1] * 1000:.0f} g [{it[6]}]")
    print("  B1 solar items:")
    for it in B1_ITEMS[3:] + STAY_ITEMS:
        if "lid structure" not in it[0]:
            print(f"      {it[0]}: {it[1] * 1000:.0f} g [{it[6]}]")
    print(f"  B1 with a custom semi-flexible laminate instead of P108 (+ 60 g backing): leaf "
          f"{(CUSTOM_KG_M2[0] * b_lam * 1e-6 + 0.06) * 1000:.0f}..{(CUSTOM_KG_M2[1] * b_lam * 1e-6 + 0.06) * 1000:.0f} g vs {p108['kg'] * 1000:.0f} g panel")

    section("3. CENTRE OF GRAVITY (world, mm; nominal masses) and movement")
    cg_tab = {}
    for arch in ("A", "B1"):
        m0, c0 = cog(items_for(arch, pose()))
        for name, ps in STATES[arch]:
            m, c = cog(items_for(arch, ps))
            cg_tab[(arch, name)] = (m, c)
            print(f"  {arch:2s} {name:14s} phi {ps['phi']:5.0f}  "
                  + (f"s {ps['sR']:.1f}/{ps['sL']:.1f} tilt {ps['tR']:+4.0f}/{ps['tL']:+4.0f}" if arch == "A" else f"psi {ps['psi']:5.0f} stay {'Y' if ps['stay'] else 'N'}")
                  + f"  CG x {c[0]:+6.1f} y {c[1]:6.1f} z {c[2]:5.1f}   move from stowed dx {c[0] - c0[0]:+5.1f} dy {c[1] - c0[1]:+6.1f} dz {c[2] - c0[2]:+5.1f}")
    print("  worst-case solar deployment for rear stability (max CG y), phi 90..135:")
    for arch in ("A", "B1"):
        best = None
        for phi in range(90, 136, 5):
            if arch == "A":
                for t in range(-75, 76, 15):
                    ps = pose(phi=phi, sR=1, tR=t, sL=1, tL=t)
                    c = cog(items_for(arch, ps))[1]
                    best = max(best or (-1e9,), (c[1], phi, t, c))
            else:
                for psi in range(0, int(PSI_MAX) + 1, 5):
                    ps = pose(phi=phi, psi=psi)
                    c = cog(items_for(arch, ps))[1]
                    best = max(best or (-1e9,), (c[1], phi, psi, c))
        print(f"    {arch}: CG y {best[0]:.1f} (z {best[3][2]:.1f}) at phi {best[1]}, {'tilt' if arch == 'A' else 'psi'} {best[2]}  "
              f"(rear support line y {D - FOOT_INSET:g})")

    section("4. TIPPING / WIND (support = foot rectangle; Cn plate model; worst of wind azimuth +-30 and incl -10/0/+10)")
    print("   state                    | CG margin rear/front/side mm | tip wind rear / front / side m/s | rearward push at the top that tips it")
    for arch in ("A", "B1"):
        extra = ([("DISPLAY_OPEN_125", pose(phi=125)), ("MAX + same stay", pose(phi=125, sR=1, tR=75, sL=1, tL=75, stay=True))] if arch == "A"
                 else [("NORMAL + stay", pose(phi=110, psi=65, stay=True)), ("HORIZONTAL no stay", pose(phi=110, psi=110)),
                       ("MAX no stay", pose(phi=110, psi=PSI_MAX)), ("UPRIGHT 125 no stay", pose(phi=125, psi=170)),
                       ("UPRIGHT 125 + stay", pose(phi=125, psi=170, stay=True))])
        for name, ps in STATES[arch] + extra:
            m, c, res, top = stability(arch, ps)
            wv = worst(res)
            side = min(wv["left"]["v_tip"], wv["right"]["v_tip"])
            sm = min(wv["left"]["margin"], wv["right"]["margin"])
            print(f"   {arch:2s} {name:22s} | {wv['rear']['margin']:6.0f} / {wv['front']['margin']:5.0f} / {sm:5.0f}       | "
                  f"{wv['rear']['v_tip']:5.1f} / {wv['front']['v_tip']:5.1f} / {side:5.1f}             | "
                  f"{wv['rear']['push']:5.1f} N at z {top:.0f}")
    print("   base-mass sensitivity (rear tip wind, m/s) light / nominal / heavy:")
    for arch, name, ps in (("A", "NORMAL", STATES["A"][3][1]), ("A", "MAX", STATES["A"][4][1]), ("B1", "NORMAL", STATES["B1"][3][1]),
                           ("B1", "HORIZONTAL_NO_STAY", pose(phi=110, psi=110)), ("B1", "STAY_DEPLOYED", STATES["B1"][5][1])):
        vv = [worst(stability(arch, ps, case)[2])["rear"]["v_tip"] for case in ("lo", "nom", "hi")]
        print(f"      {arch} {name}: {vv[0]:.1f} / {vv[1]:.1f} / {vv[2]:.1f}")
    print("   reference: NOMAD lid open 110, no solar deployed -> see A/B1 DISPLAY_OPEN rows")

    section("5. HINGE TORQUES")
    print("  display (lid) hinge, gravity torque N.m (+ = falls open), nominal / heavy parts; + front-wind torque at 10 m/s")
    for arch in ("A", "B1"):
        rows = []
        for phi in (90, 100, 110, 125, 135):
            if arch == "A":
                cands = [pose(phi=phi)] + [pose(phi=phi, sR=1, tR=t, sL=1, tL=t) for t in (-75, 0, 75)]
            else:
                cands = [pose(phi=phi, psi=p) for p in range(0, int(PSI_MAX) + 1, 10)]
            g = [lid_hinge_torque(arch, c, 10.0) for c in cands]
            gh = [lid_hinge_torque(arch, c, 0.0, "hi")[0] for c in cands]
            rows.append((phi, min(x[0] for x in g), max(x[0] for x in g), max(gh), max(abs(x[1]) for x in g)))
        for phi, lo, hi, hh, tw in rows:
            print(f"    {arch:2s} phi {phi:3d}: gravity {lo:+.2f} .. {hi:+.2f} (heavy {hh:+.2f}); front wind 10 m/s {tw:.2f}")
    print("  B1 leaf hinge (about the leaf axis), |gravity| max over psi and phi 90..135; wind on the leaf at 10 m/s (Cn 1.2)")
    gmax = max(abs(leaf_hinge_torque(pose(phi=p, psi=s))[0]) for p in (90, 110, 125, 135) for s in range(0, 191, 5))
    gmax_hi = max(abs(leaf_hinge_torque(pose(phi=p, psi=s), 0, "hi")[0]) for p in (90, 110, 125, 135) for s in range(0, 191, 5))
    tw10 = leaf_hinge_torque(pose(phi=110, psi=110), 10.0)[1]
    tw5 = leaf_hinge_torque(pose(phi=110, psi=110), 5.0)[1]
    hold = (gmax_hi + tw10) * 1.5
    print(f"    gravity max {gmax:.2f} N.m (heavy {gmax_hi:.2f}); wind 5 m/s {tw5:.2f}, 10 m/s {tw10:.2f} N.m")
    print(f"    required holding torque (heavy gravity + 10 m/s wind) x 1.5 = {hold:.2f} N.m total -> {hold / 2:.2f} N.m per hinge (2 hinges)")
    lever = (B1_LEAF_D - B1_AXIS[0]) / 1000
    print(f"    deploy force at the free edge (friction {hold:.2f} + gravity {gmax_hi:.2f}): {(hold + gmax_hi) / lever:.1f} N; "
          f"close force: {max(0.0, hold - 0) / lever:.1f} N (gravity may assist)")
    pin_shear = (items_for("B1", pose(), "hi", False))
    leaf_m = sum(i[1] for i in pin_shear if i[3] == "leaf")
    fw = 0.5 * RHO_AIR * 100 * B1_LEAF_W * B1_LEAF_D * 1e-6 * CN_MAX
    print(f"    leaf mass (heavy) {leaf_m * 1000:.0f} g; hinge shear (weight + 10 m/s wind) {(leaf_m * G + fw):.1f} N total "
          f"-> {(leaf_m * G + fw) / 2:.1f} N per hinge (printed knuckle + 4 mm steel pin: bearing "
          f"{(leaf_m * G + fw) / 2 / (4 * 8):.2f} MPa over 4 x 8 mm; PETG allowable >> this)")
    print("  A: hub loads per D-009 (T_d 1.26 N.m design, handling 5 N at 114.3), S1-R PASS; PETG hub bracket below SF 2 "
          "(bearing 1.88 / tear-out 1.73 / tension 1.61) -> OPEN (unchanged by this study)")

    section("6. B1 STAY OPTIONS (rear tip wind, NORMAL-worst pose phi 110 psi 110, nominal masses)")
    base_ps = pose(phi=110, psi=110)
    v0 = worst(stability("B1", base_ps)[2])["rear"]["v_tip"]
    print(f"   no stay: {v0:.1f} m/s")
    for x in (STAY_ARM["x"], 60.0):
        for L in (60.0, 90.0, 105.0):
            ps = pose(phi=110, psi=110, stay=True)
            r = worst(stability("B1", ps, "nom", (x, STAY_ARM["y0"] + L))[2])
            print(f"   rear outrigger arms at x +-{x:g}, reach {L:g} (feet y {STAY_ARM['y0'] + L:g}): rear {r['rear']['v_tip']:.1f} m/s, "
                  f"side {min(r['left']['v_tip'], r['right']['v_tip']):.1f} m/s")
    # lid-side prop: pivot at distance a from the lid hinge, stowed along the lid side toward the top (length <= D - a)
    for a in (60.0, 100.0):
        piv = to_world("lid", (0.0, HAY - a, ZF + B1_CORE / 2), pose(phi=110))
        Lp = D - a
        if Lp > piv[2] + FOOT_H:
            yf = piv[1] + math.sqrt(Lp ** 2 - (piv[2] + FOOT_H) ** 2)
            r = worst(stability("B1", pose(phi=110, psi=110, stay=True), "nom", (W / 2 + 6, yf))[2])
            mu = (yf - piv[1]) / (piv[2] + FOOT_H)
            print(f"   lid-side folding props, pivot {a:g} from the hinge (length {Lp:g}): feet y {yf:.0f} -> rear {r['rear']['v_tip']:.1f} m/s; "
                  f"a pinned prop at {math.degrees(math.atan(mu)):.0f} deg from vertical needs foot friction mu >= {mu:.2f} (rubber on a table ~0.6-0.9 ASSUMED); "
                  f"its foot position also changes with the lid angle")
        else:
            print(f"   lid-side folding props, pivot {a:g} from the hinge: length {Lp:g} cannot reach the table (pivot z {piv[2]:.0f})")
    ps = pose(phi=110, psi=0)
    r = worst(stability("B1", ps)[2])
    print(f"   leaf folded back (psi 0, still charging on the lid back): rear {r['rear']['v_tip']:.1f} m/s  (operating fallback)")
    # stay loads: upper bound = the whole device weight on the two feet (base front lifted) x 1.5
    m = cog(items_for("B1", pose(phi=110, psi=110, stay=True), "hi"))[0]
    R = m * G * 1.5
    t_, b_ = STAY_ARM["section"]
    Mb = R / 2 * (STAY_ARM["L"] - (D - STAY_ARM["y0"])) / 1000
    sig = Mb / (b_ * t_ ** 2 / 6 * 1e-9) / 1e6
    pry = Mb / (STAY_ARM["root"] / 1000)
    print(f"   stay load (bound: heavy device {m:.2f} kg entirely on the feet x 1.5): {R:.0f} N, {R / 2:.0f} N per arm; bending at the "
          f"base edge {Mb:.2f} N.m -> {sig:.0f} MPa in a {t_:g} x {b_:g} stainless flat (1.4301 cold-rolled yield >= 300 MPa EST); "
          f"root couple over {STAY_ARM['root']:g} mm -> {pry:.0f} N on the pivot screw / insert (M4 insert pull-out in PETG ~1 kN EST)")
    print(f"   stowed: each arm {STAY_ARM['L'] + STAY_ARM['root']:g} long, pointing forward under the base side (y "
          f"{STAY_ARM['y0'] - STAY_ARM['L']:g}..{STAY_ARM['y0'] + STAY_ARM['root']:g}, x {STAY_ARM['x'] - 8:g}..{STAY_ARM['x'] + 8:g}) in the "
          f"{FOOT_H:g} mm foot gap, clear of the feet (x >= {W / 2 - FOOT_INSET - 6:g}); swings 180 deg on the pivot; deployed: rearward, "
          f"feet at y {STAY_ARM['y0'] + STAY_ARM['L']:g}, x +-{STAY_ARM['x']:g} (outside the plug zones x 20..110)")

    section("7. CABLE ROUTING (anchor routes drawn in Onshape; lengths through fillets at the static radius)")
    for lab, route, cab, states in (("A right", a_route("R"), CABLE_A, STATES["A"]), ("A left", a_route("L"), CABLE_A, STATES["A"]),
                                    ("B1", b1_route(), CABLE_B, STATES["B1"])):
        print(f"  {lab}: cable d {cab['d']:g}, static R {cab['R']:g}, repeated-flex R {cab['R_dyn']:g} (ASSUMED 3d / 6d)")
        lens = []
        for name, ps in states:
            ln, rmin, fl = fillet_path(route_world(route, ps), cab["R"])
            lens.append(ln)
            bad = [i for i, _ in fl]
            if name in ("STOWED", "MAX", "NORMAL"):
                print(f"      {name:14s} length {ln:6.0f} mm; static corners below R at anchors {bad if bad else 'none'}"
                      + (f" (smallest {rmin:.1f})" if bad else ""))
        print(f"      length change over all states {max(lens) - min(lens):.1f} mm (the drawn path; the loop / twist zones absorb motion)")
        for tag, i, ln in moving_sections(route):
            print(f"      moving section '{tag}' from anchor {i} ({route[i][0]} -> {route[i + 1][0]}), {ln:.1f} mm")
    cro, link = ENV["CRO"], ENV["SOLAR_HUB_LINK_LENGTH"]
    print("  A hub link (inherent to D-009: cable centre CRO from the tilt axis, link length between cassette and carriage):")
    for tilt in (15, 45, 80):
        disp = 2 * cro * math.sin(tilt * DEG / 2)
        span = link + 7.5 + 2
        r_s = (span / 2) ** 2 / disp + disp / 4 if disp > 0 else 1e9
        print(f"      tilt {tilt:2d}: cable end moves {disp:.1f} mm across a {span:.1f} mm free span -> S-bend R ~{r_s:.1f} mm "
              f"= {r_s / CABLE_A['d']:.1f} d (repeated-flex min {CABLE_A['R_dyn'] / CABLE_A['d']:.0f} d)")
    print(f"  A rolling loop: R {CABLE_A['loop_R']:g} = {CABLE_A['loop_R'] / CABLE_A['d']:.1f} d for the YAML d {CABLE_A['d']:g} "
          f"(repeated flex wants ~6 d = {CABLE_A['R_dyn']:g}; a 4 mm cable gives {CABLE_A['loop_R'] / 4:.1f} d)")
    print(f"  A carriage -> loop hop: cable centre {ENV['HYR'] + ENV['CRO']:.1f} inside the rail channel (rail wall at y "
          f"{ENV['RCR'] + ENV['RW2']:.1f}), loop moving run at {ENV['LRY0'] + CABLE_A['d'] / 2:.1f}: the cable must pass the "
          f"structural rail wall along the whole travel (side slot) or exit through the top slot, which is "
          f"{ENV['ZC0'] - ENV['ZR1']:g} mm below the stowed cassette -> UNRESOLVED in E2")
    print(f"  A right hinge crossing: twist zone {134 - 115:g} mm for 135 deg = {135 / 19:.1f} deg/mm (limit {TWIST_OK_DEG_PER_MM}) "
          f"-> needs a loop instead (space: hinge mount x 120..148 / port zone x <= 110)")
    print(f"  A left hinge crossing (centre): twist {135 / 72:.2f} deg/mm over 72 mm")
    tw_b = PSI_MAX / (141 - 72)
    print(f"  B1 leaf knuckle twist: {PSI_MAX:g} deg over {141 - 72:g} mm = {tw_b:.2f} deg/mm; display-hinge centre twist 135 deg "
          f"over 49 mm = {135 / 49:.2f} deg/mm (limit {TWIST_OK_DEG_PER_MM} ASSUMED); no loop, no hop, no S-bend")

    section("8. THERMAL (rise above ambient K, full sun 1000 W/m2, battery full = no extraction unless noted; ESTIMATES)")
    print(f"   internal resistances: R_mid A {R_MID_A:.3f}, R_core B1 {R_CORE_B:.3f}, R_base {R_BASE}, R_face {R_FACE} m2K/W; "
          f"h_rad gap dark/dark {h_rad_gap(0.9, 0.9):.1f}, dark/foil {h_rad_gap(0.9, 0.1):.1f} W/m2K; "
          f"chimney h 4/6/10 mm {h_chimney(4):.1f}/{h_chimney(6):.1f}/{h_chimney(10):.1f} W/m2K per face")
    for scen, lab in (("closed_flat", "CLOSED, lying flat, sun on top"), ("open_back_sun", "OPEN, sun on the lid back, display shaded")):
        print(f"   {lab}:")
        for hk, hv in H_TOP.items():
            ta = thermal_case("A", 0, False, scen, hv)
            print(f"     [{hk}] A dark lid shell: shell {ta[0]:+.0f}, display {ta[2]:+.0f} | A light-grey shell (a 0.5): "
                  f"shell {ta[0] * ALPHA_LIGHT / ALPHA_DARK:+.0f}, display {ta[2] * ALPHA_LIGHT / ALPHA_DARK:+.0f}")
            for gap, foil in ((0, False), (4, False), (6, False), (6, True), (10, False)):
                tp, tl, td = thermal_case("B1", gap, foil, scen, hv)
                print(f"       B1 gap {gap:2d}{' +foil' if foil else '      '}: panel {tp:+.0f}, lid back shell {tl:+.0f}, display {td:+.0f}")
    print(f"   deployed panel free on both sides, charging: panel +{(0.9 - 0.15) * SOLAR_G / (H_TOP['light wind ~1 m/s'] + 10):.0f} (light wind) .. "
          f"+{(0.9 - 0.15) * SOLAR_G / (H_TOP['still air'] + 7):.0f} K (still) — same physics for an A wing and the B1 leaf")
    print(f"   at T_amb {T_AMB:g} C: PETG HDT(0.45 MPa) ~{PETG['HDT_045']:g} C, Tg ~{PETG['Tg']:g} C; ASA HDT ~{ASA['HDT_045']:g} C (EST)")

    section("9. ORIENTATION (best cosine factor; user sets lid 100..125 and A tilt / B1 leaf; device heading FIXED)")
    print("   sun direction          elev |  A best (lid, normal)  shade | B1 best (lid, normal)  shade")
    for where in ("rear (behind device)", "front (behind user)", "right", "left"):
        for el_ in (10, 30, 60):
            s = sun_vec(where, el_)
            fa, pa, na = best_aim("A", s)
            fb, pb, nb = best_aim("B1", s)
            sha = sf = 0.0
            if pa is not None:
                t = na - (90 - pa)
                sha = shaded_fraction("A", pose(phi=pa, sR=1, tR=t, sL=1, tL=t), s)
            if pb is not None:
                sf = shaded_fraction("B1", pose(phi=pb, psi=nb - (90 - pb)), s)
            print(f"   {where:22s} {el_:4d} | {fa:5.2f} ({pa}, {na}) {sha:5.0%} | {fb:5.2f} ({pb}, {nb}) {sf:5.0%}"
                  f"   -> effective A {fa * (1 - sha):.2f}, B1 {fb * (1 - sf):.2f}")
    s = (0.0, 0.0, 1.0)
    print(f"   overhead: A {best_aim('A', s)[0]:.2f}, B1 {best_aim('B1', s)[0]:.2f}")
    print(f"   normal elevation range at lid 110: A {normal_range('A', 110)}, B1 {normal_range('B1', 110)} (deg from rear-horizontal)")
    # visor check: leaf over the screen requires psi > 180 + (phi - 90): normal then points down/forward
    for psi in (170, 190, 250, 290):
        n = to_world_vec("leaf", (0, 0, 1), pose(phi=110, psi=psi))
        d_ = to_world_vec("leaf", (0, 1, 0), pose(phi=110, psi=psi))
        print(f"   visor check psi {psi}: leaf points (y {d_[1]:+.2f}, z {d_[2]:+.2f}) from the lid top; cells face (y {n[1]:+.2f}, z {n[2]:+.2f})")

    section("10. B1 COLLISION SWEEP (Y-Z sections, mm; negative = interference)")
    rows, lidp = b1_sweep()
    r_core, w = leaf_axis_relief()
    rc = math.hypot(B1_AXIS[0], B1_AXIS[1] - ZC_B1)
    print(f"   leaf frame underside front corner is {rc:.2f} from the leaf axis vs {r_core:.1f} axis-to-core-top: square corner dips "
          f"{w[0]:+.2f} mm into the core (at psi ~27) -> relief y < {RELIEF[0]:g}, z < {RELIEF[1]:g} keeps every point within R8: "
          f"relieved corners {w[1]:+.2f} / {w[2]:+.2f} mm")
    print("   phi  psi | leaf-core leaf-base leaf-plug leaf-table")
    for phi, psi, gc, gb, gp, gt in rows:
        if phi in (0, 110, 135) or gb < 2 or gp < 2 or gt < 2:
            print(f"   {phi:3d} {psi:4d} | {gc:8.1f} {gb:9.1f} {gp:9.1f} {gt:10.1f}")
    print("   lid (stowed stack) vs rear plug keep-out (y 235..280, z 4..19):")
    for lab, phi, g in lidp:
        print(f"      {lab} phi {phi}: {g:+.1f} mm")

    section("11. PORTABILITY")
    for arch, T in (("A", LID_A), ("B1", B1_LID_T)):
        h = H + ENV["LID_CLOSED_GAP"] + T
        print(f"   {arch}: closed {W:g} x {D:g} x {h:.1f} mm = {W * D * h / 1e6:.2f} L (+ feet {FOOT_H:g}); mass {tot[arch][0]:.2f} kg "
              f"({tot[arch][1]:.2f}..{tot[arch][2]:.2f})")
    print(f"   deployed footprint: A width {2 * (ENV['XI'] + ENV['SOLAR_SLIDE_TRAVEL'] + ENV['SOLAR_CASSETTE_WIDTH'] - ENV['SOLAR_SLIDE_TRAVEL']) + 2 * ENV['SOLAR_SLIDE_TRAVEL']:.0f} mm; "
          f"B1 depth with leaf horizontal ~{to_world('leaf', (0, D, B1_Z_LEAF0), pose(phi=110, psi=110))[1]:.0f} mm, "
          f"stay feet y {STAY_ARM['y0'] + STAY_ARM['L']:g}; B1 upright top z {max(to_world('leaf', (0, y, z), pose(phi=110, psi=PSI_MAX))[2] for y in (0, D) for z in (B1_Z_LEAF0, B1_Z_LEAF0 + 6)):.0f}")

    if "--emit" in argv:
        emit()
    return 0


# =====================================================================================================================
# FEATURESCRIPT DATA BLOCK
# =====================================================================================================================
BEGIN, END = "// BEGIN GENERATED D010 DATA", "// END GENERATED D010 DATA"


def fs_num(v):
    return f"{v:.4f}".rstrip("0").rstrip(".") if abs(v) > 1e-9 else "0"


def fs_vec(p):
    return "[" + ", ".join(fs_num(v) for v in p) + "]"


def emit():
    lines = [BEGIN, "// Generated by CAD/tools/d010_phase2_study.py --emit. DO NOT EDIT. Values in mm / kg / deg.",
             "// Source: nomad.yaml working values (via e_lid_layout / base_v01_layout) + the study INPUTS (tags in the script)."]
    env = {k: ENV[k] for k in ("BODY_WIDTH", "BODY_DEPTH", "BODY_HEIGHT", "ZF", "HAY", "HAZ", "LID_THICKNESS", "WALL_THICKNESS",
                               "DX", "DY0", "DY1", "ZD0", "ZD1", "XI", "CY0", "CY1", "ZC0", "ZC1", "HYR", "HYL", "HZ", "KX0", "KX1",
                               "RX1", "RCR", "RCL", "RW2", "ZR0", "ZR1", "CW2", "BW2", "BZ0", "SOLAR_HUB_PIN_DIAMETER",
                               "SOLAR_CASSETTE_WIDTH", "SOLAR_SLIDE_TRAVEL", "SOLAR_INDEX_PLATE_OUTER_RADIUS", "GX0",
                               "SOLAR_INDEX_PLATE_THICKNESS", "LRY0", "LRY1", "LLY0", "LLY1", "LPX0", "LPX1", "CBX0", "CBX1",
                               "CBY0", "IY1", "ZFR", "CBZ1", "HX0", "HLY0", "HINGE_BARREL_DIAMETER", "SW2", "IX", "IY0", "ZS0")}
    env.update({"FOOT_H": FOOT_H, "FOOT_INSET": FOOT_INSET, "B1_CORE": B1_CORE, "B1_GAP": B1_GAP, "B1_LEAF_T": B1_LEAF_T,
                "B1_LID_T": B1_LID_T, "B1_AXIS_Y": B1_AXIS[0], "B1_AXIS_Z": B1_AXIS[1], "B1_LEAF_W": B1_LEAF_W,
                "B1_Z_LEAF0": B1_Z_LEAF0, "P108_X": PANELS["P108"]["x"], "P108_Y": PANELS["P108"]["y"], "P108_T": PANELS["P108"]["t"],
                "PSI_MAX": PSI_MAX, "STAY_X": STAY_ARM["x"], "STAY_Y0": STAY_ARM["y0"], "STAY_L": STAY_ARM["L"],
                "STAY_T": STAY_ARM["section"][0], "STAY_B": STAY_ARM["section"][1], "STAY_ROOT": STAY_ARM["root"],
                "RELIEF_Y": RELIEF[0], "RELIEF_Z": RELIEF[1], "CABLE_A_D": CABLE_A["d"], "CABLE_A_R": CABLE_A["R"],
                "CABLE_B_D": CABLE_B["d"], "CABLE_B_R": CABLE_B["R"], "LOOP_APEX": _loop_apex()})
    lines.append("export const D010 = {")
    lines += [f'        "{k}" : {fs_num(v)},' for k, v in env.items()]
    lines[-1] = lines[-1].rstrip(",")
    lines.append("    };")
    # base reference prims (numeric, from the Round C layout evaluation = the E Base table)
    keep = ["ENV_KEYBOARD", "ENV_TRACKPAD", "ENV_PI_STACK", "ENV_COMPUTE_POWER", "ENV_POWER_ELECTRONICS",
            "ENV_BATTERY_BAY", "ENV_GNSS_MODULE", "KEEPOUT_PLUGS_MAIN", "KEEPOUT_PLUGS_AUX"]
    lines.append("// Round C base V0.1 envelopes (same evaluated layout table as NOMAD E Base), numeric: [name, [[kind, x0, y0, z0, x1, y1, z1]]]")
    lines.append("export const D010_BASE = [")
    for n, _, prims in BPARTS:
        if n in keep:
            ps = ", ".join(f'["{k}", {", ".join(fs_num(x) for x in v)}]' for k, _, v in prims)
            lines.append(f'        ["{n}", [{ps}]],')
    lines[-1] = lines[-1].rstrip(",")
    lines.append("    ];")
    # mass items
    lines.append("// Lumped masses [label, kg, body, [x, y, z] body frame] (nominal)")
    for arch, lst in (("A", BASE_ITEMS + A_ITEMS), ("B1", BASE_ITEMS + B1_ITEMS + STAY_ITEMS)):
        lines.append(f"export const D010_MASS_{arch} = [")
        lines += [f'        ["{it[0]}", {fs_num(it[1])}, "{it[4]}", {fs_vec(it[5])}],' for it in lst]
        lines[-1] = lines[-1].rstrip(",")
        lines.append("    ];")
    # routes
    for lab, route in (("A_R", a_route("R")), ("A_L", a_route("L")), ("B1", b1_route())):
        lines.append(f"export const D010_ROUTE_{lab} = [")
        lines += [f'        ["{b}", {fs_vec(p)}, "{tag}"],' for b, p, tag in route]
        lines[-1] = lines[-1].rstrip(",")
        lines.append("    ];")
    # states + python results for the part names
    lines.append("// Named states: [name, phi, sR, tR, sL, tL, psi, stay, rear tip wind m/s (calc, nominal)]")
    for arch in ("A", "B1"):
        lines.append(f"export const D010_STATES_{arch} = [")
        for name, ps in STATES[arch]:
            v = worst(stability(arch, ps)[2])["rear"]["v_tip"]
            lines.append(f'        ["{name}", {fs_num(ps["phi"])}, {fs_num(ps["sR"])}, {fs_num(ps["tR"])}, {fs_num(ps["sL"])}, '
                         f'{fs_num(ps["tL"])}, {fs_num(ps["psi"])}, {"true" if ps["stay"] else "false"}, {fs_num(round(v, 1))}],')
        lines[-1] = lines[-1].rstrip(",")
        lines.append("    ];")
    lines.append(END)
    block = "\n".join(lines)
    emit_harness()
    text = FS_PATH.read_text(encoding="utf-8")
    new = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), lambda _: block, text, flags=re.S)
    if new != text:
        FS_PATH.write_text(new, encoding="utf-8")
        print(f"\n{FS_PATH.name}: data block regenerated")
    else:
        print(f"\n{FS_PATH.name}: data block unchanged")


HARNESS_PATH = ROOT / "CAD" / "featurescript" / "NOMAD_D010_Concepts.test.fs"
HBEGIN, HEND = "// BEGIN GENERATED D010 EXPECTED", "// END GENERATED D010 EXPECTED"


def harness_expected():
    """Python values the kernel check compares against (same geometry definitions)."""
    exp = []
    for arch, ps, lab in (("A", pose(phi=125, sR=1, tR=75, sL=1, tL=75), "cgAmax"), ("B1", pose(phi=110, psi=110, stay=True), "cgB1stay"),
                          ("B1", pose(phi=110, psi=65), "cgB1normal")):
        c = cog(items_for(arch, ps))[1]
        exp.append((lab, arch, ps, [round(v, 4) for v in c]))
    plug = (D, 4.0, D + ENV["PLUG_KEEPOUT_LENGTH"], 19.0)
    g_a = convex_gap(poly_world("lid", (0.0, ZF, D, ZF + LID_A), pose(phi=120)), poly_world("base", plug, pose()))
    g_b = convex_gap(poly_world("lid", (0.0, ZF, D, ZF + B1_LID_T), pose(phi=125)), poly_world("base", plug, pose()))
    g_l = convex_gap(leaf_poly(pose(phi=110, psi=45)), poly_world("lid", (0.0, ZF, D, ZC_B1), pose(phi=110, psi=45)))
    return exp, {"plugA120": g_a, "plugB125": g_b, "leafCore45": g_l}


def emit_harness():
    exp, gaps = harness_expected()
    lines = [HBEGIN, "// Generated by CAD/tools/d010_phase2_study.py --emit (python expectations for the kernel check)."]
    lines.append("const D010_EXPECT_CG = [")
    for lab, arch, ps, c in exp:
        lines.append(f'        ["{lab}", "{arch}", {{ "phi" : {fs_num(ps["phi"])}, "sR" : {fs_num(ps["sR"])}, "tR" : {fs_num(ps["tR"])}, '
                     f'"sL" : {fs_num(ps["sL"])}, "tL" : {fs_num(ps["tL"])}, "psi" : {fs_num(ps["psi"])}, "stay" : {"true" if ps["stay"] else "false"} }}, '
                     f'{fs_vec(c)}],')
    lines[-1] = lines[-1].rstrip(",")
    lines.append("    ];")
    lines.append("const D010_EXPECT_GAP = { " + ", ".join(f'"{k}" : {fs_num(round(v, 4))}' for k, v in gaps.items()) + " };")
    lines.append(HEND)
    block = "\n".join(lines)
    text = HARNESS_PATH.read_text(encoding="utf-8")
    new = re.sub(re.escape(HBEGIN) + r".*?" + re.escape(HEND), lambda _: block, text, flags=re.S)
    if new != text:
        HARNESS_PATH.write_text(new, encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
