# Round D — Lid Stack-Up / Structural Envelope Study

**Status:** analysis only. No lid thickness is declared, no architecture is ranked or chosen, and D-007 is neither accepted nor rejected.

**Model:** `CAD/tools/lid_stackup_study.py`. It reuses:
- the B.1 V1 + fixes solar geometry (`solar_v1_feasibility.py`, kernel-validated in B.1) and the B.2 formulas (`lid_structure_screening.py`);
- the C.2 hinge / port model (`c2_screening.py`).

```bash
py CAD/tools/lid_stackup_study.py
```

**Evidence levels:**
- Layer arithmetic and geometry: *modeled*.
- Stiffness: *analytical screening estimate* (beam/plate formulas, **not FEA**).
- Masses, controller size and material data: *working assumptions (inferred)*.
- **Physical validation is required** for every structural number. Coupons A (rail) and B (back plate) already exist for this.

**No Onshape run.** The new content is layer arithmetic and analytical stiffness, which the kernel cannot check. The geometry it builds on (V1 solar, C.2 sweep) was already kernel-validated. API total unchanged at ~100 / 2,500.

## 1. Existing constraints

| Class | Lid-relevant values |
|---|---|
| **Authoritative** (provisional/derived) | Display diagonal 256.5 (active 217.5 × 136.0); solar rotation ±60–75°, axis ≈ slide direction (D-004) |
| **Working** (`nomad.yaml`) | Display 235 × 150 × 5; `LID_THICKNESS` 25; `LID_CLOSED_GAP` 2.0; lid angles 105 / 135°; cassette 147.5 × 200 × 8; carriage 12 × 8; deploy clearance 5; pin Ø5; wall 2.5; MIN_GAP 1.0 |
| **TBD** | Hinge axis position and hardware (D-006); display SKU and controller; solar panel (cassette mass and real thickness); INSERT_SIZE; CABLE_CLEARANCE |
| **Lid-thickness dependencies** | Display thickness; display retention; rail-layer height (= carriage height + 2 × rail walls); cassette thickness; the three stack gaps; back-structure depth; any mid-plate |
| **Unverified assumptions** | 5 mm display *including* its board/FPC; 0.3 kg cassettes; PETG E = 2000 MPa; the B.1 fixes; that the cassettes must stay enclosed; 0.2 kg display; 12 mm controller |

**Found inconsistency (flag, not changed):**
- `nomad.yaml` still carries the Round B values (carriage width 12, deploy clearance 5).
- The only solar geometry that passed B.1 is **V1 + minimal fixes**: carriage 22.6, bracket 17, deploy clearance 8, 8 mm corridor. Those exist only as what-if constants in the B.1 tool.
- This study uses V1 + fixes. None of these widths affect lid thickness; only the carriage *height* (8) does.
- **The working `LID_THICKNESS` of 25 is below every architecture studied here** (minimum 30–31 without a back structure, ~37 with an enclosed one).

## 2. Functional lid layers (lid face → back; working values)

| Layer | Thickness | Driver / note |
|---|---|---|
| Front retention lip over the display border | 0 or 1.0 | 0 = flush, clip-retained from behind; 1.0 = bezel lip (border 7–8.75 mm available) |
| Display module | 5 (working) | must include the panel's own board/FPC (B.1) |
| Display-back gap | 1.0 | MIN_GAP |
| Rail mid-plate (D, E only) | 2.0 | rails fastened along it |
| Solar rail layer | **13** | carriage height 8 + 2 × 2.5 rail walls (B.1). Largest single layer after the back structure |
| Rail–cassette gap | 1.0 | MIN_GAP |
| Stowed cassette | 8 (working) | panel not selected |
| Cassette–back gap | g | the back must deflect ≤ g/2 (B.2 criterion) |
| Back structure | 0 – 14 | spans the 202 mm cassette bay one-way; no internal support is possible |

**Stack to the cassette top:**

| | No mid-plate | With 2 mm mid-plate |
|---|---|---|
| No front lip | 28 | 30 |
| 1 mm front lip | 29 | 31 |

**Display controller (configurable envelope; no hardware selected):**
- **Space:** the hinge-end band beside the right service loop, Y 197.1–232.5 (**35.4 deep**) × Z 2.5–19 (**16.5 tall**). It is ~111.5 wide on each side of a 15 mm centre cable pass, clear of the 28 mm hinge corners.
- **Thickness:** a 12 mm controller (connectors included) fits the height; up to ~15.5 is possible with MIN_GAP.
- **Cable exit:** a single 90° bend (R 15 + Ø6 = 21) fits. A U-turn or service loop (2R + d = 36) does **not** fit the 35.4 band, so cable loops belong at the hinge/base side (Round C display riser), not in the lid band.
- **Controller outside this band:** a controller wider than ~35 mm in its short dimension, or thicker than ~15.5 mm, does not fit and must go in the base. Then the panel's own cable must cross the hinge.
- **Service access:**
  - B/C: rear shell off; the cassette edge overlaps the band over Y 197–217.
  - D: controller mountable on the rail module.

## 3. Candidate architectures

**Common basis:** 1 mm front lip; V1 + fixes solar; cassette–back gap 2 where a back structure exists.

| | A — thin structural | B — two-piece, ribbed rear shell | C — sandwich rear shell | D — modular (rail mid-plate) | E — cassette-backed (other) |
|---|---|---|---|---|---|
| Build-up | front frame + rails + local reinforcement + 1.6 non-structural cover | front frame + rails + 2.5 skin with 8.5 external ribs @ 30 | front frame + rails + skins 1.2 / core 4.5 / 1.2 (rib webs 2.0 @ 30) | front frame + **rail module** (2.0 mid-plate + rails) + sandwich service shell | front frame + rail module; **no shell over the cassettes** |
| Total thickness T (lip 1 / lip 0) | 31.6 / 30.6 | 42.0 / 41.0 | 37.9 / 36.9 | 39.9 / 38.9 | 31.0 / 30.0 |
| Closed stack (H 40 + gap 2 + T) | 73.6 | 84.0 | 79.9 | 81.9 | 73.0 |
| Display cavity (face → rail layer) | 7 | 7 | 7 | 9 | 9 |
| Controller space | band 111.5 × 35.4 × 16.5 per side (all) | same | same | same, or on the module | same |
| Solar rail height | 13 | 13 | 13 | 13 | 13 |
| Cassette clearance below / above | 1 / 1 | 1 / 2 | 1 / 2 | 1 / 2 | 1 / open |
| Back structure | cover touches the cassette at **~0.4 N** | LC1 / LC2 0.93 / 0.59 (≤ 1.0 allowed) | 0.88 / 0.56 | 0.88 / 0.56 | none: LC1 acts on the cassette/panel |
| Hinge interface | hinge band Y 218.5–235 (16.5) × 28 corners × full T; inserts in the front frame | same | same | same; the module can also tie to the hinge band | same |
| Structure mass (PETG, solid est.) | ~519 g | ~650 g | ~624 g | ~797 g | ~548 g |
| Lid total (+ display 0.2, controller 0.04, hinges 0.05, 2 × 0.3 cassettes; placeholders) | ~1.41 kg | ~1.54 kg | ~1.51 kg | ~1.69 kg | ~1.44 kg |
| Manufacturability | 2+ flat parts; cover 301 × 235 × 1.6 | front frame (supports under the edge beams, B.2), rear shell skin-down ribs-up, no supports; ribs exposed outside | sandwich printed skin-down, **top skin bridges ~28 mm** between ribs (or a separate outer skin, screwed) | 4+ large flat parts; mid-plate 296 × 230 flat | 2+ parts |
| Assembly sequence | display → rails → cassettes → cover | display → rails → loops/controller → cassettes (side slots) → rear shell (10 screws, B.2) | as B | display → rail module (rails, loops, controller pre-assembled) → cassettes → shell | display → rail module → cassettes |
| Serviceability | cover off → cassettes → rails → display | shell off → cassettes → rails → display (B.2) | as B | shell off → cassettes → **module out as one unit** → display/controller | cassettes out → module → display |
| Likely failure modes | back loads go into the panels; cover–cassette friction or jam; stowed cassettes need edge lands (not in B.1) | exposed ribs (snag, handling); open-section torsion; thickest lid; rail cantilever | skin bridging sag and rib–skin layer bond; rail cantilever | most interfaces; mid-plate at 0.5–0.9 mm vs a 1.0 gap at 3 g | panels exposed to impact and dirt; torsion; see the note below |

**Other thickness facts:**
- **Plain thick back skin:** it meets the criterion at 6.0 mm (T 37.0) but weighs ~539 g solid. Printed with sparse infill it becomes a sandwich with unknown core shear.
- **E and the "stored inside the lid" requirement:** E conflicts with it if that means *enclosed*. The branch is documented and stopped there, not developed.

## 4. Thickness calculations: back structure vs cassette gap

**Setup:**
- LC1: 20 N at mid-bay on b_eff 101.
- LC2: 1 kPa.
- Criterion: δ ≤ g/2.
- Rib-web shear is included.
- T is quoted with the 1 mm lip; subtract 1 for a flush display.

| Gap g | Ribbed (2.5 skin + h) | Plain skin | Sandwich (1.2 + core + 1.2) |
|---|---|---|---|
| 1.0 | h 11.5 → **T 44.0** (293 g) | 7.5 → T 37.5 (674 g) | core 6.5 → **T 38.9** (264 g) |
| 1.5 | h 9.5 → T 42.5 (281 g) | 6.5 → T 37.0 (584 g) | core 5.0 → T 37.9 (253 g) |
| 2.0 | h 8.5 → **T 42.0** (275 g) | 6.0 → T 37.0 (539 g) | core 4.5 → **T 37.9** (249 g) |
| 3.0 | h 7.0 → T 41.5 (266 g) | 5.25 → T 37.25 (472 g) | core 3.5 → T 37.9 (242 g) |
| 4.0 | h 6.0 → T 41.5 (260 g) | 4.75 → T 37.75 (427 g) | core 3.0 → T 38.4 (238 g) |
| 6.0 | h 5.0 → T 42.5 (254 g) | 4.25 → T 39.25 (382 g) | core 2.0 → T 39.4 (231 g) |

**Minimum T by back type:**
- **Ribbed back:** ~41.5, at gaps of 3–4. The rib height buys less than the gap costs.
- **Sandwich:** ~37.9 across gaps of 1.5–3.
- **B.2's 42.5** is reproduced (ribbed back, gap 1, no lip, 11–11.5 mm ribs). It is **not required** by any sandwich or plain-back variant.

## 5. Structural screening (analytical estimates; NOT FEA)

1. **Back-panel deflection:** the table in §4. The coupon B tests (202 span, 2.5 skin, ribs h 6 / 8 / 11) validate the ribbed rows directly. **The sandwich option has no coupon yet.**
2. **Rib spacing and height** (LC1, 2.5 skin):

   | Spacing | h 4 | h 6 | h 8 | h 10 | h 12 |
   |---|---|---|---|---|---|
   | 20 | 3.14 | 1.46 | 0.78 | 0.47 | 0.30 |
   | 30 | 4.10 | 1.98 | 1.07 | 0.64 | 0.41 |
   | 40 | 4.89 | 2.46 | 1.35 | 0.81 | 0.52 |

   Sandwich core 4 / 6 / 8 / 10: 1.01 / 0.52 / 0.32 / 0.21 in bending only, 1.06 / 0.56 / 0.34 / 0.23 with web shear.
3. **Rail deflection toward the display** (stowed 0.3 kg cassette):

   | Rail mounting | Architectures | Static | 3 g | vs 1.0 gap |
   |---|---|---|---|---|
   | Cantilever from the outboard pad | A, B, C | 0.67 | **2.00** | exceeds |
   | Fastened along a 2 mm mid-plate, simply supported over 296 | D, E | — | **0.52** (composite) – **0.88** (non-composite) | within, 0.1–0.5 mm margin |

   A metal stiffener in the rail (coupon A2) is the alternative for A–C: ~0.17 at 3 g (B.2, inferred).
4. **Cassette static load:** 0.3 kg each, stowed, on its carriage (as 3). Deployed: moment on the carriage 0.53 N·m (10 m/s wind) to 1.2 N·m (20 m/s), carriage end reactions ~13–30 N, carried rail → pad → front frame (B.2). These are unchanged by the back structure.
5. **Handling load:** LC1 / LC2 above. In A, the cover reaches the cassettes at ~0.4 N. In E, the load acts on the panels directly.
6. **Jolt (3 g):** the rail case (3) governs. The back structure's own weight is negligible.
7. **Hinge-region loading** (lid mass 1.41–1.69 kg, placeholders; CG at mid-lid, 117.5 mm from the axis):
   - Holding torque: 1.6–2.0 N·m total (0.8–1.0 per hinge).
   - At 3 g: 2.4–2.9 per hinge. A 20 N opening force at the free edge: 2.35 per hinge.
   - Over a ~12 mm screw couple inside the 16.5 mm hinge band that is **~200–245 N per screw**. That is within typical M3 heat-set pull-out in PETG (several hundred N; insert- and print-dependent, inferred) but with a modest margin.
   - This suggests ≥ 3–4 inserts per hinge or a through-bolt / metal backing plate (inferred).
   - Hinge friction must hold at least ~1 N·m per hinge.
8. **Torsion** (conceptual). Because the cassette slots open both side walls over 200 of 235 mm, the lid is an **open section** in torsion over most of its depth. Index (St Venant J of the mid-depth section only; ring frame and bands ignored; 20 N at one free corner):

   | Architecture | J (mm⁴) | Twist | Corner deflection |
   |---|---|---|---|
   | A | 5,552 | 10.0° | 26 mm |
   | B (open ribs) | 6,917 | 8.0° | 21 mm |
   | C (closed sandwich) | 28,018 | 2.0° | 5 mm |
   | D | 28,807 | 1.9° | 5 mm |
   | E | 5,938 | 9.4° | 25 mm |

   - The absolute values are conservative indices, not predictions. The perimeter frame adds stiffness the index ignores.
   - What is robust: a closed-cell back is about 4–5× stiffer in torsion than any open back of similar mass.

## 6. Solar compatibility (V1 + fixes; not redesigned)

- **Stowed:** every architecture keeps the V1 gaps: display → rail 1.0 (or display → mid-plate 1.0), rail → cassette 1.0, cassette → back ≥ 1.0.
  - A: the cover sits at 1.0 but closes under ~0.4 N.
  - E: no back.
- **Deployment path, rails, carriage, hub, bracket, tilt-joint cable zone, loops, corridor:** unchanged relative geometry, B.1 clear (all slides, all tilts ±75°, lid 0 / 105 / 135°).
  - The added lip or mid-plate shifts the whole solar group away from the display face by 1–3 mm.
  - The back structure lies outside the deploy path (the cassettes leave through the side-wall slots below it).
- **Lid and base:** deployed cassettes sit at |X| ≥ 158.5, outside the 150.5 lid and base width, so neither the back structure nor the base can meet them.
- **Lowest deployed-cassette Z** (tilts ±75°) at 105 / 120 / 135°, all above the table:

  | | h 0 | h 4 | h 8 |
  |---|---|---|---|
  | A–C | 49 / 32 / 8 | 54 / 38 / 15 | 59 / 44 / 21 |
  | D, E | 48 / 31 / 6 | 53 / 37 / 13 | 58 / 43 / 20 |

- **Contradictions found:** none in the mechanism.
- **Gap found:** stowed cassettes are held only at their hub/carriage (B.1). A and E put back loads *into* the cassettes, which requires stowed edge lands/guides that do not exist in B.1. Documented; not designed.

## 7. Hinge / port compatibility (C.2 model: D-006 rear-edge axis, gap 2, port zone Z 4–19, 45 mm plugs, MIN_GAP 1)

| T | Arch. | Max feasible opening at h 0 | Min h for 120° | Min h for 135° | Lid–base clearance |
|---|---|---|---|---|---|
| 31.0 | E | 127.0° | 0 | 2.0 | 1.41 (h 0–2) / 2.00 (h ≥ 4) |
| 31.6 | A | 126.5° | 0 | 2.5 | same |
| 35.0 | — | 122.5° | 0 | 4.0 | same |
| 37.9 | C | 120.0° | 0 | 5.0 | same |
| 39.9 | D | 118.5° | 1.0 | 6.0 | same |
| 42.0 | B | 117.0° | 1.5 | 7.0 | same |
| 42.5 | (B.2) | 116.5° | 1.5 | 7.0 | same |

- **Feasible envelope:** every T in 31–42.5 has feasible (h, θmax) pairs meeting MIN_GAP.
- **120° at h ≤ 1.5:** needed by every T listed.
- **135°:** needs h = 2–7 mm, depending on T.
- **Short plugs** (≤ 15 mm) remove the port term entirely (C.1).
- **No hinge height or angle is chosen here.**

## 8. Manufacturing implications (PETG, 0.4 / 0.2, no printer selected)

- **Footprint:** every architecture has at least one part with the full 301 × 235 footprint (front frame, rear shell, cover or mid-plate). That is the same ≥ 301 × 235 bed requirement as the base, unless split.
- **One-piece lids are unprintable:** B.2 found the closed cassette tunnel (296 × 202 × 10) needs trapped support or 200 mm bridges. Every architecture here is therefore **multi-part** (≥ 2 large parts + 2 rails).
- **Supports:** only under the front-frame edge beams (B.2). Rear shells, covers and mid-plates print flat without support. The sandwich top skin is either bridged (~28 mm spans) or printed as a separate skin. Closed sandwich cells are **not** trapped geometry (nothing to remove).
- **Inserts:** in the front-frame edge bands (rear-shell screws from outside) and in the hinge band. Sandwich screw points need solid columns through the core.
- **Long rails:** 198 mm printed C-channels. Coupon A1/A2 tests stiffness and the metal-stiffener option.

## 9. Serviceability implications

- **Controller:**
  - Hinge-end band; never trapped.
  - B/C: reached after the rear shell and the cassettes (edge overlap Y 197–217).
  - D: can ride on the removable rail module.
- **Cables:** service loops and corridor stay in the rail layer (B.1). The display cable exits at the hinge centre. Loops belong in the base riser (the lid band cannot fit a U-turn).
- **Rails, carriages:** removable in every architecture (screwed to pads or to the module). Cassettes slide out through the side slots after releasing the end stop.
- **Hinge hardware:** in the front-frame hinge band, from the back once the rear shell or cover is off.
- **Display:** from the back in every architecture. The number of parts to remove differs: A cover, rails; B/C shell, cassettes, rails; D shell, cassettes, module; E module.

## 10. Major risks

1. **The working `LID_THICKNESS` 25 is not achievable.** Every enclosed architecture is ~37–42 (lip 1). That moves every base, hinge and port result that used 25 (C.1 / C.2 rear ports need h ≥ 5–7 for 135°).
2. **Rail stiffness.** The cantilever rail (A–C) exceeds the display gap at 3 g (2.0 vs 1.0) unless a metal stiffener is added. The mid-plate (D/E) is marginal (0.5–0.9 vs 1.0).
3. **Torsion.** Cassette slots open both side walls, so open-back lids (A, B, E) rely on the perimeter frame. Closed-cell backs are ~4–5× stiffer (index).
4. **Hinge screw loads** of ~200–245 N per screw at 3 g: modest margin on printed inserts.
5. **Display and controller unknowns.** 5 mm must include the panel's board/FPC. A controller larger than the 35 × 16.5 band forces it into the base and the panel cable across the hinge.
6. **Solar parameter drift.** YAML carriage and deploy values (Round B) differ from the only passing geometry (V1 + fixes).
7. **Sandwich printing** (C/D): skin bridging and rib–skin bond quality are untested.
8. **Mass:** lid ~1.4–1.7 kg (placeholders). Combined with the rear-edge hinge, tip-back stability is still unmodeled.

## 11. Remaining unknowns

Display module thickness and board/FPC position; display retention method; controller size, connectors and cable type (bend radius); cassette panel, thickness and mass; PETG printed E and interlayer strength; hinge hardware, axis height and torque; real lid mass and CG; whether the cassettes must be enclosed; stowed-cassette support method.

## 12. Measurements that would most reduce uncertainty

1. **Coupon B results** (B1 and B2 at h 6 / 8 / 11): validates the back-plate model and the ribbed rows of §4 directly.
2. **Coupon A results** (A1 vs A2 metal stiffener): validates the rail rows in §5.3.
3. **Display module sample or datasheet:** true thickness including the board/FPC, and mounting features.
4. **Controller board and display cable:** footprint, height with connectors, cable diameter and bend radius.
5. **Cassette panel choice:** real thickness and mass (8 mm and 0.3 kg are placeholders).
6. **A small sandwich coupon** (202 span, 1.2 skins, 4.5 core): there is no coupon for this yet. *(suggested, not created)*
7. **Hinge hardware sample:** axis height achievable at the rear edge, holding torque, screw pattern.

## 13. Proposed working lid envelope (for downstream checks only; not a final thickness)

- **Envelope:** 301 × 235 × **T = 37–42** for an enclosed-cassette lid (sandwich or plain back at the low end, ribbed back at the high end, 1 mm lip). A conservative single working value for base/hinge/port checks would be the upper bound, **T ≈ 42**.
- **Why 42 bounds the case:** it covers every enclosed architecture found. It implies either h ≥ 7 mm for 135° or θmax ≤ ~117° at h 0 with the current port zone (§7).
- **Other architectures:** A and E (T 30.6–31.6) only apply if the cassettes may carry back loads or be exposed, which conflicts with the enclosure requirement as currently read.
- **Updating `LID_THICKNESS`** in `nomad.yaml` (a working value) is an owner decision. It has **not** been changed.

## 14. Dependencies that must be resolved before D-007 can be finalized

1. **Lid class:** enclosed cassettes (T 37–42) or exposed/contact-bearing (T 30–32). Sets T.
2. **Hinge axis height and maximum angle for that T** (§7). Sets the rear-port feasibility and therefore D-007's rear-I/O commitment.
3. **Rail stiffening path:** metal stiffener (no thickness change) or mid-plate (+2 mm, D). Sets T and the lid part structure.
4. **Controller location:** lid hinge band (needs a controller ≤ ~35 × 16 in section) or base (the panel cable crosses the hinge). Sets the base's display riser and pass-through sizing (Round C: 15 × 10 corridor).
5. **Hinge interface:** D-007's 28 × 21 base hinge reserves vs the lid's 16.5 mm hinge band and ~200–245 N screw loads (hardware choice).
6. **Solar parameter reconciliation:** decide whether the B.1 fixes become the working YAML values.
7. **Base closed-stack impact:** closed thickness 40 + 2 + T = 79–84 for enclosed lids (vs 67 with T 25). Ergonomics and print height are owner considerations.
