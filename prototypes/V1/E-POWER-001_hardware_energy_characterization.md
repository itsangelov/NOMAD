# E-POWER-001 — V1 Hardware + Energy Characterization

**Date:** 2026-10-01
**V1 dependency steps:**
- Step 3, down-select real hardware envelopes: first pass.
- Step 4, establish the power budget: preliminary, from published data only.

**Cost:** €0. This is a desk study from published sources.

**What this study is not:**
- Nothing was bought, measured or physically tested.
- No production CAD changed.
- No battery, pack voltage, chemistry, BMS, charger, MPPT, DC/DC or protection device is selected. That is intentional.

**Principle:** characterize the energy-consuming hardware first, then reverse-engineer the power architecture and the battery around the real loads.

## 0. Evidence labels

| Label | Meaning |
|---|---|
| **MFR** | Manufacturer datasheet, product brief, official documentation or official product page |
| **MFR-DWG** | Manufacturer mechanical drawing. Raspberry Pi drawings state "approximate, for reference purposes only" |
| **3P** | Third-party source: an independent measurement or a reseller/panel database. Used only where the manufacturer publishes nothing |
| **REPO** | Existing NOMAD record (already sourced there) |
| **CALC** | Arithmetic on the labelled inputs |
| **EST / ASSUMED** | Engineering estimate or assumption. None is used as a load value below |
| **TBD** | Not published or not verifiable. Left open |

**Source references** use [S#] tags; the sources list is in §10. All sources were retrieved 2026-10-01.

## 1. Candidates investigated and their status

| Subsystem | Candidate | Status after E-POWER-001 |
|---|---|---|
| Compute | Raspberry Pi 5, 8 GB | **SELECTED** (unchanged) |
| Cooling | Raspberry Pi Active Cooler (Pi 5) | CANDIDATE |
| Cooling | Noctua NF-A4x10 5V PWM (40 mm enclosure fan, reference) | CANDIDATE (reference for an enclosure fan; not chosen) |
| Storage adapter | Raspberry Pi M.2 HAT+ (Standard) | CANDIDATE |
| Storage | Raspberry Pi SSD 512 GB (M.2 2230) | CANDIDATE |
| Storage (power reference) | WD PC SN740 512 GB 2230 | Reference for NVMe power only |
| Display | Winstar WF101NTYA4LNN0 (10.1", 1920×1200, 500 nit, LVDS, no controller) | CANDIDATE (best documented) |
| Display | AUO B101UAN01.C (10.1", 1920×1200, 400 nit, eDP) + an HDMI→eDP controller | CANDIDATE (data third-party; power TBD) |
| Display | Waveshare 10.1inch HDMI LCD (G) (1920×1200, HDMI, integrated controller, touch, optical bonding) | CANDIDATE (weak data: brightness and power not published) |
| Display (rejected) | Waveshare 10.1inch HDMI LCD (H): 1024×600. Waveshare 10.1EP-CAPLCD: 300 nit | Below the resolution or brightness target |
| Keyboard | Perixx PERIBOARD-426 / -416 / -422 / -332 / -409H | CANDIDATE (**none meets ≤ 8 mm**, see §8) |
| Trackpad | Perixx PERIPAD-501 II (current candidate) | **UNVERIFIED** (not listed on the Perixx stores; no official dimensions) |
| Trackpad | Perixx PERIPAD-501 | CANDIDATE (official page gives no dimensions) |
| Trackpad | Perixx PERIPAD-506 | CANDIDATE (official dimensions) |
| GNSS | SparkFun GNSS Flex pHAT – DAN-F10N (GPS-29491) | CANDIDATE (unchanged) |
| GNSS antenna | DAN-F10N integrated patch (default) | CANDIDATE |
| GNSS antenna | u-blox ANN-MB5 L1/L5 active antenna (external option) | CANDIDATE |
| Display hinge | Southco E6-10-216-50 (Medium, 1.8 N·m symmetric) | CANDIDATE |
| Display hinge | Southco E6-10-416-50 (Large, 1.8 N·m symmetric) | CANDIDATE |
| Display hinge | Southco E6-10-216F-50 (Medium, asymmetric 1.8 / 1.1 N·m) | CANDIDATE |
| Display hinge | TorqMaster SB-188-SB-254-H (1.36–1.69 N·m, balanced) | CANDIDATE (REPO data) |
| Display hinge | Reell RT series | Family only (model data not obtained) |
| Solar panel | Voltaic P108 | CANDIDATE (unchanged; official data refreshed) |
| Solar-leaf hinge | TorqMaster SB-188-SB-261-6 | CANDIDATE (unchanged; record consistent, §9) |

**Nothing new is selected.** The only selected item remains the Pi 5 8 GB.

## 2. Verified electrical data

### 2.1 Raspberry Pi 5, 8 GB

| Item | Value | Label / source |
|---|---|---|
| Power input | 5 V / 5 A DC via USB-C, with USB Power Delivery support | MFR [S1] |
| Supply requirement | "5.1V supply" (all models); recommended PSU current 5.0 A; recommended supply: the official 27 W USB-C PSU | MFR [S2] |
| Typical bare-board active current | **800 mA** (≈ 4.0 W at 5.0 V, CALC) | MFR [S2] |
| Downstream USB current | **1.6 A** with a 5 A-capable supply; **600 mA** with any other supply | MFR [S2] |
| Fan connector | 4-pin JST-SH PWM; **draws from the same current limit as the USB peripherals** | MFR [S3] |
| Power when "off" (default) | **≈ 1 W to 1.4 W** | MFR [S2] |
| Power when off, with `POWER_OFF_ON_HALT=1` | **≈ 0.01 W** | MFR [S2] |
| RTC wake-alarm low-power state | ≈ 3 mA | MFR [S4] |
| Idle / stress-ng (8 GB C1) | **3.2 W / 9.8 W** | 3P [S5] (conditions only partly stated) |
| Idle at the wall (ondemand / performance governor) | 3.5 W / 5.5 W, including NVMe, Active Cooler, HDMI, 2 RF dongles and adapter losses | 3P [S6] |
| Thermal management | Arm cores throttle progressively from 80 °C; at 85 °C the Arm cores and GPU throttle | MFR [S3] |
| Operating temperature | 0 °C to 70 °C | MFR [S1] |

**Interpretation:**
- No single "Pi 5 power" number exists.
- Manufacturer-documented: typical active about 4.0 W and a 25 W input ceiling.
- Independent measurement: idle about 3.2 W, sustained CPU stress about 9.8 W. That is 3P, not NOMAD-measured.

### 2.2 Cooling

| Item | Value | Label / source |
|---|---|---|
| Active Cooler supply | 5 V DC from the Pi 5 fan header; PWM speed control with tachometer | MFR [S7] |
| Active Cooler airflow / speed | max 1.09 CFM; max 8 000 RPM ± 15 %; MTTF 379 000 h at 25 °C | MFR [S7] |
| Active Cooler current / power | **Not published** | TBD |
| Pi 5 firmware fan curve | 0 % below 50 °C; 30 % at 50 °C; 50 % at 60 °C; 70 % at 67.5 °C; 100 % at 75 °C; 5 °C hysteresis | MFR [S3] |
| Noctua NF-A4x10 5V PWM (reference) | 0.3 W typical / 0.35 W max (0.06 / 0.07 A); 5.24 CFM; 1.95 mm H₂O; −10…+70 °C | MFR [S8] |

**How cooling behaves as a load:** temperature-controlled, so it is **workload- and ambient-dependent**. The fan is off below 50 °C SoC temperature and full-speed from 75 °C. Passive cooling is **not** assumed sufficient; the manufacturer recommends active cooling for the Pi 5 [S3].

### 2.3 Storage

| Item | Value | Label / source |
|---|---|---|
| M.2 HAT+ interface | PCIe 2.0 x1, 500 MB/s peak; M key; 2230 / 2242 (Standard), 2230 only (Compact) | MFR [S9] |
| M.2 HAT+ power to the M.2 device | "up to 3A" | MFR [S9] |
| M.2 HAT+ own consumption | Not published (it has power and activity LEDs) | TBD |
| **M.2 HAT+ operating temperature** | **0 °C to 50 °C (ambient)** | MFR [S9] |
| Raspberry Pi SSD | 256 / 512 GB / 1 TB, M.2 2230, PCIe Gen 3, NVMe 1.4; 0–70 °C ambient | MFR [S10] |
| Raspberry Pi SSD power | **Not published** | TBD |
| Reference: WD PC SN740 512 GB (2230) | Average active 50 mW (MobileMark 2018); average maximum 4.7 W; sleep (PS5) 3.3 mW; 3.3 V supply | MFR [S11] |

**Reading the SN740 figures:**
- The 4.7 W "average maximum" was measured on a Gen4 x4 host.
- On the Pi 5's PCIe 2.0 x1 link it is an **upper bound**, not a NOMAD value.
- Whether the Pi enters PS5 in practice is not established.

**Compatibility:** a 2230 drive is supported by both HAT+ variants. The Standard HAT+ is "supplied with a 16 mm stacking header … so it can be fitted … with the Active Cooler in place" [S9]. **Compatible on paper.**

### 2.4 Display

| Item | WF101NTYA4LNN0 (Winstar) | B101UAN01.C (AUO) | 10.1inch HDMI LCD (G) (Waveshare) |
|---|---|---|---|
| Resolution / type | 1920×1200, IPS, normally black, anti-glare | 1920×1200, AHVA (IPS-class), **glossy** | 1920×1200, IPS, toughened glass, optical bonding, capacitive touch |
| Brightness | **500 cd/m²** | **400 cd/m²** typ. | **Not published** |
| Interface | 2-ch LVDS, **no controller board** | eDP, 30-pin, 2 lanes | HDMI (controller integrated); USB touch |
| Logic supply | 3.0 / 3.3 / 3.6 V; 300 mA typ / 360 mA max; **1.0 W typ / 1.2 W max** | 3.3 V typ | 12 V input (12 V / 2 A adapter) |
| Backlight | LED string, 26.0 / 29.0 / 33.0 V × 200 mA → **5.8 W typ (5.2–6.6 W)** (CALC) | WLED with integrated LED driver; power not published | Not published |
| Panel total at full backlight | **6.8 W typ / 7.8 W max** (CALC from MFR), excluding the controller | TBD | TBD |
| Operating temperature | **−20 °C to +70 °C** | 0 °C to 50 °C | Not published |
| Sources | MFR [S12] | 3P [S13] | MFR [S14] |

**Display controller board** (required for all three; HDMI → LVDS or eDP):
- No candidate board is characterized from a manufacturer datasheet.
- Boards sold with such panels (e.g. RTD2556-based HDMI→eDP boards) are reseller-documented only.
- Controller dimensions, power, connectors and mounting are **TBD**.

### 2.5 Keyboard and trackpad

- **Interface:** both are USB HID, USB bus-powered.
- **Power:** none of the Perixx pages publishes current or power (**TBD**).
- **Upper bound, not an estimate:** a USB 2.0 device may draw up to 500 mA (2.5 W) after enumeration. In NOMAD that comes out of the Pi 5's 1.6 A downstream budget [S2] unless powered separately.

### 2.6 GNSS

| Item | Value | Label / source |
|---|---|---|
| u-blox DAN-F10N module | GNSS **antenna module** with an internal L1/L5 antenna, 20.0 × 20.0 × 11.6 mm; GPS / Galileo / BeiDou / QZSS / NavIC (**no GLONASS**); supply 2.7–3.6 V; −40…+85 °C | MFR [S15] |
| SparkFun DAN-F10N Flex module | 2.7–3.6 V; tracking **21 mA** (GPS+GAL+BDS); acquisition **26 mA**; inrush up to 100 mA; hardware backup 31 µA; software standby 49 µA; 63 mW continuous tracking at 3 V | MFR (board vendor) [S16][S17] |
| SparkFun GNSS Flex pHAT | 3.3 V from the 40-pin header; UART (default GPIO14/15), I²C, PPS; U.FL and SMA; USB-C to the module; Qwiic | MFR (board vendor) [S18] |
| Antenna selection | Integrated patch by default; external antenna via U.FL with the `EXT_ANT` jumper | MFR (board vendor) [S16] |
| u-blox ANN-MB5 (external option) | L1/L5 active; 3.0–5.0 V; **17 mA typ** (at 5 V, ≈ 85 mW CALC); SMA plug, RG174 3.0 m cable; IPX7; −40…+85 °C | MFR [S19] |

**How GNSS behaves as a load:** treated as **always-on while navigating**. The backup and standby modes (31–49 µA) allow duty-cycling (TBD by software requirements). Either way, its power is negligible next to the display and Pi (≤ 0.09 W tracking).

### 2.7 Solar panel: Voltaic P108 (official page refreshed)

| Item | Value | Label / source |
|---|---|---|
| Peak power | **9.92 W** | MFR [S20] |
| Open-circuit voltage | 20.45 V | MFR [S20] |
| Peak voltage / peak current | 17.34 V / 570 mA | MFR [S20] |
| Short-circuit current | **Not published** | TBD |
| Size | 22.3 × 27.4 × 0.4 cm on the product page | MFR [S20] |
| Mass | 328 g | MFR [S20] |
| Build | Matte ETFE on 2.0 mm FR4, monocrystalline cells 20 % | MFR [S20] |
| Connector / cable | Waterproof 3.5 × 1.1 mm male plug, 50 cm cable | MFR [S20] |
| Operating / storage temperature | **Not published** | TBD |
| Drawing / model | `P108_dwg.pdf`, `P108_3D.stp` | MFR [S21] |

**Corrections to existing records:**
- The earlier "9.5–10.9 W" range (REPO, D-010 Phase 2) is replaced by the official **9.92 W** peak rating on the current product page.
- Earlier Voltaic material gave 273.5 mm for the long side. The current page gives 27.4 cm. The working YAML value is 273. Confirm from the drawing in step 7.

## 3. Verified physical data (best available envelope)

| Component | W | D | H / T | Weight | Interface | Status | Source |
|---|---:|---:|---:|---:|---|---|---|
| Raspberry Pi 5 | 85 | 56 | TBD (not on the drawing) | TBD | — | Selected | MFR-DWG [S22]: holes 58 × 49, Ø2.7, 3.5 from the edges |
| Active Cooler | 63.5 ‡ | 42.5 ‡ | 13.7 ‡ | TBD | 4-pin JST-SH PWM | Candidate | MFR-DWG [S7] |
| M.2 HAT+ (Standard) | 65 ‡ | 56.5 ‡ | 16 mm stacking header supplied; full stack TBD | TBD | 16-pin 0.5 mm FPC (PCIe) | Candidate | MFR / MFR-DWG [S9] |
| NVMe: Raspberry Pi SSD | 22 | 30 | 0.8 PCB + max 1.35 components | TBD | M.2 M key | Candidate | MFR-DWG [S10] |
| Display: Winstar WF101NTYA4LNN0 | 231.40 | 152.3 | **9.1 max** | TBD | 2-ch LVDS (45-pin) + 2-pin backlight | Candidate | MFR [S12]: active area 216.81 × 135.50 |
| Display: AUO B101UAN01.C | 229.71 | 150.3 | 4.6 | 115 g max | eDP 30-pin | Candidate | 3P [S13]: active area 216.81 × 135.5 |
| Display: Waveshare (G) | TBD | TBD | TBD | TBD | HDMI, USB, 12 V | Candidate | MFR [S14]: no dimensions on the product page |
| Display controller | TBD | TBD | TBD | TBD | HDMI in → LVDS / eDP | — | Not characterized |
| Keyboard: PERIBOARD-426 | 276 | 138 | **14** | "0.38" (unit not stated; kg likely) | USB-A, ~1.5 m cable, membrane | Candidate | MFR [S23] |
| Keyboard: PERIBOARD-416 | 285 | 116 | **21** | 361 g | Detachable USB-C & A cable, scissor, 4 hubs | Candidate | MFR [S23] |
| Keyboard: PERIBOARD-422 | 291 | 138 | **19** | TBD | USB-C | Candidate | MFR [S23] |
| Keyboard: PERIBOARD-332 | 285 | 116 | **21** | 361 g | USB, scissor, backlit | Candidate | MFR [S23] |
| Keyboard: PERIBOARD-409H | 314 | 146 | **20** | TBD | USB, 1.8 m cable, 2 hub ports | Candidate | MFR [S23] |
| Trackpad: PERIPAD-501 / 501 II | TBD (repo's ~86 × 75 is unverified) | TBD | TBD (~13 unverified) | TBD | USB, 5 ft 3 in cable | Unverified | MFR [S24] page lists no dimensions; "501 II" not on the Perixx stores |
| Trackpad: PERIPAD-506 | 135 | 116 | 14 | TBD | Detachable USB-C to USB-A | Candidate | MFR [S24] |
| GNSS: DAN-F10N module (u-blox) | 20.0 | 20.0 | 11.6 | TBD | UART, PPS | Candidate | MFR [S15] |
| GNSS: SparkFun DAN-F10N Flex module | 44.45 | 31.75 | TBD | TBD | Flex connector to the carrier | Candidate | MFR [S16]. **The product page says 34.0 × 44.0, which is inconsistent with this** |
| GNSS: Flex pHAT carrier | TBD (vendor dimension PDF / STEP exists) | TBD | TBD | TBD | 40-pin socket, U.FL, SMA, USB-C | Candidate | MFR [S18] |
| GNSS antenna: ANN-MB5 (optional) | 49.14 | 46.14 | 15.94 | 104 g incl. 3 m cable | SMA plug | Candidate | MFR [S19] |
| Display hinge: Southco E6-10-216-50 / -416-50 | catalogue drawing, not transcribed: TBD | — | — | TBD | Through-hole (or C = countersink) | Candidate | MFR [S25] |
| Display hinge: TorqMaster SB-188-SB-254-H | 52.3 long; Ø7.11 barrel (INF) | — | — | TBD | M4 + M3 holes | Candidate | REPO (`prototypes/B1_SB261/reports/01…`) |
| Solar: Voltaic P108 | 274 (27.4 cm) | 223 | 4 | 328 g | 3.5 × 1.1 mm plug, 50 cm | Candidate | MFR [S20] |

‡ **Interpreted Raspberry Pi drawing values:** the text extracted from the drawing lists these figures, but their dimension lines could not be machine-read. The interpretations are:
- **Active Cooler:** footprint about 63.5 × 42.5, height 13.7 (other labels: 30 / 30).
- **M.2 HAT+:** outline 65 × 56.5.

These are **inferred, to be verified visually against the drawing** before any CAD use.

**Display hinge data:**

| Hinge | Torque (N·m) | Material | Cycle life | Max static load | Operating temperature | CAD |
|---|---|---|---|---|---|---|
| Southco E6-10-216-50 (Medium) | 1.8 symmetric (16 in-lbf) | Aluminium alloy, black paint | 20 000 cycles within ±20 % of static torque | Radial / axial 155 N | Not in the catalogue page: TBD | TBD |
| Southco E6-10-416-50 (Large) | 1.8 symmetric | Zinc alloy, black paint | Same as above | 200 N | TBD | TBD |
| Southco E6-10-216F-50 | 1.8 forward / 1.1 reverse (asymmetric) | — | — | — | — | — |
| TorqMaster SB-188-SB-254-H | 1.36–1.69 balanced (PUB) | Not published | 30 000+ cycles (family, PUB) | Not published | Not published | No IGES listed |
| Reell RT series | Model-level data not obtained (TBD) | — | Reell states up to 50 000 cycles generally [S26] | — | Reell states −40…80 °C generally [S26] | — |

## 4. Power-load model (preliminary, published data only)

All values are watts at the component, **before conversion losses**.

| Component | Idle | Typical | Peak / max | Voltage | Notes | Source |
|---|---:|---:|---:|---|---|---|
| Pi 5 8 GB (board) | 3.2 | 4.0 | 9.8 (stress-ng) | 5 V (5.1 V nominal) | 25 W input ceiling (5 V / 5 A) incl. 8 W USB budget. Off: 1–1.4 W, or 0.01 W with `POWER_OFF_ON_HALT=1` | 3P [S5] / MFR [S2] / 3P [S5] |
| Active Cooler | 0 below 50 °C SoC | TBD | TBD | 5 V (fan header) | Current not published; counts against the 1.6 A USB budget | MFR [S3][S7] |
| Enclosure fan (reference NF-A4x10 5V PWM) | 0 (PWM 0 %) | 0.3 | 0.35 | 5 V | Only if an enclosure fan is added | MFR [S8] |
| NVMe 2230 (reference SN740 512 GB) | 0.0033 (PS5) | 0.05 (avg active) | ≤ 4.7 (upper bound, Gen4 host) | 3.3 V | Raspberry Pi SSD power not published | MFR [S11] |
| M.2 HAT+ | TBD | TBD | TBD | 3.3 V to the device | Adapter + LEDs; supplies ≤ 3 A to the device | MFR [S9] |
| Display panel (Winstar, full backlight) | — | 6.8 | 7.8 | 3.3 V logic; 26–33 V LED string | Dimming lowers the backlight share (not quantified) | MFR [S12], CALC |
| Display panel (AUO / Waveshare) | TBD | TBD | TBD | 3.3 V / 12 V | | — |
| Display controller board | TBD | TBD | TBD | TBD | Includes the LED driver for LVDS panels | — |
| Keyboard | TBD | TBD | ≤ 2.5 (USB 2.0 limit; bound, not an estimate) | 5 V USB | Backlit models (PERIBOARD-332) draw more | — |
| Trackpad | TBD | TBD | ≤ 2.5 (same bound) | 5 V USB | | — |
| GNSS (DAN-F10N) | 0.0001–0.0002 (backup / standby) | 0.063 (tracking, 3 V) | 0.086 (acquisition 26 mA × 3.3 V, CALC); 100 mA inrush | 3.3 V | | MFR [S16] |
| GNSS external antenna (ANN-MB5, optional) | — | 0.085 | — | 3.0–5.0 V | Bias supply path TBD | MFR [S19] |
| Other always-on electronics (BMS, charger, MPPT, DC/DC quiescent, RTC) | TBD | TBD | TBD | — | **Not selected** (step 5) | — |

## 5. Operating states (preliminary envelope)

**Method:**
- Each state sums only the components that have a published value.
- Unknown items are listed, not guessed.
- Totals are **documented subtotals**, and the real total will be **higher**.
- Display: the Winstar panel at **full backlight**, because no brightness/power curve is published. The operating brightness is not yet defined.

| State | Composition (documented values) | Documented subtotal | Excluded (TBD) |
|---|---|---:|---|
| **A — FIELD STANDBY** (display on, Pi mostly idle, GNSS on, keyboard and trackpad connected) | Pi 3.2–4.0; NVMe 0.003–0.05; display panel 6.8; GNSS 0.063–0.086; fan 0 if SoC < 50 °C | **≈ 10.1–10.9 W** | Display controller and LED-driver losses; keyboard; trackpad; HAT+; enclosure-dependent fan; conversion losses |
| **B — NORMAL OPERATION** (maps, offline knowledge, moderate CPU/storage) | Pi 4.0 (manufacturer "typical bare-board active"; no published workload-specific figure); NVMe 0.05; display 6.8; GNSS 0.086; fan 30–50 % (TBD) | **≈ 10.9 W** | Same, plus fan power. A "moderate workload" Pi value needs measurement |
| **C — MAXIMUM SUSTAINED LOAD** (sustained CPU, NVMe activity, display on, cooling active) | Pi 9.8 (stress-ng, 3P); NVMe 0.05 to ≤ 4.7 (upper bound); display 7.8 (max); GNSS 0.086; fan 100 % (TBD) | **≈ 17.7–22.4 W** | Same, plus Active Cooler at full speed and USB peripherals |

**What this establishes (CALC, not a runtime claim):**
- **The display is the largest single load** in states A and B, at about 62–67 % of the documented subtotal (6.8 W of 10.1–10.9 W). The Pi dominates only in C.
- **The P108's peak rating (9.92 W) is below the documented subtotal of every state.** This is before cell temperature, angle and conversion losses. So the solar leaf cannot carry NOMAD's operating load; it can only replenish energy. This is consistent with the energy principle (§6).
- **No runtime figure is derived here.** It needs the runtime target (owner, PWR-5), the battery architecture and a solar-yield model.

## 6. Energy-system principle (recorded)

> **NOMAD's solar system is a field energy replenishment system rather than its primary power source.**

- The purpose of B1 is to deploy a larger panel when stationary while keeping NOMAD compact when stowed.
- B1 does **not** provide energy independence.
- No runtime extension is claimed until the power budget and a solar-yield model exist.
- B1 must eventually justify its mechanical complexity through measurable energy contribution.

## 7. Major uncertainties

1. **Display power at operating brightness**, and the controller board: entirely uncharacterized. This is the largest load.
2. **Pi 5 "normal workload" power:** only manufacturer "typical active" (4.0 W) and third-party idle/stress values exist.
3. **Active Cooler current:** not published.
4. **Raspberry Pi SSD power:** not published. The SN740 reference was measured on a Gen4 x4 host.
5. **Keyboard and trackpad power:** not published.
6. **Trackpad dimensions:** the current candidate (501 II) is unverified, and its availability is unclear.
7. **How the display controller's input (voltage TBD; the Waveshare (G) uses 12 V) and the Pi's 5 V / 5 A input** are fed, from one or several converters, and their losses (step 5).
8. **Raspberry Pi drawing interpretations** (‡) and the SparkFun module size inconsistency.
9. **P108 short-circuit current and temperature ratings:** not published.

## 8. Conflicts and dependencies discovered (documented, not solved)

| # | Finding | Affects | Evidence |
|---|---|---|---|
| C1 | **Display power exceeds the ≤ 6 W target at full brightness.** The Winstar panel alone is 6.8 W typ / 7.8 W max before the controller. The target needs a defined brightness condition, or a dimming policy | DSP-1, PWR-1, thermal | MFR [S12] |
| C2 | **Display thickness and outline.** Winstar is 9.1 max × 231.4 × 152.3 vs working `DISPLAY_THICKNESS` 5 / `DISPLAY_HEIGHT` 150 / `DISPLAY_WIDTH` 235. AUO (4.6 thick) fits better but is glossy (target: matte) and rated 0–50 °C | LID-2 (B1 core ~19), DSP-3 | MFR [S12], 3P [S13] |
| C3 | **The display controller board is uncharacterized**, so its size, placement (lid vs base), LVDS/eDP cable and power are open. A base-side controller would put a wide high-speed cable through the display-hinge pass that is already shared with the solar cable | LID-5, DSP-3 | — |
| C4 | **No candidate keyboard meets ≤ 8 mm.** The candidates are 14–21 mm thick as sold, and 116–146 mm deep vs the 105 target. Meeting ≤ 8 mm likely needs an uncased or OEM keyboard module (not yet searched) | KBD-1, BODY_DEPTH, the under-keyboard height budget (Round C: 26.5) | MFR [S23] |
| C5 | **Trackpad:** PERIPAD-501 II is not listed on the Perixx stores and its dimensions are unverified. The verified alternative PERIPAD-506 is 135 × 116 × 14 (vs working 86 × 75 × 13), a large base-depth impact | TPD-1, D-003, BODY_DEPTH | MFR [S24] |
| C6 | **The GNSS module is an antenna module.** The DAN-F10N's internal patch needs sky view. The D-007 proposal places GNSS "under the keyboard", which then requires an external antenna (ANN-MB5: 49 × 46 × 16 mm, 3 m cable, SMA) and a mounting and cable route. Also, **GLONASS is not supported**, contrary to `docs/architecture.md` (now corrected) | GNS-2, GNS-3, D-007 | MFR [S15][S16][S19] |
| C7 | **M.2 HAT+ is rated 0–50 °C ambient**, narrower than the Pi (0–70) and SSD (0–70). The internal enclosure air temperature must stay ≤ 50 °C, or the adapter choice must change | THM-*, SYS-9 | MFR [S9] |
| C8 | **The Pi stack height is not yet verified.** Pi + Active Cooler (13.7‡) + 16 mm stacking header + HAT+ + SSD vs working `PI_STACK_HEIGHT` 30 (compute bay) | CMP-4, D-007 | MFR [S7][S9] |
| C9 | **The fan and USB HID devices share the Pi's 1.6 A downstream budget** (600 mA if the Pi's supply is not 5 A-capable). The internal power design must provide a 5 A-capable 5 V rail, or power peripherals separately | PWR-9, PWR-11 | MFR [S2][S3] |
| C10 | **The Pi draws about 1–1.4 W when "off"** by default. NOMAD must set `POWER_OFF_ON_HALT=1` (≈ 0.01 W) or cut power, or the battery drains in storage | PWR-13, PWR-14 | MFR [S2] |
| C11 | **Display-hinge candidates:** Southco E6 hinges (1.8 N·m) are external leaf hinges whose size is not yet transcribed. TorqMaster SB-254-H (1.36–1.69 N·m) sits at or below the 1.5–1.8 band. Fit against the D-006 hinge-mount reserve (working 28 × 21) is unverified | LID-3, D-006 | MFR [S25], REPO |
| C12 | **Battery volume** cannot be sized until a runtime target exists. The documented load envelope (≈ 10–22 W + TBD) fixes the order of magnitude only | PWR-2…5, D-007 battery bay (working 90 × 82 × 30) | CALC |
| C13 | **P108 mass and CG:** 328 g at the lid top (unchanged from D-010). The official rating is 9.92 W, not 9.5–10.9 W | SOL-4, MAS-* | MFR [S20] |
| C14 | **Pi 5 port edges vs rear I/O:** ports sit on two board edges, which interacts with the open rear vs side I/O decision | PRT-1, D-007 | MFR-DWG [S22] |

## 9. Solar-leaf hinge record: consistency check only

The established SB-188-SB-261-6 facts were checked against `prototypes/B1_SB261/` (README, VALIDATION_STATUS, reports 01–04). Every value listed for this task is present and consistent:
- **IGES geometry:** shaft Ø4.762, protrusion 1.404, flag width 7.140, hole Ø3.506 at 7.950, reach 12.700, thickness 1.143, band gap 0.127, centre gap 2.16, barrel Ø7.048.
- **Published data:** barrel Ø7.11, length 33.8, 4 flags / 4 holes Ø3.51, band -6 0.96–1.13 N·m, 360° without stops, 30 000+ cycles, black oxide.
- **B1 geometry:** hinge centres ±115, axis y 4.0 / z 63.5, leaf 0–190°, sleeve 7.5 / 5.5, R12 bends (5), sleeve x 12–76, separation ≥ 9.8, 64 mm twist zone at 2.97°/mm (limit 3.5), 190° clearance 2.03, first contact 201°.

**No change was made.**

## 10. Sources (retrieved 2026-10-01)

| Tag | Source |
|---|---|
| S1 | Raspberry Pi 5 Product Brief (RP-008348-DS): https://datasheets.raspberrypi.com/rpi5/raspberry-pi-5-product-brief.pdf |
| S2 | Raspberry Pi documentation, "Power supply" (source `power-supplies.adoc`, raspberrypi/documentation master @ e47af6c): https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#power-supply |
| S3 | Raspberry Pi documentation, "Frequency management and thermal control" / Raspberry Pi 5 fans (`frequency-management.adoc`, same commit): https://www.raspberrypi.com/documentation/computers/raspberry-pi.html |
| S4 | Raspberry Pi documentation, "Real Time Clock" (`rtc.adoc`, same commit) |
| S2–S4 source | https://github.com/raspberrypi/documentation/tree/master/documentation/asciidoc/computers/raspberry-pi (`power-supplies.adoc`, `frequency-management.adoc`, `rtc.adoc`) |
| S5 | J. Geerling, "New 2GB Pi 5 has 33% smaller die, 30% idle power savings", 2024-08-29: https://www.jeffgeerling.com/blog/2024/new-2gb-pi-5-has-33-smaller-die-30-idle-power-savings/ |
| S6 | CNX Software, "Comparison of Raspberry Pi 5 with 2GB and 8GB RAM", 2024-08-27: https://www.cnx-software.com/2024/08/27/comparison-of-raspberry-pi-5-with-2gb-and-8gb-ram-hardware-benchmarks-and-power-consumption/ |
| S7 | Raspberry Pi Active Cooler Product Brief: https://datasheets.raspberrypi.com/cooling/raspberry-pi-active-cooler-product-brief.pdf, and https://www.raspberrypi.com/products/active-cooler/ |
| S8 | Noctua NF-A4x10 5V PWM specifications: https://www.noctua.at/en/products/nf-a4x10-5v-pwm/specifications |
| S9 | Raspberry Pi M.2 HAT+ Product Brief: https://datasheets.raspberrypi.com/m2-hat-plus/raspberry-pi-m2-hat-plus-product-brief.pdf |
| S10 | Raspberry Pi SSD Product Brief: https://datasheets.raspberrypi.com/ssd/raspberry-pi-ssd-product-brief.pdf |
| S11 | Western Digital PC SN740 NVMe SSD Product Brief: https://documents.sandisk.com/content/dam/asset-library/en_us/assets/public/western-digital/product/internal-drives/pc-sn740-nvme-ssd/product-brief-pc-sn740-nvme-ssd.pdf |
| S12 | Winstar WF101NTYA4LNN0 product page (specifications, electrical characteristics): https://www.winstar.com.tw/products/tft-lcd/ips-tft/1920x1200-tft-lcd.html |
| S13 | Taiwan Screen panel database, AUO B101UAN01.C: https://www.twscreen.com/en/lcdpanel/17242/auo/b101uan01.c/10.1/1920x1200-Tablet-Computer-LCD-Panel (3P; no AUO datasheet obtained) |
| S14 | Waveshare 10.1inch HDMI LCD (G): https://www.waveshare.com/10.1inch-hdmi-lcd-g-with-case.htm and https://www.waveshare.com/wiki/10.1inch_HDMI_LCD_(G)_(with_case) |
| S15 | u-blox DAN-F10N product page: https://www.u-blox.com/en/product/dan-f10n-module |
| S16 | SparkFun GNSS Flex System hookup guide, DAN-F10N module hardware overview: https://docs.sparkfun.com/SparkFun_GNSS_Flex_System/SparkPNT_GNSS_Flex_Module_DAN-F10N/hardware_overview/ |
| S17 | SparkFun GNSS Flex pHAT – DAN-F10N (GPS-29491): https://www.sparkfun.com/sparkfun-gnss-flex-phat-dan-f10n.html |
| S18 | SparkFun GNSS Flex pHAT: https://www.sparkfun.com/sparkfun-gnss-flex-phat.html |
| S19 | u-blox ANN-MB5 data sheet UBX-22038811: https://www.u-blox.com/sites/default/files/documents/ANN-MB5_Datasheet_UBX-22038811.pdf |
| S20 | Voltaic Systems 9 Watt 18 Volt Solar Panel (P108): https://voltaicsystems.com/9-watt-18v-panel-etfe/ |
| S21 | Voltaic drawings and models: https://voltaicsystems.com/drawings-models/ (P108_dwg.pdf, P108_3D.stp) |
| S22 | Raspberry Pi 5 mechanical drawing: https://datasheets.raspberrypi.com/rpi5/raspberry-pi-5-mechanical-drawing.pdf |
| S23 | Perixx product pages: https://perixx.com/products/periboard-426, https://perixx.com/products/periboard-416, https://perixx.com/products/periboard-422, https://perixx.com/products/periboard-409h, https://eu.perixx.com/products/periboard-332 |
| S24 | Perixx product pages: https://perixx.com/products/peripad-501, https://perixx.com/products/peripad-506 |
| S25 | Southco E6 constant-torque hinge catalogue page: https://media.southco.com/media/static/Literature/e6-ct.en.pdf |
| S26 | Reell friction hinges overview: https://reell.com/products/friction-hinges |

**Source-access notes:**
- The Southco product pages were behind a bot check and were not used.
- The Raspberry Pi drawings were read as text only; see ‡ in §3.
- Link check 2026-10-01: all links resolve. raspberrypi.com, winstar.com.tw and noctua.at refuse automated requests (403/429). Their content was read in a browser or from the documentation's GitHub source.

## 11. Next dependency

Step 5: **what power architecture and battery capacity does the characterized V1 actually require?**

It needs these inputs:
- the runtime target (owner, PWR-5)
- the display brightness condition and controller data (C1, C3)
- the 5 V / 5 A rail requirement (C9)
- the off-state requirement (C10)
- the solar-replenishment principle (§6)
