# B1 solar-leaf hinge: TorqMaster SB-188-SB-261-6 (engineering record)

> **PHYSICAL VALIDATION REQUIRED.** Nothing in this folder has been printed, assembled, measured or physically tested. No hinge has been purchased. The hinge is **not** physically validated. Every result below is *IGES* (measured from the vendor's file), *kernel* (measured in an Onshape scratch model), *CALC* (analytic) or *PUB* (vendor-published). See [VALIDATION_STATUS.md](VALIDATION_STATUS.md).

> **DECISION UPDATE (2026-10-01): D-010 ACCEPTED, B1 SELECTED.**
> - The owner locked **B1** as the NOMAD V1 lid/solar architecture (`docs/decisions.md` D-010).
> - **SB-188-SB-261-6** is the current selected leaf-hinge **candidate**, subject to physical validation. It is not a validated or purchased part.
> - **D-007** is still **not** accepted (proposed).
> - The B1 working parameters from this record are in `CAD/parameters/nomad.yaml` (`solar_leaf`, `lid_b1`; TBD with working inputs). V1 requirements: `docs/v1-requirements.md` §8.
>
> *History:* this record was written earlier the same day as **exploratory, pre-decision work**, while D-010 was pending. The body below keeps that wording where it describes what was known then.

Recorded 2026-10-01 as part of a Git checkpoint. The original session reports are archived verbatim in [reports/](reports/).

## 1. What was done (2026-10-01, all in scratch)

| Step | Result | Evidence | Report |
|---|---|---|---|
| Hardware research, second pass (TorqMaster small families) | SB-188-SB-261, torque band -6, shortlisted for B1 | PUB / INF / CALC | [01](reports/01_hardware_second_pass_2026-10-01.md) |
| 2D section concept around the published drawing | Fits geometrically. **Partly superseded** by the IGES (see §3) | modeled (2D) / CALC | [02](reports/02_scratch_2d_concept_2026-10-01.md) |
| IGES download and inspection | Real geometry measured. The drawing reading was corrected | IGES | [03](reports/03_scratch_3d_validation_2026-10-01.md) §A |
| 3D Onshape scratch model `B1HingeValidation` | "Geometrically validated enough to proceed" (scratch only) | kernel / CALC | [03](reports/03_scratch_3d_validation_2026-10-01.md) |
| Physical test coupon `B1HingeCoupon` | Designed and kernel-checked. **Not printed or tested** | kernel / CALC | [04](reports/04_coupon_final_report_2026-10-01.md), [COUPON_SPEC.md](COUPON_SPEC.md) |
| Virtual V1 audit (context; not specific to SB-261) | Status audit, delivered as text | review | [05](reports/05_virtual_v1_audit_2026-10-01.md) |

## 2. IGES inspection (evidence: IGES)

Source: `TORQMASTER-HINGE-ASSEMBLY-SB-188-SB-261-REV-A.igs`, REV A, dated 2018-10-16, units inch. The file is **not** committed (vendor file, public remote); see [SOURCES.md](SOURCES.md) for the URL and SHA-256. Parser: [src/iges/iges_read.py](src/iges/iges_read.py) (standard library IGES 5.3 B-rep reader).

**Assembly:** 7 solids. One geometry covers every torque band.
- 4 identical bands "BAND 392 B 003". Each is a 300° wrap around the shaft plus a flag.
- 1 shaft "SHAFT H028P 521".
- 2 C-rings "IRRC 2000-18".

| Item | Drawing | IGES |
|---|---|---|
| Barrel (band wrap) OD | R .14 → Ø7.112 | **Ø7.048** |
| Overall length | 1.33 → 33.78 | 33.782 |
| Shaft | not given | Ø4.762 × 33.782, unkeyed, chamfered ends; C-ring grooves Ø4.19 at the centre only |
| Shaft-end protrusion | .06 → 1.52 | **1.404** each end |
| Flag width | .28 → 7.11 | 7.140 |
| Flag reach / thickness | .50 / .045 | 12.700 / 1.143 |
| Flag hole | Ø.138 at .31 (7.874) | Ø3.506 at **7.950** from the axis |
| Band gaps | — | **0.127** within each pair; 2.16 at the centre |

- **Band positions** (hinge-local x, mm): [−15.487, −8.347], [−8.220, −1.080], [1.080, 8.220], [8.347, 15.487]. C-rings at ±[0.699, 1.080].
- **".14" interpretation (corrected):** ".14" is axis to flag **outer** face (3.524). The flag inner face is tangent to the shaft (2.381). The 2D concept had this wrong by one flag thickness.
- **Flag orientation:** all 4 flags parallel and on the same side (configuration A), which matches B1 closed.
- **Fixed / rotating:** no band is inherently fixed, because the bands are identical and the shaft floats. Mounting decides it. The drawing labels the outer pair FIXED, so B1 uses **F-R-R-F** (outer fixed to the lid, inner two rotating with the leaf).
- **Consequence of the 0.127 gap:** it limits how wide a printed block around one flag can be. This is why the leaf-side fastener dropped from M3 to M2.5.
- **Not in the IGES:** material, temperature data.

## 3. B1 hinge-rail arrangement (validated in the 3D scratch model)

Frame: the closed-lid frame of `CAD/tools/d010_phase2_study.py` (y = 0 at the lid top edge, z = 61 lid back, panel z 67–71, leaf top z 73). Two hinges, centres at x = ±115.

- **Hinge axis:** y 4.0, **z 63.5**. Fixed flags at z 59.98–61.12.
- **Lid rail:**
  - Top-edge chamfer **9 × 45**. Barrel groove R4.024.
  - Fixed-flag seats 1.0 mm deep.
  - Two-zone pocket: deep zone x ±8.15, floor z 56.9 (leaf screw heads); shallow zone x ±9.2, floor z 59.0 (under the rotating flags).
  - The rail sits in the existing display-free strip, y 0–19. The display-side top bezel is unchanged.
- **Lid-side fastening (fixed flags):** M3×8 ISO 7380 from above, into Ruthex RX-M3x5.7 heat-set inserts (D1 4.6, hole Ø4.0, vendor minimum wall 1.6), insert recessed 1 mm.
- **Leaf:**
  - Leaf y 9–235; front beam y 9–18; panel P108 at y 9–232, z 67–71.
  - Leaf blocks x ±7.847, which leaves a **0.5 mm running gap** to the fixed bands.
  - The beam is notched over the fixed flags (3.2 mm of beam above the notch).
- **Leaf-side fastening (rotating flags):** M2.5×5 ISO 7380 + DIN 433 washer from below, into PartsBuilt M2.5 × 4 inserts, OD 3.55, hole Ø3.10 (SKU PBX-TI-M25-4L35W-4PK). **Standard 4.6-OD M2.5 inserts must not be used** (about 0.9 mm wall).
- **Service:** inserts first, then hinge to leaf from the flag side, then leaf to lid from above with the leaf open. With the leaf open ≥ 90°, every screw has 1.7–4.1 mm of driver clearance (kernel). No panel removal and no trapped hardware.

**Superseded parts of the 2D concept** (report 02): axis z 64; chamfer 8 × 45; M3 on both sides with ≥ 2.7 mm boss walls; first contact ~202°. The 3D model above replaces them. `src/section2d/b1_sb261_rail.py` and `b1_sb261_draw.py` (and the figures) are that superseded 2D concept. `b1_sb261_rail_v2.py` uses the IGES flag geometry but is still a 2D section model; the kernel values below govern.

## 4. Kernel results (scratch model `B1HingeValidation`)

**Static fits, closed (ψ = 0):**

| Pair | Clearance (mm) |
|---|---|
| Leaf block to fixed band | 0.50 (deliberate running gap) |
| Lid screw head to beam | 1.00 |
| Leaf screw head to pocket | 1.00 |
| Rotating flag to floor | 0.98 |
| Barrel to panel | 2.58 |

**Leaf motion 0–190° (leaf vs lid):**

| ψ | 30° | 60° | 90° | 120° | 150° | 180° | 190° | 195° | 200° |
|---|---|---|---|---|---|---|---|---|---|
| Clearance (mm) | 2.83 | 4.82 | 6.47 | 6.61 | 4.80 | 3.13 | **2.03** | 1.23 | 0.17 |

- **First contact at 201°:** the leaf front/side-wall corner meets the lid's chamfer face (a candidate soft stop).
- All cross pairs, 30–190°: ≥ 0.50 (the constant block gap); everything else ≥ 1.18.

**Printed walls:**

| Location | Wall (mm) |
|---|---|
| Lid insert to pocket | 1.47 |
| Lid insert to chamfer face | 1.89 |
| Lid insert to groove | 3.21 |
| Leaf insert to block side, to the validated Ø4.0 envelope | 1.20 |
| Leaf insert to block side, to the real OD 3.55 insert | 1.42 |

The lid wall (1.47 to the knurl) is **below** Ruthex's stated 1.6 mm minimum. Only the coupon can settle this.

**Cable:**
- 5 bends, all R 12.00 (read back from the kernel torus geometry).
- Twist zone on the axis, 64 mm long at x 12–76: 2.97°/mm for 190° (study limit 3.5).
- Sleeve OD 7.5 / ID 5.5; 1.25 mm to the leaf beam throughout the motion.
- Hinge-to-cable separation ≥ 9.8.
- Closed: leaf cable to lid 1.00, lid cable to leaf 1.05, lid cable to display 3.00. In motion: ≥ 3.30 and ≥ 2.75.

**Surroundings** (lid at 90/105/110/125°, leaf 0–190°):

| Item | Clearance (mm) |
|---|---|
| Display | ≥ 14.2 |
| Base | ≥ 17.2 |
| Stay | ≥ 21.6 |
| Plug | 2.07 at lid 125°, same as D-010 (unchanged) |
| Table | ≥ 25.1 up to lid 110°; **contact at lid 125°** for ψ ≈ 15–53° |

The table contact is **pre-existing B1 kinematics**, not caused by this hinge. The current D-010 model collides at 14–57° (lid 125°) and 23–38° (lid 120°). The new rail clears at 120°. An operating rule is needed: open the leaf before tilting the lid past about 120°.

## 5. Torque (PUB vs CALC)

| Quantity | Value |
|---|---|
| Band -6, per hinge (PUB) | 8.5–10 lb·in = **0.96–1.13 N·m**, balanced |
| Requirement, per hinge (from the D-010 Phase 2 calculations) | ≈ **0.83 N·m** |
| Minimum safety factor | 0.96 / 0.83 ≈ **1.16** |
| Gravity torque, both hinges (CALC) | 0.498 N·m, which the pair covers ≈ 3.9× |

No higher balanced band is published for this housing.

**Unpublished:** radial, axial and moment capacity, material, temperature range and derating. The CAD shows fit only.

## 6. Physical coupon

Two printed PETG parts plus one real SB-188-SB-261-6. Designed and kernel-checked only. The full specification, hardware list, print recipe, assembly, test procedure, pass/fail criteria and migration gate are in [COUPON_SPEC.md](COUPON_SPEC.md).

## 7. Known limitations and open items

1. **No physical validation.** Fit, motion, insert walls, the 0.5 mm gap and torque are all unconfirmed.
2. **Thin torque margin:** SF ≈ 1.16, with no higher balanced band published.
3. **Unpublished vendor data:** load capacity, material, temperature.
4. **Thin printed walls:** 1.20–1.47 mm around inserts. The lid wall is below the vendor's 1.6 mm guidance.
5. **0.5 mm running gap:** a printed block against a steel band, at a pitch set by the 0.127 band gap.
6. **Table contact at lid ≥ ~122°:** needs an operating rule (pre-existing B1 kinematics).
7. **The hinge in the scratch model is a rebuild from IGES dimensions**, not an import; the connector cannot import IGES. Omitted: the 60° wrap gap and the 0.025 mm fillets, both inside the Ø7.05 envelope.
8. **Earlier D-010 concept findings remain open in that model:** the two 0.00 mm leaf-end cable contacts in `NOMAD_D010_Concepts` (build log 2026-09-29). The scratch SB-261 rail was not written back into `NOMAD_D010_Concepts`.
9. **Not migrated:** the B1/SB-261 geometry exists only in the Onshape connector's scratch document and in `src/`, not in the NOMAD document or `nomad.yaml`.

## 8. Folder contents

| Path | What |
|---|---|
| `README.md` | This engineering record |
| `COUPON_SPEC.md` | Coupon specification and test procedure |
| `VALIDATION_STATUS.md` | What is and is not validated, with evidence labels |
| `SOURCES.md` | Vendor file URL and hashes, insert sources, Onshape scratch workspaces |
| `reports/` | Original session reports, verbatim (01–05) |
| `src/iges/iges_read.py` | Standard library IGES reader. Needs the vendor `.igs` next to it (not committed) |
| `src/fs/b1_common.fs` | B1 + SB-261 FeatureScript library (revised, current). `b1_common_v1.fs` is the pre-revision version |
| `src/fs/prod.fs` | Feature `B1HingeValidation` (the scratch model) |
| `src/fs/h1–h5.fs` | Validation harnesses (static fits, motion, cable, surroundings). They report through a deliberate `regenError` |
| `src/fs/coupon_common.fs`, `coupon_prod.fs` | Coupon library and feature `B1HingeCoupon` |
| `src/fs/h6.fs`, `h7.fs` | Coupon harnesses |
| `src/fs/*.payload.fs` | The exact code sent to Onshape `test_feature`. Payload = header + comment-stripped library + body (`assemble.py` builds the `b1_common` ones) |
| `src/section2d/` | 2D section models (`rail`, `rail_v2`) and the drawing script |
| `figures/` | 2D section figure (superseded 2D concept) |

**Changes made when copying:** the only change from the scratch originals is that hard-coded local absolute paths in the three `src/section2d/*.py` scripts were made repo-relative. No geometry, numbers or logic changed.
