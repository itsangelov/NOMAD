# NOMAD V1 Requirements

**Revision:** 2026-10-01, written when D-010 = B1 was locked. **Research reference (2026-10-02):** `docs/E-POWER-RESEARCH-CAMPAIGN.md`. It is research only; requirement statuses below are unchanged, and the owner decisions it lists are pending. **Updated 2026-10-01 by E-POWER-001** (hardware and energy characterization, `prototypes/V1/E-POWER-001_hardware_energy_characterization.md`): sourced candidate data, preliminary power model, conflicts C1–C14. Planning baseline for the remaining **Virtual V1** work.

**Principle:** finish the virtual design before spending money wherever reasonably possible.

> **Virtual V1 integration update (2026-10-06):** `docs/V1-VIRTUAL-INTEGRATION.md`. Real candidate hardware, the integrated base and lid layout, display hinges, power budget, thermal, harness, mass/CG, DFM and BOM. The affected rows below are updated in place and point to it. The V1 placement is **proposed as D-011** (owner acceptance needed). The decisions still owed are in §17.

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
| SYS-5 | **Envelope:** base 306 × 253 × 40; closed 306 × 253 × 73 (+ 4 mm feet) | DEFINED (provisional); owner confirmation | `nomad.yaml` (formulas); V1 §8 |
| SYS-6 | **Serviceability and modularity:** the battery is removable and never sealed; no glue; modules are replaceable; fasteners are standard | LOCKED (principle) | `CLAUDE.md` priorities; `docs/power.md`. The base service architecture is proposed in D-007 (not accepted) |
| SYS-7 | **Operating concept** (details in §8): table-top use, lid open about 105–110° (working). The B1 leaf is deployed and aimed by hand, with the stay deployed at high leaf angles. It charges while closed. Manual only, no motors | DEFINED | `CLAUDE.md` (no motors without approval); D-010 Phase 2 named states |
| SYS-8 | **Priorities, in order:** function, reliability, serviceability, modularity, mechanical simplicity, manufacturability, offline capability, expandability, aesthetics | LOCKED | `CLAUDE.md` |
| SYS-9 | Target ambient operating and storage temperature range | DEFINED (provisional, = THM-7) | V1 §7 |
| SYS-10 | **Energy-system principle:** NOMAD's solar system is a field energy replenishment system, not its primary power source. B1 deploys a larger panel when stationary while keeping NOMAD compact when stowed. No energy independence and no runtime extension is claimed until a power budget and a solar-yield model exist | LOCKED (principle) | Owner, 2026-10-01 (E-POWER-001); `docs/power.md` |

## 3. Compute

| ID | Requirement | Status | Source / notes |
|---|---|---|---|
| CMP-1 | Raspberry Pi 5, 8 GB | LOCKED (current selection) | `docs/hardware.md` "selected" |
| CMP-2 | **Storage:** 500–512 GB NVMe, 2230 preferred, through the Raspberry Pi M.2 HAT+ (Standard: 2230/2242, ≤ 3 A to the device, 16 mm stacking header so it fits over the Active Cooler) | DEFINED (target) / CANDIDATE (HAT+, Raspberry Pi SSD 512 GB) | MFR briefs (E-POWER-001 §2.3). 2230 + HAT+ + Active Cooler compatible on paper. SSD power not published; reference SN740 512 GB: 50 mW avg active, ≤ 4.7 W max |
| CMP-3 | **Active cooling** is required for the Pi 5. The Active Cooler is temperature-controlled by firmware (0 % below 50 °C, 100 % at 75 °C); passive cooling is not assumed sufficient | DEFINED / CANDIDATE (Active Cooler) | MFR (E-POWER-001 §2.2). The Active Cooler current is not published; the fan draws from the Pi's USB budget |
| CMP-4 | Pi stack height (Pi + Active Cooler + 16 mm header + HAT+ + NVMe) | DEFINED (EST 25.9 vs envelope 30); VALIDATION REQUIRED (measure at gate 3) | `v1_integration.py` |
| CMP-5 | Compute placement in the base: right palm bay, ports internal (USB toward the trackpad bay, HDMI / power rearward) | DEFINED (provisional); owner acceptance (D-011) | V1 §8 |
| CMP-6 | Remaining compute hardware (cooler model, HAT+, SSD, RTC battery, any expansion) | TBD | |

## 4. Display

| ID | Requirement | Status | Source / notes |
|---|---|---|---|
| DSP-1 | **Target class:** about 10.1" IPS, 1920 × 1200 (16:10), ≥ 400 nit (500+ preferred), matte, non-touch, HDMI, ≤ 6 W. **The ≤ 6 W target needs a brightness condition:** the best-documented panel draws 6.8 W typ / 7.8 W max at full backlight before the controller (E-POWER-001 C1) | DEFINED | `docs/architecture.md`, `docs/hardware.md`; MFR Winstar data |
| DSP-2 | **Display panel and controller (V1 candidate, 2026-10-06):** AUO **G101UAN01.0** (industrial 10.1", 1920 × 1200, eDP 2-lane, 380–410 nit, 50 000 h LED; 3P data) + **Beck BTC-mini-eDP** (HDMI → eDP 1–2 lane, 12 V, 1.10–1.29 W, 80 × 70 × 9.8, MFR). B101UAN01.7 rejected for V1: eDP 4-lane (outside the Beck range), 12 000 h LED. Winstar (D-W) kept as the documented alternative | CANDIDATE; gate 0 data required (AUO datasheet, Beck support + price) | `docs/V1-VIRTUAL-INTEGRATION.md` §2; `prototypes/V1/v1_hardware.py` |
| DSP-3 | **Physical envelope:** panel 229.9 × 150.5 × 5.35 (max of two 3P listings); controller in the **base** under the keyboard; a 30-pin eDP micro-coax through the display-hinge knuckle | DEFINED (provisional) | `nomad.yaml` DISPLAY_*; V1 §2, §9 |
| DSP-4 | Display temperature rating vs closed-in-sun heating (display about 50–57 °C at 35 °C ambient with gap + foil, EST) | VALIDATION REQUIRED | G101UAN01.0 limits are 3P and conflicting (60 / 70 °C): 3–13 K margin. Thermal mock-up (V1 §20 test 12) |

## 5. Keyboard

| ID | Requirement | Status | Source / notes |
|---|---|---|---|
| KBD-1 | **Envelope:** 285 × 117 × 16 mm, derived from the V1 keyboard (replaces the 280 × 105 × ≤ 8 target, which no wired candidate meets) | DEFINED (provisional); owner confirmation | `nomad.yaml` KEYBOARD_*; V1 §2, §19 |
| KBD-2 | Wired USB HID, ultra-low-profile, no battery, no wireless | DEFINED | `docs/hardware.md` |
| KBD-3 | **Keyboard model:** Perixx **PERIBOARD-416** (wired mini scissor, 78 / 79 keys, 285 × 117 × 16, 332 g, detachable USB-C cable, 0–40 °C; MFR manual) | CANDIDATE | `prototypes/V1/v1_hardware.py` |
| KBD-4 | Centred on the chassis centreline, above the trackpad | LOCKED | D-003 |

## 6. Trackpad

| ID | Requirement | Status | Source / notes |
|---|---|---|---|
| TPD-1 | Perixx PERIPAD-501 II: 86 × 75 × 13 per the official manual (published, not measured); USB-A fixed lead; **availability unknown** (not on the Perixx stores). Fallback PERIPAD-506 (135 × 116 × 14) would add ≈ 41 mm of base depth | CANDIDATE | E-POWER research campaign [K1]; V1 §2 |
| TPD-2 | Centred below the keyboard; the position is parameterized | LOCKED | D-003 |
| TPD-3 | Envelope, mounting (clamped in the trackpad tray) and interface (USB to the Pi USB2 port under the trackpad) | DEFINED (provisional) | V1 §8 |

## 7. Lid

| ID | Requirement | Status | Source / notes |
|---|---|---|---|
| LID-1 | **B1 lid architecture:** a thin core (display, controller zone, back shell), a vented air gap with low-e foil, and the solar leaf on top | LOCKED (architecture) | D-010 |
| LID-2 | B1 lid stack: core 19 + gap 6 + leaf 6 = **31** (`LID_THICKNESS` formula). Core kept at the SB-261 baseline; the controller moved to the base | DEFINED (provisional) | V1 §9 |
| LID-3 | **Display-hinge subsystem:** 2 × **Southco E6-10-216-50** (1.8 N·m symmetric; M4); gravity torque ≤ 1.84 N·m over 60–135° (CALC) → 1.38 N·m per hinge needed at the −20 % bound; opening force 22 N; φ-max hard stop 135° in the corner blocks | CANDIDATE; VALIDATION REQUIRED | `v1_integration.py`; V1 §9. Axis position still D-006 provisional |
| LID-4 | **Rear-port / lid-sweep interaction:** RESOLVED in V1 by having **no rear plugs** (lid corner reaches z 16.7 at 135°; ports moved to the left / front-right walls) | DEFINED (virtual); owner confirmation of the I/O policy | V1 §9, §19 |
| LID-5 | **Shared display-hinge cable pass:** eDP micro-coax + solar lead through a 20 mm centre knuckle; 60 mm twist zone, 2.25 °/mm | DEFINED; VALIDATION REQUIRED (twist cycling) | V1 §9, §11 |
| LID-6 | **Final lid geometry** | DEFINED (envelope model); persistent CAD not written | `v1_integration.py`; Onshape work after D-011 |

## 8. Solar

| ID | Requirement | Status | Source / notes |
|---|---|---|---|
| SOL-1 | **B1 solar leaf:** one leaf behind the display lid, hinged at the lid top edge | LOCKED | D-010 |
| SOL-2 | **Usable leaf motion** about 0–190° (`SOLAR_LEAF_ANGLE_MAX` 190) | DEFINED; VALIDATION REQUIRED | Owner target. KERNEL: ≥ 2.03 mm at 190°, first contact 201° (`prototypes/B1_SB261/`) |
| SOL-3 | **Leaf hinges:** two structural friction hinges. Current selected candidate: TorqMaster SB-188-SB-261-6 | CANDIDATE; VALIDATION REQUIRED | V1 leaf (413 g, 290 × 239): 0.78 N·m per hinge needed vs 0.96–1.13 published (SF ≈ 1.23, CALC). Load, material, temperature unpublished. Coupon designed, not printed |
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
| PWR-1 | **Power budget** (V1, 2026-10-06): at the battery LOW 7.1 / NORMAL 9.0 / HIGH 19.1 / WORST 24.4 W; off 0.07 W; representative day 74 Wh | DEFINED (CALC); VALIDATION REQUIRED (measurement) | `prototypes/V1/v1_power.py`; V1 §3. Display power is a proxy (ASSUMED) |
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
| PWR-13 | **Power switch:** one sealed momentary button → Pi 5 J2 (on / soft-off) + charger QON (ship-mode exit); pack connector = service disconnect; no series switch in the 10 A path | DEFINED (provisional) | V1 §6 |
| PWR-14 | **Charging / input behaviour:** charge while running (NVDC); USB-C and solar are not summed (one input at a time; USB-C priority enforced by the host); charging limited to 0–45 °C (BMS + charger JEITA), including charging while closed in the sun | DEFINED (baseline); **VALIDATION REQUIRED** | E-POWER-002 (`docs/E-POWER-002-POWER-ARCHITECTURE.md`) §6–§9 |
| PWR-15 | **Off-state drain:** the Pi 5 draws about 1–1.4 W when "off" by default, about 0.01 W with `POWER_OFF_ON_HALT=1`. NOMAD must set the EEPROM option or cut power | DEFINED | MFR (E-POWER-001 C10) |
| PWR-16 | **The 5 V rail feeding the Pi must be 5 A-capable** for the Pi to allow 1.6 A of downstream USB, which the fan and USB HID devices share. Otherwise the limit is 600 mA, or peripherals are powered separately | DEFINED (requirement on the rail; no converter chosen) | MFR (E-POWER-001 C9) |
| PWR-17 | **Battery pack fit:** holder-type 4S1P pack 91.6 × 80 × 28.9 in a **93.6 × 82 × 31 bay**, fits the left palm bay (100 × 94.5 × 35) with 2 mm per axis | DEFINED (provisional; owner confirmation with D-011) | `nomad.yaml` BATTERY_BAY_*; V1 §4, §8 |

## 10. Thermal — UNRESOLVED

**Fixed so far:**
- The Pi 5 needs active cooling.
- Cooling airflow must never be blocked, including by service panels (`CLAUDE.md`).
- Round C reserves front intake → duct → Pi → side exhaust (proposed D-007, reserved volumes only).
- The sun-exposed B1 parts and the gap and foil are covered in SOL-7.

| ID | Required future work | Status | Notes |
|---|---|---|---|
| THM-1 | Pi 5 thermal load: compute bay 3.3 / 4.3 / 11.9 / 15.6 W (LOW / NORMAL / HIGH / WORST, CALC) | DEFINED (CALC) | V1 §7 |
| THM-2 | Display and controller heat | TBD | Needs DSP-2 |
| THM-3 | Battery thermal constraints (charge and discharge limits) | TBD | Needs PWR-3 |
| THM-4 | Airflow: rear-wall + underside intake → under-keyboard → Pi bay → 30 mm exhaust fan, right wall front corner | DEFINED (provisional); VALIDATION REQUIRED | V1 §7 |
| THM-5 | Fan: Sunon MF30100V1-1000U-A99 (30 × 30 × 10, 5.5 CFM, 0.6 W), controlled on internal-air temperature | CANDIDATE; VALIDATION REQUIRED | V1 §7 |
| THM-6 | Solar and closed-lid heat: display +15–22 K with gap and foil; panel 66–91 °C at 35 °C ambient (EST) | TBD; VALIDATION REQUIRED | D-010 Phase 2 §13 |
| THM-7 | Ambient operating temperature target: 0–35 °C full function (HIGH throttles gracefully above ≈ 31 °C); storage −20…+50 °C | DEFINED (provisional); owner confirmation | V1 §7, §19 |
| THM-8 | **Component temperature limits** found so far: M.2 HAT+ 0–50 °C ambient; Pi 5 0–70 °C; Raspberry Pi SSD 0–70 °C; Winstar panel −20…+70 °C; AUO panel 0–50 °C; DAN-F10N −40…+85 °C. The **internal air temperature must stay ≤ 50 °C** while the HAT+ is used | DEFINED (from MFR data) | E-POWER-001 C7 |

## 11. GNSS

| ID | Requirement | Status | Source / notes |
|---|---|---|---|
| GNS-1 | SparkFun GNSS Flex pHAT – DAN-F10N (GPS-29491). The u-blox DAN-F10N is an **antenna module** (internal L1/L5 patch, 20.0 × 20.0 × 11.6). GPS / Galileo / BeiDou / QZSS / NavIC; **no GLONASS**. 2.7–3.6 V, 21 mA tracking / 26 mA acquisition. UART + PPS; U.FL / SMA for an external antenna. Linux support required (unchanged requirement) | CANDIDATE | MFR (u-blox, SparkFun); E-POWER-001 §2.6. Corrects the earlier "GLONASS" listing |
| GNS-2 | Separate cabled module (6-wire UART / PPS harness from the Pi GPIO pass-through), in the rear strip behind the keyboard | DEFINED (provisional) | V1 §8 |
| GNS-3 | **Antenna:** integrated patch under a non-metallic rear-deck window (sky keep-out 40 × 29.5, no metal or cable above); external antenna via U.FL is the fallback | DEFINED; VALIDATION REQUIRED (sky-window test) | V1 §8, §20 test 8 |

## 12. Ports / Controls — final list NOT defined

The P0.1 reserved-volume list (`docs/mechanical-spec.md`) keeps room for: USB-C, 2–3 × USB-A, HDMI, audio, Ethernet, GPIO, microSD, power and expansion. **That is a space reservation, not a port list.**

| ID | Open item | Status |
|---|---|---|
| PRT-1 | I/O placement policy: **no rear plugs** (V1); left wall: USB-C PD input + power button; front-right wall: 2 × USB-A 3.0; right wall: fan exhaust | DEFINED (provisional); owner confirmation | V1 §9 |
| PRT-2 | External USB: 2 × USB-A 3.0 (Pi USB3 via 0.3 m panel-mount extensions). Internal: keyboard and trackpad on the Pi USB2 ports | DEFINED (provisional) | V1 §8, §11 |
| PRT-3 | HDMI: no external video out in V1; internal Pi micro-HDMI → Beck controller in the base | DEFINED (provisional); owner confirmation | V1 §6 |
| PRT-4 | Charging input: USB-C PD only (left wall), no DC barrel | DEFINED (provisional); owner confirmation | E-POWER-002 §7.4; V1 §19 |
| PRT-5 | External power output, if any | TBD |
| PRT-6 | GNSS external antenna connector | TBD (GNS-3) |
| PRT-7 | Service ports: microSD on the Pi and the GNSS pHAT (internal); Ethernet not brought out in V1 | DEFINED (provisional) | V1 §19 |
| PRT-8 | Power button and its behaviour | DEFINED (PWR-13) | V1 §6 |
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
| MEC-3 | **Base layout (V1):** D-007 placement + V1 amendments (side / front I/O, controller in the base, GNSS rear strip, holder battery bay, sled as a panel insert); 0 envelope violations; every module removable downward | DEFINED (virtual); owner acceptance (D-011) | `v1_integration.py`; V1 §8 |
| MEC-4 | **Serviceability:** battery through its own door; electronics through the service panel; no glue; every screw reachable; B1 leaf hinges serviceable with the leaf open (KERNEL: 1.7–4.1 mm driver clearance) | DEFINED | `CLAUDE.md`, D-007 (proposed), `prototypes/B1_SB261/` |
| MEC-5 | **Fastener philosophy:** a small family (M2.5, M3); screws for structure, clips for frequent access, captive or quarter-turn fasteners for service panels, magnets and pins for covers | DEFINED | `CLAUDE.md`; `FASTENER_SIZE` provisional |
| MEC-6 | **Insert strategy:** heat-set inserts for serviced joints. B1 hinge rail: Ruthex RX-M3x5.7 (lid) and M2.5 × 4 OD 3.55 (leaf). Standard 4.6-OD M2.5 inserts are excluded. Insert walls 1.20–1.47 must be proven | CANDIDATE; VALIDATION REQUIRED | `prototypes/B1_SB261/`; `INSERT_SIZE` TBD |
| MEC-7 | **Print-bed constraint:** base shell, panels, keyboard tray and lid core (306 × 253) and the leaf frame (290 × 239) need a ≥ 310 mm bed, or a split on X = 0 with a lap joint | TBD (owner: print access) | V1 §13 |
| MEC-8 | **Split-print possibility:** base split options screened (C.2); leaf split in two halves with a spliced bar (Phase 2) | DEFINED (options); TBD (choice) | `prototypes/P0.1/c2_architectural_screening.md` |
| MEC-9 | Metal for structural shafts and pins; no structural printed gears | LOCKED (principle) | `CLAUDE.md` |
| MEC-10 | **Structural validation status:** nothing is physically tested. B1 results are KERNEL/CALC. The P0.1/P0.2 coupons (Architecture A rail and lid plates) are not printed and are deferred with A. The SB-261 coupon is designed, not printed | VALIDATION REQUIRED | |

## 15. Mass / CG

| ID | Requirement | Status | Notes |
|---|---|---|---|
| MAS-1 | **Total mass estimate 3.03 kg (2.52–3.54)**: base 1.86, lid 0.65, leaf 0.41, stay 0.11 kg; 33 % manufacturer-published | DEFINED (CALC / EST) | `v1_integration.py`; V1 §12 |
| MAS-2 | **CG and stability:** worst rearward CG is behind the rear feet at φ 135 / ψ 135 without the stay; the stay is required | DEFINED (finding); VALIDATION REQUIRED | D-010 Phase 2 §8–§9 |
| MAS-3 | Mass, CG and stability values (V1): with the stay every deployed state tips only above 12.7 m/s; closed 37.7 m/s | DEFINED (CALC); VALIDATION REQUIRED | V1 §12 |

## 16. Manufacturing

| ID | Requirement | Status | Notes |
|---|---|---|---|
| MFG-1 | **FDM PETG** is the current development assumption. Sun-exposed B1 parts are ASA or light-coloured (HDT) | DEFINED | `CLAUDE.md`; D-010 Phase 2 §13 |
| MFG-2 | **Physical coupons are required before production parts** (inserts, walls, gaps, hinge torque) | LOCKED (gate) | `prototypes/B1_SB261/COUPON_SPEC.md` |
| MFG-3 | **Real hardware measurements are required** before final interfaces (display, keyboard, trackpad, Pi stack, panel, hinges) | LOCKED (gate) | CLAUDE.md: physical testing is authoritative for fit and motion |
| MFG-4 | **Final print strategy** (orientation, splits, material per part, in-house vs service) | TBD | Not frozen |

## 17. Open owner decisions (not made here)

Collected in `docs/V1-VIRTUAL-INTEGRATION.md` §19 (2026-10-06):

| Decision | Needed for |
|---|---|
| **D-011 / D-007:** accept the V1 base placement (battery left bay, compute right bay, power / controller / GNSS under the keyboard and in the rear strip), **side / front I/O with no rear plugs**, controller in the base | Persistent V1 CAD, gate 1 |
| **Envelope growth** to 306 × 253 × 40 and the PERIBOARD-416 replacing the ≤ 8 mm keyboard target | Persistent V1 CAD |
| **Battery cell basis:** M65A (preliminary; 6 h met) or 50E (4 h minimum only). Holder pack + 93.6 × 82 × 31 bay adopted provisionally | Gate 4 |
| **Display direction:** confirm D-A family (G101UAN01.0 + Beck BTC-mini-eDP) over D-W | Gate 2 |
| **Ambient target:** 0–35 °C operating, storage −20…+50 °C (provisional) | Thermal validation |
| **External I/O list:** USB-C PD charge only (no barrel), 2 × USB-A, no Ethernet, no HDMI out, no audio in V1 | Persistent V1 CAD |
| **Budget vs BOM** (≈ €1 405 vs the €500–650 noted in D-010 §17) and **print access** (≥ 310 mm bed / service, or split parts) | Gate 1 |
| ~~Runtime target (PWR-5)~~ — decided 2026-10-02: 6 h normal target / 4 h minimum | — |

## 18. V1 dependency order (remaining virtual work)

**The rule:** finish the virtual design before spending money wherever reasonably possible. Physical work starts at step 12.

1. **D-010 B1 architecture formalization.** Done 2026-10-01.
2. **V1 requirements.** This sheet, 2026-10-01.
3. **Down-select real hardware envelopes.** First pass done 2026-10-01 (E-POWER-001); V1 candidates selected 2026-10-06 (V1 integration §2). Original scope:
   - display and controller
   - keyboard and trackpad
   - Pi stack, cooler and SSD
   - GNSS and antenna
   - display hinges
   - panel confirmation
   - Use datasheets and published drawings only. €0.
4. **Establish the power budget** from datasheets (PWR-1). Preliminary model done 2026-10-01 (E-POWER-001); it gets refined as step 3 closes.
5. **Establish the battery / power architecture** (PWR-2 … PWR-14). Baseline done 2026-10-02 (E-POWER-002). Owner decisions on cell basis, bay and display remain (E-POWER-002 §15).
6. **Establish the thermal architecture** (§10). Done 2026-10-06 (virtual; V1 integration §7).
7. **Re-baseline `nomad.yaml`:** Done 2026-10-06 (V1 master; P0.1 set frozen in `CAD/parameters/history/`). Was:
   - B1 lid stack
   - real envelopes
   - retire the A parameters from the active set
   - D-007 decision
8. **Resolve the display-lid hinge and rear-port conflict** (LID-3, LID-4, PRT-1). Done 2026-10-06 (virtual; owner confirmation of the I/O policy).
9. **Integrate the complete Virtual V1 CAD.** Envelope integration done 2026-10-06 (`CAD/tools/v1_integration.py`); persistent Onshape CAD after D-011.
10. **Mass / CG / stability analysis** (§15). Done 2026-10-06 (CALC).
11. **BOM and pricing.** Preliminary BOM done 2026-10-06 (`prototypes/V1/V1_BOM.csv`).
12. **Staged purchasing.** Plan: V1 integration §18 (gates 0–5). The first stage is the validation parts: SB-261 hinges and inserts for the coupon, cable samples.
13. **Physical validation:**
    - SB-261 coupon
    - D-010 Phase 2 §24 mock-ups
    - thermal
    - hardware fit measurements
14. **Physical build.**
