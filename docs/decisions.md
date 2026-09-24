# Engineering Decisions

Status values: **proposed** (awaiting the project owner), **accepted**, **superseded**, **rejected**.

For each decision, record: context, the decision, alternatives, the tradeoff, and status.

---

## D-001 — FeatureScript-driven CAD for P0.1

- **Status:** proposed
- **Context:** The only Onshape integration available is a FeatureScript-only MCP. It cannot create documents, Part Studios, Variable Studios or Assemblies, and it cannot insert features into a user Part Studio.
- **Proposal:** Build P0.1 as custom features in a `NOMAD_P01` Feature Studio: master parameters, layout skeleton, envelopes, solar mechanism and a clearance check. The project owner inserts the features into a single multi-part Part Studio. Motion states (slide extension, rotation angle, lid angle) are parameters, and the clearance check evaluates them.
- **Alternatives:** The project owner models natively in Onshape, with Claude writing specs only.
- **Tradeoff:** The model is fully parametric, reproducible and diffable in Git, and Claude can run clearance checks in a scratch context. The costs: the geometry is less convenient for later hand modeling, it spends API allocation, and "motion" is geometric only (modeled, not tested).

## D-002 — Location of the master parameter table

- **Status:** proposed
- **Proposal:** The parameters live as constants in the Feature Studio and are published as Part Studio `#variables`. The copy in `CAD/featurescript/` is a snapshot. `docs/mechanical-spec.md` records the status and source of each parameter.
- **Alternative:** An Onshape Variable Studio, which would have to be entered by hand because the MCP cannot write it.

## D-003 — Trackpad position

- **Status:** open (approval required)
- **Proposal:** Trackpad centred below the keyboard, with the position kept as a parameter.
- **Reason:** Placing the trackpad beside a ~280 mm keyboard makes the base about 380 mm wide, which is much wider than a 10.1" display lid.

## D-004 — Solar cassette rotation axis

- **Status:** open (approval required)
- **Proposal:** Each cassette tilts about its own lateral slide axis, with the hub at the inboard carriage, over approximately ±60° to ±75°.

## D-005 — Default branch `main`

- **Status:** accepted (Phase 0 approval, 2026-09-25)
- **Decision:** The unborn `master` branch was renamed to `main` before the first commit. There was no history to lose.
