# CAD

**Onshape is the master parametric model.** Nothing in this folder replaces it.

**Active architecture: B1 (D-010, accepted 2026-10-01).** **Virtual V1 integration (2026-10-06):** `tools/v1_integration.py` is the integrated V1 envelope model and its checks (`docs/V1-VIRTUAL-INTEGRATION.md`).
- **V1 visual master (2026-10-08):** the Feature Studio `NOMAD_V1_Visual` (below) holds the whole V1, including B1 on the SB-261 geometry, as an inspection model (not production CAD). It is kernel-checked and persisted, and the owner has inserted it into the Part Studio `NOMAD V1 — Digital Prototype`. It regenerates there with one open build warning, the base edge-chamfer cut (`docs/V1-VISUAL-MODEL.md`).
- The SB-261 hinge-rail validation model stays in the connector's scratch document (`prototypes/B1_SB261/SOURCES.md`).
- **Architecture A, superseded / deferred for V1:** the Architecture A geometry (the Round E E2 lid "NOMAD E Lid" in `NOMAD_E_Prototype`, the P0.1 rail and lid coupons, the `solar` YAML group) is kept as history.
- The B1 YAML groups (`lid_b1`, `solar_leaf`) are emitted into the generated parameter blocks of `NOMAD_P01.fs` and `NOMAD_E_Prototype.fs` as constants only. No feature uses them, and this was **not** written to Onshape.

| Folder | Contents |
|---|---|
| `parameters/` | `nomad.yaml`: the authoritative machine-readable **Virtual V1** parameters (D-002), checked by `py tools/yaml_to_featurescript.py --validate-v1` and used by `tools/v1_integration.py`. `history/nomad_P0.1_2026-10-02.yaml`: the **frozen** P0.1 / Round C / Round E / Architecture A set. The P0.1 FeatureScript files and P0.1 study scripts read it, so they reproduce unchanged. Never edit it. |
| `featurescript/` | `NOMAD_P01.fs`: the P0.1 FeatureScript source (D-001), whose parameter block is generated from `nomad.yaml`. Once a Feature Studio exists in Onshape, this is its snapshot, and Onshape is correct for everything outside the generated parameter block. `NOMAD_P01.test.fs` is the scratch test harness and is never written to Onshape. |
| `coupons/P0.1/` | P0.1 physical test coupons (test articles, not lid parts; Architecture A rail / class-A lid basis, superseded / deferred for V1 by D-010). The CAD master is the Onshape Feature Studio `NOMAD_P01_Coupons` (snapshot `featurescript/NOMAD_P01_Coupons.fs`, harness `NOMAD_P01_Coupons.test.fs`). `generate_coupons.py` is the local reference → `stl/` (print-ready) + `scad/`; `onshape_crosscheck.py` gives the expected Onshape sizes and volumes. |
| `tools/` | `yaml_to_featurescript.py` (YAML → FeatureScript parameter block, with `--check`); `build_test_payload.py` (assembles the single-feature test payload); `fs_compact.py` (strips comments / blank lines / insignificant whitespace for the Onshape copy and test payloads); `v1_visual_emit.py` (V1 visual model data block); `base_v01_layout.py` (Round C base V0.1 layout spec + checks; generates the base layout block in `NOMAD_P01.fs` and the harness data in `NOMAD_P01.basev01.test.fs`, with `--write` / `--check`). |
| `exports/` | Derived STEP / STL / 3MF files. Name them `<revision>_<part>.<ext>`, e.g. `P0.1_solar_rail.stl`. |
| `drawings/` | Derived drawings and dimensioned sketches. |

## Onshape master document

- **Document:** [NOMAD](https://cad.onshape.com/documents/b68b7c7b3b6b91fea1499e64/w/3882cd432de0cc985fb945f0/e/b6874d7cc6ee3b749fbaf2ce)
- Document ID: `b68b7c7b3b6b91fea1499e64`
- Main workspace ID: `3882cd432de0cc985fb945f0`
- Initial element ID: `b6874d7cc6ee3b749fbaf2ce`
- Feature Studio `NOMAD_P01_Coupons`: element ID `2e9a95c6ec40fe948348a500` (P0.1 coupons; custom feature "P0.1 Coupons")
- Part Studio `P0.1 Coupons`: created by the owner; contains the inserted "P0.1 Coupons" feature (13 `CPN_*` parts)
- Feature Studio `NOMAD_D010_Concepts`: element ID `d4619014058afc59574f42aa` (D-010 Phase 2 **experimental** solar concepts A and B1 on one shared base reference; custom feature "NOMAD D010 Concepts").
  - **Isolated:** it imports nothing from production and nothing references it. **Not production CAD.**
  - Snapshot `featurescript/NOMAD_D010_Concepts.fs` is the text written to Onshape. Its data block is regenerated with `py CAD/tools/d010_phase2_study.py --emit`, which also writes the expectations in the scratch harness `NOMAD_D010_Concepts.test.fs` (never written).
  - The owner inserts the feature into a Part Studio (for example "D-010 Concepts").
- Feature Studio `NOMAD_V1_Visual`: element ID `041ff69ce1d94a2b7f74d123` (2026-10-08; V1 visual master, custom feature "NOMAD V1 Visual"; **inspection model, not production CAD**).
  - The text in Onshape is `featurescript/NOMAD_V1_Visual.onshape.fs`, byte-identical (read back 2026-10-08). It is built from the readable source `featurescript/NOMAD_V1_Visual.fs` with `py CAD/tools/fs_compact.py`.
  - The data block comes from `py CAD/tools/v1_visual_emit.py --write`.
  - Kernel QA harness: `featurescript/NOMAD_V1_Visual.qa.test.fs` (never written).
  - The owner inserts the feature into a Part Studio "NOMAD V1".
- Feature Studio `NOMAD_E_Prototype`: element ID `40d4ae5868441bcb8882fe3a` (Round E digital prototype, D-008; features "NOMAD E Base", "NOMAD E Service" (E1) and "NOMAD E Lid" (E2)). Snapshot: `featurescript/NOMAD_E_Prototype.fs` (exact text written to Onshape, **except** that since 2026-09-28 it holds the locally validated D-009 index-lock candidate, which is not yet written; Onshape still has the post-F3 version, see `prototypes/P0.1/round_e_solar_index_lock_implementation.md` §15); scratch harnesses `NOMAD_E_Prototype.test.fs` (E1) and `NOMAD_E_Prototype.e2.test.fs` (E2), never written. Generated blocks: `py CAD/tools/yaml_to_featurescript.py --target NOMAD_E_Prototype.fs`, `py CAD/tools/base_v01_layout.py --write --target NOMAD_E_Prototype.fs --harness NOMAD_E_Prototype.test.fs` and `py CAD/tools/e_lid_layout.py --write` (lid block + E2 harness data; `--check` to verify). E2 scratch payload: `py CAD/tools/build_test_payload.py OUT NOMAD_E_Prototype.e2.test.fs NOMAD_E_Prototype.fs`. The Part Studio `NOMAD E — Digital Prototype` and the Assembly are created by the owner.
