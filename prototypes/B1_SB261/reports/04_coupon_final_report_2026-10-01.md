# B1 SB-261 physical validation coupon: final report

The coupon is fixed, re-validated in the kernel and saved to its own scratch workspace. Nothing was printed or tested yet.

The 0.00 mm clearances were a modelling bug, not a design failure. The leaf part was built as two separate solids, and the cuts were applied to the wrong one. I now cut all five leaf solids first and merge them afterwards, so each coupon part is a single solid. No dimensions changed.

Re-validated in the kernel (Onshape's geometry engine):

| Check | Expected | Result |
|---|---|---|
| Leaf block to fixed hinge bands | 0.5 | **0.50** |
| Lid screw heads to leaf | ~1.0 | **1.00** |
| Leaf screw heads to lid pocket | — | 1.00 |
| Lid insert wall: pocket / chamfer / groove | 1.47 / 1.89 / 3.2 | **1.47 / 1.89 / 3.21** |
| Leaf insert wall: Ø4.0 validated envelope / real Ø3.55 insert | 1.20 | **1.20 / 1.42** |
| Leaf vs lid at 30 / 60 / 90 / 120 / 150 / 180° | as B1 | 2.83 / 4.82 / 6.47 / 6.61 / 4.80 / 3.13 (identical to B1) |
| Leaf vs lid at 190° | 2.03 | **2.26** |
| First contact | ~201° | **201°** (leaf front-top chamfer on the lid's 9×45 chamfer) |

The 190° value differs from B1 because the coupon plate carries B1's chamfered side-wall profile. B1's 2.03 mm comes from the bare panel corner. Contact happens at 201° in both.

Scratch model: [B1HingeCoupon workspace](https://cad.onshape.com/documents/a3313eb551a601b46ae8de86/w/07eafe33cb44fd16843cea57/e/7c60e1e6eabeb79b9514eabf). It is in the connector's own scratch document, separate from NOMAD.
- **Adjustable parameters:** leaf angle, lid/rig angle, running gap (0.5), lid insert hole (4.0), leaf insert hole (3.1) and its depth (4.5), print layout, show hardware.

## 1. Coupon geometry (2 printed parts, 1 real hinge)
- **COUPON-LID:** 48 × 40 × 14 mm.
  - 9×45 edge chamfer, barrel groove R4.02.
  - Two fixed-flag seats, 1.0 mm deep.
  - Two-zone pocket: deep ±8.15 mm with floor 4.1 below the seats, shallow ±9.2 mm with floor 1.0 below the flags.
  - Two M3 insert holes, Ø4.0 × 7.6 deep, at ±11.92 mm with the insert set 1 mm below the seat.
  - Two Ø5.5 holes for mounting to a board.
- **COUPON-LEAF:** 44 × 106 mm, 12 mm tall at the hinge.
  - Hinge block ±7.85 mm, which gives the 0.5 mm gap to the fixed bands.
  - Cradle for the band barrel, Ø9.05 relief over the centre C-rings, beam notched over the fixed flags and screw heads.
  - Two M2.5 insert holes, Ø3.1 × 4.5, at ±4.65 mm.
  - 6 mm plate with a 3×45 front chamfer, and two stiffening ribs.
  - **Lever holes Ø4 at 50, 75 and 100 mm** horizontally from the hinge axis when the leaf is level.
- **Material and time:** about 19–22 g plus 27–31 g of PETG, roughly 50 g in total, and about 2–4 h of printing depending on the printer (CALC from kernel volumes of 23.2 and 32.7 cm³).
- **Leaf self-weight torque:** about 0.017 N·m, around 2% of the target. The two-direction torque test cancels it.

## 2. Hardware (assume nothing is owned)

| Item | Quantity | Notes |
|---|---|---|
| TorqMaster **SB-188-SB-261-6** | **2** (1 per coupon) | The second shows sample-to-sample variation and serves as a spare |
| Ruthex **RX-M3x5.7** | 4 + spares (pack of 100) | D1 4.6, hole **4.0**, L 5.7 ([Ruthex](https://www.ruthex.de/en/products/ruthex-gewindeeinsatz-m3-100-stuck-rx-m3x5-7-messing-gewindebuchsen)) |
| M2.5 × 4 insert, **OD 3.55**, hole **3.10** | 4 + spares | PartsBuilt PBX-TI-M25-4L35W-4PK ([PartsBuilt](https://partsbuilt.com/m2-5-heat-set-thread-insert-4mm-long-4-pack/)), or equivalent with OD ≤ 3.6 and L 4 |
| **ISO 7380 M3×8** | 4 + spares | 2 mm hex; 5.7 mm thread engagement (full insert) |
| **ISO 7380 M2.5×5** | 4 + spares | 1.5 mm hex; 3.4 mm thread engagement |
| **DIN 433 M2.5 washer** (2.7 × 5 × 0.5) | 4 + spares | |
| M5 screws or bolts | 2 (optional) | To fix the lid coupon to a board |

- **Do not use** standard 4.6 mm-OD M2.5 inserts (Ruthex, CNC Kitchen). They leave about 0.9 mm of wall.
- **Lid wall vs Ruthex guidance:** Ruthex states a 1.6 mm minimum wall. The lid wall is 1.47 mm to the knurl and 1.77 mm to the hole, so this is a question the coupon has to answer.
- **Tools:** soldering iron with M3 and M2.5 insert tips, 1.5 and 2.0 mm hex keys, calipers with a depth rod, feeler gauges 0.3–0.6 mm, a digital luggage scale (0–5 kg, 10 g resolution), string, a known mass of about 0.85 kg (for example a water bottle weighed on a kitchen scale), a phone inclinometer, and a vise or clamps.

## 3. Print recipe
- **Baseline:** PETG, 0.4 mm nozzle, 0.20 mm layers, 4 perimeters, 5 top and bottom layers, 40% gyroid infill, no supports.
  - **Lid:** base face down, as modelled.
  - **Leaf:** plate face down, flag face up (use the "print layout" option). A 5 mm brim on the leaf only.
- **Geometry-dependent checks after printing:**
  - Measure the printed holes. If the Ø4.0 or Ø3.1 hole comes out more than about 0.15 mm undersize, change the hole parameter and reprint.
  - Measure the block width (nominal 15.69). If it is off by more than 0.1, correct the gap parameter so the as-printed gap is 0.5, not the CAD gap.
  - The 0.5 mm gap faces print as vertical walls, which is the most accurate orientation.

## 4. Assembly
1. **Inserts** (iron at about 230–245 °C for PETG, kept vertical):
   - **Leaf M2.5:** press until flush, then 0.1–0.2 mm below. Remove any raised lip so the flag sits flat.
   - **Lid M3:** press to 1.0 ± 0.2 mm below the seat floor, checked with the depth rod.
   - Let each cool before loading.
2. **Hinge to leaf:** leaf part on the bench, flag face up. Lay the two middle (rotating) flags on the block. Fit M2.5×5 with washers, snug, about 0.25 N·m. The outer flags stay free.
3. **Leaf to lid:** with the leaf rotated to about 180°, drop the outer (fixed) flags into the seats. Fit M3×8 from above, about 0.4–0.5 N·m.
4. **No threadlocker:** one purpose of the test is to see whether the screws loosen.

## 5. Test procedure
1. **Static fit, closed:**
   - Flags seat flat with no rocking.
   - 0.4 mm feeler fits between the block and the fixed band; 0.6 mm does not.
   - Barrel turns freely in the groove.
   - All four screw heads clear.
2. **Motion:** move slowly 0 → 30 → 60 → 90 → 120 → 150 → 180 → 190° and back, checking angles with the inclinometer.
   - Note any binding, scraping, or flex that is visible.
   - Record the angle where the leaf first touches the chamfer (CAD says about 201°).
3. **Friction and holding:** fix the lid coupon with its back face vertical, so the leaf is level at 90°.
4. **Two-direction torque:** hook the luggage scale at the **100 mm** hole and pull perpendicular, slowly and steadily.
   - Read the force while the leaf is moving, 5 times upward (F_up) and 5 times downward (F_down).
   - **T = (F_up + F_down)/2 × 0.100 m**. This cancels the leaf's own weight.
   - Repeat once at 75 mm and at 50 mm as a check.
   - Reference forces at 100 mm: 0.83 N·m = **8.3 N**; published 0.96–1.13 N·m = 9.6–11.3 N.
   - This is an installed-assembly comparison, not a measurement of the manufacturer's rating.
5. **Static hold:** hang **0.85 kg** from the 100 mm hole with the leaf level. Mark the angle and leave it 10 minutes.
6. **Optional durability:** a few hundred hand cycles over 0–190°, then repeat steps 1, 4 and 5. This only indicates early wear; it does not establish life.
7. **Inspection:** check insert faces and walls for whitening, cracks, a raised or pulled insert, or a changed gap. Re-check that every screw is still tight.

## 6. Pass/fail
- **Inserts:** none spin, rise or pull out during screw tightening, three remove-and-refit cycles, or testing.
- **Walls:** no cracks or stress whitening around any insert, the gap faces or the seats.
- **Binding and interference:** smooth motion from 0° to 190°, no contact before about 195°, and the 0.4 mm feeler still passes after testing.
- **Unwanted movement:** no flag shift in its seat and no axial play of the hinge (pencil marks unchanged).
- **Sag / slip:** at most about 1–2° of drift during the 10-minute hold, and the measured torque is at least 0.83 N·m in both directions.
- **Screw access:** all four screws removable and refittable with standard hex keys while the leaf is open, with nothing taken apart.
- **Repeatability:** the readings and the two hinges agree within about ±15%. Torque after cycling stays at or above 0.83 N·m.
- **Not judged by this test:** I'm not setting tighter limits because the published data doesn't support them. The coupon does **not** validate the unpublished load, material or temperature ratings.

## 7. Migration gate (for moving SB-261 into the authoritative NOMAD CAD)
All of the following must hold on at least one coupon, preferably both hinges:
- inserts and walls intact
- 0.5 mm gap holds with no rubbing
- full 0–190° motion with contact only beyond about 195°
- installed torque at least 0.83 N·m in both directions
- static hold passes
- screws stay tight and remain accessible

Any wall or insert failure means first trying the planned fallback: a thread-forming screw on the leaf side, or a wall-margin change. Any torque below 0.83 N·m is an owner decision about torque margin or the hinge band, not a geometry fix. Even after passing, the unpublished load and temperature data remain open risks.

Onshape API use for this stage was about 48 requests (468 → 516 of 2,500). The repo, YAML, D-010, the NOMAD document and Git were untouched. The scratch sources are in the session scratchpad (`fs/coupon_common.fs`, `fs/coupon_prod.fs`). I'm stopping here; nothing has been migrated.