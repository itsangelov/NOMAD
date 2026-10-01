# Round E — F3 Investigation: Hub Bracket vs Solar Rail Floor

> **SUPERSEDED / DEFERRED FOR NOMAD V1 (D-010, 2026-10-01).** This record belongs to **Architecture A** (sliding/tilting solar cassettes and their lid, D-004 / D-009). The owner selected **Architecture B1** (one solar leaf behind the display lid) as the active V1 architecture. The content below is kept unchanged as an engineering record and possible later reference; it does not describe the V1 design. See `docs/decisions.md` D-010 and `docs/v1-requirements.md`.

> **F3 APPROVED AND IMPLEMENTED — OPTION B** (2026-09-26).
> - The owner approved option (b): tilt axis +2.0 mm and a carriage slot boss.
> - It is implemented in `nomad.yaml`, `e_lid_layout.py` and the persistent Onshape Feature Studio `NOMAD_E_Prototype`.
> - See **§10 Implementation record**. §1–§9 below are the original investigation, kept unchanged.

**Status at investigation time:** analysis only, for owner review. Nothing in the model had changed:
- `nomad.yaml`, the production FeatureScript, Onshape and Git are untouched;
- no fix is implemented;
- E3 / E4 / E7 have not started.

**Tool:** `CAD/tools/f3_investigation.py`, a NON-PRODUCTION diagnostic.
- It imports the exact E2 lid model (`e_lid_layout.py`) read-only and rebuilds each variant in memory.
- It then re-runs the E2 check set on every variant (below).
- It writes nothing. Reproduce with `py CAD/tools/f3_investigation.py` (about 5 minutes).

**Check set run on every variant:**
- moving parts at lid 0 / 105 / 120 / 135° × stowed / R / L / both deployed;
- tilts ±75° in 15° steps, same and opposite;
- slides in 1/40 steps;
- bracket to floor every 0.1 mm of travel;
- lid sweep 0–135° against the base, rear plugs, table.

**Evidence levels:**
- **Geometry and clearances:** *modeled*. This is the E2 machinery, which matched the Onshape kernel exactly at E2.
- **Loads and stresses:** *inferred*. They are hand estimates under the stated assumptions, used only to compare variants. No FEA; nothing is physically tested.

All coordinates are world coordinates, lid closed, right side; the left side is its mirror image.

---

## 1. Problem definition

**What E2 found.** The B.1 hub-bracket envelope sits 1.0 mm inside the solar rail channel floor wherever the bracket is inside the rail length. B.1 had classed the bracket–rail pair as "attached" and never checked it.

**Objective.** Remove the interference with a mechanically sound change. It should keep the architecture intact:
- cassette 200 × 147.5 × 8, carriage 22.6 × 8 × 40, travel 158, ±75° tilt;
- Ø5 pin, 8 mm deploy clearance;
- staggered rails, 8 mm corridor;
- the rail as the load path, and gears for positioning only;
- lid thickness, printability and serviceability.

## 2. Current geometry (E2)

| Item | Geometry (right side, stowed) |
|---|---|
| Rail (C-channel) | X −51…147 (end stop −53.5…−51), Y 121.5–149.1 (27.6), Z 49–62 (13). Floor Z 49–51.5, walls 2.5, lips Z 59.5–62, slot Y 126.5–144.1 (17.6) |
| Carriage | X −51…−11, Y 124–146.6 (22.6), Z 51.5–59.5 (8), centred on the hub axis. It fills the channel from the floor to the lips |
| Hub axis / pin | Y 131.8, **Z 55.5** (rail-layer mid-height, B.1 formula `0 − (MIN_GAP + RLH/2)` → −7.5 from the cassette bottom). Pin Ø5, Z 53–58, spans the link X −11…0.5 |
| Hub bracket | X 0.5–10.5, Y 126.8–143.8 (17 = pin + gap + cable + 2 walls), **Z 50.5**–63. Bottom = axis − pin radius 2.5 − wall 2.5 |
| Cassette | X 0.5–148, Z 63–71 |

**Vertical stack at the pin (E2):**

| Region | Z 49–51.5 | Z 51.5–53 | Z 53–58 | Z 58–62 | Z 62–63 | Z 63+ |
|---|---|---|---|---|---|---|
| Bracket (X 0.5–10.5) | rail floor | bracket wall 50.5–53, **1.0 inside the floor** | pin | bracket | bracket | own cassette |
| Carriage (X −51…−11) | rail floor | carriage 1.5 | pin | carriage 1.5, then **4.0 mm of empty slot above the pin** (to the rail top) | gap | the *other* cassette (stowed) |

## 3. The interference (script part A; modeled)

- **Surfaces:** the bracket's bottom face (Z 50.5) and the rail floor's top face (Z 51.5). Penetration is **1.00 mm** across the full 17 mm bracket width.
- **Other rail features around the bracket:** walls 2.8 mm away, lips 0.3 mm (the designed CLEARANCE slot fit), end stop 51.5 mm away. Only the floor is involved.
- **Along the travel:**
  - the depth is constant; only the overlapped length changes;
  - full 10 mm overlap (170 mm³) from 0 to 136.5 mm of slide, tapering to zero at 146.5 mm;
  - the bracket is clear for the last 11.5 mm (exactly the hub link length) and when deployed;
  - **93 % of the travel is affected.**
- **Tilt:** no tilt happens inside the rail (the lid slot captures the cassette), so tilt does not affect F3.
- **Shaping the bracket does not help.** A round-bottomed boss (r 5) still penetrates 1.00 mm over a 6.0 mm chord. Rounding, chamfering, lateral moves or asymmetry cannot remove F3; §5 explains why.

## 4. What the bracket is and what it carries (inferred)

**Role.** The E2 bracket is an envelope for a real **structural hub**. It is the **only** connection between the cassette and the pin once the cassette is deployed.
- Deployed load path: cassette → bracket bore → pin → carriage → rail (floor, lips, walls) → pad → lid frame.
- Stowed and sliding: the lid slot guides the cassette, and the bracket only transmits the push/pull.

**Load assumptions** (the cassette is not selected):
- **G:** cassette weight 2.45 N (0.25 kg) at the cassette centre.
- **H:** 10 N at the outboard edge (handling or gust), perpendicular to the axis.

**Loads on the bracket bore (10 long, Ø5):**
- Moment: 169 N·mm (G) and 1425 N·mm (H).
- End reactions: 25 N and 214 N; peak bore pressure 2.0 and 17.1 MPa.
- Worst direction (lid 0°, deployed, gravity): at the **inboard end of the bore** the pin bears on the **wall under the pin**. That is exactly the wall F3 concerns, so it is structural, not spare material.

**Bore-wall bending index** (the wall as a strip across the bore; for comparison only):

| Wall under the pin | Case G | Case H |
|---|---|---|
| 2.5 mm | 6.1 MPa | 51 MPa |
| 1.5 mm | 16.9 MPa | 142 MPa |
| 1.2 mm | 26.3 MPa | 223 MPa |
| 0.5 mm | 152 MPa | 1283 MPa |

Nominal PETG is about 45 MPa in-layer and 25 MPa across layers. The index scales with 1/t².

**Pin bending** at the carriage exit: 17 MPa (G) and 130 MPa (H) for Ø5. Ø4 is 1.95× and Ø3 is 4.6× higher.

**Material that could be removed:** the bracket envelope's lower corners outside the bore circle, and the region under the cable path (the cable turns up into the cassette). Removing them does not affect F3, because the bore bottom alone penetrates.

## 5. Root cause: the vertical budget below the tilt axis (script part B)

| | mm |
|---|---|
| Available: axis Z 55.5 − floor top Z 51.5 (= half the carriage height, because the axis is at mid-height) | **4.0** |
| Needed: pin radius 2.5 + bracket wall 2.5 + running gap MIN_GAP 1.0 | **6.0** |
| **Deficit** | **2.0** to MIN_GAP (1.3 to a CLEARANCE 0.3 fit; 1.0 just to reach contact) |

**Consequences:**
- Every real fix must recover 2.0 mm in this one vertical stack. There are only four ways to do it:
  1. less material under the pin;
  2. a higher axis;
  3. a lower floor;
  4. a smaller pin.
- **Where the room is:** there are 4.0 mm of empty height **above** the pin (pin top Z 58 to the rail top Z 62). The limit up there is the *other* cassette, stowed above the link at Z 63, less MIN_GAP. B.1 put the axis at mid-height for carriage symmetry and left this surplus unused.
- **Correction to the E2 report:** options (a) "1.5 mm wall" and (c) "+1 mm channel (38.6 lid)" only reach **contact (0.0)**, not MIN_GAP. The corrected values are in §6.

## 6. Alternatives investigated

All geometry below comes from the full E2 check set in `f3_investigation.py`. Every variant built has 0 rigid overlaps and 0 unexpected moving-part violations; the table lists what differs.

### Quantitative comparison (modeled)

| Variant | Bracket–floor, min over travel | Lid T / closed height | Rear plugs at 120° / first below MIN_GAP | Walls around pin: bracket below / carriage below / above | Stowed to other cassette: pin / carriage / cable | Lowest tilted cassette, lid 105–135° | Rail Iy / J |
|---|---|---|---|---|---|---|---|
| E2 baseline | **−1.00** | 37.6 / 79.6 | +1.20 / 121° | 2.5 / 1.5 / 1.5 | 5.0 / 3.5 / 4.5 | 7.8 | 1.00 / 1.00 |
| A1: wall 1.5 | 0.00 (contact) | 37.6 | same | 1.5 / 1.5 / 1.5 | same | 7.8 | 1.00 |
| A2: wall 0.5 | +1.00 | 37.6 | same | **0.5** / 1.5 / 1.5 | same | 7.8 | 1.00 |
| **B: axis +2.0 + carriage boss** | **+1.00** | **37.6 / 79.6** | **same (+1.20 / 121°)** | **2.5 / 3.5 / 2.0** | 3.0 / 1.0 / 2.5 | 6.5 | **1.00 / 1.00** |
| C1: channel +2, pin centred | 0.00 (contact) | 39.6 / 81.6 | +0.20 / 119° | 2.5 / 2.5 / 2.5 | 6.0 / 3.5 / 5.5 | 6.9 | 1.47 / 1.07 |
| C2: channel +4, pin centred | +1.00 | **41.6 / 83.6** | **−0.80 / 118°** | 2.5 / 3.5 / 3.5 | 7.0 / 3.5 / 6.5 | 5.9 | 2.06 / 1.15 |
| D: floor groove 2.0 | +1.00 | 37.6 | same | 2.5 / 1.5 / 1.5 | same | 7.8 | **0.76 / 0.65**, floor **0.5** |
| E: saddle-clamped pin | +1.50 | 37.6 | same | **0 (open)** / 1.5 / 1.5 | same | 7.8 | 1.00 |

**Notes on the table:**
- Every variant that clears the floor has a bracket-to-slot minimum of 0.3 mm. That is the designed CLEARANCE fit of the bracket in the 17.6 mm slot, not a collision.
- The side-wall strip under the notch grows from 7.5 mm (E2) to 9.5 mm (A2, B, C2), 8.5 mm (A1, C1) or 10 mm (E).
- The rear plug at 135° stays at −6.6 in every variant. That number is the depth measured normal to the lid's hinge-side end face, which does not change with lid thickness. Thickness shows up in the onset angle and the 120° value instead. It also shows in how far the lid's lowest point drops below the plug-zone top at 135°: 7.0 mm for E2 and B, 9.8 mm for C2.
- **Table at lid 0°** (tilt +30 / −45 / +75 / −75):

| Variant | Lowest point above the table (mm) |
|---|---|
| E2 | 4.8 / 0.2 / −53.0 / −25.3 |
| B | 5.1 / 0.8 / −51.5 / −23.9 |
| C2 | 8.6 / 3.6 / −50.4 / −22.8 |

  The known operating limit is unchanged in character.

### (A) Thin the bracket wall under the pin
- **Geometry:**
  - 1.5 mm gives contact only.
  - 0.5 mm is the largest wall that meets MIN_GAP; 1.2 mm with only a CLEARANCE 0.3 running fit.
  - Nothing else changes.
- **Effects:**
  - rail, cassette, travel, rotation, lid thickness and cable routing: unchanged;
  - hub strength: the wall that carries the inboard bore reaction becomes 2.8× (1.5), 4.3× (1.2) or 25× (0.5) more stressed. In case H that is 142–1283 MPa against 25–45 MPa PETG.
- **FDM:** a 0.5 mm wall is about one perimeter; 1.2 mm is three perimeters over a Ø5 bore.
- **Likely failure:** the wall splits or creeps under the pin at the bore's inboard end; the cassette droops, then detaches.
- **Confidence it works:** low. It passes the collision checker but fails the structural intent. **Rejected.**

### (B) Raise the tilt axis 2.0 mm and give the carriage a boss in the slot (recommended)
- **Geometry:**
  - The axis moves Z 55.5 → **57.5**; the pin moves to Z 55–60.
  - The bracket keeps its 2.5 mm wall and moves to Z **52.5**–63, 1.0 above the floor.
  - The carriage **body is unchanged** (22.6 × 8 × 40, Z 51.5–59.5), but is now referenced to the channel rather than the axis.
  - A **boss** 17.0 wide × 2.5 tall × 40 long rises through the slot to the rail top (Z 59.5–62), so the pin has a 2.0 mm (= MIN_WALL) wall above it.
  - The cable run (Z 54.5–60.5) and the side-wall notch bottom (Z 51.5) follow the axis.
- **Rail:** unchanged in section, Iy, J and floor thickness.
- **Hub strength:**
  - the bracket wall stays at 2.5;
  - the bracket's drop from the cassette to the axis shortens from 7.5 to 5.5, so the bracket is stiffer;
  - carriage walls around the pin go from 1.5 / 1.5 to **3.5 / 2.0**; the top wall's bending index falls 44 %;
  - cable channel walls in the carriage go from 1.0 / 1.0 to 3.0 / 1.5;
  - gravity torque the index lock must hold falls about 6 % (CoG lever 18.4 → 17.2 mm).
- **Cassette:** position unchanged, stowed and deployed.
- **Rotation (±75°):** clear at every index position. The axis is 2 mm nearer the cassette:
  - lid 0°: table clearance improves by 0.3–1.5 mm;
  - lid 105–135°: the lowest tilted-cassette point drops from 7.8 to 6.5 (lid 135°, tilt −45°).
- **Travel, lid thickness, stagger, corridor:** unchanged.
- **Cable routing:**
  - the cable run moves up 2 mm, still inside the carriage and slot;
  - the service loops (full rail-layer height) are unchanged;
  - the tilt-joint twist zone moves with the axis but stays at least 1.0 mm clear in X of every lid, base, rail and carriage part (X 151.5–157.5, between the lid face at 150.5 and the cassette at 158.5).
- **Margins that shrink:**
  - boss to the other stowed cassette: 3.5 → **1.0**, the same as the rail top everywhere;
  - pin: 5.0 → 3.0; cable: 4.5 → 2.5.
- **Budget:** the rail-layer height is now **exactly used**: floor 2.5 + gap 1.0 + bracket wall 2.5 + pin 5.0 + boss wall 2.0 = 13.0.
- **FDM:** a T-profile carriage, best printed standing on its end (bore vertical, round, no supports); on its side it needs a teardrop bore. The bracket and rail are unchanged, so the P0.2 rail coupons stay valid.
- **Assembly and service:** unchanged. The boss passes the slot exactly as the bracket does, and the carriage inserts from a rail end as in E2.
- **Likely failure:**
  - the boss binds in the slot if the slot prints narrow or the rail twists (0.3 mm fit per side); the boss only needs about 9 mm for the pin bore plus walls, so it can be narrowed to about 12–13 mm with an open cable channel if P0.2 shows binding;
  - the zero-spare budget means any growth in the pin or walls needs a thicker rail layer.
- **Confidence:** high for the geometry (fully swept); medium-high for the structure (every wall improves or stays the same; inferred).

### (C) Deepen the channel (thicker lid), pin centred
- **Geometry:**
  - With the pin centred, the carriage needs to be 12 mm tall (pin + 2 × (2.5 + 1.0)).
  - That makes the rail layer 17 and the **lid 41.6 (+4.0)**; the closed height becomes 83.6.
  - The +2 version (lid 39.6) only reaches contact.
- **Rail:** stronger (Iy 2.06×).
- **Hub:** carriage walls 3.5 / 3.5.
- **Cassette:** 4 mm further from the display.
- **Rear-port conflict worsens:** below MIN_GAP from 118° instead of 121°; −0.8 at 120°.
- **Lid window:** 41.6 is near the upper edge of the D.1 window (about 37.5–42) and against the owner's aim not to thicken the lid.
- **FDM and assembly:** fine.
- **Confidence:** high that it works; high cost. **Not recommended.**

### (D) Relief groove in the rail floor
- **Geometry:** a 2.0 mm deep groove along the full 146.5 mm bracket path leaves a **0.5 mm floor**:
  - under the square bracket (19 mm wide): the carriage bears on only 3.6 of its 22.6 mm width;
  - under a round boss only (8.9 mm wide): 13.7 mm of bearing width.
- **Rail:**
  - Iy 0.76× (or 0.91×) and open-section torsion J 0.65× (or 0.83×);
  - a notch-like stress concentration along the main structural member;
  - the carriage's sliding face is interrupted.
- **FDM:** a 0.5 mm floor is about 2 layers; it prints, but it is weak and sensitive to print quality.
- **Likely failure:** the floor cracks along the groove edge, the carriage rocks or wears into the groove, and the rail twists under deployed loads.
- **Confidence:** low. This weakens the primary load path, contrary to constraint 15. **Rejected.**

### (E) Saddle bracket: pin clamped in the bracket, bearing moved to the carriage
- **Geometry:**
  - The bracket wraps the top ~240° of the pin and is clamped (grub screw on a pin flat).
  - The bracket's lowest point is Z 53.0, 1.5 above the floor.
  - The pin then rotates in the carriage bore.
- **Effects:**
  - no global change;
  - the carriage walls stay 1.5 / 1.5;
  - the bore is open underneath, so the critical inboard reaction (pin bearing downward on the bracket, the §4 worst case) is carried by the saddle arms and the clamp, not a closed ring;
  - it needs a flatted pin and a clamp screw in PETG, which creeps.
- **Likely failure:** the clamp loosens and the cassette rotates or droops; the arms spread.
- **Confidence:** medium-low. It changes the joint concept for no geometric gain over B. **Rejected.**

### (F) Smaller pin
- **Effect:** Ø4 gives −0.5 (still interfering); Ø3 gives only contact.
- **Strength:** pin bending stress rises 1.95× (Ø4) or 4.6× (Ø3), which is 600 MPa in case H for Ø3. It also violates the Ø5 constraint. **Rejected.**

### Also considered and rejected
- **(G) Bracket as a second skid on the floor** (planned contact, 1.5 wall): it over-constrains the part, because the carriage bore and bracket bore share one pin and both would reference the floor. It binds with print tolerance and still thins the structural wall 2.8×.
- **(H) Axis above the rail** (hub in the cassette layer): geometrically impossible. The link and pin run under the *other* stowed cassette, so the pin top must stay at or below Z 62; the axis can rise at most 4.0 mm.
- **(I) Thin metal hub-bracket insert** (steel at 0.5 / 1.2 mm under the pin): at 1.2 mm the case-H index is about 223 MPa, marginal for mild steel. It adds a custom non-printed part and fasteners, and the clearance margin stays at 0.3–1.0. Kept as a fallback only.
- **(J) A local rail opening, or changing where the bracket enters:** the bracket is in the channel for 93 % of the travel. A local opening either doesn't help, or becomes (D) along the full length.
- **(K) A separate rotating hub block between carriage and bracket:** any rotating part in the channel faces the same 4.0 mm budget below the axis. It adds parts without creating height.

## 7. Recommendation

1. **Recommended solution:** **(B)**. Raise the hub/tilt axis 2.0 mm, from the rail-layer mid-height to the height set by the bracket-wall budget. Give the carriage a boss up through the rail slot so the pin keeps at least MIN_WALL of carriage above it.
2. **Why:**
   - It is the only option that removes F3 at full MIN_GAP while keeping every constraint: rail section, floor, lid thickness, cassette, travel, ±75°, pin Ø5, stagger, corridor and bracket wall.
   - It uses height that already exists (4.0 mm empty above the pin) instead of thinning structure or thickening the lid.
   - It strengthens the carriage–pin joint (1.5 / 1.5 → 3.5 / 2.0), gives the cable channel thicker walls, shortens the bracket, and adds slot guidance to the carriage.
   - The costs are modest and within the rules: stowed margins to the other cassette at 1.0 = MIN_GAP (as the rail top already is), lowest tilted cassette at 105–135° 6.5 instead of 7.8, and a zero-spare budget in the rail layer.
3. **Exact geometry changes** (world, right side; left mirrored):

| Item | E2 | Proposed |
|---|---|---|
| Hub / tilt axis Z | 55.5 | **57.5** |
| Pin | Z 53–58 | Z 55–60 (Ø5, same X span) |
| Hub bracket | Z 50.5–63 | **Z 52.5–63** (17 × 10, 2.5 wall under the pin) |
| Carriage body | Z 51.5–59.5, centred on the axis | Z 51.5–59.5 (**unchanged**, referenced to the channel: floor top to lip underside) |
| Carriage boss | — | **new:** Y 126.8–143.8 (17.0, centred on the rail), Z 59.5–62.0, full carriage length |
| Cable-run keep-out | Z 52.5–58.5 | Z 54.5–60.5 |
| Side-wall notch bottom | Z 49.5 | Z 51.5 (more side wall left) |
| MC_HUB_* / MC_CASSETTE_* / MC_RAIL_* / MC_CARRIAGE_* origin Z | 55.5 | 57.5 |

4. **Parameters that change:** `SOLAR_HUB_AXIS_OFFSET_Z`, formula only (still a working, TBD value):
   - from `0 - (MIN_GAP + SOLAR_RAIL_LAYER_HEIGHT / 2)` (−7.5)
   - to `WALL_THICKNESS + MIN_GAP + SOLAR_BRACKET_WALL + SOLAR_HUB_PIN_DIAMETER / 2 - (SOLAR_RAIL_LAYER_HEIGHT + MIN_GAP)` (−5.5).
   - Read it as: floor + running gap + bracket wall + pin radius above the rail-layer bottom, expressed from the cassette's rail-side face.
5. **Parameters that stay unchanged:**
   - carriage: `SOLAR_CARRIAGE_WIDTH` 22.6, `SOLAR_CARRIAGE_HEIGHT` 8, `SOLAR_RAIL_ENGAGEMENT` 40;
   - rail: `SOLAR_RAIL_WIDTH` 27.6, `SOLAR_RAIL_SLOT_WIDTH` 17.6, `SOLAR_RAIL_LAYER_HEIGHT` 13;
   - lid: `LID_THICKNESS` 37.6;
   - travel and clearances: `SOLAR_SLIDE_TRAVEL` 158, `SOLAR_DEPLOY_CLEARANCE` 8, `SOLAR_HUB_LINK_LENGTH` 11.5;
   - hub: `SOLAR_HUB_PIN_DIAMETER` 5, `SOLAR_HUB_AXIS_OFFSET_Y` 114.3;
   - bracket: `SOLAR_BRACKET_WIDTH` 17, `SOLAR_BRACKET_LENGTH` 10;
   - cables: `SOLAR_CABLE_*`, `SOLAR_CABLE_CORRIDOR` 8;
   - rotation: `SOLAR_ROTATION_LIMIT`, `SOLAR_INDEX_STEP`;
   - the cassette, and all authoritative values.
6. **New parameter:** `SOLAR_BRACKET_WALL`, working formula `WALL_THICKNESS` → 2.5.
   - It is the hub-bracket wall around the pin, now implicit in the generator.
   - Making it explicit keeps the budget in item 4 visible and checkable.
   - No parameter is needed for the boss: its width is `SOLAR_BRACKET_WIDTH` (the slot is sized for it) and its height is the lip thickness (`WALL_THICKNESS`).
7. **Architecture or local geometry?**
   - **Local geometry** inside the approved B.1 V1 + fixes architecture. Rail + carriage + metal pin + hub bracket, slide along X, tilt about X, rail as the load path, and D-004 all stay as they are.
   - It changes one working formula and the carriage profile. The B.1 "axis at rail mid-height" choice is superseded; record it in the build log / decisions if approved.
8. **Validation to rerun after implementation:** see §9.

## 8. Related observations (not part of the F3 fix; for the owner's attention)

- **O1: the 10 mm hub-bracket bore is the weakest point of the deployed load path** (inferred). In case H: 17.1 MPa peak bore pressure and a 51 MPa wall index at 2.5 mm, against PETG at 25–45 MPa.
  - A 20 mm bore gives 4.1 MPa and 12.4 MPa. Variant B20 (B + `SOLAR_BRACKET_LENGTH` 20) passes the full geometry check set with no new clearance issues.
  - Recommended as a separate decision, with a hub-bore test in the next physical round; it is not bundled with F3.
- **O2: pin material** (inferred). Case H gives 130 MPa bending in the Ø5 pin at the carriage exit. That needs a hardened or stainless dowel-class pin rather than soft steel or aluminium. This is independent of F3; no component is selected.
- **O3: the twist zone** is still Python-only (not an E2 part). Its clearances are governed by X separation (at least 1.0), so the axis height does not affect them.

## 9. Validation plan (after approval only)

1. **Generator** (`e_lid_layout.py`):
   - carriage body referenced to the channel, plus the boss prim;
   - `BZ0` using `SOLAR_BRACKET_WALL`;
   - bracket–rail changes from the KNOWN_B1 / F3 exclusion to a guided-fit rule (at least CLEARANCE laterally in the slot, at least MIN_GAP to the floor over the whole travel);
   - the B.1 consistency check records the intentional hub-Z and notch-Z deviations;
   - new budget assertions: floor + MIN_GAP + bracket wall + pin + MIN_WALL ≤ rail layer, and pin top + MIN_GAP ≤ cassette bottom.
2. **Local checks:**
   - full E2 check set: expect 0 unexpected violations, bracket–floor 1.00 over the full travel, bracket–slot 0.30, the rear-plug OPEN CONFLICT unchanged, table as in §6;
   - `yaml_to_featurescript.py --check` (both targets) and `base_v01_layout.py --check` (unaffected);
   - regenerate the local `NOMAD_P01.fs` block (it reads the same parameter);
   - the E0.5 study-reproducibility diff: every published study output must stay byte-identical.
3. **Onshape:**
   - regenerate the E2 harness data and run one scratch kernel cross-check (about 10 API calls); exact agreement is required;
   - only then write the Feature Studio;
   - owner visual check: section at X = 5 shows the bracket 1 mm above the floor; section at X = −30 shows the carriage boss in the slot.
4. **Physical** (next physical round, not now):
   - carriage-boss fit and binding in the printed A1 / A2 rail coupons (0.3 mm per side);
   - hub-bracket bore strength, 10 vs 20 mm (O1), under a hanging load at the cassette edge;
   - pin retention.

---

## 10. Implementation record — F3 APPROVED AND IMPLEMENTED — OPTION B (2026-09-26)

**Scope:** only option (b), exactly as in §7. These are not implemented:
- the 20 mm bore (O1) and pin material (O2), which remain separate decisions;
- F1 / F2, class B / C, and E3 / E4 / E7.

### Parameters (`nomad.yaml`, working formulas only; no authoritative value changed)

| Parameter | Before | After |
|---|---|---|
| `SOLAR_HUB_AXIS_OFFSET_Z` | `0 - (MIN_GAP + SOLAR_RAIL_LAYER_HEIGHT / 2)` → −7.5 | `WALL_THICKNESS + MIN_GAP + SOLAR_BRACKET_WALL + SOLAR_HUB_PIN_DIAMETER / 2 - (SOLAR_RAIL_LAYER_HEIGHT + MIN_GAP)` → **−5.5** |
| `SOLAR_BRACKET_WALL` (new, TBD / working) | — (implicit `WALL_THICKNESS`) | `WALL_THICKNESS` → **2.5** |

`docs/mechanical-spec.md` rows were updated or added to match; the parameter pipeline's spec cross-check requires this.

### Geometry (as §7 item 3; modeled)

| Item | Implemented |
|---|---|
| Axis | Z 55.5 → **57.5**; pin Z 55–60 (Ø5) |
| Hub bracket | **Z 52.5**–63, 2.5 mm wall under the pin (`LE_BZ0 = LE_HZ − pin/2 − SOLAR_BRACKET_WALL`) |
| Carriage | body unchanged: 22.6 × 8 × 40, Z 51.5–59.5, now defined from the channel. **Boss** 17.0 × 2.5 × 40, Z 59.5–62.0, centred on the rail |
| Follows the axis | cable-run keep-out Z 54.5–60.5; side-wall notch bottom Z 51.5; all eight solar mate connectors at Z 57.5 |
| Unchanged | lid 37.6, rail section and floor, cassette, travel 158, ±75°, deploy clearance 8, corridor 8, stagger, hinge, display, service, rear port |

### Generator (`CAD/tools/e_lid_layout.py`)

- **Geometry:** `BZ0` uses `SOLAR_BRACKET_WALL`. The carriage is body + boss, and its displayed name says "+ 17 x 2.5 slot boss".
- **Fit rule:** bracket–rail is now a guided fit (≥ CLEARANCE 0.3 in the slot), replacing the F3 known-overlap exclusion.
- **New checks:**
  - bracket–floor sweep over the full travel in 0.1 mm steps (≥ MIN_GAP);
  - F3 vertical-budget assertion (bracket–floor ≥ MIN_GAP, boss wall above the pin ≥ MIN_WALL, carriage below the pin ≥ MIN_WALL, pin top to the other cassette ≥ MIN_GAP).
- **B.1 consistency:** the check records the intentional +2.0 on hub Z and notch Z; 29 / 29 values match.

### Validation

**Local (modeled):**
- **`e_lid_layout.py`: ALL CHECKS PASSED.**
  - F3 budget: bracket–floor 1.0, boss wall 2.0, carriage below the pin 3.5, pin to the other cassette 3.0.
  - Bracket–floor over the full 158 mm travel: min **1.000**. Bracket in slot: 0.300.
  - 0 unexpected moving-part violations: lid 0 / 105 / 120 / 135° × stowed / R / L / both, tilts ±75° (same and opposite), slides 0..1.
  - Lid sweep 0–135°: no violations, minimum 1.000.
  - Rear plugs unchanged: 105°: 10.75, 120°: 1.20, 135°: −6.60 (OPEN CONFLICT, below MIN_GAP from 121°).
- **`f3_investigation.py`:** reproduces the published investigation exactly; the pre-F3 baseline and variants are now pinned. New part E: **the production layout is identical to variant B** (all parts, all primitives).
- **Study reproducibility:** every study tool (A.2, B, B.1, B.2, coupons, C, C.1, C.2, D, D.1, P0.2) produces **byte-identical** output before and after.
- **Generator checks:**
  - `yaml_to_featurescript.py --check` passes for both targets; the local-only `NOMAD_P01.fs` params block was regenerated.
  - `base_v01_layout.py --check` passes (both targets).

**Onshape scratch cross-check:** `E2 n55 mc10 L0 S0/177 c175 dv0 m0 P0/15 pd0`.
- All 177 near-pair states and 175 exact gaps match with 0.000 mm deviation.
- All 10 connector origins match with 0.000 deviation.
- All 15 posed clearances match with 0.000 deviation.

**Persistent write:** `put_featurescript` to `NOMAD_E_Prototype` succeeded. It was preceded by a read confirming that Onshape held exactly the E2 text. A read-back afterwards is **identical** to the local `NOMAD_E_Prototype.fs`. API: 125 → 140.

### Clearances that changed (stowed unless noted; modeled)

| Pair | E2 | Option B |
|---|---|---|
| Hub bracket vs rail floor | **−1.00** | **+1.00** (full travel) |
| Hub bracket vs rail (slot lips) | (masked by F3) | 0.30 (designed fit) |
| Pin vs rail | 1.50 | 3.16 |
| Carriage (boss) vs the other cassette | 3.50 | **1.00** (= MIN_GAP, same as the rail top) |
| Carriage vs its own cassette | 12.02 | 11.54 |
| Pin vs either cassette | 5.00 | 3.00 |
| Cable run vs either cassette | 4.50 | 2.50 |
| Display vs pin / bracket / cable run | 5.0 / 2.5 / 4.5 | 7.0 / 4.5 / 6.5 |
| Rear shell vs carriage / cable run | 13.5 / 14.5 | 11.0 / 12.5 |
| Cassette R vs base (lid 105°, tilt +75 / −75) | 111.48 | 110.00 |
| Lowest tilted cassette above table, lid 105–135° | 7.8 | 6.5 (lid 135°, tilt −45°) |
| Lowest point at lid 0°, tilt 0 (bracket → carriage) | 50.5 | 51.5 |

Unchanged: display–rail 1.0, cassette–rail 1.0, cassette–shell 2.0, cassette L–R 1.0, deployed cassette–lid 8.06, deployed carriage–side wall 1.0, hinge 1.0, corridor–carriage 2.5, loop–cassette 1.0, controller band–loop 1.0.

### Owner actions

- The Part Studio `NOMAD E — Digital Prototype` picks up the new Feature Studio code on regeneration. If Onshape marks NOMAD E Lid as out of date, update the feature.
- **Expect:** the same 78 parts and 10 connectors.
- **Section views:**
  - X = 5: the bracket bottom is 1 mm above the rail floor;
  - X = −30: the carriage boss fills the slot up to the rail top.
