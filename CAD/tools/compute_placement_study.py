"""Round C.1: compute-placement study (concepts A-E) and lid/port interaction screen. Analysis only.

Uses the Round C base V0.1 geometry (base_v01_layout.py) and nomad.yaml working values. Concept
placements are concept-level boxes, NOT checked against every boss/standoff; they exist to compare
heights, volumes, separations, cable-length proxies and centre of mass. Nothing here is a decision.

  py CAD/tools/compute_placement_study.py

Evidence level: modeled (geometry arithmetic on working values) unless a line says inferred.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import base_v01_layout as bl  # noqa: E402
import hinge_feasibility_2d as hm  # noqa: E402

P = bl.PARAMS
ENV, PARTS = bl.evaluate()
E = ENV
G, MIN_GAP, H0, D0 = P["LID_CLOSED_GAP"], P["MIN_GAP"], P["BODY_HEIGHT"], P["BODY_DEPTH"]
S = P["PI_STACK_HEIGHT"]
AIR_PLENUM = 5.0            # ASSUMPTION: extra top plenum if the cooler must breathe from above
# Placeholder masses (kg) for a RELATIVE centre-of-mass comparison only (inferred, not measured).
MASS = {"pi": 0.10, "battery": 0.35, "power": 0.08, "cpower": 0.03, "gnss": 0.02}


def vol(b):
    return (b[3] - b[0]) * (b[4] - b[1]) * (b[5] - b[2]) / 1000.0


def gap(a, b):
    dx = max(0.0, b[0] - a[3], a[0] - b[3])
    dy = max(0.0, b[1] - a[4], a[1] - b[4])
    dz = max(0.0, b[2] - a[5], a[2] - b[5])
    return math.sqrt(dx * dx + dy * dy + dz * dz)


def ctr(b):
    return ((b[0] + b[3]) / 2, (b[1] + b[4]) / 2, (b[2] + b[5]) / 2)


def mirror(b):
    return (-b[3], b[1], b[2], -b[0], b[4], b[5])


def box_of(name):
    for n, _, prims in PARTS:
        if n == name:
            lo, hi = bl.bbox(prims)
            return (*lo, *hi)
    raise KeyError(name)


# ---------------------------------------------------------------- stack-height budgets
def h_palm(stack):
    """Palm-rest bay: panel + gap + sled + stack + gap + deck."""
    return P["SERVICE_PANEL_THICKNESS"] + MIN_GAP + P["MOUNT_PLATE_THICKNESS"] + stack + MIN_GAP + P["WALL_THICKNESS"]


def h_under_kb(stack, plenum=0.0, tray_cutout=False):
    """Under the keyboard: stack below the keyboard tray (or below the keyboard itself via a tray cut-out)."""
    top = P["KEYBOARD_TOP_RECESS"] + P["KEYBOARD_THICKNESS"] + (0.0 if tray_cutout else P["MOUNT_PLATE_THICKNESS"])
    return top + MIN_GAP + plenum + stack + P["MOUNT_PLATE_THICKNESS"] + MIN_GAP + P["SERVICE_PANEL_THICKNESS"]


# ---------------------------------------------------------------- concepts (concept-level boxes)
A = {
    "pi": box_of("ENV_PI_STACK"), "battery": box_of("ENV_BATTERY_BAY"), "power": box_of("ENV_POWER_ELECTRONICS"),
    "gnss": box_of("ENV_GNSS_MODULE"), "cpower": box_of("ENV_COMPUTE_POWER"),
}
B = {k: mirror(v) for k, v in A.items()}

H_C = h_under_kb(S)
KTZ0_C = H_C - P["KEYBOARD_TOP_RECESS"] - P["KEYBOARD_THICKNESS"] - P["MOUNT_PLATE_THICKNESS"]
PI_W, PI_D = E["PIW"], E["PID"]
x0c = E["CW2"] + MIN_GAP + 3.5            # clear of the centreline trackpad/display corridors
C = {
    "pi": (x0c, E["KTY0"] + 13, E["SLZ1"], x0c + PI_W, E["KTY0"] + 13 + PI_D, KTZ0_C - MIN_GAP),
    "battery": (A["battery"][0], A["battery"][1], A["battery"][2], A["battery"][3], A["battery"][4],
                H_C - P["WALL_THICKNESS"] - MIN_GAP),            # palm bay grows with the body height
    "power": A["power"],
    "gnss": (60.0, 15.0, E["CZ0"], 60.0 + P["GNSS_MODULE_WIDTH"], 15.0 + P["GNSS_MODULE_DEPTH"], E["CZ0"] + P["GNSS_MODULE_HEIGHT"]),
    "cpower": (60.0, 60.0, E["CZ0"], 60.0 + P["COMPUTE_POWER_WIDTH"], 60.0 + P["COMPUTE_POWER_DEPTH"], E["CZ0"] + P["COMPUTE_POWER_HEIGHT"]),
}
# D: rear electronics bay behind the keyboard; body depth grows until the Pi fits.
D_Y0 = E["KTY1"] + MIN_GAP
D_Y1 = D_Y0 + PI_D
D_DEPTH = D_Y1 + MIN_GAP + P["WALL_THICKNESS"]
D = {
    "pi": (x0c + 4, D_Y0, E["SLZ1"], x0c + 4 + PI_W, D_Y1, E["PIZ1"]),
    "battery": A["battery"],
    "power": A["power"],
    "gnss": C["gnss"],
    "cpower": A["cpower"],
}
# E: split: Pi in the right palm bay; battery flat under the keyboard (left); power electronics under the
# keyboard (right, next to compute power); GNSS alone in the left palm bay.
E_BATT = (-E["IX"] + 7, E["KTY0"] + MIN_GAP, E["CZ0"], -E["CW2"] - MIN_GAP - 1, E["TRY0"] - MIN_GAP, E["KTZ0"] - MIN_GAP)
Ecn = {
    "pi": A["pi"],
    "battery": E_BATT,
    "power": (E["CCX0"] - P["POWER_ELEC_WIDTH"], E["KTY0"] + MIN_GAP, E["CZ0"], E["CCX0"], E["KTY0"] + MIN_GAP + P["POWER_ELEC_DEPTH"], E["PEZ1"]),
    "gnss": (-134.0, 30.0, E["CZ0"], -134.0 + P["GNSS_MODULE_WIDTH"], 30.0 + P["GNSS_MODULE_DEPTH"], E["GNZ1"]),
    "cpower": (E["CCX0"] - P["COMPUTE_POWER_WIDTH"], 150.0, E["CZ0"], E["CCX0"], 150.0 + P["COMPUTE_POWER_DEPTH"], E["CPZ1"]),
}
CONCEPTS = {"A right palm bay": (A, H0, D0), "B left palm bay": (B, H0, D0), "C under keyboard": (C, H_C, D0),
            "D rear bay": (D, H0, D_DEPTH), "E split": (Ecn, H0, D0)}


def endpoints(name, depth):
    """Cable end points (X, Y) for the length proxy: main port panel, display pass-through, keyboard drop,
    trackpad drop."""
    port = (-65.0, E["IY1"]) if name.startswith("B") else (65.0, E["IY1"])
    if name.startswith("D"):
        port = (ctr(D["pi"])[0], depth - P["WALL_THICKNESS"])       # Pi can face the rear wall
    return {"ports": port, "display": (0.0, depth), "keyboard": (0.0, (E["TRY0"] + E["TRY1"]) / 2),
            "trackpad": (0.0, E["TTY1"])}


def cable_proxy(name, c, depth):
    pc = ctr(c["pi"])
    ends = endpoints(name, depth)
    out = {k: abs(pc[0] - x) + abs(pc[1] - y) for k, (x, y) in ends.items()}
    out["cpower"] = abs(pc[0] - ctr(c["cpower"])[0]) + abs(pc[1] - ctr(c["cpower"])[1])
    return out


def com(c):
    m = sum(MASS.values())
    return tuple(sum(MASS[k] * ctr(c[k])[i] for k in MASS) / m for i in range(2))


# ---------------------------------------------------------------- lid / port screen
def lid_low(T, ang, h=0.0, plug=P["PLUG_KEEPOUT_LENGTH"], H=H0, D=D0):
    """Lowest Z of the lid inside the external plug corridor Y in [D, D + plug] (analytic polygon clip)."""
    axis = (D - P["HINGE_AXIS_OFFSET"], H + h)
    poly = hm.rotate(hm.rect(0, D, H + G, H + G + T), axis, ang)
    zs = []
    n = len(poly)
    for i in range(n):
        (y0, z0), (y1, z1) = poly[i], poly[(i + 1) % n]
        for (y, z) in ((y0, z0), (y1, z1)):
            if D - 1e-9 <= y <= D + plug:
                zs.append(z)
        for yb in (D, D + plug):
            if (y0 - yb) * (y1 - yb) < 0:
                t = (yb - y0) / (y1 - y0)
                zs.append(z0 + t * (z1 - z0))
    return min(zs) if zs else math.inf


def plug_clear(T, ang, h=0.0, H=H0, plug=P["PLUG_KEEPOUT_LENGTH"]):
    zone = hm.rect(D0, D0 + plug, E["PZ0"], E["PZ1"])
    lid = hm.rotate(hm.rect(0, D0, H + G, H + G + T), (D0 - P["HINGE_AXIS_OFFSET"], H + h), ang)
    return hm.signed_clearance(lid, zone)


def max_angle(T, h=0.0):
    a = 90.0
    while a < 180 and plug_clear(T, a + 0.5, h) >= MIN_GAP - 1e-9:
        a += 0.5
    return a


def needed_h(T, ang=P["LID_ANGLE_MAX"]):
    h = 0.0
    while plug_clear(T, ang, h) < MIN_GAP - 1e-9 and h < 60:
        h += 0.1
    return h


def main():
    print("== stack-height budgets (modeled; stack heights are working/inferred) ==")
    for s in (25, 28, 30):
        print(f"  stack {s}: palm bay needs H {h_palm(s):5.1f}; under keyboard {h_under_kb(s):5.1f} "
              f"(+{AIR_PLENUM:g} top plenum: {h_under_kb(s, AIR_PLENUM):5.1f}; tray cut-out: {h_under_kb(s, tray_cutout=True):5.1f})")
    print(f"  current working BODY_HEIGHT {H0:g}; under-keyboard free height {E['KTZ0'] - E['IZ0']:g}; palm bay {E['IZ1'] - E['IZ0']:g}")
    print(f"  D rear bay: Pi Y {D_Y0:g}..{D_Y1:g} -> BODY_DEPTH {D_DEPTH:g} (+{D_DEPTH - D0:g})")

    print("\n== concepts ==")
    for name, (c, H, depth) in CONCEPTS.items():
        cp = cable_proxy(name, c, depth)
        cx, cy = com(c)
        print(f"-- {name}: H {H:g}, depth {depth:g}")
        print(f"   battery reserve {vol(c['battery']):6.1f} cm3  box {tuple(round(v, 1) for v in c['battery'])}")
        print(f"   GNSS gaps: to Pi {gap(c['gnss'], c['pi']):6.1f}, to power elec {gap(c['gnss'], c['power']):6.1f}, "
              f"to compute power {gap(c['gnss'], c['cpower']):6.1f}; Pi-power elec {gap(c['pi'], c['power']):6.1f}")
        print("   cable proxy (Manhattan XY from Pi centre): " + ", ".join(f"{k} {v:5.0f}" for k, v in cp.items())
              + f"  sum {sum(cp.values()):5.0f}")
        print(f"   electronics CoM (placeholder masses): X {cx:+6.1f}, Y {cy:6.1f} ({cy / depth:.2f} of depth)")

    print("\n== lid / port screen (D-006 working hinge: inset 0, height 0; gap 2; port zone Z 4-19; plug 45) ==")
    for T, why in ((25.0, "working"), (31.5, "B.1 V1"), (42.5, "B.2 Concept C")):
        low = {a: lid_low(T, a) for a in (105, 120, 135)}
        print(f"  T {T:5.1f} ({why:<14}) lid low Z in plug corridor: 105 {low[105]:6.2f} | 120 {low[120]:6.2f} | 135 {low[135]:6.2f}"
              f"; plug clearance at 135 {plug_clear(T, 135):7.2f}; port top allowed {low[135] - MIN_GAP:6.2f}"
              f"; max angle for Z<=19 zone {max_angle(T):5.1f}; hinge height needed at 135 {needed_h(T):5.1f}")
    print("  closed form (axis inset 0 at height h; lid rests at H + G closed; theta > 90; plug long enough):")
    print("    z_low = H + h + (G + T - h) cos(theta)")
    print(f"  -> H 40, h 0, theta 135, need z_low >= port top 19 + MIN_GAP: G + T <= {(H0 - 19 - MIN_GAP) / math.sqrt(0.5):.2f}"
          f" (T <= {(H0 - 19 - MIN_GAP) / math.sqrt(0.5) - G:.2f})")
    for H in (40, 47.5):
        print(f"  body height {H}: T 31.5 clearance at 135 {plug_clear(31.5, 135, H=H):6.2f}; T 42.5 {plug_clear(42.5, 135, H=H):6.2f}")
    for plug in (15.0, 20.0, 45.0):
        print(f"  plug length {plug:g}: at 135 lid low Z / true clearance to zone, T 25 / 31.5 / 42.5: "
              + ", ".join(f"{lid_low(T, 135, plug=plug):6.2f}/{plug_clear(T, 135, plug=plug):5.2f}" for T in (25, 31.5, 42.5)))


if __name__ == "__main__":
    main()
