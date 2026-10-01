# Round C.2 — Final Architectural Screening before the D-007 Decision

**Status:** analysis only. D-007 stays **proposed**. No winner is selected and no alternatives are ranked.

**Model:** `CAD/tools/c2_screening.py`. The full grid is in `prototypes/P0.1/lid_hinge_port_map.csv`. Re-run with:

```bash
py CAD/tools/c2_screening.py --csv prototypes/P0.1/lid_hinge_port_map.csv
```

**Evidence levels:**
- *Modeled*: exact 2D/2.5D envelope geometry on working values, reusing the Round C base (`base_v01_layout.py`), the hinge model (`hinge_feasibility_2d.py`) and the B.1 V1 solar model with its minimal fixes (`solar_v1_feasibility.py`, unchanged).
- *Inferred*: judgement.
- Nothing is tested or measured.

**Status of the inputs:**

| Input | Standing |
|---|---|
| D-006 direction (hinge axis at the rear top edge, inset 0) | accepted, provisional |
| Hinge height h, closed gap 2.0, lid thicknesses, maximum angles | **working / what-if** |
| Rear plug zone Z 4–19, 45 mm behind the rear face; MIN_GAP 1.0 | **working** |
| Solar V1 geometry (lid 31.5, deploy travel 158, tilt ±75°) | B.1 working |
| Hand-access height 60 mm above a port | **assumption** |

## Task 1 — Lid / hinge / rear-port feasibility map (modeled)

**How to read the table:**
- A cell is the minimum clearance from the lid to the rear plug zone over the whole sweep from 0 up to that maximum opening angle.
- **✗** marks an infeasible cell: plug clearance < MIN_GAP, lid-to-base clearance < MIN_GAP, or the lid below ground.
- "Max feasible opening" is the largest angle (0.5° steps) at which every criterion still holds over the whole sweep.
- Heights 10 and 12 are included to show saturation.

| Lid T | Hinge h | Max feasible opening | 105° | 115° | 120° | 125° | 130° | 135° | Lid–base min |
|---|---|---|---|---|---|---|---|---|---|
| 25 | 0 | 137.5° | 14.01 | 9.59 | 7.50 | 5.51 | 3.65 | 1.91 | 1.41 |
| 25 | 2 | 150.0° | 16.53 | 12.44 | 10.50 | 8.66 | 6.93 | 5.32 | 1.41 |
| 25 | 4 | 165.5° | 19.05 | 15.28 | 13.50 | 11.81 | 10.22 | 8.74 | 2.00 |
| 25 | 6 | 170.0° | 21.57 | 18.12 | 16.50 | 14.96 | 13.50 | 12.15 | 2.00 |
| 25 | 8 | 172.5° | 23.00 | 20.97 | 19.50 | 18.10 | 16.79 | 15.56 | 2.00 |
| 25 | 10 | 174.0° | 23.00 | 23.00 | 22.50 | 21.25 | 20.07 | 18.98 | 2.00 |
| 25 | 12 | 175.0° | 23.00 | 23.00 | 23.00 | 23.00 | 23.00 | 22.39 | 2.00 |
| 27.5 | 0 | 132.5° | 13.37 | 8.53 | 6.25 | 4.08 | 2.04 | **0.14 ✗** | 1.41 |
| 27.5 | 2 | 143.0° | 15.88 | 11.38 | 9.25 | 7.23 | 5.32 | 3.56 | 1.41 |
| 27.5 | 4 | 160.0° | 18.40 | 14.22 | 12.25 | 10.37 | 8.61 | 6.97 | 2.00 |
| 27.5 | 6 | 170.0° | 20.92 | 17.07 | 15.25 | 13.52 | 11.89 | 10.38 | 2.00 |
| 27.5 | 8 | 172.5° | 23.00 | 19.91 | 18.25 | 16.67 | 15.18 | 13.80 | 2.00 |
| 27.5 | 10 | 174.0° | 23.00 | 22.76 | 21.25 | 19.82 | 18.47 | 17.21 | 2.00 |
| 27.5 | 12 | 175.0° | 23.00 | 23.00 | 23.00 | 22.96 | 21.75 | 20.63 | 2.00 |
| 30 | 0 | 128.5° | 12.72 | 7.48 | 5.00 | 2.65 | **0.43 ✗** | **-1.63 ✗** | 1.41 |
| 30 | 2 | 137.0° | 15.23 | 10.32 | 8.00 | 5.79 | 3.72 | 1.79 | 1.41 |
| 30 | 4 | 148.5° | 17.75 | 13.17 | 11.00 | 8.94 | 7.00 | 5.20 | 2.00 |
| 30 | 6 | 170.0° | 20.27 | 16.01 | 14.00 | 12.09 | 10.29 | 8.62 | 2.00 |
| 30 | 8 | 172.5° | 22.79 | 18.86 | 17.00 | 15.23 | 13.57 | 12.03 | 2.00 |
| 30 | 10 | 174.0° | 23.00 | 21.70 | 20.00 | 18.38 | 16.86 | 15.44 | 2.00 |
| 30 | 12 | 175.0° | 23.00 | 23.00 | 23.00 | 21.53 | 20.14 | 18.86 | 2.00 |
| 31.5 | 0 | 126.5° | 12.33 | 6.84 | 4.25 | 1.78 | **-0.53 ✗** | **-2.69 ✗** | 1.41 |
| 31.5 | 2 | 134.0° | 14.85 | 9.69 | 7.25 | 4.93 | 2.75 | **0.73 ✗** | 1.41 |
| 31.5 | 4 | 144.0° | 17.36 | 12.53 | 10.25 | 8.08 | 6.04 | 4.14 | 2.00 |
| 31.5 | 6 | 160.5° | 19.88 | 15.38 | 13.25 | 11.23 | 9.32 | 7.55 | 2.00 |
| 31.5 | 8 | 172.5° | 22.40 | 18.22 | 16.25 | 14.37 | 12.61 | 10.97 | 2.00 |
| 31.5 | 10 | 174.0° | 23.00 | 21.07 | 19.25 | 17.52 | 15.89 | 14.38 | 2.00 |
| 31.5 | 12 | 175.0° | 23.00 | 23.00 | 22.25 | 20.67 | 19.18 | 17.80 | 2.00 |
| 35 | 0 | 122.5° | 11.42 | 5.36 | 2.50 | **-0.22 ✗** | **-2.78 ✗** | **-5.16 ✗** | 1.41 |
| 35 | 2 | 128.5° | 13.94 | 8.21 | 5.50 | 2.92 | **0.50 ✗** | **-1.75 ✗** | 1.41 |
| 35 | 4 | 136.5° | 16.46 | 11.05 | 8.50 | 6.07 | 3.79 | 1.67 | 2.00 |
| 35 | 6 | 147.0° | 18.98 | 13.90 | 11.50 | 9.22 | 7.07 | 5.08 | 2.00 |
| 35 | 8 | 164.5° | 21.49 | 16.74 | 14.50 | 12.37 | 10.36 | 8.49 | 2.00 |
| 35 | 10 | 174.0° | 23.00 | 19.59 | 17.50 | 15.51 | 13.64 | 11.91 | 2.00 |
| 35 | 12 | 175.0° | 23.00 | 22.43 | 20.50 | 18.66 | 16.93 | 15.32 | 2.00 |
| 40 | 0 | 118.0° | 10.13 | 3.25 | **0.00 ✗** | **-3.09 ✗** | **-6.00 ✗** | **-8.70 ✗** | 1.41 |
| 40 | 2 | 123.0° | 12.65 | 6.09 | 3.00 | **0.06 ✗** | **-2.71 ✗** | **-5.28 ✗** | 1.41 |
| 40 | 4 | 129.0° | 15.16 | 8.94 | 6.00 | 3.20 | **0.57 ✗** | **-1.87 ✗** | 2.00 |
| 40 | 6 | 136.0° | 17.68 | 11.79 | 9.00 | 6.35 | 3.86 | 1.54 | 2.00 |
| 40 | 8 | 145.0° | 20.20 | 14.63 | 12.00 | 9.50 | 7.14 | 4.96 | 2.00 |
| 40 | 10 | 159.5° | 22.72 | 17.48 | 15.00 | 12.65 | 10.43 | 8.37 | 2.00 |
| 40 | 12 | 175.0° | 23.00 | 20.32 | 18.00 | 15.79 | 13.72 | 11.79 | 2.00 |
| 42.5 | 0 | 116.5° | 9.48 | 2.19 | **-1.25 ✗** | **-4.52 ✗** | **-7.60 ✗** | **-10.47 ✗** | 1.41 |
| 42.5 | 2 | 121.0° | 12.00 | 5.04 | 1.75 | **-1.38 ✗** | **-4.32 ✗** | **-7.05 ✗** | 1.41 |
| 42.5 | 4 | 126.0° | 14.52 | 7.88 | 4.75 | 1.77 | **-1.03 ✗** | **-3.64 ✗** | 2.00 |
| 42.5 | 6 | 132.0° | 17.04 | 10.73 | 7.75 | 4.92 | 2.25 | **-0.22 ✗** | 2.00 |
| 42.5 | 8 | 140.0° | 19.55 | 13.57 | 10.75 | 8.06 | 5.54 | 3.19 | 2.00 |
| 42.5 | 10 | 150.0° | 22.07 | 16.42 | 13.75 | 11.21 | 8.82 | 6.61 | 2.00 |
| 42.5 | 12 | 169.5° | 23.00 | 19.27 | 16.75 | 14.36 | 12.11 | 10.02 | 2.00 |
| 45 | 0 | 115.0° | 8.84 | 1.14 | **-2.50 ✗** | **-5.96 ✗** | **-9.21 ✗** | **-12.23 ✗** | 1.41 |
| 45 | 2 | 119.0° | 11.35 | 3.98 | **0.50 ✗** | **-2.81 ✗** | **-5.92 ✗** | **-8.82 ✗** | 1.41 |
| 45 | 4 | 123.5° | 13.87 | 6.83 | 3.50 | **0.34 ✗** | **-2.64 ✗** | **-5.41 ✗** | 2.00 |
| 45 | 6 | 129.0° | 16.39 | 9.67 | 6.50 | 3.48 | **0.65 ✗** | **-1.99 ✗** | 2.00 |
| 45 | 8 | 135.5° | 18.91 | 12.52 | 9.50 | 6.63 | 3.93 | 1.42 | 2.00 |
| 45 | 10 | 144.0° | 21.42 | 15.36 | 12.50 | 9.78 | 7.22 | 4.84 | 2.00 |
| 45 | 12 | 156.0° | 23.00 | 18.21 | 15.50 | 12.93 | 10.50 | 8.25 | 2.00 |

**Findings:**
- **Closed form** (plug long enough to reach the lid's hinge-end corner; θ > 90°):
  `port clearance ≈ H + h + (G + T − h)·cos θmax − port-zone top`.
  Hinge height adds almost 1 : 1 (partly offset by the cos θ term); lid thickness costs |cos θmax| per mm.
- **At h = 0** (today's working input), 135° is feasible only for T ≤ 26.3 (25: +1.91; 27.5: +0.14 ✗).
- **Lid-to-base clearance** is 1.41 for h = 0–2 and 2.00 for h ≥ 4. It is never the limiting term in this grid, which matches A.2/A.2b.
- **Every lid thickness in the grid has feasible combinations.** 135° needs (from the grid values):
  - h ≥ 2 for T 27.5–30;
  - h ≥ 4 for T 31.5–35 (31.5 at h 2 gives 0.73; C.1 found h 2.2 is enough);
  - h ≥ 6 for T 40;
  - h ≥ 8 for T 42.5–45.
- **With h fixed at 0,** the maximum opening shrinks to 137.5° / 132.5° / 128.5° / 126.5° / 122.5° / 118.0° / 116.5° / 115.0° for T 25 / 27.5 / 30 / 31.5 / 35 / 40 / 42.5 / 45.
- **Short plugs** (≤ 15 mm behind the face) are clear for all T (C.1). This map uses the 45 mm plug assumption.
- **Not assessed:** h is only a geometric axis position here. Whether hinge hardware can sit 2–8 mm above the base top at the rear edge, and the rear overhang it creates, are hinge-prototype questions (D-006).

## Task 2 — Side-port study (modeled; solar not redesigned)

**Zone checked:** port connector zone Z 4–19, plugs 45 mm outward, scanned in 5 mm slices along the full length of each side wall. Rear-face corners were checked too.

**Solar states checked:** 90 states of the B.1 V1 cassettes, each side:
- lid angles 0 / 60 / 90 / 105 / 120 / 135°;
- extension 0 / 0.25 / 0.5 / 0.75 / 1;
- at full extension, tilt −75…+75° in 15° steps.

| Check | Right side wall | Left side wall | Side/rear corner (rear face X 110–148, or side wall Y 207–232) |
|---|---|---|---|
| 1. Base-wall clearance (internal, Round C concept A layout) | **blocked along the whole length**: cooling duct / intake (Y 2.5–27.5), compute sled + Pi + exhaust zone (7.5–102.5), compute power (92.5–132.5), compute cable run (87.5–207.5), side boss (147.5–157.5), trunk (187.5–207.5), hinge-mount reserve (207.5–232.5) | **blocked**: battery bay (7.5–97.5), battery wall + power electronics (92.5–147.5), side boss (147.5–157.5), hinge-mount reserve (207.5–232.5). *Y 157.5–207.5 is internally free on the left* (GNSS sits at X ≤ −8.5) | blocked by the hinge-mount reserve and rear bosses (both sides); right also by the compute cable and trunk |
| 2. Lid sweep | never enters: the lid spans X ±150.5 = base width | same | rear face: same constraint as Task 1; side-wall corner: clear |
| 3. Stowed cassettes | inside the lid (X ≤ 148): clear | clear | clear |
| 4. Deployed cassettes | clear at lid ≥ 60° in every tilt. **Interferes (−5.0) only when deployed and tilted with the lid closed (0°)**, over Y 22.5–117.5 and 147.5–212.5 | same pattern (−5.0 at lid 0°) | clear at lid ≥ 60° |
| 5. Rail / carriage / pin / bracket / cable twist zone | included in check 4; the fixed rails stay inside the lid | same | same |
| 6. Cable routing | concept A: the right side is occupied by compute and its cable run; a side panel there would need the compute bay re-laid out | concept A: the left side is the battery and power bay; ports beside the battery conflict with its bay | corner: next to the hinge load path (D-007 separation rule) |
| 7. Service-panel access | same method as the rear panels is possible (notch open to the underside, panel slides in from below) | same | same |
| 8. Manufacturability | notch in a full-height side wall: no bridge in deck-down printing (as the rear notches) | same | corner notch weakens the wall pair that carries the hinge (inferred) |
| 9. Plugging with cassettes deployed (lid ≥ 90°) | cassette height above the port zone: front half (Y < 122) **nothing above**; Y 122–162: 155–161; 162–182: 69; rear third (Y > 182): **42–53** | front half nothing above; Y 122–142: 111; 142–162: 82; 162–182: 61; rear third **39–48** | 39–53 above the zone (side) |

**Feasible / infeasible zones:**
- **Externally** (lid + solar):
  - If cassettes are never deployed with the lid below 60°, the whole length of both side walls is clear.
  - If lid-closed deployment is allowed, the clear zones are Y 2.5–22.5, 117.5–147.5 and 212.5–232.5 (right), and Y 2.5–22.5, 87.5–117.5 and 212.5–232.5 (left).
  - Hand access above 60 mm (assumed) exists over the front two-thirds of both sides and is poor in the rear third (≈ 40–53 mm).
- **Internally, with today's concept A layout:** no side zone is feasible. Both palm bays and the under-keyboard modules sit against the side walls.
- **Consequence:** side I/O is geometrically available outside the base, but using it needs an internal re-layout. The only internally free side stretch is left Y 157.5–207.5, and its rear part has limited hand access.
- **Not assessed:** whether D-004 allows deployment with the lid closed.

## Task 3 — Print / manufacturing architecture (facts; nothing chosen)

**Envelope facts:**
- The shell footprint is 301 × 235 × 40.
- Diagonal placement needs a square bed of at least (301 + 235)/√2 ≈ 379, so it does not help.
- Round C modeled the one-piece shell deck-down with no overhang or bridge.
- Bed sizes below are the part footprint; add the slicer's skirt/brim margin, typically about 5 mm per side (inferred).

| | A. One-piece shell | B1. Split at the centreline (X = 0) | B2. Three pieces along the bulkhead planes (X ≈ ±49) | B3. Front/rear split at Y ≈ 95–97 | C. One-piece structural shell + removable non-structural underside | D. Split shell + separate metal rear spine and plate splices (other sensible strategy) |
|---|---|---|---|---|---|---|
| Minimum bed footprint | 301 × 235 | 2 × (150.5 × 235) | 2 wings 101 × 235 + centre 99 × 235 | 301 × ~96 + 301 × ~139 (width unchanged) | 301 × 235 | as B1 for the printed parts; the spine is cut or machined |
| Print orientation | deck-down | deck-down, split face vertical | deck-down | deck-down | shell deck-down; panels flat | deck-down |
| Supports | none (modeled) | none for the shell; horizontal joint holes need teardrop or self-supporting geometry (inferred) | same as B1 | same as B1 | none | none for printed parts |
| Structural joint | none | across the full depth: front wall, three deck strips (≈ 49 mm total at X = 0), the rear wall and a bisected front boss | two joints; bulkheads give bolting faces only for Y < 97; behind that the joint crosses only the rear deck strip and rear wall | along the battery wall / keyboard-tray front / bulkhead ends (existing internal walls) | none in the shell; panels screwed to bosses | as B1, but the metal spine carries the rear span |
| Joint in a primary load path? | — | **yes**: mid-span of the base under handling bending and across the rear span between the two hinges (inferred) | **yes**, rear span between the hinges (inferred) | **no** for hinge loads (all behind the joint); **yes** for palm and handling loads (inferred) | — (see note) | hinge-to-hinge path moved to metal; printed joint secondary (inferred) |
| Keyboard / trackpad mounting | unaffected | joint runs under the keyboard and trackpad openings; the trays span both halves (they can act as splice plates, but add a tolerance stack) | joints under the keyboard opening | joint on the keyboard-tray front edge; trackpad wholly in the front part | unaffected | as B1; trays or spine as splices |
| Battery / service panel | unaffected | battery door wholly in the left half; the main panel spans both halves | battery door in the left wing; the main panel spans three pieces | battery bay in the front part; its wall is on the joint; the main panel spans both | unaffected; battery door separate | as B1 |
| Serviceability | unchanged (open bottom) | unchanged (the joint is not a service seam) | unchanged | unchanged | unchanged | unchanged |
| Assembly complexity | lowest part count | +1 printed part + joint fasteners and alignment features | +2 printed parts + two joints | +1 printed part + joint | as A (this is D-007 as modeled) | +1 printed part + metal part(s) + fasteners |

**Note on C:** if the underside panels are *non-structural*, the shell alone carries torsion as an open-bottom section, which is torsionally weak (inferred). Screwed panels close the section. Whether they count as structure is a design choice, not modeled here.

## Task 4 — Final architectural decision set (facts for the owner)

**1. Constraints now understood well enough to lock as constraints** (not as values):
- **The rear-port / lid / hinge coupling:** the closed form above and the Task 1 map. Any lid architecture with rear ports must lie in the feasible region of (T, h, θmax, port-zone top, plug length).
- **The lid never reaches a side port zone** (the lid is as wide as the base).
- **Deployed V1 cassettes** clear side port zones at lid ≥ 60°. They interfere only when deployed and tilted with the lid closed.
- **At a body height of 40,** only the palm-rest bays offer 35 mm of height; under the keyboard 26.5 (C / C.1).
- **The open-bottom service strategy** (straight-down removal, separate battery door, keyboard and trackpad lift out) is geometrically consistent (C).
- **Lid-to-base clearance** at inset 0: 1.41 for h 0–2, 2.00 for h ≥ 4.
- **Printing:** a one-piece shell needs a ≥ 301 × 235 bed. Getting under 250 needs a split along X, which puts a joint across the rear hinge span and under the keyboard.

**2. Still uncertain** (working assumptions):
- The real Pi stack height.
- Lid thickness (display + controller + solar rail layer + back plate).
- Hinge axis height and hardware; maximum opening angle.
- Plug types and lengths; the external port set.
- Battery energy and volume (from a measured power budget).
- Palm-rest temperature; masses and tip-back.
- Whether solar deploys with the lid closed.
- Joint stiffness of printed PETG splits; the print service's bed size.

**3. Can D-007 reasonably be accepted as a working architecture after C.2?** The facts that bear on this:
- **For:**
  - It passes every Round C check at the working envelope.
  - The kernel cross-check matches the local model exactly.
  - Its rear-I/O dependency has a known feasible design envelope (Task 1) instead of an open question.
- **Implicit commitments:**
  - **Rear I/O.** Its internal layout occupies both side walls, so side I/O would need a re-layout (Task 2).
  - A lid that stays inside the Task 1 feasible region.
  - A GNSS module that is not stacked.
- **Separable:** the print split (Task 3) is independent of the placement, except that a split puts joints under the keyboard and across the hinge span.

Accepting D-007 as a *working, parametric* architecture is therefore geometrically supported, provided those implicit commitments are accepted with it. Whether to accept is the owner's decision.

**4. Remaining decisions before creating the persistent Base V0.1 Feature Studio:**
1. D-007 placement (compute right palm bay, battery left bay, electronics under the keyboard): accept as working, amend, or reject.
2. I/O policy: rear panels (recording the Task 1 feasible region as a requirement on the lid/hinge work) or side panels (needs an internal re-layout first).
3. GNSS as a separate cabled module (working assumption).
4. Solar operating rule: whether deployment with the lid closed is allowed. This only matters for side I/O.
5. Base shell structure in the feature: one BASE_SHELL body (A/C) or split bodies (B/D). The two give different part lists in Onshape.
6. Body envelope for V0.1: keep working 301 × 235 × 40.
7. Confirmation that the persistent feature is a regenerable parametric envelope model.

**5. The single study that would most reduce risk:**
- **What:** a lid stack-up study. Build the lid cross-section from the display module, controller, the B.1 V1 solar rail layer and cassette, and the back structure (B.2 Concept C ribs), to get a defensible lid thickness T.
- **Why:** T is the input shared by the Task 1 port feasibility, the hinge-height requirement, the lid-structure screening (B.2) and the closed thickness.
- **Limit:** it is a geometry study. The hinge height and the Pi stack still need the physical prototype and measurement.
