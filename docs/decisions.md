# Engineering Decisions

Status values: **proposed** (awaiting the project owner), **accepted**, **superseded**, **rejected**.

For each decision, record: context, the decision, alternatives, the tradeoff, and status.

---

## D-001 — FeatureScript-driven CAD for P0.1

- **Status:** accepted (2026-09-25), limited in scope
- **Scope limitation:** FeatureScript is the geometry-generation and prototyping layer for **P0.1 only**. This decision does not commit the rest of NOMAD's CAD architecture to FeatureScript. The approach for P0.2 onward (native Onshape modeling, Assemblies, or a mix) will be a separate decision.
- **Context:** The only Onshape integration available is a FeatureScript-only MCP. It cannot create documents, Part Studios, Variable Studios or Assemblies, and it cannot insert features into a user Part Studio.
- **Proposal:** Build P0.1 as custom features in a `NOMAD_P01` Feature Studio: master parameters, layout skeleton, envelopes, solar mechanism and a clearance check. The project owner inserts the features into a single multi-part Part Studio. Motion states (slide extension, rotation angle, lid angle) are parameters, and the clearance check evaluates them.
- **Alternatives:** The project owner models natively in Onshape, with Claude writing specs only.
- **Tradeoff:** The model is fully parametric, reproducible and diffable in Git, and Claude can run clearance checks in a scratch context. The costs: the geometry is less convenient for later hand modeling, it spends API allocation, and "motion" is geometric only (modeled, not tested).

## D-002 — Location of the master parameter table

- **Status:** accepted (2026-09-25)
- **Decision:** `CAD/parameters/nomad.yaml` is the **machine-readable source of truth** for NOMAD mechanical parameters. `docs/mechanical-spec.md` remains the **human-readable engineering specification**. FeatureScript consumes, or is generated from, the YAML values but does not own the authoritative values.
- **Consequences:**
  - A parameter changes in `nomad.yaml` first. `mechanical-spec.md` and the FeatureScript constants are then brought into line with it.
  - Parameter values in a Feature Studio are derived copies. If they differ from `nomad.yaml`, the YAML is correct and the Feature Studio must be regenerated or updated.
  - Values stay version-controlled and diffable in Git, and do not depend on Onshape API access.
- **Rejected alternatives:** Feature Studio constants as the master (this couples the authoritative values to one CAD tool); an Onshape Variable Studio (the MCP cannot write it).

## D-003 — Trackpad position

- **Status:** accepted (2026-09-25), with constraints
- **Decision:** The V1 baseline places the trackpad centred below the keyboard.
- **Constraints:**
  - The keyboard and trackpad are both centred on the chassis longitudinal centreline.
  - The trackpad position stays parameterized, so it can move later without restructuring the chassis.
  - The trackpad dimensions stay TBD until the actual keyboard and trackpad modules are selected.
  - Current target dimensions must not be hard-coded as verified geometry.
- **Reason:** Placing the trackpad beside a ~280 mm keyboard makes the base about 380 mm wide, which is much wider than a 10.1" display lid.
- **Tradeoff:** The base gets deeper (keyboard depth + trackpad depth + margins) in exchange for a narrower base that matches the lid.

## D-004 — Solar cassette kinematic architecture

- **Status:** accepted (2026-09-25) as the P0.1 solar kinematic architecture. **SUPERSEDED / DEFERRED FOR NOMAD V1** on 2026-10-01 by D-010 (B1 selected). The record below is kept unchanged as Architecture A history.
- **Decision:**
  - Each cassette slides laterally outward from its stored position in the display lid.
  - After deployment, each cassette rotates/tilts toward the sun independently of the other.
  - The primary rotation axis runs approximately along the cassette's slide/deployment direction.
  - The target V1 rotation range is approximately ±60° to ±75°.
  - Rotation uses discrete indexed positions with a positive mechanical lock. V1 has no motors and no continuous 360° rotation.
- **Load paths:**
  - The sliding rail carries deployment and structural loads.
  - A dedicated rotation hub/pin carries the cassette's rotational load.
  - Printed gears are for positioning and actuation only, never the primary structural load path.
- **Wiring:** A controlled, protected cable path runs through the slide/rotation mechanism. No slip ring in V1.
- **Scope:** This decision defines the intended kinematics only. The exact rail, hub, lock and axis geometry is subject to P0.1 mechanical validation. Nothing here claims the final geometry is validated.
- **Tradeoff:** Tilting about the slide axis keeps the rotation hub on the load path the rail already provides, and gives a simple one-axis sun adjustment. Only one tilt axis is adjustable, so orienting toward the sun also depends on how the machine itself is placed.

## D-006 — Provisional hinge direction and closed-lid gap (P0.1)

- **Status:** accepted (2026-09-25) as a **provisional P0.1 working direction**. It is not a final hinge design.
- **Context:** Rounds A.1, A.2 and A.2b (`prototypes/P0.1/hinge_feasibility_map.md`, `closed_gap_sweep.md`).
  - An inset hinge (axis 8 mm inside the rear face) collides with the base unless the axis is very high or the base carries a large relief (44 cm³).
  - A hinge axis on or behind the rear face clears in every tested position.
  - With the closed-lid gap equal to MIN_GAP, the closed pose meets the requirement with zero margin.
- **Decision, kept at four distinct levels:**

  | Level | Status |
  |---|---|
  | **Architectural direction** | Provisional: **hinge axis at or very near the base rear face.** Not an internally inset hinge, not the large base-relief solution, and no forward/inset hinge chosen merely to reduce rear overhang. |
  | **Exact axis position** (`HINGE_AXIS_OFFSET`, `HINGE_AXIS_HEIGHT`) | **TBD.** Working inputs are inset 0 and height 0, but the height stays a parameter. To be resolved in the physical mechanism prototype. |
  | **Hinge hardware** (type, shaft diameter, mounting geometry) | **TBD.** To be resolved in the physical mechanism prototype. |
  | **Closed-lid gap** (`LID_CLOSED_GAP`) | **Working value 2.0 mm; authoritative value TBD.** Chosen to give about 1.0 mm of modeled margin over MIN_GAP. |

- **`LID_CLOSED_GAP` vs `MIN_GAP`:**
  - `LID_CLOSED_GAP` is the *geometric* standoff between base and lid when closed.
  - `MIN_GAP` (1.0 mm) remains the general *minimum modeled clearance requirement*.
  - They are separate parameters and are no longer linked.
- **Tradeoffs:**
  - A rear-face hinge increases rear overhang when open. With a 2.0 gap at 105°: 61.8–90.8 mm at inset 0 (depending on axis height) and up to 98.3 mm at inset −6, versus 54.2–76.7 mm for the feasible inset hinges.
  - It may place hinge hardware at or proud of the rear face, which competes with the rear port zone. *(inferred)*
  - The 2.0 mm closed gap adds about 1 mm to the closed thickness.
- **Note (2026-10-01, D-010):**
  - D-006 applies to the **display** hinge and is unchanged by B1. It stays provisional, and the display-hinge hardware is TBD.
  - B1 raises the display-hinge holding requirement to about 1.6 N·m per hinge with a φ-max stop (CALC, D-010 Phase 2 §10).

## D-005 — Default branch `main`

- **Status:** accepted (Phase 0 approval, 2026-09-25)
- **Decision:** The unborn `master` branch was renamed to `main` before the first commit. There was no history to lose.

## D-007 — Base chassis V0.1 architecture (Round C)

- **Status:** **proposed** (2026-09-25), awaiting the project owner. Nothing below is accepted.
- **Context:** Round C: the first complete base architecture built around component envelopes, before any electronics are bought. Full report: `prototypes/P0.1/base_v01_architecture.md`.
  - With BODY_HEIGHT 40 (working), only 26.5 mm is free under the keyboard; the full 35 mm height exists only in the palm-rest regions beside the trackpad.
  - A conservative Pi 5 + cooler + M.2 HAT+ stack (~25–28, inferred) does not fit under the keyboard.
- **Proposal:**
  - **Structure:** one printed shell (walls, deck with keyboard/trackpad openings, bulkheads, bosses), open at the bottom. It is closed by a removable main service panel and a separate battery door. Keyboard tray, trackpad tray and compute sled are separate replaceable plates. No electronics are structural.
  - **Placement** (major module placement and battery location, under the approval gate):
    - compute: right palm-rest bay, Pi stack on a sled;
    - battery reserve: left palm-rest bay, behind its own door;
    - power electronics: under the keyboard, left;
    - GNSS: under the keyboard, centre-left, as a separate cabled module (not stacked on the Pi);
    - compute power: under the keyboard, right;
    - I/O: two replaceable rear port panels;
    - hinge mounts: reserved at both rear corners (D-006).
  - **Cooling:** front intake → duct → Pi → right-side exhaust (reserved volumes only).
  - **Service:** electronics come out downward through the main panel, the battery through its door, and the keyboard/trackpad upward. No glue.
- **Alternatives:**
  - Compute under the keyboard: needs BODY_HEIGHT ≳ 45 (inferred).
  - Battery under the keyboard with compute in a palm bay: moves mass rearward and puts the widest flat volume (under the keyboard) to a battery that doesn't need height.
  - Side-wall I/O instead of rear I/O: avoids the lid-sweep conflict, but puts ports on the sides.
  - Removable top deck: breaks the "service without removing the keyboard" requirement.
- **Tradeoffs:**
  - The compute bay sits under a palm rest (heat, inferred).
  - Rear ports are limited to Z ≤ 19 by the lid sweep of the D-006 hinge. This holds only for a 25 mm lid; it conflicts at 31.5 and 42.5 (modeled). It couples the base to the pending lid-thickness decision.
  - The shell needs a ≥ 310 mm-class bed or a split.
- **Note (2026-10-01):**
  - D-007 is **still proposed**. D-010 (B1) does not accept it, and the repository holds no owner acceptance of it.
  - **B1 changes one input:** the lid is thinner (B1 stack ~31 EST vs the class-A 37.6). The B1 plug-zone result is +2.07 at φ 125 and −2.3 mm at φ 135, so the rear-I/O conflict is reduced, not solved.
  - **Owner decisions still needed** (from `prototypes/P0.1/c2_architectural_screening.md` §4):
    1. Placement: accept as working, amend, or reject (compute in the right palm bay, battery in the left bay, electronics under the keyboard).
    2. I/O policy: rear vs side.
    3. GNSS as a separate cabled module.
    4. Shell structure: one body or split.
    5. Whether the working body envelope 301 × 235 × 40 stays.
  - These depend on the real hardware envelopes and the power and thermal architecture (`docs/v1-requirements.md` §18).

## D-008 — Round E digital prototype implementation method

- **Status:** accepted (2026-09-26) for **Round E only**. It is an implementation decision, not a project-wide CAD architecture decision; D-001 stays limited to P0.1.
- **Decision:**
  - Round E's persistent geometry is generated by FeatureScript in a new Feature Studio `NOMAD_E_Prototype`, written through the Onshape MCP.
  - The owner creates the Part Studio, inserts the features, and builds the Assembly and its mates manually. The connector cannot create Part Studios, Assemblies or mates.
  - `nomad.yaml` remains the single source of values (D-002). The Feature Studio's parameter block is generated from it, and its feature dialogs carry visualization options only (keep-outs, lid variant, pose), never engineering values.
- **Scope decisions taken with it (owner, Round E):**
  - Lid class A (sandwich, T 37.6) is the primary visualization, marked **PROVISIONAL — PENDING P0.2 PHYSICAL VALIDATION**; classes B / C only as optional visual variants.
  - Lid revolute 0–135°, with the known rear-plug-zone intrusion left visible.
  - Representative Ø8 hinge barrel with leaf/block geometry.
  - Mirrored left/right solar systems, each in its own half of the lid (V1 + fixes).
  - Sub-assemblies BASE / SERVICE / LID / HARDWARE.
- **Tradeoff:** full reuse of the validated local models and the YAML pipeline, and diffable geometry, at the cost of manual Assembly work and API allocation per update. The prototype is not production CAD.
- **Note (2026-10-01, D-010):**
  - **Superseded for V1:** the lid and solar scope of Round E (class A lid, mirrored sliding solar systems, the E2 "NOMAD E Lid" feature) is Architecture A.
  - **Still valid:** the D-008 implementation method itself. The E1 base remains a visualization of the *proposed* D-007 base.

## D-010 — NOMAD V1 Lid/Solar Architecture: B1 SELECTED

- **Status:** **accepted** by the owner on **2026-10-01**. **Architecture B1 is the selected NOMAD V1 lid/solar architecture.** It was pending from 2026-09-28 until then.
- **Scope:** this decision selects the *architecture*. It does **not** select every component. Each component keeps its own status (below and in `docs/v1-requirements.md`).
- **Selected architecture (B1):**
  - **Solar leaf:** one large solar leaf behind the display lid, hinged at the lid's top edge, covering the lid back.
  - **Leaf hinges:** two structural friction hinges. The current selected hinge candidate is **TorqMaster SB-188-SB-261-6**, subject to physical validation.
  - **Motion:** approximately **0–190°** usable leaf motion.
  - **Cable:** a dedicated cable sleeve near the leaf hinge axis, with an **R12 minimum cable bend-radius** concept.
  - **Panel:** **Voltaic P108** is the current solar-panel **candidate** (not selected).
  - **Stay:** the stay concept from Phase 2, two fold-out rear outrigger arms on the base. It is **mandatory** for B1's high leaf positions.
  - **Lid:** the B1 lid architecture: a thin lid core with the display, a vented air gap with low-e foil on the lid back, and the leaf.
- **Maturity:**
  - The current virtual geometry is mature enough to proceed with integrated Virtual V1 design (dependency order in `docs/v1-requirements.md` §18).
  - **Physical validation remains a future gate.** Nothing in B1 is physically tested.
- **Validated virtual results** (*modeled*: KERNEL / CALC from EST; not tested). These are design evidence, **not** product requirements:
  - **SB-261 rail** (`prototypes/B1_SB261/`, Onshape scratch):
    - **Motion:** leaf 0–190° with ≥ 2.03 mm to the lid, first contact at 201°. Block-to-band running gap 0.50.
    - **Cable:** all bends R 12.00. Twist zone 64 mm at 2.97°/mm. Hinge-to-cable separation ≥ 9.8.
    - **Insert walls:** 1.20–1.47 (the lid wall is below the insert vendor's 1.6 guidance; coupon required).
    - **Torque:** band -6 is 0.96–1.13 N·m per hinge (PUB) against ≈ 0.83 required (CALC), SF ≈ 1.16. Load, material and temperature ratings are unpublished.
  - **Phase 2** (`prototypes/P0.1/d010/d010_solar_architecture_phase2.md`):
    - mass 2.62 kg total (CALC from EST)
    - rear tip wind 11.4–18 m/s with the stay vs 2.4–8.3 without (CALC)
    - closed size 301 × 235 × 73.0 (CALC)
    - P108 9.5–10.9 W nameplate (VENDOR), 5.6–7.1 W real at best aim (CALC/ASSUMED)
    - display-hinge holding requirement about 1.6 N·m per hinge (CALC)
- **Explicitly not selected by D-010:**
  - display hinges (hardware TBD; D-006 direction still provisional)
  - display and controller SKU
  - battery, power electronics, cooling hardware, keyboard (all TBD)
  - the final panel (P108 candidate)
  - the stay design details
  - lid thickness and lid structure details
- **Consequences:**
  - **Architecture A is SUPERSEDED / DEFERRED FOR NOMAD V1.** A is the sliding/tilting cassette path: D-004, D-009, S1 / S1-R, F3, the Round B / B.1 / B.2 / D / D.1 lid-rail studies, the class-A lid and the Round E E2 lid.
    - Its records are preserved unchanged as engineering history and possible later reference.
    - Its open items (D-009 ±80° stops, the hub bracket below SF 2, the A cable crossing) are **no longer V1 blockers**.
  - `nomad.yaml` keeps the A parameters, marked superseded, so the existing study scripts and the Round E prototype still reproduce. B1 parameters are added with honest status. A full re-baseline is dependency step 7.
  - **The rear-port / lid-sweep conflict remains open** (B1 stack: +2.07 at φ 125, −2.3 mm at φ 135; CALC/KERNEL).
  - **D-007 is not accepted by this decision.**
- **Remaining gates (physical, later):**
  - the SB-261 coupon migration gate (`prototypes/B1_SB261/COUPON_SPEC.md` §7)
  - the Phase 2 §24 mock-ups: tipping/stay, thermal gap + foil, cable twist cycling, hinge torque, ASA frame warp, transport/latch, display-hinge pass
- **History:**
  - Study 2026-09-28: `prototypes/P0.1/d010_solar_architecture_comparison.md`.
  - **Study recommendation:** B1 (single top-hinged solar leaf on the lid back with a positive angle lock, vented air gap and a fold-out rear stay), gated by a one-day physical mock-up.
- **Phase 2** (2026-09-28, `prototypes/P0.1/d010/d010_solar_architecture_phase2.md`, tool `CAD/tools/d010_phase2_study.py`; Onshape concept Feature Studio `NOMAD_D010_Concepts`, isolated). It was pending the owner's decision until 2026-10-01.
  - **RECOMMEND B1, conditional** on the physical mock-ups.
  - **Why:** A's cable routing is not V1-acceptable:
    - an unresolved carriage-to-loop crossing through the structural rail wall;
    - a hub-link S-bend at 2.5–3.9 × *d* and a loop at 3.3 × *d*;
    - a right-hinge twist of 7.1°/mm.
    A also has the open hub bracket (below SF 2) and needs custom laminates.
  - **B1 as defined in Phase 2:**
    - a catalog P108 panel (9.5–10.9 W, VENDOR);
    - a vented gap of at least 6 mm plus low-e foil (a 4 mm gap barely ventilates);
    - an ASA leaf frame in two 256-bed halves;
    - 2 catalog friction hinges at about 0.8 N·m each;
    - a hollow cable knuckle;
    - a **mandatory** rear outrigger stay (tip wind 5.4–8.3 m/s without it, 11.4–18 m/s with it);
    - display hinges at about 1.6 N·m each.
  - **Corrections to Phase 1:** no visor while generating power; mass is equal (2.64 / 2.62 kg).
- **B1 hinge refinement after Phase 2** (2026-10-01, scratch; `prototypes/B1_SB261/`):
  - Phase 2's generic friction hinges (x ±55, axis z 69) and hollow cable knuckle were refined around the real TorqMaster SB-188-SB-261-6 IGES.
  - **Hinge positions:** centres at x ±115.
  - **Axis:** y 4.0, z 63.5, i.e. 2.5 above the lid back in the closed-lid frame.
  - **Cable:** a sleeve with a 64 mm twist zone at x 12–76.
  - The coupon is designed, not printed.
- **B was chosen (2026-10-01):** as this section anticipated, D-004's lateral-slide architecture and the D-009 wing mechanism are superseded for V1 and kept as analysis records.
- **Main tradeoffs:**
  - B: far fewer and simpler parts, better orientation, charges while closed; but a rearward CoG and wind sensitivity when deployed, lid-hinge torque, stowed heat (needs a gap), cells on the exterior.
  - A: protected cells and a neutral CoG; but high complexity and open D-009 problems.

## D-009 — Solar tilt index lock and hub-pin anti-rotation (Round E)

- **Status:** **SUPERSEDED / DEFERRED FOR NOMAD V1** on 2026-10-01 by D-010 (B1 selected).
  - D-009 was accepted by the owner on 2026-09-28 as part of Architecture A and implemented in the local digital prototype (pending physical validation).
  - It is kept unchanged below as an engineering record.
  - Its open items are no longer V1 work items.
- **Status as recorded on 2026-09-28** (history):
  - One part of it is unresolved: the **±80° structural hard stops are required but not packaged** (`SOLAR_TILT_STOP_ANGLE` open).
  - The persistent Onshape Feature Studio is not updated until the stops are decided.
- **Context:**
  - D-004 requires indexed positions with a positive lock, with the rotational load on a dedicated hub/pin.
  - The analyses behind this decision are in `prototypes/P0.1/`:
    - `round_e_solar_index_lock_investigation.md` (concept C1);
    - `round_e_solar_index_lock_manufacturing_check.md` (option D);
    - `round_e_solar_hub_pin_anti_rotation_check.md` (option C).
  - Implementation record: `round_e_solar_index_lock_implementation.md`.
- **Decision:**
  - **Positions:** 11 index positions, −75…+75° in 15° steps.
  - **Index pin and plate:**
    - A spring-loaded **Ø1.5 × 16 hardened dowel** (ISO 8734) in the cassette, in double shear. It runs in a stainless counter sleeve (2.5 × 1.6 × 4) and a printed guide.
    - It engages 11 reamed Ø1.60 holes on r 10 in a **1.5 mm stainless index plate** (301 ½-hard or 17-4PH; R 11.75).
    - The plate is keyed on a 3.0 A/F double-D at the hub-pin tip, with an M2 screw and washer.
  - **Hub pin:** Ø5 × 53.5, 303/304 cold-drawn. It is round through the carriage, link and bracket, with a 3.0 A/F double-D at each end.
  - **Anti-rotation and retention:**
    - A 1.5 mm stainless **anti-rotation plate** is captured in a carriage slot 10 mm inside the inboard face, reacted by a **Ø3 × 24 dowel**.
    - The plate and the inboard M2 screw also retain the pin axially.
  - **Operation:** a one-handed thumb slider with a 6 mm stroke. The spring only seats the pin. The cassette stows only at 0°.
  - **±80° hard stops:** required, structural (not spring, gear or friction).
- **Alternatives considered** (in the analysis records):
  - Ø2 index pin: 0.5 mm webs.
  - Laser-cut holes.
  - Roll-pin key.
  - Printed D-flat / set screw / printed double-D anti-rotation: each is below SF 2 at 1.26 N·m.
- **Tradeoffs:**
  - Four metal parts per side beyond the pin and dowel (two plates, sleeve, screws).
  - The plate holes need CNC drilling and reaming.
  - Small ligaments (0.95–1.3).
  - Hot PETG margins below 2 on the conservative dowel-bearing bound (1.18–1.49).
- **Open:**
  - The ±80° stops (options S1 outboard stop / S2 cable re-route / S3 interim waiver, implementation report §8).
    - S1 studied 2026-09-28 (`prototypes/P0.1/round_e_s1_hard_stop_study.md`): **FAIL, needs redesign**. The geometry works (±80.000°), but the stop reaction overloads the PETG hub-bracket bore and the pin root, and ±80° is not holdable with printed location.
    - Proposed S1-R (journaled stop yoke) studied 2026-09-28 (`prototypes/P0.1/round_e_s1r_stop_yoke_study.md`): **PASS, ready for owner review** (±80.000°; stop-path SF ≥ 2 at T_d; worst ±2.41° metal-referenced). Not approved for persistent Onshape.
    - S1-R does not fix the hub-bracket item below.
  - The approved lock's transverse reaction was omitted in the load checks. Reassessed 2026-09-28 (`prototypes/P0.1/round_e_d009_load_reassessment.md`):
    - The pin root is **unchanged** (SF 2.09; the S1 report's 1.75 was an error, now noted there).
    - The **PETG hub bracket** falls below its handling-basis SF 2: bearing 1.88, tear-out 1.73, peak tension 1.61.
    - It cannot be fixed without a geometry change. The minimum change is an outboard metal bearing for the cassette.
    - Owner decision needed.
  - The in-cassette cable exit route.
