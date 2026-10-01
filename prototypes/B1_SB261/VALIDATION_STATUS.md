# B1 SB-261: validation status (2026-10-01)

## PHYSICAL VALIDATION REQUIRED

**The SB-188-SB-261-6 hinge arrangement for B1 is NOT physically validated.**
- No coupon has been printed.
- No hinge, insert or screw has been purchased.
- Nothing has been measured or tested.

**Decision state:**

| Decision | State |
|---|---|
| D-010 (A vs B1) | Pending the owner |
| B1 | **Not** officially selected |
| D-007 | Proposed, **not** accepted |

This is exploratory, pre-decision work.

## Status by item

| Item | Status | Evidence |
|---|---|---|
| SB-261 geometry (shaft, bands, flags, holes, gaps) | Measured from the vendor's REV A IGES | IGES |
| ".14" = axis to flag outer face; inner face tangent to the shaft | Established from the IGES | IGES |
| F-R-R-F fixed/rotating assignment | Follows the drawing's FIXED label. The bands are identical, so mounting decides it | IGES + drawing (INF) |
| B1 rail geometry (axis y 4.0 z 63.5, chamfer 9×45, pocket, seats) | Modelled and kernel-checked in scratch | kernel |
| 0–190° leaf motion, first contact 201° | Kernel-checked in scratch | kernel |
| Static clearances (0.50 gap, 1.00 heads, …) | Kernel-checked in scratch | kernel |
| Cable bends R12, twist 2.97°/mm, separation ≥ 9.8 | Kernel-checked in scratch | kernel / CALC |
| Surroundings (display, base, stay, plug, table) | Kernel-checked in scratch; table contact at lid 125° is pre-existing B1 kinematics | kernel |
| Insert walls 1.20–1.47 mm | Modelled; the lid wall is below the vendor's 1.6 guidance | kernel / CALC; **needs the coupon** |
| 0.5 mm printed-block-to-steel-band running gap | Modelled | kernel; **needs the coupon** |
| Torque 0.96–1.13 N·m per hinge vs 0.83 required (SF ≈ 1.16) | Published band vs calculated requirement | PUB / CALC; **needs the coupon** |
| Gravity torque 0.498 N·m (pair) | Calculated | CALC |
| Radial, axial, moment capacity; material; temperature | **Unknown, unpublished** | none |
| Coupon geometry (COUPON-LID / COUPON-LEAF) | Designed and kernel-checked; saved in an Onshape scratch workspace | kernel |
| Coupon print, assembly, torque, hold, cycling | **Not done** | none |
| Life (30,000+ cycles) | Vendor claim only | PUB |

## Where the model lives

**Onshape:** only the connector's scratch document (see [SOURCES.md](SOURCES.md)).
- Not in the NOMAD Onshape document.
- Not in `NOMAD_D010_Concepts`.
- Not in `NOMAD_E_Prototype`.

**Repo:** `src/` holds the scratch code only. `nomad.yaml` has no SB-261 or B1-rail parameters.

## What would change the status

1. The owner's D-010 decision. Without B1 selected, no migration happens.
2. A coupon test that passes the [migration gate](COUPON_SPEC.md#7-migration-gate-before-sb-261-enters-authoritative-nomad-cad).
3. Vendor answers on load, material and temperature (questions in [reports/01](reports/01_hardware_second_pass_2026-10-01.md) §4). Contacting the vendor needs owner approval.
