# V1 power decision: commercial Pi 5 UPS HAT vs the current architecture (2026-10-08)

**Status:** decision study. Nothing in the V1 source of truth, BOM, CAD or Onshape was changed. Scratch calculation: `usv_calc.py` (scratchpad), reading `prototypes/V1/v1_power.py` unchanged.

**Decision: OPTION A. Keep the current V1 power architecture,** and implement it from TI reference design **TIDA-050047** (USB-PD-CHG-EVM-01) rather than as a from-scratch custom board. The commercial UPS route is rejected.

## 1. The candidate: Waveshare UPS HAT (E)

It is the only mainstream Pi 5 UPS HAT built for 21700 cells; the Waveshare UPS HAT (D) is 2 × 21700 in parallel and lists only Pi 4 / 3.

| Item | Value (source: Waveshare product page + wiki, read 2026-10-08) |
|---|---|
| Model / price | Waveshare UPS HAT (E), US$32.99 (Waveshare); £31.70 (The Pi Hut) |
| Pi support | Pi 5 / 4B / 3B+, power through **pogo pins** (stacked under the Pi) |
| Cells | 4 × 21700 in **series (4S)**, not included |
| Input | USB-C PD 3.0, 5 / 9 / 12 / 15 / 20 V, ≤ 40 W, bidirectional |
| Output | 5 V, 6 A recommended continuous (10 A peak claimed); one USB-A 5 V out |
| Charger / buck ICs | **Not named**; an MCU, a fuel-gauge IC, a "fast-charging chip" and a "high-power buck" |
| Protection | "Protection circuit" mentioned. OV / UV / OC / short / temperature **not itemized**. **Balancing not stated** (the "do not mix old and new cells" warning suggests none) |
| Monitoring / shutdown | I²C (MCU + gauge). Auto-shutdown on low battery; register command to cut power. Needs Python scripts and I²C enabled |
| Size / mass | Board 56 × 88 mm, 127 g, Ø3 holes. Stack height not published |
| Solar input / MPPT | **None** |
| Pi 5 note | Needs `PSU_MAX_CURRENT=5000`; without PD the Pi is limited to 3 A |

## 2. Samsung INR21700-53G2

Source: NKON product data, 2026-10-08.
- 3.6 V nominal; 5140 mAh minimum / 5300 typical; 15.9 A discharge.
- 21.3 × 70.7 mm, 71.5 g, flat top, unprotected.
- Mature production cell (2024 batch); **€2.69 incl. VAT**.
- Charge voltage, cycle life and temperature limits: not read here; the Samsung spec PDF was blocked.

**Pack options** (Wh use the minimum capacity × 3.6 V):

| Config | Nominal V | Wh | Fits the 93.6 × 82 × 31 bay |
|---|---:|---:|---|
| 1S4P | 3.6 | 74.0 | yes |
| 2S2P | 7.2 | 74.0 | yes |
| 3S1P | 10.8 | 55.5 | yes (3 cells) |
| **4S1P** (UPS HAT (E) and V1) | 14.4 | **74.0** | yes |
| 4S1P M65A (V1) | 14.4 | 92.0 | yes |
| 4S1P 50E | 14.5 | 71.1 | yes |

## 3. Runtime: the cell decides, the board does not

Calculation inputs:
- the current V1 loads
- UPS HAT buck η 0.92 (ASSUMED)
- 5 → 12 V boost for the Beck controller, η 0.88 (ASSUMED)
- HAT quiescent 0.1 W (ASSUMED)
- usable × 0.90, end of life × 0.80

**NORMAL at the battery:** V1 9.00 W; UPS 9.20 W. With the AUO G101UAN01.0 manufacturer power figures (below): 8.28 / 8.42 W.

| Cells | Route | NORMAL h (new / EOL) | 6 h + 10 % at EOL | HIGH h (new) |
|---|---|---|---|---|
| 4S M65A | V1 | 9.2 / 7.4 (10.0 / 8.0 with the G101 MFR figures) | yes | 4.3 |
| 4S M65A | UPS | 9.0 / 7.2 (9.8 / 7.9) | yes | 4.3 |
| 4S 53G2 | V1 | 7.4 / 5.9 (8.0 / 6.4) | **no** | 3.5 |
| 4S 53G2 | UPS | 7.2 / 5.8 (7.9 / 6.3) | **no** | 3.5 |

The representative day is ≈ 74 Wh (V1) vs ≈ 76 Wh (UPS); with the G101 figures, 69 vs 70 Wh. On the 5 V rail the UPS route draws 1.7 A NORMAL and 4.4 A WORST (including the 12 V boost), within its 6 A rating.

## 4. Side-by-side (1 = poor, 5 = good)

| Criterion | Current V1 (BQ25798 + TPS25751, Pololu rails) | Waveshare UPS HAT (E) |
|---|---|---|
| Pi 5 compatibility | 5: USB-C power-only plug + EEPROM setting | 4: pogo pins, designed for the Pi 5 |
| 5 V / 5 A capability | 4: 5.5 A Pololu (or the 5 A TPS56339 on the TI design) | 4: 6 A continuous claimed (MFR) |
| Battery capacity | 5: any 4S1P 21700 in a separate bay (92 Wh M65A) | 5: the same cells fit its holders |
| Battery safety | 4: documented protector (OV / UV / OCD / OCC / SCD / NTC, 50 mA balancing) + 1 kA fuse | **2: protections and balancing undocumented, unnamed ICs** |
| Charging | 5: 3.2 A (5 A max), JEITA from the pack NTC | 3: ≤ 40 W input, charge current not stated |
| USB-C input | 5: PD 60 W preferred / 45 W minimum | 4: PD 40 W |
| Solar compatibility | 5: P108 on VAC2 (buck-boost, Voc-MPPT) | **1: no solar input, no MPPT** |
| MPPT | 4: Voc sampling (host-enabled) | 1: none |
| Runtime | 5 | 5 (equal within 2 %) |
| Efficiency | 4 | 4 (equal within the uncertainty) |
| Physical size | 4: flat boards under the keyboard; battery in its own bay | **1: cells under the Pi raise the compute stack far beyond the 35 mm bay** (§5) |
| Weight | 4 | 4 |
| Cost | 3: ≈ €60 board + €78 Pololu (+ €167 EVM bench) | 5: ≈ €38 |
| Availability | 4 | 5 |
| Documentation | 5: TI datasheets + full reference design | 2: wiki only, no schematic or part numbers |
| Reliability | 4 (reference-design based) | 3 (unknown) |
| Serviceability | 5: battery behind its own door | 2: battery under the Pi stack |
| Replaceability | 4 | 4 |
| Offline operation | 5: TPS25751 EEPROM configures the charger with no host | 3: MCU auto-shutdown needs scripts |
| Customization | 5 | 1 |
| Engineering effort | 3 (lower with TIDA-050047) | 4 (but solar and 12 V need extra boards) |
| Physical validation | EVM bench + build | bench + build + solar subsystem |
| Risk | Medium: PCB layout, now based on a TI reference design | **High for NOMAD:** solar, fit, safety and battery placement are unknown or failing |

## 5. Solar and fit, the deciding points

- **Solar:** the UPS HAT (E) accepts only USB-C PD sources. A P108 (Voc 20.45 V, Vmp 17.3 V, 0.57 A) cannot negotiate PD. With no input-voltage regulation, a power-bank charger would collapse the panel voltage.
  - Using the P108 would need an external MPPT that outputs USB-C power. That means extra boards, double conversion, a second protection path, and no simplicity left.
  - **The UPS HAT (E) does not support the P108 properly.**
- **Fit:**
  - The cells sit on the HAT under the Pi; the board-only outline is 56 × 88. Battery layer ≥ 22 mm (21700 diameter) + board + pogo spacing, plus the existing Pi + Active Cooler + M.2 HAT+ stack (25.9 EST): **≈ 50–55 mm (EST) in a 35 mm palm bay.**
  - It does not fit the 306 × 253 × 40 envelope.
  - It would also move the battery out of its own serviceable bay into the warm compute bay, which is under the approval gate.
- **12 V:** the Beck controller and the G101UAN01.0 LED supply need 12 V. The UPS HAT only gives 5 V, so a 5 → 12 V boost is needed anyway.

## 6. Key new finding: TIDA-050047

TI's TIDA-050047 (the USB-PD-CHG-EVM-01 design guide, rev. June 2025) is **NOMAD's core power board already designed by TI:**
- TPS25751D + BQ25798, 2–4 cells, sink 5–20 V, charge ≤ 5 A
- a **5 V / 5 A TPS56339 buck** on board
- an EEPROM configuration bundle, so the PD controller configures the charger **without any host**

Building V1 from this reference schematic and layout removes most of the "custom PCB" risk identified in the audit.

What NOMAD adds:
- the P108 path on VAC2 (ideal diode, TVS, Voc-MPPT enabled by the Pi over I²C)
- the 12 V buck-boost (Pololu S18V20F12, or keep it off-board)

Board dimensions are not in the guide text; take them from the TI design files (owner action).

## 7. Gate 0 status

| Item | Result | Status |
|---|---|---|
| AUO G101UAN01.0 datasheet | **Official AUO specification rev. 1.5 (2021-07-28), via Avnet** (full table below) | **CLOSED.** Connector position: rear-view drawing on p. 24 of the same PDF, read at CAD time |
| Beck controller | eDP 1–2 lane + 12 V backlight supply match the panel on paper. HBR link-rate support (needed for 1920 × 1200 @ 60 on 2 lanes), panel firmware and price are not public | **OWNER ACTION:** e-mail Beck with the G101UAN01.0 spec |
| TorqMaster SB-261 price | No online shop or distributor listing found | **OWNER ACTION:** TorqMaster quote |
| PERIBOARD-416 USB-C port | Product photos: **rear edge, right of centre** (≈ x + 70–90 mm, EST from the photo). It does not meet the GNSS window (left); use a right-angle plug | **CLOSED (photo).** **NEW CONFLICT:** the product page says 285 × 116 × **21** mm, 361 g; the manual says 16 mm, 332 g. Measure on arrival |
| PERIPAD-501 II availability | New units on eBay.de €23–34 (several sellers) and on Galaxus (AT); 60 g, 1.6 m cable | **CLOSED** |
| TI EVM dimensions | Not in the guide text | **OWNER ACTION:** board outline from the TIDA-050047 design files |
| Printer access | — | **OWNER ACTION** |

**AUO G101UAN01.0 specification (MFR, rev. 1.5, 2021-07-28):**

| Item | Value |
|---|---|
| Outline | 228.22 × 148.32 × 5.35 mm max |
| Mass | 140 g max |
| Active area | 216.81 × 135.5 mm |
| Interface | eDP 1.2, **2-lane pin assignment**, connector IPEX 20455-030E-12 |
| Logic | VDD 3.3 V, 0.66 W typ / 0.79 W max |
| Backlight | LED supply 12 V (10.8–13.2 V), 152 / 180 mA, **1.82 / 2.16 W at 100 %**; integrated LED driver; PWM 200 Hz–20 kHz, 10–100 % duty |
| Luminance | 320 min / 380 typ cd/m² |
| Surface | HCLR |
| Temperature | operating −10…+60 °C (panel surface); storage −20…+60 °C |
| LED life | 20 000 h min / 30 000 h typ |

## 8. The other cyberdeck parts

- **Wisecoco 10.1":** no 1920 × 1200 Wisecoco model with a datasheet was found; the listings found are 1280 × 800. Not a replacement. The AUO is now fully specified.
- **CACOE mini keyboard:** Bluetooth with an internal battery, and no published dimensions. Contrary to the wired / no-battery requirement. Reject.
- **Azoteq TPS65:**
  - What it is: a 65 × 49 mm capacitive trackpad module (IQS550, I²C, 1.65–3.6 V, 100 Hz, gestures, for 0.2–1.2 mm overlays); Linux has an iqs5xx driver.
  - Why not now: it is thinner and lower-power than the Perixx, but needs an overlay, mounting, an I²C harness and driver / pointer configuration.
  - Verdict: a V1.1 candidate, not now.
- **INIU B64 (27 000 mAh, 140 W):**
  - Specs: ≈ 100 Wh, 183 × 89 × 25 mm, 625 g.
  - Not inside NOMAD: it does not fit a palm bay, cannot be serviced, has unknown cells / BMS in a warm enclosure, auto-sleeps at low loads, and pass-through behaviour is undefined.
  - Useful **outside** NOMAD: a 20 V 3 A PD source that recharges NOMAD in the field. NOMAD already accepts PD input.
- **Wiltec case:** ignored.
