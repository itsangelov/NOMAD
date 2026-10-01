# NOMAD Virtual V1: current-state audit

## Verdict first

**NOMAD is less complete than the round-by-round reports suggest.** The mechanical exploration is deep and careful: chassis envelopes, lid stack-ups, two complete solar architectures, hinge kinematics and cable routing, much of it kernel-checked. But it is built almost entirely on **placeholder envelopes**. No part of the machine is FROZEN.

The electrical side of V1 (battery, power electronics, power budget, thermal budget, BOM) **has not started**. Three things also undermine the current state:

1. **Most of the engineering is not in Git.** The last commit is `d43201c` (P0.1 coupons, 2026-09-25). Everything since — Rounds C through E, D-009, D-010, and all their tools, studies and FeatureScript — exists only as **60 uncommitted paths** (15 modified files and 45 untracked paths, some of them whole folders). One disk failure would lose about five days of work.
2. **The SB-261 hinge work is not in the repo at all.** It covers hinge research, IGES verification, 3D validation and the coupon. The build log stops on 2026-09-29, and no file mentions SB-261. It lives only in the temporary session scratchpad, my private memory notes and the connector's scratch Onshape workspaces.
3. **The documented architecture contradicts the work being done.** `decisions.md` still says **D-010 (A vs B1) is "pending owner decision. Nothing is chosen."** `nomad.yaml`, the persistent `NOMAD_E_Prototype` and D-004/D-009 all still describe architecture **A** (sliding cassettes, class-A 37.6 mm lid). All recent work (SB-261 and the B1 hinge rail) assumes **B1**. This is not a design flaw, but the decision record is missing.

**What I inspected:** the Git history and status, all of `docs/`, `nomad.yaml` (every parameter), the CAD and tools inventory, the build log, the D-010 Phase 2 study, a live run of the Round C base checker, and the list of Feature Studios in the NOMAD Onshape document (1 API request).

**What I could not inspect (UNKNOWN):** which Part Studios and Assemblies exist in Onshape, and whether the owner built the E-prototype assembly or mates. The connector cannot list them.

---

## Current-state facts that matter

| Fact | Evidence |
|---|---|
| **`nomad.yaml`: 0 of about 140 mechanical parameters have authoritative values except a handful** | Only DISPLAY_DIAGONAL and the two active-area dimensions, KEYBOARD_W/D/T, PI_W/D, NVME_FORMAT, FASTENER_SIZE and SOLAR_ROTATION_* have values, all *provisional* or *derived*. Every body, lid, solar, battery and I/O dimension is `TBD` with a working placeholder |
| **Base dimensions are placeholders** | 301 × 235 × 40: width and depth come from target keyboard and trackpad sizes; BODY_HEIGHT 40 is an explicit placeholder |
| **Base checker passes, with one known conflict** | Round C checker run today: 537 pair checks pass. **The lid sweep vs the rear plug zone is −7.0 mm at 135°** (open since Round C) |
| **Open base findings** | E1 findings F1 (11 panel screw heads into walls) and F2 (4 sled screw heads into the service panel) |
| **Decision status** | D-001/2/3/4/5/6/8/9 accepted. **D-007 (base architecture) proposed, not accepted. D-010 pending.** D-009 has open items: ±80° stops not packaged, and the hub bracket is below SF 2 |
| **Onshape (NOMAD document)** | Feature Studios: `NOMAD_P01_Coupons`, `NOMAD_E_Prototype` (behind the local copy: D-009 not written), `NOMAD_D010_Concepts`. **There is no `NOMAD_P01` studio in Onshape** (local only) |
| **Physical testing** | **Nothing has been printed or measured.** The P0.1/P0.2 coupons and the SB-261 coupon are designed only |
| **Electronics docs** | `hardware.md`: only the Pi 5 is "selected"; everything else is candidate or TBD. `power.md`: power budget table **empty**. No BOM file exists |

---

## Subsystem audit (A–Z)

The table columns cover status, current state, dependencies, remaining work, and whether it can be done for €0, needs hardware or a test, or blocks Virtual V1.

| # | Subsystem | Status | Current state | Depends on | Remaining work | €0? | Hardware / test needed? | Blocks V1? |
|---|---|---|---|---|---|---|---|---|
| A | Overall architecture | **BLOCKED** | Clamshell form factor and D-003 layout accepted. Base placement proposed (D-007). Solar architecture undecided (D-010) | Owner decisions D-010, D-007 | Record both decisions; supersede D-004/D-009 if B1 | yes | no | **yes** |
| B | Compute | DEFINED | Pi 5 8 GB "selected". Stack Pi + Active Cooler + M.2 HAT+ + 2230 NVMe is a placeholder 30 mm, not measured | — | Build the stack envelope from official drawings; confirm cooler vs. a fan duct | yes | measuring the real stack eventually | yes (drives BODY_HEIGHT) |
| C | Display | DEFINED | Requirements only (10.1", 1920×1200, ≥400 nit, HDMI, ≤6 W). **No SKU.** Module size, thickness and controller board are placeholders | — | Select a panel and driver board with drawings; decide where the controller goes | yes | no (datasheet) | **yes** (lid stack, power, hinge torque) |
| D | Keyboard | DEFINED | Target 280 × 105 × ≤8 mm, USB HID. **No SKU** | — | Select it, get dimensions | yes | maybe fit check | **yes** (sets BODY_WIDTH and DEPTH) |
| E | Trackpad | DEFINED | Candidate Perixx PERIPAD-501 II (~86 × 75 × 13, approximate) | — | Confirm dimensions and mounting from the vendor | yes | fit check later | partly |
| F | Chassis / enclosure | IN PROGRESS | Round C envelope model plus E1 in Onshape; service, assembly and printability checks pass; F1/F2 open; 310 mm print bed or split | B, C, D, J, K, L, O | Re-baseline on real envelopes, fix F1/F2, set the shell split | yes | P0.2 coupons | **yes** |
| G | Lid | **BLOCKED** | A: class-A sandwich 37.6 (pending P0.2). B1: core 19 (EST) + 6 mm gap + 6 mm leaf = 31 (EST). Not in `nomad.yaml` | D-010, C | Lid stack from the real display and controller | yes | P0.2 (shell stiffness) | **yes** |
| H | Solar system | **BLOCKED** | A: D-009 open (stops, hub bracket SF < 2), cable routing judged not V1-acceptable. B1: P108 panel (vendor data), vented gap, stay, cable routed with R ≥ 12 in concept | D-010 | After the decision: migrate B1 into the authoritative parameters | yes | mock-up / coupon | **yes** |
| I1 | Display (lid) hinges | DEFINED (weak) | D-006 direction only (axis at the rear face). Hardware TBD. Torque need about 1.5–1.8 N·m each for B1 (CALC, D-010). Ø8 placeholder barrel | G, H, mass/CG | Select hardware; resolve the rear-plug conflict | yes | torque test | **yes** |
| I2 | Solar leaf hinge (B1) | **PHYSICAL VALIDATION REQUIRED** | SB-261-6 IGES-verified; 0–190° validated in kernel; coupon designed. Only valid if D-010 = B1 | D-010 | Print and test the coupon; **move the records into the repo** | coupon ≈ hinge cost | yes | no (virtually done) |
| J | Battery | **UNKNOWN** | Volume reserved (90 × 82 × 30). No chemistry, voltage, capacity or pack. **No runtime requirement exists** | W, runtime target | Requirement, then sizing, then pack selection | yes | no (datasheets) | **yes** |
| K | Power management / charging | **UNKNOWN** | "Ready-made modules", 90 × 45 × 20 reserve. No BMS, charger, MPPT (P108 is an 18 V panel) or 5 V/5 A Pi supply chosen | J, W | Architecture plus module selection | yes | bench test later | **yes** |
| L | Cooling / thermal | **UNKNOWN** | Duct volume reserved only; "thermal design not done" | B, W, X | Fan or passive decision; vents | yes | thermal test later | **yes** |
| M | Storage | DEFINED | 512 GB 2230 NVMe via M.2 HAT+ (provisional) | B | Pick a model (dimensions are standard) | yes | no | no |
| N | GNSS | DEFINED | Candidate SparkFun DAN-F10N pHAT, not stacked; antenna and keep-out TBD | layout | Choose an antenna and its placement | yes | reception test | partly |
| O | Ports / connectors | **BLOCKED** | Two rear port panels reserved; **connector list undefined**; rear-plug vs lid sweep conflict (−7.0 at 135° for lid A) | I1, G, port list | Define the port list; resolve the conflict | yes | no | **yes** |
| P | Internal cable routing | IN PROGRESS | Base corridors (Round C); B1 solar cable routed (867 mm, R ≥ 12, concept). No harness list or connectors | F, J, K, O | Harness list after the components are known | yes | fit at build | partly |
| Q | Audio | **UNKNOWN** | Never specified | owner | Decide include/exclude (suggest optional) | yes | — | no, if deferred |
| R | Physical controls | **UNKNOWN** | **No power button or switch defined**, even though one is needed | K | Define power on/off, reset, indicators | yes | — | **yes** (minimal) |
| S | Fasteners / inserts | DEFINED | M2.5/M3 + heat-set; INSERT_SIZE TBD; hinge inserts identified (Ruthex M3 L5.7, PartsBuilt M2.5×4) | P0.2 | Set INSERT_SIZE and BOSS rules from coupons | yes | yes (coupons) | no |
| T | Serviceability | DEFINED | Round C: every module serviceable from below; battery door; no glue (checker PASS) | F | Re-check after re-baseline | yes | — | no |
| U | Structural validation | **PHYSICAL VALIDATION REQUIRED** | Screening and hand calculations only (B.2, D, D.1, D-009, B1). P0.2 package ready, not printed | — | Print and test | low | yes | no (virtual side done) |
| V | Weight / CG | IN PROGRESS | D-010 estimate 2.62 kg (EST, item list); stability and tipping calculated | BOM | Recompute from real component masses | yes | weigh at build | partly |
| W | Power budget | **UNKNOWN** | Table empty | B, C, D, E, N, L | Datasheet-based idle/typical/peak budget | yes | measure later | **yes** |
| X | Thermal budget | **UNKNOWN** | Only the solar/lid heating study (D-010) | W, L | Internal heat load and dissipation path | yes | thermal test | **yes** |
| Y | BOM | **BLOCKED** | Does not exist | selections | Build it after selection | yes | — | **yes** |
| Z | Assembly / manufacturing plan | IN PROGRESS | Fragments: base assembles from below, printability checks, P0.2 print card. No overall plan; bed size / split open | F, G, Y | Part list, print plan, assembly order | yes | — | yes |

---

## Virtual vs physical

**A. Can be completed entirely virtually (€0):**
- Owner decisions D-010 and D-007; a requirements sheet (runtime, ports, controls, audio, temperature range).
- Datasheet-based power budget; battery sizing; power architecture; thermal budget.
- Re-baselining `nomad.yaml` and an integrated layout.
- Lid stack for B1; display hinge torque; resolving the rear-port conflict.
- Cable harness list, mass/CG, BOM structure, assembly plan.

**B. Needs real component data, but can be designed before buying:**
- Display panel and driver board; keyboard; trackpad dimensions; Pi stack height (official drawings); battery cells or pack; BMS, charger, MPPT, 5 V/5 A regulator; fan; GNSS antenna; display hinges; port connectors; power switch.
- All need datasheets or drawings, not purchases.

**C. Needs physical validation:**
- SB-261 coupon (insert walls, 0.5 mm gap, torque).
- P0.2 coupons (lid shell stiffness, inserts, clearances).
- Display hinge torque and holding.
- B1 stay and tipping mock-up.
- Thermal behaviour of the closed lid in sun (6 mm gap and foil).
- Actual power draw (Pi 5 under the real workload).
- GNSS reception through the enclosure; print tolerances (CLEARANCE, MIN_GAP).

**D. Cannot responsibly be settled until the physical build:**
- Final runtime; real internal temperatures and fan need; real mass and CG.
- Wind behaviour; long-term hinge torque drift; PETG/ASA creep in the sun; EMI to GNSS.

---

## Hardware still to select

| Component | Known part / candidate | Interface | CAD / drawing | Select without buying? | Blocks CAD? |
|---|---|---|---|---|---|
| Compute | **Raspberry Pi 5 8 GB** (selected) | 5 V / 5 A, HDMI, USB, PCIe | Official mechanical drawings (STEP availability to verify) | yes | stack height → BODY_HEIGHT |
| Cooler | Active Cooler (assumed) or fan + duct | 5 V fan header | official drawing | yes | yes |
| NVMe carrier + SSD | M.2 HAT+ + 2230 512 GB (any) | PCIe | HAT+ drawing; 2230 standard | yes | minor |
| Display + driver | **none** | HDMI + power (≤6 W target) | depends on SKU | yes | **yes** (lid) |
| Keyboard | **none** (280 × 105 × ≤8 target) | USB | depends | yes | **yes** (base size) |
| Trackpad | Perixx PERIPAD-501 II (candidate) | USB | none known | yes | yes |
| GNSS + antenna | SparkFun DAN-F10N pHAT (candidate); antenna TBD | UART/I²C/PPS | SparkFun board files | yes | minor |
| Battery | **none**; chemistry and voltage UNKNOWN | — | — | yes | **yes** (base layout, mass) |
| BMS / charger / MPPT / regulators | **none** | must accept the 18 V-class P108 and supply 5 V/5 A | depends | yes | **yes** |
| Solar panel | Voltaic P108 (B1 candidate, 273 × 223 × 4, 9.5–10.9 W, vendor data) | Voltaic connector | vendor drawing | yes | if B1 |
| Leaf hinges | **SB-188-SB-261-6** (IGES verified) | screwed flags | IGES ✓ | yes (validation needs the hinge) | no |
| Display hinges | **none** (~1.5–1.8 N·m each) | — | — | yes | **yes** |
| Leaf stay | concept (stainless arms 3 × 16) | — | — | yes | if B1 |
| Ports, power switch, fan, audio | **undefined** | — | — | yes | port panels |
| Fasteners / inserts | M2.5/M3; Ruthex M3 L5.7; PartsBuilt M2.5×4 OD 3.55 | — | standard | yes | no |

---

## Dependency graph (from the actual project)

```
[0] Secure the record: commit the 60 local paths + migrate the SB-261 work (owner approval)
[1] Owner decisions: D-010 (A vs B1) ── D-007 (base architecture)
[2] V1 requirements sheet: runtime target, port list, controls, audio, temperature range
        │
[3] Component down-select from datasheets: display+driver, keyboard, trackpad, Pi stack, fan, GNSS
        │
[4] Power budget (datasheet) ──► [5] Battery sizing + power architecture (BMS/charger/MPPT/5 V)
        │                                   │
        └──► [6] Thermal budget + cooling concept
                                            │
[7] Re-baseline nomad.yaml with real envelopes ◄──────┘
        ├──► base layout (BODY_HEIGHT, F1/F2) 
        └──► lid stack (display + controller, B1 gap/leaf) ──► [8] display-hinge torque → selection
                                                                   └──► rear-port conflict resolution
[9] Integrated Virtual V1 model (base + lid + leaf + hinges + harness) ──► mass/CG/stability
[10] BOM + pricing ──► staged purchasing ──► physical validation (coupons, mock-ups)
```

**Critical path:** [1] D-010 → [2] runtime/port requirements → [3] display and keyboard selection → [4–5] power budget and battery/power electronics → [7] re-baselined layout and lid stack → [8] display hinges and rear ports → [9] integrated model → [10] BOM.

---

## Virtual V1 gap list

- **CRITICAL:**
  - D-010 and D-007 not decided.
  - No runtime requirement.
  - No display or keyboard SKU.
  - No power budget, battery, power electronics or thermal budget.
  - No display hinge.
  - Rear-port / lid-sweep conflict.
  - Port list and power switch undefined.
  - `nomad.yaml` and the E-prototype still describe architecture A.
  - No integrated model; no BOM.
  - Uncommitted work and unrecorded SB-261 work.
- **IMPORTANT:**
  - F1/F2 screw findings.
  - Print-bed size / shell split.
  - Cable harness list and connectors; GNSS antenna placement.
  - ASA vs PETG for sun-exposed parts.
  - `NOMAD_E_Prototype` in Onshape behind the local copy.
- **PHYSICAL VALIDATION:** SB-261 coupon; P0.2 coupons; display-hinge torque; B1 stay/tipping mock-up; closed-lid thermal; real Pi power draw; GNSS reception; FDM clearances.
- **OPTIONAL:** audio; lid class B/C variants; wordmark; A-architecture items (D-009 stops and hub bracket) if B1 is chosen.
- **UNKNOWN:** runtime target; battery chemistry and voltage; whether the Pi 5 needs active cooling inside a closed shell; display controller location; final mass.

---

## NOMAD VIRTUAL V1 STATUS

1. **Completion: roughly 20% (±5).** Mechanical architecture exploration is perhaps 60% done, but on placeholders. Electrical, power, thermal and BOM, about half of Virtual V1, are near 0%. Nothing is frozen.
2. **FROZEN: 0**
3. **DEFINED: 9** (B, C, D, E, I1, M, N, S, T)
4. **IN PROGRESS: 4** (F, P, V, Z)
5. **BLOCKED: 5** (A, G, H, O, Y)
6. **UNKNOWN: 7** (J, K, L, Q, R, W, X)
7. **PHYSICAL VALIDATION REQUIRED: 2** (I2 SB-261 leaf hinge, U structural); **DEFERRED: 0.** That is 27 items, with hinges split into display (I1) and leaf (I2).
8. **Critical path:** D-010 → requirements → display/keyboard selection → power budget → battery and power electronics → re-baselined layout and lid stack → display hinges and rear ports → integrated model → BOM.
9. **Next tasks, in dependency order:**
   1. Secure the record. Commit the local work, and migrate the SB-261 study, IGES findings and coupon spec into `prototypes/` with build-log entries. Needs your approval.
   2. Record D-010 (and D-007). If B1: mark D-004/D-009 superseded and plan the `nomad.yaml` lid/solar migration.
   3. Write the V1 requirements sheet: runtime target, port list, controls, audio, operating temperature.
   4. Down-select the display + driver and keyboard (plus confirm trackpad, Pi stack, fan, GNSS antenna) from datasheets and drawings.
   5. Datasheet power budget (idle, typical, peak).
   6. Battery sizing and power architecture (BMS, charger, MPPT for P108, 5 V/5 A rail, power switch).
   7. Thermal budget and cooling concept.
   8. Re-baseline `nomad.yaml` and re-run the base layout and lid stack with real envelopes.
   9. Select display hinges and resolve the rear-port conflict.
   10. Integrated Virtual V1 model, then mass/CG, then BOM and pricing.
10. **€0 tasks:** all ten. Only the physical validations after them cost money (SB-261 hinges and coupons, P0.2 prints).
11. **Do NEXT:** task 1 (secure the record, a few minutes once you approve), then **task 2, the D-010 decision**. Every lid, solar, hinge and port item depends on it. Without it, all further work risks being done on the wrong architecture again.

I made no file changes, no CAD changes, no commits and no Onshape writes; this was one read-only Onshape call. I've started none of these tasks.