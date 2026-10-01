# Power — NOMAD V1

## Approach

V1 uses ready-made power modules. The battery voltage, capacity and DC/DC selection are **TBD** and will be set from measured NOMAD power consumption.

## Mechanical reservations

- A removable, serviceable battery bay. It must never be sealed.
- A power-electronics region with mounting, airflow, cable space, service access and room for future revisions.
- A solar input path from the B1 solar leaf (one panel cable through the leaf-hinge sleeve and the display-hinge pass; see `solar.md`).
  - The current candidate panel is the Voltaic P108: 18 V, 9.5–10.9 W nameplate (VENDOR).
  - (The earlier two-cassette input belongs to Architecture A, superseded for V1.)

The battery, power and charging architecture is **unresolved**. The open items are listed in `v1-requirements.md` §9. Nothing in this file selects them.

## Power budget

To be filled with **measured** values.

| Load | Idle (W) | Typical (W) | Peak (W) | Status |
|---|---|---|---|---|
| Raspberry Pi 5 + NVMe | | | | not measured |
| Display (target ≤ 6 W) | | | | not measured |
| GNSS | | | | not measured |
| Keyboard + trackpad | | | | not measured |
| Cooling fan | | | | not measured |
| Solar input (P108 candidate) | — | — | 9.5–10.9 W nameplate (VENDOR); 5.6–7.1 W real at best aim (CALC/ASSUMED) | not measured |
