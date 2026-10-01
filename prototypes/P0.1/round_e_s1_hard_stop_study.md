# Round E — D-009 S1 Solar Tilt Hard-Stop Feasibility Study

> **ERRATUM (2026-09-28, `round_e_d009_load_reassessment.md` §11):** the hub-pin **root** results in §7–§9 are wrong.
> - Affected figures: "pin root, stop couple only / + design handling bending" 2.12 / **1.23** at T_d and 1.06 / 0.62 at 2.52, and the "pre-existing" lock value **2.09 → 1.75**.
> - The stop (or index) force and its reaction are internal to the pin + cassette system. The bracket bore passes the matching moment back to the pin, so the root sees only the external loads. **Root SF is 2.09 at T_d** in both cases.
> - The **bracket-bore** results, the pin-tip value, the tolerance analysis and the verdict (FAIL, driven by the PETG bore and tolerance) stand.

**Status:**
- This is a focused study only. Nothing here is approved geometry.
- No change to `nomad.yaml`, the spec, `NOMAD_E_Prototype.fs`, the harness, Onshape or Git.

**Tool:** `CAD/tools/s1_stop_study.py` (NON-PRODUCTION, read-only).
- It builds the S1 candidate in memory on top of the current D-009 model in `e_lid_layout.py`.
- It reruns the full check set and prints every number in this report.
- S1 inputs are study values pinned in the script. They are not YAML parameters.
- Reproduce: `py CAD/tools/s1_stop_study.py` (about 3.5 min).

**Evidence levels:**
- Geometry: *modeled* (exact 2-D regions extruded along X).
- Loads, tolerances and impact: *inferred* (hand models of the approved reports; stated assumptions).
- Nothing is physically tested.
- No Onshape scratch run (§16).

---

## 1. Verdict — **S1: FAIL (NEEDS REDESIGN)**

**What works:** the geometry.
- The modeled candidate stops at exactly **±80.000°** on both sides, in both directions, at lid 105° and 135°.
- No other interference occurs before the stop.
- All ±75° lock positions, the stow interlock, slides and service paths are unchanged.

**What fails is structural:**
- A single-sided stop at the pin tip puts its whole contact force (**245 N at 1.26 N·m**, contact R 5.14) onto the hub pin **8.75 mm outboard of the 10 mm PETG hub-bracket bore**.
- **Bracket bore:** peak bearing 30.7 MPa for the stop alone at T_d (**SF 0.98**). With the design handling bending it is 49.9 MPa (**SF 0.60**).
- **Hub-pin root (303):** SF **1.23** at T_d with the handling bending.
- At 2.52 N·m almost the whole chain is below 2.

**Tolerance:**
- The 5° margin is only 0.45 mm at the achievable contact radius.
- With a printed-located stop block, the worst-case stop spread is ±7.2°, against a window of about −4.5/+3.6°.
- Worst case is not met even with precision metal referencing (±4.36°).

**Pre-existing D-009 finding:** the analysis also exposed the same transverse-reaction effect in the approved index lock (§9).

**Not ready for persistent Onshape implementation. S2 and S3 were not chosen.** The smallest redesign is proposed in §17.

## 2. Exact stop geometry (variant B, as modeled; right side; left = rotated 180° about the lid's vertical centre)

**Frame:** X is stowed lid X; dy/dz are from the tilt axis (Y 131.8, Z 57.5). Angles are measured from +dy toward +dz, cassette frame = lid frame at 0° tilt.

| Part | Group | Geometry |
|---|---|---|
| **Stop plate** (new, 3 mm stainless) | Carriage side, keyed | X **12.5–15.5**, stacked against the index plate's outboard face on the same A/F 3.0 double-D. **Outline:** hub ring R **3.5** from −30° to 210° (over the top); radial face at **210°** from R 3.5 to R **5.774**; arc R 5.774 from 210° to 240°; flat at the hub-zone floor dz −5.0; arc R 5.774 from 300° to 330°; radial face at **330°** back to R 3.5. Key hole double-D A/F 3.0 |
| **Stop block** (new, steel) | Cassette | **Lobe** X 13.0–16.0: inner arc R **4.5** from 50° to 130°, radial faces at **50°** and **130°** up to the tray bottom (dz 5.5, dy ±4.615), embedded 1.0 into the tray (dy ±4.5). **Tab** X 16.0–18.0 flush in the same pocket (dz 5.5–6.5, dy ±4.5). Two M2 countersunk screws into heat-set inserts (not modeled) |
| Tray pocket (cassette sub) | Cassette | X 13.0–18.0, dy ±4.5, dz 5.5–6.5, open downward. PETG to the index guide bore 1.32 |
| Hub pin | Carriage | Tip double-D extended to X **15.5**. **Length 56.5** (was 53.5) |
| Tip M2 screw + washer | Carriage | Moved outboard to X 15.5–17.8 |

**Variant A (formed flange on the index plate): compared analytically, not modeled.**
- **Shape:** to put a stop face at 210°/330° in X 13–15.5, the 1.5 mm index plate would need two flaps slit from its lower hub zone and folded 90° about radial fold lines. Each flap is about 2.3 radial × 3 along X.
- **Strength:** each flap is a cantilever from its fold. At 245 N with a ≈ 2.5 mm arm, σ ≈ 612 / (2.3 × 1.5² / 6) ≈ **710 MPa**, SF ≈ 1.07 on 301 ½-hard.
- **Manufacturing:** it needs forming on the reamed, tight-tolerance plate. The inside bend radius is ≥ 1.5 t, with hole distortion and springback risk, and it must be formed before reaming or re-fixtured after.
- **Load path:** it has the same transverse-reaction problem as variant B.

| | A (formed flange) | B (stacked stop plate, modeled) |
|---|---|---|
| Stop-element strength at T_d | ≈ 1.1 (flap) | ≥ 4.8 (plate) |
| Transverse reaction on bore / pin root | Same (fails) | Same (fails) |
| Tolerance | Worse (formed faces) | EDM faces possible |
| Manufacturing | Forming a reamed precision plate | Flat plate, standard |
| Part count | +0 plates, +1 block | +1 plate, +1 block |
| Serviceability | Index plate becomes the wear part | Stop plate and block separately replaceable |
| Cable clearance | Same | Same |

**Variant A is inferior on every count, so B is the S1 candidate.**

## 3. Stop angle(s)

| Case | First contact (stop plate ↔ stop block, bisection) |
|---|---|
| Right / left, lid 105° and 135°, + and − | **80.0000°** (all eight cases) |
| Stop-pair gap at the ±75° index positions | **0.392 mm** (all four) |

## 4. Contact radius

The contact band on the faces runs from R **4.50 to 5.77**; the centroid is **R 5.14**. The axial contact is 2.5 mm (X 13.0–15.5, centre 14.25).

**The R 6–7 target is not reachable in this envelope:**
- The stop plate's corner must stay inside the hub band dy ≥ −5, or it breaks MIN_GAP to the lid side-wall notch in transit. That limits R to 5.774.
- The tray bottom limit (MIN_GAP at the stop) is R 5.874.
- The block cannot reach below R 4.5 without closing MIN_GAP to the plate's hub ring.

## 5. New dimensions / parameters (study values, proposed names)

| Name | Value | Meaning |
|---|---|---|
| S1_STOP | 80° | Stop angle |
| S1_HB | 40° | Stop block half-angle (faces at 90 ± 40°) |
| S1_TSP | 3.0 | Stop plate thickness |
| S1_LIG | 1.0 | Stop plate hub ligament over the key → S1_RH 3.5 |
| S1_RIN | = S1_RH + MIN_GAP → 4.5 | Block inner radius |
| S1_RS | = −BLY / cos(S1_HB + S1_STOP − 90) → 5.774 | Plate outer radius (≤ tray limit 5.874) |
| Stop plate faces | S1_PHI2 + S1_STOP = 210°; S1_PHI1 − S1_STOP = −30° | |
| S1_LOBE / S1_EMB / S1_BWE | 3.0 / 1.0 / 4.5 | Block lobe length / embedment / embedded half-width |
| Block X | GX1 (13.0) … GDX1 − MIN_GAP (18.0) | |
| SOLAR_HUB_PIN_LENGTH (would become) | 56.5 | |

## 6. Load path

**Stop force:** F = T / R_c, with the contact force tangential on the radial faces.

**Chain:** cassette tray → (2 × M2 heat-set inserts + 1 mm pocket) → steel stop block → contact → stop plate → A/F 3.0 key → hub pin (torsion) → anti-rotation plate → Ø3 dowel → PETG carriage → rail → lid. This is the same metal torque path as the lock from the key onward.

**Transverse reaction:** the contact force is not a couple. The pin receives +F at X 14.25, and the cassette's only bearing, the hub-bracket bore (X 0.5–10.5), reacts −F.
- **Pin:** it carries a couple F × 8.75 all the way to its root, on top of the handling bending.
- **Bracket bore:** it carries F plus the moment F × 8.75.
- This is the governing mechanism of the failure.

**Direction:** the stop force makes an angle of 50°/130° with the panel normal, so it partly adds to the handling bending (|cos| 0.643, worst side taken).

## 7. Design-case stresses (T_d = 1.26 N·m, F = 245 N)

| Component | Stress | Allowable | SF |
|---|---|---|---|
| Contact, faces aligned (flat) | 77 MPa | — | — |
| Contact, crowned R 10 face (Hertz line, realistic misalignment) | 576 MPa | Hardened steel ~2 σy | ≥ 2 only if hardened (e.g. 17-4PH H900) |
| Stop plate key A/F 3.0 (t 3) | 158 MPa | 758 (301 ½-hard) | 4.81 |
| Stop plate sector shear | 36 MPa | 440 | 12 |
| Pin tip double-D at X 11 (bending F × 3.25 + torsion) | vM 208 | 415 (303) | **2.00** |
| Pin root, stop couple only | vM 196 | 415 | 2.12 |
| **Pin root, stop couple + design handling bending** | vM **336** | 415 | **1.23** |
| **Bracket bore PETG, stop only** | **30.7 MPa** | 30 | **0.98** |
| **Bracket bore PETG, stop + design handling** | **49.9 MPa** | 30 | **0.60** |
| Stop block → tray, 2 × M2 inserts (Ø3.2 × 4) | 7.3 MPa | 30 RT / 15 hot | 4.09 / 2.05 |
| Stop block → tray, 1 mm pocket wall alone | 37.6 MPa | 30 | 0.80 (the inserts must carry it) |
| Anti-rotation plate key (unchanged) | 315 MPa | 758 | 2.41 |
| Pin inboard double-D torsion (unchanged) | vM 169 | 415 | 2.45 |
| Carriage dowel bearing, conservative bound (unchanged) | 12.7 MPa | 30 / 15 | 2.36 / 1.18 |

## 8. Acceptance-case stresses (T = 2.52 N·m, F = 491 N)

| Component | Stress | SF |
|---|---|---|
| Contact, crowned R 10 | 814 MPa | Hardened steel only |
| Stop plate key | 315 MPa | 2.41 |
| Pin tip double-D | vM 416 | **1.00** |
| Pin root, couple only / + handling | vM 392 / 673 | **1.06 / 0.62** |
| Bracket bore, stop only / + handling | 61 / 100 MPa | **0.49 / 0.30** |
| Stop block → tray (inserts) | 14.7 MPa | 2.04 RT / 1.02 hot |
| Anti-rotation plate key (unchanged) | 630 MPa | **1.20** |
| Pin inboard double-D torsion (unchanged) | vM 338 | **1.23** |
| Carriage dowel bound (unchanged) | 25.4 MPa | **1.18** |

The unchanged D-009 path elements (key, pin torsion, dowel) cannot reach SF 2 at 2.52 N·m. They were sized for SF 2 at 1.26 N·m.

## 9. Safety factors — critical components (summary, T_d / T_acc)

| Component | T_d | T_acc | Meets target? |
|---|---|---|---|
| **Hub-bracket bore (PETG)** | **0.60** (0.98 stop only) | 0.30 | **NO** |
| **Hub-pin root (303)** | **1.23** (2.12 stop only) | 0.62 | **NO** |
| Pin tip double-D (303) | 2.00 | 1.00 | Marginal / no |
| Stop block → tray | 4.09 RT / 2.05 hot | 2.04 / 1.02 | Yes at T_d |
| Stop plate key / sector | 4.81 / 12 | 2.41 / 6.1 | Yes |
| Contact | Hardened, crowned face required | — | Conditional |
| Downstream D-009 path (plate key, pin torsion, dowel) | 2.41 / 2.45 / 2.36 | 1.20 / 1.23 / 1.18 | Yes at T_d only |

**Pre-existing D-009 finding (not caused by S1; reported, not changed).** The approved index lock has the same transverse reaction: 126 N at X 11.75, a 6.25 mm arm to the bore.

| Check | Approved report | With the lock reaction | Load level |
|---|---|---|---|
| Pin root (303) | 2.09 | **1.75** | T_d |
| Bracket bore | 2.60 | **1.87** | Handling (the hub load check's basis) |
| Bracket bore | 1.30 | 0.93 | T_d |

The hub load check and the anti-rotation check treated the tip torque as a pure torque. This needs an owner decision independent of S1. The redesign in §17 also fixes it.

## 10. Tolerance analysis (stop angle relative to the ±75° index position)

The 5° margin is 0.45 mm of arc at R 5.14.

**Contributors (±°):**

| Contributor | As modeled | Improved |
|---|---|---|
| Stop plate face vs key: laser ±0.10 / wire-EDM–CNC ±0.02 | 1.12 | 0.22 |
| Stop plate key clocking (A/F clearance ≤ 0.04) | 0.57 | 0.57 |
| Index plate key clocking | 0.57 | 0.57 |
| Index hole true position | 0.17 | 0.17 |
| Index pin in hole | 0.29 | 0.29 |
| Index pin bores in the printed tray | 0.57 | 0.57 |
| Stop block location: FDM pocket ±0.20 + face ±0.05 / metal-referenced ±0.05 + 0.05 | 2.79 | 1.12 |
| PETG shrink | 0.28 | 0 |
| Bracket-bore clearance | 0.84 | 0.84 |
| **Worst case** | **±7.20** | **±4.36** |
| **RSS** | ±3.30 | ±1.76 |

**Elastic over-travel under load:** 1.4° at 1.26 N·m and 2.8° at 2.52 N·m (chain stiffness ≈ 52 N·m/rad, inferred).

**Window (assumed):**
- First contact ≥ 75.5°, so the pin seats at ±75° without preload.
- Contact + deflection ≤ 85°, the assumed cable limit; the cable route is not defined.
- This allows **−4.5 / +3.6°** of error.

**Result:**
- **±80° cannot be held reliably with FDM-located stop parts.** Worst case ±7.2°; even RSS ±3.3° only barely fits.
- It needs a precision stop plate (EDM/CNC) **and** a stop block referenced to the index sleeve by metal features. Even then the worst case (±4.36°) exceeds the +3.6° side; RSS ±1.76° fits.
- Key clocking of two separate plates (±0.57° each) is a large fixed share. Cutting the stop faces and index holes in one part, or pinning the two plates together, would remove it.

## 11. Impact / wear

**A static 2.52 N·m is not a conservative bound for a swung cassette.**
- Cassette inertia about the axis is ≈ 1,272 kg·mm² (0.35 kg).
- For a rigid cassette hitting a linear stop, peak torque T = ω √(I k).

| Chain stiffness k | ω 2 rad/s | 4 rad/s | 6 rad/s | 8 rad/s |
|---|---|---|---|---|
| 25 N·m/rad | 0.36 | 0.71 | 1.07 | 1.43 N·m |
| 52 N·m/rad (estimate) | 0.51 | 1.03 | 1.54 | 2.06 N·m |
| 100 N·m/rad | 0.71 | 1.43 | 2.14 | 2.85 N·m |

Assumed angular speeds:
- a deliberate turn is about 2 rad/s;
- a brisk flick is 4–6 rad/s (90° in about 0.3 s);
- a slap is 8 rad/s.

**Findings:**
- A brisk flick reaches T_d, and a slap reaches the acceptance torque. A stiffer stop is worse.
- A precise dynamic factor cannot be given without measured stiffness and speeds. The table is the sensitivity.
- Line or edge contact on 2.5 mm of face will brinell and wear under repeated impacts.
- Needed:
  - a **hardened, crowned, replaceable** steel contact (the stop block is the sacrificial part, screwed and not glued);
  - an inspection interval.
- A thin compliant layer behind a hard stop would cut the peak. It must not become the limiting element, which the "structural stop" requirement forbids.

## 12. Manufacturing (if pursued)

| Part | Requirement |
|---|---|
| Stop plate | 3 mm 301 ½-hard or 17-4PH. Outline laser + faces finished, or wire EDM (needed for tolerance). Double-D key A/F 3.00 +0.02/0 by EDM / CNC. Could share a drawing and order with the index plate |
| Stop block | 17-4PH H900 or hardened 420: CNC or wire EDM; radial faces crowned R ~10, hardened. Two M2 countersunk holes. Located by reamed features relative to the index sleeve (for the tolerance) |
| Hub pin | 56.5 long (+3); longer tip double-D |
| Tray | Pocket (printed, cleaned); 2 × M2 heat-set inserts |
| Tooling | Normal laser / EDM / CNC service; no special machinery |

## 13. Serviceability (modeled paths)

**Assembly order (applies to D-009 itself):** the index plate must be placed in the cassette groove **before** the cassette slides onto the pin. After the cassette is on, it cannot go on axially, because the tray wall at X 13 blocks the plate's upper part. The anti-rotation check's step order (cassette, then plate) is not feasible as modeled.

**Service paths (modeled):**
1. **Stop plate:** it slides off the tip past the stop block (min 1.000 over 20 mm).
2. **Cassette + index plate:** after the tip screw and stop plate are off, they slide off the pin (0 = the designed bore and key sliding fits; nothing else).
3. **Stop block:** it drops out of its open pocket once the two screws are out, with the cassette removed.

**Other service items:**
- The index pin, spring and cover are serviced exactly as in D-009; the stop parts are outside the cover and channel (X ≥ 19).
- Both stop parts are visible from below when deployed.
- No destructive step.

## 14. Cable clearance

- The stop parts are at X ≥ 12.5.
  - The link cable envelope (X ≤ 0.5) is ≥ 6 away.
  - The in-bracket cable pass-through (X 0.5–10.5) is ≥ 2.0 away.
- With the stop, rotation is limited to ±80°. The cable twist is then bounded by geometry, but only to the extent the stop holds (§7–§10).
- **Constraint for the open cable-exit item:** the solar cable must leave the bracket into the tray inside X 0.5–10.5. It must not run along the tray bottom at X 13–18, where the stop block is.
- The cable route itself is **not** validated.

## 15. Regression results (S1 table, modeled)

| Check | Result |
|---|---|
| Rigid groups | OK |
| Pose matrix (lid 0/105/120/135 × stowed / R / L / both; tilts ±75 in 15° steps; slides) | **0 unexpected violations** |
| Guided fits | Unchanged. New: stop block–index plate 0.500 (axial, like the groove); stop pair ≥ 0.392 within ±75 |
| F3 bracket–floor | 1.000 over the full travel |
| **D-009 A** | 11 positions, pin–hole 0.050, positive lock at every half-step |
| **D-009 B** | Free within ±75; retracted pin 1.000 from the plate; first blocked at 82.5 in 2.5° steps (the stop at 80.0 is found by the fine sweep) |
| **D-009 C** | Stow only at 0°; others blocked at 7.1 mm |
| **D-009 D** | Slide sweep clean |
| **D-009 E / F / G** | Unchanged |
| Lid sweep vs base | Clean. Rear-plug conflict unchanged (−6.6 at 135°) |
| **Hard-stop sweep** (retracted, 0.5° steps + bisection, both sides, both directions, lid 105/135) | Contact **80.0000°**; **no other interference before it** |

**Minimum clearances over 0…stop:**

| Pair | Clearance |
|---|---|
| Stop block–index plate | 0.500 |
| Stop plate–tray | 1.335 |
| Stop block–tip screw / hub pin | 2.000 |
| Stop plate–bracket | 2.000 |
| Stop plate–index pin | 3.592 |
| Stop plate–cover / sleeve | 3.66 / 3.68 |
| Slider, spring, carriage, rail, lid, cable keep-outs, hinge | ≥ 6 |

**Production files:** unchanged. `e_lid_layout.py --check` and `yaml_to_featurescript.py --check` pass.

## 16. Onshape scratch validation

**Not performed (0 API calls).**
- S1 fails on structure, so kernel-confirming a geometry that will change is not worth the allocation.
- The local region engine has matched the kernel exactly in every earlier cross-check.
- A kernel check belongs with the redesigned candidate.

## 17. Remaining risks and the smallest necessary redesign

**Why S1 as conceived cannot pass:**
- Any single-contact stop outboard of the hub bracket loads the short PETG bore and the pin root with T/R × (arm).
- The arm cannot drop below about 8 mm, because the groove and index plate sit between the bore and any outboard stop.
- R cannot exceed about 5.8 in this envelope.
- The stop torque path downstream of the key is also only SF ≈ 1.2 at 2.52 N·m.

**Smallest redesign that keeps S1's concept (proposed, not implemented, needs approval):**

1. **Journaled stop yoke (S1-R):**
   - Make the steel stop block part of a yoke whose ring runs on a clamped stainless bushing on the pin tip (X ≈ 15.8–18.5).
   - The stop reaction then closes between the stop plate and the yoke ring, both on the pin. The PETG bracket bore and the pin root see almost none of it (inferred).
   - The yoke carries only the torque into the tray, through a flange with two inserts ≥ 9 mm apart (inferred ≈ 11 MPa at T_d).
   - This also removes the lock's own transverse reaction from the bracket bore (§9).
   - Cost: +1 steel part and a bushing; the pin tip grows about 3 mm more; the cassette gets two coaxial bearings (fit to be detailed).
2. **Hub pin in 17-4PH H1025 (σy ≈ 1,000):** the pin tip/key and the root regain SF ≥ 2 at T_d with margin, and approach 2 at 2.52. This changes the approved 303/304 pin specification.
3. **Metal referencing:** stop faces and index holes in one part, or pinned together; stop block located by reamed features from the index sleeve. This is needed to hold the ±80° window.
4. **Hardened, crowned, replaceable contact faces** (§11).

**Other remaining risks:**
- The impact level is unknown (§11).
- The cable-exit route is not defined (§14).
- The pre-existing D-009 lock-reaction finding (§9) stands whatever is decided on S1.

## 18. Exact changes made to local files

| File | Change |
|---|---|
| `CAD/tools/s1_stop_study.py` | **New**, NON-PRODUCTION study tool (read-only; extends the in-process D-009 model only) |
| `prototypes/P0.1/round_e_s1_hard_stop_study.md` | **New** (this report) |
| `docs/build-log.md` | Study entry |
| `docs/decisions.md` | D-009 open item: S1 result |
| `CLAUDE.md` | Status line |

Not changed: `nomad.yaml`, `mechanical-spec.md`, `e_lid_layout.py`, `NOMAD_E_Prototype.fs`, harnesses, Onshape.

## 19. Ready for persistent Onshape implementation?

**No.**
- S1 fails the structural requirement at 1.26 N·m in the bracket bore and hub-pin root, and cannot reliably hold ±80° with printed location.
- **Owner decisions needed:**
  1. Approve a focused S1-R study (journaled yoke + pin material + metal referencing), or give other direction.
  2. The pre-existing D-009 lock-reaction finding (§9).
