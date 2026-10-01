# Round E — NOMAD Digital Prototype: Progress Log

**Plan:** `round_e_implementation_plan.md`, approved 2026-09-26 with the owner decisions recorded in D-008 (`docs/decisions.md`).

**Status:** E0.5, E1 and E2 done; **F3 APPROVED AND IMPLEMENTED — OPTION B** (see the F3 implementation section below). **Stopped for review**; E3/E4 (solar mechanism implementation / validation) have not started.

**Onshape:**
- Feature Studio **`NOMAD_E_Prototype`** (element `40d4ae5868441bcb8882fe3a`) created at E1 and written three times (E1; E2 with the full E1 content unchanged plus the lid; the F3 option-B fix).
- The P0.1 coupon Feature Studio / Part Studio are untouched.
- The owner creates the Part Studio and inserts the features (connector limit).

**Local source:** `CAD/featurescript/NOMAD_E_Prototype.fs` is the exact text written to Onshape. The scratch harnesses `NOMAD_E_Prototype.test.fs` (E1) and `NOMAD_E_Prototype.e2.test.fs` (E2) are local only.

**Evidence levels:**
- Geometry and clearances: *modeled*, kernel cross-checked in scratch.
- Fastener heads: *representative*, not a selection.
- Everything else as in the source studies.

---

## E0.5 — YAML reconciliation (working values only)

**Authoritative `value` fields:** unchanged. There are 12 authoritative values; all others stay TBD.

| Change | Before | After (working / formula) | Source |
|---|---|---|---|
| LID_THICKNESS | working 25 | formula → **37.6** (lip 1 + display 5 + 1 + rail layer 13 + 1 + cassette 8 + back gap 2 + shell 6.6) | D.1 class A, **PROVISIONAL — PENDING P0.2** |
| New lid stack | — | DISPLAY_BEZEL_LIP 1, LID_BACK_GAP 2, LID_REAR_SHELL_DEPTH 6.6, LID_SANDWICH_SKIN 1.2 / WEB 2.0 / WEB_SPACING 30, LID_EDGE_BAND → 14, LID_MID_PLATE_THICKNESS 2 (B variant), LID_RIB_SKIN 2.5 / LID_RIB_HEIGHT 8.5 (C variant) | D / D.1 |
| Solar V1 + fixes | carriage 12, deploy 5, travel 155, link 8.5, hub at cassette centre | carriage → **22.6**, deploy → **8**, travel → **158**, link → **11.5**, hub Y → 114.3 (right; left mirrored 85.7), hub Z → −7.5; new SOLAR_RAIL_SLOT_WIDTH 17.6, SOLAR_RAIL_WIDTH 27.6, SOLAR_RAIL_LAYER_HEIGHT 13, SOLAR_BRACKET_WIDTH 17, SOLAR_BRACKET_LENGTH 10, SOLAR_HUB_CABLE_OFFSET 3.5, SOLAR_CABLE_DIAMETER 6, SOLAR_CABLE_BEND_RADIUS 20, SOLAR_CABLE_CORRIDOR 8 | B.1 |
| Display | — | DISPLAY_CONTROLLER_THICKNESS 12 (envelope) | D |
| Hinge | — | HINGE_BARREL_DIAMETER 8 (representative) | Round E decision 5 |
| Compute | — | PI_HAT_ZONE_HEIGHT 10 (see below) | Round E visualization |

- **`PI_HAT_ZONE_HEIGHT`** was not in the E0.5 table. It is needed to show the planned `ENV_NVME_HAT` part: it splits the existing 30 mm Pi-stack envelope into board/cooler and HAT/NVMe zones. It is not measured and changes no clearance. **Flagged for review.**
- **`mechanical-spec.md`** rows were added or updated to match; the generator's spec cross-check is clean.

**Study reproducibility:**
- Every study tool was run before and after the YAML change and the outputs were diffed.
- Three studies silently changed, because they read the working values the change replaced: A.2 (T 25), Round B (the Round B solar values) and B.1 "as specified" (carriage 12 / deploy 5). Their inputs are now **pinned** in `hinge_feasibility_2d.py`, `solar_skeleton_model.py` and `solar_v1_feasibility.py`, with dated comments.
- All of A.2, B, B.1, B.2, coupons, C.1, C.2, D, D.1 and P0.2 now reproduce their published outputs **byte for byte**.

**Known open conflict (left visible, Round E decision 4):**
- The Round C base checker (`base_v01_layout.py`) now uses the 37.6 lid. The lid enters the 45 mm rear-plug keep-out by **−7.0 mm at 135°** (h 0), exactly as C.2 / D.1 predicted.
- It is reported on every run as `OPEN CONFLICT (known …)` and is not resolved. If it ever gets worse than the documented case, it becomes a FAIL again.

**Generators:**
- `yaml_to_featurescript.py --target FILE` and `base_v01_layout.py --target FILE --harness FILE` write the same generated blocks into the Round E files.
- Default behaviour is unchanged. `NOMAD_P01.fs` and its harness were regenerated to the new values (local only).

**D-008** is recorded in `docs/decisions.md`.

---

## E1 — base and service in `NOMAD_E_Prototype`

**Features** (dialogs are visualization-only):

| Feature | Dialog | Builds |
|---|---|---|
| **NOMAD E Base** | Show keep-outs and cable envelopes (default on) | See the parts list below. **Mate connector `MC_HINGE_BASE`** is owned by BASE_SHELL, on the D-006 axis (Y 235, Z 40), Z-axis along −X (a positive angle opens the lid), angle 0 = closed |
| **NOMAD E Service** | Show representative fasteners (default on) | SERVICE_PANEL_MAIN, BATTERY_DOOR, PORT_PANEL_MAIN, PORT_PANEL_AUX, PANEL_STANDOFF_L / R; 17 representative M3 heads (11 panel, 2 door, 4 compute sled) in Ø6.2 × 1.9 counterbores |

**NOMAD E Base parts:**
- **Structure:** BASE_SHELL, KEYBOARD_TRAY, TRACKPAD_TRAY, COMPUTE_SLED.
- **Input envelopes:** ENV_KEYBOARD, ENV_TRACKPAD [PROVISIONAL].
- **Electronics envelopes:** ENV_PI5_BOARD_COOLER, ENV_NVME_HAT, ENV_COMPUTE_POWER, ENV_POWER_ELECTRONICS, ENV_BATTERY_BAY [RESERVE], ENV_GNSS_MODULE.
- **Keep-outs and cable envelopes (toggle):** 17 KEEPOUT_* / CABLE_* parts: hinge reserves, cooling duct, ports, plugs, vents, display pass, cable runs.

**Geometry:** exactly the Round C layout (D-007 **proposed**), generated from the YAML.

**Appearance:**

| Category | Colour |
|---|---|
| structure | dark grey |
| trays | mid grey |
| service parts | warm grey |
| keyboard | near black |
| trackpad (provisional) | lighter charcoal |
| electronics | translucent light neutral |
| battery reserve | translucent amber |
| hardware | metal grey |
| keep-outs | translucent red / orange / green / purple / yellow by type |

**Kernel cross-check** (scratch, `NOMAD_E_Prototype.test.fs`; *modeled*):

```
E1 n52 mc1 L0 S0/561 c160 dv0 m0 f17 fo15: DOOR 1 DOOR 2 PANEL 1..9 SLED 1..4
```

- 52 solids, each one body (the Pi stack is two by design).
- All 561 part-pair states (overlap / touch / gap) match the local Round C model; the 160 exact gaps deviate by 0.000 mm.
- One mate connector, exactly on the hinge axis.
- **15 of 17 representative fastener heads clash:** E1 findings F1 and F2 below.

---

## E1 findings: collisions, not resolved (stop-and-report rule)

### F1 — Service-panel / battery-door screw heads collide with the shell walls

| | |
|---|---|
| **What** | 11 representative M3 heads (panel 9, door 2) at the wall-merged bosses: front ×5, side ×2, rear ×4 |
| **Where** | Base underside, around the perimeter. Each head runs **0.5–0.75 mm** into the bottom of the front, side or rear wall |
| **Parameter** | Boss centre = wall inner face + BV_OFF (= BOSS_DIAMETER/2 − WALL_THICKNESS/2 = 2.25). With the panel inset by CLEARANCE (0.3), the screw axis is only **1.95 mm** from the panel edge, but a head needs **r ≈ 2.75**. It also leaves ≈ 0.25 mm of panel beyond an M3 clearance hole |
| **Contradicts a validated study?** | No. Round C validated bosses touching the panel and the shell's printability, but never modeled screw heads. This is a gap in Round C, not a contradiction |
| **Options (not chosen)** | (a) move the panel bosses inboard by ~1.1 mm, a small Round C layout change (BV_OFF rule); (b) let the panel/door extend under the walls (walls stop at the panel top), which changes the shell/panel split; (c) a smaller head (low-profile M2.5 or countersunk), a hardware choice; (d) local reliefs in the wall bottoms at each screw |

### F2 — Compute-sled screw heads collide with the service panel

| | |
|---|---|
| **What** | 4 representative M3 heads under COMPUTE_SLED (the sled screws up into its bosses, Round C) |
| **Where** | Right palm-rest bay. The heads (1.7 tall) sit in a **1.0 mm** gap between the panel (top Z 2.5) and the sled (bottom Z 3.5), overlapping the panel by **0.7 mm** |
| **Parameter** | Sled height: BV_SLZ0 = SERVICE_PANEL_THICKNESS + MIN_GAP |
| **Contradicts a validated study?** | No (fasteners not modeled in Round C). But the obvious fix does collide: raising the sled 1.7 mm would cut the Pi-stack-to-deck clearance from 2.0 to 0.3 mm, below MIN_GAP. So this touches the Pi-stack height budget (PI_STACK_HEIGHT 30 placeholder) |
| **Options (not chosen)** | (a) countersunk screws flush in local thickened sled pads; (b) pockets in the service panel under the sled screws; (c) a clip / slide-rail sled retained by the panel, with no screws; (d) raise the sled and reduce PI_STACK_HEIGHT once measured (the 30 is conservative; ~25–28 inferred) |

Neither finding affects the lid, hinge or solar work. Both are base fastening details inside the proposed D-007 architecture.

---

## What the owner does now (E1 review)

1. In the NOMAD document, create a **Part Studio** named `NOMAD E — Digital Prototype`.
2. Insert, from the Custom features menu, **NOMAD E Base**, then **NOMAD E Service** (defaults).
3. Expect **52 parts**, **1 mate connector** and two info notices.

**Inspect:**

| # | Check | How |
|---|---|---|
| 1 | Overall base: 301 × 235 × 40; deck with keyboard/trackpad openings and palm rests | Measure tool |
| 2 | Keyboard and trackpad envelopes 1 mm below the deck, centred (D-003) | Front/top view |
| 3 | Right palm-rest bay: sled, ENV_PI5_BOARD_COOLER + ENV_NVME_HAT, cooling-duct keep-out, ~2 mm to the deck | Section view through the bay |
| 4 | Left palm-rest bay: battery reserve behind the battery door | Hide BATTERY_DOOR |
| 5 | Under the keyboard: power electronics, GNSS (separate), compute power, cable trunk | Hide SERVICE_PANEL_MAIN |
| 6 | Underside: panel / door split, 17 heads. **F1:** heads entering the wall bottoms; **F2:** hide the panel to see sled heads intersecting | Bottom view, section at a boss |
| 7 | Rear: port panels, yellow plug keep-outs, red hinge reserves, purple display pass | Rear view |
| 8 | "Show keep-outs" off → a clean base | Edit feature |
| 9 | Mate connector at the rear-top edge on the centreline, Z-axis along −X | Select the connector |
| 10 | Names and colours readable; provisional labels visible | Parts list |

**Decisions requested before E2:**
- How to treat **F1 / F2**: hold E2 until they are resolved, or proceed and keep them recorded as open base-detail issues.
- Whether **`PI_HAT_ZONE_HEIGHT`** (a visual split of the Pi envelope) is acceptable.

**E1 review outcome (owner, 2026-09-26):** the base is accepted for Round E with no architectural changes; proceed to E2. F1 / F2 and `PI_HAT_ZONE_HEIGHT` stay open.

---

## E2 — digital lid: class A lid, solar mechanism geometry, hinge

**Scope (owner E2 instruction):**
- The complete provisional lid in `NOMAD_E_Prototype`: display, lid frame, sandwich rear shell, left/right cassettes, rails, carriages, hubs/pivots, hinge, controller envelope, cable corridors and keep-outs.
- Class A, **37.6 mm, PROVISIONAL — PENDING P0.2 PHYSICAL VALIDATION**.
- Solar = B.1 V1 + fixes. Hinge on the rear-edge axis with an Ø8 barrel and leaves.
- Mate connectors for E7. Stop after E2.

**Files:**

| File | What |
|---|---|
| `CAD/tools/e_lid_layout.py` (new) | Lid layout spec (26 parts, 9 connectors, 2 base hinge pockets), written as expressions over the YAML parameters. Exact local clearance model (X-prisms, exact circles), motion sweeps and checks. `--write` regenerates the GENERATED E LID LAYOUT block and the E2 harness EXPECTED block; `--check` verifies them |
| `CAD/featurescript/NOMAD_E_Prototype.fs` | Adds the generated lid block, feature **NOMAD E Lid**, the E2 builders (`nomadEBuildLid`) and the lid colours. E1 content unchanged |
| `CAD/featurescript/NOMAD_E_Prototype.e2.test.fs` (new) | Scratch harness "NOMAD E2 Check" (never written to the document) |

**Feature NOMAD E Lid.** The dialog is for visualization only:
- Show keep-outs (default on).
- Preview lid angle 0–135 (**keep 0 for the Assembly**).
- Preview right / left extension 0–1.
- Preview right / left tilt ±75.
- Defaults: lid closed, cassettes stowed.

Pose order:
1. Tilt about the stowed hub axis.
2. Slide along X by extension × 158.
3. Rotate the lid about the D-006 axis. This moves the lid parts, carriages, cassettes and lid-side connectors; the base hinge halves stay.

When NOMAD E Base is in the same Part Studio, the feature also cuts the two hinge pockets into `BASE_SHELL`.

### Lid stack (world Z, closed; modeled)

| Layer | Z | mm |
|---|---|---|
| Bezel lip (frame face 42–44.5) | 42–43 | 1 |
| Display | 43–48 | 5 |
| Gap | 48–49 | 1 |
| Rail layer (rails, carriages, pins, loops) | 49–62 | 13 |
| Gap | 62–63 | 1 |
| Cassettes | 63–71 | 8 |
| Back gap | 71–73 | 2 |
| Rear shell (sandwich envelope) | 73–79.6 | 6.6 |
| **Lid** | 42–79.6 | **37.6** |

Closed NOMAD height is **79.6 mm**. With both cassettes deployed the span is **612 mm**.

### Parts (26) and connectors (9)

| Group | Parts |
|---|---|
| Lid structure | `LID_FRAME`: face with display opening and active window, walls, front / rear bands, rail pads, hinge blocks, side slots and hub notches, hinge notches, display cable pass. `DISPLAY`: 10.1" 16:10 envelope, 235 × 150 × 5, SKU not selected. `LID_REAR_SHELL`: solid sandwich envelope, cells not modeled |
| Solar, per side | `SOLAR_RAIL_*` (C-channel + inboard end stop), `SOLAR_CARRIAGE_*` (22.6 × 8 × 40), `SOLAR_HUB_PIN_*` (Ø5 metal pin = tilt axis), `SOLAR_HUB_BRACKET_*`, `SOLAR_CASSETTE_*` (200 × 147.5 × 8 envelope), `KEEPOUT_SOLAR_CABLE_RUN_*` |
| Hinge, per side | `HINGE_BASE_HALF_*`: knuckles 1 and 3, leaf under the deck, tongues. `HINGE_LID_HALF_*`: knuckle 2, leaf in the face notch, tongue |
| Keep-outs | `KEEPOUT_SOLAR_LOOP_R/L`, `KEEPOUT_SOLAR_CORRIDOR`, `KEEPOUT_DISPLAY_FLEX`, `KEEPOUT_LID_DISPLAY_PASS`, `KEEPOUT_CONTROLLER_BAND_R/L` |

**Key geometry.** Right side, stowed; the left side is mirrored in X and staggered in Y.

| Item | Geometry |
|---|---|
| Rail | Y 121.5–149.1, X −51…147, end stop X −53.5…−51. Left rail Y 85.9–113.5 |
| Carriage | X −51…−11, Z 51.5–59.5 |
| Hub axis | Y 131.8 (left 103.2), Z 55.5. Pin X −11…0.5 |
| Bracket | X 0.5–10.5, 17 wide, Z 50.5–63 |
| Cassette | X 0.5–148, Y 17.5–217.5. Deployed X 158.5–306 (8 mm deploy clearance past the 150.5 side face) |
| Cable loops | Right Y 150.1–196.1, left Y 38.9–84.9, X to −91 / 147. Corridor Y 113.5–121.5, X ±55 |
| Hinge | Axis Y 235, Z 40 (D-006, h 0). Ø8 knuckles X 121–129 (base), 130–138 (lid), 139–147 (base), mirrored. Base leaf Z 35–37.5 under the deck. Lid leaf Z 42–45 in the face notch. Base pocket X 120–148, Y 230+, Z 35+ |
| Controller reserves | X ±(8.5–119), Y 197.1–232.5, Z 44.5–56.5 (12 mm; location not decided, both sides reserved) |

**Mate connectors** (for E7; all move with their owner parts):

| Connector | Owner | Origin (closed) | Z axis | Intended mate |
|---|---|---|---|---|
| MC_HINGE_LID | LID_FRAME | (0, 235, 40) | −X | Revolute to MC_HINGE_BASE (E1), 0–135° |
| MC_RAIL_R / MC_CARRIAGE_R | rail / carriage | (−11, 135.3, 55.5) | +X | Slider, 0–158 |
| MC_HUB_R / MC_CASSETTE_R | carriage / cassette | (0.5, 131.8, 55.5) | +X | Revolute, ±75° |
| MC_RAIL_L / MC_CARRIAGE_L | rail / carriage | (11, 99.7, 55.5) | −X | Slider, 0–158 |
| MC_HUB_L / MC_CASSETTE_L | carriage / cassette | (−0.5, 103.2, 55.5) | −X | Revolute, ±75° |

At E7 the pin and cable-run keep-out need to be fastened (or grouped) to their carriage, and the bracket to its cassette.

### Kernel cross-check (scratch, `NOMAD_E_Prototype.e2.test.fs`; modeled)

```
E2 n55 mc10 L0 S0/181 c177 dv0 m0 P0/15 pd0 F:
```

- **55 solids:** 29 base parts (NOMAD E Base with keep-outs) + 26 lid parts. Every named part is one solid.
- **10 mate connectors:** 1 base + 9 lid. Every origin is exact (deviation 0.000).
- **Near pairs:** all 181 overlap / touch / gap states match the local model. The 177 exact gaps deviate by 0.000 mm.
  - The 4 overlaps are F3 (×2) and the by-design carriage / cable-run overlap (×2, B.1).
- **Posed clearances:** all 15 deviate by 0.000 mm. Poses: lid 105 deployed; 135 stowed; 105 deployed and tilted +75 / −75.
  - This includes the rear-plug overlap of −6.6 at 135°.

### Local validation (`py CAD/tools/e_lid_layout.py`; modeled)

**Mechanism and sweeps:**
- **B.1 consistency:** 29 of 29 V1 + fixes values are identical.
- **Rigid groups:** no structural overlaps.
- **Moving parts:** 0 unexpected violations. Poses covered: lid 0 / 105 / 120 / 135 × stowed / R / L / both; tilts ±75 in steps of 15, same and opposite; slides 0…1.
- **Lid sweep** 0–135° in 1° steps: no lid–base violations; minimum 1.000 (hinge knuckles and pockets, as designed).

| Owner check | Result |
|---|---|
| Display / cassette | 15.0 (the rail layer is between them) |
| Rail / display | 1.0 (= MIN_GAP) |
| Carriage | Runs in the channel: carriage–rail touch is the sliding joint, by design. Carriage–corridor 2.5. Deployed carriage to side wall 1.0 |
| Cassette / lid | Stowed: 1.0 to the frame, 2.0 to the rear shell, 1.0 left–right. Deployed: 8.06 to the frame |
| Cassette / base | 29.99 (105°, deployed), 28.64 (135°, stowed), 111.5 (105°, tilted ±75) |
| Hinge | Knuckle gaps 1.0 at every angle; lid half to base half 1.0 at 105° and 135° |
| Cable corridor / loops | Loop–cassette 1.0, controller band–loop 1.0. The corridor touches both rails (it is the space between them). The display flex reserve touches the right loop reserve (0.0; two reserves, flagged) |
| Side wall | Cassette slot 1.0 all round; deployed carriage 1.0 |
| Known rear port | 105°: 10.75, 120°: 1.20, 135°: **−6.60** (first below MIN_GAP at 121°). OPEN CONFLICT, left visible |

**Lowest cassette point above the table, both deployed** (Z in mm; negative = below the table):

| Lid | 0 / 0 | +30 | −30 | +45 | −45 | +75 | −75 |
|---|---|---|---|---|---|---|---|
| 0° | 50 | 5 | 19 | **−20** | 0 | **−53** | **−25** |
| 105° | 49 | 55 | 55 | 65 | 68 | 99 | 113 |
| 120° | 40 | 36 | 32 | 41 | 38 | 66 | 71 |
| 135° | 30 | 15 | 8 | 16 | 8 | 32 | 27 |

---

## E2 findings: collisions, not resolved (stop-and-report rule)

### F3 — B.1 hub-bracket envelope enters the rail channel floor

| | |
|---|---|
| **What** | `SOLAR_HUB_BRACKET_R/L` vs `SOLAR_RAIL_R/L`: **1.0 mm** overlap |
| **Where** | The bracket bottom (Z 50.5 = hub axis 55.5 − pin radius 2.5 − wall 2.5) sits below the channel floor top (Z 51.5). This holds wherever the bracket is inside the rail length: stowed and along the slide. It clears once the bracket passes the rail end |
| **Parameter** | `SOLAR_HUB_AXIS_OFFSET_Z` (−7.5), `SOLAR_HUB_PIN_DIAMETER`, `WALL_THICKNESS` (bracket wall under the pin), `SOLAR_RAIL_LAYER_HEIGHT` |
| **Contradicts a validated study?** | No. B.1 treated bracket and rail as attached and never checked this pair (a gap in B.1, not a contradiction) |
| **Options (not chosen)** | (a) thinner bracket wall under the pin (1.5), which needs a strength check; (b) raise the pin within the carriage; (c) deepen the channel by 1 mm (rail layer 14, lid +1 mm → 38.6); (d) a relief groove in the rail floor along the bracket path, which weakens the floor |
| **Resolution** | **F3 APPROVED AND IMPLEMENTED — OPTION B** (2026-09-26): tilt axis +2.0 mm (Z 57.5) and a carriage slot boss; bracket–floor now 1.0 over the full travel. See the F3 implementation section below and `round_e_f3_investigation.md` §10 |
| **Follow-up (history)** | Investigated in `round_e_f3_investigation.md` (analysis only, awaiting approval at the time). **Correction:** (a) at 1.5 mm and (c) at +1 mm only reach contact. The deficit to MIN_GAP is 2.0 mm, so (a) needs a 0.5 mm wall and (c) with a centred pin needs a 41.6 mm lid. Recommended there: (b), axis +2.0 with a carriage slot boss and no lid change |

### Notes (not collisions)

- **Table contact with the lid closed.** At lid 0° with both cassettes deployed, tilts beyond about +30 / −45 put the cassette below the table. This is the known B.1 operating limit; it is an operating rule, not a model collision. At lid 105–135° every tilt clears (≥ 8).
- **Display flex vs right solar loop.** The two reserves are adjacent (0.0 at Z 49, Y 192.5–196.1). The display FPC runs directly under the loop zone.
- **Not modeled:**
  - sandwich cells;
  - class B / C variants (deferred);
  - stowed cassette outboard support and latch;
  - hub lock / index (15° concept only);
  - deployed end stop (the rail has an inboard stop only);
  - twist zones (Python only);
  - rail reinforcement strips (P0.2);
  - controller location (both bands reserved);
  - display FPC exit (assumed centre-rear);
  - hinge hardware (representative only).

**Deviations from the plan:**
- The plan split E2 (lid), E3–E4 (solar) and E5 (hinge) into separate features. The owner's E2 instruction covered all of them, and they are built as **one** feature, NOMAD E Lid, so the preview pose moves everything consistently from one generated layout.
- The generator is `e_lid_layout.py` (lid only) instead of `e_prototype_layout.py`; the base stays in `base_v01_layout.py`.
- The builder accepts `"cutPockets" : false`. Only the scratch harness uses it, to build posed copies against one base shell; the production default always cuts.

**API:** 112 → 125 (one scratch run ≈ 10, one read, one write, one usage check).

---

## What the owner does now (E2 review)

1. In Part Studio `NOMAD E — Digital Prototype`, after NOMAD E Base and NOMAD E Service, insert **NOMAD E Lid** with its defaults.
2. Expect:
   - **26 new parts** (78 in total), or 17 with keep-outs off;
   - **9 new mate connectors** (10 in total);
   - the notice "Hinge pockets cut in BASE_SHELL. Pose: lid 0 deg, R 0 / L 0 extended."

**Inspect:**

| # | Check | How |
|---|---|---|
| 1 | Closed: lid 37.6 on the base with a 2 mm gap; total 79.6; flush sides | Side view, Measure tool |
| 2 | Stack: display / rail layer / cassette / back gap / shell | Section view (plane X = 60) |
| 3 | Rails staggered: right rail behind the centreline, left in front, 8 mm corridor between them | Hide LID_REAR_SHELL and both cassettes; top view |
| 4 | **F3:** bracket bottom inside the rail floor | Section view (plane X = 5), zoom on the hub |
| 5 | Deployment: set R and L extension to 1 → 612 mm span, cassettes 8 mm clear of the lid sides | Edit the feature |
| 6 | Tilt: ±75 on each side; cassettes rotate about the pin | Edit the feature, lid angle 105 |
| 7 | Lid 105 / 120 / 135: at 135 the rear shell enters the yellow plug keep-outs (known conflict) | Edit the feature, rear view |
| 8 | Hinge: three Ø8 knuckles per side, leaves, pockets in BASE_SHELL | Rear view; hide the lid |
| 9 | Keep-outs off → clean lid | Edit the feature |
| 10 | Before E7: reset lid angle, extensions and tilts to 0 | Edit the feature |

**Decisions requested before E3 / E4:**
- **F3:** option (a) / (b) / (c) / (d), or keep it recorded and proceed.
- Whether the **closed-lid tilt limit** is accepted as an operating rule.
- Whether **class B / C** lid variants are wanted in the digital prototype.
- Still open from E1: **F1 / F2**, **`PI_HAT_ZONE_HEIGHT`**.

---

## F3 implementation — F3 APPROVED AND IMPLEMENTED — OPTION B (2026-09-26)

The owner approved option (b) from `round_e_f3_investigation.md`. The full record, with every changed clearance, is in §10 of that file.

**What changed:**
- **Parameters:**
  - `SOLAR_HUB_AXIS_OFFSET_Z` −7.5 → **−5.5** (formula: rail floor + MIN_GAP + bracket wall + pin radius);
  - new `SOLAR_BRACKET_WALL` = `WALL_THICKNESS` → 2.5, working.
- **Geometry:**
  - tilt axis Z 55.5 → 57.5; hub bracket Z 52.5–63 (2.5 wall kept);
  - carriage body unchanged, plus a 17.0 × 2.5 × 40 boss in the rail slot (Z 59.5–62);
  - the cable run, side-wall notch bottom and the eight solar mate connectors follow the axis.
- **Unchanged:** lid 37.6, rail section, cassette, travel 158, ±75°, deploy 8, corridor 8, hinge, display, service, rear port.
- **Generator:**
  - bracket–rail is now a guided fit (≥ CLEARANCE);
  - new checks: bracket–floor sweep over the full travel and the F3 vertical-budget assertion.

**Validation (modeled):**
- **Local E2 suite:** ALL CHECKS PASSED.
  - bracket–floor min 1.000 over the full 158 mm travel;
  - 0 unexpected moving-part violations;
  - lid sweep clean;
  - rear-plug OPEN CONFLICT unchanged (−6.6 at 135°, below MIN_GAP from 121°).
- **Study reproducibility:** all published study outputs are byte-identical.
- **Onshape scratch:** `E2 n55 mc10 L0 S0/177 c175 dv0 m0 P0/15 pd0`, exact.
- **Persistent Feature Studio:** written; the read-back is identical to the local file. API 125 → 140.

**Margins that shrink** (all still ≥ MIN_GAP):
- carriage boss to the other stowed cassette: 1.0 (was 3.5);
- pin to either cassette: 3.0 (was 5.0); cable run: 2.5 (was 4.5);
- lowest tilted cassette at lid 105–135°: 6.5 (was 7.8).

**Owner check:** regenerate or update NOMAD E Lid in the Part Studio. Section at X = 5: bracket 1 mm above the floor. Section at X = −30: carriage boss in the slot.

---

## D-009 — solar tilt index lock and hub-pin anti-rotation (2026-09-28; local only)

The owner approved the complete mechanism. Full record: `round_e_solar_index_lock_implementation.md`.

**What changed in the digital lid (per side):**
- **Parts:** 26 → **46** lid parts. New per side:
  - hub pin (Ø5 × 53.5, A/F 3.0 double-D at both ends);
  - anti-rotation plate + Ø3 × 24 dowel in the carriage;
  - M2 screw / washer envelopes at both pin ends;
  - stainless index plate (R 11.75, 11 × Ø1.6 on r 10);
  - Ø1.5 index pin, counter sleeve, slider (carrier + thumb tab), spring envelope and channel cover.
- **Carriage:** access bore, anti-rotation slot, dowel bore and push-out hole.
- **Cassette:** index groove, sleeve bore + grit relief, guide bore, spring channel.
- F3 hub geometry, the lid, rails, travel, ±75° and the hinge are unchanged.

**Validation (modeled):**
- **Local suite:** ALL CHECKS PASSED, with lock checks A–G. The E2 set shows 0 unexpected violations.
- **Onshape scratch:** `E2 n75 mc10 L0 S0/398 c396 dv0 m0 P0/27 pd0`, exact.

**Open, blocking the persistent write:** the **±80° hard stops are not packaged**.
- `NOMAD_E_Prototype` in Onshape still holds the post-F3 version.
- The local `.fs` is the validated D-009 candidate.

**Owner decision:** stops option S1 / S2 / S3 (implementation report §8).
