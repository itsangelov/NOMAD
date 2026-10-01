# Round E — Solar Tilt / Index Lock Investigation (concept selection)

**Status:** analysis only. No change to `nomad.yaml`, the spec, FeatureScript, Onshape, CAD or Git. Awaiting owner approval.

**Baseline:** F3 Option B as implemented (hub/pin load check closed: `round_e_solar_hub_load_check.md`).

**Evidence levels:**
- Geometry and packaging: *modeled* (current `e_lid_layout.py` values).
- Loads and stresses: *inferred* (hand calculations; scratch script outside the repository; nothing tested).

**Recommendation:** an axial, spring-loaded hardened index pin in the cassette, in double shear, engaging a pin-keyed stainless index plate: **11 discrete positions at 15°**, one-handed thumb release (§8–§9).

---

## 1. Requirements

**Function:**
- ±75° tilt in 15° steps: −75, −60, …, 0, …, +75 (11 positions).
- Positive lock that holds the §3 torque with a safety factor ≥ 2; manual; no motor or servo; no continuous 360° rotation.
- Printed gears are never the structural path (D-004).
- The 0° position must hold the cassette flat for sliding in and out.

**Use:**
- One-handed; mechanically obvious; repairable with common hardware.
- No accidental release from a bump or vibration.

**Envelope:**
- No growth of the lid, cassette or rail.
- No change to F3 Option B: pin Ø5, bore 10, bracket wall 2.5, axis Z 57.5, 1.0 mm bracket-to-floor clearance.

## 2. Interface constraints (why the space is tight)

Coordinates relative to the tilt axis (Y 131.8, Z 57.5), right side; the left is mirrored.

| Region | Limits | Why |
|---|---|---|
| Rail-slot band: every part that rides along the rail when stowed | dy −5…+12, dz ≥ −5 | Bracket / slot envelope (Y 126.8–143.8) and 1 mm above the rail floor. Anything hub-mounted below the cassette travels here for 93 % of the slide |
| Cassette tray above the axis | dz +5.5…+13.5 (Z 63–71). A groove can go to dz +12, keeping a 1.5 mm skin | The axis is only 5.5 mm below an 8 mm cassette |
| Link region (between carriage and cassette) | Band only, and dz ≤ +4.5 | When stowed it sits under the *other* cassette |
| Solar cable | dy +3.5…+9.5, dz ±3 through the carriage, the link and the bracket's inboard part; the twist zone lies between the lid face and the cassette | Must not be crossed |
| Lid side wall near the deployed hub | Cut away by the cassette slot (Z 62–75.5) and the hub notch | No usable large-radius lid reference |

**Consequence.** The lock's fixed element must be keyed to the non-rotating hub pin. The pin is fixed in the carriage, and the rail stops the carriage rotating. The lock's moving element sits in the cassette. Both must lie within band ∪ tray.

The table below (*modeled*) is the largest contiguous arc available for the index-hole centres at radius r, including the hole plus a 0.75 mm wall:

| r (mm) | 8.0 | 9.0 | 9.5 | **10.0** | 10.25 | 10.5 | 11.0 | 12.0 |
|---|---|---|---|---|---|---|---|---|
| Arc for Ø1.5 holes | 145° | 152° | 154° | **156°** | 157° | 158° | 55° | 32° |
| Arc for Ø2.0 holes | 139° | 148° | 151° | 153° | 153° | 65° | 47° | 27° |
| 15° pitch (mm) | 2.09 | 2.36 | 2.49 | **2.62** | 2.68 | 2.75 | 2.88 | 3.14 |

Eleven positions need a **150°** arc. That is only possible at **r ≈ 9.5–10.5 mm**. Beyond about 10.5 mm the band's +Y edge (the slot fit) cuts the arc to under 65°.

The index radius is therefore about 10 mm, and **the 15° pitch is only about 2.6 mm**. This packaging fact drives the whole selection, far more than strength does. At r = 10 mm and Ø1.5 holes the arc runs from −20° to +136°, so the hole centres sit at **−17.5° … +132.5°** with about 2.5° of margin at each end.

## 3. Load case

**Handling torque about the tilt axis** (from the closed load check):
- T_h = 5 N × 114.3 mm (far corner) + 3.43 N × 17.2 mm (0.35 kg upper-bound cassette) = **0.63 N·m**.
- Design torque with SF 2: **T_d = 1.26 N·m**.

**Tangential force at the index radius** (F = T / r, at r = 10 mm):

| Case | Force |
|---|---|
| Handling | 63 N |
| Design | 126 N |
| Misuse check only (someone forces 20 N at the corner without releasing): T = 2.35 N·m, 3.7 × handling | 235 N; used only to set the failure order, not as a requirement |

**Sustained torque (gravity alone):** ≤ 0.06 N·m, 1/10 of handling.

**Discrete vs continuous:**
- At a worst-case 7.5° mis-set the cosine loss is **0.86 %**; the mean over ±7.5° is 0.29 %.
- **Eleven discrete positive positions** cost negligible energy compared with continuous adjustment. They give repeatable angles and a positive lock without relying on friction.
- **Decision: 11 discrete positions, no continuous clamp.**

## 4. Candidate concepts

| # | Concept | Summary |
|---|---|---|
| C1 | **Spring index pin** (axial) | Hardened pin in the cassette engages 1 of 11 holes in a pin-keyed index plate at r ≈ 10 |
| C1b | Twin-pin vernier | Holes at 30° with two pins offset 15° to double the pitch. At r ≈ 10 the two pins would be only 2.6 mm apart, so a second hole row at r ≈ 6.5 is needed: 2 rows, 2 pins, 2 springs |
| C2 | Detent plate + spring ball / roller | Profiled track, ball held in by a spring |
| C3 | Serrated / toothed index ring | Face or peripheral teeth at 15° pitch; a spring-engaged toothed shoe or pawl |
| C4 | Cam-lever friction clamp | Continuous clamp of the bracket against a pin-keyed friction face, optional detents |
| C5 | Commercial constant-torque friction hinge | Replaces the hub joint |
| C6 | Lid-referenced lock | A cassette pin engaging holes in the lid side face |

## 5. Quantitative comparison

Stresses are at T_h / T_d unless noted. The PETG allowables are the conservative load-check values: bearing 30, in-layer tension 35, interlayer 20, shear 15 MPa.

| | C1 metal pin + plate | C2 detent | C3 PETG teeth | C4 clamp | C5 friction hinge | C6 lid lock |
|---|---|---|---|---|---|---|
| Torque capacity | Pin Ø1.5 double shear 18 / 36 MPa; plate bearing 28 / 56 MPa; plate web 49 / 97 MPa (304 stainless, yield ≥ 205): **SF ≥ 2 at T_d** | Holding = F_spring · r · tan(flank). At r 10 and 45° it needs a **63 N** spring (126 N at T_d); a practical 5–10 N spring holds only 0.05–0.1 N·m | 2 teeth loaded: 74 N/tooth, root bending **55 MPa** ✗. Only with 5 teeth sharing equally: 22 MPa, marginal | Needs **280–420 N** clamp force (μ 0.2–0.3, r_eff 7.5, 2 faces) | Commercial parts reach 1–2 N·m | — |
| Positive? | **Yes.** The pin is in pure shear, with no cam-out component | No | Only with straight flanks plus an axial latch | No (friction) | No (friction) | Would be |
| Accidental release | Only by the slider; a bump cannot release it | Clicks over at about 5–10 N | Cams out without a latch | Slips at overload | Moves at overload | — |
| One-handed | **Yes:** thumb slider plus rotate | Yes | Yes (shoe pull) | Two actions (lever, rotate, lever) | Yes | — |
| Parts per side | ~7: plate, pin, spring, key pin, slider, cap, screw | ~4 | ~5 | ~6–8 incl. cam hardware | 1 (buy) | — |
| Spring | Light preload 1–3 N (steel) | Heavy, 60–130 N | Light | None, but a high clamp force | Internal | — |
| PETG printability | Only guides / clevis / slider are printed | Track in PETG wears | Teeth 1.1 mm wide, 2.6 pitch: poor definition | Fine | n/a | — |
| Wear | Metal on metal; the pin and plate are replaceable | High (sliding ball under high load) | High (PETG flanks) | Faces polish, lose μ | Low | — |
| Orientation sensitivity | Low (PETG sees ≤ 7 MPa) | Medium | **High** (tooth roots across layers) | Medium | n/a | — |
| Tolerance sensitivity | Hole Ø +0.1 gives ±0.29° play | Low | High (tooth sharing) | Low | Low | — |
| Dirt / debris | Through-holes plus an open-bottom groove push grit through | Tolerant | Teeth pack with grit | Grit alters μ | Sealed | — |
| Service | Pin / spring from a cap; plate after one roll pin | Easy | Reprint | Medium | Replace the hinge | — |
| Package / envelope | Fits band ∪ tray at r 10 (§2); no envelope growth | Fits | Fits at r ≈ 10 | Fits, but the lever sticks out | **Does not fit.** It replaces the accepted pin / bracket | **Does not fit.** No lid material on the arc |
| Thermal (60–70 °C) | Insensitive: metal load path, steel spring, sustained PETG stress ≤ 1 MPa | **Very sensitive** (preload *is* the holding torque; PETG creep) | Sensitive (PETG strength about halves) | **Most sensitive** (PETG clamp relaxes) | Insensitive | — |
| Verdict | **Selected** | Rejected (not positive, impractical spring) | Rejected (PETG), or custom metal teeth | Rejected (friction, creep, complexity) | Rejected (hub redesign, friction) | Rejected (no geometry) |

C1b (vernier) is a fallback only. It allows larger holes (30° pitch, Ø2.5) but doubles the pins and springs and needs a second hole row. It becomes attractive only if the 1.0 mm web of C1 proves unmanufacturable (§13).

## 6. Wear and thermal

**Wear:**
- The pin and plate are hardened / stainless metal. The sliding contact happens only when the released pin rides the plate face under a 1–3 N spring, which is negligible.
- Engagement is flat-ended in through-holes, so there is no ramp wear.
- If wear shows in testing, only the pin (a standard dowel) and the plate (a flat laser-cut part) are replaced.

**Thermal:**
- The torque path is metal: pin → plate → key pin → Ø5 hub pin.
- PETG carries only bearing: the pin clevis at 7 / 14 MPa and the pin-to-carriage flat at 10.5 / 21 MPa.
- Under sustained gravity these stresses fall to about 1 MPa, so PETG creep is irrelevant.
- The steel spring does not relax at 70 °C. Its preload only *seats* the pin; it never carries the holding torque, so preload loss cannot release the lock.
- PETG/steel expansion mismatch at ΔT 50 K is about 0.03 mm at r 10, about 0.15°, which is negligible.
- **Using a metal pin, plate and spring removes the thermal concern cheaply.** C2 and C4 are exactly the concepts that high temperature would defeat.

## 7. Packaging (C1)

**Stacking along X from the cassette's inboard edge (deployed values; stowed is −158):**

| X (mm) | What |
|---|---|
| 158.5–168.5 | Existing hub bracket and 10 mm bore (unchanged) |
| 168.5–171.0 | **Clevis groove**, 2.5 wide (0.5 + 1.5 plate + 0.5), cut into the tray around the axis, open at the bottom into the band |
| 169.0–170.5 | Index plate (non-rotating) |
| 171–183 | Plunger block in the tray (outboard clevis cheek): pin guide, spring, cap |

**Plate shape:**
- A sector plus hub. Holes at r 10 from −17.5° to +132.5° (lid frame); outer edge r ≤ 12.
- Below the tray it stays inside the band (dy −5…+12, dz ≥ −5); above it sits in the tray groove.
- It rides the rail slot exactly like the bracket (the B20 variant already showed an extended hub zone passes all E2 checks).

**Index pin position:**
- At a fixed cassette-frame angle of **57.5°**, r 10: Y 137.2, Z 65.9, inside the tray.
- It crosses the groove and seats in a counter-hole in the tray inboard of the groove, so it is in **double shear**.
- That counter-hole runs through to the cassette's inboard face so grit can escape.

**Cable:**
- It rises inside the bracket's inboard part as now, then must leave the hub zone at |dy| > 12 before X 168.5.
- It must not cross the clevis groove. Only the routing inside the cassette changes.

**Existing geometry changed:**
- Ø5 pin: +2.5 mm, plus a Ø1.5 cross hole and a flat.
- Carriage bore: gains a flat.
- Cassette tray: gains the groove, the plunger block and a slider recess.

**Unchanged:** lid and cassette envelopes, rail, bracket, bore, wall, axis and F3 clearances.

## 8. Recommended concept: C1, axial spring index pin with a pin-keyed stainless index plate

**Why:**
- It is the only candidate that is positive and one-handed, fits the envelope, and is insensitive to heat.
- It uses the fewest custom parts: one flat laser-cut plate, with everything else standard.
- It puts every load-critical interface in metal where the 2.6 mm pitch demands it. PETG carries only low bearing loads.
- It follows D-004 (rail = structure, pin = rotation, indexed positive lock, gears not structural).

**Operation (one hand):**
1. Deploy: slide the cassette out at 0°. The pin is seated in the 0° hole, so the cassette stays flat through the slot.
2. With the hand near the cassette's inboard end, the thumb slides the recessed slider outboard about 5 mm, which withdraws the pin.
3. Rotate the cassette with the same hand; the bore turns freely.
4. Let the slider go. The pin rides the plate face and **clicks** into the next hole when aligned.
5. Collect solar. Torque puts the pin in shear with no axial component, so a bump cannot unlock it.
6. Stow: release, return to 0° (click), slide in. A tilted cassette cannot enter the slot, which acts as a natural interlock.

**Failure order under misuse** (forced without releasing):
- First to yield: the PETG pin-to-carriage flat (39 MPa at 20 N), a printed, replaceable part.
- Next: the plate web (181 MPa, still below yield).
- The metal pin, key pin and Ø5 hub pin keep SF ≥ 2.

## 9. Mechanism architecture (exact concept)

- **Fixed side** (does not rotate): the Ø5 hub pin, anti-rotated in the carriage by a flat along the full 40 mm carriage engagement. At its tip, just outboard of the bracket, the **index plate** is keyed by a Ø1.5 roll pin, fitted vertically and inserted from below when deployed. The plate is also the cassette's **axial retainer**, captured in the clevis groove with 0.5 mm clearance each side.
- **Rotating side:** the cassette tray forms a **clevis** around the plate: the inboard cheek has the counter-hole, the outboard cheek is the plunger block. A **hardened Ø1.5 index pin** runs in the outboard cheek along X at r 10, 57.5°. It is pushed −X by a light compression spring through the plate hole into the inboard counter-hole.
- **Release:** a printed slider in a recess on the cassette's non-panel face, linked to the pin carrier. Stroke 5 mm, thumb force about 2–3 N.
- **Tilt hard stops at ±80°:** required to protect the cable twist zone, which is sized for ±75°. They are formed by the plate's arc ends striking stop lugs in the cassette groove near the hub. This is packaging-tight and is a detail-design item (§13).
- **Gears:** not needed for manual 15° indexing. If a gear drive is added later for actuation, its backlash must exceed the index play (±0.3°) so the gear never carries locked torque.

## 10. Required hardware (per side; common unless noted)

| Item | Spec (provisional) |
|---|---|
| Index pin | Ø1.5 × 16 mm hardened steel dowel (ISO 8734 / DIN 6325), tip chamfered |
| Spring | Stainless compression spring, OD ≈ 3.0, wire 0.3–0.4, free length ≈ 10, rate ≈ 0.3 N/mm (preload ≈ 1 N, ≈ 2.5 N at full stroke) |
| Index plate | **Custom** laser-cut stainless (301 ½-hard preferred, or 304), 1.5 mm; 11 × Ø1.6 holes on R10; outer R ≤ 12; hub with Ø5 bore and a Ø1.5 key hole |
| Key pin | Ø1.5 × ~8 mm spring (roll) pin or hardened dowel |
| Hub pin | Existing Ø5 metal pin, now **custom**: ≈ 64 mm long (40 in the carriage + 11.5 link + 10 bore + 2.5 plate), 0.5 mm flat over the carriage length, Ø1.5 cross hole at the tip. Stainless 303 / 304 or 5 mm D-shaft stock |
| Cap screw | 1 × M2.5 screw + heat-set insert (plunger-block cap) |

## 11. Required printed parts (PETG)

- **Cassette hub zone:** new features in the existing cassette, not new parts: clevis groove, inboard counter-hole (through to the inboard face), plunger bore Ø1.6 about 6 mm long, spring pocket, slider recess and slot, stop lugs.
- **Slider / pin carrier:** 1 part.
- **Plunger-block cap:** 1 part, retaining the pin and spring.
- **Carriage:** existing part; the pin bore gains a flat.

## 12. Parameters to add to `nomad.yaml` (proposed; not added)

| Parameter | Proposed working value | Note |
|---|---|---|
| SOLAR_INDEX_STEP | 15° (exists) | Unchanged |
| SOLAR_INDEX_POSITIONS | formula 2 × ROTATION_LIMIT.max / STEP + 1 → 11 | Derived |
| SOLAR_INDEX_RADIUS | 10 | Hole-circle radius; valid window ≈ 9.5–10.5 (§2) |
| SOLAR_INDEX_PIN_DIAMETER | 1.5 | Hardened dowel |
| SOLAR_INDEX_HOLE_CLEARANCE | 0.1 | Hole = pin + clearance; sets the ±0.29° play |
| SOLAR_INDEX_PIN_ANGLE | 57.5° | Pin position in the cassette frame (from +Y toward +Z), centring the hole arc in the window |
| SOLAR_INDEX_PLATE_THICKNESS | 1.5 | Stainless |
| SOLAR_INDEX_PLATE_OUTER_RADIUS | 12 | Band / tray limit |
| SOLAR_INDEX_GROOVE_CLEARANCE | 0.5 | Each side of the plate |
| SOLAR_INDEX_PIN_STROKE | 5 | ≥ counter-hole 2 + gap 0.5 + plate 1.5 + 0.5 |
| SOLAR_INDEX_COUNTERHOLE_DEPTH | 2 | Double-shear support |
| SOLAR_INDEX_SPRING_PRELOAD | 1 N | Seating only |
| SOLAR_INDEX_KEY_PIN_DIAMETER | 1.5 | Plate-to-pin key |
| SOLAR_HUB_PIN_FLAT_DEPTH | 0.5 | Pin anti-rotation in the carriage |
| SOLAR_HUB_PIN_TIP_EXTENSION | 2.5 | Pin beyond the bracket bore |
| SOLAR_TILT_STOP_ANGLE | 80° | Hard stop beyond the last index |

The generator would also need an index-packaging check: holes plus wall inside band ∪ tray for all 11 positions, and plate travel inside the rail-slot envelope.

## 13. Risks

| Risk | Level | Mitigation / fallback |
|---|---|---|
| **Tight packaging window:** only ≈ 2.5° margin at each arc end at r 10 | Medium | Confirm in CAD with the generator check; fall back to the C1b vernier or r 9.5 |
| **Plate web 1.0 mm in 1.5 mm stainless** (laser minimum-web rule) | Medium | 1.2 mm 301 ½-hard, fiber laser or waterjet; supplier DFM check; C1b fallback |
| Pin-to-carriage flat in PETG: SF 2.9 handling / 1.4 design; yields first under misuse | Low–Med | Accept as the replaceable fuse; upgrade path is a metal insert or cross pin |
| 0° accuracy for stowing: play ±0.29° gives ≈ 0.6 mm at the far corner against 1 mm bay clearance | Low | Lead-in chamfers at the slot and bay; hole clearance ≤ 0.1 |
| Hard stop at ±80° near the hub: small lever, high contact force | Medium | Detail design; alternatively a stop between the bracket and the pin collar |
| Cable must be rerouted away from the clevis groove inside the cassette | Low | Route at \|dy\| > 12 |
| Grit in 1.6 mm holes | Low | Through-holes, through counter-hole, open-bottom groove |
| Small custom Ø5 pin machining (flat + cross hole) | Low | Simple lathe / drill work, or D-shaft stock |

## 14. Physical prototype test plan (next physical round; nothing ordered)

**Coupon:**
- Printed carriage segment in a printed rail segment (A1 / A2 geometry).
- Custom Ø5 pin with flat and cross hole.
- Stainless index plate: 1.5 mm, plus a 1.2 mm variant.
- Printed cassette-hub block with the clevis, index pin, spring, slider and cap.
- A 200 mm aluminium or printed lever arm standing in for the cassette.

| # | Test | Pass criterion |
|---|---|---|
| 1 | Operation: one-handed release, rotate, click at all 11 positions; 0° stow alignment | One hand, no tool; audible / tactile engagement; 0° within ±0.5° |
| 2 | Angular play at each position (dial or phone inclinometer on the arm) | ≤ ±0.5° |
| 3 | Static torque 0.63 N·m (≈ 320 g at 200 mm), then **1.26 N·m** (≈ 640 g), 1 min each | No slip, no permanent set, no play increase |
| 4 | Accidental-release test: taps and vibration at 0.63 N·m preload; drop the lever tip 20 mm onto a stop | Stays engaged |
| 5 | Cycling: 2,000 release / rotate / engage cycles across the range | Play increase ≤ 0.2°, no pin or plate damage |
| 6 | Grit: sand / dust applied, then 50 cycles | Still engages; the pin clears the holes |
| 7 | Hot hold: 65 °C oven, 1.26 N·m for 24 h, and cycling hot | No creep drift > 0.3°, still releases |
| 8 | Misuse / failure order: increase torque to first yield | Failure in the intended fuse (carriage flat or plate), never the Ø5 pin or the bracket |
| 9 | Hard stop at ±80° | Stops before the cable twist limit |

## 15. Recommendation (awaiting approval)

**Adopt C1:**
- An axial, spring-loaded Ø1.5 hardened index pin in the cassette, in double shear through a clevis.
- It engages a pin-keyed stainless index plate with 11 holes at 15° on R 10 mm.
- One-handed thumb-slider release; **11 discrete positive positions, no continuous clamp**.

**Why this over the others:**
- It is positive and bump-proof, fits the existing envelope with no F3 or envelope change, and is thermally insensitive.
- All parts are common except one flat laser-cut plate.

**Before implementation, confirm:**
- (i) The owner accepts the small custom metal parts: the plate, and the modified Ø5 pin with flat and cross hole.
- (ii) The packaging window check in CAD.
- (iii) The laser-cut web on the plate.
- (iv) The hard-stop detail.

Nothing is implemented. The next action is the owner's decision.
