# Mechanical Specification — NOMAD V1

Revision: P0.1 (draft). No values below are locked.

## Parameter status legend

| Status | Meaning |
|---|---|
| **verified** | Measured on the physical part, or taken from a manufacturer datasheet for a locked SKU |
| **derived** | Calculated from other values (the calculation is shown) |
| **provisional** | A working value from a candidate part or the spec target. Expect it to change. |
| **TBD** | No value yet. It needs a decision, a part selection or a measurement. |

All dimensions are in mm unless noted.

## Master parameters

### Body

| Parameter | Value | Status | Source / notes |
|---|---|---|---|
| BODY_WIDTH | TBD | TBD | Driven by keyboard width + walls, and by the trackpad layout decision (D-003) |
| BODY_DEPTH | TBD | TBD | Driven by keyboard + trackpad + hinge + port zones |
| BODY_HEIGHT | TBD | TBD | Driven by the Pi + HAT stack, cooling and battery reserve |
| WALL_THICKNESS | TBD | TBD | PETG FDM; set during P0.1 |
| SERVICE_PANEL_THICKNESS | TBD | TBD | |

### Display

| Parameter | Value | Status | Source / notes |
|---|---|---|---|
| DISPLAY_DIAGONAL | 10.1 in (256.5) | provisional | Spec target |
| DISPLAY_ACTIVE_WIDTH | 217.5 | derived | 256.5 × 16/√(16²+10²) |
| DISPLAY_ACTIVE_HEIGHT | 136.0 | derived | 256.5 × 10/√(16²+10²) |
| DISPLAY_WIDTH | TBD | TBD | Module outline; depends on the SKU (not locked) |
| DISPLAY_HEIGHT | TBD | TBD | Module outline; depends on the SKU |
| DISPLAY_THICKNESS | TBD | TBD | Module + controller board; depends on the SKU |

### Controls

| Parameter | Value | Status | Source / notes |
|---|---|---|---|
| KEYBOARD_WIDTH | 280 | provisional | Spec target (SKU not locked) |
| KEYBOARD_DEPTH | 105 | provisional | Spec target |
| KEYBOARD_THICKNESS | ≤ 8 | provisional | Spec target (preferred maximum) |
| TRACKPAD_WIDTH | 86 | provisional | Perixx PERIPAD-501 II (candidate), approximate |
| TRACKPAD_DEPTH | 75 | provisional | Same |
| TRACKPAD_THICKNESS | 13 | provisional | Same |

### Computer, storage and GNSS

| Parameter | Value | Status | Source / notes |
|---|---|---|---|
| PI_WIDTH | 85 | provisional | Raspberry Pi 5, approximate board outline |
| PI_DEPTH | 56 | provisional | Same |
| PI_STACK_HEIGHT | TBD | TBD | Pi + M.2 HAT+ + GNSS pHAT + cooler |
| NVME_FORMAT | 2230 | provisional | Preferred; the SSD is not locked |
| GNSS_ANTENNA_KEEPOUT | TBD | TBD | Must be away from major noise sources |

### Clearances and fasteners

| Parameter | Value | Status | Source / notes |
|---|---|---|---|
| CLEARANCE | TBD | TBD | Set from FDM test coupons |
| MIN_GAP | TBD | TBD | |
| MIN_WALL | TBD | TBD | |
| CABLE_CLEARANCE | TBD | TBD | Set per cable from its bend radius |
| FASTENER_SIZE | M3 / M2.5 | provisional | Standard family |
| INSERT_SIZE | TBD | TBD | Heat-set inserts; depends on the insert supplier |
| OVERHANG_LIMIT | TBD | TBD | Print-dependent |

### Solar

| Parameter | Value | Status | Source / notes |
|---|---|---|---|
| SOLAR_CASSETTE_WIDTH | TBD | TBD | Bounded by the lid width (two cassettes side by side) |
| SOLAR_CASSETTE_HEIGHT | TBD | TBD | Bounded by the lid height |
| SOLAR_CASSETTE_THICKNESS | TBD | TBD | Panel + frame; depends on the panel selection |
| SOLAR_ROTATION_LIMIT | ±60° to ±75° | provisional | Spec range; the rotation axis is open (D-004) |

### Battery

| Parameter | Value | Status | Source / notes |
|---|---|---|---|
| BATTERY_BAY_WIDTH | TBD | TBD | Reserve only; capacity comes from measured power draw |
| BATTERY_BAY_DEPTH | TBD | TBD | |
| BATTERY_BAY_HEIGHT | TBD | TBD | |

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
