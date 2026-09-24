# Solar Cassettes — NOMAD V1

## Concept

Two cassettes are stored side by side in the rear of the display lid. Each one slides out laterally (left and right) and rotates independently for sun angle. Operation is manual only; there are no motors.

The cassette itself is the structural solar wing. It carries the panel, frame, rotation interface, electrical connector and structural load. There is no separate articulated arm.

## Requirements

| Area | Requirement |
|---|---|
| Rail | Constrained lateral slide, low play, resists twisting, positive retention, hard end stop, self-aligning, serviceable, printable. Candidates: dovetail, captured box rail, guide blocks, metal rod, replaceable wear surfaces. |
| Rotation | A dedicated structural hub/pin (metal) carries the rotational load; the rail carries deployment and structural loads. Printed gears are for positioning and actuation only, never the primary structural load path. Approximate range ±60° to ±75°; no continuous rotation. Axis: approximately along the slide/deployment direction (D-004). Discrete indexed positions. |
| Lock | Positive manual lock with an obvious locked/unlocked state. Durable, serviceable, manually releasable. Candidates: spring pin, detent, indexed holes, toothed ring, lever. |
| Wind | Extended panels act as sails. Account for bending, twist, rail and chassis loads, and lock strength. Define a safe stowage procedure. |
| Wiring | Panel → internal wiring → serviceable connector → protected flex cable → rotation interface → chassis. Stranded wire, strain relief, controlled bend radius. Never route through exposed gears. No slip rings. |
| Modularity | Unlock → disconnect → remove → replace → connect → lock. No destructive assembly. |

## Open issues

- Wind load on a deployed cassette is reacted through the lid and the display hinge. The hinge design and a lid-angle lock must account for it. *(inferred; not calculated)*
- Panel selection determines cassette thickness and electrical output.

## First physical prototype priority

1. Cassette
2. Rail
3. Rotation interface
4. Lock
5. Critical chassis interfaces
