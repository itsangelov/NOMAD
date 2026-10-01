# D-010 — Solar Architecture Comparison (Sliding Wings vs Solar Lid)

**Status:** architecture study and decision gate. **Nothing is chosen.**

> **ERRATUM (D-010 Phase 2, 2026-09-28, `prototypes/P0.1/d010/d010_solar_architecture_phase2.md`):**
> - **Visor:** a leaf hinged at the lid's top-back edge **cannot** shade the screen while generating power; tilted over the screen, its cells face the table. The visor claims below are withdrawn.
> - **Mass:** the real catalog panel that fits B1 is FR4-backed (Voltaic P108, 328 g). With it and the stay, total mass is **equal** (A 2.64 / B1 2.62 kg); "B1 about 180 g lighter" is withdrawn.
> - **Stability:** the tipping model is refined (foot polygon, 3-D plate model, real stay). See Phase 2 §9 and §11.
- No change to production Onshape, master geometry, `nomad.yaml`, FeatureScript or Git.

**Tool:** `CAD/tools/d010_solar_architecture_study.py` (NON-PRODUCTION).
- It prints every calculated number below.
- It writes concept views to `prototypes/P0.1/d010/` (`d010_side_views.svg`, `d010_front_views.svg`).

**Evidence labels:**
- **[calc]** calculated by the tool from the stated inputs.
- **[est]** engineering estimate.
- **[assume]** assumption.
- **[unknown]** not known.
- Nothing here is measured, and there is no FEA.

**Candidates:**
- **A:** current sliding / tilting wings (D-009 baseline, including S1-R).
- **B1:** solar lid, a single leaf hinged at the lid top edge, covering the lid back.
- **B2:** solar lid tri-fold: a full-width centre leaf plus two half-width side leaves folded onto it.

---

## 1. Executive summary

**The solar lid (B1) is the better V1 architecture on the criteria that dominate a PETG, low-budget, January-2027 build:**
- mechanical complexity;
- cable routing;
- printability without machined parts;
- cost;
- user steps;
- solar orientation.

**It delivers about the same power as the wings:** about 10 W nameplate against about 9 W [calc].

**The wings keep two real advantages:**
- the cells are protected inside the lid in transport;
- deploying them does not move mass rearward.

**A still carries unresolved engineering problems:**
- the PETG hub-bracket shortfall;
- the ±80° stop needing a four-part precision yoke;
- a cable that must twist ±80° inside an 11.5 mm link;
- about 20 parts per wing, several of them wire-EDM / CNC.

**B's risks are physical and solvable with simple parts, but they are real:**
- **Tipping and wind:** a leaf deployed behind the lid top moves the centre of gravity toward the rear tipping edge. The lid hinge sits on that edge (D-006).
- **Hinge torque:** the lid hinges must hold about 1.0–1.4 N·m [calc].
- **Stowed heat:** the leaf needs a vented air gap.

**Limits of B:**
- A tri-fold (B2) for about 20 W tips over when cantilevered from the lid top [calc]. It is only viable with ground support.
- B1 needs a positive angle lock and, for wind, a fold-out rear stay.

**Recommendation: ARCHITECTURE B (B1), gated by a one-day physical mock-up** that measures tipping, hinge torque and wind with real masses (§13).

## 2. Architecture A analysis — sliding wings (baseline)

**Concept:**
- Two 147.5 × 200 × 8 cassettes are stowed inside the lid (rail layer 13 + cassette 8).
- Each slides 158 mm sideways and tilts about its slide axis over ±75° in 15° indexed steps, with a ±80° hard stop.
- The lid is 37.6 mm thick.

**Status of the engineering:**
- **Modeled and validated:** the lock and wing geometry (D-009).
- **Studied only:** the stop (S1-R: PASS for review, not integrated).
- **Open:**
  - the PETG hub bracket is below SF 2 at handling once the lock reaction is included;
  - the cable twist in the link;
  - the slide lock / detent and the stowed cassette retention (not designed).

**Strengths:**
- The cells are **inside the lid** when stowed: protected, no scratch or impact risk.
- Deployed mass moves **sideways**, so the side-view centre of gravity is unchanged.
- Each wing tilts independently.

**Weaknesses:**
- A small, fixed area (two panels about 190 × 140) and no growth path without a thicker lid.
- It needs lateral room (612 mm span).
- **Tilt is relative to the lid**, so the reachable panel elevation depends on the display angle. The panels face only the rear hemisphere.
- High part count and precision.

## 3. Architecture B analysis — solar lid

**B1 (primary):**
- One leaf about 295 × 229 covers the lid back. The cells face outward when stowed.
- It is hinged at the lid top edge and swings up and back on its own angle (ψ 0–150°) with a positive lock.
- A 4–6 mm **vented air gap** separates it from a thin rear shell.
- The lid core drops to about 20 mm without the rail layer, so the total lid is about 29 mm [est] (A: 37.6).

**B2:** adds two half-width side leaves folded onto the centre leaf, for twice the area. Lid about 35 mm [est].

**B-base (variant noted, not modeled):** the leaf is hinged at the lid's hinge-side edge and deploys onto the table or a prop behind NOMAD.
- Its weight is carried by the table, so there is no tipping lever.
- Its orientation is limited to low tilt unless propped.

**Strengths:**
- **Solar angle independent of the display angle.** It can reach overhead, and in the visor position (leaf over the top, facing the sky in front) it also works with the sun behind the user and shades the screen.
- **Charges while closed.** The stowed cells face out: a closed NOMAD lying in the sun charges.
- **Few simple parts:** 2 hinges, 1 angle lock, 1 latch, 1 leaf.
- **Cable routing:** single-axis folds, and the lid path is shared with the display cable.
- **Thinner lid** (about 29 vs 37.6 mm).
- A growth path to about 20 W (B2, with ground support).

**Weaknesses:**
- The cells are the **exterior** in transport: scratch and impact risk (ETFE tolerates it; glass would not).
- **Deployed mass and wind area sit high and behind the rear tipping edge.**
- Stowed heat on the lid unless it is air-gapped.
- The 295 mm leaf tray exceeds 256 mm print beds.
- The GNSS antenna can no longer use the lid back.

## 4. Quantitative estimates

### 4.1 Solar area and power

**Inputs:**
- Module area from the envelopes, minus frame margins [est].
- Nameplate 150 / 170 / 190 W/m² of module area for small mono ETFE panels [assume].
- Real-world output at best orientation, clear midday: 0.55–0.70 × nameplate [assume] (heat, irradiance, controller losses).

| | Panels | Module area | Nameplate (low / typ / high) | Real, best orientation |
|---|---|---|---|---|
| A | 2 | 515 cm² (0 exposed when stowed) | 7.7 / **8.8** / 9.8 W | 4.8–6.1 W |
| B1 | 1 | 600 cm² (all exposed when stowed) | 9.0 / **10.2** / 11.4 W | 5.6–7.1 W |
| B2 | 3 | 1,182 cm² | 17.7 / **20.1** / 22.5 W | 11.1–14.1 W |

**Targets:**

| Target | A | B1 | B2 | Notes |
|---|---|---|---|---|
| **10 W** | No (≈ 9) | Marginal (≈ 10) | Yes | |
| **15 W / 20 W** | No | No | Yes (≈ 20) | B2 only with ground support (§4.3) |
| **30 W** | No | No | No | Would need a 3-layer stack or an external panel; not realistic for V1 |

**Context [assume]:** a Pi 5 system draws about 6–10 W. All options are **supplementary** power. About 20–30 Wh/day for A/B1 and 45–55 Wh/day for B2, at about 4 good sun hours.

### 4.2 Mass [est]

| | Solar assembly | Main items |
|---|---|---|
| A | **≈ 590 g** | 2 laminates 148, 2 trays 140, 2 rails 90, carriages 16, pin / lock / stop hardware 74, wiring 30, deeper lid frame + slot reinforcement 90 |
| B1 | **≈ 410 g** | Laminate 162, ribbed tray 160, hinges 20, angle lock 25, latch 10, wiring 20, air-gap standoffs 15 |
| B2 | **≈ 780 g** | B1 + 2 half leaves (laminate 157, trays 160, hinges / latches / jumpers 50) |

- All solar mass sits in the lid in both architectures.
- Lid totals [est]: A about 1.19 kg; B1 about 0.89 kg (lid core lighter without the rail layer); B2 about 1.26 kg.
- **B1 does not create an unusually heavy lid:** it is lighter than A's.

### 4.3 Centre of gravity, tipping and lid-hinge torque [calc; base 1.45 kg at y 120 assumed, light 1.15, heavy 1.80]

**Frame:** the lid hinge is at the base **rear face** (D-006). The rear bottom edge (y 235) is the tipping edge. Wind comes from the front (the worst case).

| State (lid 110° unless noted) | CoG ahead of the rear edge | Static restoring | Lid-hinge gravity torque | Front-wind tip speed, light / nominal / heavy base |
|---|---|---|---|---|
| A (stowed or wings out; same side view) | 36 mm | 0.94 N·m | 0.70 N·m | 6.8 / **8.3** / 10.3 m/s |
| A, lid 125° | 25 mm | 0.65 | 0.98 | 5.3 / 7.4 / 9.8 |
| B1 stowed | 49 mm | 1.13 | 0.50 | 7.6 / 8.9 / 10.7 |
| B1 leaf 60° | 29 mm | 0.66 | 0.97 | 4.8 / 6.6 / 8.7 |
| **B1 leaf ≈ horizontal (overhead sun)** | 22 mm | 0.50 | **1.14** | 3.1 / **5.1** / 7.2 |
| B1 lid 125°, leaf horizontal | 8 mm | 0.19 | 1.44 | 0 / 3.6 / 6.7 |
| B1 visor (leaf over the top) | 26 mm | 0.61 | 1.03 | 3.5 / 5.1 / 6.8 |
| **B2 ≈ horizontal (cantilevered)** | **−12 mm (tips)** | **−0.33** | **1.97** | Tips at rest |

**Readings:**
1. **NOMAD is already tipping-sensitive with any lid-side mass**, because the lid hinge sits on the tipping edge. A itself tips in a 7–8 m/s front wind at lid 110–125° [calc]. This is a NOMAD-level issue from D-006, not only a solar one.
2. **B1 deployed** roughly halves the wind margin (≈ 5 m/s nominal, horizontal leaf) and **raises the lid-hinge holding torque to about 1.1–1.4 N·m**. It needs friction / torque lid hinges of that class **and** a simple fold-out rear stay (leaf edge or lid to the table) for any real wind.
3. **B2 cantilevered from the lid top is not viable.** Its CoG passes the tipping edge at rest. B2 only works ground-supported (B-base style or with a stay).
4. **A with one wing deployed:** the lateral CoG shift is about 14 mm [est], negligible against the 150 mm half-width. The asymmetric load is only on the one rail / hub.

## 5. Thermal comparison [est; full sun 1,000 W/m², absorptance 0.9, still air to light breeze]

| Surface / state | Temperature rise above ambient |
|---|---|
| Exposed dark PETG lid shell (A stowed; B deployed lid back) | +45 … +69 K |
| B stowed, laminate bonded / in contact with the lid (back insulated) | +43 … +64 K |
| B stowed, 4–6 mm **vented** air gap | Leaf +35 … +50 K; **lid shell beneath +14 … +28 K** |
| Deployed panel, free on both sides (A wing / B leaf), charging | +25 … +37 K |

**Conclusions:**
- **B1 with a vented gap is thermally no worse, and likely better, than A.** The leaf shades the lid shell, while A's (or any) dark lid back takes the full sun directly.
- **Bonded directly to the lid, B is a real risk:** the display back can reach about 70–90 °C in still air at 25–30 °C ambient. That exceeds typical LCD operating limits (about 50–70 °C [assume]) and approaches PETG's Tg (about 80 °C).
- **Requirements for B:**
  - an air gap of ≥ 4–6 mm, open at the top and bottom edges;
  - a light-coloured or reflective lid shell under the leaf;
  - no display or controller electronics in contact with the leaf.
- **Charging while closed in the sun** puts the base (battery) under a warm lid. The charger must derate or cut off above the battery's charge limit (about 45 °C [assume]). This applies to B only, and is a firmware and thermal-sensor item.
- **Deployed,** both A and B cool on both faces. No difference.

## 6. Cable comparison [est]

| | A (per wing, ×2) | B1 | B2 |
|---|---|---|---|
| Length | ≈ 500 mm per wing | ≈ 500 mm | ≈ 600 mm + jumpers |
| Moving sections | **2 per wing (4 total):** a 158 mm slide service loop (R 20) and a **±80° twist at the hub, inside an 11.5 mm link** (cable offset 6.5 from the axis, so about 13 mm end displacement in 11.5 mm) | **2:** leaf hinge (single axis, ≈ 150°, loop R ≥ 20 or along the hinge axis) and the lid hinge (**shared with the display cable path**) | 4 (+2 side-leaf fold jumpers) |
| Slip ring | No (by D-004), but the twist is severe | No | No |
| Pinch / snag risk | Moderate: slide loop in the lid; twist at the hub | Low: loop at a hinge end, easy to guard | Low |
| Replaceability | Needs the cassette off; routed through the carriage and hub | Connector at the leaf; lid path as the display | Same + jumpers |
| Reliability | **The hub twist is the weak point.** Not resolved in D-009 (cable exit route open) | Standard laptop-hinge practice | Standard |

**Can B route power through the display-lid hinge?** Yes. The lid-to-base pass already exists (`KEEPOUT_LID_DISPLAY_PASS`), and a 2-conductor solar lead (e.g. 22–20 AWG) is thinner than the display flex [assume]. It adds no new hinge crossing beyond the leaf hinge.

## 7. Mechanical comparison

### Parts

| | A (per wing, ×2) | B1 | B2 |
|---|---|---|---|
| Sliders | Rail + carriage | — | — |
| Shafts / pins | Hub pin, index pin, 2 dowels, bushing | 2 hinge pins (off-the-shelf steel) | 6 hinge pins |
| Springs | 1 (index) | 0 (or in a detent hinge) | 0 |
| Stops | Slide end stops, stow interlock, ±80° stop (S1-R: yoke, stop plate, bushing, drive dowel) | Hinge travel stops (moulded) | + side-leaf stops |
| Locks | Index plate + pin + slider, **slide lock / stowed retention (not designed)** | 1 angle lock (friction hinge or strut with detents), 1 stow latch | + 2 leaf latches |
| Metal precision parts | Index plate, anti-rotation plate, stop plate, yoke, bushing, sleeve (EDM / CNC / reamed) | None | None |
| Printed parts | Cassette tray, carriage, slider, cover, rails, lid rail layer | Leaf tray, hinge knuckles, lock parts | + 2 trays |
| Screws | 4–6 | 4–8 | 10–14 |

**Rough totals:**

| | Parts | Complexity | Why |
|---|---|---|---|
| A | ≈ **40 parts** for two wings (≈ 14 metal, 6 of them precision) | **High** | Two coupled mechanisms (slide + indexed tilt) per side, precision fits, open sub-problems |
| B1 | ≈ **10–12 parts** | **Low** | One single-axis fold + lock + latch |
| B2 | ≈ **20–24 parts** | **Moderate** | Three single-axis folds + support |

### Structural difficulty (qualitative)

**A:**
- Lateral cantilever about 150 mm from the carriage.
- Rail and hub bending at the lid side walls.
- Tilt torque into the index lock, stop impact into the hub.
- **Known shortfall at the PETG hub bracket.**
- Wind moments are moderate and sit at mid-lid height.

**B:**
- The leaf is a **lever on the lid top** (hinge moment from the leaf's weight plus wind: 0.57 N·m at 10 m/s, 1.29 N·m at 15 m/s [calc]).
- The lid hinge must hold 1.0–1.4 N·m from gravity plus up to about 1–2 N·m of wind.
- Lid torsion if the leaf is loaded off-centre.
- **Panel flex** of a 295 × 229 printed tray needs ribs.

**Which is harder?** B's problem is **simpler** (a lever and hinge friction, fixable with a stay and torque hinges). A's problem is **harder**: precision small parts in PETG under concentrated loads.

**Wind:**
- B is **more wind-sensitive**: higher sail, rearward CoG. A is also marginal because of the rear-face hinge.
- Both need the lid to hold in wind.
- B needs a positive leaf lock (not friction alone) and a stay.
- A's index lock and stop take wing gusts; its hub torques are small (≤ 0.5 N·m at 15 m/s per wing [calc]).
- A sacrificial / fusible element is not needed in either if locks are positive. B's stay should be a cheap replaceable printed part.

## 8. Printability comparison

| | A | B1 / B2 |
|---|---|---|
| Structural parts in PETG | Yes, but **precision-critical**: 200 mm straight rails with 0.3 running fits, carriages, bracket bores | Yes, **tolerance-tolerant**: hinges ±0.2 are fine |
| Largest part | Cassette tray 147.5 × 200 (fits a 256 bed) | **Leaf tray 295 × 229: needs a ≥ 300 mm bed** (the base shell already does) or a 2-piece bonded / screwed tray |
| Flatness / warping | Small parts; rails must be straight (warp risk on long thin C-channels) | **Large thin flat tray: warp risk.** Ribbed tray, PETG, brim, flat orientation |
| Supports | Rails and carriage: some | Minimal (tray printed flat) |
| Inserts | Several | 4–8 |
| Non-printed | **Several EDM / CNC stainless parts, reamed holes** | **Only off-the-shelf pins, screws and maybe torque hinges** |
| Print time / material [est] | ≈ 10–14 h, ≈ 300 g | ≈ 6–9 h, ≈ 200 g (B2 ≈ 12–16 h, ≈ 380 g) |

**Summary:** A's print risk is **precision**. B's print risk is **flatness of one large part**, which is the more tractable problem for FDM.

## 9. UX comparison

| | A | B1 |
|---|---|---|
| Open | Unlatch lid; open | Same |
| Deploy | For each wing: release (slide retention not yet designed), slide out 158 mm → **2 + actions** | Release the leaf latch, swing the leaf to an angle (the lock holds) → **2 actions** |
| Aim at the sun | For each wing: hold the thumb tab, turn to an index, release → 2 × 3 actions; elevation limited by the display angle | Push the leaf to the desired angle (detents or friction); rotate NOMAD for azimuth |
| Stow | Each wing to 0° (interlock), slide in, latch | Fold the leaf, latch |
| Forget to lock | The index pin self-locks (spring). If the slide is unlatched, a wing can slide out in transport (retention not designed) | An unlatched leaf flaps in transport (latch mandatory; a magnet backup is cheap). In wind, a leaf on friction alone can slam: needs a positive lock |
| Intuitiveness | Moderate (two mechanisms per wing, hidden interlocks) | **High** (one familiar flap, like a laptop sun hood) |

**Orientation effectiveness [calc]** (best cosine factor; the user picks lid 100–125° and the azimuth):

| Sun elevation | A, sun behind device | A, sun behind user | B1, sun behind device | B1, sun behind user (visor) |
|---|---|---|---|---|
| 10° | 1.00 | 0.00 | 1.00 | 0.87 |
| 30° | 1.00 | 0.09 | 1.00 | 0.98 |
| 60° | 1.00 | 0.57 | 1.00 | 1.00 |
| 75° | 0.98 | 0.77 | 1.00 | 1.00 |
| 90° | 0.91 | 0.91 | 1.00 | 1.00 |

- **A works only with the sun behind the device** (the user facing the sun).
- **B1 works in both.** In the visor position it also shades the screen when the sun is behind the user.
- **A's independent left / right tilt gives no energy benefit for a single sun.** It helps only for split / diffuse aiming or to reduce self-shading.
- **Shading:**
  - A: wings sit beside the lid (little self-shading); the user may shade a wing when standing beside it.
  - B1: one panel with no panel-to-panel shading. Partial shading of one cell string cuts output strongly, as in any panel. Bypass diodes in the module help.
  - B2: coplanar leaves when unfolded (no mutual shading).

## 10. Cost comparison (relative; prices not checked)

| Category | A | B1 | B2 |
|---|---|---|---|
| Panels | 2 small custom-size laminates | 1 medium laminate (common size class) | 3 laminates |
| Machined / EDM metal parts | **Significant** (≈ 6 precision parts per side; small-batch EDM / CNC dominates cost) | None | None |
| Hinges / pins / fasteners | Pins, dowels, springs, screws | 2 hinges (printed + pins, or 2 torque hinges), latch, stay | + 4 hinges, latches |
| Printed material | ≈ 300 g | ≈ 200 g | ≈ 380 g |
| Wiring / connectors | 2 sets + slide loops | 1 set | 1 set + jumpers |
| **Relative V1 cost** | **Highest** (machining) | **Lowest** | Moderate |

## 11. Concept-model observations

**Onshape concept model:** not created.
- It would add an element to the production NOMAD document (the gate forbids changes there).
- A scratch Part Studio is not viewable by the owner.
- The generated side and front views answer the spatial questions.
- An isolated concept Feature Studio can be built on request.

**Side views** (`prototypes/P0.1/d010/d010_side_views.svg`, lid 110°, red dot = combined CoG, dashed = tipping edge). They show:
1. A's side view does not change when the wings deploy. Its CoG sits 36 mm inside the tipping edge.
2. B1's leaf positions (stowed, 60°, horizontal, visor) move the CoG from 49 mm to 22–26 mm inside the edge.
3. The leaf sits high above the lid top. Its lid-hinge wind moment is about 1.9× A's wings (0.98 vs 0.51 N·m at 10 m/s [calc]).

**Front views** (`d010_front_views.svg`):
- A's deployed span is 612 mm at lid mid-height.
- B1's leaf stays within the 301 mm width.
- B2 unfolds to about 590 mm at the lid top.

## 12. Decision matrix (no overall score)

| Criterion | Sliding wings (A) | Solar lid (B1; B2 where noted) |
|---|---|---|
| Solar area | 515 cm², fixed | 600 cm² (B2 1,182) |
| Solar orientation | 1 axis per wing, ±75° **relative to the lid**; rear hemisphere only | 1 axis, **independent of the display**; rear + visor front; reaches overhead |
| Real-world effectiveness | ≈ 5–6 W best; only with the sun behind the device | ≈ 6–7 W best, both sun directions; **charges while closed** |
| Weight | ≈ 590 g | ≈ 410 g (B2 780) |
| Mass distribution | Lateral, symmetric when both deployed | Rearward / up when deployed |
| Centre of gravity / tipping | Unchanged by deployment; tips at ≈ 8 m/s (rear hinge, D-006) | Deployed: tips at ≈ 5 m/s without a stay; **B2 tips at rest** unless ground-supported |
| Mechanical complexity | **High** (≈ 40 parts, precision) | **Low** (≈ 10–12) |
| Structural difficulty | High: small precision PETG / metal joints; **open hub-bracket shortfall** | Moderate: leaf lever, lid hinge 1.0–1.4 N·m, flat-panel stiffness |
| 3D-printability | Precision rails / fits + machined metal | Large flat tray (bed ≥ 300); otherwise tolerant |
| Cable routing | 4 moving sections; **±80° twist in 11.5 mm** | 2 moving sections; shares the display hinge path |
| Heat | Cells protected; dark lid shell in the sun | Needs a vented gap; then equal or better (the leaf shades the lid) |
| Wind sensitivity | Moderate | **Higher** (needs a positive lock + stay) |
| Display impact | None beyond a 37.6 mm lid | Lid about 29 mm; lid hinges must hold ≈ 1.1–1.4 N·m deployed |
| Chassis impact | Rail layer, side-wall slots, 612 mm lateral clearance | Thinner lid (**may relieve the rear-plug conflict**, not modeled); GNSS antenna moves off the lid back |
| Portability | Cells protected; flat lid | Cells are the exterior (scratch / impact); thinner package |
| Serviceability | Cassette via hub parts; many small parts | Leaf off via 2 hinge pins + 1 connector |
| V1 cost | Highest | Lowest |
| Deployment UX | 6 + steps, hidden interlocks | 2 steps, familiar |
| Failure modes | Hub bracket, cable twist, slide retention, stop impact on small parts | Unlatched leaf flaps; wind slams the leaf or tips the unit; stowed heat if no gap |
| Future scalability | Poor (a thicker lid for more area) | B2 / ground-supported leaves to about 20 W |

## 13. Recommendation

### Architecture A — strongest arguments
- Cells protected inside the lid.
- Deployment doesn't move the CoG rearward.
- Much of the detailed design is already done and validated in geometry.

### Architecture B — strongest arguments
- **Far simpler:** about ¼ of the parts and no precision metal.
- **Cable path is standard single-axis hinge practice.**
- **Better orientation:** independent of the display, both sun directions, overhead.
- **Charges while closed.**
- Same or more power (≈ 10 W B1; path to ≈ 20 W).
- Lighter and thinner lid.
- Printable in PETG with off-the-shelf hardware.

### Critical unknowns
1. **Base mass and its CoG** [unknown: battery not chosen]. They decide the tipping margin for both architectures.
2. **Lid hinge hardware and holding torque** (D-006 hardware is TBD). B needs about 1.1–1.4 N·m.
3. **Real panel:** mass, efficiency and size availability [assume 2.5 kg/m², 170 W/m²].
4. **User sun orientation in practice:** sun behind the device vs behind the user.
5. Real stowed temperatures with a vented gap.
6. How much wind V1 must tolerate.

### Engineering risks
- **A:** the unresolved hub-bracket shortfall; the cable twist; the machining cost and schedule for January 2027; the untested precision fits in PETG.
- **B:** tipping / wind with the leaf deployed (needs a stay); lid-hinge torque; stowed heat (needs the gap); exterior cell damage; flatness of a large printed leaf.

### What would need to change in NOMAD

**For A:**
- Resolve the hub bracket (outboard bearing), the S1-R stop, the cable twist, and the slide retention.
- Keep the 37.6 mm lid.

**For B:**
- A new lid stack: remove the rail layer; add a vented gap and the leaf.
- Leaf hinge and angle lock at the lid top.
- Specify the lid hinge torque.
- Add a rear stay.
- Move the GNSS antenna off the lid back.
- Add a charger thermal cutoff.
- A ≥ 300 mm print bed (already needed for the base).
- The D-009 solar-wing mechanism would be retired, kept as an analysis record.

### **RECOMMEND ARCHITECTURE B** (B1: single top-hinged leaf with positive angle lock, vented air gap and a fold-out rear stay)

**Condition:** a **one-day physical mock-up** before any production CAD, with a printed or cardboard lid and leaf, real-mass ballast for base, lid and panel, and a hinge with a torque gauge. Measure:
1. the tipping angle and wind (fan) margin with and without the stay;
2. the lid-hinge holding torque needed;
3. the leaf-lock holding under a push.

If B1 cannot be made stable with a simple stay at the expected base mass, the fallback is **B-base** (the leaf deploys onto the table behind NOMAD). This is still simpler than A.

**B2 (about 20 W) is a later option only in a ground-supported form.**

This is not "too close". A's remaining problems are precision and reliability problems in exactly the areas V1 cannot afford (PETG, no machining, schedule). B's problems are simple statics, checkable in a day.

## 14. Remaining unknowns

The critical unknowns above, plus:
- **LCD temperature limits** of the chosen display [unknown].
- **Whether ETFE laminates of the needed size exist off the shelf** [unknown; not researched].
- **Bed size of the owner's printer** [unknown].
- **Rear-plug conflict:** whether the thinner B lid actually resolves it [est only; not modeled].
- **Real-world user behaviour** outdoors.

## 15. Exact next step after owner approval

**If B is approved:**
1. Record D-010 (architecture choice) and mark D-009 / S1 / S1-R as **superseded (analysis records)**.
2. Build the one-day mock-up (§13) and record the measurements (P0.2-class physical test).
3. **Round F, lid re-architecture study** (analysis + local model, then Onshape on approval):
   - lid stack without the rail layer;
   - leaf envelope, hinge line, angle-lock concept and stay;
   - vented gap;
   - lid-hinge torque requirement;
   - rear-plug check;
   - new YAML parameters as TBD / working.

**If A is chosen instead:**
1. Resolve the D-009 hub-bracket shortfall (rigid-yoke / outboard-bearing study).
2. Resolve the cable twist and the slide retention.
3. Then integrate S1-R.

---

**SOLAR ARCHITECTURE STUDY COMPLETE — AWAITING OWNER DECISION**
