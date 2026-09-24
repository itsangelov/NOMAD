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
