# Round D.1 — Lid Architecture Convergence

> **SUPERSEDED / DEFERRED FOR NOMAD V1 (D-010, 2026-10-01).** This record belongs to **Architecture A** (sliding/tilting solar cassettes and their lid, D-004 / D-009). The owner selected **Architecture B1** (one solar leaf behind the display lid) as the active V1 architecture. The content below is kept unchanged as an engineering record and possible later reference; it does not describe the V1 design. See `docs/decisions.md` D-010 and `docs/v1-requirements.md`.

**Status:** analysis only. No lid class is chosen or ranked, no lid thickness is declared, and no rail reinforcement, hinge height, maximum angle or controller location is selected. D-007 stays proposed.

**Model:** `CAD/tools/lid_architecture_convergence.py`. It reuses:
- the Round D layer stack and formulas (`lid_stackup_study.py`) and B.2 (`lid_structure_screening.py`);
- the coupon A2 stiffener envelope (`coupon_expectations.py`, `P01_test_coupons.md`);
- the B.1 V1 + fixes solar geometry and its collision machinery (`solar_v1_feasibility.py`, kernel-validated in B.1);
- the C.2 hinge / rear-port geometry (`c2_screening.py`, kernel-validated in C.2).

```bash
py CAD/tools/lid_architecture_convergence.py
```

Every study value can be varied from the command line: `--T --skin --rib-h --rib-s --rail-h --cassette --reinf --h --lip --gap`.

**Evidence levels:**
- Layer arithmetic, clearances, hinge/port sweeps and solar collision checks: *modeled*.
- Stiffness, deflection, torsion, screw loads: *analytical screening estimates* (beam/plate formulas, **not FEA**, not certification).
- Masses, tolerances, bridging behaviour, part/insert counts, assembly time, pull-out strength: *working assumptions (inferred)*.
- **Nothing in this round is physically tested or measured.**

**No Onshape run** (API unchanged at ~100 / 2,500). The only new geometric conclusion is that the re-spaced rails the metal strips need stay collision-free. That was checked with the same B.1 prism machinery the kernel already matched exactly; a kernel run would re-verify the machinery, not the conclusion. Everything else is analytical.

---

## 1. Round D baseline

**Carried over unchanged:**
- Stack to the stowed-cassette top: lip + display 5 + gap 1 (+ mid-plate 2) + rail layer 13 + gap 1 + cassette 8 = **29** (lip 1) / **31** (lip 1 + mid-plate).
- Back structure spans the 202 mm cassette bay one-way. Criterion δ ≤ gap/2 for LC1 (20 N on b_eff 101) and LC2 (1 kPa). Cassette–back gap 2.
- Rail cantilever from the outboard pad, arm 149.5 mm to the stowed carriage. Stowed cassette 0.3 kg, 3 g jolt.
- D-006 rear-edge hinge (inset 0, height h), closed gap 2.0, MIN_GAP 1.0; Round C rear port zone Z 4–19 with 45 mm plugs.
- Controller band per side of the 15 mm centre pass: ~111.5 × 35.4 × 16.5 (lip 0). It is **17.5 tall with lip 1**.

**What D.1 changes in method (not in inputs):**
- **Finer grid.** Minimum back depths are solved on a 0.1 mm grid instead of 0.5. Round D's 37.9 (sandwich) and 39.9 (modular) become **37.6** and **39.6** at the criterion boundary, with LC1 0.98 against 1.0, i.e. no margin. Round D's values carried ~0.1 mm of margin.
- **Rail criterion now includes tolerance.** Static δ(1 g) ≤ gap/2 (0.5), and δ(3 g) + tolerance RSS ≤ gap (1.0, no display contact). Round D compared δ with the bare gap.
- **Masses normalized.** Structure is estimated geometrically (front frame by feature, rails, shell, plate). Fasteners (~44–49 g) and cables (30 g, placeholder) are added. Totals are therefore ~0.1 kg above Round D.
- **Lid CG** is computed from the layer masses and used for hinge torque, opening force and tip-back.

---

## 2. Class A: sandwich rear shell (~37–38 mm)

**Build-up** (lid face → back):

| Part | Content |
|---|---|
| Front frame | Face ring 2.5, 1 mm lip over the display border, perimeter walls, side walls with cassette slots, two 14 mm edge bands, rail pads beside the display, hinge corner blocks. 31 mm from the face to the shell seat. |
| Display | 235 × 150 × 5 (working), seated behind the lip |
| Rails ×2 | 13 mm C-channels, cantilevered from 28.5 mm pads at x 118.5–147 |
| Stowed cassettes | 8 mm, with 1 mm to the rails and 2 mm to the shell |
| Rear shell | Sandwich: outer skin 1.2, rib-web core 4.2 (webs 2.0 @ 30, along the span), inner skin 1.2 = **6.6** |
| **Total** | **T 37.6** (lip 1) / 36.6 (lip 0); closed NOMAD 79.6 |

**Back structure:** LC1 0.98 / LC2 0.62 against 1.0 allowed (at the boundary).

**Can it be printed? The bridged-skin question** (*analytical; bridging behaviour inferred*):
- **How it prints:** the monolithic shell prints outer skin down, webs up, then the inner skin across the webs. The inner skin **bridges 28 mm** (webs @ 30).
  - Bridge sag goes *into the cells*, away from the cassette gap, so the gap is not lost.
  - The inner surface facing the cassettes may be wavy by a few tenths of a mm (inferred). That sits inside the 0.30 shell-flatness allowance.
- **Strength is not the issue.** At LC1 the web-top interface shear is ~0.26 MPa and web shear ~0.35 MPa, against PETG interlayer strength of ~10+ MPa (inferred). The open question is **stiffness and flatness**: how much of the bridged skin actually carries load.

| Sandwich variant (lip 1) | LC1 at depth 6.6 | Depth needed | **T needed** |
|---|---|---|---|
| Nominal: skins 1.2, webs @ 30, bonded as printed | 0.98 | 6.6 | **37.6** |
| Bridged skin effective 0.8 (first 2 layers lost) | 1.29 | 7.4 | **38.4** |
| Bridged skin effective 0.6 | 1.56 | 7.9 | **38.9** |
| Webs @ 20 (18 mm bridges) | 0.96 | 6.5 | 37.5 (+11 g) |
| Slicer-infill core, G_core = 10 / 5 / 2 % of G_PETG (no bridging: top skin over infill) | 0.99 / 1.02 / 1.12 | 6.6 / 6.7 / 7.0 | 37.6 / 37.7 / 38.0 |
| Two-piece: ribbed shell + separate inner skin, **not bonded** | 7.27 | 12.0 | 43.0: **not viable unbonded** |
| Two-piece, bonded (adhesive) | as nominal | | 37.6, but bonding becomes a critical, permanent process |

**Skin × web-spacing trade** (lip 1; shell mass, solid):

| Skin | Webs @ 15 (13 mm bridge) | Webs @ 20 (18) | Webs @ 30 (28) |
|---|---|---|---|
| 1.0 | T 37.7 (243 g) | 37.8 (230 g) | 37.9 (216 g) |
| 1.2 | 37.5 (271 g) | 37.5 (258 g) | 37.6 (247 g) |
| 1.6 | 37.2 (328 g) | 37.2 (319 g) | 37.3 (311 g) |

**Other areas investigated:**
- **Front/display structure and retention:** the lip retains the display to the front. Rear clips press it back; rear clips can only go where no rail or loop sits above the display border (§8).
- **Solar rail region:** printed cantilever rails do **not** meet the 3 g no-contact criterion (§6). Class A needs rail stiffening (metal strips) or +1.4 mm of display gap.
- **Cassette clearance:** 2.0 behind the cassettes. The back-gap tolerance (cassette thickness 0.30, rail stack 0.15, shell seat 0.15, shell flatness 0.30) is RSS 0.47 / worst case 0.90. The 1.0 not used by the deflection allowance covers both.
- **Cable channels:** none in the shell. Loops and the corridor stay in the rail layer (B.1). The display cable and solar leads leave through the 15 mm hinge centre pass.
- **Hinge band:** frame corner blocks 28 (X) × 16.5 (Y) × 31 (Z). Hinge loads stay in the front frame, not the shell (§7).
- **Service access:** rear shell off (10 external screws), then the cassettes.
- **Mechanical result:** every stiffness number is at the boundary of the criterion. There is no margin unless the shell gets slightly deeper or has more webs.

**Answer (inferred):** class A is **realistically printable and assemblable if** the sandwich is printed monolithically with webs at ≤ 20 mm spacing, or with an infill core, and the effective inner skin is close to nominal. The practical T is then **37.5–37.7**; with a poor bridged skin it is **38.4–38.9**. That spread is only resolvable with a sandwich coupon, which does not exist yet.

---

## 3. Class B: modular rail module (~39–40 mm)

**Build-up:**
- **Front frame:** as A, but 33 mm to the shell seat, with **module lands** beside the display instead of rail pads.
- **Rail module:** 2.0 mid-plate, 296 × 230, 1 mm behind the display, with **both rails printed integral** (plate down, rails up; no support), plus controller and loop mounts. 296 × 230 × 15.
- **Rear service shell:** sandwich as A (6.6).
- **Total: T 39.6** (lip 1) / 38.6 (lip 0); closed NOMAD 81.6. Back LC1 0.98 / LC2 0.62, as A.

**Removable solar rail plate:** the module carries both rails, the loop anchors and optionally the controller. It comes out as one unit once the shell (10 screws) and cassettes are off, held by 8 screws into the frame lands.

**Rail-to-plate fastening (a geometry finding, modeled):**
- The carriage sweeps the whole rail interior (travel 158 + carriage 40 = 198).
- The corridor (8) and loops (1 mm) flank the rail, so there is no room for a continuous screw flange.
- Screws from the display side would put heads in the 1 mm display gap.
- Practical choices are an **integral module** (rails printed with the plate), or rails screwed only at their end blocks (ear at x 118.5–147 and a block past the inboard end stop).

**Are the joints too compliant, or the tolerance stack too large?** (*analytical + inferred tolerances*)

| Module / rail variant | 3 g deflection | + tolerance RSS 0.49 | vs 1.0 |
|---|---|---|---|
| Integral module, printed rails (composite) | 0.50 | **0.99–1.00** | **at the limit** |
| Rails screwed at their ends only (non-composite), printed | 0.88 | 1.37 | **fails** |
| Integral module + 2 steel strips per rail | 0.07 | 0.56 | meets |
| Integral module + 1 steel strip per rail | 0.11 | 0.60 | meets |

- **Compliance:** in the critical direction (toward the display) the module bears on the frame lands in compression, so screw slip is not in that load path (inferred). What matters is composite action between rail and plate, which is why an integral module works and a screwed one does not.
- **Tolerance:** the **mid-plate flatness** (296 × 230 × 2 printed, screwed at its edges, 0.4 inferred) is the largest term. It makes B's stack RSS 0.49 / worst 0.90, against 0.35 / 0.70 for frame-mounted rails. It is unmeasured.
- **Verdict (inferred):**
  - With printed-only rails the modular joint is acceptable only as an integral module, and only if the plate stays flat within ~0.4.
  - With strips the margin is ~0.44 mm.
  - A screwed printed rail on the plate is not acceptable.

**Other areas investigated:**
- **Screw/insert interfaces:**
  - 10 rear-shell joint + 8 module + 8 hinge + 12 small inserts = **38**.
  - The module lands give **~7 mm of material to the lid face**. That is tight for the ~5.7 mm M3 insert envelope (the insert bottom lands ~0.3 mm from the cosmetic face). A shorter M3 or M2.5 insert fits better (inferred).
  - The same 7 mm limit applies to the rail pads in A and C.
- **Cassette retention:** unchanged (carriage in rail). The stowed cassettes are held only at hub and carriage in every class (see §14).
- **Display frame:** as A. The display is installed before the module.
- **Cable access:** the best of the three for first build. Loops and controller can be routed on the module at the bench. Removing the module requires unplugging the display and both solar leads at the hinge side.
- **Hinge structure:** frame corner blocks 28 × 16.5 × 33. The extra 2 mm of frame height slightly lengthens a Z-direction screw couple (21 vs 19 mm).
- **Mass:** the mid-plate adds **~173 g**, making B the heaviest class (~0.2 kg more than A).

---

## 4. Class C: ribbed rear shell (~42 mm, conservative fallback, not preferred)

**Build-up:**
- Front frame as A (31 to the shell seat).
- Rear shell: 2.5 skin + **external** ribs 8.5 × 2.0 @ 30 along the span (plus B.2's cross ribs).
- **T 42.0** (lip 1) / 41.0 (lip 0); closed NOMAD 84.0. LC1 0.93 / LC2 0.59.

**Rib geometry and spacing** (LC1 mm, 2.5 skin; min T, shell mass):

| Spacing | h 6 | h 7 | h 8 | h 9 | h 10 | h 12 | Min T |
|---|---|---|---|---|---|---|---|
| 20 | 1.46 | 1.05 | 0.78 | 0.60 | 0.47 | 0.30 | **41.0** (292 g) |
| 25 | 1.73 | 1.25 | 0.93 | 0.71 | 0.55 | 0.36 | 41.5 (282 g) |
| 30 | 1.98 | 1.44 | 1.07 | 0.82 | 0.64 | 0.41 | **42.0** (275 g) |
| 40 | 2.46 | 1.80 | 1.35 | 1.03 | 0.81 | 0.52 | 43.0 (270 g) |

Opening the cassette–back gap to 3 gives 41.5 at spacing 30 (Round D).

**Other areas investigated:**
- **Printability:** the easiest of the three. The shell prints skin down, ribs up, with no bridging and no support. It is the only back structure with a direct coupon (B2 at h 6 / 8 / 11) (inferred from geometry).
- **Structural performance:** meets the back criterion.
  - **Torsion index is ~3.5× worse than A/B** (21 mm vs 6 mm corner deflection at 20 N), because the ribbed back is an open section and the side walls are slotted.
  - Rib tip stresses at LC1 are only a few MPa (inferred), so the ribs are not strength-critical.
- **Assembly:** identical to A.
- **Mass:** ~28 g heavier than A's shell; lid 1.64 kg.
- **Hinge structure:** as A.
- **Handling:**
  - The ribs are **exposed on the lid back**: snagging, impact damage to rib tips, dirt. A flush perimeter rim would protect the edges without adding thickness (inferred).
  - It is the thickest class, which costs hinge height (§7).

---

## 5. Normalized comparison

All three classes use lip 1, gap 2, placeholders as marked, and solid-PETG structure. Where two values appear as "x / y", they are printed-only rails / + 2 steel strips per rail.

| Metric | A sandwich | B modular | C ribbed | Evidence |
|---|---|---|---|---|
| Total lid thickness T | **37.6** (36.6 lip 0) | **39.6** (38.6) | **42.0** (41.0) | modeled |
| Closed NOMAD (40 + 2 + T) | 79.6 | 81.6 | 84.0 | modeled |
| Lid mass | 1.61 / 1.70 kg | 1.82 / 1.91 kg | 1.64 / 1.73 kg | inferred |
| – of which printed structure | 651 g | 850 g | 679 g | inferred |
| Back-panel LC1 / LC2 (allowed 1.0) | 0.98 / 0.62 | 0.98 / 0.62 | 0.93 / 0.59 | analytical |
| Rail, static (1 g), criterion ≤ 0.5 | 0.67 ✗ / 0.06 | 0.17 / 0.02 | 0.67 ✗ / 0.06 | analytical |
| Rail, 3 g + tolerance RSS, criterion ≤ 1.0 | 2.36 ✗ / 0.53 | 1.00 (limit) / 0.56 | 2.36 ✗ / 0.53 | analytical + inferred |
| Cassette static load | 2.94 N each (8.8 N at 3 g) → pad; far pad screw 56 N at 3 g | → module → lands | as A | analytical |
| Hinge friction needed (1.25 × worst gravity torque ≥ 30°) | 0.93 / 0.98 N·m per hinge | 1.06 / 1.11 | 0.95 / 1.00 | analytical + inferred |
| Hinge torque at 3 g, per hinge | 2.23 / 2.36 N·m | 2.53 / 2.66 | 2.29 / 2.41 | analytical |
| Hinge screw couple at 3 g, force per row (Z pattern / Y pattern) | 118–196 N | 121–221 N | 120–201 N | analytical |
| Torsion index (20 N corner) | 2.2° / 6 mm | 2.1° / 6 mm | 8.0° / **21 mm** | conservative index |
| Printed parts: large structural / solar (common) / small | 4 / 6 / ~11 | 3 / 6 / ~11 | 4 / 6 / ~11 | inferred plan |
| Largest printed part | front frame 301 × 235 × 31 | frame 301 × 235 × 33 | frame 301 × 235 × 31 | modeled |
| Minimum bed | ≥ 301 × 235 (~311 × 245 with skirt) | same | same | inferred |
| Heat-set inserts | 34 | 38 | 34 | inferred plan |
| First assembly (rough; excludes printing and the undesigned hub/lock) | ~110 min | ~107 min | ~110 min | inferred |
| Serviceability | shell (10) → cassettes → item | shell → cassettes → **module as one unit** → item | as A | inferred plan |
| Cable access | shell + cassettes off; rails stay in | same, or route on the module at the bench | as A | inferred plan |
| Display service access (rear retention) | shell, cassettes, both rails, loops, 4 clips | shell, cassettes, module (8), 4 clips | as A | inferred plan |
| Solar mechanism service access | rail + carriage out after shell + cassettes (2 pad screws per rail) | module out; integral rails mean reprinting the module | as A | inferred plan |

---

## 6. Solar rail reinforcement

**The two implementations:**
- **A. Printed rail alone:** the V1 + fixes C-channel, 27.6 × 13, walls 2.5.
- **B. Printed rail + replaceable metal strips**, using the coupon A2 envelope:
  - Side walls 4.1 with a 2.3 × 10.4 slot each.
  - Flat strips slid in edge-on, cut to 194 mm, retained at the rail end.
  - Two-strip variants (Al 10 × 2 or steel 10 × 1.5 in both walls) and single-strip variants (outboard, loop-side wall only).

**Load cases:** stowed 0.3 kg cassette at 149.5 mm on the pad cantilever (A, C) or on the mid-plate (B), 1 g and 3 g.

| Rail | Width | EI (N·mm²) | Mass per rail (printed + metal) | A/C: 1 g / 3 g | A/C 3 g + tol (≤ 1.0) | B plate: 3 g + tol |
|---|---|---|---|---|---|---|
| Printed only | 27.6 | 4.9e6 | 33.7 g | 0.67 / **2.00** | **2.36 fails** | 1.00 (limit) |
| + 2 × Al 10×2 | 30.8 | 28.9e6 | 32.1 + 21.0 g | 0.11 / 0.34 | 0.69 | 0.61 |
| + 2 × steel 10×1.5 | 30.8 | 56.0e6 | 32.1 + 45.7 g | 0.06 / 0.18 | 0.53 | 0.56 |
| + 1 × Al (outboard) | 29.2 | 17.2e6 | 32.9 + 10.5 g | 0.19 / 0.57 | 0.92 (thin margin) | 0.66 |
| + 1 × steel (outboard) | 29.2 | 30.8e6 | 32.9 + 22.8 g | 0.11 / 0.32 | 0.67 | 0.60 |

**How the reinforcement changes things:**
- **Rail deflection:** two strips cut the 3 g cantilever deflection 6–11×; one strip 3.5–6×.
  - Loose (unbonded) strips give nearly the same result as bonded ones (0.35 vs 0.34 Al; 0.18 vs 0.18 steel). The edge-on strip's own stiffness dominates, and its centroid sits at the rail's centroid. **Strips can stay removable without losing stiffness** (analytical).
  - The model agrees with the coupon A2 predictions (0.33 Al / 0.18 steel at 0.9 kg).
- **Lid thickness:** **no change**. The strips sit edge-on inside the 13 mm rail.
  - The printed-only alternative costs thickness. Opening the display gap to 2.36 costs **+1.4 mm**. Thicker floors and lips cost +3 to +5 mm and still end at 1.04–1.36 (fails). Printed-only A/C would become ~39.0 / ~43.4.
- **Rail mass:** +21–46 g per rail (two strips) or +10–23 g (one strip); +42–91 g per lid.
- **Width and layout (modeled):**
  - **Two strips:** rails widen 3.2 mm and move 1.6 mm apart to keep the 8 mm corridor. The **hubs move 1.6 mm outward in Y**, 131.8 → 133.4 and 103.2 → 101.6.
    - I re-ran the full B.1 collision sweep with this layout: **no collisions** at lid 0 / 105 / 135°, all slides, tilts ±75°. Both cable routes to the hinge still work. The controller band and front zone shrink 35.4 → 32.2.
    - Hub location is TBD under D-004, but this is a shift inside the solar module and is **flagged for owner awareness, not adopted**.
  - **One outboard strip:** carriage, pin, hub, bracket and corridor are untouched. Only the loop-side wall (+1.6) and its service loop move. The controller band becomes 33.8.
- **Manufacturability:**
  - Strip slots leave 0.9 mm printed skins (about 2 perimeters) beside each strip. That is printable but thin (inferred).
  - Strips are cut from standard flat bar and deburred.
  - Tolerance on the slot fit (2.3 for a 2.0 strip) is part of what coupon A2 tests.
- **Serviceability:**
  - A strip can only be swapped with the rail out. The slot opens at the outboard end, which faces the lid side wall 1 mm away. So it is a bench operation after shell + cassettes (A/C) or module removal (B).
  - An access hole in the side wall would weaken the lower side-wall strip. Not recommended (inferred).
- **Secondary effect:** the rail also deflects *away* from the display in a face-up jolt, carrying the cassette hub toward the back shell. Printed-only A/C rails (2.0 at 3 g) would also use up the 2.0 cassette–back gap. Strips resolve both directions (analytical).

**Not selected.** The mechanical consequence is plain:
- **A and C** need either strips (thickness-neutral, +42–91 g) or +1.4 mm of lid thickness.
- **B** works with printed rails only as an integral module and only at the tolerance limit.

---

## 7. Hinge / port feasibility

C.2 geometry: rear-edge axis, closed gap 2, port zone Z 4–19. Rear port clearance is the running minimum of lid-to-plug-zone clearance, 45 mm plugs, at h 0. *Modeled; cross-checked against `c2.feasibility` (T 31.5: 126.5° / 126.5°; T 42.5: 116.5° / 116.5°).*

| T | Class | Max opening, 45 mm plugs, at h 0 / 1 / 2 / 3 / 4 | Min h for 135°, plug 45 / 25 / ≤ 15 / no rear ports | Port clearance at 105 / 120 / 135°, h 0 |
|---|---|---|---|---|
| 36.6 | A, lip 0 | 121.0 / 120.0* / 126.5 / 130.0 / 133.5 | 4.5 / 4.5 / 0 / 0 | +11.0 / +1.7 / −6.3 |
| 37.6 | A | 120.0 / 120.0* / 125.5 / 128.5 / 132.0 | **5.0** / 5.0 / 0 / 0 | +10.8 / +1.2 / −7.0 |
| 38.6 | B, lip 0 | 119.5 / 120.0* / 124.5 / 127.5 / 130.5 | 5.5 / 5.5 / 0 / 0 | +10.5 / +0.7 / −7.7 |
| 39.6 | B | 118.5 / 120.0* / 123.5 / 126.5 / 129.5 | **6.0** / 5.5 / 0 / 0 | +10.2 / +0.2 / −8.4 |
| 41.0 | C, lip 0 | 117.5 / 120.0* / 122.0 / 125.0 / 127.5 | 6.5 / 5.5 / 0 / 0 | +9.9 / −0.5 / −9.4 |
| 42.0 | C | 117.0 / 119.0 / 121.5 / 124.0 / 126.5 | **7.0** / 5.5 / 0 / 0 | +9.6 / −1.0 / −10.1 |

\* **h ≈ 1 mm is a lid–base thin spot.** At h ≈ 1 the lid–base clearance touches 0.99 against MIN_GAP 1.0 near 120°, independent of T. This is a real feature of the D-006 geometry at the model's resolution (the A.2b grid sampled only h 0 and 2). Treat it as marginal, not as a hard limit.

**Findings:**
- **105° (nominal):** never port-limited. There is ≥ 9.6 mm clearance in every class.
- **At h 0:**
  - A reaches 120.0°, B 118.5°, C 117.0°. None reaches 135° with 45 mm rear plugs.
- **Short plugs:**
  - With plugs ≤ 15 mm (right-angle or recessed connectors) or no rear ports, **h 0 gives 135° in every class**.
  - 25 mm plugs barely help (5.0–5.5).
  - This is the C.1 result, now confirmed per class.
- **Hinge screw loads** at 3 g, force per screw row:
  - Y pattern (12 mm couple inside the 16.5 band): 186–221 N.
  - Z pattern (19–21 mm couple on the rear end face of the frame corner): 118–127 N.
  - Typical M3 heat-set pull-out in PETG is ~300–800 N (inferred, print-dependent), a margin of ~1.4–6.8× per single-screw row.
  - A Z-direction couple or two screws per row roughly halves the load.
- **Hinge-band thickness:** the corner blocks are 28 × 16.5 × 31 (A, C) or × 33 (B), the full frame height. The band's Y depth is fixed at 16.5 by the cassette slot starting at y 218.5, in every class.
- **Integration without weakening the rear shell:**
  - In all three classes the hinge loads go into the **front frame** corner blocks: hinge → corner block → side-wall end post / edge band → frame. The rear shell is not in the hinge load path, so hinge integration does not weaken it (modeled load path, inferred behaviour).
  - The shell still contributes to the torsion that one-corner loads put through the frame (A/B closed, C open).
- **Not locked:** h and θmax. The table is the trade.

---

## 8. Display + controller feasibility

**Display envelope:** 235 × 150 × 5 (working), centred at Y 42.5–192.5, behind a 1 mm lip in every class. Class B puts the 2 mm plate 1 mm behind it.

**Display retention: rear clip sites** (*modeled*). A rear clip needs rail-layer height above the display border. The rails and service loops cover most of the border, leaving:

| Border | Free stretch | Length |
|---|---|---|
| Short edge +X | Y 42.5–120.5 | **78** |
| Short edge −X | Y 114.5–192.5 | **78** |
| Long edge, free-edge side | X 92–117.5 | 26 |
| Long edge, hinge side | X −117.5 to −92 | 26 |

Same with the re-spaced rails. **Four clips fit on the short edges, one or two per corner window.** The long edges are otherwise under the loops. This applies equally to A, B and C.

**Alternative (not chosen):** a removable front bezel ring, screwed or snapped from the face, with a rear ledge in the frame.
- The display would then be serviced **from the front** without touching the solar layer, in every class.
- Cost: likely +0–1 mm (a ~2 mm bezel for screws), a face seam, and a second 301 × 235 ring-shaped print (inferred).

**Controller envelope** (working band per side of the 15 mm centre pass, beside the 28 mm hinge corners):

| Class | Band per side (X × Y × Z) | Cable exit (90° bend, R 15 + Ø6 = 21) | Service loop / U-turn (36) |
|---|---|---|---|
| A, C (printed rails) | 111.5 × 35.4 × 17.5 | fits | does not fit |
| A, C + 2 strips / 1 strip | 111.5 × 32.2 / 33.8 × 17.5 | fits | does not fit |
| B | Z 19.5 with a plate cut-out in the band, **13** if mounted on the plate; Y as for A | fits | does not fit |

**Connector clearance and exit:**
- The display's hinge-side edge is 4.6 mm from the band. An FPC exiting that long edge can pass under the right service loop in the display layer and rise into the band.
- An FPC on the **free-edge side has no route**: only the 1 mm display gap lies under the rail layer there.
- **Requirement on any future display SKU (not a selection):** a hinge-side FPC exit, or a short-edge exit near the hinge end.

**Front-frame printing interaction:**
- The hinge-end edge band (y 218.5–232.5, 14 mm overhang) needs support or a 45° gusset when the frame prints face down.
- A gusset would take the top-rear triangle of the controller band (Y 218.5–232.5, Z ~6–20), leaving ~21 mm of full-height band depth.
- Alternatives: removable supports (reachable through the open back), or moving the edge bands onto the rear shell as downstands, which print support-free. Not chosen.

**Lid or base** (conditions only; *no choice*):

| | Controller can live in the lid if… | Otherwise it goes in the base, and… |
|---|---|---|
| A | its section is ≤ ~32–35 (Y) × ≤ ~16.5 (Z, with 1 mm margin), and a 90° exit suffices | the panel's own cable crosses the hinge (flex-rated), with its loop in the base riser (Round C) |
| B | as A; ≤ 12 mm tall if it rides on the module plate; up to ~18.5 with a plate cut-out. Riding on the module improves service (it comes out with the module) | as A; the module then carries no electronics |
| C | as A | as A |

- **Service access:** in every class the band is reached with the shell off. The cassettes overlap Y 197–217.5 of the band, so a controller taller than the free rear 15 mm strip needs the cassettes out too.
- **Class B:** the controller can travel with the module.

---

## 9. Solar compatibility

The baseline is B.1 V1 + fixes. **The mechanism is not changed in any class.**

| Check | A | B | C |
|---|---|---|---|
| Stowed gaps | display–rail 1, rail–cassette 1, cassette–back 2 | display–plate 1, rail–cassette 1, cassette–back 2 | as A |
| Solar group shift from the display face | +1 (lip) | +3 (lip + plate) | +1 |
| Carriage travel | 158, unchanged | same | same |
| Hub, pin (Ø5), bracket (17), carriage (22.6 × 8) | unchanged | same | same |
| Cable corridor (8) and both routes to the hinge side | OK | OK | OK |
| Deployed ±75° at 105° / 120° / 135°: lowest Z, h 0 | 49 / 32 / 8 | 48 / 31 / 6 | 49 / 32 / 8 |
| … h 2 / 4 / 7 at 135° | 11 / 15 / 20 | 10 / 13 / 18 | 11 / 15 / 20 |
| Back structure vs deployed cassettes | never meet: deployed cassettes sit at \|X\| ≥ 158.5, outside the 150.5 half-width | same | same |
| Solar mechanism change required? | **no** | **no** | **no** |

- **Two-strip rail variant:** hubs shift 1.6 mm in Y. **Re-validated collision-free (modeled).** This is a layout shift, not a mechanism change, and it is flagged rather than adopted.
- **Single-strip variant:** leaves the mechanism geometry identical.
- **No class is marked as needing additional solar architecture work.** The stowed cassette's outboard-edge support is common to all classes (§14).

---

## 10. Manufacturing / self-assembly

*All inferred from the envelope-level plan. PETG, 0.4 nozzle, no printer selected.*

| Question | A sandwich | B modular | C ribbed |
|---|---|---|---|
| Parts printable flat? | yes: frame face down; shell outer skin down; rails floor down | yes: module plate down, rails up | yes |
| Supports required? | frame edge bands (14 mm overhang: supports or gussets, or bands moved onto the shell); shell none, but **28 mm bridges** unless webs ≤ 20 or an infill core | frame as A; module none; shell as A | frame as A; **shell none, no bridges** |
| Screws accessible with a normal hand tool? | yes: all M3, straight-line from outside (shell) or from the open back (pads, clips, controller, hinges) | yes; module screws from the back once the cassettes are out | yes |
| Inserts accessible for installation? | yes, all from open faces; pads leave ~7 mm to the lid face (tight for M3 × 5.7) | yes; lands ~7 mm (same caution) | yes |
| Display installed after printing? | yes, from the back before the rails (or from the front with a bezel ring) | yes, before the module | yes |
| Solar mechanism installed without trapped parts? | yes, with the carriage slid into the rail **on the bench first**. The side-wall notch (19) is narrower than the carriage (22.6), and the rail end sits 1 mm from the wall, so a carriage cannot enter an installed rail | same; carriages go into the module's rails on the bench | as A |
| Lid serviceable later? | yes: shell (10 external screws) | yes | yes |
| Broken rail replaceable? | yes: shell + cassettes + 2 screws per rail | only as the whole module if the rails are integral (reprint ~0.24 kg); 2–4 screws if screwed, but the screwed rail fails §3 | yes, as A |
| Broken cassette replaceable? | needs a **detachable hub joint + lead connector** (not designed; D-004 hub TBD). Otherwise it can't leave: the carriage can't pass the side wall | same | same |
| Cables routed without dismantling the whole lid? | shell + cassettes off; display and rails stay | same, or route on the module at the bench | same |
| Special tools? | heat-set insert tip for a soldering iron (common maker tool); nothing else identified | same | same |

- **Normal-hand-tool principle:** no fastener in any class needs more than a standard driver at envelope level.
- **Two items need justification in detail design:** the hinge screws (hardware TBD) and the pad/land insert depth.
- **Bed:** every class has a 301 × 235 part, needing a ≥ ~311 × 245 bed or a split.
  - Splitting the rear shell at X = 0 keeps its one-way bending path intact (the split runs along the span) but cuts its torsion cell.
  - Splitting the frame cuts the edge bands and the hinge span and needs splice plates.
  - Split screening only (C.2 method); not developed.

---

## 11. Mass / handling

**Mass breakdown** (g; solid-PETG structure is an upper bound: thick members printed with infill would be lighter, maybe ~10–15 % overall, inferred):

| | A | B | C |
|---|---|---|---|
| Front frame (face ring 104, lip 7, walls 90–97, edge bands 116, pads/lands 7–25, hinge corners 12–13) | 336 | 363 | 336 |
| Rails ×2 (printed) | 67 | 67 | 67 |
| Rear shell | 247 | 247 | 275 |
| Mid-plate | — | 173 | — |
| **Printed structure** | **651** | **850** | **679** |
| Metal strips (none / 2 × Al / 2 × steel, both rails) | 0 / 42 / 91 | same | same |
| Screws + inserts (inferred) | 44 | 49 | 44 |
| **Cassettes ×2 (placeholder, 0.3 kg each; no panel selected)** | 600 | 600 | 600 |
| **Display (placeholder)** | 200 | 200 | 200 |
| **Hinge hardware ×2 (placeholder)** | 50 | 50 | 50 |
| **Controller + cables (placeholders)** | 70 | 70 | 70 |
| **Complete lid** (printed rails / + 2 steel) | **1.61 / 1.70 kg** | **1.82 / 1.91 kg** | **1.64 / 1.73 kg** |
| Lid CG from the free edge / from the face | 124 / 20 mm | 124 / 20 mm | 124 / 21 mm |

**Handling** (analytical from the placeholder masses; the hold margin, base masses and CG are inferred):

| | A | B | C |
|---|---|---|---|
| Worst gravity torque from 30° up | 1.49 N·m | 1.69 N·m | 1.52 N·m |
| Friction needed (× 1.25), total / per hinge | 1.86 / 0.93 | 2.11 / 1.06 | 1.90 / 0.95 |
| Free-edge force to open / close | ~15 / ~1 N | ~17 / ~1 N | ~15 / ~1 N |
| Base mass to open **one-handed** without the base lifting (base CG at 0.40 / 0.50 D from the front) | 1.35 / 1.62 kg | 1.53 / 1.83 kg | 1.38 / 1.65 kg |
| Base mass against **tip-back** at 105 / 135° (CG 0.40 D) | 0.57 / 1.08 kg | 0.65 / 1.22 kg | 0.59 / 1.10 kg |

**Is the lid impractical to open by hand?** (inferred)
- **Two-handed** (one hand holding the base): no. A free-edge force of ~15–17 N is heavy for one finger but normal for a hand.
- **One-handed:** depends on the base mass, which is not modeled. The requirement (1.35–1.83 kg) sits inside or above the placeholder range (1.2–1.8 kg), so one-handed opening is **marginal in every class and worst in B**.
- **Tip-back at 135°** needs a base of ~1.1–1.5 kg.
- **Options, not chosen:** variable-torque (cam) hinges with low torque near closed; a counterbalance spring; forward battery placement (Round C already notes it helps).
- **The largest single contributor is the two cassettes (0.6 kg, placeholder).** A lighter panel choice would move every handling number more than any lid-class choice.

---

## 12. Main failure modes

*Inferred, from the numbers above.*

| Class | Failure mode | Consequence | Driver / mitigation direction |
|---|---|---|---|
| **All** | Printed cantilever rail deflects 2.0 mm at 3 g | rail touches the display back (1 mm gap), and in a face-up jolt the cassette hub reaches the back shell | strips, +1.4 mm gap, or the B module |
| **All** | Hinge insert pull-out | lid drops or loosens | 118–221 N per row at 3 g against a ~300–800 N inferred pull-out; Z couple or 2 screws per row |
| **All** | Base lifts on one-handed opening; tip-back at 135° | handling, falls | base mass/CG, hinge torque profile |
| **All** | Stowed cassette supported only at hub/carriage | cassette outboard edge rattles or hits the rail layer at 3 g | define lands at the side-wall slot edges (1 mm clearance) |
| **All** | Display FPC on the wrong edge | no route to the controller | SKU requirement (§8) |
| **All** | Edge-band overhang printing | support scars or a gusset that eats the controller band | supports, gussets, or bands on the shell |
| **A** | Bridged inner skin sags or under-bonds | back stiffness falls; T needs +0.8–1.3 | webs ≤ 20, infill core, sandwich coupon |
| **A** | Thin 6.6 mm shell warps | cassette gap lost | shell flatness is in the 0.30 allowance; needs measuring |
| **A** | Core crushed at screw bosses | loose shell | solid columns through the core |
| **B** | Mid-plate bows toward the display | display contact (tolerance RSS 0.49, largest term) | flatness test; strips give margin |
| **B** | Screwed (non-integral) rail on the plate | 1.37 vs 1.0: display contact at 3 g | integral module |
| **B** | Heaviest lid (+~0.2 kg) | handling numbers worst | — |
| **B** | Module removal needs display and solar leads unplugged | service complexity | connectors at the hinge side |
| **C** | Open-section torsion (~3.5× A/B) | corner lift when carried by one corner; display stress | frame stiffness; not developed |
| **C** | Exposed ribs | snag, impact, dirt | perimeter rim |
| **C** | Thickest lid | h 7 for 135° or ≤ 117° at h 0 | short plugs or higher axis |

---

## 13. Convergence window

These are thresholds, not preferences. Values are with lip 1; lip 0 in parentheses (−1 mm).

| Constraint | Threshold (enclosed lid) | Basis |
|---|---|---|
| **Solar mechanism minimum** | 29 (28) to the cassette top + ≥ 1 back gap + any back → **≥ 30 (29) before structure** | modeled stack (B.1); unchanged in every class |
| **Structural minimum** (PETG, δ ≤ gap/2) | **~37.2 (36.2)** with 1.6 skins; 37.6 (36.6) with 1.2 skins; 37.0 with a solid 6 mm plate at 539 g | analytical |
| **Manufacturing minimum** (as-printed sandwich) | **37.5–37.7** with webs ≤ 20 or an infill core (G ≥ 5 %); **38.4–38.9** if a 28 mm bridged skin loses 2–3 layers; ribbed with no bridging **41.0–42.0** | analytical + inferred; *untested* |
| **Rail minimum** | +0 with strips; **+1.4** for printed-only cantilever rails (A/C); B at the limit | analytical + inferred tolerance |
| **Hinge/port** (an *upper-side* constraint) | 135° at h ≤ 4 with 45 mm rear plugs needs **T ≤ ~35**, below every enclosed class. Enclosed classes need h 5–7, or θmax 117–120° at h 0, or plugs ≤ 15 mm / no rear ports (then h 0 works at every T) | modeled |

**Window:**
- **Below ~37 mm (lip 1; ~36 lip 0):** structural and manufacturing constraints become problematic. No enclosed PETG back was found that meets the handling criterion over the 202 mm bay. The only candidate near 37.0 is a solid 6 mm plate (+~290 g vs the sandwich, and a sparse-infill print of it becomes an untested sandwich).
- **Between ~37.5 and ~42 mm:** multiple architectures remain credible:
  - A from 37.5–38.9, depending on the as-printed sandwich;
  - B from 39.6 to ~40.9 with the same shell uncertainty;
  - C from 41.0 (ribs @ 20) to 42.0 (ribs @ 30).
  Printed-only rails push A/C up by 1.4 mm; strips do not change T.
- **Above ~42 mm:** thickness mainly adds margin. All three classes meet the back criterion by 42.0; beyond that, no demonstrated constraint is being solved. Each extra mm costs ~+0.5 mm of hinge height for 135° (45 mm plugs), ~−0.7° of opening at h 0, +1 mm closed height, and mass.

**Outside the three classes (reference only, not analyzed):**
- The ~37 mm structural floor is a **PETG-material** floor.
- An equal-stiffness plain aluminium back sheet would be ~1.84 mm (T ~32.8, ~352 g).
- This needs owner direction before any further look; it is not a proposed class.

**Class status:**
- **Mechanically credible (conditional):** all three.
  - **A** on the as-printed sandwich plus rail stiffening.
  - **B** on the integral module plus mid-plate flatness (or strips).
  - **C** on rail stiffening; the most predictable manufacturing, the thickest and least torsionally stiff.
- **Unresolved risks:**
  - A: bridged-skin performance (±1.3 mm of T).
  - B: plate flatness, the 7 mm land insert depth, and the heaviest lid.
  - C: torsion, exposed ribs, and the hinge-height demand.
  - All: rail stiffening path, hinge insert loads, handling (base mass), cassette hub detachability.
- **Eliminated by hard constraints:** **none of the three classes.** These sub-variants fail their criteria and are eliminated as specified:
  - printed-only cantilever rails at the current 1 mm display gap (A/C): 2.36 vs 1.0;
  - B with printed rails screwed to the plate: 1.37 vs 1.0;
  - a two-piece sandwich with an **unbonded** inner skin: 7.3 vs 1.0.
- **Evidence required for the final decision:** listed in §15.

---

## 14. Remaining unknowns

1. **As-printed sandwich behaviour:** effective bridged-skin thickness, flatness, core shear of an infill core. Decides A's T within 37.5–38.9, and B's shell.
2. **Rail stiffness in reality:** coupon A1/A2 (printed E, pad compliance, strip fit).
3. **Mid-plate flatness** (B only): 296 × 230 × 2 printed plate, before and after screwing.
4. **Display SKU:** true thickness including board/FPC, FPC exit edge, mounting features, tolerance.
5. **Controller:** size, height with connectors, cable type and bend radius.
6. **Cassette panel:** real thickness and mass (8 mm / 0.3 kg placeholders dominate the handling numbers).
7. **Hub detachability and lead connector:** needed to replace a cassette at all (D-004 hub TBD).
8. **Stowed cassette outboard-edge support:** lands at the side-wall slot edges, all classes.
9. **Hinge hardware:** achievable axis height (h 5–7?), torque profile, screw pattern (Y vs Z couple), insert pull-out.
10. **Rear-port plug length policy:** ≤ 15 mm plugs remove the h requirement entirely. This is an owner decision, not a measurement.
11. **Base mass and CG:** decide one-handed opening and tip-back.
12. **Printer/bed or print service** (≥ ~311 × 245), or a split strategy.
13. **Solar YAML reconciliation** (Round D flag, still open): YAML carriage 12 / deploy 5 vs V1 + fixes 22.6 / 8, plus a hub offset formula that doesn't match V1.

---

## 15. Recommended physical measurements / tests before persistent CAD

Ordered by how much uncertainty each removes. None have been run; the new coupons listed are **suggested, not created**.

1. **Coupon A (existing, not printed):** A1 printed vs A2 empty / Al / steel. Decides printed rails vs strips and calibrates the rail model. *Suggested addition:* test A2 with one strip in the outboard wall only.
2. **Sandwich coupon (new, suggested):** 202 span × 90, skins 1.2, core 4.2–4.5, three versions:
   - webs @ 30 (28 mm bridge);
   - webs @ 20;
   - infill core.
   Measure LC1 at 20 N against the model (0.98 nominal). Section-cut to measure the effective bridged skin; check inner-face flatness. This is the only test that can place A inside 37.5–38.9.
3. **Coupon B (existing):** B2 at h 6 / 8 / 11 calibrates the ribbed rows (C) and the B.2 plate model shared by all classes.
4. **Mid-plate flatness print (B only):** a representative 2 mm plate (full 296 × 230 if a bed allows). Measure bow before and after screwing at the lands against the 0.4 allowance.
5. **Heat-set insert pull-out in PETG** (M3 × 5.7 and a short M3/M2.5 variant in 7 mm of material): calibrates the 118–221 N hinge-row loads and the pad/land depth.
6. **Display datasheet or sample:** thickness incl. FPC, FPC exit edge, border widths.
7. **Controller + display cable sample:** band fit (≤ 32–35 × 16.5), bend radius.
8. **Cassette panel selection** (owner): real thickness and mass.
9. **Hinge hardware samples:** axis height relative to the rear face, torque profile, holding ~1 N·m per hinge, screw pattern.
10. **Owner decisions that act like measurements:**
    - rear-port plug length (≤ 15 mm vs 45 mm);
    - enclosed lid confirmed (Round D);
    - printer or print service bed size.

**Earliest point at which a persistent Lid V0.1 Feature Studio would not be built on a guessed thickness:** after items 1, 2 and 8. Items 3–7 refine it. *(Inferred.)*

---

## Housekeeping (this round)

- **Created:** `CAD/tools/lid_architecture_convergence.py`, this report.
- **Modified:** `docs/build-log.md` (D.1 entry), `CLAUDE.md` (status line).
- **Parameters:** none added or changed in `nomad.yaml`. All D.1 study values (lip, gap, skins, webs, rib spacing, reinforcement geometry, tolerances, handling margins) are local to the script and labelled working/inferred. Existing YAML names are reused where they exist.
- **Onshape:** no calls (~100 / 2,500).
- **Git:** no commit, no push.
