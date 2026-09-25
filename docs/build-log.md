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
