# B1 hinge rail around SB-188-SB-261: scratch concept study

SB-261 fits B1 geometrically, using plain M3 hardware and no adapters. The lid and the leaf move freely from 0° to 190°, with first contact at about 202°. All cable bends are R 12.

The key move is to **put the hinge's structure into the lid, not beside the panel**. Lowering the hinge axis by 5 mm drops the flags into a rail built into the lid's top edge. The only visible changes to the lid are an 8 mm × 45° chamfer on its top edge and the pocket cut-outs.

Evidence: everything here is **modelled** in a scratch 2D section model or **CALC**. Nothing is physically tested.
- I used the published SB-261 drawing, standard M3 hardware dimensions, and the existing B1 stack (lid back z 61, panel z 67–71, leaf top z 73, lid depth 235).
- The model sweeps 7 sections through the hinge line over 0–240° at 0.1 mm resolution.
- World checks against the base, plug, table and stay ran the D-010 study kinematics, read-only.
- Nothing in the repo, YAML, FeatureScript, Onshape (0 calls) or Git was touched. The scratch files are `b1_sb261_rail.py`, `b1_sb261_draw.py` and the section PNG/SVG in the session scratchpad.

## A. Scratch CAD result

**Hinge position.** The axis is at **y 4.0, z 64.0** in the closed-lid frame. That is 5 mm lower than the current model's (4, 69).
- The barrel sits 0.44 mm inside the lid edge (no protrusion).
- The axis is 3 mm above the lid back, 3 mm below the panel back, and 9 mm below the leaf top.
- Hinge centres are at x = ±115.

Lowering the axis is what makes conventional mounting work. Both flag pairs now lie at z 59.3–60.4, in the lid rail, instead of under the panel. The cost is an 8 × 45° chamfer on the lid's top edge, so the leaf can pass 180–190°.

**Rail and bezel size.** The y budget is fixed by the stock panel: 235 − 223 = 12 mm. I split it 9 mm at the front and 3 mm at the rear: the rear frame becomes 2.5 mm of wall plus 0.5 mm of rebate, using the relaxed rim.

A visible 10–15 mm strip would therefore mean lengthening the lid. It isn't needed, because the structure goes **down** into the lid instead:
- **Lid hinge rail:** occupies y 0–20, z ≈ 51.6–61, inside the lid's existing display-free top strip. The display starts at y 42.5, so the display-side top bezel is unchanged.
- **Visible back strip:** 9 mm, most of it the 8 × 45° chamfer, with the barrels and the cable sleeve sitting on it.
- **Leaf front beam:** 9 × 6 mm (y 9–18, z 61–67) under the panel's front edge.

**Flag mounting (both conventional M3).** I assumed the segment order is fixed–rotating–rotating–fixed (outer flags fixed); this still needs checking against the IGES.

| Flag | Location | Fastening | Access |
|---|---|---|---|
| **Fixed flags** | 1.7 mm deep seat in the lid rail | ISO 7380 M3×6 from above into a standard M3 heat-set insert (L 5.7) in the rail | From above, with the leaf open |
| **Rotating flags** | On a leaf block that hugs its own barrel segment | ISO 7380 M3×5 from below into a short M3 insert (L 4) in the block; the head sits in a lid pocket (R 16, floor z 56.5) at those segments | From below; exposed once the leaf is open about 90° or more |

- **Insert-boss walls:** ≥ 2.7 mm.
- **No panel removal** is needed to service either hinge.
- **Screw shear from the friction torque:** about 72 N per screw at 1.13 N·m (CALC).

**Cable routing.** The cable leaves the panel junction at the assumed position (0, 40), runs in the gap layer at z 64, and bends R 12 onto the axis. Along the axis it runs in a lid-fixed tube (OD 7.5 / ID 5.5).
- **Twist zone:** x 12 to 76, 64 mm, which is 2.97°/mm against the study limit of 3.5.
- **Lid end:** the cable bends R 12 toward +y, descends through a lid-back slot at y ≈ 22–30, then runs at z 53 to rejoin the existing lid route at x 141.
- **Total length:** 582 mm.
- **Separate from the hinge:** the right hinge starts 8 mm beyond the lid exit.

**Leaf motion.** The leaf has full motion from 0° to 190°. The first contact beyond that is the leaf's front-top corner meeting the lid chamfer face at 202°, which can serve as a natural soft-stop surface.

## B. Clearance check (mm)

| Item | Value |
|---|---|
| Hinge barrel to panel | 2.27 |
| Sleeve to panel / to leaf beam | 2.08 / 1.25 |
| Hinge to display | ≥ 22.5 in y (pocket edge); insert boss 26.6 from the display edge |
| Lid screw head to panel / to stepped leaf beam | 4.91 / 1.00 |
| Leaf screw head to pocket floor | 1.15; ≥ 1.24 while sweeping |
| Leaf insert cap to panel back | 2.56 |
| Cable in the gap layer, to lid back / to panel | 1.0 / 1.0 |
| Cable in the twist tube | 0.75 radial |
| Lid cable run to display back | 3.0 |
| Cable bend radius | **12.0 at every bend** |
| Leaf to lid, 30–190° (concentric pairs, constant) | ≥ 1.25 (sleeve) and 1.44 (beam to fixed barrel) |
| Leaf to lid at 190° | 2.08–2.33 |
| Leaf to lid edge chamfer at 190° | 2.08 (panel/beam), 2.33 (side wall or lip, with a 3 × 45° leaf corner chamfer) |
| First contact | 202° (lip/side-wall corner), 206° (everything else) |
| Leaf vs base, plug, table and stay, lid 90–125° | No pose worse than the current model; plug 0.94 → 1.37, table 1.37 → 3.00, stay 0.62 → 2.00 |
| Gravity torque on the leaf hinges | 0.498 N·m for both hinges (was 0.488) |

At 0° the leaf beam rests on the lid back, which serves as the closed stop.

## C. Recommended B1 geometry (comfortable values, not minimums)

- **Hinge axis:** y 4.0, z 64.0; hinge centres x ±115; two SB-261-6 hinges.
- **Panel and leaf:**
  - Panel at y 9–232, z 67–71.
  - Leaf outline y 9–235, with a 3.0 mm rear frame.
  - Lip allowed on all 4 sides, with a 3 × 45° chamfer on its front-top corner.
- **Lid:**
  - 8 × 45° chamfer along the full top edge.
  - Hinge rail in the top strip, y 0–20, z ≥ 51.6.
  - Barrel groove R 4.06 along the hinge length.
  - Fixed-flag seats 1.7 deep, with standard M3 inserts at y 11.87.
  - Pocket R 16 (floor z 56.5) about 17 mm wide in x at the rotating segments.
- **Leaf front beam:** 9 × 6 across the full width.
  - Stepped up to start at z 63.1 over the fixed flags.
  - Hinge blocks at y 4–17.5 with short M3 inserts.
  - Notches at x −2 to 12 (leaf cable) and x 76 to 92 (lid cable).
- **Fasteners:** 8 × ISO 7380 M3 in total (4 × M3×6 on the lid side, 4 × M3×5 on the leaf side).
- **Cable:** sleeve tube OD 7.5 / ID 5.5 on the axis at x 12–76, with exit bends at x 0–12 and 76–88, all R 12.

## D. Problems still open

1. **Torque margin (unchanged from the last pass).** Band -6 has a 0.96 N·m minimum against the 0.83 requirement, a safety factor of 1.16. No higher balanced band is published for SB-261. Against gravity alone the pair has 3.9× margin.
2. **Load capacity, material and temperature** are still unpublished. This affects validation, not this geometry.
3. **The cable is tight in the gap layer:** 1.0 mm to both the lid back and the panel. That meets the target with no spare, because a Ø4 cable sits in the existing 6 mm gap.
4. **Two hinge details are read from the drawing, not the model.** Both are checkable from the published IGES, without contacting the vendor.
   - **Segment order.** I assumed fixed–rotating–rotating–fixed. Another order only moves the pockets and seats along x.
   - **Flag offset.** I read ".14" as the flag's inner face being tangent to the barrel. If it is measured to the flag's outer face instead, the flags sit 1.14 mm higher. The leaf insert cap then drops to 1.42 mm, so a 3 mm short insert would be used. That still fits.

## E. Next step

What needs modelling next, in order:
1. **Read the published SB-261 IGES** (TorqMaster zip, public download) to confirm the segment order and the flag offset. I can parse it with the standard library once you approve the download.
2. **Build a 3D scratch model** of this concept: the lid rail block with groove, seats, pockets and inserts; the leaf beam and blocks; the SB-261 envelopes; the sleeve; and the 3D cable path. Then run the checks the 2D sections can't do: the x layout (segment gaps, shaft ends, pocket widths), the beam notches, and the 3D cable. This would go in a new isolated Onshape Feature Studio, at roughly 20–40 API calls. It needs your approval and would not touch production.
3. **Physical:** buy 2 × SB-188-SB-261-6 and print a rail coupon (lid seat + leaf block + inserts) to check the fit and the friction torque in hand.

**Approval needed:** downloading the IGES; the scratch Onshape model and its API budget; and the concept direction itself. That direction means the axis moves to z 64, the rear rim shrinks to 3.0, and the lid gets the 8 × 45° top-edge chamfer and the hinge rail.