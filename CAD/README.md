# CAD

**Onshape is the master parametric model.** Nothing in this folder replaces it.

| Folder | Contents |
|---|---|
| `parameters/` | `nomad.yaml`: the authoritative machine-readable mechanical parameters (D-002). FeatureScript values are derived from it. |
| `featurescript/` | `NOMAD_P01.fs`: the P0.1 FeatureScript source (D-001), whose parameter block is generated from `nomad.yaml`. Once a Feature Studio exists in Onshape, this is its snapshot, and Onshape is correct for everything outside the generated parameter block. `NOMAD_P01.test.fs` is the scratch test harness and is never written to Onshape. |
| `coupons/P0.1/` | P0.1 physical test coupons (test articles, not lid parts). The CAD master is the Onshape Feature Studio `NOMAD_P01_Coupons` (snapshot `featurescript/NOMAD_P01_Coupons.fs`, harness `NOMAD_P01_Coupons.test.fs`). `generate_coupons.py` is the local reference → `stl/` (print-ready) + `scad/`; `onshape_crosscheck.py` gives the expected Onshape sizes and volumes. |
| `tools/` | `yaml_to_featurescript.py` (YAML → FeatureScript parameter block, with `--check`); `build_test_payload.py` (assembles the single-feature test payload). |
| `exports/` | Derived STEP / STL / 3MF files. Name them `<revision>_<part>.<ext>`, e.g. `P0.1_solar_rail.stl`. |
| `drawings/` | Derived drawings and dimensioned sketches. |

## Onshape master document

- **Document:** [NOMAD](https://cad.onshape.com/documents/b68b7c7b3b6b91fea1499e64/w/3882cd432de0cc985fb945f0/e/b6874d7cc6ee3b749fbaf2ce)
- Document ID: `b68b7c7b3b6b91fea1499e64`
- Main workspace ID: `3882cd432de0cc985fb945f0`
- Initial element ID: `b6874d7cc6ee3b749fbaf2ce`
- Feature Studio `NOMAD_P01_Coupons`: element ID `2e9a95c6ec40fe948348a500` (P0.1 coupons; custom feature "P0.1 Coupons")
- Part Studio `P0.1 Coupons`: created by the owner; contains the inserted "P0.1 Coupons" feature (13 `CPN_*` parts)
