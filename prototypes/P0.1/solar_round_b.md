# P0.1 Round B: Solar Cassette Kinematic Skeleton (initial analysis)

**Status: modeled, P0.1 working geometry. No solar rail architecture has been chosen.** Kinematic envelopes only: cassette body, hub pin, carriage and fixed-rail keep-out. No hardware, panels or motors. D-004 kinematics are assumed throughout: lateral slide out of the lid, tilt about an axis along the slide direction, rail carries structural load, hub pin carries rotation, indexed tilt.

## Method

- **Model:** `CAD/tools/solar_skeleton_model.py`. It is an exact prism model: every body is an X-interval times a Y–Z polygon, because the lid and the cassettes only rotate about X-parallel axes and only slide along X. It reuses the hinge model code that was validated against Onshape.
- **Geometry:** working inputs from `nomad.yaml`, with the D-006 hinge (rear face, 2.0 mm closed gap).
- **States checked:**
  - lid at 0°, 105° and 135°
  - left/right slide extensions 0–1 in quarter steps, in every combination
  - deployed tilt −75°…+75° in 5° steps, with index positions every 15°
- **Rules:** clearance ≥ MIN_GAP (1.0) for all non-attached pairs, and the table at z = 0.
  - Rail contact with lid walls is allowed, because a fixed rail can be integral with the lid.
  - Where the cassette and pin cross the lid side wall, that crossing is reported as a required wall opening, not as a collision.
- **Layouts:**
  - **V0:** the current working values: hub axis at the cassette mid-plane, rail coaxial with the hub, both sides mirrored.
  - **V1, V2:** evaluated *only because V0 fails*, each at the minimum lid thickness or cassette height it needs.
- **Onshape cross-check:** one scratch run (9 API requests) rebuilt V0 with the production FeatureScript builder (`nomadBuildSolarSide`) in six states. It matched the model exactly: the same overlapping pairs in every state and the same minimum heights (50.8, 50.8, 6.0, −14.0, 55.8, 20.7).

## Model output

```
=== Travel budget (single-stage carriage, any layout) ===
required cassette travel S = 155 (cassette fully outside lid + 5 clearance)
carriage always sits inboard of the cassette by engagement 40 + link 8.5 = 48.5
rail length needed per side = 195 (x -48 .. 147)
rail length available inside own half = 146.5  ->  available carriage travel 106.5 vs required 155: shortfall 48.5; each rail must cross the centreline by 48

=== V0  (lid T=25, cassette 147.5 x 200 x 8) ===
hub axis (lid frame y, z above display face): R 117.5, 17.5   L 117.5, 17.5;  cassette z 13.5-21.5, y 17.5-217.5;  lid inner z 0-22.5
side-wall opening needed (each side): 202.0 (Y) x 10.0 (Z), from z 12.5 above display face
slide/stowed violations (pair: worst clearance, mm): RL-RR -13.0, CL-RL -8.0, CL-RR -8.0, CR-RL -8.0, CR-RR -8.0, CL-KR -8.0, CR-KL -8.0, KL-RR -8.0, KR-RL -8.0, KL-KR -8.0, PL-RR -5.0, PR-RL -5.0, CL-PR -5.0, CR-PL -5.0, KL-PR -5.0, KR-PL -5.0, PL-PR -1.0
lid   0.0: reachable tilt from 0 = -30..30 deg (index positions ok: [-30, -15, 0, 15, 30]); solar min z over sweep -38.1, at 0 deg +53.0; cassette collisions: none (ground only)
lid 105.0: reachable tilt from 0 = -75..75 deg (index positions ok: [-75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75]); solar min z over sweep +48.4, at 0 deg +50.8; cassette collisions: none
lid 135.0: reachable tilt from 0 = -75..75 deg (index positions ok: [-75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75]); solar min z over sweep +9.3, at 0 deg +35.8; cassette collisions: none
extents at lid 105: stowed overall X 301.0; deployed overall X 606.0 (cassette outer edges at +/-303.0)

V1 needs lid thickness >= 31.5 (current 25); V2 needs cassette height <= 194 (current 200)

=== V1  (lid T=31.5, cassette 147.5 x 200 x 8) ===
hub axis (lid frame y, z above display face): R 126.5, 12.5   L 108.5, 12.5;  cassette z 20.0-28.0, y 17.5-217.5;  lid inner z 0-29.0
side-wall opening needed (each side): 202.0 (Y) x 20.0 (Z), from z 9.0 above display face
slide/stowed violations: none (all lid angles, extensions 0..1 in quarters, both sides)
lid   0.0: reachable tilt from 0 = -30..30 deg (index positions ok: [-30, -15, 0, 15, 30]); solar min z over sweep -48.8, at 0 deg +48.0; cassette collisions: none (ground only)
lid 105.0: reachable tilt from 0 = -75..75 deg (index positions ok: [-75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75]); solar min z over sweep +48.4, at 0 deg +49.1; cassette collisions: none
lid 135.0: reachable tilt from 0 = -75..75 deg (index positions ok: [-75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75]); solar min z over sweep +9.2, at 0 deg +31.2; cassette collisions: none
extents at lid 105: stowed overall X 301.0; deployed overall X 606.0 (cassette outer edges at +/-303.0)

=== V2  (lid T=25, cassette 147.5 x 194 x 8) ===
hub axis (lid frame y, z above display face): R 224.0, 16.0   L 11.0, 16.0;  cassette z 13.5-21.5, y 20.5-214.5;  lid inner z 0-22.5
side-wall opening needed (each side): 208.0 (Y) x 10.0 (Z), from z 12.5 above display face
slide/stowed violations: none (all lid angles, extensions 0..1 in quarters, both sides)
lid   0.0: reachable tilt from 0 = -15..15 deg (index positions ok: [-15, 0, 15]); solar min z over sweep -139.2, at 0 deg +51.5; cassette collisions: none (ground only)
lid 105.0: reachable tilt from 0 = -75..75 deg (index positions ok: [-75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75]); solar min z over sweep +36.1, at 0 deg +36.1; cassette collisions: none
lid 135.0: reachable tilt from 0 = -15..50 deg (index positions ok: [-15, 0, 15, 30, 45]); solar min z over sweep -71.5, at 0 deg +24.4; cassette collisions: none (ground only)
extents at lid 105: stowed overall X 301.0; deployed overall X 606.0 (cassette outer edges at +/-303.0)
```

Codes: C = cassette, R = rail keep-out, K = carriage, P = hub pin; suffix R/L = right/left side. Wb/Wf/Wr = lid back plate, front wall and rear wall; D = display; B = base.

## Findings (modeled)

1. **Travel.**
   - The required travel is 155 mm: the cassette must fully leave the lid, plus a 5 mm deploy clearance, before it can tilt about an axis along the slide.
   - A single-stage carriage always sits 48.5 mm inboard of its cassette (40 engagement + 8.5 link).
   - Each rail must therefore be 195 mm long, but only 146.5 mm is available in its own half of the lid. That is 106.5 mm of carriage travel against the 155 required.
   - **Each rail must cross the centreline by 48 mm.**
2. **The current working layout (V0) is geometrically impossible.**
   - The two stowed cassettes fill the lid's entire inner width in their layer, so a rail at the cassette mid-plane runs through both stowed cassettes (−8 mm).
   - The mirrored left and right rails occupy the same space in the crossing zone (−13 mm).
   - Carriages and pins also hit the opposite cassette.
   - None of these conflicts depends on lid angle.
3. **The D-004 kinematics are feasible once the rail leaves the cassette layer.** Two envelope-level layouts pass every slide and stowed state:
   - **V1:** a rail layer between the display and the cassettes, with the left and right rails staggered in Y. It needs the lid to be **31.5 mm thick instead of 25 (+6.5)** with the working carriage (12 × 8) and rail walls (2.5). This thickness scales directly with the rail cross-section.
   - **V2:** rails in edge bands beside the cassettes, right rail in the rear band and left rail in the front band. It needs **cassettes 194 mm tall instead of 200 (−6)**. The hub axis then sits beyond the cassette edge, which cuts the reachable tilt to ±15° with the lid closed and −15…+50° at 135°.
4. **Tilt sweep.**
   - With the hub at or near the cassette mid-height (V0, V1), the full ±75° is reachable at lid 105° and 135°.
   - With the lid closed (0°) the table limits tilt to ±30° (index positions ±15 and ±30). At ±45° the cassette edge would sit 14 mm below the table.
   - No cassette ever collides with the lid or base when deployed, because it is laterally clear of both by ≥ 5 mm.
5. **Required side-wall opening** (each lid side wall), because the whole cassette slides out through it:
   - V0 and V2: 202–208 × 10 mm in a 25 mm wall.
   - V1: 202 × 20 mm in a 31.5 mm wall. Most of the side wall's height is open along ~200 mm, which is a structural concern for the lid frame. *(inferred, not analysed)*
6. **Extents:** 301 mm wide when stowed; **606 mm across both deployed cassettes.**
7. **Not evaluated:** loads, wind, rail play, lock geometry, cable path through the hub, and the display controller. The controller would compete with V1's rail layer for the space behind the display.