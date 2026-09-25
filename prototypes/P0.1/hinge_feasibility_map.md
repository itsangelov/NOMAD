# P0.1 Hinge-Axis Feasibility Map (Round A.2)

**Status: modeled, P0.1 working geometry. No hinge architecture has been chosen.** This map is input for the owner's decision. It does not recommend a point.

## Method

- **Geometry:**
  - base envelope 235 deep × 40 high (`BODY_DEPTH`, `BODY_HEIGHT`)
  - lid envelope 25 thick (`LID_THICKNESS`), resting 1.0 above the base when closed (`LID_CLOSED_GAP` = `MIN_GAP`)
  - all values are working inputs from `CAD/parameters/nomad.yaml`
- **Hinge axis:** parallel to X, at y = 235 − inset and z = 40 + height.
  - Inset is `HINGE_AXIS_OFFSET`; negative means behind the base rear face.
  - Height is `HINGE_AXIS_HEIGHT`, measured above the base top surface.
  - The closed lid spans heights 1 to 26.
- **Sweep:** lid rotated 0–135° in 5° steps (28 samples), as in A.1. A 0.1° sweep was also run as a sensitivity check.
- **Signed clearance:** the gap between the lid and base envelopes when they are separated; minus the penetration depth (separating-axis minimum translation) when they overlap.
- **Model:** `CAD/tools/hinge_feasibility_2d.py`. It is exact 2D in the side view: both envelopes span the same X range and the axis is parallel to X, so every clearance lies in the Y–Z plane.
- **Raw data:** `hinge_feasibility_map.csv`, one row per grid point.
- **Feasibility criterion:** minimum signed clearance ≥ 1.0 mm (the current requirement, `MIN_GAP`) and no ground contact.

## Validation

- The model reproduces the three A.1 Onshape points exactly: (0, 0), (8, 0) and (8, 13.5), including overhangs, heights, the 0.707 mm clearance and the 1.33 mm dip.
- One Onshape scratch run recomputed 11 grid points with the Onshape kernel: solid lid and base envelopes, `evCollision` and `evDistance`. Its output matched the model's prediction exactly, to 0.01 mm, including the angle of minimum and the count of overlapping samples:

  `-6/-4:1@0n0 -2/14:1@0n0 0/-2:1@0n0 0/0:0.71@135n0 0/2:1@0n0 0/26:1@0n0 2/26:0.92@5n0 4/10:0.15@25n0 6/12:0.13@10n9 6/14:0.16@10n5 10/26:0.22@5n6`

  Format: `inset/height : minimum gap over non-overlapping samples @ angle, n = overlapping samples`.

## Maps

### Minimum signed clearance over the full sweep 0–135° (mm). ✓ = meets ≥ 1.0 mm; negative = penetration depth

| height (axis z) \ inset (axis y) | -6 (241) | -4 (239) | -2 (237) | 0 (235) | 2 (233) | 4 (231) | 6 (229) | 8 (227) | 10 (225) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 26 (66) | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | +0.92 ✗ | +0.69 ✗ | +0.30 ✗ | -0.23 ✗ | -0.91 ✗ |
| 24 (64) | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | +0.91 ✗ | +0.66 ✗ | +0.23 ✗ | -0.35 ✗ | -1.07 ✗ |
| 22 (62) | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | +0.91 ✗ | +0.62 ✗ | +0.16 ✗ | -0.47 ✗ | -1.26 ✗ |
| 20 (60) | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | +0.90 ✗ | +0.59 ✗ | +0.09 ✗ | -0.60 ✗ | -1.45 ✗ |
| 18 (58) | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | +0.89 ✗ | +0.54 ✗ | -0.03 ✗ | -0.79 ✗ | -1.72 ✗ |
| 16 (56) | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | +0.88 ✗ | +0.48 ✗ | -0.15 ✗ | -0.99 ✗ | -2.02 ✗ |
| 14 (54) | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | +0.85 ✗ | +0.41 ✗ | -0.32 ✗ | -1.26 ✗ | -2.39 ✗ |
| 12 (52) | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | +0.82 ✗ | +0.29 ✗ | -1.76 ✗ | -3.56 ✗ | -4.97 ✗ |
| 10 (50) | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | +0.79 ✗ | +0.15 ✗ | -3.17 ✗ | -6.59 ✗ | -8.38 ✗ |
| 8 (48) | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | +0.72 ✗ | -1.17 ✗ | -4.59 ✗ | -8.00 ✗ | -11.41 ✗ |
| 6 (46) | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | +0.62 ✗ | -2.59 ✗ | -6.00 ✗ | -9.41 ✗ | -12.83 ✗ |
| 4 (44) | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | -0.59 ✗ | -4.00 ✗ | -7.41 ✗ | -10.83 ✗ | -14.24 ✗ |
| 2 (42) | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | -2.00 ✗ | -5.41 ✗ | -8.83 ✗ | -12.24 ✗ | -15.66 ✗ |
| 0 (40) | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | +0.71 ✗ | -2.71 ✗ | -6.12 ✗ | -9.54 ✗ | -12.95 ✗ | -16.36 ✗ |
| -2 (38) | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | -1.29 ✗ | -4.71 ✗ | -8.12 ✗ | -11.54 ✗ | -14.95 ✗ |
| -4 (36) | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | **+1.00 ✓** | +0.12 ✗ | -3.29 ✗ | -6.71 ✗ | -10.12 ✗ | -13.54 ✗ |

### Minimum signed clearance over the opening motion only, 5–135° (mm)

| height (axis z) \ inset (axis y) | -6 (241) | -4 (239) | -2 (237) | 0 (235) | 2 (233) | 4 (231) | 6 (229) | 8 (227) | 10 (225) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 26 (66) | **+1.62 ✓** | **+1.44 ✓** | **+1.27 ✓** | **+1.09 ✓** | +0.92 ✗ | +0.69 ✗ | +0.30 ✗ | -0.23 ✗ | -0.91 ✗ |
| 24 (64) | **+1.61 ✓** | **+1.44 ✓** | **+1.26 ✓** | **+1.09 ✓** | +0.91 ✗ | +0.66 ✗ | +0.23 ✗ | -0.35 ✗ | -1.07 ✗ |
| 22 (62) | **+1.60 ✓** | **+1.43 ✓** | **+1.25 ✓** | **+1.08 ✓** | +0.91 ✗ | +0.62 ✗ | +0.16 ✗ | -0.47 ✗ | -1.26 ✗ |
| 20 (60) | **+1.59 ✓** | **+1.42 ✓** | **+1.25 ✓** | **+1.07 ✓** | +0.90 ✗ | +0.59 ✗ | +0.09 ✗ | -0.60 ✗ | -1.45 ✗ |
| 18 (58) | **+1.59 ✓** | **+1.41 ✓** | **+1.24 ✓** | **+1.06 ✓** | +0.89 ✗ | +0.54 ✗ | -0.03 ✗ | -0.79 ✗ | -1.72 ✗ |
| 16 (56) | **+1.58 ✓** | **+1.41 ✓** | **+1.23 ✓** | **+1.06 ✓** | +0.88 ✗ | +0.48 ✗ | -0.15 ✗ | -0.99 ✗ | -2.02 ✗ |
| 14 (54) | **+1.57 ✓** | **+1.40 ✓** | **+1.22 ✓** | **+1.05 ✓** | +0.85 ✗ | +0.41 ✗ | -0.32 ✗ | -1.26 ✗ | -2.39 ✗ |
| 12 (52) | **+1.56 ✓** | **+1.39 ✓** | **+1.22 ✓** | **+1.04 ✓** | +0.82 ✗ | +0.29 ✗ | -1.76 ✗ | -3.56 ✗ | -4.97 ✗ |
| 10 (50) | **+1.56 ✓** | **+1.38 ✓** | **+1.21 ✓** | **+1.03 ✓** | +0.79 ✗ | +0.15 ✗ | -3.17 ✗ | -6.59 ✗ | -8.38 ✗ |
| 8 (48) | **+1.55 ✓** | **+1.38 ✓** | **+1.20 ✓** | **+1.03 ✓** | +0.72 ✗ | -1.17 ✗ | -4.59 ✗ | -8.00 ✗ | -11.41 ✗ |
| 6 (46) | **+1.54 ✓** | **+1.37 ✓** | **+1.19 ✓** | **+1.02 ✓** | +0.62 ✗ | -2.59 ✗ | -6.00 ✗ | -9.41 ✗ | -12.83 ✗ |
| 4 (44) | **+1.53 ✓** | **+1.36 ✓** | **+1.19 ✓** | **+1.01 ✓** | -0.59 ✗ | -4.00 ✗ | -7.41 ✗ | -10.83 ✗ | -14.24 ✗ |
| 2 (42) | **+1.53 ✓** | **+1.35 ✓** | **+1.18 ✓** | **+1.00 ✓** | -2.00 ✗ | -5.41 ✗ | -8.83 ✗ | -12.24 ✗ | -15.66 ✗ |
| 0 (40) | **+1.52 ✓** | **+1.35 ✓** | **+1.17 ✓** | +0.71 ✗ | -2.71 ✗ | -6.12 ✗ | -9.54 ✗ | -12.95 ✗ | -16.36 ✗ |
| -2 (38) | **+1.53 ✓** | **+1.36 ✓** | **+1.18 ✓** | **+1.01 ✓** | -1.29 ✗ | -4.71 ✗ | -8.12 ✗ | -11.54 ✗ | -14.95 ✗ |
| -4 (36) | **+1.54 ✓** | **+1.36 ✓** | **+1.19 ✓** | **+1.01 ✓** | +0.12 ✗ | -3.29 ✗ | -6.71 ✗ | -10.12 ✗ | -13.54 ✗ |

### Lid angle at which the full-sweep minimum occurs (deg)

| height (axis z) \ inset (axis y) | -6 (241) | -4 (239) | -2 (237) | 0 (235) | 2 (233) | 4 (231) | 6 (229) | 8 (227) | 10 (225) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 26 (66) | 0.0 | 0.0 | 0.0 | 0.0 | 5.0 | 10.0 | 15.0 | 20.0 | 20.0 |
| 24 (64) | 0.0 | 0.0 | 0.0 | 0.0 | 5.0 | 10.0 | 15.0 | 20.0 | 25.0 |
| 22 (62) | 0.0 | 0.0 | 0.0 | 0.0 | 5.0 | 10.0 | 15.0 | 20.0 | 25.0 |
| 20 (60) | 0.0 | 0.0 | 0.0 | 0.0 | 5.0 | 10.0 | 20.0 | 25.0 | 30.0 |
| 18 (58) | 0.0 | 0.0 | 0.0 | 0.0 | 5.0 | 15.0 | 20.0 | 25.0 | 30.0 |
| 16 (56) | 0.0 | 0.0 | 0.0 | 0.0 | 10.0 | 15.0 | 20.0 | 30.0 | 35.0 |
| 14 (54) | 0.0 | 0.0 | 0.0 | 0.0 | 10.0 | 15.0 | 25.0 | 30.0 | 40.0 |
| 12 (52) | 0.0 | 0.0 | 0.0 | 0.0 | 10.0 | 20.0 | 135.0 | 135.0 | 135.0 |
| 10 (50) | 0.0 | 0.0 | 0.0 | 0.0 | 15.0 | 25.0 | 135.0 | 135.0 | 135.0 |
| 8 (48) | 0.0 | 0.0 | 0.0 | 0.0 | 15.0 | 135.0 | 135.0 | 135.0 | 135.0 |
| 6 (46) | 0.0 | 0.0 | 0.0 | 0.0 | 20.0 | 135.0 | 135.0 | 135.0 | 135.0 |
| 4 (44) | 0.0 | 0.0 | 0.0 | 0.0 | 135.0 | 135.0 | 135.0 | 135.0 | 135.0 |
| 2 (42) | 0.0 | 0.0 | 0.0 | 0.0 | 135.0 | 135.0 | 135.0 | 135.0 | 135.0 |
| 0 (40) | 0.0 | 0.0 | 0.0 | 135.0 | 135.0 | 135.0 | 135.0 | 135.0 | 135.0 |
| -2 (38) | 0.0 | 0.0 | 0.0 | 0.0 | 135.0 | 135.0 | 135.0 | 135.0 | 135.0 |
| -4 (36) | 0.0 | 0.0 | 0.0 | 0.0 | 135.0 | 135.0 | 135.0 | 135.0 | 135.0 |

### Rear overhang behind the base at 105° (mm)

| height (axis z) \ inset (axis y) | -6 (241) | -4 (239) | -2 (237) | 0 (235) | 2 (233) | 4 (231) | 6 (229) | 8 (227) | 10 (225) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 26 (66) | 68.4 | 65.9 | 63.3 | 60.8 | 58.3 | 55.8 | 53.3 | 50.8 | 48.2 |
| 24 (64) | 70.3 | 67.8 | 65.3 | 62.8 | 60.2 | 57.7 | 55.2 | 52.7 | 50.2 |
| 22 (62) | 72.2 | 69.7 | 67.2 | 64.7 | 62.2 | 59.7 | 57.1 | 54.6 | 52.1 |
| 20 (60) | 74.2 | 71.7 | 69.1 | 66.6 | 64.1 | 61.6 | 59.1 | 56.5 | 54.0 |
| 18 (58) | 76.1 | 73.6 | 71.1 | 68.5 | 66.0 | 63.5 | 61.0 | 58.5 | 56.0 |
| 16 (56) | 78.0 | 75.5 | 73.0 | 70.5 | 68.0 | 65.4 | 62.9 | 60.4 | 57.9 |
| 14 (54) | 80.0 | 77.4 | 74.9 | 72.4 | 69.9 | 67.4 | 64.9 | 62.3 | 59.8 |
| 12 (52) | 81.9 | 79.4 | 76.9 | 74.3 | 71.8 | 69.3 | 66.8 | 64.3 | 61.8 |
| 10 (50) | 83.8 | 81.3 | 78.8 | 76.3 | 73.8 | 71.2 | 68.7 | 66.2 | 63.7 |
| 8 (48) | 85.8 | 83.2 | 80.7 | 78.2 | 75.7 | 73.2 | 70.7 | 68.1 | 65.6 |
| 6 (46) | 87.7 | 85.2 | 82.7 | 80.1 | 77.6 | 75.1 | 72.6 | 70.1 | 67.6 |
| 4 (44) | 89.6 | 87.1 | 84.6 | 82.1 | 79.6 | 77.0 | 74.5 | 72.0 | 69.5 |
| 2 (42) | 91.6 | 89.0 | 86.5 | 84.0 | 81.5 | 79.0 | 76.5 | 73.9 | 71.4 |
| 0 (40) | 93.5 | 91.0 | 88.5 | 85.9 | 83.4 | 80.9 | 78.4 | 75.9 | 73.3 |
| -2 (38) | 95.4 | 92.9 | 90.4 | 87.9 | 85.4 | 82.8 | 80.3 | 77.8 | 75.3 |
| -4 (36) | 97.4 | 94.8 | 92.3 | 89.8 | 87.3 | 84.8 | 82.2 | 79.7 | 77.2 |

### Rear overhang behind the base at 135° (mm)

| height (axis z) \ inset (axis y) | -6 (241) | -4 (239) | -2 (237) | 0 (235) | 2 (233) | 4 (231) | 6 (229) | 8 (227) | 10 (225) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 26 (66) | 176.4 | 173.0 | 169.6 | 166.2 | 162.8 | 159.3 | 155.9 | 152.5 | 149.1 |
| 24 (64) | 177.8 | 174.4 | 171.0 | 167.6 | 164.2 | 160.8 | 157.3 | 153.9 | 150.5 |
| 22 (62) | 179.2 | 175.8 | 172.4 | 169.0 | 165.6 | 162.2 | 158.8 | 155.3 | 151.9 |
| 20 (60) | 180.7 | 177.2 | 173.8 | 170.4 | 167.0 | 163.6 | 160.2 | 156.8 | 153.3 |
| 18 (58) | 182.1 | 178.7 | 175.2 | 171.8 | 168.4 | 165.0 | 161.6 | 158.2 | 154.8 |
| 16 (56) | 183.5 | 180.1 | 176.7 | 173.2 | 169.8 | 166.4 | 163.0 | 159.6 | 156.2 |
| 14 (54) | 184.9 | 181.5 | 178.1 | 174.7 | 171.2 | 167.8 | 164.4 | 161.0 | 157.6 |
| 12 (52) | 186.3 | 182.9 | 179.5 | 176.1 | 172.7 | 169.2 | 165.8 | 162.4 | 159.0 |
| 10 (50) | 187.7 | 184.3 | 180.9 | 177.5 | 174.1 | 170.7 | 167.2 | 163.8 | 160.4 |
| 8 (48) | 189.1 | 185.7 | 182.3 | 178.9 | 175.5 | 172.1 | 168.7 | 165.2 | 161.8 |
| 6 (46) | 190.6 | 187.1 | 183.7 | 180.3 | 176.9 | 173.5 | 170.1 | 166.7 | 163.2 |
| 4 (44) | 192.0 | 188.6 | 185.1 | 181.7 | 178.3 | 174.9 | 171.5 | 168.1 | 164.7 |
| 2 (42) | 193.4 | 190.0 | 186.6 | 183.1 | 179.7 | 176.3 | 172.9 | 169.5 | 166.1 |
| 0 (40) | 194.8 | 191.4 | 188.0 | 184.6 | 181.1 | 177.7 | 174.3 | 170.9 | 167.5 |
| -2 (38) | 196.2 | 192.8 | 189.4 | 186.0 | 182.6 | 179.1 | 175.7 | 172.3 | 168.9 |
| -4 (36) | 197.6 | 194.2 | 190.8 | 187.4 | 184.0 | 180.6 | 177.1 | 173.7 | 170.3 |

### Maximum overall height at 105° (mm)

| height (axis z) \ inset (axis y) | -6 (241) | -4 (239) | -2 (237) | 0 (235) | 2 (233) | 4 (231) | 6 (229) | 8 (227) | 10 (225) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 26 (66) | 305.3 | 303.3 | 301.4 | 299.5 | 297.5 | 295.6 | 293.7 | 291.7 | 289.8 |
| 24 (64) | 302.7 | 300.8 | 298.9 | 296.9 | 295.0 | 293.1 | 291.1 | 289.2 | 287.3 |
| 22 (62) | 300.2 | 298.3 | 296.4 | 294.4 | 292.5 | 290.6 | 288.6 | 286.7 | 284.8 |
| 20 (60) | 297.7 | 295.8 | 293.8 | 291.9 | 290.0 | 288.0 | 286.1 | 284.2 | 282.3 |
| 18 (58) | 295.2 | 293.3 | 291.3 | 289.4 | 287.5 | 285.5 | 283.6 | 281.7 | 279.7 |
| 16 (56) | 292.7 | 290.7 | 288.8 | 286.9 | 284.9 | 283.0 | 281.1 | 279.1 | 277.2 |
| 14 (54) | 290.2 | 288.2 | 286.3 | 284.4 | 282.4 | 280.5 | 278.6 | 276.6 | 274.7 |
| 12 (52) | 287.6 | 285.7 | 283.8 | 281.8 | 279.9 | 278.0 | 276.0 | 274.1 | 272.2 |
| 10 (50) | 285.1 | 283.2 | 281.3 | 279.3 | 277.4 | 275.5 | 273.5 | 271.6 | 269.7 |
| 8 (48) | 282.6 | 280.7 | 278.7 | 276.8 | 274.9 | 272.9 | 271.0 | 269.1 | 267.1 |
| 6 (46) | 280.1 | 278.1 | 276.2 | 274.3 | 272.4 | 270.4 | 268.5 | 266.6 | 264.6 |
| 4 (44) | 277.6 | 275.6 | 273.7 | 271.8 | 269.8 | 267.9 | 266.0 | 264.0 | 262.1 |
| 2 (42) | 275.0 | 273.1 | 271.2 | 269.3 | 267.3 | 265.4 | 263.5 | 261.5 | 259.6 |
| 0 (40) | 272.5 | 270.6 | 268.7 | 266.7 | 264.8 | 262.9 | 260.9 | 259.0 | 257.1 |
| -2 (38) | 270.0 | 268.1 | 266.1 | 264.2 | 262.3 | 260.4 | 258.4 | 256.5 | 254.6 |
| -4 (36) | 267.5 | 265.6 | 263.6 | 261.7 | 259.8 | 257.8 | 255.9 | 254.0 | 252.0 |

### Maximum overall height at 135° (mm)

| height (axis z) \ inset (axis y) | -6 (241) | -4 (239) | -2 (237) | 0 (235) | 2 (233) | 4 (231) | 6 (229) | 8 (227) | 10 (225) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 26 (66) | 254.1 | 252.7 | 251.3 | 249.8 | 248.4 | 247.0 | 245.6 | 244.2 | 242.8 |
| 24 (64) | 250.7 | 249.3 | 247.8 | 246.4 | 245.0 | 243.6 | 242.2 | 240.8 | 239.4 |
| 22 (62) | 247.3 | 245.8 | 244.4 | 243.0 | 241.6 | 240.2 | 238.8 | 237.4 | 235.9 |
| 20 (60) | 243.8 | 242.4 | 241.0 | 239.6 | 238.2 | 236.8 | 235.4 | 233.9 | 232.5 |
| 18 (58) | 240.4 | 239.0 | 237.6 | 236.2 | 234.8 | 233.4 | 231.9 | 230.5 | 229.1 |
| 16 (56) | 237.0 | 235.6 | 234.2 | 232.8 | 231.4 | 229.9 | 228.5 | 227.1 | 225.7 |
| 14 (54) | 233.6 | 232.2 | 230.8 | 229.4 | 227.9 | 226.5 | 225.1 | 223.7 | 222.3 |
| 12 (52) | 230.2 | 228.8 | 227.4 | 225.9 | 224.5 | 223.1 | 221.7 | 220.3 | 218.9 |
| 10 (50) | 226.8 | 225.4 | 223.9 | 222.5 | 221.1 | 219.7 | 218.3 | 216.9 | 215.5 |
| 8 (48) | 223.4 | 221.9 | 220.5 | 219.1 | 217.7 | 216.3 | 214.9 | 213.5 | 212.0 |
| 6 (46) | 219.9 | 218.5 | 217.1 | 215.7 | 214.3 | 212.9 | 211.5 | 210.0 | 208.6 |
| 4 (44) | 216.5 | 215.1 | 213.7 | 212.3 | 210.9 | 209.5 | 208.0 | 206.6 | 205.2 |
| 2 (42) | 213.1 | 211.7 | 210.3 | 208.9 | 207.5 | 206.0 | 204.6 | 203.2 | 201.8 |
| 0 (40) | 209.7 | 208.3 | 206.9 | 205.5 | 204.0 | 202.6 | 201.2 | 199.8 | 198.4 |
| -2 (38) | 206.3 | 204.9 | 203.5 | 202.0 | 200.6 | 199.2 | 197.8 | 196.4 | 195.0 |
| -4 (36) | 202.9 | 201.5 | 200.0 | 198.6 | 197.2 | 195.8 | 194.4 | 193.0 | 191.6 |

Feasible points: 63 of 144. Ground collisions: 0. Minimum display–keyboard/trackpad clearance over all points and angles: 2.00 mm.
Largest difference between 5° and 0.1° sampling of the minimum clearance: 0.021 mm; pass/fail changes: 0.

## Observations (modeled; no point is recommended)

1. **Feasible region:** inset ≤ 0, meaning the axis is on or behind the base rear face (axis y ≥ 235), at every tested height from −4 to 26. The one exception is the exact rear-top corner (inset 0, height 0), which reaches only 0.71 mm. That is 63 of 144 points. No point with inset > 0 is feasible.
2. **The boundary at inset 0 is structural, not a sampling artifact.**
   - With the axis above the lid's rear-bottom edge (height > 1) and ahead of it (inset > 0), that edge swings down as the lid starts to open.
   - Its lowest point dips by √(inset² + (height − 1)²) − (height − 1) mm.
   - The clearance is therefore LID_CLOSED_GAP − dip. That value is below 1.0 for every inset > 0, because LID_CLOSED_GAP = MIN_GAP = 1.0.
   - The formula reproduces the table exactly, e.g. inset 4 / height 10 → 0.15 and inset 2 / height 26 → 0.92.
   - The boundary therefore depends on LID_CLOSED_GAP: a larger closed gap would admit some inset > 0 points with a high axis.
3. **Every feasible point meets the requirement with zero margin.** Its minimum is exactly the closed-pose gap of 1.00 at 0°, because LID_CLOSED_GAP equals MIN_GAP. During opening, the clearance of feasible points is 1.00–1.62. It grows as the axis moves rearward (about +0.09 mm per 1 mm of inset) and hardly depends on height.
4. **The exact corner behaves unexpectedly.** At inset 0, height 0 fails (0.71 at 135°: the lid's rear face closes on the base's rear face), while heights −2 and +2 both pass (1.01 and 1.00).
5. **There are two separate collision modes in the infeasible region:**
   - (a) An early-opening dip of the lid's rear-bottom edge, with the minimum between 5° and 40°. This happens when the axis is high.
   - (b) End-of-travel intrusion of the lid tail into the base at 135°, when the axis is low.

   The switch between them is visible at inset 6–10, between heights 12 and 14. That is why the table jumps from about −0.3 to −1.8 there.
6. **Trade-offs are smooth and linear within the grid:**
   - Each 2 mm the axis moves rearward adds about 2.5 mm of rear overhang at 105° and about 3.4 mm at 135°.
   - Each 2 mm the axis rises removes about 1.9 mm of overhang at 105° and about 1.4 mm at 135°, and adds about 2.5 mm (105°) or 3.4 mm (135°) of overall height.
   - Within the feasible region: overhang at 105° is 60.8–97.4 mm, overhang at 135° is 166.2–197.6 mm, max height at 105° is 261.7–305.3 mm, and max height at 135° is 198.6–254.1 mm.
7. **Other checks:**
   - No ground contact at any point.
   - Display–keyboard/trackpad clearance never falls below 2.0 mm; the minimum is always the closed pose.
   - 0.1° sampling changes no pass/fail result; the largest difference from 5° sampling is 0.021 mm.
8. **Physical meaning is not evaluated.** A negative inset puts the axis behind the base's rear face, so hinge hardware would stand proud of the rear face. A height above 1 puts the axis inside or above the closed lid's thickness. Neither is assessed for strength, cable routing or wind load; that is outside this map. *(inferred)*