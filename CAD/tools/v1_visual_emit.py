"""NOMAD V1 visual master model: data generator for the Onshape Feature Studio NOMAD_V1_Visual (standard library).

  py CAD/tools/v1_visual_emit.py            print the part / cable / conflict report
  py CAD/tools/v1_visual_emit.py --write    (re)write the GENERATED V1 VISUAL DATA block in CAD/featurescript/NOMAD_V1_Visual.fs
  py CAD/tools/v1_visual_emit.py --check    exit 1 if that block is out of date

Every coordinate comes from the V1 integration model (CAD/tools/v1_integration.py -> CAD/parameters/nomad.yaml +
prototypes/V1/v1_hardware.py) or from a named, sourced constant below. The B1 / SB-261 hinge rail, leaf and lid hinge
region are NOT generated here: the Feature Studio carries the kernel-validated SB-261 code (prototypes/B1_SB261/src/fs/
b1_common.fs) unchanged except for the V1 lid width / depth. This is a VISUALIZATION model, not production CAD.

Status tags (shown in every part name and, optionally, as colours):
  ENGINEERED   our own V1 design geometry from the integration model (printed parts, layout) - modelled, not physically tested
  SELECTED     a selected / candidate commercial part drawn from manufacturer data - not bought, not physically validated
  PLACEHOLDER  needs data: no exact part / PCB / drawing exists; the envelope is honest but conceptual
  CONFLICT     two sources disagree; shown so it is not hidden
"""
import importlib.util
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FS_PATH = ROOT / "CAD" / "featurescript" / "NOMAD_V1_Visual.fs"
BEGIN, END = "// BEGIN GENERATED V1 VISUAL DATA", "// END GENERATED V1 VISUAL DATA"

_s = importlib.util.spec_from_file_location("v1i", HERE / "v1_integration.py")
VI = importlib.util.module_from_spec(_s)
_s.loader.exec_module(VI)
VI.build_index()
P, B = VI.P, VI.BOXES_D
HW = VI.HW

W, D, H = VI.W, VI.D, VI.H
W2 = W / 2
WT, PT = VI.WT, VI.PT
IX, IY0, IY1, IZ0, IZ1 = VI.IX, VI.IY0, VI.IY1, VI.IZ0, VI.IZ1
ZF, CORE = VI.ZF, VI.CORE
HAY, HAZ = VI.HAY, VI.HAZ

# ---- AUO G101UAN01.0 product specification rev. 1.5 (2021-07-28, MFR, via Avnet) - supersedes the 3P envelope in nomad.yaml
DSP = {"w": 228.22, "h": 148.32, "t": 5.35, "aw": 216.81, "ah": 135.50, "mass": 140}
DSP_YC = D / 2 - P["DISPLAY_VERTICAL_OFFSET"]
DSP_Y0, DSP_Y1 = DSP_YC - DSP["h"] / 2, DSP_YC + DSP["h"] / 2
DSP_Z0 = ZF + P["DISPLAY_BEZEL_LIP"]
DSP_Z1 = DSP_Z0 + DSP["t"]

ENG, SEL, PH, CF = "ENGINEERED", "SELECTED", "PLACEHOLDER", "CONFLICT"
PARTS = []      # [pid, name, group, explodeKey, colorKey, status, stages]


def part(pid, name, group, ek, ck, status, *stages):
    PARTS.append([pid, name, group, ek, ck, status, [list(s) for s in stages]])


def bx(x0, y0, z0, x1, y1, z1):
    return ["B", min(x0, x1), min(y0, y1), min(z0, z1), max(x0, x1), max(y0, y1), max(z0, z1)]


def cyl(p0, p1, r):
    return ["C", p0[0], p0[1], p0[2], p1[0], p1[1], p1[2], r]


def dia(axis, a0, a1, c1, c2, h):
    return ["D" + axis, a0, a1, c1, c2, h]


def ob(name, grow=0.0):
    b = B[name]
    return bx(b[2] - grow, b[4] - grow, b[6] - grow, b[3] + grow, b[5] + grow, b[7] + grow)


# =====================================================================================================================
# BASE SHELL (one printed part: walls, deck, bulkheads, bay wall, hinge corner blocks, bosses, openings, ports, vents)
# =====================================================================================================================
KB0, KB1 = VI.KBY0, VI.KBY1
TP0, TP1 = VI.TPY0, VI.TPY1
CL = P["CLEARANCE"]
SOUTHCO_X = IX - P["HINGE_MOUNT_WIDTH"] / 2          # hinge centred on its corner block
SOUTHCO_L = 38.0                                      # MFR catalogue, E6-10 medium length
SOUTHCO_R = P["HINGE_BARREL_DIAMETER"] / 2

shell_add = [bx(-W2, 0, 0, W2, D, H)]
shell_cut = [
    bx(-IX, IY0, -1, IX, IY1, IZ1),                                                     # hollow, open bottom
    bx(-VI.KBX - CL, KB0 - CL, IZ1 - 1, VI.KBX + CL, KB1 + CL, H + 1),                  # keyboard opening
    bx(-VI.TPX - CL, TP0 - CL, IZ1 - 1, VI.TPX + CL, TP1 + CL, H + 1),                  # trackpad opening
]
# Vertical corner chamfers 8 (front) / 5 (rear) on a 2.5 wall: cut after the hollow they would open the front corners and
# leave a non-manifold edge at the rear (5 = 2 x 2.5; Onshape BOOLEAN_NON_MANIFOLD_RESULT, 2026-10-08). The wall is kept
# 2.5 thick behind each chamfer by an inner corner fill (45 deg, leg L - WT * (2 - sqrt 2)) added before the exterior cut.
# Corner chamfers are visual styling only (no nomad.yaml parameter). The front ones are an edge break: the fan sits flush in the
# front-right corner (ENV_FAN) and the battery holder 4 mm from the front-left one, so a large front chamfer would cut into them
# (kernel QA 2026-10-08: 8 mm -> fan intrusion ~4.6 mm). A 1.5 break leaves the wall >= 2.47 thick, so it needs no fill.
CH_F, CH_R = 1.5, 5.0
FILL_F, FILL_R = CH_F - WT * (2 - math.sqrt(2)), CH_R - WT * (2 - math.sqrt(2))
corner_fill = [dia("Z", 0, H, sx * IX, IY1, FILL_R) for sx in (-1, 1)]
if FILL_F > 0.5:
    corner_fill += [dia("Z", 0, H, sx * IX, IY0, FILL_F) for sx in (-1, 1)]
shell_ext = [
    dia("X", -W2 - 1, W2 + 1, 0, H, 3.0),                                               # 3 x 45 top front edge
    dia("Y", -1, D + 1, -W2, H, 3.0), dia("Y", -1, D + 1, W2, H, 3.0),                  # top side edges
    dia("Z", -1, H + 1, -W2, 0, CH_F), dia("Z", -1, H + 1, W2, 0, CH_F),                # vertical front corners
    dia("Z", -1, H + 1, -W2, D, CH_R), dia("Z", -1, H + 1, W2, D, CH_R),                # vertical rear corners
    dia("X", -W2 - 1, W2 + 1, 0, 0, 1.5), dia("X", -W2 - 1, W2 + 1, D, 0, 1.5),         # bottom edge breaks
]
shell_add2 = [ob("BULKHEAD_L"), ob("BULKHEAD_R"), ob("BATTERY_BAY_REAR_WALL"),
              ob("HINGE_BLOCK_L"), ob("HINGE_BLOCK_R")]
# representative M3 boss set at PANEL_SCREW_INSET from the walls, placed only in free zones (V1 F1 fix)
INS = P["PANEL_SCREW_INSET"]
BOSS_R = P["BOSS_DIAMETER"] / 2
DOOR_BOSSES = [(-50.5, 25.0), (-50.5, 70.0)]                    # battery door: 2 screws into the bulkhead + 2 front/left hooks
for x, y in DOOR_BOSSES:
    shell_add2.append(cyl((x, y, PT), (x, y, PT + 15), BOSS_R))   # short: stays below the trackpad tray
BOSSES = [(30, IY0 + INS), (110, IY0 + INS),
          (-95, IY1 - INS), (30, IY1 - INS), (95, IY1 - INS),
          (-IX + INS, 170), (-IX + INS, 210), (IX - INS, 160), (IX - INS, 205), (IX - INS, 100)]
for x, y in BOSSES:
    top = VI.KTZ0 if VI.KTY0 <= y <= VI.KTY1 else IZ1 + 0.5          # under the keyboard tray: tray posts
    shell_add2.append(cyl((x, y, PT), (x, y, top), BOSS_R))
# openings that must be cut after the internal structure is added
FAN = B["ENV_FAN"]
USBC_ZC = B["ENV_POWER_ELEC"][6] + 2.0 + 1.6 + 1.5   # receptacle centre on the power board (see usbcIn); inside W_PORT_USB_C_LEFT
shell_cut2 = [
    bx(-W2 - 1, 108.5, USBC_ZC - 1.75, -IX + 0.6, 117.5, USBC_ZC + 1.75),             # USB-C charge input (left wall)
    cyl((-W2 - 1, B["ENV_BUTTON"][4] + 7, 12.5), (-IX + 0.6, B["ENV_BUTTON"][4] + 7, 12.5), 6.2),   # power button
    bx(64.0, -1, 10.0, 77.5, IY0 + 0.6, 16.5), bx(82.0, -1, 10.0, 95.5, IY0 + 0.6, 16.5),          # 2 x USB-A (front right)
    bx(48 - 0.2, 40, 5.0, 50.5 + 0.2, 90, 22.5),                                      # bulkhead R: Pi USB plug pass-through
    bx(48 - 0.2, 20, 8.0, 50.5 + 0.2, 34, 21.0),                                      # bulkhead R: USB 3 extension pass
    bx(-12, D - WT - 0.6, 24, 12, D + 1, 38),                                         # display / solar cable pass to the knuckle
    bx(-150.0, B["BATTERY_BAY_REAR_WALL"][4] - 0.5, IZ0 + 1, -129.0, B["BATTERY_BAY_REAR_WALL"][5] + 0.5, IZ0 + 16),  # battery-lead slot
]
for k in range(5):                                                                   # fan exhaust grille, right wall
    z = FAN[6] + 3 + k * 5.5
    shell_cut2.append(bx(IX - 0.6, FAN[4] + 3, z, W2 + 1, FAN[5] - 3, z + 3))
for k in range(10):                                                                  # rear intake grille
    x = -55 + k * 11.5
    shell_cut2.append(bx(x, D - WT - 0.6, 6.0, x + 6, D + 1, 18.0))
shell_cut2.append(cyl((-12.5, HAY, HAZ), (12.5, HAY, HAZ), 6.5))                       # knuckle notch on the hinge axis
for sx in (-1, 1):                                                                   # Southco base-leaf pockets (rear face)
    shell_cut2.append(cyl((sx * SOUTHCO_X - SOUTHCO_L / 2 - 0.5, HAY, HAZ), (sx * SOUTHCO_X + SOUTHCO_L / 2 + 0.5, HAY, HAZ),
                          SOUTHCO_R + 0.5))                                        # barrel notch
    c = sx * SOUTHCO_X
    shell_cut2.append(bx(c - SOUTHCO_L / 2 - 0.3, D - 3.3, 21.7, c + SOUTHCO_L / 2 + 0.3, D + 1, H - 1.5))
part("shell", "BASE | shell (walls, deck, bulkheads, hinge corner blocks, bosses) PETG 2.5 [355 g EST]", "base", "",
     "shell", ENG, ["+", shell_add], ["-", shell_cut], ["+", corner_fill], ["-", shell_ext], ["+", shell_add2], ["-", shell_cut2])

for nm, key, label in (("KEYBOARD_TRAY", "kbtray", "keyboard tray 2.0"), ("TRACKPAD_TRAY", "tptray", "trackpad tray 2.0")):
    part(key, f"BASE | {label} (lifts out upward with its device)", "base", "kb" if key == "kbtray" else "tp", "tray", ENG,
         ["+", [ob(nm)]])
# service closures with intake slots, sled pocket and screw heads
main = B["SERVICE_PANEL_MAIN"]
mslots = [bx(60 + k * 9, 165, -1, 65 + k * 9, 205, PT + 1) for k in range(9)]
# closures are notched at the wall corners to clear the shell corner fill
part("panelMain", "SERVICE | main panel, rear (under the keyboard): power board, Beck, 5 V, GNSS; intake slots", "base", "panel",
     "panel", ENG, ["+", [ob("SERVICE_PANEL_MAIN")]],
     ["-", mslots + [dia("Z", -1, PT + 1, sx * IX, IY1, FILL_R) for sx in (-1, 1)]])
part("panelFront", "SERVICE | front panel (trackpad + compute bays) with compute-sled pocket", "base", "panel", "panel", ENG,
     ["+", [ob("SERVICE_PANEL_FRONT")]], ["-", [ob("COMPUTE_SLED", 0.2)] + ([dia("Z", -1, PT + 1, IX, IY0, FILL_F)] if FILL_F > 0.5 else [])])
part("door", "SERVICE | battery door (2 x M3 captive into the bulkhead + 2 edge hooks) - battery comes out downward", "base", "door", "door", ENG,
     ["+", [ob("BATTERY_DOOR")]], *([["-", [dia("Z", -1, PT + 1, -IX, IY0, FILL_F)]]] if FILL_F > 0.5 else []))
heads = [cyl((x, y, -1.65), (x, y, 0.02), 2.85) for x, y in BOSSES if not (x < -48 and y < VI.PALM_Y1)]
part("panelScrews", "FASTENERS | M3 ISO 7380 panel screws at PANEL_SCREW_INSET 3.5 (F1 fix; representative set, CONCEPT)", "base", "panel",
     "fastener", SEL, ["+", heads])
door_heads = [cyl((x, y, -1.65), (x, y, 0.02), 2.85) for x, y in DOOR_BOSSES]
part("doorScrews", "FASTENERS | battery door 2 x M3 captive screws into the bulkhead (+ 2 edge hooks, CONCEPT)", "base", "door", "fastener", SEL, ["+", door_heads])
feet = [cyl((sx * (W2 - 8), y, -4), (sx * (W2 - 8), y, 0.01), 6) for sx in (-1, 1) for y in (8, D - 8)]
part("feet", "BASE | rubber feet x4, 4 mm (ASSUMED)", "base", "", "rubber", SEL, ["+", feet])

# =====================================================================================================================
# INPUT DEVICES
# =====================================================================================================================
KBX = VI.KBX
kbz0, kbz1 = VI.KBZ0, VI.KBZ1
caps = []
rows = [(KB0 + 3, 16.5, 14), (KB0 + 21.5, 16.5, 14), (KB0 + 40, 16.5, 14), (KB0 + 58.5, 16.5, 14), (KB0 + 77, 16.5, 14)]
for (y, dy, n) in rows:
    pitch = (2 * KBX - 6) / n
    for i in range(n):
        x = -KBX + 3 + i * pitch
        caps.append(bx(x + 1, y, kbz1 - 2.6, x + pitch - 1, y + dy, kbz1))
for i in range(14):                                                                   # function row
    pitch = (2 * KBX - 6) / 14
    x = -KBX + 3 + i * pitch
    caps.append(bx(x + 1, KB0 + 96, kbz1 - 2.6, x + pitch - 1, KB0 + 105, kbz1))
caps[2 * 0 + 4: 2 * 0 + 10] = []                                                       # no-op guard (keep list type)
part("keyboard", "KEYBOARD | Perixx PERIBOARD-416, 285 x 117 x 16 per MFR manual (product page: 21 mm, 361 g - MEASURE) [332 g MFR]",
     "base", "kb", "keyboard", SEL, ["+", [bx(-KBX, KB0, kbz0, KBX, KB1, kbz1 - 2.5)] + caps])
KBC_X = 80.0                     # USB-C receptacle: rear edge, right of centre (EST from the Perixx product photo, 2026-10-08)
part("kbPlug", "KEYBOARD | USB-C right-angle plug at the rear edge (x ~ +80 EST from photo) [PLACEHOLDER position]", "base", "kb",
     "connector", PH, ["+", [bx(KBC_X - 6, KB1, 28, KBC_X + 6, KB1 + 9, 34)]])
TPX = VI.TPX
tz0, tz1 = VI.TPZ0, VI.TPZ1
part("trackpad", "TRACKPAD | Perixx PERIPAD-501 II, 86 x 75 x 13 (MFR manual), 2 buttons [60 g 3P]", "base", "tp", "keyboard", SEL,
     ["+", [bx(-TPX, TP0, tz0, TPX, TP1, tz1 - 0.6), bx(-TPX + 6, TP0 + 18, tz1 - 0.7, TPX - 6, TP1 - 4, tz1),
            bx(-TPX + 6, TP0 + 3, tz1 - 0.7, -1, TP0 + 15, tz1 - 0.2), bx(1, TP0 + 3, tz1 - 0.7, TPX - 6, TP0 + 15, tz1 - 0.2)]])
part("tpCoil", "TRACKPAD | excess 1.6 m USB lead, coiled + clipped (or shortened) [PLACEHOLDER]", "base", "tp", "cableUsb", PH,
     ["+", [cyl((-22, 50, 6), (-22, 50, 13), 14)]])

# =====================================================================================================================
# COMPUTE: Raspberry Pi 5 (rotated 180 deg: USB/ETH edge -> -X (bulkhead), HDMI/USB-C edge -> +Y (rear))
# =====================================================================================================================
pe = B["ENV_PI_STACK"]
m = P["PI_ENVELOPE_MARGIN"]
px0, py0 = pe[2] + m, pe[4] + m                       # PCB corner
pz = VI.PCB_Z
pz1 = pz + 1.6


def pr(x, y):                                          # standard Pi board coordinates -> world after the 180 deg rotation
    return px0 + (85 - x), py0 + (56 - y)


holes = [pr(3.5, 3.5), pr(61.5, 3.5), pr(3.5, 52.5), pr(61.5, 52.5)]
part("sled", "COMPUTE | sled plate 2.5 (insert in the front panel pocket; F2 fix) - Pi stack comes out downward", "base", "pi",
     "tray", ENG, ["+", [ob("COMPUTE_SLED")]])
part("piStandoffs", "COMPUTE | M2.5 standoffs 3 + 16 (Pi / HAT+)", "base", "pi", "metal", SEL,
     ["+", [cyl((x, y, IZ0 - 0.1), (x, y, pz + 0.05), 2.5) for x, y in holes] +
      [cyl((x, y, pz1 - 0.05), (x, y, pz1 + 16.05), 2.5) for x, y in holes]])
eth = pr(85, 45.75)
u1, u2 = pr(85, 27.0), pr(85, 9.0)
pi_add = [bx(px0, py0, pz, px0 + 85, py0 + 56, pz1),
          bx(px0 - 3, eth[1] - 8, pz1 - 0.1, px0 + 18, eth[1] + 8, pz1 + 13.5),          # Ethernet (unused in V1)
          bx(px0 - 3, u1[1] - 6.6, pz1 - 0.1, px0 + 14.5, u1[1] + 6.6, pz1 + 15.6),       # USB 3.0 x2 (stack)
          bx(px0 - 3, u2[1] - 6.6, pz1 - 0.1, px0 + 14.5, u2[1] + 6.6, pz1 + 15.6)]       # USB 2.0 x2 (stack)
for sx, w in ((11.2, 9.0), (25.8, 7.0), (39.2, 7.0)):                                # USB-C power, micro-HDMI 0 / 1
    cx_, cy_ = pr(sx, 0)
    pi_add.append(bx(cx_ - w / 2, cy_ - 7.5, pz1 - 0.1, cx_ + w / 2, cy_ + 1.0, pz1 + 3.4))
g0, g1 = pr(58.0, 52.5), pr(7.1, 52.5)
pi_add.append(bx(g0[0], g0[1] - 2.6, pz1 - 0.1, g1[0], g0[1] + 2.6, pz1 + 16.0))     # GPIO (16 mm stacking header)
part("pi5", "COMPUTE | Raspberry Pi 5 8 GB (ports per RPi drawing, approximate) [46 g EST]", "base", "pi", "pcb", SEL,
     ["+", pi_add])
soc = pr(29.0, 32.0)
part("cooler", "COMPUTE | Raspberry Pi Active Cooler 63.5 x 42.5 x 13.7 (MFR-DWG, interpreted) - blower exhausts sideways",
     "base", "pi", "cooler", SEL, ["+", [bx(px0 + 20, soc[1] - 21.25, pz1 + 0.05, px0 + 83.5, soc[1] + 21.25, pz1 + 13.7),
                                         cyl((px0 + 60, soc[1], pz1 + 13.6), (px0 + 60, soc[1], pz1 + 13.75), 14)]])
hat_x0 = pr(85, 0)[0] + 20 - 0.5
hatz = pz1 + 16
part("m2hat", "STORAGE | Raspberry Pi M.2 HAT+ 65 x 56.5 (0-50 C AMBIENT limit) + PCIe FPC", "base", "pi", "pcb", SEL,
     ["+", [bx(hat_x0, py0, hatz, hat_x0 + 65, py0 + 56.5, hatz + 1.6),
            bx(px0 + 85 - 0.5, py0 + 16, pz1, px0 + 85 + 0.6, py0 + 32, hatz + 0.1)]])
part("ssd", "STORAGE | Raspberry Pi SSD 512 GB M.2 2230 (replace: remove sled downward, then one M.2 screw)", "base", "pi", "ssd",
     SEL, ["+", [bx(hat_x0 + 18, py0 + 17, hatz + 1.6, hat_x0 + 48, py0 + 39, hatz + 3.75)]])
part("gpioPlug", "COMPUTE | GPIO harness housings, RIGHT-ANGLE 2.54 (vertical Dupont hits the deck: audit) [PLACEHOLDER]",
     "base", "pi", "connector", PH, ["+", [bx(g0[0] + 5, g0[1] - 1.5, hatz + 1.6, g0[0] + 25, g0[1] + 6, hatz + 9.6)]])
# plugs in the Pi ports (through the bulkhead openings into the volume under the trackpad)
plugs = []
for (uy, zlo) in ((u2[1], pz1 + 1.0), (u2[1], pz1 + 8.6), (u1[1], pz1 + 1.0), (u1[1], pz1 + 8.6)):
    plugs.append(bx(px0 - 3 - 21, uy - 6.0, zlo, px0 - 3 + 1, uy + 6.0, zlo + 6.0))
part("piUsbPlugs", "COMPUTE | USB-A plugs in the Pi (USB2: keyboard + trackpad; USB3: 2 external extensions)", "base", "pi",
     "connector", SEL, ["+", plugs])
cpc = pr(11.2, 0)
part("piPowerPlug", "POWER | 5.1 V into the Pi: right-angle USB-C power-only plug", "base", "pi", "connector", SEL,
     ["+", [bx(cpc[0] - 4.5, cpc[1] + 1.0, pz1 - 0.5, cpc[0] + 4.5, cpc[1] + 11, pz1 + 6)]])
hd0 = pr(25.8, 0)
part("piHdmiPlug", "DISPLAY | micro-HDMI plug (Pi HDMI0 -> Beck)", "base", "pi", "connector", SEL,
     ["+", [bx(hd0[0] - 4, hd0[1] + 1.0, pz1 - 0.5, hd0[0] + 4, hd0[1] + 12, pz1 + 5)]])

# =====================================================================================================================
# BATTERY: 4S1P Molicel M65A holder pack (E-POWER-002 s.11.1 holder build 91.6 x 80 x 28.9)
# =====================================================================================================================
bb = B["ENV_BATTERY_BAY"]
pk = (bb[2] + 1, bb[4] + 1, bb[6] + 1, bb[3] - 1, bb[5] - 1, bb[6] + 1 + 28.9)
cd, cl = 21.55, 70.21                                    # M65A MFR (preliminary)
ccx = (pk[0] + pk[3]) / 2
cyc = (pk[1] + pk[4]) / 2
czc = pk[2] + 1.2 + cd / 2
for i in range(4):
    x = ccx + (i - 1.5) * (cd + 0.25)
    part(f"cell{i}", f"BATTERY | Molicel INR-21700-M65A cell {i + 1} of 4 (4S1P, 23.0 Wh, 74.5 g MFR prelim.)", "base", "battery",
         "cell", SEL, ["+", [cyl((x, cyc - cl / 2, czc), (x, cyc + cl / 2, czc), cd / 2)]])
holder = [bx(pk[0], pk[1], pk[2], pk[3], pk[1] + 3.5, pk[2] + 24.5), bx(pk[0], pk[4] - 3.5, pk[2], pk[3], pk[4], pk[2] + 24.5),
          bx(pk[0], pk[1], pk[2], pk[3], pk[4], pk[2] + 1.2)]
part("holder", "BATTERY | 4S1P cell holder + base (custom pack SPEC; spot-welded by a competent assembler) [PLACEHOLDER]", "base",
     "battery", "holder", PH, ["+", holder])
part("nickel", "BATTERY | nickel strips (series links)", "base", "battery", "metal", PH,
     ["+", [bx(pk[0] + 2, pk[1] - 0.3, czc - 8, pk[3] - 2, pk[1] + 0.05, czc + 8),
            bx(pk[0] + 2, pk[4] - 0.05, czc - 8, pk[3] - 2, pk[4] + 0.3, czc + 8)]])
part("bms", "BATTERY | on-pack BMS (BQ77915-class 4S protector, NTC, 50 mA balance) + 10 A MINI fuse + Micro-Fit lead [PLACEHOLDER]",
     "base", "battery", "pcb", PH, ["+", [bx(pk[0] + 6, pk[1] + 8, pk[5] - 1.6, pk[3] - 6, pk[4] - 8, pk[5]),
                                         bx(pk[0] + 10, pk[4] - 18, pk[5] - 0.1, pk[0] + 21, pk[4] - 8, pk[5] + 0.0 + 0.0 + 0.1 + 0.0)]])
part("packConn", "BATTERY | Molex Micro-Fit 3.0 keyed latching pack connector (P+ P- NTC) - disconnect at the door", "base",
     "battery", "connector", SEL, ["+", [bx(-146, pk[4] + 0.4, 9, -134, pk[4] + 5.0, 17)]])

# =====================================================================================================================
# POWER ELECTRONICS
# =====================================================================================================================
pw = B["ENV_POWER_ELEC"]
pbz = pw[6] + 2.0
pcb = (pw[2], pw[4] + 0.5, pbz, pw[2] + 80, pw[4] + 40.5, pbz + 1.6)
part("powerPcb", "POWER | power board per TI TIDA-050047 (TPS25751 PD + BQ25798 4S NVDC/MPPT + TPS56339 5 V) - NO LAYOUT EXISTS "
     "[PLACEHOLDER envelope 80 x 40]", "base", "power", "pcbPh", PH,
     ["+", [bx(*pcb), bx(pcb[0] + 30, pcb[1] + 10, pcb[5] - 0.1, pcb[0] + 34, pcb[1] + 14, pcb[5] + 0.9),
            bx(pcb[0] + 40, pcb[1] + 10, pcb[5] - 0.1, pcb[0] + 44, pcb[1] + 14, pcb[5] + 0.9),
            bx(pcb[0] + 48, pcb[1] + 6, pcb[5] - 0.1, pcb[0] + 56, pcb[1] + 14, pcb[5] + 5.0)]])
part("usbcIn", "POWER | USB-C PD charge input receptacle (GCT USB4105-class) at the left wall", "base", "power", "metal", SEL,
     ["+", [bx(-IX - 0.6, 108.9, pcb[5] - 0.2, -IX + 7.4, 117.1, pcb[5] + 3.2)]])
part("solarIn", "POWER | solar input 2-pin keyed connector + ideal diode / TVS (P108 -> VAC2) [PLACEHOLDER]", "base", "power",
     "connector", PH, ["+", [bx(pcb[0] + 8, pcb[4] - 6, pcb[5] - 0.1, pcb[0] + 20, pcb[4] - 0.5, pcb[5] + 6)]])
part("reg12", "POWER | Pololu S18V20F12 12 V buck-boost (Beck rail) 43 x 21 x 10 MFR", "base", "power", "pcbMod", SEL,
     ["+", [bx(pcb[3] - 2 - 43, pcb[1] + 17, pcb[5] - 0.1, pcb[3] - 2, pcb[1] + 38, pcb[5] + 8.5)]])
cp = B["ENV_COMPUTE_POWER"]
part("reg5", "POWER | Pololu D36V50F5 5 V 5.5 A buck (Pi rail) 25.4 x 25.4 x 9.5 MFR", "base", "power", "pcbMod", SEL,
     ["+", [bx(cp[2] + 10, cp[4] + 2, cp[6] + 1.5, cp[2] + 35.4, cp[4] + 27.4, cp[6] + 11)]])
bk = B["ENV_DISPLAY_CTRL"]
bkp = (bk[2] + 2, bk[4] + 2, bk[6] + 1.5)
part("beck", "DISPLAY | Beck BTC-mini-eDP HDMI->eDP controller 80 x 70 x 9.8 MFR (HBR support + price: OWNER e-mail)", "base",
     "power", "pcbCtrl", SEL, ["+", [bx(bkp[0], bkp[1], bkp[2], bkp[0] + 80, bkp[1] + 70, bkp[2] + 1.6),
                                     bx(bkp[0] + 80 - 0.5, bkp[1] + 20, bkp[2] + 1.5, bkp[0] + 80 + 4, bkp[1] + 35, bkp[2] + 7),   # HDMI in
                                     bx(bkp[0] + 33, bkp[1] + 70 - 4, bkp[2] + 1.5, bkp[0] + 47, bkp[1] + 70 + 0.5, bkp[2] + 3.5),  # eDP out
                                     bx(bkp[0] - 0.5, bkp[1] + 10, bkp[2] + 1.5, bkp[0] + 6, bkp[1] + 18, bkp[2] + 8),            # 12 V in
                                     bx(bkp[0] + 25, bkp[1] + 25, bkp[2] + 1.5, bkp[0] + 40, bkp[1] + 40, bkp[2] + 2.8)]])
gn = B["ENV_GNSS"]
part("gnss", "GNSS | SparkFun GNSS Flex pHAT DAN-F10N (GPS-29491): pHAT 65 x 30 + module (layout EST)", "base", "power", "pcbGnss",
     SEL, ["+", [bx(gn[2] + 2.5, gn[4] + 1.5, gn[6] + 4, gn[2] + 67.5, gn[4] + 31.5, gn[6] + 5.6),
                 bx(gn[2] + 18, gn[4] + 1.5, gn[6] + 5.5, gn[2] + 52, gn[4] + 31.5, gn[6] + 7.2)]])
part("gnssPatch", "GNSS | DAN-F10N L1/L5 patch 20 x 20 x 8 (MFR) under the non-metallic rear-deck sky window", "base", "power",
     "patch", SEL, ["+", [bx(gn[2] + 25, gn[4] + 11, gn[6] + 7.1, gn[2] + 45, gn[4] + 31, gn[6] + 15.2)]])
part("gnssStand", "GNSS | M2.5 standoffs (supplied)", "base", "power", "metal", SEL,
     ["+", [cyl((x, y, IZ0 - 0.1), (x, y, gn[6] + 4.05), 2.0) for x in (gn[2] + 5.5, gn[2] + 64.5) for y in (gn[4] + 4.5, gn[4] + 28.5)]])

# =====================================================================================================================
# COOLING
# =====================================================================================================================
fx0, fx1, fy0, fy1, fz0, fz1 = FAN[2], FAN[3], FAN[4], FAN[5], FAN[6], FAN[7]
fyc, fzc = (fy0 + fy1) / 2, (fz0 + fz1) / 2
part("fan", "COOLING | Sunon MF30100V1-1000U-A99 30 x 30 x 10, 5 V 0.6 W, 5.5 CFM MFR - exhaust through the right wall",
     "base", "fan", "fan", SEL, ["+", [bx(fx0, fy0, fz0, fx1, fy1, fz1)]], ["-", [cyl((fx0 - 1, fyc, fzc), (fx1 + 1, fyc, fzc), 14)]],
     ["+", [cyl((fx0 + 1, fyc, fzc), (fx1 - 1, fyc, fzc), 6.5),
            bx(fx0 + 3, fyc - 1, fzc - 14.3, fx0 + 7, fyc + 1, fzc + 14.3), bx(fx0 + 3, fyc - 14.3, fzc - 1, fx0 + 7, fyc + 14.3, fzc + 1)]])

# =====================================================================================================================
# DISPLAY HINGES (Southco E6-10-216-50) - base leaves recessed in the rear-face pockets; lid leaves in the lid
# =====================================================================================================================
for k, sx in enumerate((-1, 1)):
    c = sx * SOUTHCO_X
    part(f"southcoB{k}", f"DISPLAY HINGE | Southco E6-10-216-50 1.8 N.m, base leaf + barrel {'L' if sx < 0 else 'R'} "
         "(mounting CONCEPTUAL; axis D-006 provisional; torque variant: weigh lid first)", "base", "", "southco", SEL,
         ["+", [bx(c - SOUTHCO_L / 2, D - 3.0, 22, c + SOUTHCO_L / 2, D, H - 1.8),
                cyl((c - SOUTHCO_L / 2, HAY, HAZ), (c + SOUTHCO_L / 2, HAY, HAZ), SOUTHCO_R)]])
    part(f"southcoS{k}", f"FASTENERS | M4 countersunk, Southco base leaf {'L' if sx < 0 else 'R'} (from behind, lid open)", "base", "",
         "fastener", SEL, ["+", [cyl((c + dx, D - 0.6, zz), (c + dx, D + 0.05, zz), 3.6) for dx in (-14, 14) for zz in (27,)]])
    part(f"southcoL{k}", f"DISPLAY HINGE | Southco E6-10-216-50 lid leaf {'L' if sx < 0 else 'R'}", "lid", "", "southco", SEL,
         ["+", [bx(c - SOUTHCO_L / 2, D - 3.0, ZF + 3, c + SOUTHCO_L / 2, D, ZF + 17)]])
part("knuckle", "CABLES | display-hinge cable knuckle 20 mm (eDP + solar lead, 60 mm axial twist zone) [CONCEPT]", "base", "",
     "knuckle", ENG, ["+", [cyl((-12, HAY, HAZ), (12, HAY, HAZ), 6.0)]], ["-", [cyl((-13, HAY, HAZ), (13, HAY, HAZ), 4.0)]])
part("foil", "LID | low-e foil on the lid back in the 6 mm vented air gap (D-010)", "lid", "", "foil", ENG,
     ["+", [bx(-135, 22, ZF + CORE, 135, 231.5, ZF + CORE + 0.15)]])            # ends before the leaf rear wall (y 232)
part("edpConn", "DISPLAY | eDP connector IPEX 20455-030E-12 (MFR); position on the panel back from drawing p.24 [PLACEHOLDER position]",
     "lid", "", "connector", PH, ["+", [bx(-7, DSP_Y1 - 10, DSP_Z1 - 0.05, 7, DSP_Y1 - 5, DSP_Z1 + 1.6)]])
part("display", "DISPLAY | AUO G101UAN01.0 10.1 in 1920x1200 eDP 2-lane, 228.22 x 148.32 x 5.35, 140 g (MFR spec rev 1.5)",
     "lid", "", "display", SEL, ["+", [bx(-DSP["w"] / 2, DSP_Y0, DSP_Z0, DSP["w"] / 2, DSP_Y1, DSP_Z1)]])
part("displayAA", "DISPLAY | active area 216.81 x 135.50 (MFR)", "lid", "", "screen", SEL,
     ["+", [bx(-DSP["aw"] / 2, DSP_YC - DSP["ah"] / 2, DSP_Z0 - 0.02, DSP["aw"] / 2, DSP_YC + DSP["ah"] / 2, DSP_Z0 + 0.3)]])
# lid-core cuts applied to the SB-261 lid core: display window (1 mm lip), display pocket, Southco lid-leaf pockets
LIDCUTS = [bx(-DSP["aw"] / 2 - 1, DSP_YC - DSP["ah"] / 2 - 1, ZF - 1, DSP["aw"] / 2 + 1, DSP_YC + DSP["ah"] / 2 + 1, DSP_Z0 + 0.05),
           bx(-DSP["w"] / 2 - 0.3, DSP_Y0 - 0.3, DSP_Z0, DSP["w"] / 2 + 0.3, DSP_Y1 + 0.3, DSP_Z1 + 0.3),
           bx(-10, DSP_Y1 - 12, DSP_Z1, 10, D + 1, DSP_Z1 + 3.4),                     # eDP channel (cable top at +3.1)
           bx(-10, D - 12, ZF - 1, 10, D + 1, DSP_Z1 + 3.4)]                          # eDP / solar exit notch to the knuckle
for sx in (-1, 1):
    c = sx * SOUTHCO_X
    LIDCUTS.append(bx(c - SOUTHCO_L / 2 - 0.3, D - 3.3, ZF + 2.7, c + SOUTHCO_L / 2 + 0.3, D + 1, ZF + 17.3))
LIDCUTS.append(cyl((-12.5, HAY, HAZ), (12.5, HAY, HAZ), 6.5))
for sx in (-1, 1):
    LIDCUTS.append(cyl((sx * SOUTHCO_X - SOUTHCO_L / 2 - 0.5, HAY, HAZ), (sx * SOUTHCO_X + SOUTHCO_L / 2 + 0.5, HAY, HAZ), SOUTHCO_R + 0.5))
LIDCUTS.append(dia("Z", ZF - 1, ZF + CORE + 1, -W2, 0, CH_F))                        # lid corners follow the base outline
LIDCUTS.append(dia("Z", ZF - 1, ZF + CORE + 1, W2, 0, CH_F))
LIDCUTS.append(dia("Z", ZF - 1, ZF + CORE + 1, -W2, D, CH_R))
LIDCUTS.append(dia("Z", ZF - 1, ZF + CORE + 1, W2, D, CH_R))

# =====================================================================================================================
# B1 STAY (both states; the feature builds the one that matches the pose)
# =====================================================================================================================
SX = W2 - P["STAY_PIVOT_INSET_X"]
SY = D - P["STAY_PIVOT_INSET_Y"]
SR = P["SOLAR_STAY_REACH"]
for st, grp in (("stowed", "stayS"), ("deployed", "stayD")):
    arms = []
    for sg in (-1, 1):
        if st == "deployed":
            arms.append(bx(sg * SX - 8, SY - 12, -3.5, sg * SX + 8, SY + SR, -0.5))
        else:
            arms.append(bx(sg * SX - 8, SY - SR - 12, -3.5, sg * SX + 8, SY + 12 - 12, -0.5))
    part(f"stay_{st}", f"B1 STAY | 2 x stainless 1.4301 3 x 16, reach {SR:g} ({st}) - MANDATORY for leaf deployment", grp, "",
         "stay", ENG, ["+", arms])
    part(f"stayPiv_{st}", "B1 STAY | M4 shoulder-screw pivots in the rear corner blocks", grp, "", "fastener", SEL,
         ["+", [cyl((sg * SX, SY, -4), (sg * SX, SY, 6), 2.0) for sg in (-1, 1)]])
    if st == "deployed":
        part("stayPads", "B1 STAY | foot pads", grp, "", "rubber", ENG,
             ["+", [cyl((sg * SX, SY + SR - 8, -4), (sg * SX, SY + SR - 8, -3.4), 8) for sg in (-1, 1)]])

# =====================================================================================================================
# CLEARANCE / KEEP-OUT BODIES (group keep) and CONFLICT ghosts
# =====================================================================================================================
for nm in ("KEEPOUT_PI_USB_PLUGS", "KEEPOUT_PI_REAR_PLUGS", "KEEPOUT_GNSS_SKY", "KEEPOUT_FAN_INLET",
           "C_DISPLAY_RISER", "C_REAR_TRUNK", "C_PI_TO_UNDERKB", "C_BATTERY"):
    part("k_" + nm, f"CLEARANCE | {nm} (v1_integration keep-out / corridor)", "keep", "", "keep" if nm.startswith("K") else "corridor",
         ENG, ["+", [ob(nm)]])
part("k_plugUsbC", "CLEARANCE | external USB-C charge plug + cable bend (45 mm)", "keep", "", "keep", ENG,
     ["+", [bx(-W2 - 45, 107, USBC_ZC - 4, -W2, 119, USBC_ZC + 4)]])
part("k_plugUsbA", "CLEARANCE | external USB-A plugs (front right, 45 mm)", "keep", "", "keep", ENG,
     ["+", [bx(62, -45, 8.5, 97.5, 0, 18)]])
part("k_exhaust", "CLEARANCE | fan exhaust plume (keep free, 40 mm)", "keep", "", "air", ENG,
     ["+", [bx(W2, fy0, fz0, W2 + 40, fy1, fz1)]])
part("k_kb21", "CONFLICT | keyboard 21 mm thick per Perixx product page (manual: 16) - 5 mm proud of the deck or 5 mm into the under-keyboard zone",
     "keep", "", "conflict", CF, ["+", [bx(-KBX, KB0, kbz1 - 21, KBX, KB1, kbz1)]])
part("k_table", "REFERENCE | table plane z = -4 (feet)", "table", "", "table", ENG, ["+", [bx(-450, -200, -6, 450, 560, -4)]])

# airflow arrows (group air): shaft + head
AIR = [((0, D + 30, 12), (0, D - 10, 12)), ((40, 190, 12), (90, 120, 14)), ((110, 100, 30), (110, 45, 30)),
       ((140, 17, 18), (W2 + 30, 17, 18)), ((-30, D + 30, 12), (-30, D - 10, 12))]
for i, (a, b2) in enumerate(AIR):
    u = [b2[j] - a[j] for j in range(3)]
    ln = math.sqrt(sum(v * v for v in u))
    h0 = [b2[j] - u[j] / ln * 8 for j in range(3)]
    part(f"air{i}", "COOLING | airflow (rear/underside intake -> under keyboard -> Pi bay -> right-wall exhaust)", "air", "", "air",
         ENG, ["+", [cyl(a, h0, 1.6), cyl(h0, b2, 4.0)]])

# =====================================================================================================================
# CABLE ROUTES [name, diameter, bend R, colorKey, status, [[frame, x, y, z] ...]] - route concepts, not cut lengths
# =====================================================================================================================
def rb(*pts):
    return [["base", *p] for p in pts]


pb_conn = (-125, pk[4] + 2, 13)
ROUTES = [
    ["CABLE | battery lead 2 x 16 AWG + NTC (pack -> power board BAT)", 4.5, 10, "cablePower", ENG,
     rb((-139, pk[4] + 2, 13), (-139, 96, 10), (-139, pcb[1] + 6, pcb[5] + 2))],
    ["CABLE | SYS bus 2 x 18 AWG (power board -> 5 V buck)", 3.5, 8, "cablePower", ENG,
     # rear trunk (C_REAR_TRUNK, z 16.3-19.8) side by side in y: SYS 190.5 / control 196 / solar 200.5; past the Beck envelope
     # (x 42) the SYS bus drops to z 10.5 to pass under the keyboard lead and the GNSS / control lanes (x 51-57.5)
     rb((pcb[3], pcb[1] + 20, pcb[5] + 2), (-55, pcb[1] + 20, 18), (-55, 190.5, 18), (42, 190.5, 18), (50, 190.5, 10.5),
        (100, 190.5, 10.5), (120, 150, 12), (122, 147, 12))],
    ["CABLE | 5.1 V -> Pi USB-C power-only lead 2 x 18 AWG", 3.5, 15, "cablePower", ENG,
     rb((122, cp[4] + 2, 12), (cpc[0], cpc[1] + 18, 12), (cpc[0], cpc[1] + 11.5, pz1 + 2.5))],
    ["CABLE | 12 V -> Beck 2 x 22 AWG", 2.5, 6, "cablePower", ENG,
     rb((pcb[3] - 20, pcb[1] + 30, pcb[5] + 9), (-55, 150, 14), (bkp[0] - 1, bkp[1] + 14, bkp[2] + 5))],
    ["CABLE | HDMI0 micro-HDMI -> HDMI FPC (Pi -> Beck)", 4.0, 10, "cableSig", SEL,
     rb((hd0[0], hd0[1] + 12, pz1 + 2), (hd0[0], 112, 10), (bkp[0] + 90, 112, 10), (bkp[0] + 88, bkp[1] + 27, bkp[2] + 4.5),
        (bkp[0] + 84, bkp[1] + 27, bkp[2] + 4.5))],
    ["CABLE | eDP 30-pin micro-coax (Beck -> knuckle twist zone -> panel)", 3.0, 5, "cableEdp", PH,
     rb((bkp[0] + 40, bkp[1] + 70.5, bkp[2] + 2.5), (0, 230, 10), (0, D - 6, 30), (0, HAY - 2, HAZ - 3)) +
     [["lid", 0, D - 4, DSP_Z1 + 1.6], ["lid", 0, DSP_Y1 + 4, DSP_Z1 + 1.6], ["lid", 0, DSP_Y1 - 7.5, DSP_Z1 + 1.6]]],
    ["CABLE | solar lead 2 x 0.5 mm2 d4: SB-261 lid run -> knuckle (axial twist) -> power board VAC2 (R12 concept)", 4.0, 12,
     "cableSolar", ENG,
     [["lid", 141, 193.5, 53], ["lid", 141, 244, 53], ["lid", 6, 244, 53], ["lid", 6, D - 3, ZF + 3], ["base", 6, HAY - 2, HAZ - 3],
      ["base", 6, D - 8, 30], ["base", 6, 236, 18], ["base", 6, 200.5, 18], ["base", -100, 200.5, 18], ["base", -100, pcb[4] + 2, 12],
      ["base", pcb[0] + 14, pcb[4] - 3, pcb[5] + 3]]],
    ["CABLE | keyboard USB-C -> A short lead -> Pi USB2 (upper)", 4.0, 15, "cableUsb", ENG,
     rb((KBC_X, KB1 + 9, 31), (KBC_X, KB1 + 9, 18), (54, KB1 + 2, 18), (54, 99, 18), (28, 99, 18), (28, u2[1], pz1 + 11.6),
        (px0 - 24, u2[1], pz1 + 11.6))],
    ["CABLE | trackpad USB lead -> Pi USB2 (lower)", 3.5, 15, "cableUsb", SEL,
     rb((0, TP1, 31), (0, 95, 31), (0, 95, 11), (24, 95, 11), (24, u2[1], pz1 + 4), (px0 - 24, u2[1], pz1 + 4))],
    ["CABLE | USB 3.0 extension 1 (Pi USB3 -> front-right socket)", 5.0, 20, "cableUsb", SEL,
     rb((px0 - 24, u1[1], pz1 + 4), (20, u1[1], pz1 + 4), (20, 27, 11), (71, 27, 11), (71, 22.5, 13))],
    ["CABLE | USB 3.0 extension 2 (Pi USB3 -> front-right socket)", 5.0, 20, "cableUsb", SEL,
     rb((px0 - 24, u1[1], pz1 + 11.6), (14, u1[1], pz1 + 11.6), (14, 31, 18), (89, 31, 18), (89, 22.5, 13))],
    # GNSS + control harness: over the Pi USB plugs (top z 21.7) at z 31.5 / 35, down the bulkhead-Pi gap at y 94 (plugs end at
    # y 90, keyboard tray starts at y 97), then under the tray at z 14 (below the keyboard lead, above the HDMI lead).
    # Kernel QA 2026-10-08: the previous concept crossed the USB plugs.
    ["CABLE | GNSS 6-wire UART/PPS (Pi GPIO -> pHAT)", 3.0, 8, "cableSig", ENG,
     rb((g0[0] + 15, g0[1] + 6, hatz + 6), (g0[0] + 15, g0[1] + 6, 35), (56, g0[1] + 6, 35), (56, 94, 35), (56, 94, 14), (56, 207, 14),
        (-40, 207, 14), (-40, gn[4] + 3, gn[6] + 7))],
    ["CABLE | control harness: charger I2C + J2 button + fan PWM (power board -> Pi GPIO)", 3.0, 8, "cableSig", ENG,
     rb((pcb[0] + 50, pcb[4] - 1, pcb[5] + 2), (-94, 144, 12), (-94, 196, 18), (36, 196, 18), (52.5, 196, 14), (52.5, 94, 14), (52.5, 94, 31.5),
        (52.5, g0[1] + 1.5, 31.5), (g0[0] + 6.5, g0[1] + 1.5, 31.5))],
    # fan lead: right-hand side of the Pi stack (x 141.5, clear of the rear plugs, the corner boss and the HAT), over the HAT at z 32
    ["CABLE | enclosure fan 2 x 26 AWG (5.1 V via FET)", 2.0, 8, "cableSig", ENG,
     # z 15: the R8 riser bend then stays under the keyboard tray (z 21 from y 97); kernel QA 2026-10-08 (z 16 grazed it)
     rb((cp[2] + 12, cp[4] + 2, 12), (cp[2] + 12, 112, 15), (141.5, 112, 15), (141.5, 95.5, 15), (141.5, 95.5, 32), (141.5, fy1 - 0.5, 32))],
    ["CABLE | power button + charge LED (left wall -> power board)", 2.0, 8, "cableSig", ENG,
     rb((-IX + 25, B["ENV_BUTTON"][4] + 7, 12.5), (-110, B["ENV_BUTTON"][4] + 7, 12.5), (-110, pcb[4] - 2, pcb[5] + 2))],
]
# USB-A panel sockets (front right) and the Pi-side bulkhead are bodies, not cables
part("usbSockets", "IO | 2 x USB-A 3.0 panel-mount sockets (front right) [PLACEHOLDER generic]", "base", "power", "connector", PH,
     ["+", [bx(64.5, IY0, 9, 77.0, IY0 + 20, 17.5), bx(82.5, IY0, 9, 95.0, IY0 + 20, 17.5)]])
part("button", "IO | power button 12 mm sealed momentary (Pi J2 + charger QON) [PLACEHOLDER generic]", "base", "power", "connector",
     PH, ["+", [cyl((-IX - 1.2, B["ENV_BUTTON"][4] + 7, 12.5), (-IX + 24, B["ENV_BUTTON"][4] + 7, 12.5), 5.8)]])

EXPLODE = {"panel": [0, 0, -70], "door": [0, 0, -60], "battery": [0, 0, -135], "pi": [0, 0, -110], "power": [0, 0, -95],
           "fan": [0, 0, -95], "kb": [0, 0, 80], "tp": [0, 0, 55]}

CONST = {"W": W, "D": D, "H": H, "ZF": ZF, "CORE": CORE, "HAY": HAY, "HAZ": HAZ, "LDD": D, "LW2": W2,
         "LIDMAX": P["LID_ANGLE_MAX"], "LEAFMAX": P["SOLAR_LEAF_ANGLE_MAX"], "LIDNOM": P["LID_ANGLE_NOMINAL"],
         "SOLAR_ROUTE": next(i for i, r in enumerate(ROUTES) if r[0].startswith("CABLE | solar lead"))}

CONFLICTS = [
    "Display outline: nomad.yaml 229.9 x 150.5 (3P) vs AUO spec rev 1.5 228.22 x 148.32 (MFR) -> model uses MFR; YAML update "
    "pending owner approval (no clearance changes: the MFR panel is smaller).",
    "Leaf depth: nomad.yaml SOLAR_LEAF_DEPTH 239 (panel + 16) vs the kernel-validated SB-261 leaf (y 9..235 = 226) -> model uses "
    "the validated SB-261 geometry; 239 stays a conservative load input.",
    "Panel width: SB-261 leaf rebate holds 273 (+-136.5) but P108 is 274 (MFR) and the ASA/FR4 CTE needs >= 0.6 mm per side -> "
    "leaf side walls must move out ~1.1 mm per side (leaf 289 -> ~291; fits the 306 lid). Shown as-is (validated geometry).",
    "Keyboard thickness: MFR manual 16 mm / 332 g vs product page 21 mm / 361 g -> 16 modelled, 21 shown as a CONFLICT ghost.",
    "Southco E6 on the rear faces puts its real axis ~5 mm behind the base face; the model keeps the D-006 working axis "
    "(rear top edge). Leaves are drawn recessed in rear-face pockets (CONCEPT).",
]


# =====================================================================================================================
# emit / report
# =====================================================================================================================
def fsv(v):
    if isinstance(v, str):
        return '"' + v.replace('"', "'") + '"'
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        s = f"{v:.3f}".rstrip("0").rstrip(".")
        return "0" if s in ("-0", "") else s
    if isinstance(v, dict):
        return "{ " + ", ".join(f'"{k}" : {fsv(x)}' for k, x in v.items()) + " }"
    return "[" + ", ".join(fsv(x) for x in v) + "]"


def block():
    out = [BEGIN, "// Generated by CAD/tools/v1_visual_emit.py --write. DO NOT EDIT. mm, closed-lid world frame.",
           "// Sources: CAD/tools/v1_integration.py (nomad.yaml + v1_hardware.py), AUO G101UAN01.0 spec rev 1.5, RPi drawings.",
           "const V1 = " + fsv(CONST) + ";", "const V1_EXPLODE = " + fsv(EXPLODE) + ";",
           "const V1_LIDCUTS = ["] + ["    " + fsv(c) + ("," if i < len(LIDCUTS) - 1 else "") for i, c in enumerate(LIDCUTS)] + [
           "];", "const V1_PARTS = ["]
    for i, p in enumerate(PARTS):                       # one stage per line (short lines, readable compiler errors)
        out.append("    [" + ", ".join(fsv(x) for x in p[:6]) + ", [")
        for k, st in enumerate(p[6]):
            out.append("        [" + fsv(st[0]) + ", [")
            for m, prim in enumerate(st[1]):
                out.append("            " + fsv(prim) + ("," if m < len(st[1]) - 1 else ""))
            out.append("        ]]" + ("," if k < len(p[6]) - 1 else ""))
        out.append("    ]]" + ("," if i < len(PARTS) - 1 else ""))
    out += ["];", "const V1_ROUTES = ["]
    for i, r in enumerate(ROUTES):
        out.append("    [" + ", ".join(fsv(x) for x in r[:5]) + ", [")
        for m, wp in enumerate(r[5]):
            out.append("        " + fsv(wp) + ("," if m < len(r[5]) - 1 else ""))
        out.append("    ]]" + ("," if i < len(ROUTES) - 1 else ""))
    out += ["];", END]
    return "\n".join(out)


def route_hits():
    """Sample each cable route (base-frame segments) against solid envelopes it does not serve (route-concept check)."""
    solid = [b for b in VI.BOXES if b[1] in ("E", "S") and b[0] not in ("SERVICE_PANEL_MAIN", "SERVICE_PANEL_FRONT", "BATTERY_DOOR")]
    hits = []
    for r in ROUTES:
        pts = [p[1:] for p in r[5] if p[0] == "base"]
        bad = set()
        served = {bb[0] for bb in solid for e in (pts[0], pts[-1])
                  if bb[2] <= e[0] <= bb[3] and bb[4] <= e[1] <= bb[5] and bb[6] <= e[2] <= bb[7]}
        for a, b in zip(pts, pts[1:]):
            for t in [i / 20 for i in range(2, 19)]:
                q = [a[j] + (b[j] - a[j]) * t for j in range(3)]
                for bb in solid:
                    if bb[0] not in served and bb[2] + 1 < q[0] < bb[3] - 1 and bb[4] + 1 < q[1] < bb[5] - 1 and bb[6] + 1 < q[2] < bb[7] - 1:
                        bad.add(bb[0])
        hits.append((r[0], sorted(bad)))
    return hits


NL = chr(10)
SB_BEGIN, SB_END = "// BEGIN SB261 LIBRARY", "// END SB261 LIBRARY"
SB_SRC = ROOT / "prototypes" / "B1_SB261" / "src" / "fs" / "b1_common.fs"
# The ONLY edits to the kernel-validated SB-261 library: V1 lid width / depth, leaf depth kept at the validated 235,
# the old 235 x 150 display envelope removed (the V1 display is a generated part), unused pair-check helpers dropped.
SB_EDITS = [("const W2 = 150.5;", f"const W2 = {W2:g}; // V1 lid half-width (was 150.5)"),
            ("const DD = 235.0;", f"const DD = {D:g}; // V1 lid depth (was 235)" + NL + "const LDY = 235.0; // leaf rear edge: validated SB-261 leaf"),
            ('bx(context, id + "swr", 136.5, LF, ZB, 144.5, DD, ZT);', 'bx(context, id + "swr", 136.5, LF, ZB, 144.5, LDY, ZT);'),
            ('bx(context, id + "swl", -144.5, LF, ZB, -136.5, DD, ZT);', 'bx(context, id + "swl", -144.5, LF, ZB, -136.5, LDY, ZT);'),
            ('bx(context, id + "rw", -144.5, 232, ZB, 144.5, DD, ZT);', 'bx(context, id + "rw", -144.5, 232, ZB, 144.5, LDY, ZT);'),
            ('bx(context, idL + "d", -117.5, 42.5, 43, 117.5, 192.5, 48);', "// (old 235 x 150 display envelope removed: V1 display is a generated part)"),
            ('"Ld" : bq(idL + "d"), ', "")]


def sb_block():
    src = SB_SRC.read_text(encoding="utf-8").replace("\r\n", NL)
    for a, b in SB_EDITS:
        assert src.count(a) == 1, a
        src = src.replace(a, b)
    src = src[:src.index("// Cross-group pair list")].rstrip() + NL
    src = src.replace(chr(0xD8), "D")                                   # ASCII only (Onshape editor paste safety)
    return (SB_BEGIN + NL + "// Spliced by CAD/tools/v1_visual_emit.py from prototypes/B1_SB261/src/fs/b1_common.fs "
            "(kernel-validated). DO NOT EDIT HERE." + NL + src + SB_END)


def splice(text, b0, b1, content):
    i, j = text.index(b0), text.index(b1) + len(b1)
    return text[:i] + content + text[j:]


def main(argv):
    text = FS_PATH.read_text(encoding="utf-8") if FS_PATH.exists() else ""
    updated = splice(splice(text, BEGIN, END, block()), SB_BEGIN, SB_END, sb_block())
    if "--write" in argv:
        FS_PATH.write_text(updated, encoding="utf-8", newline="\n")
        print(f"wrote {FS_PATH.relative_to(ROOT)}")
    if "--check" in argv:
        if updated != text:
            print("NOMAD_V1_Visual.fs: GENERATED V1 VISUAL DATA block is OUT OF DATE")
            return 1
        print("NOMAD_V1_Visual.fs: GENERATED V1 VISUAL DATA block is up to date")
    st = {}
    for p in PARTS:
        st[p[5]] = st.get(p[5], 0) + 1
    print(f"parts {len(PARTS)} ({', '.join(f'{k} {v}' for k, v in st.items())}), cable routes {len(ROUTES)}, lid cuts {len(LIDCUTS)}")
    print("route-concept intersections with solid envelopes (base-frame segments, 1 mm inset):")
    for nm, bad in route_hits():
        print(f"  {'OK ' if not bad else 'HIT'} {nm}" + (f" -> {', '.join(bad)}" if bad else ""))
    print("conflicts shown in the model:")
    for c in CONFLICTS:
        print("  - " + c)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
