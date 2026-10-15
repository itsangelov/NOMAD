# Mechanical Specification — NOMAD V1

Revision: **Virtual V1 (2026-10-06)**. No value below is locked or physically verified.

> **Source of truth (D-002):** `CAD/parameters/nomad.yaml` holds the authoritative machine-readable values. This document is the human-readable specification and must agree with it. If they differ, the YAML is correct. `py CAD/tools/yaml_to_featurescript.py --validate-v1` checks that every YAML parameter is named here.

> **Architecture: B1 (D-010).** The Virtual V1 integration (layout, checks, masses, thermal) is `CAD/tools/v1_integration.py`, reported in [`docs/V1-VIRTUAL-INTEGRATION.md`](V1-VIRTUAL-INTEGRATION.md). The V1 integration baseline is proposed as D-011.

> **History:** the P0.1 / Round C / Round E / Architecture A parameter set is frozen in `CAD/parameters/history/nomad_P0.1_2026-10-02.yaml` and reproduced unchanged under [Historical P0.1 record](#historical-p01-record-frozen-2026-10-02) below. It is not the V1 design.

## Parameter status legend

| Status | Meaning |
|---|---|
| **verified** | Measured on the physical part, or from a manufacturer datasheet for a locked SKU (none yet) |
| **derived** | Calculated from other values |
| **provisional** | Chosen for V1, or taken from candidate-part documentation. Not physically verified. Expect change. |
| **TBD** | No authoritative value. A working input (number or formula) may still drive the V1 envelope model. |

All dimensions in mm unless noted. "Working" = the number the V1 envelope model uses while the value is TBD (formula results follow their inputs).

## V1 master parameters


### body

| Parameter | Value | Unit | Status | Working (model) | Source / notes |
|---|---|---|---|---|---|
| BODY_WIDTH | — | mm | TBD | = KEYBOARD_WIDTH + 2 * (BASE_SIDE_MARGIN + WALL_THICKNESS) → 306 | Derived: keyboard width + side margins + walls (D-003) |
| BODY_DEPTH | — | mm | TBD | = BASE_FRONT_MARGIN + TRACKPAD_DEPTH + TRACKPAD_KEYBOARD_GAP + KEYBOARD_DEPTH + BASE_REAR_ZONE_DEPTH → 253 | Derived: front margin + trackpad + gap + keyboard + rear zone (D-003) |
| BODY_HEIGHT | 40 | mm | provisional | — | V1 integration: palm bays hold the holder battery pack (31) and the Pi stack envelope (30) under a 2.5 deck over a 2.5 panel; under-keyboard zone 18.5 (v1_integration.py) |
| WALL_THICKNESS | 2.5 | mm | provisional | — | PETG FDM, ~6 perimeters at 0.4 mm; confirm with the P0.2 coupons |
| SERVICE_PANEL_THICKNESS | 2.5 | mm | provisional | — | Main service panel and battery door |
| MOUNT_PLATE_THICKNESS | 2 | mm | provisional | — | Keyboard tray, trackpad tray, compute sled |
| INPUT_TRAY_LIP | 3 | mm | provisional | — | Tray margin beyond the keyboard / trackpad outline, front and rear |
| TRACKPAD_BAY_MARGIN | 5 | mm | provisional | — | Trackpad edge to the trackpad-bay bulkhead |
| BOSS_DIAMETER | 8 | mm | provisional | — | Shell boss OD around a 4.0 hole for the Ruthex RX-M3x5.7 insert: 2.0 wall (V1 DFM review; was 7 working = 1.5 wall) |
| PANEL_SCREW_INSET | 3.5 | mm | provisional | — | Service-panel / door screw axis from the wall inner face: ISO 7380 M3 head r 2.85 clears the wall by >= 0.5 and leaves >= 1.2 panel beyond the 3.4 hole (fixes Round E F1, where the axis was 1.95 from the panel edge) |
| TRAY_POST_DIAMETER | 6 | mm | provisional | — | Tray posts with M2.5 inserts (OD 3.55): >= 1.2 wall (V1 DFM review; was 5 working) |
| HINGE_MOUNT_WIDTH | 44 | mm | provisional | — | Display-hinge corner block across X: Southco E6-10 medium 38 long + 2 x 3 (catalogue) |
| HINGE_MOUNT_DEPTH | 24 | mm | provisional | — | Display-hinge corner block along Y from the rear inner face: E6 base leaf ~20 (INFERRED) + 4 for M4 inserts |
| BASE_SIDE_MARGIN | 8 | mm | provisional | — | Keyboard edge to inner side wall |
| BASE_FRONT_MARGIN | 15 | mm | provisional | — | Base front face to trackpad front edge (includes wall) |
| BASE_REAR_ZONE_DEPTH | 36 | mm | provisional | — | Keyboard rear edge to base rear face: hinge corner blocks + GNSS sky strip (GNSS pHAT 30 deep + walls); was 30 working (V1 integration) |
| HINGE_AXIS_OFFSET | — | mm | TBD | 0 | Display hinge axis inset from the base rear face (negative = behind it); note: D-006 provisional rear-face direction; exact position at the mechanism prototype |
| HINGE_AXIS_HEIGHT | — | mm | TBD | 0 | Display hinge axis height above the base top surface; note: D-006; exact Z at the mechanism prototype |
| HINGE_BARREL_DIAMETER | 10 | mm | provisional | — | Southco E6-10 medium barrel (catalogue drawing, INFERRED) |

### lid

| Parameter | Value | Unit | Status | Working (model) | Source / notes |
|---|---|---|---|---|---|
| LID_THICKNESS | — | mm | TBD | = LID_CORE_THICKNESS + SOLAR_LEAF_AIR_GAP + SOLAR_LEAF_THICKNESS → 31 | B1 lid stack: core + vented air gap + leaf |
| LID_CLOSED_GAP | — | mm | TBD | 2 | Closed-lid standoff between base top and lid display face (bumpers); note: D-006 working value |
| LID_ANGLE_NOMINAL | — | deg | TBD | 110 | Nominal open pose for checks (SYS-7: 105-110; D-010 states use 110) |
| LID_ANGLE_MAX | 135 | deg | provisional | — | Mechanical hard stop in the display-hinge corner blocks (V1 Phase 8); hinge torque sized to 135 |
| LID_HINGE_TORQUE | 1.8 | none | provisional | — | N.m per hinge, Southco E6-10-216-50 symmetric (catalogue); 2 hinges; selected by v1_integration.py hinge check |

### lid_b1

| Parameter | Value | Unit | Status | Working (model) | Source / notes |
|---|---|---|---|---|---|
| LID_CORE_THICKNESS | 19 | mm | provisional | — | B1 lid core kept at the D-010 / SB-261 baseline (the SB-261 lid hinge rail needs it): lip 1 + panel 5.35 + gap 1 + cable/rib zone 9.15 + back shell 2.5; controller moved to the base |
| SOLAR_LEAF_AIR_GAP | 6 | mm | provisional | — | Vented air gap with low-e foil (D-010 Phase 2 s.13, EST thermal model) (limit: min) |

### solar_leaf

| Parameter | Value | Unit | Status | Working (model) | Source / notes |
|---|---|---|---|---|---|
| SOLAR_LEAF_ANGLE_MAX | 190 | deg | provisional | — | D-010 (owner, 2026-10-01). Scratch kernel: >= 2.03 mm leaf-to-lid at 190, first contact 201 (prototypes/B1_SB261) |
| SOLAR_LEAF_CABLE_BEND_RADIUS | 12 | mm | provisional | — | D-010 (owner): R12 static bends (3 x d of a 4 mm 2 x 0.5 mm2 lead); moving sections are axial twist zones (limit: min) |
| SOLAR_LEAF_HINGE_AXIS_INSET | — | mm | TBD | 4 | Leaf hinge axis from the lid free edge (SB-261 scratch rail; kernel-checked, not tested) |
| SOLAR_LEAF_HINGE_AXIS_HEIGHT | — | mm | TBD | 2.5 | Leaf hinge axis above the lid-back face (SB-261 scratch rail: axis z 63.5, lid back z 61) |
| SOLAR_LEAF_HINGE_SPACING | — | mm | TBD | 230 | Leaf hinge centres (SB-261 scratch rail x = +/-115); reference: TorqMaster SB-188-SB-261-6, 33.8 long, barrel 7.05 (IGES) |
| SOLAR_LEAF_WIDTH | — | mm | TBD | = SOLAR_PANEL_WIDTH + 16 → 290 | Leaf outline X: panel + 2 x 8 frame |
| SOLAR_LEAF_DEPTH | — | mm | TBD | = SOLAR_PANEL_DEPTH + 16 → 239 | Leaf outline Y: panel + 2 x 8 frame (V1: the lid grew to 253 deep; the leaf follows the panel, not the lid, which keeps the leaf mass and wind area at the D-010 basis) |
| SOLAR_LEAF_THICKNESS | 6 | mm | provisional | — | Leaf frame: 4 mm panel in a rebate under a 2 mm lip (D-010 Phase 2) |
| SOLAR_PANEL_WIDTH | 274 | mm | provisional | — | Voltaic P108 candidate, 27.4 cm (MFR page; confirm on P108_dwg.pdf) |
| SOLAR_PANEL_DEPTH | 223 | mm | provisional | — | Voltaic P108 candidate (MFR) |
| SOLAR_PANEL_THICKNESS | 4 | mm | provisional | — | Voltaic P108 candidate, ETFE on 2 mm FR4 (MFR) |
| SOLAR_STAY_REACH | — | mm | TBD | 105 | Rear outrigger stay reach behind the base (D-010 Phase 2 s.11: >= 90; mandatory) |
| STAY_PIVOT_INSET_X | — | mm | TBD | 28 | Stay pivot from the base side face, in the rear corner block (D-010: x +/-125 on a 301 base) |
| STAY_PIVOT_INSET_Y | — | mm | TBD | 13 | Stay pivot from the base rear face (D-010: y 222 on a 235 base = 13; V1 corner block) |

### display

| Parameter | Value | Unit | Status | Working (model) | Source / notes |
|---|---|---|---|---|---|
| DISPLAY_DIAGONAL | 256.5 | mm | provisional | — | 10.1 in (spec target) |
| DISPLAY_ACTIVE_WIDTH | 216.81 | mm | provisional | — | AUO 10.1 WUXGA family active area (3P) |
| DISPLAY_ACTIVE_HEIGHT | 135.5 | mm | provisional | — | AUO 10.1 WUXGA family active area (3P) |
| DISPLAY_WIDTH | 229.9 | mm | provisional | — | AUO G101UAN01.0 candidate: max of two 3P outlines (228.22 / 229.9); AUO datasheet to confirm |
| DISPLAY_HEIGHT | 150.5 | mm | provisional | — | AUO G101UAN01.0 candidate: max of two 3P outlines (148.32 / 150.5) |
| DISPLAY_THICKNESS | 5.35 | mm | provisional | — | AUO G101UAN01.0 candidate: max of two 3P values (5.35 / 4.15) |
| DISPLAY_VERTICAL_OFFSET | — | mm | TBD | 0 | Display centre offset from the lid centre, + toward the lid free edge; intent: 0 = centred; v1_integration checks >= the SB-261 display-free band |
| DISPLAY_BEZEL_LIP | — | mm | TBD | 1 | Front retention lip over the display border |
| DISPLAY_FREE_BAND | 42.5 | mm | provisional | — | Display-free band at the lid free edge for the SB-261 leaf hinge rail (prototypes/B1_SB261: display starts at y 42.5) |
| DISPLAY_CONTROLLER_WIDTH | 80 | mm | provisional | — | Beck BTC-mini-eDP candidate (MFR) |
| DISPLAY_CONTROLLER_DEPTH | 70 | mm | provisional | — | Beck BTC-mini-eDP candidate (MFR) |
| DISPLAY_CONTROLLER_THICKNESS | 9.8 | mm | provisional | — | Beck BTC-mini-eDP total height (MFR); located in the BASE under the keyboard (V1) |

### controls

| Parameter | Value | Unit | Status | Working (model) | Source / notes |
|---|---|---|---|---|---|
| KEYBOARD_WIDTH | 285 | mm | provisional | — | Perixx PERIBOARD-416 candidate (MFR manual 285 x 117 x 16) |
| KEYBOARD_DEPTH | 117 | mm | provisional | — | Perixx PERIBOARD-416 candidate (MFR manual) |
| KEYBOARD_THICKNESS | 16 | mm | provisional | — | Perixx PERIBOARD-416 candidate (MFR manual). The <= 8 target is not met by any wired candidate (E-POWER-001 C4) |
| TRACKPAD_WIDTH | 86 | mm | provisional | — | Perixx PERIPAD-501 II candidate (MFR manual) |
| TRACKPAD_DEPTH | 75 | mm | provisional | — | Perixx PERIPAD-501 II candidate (MFR manual) |
| TRACKPAD_THICKNESS | 13 | mm | provisional | — | Perixx PERIPAD-501 II candidate (MFR manual) |

### layout

| Parameter | Value | Unit | Status | Working (model) | Source / notes |
|---|---|---|---|---|---|
| KEYBOARD_LATERAL_OFFSET | 0 | mm | provisional | — | D-003: centred on the chassis centreline |
| TRACKPAD_LATERAL_OFFSET | 0 | mm | provisional | — | D-003: centred on the chassis centreline |
| TRACKPAD_KEYBOARD_GAP | — | mm | TBD | 10 | D-003; trackpad below the keyboard |
| KEYBOARD_TOP_RECESS | — | mm | TBD | 1 | Keyboard top below the base top surface |
| TRACKPAD_TOP_RECESS | — | mm | TBD | 1 | Trackpad top below the base top surface |

### computer

| Parameter | Value | Unit | Status | Working (model) | Source / notes |
|---|---|---|---|---|---|
| PI_WIDTH | 85 | mm | provisional | — | Raspberry Pi 5 board outline (MFR drawing, approximate) |
| PI_DEPTH | 56 | mm | provisional | — | Raspberry Pi 5 board outline (MFR drawing, approximate) |
| PI_STACK_HEIGHT | — | mm | TBD | 30 | Sled top to stack top: Pi 5 + Active Cooler + 16 mm header + M.2 HAT+ + 2230 SSD; note: EST 25-27 (v1_integration.py stack sum); measure at gate 3 |
| PI_ENVELOPE_MARGIN | — | mm | TBD | 3 | Board outline to envelope, each side: port overhang + fit |
| COMPUTE_POWER_WIDTH | — | mm | TBD | 50 | 5.1 V rail zone (Pololu D36V50F5 25.4 x 25.4 x 9.5 + leads) |
| COMPUTE_POWER_DEPTH | — | mm | TBD | 30 | 5.1 V rail zone |
| COMPUTE_POWER_HEIGHT | — | mm | TBD | 15 | 5.1 V rail zone |
| GNSS_MODULE_WIDTH | — | mm | TBD | 70 | SparkFun GNSS Flex pHAT envelope X (pHAT 65 + margin) |
| GNSS_MODULE_DEPTH | — | mm | TBD | 33 | GNSS pHAT envelope Y (30 + margin) |
| GNSS_MODULE_HEIGHT | — | mm | TBD | 16 | GNSS pHAT envelope Z incl. standoffs and the 8 mm patch |
| GNSS_ANTENNA_KEEPOUT | — | mm | TBD | 10 | No metal or cable above / around the patch (u-blox: 70 x 70 ground plane optimal) |
| NVME_FORMAT | 2230 | none | provisional | — | Raspberry Pi SSD 512 GB candidate |

### cooling

| Parameter | Value | Unit | Status | Working (model) | Source / notes |
|---|---|---|---|---|---|
| COOLING_FAN_SIZE | 30 | mm | provisional | — | Sunon MF30100V1-1000U-A99 candidate, 30 x 30 x 10 (MFR); a 40 mm fan does not fit the 35 internal height wall-mounted |
| COOLING_FAN_THICKNESS | 10 | mm | provisional | — | Sunon MF30100V1 (MFR) |
| VENT_INTAKE_AREA | — | none | TBD | 1500 | mm2 open area, rear-wall + underside intake grilles (v1_integration thermal check) |

### clearances

| Parameter | Value | Unit | Status | Working (model) | Source / notes |
|---|---|---|---|---|---|
| CLEARANCE | — | mm | TBD | 0.3 | FDM fit clearance (P0.2 coupons) |
| MIN_GAP | — | mm | TBD | 1 | Minimum clearance between envelopes |
| MIN_WALL | — | mm | TBD | 2 | Minimum printed wall (PETG FDM) |
| CABLE_CLEARANCE | — | mm | TBD | — | Per cable, from bend radius (harness table, docs/V1-VIRTUAL-INTEGRATION.md s.11) |
| CABLE_CORRIDOR_WIDTH | — | mm | TBD | 15 | Reserved cable-corridor cross-section width |
| CABLE_CORRIDOR_HEIGHT | — | mm | TBD | 10 | Reserved cable-corridor cross-section height |
| OVERHANG_LIMIT | 45 | deg | provisional | — | Common FDM practice for PETG without supports; confirm on the printer |

### fasteners

| Parameter | Value | Unit | Status | Working (model) | Source / notes |
|---|---|---|---|---|---|
| FASTENER_SIZE | M2.5, M3, M4 | none | provisional | — | Standard family; M4 only for the display hinges (Southco 4.5 holes) and the stay pivots |
| INSERT_SIZE | RX-M3x5.7 in 4.0 x 7.0, M2.5 x 4 OD 3.55, M4 (SKU TBD) | none | provisional | — | prototypes/B1_SB261, P0.2-HW (prototypes/P0.1/P0.2_insert_interface.md) |

### io

| Parameter | Value | Unit | Status | Working (model) | Source / notes |
|---|---|---|---|---|---|
| REAR_PORTS | none | none | provisional | — | V1: no external plugs on the rear face (resolves the lid-sweep conflict, Phase 8). Ports on the side and front walls |
| SIDE_PORT_ZONE_BOTTOM | — | mm | TBD | 5 | Lowest connector edge above the base underside |
| PLUG_KEEPOUT_LENGTH | — | mm | TBD | 45 | External plug + cable-bend keep-out outside a wall |

### battery

| Parameter | Value | Unit | Status | Working (model) | Source / notes |
|---|---|---|---|---|---|
| BATTERY_BAY_WIDTH | 93.6 | mm | provisional | — | Holder-type 4S1P 21700 pack (E-POWER-002 s.11.1: 91.6 x 80.0 x 28.9 + 1 each side) |
| BATTERY_BAY_DEPTH | 82 | mm | provisional | — | Holder-type 4S1P pack (E-POWER-002 s.11.1) |
| BATTERY_BAY_HEIGHT | 31 | mm | provisional | — | Holder-type 4S1P pack (E-POWER-002 s.11.1) |
| POWER_ELEC_WIDTH | — | mm | TBD | 90 | Power board + 12 V regulator + fuse access zone, X |
| POWER_ELEC_DEPTH | — | mm | TBD | 45 | Power zone, Y |
| POWER_ELEC_HEIGHT | — | mm | TBD | 16 | Power zone, Z: tallest part 12 (E-POWER-002 s.11.2) + PCB + standoff; was 20 working |

## Historical P0.1 record (frozen 2026-10-02)

> **History, not the V1 design.** Everything below is the mechanical specification as it stood at commit `f9166d7`, before the Virtual V1 sprint. It matches `CAD/parameters/history/nomad_P0.1_2026-10-02.yaml`, which the P0.1 FeatureScript files and study scripts read. Headings are demoted one level; the text is otherwise unchanged.

### Master parameters

#### Body

| Parameter | Value | Status | P0.1 working input | Source / notes |
|---|---|---|---|---|
| BODY_WIDTH | TBD | TBD | = KEYBOARD_WIDTH + 2 × (BASE_SIDE_MARGIN + WALL_THICKNESS) → 301 | Driven by keyboard width + walls, and by the trackpad layout (D-003) |
| BODY_DEPTH | TBD | TBD | = BASE_FRONT_MARGIN + TRACKPAD_DEPTH + TRACKPAD_KEYBOARD_GAP + KEYBOARD_DEPTH + BASE_REAR_ZONE_DEPTH → 235 | Driven by keyboard + trackpad + hinge + port zones |
| BODY_HEIGHT | TBD | TBD | 40 | Placeholder until the Pi stack, cooling and battery are enveloped |
| WALL_THICKNESS | TBD | TBD | 2.5 | PETG FDM, ~6 perimeters at 0.4 mm; set during P0.1 |
| SERVICE_PANEL_THICKNESS | TBD | TBD | 2.5 | Bottom service panel and battery door plates (Round C) |
| MOUNT_PLATE_THICKNESS | TBD | TBD | 2.0 | Keyboard tray, trackpad tray and compute sled plates (Round C) |
| INPUT_TRAY_LIP | TBD | TBD | 3 | Keyboard/trackpad tray margin beyond the module outline, front and rear (Round C) |
| TRACKPAD_BAY_MARGIN | TBD | TBD | 5 | Trackpad edge to the trackpad-bay bulkhead (Round C) |
| BOSS_DIAMETER | TBD | TBD | 7 | Shell fastener boss outer diameter; the insert hole follows INSERT_SIZE (TBD) (Round C) |
| TRAY_POST_DIAMETER | TBD | TBD | 5 | Keyboard-tray posts and panel standoffs under the keyboard tray (Round C) |
| HINGE_MOUNT_WIDTH | TBD | TBD | 28 | Reserved hinge-mount volume at each rear corner, across X. Hinge hardware TBD (D-006, Round C) |
| HINGE_MOUNT_DEPTH | TBD | TBD | 21 | Reserved hinge-mount volume at each rear corner, along Y from the rear inner face (D-006, Round C) |
| BASE_SIDE_MARGIN | TBD | TBD | 8 | Keyboard edge to inner side wall |
| BASE_FRONT_MARGIN | TBD | TBD | 15 | Base front face to trackpad front edge (includes wall) |
| BASE_REAR_ZONE_DEPTH | TBD | TBD | 30 | Keyboard rear edge to base rear face: hinge + rear port zone |
| HINGE_AXIS_OFFSET | TBD | TBD | 0 | Hinge axis inset from the base rear face (negative = behind it). Working input follows the D-006 provisional rear-face hinge direction; the exact position is TBD |
| HINGE_AXIS_HEIGHT | TBD | TBD | 0 | Hinge axis height above the base top surface. Exact Z is TBD (mechanism prototype). With a 2.0 closed gap at inset 0, heights 0–2 give 1.41 mm minimum clearance and heights ≥ 4 give 2.0 (A.2b) |
| HINGE_BARREL_DIAMETER | TBD | TBD | 8 | Representative hinge knuckle envelope on the hinge axis (Round E digital prototype). Visualization only; hinge hardware TBD |

#### Lid

`LID_CLOSED_GAP` and `LID_ANGLE_*` (display hinge) apply to V1.

The class-A stack rows are **Architecture A, SUPERSEDED / DEFERRED FOR NOMAD V1** (D-010). These are `LID_THICKNESS` as formulated, and `LID_BACK_GAP` to `LID_RIB_HEIGHT`. They are kept so the A studies and the Round E prototype reproduce. The B1 lid is in [Lid (B1)](#lid-b1--active-v1-architecture-d-010).

| Parameter | Value | Status | P0.1 working input | Source / notes |
|---|---|---|---|---|
| LID_THICKNESS | TBD | TBD | = DISPLAY_BEZEL_LIP + DISPLAY_THICKNESS + MIN_GAP + SOLAR_RAIL_LAYER_HEIGHT + MIN_GAP + SOLAR_CASSETTE_THICKNESS + LID_BACK_GAP + LID_REAR_SHELL_DEPTH → 37.6 | **Architecture A (class-A lid): SUPERSEDED / DEFERRED FOR V1.** The B1 stack (core + vented gap + leaf, ~31 EST) is not yet re-baselined (V1 step 7). *History:* enclosed-lid stack, Round D.1 class A (sandwich rear shell); was PROVISIONAL — PENDING P0.2 PHYSICAL VALIDATION. Replaced the Round A placeholder 25 |
| LID_BACK_GAP | TBD | TBD | 2.0 | Stowed cassette to rear-shell clearance; the shell may deflect ≤ half of it (Round D / D.1) |
| LID_REAR_SHELL_DEPTH | TBD | TBD | 6.6 | Class A sandwich rear shell (skin + core + skin), sized at the D.1 criterion; = P0.2 coupon B-S30. Pending P0.2 |
| LID_SANDWICH_SKIN | TBD | TBD | 1.2 | Class A sandwich skins (D.1, P0.2) |
| LID_SANDWICH_WEB | TBD | TBD | 2.0 | Class A sandwich webs (D.1, P0.2) |
| LID_SANDWICH_WEB_SPACING | TBD | TBD | 30 | Class A web pitch (D.1; P0.2 compares 30 and 20) |
| LID_EDGE_BAND | TBD | TBD | = (BODY_DEPTH − SOLAR_CASSETTE_HEIGHT) / 2 − MIN_GAP − WALL_THICKNESS → 14 | Lid front/rear edge bands beside the cassette bay: rear-shell seat and screws (B.2 / D) |
| LID_MID_PLATE_THICKNESS | TBD | TBD | 2.0 | Class B (modular rail module) mid-plate, D.1. Round E visualization variant only |
| LID_RIB_SKIN | TBD | TBD | 2.5 | Class C (ribbed rear shell) skin, D.1. Round E visualization variant only |
| LID_RIB_HEIGHT | TBD | TBD | 8.5 | Class C external rib height at 30 mm pitch, D.1. Round E visualization variant only |
| LID_CLOSED_GAP | TBD | TBD | 2.0 | *Geometric* closed-lid standoff between the base top surface and the lid display face (e.g. bumpers). Not the same as MIN_GAP, which is the clearance *requirement*. The 2.0 working value gives ~1.0 mm modeled margin (D-006, A.2b) |
| LID_ANGLE_NOMINAL | TBD | TBD | 105° | Nominal open pose for checks |
| LID_ANGLE_MAX | TBD | TBD | 135° | Maximum open pose for checks |

#### Display

| Parameter | Value | Status | P0.1 working input | Source / notes |
|---|---|---|---|---|
| DISPLAY_DIAGONAL | 10.1 in (256.5) | provisional | — | Spec target |
| DISPLAY_ACTIVE_WIDTH | 217.5 | derived | — | 256.5 × 16/√(16²+10²) |
| DISPLAY_ACTIVE_HEIGHT | 136.0 | derived | — | 256.5 × 10/√(16²+10²) |
| DISPLAY_WIDTH | TBD | TBD | 235 | Module outline; SKU not locked. Working input = active area + ~9 mm border, not from a datasheet |
| DISPLAY_HEIGHT | TBD | TBD | 150 | Module outline; SKU not locked. Working input = active area + ~7 mm border, not from a datasheet |
| DISPLAY_THICKNESS | TBD | TBD | 5 | Panel only; controller not yet placed |
| DISPLAY_VERTICAL_OFFSET | TBD | TBD | 0 | Display centre offset from lid centre, positive toward the lid free edge; 0 = centred |
| DISPLAY_BEZEL_LIP | TBD | TBD | 1 | Front retention lip over the display border; 0 = flush, clip-retained (Round D) |
| DISPLAY_CONTROLLER_THICKNESS | TBD | TBD | 12 | Display-controller envelope height incl. connectors; location (lid band or base) not decided (Round D). Envelope only |

#### Controls

| Parameter | Value | Status | P0.1 working input | Source / notes |
|---|---|---|---|---|
| KEYBOARD_WIDTH | 280 | provisional | — | Spec target (SKU not locked) |
| KEYBOARD_DEPTH | 105 | provisional | — | Spec target |
| KEYBOARD_THICKNESS | ≤ 8 | provisional | — | Spec target (preferred maximum) |
| TRACKPAD_WIDTH | TBD | TBD | 86 | TBD until module selected (D-003). Reference: Perixx PERIPAD-501 II candidate ~86 |
| TRACKPAD_DEPTH | TBD | TBD | 75 | Same; reference ~75 |
| TRACKPAD_THICKNESS | TBD | TBD | 13 | Same; reference ~13 |

#### Layout (D-003)

The keyboard and trackpad are centred on the chassis longitudinal centreline, with the trackpad below the keyboard. Their positions are parameters, so they can move without restructuring the chassis.

| Parameter | Value | Status | P0.1 working input | Source / notes |
|---|---|---|---|---|
| KEYBOARD_LATERAL_OFFSET | TBD | TBD | 0 | Design intent: 0 = centred on the chassis centreline |
| TRACKPAD_LATERAL_OFFSET | TBD | TBD | 0 | Design intent: 0 = centred on the chassis centreline |
| TRACKPAD_KEYBOARD_GAP | TBD | TBD | 10 | Gap between the keyboard and the trackpad below it |
| KEYBOARD_TOP_RECESS | TBD | TBD | 1 | Keyboard top surface below the base top surface |
| TRACKPAD_TOP_RECESS | TBD | TBD | 1 | Trackpad top surface below the base top surface |

#### Computer, storage and GNSS

| Parameter | Value | Status | P0.1 working input | Source / notes |
|---|---|---|---|---|
| PI_WIDTH | 85 | provisional | — | Raspberry Pi 5, approximate board outline |
| PI_DEPTH | 56 | provisional | — | Same |
| PI_STACK_HEIGHT | TBD | TBD | 30 | Pi 5 + Active Cooler + M.2 HAT+ + 2230 NVMe incl. standoffs, above the compute sled. Conservative placeholder (inferred ~25–28, not measured); the GNSS board is assumed **not** stacked |
| PI_ENVELOPE_MARGIN | TBD | TBD | 4 | Pi board outline to its conservative envelope, each side: connector overhang + fit (Round C) |
| PI_HAT_ZONE_HEIGHT | TBD | TBD | 10 | Top part of the PI_STACK_HEIGHT envelope shown as the M.2 HAT+ / NVMe zone (Round E). Visual subdivision only; not measured; changes no clearance |
| COMPUTE_POWER_WIDTH | TBD | TBD | 50 | Compute-bay power conversion (Pi 5 V supply) envelope, X (Round C) |
| COMPUTE_POWER_DEPTH | TBD | TBD | 30 | Same, Y |
| COMPUTE_POWER_HEIGHT | TBD | TBD | 15 | Same, Z |
| COOLING_DUCT_DEPTH | TBD | TBD | 20 | Reserved intake/fan/duct volume ahead of the Pi stack, Y. Thermal design not done (Round C) |
| GNSS_MODULE_WIDTH | TBD | TBD | 70 | GNSS module envelope, X; SparkFun Flex pHAT class ~65 × 30 (Round C) |
| GNSS_MODULE_DEPTH | TBD | TBD | 35 | Same, Y |
| GNSS_MODULE_HEIGHT | TBD | TBD | 12 | Same, Z |
| NVME_FORMAT | 2230 | provisional | — | Preferred; the SSD is not locked |
| GNSS_ANTENNA_KEEPOUT | TBD | TBD | — | Must be away from major noise sources |

#### Clearances and fasteners

| Parameter | Value | Status | P0.1 working input | Source / notes |
|---|---|---|---|---|
| CLEARANCE | TBD | TBD | 0.3 | Set from FDM test coupons |
| MIN_GAP | TBD | TBD | 1.0 | |
| MIN_WALL | TBD | TBD | 2.0 | Minimum printed wall (5 perimeters at 0.4 mm); checked, not a design input |
| CABLE_CLEARANCE | TBD | TBD | — | Set per cable from its bend radius |
| CABLE_CORRIDOR_WIDTH | TBD | TBD | 15 | Reserved internal cable-corridor cross-section width (Round C); per-cable sizing via CABLE_CLEARANCE |
| CABLE_CORRIDOR_HEIGHT | TBD | TBD | 10 | Same, height |
| FASTENER_SIZE | M3 / M2.5 | provisional | — | Standard family |
| INSERT_SIZE | TBD | TBD | — | Heat-set inserts; depends on the insert supplier |
| OVERHANG_LIMIT | TBD | TBD | — | Print-dependent |

#### Lid (B1) — active V1 architecture (D-010)

The B1 lid has three layers:
1. a thin **core** (display, controller zone, back shell);
2. a **vented air gap** with low-e foil on the core back;
3. the **solar leaf**.

The axis of the solar leaf hinge sits at the lid's top edge. The stack is about 31 mm (19 + 6 + 6, EST, D-010 Phase 2), and the B1 closed size is 301 × 235 × 73.0 (CALC). Neither is re-baselined into `LID_THICKNESS` yet (V1 step 7).

| Parameter | Value | Status | P0.1 working input | Source / notes |
|---|---|---|---|---|
| LID_CORE_THICKNESS | TBD | TBD | 19 | B1 lid core: bezel lip + display + gap + controller zone + thin back shell (1 + 5 + 1 + 8 + 4, EST). Display and controller not selected |
| SOLAR_LEAF_AIR_GAP | TBD (min) | TBD | 6 | Vented gap between the lid back and the panel back, with low-e foil. Phase 2 §13 recommends ≥ 6 as a requirement; EST thermal model, not tested |

#### Solar leaf (B1) — active V1 architecture (D-010)

- **Leaf:** one leaf behind the display lid, hinged at the lid top edge.
- **Hinges:** two structural friction hinges. TorqMaster **SB-188-SB-261-6** is the current selected hinge **candidate**, subject to physical validation.
- **Cable:** a dedicated sleeve near the hinge axis, R12 minimum bend radius.
- **Stay:** a mandatory rear outrigger stay.
- **Panel:** Voltaic P108 is the **candidate**.

Records:
- **Engineering record and coupon:** `prototypes/B1_SB261/`.
- **Architecture study:** `prototypes/P0.1/d010/d010_solar_architecture_phase2.md`.
- **Frame:** the closed-lid frame of `CAD/tools/d010_phase2_study.py`.

Nothing here is physically validated.

| Parameter | Value | Status | P0.1 working input | Source / notes |
|---|---|---|---|---|
| SOLAR_LEAF_ANGLE_MAX | 190° | provisional | — | Owner target (D-010): approximately 0–190° usable leaf motion. Scratch kernel: ≥ 2.03 mm leaf-to-lid at 190°, first contact at 201° |
| SOLAR_LEAF_CABLE_BEND_RADIUS | ≥ 12 | provisional | — | Owner concept (D-010): R12 minimum bend radius for static bends (3 × *d* of the assumed Ø4 cable). Phase 2 assumed 6 × *d* for repeated flex. The moving sections are axial twist zones (≤ 3.5°/mm). Cable not selected |
| SOLAR_LEAF_HINGE_AXIS_INSET | TBD | TBD | 4.0 | Leaf hinge axis from the lid top edge (SB-261 scratch rail; kernel-checked, not tested) |
| SOLAR_LEAF_HINGE_AXIS_HEIGHT | TBD | TBD | 2.5 | Leaf hinge axis above the lid-back face (scratch rail: axis z 63.5, lid back z 61) |
| SOLAR_LEAF_HINGE_SPACING | TBD | TBD | 230 | Distance between the two leaf hinge centres (scratch rail x = ±115). Hinge candidate SB-188-SB-261-6: 33.8 long, barrel Ø7.05 (IGES) |
| SOLAR_LEAF_WIDTH | TBD | TBD | 289 | Leaf outline X: panel 273 + 2 × 8 frame (Phase 2); follows the panel selection |
| SOLAR_LEAF_DEPTH | TBD | TBD | = BODY_DEPTH → 235 | Leaf outline Y = lid depth (Phase 2). The SB-261 scratch rail starts the leaf frame at y 9 |
| SOLAR_LEAF_THICKNESS | TBD | TBD | 6 | Leaf frame: 4 mm panel in a rebate under a 2 mm lip (Phase 2, EST) |
| SOLAR_PANEL_WIDTH | TBD | TBD | 273 | Panel not selected. Voltaic P108 candidate: 273 (VENDOR) |
| SOLAR_PANEL_DEPTH | TBD | TBD | 223 | Same; P108: 223 (VENDOR) |
| SOLAR_PANEL_THICKNESS | TBD | TBD | 4 | Same; P108: 4, ETFE on 2 mm FR4 (VENDOR) |
| SOLAR_STAY_REACH | TBD | TBD | 105 | Rear outrigger stay reach behind the base (Phase 2 §11: ≥ 90 recommended, 105 modelled). Mandatory for B1; design details TBD |

#### Solar (Architecture A) — SUPERSEDED / DEFERRED FOR NOMAD V1

> **SUPERSEDED / DEFERRED FOR NOMAD V1 (D-010, 2026-10-01).** These rows describe Architecture A: two sliding/tilting cassettes (D-004 / D-009). B1 was selected as the active V1 architecture. The rows and the YAML values are kept unchanged as the A-path engineering record (the A studies and the Round E E2 lid read them). They do not describe the V1 design.

Working inputs follow the Round B.1 **V1 + minimal fixes** geometry (the only solar layout that passed B.1), adopted as working values for Round E. The Round B values they replace (carriage 12, deploy clearance 5, hub at the cassette centre) stay pinned inside the Round B / B.1 study scripts, so those reports still reproduce.

| Parameter | Value | Status | P0.1 working input | Source / notes |
|---|---|---|---|---|
| SOLAR_CASSETTE_WIDTH | TBD | TBD | = (BODY_WIDTH − 2 × WALL_THICKNESS − MIN_GAP) / 2 → 147.5 | Bounded by the lid width (two cassettes side by side) |
| SOLAR_CASSETTE_HEIGHT | TBD | TBD | 200 | Bounded by the lid height |
| SOLAR_CASSETTE_THICKNESS | TBD | TBD | 8 | Panel + frame; depends on the panel selection |
| SOLAR_ROTATION_LIMIT | ±60° to ±75° | provisional | — | D-004 target range, ± about the rotation axis |
| SOLAR_ROTATION_AXIS | slide direction | provisional | — | D-004: approximately along the slide/deployment direction; exact geometry subject to P0.1 validation |
| SOLAR_DEPLOY_CLEARANCE | TBD | TBD | = SOLAR_CABLE_DIAMETER + 2 × MIN_GAP → 8 | Cassette inboard edge to lid side wall when fully deployed; room for the tilt-joint cable zone (B.1 fix; was 5) |
| SOLAR_SLIDE_TRAVEL | TBD | TBD | = SOLAR_CASSETTE_WIDTH + WALL_THICKNESS + SOLAR_DEPLOY_CLEARANCE → 158 | D-004: lateral outward deployment from the lid (deployed span 612) |
| SOLAR_RAIL_ENGAGEMENT | TBD | TBD | 40 | Carriage length retained in the rail at full deployment |
| SOLAR_CARRIAGE_WIDTH | TBD | TBD | = SOLAR_RAIL_SLOT_WIDTH + 2 × WALL_THICKNESS → 22.6 | Carriage cross-section across the lid depth (Y), retained under the bracket slot by WALL_THICKNESS lips each side (B.1 fix; was 12) |
| SOLAR_CARRIAGE_HEIGHT | TBD | TBD | 8 | Carriage cross-section through the lid thickness (Z); the rail envelope adds WALL_THICKNESS each side |
| SOLAR_HUB_LINK_LENGTH | TBD | TBD | = WALL_THICKNESS + SOLAR_DEPLOY_CLEARANCE + MIN_GAP → 11.5 | Carriage outboard end to cassette inboard edge, so the carriage stays MIN_GAP inside the lid wall at full deployment |
| SOLAR_HUB_AXIS_OFFSET_Y | TBD | TBD | = SOLAR_CASSETTE_HEIGHT / 2 + SOLAR_RAIL_WIDTH / 2 + SOLAR_CABLE_CORRIDOR / 2 − SOLAR_HUB_CABLE_OFFSET → 114.3 | Hub axis from the cassette's free-edge-side edge, right cassette; the left hub mirrors about the cassette centre line (85.7). B.1 V1 + fixes: pin beside the cable, rails staggered around the corridor |
| SOLAR_HUB_AXIS_OFFSET_Z | TBD | TBD | = WALL_THICKNESS + MIN_GAP + SOLAR_BRACKET_WALL + SOLAR_HUB_PIN_DIAMETER / 2 − (SOLAR_RAIL_LAYER_HEIGHT + MIN_GAP) → −5.5 | Hub axis from the cassette's rail-side face; negative = into the rail layer. F3 fix (Round E, option B): axis at rail floor + MIN_GAP + bracket wall + pin radius, so the hub bracket clears the rail floor by MIN_GAP; the carriage carries a boss in the rail slot above the pin. Was −7.5 (B.1 rail mid-height) |
| SOLAR_RAIL_SLOT_WIDTH | TBD | TBD | = SOLAR_BRACKET_WIDTH + 2 × CLEARANCE → 17.6 | Rail top slot passing the hub bracket (B.1 fix) |
| SOLAR_RAIL_WIDTH | TBD | TBD | = SOLAR_CARRIAGE_WIDTH + 2 × WALL_THICKNESS → 27.6 | Rail C-channel envelope across the lid depth (B.1) |
| SOLAR_RAIL_LAYER_HEIGHT | TBD | TBD | = SOLAR_CARRIAGE_HEIGHT + 2 × WALL_THICKNESS → 13 | Rail C-channel envelope through the lid thickness = the solar rail layer (B.1, Round D) |
| SOLAR_BRACKET_WIDTH | TBD | TBD | = SOLAR_HUB_PIN_DIAMETER + MIN_GAP + SOLAR_CABLE_DIAMETER + 2 × WALL_THICKNESS → 17 | Hub bracket enclosing pin + cable side by side (B.1 fix) |
| SOLAR_BRACKET_LENGTH | TBD | TBD | 10 | Hub bracket length along the tilt axis (B.1 envelope) |
| SOLAR_BRACKET_WALL | TBD | TBD | = WALL_THICKNESS → 2.5 | Hub bracket wall around the pin bore; structural in the deployed load path; sets the F3 vertical budget (Round E, option B) |
| SOLAR_HUB_CABLE_OFFSET | TBD | TBD | = (MIN_GAP + SOLAR_CABLE_DIAMETER) / 2 → 3.5 | Carriage/rail centre offset from the pin toward the cable (B.1 fix) |
| SOLAR_CABLE_DIAMETER | TBD | TBD | 6 | Protected solar-lead envelope (B.1); not a cable selection |
| SOLAR_CABLE_BEND_RADIUS | TBD | TBD | 20 | Solar-lead service-loop bend-radius envelope (B.1); not a cable selection |
| SOLAR_CABLE_CORRIDOR | TBD | TBD | = SOLAR_CABLE_DIAMETER + 2 × MIN_GAP → 8 | Cable corridor between the staggered rails (B.1 fix) |
| SOLAR_INDEX_STEP | TBD (deg) | TBD | 15° | D-004: discrete indexed positions with a positive lock |
| SOLAR_HUB_PIN_DIAMETER | TBD | TBD | 5 | D-004: dedicated metal hub/pin carries the rotational load |

##### Solar tilt index lock and hub-pin anti-rotation (D-009, Round E; Architecture A — SUPERSEDED / DEFERRED FOR V1)

Architecture approved 2026-09-28 (design basis: `prototypes/P0.1/round_e_solar_index_lock_investigation.md`, `…_manufacturing_check.md`, `round_e_solar_hub_pin_anti_rotation_check.md`; implementation record: `round_e_solar_index_lock_implementation.md`).

- **Index lock:** a spring-loaded hardened Ø1.5 index pin in the cassette engages 1 of 11 reamed holes (15° steps, −75…+75°) in a stainless index plate keyed to the hub-pin tip. The pin works in double shear between a stainless counter sleeve (inboard) and a printed guide bore (outboard). It is released one-handed by a thumb slider, and the stroke clears the pin MIN_GAP from the plate. The spring only seats the pin and never carries torque.
- **Anti-rotation and retention:** the Ø5 hub pin is round through the carriage, link and bracket bore. It has a 3.0 A/F double-D only at its two ends.
  - At the inboard end, a stainless anti-rotation plate captured in a carriage slot and a Ø3 dowel carry the torque into the carriage. The plate and the M2 screw + washer also fix the pin axially (float +0.1/−0).
  - At the tip, the same double-D keys the index plate, retained by an M2 screw + washer.
- **Stow interlock:** only 0° can slide back into the lid (modeled: any other index position is blocked within about 7 mm).
- **±80° hard stops:** required, but **not packaged**. No stop within the approved parts and envelope reaches SF 2 (open decision, `SOLAR_TILT_STOP_ANGLE` unresolved; options S1 outboard stop / S2 cable re-route / S3 interim waiver in the implementation record §8).
- **Materials:**
  - Index pin: ISO 8734 hardened, m6.
  - Plates: stainless with σy ≥ 500 MPa (301 ½-hard or 17-4PH; not annealed 304/316), 1.5 mm; holes Ø1.60 +0.04/0, drilled + reamed, true position Ø0.06 to the key.
  - Hub pin: 303/304 cold-drawn (σy ≥ 415, not annealed).
  - Anti-rotation dowel: ISO 2338 m6 A1/A2 or ISO 8734.
  - Counter sleeve: stainless OD 2.50 h7 / ID 1.60 +0.05/0.

| Parameter | Value | Status | P0.1 working input | Source / notes |
|---|---|---|---|---|
| SOLAR_INDEX_RANGE | TBD (deg) | TBD | 75° | Operating tilt served by the index lock, ± (max of SOLAR_ROTATION_LIMIT) |
| SOLAR_INDEX_POSITIONS | TBD (count) | TBD | = 2 × SOLAR_INDEX_RANGE / SOLAR_INDEX_STEP + 1 → 11 | Index positions −75…+75 in 15° steps |
| SOLAR_INDEX_RADIUS | TBD | TBD | 10 | Index hole-circle radius; packaging window ≈ 9.5–10.5 |
| SOLAR_INDEX_PIN_ANGLE | TBD (deg) | TBD | 57.5° | Index pin position in the cassette frame, from the cable side toward the panel side; centres the hole arc in the window |
| SOLAR_INDEX_PIN_DIAMETER | TBD | TBD | 1.5 | Hardened dowel ISO 8734 1.5 m6 |
| SOLAR_INDEX_PIN_LENGTH | TBD | TBD | 16 | Index dowel length |
| SOLAR_INDEX_HOLE_DIAMETER | TBD | TBD | 1.6 | Index holes, counter-sleeve bore and guide bore: 1.60 +0.04/0 |
| SOLAR_INDEX_PLATE_THICKNESS | TBD | TBD | 1.5 | Stainless index plate (301 ½-hard or 17-4PH) |
| SOLAR_INDEX_PLATE_OUTER_RADIUS | TBD | TBD | 11.75 | Index plate outline radius; clears the rotating tray groove at every tilt |
| SOLAR_INDEX_GROOVE_CLEARANCE | TBD | TBD | 0.5 | Axial running clearance each side of the index plate |
| SOLAR_INDEX_GROOVE_RADIAL_CLEARANCE | TBD | TBD | 0.25 | Radial running clearance of the index plate in the tray groove |
| SOLAR_INDEX_ENGAGEMENT | TBD | TBD | 3 | Index pin tip depth in the counter sleeve |
| SOLAR_INDEX_PIN_STROKE | TBD | TBD | = SOLAR_INDEX_ENGAGEMENT + SOLAR_INDEX_GROOVE_CLEARANCE + SOLAR_INDEX_PLATE_THICKNESS + MIN_GAP → 6 | Thumb-slider stroke; the retracted tip is MIN_GAP clear of the plate |
| SOLAR_INDEX_SLEEVE_OD | TBD | TBD | 2.5 | Stainless counter sleeve pressed into the tray (wall 0.45) |
| SOLAR_INDEX_SLEEVE_LENGTH | TBD | TBD | = SOLAR_INDEX_ENGAGEMENT + MIN_GAP → 4 | Counter-sleeve length (1 mm grit reserve) |
| SOLAR_INDEX_GUIDE_LENGTH | TBD | TBD | 6 | Printed guide bore outboard of the groove |
| SOLAR_INDEX_CARRIER_LENGTH | TBD | TBD | 4 | Printed slider carrier gripping the pin's outer end |
| SOLAR_INDEX_CARRIER_WIDTH | TBD | TBD | 3.6 | Slider carrier square section |
| SOLAR_INDEX_SPRING_OD | TBD | TBD | 3.4 | Stainless compression-spring envelope (seating only) |
| SOLAR_INDEX_SPRING_POCKET_WIDTH | TBD | TBD | 3.8 | Square spring / carrier channel in the tray |
| SOLAR_INDEX_SPRING_INSTALLED_LENGTH | TBD | TBD | 12 | Spring length engaged; retracted = 12 − stroke = 6 |
| SOLAR_INDEX_SPRING_PRELOAD | TBD (N) | TBD | 0.6 | Engaged spring force (about 1.5 N retracted) |
| SOLAR_INDEX_COVER_END | TBD | TBD | 3 | Channel cover spring-seat block length |
| SOLAR_TILT_STOP_ANGLE | TBD (deg) | TBD | — (unresolved) | Required ±80° structural hard stops; not packaged; open decision |
| SOLAR_HUB_PIN_KEY_ACROSS_FLATS | TBD | TBD | 3.0 | Double-D key on both hub-pin ends, flats facing ±Y |
| SOLAR_HUB_PIN_LENGTH | TBD | TBD | = SOLAR_RAIL_ENGAGEMENT − SOLAR_ANTIROT_PLATE_INSET + SOLAR_HUB_LINK_LENGTH + SOLAR_BRACKET_LENGTH + SOLAR_INDEX_GROOVE_CLEARANCE + SOLAR_INDEX_PLATE_THICKNESS → 53.5 | Hub pin length |
| SOLAR_HUB_SCREW_HEAD_DIAMETER | TBD | TBD | 3.8 | M2 retention screw head envelope (both pin ends) |
| SOLAR_HUB_SCREW_HEAD_HEIGHT | TBD | TBD | 2 | M2 retention screw head height envelope |
| SOLAR_HUB_WASHER_DIAMETER | TBD | TBD | 5 | M2 washer clamping each plate on its double-D shoulder |
| SOLAR_HUB_WASHER_THICKNESS | TBD | TBD | 0.3 | M2 washer thickness |
| SOLAR_HUB_ACCESS_DIAMETER | TBD | TBD | = SOLAR_HUB_WASHER_DIAMETER + 2 × SOLAR_INDEX_GROOVE_RADIAL_CLEARANCE → 5.5 | Carriage access bore for the inboard M2 screw |
| SOLAR_ANTIROT_PLATE_INSET | TBD | TBD | 10 | Anti-rotation plate position from the carriage inboard face |
| SOLAR_ANTIROT_PLATE_THICKNESS | TBD | TBD | = SOLAR_INDEX_PLATE_THICKNESS → 1.5 | Same stock and process as the index plate |
| SOLAR_LOCK_SLOT_CLEARANCE | TBD | TBD | 0.1 | Printed slot clearance around captured plates, carrier and tab |
| SOLAR_ANTIROT_LIGAMENT | TBD | TBD | 1.3 | Anti-rotation plate ligament around the key |
| SOLAR_ANTIROT_SKIN | TBD | TBD | 0.5 | Carriage floor skin under the anti-rotation slot |
| SOLAR_ANTIROT_CABLE_WALL | TBD | TBD | 0.6 | PETG wall between the anti-rotation slot and the cable envelope (≥ 0.5 required) |
| SOLAR_ANTIROT_DOWEL_DIAMETER | TBD | TBD | 3 | Anti-rotation dowel |
| SOLAR_ANTIROT_DOWEL_LENGTH | TBD | TBD | 24 | Anti-rotation dowel length (recessed MIN_GAP from the carriage inboard face) |
| SOLAR_ANTIROT_DOWEL_OFFSET_Y | TBD | TBD | 5 | Dowel offset from the pin axis, away from the cable |
| SOLAR_ANTIROT_DOWEL_OFFSET_Z | TBD | TBD | −2.5 | Dowel offset from the pin axis, Z |
| SOLAR_ANTIROT_PUSHOUT_DIAMETER | TBD | TBD | 2 | Service push-out hole behind the dowel |

Solar kinematics of Architecture A (D-004, superseded for V1): each cassette slides laterally out of the lid, then tilts independently about an axis approximately along its slide direction. The rail carries deployment and structural loads, and the hub/pin carries rotational load. Printed gears position and actuate only. Rotation is locked at discrete indexed positions, with no motors, no continuous rotation and no slip ring.

#### I/O (Round C)

The external connector set is **not** locked. Ports sit on replaceable port-panel plates in notches in the rear wall (open to the underside, so a panel slides in from below).

| Parameter | Value | Status | P0.1 working input | Source / notes |
|---|---|---|---|---|
| PORT_PANEL_WIDTH | TBD | TBD | 90 | Each port-panel aperture, X |
| PORT_PANEL_HEIGHT | TBD | TBD | 15 | Aperture height, Z. Bounded by the lid sweep behind the base (D-006); see the base V0.1 report |
| PORT_PANEL_BOTTOM | TBD | TBD | 4 | Connector-zone bottom above the base underside |
| PORT_PANEL_INSET | TBD | TBD | 20 | Aperture inner edge from the centreline, X |
| PORT_KEEPOUT_DEPTH | TBD | TBD | 25 | Minimum internal connector depth behind a panel |
| PLUG_KEEPOUT_LENGTH | TBD | TBD | 45 | External plug + cable-bend keep-out behind the rear face |

#### Battery and power

| Parameter | Value | Status | P0.1 working input | Source / notes |
|---|---|---|---|---|
| BATTERY_BAY_WIDTH | TBD | TBD | 90 | Reserve only; capacity comes from measured power draw. No pack, cell format or voltage chosen |
| BATTERY_BAY_DEPTH | TBD | TBD | 82 | Reserve only |
| BATTERY_BAY_HEIGHT | TBD | TBD | 30 | Reserve only |
| POWER_ELEC_WIDTH | TBD | TBD | 90 | Power-electronics envelope, X (BMS / charger / solar input / DC-DC); modules not selected (Round C) |
| POWER_ELEC_DEPTH | TBD | TBD | 45 | Same, Y |
| POWER_ELEC_HEIGHT | TBD | TBD | 20 | Same, Z |

### Base V0.1 architecture (Round C, proposed D-007)

Engineering envelope model only; layout and results in `prototypes/P0.1/base_v01_architecture.md` (model `CAD/tools/base_v01_layout.py`, FeatureScript `nomadBuildBaseV01`). Summary:

- **Structure:** one printed shell (walls + top deck with keyboard/trackpad openings + bulkheads + fastener bosses), printed deck-down. The bottom is closed by a removable main service panel and a separate battery door. Keyboard tray, trackpad tray and compute sled are separate plates.
- **Bays:** right palm-rest bay = compute (Pi stack on a replaceable sled, cooling duct in front, exhaust in the right wall); left palm-rest bay = battery reserve behind its own door; under the keyboard = power electronics (left), GNSS (centre-left), compute power conversion (right) and the cable trunk; rear zone = hinge-mount reserves at both corners, two port-panel notches and the display-cable riser on the centreline.
- **Service:** every electronics reserve comes out straight down through the main panel; the battery through its door; keyboard and trackpad lift out upward. No reserve sits behind permanent geometry.

### Mandatory reserved volumes (P0.1)

- Display: panel, controller, cable exit, bezel, mounting, hinge interface
- Pi 5 + M.2 HAT+ + NVMe
- GNSS board + antenna keep-out
- Cooling: heatsink, fan, intake, exhaust, airflow corridors, fan service access
- Power electronics: mounting, airflow, cable space, service access, revision margin
- Battery: removable, serviceable bay (never sealed)
- Port zones: USB-C, 2–3 × USB-A, HDMI, audio, Ethernet, GPIO, microSD, power, expansion
- Cable corridors for every important cable
- Service-panel zones that never block airflow
- Solar (B1, D-010):
  - the leaf on the lid back, with its 0–190° sweep envelope
  - the vented air gap and foil
  - the two leaf hinges and the cable sleeve and twist zone
  - the stay (stowed under the base and deployed behind it)
  - the shared display-hinge cable pass
  - (Architecture A's cassette storage and deployment envelope are superseded.)
