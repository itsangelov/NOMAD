# Round E — D-009 Index-Lock Load Reassessment (transverse reaction included)

**Status:**
- Analysis only. No change to geometry, `nomad.yaml`, the spec, FeatureScript, Onshape or Git.
- **Tool:** `CAD/tools/d009_load_reassessment.py` (NON-PRODUCTION, read-only). It prints every number below.

**Evidence levels:**
- Geometry: *modeled* (the current D-009 E-lid model).
- Loads and stresses: *inferred* (hand statics with the models of the approved reports; no FEA; nothing tested).

**Trigger:** the S1 study found that the hub load check and the anti-rotation check treated the pin-tip index load as a pure torque.

---

## 1. Verdict

**The corrected model changes one subsystem: the PETG hub bracket around the 10 mm bore.**
- Hub-pin root: unchanged.
- Other hub-pin sections: essentially unchanged.
- Index pin, index plate, keys, anti-rotation plate, dowel, carriage and screws: unchanged, except a small tip-key increase.

**What changes:** the index lock's transverse reaction flows through the bore and adds force and moment there.
- At the hub load check's own basis (handling load, SF ≥ 2), the bracket drops **below 2**:

| Check | Before | Corrected |
|---|---|---|
| Bearing | 2.60 | **1.88** |
| Tear-out | 2.56 | **1.73** |
| Peak ligament tension | 2.39 | **1.61** |

- **The existing D-009 geometry does not fully satisfy the previously defined acceptance requirements** (§7).
- **It cannot be fixed without a geometry change** while the cassette hub stays PETG (§8).
- The minimum geometry change is a second, outboard metal bearing for the cassette on the pin tip (§9).

**Correction to the S1 study (§11):** the S1 report said the pin root drops from SF 2.09 to 1.75 (lock) and to 1.23 (S1). **That was wrong.**
- The root is unaffected, because the reaction pair is internal to the pin + cassette system.
- The S1 bracket-bore finding stands.

## 2. Corrected load path

**Bodies:**
- **Hub pin:** a cantilever from the carriage (root at the carriage outboard face, X −11).
- **Cassette:** rigid; it sits on the pin through the hub-bracket bore (X 0.5–10.5, centre 5.5).

**External loads on the cassette** (the hub load check's handling case, ×2 at design, ×4 at acceptance):
- P = 5 N at an outboard corner, along the panel normal. The far corner is 114.3 from the axis at X 148, which gives the largest torque.
- The weight W = 3.43 N at X 74.25, in any direction.
- T = P·114.3 + W·17.2 = 0.63 N·m. The design torque T_d is 1.26 N·m.

**Internal pair (the index lock):**
- The cassette's index pin pushes the index plate with F = T / r = T / 10, tangential at the index-pin angle (57.5° + tilt), at X 11.75.
- The index plate passes F and T to the pin through the double-D key.
- The cassette receives −F at the same X.

**Statics (exact):**
- The bore carries **V = P + W − F** and **M = 142.5 P + 68.75 W − 6.25 F** (vectors, moment about X 5.5).
- The pin carries +F at X 11.75 plus the bore loads.
- **Inboard of the bore, F cancels:** −16.5 − 6.25 + 22.75 = 0 at the root. So the pin root, the link section, the carriage bore and the anti-rotation plate see only P, W and T.
- **Numerical check:** the pin moment at X −11 / 0 / 0.5 with and without the index force agrees to 0.01 N·mm (2117.26 / 2117.27 N·mm in the check case).
- **What F does load:** the bore (force + moment), the pin inside and just outboard of the bore, the tip key (transverse bearing), and the plate.

**Direction:**
- For a far-corner push, the index force makes 57.5° with the panel normal and **adds** to the bore moment (|cos| 0.537).
- The script also sweeps the near corner, tilts −75…+75 and 24 gravity directions, and takes the worst case.

**Retention and fasteners:** the M2 screws carry only axial stow/deploy loads. The transverse loads go through the keys and bores.

## 3. Corrected loads (worst over corner / tilt / gravity direction)

| Case | T (N·m) | Index force F | Bore V / M (N, N·mm), corrected | Bore V / M, previous model | Pin root M (N·mm) |
|---|---|---|---|---|---|
| Handling (0.35 kg + 5 N) | 0.63 | 63 N | 69 / 1,218 | 8 / 949 | 1,088 (unchanged) |
| Design T_d | 1.26 | 126 N | 139 / 2,435 | 17 / 1,897 | 2,175 (unchanged) |
| Acceptance 2 × T_d | 2.52 | 252 N | 277 / 4,870 | 34 / 3,794 | 4,351 (unchanged) |

## 4. Corrected stresses and safety factors (room temperature; hot PETG = half the allowable)

| Component | Handling | T_d | 2.52 N·m | Allowable |
|---|---|---|---|---|
| Hub pin root (round, bending + torsion) | 99 MPa / **4.18** | 198 / **2.09** | 397 / 1.05 | 303: 415 |
| Hub pin inside the bore (max, round) | 92 / 4.50 | 184 / 2.25 | 369 / 1.13 | 415 |
| Hub pin at the plate / tip double-D | 85 / 4.89 | 170 / 2.44 | 340 / 1.22 | 415 |
| Hub pin inboard double-D (torsion) | 85 / 4.90 | 169 / 2.45 | 339 / 1.23 | 415 |
| **Bracket bore bearing** | 16.0 / **1.88** | 32.0 / **0.94** | 64.0 / 0.47 | PETG 30 (hot 15) |
| **Bracket tear-out under the pin** | 8.7 / **1.73** (across layers 1.15) | 17.4 / 0.86 | 34.8 / 0.43 | 15 in-layer / 10 across |
| **Bracket ligament tension, Kt 2.5 peak** | 21.7 / **1.61** (across layers 0.92) | 43.5 / 0.81 | 86.9 / 0.40 | 35 / 20 |
| Index pin bending (double shear) | 178 / 5.61 | 357 / **2.80** | 714 / 1.40 | Hardened ≥ 1,000 |
| Index pin shear | 18 / 32 | 36 / 16 | 71 / 8.1 | |
| Index plate bearing / web bending | 28 / 27; 49 / 15 | 56 / 13.5; 99 / 7.7 | 112 / 6.8; 198 / 3.8 | 301 ½-hard: 758 |
| Tip key, torque only (previous) | 158 / 4.81 | 315 / 2.40 | 630 / 1.20 | 758 |
| **Tip key + transverse F on one flat** | 168 / 4.51 | 336 / **2.25** | 673 / 1.13 | 758 |
| Anti-rotation plate key (F does not reach it) | 158 / 4.81 | 315 / 2.40 | 630 / 1.20 | 758 |
| Carriage PETG under the Ø3 dowel, bound (k 2,500) | 6.4 / 4.72 | 12.7 / **2.36** (hot 1.18) | 25.4 / 1.18 | 30 (hot 15) |
| Carriage pin bearing (28.4 engaged) | 1.7 / 18 | 3.4 / 8.9 | 6.7 / 4.5 | 30 |
| M2 screws (axial 100 N impact) | 48 / 9.3 | Same | Same | A2-70 450 |

## 5. Weakest components

1. **PETG hub bracket around the bore.**
   - Handling: bearing 1.88, tear-out 1.73 (1.15 across layers), peak ligament tension 1.61 (0.92 across layers).
   - T_d: 0.81–0.94.
   - Hot: roughly half of each.
2. **Carriage PETG under the anti-rotation dowel**, hot: 1.18 at T_d. This is unchanged and was already accepted.
3. **Metal parts at 2.52 N·m:** tip key 1.13, anti-rotation key 1.20, pin root 1.05. All are unchanged or nearly so; they meet "no yield at 2.52" only barely.

## 6. Comparison with the published D-009 values

| Item | Published | Corrected | Change |
|---|---|---|---|
| Pin root (303) at T_d | 2.09 | **2.09** | None (exact statics; the S1 study's 1.75 is withdrawn) |
| Pin inboard / tip double-D at T_d | 2.44 | 2.45 / 2.44 | None |
| Index pin bending at T_d | 2.80 | 2.80 | None (already a transverse model) |
| Index plate bearing / web at T_d | 13.5 / 7.7 | 13.5 / 7.7 | None |
| Tip key at T_d | 2.41 | **2.25** | −7 % (transverse F on a flat) |
| Anti-rotation key / dowel bound at T_d | 2.41 / 2.36 | 2.40 / 2.36 | None |
| Hub-bracket bore bearing, handling | 2.6 | **1.88** | −28 % |
| Hub-bracket tear-out, handling (favourable / unfavourable) | 2.5 / 1.7 | **1.73 / 1.15** | −31 % |
| Hub-bracket peak ligament tension, handling | 2.4 / 1.4 | **1.61 / 0.92** | −33 % |
| Hub-bracket bearing, hot handling | ≈ 1.4 (load check §10) | ≈ 0.94 | |

**Approximations in the previous analyses:**
- **Hub load check:** it computed the bore from P and W only. The index lock was "not designed"; the torque was only an input to it.
- **Anti-rotation check:** it evaluated the torque chain as pure torque, and the pin root from the load check's bending (correct for the root).
- **What was missing:** neither combined the lock's force F with the bore. The bore is the only link between the cassette and the pin, so it must carry F and its 6.25 mm moment arm.
- **The bore model itself remains an approximation:** a rigid pin in a short bore with a linear pressure distribution. Pin/bore clearance would raise the edge pressure; local PETG yielding would redistribute it. It is unchanged here so the numbers compare like for like.

## 7. Does the existing D-009 geometry satisfy the previously defined acceptance requirements?

| Requirement (source) | Result |
|---|---|
| D-009 lock torque path: SF ≥ 2 at 1.26 N·m, room temperature, conservative models (anti-rotation check; manufacturing check) | **Yes.** Index pin 2.80, plate 7.7, tip key 2.25, pin 2.09–2.45, anti-rotation key 2.40, dowel 2.36 |
| No yield at 2.52 N·m (the same requirement restated) | Yes for the metal parts (1.05–1.40), barely |
| **Hub bearing path: SF ≥ 2 at handling, favourable print orientation (hub load check / F3)** | **No.** Bearing 1.88, tear-out 1.73, peak tension 1.61. The previously accepted unfavourable-orientation values (1.7 / 1.4) fall to 1.15 / 0.92 |
| Hot handling (load check §10 noted ≈ 1.4) | **No.** ≈ 0.94 bearing |

**Overall:** the D-009 lock's own components are acceptable. The **PETG hub bracket that now carries the lock's reaction is not.**
- Even without the lock, the bracket was only SF 1.30 at T_d-level loads. It was accepted against the handling basis, never against 2 × handling.

## 8. Can it be fixed without changing geometry?

**Not with PETG as specified.**
- To reach SF 2 at the handling basis, the bracket needs roughly:
  - bearing allowable ≥ 32 MPa (PETG 30);
  - in-layer shear ≥ 17.4 MPa (PETG 15);
  - peak tension ≥ 43.5 MPa (PETG 35).
- At T_d-level loads it needs twice those.

**Non-geometric options (all need owner decisions and physical validation):**
- Print the cassette hub region in a stronger material (e.g. PC or PA12-CF). Handling-level SF 2 is plausible; T_d-level is not.
- Re-baseline the hub criterion. This is a requirement change, not a fix.
- Neither is recommended as the only measure.

## 9. Minimum necessary geometry change (not implemented)

**A second, outboard metal bearing for the cassette on the pin tip.**
- A stainless ring, rigidly fixed to the cassette tray, runs on a clamped bushing outboard of the index plate (X ≈ 13–15.5).
- It is made coaxial with the bracket bore by line reaming.
- The cassette is then supported at two stations about 8.75 mm apart. The bore moment becomes a force couple instead of an edge load on a 10 mm PETG bore.

**Rough numbers (inferred):**

| Case | Couple force | PETG bore bearing | Load into the tray (two Ø3 dowels along X, foundation bound) |
|---|---|---|---|
| Handling | 1,218 / 8.75 ≈ 139 N (+ V share) | ≈ 3.5 MPa (SF ≈ 8.6) | ≈ 4.9 MPa (SF ≈ 6) |
| T_d | ≈ 278 N | ≈ 7 MPa (SF ≈ 4.3) | ≈ 9.8 MPa (SF ≈ 3) |

- This is the same hardware family as the S1-R yoke. If the S1-R yoke is made **rigid** (coaxially reamed) instead of floating, it provides this bearing.
- Trade-off: two coaxial bearings (line reaming, overconstraint), and the yoke–tray connection then carries the cassette's bending loads (§ S1-R report).
- A steel bushing in the existing bore alone is not enough. The 17 × 10.5 bracket envelope leaves only about 1.5 mm of PETG wall around a larger bore, so tear-out gets worse.

## 10. Uncertainty

- **Bore pressure distribution:** linear rigid-pin model; clearance and PETG yielding are not modeled.
- **Allowables:** the conservative printed-PETG values of the load check; not measured.
- **Load combination:** worst-case alignment of gravity over 24 directions and the far-corner push. The near corner gives a smaller T and partial cancellation.
- **Panel mass:** upper bound 0.35 kg.
- **Physical validation needed:** a hub-bracket coupon under index-force + bending loading (P0.2 class).

## 11. Correction to `round_e_s1_hard_stop_study.md`

- **§7–§9 of that report state that the S1 stop couple, and the approved lock's reaction, reduce the hub-pin root SF** (lock 2.09 → 1.75; S1 1.23 / 0.62). **That is incorrect.**
  - Those figures added a couple F × (x_contact − 5.5) at the root.
  - They omitted the equal and opposite moment the bracket bore passes back to the pin.
  - The root sees only the external loads, so its SF is **2.09 at T_d** in both cases.
- **The other S1 findings stand:** bracket bore, pin tip, tolerance and the variant A comparison.
- An erratum note has been added at the top of the S1 report. The rest of it is kept as the analysis record.
