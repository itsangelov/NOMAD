# B1 SB-261: sources

## Vendor CAD (not committed)

The TorqMaster IGES assembly is a third-party file and this repository has a public remote, so the file is **kept outside Git** and recorded here by hash.

| Field | Value |
|---|---|
| Archive URL | https://torqmaster.com/wp-content/uploads/2020/09/TORQMASTER-HINGE-ASSEMBLY-3D-IGES-SB-188-SB-261.zip |
| Archive, as saved | `SB-188-SB-261.zip`, 52,003 bytes, SHA-256 `bb349bcb8f933c96b1408f4fa55bc8d20afdc04a8caa85356ff1a5999a1cb1bc` |
| IGES file | `TORQMASTER-HINGE-ASSEMBLY-SB-188-SB-261-REV-A.igs`, 437,470 bytes, SHA-256 `73009532bf4fb540a5ccae6ce8f23771ee520053084fcf3583dcfe3ffbbe4e77` |
| Revision / date / units | REV A, 2018-10-16, inch |

**To reproduce:**
1. Download the archive and check the SHA-256.
2. Put the `.igs` next to `src/iges/iges_read.py`.
3. Use `load()`, `solid_instances()`, `solid_faces()` and `solid_vertices()`.

**Published data:** the SB-188 Type-2 drawing and product data (torque bands, balance, life) were read from torqmaster.com during the hardware research ([reports/01](reports/01_hardware_second_pass_2026-10-01.md)). The exact page URLs were not recorded in the session reports, so none are given here.

## Inserts

| Insert | Source | Data |
|---|---|---|
| Ruthex RX-M3x5.7 | https://www.ruthex.de/en/products/ruthex-gewindeeinsatz-m3-100-stuck-rx-m3x5-7-messing-gewindebuchsen | D1 4.6, hole 4.0, L 5.7, minimum wall 1.6 (vendor) |
| PartsBuilt PBX-TI-M25-4L35W-4PK | https://partsbuilt.com/m2-5-heat-set-thread-insert-4mm-long-4-pack/ | M2.5 × 4, OD 3.55, hole 3.10 |

## Onshape scratch models (outside Git; not the NOMAD document)

All three are branches of the Onshape connector's own placeholder document `a3313eb551a601b46ae8de86`, Part Studio element `7c60e1e6eabeb79b9514eabf`. The NOMAD document (`b68b7c7b3b6b91fea1499e64`) was not touched.

| Workspace | Feature | State |
|---|---|---|
| `cbaa5a0d171df874fa4f6dd3` | `B1HingeValidation` (ψ, φ, surroundings, check) | Current, revised B1 rail |
| `f8c158e60c71fe8f2e9aaffe` | `B1HingeValidation`, pre-revision | Superseded (kept; not deleted) |
| `07eafe33cb44fd16843cea57` | `B1HingeCoupon` | Current coupon |

**Links:**
- [B1HingeValidation](https://cad.onshape.com/documents/a3313eb551a601b46ae8de86/w/cbaa5a0d171df874fa4f6dd3/e/7c60e1e6eabeb79b9514eabf)
- [B1HingeCoupon](https://cad.onshape.com/documents/a3313eb551a601b46ae8de86/w/07eafe33cb44fd16843cea57/e/7c60e1e6eabeb79b9514eabf)

**If those workspaces are lost:** the code in `src/fs/` rebuilds both features.
- `b1_common.fs` + `prod.fs` rebuild `B1HingeValidation`.
- `coupon_common.fs` + `coupon_prod.fs` rebuild `B1HingeCoupon`.

**Onshape API use** for the SB-261 stages: 382 → 516 of 2,500 (3D validation 382 → 468; coupon 468 → 516). Total after the 2026-10-01 audit: 517.

## Inputs from this repository (read-only)

- `CAD/tools/d010_phase2_study.py`: the closed-lid frame, the B1 stack and the torque requirement. It was imported read-only by the 2D section models.
- `prototypes/P0.1/d010/d010_solar_architecture_phase2.md`: the D-010 Phase 2 study.
