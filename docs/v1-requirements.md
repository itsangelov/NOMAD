# NOMAD V1 Requirements

**Revision:** 2026-10-01, written when D-010 = B1 was locked. **Research reference (2026-10-02):** `docs/E-POWER-RESEARCH-CAMPAIGN.md`. It is research only; requirement statuses below are unchanged, and the owner decisions it lists are pending. **Updated 2026-10-01 by E-POWER-001** (hardware and energy characterization, `prototypes/V1/E-POWER-001_hardware_energy_characterization.md`): sourced candidate data, preliminary power model, conflicts C1–C14. Planning baseline for the remaining **Virtual V1** work.

**Principle:** finish the virtual design before spending money wherever reasonably possible.

**How to use this sheet:**
- It states **what V1 must do and what is still open**. It does not select hardware, and it invents no values.
- Where a number appears, the source and evidence type are given:
  - **PUB / VENDOR:** manufacturer data
  - **KERNEL:** Onshape scratch model
  - **CALC:** calculated
  - **EST:** estimate
  - **ASSUMED**
- Nothing in NOMAD is physically tested or measured yet.

**Sources of truth:**
- Decisions: `docs/decisions.md`
- Mechanical parameter values: `CAD/parameters/nomad.yaml` (D-002) and `docs/mechanical-spec.md`
- If this sheet disagrees with them, they win and this sheet must be corrected.

## 1. Status scheme

| Status | Meaning |
|---|---|
| **LOCKED** | Owner or architecture decision is established |
| **DEFINED** | A target exists, but the implementation is not finalized |
| **CANDIDATE** | A hardware or design candidate, not final |
| **TBD** | Unresolved |
| **VALIDATION REQUIRED** | A virtual design exists, but physical proof is still required |
| **BLOCKED** | Cannot responsibly proceed without another dependency (named) |

## 2. System

| ID | Requirement | Status | Source / notes |
|---|---|---|---|
| SYS-1 | **NOMAD V1 scope:** a portable, self-contained field computer built around compute, storage, offline knowledge, offline maps, GNSS navigation, local AI, display, controls, battery power and solar generation. V1 is the validated prototype stage (revisions P0.1 → P0.2 → P1 → V1) | DEFINED | `README.md`, `CLAUDE.md`. The software feature set and communications hardware are not yet specified (TBD) |
| SYS-2 | **Offline-first:** "assume the infrastructure is gone" | LOCKED | Project principle (`README.md`, `CLAUDE.md`) |
| SYS-3 | **No cloud dependency for core operation.** Compute, storage, maps, navigation, knowledge and local AI work with no network | LOCKED | Owner, 2026-10-01; follows SYS-2 |
| SYS-4 | **Form factor:** clamshell. The base holds the keyboard, trackpad, electronics and battery. The lid holds the 10.1" display, with the B1 solar leaf behind it | LOCKED (architecture) | D-003, D-006 (direction), D-010 |
| SYS-5 | **Envelope:** base working 301 × 235 × 40; B1 closed about 301 × 235 × 73.0 | TBD | Working inputs and CALC only (`nomad.yaml`, D-010 Phase 2). Set by real hardware envelopes (step 3) and the re-baseline (step 7) |
| SYS-6 | **Serviceability and modularity:** the battery is removable and never sealed; no glue; modules are replaceable; fasteners are standard | LOCKED (principle) | `CLAUDE.md` priorities; `docs/power.md`. The base service architecture is proposed in D-007 (not accepted) |
| SYS-7 | **Operating concept** (details in §8): table-top use, lid open about 105–110° (working). The B1 leaf is deployed and aimed by hand, with the stay deployed at high leaf angles. It charges while closed. Manual only, no motors | DEFINED | `CLAUDE.md` (no motors without approval); D-010 Phase 2 named states |
| SYS-8 | **Priorities, in order:** function, reliability, serviceability, modularity, mechanical simplicity, manufacturability, offline capability, expandability, aesthetics | LOCKED | `CLAUDE.md` |
| SYS-9 | Target ambient operating and storage temperature range | TBD | Not set by the owner. D-010 used 35 °C as a calculation case only |
| SYS-10 | **Energy-system principle:** NOMAD's solar system is a field energy replenishment system, not its primary power source. B1 deploys a larger panel when stationary while keeping NOMAD compact when stowed. No energy independence and no runtime extension is claimed until a power budget and a solar-yield model exist | LOCKED (principle) | Owner, 2026-10-01 (E-POWER-001); `docs/power.md` |

## 3. Compute

| ID | Requirement | Status | Source / notes |
|---|---|---|---|
| CMP-1 | Raspberry Pi 5, 8 GB | LOCKED (current selection) | `docs/hardware.md` "selected" |
| CMP-2 | **Storage:** 500–512 GB NVMe, 2230 preferred, through the Raspberry Pi M.2 HAT+ (Standard: 2230/2242, ≤ 3 A to the device, 16 mm stacking header so it fits over the Active Cooler) | DEFINED (target) / CANDIDATE (HAT+, Raspberry Pi SSD 512 GB) | MFR briefs (E-POWER-001 §2.3). 2230 + HAT+ + Active Cooler compatible on paper. SSD power not published; reference SN740 512 GB: 50 mW avg active, ≤ 4.7 W max |
| CMP-3 | **Active cooling** is required for the Pi 5. The Active Cooler is temperature-controlled by firmware (0 % below 50 °C, 100 % at 75 °C); passive cooling is not assumed sufficient | DEFINED / CANDIDATE (Active Cooler) | MFR (E-POWER-001 §2.2). The Active Cooler current is not published; the fan draws from the Pi's USB budget |
| CMP-4 | Pi stack height (Pi + Active Cooler + 16 mm stacking header + HAT+ + NVMe) | TBD | Working 30, not measured. The Active Cooler drawing suggests 13.7 (inferred). Verify against the drawings (E-POWER-001 C8) |
| CMP-5 | Compute placement in the base | TBD | D-007 proposes the right palm-rest bay; not accepted |
| CMP-6 | Remaining compute hardware (cooler model, HAT+, SSD, RTC battery, any expansion) | TBD | |

## 4. Display

| ID | Requirement | Status | Source / notes |
|---|---|---|---|
| DSP-1 | **Target class:** about 10.1" IPS, 1920 × 1200 (16:10), ≥ 400 nit (500+ preferred), matte, non-touch, HDMI, ≤ 6 W. **The ≤ 6 W target needs a brightness condition:** the best-documented panel draws 6.8 W typ / 7.8 W max at full backlight before the controller (E-POWER-001 C1) | DEFINED | `docs/architecture.md`, `docs/hardware.md`; MFR Winstar data |
| DSP-2 | **Display panel and controller.** Shortlist: Winstar WF101NTYA4LNN0 (500 nit, LVDS, anti-glare, −20…+70 °C, best documented); AUO B101UAN01.C (400 nit, eDP, glossy, 0–50 °C, 3P data); Waveshare 10.1inch HDMI LCD (G) (integrated HDMI controller, touch, data incomplete). The controller board is uncharacterized | CANDIDATE (panels) / TBD (controller) | E-POWER-001 §2.4. Not selected |
| DSP-3 | **Physical envelope:** outline, thickness, controller size and location (lid band or base), cable exit | TBD | Candidate panels: 231.4 × 152.3 × 9.1 (Winstar) / 229.7 × 150.3 × 4.6 (AUO). Both exceed working `DISPLAY_HEIGHT` 150 or `DISPLAY_THICKNESS` 5 (E-POWER-001 C2). Controller TBD (C3) |
| DSP-4 | Display temperature rating vs closed-in-sun heating (B1 with foil: display about 50–57 °C at 35 °C ambient, EST) | TBD | D-010 Phase 2 §13; LCD limits are unknown until the panel is selected |

## 5. Keyboard

| ID | Requirement | Status | Source / notes |
|---|---|---|---|
| KBD-1 | **Envelope target:** about 280 × 105 × ≤ 8 mm | DEFINED | `nomad.yaml` provisional values (spec target) |
| KBD-2 | Wired USB HID, ultra-low-profile, no battery, no wireless | DEFINED | `docs/hardware.md` |
| KBD-3 | **Actual keyboard model.** Retail wired USB candidates (Perixx PERIBOARD-426 / -416 / -422 / -332 / -409H) are **14–21 mm thick and 116–146 mm deep as sold**. None meets KBD-1. An uncased or OEM keyboard module has not yet been searched | TBD (conflict) | E-POWER-001 §3, C4 |
| KBD-4 | Centred on the chassis centreline, above the trackpad | LOCKED | D-003 |

## 6. Trackpad

| ID | Requirement | Status | Source / notes |
|---|---|---|---|
| TPD-1 | Perixx PERIPAD-501 II: **availability and dimensions unverified** (not listed on the Perixx stores; no official dimensions; the earlier ~86 × 75 × 13 is unverified). Verified alternative: PERIPAD-506, 135 × 116 × 14, USB-C to A | CANDIDATE (unverified) | E-POWER-001 §3, C5 |
| TPD-2 | Centred below the keyboard; the position is parameterized | LOCKED | D-003 |
| TPD-3 | Final envelope, mounting and electrical interface | TBD | D-003 keeps the dimensions TBD until the module is selected |

## 7. Lid

| ID | Requirement | Status | Source / notes |
|---|---|---|---|
| LID-1 | **B1 lid architecture:** a thin core (display, controller zone, back shell), a vented air gap with low-e foil, and the solar leaf on top | LOCKED (architecture) | D-010 |
| LID-2 | B1 lid stack thickness (about 19 core + 6 gap + 6 leaf = 31, EST) | TBD | Needs the actual display stack (DSP-3) |
| LID-3 | **Display-hinge subsystem:** hardware, axis position, torque (about 1.5–1.8 N·m per hinge for B1, CALC), φ-max stop. Candidates: Southco E6-10-216-50 / E6-10-416-50 (1.8 N·m symmetric, 20 000 cycles within ±20 %), E6-10-216F-50 (1.8 / 1.1 asymmetric), TorqMaster SB-188-SB-254-H (1.36–1.69 N·m) | TBD / CANDIDATE | D-006 sets only a provisional rear-face direction. Working closed gap 2.0; lid angles 105 nominal / 135 max (working). Hinge size and fit not verified (E-POWER-001 C11) |
| LID-4 | **Rear-port / lid-sweep interaction must be resolved.** The B1 stack clears the plug keep-out by +2.07 at φ 125 but is −2.3 mm at φ 135 (KERNEL / CALC) | BLOCKED | Needs the display-hinge geometry (LID-3), the lid stack (LID-2) and the I/O policy (PRT-1). Dependency step 8 |
| LID-5 | **Shared display-hinge cable pass** (display cable + solar cable) | TBD | Display cable size unknown (D-010 Phase 2 §12) |
| LID-6 | **Final lid geometry** | BLOCKED | Needs the actual display stack (DSP-3) and the display hinge (LID-3) |

## 8. Solar

| ID | Requirement | Status | Source / notes |
|---|---|---|---|
| SOL-1 | **B1 solar leaf:** one leaf behind the display lid, hinged at the lid top edge | LOCKED | D-010 |
| SOL-2 | **Usable leaf motion** about 0–190° (`SOLAR_LEAF_ANGLE_MAX` 190) | DEFINED; VALIDATION REQUIRED | Owner target. KERNEL: ≥ 2.03 mm at 190°, first contact 201° (`prototypes/B1_SB261/`) |
| SOL-3 | **Leaf hinges:** two structural friction hinges. Current selected candidate: TorqMaster SB-188-SB-261-6 | CANDIDATE; VALIDATION REQUIRED | Torque 0.96–1.13 N·m per hinge (PUB) vs about 0.83 required (CALC), SF ≈ 1.16. Load, material and temperature unpublished. Coupon designed, not printed |
| SOL-4 | **Panel:** Voltaic P108: 9.92 W peak, Voc 20.45 V, 17.34 V / 570 mA, 22.3 × 27.4 × 0.4 cm, 328 g, 3.5 × 1.1 mm plug, 50 cm cable (MFR, 2026-10-01). Isc and temperature ratings are not published | CANDIDATE | Not selected. Replaces the earlier 9.5–10.9 W range. Solar is replenishment only (SYS-10): the 9.92 W peak is below every preliminary load state |
| SOL-5 | **Cable:** dedicated sleeve near the hinge axis; static bends R ≥ 12 (`SOLAR_LEAF_CABLE_BEND_RADIUS`); twist along the axis ≤ 3.5°/mm; leaf connector so the panel can be removed; no slip ring | DEFINED; VALIDATION REQUIRED | Owner concept (D-010). KERNEL: 5 bends at R 12.00, 2.97°/mm over 64 mm. Cable not selected (Ø4 ASSUMED). Twist cycling test needed |
| SOL-6 | **Stay:** mandatory fold-out rear outrigger stay | DEFINED; VALIDATION REQUIRED | Rear tip wind 11.4–18 m/s with the stay vs 2.4–8.3 without (CALC). Design details TBD |
| SOL-7 | **Thermal:** vented gap ≥ 6 mm with low-e foil; sun-exposed parts ASA or light-coloured | DEFINED; VALIDATION REQUIRED | D-010 Phase 2 §13 (EST). Thermal mock-up needed |
| SOL-8 | **Physical validation gate:** the SB-261 coupon migration gate (`prototypes/B1_SB261/COUPON_SPEC.md` §7) and the D-010 Phase 2 §24 mock-ups | VALIDATION REQUIRED | Dependency step 13. **No purchase now** |
| SOL-9 | Leaf latch for transport; PV surface protection (sleeve) | TBD | D-010 Phase 2 §16 / §20 |

## 9. Battery / Power — ARCHITECTURE BASELINE (E-POWER-002, 2026-10-02); parts TBD

**Fixed so far:**
- The battery is removable and serviceable, in a bay that is never sealed (LOCKED, principle).
- Ready-made power modules (DEFINED approach, `docs/power.md`).
- The battery is sized from measured consumption (DEFINED approach).
- The base reserves volume for a battery (90 × 82 × 30) and power electronics (90 × 45 × 20). These are working reserves only (D-007 proposed).

**Status after E-POWER-002.** The values below come from E-POWER-002 (`docs/E-POWER-002-POWER-ARCHITECTURE.md`). Statuses use this sheet's scheme. Specific SKUs remain TBD. Nothing is physically validated.

| ID | Item | Status | Depends on |
|---|---|---|---|
| PWR-1 | **Power budget** (idle / typical / peak per load) | DEFINED (preliminary, published data only); VALIDATION REQUIRED (measurement) | E-POWER-001 §4–§5. Documented subtotals: standby ≈ 10.1–10.9 W, normal ≈ 10.9 W, max sustained ≈ 17.7–22.4 W, each **+ TBD** (display controller, HID, fan, HAT+, conversion losses) |
| PWR-2 | **Battery voltage:** 4S: 16.8 V full / 14.4 V nominal / 12.8 V system cutoff (3.2 V/cell) / 11.2 V BMS floor | DEFINED (baseline) | E-POWER-002 (`docs/E-POWER-002-POWER-ARCHITECTURE.md`) §3–§4: 1S exceeds the charger's 6 A discharge limit; 3S fits only 3 cells |
| PWR-3 | **Chemistry and pack architecture:** Li-ion 21700, **4S1P** (4 cells, single layer); LiFePO4 cannot meet the target in the bay | DEFINED (baseline); cell SKU **TBD (owner)** | E-POWER-002 (`docs/E-POWER-002-POWER-ARCHITECTURE.md`) §4 |
| PWR-4 | **Capacity:** 92 Wh class (4 × Molicel M65A-type, preliminary datasheet) needed for 6 h at end of life with reserve; 71 Wh class (4 × 50E-type) meets the 4 h minimum only | CANDIDATE; **owner decision** | E-POWER-002 (`docs/E-POWER-002-POWER-ARCHITECTURE.md`) §12, §15 |
| PWR-5 | **Runtime target:** 6 h normal interactive use (design target), 4 h minimum acceptable; 8 h reference only; maximum sustained load is a separate stress case | **LOCKED** (owner, 2026-10-02) | Owner direction in the E-POWER-002 brief |
| PWR-6 | **BMS:** on-pack 3–5S protector with OV 4.25–4.30 V, UV 2.8–3.0 V, discharge / charge over-current, short-circuit < 1 ms, NTC, 50 mA passive balancing; plus a 10 A / 32 V DC / ≥ 1 kA fuse and a secondary OV protector (recommended) | DEFINED (requirements); SKU TBD | E-POWER-002 (`docs/E-POWER-002-POWER-ARCHITECTURE.md`) §9 (reference: TI BQ77915) |
| PWR-7 | **Charging:** USB-C PD sink, 20 V 3 A (60 W) preferred, ≥ 45 W minimum; NVDC buck-boost charger (input ≤ 3.3 A, charge ≤ 5 A, baseline 3.2 A); charges while running; no DC barrel recommended | DEFINED (baseline); parts TBD | E-POWER-002 (`docs/E-POWER-002-POWER-ARCHITECTURE.md`) §6–§7 (reference: TI BQ25798, TPS25751 / TPS25730) |
| PWR-8 | **Solar charging:** P108 on the charger's second input; VOC-sampling MPPT (host-enabled); reverse-polarity FET + TVS; VAC OVP 26 V; USB-C priority; never a direct system source | DEFINED (baseline); **VALIDATION REQUIRED** | E-POWER-002 (`docs/E-POWER-002-POWER-ARCHITECTURE.md`) §8 |
| PWR-9 | **Pi 5 rail:** 5.1 V, ≥ 5 A buck from the 12–16.8 V bus; EEPROM `PSU_MAX_CURRENT=5000`; a ≥ 6 A-class part or a verified derating is recommended | DEFINED (baseline); part TBD | E-POWER-002 (`docs/E-POWER-002-POWER-ARCHITECTURE.md`) §5 (E2-R03) |
| PWR-10 | **Display rail:** 12 V ±5 %, ≈ 1 A, buck-boost from the bus (the bus straddles 12 V) | DEFINED (baseline for D-A / D-W controllers) | E-POWER-002 (`docs/E-POWER-002-POWER-ARCHITECTURE.md`) §5; controller location TBD (EP-C02) |
| PWR-11 | **Accessory rails:** USB HID, Active Cooler and GNSS (3.3 V header) are fed through the Pi (1.6 A USB budget); NVMe through the M.2 HAT+; no dedicated 3.3 V rail; an optional fused aux 5 V from the bus for an enclosure fan or future peripherals | DEFINED (baseline); aux rail TBD | E-POWER-002 (`docs/E-POWER-002-POWER-ARCHITECTURE.md`) §5 |
| PWR-12 | **Protection:** pack fuse; BMS functions (PWR-6); input OVP / reverse blocking (charger back-to-back FETs); solar reverse polarity + TVS; charger JEITA; ship mode | DEFINED (requirements) | E-POWER-002 (`docs/E-POWER-002-POWER-ARCHITECTURE.md`) §8–§9 |
| PWR-13 | **Power switch and its behaviour:** soft power via the Pi; charger ship mode for storage; pack connector as the service disconnect | TBD (behaviour / UX) | E-POWER-002 (`docs/E-POWER-002-POWER-ARCHITECTURE.md`) §9 |
| PWR-14 | **Charging / input behaviour:** charge while running (NVDC); USB-C and solar are not summed (one input at a time; USB-C priority enforced by the host); charging limited to 0–45 °C (BMS + charger JEITA), including charging while closed in the sun | DEFINED (baseline); **VALIDATION REQUIRED** | E-POWER-002 (`docs/E-POWER-002-POWER-ARCHITECTURE.md`) §6–§9 |
| PWR-15 | **Off-state drain:** the Pi 5 draws about 1–1.4 W when "off" by default, about 0.01 W with `POWER_OFF_ON_HALT=1`. NOMAD must set the EEPROM option or cut power | DEFINED | MFR (E-POWER-001 C10) |
| PWR-16 | **The 5 V rail feeding the Pi must be 5 A-capable** for the Pi to allow 1.6 A of downstream USB, which the fan and USB HID devices share. Otherwise the limit is 600 mA, or peripherals are powered separately | DEFINED (requirement on the rail; no converter chosen) | MFR (E-POWER-001 C9) |
| PWR-17 | **Battery pack fit:** a tightly bonded 4S1P pack fits 90 × 82 × 30 (1.3 mm per side across the width); a holder-type pack needs ≈ 93.6 × 82 × 31 | **BLOCKED** (owner decision on pack style / bay; D-007 / YAML step 7) | E-POWER-002 (`docs/E-POWER-002-POWER-ARCHITECTURE.md`) §11 |

## 10. Thermal — UNRESOLVED

**Fixed so far:**
- The Pi 5 needs active cooling.
- Cooling airflow must never be blocked, including by service panels (`CLAUDE.md`).
- Round C reserves front intake → duct → Pi → side exhaust (proposed D-007, reserved volumes only).
- The sun-exposed B1 parts and the gap and foil are covered in SOL-7.

| ID | Required future work | Status | Notes |
|---|---|---|---|
| THM-1 | Pi 5 thermal load (W) at the target workloads, including local AI | TBD | Needs PWR-1 |
| THM-2 | Display and controller heat | TBD | Needs DSP-2 |
| THM-3 | Battery thermal constraints (charge and discharge limits) | TBD | Needs PWR-3 |
| THM-4 | Enclosure airflow path, intake and exhaust | TBD | D-007 reserve proposed only |
| THM-5 | Fan and duct selection | TBD | |
| THM-6 | Solar and closed-lid heat: display +15–22 K with gap and foil; panel 66–91 °C at 35 °C ambient (EST) | TBD; VALIDATION REQUIRED | D-010 Phase 2 §13 |
| THM-7 | Ambient operating temperature target | TBD | Owner decision (SYS-9) |
| THM-8 | **Component temperature limits** found so far: M.2 HAT+ 0–50 °C ambient; Pi 5 0–70 °C; Raspberry Pi SSD 0–70 °C; Winstar panel −20…+70 °C; AUO panel 0–50 °C; DAN-F10N −40…+85 °C. The **internal air temperature must stay ≤ 50 °C** while the HAT+ is used | DEFINED (from MFR data) | E-POWER-001 C7 |

## 11. GNSS

| ID | Requirement | Status | Source / notes |
|---|---|---|---|
| GNS-1 | SparkFun GNSS Flex pHAT – DAN-F10N (GPS-29491). The u-blox DAN-F10N is an **antenna module** (internal L1/L5 patch, 20.0 × 20.0 × 11.6). GPS / Galileo / BeiDou / QZSS / NavIC; **no GLONASS**. 2.7–3.6 V, 21 mA tracking / 26 mA acquisition. UART + PPS; U.FL / SMA for an external antenna. Linux support required (unchanged requirement) | CANDIDATE | MFR (u-blox, SparkFun); E-POWER-001 §2.6. Corrects the earlier "GLONASS" listing |
| GNS-2 | Mounted as a separate cabled module, not stacked on the Pi | TBD | Working assumption in D-007 (proposed) |
| GNS-3 | **Antenna:** internal patch (needs sky view) or external L1/L5 active antenna, e.g. u-blox ANN-MB5 (49.14 × 46.14 × 15.94, 17 mA at 5 V, SMA, 3 m cable). Location and keep-out | TBD / CANDIDATE | `GNSS_ANTENNA_KEEPOUT` TBD. D-007's under-keyboard GNSS placement implies an external antenna (E-POWER-001 C6) |

## 12. Ports / Controls — final list NOT defined

The P0.1 reserved-volume list (`docs/mechanical-spec.md`) keeps room for: USB-C, 2–3 × USB-A, HDMI, audio, Ethernet, GPIO, microSD, power and expansion. **That is a space reservation, not a port list.**

| ID | Open item | Status |
|---|---|---|
| PRT-1 | I/O placement policy: rear panels vs side panels (rear is limited by the lid sweep, LID-4) | TBD (owner; D-007) |
| PRT-2 | External USB ports (count, type, data / power) | TBD |
| PRT-3 | HDMI: external video out? Internal display connection (Pi micro-HDMI to the display controller, cable route through the hinge) | TBD |
| PRT-4 | Charging / power input connector | TBD (PWR-7) |
| PRT-5 | External power output, if any | TBD |
| PRT-6 | GNSS external antenna connector | TBD (GNS-3) |
| PRT-7 | Service ports (microSD, debug / UART, GPIO, Ethernet) | TBD |
| PRT-8 | Power button and its behaviour | TBD (PWR-13) |
| PRT-9 | Reset / forced shutdown behaviour | TBD |
| PRT-10 | Indicators (power, charge, solar, storage, GNSS fix) | TBD |
| PRT-11 | Any other external I/O (expansion) | TBD |

## 13. Audio

| ID | Requirement | Status | Notes |
|---|---|---|---|
| AUD-1 | Audio input/output (speaker, microphone, jack) | TBD / optional | Audio is in the reserved port-zone list only. No owner decision on audio hardware |

## 14. Mechanical

| ID | Requirement | Status | Source / notes |
|---|---|---|---|
| MEC-1 | B1 architecture (§7, §8) | LOCKED | D-010 |
| MEC-2 | **Base / lid relationship:** clamshell; display hinge axis at or near the base rear face; closed gap 2.0 (working); lid angles 105 / 135 (working) | DEFINED (provisional direction) | D-006 |
| MEC-3 | **Base layout:** shell with removable bottom service panel and battery door; replaceable trays and sled; module placement | TBD (proposed) | D-007 proposed, not accepted (§17) |
| MEC-4 | **Serviceability:** battery through its own door; electronics through the service panel; no glue; every screw reachable; B1 leaf hinges serviceable with the leaf open (KERNEL: 1.7–4.1 mm driver clearance) | DEFINED | `CLAUDE.md`, D-007 (proposed), `prototypes/B1_SB261/` |
| MEC-5 | **Fastener philosophy:** a small family (M2.5, M3); screws for structure, clips for frequent access, captive or quarter-turn fasteners for service panels, magnets and pins for covers | DEFINED | `CLAUDE.md`; `FASTENER_SIZE` provisional |
| MEC-6 | **Insert strategy:** heat-set inserts for serviced joints. B1 hinge rail: Ruthex RX-M3x5.7 (lid) and M2.5 × 4 OD 3.55 (leaf). Standard 4.6-OD M2.5 inserts are excluded. Insert walls 1.20–1.47 must be proven | CANDIDATE; VALIDATION REQUIRED | `prototypes/B1_SB261/`; `INSERT_SIZE` TBD |
| MEC-7 | **Print-bed constraint:** a one-piece base shell needs a bed of at least 301 × 235 (310-class); the B1 leaf frame (289 × 235) is split into two halves (144.5 × 235) for a 256 bed. The printer or service actually used is not recorded | TBD | Round C.2; D-010 Phase 2 §17 |
| MEC-8 | **Split-print possibility:** base split options screened (C.2); leaf split in two halves with a spliced bar (Phase 2) | DEFINED (options); TBD (choice) | `prototypes/P0.1/c2_architectural_screening.md` |
| MEC-9 | Metal for structural shafts and pins; no structural printed gears | LOCKED (principle) | `CLAUDE.md` |
| MEC-10 | **Structural validation status:** nothing is physically tested. B1 results are KERNEL/CALC. The P0.1/P0.2 coupons (Architecture A rail and lid plates) are not printed and are deferred with A. The SB-261 coupon is designed, not printed | VALIDATION REQUIRED | |

## 15. Mass / CG

| ID | Requirement | Status | Notes |
|---|---|---|---|
| MAS-1 | **Total mass estimate 2.62 kg (2.02–3.34)**, base 1.465 kg nominal, B1 solar 603 g including the stay | TBD (provisional estimate) | CALC from EST (D-010 Phase 2 §7). The battery is not chosen |
| MAS-2 | **CG and stability:** worst rearward CG is behind the rear feet at φ 135 / ψ 135 without the stay; the stay is required | DEFINED (finding); VALIDATION REQUIRED | D-010 Phase 2 §8–§9 |
| MAS-3 | Final mass, CG and stability values | BLOCKED | Need actual component masses (step 3) and the integrated CAD (step 9); analysis is step 10 |

## 16. Manufacturing

| ID | Requirement | Status | Notes |
|---|---|---|---|
| MFG-1 | **FDM PETG** is the current development assumption. Sun-exposed B1 parts are ASA or light-coloured (HDT) | DEFINED | `CLAUDE.md`; D-010 Phase 2 §13 |
| MFG-2 | **Physical coupons are required before production parts** (inserts, walls, gaps, hinge torque) | LOCKED (gate) | `prototypes/B1_SB261/COUPON_SPEC.md` |
| MFG-3 | **Real hardware measurements are required** before final interfaces (display, keyboard, trackpad, Pi stack, panel, hinges) | LOCKED (gate) | CLAUDE.md: physical testing is authoritative for fit and motion |
| MFG-4 | **Final print strategy** (orientation, splits, material per part, in-house vs service) | TBD | Not frozen |

## 17. Open owner decisions (not made here)

| Decision | Needed for |
|---|---|
| **D-007:** accept as working, amend or reject the base placement (compute right palm bay, battery left bay, electronics under the keyboard), the I/O policy (rear vs side), GNSS as a separate module, the shell structure (one body vs split), and whether the working 301 × 235 × 40 envelope stays (`c2_architectural_screening.md` §4) | Steps 7–9 |
| ~~Runtime target (PWR-5)~~ — decided 2026-10-02: 6 h normal target / 4 h minimum | — |
| **Battery cell basis:** M65A-class (preliminary; meets 6 h) or a mature 50E-class cell (meets 4 h, ≈ 5.8 h at end of life) (PWR-4; E-POWER-002 §15) | Steps 5–7 |
| **Battery pack style / bay:** a tightly bonded pack in 90 × 82 × 30, or a holder-type pack with the bay grown to ≈ 93.6 × 82 × 31 (PWR-17) | Step 7, D-007 |
| **Display direction** D-A vs D-W (E-POWER research §19; D-W misses 6 h at end of life with reserve) | Steps 3, 5–9 |
| **Charging input:** confirm USB-C PD only (60 W preferred / 45 W minimum), no DC barrel (PWR-7) | Step 8 |
| Ambient operating temperature target (SYS-9 / THM-7) | Step 6 |
| Port and control list (§12) | Steps 8–9 |
| Audio in or out of V1 (AUD-1) | Step 3 |

## 18. V1 dependency order (remaining virtual work)

**The rule:** finish the virtual design before spending money wherever reasonably possible. Physical work starts at step 12.

1. **D-010 B1 architecture formalization.** Done 2026-10-01.
2. **V1 requirements.** This sheet, 2026-10-01.
3. **Down-select real hardware envelopes.** First pass done 2026-10-01 (E-POWER-001): candidates characterized, conflicts C1–C14 open:
   - display and controller
   - keyboard and trackpad
   - Pi stack, cooler and SSD
   - GNSS and antenna
   - display hinges
   - panel confirmation
   - Use datasheets and published drawings only. €0.
4. **Establish the power budget** from datasheets (PWR-1). Preliminary model done 2026-10-01 (E-POWER-001); it gets refined as step 3 closes.
5. **Establish the battery / power architecture** (PWR-2 … PWR-14). Baseline done 2026-10-02 (E-POWER-002). Owner decisions on cell basis, bay and display remain (E-POWER-002 §15).
6. **Establish the thermal architecture** (§10).
7. **Re-baseline `nomad.yaml`:**
   - B1 lid stack
   - real envelopes
   - retire the A parameters from the active set
   - D-007 decision
8. **Resolve the display-lid hinge and rear-port conflict** (LID-3, LID-4, PRT-1).
9. **Integrate the complete Virtual V1 CAD.**
10. **Mass / CG / stability analysis** (§15).
11. **BOM and pricing.**
12. **Staged purchasing.** The first stage is the validation parts: SB-261 hinges and inserts for the coupon, cable samples.
13. **Physical validation:**
    - SB-261 coupon
    - D-010 Phase 2 §24 mock-ups
    - thermal
    - hardware fit measurements
14. **Physical build.**
