# Round E — Solar Hub Pin Anti-Rotation Check

**Status:** analysis only. No change to `nomad.yaml`, the spec, FeatureScript, Onshape, CAD or Git. Awaiting owner approval.

**Basis:**
- F3 Option B geometry as implemented (`e_lid_layout.py` from `nomad.yaml`);
- `round_e_solar_hub_load_check.md`;
- `round_e_solar_index_lock_investigation.md`;
- `round_e_solar_index_lock_manufacturing_check.md` (accepted direction: Ø1.5 hardened index dowel, 1.5 mm 301 ½-hard / 17-4PH index plate, double-D key plus M2 clamp screw).

**Evidence levels:**
- Geometry: *modeled*.
- Stresses: *inferred* (hand and numerical calculations, stated models, no FEA, nothing tested).
- Scratch script: `antirot.py` in the session scratchpad (not in the repository). All formulas are given below.

**Acceptance basis (owner):** SF ≥ 2 at the **1.26 N·m design torque**, i.e. no yield at **2.52 N·m** under conservative assumptions.

**Decision: C — CAPTURED METAL ANTI-ROTATION FEATURE (§10).**

---

## 1. Current geometry

The carriage cross-section is given relative to the hub-pin axis (Y 131.8, Z 57.5). Right side shown; the left is mirrored.

| Item | Extent (dy × dz) or value |
|---|---|
| Carriage body | dy −7.8 … +14.8, dz −6.0 … +2.0; length 40 (X, KX0 inboard → KX1 outboard) |
| Carriage boss (in the rail slot) | dy −5.0 … +12.0, dz +2.0 … +4.5 |
| Hub pin | Ø5, fixed in the carriage; walls 2.0 above (boss top) and 3.5 below (to the carriage bottom = rail floor) |
| Solar cable envelope (Ø6) | **dy +3.5 … +9.5, dz −3 … +3, along the full carriage length.** Only 1.0 mm of PETG between the pin bore and the cable |
| −Y side of the pin | Solid PETG block dy −7.8 … −2.5 (5.3 mm). The −Y face runs against the rail wall |
| Root (maximum pin bending) | Carriage **outboard** face KX1. M = 1088 N·mm at handling (0.35 kg + 5 N), 2176 N·mm at the design case |
| Proposed anti-rotation (investigation §9) | Single 0.5 mm flat on the pin (flat width 3.0) along the full 40 mm, in a printed D-bore |

**Open items noted:**
- None of the earlier reports specifies how the pin is **axially** retained in the carriage.
- The stow push (−X) and deploy pull (+X) must pass from the pin into the carriage, so the chosen solution should cover axial retention as well (§10 does).

## 2. Design torque

| Case | Torque | Note |
|---|---|---|
| Handling T_h | 0.63 N·m | 5 N at the far corner + 0.35 kg cassette |
| **Design T_d** | **1.26 N·m** | SF 2 on handling |
| Acceptance | No yield at 2.52 N·m | SF 2 at T_d |
| Sustained (gravity only) | ≤ 0.06 N·m | |

Torque flows: index dowel → index plate → pin tip → through the pin → carriage → rail. The carriage-to-rail couple (11.3 mm lever, 40 mm length) is lightly stressed and is not an issue.

## 3. Failure mode of the current flat

**Model.** A D-flat in a printed clearance bore touches along *half* the flat. Pressure rises linearly to the flat edge. The round side reacts radially (no moment).
- T = p·L·w²/12, so **p = 12·T/(L·w²)**.
- A fully preloaded contact would give 6·T/(L·w²), which is the investigation's best-case value.

**Current flat (f 0.5, w 3.0, L 40):**
- **21 MPa at handling, 42 MPa at design.** Against 30 MPa: SF 1.43 at handling, **0.71 at design**, so it yields below the design torque.
- A 0.1 mm clearance on the flat gives about ±3.8° of free play (rotation ≈ c / (w/2)).

**Why it fails:**
- The lever is only half the flat width (≤ 2.5 mm, because the flat lies inside Ø5).
- Every printed interface inside the Ø5 envelope has the same weakness.
- The flat also reduces the pin section exactly at the root, where bending is highest (§5.1).

## 4. Candidate solutions

| # | Concept |
|---|---|
| A | Deeper single printed flat (f 0.5 → 2.0) |
| B | Metal set screw onto the flat: friction, or a dog point in a pin dimple |
| C1 | **Captured anti-rotation plate:** a stainless plate on a short double-D at the pin's *inboard* end, captured in a transverse carriage slot, reacted by a Ø3 dowel at a 5.6 mm lever |
| C2 | Vertical cross pin through the hub pin |
| C3 | Radial peg on the −Y side |
| C4 | Parallel key under a flat; metal sleeve; hex coupling nut |
| D | Double-D along the carriage length in a printed double-D bore (the owner's question) |
| E | Other: hex-bar pin |

## 5. Calculations

### 5.1 Pin section properties (Ø5, numerical)

Torsion values come from a Prandtl finite-difference solve. The raw solve under-predicted the round-bar Zt by 15 %, so all Zt values are scaled by that calibration.

| Section | Z_min (mm³) | Zt (mm³) | Pin at root, design: σ / τ / von Mises (MPa) | SF on 303 (σy 415) | Torsion only (no bending), vM → SF 303 |
|---|---|---|---|---|---|
| Round | 12.3 | 24.5 | 177 / 51 / **198** | **2.09** | 89 → 4.7 |
| Single flat f 0.5 | 10.7 | 22.0 | 203 / 57 / 227 | 1.83 | — |
| Single flat f 1.0 | 8.5 | 17.9 | 255 / 70 / 283 | 1.47 | — |
| Double-D A/F 3.5 | 8.5 | 16.4 | 255 / 77 / 288 | 1.44 | 133 → **3.1** |
| Double-D A/F 3.0 | 6.6 | 12.9 | 328 / 98 / 369 | 1.12 | 170 → **2.44** |

**Conclusions:**
- **Keep the pin round at the carriage root.** Any flat there costs 10–45 % of the pin's margin.
- Flats belong only where bending is about zero: the tip (already accepted) and the carriage **inboard** end.

### 5.2 A — deeper printed flat (L 40, PETG edge pressure at T_d)

| f | w | Clearance fit (MPa / SF) | Preloaded (MPa / SF) |
|---|---|---|---|
| 0.5 | 3.00 | 42.0 / 0.71 | 21.0 / 1.43 |
| 0.75 | 3.57 | 29.6 / 1.01 | 14.8 / 2.02 |
| 1.0 | 4.00 | 23.6 / 1.27 | 11.8 / 2.54 |
| 1.5 | 4.58 | 18.0 / 1.67 | 9.0 / 3.33 |
| 2.0 | 4.90 | 15.8 / 1.90 | 7.9 / 3.81 |

**Not viable:**
- SF 2 with a clearance fit needs a flat 5.02 mm wide, which is wider than the pin.
- Deeper flats also weaken the root (§5.1).
- Only a preloaded fit reaches SF 2, and preload in PETG relaxes (creep, heat). That is friction, not geometry.

### 5.3 B — set screw

| Variant | Result | SF / fraction of T_d |
|---|---|---|
| Friction: M2.5 / M3 in a heat-set insert, preload 250–350 N (insert-limited), μ 0.15–0.2, acting at the flat and the opposite round side | 0.17–0.32 N·m | **0.13–0.25 × T_d** |
| Positive: dog point in a pin dimple, lever ≤ 2.5 | Lateral force **504 N** at T_d. M3 dog Ø2 shear 160 MPa | SF ≈ 1.6 (A2-70) |
| | Insert radial bearing in PETG 19 MPa | **SF 1.56** |

**Access:** from −Y (the rail wall covers it) or from below (the rail floor covers it). Either way it can only be done with the carriage out of the rail.

**Not viable** as the torque path. It is still useful for removing play, but it is not needed with C1.

### 5.4 Other C geometries (capacity at a 15 MPa PETG limit, SF 2)

| Geometry | Capacity |
|---|---|
| C2: vertical Ø2 cross pin (only 3.5 / 2.0 mm walls to bury it) | 0.51 N·m = **0.40 × T_d** |
| C3: radial Ø2 peg to dy −7 | 0.64 N·m = **0.51 × T_d** |

**C4:**
- A **parallel key under a flat** only works if the key and pin are one rigid body. A flat-to-key contact face cannot carry the moment without a tension tie. A screw tie sees about 700 N at T_d, which exceeds an M2 screw. A keyseat in Ø5 is too small.
- **A metal sleeve or hex coupling nut** does not fit: the 1.0 mm cable wall, the 2.0 mm boss wall and the 3.5 mm floor wall leave no room for anything larger than Ø5.

### 5.5 D — double-D along the carriage in a printed double-D bore (owner's question)

The model is the same as §3, with two flats: **T = p·L·w²/6**.

**Uniform torque-transfer model:**

| A/F | L | PETG at T_d (MPa) | SF (RT / hot) |
|---|---|---|---|
| 3.5 | 40 | 14.8 | 2.02 / 1.01 |
| 3.0 | 40 | 11.8 | 2.54 / 1.27 |

**Correction for non-uniform transfer.** The torque enters at the outboard end. The pin's torsional stiffness competes with the contact stiffness (k_s 300–1000 N/mm³). The decay length is 20–52 mm, which makes peak pressure 1.2–2.0 × the mean:

| A/F | PETG peak at T_d (MPa) | SF (RT / hot) |
|---|---|---|
| 3.0 | 16–24 | **1.24–1.87 / 0.62–0.93** |
| 3.5 | 18–24 | 1.27–1.70 |

**Other consequences:**
- Pin at the root: A/F 3.0 gives SF 1.12 on 303 (§5.1). A/F 3.5 gives 1.44. It would need 17-4PH or a hardened pin.
- Ending the flats 10 mm inside the face (L 30) raises PETG to 15.8+ MPa.

**Answer: yes, a positive double-D capture works, but not at SF 2.**
- Its capacity is **≈ 1.6–2.4 N·m at RT** (1.24–1.87 × T_d) and roughly half that hot.
- It also costs pin margin at the root.
- It leaves printed-fit play of ±1–3°.
- Under overload it crushes the **carriage**, which is the wrong part to fail first.

### 5.6 C1 — captured anti-rotation plate + dowel (recommended)

**Torque path:** pin (round through the carriage, double-D A/F 3.0 only at its inboard end) → stainless plate (1.5 mm, same stock as the index plate) → Ø3 dowel at (dy −5.0, dz −2.5) → PETG carriage over the dowel's length.

| Check (at T_d unless noted) | Value | Result |
|---|---|---|
| Dowel lever e | √(5.0² + 2.5²) = 5.59 mm | |
| Dowel force F = T/e | **225 N** (113 N handling), direction 0.89 Z / 0.45 Y | |
| PETG dowel bearing, beam on elastic foundation, β = (k/4EI)^¼, k 1000–2500 N/mm². Infinite beam: p = Fβ/(2d); conservative bound: p = Fβ/d | 5.0–6.3 MPa (infinite); **10.1–12.7 MPa** (bound) | **SF 4.8–6.0 / ≥ 2.36 RT**; hot SF 2.4–3.0 / ≥ 1.18 |
| PETG wall shear-out under the dowel (bottom wall 2.0, effective length 2/β ≈ 13, two planes, interlayer 10 MPa) | 4.3 MPa | SF 2.3 even across layers |
| Plate double-D key (A/F 3.0, t 1.5): p = 6T/(t·w²) | 315 MPa | 301 ½-hard **SF 2.41**; 17-4PH 2.30 |
| Plate dowel-hole bearing | 50 MPa | ≫ 2 |
| Dowel Ø3 in double shear across the slot | 16 MPa | ≫ 2 |
| Dowel bending (infinite beam, M ≈ F/4β) | ≈ 140 MPa | A1/A2 stainless ISO 2338 ≥ 2.5; hardened ISO 8734 ≫ |
| Pin at the root (round, unchanged) | vM 198 | 303 **SF 2.09** |
| Pin inboard double-D (A/F 3.0, torsion only) | vM 170 | 303 **SF 2.44** |
| Pin embedment in the carriage 30 mm (was 40) | Bearing ≈ 2.5 MPa (load check: 3.8 @ 20, 0.9 @ 40) | OK |
| Axial: stow push / deploy pull (≤ 50 N, 100 N impact) | Plate on slot wall ≈ 1–3 MPa; M2 screw in trivial tension | OK |
| Plate ligaments | Double-D top 1.3, bottom 2.9, +Y 1.3; dowel hole to the −Y edge 1.1, to the bottom 1.4; dowel-to-key 2.4 | OK |
| Wall from the dowel to: side face / pin bore / bottom / top | 1.3 / 1.6 / 2.0 / 3.0 | OK (the side face is backed by the rail wall) |

## 6. PETG assumptions

| Property | Value |
|---|---|
| Short-term bearing (RT) | 30 MPa |
| Hot (60–70 °C) | ≈ 15 MPa |
| Sustained | 8 MPa |
| Tension in-layer / across layers | 35 / 20 MPa |
| Shear in-layer / across layers | 15 / 10 MPa |

These are the conservative load-check values, below typical datasheet figures.

**Contact stiffness:**
- Flat on a printed wall: k_s 300–1000 N/mm³.
- Dowel foundation modulus: k 1000–2500 N/mm².
- Both are bracketed; the worse end of each bracket is used for the SF claims.

Printed parts use at least 4 perimeters and solid infill around the bore, the slot and the dowel hole.

## 7. Thermal considerations

**C1:** the torque path is **metal up to the dowel**. PETG sees only the dowel bearing:
- ≤ 12.7 MPa at T_d on the conservative bound (≈ 6 MPa likely);
- ≤ 6.3 MPa at handling;
- ≈ 0.3–0.6 MPa under sustained gravity, so creep is irrelevant.

**Hot SF at T_d** (the only sub-2 case, and only on the conservative bound):

| Option | Hot SF at T_d |
|---|---|
| C1 | ≥ 1.18 (≈ 2.4–3.0 on the infinite-beam estimate) |
| D | 0.62–1.27 |
| A (f 0.5) | 0.36 |

Handling hot: C1 SF ≥ 2.4.

**Expansion:** steel plate in a PETG slot, ΔT 50 K over 18 mm, mismatch ≈ 0.04 mm, within the 0.1 slot clearance.

C1 is the only option whose load-bearing PETG stress stays in the low single digits at the likely stiffness.

## 8. Assembly considerations (C1)

1. **Hub pin into the carriage** (carriage out of the rail; bench):
   1. Slide the anti-rotation plate into the transverse slot from the −Y side face.
   2. Insert the pin from the carriage **outboard** face, inboard end first. Its double-D end passes the Ø5 bore; align the flats with the plate hole (flats ±Y, visible) and push until the shoulder seats on the plate.
   3. Fit the M2 screw and Ø5 washer through the Ø5.5 access bore in the inboard face into the pin end (medium threadlocker, ≈ 0.15 N·m). The tool is **straight along X** (1.5 mm hex key).
   4. Press the Ø3 dowel from the inboard face through the carriage hole and the plate (light press in the plate) until it is flush with the inboard face.
2. **Carriage into the rail.** The rail wall now covers the slot opening and the rail floor covers the underside. Nothing protrudes; the carriage envelope is unchanged.
3. **Cassette hub bracket onto the pin tip.** The bracket bore slides over the tip double-D.
4. **Index plate onto the tip double-D.** Tip and inboard flats are milled in one setup with the same orientation.
5. **M2 screw and washer at the tip** (as accepted), with the same hardware as step 1.3.
6. **Spring-loaded index pin, spring and cap.**
7. **Operation.**

No step needs an angled tool. Steps 1.3 and 1.4 are axial from the free inboard face.

**Service** (plate, dowel or pin):
1. Remove the tip screw, the index plate and the cassette.
2. Slide the carriage out of the rail.
3. Remove the inboard M2 screw.
4. Drive the dowel out with a Ø2 punch through the push-out hole from the outboard face.
5. Pull the pin out outboard and slide the plate out.

All with hand tools.

## 9. Manufacturability

**Plate:**
- Same material (301 ½-hard or 17-4PH), same 1.5 mm thickness, same process (outline laser / waterjet, then CNC drill and ream) and same shop as the index plate. It can go on one drawing sheet and one order.
- Critical features: double-D A/F 3.00 +0.02/0 and the dowel hole.
- The other features are laser-grade.

**Pin:**
- 303 / 304 cold-drawn or ground rod.
- Operations: two double-D sections milled in **one setup** (tip A/F 3.5 as accepted; inboard A/F 3.0), and two M2 tapped end holes.
- **No flat along the carriage length.** This is simpler than the investigation's proposal.

**Dowel:** standard Ø3 × 24, ISO 2338 m6 stainless (A1/A2) or ISO 8734 hardened.

**Carriage (printed):**
- A transverse slot (1.6 mm, open to −Y);
- a Ø3 dowel hole (printed about Ø2.8, drilled / reamed to Ø3.0) through to the outboard face (Ø2 push-out beyond the dowel);
- a Ø5.5 × 10 access bore;
- the pin bore now 30 mm long (x 10–40).

**Print orientation:**
- Bottom-down is preferred. The slot is a 1.6 mm vertical gap with a trivial bridge; the horizontal holes are post-drilled.
- The dowel's Z load then crosses layers in compression and shear-out (SF 2.3 on interlayer shear, §5.6).
- On-end printing is also possible (holes vertical and accurate), but the slot then becomes a horizontal cavity with about a 10 mm bridge.

**Hardware family:** M2 is already accepted for the index plate; no new fastener type.

## 10. Recommended solution — **C. CAPTURED METAL ANTI-ROTATION FEATURE**

**What it is:**
- A 1.5 mm stainless anti-rotation plate, identical in material and process to the index plate.
- It is clamped on a short double-D at the hub pin's **inboard** end by the same M2 screw and washer used at the tip.
- It is captured in a transverse slot 10 mm inside the carriage's inboard face.
- A Ø3 dowel at a 5.6 mm lever reacts it into the carriage.

**Why:**
- **It is the only candidate that shows SF ≥ 2 at 1.26 N·m under conservative assumptions:**
  - PETG ≥ 2.36 on the worst-case bound (≈ 5 likely);
  - metal ≥ 2.09 (pin root on 303), 2.41 (plate key), 2.44 (pin torsion).
- The pin stays **round at the root**. This is stronger than any flat option.
- The torque path is metal. PETG stress is low and spread along the dowel, so heat is handled.
- Near-zero play: clamped key, dowel transition-fit in the plate.
- It also **solves the unspecified axial retention** of the pin in the carriage, positively in both directions.
- It reuses the index-plate stock, process and M2 hardware. The only new standard part is one dowel.
- No change to the carriage, lid or cassette envelope, the F3 hub, the bore, the rail or the cable routing.

## 11. Exact geometry and hardware specification (for implementation; not implemented)

**Frame:**
- x = distance along +X from the carriage **inboard** face (KX0);
- dy / dz = offsets from the hub-pin axis (right side; the left mirrors Y).

| Item | Specification |
|---|---|
| **Anti-rotation plate** | 301 ½-hard (ASTM A666) or 17-4PH, **1.5 mm**, same stock and process as the index plate. Outline: dy −7.6 … +2.8 with dz −5.4 … +1.6 for dy < −4.8, and dz −5.4 … +3.8 for dy ≥ −4.8 (L-shape following the body and boss). Inner corners R ≥ 0.5; edges deburred |
| Plate key hole | Double-D **A/F 3.00 +0.02/0**, flats facing ±Y, round R 2.50 +0.02, centred on the pin axis |
| Plate dowel hole | **Ø2.99 +0.01/0** (light press on an m6 dowel) at dy −5.00, dz −2.50 ±0.03 relative to the key-hole centre |
| **Carriage slot** | x 10.0 … 11.6 (1.6 wide); profile = plate outline + 0.1, open to the −Y side face. Leaves 0.6 mm PETG to the cable channel (dy +3.5), 0.6 to the boss top, 0.5 to the carriage bottom |
| Carriage pin bore | Ø5 (existing fit) over x 11.6 … 40; x 0 … 10 becomes the **Ø5.5 access bore** |
| Carriage dowel hole | Ø3.0 (printed Ø2.8, drilled / reamed; slip to line fit) at dy −5.0, dz −2.5, x 0 … 24; **Ø2 push-out hole** x 24 … 40 |
| **Hub pin** | Ø5, 303 / 304 cold-drawn or ground (σy ≥ 415; **not annealed**), length **53.5** (was ≈ 63.5–64). Inboard end: double-D **A/F 3.00 −0.02/0**, flats ±Y, length 1.45 (the end sits 0.05 below the plate face so the washer clamps). Shoulder bears on the plate's outboard face. **M2 × 4 deep tapped hole**. Round Ø5 over x 11.6 … 40 (no carriage flat). Tip unchanged from the manufacturing check (double-D A/F 3.5 + M2), milled in the **same setup and orientation** as the inboard flats (parallel within 0.02 mm across the flat, ≈ 0.3°) |
| **Dowel** | Ø3 × 24, ISO 2338 m6 A1 / A2 stainless (or ISO 8734 hardened), flush with the inboard face |
| **Screw / washer** | M2 × 5 ISO 7380 or ISO 4762, A2 + ISO 7089 M2 washer (Ø5 × 0.3), medium threadlocker, ≈ 0.15 N·m. Same parts as the tip |
| Pin axial float in the carriage | 0.1 mm (slot 1.6 − plate 1.5) |

**Proposed `nomad.yaml` changes** (not added):

| Parameter | Proposal |
|---|---|
| SOLAR_HUB_PIN_FLAT_DEPTH | **Withdrawn** |
| SOLAR_HUB_ANTIROT_PLATE_THICKNESS | New; formula = SOLAR_INDEX_PLATE_THICKNESS |
| SOLAR_HUB_ANTIROT_PLATE_X | 10 |
| SOLAR_HUB_PIN_INBOARD_ACROSS_FLATS | 3.0 |
| SOLAR_HUB_ANTIROT_DOWEL_DIAMETER | 3 |
| SOLAR_HUB_ANTIROT_DOWEL_LENGTH | 24 |
| SOLAR_HUB_ANTIROT_DOWEL_Y / _Z | −5.0 / −2.5 |
| SOLAR_HUB_ANTIROT_SLOT_CLEARANCE | 0.1 |
| SOLAR_HUB_PIN_LENGTH | Derived: carriage length − plate X + link + bracket length + tip extension = 53.5 |

## 12. Remaining risks

| Risk | Level | Note / mitigation |
|---|---|---|
| **Dowel bearing model spread** (k and bearing distribution): SF 2.36–6.0 at RT, 1.18–3.0 hot | Medium | Test 1 and test 3 below. Fallback: a second 1.5 plate stacked (slot 3.1), which halves the key stress and spreads the dowel load |
| **Cassette counter-hole (PETG, 3 mm) is the next weakest printed link:** yields at 2.14 × T_d at RT and **1.07 × T_d hot**. Under hot misuse it could fail before the intended metal fuse | Medium | Outside this task (index-lock cassette detail). Consider a pressed stainless sleeve in the counter-hole at implementation |
| **Failure order (RT, multiples of T_d at first yield):** index-plate tip key bedding 1.92 × → cassette counter-hole 2.14 × → carriage dowel bearing ≥ 2.36 × (bound; ≈ 5 × likely) → anti-rotation plate key 2.41 × → index dowel 2.8 × | Low | Matches the owner's hierarchy (cheap metal first, carriage late, lid never). Note: the **tip key** is SF 1.92 at T_d by the conservative linear model; harmonising the tip to A/F 3.0 raises it to 2.41 (owner's option) |
| Thin PETG skins around the slot (0.5–0.7 mm) | Low | Non-structural; may be left open |
| The cable passes 0.5 mm from the plate's +Y edge (PETG wall 0.6) | Low | Deburr; keep the wall |
| Pin needs 303 / 304 cold-drawn, not annealed | Low | State it on the drawing |
| Packaging modeled 2-D only | Low | Include the plate, slot and dowel in the E-model generator check at implementation |

## 13. Physical test recommendation

**Coupon:**
- Printed carriage segment (40 mm, production orientation) in a printed rail segment;
- 303 pin with both double-Ds;
- anti-rotation plate, Ø3 dowel, M2 hardware;
- a 200 mm lever clamped to the pin tip.

**Control:** also print a D-option carriage (double-D A/F 3.0 over 40 mm) to validate §5.5.

| # | Test | Pass |
|---|---|---|
| 1 | Static 2.52 N·m (SF 2 × T_d), 1 min each direction, RT | No slip; permanent rotation ≤ 0.2°; no cracking |
| 2 | Play at ±0.1 N·m | ≤ ±0.3° pin-to-carriage |
| 3 | Hot hold 65 °C, 1.26 N·m for 1 h, then 0.63 N·m cycles | Drift ≤ 0.3°; no visible dowel-hole ovalisation |
| 4 | Axial ±100 N (stow push / deploy pull) | No movement beyond the 0.1 float |
| 5 | Ramp to first yield (RT) | First damage in the metal key or plate, or dowel bearing; **not** carriage fracture. Record the torque |
| 6 | 20 × assembly / disassembly (steps 1 and 8) | No wear of the slot or dowel hole; the dowel stays retained |
| 7 | Control coupon (D) to first yield | Confirms the §5.5 capacity (expected 1.6–2.4 N·m) |

---

## Decision

**C. CAPTURED METAL ANTI-ROTATION FEATURE.** A 1.5 mm stainless plate on an A/F 3.0 double-D at the pin's inboard end, captured in a carriage slot, reacted by a Ø3 × 24 dowel, and clamped by the M2 screw and washer.

**It demonstrates SF ≥ 2 at 1.26 N·m:**

| Element | SF |
|---|---|
| PETG | ≥ 2.36 (worst-case bound) |
| Plate key | 2.41 |
| Pin root | 2.09 |
| Pin torsion | 2.44 |

It also fixes the pin's axial retention. The deeper flat (A), the set screw (B) and the printed double-D (D) are each below SF 2 at T_d under conservative assumptions.

Nothing is implemented. No production file, `nomad.yaml`, spec, FeatureScript, Onshape or Git change. Awaiting the owner's decision.
