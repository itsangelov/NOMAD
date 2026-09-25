# Build Log

Record every prototype build and test here. Label each result as: modeled / simulated / inferred / physically tested / measured.

---

## 2026-09-25 — Phase 0: engineering workspace

- Created the repository structure, `CLAUDE.md`, the spec skeletons and the decision log.
- Renamed the default branch to `main`.
- Confirmed the Onshape MCP connection. It is FeatureScript-only, with an allocation of 2,500 API requests per annual cycle.
- No CAD exists yet. No Onshape document has been created.

## 2026-09-25 — P0.1 Phase 1, Round A (modeled, scratch context only)

Scope: parameter pipeline, world/hinge frames, base skeleton, keyboard and trackpad envelopes (D-003), lid skeleton, display envelope, lid poses at 0°, 105° and 135°. Nothing was written to the NOMAD Onshape document; there is no Feature Studio yet.

**Pipeline**
- `nomad.yaml` gained an explicit authoritative-vs-working schema (`value`/`status` vs `working`/`formula`).
- `CAD/tools/yaml_to_featurescript.py` (standard library only) parses the restricted YAML subset, validates the schema, evaluates formulas safely and regenerates the parameter block in `NOMAD_P01.fs`. Result: 55 parameters, 12 authoritative, 33 working (6 via formula), 10 unresolved.
- The parser rejected all 16 malformed and invalid test inputs. PyYAML was not needed.

**Geometry results.** All are *modeled*: envelope boxes built from working inputs, not measured parts.

| Item | Result |
|---|---|
| Base skeleton | 301 × 235 × 40, wall 2.5 |
| Lid skeleton | 301 × 235 × 25 |
| Keyboard envelope | 280 × 105 × 8, x ±140, y 100–205, top flush with the base top |
| Trackpad envelope | 86 × 75 × 13, x ±43, y 15–90, top flush with the base top |
| Display envelope | 235 × 150 × 5, centred in the lid |
| Containment | All three envelopes lie inside their skeletons |
| Closed-pose gaps | keyboard–base 8, trackpad–base 12.5, keyboard–trackpad 10, display–lid back 17.5 |
| Hinge axis | (0, 227, 40): 8 mm in from the rear face, at the base top surface |
| Closed, 0° | overall 301 × 235 × 65 |
| Open, 105° | overall 301 × 309.9 × 259.3; lid reaches 74.9 mm behind the base |
| Open, 135° | overall 301 × 405.2 × 200.5; lid reaches 170.2 mm behind the base |
| Ground | Nothing goes below z = 0 in any pose |

**Findings**
1. **Lid–base overlap when open.** The 8 mm of lid behind the hinge axis swings down into the base top edge.
   - At 105°, the overlap region is 301 × 10.1 × 10.4 mm (2.3 cm³).
   - At 135°, it is 301 × 13.7 × 19.3 mm (3.4 cm³).
   - Cause: hinge axis inset (`HINGE_AXIS_OFFSET` 8) at base top-surface height, with no relief on either part.
2. **Display face touches the keyboard and trackpad when the lid is closed.** Both gaps are 0 mm, because both tops are flush with the base top and the display face is flush with the lid's open face. The flush placement is an implicit assumption in the envelope code, not a parameter.
3. Lid and base are in full-face contact when closed. This is expected seating, but there is no bumper or closed-gap allowance yet.

**Test method notes**
- `test_feature` costs about 9 API requests per run and returns evaluation notices only, not console output.
- Notice messages are truncated after roughly 330 characters. The harness therefore returns a compact report line as the message of a deliberate `regenError`.
- The production features (Skeleton, Base, Lid, Clearance Check) were not executed in Round A; only the library code they call was.

API requests used by Round A: 27 (3 × `test_feature`). Cycle total: 32 / 2,500.

## 2026-09-25 — P0.1 Round A.1: closed-lid clearances and hinge comparison (modeled, scratch only)

No hinge architecture was chosen. All values are provisional working inputs, and nothing was written to the NOMAD Onshape document.

**Changes**
- Four new TBD parameters with working inputs:
  - `KEYBOARD_TOP_RECESS` = 1
  - `TRACKPAD_TOP_RECESS` = 1
  - `LID_CLOSED_GAP` = MIN_GAP → 1
  - `HINGE_AXIS_HEIGHT` = 0 (the Round A baseline)
- The flush-top assumptions are gone. Keyboard and trackpad tops sit at `BODY_HEIGHT − *_TOP_RECESS`, and the closed lid sits `LID_CLOSED_GAP` above the base.
- The hinge frame now takes a hinge definition (inset and height), so alternatives can be evaluated without editing constants.

**Closed pose** (identical for every hinge option, because the axis does not move the closed lid)
- Overall 301 × 235 × 66.
- Base–lid gap 1.0, display–keyboard 2.0, display–trackpad 2.0.

**Hinge comparison**
- The lid envelope was swept 0–135° in 5° samples to find intrusion into the base envelope between the check poses.
- Rear zone envelope (y 205–235, full width and height) = 361 cm³.

| | A: axis at rear edge | B: axis raised to lid mid-thickness | C: current axis + modeled base relief |
|---|---|---|---|
| Hinge axis (y, z) | 235, 40 | 227, 53.5 | 227, 40 |
| Lid/base collision eliminated? | Yes: no intrusion anywhere in the sweep | No. Sweep intrudes 1.3 mm deep, 301 × 11.6 × 1.3 (2.4 cm³) at y 221–233, around 30–35°. Overlap at 135° | Yes at the check poses, but with 0 mm clearance (the relief is the exact swept envelope) |
| Clearance issues | Lid rear face to base rear face: 1.0 at 105°, **0.7 at 135°** (below MIN_GAP) | Overlap at 135° | 0 mm at 105° and 135° |
| 105°: rear overhang / max height | 85.9 / 266.7 | 62.8 / 276.0 | 75.9 / 259.0 |
| 135°: rear overhang / max height | 184.6 / 205.5 | 161.4 / 222.9 | 170.9 / 199.8 |
| Rear internal volume lost | 0 | 2.4 cm³ (0.7% of rear zone) | 44 cm³ relief (12% of rear zone): 301 × 13 × 19.3 at y 222–235, z 20.7–40, cutting through the rear wall and top edge full width |
| Keyboard/display clearance | Unchanged, 2.0 closed; no open-pose interaction | Same | Same |
| Secondary collisions / ground | None | None beyond base–lid | None beyond base–lid |

**Body-height check**
- Available clear height, from floor top (z 2.5) to envelope underside: **28.5 mm under the keyboard**, **23.5 mm under the trackpad**. No keyboard support deck is modeled; its thickness would come off these figures.
- Derived fit limit with MIN_GAP above: ≤ 27.5 mm under the keyboard, ≤ 22.5 mm under the trackpad, including standoffs and airflow.
- Pi 5 + cooling stack comparison: **unresolved.** `PI_STACK_HEIGHT` is TBD and no authoritative height data exists in the project. Only the 85 × 56 footprint (provisional) is known, and it fits under the keyboard in plan view.

**Test method notes**
- `box` is a reserved word in FeatureScript. Using it as a variable name made the payload fail to compile ("no features found"), which cost 7 requests.

API requests used by Round A.1: 16 (one failed compile, 7; one successful run, 9). Cycle total: 48 / 2,500.

## 2026-09-25 — P0.1 Round A.2: hinge-axis feasibility map (modeled; no hinge chosen)

- **Grid:** inset −6…10 step 2 (axis y 241…225) × height −4…26 step 2 (axis z 36…66), 144 points.
- **Sweep:** lid swept 0–135° in 5° steps against the base envelope.
- **Tool:** `CAD/tools/hinge_feasibility_2d.py`, an exact 2D side-view model.
  - It reproduces all three A.1 Onshape points.
  - One Onshape scratch run recomputed 11 grid points and matched the model to 0.01 mm, including angles and overlap counts.
- **Output:** full maps and data in `prototypes/P0.1/hinge_feasibility_map.md` and `.csv`.

**Results**
- **Feasible (≥ 1.0 mm):** 63 of 144 points. All have inset ≤ 0 (axis on or behind the base rear face), except the exact rear-top corner (0, 0) at 0.71 mm. No inset > 0 point is feasible.
- **Why:** with LID_CLOSED_GAP = MIN_GAP = 1.0, any axis ahead of the lid's rear-bottom edge lets that edge dip on opening, by √(inset² + (height − 1)²) − (height − 1).
- **Margin:** every feasible point's minimum is the closed-pose 1.00 mm. Opening-motion clearance is 1.00–1.62 mm.
- **Other checks:** no ground contact and no display/keyboard/trackpad issues. 0.1° sampling changes no result.

API requests used by Round A.2: 9 (one `test_feature` run). Cycle total: 57 / 2,500.

## 2026-09-25 — P0.1 Round A.2b: LID_CLOSED_GAP refinement (modeled, local only; no hinge chosen)

- **Method:** the A.2 map recomputed for `LID_CLOSED_GAP` = 1.0, 1.5, 2.0, 2.5, 3.0 with `MIN_GAP` held at 1.0. Same grid and sweep as A.2. The regression at 1.0 matches A.2 exactly. No Onshape calls.
- **Feasible points:** 63 / 79 / 86 / 91 / 94 of 144.
- **Points with inset > 0:** 0 / 15 / 22 / 27 / 30. The largest feasible inset is 0 / 4 / 6 / 8 / 8, reached only with the axis high (height ≥ 18–24).
- **Best margin above 1.0:** 0 / 0.5 / 1.0 / 1.5 / 2.0 mm.
- **Low-axis boundary does not move:** it is set by end-of-travel intrusion, which is independent of the closed gap.
- **Diminishing returns** above 2.5 mm.
- **Details:** `prototypes/P0.1/closed_gap_sweep.md` and `.csv`.

API requests used by Round A.2b: 0. Cycle total: 57 / 2,500.

**Owner decision after A.2b (D-006, provisional):**
- Rear-face hinge direction. Working `HINGE_AXIS_OFFSET` changed from 8 to 0; `HINGE_AXIS_HEIGHT` kept at 0 and still TBD.
- `LID_CLOSED_GAP` working value 2.0 mm, no longer tied to `MIN_GAP`. `MIN_GAP` stays 1.0.
- Exact axis position and hinge hardware remain TBD until the mechanism prototype.
- Committed as `0fdc92e`.

## 2026-09-25 — P0.1 Round B: solar kinematic skeleton, initial analysis (modeled; no rail architecture chosen)

- **New working inputs (TBD):** `SOLAR_CARRIAGE_WIDTH` 12, `SOLAR_CARRIAGE_HEIGHT` 8, and `SOLAR_HUB_LINK_LENGTH` = WALL + deploy clearance + MIN_GAP = 8.5.
- **New code:**
  - production builder `nomadBuildSolarSide` and layout `nomadSolarLayout` in `NOMAD_P01.fs`
  - model `CAD/tools/solar_skeleton_model.py`
  - Onshape harness `NOMAD_P01.solar.test.fs`
- **Onshape cross-check (V0, 6 states):** matched the model exactly.
- **Results** (details in `prototypes/P0.1/solar_round_b.md`):
  - Travel: 155 mm required. Only 106.5 mm is available if each rail stays in its own half, so rails must cross the centreline by 48 mm.
  - The current working layout (hub and rail at the cassette mid-plane) is impossible: rails run through the stowed cassettes and through each other.
  - D-004 kinematics are feasible with the rail outside the cassette layer: V1 (stacked rail layer, lid +6.5 mm) or V2 (edge rails, cassettes −6 mm, tilt restricted).
  - Tilt reaches the full ±75° at lid 105° and 135°. With the lid closed, the table limits it to ±30°.
  - Deployed span is 606 mm.

API requests used by Round B: 9. Cycle total: 66 / 2,500.

## 2026-09-25 — P0.1 Round B.1: V1 feasibility pass (modeled; V1 not chosen)

- **Model:** `CAD/tools/solar_v1_feasibility.py`, adding the bezel, per-side wall openings, hub bracket, provisional cable envelope, service loops, cable routing and hinge check. The Onshape cross-check of the V1 core skeleton matched exactly.
- **V1 as specified fails on four specific points:**
  1. pin and cable don't fit together in the 12 mm carriage
  2. 0.7 mm carriage retaining lip
  3. the cable's zone at the tilt joint hits the side wall (5 mm deploy clearance, about 8 mm needed)
  4. one cassette's cable is blocked from the hinge by the staggered rails
- **Minimal fixes** (lid stays 31.5 mm): 17 mm bracket and 22.6 mm carriage, an 8 mm cable corridor between the rails, deploy clearance 8 mm. These clear every modeled collision and routing problem.
- **Remaining structural concerns:**
  - The back plate spans 202 mm over the cassette bay (rough estimate: touches the cassettes at about 4.5 N).
  - The side walls are reduced to end posts and a lower strip.
  - The lid is likely only printable as two pieces. *(inferred)*
- **Details:** `prototypes/P0.1/solar_v1_feasibility.md`.

API requests used by Round B.1: 9. Cycle total: 75 / 2,500.

**Correction (2026-09-25):** the V1 tool printed the fixed-configuration rail Y ranges centred on the hub pin instead of the rail. The geometry and every check were correct. The actual rails are R y 121.5–149.1 and L y 85.9–113.5, with the 8 mm corridor between them. The print and `solar_v1_feasibility.md` have been corrected.

## 2026-09-25 — P0.1 Round B.2: lid structure / printability screening (screening estimates, not FEA; nothing chosen)

- **Tool:** `CAD/tools/lid_structure_screening.py`. Details in `prototypes/P0.1/lid_structure_screening.md`.
- **Concepts compared (V1 + fixes throughout):**
  - A: one-piece lid with a ribbed back plate
  - B: one-piece lid with a perimeter frame and thin panel
  - C: two-piece lid, front frame + ribbed rear shell, joined with M3 heat-set inserts and screws
- **Back plate** (202 mm one-way span):
  - Needs ~11 mm external ribs to stay within half the 1 mm cassette clearance under a conservative 20 N press, which makes the lid 42.5 mm (closed stack 84.5).
  - A printed sandwich plate is optimistic at 38.5 mm.
  - B's thin panel deflects ~50 mm: it cannot work as a load-bearing back.
- **Printing and assembly:** one-piece A and B have no practical print orientation (closed cassette-bay tunnel) and cannot take the display (rails 1 mm above it). C prints as flat parts and assembles in a clear order.
- **Rail cantilever over the display** (all concepts): 0.67 mm static and 2.0 mm at 3 g, against 1.0 mm clearance. This is a new risk; a metal stiffener in each rail is the likely mitigation.
- **No new collisions**; the hinge clearance stays ≥ 1.41 mm.
- **No Onshape run.** API total 75 / 2,500.

## 2026-09-25 — P0.1 test coupons designed (Concept C provisional basis; not printed yet)

- **Spec:** `prototypes/P0.1/coupons/P01_test_coupons.md`. Expected values from `CAD/tools/coupon_expectations.py`.
- **Coupon A (solar rail):**
  - the full 198 mm V1 rail on a clamped pad stub
  - carriage with load post, and a 5 mm display surrogate (1.0 mm gap)
  - A1 is the printed rail; A2 has slotted walls for generic 10 × 2 aluminium or 10 × 1.5 steel strips
  - Expected: A1 0.69 mm at 300 g, touching at +0.44 kg; A2 0.06–0.11 mm.
- **Coupon B (rear shell):**
  - the full 202 mm span on 14 mm shelves with an M3 insert joint at 70 mm pitch, a removable 1.0 mm clearance block, and a 90 mm strip
  - B1 plain 2.5 plate; B2 ribbed (h 11 default, 6 and 8 optional)
  - Expected: B1 14.7 mm at 20 N (touches at 1.4 N); B2 h 11 0.55 mm at 20 N.
- **Design note:** ribs may stop at the edge-beam line (moment is ~zero over the supports), which frees the screw bands.
- **Printing:** coupon A fits a 220 mm-class bed; coupon B needs ≥ 235 mm in one axis. Roughly 0.45 kg of PETG in total.
- No Onshape use. API total 75 / 2,500.

## 2026-09-25 — P0.1 coupon files generated (Round B.3; not printed yet)

- **Files:**
  - `CAD/coupons/P0.1/generate_coupons.py`: parametric master, standard-library Python.
  - 13 print-ready STLs and matching OpenSCAD copies.
  - A README with parts, orientations, infill, hardware, assembly, and test-critical vs fixture dimensions.
- **Parts:** A1 and A2 rails, pad stub, carriage + post, load platform, display surrogate; B frame, clearance block, B1, B2 at h 6/8/11, load pad.
- **Sanity checks:** all passed.
  - every mesh watertight (0 open or non-manifold edges), one body per part
  - channel 22.6 × 8.0, slot 17.6, lips present, carriage fit, strip slots open, ribs attached, 1.0 mm references, bed fit
  - STL read-back matches
- **Geometry changes from the spec:**
  - rail 200 long (end stop beyond the 198 channel, preserving the 149.5 mm arm)
  - carriage post +2 mm (load rod clears the lips)
  - edge reliefs instead of chamfers
  - load platform added
- **Estimate:** ~0.58 kg PETG, ~35–45 h printing (rough).

## 2026-09-25 — P0.1 coupons in Onshape (Feature Studio `NOMAD_P01_Coupons`)

- **Onshape write (approved):** created Feature Studio `NOMAD_P01_Coupons` (element `2e9a95c6ec40fe948348a500`) in the NOMAD main workspace and wrote the coupon FeatureScript. Compile check on write: no errors. Read back: matches the local snapshot `CAD/featurescript/NOMAD_P01_Coupons.fs`. It is the NOMAD document's only Feature Studio; no Part Studio feature was added (the connector cannot), so **no coupon geometry exists in a NOMAD Part Studio until the owner inserts "P0.1 Coupons"**.
- **Feature:** one custom feature builds all 13 coupons as separate named solids (`CPN_*`), print orientation, laid out 20 mm apart. Dialog: B2 rib heights 6 / 8 / 11 and insert hole Ø 4.0 × 6.0; all other dimensions are named `CPN_*` constants (coupon-local, deliberately not in `nomad.yaml`).
- **Validation (modeled, Onshape kernel, scratch Part Studio; one `test_feature` run, harness `NOMAD_P01_Coupons.test.fs`):**
  - 13 solid bodies, 13 unique expected names, 13/13 bounding boxes exact, all on Z = 0, one solid each.
  - Volumes vs `onshape_crosscheck.py` (exact, true holes): max deviation < 0.00005 %.
  - Laid-out parts: 0 overlaps, 0 touches (78 pairs).
  - Point probes 185/192. The 7 misses were misplaced probes (A2 channel edge probed at Y 16.05 < 16.1; B2 rib-side probes at X 115, on the mid-span transverse rib); the reference model is solid at the same 7 points, so the kernel agrees with it at all 192. Probes corrected in the harness; not re-run.
  - Rigs 16/16: rail seated on the pad stub with insert holes over the stub holes; display gap 1.000; carriage stowed against the end stop with no interference, arm 149.500; centred clearance 0.300 (A1 and A2); at the +Y wall and up against the lips it touches without interference, 0.05 mm higher it interferes (lip engagement 2.2 per side); B1 and all three B2 plates seated on the shelves with no interference; clearance-block gap 1.000 under every plate; load pad seated; plate holes over the frame inserts.
- **Discrepancies from the reference generator:** none dimensional. Round holes are true circles (STL: 0.1 mm steps); joints are exact face contact instead of the generator's 0.01 mm overlaps.
- **API:** 14 requests (1 inspection list, 1 `test_feature` ≈ 9, create, write, read-back, list). Cycle total ≈ 89–90 / 2,500.

## 2026-09-25 — Milestone: persistent Onshape coupon geometry (NOMAD → P0.1)

- P0.1 coupon geometry is now persistent in the NOMAD Onshape document. The geometry was validated in scratch against the reference generator, then inserted into the user-created P0.1 Coupons Part Studio and visually verified by the user. Physical coupons have not yet been printed or tested.
- **Confirmed by the owner:** the `NOMAD_P01_Coupons` Feature Studio is in the main NOMAD workspace; the owner created the Part Studio **P0.1 Coupons** and inserted the "P0.1 Coupons" custom feature; the feature regenerates without error; all 13 `CPN_*` parts are present and look correct; the geometry stays editable through the feature dialog and the Feature Studio.
- **Evidence levels:** geometry *modeled* and validated in a scratch Part Studio (previous entry); insertion and appearance *visually verified by the owner* in NOMAD. Nothing is *physically tested* or *measured*.
- **Source sync:** `CAD/featurescript/NOMAD_P01_Coupons.fs` is the file written to the Feature Studio (read back identical on write, unchanged locally since). No geometry changed in this pass; no Onshape API calls.
- **Next (not started):** export and print-service preparation for the physical coupons.
