"""Reference numbers for the Onshape coupon Feature Studio (NOMAD_P01_Coupons) cross-check.

Computes, from generate_coupons.py (the parametric master), each coupon's exact bounding box and exact
volume with TRUE round holes (the STL steps them at 0.1 mm), so the Onshape kernel result can be compared
tightly. Box CSG is evaluated exactly on the generator's box-coordinate grid; round holes are subtracted
analytically (each lies wholly inside solid material; the pad-stub counterbore/through-hole pair is handled
as one stepped hole).

Usage:  py CAD/coupons/P0.1/onshape_crosscheck.py        (prints the table and the FeatureScript literal)
"""

import math

import generate_coupons as g

ONSHAPE_NAMES = {
    "A1_rail_printed": "CPN_A1_rail",
    "A2_rail_stiffener_slots": "CPN_A2_rail_stiffener_slots",
    "A_pad_stub": "CPN_A_pad_stub",
    "A_carriage_load_post": "CPN_A_carriage_load_post",
    "A_load_platform": "CPN_A_load_platform",
    "A_display_surrogate": "CPN_A_display_surrogate",
    "B_frame_supports": "CPN_B_supports",
    "B_clearance_block": "CPN_B_clearance_block",
    "B1_plate_plain_2p5": "CPN_B1_plate",
    "B2_plate_ribbed_h06": "CPN_B2_h6_plate",
    "B2_plate_ribbed_h08": "CPN_B2_h8_plate",
    "B2_plate_ribbed_h11": "CPN_B2_h11_plate",
    "B_load_pad": "CPN_B_load_pad",
}


def box_volume(part):
    """Exact volume of (union of add boxes) minus (union of subtracted boxes), round subs ignored."""
    boxes = [a for k, a in part.adds + part.subs if k == "box"]
    axes = [sorted({b[i] for b in boxes} | {b[i + 3] for b in boxes}) for i in range(3)]
    adds = [a for k, a in part.adds if k == "box"]
    subs = [a for k, a in part.subs if k == "box"]

    def inb(b, p):
        return b[0] < p[0] < b[3] and b[1] < p[1] < b[4] and b[2] < p[2] < b[5]

    vol = 0.0
    for i in range(len(axes[0]) - 1):
        for j in range(len(axes[1]) - 1):
            for k in range(len(axes[2]) - 1):
                c = ((axes[0][i] + axes[0][i + 1]) / 2, (axes[1][j] + axes[1][j + 1]) / 2, (axes[2][k] + axes[2][k + 1]) / 2)
                if any(inb(b, c) for b in adds) and not any(inb(b, c) for b in subs):
                    vol += (axes[0][i + 1] - axes[0][i]) * (axes[1][j + 1] - axes[1][j]) * (axes[2][k + 1] - axes[2][k])
    return vol


def round_removed(name, rib_h=0.0):
    """Material removed by the round holes of each part (analytic, true circles)."""
    ins = math.pi * (g.INSERT_D / 2) ** 2 * g.INSERT_DEPTH
    if name.startswith(("A1_", "A2_")):
        return 2 * ins
    if name == "A_carriage_load_post":
        r = g.LOAD_HOLE_D / 2
        return (0.75 * math.pi + 1) * r * r * (g.SLOT_W - 2 * g.POST_CLR)   # teardrop = circle + 45-deg roof
    if name == "A_pad_stub":
        per = math.pi * (g.CBORE_D / 2) ** 2 * g.CBORE_DEPTH + math.pi * (g.SCREW_CLEAR_D / 2) ** 2 * (g.PAD_BASE[2] - g.CBORE_DEPTH)
        return 2 * per
    if name == "B_frame_supports":
        return 4 * ins
    if name.startswith(("B1_", "B2_")):
        return 4 * math.pi * (g.SCREW_CLEAR_D / 2) ** 2 * g.PLATE_T
    return 0.0


def table():
    rows = []
    for p in g.all_parts(g.RIB_HEIGHTS):
        b = p.bbox()
        size = tuple(round(b[i + 3] - b[i], 4) for i in range(3))
        vol = box_volume(p) - round_removed(p.name)
        rows.append((ONSHAPE_NAMES[p.name], size, vol))
    return rows


if __name__ == "__main__":
    rows = table()
    for n, s, v in rows:
        print(f"{n:<30} {s[0]:>7.2f} x {s[1]:>6.2f} x {s[2]:>6.2f}   vol {v:>12.4f} mm3")
    print("\nFeatureScript literal [name, sx, sy, sz, vol_mm3]:")
    print(",\n".join(f'["{n}", {s[0]:g}, {s[1]:g}, {s[2]:g}, {v:.3f}]' for n, s, v in rows))
