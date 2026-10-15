# Solar — NOMAD V1

**Active architecture: B1 (D-010, accepted 2026-10-01).** One large solar leaf behind the display lid. Requirements and their status: `docs/v1-requirements.md` §8. Parameters: `docs/mechanical-spec.md` (Lid (B1), Solar leaf (B1)).

## V1 integration (2026-10-06)

- B1 is integrated unchanged. The SB-261 axis stays at (y 4.0, z 63.5) closed, because the lid core stays 19.
- **Leaf outline:** 290 × 239 (panel + 2 × 8 frame). It now follows the panel, not the lid, because the lid grew to 253 deep.
- **Leaf mass:** ≈ 413 g. It needs 0.78 N·m per hinge vs 0.96–1.13 published (SF ≈ 1.23, CALC).
- **Stability:** with the stay, every deployed state tips only above 12.7 m/s wind (CALC).
- **Solar lead:** runs through the display-hinge centre knuckle (60 mm twist zone) to the power board, ≈ 860 mm.
- Record: `V1-VIRTUAL-INTEGRATION.md` §5, §10.

## B1 concept

- **Leaf:** a rigid solar leaf covers the lid back. It is hinged at the lid's top edge and swings from 0° (stowed flat on the lid back) to about 190° (upright above the lid).
  - It aims at a sun behind the device, overhead or behind the user.
  - It charges while the machine is closed.
  - It **cannot** shade the screen while generating power (Phase 2 §15).
- **Leaf hinges:** two structural constant-torque friction hinges hold the leaf angle. There is no separate lock and no motor.
  - Current selected hinge candidate: **TorqMaster SB-188-SB-261-6**, mounted F-R-R-F (outer bands to the lid, inner bands to the leaf).
  - Subject to physical validation. Record: `prototypes/B1_SB261/`.
- **Cable:**
  - One panel cable runs in a dedicated sleeve near the hinge axis.
  - Bends are R ≥ 12, and the twist happens along the axis (the scratch rail has a 64 mm zone at 2.97°/mm).
  - A connector at the leaf lets the panel come off.
  - No slip ring, no loop, no gears.
- **Panel:** **Voltaic P108** is the current **candidate**, not selected. Per the manufacturer page (2026-10-01, E-POWER-001):
  - 9.92 W peak, Voc 20.45 V, Vmp 17.34 V, Imp 570 mA
  - 22.3 × 27.4 × 0.4 cm, matte ETFE on 2.0 mm FR4, 328 g
  - 3.5 × 1.1 mm plug, 50 cm cable
  - Isc and temperature ratings are not published
  - This replaces the earlier 9.5–10.9 W range.
- **Role:** a field energy **replenishment** system, not NOMAD's primary power source (`power.md`). The P108 peak rating is below every preliminary load state.
- **Lid:** a vented air gap of at least 6 mm with low-e foil between the lid back and the panel back (Phase 2 §13, EST). Sun-exposed parts should be ASA or light-coloured.
- **Stay:** a **mandatory** fold-out rear outrigger stay (two stainless flats on M4 shoulder screws at the rear base corners). Without it, B1 tips at 2.4–8.3 m/s; with it, at 11.4–18 m/s (CALC). Design details are TBD.

**Operating rules (from the studies, not yet owner-confirmed):**
- Deploy the stay when the leaf is above about 45° or it is windy.
- At a lid angle above about 120°, the leaf free edge can touch the table at low leaf angles: 10–60° in Phase 2, 15–53° at φ 125 for the SB-261 rail. Open the leaf first.
- Closed charging in hot sun needs a battery-temperature limit in the charger or BMS (≤ 45 °C).

## Status

| Item | Status |
|---|---|
| Architecture B1 | **LOCKED** (D-010) |
| Leaf motion 0–190° | DEFINED (owner target); **VALIDATION REQUIRED** (kernel only) |
| SB-188-SB-261-6 leaf hinges | **CANDIDATE** (current selection); **VALIDATION REQUIRED** (coupon not printed; SF ≈ 1.16 on torque; load and temperature unpublished) |
| P108 panel | **CANDIDATE** |
| Cable sleeve, R12 | DEFINED (concept); **VALIDATION REQUIRED** (twist cycling) |
| Stay | DEFINED (concept); design TBD; **VALIDATION REQUIRED** (tip test) |
| Vented gap + foil | DEFINED (EST); **VALIDATION REQUIRED** (thermal mock-up) |
| Solar charge controller / MPPT | BASELINE: charger-integrated VOC-MPPT on the second charger input (BQ25798-class), USB-C priority, never a direct system source (E-POWER-002 §8); part TBD; VALIDATION REQUIRED |

## Physical validation gates (future)

- The SB-261 coupon migration gate (`prototypes/B1_SB261/COUPON_SPEC.md` §7).
- The D-010 Phase 2 §24 mock-ups:
  - tipping with and without the stay
  - thermal gap and foil
  - cable twist cycling
  - friction-hinge torque against angle and temperature
  - ASA frame warp
  - transport and latch
  - display-hinge cable pass

## Records

| Record | Path |
|---|---|
| Architecture decision | `docs/decisions.md` D-010 |
| A vs B1 studies | `prototypes/P0.1/d010_solar_architecture_comparison.md`, `prototypes/P0.1/d010/d010_solar_architecture_phase2.md` (tool `CAD/tools/d010_phase2_study.py`) |
| Concept model (isolated) | Onshape Feature Studio `NOMAD_D010_Concepts` |
| SB-261 hinge rail | `prototypes/B1_SB261/` |

## Architecture A — SUPERSEDED / DEFERRED FOR NOMAD V1

Before D-010, the solar concept was two cassettes stored side by side in the rear of the display lid (D-004).
- Each slid out laterally and tilted independently (±60–75°) about an axis along its slide direction.
- Each tilt had a positive indexed lock (D-009).
- A metal hub/pin carried the rotational load; printed gears only positioned.
- No motors and no slip ring.

**Why it was not selected for V1** (D-010 Phase 2):
- an unresolved cable crossing through the structural rail wall
- tight cable bends
- a hub bracket below SF 2
- ±80° hard stops not packaged
- precision metal parts
- custom-size laminates

**What is kept:** the A requirements (rail, rotation, lock, wind, wiring, modularity), the Round B–E studies and the D-004 / D-009 records.
- They are preserved unchanged in `docs/decisions.md`, `docs/mechanical-spec.md` and `prototypes/P0.1/` as engineering history and possible later reference.
- They do not describe the V1 design.

### Original Architecture A solar specification (verbatim, as it stood before D-010)

#### Concept

Two cassettes are stored side by side in the rear of the display lid. Each one slides out laterally (left and right) and rotates independently for sun angle. Operation is manual only; there are no motors.

The cassette itself is the structural solar wing. It carries the panel, frame, rotation interface, electrical connector and structural load. There is no separate articulated arm.

#### Requirements

| Area | Requirement |
|---|---|
| Rail | Constrained lateral slide, low play, resists twisting, positive retention, hard end stop, self-aligning, serviceable, printable. Candidates: dovetail, captured box rail, guide blocks, metal rod, replaceable wear surfaces. |
| Rotation | A dedicated structural hub/pin (metal) carries the rotational load; the rail carries deployment and structural loads. Printed gears are for positioning and actuation only, never the primary structural load path. Approximate range ±60° to ±75°; no continuous rotation. Axis: approximately along the slide/deployment direction (D-004). Discrete indexed positions. |
| Lock | Positive manual lock with an obvious locked/unlocked state. Durable, serviceable, manually releasable. Candidates: spring pin, detent, indexed holes, toothed ring, lever. |
| Wind | Extended panels act as sails. Account for bending, twist, rail and chassis loads, and lock strength. Define a safe stowage procedure. |
| Wiring | Panel → internal wiring → serviceable connector → protected flex cable → rotation interface → chassis. Stranded wire, strain relief, controlled bend radius. Never route through exposed gears. No slip rings. |
| Modularity | Unlock → disconnect → remove → replace → connect → lock. No destructive assembly. |

#### Open issues

- Wind load on a deployed cassette is reacted through the lid and the display hinge. The hinge design and a lid-angle lock must account for it. *(inferred; not calculated)*
- Panel selection determines cassette thickness and electrical output.

#### First physical prototype priority

1. Cassette
2. Rail
3. Rotation interface
4. Lock
5. Critical chassis interfaces
