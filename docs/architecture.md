# System Architecture — NOMAD V1

## Form factor

A clamshell field computer:
- **Base:** keyboard, trackpad, computer, storage, GNSS, power electronics, cooling and a removable battery.
- **Lid:** the display, with **one solar leaf behind it**. This is Architecture **B1** (D-010, accepted 2026-10-01).
  - The leaf is hinged at the lid's top edge on two friction hinges and swings 0–190°.
  - A fold-out rear stay on the base keeps the machine from tipping when the leaf is deployed.

Module placement inside the base: the **Virtual V1 integration baseline** (`V1-VIRTUAL-INTEGRATION.md`, proposed as **D-011**, which amends the proposed D-007). Battery in the left palm bay, compute in the right palm bay, power board / display controller / 5 V rail under the keyboard, GNSS in the rear strip. **No plugs on the rear face**: USB-C power and button on the left wall, 2 × USB-A at the front right, fan exhaust on the right wall. Not yet accepted by the owner.

**Architecture A, SUPERSEDED / DEFERRED FOR V1:** two sliding/tilting solar cassettes stored in the lid (D-004 / D-009). It is kept as an engineering record only.

Requirements by subsystem, with their status and the dependency order of the remaining virtual work: **`v1-requirements.md`**.

## Subsystems

| Subsystem | V1 baseline (2026-10-06) | Status |
|---|---|---|
| Compute | Raspberry Pi 5, 8 GB + Active Cooler | selected / candidate |
| Storage | Raspberry Pi SSD 512 GB (2230) on the M.2 HAT+ | candidate |
| Display | AUO G101UAN01.0 (10.1" 1920×1200, eDP 2-lane, 380–410 nit, industrial; 3P data) + Beck BTC-mini-eDP controller in the base | candidate (gate 0 data required) |
| Display hinges | 2 × Southco E6-10-216-50 (1.8 N·m), rear-face direction (D-006), stop at 135° | candidate |
| Keyboard | Perixx PERIBOARD-416, wired USB, 285 × 117 × 16 (the ≤ 8 mm target is not met) | candidate |
| Trackpad | Perixx PERIPAD-501 II (86 × 75 × 13 per the official manual, not measured; availability unknown); alternative PERIPAD-506 | candidate |
| GNSS | SparkFun GNSS Flex pHAT / DAN-F10N; GPS / Galileo / BeiDou / QZSS / NavIC, L1/L5 (no GLONASS); integrated patch under a rear-deck window; PPS | candidate |
| Cooling | Active Cooler + Sunon MF30100V1 30 mm exhaust fan (right wall) | candidate |
| Power | NVDC buck-boost charger (BQ25798) + USB-C PD (TPS25751) on a custom board; P108 on the MPPT input; 12–16.8 V bus; Pololu 5 V 5.5 A and 12 V rails | architecture baseline; parts candidate |
| Battery | Removable 4S1P 21700 holder pack (Molicel M65A, 92 Wh) in its own bay; runtime NORMAL 9.2 h new / 7.4 h end of life (CALC); target 6 h / 4 h (owner) | candidate; cell = owner decision |
| Solar | B1 leaf (D-010), a field energy replenishment system, not the primary power source: Voltaic P108 (9.92 W peak); TorqMaster SB-188-SB-261-6 leaf hinges; manual; no motors | architecture locked; parts candidate |

Envelope: base 306 × 253 × 40, closed 306 × 253 × 73 (+ feet); mass ≈ 3.0 kg (CALC / EST).

## Software (planned areas)

Launcher, offline maps, navigation, offline knowledge, local AI, power management, system. See `software/`.

## Detailed specifications

- **Virtual V1 integration baseline: `V1-VIRTUAL-INTEGRATION.md`**
- V1 requirements: `v1-requirements.md`
- Mechanical: `mechanical-spec.md`
- Hardware: `hardware.md`
- Power: `power.md`
- Solar: `solar.md`
- Hardware and energy characterization (E-POWER-001): `../prototypes/V1/E-POWER-001_hardware_energy_characterization.md`
