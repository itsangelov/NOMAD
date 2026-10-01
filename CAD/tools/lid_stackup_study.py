"""Round D: lid stack-up / structural envelope study (analysis only; nothing is chosen).

Builds the lid from functional layers (display, retention, controller band, solar rail layer, cassette,
back structure), evaluates five lid architectures (A thin, B two-piece ribbed, C sandwich rear shell,
D modular with a rail mid-plate, E cassette-backed), screens stiffness with simple beam/plate formulas
(NOT FEA), and couples every resulting thickness to the D-006 hinge / rear-port map (Round C.2) and to
the validated B.1 V1 + fixes solar geometry.

  py CAD/tools/lid_stackup_study.py

Evidence levels: layer arithmetic and geometry = modeled; stiffness = analytical screening estimate;
masses, controller sizes and material data = working assumptions (inferred). Physical validation is
still required for every structural number (coupons A/B exist for the rail and the back plate).

STUDY PARAMETERS (local to this study, NOT in nomad.yaml, all working): the names requested for Round D.
Existing nomad.yaml parameters are reused where they exist (DISPLAY_THICKNESS, SOLAR_CASSETTE_THICKNESS,
HINGE_AXIS_HEIGHT, LID_CLOSED_GAP, MIN_GAP, WALL_THICKNESS, SOLAR_CARRIAGE_HEIGHT ...).
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import c2_screening as c2  # noqa: E402
import hinge_feasibility_2d as hm  # noqa: E402
import solar_skeleton_model as sk  # noqa: E402
import solar_v1_feasibility as sv  # noqa: E402

V = hm.V
D, H, W = V["BODY_DEPTH"], V["BODY_HEIGHT"], V["BODY_WIDTH"]
G = V["LID_CLOSED_GAP"]                  # working 2.0 (D-006)
MIN_GAP, WALL = V["MIN_GAP"], V["WALL_THICKNESS"]
DISPLAY_THICKNESS = V["DISPLAY_THICKNESS"]            # working 5 (SKU not locked)
SOLAR_CASSETTE_THICKNESS = V["SOLAR_CASSETTE_THICKNESS"]  # working 8
HC = V["SOLAR_CASSETTE_HEIGHT"]
VFIX = sv.config(fix=True)               # B.1 V1 + minimal fixes (validated geometry)

# ---------------------------------------------------------------- study parameters (working, local)
SOLAR_RAIL_LAYER_HEIGHT = V["SOLAR_CARRIAGE_HEIGHT"] + 2 * WALL   # 13: carriage 8 + rail floor/lip walls
DISPLAY_BEZEL_LIP = 1.0                  # front retention lip over the display border (0 = flush, clip-retained)
DISPLAY_CONTROLLER_THICKNESS = 12.0      # configurable envelope (no hardware selected); incl. connectors
DISPLAY_CABLE_CLEARANCE = 6.0            # cable/connector envelope thickness at the controller exit
DISPLAY_CABLE_BEND_RADIUS = 15.0         # working bend-radius envelope for the display cable (not a cable choice)
MID_PLATE_THICKNESS = 2.0                # rail-module mid-plate (architectures D, E)
STRUCTURAL_SKIN_THICKNESS = 2.5          # single skin (A cover uses THIN_COVER instead)
SANDWICH_SKIN = 1.2                      # each skin of the sandwich rear shell (C, D)
THIN_COVER = 1.6                         # architecture A non-structural back cover
RIB_HEIGHT = 8.0                         # default for reporting; sweeps below
RIB_THICKNESS = 2.0
RIB_SPACING = 30.0
HINGE_AXIS_HEIGHT = V["HINGE_AXIS_HEIGHT"]   # working 0 (TBD)

# ---------------------------------------------------------------- screening material / loads (assumptions)
E_PETG, NU = 2000.0, 0.37
G_PETG = E_PETG / (2 * (1 + NU))
RHO = 1.27e-3                            # g/mm^3 PETG solid
P1, Q2 = 20.0, 0.001                     # LC1 20 N hand press (b_eff = L/2), LC2 1 kPa (as B.2)
SHOCK = 3.0                              # jolt factor (as B.2)
CASSETTE_MASS = 0.30                     # kg each, screening placeholder (no panel selected)
MASS = {"display": 0.20, "controller": 0.04, "hinges": 0.05, "cassettes": 2 * CASSETTE_MASS}   # kg, inferred
SPAN = HC + 2 * MIN_GAP                  # 202: back structure spans the cassette bay one-way (front/rear bands)
B_EFF = SPAN / 2
INNER_X = W - 2 * WALL                   # 296
CORNER_P = 20.0                          # N at one free-edge corner (one-handed opening / handling), torsion index


# ---------------------------------------------------------------- section properties
def i_ribbed(skin, h, t=RIB_THICKNESS, s=RIB_SPACING):
    """Per-mm-width I of a skin with external T-ribs (ribs run along the span, Y)."""
    if h <= 0:
        return skin ** 3 / 12
    af, yf = s * skin, skin / 2
    aw, yw = t * h, skin + h / 2
    yb = (af * yf + aw * yw) / (af + aw)
    return (s * skin ** 3 / 12 + af * (yf - yb) ** 2 + t * h ** 3 / 12 + aw * (yw - yb) ** 2) / s


def i_sandwich(skin, core, t=RIB_THICKNESS, s=RIB_SPACING):
    """Per-mm-width I of two skins + rib webs (rib core along the span)."""
    d = (core + skin) / 2
    return 2 * (skin ** 3 / 12 + skin * d ** 2) + t * core ** 3 / 12 / s


def shear_area(h, t=RIB_THICKNESS, s=RIB_SPACING):
    """Per-mm-width shear area carried by the rib webs (Timoshenko term)."""
    return max(t * h / s, 1e-9)


def deflect(iw, as_w=None):
    """LC1 / LC2 mid-span deflection of a one-way strip over SPAN (bending + web shear if as_w)."""
    d1 = P1 * SPAN ** 3 / (48 * E_PETG * iw * B_EFF)
    d2 = 5 * Q2 * SPAN ** 4 / (384 * E_PETG * iw)
    if as_w:
        d1 += P1 * SPAN / (4 * G_PETG * as_w * B_EFF)
        d2 += Q2 * SPAN ** 2 / (8 * G_PETG * as_w)
    return d1, d2


# ---------------------------------------------------------------- layer stack
def front_stack(lip=DISPLAY_BEZEL_LIP, mid=0.0):
    """Lid face -> cassette top: lip + display + gap (+ mid-plate) + rail layer + gap + cassette."""
    layers = [("front retention lip", lip), ("display module", DISPLAY_THICKNESS), ("display-back gap", MIN_GAP)]
    if mid:
        layers.append(("rail mid-plate", mid))
    layers += [("solar rail layer", SOLAR_RAIL_LAYER_HEIGHT), ("rail-cassette gap", MIN_GAP),
               ("stowed cassette", SOLAR_CASSETTE_THICKNESS)]
    return layers


def back_options(allow_factor=0.5):
    """Minimum-thickness back structures meeting delta <= allow_factor * gap for gaps 1..6 mm."""
    out = []
    for gap in (1.0, 1.5, 2.0, 3.0, 4.0, 6.0):
        allow = allow_factor * gap
        best = {}
        # B: single skin 2.5 + external ribs
        h = 0.0
        while h <= 30:
            d = deflect(i_ribbed(STRUCTURAL_SKIN_THICKNESS, h), shear_area(h) if h else None)
            if max(d) <= allow:
                best["ribbed"] = (h, STRUCTURAL_SKIN_THICKNESS + h, d)
                break
            h += 0.5
        # plain thick skin
        t = 2.0
        while t <= 12:
            d = deflect(t ** 3 / 12)
            if max(d) <= allow:
                best["plain"] = (t, t, d)
                break
            t += 0.25
        # C: rib-core sandwich
        c = 2.0
        while c <= 30:
            d = deflect(i_sandwich(SANDWICH_SKIN, c), shear_area(c))
            if max(d) <= allow:
                best["sandwich"] = (c, 2 * SANDWICH_SKIN + c, d)
                break
            c += 0.5
        out.append((gap, best))
    return out


# ---------------------------------------------------------------- torsion index (conceptual)
def j_open_rect(b, t):
    return b * t ** 3 / 3


def j_closed_box(b, hc, ts, tw):
    a = b * hc
    return 4 * a * a / (2 * b / ts + 2 * hc / tw)


def torsion_index(parts):
    j = sum(parts.values())
    torque = CORNER_P * W / 2
    phi = torque * D / (G_PETG * j)
    return j, math.degrees(phi), phi * W / 2


def front_frame_j(mid):
    rz0 = DISPLAY_THICKNESS + MIN_GAP
    strips = 2 * j_open_rect(INNER_X / 2 - sk.DISP_W / 2, rz0)        # bezel side strips beside the display
    walls = 2 * j_open_rect(VFIX["rz0"] + VFIX["rail_h"], WALL)       # side-wall strips below the cassette slot
    rails = 2 * (VFIX["rail_w"] + 2 * VFIX["rail_h"]) * WALL ** 3 / 3
    out = {"bezel strips": strips, "side-wall strips": walls, "rails": rails}
    if mid:
        out["mid-plate"] = j_open_rect(INNER_X, mid)
    return out


# ---------------------------------------------------------------- rail deflection
def rail_cantilever_3g():
    import lid_structure_screening as b2
    i, arm, d, d3 = b2.rail_cantilever()
    return i, arm, d, d3


def rail_on_midplate(mid=MID_PLATE_THICKNESS, b_extra=10.0, composite=True):
    """Rail fastened along a mid-plate strip; simply supported between the side frames (span INNER_X)."""
    import lid_structure_screening as b2
    ir, ar = b2.rail_section()
    b = VFIX["rail_w"] + 2 * b_extra
    ip, ap = b * mid ** 3 / 12, b * mid
    if composite:
        yr = mid + VFIX["rail_h"] * 0.35          # rail centroid above the plate (floor-heavy C-channel, approx.)
        yp = mid / 2
        yb = (ar * yr + ap * yp) / (ar + ap)
        i = ir + ar * (yr - yb) ** 2 + ip + ap * (yp - yb) ** 2
    else:
        i = ir + ip
    p = CASSETTE_MASS * 9.81 * SHOCK
    xc = sk.XI - VFIX["link"] - sk.L / 2              # stowed carriage centre (right cassette)
    a, bb = xc + INNER_X / 2, INNER_X / 2 - xc
    d = p * a * a * bb * bb / (3 * E_PETG * i * INNER_X)
    return i, d


# ---------------------------------------------------------------- masses (solid PETG estimates)
def mass_rear(kind, h):
    area = W * D
    if kind == "ribbed":
        n = int(INNER_X / RIB_SPACING) + 1
        return (area * STRUCTURAL_SKIN_THICKNESS + n * RIB_THICKNESS * D * h) * RHO
    if kind == "sandwich":
        n = int(INNER_X / RIB_SPACING) + 1
        return (area * 2 * SANDWICH_SKIN + n * RIB_THICKNESS * D * h + 2 * WALL * D * h) * RHO
    if kind == "plain":
        return area * h * RHO
    if kind == "cover":
        return area * THIN_COVER * RHO
    return 0.0


FRONT_FRAME_G = 375.0      # B.2 estimate: front frame + edge bands + rails (solid PETG)
MID_PLATE_G = INNER_X * (D - 2 * WALL) * MID_PLATE_THICKNESS * RHO


# ---------------------------------------------------------------- solar / hinge coupling
def deployed_lowest_z(dz, h, lid):
    """Lowest world Z of both deployed cassettes over tilts -75..75 (B.1 V1+fix geometry shifted dz in the lid)."""
    axis = (D - V["HINGE_AXIS_OFFSET"], H + h)
    zmin = math.inf
    for tilt in range(-75, 76, 15):
        for s in (1, -1):
            for k, (x0, x1, poly) in sv.solar_side(VFIX, s, 1, tilt).items():
                if k[0] == "R":
                    continue
                pts = hm.rotate([(y, z + dz + H + G) for y, z in poly], axis, lid)
                zmin = min(zmin, min(z for _, z in pts))
    return zmin


def port_envelope(T):
    """From the C.2 map model: max feasible opening at h 0; minimum h for 120 / 135 deg."""
    mo0, _ = c2.feasibility(T, 0.0)
    need = {}
    for ang in (120.0, 135.0):
        h = 0.0
        while h <= 20:
            mo, _ = c2.feasibility(T, h)
            if mo is not None and mo >= ang:
                need[ang] = h
                break
            h += 0.5
    base = min(hm.signed_clearance(hm.rotate(hm.rect(0, D, H + G, H + G + T), (D, H), a), hm.BASE)
               for a in [i * 1.0 for i in range(0, 136)])
    return mo0, need, base


# ---------------------------------------------------------------- report
def main():
    print("== 1. layer stack (lid face -> back), working values ==")
    for lip in (0.0, DISPLAY_BEZEL_LIP):
        for mid in (0.0, MID_PLATE_THICKNESS):
            st = front_stack(lip, mid)
            print(f"  lip {lip:g}, mid-plate {mid:g}: " + " + ".join(f"{n} {v:g}" for n, v in st)
                  + f" = {sum(v for _, v in st):g} (to cassette top)")
    print(f"  V1 + fixes reference: T 31.5 = 5 + 1 + 13 + 1 + 8 + 1 gap + 2.5 back plate (lip 0)")
    band_y0 = max(y for y, _ in sv.loops(VFIX)["LR"][2]) + MIN_GAP
    band_depth = (D - WALL) - band_y0
    cz0 = VFIX["cz0"]
    print(f"  controller band (hinge end, beside the right service loop): Y {band_y0:.1f}-{D - WALL:g} ({band_depth:.1f} deep), "
          f"Z {WALL:g}-{cz0 - MIN_GAP:g} ({cz0 - MIN_GAP - WALL:g} tall, lid frame, lip 0); X usable per side of a "
          f"{2 * c2.ENV['CW2']:g} mm centre cable pass and {V['HINGE_MOUNT_WIDTH']:g} mm hinge corners: "
          f"{c2.ENV['IX'] - V['HINGE_MOUNT_WIDTH'] - c2.ENV['CW2'] - MIN_GAP:.1f}")
    ctrl_ok = DISPLAY_CONTROLLER_THICKNESS + MIN_GAP <= cz0 - MIN_GAP - WALL
    print(f"  controller envelope {DISPLAY_CONTROLLER_THICKNESS:g} thick fits the band height: {ctrl_ok}; "
          f"cable exit: single 90-deg bend needs R + d = {DISPLAY_CABLE_BEND_RADIUS + DISPLAY_CABLE_CLEARANCE:g} "
          f"({'fits' if DISPLAY_CABLE_BEND_RADIUS + DISPLAY_CABLE_CLEARANCE <= band_depth else 'DOES NOT fit'}); "
          f"a U-turn/service loop needs 2R + d = {2 * DISPLAY_CABLE_BEND_RADIUS + DISPLAY_CABLE_CLEARANCE:g} "
          f"({'fits' if 2 * DISPLAY_CABLE_BEND_RADIUS + DISPLAY_CABLE_CLEARANCE <= band_depth else 'DOES NOT fit'} the {band_depth:.1f} band)")

    print("\n== 2. back structure needed over the 202 mm cassette bay (LC1 20 N / LC2 1 kPa; delta <= gap/2 as B.2) ==")
    print("  gap | ribbed (2.5 skin + h)        | plain skin            | sandwich (2x1.2 + core, shear incl.)")
    opts = back_options()
    for gap, best in opts:
        r, p, s = best.get("ribbed"), best.get("plain"), best.get("sandwich")
        print(f"  {gap:3g} | h {r[0]:4.1f} -> back {r[1]:5.1f}      | t {p[0]:5.2f} -> back {p[1]:5.2f} | "
              f"core {s[0]:4.1f} -> back {s[1]:5.1f}")
    print("  rib height / spacing sensitivity (LC1 mm, 2.5 skin, external ribs; shear incl.):")
    for s in (20, 30, 40):
        vals = []
        for h in (4, 6, 8, 10, 12):
            vals.append(f"h{h}:{deflect(i_ribbed(STRUCTURAL_SKIN_THICKNESS, h, s=s), shear_area(h, s=s))[0]:.2f}")
        print(f"    spacing {s}: " + "  ".join(vals))
    print("  sandwich core sensitivity (LC1 mm, skins 1.2, webs 2.0 @ 30; bending only / with shear):")
    print("    " + "  ".join(f"c{c}:{deflect(i_sandwich(SANDWICH_SKIN, c))[0]:.2f}/{deflect(i_sandwich(SANDWICH_SKIN, c), shear_area(c))[0]:.2f}"
                          for c in (4, 6, 8, 10)))

    print("\n== 3. rail deflection toward the display (stowed cassette, 3 g) ==")
    i, arm, d, d3 = rail_cantilever_3g()
    print(f"  rail cantilever from its outboard pad (A, B, C): I {i:.0f} mm^4, arm {arm:.0f}: {d:.2f} static, {d3:.2f} at 3 g vs 1.0 gap")
    for comp in (False, True):
        ii, dd = rail_on_midplate(composite=comp)
        print(f"  rail fastened on a {MID_PLATE_THICKNESS:g} mid-plate strip, span {INNER_X:g} between side frames (D, E), "
              f"{'composite' if comp else 'non-composite'}: I {ii:.0f}: {dd:.2f} at 3 g")

    print("\n== 4. architectures ==")
    gap_pick = 2.0
    back = dict(opts)[gap_pick]
    arch = {}
    base28 = sum(v for _, v in front_stack(DISPLAY_BEZEL_LIP, 0))
    base30 = sum(v for _, v in front_stack(DISPLAY_BEZEL_LIP, MID_PLATE_THICKNESS))
    # A thin: cover bears on the cassette under load
    cov_per_n = deflect(THIN_COVER ** 3 / 12)[0] / P1
    arch["A thin structural"] = dict(T=base28 + MIN_GAP + THIN_COVER, back="1.6 cover (non-structural)",
                                     midplate=0, rear_mass=mass_rear("cover", 0), dz=DISPLAY_BEZEL_LIP,
                                     note=f"cover touches the cassette at ~{MIN_GAP / cov_per_n:.1f} N (LC1 per-N {cov_per_n:.2f} mm)",
                                     jparts={**front_frame_j(0), "cover": j_open_rect(INNER_X, THIN_COVER)})
    rb = back["ribbed"]
    arch["B two-piece ribbed"] = dict(T=base28 + gap_pick + rb[1], back=f"2.5 skin + {rb[0]:g} ribs", midplate=0,
                                      rear_mass=mass_rear("ribbed", rb[0]), dz=DISPLAY_BEZEL_LIP,
                                      note=f"LC1/LC2 {rb[2][0]:.2f}/{rb[2][1]:.2f}",
                                      jparts={**front_frame_j(0), "rear ribbed (open)": j_open_rect(INNER_X, STRUCTURAL_SKIN_THICKNESS) + 10 * rb[0] * RIB_THICKNESS ** 3 / 3})
    sw = back["sandwich"]
    arch["C sandwich rear shell"] = dict(T=base28 + gap_pick + sw[1], back=f"1.2 + {sw[0]:g} core + 1.2", midplate=0,
                                         rear_mass=mass_rear("sandwich", sw[0]), dz=DISPLAY_BEZEL_LIP,
                                         note=f"LC1/LC2 {sw[2][0]:.2f}/{sw[2][1]:.2f}",
                                         jparts={**front_frame_j(0), "rear sandwich (closed)": j_closed_box(INNER_X, sw[0] + SANDWICH_SKIN, SANDWICH_SKIN, WALL)})
    arch["D modular (mid-plate rail module)"] = dict(T=base30 + gap_pick + sw[1], back=f"1.2 + {sw[0]:g} core + 1.2 (service shell)",
                                                     midplate=MID_PLATE_THICKNESS, rear_mass=mass_rear("sandwich", sw[0]),
                                                     dz=DISPLAY_BEZEL_LIP + MID_PLATE_THICKNESS,
                                                     note=f"LC1/LC2 {sw[2][0]:.2f}/{sw[2][1]:.2f}",
                                                     jparts={**front_frame_j(MID_PLATE_THICKNESS), "rear sandwich (closed)": j_closed_box(INNER_X, sw[0] + SANDWICH_SKIN, SANDWICH_SKIN, WALL)})
    arch["E cassette-backed (no rear shell)"] = dict(T=base30, back="none: stowed cassettes form the back", midplate=MID_PLATE_THICKNESS,
                                                     rear_mass=0.0, dz=DISPLAY_BEZEL_LIP + MID_PLATE_THICKNESS,
                                                     note="LC1 acts directly on the cassette/panel",
                                                     jparts=front_frame_j(MID_PLATE_THICKNESS))
    for name, a in arch.items():
        j, phi, dc = torsion_index(a["jparts"])
        struct = FRONT_FRAME_G + a["rear_mass"] + (MID_PLATE_G if a["midplate"] else 0)
        total = struct / 1000 + sum(MASS.values())
        a.update(j=j, phi=phi, dc=dc, struct=struct, total=total)
        print(f"-- {name}: T {a['T']:.1f} (closed stack {H + G + a['T']:.1f}); back {a['back']}; {a['note']}")
        print(f"   display cavity (face -> rail layer) {DISPLAY_BEZEL_LIP + DISPLAY_THICKNESS + MIN_GAP + a['midplate']:g}; rail layer {SOLAR_RAIL_LAYER_HEIGHT:g}; "
              f"cassette clearances {MIN_GAP:g} below / {gap_pick if 'none' not in a['back'] and 'cover' not in a['back'] else MIN_GAP:g} above")
        print(f"   structure ~{struct:.0f} g PETG; lid total ~{total:.2f} kg (placeholders: display, controller, hinges, 2 cassettes)")
        print(f"   torsion index (mid-depth section, open/closed St Venant only, ring frame ignored): J {j:.0f} mm^4 -> "
              f"{phi:.1f} deg / {dc:.0f} mm corner deflection at {CORNER_P:g} N (conservative index, not a prediction)")

    print("\n== 5. hinge / rear-port coupling (C.2 model: D-006 rear-edge axis, gap 2, port zone Z 4-19, plug 45) ==")
    Ts = sorted({round(a["T"], 1) for a in arch.values()} | {31.5, 35.0, 38.0, 40.0, 42.5})
    for T in Ts:
        mo0, need, base = port_envelope(T)
        print(f"  T {T:5.1f}: max feasible opening at h 0: {mo0:6.1f} deg; min h for 120 deg: {need.get(120.0, '>20')}; "
              f"for 135 deg: {need.get(135.0, '>20')}; lid-base clearance h0 {base:.2f}")

    print("\n== 6. solar coupling (B.1 V1 + fixes geometry shifted with the stack) ==")
    for name, a in arch.items():
        vals = []
        for h in (0.0, 4.0, 8.0):
            lows = [deployed_lowest_z(a["dz"], h, lid) for lid in (105.0, 120.0, 135.0)]
            vals.append(f"h{h:g}: " + "/".join(f"{z:.0f}" for z in lows))
        print(f"  {name}: deployed-cassette lowest Z (tilts +-75) at 105/120/135 deg -> " + "; ".join(vals))
    print("  stowed/deployed internal clearances are the V1+fix stack gaps (>= MIN_GAP); deployed cassettes sit at |X| >= "
          f"{sk.XI + VFIX['S']:.1f}, outside the lid/base width {W / 2:g}, so back structure and base never meet them.")


if __name__ == "__main__":
    main()
