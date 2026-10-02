# E-POWER Research Campaign — NOMAD V1 energy, power, battery, charging, solar and thermal

**Date:** 2026-10-02. **Status: research dossier only.** Nothing here is selected, frozen, ordered or physically tested.

- **Builds on:** E-POWER-001 (`prototypes/V1/E-POWER-001_hardware_energy_characterization.md`, commit `40f3d28`).
- **Covers:** the remaining V1 energy chain that E-POWER-002 … E-POWER-007 would have covered.
- **Owner-decision boundary:** the runtime target and the normal display brightness are **owner decisions**. They are modelled here as scenarios only. No candidate is selected.
- **Calculator:** every derived number comes from `prototypes/V1/epower_campaign_calc.py`. It is standard library only; run it with `py prototypes/V1/epower_campaign_calc.py`.
- **Unchanged by this campaign:** `nomad.yaml`, CAD, Onshape and the authoritative requirements.

**Evidence labels:**

| Label | Meaning |
|---|---|
| **MFR** | Manufacturer datasheet, product page or official documentation |
| **3P** | Named independent measurement |
| **3P-SEC** | Secondary third-party claim with unclear method (lowest weight) |
| **PVGIS** | EU JRC PVGIS 5.3 model |
| **REPO** | Existing NOMAD record |
| **CALC** | Arithmetic on labelled inputs |
| **ASSUMED** | A stated scenario assumption |
| **UNKNOWN** | Not published or not verifiable |

Source tags such as [R1] refer to §21.

---

## 1. Executive summary

1. **The display choice now dominates the energy story more than any battery choice.** Two documented display systems bracket the problem:
   - **D-A: AUO B101UAN01 eDP panel + Beck BTC-mini-eDP**
     - 2.7 / 3.3 / 4.6 W at low / mid / full brightness, including the controller [D2][C1] (CALC).
     - Meets the ≤ 6 W target.
     - But it is **glossy**, has 380 cd/m² typical (sibling .7 spec; .C listed at 400 by a third party), and is rated 0–60 °C (.7 manufacturer spec; .C listed at 0–50 °C by a third party).
   - **D-W: Winstar WF101NTYA4LNN0 LVDS panel + Beck BTC-mini + an LED driver**
     - 3.4 / 5.0 / 8.4 W [D1][C2] (CALC; LED-driver efficiency ASSUMED).
     - Matte, 500 cd/m², −20 to +70 °C, but **exceeds ≤ 6 W at full brightness**.
   - **No documented panel meets every display target at once** (≥ 400 nit, matte, ≤ 6 W).
2. **Whole-system battery-side load** (published data + stated assumptions, conversion included):

   | Scenario | D-A | D-W |
   |---|---|---|
   | LOW | 6.9 W | 7.6 W |
   | NORMAL | 8.7 W | 10.6 W |
   | HIGH | 18.0 W | 22.1 W |
   | WORST | 23.1 W | 27.6 W |

   The Pi is 3.2 W idle to 9.8 W under stress (3P), and 4.0 W "typical active" (MFR).
3. **The reserved battery bay (90 × 82 × 30) holds one flat layer of four 21700 cells**, i.e. at most:
   - **71 Wh** with a mature cell (Samsung 50E)
   - **92 Wh** with the new Molicel M65A (datasheet v0.1, preliminary; 0.8 mm side clearance, marginal)

   A second layer needs a 47 mm-tall bay, which exceeds the 40 mm working body height.
4. **Runtime the bay supports** (battery-only, CALC, before the 10 % reserve):

   | Pack | NORMAL D-A, new | NORMAL D-A, end of life | HIGH D-A, new | HIGH D-A, end of life |
   |---|---|---|---|---|
   | 92 Wh M65A | 9.5 h | 7.6 h | 4.6 h | 3.7 h |
   | 71 Wh 50E | 7.3 h | 5.9 h | 3.6 h | 2.8 h |

   **NORMAL-load runtimes of 4–6 h fit the bay. 8 h at NORMAL load, or any HIGH-load target, does not.**
5. **Above 100 Wh needs airline approval** (IATA 2026 [B7]). HIGH-load 4 h already needs 110–135 Wh of design capacity.
6. **Solar** (P108, Sofia, PVGIS 2018–2023 hourly, 85 % charge chain ASSUMED), into the battery per day:

   | Condition | Wh/day | Share of a NORMAL 6 h day (D-A, 52 Wh) |
   |---|---|---|
   | Summer median, panel out all day at 35° south | ≈ 48 | ≈ 91 % |
   | Annual mean | ≈ 36 | ≈ 68 % |
   | Winter median | ≈ 16 | ≈ 30 % |
   | Winter worst-decile days | ≈ 5 | ≈ 10 % |

   **Solar is significant in summer, useful in winter, and marginal on bad winter days.** It never carries the instantaneous load: the P108's 9.92 W peak is below every load state.
7. **Electrical compatibility:** P108 Vmp is 17.34 V at STC and about 16 V hot (inferred from Voltaic's own temperature data). **A buck-only MPPT cannot fully charge a 4S Li-ion pack (16.8 V) from the P108 when hot.**
   - 3S Li-ion, 2S, 1S and 4S LiFePO4 are workable with buck chargers.
   - Buck-boost chargers (TI BQ25798, ADI LT8491) work with every option.
8. **Thermal:**
   - Base heat is 4–18 W across states. Exchanging 13 W (HIGH) at a 10 K internal rise needs about 2.4 CFM of effective airflow, above the Active Cooler's 1.09 CFM free-air rating.
   - **The M.2 HAT+ is rated 0–50 °C ambient** [R5], so the internal air limit sets an outside-ambient ceiling of about 35–40 °C.
   - Charging adds about 2.4 W at 60 W input. The P108 turns about 46 W of sunlight into heat at the leaf.
9. **Mass:**
   - A 4–6 h NORMAL battery (53–80 Wh) is 0.25–0.42 kg, close to the Phase 2 0.26 kg placeholder.
   - HIGH-load 6–8 h (165–220 Wh) is 0.72–1.08 kg, pushing NOMAD to about 3.1–3.4 kg (CALC).
10. **Architecture:** with the efficiencies assumed here, the candidate power architectures differ by only about ±5 % in battery-side power.
    - What separates them is peak current: a 1S pack draws about 9 A at 27.6 W near empty, versus 2.3 A for 4S.
    - Rail compatibility also separates them: the eDP controller needs a regulated 12 V ±5 %, and the Pi needs 5.1 V / 5 A with `PSU_MAX_CURRENT=5000` [R2].

**Owner decisions required** (§19): runtime target, normal display brightness, the display trade (D-A vs D-W), the battery energy and size ceiling (including the 100 Wh air-travel line), how much solar matters, and the external charging input.

---

## 2. Current NOMAD power architecture (repository state at `40f3d28`)

- **Architecture:** B1 (D-010). D-007 (base placement) is still **proposed**.
- **Reservations** (`nomad.yaml` working values, Round C, all TBD):

  | Reserve | Size (mm) | Volume |
  |---|---|---|
  | Battery bay | 90 × 82 × 30 | 221 cm³ |
  | Power electronics | 90 × 45 × 20 | — |
  | Compute power | 50 × 30 × 15 | — |
  | Cooling duct | 84 × 20 × 31, front intake → Pi → right exhaust | — |
  | Body height | 40 (under the keyboard 26.5 free, REPO) | — |

- **Mass:** 2.62 kg total (D-010 Phase 2, CALC from EST), including a 0.26 kg battery placeholder, 0.08 kg power electronics and 0.03 kg compute power.
- **Principle** (`docs/power.md`, SYS-10): solar is field energy replenishment, not the primary source.
- **Open from E-POWER-001:** C1–C14 (display power and size, controller, keyboard thickness, trackpad availability, GNSS antenna, HAT+ 50 °C, Pi off-state drain, 5 A rail).

## 3. Load characterization

### 3.1 Raspberry Pi 5 8 GB: board versus system

| State | Value (W) | Label | Notes |
|---|---:|---|---|
| Typical bare-board active | 4.0 (0.8 A × 5.0 V) | MFR [R1] | The only manufacturer workload figure |
| Idle | 2.6 (with Active Cooler) / 2.7 (passive) | 3P Tom's [P1] | Board |
| Idle | 3.2 | 3P Geerling 2024 [P3] | 8 GB C1 |
| Idle, headless Wi-Fi / with Ethernet + USB + HDMI | 3.0 / 3.6 | 3P CNX [P2] | **Wall meter, includes adapter loss and peripherals** |
| 1080p video (Firefox / Chromium) | 5.5–6.2 / 5.7–6.8 | 3P CNX [P2] | Wall |
| CPU stress | 6.8 (cooler) / 7 (throttling, passive) | 3P Tom's [P1] | |
| CPU stress | 8.8 / 9.8 | 3P CNX wall [P2] / Geerling [P3] | |
| 4K HEVC + USB storage I/O + CPU stress | 15.9–16.8 | 3P CNX wall [P2] | Includes a USB SSD; worst documented system figure |
| CPU + GPU-heavy (no video) | **UNKNOWN** | — | No credible published figure found |
| "Off" (default) / with `POWER_OFF_ON_HALT=1` | 1–1.4 / 0.01 | MFR [R1] | Tom's measured 1.3–1.4 and 0.05 W [P1] |
| RTC wake-alarm state | ≈ 3 mA | MFR (E-POWER-001) | |
| Boot transient | **UNKNOWN** for Pi 5 | — | The docs give boot data only up to Pi 4 |

- **Board versus system:** CNX figures are wall measurements and include the USB-C adapter's loss and attached peripherals. Using them as board loads (as the HIGH scenario does) is **conservative**.
- **USB budget:** the 1.6 A downstream limit [R1] is a **limit, not a consumption**. It is not counted as load.
- **The fan header shares that USB limit** [R3].

### 3.2 Peripherals and storage

| Load | Idle | Typical | Peak / bound | Label |
|---|---:|---:|---:|---|
| Active Cooler | 0 below 50 °C SoC [R3] | UNKNOWN (MFR unpublished) | ≈ 0.5 W | 3P-SEC [P4] |
| NVMe (reference WD SN740 512 GB) | 0.0033 (PS5) | 0.05 (avg active) | 4.7 (avg max, Gen4 host) | MFR (E-POWER-001) |
| NVMe sustained I/O on Pi PCIe 2.0 x1 | — | — | 2.0 used in HIGH | ASSUMED (3P-SEC claims +1–2 W [P4]) |
| M.2 HAT+ itself | UNKNOWN | UNKNOWN | supplies ≤ 3 A to the device | MFR [R5] |
| GNSS DAN-F10N | 31 µA hardware backup / 49 µA standby | 18–21 mA tracking at 3.0 V | 22–26 mA acquisition; 100 mA inrush | MFR [G1] |
| Keyboard + trackpad (Perixx) | **UNKNOWN** | **UNKNOWN** | USB-class bound | 0.15 / 0.25 / 1.0 W ASSUMED in scenarios |
| Cirque TM040040 OEM trackpad (reference) | 1.7 mA at 3.3 V idle | 2.9 mA active | — | MFR [K2] |

### 3.3 Scenario definitions (ASSUMED combinations of the documented values)

| Scenario | Pi | NVMe | Fan | GNSS | HID | Display duty |
|---|---|---|---|---|---|---|
| LOW | idle 3.2 | 0.05 | 0 | 0.069 | 0.15 | 25 % |
| NORMAL | typical active 4.0 (MFR) | 0.05 | 0.15 | 0.069 | 0.25 | 50 % |
| HIGH | stress 8.8 (CNX wall) | 2.0 | 0.5 | 0.086 | 0.25 | 100 % |
| WORST | stress 9.8 | 4.7 (MFR bound) | 0.5 | 0.086 | 1.0 | 100 %, controller at max |

**Conversion (ASSUMED within manufacturer bands):**
- 5 V rail η 0.90 (Pololu D36V50F5: 80–95 % [V1]).
- 12 V display rail η 0.92.
- Quiescent 0.10 W for regulators (2–4 mA each [V1]) plus charger (17 µA [M1]) plus BMS (8–40 µA [M2][M3]).

### 3.4 Results: watts at the battery (CALC)

| Scenario | Base-side load | Display | Total at loads | Losses | **At battery** |
|---|---:|---:|---:|---:|---:|
| LOW, D-A | 3.47 | 2.70 | 6.16 | 0.72 | **6.88** |
| NORMAL, D-A | 4.52 | 3.32 | 7.84 | 0.89 | **8.73** |
| HIGH, D-A | 11.64 | 4.57 | 16.21 | 1.79 | **18.00** |
| WORST, D-A | 16.09 | 4.74 | 20.83 | 2.30 | **23.13** |
| LOW, D-W | 3.47 | 3.38 | 6.85 | 0.78 | **7.63** |
| NORMAL, D-W | 4.52 | 5.03 | 9.55 | 1.04 | **10.59** |
| HIGH, D-W | 11.64 | 8.35 | 19.98 | 2.12 | **22.10** |
| WORST, D-W | 16.09 | 8.88 | 24.96 | 2.66 | **27.62** |

## 4. Display research (E-POWER-002)

| | **Winstar WF101NTYA4LNN0** | **AUO B101UAN01.7 / .C** | AUO G101UAN02.0 (lead only) | Waveshare 10.1" HDMI LCD (G) |
|---|---|---|---|---|
| Resolution / active area | 1920 × 1200; 216.81 × 135.50 | 1920 × 1200; 216.81 × 135.50 | 1920 × 1200 | 1920 × 1200 |
| Outline / thickness | 231.40 × 152.3 × 9.1 max | .7: 227.72 × 147.8; 2.45 panel / 5.35 at the driver PCB. .C: 229.71 × 150.3 × 4.6 (3P) | 229.9 × 150.5 × 4.95 (3P) | not published |
| Mass | not on product page (datasheet not extractable) — UNKNOWN | .7: 140 g max; .C: 115 g max (3P) | 170 g (3P) | not published |
| Brightness | 500 cd/m² | .7: **380 typ / 323 min**; .C: 400 typ (3P) | 800 (3P) | not published |
| Surface | anti-glare | **glossy** (.C, 3P) | glossy (3P) | optical-bonded touch glass |
| Interface | 2-ch LVDS, **no controller** | eDP 2-lane (.C) / 4-lane (.7) | MIPI-DSI 4-lane | HDMI (integrated controller) |
| Logic power | 3.3 V; 1.0 W typ / 1.2 W max | .7: 0.95 W max (3.0–4.2 V) | UNKNOWN (not on the database page) | — |
| Backlight | raw LED string 26 / 29 / 33 V × 200 mA = 5.2–6.6 W; **needs an external LED driver** | integrated LED driver; **2.5 W max at 380 nit**; PWM 200 Hz–20 kHz, duty 5–100 % | UNKNOWN | 12 V / 2 A adapter |
| Temperature | operating −20…+70; storage −30…+80 °C | .7: operating 0–60; **storage −20…+60 °C** (MFR). .C: 0–50 / −20…60 °C (3P) | −10…60; storage −20…70 (3P) | — |
| LED life | 50 000 h | **12 000 h** to 50 % (.7) | 20 000 h (3P) | — |
| Source quality | MFR product page [D1] | AUO spec v0.8 for .7 [D2]; .C 3P [D3] | 3P only [D4] | MFR, incomplete [D5] |

**Brightness model:**
- **No vendor publishes a brightness-to-power curve.**
- With **PWM dimming** (both systems use PWM: AUO pin LED_PWM; Beck boards output a PWM adjust signal), average LED power at fixed LED current is proportional to duty. This is physics, not a vendor curve.
- The scenarios therefore use PWM duty 25 / 50 / 100 % (ASSUMED levels), where luminance is roughly proportional to duty.

| Display system (incl. controller) | Low 25 % | Mid 50 % | Full | Full, controller max | Luminance low / mid / full |
|---|---:|---:|---:|---:|---|
| D-A AUO + BTC-mini-eDP | 2.70 W | 3.32 W | 4.57 W | 4.74 W | 95 / 190 / 380 nit |
| D-W Winstar + BTC-mini + LED driver (η 0.85–0.90 ASSUMED) | 3.38 W | 5.03 W | 8.35 W | 8.88 W | 125 / 250 / 500 nit |

**Market observations:**
- Industrial 10.1" 1920×1200 panels are LVDS or MIPI and need a controller.
- Consumer HDMI kits rarely publish power.
- **A Pi 5 MIPI-DSI route** (no HDMI controller, saving about 1 W) exists in principle: the Pi 5 has two 4-lane MIPI transceivers [E-POWER-001 S1]. It would need panel-driver work and is a **research lead, not a candidate** (UNKNOWN effort).

## 5. Display controller research

| Controller | In → out | Supply | Power | Size / mass | Temperature | Notes | Label |
|---|---|---|---|---|---|---|---|
| **Beck BTC-mini-eDP** | HDMI 1.4a / DP 1.2 / RGB → eDP (1–2 lane, 8/10-bit) | 12 V (11.4–12.6), variant 15–30 V, Lite 10.8–13.2 | active **1.10 / 1.12 / 1.29 W**; sleep 0.13–0.16 W | 80 × 70; 9.8 mm total height; 33 g | 0–60 °C (STD) | OSD, brightness via I²C / DDC-CI; backlight supply = VDD, ≤ 2 A; eDP pre-emphasis for long cables | MFR [C1] (Rev.0, 2025-05-20) |
| **Beck BTC-mini** | HDMI 1.4a / DP / RGB → dual LVDS | Var. STD: min 10.8 V, typ 12.0 V or 13.5–32 V (Beck: "avoid permanent voltages which are others than Typ-values"); Lite-12V 10.8–13.2 V | active **0.56 / 0.72 / 1.25 W** | 80 × 70; 35 g | 0–60 °C | Panel VDD 3.3 / 5 / 12 V; backlight supply 5 / 12 / 24 V (≤ 3 A) to an **external** LED driver | MFR [C2] |
| Beck DCMR-64 | DP / DVI-I (HDMI 1.4a) / RGB → LVDS | 10.8–26.4 V | sleep 0.21; active 0.82 typ / 1.36 max W | 150 × 116; 105 g | — | Too large | MFR [C4] |
| Beck DCMR-62 | **DisplayPort only** → eDP | 12 V | 1.14–1.5 W | 90 × 70 × 9; 27 g | 0–70 °C | Needs DP input; Pi 5 is HDMI | MFR [C3] |
| TouchFly CX-2556 (RTD2556V3.1) | HDMI / DVI / VGA → eDP | 12–36 V | standby 0.25 W; **active UNKNOWN** | — | — | Reseller-grade spec | 3P-vendor [C6] |

**Measured or specified?** Beck publishes min / typ / max tables measured "at VDD 12 V, 25 °C, board only" plus "with display" currents (MFR, specified). Everything else is UNKNOWN.

**Price:** Beck prices are not published (UNKNOWN; quote required). Beck is in Nuremberg, so EU availability is likely.

**The Winstar path needs a third board:** a constant-current LED driver (26–33 V, 200 mA, PWM input). No candidate is characterized (UNKNOWN).

## 6. Compute and peripheral research

- **Pi 5 rail:**
  - "5.1V supply" [R1]; 5 A recommended; the 27 W PSU at €12.40 [PR1].
  - A non-PD internal 5 V rail is accepted at full USB budget only with EEPROM `PSU_MAX_CURRENT=5000` (Pi 5 only) [R2]. Waveshare's UPS HAT (E) documentation requires the same setting [U1].
- **Regulators:**

  | Regulator | Function | Input | Output | Efficiency | No-load Iq | Size | Price |
  |---|---|---|---|---|---|---|---|
  | Pololu D36V50F5 | 5 V buck | 5.5–50 V | 5 V ±4 %, 5.5 A | 80–95 % | 2–4 mA | 25.4 × 25.4 × 9.5 | US$39.95 |
  | Pololu D36V50F12 | 12 V buck | ≥ 13.3 V | 12 V | — | — | — | — |
  | Pololu S18V20F12 | 12 V buck-boost | 2.9–32 V | 12 V, ≈ 2 A | 80–90 % | ≈ 1 mA | 43 × 21 × 10 | US$29.95 |
  | Pololu U3V70F12 | 12 V boost | 2.9–12 V | 12 V | — | < 1 mA | 3.5 g | US$25.95 |

  All MFR [V1]. **Note:** Pololu's 5 V part is 5.0 V nominal while the Pi asks for 5.1 V. The drop at 5 A needs checking (UNKNOWN until a harness is defined).
- **Active Cooler** (MFR, E-POWER-001): 5 V PWM, 1.09 CFM, 8 000 RPM. The official blog measured Active Cooler + M.2 HAT at about 64 °C SoC under sustained stress on an open bench [R4].
- **Keyboards:**
  - Perixx manuals give PERIBOARD-416 285 × 117 × **16** mm, 332 g (the product page said 21 mm). PERIBOARD-429 is 282 × 135 × 14 mm, 332 g. PERIBOARD-414 is 311 × 135 × 18 mm, 337 g [K1].
  - **None publishes current. None meets ≤ 8 mm.**
- **Trackpads:**
  - The **PERIPAD-501 II's 86 × 75 × 13 mm is now verified** by the official Perixx manual [K1]. It is not listed in the Perixx online stores (availability UNKNOWN).
  - PERIPAD-506 is 135 × 116 × 14 mm.
  - Thin OEM alternative: Cirque TM040040 (Ø40 mm, 2.5–3.6 V, 2.9 mA active, I²C / SPI). It needs a USB-HID bridge, and usability at Ø40 mm is UNKNOWN [K2].
  - **HID power is milliwatt-class** for the sensing electronics (Cirque MFR). The Perixx devices' own consumption is UNKNOWN.
- **GNSS:**
  - The DAN-F10N is a **GNSS antenna module**: 20 × 20 mm footprint, internal L1/L5 patch. **u-blox states optimal antenna performance needs a 70 × 70 mm ground plane** [G1]; SparkFun's module board is 44.45 × 31.75 mm [G2].
  - Power is negligible (≤ 0.09 W).
  - **Suitability:** the receiver is suitable electrically. The **integrated-patch** approach is suitable only if NOMAD gives it a sky view through non-metallic material. Under the keyboard (D-007 proposal), scissor keyboards may have metal backplates (INFERRED), so an external L1/L5 active antenna (e.g. u-blox ANN-MB5, 17 mA at 5 V [G3]) would be needed.
  - Whether SparkFun routes active-antenna bias (`VCC_RF`) to its U.FL is **UNKNOWN**; check the schematic. The evidence does not prove an external antenna is required.

## 7. Battery chemistry

| | Li-ion NMC/NCA cylindrical | LiPo pouch | LiFePO4 cylindrical |
|---|---|---|---|
| Nominal / range per cell | 3.6–3.63 V; 2.5–4.2 V [B1–B4] | 3.7 V (EEMB [B6]) | 3.3 V; charge to 3.6 V [B5] |
| Cell energy density (MFR examples) | M65A 23.0–23.4 Wh, 322 Wh/kg, 943 Wh/L (v0.1, preliminary). P45B 242 Wh/kg, 643 Wh/L. 50E ≈ 17.8 Wh, 69.5 g | LP9051109: 20.35 Wh, 110 g → ≈ 185 Wh/kg, ≈ 383 Wh/L (CALC) | ANR26650M1-B: 8.25 Wh, 76 g → ≈ 109 Wh/kg (CALC) |
| Discharge capability | 50E 9.8 A; P45B 45 A; M65A 26 A continuous | 2C (EEMB) | 50 A continuous |
| Charging window | 50E **0–45 °C**; P45B / M65A **0–60 °C** | — | — |
| Discharge window | −20…60 (50E); −40…60 (Molicel) | −20…60 (EEMB) | −30…55 °C operating |
| Cycle life (MFR) | 50E ≥ 80 % after 500 cycles; M65A not stated | not stated on the EEMB product page (UNKNOWN) | > 1 000 cycles at 100 % DOD |
| Safety and thermal | Highest energy; needs a protected pack, BMS and thermal isolation | Swelling allowance and compression needed; least robust mechanically | Most thermally stable (general knowledge, not quantified here); lowest density |
| Fit in the 221 cm³ bay | **4 × 21700 → 71–92 Wh** | Stock sizes fit poorly (LP9051109 is 111 mm long: 0 fit) | 3 × 26650 → **25 Wh** |
| EU price (NKON, incl. VAT, 2026-10-02) | M65A €9.75; P45B €4.15; Samsung 50G €2.75 [PR2] | — | — |

**Consequences:**
- **LiFePO4 cannot reach any modelled scenario inside the reserved bay** (25 Wh vs 42+ Wh needed).
- **LiPo pouch** is attractive volumetrically only with custom cells (UNKNOWN availability and cost).
- **Li-ion 21700** is the only chemistry that fits the current reserve at useful energy.

## 8. Battery scenarios (design capacity)

**Method (CALC):**
- **Theoretical:** load × hours.
- **Usable needed at the battery:** watts at the battery × hours.
- **Design nominal:** usable ÷ 0.90 usable window (ASSUMED) ÷ 0.80 end of life (MFR 50E criterion).
- **Recommended:** design nominal + 10 % reserve (ASSUMED).

| Scenario | Hours | D-A design + reserve (Wh) | D-W design + reserve (Wh) | Ah at 4S 14.4 V (D-A / D-W) | Ah at 3S 10.8 V (D-A / D-W) | Ah at 1S 3.6 V (D-A / D-W) |
|---|---:|---:|---:|---|---|---|
| LOW | 4 / 6 / 8 | 42 / 63 / 84 | 47 / 70 / 93 | 2.9–5.8 / 3.2–6.5 | 3.9–7.8 / 4.3–8.6 | 11.7–23.4 / 12.9–25.9 |
| NORMAL | 4 / 6 / 8 | 53 / 80 / 107 | 65 / 97 / 129 | 3.7–7.4 / 4.5–9.0 | 4.9–9.9 / 6.0–12.0 | 14.8–29.6 / 18.0–36.0 |
| HIGH | 4 / 6 / 8 | 110 / 165 / 220 | 135 / 203 / 270 | 7.6–15.3 / 9.4–18.8 | 10.2–20.4 / 12.5–25.0 | 30.5–61.1 / 37.5–75.0 |
| WORST | 4 / 6 / 8 | 141 / 212 / 283 | 169 / 253 / 338 | 9.8–19.6 / 11.7–23.4 | 13.1–26.2 / 15.6–31.3 | 39.3–78.5 / 46.9–93.8 |

**Pack mass** (cells × 1.20 pack overhead ASSUMED):

| Scenario | 21700 M65A | 50E |
|---|---|---|
| NORMAL 4 h | 0.27 kg | 0.25 kg |
| NORMAL 6 h | 0.36 kg | 0.42 kg |
| NORMAL 8 h | 0.45 kg | 0.50 kg |
| HIGH 6 h | 0.72 kg | 0.83 kg |
| HIGH 8 h | 0.89 kg | 1.08 kg |

LiFePO4 (A123) is 2–3.5 times heavier, up to 3.0–3.7 kg for HIGH or WORST 8 h. The full tables are in the calculator output.

## 9. Battery fit and power architecture

### 9.1 Fit against the reserved bay (90 × 82 × 30)

**Allowances (ASSUMED):** 1.5 mm holder wall each side, 4 mm height for strips, insulation and a flat BMS.

| Bay content | Cells | Energy | Side spare | Verdict |
|---|---|---|---|---|
| 4 × 21700 M65A | 4 | 92 Wh | 0.8 mm | **marginal** |
| 4 × 21700 50E | 4 | 71 Wh | 2.0 mm | **fits (tight)** |
| 4 × 18650 MJ1 | 4 | 51 Wh | — | fits |
| 3 × 26650 LFP | 3 | 25 Wh | 0 mm in height | marginal |
| EEMB pouch | 0 | — | — | does not fit |

**By scenario** (D-A / D-W):

| Verdict | Scenarios |
|---|---|
| **Fits (mature cell, ≤ 71 Wh)** | LOW 4–6 h; NORMAL 4 h (both displays) |
| **Marginal (needs M65A, ≤ 92 Wh)** | LOW 8 h (D-A); NORMAL 6 h (D-A); LOW 8 h is just above for D-W (93 Wh) |
| **Does not fit** | NORMAL 8 h; NORMAL 6 h for D-W (97 Wh); every HIGH and WORST case |

- **Two 21700 layers** need a bay of 90 × 82 × 47 mm, which exceeds the 40 mm working body height. **A thicker body or a larger footprint is required.**
- **Footprint alternatives (INFERRED):**
  - Round C.1's "flat pack under the keyboard" (≈ 293 cm³, with 26.5 mm free height, which barely fits a 21700 layer at 25.6 mm).
  - A second bay (concept D).
- These are D-007 matters and are not resolved here.
- **The installed envelope is larger than bare cells:** the allowances above cover the BMS, wiring and the restraint. A cell-holder pack with a separate door also needs service clearance at the connector end (11.2 mm available at the 82 mm length).

### 9.2 Power architectures (none selected)

| | A: one 5 V rail for everything | B: separate optimized rails | C: intermediate 12 V bus | D: 1S Pi-UPS-HAT style |
|---|---|---|---|---|
| Topology | battery → 5 V; display controller via 5→12 V boost | battery → 5 V buck (Pi side) + 12 V buck-boost (display) | battery → 12 V bus → 5 V buck | 1S pack → 5 V boost (HAT) + 1S → 12 V boost |
| Battery-side W, NORMAL / HIGH (D-A, CALC) | 9.18 / 18.63 | **8.73 / 18.00** | 9.07 / 18.92 | 9.01 / 18.52 |
| Peak battery current at 27.6 W, near empty | depends on S | 2S 4.6 A, 3S 3.1 A, **4S 2.3 A** | same as B | **1S 9.2 A** |
| Strengths | fewest rails | best efficiency; each rail sized to its load. A 4S pack (12.0–16.8 V) falls partly between the BTC-mini's specified supply values, so a direct battery feed needs Beck's confirmation (UNKNOWN) | one robust bus, simple distribution | off-the-shelf boards exist (Waveshare UPS HAT (E): 1S4P 21700, 5 V 6 A, PD 3.0 40 W, fuel gauge [U1]; Geekworm X1202: 4 × 18650, 5.1 V 5 A, 6–18 V DC / 5 V 5 A USB-C [U2]) |
| Weaknesses | double conversion for the display | two converters plus wiring | double conversion for the Pi | high current, thick wiring; display 12 V boost still needed; HAT form factor fights the separate battery bay |
| Idle losses | lowest count | 2 regulators × 2–4 mA | 2 regulators | HAT quiescent UNKNOWN |

**Rail constraints found:**
- The BTC-mini-eDP needs 12 V ±5 %, so a 3S or 4S pack needs a **buck-boost** to make 12 V (S18V20F12-class). The D36V50F12 buck needs ≥ 13.3 V input.
- The Pi needs 5.1 V / 5 A with `PSU_MAX_CURRENT=5000`.

## 10. Charging (external)

**Options:**
- **USB-C PD sink** (TI TPS25730: PD 3.1 sink, 20 V / 5 A, dead-battery support, resistor-strapped, integrated power-path control [M4]). USB-IF: 100 W at 20 V with 5 A cables; PD 3.1 EPR adds 28 / 36 / 48 V up to 240 W [X1].
- **Dedicated DC barrel input**, e.g. 12–20 V (direct vehicle-12 V compatibility is INFERRED).

**Charge and operate together:**
- An NVDC power-path charger (TI BQ25798: NVDC, dual-input mux, 1–4S, 3.6–24 V in, 5 A charge, USB-PD-compatible [M1]) or ADI LTC4162 ("input current limit prioritizes system load", PowerPath [M6]) supplies the system from the input and charges with the remainder.
- **Charge time** for an 83 Wh (usable) pack at 30 / 45 / 60 W input: about 3.0 / 2.0 / 1.5 h, plus the CC-CV taper (CALC, 93 % chain ASSUMED). It is capped by charger current (BQ25798: 5 A).
- **Thermal:** at 60 W input with a 96.5 %-class charger, charging adds about 2.4 W of heat in the base (CALC).
- **Cell charge window:** 0–45 °C (50E) or 0–60 °C (Molicel). JEITA charge control is available in the BQ25798 [M1].
- **Three-source issue:** BQ25798 has two inputs (e.g. USB-C + solar). USB-C + DC barrel + solar would need external OR-ing (INFERRED).

## 11. Solar (P108)

**Inputs:** Voltaic P108, 9.92 W peak, Voc 20.45 V, Vmp 17.34 V, Imp 570 mA, 22.3 × 27.4 × 0.4 cm, 328 g [S1].
- **Stock:** "out of stock, expected back October 12th" at US$45.00 [S1].
- **Temperature:** Isc and temperature coefficients are not published. Voltaic's blog states panels "may reach 60 °C on a warm day". A sibling 6 V panel's MPP voltage falls from 5.71 V (STC) to about 5.3 V at 150 °F [S2]. Scaled to the P108 (INFERRED), Vmp ≈ 16.1 V at about 65 °C.

**Yield:** PVGIS 5.3, Sofia, SARAH3 / ERA5, c-Si, loss 0, i.e. at the panel before the charger [S3]. **PVGIS already includes temperature and real weather; peak watts are never treated as continuous.**

| Condition | Panel Wh/day | Into battery (× 0.85 chain, ASSUMED) |
|---|---:|---:|
| Ideal: user re-aims continuously (2-axis tracking), July mean | 78.1 | 66.4 |
| Good: 35° south fixed, Jun–Aug median of 2018–2023 days | 56.0 | 47.6 |
| Annual mean, 35° south | 41.9 | 35.6 |
| Winter typical: Dec–Jan median | 18.6 | 15.8 |
| Poor: Dec–Jan worst-decile days | 6.0 | 5.1 |
| Closed lid lying flat (building-integrated temperatures), December median | 10.7 | 9.1 |

- The best single hour in 2018–2023 reached 10.84 W (35°).
- The figures assume the panel is out all day. **Practical deployment windows are shorter** (a deployment fraction, owner and usage dependent).

## 12. MPPT and solar charging

| Candidate | Type | Input | Battery support | Charge current | Efficiency / quiescent | Size / mass | Price | P108 fit | Label |
|---|---|---|---|---|---|---|---|---|---|
| **TI BQ25798** (IC; EVM BQ25798EVM) | Buck-boost, VOC-sampling MPPT, dual input, NVDC | 3.6–24 V | 1–4S Li-ion / LiFePO4 | 5 A | 96.5 % (16 V / 3 A from 20 V); 17 µA battery-only | QFN 4 × 4 | EVM price UNKNOWN (login) | **all chemistries and series counts** | MFR [M1] |
| **ADI LT8491** (controller; demo DC2703A) | 4-switch buck-boost MPPT, I²C | 6–80 V | 1.3–80 V battery | external FETs | — | QFN 7 × 11 | US$15.43 at 1k | all | MFR [M5] |
| ADI LTC4162-L (+ pin-compatible LiFePO4 version) | Buck, input MPPT, PowerPath | 4.5–35 V | 1–8 Li-ion (-L); a LiFePO4 version exists | 3.2 A | — | — | US$3.81 at 1k | needs Vmp > Vbat: OK ≤ 3S; **4S Li-ion not when hot** | MFR [M6] |
| Genasun GV-5 (Li) | Buck MPPT | ≤ 27 V (Voc ≤ 22 V recommended) | 3S / 4S Li-ion, 3S / 4S LiFePO4 | 5 A | 96–99.85 %; 0.125 mA standby | 110 × 56 × 29 mm, 80 g | US$104 | 3S OK; 4S LFP marginal hot; **4S Li-ion not when hot** | MFR [M7] |
| Victron SmartSolar 75/10 | Buck MPPT | PV must exceed Vbat + 5 V to start, then Vbat + 1 V | 12 / 24 V systems | 10 A | 98 %; 10 mA self-consumption | 100 × 113 × 40 mm, 0.5 kg | UNKNOWN | oversized; 0.12 W idle | MFR [M9] |
| DFRobot DFR0535 | MPPT (OFF / 9 / 12 / 18 V setpoints) | 7–30 V | 1S Li-ion | 2 A | 78 % at 1 A (18 V in); < 3 mA | 78 × 68 mm | US$38.90 | 1S only | MFR [M8] |
| DFRobot DFR0559 | Constant-voltage MPPT | **4.5–6 V** | 1S | 0.9 A | 73 % | 33 × 63 mm | US$7.90 | **incompatible (P108 is 18 V)** | MFR [M8] |

**P108 compatibility summary** (INFERRED from MFR data):
- **Buck-only MPPT:** fine for 1S, 2S and 3S Li-ion; marginal for 4S LiFePO4 (absorption 14.4–14.6 V vs Vmp ≈ 16 V hot); **not viable for 4S Li-ion** (16.8 V).
- **Buck-boost MPPT:** any option.

## 13. Thermal

### 13.1 Heat by state (CALC)

All electrical input ends up as heat.

| State | Base heat (W) | Lid heat, D-A / D-W (W) | Airflow for ΔT 10 K | ΔT 15 K |
|---|---:|---|---:|---:|
| LOW | 4.0 | 2.9 / 3.7 | 0.74 CFM | 0.49 |
| NORMAL | 5.1 | 3.6 / 5.5 | 0.95 | 0.64 |
| HIGH | 13.0 | 5.0 / 9.1 | 2.43 | 1.62 |
| WORST | 18.0 | 5.2 / 9.7 | 3.35 | 2.23 |
| Charging at 60 W in | +2.4 | — | — | — |
| P108 in full sun | ≈ 46 at the leaf (≈ 55 W absorbed, α 0.9 ASSUMED, minus electrical output) | — | — | — |

### 13.2 What this means

- **Hot components:** the Pi SoC (throttles from 80 °C [R3]), the NVMe under sustained I/O, the regulators, the display LED driver (D-W), the charger while charging, and the P108.
- **Airflow:**
  - The Active Cooler's 1.09 CFM free-air rating moves air across the SoC but cannot alone exchange the enclosure air at HIGH load.
  - **A dedicated enclosure fan is likely needed for HIGH and WORST** (INFERRED). A Noctua NF-A4x10 5V PWM is 5.24 CFM free-air, 1.95 mm H₂O, 0.3 W [E-POWER-001 S8]. In-duct flow is lower (UNKNOWN until the duct exists).
  - NORMAL (≈ 5 W) may be manageable with passive exchange plus the Active Cooler (UNKNOWN; needs test).
- **The M.2 HAT+ 50 °C issue:**
  - The brief states "Operating temperature: 0 °C to 50 °C (ambient)" [R5]. It is an *ambient* rating, not a component-surface limit, and no absolute-maximum figure is given.
  - Inside NOMAD, "ambient" is the internal air: outside air + ΔT. A 10 K rise caps outside air at 40 °C; 15 K caps it at 35 °C.
  - The Pi (0–70 °C) and the SSD (0–70 °C) are less restrictive, so **the HAT+ sets the enclosure air limit**.
  - Forced airflow is likely necessary in hot field conditions (INFERRED).
- **Battery thermal separation is recommended** (INFERRED):
  - 50E charging stops at 45 °C; Molicel allows up to 60 °C.
  - Base heat of 5–18 W, plus charging, plus solar-heated surfaces, can push a shared compartment past 45 °C on hot days.
- **Solar heat** (D-010 Phase 2 estimates, REPO, 35 °C ambient):
  - **Panel temperature:** 66–91 °C; Voltaic says up to about 60 °C on a warm day [S2].
  - **Closed lid in sun:** display +15–22 K with the 6 mm vented gap + foil, versus +22–32 K with no gap. **The air gap plus foil materially helps (≈ 10 K).**
  - **The dark leaf is a thermal shield only relative to a dark bare lid.** A light-coloured bare lid ran cooler in Phase 2 (+8–12 K), so the leaf is not a net thermal benefit.
  - **Open lid, leaf deployed:** the leaf is held off the lid and mostly decoupled (INFERRED); the display rise was +6–9 K with foil (Phase 2).
- **Display limits under sun:**
  - The AUO .7 is rated **operating ≤ 60 °C and storage ≤ 60 °C**. Closed in the sun at 35 °C ambient (50–57 °C, EST) leaves only 3–10 K margin; at 40 °C ambient it exceeds 60 °C.
  - The Winstar (≤ 70 / 80 °C) has margin.

## 14. Mass

Compared with the 2.62 kg D-010 Phase 2 base case (CALC; placeholders from REPO).

| Item | Phase 2 placeholder | Researched value |
|---|---|---|
| Battery, NORMAL 4 / 6 / 8 h (53 / 80 / 107 Wh) | 0.26 kg | 0.25–0.27 / 0.36–0.42 / 0.45–0.50 kg → NOMAD ≈ 2.61–2.63 / 2.72–2.78 / 2.81–2.86 kg |
| Battery, HIGH 6 / 8 h (165 / 220 Wh) | 0.26 kg | 0.72–0.83 / 0.89–1.08 kg → NOMAD ≈ 3.08–3.19 / 3.25–3.44 kg |
| Display + controller | 0.15 + 0.03 kg | D-A ≈ 0.173 kg (140 g panel .7 max + 33 g Beck); D-W panel mass UNKNOWN + 35 g Beck + LED driver |
| P108 | 0.328 kg | 0.328 kg (MFR, unchanged) |
| Charger / MPPT | in 0.08 kg power electronics | IC-based board UNKNOWN (EST 10–25 g); GV-5 80 g; Victron 500 g |
| BMS | in 0.08 kg | IC-based (BQ77915-class) board UNKNOWN (EST 5–15 g) |
| Regulators | 0.03 kg (compute power) | U3V70F12 3.5 g; D36V50F5 / S18V20F12 mass not published |
| Cooling | in the Pi stack | NF-A4x10 10 g (+ duct) |

**Trade:** each +1 h at NORMAL load (D-A) costs about 13 Wh of design capacity (8.73 W ÷ 0.9 ÷ 0.8 × 1.1, CALC), i.e. about 0.06 kg of 21700 cells. At HIGH load it is about 28 Wh, i.e. 0.12 kg. Solar can replace 10–91 % of a NORMAL 6 h day depending on season and conditions (§16) at a fixed 0.33 kg panel cost, and never replaces battery capacity for continuous use.

## 15. Power-flow model (conceptual — not a design)

The example shows architecture B with a 4S Li-ion pack. Values are at the NORMAL / WORST scenarios (D-A).

```
 SOLAR  P108  Voc 20.45 V | Vmp 17.34 V STC (~16 V hot, INFERRED) | Imp 0.57 A | 9.92 Wp
   |
   v                          EXTERNAL: USB-C PD sink (TPS25730-class)  5-20 V, <=3 A (5 A e-marked), <=60-100 W
 [ CHARGER / MPPT  buck-boost, NVDC, dual input  (BQ25798-class: 1-4S, <=5 A, 96.5 % peak, 17 uA) ] <---+
   |   (power path: system runs from input when present)
   v
 [ BMS / PROTECTOR (BQ77915-class 3-5S, OV/UV/OCD/SCD/OT, 50 mA balance)  + FUSE ]  <- protection boundary
   |
 BATTERY 4S1P 21700   12.0-16.8 V   (bay max 71 Wh 50E / 92 Wh M65A)
   |   NORMAL 8.7 W -> ~0.6 A   |   WORST 27.6 W (D-W) -> 2.3 A at 12 V
   +--> 5 V / 5.5 A buck (D36V50F5-class, 80-95 %)  --> Pi 5 (5.1 V target; PSU_MAX_CURRENT=5000)
   |        NORMAL ~4.5 W (0.9 A) | WORST ~16 W (3.2 A); USB budget 1.6 A (limit, not load)
   |        +-- M.2 HAT+ (<=3 A to SSD) -- NVMe 0.05-4.7 W
   |        +-- USB: keyboard, trackpad (unpublished; mW-class sensing)
   |        +-- fan header (Active Cooler, shares USB limit)
   |        +-- GPIO 3.3 V -- GNSS pHAT (18-26 mA)
   +--> 12 V buck-boost (S18V20F12-class, 80-90 %) --> display controller (BTC-mini-eDP 12 V +-5 %, 1.1-1.3 W)
            NORMAL ~3.3 W (0.28 A) | full ~4.6 W (0.39 A)  --> eDP panel (3.3 V logic + integrated LED driver)
```

**Protection boundaries** (INFERRED, to be designed):
- Input OVP and reverse protection (PD sink / charger).
- The pack BMS and fuse.
- A per-rail current limit at each regulator (Pololu parts have over-current and over-temperature shutoff [V1]).

## 16. Solar versus battery energy balance

| Scenario (D-A) | Daily need at the battery | Ideal | Good (summer median) | Annual mean | Winter median | Poor (winter worst decile) |
|---|---:|---:|---:|---:|---:|---:|
| NORMAL 4 h | 35 Wh | 190 % | 136 % | 102 % | 45 % | 15 % |
| NORMAL 6 h | 52 Wh | 127 % | 91 % | 68 % | 30 % | 10 % |
| NORMAL 8 h | 70 Wh | 95 % | 68 % | 51 % | 23 % | 7 % |
| HIGH 4 h | 72 Wh | 92 % | 66 % | 49 % | 22 % | 7 % |
| HIGH 6 h | 108 Wh | 61 % | 44 % | 33 % | 15 % | 5 % |
| HIGH 8 h | 144 Wh | 46 % | 33 % | 25 % | 11 % | 4 % |

The table assumes the panel is out all day. **Classification thresholds defined by this study:** < 15 % negligible, 15–50 % useful, > 50 % significant.
- **NORMAL 4–6 h:** solar is **significant in summer and the annual mean**, **useful in typical winter**, and **negligible to marginal on poor winter days**.
- **HIGH 6–8 h:** solar is **useful** in summer and **negligible** on poor days.

| Recharge | Ideal | Good | Annual | Winter typical | Poor |
|---|---:|---:|---:|---:|---:|
| Solar days to replace one NORMAL 6 h day (52 Wh) | 0.8 | 1.1 | 1.5 | 3.3 | 10.3 |
| Solar days to refill a full 92 Wh bay pack (83 Wh usable) | 1.2 | 1.7 | 2.3 | 5.2 | 16.2 |
| USB-C at 30 / 45 / 60 W | 3.0 / 2.0 / 1.5 h | | | | |

**Battery-only runtime of the maximum bay packs** (CALC):

| Pack | NORMAL D-A | HIGH D-A | NORMAL D-W | HIGH D-W |
|---|---|---|---|---|
| 92 Wh (M65A), new / end of life | 9.5 / 7.6 h | 4.6 / 3.7 h | 7.8 / 6.3 h | 3.7 / 3.0 h |
| 71 Wh (50E), new / end of life | 7.3 / 5.9 h | 3.6 / 2.8 h | 6.0 / 4.8 h | 2.9 / 2.3 h |

## 17. Candidate tables

**Status key:**
- **V** = verified manufacturer data
- **C** = candidate
- **I** = inferred
- **U** = unknown

| Category | Candidate | Key data | Status |
|---|---|---|---|
| Display | Winstar WF101NTYA4LNN0 | 500 nit, matte, LVDS, 6.8 W panel at full; 231.4 × 152.3 × 9.1 | C; V (product page); mass U |
| Display | AUO B101UAN01.7 / .C | 380 / 400 nit, glossy, eDP, 3.45 W max; 140 / 115 g | C; V for .7 (AUO spec), .C 3P |
| Display | AUO G101UAN02.0 | MIPI, 800 nit, glossy, 170 g (3P); power UNKNOWN | Lead; U |
| Display | Waveshare 10.1" (G) | HDMI, touch | C; power U |
| Controller | Beck BTC-mini-eDP | HDMI → eDP, 1.12 W, 12 V ±5 %, 33 g | C; V; price U |
| Controller | Beck BTC-mini | HDMI → LVDS, 0.72 W, 12 V (or 13.5–32 V STD), 35 g | C; V; price U |
| Controller | TouchFly CX-2556 | HDMI → eDP, 12–36 V, standby 0.25 W | C; active power U |
| LED driver (D-W) | — | 26–33 V, 200 mA, PWM | U |
| Keyboard | Perixx PERIBOARD-416 / 429 / 414 / 426 / 422 / 332 / 409H | 14–21 mm thick; current not published | C; V dimensions; power U |
| Trackpad | Perixx PERIPAD-501 II | 86 × 75 × 13 (official manual); availability U | C; V |
| Trackpad | Perixx PERIPAD-506 | 135 × 116 × 14 | C; V |
| Trackpad | Cirque TM040040 (OEM) | Ø40, 2.9 mA at 3.3 V, I²C / SPI | C; V; usability U |
| Battery cell | Molicel M65A | 23.0–23.4 Wh, 74.5 g, 0–60 °C charge | C; V (preliminary v0.1); cycle life U |
| Battery cell | Samsung 50E | ≈ 17.8 Wh, 69.5 g, 0–45 °C charge, ≥ 80 % at 500 cycles | C; V |
| Battery cell | Molicel P45B | 16.2 Wh, 70 g, 45 A | C; V |
| Battery cell | LG MJ1 (18650) | 12.7 Wh, 49 g | C; V |
| Battery cell | A123 ANR26650M1-B (LFP) | 8.25 Wh, 76 g, > 1 000 cycles | C; V (does not fit the scenarios in the bay) |
| Battery cell | EEMB LP9051109 (pouch) | 20.35 Wh, 110 g, 51.5 × 111 × 9.3 | C; V (product page); does not fit the bay |
| BMS | TI BQ77915 (standalone 3–5S protector) | 8 µA, 50 mA balance, OV / UV / OCC / OCD / SCD / OT / UT | C; V (IC; board U) |
| BMS | TI BQ76920 (AFE + MCU) | 3–5S, 40 µA, I²C, integrated balancing FETs | C; V (IC; EVM BQ76920EVM) |
| BMS | JBD smart BMS | Documentation not retrievable (bot-blocked) | U |
| Regulator | Pololu D36V50F5 | 5 V, 5.5 A, 80–95 %, 2–4 mA, 25.4 × 25.4 × 9.5, US$39.95 | C; V |
| Regulator | Pololu S18V20F12 | 12 V buck-boost, 2.9–32 V, 80–90 %, 43 × 21 × 10, US$29.95 | C; V |
| Regulator | Pololu D36V50F12 / U3V70F12 / S13V20F5 | 12 V buck (≥ 13.3 V in) / 12 V boost / 5 V buck-boost 2 A | C; V |
| Charger / MPPT | TI BQ25798 | 1–4S, buck-boost, MPPT, dual input, NVDC, 5 A | C; V |
| Charger / MPPT | ADI LT8491 | Buck-boost MPPT 6–80 V | C; V |
| Charger | ADI LTC4162-L (+ LiFePO4 version) | Buck, 35 V, 3.2 A, MPPT, PowerPath | C; V |
| MPPT module | Genasun GV-5 Li | 5 A, 3S / 4S, 80 g, US$104 | C; V; fails 4S Li-ion hot (I) |
| MPPT module | Victron 75/10 | 0.5 kg, 10 mA idle | C (oversized); V |
| MPPT module | DFRobot DFR0535 / DFR0559 | 1S; DFR0559 incompatible | C / rejected; V |
| Integrated Pi power | Waveshare UPS HAT (E) | 1S4P 21700, 5 V 6 A, PD 3.0 40 W | C; V; efficiency U |
| Integrated Pi power | Geekworm X1202 | 4 × 18650, 5.1 V 5 A, 97.4 × 85 PCB, US$51 | C; V; efficiency U |
| Fan | Raspberry Pi Active Cooler | 1.09 CFM, €5.90 | C; V; power U |
| Fan | Noctua NF-A4x10 5V PWM | 0.3 W, 5.24 CFM, 10 g | C; V |
| GNSS | SparkFun Flex pHAT DAN-F10N | 18–26 mA, no GLONASS, 70 × 70 ground plane optimal | C; V |
| GNSS antenna | u-blox ANN-MB5 | 17 mA at 5 V, 49 × 46 × 16, SMA, 3 m | C; V; bias path U |
| External power | TI TPS25730 PD sink | 20 V / 5 A, PD 3.1 | C; V |
| External power | DC barrel 12–20 V | — | C; connector U |

**Prices** (research data only, 2026-10-01/02):

| Item | Price | Seller and terms |
|---|---|---|
| Pi 5 8 GB | €184.90 | BerryBase DE, incl. VAT [PR1] |
| Active Cooler | €5.90 | BerryBase DE [PR1] |
| M.2 HAT | €12.50 | BerryBase DE [PR1] |
| 27 W PSU | €12.40 | BerryBase DE [PR1] |
| Molicel M65A | €9.75 | NKON NL, incl. VAT [PR2] |
| Molicel P45B | €4.15 | NKON NL [PR2] |
| P108 | US$45.00 | US, out of stock [S1] |
| Pololu regulators | US$25.95–39.95 | US [V1] |
| GV-5 Li | US$104 | [M7] |
| Geekworm X1202 | US$51 | [U2] |
| DFR0535 | US$38.90 | [M8] |
| LT8491 | US$15.43 | 1k list [M5] |
| LTC4162-L | US$3.81 | 1k list [M6] |
| Beck controllers, TI EVMs | UNKNOWN | — |

## 18. Conflicts (EP-C, documented, not solved)

| ID | Conflict | Evidence |
|---|---|---|
| EP-C01 | **No documented display meets ≥ 400 nit + matte + ≤ 6 W together.** D-A is ≤ 6 W but glossy at 380–400 nit; D-W is matte at 500 nit but 8.4 W at full | §4 |
| EP-C02 | **The display controller (80 × 70 × 9.8 mm) exceeds the D-010 Phase 2 lid controller zone** (8 mm EST in the 19 mm B1 core) if mounted in the lid. In the base, an eDP / LVDS cable must cross the display hinge with the solar cable | [C1], REPO |
| EP-C03 | **The Winstar path needs an external LED driver** (third board, uncharacterized) | [D1][C2] |
| EP-C04 | **AUO .7 operating and storage max 60 °C** vs closed-in-sun display 50–57 °C at 35 °C ambient (EST), so it exceeds on hotter days. LED life 12 000 h | [D2], REPO |
| EP-C05 | **The battery bay holds 71 Wh (mature cell) or 92 Wh (preliminary cell) at most.** NORMAL 8 h and every HIGH-load runtime do not fit | §9 |
| EP-C06 | **A second cell layer (47 mm) exceeds the 40 mm working body height** | §9 |
| EP-C07 | **Above 100 Wh needs airline approval** (IATA). HIGH 4 h already needs 110–135 Wh design | [B7] |
| EP-C08 | **LiFePO4 cannot meet any scenario inside the bay** (25 Wh max) | §7 |
| EP-C09 | **A buck-only MPPT plus 4S Li-ion cannot fully charge from a hot P108** (Vmp ≈ 16 V < 16.8 V). Buck-boost is required, or a different series count | [S1][S2][M6][M7] |
| EP-C10 | **The eDP controller needs a regulated 12 V ±5 %; the D36V50F12 buck needs ≥ 13.3 V input.** A 3S / 4S pack needs a buck-boost 12 V stage | [C1][V1] |
| EP-C11 | **Pi 5 on an internal rail:** needs `PSU_MAX_CURRENT=5000` and 5.1 V at the board. Pololu D36V50F5 is 5.0 V ±4 %, and the harness drop at 5 A is unverified | [R1][R2][V1] |
| EP-C12 | **The M.2 HAT+ 50 °C ambient limit** sets the internal-air ceiling; outside ambient is capped at about 35–40 °C depending on internal ΔT | [R5], §13 |
| EP-C13 | **HIGH and WORST base heat (13–18 W) needs about 2.4–3.4 CFM** effective exchange at ΔT 10 K, above the Active Cooler's 1.09 CFM. An enclosure fan and duct are likely | §13 |
| EP-C14 | **Battery charge window 0–45 °C (50E) inside a 5–18 W base** with solar-heated surfaces. Thermal separation is needed; or choose a 0–60 °C cell (Molicel) | [B1–B3] |
| EP-C15 | **Off-the-shelf MPPT modules do not fit the 90 × 45 × 20 power-electronics reserve** (GV-5 110 × 56 × 29; Victron 100 × 113 × 40; DFR0535 78 × 68). An IC-based custom board would be needed (INFERRED) | [M7][M8][M9] |
| EP-C16 | **The P108 is out of stock** (single US vendor) | [S1] |
| EP-C17 | **GNSS integrated patch:** u-blox's 70 × 70 mm optimal ground plane, plus sky view, vs under-keyboard placement. External-antenna bias on the SparkFun board is UNKNOWN | [G1][G2] |
| EP-C18 | **Peripheral power is unpublished** (Perixx HID, Active Cooler, HAT+, Raspberry Pi SSD), so the scenarios rely on ASSUMED values for those lines | §3 |
| EP-C19 | **Three charge sources** (USB-C, DC barrel, solar) exceed the BQ25798's two inputs | [M1] |
| EP-C20 | **Pi-UPS-HAT (1S) style power draws about 9 A near empty at WORST load** and is a HAT form factor, which conflicts with the separate battery bay and door concept | [U1][U2] |

## 18b. Requirement conflicts (NOT applied)

| Requirement | Evidence | Conflict | Possible resolutions | Owner decision? |
|---|---|---|---|---|
| DSP-1 ≤ 6 W, ≥ 400 nit, matte | D-A 4.6 W but glossy, 380–400 nit; D-W 8.4 W at full | EP-C01 | Define ≤ 6 W at the *normal* brightness; accept glossy plus an anti-glare film; accept 380 nit; accept higher display power | **Yes** |
| KBD-1 ≤ 8 mm | All Perixx candidates 14–21 mm (manuals / product pages) | Unchanged from E-POWER-001 C4 | Uncased / OEM keyboard search; relax to the real thickness | Yes (mechanical) |
| TPD-1 86 × 75 × 13 | Verified by the official manual; availability unclear | Availability only | Confirm stock; fall back to PERIPAD-506 | No (engineering), unless 506 is chosen |
| Battery bay 90 × 82 × 30 | ≤ 71 / 92 Wh | EP-C05 / C06 | Accept a ≤ 6 h NORMAL target; grow the footprint (under-keyboard flat pack, second bay); raise the body height | **Yes** (runtime and size) |
| HAT+ thermal (CMP-3 / THM) | 0–50 °C ambient | EP-C12 | Forced airflow; thermal zoning; a different NVMe adapter (UNKNOWN candidates) | No (engineering), within the owner's ambient target (SYS-9) |
| PWR / charging (TBD) | Three sources vs two inputs | EP-C19 | USB-C + solar only; add OR-ing for DC | **Yes** (connector set) |
| GNSS placement (D-007 proposal) | Antenna module needs sky view | EP-C17 | Relocate the module; external antenna | Part of D-007 |

## 19. OWNER DECISIONS REQUIRED

1. **Runtime target.**
   - **Why it matters:** it sets battery energy, which in turn sets volume, mass, air-travel class and bay geometry (§8–9).
   - **Options and consequences:**
     - 4 h NORMAL: 53–65 Wh; fits the bay with mature cells.
     - 6 h NORMAL: 80–97 Wh; fits only with a preliminary high-density cell (D-A) or not at all (D-W).
     - 8 h NORMAL: 107–129 Wh; doesn't fit and needs airline approval.
     - A HIGH-load target at any hours: 110–270 Wh; a new bay, plus 0.2–0.8 kg.
   - **Information you need:** which workload the target applies to (NORMAL vs HIGH), and whether solar may count toward it.
2. **Normal display brightness.**
   - **Why it matters:** it sets the largest NORMAL load and decides whether ≤ 6 W is met.
   - **Options and consequences:**
     - Low (~25 % PWM): 2.7–3.4 W, about 95–125 nit.
     - Mid (~50 %): 3.3–5.0 W, about 190–250 nit.
     - Full: 4.6–8.4 W.
   - **Information you need:** the expected use (indoor, shade, direct sun) and whether ≤ 6 W applies at normal or full brightness.
3. **Display direction (EP-C01).**
   - **Why it matters:** no candidate meets every target.
   - **Options and consequences:**
     - D-A (AUO eDP + Beck BTC-mini-eDP): lowest power, but glossy, 380–400 nit and 0–60 °C.
     - D-W (Winstar LVDS + BTC-mini + LED driver): matte, 500 nit and −20…70 °C, but +3.8 W at full brightness and a third board.
     - Research the MIPI-DSI route further.
   - **Information you need:** the importance of sunlight readability versus runtime, and of the hot-storage margin.
4. **Battery energy ceiling and physical size.**
   - **Why it matters:** the bay supports ≤ 71 / 92 Wh; beyond that the body or footprint grows; above 100 Wh needs airline approval.
   - **Options:**
     - Stay ≤ 71 Wh (mature cell).
     - Go to ≤ 92 Wh (preliminary cell; marginal fit).
     - Grow the bay (under-keyboard / second bay; D-007).
     - Accept above 100 Wh.
   - **Information you need:** whether air travel matters, and the mass ceiling for NOMAD.
5. **How much solar matters** (within the replenishment principle).
   - **Why it matters:** it decides between buck-boost charge electronics (any pack) and a simpler buck charger (constrains the series count), and how much deployment the user will do.
   - **Information you need:** typical deployment hours and season; whether winter use is expected.
6. **External charging input.**
   - **Options:**
     - USB-C PD only: universal, 60–100 W.
     - USB-C + DC barrel: vehicle and bench, but needs a third input path.
   - **Consequence:** connector set, rear I/O and the charger topology.

The chemistry is not listed as an owner decision. With the current bay, only Li-ion 21700 reaches the modelled energies; LiFePO4 would require you to accept a much larger bay. If you prefer LiFePO4 for safety regardless, that becomes decision 4.

## 20. Recommended next engineering sequence (after the owner decisions)

1. Record the owner decisions (runtime, brightness, display direction, energy ceiling, solar importance, charging input).
2. **Display freeze study:** request a Beck quote and lead time; obtain the B101UAN01.C datasheet (AUO / distributor); measure brightness versus power once hardware is approved.
3. **Power architecture baseline:** pick from A–D with the decided pack series count. Size the 5 V / 12 V rails and the protection boundaries. Verify `PSU_MAX_CURRENT` and the 5.1 V delivery.
4. **Battery pack definition:** cell, series count, BMS, fuse, holder, door. Re-check the bay and D-007.
5. **Thermal architecture:** airflow path, enclosure fan, battery separation, HAT+ 50 °C strategy.
6. **YAML re-baseline** (dependency step 7): battery bay, power-electronics reserve, display stack.
7. Then the display-hinge / rear-port conflict and the integrated Virtual V1 CAD (steps 8–9).
8. **Physical measurement** at the staged purchasing gate: Pi + NVMe + display power, fan current, HID current.

## 21. Sources (retrieved 2026-10-01 / 02)

**Raspberry Pi, official:**

| Tag | Source |
|---|---|
| R1 | `power-supplies.adoc`: https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/raspberry-pi/power-supplies.adoc |
| R2 | `eeprom-bootloader.adoc` (`PSU_MAX_CURRENT`): https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/raspberry-pi/eeprom-bootloader.adoc |
| R3 | `frequency-management.adoc` (fan curve, throttling): https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/raspberry-pi/frequency-management.adoc |
| R4 | "Heating and cooling Raspberry Pi 5": https://www.raspberrypi.com/news/heating-and-cooling-raspberry-pi-5/ |
| R5 | Product briefs (Pi 5, Active Cooler, M.2 HAT+, SSD): https://datasheets.raspberrypi.com/m2-hat-plus/raspberry-pi-m2-hat-plus-product-brief.pdf (others as in E-POWER-001 S1, S7, S10) |

**Pi measurements, third-party:**

| Tag | Source |
|---|---|
| P1 | Tom's Hardware, "Raspberry Pi 5 Review": https://www.tomshardware.com/reviews/raspberry-pi-5 (3P) |
| P2 | CNX Software, Pi 5 review part 2, 2023-11-05: https://www.cnx-software.com/2023/11/05/raspberry-pi-5-review-raspberry-pi-os-bookworm-benchmarks-power-consumption/ (3P, wall meter) |
| P3 | J. Geerling, 2024-08-29: https://www.jeffgeerling.com/blog/2024/new-2gb-pi-5-has-33-smaller-die-30-idle-power-savings/ (3P) |
| P4 | raspberry.tips, Pi power 2026: https://raspberry.tips/en/raspberrypi-tutorials/raspberry-pi-power-consumption-update-2026-all-models-compared (3P-SEC) |

**Displays:**

| Tag | Source |
|---|---|
| D1 | Winstar WF101NTYA4LNN0: https://www.winstar.com.tw/products/tft-lcd/ips-tft/1920x1200-tft-lcd.html |
| D2 | AUO B101UAN01.7 Product Specification v0.8 (AUO document, hosted by a third party): https://www.beyondinfinite.com/lcd/Library/Auo/B101UAN01.7.pdf |
| D3 | AUO B101UAN01.C (3P database): https://www.twscreen.com/en/lcdpanel/17242/auo/b101uan01.c/10.1/1920x1200-Tablet-Computer-LCD-Panel |
| D4 | AUO G101UAN02.0 (3P database): https://www.twscreen.com/en/lcdpanel/15257/auo/g101uan02.0/10.1/1920x1200-Industrial-LCD-Panel |
| D5 | Waveshare 10.1inch HDMI LCD (G): https://www.waveshare.com/10.1inch-hdmi-lcd-g-with-case.htm |

**Display controllers:**

| Tag | Source |
|---|---|
| C1 | Beck BTC-mini-eDP Product Specification Rev.0: https://www.beck-elektronik.de/fileadmin/user_upload/Produkte/BECK_Elektronik/Displays/Downloads/Controller/BTC-mini-eDP_PS_full_final_Rev.0.pdf |
| C2 | Beck BTC-mini PS Rev.0: https://www.beck-elektronik.de/fileadmin/user_upload/Produkte/BECK_Elektronik/Displays/Downloads/Controller/BTC-mini_PS_full_final_Rev.0.pdf |
| C3 | Beck DCMR-62 brief and full spec: https://www.beck-elektronik.de/fileadmin/user_upload/Produkte/BECK_Elektronik/Displays/Downloads/Controller/DCMR-62_brief_Specs.pdf |
| C4 | Beck DCMR-64 PS: https://www.beck-elektronik.de/fileadmin/user_upload/Produkte/BECK_Elektronik/Displays/Downloads/Controller/DCMR-64_PS_full_final_Rev.A.pdf |
| C5 | Beck controller overview: https://www.beck-elektronik.de/en/products/displays/display-controller/ |
| C6 | TouchFly CX-2556: https://www.touchflyboard.com/pdf/CX-2556.pdf |

**Input devices:**

| Tag | Source |
|---|---|
| K1 | Perixx manuals: https://downloads.perixx.com/manuals/PERIPAD-501%20II_.pdf, …/PERIBOARD-416_.pdf, …/PERIBOARD-429_.pdf, …/PERIBOARD-414_E-Manual_compressed.pdf |
| K2 | Cirque TM040040 spec v1.1: https://static1.squarespace.com/static/53233e4be4b044fa7626c453/t/591c7ab16a4963872bf5f3ab/1495038642989/TM040040_SPI-I2C-PINNTrackpad_SPEC1-1.pdf |

**GNSS:**

| Tag | Source |
|---|---|
| G1 | u-blox DAN-F10N data sheet UBXDOC-963802114-13074 R04: https://www.u-blox.com/sites/default/files/documents/DAN-F10N_DataSheet_UBXDOC-963802114-13074.pdf |
| G2 | SparkFun DAN-F10N hardware overview: https://docs.sparkfun.com/SparkFun_GNSS_Flex_System/SparkPNT_GNSS_Flex_Module_DAN-F10N/hardware_overview/ |
| G3 | u-blox ANN-MB5 data sheet: https://www.u-blox.com/sites/default/files/documents/ANN-MB5_Datasheet_UBX-22038811.pdf |

**Regulators and Pi power boards:**

| Tag | Source |
|---|---|
| V1 | Pololu D36V50F5 https://www.pololu.com/product/4091; D36V50F12 https://www.pololu.com/product/4095; S18V20F12 https://www.pololu.com/product/2577; U3V70F12 https://www.pololu.com/product/2895; S13V20F5 https://www.pololu.com/product/4085 |
| U1 | Waveshare UPS HAT (E): https://www.waveshare.com/wiki/UPS_HAT_(E) |
| U2 | Geekworm X1202: https://geekworm.com/products/x1202 |

**Cells and transport:**

| Tag | Source |
|---|---|
| B1 | Molicel INR-21700-M65A data sheet v0.1: https://www.molicel.com/wp-content/uploads/2025-Product-Data-Sheet-of-INR-21700-M65A-80153-0.1_250620.pdf |
| B2 | Molicel P45B: https://www.molicel.com/wp-content/uploads/INR21700P45B_1.2_Product-Data-Sheet-of-INR-21700-P45B-80109.pdf |
| B3 | Samsung SDI INR21700-50E spec V1.0 (hosted on TI E2E): https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/196/INR21700_2D00_50E-Cell-Specification_5F00_V1.0_5F00_180711.pdf |
| B4 | LG INR18650 MJ1 spec (hosted): https://enerpower.de/wp-content/uploads/2016/03/Specification_INR18650MJ1.pdf |
| B5 | A123 ANR26650M1-B (hosted): https://www.batteryspace.com/prod-specs/6610.pdf |
| B6 | EEMB LP9051109: https://www.eemb.com/product-153 |
| B7 | IATA, Passengers travelling with lithium batteries, 31/03/2026: https://www.iata.org/contentassets/6fea26dd84d24b26a7a1fd5788561d6e/passengers_travelling_with_lithium_batteries.pdf |

**Chargers, protection and MPPT:**

| Tag | Source |
|---|---|
| M1 | TI BQ25798: https://www.ti.com/product/BQ25798 |
| M2 | TI BQ76920: https://www.ti.com/product/BQ76920 |
| M3 | TI BQ77915: https://www.ti.com/product/BQ77915 |
| M4 | TI TPS25730: https://www.ti.com/product/TPS25730 |
| M5 | ADI LT8491: https://www.analog.com/en/products/lt8491.html |
| M6 | ADI LTC4162-L: https://www.analog.com/en/products/ltc4162-l.html |
| M7 | Genasun GV-5 / GV-4: https://sunforgellc.com/gv-5/, https://sunforgellc.com/gv-4/ |
| M8 | DFRobot DFR0535 https://www.dfrobot.com/product-1714.html; DFR0559 https://www.dfrobot.com/product-1712.html |
| M9 | Victron SmartSolar 75/10 datasheet: https://www.victronenergy.com/upload/documents/Datasheet-SmartSolar-charge-controller-MPPT-75-10,-75-15,-100-15,-100-20-EN.pdf |
| X1 | USB-IF USB Charger (USB Power Delivery): https://www.usb.org/usb-charger-pd |

**Solar:**

| Tag | Source |
|---|---|
| S1 | Voltaic P108: https://voltaicsystems.com/9-watt-18v-panel-etfe/ |
| S2 | Voltaic blog, "How to Select MPP Voltage on a Solar Charge Controller": https://blog.voltaicsystems.com/select-mpp-voltage-solar-charge-controller/ |
| S3 | PVGIS 5.3 API, e.g. https://re.jrc.ec.europa.eu/api/v5_3/PVcalc?lat=42.698&lon=23.322&peakpower=1&loss=0&pvtechchoice=crystSi&angle=35&aspect=0&mountingplace=free&outputformat=json, `fixed=0&twoaxis=1`, and `seriescalc` 2018–2023 hourly. P108 = 9.92 Wp scaling |

**Prices:**

| Tag | Source |
|---|---|
| PR1 | BerryBase (DE): https://www.berrybase.de/en/raspberry-pi-5-8gb-ram |
| PR2 | NKON (NL), 21700 category: https://www.nkon.nl/en/rechargeable/li-ion/21700-20700-size.html |

**Source-access notes:**
- Winstar's datasheet PDF, the panelook database (CAPTCHA), Geekworm's wiki and JBD (bot checks) were not bypassed.
- analog.com PDFs timed out; ADI product pages were read in a browser.
- No search-result snippet is used as evidence. Values seen only in snippets were either verified at the source or dropped (e.g. a retailer "10 000 mAh / 50 g" LiPo listing, which is physically implausible).
