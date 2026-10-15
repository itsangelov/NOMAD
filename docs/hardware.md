# Hardware — NOMAD V1

Component selections and their status. Update this file when a SKU is locked or a part is measured.

- The architecture is B1 (D-010). Requirement status by subsystem is in `v1-requirements.md`.
- **Characterization:** `prototypes/V1/E-POWER-001_hardware_energy_characterization.md` (2026-10-01). It holds the sourced electrical and physical data, the preliminary power model and the conflicts. Nothing there was bought or measured.
- **Power architecture baseline (2026-10-02):** `docs/E-POWER-002-POWER-ARCHITECTURE.md`.
- **Energy-chain research (2026-10-02):** `docs/E-POWER-RESEARCH-CAMPAIGN.md`. It adds display controllers (Beck BTC-mini / BTC-mini-eDP), cells, BMS, chargers, MPPT, regulators and candidate tables. Nothing is selected.

## V1 candidate set (2026-10-06)

The Virtual V1 integration selects one candidate per function. Full records (dimensions, masses, interfaces, sources, prices, purchase gate) are in `prototypes/V1/v1_hardware.py`. The BOM is `prototypes/V1/V1_BOM.csv`; the reasoning is in `V1-VIRTUAL-INTEGRATION.md` §2.

| Function | V1 candidate | Status |
|---|---|---|
| Computer | Raspberry Pi 5 8 GB + Active Cooler + M.2 HAT+ + Raspberry Pi SSD 512 GB | selected / candidate |
| Display | **AUO G101UAN01.0** (eDP 2-lane, industrial, 3P data) | candidate; datasheet needed (gate 0) |
| Display controller | **Beck BTC-mini-eDP**, in the base | candidate; quote needed |
| Keyboard | **Perixx PERIBOARD-416** (285 × 117 × 16, 332 g, MFR manual) | candidate |
| Trackpad | Perixx PERIPAD-501 II | candidate; availability unknown |
| GNSS | SparkFun GNSS Flex pHAT DAN-F10N (US$74.95, in stock) | candidate |
| Enclosure fan | **Sunon MF30100V1-1000U-A99** (30 × 30 × 10, 5 V, 0.6 W, 5.5 CFM) | candidate |
| Display hinges | **2 × Southco E6-10-216-50** (1.8 N·m, €39.38 each, RS) | candidate |
| Leaf hinges | 2 × TorqMaster SB-188-SB-261-6 | candidate (coupon gate) |
| Panel | Voltaic P108 | candidate |
| Cells / pack | 4 × Molicel M65A (preliminary) in a holder-type 4S1P pack (custom spec) | candidate; cell = owner |
| Power board | Custom: BQ25798 + TPS25751 (bench-validated first on TI USB-PD-CHG-EVM-01) | spec / candidate |
| Rails | Pololu D36V50F5 (5 V 5.5 A), S18V20F12 (12 V) | candidate |
| Power button | 12 mm sealed momentary → Pi J2 + charger QON | provisional (generic spec) |

## Characterization table (E-POWER-001 and the research campaign; history of the candidates above)

| Component | Candidate / target | Status | Key data (source in E-POWER-001) | Key constraints |
|---|---|---|---|---|
| Computer | Raspberry Pi 5, 8 GB | selected | 85 × 56, holes 58 × 49 (MFR drawing); 5 V / 5 A USB-C PD; typical active 0.8 A (MFR); 3.2 W idle / 9.8 W stress (3P); 1–1.4 W when off unless `POWER_OFF_ON_HALT=1` (MFR) | Needs active cooling; 1.6 A USB budget shared with the fan |
| Cooler | Raspberry Pi Active Cooler | candidate | 5 V PWM fan, 1.09 CFM, 8 000 RPM; current not published; drawing ≈ 63.5 × 42.5 × 13.7 (inferred) | Fan off below 50 °C SoC (firmware curve) |
| Enclosure fan (reference) | Noctua NF-A4x10 5V PWM | candidate (reference) | 40 × 40 × 10, 0.3 W typ / 0.35 W max, 5.24 CFM (MFR) | Only if the enclosure needs one (thermal, step 6) |
| NVMe adapter | Raspberry Pi M.2 HAT+ (Standard) | candidate | PCIe 2.0 x1; ≤ 3 A to the device; 16 mm stacking header (fits over the Active Cooler); **0–50 °C ambient** (MFR) | Narrowest temperature rating in the stack |
| SSD | Raspberry Pi SSD 512 GB, M.2 2230 | candidate | 22 × 30; 0–70 °C; power not published (MFR). Reference SN740 512 GB: 50 mW avg active, ≤ 4.7 W max avg, 3.3 mW PS5 (MFR) | |
| Display | Winstar WF101NTYA4LNN0 | candidate | 1920×1200 IPS, 500 nit, anti-glare, 2-ch LVDS, no controller; 231.4 × 152.3 × 9.1; panel 6.8 W typ / 7.8 W max at full backlight; −20…+70 °C (MFR) | Above the ≤ 6 W target; thicker than the working value |
| Display | AUO B101UAN01.C | candidate | 1920×1200, 400 nit, eDP, glossy; 229.71 × 150.3 × 4.6, 115 g; 0–50 °C (3P); power not published | Glossy (target is matte) |
| Display | Waveshare 10.1inch HDMI LCD (G) | candidate (weak data) | 1920×1200 IPS, HDMI, 12 V input, touch + optical bonding; brightness and power not published (MFR) | V1 is non-touch |
| Display controller | HDMI → LVDS / eDP board | TBD | Not characterized | Placement and cable through the hinge |
| Display hinges | Southco E6-10-216-50 / E6-10-416-50 (1.8 N·m symmetric; 20 000 cycles ±20 %); E6-10-216F-50 (1.8 / 1.1 asymmetric); TorqMaster SB-188-SB-254-H (1.36–1.69 N·m) | candidates | Southco catalogue; TorqMaster per `prototypes/B1_SB261/reports/01` | ~1.5–1.8 N·m per hinge target (D-010 CALC); fit with D-006 unverified |
| Keyboard | Perixx PERIBOARD-426 (276 × 138 × 14), -416 / -332 (285 × 116 × 21, 361 g), -422 (291 × 138 × 19), -409H (314 × 146 × 20) | candidates | USB HID; power not published (MFR) | **None meets ≤ 8 mm** |
| Trackpad | Perixx PERIPAD-501 II | candidate (availability unknown) | 86 × 75 × 13 per the official Perixx manual, not measured (E-POWER research campaign [K1], 2026-10-02); not listed on the Perixx stores | |
| Trackpad | Perixx PERIPAD-501 / PERIPAD-506 | candidates | 501: no official dimensions. 506: 135 × 116 × 14, USB-C to A (MFR) | |
| GNSS | SparkFun GNSS Flex pHAT – DAN-F10N (GPS-29491) | candidate | DAN-F10N antenna module 20 × 20 × 11.6 (u-blox); GPS / Galileo / BeiDou / QZSS / NavIC, L1/L5, **no GLONASS**; 21 mA tracking / 26 mA acquisition at 2.7–3.6 V; UART + PPS | The internal patch needs sky view |
| GNSS antenna | Internal patch (default) or u-blox ANN-MB5 (L1/L5 active, 49.14 × 46.14 × 15.94, 17 mA at 5 V, SMA, 3 m RG174, IPX7) | candidate | MFR | |
| Solar panel | Voltaic P108 | candidate | 9.92 W peak; Voc 20.45 V; 17.34 V / 570 mA; 22.3 × 27.4 × 0.4 cm; 328 g; 3.5 × 1.1 mm plug, 50 cm (MFR); Isc and temperatures not published | Fits the B1 leaf; single US vendor |
| Solar-leaf hinges | TorqMaster SB-188-SB-261-6, ×2: band -6, 0.96–1.13 N·m, balanced (PUB) | candidate (current selection; physical validation required) | `prototypes/B1_SB261/` | SF ≈ 1.16 vs 0.83 N·m required; load, material and temperature unpublished |
| Heat-set inserts (B1 hinge rail) | Ruthex RX-M3x5.7 (lid); M2.5 × 4, OD 3.55 (e.g. PartsBuilt PBX-TI-M25-4L35W-4PK) (leaf) | candidate | | Standard 4.6-OD M2.5 inserts must not be used at the leaf |
| Stay | 2 stainless flats 3 × 16, M4 shoulder-screw pivots (D-010 Phase 2) | concept | | Mandatory for B1; design TBD |
| Battery pack | **4S1P 21700 Li-ion** (E-POWER-002 baseline). Cells: Molicel INR-21700-M65A (23.0 Wh, preliminary datasheet) or Samsung 50E-class (17.8 Wh) | candidate (topology baseline; cell **owner decision**) | 92 / 71 Wh nominal; 16.8 / 14.4 / 12.8 V; ≈ 358 / 334 g | Fits 90 × 82 × 30 only as a tightly bonded pack; removable, serviceable as a unit |
| Charger / power path | TI BQ25798-class: NVDC buck-boost 1–4S, dual input, VOC-MPPT; US$5.20 (DigiKey) | candidate | Input ≤ 3.3 A, charge ≤ 5 A, discharge ≤ 6 A continuous (MFR) | Custom PCB in the power-electronics reserve |
| USB-C PD sink | TI TPS25751 (I²C charger control, US$2.99) or TPS25730 (strap-configured, US$3.04) | candidate | 20 V 3 A preferred, ≥ 45 W minimum | Beside the USB-C receptacle (rear panel) |
| BMS / protection | 3–5S standalone protector (TI BQ77915-class, US$2.05) on the pack; Littelfuse MINI 10 A / 32 V DC / 1 kA fuse (US$0.39) | candidate (requirements baseline) | OV 4.25–4.30, UV 2.8–3.0, OCD / OCC / SCD, NTC, 50 mA balancing | NANO2 0451-class fuse rejected (50 A breaking) |
| 5 V rail | Pololu D36V50F5 (5 V 5.5 A buck, US$39.95) or a ≥ 6 A 5.1 V equivalent | candidate | 80–95 %; 25.4 × 25.4 × 9.5 mm | 5.0 V ±4 % vs the Pi's 5.1 V (E2-R03) |
| 12 V rail | Pololu S18V20F12 (12 V 2 A buck-boost, US$29.95) | candidate | 2.9–32 V in, 80–90 %; 43 × 21 × 10 mm | For the display controller |
| Fasteners | M2.5, M3 with heat-set inserts | provisional | | |
