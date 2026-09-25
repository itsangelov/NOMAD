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

- **Status:** accepted (2026-09-25) as the P0.1 solar kinematic architecture
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

## D-005 — Default branch `main`

- **Status:** accepted (Phase 0 approval, 2026-09-25)
- **Decision:** The unborn `master` branch was renamed to `main` before the first commit. There was no history to lose.
