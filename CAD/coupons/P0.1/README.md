# P0.1 Test Coupons: Printable Files

> **SUPERSEDED / DEFERRED FOR NOMAD V1 (D-010, 2026-10-01).** This record belongs to **Architecture A** (sliding/tilting solar cassettes and their lid, D-004 / D-009). The owner selected **Architecture B1** (one solar leaf behind the display lid) as the active V1 architecture. The content below is kept unchanged as an engineering record and possible later reference; it does not describe the V1 design. See `docs/decisions.md` D-010 and `docs/v1-requirements.md`.

Physical test articles for the two largest P0.1 screening risks:
- **Coupon A:** the solar rail cantilever over the display.
- **Coupon B:** the 202 mm rear-shell span and its insert joint.

The test design and procedure are in `prototypes/P0.1/coupons/P01_test_coupons.md`. Concept C (two-piece lid) is the **provisional** basis only; these are test articles, not NOMAD lid parts.

**Location:** `CAD/coupons/P0.1/`. The repo has no `CAD/01_CHASSIS/` tree, and creating a numbered tree just for coupons would restructure `CAD/`. The coupons are self-contained derived test articles, so they live here.

**Status (2026-09-25):** P0.1 coupon geometry is now persistent in the NOMAD Onshape document. The geometry was validated in scratch against the reference generator, then inserted into the user-created P0.1 Coupons Part Studio and visually verified by the user. Physical coupons have not yet been printed or tested.

## Source and regeneration

| Item | Role |
|---|---|
| Onshape Feature Studio `NOMAD_P01_Coupons` | **CAD master** (NOMAD document, element `2e9a95c6ec40fe948348a500`; snapshot `CAD/featurescript/NOMAD_P01_Coupons.fs`). Custom feature "P0.1 Coupons" builds all 13 parts as named solids (`CPN_*`, mapping below); it is inserted in the owner-created Part Studio **P0.1 Coupons**. Edit geometry there (dialog or Feature Studio), not in exported meshes. |
| `generate_coupons.py` | **Local reference** and STL/SCAD source. Standard-library Python; all dimensions are parameters at the top. Must match the Feature Studio. |
| `onshape_crosscheck.py` | Exact expected bounding boxes and volumes (true round holes) for the Onshape parts. |
| `stl/*.stl` | Generated, print-ready binary STL, in mm, already in print orientation (Z = build direction). |
| `scad/*.scad` | Generated OpenSCAD copies of the same geometry, for an independent re-render. **Edit the Python, not these.** |

```bash
py CAD/coupons/P0.1/generate_coupons.py
```
```bash
py CAD/coupons/P0.1/generate_coupons.py --rib-heights 6,8,11
```

The generator rewrites all STL and SCAD files and runs the sanity checks; it fails (exit 1) if any check fails. Optional OpenSCAD cross-check, where OpenSCAD is installed: `openscad -o A1_check.stl scad/A1_rail_printed.scad`.

**Meshing:**
- Box faces are exact.
- Round holes are stepped at **0.1 mm**, finer than a 0.4 mm nozzle and 0.2 mm layer can resolve.
- Every mesh is watertight: each edge is shared by exactly two faces in opposite directions, with no degenerate triangles and one solid body per part.

## Onshape part names

| STL file | Onshape part |
|---|---|
| `A1_rail_printed` | `CPN_A1_rail` |
| `A2_rail_stiffener_slots` | `CPN_A2_rail_stiffener_slots` |
| `A_pad_stub` | `CPN_A_pad_stub` |
| `A_carriage_load_post` | `CPN_A_carriage_load_post` |
| `A_load_platform` | `CPN_A_load_platform` |
| `A_display_surrogate` | `CPN_A_display_surrogate` |
| `B_frame_supports` | `CPN_B_supports` |
| `B_clearance_block` | `CPN_B_clearance_block` |
| `B1_plate_plain_2p5` | `CPN_B1_plate` |
| `B2_plate_ribbed_h06` / `h08` / `h11` | `CPN_B2_h6_plate` / `CPN_B2_h8_plate` / `CPN_B2_h11_plate` (name follows the dialog rib height) |
| `B_load_pad` | `CPN_B_load_pad` |

In Onshape every part is in print orientation on Z = 0, laid out side by side 20 mm apart. Dialog parameters: the three B2 rib heights (6 / 8 / 11) and the insert hole diameter / depth (Onshape default 4.0 / 6.0; **set the depth to 7.0 mm in the dialog** to match the local generator after P0.2-HW, see `prototypes/P0.1/P0.2_insert_interface.md`); everything else is a named `CPN_*` constant at the top of the Feature Studio. Round holes are true circles in Onshape (the STLs step them at 0.1 mm).

## Parts

| File | Coupon | Role | Size X × Y × Z (mm) | Print orientation | Infill |
|---|---|---|---|---|---|
| `A1_rail_printed.stl` | **A1** | Printed V1 rail (exact section) | 200.0 × 39.6 × 13.0 | as exported: floor on bed | **100 % (solid)** |
| `A2_rail_stiffener_slots.stl` | **A2** | Rail with two strip slots | 200.0 × 42.8 × 13.0 | floor on bed | **100 % (solid)** |
| `A_pad_stub.stl` | A | Front-frame pad stub (bezel 2.5 + pad 3.5) | 60.0 × 70.0 × 6.0 | as exported: counterbores on bed | **100 %** (rigid boundary) |
| `A_carriage_load_post.stl` | A | Carriage + load post (Ø5.5 teardrop hole) | 40.0 × 22.0 × 20.0 | body on bed, post up | 40 % |
| `A_load_platform.stl` | A | Optional weight platform over the post | 60.0 × 60.0 × 6.0 | as exported: pocket up | 40 % |
| `A_display_surrogate.stl` | A | Display reference, 5.0 thick | 170.0 × 30.0 × 5.0 | flat | 40 % |
| `B_frame_supports.stl` | B | Base + two 14 mm shelves, 202 mm clear span | 230.0 × 90.0 × 14.0 | base on bed | 40 % (≥ 4 perimeters around inserts) |
| `B_clearance_block.stl` | B | 1.0 mm cassette-clearance reference | 60.0 × 60.0 × 9.0 | flat | 40 % |
| `B1_plate_plain_2p5.stl` | **B1** | Plain 2.5 mm plate | 230.0 × 90.0 × 2.5 | flat | **100 %** |
| `B2_plate_ribbed_h06.stl` | **B2-6** | Ribbed plate, h = 6 | 230.0 × 90.0 × 8.5 | skin on bed, ribs up | **100 %** |
| `B2_plate_ribbed_h08.stl` | **B2-8** | Ribbed plate, h = 8 | 230.0 × 90.0 × 10.5 | skin on bed, ribs up | **100 %** |
| `B2_plate_ribbed_h11.stl` | **B2-11** | Ribbed plate, h = 11 (screened default) | 230.0 × 90.0 × 13.5 | skin on bed, ribs up | **100 %** |
| `B_load_pad.stl` | B | Centre-load spreader | 20.0 × 20.0 × 5.0 | flat | 40 % |

**Print baseline:**
- PETG, 0.4 mm nozzle, 0.2 mm layers.
- **No supports** for any part in the exported orientation.
  - The rail lips are 2.5 mm inward overhangs.
  - The strip-slot roofs are 2.3 mm bridges.
  - The load hole is a teardrop.
  - The pad-stub counterbore step is a 1.55 mm annular overhang.
- **Solid parts** (100 %): the rails, plates and pad stub. The stiffness model assumes solid sections.
- **Minimum features:** rib and wall thickness 2.0 mm; skins around the strip slots 0.9 mm.
- **Record:** slicer settings, filament brand, and the printed mass of every part.

**Minimum bed:**
- Coupon A: ≥ 205 × 45 mm (any 220 mm-class printer).
- Coupon B: **≥ 235 mm in one axis** (230 mm parts), a 250 mm-class printer; it won't fit a 220 × 220 bed.

## Hardware

| Item | Qty | Notes |
|---|---|---|
| M3 heat-set insert | 6 (A 2, B 4) | Holes are **Ø4.0 × 7.0 deep** (P0.2-HW: Ø4.0 is the smallest common pilot, drill up to the datasheet value; 7.0 gives melt relief under a 5.7 insert). See `prototypes/P0.1/P0.2_insert_interface.md` |
| M3 × 8 screw | 6 (A 2, B 4) | A: through the 2.5 mm counterbore seat. B: through the 2.5 mm plate in the rib-free bands |
| Flat strip, ~194 mm long | 2 (A2 only) | 10 × 2 aluminium or 10 × 1.5 steel (slot 2.3 × 10.4); no final material chosen |
| M5 × 60 bolt or rod | 1 | load rod through the post (alternative to the platform) |
| C-clamp, bag, known weights / kitchen scale, feeler gauges 0.05 / 0.5 / 1.0, caliper | — | test tools |

## Assembly

**Coupon A**
1. Heat-set the 2 inserts into the rail ear from the **underside**, at X 7.0 and 21.5.
2. Put the pad stub counterbores down. Screw the rail on from below with 2 × M3 × 8 (heads sit in the counterbores, so the stub stays flat on the table). The rail's X = 0 end lands at stub X 31.5, and the stub's other edge is at rail X 28.5, where the free cantilever starts.
3. Clamp the stub to the table over its outboard 26 mm (away from the rail).
4. **A2:** slide the two strips into the wall slots from the rail's X = 0 end; tape the ends. Test empty first.
5. Slide the carriage into the channel from X = 0, post up through the slot, and push it to the end stop. Stowed carriage centre is X 178, **149.5 mm** from the pad edge.
6. Lay the display surrogate under the cantilever (rail X 30–198). The gap to the rail underside is 1.0 mm.
7. Load with the rod through the post hole and a bag on each side, or with the platform set on the post and weights on top. Use one method or the other, not both.

**Coupon B**
1. Heat-set the 4 inserts into the shelf tops (X 7 / 223, Y 10 / 80).
2. Centre the clearance block in the bay (frame X 85–145, Y 15–75). Leave it out for free-deflection runs.
3. Seat the plate on the shelves (B2: ribs up), holes over the inserts, and fit 4 × M3 × 8 snug.
4. Put the load pad at the plate centre (X 115, Y 45), on the centre rib for B2.

## Test-critical vs fixture dimensions

| Test-critical (changing these changes what is measured) | Fixture only |
|---|---|
| Rail channel 22.6 × 8.0; floor 2.5; lips 2.5 thick; slot 17.6; walls 2.5 (A1) / 4.1 (A2) | Pad-stub footprint 60 × 70 and clamp area |
| Channel length 198, end stop beyond it; stowed carriage centre X 178 → 149.5 arm | Display-surrogate length and width |
| Ear and insert positions (X 7.0 / 21.5); pad-stub thickness 6.0; stub edge at rail X 28.5 | Carriage post height 12.6, load-hole position, platform |
| Display surrogate 5.0 (gives the 1.0 mm gap) | B frame base 4.0 and footprint |
| Carriage clearances: 0.3 per side, 0.6 vertical; post 16.6 in a 17.6 slot | Clearance-block footprint |
| Strip-slot envelope 2.3 × 10.4 at Z 1.3–11.7 | Load-pad size |
| B span 202; bands 14; shelf seat plane Z 14.0; plate 2.5; ribs 2.0 × h at Y 15/45/75 and X 14/115/216 | |
| B screw pitch 70 (Y 10 / 80); clearance block 9.0 (1.0 mm reference) | |

## Geometry changes from `P01_test_coupons.md`

Each change keeps or improves test fidelity.
1. **Rail total length 200, not 198.** The spec put the 2 mm end stop *inside* the 198 mm rail, which would stop the carriage at X 156–196. That shortens the tested arm to 147.5 and cuts the expected deflection by about 4 %. The channel is now the full 198 and the stop sits beyond it, so the **149.5 mm arm and 158 mm travel are preserved**. The strip slots run the full channel length for the same reason.
2. **Carriage post 12.6 tall, not 10.6** (carriage 40 × 22 × 20, not × 18). With the Ø5.5 hole 5 mm below the top, the load rod clears the rail lips by **1.75 mm instead of 0.75**, so the load cannot bear on the lips. Fixture only.
3. **Carriage 0.5 mm edge chamfers** are 0.5 × 0.5 edge reliefs. Same function; box-based geometry.
4. **Added `A_load_platform`** as an optional, support-free way to load the carriage with weights. Fixture only.
5. Round holes are stepped at 0.1 mm (see Meshing), and the load hole is a teardrop, which the spec allowed.
6. Coordinates are shifted so every part starts at (0, 0, 0) in print orientation. No dimensional change.

## Material and print estimate *(rough; the slicer gives the real figures)*

- **Solid parts** (100 %): about 428 g of PETG.
  - A1 40, A2 39, pad stub 32, B1 66, B2-6 79, B2-8 83, B2-11 90 g.
- **Fixtures** (40 %, about 60 % of solid mass): about 154 g.
- **Total:** about **0.58 kg of PETG** and **roughly 35–45 h** of printing at 0.2 mm layers.
- **Minimum run** (A1 + A2 + B1 + B2-11 + fixtures): about 0.42 kg.
