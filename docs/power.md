# Power — NOMAD V1

## Energy-system principle

> **NOMAD's solar system is a field energy replenishment system rather than its primary power source.**

- The purpose of B1 (D-010) is to deploy a larger panel when stationary while keeping NOMAD compact when stowed.
- B1 does **not** provide energy independence.
- No runtime extension is claimed until the power budget is established and a solar-yield model exists.
- B1 must eventually justify its mechanical complexity through measurable energy contribution.

## Approach

- V1 uses ready-made power modules.
- The battery voltage, chemistry, capacity, BMS, charger, MPPT and DC/DC selection are **TBD**.
- They will be reverse-engineered from the characterized loads (step 5 in `v1-requirements.md` §18).
- **No battery is chosen. No capacity is a requirement.** An 80–120 Wh figure was mentioned earlier only as a planning envelope. It is **not** an owner requirement or a parameter.

## Mechanical reservations

- A removable, serviceable battery bay. It must never be sealed.
- A power-electronics region with mounting, airflow, cable space, service access and room for future revisions.
- A solar input path from the B1 solar leaf: one panel cable through the leaf-hinge sleeve and the display-hinge pass (see `solar.md`).
  - The current candidate panel is the Voltaic P108: **9.92 W peak, Voc 20.45 V, 17.34 V / 570 mA** (manufacturer page, 2026-10-01).
  - Isc and temperature ratings are not published.
  - (The earlier two-cassette input belongs to Architecture A, superseded for V1.)

The battery, power and charging architecture is **unresolved**. The open items are listed in `v1-requirements.md` §9. Nothing in this file selects them.

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
