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

## 2026-09-25 — Round C: base chassis V0.1 architecture (envelope model; proposed D-007, not accepted)

- **Scope:** base only. No lid, solar, display mounting, hinge hardware, hole patterns, port or vent cut-outs, battery geometry. Coupons untouched.
- **Architecture (proposed):**
  - Printed structural shell (walls, deck with keyboard/trackpad openings, bulkheads, bosses), open underneath, closed by a removable main service panel and a separate battery door.
  - Separate keyboard tray, trackpad tray and compute sled.
  - Compute in the right palm-rest bay; battery reserve in the left bay; power electronics, GNSS and compute power under the keyboard.
  - Two replaceable rear port panels; hinge-mount reserves at the rear corners; front → right-side cooling path; reserved cable corridors (trunk + 6 runs).
- **Parameters:**
  - 28 new TBD parameters with working values, plus working values for SERVICE_PANEL_THICKNESS, PI_STACK_HEIGHT, BATTERY_BAY_* and MIN_WALL.
  - New `io` group.
  - No authoritative value changed; BODY_WIDTH/DEPTH/HEIGHT unchanged (working 301 × 235 × 40).
- **Model:**
  - `CAD/tools/base_v01_layout.py`: one layout spec → local checks + generated FeatureScript layout block + kernel harness data.
  - `nomadBuildBaseV01` and the production feature "NOMAD Base V0.1" in `NOMAD_P01.fs`.
  - 34 named parts.
- **Validation (modeled):** all local checks pass.
  - 537 pair rules; service access for every module; nothing trapped; assembly from below; wall thickness; deck-down printability (no overhang or bridge).
  - Closed lid 2.0.
  - Lid sweep 0–135° min 1.414 (D-006 working hinge).
  - Rear plug zones 1.908 at 135°.
- **Onshape kernel cross-check** (1 `test_feature`, scratch): `BV n34 L0 S0/561 c160 dv0 l2,1.932,1.414 p14.012,1.908 e0`.
  - All 34 parts are single solids.
  - All 561 pair states match; 160 exact gaps match to 0.000 mm.
  - Lid clearances identical.
- **Key risks:**
  - Rear I/O vs hinge vs lid thickness: rear plugs conflict with the lid at 135° for 31.5 / 42.5 mm lids (clear only at 25).
  - Only 26.5 mm under the keyboard.
  - Compute heat under the palm rest (inferred).
  - Shell exceeds a 250 mm bed.
- **Report:** `prototypes/P0.1/base_v01_architecture.md`.
- **Onshape:** no document changes. API ≈ 100 / 2,500 (this round ≈ 10).

## 2026-09-25 — Round C.1: compute-placement study and lid/port screen (analysis only; nothing decided)

- **Concepts:** A right palm bay (D-007), B left palm bay, C under the keyboard, D rear bay, E split electronics. All compared on 12 criteria in `prototypes/P0.1/compute_placement_study.md` (model `CAD/tools/compute_placement_study.py`). No ranking, no choice.
- **Stack budget (modeled):**
  - Palm bays need a body height of 39.0 (fits 40).
  - Under the keyboard needs 47.5 (45.5 with a tray cut-out; 52.5 with a 5 mm plenum).
  - A rear bay needs a body depth of 276.5 (+41.5).
- **Lid/port constraint (modeled):** with the D-006 working axis, 135° and a Z ≤ 19 port zone, `z_low = H + h + (G + T − h)·cos θ_max ≥ port top + MIN_GAP`.
  - Today this means lid T ≤ 26.3.
  - The 31.5 lid is −2.69 and the 42.5 lid −10.47 at 135°. Hinge height 2.2 / 6.8, or a maximum angle of 126.5° / 116.5°, would restore clearance.
  - Plugs ≤ 15 mm long clear every lid.
- **Measurements that matter most:**
  1. Real Pi stack height.
  2. Required lid thickness.
  3. Hinge axis position.
  4. Measured power budget.
  5. Palm-rest temperature.
- No YAML, geometry or Onshape changes. API unchanged (≈ 100 / 2,500).

## 2026-09-25 — Round C.2: final architectural screening before the D-007 decision (analysis only)

- **Report:** `prototypes/P0.1/c2_architectural_screening.md` (model `CAD/tools/c2_screening.py`, grid `prototypes/P0.1/lid_hinge_port_map.csv`). No winner, no ranking; D-007 still proposed.
- **Lid/hinge/port map** (8 thicknesses × 7 hinge heights × 6 maximum angles; modeled):
  - At h 0, 135° is feasible only for T ≤ 26.3. 135° needs h ≥ 2 (T 27.5–30), ≥ 4 (31.5–35), ≥ 6 (40), ≥ 8 (42.5–45).
  - Lid-to-base clearance is never limiting (1.41 / 2.00).
- **Side ports** (modeled):
  - The lid never reaches a side zone.
  - V1 cassettes clear side zones at lid ≥ 60°; they interfere (−5.0) only when deployed and tilted with the lid closed.
  - Hand access is poor over the rear third (~40–53 mm above the ports).
  - With the Round C concept A internal layout, no side zone is internally feasible; side I/O implies a re-layout.
- **Print architecture:** one-piece needs ≥ 301 × 235. Splits to ≤ 250 put a joint across the hinge span and under the keyboard. A front/rear split keeps the width at 301.
- No YAML, geometry, Onshape or Git changes.

## 2026-09-25 — Round D: lid stack-up / structural envelope study (analysis only; nothing chosen)

- **Report:** `prototypes/P0.1/lid_stackup_study.md` (model `CAD/tools/lid_stackup_study.py`; reuses the B.1 V1 + fixes solar geometry, B.2 formulas and the C.2 hinge/port model).
- **Layer stack:** lip 0–1 + display 5 + gap 1 (+ mid-plate 2) + rail layer 13 + gap 1 + cassette 8 = 28–31 to the cassette top, then gap + back structure over the 202 mm bay.
- **Minimum T** (lip 1, δ ≤ gap/2 at 20 N / 1 kPa): ribbed back ~41.5–42 (B.2's 42.5 reproduced); sandwich or plain back ~37–38; modular with mid-plate ~40; thin/cassette-backed 31–32, which puts back loads into the cassettes.
- **Screening (analytical, not FEA):**
  - Cantilever rails reach 2.0 mm at 3 g vs 1.0 gap; on a mid-plate 0.5–0.9 mm.
  - Torsion index: closed-cell back ~4–5× stiffer than open backs.
  - Hinge screws ~200–245 N at 3 g.
- **Hinge/port:** every T 31–42.5 has feasible (h, θmax). 135° needs h 2–7; 120° needs h ≤ 1.5.
- **Flags:**
  - Working `LID_THICKNESS` 25 is below every studied architecture.
  - YAML solar carriage/deploy values differ from the passing V1 + fixes.
  - The display cable U-turn does not fit the lid controller band.
- No YAML, geometry, Onshape (API ~100 / 2,500) or Git changes.

## 2026-09-26 — Round D.1: lid architecture convergence (analysis only; nothing chosen or ranked)

- **Report:** `prototypes/P0.1/lid_architecture_convergence.md` (model `CAD/tools/lid_architecture_convergence.py`; reuses Round D, B.2, coupon A2, B.1 and C.2 models; all study values local).
- **Classes (lip 1, gap 2; 0.1 mm grid):** A sandwich T 37.6, B modular 39.6, C ribbed 42.0 (41.0 with ribs @ 20). Lip 0 subtracts 1. Back LC1 0.93–0.98 against 1.0.
- **Sandwich printing:** A's T is 37.5–37.7 with webs ≤ 20 or an infill core; it rises to 38.4–38.9 if the 28 mm bridged skin loses 2–3 layers. An unbonded two-piece sandwich is not viable. There is no sandwich coupon yet.
- **Rails (tolerance-inclusive criterion):**
  - Printed cantilever rails fail at 3 g (2.36 vs 1.0).
  - Coupon-A2 strips are thickness-neutral: 0.53–0.69, +42–91 g per lid.
  - Two strips move the hubs 1.6 mm in Y; this was re-validated collision-free and is flagged, not adopted. One outboard strip leaves the mechanism unchanged.
  - B works with printed rails only as an integral module, at the limit (0.99–1.00).
- **Hinge/port:** at h 0, 120.0 / 118.5 / 117.0°. 135° needs h 5.0 / 6.0 / 7.0 with 45 mm plugs, and h 0 with ≤ 15 mm plugs. h ≈ 1 is a lid–base thin spot (0.99 vs 1.0).
- **Mass/handling (placeholders):** lid 1.61–1.91 kg. Hinge rows 118–221 N at 3 g. One-handed opening needs a base of 1.35–1.83 kg.
- **Convergence window:** below ~37 structural and manufacturing constraints become problematic; ~37.5–42 all three classes remain credible (conditional); above ~42 thickness adds margin only. No class is eliminated; three sub-variants fail their criteria.
- No YAML, geometry, Onshape (API ~100 / 2,500) or Git changes.

## 2026-09-26 — P0.2: physical risk coupon package defined (test plan only; nothing printed or ordered)

- **Plan:** `prototypes/P0.1/P0.2_physical_test_plan.md`. **Generator and expected values:** `CAD/tools/generate_p02_coupons.py`, writing `CAD/coupons/P0.2/{stl,scad}` (git-ignored).
- **Reused unchanged from P0.1:** A1 and A2 rails, pad stub, carriage, display surrogate, load platform, B frame, B1, B-L pad (B2 h 8 optional).
- **New:**
  - B-S30 and B-S20 sandwich plates: 230 × 90 × 6.6, skins 1.2, core 4.2, bridges 27.87 / 20.40.
  - B-INFILL (6.6 envelope, slicer core).
  - A 2.0 mm clearance block and a full-width load bar.
  - All generated watertight, with every check passing.
- **Review findings (inferred from the geometry):**
  - The A2 strip slot's 0.4 mm vertical play means an unshimmed strip only engages after ~2.8 mm of tip deflection. The procedure now shims the strip.
  - One strip makes the rail asymmetric: the soft-lip tip at 3 g could be anywhere from 0.38 to 2.24 mm. Both lips are now measured.
  - The rail tip, not the carriage, is the minimum-clearance point (~1.2× the D.1 value). At the tip, a single aluminium strip becomes a marginal fail (0.67 vs 0.65).
- **Loads:**
  - Rail: R0–R3 (0.3 kg, 0.9 kg static 3 g equivalent, 20–50 cycles).
  - Plates: S0–S3 (1.82 kg LC1 equivalent, 2.04 kg 20 N reference, recovery, 20 cycles, unscrewed calibration run).
  - Thresholds are the D.1 limits, not tightened.
- **Sandwich:** the coupon sits at the criterion by design (S30 predicted 0.98 vs 1.0). The measured ratio maps to class A T 36.7–39.0.
- **Package:** minimum 9 parts, ~384 g, ~27 h; recommended 14 parts, ~593 g, ~42 h. Needs a bed ≥ 235 mm in one axis; one order.
- **Readiness:** ready to print from local STLs. The insert pilot hole (Ø4.0 × 6.0 placeholder) needs confirming, and the owner decides whether the P0.2 parts must go into Onshape first.
- **Also changed:** `.gitignore` (P0.2 outputs); a pointer note in `P01_test_coupons.md`.
- No YAML, Onshape (API ~100 / 2,500) or Git changes.

## 2026-09-26 — P0.2-HW: M3 heat-set insert interface for the P0.2 coupons (scoped to the coupons)

- **Report:** `prototypes/P0.1/P0.2_insert_interface.md`.
- **Published M3 pilots span 4.0–4.6**, so Ø4.0 is kept as the *lower bound*: a hole that is too small is fixed by drilling up to the datasheet value after printing.
- **Depth changed 6.0 → 7.0** (`INSERT_DEPTH` in `CAD/coupons/P0.1/generate_coupons.py`): ~1 mm melt relief under a 5.7 insert and no screw bottoming. Affects the A1/A2 ear and B-frame holes only. Regenerated; all checks pass.
- **Insert requirement for P0.2:** straight knurled, non-flanged, length 4.0–6.0, OD ≤ 5.0. A flange would shift the test-critical seating planes.
- **Screws:** M3 × 8 (rail, B1/B2), M3 × 12 (sandwich plates; M3 × 10 is too short).
- **Onshape:** not changed. The owner should set the coupon dialog "insert hole depth" to 7 mm to match (no API needed).
- **`INSERT_SIZE`:** flagged for later authoritative review; not locked.
- No YAML, Onshape (API ~100 / 2,500) or Git changes.

## 2026-09-26 — P0.2 final print package (packaging only; no geometry change)

- Verified all 15 STLs: watertight, one body each, sizes match the spec, origin at 0, no duplicates.
- Copied them to `CAD/coupons/P0.2/print_order/NOMAD_P02_*.stl` (git-ignored).
- Print card: `prototypes/P0.1/P0.2_print_card.md`. Minimum set 9 parts ~384 g; recommended 14 parts ~593 g (PETG 1.27 g/cm³, estimate).
- Minimum bed 235 × 95; needs several plates on a 250 mm-class bed.
- No YAML, Onshape or Git changes.

## 2026-09-26 — Round E: E0.5 YAML reconciliation and E1 base in Onshape (stopped at the E1 review)

- **Plan approved** (D-008, Round E only). Log: `prototypes/P0.1/round_e_digital_prototype.md`.
- **E0.5:**
  - `nomad.yaml` working values only; authoritative values unchanged.
  - `LID_THICKNESS` becomes a formula → 37.6 (D.1 class A, PROVISIONAL — PENDING P0.2).
  - The B.1 V1 + fixes solar values are now the working values: carriage 22.6, deploy 8, travel 158, link 11.5, hub 114.3 / −7.5, plus slot, rail, bracket, cable and corridor parameters.
  - New lid-stack, controller, hinge-barrel (Ø8) and Pi HAT-zone working parameters; spec rows added.
- **Study integrity:** all study tools were diffed before and after. The A.2, Round B and B.1 "as specified" inputs are pinned, so every published study output reproduces exactly.
- **Known open conflict:** the Round C base checker now uses the 37.6 lid and reports the rear-plug intrusion (−7.0 at 135°) as a known OPEN CONFLICT (Round E decision 4), not resolved.
- **Generators:** `--target` / `--harness` options added for the Round E file.
- **E1:**
  - Created Onshape Feature Studio `NOMAD_E_Prototype` (`40d4ae5868441bcb8882fe3a`) with "NOMAD E Base" (52-part base incl. keep-outs, owned mate connector on the hinge axis) and "NOMAD E Service" (panels, doors, port panels, 17 representative M3 heads).
  - Scratch kernel check: 561 pair states match Round C, 0.000 gap deviation, connector exact.
- **E1 findings (open, not resolved):**
  - **F1:** 11 panel/door screw heads run 0.5–0.75 mm into the shell walls (boss axis 1.95 mm from the panel edge).
  - **F2:** 4 compute-sled screw heads overlap the service panel by 0.7 mm (1.0 mm sled gap). Raising the sled would break the Pi-to-deck MIN_GAP.
- **API:** 100 → 112. No Git commit or push.

## 2026-09-26 — Round E: E2 digital lid in Onshape (stopped at the E2 review)

- **E1 review:** the owner accepted the base with no architectural changes. F1 / F2 and `PI_HAT_ZONE_HEIGHT` stay open.
- **E2 built:**
  - Feature **NOMAD E Lid** in `NOMAD_E_Prototype`: 26 parts and 9 owned mate connectors (lid revolute, left and right slider pairs, left and right cassette revolute pairs).
  - Class A lid, 37.6 mm, **PROVISIONAL — PENDING P0.2**: frame, display envelope, sandwich rear-shell envelope, B.1 V1 + fixes solar on both sides (rails, carriages, Ø5 hub pins, brackets, cassettes, cable keep-outs), Ø8 three-knuckle hinges with leaves and base pockets, controller and display-cable reserves.
  - The dialog has preview-only lid angle, extension and tilt. No YAML change.
  - Layout spec and checks: `CAD/tools/e_lid_layout.py` (generated block + harness data). Log: `prototypes/P0.1/round_e_digital_prototype.md`.
- **Validation (modeled):**
  - Scratch kernel check `E2 n55 mc10 L0 S0/181 c177 dv0 m0 P0/15 pd0`: every state, gap, connector and posed clearance matches the local model exactly.
  - Local sweeps: 0 unexpected moving-part violations; lid sweep 0–135 clean (minimum 1.0).
  - Rear-plug OPEN CONFLICT reproduced (−6.6 at 135°, below MIN_GAP from 121°), left visible.
- **E2 finding F3 (open, not resolved):** the B.1 hub-bracket envelope sits 1.0 mm into the rail channel floor. B.1 never checked this pair. Options (a)–(d) are in the log; none applied.
- **Notes:**
  - With the lid closed, deployed tilts beyond about +30 / −45 reach the table (known B.1 operating limit).
  - The display-flex and right-loop reserves are adjacent (0.0).
  - Class B / C variants are deferred.
- **API:** 112 → 125. No Git commit or push.

## 2026-09-26 — Round E: F3 investigation (analysis only; nothing implemented)

- **Report:** `prototypes/P0.1/round_e_f3_investigation.md`. Diagnostic: `CAD/tools/f3_investigation.py` (NON-PRODUCTION, read-only, rebuilds the E2 lid in memory).
- **Interference (modeled):**
  - bracket bottom Z 50.5 vs floor top Z 51.5: constant 1.0 mm over slide 0–146.5 of 158 (93 %), full width;
  - only the floor is involved; rounding or reshaping the bracket cannot remove it.
- **Root cause:** below the tilt axis there are 4.0 mm available and 6.0 needed (pin radius + bracket wall + MIN_GAP). Meanwhile 4.0 mm above the pin are unused.
- **Correction to the E2 report:** options (a) 1.5 mm wall and (c) +1 mm channel only reach contact.
- **Eight variants** were run through the full E2 check set, plus the rejected concepts, with inferred structural estimates.
  - **Recommended (not applied):** raise the axis 2.0 mm (`SOLAR_HUB_AXIS_OFFSET_Z` −7.5 → −5.5, formula only) and add a carriage boss in the slot; new working parameter `SOLAR_BRACKET_WALL`.
  - Result: no lid, rail, cassette, travel or pin change; bracket–floor 1.0 over the full travel; carriage walls around the pin 1.5 / 1.5 → 3.5 / 2.0.
- **Related observations:** the 10 mm hub-bracket bore is the weakest deployed-load element (O1); the pin needs a hardened / stainless dowel-class material (O2).
- **No change** to `nomad.yaml`, FeatureScript, Onshape or Git.

## 2026-09-26 — Round E: F3 APPROVED AND IMPLEMENTED — OPTION B

- **Decision (owner):** option (b) from `prototypes/P0.1/round_e_f3_investigation.md`. Raise the solar tilt axis 2.0 mm instead of thinning the bracket or weakening the rail. Record: §10 of that file.
- **What changed:**
  - `nomad.yaml`, working formulas only: `SOLAR_HUB_AXIS_OFFSET_Z` −7.5 → −5.5; new `SOLAR_BRACKET_WALL` = `WALL_THICKNESS` (2.5). Spec rows updated.
  - Axis Z 55.5 → 57.5; hub bracket Z 52.5–63 (2.5 wall); carriage body unchanged plus a 17 × 2.5 × 40 slot boss.
  - The cable run, notch bottom and solar mate connectors follow the axis.
  - `e_lid_layout.py`: bracket–rail guided-fit rule, full-travel bracket–floor sweep, F3 budget assertion.
  - `f3_investigation.py`: pre-F3 inputs pinned, plus an implemented-equals-B check.
- **Why:** F3 put the hub bracket 1.0 mm into the rail floor over 93 % of the travel. Option B recovers the 2.0 mm budget from unused height above the pin, with no change to the lid, rail, cassette, travel, pin or bracket wall.
- **Tradeoff:**
  - stowed margins shrink but stay ≥ MIN_GAP (carriage boss to the other cassette 3.5 → 1.0, pin 5.0 → 3.0, cable run 4.5 → 2.5);
  - lowest tilted cassette at lid 105–135°: 7.8 → 6.5;
  - the 13 mm rail layer is now fully used by the pin stack.
- **Validation (modeled):**
  - local E2 suite passes: bracket–floor 1.000 over the full travel, 0 unexpected violations, rear-plug OPEN CONFLICT unchanged;
  - all study outputs byte-identical;
  - Onshape scratch `E2 n55 mc10 L0 S0/177 c175 dv0 m0 P0/15 pd0` (exact);
  - persistent `NOMAD_E_Prototype` written, read-back identical.
- **API:** 125 → 140. No Git commit or push.

## 2026-09-28 — Round E: solar tilt index lock and hub-pin anti-rotation (D-009) implemented locally; ±80° stops open

- **Analyses** (analysis only, no files changed):
  - `prototypes/P0.1/round_e_solar_index_lock_manufacturing_check.md` → option D (Ø1.5 hardened pin, stainless plate, double-D + M2 clamp);
  - `round_e_solar_hub_pin_anti_rotation_check.md` → option C (captured anti-rotation plate + Ø3 dowel).
- **Decision:** the owner approved and requested the implementation of the complete mechanism (D-009).
- **What changed:**
  - `nomad.yaml`: 41 new TBD parameters with working values or formulas; `SOLAR_TILT_STOP_ANGLE` has no value. Spec subsection + rows.
  - New `CAD/tools/region2d.py`: exact 2-D regions (arcs, holes).
  - `e_lid_layout.py`: lock parts from YAML formulas, profile prisms, 46-part lid, lock checks A–G, new guided fits.
  - `f3_investigation.py`: pinned to the E2 lid without the lock.
  - `NOMAD_E_Prototype.fs`: regenerated blocks and a profile builder, **local only**. E2 harness data regenerated. `NOMAD_P01.fs` params regenerated.
  - Record: `prototypes/P0.1/round_e_solar_index_lock_implementation.md`.
- **Validation (modeled):**
  - local suite ALL CHECKS PASSED: 11 positions pin–hole 0.050; positive lock at every half-step; retracted pin 1.000 clear; stow only at 0° (blocked at 7.1 mm otherwise); 0 unexpected moving-part violations; F3 bracket–floor 1.000;
  - study outputs and the F3 study byte-identical;
  - Onshape scratch `E2 n75 mc10 L0 S0/398 c396 dv0 m0 P0/27 pd0` (exact).
- **Loads (inferred, T_d 1.26 N·m):** every implemented element has SF ≥ 2 at room temperature.
  - Lowest: pin root 2.09, dowel bearing bound 2.36, keys 2.30–2.41, index pin 2.80.
  - The sleeve lifts the counter-hole from 1.07 to 2.38 hot.
- **Deviations:**
  - dowel recessed 1.0 (rail end-stop rule);
  - anti-rotation plate outline derived from clearances (ligaments 1.0 / 1.3 / 2.04);
  - tip key A/F 3.0 (owner).
- **Open (critical):** the **±80° hard stops are not packaged**.
  - No location within the approved parts reaches SF 2: plate plane, retracted pin, cable link, bracket, lid wall.
  - With the pin held retracted, the model rotates freely to ±90°.
  - Options S1 (outboard stop, recommended study) / S2 (cable re-route) / S3 (interim waiver).
  - The persistent `NOMAD_E_Prototype` is therefore **not written**; the local snapshot is ahead of Onshape.
- **API:** 140 → 167 (three scratch runs, two stopped on test-payload faults). No Git commit or push.

## 2026-09-28 — D-009 S1 hard-stop feasibility study: FAIL (needs redesign)

- **Report:** `prototypes/P0.1/round_e_s1_hard_stop_study.md`.
- **Tool:** `CAD/tools/s1_stop_study.py` (NON-PRODUCTION, read-only, in-memory model).
- **Candidate (variant B, modeled):** a 3 mm stainless stop plate keyed with the index plate on a pin tip extended to 15.5 (pin 56.5), and a steel stop block in a pocket under the tray.
- **Geometry (modeled):**
  - contact at exactly ±80.000° both sides, both directions, lid 105 / 135; no other interference before it;
  - full regression clean (0 unexpected violations; D-009 A–G unchanged; stow only at 0°);
  - service paths OK.
- **Load failure:** achievable contact R 4.5–5.77 (centroid 5.14). Stop force 245 N at 1.26 N·m, reacted 8.75 mm outboard of the 10 mm PETG bracket bore:
  - bracket bore SF 0.98 (stop only) / 0.60 (with design handling);
  - hub-pin root SF 1.23;
  - at 2.52 N·m most of the chain is about 1.
- **Tolerance:** the 5° margin is 0.45 mm; worst case ±7.2° with an FDM-located block (±4.36° with metal referencing) against a window of about −4.5/+3.6°.
- **Variant A (formed flange):** inferior (flap SF about 1.1).
- **Pre-existing D-009 finding:** the approved lock's own transverse reaction was omitted in the load and anti-rotation checks.
  - Pin root SF 2.09 → 1.75 at T_d. **(Withdrawn: see the reassessment below; the root is unaffected.)**
  - Bracket bore SF 2.60 → 1.87 at handling.
- **Proposed smallest redesign (not implemented):** a journaled stop yoke on a clamped tip bushing, a 17-4PH pin, metal-referenced stop faces, and hardened, crowned, replaceable contacts.
- **Not changed:** nomad.yaml, spec, FeatureScript, Onshape (0 API calls). No Git commit or push.

## 2026-09-28 — D-009 load reassessment (Phase 1) and S1-R stop-yoke feasibility (Phase 2)

- **Phase 1** (`prototypes/P0.1/round_e_d009_load_reassessment.md`, tool `CAD/tools/d009_load_reassessment.py`): the index lock's transverse reaction was added to the load path.
  - **Pin root unchanged** (SF 2.09 at T_d). The index force is internal to the pin + cassette system; checked numerically. The S1 report's 1.75 / 1.23 root figures are withdrawn (erratum added there).
  - **PETG hub bracket below its handling-basis SF 2:** bearing 2.60 → 1.88, tear-out 2.56 → 1.73, peak tension 2.39 → 1.61. At T_d: 0.81–0.94.
  - Lock torque-path parts still ≥ 2 at T_d; the tip key 2.41 → 2.25.
  - Not fixable with PETG without a geometry change. The minimum change is an outboard metal bearing for the cassette.
- **Phase 2** (`prototypes/P0.1/round_e_s1r_stop_yoke_study.md`, tool `CAD/tools/s1r_stop_study.py`): **PASS, READY FOR OWNER REVIEW**, not approved for persistent Onshape.
  - **Design:** a floating 17-4 stop yoke journaled on a clamped tip bushing, driven by a Ø3 dowel at R 25. The stop plate is at X 15.8–18.3 and the pin becomes 59.3 long.
  - **Geometry:** stop at exactly ±80.000° both sides and directions; D-009 A–G, stow, sweeps and service paths clean.
  - **Transverse load into the PETG bore at T_d:** 60 N / 529 N·mm (S1: 245 N / 2,144 N·mm); bore SF 3.97.
  - **Loads:** all stop-path elements ≥ 2 at T_d (minimum pin tip 2.32 in 303). 17-4 pin not required at T_d; needed only for SF 2 at 2.52 N·m.
  - **Tolerance:** metal-referenced worst ±2.41° (RSS ±0.80°) within the −4.5/+3.9° window.
  - **Open:** it does not fix the Phase 1 hub-bracket shortfall (a rigid-yoke variant could; needs its own study); tray slot; thumb access (about 4 mm).
  - The corrected index-plate assembly order is documented for review.
- **Not changed:** production geometry, nomad.yaml, spec, FeatureScript, Onshape (0 API calls). No Git commit or push.

## 2026-09-28 — D-010 solar architecture comparison (sliding wings vs solar lid): awaiting owner decision

- **Report:** `prototypes/P0.1/d010_solar_architecture_comparison.md`.
- **Tool:** `CAD/tools/d010_solar_architecture_study.py` (NON-PRODUCTION; estimates).
- **Concept views:** `prototypes/P0.1/d010/*.svg`.
- **Power (est.):** A about 8.8 W nameplate; B1 (single top-hinged leaf) about 10.2 W; B2 (tri-fold) about 20 W. Real best-orientation output about 0.55–0.70 × nameplate.
- **Mass (est.):** A about 590 g; B1 about 410 g; B2 about 780 g.
- **Stability (calc, base 1.45 kg assumed):** the lid hinge sits on the rear tipping edge (D-006), so NOMAD is wind-sensitive in any architecture.
  - A tips at about 8 m/s front wind.
  - B1 deployed tips at about 5 m/s without a stay.
  - B2 cantilevered tips at rest.
  - The lid hinge must hold about 1.1–1.4 N·m for B1 deployed.
- **Orientation (calc):** B1 is independent of the display angle and works with the sun on either side (visor); A works only with the sun behind the device.
- **Heat (est.):** B needs a vented air gap (then about equal to A); a bonded leaf risks overheating the display.
- **Complexity:** A about 40 parts including precision EDM / CNC; B1 about 10–12 off-the-shelf / printed.
- **Cable:** A has a ±80° twist in an 11.5 mm link and slide loops; B1 has one hinge fold and shares the display hinge path.
- **Recommendation:** Architecture B (B1 + positive angle lock + vented gap + fold-out rear stay), gated by a one-day physical mock-up (tipping, hinge torque, wind); fallback B-base.
- **Not changed:** production Onshape, geometry, YAML, FeatureScript (0 API calls). No Git commit or push.

## 2026-09-28 — D-010 Phase 2: A vs B1 engineering study + dual Onshape concept model: awaiting owner review

**Files**

| What | Where |
|---|---|
| Report | `prototypes/P0.1/d010/d010_solar_architecture_phase2.md` |
| Tool | `CAD/tools/d010_phase2_study.py` (NON-PRODUCTION; `--emit` regenerates the Onshape data block and the kernel expectations) |
| Onshape | new isolated Feature Studio **`NOMAD_D010_Concepts`** (element `d4619014058afc59574f42aa`), custom feature "NOMAD D010 Concepts" |
| Snapshot | `CAD/featurescript/NOMAD_D010_Concepts.fs` |
| Scratch harness | `NOMAD_D010_Concepts.test.fs` (never written) |

**The Onshape model**
- A gallery of both architectures in 6 named states each, plus side-by-side, single and CUSTOM layouts.
- Both share one base reference.
- It shows cable tubes colour-coded by type, CG markers, support polygons, deployment envelopes and keep-outs.
- The owner must insert the feature into a new Part Studio; the connector cannot insert features.

**Kernel cross-check (scratch; KERNEL vs CALC)**
- CG error 4e-5 mm.
- A lid to plug keep-out at 120°: 1.200 / 1.200.
- B1 stack to plug keep-out at 125°: 2.072 / 2.072.
- Leaf to lid at ψ 45: 1.141 / 1.141.
- Deployed wing to lid: 8.0.
- The gallery regenerates: 545 bodies, no errors.

**Results (CALC / EST / VENDOR)**
- **Power:** B1 catalog P108 9.5–10.9 W vs A custom laminate 8.8 W (or 5.2 W catalog).
- **Mass:** equal, 2.64 / 2.62 kg.
- **Tip wind without a stay:** A 8.3–10.6 m/s; B1 5.4–8.3 m/s (2.4 upright at φ 125).
- **Tip wind with a 105 mm stainless outrigger stay:** B1 11.4–18 m/s; A 18.2.
- **Leaf hinge:** 0.83 N·m per hinge required.
- **Display hinge:** B1 about 1.5× A's torque.
- **Cables:**
  - A: 2 cables, 0.73 / 1.30 m. The carriage-to-loop crossing is unresolved; S-bend 2.5–3.9 × *d*; loop 3.3 × *d*; right-hinge twist 7.1°/mm.
  - B1: 1 cable, 0.85 m, with 2 twist zones at 2.75°/mm.
- **Thermal:** a vented gap of at least 6 mm plus low-e foil is required for B1. Sun-exposed parts should be ASA or light-coloured in both architectures.
- **Orientation:** B1 covers front, rear, side and overhead sun. A covers the rear only.

**Corrections to Phase 1 (erratum added to the Phase 1 report)**
- There is no visor while generating power.
- Mass is equal.

**Recommendation:** B1, conditional on the tipping / hinge / thermal / cable mock-ups.

**Not changed:** production Onshape elements, geometry, `nomad.yaml`, production FeatureScript, D-009 / S1 / S1-R records.

**Onshape API:** 40 calls (167 → 207). The connector's notes tool also created a separate "FeatureScript MCP Notes" Onshape document (not NOMAD).

No Git commit or push.

## 2026-09-29 — D-010 concept: NOMAD wordmark on the B1 lid back (visual only): awaiting owner visual review

- **What:** a recessed "NOMAD" wordmark on the B1 lid back, in the isolated `NOMAD_D010_Concepts` only.
- **Font:** Michroma, as a documented **fallback**; Eurostile Extended is not available in Onshape.
- **Size and position:** 18 mm letter height, 139 × 19.5 mm; centred on the lid centreline, 200 mm from the lid's top edge.
- **Engraving:** 1.0 mm deep. A 1 mm internal backing pad keeps 2.5 mm of material under the letters.
- **Foil:** the low-e foil gets a window around the wordmark.
- **Visibility:** hidden when the leaf is stowed or at 30°; fully visible at 65° and above.
- **Checks:** the geometry passed a scratch kernel check. Written to Onshape and read back: identical to the local file.
- **Not changed:** production, YAML, and the B1 mechanics.
- **Report:** addendum in `prototypes/P0.1/d010/d010_solar_architecture_phase2.md`. No commit.

## 2026-09-29 — D-010 concept: wordmark rebuild failure repaired (isolated `NOMAD_D010_Concepts` only)

**Correction to the entry above:** "passed a scratch kernel check … read back identical" was not enough. The written file did not compile, so every instance of "NOMAD D010 Concepts" failed.

**Root causes**
1. `box` is a FeatureScript reserved word. The wordmark code used it as a variable, a map value and a member (`w.box`), which is a parse error that blocks the whole Feature Studio.
2. A latent defect: `qSketchRegion` without the inner-loop filter extruded the letter counters too, filling O, A and D. The kernel counts 8 regions vs 5 glyph regions.

**Repair**
- Renamed `box` → `rect` / `wmBox` → `wmRect`.
- Both text extrudes use `qSketchRegion(id + "sk", true)`.
- No change to font, size, position, depth, pad, foil window, B1 mechanics, A, YAML or production.

**Tests (KERNEL, scratch)**

| Case | Result |
|---|---|
| Wordmark OFF | 12/12 gallery instances, 545 bodies, the same as before the wordmark. The D010 check is unchanged: CG 4e-5; plugs 1.200 and 2.072; leaf-core 1.141; cassette/bracket 8.0; stay-base 0.5. |
| Wordmark ON | 12/12 gallery instances, 581 bodies (+5 letters and 1 pad per B1 state). Recess 1.00 mm, 2.50 mm under the letters. The lid stays one body; the lid volume drops by exactly glyph area × 1 mm. The foil window is present. |
| Clearances from the wordmark and pad | hinges 164, display hinge 26.7, stay 72, knuckles 180, leaf 6.8, controller 1.0 |

- The full source (UI feature included) was compiled in scratch before the write.
- Written, read back byte-identical (53,687 characters).
- The persisted file itself evaluated cleanly: the real feature, GALLERY, wordmark on, 0 notices.

**Open (awaiting owner):** the backing pad is 0.19 mm from the B1 lid cable run under the "D" (no intersection). A fix needs a cable-route or wordmark change, both of which are frozen. Options are in the report §9.

**Report:** `prototypes/P0.1/d010/d010_wordmark_rebuild_diagnosis.md`. New scratch harness: `CAD/featurescript/NOMAD_D010_Concepts.gallery.test.fs` (never written to Onshape).

**Onshape API:** 38 calls (239 → 277 of 2,500).

No Git commit or push.

## 2026-09-29 — D-010 concept: B1 lid-cable rise point moved (owner-approved option a)

- **Change:** B1 cable route point (−60, 194.5, 53) → **(−78, 194.5, 53)**, made in `d010_phase2_study.py` and regenerated with `--emit`. Only the isolated `NOMAD_D010_Concepts` changed.
- **Unchanged:** the wordmark, pad, foil, B1, A, YAML and production.
- **Result (KERNEL):**

  | Check | Result |
  |---|---|
  | Min cable to wordmark pad | **2.35 mm** (was 0.19); cable to letters 4.97 |
  | Gallery | 12/12 with the wordmark ON (581 bodies) and OFF (545) |
  | Validation check | unchanged |
  | Wordmark geometry | identical |
  | Cable to stay | 12.77 |
  | Saved file | evaluates cleanly (0 notices); read-back byte-identical |

- **Pre-existing findings, not fixed:**
  - The cable touches the right leaf friction-hinge barrel at (66, 8, 69) and the right leaf-frame edge at (139, 18, 61). Both are on the unchanged leaf-side route.
  - The new rise corner is limited to R 9.1 mm (target 12).
  - Cable 852 → 861 mm.
- **Details:** report §10.
- **Onshape API:** 32 calls (277 → 309). No commit or push.

## 2026-09-29 — D-010 concept: B1 cable routing correction pass (owner-approved; isolated `NOMAD_D010_Concepts` only)

- **Done:** minimum bend radius restored to **12 mm** (was 9.1 at the x −78 rise; 11.9 at the base riser, pre-existing). Route edits: (141, 194.5, 53) → (141, 193.5, 53); (−78, 194.5, 53) → (−78, 193.5, 53); (−75, 215, 56) → (−82, 215, 56); (5, 226, 16) → (5, 227, 16). Cable 861 → 867 mm.
- **Clearances (KERNEL):** pad 2.42 (letters 5.0), controller 0.6 → 1.6, stay 12.77.
- **Gallery:** 12/12 with the wordmark ON (581 bodies) and OFF (545). The validation check and the wordmark geometry are unchanged. The saved file evaluates cleanly (0 notices). Read-back is byte-identical.
- **Not done (STOP per the owner's rule):** the two 0.00 mm leaf-end contacts.
  - (66, 8, 69): hinge barrel, hinge leaf plate, PV panel edge and the in-line connector.
  - (139, 18, 61): leaf-frame side wall and lid skin.
  - A Ø4 cable cannot leave the knuckle axis: the gap between the frame front-bar corner and the panel corner is 3.04 mm, the outside path is 3.5 mm, and the cable is tangent to the panel face along the whole twist zone. Elimination needs a structural change, so it is left for the owner.
- **Details:** report §11 (options included). No commit or push. Onshape API: 70 calls (309 → 379 of 2,500).

## 2026-10-01 — Checkpoint: B1 / SB-261 hinge record (exploratory, pre-decision) and V1 studies committed

- **What:** a Git checkpoint of the uncommitted engineering state since `d43201c`:
  - the Round C–E, D-009 and D-010 records already logged above
  - the B1 / TorqMaster SB-188-SB-261-6 hinge work done in scratch on 2026-10-01
- **New record:** `prototypes/B1_SB261/`. It holds:
  - the engineering record, coupon specification, validation status and sources
  - the original session reports, verbatim
  - copies of the scratch code: IGES reader, FeatureScript library and harnesses, 2D section models
- **Evidence:**
  - The SB-261 geometry is from the vendor IGES (REV A). The B1 rail and coupon results are kernel (Onshape scratch) or CALC.
  - **Nothing is physically tested.** **PHYSICAL VALIDATION REQUIRED.**
  - Torque: band -6 is 0.96–1.13 N·m per hinge against ≈ 0.83 required (SF ≈ 1.16). Load, material and temperature ratings are unpublished.
- **Documentation status (unchanged by this checkpoint):**
  - **D-010 is still pending the owner's decision.** B1 is **not** officially selected.
  - **D-007 is not accepted** (still proposed).
  - The B1 / SB-261 work is exploratory, pre-decision work.
  - The existing architecture-A documentation (`nomad.yaml`, `docs/decisions.md`, `docs/mechanical-spec.md`, `NOMAD_E_Prototype`) was **not** rewritten.
- **Not changed:**
  - `nomad.yaml` values, production geometry and FeatureScript
  - the NOMAD Onshape document
  - `NOMAD_D010_Concepts`
- **Onshape:** the SB-261 models live only in the connector's scratch document (workspaces in `prototypes/B1_SB261/SOURCES.md`). No production writes. API 517 of 2,500.
- **Kept outside Git:**
  - the vendor IGES/zip (third-party file; URL and SHA-256 recorded)
  - ignored caches and generated coupon STL/SCAD
  - `.claude/` local settings
- No push.

## 2026-10-01 — D-010 locked: B1 selected; source of truth migrated; V1 requirements sheet

- **Decision (owner):** **D-010 accepted: Architecture B1** is the NOMAD V1 lid/solar architecture.
  - It is one solar leaf behind the display lid, on two structural friction hinges.
  - SB-188-SB-261-6 is the current selected hinge candidate.
  - Leaf motion about 0–190°, cable sleeve with R12, mandatory stay, Voltaic P108 panel candidate.
  - Physical validation remains a future gate.
- **Architecture A** (D-004, D-009, Rounds B–E solar and lid-rail work, class-A lid, the E2 lid, the P0.1/P0.2 coupons) is **SUPERSEDED / DEFERRED FOR NOMAD V1**.
  - Nothing was deleted or rewritten.
  - Each A-path record got a one-line banner under its title (24 files, additions only). The D-010 study records got a "decided" banner.
- **Source-of-truth changes:**
  - `docs/decisions.md`:
    - D-010 rewritten as accepted (history kept).
    - D-004 and D-009 marked superseded for V1.
    - Notes added to D-006, D-007 and D-008.
  - `CAD/parameters/nomad.yaml`:
    - header and `meta.architecture`
    - the `solar` group and the class-A lid parameters marked superseded (comments and one `note`)
    - new groups `lid_b1` (2) and `solar_leaf` (12): two provisional owner targets (`SOLAR_LEAF_ANGLE_MAX` 190°, `SOLAR_LEAF_CABLE_BEND_RADIUS` 12); everything else TBD with working inputs from D-010 Phase 2 and `prototypes/B1_SB261/`
    - **No existing value, working input or formula changed.**
  - Generated parameter blocks regenerated:
    - `NOMAD_P01.fs` and `NOMAD_E_Prototype.fs`, the 14 new constants only.
    - Local only; **not written to Onshape**; no feature uses them.
  - `docs/mechanical-spec.md`: B1 sections added; A sections marked superseded.
  - `docs/solar.md`: rewritten for B1 (A kept as a superseded section).
  - Also updated: `docs/architecture.md`, `docs/hardware.md`, `docs/power.md`, `README.md`, `CLAUDE.md`, `CAD/README.md`, `prototypes/P0.1/README.md`, and the `prototypes/B1_SB261/` status lines.
- **New:** `docs/v1-requirements.md`.
  - Requirements by subsystem with the LOCKED / DEFINED / CANDIDATE / TBD / VALIDATION REQUIRED / BLOCKED scheme.
  - Battery/power and thermal are explicitly unresolved.
  - The 14-step V1 dependency order.
- **D-007:** still **proposed**. No owner acceptance exists in the repository. The open owner decisions are listed in D-007 and `v1-requirements.md` §17.
- **Checks:**
  - YAML validation and both generated-block checks pass.
  - The base layout and E-lid layout checks pass.
  - Every study script gives output identical to the pre-change baseline, apart from the expected parameter count.
- **No production geometry changed.** No Onshape calls (API 517 of 2,500). Nothing purchased. No push.
- **Next:** V1 dependency step 3, down-select real hardware envelopes.

## 2026-10-01 — E-POWER-001: V1 hardware + energy characterization (desk study, €0)

- **Record:** `prototypes/V1/E-POWER-001_hardware_energy_characterization.md`. It has 26 sources, all retrieved 2026-10-01: manufacturer sources first, third-party sources labelled.
- **Selected:** unchanged (Pi 5 8 GB only).
- **Candidates characterized:**
  - Pi 5 power; Active Cooler; M.2 HAT+; Raspberry Pi SSD, with WD SN740 as the power reference
  - displays: Winstar WF101NTYA4LNN0, AUO B101UAN01.C, Waveshare (G)
  - Perixx keyboards and trackpads
  - SparkFun / u-blox DAN-F10N and the ANN-MB5 antenna
  - display hinges: Southco E6, TorqMaster SB-254-H
  - Voltaic P108 (official data refreshed: 9.92 W peak, Voc 20.45 V, 17.34 V / 570 mA)
- **Preliminary power model:** published data only. Documented subtotals, each + TBD:
  - standby ≈ 10.1–10.9 W
  - normal ≈ 10.9 W
  - max sustained ≈ 17.7–22.4 W
  - **The display is the largest load. The P108 peak is below every state.**
- **Energy principle recorded:** solar = field energy replenishment, not the primary power source (`docs/power.md`, SYS-10).
- **Key conflicts (documented, not solved):**
  - Display at full backlight 6.8 W typ > the ≤ 6 W target.
  - Candidate displays thicker or taller than the working envelope.
  - The controller board is uncharacterized.
  - No keyboard ≤ 8 mm (retail 14–21 mm).
  - PERIPAD-501 II unverified.
  - The DAN-F10N is an antenna module, and has no GLONASS (docs corrected).
  - M.2 HAT+ 0–50 °C ambient.
  - Pi draws 1–1.4 W when "off" unless `POWER_OFF_ON_HALT=1`.
  - The 5 V rail must be 5 A-capable for the 1.6 A USB budget.
- **Docs updated:** `docs/hardware.md`, `docs/power.md`, `docs/v1-requirements.md`, `docs/architecture.md`, `docs/solar.md`, `README.md`, `CLAUDE.md`.
- **Not changed:**
  - `nomad.yaml`, so no TBD was replaced. Verified values are recorded for the step 7 re-baseline.
  - Production CAD.
  - `decisions.md`.
- **No battery or power electronics chosen.** No Onshape calls. Nothing purchased. No push.
- **Next:** step 5, the power architecture and battery capacity from the characterized loads. This needs the owner's runtime target.

## 2026-10-02 — E-POWER research campaign (research only; nothing selected)

- **Dossier:** `docs/E-POWER-RESEARCH-CAMPAIGN.md`. **Calculator:** `prototypes/V1/epower_campaign_calc.py` (standard library; reproduces every derived number).
- **Scope:** display and controllers, the refined load model, battery chemistry and scenarios (4 / 6 / 8 h × LOW / NORMAL / HIGH / WORST), bay fit, power architectures A–D, charging, solar yield (PVGIS 5.3, Sofia, 2018–2023 hourly), MPPT compatibility, thermal, mass, power-flow model, candidate tables and EU prices.
- **Key findings** (CALC from MFR / 3P data and stated assumptions):
  - **Display:**
    - D-A (AUO eDP + Beck BTC-mini-eDP): 2.7 / 3.3 / 4.6 W at 25 / 50 / 100 % PWM.
    - D-W (Winstar LVDS + Beck BTC-mini + LED driver): 3.4 / 5.0 / 8.4 W.
    - No documented panel meets ≥ 400 nit + matte + ≤ 6 W.
  - **System at battery:** NORMAL 8.7 W (D-A) / 10.6 W (D-W); HIGH 18.0 / 22.1 W.
  - **The 90 × 82 × 30 bay holds at most 4 × 21700:** 71 Wh (Samsung 50E) or 92 Wh (Molicel M65A, datasheet v0.1, marginal fit).
    - NORMAL 4–6 h fits.
    - NORMAL 8 h and every HIGH-load target do not.
    - A second layer exceeds the 40 mm body height.
  - **Above 100 Wh needs airline approval** (IATA 2026).
  - **Solar into battery:** about 48 Wh/day summer median, 36 annual mean, 16 winter median, 5 on poor winter days. That is about 91 / 68 / 30 / 10 % of a NORMAL 6 h day.
  - **A buck-only MPPT cannot charge 4S Li-ion from a hot P108;** buck-boost (BQ25798, LT8491) works with any pack.
  - **Thermal:** M.2 HAT+ 0–50 °C ambient caps outside air at about 35–40 °C. HIGH-load base heat of 13 W needs about 2.4 CFM.
- **Conflicts and decisions:** EP-C01–EP-C20 and the requirement-conflict table are documented and **not applied**. Owner decisions are listed in dossier §19.
- **Corrections recorded:**
  - PERIPAD-501 II 86 × 75 × 13 mm is verified by the official Perixx manual.
  - PERIBOARD-416 is 16 mm per its manual (the product page says 21).
- **Not changed:** `nomad.yaml`, CAD, Onshape, requirement statuses. No Onshape calls, no purchases, no push.
- **Source-access notes:** CAPTCHA and bot-checked sites were not bypassed; snippet-only values were dropped or verified at the source.
