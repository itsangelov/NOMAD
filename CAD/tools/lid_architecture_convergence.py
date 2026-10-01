"""Round D.1: lid architecture convergence (analysis only; nothing is chosen, nothing is ranked).

Narrows Round D to three enclosed-cassette lid classes and evaluates them on one normalized basis:
  A  ~37-38 mm sandwich rear shell   (Round D architecture C)
  B  ~39-40 mm modular rail module    (Round D architecture D)
  C  ~42 mm ribbed rear shell         (Round D architecture B; conservative fallback, not preferred)

Also: printed rail vs printed rail + replaceable metal strips (coupon A2 geometry), hinge/port map per
class (D-006 / C.2 geometry, variable plug length), display/controller fit, solar (B.1 V1 + fixes)
re-validation including the re-spaced rails the strips need, manufacturing/self-assembly counts,
mass/handling (hinge torque, opening force, tip-back), and a thickness sweep for the convergence window.

  py CAD/tools/lid_architecture_convergence.py                 # full report
  py CAD/tools/lid_architecture_convergence.py --T 38 --reinf steel2 --h 4
  py CAD/tools/lid_architecture_convergence.py --skin 1.0 --rib-s 20 --rail-h 13 --cassette 8 --lip 0

Options (all local study values, NOT nomad.yaml): --T (force total lid thickness; the back structure gets
what is left), --skin (sandwich skin), --rib-h (ribbed class rib height), --rib-s (rib/web spacing),
--rail-h (solar rail layer height), --cassette (cassette thickness), --reinf (none|al2|steel2|al1|steel1),
--h (hinge-axis height), --lip (front display lip), --gap (cassette-to-back clearance).

Evidence levels: layer arithmetic and 2D/2.5D geometry = modeled (B.1 / C.2 machinery, kernel-validated
earlier); stiffness = analytical screening (beam/plate formulas, NOT FEA); masses, tolerances, part and
insert counts, assembly time = working assumptions (inferred). Nothing here is physically tested.
"""

import argparse
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import c2_screening as c2  # noqa: E402
import hinge_feasibility_2d as hm  # noqa: E402
import lid_stackup_study as ld  # noqa: E402
import solar_skeleton_model as sk  # noqa: E402
import solar_v1_feasibility as sv  # noqa: E402

V = hm.V
D, H, W, G = ld.D, ld.H, ld.W, ld.G
MIN_GAP, WALL = ld.MIN_GAP, ld.WALL
VFIX = ld.VFIX
INNER_X = ld.INNER_X
E_PETG, G_PETG, RHO = ld.E_PETG, ld.G_PETG, ld.RHO
GRAV = 9.81

# ---------------------------------------------------------------- study parameters (local, working, NOT in nomad.yaml)
S = {
    "lip": ld.DISPLAY_BEZEL_LIP,            # 1.0 front retention lip (0 = flush, clip-retained)
    "rail_h": ld.SOLAR_RAIL_LAYER_HEIGHT,   # 13 = carriage 8 + floor 2.5 + lips 2.5
    "cassette": ld.SOLAR_CASSETTE_THICKNESS,
    "gap": 2.0,                             # cassette-to-back clearance (Round D pick)
    "mid": ld.MID_PLATE_THICKNESS,          # 2.0 class B rail-module plate
    "skin": ld.SANDWICH_SKIN,               # 1.2 sandwich skins (class A, B shell)
    "web_t": ld.RIB_THICKNESS,              # 2.0 sandwich webs / ribs
    "web_s": ld.RIB_SPACING,                # 30 web / rib spacing
    "rib_skin": ld.STRUCTURAL_SKIN_THICKNESS,   # 2.5 ribbed-shell skin (class C)
    "rib_h": None,                          # class C rib height; None = minimum meeting the criterion
    "reinf": "none",
    "h": ld.HINGE_AXIS_HEIGHT,              # 0 working (TBD)
    "T": None,                              # None = derive from layers
}

CASSETTE_MASS = ld.CASSETTE_MASS            # 0.30 kg each, placeholder
PLACEHOLDER_KG = {"display": 0.20, "controller": 0.04, "hinge hardware (2)": 0.05, "cables/loops": 0.03}
SHOCK = ld.SHOCK
ARM = 149.5                                  # pad inboard edge -> stowed carriage centre (B.2 / coupon A)

# Rail reinforcement (coupon A2 envelope): side walls 4.1 with a 2.3 x 10.4 slot each; strips slid in.
A2_WALL, SLOT_W, SLOT_H = 4.1, 2.3, 10.4
STRIP_LEN = 194.0
STRIPS = {"al": (69000.0, 2.0, 10.0, 2.70e-3), "steel": (200000.0, 1.5, 10.0, 7.85e-3)}   # E, t, h, density
REINF = {
    "none": dict(walls=(WALL, WALL), strips=()),
    "al2": dict(walls=(A2_WALL, A2_WALL), strips=("al", "al")),
    "steel2": dict(walls=(A2_WALL, A2_WALL), strips=("steel", "steel")),
    "al1": dict(walls=(WALL, A2_WALL), strips=("al",)),          # one strip, outboard (loop-side) wall only
    "steel1": dict(walls=(WALL, A2_WALL), strips=("steel",)),
}

# Display-gap tolerance allowances (inferred typical values; not measured)
TOL_FRAME = {"display module thickness": 0.20, "display seat / lip + retention foam": 0.15,
             "front-frame pad height (printed)": 0.15, "rail underside straightness over 198 (printed)": 0.20}
TOL_MODULE = {"display module thickness": 0.20, "display seat / lip + retention foam": 0.15,
              "frame ledge height (printed)": 0.15, "mid-plate flatness, 296 x 230 x 2 printed, screwed at edges": 0.40}
TOL_BACK = {"cassette thickness (panel + frame)": 0.30, "rail/carriage height stack": 0.15,
            "shell seat (printed)": 0.15, "shell inner-face flatness": 0.30}

M3_SCREW_G, M3_INSERT_G = 0.8, 0.5         # inferred
PULL_OUT_N = (300.0, 800.0)                  # typical M3 heat-set pull-out range in PETG (inferred, print-dependent)
BASE_MASS_RANGE = (1.2, 1.8)                 # kg, base placeholder range (no base mass model exists)
BASE_CG_FRAC = (0.40, 0.50)                  # base CG from the front as a fraction of depth (inferred; C.1 electronics 0.30-0.52)
HOLD_MARGIN = 1.25                           # friction torque / worst gravity torque (inferred)
HOLD_FROM = 30.0                             # friction hinge must hold the lid from this angle up (inferred)


def rss(d):
    return math.sqrt(sum(v * v for v in d.values()))


# ---------------------------------------------------------------- sections
def section_ei(pieces):
    """pieces: (b, t, zc, E); b < 0 removes material. Returns EI, EA, z-bar."""
    ea = sum(e * b * t for b, t, _, e in pieces)
    zb = sum(e * b * t * z for b, t, z, e in pieces) / ea
    ei = sum(e * (b * t ** 3 / 12 + b * t * (z - zb) ** 2) for b, t, z, e in pieces)
    return ei, ea, zb


def rail_pieces(reinf="none", rail_h=None, z0=0.0, metal=True):
    """Rail C-channel (floor toward the display) + optional strips. Floor/lip thickness grows with rail_h."""
    r = REINF[reinf]
    rail_h = rail_h or S["rail_h"]
    ch = VFIX["ch"]
    fl = (rail_h - ch) / 2                                  # floor = lip thickness (2.5 at 13)
    wa, wb = r["walls"]
    w = VFIX["cw"] + wa + wb
    slot = VFIX["slot_w"]
    lip_a, lip_b = wa + (VFIX["cw"] - slot) / 2, wb + (VFIX["cw"] - slot) / 2
    p = [(w, fl, z0 + fl / 2, E_PETG), (wa, ch, z0 + fl + ch / 2, E_PETG), (wb, ch, z0 + fl + ch / 2, E_PETG),
         (lip_a, fl, z0 + rail_h - fl / 2, E_PETG), (lip_b, fl, z0 + rail_h - fl / 2, E_PETG)]
    zs = z0 + rail_h / 2
    for s in r["strips"]:
        p.append((-SLOT_W, SLOT_H, zs, E_PETG))              # printed slot void
        if metal:
            e, t, h, _ = STRIPS[s]
            p.append((t, h, zs, e))
    return p, w


def rail_ei(reinf="none", composite=True, rail_h=None):
    p, _ = rail_pieces(reinf, rail_h)
    if composite or not REINF[reinf]["strips"]:
        return section_ei(p)[0]
    printed = [q for q in p if q[3] == E_PETG]
    ei = section_ei(printed)[0]
    for s in REINF[reinf]["strips"]:
        e, t, h, _ = STRIPS[s]
        ei += e * t * h ** 3 / 12
    return ei


def rail_mass(reinf="none", rail_h=None):
    p, w = rail_pieces(reinf, rail_h, metal=False)
    area = sum(b * t for b, t, _, _ in p)
    g = area * (VFIX["S"] + sk.L) * RHO
    metal = sum(STRIPS[s][1] * STRIPS[s][2] * STRIP_LEN * STRIPS[s][3] for s in REINF[reinf]["strips"])
    return g, metal, w


def rail_cantilever(reinf="none", rail_h=None, composite=True):
    ei = rail_ei(reinf, composite, rail_h)
    p = CASSETTE_MASS * GRAV
    d1 = p * ARM ** 3 / (3 * ei)
    return d1, d1 * SHOCK


def rail_on_plate(reinf="none", mid=None, integral=True, span="ss296"):
    """Class B: rail on the mid-plate. integral = rail printed with the plate (composite)."""
    mid = S["mid"] if mid is None else mid
    rp, w = rail_pieces(reinf, z0=mid)
    b = w + 20.0
    plate = [(b, mid, mid / 2, E_PETG)]
    if integral:
        ei = section_ei(rp + plate)[0]
    else:
        ei = rail_ei(reinf, True) + E_PETG * b * mid ** 3 / 12
    p = CASSETTE_MASS * GRAV * SHOCK
    xc = sk.XI - VFIX["link"] - sk.L / 2
    if span == "ss296":
        L = INNER_X
        a, bb = xc + L / 2, L / 2 - xc
        d3 = p * a * a * bb * bb / (3 * ei * L)
    else:                                            # fixed-fixed between the frame lands (unconservative bound)
        L = 2 * (sk.DISP_W / 2 + MIN_GAP)
        a, bb = xc + L / 2, L / 2 - xc
        d3 = p * a ** 3 * bb ** 3 / (3 * ei * L ** 3)
    return d3 / SHOCK, d3


def pad_screw_tension(shock=SHOCK):
    """Rail ear on the pad: pivot at the pad inboard edge, screws at 7 and 21.5 mm (coupon A)."""
    m = CASSETTE_MASS * GRAV * shock * ARM
    k = m / (7.0 ** 2 + 21.5 ** 2)
    return m / 1000, 21.5 * k


# ---------------------------------------------------------------- back structures (one-way strip over the 202 bay)
def i_two_skins(t_out, t_in, core, web_t, web_s):
    """Per-mm I of an asymmetric sandwich: outer skin, core webs, inner skin (z from the outer face)."""
    pcs = [(1.0, t_out, t_out / 2), (web_t / web_s, core, t_out + core / 2), (1.0, t_in, t_out + core + t_in / 2)]
    a = sum(b * t for b, t, _ in pcs)
    zb = sum(b * t * z for b, t, z in pcs) / a
    return sum(b * t ** 3 / 12 + b * t * (z - zb) ** 2 for b, t, z in pcs)


def back_sandwich(depth, skin=None, web_t=None, web_s=None, inner_eff=None, core_g=None, composite=True):
    """LC1/LC2 deflection of a sandwich of total depth. inner_eff = effective bridged skin;
    core_g = slicer-infill core shear modulus as a fraction of G_PETG (replaces the explicit webs)."""
    skin = skin or S["skin"]
    web_t = web_t or S["web_t"]
    web_s = web_s or S["web_s"]
    core = depth - 2 * skin
    if core <= 0:
        return None
    t_in = skin if inner_eff is None else inner_eff
    if composite:
        iw = i_two_skins(skin, t_in, core, web_t, web_s)
    else:
        iw = ld.i_ribbed(skin, core, web_t, web_s) + t_in ** 3 / 12
    if core_g is not None:
        iw = i_two_skins(skin, t_in, core, 0.0, 1.0)
        as_w = core_g * core
    else:
        as_w = ld.shear_area(core, web_t, web_s)
    return ld.deflect(iw, as_w), core


def back_ribbed(depth, skin=None, rib_t=None, rib_s=None):
    skin = skin or S["rib_skin"]
    rib_t = rib_t or S["web_t"]
    rib_s = rib_s or S["web_s"]
    h = depth - skin
    if h < 0:
        return None
    return ld.deflect(ld.i_ribbed(skin, h, rib_t, rib_s), ld.shear_area(h, rib_t, rib_s) if h > 0 else None), h


def min_depth(fn, allow, lo=1.0, hi=30.0, step=0.1, **kw):
    d = lo
    while d <= hi + 1e-9:
        r = fn(d, **kw)
        if r and max(r[0]) <= allow:
            return round(d, 2), r
        d += step
    return None, None


# ---------------------------------------------------------------- class definitions
def stack(lip, mid, rail_h, cassette):
    return lip + ld.DISPLAY_THICKNESS + MIN_GAP + mid + rail_h + MIN_GAP + cassette


def classes(p=None):
    p = {**S, **(p or {})}
    allow = p["gap"] / 2
    out = {}
    base = stack(p["lip"], 0.0, p["rail_h"], p["cassette"])
    baseB = stack(p["lip"], p["mid"], p["rail_h"], p["cassette"])
    for key, label, st, kind, mid in (("A", "A sandwich (~37-38)", base, "sandwich", 0.0),
                                      ("B", "B modular (~39-40)", baseB, "sandwich", p["mid"]),
                                      ("C", "C ribbed fallback (~42)", base, "ribbed", 0.0)):
        if p["T"] is not None:
            depth = p["T"] - st - p["gap"]
            r = back_sandwich(depth, p["skin"]) if kind == "sandwich" else back_ribbed(depth)
        elif kind == "sandwich":
            depth, r = min_depth(back_sandwich, allow, lo=2 * p["skin"] + 0.5, skin=p["skin"])
        else:
            if p["rib_h"] is not None:
                depth = p["rib_skin"] + p["rib_h"]
                r = back_ribbed(depth)
            else:
                depth, r = min_depth(back_ribbed, allow, lo=p["rib_skin"], step=0.5)
        T = st + p["gap"] + depth
        out[key] = dict(key=key, label=label, kind=kind, mid=mid, stack=st, depth=depth, T=round(T, 2),
                        defl=r[0] if r else (math.inf, math.inf), core=r[1] if r else None,
                        frame_h=st + p["gap"], dz=p["lip"] + mid, allow=allow)
    return out


# ---------------------------------------------------------------- hinge / ports (C.2 geometry, variable plug)
def port_sweep(T, h, plug=c2.PLUG, step=0.5, stop=180.0):
    axis = (D - c2.INSET, H + h)
    zone = hm.rect(D, D + plug, c2.PZ0, c2.PZ1) if plug else None
    lid0 = hm.rect(0, D, H + G, H + G + T)
    pmin, bmin, gmin = math.inf, math.inf, math.inf
    max_ok, at, failed = None, {}, False
    a = 0.0
    while a <= stop + 1e-9:
        lid = hm.rotate(lid0, axis, a)
        if zone:
            pmin = min(pmin, hm.signed_clearance(lid, zone))
        bmin = min(bmin, hm.signed_clearance(lid, c2.BASE))
        gmin = min(gmin, min(z for _, z in lid))
        ok = (pmin >= MIN_GAP - 1e-9 or not zone) and bmin >= MIN_GAP - 1e-9 and gmin >= -1e-9
        failed = failed or not ok
        if not failed:
            max_ok = a
        for ang in (105.0, 120.0, 135.0):
            if abs(a - ang) < 1e-9:
                at[ang] = pmin
        a += step
    return max_ok, at, bmin


def min_h_for(T, ang, plug=c2.PLUG):
    h = 0.0
    while h <= 20.0:
        mo, _, _ = port_sweep(T, h, plug, stop=ang + 1)
        if mo is not None and mo >= ang:
            return h
        h += 0.5
    return None


# ---------------------------------------------------------------- mass / CG / handling
def frame_mass(frame_h, band_h, kind_mid):
    """Front frame (solid PETG estimate): face ring, lip, perimeter walls, edge bands, pads/lands, hinge corners."""
    ring = ((INNER_X * (D - 2 * WALL)) - sk.DISP_W * sk.DISP_H) * WALL
    lip = (sk.DISP_W * sk.DISP_H - V["DISPLAY_ACTIVE_WIDTH"] * V["DISPLAY_ACTIVE_HEIGHT"]) * S["lip"]
    walls = 2 * W * WALL * frame_h + 2 * WALL * ((D - 2 * WALL) * frame_h - ld.SPAN * (S["cassette"] + 2 * MIN_GAP) - 19.0 * 12.5)
    bands = 2 * INNER_X * (VFIX["cy0"] - MIN_GAP - WALL) * band_h
    pads = 2 * 28.5 * VFIX["rail_w"] * 3.5 if not kind_mid else 2 * 29.5 * sk.DISP_H * 4.5 * 0.5
    corners = 2 * V["HINGE_MOUNT_WIDTH"] * 14.0 * max(frame_h - band_h, 0) * 0.6
    parts = {"face ring": ring, "display lip": lip, "perimeter walls": walls, "edge bands": bands,
             "rail pads / module lands": pads, "hinge corner blocks": corners}
    return {k: v * RHO for k, v in parts.items()}


def shell_mass(c):
    if c["kind"] == "sandwich":
        return ld.mass_rear("sandwich", c["core"])
    return ld.mass_rear("ribbed", c["depth"] - S["rib_skin"])


def lid_mass(c, reinf="none"):
    band_h = MIN_GAP + S["cassette"] + S["gap"]
    fr = frame_mass(c["frame_h"], band_h, c["mid"] > 0)
    rp, rm, _ = rail_mass(reinf)
    n_ins = PLAN[c["key"]]["inserts_total"]
    struct = {"front frame": sum(fr.values()), "rails (2, printed)": 2 * rp,
              "rear shell": shell_mass(c)}
    if c["mid"]:
        struct["mid-plate"] = INNER_X * (D - 2 * WALL) * c["mid"] * RHO
    other = {"reinforcement strips": 2 * rm, "screws + inserts": n_ins * (M3_SCREW_G + M3_INSERT_G)}
    ph = {**{k: v * 1000 for k, v in PLACEHOLDER_KG.items()}, "cassettes (2)": 2 * CASSETTE_MASS * 1000}
    return struct, other, ph, fr


def lid_cg(c, struct, other, ph):
    """Mass-weighted CG in the closed lid frame: Y from the free edge, z from the display face."""
    dz = c["dz"]
    z_cass = VFIX["cz0"] + dz + S["cassette"] / 2
    items = [
        (struct["front frame"], D / 2, c["frame_h"] * 0.45),
        (struct["rails (2, printed)"] + other["reinforcement strips"], VFIX["rc"][1] / 2 + VFIX["rc"][-1] / 2, VFIX["rz0"] + dz + S["rail_h"] / 2),
        (struct["rear shell"], D / 2, c["T"] - c["depth"] / 2),
        (struct.get("mid-plate", 0.0), D / 2, S["lip"] + ld.DISPLAY_THICKNESS + MIN_GAP + c["mid"] / 2),
        (other["screws + inserts"], D / 2, c["frame_h"]),
        (ph["display"], D / 2, S["lip"] + ld.DISPLAY_THICKNESS / 2),
        (ph["controller"], 215.0, 10.0),
        (ph["hinge hardware (2)"], 228.0, c["frame_h"] / 2),
        (ph["cables/loops"], 170.0, VFIX["rz0"] + dz + 6.5),
        (ph["cassettes (2)"], D / 2, z_cass),
    ]
    m = sum(i[0] for i in items)
    return m / 1000, sum(i[0] * i[1] for i in items) / m, sum(i[0] * i[2] for i in items) / m


def gravity_arm(yc, zc, h, ang):
    """Horizontal CG offset (mm) from the hinge axis at opening angle ang; + = in front of the axis."""
    axis = (D - c2.INSET, H + h)
    (y, _), = hm.rotate([(yc, H + G + zc)], axis, ang)
    return axis[0] - y, y


def handling(c, m, yc, zc, h):
    arms = {a: gravity_arm(yc, zc, h, a) for a in range(0, 136, 5)}
    hold = max(abs(arms[a][0]) for a in arms if a >= HOLD_FROM) * m * GRAV / 1000     # N*m total
    m105 = abs(arms[105][0]) * m * GRAV / 1000
    friction = HOLD_MARGIN * hold
    per_hinge = friction / 2
    r_edge = D                                         # free-edge lever ~ lid depth from the rear-edge axis
    f_open = (friction + abs(arms[10][0]) * m * GRAV / 1000) / (r_edge / 1000)
    f_close = max(friction - abs(arms[10][0]) * m * GRAV / 1000, 0) / (r_edge / 1000)
    tip = {}
    for ang in (105, 120, 135):
        behind = max(arms[ang][1] - D, 0.0)            # CG behind the base rear-bottom edge
        need = {f: m * behind / (D - f * D) for f in BASE_CG_FRAC}
        tip[ang] = (behind, need)
    one_hand = {f: friction / (GRAV * (D - f * D) / 1000) for f in BASE_CG_FRAC}
    return dict(hold=hold, m105=m105, friction=friction, per_hinge=per_hinge, f_open=f_open, f_close=f_close,
                tip=tip, one_hand=one_hand)


def hinge_screws(per_hinge_3g, frame_h):
    arm_y = 12.0
    arm_z = frame_h - 2 * 6.0
    return {"Y-pattern (arm 12, in the 16.5 band)": per_hinge_3g / (arm_y / 1000),
            f"Z-pattern (arm {arm_z:.0f}, on the rear end face)": per_hinge_3g / (arm_z / 1000)}


# ---------------------------------------------------------------- manufacturing / service plan (inferred counts)
PLAN = {
    "A": dict(
        parts=[("front frame (bezel, walls, side slots, edge bands, pads, hinge corners)", "301 x 235 x {fh}", "face down; supports or 45-deg gussets under the two edge bands"),
               ("rear shell, sandwich 1.2 / core / 1.2 (monolithic)", "301 x 235 x {bd}", "outer skin down; inner skin bridges {br} mm between webs"),
               ("rails x2", "198 x {rw} x 13", "floor down; lip overhang 2.5; no support"),
               ("solar: carriages x2, hub brackets x2, cassette frames x2", "<= 200 x 147.5", "common to all classes")],
        small=["display clips x4", "controller bracket", "cable clamps x4", "end-stop releases x2"],
        inserts={"rear-shell joint (edge bands)": 10, "rail pads (2 per rail)": 4, "hinges (4 per hinge)": 8,
                 "display clips": 4, "controller": 4, "cable / loop anchors": 4},
        service={"cassette": "deploy, release end stop, unplug lead, slide out (no lid screws)",
                 "cables / loops": "rear shell (10 screws) + both cassettes out",
                 "controller": "rear shell (10) + cassettes out + 4 screws",
                 "rail": "rear shell (10) + cassettes out + 2 pad screws; carriage comes out with the rail",
                 "display (rear retention)": "rear shell (10) + cassettes + both rails (4) + loops + controller cable + 4 clips",
                 "hinge": "rear shell (10) + 4 screws per hinge (if the hinge screws sit under the shell)"}),
    "B": dict(
        parts=[("front frame (bezel, walls, side slots, edge bands, module lands, hinge corners)", "301 x 235 x {fh}", "face down; supports or gussets under the edge bands"),
               ("rail module: mid-plate + 2 rails (integral) + controller/loop mounts", "296 x 230 x {mh}", "plate down, rails up; no support"),
               ("rear service shell, sandwich", "301 x 235 x {bd}", "outer skin down; bridged inner skin as A"),
               ("solar: carriages x2, hub brackets x2, cassette frames x2", "<= 200 x 147.5", "common to all classes")],
        small=["display clips x4", "controller bracket", "cable clamps x4", "end-stop releases x2"],
        inserts={"rear-shell joint (edge bands)": 10, "module to frame lands": 8, "hinges (4 per hinge)": 8,
                 "display clips": 4, "controller (on module)": 4, "cable / loop anchors (on module)": 4},
        service={"cassette": "as A",
                 "cables / loops": "rear shell (10) + cassettes out; or module out and route on the bench",
                 "controller": "rear shell (10) + cassettes out + 4 screws (on the module)",
                 "rail": "rear shell (10) + cassettes + module (8); integral rails = reprint the module, screwed variant = 2-4 screws",
                 "display (rear retention)": "rear shell (10) + cassettes + module out as ONE unit (8) + 4 clips",
                 "hinge": "as A"}),
    "C": dict(
        parts=[("front frame (as A)", "301 x 235 x {fh}", "face down; supports or gussets under the edge bands"),
               ("rear shell, 2.5 skin + external ribs", "301 x 235 x {bd}", "skin down, ribs up; no support, no bridging"),
               ("rails x2", "198 x {rw} x 13", "as A"),
               ("solar: carriages x2, hub brackets x2, cassette frames x2", "<= 200 x 147.5", "common to all classes")],
        small=["display clips x4", "controller bracket", "cable clamps x4", "end-stop releases x2"],
        inserts={"rear-shell joint (edge bands)": 10, "rail pads (2 per rail)": 4, "hinges (4 per hinge)": 8,
                 "display clips": 4, "controller": 4, "cable / loop anchors": 4},
        service={k: "as A" for k in ("cassette", "cables / loops", "controller", "rail", "display (rear retention)", "hinge")}),
}
for _k, _p in PLAN.items():
    _p["inserts_total"] = sum(_p["inserts"].values())


def assembly_minutes(key):
    p = PLAN[key]
    n_ins = p["inserts_total"]
    large = len(p["parts"]) + (2 if key != "B" else 0)          # rails counted separately for A/C
    small = len(p["small"]) + 6
    return n_ins * 1.0 + n_ins * 0.5 + large * 5 + small * 1 + 20


# ---------------------------------------------------------------- solar re-validation of the re-spaced rails (strips x2)
def solar_cfg(reinf="none"):
    c = dict(sv.config(fix=True))
    wa, wb = REINF[reinf]["walls"]
    if wa == wb and wa != WALL:
        c["rail_w"] = c["cw"] + 2 * wa
        rz = c["rz0"] + c["rail_h"] / 2
        c["rc"] = {s: D / 2 + s * (c["rail_w"] / 2 + c["corridor"] / 2) for s in (1, -1)}
        c["hub"] = {s: (c["rc"][s] - s * c["coff"], rz) for s in (1, -1)}
    return c


def solar_recheck(c):
    viol = {}
    for lid in sk.LID_ANGLES:
        for eR in (0, 0.5, 1):
            for eL in (0, 0.5, 1):
                v, _, _ = sv.check(sv.to_world(sv.all_parts(c, eR, eL, 0), lid))
                for p, cl in v:
                    viol[p] = min(viol.get(p, 9e9), cl)
        for t in sv.TILTS_REPORT:
            v, _, _ = sv.check(sv.to_world(sv.all_parts(c, 1, 1, t), lid))
            for p, cl in v:
                viol[p] = min(viol.get(p, 9e9), cl)
    route, _ = sv.routing(c)
    lp = sv.loops(c)
    band = (D - WALL) - (max(y for y, _ in lp["LR"][2]) + MIN_GAP)
    front = (min(y for y, _ in lp["LL"][2]) - MIN_GAP) - WALL
    return viol, route, band, front


def clip_windows(c):
    """Display-border stretches with no rail-layer keep-out above them (rear retention clip sites).

    Border = display outline minus the active area. Keep-outs: both rails, both service loops (B.1 V1 + fixes,
    or the re-spaced variant `c`). Returns {edge: [(a, b), ...]} free intervals (+ MIN_GAP margin), mm."""
    dy0 = D / 2 - V["DISPLAY_VERTICAL_OFFSET"] - sk.DISP_H / 2
    bx = (sk.DISP_W - V["DISPLAY_ACTIVE_WIDTH"]) / 2
    by = (sk.DISP_H - V["DISPLAY_ACTIVE_HEIGHT"]) / 2
    keep = []
    for s in (1, -1):
        x0, x1, p = sv.solar_side(c, s, 0, 0)["R" + ("R" if s > 0 else "L")]
        keep.append((x0, x1, min(y for y, _ in p), max(y for y, _ in p)))
    for k, (x0, x1, p) in sv.loops(c).items():
        keep.append((x0, x1, min(y for y, _ in p), max(y for y, _ in p)))
    edges = {"short edge +X": ("y", sk.DISP_W / 2 - bx, sk.DISP_W / 2, dy0, dy0 + sk.DISP_H),
             "short edge -X": ("y", -sk.DISP_W / 2, -sk.DISP_W / 2 + bx, dy0, dy0 + sk.DISP_H),
             "long edge, free-edge side": ("x", dy0, dy0 + by, -sk.DISP_W / 2, sk.DISP_W / 2),
             "long edge, hinge side": ("x", dy0 + sk.DISP_H - by, dy0 + sk.DISP_H, -sk.DISP_W / 2, sk.DISP_W / 2)}
    out = {}
    for name, (axis, f0, f1, a0, a1) in edges.items():
        blocked = []
        for x0, x1, y0, y1 in keep:
            if axis == "y" and x1 > f0 and x0 < f1:
                blocked.append((y0 - MIN_GAP, y1 + MIN_GAP))
            if axis == "x" and y1 > f0 and y0 < f1:
                blocked.append((x0 - MIN_GAP, x1 + MIN_GAP))
        free, cur = [], a0
        for b0, b1 in sorted(blocked):
            if b0 > cur:
                free.append((cur, min(b0, a1)))
            cur = max(cur, b1)
        if cur < a1:
            free.append((cur, a1))
        out[name] = [(round(a, 1), round(b, 1)) for a, b in free if b - a > 1]
    return out


def controller_band(reinf, c):
    """Hinge-end controller band: depth (Y) and height (Z) per class, per side of the centre pass."""
    wa, wb = REINF[reinf]["walls"]
    grow = (wb - WALL) + ((wa - WALL) if wa == wb else 0.0)
    depth = 35.4 - grow
    height = VFIX["cz0"] + c["dz"] - MIN_GAP - WALL
    width = c2.ENV["IX"] - V["HINGE_MOUNT_WIDTH"] - c2.ENV["CW2"] - MIN_GAP
    return depth, height, width


# ---------------------------------------------------------------- report
def fmt(x, n=2):
    return "-" if x is None else f"{x:.{n}f}"


def main(args):
    for k in ("T", "skin", "rib_h", "rail_h", "cassette", "h", "lip", "gap"):
        v = getattr(args, k)
        if v is not None:
            S[k] = v
    if args.rib_s is not None:
        S["web_s"] = args.rib_s
    if args.reinf:
        S["reinf"] = args.reinf
    reinf = S["reinf"]
    print(f"study values: {', '.join(f'{k} {v}' for k, v in S.items())}")
    cl = classes()

    print("\n== 1. class stacks (lid face -> back; working values) ==")
    for c in cl.values():
        print(f"  {c['label']}: stack to cassette top {c['stack']:g} + cassette-back gap {S['gap']:g} + back {c['depth']:g} "
              f"({'core ' + fmt(c['core'], 1) if c['kind'] == 'sandwich' else 'ribs ' + fmt(c['core'], 1)}) = T {c['T']:.1f}; "
              f"closed NOMAD {H + G + c['T']:.1f}; frame height (face -> shell seat) {c['frame_h']:g}; solar shift dz {c['dz']:g}")

    print("\n== 2. back structure (LC1 20 N on b_eff 101 / LC2 1 kPa, span 202; criterion <= gap/2) ==")
    for c in cl.values():
        print(f"  {c['key']}: LC1 {c['defl'][0]:.2f} / LC2 {c['defl'][1]:.2f} vs {c['allow']:.2f}")
    print("  A/B sandwich manufacturing variants at the class depth (LC1 / LC2, mm):")
    dA = cl["A"]["depth"]
    rows = [("nominal (skins 1.2, webs 2 @ 30, composite)", {}),
            ("bridged inner skin effective 0.8 (first 2 layers lost)", {"inner_eff": 0.8}),
            ("bridged inner skin effective 0.6", {"inner_eff": 0.6}),
            ("webs @ 20 (bridge 18)", {"web_s": 20.0}),
            ("two-piece, inner skin NOT bonded (non-composite)", {"composite": False}),
            ("slicer-infill core, G_core = 10% G_PETG", {"core_g": 0.10}),
            ("slicer-infill core, G_core = 5%", {"core_g": 0.05}),
            ("slicer-infill core, G_core = 2%", {"core_g": 0.02})]
    for name, kw in rows:
        r = back_sandwich(dA, **kw)
        dmin, _ = min_depth(back_sandwich, cl["A"]["allow"], lo=2.9, **kw)
        tn = None if dmin is None else cl["A"]["stack"] + S["gap"] + dmin
        print(f"    {name:<58} depth {dA:g}: {r[0][0]:6.2f} / {r[0][1]:5.2f}  | depth to meet: {fmt(dmin, 1)} -> T {fmt(tn, 1)}")
    print("  web-skin interface shear at LC1 (nominal): "
          + interface_shear(dA))
    print("  sandwich skin x web spacing: min T meeting the criterion (lip, gap as set):")
    for sk_ in (1.0, 1.2, 1.6):
        vals = []
        for ws in (15.0, 20.0, 30.0):
            dmin, r = min_depth(back_sandwich, cl["A"]["allow"], lo=2 * sk_ + 0.5, skin=sk_, web_s=ws)
            m = (W * D * 2 * sk_ + (int(INNER_X / ws) + 1) * S["web_t"] * D * (dmin - 2 * sk_) + 2 * WALL * D * (dmin - 2 * sk_)) * RHO
            vals.append(f"@{ws:g}: T {cl['A']['stack'] + S['gap'] + dmin:.1f} ({m:.0f} g, bridge {ws - S['web_t']:g})")
        print(f"    skin {sk_:g}: " + "; ".join(vals))
    t_pl = 6.0
    while max(ld.deflect(t_pl ** 3 / 12)) > cl["A"]["allow"]:
        t_pl += 0.05
    t_al = t_pl * (E_PETG / 69000.0) ** (1 / 3)
    print(f"  plain PETG back meeting the criterion: {t_pl:.2f} mm -> T {cl['A']['stack'] + S['gap'] + t_pl:.1f} ({W * D * t_pl * RHO:.0f} g). "
          f"Reference only, OUTSIDE the three D.1 classes: an equal-stiffness plain aluminium sheet would be {t_al:.2f} mm -> "
          f"T {cl['A']['stack'] + S['gap'] + t_al:.1f} ({W * D * t_al * 2.70e-3:.0f} g); not analyzed further")
    print("  ribbed (class C) rib height x spacing: LC1 mm (2.5 skin) and min T:")
    for rs in (20.0, 25.0, 30.0, 40.0):
        vals = [f"h{h}:{back_ribbed(S['rib_skin'] + h, rib_s=rs)[0][0]:.2f}" for h in (6, 7, 8, 9, 10, 12)]
        dmin, _ = min_depth(back_ribbed, cl["C"]["allow"], lo=S["rib_skin"], step=0.5, rib_s=rs)
        m = ld.mass_rear("ribbed", dmin - S["rib_skin"]) if rs == 30 else (W * D * S["rib_skin"] + (int(INNER_X / rs) + 1) * S["web_t"] * D * (dmin - S["rib_skin"])) * RHO
        print(f"    spacing {rs:g}: " + "  ".join(vals) + f"  | min T {cl['C']['stack'] + S['gap'] + dmin:.1f} ({m:.0f} g)")

    print("\n== 3. rail: printed vs printed + replaceable metal strips (stowed 0.3 kg cassette) ==")
    tolF, tolM = rss(TOL_FRAME), rss(TOL_MODULE)
    print(f"  display-gap tolerance (inferred): frame-mounted rails RSS {tolF:.2f} / worst {sum(TOL_FRAME.values()):.2f}; "
          f"module (mid-plate) RSS {tolM:.2f} / worst {sum(TOL_MODULE.values()):.2f}")
    print("  criteria: static 1 g <= gap/2 (0.5); 3 g + tolerance RSS <= gap (1.0, no display contact)")
    for rv in ("none", "al2", "steel2", "al1", "steel1"):
        g, metal, w = rail_mass(rv)
        d1, d3 = rail_cantilever(rv)
        _, d3n = rail_cantilever(rv, composite=False)
        b1, b3 = rail_on_plate(rv, integral=True)
        _, b3n = rail_on_plate(rv, integral=False)
        _, b3f = rail_on_plate(rv, integral=True, span="ff")
        okA = d1 <= 0.5 and d3 + tolF <= 1.0
        okB = b1 <= 0.5 and b3 + tolM <= 1.0
        print(f"  {rv:<7} rail width {w:4.1f}, EI {rail_ei(rv) / 1e6:5.1f}e6 N*mm2, mass {g:4.1f} g printed + {metal:4.1f} g metal per rail")
        print(f"          A/C cantilever: {d1:.2f} static / {d3:.2f} at 3 g (loose strips {d3n:.2f}) -> 3 g + tol {d3 + tolF:.2f} "
              f"[{'meets' if okA else 'FAILS'}]")
        print(f"          B on plate: integral {b1:.2f} / {b3:.2f} at 3 g (screwed {b3n:.2f}; fixed-fixed bound {b3f:.2f}) -> 3 g + tol "
              f"{b3 + tolM:.2f} [{'meets' if okB else 'FAILS'}]")
    mp, tp = pad_screw_tension()
    print(f"  pad moment (A/C) at 3 g {mp:.2f} N*m -> far pad screw tension {tp:.0f} N (pull-out range {PULL_OUT_N[0]:.0f}-{PULL_OUT_N[1]:.0f}, inferred)")
    print("  printed rail alone - what it would take in A/C (thickness cost):")
    for fl in (2.5, 3.0, 3.5, 4.0, 4.5, 5.0):
        rh = VFIX["ch"] + 2 * fl
        d1, d3 = rail_cantilever("none", rail_h=rh)
        print(f"    floor = lip {fl:g} -> rail {rh:g} (T +{rh - 13:g}): {d1:.2f} / {d3:.2f} at 3 g; 3 g + tol {d3 + tolF:.2f}")
    d1, d3 = rail_cantilever("none")
    need_gap = max(2 * d1, d3 + tolF)
    print(f"    or open the display gap to {need_gap:.2f} (T +{need_gap - MIN_GAP:.2f}) keeping the 13 mm rail")

    print("\n== 4. hinge / rear ports (C.2 geometry: rear-edge axis, gap 2, port zone Z 4-19; plug length varied) ==")
    Ts = sorted({c["T"] for c in cl.values()} | {c["T"] - S["lip"] for c in cl.values()} | {35.0})
    print("  T     | max opening at h 0 / 1 / 2 / 3 / 4 (45 mm plug)   | min h for 135 (plug 45 / 25 / 15 / none) | "
          "port clearance at 105/120/135, h 0")
    for T in Ts:
        mos = []
        for h in (0, 1, 2, 3, 4):
            mo, _, _ = port_sweep(T, h)
            mos.append(fmt(mo, 1))
        need = [fmt(min_h_for(T, 135.0, pl), 1) for pl in (45.0, 25.0, 15.0, 0.0)]
        _, at, _ = port_sweep(T, 0.0)
        print(f"  {T:5.1f} | {' / '.join(mos):<46} | {' / '.join(need):<40} | "
              + " / ".join(f"{at.get(a, math.nan):+.1f}" for a in (105.0, 120.0, 135.0)))
    chk = [(T, port_sweep(T, 0.0)[0], c2.feasibility(T, 0.0)[0]) for T in (31.5, 42.5)]
    print("  cross-check vs c2.feasibility (plug 45, h 0): " + ", ".join(f"T {t}: {a} / {b}" for t, a, b in chk))

    print("\n== 5. display + controller ==")
    for c in cl.values():
        for rv in ("none", "steel2", "steel1"):
            dep, hgt, wid = controller_band(rv, c)
            if c["key"] == "B":
                hgt_plate = S["rail_h"]
                note = f"height {hgt:.1f} with a plate cut-out in the band, {hgt_plate:g} if the controller sits on the plate"
            else:
                note = f"height {hgt:.1f}"
            print(f"  {c['key']} rails {rv:<6}: band {wid:.1f} (X, per side) x {dep:.1f} (Y) x {note}; "
                  f"90-deg exit R+d {ld.DISPLAY_CABLE_BEND_RADIUS + ld.DISPLAY_CABLE_CLEARANCE:g} "
                  f"{'fits' if ld.DISPLAY_CABLE_BEND_RADIUS + ld.DISPLAY_CABLE_CLEARANCE <= dep else 'DOES NOT fit'}; "
                  f"U-turn {2 * ld.DISPLAY_CABLE_BEND_RADIUS + ld.DISPLAY_CABLE_CLEARANCE:g} "
                  f"{'fits' if 2 * ld.DISPLAY_CABLE_BEND_RADIUS + ld.DISPLAY_CABLE_CLEARANCE <= dep else 'does not fit'}")
    dy0 = D / 2 - V["DISPLAY_VERTICAL_OFFSET"] - sk.DISP_H / 2
    print(f"  display outline Y {dy0:g}-{dy0 + sk.DISP_H:g}; hinge-side edge to band start {197.1 - (dy0 + sk.DISP_H):.1f} mm; "
          f"free-edge side has only the {MIN_GAP:g} mm display gap under the rail layer (no FPC route there)")
    for rv in ("none", "steel2"):
        win = clip_windows(solar_cfg(rv))
        print(f"  rear-clip sites on the display border (no rail/loop above), rails {rv}: "
              + "; ".join(f"{k}: " + (", ".join(f"{a:g}..{b:g} ({b - a:.0f})" for a, b in v) or "none") for k, v in win.items()))

    print("\n== 6. solar: stowed gaps, deployed lowest Z, and re-validation of the re-spaced (2-strip) rails ==")
    for c in cl.values():
        vals = []
        for h in (0.0, 2.0, 4.0, 7.0):
            vals.append(f"h{h:g}: " + "/".join(f"{ld.deployed_lowest_z(c['dz'], h, a):.0f}" for a in (105.0, 120.0, 135.0)))
        print(f"  {c['key']} (dz {c['dz']:g}): stowed gaps display-{'plate' if c['mid'] else 'rail'} {MIN_GAP:g}, rail-cassette {MIN_GAP:g}, "
              f"cassette-back {S['gap']:g}; deployed lowest Z (tilt +-75) at 105/120/135 -> " + "; ".join(vals))
    for rv in ("none", "steel2"):
        c = solar_cfg(rv)
        viol, route, band, front = solar_recheck(c)
        print(f"  rails {rv:<6} (rail width {c['rail_w']:g}, rail centres Y {c['rc'][-1]:.1f} / {c['rc'][1]:.1f}, hubs Y "
              f"{c['hub'][-1][0]:.1f} / {c['hub'][1][0]:.1f}): collisions over lid 0/105/135, slides, tilts +-75: "
              f"{viol or 'none'}; cable routes R {route['R']}, L {route['L']}; controller band depth {band:.1f}; front zone {front:.1f}")
    print("  single outboard strip (al1/steel1): carriage, hub, pin, bracket, corridor unchanged; only the loop-side rail wall "
          "(+1.6) and its service loop move (static change; kinematics as B.1)")

    print("\n== 7. mass / CG / hinge / handling (solid-PETG structure; placeholders marked) ==")
    res = {}
    for c in cl.values():
        struct, other, ph, fr = lid_mass(c, reinf)
        m, yc, zc = lid_cg(c, struct, other, ph)
        hd = handling(c, m, yc, zc, S["h"])
        res[c["key"]] = (struct, other, ph, fr, m, yc, zc, hd)
        print(f"  {c['key']}: structure {sum(struct.values()):.0f} g ({', '.join(f'{k} {v:.0f}' for k, v in struct.items())}); "
              f"{', '.join(f'{k} {v:.0f}' for k, v in other.items())}; placeholders {sum(ph.values()):.0f} g "
              f"({', '.join(f'{k} {v:.0f}' for k, v in ph.items())})")
        print(f"     front frame breakdown: {', '.join(f'{k} {v:.0f}' for k, v in fr.items())}")
        print(f"     lid total {m:.2f} kg; CG Y {yc:.1f} from the free edge, z {zc:.1f} from the face; "
              f"gravity torque max (>= {HOLD_FROM:g} deg) {hd['hold']:.2f} N*m, at 105 {hd['m105']:.2f}; friction needed "
              f"{hd['friction']:.2f} total / {hd['per_hinge']:.2f} per hinge; 3 g per hinge {hd['per_hinge'] * SHOCK / HOLD_MARGIN:.2f}")
        print(f"     free-edge force: open ~{hd['f_open']:.1f} N, close ~{hd['f_close']:.1f} N; base mass for one-handed opening "
              f"(CG at {BASE_CG_FRAC[0]:g}/{BASE_CG_FRAC[1]:g} D): {hd['one_hand'][BASE_CG_FRAC[0]]:.2f}/{hd['one_hand'][BASE_CG_FRAC[1]]:.2f} kg")
        print("     tip-back (lid CG behind base rear edge; base mass needed, CG 0.40/0.50 D): "
              + "; ".join(f"{a}: {b:.1f} mm -> {n[BASE_CG_FRAC[0]]:.2f}/{n[BASE_CG_FRAC[1]]:.2f} kg" for a, (b, n) in hd["tip"].items()))
        hs = hinge_screws(hd["per_hinge"] * SHOCK / HOLD_MARGIN, c["frame_h"])
        print("     hinge screw couple at 3 g (force per row): " + "; ".join(f"{k} {v:.0f} N" for k, v in hs.items()))

    print("\n== 8. torsion index (Round D method; conservative index, not a prediction) ==")
    for c in cl.values():
        parts = ld.front_frame_j(c["mid"])
        if c["kind"] == "sandwich":
            parts["rear sandwich (closed)"] = ld.j_closed_box(INNER_X, c["core"] + S["skin"], S["skin"], WALL)
        else:
            parts["rear ribbed (open)"] = ld.j_open_rect(INNER_X, S["rib_skin"]) + 10 * c["core"] * S["web_t"] ** 3 / 3
        j, phi, dc = ld.torsion_index(parts)
        print(f"  {c['key']}: J {j:.0f} mm^4 -> {phi:.1f} deg / {dc:.0f} mm corner at {ld.CORNER_P:g} N")

    print("\n== 9. manufacturing / assembly counts (inferred plan) ==")
    for c in cl.values():
        p = PLAN[c["key"]]
        _, _, rw = rail_mass(reinf)
        dims = {"fh": f"{c['frame_h']:g}", "bd": f"{c['depth']:g}", "rw": f"{rw:g}", "mh": f"{c['mid'] + S['rail_h']:g}"}
        bridge = f"{S['web_s'] - S['web_t']:g}"
        for name, size, how in p["parts"]:
            print(f"  {c['key']}: {name}: {size.format(**dims)}; {how.format(br=bridge)}")
        print(f"  {c['key']}: inserts {p['inserts_total']} ({', '.join(f'{k} {v}' for k, v in p['inserts'].items())}); "
              f"small parts {len(p['small'])}; first assembly ~{assembly_minutes(c['key']):.0f} min (rough)")

    print("\n== 10. thickness sweep (lip, gap as set): back LC1 per class (* = meets delta <= gap/2) ==")
    print("  rail criterion is independent of T: A/C cantilever printed 3 g + tol "
          f"{rail_cantilever('none')[1] + tolF:.2f} (fails), steel2 {rail_cantilever('steel2')[1] + tolF:.2f}; "
          f"B plate printed {rail_on_plate('none')[1] + tolM:.2f} (at the limit), steel2 {rail_on_plate('steel2')[1] + tolM:.2f}")
    print("  T    | A sandwich | B modular  | C ribbed   | min h for 135 (45 plug) | max open h 0 | closed")
    for T in [36.0, 36.5, 37.0, 37.5, 37.6, 38.0, 38.5, 39.0, 39.5, 39.6, 40.0, 40.5, 41.0, 41.5, 42.0, 43.0, 44.0]:
        cc = classes({"T": T})
        row = []
        for k in "ABC":
            d = cc[k]["defl"][0]
            row.append(f"{d:6.2f}{'*' if d <= cc[k]['allow'] else ' '}" if math.isfinite(d) else "   n/a ")
        print(f"  {T:4.1f} | {row[0]:<10} | {row[1]:<10} | {row[2]:<10} | {fmt(min_h_for(T, 135.0), 1):<23} | "
              f"{fmt(port_sweep(T, 0.0)[0], 1):<12} | {H + G + T:.1f}")

    print("\n== 11. normalized comparison (per class; rails printed-only / + 2 steel strips) ==")
    for c in cl.values():
        for rv in ("none", "steel2"):
            struct, other, ph, fr = lid_mass(c, rv)
            m, yc, zc = lid_cg(c, struct, other, ph)
            hd = handling(c, m, yc, zc, S["h"])
            if c["mid"]:
                r1, r3 = rail_on_plate(rv)
                tol = tolM
            else:
                r1, r3 = rail_cantilever(rv)
                tol = tolF
            parts = ld.front_frame_j(c["mid"])
            if c["kind"] == "sandwich":
                parts["rear"] = ld.j_closed_box(INNER_X, c["core"] + S["skin"], S["skin"], WALL)
            else:
                parts["rear"] = ld.j_open_rect(INNER_X, S["rib_skin"]) + 10 * c["core"] * S["web_t"] ** 3 / 3
            j, phi, dc = ld.torsion_index(parts)
            hs = hinge_screws(hd["per_hinge"] * SHOCK / HOLD_MARGIN, c["frame_h"])
            n_large = len(PLAN[c["key"]]["parts"]) - 1 + (1 if c["key"] != "B" else 0)
            print(f"  {c['key']} {rv:<6}: T {c['T']:.1f} | closed {H + G + c['T']:.1f} | lid {m:.2f} kg (structure {sum(struct.values()):.0f} g "
                  f"+ metal {other['reinforcement strips']:.0f} g) | back LC1/LC2 {c['defl'][0]:.2f}/{c['defl'][1]:.2f} | rail {r1:.2f} static, "
                  f"{r3:.2f} 3 g (+tol {r3 + tol:.2f}) | hinge hold {hd['per_hinge']:.2f} N*m/hinge, 3 g {hd['per_hinge'] * SHOCK / HOLD_MARGIN:.2f} | "
                  f"screw row {min(hs.values()):.0f}-{max(hs.values()):.0f} N | torsion {dc:.0f} mm | large printed parts {n_large} "
                  f"| inserts {PLAN[c['key']]['inserts_total']} | assembly ~{assembly_minutes(c['key']):.0f} min")
    print(f"  cassette static load: {CASSETTE_MASS * GRAV:.2f} N each ({CASSETTE_MASS * GRAV * SHOCK:.1f} N at 3 g); display at 3 g "
          f"{PLACEHOLDER_KG['display'] * GRAV * SHOCK:.1f} N on its retention; largest printed part 301 x 235 in every class "
          f"(bed >= ~311 x 245 with a 5 mm skirt margin, inferred)")

    print("\n== 12. sensitivities (T shift per class) ==")
    for rh in (11.0, 13.0, 15.0):
        cc = classes({"rail_h": rh})
        print(f"  rail layer {rh:g}: T A/B/C {cc['A']['T']:.1f} / {cc['B']['T']:.1f} / {cc['C']['T']:.1f}; printed rail 3 g "
              f"{rail_cantilever('none', rail_h=rh)[1]:.2f} (floor/lip {(rh - VFIX['ch']) / 2:g}; carriage 8 unchanged)")
    for ct in (6.0, 8.0, 10.0):
        cc = classes({"cassette": ct})
        print(f"  cassette {ct:g}: T A/B/C {cc['A']['T']:.1f} / {cc['B']['T']:.1f} / {cc['C']['T']:.1f}")
    for lp in (0.0, 1.0, 2.0):
        cc = classes({"lip": lp})
        print(f"  front lip {lp:g}: T A/B/C {cc['A']['T']:.1f} / {cc['B']['T']:.1f} / {cc['C']['T']:.1f}")
    for gp in (1.0, 1.5, 2.0, 3.0):
        cc = classes({"gap": gp})
        print(f"  cassette-back gap {gp:g}: T A/B/C {cc['A']['T']:.1f} / {cc['B']['T']:.1f} / {cc['C']['T']:.1f}")
    print(f"  back-gap tolerance (inferred) RSS {rss(TOL_BACK):.2f} / worst {sum(TOL_BACK.values()):.2f} vs the gap/2 "
          f"({S['gap'] / 2:g}) left after the deflection allowance")


def interface_shear(depth):
    """Shear stress at the web tops (skin-web layer interface) and in the webs for LC1 (nominal sandwich)."""
    skin, t, s = S["skin"], S["web_t"], S["web_s"]
    core = depth - 2 * skin
    iw = i_two_skins(skin, skin, core, t, s)
    v = ld.P1 / 2 / ld.B_EFF                               # N per mm width at the support
    q = v * skin * (core + skin) / 2 / iw                  # shear flow per mm width, N/mm per mm
    tau_if = q * s / t
    tau_web = v * s / (t * core)
    return f"interface ~{tau_if:.2f} MPa, web ~{tau_web:.2f} MPa (PETG interlayer strength ~10+ MPa, inferred) -> stiffness/flatness, not strength, is the bridging question"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--T", type=float)
    ap.add_argument("--skin", type=float)
    ap.add_argument("--rib-h", dest="rib_h", type=float)
    ap.add_argument("--rib-s", dest="rib_s", type=float)
    ap.add_argument("--rail-h", dest="rail_h", type=float)
    ap.add_argument("--cassette", type=float)
    ap.add_argument("--reinf", choices=list(REINF))
    ap.add_argument("--h", type=float)
    ap.add_argument("--lip", type=float)
    ap.add_argument("--gap", type=float)
    main(ap.parse_args())
