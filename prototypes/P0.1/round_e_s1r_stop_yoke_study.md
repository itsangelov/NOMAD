# Round E — D-009 S1-R Journaled Stop-Yoke Feasibility Study

**Status:**
- Feasibility study only. It is not approved geometry and not for persistent Onshape.
- No change to `nomad.yaml`, the spec, `e_lid_layout.py`, FeatureScript, Onshape (0 API calls) or Git.
- **Tool:** `CAD/tools/s1r_stop_study.py` (NON-PRODUCTION, read-only; builds the candidate in memory on the current D-009 model and reruns the full check set; about 4 min).
- Phase 1 (the D-009 load reassessment) is in `round_e_d009_load_reassessment.md`. Read it first.

**Evidence levels:**
- Geometry: *modeled* (exact 2-D regions extruded along X).
- Loads, tolerances and impact: *inferred*.
- Nothing is physically tested.

---

## 1. Verdict — **S1-R: PASS (READY FOR OWNER REVIEW)**

S1-R meets the stop requirements. It is **not approved for persistent Onshape implementation.**

- **Stop angle:** hard contact at exactly **±80.000°** on both sides, both directions, lid 105°/135°. No other interference before it, and no engagement at ±75°.
- **D-009 unchanged:** lock checks A–G, stow interlock (only 0°), slide and lid sweeps, and F3 floor gap all unchanged. Service paths are non-destructive.
- **Stop reaction:** it closes through metal (stop plate → yoke → ring → bushing → pin).
  - The transverse load into the PETG bracket falls from **245 N / 2,144 N·mm (S1)** to **60 N / 529 N·mm** at 1.26 N·m.
  - The bracket SF for the stop alone is **3.97** (S1: 0.98).
- **SF ≥ 2 at 1.26 N·m** for every element of the stop load path. The weakest is the pin tip double-D at 2.32 in 303, then the unchanged D-009 dowel bearing at 2.36.
- **At 2.52 N·m:** the new S1-R parts are ≥ 2.0. The unchanged D-009 torque-path elements are about 1.2 (§9).
- **Tolerance:** with metal referencing, ±80° holds to **±2.41° worst / ±0.80° RSS**. The window is −4.5/+3.9°.

**Conditions and open dependencies (see §15):**
- **The Phase 1 problem remains.** The floating S1-R yoke does **not** fix the D-009 hub-bracket shortfall. The index lock's own reaction still goes through the PETG bore. A rigid, coaxially reamed variant of the same yoke would address both, but it needs its own study.
- It needs hardened, crowned contact faces, jig-reamed tray bores and tight key fits.
- About 4 mm of finger room is left in front of the thumb tab.
- A 3.3 × 6.3 × 31 mm slot is cut into the (not yet designed) cassette tray near the hub.

## 2. Architecture and exact geometry (right side; left rotated 180° about the lid's vertical centre)

**Frame:** X is stowed lid X; dy/dz are from the tilt axis (Y 131.8, Z 57.5). Angles are measured from +dy toward +dz.

| Part | Side | Geometry (modeled) |
|---|---|---|
| Index plate | Carriage (fixed) | Unchanged, X 11.0–12.5 |
| **Journal bushing** (new, stainless 303 / 17-4) | Carriage, clamped | X 12.5–15.8, OD 6.0 (g6), double-D bore A/F 3.0 on the pin tip |
| **Stop plate** (new, 2.5 mm stainless) | Carriage, clamped | X 15.8–18.3. Hub ring R 3.5; radial stop faces at **210°** and **330°** from R 3.5 to **R 5.774**; floor flat dz −5.0. Double-D key A/F 3.0 |
| Hub pin | Carriage | Tip double-D X 11.0–18.3, **length 59.3** (D-009: 53.5) |
| M2 tip screw + washer | Carriage | Clamps index plate + bushing + stop plate to the pin shoulder; X 18.3–20.6 |
| **Stop yoke** (new, machined 17-4PH H1025) | Cassette | **Ring:** X 13.0–15.5, bore Ø6.1 on the bushing (0.05 radial), OD 10.<br>**Neck:** dy ±3.0, dz 4.0–5.8.<br>**Stop lobe:** X 13.0–18.3, inner R 4.5, radial faces at **50°** and **130°**, top dz 5.2 (0.3 float below the tray).<br>**Drive arm:** X 13.0–15.5, dy −27.5…+3.0, dz 5.8–11.5, in a tray slot, with a radial drive slot 3.6 × 3.02 at dy −25 |
| **Yoke drive dowel** (new, Ø3 m6) | Cassette | Along X at (dy −25, dz 8.65), X 1.0–19.0, pressed into a tray bore from the cassette inboard edge |
| Tray (cassette) changes | Cassette | **Slot:** X 13.0–15.8, dy −27.8…+3.3, dz 5.5–11.8 (0.3 float all round; 1.7 mm top skin; 1.27 PETG to the index guide bore).<br>**Bore:** Ø3 dowel bore X 0.5–19.0 |

**Float:** the yoke is located radially **only** by its ring on the bushing, and angularly **only** by the dowel's tangential fit. Everything else has 0.3 of clearance. So the yoke does not share the cassette's bending loads.

## 3. Stop angle(s)

| | Result |
|---|---|
| First contact (stop plate ↔ yoke lobe, bisection, retracted pin) | **80.0000°**: R and L, + and −, lid 105° and 135° |
| At the ±75° index positions | Face gap 0.392 mm (at R 4.5). Pair minimum 0.300 mm (the designed axial gap between the yoke plate and the stop plate) |
| Before the stop (0.5° steps, both sides, both directions, lid 105/135) | **No other interference** |

## 4. Contact radius

- The contact band runs from R **4.50 to 5.77** (centroid **R 5.14**). The axial contact is 2.5 mm (X 15.8–18.3).
- **R 6–7 is not reachable in this envelope**, for the same reasons as S1:
  - the stop-plate corner must stay inside the hub band (dy ≥ −5) to clear the lid side-wall notch;
  - the tray bottom is 5.5 mm above the axis.
- The yoke's lobe faces run out to R 6.8, so the stop plate is the limit.

## 5. New dimensions / parameters (study values, proposed names)

| Name | Value |
|---|---|
| R1_STOP / R1_HB | 80° / 40° (lobe faces 50°, 130°; stop plate faces 210°, 330°) |
| R1_TSP / R1_TY / R1_AX | 2.5 stop plate / 2.5 yoke plate / 0.3 axial running gap |
| R1_RH / R1_RIN / R1_RS | 3.5 / 4.5 / 5.774 (= −BLY / cos 30°; tray limit 5.874) |
| R1_BUSH_OD / R1_BORE_CL | 6.0 / 0.1 (diametral) |
| R1_RRO | 5.0 ring OD / 2 (= hub-zone floor) |
| R1_FLOAT | 0.3 |
| R1_RK | 25 (drive radius) |
| R1_DD | 3.0 |
| Arm | dy −27.5…+3.0, dz 5.8–11.5 |
| Pin length (would become) | 59.3 |

## 6. Load path (explicit)

1. **Contact:** stop plate face ↔ yoke lobe face. F = T / R_c, tangential.
2. **Yoke:** the lobe (cantilever from the ring plate) carries it to the ring. The ring bears on the bushing with force **N ≈ F** and edge moment **F × 2.8** (contact X 17.05 vs ring X 14.25).
3. **Pin (fixed side):** it takes +F at the stop plate and −N / −moment from the bushing. Inboard of the bushing the residual stop moment is **0.0 N·mm**: the pair closes in metal. The torque T goes through the stop-plate key into the pin, then through the pin (torsion) to the anti-rotation plate, the dowel and the carriage (unchanged D-009 path).
4. **Yoke torque into the cassette:** only by the drive dowel. Tangential force **K = T / R_k = 50 N** at R 25. With radial float, the ring carries the rest.
5. **PETG bracket:** it sees only **K** (plus 20 % assumed friction in the float) and its moment about the bore: **60 N and 529 N·mm** at T_d, against 245 N and 2,144 N·mm in S1.
   - The index lock's own reaction (Phase 1) is **not** changed by S1-R. It still goes through the bore when the pin is engaged.

## 7. Design-case stresses (T_d = 1.26 N·m; stop force 245 N; drive force 50 N)

| Component | Stress | SF |
|---|---|---|
| Contact, crowned R10 face (Hertz line) | 576 MPa | Hardened faces required (17-4 H900 / H1025) |
| Stop plate key A/F 3.0 (t 2.5) | 189 MPa | 4.01 (301 ½-hard) |
| Stop plate sector shear | 43 MPa | 10.2 |
| Yoke lobe root bending | 56 MPa | 17.9 (17-4 H1025) |
| Yoke ring edge bearing on the bushing | 126 MPa | 11.9 |
| Yoke ring bending | 198 MPa | 5.05 (17-4 H1025) |
| **Hub pin tip double-D** (local stop couple 378 N·mm + torsion) | vM 179 | **2.32 (303)** / 5.60 (17-4 H1025) |
| Hub pin root (handling bending; the stop adds nothing) | vM 198 | 2.09 (303) / 5.04 |
| Hub pin inboard double-D torsion | vM 169 | 2.45 (303) / 5.91 |
| **PETG bracket bore, stop only** | 7.6 MPa | **3.97** RT / 1.98 hot |
| Drive dowel in the tray (foundation bound) | 2.8 MPa | 10.6 RT / 5.3 hot |
| Yoke drive arm bending | 82 MPa | 12.2 |
| Anti-rotation plate key (D-009, unchanged) | 315 MPa | 2.41 |
| Carriage PETG under the anti-rotation dowel, bound (D-009, unchanged) | 12.7 MPa | 2.36 RT / 1.18 hot |

## 8. Acceptance-case stresses (2.52 N·m; stop force 491 N; drive 101 N)

| Component | Stress | SF |
|---|---|---|
| Contact, crowned R10 | 814 MPa | Hardened only |
| Stop plate key | 378 MPa | **2.01** |
| Yoke ring bending / lobe / ring bearing / arm | 396 / 112 / 253 / 164 MPa | 2.52 / 9.0 / 5.9 / 6.1 |
| Hub pin tip double-D | vM 357 | **1.16 (303)** / 2.80 (17-4 H1025) |
| Hub pin root | vM 397 | 1.05 (303) / 2.52 (17-4) |
| Hub pin inboard double-D torsion | vM 338 | 1.23 (303) / 2.96 (17-4) |
| PETG bracket bore, stop only | 15.1 MPa | 1.98 RT |
| Drive dowel in the tray | 5.7 MPa | 5.3 |
| Anti-rotation plate key (unchanged) | 630 MPa | **1.20** |
| Carriage dowel bearing, bound (unchanged) | 25.4 MPa | **1.18** |

## 9. Safety factors — summary and material question

**Summary:**
- **At T_d:** every element of the stop path is ≥ 2.0. The minimum is the pin tip at 2.32 in 303; the D-009 downstream elements are 2.36–2.45.
- **At 2.52 N·m:** the new parts (stop plate, yoke, bushing, drive) are ≥ 2.0. Not ≥ 2:
  - hub pin sections in 303 (1.05–1.23);
  - the unchanged D-009 anti-rotation key (1.20) and carriage dowel bearing (1.18).
- Those are D-009 path limits, not S1-R ones.

**Pin material:**

| | A. 303/304 (approved) | B. 17-4PH H1025 |
|---|---|---|
| Tip / root / torsion at T_d | 2.32 / 2.09 / 2.45 | 5.60 / 5.04 / 5.91 |
| Same at 2.52 | 1.16 / 1.05 / 1.23 | 2.80 / 2.52 / 2.96 |

- **17-4PH is not required** for the stated target (SF ≥ 2 at 1.26 N·m). With the S1-R path the pin tip keeps 2.32 in 303, so the tip is no longer marginal.
- 17-4PH is needed **only** to meet the preferred SF ≥ 2 at 2.52 N·m for the pin, and to add margin against impact (§11).
- Even with 17-4PH, the D-009 chain stays near 1.2 at 2.52 N·m because of the anti-rotation key and the carriage dowel bearing. Reaching 2 there would need a thicker anti-rotation plate and a larger dowel lever or length: D-009 changes.
- **Recommendation:** keep 303 unless the owner adopts the 2.52 N·m target for the whole chain.

## 10. Tolerance analysis (stop angle relative to the ±75° index position)

The 5° margin is 0.45 mm of arc at R 5.14.

**Reference chain:** stop plate faces (EDM) → stop-plate key on the pin → pin → index-plate key → index hole → index pin → index-pin bores in the tray → drive-dowel bore in the tray → yoke drive slot (EDM) → yoke lobe faces (EDM) → yoke bore on the bushing.

- Two of these are printed-and-reamed features: the index-pin bores and the drive-dowel bore. They must be reamed from **one metal jig** so their relative position is metal-defined (±0.03).

| Contributor (±°) | D-009 fits, printed + reamed | Metal-referenced |
|---|---|---|
| Stop plate faces vs its key (EDM ±0.02) | 0.22 | 0.22 |
| Stop plate key clocking (A/F clearance 0.04 / 0.02) | 0.57 | 0.29 |
| Index plate key clocking | 0.57 | 0.29 |
| Index hole true position | 0.17 | 0.17 |
| Index pin in its hole | 0.29 | 0.29 |
| Index-pin bores vs drive-dowel bore (±0.10 / jig ±0.03) | 0.57 | 0.17 |
| Drive-dowel bore at R 25 | 0.23 | 0.07 |
| Yoke lobe faces vs bore / drive slot (EDM) | 0.27 | 0.27 |
| Drive slot fit | 0.02 | 0.02 |
| Yoke bore on the bushing (0.05 / H7-g6 0.02) | 0.56 | 0.22 |
| Bracket-bore clearance (cassette shift 0.05) | 0.40 | 0.40 |
| **Worst case** | **±3.88** | **±2.41** |
| **RSS** | ±1.32 | ±0.80 |

**Window:**
- First contact ≥ 75.5°.
- Contact + elastic over-travel ≤ 85° (an assumed cable limit; the cable route is not defined).
- The chain stiffness is about 68 N·m/rad, which gives 1.1° over-travel at T_d. So the window is **−4.5 / +3.9°**.

**Result:**
- **±80° is achievable:** worst case ±2.41° with metal referencing. With unchanged D-009 key fits and a jig it is ±3.88°, which only just fits on the + side.
- Printed-only location (S1: ±7.2°) is avoided because nothing in the angular chain depends on a printed pocket.
- The lowest possible first contact is 77.6°, so there is no engagement at ±75°.
- At 2.52 N·m the stop can reach about 84.5° (2.1° over-travel).

## 11. Impact / accidental over-rotation (inferred sensitivity; no dynamic data)

- Cassette inertia about the axis is 1,272 kg·mm² (0.35 kg). Peak torque into a linear stop is T = ω √(I k).

| k (N·m/rad) | ω 2 rad/s | 4 rad/s | 6 rad/s | 8 rad/s |
|---|---|---|---|---|
| 40 | 0.45 | 0.90 | 1.35 | 1.80 N·m |
| **68 (estimate)** | 0.59 | 1.17 | 1.76 | 2.35 N·m |
| 120 | 0.78 | 1.56 | 2.34 | 3.13 N·m |

- Assumed angular speeds: a deliberate turn is about 2 rad/s; a brisk flick is 4–6 rad/s; a slap is 8 rad/s.
- **A brisk flick reaches T_d to about 1.4 × T_d; a slap reaches the acceptance torque.** So the static 2.52 N·m case is a fair bound for a slap, not a conservative one.
- The metal stop path (≥ 2 at 2.52 for the new parts) takes this. The unchanged D-009 anti-rotation key and dowel (1.2 at 2.52) are the likely first damage under repeated slaps.
- **Contact:** hardened (≥ 17-4 H1025, preferably H900), crowned (R ≈ 10) faces keep Hertz stress at 576 / 814 MPa. Line contact would brinell.
- **Wear:** the stop plate is the cheap, replaceable part. The yoke lobe faces are hardened and are inspected with the cassette off.
- Without measured stiffness and speed, no dynamic factor is claimed. **Physical test:** drop-weight or pendulum impacts at the ±80° stop with angle measurement.

## 12. Manufacturing

| Part | Material / process / tolerance |
|---|---|
| Stop plate | 2.5 mm 301 ½-hard or 17-4PH. Outline and faces by **wire EDM** (±0.02). Double-D key A/F 3.00 +0.01/0. Faces hardened if 17-4 (H900) |
| Journal bushing | 303 or 17-4 turned, OD 6.00 g6, length 3.3. Double-D bore A/F 3.00 +0.01/0 by EDM (or a round Ø5.00 bore if keying is not needed) |
| Stop yoke | 17-4PH H1025 (H900 on the lobe faces), CNC milled from 6 mm stock + wire-EDM profile. Bore Ø6.10 H7. Lobe faces ±0.02 to the bore and drive slot; crowned R ≈ 10. Radial drive slot 3.6 × 3.02 |
| Drive dowel | ISO 2338 Ø3 × 18 m6 A1/A2 |
| Hub pin | As D-009, with the tip double-D extended to 7.3 mm; 59.3 long |
| Tray (FDM PETG) | Slot 3.3 × 6.3 × 31 (0.3 float all round). Ø3 dowel bore from the inboard edge. **Index sleeve / guide bores and the dowel bore reamed from one metal drilling jig** |
| M2 screw / washer | As D-009 |
| Tooling | Normal wire-EDM / CNC / turning service; no special machinery |

## 13. Assembly sequence (corrected) and service

**Correction to the D-009 records:** the anti-rotation check lists "cassette onto the pin, then the index plate onto the tip". That is not possible as modeled: the plate's upper part in the tray groove cannot pass the tray wall at X 13. The correct order, **documented here for review; the production specification is not changed**:

1. **Carriage sub-assembly** (as D-009): anti-rotation plate into its slot; hub pin in from the carriage outboard face; inboard M2 screw; Ø3 anti-rotation dowel.
2. **Cassette sub-assembly:**
   1. Index plate into the cassette groove (from below).
   2. Stop yoke into the tray slot (from below).
   3. Drive dowel pressed in from the cassette inboard edge through the yoke's drive slot.
   4. Index pin retracted (hold the slider).
3. **Cassette + index plate + yoke onto the pin:** slide on along −X. The pin passes the bracket bore, the index-plate key and the yoke ring bore (0.55 clearance around the pin).
4. **Bushing:** onto the pin tip into the yoke ring, seated on the index plate.
5. **Stop plate** onto the tip key.
6. **Washer + M2 screw:** clamps index plate + bushing + stop plate to the pin shoulder (threadlocker, 0.15 N·m).
7. Release the index pin.

**Removal (reverse; paths modeled):**
- (1) **Stop plate** off the tip: min 0.300 to the cassette group. The cassette stays on, so the stop plate can be **inspected and replaced in place**.
- (2) **Bushing** out of the ring: 0.050 (journal).
- (3) **Cassette + index plate + yoke** off the pin: 0.000, which is only the designed sliding fits.

**Other service items:**
- The yoke is replaced with the cassette off: press out the drive dowel, then lift the yoke out of the slot.
- The index pin, spring and cover are serviced as in D-009.
- No destructive step.

## 14. Cable clearance

- The yoke, dowel and stop plate are **≥ 6 mm** from the link cable envelope.
- They are outboard of the in-bracket pass-through (X 0.5–10.5), and the dowel is at dy −25 against a cable at dy 3.5–9.5.
- The stop limits rotation to ±80° (+ ≤ 3.9° incl. tolerance and deflection), so cable twist is bounded whenever the pin is retracted.
- **Constraints for the open cable-exit route:**
  - exit the bracket upward within X 0.5–10.5;
  - avoid the tray slot (X 13–15.8, dy −27.8…+3.3) and the dowel line (dy −25, X 0.5–19);
  - avoid the index-lock channel (dy 3.5–7.3, X 13–40.5).
- The cable route is **not validated**.

## 15. Remaining risks / open items

1. **The D-009 hub-bracket shortfall (Phase 1) is not addressed by the floating yoke.** The lock reaction still loads the PETG bore: SF 1.88 at handling.
   - Option: make the yoke **rigid** (fixed in the tray, bore line-reamed coaxial with the bracket bore) so it also acts as the outboard cassette bearing.
   - Cost: overconstraint and coaxiality control, and the yoke–tray joint then carries the cassette's bending (≈ 140 N handling / 280 N at T_d, inferred).
   - Needs its own study and approval.
2. **Tray slot** near the hub (31 × 6.3 of the 8 mm tray): the tray structure is undesigned. Check it when the cassette is designed.
3. **Thumb access:** the stop lobe ends at X 18.3 and the tab slot starts at 22.4, leaving about 4.1 mm of finger room. Needs an ergonomic check.
4. **Float must stay open:** the 0.3 float has to exceed bracket-bore play plus PETG deflection under handling (inferred small at handling). If it closes, the yoke starts sharing cassette loads.
5. **Precision parts:** part count +4 per side (bushing, stop plate, yoke, dowel); jig reaming of printed bores.
6. **Downstream D-009 margins at 2.52 N·m** (1.18–1.23) and impact (§11).
7. **Cable exit route** undefined (§14).

## 16. Regression (S1-R table, modeled)

| Check | Result |
|---|---|
| Rigid groups | OK |
| Pose matrix (lid 0/105/120/135 × stowed / R / L / both; tilts ±75; slides) | **0 unexpected violations** |
| Guided fits | Unchanged D-009 values. New: bushing–yoke 0.050 (journal), yoke–pin 0.550, yoke–index plate 0.500, yoke–rail 0.665, stop plate–yoke 0.300 |
| F3 bracket–floor | 1.000 |
| **D-009 A** | 11 positions, 0.050, positive lock |
| **D-009 B** | Free within ±75; retracted pin 1.000 from the plate |
| **D-009 C** | Stow only at 0° (others blocked at 7.1 mm) |
| **D-009 D** | Slide sweep clean |
| **D-009 E / F / G** | Unchanged |
| Lid sweep vs base | Clean; rear-plug conflict unchanged |
| **Hard-stop sweep** | **80.0000°** everywhere; no other interference |
| Service paths (1)–(3) | ≥ 0 |
| Cable envelope | ≥ 6 mm |

**Onshape scratch:** not run (0 API calls). The local engine has matched the kernel exactly in every earlier cross-check, and this is not a candidate for integration yet.

## 17. Files

**New:**
- `CAD/tools/s1r_stop_study.py`
- `CAD/tools/d009_load_reassessment.py`
- this report
- `round_e_d009_load_reassessment.md`

**Changed:**
- `CAD/tools/s1_stop_study.py`: sweep helper parameterised for reuse (study tool).
- `round_e_s1_hard_stop_study.md`: erratum on the pin-root figures.
- `docs/build-log.md`, `docs/decisions.md`, `CLAUDE.md`: status.

**Not changed:** production geometry, `nomad.yaml`, spec, `e_lid_layout.py`, FeatureScript, harnesses, persistent Onshape.
