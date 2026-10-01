# Round E — Solar Tilt Index Lock: Implementation (D-009)

**Status:** approved by the owner on 2026-09-28 and implemented in `nomad.yaml`, the spec, the E-lid generator and the local FeatureScript. Validated locally and in an Onshape scratch Part Studio. **The persistent Onshape Feature Studio has NOT been updated.**
- **Why not:** the approved ±80° structural hard stops could not be packaged (§8). This is an unresolved critical item, and the owner's precondition for the persistent write is that none remains.
- No Git commit or push.

**Design basis (analysis records, unchanged):**
- `round_e_solar_index_lock_investigation.md` (concept C1);
- `round_e_solar_index_lock_manufacturing_check.md` (option D: Ø1.5 hardened pin, stainless plate, double-D key + M2 clamp);
- `round_e_solar_hub_pin_anti_rotation_check.md` (option C: captured anti-rotation plate + Ø3 dowel);
- `round_e_solar_hub_load_check.md` (loads).

F3 Option B hub geometry is unchanged.

**Evidence levels:**
- Geometry and clearances: *modeled*. Exact 2-D regions extruded along X, swept over lid angle, slide and tilt. The kernel cross-check in Onshape is exact.
- Loads: *inferred*. Hand calculations with the conservative models of the approved reports; no FEA.
- **Nothing is physically tested.**
- Scratch scripts: `lockload.py` (load and stop numbers) and the payload minifiers are in the session scratchpad, not the repository. Every formula they use is written out here or in the approved reports.

---

## 1. Summary

| Item | Result |
|---|---|
| Index lock: 11 positions, −75…+75° in 15° steps, positive pin lock | **Implemented, validated (modeled)** |
| Ø1.5 hardened index pin in double shear (stainless sleeve + printed guide) | Implemented |
| Stainless index plate (1.5, R 11.75, 11 × Ø1.60 on r 10, A/F 3.0 key) | Implemented |
| Hub pin Ø5 × 53.5, round in bending, A/F 3.0 double-D at both ends, M2 both ends | Implemented |
| Anti-rotation plate + Ø3 × 24 dowel; pin axial retention | Implemented |
| Counter-hole metal sleeve | Implemented (derived, §6) |
| Spring (seating only), thumb slider, stow only at 0° | Implemented |
| **±80° structural hard stops** | **NOT PACKAGED. Open decision (§8)** |
| Load check at T_d = 1.26 N·m | Every implemented element ≥ SF 2 at room temperature (§10). Hot PETG margins as in the approved reports |
| Existing clearance suite, studies, F3 | Unchanged / identical |
| Onshape | Scratch cross-check exact. Persistent write **withheld** |

## 2. What changed

| File | Change |
|---|---|
| `CAD/parameters/nomad.yaml` | 41 new parameters, all status TBD with working values or formulas (block "D-009"). `SOLAR_TILT_STOP_ANGLE` has no working value (unresolved) |
| `docs/mechanical-spec.md` | New subsection "Solar tilt index lock and hub-pin anti-rotation (D-009…)": architecture, materials, one row per parameter |
| `CAD/tools/region2d.py` | **New.** Exact 2-D regions (line and arc edges, holes): distance, containment, rotation. Used for the double-D keys, plates and profiles |
| `CAD/tools/e_lid_layout.py` | See below |
| `CAD/tools/f3_investigation.py` | Compares against the E2 model without the lock (`PARTS_E2`), so its published output stays byte-identical |
| `CAD/featurescript/NOMAD_E_Prototype.fs` | Regenerated GENERATED PARAMS and GENERATED E LID LAYOUT blocks (46 lid parts). New profile builder `nomadELidPrim` (sketch + extrude for key and plate outlines). Stainless appearance. Header / info note about D-009 and the missing stops. **Local only (§15)** |
| `CAD/featurescript/NOMAD_E_Prototype.e2.test.fs` | Regenerated expected data (398 near pairs, 27 posed clearances) |
| `CAD/featurescript/NOMAD_P01.fs` | GENERATED PARAMS regenerated (new YAML entries; no P0.1 geometry change) |
| This report; `docs/decisions.md` (D-009); `docs/build-log.md`; `round_e_digital_prototype.md`; `CLAUDE.md`; `CAD/README.md` | Documentation |

**`e_lid_layout.py` changes:**
- The lock part set comes from YAML formulas (`DERIVED_LOCK`).
- New `prof` primitive (exact profile prisms).
- `PARTS_E2` (the 26-part E2 lid, kept for the studies) alongside `PARTS` (46 parts with the lock).
- Guided-fit rules for the new running fits.
- Lock checks A–G (§9), called from `main`.
- Posed kernel checks for pin–plate, plate–cassette and plate–bracket.

Historical analysis reports are not edited.

## 3. Implemented mechanism

Per side (right shown; the left is the right rotated 180° about the lid's vertical centre line, i.e. mirrored in X and in dy):

1. **Torque path when locked:** cassette tray → stainless counter sleeve + printed guide → **Ø1.5 index pin** (double shear) → **index plate** (keyed on the hub-pin tip) → **Ø5 hub pin** (torsion) → **anti-rotation plate** (keyed on the pin's inboard end) → **Ø3 dowel** → PETG carriage → rail → lid. Metal throughout up to the dowel bearing.
2. **Bending path (unchanged from F3):** cassette → hub bracket bore → pin (round Ø5) → carriage bore (root at the carriage outboard face).
3. **Axial retention:** the anti-rotation plate sits in a 1.6 slot in the carriage. The pin shoulder and the inboard M2 screw + washer clamp it, so the pin is held both ways with a float of +0.1/−0. At the tip, the index plate is clamped on the double-D shoulder by the second M2 screw + washer.
4. **Operation:**
   - The user pushes the thumb tab 6 mm outboard, which retracts the pin 1.0 mm clear of the plate.
   - The user turns the cassette and releases the tab. The spring re-seats the pin in the next hole.
   - The spring only seats the pin. It never carries torque.
5. **Stow:** only the 0° position slides back into the lid. At any other position the cassette meets the lid side wall within about 7 mm of travel (modeled, §7).

## 4. Exact geometry (modeled, right side)

**Frame:**
- **X:** lid-frame X with the solar system stowed. The cassette inboard edge (hub face) is at X 0.5; the carriage spans X −51 … −11. Deployed, every moving part is at X + 158.
- **dy / dz:** offsets from the tilt axis (right: Y 131.8, Z 57.5; left: Y 103.2).
- **Tilt:** positive about +X.
- **Angles:** measured in the YZ plane from +dy toward +dz.

### 4.1 Hub pin and anti-rotation (carriage group)

| Part | Geometry |
|---|---|
| Hub pin, 303/304 cold-drawn, Ø5 × **53.5** | X −41.0 … +12.5. Inboard double-D **A/F 3.0** (flats ±Y) X −41.0 … −39.5; round Ø5 X −39.5 … 11.0; tip double-D **A/F 3.0** X 11.0 … 12.5; M2 tapped both ends |
| Anti-rotation plate, 1.5 stainless | X −41.0 … −39.5 (10.0–11.5 inside the carriage inboard face). Outline dy −7.5 … 2.8 × dz −5.4 … 1.0, plus the tab dy −4.9 … 2.8 × dz 1.0 … 3.8. Key hole A/F 3.0 on the axis; dowel hole Ø3 at (−5.0, −2.5). **Ligaments:** key–edge 1.3, dowel hole–edge 1.0, dowel hole–key 2.04 |
| Carriage slot | X −41.0 … −39.4 (1.6). Profile = plate + 0.1, open to the −Y side face (covered by the rail wall). **PETG skins:** 0.5 to the carriage bottom, 0.6 to the cable envelope (dy 3.5), 0.6 to the boss top |
| Carriage bores | Access Ø5.5 X −51 … −41 (inboard screw); pin bore Ø5 X −39.4 … −11 (28.4 engaged) |
| Dowel Ø3 × 24 | At (−5.0, −2.5), X −50.0 … −26.0 (recessed 1.0 from the inboard face, §11). Bore X −51 … −26; push-out Ø2 X −26 … −11 |
| Screws / washers | M2 head envelope Ø3.8 × 2 and Ø5 × 0.3 washer at X −43.3 … −41.0 (in the access bore) and 12.5 … 14.8 (tip) |

### 4.2 Index plate (carriage group)

- **Position and material:** X 11.0 … 12.5; 1.5 stainless.
- **Outline:**
  - an arc R **11.75** from −25.2° to 152.1°;
  - a line at dz 5.5 back to dy −5.0;
  - a line at dy −5.0 down to dz −5.0 (bracket-bottom plane, 1.0 above the rail floor);
  - a line at dz −5.0 back to the arc.
- **Holes:** 11 × **Ø1.60** on **r 10** at **−17.5° … 132.5°**, step 15° (at 0° tilt); key hole A/F 3.0.
- **Ligaments:** edge 0.95, web 1.01.

### 4.3 Cassette interface (cassette group; tray = cassette at dz ≥ 5.5)

| Feature | Geometry |
|---|---|
| Index groove | X 10.5 … 13.0; box dy ±12.0 × dz 0 … 12.0 (tray skin above 1.5). Plate running clearance: radial 0.25 (all tilts), axial 0.5 each side |
| Index pin Ø1.5 × 16, ISO 8734 hardened | Axis at (5.373, 8.434), i.e. r 10 at 57.5° in the cassette frame. Engaged X 7.5 … 23.5; retracted X 13.5 … 29.5 |
| Counter sleeve (§6) | OD 2.5 × ID 1.6 × 4.0, X 6.5 … 10.5. Seats on a 0.45 shoulder; grit relief Ø1.6 X 0.5 … 6.5 (open at the cassette inboard edge) |
| Guide bore | Ø1.6, X 13.0 … 19.0 (printed, reamed) |
| Slider | Carrier 3.6 × 3.6 × 4.0 at X 21.5 … 25.5 (grips the pin's outer 2 mm). Thumb tab 1.5 × 2.0 at X 22.5 … 24.5, reaching to 0.3 above the cassette rail-side face |
| Spring channel + cover | Channel 3.8 square, X 19.0 … 40.5, open to the rail-side face. The cover closes it: floor dz 5.5 … 6.53, spring seat X 37.5 … 40.5, tab slot X 22.4 … 30.6 (stroke + 2 × 0.1) |
| Spring | Envelope Ø3.4. X 25.5 … 37.5 engaged (12); 6 retracted |

## 5. Hub pin, retention and anti-rotation

Built as specified in the anti-rotation check §11, with the owner's decision to use **A/F 3.0 at both ends** (the tip was A/F 3.5 in the manufacturing check).

**Pin length:**
- Derived: `SOLAR_RAIL_ENGAGEMENT − SOLAR_ANTIROT_PLATE_INSET + SOLAR_HUB_LINK_LENGTH + SOLAR_BRACKET_LENGTH + SOLAR_INDEX_GROOVE_CLEARANCE + SOLAR_INDEX_PLATE_THICKNESS` = 40 − 10 + 11.5 + 10 + 0.5 + 1.5 = **53.5**.
- This is the same as the anti-rotation check's estimate.

**Key fit (modeled):**
- Turning the pin 0.05° in the anti-rotation plate overlaps by 0.0017 mm; turning the plate about the pin overlaps the dowel by 0.0033 mm. So the model has no free play.
- The physical play comes from tolerances (A/F 3.00 −0.02/0 in +0.02/0: ≤ 0.04 → ≤ ±0.6° at the flat, clamped out by the screw).

**Axial float:**
- +0.10 (contact at +0.10, overlap at +0.11) and 0 inward (the key shoulder and washer are captured).
- Dowel engagement: 9.0 inboard / 13.4 outboard of the plate.

## 6. Counter-hole sleeve (derived)

**Why a sleeve:**
- The anti-rotation check (§12) found the 3 mm PETG counter-hole to be the next weakest printed link: 14.0 MPa at T_d, SF 2.14 at room temperature, **1.07 hot**.
- The owner approved a metal sleeve.

**Derivation:**

| Quantity | Value | Reason |
|---|---|---|
| ID | 1.60 (+0.05/0) | Same as the index holes (`SOLAR_INDEX_HOLE_DIAMETER`), pin Ø1.5 m6 |
| OD | **2.50** (h7) | Largest that keeps 1.68 mm of PETG to the tray bottom face and 3.8 to the tray top at the pin position (r 10 / 57.5°). Wall 0.45 |
| Length | **4.0** = engagement 3 + MIN_GAP 1 | The pin engages 3; the last 1 mm is a grit reserve so the tip never bottoms |
| Seat | 0.45 shoulder, Ø1.6 grit relief through to the cassette inboard edge | Axial location; debris exits instead of packing |
| Fit | Press into a reamed PETG bore Ø2.50 −0.02…−0.05 | Retained by interference; the pin load is radial |
| Part | Precision stainless tube 2.5 × 0.45 wall, cut to 4.0 and deburred, or a turned bush | Standard stock |

**Effect (inferred, T_d):**
- The pin bears on steel at 14 MPa.
- The sleeve spreads the load on PETG to **6.3 MPa**: SF 4.76 at room temperature, **2.38 hot** (was 2.14 / 1.07).

## 7. Index pin, spring, slider and stow interlock

**Engagement:** 3 mm into the sleeve. Stroke 6 = 3 + 0.5 + 1.5 + MIN_GAP 1 (formula). Retracted, the tip is 1.000 from the plate (modeled).

**Spring:**
- Envelope Ø3.4 in a 3.8 channel. Installed length 12, retracted 6. **0.6 N** engaged (seating only), about 1.5 N retracted, so the rate is ≈ 0.15 N/mm and the free length ≈ 16.
- Feasible example (inferred): 302 stainless, wire 0.28, ≈ 11.6 active coils, solid ≈ 3.8 (< 6), τ ≈ 613 MPa at 1.5 N.
- Wire 0.30 would reach solid 5.3, too close to the 6 mm retracted length.
- Rate and free length are not parameters yet; they are chosen with the spring (TBD).

**Slider:**
- A printed carrier grips the pin's outer end, with a 1.5 × 2 thumb tab exposed on the cassette's rail-side face near the hub.
- The user pushes it outboard 6 mm.
- The tab sits 0.3 inside the face, so it doesn't snag when stowed.

**Stow interlock:**
- Slide the right cassette inward from deployed at lid 105° and find the first MIN_GAP violation (modeled):
  - at 0° it enters fully;
  - at every other index position it is blocked at **7.1 mm**. The cassette meets the lid side wall, and the rail cannot carry it in.
- This is geometric; there is no dedicated interlock part (see §14).

## 8. ±80° hard stops — required, NOT packaged (open decision)

**Requirement:**
- Structural stops at about ±80°, not spring, gear or friction.
- They protect the solar cable when the index pin is held retracted and the cassette is turned past ±75°.

**Finding:**
- **No stop fits the approved parts and envelope with SF ≥ 2.**
- With the pin retracted, the model shows no collision up to ±90° (check B). **The cassette can over-rotate and wind the cable.** Only the engaged index pin limits rotation.
- `SOLAR_TILT_STOP_ANGLE` is unresolved (no working value) and nothing is modeled for it.

**Stop force** at the contact radius r (inferred): F = T / r.

| r (mm) | T_h 0.63 N·m | T_d 1.26 N·m |
|---|---|---|
| 2.5 | 252 N | 504 N |
| 3.5 | 180 N | 360 N |
| 5 | 126 N | 252 N |
| 7 | 90 N | 180 N |
| 10 | 63 N | 126 N |

### 8.1 Why each location fails (modeled geometry, inferred stresses)

1. **Index-plate plane (X 11–12.5).**
   - The fixed plate fills every point within R 11.75 above dz −5 in the rail-slot band. The rotating tray groove clears it by only 0.25, so no rotating feature can meet the plate.
   - The plate would need a ≥ 160° notch or arc slot:
     - In the outer band (R 10.8–11.75) such a slot opens every index hole.
     - Inside the hole circle, it leaves the key hub joined through less than 200° by a ≈ 2 mm ring. The key-flat reaction is ≈ 470 N per flat at T_d, giving ≈ 1,400 MPa ring bending (order of magnitude) against 758 yield.
2. **Retracted index pin.** It is 1.0 clear of the plate by design, and the tray is solid outboard of the groove (guide bore). There is no room for a fixed ear it could meet.
3. **Link (X −11 … 0.5), where the cable twists.**
   - The Ø6 cable envelope (centre R 6.5, annulus R 3.5–9.5) twists through the full tilt. It sweeps ±(80 + 27.5) = ±107.5°, leaving 145° of the annulus.
   - A fixed-arm / rotating-lug pair in that annulus would need the lug to cover the cable's own ±27.5°: a contradiction.
   - Inside R 3.5 there is only a 1 mm ring around the pin. A lug at r 3 (420 N at T_d) on a ≈ 2 × 1 arm spanning the 11.5 link gives ≈ 14,000 MPa.
   - Outside R 9.5 the stowed envelope (rail channel dy −7.8 … 14.8 below dz 2, slot band above, the other stowed cassette at dz 5.5) has no room at the required angles.
4. **Bracket plane (X 0.5–10.5).**
   - The bracket fills the rail-slot band (dy −5 … 12, dz −5 … 5.5) with 0.3 clearance, and the only fixed part inside it is the pin (the bearing).
   - A key in the bore would work at r 2.5 (504 N at T_d) and would cut the pin just outboard of its root, where the pin margin is 2.09.
5. **Lid side wall (deployed).**
   - A lug on the bracket reaching into the wall notch: the wall is open above dz 4.5 (the cassette slot), so it can only stop downward or sideways motion.
   - Searching every lug position that fits the stowed link envelope and avoids the cable sweep: **0 positions** stop within 77.5–85° on both sides. The best two-sided point stops at −54.5° / +135°.
6. **Cassette against the lid or rail:** no contact up to ±90° (check B).

### 8.2 Options (not implemented; for the owner)

| Option | What | For | Against |
|---|---|---|---|
| **S1. Outboard stop (recommended to study)** | A fixed stop element keyed with the index plate on the pin tip (a formed flange on the plate's lower edge, or a separate stacked stop plate on an extended tip), met by a **steel-faced stop block hanging from the tray** just outboard of the groove (X 13 … ≈ 21, clear of the thumb tab at X ≥ 22.4). Contact at R ≈ 6–7 → ≈ 180–210 N at T_d | Uses the free space below the tray outboard of the plate. Loads the same metal torque path as the lock (key SF 2.41). A steel facing spreading into the tray keeps PETG at ≈ 6 MPa (SF ≈ 5 RT / 2.5 hot) | New parts: a tray stop insert, plus a flange (forming step) or a thicker stop plate with a longer tip (pin > 53.5). The flange puts an out-of-plane moment on the 1.5 plate (≈ 390 MPa for an 8 mm flange, SF ≈ 2, so it needs detailing). Only 5° between ±75 and ±80 (≈ 0.5–0.6 mm at R 6–7), and ±0.1 mm of tolerance moves the stop by ≈ ±1° |
| S2. Re-route the cable out of the link annulus | Take the solar lead outside R 9.5 (or through a different path), then place a fixed arm on the carriage end and a lug on the bracket | A classical stop at a good radius | Changes the D-009 cable path, which is already an open item (in-cassette exit route not modeled). Link and lid-wall notch changes |
| S3. Defer structural stops to P0.2 | Keep the lock as the only limit in P0.1, and mark the ±75° ends on the cassette | No new parts now | The cable is unprotected when the pin is held retracted, which contradicts the approved requirement. Needs an explicit owner waiver |

**Recommendation:**
- Approve a focused **S1 study**: geometry in the generator, load check, packaging sweep.
- Then write the persistent Feature Studio once the stops pass.
- If the persistent model is wanted before that, it needs an explicit waiver (S3, interim).

## 9. Validation (modeled)

**Local suite:** `py CAD/tools/e_lid_layout.py --write`, then `--check` (exit 0).
- Result: **ALL CHECKS PASSED**.
- Known items are reported, not hidden: the rear-plug OPEN CONFLICT; F3 resolved by option B; **D-009 ±80 hard stops NOT PACKAGED (open)**.

| # | Check | Result |
|---|---|---|
| A | Index positions −75 … +75 (both sides, lid 105°, deployed) | Pin-to-hole 0.050 at all 11 (design 0.05). The pin spans the plate and both groove gaps. At every half-step the engaged pin overlaps the plate: positive lock, it must be retracted to turn |
| B | Retracted pin, tilt −90 … +90 in 2.5° steps | No collision inside ±75. Retracted pin to plate min **1.000**. **No geometric stop up to ±90** (§8) |
| C | Stow interlock (right cassette slid in from deployed, lid 105°) | 0°: enters fully. ±15 … ±75: blocked at 7.1 mm |
| D | Slide sweep 0 … 158 in 1 mm steps, tilt 0, lid 0° and 105°, right side vs lid | No violations |
| E | Hub pin | Key rotation 0.05°: −0.0017 (no free play). Plate vs dowel: −0.0033. Axial float +0.10/−0. The pin + tip screw moved +0.05 against the plate overlap (captured). Dowel engagement 9.0 / 13.4 |
| F | Index plate | 11 holes at −17.5 … 132.5°, pitch 15.0. Plate to cable run 10.50. Plate to its rail floor over the full travel **1.000** |
| G | Counter sleeve | Wall 0.45, seated on a 0.45 shoulder. To the hub pin ≥ 6.25. To the cable pass-through inside the bracket (same frame) 4.18 |
| H | Clearance regression | Moving-part sweeps (lid 0/105/120/135 × stowed / R / L / both; tilts ±75 in 15° steps; slides 0…1): **0 unexpected violations**. Lid sweep 0–135 clean (min 1.000). F3 bracket–floor 1.000 over the full travel. Rear-plug conflict unchanged (−6.6 at 135°, below MIN_GAP from 121°) |

**Guided running fits** (minimum over all poses, need):

| Pair | Min | Need |
|---|---|---|
| Anti-rotation plate – rail | 0.300 | 0.3 |
| Cassette – index plate | 0.250 | 0.25 |
| Bracket – index plate | 0.500 | 0.5 |
| Bracket – rail | 0.300 | 0.3 |
| Index pin – index plate | 0.050 | 0.05 |
| Index plate – sleeve | 0.500 | 0.5 |
| Index plate – rail | 0.300 | 0.3 |

**Reproducibility:**
- Every published study output (hinge, skeleton ×2, V1, B.2, coupons ×2, C.1, C.2, D, D.1, P0.2, base V0.1) is **byte-identical** to the post-F3 baseline. `hinge.txt` differs only in the output path it prints.
- `f3_investigation.py` output is byte-identical.
- `yaml_to_featurescript.py --check`: `NOMAD_P01.fs` block up to date.

**Onshape scratch kernel cross-check** (test build of the regenerated `NOMAD_E_Prototype.fs` + the E2 harness):

`E2 n75 mc10 L0 S0/398 c396 dv0 m0 P0/27 pd0`

- 75 solids (29 base + 46 lid), each a single body.
- All 398 pair states match; the 396 compared distances are exact (to 0.001).
- The 10 mate connectors are exact.
- All 27 posed clearances pass, including pin–plate 0.05, plate–cassette 0.25/0.5 and plate–bracket 0.5 at 0°, +75/−75 and −30/+45.

Two earlier runs failed on test-payload issues only; neither was a geometry fault:
- `LE_… − 0` on unit values, fixed in the generator: a zero offset now returns the base expression.
- An empty display name in the minified harness, a harness-only fix.

## 10. Integrated load check (inferred; T_d = 1.26 N·m, acceptance SF ≥ 2 = no yield at 2.52 N·m)

**Models:** those of the approved reports. The index-pin force is F = T/r = **126 N** at r 10. The dowel force is T/5.59 = **225 N**.

| Element | Model | Stress at T_d | Allowable | SF |
|---|---|---|---|---|
| Index pin Ø1.5, bending | Span 0.5 + t + 0.5 + 2 × 1.0; M = F(L/4 − t/8) | 357 MPa | ≥ 1,000 (ISO 8734 hardened) | **2.80** |
| Index pin, double shear | F / (2πd²/4) | 36 MPa | — | ≫ 2 |
| Index plate, bearing | F/(d·t) | 56 MPa | 758 (301 ½-hard) | 13.5 |
| Index plate, web 1.01 bending / shear | (F·h/8)/(t·w²/6); F/(2wt) | 99 / 42 MPa | 758 | **7.7** / ≫ 2 |
| Tip key A/F 3.0 in the index plate | p = 6T/(t·w_f²), w_f 4.0 | 315 MPa | 758 / 725 (17-4PH) | **2.41 / 2.30** |
| Anti-rotation plate key A/F 3.0 | Same | 315 MPa | 758 / 725 | **2.41 / 2.30** |
| Anti-rotation plate, dowel hole | Bearing 225/(3 × 1.5); shear-out of the 1.0 ligament (Y component 101 N) and the 1.4 ligament (Z 201 N) | 50; 34 / 48 MPa | 758; τy ≈ 440 | ≫ 2 |
| Hub pin root, round Ø5 (bending + torsion) | Anti-rotation check §5.1 | vM 198 | 415 (303) | **2.09** |
| Hub pin double-D A/F 3.0, both ends (torsion only) | Same | vM 170 | 415 | **2.44** |
| Carriage PETG under the Ø3 dowel | Beam on elastic foundation, k 1,000–2,500 N/mm²; infinite p = Fβ/2d, bound p = Fβ/d | 5.0–6.3 (infinite); **10.1–12.7** (bound) | 30 RT / 15 hot | RT **2.36–2.97** (bound), 4.7–5.9; hot 1.18–1.49 (bound), 2.4–3.0 |
| PETG shear-out under the dowel | Anti-rotation check §5.6 | 4.3 MPa | 10 (interlayer) | 2.3 |
| Counter sleeve on PETG (§6) | (F/2)/(OD × L) | 6.3 MPa | 30 / 15 | **4.76 / 2.38** |
| Index pin in the sleeve (steel) | (F/2)/(d × 3) | 14 MPa | — | ≫ 2 |
| Guide bore, PETG, 6 mm | (F/2)/(d × 6) | 7.0 MPa | 30 / 15 | 4.29 / 2.14 |
| Spring | Seating only, never structural | — | — | — |
| **Hard stops** | **Not packaged** | — | — | **— (§8)** |

**Integration effects:**
- **Dowel recessed 1.0:** engagement 9.0 / 13.4 instead of 10.0 / 12.4. With 1/β = 5.9–7.4 mm, neither side is "infinite". The conservative bound (p = Fβ/d, the end-loaded semi-infinite case) still covers it, so the bound SF is unchanged.
- **Anti-rotation plate ligaments:** 1.0 (dowel hole–edge) and 2.04 (dowel hole–key), against 1.1 / 2.4 in the approved sketch, because the outline is now derived from the carriage clearances (§11). Shear-out SF stays far above 2.
- **Tip key A/F 3.5 → 3.0:** tip-key SF rises from 1.92 to 2.41, and the tip section torsion SF is 2.44.

**Failure order at room temperature** (multiples of T_d to first yield, inferred): pin root 2.09 → carriage dowel bearing ≥ 2.36 (bound; ≈ 5 likely) → keys 2.30–2.41 → index pin 2.80 → sleeve PETG 4.76.

**Hot (60–70 °C):** below 2 only for the dowel bearing on the conservative bound (1.18–1.49), which the approved anti-rotation check already accepted. The sleeve lifts the counter-hole from 1.07 to 2.38.

## 11. Deviations from the approved design

| Item | Approved | Implemented | Why |
|---|---|---|---|
| ±80° hard stops | Required | **Not packaged** | §8. Open decision |
| Anti-rotation dowel | Flush with the carriage inboard face (X 0 … 24) | Recessed **1.0** (X 1 … 25), push-out 25 … 40 | Flush, the dowel end touched the rail end stop at the stowed limit (moving-pair MIN_GAP rule). Recessed, the stow push stays on the PETG face, not the dowel end |
| Anti-rotation plate outline | dy −7.6 … 2.8; dz −5.4 … 1.6 below dy −4.8; to 3.8 above | dy −7.5 … 2.8; dz −5.4 … 1.0 below dy −4.9; to 3.8 above | Derived from parameters: 0.3 CLEARANCE to the rail wall, 0.1 slot clearance to the boss side, and MIN_GAP below the carriage top. Ligaments 1.0 / 1.3 / 2.04 (§10) |
| Tip key | A/F 3.5 (manufacturing check) | A/F 3.0 | Owner decision (same key both ends) |
| Counter-hole | PETG 2–3 mm | 3 mm engagement in a **stainless sleeve** 2.5 × 1.6 × 4 | Owner request, derived in §6. Stroke 6 (not 5) |
| Spring | ≈ 1 N preload (investigation) | 0.6 N engaged, ≈ 1.5 N retracted; OD 3.4, installed 12 | Fits the 3.8 channel. Seating only |
| Plate outer radius | R ≤ 12 (investigation) | R 11.75 | Manufacturing check §1: stays inside the rotating R 12 groove |

## 12. Manufacturing requirements

| Part | Requirement |
|---|---|
| **Index plate** | 301 ½-hard (ASTM A666) or 17-4PH (H1150), **not annealed 304/316**. 1.5 mm. Outline by laser / waterjet / milling. **11 holes Ø1.60 +0.04/0 drilled + reamed on CNC** (not laser-cut), true position Ø0.06 to the key. Key double-D A/F 3.00 +0.02/0, round R 2.50 +0.02. Deburred |
| **Anti-rotation plate** | Same stock, process and shop as the index plate (one drawing sheet, one order). Key A/F 3.00 +0.02/0. Dowel hole Ø2.99 +0.01/0 (light press on m6) at (−5.00, −2.50) ±0.03 |
| **Hub pin** | 303/304 cold-drawn or ground Ø5 (σy ≥ 415, not annealed). L 53.5. Both double-Ds A/F 3.00 −0.02/0 × 1.5 milled **in one setup** (flats parallel within 0.02). M2 × 4 tapped each end. **No flat along the length** |
| **Index pin** | ISO 8734 Ø1.5 × 16 m6, hardened (a stainless dowel has SF 1.16 in bending, which is not acceptable) |
| **Anti-rotation dowel** | ISO 2338 Ø3 × 24 m6 A1/A2, or ISO 8734 |
| **Counter sleeve** | Stainless tube OD 2.50 h7 × ID 1.60 +0.05/0 × 4.0, or a turned bush. Pressed into a reamed Ø2.50 −0.02…−0.05 bore |
| **Spring** | 302 / 17-7 stainless compression spring, OD ≤ 3.4, ≈ 0.6 N at 12 and ≈ 1.5 N at 6, solid ≤ 5 (e.g. wire 0.28) |
| **Screws** | M2 × 5 ISO 7380 / 4762 A2 + ISO 7089 M2 washers, both pin ends. Medium threadlocker, ≈ 0.15 N·m |
| **Printed parts (PETG)** | ≥ 4 perimeters, solid infill around every bore, slot and dowel hole. Carriage printed bottom-down. Dowel hole printed ≈ Ø2.8 then drilled / reamed Ø3.0. Guide bore reamed Ø1.6. Slots 0.1 per side |

## 13. Physical prototype requirements

1. **Anti-rotation coupon:** tests 1–7 of `round_e_solar_hub_pin_anti_rotation_check.md` §13 (2.52 N·m static, play, 65 °C hold, ±100 N axial, ramp to first yield, 20 × service, D-control).
2. **Index lock static:** 2.52 N·m for 1 min each way at 0°, ±45° and ±75°.
   - Pass: no slip; permanent set ≤ 0.2°; sleeve not displaced; plate holes not elongated (measure).
3. **Play:** ±0.1 N·m gives ≤ ±0.5° at the cassette.
4. **Hot:** 65 °C, 1.26 N·m for 1 h. Pass: drift ≤ 0.3°; guide bore and sleeve seat not ovalised.
5. **Cycling:** 1,000 engage / release cycles over all 11 positions, one-handed. Pass: no binding; spring force within 20 %; no pin or hole wear visible at 10×.
6. **Grit:** sand / dust in the groove; the pin must still seat at every position (grit relief works).
7. **Stow interlock:** try to stow at each non-zero position with 50 N. It must block with no damage, and slide freely at 0°.
8. **Plate inspection:** hole positions (true position Ø0.06) and reamed sizes on both plates before assembly.
9. **Cable over-rotation (until stops exist):** with the pin retracted, measure the torque and cable state at ±80° / ±90°. This characterises the §8 risk.

## 14. Remaining risks

| Risk | Level | Note |
|---|---|---|
| **±80° hard stops missing:** cable over-rotation with the pin held retracted | **Critical (open)** | §8. Blocks the persistent Onshape write |
| In-cassette cable exit route not modeled | Medium | The lock parts are clear of the assumed pass-through (sleeve 4.18 away). Must be checked when the route is defined |
| Hot PETG margins: dowel bearing 1.18–1.49 (bound), guide 2.14, sleeve 2.38 | Medium | As accepted in the anti-rotation check. Test 4 |
| Bearing-model spread for small pins in PETG (beam-on-foundation vs uniform) | Medium | Coupon tests 1 / 2 |
| Stow interlock is geometric (cassette against the lid side wall), no dedicated feature | Low–medium | Test 7. A visual 0° mark or chamfer may be wanted |
| Thin features: plate ligaments 0.95 / 1.0 / 1.01; PETG skins 0.5–0.6 around the carriage slot | Low | Drilled / reamed plates; skins are non-structural |
| Spring solid height vs the 6 mm retracted length | Low | Choose the wire (≤ 0.28) with the spring |
| Pin root SF 2.09 is the first metal element to yield | Low | Unchanged from the approved check. Cold-drawn 303/304 is required |

## 15. Onshape status and API

- **Persistent Feature Studio `NOMAD_E_Prototype` (element `40d4ae5868441bcb8882fe3a`): not written.** It still holds the post-F3 version (read back identical at API 140).
- The local snapshot `CAD/featurescript/NOMAD_E_Prototype.fs` is therefore **ahead of Onshape**. It is the validated D-009 candidate, and the only text that would be written.
- **Scratch validation:** exact (§9).
- **API:** **140 → 167** (27 requests: three `test_feature` runs of about 9 each; two stopped on test-payload faults before the passing run). 2,333 of 2,500 remain this cycle.
- No Assembly was created.

## 16. Decision required / next step

**Owner decision on the ±80° stops:**
- **S1** (recommended): a focused outboard-stop study.
- **S2**: re-route the cable.
- **S3**: a written interim waiver.

**Then:**
1. Implement the chosen option.
2. Rerun the suite and the scratch cross-check.
3. Read the persistent Feature Studio and confirm it matches the post-F3 baseline.
4. Write the complete local file, read it back and verify it is byte-identical.

Nothing further is done until the owner decides.
