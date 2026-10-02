# Power — NOMAD V1

## Energy-system principle

> **NOMAD's solar system is a field energy replenishment system rather than its primary power source.**

- The purpose of B1 (D-010) is to deploy a larger panel when stationary while keeping NOMAD compact when stowed.
- B1 does **not** provide energy independence.
- No runtime extension is claimed until the power budget is established and a solar-yield model exists.
- B1 must eventually justify its mechanical complexity through measurable energy contribution.

## Approach

- V1 uses ready-made or custom power electronics built from documented ICs and modules.
- **Owner direction (2026-10-02):**
  - **Runtime:** 6 h normal-use design target, 4 h minimum. 8 h is reference only.
  - **Battery:** ≤ 92 Wh if realistically possible; do not casually exceed 100 Wh.
- **Power architecture baseline: E-POWER-002** (`docs/E-POWER-002-POWER-ARCHITECTURE.md`, 2026-10-02). It is summarised below.
- **Not selected yet:** battery cell SKU and supplier, BMS SKU, charger PCB, PD controller, connectors and wire gauge (TBD).
- *History:* before E-POWER-002, voltage, chemistry and capacity were TBD. An 80–120 Wh figure was once mentioned as a planning envelope only.

## Mechanical reservations

- A removable, serviceable battery bay. It must never be sealed.
- A power-electronics region with mounting, airflow, cable space, service access and room for future revisions.
- A solar input path from the B1 solar leaf: one panel cable through the leaf-hinge sleeve and the display-hinge pass (see `solar.md`).
  - The current candidate panel is the Voltaic P108: **9.92 W peak, Voc 20.45 V, 17.34 V / 570 mA** (manufacturer page, 2026-10-01).
  - Isc and temperature ratings are not published.
  - (The earlier two-cassette input belongs to Architecture A, superseded for V1.)

The battery, power and charging **architecture** now has an engineering baseline (E-POWER-002, below). Specific parts remain TBD. The requirement statuses are in `v1-requirements.md` §9.

## Power architecture baseline (E-POWER-002, 2026-10-02)

| Element | Baseline | Status |
|---|---|---|
| Battery | **4S1P 21700 Li-ion**: 16.8 / 14.4 / 12.8 V (full / nominal / system cutoff); BMS floor 11.2 V. 92 Wh class with M65A-type cells (preliminary datasheet); 71 Wh with mature 50E-type cells | BASELINE (topology); cell **TBD / owner** |
| Charger / power path | NVDC buck-boost charger, 1–4S, dual input, VOC-MPPT (TI BQ25798-class); input ≤ 3.3 A, charge ≤ 5 A (baseline 3.2 A), discharge ≤ 6 A continuous | BASELINE; PCB TBD |
| External input | **USB-C PD sink**; 20 V 3 A (60 W) preferred, ≥ 45 W minimum; no DC barrel recommended | BASELINE; controller TBD (TPS25751 / TPS25730 class) |
| Solar | P108 on the second charger input through reverse-polarity protection + TVS; MPPT; USB-C has priority; never a direct system source | BASELINE |
| System bus | 12.0–16.8 V (VSYSMIN 12 V) | BASELINE |
| 5 V rail | 5.1 V, ≥ 5 A buck from the bus, feeding the Pi 5 (`PSU_MAX_CURRENT=5000`). USB peripherals, Active Cooler, GNSS and NVMe are fed through the Pi | BASELINE |
| 12 V rail | 12 V ±5 % buck-boost, ≈ 1 A, feeding the display controller | BASELINE |
| Protection | BMS on the pack (3–5S protector: OV 4.25–4.30, UV 2.8–3.0, OCD, OCC, SCD, NTC, 50 mA balancing); 10 A, 32 V DC, ≥ 1 kA MINI fuse; keyed pack connector; charger JEITA (0–45 °C charge); ship mode | BASELINE requirements; SKUs TBD |
| Runtime (D-A, normal) | 9.3 h new / 7.4 h end of life (92 Wh); 7.2 / 5.8 h (71 Wh) | CALC |
| Power-electronics heat | ≈ 1.1 W normal; ≤ 5.7 W worst while charging | CALC |
| Fit | Pack fits 90 × 82 × 30 **only as a tightly bonded pack**; a holder pack needs ≈ 93.6 × 82 × 31. Power electronics ≈ 66 % of the 90 × 45 floor | CALC / EST; **owner decision** on the bay |

**Not physically validated:** battery safety, charging behaviour, MPPT behaviour and thermal.

## E-POWER research campaign (2026-10-02)

The full research dossier is `docs/E-POWER-RESEARCH-CAMPAIGN.md` (calculator: `prototypes/V1/epower_campaign_calc.py`). It covers:
- display and controller research
- refined load scenarios
- battery chemistry, scenarios and bay fit
- power architectures, charging, solar yield (PVGIS) and MPPT compatibility
- thermal and mass
- conflicts EP-C01–EP-C20 and the **owner decisions required**

**It selects nothing.** The table below remains the E-POWER-001 preliminary budget.

## Power budget (preliminary, published data only — E-POWER-001)

- **Full record, sources and evidence labels:** `prototypes/V1/E-POWER-001_hardware_energy_characterization.md`.
- **Labels:** MFR = manufacturer; 3P = independent third-party measurement; CALC; TBD.
- **Scope:** watts at the component, before conversion losses. **Nothing is NOMAD-measured.**

| Load | Idle (W) | Typical (W) | Peak (W) | Voltage | Status |
|---|---|---|---|---|---|
| Raspberry Pi 5 8 GB | 3.2 (3P) | 4.0 (MFR "typical bare-board active", 0.8 A) | 9.8 (3P stress-ng) | 5 V (5 A supply; 1.6 A of it for USB) | published |
| Pi 5 when "off" | 1–1.4 (MFR default); 0.01 with `POWER_OFF_ON_HALT=1` (MFR) | — | — | 5 V | published |
| Active Cooler | 0 below 50 °C SoC | TBD | TBD | 5 V (fan header) | not published |
| NVMe 2230 (reference: WD SN740 512 GB) | 0.0033 (PS5) | 0.05 (avg active) | ≤ 4.7 (upper bound) | 3.3 V | published for the reference drive; Raspberry Pi SSD not published |
| M.2 HAT+ | TBD | TBD | TBD | — | not published |
| Display panel (Winstar WF101NTYA4LNN0, full backlight) | — | 6.8 (CALC from MFR: 1.0 logic + 5.8 LED) | 7.8 (CALC from MFR max) | 3.3 V + 26–33 V LED string | published |
| Display controller board | TBD | TBD | TBD | — | not characterized |
| Keyboard | TBD | TBD | ≤ 2.5 (USB 2.0 limit, a bound) | 5 V USB | not published |
| Trackpad | TBD | TBD | ≤ 2.5 (same bound) | 5 V USB | not published |
| GNSS (DAN-F10N) | 0.0001–0.0002 (backup / standby) | 0.063 (tracking) | 0.086 (acquisition, CALC) | 3.3 V | published |
| Other always-on electronics (BMS, charger, MPPT, DC/DC quiescent) | TBD | TBD | TBD | — | not selected |
| Solar input (P108 candidate) | — | — | 9.92 W peak rating (MFR); real output depends on angle, temperature and losses | 17.34 V Vmp | published |

## Operating states (preliminary envelope)

Documented subtotals only. **The real totals are higher**: the display controller, HID devices, fan, HAT+ and conversion losses are not yet included. The display is counted at full backlight.

| State | Documented subtotal |
|---|---|
| A — Field standby (display on, Pi mostly idle, GNSS on) | ≈ 10.1–10.9 W + TBD |
| B — Normal operation (maps, offline knowledge, moderate load) | ≈ 10.9 W + TBD |
| C — Maximum sustained load | ≈ 17.7–22.4 W + TBD |

**What follows from these figures:**
- **The display is the largest load** in A and B.
- **The P108 peak rating (9.92 W) is below every state subtotal**, so the solar leaf replenishes energy; it cannot carry the operating load.
- No runtime is derived yet. That needs the owner's runtime target (PWR-5).
