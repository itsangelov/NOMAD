# System Architecture — NOMAD V1

## Form factor

A clamshell field computer:
- **Base:** keyboard, trackpad, computer, storage, GNSS, power electronics, cooling and a removable battery.
- **Lid:** display, with two deployable solar cassettes stored in its rear.

Exact module placement inside the base is subject to approval (see `decisions.md`).

## Subsystems

| Subsystem | Baseline | Status |
|---|---|---|
| Compute | Raspberry Pi 5, 8 GB | selected |
| Storage | 500–512 GB NVMe (2230 preferred), Raspberry Pi M.2 HAT+ | provisional |
| Display | 10.1" IPS 1920×1200, ≥400 nit (500+ preferred), matte, HDMI, non-touch, ≤6 W | SKU not locked |
| Keyboard | Ultra-low-profile wired USB HID, ~280×105 mm, ≤8 mm | SKU not locked |
| Trackpad | Perixx PERIPAD-501 II | candidate |
| GNSS | SparkFun GNSS Flex pHAT / DAN-F10N; GPS/Galileo/GLONASS(/BeiDou), external antenna, PPS | candidate |
| Power | Ready-made modules; battery voltage and DC/DC TBD | TBD |
| Battery | Removable bay; capacity from measured consumption | TBD |
| Solar | Two sliding, rotating, lockable cassettes; manual; no motors | concept |

## Software (planned areas)

Launcher, offline maps, navigation, offline knowledge, local AI, power management, system. See `software/`.

## Detailed specifications

- Mechanical: `mechanical-spec.md`
- Hardware: `hardware.md`
- Power: `power.md`
- Solar: `solar.md`
