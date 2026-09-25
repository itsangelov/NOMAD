# Mechanical Specification — NOMAD V1

Revision: P0.1 (draft). No values below are locked.

> **Source of truth (D-002):** `CAD/parameters/nomad.yaml` holds the authoritative machine-readable parameter values. This document is the human-readable specification and must agree with it. If they differ, the YAML is correct and this document must be updated.

## Parameter status legend

| Status | Meaning |
|---|---|
| **verified** | Measured on the physical part, or taken from a manufacturer datasheet for a locked SKU |
| **derived** | Calculated from other values (the calculation is shown) |
| **provisional** | A working value from a candidate part or the spec target. Expect it to change. |
| **TBD** | No value yet. It needs a decision, a part selection or a measurement. |

## Authoritative value vs P0.1 working input

- **Value / Status** is the authoritative engineering value. For every TBD parameter it stays empty.
- **P0.1 working input** is a provisional placeholder, or a formula over other parameters, used **only** to generate P0.1 envelope geometry. It is not an engineering decision, not a verified dimension, and it does not change the parameter's TBD status.
- Geometry uses the value if one exists, otherwise the working input. Every generated constant is labelled with its source.

All dimensions are in mm unless noted.

## Master parameters

### Body

| Parameter | Value | Status | P0.1 working input | Source / notes |
|---|---|---|---|---|
| BODY_WIDTH | TBD | TBD | = KEYBOARD_WIDTH + 2 × (BASE_SIDE_MARGIN + WALL_THICKNESS) → 301 | Driven by keyboard width + walls, and by the trackpad layout (D-003) |
| BODY_DEPTH | TBD | TBD | = BASE_FRONT_MARGIN + TRACKPAD_DEPTH + TRACKPAD_KEYBOARD_GAP + KEYBOARD_DEPTH + BASE_REAR_ZONE_DEPTH → 235 | Driven by keyboard + trackpad + hinge + port zones |
| BODY_HEIGHT | TBD | TBD | 40 | Placeholder until the Pi stack, cooling and battery are enveloped |
| WALL_THICKNESS | TBD | TBD | 2.5 | PETG FDM, ~6 perimeters at 0.4 mm; set during P0.1 |
| SERVICE_PANEL_THICKNESS | TBD | TBD | — | |
| BASE_SIDE_MARGIN | TBD | TBD | 8 | Keyboard edge to inner side wall |
| BASE_FRONT_MARGIN | TBD | TBD | 15 | Base front face to trackpad front edge (includes wall) |
| BASE_REAR_ZONE_DEPTH | TBD | TBD | 30 | Keyboard rear edge to base rear face: hinge + rear port zone |
| HINGE_AXIS_OFFSET | TBD | TBD | 0 | Hinge axis inset from the base rear face (negative = behind it). Working input follows the D-006 provisional rear-face hinge direction; the exact position is TBD |
| HINGE_AXIS_HEIGHT | TBD | TBD | 0 | Hinge axis height above the base top surface. Exact Z is TBD (mechanism prototype). With a 2.0 closed gap at inset 0, heights 0–2 give 1.41 mm minimum clearance and heights ≥ 4 give 2.0 (A.2b) |

### Lid

| Parameter | Value | Status | P0.1 working input | Source / notes |
|---|---|---|---|---|
| LID_THICKNESS | TBD | TBD | 25 | Placeholder: display 5 + cassette 8 + walls 2 × 2.5 + ~7 rail/structure allowance |
| LID_CLOSED_GAP | TBD | TBD | 2.0 | *Geometric* closed-lid standoff between the base top surface and the lid display face (e.g. bumpers). Not the same as MIN_GAP, which is the clearance *requirement*. The 2.0 working value gives ~1.0 mm modeled margin (D-006, A.2b) |
| LID_ANGLE_NOMINAL | TBD | TBD | 105° | Nominal open pose for checks |
| LID_ANGLE_MAX | TBD | TBD | 135° | Maximum open pose for checks |

### Display

| Parameter | Value | Status | P0.1 working input | Source / notes |
|---|---|---|---|---|
| DISPLAY_DIAGONAL | 10.1 in (256.5) | provisional | — | Spec target |
| DISPLAY_ACTIVE_WIDTH | 217.5 | derived | — | 256.5 × 16/√(16²+10²) |
| DISPLAY_ACTIVE_HEIGHT | 136.0 | derived | — | 256.5 × 10/√(16²+10²) |
| DISPLAY_WIDTH | TBD | TBD | 235 | Module outline; SKU not locked. Working input = active area + ~9 mm border, not from a datasheet |
| DISPLAY_HEIGHT | TBD | TBD | 150 | Module outline; SKU not locked. Working input = active area + ~7 mm border, not from a datasheet |
| DISPLAY_THICKNESS | TBD | TBD | 5 | Panel only; controller not yet placed |
| DISPLAY_VERTICAL_OFFSET | TBD | TBD | 0 | Display centre offset from lid centre, positive toward the lid free edge; 0 = centred |

### Controls

| Parameter | Value | Status | P0.1 working input | Source / notes |
|---|---|---|---|---|
| KEYBOARD_WIDTH | 280 | provisional | — | Spec target (SKU not locked) |
| KEYBOARD_DEPTH | 105 | provisional | — | Spec target |
| KEYBOARD_THICKNESS | ≤ 8 | provisional | — | Spec target (preferred maximum) |
| TRACKPAD_WIDTH | TBD | TBD | 86 | TBD until module selected (D-003). Reference: Perixx PERIPAD-501 II candidate ~86 |
| TRACKPAD_DEPTH | TBD | TBD | 75 | Same; reference ~75 |
| TRACKPAD_THICKNESS | TBD | TBD | 13 | Same; reference ~13 |

### Layout (D-003)

The keyboard and trackpad are centred on the chassis longitudinal centreline, with the trackpad below the keyboard. Their positions are parameters, so they can move without restructuring the chassis.

| Parameter | Value | Status | P0.1 working input | Source / notes |
|---|---|---|---|---|
| KEYBOARD_LATERAL_OFFSET | TBD | TBD | 0 | Design intent: 0 = centred on the chassis centreline |
| TRACKPAD_LATERAL_OFFSET | TBD | TBD | 0 | Design intent: 0 = centred on the chassis centreline |
| TRACKPAD_KEYBOARD_GAP | TBD | TBD | 10 | Gap between the keyboard and the trackpad below it |
| KEYBOARD_TOP_RECESS | TBD | TBD | 1 | Keyboard top surface below the base top surface |
| TRACKPAD_TOP_RECESS | TBD | TBD | 1 | Trackpad top surface below the base top surface |

### Computer, storage and GNSS

| Parameter | Value | Status | P0.1 working input | Source / notes |
|---|---|---|---|---|
| PI_WIDTH | 85 | provisional | — | Raspberry Pi 5, approximate board outline |
| PI_DEPTH | 56 | provisional | — | Same |
| PI_STACK_HEIGHT | TBD | TBD | — | Pi + M.2 HAT+ + GNSS pHAT + cooler |
| NVME_FORMAT | 2230 | provisional | — | Preferred; the SSD is not locked |
| GNSS_ANTENNA_KEEPOUT | TBD | TBD | — | Must be away from major noise sources |

### Clearances and fasteners

| Parameter | Value | Status | P0.1 working input | Source / notes |
|---|---|---|---|---|
| CLEARANCE | TBD | TBD | 0.3 | Set from FDM test coupons |
| MIN_GAP | TBD | TBD | 1.0 | |
| MIN_WALL | TBD | TBD | — | |
| CABLE_CLEARANCE | TBD | TBD | — | Set per cable from its bend radius |
| FASTENER_SIZE | M3 / M2.5 | provisional | — | Standard family |
| INSERT_SIZE | TBD | TBD | — | Heat-set inserts; depends on the insert supplier |
| OVERHANG_LIMIT | TBD | TBD | — | Print-dependent |

### Solar

Working inputs are recorded for Round B; Round A does not use them.

| Parameter | Value | Status | P0.1 working input | Source / notes |
|---|---|---|---|---|
| SOLAR_CASSETTE_WIDTH | TBD | TBD | = (BODY_WIDTH − 2 × WALL_THICKNESS − MIN_GAP) / 2 → 147.5 | Bounded by the lid width (two cassettes side by side) |
| SOLAR_CASSETTE_HEIGHT | TBD | TBD | 200 | Bounded by the lid height |
| SOLAR_CASSETTE_THICKNESS | TBD | TBD | 8 | Panel + frame; depends on the panel selection |
| SOLAR_ROTATION_LIMIT | ±60° to ±75° | provisional | — | D-004 target range, ± about the rotation axis |
| SOLAR_ROTATION_AXIS | slide direction | provisional | — | D-004: approximately along the slide/deployment direction; exact geometry subject to P0.1 validation |
| SOLAR_DEPLOY_CLEARANCE | TBD | TBD | 5 | Cassette inboard edge to lid side wall when fully deployed |
| SOLAR_SLIDE_TRAVEL | TBD | TBD | = SOLAR_CASSETTE_WIDTH + WALL_THICKNESS + SOLAR_DEPLOY_CLEARANCE → 155 | D-004: lateral outward deployment from the lid |
| SOLAR_RAIL_ENGAGEMENT | TBD | TBD | 40 | Carriage length retained in the rail at full deployment |
| SOLAR_HUB_AXIS_OFFSET_Y | TBD | TBD | = SOLAR_CASSETTE_HEIGHT / 2 → 100 | Hub axis position across the cassette height (not a decision; D-004) |
| SOLAR_HUB_AXIS_OFFSET_Z | TBD | TBD | = SOLAR_CASSETTE_THICKNESS / 2 → 4 | Hub axis position through the cassette thickness (not a decision; D-004) |
| SOLAR_INDEX_STEP | TBD (deg) | TBD | 15° | D-004: discrete indexed positions with a positive lock |
| SOLAR_HUB_PIN_DIAMETER | TBD | TBD | 5 | D-004: dedicated metal hub/pin carries the rotational load |

Solar kinematics (D-004): each cassette slides laterally out of the lid, then tilts independently about an axis approximately along its slide direction. The rail carries deployment and structural loads, and the hub/pin carries rotational load. Printed gears position and actuate only. Rotation is locked at discrete indexed positions, with no motors, no continuous rotation and no slip ring.

### Battery

| Parameter | Value | Status | P0.1 working input | Source / notes |
|---|---|---|---|---|
| BATTERY_BAY_WIDTH | TBD | TBD | — | Reserve only; capacity comes from measured power draw |
| BATTERY_BAY_DEPTH | TBD | TBD | — | |
| BATTERY_BAY_HEIGHT | TBD | TBD | — | |

## Mandatory reserved volumes (P0.1)

- Display: panel, controller, cable exit, bezel, mounting, hinge interface
- Pi 5 + M.2 HAT+ + NVMe
- GNSS board + antenna keep-out
- Cooling: heatsink, fan, intake, exhaust, airflow corridors, fan service access
- Power electronics: mounting, airflow, cable space, service access, revision margin
- Battery: removable, serviceable bay (never sealed)
- Port zones: USB-C, 2–3 × USB-A, HDMI, audio, Ethernet, GPIO, microSD, power, expansion
- Cable corridors for every important cable
- Service-panel zones that never block airflow
- Solar cassette storage (rear of display lid) and the deployment envelope
