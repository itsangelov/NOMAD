# NOMAD Mechanical V0.1 — Base Chassis Architecture (Round C)

**Status:** engineering envelope model, **proposed** (D-007, awaiting the owner). Not a cosmetic enclosure and not a hardware design. Every dimension is a TBD parameter with a working value in `CAD/parameters/nomad.yaml`.

**Evidence levels:**
- *Modeled*: exact local geometry model, cross-checked in the Onshape kernel (scratch Part Studio, not the NOMAD document).
- *Inferred*: engineering judgement, not computed.
- Nothing here is *physically tested* or *measured*.

**Sources:**
- Model and checks: `CAD/tools/base_v01_layout.py`, the single layout spec. It generates the FeatureScript layout block in `CAD/featurescript/NOMAD_P01.fs` and the kernel harness data.
- FeatureScript builder: `nomadBuildBaseV01`; production feature "NOMAD Base V0.1".
- Kernel harness: `CAD/featurescript/NOMAD_P01.basev01.test.fs`.

Regenerate and re-check:

```bash
py CAD/tools/base_v01_layout.py --write
```

## 1. Assessment before changes

### Current constraints relevant to the chassis

| Item | Value | Standing |
|---|---|---|
| Body envelope | 301 × 235 × 40 | **working** (BODY_WIDTH/DEPTH formulas, BODY_HEIGHT 40 placeholder); unchanged by this round |
| Keyboard | 280 × 105 × ≤ 8, top 1 below the deck, centred (D-003) | provisional values; unchanged |
| Trackpad | 86 × 75 × 13 reference (Perixx), centred below the keyboard, gap 10 | TBD / working (D-003); unchanged |
| Walls | 2.5 | working |
| Hinge | axis at the base rear top edge (inset 0, height 0) | D-006 provisional direction; exact axis and hardware TBD |
| Closed-lid gap | 2.0 working (MIN_GAP 1.0 requirement) | D-006 |
| Lid | 25 thick (Round A), 105° / 135° poses | working |
| Pi 5 | 85 × 56 board | provisional |
| Fasteners | M3 / M2.5 family, heat-set inserts | provisional; INSERT_SIZE TBD |

### Still TBD

All body, lid, trackpad, clearance, battery and I/O dimensions; PI_STACK_HEIGHT; INSERT_SIZE; CABLE_CLEARANCE; GNSS_ANTENNA_KEEPOUT; OVERHANG_LIMIT; every hinge dimension and piece of hardware; every component SKU except the Pi 5.

### P0.1 decisions preserved

- D-002: parameters live in YAML.
- D-003: keyboard and trackpad centred on the centreline, trackpad below, positions parameterized.
- D-006: rear-face hinge direction, 2.0 closed gap.
- D-004: solar is untouched in this round.
- Test coupons: untouched.

### Conflicts found between the spec and the full-chassis goal

1. **Height budget.**
   - With BODY_HEIGHT 40, the space under the keyboard is only **26.5** (service panel 2.5 up to the tray underside at 29).
   - A conservative Pi 5 + Active Cooler + M.2 HAT+ + 2230 stack is ~25–28 (inferred), plus airflow. It does not fit under the keyboard.
   - Only the palm-rest regions either side of the trackpad have full height (**35**).
   - Resolved by placement (compute in the right palm-rest bay), without changing BODY_HEIGHT.
2. **GNSS pHAT stacking.**
   - `PI_STACK_HEIGHT`'s old note assumed a GNSS pHAT *in* the stack. Stacked above the M.2 HAT+, it would push the stack to ~40 (inferred).
   - **Assumption for V0.1:** the GNSS board is a separate, cabled module (ENV_GNSS_MODULE). Not a decision; flagged for the owner.
3. **Rear ports vs the D-006 rear-face hinge.**
   - At 135° the lid swings down behind the base; its lowest point (y ≈ 254) is at **Z 20.9 with the 25 mm working lid**.
   - Plugs in the rear face must stay below it. That limits the connector zone to Z 4–19, a single row of connectors.
   - It fails for the thicker lids already studied (see §6).
4. **Battery location** was open. The spec only required a removable, never-sealed bay. Placement is proposed here (D-007), not decided.

## 2. Architecture (proposed)

- **Structural shell** (`BASE_SHELL`, one printed part):
  - Perimeter walls and a top deck with keyboard and trackpad openings (0.3 fit).
  - Two trackpad-bay bulkheads, a battery-bay rear wall with a cable slot, and 15 fastener bosses.
  - It prints deck-down with no overhang or bridge (modeled check).
  - The underside is open: electronics are never built into the shell.
- **Bottom closures:**
  - `SERVICE_PANEL_MAIN` covers everything except the battery bay.
  - `BATTERY_DOOR` is separate, so a battery swap does not expose the electronics.
  - Both are screwed into bosses; the seams sit on the left bulkhead and on the battery-bay wall. No glue.
- **Mounting plates** (separate, replaceable; component hole patterns are deliberately *not* modeled):
  - `KEYBOARD_TRAY`: notched around the side bosses; four posts up to the deck; two metal `PANEL_STANDOFF`s down to the panel.
  - `TRACKPAD_TRAY`: spans between the bulkheads.
  - `COMPUTE_SLED`: carries the Pi stack, on four sled bosses.
- **Rear service region:**
  - Two replaceable port-panel plates in notches in the rear wall, open to the underside (a panel slides in from below; no bridge).
  - Hinge-mount reserves at both rear corners.
  - Display-cable riser on the centreline, exiting next to the hinge axis, where cable length change is smallest (inferred).
- **Load paths vs cables:**
  - Hinge loads go into the rear corners, walls and deck. Panel and keyboard-tray loads go into bosses and posts.
  - Cable corridors keep ≥ MIN_GAP from the hinge reserves and bosses and never pass through structure; the one exception is the battery-wall slot, which has 1 mm each side.

## 3. Component-envelope layout (working values)

| Region | Contents (all reserves, not hardware) | Where |
|---|---|---|
| A. Compute bay | `ENV_PI_STACK` 93 × 64 × 30 on `COMPUTE_SLED`; `ENV_COMPUTE_POWER` 50 × 30 × 15; cable access `CABLE_COMPUTE` | Right palm-rest bay (X 50.5–148, full 35 height); compute power under the keyboard, right |
| B. I/O / rear service | `PORT_PANEL_MAIN` (right, compute side: USB/Ethernet/HDMI), `PORT_PANEL_AUX` (left: USB-C power in, GNSS antenna, future); `KEEPOUT_PORTS_*` 27.5 deep; `KEEPOUT_PLUGS_*` 45 long outside | Rear wall, X ±20–110, connector zone Z 4–19 |
| C. Keyboard | `ENV_KEYBOARD` 280 × 105 × 8 in a deck opening, on `KEYBOARD_TRAY` | Unchanged Round A position |
| D. Trackpad | `ENV_TRACKPAD` 86 × 75 × 13 (Perixx reference only) on `TRACKPAD_TRAY`, in its own bay between bulkheads | Unchanged Round A position |
| E. Power / battery | `ENV_BATTERY_BAY` 90 × 82 × 30 behind `BATTERY_DOOR`; `ENV_POWER_ELECTRONICS` 90 × 45 × 20 directly behind it; `CABLE_BATTERY` through the bay-wall slot | Left palm-rest bay; power electronics under the keyboard, left |
| F. Cooling | `KEEPOUT_COOLING_DUCT` 84 × 20 × 31 ahead of the Pi; `KEEPOUT_VENT_INTAKE` in the front wall; `KEEPOUT_VENT_EXHAUST` in the right wall beside the Pi | Front → Pi → right side. No vents are cut; thermal performance **not** solved |
| G. Service | Main panel (compute, compute power, power electronics, GNSS, cables); battery door; keyboard/trackpad lift out upward | Underside / top |
| H. Cables | `CABLE_TRUNK` across the rear of the under-keyboard zone; `CABLE_COMPUTE`, `CABLE_POWER`, `CABLE_BATTERY`, `CABLE_TRACKPAD`, `CABLE_KEYBOARD`, `CABLE_DISPLAY` (riser to the hinge pass-through); GNSS sits on the trunk. Storage (NVMe on the M.2 HAT+) is inside the Pi stack | 15 × 10 reserved sections; no cables routed |
| GNSS | `ENV_GNSS_MODULE` 70 × 35 × 12, centre-left under the keyboard, 12.3 from the power electronics | Antenna keep-out TBD (antenna location TBD) |

## 4. Minimum new parameters (all TBD, working values only)

- **Body:**
  - MOUNT_PLATE_THICKNESS 2.0, INPUT_TRAY_LIP 3, TRACKPAD_BAY_MARGIN 5
  - BOSS_DIAMETER 7, TRAY_POST_DIAMETER 5
  - HINGE_MOUNT_WIDTH 28, HINGE_MOUNT_DEPTH 21
- **Computer:**
  - PI_ENVELOPE_MARGIN 4, COOLING_DUCT_DEPTH 20
  - COMPUTE_POWER_WIDTH / DEPTH / HEIGHT 50 / 30 / 15
  - GNSS_MODULE_WIDTH / DEPTH / HEIGHT 70 / 35 / 12
- **Clearances:** CABLE_CORRIDOR_WIDTH 15, CABLE_CORRIDOR_HEIGHT 10.
- **I/O (new group):** PORT_PANEL_WIDTH 90, PORT_PANEL_HEIGHT 15, PORT_PANEL_BOTTOM 4, PORT_PANEL_INSET 20, PORT_KEEPOUT_DEPTH 25, PLUG_KEEPOUT_LENGTH 45.
- **Battery / power:** POWER_ELEC_WIDTH / DEPTH / HEIGHT 90 / 45 / 20.
- **Working values added to existing TBD parameters:** SERVICE_PANEL_THICKNESS 2.5, PI_STACK_HEIGHT 30, BATTERY_BAY_WIDTH / DEPTH / HEIGHT 90 / 82 / 30, MIN_WALL 2.0.

No authoritative value changed. BODY_WIDTH, BODY_DEPTH, BODY_HEIGHT, keyboard and trackpad values are unchanged. The layout has no hidden length constants: every coordinate is an expression over these parameters.

## 5. Validation (modeled)

**Local model**, exact box / vertical-cylinder geometry, 34 parts, 77 primitives. All checks passed:

| Check | Result |
|---|---|
| One solid per part; all internal parts inside 301 × 235 × 40 | pass |
| Pair rules (537 pairs): no overlaps; ≥ MIN_GAP between envelopes, keep-outs, cables and structure; contact only at designed interfaces (seating, served cable entries, 0.3 keyboard/trackpad fits) | 0 violations |
| Keyboard fit / trackpad fit | 0.300 to the deck openings; seated on their trays; 3.0 below the closed display face |
| Compute-bay fit | Pi envelope 93 × 64 × 30 with 1.000 to the shell; 2.0 below the deck |
| Major separation | Pi–battery 107; battery–power electronics 4.5; power electronics–GNSS 12.3; Pi–compute power 9.0 |
| Service access (straight-down removal, footprint inside the named panel, nothing in the way) | compute (sled + Pi + duct), compute power, power electronics, GNSS: main panel; battery: door; keyboard, trackpad: upward |
| Trapped volumes | none: every reserve lies over the bottom opening with no shell below it |
| Assembly from below into the empty shell | keyboard tray, trackpad tray, compute sled, standoffs: unobstructed |
| Wall thickness | walls/deck/bulkheads 2.5, panels 2.5, plates 2.0 ≥ MIN_WALL 2.0 |
| Printability of the shell (deck-down) | every primitive chains to the deck: no overhang, no bridge |
| Vents and display pass-through clear of bosses | ≥ MIN_GAP |
| Cables vs load paths | trunk 6.5 from the hinge reserve; nothing routed through bosses or hinge reserves |
| Base/lid interface, closed | nothing above Z 40; lid clearance 2.000 |
| Hinge (D-006 working axis), lid sweep 0–135° vs every base part | min 1.414 (rear wall, as A.2): pass |
| Lid sweep vs external plug keep-outs | min 1.908 at 135°: pass with LID_THICKNESS 25 only |

**Onshape kernel cross-check** (one `test_feature` run in a scratch Part Studio; the production builder and the generated layout):

```
BV n34 L0 S0/561 c160 dv0 l2,1.932,1.414 p14.012,1.908 e0
```

- **Parts:** 34 parts, each exactly one solid.
- **Pair states:** all 561 overlap / touch / gap states identical to the local model.
- **Gaps:** 160 exact gaps compared, max deviation 0.000 mm.
- **Lid:**
  - Clearance to the base at 0° / 105° / 135°: 2.000 / 1.932 / 1.414.
  - Clearance to the plug zones at 105° / 135°: 14.012 / 1.908.
  - Identical to the local model.

## 6. Risks (architectural)

1. **Rear I/O vs hinge vs lid thickness** (modeled; the largest risk).
   - With the D-006 working axis at the rear top edge and a 135° maximum, the lid's lowest point behind the base is Z 20.9 / 16.3 / 8.5 for lids 25 / 31.5 (B.1 V1) / 42.5 (B.2 Concept C) thick.
   - The rear connector zone (top Z 19) clears only the 25 mm lid. With the thicker lids already studied, plugs would be hit at 135°.
   - Options for the owner:
     - raise HINGE_AXIS_HEIGHT;
     - reduce LID_ANGLE_MAX;
     - move ports to the side walls;
     - use right-angle plugs;
     - lower the connector zone.
   - This couples the base to the lid thickness decision still pending from B.2.
2. **Height budget.** Under the keyboard only 26.5 is available, so the Pi stack must stay in a palm-rest bay. Any taller compute, cooler or stacked GNSS forces BODY_HEIGHT up (a working value; owner decision).
3. **Heat under the palm rest** (inferred). The compute bay sits under the right palm rest; the deck above the Pi is 2 mm clear. The airflow path and skin temperature are unverified, and thermal design is not done.
4. **Front mass / tipping** (inferred). Putting the battery at the front-left helps against tipping backward with the lid open; masses are not known yet.
5. **Print size** (inferred). The shell is 301 × 235 × 40: it needs a ≥ 310 mm-class bed or a split shell, to be decided with the print service.
6. **Rear-wall stiffness** (inferred). The two port notches leave the rear wall 21 mm tall between Z 19 and the deck over 90 mm spans, between the hinge corners. It needs a structural check once hinge loads exist.
7. **GNSS noise** (inferred). The GNSS module is 12.3 from the power-electronics reserve and in the same enclosure as the Pi. Antenna placement (GNSS_ANTENNA_KEEPOUT) is still TBD.
8. **Envelope sizes are placeholders.** Battery 90 × 82 × 30 (≈ 221 cm³), power electronics and GNSS envelopes are not sized from real parts.
9. **Duplicate names in one Part Studio.** Round A's "NOMAD Base" and "NOMAD Base V0.1" both create `ENV_KEYBOARD` / `ENV_TRACKPAD`. Insert only one of them per Part Studio.

## 7. Not done in this round (by instruction)

Lid, solar integration, display mounting, final hinge hardware, Pi / GNSS mounting-hole patterns, port cut-outs, vent cut-outs, battery geometry, feet, exterior styling. The model is **not** written to the NOMAD Onshape document. Onshape changes in this round: none (one scratch `test_feature` run only).
