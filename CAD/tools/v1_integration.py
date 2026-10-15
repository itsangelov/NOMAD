"""NOMAD Virtual V1 integration model: layout, clearances, kinematics, hinge torque, mass / CG, stability,
thermal, harness and DFM checks (standard library only, no side effects).

  py CAD/tools/v1_integration.py           print the full integration report
  py CAD/tools/v1_integration.py --check   same, exit 1 if any check FAILS (WARN items do not fail)

Inputs:
  CAD/parameters/nomad.yaml        V1 master (D-002), resolved by yaml_to_featurescript.resolve()
  prototypes/V1/v1_hardware.py     candidate hardware (dimensions, masses, sources)
  prototypes/V1/v1_power.py        power states and heat split (imports the E-POWER calculators)
Method references: Round C base layout (base_v01_layout.py), D-010 Phase 2 kinematics / wind / tipping model
(d010_phase2_study.py, re-implemented here for the V1 geometry and masses), SB-261 B1 hinge rail (prototypes/B1_SB261).

World frame (as Round C / D-010): origin at the base bottom-front edge on the centreline, +X right, +Y rear (toward the
display hinge), +Z up. Closed-lid frame = world frame with the lid closed (phi = 0).
Every box is an ENVELOPE or KEEP-OUT, not detailed geometry. Results are CALC / modelled; nothing is measured.
Evidence tags in the report: MFR, 3P, EST, ASSUMED, CALC, REPO, YAML.
"""
import importlib.util
import math
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from yaml_to_featurescript import YAML_PATH, flatten, parse_restricted_yaml, resolve, validate  # noqa: E402


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


HWM = _load(ROOT / "prototypes" / "V1" / "v1_hardware.py", "v1_hardware")
PWR = _load(ROOT / "prototypes" / "V1" / "v1_power.py", "v1_power")
HW = HWM.HW

_params = flatten(parse_restricted_yaml(YAML_PATH.read_text(encoding="utf-8")))
_errors = validate(_params)
_res, _unres = resolve(_params)
P = {k: v for k, (v, _) in _res.items()}
BASIS = {k: b for k, (_, b) in _res.items()}

G = 9.81
DEG = math.pi / 180
RESULTS = []          # (section, name, status PASS/WARN/FAIL/INFO, detail)


def rec(section, name, ok, detail, warn=False):
    st = "PASS" if ok else ("WARN" if warn else "FAIL")
    RESULTS.append((section, name, st, detail))
    return ok


def info(section, name, detail):
    RESULTS.append((section, name, "INFO", detail))


# =====================================================================================================================
# 1. ENVELOPE AND LAYOUT (all coordinates are expressions over YAML parameters + named layout allowances)
# =====================================================================================================================
W, D, H = P["BODY_WIDTH"], P["BODY_DEPTH"], P["BODY_HEIGHT"]
WT, PT, MP = P["WALL_THICKNESS"], P["SERVICE_PANEL_THICKNESS"], P["MOUNT_PLATE_THICKNESS"]
GAP = P["MIN_GAP"]
IX = W / 2 - WT                      # inner side-wall face
IY0, IY1 = WT, D - WT                # inner front / rear wall faces
IZ0, IZ1 = PT, H - WT                # top of the bottom panel / underside of the deck

# Input devices (D-003: centred)
TPX = P["TRACKPAD_WIDTH"] / 2
TPY0 = P["BASE_FRONT_MARGIN"]
TPY1 = TPY0 + P["TRACKPAD_DEPTH"]
TPZ1 = H - P["TRACKPAD_TOP_RECESS"]
TPZ0 = TPZ1 - P["TRACKPAD_THICKNESS"]
KBX = P["KEYBOARD_WIDTH"] / 2
KBY0 = TPY1 + P["TRACKPAD_KEYBOARD_GAP"]
KBY1 = KBY0 + P["KEYBOARD_DEPTH"]
KBZ1 = H - P["KEYBOARD_TOP_RECESS"]
KBZ0 = KBZ1 - P["KEYBOARD_THICKNESS"]
KTZ0 = KBZ0 - MP                     # keyboard tray underside: ceiling of the under-keyboard zone
KTY0, KTY1 = KBY0 - P["INPUT_TRAY_LIP"], KBY1 + P["INPUT_TRAY_LIP"]
TTZ0 = TPZ0 - MP
BHX0 = TPX + P["TRACKPAD_BAY_MARGIN"]  # bulkhead inner face (trackpad side)
BHX1 = BHX0 + WT
PALM_Y1 = KTY0                       # palm bays end where the keyboard tray starts (full height only in front of it)

# Hardware envelopes (dimensions from v1_hardware / YAML)
PIW = P["PI_WIDTH"] + 2 * P["PI_ENVELOPE_MARGIN"]
PID = P["PI_DEPTH"] + 2 * P["PI_ENVELOPE_MARGIN"]
PIH = P["PI_STACK_HEIGHT"]
FAN = P["COOLING_FAN_SIZE"]
FANT = P["COOLING_FAN_THICKNESS"]
BBW, BBD, BBH = P["BATTERY_BAY_WIDTH"], P["BATTERY_BAY_DEPTH"], P["BATTERY_BAY_HEIGHT"]
PACKW, PACKD, PACKH = HW["PACK"]["dims"]
PEW, PED, PEH = P["POWER_ELEC_WIDTH"], P["POWER_ELEC_DEPTH"], P["POWER_ELEC_HEIGHT"]
CPW, CPD, CPH = P["COMPUTE_POWER_WIDTH"], P["COMPUTE_POWER_DEPTH"], P["COMPUTE_POWER_HEIGHT"]
DCW, DCD, DCH = P["DISPLAY_CONTROLLER_WIDTH"], P["DISPLAY_CONTROLLER_DEPTH"], P["DISPLAY_CONTROLLER_THICKNESS"]
GNW, GND, GNH = P["GNSS_MODULE_WIDTH"], P["GNSS_MODULE_DEPTH"], P["GNSS_MODULE_HEIGHT"]
HMW, HMD = P["HINGE_MOUNT_WIDTH"], P["HINGE_MOUNT_DEPTH"]
STANDOFF = 1.0                       # EST standoff / foam height under boards on the panel (layout allowance)
PLUG = 22.0                          # EST straight USB-A / micro-HDMI / USB-C plug + strain relief beyond the port face
CTRL_CONN = 2.0                      # EST connector overhang allowance around the Beck board (each side)

# Pi stack (V1 orientation, Phase 7): USB/Ethernet edge faces -X (the bulkhead), micro-HDMI / USB-C edge faces +Y.
#  -> internal USB plugs (keyboard, trackpad, 2 external USB extensions) pass through bulkhead openings into the empty
#     volume under the trackpad; HDMI / power plugs go rearward under the keyboard tray (low Z).
PI_X1 = IX - GAP                     # +X side (PCIe FPC side) 1 mm from the right wall
PI_X0 = PI_X1 - PIW
PI_Y1 = PALM_Y1 - GAP
PI_Y0 = PI_Y1 - PID
PI_Z0 = IZ0                          # compute sled = 2.5 mm insert plate flush in a main-panel pocket (V1 DFM / height fix)
PI_Z1 = PI_Z0 + PIH
PCB_Z = PI_Z0 + 3.0                  # EST: M2.5 standoff 3 under the Pi PCB
FAN_Y0 = IY0                         # fan frame seated in the front-right corner (wall contact by design)
FAN_Z0 = IZ0 + GAP

BOXES = []   # (name, cat, x0, x1, y0, y1, z0, z1)
# categories: S structure | E component envelope | K internal keep-out | C cable corridor | W wall zone (opening) |
#             X external keep-out


def box(name, cat, x0, x1, y0, y1, z0, z1):
    BOXES.append((name, cat, min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1), min(z0, z1), max(z0, z1)))


# ---- structure (S): shell walls, deck, bulkheads, trays, panels, hinge corner blocks
box("SHELL_WALL_FRONT", "S", -W / 2, W / 2, 0, WT, 0, H)
box("SHELL_WALL_REAR", "S", -W / 2, W / 2, D - WT, D, 0, H)
box("SHELL_WALL_LEFT", "S", -W / 2, -IX, WT, D - WT, 0, H)
box("SHELL_WALL_RIGHT", "S", IX, W / 2, WT, D - WT, 0, H)
box("SHELL_DECK_FRONT_L", "S", -IX, -TPX - P["CLEARANCE"], WT, KBY0 - P["CLEARANCE"], IZ1, H)   # palm rest left
box("SHELL_DECK_FRONT_R", "S", TPX + P["CLEARANCE"], IX, WT, KBY0 - P["CLEARANCE"], IZ1, H)     # palm rest right
box("SHELL_DECK_FRONT_C", "S", -TPX - P["CLEARANCE"], TPX + P["CLEARANCE"], WT, TPY0 - P["CLEARANCE"], IZ1, H)
box("SHELL_DECK_REAR", "S", -IX, IX, KBY1 + P["CLEARANCE"], D - WT, IZ1, H)                      # rear strip (GNSS window)
box("BULKHEAD_L", "S", -BHX1, -BHX0, WT, PALM_Y1, IZ0, IZ1)
box("BULKHEAD_R", "S", BHX0, BHX1, WT, PALM_Y1, IZ0, IZ1)
box("KEYBOARD_TRAY", "S", -IX + P["CLEARANCE"], IX - P["CLEARANCE"], KTY0, KTY1, KTZ0, KBZ0)
box("TRACKPAD_TRAY", "S", -BHX0 + P["CLEARANCE"], BHX0 - P["CLEARANCE"], TPY0 - P["INPUT_TRAY_LIP"],
    TPY1 + P["INPUT_TRAY_LIP"], TTZ0, TPZ0)
box("SERVICE_PANEL_MAIN", "S", -IX, IX, PALM_Y1, D - WT, 0, PT)                  # rear part: whole width under the keyboard
box("SERVICE_PANEL_FRONT", "S", -BHX0, IX, WT, PALM_Y1, 0, PT)                   # front part: trackpad + compute bays
box("BATTERY_DOOR", "S", -IX, -BHX0 - GAP, WT, PALM_Y1, 0, PT)
box("HINGE_BLOCK_L", "S", -IX, -IX + HMW, D - WT - HMD, D - WT, KTZ0, IZ1)      # above the under-keyboard zone: Z band
box("HINGE_BLOCK_R", "S", IX - HMW, IX, D - WT - HMD, D - WT, KTZ0, IZ1)
box("COMPUTE_SLED", "S", PI_X0, PI_X1, PI_Y0, PI_Y1, 0, PT)                      # insert plate in the front panel pocket

# ---- envelopes (E)
box("ENV_KEYBOARD", "E", -KBX, KBX, KBY0, KBY1, KBZ0, KBZ1)
box("ENV_TRACKPAD", "E", -TPX, TPX, TPY0, TPY1, TPZ0, TPZ1)
box("ENV_PI_STACK", "E", PI_X0, PI_X1, PI_Y0, PI_Y1, PI_Z0, PI_Z1)
box("ENV_FAN", "E", IX - FANT, IX, FAN_Y0, FAN_Y0 + FAN, FAN_Z0, FAN_Z0 + FAN)
bx0 = -IX + (IX - BHX1 - BBW) / 2                 # battery bay centred in the left palm bay
box("ENV_BATTERY_BAY", "E", bx0, bx0 + BBW, IY0 + GAP, IY0 + GAP + BBD, IZ0, IZ0 + BBH)
box("BATTERY_BAY_REAR_WALL", "S", -IX, -BHX1, IY0 + GAP + BBD + GAP, IY0 + GAP + BBD + GAP + WT, IZ0, IZ1)
UKZ0 = IZ0 + STANDOFF                             # under-keyboard boards sit on standoffs on the main panel
BTN_Y0 = KTY0 + GAP + PED + 2.0                   # button behind the power board on the left wall
box("ENV_POWER_ELEC", "E", -IX + GAP, -IX + GAP + PEW, KTY0 + GAP, KTY0 + GAP + PED, UKZ0, UKZ0 + PEH)
dcx0 = -DCW / 2 - CTRL_CONN
box("ENV_DISPLAY_CTRL", "E", dcx0, dcx0 + DCW + 2 * CTRL_CONN, KBY1 - DCD - 2 * CTRL_CONN - 14.0, KBY1 - 14.0,
    UKZ0, UKZ0 + DCH + CTRL_CONN)
cpx1 = IX - GAP
box("ENV_COMPUTE_POWER", "E", cpx1 - CPW, cpx1, PI_Y1 + PLUG + GAP, PI_Y1 + PLUG + GAP + CPD, UKZ0, UKZ0 + CPH)
gx0 = -GNW - 12.0                                 # GNSS left of the centreline display-cable riser
box("ENV_GNSS", "E", gx0, gx0 + GNW, D - WT - GAP - GND, D - WT - GAP, UKZ0, UKZ0 + GNH)

box("ENV_BUTTON", "E", -IX, -IX + 25.0, BTN_Y0, BTN_Y0 + 14, UKZ0 + 2, UKZ0 + 16)         # 12 mm panel button body (EST)
box("ENV_USB_EXT_SOCKETS", "E", BHX1 + 12, BHX1 + 12 + 34, IY0, IY0 + 20, IZ0 + 4, IZ0 + 18)  # 2 panel-mount USB-A (EST)
# ---- internal keep-outs (K)
box("KEEPOUT_PI_USB_PLUGS", "K", PI_X0 - PLUG - (BHX1 - BHX0) - GAP, PI_X0, PI_Y0 + 6, PI_Y1 - 6, PCB_Z, PCB_Z + 16.5)
box("KEEPOUT_PI_REAR_PLUGS", "K", PI_X1 - 60.0, PI_X1 - 8.0, PI_Y1, PI_Y1 + PLUG, PCB_Z, PCB_Z + 8.0)
box("KEEPOUT_GNSS_SKY", "K", gx0 + 8, gx0 + 8 + 20 + 2 * P["GNSS_ANTENNA_KEEPOUT"], KTY1 + GAP,
    D - WT, UKZ0 + GNH, IZ1)                       # patch sky window: nothing (esp. metal) between patch and deck
box("KEEPOUT_FAN_INLET", "K", IX - FANT - 6.0, IX - FANT, FAN_Y0, FAN_Y0 + FAN, FAN_Z0, FAN_Z0 + FAN)

# ---- wall zones (W): openings in walls (may overlap the shell)
box("W_PORT_USB_C_LEFT", "W", -W / 2, -IX, KTY0 + 10, KTY0 + 22, UKZ0 + 3, UKZ0 + 11)
box("W_BUTTON_LEFT", "W", -W / 2, -IX, BTN_Y0, BTN_Y0 + 14, UKZ0 + 2, UKZ0 + 16)
box("W_EXHAUST_FAN_R", "W", IX, W / 2, FAN_Y0, FAN_Y0 + FAN, FAN_Z0, FAN_Z0 + FAN)
box("W_USB_EXT_FRONT_R", "W", BHX1 + 12, BHX1 + 12 + 34, 0, WT, IZ0 + 4, IZ0 + 18)
box("W_INTAKE_REAR", "W", -60.0, 60.0, D - WT, D, UKZ0 + 2, KTZ0 - 2)
box("W_DISPLAY_PASS", "W", -10.0, 10.0, D - WT, D, KTZ0 + 2, IZ1)

# ---- cable corridors (C) - reserved routes, sized by the harness table
CW, CH = P["CABLE_CORRIDOR_WIDTH"], P["CABLE_CORRIDOR_HEIGHT"]
box("C_DISPLAY_RISER", "C", -CW / 2, CW / 2, KBY1 - 14.0, D - WT, UKZ0, UKZ0 + CH)
box("C_REAR_TRUNK", "C", -IX + HMW + GAP, IX - HMW - GAP, KBY1 - 14.0 - CW, KBY1 - 14.0, UKZ0 + DCH + CTRL_CONN + GAP,
    UKZ0 + DCH + CTRL_CONN + GAP + 3.5)                                     # flat trunk (ribbon / flat bundle) over the controller
box("C_PI_TO_UNDERKB", "C", PI_X0, PI_X1 - 60.0 - GAP, PI_Y1, KTY0 + 40.0, UKZ0, UKZ0 + CH)
box("C_BATTERY", "C", -IX + GAP, -IX + GAP + 20.0, IY0 + GAP + BBD + GAP + WT, KTY0 + GAP, UKZ0, UKZ0 + 8.0)

INTERFACES = {   # designed contacts / served entries (allowed to touch or overlap)
    frozenset(("ENV_KEYBOARD", "KEYBOARD_TRAY")), frozenset(("ENV_TRACKPAD", "TRACKPAD_TRAY")),
    frozenset(("ENV_PI_STACK", "COMPUTE_SLED")), frozenset(("ENV_PI_STACK", "KEEPOUT_PI_USB_PLUGS")),
    frozenset(("ENV_PI_STACK", "KEEPOUT_PI_REAR_PLUGS")), frozenset(("ENV_FAN", "KEEPOUT_FAN_INLET")),
    frozenset(("ENV_FAN", "SHELL_WALL_RIGHT")), frozenset(("KEEPOUT_PI_USB_PLUGS", "BULKHEAD_R")),
    frozenset(("ENV_GNSS", "KEEPOUT_GNSS_SKY")), frozenset(("KEEPOUT_GNSS_SKY", "SHELL_DECK_REAR")),
    frozenset(("KEEPOUT_GNSS_SKY", "SHELL_WALL_REAR")), frozenset(("ENV_BATTERY_BAY", "BATTERY_DOOR")),
    frozenset(("COMPUTE_SLED", "SERVICE_PANEL_FRONT")), frozenset(("ENV_PI_STACK", "SERVICE_PANEL_FRONT")),
    frozenset(("ENV_FAN", "SHELL_WALL_FRONT")), frozenset(("ENV_BUTTON", "SHELL_WALL_LEFT")),
    frozenset(("ENV_USB_EXT_SOCKETS", "SHELL_WALL_FRONT")), frozenset(("KEEPOUT_FAN_INLET", "SHELL_WALL_FRONT")),
    frozenset(("C_DISPLAY_RISER", "ENV_DISPLAY_CTRL")), frozenset(("C_DISPLAY_RISER", "SHELL_WALL_REAR")),
    frozenset(("C_REAR_TRUNK", "C_DISPLAY_RISER")), frozenset(("C_PI_TO_UNDERKB", "KEEPOUT_PI_REAR_PLUGS")),
    frozenset(("C_PI_TO_UNDERKB", "ENV_PI_STACK")), frozenset(("C_BATTERY", "ENV_POWER_ELEC")),
    frozenset(("C_BATTERY", "BATTERY_BAY_REAR_WALL")),
}


def overlap(a, b):
    return all(a[2 + 2 * i] < b[3 + 2 * i] and b[2 + 2 * i] < a[3 + 2 * i] for i in range(3))


def gap(a, b):
    d = [max(0.0, a[2 + 2 * i] - b[3 + 2 * i], b[2 + 2 * i] - a[3 + 2 * i]) for i in range(3)]
    return math.sqrt(sum(x * x for x in d))


def check_layout():
    S = "7 layout"
    inner = (-IX, IX, IY0, IY1, IZ0, IZ1)
    for b in BOXES:
        if b[1] in ("E", "K", "C") and b[0] not in ("ENV_KEYBOARD", "ENV_TRACKPAD"):
            inside = (b[2] >= -IX - 1e-9 and b[3] <= IX + 1e-9 and b[4] >= IY0 - 1e-9 and b[5] <= IY1 + 1e-9
                      and b[6] >= IZ0 - 1e-9 and b[7] <= IZ1 + 1e-9)
            rec(S, f"{b[0]} inside the shell interior", inside, f"x {b[2]:.1f}..{b[3]:.1f} y {b[4]:.1f}..{b[5]:.1f} "
                f"z {b[6]:.1f}..{b[7]:.1f} vs interior {inner[0]:.1f}..{inner[1]:.1f} / {inner[2]:.1f}..{inner[3]:.1f} / "
                f"{inner[4]:.1f}..{inner[5]:.1f}")
    viol, pairs = [], 0
    for i, a in enumerate(BOXES):
        for b in BOXES[i + 1:]:
            if a[1] == "W" or b[1] == "W":
                continue
            if a[1] == "S" and b[1] == "S":
                continue
            pairs += 1
            key = frozenset((a[0], b[0]))
            if key in INTERFACES:
                continue
            g = gap(a, b)
            need = 0.0 if "C" in (a[1], b[1]) or ("S" in (a[1], b[1]) and "K" in (a[1], b[1])) else GAP
            if {a[0], b[0]} & {"ENV_KEYBOARD", "ENV_TRACKPAD"} and (a[0].startswith("SHELL_DECK") or b[0].startswith("SHELL_DECK")):
                need = P["CLEARANCE"]                     # designed deck-opening fit (0.3)
            if overlap(a, b) or g < need - 1e-9:
                viol.append(f"{a[0]} / {b[0]}: gap {g:.2f} (need {need:.1f})")
    rec(S, "pairwise clearance (no overlap; >= MIN_GAP between envelopes, structure and keep-outs; corridors may touch)",
        not viol, f"{pairs} pairs checked; " + ("0 violations" if not viol else "; ".join(viol[:12])))
    # under-keyboard height budget
    ukz = KTZ0 - IZ0
    tallest = max((b for b in BOXES if b[1] == "E" and b[0] != "ENV_KEYBOARD" and b[5] > KTY0 and b[4] < KTY1
                   and b[0] not in ("ENV_PI_STACK", "ENV_BATTERY_BAY", "ENV_FAN")),
                  key=lambda b: b[7])
    rec(S, "under-keyboard height budget", tallest[7] <= KTZ0 - GAP + 1e-9,
        f"free height {ukz:.1f} (panel top z {IZ0} .. tray underside z {KTZ0:.1f}); tallest {tallest[0]} top z {tallest[7]:.1f}")
    # palm-bay height for battery and Pi
    rec(S, "battery bay fits the left palm bay (height, width, depth)",
        BBH <= IZ1 - IZ0 and BBW <= IX - BHX1 and IY0 + GAP + BBD + GAP + WT <= PALM_Y1,
        f"bay {BBW} x {BBD} x {BBH} in palm bay {IX - BHX1:.1f} x {PALM_Y1 - IY0:.1f} x {IZ1 - IZ0:.1f}; "
        f"pack {PACKW} x {PACKD} x {PACKH} (holder build, E-POWER-002) leaves {BBW - PACKW:.1f} / {BBD - PACKD:.1f} / {BBH - PACKH:.1f}")
    stack = 3.0 + 1.6 + 16.0 + 1.6 + HW["SSD"]["dims"][2] + 1.5
    rec(S, "Pi stack estimate inside PI_STACK_HEIGHT", stack <= PIH,
        f"standoff 3 + Pi PCB 1.6 + 16 header (Active Cooler 13.7 inside it, MFR) + HAT+ 1.6 + SSD {HW['SSD']['dims'][2]} + "
        f"screw heads 1.5 = {stack:.1f} EST vs envelope {PIH} (YAML working); USB stack top = PCB + ~16 (MFR-DWG class) "
        f"= z {PCB_Z + 1.6 + 16:.1f} < envelope top z {PI_Z1:.1f}")
    rec(S, "Pi envelope below the deck", PI_Z1 <= IZ1 - GAP + 1e-9, f"stack top z {PI_Z1:.1f}, deck underside z {IZ1:.1f}")
    hat_top = PCB_Z + 1.6 + 16.0 + 1.6
    rec(S, "GPIO harness connectors on the HAT+ pass-through header stay below the deck (right-angle housings)",
        hat_top + 8.0 <= IZ1 - GAP and hat_top + 14.0 > IZ1,
        f"HAT+ top z {hat_top:.1f}: a vertical 2.54 mm Dupont housing (14) reaches z {hat_top + 14:.1f} > deck underside "
        f"{IZ1} -> SPEC right-angle housings (8 EST, top z {hat_top + 8:.1f}) or soldered leads (audit 2026-10-06)")
    rec(S, "Pi rear plugs pass under the keyboard tray", PCB_Z + 8.0 <= KTZ0 - GAP,
        f"micro-HDMI / USB-C plug zone top z {PCB_Z + 8:.1f} vs tray underside {KTZ0:.1f}")
    rec(S, "Pi USB plugs fit the volume under the trackpad tray", PCB_Z + 16.5 <= TTZ0 - GAP,
        f"USB plug zone top z {PCB_Z + 16.5:.1f} vs trackpad tray underside z {TTZ0:.1f} (straight plugs, cables turn forward/rearward)")
    rec(S, "GNSS patch is behind the keyboard (sky strip, no keyboard metal above)", BOXES_D["KEEPOUT_GNSS_SKY"][4] >= KBY1,
        f"sky window y {BOXES_D['KEEPOUT_GNSS_SKY'][4]:.1f}..{D - WT:.1f} ({D - WT - BOXES_D['KEEPOUT_GNSS_SKY'][4]:.1f} deep), keyboard tray rear y {KTY1:.1f}; "
        "patch must be on the rear half of the module (orientation at assembly)", warn=True)
    # service access: straight-down removal footprints
    panels = {"BATTERY_DOOR": ("BATTERY_DOOR",), "MAIN": ("SERVICE_PANEL_MAIN", "SERVICE_PANEL_FRONT")}
    for name, panel in (("ENV_BATTERY_BAY", "BATTERY_DOOR"), ("ENV_PI_STACK", "MAIN"),
                        ("ENV_POWER_ELEC", "MAIN"), ("ENV_DISPLAY_CTRL", "MAIN"),
                        ("ENV_COMPUTE_POWER", "MAIN"), ("ENV_GNSS", "MAIN"), ("ENV_FAN", "MAIN")):
        e = BOXES_D[name]
        inside = True
        for xs in (e[2] + 1e-3, e[3] - 1e-3):
            for ys in (e[4] + 1e-3, e[5] - 1e-3):
                inside &= any(BOXES_D[q][2] <= xs <= BOXES_D[q][3] and BOXES_D[q][4] <= ys <= BOXES_D[q][5] for q in panels[panel])
        below = [b[0] for b in BOXES if b[1] in ("E", "S") and b[0] not in (name, "COMPUTE_SLED") + panels[panel] and overlap(
            (0, 0, e[2], e[3], e[4], e[5], 0.0, e[6]), b) and b[7] > PT + 1e-6]
        rec(S, f"service: {name} removable downward through {'/'.join(panels[panel])}", inside and not below,
            ("footprint inside the opening" if inside else "footprint NOT inside the panel") +
            ("; nothing in the way" if not below else f"; blocked by {below}"))
    # power board USB-C reaches the left wall
    pe = BOXES_D["ENV_POWER_ELEC"]
    rec(S, "USB-C receptacle on the power board reaches the left wall", abs(pe[2] - (-IX)) <= GAP + 1e-6,
        f"board edge x {pe[2]:.1f}, wall inner face x {-IX:.1f}")


BOXES_D = {}


def build_index():
    BOXES_D.clear()
    for b in BOXES:
        BOXES_D[b[0]] = b


# =====================================================================================================================
# 2. LID, LEAF, KINEMATICS
# =====================================================================================================================
HAY = D - P["HINGE_AXIS_OFFSET"]
HAZ = H + P["HINGE_AXIS_HEIGHT"]
ZF = H + P["LID_CLOSED_GAP"]                          # closed-lid display face
CORE, AIRG, LEAFT = P["LID_CORE_THICKNESS"], P["SOLAR_LEAF_AIR_GAP"], P["SOLAR_LEAF_THICKNESS"]
LIDT = P["LID_THICKNESS"]
ZL0 = ZF + CORE + AIRG                                 # leaf underside (closed)
LAX = (P["SOLAR_LEAF_HINGE_AXIS_INSET"], ZF + CORE + P["SOLAR_LEAF_HINGE_AXIS_HEIGHT"])   # leaf axis (y, z), closed frame
DSP_H = P["DISPLAY_HEIGHT"]
DSP_YC = D / 2 - P["DISPLAY_VERTICAL_OFFSET"]
DSP_Y0, DSP_Y1 = DSP_YC - DSP_H / 2, DSP_YC + DSP_H / 2
DSP_Z0 = ZF + P["DISPLAY_BEZEL_LIP"]
DSP_Z1 = DSP_Z0 + P["DISPLAY_THICKNESS"]
FOOT_H, FOOT_IN = 4.0, 8.0                            # ASSUMED rubber feet (as D-010 Phase 2)
STAY_X = W / 2 - P["STAY_PIVOT_INSET_X"]
STAY_Y0 = D - P["STAY_PIVOT_INSET_Y"]
STAY_FOOT_Y = STAY_Y0 + P["SOLAR_STAY_REACH"]


def rot_x(p, a, yc, zc):
    c, s = math.cos(a * DEG), math.sin(a * DEG)
    dy, dz = p[1] - yc, p[2] - zc
    return (p[0], yc + c * dy - s * dz, zc + s * dy + c * dz)


def rot_v(v, a):
    c, s = math.cos(a * DEG), math.sin(a * DEG)
    return (v[0], c * v[1] - s * v[2], s * v[1] + c * v[2])


def to_world(body, p, phi, psi):
    if body in ("base", "stay"):
        return p
    if body == "leaf":
        p = rot_x(p, psi, LAX[0], LAX[1])
    return rot_x(p, -phi, HAY, HAZ)


def to_world_vec(body, v, phi, psi):
    if body == "leaf":
        v = rot_v(v, psi)
    return rot_v(v, -phi)


def check_lid():
    S = "8/9 lid and leaf"
    rec(S, "display-free band for the SB-261 leaf hinge rail", DSP_Y0 >= P["DISPLAY_FREE_BAND"] - 1e-9,
        f"display y {DSP_Y0:.1f}..{DSP_Y1:.1f} in a {D:.0f} deep lid; band needed {P['DISPLAY_FREE_BAND']} (REPO)")
    room = CORE - P["DISPLAY_BEZEL_LIP"] - P["DISPLAY_THICKNESS"] - 2.5
    rec(S, "lid core holds the display (lip + panel + back shell)", room >= GAP,
        f"core {CORE}: lip {P['DISPLAY_BEZEL_LIP']} + panel {P['DISPLAY_THICKNESS']} + back shell 2.5 leaves {room:.2f} for "
        "the eDP cable, foam and ribs (controller now in the base)")
    rec(S, "display width inside the lid side walls", P["DISPLAY_WIDTH"] <= W - 2 * WT - 2 * GAP,
        f"panel {P['DISPLAY_WIDTH']} vs {W - 2 * WT - 2 * GAP:.1f}")
    rec(S, "panel inside the leaf frame and the leaf inside the lid footprint",
        P["SOLAR_LEAF_WIDTH"] <= W and P["SOLAR_PANEL_DEPTH"] + 2 * 8 <= P["SOLAR_LEAF_DEPTH"],
        f"leaf {P['SOLAR_LEAF_WIDTH']} x {P['SOLAR_LEAF_DEPTH']} on a {W:.0f} x {D:.0f} lid; panel {P['SOLAR_PANEL_WIDTH']} x "
        f"{P['SOLAR_PANEL_DEPTH']}")
    rec(S, "SB-261 leaf hinges inside the leaf width", P["SOLAR_LEAF_HINGE_SPACING"] / 2 + 33.8 / 2 <= P["SOLAR_LEAF_WIDTH"] / 2 - 8,
        f"hinge outer end x {P['SOLAR_LEAF_HINGE_SPACING'] / 2 + 16.9:.1f} vs frame inner x {P['SOLAR_LEAF_WIDTH'] / 2 - 8:.1f}")
    info(S, "B1 leaf geometry", f"SB-261 rail axis (y {LAX[0]}, z {LAX[1]:.1f}) = the scratch-validated rail (axis z 63.5, "
         "lid back z 61): unchanged, because LID_CORE 19 and LID_CLOSED_GAP 2 are unchanged. 0-190 deg, R12 sleeve, "
         "first contact 201 deg are REPO kernel results and still apply")
    # lid sweep: rear face has no plugs; check the lid vs the table plane, stay arms and the base at phi max
    zmin, worst = 1e9, None
    for phi in range(0, int(P["LID_ANGLE_MAX"]) + 1, 5):
        for y in (0.0, D):
            for z in (ZF, ZF + LIDT):                 # display face .. stowed-leaf outer face (whole lid stack)
                w = to_world("lid", (0.0, y, z), phi, 0)
                if w[1] > D - 1 and w[2] < zmin:
                    zmin, worst = w[2], (phi, w)
    rec(S, "lid sweep behind the base clears the table and the deployed stay (no rear plugs in V1)",
        zmin > -FOOT_H + 5.0, f"lowest lid point behind the base z {zmin:.1f} at phi {worst[0]} (y {worst[1][1]:.1f}); "
        f"table z {-FOOT_H}; stay arms z {-FOOT_H}..{-FOOT_H + 3}")
    old_plug_top = 19.0
    info(S, "rear-port conflict (D-007 / Round C)", f"RESOLVED by relocation: with the old rear connector zone (top z "
         f"{old_plug_top}) this lid (T {LIDT}) would be hit at phi 135 (lid corner z {zmin:.1f} < {old_plug_top}); V1 has "
         "no rear plugs (USB-C power and button on the left wall, USB on the front-right wall, exhaust on the right wall)")
    # leaf vs table at large lid angles
    touch = []
    for phi in (110, 120, 125, 130, 135):
        bad = []
        for psi in range(0, 191, 5):
            zm = min(to_world("leaf", (x, y, z), phi, psi)[2] for x in (0.0,) for y in (0.0, D)
                     for z in (ZL0, ZL0 + LEAFT))
            if zm < -FOOT_H + 1.0:
                bad.append(psi)
        if bad:
            touch.append(f"phi {phi}: psi {min(bad)}-{max(bad)}")
    rec(S, "leaf free edge clears the table over 0-190 deg", not touch,
        "contact with the table: " + ("; ".join(touch) if touch else "none") +
        " -> operating rule kept from D-010: above phi ~120 open the leaf before the lid (the leaf rests on the table, no "
        "damage path; a printed lid stop at 120 would remove it but costs solar aim)", warn=True)
    # display-hinge cable pass
    twist = P["LID_ANGLE_MAX"] / 60.0
    rec(S, "display-hinge cable pass twist rate (eDP micro-coax + solar lead, 60 mm axial twist zone)", twist <= 3.5,
        f"{P['LID_ANGLE_MAX']} deg over 60 mm = {twist:.2f} deg/mm <= 3.5 (D-010 ASSUMED limit)")


# =====================================================================================================================
# 3. MASS ITEMS AND PRINTED-PART MASSES
# =====================================================================================================================
RHO_PETG, RHO_ASA = 1.27e-3, 1.07e-3         # g/mm3 (EST)


def cen(name):
    b = BOXES_D[name]
    return ((b[2] + b[3]) / 2, (b[4] + b[5]) / 2, (b[6] + b[7]) / 2)


def printed_parts():
    """Printed part volumes (mm3) and masses (g), EST from the envelope model: thin walls are solid (perimeters),
    blocks 40 % infill. Returns list of (part, material, g, bed footprint x, y)."""
    kbo = (P["KEYBOARD_WIDTH"] + 2 * P["CLEARANCE"]) * (P["KEYBOARD_DEPTH"] + 2 * P["CLEARANCE"])
    tpo = (P["TRACKPAD_WIDTH"] + 2 * P["CLEARANCE"]) * (P["TRACKPAD_DEPTH"] + 2 * P["CLEARANCE"])
    deck = (W * D - kbo - tpo) * WT
    walls = 2 * (W + D) * H * WT
    bulk = 2 * (PALM_Y1 - WT) * (IZ1 - IZ0) * WT + (IX - BHX1) * (IZ1 - IZ0) * WT
    bosses = 18 * math.pi * (P["BOSS_DIAMETER"] / 2) ** 2 * (IZ1 - IZ0) * 0.6
    corner = 2 * HMW * HMD * (IZ1 - KTZ0) * 0.4
    vents_ribs = 0.08 * (deck + walls)
    shell = deck + walls + bulk + bosses + corner + vents_ribs
    panel = (2 * IX) * (IY1 - IY0) * PT * 1.10                        # main panel + door, 10 % ribs / grilles
    trays = ((2 * IX) * (KTY1 - KTY0) + (2 * BHX0) * (TPY1 - TPY0 + 6) + PIW * PID) * MP * 1.10
    # lid core: back shell 2.5, side walls, bezel skin 1.5 over the border ring, pocket walls, ribs, hinge blocks
    border = W * D - P["DISPLAY_ACTIVE_WIDTH"] * P["DISPLAY_ACTIVE_HEIGHT"]
    lid = (W * D * 2.5 + 2 * (W + D) * CORE * WT + border * 1.5 + 2 * (P["DISPLAY_WIDTH"] + DSP_H) * 5.0 * 1.2
           + 0.10 * W * D * 2.5 + 2 * 44 * 42 * CORE * 0.4 + 2 * HMW * 20 * CORE * 0.4)
    spacers = 0.012 / RHO_ASA * 1000 * 0                              # counted as an item (D-010 12 g)
    leaf = (P["SOLAR_LEAF_WIDTH"] * P["SOLAR_LEAF_DEPTH"] - (P["SOLAR_PANEL_WIDTH"] - 4) * (P["SOLAR_PANEL_DEPTH"] - 4)) * LEAFT
    out = [("base shell (walls, deck, bulkheads, bosses, hinge blocks)", "PETG", shell * RHO_PETG, W, D),
           ("service panel + battery door", "PETG", panel * RHO_PETG, W - 2 * WT, D - 2 * WT),
           ("keyboard tray, trackpad tray, compute sled", "PETG", trays * RHO_PETG, 2 * IX, KTY1 - KTY0),
           ("lid core (back shell, walls, bezel, ribs, hinge blocks)", "ASA", lid * RHO_ASA, W, D),
           ("leaf frame (open back)", "ASA", leaf * RHO_ASA + spacers, P["SOLAR_LEAF_WIDTH"], P["SOLAR_LEAF_DEPTH"])]
    return out


def mass_items():
    """(label, g, body, closed-frame point, tag)."""
    pp = {p[0]: p[2] for p in printed_parts()}
    base_c = (0.0, D / 2, H / 2)
    it = [
        ("base shell", pp["base shell (walls, deck, bulkheads, bosses, hinge blocks)"], "base", (0.0, D / 2, H * 0.6), "EST"),
        ("service panel + door", pp["service panel + battery door"], "base", (0.0, D / 2, PT / 2), "EST"),
        ("trays + sled", pp["keyboard tray, trackpad tray, compute sled"], "base", (0.0, (KTY0 + KTY1) / 2, KTZ0), "EST"),
        ("keyboard PERIBOARD-416", HW["KEYBOARD"]["mass_g"], "base", cen("ENV_KEYBOARD"), "MFR"),
        ("trackpad PERIPAD-501 II", HW["TRACKPAD"]["mass_g"], "base", cen("ENV_TRACKPAD"), "EST"),
        ("Pi 5 + Active Cooler + M.2 HAT+ + SSD", HW["PI5"]["mass_g"] + HW["COOLER"]["mass_g"] + HW["M2HAT"]["mass_g"]
         + HW["SSD"]["mass_g"], "base", cen("ENV_PI_STACK"), "EST"),
        ("battery cells 4 x M65A", 4 * HW["CELL"]["mass_g"], "base", cen("ENV_BATTERY_BAY"), "MFR"),
        ("pack hardware (holder, strip, BMS, fuse, lead)", HW["PACK"]["mass_g"], "base", cen("ENV_BATTERY_BAY"), "EST"),
        ("power board + 12 V regulator", HW["PWR_PCB"]["mass_g"] + HW["BB12"]["mass_g"], "base", cen("ENV_POWER_ELEC"), "EST"),
        ("5.1 V buck", HW["BUCK5"]["mass_g"], "base", cen("ENV_COMPUTE_POWER"), "EST"),
        ("display controller BTC-mini-eDP", HW["DCTRL"]["mass_g"], "base", cen("ENV_DISPLAY_CTRL"), "MFR"),
        ("GNSS pHAT", HW["GNSS"]["mass_g"], "base", cen("ENV_GNSS"), "EST"),
        ("enclosure fan", HW["FAN"]["mass_g"], "base", cen("ENV_FAN"), "EST"),
        ("button, USB extensions, HDMI cable", HW["BUTTON"]["mass_g"] + 2 * HW["USB_EXT"]["mass_g"] + HW["HDMI_CABLE"]["mass_g"],
         "base", (60.0, 60.0, 10.0), "EST"),
        ("fasteners, inserts, feet", HW["INSERTS"]["mass_g"], "base", base_c, "EST"),
        ("base harness (power, USB, fan, GNSS)", 0.6 * HW["WIRING"]["mass_g"], "base", (0.0, 150.0, 8.0), "EST"),
        ("display hinges, base leaves", HW["LID_HINGE"]["mass_g"], "base", (0.0, HAY - 10, HAZ - 8), "EST"),
        ("stay arms + pivots", HW["STAY"]["mass_g"], "stay", (0.0, STAY_Y0, -FOOT_H / 2), "EST"),
        # lid
        ("lid core (printed)", pp["lid core (back shell, walls, bezel, ribs, hinge blocks)"], "lid", (0.0, D / 2, ZF + CORE * 0.55), "EST"),
        ("display AUO G101UAN01.0", HW["DISPLAY"]["mass_g"], "lid", (0.0, DSP_YC, (DSP_Z0 + DSP_Z1) / 2), "EST"),
        ("eDP cable", HW["EDP_CABLE"]["mass_g"], "lid", (0.0, (DSP_Y1 + D) / 2, ZF + 10), "EST"),
        ("display hinges, lid leaves", HW["LID_HINGE"]["mass_g"], "lid", (0.0, HAY - 10, ZF + 6), "EST"),
        ("air-gap spacers + low-e foil", 12.0, "lid", (0.0, D / 2, ZF + CORE + 1), "REPO D-010"),
        ("leaf hinges SB-261 x2 (lid + leaf halves)", 2 * HW["LEAF_HINGE"]["mass_g"], "lid", (0.0, LAX[0], LAX[1]), "EST"),
        ("lid solar run + knuckle", 0.15 * HW["WIRING"]["mass_g"], "lid", (100.0, D / 2, ZF + 11), "EST"),
        # leaf
        ("P108 panel", HW["PANEL"]["mass_g"], "leaf", (0.0, D / 2, ZL0 + 2.0), "MFR"),
        ("leaf frame (printed)", pp["leaf frame (open back)"], "leaf", (0.0, D / 2, ZL0 + 2.5), "EST"),
        ("leaf latch + wiring + connector", 20.0, "leaf", (0.0, 14.0, ZL0 + 1.0), "REPO D-010"),
    ]
    return it


def cog(items, phi, psi, stay):
    m, s = 0.0, [0.0, 0.0, 0.0]
    for lab, g, body, p, _ in items:
        if body == "stay":
            q = (p[0], p[1] + (P["SOLAR_STAY_REACH"] / 2 if stay else -60.0), p[2])
        else:
            q = to_world(body, p, phi, psi)
        m += g
        for i in range(3):
            s[i] += g * q[i]
    return m, tuple(v / m for v in s)


# =====================================================================================================================
# 4. HINGE TORQUE (display lid), STABILITY (D-010 method)
# =====================================================================================================================
SOUTHCO_E6_MED = [("E6-10-208-50", 0.9), ("E6-10-212-50", 1.4), ("E6-10-216-50", 1.8), ("E6-10-220-50", 2.3)]  # MFR
HOLD_SF = 1.5               # ASSUMED holding factor on the gravity torque (as D-010)
TORQUE_TOL = 0.80           # MFR: torque within +-20 % over life -> design on the low bound
OPEN_FORCE_MAX = 25.0       # N at the lid free edge, ASSUMED ergonomic limit for two-handed opening
MISUSE_PUSH = 30.0          # N rearward at the lid free edge at phi max (ASSUMED misuse / handling case)


def lid_torque(phi, psi, items):
    """Gravity torque about the display hinge (N.m), + = tends to open further (lid falls back)."""
    t = 0.0
    for lab, g, body, p, _ in items:
        if body in ("lid", "leaf"):
            q = to_world(body, p, phi, psi)
            t += g / 1000 * G * (q[1] - HAY) / 1000
    return t


RHO_AIR, CN_MAX, CN_SLOPE = 1.2, 1.2, 2.5


def plates(phi, psi):
    out = [("base front/rear", W * H * 1e-6, (0.0, D / 2, H / 2), (0.0, 1.0, 0.0)),
           ("base side", D * H * 1e-6, (0.0, D / 2, H / 2), (1.0, 0.0, 0.0)),
           ("lid", W * D * 1e-6, to_world("lid", (0.0, D / 2, ZF + CORE / 2), phi, psi),
            to_world_vec("lid", (0, 0, 1), phi, psi))]
    if psi > 8.0:
        out.append(("leaf", P["SOLAR_LEAF_WIDTH"] * P["SOLAR_LEAF_DEPTH"] * 1e-6,
                    to_world("leaf", (0.0, D / 2, ZL0 + LEAFT / 2), phi, psi), to_world_vec("leaf", (0, 0, 1), phi, psi)))
    return out


def wind(phi, psi, v, beta, incl):
    b, g = beta * DEG, incl * DEG
    w = (math.cos(g) * math.sin(b), math.cos(g) * math.cos(b), math.sin(g))
    q = 0.5 * RHO_AIR * v * v
    out = []
    for _, a, c, n in plates(phi, psi):
        dn = sum(w[i] * n[i] for i in range(3))
        alpha = math.asin(max(-1.0, min(1.0, abs(dn))))
        f = q * a * min(CN_MAX, CN_SLOPE * abs(alpha)) * (1 if dn >= 0 else -1)
        out.append((c, tuple(f * n[i] for i in range(3))))
    return out


def support(stay):
    xi, y0, y1 = W / 2 - FOOT_IN, FOOT_IN, D - FOOT_IN
    pts = [(-xi, y0), (xi, y0), (xi, y1), (-xi, y1)]
    if stay:
        pts += [(-STAY_X, STAY_FOOT_Y), (STAY_X, STAY_FOOT_Y)]
    pts = sorted(set(pts))

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


def tip_m(point, force, e, m):
    r = (point[0] - e[0], point[1] - e[1], point[2] + FOOT_H)
    t = (-m[1], m[0], 0.0)
    cr = (r[1] * force[2] - r[2] * force[1], r[2] * force[0] - r[0] * force[2], r[0] * force[1] - r[1] * force[0])
    return (t[0] * cr[0] + t[1] * cr[1]) / 1000.0


def stability(items, phi, psi, stay):
    m, c = cog(items, phi, psi, stay)
    poly = support(stay)
    res = {}
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        ex, ey = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(ex, ey)
        mv = (ey / ln, -ex / ln)
        lab = "rear" if mv[1] > 0.7 else "front" if mv[1] < -0.7 else "right" if mv[0] > 0.7 else "left" if mv[0] < -0.7 else "corner"
        mg = tip_m(c, (0.0, 0.0, -m / 1000 * G), a, mv)
        margin = -mg / (m / 1000 * G) * 1000
        best = None
        beta0 = math.degrees(math.atan2(mv[0], mv[1]))
        for db in (-30.0, -15.0, 0.0, 15.0, 30.0):
            for inc in (-10.0, 0.0, 10.0):
                mw = sum(tip_m(p, f, a, mv) for p, f in wind(phi, psi, 1.0, beta0 + db, inc))
                if mw > 1e-9 and mg < 0:
                    v = math.sqrt(-mg / mw)
                    best = v if best is None else min(best, v)
        k = lab
        while k in res:
            k += "'"
        res[k] = (margin, best if mg < 0 else 0.0)
    return m, c, res


STATES = [("STOWED (closed)", 0, 0, False), ("DISPLAY OPEN phi 110", 110, 0, False),
          ("NORMAL: phi 110, leaf 65 (sun behind, 45 deg)", 110, 65, False),
          ("NORMAL + stay", 110, 65, True), ("LEAF HORIZONTAL phi 110 psi 110, no stay", 110, 110, False),
          ("LEAF HORIZONTAL + stay", 110, 110, True), ("MAX: phi 110 psi 190 + stay", 110, 190, True),
          ("phi 135, leaf stowed, no stay", 135, 0, False), ("WORST REARWARD: phi 135 psi 135 + stay", 135, 135, True),
          ("WORST REARWARD without stay", 135, 135, False)]


def check_mechanics(items):
    S = "8 hinge"
    rows = []
    phis = list(range(0, int(P["LID_ANGLE_MAX"]) + 1, 5))
    for psi_case, psi in (("leaf stowed", 0), ("leaf 110", 110), ("leaf 190", 190)):
        t = [lid_torque(ph, psi, items) for ph in phis]
        rows.append((psi_case, psi, t))
    hold = [ph for ph in phis if ph >= 60]
    tmax = max(abs(lid_torque(ph, psi, items)) for ph in hold for psi in (0, 65, 110, 190))
    need_per = HOLD_SF * tmax / 2
    choice = None
    for sku, tq in SOUTHCO_E6_MED:
        if tq * TORQUE_TOL >= need_per:
            choice = (sku, tq)
            break
    t_close = max(lid_torque(ph, 0, items) for ph in phis)        # most opening-assisting
    t_open_res = -min(lid_torque(ph, 0, items) for ph in phis)    # most closing torque (lid near closed)
    if choice:
        f_open = (2 * choice[1] * 1.2 + max(0.0, t_open_res)) / (D / 1000)
    rec(S, "display-hinge torque: 2 x Southco E6 medium (low bound -20 %) >= 1.5 x max gravity torque, phi 60-135",
        choice is not None and abs(choice[1] - P["LID_HINGE_TORQUE"]) < 1e-9,
        f"max |gravity torque| {tmax:.2f} N.m (lid + leaf, any leaf angle) -> need {need_per:.2f} N.m per hinge at the "
        f"low bound; selected {choice[0] if choice else 'NONE'} {choice[1] if choice else ''} N.m (low bound "
        f"{choice[1] * TORQUE_TOL if choice else 0:.2f}); YAML LID_HINGE_TORQUE {P['LID_HINGE_TORQUE']}")
    if choice:
        rec(S, "lid opening force at the free edge (hinge high bound +20 %)", f_open <= OPEN_FORCE_MAX,
            f"{f_open:.1f} N worst (near closed) vs {OPEN_FORCE_MAX} N ASSUMED limit", warn=True)
    # hard stop at phi max: gravity + 10 m/s front wind - hinge friction (low bound) at a 12 mm stop radius
    tw = 0.0
    for p, f in wind(P["LID_ANGLE_MAX"], 0, 10.0, 0.0, 0.0):
        if p[1] > HAY - 1 and abs(p[2] - H / 2) > 1e-6:
            tw += ((p[2] - HAZ) * f[1] - (p[1] - HAY) * f[2]) / 1000
    tg = lid_torque(P["LID_ANGLE_MAX"], 190, items)
    t_stop = max(0.0, tg + tw - (2 * choice[1] * TORQUE_TOL if choice else 0))
    f_stop = t_stop / 0.012 / 2
    t_push = MISUSE_PUSH * D / 1000                  # user pushes the lid free edge rearward at phi max
    t_stop_m = max(t_stop, tg + t_push - (2 * choice[1] * TORQUE_TOL if choice else 0))
    f_stop = t_stop_m / 0.012 / 2
    sigma = f_stop / (8.0 * 6.0)
    rec(S, "phi-max hard stop (2 printed stop faces in the corner blocks, 8 x 6 mm contact at r 12)", sigma <= 25.0 / 2,
        f"gravity {tg:.2f} + 10 m/s front wind {tw:.2f} N.m is held by the hinge friction (stop load {t_stop:.2f}); misuse "
        f"push {MISUSE_PUSH:.0f} N at the free edge -> stop torque {t_stop_m:.2f} N.m, {f_stop:.0f} N per stop, bearing "
        f"{sigma:.1f} MPa vs PETG ~25 / SF 2 (EST); a steel stop pin in the block is the fallback")
    radial = (sum(g for _, g, b, _, _ in items if b in ("lid", "leaf")) / 1000 * G) / 2
    heavy = [(l, g * (1.25 if t.startswith("EST") else 1.0), b, p, t) for l, g, b, p, t in items]
    t_heavy = max(abs(lid_torque(ph, ps, heavy)) for ph in hold for ps in (0, 65, 110, 190))
    need_heavy = HOLD_SF * t_heavy / 2
    rec(S, "display-hinge variant robust to the estimated lid / leaf masses (EST items +25 %)",
        choice is not None and choice[1] * TORQUE_TOL >= need_heavy,
        f"heavy case needs {need_heavy:.2f} N.m per hinge vs {choice[1] * TORQUE_TOL if choice else 0:.2f} low bound of "
        f"{choice[0] if choice else '-'}: the torque variant cannot be frozen until the printed lid + display are weighed "
        "(audit 2026-10-06)", warn=True)
    rec(S, "Southco E6 medium radial load (MFR max static 155 N)", radial * 3 <= 155,
        f"lid + leaf weight {radial:.1f} N per hinge; x3 handling factor {radial * 3:.0f} N")
    info(S, "gravity torque vs lid angle (N.m)", "; ".join(
        f"{case}: " + ", ".join(f"{ph}:{t[i]:+.2f}" for i, ph in enumerate(phis) if ph % 15 == 0) for case, _, t in rows))
    # leaf hinge (SB-261): reuse the REPO requirement but with V1 leaf mass
    leaf_g = sum(g for _, g, b, _, _ in items if b == "leaf")
    t_leaf = leaf_g / 1000 * G * (P["SOLAR_LEAF_DEPTH"] / 2 - LAX[0]) / 1000
    t_wind = 0.5 * RHO_AIR * 100 * P["SOLAR_LEAF_WIDTH"] * P["SOLAR_LEAF_DEPTH"] * 1e-6 * CN_MAX * (P["SOLAR_LEAF_DEPTH"] / 2 - LAX[0]) / 1000
    need_leaf = (t_leaf + t_wind) * 1.5 / 2
    rec(S, "SB-261-6 leaf hinge torque vs V1 leaf (gravity + 10 m/s, x1.5, per hinge)", 0.96 >= need_leaf,
        f"leaf {leaf_g:.0f} g; gravity {t_leaf:.2f} + wind {t_wind:.2f} N.m -> {need_leaf:.2f} per hinge vs published "
        f"0.96-1.13 (SF {0.96 / need_leaf:.2f} at the low end; REPO D-010 basis was 0.83) - PHYSICAL VALIDATION REQUIRED",
        warn=True)
    return choice


def check_stability(items):
    S = "12 stability"
    out = []
    for name, phi, psi, stay in STATES:
        m, c, res = stability(items, phi, psi, stay)
        rear = min((v for k, v in res.items() if k.startswith("rear")), key=lambda r: r[1] if r[1] is not None else 99,
                   default=(None, None))
        out.append((name, m, c, rear, res))
    return out


# =====================================================================================================================
# 5. THERMAL (lumped, CALC; no CFD)
# =====================================================================================================================
RHO_A, CP_A = 1.13, 1007.0
FAN_FREE_CFM = 5.5                   # MFR Sunon MF30100V1
FAN_DERATE = 0.50                    # ASSUMED in-system / free-air flow (vents, grilles, duct); sensitivity 0.35 shown
HAT_LIMIT, SOC_THROTTLE, CELL_CHG_MAX = 50.0, 80.0, 45.0
SOC_K = (64.0 - 24.0) / 8.8          # K/W: Raspberry Pi blog, Active Cooler + M.2 HAT, ~64 C SoC at sustained stress
                                     # on an open bench (MFR blog); 24 C bench ambient and 8.8 W stress ASSUMED
NAT_W_PER_K = 0.30                   # EST passive loss of the base (vents + walls), W/K, fan off
BAY_COUPLING = 0.35                  # EST fraction of the base air rise reaching the separated battery bay


def check_thermal():
    S = "6 thermal"
    q = FAN_FREE_CFM * FAN_DERATE / 2118.88
    rows = []
    for st in ("LOW", "NORMAL", "HIGH", "WORST"):
        h = PWR.heat_split(st)
        sp = PWR.FAN_SPEED[st]
        dT = h["base"] / (RHO_A * CP_A * q * sp + NAT_W_PER_K)
        mode = f"fan {100 * sp:.0f} % speed, {FAN_DERATE * FAN_FREE_CFM * sp:.2f} CFM"
        pi = PWR.states()[st]["v5_items"]["Pi 5"]
        dsoc = dT + SOC_K * pi
        amb_hat = HAT_LIMIT - dT
        amb_soc = SOC_THROTTLE - dsoc
        rows.append((st, h["base"], h["lid"], mode, dT, dsoc, amb_hat, amb_soc))
    T_OP = 35.0
    nrm = [r for r in rows if r[0] == "NORMAL"][0]
    high = [r for r in rows if r[0] == "HIGH"][0]
    rec(S, f"NORMAL at {T_OP:.0f} C ambient: internal air <= HAT+ 50 C limit", nrm[6] >= T_OP,
        f"base {nrm[1]:.1f} W, air rise {nrm[4]:.1f} K -> max ambient {nrm[6]:.1f} C (CALC, fan ASSUMED {FAN_DERATE:.0%} of free air)")
    rec(S, f"NORMAL at {T_OP:.0f} C: SoC below the 80 C throttle onset", nrm[7] >= T_OP,
        f"SoC rise {nrm[5]:.1f} K -> max ambient {nrm[7]:.1f} C")
    rec(S, f"HIGH at {T_OP:.0f} C: internal air <= 50 C", high[6] >= T_OP, f"air rise {high[4]:.1f} K -> max ambient "
        f"{high[6]:.1f} C", warn=True)
    rec(S, f"HIGH sustained at {T_OP:.0f} C without throttling", high[7] >= T_OP,
        f"SoC rise {high[5]:.1f} K -> no throttling up to {high[7]:.1f} C ambient; above that the Pi throttles (graceful)",
        warn=True)
    lowq = FAN_FREE_CFM * 0.35 / 2118.88
    dT_low = PWR.heat_split("HIGH")["base"] / (RHO_A * CP_A * lowq + NAT_W_PER_K)
    info(S, "fan sensitivity", f"at 35 % of free air (instead of 50 %) HIGH air rise {dT_low:.1f} K (max ambient for the HAT+ "
         f"{HAT_LIMIT - dT_low:.1f} C). Passive only (fan failed) at LOW: {PWR.heat_split('LOW')['base'] / NAT_W_PER_K:.1f} K: "
         "the fan is required; control it on internal-air temperature, not only on SoC temperature")
    chg = PWR.heat_split("NORMAL", 60.0)
    dT_c = chg["base"] / (RHO_A * CP_A * q * PWR.FAN_SPEED["NORMAL"] + NAT_W_PER_K)
    bay = BAY_COUPLING * dT_c + 2.0
    rec(S, "charging at 60 W while NORMAL: cells <= 45 C (BMS / JEITA charge window) at 35 C ambient",
        T_OP + bay <= CELL_CHG_MAX, f"base {chg['base']:.1f} W (charger + I2R {chg['charging']:.1f} W), air rise {dT_c:.1f} K; "
        f"bay EST +{bay:.1f} K (separated bay, {BAY_COUPLING} coupling + 2 K self-heating) -> cells ~{T_OP + bay:.1f} C")
    info(S, "lid / sun (REPO D-010 Phase 2 s.13, EST, not re-run)", "closed lid in sun at 35 C: display +15-22 K with the 6 mm "
         "vented gap + low-e foil (50-57 C) vs G101UAN01.0 3P limits -10/-20..60/70 C (conflicting) -> 3-13 K margin; "
         "open with leaf deployed +6-9 K. VALIDATION REQUIRED (thermal mock-up)")
    return rows, q


# =====================================================================================================================
# 6. HARNESS (estimated lengths, +25 % + service loops)
# =====================================================================================================================
def harness():
    def L(*pts):
        return sum(abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2]) for a, b in zip(pts, pts[1:]))
    pe, dc, cp, gn, pi = cen("ENV_POWER_ELEC"), cen("ENV_DISPLAY_CTRL"), cen("ENV_COMPUTE_POWER"), cen("ENV_GNSS"), cen("ENV_PI_STACK")
    bat = cen("ENV_BATTERY_BAY")
    hinge_pass = (0.0, D - WT, KTZ0)
    lid_far = (0.0, DSP_Y1, ZF + 8)
    leaf_sleeve = (44.0, LAX[0] + 8, LAX[1])
    rows = [
        # (cable, type, from, to, est length, bend radius, connectors, service)
        ("Battery pack lead", "2 x 16 AWG silicone + NTC 26 AWG", "pack (left bay)", "power board BAT", L(bat, pe), 10,
         "Micro-Fit 3.0 2+2, keyed latching", "unplug at the battery door"),
        ("SYS bus to 5.1 V buck", "2 x 18 AWG silicone", "power board SYS", "5.1 V buck (right)", L(pe, cp), 8,
         "JST-XH 2 / screw terminal", "board-to-board, captive"),
        ("5.1 V to Pi", "USB-C plug, power-only, 2 x 18 AWG", "5.1 V buck", "Pi USB-C (rear edge)", L(cp, (pi[0] + 30, PI_Y1, PCB_Z)), 15,
         "USB-C plug (right-angle)", "plug"),
        ("12 V to display controller", "2 x 22 AWG", "12 V regulator (power board)", "Beck controller", L(pe, dc), 6,
         "JST-PH / controller header", "plug"),
        ("HDMI0 to controller", "micro-HDMI to HDMI FPC ribbon", "Pi micro-HDMI (rear edge)", "Beck HDMI in",
         L((pi[0] + 10, PI_Y1, PCB_Z), dc), 10, "micro-HDMI / HDMI", "plug both ends"),
        ("eDP to panel", "30-pin micro-coax eDP", "Beck eDP out", "panel (lid)", L(dc, hinge_pass) + L(hinge_pass, lid_far) + 60, 5,
         "I-PEX-class 30-pin both ends", "through the display-hinge pass, 60 mm twist zone"),
        ("Solar lead", "2 x 0.5 mm2 silicone, d 4", "P108 (leaf)", "power board VAC2",
         L(leaf_sleeve, (60.0, D / 2, ZF + 11), hinge_pass) + 60 + L(hinge_pass, pe), 12,
         "keyed 2-pin at the leaf (lift-off) + at the board", "R12 sleeve (REPO) + display-hinge pass"),
        ("USB keyboard", "USB-C to USB-A, 0.3 m (short lead)", "keyboard USB-C", "Pi USB2 (under trackpad)",
         L((0.0, KBY0 + 20, KTZ0), (pi[0] - PIW / 2 - 15, pi[1], PCB_Z)), 15, "USB-C / USB-A", "plug"),
        ("USB trackpad", "fixed USB-A lead, excess coiled", "trackpad", "Pi USB2", L((0.0, (TPY0 + TPY1) / 2, TTZ0),
         (pi[0] - PIW / 2 - 15, pi[1], PCB_Z)), 15, "USB-A", "plug; coil secured with a clip"),
        ("USB 3.0 external x2", "USB 3.0 panel-mount extension 0.3 m", "Pi USB3", "front-right wall",
         L((pi[0] - PIW / 2 - 15, pi[1], PCB_Z), (BHX1 + 29, WT, IZ0 + 10)), 20, "USB-A male / panel female", "plug"),
        ("GNSS", "6-wire 26 AWG (3V3, GND, TX, RX, PPS, spare)", "Pi GPIO pass-through header", "GNSS pHAT",
         L((pi[0], PI_Y0 + 4, PI_Z1), gn), 8, "right-angle 2.54 mm housings on the HAT+ pass-through (vertical ones hit the deck)", "plug"),
        ("Enclosure fan", "2 x 26 AWG + logic FET", "5.1 V rail via FET (GPIO PWM)", "fan", L(cp, cen("ENV_FAN")), 8,
         "JST-PH 2", "plug"),
        ("Power button + LED", "4 x 26 AWG", "left-wall button", "Pi J2 + charger QON", L(cen("ENV_BUTTON"), pe) + L(pe, pi),
         8, "JST-SH / PH", "plug"),
        ("Charger I2C", "4 x 28 AWG", "power board", "Pi GPIO (I2C1)", L(pe, pi), 8, "JST-SH 4 (Qwiic-style)", "plug"),
    ]
    return [(a, b, c, d, e * 1.25 + 30.0, f, g, h) for a, b, c, d, e, f, g, h in rows]


# =====================================================================================================================
# 7. DFM REVIEW
# =====================================================================================================================
BEDS = {"256 x 256 (Bambu P1/X1/A1, Prusa MK4 250 x 210 excluded)": (256, 256), "350 x 320 (Bambu H2D class)": (350, 320),
        "360 x 360 (Prusa XL)": (360, 360)}


def check_dfm():
    S = "13 DFM"
    for name, b in BOXES_D.items():
        if b[1] == "S" and name.startswith(("SHELL_WALL", "BULKHEAD", "SERVICE", "BATTERY_DOOR", "KEYBOARD_TRAY", "TRACKPAD_TRAY")):
            t = min(b[3] - b[2], b[5] - b[4], b[7] - b[6])
            if t < P["MIN_WALL"] - 1e-9:
                rec(S, f"{name} wall thickness", False, f"{t:.2f} < MIN_WALL {P['MIN_WALL']}")
    rec(S, "wall / panel / plate thickness >= MIN_WALL", min(WT, PT, MP) >= P["MIN_WALL"],
        f"walls {WT}, panels {PT}, plates {MP} vs {P['MIN_WALL']}")
    boss_wall = (P["BOSS_DIAMETER"] - 4.0) / 2
    rec(S, "boss wall around the M3 insert hole (Ø4.0 for RX-M3x5.7)", boss_wall >= 1.5,
        f"{boss_wall:.2f} mm (>= 1.5 EST practice)")
    post_wall = (P["TRAY_POST_DIAMETER"] - 3.55) / 2
    rec(S, "tray post wall around the M2.5 insert (OD 3.55)", post_wall >= 1.2, f"{post_wall:.2f} mm")
    ins, head_r, hole_r = P["PANEL_SCREW_INSET"], 5.7 / 2, 3.4 / 2           # ISO 7380 M3 head dk 5.7 (standard)
    rec(S, "F1 (Round E): panel / door screw heads clear the walls; panel ligament around the hole",
        ins - head_r >= 0.5 and ins - P["CLEARANCE"] - hole_r >= 1.2,
        f"axis {ins} from the wall face: head clearance {ins - head_r:.2f} (>= 0.5), panel ligament "
        f"{ins - P['CLEARANCE'] - hole_r:.2f} (>= 1.2); boss Ø{P['BOSS_DIAMETER']} merges into the wall")
    rec(S, "F2 (Round E): compute-sled screw heads", PT >= 1.65,
        f"V1 sled = {PT} mm insert plate in the front panel pocket: Pi standoffs fixed with ISO 10642 M2.5 countersunk screws "
        "(head 1.5) flush with the underside; no gap layer between sled and panel remains")
    parts = printed_parts()
    for part, mat, g, fx, fy in parts:
        fits = [k for k, (bx, by) in BEDS.items() if (fx <= bx - 4 and fy <= by - 4) or (fy <= bx - 4 and fx <= by - 4)]
        rec(S, f"print bed: {part} ({fx:.0f} x {fy:.0f})", "256 x 256 (Bambu P1/X1/A1, Prusa MK4 250 x 210 excluded)" in fits,
            ("fits " + ", ".join(fits)) if fits else "fits no listed bed", warn=True)
    tot = sum(g for _, _, g, _, _ in parts)
    info(S, "printed mass", f"{tot:.0f} g total (" + ", ".join(f"{p.split(' (')[0]} {g:.0f} g {m}" for p, m, g, _, _ in parts)
         + "); EST; filament to buy x1.4 for supports, coupons and one reprint")
    return parts


# =====================================================================================================================
# REPORT
# =====================================================================================================================
def main(argv):
    build_index()
    if _errors:
        print("YAML INVALID: " + "; ".join(_errors))
        return 1
    rec("15 source of truth", "nomad.yaml valid and resolvable", not _errors and _unres == ["CABLE_CLEARANCE"],
        f"{len(_params)} parameters; unresolved (TBD without working input): {', '.join(_unres)}")
    check_layout()
    check_lid()
    items = mass_items()
    choice = check_mechanics(items)
    stab = check_stability(items)
    therm, q = check_thermal()
    parts = check_dfm()

    print("# NOMAD Virtual V1 integration report (CAD/tools/v1_integration.py)\n")
    print("All results are CALC / modelled from candidate-part data and estimates. Nothing is measured or physically tested.\n")
    print("## Envelope\n")
    print(f"- Base {W:.0f} x {D:.0f} x {H:.0f} mm (W x D x H); lid {LIDT:.0f} thick (core {CORE} + air gap {AIRG} + leaf {LEAFT}); "
          f"closed {W:.0f} x {D:.0f} x {H + P['LID_CLOSED_GAP'] + LIDT:.0f} mm (excl. feet {FOOT_H:.0f} and the hinge barrels).")
    print(f"- Under-keyboard free height {KTZ0 - IZ0:.1f}; palm bays {IX - BHX1:.1f} wide x {PALM_Y1 - IY0:.1f} deep x "
          f"{IZ1 - IZ0:.1f} high; display hinge axis (y {HAY:.1f}, z {HAZ:.1f}); leaf axis closed (y {LAX[0]}, z {LAX[1]:.1f}).")
    print(f"- Display y {DSP_Y0:.1f}..{DSP_Y1:.1f}, z {DSP_Z0:.1f}..{DSP_Z1:.2f} (closed frame).\n")
    print("## Layout boxes (x0..x1 / y0..y1 / z0..z1, mm)\n")
    print("| Box | cat | x | y | z |")
    print("|---|---|---|---|---|")
    for b in BOXES:
        print(f"| {b[0]} | {b[1]} | {b[2]:.1f}..{b[3]:.1f} | {b[4]:.1f}..{b[5]:.1f} | {b[6]:.1f}..{b[7]:.1f} |")

    print("\n## Mass (g) and centre of gravity\n")
    tot = sum(g for _, g, _, _, _ in items)
    by = {}
    for lab, g, body, _, tag in items:
        grp = {"base": "base", "stay": "stay", "lid": "lid", "leaf": "leaf"}[body]
        by[grp] = by.get(grp, 0) + g
    print("| Item | g | body | tag |")
    print("|---|---:|---|---|")
    for lab, g, body, _, tag in items:
        print(f"| {lab} | {g:.0f} | {body} | {tag} |")
    print(f"| **total** | **{tot:.0f}** | | |")
    print("\nBy subsystem: " + ", ".join(f"{k} {v:.0f} g ({100 * v / tot:.0f} %)" for k, v in by.items()))
    meas = sum(g for _, g, _, _, t in items if t.startswith("MFR"))
    print(f"Manufacturer-published masses: {meas:.0f} g ({100 * meas / tot:.0f} %); the rest is EST / REPO.")
    lo, hi = tot - 0.25 * (tot - meas), tot + 0.25 * (tot - meas)
    print(f"Range (EST items -25 % / +25 %): {lo / 1000:.2f} - {hi / 1000:.2f} kg.\n")

    print("## Stability (D-010 Phase 2 method: rigid table, feet 8 mm in, flat-plate Cn wind; CALC)\n")
    print("| State | kg | CG x / y / z | rear margin mm | rear tip wind m/s | worst other edge |")
    print("|---|---:|---|---:|---:|---|")
    for name, m, c, rear, res in stab:
        oth = min(((k, v) for k, v in res.items() if not k.startswith("rear")), key=lambda kv: kv[1][1] if kv[1][1] else 99)
        rm, rv = rear
        print(f"| {name} | {m / 1000:.2f} | {c[0]:.1f} / {c[1]:.1f} / {c[2]:.1f} | {rm:.0f} | "
              f"{('TIPS (gravity)' if rv == 0 else f'{rv:.1f}')} | {oth[0]} {oth[1][1]:.1f} |")
    worst_ns = [s for s in stab if s[0] == "WORST REARWARD without stay"][0]
    rec("12 stability", "B1 stability with the stay: every deployed state rear tip wind >= 10 m/s",
        all((s[3][1] or 0) >= 10.0 for s in stab if "+ stay" in s[0]),
        "; ".join(f"{s[0]}: {s[3][1]:.1f} m/s" for s in stab if "+ stay" in s[0]))
    rec("12 stability", "statically stable in every listed state (gravity alone)", all((s[3][1] or 0) > 0 for s in stab)
        or worst_ns[3][1] == 0, f"phi 135 / psi 135 without stay: rear margin {worst_ns[3][0]:.0f} mm "
        "(stay mandatory, D-010)", warn=True)

    print("\n## Thermal (lumped; CALC / ASSUMED; no CFD)\n")
    print(f"Fan {HW['FAN']['mfr']} {HW['FAN']['sku']}: {FAN_FREE_CFM} CFM free (MFR) x {FAN_DERATE} ASSUMED = {q * 1000:.2f} L/s; "
          f"passive {NAT_W_PER_K} W/K EST; SoC {SOC_K:.2f} K/W over local air (MFR blog, inferred).\n")
    print("| State | base W | lid W | cooling | air rise K | SoC rise K | max ambient (HAT+ 50 C) | max ambient (no SoC throttle) |")
    print("|---|---:|---:|---|---:|---:|---:|---:|")
    for r in therm:
        print(f"| {r[0]} | {r[1]:.1f} | {r[2]:.1f} | {r[3]} | {r[4]:.1f} | {r[5]:.1f} | {r[6]:.1f} | {r[7]:.1f} |")

    print("\n## Harness (estimated lengths: Manhattan route x 1.25 + 30 mm service; fix at the fit-up)\n")
    print("| Cable | type | from | to | est. length mm | min bend R | connectors | service |")
    print("|---|---|---|---|---:|---:|---|---|")
    for row in harness():
        print(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]:.0f} | {row[5]} | {row[6]} | {row[7]} |")

    print("\n## Printed parts (EST)\n")
    for part, mat, g, fx, fy in parts:
        print(f"- {part}: {mat}, {g:.0f} g, footprint {fx:.0f} x {fy:.0f} mm")

    print("\n## Checks\n")
    print("| # | Section | Check | Result | Detail |")
    print("|---:|---|---|---|---|")
    for i, (sec, name, st, det) in enumerate(RESULTS, 1):
        print(f"| {i} | {sec} | {name} | {st} | {det} |")
    n = {k: sum(1 for r in RESULTS if r[2] == k) for k in ("PASS", "WARN", "FAIL", "INFO")}
    print(f"\nSUMMARY: {n['PASS']} PASS, {n['WARN']} WARN, {n['FAIL']} FAIL, {n['INFO']} INFO")
    if "--check" in argv and n["FAIL"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
