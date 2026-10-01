"""Round E, stage E2: NOMAD digital lid layout spec + local pose/clearance checks + FeatureScript generator.

Lid = Round D.1 class A (PROVISIONAL - PENDING P0.2 PHYSICAL VALIDATION): lip 1 | display 5 | gap 1 | rail layer 13 |
gap 1 | cassette 8 | gap 2 | sandwich shell 6.6 = 37.6. Solar = Round B.1 V1 + fixes (mirrored, each cassette in its own
half of the lid, staggered rails, 8 mm corridor). Hinge = D-006 rear-edge axis, representative Ø8 knuckle barrel with
leaf/block geometry in the Round C hinge reserves. Every coordinate is an expression over nomad.yaml parameters
(WORLD frame: base bottom-front centreline origin, +X right, +Y rear, +Z up; lid CLOSED, cassettes STOWED).

  py CAD/tools/e_lid_layout.py            spec checks + pose/clearance matrix
  py CAD/tools/e_lid_layout.py --write    also regenerate the GENERATED E LID LAYOUT block in NOMAD_E_Prototype.fs and
                                          the expected block in NOMAD_E_Prototype.e2.test.fs (kernel cross-check)
  py CAD/tools/e_lid_layout.py --check    fail if either generated block is out of date

Evidence level: modeled (exact X-prism geometry: every motion is a rotation about an X-parallel axis or a
translation along X, so all parts stay X-extruded Y-Z polygons; same machinery as B.1 / C.2).
"""

import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ast  # noqa: E402

import base_v01_layout as bl  # noqa: E402
import hinge_feasibility_2d as hm  # noqa: E402
import region2d as rg  # noqa: E402
import solar_skeleton_model as sk  # noqa: E402
import solar_v1_feasibility as sv  # noqa: E402
from yaml_to_featurescript import _eval_formula  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
FS_PATH = ROOT / "CAD" / "featurescript" / "NOMAD_E_Prototype.fs"
HARNESS_PATH = ROOT / "CAD" / "featurescript" / "NOMAD_E_Prototype.e2.test.fs"
BEGIN, END = "// BEGIN GENERATED E LID LAYOUT", "// END GENERATED E LID LAYOUT"
HBEGIN, HEND = "// BEGIN GENERATED E LID EXPECTED", "// END GENERATED E LID EXPECTED"
P = bl.PARAMS
MIN_GAP = P["MIN_GAP"]
EPS = 1e-6
NEAR = 15.0

# ------------------------------------------------------------------ derived values (emitted as LE_<name>)
DERIVED = [
    # lid frame and layer stack (world Z, closed lid)
    ("ZF", "BODY_HEIGHT + LID_CLOSED_GAP"),                    # lid display-side face
    ("W2", "BODY_WIDTH / 2"),
    ("IX", "W2 - WALL_THICKNESS"),
    ("IY0", "WALL_THICKNESS"),
    ("IY1", "BODY_DEPTH - WALL_THICKNESS"),
    ("ZFR", "ZF + WALL_THICKNESS"),                            # face-ring top
    ("ZD0", "ZF + DISPLAY_BEZEL_LIP"),
    ("ZD1", "ZD0 + DISPLAY_THICKNESS"),
    ("ZR0", "ZD1 + MIN_GAP"),                                  # solar rail layer
    ("ZR1", "ZR0 + SOLAR_RAIL_LAYER_HEIGHT"),
    ("ZC0", "ZR1 + MIN_GAP"),                                  # stowed cassettes
    ("ZC1", "ZC0 + SOLAR_CASSETTE_THICKNESS"),
    ("ZS0", "ZC1 + LID_BACK_GAP"),                             # rear-shell seat = frame top
    ("ZS1", "ZS0 + LID_REAR_SHELL_DEPTH"),
    # display
    ("DX", "DISPLAY_WIDTH / 2"),
    ("DYC", "BODY_DEPTH / 2 - DISPLAY_VERTICAL_OFFSET"),
    ("DY0", "DYC - DISPLAY_HEIGHT / 2"),
    ("DY1", "DYC + DISPLAY_HEIGHT / 2"),
    ("AX", "DISPLAY_ACTIVE_WIDTH / 2"),
    ("AY0", "DYC - DISPLAY_ACTIVE_HEIGHT / 2"),
    ("AY1", "DYC + DISPLAY_ACTIVE_HEIGHT / 2"),
    # solar, B.1 V1 + fixes (right side; the left side mirrors X and uses the L rail / hub values)
    ("XI", "MIN_GAP / 2"),                                     # stowed cassette inboard edge
    ("CY0", "(BODY_DEPTH - SOLAR_CASSETTE_HEIGHT) / 2"),
    ("CY1", "CY0 + SOLAR_CASSETTE_HEIGHT"),
    ("RCR", "BODY_DEPTH / 2 + SOLAR_RAIL_WIDTH / 2 + SOLAR_CABLE_CORRIDOR / 2"),
    ("RCL", "BODY_DEPTH / 2 - SOLAR_RAIL_WIDTH / 2 - SOLAR_CABLE_CORRIDOR / 2"),
    ("HYR", "CY0 + SOLAR_HUB_AXIS_OFFSET_Y"),
    ("HYL", "CY1 - SOLAR_HUB_AXIS_OFFSET_Y"),
    ("HZ", "ZC0 + SOLAR_HUB_AXIS_OFFSET_Z"),
    ("KX1", "XI - SOLAR_HUB_LINK_LENGTH"),                     # stowed carriage outboard end
    ("KX0", "KX1 - SOLAR_RAIL_ENGAGEMENT"),                    # stowed carriage inboard end = rail inboard end
    ("RX1", "XI + SOLAR_SLIDE_TRAVEL - SOLAR_HUB_LINK_LENGTH"),  # rail outboard end
    ("RW2", "SOLAR_RAIL_WIDTH / 2"),
    ("SW2", "SOLAR_RAIL_SLOT_WIDTH / 2"),
    ("CW2", "SOLAR_CARRIAGE_WIDTH / 2"),
    ("CH2", "SOLAR_CARRIAGE_HEIGHT / 2"),
    ("BW2", "SOLAR_BRACKET_WIDTH / 2"),
    ("BZ0", "HZ - SOLAR_HUB_PIN_DIAMETER / 2 - SOLAR_BRACKET_WALL"),   # hub bracket bottom (MIN_GAP above the rail floor, F3)
    ("CRO", "SOLAR_HUB_PIN_DIAMETER / 2 + MIN_GAP + SOLAR_CABLE_DIAMETER / 2"),  # cable centre from the tilt axis
    ("CD2", "SOLAR_CABLE_DIAMETER / 2"),
    ("LPB", "2 * SOLAR_CABLE_BEND_RADIUS + SOLAR_CABLE_DIAMETER"),  # service-loop band
    ("LPX0", "KX0 - 2 * SOLAR_CABLE_BEND_RADIUS"),
    ("LPX1", "KX0 + SOLAR_SLIDE_TRAVEL + 2 * SOLAR_CABLE_BEND_RADIUS"),
    ("LRY0", "RCR + RW2 + MIN_GAP"),
    ("LRY1", "LRY0 + LPB"),
    ("LLY1", "RCL - RW2 - MIN_GAP"),
    ("LLY0", "LLY1 - LPB"),
    ("CORX", "SOLAR_CABLE_DIAMETER / 2 + MIN_GAP - KX0"),     # corridor half-length (both rails present)
    ("NR0", "RCR - BW2 - MIN_GAP"),                            # side-wall notch for bracket / pin / cable
    ("NR1", "RCR + BW2 + MIN_GAP"),
    ("NL0", "RCL - BW2 - MIN_GAP"),
    ("NL1", "RCL + BW2 + MIN_GAP"),
    ("NZ0", "BZ0 - MIN_GAP"),
    ("PADX0", "DX + MIN_GAP"),                                 # rail pads beside the display
    ("PADX1", "IX - MIN_GAP"),
    # hinge (D-006 axis; representative barrel + leaves in the Round C corner reserves)
    ("HAY", "BODY_DEPTH - HINGE_AXIS_OFFSET"),
    ("HAZ", "BODY_HEIGHT + HINGE_AXIS_HEIGHT"),
    ("HR", "HINGE_BARREL_DIAMETER / 2"),
    ("HX0", "IX - HINGE_MOUNT_WIDTH"),
    ("HLY0", "IY1 - HINGE_MOUNT_DEPTH"),                       # leaf front edge
    ("HTY", "HAY - HR - MIN_GAP"),                             # leaf trim: clear of the other half's barrel
    ("HTY1", "HAY - HR / 2"),                                  # tongue into its own barrel
    ("HLZ1", "HAZ + HR + MIN_GAP"),                            # lid hinge notch top / corner-block bottom
    ("HBZ0", "HAZ - HR - MIN_GAP"),                            # base hinge pocket bottom
    ("KNW", "(HINGE_MOUNT_WIDTH - 4 * MIN_GAP) / 3"),         # three knuckles, MIN_GAP between and at both ends
    ("K1X0", "HX0 + MIN_GAP"),
    ("K1X1", "K1X0 + KNW"),
    ("K2X0", "K1X1 + MIN_GAP"),
    ("K2X1", "K2X0 + KNW"),
    ("K3X0", "K2X1 + MIN_GAP"),
    ("K3X1", "K3X0 + KNW"),
    ("BLZ0", "BODY_HEIGHT - 2 * WALL_THICKNESS"),              # base leaf under the deck
    ("BLZ1", "BODY_HEIGHT - WALL_THICKNESS"),
    # cables and controller reserve
    ("PW2", "CABLE_CORRIDOR_WIDTH / 2"),
    ("PY0", "IY1 - CABLE_CORRIDOR_HEIGHT"),
    ("CBX0", "PW2 + MIN_GAP"),
    ("CBX1", "HX0 - MIN_GAP"),
    ("CBY0", "LRY1 + MIN_GAP"),
    ("CBZ1", "ZFR + DISPLAY_CONTROLLER_THICKNESS"),
]

# Solar tilt index lock + hub-pin anti-rotation (D-009). Coordinates RELATIVE to the hub axis (dy toward the cable side,
# i.e. +Y on the right cassette and -Y on the left; dz up), cassette frame = lid frame at tilt 0. X values are absolute
# (stowed, right side; mirrored for the left). Angles in degrees: DEG is 1 locally and `degree` in FeatureScript.
# Kept separate from DERIVED so the pinned F3 study (f3_investigation.py, plain + - * / evaluator) is unaffected.
DERIVED_LOCK = [
    ("IXC", "SOLAR_INDEX_RADIUS * cos(SOLAR_INDEX_PIN_ANGLE)"),       # index pin in the cassette
    ("IZC", "SOLAR_INDEX_RADIUS * sin(SOLAR_INDEX_PIN_ANGLE)"),
    ("GX0", "XI + SOLAR_BRACKET_LENGTH"),                             # index groove inboard face (bracket outboard face)
    ("PX0", "GX0 + SOLAR_INDEX_GROOVE_CLEARANCE"),                    # index plate
    ("PX1", "PX0 + SOLAR_INDEX_PLATE_THICKNESS"),                     # = hub pin tip
    ("GX1", "PX1 + SOLAR_INDEX_GROOVE_CLEARANCE"),                    # groove outboard face
    ("GR", "SOLAR_INDEX_PLATE_OUTER_RADIUS + SOLAR_INDEX_GROOVE_RADIAL_CLEARANCE"),
    ("TRB", "ZC0 - HZ"),                                              # tray bottom above the axis
    ("FLZ", "BZ0 - HZ"),                                              # hub-zone floor (bracket bottom) below the axis
    ("BLY", "SOLAR_HUB_CABLE_OFFSET - BW2"),                          # hub-zone band edge away from the cable (< 0)
    ("PAB", "asin(FLZ / SOLAR_INDEX_PLATE_OUTER_RADIUS)"),            # index plate outline arc ends
    ("PAT", "180 * DEG - asin(TRB / SOLAR_INDEX_PLATE_OUTER_RADIUS)"),
    ("KR", "SOLAR_HUB_PIN_DIAMETER / 2"),                             # double-D key, flats facing +-Y
    ("KF", "SOLAR_HUB_PIN_KEY_ACROSS_FLATS / 2"),
    ("KZ", "sqrt(KR * KR - KF * KF)"),
    ("KA", "acos(KF / KR)"),
    ("IPX0", "GX0 - SOLAR_INDEX_ENGAGEMENT"),                         # index pin tip (engaged), in the counter sleeve
    ("IPX1", "IPX0 + SOLAR_INDEX_PIN_LENGTH"),
    ("SLX0", "GX0 - SOLAR_INDEX_SLEEVE_LENGTH"),
    ("GDX1", "GX1 + SOLAR_INDEX_GUIDE_LENGTH"),                       # guide bore end = spring channel start
    ("CRX0", "IPX1 - SOLAR_INDEX_CARRIER_LENGTH / 2"),                # slider carrier grips the pin's outer end
    ("CRX1", "CRX0 + SOLAR_INDEX_CARRIER_LENGTH"),
    ("SPX1", "CRX1 + SOLAR_INDEX_SPRING_INSTALLED_LENGTH"),           # spring seat (cover)
    ("CHX1", "SPX1 + SOLAR_INDEX_COVER_END"),                         # channel end
    ("CHW2", "SOLAR_INDEX_SPRING_POCKET_WIDTH / 2"),
    ("CRW2", "SOLAR_INDEX_CARRIER_WIDTH / 2"),
    ("CHZ0", "IZC - CHW2"),                                           # channel floor = cover top
    ("TBX0", "CRX0 + SOLAR_INDEX_CARRIER_LENGTH / 4"),                # thumb tab
    ("TBX1", "CRX1 - SOLAR_INDEX_CARRIER_LENGTH / 4"),
    ("ARX0", "KX0 + SOLAR_ANTIROT_PLATE_INSET"),                      # anti-rotation plate in the carriage
    ("ARX1", "ARX0 + SOLAR_ANTIROT_PLATE_THICKNESS"),
    ("ARS1", "ARX1 + SOLAR_LOCK_SLOT_CLEARANCE"),                     # slot outboard face = start of the pin bore
    ("KBY0", "SOLAR_HUB_CABLE_OFFSET - CW2"),                         # carriage body / boss, relative
    ("KBY1", "SOLAR_HUB_CABLE_OFFSET + CW2"),
    ("KSY1", "SOLAR_HUB_CABLE_OFFSET + BW2"),
    ("KBZ0", "ZR0 + WALL_THICKNESS - HZ"),
    ("KBZ1", "ZR1 - WALL_THICKNESS - HZ"),
    ("KSZ1", "ZR1 - HZ"),
    ("ARY0", "KBY0 + CLEARANCE"),                                     # anti-rotation plate outline, relative
    ("ARY1", "CRO - CD2 - SOLAR_ANTIROT_CABLE_WALL - SOLAR_LOCK_SLOT_CLEARANCE"),
    ("ARZ0", "KBZ0 + SOLAR_ANTIROT_SKIN + SOLAR_LOCK_SLOT_CLEARANCE"),
    ("ARZ1", "KR + SOLAR_ANTIROT_LIGAMENT"),
    ("ARZL", "KBZ1 - MIN_GAP"),
    ("ARYS", "BLY + SOLAR_LOCK_SLOT_CLEARANCE"),
    ("SLY1", "ARY1 + SOLAR_LOCK_SLOT_CLEARANCE"),                     # carriage slot around the plate
    ("SLZ0", "ARZ0 - SOLAR_LOCK_SLOT_CLEARANCE"),
    ("SLZ1", "ARZ1 + SOLAR_LOCK_SLOT_CLEARANCE"),
    ("ADY", "-SOLAR_ANTIROT_DOWEL_OFFSET_Y"),                         # anti-rotation dowel, away from the cable
    ("ADX0", "KX0 + MIN_GAP"),                                          # dowel recessed from the carriage inboard face
    ("ADX1", "ADX0 + SOLAR_ANTIROT_DOWEL_LENGTH"),
]
DERIVED_LOCK += [(f"IH{_k}{_c}", f"SOLAR_INDEX_RADIUS * {_f}(SOLAR_INDEX_PIN_ANGLE + ({_k} - (SOLAR_INDEX_POSITIONS - 1) / 2) "
                  f"* SOLAR_INDEX_STEP)") for _k in range(int(round(P["SOLAR_INDEX_POSITIONS"]))) for _c, _f in (("Y", "cos"), ("Z", "sin"))]
LOCK_FUNCS = {"cos": lambda a: math.cos(math.radians(a)), "sin": lambda a: math.sin(math.radians(a)),
              "tan": lambda a: math.tan(math.radians(a)), "asin": lambda x: math.degrees(math.asin(x)),
              "acos": lambda x: math.degrees(math.acos(x)), "sqrt": math.sqrt}


def _evx(expr, where, get):
    """Layout expression evaluator: + - * /, parameters, DEG (= 1: angles are degrees) and cos/sin/tan/asin/acos/sqrt."""
    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.Name):
            return 1.0 if n.id == "DEG" else get(n.id)
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.USub, ast.UAdd)):
            return -ev(n.operand) if isinstance(n.op, ast.USub) else ev(n.operand)
        if isinstance(n, ast.BinOp) and isinstance(n.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
            a, b = ev(n.left), ev(n.right)
            return {ast.Add: a + b, ast.Sub: a - b, ast.Mult: a * b, ast.Div: a / b if b else math.nan}[type(n.op)]
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in LOCK_FUNCS and len(n.args) == 1:
            return LOCK_FUNCS[n.func.id](ev(n.args[0]))
        raise ValueError(f"{where}: unsupported layout expression {ast.dump(n)}")
    return ev(ast.parse(str(expr), mode="eval"))


def box(label, *c):
    return ("box", label, c)


def cylx(label, *c):
    """Cylinder along X: (cy, cz, d, x0, x1)."""
    return ("cylx", label, c)


def prof(label, x0, x1, edges):
    """Profile prism along X: one closed loop of ("L", y0, z0, y1, z1) / ("A", cy, cz, r, a0, a1) edges (arc CCW)."""
    return ("prof", label, (x0, x1, tuple(edges)))


def mirror(prims):
    """Mirror a right-side primitive list to the left (X -> -X); Y/Z expressions unchanged."""
    out = []
    for kind, label, c in prims:
        if kind == "box":
            out.append(("box", label, (f"-({c[3]})", c[1], c[2], f"-({c[0]})", c[4], c[5])))
        elif kind == "prof":
            out.append(("prof", label, (f"-({c[1]})", f"-({c[0]})", c[2])))
        else:
            out.append(("cylx", label, (c[0], c[1], c[2], f"-({c[4]})", f"-({c[3]})")))
    return out


def _off(base, d):
    """Expression base + d, written compactly (d is an expression string)."""
    d = str(d).strip()
    if d in ("0", "-0"):
        return base
    if d.startswith("-") and re.fullmatch(r"-[A-Za-z_][A-Za-z0-9_]*|-[0-9.]+", d):
        return f"{base} - {d[1:]}"
    return f"{base} + {d}" if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*|[0-9.]+", d) else f"{base} + ({d})"


class _Hub:
    """Relative hub-frame coordinates -> world expressions for one side (dy is toward the cable side)."""

    def __init__(self, side):
        self.s = side
        self.hy = "HYR" if side > 0 else "HYL"

    def y(self, d):
        if self.s > 0:
            return _off(self.hy, d)
        d = str(d).strip()
        return _off(self.hy, d[1:] if d.startswith("-") and re.fullmatch(r"-[A-Za-z_][A-Za-z0-9_]*|-[0-9.]+", d) else
                    (f"-{d}" if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*|[0-9.]+", d) else f"-({d})"))

    @staticmethod
    def z(d):
        return _off("HZ", d)

    def yr(self, d0, d1):
        return (self.y(d0), self.y(d1)) if self.s > 0 else (self.y(d1), self.y(d0))

    def line(self, p, q):
        return ("L", self.y(p[0]), self.z(p[1]), self.y(q[0]), self.z(q[1]))

    def arc(self, r, a0, a1):
        if self.s > 0:
            return ("A", self.hy, "HZ", r, a0, a1)
        return ("A", self.hy, "HZ", r, f"180 * DEG - ({a1})", f"180 * DEG - ({a0})")

    def poly(self, pts):
        return [self.line(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts))]

    def box(self, label, x0, dy0, dz0, x1, dy1, dz1):
        y0, y1 = self.yr(dy0, dy1)
        return box(label, x0, y0, self.z(dz0), x1, y1, self.z(dz1))

    def cyl(self, label, dy, dz, d, x0, x1):
        return cylx(label, self.y(dy), self.z(dz), d, x0, x1)

    def key(self):
        """Double-D key loop (hub-pin end section / plate key hole), flats facing +-Y."""
        return [self.line(("KF", "-KZ"), ("KF", "KZ")), self.arc("KR", "KA", "180 * DEG - KA"),
                self.line(("-KF", "KZ"), ("-KF", "-KZ")), self.arc("KR", "180 * DEG + KA", "360 * DEG - KA")]


def rail(rc, side):
    prims = [box("floor", "KX0", f"{rc} - RW2", "ZR0", "RX1", f"{rc} + RW2", "ZR0 + WALL_THICKNESS"),
             box("wall_a", "KX0", f"{rc} - RW2", "ZR0 + WALL_THICKNESS", "RX1", f"{rc} - RW2 + WALL_THICKNESS", "ZR1 - WALL_THICKNESS"),
             box("wall_b", "KX0", f"{rc} + RW2 - WALL_THICKNESS", "ZR0 + WALL_THICKNESS", "RX1", f"{rc} + RW2", "ZR1 - WALL_THICKNESS"),
             box("lip_a", "KX0", f"{rc} - RW2", "ZR1 - WALL_THICKNESS", "RX1", f"{rc} - SW2", "ZR1"),
             box("lip_b", "KX0", f"{rc} + SW2", "ZR1 - WALL_THICKNESS", "RX1", f"{rc} + RW2", "ZR1"),
             box("end_stop", "KX0 - WALL_THICKNESS", f"{rc} - RW2", "ZR0", "KX0", f"{rc} + RW2", "ZR1")]
    return prims if side > 0 else mirror(prims)


def side_parts_e2(side):
    """One solar side as built in E2 / F3 (pre index lock): rail, carriage, hub pin, hub bracket, cassette, cable run."""
    s = "R" if side > 0 else "L"
    rc, hy = ("RCR", "HYR") if side > 0 else ("RCL", "HYL")
    cy = f"{hy} + CRO" if side > 0 else f"{hy} - CRO"
    parts = {
        "rail": rail(rc, side),
        # F3 option B: the body fills the channel (floor top to lip underside); the boss rises through the slot to the
        # rail top so the raised pin keeps MIN_WALL of carriage above it
        "carriage": [box("body", "KX0", f"{rc} - CW2", "ZR0 + WALL_THICKNESS", "KX1", f"{rc} + CW2", "ZR1 - WALL_THICKNESS"),
                     box("boss", "KX0", f"{rc} - BW2", "ZR1 - WALL_THICKNESS", "KX1", f"{rc} + BW2", "ZR1")],
        "pin": [cylx("pin", hy, "HZ", "SOLAR_HUB_PIN_DIAMETER", "KX1", "XI")],
        "bracket": [box("bracket", "XI", f"{rc} - BW2", "BZ0", "XI + SOLAR_BRACKET_LENGTH", f"{rc} + BW2", "ZC0")],
        "cassette": [box("envelope", "XI", "CY0", "ZC0", "XI + SOLAR_CASSETTE_WIDTH", "CY1", "ZC1")],
        "cable": [box("run", "KX0", f"{cy} - CD2", "HZ - CD2", "XI", f"{cy} + CD2", "HZ + CD2")],
    }
    if side < 0:
        for k in ("carriage", "pin", "bracket", "cassette", "cable"):
            parts[k] = mirror(parts[k])
    return s, parts


def side_parts(side):
    """One solar side with the D-009 index lock and hub-pin anti-rotation (Round E): the E2 rail / cable run unchanged;
    carriage (anti-rotation slot, access / pin / dowel / push-out bores), hub pin (round through the carriage, link and
    bracket bore, 3.0 A/F double-D at both ends), anti-rotation plate + dowel, M2 screws + washers, index plate (11
    reamed holes, keyed on the pin tip), bracket bore, cassette (plate groove, counter-sleeve bore, guide bore, spring /
    carrier channel), index pin, counter sleeve, slider (carrier + thumb tab), spring envelope, channel cover."""
    s, parts = side_parts_e2(side)
    h = _Hub(side)
    rc = "RCR" if side > 0 else "RCL"
    T = [("KBY0", "KBZ0"), ("KBY1", "KBZ0"), ("KBY1", "KBZ1"), ("KSY1", "KBZ1"), ("KSY1", "KSZ1"), ("BLY", "KSZ1"),
         ("BLY", "KBZ1"), ("KBY0", "KBZ1")]
    TS = [("KBY0", "KBZ0"), ("KBY1", "KBZ0"), ("KBY1", "KBZ1"), ("KSY1", "KBZ1"), ("KSY1", "KSZ1"), ("BLY", "KSZ1"),
          ("BLY", "SLZ1"), ("SLY1", "SLZ1"), ("SLY1", "SLZ0"), ("KBY0", "SLZ0")]
    AR = [("ARY0", "ARZ0"), ("ARY1", "ARZ0"), ("ARY1", "ARZ1"), ("ARYS", "ARZ1"), ("ARYS", "ARZL"), ("ARY0", "ARZL")]
    PIN, HOLE = "SOLAR_HUB_PIN_DIAMETER", "SOLAR_INDEX_HOLE_DIAMETER"
    DZ = "SOLAR_ANTIROT_DOWEL_OFFSET_Z"
    n = int(round(P["SOLAR_INDEX_POSITIONS"]))
    holes = []
    for k in range(n):
        holes.append(h.cyl(f"index_hole_{k}", f"IH{k}Y", f"IH{k}Z", HOLE, "PX0", "PX1"))
    outline = [h.arc("SOLAR_INDEX_PLATE_OUTER_RADIUS", "PAB", "PAT"),
               h.line(("SOLAR_INDEX_PLATE_OUTER_RADIUS * cos(PAT)", "TRB"), ("BLY", "TRB")),
               h.line(("BLY", "TRB"), ("BLY", "FLZ")),
               h.line(("BLY", "FLZ"), ("SOLAR_INDEX_PLATE_OUTER_RADIUS * cos(PAB)", "FLZ"))]
    lock = {
        "carriage": ([prof("slab_inboard", "KX0", "ARX0", h.poly(T)), prof("slab_slot", "ARX0", "ARS1", h.poly(TS)),
                      prof("slab_outboard", "ARS1", "KX1", h.poly(T))],
                     [h.cyl("access_bore", "0", "0", "SOLAR_HUB_ACCESS_DIAMETER", "KX0", "ARX0"),
                      h.cyl("pin_bore", "0", "0", PIN, "ARS1", "KX1"),
                      h.cyl("dowel_bore", "ADY", DZ, "SOLAR_ANTIROT_DOWEL_DIAMETER", "KX0", "ADX1"),
                      h.cyl("dowel_push_out", "ADY", DZ, "SOLAR_ANTIROT_PUSHOUT_DIAMETER", "ADX1", "KX1")]),
        "pin": ([prof("key_inboard", "ARX0", "ARX1", h.key()), h.cyl("round", "0", "0", PIN, "ARX1", "PX0"),
                 prof("key_tip", "PX0", "PX1", h.key())], []),
        "antirot": ([prof("plate", "ARX0", "ARX1", h.poly(AR))],
                    [prof("key_hole", "ARX0", "ARX1", h.key()),
                     h.cyl("dowel_hole", "ADY", DZ, "SOLAR_ANTIROT_DOWEL_DIAMETER", "ARX0", "ARX1")]),
        "dowel": ([h.cyl("dowel", "ADY", DZ, "SOLAR_ANTIROT_DOWEL_DIAMETER", "ADX0", "ADX1")], []),
        "screw_in": ([h.cyl("washer", "0", "0", "SOLAR_HUB_WASHER_DIAMETER", "ARX0 - SOLAR_HUB_WASHER_THICKNESS", "ARX0"),
                      h.cyl("head", "0", "0", "SOLAR_HUB_SCREW_HEAD_DIAMETER",
                            "ARX0 - SOLAR_HUB_WASHER_THICKNESS - SOLAR_HUB_SCREW_HEAD_HEIGHT", "ARX0 - SOLAR_HUB_WASHER_THICKNESS")], []),
        "screw_tip": ([h.cyl("washer", "0", "0", "SOLAR_HUB_WASHER_DIAMETER", "PX1", "PX1 + SOLAR_HUB_WASHER_THICKNESS"),
                       h.cyl("head", "0", "0", "SOLAR_HUB_SCREW_HEAD_DIAMETER", "PX1 + SOLAR_HUB_WASHER_THICKNESS",
                             "PX1 + SOLAR_HUB_WASHER_THICKNESS + SOLAR_HUB_SCREW_HEAD_HEIGHT")], []),
        "index_plate": ([prof("plate", "PX0", "PX1", outline)], [prof("key_hole", "PX0", "PX1", h.key())] + holes),
        "bracket": ([box("bracket", "XI", f"{rc} - BW2", "BZ0", "XI + SOLAR_BRACKET_LENGTH", f"{rc} + BW2", "ZC0")],
                    [h.cyl("bore", "0", "0", PIN, "XI", "GX0")]),
        "cassette": ([box("envelope", "XI", "CY0", "ZC0", "XI + SOLAR_CASSETTE_WIDTH", "CY1", "ZC1")],
                     [h.box("index_groove", "GX0", "-GR", "0", "GX1", "GR", "GR"),
                      h.cyl("counter_sleeve_bore", "IXC", "IZC", "SOLAR_INDEX_SLEEVE_OD", "SLX0", "GX0"),
                      h.cyl("grit_relief", "IXC", "IZC", HOLE, "XI", "SLX0"),
                      h.cyl("guide_bore", "IXC", "IZC", HOLE, "GX1", "GDX1"),
                      h.box("spring_channel", "GDX1", "IXC - CHW2", "0", "CHX1", "IXC + CHW2", "IZC + CHW2")]),
        "index_pin": ([h.cyl("pin", "IXC", "IZC", "SOLAR_INDEX_PIN_DIAMETER", "IPX0", "IPX1")], []),
        "sleeve": ([h.cyl("sleeve", "IXC", "IZC", "SOLAR_INDEX_SLEEVE_OD", "SLX0", "GX0")],
                   [h.cyl("bore", "IXC", "IZC", HOLE, "SLX0", "GX0")]),
        "slider": ([h.box("carrier", "CRX0", "IXC - CRW2", "IZC - CRW2", "CRX1", "IXC + CRW2", "IZC + CRW2"),
                    h.box("thumb_tab", "TBX0", "IXC - SOLAR_INDEX_PIN_DIAMETER / 2", "TRB + CLEARANCE", "TBX1",
                          "IXC + SOLAR_INDEX_PIN_DIAMETER / 2", "IZC - CRW2")],
                   [h.cyl("pin_socket", "IXC", "IZC", "SOLAR_INDEX_PIN_DIAMETER", "CRX0", "IPX1")]),
        "spring": ([h.cyl("spring", "IXC", "IZC", "SOLAR_INDEX_SPRING_OD", "CRX1", "SPX1")], []),
        "cover": ([h.box("floor", "GDX1", "IXC - CHW2", "TRB", "CHX1", "IXC + CHW2", "CHZ0"),
                   h.box("spring_seat", "SPX1", "IXC - CHW2", "CHZ0", "CHX1", "IXC + CHW2", "IZC + CHW2")],
                  [h.box("tab_slot", "TBX0 - SOLAR_LOCK_SLOT_CLEARANCE", "IXC - SOLAR_INDEX_PIN_DIAMETER / 2 - SOLAR_LOCK_SLOT_CLEARANCE",
                         "TRB - MIN_GAP", "TBX1 + SOLAR_INDEX_PIN_STROKE + SOLAR_LOCK_SLOT_CLEARANCE",
                         "IXC + SOLAR_INDEX_PIN_DIAMETER / 2 + SOLAR_LOCK_SLOT_CLEARANCE", "CHZ0 + MIN_GAP")]),
    }
    if side < 0:
        lock = {k: (mirror(v[0]), mirror(v[1])) for k, v in lock.items()}
    return s, parts, lock


def hinge_parts(side):
    base = [cylx("knuckle_1", "HAY", "HAZ", "HINGE_BARREL_DIAMETER", "K1X0", "K1X1"),
            cylx("knuckle_3", "HAY", "HAZ", "HINGE_BARREL_DIAMETER", "K3X0", "K3X1"),
            box("leaf", "HX0", "HLY0", "BLZ0", "IX", "HTY", "BLZ1"),
            box("tongue_1", "K1X0", "HTY", "BLZ0", "K1X1", "HTY1", "BLZ1"),
            box("tongue_3", "K3X0", "HTY", "BLZ0", "K3X1", "HTY1", "BLZ1")]
    lid = [cylx("knuckle_2", "HAY", "HAZ", "HINGE_BARREL_DIAMETER", "K2X0", "K2X1"),
           box("leaf", "HX0", "HLY0", "ZF", "IX", "HTY", "HLZ1"),
           box("tongue_2", "K2X0", "HTY", "ZF", "K2X1", "HTY1", "HLZ1")]
    return (base, lid) if side > 0 else (mirror(base), mirror(lid))


PROV = "PROVISIONAL - PENDING P0.2 PHYSICAL VALIDATION"

# (name, displayed name, group, appearance key, adds, subs). Groups: lid (rotates with the lid), carR / carL (slide),
# casR / casL (slide + tilt), baseHinge (fixed to the base). Keep-outs are KEEPOUT_* (visualization toggle).
_LID_PARTS = [
    ("LID_FRAME", f"LID_FRAME [class A front frame - {PROV}]", "lid", "structure", [
        box("face", "-IX", "IY0", "ZF", "IX", "IY1", "ZFR"),
        box("wall_front", "-W2", "0", "ZF", "W2", "IY0", "ZS0"),
        box("wall_rear", "-W2", "IY1", "ZF", "W2", "BODY_DEPTH", "ZS0"),
        box("wall_left", "-W2", "IY0", "ZF", "-IX", "IY1", "ZS0"),
        box("wall_right", "IX", "IY0", "ZF", "W2", "IY1", "ZS0"),
        box("band_front", "-IX", "IY0", "ZC0 - MIN_GAP", "IX", "CY0 - MIN_GAP", "ZS0"),
        box("band_rear", "-IX", "CY1 + MIN_GAP", "ZC0 - MIN_GAP", "IX", "IY1", "ZS0"),
        box("pad_right", "PADX0", "RCR - RW2", "ZFR", "PADX1", "RCR + RW2", "ZR0"),
        box("pad_left", "-PADX1", "RCL - RW2", "ZFR", "-PADX0", "RCL + RW2", "ZR0"),
        box("hinge_block_right", "HX0", "CY1 + MIN_GAP", "HLZ1", "IX", "IY1", "ZC0 - MIN_GAP"),
        box("hinge_block_left", "-IX", "CY1 + MIN_GAP", "HLZ1", "-HX0", "IY1", "ZC0 - MIN_GAP"),
    ], [
        box("display_opening", "-DX", "DY0", "ZD0", "DX", "DY1", "ZD1"),
        box("active_window", "-AX", "AY0", "ZF - WALL_THICKNESS", "AX", "AY1", "ZD0"),
        box("slot_right", "IX", "CY0 - MIN_GAP", "ZC0 - MIN_GAP", "W2 + WALL_THICKNESS", "CY1 + MIN_GAP", "ZS0 + WALL_THICKNESS"),
        box("slot_left", "-W2 - WALL_THICKNESS", "CY0 - MIN_GAP", "ZC0 - MIN_GAP", "-IX", "CY1 + MIN_GAP", "ZS0 + WALL_THICKNESS"),
        box("notch_right", "IX", "NR0", "NZ0", "W2 + WALL_THICKNESS", "NR1", "ZC0"),
        box("notch_left", "-W2 - WALL_THICKNESS", "NL0", "NZ0", "-IX", "NL1", "ZC0"),
        box("hinge_notch_right", "HX0", "HLY0", "ZF - WALL_THICKNESS", "IX", "BODY_DEPTH + WALL_THICKNESS", "HLZ1"),
        box("hinge_notch_left", "-IX", "HLY0", "ZF - WALL_THICKNESS", "-HX0", "BODY_DEPTH + WALL_THICKNESS", "HLZ1"),
        box("display_cable_pass", "-PW2", "PY0", "ZF - WALL_THICKNESS", "PW2", "BODY_DEPTH + WALL_THICKNESS", "ZFR"),
    ]),
    ("DISPLAY", "DISPLAY [10.1in 1920x1200 16:10 envelope 235x150x5 - SKU not selected]", "lid", "display", [
        box("module", "-DX", "DY0", "ZD0", "DX", "DY1", "ZD1")], []),
    ("LID_REAR_SHELL", f"LID_REAR_SHELL [sandwich 1.2/4.2/1.2, cells not modeled - {PROV}]", "lid", "shell", [
        box("shell", "-W2", "0", "ZS0", "W2", "BODY_DEPTH", "ZS1")], []),
]
_LID_KEEPOUTS = [
    ("KEEPOUT_SOLAR_LOOP_R", "KEEPOUT_SOLAR_LOOP_R", "lid", "C", [box("loop", "LPX0", "LRY0", "ZR0", "LPX1", "LRY1", "ZR1")], []),
    ("KEEPOUT_SOLAR_LOOP_L", "KEEPOUT_SOLAR_LOOP_L", "lid", "C", [box("loop", "-LPX1", "LLY0", "ZR0", "-LPX0", "LLY1", "ZR1")], []),
    ("KEEPOUT_SOLAR_CORRIDOR", "KEEPOUT_SOLAR_CORRIDOR [8 mm cable corridor]", "lid", "C",
     [box("corridor", "-CORX", "RCL + RW2", "ZR0", "CORX", "RCR - RW2", "ZR1")], []),
    ("KEEPOUT_DISPLAY_FLEX", "KEEPOUT_DISPLAY_FLEX [display cable path, assumed hinge-side exit]", "lid", "C",
     [box("flex", "-PW2", "DY1", "ZFR", "PW2", "PY0", "ZR0")], []),
    ("KEEPOUT_LID_DISPLAY_PASS", "KEEPOUT_LID_DISPLAY_PASS [lid-to-base cable pass at the hinge]", "lid", "W",
     [box("pass", "-PW2", "PY0", "BODY_HEIGHT", "PW2", "BODY_DEPTH", "ZFR")], []),
    ("KEEPOUT_CONTROLLER_BAND_R", "KEEPOUT_CONTROLLER_BAND_R [display controller reserve 12 mm; location not decided]", "lid", "K",
     [box("band", "CBX0", "CBY0", "ZFR", "CBX1", "IY1", "CBZ1")], []),
    ("KEEPOUT_CONTROLLER_BAND_L", "KEEPOUT_CONTROLLER_BAND_L [display controller reserve 12 mm; location not decided]", "lid", "K",
     [box("band", "-CBX1", "CBY0", "ZFR", "-CBX0", "IY1", "CBZ1")], []),
]



def _build_parts(with_lock):
    """E2 part table; with_lock adds the D-009 index lock / anti-rotation parts and replaces the E2 carriage, pin,
    bracket and cassette with their lock-integrated versions (the E2 table is kept for the pinned F3 study)."""
    parts = list(_LID_PARTS)
    for _side in (1, -1):
        if with_lock:
            _s, _p, _k = side_parts(_side)
        else:
            _s, _p = side_parts_e2(_side)
        c, k = f"car{_s}", f"cas{_s}"
        parts.append((f"SOLAR_RAIL_{_s}", f"SOLAR_RAIL_{_s} [structural rail, V1 + fixes; reinforcement pending P0.2]", "lid", "rail", _p["rail"], []))
        if not with_lock:
            parts += [
                (f"SOLAR_CARRIAGE_{_s}", f"SOLAR_CARRIAGE_{_s} [22.6 x 8 x 40 + 17 x 2.5 slot boss, provisional]", c, "carriage", _p["carriage"], []),
                (f"SOLAR_HUB_PIN_{_s}", f"SOLAR_HUB_PIN_{_s} [metal pin, tilt axis]", c, "hardware", _p["pin"], []),
                (f"SOLAR_HUB_BRACKET_{_s}", f"SOLAR_HUB_BRACKET_{_s} [hub bracket; index / lock not designed]", k, "bracket", _p["bracket"], []),
                (f"SOLAR_CASSETTE_{_s}", f"SOLAR_CASSETTE_{_s} [envelope 200 x 147.5 x 8 - panel not selected]", k, "cassette", _p["cassette"], []),
            ]
        else:
            parts += [
                (f"SOLAR_CARRIAGE_{_s}", f"SOLAR_CARRIAGE_{_s} [22.6 x 8 x 40 + slot boss; anti-rotation slot, bores - provisional]", c, "carriage", *_k["carriage"]),
                (f"SOLAR_HUB_PIN_{_s}", f"SOLAR_HUB_PIN_{_s} [5 x 53.5, 303/304 cold-drawn; 3.0 A/F double-D both ends]", c, "hardware", *_k["pin"]),
                (f"SOLAR_ANTIROT_PLATE_{_s}", f"SOLAR_ANTIROT_PLATE_{_s} [1.5 stainless 301 1/2-hard or 17-4PH]", c, "stainless", *_k["antirot"]),
                (f"SOLAR_ANTIROT_DOWEL_{_s}", f"SOLAR_ANTIROT_DOWEL_{_s} [3 x 24 dowel ISO 2338 m6]", c, "hardware", *_k["dowel"]),
                (f"SOLAR_HUB_SCREW_IN_{_s}", f"SOLAR_HUB_SCREW_IN_{_s} [M2 screw + washer, envelope]", c, "hardware", *_k["screw_in"]),
                (f"SOLAR_HUB_SCREW_TIP_{_s}", f"SOLAR_HUB_SCREW_TIP_{_s} [M2 screw + washer, envelope]", c, "hardware", *_k["screw_tip"]),
                (f"SOLAR_INDEX_PLATE_{_s}", f"SOLAR_INDEX_PLATE_{_s} [1.5 stainless, 11 x 1.60 reamed on R10, 15 deg]", c, "stainless", *_k["index_plate"]),
                (f"SOLAR_HUB_BRACKET_{_s}", f"SOLAR_HUB_BRACKET_{_s} [hub bracket, 5 bore]", k, "bracket", *_k["bracket"]),
                (f"SOLAR_CASSETTE_{_s}", f"SOLAR_CASSETTE_{_s} [envelope 200 x 147.5 x 8 - panel not selected; index-lock features]", k, "cassette", *_k["cassette"]),
                (f"SOLAR_INDEX_PIN_{_s}", f"SOLAR_INDEX_PIN_{_s} [1.5 x 16 hardened dowel ISO 8734]", k, "hardware", *_k["index_pin"]),
                (f"SOLAR_INDEX_SLEEVE_{_s}", f"SOLAR_INDEX_SLEEVE_{_s} [stainless counter sleeve 2.5 / 1.6 x 4, pressed]", k, "stainless", *_k["sleeve"]),
                (f"SOLAR_INDEX_SLIDER_{_s}", f"SOLAR_INDEX_SLIDER_{_s} [printed carrier + thumb tab]", k, "bracket", *_k["slider"]),
                (f"SOLAR_INDEX_SPRING_{_s}", f"SOLAR_INDEX_SPRING_{_s} [stainless compression spring, envelope]", k, "hardware", *_k["spring"]),
                (f"SOLAR_INDEX_COVER_{_s}", f"SOLAR_INDEX_COVER_{_s} [printed channel cover / spring seat]", k, "bracket", *_k["cover"]),
            ]
        parts.append((f"KEEPOUT_SOLAR_CABLE_RUN_{_s}", f"KEEPOUT_SOLAR_CABLE_RUN_{_s}", c, "C", _p["cable"], []))
        _b, _l = hinge_parts(_side)
        parts += [
            (f"HINGE_BASE_HALF_{_s}", f"HINGE_BASE_HALF_{_s} [representative barrel 8 + leaf; hardware TBD]", "baseHinge", "hinge", _b, []),
            (f"HINGE_LID_HALF_{_s}", f"HINGE_LID_HALF_{_s} [representative barrel 8 + leaf; hardware TBD]", "lid", "hinge", _l, []),
        ]
    return parts + _LID_KEEPOUTS


PARTS_E2 = _build_parts(False)
PARTS = _build_parts(True)

BASE_POCKETS = [box("hinge_pocket_right", "HX0", "HTY", "HBZ0", "IX", "BODY_DEPTH + WALL_THICKNESS", "BODY_HEIGHT + WALL_THICKNESS"),
                box("hinge_pocket_left", "-IX", "HTY", "HBZ0", "-HX0", "BODY_DEPTH + WALL_THICKNESS", "BODY_HEIGHT + WALL_THICKNESS")]

# Mate connectors: (name, owner part, origin exprs, x axis, z axis). Revolute / slider act about / along Z.
CONNECTORS = [
    ("MC_HINGE_LID", "LID_FRAME", ("0", "HAY", "HAZ"), (0, 1, 0), (-1, 0, 0)),
    ("MC_RAIL_R", "SOLAR_RAIL_R", ("KX1", "RCR", "HZ"), (0, 1, 0), (1, 0, 0)),
    ("MC_CARRIAGE_R", "SOLAR_CARRIAGE_R", ("KX1", "RCR", "HZ"), (0, 1, 0), (1, 0, 0)),
    ("MC_HUB_R", "SOLAR_CARRIAGE_R", ("XI", "HYR", "HZ"), (0, 1, 0), (1, 0, 0)),
    ("MC_CASSETTE_R", "SOLAR_CASSETTE_R", ("XI", "HYR", "HZ"), (0, 1, 0), (1, 0, 0)),
    ("MC_RAIL_L", "SOLAR_RAIL_L", ("-(KX1)", "RCL", "HZ"), (0, 1, 0), (-1, 0, 0)),
    ("MC_CARRIAGE_L", "SOLAR_CARRIAGE_L", ("-(KX1)", "RCL", "HZ"), (0, 1, 0), (-1, 0, 0)),
    ("MC_HUB_L", "SOLAR_CARRIAGE_L", ("-(XI)", "HYL", "HZ"), (0, 1, 0), (-1, 0, 0)),
    ("MC_CASSETTE_L", "SOLAR_CASSETTE_L", ("-(XI)", "HYL", "HZ"), (0, 1, 0), (-1, 0, 0)),
]


# ------------------------------------------------------------------ evaluation
def evaluate(table=None):
    env = dict(P)
    for name, expr in DERIVED:
        env[name] = _eval_formula(expr, name, lambda k: env[k])
    for name, expr in DERIVED_LOCK:
        env[name] = _evx(expr, name, lambda k: env[k])

    def ev(e, where):
        return _evx(e, where, lambda k: env[k])

    def prims(lst, where):
        out = []
        for kind, label, c in lst:
            if kind == "prof":
                x0, x1 = ev(c[0], f"{where}.{label}"), ev(c[1], f"{where}.{label}")
                edges = []
                for e in c[2]:
                    v = [ev(x, f"{where}.{label}") for x in e[1:]]
                    if e[0] == "L":
                        edges.append(("L", (v[0], v[1]), (v[2], v[3])))
                    else:
                        assert v[3] < v[4] <= v[3] + 360 + 1e-9, f"{where}.{label}: bad arc {v}"
                        edges.append(("A", (v[0], v[1]), v[2], v[3], v[4]))
                assert x0 < x1, f"{where}.{label}: empty profile prism"
                out.append((kind, label, [x0, x1, edges]))
                continue
            v = [ev(x, f"{where}.{label}") for x in c]
            if kind == "box":
                assert v[0] < v[3] and v[1] < v[4] and v[2] < v[5], f"{where}.{label}: empty box {v}"
            else:
                assert v[2] > 0 and v[3] < v[4], f"{where}.{label}: bad cylinder {v}"
            out.append((kind, label, v))
        return out

    parts = [(n, disp, g, key, prims(a, n), prims(s, n)) for n, disp, g, key, a, s in (table or PARTS)]
    pockets = prims(BASE_POCKETS, "BASE_POCKETS")
    conns = [(n, o, [ev(x, n) for x in org], xa, za) for n, o, org, xa, za in CONNECTORS]
    return env, parts, pockets, conns


# ------------------------------------------------------------------ prism geometry (X interval x convex Y-Z polygon)
def _box_minus(a, b):
    """Axis-aligned box a minus box b -> list of disjoint boxes."""
    if any(b[i] >= a[i + 3] - EPS or b[i + 3] <= a[i] + EPS for i in range(3)):
        return [a]
    out, cur = [], list(a)
    for i in range(3):
        if b[i] > cur[i] + EPS:
            piece = cur[:]
            piece[i + 3] = b[i]
            out.append(tuple(piece))
            cur[i] = b[i]
        if b[i + 3] < cur[i + 3] - EPS:
            piece = cur[:]
            piece[i] = b[i + 3]
            out.append(tuple(piece))
            cur[i + 3] = b[i + 3]
    return out


def _circle(cy, cz, r):
    """Exact circle cross-section (X cylinders): ("circ", centre, r)."""
    return ("circ", (cy, cz), r)


def _poly_signed_dist(pt, poly):
    """Signed distance from a point to a convex polygon (positive outside, negative inside)."""
    n = len(poly)
    dmin = min(hm._seg_dist(pt, poly[i], poly[(i + 1) % n]) for i in range(n))
    area = sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))
    inside = all((poly[(i + 1) % n][0] - poly[i][0]) * (pt[1] - poly[i][1]) - (poly[(i + 1) % n][1] - poly[i][1]) * (pt[0] - poly[i][0])
                 >= -1e-12 if area > 0 else
                 (poly[(i + 1) % n][0] - poly[i][0]) * (pt[1] - poly[i][1]) - (poly[(i + 1) % n][1] - poly[i][1]) * (pt[0] - poly[i][0])
                 <= 1e-12 for i in range(n))
    return -dmin if inside else dmin


def _as_reg(s):
    if isinstance(s, rg.Reg):
        return s
    if isinstance(s, tuple) and s[0] == "circ":
        return rg.from_circle(s[1], s[2])
    return rg.from_poly(s)


def _yz_bbox(s):
    if isinstance(s, rg.Reg):
        return s.bbox()
    if isinstance(s, tuple) and s[0] == "circ":
        return (s[1][0] - s[2], s[1][1] - s[2], s[1][0] + s[2], s[1][1] + s[2])
    return (min(y for y, _ in s), min(z for _, z in s), max(y for y, _ in s), max(z for _, z in s))


def _yz_clear(a, b):
    if isinstance(a, rg.Reg) or isinstance(b, rg.Reg):
        return rg.clearance(_as_reg(a), _as_reg(b))
    ca, cb = isinstance(a, tuple) and a[0] == "circ", isinstance(b, tuple) and b[0] == "circ"
    if ca and cb:
        return math.dist(a[1], b[1]) - a[2] - b[2]
    if ca:
        return _poly_signed_dist(a[1], b) - a[2]
    if cb:
        return _poly_signed_dist(b[1], a) - b[2]
    return hm.signed_clearance(a, b)


def _rot(shape, axis, deg):
    if isinstance(shape, rg.Reg):
        return rg.rotate(shape, axis, deg)
    if isinstance(shape, tuple) and shape[0] == "circ":
        return ("circ", hm.rotate([shape[1]], axis, deg)[0], shape[2])
    return hm.rotate(shape, axis, deg)


def _zmin(shape):
    if isinstance(shape, rg.Reg):
        return rg.zmin(shape)
    if isinstance(shape, tuple) and shape[0] == "circ":
        return shape[1][1] - shape[2]
    return min(z for _, z in shape)


def _hole_inside(H, base):
    """True if hole region H lies strictly inside the material of region `base` (no boundary contact)."""
    d = min(rg.edge_dist(e, f) for e in H.edges() for f in base.edges())
    p = rg._edge_samples(H.outer[0], (0.5,))[0][0]
    return d > 1e-9 and rg.in_region(p, base)


def to_prisms(adds, subs):
    """Part primitives -> X-prisms. Box adds minus box subs (exact boxes); cylinder / profile subtractions become holes
    of the pieces they fall inside (a subtraction may also lie wholly in empty space: skipped; one that straddles a
    part boundary is rejected). Cylinder adds stay exact circles; profile adds are rg.Reg regions."""
    box_subs = [tuple(v) for k, _, v in subs if k == "box"]
    holes = [(v[3], v[4], rg.loop_circle((v[0], v[1]), v[2] / 2)) if k == "cylx" else (v[0], v[1], list(v[2]))
             for k, _, v in subs if k in ("cylx", "prof")]
    boxes = [tuple(v) for k, _, v in adds if k == "box"]
    for sv_ in box_subs:
        boxes = [nb for bb in boxes for nb in _box_minus(bb, sv_)]
    pieces = [(bb[0], bb[3], hm.rect(bb[1], bb[4], bb[2], bb[5])) for bb in boxes]
    for k, _, v in adds:
        if k == "cylx":
            for sv_ in box_subs:
                assert (sv_[3] <= v[3] or sv_[0] >= v[4] or sv_[4] <= v[0] - v[2] / 2 or sv_[1] >= v[0] + v[2] / 2
                        or sv_[5] <= v[1] - v[2] / 2 or sv_[2] >= v[1] + v[2] / 2), "box subtraction through a cylinder"
            pieces.append((v[3], v[4], _circle(v[0], v[1], v[2] / 2)))
        elif k == "prof":
            assert not any(sv_[3] > v[0] and sv_[0] < v[1] for sv_ in box_subs), "box subtraction through a profile"
            pieces.append((v[0], v[1], rg.Reg(v[2])))
    if not holes:
        return pieces
    out = []
    for x0, x1, shp in pieces:
        cuts = sorted({x0, x1} | {h[i] for h in holes for i in (0, 1) if x0 + EPS < h[i] < x1 - EPS})
        for a, b in zip(cuts, cuts[1:]):
            base = None
            inside = []
            for h0, h1, loop in holes:
                if h1 <= a + EPS or h0 >= b - EPS:
                    continue
                base = base or _as_reg(shp)
                H = rg.Reg(loop)
                if rg.clearance(H, base) >= -EPS:
                    continue                                   # subtraction in empty space
                assert _hole_inside(H, base), "subtraction straddles a part boundary (unsupported)"
                inside.append(loop)
            out.append((a, b, shp if not inside else rg.Reg(base.outer, base.holes + inside)))
    return out


def base_prisms(pockets):
    """Round C base parts as prisms (Z cylinders -> bounding boxes, conservative); BASE_SHELL gets the hinge pockets."""
    _, parts = bl.evaluate()
    out = {}
    for name, cat, prims in parts:
        boxes = []
        for k, _, v in prims:
            if k == "box":
                boxes.append(tuple(v))
            else:
                boxes.append((v[0] - v[2] / 2, v[1] - v[2] / 2, v[3], v[0] + v[2] / 2, v[1] + v[2] / 2, v[4]))
        if name == "BASE_SHELL":
            for _, _, pv in pockets:
                nxt = []
                for bb in boxes:
                    nxt += _box_minus(bb, tuple(pv))
                boxes = nxt
        out[name] = (cat, [(bb[0], bb[3], hm.rect(bb[1], bb[4], bb[2], bb[5])) for bb in boxes])
    return out


def _clearance(a, b):
    """Signed clearance of two X-prisms (same combination rule as solar_skeleton_model.clearance)."""
    xo = min(a[1], b[1]) - max(a[0], b[0])
    s = _yz_clear(a[2], b[2])
    if xo > 1e-9 and s < 0:
        return -min(xo, -s)
    return math.hypot(max(0.0, -xo), max(0.0, s))


def _lower_bound(a, b):
    """Bounding-box lower bound of _clearance(a, b) (-inf when the boxes overlap)."""
    xg = max(a[0], b[0]) - min(a[1], b[1])
    ba, bb = _yz_bbox(a[2]), _yz_bbox(b[2])
    yg = max(ba[0], bb[0]) - min(ba[2], bb[2])
    zg = max(ba[1], bb[1]) - min(ba[3], bb[3])
    if xg <= 0 and yg <= 0 and zg <= 0:
        return -math.inf
    return math.hypot(max(0.0, xg), math.hypot(max(0.0, yg), max(0.0, zg)))


def clear(pa, pb, cut=None):
    """Minimum signed clearance of two parts. With `cut`, a value >= cut may be returned as a bounding-box lower
    bound (only used where values at or above `cut` do not matter)."""
    if cut is not None:
        lb = min(_lower_bound(a, b) for a in pa for b in pb)
        if lb >= cut:
            return lb
    return min(_clearance(a, b) for a in pa for b in pb)


# ------------------------------------------------------------------ poses
_PRISM_CACHE = {}


def pose(parts, env, lid=0.0, ext=(0.0, 0.0), tilt=(0.0, 0.0)):
    """Return {name: prisms} for a pose. ext / tilt = (right, left); tilt sign as the FeatureScript pose
    (right: about +X, left: about -X, right-hand rule)."""
    axis = (env["HAY"], env["HAZ"])
    out = {}
    for name, _, g, _, adds, subs in parts:
        hit = _PRISM_CACHE.get(name)
        if hit is not None and hit[0] is adds and hit[1] is subs:
            pr = hit[2]
        else:
            pr = to_prisms(adds, subs)
            _PRISM_CACHE[name] = (adds, subs, pr)
        side = 0 if g in ("lid", "baseHinge") else (1 if g.endswith("R") else -1)
        if side:
            e, t = (ext[0], tilt[0]) if side > 0 else (ext[1], tilt[1])
            dx = side * e * env["SOLAR_SLIDE_TRAVEL"]
            if g.startswith("cas") and t:
                hub = (env["HYR"] if side > 0 else env["HYL"], env["HZ"])
                pr = [(x0, x1, _rot(poly, hub, -t if side > 0 else t)) for x0, x1, poly in pr]
            pr = [(x0 + dx, x1 + dx, poly) for x0, x1, poly in pr]
        if g != "baseHinge" and lid:
            pr = [(x0, x1, _rot(poly, axis, lid)) for x0, x1, poly in pr]
        out[name] = pr
    return out


# ------------------------------------------------------------------ rules
JOINTS = {frozenset(p) for p in (
    ("SOLAR_CARRIAGE_R", "SOLAR_RAIL_R"), ("SOLAR_CARRIAGE_L", "SOLAR_RAIL_L"),            # slider in its channel
    ("SOLAR_HUB_PIN_R", "SOLAR_HUB_BRACKET_R"), ("SOLAR_HUB_PIN_L", "SOLAR_HUB_BRACKET_L"),  # revolute joint
    ("KEEPOUT_SOLAR_CABLE_RUN_R", "SOLAR_HUB_BRACKET_R"), ("KEEPOUT_SOLAR_CABLE_RUN_L", "SOLAR_HUB_BRACKET_L"),  # cable enters the bracket
    ("KEEPOUT_SOLAR_CABLE_RUN_R", "KEEPOUT_SOLAR_LOOP_R"), ("KEEPOUT_SOLAR_CABLE_RUN_L", "KEEPOUT_SOLAR_LOOP_L"),  # own service loop
    ("KEEPOUT_SOLAR_CABLE_RUN_R", "SOLAR_CASSETTE_R"), ("KEEPOUT_SOLAR_CABLE_RUN_L", "SOLAR_CASSETTE_L"),
    ("KEEPOUT_SOLAR_CABLE_RUN_R", "SOLAR_CARRIAGE_R"), ("KEEPOUT_SOLAR_CABLE_RUN_L", "SOLAR_CARRIAGE_L"),  # carriage encloses pin + cable (B.1)
    ("KEEPOUT_SOLAR_CABLE_RUN_R", "SOLAR_HUB_PIN_R"), ("KEEPOUT_SOLAR_CABLE_RUN_L", "SOLAR_HUB_PIN_L"),
)}
# Guided fits: the hub bracket runs in its rail slot with the CLEARANCE fit B.1 sized the slot for (17.6 = 17 + 2 x 0.3).
# F3 (resolved, option B): the bracket must also clear the channel floor by MIN_GAP over the whole travel (checked in main).
GUIDED = {frozenset(("SOLAR_HUB_BRACKET_R", "SOLAR_RAIL_R")): P["CLEARANCE"],
          frozenset(("SOLAR_HUB_BRACKET_L", "SOLAR_RAIL_L")): P["CLEARANCE"]}
# D-009 index lock: designed running fits between the sliding / tilting groups (their own minima, not MIN_GAP).
for _s in "RL":
    GUIDED.update({
        frozenset((f"SOLAR_INDEX_PLATE_{_s}", f"SOLAR_RAIL_{_s}")): P["CLEARANCE"],           # rides the rail slot like the bracket
        frozenset((f"SOLAR_ANTIROT_PLATE_{_s}", f"SOLAR_RAIL_{_s}")): P["CLEARANCE"],         # inside the carriage, open to its -Y face
        frozenset((f"SOLAR_INDEX_PIN_{_s}", f"SOLAR_INDEX_PLATE_{_s}")): (P["SOLAR_INDEX_HOLE_DIAMETER"] - P["SOLAR_INDEX_PIN_DIAMETER"]) / 2,
        frozenset((f"SOLAR_INDEX_PLATE_{_s}", f"SOLAR_CASSETTE_{_s}")): P["SOLAR_INDEX_GROOVE_RADIAL_CLEARANCE"],
        frozenset((f"SOLAR_INDEX_PLATE_{_s}", f"SOLAR_HUB_BRACKET_{_s}")): P["SOLAR_INDEX_GROOVE_CLEARANCE"],
        frozenset((f"SOLAR_INDEX_PLATE_{_s}", f"SOLAR_INDEX_SLEEVE_{_s}")): P["SOLAR_INDEX_GROOVE_CLEARANCE"],
    })


def groups(parts):
    return {n: g for n, _, g, _, _, _ in parts}


def moving_pairs_check(pr, grp, names=None, fast=False):
    """Violations between parts of different rigid groups (MIN_GAP), joints (>= 0), keep-outs (>= 0), guided fits
    (>= CLEARANCE). Returns (violations, guided-fit clearances, all minima)."""
    viol, known, mins = [], [], {}
    ns = sorted(pr if names is None else names)
    for i, a in enumerate(ns):
        for b in ns[i + 1:]:
            if grp[a] == grp[b]:
                continue
            key = frozenset((a, b))
            need = 0.0 if (key in JOINTS or a.startswith("KEEPOUT") or b.startswith("KEEPOUT")) else MIN_GAP
            if key in GUIDED:
                need = GUIDED[key]
            c = clear(pr[a], pr[b], None if (not fast or key in GUIDED) else need + 1e-6)
            mins[key] = c
            if key in GUIDED:
                known.append((a, b, round(c, 3)))
            if c < need - EPS:
                viol.append((a, b, round(c, 3)))
    return viol, known, mins


def lid_vs_base(pr, grp, base, lid_ang_names=None, fast=False):
    """Lid-side parts (all groups except baseHinge) vs base parts; plug zones reported separately."""
    viol, plug = [], []
    hard = {n: v for n, (c, v) in base.items() if c in ("S", "E")}
    plugs = {n: v for n, (c, v) in base.items() if c == "X"}
    for a, pa in pr.items():
        if grp[a] == "baseHinge":
            continue
        for b, pb in list(hard.items()) + [(n, pr[n]) for n in pr if grp[n] == "baseHinge"]:
            need = 0.0 if a.startswith("KEEPOUT") else MIN_GAP
            c = clear(pa, pb, need + 1e-6 if fast else None)
            if c < need - EPS:
                viol.append((a, b, round(c, 3)))
        if not a.startswith("KEEPOUT"):
            for b, pb in plugs.items():
                plug.append((a, b, clear(pa, pb, min((c for _, _, c in plug), default=None) if fast else None)))
    return viol, plug


def zmin(pr, names):
    return min(_zmin(poly) for n in names for _, _, poly in pr[n])


def rigid_group_checks(parts, pr0):
    """Inside each rigid group, structure must not overlap (touching allowed); keep-outs must not overlap structure."""
    grp = groups(parts)
    bad = []
    ns = sorted(pr0)
    for i, a in enumerate(ns):
        for b in ns[i + 1:]:
            if grp[a] != grp[b]:
                continue
            if a.startswith("KEEPOUT") and b.startswith("KEEPOUT"):
                continue
            c = clear(pr0[a], pr0[b], 0.0)
            if c < -EPS and frozenset((a, b)) not in JOINTS:
                bad.append((a, b, round(c, 3)))
    return bad


def consistency_with_b1(env):
    """The E2 solar geometry must equal the validated B.1 V1 + fixes model (lid frame offset by ZD0), except the one
    intentional F3 deviation (Round E, option B): hub axis, hub bracket and side-wall notch bottom sit higher by the
    F3 budget (rail floor + MIN_GAP + bracket wall + pin radius instead of the rail mid-height)."""
    c = sv.config(fix=True)
    z = env["ZD0"]
    f3_hub = c["rz0"] + env["WALL_THICKNESS"] + MIN_GAP + env["SOLAR_BRACKET_WALL"] + env["SOLAR_HUB_PIN_DIAMETER"] / 2
    f3_raise = f3_hub - c["hub"][1][1]
    checks = [
        ("rail width", env["SOLAR_RAIL_WIDTH"], c["rail_w"]), ("rail height", env["SOLAR_RAIL_LAYER_HEIGHT"], c["rail_h"]),
        ("carriage width", env["SOLAR_CARRIAGE_WIDTH"], c["cw"]), ("slot", env["SOLAR_RAIL_SLOT_WIDTH"], c["slot_w"]),
        ("bracket", env["SOLAR_BRACKET_WIDTH"], c["bracket_w"]), ("travel", env["SOLAR_SLIDE_TRAVEL"], c["S"]),
        ("link", env["SOLAR_HUB_LINK_LENGTH"], c["link"]), ("deploy clearance", env["SOLAR_DEPLOY_CLEARANCE"], c["deploy"]),
        ("corridor", env["SOLAR_CABLE_CORRIDOR"], c["corridor"]), ("rail centre R", env["RCR"], c["rc"][1]),
        ("rail centre L", env["RCL"], c["rc"][-1]), ("hub R y", env["HYR"], c["hub"][1][0]), ("hub L y", env["HYL"], c["hub"][-1][0]),
        ("hub z (B.1 + F3 raise)", env["HZ"] - z, c["hub"][1][1] + f3_raise), ("rail z0", env["ZR0"] - z, c["rz0"]), ("cassette z0", env["ZC0"] - z, c["cz0"]),
        ("cassette y0", env["CY0"], c["cy0"]),
    ]
    op = sv.openings(c, 1)
    notch_y0 = min(op[k][0] for k in "QPX")
    notch_y1 = max(op[k][1] for k in "QPX")
    notch_z0 = min(op[k][2] for k in "QPX")
    checks += [("notch y0", env["NR0"], notch_y0), ("notch y1", env["NR1"], notch_y1), ("notch z0 (B.1 + F3 raise)", env["NZ0"] - z, notch_z0 + f3_raise),
               ("slot y0", env["CY0"] - MIN_GAP, op["C"][0]), ("slot y1", env["CY1"] + MIN_GAP, op["C"][1]),
               ("slot z0", env["ZC0"] - MIN_GAP - z, op["C"][2])]
    lp = sv.loops(c)
    checks += [("loop R x0", env["LPX0"], lp["LR"][0]), ("loop R x1", env["LPX1"], lp["LR"][1]),
               ("loop R y0", env["LRY0"], min(y for y, _ in lp["LR"][2])), ("loop L y1", env["LLY1"], max(y for y, _ in lp["LL"][2]))]
    checks += [("lid thickness", env["ZS1"] - env["ZF"], P["LID_THICKNESS"]),
               ("deployed span", 2 * (env["XI"] + env["SOLAR_SLIDE_TRAVEL"] + env["SOLAR_CASSETTE_WIDTH"]), 612.0)]
    return [(n, a, b) for n, a, b in checks if abs(a - b) > 1e-6], checks, f3_raise


def f3_budget(env):
    """F3 vertical budget (Round E, option B). Returns (failures, report string)."""
    floor_top = env["ZR0"] + env["WALL_THICKNESS"]
    pin_bot = env["HZ"] - env["SOLAR_HUB_PIN_DIAMETER"] / 2
    pin_top = env["HZ"] + env["SOLAR_HUB_PIN_DIAMETER"] / 2
    items = [("bracket bottom above the rail floor", env["BZ0"] - floor_top, MIN_GAP),
             ("carriage boss wall above the pin", env["ZR1"] - pin_top, P["MIN_WALL"]),
             ("carriage wall below the pin", pin_bot - floor_top, P["MIN_WALL"]),
             ("pin top below the other stowed cassette", env["ZC0"] - pin_top, MIN_GAP)]
    fails = [(n, v, need) for n, v, need in items if v < need - EPS]
    return fails, "; ".join(f"{n} {v:g} (>= {need:g})" for n, v, need in items)


def bracket_floor_sweep(parts, pr0, env):
    """Hub bracket vs its own rail floor over the whole travel, 0.1 mm steps (rigid in the lid frame)."""
    worst = math.inf
    for s, sign in (("R", 1), ("L", -1)):
        adds = next(a for n, _, _, _, a, _ in parts if n == f"SOLAR_RAIL_{s}")
        floor = to_prisms([p for p in adds if p[1] == "floor"], [])
        b = pr0[f"SOLAR_HUB_BRACKET_{s}"]
        for i in range(0, int(round(env["SOLAR_SLIDE_TRAVEL"] * 10)) + 1):
            dx = sign * i / 10
            worst = min(worst, clear([(x0 + dx, x1 + dx, poly) for x0, x1, poly in b], floor))
    return worst


# ------------------------------------------------------------------ D-009 index lock checks
def _shift_prims(prims, dx, keep_x0=False, keep_x1=False):
    """Shift evaluated primitives along X; keep_x0 / keep_x1 pin one end (used to shorten the spring envelope)."""
    out = []
    for kind, label, v in prims:
        v = list(v)
        ix = (0, 3) if kind == "box" else ((3, 4) if kind == "cylx" else (0, 1))
        if not keep_x0:
            v[ix[0]] += dx
        if not keep_x1:
            v[ix[1]] += dx
        out.append((kind, label, v))
    return out


def retracted(parts, env, sides=("R", "L")):
    """Parts with the index pin retracted by SOLAR_INDEX_PIN_STROKE (pin and slider move outboard, the spring
    envelope shortens against its fixed seat)."""
    st = env["SOLAR_INDEX_PIN_STROKE"]
    out = []
    for n, d, g, k, a, s in parts:
        sd = n[-1]
        sign = 1 if sd == "R" else -1
        if sd in sides and n in (f"SOLAR_INDEX_PIN_{sd}", f"SOLAR_INDEX_SLIDER_{sd}"):
            a, s = _shift_prims(a, sign * st), _shift_prims(s, sign * st)
        elif sd in sides and n == f"SOLAR_INDEX_SPRING_{sd}":
            a = _shift_prims(a, sign * st, keep_x1=(sign > 0), keep_x0=(sign < 0))
        out.append((n, d, g, k, a, s))
    return out


def _axis_rot(prisms, axis, deg):
    return [(x0, x1, _rot(poly, axis, deg)) for x0, x1, poly in prisms]


def _sx(prs, dx):
    return [(x0 + dx, x1 + dx, poly) for x0, x1, poly in prs]


def lock_checks(parts, env, grp, pr0):
    """Checks A-G of the D-009 validation (modeled). Returns (failures, report lines)."""
    fails, rep = [], []
    step, n = env["SOLAR_INDEX_STEP"], int(round(env["SOLAR_INDEX_POSITIONS"]))
    tilts = [(k - (n - 1) / 2) * step for k in range(n)]
    side_names = {s: [nm for nm, *_ in parts if nm.endswith("_" + s) and grp[nm] in ("car" + s, "cas" + s)] for s in "RL"}
    others = [nm for nm, *_ in parts if grp[nm] in ("lid", "baseHinge")]

    # A. index positions: engaged pin concentric in each hole (running fit), positive lock between holes
    hole = (env["SOLAR_INDEX_HOLE_DIAMETER"] - env["SOLAR_INDEX_PIN_DIAMETER"]) / 2
    seat, between = [], []
    for s in "RL":
        for t_ in tilts:
            tt = (t_, 0.0) if s == "R" else (0.0, t_)
            pr = pose(parts, env, 105.0, (1, 1), tt)
            seat.append(clear(pr[f"SOLAR_INDEX_PIN_{s}"], pr[f"SOLAR_INDEX_PLATE_{s}"]))
            v, _, _ = moving_pairs_check(pr, grp, side_names[s] + others, fast=True)
            if v:
                fails.append(f"index position {s} {t_:+g}: {v[:3]}")
            tb = t_ + step / 2
            if tb < max(tilts):
                tt = (tb, 0.0) if s == "R" else (0.0, tb)
                pr = pose(parts, env, 105.0, (1, 1), tt)
                between.append(clear(pr[f"SOLAR_INDEX_PIN_{s}"], pr[f"SOLAR_INDEX_PLATE_{s}"]))
    full = env["IPX0"] < env["PX0"] and env["IPX1"] > env["PX1"] + env["SOLAR_INDEX_GROOVE_CLEARANCE"]
    ok = all(abs(c - hole) < 1e-6 for c in seat) and full and all(c < -1e-6 for c in between)
    rep.append(f"A index positions {', '.join(f'{x:+g}' for x in tilts)} (both sides, lid 105, deployed): pin-to-hole "
               f"{min(seat):.3f}..{max(seat):.3f} (design {hole:.3f}); pin spans the plate and both groove gaps: {full}; "
               f"engaged pin at every half-step overlaps the plate (positive lock, must be retracted to turn): "
               f"{all(c < 0 for c in between)}")
    if not ok:
        fails.append("index seating")

    # B. retracted: free rotation over the operating range, and what (if anything) stops it
    prt = retracted(parts, env)
    free, worst = [], math.inf
    for a10 in range(-900, 901, 25):
        a = a10 / 10
        pr = pose(prt, env, 105.0, (1, 1), (a, a))
        v, _, _ = moving_pairs_check(pr, grp, side_names["R"] + side_names["L"] + others, fast=True)
        worst = min(worst, clear(pr["SOLAR_INDEX_PIN_R"], pr["SOLAR_INDEX_PLATE_R"]))
        free.append((a, bool(v)))
    blocked = sorted(abs(a) for a, b in free if b)
    rng = env["SOLAR_INDEX_RANGE"]
    ok = not [a for a in blocked if a <= rng + 1e-9]
    rep.append(f"B retracted pin (stroke {env['SOLAR_INDEX_PIN_STROKE']:g}): tilt -90..+90 step 2.5, free of collisions "
               f"inside +-{rng:g}: {ok}; retracted pin-to-plate min {worst:.3f}; first blocked |tilt| "
               f"{blocked[0] if blocked else 'none up to 90'} -> no geometric hard stop "
               f"(SOLAR_TILT_STOP_ANGLE unresolved: +-80 stops NOT PACKAGED, see the implementation report)")
    if not ok:
        fails.append("retracted rotation")

    # C. stow interlock: slide inward from deployed at each index tilt; only 0 may enter
    inter = []
    for t_ in [0, 15, -15, 30, -30, 45, -45, 60, -60, 75, -75]:
        first = None
        for i in range(0, 401):
            e = 1 - i / 400
            pr = pose(parts, env, 105.0, (e, 1.0), (t_, 0.0))
            v, _, _ = moving_pairs_check(pr, grp, side_names["R"] + others, fast=True)
            if v:
                first = (1 - e) * env["SOLAR_SLIDE_TRAVEL"]
                break
        inter.append((t_, first))
    ok = inter[0][1] is None and all(f is not None for _, f in inter[1:])
    rep.append("C stow interlock (right cassette slid inward from deployed, lid 105; first MIN_GAP violation): " +
               ", ".join(f"{t_:+d}: {'enters fully' if f is None else f'blocked at {f:.1f} mm'}" for t_, f in inter))
    if not ok:
        fails.append("stow interlock")

    # D. slide sweep at 0 deg, 1 mm steps, lid 0 and 105
    bad = []
    for lid in (0.0, 105.0):
        for i in range(0, int(env["SOLAR_SLIDE_TRAVEL"]) + 1):
            e = i / env["SOLAR_SLIDE_TRAVEL"]
            pr = pose(parts, env, lid, (e, 0.0))
            v, _, _ = moving_pairs_check(pr, grp, side_names["R"] + others, fast=True)
            bad += [(lid, i) + x for x in v]
    rep.append(f"D slide sweep 0..{env['SOLAR_SLIDE_TRAVEL']:g} mm step 1, tilt 0, lid 0 and 105, right side vs lid: "
               f"{'no violations' if not bad else bad[:3]}")
    if bad:
        fails.append("slide sweep")

    # E. hub pin: no rotational play, axial capture, dowel engagement
    ax = (env["HYR"], env["HZ"])
    ar, pin, dw, car = pr0["SOLAR_ANTIROT_PLATE_R"], pr0["SOLAR_HUB_PIN_R"], pr0["SOLAR_ANTIROT_DOWEL_R"], pr0["SOLAR_CARRIAGE_R"]
    rot_pin = min(clear(_axis_rot(pin, ax, d), ar) for d in (0.05, -0.05))
    rot_pl = min(clear(_axis_rot(ar, ax, d), dw) for d in (0.05, -0.05))
    moving = ["SOLAR_ANTIROT_PLATE_R", "SOLAR_HUB_PIN_R", "SOLAR_HUB_SCREW_IN_R"]
    ax_out = [min(clear(_sx(pr0[g], dx), car) for g in moving) for dx in (0.1, 0.11, -0.01)]
    alone = [min(clear(_sx(pin, 0.05), ar), clear(_sx(pr0["SOLAR_HUB_SCREW_IN_R"], 0.05), ar)), clear(_sx(pin, -0.05), ar)]
    embed_in = env["ARX0"] - env["ADX0"]
    embed_out = env["ADX1"] - env["ARS1"]
    ok = rot_pin < 0 and rot_pl < 0 and abs(ax_out[0]) < 1e-9 and ax_out[1] < 0 and ax_out[2] < 0 and all(c < 0 for c in alone)
    rep.append(f"E hub pin: turn the pin 0.05 deg in the anti-rotation plate -> {rot_pin:.4f} (overlap: no free play); turn the "
               f"plate 0.05 deg about the pin -> vs dowel {rot_pl:.4f}; pin + plate + inboard screw axial float "
               f"+{env['SOLAR_LOCK_SLOT_CLEARANCE']:g}/-0 (+0.10: {ax_out[0]:.3f}, +0.11: {ax_out[1]:.3f}, -0.01: {ax_out[2]:.3f}); "
               f"pin vs the plate +0.05 (with its screw: washer) {alone[0]:.3f} / -0.05 (key shoulder) {alone[1]:.3f} (captured); dowel engagement "
               f"{embed_in:g} inboard / {embed_out:g} outboard of the plate")
    if not ok:
        fails.append("hub pin capture")

    # F. index plate: hole pattern, envelope, cable, rail floor over the travel
    plate = next(s_ for nm, _, _, _, _, s_ in parts if nm == "SOLAR_INDEX_PLATE_R")
    angs = sorted(math.degrees(math.atan2(v[1] - env["HZ"], v[0] - env["HYR"])) for k, lab, v in plate if lab.startswith("index_hole"))
    pitch = {round(b - a, 6) for a, b in zip(angs, angs[1:])}
    cab = clear(pr0["SOLAR_INDEX_PLATE_R"], pr0["KEEPOUT_SOLAR_CABLE_RUN_R"])
    floor = next(a for nm, _, _, _, a, _ in parts if nm == "SOLAR_RAIL_R")
    fl = to_prisms([q for q in floor if q[1] == "floor"], [])
    pf = min(clear(_sx(pr0["SOLAR_INDEX_PLATE_R"], i / 2), fl) for i in range(0, int(2 * env["SOLAR_SLIDE_TRAVEL"]) + 1))
    ok = len(angs) == n and pitch == {round(step, 6)} and pf >= MIN_GAP - EPS
    rep.append(f"F index plate: {len(angs)} holes at {angs[0]:.1f}..{angs[-1]:.1f} deg (lid frame, 0 deg tilt), pitch "
               f"{sorted(pitch)} deg; plate to the cable run {cab:.2f}; plate to its rail floor over the travel {pf:.3f}")
    if not ok:
        fails.append("index plate")

    # G. counter sleeve: wall, capture shoulder, clear of the hub pin and of the cable pass-through in the bracket
    wall = (env["SOLAR_INDEX_SLEEVE_OD"] - env["SOLAR_INDEX_HOLE_DIAMETER"]) / 2
    cy0, cy1 = env["HYR"] + env["CRO"] - env["CD2"], env["HYR"] + env["CRO"] + env["CD2"]
    thru = [(env["XI"], env["GX0"], hm.rect(cy0, cy1, env["HZ"] - env["CD2"], env["HZ"] + env["CD2"]))]
    sp = math.inf
    for t_ in tilts:
        pr = pose(parts, env, 0.0, (0.0, 0.0), (t_, 0.0))
        sp = min(sp, clear(pr["SOLAR_INDEX_SLEEVE_R"], pr0["SOLAR_HUB_PIN_R"]))
    sc = clear(pr0["SOLAR_INDEX_SLEEVE_R"], thru)      # the in-bracket cable pass-through turns with the cassette
    ok = wall > 0.3 and sp >= MIN_GAP and sc >= MIN_GAP
    rep.append(f"G counter sleeve: wall {wall:.2f}, seated on a {wall:.2f} shoulder (grit-relief bore); to the hub pin >= {sp:.2f}; "
               f"to the cable pass-through inside the bracket (same frame) {sc:.2f}")
    if not ok:
        fails.append("sleeve")
    return fails, rep


# ------------------------------------------------------------------ FeatureScript emission
def _fs(e):
    e = str(e).strip()
    if re.fullmatch(r"-?0", e):
        return "0 * millimeter"
    names = {n for n, _ in DERIVED + DERIVED_LOCK}
    return re.sub(r"\b([A-Z][A-Z0-9_]*)\b", lambda m: "degree" if m.group(1) == "DEG" else
                  (f"LE_{m.group(1)}" if m.group(1) in names else m.group(1)), e)


def _edges_fs(edges):
    return "[" + ", ".join(f'["{e[0]}", ' + ", ".join(_fs(x) for x in e[1:]) + "]" for e in edges) + "]"


def _prim_fs(p, loops=None):
    kind, label, c = p
    if kind == "prof":
        edges = (loops or {}).get(c[2]) or _edges_fs(c[2])
        return f'["prof", "{label}", {_fs(c[0])}, {_fs(c[1])}, {edges}]'
    return f'["{kind}", "{label}", ' + ", ".join(_fs(x) for x in c) + "]"


def emit_layout():
    lines = [BEGIN,
             "// Generated from CAD/tools/e_lid_layout.py (Round E, stage E2 lid). DO NOT EDIT.",
             f"// Class A lid, {PROV}. Solar = B.1 V1 + fixes. Hinge = representative. WORLD frame, lid closed, stowed."]
    for name, expr in DERIVED:
        lines.append(f"export const LE_{name} = {_fs(expr)};")
    lines.append("// D-009 solar index lock + hub-pin anti-rotation; values relative to the hub axis (dy toward the cable side)")
    for name, expr in DERIVED_LOCK:
        lines.append(f"export const LE_{name} = {_fs(expr)};")
    count = {}
    for _, _, _, _, adds, subs in PARTS:
        for kind, _, c in adds + subs:
            if kind == "prof":
                count[c[2]] = count.get(c[2], 0) + 1
    loops = {}
    for edges, k in count.items():
        if k > 1:
            loops[edges] = f"LE_LOOP{len(loops)}"
            lines.append(f"export const {loops[edges]} = {_edges_fs(edges)};")
    lines.append('// [name, displayed name, group, appearance, [adds], [subs]]; prims ["box", label, x0, y0, z0, x1, y1, z1] |')
    lines.append('// ["cylx", label, cy, cz, d, x0, x1] (cylinder along X) | ["prof", label, x0, x1, [edges]] (Y-Z loop extruded')
    lines.append('// along X; edges ["L", y0, z0, y1, z1] | ["A", cy, cz, r, a0, a1] = arc counter-clockwise from a0 to a1)')
    lines.append("export function nomadELidParts() returns array")
    lines.append("{")
    lines.append("    return [")
    for i, (name, disp, g, key, adds, subs) in enumerate(PARTS):
        sep = "," if i < len(PARTS) - 1 else ""
        lines.append(f'        ["{name}", "{disp}", "{g}", "{key}", [')
        lines.append(",\n".join("            " + _prim_fs(p, loops) for p in adds))
        lines.append("        ], [" + ("" if not subs else ""))
        if subs:
            lines.append(",\n".join("            " + _prim_fs(p, loops) for p in subs))
        lines.append(f"        ]]{sep}")
    lines.append("    ];")
    lines.append("}")
    lines.append("export function nomadELidBasePockets() returns array")
    lines.append("{")
    lines.append("    return [\n" + ",\n".join("        " + _prim_fs(p) for p in BASE_POCKETS) + "\n    ];")
    lines.append("}")
    lines.append("// [name, owner part, [origin], [x axis], [z axis]]")
    lines.append("export function nomadELidConnectors() returns array")
    lines.append("{")
    rows = []
    for n, o, org, xa, za in CONNECTORS:
        rows.append(f'        ["{n}", "{o}", [{", ".join(_fs(x) for x in org)}], {list(xa)}, {list(za)}]')
    lines.append("    return [\n" + ",\n".join(rows) + "\n    ];")
    lines.append("}")
    lines.append(END)
    return "\n".join(lines)


def emit_expected(parts, pr0, conns, base, poses):
    """Kernel cross-check data: near pairs (closed, stowed) and a few posed clearances."""
    names = [n for n, *_ in parts]
    bnames = ["BASE_SHELL", "ENV_KEYBOARD", "ENV_TRACKPAD", "KEEPOUT_PLUGS_MAIN", "KEEPOUT_PLUGS_AUX"]
    allp = {**pr0, **{b: base[b][1] for b in bnames}}
    order = names + bnames
    pairs = []
    for i, a in enumerate(order):
        for j in range(i + 1, len(order)):
            b = order[j]
            if a in bnames and b in bnames:
                continue
            c = clear(allp[a], allp[b], NEAR)
            if c < NEAR:
                st = "O" if c < -EPS else ("T" if c < EPS else "G")
                pairs.append((i, j, st, round(max(c, 0.0), 4) if st != "O" else -1))
    lines = [HBEGIN, "// Generated by CAD/tools/e_lid_layout.py --write. DO NOT EDIT.",
             "const LE_NAMES = [" + ", ".join(f'"{n}"' for n in order) + "];",
             "// near pairs (closed, stowed): [i, j, state O/T/G, gap or -1]",
             "const LE_PAIRS = ["]
    chunks = [f"[{i}, {j}, \"{s}\", {g:g}]" for i, j, s, g in pairs]
    for k in range(0, len(chunks), 6):
        lines.append("    " + ", ".join(chunks[k:k + 6]) + ("," if k + 6 < len(chunks) else ""))
    lines.append("];")
    lines.append("// connectors: [name, x, y, z]")
    lines.append("const LE_CONNECTORS = [" + ", ".join(f'["{n}", {o[0]:g}, {o[1]:g}, {o[2]:g}]' for n, _, o, _, _ in conns) + "];")
    lines.append("// posed checks: [lid deg, extR, extL, tiltR, tiltL, part A, part B, signed clearance]")
    lines.append("const LE_POSES = [")
    lines.append(",\n".join(f'    [{p[0]:g}, {p[1]:g}, {p[2]:g}, {p[3]:g}, {p[4]:g}, "{a}", "{b}", {c:.4f}]' for p, a, b, c in poses))
    lines.append("];")
    lines.append(HEND)
    return "\n".join(lines), len(pairs)


def splice(text, begin, end, block, path):
    i, j = text.find(begin), text.find(end)
    if i < 0 or j < 0:
        raise ValueError(f"{path.name}: markers {begin!r} / {end!r} not found")
    return text[:i] + block + text[j + len(end):]


# ------------------------------------------------------------------ main
def main(argv):
    env, parts, pockets, conns = evaluate()
    grp = groups(parts)
    base = base_prisms(pockets)
    fails = []

    diff, all_checks, f3_raise = consistency_with_b1(env)
    print(f"E2 lid layout: {len(parts)} parts, {len(conns)} mate connectors; lid T {env['ZS1'] - env['ZF']:.1f} "
          f"(face Z {env['ZF']:g} .. back Z {env['ZS1']:g}), {PROV}")
    print(f"  stack (world Z): lip {env['ZF']:g}-{env['ZD0']:g} | display {env['ZD0']:g}-{env['ZD1']:g} | rail layer {env['ZR0']:g}-{env['ZR1']:g} | "
          f"cassette {env['ZC0']:g}-{env['ZC1']:g} | shell {env['ZS0']:g}-{env['ZS1']:g}")
    print(f"  B.1 V1 + fixes consistency: {len(all_checks) - len(diff)}/{len(all_checks)} values equal" + (f"; MISMATCH {diff}" if diff else "")
          + f" (hub axis / bracket / notch bottom intentionally +{f3_raise:g} above B.1: F3 option B)")
    if diff:
        fails.append("B.1 mismatch")
    bfails, brep = f3_budget(env)
    print(f"  F3 vertical budget: {brep}" + (f"; FAIL {bfails}" if bfails else "; ok"))
    if bfails:
        fails.append("F3 budget")

    pr0 = pose(parts, env)
    rb = rigid_group_checks(parts, pr0)
    print(f"  rigid groups (structure must not overlap): {rb or 'ok'}")
    if rb:
        fails.append("rigid overlap")

    # ---------------- pose matrix
    lids = [0.0, 105.0, 120.0, 135.0]
    exts = {"stowed": (0, 0), "R deployed": (1, 0), "L deployed": (0, 1), "both deployed": (1, 1)}
    tilts = [0, 15, -15, 30, -30, 45, -45, 60, -60, 75, -75]
    summary, unexpected, known_b1 = {}, set(), set()
    solar = [n for n in pr0 if grp[n] not in ("lid", "baseHinge")]
    for lid in lids:
        for label, e in exts.items():
            pr = pose(parts, env, lid, e)
            v, k, _ = moving_pairs_check(pr, grp, fast=True)
            unexpected |= {(lid, label, 0) + x for x in v}
            known_b1 |= {(x[0], x[1], x[2]) for x in k}
        for t in tilts:
            for tt in ((t, t), (t, -t)):
                pr = pose(parts, env, lid, (1, 1), tt)
                v, k, _ = moving_pairs_check(pr, grp, fast=True)
                unexpected |= {(lid, "both deployed", tt) + x for x in v}
                known_b1 |= {(x[0], x[1], x[2]) for x in k}
                summary[(lid, tt)] = zmin(pr, [n for n in solar if not n.startswith("KEEPOUT")])
    # slides (each side 0..1, other side stowed or deployed), lid 105
    for side in (0, 1):
        for other in (0, 1):
            for i in range(21):
                e = [0.0, 0.0]
                e[side] = i / 20
                e[1 - side] = other
                pr = pose(parts, env, 105.0, tuple(e))
                v, k, _ = moving_pairs_check(pr, grp, fast=True)
                unexpected |= {(105.0, f"slide {e}", 0) + x for x in v}
                known_b1 |= {(x[0], x[1], x[2]) for x in k}
    print(f"\n  moving-part checks (lid 0/105/120/135 x stowed / R / L / both; tilts +-75 step 15 both deployed; slides 0..1): "
          f"{len(unexpected)} unexpected violations")
    for u in sorted(unexpected, key=str)[:12]:
        print(f"    UNEXPECTED {u}")
    if unexpected:
        fails.append("moving-part violations")
    fits = {}
    for a, b, c in known_b1:
        k = " / ".join(sorted(x[:-2] for x in (a, b)))
        fits[k] = min(fits.get(k, math.inf), c)
    need = {" / ".join(sorted(x[:-2] for x in key)): v for key, v in GUIDED.items()}
    print("  guided / running fits (min over all poses; need): " + "; ".join(f"{k} {v:.3f} ({need[k]:g})" for k, v in sorted(fits.items())))
    bf = bracket_floor_sweep(parts, pr0, env)
    print(f"  F3: hub bracket vs rail floor over the full {env['SOLAR_SLIDE_TRAVEL']:g} mm travel (0.1 mm steps): min {bf:.3f} mm "
          f"(needs >= MIN_GAP {MIN_GAP:g})")
    if bf < MIN_GAP - EPS:
        fails.append("F3 bracket-floor")
    lf, lrep = lock_checks(parts, env, grp, pr0)
    print("\n  D-009 index lock (modeled):")
    for line in lrep:
        print("    " + line)
    fails += lf

    # ---------------- lid vs base (sweep) and the known rear-plug conflict
    sweep = {}
    worst_base, plug_at = (math.inf, None), {}
    for a10 in range(0, 1351, 10):
        lid = a10 / 10
        pr = pose(parts, env, lid)
        v, plug = lid_vs_base(pr, grp, base, fast=True)
        if v:
            unexpected |= {(lid, "lid-base") + x for x in v}
        wb = math.inf
        for a in pr:
            if grp[a] != "baseHinge" and not a.startswith("KEEPOUT"):
                wb = min(wb, clear(pr[a], base["BASE_SHELL"][1], wb))
        worst_base = min(worst_base, (wb, lid))
        plug_at[lid] = min(c for _, _, c in plug)
        sweep[lid] = v
    lvb = [(k, v) for k, v in sweep.items() if v]
    print(f"\n  lid sweep 0..135 (step 1): lid-side parts vs base parts / base hinge halves: "
          f"{'no violations' if not lvb else f'{sum(len(v) for _, v in lvb)} violations, e.g. {lvb[0]}'}; "
          f"min lid-frame/shell/display/solar to BASE_SHELL {worst_base[0]:.3f} at {worst_base[1]:g} deg")
    print(f"  rear-plug keep-outs (known OPEN CONFLICT, left visible): clearance at 105 {plug_at[105.0]:.3f}, 120 {plug_at[120.0]:.3f}, "
          f"135 {plug_at[135.0]:.3f}; first below MIN_GAP at {min((a for a, c in plug_at.items() if c < MIN_GAP - EPS), default='none')} deg")
    if lvb:
        fails.append("lid-base violations")

    # ---------------- ground (table) with deployed tilts
    print("\n  deployed-cassette lowest point above the table (Z, both deployed; tilt R/L):")
    for lid in lids:
        row = [f"{tt[0]:+d}/{tt[1]:+d}:{summary[(lid, tt)]:.0f}" for tt in [(0, 0), (30, 30), (-30, -30), (45, 45), (-45, -45),
                                                                              (75, 75), (-75, -75), (75, -75)]]
        print(f"    lid {lid:5.1f}: " + "  ".join(row))

    # ---------------- key clearances (closed, stowed and deployed)
    pr = pr0
    prd = pose(parts, env, 105.0, (1, 1))
    key = [("DISPLAY", "SOLAR_RAIL_R", pr), ("DISPLAY", "SOLAR_CASSETTE_R", pr), ("SOLAR_CASSETTE_R", "SOLAR_RAIL_R", pr),
           ("SOLAR_CASSETTE_R", "LID_REAR_SHELL", pr), ("SOLAR_CASSETTE_R", "SOLAR_CASSETTE_L", pr),
           ("SOLAR_CASSETTE_R", "LID_FRAME", pr), ("SOLAR_CARRIAGE_R", "LID_FRAME", prd), ("SOLAR_CASSETTE_R", "LID_FRAME", prd),
           ("SOLAR_HUB_BRACKET_R", "LID_FRAME", prd), ("KEEPOUT_SOLAR_CABLE_RUN_R", "LID_FRAME", prd),
           ("SOLAR_CASSETTE_R", "KEEPOUT_SOLAR_LOOP_R", pr), ("SOLAR_CARRIAGE_R", "KEEPOUT_SOLAR_CORRIDOR", pr),
           ("SOLAR_CARRIAGE_L", "KEEPOUT_SOLAR_CORRIDOR", pr), ("HINGE_LID_HALF_R", "HINGE_BASE_HALF_R", pr),
           ("KEEPOUT_CONTROLLER_BAND_R", "KEEPOUT_SOLAR_LOOP_R", pr), ("KEEPOUT_DISPLAY_FLEX", "KEEPOUT_SOLAR_LOOP_R", pr)]
    print("\n  key clearances (modeled): " + "; ".join(f"{a} x {b} {'deployed' if p is prd else 'stowed'} {clear(p[a], p[b]):.2f}" for a, b, p in key))
    print(f"  deployed span (cassette outer edges) {2 * (env['XI'] + env['SOLAR_SLIDE_TRAVEL'] + env['SOLAR_CASSETTE_WIDTH']):g} mm; "
          f"closed NOMAD {env['ZS1']:g} mm")

    # ---------------- expected block for the kernel cross-check
    poses = []
    for p in ((105.0, 1, 1, 0, 0), (135.0, 0, 0, 0, 0), (105.0, 1, 1, 75, -75)):
        prp = pose(parts, env, p[0], (p[1], p[2]), (p[3], p[4]))
        for a, b in (("SOLAR_CASSETTE_R", "BASE_SHELL"), ("SOLAR_CASSETTE_L", "LID_FRAME"), ("LID_REAR_SHELL", "KEEPOUT_PLUGS_MAIN"),
                     ("SOLAR_CARRIAGE_R", "LID_FRAME"), ("HINGE_LID_HALF_R", "HINGE_BASE_HALF_R")):
            pa = prp[a] if a in prp else base[a][1]
            pb = prp[b] if b in prp else base[b][1]
            poses.append((p, a, b, clear(pa, pb)))
    for p in ((105.0, 1, 1, 0, 0), (105.0, 1, 1, 75, -75), (105.0, 1, 1, -30, 45)):       # D-009: tilted index positions
        prp = pose(parts, env, p[0], (p[1], p[2]), (p[3], p[4]))
        for a, b in (("SOLAR_INDEX_PIN_R", "SOLAR_INDEX_PLATE_R"), ("SOLAR_INDEX_PIN_L", "SOLAR_INDEX_PLATE_L"),
                     ("SOLAR_INDEX_PLATE_R", "SOLAR_CASSETTE_R"), ("SOLAR_INDEX_PLATE_L", "SOLAR_HUB_BRACKET_L")):
            poses.append((p, a, b, clear(prp[a], prp[b])))
    expected, npairs = emit_expected(parts, pr0, conns, base, poses)
    layout = emit_layout()
    status = 0 if not fails else 1
    if "--write" in argv or "--check" in argv:
        fs_text, h_text = FS_PATH.read_text(encoding="utf-8"), HARNESS_PATH.read_text(encoding="utf-8")
        fs_new, h_new = splice(fs_text, BEGIN, END, layout, FS_PATH), splice(h_text, HBEGIN, HEND, expected, HARNESS_PATH)
        for path, old, new in ((FS_PATH, fs_text, fs_new), (HARNESS_PATH, h_text, h_new)):
            if new != old:
                if "--write" in argv:
                    path.write_text(new, encoding="utf-8", newline="\n")
                    print(f"wrote {path.relative_to(ROOT)}")
                else:
                    print(f"{path.name}: generated block OUT OF DATE")
                    status = 1
    print(f"\n  kernel cross-check data: {npairs} near pairs, {len(poses)} posed clearances")
    print("\nALL CHECKS PASSED (known: rear-plug OPEN CONFLICT; F3 resolved by option B; D-009 +-80 hard stops NOT "
          "PACKAGED - open)" if not fails else f"\nFAILED: {fails}")
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
