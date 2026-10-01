# D-010 concept: wordmark rebuild failure: diagnosis and repair (2026-09-29)

> **D-010 DECIDED (2026-10-01): B1 SELECTED** by the owner as the NOMAD V1 lid/solar architecture. This study is part of the decision record and is kept unchanged; statements below such as "pending" or "nothing is chosen" describe the state when it was written. See `docs/decisions.md` D-010.

**Status: REPAIRED.** The isolated `NOMAD_D010_Concepts` Feature Studio compiles and the full gallery regenerates with the NOMAD wordmark on and off. It was written to Onshape, read back byte-identical, and the persisted file itself evaluated cleanly in scratch.
- **Not changed:** production CAD, `NOMAD_E_Prototype`, `nomad.yaml`, the Architecture A implementation, the B1 mechanics, and the wordmark's font, size and position.
- No Git commit or push.

Evidence labels: **KERNEL** = Onshape scratch evaluation (modelled); **CALC** = hand calculation from the model dimensions.

## 1. Root causes

| # | Cause | Kind | Effect |
|---|---|---|---|
| R1 | **`box` is a reserved word in FeatureScript** (the mutable `box` type). The wordmark code used it as a local name (`const box = ...`), as a map value (`"box" : box`) and in member access (`w.box`). | **Compile (parse) failure** | Parser error `mismatched input 'box' expecting ID` at 3 sites. The whole Feature Studio failed to load, so every instance of "NOMAD D010 Concepts" (all 12 gallery instances, every layout and state, A and B1) errored. The "Show NOMAD wordmark" toggle could not help. |
| R2 | **Letter counters filled (latent geometry defect, masked by R1).** `qSketchRegion(id + "sk")` returns *all* sketch regions of the text, including the counters inside O, A and D. KERNEL: 8 regions for "NOMAD" vs 5 glyph regions. Extruding all 8 fills the counters, so the recess and inlay would have been solid blobs for O, A and D. | **Text/sketch region selection** | It would not have failed the rebuild, but the letters would have been wrong. It contradicted the addendum's printability statement (counters attached to the recess floor). |

**No other failure classes were found.** The following were all checked and showed no problem:
- body creation, booleans (the lid stays one solid), the font (Michroma resolves)
- queries and references, part naming, transforms and placement
- gallery states, the Onshape kernel, the test harness

The pre-existing code (everything that is not the wordmark) regenerates exactly as before: same body count and same check values.

## 2. Exact repairs

All repairs are in `CAD/featurescript/NOMAD_D010_Concepts.fs` (the local source, now identical to Onshape):

| Where | Before | After |
|---|---|---|
| `d010Wordmark` | `const box = [...]` | `const rect = [...]` |
| `d010Wordmark` (part name, pad corners) | `box[0..3]` | `rect[0..3]` |
| `d010Wordmark` return | `{ ..., "box" : box }` | `{ ..., "rect" : rect }` |
| `d010BuildB1` | `var wmBox`, `wmBox = w.box`, foil window from `wmBox` | `var wmRect`, `wmRect = w.rect`, foil window from `wmRect` |
| `d010Wordmark`, both extrudes (cutting tool, inlay) | `qSketchRegion(id + "sk")` | `qSketchRegion(id + "sk", true)` (glyph regions only; counters open) |
| comment above `d010Wordmark` | — | documents both rules |

Geometry is unchanged, except that the counters are now open as intended:
- Text, font (Michroma fallback), 18 mm height, 139.1 mm width, 1.0 mm depth, yc 200 and the 0.2 mm inlay are all unchanged.
- The pad (1.0 mm, +2 mm margin) and the foil window (+3 mm margin) are unchanged.

No new features, no parameter changes, no YAML changes.

## 3. Why the previous implementation failed

- `box` is a keyword. A bare identifier named `box` does not parse, and neither does `.box`. The string `"box"` as a map key is legal (the generated `D010_BASE` table uses `"box"` strings safely).
- **Why the error reached Onshape:** `put_featurescript` returns no error on a file that does not parse (it returned `null`). The earlier "written and read back identical" check proved the transfer, not that the file compiles. The pre-write scratch test ran the wordmark as an inline snippet with different variable names, never the full file.
- **Why the counters went unnoticed:** the earlier check counted *bodies* (5 letters). A filled O is still one body, so the count could not tell.

**Process fix:** always run the full file through `test_feature` before any write, and run the persisted file itself after the write. Both rules are recorded in the FeatureScript notes.

## 4. Tests performed

| Test | Method | Payload |
|---|---|---|
| Reserved-word scan | local script over source and harness: declarations, member access, map values | — |
| Diff against the last known-good source | pre-wordmark Onshape copy (`onshape_before.fs`, 2026-09-28) vs the current source | — |
| T1: wordmark OFF, full gallery + D010 validation check | scratch `test_feature` | Full source including the UI feature (compiled, un-exported) + `NOMAD_D010_Concepts.test.fs` + new `NOMAD_D010_Concepts.gallery.test.fs` |
| T2/T3/T4: wordmark ON, full gallery (all 12 states) + geometry sanity | scratch `test_feature` | same, with the wordmark on |
| T5: persisted file | after the write: `get_featurescript`, byte compare, then the **unmodified persisted file** through `test_feature` (runs the real "NOMAD D010 Concepts" feature with its defaults: GALLERY, all display options on, wordmark ON) | the persisted file |

The gallery harness rebuilds the 12 instances exactly as the GALLERY layout does: same poses, offsets, labels and options (envelopes only in state 4, internals only in state 1). Each instance is wrapped so a failure in one state is reported, not hidden.

## 5. Results: wordmark OFF (KERNEL)

- **Gallery:** A 6/6, B1 6/6, **no failures.** Bodies: A 308, B1 237 = **545**, identical to the pre-wordmark baseline (2026-09-28).
- **Validation check (unchanged behaviour; it builds its B1 instances with the wordmark on):**

  | Check | KERNEL | Expected (python / Phase 2) |
  |---|---|---|
  | CG error | 4e-5 mm | < 1e-4 |
  | A lid to plug keep-out, φ 120 | 1.200 | 1.200 |
  | B1 stack to plug keep-out, φ 125 | 2.072 | 2.072 |
  | B1 leaf to lid core, ψ 45 | 1.141 | 1.141 |
  | A cassette / bracket to lid | 8 / 8 | 8.0 / 8.0 |
  | Stay to base | 0.5 | 0.5 |

## 6. Results: wordmark ON (KERNEL)

- **Gallery:** A 6/6, B1 6/6, **no failures.** Bodies: A 308, B1 273 = **581** = 545 + 6 × (5 letters + 1 pad).
- **Wordmark:** 5 letter bodies in each of the 6 B1 states; 139.1 × 19.5 mm.
- **Recess:** depth **1.00 mm**. Under the letters: 1.5 mm skin + 1.0 mm pad = **2.50 mm** (MIN_WALL 2.0).
- **No through-cut:** the lid volume is 302,720 mm³ with the wordmark off and 301,971 mm³ with it on. The difference, 749 mm³, equals glyph area × 1.0 mm (inlay volume 149.9 mm³ / 0.2 mm = 749.5 mm²), so exactly the recess is removed.
- **Lid:** 1 body in every state (the recess does not split it).
- **Backing pad:** present in all 6 states; 1.0 mm from the display controller.
- **Foil window:** present in all 6 states. The foil has 10 faces (a box with a rectangular through-window).
- **Counters:** 8 sketch regions vs 5 glyph regions confirms R2; the repaired code extrudes only the 5.

## 7. Gallery-state results and geometry sanity (KERNEL, minimum over all 6 B1 states)

Minimum distance from the wordmark + backing pad to each part group:

| Other part | Min distance (mm) | Verdict |
|---|---|---|
| Leaf friction hinges (barrels + plates) | 164.05 | clear |
| Display hinge axis | 26.69 | clear |
| Stay (arms, pivots, pads) | 72.11 | clear |
| Leaf knuckle / idler | 179.53 | clear |
| Leaf (frames, PV, splice, latch, connector) | 6.8 | clear |
| Display controller | 1.0 | as designed |
| **B1 cable (lid run)** | **0.19** | **no intersection, but near-contact (pad only; see §9)** |
| Anything else (foil, gap, envelopes, CG markers, keep-outs) | 0.19 (nearest = the B1 cable) | no intersection |

- **State failures:** none. No missing or duplicate bodies, no transform failures.
- **Leaf deployment:** the leaf builds and poses in all 6 states (ψ 0 / 0 / 30 / 65 / 190 / 110). Leaf-to-core at ψ 45 is unchanged at 1.141.
- **Clearances unchanged:** stay-to-base and all plug keep-out clearances match the pre-wordmark values.

## 8. Onshape validation result

1. **Before the write:** `get_featurescript` of `NOMAD_D010_Concepts` was byte-identical to the local pre-repair file (53,410 characters), so nobody had edited it in Onshape in the meantime.
2. **Write:** `put_featurescript` of the repaired local file, 53,687 characters. Only this isolated Feature Studio was written.
3. **Read-back:** **byte-identical** to `CAD/featurescript/NOMAD_D010_Concepts.fs` (line endings normalised; the reserved-word scan of the read-back is clean).
4. **Persisted file evaluated as-is** (T5): "Feature 'nomadD010Concepts' evaluated successfully", **0 notices** (no errors, no warnings). This is the real feature with its defaults: GALLERY with the wordmark on.

**Owner action:** in the Part Studio holding the "NOMAD D010 Concepts" feature, the errors should clear on the next regeneration. If the feature was inserted before this fix, open and close its dialog or pick the latest Feature Studio version, if Onshape asks.

## 9. Remaining known limitations

1. **Backing pad vs B1 lid cable run: 0.19 mm clearance (KERNEL; no intersection).**
   - **Where:** under the "D" end of the wordmark. The B1 lid cable (Ø4, route point (−60, 194.5, 53) → (−75, 215, 56)) rises toward the hinge and passes 0.19 mm under the pad's corner (CALC: pad bottom z 57.5, cable top ≈ 57.3 near x −71.5, y 210). The letters themselves are 3.2 mm from the cable.
   - This is below any practical cable clearance.
   - **Not changed:** a fix needs either a cable-route change or a wordmark/pad change, and you have frozen both. Options for your decision:
     - (a) Move the lid-run rise point from x −60 to about x −78, so the cable climbs outside the pad. Cable routing change, smallest.
     - (b) Lower that segment by about 1.5 mm. Cable routing change.
     - (c) Relieve the pad's corner. This leaves 1.5 mm of skin under part of the "D", below MIN_WALL 2.0, so it is not recommended.
     - (d) Move the wordmark (yc), which is a position change.
2. **Font:** Michroma remains a **fallback** for Eurostile Extended (not available in Onshape); this is not the final identity.
3. **Concept only:** the wordmark, pad and foil window are visual-concept geometry, not in `nomad.yaml`. Thermal impact of the foil window (about 5 % of the foil area) is estimated, not measured.
4. **Kernel checks are modelled.** Recess printability, legibility and pad function are **not physically tested.**
5. **Test-harness scope:** the gallery harness reports through a truncated regenError (about 330 characters). Test T5 confirms the real feature regenerates, but it reports no geometry figures itself; those come from T1 to T4.

## Files

| File | Change |
|---|---|
| `CAD/featurescript/NOMAD_D010_Concepts.fs` | repaired (R1 rename, R2 region filter, comment); identical to Onshape |
| `CAD/featurescript/NOMAD_D010_Concepts.test.fs` | `d010Check` body moved to `d010CheckMsg()` (reusable); added pad/inlay-to-cable distances. Never written to Onshape. |
| `CAD/featurescript/NOMAD_D010_Concepts.gallery.test.fs` | **new** gallery regression harness (wordmark ON/OFF sweep + sanity). Never written to Onshape. |
| `prototypes/P0.1/d010/d010_solar_architecture_phase2.md` | erratum on the wordmark addendum |
| `docs/build-log.md` | entry for this repair |

## Onshape API

38 calls for the repair: 3 × `test_feature`, 2 × `get_featurescript`, 1 × `put_featurescript`, notes, usage. Total 239 → 277 of 2,500 (11.1 %).

The diagnosis before the repair used 10 calls (229 → 239).

## 10. Follow-up (2026-09-29): cable route option (a), approved

**Change:** one point on the B1 cable route was moved: the lid-run point where the cable starts to rise toward the display hinge, from **x −60 to x −78** (y 194.5, z 53). It was changed in `CAD/tools/d010_phase2_study.py` (`b1_route`) and regenerated with `--emit`. The only line that changed in `NOMAD_D010_Concepts.fs` is that route point.
- **Unchanged:** the wordmark, backing pad, foil window, B1 mechanics, A, YAML and production.
- The harness expectations regenerated identical, since CG and gaps do not depend on the route.

**Results (KERNEL unless marked)**

| Check | Result |
|---|---|
| Gallery, wordmark OFF | A 6/6, B1 6/6, no failures, 545 bodies (unchanged) |
| Gallery, wordmark ON | A 6/6, B1 6/6, no failures, 581 bodies (unchanged) |
| D010 validation check | CG 4e-5; plugA120 1.200; plugB125 2.072; leafCore45 1.141; cassette/bracket 8 / 8; stay–base 0.5 (all unchanged) |
| **Min cable to wordmark pad** | **2.35 mm** (was 0.19), over all 6 B1 states |
| Min cable to the letters themselves | 4.97 mm (was 3.2) |
| Wordmark unchanged | 5 letters × 6 states; 139.1 × 19.5 mm; recess 1.00 mm; 2.50 mm under the letters; inlay 149.9 mm³; lid volume 301,971 mm³ with the wordmark on; foil window in all 6 states. All identical to before. |
| Other clearances from the wordmark + pad | leaf hinges 164.05, display hinge 26.69, stay 72.11, knuckles 179.53, leaf 6.8, controller 1.0 (unchanged). The nearest part overall is now the controller (1.0 mm, by design), not the cable. |
| Cable to stay | 12.77 mm, clear |
| Saved file, run as-is | "evaluated successfully", 0 notices (GALLERY, wordmark on) |
| Read-back | byte-identical to the local source (53,687 characters) |

**Findings from the new checks (not caused by this change; not fixed):**
1. **The cable touches the leaf hinge and the leaf frame (0.00 mm) in the concept model.**
   - Contact points in the stowed frame: **(66, 8, 69)**, where the cable's twist segment on the leaf axis runs into the right friction-hinge barrel (x 40–70); and **(139, 18, 61)**, where the lid-side descent from the knuckle, (141, 4, 69) → (141, 32, 53), passes through the right leaf-frame edge.
   - Both are on route anchors 3–5, about 175 mm from the moved point and outside every segment it affects. So they come from the original Phase 2 route, which Phase 2 never checked.
   - They need either a hinge/cable pass-through or a route change near the knuckle. This is a cable-routing / B1 decision for the owner.
2. **Bend radius at the new corner (CALC and in the model):** the rise from (−78, 194.5, 53) to (−75, 215, 56) turns more than 90°. The drawn fillet is therefore limited to **R 9.1 mm** (about 2.3 × d) instead of the R 12 target, which was 11.9 before.
   - Any rise point at or beyond about x −72 has this limit, because the next anchor (−75, 215, 56) is fixed.
   - Cable length 852 → 861 mm (CALC, python study). The Phase 2 report's "0.85 m" is now about 0.86 m. That report was not edited.

**Onshape API:** 32 calls for this step (277 → 309 of 2,500): 3 × `test_feature`, 2 × `get_featurescript`, 1 × `put_featurescript`, usage checks.

## 11. B1 cable routing correction pass (2026-09-29): bend radius fixed; leaf-end contacts NOT fixable by routing

Owner instruction: restore bend radius ≥ 12 mm with the rise point kept at x −78, then eliminate the two 0.00 mm leaf-end cable contacts by a local reroute, and STOP if that needs structural redesign. Only the isolated `NOMAD_D010_Concepts` was changed (written and read back). Nothing else was changed: wordmark, pad, foil window, B1 mechanics, Architecture A, YAML and production. No commit or push.

### 11.1 Route changes (source: `b1_route()` in `CAD/tools/d010_phase2_study.py`, regenerated with `--emit`)

| Point | Before | After | Reason |
|---|---|---|---|
| lid run, east end | (141, 194.5, 53) | (141, **193.5**, 53) | cable to controller was 0.6 mm; y run shifted 1 mm toward the display (target ≥ 1.0) |
| lid run, rise point | (−78, 194.5, 53) | (−78, **193.5**, 53) | same y shift; the x = −78 rise point is kept |
| next point | (−75, 215, 56) | (**−82**, 215, 56) | minimal move that restores R 12 at the rise (the 98° turn needs 13.8 mm of tangent, but each fillet is limited to half of its adjacent segment) |
| base riser | (5, 226, 16) | (5, **227**, 16) | the corner at (5, 205, 8.5) was R 11.9 (pre-existing, not from the x −78 change); a 1 mm longer riser gives R 12.0 |

All other points are unchanged.

### 11.2 Results (KERNEL unless marked)

| Quantity | Before this pass | After |
|---|---|---|
| Smallest drawn bend radius | 9.1 mm (11.9 elsewhere) | **12 mm** at every bend |
| Cable length (CALC, study and model agree) | 861 mm | **867 mm** (+6) |
| Cable to wordmark pad | 2.35 mm | **2.42 mm** (to the letters: 5.0) |
| Cable to controller | 0.6 mm | **1.6 mm** |
| Cable to display envelope (CALC) | 3.4 mm | 3.1 mm |
| Cable to stay | 12.77 mm | 12.77 mm |
| Gallery, wordmark ON | 12/12, 581 bodies | 12/12, **581** bodies, no failures |
| Gallery, wordmark OFF | 12/12, 545 bodies | 12/12, **545** bodies, no failures |
| D010 validation check | matches | unchanged (CG 4e-5; plugs 1.200 / 2.072; leaf-core 1.141; cassette / bracket 8 / 8; stay–base 0.5) |
| Wordmark | 139.1 × 19.5, recess 1.00, 2.50 under, inlay 149.9 mm³, lid 301,971 mm³ | identical |
| Saved file, run as-is | 0 notices | **evaluated successfully, 0 notices** |
| Read-back | byte-identical | **byte-identical** (53,687 characters) |

### 11.3 The two contacts: exact bodies, cause, and why no local reroute exists

**Contact 1, (66, 8, 69).** The leaf-side segment (52, 14, 64) → (72, 4, 69) runs through several bodies, all at 0.00 mm (penetration):
- the right friction-hinge **barrel** (x 40–70, Ø8 on the leaf axis): this is the reported point.
- the right friction-hinge **leaf plate** (x 43–67, y 0.5–24, z 62–64.5): about (49, 12, 65).
- the **PV panel** front-bottom edge (y 6, z 67): about (65, 10, 67).
- the in-line **panel connector** (x 30–46, y 10–18, z 61.5–66.5): about (46, 15, 66). This is the cable's own connector, so contact there is by design.
- The connector and the hinge plate also overlap each other by 3 mm (x 43–46). That is an existing envelope conflict, separate from the cable.

**Contact 2, (139, 18, 61).** The lid-side descent (141, 4, 69) → (141, 32, 53) runs inside the **right leaf-frame side wall** (x 137–144.5, solid for y ≥ 9.5, full height z 61–73). It enters at the relief back face y = 9.5 and leaves through the wall underside z = 61 near y = 18. It then crosses the **lid back skin** (z 58.5–61) and the foil at the same place; a skin and foil pass-through is needed by any route, and it is not modelled.

**Why a local reroute cannot remove them (CALC with a numeric model that reproduces the kernel, plus a grid reachability search):**
- Around the knuckle axis (y 4, z 69) a Ø4 cable is boxed in. The only opening toward the free pocket is the gap between the frame front-bar corner (y 5.5, z 64) and the panel front-bottom corner (y 6, z 67), which is **3.04 mm wide**. A tube of radius 2.0 or 1.9 cannot pass it; radius 1.5 can.
- The way round the outside is 3.5 mm wide (frame outer edge x 144.5, lid inner wall x 148), also less than Ø4.
- The gap between the hinge leaf plate (top z 64.5) and the barrel (bottom z 65) is 0.5 mm.
- Along the knuckle the cable is tangent to the panel front face (axis y 4, cable r 2, panel y 6): 0.00 mm even with no penetration. This holds for the whole twist zone, x 72 to 136.5.

Reaching cable-to-leaf and cable-to-hinge ≥ 1.0 mm therefore needs a structural change (frame, panel edge, hinge or connector geometry, or the cable diameter), which was excluded, so **I stopped there**. The routing edits in 11.1 are limited to what is achievable without touching those parts.

### 11.4 Remaining below target (not fixed)

| Item | Now | Target | Note |
|---|---|---|---|
| Cable to friction hinge (barrel and plate) | 0.00 (penetrates) | ≥ 1.0 | structural, see 11.3 |
| Cable to leaf frame and PV panel | 0.00 (penetrates; twist zone tangent) | ≥ 1.0 | structural |
| Cable to foil (leaf-side run at z 64) | 0.7 | ≥ 1.0 | the 5.7 mm gap between foil and panel leaves at most 0.85 mm each side for a Ø4 cable |
| Lid skin / foil crossing near (139, 18, 61) | pass-through unmodelled | none | needed by any route |

### 11.5 Options for the owner (none applied)

1. Cut a cable notch through the frame side wall / front bar and the panel edge strip (structural, needs approval), plus a grommet in the lid skin and foil.
2. Move the twist axis or the panel front edge so the cable has ≥ 1.0 mm to the panel face (for example a panel edge at y ≥ 7). A 3 mm cable passes the 3.04 mm gap but still has zero clearance.
3. Re-plan the knuckle so the cable enters from the leaf side through the hinge (hinge pair moved along the axis, or a hollow hinge barrel).

### 11.6 Files and API

- `CAD/tools/d010_phase2_study.py`: route edits (the local file is now ahead of Phase 2 on the route).
- `CAD/featurescript/NOMAD_D010_Concepts.fs`: regenerated data block, identical to Onshape.
- `CAD/featurescript/NOMAD_D010_Concepts.gallery.test.fs`: cable to controller added.
- `CAD/featurescript/NOMAD_D010_Concepts.cable.test.fs`: **new** scratch cable clearance diagnostic (never written to Onshape).
- `CAD/tools/d010_cable_analysis/` (`cabmath.py`, `cabmodel.py`, `reach.py`): numeric model and reachability search. The model reproduces the kernel: controller 0.6 → 1.6, foil 0.7, pad 2.36 vs 2.35, and all penetrations.
- **Onshape API:** 70 calls (309 → 379 of 2,500, 15.2 %): 7 × `test_feature` (4 diagnostics, ON, OFF, saved file), 3 × `get_featurescript`, 1 × `put_featurescript`, usage checks.
