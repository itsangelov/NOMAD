# Round E — NOMAD Full Digital Prototype: E0 Architecture Review and Implementation Plan

> **PARTLY SUPERSEDED FOR NOMAD V1 (D-010, 2026-10-01).** Its lid / solar content (class-A lid, sliding solar cassettes, E2 lid, F3, D-009) is **Architecture A**, superseded / deferred for V1; B1 was selected. The base content still shows the *proposed* D-007 (not accepted). Kept unchanged as an engineering record. See `docs/decisions.md` D-010 and `docs/v1-requirements.md`.

**Status:** plan only, awaiting approval.
- No Onshape changes, and no YAML, geometry or Git changes.
- One read-only FeatureScript documentation search (~1 API call) confirmed that `opMateConnector` exists.

---

## A. Repository findings

**What already exists and is reused, not recreated:**

| Asset | Content | Validation state |
|---|---|---|
| `nomad.yaml` → `yaml_to_featurescript.py` | 88 parameters; GENERATED PARAMS block | pipeline works (`--check`) |
| `CAD/tools/base_v01_layout.py` (Round C) | Complete base V0.1: shell (33 primitives: walls, deck with keyboard/trackpad openings, palm rests, bulkheads, bosses, rear port notches), keyboard tray, trackpad tray, compute sled, main service panel, battery door, 2 port panels, standoffs, 7 component envelopes, hinge reserves, cooling/port/plug/vent keep-outs, 7 cable runs; generates the FeatureScript layout block | local checks + one scratch kernel cross-check (Round C) |
| `NOMAD_P01.fs` builders | `nomadBuildBaseV01` (Round C base), `nomadBuildSolarSide` (Round B skeleton), Round A skeleton / lid / clearance check, hinge transform helpers | scratch-tested only. **Never written to Onshape** (the only Feature Studio in the document is `NOMAD_P01_Coupons`). |
| `solar_v1_feasibility.py` (B.1) | **V1 + fixes:** carriage 22.6 × 8, rail 27.6 × 13, slot 17.6, bracket 17 × 10, pin Ø5, link 11.5, deploy clearance 8, travel 158, 8 mm corridor, staggered rails crossing the centreline, service loops (R 20, cable Ø6), tilt-joint cable zone, side-wall slots and notches | full collision sweep; B.1 kernel cross-check matched exactly; re-run with 2-strip rails in D.1 |
| `hinge_feasibility_2d.py`, `c2_screening.py` | D-006 hinge sweeps; lid × h × θ × plug feasibility | kernel cross-checked (A.2, C.2) |
| `lid_stackup_study.py`, `lid_architecture_convergence.py` (D, D.1) | lid layer stack, classes A/B/C, controller band, rail reinforcement | analytical; no class chosen |
| P0.1/P0.2 coupons | physical test articles (rail, sandwich); print package ready | not printed |

**Decisions:**
- D-001 accepted: FeatureScript, **P0.1 scope only**.
- D-002 accepted: YAML is the master.
- D-003 accepted: trackpad centred below keyboard.
- D-004 accepted: slide + tilt about the slide axis, indexed, rail + hub load paths, no motors or slip ring.
- D-006 accepted, provisional: rear-edge hinge axis, closed gap 2.0.
- **D-007 proposed:** Round C base placement and service; not accepted.

**Inconsistencies the prototype must not paper over:**
1. **`LID_THICKNESS` working 25** is below every enclosed lid (Round D / D.1: 37.5–42). The YAML has no lid-stack parameters.
2. **Solar YAML ≠ validated V1 + fixes:**
   - carriage 12 vs 22.6;
   - deploy clearance 5 vs 8;
   - travel 155 vs 158;
   - link 8.5 vs 11.5;
   - hub offset formula (cassette centre) vs V1 hub (rail centre ± 3.5);
   - no corridor, cable, bracket or slot parameters at all.
3. **D-001 covers P0.1 only.** Using FeatureScript for Round E needs a decision (proposed D-008 below).
4. **D-007 is proposed.** The base will visualize a proposed architecture, labelled as such.
5. **Rear ports vs lid sweep (C.2 / D.1, modeled):** at T 37.6 and h 0, rear ports with 45 mm plugs allow only 120°. 135° needs h ≈ 5, plugs ≤ 15 mm, or no rear ports.
6. **Undesigned items** that the prototype can only show as envelopes: hinge hardware, hub/lock/index mechanism, stowed-cassette outboard-edge support, controller location (lid band vs base), rail reinforcement (pending P0.2).

---

## B. Architecture to implement (current working state; nothing new decided)

**Global frame** (as Round C): X across the width (0 = centreline, +X = right, viewed from the front), Y front → rear (base front face = 0), Z up (base underside = 0).

**BASE:** Round C V0.1 exactly (D-007 as proposed).
- **Size:** 301 × 235 × 40 (working).
- **Shell:** wall 2.5, open underside.
- **Inputs:** keyboard 280 × 105 × 8, recessed 1; trackpad 86 × 75 × 13 (provisional envelope), recessed 1, centred below the keyboard, gap 10; front margin 15; rear zone 30.
- **Compute:** Pi stack envelope 93 × 64 × 30 on a sled in the right palm bay, with a 20 mm cooling duct ahead of it.
- **Battery:** reserve 90 × 82 × 30 in the left palm bay, behind its own door.
- **Under the keyboard:** power electronics 90 × 45 × 20 (left), GNSS 70 × 35 × 12 (centre-left, separate module), compute power 50 × 30 × 15 (right).
- **Service:**
  - main service panel and battery door on the underside;
  - two rear port panels 90 × 15 at Z 4–19;
  - hinge-mount reserves 28 × 21 at both rear corners;
  - cable trunk 15 × 10 and display riser.
- **Visual realism:** the shell already has real walls, deck openings, palm rests, bulkheads, bosses and port notches. Only electronics stay as envelopes.

**LID:** D.1 class A, sandwich rear shell, **T 37.6**. Default for visualization only, marked **PROVISIONAL, PENDING P0.2 PHYSICAL VALIDATION**. Classes B / C are available as a dialog toggle.

| Layer (from the display face) | Z in the lid | Source |
|---|---|---|
| Front retention lip over the display border | 0–1 | D (1 mm) |
| Display 235 × 150 × 5, centred | 1–6 | YAML working |
| Display gap | 6–7 | MIN_GAP (the **1.0 mm rail/display criterion**) |
| Solar rail layer (rails, carriages, loops, corridor) | 7–20 | V1 + fixes (13) |
| Rail–cassette gap | 20–21 | MIN_GAP |
| Stowed cassette 147.5 × 200 × 8 | 21–29 | YAML working |
| Cassette–back gap | 29–31 | **2.0** (D.1 / P0.2) |
| Sandwich rear shell 1.2 / 4.2 core / 1.2, webs 2.0 @ 30 | 31–37.6 | D.1 class A (= P0.2 B-S30) |

- **Front frame:**
  - face ring, lip, perimeter walls;
  - side walls with the **cassette slots** (Y 16.5–218.5) and bracket/pin/cable notches;
  - 14 mm edge bands (shell seat, 10 screw positions);
  - rail pads beside the display (x 118.5–147);
  - hinge corner blocks (Y 218.5–235 × 28);
  - controller band (111.5 × 35.4 × 17.5 per side of the 15 mm centre pass, working envelope; location not decided).
- **Rear shell:** separate part.

**SOLAR (B.1 V1 + fixes, unchanged):**
- **Layout:** each cassette lives in **its own half of the lid width**, right cassette x 0.5–148 and left −148 to −0.5, in the same layer. Each deploys outward from its own side wall.
- **Rails:** staggered in Y (right Y 121.5–149.1, left 85.9–113.5), each crossing the centreline by 51 mm, with an 8 mm cable corridor between them.
- **Moving parts:**
  - carriage 22.6 × 8 × 40 in the rail;
  - Ø5 hub pin over the 11.5 mm link;
  - 17 mm hub bracket on the cassette;
  - tilt axis along X at the hub (right hub Y 131.8, left 103.2; Z at rail mid-height).
- **Motion:** travel 158, deploy clearance 8, **deployed span 612**, tilt ±75° in 15° index steps.
- **Cable envelopes:** loops (bend R 20, Ø6) at Y 150–196 (right) and 39–85 (left), plus a tilt-joint cable zone.
- **Rail reinforcement strips:** a toggle (none / 1 / 2), default **none**, pending P0.2.

**HINGE:** D-006 axis at the base rear face (inset 0) and the base top + h (h working 0); closed gap 2.0. Hardware is TBD, so it is shown as a **representative knuckle hinge** inside the reserved corner volumes (see H5).

---

## C. Proposed Onshape document structure

**Existing elements, not touched:**
- the original tab;
- Feature Studio `NOMAD_P01_Coupons`;
- Part Studio `P0.1 Coupons`.

**New elements:**

| Element | Created by | Content |
|---|---|---|
| Feature Studio **`NOMAD_E_Prototype`** | Claude (`create_feature_studio`, then `put_featurescript` per stage) | Generated params block (from YAML), generated base layout block (Round C generator), lid / solar / hinge layout blocks (new generator), builders, 5 production features, one check feature |
| Part Studio **`NOMAD E — Digital Prototype`** | **Owner** (the connector cannot create Part Studios) | The E features inserted in order; every part named, coloured and in the closed/stowed pose; mate connectors on the moving parts |
| Assembly **`NOMAD — Digital Prototype`** + sub-assemblies **`BASE`**, **`LID`** (flexible), **`SERVICE`** | **Owner** (the connector cannot create Assemblies or mates) | Instances of the Part Studio parts; ~7 mates using the pre-built connectors (§G); a click-by-click guide is supplied at E7 |

**Local files (planned):**
- `CAD/featurescript/NOMAD_E_Prototype.fs` (snapshot) and `NOMAD_E_Prototype.test.fs` (scratch harness).
- `CAD/tools/e_prototype_layout.py`: lid / solar / hinge layout spec + local checks + FeatureScript block generation, reusing the D.1 / B.1 / C.2 models.
- Small `--target` options in `yaml_to_featurescript.py` and `base_v01_layout.py`, so the same generators also write the E file. Default behaviour is unchanged.
- Report `prototypes/P0.1/round_e_digital_prototype.md`.

---

## D. Part Studio / Feature Studio / Assembly structure

**Features in `NOMAD_E_Prototype`** (each a dialog-light feature, inserted in this order):

| Feature | Builds (part names) | Dialog (visualization only; no engineering values) |
|---|---|---|
| NOMAD E Base | `BASE_SHELL`, `KEYBOARD_TRAY`, `TRACKPAD_TRAY`, `COMPUTE_SLED`, `ENV_KEYBOARD`, `ENV_TRACKPAD (PROVISIONAL)`, `ENV_PI_STACK`, `ENV_NVME_HAT`, `ENV_COMPUTE_POWER`, `ENV_POWER_ELECTRONICS`, `ENV_BATTERY_BAY`, `ENV_GNSS_MODULE` | show keep-outs / cable runs (default on) |
| NOMAD E Service | `SERVICE_PANEL_MAIN`, `BATTERY_DOOR`, `PORT_PANEL_MAIN`, `PORT_PANEL_AUX`, `PANEL_STANDOFF_L/R`, representative `FASTENER_*` (shell, panel, hinge screws) | show fasteners |
| NOMAD E Lid | `LID_FRAME`, `DISPLAY`, `LID_REAR_SHELL`, `ENV_DISPLAY_CONTROLLER_L/R`, `SOLAR_RAIL_L/R`, `KEEPOUT_SOLAR_LOOP_L/R`, `KEEPOUT_SOLAR_CORRIDOR` | lid class A / B / C (default A); rail strips none / 1 / 2 |
| NOMAD E Solar | `SOLAR_CARRIAGE_L/R` (+ hub pin), `SOLAR_CASSETTE_L/R` (+ hub bracket), `KEEPOUT_SOLAR_TWIST_L/R`; mate connectors on the rail, carriage, hub and cassette | none (pose is set in the Assembly) |
| NOMAD E Hinge | `HINGE_L/R_BASE_LEAF`, `HINGE_L/R_LID_LEAF`, `HINGE_L/R_PIN`; mate connectors on the base and lid at the axis | none |
| NOMAD E Check | no parts; reports clearances for closed / 105° / 135° / deployed poses as a feature notice, computed on transformed copies, so you can re-check after parameter edits without Claude | poses to check |

**Assembly:**

```
NOMAD — DIGITAL PROTOTYPE
├── BASE (sub-assembly, grouped): BASE_SHELL, trays, sled, keyboard, trackpad, ENV_* (Pi, NVMe/HAT, battery, GNSS, power, compute power), KEEPOUT_PORTS_*, HINGE_*_BASE_LEAF, cable runs
├── SERVICE (sub-assembly, fastened to BASE): SERVICE_PANEL_MAIN, BATTERY_DOOR, PORT_PANEL_MAIN/AUX, standoffs, FASTENER_*
└── LID (flexible sub-assembly, revolute to BASE)
    ├── lid structure group: LID_FRAME, DISPLAY, LID_REAR_SHELL, SOLAR_RAIL_L/R, ENV_DISPLAY_CONTROLLER_*, KEEPOUT_SOLAR_*, HINGE_*_LID_LEAF, HINGE_*_PIN
    ├── SOLAR_CARRIAGE_L / SOLAR_CARRIAGE_R (slider to the lid structure)
    └── SOLAR_CASSETTE_L / SOLAR_CASSETTE_R (revolute to their carriages)
```

**Fallback if sub-assembly setup is too slow:** one flat assembly with Group mates. Composite parts would reduce clicks but prevent hiding individual parts, so they are not recommended.

**Appearance** (engineering readability):

| Category | Appearance |
|---|---|
| structure | dark grey |
| display | near-black, glossy |
| solar cassettes | restrained blue |
| rails / carriages / hardware | metal grey |
| electronics envelopes | light neutral, semi-transparent where the API allows |
| service panels | slightly warmer grey |
| keep-outs / cable envelopes | translucent colours, `KEEPOUT_*` names |

---

## E. Parameter mapping (YAML is the only master)

| Subsystem | YAML parameters used (status) |
|---|---|
| Base envelope | BODY_WIDTH / DEPTH (formula → 301 / 235), BODY_HEIGHT 40, WALL_THICKNESS 2.5, SERVICE_PANEL_THICKNESS, MOUNT_PLATE_THICKNESS, INPUT_TRAY_LIP, TRACKPAD_BAY_MARGIN, BOSS_DIAMETER, TRAY_POST_DIAMETER, BASE_SIDE / FRONT_MARGIN, BASE_REAR_ZONE_DEPTH (all working / TBD) |
| Keyboard / trackpad | KEYBOARD_WIDTH / DEPTH / THICKNESS (provisional values); TRACKPAD_* (working); KEYBOARD / TRACKPAD_LATERAL_OFFSET, TRACKPAD_KEYBOARD_GAP, *_TOP_RECESS (working) |
| Compute / power / GNSS | PI_WIDTH / DEPTH (provisional), PI_STACK_HEIGHT, PI_ENVELOPE_MARGIN, COOLING_DUCT_DEPTH, COMPUTE_POWER_*, POWER_ELEC_*, GNSS_MODULE_*, NVME_FORMAT |
| Battery | BATTERY_BAY_WIDTH / DEPTH / HEIGHT (reserve only) |
| I/O | PORT_PANEL_*, PORT_KEEPOUT_DEPTH, PLUG_KEEPOUT_LENGTH |
| Cables | CABLE_CORRIDOR_WIDTH / HEIGHT |
| Hinge | HINGE_AXIS_OFFSET, HINGE_AXIS_HEIGHT, HINGE_MOUNT_WIDTH / DEPTH, LID_CLOSED_GAP, LID_ANGLE_NOMINAL / MAX |
| Display | DISPLAY_WIDTH / HEIGHT / THICKNESS / VERTICAL_OFFSET (working), DISPLAY_ACTIVE_* (derived) |
| Lid | **LID_THICKNESS** (working 25: **must change, see E0.5**) + new lid-stack parameters (E0.5) |
| Solar | SOLAR_CASSETTE_* (formula / working), SOLAR_ROTATION_LIMIT (provisional ±60–75), SOLAR_INDEX_STEP, SOLAR_HUB_PIN_DIAMETER, SOLAR_RAIL_ENGAGEMENT, SOLAR_CARRIAGE_HEIGHT + **V1-fix reconciliation (E0.5)** |
| Clearances | CLEARANCE 0.3, MIN_GAP 1.0, MIN_WALL 2.0 |

**E0.5: proposed YAML working-value reconciliation.** These are working / TBD values only; no authoritative `value` changes. **Each needs your approval.**

| Parameter | Now | Proposed working / formula | Source |
|---|---|---|---|
| SOLAR_CARRIAGE_WIDTH | 12 | formula → **22.6** (bracket + 2 × CLEARANCE + 2 × WALL) | B.1 fix |
| SOLAR_DEPLOY_CLEARANCE | 5 | formula → **8** (cable Ø + 2 × MIN_GAP) | B.1 fix |
| SOLAR_SLIDE_TRAVEL, SOLAR_HUB_LINK_LENGTH | 155, 8.5 | unchanged formulas → **158, 11.5** | follows |
| *new* SOLAR_CABLE_DIAMETER, SOLAR_CABLE_BEND_RADIUS | — | 6, 20 (envelopes, not cable choices) | B.1 |
| *new* SOLAR_CABLE_CORRIDOR | — | formula → 8 | B.1 fix |
| *new* SOLAR_BRACKET_WIDTH / _LENGTH, SOLAR_RAIL_SLOT_WIDTH | — | formula 17 / working 10 / formula 17.6 | B.1 |
| SOLAR_HUB_AXIS_OFFSET_Y / _Z | formulas (cassette centre) | V1 derivation (rail centre ∓ 3.5; rail mid-height) | B.1 (D-004 left the hub to P0.1 validation) |
| *new* DISPLAY_BEZEL_LIP, SOLAR_RAIL_LAYER_HEIGHT, LID_BACK_GAP, LID_REAR_SHELL_DEPTH, SANDWICH_SKIN, SANDWICH_WEB, SANDWICH_WEB_SPACING, LID_EDGE_BAND | — | 1, formula → 13, 2.0, 6.6, 1.2, 2.0, 30, 14 | D / D.1 class A |
| **LID_THICKNESS** | working 25 | **formula** (sum of the stack) → **37.6** | D.1; **owner decision** |
| *new* DISPLAY_CONTROLLER_THICKNESS | — | 12 (envelope) | D |
| *new* HINGE_BARREL_DIAMETER | — | 8 (representative only) | new (H5) |

**Pipeline:** `mechanical-spec.md` rows are added to match, and the FeatureScript block is regenerated. Round E's Feature Studio gets **no** dialog overrides for engineering values, so there is no second parameter system. Edits are YAML → regenerate → one `put_featurescript` call.

---

## F. Provisional dimensions

**Everything is provisional or working except:** DISPLAY_DIAGONAL / ACTIVE (provisional / derived), KEYBOARD 280 × 105 × 8 (provisional), PI 85 × 56 (provisional), SOLAR_ROTATION_LIMIT (provisional).

**Marked PROVISIONAL in the model:**
- **Body:** 301 × 235 × 40.
- **Display module:** 235 × 150 × 5.
- **Trackpad envelope:** 86 × 75 × 13 (candidate module, not locked).
- **Lid:** the whole stack (T 37.6, class A: *pending P0.2*).
- **Hinge:** axis h 0; representative hinge hardware.
- **Solar:** cassette 147.5 × 200 × 8; the V1 + fix mechanism (validated geometrically, not physically); the hub/lock/index as envelopes; no rail reinforcement.
- **Controller:** controller band.
- **Base contents:** all electronics envelopes; battery reserve; port panels.
- **Service parts:** panel / door outlines; fastener positions.

---

## G. Motions implemented as mates

The parts are built in one canonical pose: closed, stowed, tilt 0. Mate connectors are created in FeatureScript, so each mate is a two-click connector pick.

| Motion | Mate | Connectors | Limits |
|---|---|---|---|
| Lid open / close | **Revolute** LID ↔ BASE | `MC_HINGE_BASE` / `MC_HINGE_LID`: axis along X at (Y = D − HINGE_AXIS_OFFSET, Z = H + h) | 0 → **135°** (LID_ANGLE_MAX) or 0 → 120° (see H4) |
| Right carriage slide | **Slider** carriage ↔ lid structure | `MC_RAIL_R` / `MC_CARRIAGE_R`, +X | 0 → 158 |
| Left carriage slide | **Slider** | `MC_RAIL_L` / `MC_CARRIAGE_L`, −X | 0 → 158 |
| Right cassette tilt | **Revolute** cassette ↔ carriage | `MC_HUB_R` / `MC_CASSETTE_R`: axis along X through the hub pin | −75° → +75° |
| Left cassette tilt | **Revolute** | `MC_HUB_L` / `MC_CASSETTE_L` | −75° → +75° |
| Everything else | Group / Fastened within BASE, SERVICE and the lid structure | — | — |

**Not enforceable with mates** (documented; checked in E8 and by the check feature):
- the 15° index steps (type the angles);
- the "tilt only at full extension" interlock: tilting a stowed cassette will visibly collide, which is correct;
- the positive lock.

---

## H. Known risks

1. **Connector limits.** It cannot create Part Studios, Assemblies or mates, or insert features. You do those steps. My side: mate connectors, a click list and stable feature ids, so mates survive regeneration.
2. **YAML reconciliation (E0.5) is a prerequisite.** Without it, the prototype would have to use a second, hidden parameter set, which the brief forbids.
3. **Lid class for visualization.** A (37.6) is proposed as the default because it is what P0.2 validates, and B / C sit behind a toggle. This is **not** a lid-class decision.
4. **Rear ports vs lid sweep** (known, C.2 / D.1). At T 37.6 and h 0 the lid enters the 45 mm plug keep-out beyond 120°. The prototype will **show** this rather than fix it. You choose the revolute limit (135° shows the intrusion; 120° stays feasible).
5. **Hinge representation.** A physical barrel on a rear-edge axis at h 0 must sit in notches in the base and lid corners. Those notches fall inside the Round C hinge reserves, so they are not new structure, but they are new geometry. The alternative is leaf blocks only with a phantom axis. The barrel diameter (8) would be a new representative working value.
6. **D-001 scope.** FeatureScript for Round E needs **proposed D-008**: "Round E digital prototype: FeatureScript-generated parts + owner-built Assembly; YAML remains master; not production CAD".
7. **D-007 is still proposed.** The base shows it labelled "proposed".
8. **Undesigned mechanisms** are shown as envelopes only: the hub lock / index gears, the stowed-cassette outboard-edge support, the controller location, and cable flexing (loops are static keep-outs).
9. **Visual realism vs printability.** Boxes-with-openings geometry plus light external fillets (E9, optional). Print splits and overhang fixes are not optimized (per the brief).
10. **Part identity.** Changing feature order or ids can break Assembly references. Ids are kept deterministic.
11. **Clash visibility.** Onshape Assembly clash display depends on the account's features. Clearances are guaranteed by local sweeps + the kernel harness + the check feature, not by eye.
12. **Wording to confirm:** "not side-by-side across the lid width". In V1 each cassette occupies **its own half** of the lid width and deploys from its own side. I read your instruction as ruling out a shared or stacked bay, which V1 already satisfies. Please confirm.

---

## I. Estimated effort

**Claude:** roughly **8–10 working turns** for E0.5–E9.
- The base (E1) is mostly a port of validated Round C code.
- The lid and solar stages (E2–E4) are the bulk: a new layout generator, but the geometry comes from the B.1 / D.1 models.

**Owner:**
- ~10 min to create the Part Studio and insert features (at E1, then new features at later stages).
- ~30–45 min for the Assembly and mates at E7, with a click list.
- Review at the E1 and E7/E8 gates.

---

## J. Estimated Onshape API usage (current total ~100 / 2,500)

| Stage | Calls (est.) |
|---|---|
| E0 | ~1 (done) |
| E0.5 YAML reconciliation | 0 |
| E1 base: 1–2 scratch runs + create Feature Studio + put | ~15–22 |
| E2 lid | ~10–20 |
| E3 + E4 solar (B.1-style 6-state kernel cross-check) | ~20–30 |
| E5 hinge | ~10–12 |
| E6 envelopes / service / fasteners | ~10–12 |
| E7 connector fixes, if any | ~2–5 |
| E8 validation harness (2–3 runs) | ~20–30 |
| E9 cleanup | ~5–12 |
| **Total** | **~95–145** (≈ 4–6 % of the annual allocation) |

Everything checkable locally (layout, sweeps, collisions) stays in Python. Kernel runs are reserved for cross-checks.

---

## K. Implementation sequence

1. **E0 (this):** approval gate for the plan, E0.5 items, lid default, the H4 limit, H5 hinge representation, D-008, the H12 wording, and the Assembly method.
2. **E0.5, YAML reconciliation (local):**
   - Update the working values; add spec rows.
   - Extend the generators with `--target`; regenerate.
   - Re-run B.1 / C.2 / D.1 locally to confirm the numbers are unchanged. No API.
3. **E1, base:**
   - Port `nomadBuildBaseV01` into `NOMAD_E_Prototype.fs`; add appearances, names and mate connectors.
   - Local check; one scratch run.
   - **Create the Feature Studio persistently**, then you create the Part Studio and insert "NOMAD E Base" + "NOMAD E Service". **Review gate.**
4. **E2, lid shell / display:** `e_prototype_layout.py` lid block (class A / B / C), frame with slots and notches, display, rear shell, controller band; local checks (D.1 stack, slots vs V1 openings); scratch run; put.
5. **E3, cassettes:** cassette frame + panel face + bracket, both sides, stowed.
6. **E4, rails / carriages / hub:** C-channel rails (strip toggle), carriages, pins, loops, corridor, twist zones, mate connectors. Local B.1 sweep with the new stack; kernel cross-check of the B.1 six states; put.
7. **E5, hinge:** knuckles, leaves and notches within the reserves, hinge connectors. A.2b / C.2 sweeps locally; scratch run; put.
8. **E6, envelopes / service / fasteners:** remaining envelopes, representative fasteners at the existing bosses and screw stations, the "NOMAD E Check" feature; put.
9. **E7, Assembly:** you build it with the click list. I verify the connector names and axes and fix them if needed.
10. **E8, validation:**
    - Local full sweep plus 2–3 kernel harness runs (closed, 105, 120, 135; slides 0 / ½ / 1; tilts ±75 at full extension); you run the 15-step acceptance test.
    - **Any collision → STOP and report** (what, where, which parameter, whether it contradicts a study, options).
11. **E9, visual cleanup:** colours, names, light fillets on the outer shells (optional). Final report, build-log, CLAUDE.md.

**Clearances verified in E8** (reusing the validated models):

| Check | Model |
|---|---|
| Closed lid and 0–135° sweep | A.2b, C.2 |
| Hinge | A.2b / E5 |
| Keyboard / trackpad vs display | A.1 |
| Pi / shell, battery / service | Round C checks |
| Cassette vs lid, cassette vs base, rail vs display, carriage vs wall, corridor, deployed | B.1 / D.1 |
| Side-port zones | C.2 |
