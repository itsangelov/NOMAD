# System Architecture — NOMAD V1

## Form factor

A clamshell field computer:
- **Base:** keyboard, trackpad, computer, storage, GNSS, power electronics, cooling and a removable battery.
- **Lid:** the display, with **one solar leaf behind it**. This is Architecture **B1** (D-010, accepted 2026-10-01).
  - The leaf is hinged at the lid's top edge on two friction hinges and swings 0–190°.
  - A fold-out rear stay on the base keeps the machine from tipping when the leaf is deployed.

Exact module placement inside the base is still **proposed** (D-007, not accepted; see `decisions.md`).

**Architecture A, SUPERSEDED / DEFERRED FOR V1:** two sliding/tilting solar cassettes stored in the lid (D-004 / D-009). It is kept as an engineering record only.

Requirements by subsystem, with their status and the dependency order of the remaining virtual work: **`v1-requirements.md`**.

## Subsystems

| Subsystem | Baseline | Status |
|---|---|---|
| Compute | Raspberry Pi 5, 8 GB | selected |
| Storage | 500–512 GB NVMe (2230 preferred), Raspberry Pi M.2 HAT+ | provisional |
| Display | 10.1" IPS 1920×1200, ≥400 nit (500+ preferred), matte, HDMI, non-touch, ≤6 W | SKU not locked |
| Display hinges | Rear-face direction (D-006, provisional); ~1.6 N·m each for B1 (CALC) | TBD |
| Keyboard | Ultra-low-profile wired USB HID, ~280×105 mm, ≤8 mm | SKU not locked |
| Trackpad | Perixx PERIPAD-501 II | candidate |
| GNSS | SparkFun GNSS Flex pHAT / DAN-F10N; GPS/Galileo/GLONASS(/BeiDou), external antenna, PPS | candidate |
| Power | Ready-made modules; battery voltage and DC/DC TBD | TBD |
| Battery | Removable bay; capacity from measured consumption | TBD |
| Solar | B1 leaf (D-010): Voltaic P108 candidate panel; TorqMaster SB-188-SB-261-6 candidate leaf hinges; manual; no motors | architecture locked; parts candidate |

## Software (planned areas)

Launcher, offline maps, navigation, offline knowledge, local AI, power management, system. See `software/`.

## Detailed specifications

- V1 requirements: `v1-requirements.md`
- Mechanical: `mechanical-spec.md`
- Hardware: `hardware.md`
- Power: `power.md`
- Solar: `solar.md`
