# CLAUDE.md — NOMAD

Persistent working instructions for Claude Code. The approved engineering specification in `docs/` takes precedence over this file. If the two disagree, fix this file; do not treat it as a second spec.

## Project

NOMAD is a portable, offline-first field computer. Principle: **assume the infrastructure is gone.**

Priorities, in order: function, reliability, serviceability, modularity, mechanical simplicity, manufacturability, offline capability, expandability, aesthetics. Never trade the first eight for appearance. Prefer a simple, robust mechanism over a clever one unless the complexity buys a substantial real benefit.

## Roles

- **Project owner:** the final decision-maker.
- **Engineering assistant:** architecture, requirements, tradeoffs.
- **Claude Code:** turns approved requirements into CAD, project files, docs and automation.

## Approval gate

Do not silently change: overall architecture, the solar concept, display orientation, keyboard/trackpad layout, battery location, major module placement, mechanism architecture, motors (none without approval), or subsystem scope. If a change seems necessary, explain the problem, propose alternatives with tradeoffs, and wait. Small, reversible changes that are consistent with the spec may be made autonomously.

## Current status

- **ACTIVE ARCHITECTURE: B1 (D-010 accepted 2026-10-01).**
  - B1 is one solar leaf behind the display lid, on two friction hinges. TorqMaster SB-188-SB-261-6 is the current hinge candidate.
  - Leaf motion is 0–190°, with a cable sleeve (R12) and a mandatory rear stay. Voltaic P108 is the panel candidate.
  - Physical validation is a future gate.
  - Record: `prototypes/B1_SB261/`. Requirements and dependency order: **`docs/v1-requirements.md`**.
  - **Architecture A** (sliding/tilting cassettes: D-004, D-009, Rounds B–E solar/lid-rail work, class-A lid, E2 lid) is **SUPERSEDED / DEFERRED FOR V1**. Its records below are kept as history, not active work.
  - Next: dependency step 3 (down-select real hardware envelopes).
- Phase: Virtual V1 (finish the virtual design before buying hardware). Prototype: **P0.1** (mechanical proof of concept).
- Phase 0 (workspace setup) is done. The NOMAD Onshape document exists (link in `CAD/README.md`). Its only Feature Studio is `NOMAD_P01_Coupons`, used by the owner-created Part Studio `P0.1 Coupons` (P0.1 test coupons, below); it holds no NOMAD product (chassis) geometry yet.
- Phase 1 Round A (skeleton + keyboard/trackpad/display envelopes) has been modeled and tested in the scratch context only; results are in `docs/build-log.md`.
- Round A.1 (closed-lid clearances, hinge comparison, body-height check) has been modeled. The hinge direction is now set provisionally by D-006.
- Round A.2: the hinge-axis feasibility map is in `prototypes/P0.1/hinge_feasibility_map.md` (model: `CAD/tools/hinge_feasibility_2d.py`, cross-checked in Onshape). A.2b varies the closed gap (`prototypes/P0.1/closed_gap_sweep.md`).
- Round B (initial solar kinematic skeleton) **[Architecture A: superseded / deferred for V1 by D-010]** has been modeled: `prototypes/P0.1/solar_round_b.md` (model: `CAD/tools/solar_skeleton_model.py`, cross-checked in Onshape). The solar rail architecture is **not chosen** and awaits the owner.
- Round B.1 (V1 feasibility pass) **[Architecture A: superseded / deferred for V1 by D-010]** has been modeled: `prototypes/P0.1/solar_v1_feasibility.md` (model: `CAD/tools/solar_v1_feasibility.py`). V1 needs minimal fixes to be viable and is **not chosen**.
- Round B.2 (lid structure / printability screening of concepts A, B and C) **[Architecture A: superseded / deferred for V1 by D-010]** has been done: `prototypes/P0.1/lid_structure_screening.md`. No concept is chosen.
- P0.1 test coupons (rail A1/A2, rear shell B1/B2) **[Architecture A: superseded / deferred for V1 by D-010]** have been designed on the provisional Concept C basis: `prototypes/P0.1/coupons/P01_test_coupons.md`. They are not yet printed or tested. **Onshape CAD:** Feature Studio `NOMAD_P01_Coupons` in the NOMAD document (custom feature "P0.1 Coupons"; snapshot `CAD/featurescript/NOMAD_P01_Coupons.fs`), validated in scratch and inserted by the owner into the Part Studio **P0.1 Coupons** (13 parts, visually verified). The coupon geometry is persistent in the NOMAD document; physical coupons are not yet printed or tested. Reference STLs: `CAD/coupons/P0.1/` via `py CAD/coupons/P0.1/generate_coupons.py`. The two must agree; `onshape_crosscheck.py` gives the expected sizes and volumes.
- Round C (base chassis V0.1 architecture, envelope model) has been modeled and cross-checked in scratch: `prototypes/P0.1/base_v01_architecture.md` (layout spec + checks: `CAD/tools/base_v01_layout.py`, which also generates the FeatureScript layout block; regenerate with `py CAD/tools/base_v01_layout.py --write`). Its placement and service strategy are **proposed** as D-007 and await the owner. It is not in the NOMAD Onshape document.
- Round C.1 (compute-placement study A–E + lid/port screen) has been modeled: `prototypes/P0.1/compute_placement_study.md` (`CAD/tools/compute_placement_study.py`). Neutral comparison; no concept chosen; D-007 still proposed.
- Round C.2 (lid/hinge/port feasibility map, side-port study, print-split screening) has been modeled: `prototypes/P0.1/c2_architectural_screening.md` (`CAD/tools/c2_screening.py`). No choice made; D-007 still proposed.
- Round D (lid stack-up / structural envelope, architectures A–E) **[Architecture A: superseded / deferred for V1 by D-010]** has been modeled: `prototypes/P0.1/lid_stackup_study.md` (`CAD/tools/lid_stackup_study.py`). No lid thickness declared; working `LID_THICKNESS` 25 is flagged as below every studied architecture (37–42 enclosed).
- Round D.1 (lid architecture convergence: sandwich / modular / ribbed classes, rail strips, hinge/port, handling) **[Architecture A: superseded / deferred for V1 by D-010]** has been modeled: `prototypes/P0.1/lid_architecture_convergence.md` (`CAD/tools/lid_architecture_convergence.py`). Nothing chosen or ranked; window ~37.5–42 mm; awaits owner review before any persistent lid CAD.
- P0.2 physical risk coupon package **[Architecture A: superseded / deferred for V1 by D-010]** defined (not printed or ordered): `prototypes/P0.1/P0.2_physical_test_plan.md`.
  - It reuses the P0.1 coupons and adds sandwich plates B-S30 / B-S20 / B-INFILL, a 2.0 mm block and a load bar, generated by `py CAD/tools/generate_p02_coupons.py` into `CAD/coupons/P0.2/`, local only and not in Onshape.
  - A2 strips must be shimmed snug, and both lips measured.
- Round E (digital prototype, D-008, Round E only; its E2 lid / solar / F3 / D-009 work is Architecture A, superseded / deferred for V1 by D-010; the E1 base still shows the proposed D-007): plan `prototypes/P0.1/round_e_implementation_plan.md`, log `prototypes/P0.1/round_e_digital_prototype.md`.
  - E0.5: `nomad.yaml` working values reconciled (lid formula → 37.6, class A, PROVISIONAL — PENDING P0.2; solar V1 + fixes: carriage 22.6, deploy 8, travel 158, link 11.5; new lid/solar/hinge working params). Historical study inputs pinned in their scripts so reports reproduce. The rear-plug conflict (−7.0 at 135°) is reported as a known OPEN CONFLICT, not resolved.
  - E1: Feature Studio `NOMAD_E_Prototype` (Onshape element `40d4ae5868441bcb8882fe3a`) with "NOMAD E Base" and "NOMAD E Service"; kernel-checked in scratch (Round C geometry exact). Findings F1 (panel screw heads vs walls) and F2 (sled screw heads vs panel) are open. E1 accepted by the owner (no architectural changes).
  - E2: feature "NOMAD E Lid" (class A 37.6 lid, B.1 V1 + fixes solar both sides, Ø8 hinges, 9 mate connectors, preview-only pose dialog); layout/checks `CAD/tools/e_lid_layout.py`; kernel cross-check exact. Finding F3 (B.1 hub-bracket envelope 1.0 mm into the rail floor) was found here and is now resolved (below).
  - **F3 APPROVED AND IMPLEMENTED — OPTION B** (`prototypes/P0.1/round_e_f3_investigation.md` §10): `SOLAR_HUB_AXIS_OFFSET_Z` → −5.5 (axis +2.0), new working `SOLAR_BRACKET_WALL` 2.5, carriage slot boss; bracket–floor 1.0 over the full travel; local suite, study reproducibility and Onshape scratch exact; persistent `NOMAD_E_Prototype` updated. Stopped for review; E3/E4/E7 not started. Bore length (O1) and pin material (O2) are separate open decisions.
  - **D-009 (solar tilt index lock + hub-pin anti-rotation) accepted and implemented locally, PENDING PHYSICAL VALIDATION** (`prototypes/P0.1/round_e_solar_index_lock_implementation.md`).
    - Mechanism: 11 × 15° positions, Ø1.5 hardened pin in a stainless plate on the hub-pin tip, anti-rotation plate + Ø3 dowel in the carriage, counter sleeve, thumb slider.
    - Validation: local suite and Onshape scratch exact; SF ≥ 2 at 1.26 N·m (RT, inferred).
    - **±80° hard stops are NOT packaged** (open decision: S1 / S2 / S3, report §8). The persistent `NOMAD_E_Prototype` is therefore NOT written: the local `.fs` is ahead of Onshape.
    - S1 feasibility study: **FAIL / needs redesign** (`prototypes/P0.1/round_e_s1_hard_stop_study.md`, tool `CAD/tools/s1_stop_study.py`, non-production).
      - The stop reaction overloads the PETG hub-bracket bore and the pin root, and ±80° is not holdable with printed location.
      - (Erratum: its pin-root figures are withdrawn.)
    - D-009 load reassessment (`round_e_d009_load_reassessment.md`): pin root unchanged. The **PETG hub bracket is below its handling-basis SF 2** (bearing 1.88, tear-out 1.73, peak tension 1.61) once the lock's transverse reaction is included. The minimum fix is an outboard metal bearing (geometry change). Awaits the owner.
    - S1-R journaled stop yoke (`round_e_s1r_stop_yoke_study.md`, tool `CAD/tools/s1r_stop_study.py`): **PASS, READY FOR OWNER REVIEW** (±80.000°, stop-path SF ≥ 2 at T_d, worst ±2.41°). Not approved for Onshape; does not fix the hub-bracket item.
- **D-010 solar architecture comparison: DECIDED, B1 selected on 2026-10-01** (`prototypes/P0.1/d010_solar_architecture_comparison.md`, tool `CAD/tools/d010_solar_architecture_study.py`): sliding wings (A) vs solar lid (B). The history follows.
  - Recommends **B1** (single top-hinged leaf, positive angle lock, vented air gap, rear stay), gated by a physical tipping / hinge-torque / wind mock-up.
  - **Phase 2** (`prototypes/P0.1/d010/d010_solar_architecture_phase2.md`, tool `CAD/tools/d010_phase2_study.py`):
    - **RECOMMEND B1, conditional.** A's cable routing is not V1-acceptable, and the B1 stay is mandatory.
    - Both architectures are modelled in the isolated Onshape Feature Studio **`NOMAD_D010_Concepts`** (`d4619014058afc59574f42aa`; snapshot `CAD/featurescript/NOMAD_D010_Concepts.fs`, regenerated with `--emit`).
    - The owner must insert the feature into a new Part Studio.
    - Phase 1's visor and mass claims are corrected (erratum added).
  - **Owner decision 2026-10-01: B1.** D-009 / S1-R are superseded for V1 (records kept). The B1 hinge rail around SB-261 was validated in Onshape scratch (`prototypes/B1_SB261/`; not in the NOMAD document).
  - Insert interface for the coupons (P0.2-HW, `prototypes/P0.1/P0.2_insert_interface.md`): Ø4.0 × 7.0, drilled up to the datasheet pilot. The Onshape dialog depth is still 6 until the owner sets 7.
- D-001 accepted: P0.1 geometry is generated with FeatureScript. This covers P0.1 only, not the long-term CAD architecture.
- D-002 accepted: `CAD/parameters/nomad.yaml` holds the authoritative parameter values.
- D-003 accepted: the trackpad is centred below the keyboard, and both sit on the chassis centreline. Positions are parameterized; trackpad dimensions are TBD until the modules are selected.
- D-004 (SUPERSEDED / DEFERRED FOR V1 by D-010; was accepted 2026-09-25): each solar cassette slides laterally out of the lid, then tilts independently about an axis approximately along its slide direction (±60–75°). Rotation locks at indexed positions. The rail carries structural load and a dedicated hub/pin carries rotational load; gears only position. No motors, no slip ring. Rail, hub, lock and axis geometry, including hub location, are left to P0.1 validation.
- D-007 (base V0.1 placement and service) is still **proposed**, not accepted. The open owner decisions are in `docs/decisions.md` D-007.
- D-010 accepted 2026-10-01: **B1** is the V1 lid/solar architecture. Components are not all selected (see `docs/v1-requirements.md`).
- D-006 accepted as a **provisional** P0.1 direction: hinge axis at or near the base rear face; `LID_CLOSED_GAP` working value 2.0 mm. The exact axis position and the hinge hardware stay TBD until the mechanism prototype.
- See `docs/decisions.md`.

## Sources of truth

| What | Where |
|---|---|
| Mechanical parameter values | `CAD/parameters/nomad.yaml` (machine-readable master, D-002) |
| Parametric CAD | Onshape (master for geometry) |
| FeatureScript snapshots | `CAD/featurescript/` (copies of the Onshape Feature Studios; Onshape wins on conflict) |
| Exports (STEP/STL/3MF/drawings) | `CAD/exports/`, `CAD/drawings/`, or releases: derived, never authoritative |
| Specifications | `docs/` |
| Decisions | `docs/decisions.md` |
| Build/test history | `docs/build-log.md`, `prototypes/<rev>/` |
| Software | Local Git repo; GitHub `origin` is the remote and backup |

## Onshape MCP constraints

The connected Onshape MCP is **FeatureScript-only**. It can:
- create and list Feature Studios (given a document ID and workspace ID)
- read and write Feature Studio code
- test code in a scratch Part Studio
- search the FeatureScript docs

It **cannot** list or create documents, Part Studios, Variable Studios or Assemblies. It cannot insert features into a user Part Studio, read existing geometry, create mates, or export. Do not assume other operations exist.

- The project owner supplies document URLs, inserts custom features, and does exports.
- Every tool call spends the owner's Onshape API allocation: 2,500 requests per annual cycle. Test before writing, batch work, and check `get_api_usage` periodically.
- `put_featurescript` overwrites the entire Feature Studio: always `get_featurescript` first.
- `test_feature` costs about 9 requests and returns notices only (no console output). Messages are truncated after roughly 330 characters. The test harness therefore returns a compact report through a deliberate `regenError`.

## Parameter pipeline

- Edit `CAD/parameters/nomad.yaml`, then run `py CAD/tools/yaml_to_featurescript.py` to regenerate the `GENERATED PARAMS` block in `CAD/featurescript/NOMAD_P01.fs`. Never edit that block by hand.
- Run `py CAD/tools/yaml_to_featurescript.py --check` to verify the block is current.
- Test payload: `py CAD/tools/build_test_payload.py <out>` builds `NOMAD_P01.fs` without its production features, plus `NOMAD_P01.test.fs`.
- Python is `py` (3.14, standard library only). Bare `python` is the Microsoft Store alias.
- Before any CAD change: inspect, understand dependencies and downstream effects, and never destroy working geometry for convenience.

## CAD conventions

- Model in three levels: **envelope**, then **interface** (holes, bosses, connectors, clearances), then **detail**. Add detail only where it affects fit, motion, strength, assembly, manufacturing, cable routing or cooling.
- Every uncertain dimension is a named parameter (UPPER_SNAKE_CASE, mm), never a hidden constant. Define it in `CAD/parameters/nomad.yaml` first, with its status (verified / derived / provisional / TBD) and source, then reflect it in `docs/mechanical-spec.md`. FeatureScript parameter values are derived from the YAML and never edited as the master.
- Use clear feature and part names. Name keep-out volumes `KEEPOUT_*` and envelopes `ENV_*`.
- Avoid giant monolithic feature histories. Split them into logical modules.
- Target FDM PETG. Watch wall thickness, overhangs, print orientation, supports, heat-set inserts and tolerances for repeated disassembly. Use metal for structural shafts and pins.
- Keep a small fastener family (M2.5, M3) with heat-set inserts for serviced joints. Match the fastening method to the joint: screws for structure, clips for frequent access, captive/quarter-turn fasteners for service panels, magnets and pins for covers.
- Every important cable gets an intentional path, with bend radius, strain relief and protection. Never route wires through gears. No slip rings in V1.
- The battery must stay removable and serviceable. Never block cooling airflow.

## Reporting

Report progress under: **COMPLETED / CURRENT MODEL / ASSUMPTIONS / PROBLEMS / NEXT ACTION / APPROVAL REQUIRED**.
Always say which of these a claim is: *modeled*, *simulated*, *inferred*, *physically tested* or *measured*. They are not equivalent. Physical testing is authoritative for fit and motion.

## Git

- Default branch: `main`. Remote: `origin` (GitHub).
- Commit messages are meaningful and prefixed with the revision, e.g. `P0.1: add solar cassette envelope`. Never use "update", "test" or "final2".
- Summarize changes before major commits. Push only with owner approval.
- Never delete files, rewrite history, force-push, remove branches or discard changes without explicit approval.
- Never commit secrets, tokens or personal information. `.claude/settings.local.json` is git-ignored.

## Revision naming

P0.1, then P0.1.x (sub-revisions), P0.2 (physical-measurement revision), P1 (functional chassis), P1.x, V1 (validated prototype). For each major change, record what changed, why, what problem it solved, and what tradeoff it introduced (in `docs/decisions.md` / `docs/build-log.md`).
