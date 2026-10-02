# E-POWER-002 — NOMAD V1 Power Architecture Baseline

**Date:** 2026-10-02. **Status: engineering baseline for the next phase.** It is virtual engineering only.
- **Not done:** no part is purchased, no SKU is selected, and nothing is physically validated (battery safety and thermal behaviour included).
- **Evidence base:**
  - `docs/E-POWER-RESEARCH-CAMPAIGN.md` (the dossier)
  - targeted datasheet checks (TI BQ25798, BQ77915, TPS25751 / TPS25730; Littelfuse MINI)
  - DigiKey prices (all 2026-10-02)
- **Calculator:** `prototypes/V1/epower_architecture_calc.py`. Run it with `py prototypes/V1/epower_architecture_calc.py`. It imports its loads from `epower_campaign_calc.py`, so the two cannot drift apart.
- **Unchanged:** `CAD/parameters/nomad.yaml`, CAD, Onshape, B1, D-010 and D-007.

**Labels:**

| Label | Meaning |
|---|---|
| **MFR** | Manufacturer |
| **3P** | Third party |
| **CALC** | Calculated |
| **ASSUMED** | Stated assumption |
| **EST** | Estimate |
| **UNKNOWN** | Not determined |
| **LOCKED** | Owner decision |
| **BASELINE** | Engineering recommendation used for continued development |
| **PROVISIONAL** | Reasonable assumption, may change |
| **TBD / OWNER** | Needs explicit owner approval |

---

## 0. Result in one paragraph

**Baseline architecture:** **4S1P 21700 Li-ion → NVDC buck-boost charger / power path (BQ25798-class) → system bus 12–16.8 V → 5.1 V / ≥ 5 A buck (Pi 5 and everything it powers) + 12 V buck-boost (display controller).** It has USB-C PD as the primary input on charger input 1 and the P108 on input 2 (MPPT), with a standalone 3–5S protector BMS and a 10 A automotive MINI fuse on the pack.
- **Why this choice:**
  - Only four 21700 cells fit the bay, so 1S4P, 2S2P and 4S1P carry the same energy, and 3S carries only three cells.
  - **4S has the lowest battery current:** ≤ 2.6 A worst case. It keeps the charger inside its 6 A discharge limit with large margin, matches the charger's documented best-efficiency point (16 V, 3 A, from 20 V: 96.5 %), and gives the 5 V buck ample headroom.
- **Runtime** (display D-A, normal use, with a 92 Wh-class pack): about **9.3 h new / 7.4 h at end of life.** The 6 h target is met with reserve.
- **Two things are not settled and need you:**
  1. That runtime relies on the **Molicel M65A**, whose datasheet is **preliminary**. A mature 71 Wh cell meets the 4 h minimum but **not** 6 h at end of life.
  2. **The pack fits the 90 × 82 × 30 bay only as a tightly bonded pack.** A conventional cell-holder pack needs about **93.6 × 82 × 31**.

## 1. Owner direction and status of every item

| Item | Status | Value / note |
|---|---|---|
| Runtime | **LOCKED** (owner, 2026-10-02) | **6 h normal-use design target; 4 h minimum acceptable.** 8 h is reference only and does not drive the architecture |
| Load definition | **LOCKED** (owner, 2026-10-02) | Runtime applies to normal interactive use. Maximum sustained load is a separate thermal and electrical stress case |
| Battery energy | **LOCKED** direction (owner) | ≤ 92 Wh if realistically possible; do not casually exceed 100 Wh |
| Solar | **LOCKED** (owner; D-010) | Keep the P108 and B1. Solar is supplementary, never the primary source |
| Display for calculations | **PROVISIONAL** | D-A (AUO eDP + Beck BTC-mini-eDP) is the electrical baseline. **Not a display selection.** D-W is carried as a comparison |
| Cell configuration 4S1P 21700 Li-ion | **BASELINE** | §3–§4 |
| Cell type | **PROVISIONAL**, **TBD / OWNER** | M65A (preliminary datasheet) for 6 h; 50E-class mature cell gives the 4 h minimum only |
| Charger: NVDC buck-boost, 1–4S, dual input, MPPT (BQ25798-class) | **BASELINE** (topology). Exact charger PCB **TBD** | §6 |
| USB-C PD sink, 20 V 3 A preferred, ≥ 45 W minimum | **BASELINE** (input profile). Controller part **TBD** (TPS25751 or TPS25730 class) | §7 |
| P108 on charger input 2, VOC-MPPT, USB-C priority | **BASELINE** | §8 |
| BMS: standalone 3–5S protector + passive balancing on the pack | **BASELINE** (requirements). SKU **TBD** | §9 |
| Pack fuse: 10 A, 32 V DC, ≥ 1 kA breaking (MINI blade class) | **BASELINE** (requirement). Exact part **TBD** | §9 |
| 5.1 V rail ≥ 5 A buck; `PSU_MAX_CURRENT=5000` | **BASELINE** | §5 |
| 12 V ±5 % rail, buck-boost, ≥ 1 A | **BASELINE** (for D-A / D-W controllers) | §5 |
| DC barrel input | **Not recommended** (§7.4). Owner may confirm | — |
| Connectors, wire gauge, exact parts | **TBD** | Requirements are given; no SKU is locked |
| Battery bay growth for a holder-type pack | **TBD / OWNER** (D-007 / YAML step 7) | §11 |
| Active Cooler | Repository status: **candidate** (`docs/hardware.md`). Owner brief calls it the selected cooling direction | Not changed here; flagged for the owner (§14) |

## 2. Loads used

The loads come from the campaign calculator; this document does not re-research them.

| Case | 5 V-rail load (Pi + NVMe + fan + GNSS + HID) | 12 V-rail load (display system) | Total |
|---|---:|---:|---:|
| NORMAL, D-A (Pi 4.0 W MFR "typical active"; display 50 % PWM) | 4.52 W | 3.32 W | 7.84 W |
| NORMAL, D-W | 4.52 W | 5.03 W | 9.55 W |
| HIGH, D-A (Pi 8.8 W stress, wall, 3P; NVMe 2 W ASSUMED; display full) | 11.64 W | 4.57 W | 16.21 W |
| WORST, D-W (Pi 9.8 W; NVMe 4.7 W MFR bound; display full, controller max) | 16.09 W | 8.88 W | 24.96 W |

**Caveat:** the HID, Active Cooler, HAT+ and Raspberry Pi SSD power values remain UNKNOWN or ASSUMED (dossier EP-C18). The NORMAL Pi value is the manufacturer's "typical bare-board active" figure, not a NOMAD measurement.

## 3. Architecture comparison (4 cells fit the bay; 3S uses 3)

**CALC** with M65A cells. Efficiencies are ASSUMED inside manufacturer bands:
- Pololu buck: 80–95 %
- buck-boost: 80–90 %
- boost: 80–95 %

| | **A 1S4P** | **B 2S2P** | **C 3S1P** | **D 4S1P** |
|---|---|---|---|---|
| Cells | 4 | 4 | **3** | 4 |
| Full / nominal / cutoff (3.2 V/cell, ASSUMED) / BMS UV (2.8) | 4.2 / 3.6 / 3.2 / 2.8 V | 8.4 / 7.2 / 6.4 / 5.6 V | 12.6 / 10.8 / 9.6 / 8.4 V | 16.8 / 14.4 / 12.8 / 11.2 V |
| Nominal / usable new / EOL | 92.0 / 82.8 / 66.2 Wh | 92.0 / 82.8 / 66.2 Wh | **69.0 / 62.1 / 49.7 Wh** | 92.0 / 82.8 / 66.2 Wh |
| Battery current NORMAL (nominal V) | 2.61 A | 1.22 A | 0.83 A | **0.62 A** |
| Battery current WORST (cutoff / BMS UV) | **10.7 / 13.3 A** | 4.5 / 5.2 A | 3.0 / 3.5 A | **2.2 / 2.6 A** |
| BQ25798 discharge limit, 6 A continuous / 10 A peak / OCP 9.3 A (MFR) | **exceeded** (HIGH D-W is 7.4 A even at 3.0 V/cell) | OK | OK | OK, ≥ 2.3× margin |
| 5 V stage | boost, ~25 W from 3–4.2 V (very high input current) | buck from 5.6–8.4 V: **dropout near empty at 5 A** | buck from 8.4–12.6 V | buck from 11.2–16.8 V, ample headroom |
| 12 V stage | boost | boost | buck-boost (straddles 12 V) | buck-boost (straddles 12 V) |
| Charger | 1S: large step-down from 20 V (lower efficiency, ASSUMED 0.90) | 2S | 3S | **4S: matches the BQ25798 96.5 % datasheet point** |
| Solar (P108, Vmp ≈ 16–17.3 V) | buck works | buck works | buck works | **buck-boost required** (hot Vmp ≈ 16.1 V < 16.8 V) — BQ25798 is buck-boost |
| BMS / balancing | 1S protector, no balancing (parallel) | 2S protector, 2 groups to balance | 3S, balancing | 4S, balancing (BQ77915-class, 50 mA) |
| Wiring and current | thick conductors, ≥ 15 A-class contacts | moderate | low | **lowest** |
| Converter count | 2 + charger | 2 + charger | 2 + charger | 2 + charger |
| Heat, NORMAL D-A / WORST D-W at cutoff (converters + I²R) | 1.56 / 9.2 W | 0.92 / 3.8 W | 1.08 / 4.0 W | 1.07 / 3.8 W |
| Pack fit in bay | 4 cells (tight, §11) | 4 cells (tight) | 3 cells (fits easily) | 4 cells (tight) |
| Meets 6 h at EOL with reserve (D-A) | energy yes, but **current fails** | yes | **no** (5.6 h at EOL, no reserve) | **yes** |
| Serviceability | parallel-only pack, simplest swap | parallel groups | simple | series pack; cells must be matched |
| Safety / protection complexity | high current, short-circuit energy at low voltage | moderate | moderate | moderate (16.8 V, SELV) |
| Expandability | poor (current) | fair | low (energy) | **good** (12–16.8 V bus suits 12 V accessories via the buck-boost) |

**Conclusions (documented engineering, CALC from MFR limits):**
- **A (1S) is rejected for a BQ25798-class charger.** Battery current exceeds the charger's continuous discharge rating (6 A) at HIGH load and its over-current trip (9.3 A) at WORST load.
- **C (3S) is rejected for the 6 h target.** Only three cells fit, giving 49.7 Wh usable at end of life.
- **D (4S1P) is the baseline.** **B (2S2P) is the documented fallback.** B has a 5 V-rail dropout problem near empty and twice D's current.

## 4. Baseline battery pack (4S1P 21700)

| | M65A (preliminary) | 50E (mature) |
|---|---|---|
| Arrangement | 4S1P, 4 cells | 4S1P, 4 cells |
| Full / nominal / system cutoff / BMS UV | 16.8 / 14.4 / 12.8 / 11.2 V | same |
| Nominal Wh (rated min / typ) | 92.0 / 93.6 | 71.1 |
| Usable new (× 0.90) / end of life (× 0.80) | 82.8 / 66.2 Wh | 64.0 / 51.2 Wh |
| Mass: cells / pack estimate (× 1.20) | 298 g / ≈ 358 g | 278 g / ≈ 334 g |
| Pack DC resistance (cells) | ≈ 100 mΩ (25 mΩ/cell, MFR) | ≈ 100 mΩ (ASSUMED) |
| Cell continuous limit | 26 A | 9.8 A |
| Cell charge window | 0–60 °C | 0–45 °C |
| Battery current | NORMAL 0.62 A; WORST 2.2 A at cutoff / 2.6 A at BMS UV; charging ≤ 3.2 A (§7) | same order |
| IATA class | 93.6 Wh typical, **< 100 Wh** | < 100 Wh |

**Required ratings:**
- **BMS:** continuous discharge ≥ 3 A; charge ≥ 5 A (charger max); over-current trip about 2–3× the continuous value; short-circuit trip well below the cell pulse limit.
- **Prospective short-circuit current at full charge:** ≈ **119 A** (CALC: 16.8 V ÷ (100 mΩ pack + 41 mΩ path)).

**Not a finished battery:** *the 92 Wh figure is the cell sum. The usable energy above already removes the 3.2 V/cell cutoff window and end-of-life fade. Pack fit is in §11.*

## 5. Power tree (baseline)

```
USB-C receptacle (rear port panel; >= 3 A VBUS rating)            P108 leaf (Voc 20.45 V, Vmp 17.34 V, Imp 0.57 A STC)
   |                                                                  |  0.85 m cable through leaf sleeve + display-hinge pass
 PD sink controller (TPS25751-class: PD3.1 sink, 20 V/5 A path,      connector -> reverse-polarity ideal-diode FET -> TVS
 dead-battery, I2C control of the charger) - requests 20 V 3 A       |
   |  VAC1 (primary) -- back-to-back NFETs ACFET1/RBFET1        VAC2 (secondary) -- ACFET2/RBFET2
   +------------------------------+-----------------------------------+
                                  v
     CHARGER / NVDC POWER PATH (BQ25798-class): 3.6-24 V in, <= 3.3 A in, buck-boost, VOC-MPPT,
     VAC OVP = 26 V, charge <= 5 A (baseline 3.2 A), VSYSMIN 12.0 V (4S default), BATFET 11 mOhm
           |                                      |
      SYS BUS 12.0-16.8 V (battery-only:      BAT -- 10 A MINI fuse (32 V DC, 1 kA) -- BMS (3-5S protector,
      ~VBAT; with input: >= VSYSMIN)             low-side FETs, Rsense, NTC, 50 mA balancing) -- 4S1P 21700 pack
           |                                     (pack connector: P+, P-, NTC -> charger TS / JEITA)
   +-------+-----------------------------------------------+
   |                                                       |
 5.1 V / >= 5 A buck (D36V50F5-class, 80-95 %)       12 V +-5 % buck-boost (S18V20F12-class, 2 A, 80-90 %)
   | in: 5.0 W NORMAL / 17.9 W WORST                       | in: 3.8 W NORMAL D-A / 10.1 W WORST D-W
   v                                                       v
 Raspberry Pi 5 (EEPROM PSU_MAX_CURRENT=5000)        Display controller (Beck BTC-mini-eDP: 12 V, 1.1-1.3 W)
   |- USB budget 1.6 A: keyboard, trackpad                 '- eDP panel (3.3 V logic + integrated LED driver)
   |- fan header (Active Cooler; shares USB limit)        (location lid/base TBD: dossier EP-C02)
   |- 3.3 V GPIO: GNSS Flex pHAT (18-26 mA, 100 mA inrush)
   '- PCIe FPC -> M.2 HAT+ (<= 3 A to the device) -> NVMe
 [optional, TBD] fused aux 5 V from SYS for an enclosure fan / future peripherals (not through the Pi USB budget)
```

| Rail | Voltage | Continuous (NORMAL / WORST) | Peak / design rating | Headroom | Efficiency (ASSUMED) |
|---|---|---|---|---|---|
| Battery / SYS bus | 12.0–16.8 V (cutoff 12.8 V; BMS floor 11.2 V) | 0.62 A / 2.6 A | charge ≤ 5 A; charger discharge limit 6 A continuous | ≥ 2.3× | — |
| 5.1 V | 5.1 V (Pi asks for "5.1 V supply", MFR) | 0.9 A / 3.2 A (+ USB within 1.6 A budget) | **5 A** (Pi 5 full capability) | 5.5 A-class part: ~10 %. **Choose a ≥ 6 A-class part or verify thermal derating at 12–16.8 V in** | 0.90 |
| 12 V | 12 V ±5 % (11.4–12.6, Beck MFR) | 0.28 A (D-A mid) / 0.74 A (D-W full) | ≈ 1 A | 2 A part: ≥ 2.7× | 0.88 |
| 3.3 V | **No dedicated rail.** GNSS and NVMe 3.3 V come from the Pi / HAT+ | — | — | — | — |

## 6. Charger topology

**BASELINE:** an NVDC buck-boost charger with integrated power path, dual-input selector and VOC-MPPT. **TI BQ25798** is the reference candidate (MFR, SLUSDV2C rev. June 2026).

| Requirement | BQ25798 (MFR) | Fit for NOMAD |
|---|---|---|
| 4S charge voltage | VBAT ≤ 18.8 V; 4S VREG range 14–18.8 V, default 16.8 V | yes |
| Input range | VBUS 3.6–24 V; VAC / VBUS absolute max 30 V | PD 5–20 V and P108 Voc ≤ ~23 V (cold, ASSUMED −0.3 %/K): yes |
| Input current | ≤ 3.3 A (IINDPM 0.1–3.3 A) | caps useful PD at ≈ 66 W |
| Charge current | ≤ 5 A | baseline 3.2 A (~0.5C) |
| Battery discharge (system from battery) | 6 A RMS continuous, 10 A peak (1 s), OCP 9.3 A | 4S worst 2.6 A: yes |
| Power path | NVDC; system kept ≥ VSYSMIN (4S default 12 V); battery supplement when load > input | charge while running: yes |
| Dual input | VAC1 / VAC2 with back-to-back FETs; **one input at a time**, first valid wins, host can swap over I²C; inputs are never summed | USB-C + solar: yes, not simultaneously |
| MPPT | VOC sampling; VINDPM = VOC_PCT × VOC (0.5625–1.0); **disabled at power-on; needs a host write** | host-dependent (§8) |
| Host independence | Default mode charges autonomously (PROG pin: 4S, 1 A, 16.8 V); the host can disable the watchdog so settings persist while the battery is connected | works with the Pi off, after one configuration |
| Efficiency | 96.5 % at 16 V / 3 A from 20 V | 4S sits exactly here |
| Price | US$5.20 (qty 1), DigiKey 2026-10-02 | — |

**Exact charger PCB: TBD.** A custom board is assumed (§11); EVM boards are not sized.

## 7. USB-C PD

| PD contract | Usable input (≤ 3.3 A) | Charge power while NORMAL / WORST | Charge current (NORMAL) | 0 → 90 % usable while NORMAL (CC only) |
|---|---|---|---|---|
| 15 V 3 A (45 W) | 45 W | 34.6 / 15.4 W | 2.2 A | 2.2 h |
| 20 V 2.25 A (45 W) | 45 W | 34.6 / 15.4 W | 2.2 A | 2.2 h |
| **20 V 3 A (60 W)** | 60 W | **49.0 / 29.9 W** | **3.2 A** | **1.5 h** |
| 20 V 3.25 A (65 W) | 65 W | 53.9 / 34.7 W | 3.2 A (capped) | 1.5 h |
| 20 V 5 A (100 W) | **66 W (charger input cap)** | 54.8 / 35.7 W | 3.2 A | 1.5 h. **No benefit; needs an e-marked 5 A cable** |
| 5 V 3 A (non-PD fallback) | 15 W | 4.6 W while NORMAL; battery assists at WORST | — | slow |

**BASELINE:**
- **Request 20 V 3 A (60 W) as the preferred contract.** The **minimum** is 45 W (15 V 3 A or 20 V 2.25 A): it still charges at about 2.2 A while running NORMAL, and still charges at WORST.
- **A higher PD contract is not worthwhile:** the charger input is capped at 3.3 A, and 5 A cables add cost and heat.
- **Connector:** a standard 3 A-rated USB-C receptacle is sufficient. The GCT USB4105-GF-A (US$0.80, DigiKey) is an example; **its current rating is still to be verified**.
- **PD controller:**
  - **TPS25751-class** (US$2.99) can set the charger's input current from the negotiated contract over I²C (MFR: compatible with BQ25798).
  - **TPS25730-class** (US$3.04) is strap-configured and standalone.
  - Choice **TBD**.
- **Thermal:** charging at 60 W while NORMAL adds about 2.1 W of charger loss plus 1.4 W of cell / path I²R (§10).

### 7.4 DC barrel input

**Not recommended for V1.** The charger has two inputs and both are used (USB-C + solar). A barrel input would need external OR-ing (dossier EP-C19), an extra connector and an extra protection path. USB-C PD already accepts 5–20 V from laptop adapters, power banks and 12 V vehicle USB-C adapters (INFERRED). You may still choose to keep it.

## 8. Solar (P108) integration

- **Electrical:**
  - Voc 20.45 V and Vmp 17.34 V at STC; Imp 0.57 A (MFR).
  - **Voc is about 23 V at −20 °C** (ASSUMED −0.30 %/K; Voltaic publishes no coefficient). That is below the 26 V OVP setting (25.2 V minimum) and the 30 V absolute maximum.
  - Hot Vmp is about 16.1 V (INFERRED from Voltaic data), so **buck-boost is required near full 4S charge**, which the BQ25798 provides.
- **MPPT:** BQ25798 VOC sampling on VAC2. VOC_PCT 0.8125 (≈ 16.6 V) or 0.875 (≈ 17.9 V) brackets the STC Vmp / Voc ratio of 0.848. **The choice is PROVISIONAL and needs measurement.**
- **Direct connection to the battery or system: no.** Solar always goes through the charger. The battery stays the buffer, and the solar leaf never powers the system directly.
- **Charging while running:** yes, through the NVDC path, when USB-C is absent.
- **USB-C and solar together:** **not simultaneously.**
  - **Recommended priority:** USB-C first when present, solar otherwise. The charger keeps the first valid input, so the host (Pi or the PD controller) must enforce USB-C priority over I²C.
  - Solar energy is wasted while USB-C is connected. That is acceptable, because USB-C is the larger source.
- **Host dependence:** MPPT needs one I²C configuration (Pi when running), with the watchdog disabled so it persists while the battery is connected. **After the battery is removed, defaults return** (1 A charging, MPPT off). Solar behaviour without MPPT is **UNKNOWN**, and validation is required.
- **Input protection:**
  - a reverse-polarity ideal-diode FET (Schottky alternative: ≈ 0.23 W loss)
  - a TVS on the 0.85 m panel lead
  - a keyed connector
  - VAC OVP set to 26 V
- **Damage under realistic faults** (INFERRED from MFR ratings):
  - The panel is current-limited (≈ 0.6 A) and stays below 30 V even when cold.
  - A shorted panel is harmless.
  - Backfeed into the panel is blocked by the back-to-back FETs.
  - **Residual risks:** reverse polarity without the protection FET, and lightning / ESD on the long lead.
- **Yield:** unchanged from the dossier: ≈ 48 / 36 / 16 / 5 Wh per day into the battery (summer median / annual mean / winter median / poor winter).

## 9. BMS and protection (requirements; SKU TBD)

| Function | Requirement | Reference implementation (not selected) |
|---|---|---|
| Overcharge | cell OV 4.25–4.30 V, above the charger setpoint (16.8 V / 4.20 V per cell) | BQ7791501: OV 4.25 V. (BQ7791500's 4.20 V OV would require a lower charge voltage) |
| Overdischarge | cell UV 2.8–3.0 V (hardware); **system cutoff 3.2 V/cell (12.8 V) in software** | BQ7791501: UV 2.8 V |
| Over-current, discharge | trip ≥ 2× max continuous (≥ 5–6 A), ≤ cell limit | Thresholds are voltages across Rsense (OCD1 35 / OCD2 60 mV). Rsense 3–5 mΩ gives 7–12 A / 12–20 A (CALC; Rsense TBD) |
| Over-current, charge | trip > 5 A (charger max) | OCC 20 mV → Rsense ≤ 3 mΩ (6.7 A) |
| Short circuit | fast trip (< 1 ms) well below 119 A prospective | SCD 120 mV, 0.96 ms → 24–40 A at 5–3 mΩ |
| Balancing | passive, all 4 cells; cells matched at assembly | 50 mA integrated |
| Temperature (BMS) | NTC on the cells; charge inhibit outside **0–45 °C** (covers both cell options and the hot-enclosure case); discharge 65–70 °C / −10…−20 °C | BQ7791501: OTC 50 / UTC 0 / OTD 70 / UTD −20 °C. The 45 °C requirement needs the charger JEITA window or a different variant (TBD) |
| Temperature (charger) | JEITA charge control from the pack NTC via the charger TS pin | BQ25798 JEITA (MFR) |
| Pack fuse | 10 A rating (≥ 2× the 5 A charge current), **≥ 32 V DC, ≥ 1 kA breaking**, replaceable | Littelfuse MINI 0297010.WXNV: 10 A, 32 V DC, 1 kA, 7.42 mΩ, US$0.39. **Rejected:** NANO2 0451 (50 A breaking capacity < 119 A prospective) |
| Secondary overvoltage | independent second protector recommended | part **TBD** |
| Service disconnect | the **BMS lives on the pack**, so a removed pack is self-protected. Keyed, latching pack connector (≥ 5 A per power contact) with P+, P− and NTC; plus the battery door | e.g. Molex Micro-Fit 3.0 (housing 0436450200, US$0.39); connector **TBD** |
| Storage / ship | charger ship-FET mode; Pi `POWER_OFF_ON_HALT=1` (≈ 0.01 W off) | MFR |
| State of charge | charger 16-bit ADC (VBAT, IBAT) for software gauging; a dedicated fuel gauge is optional | TBD |

## 10. Thermal interaction (power to heat, CALC)

| State | 5 V buck heat | 12 V buck-boost heat | Charger heat | Pack + path I²R | **Total power-electronics + pack heat** |
|---|---:|---:|---:|---:|---:|
| NORMAL D-A | 0.50 | 0.45 | 0 | 0.05 | **1.07 W** |
| NORMAL D-W | 0.50 | 0.69 | 0 | 0.08 | 1.33 W |
| HIGH D-A | 1.29 | 0.62 | 0 | 0.23 | 2.21 W |
| WORST D-W | 1.79 | 1.21 | 0 | 0.56 | **3.62 W** |
| NORMAL + charging at 60 W | 0.50 | 0.45 | 2.10 | 1.42 | **4.53 W** |
| NORMAL + charging at 45 W | 0.50 | 0.45 | 1.58 | 0.71 | 3.30 W |
| WORST + charging at 60 W | 1.79 | 1.21 | 2.10 | 0.53 | **5.69 W** |

**Verdict:** the electrical architecture adds **≈ 1 W at NORMAL and ≤ 6 W in the worst combined case.** That is small next to the 4–18 W of base heat from the loads (dossier §13), so there is **no obviously unacceptable burden.** Caveats:
- The charger (≈ 2 W while charging) should sit away from the battery, because of the 0–45 °C charge window.
- The 5 V buck runs at ≈ 1.8 W in WORST and needs copper or airflow.
- The HAT+ 50 °C internal-air limit (dossier EP-C12) is unchanged by this architecture.
- **Thermal behaviour is not physically validated.**

## 11. Physical fit

### 11.1 Battery bay (90 × 82 × 30)

Build allowances (ASSUMED):
- **Tight:** cell wraps + fish paper + 0.6 mm outer insulation; 1.7 mm per end for strips; 4 mm for lead egress; 5 mm BMS on top.
- **Holder:** 1.0 mm ribs, 1.2 mm walls.

| Pack build | M65A | 50E |
|---|---|---|
| **Tight (cells bonded)** | 87.4 × 77.6 × 27.8 → spare +2.6 / +4.4 / +2.2 → **fits, tight (1.3 mm per side across the width)** | 86.2 × 78.2 × 27.4 → fits, tight |
| **Holder (ribs)** | 91.6 × 80.0 × 28.9 → **does NOT fit** (−1.6 mm width). Needs **≈ 93.6 × 82 × 31** | 90.4 × 80.6 × 28.6 → does not fit. Needs ≈ 92.4 × 82.6 × 31 |

**Consequence:** the 4S1P baseline fits the current reserve **only as a tightly bonded pack** (cells are not individually replaceable; the pack is replaced as a unit). A serviceable holder-type pack requires a bay change of about **+3.6 mm in width and +1 mm in height**. That is an owner decision for D-007 and the YAML re-baseline. **`nomad.yaml` is not changed here.**

### 11.2 Power electronics (90 × 45 × 20)

EST areas:

| Item | Size | Area |
|---|---|---|
| Charger board | 35 × 30 × 7 | 1050 mm² |
| 12 V buck-boost | 43 × 21 × 10 (MFR size) | 903 mm² |
| Fuse holder | 20 × 10 × 12 | 200 mm² |
| Solar input protection | 20 × 15 × 8 | 300 mm² |
| Harness landing | 15 × 15 × 8 | 225 mm² |
| **Total** | tallest 12 mm (≤ 20 mm) | **≈ 2 678 mm² = 66 % of 4 050 mm²** |

- **Plausible fit with a custom charger board.** Off-the-shelf MPPT modules do not fit (dossier EP-C15).
- **Not in this reserve:**
  - the 5 V buck (25.4 × 25.4 × 9.5), which goes in the compute-power reserve 50 × 30 × 15 (fits)
  - the BMS, which sits on the pack
  - the PD controller, which sits beside the USB-C receptacle on the rear port panel

## 12. Runtime model (baseline 4S1P)

The model applies conversion efficiencies, quiescent draw (0.06 W) and pack and path I²R. Usable energy is nominal × 0.90, and end of life is × 0.80. "Meets" means usable at end of life ≥ needed × 1.10.

**Display D-A:**

| Case | Load W | Battery-side W | Losses W | Needed Wh | M65A runtime new / EOL | Meets (M65A / 50E) |
|---|---:|---:|---:|---:|---|---|
| Normal 4 h | 7.84 | 8.91 | 1.07 | 35.6 | 9.3 / 7.4 h | yes / yes |
| **Normal 6 h** | 7.84 | 8.91 | 1.07 | 53.4 | 9.3 / 7.4 h | **yes / no** (50E: 7.2 / 5.8 h) |
| Normal 8 h (reference) | 7.84 | 8.91 | 1.07 | 71.3 | 9.3 / 7.4 h | no / no |
| High sustained 15 min / 1 h | 16.21 | 18.41 | 2.21 | 4.6 / 18.4 | 4.5 / 3.6 h | yes / yes |
| High sustained 4 h (reference) | 16.21 | 18.41 | 2.21 | 73.7 | 4.5 / 3.6 h | no / no |
| Worst 15 min / 1 h | 20.83 | 23.70 | 2.88 | 5.9 / 23.7 | 3.5 / 2.8 h | yes / yes |

**Display D-W:**

| Case | Load W | Battery-side W | Losses W | Needed Wh | M65A runtime new / EOL | Meets (M65A / 50E) |
|---|---:|---:|---:|---:|---|---|
| Normal 4 h | 9.55 | 10.88 | 1.33 | 43.5 | 7.6 / 6.1 h | yes / yes |
| **Normal 6 h** | 9.55 | 10.88 | 1.33 | 65.3 | 7.6 / 6.1 h | **no / no** (6.1 h at EOL, but not with the 10 % reserve) |
| High sustained 1 h / 4 h | 19.98 | 22.83 | 2.85 | 22.8 / 91.3 | 3.6 / 2.9 h | yes / no |

**Result:**

| Combination | 6 h target with reserve | 4 h minimum |
|---|---|---|
| D-A + M65A | met | met |
| D-A + 50E | not met | met |
| D-W + either cell | not met | met |

## 13. Planning-level cost

One unit, 2026-10-02, not a BOM, nothing ordered.

| Item | Price | Source |
|---|---:|---|
| 4 × Molicel M65A | €9.75 each (≈ US$45.6 total, FX ASSUMED) | NKON (NL) https://www.nkon.nl/en/rechargeable/li-ion/21700-20700-size.html |
| BQ25798RQMR charger IC | US$5.20 (qty 1), US$3.96 (qty 10) | DigiKey https://www.digikey.com/en/products/result?keywords=BQ25798RQMR |
| TPS25751DREFR PD controller | US$2.99 | DigiKey https://www.digikey.com/en/products/result?keywords=TPS25751DREFR |
| TPS25730DREFR (alternative) | US$3.04 | DigiKey https://www.digikey.com/en/products/result?keywords=TPS25730DREFR |
| BQ7791501PWR protector | US$2.05 | DigiKey https://www.digikey.com/en/products/result?keywords=BQ7791500PWR |
| Littelfuse 0297010.WXNV MINI 10 A fuse | US$0.39 (+ holder EST US$1–3) | DigiKey https://www.digikey.com/en/products/result?keywords=0297010.WXNV |
| GCT USB4105-GF-A USB-C receptacle | US$0.80 | DigiKey https://www.digikey.com/en/products/result?keywords=USB4105-GF-A |
| Molex Micro-Fit 3.0 2-pos housing 0436450200 | US$0.39 (+ contacts / header EST US$2) | DigiKey https://www.digikey.com/en/products/result?keywords=0436450200 |
| Pololu D36V50F5 (5 V 5.5 A) | US$39.95 | https://www.pololu.com/product/4091 |
| Pololu S18V20F12 (12 V buck-boost) | US$29.95 | https://www.pololu.com/product/2577 |
| Passives, FETs, inductor, NTC, PCB, nickel strip, insulation, wire | EST ≈ US$40 | not sourced |
| **Total** | **≈ US$167**, excluding the P108 (US$45, out of stock), shipping and import VAT | — |

Custom regulator designs would cost less than the Pololu modules (not quantified).

## 14. Risks and conflicts (E2-R)

| ID | Risk / conflict | Severity | Next step |
|---|---|---|---|
| E2-R01 | **The 6 h target depends on the M65A**, whose datasheet is v0.1 preliminary: cycle life unstated, single new cell. A mature 71 Wh cell gives 5.8 h at end of life | High | Owner decision (§15); obtain the final datasheet |
| E2-R02 | **The pack fits the bay only as a tightly bonded pack;** a holder pack needs ≈ 93.6 × 82 × 31 | High | Owner decision; D-007 / YAML step 7 |
| E2-R03 | **5.1 V delivery at 5 A:** the Pololu D36V50F5 is 5.0 V ±4 % and 5.5 A typical, depending on input voltage; harness drop is unverified | Medium | Choose a 5.1 V / ≥ 6 A part or remote sense; measure |
| E2-R04 | **MPPT and source priority are host-dependent** (I²C); defaults return after battery removal | Medium | Configure at boot; validate solar behaviour without the host |
| E2-R05 | **USB-C and solar can't be summed;** solar is idle while USB-C is present | Low (accepted) | — |
| E2-R06 | **BMS temperature window:** BQ7791501 OTC 50 °C vs the 45 °C requirement; charger JEITA must enforce 45 °C | Medium | Choose the variant or JEITA setting |
| E2-R07 | **Peripheral loads are unpublished** (HID, Active Cooler, HAT+, SSD); NORMAL uses manufacturer "typical" Pi power, not a NOMAD workload | Medium | Measure at the purchasing gate |
| E2-R08 | **P108 Voc temperature coefficient is unpublished;** cold Voc ≈ 23 V is ASSUMED; the OVP margin is 2.2 V minimum | Low | Confirm with Voltaic / measure |
| E2-R09 | **Where the 12 V rail and controller live** (lid vs base) is unresolved (EP-C02); it affects the hinge pass | Medium | Lid / hinge phase |
| E2-R10 | **D-W misses 6 h at end of life with reserve** | Medium | Display decision |
| E2-R11 | **The Active Cooler is "candidate" in the repo but "selected" in the owner brief** | Low | Owner to confirm; repository not changed |
| E2-R12 | **Battery safety, charging and thermal are not physically validated** | — | Staged validation (dependency step 13) |
| E2-R13 | **`docs/VALIDATION_STATUS.md` does not exist** (the only validation-status file is `prototypes/B1_SB261/VALIDATION_STATUS.md`); this document's §16 records power validation status | Info | — |

## 15. Decisions that need the owner

1. **Cell basis for the baseline pack.**
   - M65A-class (preliminary): **meets 6 h with reserve**.
   - Mature 50E-class: **meets 4 h, about 5.8 h at end of life**.
2. **Battery bay.**
   - Accept a tightly bonded, non-cell-serviceable pack within 90 × 82 × 30.
   - Or allow the bay to grow to about 93.6 × 82 × 31 for a holder-type pack (D-007 / YAML step 7).
3. **Display direction** (unchanged from the dossier). D-W does not meet 6 h at end of life with reserve.
4. **Confirm USB-C PD only** (no DC barrel), and the 60 W preferred / 45 W minimum input profile.

## 16. Validation status (power)

| Item | Status |
|---|---|
| Architecture, currents, energies, heat | CALC (this document); **not measured** |
| Component limits | MFR datasheets (BQ25798, BQ77915, TPS25751 / TPS25730, Littelfuse MINI, Molicel, Samsung) |
| Battery safety, charging behaviour, MPPT behaviour, thermal | **VALIDATION REQUIRED** (physical) |
| Pack fit | CALC with ASSUMED build allowances; **physical mock-up required** |

## 17. Sources (accessed 2026-10-02)

| Source | Link |
|---|---|
| TI BQ25798 datasheet SLUSDV2C (rev. June 2026) | https://www.ti.com/lit/ds/symlink/bq25798.pdf |
| TI BQ77915 datasheet | https://www.ti.com/lit/ds/symlink/bq77915.pdf |
| TI TPS25751 | https://www.ti.com/product/TPS25751 |
| TI TPS25730 | https://www.ti.com/product/TPS25730 |
| Littelfuse MINI 0297010.WXNV (DigiKey) | https://www.digikey.com/en/products/result?keywords=0297010.WXNV |
| Littelfuse 0451007.MRL (DigiKey) | https://www.digikey.com/en/products/result?keywords=0451007.MRL |
| DigiKey price pages | as in §13 |
| Pololu | https://www.pololu.com/product/4091, https://www.pololu.com/product/2577 |
| Dossier sources | `docs/E-POWER-RESEARCH-CAMPAIGN.md` §21 |

**Access notes:**
- Mouser ("access denied" to automation) and TME (Cloudflare check) were not bypassed.
- TI's own pages do not show prices without a session.
