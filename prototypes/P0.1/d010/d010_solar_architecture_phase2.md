# D-010 Phase 2: solar architecture engineering study, A (sliding wings) vs B1 (solar-lid leaf)

**Status:** study complete, **awaiting owner review**. This is not production CAD and does not approve anything.

| | |
|---|---|
| Calculation script | `CAD/tools/d010_phase2_study.py` (standard library only; `--emit` regenerates the Onshape data block and the kernel-check expectations) |
| Onshape concept model | Feature Studio **`NOMAD_D010_Concepts`** (element `d4619014058afc59574f42aa`) in the NOMAD document. New and isolated: it imports nothing from production and nothing references it. Custom feature **"NOMAD D010 Concepts"**. |
| Local snapshot | `CAD/featurescript/NOMAD_D010_Concepts.fs` (the text written to Onshape) |
| Scratch kernel harness | `CAD/featurescript/NOMAD_D010_Concepts.test.fs` (never written to Onshape) |
| Phase 1 | `prototypes/P0.1/d010_solar_architecture_comparison.md` (preserved; §3 below lists what Phase 2 corrects) |

**Evidence tags** used below:

| Tag | Meaning |
|---|---|
| **MEASURED** | Nothing in this study is measured. |
| **VENDOR** | Manufacturer web data retrieved 2026-09-28; not checked by us. |
| **CALC** | Calculated by the script from the tagged inputs. |
| **KERNEL** | Evaluated by the Onshape geometry kernel in the scratch check. |
| **EST** | Engineering estimate. |
| **ASSUMED** | No data behind it. |
| **UNKNOWN** | Not determinable yet. |

**Architecture labels:** **A** is the sliding-wing design; **B1** is the single leaf hinged at the lid's top edge (on the lid back).

**Symbols** (all angles in degrees):

| Symbol | Meaning |
|---|---|
| φ | Display (lid) angle; 0 = closed, 110 = the usual working angle |
| ψ | B1 leaf angle; 0 = stowed flat on the lid back, 190 = standing upright above the lid |
| *d* | Cable outer diameter |

## 1. Executive summary

- **Recommendation: B1 proceeds (RECOMMEND B1), conditional on the physical checks in §23.** The reason is not that B1 wins everywhere. Phase 2 found that B1's Phase 1 advantages in mass and screen shading were overstated.
  - **A's remaining problems are built into the design.**
    - The cable cannot get from the carriage into its service loop without passing through the structural rail wall. This is unresolved.
    - The hub-link cable bends at 2.5–3.9 × *d* where about 6 × *d* is needed.
    - The hub bracket is below safety factor 2.
    - It needs precision metal parts and custom-size PV laminates.
  - **B1's problems each have a simple, cheap fix that a one-day mock-up can verify:**
    - tipping → a stay;
    - heat → a 6 mm vented gap plus foil;
    - hinge torque → catalog friction hinges.
- **Power:**
  - B1 carries a real catalog panel (Voltaic P108, 273 × 223 × 4 mm, 9.5–10.9 W, 328 g — VENDOR) that fits the leaf.
  - A reaches about 8.8 W only with custom-size laminates (availability ASSUMED); the largest catalog panel that fits its cassette gives 2 × 2.6 W.
  - Realistic output at best aim is B1 5.6–7.1 W vs A 4.8–6.1 W (CALC; custom laminate for A).
- **Where the sun can be:**
  - Sun behind the device: both architectures are equal.
  - Sun behind the user: A is useless (cosine 0–0.57); B1 reaches 1.0 (0.56 at 10° elevation, when the operator's body shades it).
  - Sun from the side or overhead: B1 is slightly better, with no self-shading (A 11–15 %).
- **Mass: a tie.** A 2.64 kg vs B1 2.62 kg in total (CALC from EST).
  - The catalog FR4-backed panel and the stay cancel B1's thinner-lid saving.
  - The Phase 1 "B1 is 180 g lighter" is withdrawn.
- **Stability without a stay:** B1 is worse at high leaf angles.
  - It tips at 5.4–5.5 m/s with the leaf horizontal or upright, and 2.4 m/s upright at φ 125.
  - A tips at 8.3–10.6 m/s.
  - A NOMAD with the lid open and nothing deployed tips at about 11 m/s (all CALC).
- **Stability with the stay:** two stainless outrigger arms (3 × 16 mm, 105 mm reach) raise B1 to 11.4–18 m/s and A to 18.2 m/s.
  - **For B1 the stay is required; for A it is optional.**
- **Hinges:**
  - B1 needs display hinges with about 1.5× A's holding torque: gravity up to 1.8 N·m nominal / 2.1 heavy, vs 1.1 / 1.4 for A.
  - B1 also needs two leaf friction hinges of about 0.8 N·m each.
  - Both are catalog-class parts (not selected).
- **Cables:**
  - **A:** two cables, 0.73 m and 1.30 m (CALC). Each has four moving sections, including the unresolved rail-wall crossing. The right cable's hinge twist is 7.1°/mm (too tight).
  - **B1:** one cable, 0.85 m. It has two axial twist zones at 2.75°/mm and no loop, crossing or S-bend.
  - **A's cable routing is not acceptable for V1 as currently defined.**
- **Thermal:** B1's panel is always exposed.
  - Closed in full sun on a 35 °C day, the display rises +18–32 K vs A's +14–21 K with a dark lid.
  - With the recommended 6 mm vented gap plus low-e foil on the lid back, B1's display rise drops to +15–22 K.
  - **The 4 mm gap barely ventilates.** Chimney h ≈ 0.8 vs 2.4 W/m²K at 6 mm.
  - **Both architectures have a PETG heat problem:**
    - A's dark lid shell reaches about 90 °C;
    - B1's leaf frame sits at panel temperature (66–91 °C).
    - The sun-exposed parts should be ASA or light-coloured.
- **Screen visor: B1 cannot shade the screen while generating power (corrects Phase 1).** With a fixed top-back hinge, a leaf tilted over the screen has its cells facing the table. Only a removable, reversible leaf could do both; that is not part of the recommendation.
- **Onshape:** both architectures are modelled on one shared base with six named states each.
  - The kernel cross-check matches Python exactly: CG error 0.00004 mm; A lid to plug keep-out +1.200; B1 stack to plug keep-out +2.072; leaf to lid +1.141 mm.

## 2. Inputs

All envelope values come from `nomad.yaml` working values through `e_lid_layout.py` / `base_v01_layout.py`. They are provisional, not validated.

| Input | Value | Tag |
|---|---|---|
| Base | 301 × 235 × 40; display hinge axis y 235, z 40 (D-006) | YAML |
| A lid | class A 37.6 (lip 1, display 5, gap 1, rail layer 13, gap 1, cassette 8, gap 2, shell 6.6) | YAML |
| A solar | 2 cassettes 147.5 × 200 × 8; slide 158; tilt ±75 (index), ±80 stops (S1-R study) | YAML |
| B1 lid | core 19 (lip, display, gap, controller zone, thin shell) + vented gap 6 + leaf 6 = 31 | EST |
| B1 leaf | 289 × 235 outline; axis at y 4, z 69 (barrel inside the envelope); ψ 0–190 | design (this study) |
| Catalog panel for B1 | Voltaic P108: 273 × 223 × 4, 328 g, 9.5 W (datasheet) – 10.9 W (listing), 18 V, ETFE on 2 mm FR4, US$65 | VENDOR |
| Catalog panel for A | Voltaic P126: 136 × 112, 79 g, 2.6 W. The P105 (148 × 221) does **not** fit the 147.5 × 200 cassette | VENDOR |
| Custom laminate | 150 / 170 / 190 W/m² nameplate; 2.5–3.2 kg/m² | ASSUMED |
| Real / nameplate | 0.55–0.70 at best aim, clear midday | ASSUMED |
| Base masses | component list in the script, 1.07–1.94 kg, nominal 1.465 kg; the battery is not chosen | EST / ASSUMED |
| Feet | 4 mm high, inset 8 mm; the table plane is z = −4 | ASSUMED |
| Wind | ρ 1.2; plate normal force Cn = min(1.2, 2.5·α); worst of azimuth ±30° and gust inclination −10/0/+10° | ASSUMED |
| Thermal | 1000 W/m², absorptance 0.9 (PV / dark) or 0.5 (light grey); h_top 14 (still) / 22 (light wind); ambient 35 °C | EST |
| Cables | A Ø6, loop R20 (YAML); B1 Ø4 2 × 0.5 mm² silicone; static bend 3 × *d*, repeated flex 6 × *d*; twist limit 3.5°/mm | ASSUMED |

## 3. Assumptions and corrections to Phase 1

- **Corrected: the visor.** Phase 1 said B1 "in a visor position works with the sun behind you while shading the screen". This is wrong for a leaf hinged at the lid's top-back edge (CALC §14).
- **Corrected: mass.** Phase 1 used a 2.5 kg/m² laminate for B1. The real catalog panel that fits is FR4-backed at 5.4 kg/m² (VENDOR), and B1 now also carries a stay. Total mass is equal (§7).
- **Corrected: tipping model.** Phase 1 tipped about the base outline and treated all surfaces as normal to the wind. Phase 2 uses the foot support polygon, a 3-D plate model with incidence, gusts and azimuth, and a real stay geometry.
- **Kept from Phase 1:** base CG from the component layout (now calculated, not assumed); the D-006 rear hinge; the D-009 load results for A (not redone).
- **Named states:**
  - A: NORMAL = wings out, tilt +65 at φ 110; MAX = φ 125, tilt +75; ONE_WING = asymmetric.
  - B1: NORMAL = ψ 65 (normal at 45°), stay stowed; MAX = ψ 190 upright plus stay; STAY_DEPLOYED = ψ 110 (horizontal) plus stay.
- **Recommended B1 stay rule (ASSUMED):** deploy the stay whenever ψ > 45° or it is windy.

## 4. Architecture A (as modelled)

- **Lid:** class A 37.6 lid with side slots.
- **Solar hardware, per side:** a C-channel rail (structural) and a carriage.
  - Hub parts on the carriage: a 5 mm hub pin (D-009 anti-rotation), a D-009 index plate (a local candidate, not in production Onshape) and an S1-R stop-yoke envelope (study only).
  - Parts that tilt with the cassette: the PETG hub bracket (open item: below safety factor 2) and a 147.5 × 200 tray carrying a custom 135.5 × 190 laminate.
- **Cable:** a rolling service loop in the E2 reserve band. The loop apex sits inboard, consistent with LPX0 = KX0 − 2R.
- **Existing loads (not redone):** hub design torque T_d 1.26 N·m. S1-R passes as a stop. The hub bracket is at bearing 1.88 / tear-out 1.73 / tension 1.61, below safety factor 2 (open).
- **Kernel:** a fully deployed wing clears the lid side wall by 8.0 mm (= SOLAR_DEPLOY_CLEARANCE), and the bracket clears it by 8.0 mm.

## 5. Architecture B1 (as modelled)

**Lid:**
- Core 19 mm, with low-e aluminium foil on its back.
- Vented air gap: 6 mm between the lid back and the panel back.
  - Vents: the rear bar has an open window at |x| < 110; the front (hinge) bar has one at |x| < 30. The hinges occupy the rest of the front bar.

**Leaf:**
- An open-back frame in two halves (144.5 × 235 each), spliced at x = 0.
- It holds the rigid P108 panel in a rebate under a 2 mm lip.

**Hinges:**
- Two catalog constant-torque friction hinges at x = ±55.
- A hollow cable knuckle on the axis (x 72–140.5); the cable twist zone runs inside it.
- An idler knuckle with a 4 mm pin on the left.

**Other parts:**
- A stow latch at the leaf's free edge.
- A 2-pin panel connector in the leaf, so the panel can be removed.
- The stay: two stainless flats (3 × 16 mm) on M4 shoulder-screw pivots in the rear hinge-mount corners (x ±125, y 222).
  - Stowed: they point forward under the base in the foot gap.
  - Deployed: they point rearward, with the feet at y 327.

**Relief at the leaf underside:** the front-bottom corner of the leaf underside is 8.94 mm from the leaf axis, while the axis is 8.0 mm above the core top. A square corner would dip 0.94 mm into the core at ψ ≈ 27 (CALC). The modelled relief (y < 4, z < 63.3) keeps 1.0 mm. Kernel: leaf to lid is 1.141 mm at ψ 45 (KERNEL = CALC).

## 6. Solar area and power

| | Physical max | Panel as modelled | Nameplate | Real, best aim | Day (2–5 peak-sun-hours) | Stowed exposed |
|---|---|---|---|---|---|---|
| A, custom laminate | 590 cm² (2 cassette faces) | 515 cm² (2 × 135.5 × 190) | 7.7 / 8.8 / 9.8 W | 4.8–6.1 W | 10–31 Wh | 0 (inside the lid) |
| A, catalog (2 × P126) | | 305 cm² | 5.2 W | 2.9–3.6 W | 6–18 Wh | 0 |
| B1, catalog (P108) | 679 cm² (leaf outline) | 609 cm² | 9.5–10.9 W | 5.6–7.1 W | 11–36 Wh | 609 cm² (charges closed) |
| B1, custom laminate | | 618 cm² | 9.3 / 10.5 / 11.7 W | 5.8–7.4 W | 12–37 Wh | 618 cm² |

Tags: CALC; VENDOR for the catalog rows; ASSUMED for the custom rows and the real/day factors.

Neither design reaches 30 W: solar is supplementary for a 6–10 W Pi system. Whether custom-size ETFE laminates are commercially available at V1 quantities (1–3 pieces) is **UNKNOWN**.

## 7. Mass

Nominal values, with the low–high range in brackets; CALC from EST items.

| Group | A | B1 |
|---|---|---|
| Base (common) | 1465 g (1070–1940) | 1465 g |
| Display + controller + hinge (common) | 210 g (160–280) | 210 g |
| Lid structure | 435 g (350–520), class A 37.6 | 342 g (278–420), core 19 + vent spacers |
| Solar subsystem | 528 g (439–690) | 603 g (510–702), stay included |
| **NOMAD total** | **2.64 kg (2.02–3.43)** | **2.62 kg (2.02–3.34)** |

- **A solar, both sides:** rails 90 g, carriages 16 g, hub/index/spring 50 g, S1-R hardware 24 g, trays 140 g, laminates 148 g, wiring 40 g.
- **B1 solar:** P108 panel 328 g (VENDOR), frame 90 g, friction hinges 40 g, knuckle 8 g, latch 10 g, wiring 22 g, gap spacers 12 g, stay 105 g.
- **B1 with a custom semi-flexible laminate instead of the P108:** the leaf is 214–258 g instead of 328 g. This is an option if a laminate supplier is found.
- **Distribution:** the base is 55 % of the total in both designs. The lid assembly is 44 % (A) and 43 % (B1).

## 8. Centre of gravity

World frame, mm, nominal masses (CALC). In Onshape, each CG marker's part name carries the same values.

| State | A: x / y / z | B1: x / y / z |
|---|---|---|
| 1 STOWED (closed) | −7.2 / 114.4 / 38.7 | −6.1 / 116.6 / 35.4 |
| 2 DISPLAY OPEN (φ 110) | −7.2 / 190.1 / 73.3 | −6.1 / 186.6 / 69.1 |
| 3 PARTIAL | −7.2 / 190.1 / 73.3 (wings half out) | −6.1 / 196.4 / 68.3 (ψ 30) |
| 4 NORMAL (sun behind, 45°) | −7.2 / 189.8 / 74.6 | −6.1 / 206.5 / 73.6 |
| 5 MAX | −7.2 / 200.5 / 66.6 (φ 125, +75) | −6.1 / 198.4 / 105.7 (ψ 190 + stay) |
| 6 SPECIAL | +4.6 / 189.1 / 73.8 (one wing) | −6.1 / 214.1 / 87.0 (ψ 110 + stay) |
| Worst rearward CG | y 206.6 at φ 135, tilt 45 | y 234.3 at φ 135, ψ 135: **behind the rear feet line (y 227)** |

- **Rearward movement of the CG from stowed:** A 75–86 mm; B1 70–98 mm.
- **A's wings slide sideways and move the CG only laterally**, by up to +11.8 mm in x with one wing out.
- **B1 at φ 135 with the leaf near horizontal would tip over by gravity alone, with no wind, unless the stay is deployed** (CALC).

## 9. Tipping and stability

Rear tip-wind speed with nominal masses (CALC). The ranges in brackets are for light and heavy bases.

| State | A | B1 without stay | B1 with stay |
|---|---|---|---|
| Lid open, nothing deployed (reference) | 10.6 m/s | 11.1 | — |
| Partial | 8.9 | 7.5 | — |
| Normal | 9.4 (7.7–10.9) | 8.3 (5.8–10.6) | 18.1 |
| Leaf horizontal (ψ 110) | — | 5.5 (3.3–7.4) | **18.0 (15.2–20.9)** |
| Max: A φ 125 +75; B1 upright ψ 190 | 8.3 (6.5–9.7) | 5.4 | 11.6 |
| B1 upright at φ 125 | — | **2.4** | 11.4 |
| A max + the same stay | 18.2 | | |

- **Front tipping** (wind from behind the device): 12–36 m/s, not critical.
- **Side tipping:** 19.5–49 m/s. The side margin is 135–138 mm, and the panels meet a side wind edge-on in both architectures.
- **Handling:** a rearward push at the top edge tips any laptop-like device. It takes 3.6 N for A and 3.9 N for B1 with the lid open, 6.9–11.5 N for B1 with the stay, and only 1.5–2.0 N for B1 without the stay with the leaf deployed (CALC). Users will hold the base, as they do with laptops, but **B1 without the stay is noticeably twitchy**.
- **Assumptions:** the flat-plate Cn model is conservative for a leaf partly in the lid's wake; the wind is steady (gust factor not included); the table is rigid and flat. **Not experimentally validated.**

## 10. Hinge torque

**Display (lid) hinge.** Gravity holding torque, with the heavy-parts figure in brackets (CALC):

| | φ 110 | φ 135 | ×1.5 total requirement |
|---|---|---|---|
| A | 0.63–0.67 (0.84) N·m | 1.04–1.09 (1.37) | ≈ 2.1 N·m for 2 hinges (~1.0 each) |
| B1 | 0.60–1.25 (1.46) | 0.99–1.82 (2.14) | ≈ 3.2 N·m for 2 hinges (~1.6 each) |

- A front wind of 10 m/s adds 1.1 N·m (A) or 2.3 N·m (B1). Hinges are not expected to hold this; the φ-max stop takes it.
- **A φ-max hard stop (≈ 125–135°) is needed in both architectures.**
- Friction hinges of 1–2 N·m each are typical laptop hardware (EST; not selected).

**B1 leaf hinge:**

| Item | Value |
|---|---|
| Gravity | ≤ 0.49 N·m (heavy 0.55) |
| Wind | 0.14 N·m at 5 m/s; 0.56 N·m at 10 m/s (Cn 1.2) |
| Holding requirement | (0.55 + 0.56) × 1.5 = **1.66 N·m → 0.83 N·m per hinge** |
| Deploy force at the free edge | ≈ 9.6 N |
| Closing force | ≈ 7 N |
| Hinge shear | weight + 10 m/s wind ≈ 10 N total, 5 N per hinge; bearing on a 4 mm pin in a printed knuckle ≈ 0.16 MPa (negligible) |

**Hinge options:**

| Option | Verdict |
|---|---|
| Printed hinge alone | Strong enough for the load, but wears, creeps (heat) and slops. Not for the friction function. |
| Metal pin + printed knuckles | Realistic for the idler and cable knuckles. |
| Off-the-shelf constant-torque hinges | **Preferred** for the leaf angle: 2 catalog parts give the hinge and the angle hold together (cheap generic 0.5–1.5 N·m types to Southco / Reell class; EST price €3–15 each; UNKNOWN until selected). |
| Locking hinge | Not needed with a stay and friction hinges. A detent strut is the fallback if friction slips in gusts. |

**A (existing results, not redone):** hub T_d 1.26 N·m; the hub bracket is below safety factor 2 (open); the rails carry the structural load; the S1-R stop path passes.

## 11. Stay / support

Rear tip wind with the leaf horizontal (φ 110, ψ 110), nominal masses (CALC):

| Option | Result | Verdict |
|---|---|---|
| None | 5.5 m/s | Not acceptable for B1's high leaf positions |
| **Rear outrigger arms** (sliding / folding rigid) at x ±125, reach 60 / 90 / 105 | 12.9 / 16.3 / **18.0** m/s | **Chosen**: independent of the lid angle; stows flat; purely vertical foot load |
| Same arms at x ±60 | equal rear value; side value 22.9–26 | No benefit, weaker base region |
| Lid-side folding props, pivot 60 from the hinge (175 long) | feet y 412, 29 m/s | **Rejected:** the prop sits 57° from vertical and needs foot friction μ ≥ 1.5 (rubber ~0.6–0.9); the foot moves with φ |
| Lid-side props, pivot 100 (135 long) | 14.5 m/s | Rejected: cannot reach the table at φ ≤ 95; the stay length depends on φ |
| Telescoping prop | — | More parts for the same function as the outrigger; rejected for V1 |
| Hinged printed leaf strut (leaf to lid) | Holds the angle only; no tipping gain | Only as a fallback for friction hinges |
| Table / ground fallback | The leaf cannot reach the table from the lid top at φ 110–125 | Operating fallback instead: fold the leaf back (ψ 0, still charging, 11.1 m/s), or remove the leaf and lay it on the ground using a cable extension (this needs a lift-off leaf; see §17) |

**Minimum practical stay:**
- Two 3 × 16 mm stainless flats (1.4301 cold-rolled), 117 mm long (12 root + 105 reach), each on an M4 shoulder screw into an insert in the rear hinge-mount corner block (x ±125, y 222).
- A detent at 0° and 180°.
- **Deployed:** the arms point rearward and the feet sit at y 327, outside the plug zones (x 20–110).
- **Stowed:** the arms point forward under the base side (x 117–133, y 117–234), inside the 4 mm foot gap and clear of the feet (KERNEL: arm to base 0.5 mm).

**Loads,** bounded by the heavy device resting entirely on the feet, × 1.5 (CALC):

| Load | Value |
|---|---|
| Foot load | 49 N total, 25 N per arm |
| Bending at the base edge | 2.26 N·m → 94 MPa in the 3 × 16 flat (cold-rolled yield ≥ 300 MPa, EST) |
| Root couple (over 12 mm) | 189 N on the pivot screw / insert (M4 insert pull-out in PETG ~1 kN, EST) |
| Mass | ≈ 105 g |

## 12. Cable routing

The anchor routes are the same in the script and in Onshape. The routes are drawn at the static bend radius (3 × *d*). **Moving sections** are the segments that bend or twist when the solar deploys.

| | A right | A left | B1 |
|---|---|---|---|
| Cable | Ø6 (YAML) | Ø6 | Ø4, 2 × 0.5 mm² silicone (ASSUMED) |
| Length (CALC) | 735 mm | 1297 mm (detours in front of its loop band, then crosses both rail bands where they end) | 852 mm |
| Moving sections | hub-link S-bend; carriage-to-loop crossing; rolling loop; right-knuckle twist | hub-link S-bend; carriage-to-loop crossing; rolling loop; centre twist | leaf-knuckle twist; centre display-hinge twist |
| Worst moving bend | S-bend R ≈ 15 mm = **2.5 × d** at 80° tilt (3.9 × *d* at 45°); loop R20 = **3.3 × d** | same | twist 2.75°/mm (190° over 69 mm; 135° over 49 mm) |
| Hinge crossing | right knuckle: 19 mm twist zone → **7.1°/mm (limit 3.5)** | centre pass: 1.88°/mm | centre pass (shared with the display cable): 2.76°/mm |
| Carriage-to-loop crossing | **Unresolved:** the cable centre (y 138.3) is inside the rail channel; the loop's moving run is outside the rail wall (y 149.1). The cable must cross a structural rail wall along the whole travel, or leave through the top slot, which has 1 mm under the stowed cassette. | same | none |
| Static corners below 3 × *d* | 5 corners, tightest 8 mm (hinge approaches and the U-turn detour) | 5 corners, tightest 10.5 mm | 1 corner, 11.9 vs 12 (negligible) |
| Connectors | cassette / carriage / power electronics (PE); service needs the cassette out | same | 2-pin connector at the leaf (the panel comes off) + PE |

**Verdict:**
- **A's cable architecture is not acceptable for V1 as defined.** Fixing it needs:
  - a hollow tilt axis, or a twist zone of at least 60 mm along the axis;
  - a new carriage-to-loop path that does not cut the structural rail;
  - a thinner cable (Ø4 gives a loop at 5 × *d*);
  - a proper right-hinge crossing.
- **B1's route is significantly simpler:** one cable, two single-axis twist zones, no loop.
- **Physical checks needed for B1:**
  - twist fatigue of the hollow knuckle;
  - the capacity of the centre display-hinge pass, which is shared with the display cable. The display cable's size is **UNKNOWN**.

## 13. Thermal

Temperature rise above ambient, full sun (1-D resistance network; **ESTIMATES**). Each cell gives still air / light wind.

| Case | A, dark shell | A, light grey | B1 gap 0 | B1 gap 4 | B1 gap 6 | **B1 gap 6 + foil** | B1 gap 10 |
|---|---|---|---|---|---|---|---|
| Closed, flat, sun on top: panel or shell | +57 / +38 | +32 / +21 | +53 / +36 | +54 / +37 | +55 / +37 | +56 / +38 | +55 / +37 |
| Closed: display | +21 / +14 | +12 / +8 | +32 / +22 | +28 / +19 | +27 / +18 | **+22 / +15** | +26 / +18 |
| Open, sun on the lid back: panel or shell | +55 / +37 | +31 / +21 | +49 / +34 | +48 / +34 | +43 / +31 | +46 / +33 | +39 / +29 |
| Open: lid-back shell (B1) | — | — | +47 / +33 | +35 / +24 | +27 / +19 | **+20 / +14** | +20 / +15 |
| Open: display | +13 / +8 | +7 / +5 | +22 / +15 | +16 / +11 | +12 / +9 | **+9 / +6** | +9 / +7 |
| Deployed panel, both sides free, charging | +23 to +36 (same physics for an A wing and the B1 leaf) | | | | | | |

**Findings:**
- **Radiation dominates the gap** (h_rad ≈ 7 W/m²K dark-to-dark), so a gap alone does little in the flat, closed case. Low-e foil (h_rad ≈ 0.9) is what cuts heat flow to the display.
- **Chimney ventilation is weak at 4 mm** (h ≈ 0.8 W/m²K per face) and useful at 6 mm (2.4). **Make "≥ 6 mm vented gap + low-e foil" a mechanical requirement** for B1. 10 mm adds little beyond 6.
- **At 35 °C ambient:**
  - Panels reach 66–91 °C. ETFE panels are typically rated to 85 °C: marginal on the hottest still days (EST).
  - A's dark PETG shell reaches 90–92 °C; B1's frame, which touches the panel, reaches 66–91 °C.
  - PETG's heat-deflection temperature is ~70 °C and its glass transition ~80 °C (EST).
  - **So sun-exposed parts should be ASA (heat-deflection temperature ~95 °C) or light-coloured in both architectures.**
- **The display closed in the sun:**
  - B1 with foil: 50–57 °C; A light grey: 43–47 °C.
  - Typical LCD storage limit is 60–70 °C (UNKNOWN until the panel is selected).
- **B1 "charges while closed":** on hot days this heats the base by a similar amount. Li-ion charging must be temperature-limited (≤ 45 °C) by the BMS or charger. **This is a real limitation**, not a showstopper.

## 14. Solar orientation

The device heading is fixed; the user sets φ 100–125 and the tilt or leaf. Only normals at or above the horizon count. Shading is ray-cast against the lid, base, other wing and a seated-operator box (ASSUMED). Values are cosine × (1 − shaded fraction), CALC.

| Sun | Elevation | A | B1 |
|---|---|---|---|
| Behind the device | 10 / 30 / 60 | 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 |
| Behind the user | 10 / 30 / 60 | **0.00 / 0.08 / 0.57** | 0.56 (44 % operator shade) / 1.00 / 1.00 |
| Right or left | 10 / 30 / 60 | 0.13 / 0.39 / 0.75 (the lid and the other wing shade 5–15 %) | 0.17 / 0.50 / 0.87 |
| Overhead | 90 | 0.91 | 1.00 |

- **Panel-normal elevation range at φ 110:** A −95 to +55 (so the wings can never face a sun behind the user); B1 −20 to +170.
- **Display blocking:** never for B1, because the leaf is above and behind the lid top edge. For A, the lid shades the far wing with the sun from the side.
- **Chassis:** blocks neither design.
- **Operator's body:** shades B1 below about 15° elevation with the sun directly behind the user.

## 15. Display interaction and the visor question

- **Visor: no.** The leaf's axis runs along its top-back edge, so tilting the leaf over the screen (ψ > 180 + (φ − 90)) turns its cells to face forward and down:
  - at ψ 250 the cells face (y −0.64, z −0.77);
  - at ψ 290 they face straight down (CALC).
  - **B1 cannot shade the screen while generating power.**
  - A removable, reversible leaf mounted face-up over the screen could do both, but it needs lift-off hinges and gives up the friction-hinge angle hold. It stays a possible later variant and is **not recommended for V1**.
- **Sun behind the user** (the case that washes out the screen): B1 still generates power (leaf ψ 130–170, above and behind the lid) but gives no shade. A generates almost nothing.
- **Sun behind the device:** the lid shades the screen in both designs, with the panels behind it.
- **Glare:** the B1 leaf above the lid can reflect into the user's eyes at some angles (matte ETFE, VENDOR); **UNKNOWN**, check in the mock-up.
- **Display hinge load:** B1 needs about 1.5× the holding torque of A (§10).

## 16. Stowed configuration and portability

| | A | B1 |
|---|---|---|
| Closed size (feet excluded) | 301 × 235 × 79.6 = 5.63 L | 301 × 235 × **73.0** = **5.16 L** |
| Mass | 2.64 kg | 2.62 kg |
| PV protection when packed | Inside the lid (protected) | **Exposed:** ETFE on FR4 resists scratches and does not flex-crack (VENDOR); point impacts from keys or rocks are a risk. The frame lip sits 2 mm proud; a padded sleeve is recommended for rough transport (EST) |
| Snag points | side slots, thumb sliders, hub zone | leaf edges, hinge barrels (inside the envelope), latch, stay under the base |
| Deployed footprint | 612 mm wide | 572 mm deep (leaf horizontal) + stay feet at y 327; upright leaf top at z 475 |
| Charges while packed | no | yes (hot-day battery limit, §13) |
| Backpack / case / vehicle | protected PV, but moving side parts can loosen | thinner, but the PV surface needs a sleeve; the leaf latch must hold under vibration (**UNKNOWN**) |

- **Rear-plug conflict** (known open item): A's lid enters the plug keep-out beyond φ ≈ 122 (−7.0 mm at 135, CALC = KERNEL at 120: +1.2). The thinner B1 stack stays clear up to φ ≈ 129 (+2.1 at 125, KERNEL) and is −2.3 mm at 135. **Improved, not solved.**
- **B1 leaf versus the table:** at φ ≥ 120 with ψ 10–60, the leaf's free edge touches the table (−7 to −44 mm, CALC). This does no damage (the leaf simply stops) but limits the leaf range at high lid angles.

## 17. Manufacturing (V1: PETG/ASA printed externally, cheap metal, budget €500–650 overall)

| | A | B1 |
|---|---|---|
| Largest printed part | lid frame 301 × 235 (both need a lid of this size) + 198 mm straight rails (precision) | lid core 301 × 235; **the leaf frame is 289 × 235** |
| Needs a bed > 300 mm? | lid: yes (same as B1) | whole leaf frame: 289 fits a 300 bed only without a brim, so warp risk. **Split into two halves (144.5 × 235) that fit any 256 × 256 bed** (and 250 × 210), joined by a spliced rear bar (M3 + inserts). The rigid FR4 panel bridges the split. |
| Metal / purchased parts | hub pins, stainless index plates (laser/EDM), dowels, springs, S1-R yoke / bushing / stop plate (jig-reamed), rails' straightness | 2 friction hinges, 1 × 4 mm pin, an aluminium tube for the knuckle, 2 stainless flats + 2 M4 shoulder screws, M3 inserts |
| Tolerances | tight (index, rail fit, S1-R) | loose (hinge alignment ±0.3; knuckle bore) |
| Supports | rails / carriages need orientation care | flat frames print support-free |
| Part count (solar) | ≈ 40 | ≈ 14 |
| Solar cost (EST) | €130–270 (custom laminates €50–80 UNKNOWN; metalwork €40–120; printing €30–60; wiring €10–15) | €120–180 (P108 €60–110 with shipping and VAT; printing €15–30; hinges €6–30; stay and screws €5–10; wiring €8–12) |

## 18. Serviceability

| | A | B1 |
|---|---|---|
| Panel replacement | Cassette out (hub, index, S1-R) | 4–6 screws or clips + 1 connector; no glue |
| Cable replacement | 2 long cables through the rails, loop and hinges | 1 cable: the leaf connector, knuckle and hinge pass (the display cable is nearby) |
| Hinge replacement | Hub parts: small, precise, many | Screw-mounted catalog friction hinges |
| Stay replacement | — | 1 shoulder screw per arm |
| Fastener access | Some fasteners are reached through the slots | All from the leaf back or the base underside |

## 19. Onshape findings

**What exists:** a new Feature Studio `NOMAD_D010_Concepts` in the NOMAD document, with the custom feature **"NOMAD D010 Concepts"**. It is isolated: it has no imports from production and nothing references it. The Onshape connector can only create and write Feature Studios; it cannot create a Part Studio, insert a feature, mates or configurations.

**What the owner needs to do:**

1. Create a new Part Studio in the NOMAD document, for example "D-010 Concepts".
2. Insert the custom feature "NOMAD D010 Concepts" from the `NOMAD_D010_Concepts` Feature Studio (add it through the toolbar's custom features).
3. Optional: create a Part Studio **configuration** that drives "State" (and "Layout"). This gives native named configurations: STOWED, DISPLAY_OPEN, PARTIAL, NORMAL, MAX, STAY/ONE_WING and CUSTOM.

**Dialog:**

| Setting | Options |
|---|---|
| Layout | **Gallery** (default: A row at y 0, B1 row at y −800, columns 1–6 every 800 mm); **side by side**; **A only**; **B1 only** |
| State | 6 named states, plus **CUSTOM** with sliders: display angle 0–135, A wing extension 0–1 and tilt ±80, B1 leaf 0–190 and stay yes/no |
| Toggles | cables, CG / support polygon, envelopes / keep-outs, base electronics |

**Contents:**
- **Shared base** for both: a simplified shell, keyboard/trackpad/Pi/battery/power/GNSS envelopes from the same evaluated Round C layout as "NOMAD E Base", the rear-plug keep-outs and feet.
- **A:** the lid with side slots, display and controller, and per side: rail, carriage, hub pin, index plate, S1-R yoke envelope, bracket, tray, laminate, loop-band reserve, plus the ±75° deployment envelope.
- **B1:** the lid core, foil, air gap, two frame halves plus splice, P108 panel, friction hinges, cable and idler knuckles, latch, connector, stay, plus the 0–190° leaf envelope.
- **Cables** are drawn as real Ø6 / Ø4 tubes with bend radii, colour-coded by type (the legend is in the feature info):

  | Colour | Section |
  |---|---|
  | Black | static |
  | Yellow | twist zones |
  | Orange | loop |
  | Magenta | hub S-bend |
  | Red | the unresolved carriage-to-loop crossing |

- **CG:** a red cube marker, a plumb line and a green support polygon (including the stay feet). The CG part name reads, for example, "B1 6 STAY_DEPLOYED | CG x −6.1 y 214.1 z 87.0 | rear margin 112.9 mm | calc rear tip wind 18 m/s".

**Kernel cross-check** (scratch document, the harness above; KERNEL vs CALC):
- CG: largest error 0.00004 mm, across 3 poses.
- A lid to plug keep-out at φ 120: **1.200 / 1.200**.
- B1 stack to plug keep-out at φ 125: **2.072 / 2.072**.
- B1 leaf to lid core at ψ 45: **1.141 / 1.141**.
- A deployed wing to lid: 8.0; bracket to lid: 8.0.
- Stay to base: 0.5.
- The gallery regenerates: 12 instances, 545 bodies, no errors.

**API calls:** 40 in this phase (usage 167 → 207 of 2,500, 8.3 %).

**Side effect:** the connector's notes tool created a separate Onshape document, "FeatureScript MCP Notes" (id 9ac1dd5e…), to hold coding notes. It is not part of NOMAD and can be deleted.

## 20. Risks

**B1:**
1. Tipping without the stay (a user who forgets it). Mitigation: stay, operating rule, leaf fold-back.
2. Display and battery heat when closed in the sun.
3. Exposed PV in transport.
4. Display-hinge torque about 1.5× A's.
5. Twist fatigue of the hollow knuckle.
6. The shared centre hinge pass.
7. P108 lead time or cost (single US vendor; an alternative panel is **UNKNOWN**).
8. Leaf-latch retention under vibration.
9. Leaf versus table at φ ≥ 120.

**A:**
1. Cable architecture unresolved.
2. Hub-bracket safety factor below 2.
3. S1-R not approved.
4. Precision and metalwork cost.
5. Custom-laminate availability.
6. Rear-plug conflict (−7 mm).
7. No front-sun capability.
8. Heat on the dark lid shell.

## 21. Remaining unknowns

- Real masses: battery, keyboard, trackpad, printed parts.
- Actual P108 performance and temperature rating. Alternative panels.
- Which friction hinges are available, their torque tolerance and how it drifts over life.
- The display-hinge hardware.
- The size of the display cable and the capacity of the centre pass.
- Knuckle twist fatigue.
- Real temperatures (closed and open) with foil and gap.
- LCD panel temperature ratings.
- Wind gustiness at use sites.
- Table friction.
- Whether users will deploy the stay.
- Glare off the leaf.
- Printed-frame warp in ASA/PETG at 144.5 × 235.
- Latch retention.

## 22. A / B1 comparison: decision matrix (factual, no scores)

| Category | A (sliding wings) | B1 (solar lid leaf) | Evidence |
|---|---|---|---|
| Solar area | 515 cm² laminate (2 × 135.5 × 190); max 590 | 609 cm² catalog panel; max 679 | CALC; VENDOR |
| Estimated output | 8.8 W nameplate (custom) / 5.2 W (catalog); 4.8–6.1 W real | 9.5–10.9 W nameplate; 5.6–7.1 W real | VENDOR + ASSUMED factors |
| Mass | 2.64 kg total; solar 528 g; lid 435 g | 2.62 kg total; solar 603 g incl. stay; lid 342 g | CALC from EST |
| CG movement | y +75 to +86 mm; x up to +12 (one wing) | y +70 to +98 mm; z up to +70 (upright) | CALC |
| Stability | tips at 8.3–10.6 m/s without a stay; 18.2 with | 5.4–8.3 without (2.4 upright at φ 125); **11.4–18.1 with the stay (required)** | CALC, not tested |
| Hinge complexity | hub pin + index lock + S1-R + bracket (hub bracket below safety factor 2 open); display hinge ~1.0 N·m each | 2 catalog friction hinges ~0.8 N·m + knuckles; display hinge ~1.6 N·m each | CALC / EST |
| Cable complexity | 2 cables (0.73 / 1.30 m); S-bend 2.5–3.9 × *d*; loop 3.3 × *d*; unresolved rail-wall crossing; right-hinge twist 7.1°/mm | 1 cable (0.85 m); 2 twist zones at 2.75°/mm; no loop | CALC, modelled |
| Thermal | PV hidden when closed; dark shell +55–57 K (use light / ASA); display +8–21 K | PV exposed; needs ≥ 6 mm vented gap + foil; display +6–22 K; frame at panel temperature (ASA) | EST |
| Printability | precision straight rails; tight tolerances | two frame halves fit a 256 bed; loose tolerances | EST |
| Hardware | EDM/laser/reamed small metal parts | catalog hinges, stainless flats, one pin, one tube | EST |
| Serviceability | cassette removal via the hub; long cables | panel = screws + connector; one short cable | modelled / EST |
| Portability | 79.6 mm thick, 5.63 L; PV protected | 73.0 mm, 5.16 L; PV exposed (sleeve) | CALC |
| Deployment | slide + tilt ±75°, per side; rear sun only | one leaf 0–190° + stay; sun from the rear, overhead or front; no visor | CALC |
| V1 cost (solar) | €130–270 | €120–180 | EST |
| Major unresolved risks | cable architecture; hub-bracket safety factor; custom laminates; −7 mm plug conflict | tipping discipline (stay); closed-in-sun heat; exposed PV; knuckle twist fatigue | — |

## 23. Engineering recommendation: RECOMMEND B1

**Why:**
- A's open items are inside its mechanism (hub, rail, cable path) and need redesign, not validation. Fixing A's cable needs a hollow hub axis or a long twist zone and a new rail-wall crossing, which adds precision complexity on top of D-009 and S1-R.
- B1's open items are all external, cheap and testable in a day: a stay, foil and gap, catalog hinges, a knuckle.
- B1 gives more realistic power from a buyable catalog panel, works with the sun in more directions, is thinner, and has one simple cable.
- It is **not** lighter, and it does **not** shade the screen (Phase 1 is corrected on both).

**B1 as recommended (differences from Phase 1 in bold):**
- **Catalog P108-class 18 V rigid panel.**
- **Open-back ASA frame in two halves.**
- **Vented gap of at least 6 mm, plus low-e foil.**
- Two catalog friction hinges of about 0.8–1 N·m.
- **Hollow cable knuckle with a twist zone of at least 60 mm.**
- Centre display-hinge pass shared with the display cable.
- **Mandatory rear outrigger stay (reach ≥ 90 mm).**
- **Display hinges of about 1.6 N·m each, with a φ-max stop.**
- Leaf-range rule at φ ≥ 120.

**What is not decided and still needs the owner:** whether to keep A as a paper fallback; the stay design details; whether a lift-off leaf (ground mode, possible visor) is worth its cost.

## 24. Next validation steps (before any production CAD)

1. **One-day mock-up** (cardboard or foam-board lid and leaf, a real 330 g ballast panel, the real base mass).
   - Measure the tip force and angle with and without the stay.
   - Check the leaf hold with the friction hinges in a fan gust.
   - Check the display-hinge holding torque at φ 110–135.
2. **Thermal:** the P108 (or a dark plate of equal mass) on a mock lid with 0 / 4 / 6 mm gaps and with and without foil, in sun. Log thermocouples on the panel, the lid back and the display position.
3. **Cable:** cycle a 2 × 0.5 mm² silicone cable at 190° twist over 60–70 mm for 2,000 cycles, and check continuity and jacket condition.
4. **Friction hinges:** buy two candidates and measure torque against angle and against temperature (60 °C).
5. **Printing:** print one ASA frame half; measure warp and the rebate fit to the P108.
6. **Transport:** carry it in a backpack for a week with a padded sleeve; check the latch retention and the PV surface.
7. **Display hinge pass:** measure the chosen display cable bundle and size the shared pass.

**Still needs physical validation even with B1 chosen:** panel mass and efficiency, hinge friction, PETG/ASA stiffness and creep, wind behaviour, real temperatures, cable fatigue, connector strain and printed tolerances. CAD does not settle any of these.

**Exactly what remains before production CAD:** owner review of this report and the Onshape concepts; an owner decision recording D-010; the step 1–2 mock-ups; hinge and panel sourcing. Only then a production lid re-architecture round, with new YAML parameters added as TBD. D-009 / S1 / S1-R stay preserved as the record of A.

## 25. Production freeze verification

| Check | Result |
|---|---|
| Production geometry | Unchanged: no write to `NOMAD_E_Prototype` (40d4…) or `NOMAD_P01_Coupons` (2e9a…); only the new `NOMAD_D010_Concepts` element was created and written |
| Production YAML | Unchanged: `nomad.yaml` last modified 2026-09-28 12:22, before D-010; `yaml_to_featurescript.py --check` passes for both targets |
| Production FeatureScript | Unchanged: `NOMAD_E_Prototype.fs` 12:36, `NOMAD_P01.fs` 12:20; `e_lid_layout.py --check` and `base_v01_layout.py --check` pass |
| D-009 / S1 / S1-R records | Preserved; not edited in this phase |
| Dependencies | No production part depends on the concept geometry. The concept Feature Studio imports nothing and duplicates only generated numbers from the same YAML / layout generators |
| Git | No commit, no push |

## Addendum (2026-09-29): NOMAD wordmark on the B1 lid back (visual concept only)

- **Scope:** a recessed "NOMAD" wordmark on the B1 lid back, in `NOMAD_D010_Concepts` only. The solar leaf, hinges, cable, stay, air gap, `nomad.yaml` and production CAD are unchanged. The one exception is the foil (see below).
- **Font:** Eurostile Extended is **not available** in Onshape; an unknown font name silently falls back to a normal-width face. This was checked by measurement.
  - The preview uses **Michroma** (in Onshape's font set; an extended geometric sans in the Eurostile Extended style) as a **fallback only, not the final identity font**.
- **Size (KERNEL):** 18 mm letter height; the letters span 139.1 × 19.5 mm including the round overshoot of the O. That is about 46 % of the 301 mm lid width.
- **Position:** centred on the lid centreline. The text centre is 200 mm from the lid's top edge, about 35 mm above the display hinge when the lid is open. It reads upright from behind the open lid.
- **Engraving:**
  - Recessed 1.0 mm into the 2.5 mm back skin, with a light-coloured 0.2 mm fill at the bottom of the letters so they read.
  - A 1.0 mm backing pad inside the lid keeps 2.5 mm of material under the letters (MIN_WALL is 2.0). The pad clears the display controller by 1.0 mm (KERNEL).
  - The letters produce 5 separate bodies, one per letter; the lid shell stays a single solid.
- **Foil:** the low-e foil gets a window 3 mm larger than the wordmark all round (about 5 % of the foil area). This is the only change touching the thermal design.
- **Visibility (CALC, line of sight past the leaf; percentages are looking straight at the lid back / from directly behind at table level):**

  | Leaf position | Visible |
  |---|---|
  | Stowed, lid closed or open | 0 % |
  | 30° | 0 % |
  | 65° (NORMAL) | 100 % / 100 % |
  | 110° | 100 % / 100 % |
  | 190° (MAX) and φ 125 with the leaf at 170° | 100 % |

  From the user's side the lid back is never in view.
- **Printability:** the letter counters stay attached to the recess floor, so there are no loose islands. Strokes are about 2.4 mm wide; no thickening was needed.
- **Dialog:** a new toggle, "Show NOMAD wordmark", default on. Part names: `D010_NOMAD_Wordmark`, `D010_NOMAD_Wordmark backing pad`.

**Erratum (2026-09-29, repair):** the first wordmark write did not compile.
- **Cause:** `box` is a FeatureScript reserved word, so the whole Feature Studio failed to load.
- **Latent defect:** the code also extruded every text region, which would have filled the O, A and D counters. The printability statement above was therefore not true of that code.
- **Fix:** both are fixed, with no change to font, size, position, depth, pad or foil window. The full gallery regenerates with the wordmark on (581 bodies) and off (545, same as before the wordmark).
- **Open item:** the kernel found the backing pad 0.19 mm from the B1 lid cable run (no intersection). This is left for your decision.
- **Details:** `d010_wordmark_rebuild_diagnosis.md`.
