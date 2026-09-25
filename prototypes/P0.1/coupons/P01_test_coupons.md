# P0.1 Test Coupons: Solar Rail (A) and Rear Shell (B)

**Printable files:** `CAD/coupons/P0.1/` (see its README).

**Round B.3 file changes** (details in that README):
- The rail is **200 long**: the channel keeps its full 198 mm and the end stop sits beyond it. This preserves the 149.5 mm arm; the text below said 198 with the stop inside it.
- The carriage post is 12.6 tall, so the carriage is 40 × 22 × 20.
- 0.5 mm edge reliefs replace the chamfers.
- A load platform was added.

**Status:** coupon design and test plan. The coupons use Concept C (two-piece lid) as a **provisional** basis. They are not the final V1 design, and nothing here changes `nomad.yaml`.

**Purpose:** turn the two largest screening risks from Round B.2 into measurements.
1. The solar rail cantilever over the display: model 0.69 mm with a 0.3 kg cassette, against 1.0 mm clearance.
2. The 202 mm rear-shell span: plain 2.5 mm plate versus ribbed plate, plus the heat-set insert joint.

The coupons calibrate the P0.1 screening model against reality. They do not replace FEA. Expected values come from `CAD/tools/coupon_expectations.py`, on the same basis as `lid_structure_screening.py`.

---

## Why these coupons are small but still representative

| Risk | Governing quantity | What the coupon keeps full-size | What it leaves out |
|---|---|---|---|
| Rail cantilever | Deflection = P·a³/(3·E·I): cubic in the arm *a* | **The whole V1 rail (198 mm)**. Scaling the arm would change deflection with the cube of length, so a scaled rail would not be representative. Full size is only 198 mm long anyway. | The rest of the lid. The pad/bezel stub is clamped rigid, so the real frame adds some compliance: **real deflection ≥ coupon**. |
| Rear-shell span | Deflection = P·L³/(48·E·I·b): cubic in the span *L* | **The full 202 mm span**, the real 14 mm support bands, the 2.5 mm plate, the rib section and the insert/screw joint | Full width. The strip is 90 mm wide (3 rib pitches), narrower than the model's 101 mm effective width, so a centre point load is slightly **conservative** (the real plate spreads load wider). |

---

## Coupon A: solar rail cantilever

**Coordinates:** X runs along the rail. X = 0 is the rail's outboard end, which is lid x = 147. X = 198 is the inboard end, lid x = −51. Y runs across the rail, Z is up, and Z = 0 is the rail underside.

The lid mapping is:
- pad: X 0–28.5, lid x 147–118.5
- free cantilever: X 28.5–198
- stowed carriage: X 158–198, centre at X 178, which is **149.5 mm from the pad edge**
- deployed carriage: X 0–40
- travel: 158 mm

### Parts

| Part | Qty | Description | Bounding box (X × Y × Z, mm) |
|---|---|---|---|
| **A-R1**: rail, printed only (A1) | 1 | V1 rail cross-section, exact | 198.0 × 39.6 × 13.0 (includes the ear) |
| **A-R2**: rail with stiffener slots (A2) | 1 | Side walls thickened to host optional metal strips | 198.0 × 42.8 × 13.0 |
| **A-P**: pad / front-frame stub | 1 | Stands in for the bezel (2.5) + pad (3.5) under the rail; clamped to the table | 60.0 × 70.0 × 6.0 |
| **A-K**: carriage with load post | 1 | Runs in the channel; the post passes the top slot | 40.0 × 22.0 × 18.0 |
| **A-D**: display surrogate strip | 1 | Sits on the table under the cantilever, leaving a 1.0 mm gap | 170.0 × 30.0 × 5.0 |

### A-R1: rail cross-section (constant along X 0–196)

| Feature | Y range | Z range |
|---|---|---|
| Floor | 0 – 27.6 | 0 – 2.5 |
| Side walls (2.5 thick) | 0 – 2.5 and 25.1 – 27.6 | 2.5 – 10.5 |
| Channel interior (carriage space) | 2.5 – 25.1 (22.6) | 2.5 – 10.5 (8.0) |
| Top lips (retain the carriage) | 0 – 5.0 and 22.6 – 27.6 | 10.5 – 13.0 |
| **Top slot** (bracket passage) | 5.0 – 22.6 (**17.6**) | 10.5 – 13.0 |

- **Inboard end stop:** X 196–198, full solid section. It is the stowed carriage stop.
- **Outboard end (X 0):** open, for inserting the carriage. The deployed end stop is not part of this coupon.
- **Attachment ear** (candidate pad attachment, on the cable-corridor side):
  - solid block X 0–28.5, Y −12.0 to 0, Z 0–13.0
  - two M3 heat-set insert holes from the underside at (X 7.0, Y −6.0) and (X 21.5, Y −6.0), sized to the insert maker's datasheet (the model assumes Ø4.0 × 6.0 deep)
- The ear is where the rail meets the front frame in V1: beside the rail at lid x 118.5–147. The cable corridor keep-out ends at lid |x| ≤ 55, so the ear doesn't block it.

```
 A-R1 section (looking along X)          side view
     5.0   17.6 slot   5.0               X=0 (outboard)                 X=198
   ┌─────┐           ┌─────┐  Z13       ┌──────────────────────────────────────┐▌ end stop
   │ lip │           │ lip │  Z10.5     │ pad │← 149.5 to carriage centre →   ▓▓▓│
 ┌─┘     └───────────┘     └─┐          ├─────┤ free cantilever          carriage │
 │  channel 22.6 x 8.0        │          │base │ (1.0 mm over display surrogate)   │
 └────────────────────────────┘  Z0      └─────┘══════════════════════════════════╛ table
   ← 27.6 →   + ear 12 on the −Y side          X0   X28.5                 X158   X198
```

### A-R2: stiffener version (same as A-R1 except)
- **Side walls 4.1 thick:** outer width 30.8; lips (30.8 − 17.6)/2 = 6.6 wide; channel and slot unchanged (22.6 × 8.0 and 17.6).
- **Strip slot in each side wall:**
  - 2.3 (Y) × 10.4 (Z, from Z 1.3 to 11.7) × 196 (X 0–196)
  - open at X = 0, centred in the wall (0.9 skin each side)
- **Strips:** generic envelope, no final material chosen. Either 10 × 2 mm aluminium flat bar or 10 × 1.5 mm steel flat strip, cut to ~194 mm, slid in from X = 0 and held with tape.
- **Test in three states:** empty, 2 × aluminium, 2 × steel.

### A-P: pad / front-frame stub
- **Plate:** 60 (X −31.5 to 28.5) × 70 (Y −21 to 49) × 6.0.
  - Its inboard edge is at X 28.5, so the rail is free exactly where it leaves the pad.
  - Clamp zone: X −31.5 to −5.
- **Screw holes:** two Ø3.4 through-holes at (X 7.0, Y −6.0) and (X 21.5, Y −6.0). Underside counterbores Ø6.5 × 3.5 deep leave a 2.5 mm seat.
- **Screws:** M3 × 8 (2.5 seat + 5.5 into the insert).

### A-K: carriage with load post
- **Body:** 40.0 × 22.0 × 7.4, giving 0.3 mm clearance each side and on top inside the 22.6 × 8.0 channel. 0.5 mm edge chamfers.
- **Post:** 40.0 × 16.6 × 10.6, centred on the body, passing the 17.6 slot with 0.5 mm per side. The top is 7.5 mm above the rail top when seated.
- **Load hole:** Ø5.5 horizontal through the post (along Y) at X 20, 4 mm below the post top. A rod (M5 bolt or pencil) through it carries a bag of weights on both sides of the rail, so the load stays centred.

### A-D: display surrogate
- A 5.0 mm strip on the table, 1.0 mm below the rail underside (the rail sits on the 6.0 mm pad plate).
- Measure and record its actual thickness, since printing tolerance is about ±0.1.

---

## Coupon B: rear-shell span and joint

**Coordinates:** Y runs along the span. The support bands are Y 0–14 and Y 216–230, with the 202 mm clear span between them. X runs across the 90 mm strip width. Z is up; the frame base underside is Z = 0.

### Parts

| Part | Qty | Description | Bounding box (Y × X × Z, mm) |
|---|---|---|---|
| **B-F**: frame / front-frame stub | 1 | Base plate + two edge-beam shelves with inserts | 230.0 × 90.0 × 14.0 |
| **B-S**: cassette-clearance surrogate | 1 | Removable block whose top sits 1.0 mm below the plate | 60.0 × 60.0 × 9.0 |
| **B1**: plain plate | 1 | 2.5 mm plate, as-drawn V1 back | 230.0 × 90.0 × 2.5 |
| **B2**: ribbed plate (default h = 11) | 1 (+ optional h 6 / 8) | 2.5 mm skin + ribs | 230.0 × 90.0 × 13.5 |
| **B-L**: load pad | 1 | Spreads the centre load | 20.0 × 20.0 × 5.0 |

### B-F: frame
- **Base plate:** 230 × 90 × 4.0 (Z 0–4).
- **Shelves:** Y 0–14 and Y 216–230, full width, Z 4–14. Shelf tops at **Z 14.0** are the plate seat, as in the lid's edge beams.
- **Inserts:** four M3 heat-set inserts in the shelf tops at (Y 7, X 10) and (Y 7, X 80), mirrored at Y 223. That gives a **70 mm screw pitch**, as in the Concept C joint. Boss envelope Ø8 within the 14 mm band; hole to the insert datasheet.

### B-S: cassette-clearance surrogate
- A 60 × 60 × 9.0 block on the base at the bay centre (Y 85–145, X 15–75).
- Its top is at Z 13.0, which is **1.0 mm below the plate's inner face**: the real cassette clearance.
- It's removable so free deflection can be measured past 1 mm.

### B1: plain plate
- 230 × 90 × 2.5.
- Four Ø3.4 holes at (Y 7/223, X 10/80).
- Printed inner face down.

### B2: ribbed plate (dimensions are parameters)

| Parameter | Default | Notes |
|---|---|---|
| Skin | 2.5 | as the lid |
| Longitudinal ribs | 3 at X 15, 45, 75 (30 mm pitch) | run **Y 14–216 only**, i.e. over the span |
| Rib thickness | 2.0 | FDM minimum ~1.6 (4 × 0.4 mm perimeters) |
| Rib height h | **11** (screened minimum) | optional prints at 6 and 8 to measure the stiffness curve |
| Transverse ribs | 3 at Y 14, 115, 216, full width, same h and thickness | at both support edges and mid-span |
| Screw zones | Y 0–14 and 216–230 left rib-free | moment is ~zero over simple supports, so the ribs can stop at the support edge; screws are then accessible anywhere in the band |

- **Design note for Concept C:** in the real rear shell too, ribs can end at the edge-beam line. That frees the whole screw band.

```
 B side view (Y along span)
  Y0   Y14                         Y115                         Y216  Y230
  ┌────┬───────────── plate / ribs (B1 or B2) ───────────────────┬────┐  Z14..16.5(+h)
  │ ▣  │          load pad ▼ (centre)                            │ ▣  │  ▣ = M3 screw + insert
  │shelf  ...................[ B-S surrogate, top Z13 ]....... shelf │  Z4..14
  └────┴────────────────────────── base plate ────────────────────┴────┘  Z0..4
         ← clear span 202 →
```

---

## Printing (all parts)

- **Material:** PETG, 0.4 mm nozzle, 0.2 mm layers.
- **Solid parts:** the rails (A-R1, A-R2) and plates (B1, B2) must print **fully solid** (100 % infill, or perimeters filling the section). The model assumes solid sections.
- **Supports:** the stubs, frame, surrogates and carriage can use ≥ 40 % infill. No part needs supports.
- **Record** the slicer settings, filament brand, and each part's weighed mass (kitchen scale).

| Part | Orientation | Supports | Min wall/rib | Approx. PETG / time *(rough)* |
|---|---|---|---|---|
| A-R1 | floor down (Z up) | none; the 2.5 mm lips are short inward overhangs | 2.5 | ~40 g / ~2.5 h |
| A-R2 | floor down | none; slot roofs are 2.3 mm bridges | 0.9 skins around the slots | ~50 g / ~3 h |
| A-P | flat, counterbores down | none | — | ~30 g / ~1.5 h |
| A-K | body down, post up | none (Ø5.5 horizontal hole; teardrop it if needed) | — | ~12 g / ~0.7 h |
| A-D | flat | none | — | ~25 g / ~1 h |
| B-F | base down | none | shelf 14 | ~80 g / ~4 h |
| B-S | flat | none | — | ~30 g / ~1.5 h |
| B1 | inner face down | none | 2.5 | ~66 g / ~3 h |
| B2 (h 11) | **inner face down, ribs up** | none | ribs 2.0 | ~95 g / ~4.5 h |
| B-L | flat | none | — | ~3 g |

- **Minimum printer bed:**
  - Coupon A: ≥ 200 × 50 mm, so any 220 mm-class printer.
  - Coupon B: **≥ 235 mm in one axis** (230 mm parts). That is a 250 mm-class printer such as a common 250 × 210 or 256 × 256 machine. It won't fit a 220 × 220 bed.
- **Total:** roughly 0.45 kg of PETG and ~22 h of printing for everything, with one each of B2 h = 6 and h = 8 adding about 0.15 kg and ~7 h *(rough)*.
- **Hardware:**
  - 6 × M3 heat-set inserts: 2 for A, 4 for B, per supplier datasheet (no brand chosen).
  - 2 × M3 × 8 screws for A and 4 × M3 × 8 for B.
  - Optional flat strips for A2.
  - A rod, a bag, and weights or a kitchen scale.

---

## Test procedure (basic tools: caliper, ruler, known weights or kitchen scale, flat table, phone)

**General:**
- Test at room temperature.
- Measure each point **three times** and record the mean.
- Before testing, weigh the carriage and every load bag.
- For height readings, stand the caliper vertically. Rest the end of the main beam on the measured surface and drop the depth rod to the table beside the part. Tap lightly and read. The change from unloaded to loaded is the deflection.

### Coupon A: rail

**Setup**
1. Install the two inserts in the ear. Screw the rail to A-P with 2 × M3 × 8, snug (firm hand tightness; note what you used).
2. Clamp A-P to the table at X −31.5…−5 with a C-clamp. The rail must be horizontal and free past X 28.5.
3. Place A-D under the cantilever (X 30–198).
4. Check that a **1.0 mm feeler** just slides between the rail underside and A-D at X 100 and X 190. Record the actual gap: largest feeler that passes.

**A-1: load–deflection**
Carriage parked against the inboard stop (centre at X 178).

| Step | Hanging load (excluding carriage) |
|---|---|
| 0 | carriage only |
| 1 | 100 g |
| 2 | 200 g |
| 3 | **300 g** (representative cassette) |
| 4 | 600 g |
| 5 | **900 g** (≈ 3 g static equivalent) |

- **Measure:** rail-top height at **X 190** and **X 100**, and at **X 30** (just past the pad).
- **After step 5:** remove the load and re-measure all three to record permanent set.
- **Contact check:** at each step, check whether a 0.5 mm feeler and paper still pass under the rail at X 178–198. Take a phone macro photo of the gap at 300 g and 900 g.
- **A2 only:** repeat with the strips inserted. Optionally add 1.5 kg and 2.0 kg to get measurable deflections for the steel version.

**A-2: pad/attachment movement**
- The height change at X 30 under 900 g is pad and attachment compliance.
- Also check, with 0.05 mm shim or paper, whether the rail lifts or gaps at its ear and pad interface under load.

**A-3: creep (optional but valuable)**
- Leave 300 g on the stowed carriage for 24 h.
- Record the X 190 height at 0 h, 1 h and 24 h, and again 1 h after unloading.

**A-4: slide smoothness**
- **By hand:** push the empty carriage over the full 158 mm travel (X 158→0 and back) 10 times. Note any binding points by X position.
- **Tilt test:** lift the free end of the table or board until the carriage starts sliding by itself. Read the angle θ with a phone inclinometer; friction μ ≈ tan θ. Do it 3 times empty and 3 times with 300 g hung.

**A-5: carriage retention**
- **Pull test:** with the rail held upside down (clamped or held over the table edge), hang 1.0 kg from the carriage, then 2.0 kg if the first holds. The carriage must not pull through the 17.6 slot.
- **Lips:** measure the slot width at X 50 and X 150 before and after. Any increase above 0.1 mm counts as lip yield.

**Pass/fail signals**

| Test | Pass | Marginal | Fail |
|---|---|---|---|
| Deflection at the carriage, 300 g | ≤ 0.5 mm | 0.5 – 1.0 | ≥ 1.0 (touches display) |
| 900 g (3 g equivalent) | no contact; 0.5 mm feeler passes | paper passes, 0.5 doesn't | contact |
| Pad movement at X 30, 900 g | ≤ 0.05 mm | 0.05 – 0.15 | > 0.15 |
| Permanent set after 900 g | ≤ 0.05 mm | — | > 0.05 |
| Slide | no binding over 158 mm | local catch | jams |
| Tilt angle | *(no provisional limit yet; this run records the baseline)* | | |
| Retention | holds 2 kg, no lip yield | holds 1 kg | pulls through < 1 kg |

**Record for A:** part masses, slicer settings, actual gap, a table of load vs height at X 30, 100 and 190 for A1, A2-empty, A2-Al and A2-steel, contact yes/no, creep readings, tilt angles, retention result, and slot widths before and after.

### Coupon B: rear shell

**Setup**
1. Install the four inserts in B-F.
2. Place B-S at the bay centre.
3. Seat the plate: flat face down for B1; inner face down with ribs up for B2.
4. Screw it down with 4 × M3 × 8, snug.
5. Check that the unloaded gap between the plate underside and B-S accepts a 1.0 mm feeler. Record the actual gap.

**B-1: load–deflection with the surrogate removed** (measures true stiffness)
- Measure the top-surface height at the centre line (Y 115). For B2, measure on a side-rib top at X 15, Y 115, beside the load pad.
- Also measure at Y 20 and Y 210, next to the supports, to capture support or joint settling.

| Plate | Loads on B-L at the centre (Y 115, X 45) |
|---|---|
| B1 | 0, 100 g, 200 g (≈ 1, 2 N). **Stop if the deflection exceeds 5 mm.** |
| B2 | 0, 0.2, 0.5, 1.0, **2.04 kg (20 N)** |

- Unload and re-measure to record permanent set.

**B-2: clearance check with the surrogate in place**
- Apply 20 N (2.04 kg) at the centre.
- **B2 pass** if a 0.5 mm feeler still slides between the plate and B-S.
- **B1:** record the load at which it first touches B-S (expected almost immediately).

**B-3: joint**
- **Unscrewed baseline:** repeat B-1 on B2 with the screws removed (plate just resting), to see how much the screwed supports stiffen it.
- **Service cycles:** 10 screw-in/out cycles on one insert. Note any spinning, pull-up, or thread wear.
- **Seating under load:** under 20 N, check with a 0.05 mm shim or paper whether the plate lifts from a shelf.

**B-4: creep (optional)**
- Leave 20 N on B2 for 1 h. Read at 0, 10 and 60 min, then 10 min after unloading.

**Pass/fail signals**

| Test | Pass | Marginal | Fail |
|---|---|---|---|
| B2 at 20 N | ≤ 0.5 mm (0.5 mm feeler passes) | 0.5 – 1.0 | touches B-S |
| Plate lift at supports | none (0.05 shim doesn't enter) | — | visible lift |
| Insert after 10 cycles | holds, no spin | slight pull-up | spins or pulls out |
| Permanent set | ≤ 0.05 mm | — | > 0.05 |

**Record for B:** part masses, rib height as printed (measured), actual reference gap, load vs centre and near-support heights (screwed and unscrewed), feeler results, joint observations, creep.

---

## Expected observations (current screening model, E = 2000 MPa, solid sections)

**Coupon A.** Deflection at the stowed carriage centre, 149.5 mm from the pad edge, including a 12 g carriage:

| Rail | carriage only | +100 g | +200 g | **+300 g** | +600 g | **+900 g** | 1.0 mm reached at |
|---|---|---|---|---|---|---|---|
| A1 printed | 0.03 | 0.25 | 0.47 | **0.69** | 1.36 | **2.03** | +0.44 kg |
| A2 empty | 0.02 | 0.20 | 0.37 | 0.54 | 1.07 | 1.59 | +0.56 kg |
| A2 + 2 × Al 10×2 | 0.00 | 0.04 | 0.08 | **0.11** | 0.22 | **0.33** | +2.75 kg |
| A2 + 2 × steel 10×1.5 | 0.00 | 0.02 | 0.04 | **0.06** | 0.12 | **0.18** | +5.2 kg |

- A1 is expected to be **marginal at 300 g** and to **touch the display surrogate at about 440 g**, so it fails the 900 g check.
- Either A2 stiffener version is expected to pass comfortably.
- The rail's own weight is not included; it is small, a few hundredths of a mm.

**Coupon B.** Centre deflection of the 90 mm strip over the 202 mm span:

| Plate | 2 N | 5 N | 10 N | **20 N** | 1.0 mm reached at |
|---|---|---|---|---|---|
| B1 plain 2.5 | 1.47 | 3.66 | 7.33 | **14.65** | 1.4 N |
| B2 h 6 | 0.22 | 0.55 | 1.09 | 2.19 | 9.2 N |
| B2 h 8 | 0.12 | 0.29 | 0.59 | 1.17 | 17.0 N |
| **B2 h 11** | 0.06 | 0.14 | 0.28 | **0.55** | 36 N |

- B1 is expected to bottom out on the clearance block at a very light touch.
- B2 h 11 is expected at the criterion (about 0.5 mm) at 20 N.

**Likely direction of error** *(inferred)*:
- Printed PETG usually behaves stiffer or softer than the nominal 2000 MPa depending on layers and temperature, so a spread of about ±30 % is plausible.
- The real rail pad and the real edge beams are less rigid than the clamped coupon stubs.

Treat the measured-to-predicted ratio as the **calibration factor** for the P0.1 models.

---

## How the results change the NOMAD design

| Outcome | Design consequence |
|---|---|
| A1 passes (≤ 0.5 mm at 300 g, no contact at 900 g) | Printed rails are adequate. No stiffener; the V1 rail width stays 27.6. |
| A1 fails, A2 + strip passes | Adopt a replaceable metal stiffener strip in each rail: side walls 4.1, rail width 30.8 (+3.2). Re-space the rails, the 8 mm corridor and the loops in Y (room exists). Add stiffener parameters to `nomad.yaml` as working inputs. |
| A2 fails, or pad movement dominates | The attachment or pad, not the rail, is the weak link. Redesign the pad attachment (longer pad, through-bolts), add display-protection clearance (rail layer +thickness), or reconsider intermediate support. That needs a loop/corridor re-layout and would be an architecture question, brought back for review. |
| Slide binds or μ is high | Adjust CLEARANCE (0.3 working) and the carriage chamfers or wear strips; re-test. |
| Retention < 1 kg or lips yield | Widen the lips (larger carriage, or a smaller slot via a narrower bracket) or use metal wear/retention strips. |
| B2 h 11 passes with margin | Screen a lower rib height (h 8 measured) to recover lid thickness; update the rib working value. |
| B2 h 11 marginal or fails | Taller ribs, or more cassette clearance (thickness trade from Round B.2), or a sandwich back plate. Update the lid thickness working input. |
| Joint lifts, or inserts spin or pull | Larger bosses or longer inserts, more screws (e.g. 50 mm pitch), or a tongue-and-groove locating edge. |
| Measured/predicted ratio ≠ 1 | Apply it as E_eff in the screening tools and re-run the Round B.2 comparisons with calibrated values. |

Results go to `docs/build-log.md` as **physically tested / measured**, and the calibrated values feed P0.2 (the physical-measurement revision).
