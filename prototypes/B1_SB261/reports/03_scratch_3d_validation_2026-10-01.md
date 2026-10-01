# B1 hinge rail around SB-261: 3D scratch validation

**Classification: 1, geometrically validated enough to proceed.** Two real SB-188-SB-261-6 hinges, mounted directly into a lid hinge rail and a leaf beam, make B1 work: the leaf moves 0–190° with ≥ 2.03 mm clearance and first touches the lid at 201°.

Getting there took one small revision, made inside dimensions we control and already re-validated in the kernel. The real IGES showed the flags 1.2 mm closer to the axis than the drawing reading assumed, and the bands too closely spaced for a full M3 insert on the leaf side. The leaf side therefore uses M2.5 fasteners.

Evidence labels: **IGES** = measured from TorqMaster's file; **kernel** = measured in the Onshape scratch model; **CALC** = analytic. Nothing is physically tested.

## A. IGES verification

The public file is `TORQMASTER-HINGE-ASSEMBLY-SB-188-SB-261-REV-A.igs` (dated 2018-10-16), parsed directly. It is one geometry for every torque band. The assembly is seven solids: one plain unkeyed shaft, four **identical** bands (each a wrap around the shaft plus a flag), and two C-rings at the centre.

| Item | Drawing | IGES |
|---|---|---|
| Barrel OD | R .14, so Ø7.112 | **Ø7.048** (band wrap, 300° around the shaft) |
| Overall length | 1.33, so 33.78 | 33.782 ✓ |
| Shaft | not given | Ø4.762, chamfered ends; C-ring grooves Ø4.19 at the centre only |
| Shaft-end protrusion | .06, so 1.52 | **1.404** |
| Flags | 4 | 4, all parallel and on the same side |
| Flag width | .28, so 7.11 | 7.140 |
| Pitch / gaps | .29 / .37 | 7.267 / 9.300 (gaps of **0.127** between bands, 2.16 at the centre) |
| Reach / thickness | .50 / .045 | 12.700 / 1.143 ✓ |
| Hole | Ø.138 at .31 | Ø3.506 at **7.950** |

- **".14" interpretation (corrected):** it is the distance from the axis to the flag's *outer* face (3.524). The flag's inner face is tangent to the shaft (2.381). The previous scratch study had this wrong by one flag thickness.
- **Fixed / rotating:** nothing in the hinge fixes any band, because the bands are identical and the shaft floats. Which flags are fixed is set by mounting. The drawing labels the outer two FIXED, and the model uses that, **fixed–rotating–rotating–fixed**.
- **Asymmetry that matters:** only the 0.127 mm band gap. It limits how wide a printed block around one flag can be.
- **Material and temperature:** the IGES carries no material or temperature data.

## B. Onshape scratch model

- **Where it lives:** [scratch workspace](https://cad.onshape.com/documents/a3313eb551a601b46ae8de86/w/cbaa5a0d171df874fa4f6dd3/e/7c60e1e6eabeb79b9514eabf), a branch of the connector's own placeholder document, isolated from NOMAD. The connector can't create named documents. Workspace `f8c158e6…` is the superseded pre-revision version and can be deleted.
- **Feature:** `B1HingeValidation`, with parameters for leaf angle ψ, lid angle φ, a surroundings toggle and a live clearance report.
- **Hinge:** the connector cannot import IGES, so the hinge was rebuilt from the IGES dimensions: 4 bands with flags and holes, the shaft and the C-rings. Only the 60° wrap gap and the 0.025 mm fillets are left out, and both sit inside the Ø7.05 envelope.
- **Other geometry modelled:** the lid core and hinge rail, the display, the leaf (panel, beam, blocks, walls), 8 screws and inserts, the cable sleeve, the cables, base, plug, table and stays.

**Mounting works, conventionally.** Changes from the starting concept:
- Axis z 64 → **63.5**. Flags now sit at z 59.98–61.12.
- Lid-edge chamfer 8 → **9 × 45**.
- Fixed flags sit in seats 1.0 mm deep. They are fastened with **M3×8 ISO 7380 from above** into M3 heat-set inserts (L 5.7) recessed 1 mm.
- Rotating flags sit under leaf blocks (x ±7.85). They are fastened with **M2.5×5 ISO 7380 + DIN 433 washer from below** into M2.5 inserts (L 4).
- The pocket has two zones: deep (±8.15, floor z 56.9) for the leaf screw heads, shallow (±9.2, floor z 59.0) under the rotating flags.
- The leaf beam is notched over the fixed flags, leaving 3.2 mm of beam above the notch.
- The display-side top bezel is unchanged. The rail sits in the existing display-free strip, y 0–19.

**Printed walls (CALC):**

| Location | Wall |
|---|---|
| Lid insert to pocket | **1.47** (was 0.42) |
| Lid insert to chamfer face | 1.89 |
| Lid insert to groove | 3.2 |
| Leaf insert to block side | **1.20** (was 0.40 with M3) |
| Leaf insert cap under panel | 1.88 |

**Assembly and service:**
- Inserts go in first.
- Hinge to leaf from the flag side, then leaf to lid from above with the leaf open.
- With the leaf open 90° or more, every screw has 1.7–4.1 mm of driver clearance (kernel).
- No panel removal and no trapped hardware.

## C. Motion (kernel, leaf vs lid)

| Leaf angle ψ | Clearance (mm) |
|---|---|
| 0° | Rest on the lid back (closed stop). Closest static fits: block to fixed band 0.50 (deliberate running gap); lid head to beam 1.00; leaf head to pocket 1.00; rotating flag to floor 0.98; barrel to panel 2.58 |
| 30 / 60° | 2.83 / 4.82 |
| **90°** | **6.47** |
| 120 / 150° | 6.61 / 4.80 |
| **180°** | **3.13** |
| **190°** | **2.03** |

- **First interference: 201°**, the leaf front/side-wall corner meeting the lid's chamfer face (1.23 mm at 195°, 0.17 mm at 200°). That face can serve as the soft stop.
- **All cross pairs, 30–190°:** ≥ 0.50 mm, which is the constant block-to-fixed-band gap. Everything else is ≥ 1.18 mm.

## D. Cable

- **Bend radius:** all 5 bends are R 12.00 (read back from the kernel's torus geometry).
- **Twist:** 64 mm twist zone on the axis gives 2.97°/mm for 190°; the study's limit is 3.5.
- **Sleeve (OD 7.5 / ID 5.5):** 1.25 mm to the leaf beam, constant through the motion. It fits the central region x 12–76.
- **Hinge/cable separation:** ≥ 9.8 mm.
- **Closed clearances:** leaf cable to lid 1.00, lid cable to leaf 1.05, lid cable to display 3.00.
- **In motion:** ≥ 3.30 and ≥ 2.75. No interference anywhere from 0° to 190°.

## E. Surrounding geometry (lid at 90/105/110/125°, leaf 0–190°)

| Item | Result |
|---|---|
| Display | ≥ 14.2 mm |
| Base | ≥ 17.2 mm |
| Stay | ≥ 21.6 mm |
| Plug | 2.07 mm at lid 125°, identical to D-010 (unchanged) |
| Table | ≥ 25.1 mm up to lid 110°; contact at lid 125° (below) |

The table contact needs explaining. At lid 125°, the leaf's free end crosses the table plane for ψ ≈ 15–53°. This is **pre-existing B1 kinematics**: the current D-010 geometry collides at 14–57° (lid 125°) and 23–38° (lid 120°). The new rail is slightly better, clearing at 120°.

## F. Remaining risks

1. **Torque margin unchanged:** band -6 has a 0.96 N·m minimum against the 0.83 requirement, SF ≈ 1.16. Gravity alone for the pair is 0.498 N·m (CALC), a 3.9× margin.
2. **Unpublished data:** radial, axial and moment capacity, material, and temperature derating. The CAD shows fit only.
3. **Thin margins that need a physical coupon:** insert walls of 1.2–1.5 mm, and the 0.5 mm printed-block-to-steel-band running gap. The band pitch forces these.
4. **Operating rule needed:** open the leaf before tilting the lid past about 120°. This is not a hinge issue.

## G. Recommendation

**1. Validated enough to proceed**, with the revised geometry above, which is already re-validated.

The next step, if you approve, is the physical coupon (lid seat and leaf block with inserts and real hinges) to confirm the insert walls, the 0.5 mm gap and torque in hand. No hinge purchase or migration into NOMAD CAD has been done.

**What was and wasn't touched:** the repo, YAML, specs, D-010 files, the NOMAD Onshape document and git are untouched. Onshape usage rose from 382 to 468 of 2,500 requests (11 paid calls; one run failed on a FeatureScript Id-ordering rule, now in the notes). The scratch sources (IGES parser, FeatureScript, harnesses) are in the session scratchpad, which is temporary. I added a memory note with these results and the workspace link.

I'm stopping here for your approval.