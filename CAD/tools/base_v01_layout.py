"""NOMAD Mechanical V0.1 base chassis (Round C): layout spec, local checks, FeatureScript generation.

One spec drives everything: every part below is a union of axis-aligned boxes and vertical cylinders
whose coordinates are expressions over nomad.yaml parameters (working values where TBD) and the named
derived quantities in DERIVED. No hidden length constants: literal numbers are unitless factors only.

  py CAD/tools/base_v01_layout.py            evaluate + run all local checks (modeled), print the report
  py CAD/tools/base_v01_layout.py --write    also regenerate the GENERATED BASE V0.1 LAYOUT block in
                                             NOMAD_P01.fs and the expected-value block in
                                             NOMAD_P01.basev01.test.fs (Onshape kernel cross-check)
  py CAD/tools/base_v01_layout.py --check    fail if either generated block is out of date
  add --target FILE [--harness FILE] to write/check the same blocks in other CAD/featurescript files (Round E)

World frame (as Round A): origin at the base bottom-front edge on the centreline, +X right, +Y rear
(toward the hinge), +Z up. Part categories:
  S structure (printed/metal parts)      E component envelope (reserve, not hardware)
  H hinge-mount reserve (load path)      K internal keep-out (cooling, connectors)
  C cable corridor keep-out              W zone inside a wall (vents, pass-through; overlaps the shell)
  X external keep-out (plugs behind the rear face)
This is an engineering envelope model, not a detailed enclosure. Results are modeled, not tested.
"""

import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hinge_feasibility_2d as hm  # noqa: E402
from yaml_to_featurescript import (YAML_PATH, _eval_formula, _num, flatten,  # noqa: E402
                                   parse_restricted_yaml, resolve)

ROOT = Path(__file__).resolve().parents[2]
FS_PATH = ROOT / "CAD" / "featurescript" / "NOMAD_P01.fs"
HARNESS_PATH = ROOT / "CAD" / "featurescript" / "NOMAD_P01.basev01.test.fs"
BEGIN, END = "// BEGIN GENERATED BASE V0.1 LAYOUT", "// END GENERATED BASE V0.1 LAYOUT"
HBEGIN, HEND = "// BEGIN GENERATED BASE V0.1 EXPECTED", "// END GENERATED BASE V0.1 EXPECTED"
NEAR = 15.0        # pairs closer than this (mm) get an exact kernel distance comparison
EPS = 1e-6
KNOWN_PLUG_CONFLICT_FLOOR = -7.01    # documented open conflict (Round E0.5, T 37.6, h 0, 135 deg: -7.001); not a design value

P, _ = resolve(flatten(parse_restricted_yaml(YAML_PATH.read_text(encoding="utf-8"))))
PARAMS = {k: v for k, (v, _) in P.items() if isinstance(v, (int, float)) and not isinstance(v, bool)}

# ---------------------------------------------------------------- derived layout quantities (ordered)
DERIVED = [
    # envelope and interior (walls/deck = WALL_THICKNESS, bottom = removable panels)
    ("W2", "BODY_WIDTH / 2"),
    ("IX", "W2 - WALL_THICKNESS"),
    ("IY0", "WALL_THICKNESS"),
    ("IY1", "BODY_DEPTH - WALL_THICKNESS"),
    ("IZ0", "SERVICE_PANEL_THICKNESS"),
    ("IZ1", "BODY_HEIGHT - WALL_THICKNESS"),
    ("OFF", "BOSS_DIAMETER / 2 - WALL_THICKNESS / 2"),          # boss centre from a wall's inner face
    # trackpad (D-003: centred below the keyboard) and keyboard, as Round A
    ("TPC", "TRACKPAD_LATERAL_OFFSET"),
    ("KBC", "KEYBOARD_LATERAL_OFFSET"),
    ("TPY0", "BASE_FRONT_MARGIN"),
    ("TPY1", "TPY0 + TRACKPAD_DEPTH"),
    ("TPZ1", "BODY_HEIGHT - TRACKPAD_TOP_RECESS"),
    ("TPZ0", "TPZ1 - TRACKPAD_THICKNESS"),
    ("KBY0", "TPY1 + TRACKPAD_KEYBOARD_GAP"),
    ("KBY1", "KBY0 + KEYBOARD_DEPTH"),
    ("KBZ1", "BODY_HEIGHT - KEYBOARD_TOP_RECESS"),
    ("KBZ0", "KBZ1 - KEYBOARD_THICKNESS"),
    # input trays (separate parts under the deck openings)
    ("KTY0", "KBY0 - INPUT_TRAY_LIP"),
    ("KTY1", "KBY1 + INPUT_TRAY_LIP"),
    ("KTZ0", "KBZ0 - MOUNT_PLATE_THICKNESS"),
    ("KTX", "IX - CLEARANCE"),
    ("TTY0", "TPY0 - INPUT_TRAY_LIP"),
    ("TTY1", "TPY1 + INPUT_TRAY_LIP"),
    ("TTZ0", "TPZ0 - MOUNT_PLATE_THICKNESS"),
    # trackpad-bay bulkheads -> left (power) and right (compute) palm-rest bays
    ("BHR0", "TPC + TRACKPAD_WIDTH / 2 + TRACKPAD_BAY_MARGIN"),
    ("BHR1", "BHR0 + WALL_THICKNESS"),
    ("BHL1", "TPC - TRACKPAD_WIDTH / 2 - TRACKPAD_BAY_MARGIN"),
    ("BHL0", "BHL1 - WALL_THICKNESS"),
    ("BAYRC", "(BHR1 + IX) / 2"),
    ("BAYLC", "(BHL0 - IX) / 2"),
    ("FBY", "IY0 + OFF"),                                       # front boss row
    # compute bay: sled, Pi stack, cooling duct, sled bosses
    ("SLZ0", "IZ0 + MIN_GAP"),
    ("SLZ1", "SLZ0 + MOUNT_PLATE_THICKNESS"),
    ("SLY0", "FBY + BOSS_DIAMETER / 2 + CLEARANCE"),
    ("SLY1", "KTY0 - CLEARANCE"),
    ("PIW", "PI_WIDTH + 2 * PI_ENVELOPE_MARGIN"),
    ("PID", "PI_DEPTH + 2 * PI_ENVELOPE_MARGIN"),
    ("PIX0", "BAYRC - PIW / 2"),
    ("PIX1", "BAYRC + PIW / 2"),
    ("PIY1", "KTY0 - BOSS_DIAMETER - MIN_GAP"),
    ("PIY0", "PIY1 - PID"),
    ("PIZ1", "SLZ1 + PI_STACK_HEIGHT"),
    ("SBYF", "FBY + BOSS_DIAMETER + MIN_GAP"),
    ("SBYR", "PIY1 + MIN_GAP + BOSS_DIAMETER / 2"),
    ("DUX0", "BHR1 + OFF + BOSS_DIAMETER / 2 + MIN_GAP"),
    ("DUX1", "IX - OFF - BOSS_DIAMETER / 2 - MIN_GAP"),
    ("DUY0", "PIY0 - COOLING_DUCT_DEPTH"),
    ("DUZ1", "IZ1 - MIN_GAP"),
    # power bay: battery reserve, bay rear wall (with cable slot), power electronics
    ("RIBY1", "KTY0 - CLEARANCE"),
    ("RIBY0", "RIBY1 - WALL_THICKNESS"),
    ("BATY1", "RIBY0 - MIN_GAP"),
    ("BATY0", "BATY1 - BATTERY_BAY_DEPTH"),
    ("BATX0", "BAYLC - BATTERY_BAY_WIDTH / 2"),
    ("BATX1", "BAYLC + BATTERY_BAY_WIDTH / 2"),
    ("BATZ0", "IZ0 + MIN_GAP"),
    ("BATZ1", "BATZ0 + BATTERY_BAY_HEIGHT"),
    ("PEY0", "RIBY1 + MIN_GAP"),
    ("PEY1", "PEY0 + POWER_ELEC_DEPTH"),
    ("PEX0", "BAYLC - POWER_ELEC_WIDTH / 2"),
    ("PEX1", "BAYLC + POWER_ELEC_WIDTH / 2"),
    # floor-level cable corridors
    ("CZ0", "IZ0 + MIN_GAP"),
    ("CZ1", "CZ0 + CABLE_CORRIDOR_HEIGHT"),
    ("PEZ1", "CZ0 + POWER_ELEC_HEIGHT"),
    ("TRY1", "KBY1"),
    ("TRY0", "TRY1 - CABLE_CORRIDOR_WIDTH"),
    ("BLX0", "BAYLC - CABLE_CORRIDOR_WIDTH / 2"),
    ("BLX1", "BAYLC + CABLE_CORRIDOR_WIDTH / 2"),
    ("CCX1", "IX - OFF - BOSS_DIAMETER / 2 - MIN_GAP"),
    ("CCX0", "CCX1 - CABLE_CORRIDOR_WIDTH"),
    ("CCZ0", "SLZ1 + MIN_GAP"),
    ("CCZ1", "CCZ0 + CABLE_CORRIDOR_HEIGHT"),
    ("CPX1", "CCX0"),
    ("CPX0", "CPX1 - COMPUTE_POWER_WIDTH"),
    ("CPY0", "KTY0 + MIN_GAP"),
    ("CPY1", "CPY0 + COMPUTE_POWER_DEPTH"),
    ("CPZ1", "CZ0 + COMPUTE_POWER_HEIGHT"),
    ("GNX1", "TPC - CABLE_CORRIDOR_WIDTH / 2 - MIN_GAP"),
    ("GNX0", "GNX1 - GNSS_MODULE_WIDTH"),
    ("GNY1", "TRY0"),
    ("GNY0", "GNY1 - GNSS_MODULE_DEPTH"),
    ("GNZ1", "CZ0 + GNSS_MODULE_HEIGHT"),
    ("CW2", "CABLE_CORRIDOR_WIDTH / 2"),
    ("RSY0", "KTY1 + MIN_GAP"),
    ("RSY1", "IY1 - MIN_GAP"),
    # keyboard-tray side bosses (full height, tray notched around them), tray posts, panel standoffs
    ("SBSY", "KBY0 + KEYBOARD_DEPTH / 2"),
    ("NOTX", "IX - OFF - BOSS_DIAMETER / 2 - CLEARANCE"),
    ("NOTY0", "SBSY - BOSS_DIAMETER / 2 - CLEARANCE"),
    ("NOTY1", "SBSY + BOSS_DIAMETER / 2 + CLEARANCE"),
    ("POSTX", "KEYBOARD_WIDTH / 2 + BASE_SIDE_MARGIN / 2"),
    ("POSTY0", "KBY0 + KEYBOARD_DEPTH / 6"),
    ("POSTY1", "KBY0 + KEYBOARD_DEPTH * 5 / 6"),
    ("STDX", "KEYBOARD_WIDTH / 8"),
    ("STDY", "KBY0 + KEYBOARD_DEPTH / 4"),
    # rear service region: port-panel apertures, hinge-mount reserves, rear bosses
    ("PX0", "PORT_PANEL_INSET"),
    ("PX1", "PX0 + PORT_PANEL_WIDTH"),
    ("PZ0", "PORT_PANEL_BOTTOM"),
    ("PZ1", "PZ0 + PORT_PANEL_HEIGHT"),
    ("HX0", "IX - HINGE_MOUNT_WIDTH"),
    ("HY0", "IY1 - HINGE_MOUNT_DEPTH"),
    ("RBX", "(PX1 + HX0) / 2"),
    ("RCX", "CABLE_CORRIDOR_WIDTH / 2 + MIN_GAP + BOSS_DIAMETER / 2"),
    ("RBY", "IY1 - OFF"),
    # service-panel seams: on the left bulkhead and on the battery-bay rear wall
    ("SEAMX", "BHL0 + WALL_THICKNESS / 2"),
    ("SEAMY", "(RIBY0 + RIBY1) / 2"),
]


def box(label, *c):
    return ("box", label, c)


def cyl(label, *c):
    return ("cyl", label, c)


B = "BOSS_DIAMETER"
# ---------------------------------------------------------------- parts: (name, category, [primitives])
PARTS = [
    ("BASE_SHELL", "S", [
        # walls (full height; bottom closed by removable panels)
        box("wall_front", "-W2", "0", "0", "W2", "IY0", "BODY_HEIGHT"),
        box("wall_left", "-W2", "IY0", "0", "-IX", "IY1", "BODY_HEIGHT"),
        box("wall_right", "IX", "IY0", "0", "W2", "IY1", "BODY_HEIGHT"),
        # rear wall: port-panel notches open to the underside (panels slide in from below; no bridge)
        box("wall_rear_high", "-W2", "IY1", "PZ1", "W2", "BODY_DEPTH", "BODY_HEIGHT"),
        box("wall_rear_l", "-W2", "IY1", "0", "-PX1", "BODY_DEPTH", "PZ1"),
        box("wall_rear_c", "-PX0", "IY1", "0", "PX0", "BODY_DEPTH", "PZ1"),
        box("wall_rear_r", "PX1", "IY1", "0", "W2", "BODY_DEPTH", "PZ1"),
        # top deck with keyboard and trackpad openings (CLEARANCE fit around each module)
        box("deck_front", "-IX", "IY0", "IZ1", "IX", "TPY0 - CLEARANCE", "BODY_HEIGHT"),
        box("deck_tp_l", "-IX", "TPY0 - CLEARANCE", "IZ1", "TPC - TRACKPAD_WIDTH / 2 - CLEARANCE", "TPY1 + CLEARANCE", "BODY_HEIGHT"),
        box("deck_tp_r", "TPC + TRACKPAD_WIDTH / 2 + CLEARANCE", "TPY0 - CLEARANCE", "IZ1", "IX", "TPY1 + CLEARANCE", "BODY_HEIGHT"),
        box("deck_mid", "-IX", "TPY1 + CLEARANCE", "IZ1", "IX", "KBY0 - CLEARANCE", "BODY_HEIGHT"),
        box("deck_kb_l", "-IX", "KBY0 - CLEARANCE", "IZ1", "KBC - KEYBOARD_WIDTH / 2 - CLEARANCE", "KBY1 + CLEARANCE", "BODY_HEIGHT"),
        box("deck_kb_r", "KBC + KEYBOARD_WIDTH / 2 + CLEARANCE", "KBY0 - CLEARANCE", "IZ1", "IX", "KBY1 + CLEARANCE", "BODY_HEIGHT"),
        box("deck_rear", "-IX", "KBY1 + CLEARANCE", "IZ1", "IX", "IY1", "BODY_HEIGHT"),
        # trackpad-bay bulkheads; battery-bay rear wall with a cable slot
        box("bulkhead_l", "BHL0", "IY0", "IZ0", "BHL1", "KTY0", "IZ1"),
        box("bulkhead_r", "BHR0", "IY0", "IZ0", "BHR1", "KTY0", "IZ1"),
        box("battery_wall_1", "-IX", "RIBY0", "IZ0", "BLX0 - MIN_GAP", "RIBY1", "IZ1"),
        box("battery_wall_2", "BLX1 + MIN_GAP", "RIBY0", "IZ0", "BHL0", "RIBY1", "IZ1"),
        # panel/door bosses (full height, merged into walls)
        cyl("boss_front_lo", "-(IX - OFF)", "FBY", B, "IZ0", "IZ1"),
        cyl("boss_front_li", "BHL0 - OFF", "FBY", B, "IZ0", "IZ1"),
        cyl("boss_front_c", "TPC", "FBY", B, "IZ0", "IZ1"),
        cyl("boss_front_ri", "BHR1 + OFF", "FBY", B, "IZ0", "IZ1"),
        cyl("boss_front_ro", "IX - OFF", "FBY", B, "IZ0", "IZ1"),
        cyl("boss_side_l", "-(IX - OFF)", "SBSY", B, "IZ0", "IZ1"),
        cyl("boss_side_r", "IX - OFF", "SBSY", B, "IZ0", "IZ1"),
        cyl("boss_rear_lo", "-RBX", "RBY", B, "IZ0", "IZ1"),
        cyl("boss_rear_li", "-RCX", "RBY", B, "IZ0", "IZ1"),
        cyl("boss_rear_ri", "RCX", "RBY", B, "IZ0", "IZ1"),
        cyl("boss_rear_ro", "RBX", "RBY", B, "IZ0", "IZ1"),
        # compute-sled bosses (sled screws up into them)
        cyl("boss_sled_fi", "BHR1 + OFF", "SBYF", B, "SLZ1", "IZ1"),
        cyl("boss_sled_fo", "IX - OFF", "SBYF", B, "SLZ1", "IZ1"),
        cyl("boss_sled_ri", "BHR1 + OFF", "SBYR", B, "SLZ1", "IZ1"),
        cyl("boss_sled_ro", "IX - OFF", "SBYR", B, "SLZ1", "IZ1"),
    ]),
    ("KEYBOARD_TRAY", "S", [
        box("plate", "-NOTX", "KTY0", "KTZ0", "NOTX", "KTY1", "KBZ0"),
        box("strip_l_front", "-KTX", "KTY0", "KTZ0", "-NOTX", "NOTY0", "KBZ0"),
        box("strip_l_rear", "-KTX", "NOTY1", "KTZ0", "-NOTX", "KTY1", "KBZ0"),
        box("strip_r_front", "NOTX", "KTY0", "KTZ0", "KTX", "NOTY0", "KBZ0"),
        box("strip_r_rear", "NOTX", "NOTY1", "KTZ0", "KTX", "KTY1", "KBZ0"),
        cyl("post_lf", "KBC - POSTX", "POSTY0", "TRAY_POST_DIAMETER", "KBZ0", "IZ1"),
        cyl("post_lr", "KBC - POSTX", "POSTY1", "TRAY_POST_DIAMETER", "KBZ0", "IZ1"),
        cyl("post_rf", "KBC + POSTX", "POSTY0", "TRAY_POST_DIAMETER", "KBZ0", "IZ1"),
        cyl("post_rr", "KBC + POSTX", "POSTY1", "TRAY_POST_DIAMETER", "KBZ0", "IZ1"),
    ]),
    ("TRACKPAD_TRAY", "S", [box("plate", "BHL1", "TTY0", "TTZ0", "BHR0", "TTY1", "TPZ0")]),
    ("COMPUTE_SLED", "S", [box("plate", "BHR1 + CLEARANCE", "SLY0", "SLZ0", "IX - CLEARANCE", "SLY1", "SLZ1")]),
    ("SERVICE_PANEL_MAIN", "S", [
        box("main", "SEAMX + CLEARANCE / 2", "IY0 + CLEARANCE", "0", "IX - CLEARANCE", "IY1 - CLEARANCE", "IZ0"),
        box("rear_left", "-IX + CLEARANCE", "SEAMY + CLEARANCE / 2", "0", "SEAMX + CLEARANCE / 2", "IY1 - CLEARANCE", "IZ0"),
    ]),
    ("BATTERY_DOOR", "S", [box("plate", "-IX + CLEARANCE", "IY0 + CLEARANCE", "0", "SEAMX - CLEARANCE / 2", "SEAMY - CLEARANCE / 2", "IZ0")]),
    ("PORT_PANEL_MAIN", "S", [box("plate", "PX0 + CLEARANCE", "IY1", "0", "PX1 - CLEARANCE", "BODY_DEPTH", "PZ1 - CLEARANCE")]),
    ("PORT_PANEL_AUX", "S", [box("plate", "-PX1 + CLEARANCE", "IY1", "0", "-PX0 - CLEARANCE", "BODY_DEPTH", "PZ1 - CLEARANCE")]),
    ("PANEL_STANDOFF_L", "S", [cyl("standoff", "KBC - STDX", "STDY", "TRAY_POST_DIAMETER", "IZ0", "KTZ0")]),
    ("PANEL_STANDOFF_R", "S", [cyl("standoff", "KBC + STDX", "STDY", "TRAY_POST_DIAMETER", "IZ0", "KTZ0")]),
    # component envelopes (reserves, not hardware)
    ("ENV_KEYBOARD", "E", [box("env", "KBC - KEYBOARD_WIDTH / 2", "KBY0", "KBZ0", "KBC + KEYBOARD_WIDTH / 2", "KBY1", "KBZ1")]),
    ("ENV_TRACKPAD", "E", [box("env", "TPC - TRACKPAD_WIDTH / 2", "TPY0", "TPZ0", "TPC + TRACKPAD_WIDTH / 2", "TPY1", "TPZ1")]),
    ("ENV_PI_STACK", "E", [box("env", "PIX0", "PIY0", "SLZ1", "PIX1", "PIY1", "PIZ1")]),
    ("ENV_COMPUTE_POWER", "E", [box("env", "CPX0", "CPY0", "CZ0", "CPX1", "CPY1", "CPZ1")]),
    ("ENV_POWER_ELECTRONICS", "E", [box("env", "PEX0", "PEY0", "CZ0", "PEX1", "PEY1", "PEZ1")]),
    ("ENV_BATTERY_BAY", "E", [box("env", "BATX0", "BATY0", "BATZ0", "BATX1", "BATY1", "BATZ1")]),
    ("ENV_GNSS_MODULE", "E", [box("env", "GNX0", "GNY0", "CZ0", "GNX1", "GNY1", "GNZ1")]),
    # hinge-mount reserves (structural load path; hinge hardware TBD, D-006)
    ("KEEPOUT_HINGE_MOUNT_L", "H", [box("reserve", "-IX", "HY0", "IZ0", "-HX0", "IY1", "IZ1")]),
    ("KEEPOUT_HINGE_MOUNT_R", "H", [box("reserve", "HX0", "HY0", "IZ0", "IX", "IY1", "IZ1")]),
    # internal keep-outs
    ("KEEPOUT_COOLING_DUCT", "K", [box("duct", "DUX0", "DUY0", "SLZ1", "DUX1", "PIY0", "DUZ1")]),
    ("KEEPOUT_PORTS_MAIN", "K", [box("connectors", "PX0", "TRY1", "PZ0", "PX1", "IY1", "PZ1")]),
    ("KEEPOUT_PORTS_AUX", "K", [box("connectors", "-PX1", "TRY1", "PZ0", "-PX0", "IY1", "PZ1")]),
    # cable corridors (reserved, no cables routed)
    ("CABLE_TRUNK", "C", [box("trunk", "BLX0", "TRY0", "CZ0", "CCX1", "TRY1", "CZ1")]),
    ("CABLE_COMPUTE", "C", [box("run", "CCX0", "PIY1", "CCZ0", "CCX1", "TRY1", "CCZ1")]),
    ("CABLE_TRACKPAD", "C", [
        box("drop", "TPC - CW2", "TTY1 - CABLE_CORRIDOR_WIDTH", "CZ1", "TPC + CW2", "TTY1", "TTZ0"),
        box("run", "TPC - CW2", "TTY1 - CABLE_CORRIDOR_WIDTH", "CZ0", "TPC + CW2", "TRY1", "CZ1"),
    ]),
    ("CABLE_KEYBOARD", "C", [box("drop", "KBC - CW2", "TRY0", "CZ1", "KBC + CW2", "TRY1", "KTZ0")]),
    ("CABLE_DISPLAY", "C", [
        box("run", "-CW2", "TRY0", "CZ0", "CW2", "RSY0 + CABLE_CORRIDOR_WIDTH", "CZ1"),
        box("riser", "-CW2", "RSY0", "CZ1", "CW2", "RSY1", "IZ1"),
    ]),
    ("CABLE_POWER", "C", [box("run", "BLX0", "PEY1", "CZ0", "BLX1", "TRY1", "CZ1")]),
    ("CABLE_BATTERY", "C", [box("run", "BLX0", "BATY1", "CZ0", "BLX1", "PEY0", "CZ1")]),
    # zones inside walls (overlap the shell by design)
    ("KEEPOUT_VENT_INTAKE", "W", [box("zone", "DUX0", "0", "SLZ1", "DUX1", "IY0", "DUZ1")]),
    ("KEEPOUT_VENT_EXHAUST", "W", [box("zone", "IX", "PIY0", "SLZ1", "W2", "PIY1", "PIZ1")]),
    ("KEEPOUT_DISPLAY_PASS", "W", [box("zone", "-CW2", "IY1", "IZ1 - CABLE_CORRIDOR_HEIGHT", "CW2", "BODY_DEPTH", "BODY_HEIGHT")]),
    # external plug keep-outs behind the rear face
    ("KEEPOUT_PLUGS_MAIN", "X", [box("zone", "PX0", "BODY_DEPTH", "PZ0", "PX1", "BODY_DEPTH + PLUG_KEEPOUT_LENGTH", "PZ1")]),
    ("KEEPOUT_PLUGS_AUX", "X", [box("zone", "-PX1", "BODY_DEPTH", "PZ0", "-PX0", "BODY_DEPTH + PLUG_KEEPOUT_LENGTH", "PZ1")]),
]

# Pairs allowed to touch (served interfaces / seating / fits); everything else in E/K/H/C/S follows RULES.
SERVE = {frozenset(p) for p in [
    ("ENV_KEYBOARD", "KEYBOARD_TRAY"), ("ENV_TRACKPAD", "TRACKPAD_TRAY"), ("ENV_PI_STACK", "COMPUTE_SLED"),
    ("KEEPOUT_COOLING_DUCT", "COMPUTE_SLED"), ("KEEPOUT_COOLING_DUCT", "ENV_PI_STACK"),
    ("CABLE_COMPUTE", "ENV_PI_STACK"), ("CABLE_COMPUTE", "ENV_COMPUTE_POWER"), ("CABLE_TRUNK", "ENV_GNSS_MODULE"),
    ("CABLE_TRACKPAD", "TRACKPAD_TRAY"), ("CABLE_KEYBOARD", "KEYBOARD_TRAY"), ("CABLE_DISPLAY", "BASE_SHELL"),
    ("CABLE_POWER", "ENV_POWER_ELECTRONICS"), ("CABLE_BATTERY", "ENV_POWER_ELECTRONICS"),
    ("CABLE_BATTERY", "ENV_BATTERY_BAY"),
    ("KEEPOUT_PORTS_MAIN", "PORT_PANEL_MAIN"), ("KEEPOUT_PORTS_AUX", "PORT_PANEL_AUX"),
    ("KEEPOUT_PORTS_MAIN", "BASE_SHELL"), ("KEEPOUT_PORTS_AUX", "BASE_SHELL"),
    ("KEEPOUT_PORTS_MAIN", "CABLE_TRUNK"), ("KEEPOUT_PORTS_AUX", "CABLE_TRUNK"),
    ("KEEPOUT_PORTS_AUX", "CABLE_POWER"),          # external power input on the aux panel -> power electronics
]}
FIT = {frozenset(p) for p in [("ENV_KEYBOARD", "BASE_SHELL"), ("ENV_TRACKPAD", "BASE_SHELL")]}

# Service groups: removed together, through which panel (or upward through the deck opening).
SERVICE = [
    ("compute (Pi stack on sled + duct)", ["ENV_PI_STACK", "COMPUTE_SLED", "KEEPOUT_COOLING_DUCT"], "SERVICE_PANEL_MAIN"),
    ("compute power", ["ENV_COMPUTE_POWER"], "SERVICE_PANEL_MAIN"),
    ("power electronics", ["ENV_POWER_ELECTRONICS"], "SERVICE_PANEL_MAIN"),
    ("GNSS module", ["ENV_GNSS_MODULE"], "SERVICE_PANEL_MAIN"),
    ("battery", ["ENV_BATTERY_BAY"], "BATTERY_DOOR"),
    ("keyboard (upward)", ["ENV_KEYBOARD"], "UP"),
    ("trackpad (upward)", ["ENV_TRACKPAD"], "UP"),
]
# Assembly: installed from below into the empty shell, in this order (shell obstacles only).
ASSEMBLY = ["KEYBOARD_TRAY", "TRACKPAD_TRAY", "COMPUTE_SLED", "PANEL_STANDOFF_L", "PANEL_STANDOFF_R"]


# ---------------------------------------------------------------- evaluation
def evaluate():
    env = dict(PARAMS)
    for name, expr in DERIVED:
        env[name] = _eval_formula(expr, name, lambda k: env[k])
    parts = []
    for name, cat, prims in PARTS:
        out = []
        for kind, label, coords in prims:
            v = [_eval_formula(e, f"{name}.{label}", lambda k: env[k]) for e in coords]
            if kind == "box":
                assert v[0] < v[3] and v[1] < v[4] and v[2] < v[5], f"{name}.{label}: empty box {v}"
            else:
                assert v[2] > 0 and v[3] < v[4], f"{name}.{label}: bad cylinder {v}"
            out.append((kind, label, v))
        parts.append((name, cat, out))
    return env, parts


def _ivl(a0, a1, b0, b1):
    """(gap, overlap) of two intervals; gap > 0 if separated, overlap > 0 if they share length."""
    return max(0.0, b0 - a1, a0 - b1), min(a1, b1) - max(a0, b0)


def _xy(p):
    k, _, v = p
    return ("rect", v[0], v[1], v[3], v[4]) if k == "box" else ("disk", v[0], v[1], v[2] / 2)


def _zr(p):
    k, _, v = p
    return (v[2], v[5]) if k == "box" else (v[3], v[4])


def prim_dist(p, q):
    """(distance, overlaps) between two primitives; exact for box/vertical-cylinder products."""
    a, b = _xy(p), _xy(q)
    if a[0] == "disk" and b[0] == "rect":
        a, b = b, a
    if a[0] == "rect" and b[0] == "rect":
        gx, ox = _ivl(a[1], a[3], b[1], b[3])
        gy, oy = _ivl(a[2], a[4], b[2], b[4])
        dxy, oxy = math.hypot(gx, gy), ox > EPS and oy > EPS
    elif a[0] == "rect":
        cx, cy, r = b[1], b[2], b[3]
        ex, ey = max(a[1] - cx, 0.0, cx - a[3]), max(a[2] - cy, 0.0, cy - a[4])
        c = math.hypot(ex, ey)
        dxy, oxy = max(0.0, c - r), c < r - EPS
    else:
        c = math.hypot(a[1] - b[1], a[2] - b[2])
        dxy, oxy = max(0.0, c - a[3] - b[3]), c < a[3] + b[3] - EPS
    gz, oz = _ivl(*_zr(p), *_zr(q))
    return math.hypot(dxy, gz), oxy and oz > EPS


def part_dist(pa, pb):
    d, ov = math.inf, False
    for p in pa:
        for q in pb:
            dd, oo = prim_dist(p, q)
            d, ov = min(d, dd), ov or oo
    return (0.0 if ov else d), ov


def bbox(prims):
    lo, hi = [math.inf] * 3, [-math.inf] * 3
    for k, _, v in prims:
        a = (v[0], v[1], v[2], v[3], v[4], v[5]) if k == "box" else (
            v[0] - v[2] / 2, v[1] - v[2] / 2, v[3], v[0] + v[2] / 2, v[1] + v[2] / 2, v[4])
        for i in range(3):
            lo[i], hi[i] = min(lo[i], a[i]), max(hi[i], a[i + 3])
    return lo, hi


def rule(a, ca, b, cb):
    """Required minimum distance for a pair, or None if the pair is not checked. 0 = contact allowed."""
    pair = frozenset((a, b))
    cats = {ca, cb}
    if "X" in cats:
        return 0.0                                 # external zones: must not overlap anything
    if "W" in cats:
        return None if "BASE_SHELL" in pair else 0.0
    if cats == {"C"}:
        return None                                # corridors join each other
    if pair in SERVE:
        return 0.0
    if pair in FIT:
        return PARAMS["CLEARANCE"]
    if cats == {"S"}:
        return 0.0                                 # separate structural parts may touch, never overlap
    if "H" in cats and cats & {"S"}:
        return 0.0                                 # hinge reserve sits against the shell/panel
    return PARAMS["MIN_GAP"]


def pair_table(parts):
    rows = []
    for i in range(len(parts)):
        for j in range(i + 1, len(parts)):
            (a, ca, pa), (b, cb, pb) = parts[i], parts[j]
            d, ov = part_dist(pa, pb)
            rows.append((i, j, a, b, ca, cb, d, ov, rule(a, ca, b, cb)))
    return rows


def _in_panel(fp, panel_prims):
    """Footprint rectangle fully covered by the (non-overlapping) panel rectangles."""
    x0, y0, x1, y1 = fp
    area = 0.0
    for k, _, v in panel_prims:
        ox, oy = min(x1, v[3]) - max(x0, v[0]), min(y1, v[4]) - max(y0, v[1])
        area += max(0.0, ox) * max(0.0, oy)
    return abs(area - (x1 - x0) * (y1 - y0)) < 1e-6


def prism_hits(prim, obstacles, up, top):
    """Obstacles (name.label) intersecting the vertical prism below (or above) a primitive's footprint."""
    lo, hi = bbox([prim])
    z = (hi[2], top + 1) if up else (-1.0, lo[2])
    probe = ("box", "prism", [lo[0], lo[1], z[0], hi[0], hi[1], z[1]])
    return [f"{n}.{q[1]}" for n, q in obstacles if prim_dist(probe, q)[1]]


def lid_polys(T):
    D, H, G = PARAMS["BODY_DEPTH"], PARAMS["BODY_HEIGHT"], PARAMS["LID_CLOSED_GAP"]
    dc = D / 2 - PARAMS["DISPLAY_VERTICAL_OFFSET"]
    return (hm.rect(0, D, H + G, H + G + T),
            hm.rect(dc - PARAMS["DISPLAY_HEIGHT"] / 2, dc + PARAMS["DISPLAY_HEIGHT"] / 2, H + G, H + G + PARAMS["DISPLAY_THICKNESS"]))


def yz_rect(prims):
    lo, hi = bbox(prims)
    return hm.rect(lo[1], hi[1], lo[2], hi[2])


def lid_clearance(parts, T, angles, cats):
    axis = (PARAMS["BODY_DEPTH"] - PARAMS["HINGE_AXIS_OFFSET"], PARAMS["BODY_HEIGHT"] + PARAMS["HINGE_AXIS_HEIGHT"])
    res = {}
    for ang in angles:
        polys = [hm.rotate(p, axis, ang) for p in lid_polys(T)]
        best = (math.inf, None)
        for name, cat, prims in parts:
            if cat not in cats:
                continue
            for p in prims:                         # every primitive's Y-Z silhouette (lid spans full X)
                for lp in polys:
                    s = hm.signed_clearance(lp, yz_rect([p]))
                    if s < best[0]:
                        best = (s, f"{name}.{p[1]}")
        res[ang] = best
    return res


# ---------------------------------------------------------------- checks + report
def run_checks(env, parts):
    by = {n: (c, p) for n, c, p in parts}
    fails, lines = [], []

    def ok(cond, msg):
        (lines if cond else fails).append(("PASS " if cond else "FAIL ") + msg)

    # 1. connectivity of each part's primitives (one solid per part)
    for n, c, prims in parts:
        comp, seen = 0, set()
        for i in range(len(prims)):
            if i in seen:
                continue
            comp += 1
            stack = [i]
            seen.add(i)
            while stack:
                k = stack.pop()
                for m in range(len(prims)):
                    if m not in seen and prim_dist(prims[k], prims[m])[0] <= EPS:
                        seen.add(m)
                        stack.append(m)
        if comp != 1:
            fails.append(f"FAIL {n}: {comp} disconnected pieces")
    lines.append("PASS every part is one connected solid" if not any("disconnected" in f for f in fails) else "")

    # 2. containment in the outer envelope (all but external zones)
    W2, D, H = env["W2"], PARAMS["BODY_DEPTH"], PARAMS["BODY_HEIGHT"]
    bad = []
    for n, c, prims in parts:
        if c == "X":
            continue
        lo, hi = bbox(prims)
        if lo[0] < -W2 - EPS or hi[0] > W2 + EPS or lo[1] < -EPS or hi[1] > D + EPS or lo[2] < -EPS or hi[2] > H + EPS:
            bad.append(n)
    ok(not bad, f"all internal parts inside the {2 * W2:g} x {D:g} x {H:g} envelope" + (f": {bad}" if bad else ""))

    # 3. pairwise rules
    rows = pair_table(parts)
    viol = [r for r in rows if r[8] is not None and (r[7] or r[6] < r[8] - EPS)]
    for r in viol:
        fails.append(f"FAIL {r[2]} x {r[3]}: {'OVERLAP' if r[7] else f'gap {r[6]:.3f}'} (needs >= {r[8]:g})")
    checked = sum(1 for r in rows if r[8] is not None)
    lines.append(f"{'PASS' if not viol else 'FAIL'} pair rules: {checked} pairs checked, {len(viol)} violations")

    # 4. primitive-level: vents/pass-through zones free of bosses; hinge reserves vs cables
    bosses = [(n, p) for n, c, pr in parts if n == "BASE_SHELL" for p in pr if p[1].startswith("boss_")]
    for n, c, prims in parts:
        if c == "W":
            hits = [f"{bn}.{bp[1]}" for bn, bp in bosses for p in prims if prim_dist(p, bp)[0] < PARAMS["MIN_GAP"] - EPS]
            ok(not hits, f"{n} clear of bosses by >= MIN_GAP" + (f": {hits}" if hits else ""))

    # 5. service access: straight down through the named panel, or up through the deck opening
    obstacles_all = [(n, p) for n, c, pr in parts if c in "SEHK" for p in pr]
    for label, group, panel in SERVICE:
        issues = []
        for g in group:
            for p in by[g][1]:
                lo, hi = bbox([p])
                if panel != "UP" and not _in_panel((lo[0], lo[1], hi[0], hi[1]), by[panel][1]):
                    issues.append(f"{g} footprint not inside {panel}")
                obst = [(n, q) for n, q in obstacles_all if n not in group and n != panel]
                hits = prism_hits(p, obst, panel == "UP", H)
                if hits:
                    issues.append(f"{g} path blocked by {sorted(set(hits))}")
        ok(not issues, f"service: {label} via {panel}" + (f": {issues}" if issues else ""))

    # 6. nothing internal is trapped: every E/K/H footprint is under a removable panel, with no shell below
    opening = [("box", "opening", [-env["IX"], env["IY0"], 0, env["IX"], env["IY1"], env["IZ0"]])]
    shell = [("BASE_SHELL", p) for p in by["BASE_SHELL"][1]]
    trapped = []
    for n, c, prims in parts:
        if c not in "EKHC" or n in ("KEEPOUT_PORTS_MAIN", "KEEPOUT_PORTS_AUX", "ENV_KEYBOARD", "ENV_TRACKPAD"):
            continue
        for p in prims:
            lo, hi = bbox([p])
            if not _in_panel((lo[0], lo[1], hi[0], hi[1]), opening) or prism_hits(p, shell, False, H):
                trapped.append(n)
    ok(not trapped, "no reserve trapped behind permanent geometry (all inside the bottom opening, no shell below)" + (f": {sorted(set(trapped))}" if trapped else ""))

    # 7. assembly from below into the empty shell
    for n in ASSEMBLY:
        hits = [h for p in by[n][1] for h in prism_hits(p, shell, False, H)]
        ok(not hits, f"assembly: {n} installs from below" + (f": blocked by {sorted(set(hits))}" if hits else ""))

    # 8. wall thickness vs MIN_WALL; shell printable deck-down (every primitive reaches the deck plane)
    mw = PARAMS["MIN_WALL"]
    walls = {"WALL_THICKNESS (walls, deck, bulkheads, battery wall)": PARAMS["WALL_THICKNESS"],
             "SERVICE_PANEL_THICKNESS (panel, door)": PARAMS["SERVICE_PANEL_THICKNESS"],
             "MOUNT_PLATE_THICKNESS (trays, sled)": PARAMS["MOUNT_PLATE_THICKNESS"]}
    for k, v in walls.items():
        ok(v >= mw - EPS, f"thickness {k} = {v:g} >= MIN_WALL {mw:g}")
    # Deck-down print: a primitive is supported if its top face (print bottom) is on the deck plane or
    # fully covered by primitives already supported that sit directly above it (a chain to the deck).
    sh = by["BASE_SHELL"][1]
    supported = {i for i, p in enumerate(sh) if bbox([p])[1][2] >= env["IZ1"] - EPS}
    changed = True
    while changed:
        changed = False
        for i, p in enumerate(sh):
            if i in supported:
                continue
            lo, hi = bbox([p])
            above = [q for j, q in enumerate(sh) if j in supported and q[0] == "box" and abs(bbox([q])[0][2] - hi[2]) < EPS]
            if p[0] == "box" and _in_panel((lo[0], lo[1], hi[0], hi[1]), above):
                supported.add(i)
                changed = True
    floating = [p[1] for i, p in enumerate(sh) if i not in supported]
    ok(not floating, "shell prints deck-down with no overhang or bridge (every primitive chains to the deck)"
       + (f": {floating}" if floating else ""))

    # 9. closed lid: nothing above the base top; module tops vs the lid display face
    top = max(bbox(p)[1][2] for n, c, p in parts if c != "X")
    ok(top <= H + EPS, f"closed lid: base max Z {top:g} <= BODY_HEIGHT {H:g}")
    for mod, rec in (("keyboard", "KEYBOARD_TOP_RECESS"), ("trackpad", "TRACKPAD_TOP_RECESS")):
        g = PARAMS["LID_CLOSED_GAP"] + PARAMS[rec]
        ok(g >= PARAMS["MIN_GAP"] - EPS, f"closed lid: {mod} top to display face {g:g} >= MIN_GAP")

    # 10. lid sweep (Round A lid, D-006 working hinge) vs base parts and external plug zones
    step = 1.0
    angs = [i * step for i in range(int(PARAMS["LID_ANGLE_MAX"] / step) + 1)]
    lb = lid_clearance(parts, PARAMS["LID_THICKNESS"], angs, "SEHKCW")
    worst = min(lb.values(), key=lambda t: t[0])
    ok(worst[0] >= PARAMS["MIN_GAP"] - EPS, f"lid sweep 0..{PARAMS['LID_ANGLE_MAX']:g} deg vs base parts: min {worst[0]:.3f} ({worst[1]})")
    lp = lid_clearance(parts, PARAMS["LID_THICKNESS"], angs, "X")
    worstp = min(lp.values(), key=lambda t: t[0])
    ang_p = min(lp, key=lambda a: lp[a][0])
    msg = f"lid sweep vs rear plug keep-outs: min {worstp[0]:.3f} at {ang_p:g} deg"
    if worstp[0] >= PARAMS["MIN_GAP"] - EPS:
        ok(True, msg)
    elif worstp[0] >= KNOWN_PLUG_CONFLICT_FLOOR - EPS:
        # OPEN CONFLICT, deliberately NOT resolved (Round E decision 4): the enclosed lid (Round D.1) enters the 45 mm
        # rear-plug keep-out near LID_ANGLE_MAX at h 0 (C.2 / D.1 modeled). Reported on every run; it becomes a FAIL
        # again if it gets worse than the documented case.
        lines.append("OPEN CONFLICT (known, C.2 / D.1; left visible in Round E) " + msg)
    else:
        ok(False, msg + f" (worse than the documented open conflict {KNOWN_PLUG_CONFLICT_FLOOR:g})")

    return fails, [ln for ln in lines if ln], rows, (lb, lp)


def sensitivity(parts):
    """Rear-port height budget vs lid thickness at LID_ANGLE_MAX (D-006 working hinge)."""
    out = []
    axis = (PARAMS["BODY_DEPTH"] - PARAMS["HINGE_AXIS_OFFSET"], PARAMS["BODY_HEIGHT"] + PARAMS["HINGE_AXIS_HEIGHT"])
    for T, why in ((PARAMS["LID_THICKNESS"], "LID_THICKNESS working"), (31.5, "B.1 V1 lid"), (42.5, "B.2 Concept C lid")):
        lid = hm.rotate(lid_polys(T)[0], axis, PARAMS["LID_ANGLE_MAX"])
        low = min(z for y, z in lid if y > PARAMS["BODY_DEPTH"] - 1e-9) if any(y > PARAMS["BODY_DEPTH"] for y, _ in lid) else math.inf
        plug = lid_clearance(parts, T, [PARAMS["LID_ANGLE_NOMINAL"], PARAMS["LID_ANGLE_MAX"]], "X")
        out.append((T, why, low, plug[PARAMS["LID_ANGLE_MAX"]][0]))
    return out


# ---------------------------------------------------------------- FeatureScript generation
def _fs_expr(e):
    e = e.strip()
    if re.fullmatch(r"-?0", e):
        return "0 * millimeter"
    return re.sub(r"\b([A-Z][A-Z0-9_]*)\b", lambda m: m.group(1) if m.group(1) in PARAMS else f"BV_{m.group(1)}", e)


def emit_layout():
    lines = [BEGIN,
             "// Generated from CAD/tools/base_v01_layout.py (Round C base V0.1 layout). DO NOT EDIT.",
             "// Parametric: every coordinate is an expression over the GENERATED PARAMS constants.",
             "// Envelopes / keep-outs are reserves, not hardware; see prototypes/P0.1/base_v01_architecture.md."]
    for name, expr in DERIVED:
        lines.append(f"export const BV_{name} = {_fs_expr(expr)};")
    lines.append("// [part name, category, [[\"box\", label, x0, y0, z0, x1, y1, z1] | [\"cyl\", label, cx, cy, d, z0, z1], ...]]")
    lines.append("export function nomadBaseV01Parts() returns array")
    lines.append("{")
    lines.append("    return [")
    for pi, (name, cat, prims) in enumerate(PARTS):
        lines.append(f'        ["{name}", "{cat}", [')
        for qi, (kind, label, coords) in enumerate(prims):
            sep = "," if qi < len(prims) - 1 else ""
            lines.append(f'            ["{kind}", "{label}", ' + ", ".join(_fs_expr(c) for c in coords) + f"]{sep}")
        lines.append("        ]]" + ("," if pi < len(PARTS) - 1 else ""))
    lines.append("    ];")
    lines.append("}")
    lines.append(END)
    return "\n".join(lines)


def emit_expected(parts, rows, lid):
    lb, lp = lid
    names = [n for n, _, _ in parts]
    sel = [PARAMS["LID_ANGLE_NOMINAL"], PARAMS["LID_ANGLE_MAX"]]
    lines = [HBEGIN, "// Generated by CAD/tools/base_v01_layout.py --write. DO NOT EDIT.",
             "const BV_NAMES = [" + ", ".join(f'"{n}"' for n in names) + "];",
             "// [i, j, state O/T/G, exact gap mm or -1 if not compared]"]
    body = []
    for i, j, a, b, ca, cb, d, ov, r in rows:
        st = "O" if ov else ("T" if d <= EPS else "G")
        g = _num(round(d, 4)) if (not ov and d < NEAR) else "-1"
        body.append(f'[{i}, {j}, "{st}", {g}]')
    lines.append("const BV_PAIRS = [")
    for k in range(0, len(body), 6):
        lines.append("    " + ", ".join(body[k:k + 6]) + ("," if k + 6 < len(body) else ""))
    lines.append("];")
    vals = [lb[0][0]] + [lb[a][0] for a in sel] + [lp[a][0] for a in sel]
    lines.append("// lid (Round A) min signed clearance to base parts at 0 / NOMINAL / MAX, then to plug zones at NOMINAL / MAX")
    lines.append("const BV_LID = [" + ", ".join(_num(round(v, 4)) for v in vals) + "];")
    lines.append(HEND)
    return "\n".join(lines)


def splice(text, begin, end, block, path):
    pat = re.compile(re.escape(begin) + r".*?" + re.escape(end), re.S)
    if not pat.search(text):
        raise SystemExit(f"{path.name}: markers {begin!r} not found")
    return pat.sub(lambda _: block, text, count=1)


def main(argv):
    env, parts = evaluate()
    fails, lines, rows, lid = run_checks(env, parts)
    print(f"NOMAD base V0.1 (Round C) -- {len(parts)} parts, {sum(len(p) for _, _, p in parts)} primitives; "
          f"envelope {2 * env['W2']:g} x {PARAMS['BODY_DEPTH']:g} x {PARAMS['BODY_HEIGHT']:g} (working)")
    for ln in lines:
        print("  " + ln)
    for f in fails:
        print("  " + f)
    print("\nkey clearances (modeled):")
    key = [("ENV_PI_STACK", "BASE_SHELL"), ("ENV_PI_STACK", "ENV_COMPUTE_POWER"), ("ENV_BATTERY_BAY", "ENV_POWER_ELECTRONICS"),
           ("ENV_POWER_ELECTRONICS", "ENV_GNSS_MODULE"), ("ENV_BATTERY_BAY", "BASE_SHELL"), ("ENV_KEYBOARD", "BASE_SHELL"),
           ("ENV_TRACKPAD", "BASE_SHELL"), ("KEEPOUT_COOLING_DUCT", "BASE_SHELL"), ("CABLE_COMPUTE", "BASE_SHELL"),
           ("CABLE_TRUNK", "KEEPOUT_HINGE_MOUNT_R"), ("CABLE_DISPLAY", "KEEPOUT_HINGE_MOUNT_L"),
           ("KEEPOUT_PORTS_MAIN", "KEEPOUT_HINGE_MOUNT_R"), ("ENV_PI_STACK", "ENV_BATTERY_BAY")]
    idx = {frozenset((r[2], r[3])): r for r in rows}
    for a, b in key:
        r = idx[frozenset((a, b))]
        print(f"  {a:<24} x {b:<24} {'OVERLAP' if r[7] else f'{r[6]:8.3f}'}")
    print("\nheights available (Z, modeled):")
    print(f"  palm-rest bays: {env['IZ1'] - env['IZ0']:g} (panel {env['IZ0']:g} .. deck {env['IZ1']:g}); "
          f"Pi stack envelope {env['PIW']:g} x {env['PID']:g} x {PARAMS['PI_STACK_HEIGHT']:g} on sled top {env['SLZ1']:g}")
    print(f"  under keyboard tray: {env['KTZ0'] - env['IZ0']:g} (panel .. tray underside {env['KTZ0']:g})")
    print(f"  under trackpad tray: {env['TTZ0'] - env['IZ0']:g}")
    print(f"  port keep-out depth {env['IY1'] - env['TRY1']:g} (>= PORT_KEEPOUT_DEPTH {PARAMS['PORT_KEEPOUT_DEPTH']:g}: "
          f"{'yes' if env['IY1'] - env['TRY1'] >= PARAMS['PORT_KEEPOUT_DEPTH'] - EPS else 'NO'}); cooling duct "
          f"{env['PIY0'] - env['DUY0']:g} deep, {env['DUY0'] - env['IY0']:g} behind the front wall")
    print("\nrear ports vs lid thickness at LID_ANGLE_MAX (D-006 working hinge; modeled):")
    for T, why, low, plug in sensitivity(parts):
        print(f"  T {T:5.1f} ({why:<22}) lid lowest Z behind the base {low:6.2f}; clearance to plug zone "
              f"(top Z {env['PZ1']:g}) {plug:7.3f} -> {'ok' if plug >= PARAMS['MIN_GAP'] - EPS else 'CONFLICT'}")
    lb, lp = lid
    print(f"\nlid min clearance to base parts: 0 deg {lb[0][0]:.3f}, {PARAMS['LID_ANGLE_NOMINAL']:g} deg "
          f"{lb[PARAMS['LID_ANGLE_NOMINAL']][0]:.3f}, {PARAMS['LID_ANGLE_MAX']:g} deg {lb[PARAMS['LID_ANGLE_MAX']][0]:.3f}")

    status = 0 if not fails else 1
    layout, expected = emit_layout(), emit_expected(parts, rows, lid)
    fs_path, h_path = FS_PATH, HARNESS_PATH
    if "--target" in argv:                 # Round E: the same blocks in another FeatureScript file / harness
        fs_path = FS_PATH.parent / argv[argv.index("--target") + 1]
    if "--harness" in argv:
        h_path = FS_PATH.parent / argv[argv.index("--harness") + 1]
    fs_text, h_text = fs_path.read_text(encoding="utf-8"), h_path.read_text(encoding="utf-8")
    fs_new = splice(fs_text, BEGIN, END, layout, fs_path)
    h_new = splice(h_text, HBEGIN, HEND, expected, h_path)
    if "--write" in argv:
        for path, old, new in ((fs_path, fs_text, fs_new), (h_path, h_text, h_new)):
            if new != old:
                path.write_text(new, encoding="utf-8", newline="\n")
                print(f"wrote {path.relative_to(ROOT)}")
    elif "--check" in argv:
        for path, old, new in ((fs_path, fs_text, fs_new), (h_path, h_text, h_new)):
            if new != old:
                print(f"{path.name}: generated block OUT OF DATE")
                status = 1
    known = [ln for ln in lines if ln.startswith("OPEN CONFLICT")]
    print(("\nALL CHECKS PASSED" if not fails else f"\n{len(fails)} CHECK(S) FAILED")
          + (f"; {len(known)} KNOWN OPEN CONFLICT(S) REPORTED ABOVE (not resolved)" if known else ""))
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
