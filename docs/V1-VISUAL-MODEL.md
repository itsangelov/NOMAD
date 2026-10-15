# NOMAD V1 visual master model (Onshape)

**What it is:** one Onshape custom feature, **"NOMAD V1 Visual"**, that builds the whole engineered V1 so it can be inspected before buying hardware. It covers:
- the base and lid exterior
- the display
- the keyboard and trackpad
- the B1 solar leaf on the real SB-261 hinge geometry
- the Southco display hinges
- every internal module
- ports and vents
- 15 cable routes
- keep-out bodies
- poses and an exploded service view

**What it is not:** production CAD, or a validated design.

| Item | Location |
|---|---|
| Source | `CAD/featurescript/NOMAD_V1_Visual.fs` (readable master) |
| Onshape copy | `CAD/featurescript/NOMAD_V1_Visual.onshape.fs` = `py CAD/tools/fs_compact.py CAD/featurescript/NOMAD_V1_Visual.fs CAD/featurescript/NOMAD_V1_Visual.onshape.fs` (comments / blank lines / insignificant spaces stripped; same code). This exact file is in Onshape. |
| Onshape | NOMAD document, Feature Studio **`NOMAD_V1_Visual`** (element `041ff69ce1d94a2b7f74d123`), custom feature **NOMAD V1 Visual** |
| QA harness | `CAD/featurescript/NOMAD_V1_Visual.qa.test.fs` (test_feature payload part; see its header) |
| Generator | `py CAD/tools/v1_visual_emit.py --write` (`--check` verifies the generated block is current) |
| Generator inputs | the V1 integration model (`CAD/tools/v1_integration.py` → `nomad.yaml`, `prototypes/V1/v1_hardware.py`) and the AUO G101UAN01.0 specification rev 1.5 |
| B1 hinge rail / leaf / solar sleeve | spliced unchanged from the kernel-validated `prototypes/B1_SB261/src/fs/b1_common.fs`; only the lid width (306) and lid depth (253) changed |

**2026-10-08 compatibility pass:**
- The first manual paste would not commit.
- The builder now uses only FeatureScript calls and patterns that already compiled in this repository (NOMAD_D010_Concepts, the SB-261 library).
- The file is ASCII-only, with one primitive per line (max 214 characters).
- The generated geometry data is identical.

**Status (2026-10-08, simulated in the Onshape kernel, not physically tested):**
- Compiled and regenerated in Onshape (`test_feature`, FeatureScript 3083): all 10 poses build, 287–289 bodies, every body named, no build warnings.
- Persisted in the NOMAD document (Feature Studio above). The persisted text was read back and is byte-identical to `NOMAD_V1_Visual.onshape.fs`.
- **2026-10-15:** inserted by the owner into the Part Studio **`NOMAD V1 — Digital Prototype`** (element `0f33f26180e493dbfcfd4d4a`), where it regenerates. Onshape reports one open build warning: `shell cut 3` (the base's exterior edge-chamfer cut). This was not visible through the test harness. The cavity and all other geometry build; the base edges are drawn sharp. Screenshots: `docs/images/`.

## Put it in Onshape (owner, about 2 minutes)

1. Open the NOMAD document. The Feature Studio **`NOMAD_V1_Visual`** already exists.
2. Create a Part Studio **`NOMAD V1`** and insert the custom feature **NOMAD V1 Visual** (custom features list, or the Feature Studio's insert button). Default: pose 2 (lid 110), cables on, clearance report on.
3. Change *Pose* in the dialog for the other states. The feature's info line shows the leaf-table and clearance read-out. A yellow **BUILD WARNING** means a boolean failed and names the part.
4. Optional: Part Studio configuration inputs for *Pose*, *Lid angle* and *Leaf angle*, linked to the dialog fields, give drop-downs. Optional: insert the Part Studio into an Assembly (no mates are needed; every part is placed for the pose).

**If something fails:** the Onshape copy has no comments, so error lines refer to `NOMAD_V1_Visual.onshape.fs`. Fix the readable `.fs` (or the generator) and regenerate the copy with `fs_compact.py`.

## Onshape QA (2026-10-08, kernel-checked with `NOMAD_V1_Visual.qa.test.fs`)

| Check | Result |
|---|---|
| Poses (all display options on) | 1 closed, 2 open 110, 3–6 leaf 90 / 120 / 180 / 190, 7 lid 135, 8 table limit, 9 service (exploded), custom (lid 60 / leaf 45): all build, 0 unnamed bodies |
| Lid core – base | 2.00 closed (D-006 working gap), 1.83 at 110, 1.41 at the 135 stop |
| Leaf frame – lid core | 6.47 / 6.61 / 3.13 / **2.03** at leaf 90 / 120 / 180 / 190 (B1 record: 2.03 at 190) |
| Leaf lowest point | above the table in every pose except 8: **z −31.5 at lid 135 + leaf 40 = leaf / table contact (known B1 limit, shown)** |
| Booleans | every cut applied (volume vs a "+"-only rebuild: shell 2.84e6 mm³, lid core 2.41e5 mm³, panels, fan, knuckle) |
| Cables | 15 routes, every bend present |
| Pairwise overlaps (closed, 82 groups) | 56, of which 47 are intentional contacts (screws in bosses, standoffs through PCBs, plugs in sockets, cable ends in their connectors, hinge bands on their shaft, 0.01–0.2 mm seating) and 9 are the open findings below |

**Open findings from the kernel check (shown, not hidden):**
1. B1 stay pivots (±125, 240) pass through the main service panel (and the shell floor zone): the pivot / panel interface is not designed.
2. Active Cooler envelope (63.5 × 42.5, interpreted drawing) overlaps the GPIO header strip by ≈ 3.4 mm and the two front Pi standoffs: needs the real cooler outline.
3. Power board (no layout): the control-harness and button-lead terminals, and the solar lead's last segment, touch the 12 V module envelope; the solar lead crosses the button lead there.
4. eDP and solar leads cross the knuckle wall (the knuckle is a concept tube; the axial twist path is not modelled).

## Fixes made in the Onshape run (2026-10-08)

Geometry consistency only; no engineering parameter changed. Each was found by the kernel, not by inspection.
- **Base shell cavity was silently not cut** (`BOOLEAN_NON_MANIFOLD_RESULT`, hidden by `try silent`): the 5 mm rear corner chamfer on a 2.5 wall passed exactly through the inner corner edge. Now: cavity → 2.5 mm inner corner fill → exterior chamfers. Service panel corners are notched to match.
- **Front vertical corner chamfers 8 → 1.5 mm (base and lid).** They were visual styling from this generator (no `nomad.yaml` parameter). With a 2.5 wall an 8 mm chamfer cuts ≈ 4.6 mm into the fan, which the integration layout places flush in the front-right corner.
- **The builder now reports failed booleans** as a yellow BUILD WARNING naming the part, instead of hiding them.
- **Cable route concepts** (were crossing solids):
  - GNSS and control harness now pass over the Pi USB plugs (z 35 / 31.5), drop in the bulkhead–Pi gap at y 94 and run under the keyboard tray at z 14.
  - The fan lead runs down the right-hand side of the Pi stack.
  - The rear trunk is now side by side: SYS 190.5, control 196, solar 200.5. The SYS bus drops to z 10.5 after the Beck envelope.
- **Lid:** solar-lead channels cut in the lid core and the foil; eDP channel 0.1 mm higher; eDP / solar exit notch to the knuckle. The foil now ends before the leaf rear wall.
- **USB-C wall opening** re-centred on the receptacle (z 8.6; it was 1.9 mm high). The external plug keep-out moved with it.
- Fan rotor struts reach the frame (one body).

## Dialog

| Option | What it shows |
|---|---|
| **Pose** | 1 Closed · 2 Open (lid 110) · 3 / 4 / 5 / 6 Solar leaf 90 / 120 / 180 / 190 (stay out) · 7 Lid at the 135 stop · **8 KNOWN LIMIT: lid 135 + leaf 40, leaf edge reaches the table** · 9 Service view (exploded) · Custom (any lid 0–135, leaf 0–190, stay, explode) |
| Show cables / harness | 15 routed cables, colour-coded: red power, orange solar, grey-blue eDP, grey USB, yellow signal |
| Show clearance / keep-out bodies and conflicts | Every v1_integration keep-out and corridor, plug clearances, the exhaust plume, and the **21 mm keyboard conflict ghost** |
| Show airflow arrows | Rear / underside intake → under the keyboard → Pi bay → right-wall exhaust |
| Show table plane | z = −4 (rubber feet) |
| X-ray | Transparent base shell, panels, door, trays, lid core and keyboard, so the internals are visible |
| Colour by validation status | Green ENGINEERED, amber SELECTED, red PLACEHOLDER, magenta CONFLICT |
| Report clearances | The feature info line shows the leaf's lowest point vs the table, lid-core–base, leaf–base and leaf–lid-core distances at the current pose |

Every part name starts `V1 |`, then the subsystem and the part (for example `BATTERY | Molicel INR-21700-M65A cell 1 of 4 …`). It ends with its status tag.

## What is represented

| Category | Parts | Basis |
|---|---|---|
| **ENGINEERED** (our V1 design, modelled, not physically tested) | Base shell (walls, deck with keyboard / trackpad openings, 3 × 45 top edges, corner chamfers, bulkheads with plug pass-throughs, bay wall with battery-lead slot, hinge corner blocks, M3 bosses); ports (USB-C, button, 2 × USB-A); exhaust and intake grilles; display-cable pass; keyboard / trackpad trays; main panel with intake slots; front panel with sled pocket; battery door; compute sled; lid core 19 with display window / pocket and hinge pockets; leaf frame; foil; stay (stowed / deployed); cable knuckle; cable routes; keep-outs | `v1_integration.py` (58 PASS / 8 WARN / 0 FAIL), D-010, SB-261 record |
| **SELECTED** (catalogue part, manufacturer data, not bought or validated) | Pi 5 (ports per the RPi drawing, approximate), Active Cooler, M.2 HAT+, SSD 2230, AUO G101UAN01.0 (**MFR rev 1.5: 228.22 × 148.32 × 5.35, active 216.81 × 135.5, 140 g**), Beck BTC-mini-eDP, PERIBOARD-416, PERIPAD-501 II, DAN-F10N pHAT + patch, Sunon 30 mm fan, 4 × M65A cells, Pololu 5 V / 12 V, Southco E6-10-216-50 ×2, SB-261-6 ×2 (IGES geometry), P108, fasteners | `v1_hardware.py` |
| **PLACEHOLDER** (needs data) | Power board (TIDA-050047-based, **no layout exists**: an 80 × 40 envelope with the expected USB-C, solar, 12 V and I²C interface positions); battery holder, nickel and on-pack BMS / fuse; keyboard USB-C position (from a photo); eDP connector position on the panel (datasheet drawing p. 24 not yet read); GPIO right-angle housings; USB-A panel sockets; power button; trackpad lead coil | — |
| **CONFLICT** | 21 mm keyboard ghost | Perixx product page vs manual |

## Source conflicts found while building it

Each one is shown in the model and none was silently resolved.

1. **Display outline:** `nomad.yaml` 229.9 × 150.5 (3P) vs **AUO spec 228.22 × 148.32 (MFR)**. The model uses the MFR value. The YAML update needs owner approval. No clearance gets worse, because the panel is smaller.
2. **Leaf depth:** `SOLAR_LEAF_DEPTH` 239 (panel + 16) vs the kernel-validated SB-261 leaf (y 9–235, 226 deep). The model uses the validated geometry. 239 remains a conservative load input.
3. **Panel width vs leaf rebate:**
   - The validated leaf rebate holds 273 mm; the P108 is 274 mm (MFR).
   - The ASA / FR4 expansion clearance needs ≥ 0.6 mm per side.
   - So the leaf side walls must move out ≈ 1.1 mm per side (leaf ≈ 291 wide, still inside the 306 lid).
   - **This is a real (small) fix needed before the leaf frame is printed.** The model shows the validated 273.
4. **Keyboard thickness:** 16 mm (manual) is modelled; 21 mm (product page) is shown as the CONFLICT ghost. At 21 mm either the keyboard stands 5 mm proud of the deck (and the closed lid would hit it), or its tray drops 5 mm and the under-keyboard free height falls from 18.5 to 13.5, below the 16 mm power-zone envelope. **Measure the keyboard first.**
5. **Display hinge axis:**
   - The model keeps the D-006 working axis at the base rear top edge.
   - Barrels and leaves sit in notches / rear-face pockets (concept).
   - A surface-mounted E6 really puts the axis ≈ 5 mm behind the face; the lid sweep has ≥ 20 mm margin, so this does not change any clearance verdict.

## Fixes made while building the visual model

Placement detail only; no engineering value changed.
- **Battery door:**
  - The 4 corner screws of the first draft would have sat inside the cells.
  - The door now uses 2 captive M3 into the bulkhead plus 2 edge hooks, with short bosses that stay under the trackpad tray.
- **Front-wall bosses** in the battery bay were removed. One rear boss moved off the knuckle.
- **Battery-lead slot** cut through the bay rear wall: the corridor in v1_integration started after the wall.
- **Pack connector** moved into that slot.
- **Solar input connector** on the power board moved clear of the 12 V module.
- **Active Cooler** kept inside the Pi PCB outline.
- **Cable routes:**
  - The GNSS and control harnesses run above the Pi stack (z 35, under the 37.5 deck) and down the 8 mm gap between the bulkhead and the Pi.
  - All 15 routes clear every solid envelope they do not serve (generator check).

## What still cannot be shown accurately

- Exact connector positions on the Beck board, the power board, the keyboard and the eDP panel connector (drawings or photos needed).
- The power board itself (no layout).
- Cable cut lengths and real bend behaviour.
- Southco leaf geometry (the catalogue drawing was only partly transcribed).
- Real Pi 5 component heights beyond the port blocks.
- Drag-able assembly mates (an owner action in Onshape).
