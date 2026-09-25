"""P0.1 test coupons A (solar rail cantilever) and B (rear-shell span): model predictions.

Screening beam formulas only (same basis as lid_structure_screening.py), used to state what the
physical coupons are EXPECTED to show so measurements can calibrate the model. Not FEA.

Usage:  py CAD/tools/coupon_expectations.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lid_structure_screening as ls  # noqa: E402

C = ls.C
E = ls.E_PETG
G = 9.81

# ---------------- Coupon A: rail cantilever ----------------
RAIL_LEN = C["S"] + ls.sk.L                      # 198: full V1-fix rail
PAD_LEN = ls.XW - ls.MIN_GAP - (ls.sk.DISP_W / 2 + ls.MIN_GAP)   # 28.5 pad under the rail
ARM = ls.rail_cantilever()[1]                    # pad inboard edge -> stowed carriage centre
CARRIAGE_G = 12.0                                # printed carriage + post, approx (weigh the real one)
A2_WALL = 4.1                                    # side wall thickened to host a strip slot
STRIPS = {"aluminium 10x2": (70000.0, 2.0, 10.0), "steel 10x1.5": (200000.0, 1.5, 10.0)}
STRIP_Z = 1.5 + 10.0 / 2                         # strip centroid height above rail underside


def section(pieces):
    a = sum(b * t for b, t, _ in pieces)
    yb = sum(b * t * y for b, t, y in pieces) / a
    return yb, sum(b * t ** 3 / 12 + b * t * (y - yb) ** 2 for b, t, y in pieces), a


def rail_pieces(wall):
    w, h, ch, slot, fl = C["cw"] + 2 * wall, C["rail_h"], C["ch"], C["slot_w"], ls.WALL
    return [(w, fl, fl / 2), (wall, ch, fl + ch / 2), (wall, ch, fl + ch / 2),
            ((w - slot) / 2, fl, h - fl / 2), ((w - slot) / 2, fl, h - fl / 2)]


def ei_a1():
    _, i, _ = section(rail_pieces(ls.WALL))
    return E * i


def ei_a2(strip=None):
    yb, i, a = section(rail_pieces(A2_WALL))
    if strip is None:
        return E * i
    es, t, h = STRIPS[strip]
    n = es / E                                    # transformed-section factor, two strips
    a_s = 2 * t * h * n
    ybar = (a * yb + a_s * STRIP_Z) / (a + a_s)
    i_tot = i + a * (yb - ybar) ** 2 + 2 * n * (t * h ** 3 / 12) + a_s * (STRIP_Z - ybar) ** 2
    return E * i_tot


def tip_defl(ei, mass_kg):
    return mass_kg * G * ARM ** 3 / (3 * ei)


# ---------------- Coupon B: rear-shell strip ----------------
SPAN = ls.SPAN                                   # 202 clear span between edge beams
STRIP_W = 3 * ls.RIB_S                           # 90: three rib pitches
BAND = C["cy0"] - ls.MIN_GAP - ls.WALL           # 14: edge-beam (shelf) band width


def b_defl(ei_per_mm, load_n):
    return load_n * SPAN ** 3 / (48 * E * ei_per_mm * STRIP_W)


def main():
    print(f"Coupon A: rail length {RAIL_LEN:g}, pad {PAD_LEN:g}, arm pad-edge -> carriage centre {ARM:.1f}, travel {C['S']:g}")
    loads = [0.0, 0.1, 0.2, 0.3, 0.6, 0.9]
    for name, ei in (("A1 printed rail", ei_a1()), ("A2 slotted, empty", ei_a2()),
                     *((f"A2 + 2x {k}", ei_a2(k)) for k in STRIPS)):
        row = "  ".join(f"{m:.1f}kg:{tip_defl(ei, m + CARRIAGE_G / 1000):.2f}" for m in loads)
        touch = 1.0 * 3 * ei / (G * ARM ** 3) - CARRIAGE_G / 1000
        print(f"  {name:<24} EI {ei / 1e6:6.1f} N*m^2e-3 | deflection at carriage (mm): {row} | touches 1.0 mm at {touch:.2f} kg added")
    print(f"\nCoupon B: clear span {SPAN:g}, strip width {STRIP_W:g}, support bands {BAND:g}")
    for label, iw in (("B1 plain 2.5", ls.i_ribbed(ls.WALL, 0)),
                      *((f"B2 ribs h={h:g}", ls.i_ribbed(ls.WALL, h)) for h in (6, 8, 11))):
        row = "  ".join(f"{n}N:{b_defl(iw, n):.2f}" for n in (2, 5, 10, 20))
        touch = 1.0 * 48 * E * iw * STRIP_W / SPAN ** 3
        print(f"  {label:<14} deflection at centre (mm): {row} | reaches 1.0 mm at {touch:.1f} N")


if __name__ == "__main__":
    main()
