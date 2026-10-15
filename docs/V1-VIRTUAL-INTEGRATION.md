# NOMAD Virtual V1 — Integration Baseline

**Date:** 2026-10-06. **Architecture:** B1 (D-010, unchanged). **Decision record:** D-011 (proposed).
**Spend:** €0. Nothing was bought, printed, assembled, measured or physically tested.

**What this is:** the integrated Virtual V1. Real candidate hardware is placed into the B1 clamshell. Every subsystem is then sized and checked: power, battery, solar, power electronics, thermal, layout, display hinges, solar leaf, harness, mass/CG, stability, DFM and BOM. Remaining unknowns are reduced to named physical-validation gates.

**Evidence labels:**

| Label | Meaning |
|---|---|
| **MFR** | Manufacturer document |
| **3P** | Distributor or third-party source |
| **REPO** | An earlier NOMAD record |
| **CALC** | Arithmetic on labelled inputs |
| **EST** | Engineering estimate |
| **ASSUMED** | Stated assumption |
| **KERNEL** | Onshape scratch-model result (REPO) |

No value here is a measurement.

**Reproduce every number:**

```bash
py CAD/tools/v1_integration.py --check
```

```bash
py prototypes/V1/v1_power.py
```

```bash
py prototypes/V1/v1_bom.py --check
```

```bash
py CAD/tools/yaml_to_featurescript.py --validate-v1
```

| File | Role |
|---|---|
| `CAD/parameters/nomad.yaml` | V1 parameter master (rewritten; the P0.1 set is frozen in `CAD/parameters/history/`) |
| `prototypes/V1/v1_hardware.py` | Hardware catalogue: one record per item, with sources |
| `prototypes/V1/v1_power.py` | Power, battery, solar, energy and heat split. It imports the E-POWER calculators unchanged |
| `CAD/tools/v1_integration.py` | Layout boxes, 57 PASS / 7 WARN / 0 FAIL checks, kinematics, hinge torque, mass/CG, stability, thermal, harness, DFM |
| `prototypes/V1/v1_bom.py` → `prototypes/V1/V1_BOM.csv` | BOM and gate totals |

---

## 0. Result

**Virtual V1 is coherent, with no open geometric conflict.**
- **Layout:** every component envelope fits the 306 × 253 × 40 base with ≥ 1 mm clearance (532 pairs checked).
- **Service:** every module comes out downward through the service panel or the battery door.
- **Rear-port conflict:** resolved mechanically. The rear face carries no plugs.
- **Round E findings:** F1 and F2 are resolved.
- **Hinges:** the display hinges are sized, and B1 is unchanged.

**What is still open:**
- The physical gates (§20).
- Seven decisions that only the owner can make (§19).
- A cost conflict with the €500–650 figure recorded in D-010 §17 (§18).

**Headline numbers** (all CALC / EST):

| Item | Value |
|---|---|
| Base / closed size | 306 × 253 × 40 mm / 306 × 253 × 73 mm (+4 mm feet). Was 301 × 235 × 40 working |
| Total mass | **3.03 kg** (range 2.52–3.54 kg). 33 % of it is manufacturer-published; the rest is EST |
| Battery | 4S1P 21700 (Molicel M65A, preliminary datasheet), 92 Wh nominal / 82.8 usable / 66.2 at end of life, holder-type pack 91.6 × 80 × 28.9 mm |
| Power at the battery | LOW 7.1 W, **NORMAL 9.0 W**, **HIGH 19.1 W**, WORST 24.4 W; off 0.07 W |
| Runtime NORMAL | **9.2 h new / 7.4 h end of life.** The 6 h target is met with +12 % margin (M65A). With 50E: 7.1 / 5.7 h, and 6 h is not met |
| Representative day | 6 h NORMAL + 1 h HIGH = 74 Wh |
| Solar into the battery (Sofia) | ≈ 48 Wh/day summer median, 36 annual mean, 16 winter median, 5 poor winter day. That is 66 % of a 6 h NORMAL day on the annual mean |
| Base heat | NORMAL 6.8 W, HIGH 15.6 W, WORST 20.9 W; lid 2.2–3.5 W |
| Internal air rise | NORMAL 6.5 K, HIGH 8.8 K (30 mm fan, 50 % in-system flow ASSUMED). HAT+ 50 °C limit → max ambient 43.5 °C NORMAL / 41.2 °C HIGH |
| Display hinge | 2 × Southco E6-10-216-50 at 1.8 N·m. Gravity torque ≤ 1.84 N·m over 60–135°; opening force 22 N; hard stop at 135° |
| Leaf hinge | SB-261-6 needs 0.78 N·m per hinge vs 0.96–1.13 published (SF 1.23 at the low end) |
| Stability | With the stay, every deployed state tips only above **12.7 m/s** wind (worst: leaf upright). Closed: 37.7 m/s |
| BOM | **≈ €1,405** prototype incl. 15 % contingency, + €179 bench-only items (approximate prices) |

---

## 1. Inspection summary (what was already solved; not redone)

Already established before this sprint, and reused:
- **B1:** D-010, SB-261 rail kernel validation and the coupon spec.
- **Power:** the E-POWER-001 loads, the E-POWER campaign (PVGIS, cells, chargers) and the E-POWER-002 4S1P architecture.
- **Layout:** the Round C base layout method (D-007 proposed) and the D-010 Phase 2 stability / wind / torque method.

This sprint adds:
- real envelopes and masses
- the integrated layout
- the lid hinge
- the thermal model
- mass/CG with V1 masses
- the BOM and the gate plan

Nothing from those records was changed. They are cited as REPO.

---

## 2. Hardware down-selection (Phase 1)

| Subsystem | V1 candidate | Key data (source) | Status | Why this one |
|---|---|---|---|---|
| Compute | Raspberry Pi 5 8 GB | 85 × 56, M2.5 on 58 × 49 (MFR-DWG); 5.1 V / 5 A; 0–70 °C | **SELECTED** (owner) | — |
| Cooling (SoC) | Raspberry Pi Active Cooler | 63.5 × 42.5 × 13.7 (MFR-DWG, interpreted), inside the 16 mm HAT header | CANDIDATE | Required for the Pi 5 (MFR) |
| Storage | M.2 HAT+ (Standard) + Raspberry Pi SSD 512 GB (2230) | PCIe 2.0 x1; HAT+ **0–50 °C ambient** (MFR) | CANDIDATE | 2230 + HAT+ + Active Cooler are compatible on paper (MFR) |
| Display panel | **AUO G101UAN01.0** (industrial 10.1", 1920 × 1200, eDP 2-lane, 380–410 nit) | 229.9 × 150.5 × 5.35 envelope (max of two 3P listings); 50 000 h LED; −20…70 or −10…60 °C (3P, **conflicting**); stock 394, MOQ 1 (3P) | CANDIDATE | See below |
| Display controller | **Beck BTC-mini-eDP** (12 V) | 80 × 70 × 9.8, 33 g, 1.10–1.29 W, eDP 1–2 lane, 0–60 °C (MFR) | CANDIDATE, price by quote | Only controller with a manufacturer datasheet (E-POWER campaign) |
| Keyboard | **Perixx PERIBOARD-416** (wired mini scissor, 78/79 keys) | **285 × 117 × 16**, 332 g, detachable USB-C cable, 0–40 °C (MFR manual, read 2026-10-06) | CANDIDATE | ≤ 8 mm is not met by any wired candidate (E-POWER-001 C4); this one has scissor keys and a detachable cable |
| Trackpad | Perixx PERIPAD-501 II (kept) | 86 × 75 × 13 (MFR manual), USB-A fixed cable | CANDIDATE, **availability unknown** | No mechanical or electrical reason to replace it. The fallback PERIPAD-506 costs +41 mm of base depth |
| GNSS | SparkFun GNSS Flex pHAT DAN-F10N (GPS-29491), kept | US$74.95, in stock; module 34 × 44, patch 20 × 20 × 8 (MFR); UART + PPS | CANDIDATE | Adequate. Cabled, not stacked |
| Enclosure fan | **Sunon MF30100V1-1000U-A99** | 30 × 30 × 10, 5 V, 0.6 W, 5.5 CFM, −10…70 °C (MFR, distributor data) | CANDIDATE | A 40 mm fan wall-mounted does not fit the 35 mm internal height |
| Display hinges | **Southco E6-10-216-50** ×2 | 1.8 N·m symmetric, 38 mm long, 4 × Ø4.5 holes, 20 000 cycles ±20 %, 155 N radial (MFR); €39.38 (RS) | CANDIDATE | Sized in §9 |
| Leaf hinges | TorqMaster SB-188-SB-261-6 ×2 (unchanged) | REPO | CANDIDATE | B1 record |
| Panel | Voltaic P108 (unchanged) | 9.92 Wp, 328 g (MFR) | CANDIDATE | B1 record |
| Power button | 12 mm sealed momentary panel button (generic SPEC) | Wired to Pi 5 J2 and charger QON | PROVISIONAL | One button for power-on, soft-off and ship-mode exit |

**Display decision (provisional):**
- **AUO B101UAN01.7**, the E-POWER electrical baseline, is **eDP 4-lane** (MFR). That is outside the BTC-mini-eDP's 1–2 lane range.
- It also has a 12 000 h LED life and 0–60 °C operating / −20…60 °C storage.
- **G101UAN01.0** is the same AUO 10.1" WUXGA class, but 2-lane and industrial-grade, with stock at MOQ 1.
- Its power is **not published** in the sources read. The B101UAN01.7 MFR figures (0.95 W logic + 2.5 W LED) are used as a proxy (ASSUMED).
- **Gate:** obtain the AUO datasheet (distributor download) and a Beck confirmation of panel support *before* buying either.

**Display controller placement (V1 change):** the controller moves into the **base** under the keyboard.
- Only a thin 30-pin eDP micro-coax passes through the display hinge, as in laptops.
- The B1 lid core stays at 19 mm, which keeps the SB-261 rail geometry exact. The space freed in the lid carries the eDP cable, foam and ribs.

---

## 3. Power budget (Phase 2)

W at the component, then at the battery (CALC; the inputs are the E-POWER loads, MFR / 3P / ASSUMED, plus the V1 additions):

| Load | Rail | LOW | NORMAL | HIGH | WORST | Basis |
|---|---|---:|---:|---:|---:|---|
| Pi 5 | 5.1 V | 3.20 | 4.00 | 8.80 | 9.80 | 3P idle / MFR typical / 3P stress |
| NVMe | 5.1 V | 0.05 | 0.05 | 2.00 | 4.70 | MFR SN740 reference; HIGH ASSUMED |
| Active Cooler | 5.1 V | 0.00 | 0.15 | 0.50 | 0.50 | firmware curve; 3P-SEC |
| GNSS | 5.1 V | 0.07 | 0.07 | 0.09 | 0.09 | MFR |
| Keyboard + trackpad | 5.1 V | 0.15 | 0.25 | 0.25 | 1.00 | ASSUMED (unpublished) |
| Enclosure fan (Sunon) | 5.1 V | 0.05 | 0.08 | 0.60 | 0.60 | MFR 0.6 W; speed by state ASSUMED (fan laws) |
| Display panel (PWM 25/50/100/100 %) | 12 V | 1.57 | 2.20 | 3.45 | 3.45 | B101UAN01.7 MFR as proxy (ASSUMED) |
| Display controller | 12 V | 1.12 | 1.12 | 1.12 | 1.29 | Beck MFR |
| **Load** | | **6.21** | **7.92** | **16.81** | **21.43** | |
| Conversion (η 0.90 / 0.88) + quiescent 0.06 + I²R | | 0.85 | 1.08 | 2.29 | 2.97 | CALC |
| **At the battery** | | **7.07** | **9.00** | **19.10** | **24.39** | CALC |
| Battery current at nominal / cutoff | | 0.49 / 0.55 A | 0.62 / 0.70 A | 1.33 / 1.50 A | 1.69 / 1.91 A | vs 6 A charger continuous |

- **Off** (Pi `POWER_OFF_ON_HALT=1`, 12 V rail disabled by the Pi): 0.071 W.
- **Ship / transport:** charger ship-FET mode, ≈ 0.
- **Representative field day** (ASSUMED: 6 h NORMAL + 1 h HIGH + 17 h off): **74.3 Wh** at the battery.
- **Peak ≠ continuous:** WORST is a thermal and electrical stress case. Runtime is quoted for NORMAL, as the owner directed (E-POWER-002 §1).

## 4. Battery (Phase 3)

**Architecture:** unchanged from E-POWER-002.
- 4S1P 21700 Li-ion: 16.8 / 14.4 / 12.8 / 11.2 V (full / nominal / system cutoff / BMS UV).
- On-pack 3–5S protector BMS (BQ77915-class, OV 4.25, UV 2.8, OCD / OCC / SCD, NTC, 50 mA balancing).
- 10 A 32 V DC MINI fuse with 1 kA breaking capacity (prospective short circuit ≈ 119 A, CALC).

**V1 choices:**
- **Cells (provisional): Molicel INR-21700-M65A.**
  - It is the only cell that meets 6 h at end of life with reserve.
  - Its datasheet is **preliminary**. Samsung 50E is the documented fallback (4 h minimum only).
- **Pack style (provisional): holder-type,** not bonded.
  - Envelope 91.6 × 80.0 × 28.9 (E-POWER-002 CALC) in a **93.6 × 82 × 31 bay**.
  - It fits the left palm bay (100 × 94.5 × 35) with 2 mm on each axis.
  - A holder pack can be built and inspected without adhesive and can be rebuilt. The bay grows only inside space that already exists, so no envelope changes.

| Cell | Nominal / usable new / EOL Wh | NORMAL h (new / EOL) | HIGH h | 6 h NORMAL with 10 % reserve | Cells mass |
|---|---|---|---|---|---|
| M65A (preliminary) | 92.0 / 82.8 / 66.2 | **9.2 / 7.4** | 4.3 / 3.5 | **met** (needs 59.4 Wh at EOL; +12 %) | 298 g (MFR) |
| 50E (mature) | 71.1 / 64.0 / 51.2 | 7.1 / 5.7 | 3.4 / 2.7 | not met (4 h met) | 278 g |

**Other figures:**
- Conversion and I²R losses take 12 % of battery energy at NORMAL.
- Pack ≈ 358 g (298 g cells + 60 g hardware, EST).
- 93.6 Wh typical, so it is below the 100 Wh air-transport threshold.

**Charging (USB-C PD, CALC, CC phase):**
- 60 W while NORMAL: 3.2 A, 0 → 90 % in ≈ 1.8 h.
- 45 W minimum: 2.4 A, ≈ 2.4 h.

## 5. Solar (Phase 4)

B1 and the P108 are unchanged.

| Condition (PVGIS 5.3, Sofia, chain 0.85 ASSUMED) | Into battery Wh/day | Share of a 6 h NORMAL day | Share of the representative day |
|---|---:|---:|---:|
| Summer median, 35° fixed, all day | 47.6 | 88 % | 64 % |
| Annual mean | 35.6 | 66 % | 48 % |
| Winter median | 15.8 | 29 % | 21 % |
| Poor winter day (P10) | 5.1 | 9 % | 7 % |
| Closed lid flat, December median | 9.1 | 17 % | 12 % |

**MPPT:** charger-integrated VOC-MPPT on the BQ25798's second input.
- **Buck-boost is required,** because hot Vmp ≈ 16.1 V < 16.8 V (INFERRED).
- USB-C takes priority. The two inputs are never summed.
- MPPT needs one I²C configuration from the Pi; defaults return after the battery is removed.

**Operation while charging:** yes, through the NVDC path.
- **Best case:** the best single hour delivers ≈ 9.2 W into the system vs 9.0 W NORMAL. So solar can at best match NORMAL briefly at midday in summer.
- **Never:** it never carries HIGH (19.1 W).
- **Conclusion:** solar replenishes energy; it does not power NOMAD continuously.

## 6. Power electronics (Phase 5)

```
USB-C (left wall) --PD sink (TPS25751)--> VAC1 --+
                                                  +--> BQ25798 NVDC buck-boost charger, VOC-MPPT --> SYS 12-16.8 V
P108 (leaf) --keyed 2-pin--ideal-diode + TVS--> VAC2 --+         |                                        |
                                                  BAT --10 A MINI fuse--BMS (BQ77915-class, on pack)--4S1P M65A
SYS --> Pololu D36V50F5 5 V 5.5 A --> Pi 5 (USB-C power plug), fan via logic FET (not via the Pi USB budget)
SYS --> Pololu S18V20F12 12 V buck-boost (EN from a Pi GPIO) --> Beck BTC-mini-eDP --> eDP panel
Button (left wall) --> Pi J2 (on / soft-off) + charger QON (ship-mode exit)
```

| Function | V1 candidate | Class | Gate |
|---|---|---|---|
| PD sink + charger + MPPT + power path | Custom power PCB: BQ25798RQMR + TPS25751DREFR + USB4105-GF-A + input protection (EST 80 × 40 × 12) | FABRICATE | 5 |
| Bench validation of the same silicon | TI **USB-PD-CHG-EVM-01** (BQ25798 + TPS25751, US$149) | BUY (bench only) | 4 |
| 5.1 V rail | Pololu D36V50F5 (5.5 A). The 5.0 V nominal vs the Pi's 5.1 V drop at 5 A must be measured (E2-R03) | BUY | 4 |
| 12 V rail | Pololu S18V20F12 | BUY | 4 |
| BMS, fuse, pack connector | BQ7791501-class on a pack PCB, Littelfuse 0297010.WXNV, Molex Micro-Fit 3.0 | FABRICATE (pack) | 4 |
| Power switch | Momentary button + ship mode. No series switch in the 10 A path (a switch is a failure point, and the pack connector is the service disconnect) | SOURCE LATER | 5 |

**Why custom:** off-the-shelf MPPT / UPS modules do not fit the 90 × 45 × 16 power zone and do not cover 4S + PD + MPPT (EP-C15, E-POWER-002 §11.2). The EVM proves the silicon first.

## 7. Thermal (Phase 6)

**Model:** lumped and CALC.
- All electrical input becomes heat. The controller and the converters are in the base; only the panel heats the lid.
- **Fan:** Sunon MF30100V1 at 5.5 CFM free air × **0.5 in-system (ASSUMED)**. Speed by state: 35 / 50 / 100 / 100 %.
- **Passive loss:** 0.3 W/K EST.
- **SoC:** 4.55 K/W over the local air. This is inferred from the Raspberry Pi blog's ≈ 64 °C SoC at sustained stress with Active Cooler + M.2 HAT on an open bench (24 °C ambient ASSUMED).

| State | Base W | Lid W | Air rise K | SoC rise K | Max ambient for the HAT+ (internal air ≤ 50 °C) | Max ambient before the SoC throttles (80 °C) |
|---|---:|---:|---:|---:|---:|---:|
| LOW | 5.5 | 1.6 | 6.7 | 21.3 | 43.3 | 58.7 |
| NORMAL | 6.8 | 2.2 | 6.5 | 24.7 | **43.5** | 55.3 |
| HIGH | 15.6 | 3.5 | 8.8 | 48.8 | 41.2 | **31.2** |
| WORST | 20.9 | 3.5 | 11.8 | 56.3 | 38.2 | 23.7 |

**Ambient operating target (provisional, owner to confirm):** **0–35 °C full function.**
- Above ≈ 31 °C, sustained HIGH load throttles gracefully (Pi firmware).
- **Storage:** −20…+50 °C. Never closed in direct sun above 35 °C (display limit).

**Cooling architecture:**
- **Airflow path:** rear-wall intake grille (120 × 13.5) + an underside grille under the keyboard zone → under the keyboard (controller, 5 V buck) → right palm bay (Pi + Active Cooler) → **exhaust fan in the right wall, front corner**.
- **Fan control:** the fan is driven from a Pi GPIO (PWM via a logic FET) on **internal-air temperature** (one NTC / sensor), not only on SoC temperature. Passive-only would be a +18 K rise at LOW.

**Battery separation:**
- The battery sits in its own left bay behind a bulkhead and its own door, outside the airflow path.
- **Charging at 60 W while NORMAL at 35 °C:** cells ≈ 39 °C (EST), under the 45 °C BMS / JEITA window.

**Sun on the lid (REPO D-010, EST, not re-run):**
- Closed in sun at 35 °C: display 50–57 °C with the 6 mm vented gap + low-e foil.
- The G101UAN01.0 limits are 3P and conflicting (60 / 70 °C). Margin is 3–13 K.

**Validation:** all of the above is VALIDATION REQUIRED.
- the fan's in-system flow
- the SoC thermal resistance in the enclosure
- skin temperature over the Pi bay
- closed-lid solar heating

## 8. Mechanical integration and base layout (Phases 7 and 10)

**Envelope:**
- **306 × 253 × 40.** Width = keyboard 285 + 2 × (8 + 2.5). Depth = 15 + 75 + 10 + 117 + 36.
- **Changes from the working 301 × 235 × 40:**
  - The keyboard is 285 × 117 × 16 instead of 280 × 105 × ≤ 8.
  - The rear zone is 36 instead of 30 (GNSS sky strip).
- **Height:** 40 is unchanged.
  - The palm bays have 35 internal height for the battery (31) and the Pi stack (30 envelope, 25.9 EST stack).
  - The under-keyboard zone shrinks to **18.5** (it was 26.5) because the keyboard is 16 thick. The boards there are ≤ 16 + 1 standoff.

| Zone | Contents (V1) |
|---|---|
| Left palm bay (own door) | Battery bay 93.6 × 82 × 31 (holder pack), bay rear wall with cable slot |
| Right palm bay | Pi 5 stack on a 2.5 mm sled plate flush in the panel pocket. Fan in the front-right corner (exhaust, right wall). Pi orientation: USB/Ethernet edge faces the trackpad-bay bulkhead; micro-HDMI / USB-C edge faces rearward |
| Under the trackpad (empty volume) | Pi USB plugs through bulkhead openings: keyboard, trackpad, 2 × USB 3.0 extensions to the front-right wall |
| Under the keyboard, left | Power board (USB-C on the left wall) + 12 V regulator; power button behind it on the left wall |
| Under the keyboard, centre | Beck controller; display-cable riser to the hinge pass; flat trunk over it |
| Under the keyboard, right | 5.1 V buck, behind the Pi rear-plug zone |
| Rear strip (y 217–250) | GNSS pHAT under a non-metallic deck window (sky keep-out 40 × 29.5); display-hinge corner blocks 44 × 24 |

**Results** (`v1_integration.py`, modelled):
- 532 envelope pairs: **0 violations** (≥ 1.0 mm, keyboard and trackpad 0.3 deck fit).
- Every module is removable downward: battery through its door; Pi, power board, controller, 5 V buck, GNSS and fan through the main / front panels.
- The keyboard and trackpad lift out upward (Round C principle).
- **Round E F1 resolved:** panel screw axis 3.5 mm from the wall (YAML `PANEL_SCREW_INSET`). The ISO 7380 M3 head clears the wall by 0.65, and the panel ligament is 1.5.
- **Round E F2 resolved:** the sled is a panel insert with countersunk M2.5 screws, so no head layer remains.

**Fasteners:**
- M2.5 / M3 heat-set family, plus **M4 only** for the Southco hinges (Ø4.5 holes) and the stay pivots.
- Bosses Ø8 (2.0 wall on the RX-M3x5.7 Ø4.0 hole); tray posts Ø6.

## 9. Lid and display hinges (Phase 8)

**Lid stack:** core 19 + air gap 6 + leaf 6 = **31**.
- The display is centred: y 51–202 in a 253 deep lid. The SB-261 rail needs ≥ 42.5 free at the free edge: met.

**Gravity torque about the display axis** (lid 652 g + leaf 413 g, CALC; + = tends to open):

| Leaf | 0° | 60° | 90° | 105° | 120° | 135° |
|---|---:|---:|---:|---:|---:|---:|
| Stowed | −1.33 | −0.50 | +0.19 | +0.53 | +0.83 | +1.08 |
| ψ 110 | −1.99 | −0.47 | +0.60 | +1.10 | +1.52 | **+1.84** |
| ψ 190 | −2.27 | −1.08 | +0.06 | +0.65 | +1.19 | +1.65 |

**Selection:**
- **Requirement:** 2 hinges at the −20 % torque low bound ≥ 1.5 × max |torque| over 60–135° → **1.38 N·m per hinge.**
- **Choice: Southco E6-10-216-50, 1.8 N·m** (low bound 1.44).
- **Opening force** at the free edge, worst case near closed at +20 %: **22 N** (≤ 25 N ASSUMED). The asymmetric E6-10-216F-50 (1.8 / 1.1) is the fallback if it feels stiff.
- **Radial load:** 5.2 N per hinge, vs 155 N MFR.

**φ-max = 135° hard stop:**
- Printed stop faces in the corner blocks, at r 12.
- Gravity + 10 m/s front wind (2.36 N·m) is held by hinge friction.
- A 30 N misuse push at the free edge gives 265 N per stop and 5.5 MPa bearing. That is under PETG 25 MPa / SF 2 (EST). A steel stop pin is the fallback.

**Rear-port / lid-sweep conflict: RESOLVED mechanically.**
- With T 31, the lid corner reaches z 16.7 at 135°. That would hit the old rear connector zone (top z 19, Round C).
- **V1 puts no plugs on the rear face:**
  - USB-C power and the button on the left wall
  - USB on the front-right wall
  - exhaust on the right wall
  - the Pi's own ports used internally
- The rear face keeps only the intake grille and the display-cable pass.
- The lid clears the table and the deployed stay (lowest point z 16.7, table z −4).
- No operating rule is needed. The D-007 "rear vs side I/O" question is answered by geometry. Owner confirmation is still required (§19).

**Display-hinge cable pass:**
- eDP micro-coax + solar lead through a centre knuckle (20 mm wide) between the hinges.
- 60 mm axial twist zone: 135° → 2.25 °/mm (≤ 3.5, D-010 ASSUMED limit).

## 10. B1 solar-leaf integration (Phase 9)

**Unchanged from the B1 record:**
- SB-261 axis at (y 4.0, z 63.5) closed. The lid core stays 19 and the closed gap 2, so the scratch-validated rail is exact (KERNEL, REPO).
- 0–190°, first contact at 201°, R12 sleeve, 64 mm twist zone at 2.97 °/mm.

**V1 changes:**
- **Leaf outline:** now 290 × 239, i.e. the panel + 2 × 8 frame.
  - The lid grew to 253 deep, but the leaf follows the panel, not the lid. Leaf mass stays ≈ 413 g (P108 328 + frame 65 + latch / wiring 20).
  - **Effect:** leaf-hinge demand is 0.78 N·m per hinge (gravity 0.47 + 10 m/s wind 0.58, × 1.5 / 2). Against 0.96–1.13 published, **SF ≈ 1.23**. The REPO basis was 0.83 / SF 1.16.
- **Hinge placement:** hinges at ±115 sit inside the frame (outer end x 131.9 vs frame inner x 137).
- **Stay:** pivots in the rear corner blocks, 28 mm from the side and 13 mm from the rear face. Reach 105. Mandatory (D-010).

**Kept from D-010 (WARN):**
- At φ ≥ 120° and low leaf angles (ψ 10–75), the leaf free edge touches the table.
- The leaf rests on the table; there is no damage path.
- **Operating rule kept: open the leaf before the lid.** A 120° lid stop would remove the contact but cost solar aim. That is an owner choice, and the rule stands.

## 11. Cable harness (Phase 11)

Estimated lengths: Manhattan route × 1.25 + 30 mm service. Final lengths are fixed at the gate-2/3 fit-up.

| Cable | Type | Route | Est. length | Min bend R | Connectors / service |
|---|---|---|---:|---:|---|
| Battery lead | 2 × 16 AWG + NTC | pack → power board | 140 | 10 | Micro-Fit 3.0 keyed latching; unplug at the door |
| SYS → 5.1 V buck | 2 × 18 AWG | left → right under the keyboard | 330 | 8 | JST-XH / terminal |
| 5.1 V → Pi | power-only USB-C plug, 2 × 18 AWG | buck → Pi rear edge | 100 | 15 | right-angle USB-C |
| 12 V → controller | 2 × 22 AWG | power board → Beck | 220 | 6 | JST-PH |
| HDMI0 → controller | micro-HDMI → HDMI FPC | Pi rear edge → Beck | 270 | 10 | plug both ends |
| **eDP → panel** | 30-pin micro-coax | Beck → riser → hinge knuckle → lid | 320 (spec 380 ± 20) | 5 | I-PEX-class; 60 mm twist zone |
| **Solar lead** | 2 × 0.5 mm², d 4 | leaf sleeve (R12) → lid run → hinge knuckle → power board | 860 | 12 | keyed 2-pin at the leaf (lift-off) and at the board |
| USB keyboard | short USB-C → A | keyboard → Pi USB2 under the trackpad | 170 | 15 | plug |
| USB trackpad | fixed USB-A lead, coiled | trackpad → Pi USB2 | 120 + coil | 15 | clip |
| USB 3.0 external ×2 | panel-mount extensions 0.3 m | Pi USB3 → front-right wall | 160 | 20 | panel socket |
| GNSS | 6 × 26 AWG (3V3, GND, TX, RX, PPS) | Pi GPIO pass-through → rear strip | 490 | 8 | Dupont housings |
| Fan | 2 × 26 AWG via FET | 5.1 V rail → fan | 210 | 8 | JST-PH |
| Button + LED | 4 × 26 AWG | left wall → Pi J2 + charger QON | 450 | 8 | JST-SH / PH |
| Charger I²C | 4 × 28 AWG | power board → Pi I²C1 | 370 | 8 | JST-SH 4 |

**Rules:** no cable runs through structure, gears or the hinge-block load path. Every cable that crosses a module boundary has a connector. There are no slip rings.

## 12. Mass, CG and stability (Phase 12)

**Mass (g):**

| Subsystem | Mass | Main items |
|---|---:|---|
| Base | 1 859 (61 %) | shell 355, panels 261, trays 141 (EST); keyboard 332 (MFR); battery 298 + 60; trackpad 90; Pi stack 89; electronics ≈ 120; hinges, fasteners, harness ≈ 87 |
| Lid | 652 (22 %) | lid core 411 (ASA, EST); display 170 (EST); hinges, cable, spacers 71 |
| Leaf | 413 (14 %) | P108 328 (MFR); frame 65; latch / wiring 20 |
| Stay | 105 (3 %) | REPO D-010 |
| **Total** | **3 029** | 33 % MFR-published. Range 2.52–3.54 kg (EST items ±25 %) |

- **Heavier than the D-010 basis** (2.62 kg). The causes are the real keyboard (332 g vs 250), a printed shell computed from the envelope, and the battery pack.
- **This helps stability.**

**Stability** (D-010 Phase 2 method, re-implemented; rigid table, feet 8 mm in, flat-plate wind; CALC):

| State | CG y / z | Rear margin | Rear tip wind |
|---|---|---:|---:|
| Closed | 119.8 / 32.3 | 125 mm | 37.7 m/s |
| Open φ 110 | 185.9 / 66.0 | 59 | 13.4 |
| NORMAL (ψ 65), no stay / with stay | 202.5 / 70.5 | 42 / 139 | 11.8 / **19.6** |
| Leaf horizontal, no stay / with stay | 206.7 / 82.0 | 38 / 134 | 9.0 / **19.7** |
| Leaf upright ψ 190 + stay | 196.6 / 97.1 | 148 | **12.7** (front 12.4) |
| Worst rearward φ 135 ψ 135, no stay / with stay | 227.6 / 65.8 | **17** / 114 | 5.8 / **18.9** |

- **Verdict:** mechanically sensible. The stay remains mandatory.
- Every deployed state with the stay holds above 12 m/s wind.
- Without the stay, the worst rearward pose has only 17 mm gravity margin.

## 13. Structural / manufacturing review (Phase 13)

| Topic | Finding | Status |
|---|---|---|
| Walls / panels / plates | 2.5 / 2.5 / 2.0 ≥ 2.0 MIN_WALL | PASS |
| Insert bosses | Ø8 around the Ø4.0 RX-M3x5.7 hole: 2.0 wall. Tray posts Ø6 around M2.5 OD 3.55: 1.2 wall | PASS (was 1.5 / 0.7) |
| Panel screws | F1 fixed (`PANEL_SCREW_INSET` 3.5) | PASS |
| Print orientation | Base shell deck-down (Round C: no overhangs). Lid core bezel-down. Panels flat. Leaf frame flat, support-free (D-010) | PASS (modelled) |
| **Bed size** | Base shell 306 × 253, panels 301 × 248, keyboard tray 301 × 123, lid core 306 × 253, leaf frame 290 × 239 **need a ≥ 310 mm bed** (Bambu H2D 350 × 320 / Prusa XL class) | **WARN** |
| Split option | On a 256 bed, split each large part on X = 0 with a 15 mm lap joint + M3 inserts. The leaf frame splits as already planned in D-010 (the FR4 panel bridges the split). Owner question §19 | — |
| Printed mass | 1 233 g (PETG 757, ASA 476) EST → buy 2 kg PETG + 1 kg ASA | — |
| Hinge mounting | Display hinges: M4 inserts in 44 × 24 corner blocks (40 % infill, solid around inserts). Leaf hinges: REPO rail | modelled |
| Heat-set access | Every insert is installed from the open underside or the lid interior before closing | modelled |
| Battery replacement | Door (4 × M3 captive) → unlatch Micro-Fit → lift the pack out. No other part disturbed | PASS (service check) |

**Assembly sequence:**
1. Install inserts in the shell.
2. Fit the hinge blocks' M4 inserts.
3. Keyboard tray and keyboard (from the top).
4. Trackpad tray and trackpad.
5. Under-keyboard boards: power board, Beck, 5 V buck, GNSS (from below).
6. Harness and Pi sled into the panel pocket; fan.
7. Close the main panel.
8. Battery into its bay; close the door.
9. **Lid:** display into the bezel; eDP cable; lid back shell; SB-261 rail and leaf; solar lead through the knuckle; display hinges to the base corner blocks.
10. Stay.

## 14. Virtual V1 validation (Phase 14)

All existing repository checks were run before and after the sprint (§16 of the build-log entry).
- **Every P0.1 study and generator reproduces byte-identical output.** The one expected exception: `yaml_to_featurescript.py --check` now names the frozen snapshot path.
- **New checks:**
  - `v1_integration.py --check`: 57 PASS, 7 WARN, 0 FAIL
  - `--validate-v1`: valid, every parameter in the spec
  - `v1_bom.py --check`: current
  - `v1_power.py`: runs

**The 7 WARN items are engineering facts, not defects:**
- the leaf/table contact rule
- HIGH throttling above 31 °C
- the bed size (5 parts)

## 15. Source of truth (Phase 15)

- **`CAD/parameters/nomad.yaml`** now describes **only Virtual V1**: 96 parameters, 55 with a provisional value, the rest TBD with working inputs.
  - Architecture A, class-A lid, rear port panels and D-009 groups are gone from it.
  - They are kept, unchanged, in **`CAD/parameters/history/nomad_P0.1_2026-10-02.yaml`**.
- **`yaml_to_featurescript.py`:**
  - The P0.1 FeatureScript files (`NOMAD_P01.fs`, `NOMAD_E_Prototype.fs`) and every P0.1 study now read the frozen snapshot, so they reproduce exactly.
  - `--validate-v1` validates the V1 master.
- **`docs/mechanical-spec.md`:** V1 tables generated from the YAML, plus the frozen P0.1 record.
- **No V1 FeatureScript or Onshape geometry was written.** No Onshape API calls were made this sprint. The integrated V1 is an envelope model in `v1_integration.py`.

## 16. Completion review (Phase 16)

| Subsystem | Classification | Why |
|---|---|---|
| Architecture (B1) | **COMPLETE** | Locked; integrated without change |
| Compute stack | **PROVISIONAL** | Pi selected; stack height EST 25.9 vs envelope 30, to measure |
| Storage | **PROVISIONAL** | Candidate; SSD power unpublished |
| Display + controller | **PROVISIONAL / BLOCKED on data** | G101UAN01.0 datasheet (power, connector position, surface, temperature) and Beck panel support + price are needed before purchase |
| Keyboard | **PROVISIONAL** | Real part, MFR dimensions; ≤ 8 mm target formally replaced (owner) |
| Trackpad | **PROVISIONAL** | Availability unknown |
| GNSS | **PHYSICAL VALIDATION REQUIRED** | Envelope and placement defined; sky-window performance only by test |
| Power budget | **PROVISIONAL** | Display power proxy; HID and SSD power unpublished |
| Battery | **PROVISIONAL** (cell = owner) | Architecture complete; M65A datasheet preliminary |
| Solar | **PHYSICAL VALIDATION REQUIRED** | Yield modelled; MPPT behaviour and panel heat by test |
| Power electronics | **PROVISIONAL** | Architecture and parts defined; the custom PCB is a design task after the EVM gate |
| Thermal | **PHYSICAL VALIDATION REQUIRED** | Architecture defined; flow and SoC resistance ASSUMED |
| Mechanical integration (base) | **COMPLETE (virtual)** | 0 violations; service paths; F1 / F2 closed |
| Display hinge / rear ports | **COMPLETE (virtual)**, PHYSICAL VALIDATION REQUIRED | Sized; conflict removed |
| B1 leaf | **PHYSICAL VALIDATION REQUIRED** | Unchanged; the coupon gate stands |
| Harness | **PROVISIONAL** | Routes and types; lengths at fit-up |
| Mass / CG / stability | **PROVISIONAL** | 67 % of mass EST |
| DFM | **PROVISIONAL** | Bed-size decision open |
| BOM | **PROVISIONAL** | Approximate prices; 3 quotes needed (Beck, TorqMaster, AUO distributor) |
| Integrated V1 CAD in Onshape | **BLOCKED** (owner action + API budget) | Envelope model exists. Persistent CAD needs owner-created Part Studios and a deliberate API spend (§21) |

## 17. Preliminary BOM (Phase 17)

**Full table:** `prototypes/V1/V1_BOM.csv` and `py prototypes/V1/v1_bom.py`.

**Pricing basis:**
- EUR, approximate, as found 2026-10-01…06.
- US-listed prices are × 0.86 (FX, ASSUMED) × 1.30 (shipping and import, ASSUMED).
- Nothing was ordered.

| Group | EUR |
|---|---:|
| Electronics (buy + fabricate + source later) | 958 |
| Mechanical / materials (hinges, stay, inserts, wire, filament) | 264 |
| Subtotal prototype | 1 222 |
| Contingency 15 % | 183 |
| **Estimated V1 prototype** | **≈ 1 405** |
| Bench-only validation items (TI EVM, 27 W PSU) | + 179 |

**Largest items:**

| Item | EUR |
|---|---:|
| Pi 5 8 GB (BerryBase, 2026 price) | 185 |
| TI EVM | 167 |
| G101UAN01.0 | 123 |
| Beck (EST, quote) | 120 |
| GNSS pHAT | 84 |
| Southco hinges | 79 |

**Cost conflict:** D-010 §17 recorded "budget €500–650 overall". The V1 BOM is ≈ 2.2 × that. Levers that change no architecture (owner, §19):
- Generic friction hinges instead of Southco: −€60, but no published torque data.
- A generic RTD2556 controller instead of Beck: −€95, but reseller data only.
- Skipping the EVM: −€167, at the cost of more PCB risk.
- Deferring the GNSS pHAT to after integration: €84 later.

## 18. Staged purchase plan (Phase 18)

**Rule:** never buy an expensive part before its cheaper dependency is validated on paper or on the bench.

| Gate | Buy | Approx. EUR | Entry condition (paper / bench) | Exit (what it proves) |
|---|---|---:|---|---|
| **0** (now, €0) | — | 0 | — | Datasheets / quotes: AUO G101UAN01.0 datasheet, Beck support + price, TorqMaster price, PERIPAD-501 II availability, P108 stock |
| **1 — mechanical risk** | 2 × SB-261-6 (+1 spare), inserts and fasteners, 2 kg PETG + 1 kg ASA, stay flats + M4 shoulder screws | ≈ 150 | Owner approves D-011 placement | SB-261 coupon (COUPON_SPEC §7), stay tip test with dummy masses, P0.2 wall / insert coupons, bed / split decision |
| **2 — envelope-critical HMI** | Display + Beck + eDP cable, keyboard, trackpad, 2 × Southco E6 | ≈ 420 | Gate 0 data confirms panel / controller compatibility; gate 1 passes | Fit in a printed lid/base mock-up; hinge feel; display brightness and power measured |
| **3 — compute** | Pi 5 + cooler + HAT+ + SSD, GNSS pHAT, fan, 27 W PSU | ≈ 360 | Gate 2 fit OK | Stack height, port / plug fit, thermal in the printed base on the PSU, GNSS sky-window test |
| **4 — power validation** | TI EVM, 4 (+1) cells, Pololu 5 V / 12 V, P108, BMS parts | ≈ 360 | Cell decision (owner); gate 3 loads measured | PD contract, MPPT on the P108, 4S charge, rail drops at 5 A, runtime at measured loads |
| **5 — integration** | Custom power PCB fab + parts, harness, button, USB extensions | ≈ 115 | EVM settings proven | Full V1 build |

**Cumulative:** ≈ €1 400 before contingency, spread over five decisions.

## 19. Owner decisions (collected; nothing else needs the owner)

1. **D-011 / D-007 placement.** Accept the V1 base placement:
   - battery left bay, compute right bay, power / controller / GNSS under the keyboard and in the rear strip
   - **side / front I/O with no rear plugs**
   - controller in the base

   This is under the approval gate (major module placement, I/O).
2. **Envelope growth** to 306 × 253 × 40, and the keyboard replacing the ≤ 8 mm target (PERIBOARD-416, 16 mm).
3. **Battery cell:** M65A (preliminary datasheet, 6 h met) or 50E (4 h minimum only). The holder-type pack and bay growth are adopted provisionally.
4. **Display:** confirm the D-A family path (G101UAN01.0 + Beck) over D-W. D-W misses 6 h.
5. **Ambient target:** 0–35 °C operating (provisional), storage −20…+50 °C.
6. **External I/O list:** USB-C PD charge only (no barrel); 2 × USB-A; no Ethernet, no HDMI out, **no audio** in V1.
7. **Budget vs BOM** (≈ €1 405 vs €500–650) and **print access** (a ≥ 310 mm bed / print service, or split parts).

## 20. Physical validation still required (exact tests)

| # | Test | Pass criterion | Gate |
|---|---|---|---|
| 1 | SB-261 coupon: torque vs angle at 0 / 23 / 45 °C, cycle 1 000, slip under the 413 g leaf + 10 m/s equivalent load | holds ≥ 0.78 N·m per hinge, no creep | 1 |
| 2 | Stay tip test (dummy masses at the computed CG, fan wind / spring scale) | rear tip ≥ 12 m/s equivalent with the stay | 1 |
| 3 | P0.2 coupons: wall, insert pull-out (M3 / M4), PETG / ASA warp | per P0.2 plan | 1 |
| 4 | Display + Beck bench: image, brightness, 12 V current at 25 / 50 / 100 % | ≤ 4.7 W system at full | 2 |
| 5 | Lid mock-up with display and Southco hinges: holding 60–135°, opening force, stop | holds; ≤ 25 N | 2 |
| 6 | Pi stack measured; ports and plugs through the bulkhead openings; HDMI / USB-C plug clearance under the tray | fits the envelopes | 3 |
| 7 | Thermal in the printed base: NORMAL / HIGH at 25 °C ambient, internal air, SoC, palm-rest skin | air rise ≤ 10 K NORMAL; HAT+ air ≤ 50 °C at 35 °C extrapolated | 3 |
| 8 | GNSS sky window: TTFF and C/N0 lid open / closed vs bare module | ≤ 3 dB loss open | 3 |
| 9 | Power: EVM PD 45 / 60 W, P108 MPPT (VOC_PCT 0.8125 / 0.875), 4S charge to 16.8 V, JEITA | stable, both inputs, priority correct | 4 |
| 10 | 5.1 V drop at 5 A at the Pi; runtime at measured NORMAL | Pi no under-voltage; ≥ 6 h at EOL by extrapolation | 4 |
| 11 | Cable twist cycling: solar lead + eDP through the knuckle, 5 000 cycles | no conductor / coax damage | 2–4 |
| 12 | Closed-lid sun thermal mock-up (gap + foil) | display ≤ datasheet storage limit at 35 °C | 4 |

## 21. Not done (deliberately)

- **No Onshape writes.** A persistent V1 Feature Studio would cost API allocation, and the owner must create the Part Studio. The envelope model holds every coordinate and can be emitted when the owner approves D-011.
- No PCB design, no final pack design, no drawings. Those are post-gate work.
- No GitHub, README or licence work; no commit.
