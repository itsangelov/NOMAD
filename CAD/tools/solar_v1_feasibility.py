"""P0.1 Round B.1: focused feasibility pass on solar layout V1 (modeled; V1 is NOT chosen).

V1 = rail layer between display and cassettes, left/right rails staggered in Y, lid 31.5 mm.
Adds to the Round B skeleton: display bezel, lid walls with explicit side-wall openings, the hub
bracket that joins the (rail-layer) hub pin to the cassette, a provisional protected cable
envelope (tilt-joint twist zone + rolling service loops + routing to the hinge side), and the
rear-face hinge (D-006) with the thicker lid.

Same exact prism machinery as solar_skeleton_model.py (Onshape-validated). Values that are not
in nomad.yaml are provisional what-if constants below; nomad.yaml is not changed by this pass.

Usage:  py CAD/tools/solar_v1_feasibility.py [--crosscheck]
"""

import math
import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hinge_feasibility_2d as hm  # noqa: E402
import solar_skeleton_model as sk  # noqa: E402

V = hm.V
D, H, G, W, WALL, MIN_GAP, CLR = sk.D, sk.H, sk.G, sk.W, sk.WALL, sk.MIN_GAP, V["CLEARANCE"]
WC, HC, TC, L, PIN = sk.WC, sk.HC, sk.TC, sk.L, sk.PIN
DISP_T, DISP_W, DISP_H = sk.DISP_T, sk.DISP_W, sk.DISP_H
HINGE, LID_ANGLES, XW = sk.HINGE, sk.LID_ANGLES, sk.X_WALL_IN
TILT_MAX = sk.TILT_MAX
box = sk.box

# ---- provisional what-if constants (V1 pass only; not in nomad.yaml) ----
T1 = 31.5            # V1 lid thickness (Round B minimum)
BRACKET_L = 10.0     # hub bracket length along X (rotates with cassette), envelope only
CABLE_D = 6.0        # protected solar-lead envelope diameter (not a wire selection)
CABLE_R = 20.0       # service-loop bend-radius envelope (not a wire selection)
E_PETG = 2000.0      # MPa, nominal PETG modulus for a rough plate estimate only
TILTS_REPORT = [0, 15, -15, 30, -30, 45, -45, 60, -60, 75, -75]


CABLE_R_OFF = PIN / 2 + MIN_GAP + CABLE_D / 2     # cable centre offset from the tilt axis (beside the pin)


def config(fix=False):
    """V1 as specified (fix=False) or V1 with the minimal fixes found by this pass (fix=True).

    As specified: Round B carriage 12 x 8 centred on the pin, bracket = pin + walls, rails 1 mm apart,
    deploy clearance 5. Fixes: bracket/carriage enclose pin + cable side by side, carriage wide enough to
    be retained under the bracket slot, an 8 mm cable corridor between the rails, deploy clearance 8.
    """
    deploy = V["SOLAR_DEPLOY_CLEARANCE"] + (CABLE_D + 2 * MIN_GAP - V["SOLAR_DEPLOY_CLEARANCE"] if fix else 0)
    bracket_w = PIN + MIN_GAP + CABLE_D + 2 * WALL if fix else PIN + 2 * WALL
    coff = (MIN_GAP + CABLE_D) / 2 if fix else 0.0       # carriage/rail centre offset from the pin, toward the cable
    slot_w = bracket_w + 2 * CLR
    cw = slot_w + 2 * WALL if fix else V["SOLAR_CARRIAGE_WIDTH"]
    rail_w, rail_h = cw + 2 * WALL, V["SOLAR_CARRIAGE_HEIGHT"] + 2 * WALL
    corridor = CABLE_D + 2 * MIN_GAP if fix else MIN_GAP
    travel = WC + WALL + deploy
    link = WALL + deploy + MIN_GAP
    rz0 = DISP_T + MIN_GAP                      # rail layer bottom (lid frame, from display face)
    rz = rz0 + rail_h / 2
    cz0 = rz0 + rail_h + MIN_GAP
    rc = {s: D / 2 + s * (rail_w / 2 + corridor / 2) for s in (1, -1)}
    return {"fix": fix, "T": T1, "deploy": deploy, "S": travel, "link": link, "cw": cw, "ch": V["SOLAR_CARRIAGE_HEIGHT"],
            "rail_w": rail_w, "rail_h": rail_h, "rz0": rz0, "cz0": cz0, "cy0": (D - HC) / 2, "slot_w": slot_w,
            "bracket_w": bracket_w, "coff": coff, "corridor": corridor, "rc": rc,
            "hub": {s: (rc[s] - s * coff, rz) for s in (1, -1)}, "back": T1 - WALL}


# ------------------------------------------------------------------ geometry (lid frame, z from display face)
def xint(s, a, b):
    return (a, b) if s > 0 else (-b, -a)


def cable_offset(s):
    """Right cable rides on the +Y side of its pin (toward the rear zone), left on the -Y side."""
    return s


def twist_zone(c, s, xi):
    """Convex hull of the cable envelope swept +/-TILT_MAX about the hub at the tilt joint."""
    hy, hz = c["hub"][s]
    r = CABLE_R_OFF
    base = 0.0 if cable_offset(s) > 0 else 180.0
    pts = []
    for k in range(-15, 16):
        a = math.radians(base + TILT_MAX * k / 15)
        cy, cz = hy + r * math.cos(a), hz + r * math.sin(a)
        for j in range(8):
            b = 2 * math.pi * j / 8
            pts.append((cy + CABLE_D / 2 * math.cos(b), cz + CABLE_D / 2 * math.sin(b)))
    hull = _hull(pts)
    return (*xint(s, xi - MIN_GAP - CABLE_D, xi - MIN_GAP), hull)


def _hull(pts):
    pts = sorted(set(pts))
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and _cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and _cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def _cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def solar_side(c, s, ext, tilt):
    t = "R" if s > 0 else "L"
    xi = sk.XI + ext * c["S"]
    kx1 = xi - c["link"]
    hy, hz = c["hub"][s]
    rc = c["rc"][s]
    cy = hy + cable_offset(s) * CABLE_R_OFF
    bc = hy + s * c["coff"]
    cass = box(c["cy0"], c["cy0"] + HC, c["cz0"], c["cz0"] + TC)
    brk = box(bc - c["bracket_w"] / 2, bc + c["bracket_w"] / 2, hz - PIN / 2 - WALL, c["cz0"])
    if tilt:
        cass, brk = hm.rotate(cass, (hy, hz), tilt), hm.rotate(brk, (hy, hz), tilt)
    parts = {
        "C" + t: (*xint(s, xi, xi + WC), cass),
        "Q" + t: (*xint(s, xi, xi + BRACKET_L), brk),                       # hub bracket (rotates)
        "P" + t: (*xint(s, kx1, xi), box(hy - PIN / 2, hy + PIN / 2, hz - PIN / 2, hz + PIN / 2)),
        "K" + t: (*xint(s, kx1 - L, kx1), box(rc - c["cw"] / 2, rc + c["cw"] / 2, hz - c["ch"] / 2, hz + c["ch"] / 2)),
        "X" + t: (*xint(s, kx1 - L, xi), box(cy - CABLE_D / 2, cy + CABLE_D / 2, hz - CABLE_D / 2, hz + CABLE_D / 2)),  # cable along link
        "R" + t: (*xint(s, sk.XI - c["link"] - L, sk.XI + c["S"] - c["link"]),
                  box(rc - c["rail_w"] / 2, rc + c["rail_w"] / 2, c["rz0"], c["rz0"] + c["rail_h"])),
    }
    if ext == 1:
        parts["Z" + t] = twist_zone(c, s, xi)
    return parts


def loops(c):
    """Rolling service-loop keep-outs in the rail layer: right in the rear zone, left in the front zone."""
    band = 2 * CABLE_R + CABLE_D
    out = {}
    for s in (1, -1):
        rc = c["rc"][s]
        exit_lo = sk.XI - c["link"] - L                       # carriage inboard end, stowed
        exit_hi = exit_lo + c["S"]                            # deployed
        x0, x1 = max(-XW, exit_lo - 2 * CABLE_R), min(XW, exit_hi + 2 * CABLE_R)
        if s > 0:
            y0 = rc + c["rail_w"] / 2 + MIN_GAP
            out["LR"] = (x0, x1, box(y0, y0 + band, c["rz0"], c["rz0"] + c["rail_h"]))
        else:
            y1 = rc - c["rail_w"] / 2 - MIN_GAP
            out["LL"] = (-x1, -x0, box(y1 - band, y1, c["rz0"], c["rz0"] + c["rail_h"]))
    return out


def openings(c, s=1):
    """Per-part Y-Z boxes (lid frame) that must pass side wall `s` during the slide, + MIN_GAP."""
    boxes = {}
    for ext in [i / 40 for i in range(41)]:
        for k, (x0, x1, p) in solar_side(c, s, ext, 0).items():
            a, b = (x0, x1) if s > 0 else (-x1, -x0)
            if k[0] in "CQPX" and b > XW and a < W / 2:
                ys, zs = [y for y, _ in p], [z for _, z in p]
                b = boxes.get(k[0], [9e9, -9e9, 9e9, -9e9])
                boxes[k[0]] = [min(b[0], min(ys) - MIN_GAP), max(b[1], max(ys) + MIN_GAP),
                               min(b[2], min(zs) - MIN_GAP), max(b[3], max(zs) + MIN_GAP)]
    return boxes


def lid_parts(c):
    T, back = c["T"], c["back"]
    dy0 = D / 2 - V["DISPLAY_VERTICAL_OFFSET"] - DISP_H / 2
    return {
        "D": (-DISP_W / 2, DISP_W / 2, box(dy0, dy0 + DISP_H, 0, DISP_T)),
        "Nf": (-XW, XW, box(WALL, dy0, 0, WALL)), "Nr": (-XW, XW, box(dy0 + DISP_H, D - WALL, 0, WALL)),   # bezel frame
        "Ns": (DISP_W / 2, XW, box(dy0, dy0 + DISP_H, 0, WALL)), "Nt": (-XW, -DISP_W / 2, box(dy0, dy0 + DISP_H, 0, WALL)),
        "Wb": (-W / 2, W / 2, box(0, D, back, T)),
        "Wf": (-XW, XW, box(0, WALL, 0, back)), "Wr": (-XW, XW, box(D - WALL, D, 0, back)),
    }


def side_wall_pieces(c, s=1):
    """Remaining side-wall material (Y-Z rectangles, lid frame) after cutting the openings."""
    ops = list(openings(c, s).values())
    ys = sorted({0, D} | {min(max(v, 0), D) for o in ops for v in o[:2]})
    zs = sorted({0, c["back"]} | {min(max(v, 0), c["back"]) for o in ops for v in o[2:]})
    pieces = []
    for y0, y1 in zip(ys, ys[1:]):
        for z0, z1 in zip(zs, zs[1:]):
            ym, zm = (y0 + y1) / 2, (z0 + z1) / 2
            if not any(o[0] < ym < o[1] and o[2] < zm < o[3] for o in ops):
                pieces.append((y0, y1, z0, z1))
    return pieces


def all_parts(c, eR, eL, tilt):
    p = {**lid_parts(c), **loops(c), **solar_side(c, 1, eR, tilt if eR == 1 else 0),
         **solar_side(c, -1, eL, tilt if eL == 1 else 0)}
    for i, (y0, y1, z0, z1) in enumerate(side_wall_pieces(c, 1)):
        p[f"S{i:02d}"] = (XW, W / 2, box(y0, y1, z0, z1))
    for i, (y0, y1, z0, z1) in enumerate(side_wall_pieces(c, -1)):
        p[f"s{i:02d}"] = (-W / 2, -XW, box(y0, y1, z0, z1))
    return p


ATTACHED = [set(x) for x in ("PK", "PR", "KR", "PC", "PQ", "QC", "XP", "XK", "XQ", "XR", "XC", "ZP", "ZQ", "ZX", "ZC", "QR", "KQ")]


def excluded(a, b):
    if a[0] in "DNWSsL" and b[0] in "DNWSsL":
        return True                           # fixed lid structure/keep-outs among themselves
    if len(a) == 2 and len(b) == 2 and a[1] == b[1] and a[0] in "CQPKXRZ" and b[0] in "CQPKXRZ" and {a[0], b[0]} in ATTACHED:
        return True                           # same-side assembly, by design (QR = bracket in rail slot)
    if {a[0], b[0]} & {"R"} and {a[0], b[0]} & set("WNSs"):
        return True                           # fixed rail may be integral with lid structure
    if a[0] == "L" and b[0] == "L":
        return True
    return False


def own_loop(a, b):
    """A cable may join its own service loop."""
    pair = {a, b}
    return pair in ({"XR", "LR"}, {"XL", "LL"})


def to_world(parts, lid):
    zb = H + G
    return {k: (x0, x1, hm.rotate([(y, z + zb) for y, z in p], HINGE, lid)) for k, (x0, x1, p) in parts.items()}


def check(world, base=True):
    if base:
        world = {**world, "B": (-W / 2, W / 2, box(0, D, 0, H))}
    names = sorted(world)
    viol, mins = [], {}
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if "B" in (a, b):
                other = b if a == "B" else a
                if other[0] not in "CQPKXRZ":
                    continue
            elif excluded(a, b) or own_loop(a, b):
                continue
            cl = sk.clearance(world[a], world[b])
            mins[a + "-" + b] = cl
            if cl < MIN_GAP - 1e-6:
                viol.append((a + "-" + b, round(cl, 2)))
    zmin = min(min(z for _, z in p) for k, (_, _, p) in world.items() if k[0] in "CQPKXRZ")
    return viol, zmin, mins


# ------------------------------------------------------------------ analyses
def routing(c):
    """Can each side's service-loop fixed end reach the hinge-side zone in the rail layer (1 mm grid)?"""
    inflate = CABLE_D / 2 + MIN_GAP
    lp = loops(c)
    obst = []
    for s in (1, -1):
        x0, x1, p = solar_side(c, s, 0, 0)["R" + ("R" if s > 0 else "L")]
        ys = [y for y, _ in p]
        obst.append((x0 - inflate, x1 + inflate, min(ys) - inflate, max(ys) + inflate))
    res = {}
    for s, own, other in ((1, "LR", "LL"), (-1, "LL", "LR")):
        ox0, ox1, op = lp[other]
        oys = [y for y, _ in op]
        blocks = obst + [(ox0 - inflate, ox1 + inflate, min(oys) - inflate, max(oys) + inflate)]
        x0, x1, p = lp[own]
        ys = [y for y, _ in p]
        h = 0.5                                                # grid step, mm
        start = (round((x0 + x1) / 2 / h) * h, round((min(ys) + max(ys)) / 2 / h) * h)
        seen, q = {start}, deque([start])
        free = lambda x, y: (-XW + inflate <= x <= XW - inflate and WALL + inflate <= y <= D - WALL - inflate and
                             not any(b[0] + 1e-9 < x < b[1] - 1e-9 and b[2] + 1e-9 < y < b[3] - 1e-9 for b in blocks))
        ok = False
        while q:
            x, y = q.popleft()
            if y >= D - WALL - inflate - 1:
                ok = True
                break
            for dx, dy in ((h, 0), (-h, 0), (0, h), (0, -h)):
                n = (x + dx, y + dy)
                if n not in seen and free(*n):
                    seen.add(n)
                    q.append(n)
        res["R" if s > 0 else "L"] = ok
    under = c["rz0"] - WALL          # free height between bezel back and rail layer beside the display
    return res, under


def hinge_check(c):
    """Lid envelope (thickness T) swept 0..LID_ANGLE_MAX vs base, rear-face hinge (D-006 working)."""
    lid = hm.rect(0, D, H + G, H + G + c["T"])
    worst, at = 9e9, None
    for a in hm.angles(hm.STEP):
        s = hm.signed_clearance(hm.rotate(lid, HINGE, a), hm.BASE)
        if s < worst:
            worst, at = s, a
    out = {}
    for tag, a in (("105", LID_ANGLES[1]), ("135", LID_ANGLES[2])):
        pts = hm.rotate(lid, HINGE, a)
        out[tag] = (max(y for y, _ in pts) - D, max(z for _, z in pts))
    return worst, at, out


def plate_estimate(c):
    """Back plate as a simply supported strip across the cassette bay (rough beam estimate only)."""
    span = HC + 2 * MIN_GAP
    b, t = W - 2 * WALL, WALL
    I = b * t ** 3 / 12
    per_n = span ** 3 / (48 * E_PETG * I)
    return span, per_n, MIN_GAP / per_n


def report(c):
    tag = "V1 + minimal fixes" if c["fix"] else "V1 as specified"
    print(f"\n==================== {tag} ====================")
    print(f"lid T {c['T']:g}: display z 0-{DISP_T:g}; rail layer z {c['rz0']:g}-{c['rz0'] + c['rail_h']:g}; "
          f"cassette z {c['cz0']:g}-{c['cz0'] + TC:g}; back plate z {c['back']:g}-{c['T']:g}")
    hy, rc = c["hub"], c["rc"]
    print(f"rails: R y {rc[1] - c['rail_w'] / 2:g}-{rc[1] + c['rail_w'] / 2:g}, L y {rc[-1] - c['rail_w'] / 2:g}-{rc[-1] + c['rail_w'] / 2:g} "
          f"(gap {c['corridor']:g}); hub axes y {hy[1][0]:g} / {hy[-1][0]:g}, z {hy[1][1]:g}; carriage {c['cw']:g} x {c['ch']:g}; "
          f"rail env {c['rail_w']:g} x {c['rail_h']:g}")
    print(f"travel S {c['S']:g} (deploy clearance {c['deploy']:g}), link {c['link']:g}, rail x {sk.XI - c['link'] - L:g}..{sk.XI + c['S'] - c['link']:g} "
          f"(length {c['S'] + L:g}; own-half available carriage travel {XW - MIN_GAP - sk.XI - L:g})")
    print(f"carriage capture: rail top slot {c['slot_w']:.1f} (bracket {c['bracket_w']:g} + 2x{CLR:g}) vs carriage {c['cw']:g} "
          f"-> retaining lip {(c['cw'] - c['slot_w']) / 2:.2f} per side")
    hy0, rc0, bc0 = c["hub"][1][0], c["rc"][1], c["hub"][1][0] + c["coff"]
    cab = (hy0 + CABLE_R_OFF - CABLE_D / 2, hy0 + CABLE_R_OFF + CABLE_D / 2)
    over_k = max(0, cab[1] - (rc0 + c["cw"] / 2), (rc0 - c["cw"] / 2) - (hy0 - PIN / 2))
    over_b = max(0, cab[1] + WALL - (bc0 + c["bracket_w"] / 2), (bc0 - c["bracket_w"] / 2) - (hy0 - PIN / 2 - WALL))
    print(f"pin + cable side by side: cable y {cab[0] - hy0:+.1f}..{cab[1] - hy0:+.1f} from axis; exceeds carriage by {over_k:.1f}, "
          f"exceeds bracket (with wall) by {over_b:.1f}  -> {'FITS' if over_k == 0 and over_b == 0 else 'DOES NOT FIT'}")
    # structure
    for s, nm in ((1, "right"), (-1, "left")):
        ops = openings(c, s)
        slot = ops["C"]
        notch = [min(ops[k][0] for k in "QPX"), max(ops[k][1] for k in "QPX"), min(ops[k][2] for k in "QPX")]
        rail_y = (c["rc"][s] - c["rail_w"] / 2, c["rc"][s] + c["rail_w"] / 2)
        left_in_rail = max(0, notch[0] - rail_y[0]) + max(0, rail_y[1] - notch[1])
        print(f"{nm} side wall (y 0-{D:g} x z 0-{c['back']:g}, {WALL:g} thick): cassette slot y {slot[0]:.1f}-{slot[1]:.1f} x z {slot[2]:.1f}-{slot[3]:.1f}; "
              f"bracket/pin/cable notch y {notch[0]:.1f}-{notch[1]:.1f} from z {notch[2]:.1f} up into the slot")
        print(f"   remaining: end posts {slot[0]:.1f} and {D - slot[1]:.1f} wide (full height); lower strip z 0-{slot[2]:.1f} "
              f"reduced to z 0-{notch[2]:.1f} over the notch ({notch[1] - notch[0]:.1f} wide); nothing above the slot except the "
              f"back plate edge ({WALL:g}); wall left inside the rail's Y band for a rail-to-wall joint: {left_in_rail:.1f} of {c['rail_w']:g}")
    span, per_n, n_to_touch = plate_estimate(c)
    print(f"back plate: {WALL:g} thick, clear span {span:g} across the cassette bay (no internal ribs possible); "
          f"rough estimate {per_n:.3f} mm per N at centre -> touches cassettes (1 mm) at ~{n_to_touch:.1f} N")
    # electronics space
    lp = loops(c)
    ry = [y for y, _ in lp["LR"][2]]
    ly = [y for y, _ in lp["LL"][2]]
    rear = (max(ry) + MIN_GAP, D - WALL)
    front = (WALL, min(ly) - MIN_GAP)
    rl = c["rail_h"]
    print(f"service loops (bend R {CABLE_R:g}, cable {CABLE_D:g}): LR y {min(ry):g}-{max(ry):g}, x {lp['LR'][0]:g}..{lp['LR'][1]:g}; "
          f"LL y {min(ly):g}-{max(ly):g}")
    print(f"free rail-layer space (height {rl:g}): rear zone y {rear[0]:g}-{rear[1]:g} ({rear[1] - rear[0]:g} x {2 * XW:g}); "
          f"front zone y {front[0]:g}-{front[1]:g} ({front[1] - front[0]:g} x {2 * XW:g})")
    route, under = routing(c)
    print(f"cable routing to hinge side (rail layer): right {'OK' if route['R'] else 'BLOCKED'}, left {'OK' if route['L'] else 'BLOCKED'}; "
          f"free height under rail layer beside display {under:g} (cable needs {CABLE_D + 2 * MIN_GAP:g})")
    # motion + whole device
    worst_static = {}
    for lid in LID_ANGLES:
        for eR in (0, 0.25, 0.5, 0.75, 1):
            for eL in (0, 0.25, 0.5, 0.75, 1):
                viol, _, _ = check(to_world(all_parts(c, eR, eL, 0), lid))
                for p, cl in viol:
                    worst_static[p] = min(worst_static.get(p, 9e9), cl)
    print("slide/stowed violations:", ", ".join(f"{p} {v:+.2f}" for p, v in sorted(worst_static.items(), key=lambda x: x[1])) or "none")
    _, _, m0 = check(to_world(all_parts(c, 0, 0, 0), LID_ANGLES[1]))
    keys = ["CL-CR", "CR-Wb", "CR-RR", "CR-RL", "CL-RR", "RL-RR", "D-RL", "D-RR", "QR-RL", "D-QR", "D-KR"]
    print("stowed clearances:", ", ".join(f"{k} {m0[k]:.2f}" for k in keys if k in m0))
    for lid in LID_ANGLES:
        row, bad = [], []
        for t in TILTS_REPORT:
            viol, zmin, _ = check(to_world(all_parts(c, 1, 1, t), lid))
            viol = [v for v in viol if v[0] not in worst_static]
            row.append(f"{t:+d}:{zmin:.0f}{'!' if zmin < 0 else ''}")
            bad += [f"{t:+d} {p}" for p, _ in viol]
        print(f"lid {lid:5.1f} deployed, tilt: solar min z (! = below table): " + " ".join(row) + (f"; collisions: {bad}" if bad else ""))
    worst_dep = {}
    for lid in LID_ANGLES:
        for t in TILTS_REPORT:
            _, _, md = check(to_world(all_parts(c, 1, 1, t), lid))
            for k, v in md.items():
                a, b = k.split("-")
                for part in (a, b):
                    if part in ("CR", "QR", "XR", "ZR", "PR"):
                        other = b if part == a else a
                        cat = "base" if other == "B" else "lid side wall" if other[0] == "S" else other
                        worst_dep[(part, cat)] = min(worst_dep.get((part, cat), 9e9), v)
    names = {"CR": "cassette", "QR": "hub bracket", "XR": "cable run", "ZR": "cable twist zone", "PR": "pin"}
    print("deployed minimum clearances (all lid angles and tilts, right side):",
          ", ".join(f"{names[p]}-{cat} {v:.2f}" for (p, cat), v in sorted(worst_dep.items()) if cat in ("base", "lid side wall", "Wb", "Nt", "Ns", "KR", "RR")))
    w, at, ov = hinge_check(c)
    print(f"rear-face hinge with lid {c['T']:g}: min lid/base clearance over 0-135 = {w:.2f} at {at:g} deg; "
          f"rear overhang/max height 105: {ov['105'][0]:.1f}/{ov['105'][1]:.1f}, 135: {ov['135'][0]:.1f}/{ov['135'][1]:.1f}; "
          f"closed stack {H + G + c['T']:g}")


def crosscheck():
    """V1 core skeleton (cassette, pin, carriage, rail) in the six Round B cross-check states."""
    lay = sk.layout("V1", T=T1)
    out = ["X"]
    for label, lid, eR, eL, t in sk.CROSSCHECK:
        w = sk.state(lay, lid, eR, eL, t)
        w = {k: v for k, v in w.items() if k in sk.XC_KEYS}
        viol, zmin, _ = sk.check(w)
        pairs = "".join(sorted(p.replace("-", "") for p, cl in viol if cl < 0))
        out.append(f"{label}:{pairs or '-'}z{zmin:.1f}")
    print(" ".join(out))


if __name__ == "__main__":
    if "--crosscheck" in sys.argv:
        crosscheck()
        sys.exit()
    report(config(False))
    report(config(True))
