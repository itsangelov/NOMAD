# P0.1 Round B.2: Lid Structure and Printability Screening (V1 + fixes)

> **SUPERSEDED / DEFERRED FOR NOMAD V1 (D-010, 2026-10-01).** This record belongs to **Architecture A** (sliding/tilting solar cassettes and their lid, D-004 / D-009). The owner selected **Architecture B1** (one solar leaf behind the display lid) as the active V1 architecture. The content below is kept unchanged as an engineering record and possible later reference; it does not describe the V1 design. See `docs/decisions.md` D-010 and `docs/v1-requirements.md`.

**Status: modeled, screening only. Stiffness values are simple beam estimates, NOT FEA. No lid concept and no V1 architecture has been chosen.**

## Basis

- **Geometry:** V1 with its four provisional fixes: 17 mm bracket, 22.6 mm carriage, deploy clearance 8, 8 mm cable corridor. Cassettes, tilt architecture and ±75° target are unchanged. Tool: `CAD/tools/lid_structure_screening.py`, reusing the validated V1 prism model.
- **Back plate:** a one-way strip spanning the 202 mm cassette bay between the front and rear edge beams.
  - No support is possible inside the bay: the cassettes need all of it.
  - The side edges are open cassette slots.
- **Load cases:**
  - LC1: 20 N point load (hand press) on an effective width of L/2 = 101 mm. This is conservative; Round B.1 used the full width, which gives about 3× less deflection.
  - LC2: 1 kPa uniform (e.g. packed in a bag).
- **Criterion:** deflection ≤ half of the 1.0 mm cassette clearance.
- **Other assumptions:** PETG E = 2000 MPa and density 1.27 g/cm³, solid-section masses. Provisional screening loads: cassette 0.3 kg (no panel selected), 3 g shock, wind 10 and 20 m/s.
- **No Onshape run.** The kernel cannot check stiffness or printability, and the static structure added here uses the prism method already validated three times. API total unchanged at 75 / 2,500.

## Comparison

| | A: one-piece, external ribs | B: one-piece, perimeter frame + 1.6 mm panel | C: two-piece, front frame + ribbed rear shell |
|---|---|---|---|
| Back-plate deflection, LC1 / LC2 | 0.49 / 0.31 mm (11 mm ribs, 2.0 thick @ 30 mm, on a 2.5 skin) | **49.8 / 31.8 mm** (would need ~100 mm clearance) | 0.49 / 0.31 mm (same rear shell as A) |
| Lid thickness / closed stack | 42.5 / 84.5 mm | 31.5 / 73.5 mm | 42.5 / 84.5 mm |
| Unsupported span | 202 mm (ribs span it) | 202 mm: the frame **cannot** shorten it | 202 mm (ribs span it) |
| Collisions (all lid angles, slides, tilts) | none | none | none |
| Loops / corridor / display | clear | clear | clear |
| Controller keep-out | 12 mm tall under the rear edge beam (touches its boundary) | same | same |
| Hinge / base | ≥ 1.41 mm; overhang 103.8 / 197.6 at 105° / 135° | ≥ 1.41; 93.2 / 189.9 | ≥ 1.41; 103.8 / 197.6 |
| Printable? | **No practical orientation**: the cassette bay is a closed 296 × 202 × 10 tunnel (trapped support or a 202 mm bridge; on-edge needs 301 mm Z) | **No**, same tunnel | **Yes**: all parts print flat (front frame display-face-down, supports only under the two 14 mm edge beams; rear shell inner-face-down, ribs up; rails floor-down) |
| Can the display be installed? | **No**: integral rails sit 1 mm above the display back and the display is larger than its window | **No**, same | Yes: display in first, then rails (separate), then rear shell |
| Structure mass (solid estimate) | ~690 g | ~520 g (but no functional back) | ~690 g (front frame + rails ~375 g, rear shell ~315 g) |

## Stiffness alternatives for the back plate (LC1, conservative)

**Ribs:**

| Rib height | 6 mm | 8 mm | 10 mm | 12 mm |
|---|---|---|---|---|
| Deflection | 1.95 mm | 1.05 mm | 0.62 mm | 0.40 mm |

**Minimum stiffening to meet the criterion, by cassette clearance:**

| Cassette clearance | Minimum ribs → lid thickness | Printed sandwich → lid thickness |
|---|---|---|
| 1 mm | 11 mm → 42.5 | 9.5 mm → 38.5 |
| 2 mm | 8.5 mm → 41 | 7 mm → 37 |
| 3 mm | 7 mm → 40.5 | 6 mm → 37 |

The sandwich option is a thick printed plate with sparse infill. Its core shear is ignored, so its figures are optimistic.

## Front-frame and rail loads (all concepts)

- **Each rail is a ~150 mm cantilever over the display.**
  - It can only be supported at its outboard pad, beside the display.
  - Inboard supports are blocked by the display below, the cassettes above, and the cable corridor and service loops beside it.
  - Printed C-channel (I ≈ 2455 mm⁴) with a stowed 0.3 kg cassette: **0.67 mm static, 2.0 mm at 3 g**, against the 1.0 mm display clearance. **Risk for all concepts.** A metal stiffener in each rail would reduce this to roughly 0.2 mm *(inferred)*.
- **Deployed cassette:** moment on the carriage 0.53 N·m (10 m/s wind) to 1.2 N·m (20 m/s); carriage end reactions ~13–30 N.
  - In C these loads stay entirely in the front frame: rail → pad → frame → hinge. The rear-shell joint doesn't carry them.
- **Rail-to-frame attachment:** the outboard pad is 28.5 mm long, with only ~6 mm of material below the channel floor, and the channel must stay open for the deployed carriage. Tight; it needs a dedicated detail *(inferred)*.

## Concept C joint and assembly

- **Joint:** M3 heat-set inserts in the tops of the front and rear edge beams (14 mm bands, 8 mm bosses), 5 per band = 10 screws, M3 × ~9 through the 2.5 mm rear shell, driven from outside. Rib-free pockets at each screw.
  - Uniform back load (60 N total) is about 6 N per screw.
  - The screws also provide the rear shell's shear connection to the frame.
- **Assembly order:**
  1. Display into the front frame, from the back.
  2. Rails onto the pads.
  3. Cables, loops and controller.
  4. Cassettes slide in through the side slots onto the rails.
  5. Rear shell (10 screws).
- **Service:**
  - Cassette swap without opening the lid (release the end stop).
  - Display or controller service: rear shell off, cassettes out, rails off.

## Model output

```
=== Screening basis (NOT FEA) ===
back plate spans the cassette bay one-way: L = 202 mm between edge beams (no internal supports possible; side edges are open slots). E = 2000 MPa. LC1 20 N point at mid-bay on b_eff 101; LC2 1 kPa uniform. Criterion: deflection <= half the cassette clearance = 0.5 mm.

rib height sweep (skin 2.5, ribs 2.0 thick @ 30 mm, external):
  h  0: LC1  13.06 mm  LC2   8.32 mm  lid T 31.5  back-plate mass  225 g
  h  2: LC1   8.55 mm  LC2   5.45 mm  lid T 33.5  back-plate mass  241 g
  h  4: LC1   4.05 mm  LC2   2.58 mm  lid T 35.5  back-plate mass  258 g
  h  6: LC1   1.95 mm  LC2   1.24 mm  lid T 37.5  back-plate mass  274 g
  h  8: LC1   1.05 mm  LC2   0.67 mm  lid T 39.5  back-plate mass  291 g
  h 10: LC1   0.62 mm  LC2   0.40 mm  lid T 41.5  back-plate mass  307 g
  h 12: LC1   0.40 mm  LC2   0.25 mm  lid T 43.5  back-plate mass  324 g
  h 14: LC1   0.27 mm  LC2   0.17 mm  lid T 45.5  back-plate mass  340 g
  plain 1.2 plate: LC1 118.07  LC2  75.28
  plain 1.6 plate: LC1  49.81  LC2  31.76
  plain 2.0 plate: LC1  25.50  LC2  16.26
  plain 2.5 plate: LC1  13.06  LC2   8.32
  plain 4.0 plate: LC1   3.19  LC2   2.03

minimum stiffening to meet the criterion, versus cassette clearance (thickness = 28 + gap + plate):
  clearance 1: ribs 11 mm on 2.5 skin -> lid T 42.5;  printed sandwich 9.5 mm (core shear ignored, optimistic) -> lid T 38.5
  clearance 2: ribs 8.5 mm on 2.5 skin -> lid T 41;  printed sandwich 7 mm (core shear ignored, optimistic) -> lid T 37
  clearance 3: ribs 7 mm on 2.5 skin -> lid T 40.5;  printed sandwich 6 mm (core shear ignored, optimistic) -> lid T 37

concept B central panel 1.6 (no ribs): LC1 49.8 mm, LC2 31.8 mm -> would need ~100 mm clearance to stay off the cassettes; frame cannot shorten the 202 mm span (bay is clear, side edges slotted)

rail cantilever (all concepts): printed C-channel I = 2455 mm^4; stowed carriage 150 mm from the outboard pad; 0.3 kg cassette -> 0.67 mm static, 2.00 mm at 3 g toward the display (1.0 mm clearance)
  with a metal stiffener (aluminium bar insert (E 70 GPa, same section share ~30%)): roughly x12 stiffer -> 0.17 mm at 3 g (inferred)
deployed cassette on its carriage (arm 105 mm): wind 10 m/s: wind force 2.1 N, moment 0.53 N*m, carriage end reactions ~13 N; wind 20 m/s: wind force 8.5 N, moment 1.20 N*m, carriage end reactions ~30 N

--- A  one-piece, external ribs ---
lid thickness 42.5 (closed stack 84.5); back deflection LC1 0.49 / LC2 0.31 mm vs allowed 0.50; back-plate(+ribs) mass 315 g, edge beams 105 g
motion/stowed collisions (all lid angles, extensions, tilts): none
static conflicts with loops/corridor/controller keep-out/display: [('Wh1', 'controller(provisional)', 'touching boundary', 0.0)]
hinge: min lid/base clearance over 0-135 1.41; lid lowest z at 0/105/135: 42.0, 28.5, 8.5; rear overhang 105/135: 103.8/197.6; solar lowest z (deployed tilts) at 0/105/135: -54, 49, 9

--- B  one-piece, perimeter frame + 1.6 panel ---
lid thickness 31.5 (closed stack 73.5); back deflection LC1 49.81 / LC2 31.76 mm vs allowed 0.95; back-plate(+ribs) mass 144 g, edge beams 105 g
motion/stowed collisions (all lid angles, extensions, tilts): none
static conflicts with loops/corridor/controller keep-out/display: [('Wh1', 'controller(provisional)', 'touching boundary', 0.0)]
hinge: min lid/base clearance over 0-135 1.41; lid lowest z at 0/105/135: 42.0, 31.3, 16.3; rear overhang 105/135: 93.2/189.9; solar lowest z (deployed tilts) at 0/105/135: -54, 49, 9

--- C  two-piece: front frame + ribbed rear shell ---
lid thickness 42.5 (closed stack 84.5); back deflection LC1 0.49 / LC2 0.31 mm vs allowed 0.50; back-plate(+ribs) mass 315 g, edge beams 105 g
motion/stowed collisions (all lid angles, extensions, tilts): none
static conflicts with loops/corridor/controller keep-out/display: [('Wh1', 'controller(provisional)', 'touching boundary', 0.0)]
hinge: min lid/base clearance over 0-135 1.41; lid lowest z at 0/105/135: 42.0, 28.5, 8.5; rear overhang 105/135: 103.8/197.6; solar lowest z (deployed tilts) at 0/105/135: -54, 49, 9

C joint: M3 heat-set inserts (typ. envelope 4.5 x 5.7, boss 8) in the tops of the two edge beams (band width 14), 5 per band = 10 screws, M3 x ~9 through the 2.5 rear shell from outside; LC2 total 60 N -> 6 N per screw
```
