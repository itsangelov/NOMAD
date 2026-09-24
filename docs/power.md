# Power — NOMAD V1

## Approach

V1 uses ready-made power modules. The battery voltage, capacity and DC/DC selection are **TBD** and will be set from measured NOMAD power consumption.

## Mechanical reservations

- A removable, serviceable battery bay. It must never be sealed.
- A power-electronics region with mounting, airflow, cable space, service access and room for future revisions.
- A solar input path from both cassettes (see `solar.md`).

## Power budget

To be filled with **measured** values.

| Load | Idle (W) | Typical (W) | Peak (W) | Status |
|---|---|---|---|---|
| Raspberry Pi 5 + NVMe | | | | not measured |
| Display (target ≤ 6 W) | | | | not measured |
| GNSS | | | | not measured |
| Keyboard + trackpad | | | | not measured |
| Cooling fan | | | | not measured |
