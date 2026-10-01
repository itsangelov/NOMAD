# B1 SB-261 physical validation coupon: specification and test procedure

> **PHYSICAL VALIDATION REQUIRED.** The coupon is designed and kernel-checked only. It has **not** been printed, assembled or tested, and no hardware has been ordered.
>
> This is exploratory, pre-decision work. D-010 is pending and B1 is not selected (see [README.md](README.md)).

- **Source:** the final coupon report, [reports/04](reports/04_coupon_final_report_2026-10-01.md) (2026-10-01), reorganised here. No values were added.
- **Model:** Onshape scratch workspace `07eafe33cb44fd16843cea57`, feature `B1HingeCoupon` (see [SOURCES.md](SOURCES.md)). Code: [src/fs/coupon_common.fs](src/fs/coupon_common.fs), [src/fs/coupon_prod.fs](src/fs/coupon_prod.fs).
- **Feature parameters (defaults):**

  | Parameter | Default |
  |---|---|
  | Leaf angle ψ | 0° |
  | Lid / rig angle φ | 0° |
  | Running gap | 0.5 |
  | Lid insert hole | Ø4.0 |
  | Leaf insert hole | Ø3.1 × 4.5 deep |
  | Print layout | off |
  | Show hardware | on |

## Kernel re-validation (after the leaf boolean fix)

The first build showed false 0.00 mm clearances. That was a modelling bug: cuts were applied to the wrong leaf solid. The fix cuts all five raw leaf solids first and unions them afterwards. Each coupon part is now one solid (n 1/1). No dimensions changed.

| Check | Expected | Kernel |
|---|---|---|
| Leaf block to fixed bands | 0.5 | 0.50 |
| Lid screw heads to leaf | ~1.0 | 1.00 |
| Leaf screw heads to lid pocket | — | 1.00 |
| Lid insert wall: pocket / chamfer / groove | 1.47 / 1.89 / 3.2 | 1.47 / 1.89 / 3.21 |
| Leaf insert wall: Ø4.0 envelope / real Ø3.55 insert | 1.20 | 1.20 / 1.42 |
| Leaf vs lid at 30 / 60 / 90 / 120 / 150 / 180° | as B1 | 2.83 / 4.82 / 6.47 / 6.61 / 4.80 / 3.13 |
| Leaf vs lid at 190° | 2.03 | 2.26 |
| First contact | ~201° | 201° (leaf front-top chamfer on the lid's 9×45 chamfer) |

The coupon's 190° value (2.26) differs from B1's (2.03). The coupon plate carries B1's chamfered side-wall profile, while B1's 2.03 comes from the bare panel corner. Both make first contact at 201°.

## 1. Geometry: 2 printed parts, 1 real hinge

**COUPON-LID**, 48 × 40 × 14 mm, 23.16 cm³ (kernel):
- 9 × 45 edge chamfer; barrel groove R4.02.
- Two fixed-flag seats, 1.0 mm deep.
- Two-zone pocket:
  - deep zone ±8.15, floor 4.1 below the seats
  - shallow zone ±9.2, floor 1.0 below the flags
- Two M3 insert holes, Ø4.0 × 7.6 deep, at ±11.92. Inserts sit 1 mm below the seat.
- Two Ø5.5 holes for mounting to a board.

**COUPON-LEAF**, 44 × 106 mm, 12 mm tall at the hinge, 32.65 cm³ (kernel), CG at y 57.44:
- Hinge block ±7.85, which gives the 0.5 mm gap to the fixed bands.
- Cradle for the band barrel; Ø9.05 relief over the centre C-rings.
- Beam notched over the fixed flags and screw heads.
- Two M2.5 insert holes, Ø3.1 × 4.5, at ±4.65.
- 6 mm plate with a 3 × 45 front chamfer and two stiffening ribs.
- **Lever holes Ø4 at 50, 75 and 100 mm** horizontally from the hinge axis when the leaf is level.

**Material and time (CALC):** about 19–22 g plus 27–31 g of PETG, about 50 g in total, roughly 2–4 h of printing.

**Leaf self-weight torque:** about 0.017 N·m, around 2% of the target. The two-direction torque test cancels it.

## 2. Hardware (nothing is owned or ordered)

| Item | Qty | Notes |
|---|---|---|
| TorqMaster **SB-188-SB-261-6** | 2 (1 per coupon) | The second shows sample variation and serves as a spare |
| Ruthex **RX-M3x5.7** | 4 + spares | D1 4.6, hole **4.0**, L 5.7 |
| M2.5 × 4 insert, **OD 3.55**, hole **3.10** | 4 + spares | PartsBuilt PBX-TI-M25-4L35W-4PK, or equivalent with OD ≤ 3.6 and L 4 |
| ISO 7380 M3×8 | 4 + spares | 2 mm hex; 5.7 mm thread engagement |
| ISO 7380 M2.5×5 | 4 + spares | 1.5 mm hex; 3.4 mm thread engagement |
| DIN 433 M2.5 washer (2.7 × 5 × 0.5) | 4 + spares | |
| M5 screws or bolts | 2 (optional) | To fix the lid coupon to a board |

- **Do not use** standard 4.6 mm-OD M2.5 inserts. They leave about 0.9 mm of wall.
- **Lid wall vs Ruthex guidance:** Ruthex states a 1.6 mm minimum wall. The lid wall is 1.47 mm to the knurl and 1.77 mm to the hole, so this is a question the coupon must answer.
- **Tools:**
  - soldering iron with M3 and M2.5 insert tips
  - 1.5 and 2.0 mm hex keys
  - calipers with a depth rod
  - feeler gauges 0.3–0.6 mm
  - digital luggage scale (0–5 kg, 10 g resolution) and string
  - a known mass of about 0.85 kg
  - phone inclinometer
  - vise or clamps

## 3. Print recipe (baseline)

- PETG, 0.4 mm nozzle, 0.20 mm layers, 4 perimeters, 5 top and bottom layers, 40% gyroid infill, no supports.
- **Lid:** base face down, as modelled.
- **Leaf:** plate face down, flag face up (use the "print layout" option). 5 mm brim on the leaf only.
- **After printing:**
  - Measure the holes. If Ø4.0 or Ø3.1 comes out more than about 0.15 mm undersize, change the hole parameter and reprint.
  - Measure the block width (nominal 15.69). If it is off by more than 0.1, correct the gap parameter so the as-printed gap is 0.5.

## 4. Assembly

1. **Inserts** (iron at about 230–245 °C, kept vertical). Let each cool before loading.
   - **Leaf M2.5:** flush, then 0.1–0.2 mm below. Remove any raised lip.
   - **Lid M3:** 1.0 ± 0.2 mm below the seat floor, checked with the depth rod.
2. **Hinge to leaf:**
   - Leaf part on the bench, flag face up.
   - Middle (rotating) flags on the block.
   - Fit M2.5×5 with washers, snug, about 0.25 N·m. The outer flags stay free.
3. **Leaf to lid:**
   - Leaf rotated to about 180°.
   - Drop the outer (fixed) flags into the seats.
   - Fit M3×8 from above, about 0.4–0.5 N·m.
4. **No threadlocker.** One purpose of the test is to see whether the screws loosen.

## 5. Test procedure

1. **Static fit, closed:**
   - Flags seat flat with no rocking.
   - A 0.4 mm feeler fits between the block and the fixed band; a 0.6 mm feeler does not.
   - The barrel turns freely in the groove.
   - All four screw heads clear.
2. **Motion:**
   - Move 0 → 30 → 60 → 90 → 120 → 150 → 180 → 190° and back, checking angles with the inclinometer.
   - Note any binding, scraping or visible flex.
   - Record the first contact angle (CAD: about 201°).
3. **Rig:** fix the lid coupon with its back face vertical, so the leaf is level at 90°.
4. **Two-direction torque:**
   - Hook the luggage scale at the **100 mm** hole and pull perpendicular, slowly and steadily.
   - Read 5 × up (F_up) and 5 × down (F_down) while the leaf is moving.
   - **T = (F_up + F_down) / 2 × 0.100 m.** This cancels the leaf's own weight.
   - Repeat once at 75 mm and at 50 mm as a check.
   - **Reference forces at 100 mm:**
     - requirement 0.83 N·m = **8.3 N**
     - published 0.96–1.13 N·m = 9.6–11.3 N
   - This compares the installed assembly; it is not a measurement of the manufacturer's rating.
5. **Static hold:** hang **0.85 kg** from the 100 mm hole with the leaf level. Mark the angle and leave it 10 minutes.
6. **Optional durability:** a few hundred hand cycles over 0–190°, then repeat steps 1, 4 and 5. This indicates early wear only; it does not establish life.
7. **Inspection:**
   - Insert faces and walls: whitening, cracks, a raised or pulled insert.
   - Any change in the gap.
   - Every screw still tight.

## 6. Pass / fail

| Criterion | Pass |
|---|---|
| Inserts | None spin, rise or pull out during tightening, three remove-and-refit cycles, or testing |
| Walls | No cracks or stress whitening around any insert, the gap faces or the seats |
| Binding and interference | Smooth 0–190°; no contact before about 195°; the 0.4 mm feeler still passes after testing |
| Unwanted movement | No flag shift in its seat; no hinge axial play (pencil marks unchanged) |
| Sag / slip | ≤ about 1–2° drift during the 10-minute hold; measured torque ≥ 0.83 N·m in both directions |
| Screw access | All four screws removable and refittable with standard hex keys while the leaf is open, with nothing taken apart |
| Repeatability | Readings and the two hinges agree within about ±15%; torque after cycling stays ≥ 0.83 N·m |

**Not judged by this test:** the unpublished load, material and temperature ratings.

## 7. Migration gate (before SB-261 enters authoritative NOMAD CAD)

All of the following must hold on at least one coupon, preferably both hinges:
- inserts and walls intact
- the 0.5 mm gap holds with no rubbing
- full 0–190° motion, with contact only beyond about 195°
- installed torque ≥ 0.83 N·m in both directions
- the static hold passes
- the screws stay tight and remain accessible

**On failure:**
- A wall or insert failure: first try the planned fallback, a thread-forming screw on the leaf side or a wall-margin change.
- Torque below 0.83 N·m: an owner decision (torque margin or hinge band), not a geometry fix.

**Even after a pass,** the unpublished load and temperature data remain open risks. **Migration also requires the owner's D-010 decision to select B1.**
