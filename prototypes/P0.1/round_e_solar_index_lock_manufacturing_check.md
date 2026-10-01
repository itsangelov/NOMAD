# Round E — Solar Index Lock: Pin Size and Plate Manufacturing Check

> **SUPERSEDED / DEFERRED FOR NOMAD V1 (D-010, 2026-10-01).** This record belongs to **Architecture A** (sliding/tilting solar cassettes and their lid, D-004 / D-009). The owner selected **Architecture B1** (one solar leaf behind the display lid) as the active V1 architecture. The content below is kept unchanged as an engineering record and possible later reference; it does not describe the V1 design. See `docs/decisions.md` D-010 and `docs/v1-requirements.md`.

**Status:** analysis only. No change to `nomad.yaml`, the spec, FeatureScript, Onshape, CAD or Git. Awaiting owner approval.

**Starting point:** `round_e_solar_index_lock_investigation.md` (concept C1). F3 Option B hub geometry is unchanged and accepted.

**Evidence levels:**
- Packaging geometry: *modeled* (2-D window around the tilt axis from the current `e_lid_layout.py` values; not kernel-checked).
- Loads and stresses: *inferred* (hand calculations, stated models, no FEA, nothing tested).
- Manufacturing capability: *published generic guidance* and *published vendor-specific data*, labelled separately (§8). No quote or DFM review has been obtained.
- Scratch script: `indexmfg.py` in the session scratchpad, not in the repository. Every formula it uses is written out below so the numbers can be reproduced.

**Answer: D — keep the Ø1.5 mm pin, with a minor plate-geometry change** (§7).
- The 15° pitch at r 10 leaves only about 2.6 mm between hole centres. That space fits a Ø1.5 pin (1.0 mm webs) but not a Ø2 pin (0.5 mm webs).
- The plate can be made, but **not with laser-cut holes**. Cut the outline by laser, waterjet or milling. Drill and ream the 11 holes on a CNC or dividing-head mill, or make everything by wire EDM.
- Replace the roll-pin key with a **double-D key plus an M2 clamp screw**. This removes the tiny cross-hole, and it also retains the plate axially, which the roll-pin arrangement did not.
- This check also corrects three numbers in the investigation (§6). One of them becomes the **single biggest remaining risk**: the Ø5 pin's anti-rotation flat in the printed carriage (§9).

---

## 1. Basis and geometry assumptions

### Loads (from the closed load check)

| Case | Torque | Force at r 10 |
|---|---|---|
| Handling | T_h = 0.63 N·m | F = T/r = **63 N** |
| Design (SF 2) | T_d = 1.26 N·m | **126 N** |

- Acceptance: no yield at T_d, which is equivalent to SF ≥ 2 on handling.
- PETG bearing allowable: 30 MPa. Assume 15 MPa hot (60–70 °C), per the load check's temperature note.

### Metal allowables (handbook minimum yield; not re-researched here)

| Material | Yield (MPa) |
|---|---|
| 304 annealed (ASTM A240) | ≥ 205 |
| 301 ¼-hard (ASTM A666) | ≥ 515 |
| 301 ½-hard | ≥ 758 |
| 17-4PH H1150 | ≈ 725 |
| 303 cold-drawn bar | ≈ 415 |
| Hardened dowel (ISO 8734, ≈ 550–650 HV) | ≥ 1,000 (conservative) |

### Packaging window

Coordinates are relative to the tilt axis in the lid frame (right side; dy along +Y, dz along +Z).

**Plate region (fixed; it does not rotate):**
- Disc R_OUT;
- dz ≥ −5 (plate bottom at the bracket bottom, 1.0 mm above the rail floor);
- excluding the region dy < −5 with dz < 5.5 (outside the 17 mm rail-slot band, below the tray).

**R_OUT = 11.75.** This is a small correction to the investigation's "R ≤ 12". The plate is fixed but the tray groove rotates ±80° with the cassette, so every part of the plate must stay inside a groove disc of R 12.0 at all tilts:
- a groove of R 12.0 keeps the 1.5 mm tray skin (dz ≤ 12);
- 0.25 mm radial running clearance then gives R_OUT 11.75;
- accepting a 1.25 mm skin (groove R 12.25) would allow R_OUT 12.0 and gain about 0.1 mm of edge ligament.

**Holes:** 11 holes at 15° pitch on radius r. The index pin sits at a fixed cassette-frame angle of 57.5°, so the hole centres lie at lid-frame −17.5° … +132.5°.

### Formulas

| Quantity | Formula |
|---|---|
| Web (hole-to-hole ligament) | w = 2r·sin 7.5° − h (h = hole Ø) |
| Edge ligament | Minimum distance from the hole edge to the plate boundary |
| Pin double shear | τ = F / (2·πd²/4) |
| Pin bending (simply supported across the clevis) | Span L = 0.5 + t + 0.5 + 2 × 1.0 (effective support 1.0 mm into each PETG cheek). M = F·(L/4 − t/8); σ = M / (πd³/32) |
| Plate bearing | F / (d·t) |
| Web: bending, as a beam spanning the hole diameter radially, fixed at both ends, loaded by the pin | σ = (F·h/8) / (t·w²/6) |
| Web: shear | τ = F / (2·w·t) |
| PETG bearing | (F/2) / (d × engaged length). Inboard counter-hole: 2 mm (investigation) or 3 mm. Outboard guide: 6 mm |
| Pin stroke | Counter-hole depth + 0.5 + t + 0.5 + 0.5 lead-in |
| Double-D key | Two flats of depth f on Ø5; flat width w_f = 2√(2.5² − (2.5 − f)²); linear pressure on half of each flat. p = 6T / (t·w_f²) |

## 2. Question 1 — Ø1.5 vs Ø2.0 index pin

Both cases use r = 10, t = 1.5 stainless and hole = pin + 0.1.

| Check | **Ø1.5 (hole 1.6)** | Ø2.0 (hole 2.1) |
|---|---|---|
| Web between holes | **1.01 mm (0.67 t)** | **0.51 mm (0.34 t)** |
| Minimum edge ligament (R_OUT 11.75) | 0.95 | 0.70 |
| Angular slack of the 11-hole pattern while keeping edge ≥ 0.75 | **±2.6°** | **none** (already < 0.75) |
| Best achievable r (web = outer ligament) | r 9.95 → 1.00 / 1.00 | r 10.15 → **0.55 / 0.55** |
| Larger r possible? | No. Above ≈ 10.45 the rail-slot band edge (dy +12) and the tray skin split the arc (investigation §2) | No. Limit ≈ 10.2 |
| Pin double shear, T_h / T_d | 18 / 36 MPa | 10 / 20 MPa |
| Pin bending, T_h / T_d | 178 / **357** MPa (needs a **hardened** dowel) | 75 / 150 MPa |
| Plate bearing, T_h / T_d | 28 / 56 MPa | 21 / 42 MPa |
| Plate web bending, T_h / T_d | 49 / **99** MPa | 254 / **508** MPa |
| Plate web shear, T_h / T_d | 21 / 42 MPa | 41 / 82 MPa |
| PETG inboard counter-hole bearing, 2 mm deep, T_h / T_d | 10.5 / **21.0** MPa | 7.9 / 15.8 MPa |
| Same, 3 mm deep | 7.0 / 14.0 MPa | 5.2 / 10.5 MPa |
| PETG outboard guide (6 mm), T_h / T_d | 3.5 / 7.0 MPa | 2.6 / 5.2 MPa |
| Pin stroke | 5.0 (6.0 with a 3 mm counter-hole) | Same (plate and groove unchanged) |
| Spring | Unchanged (≈ 1 N preload) | Unchanged |
| Counter-hole wall to the tray bottom | 2.18 mm | 1.93 mm |
| Standard dowel | ISO 8734 Ø1.5 × 16 (confirm stock length) | ISO 8734 Ø2 × 16 |
| Plate manufacturability | Hole ≈ 1 t; web 0.67 t: at or below generic laser rules (§3); fine for drilling | Hole 1.4 t (easier by itself), but the **0.34 t web is unmanufacturable** by laser or waterjet and fragile even when drilled |

**Verdict: keep Ø1.5.**
- Ø2 would have real advantages: pin bending 2.4× lower, about 25 % less PETG bearing, and a stiffer pin.
- But at 15° on the only feasible radius it leaves a **0.5 mm web**. That web yields at T_d in 304 (508 MPa against 205) and has only SF 1.5 even in 301 ½-hard. It also leaves **no packaging slack**.
- There is no room to grow the radius.
- Ø1.5 in a hardened dowel carries the design load in bending with SF > 2.5, so the stronger pin buys nothing needed.
- The one Ø1.5 caveat: **the dowel must be hardened.** A stainless dowel (σy ≈ 415) would have SF 1.16 at T_d.

## 3. Question 2 — can the plate be manufactured?

### Plate as specified

| Item | Value |
|---|---|
| Material / thickness | Stainless, 1.5 mm |
| Holes | 11 × Ø1.6, r 10 |
| Web | 1.01 |
| Edge | ≥ 0.95 |
| Outline | R 11.75 with a floor flat and a band cut-out |
| Keyed centre | Double-D (§4) |
| Overall size | ≈ 23 × 17 mm |

**Required accuracy (the 0° stow hole matters most):**
- A tangential hole-position error δ tilts the cassette by δ/r.
- **0.05 mm → 0.29° → 0.57 mm at the far corner**; 0.1 mm → 1.14 mm.
- Hole diametral clearance 0.1 → ±0.29° free play.
- Laser-class tolerances of ±0.1–0.2 mm are therefore too coarse for the holes, though fine for the outline.

### Manufacturing options

| Method | Ø1.6 holes in 1.5 mm | 1.0 mm web | Position / size tolerance | Edge / heat | Local availability | Verdict |
|---|---|---|---|---|---|---|
| **A. Fiber laser** | Generic rule is hole ≥ 1 × t [G1]; Ø1.6 = 1.07 t is at the limit. One vendor lists much smaller minimums (0.8 mm for 1.25–1.5 mm stainless) [V2] | Generic: features ≥ 1 × t apart because of heat build-up [G1]; one vendor states webs ≥ material thickness [V1]. **0.67 t fails both** | Generic ±0.1 mm [G1]; vendor ±0.005" (0.13 mm) [V1]; vendor ISO 9013 ±0.2 mm for this size range [V2] | HAZ 0.1–0.2 mm per side [G1] takes 20–40 % of a 1.0 mm web. 11 closely spaced pierces concentrate heat, with a risk of local rounding or distortion and a pierce mark in each hole | Very common | **Outline: yes. Holes: no** (web rule, heat, tolerance) |
| **B. Abrasive waterjet** | Kerf 0.76–1.14 mm; features ≥ 1.5 × kerf ≈ 1.1–1.7 mm [G2]; one vendor's minimum hole is ≥ 0.070" = 1.78 mm [V1] | Below the ≥ 1.5 × kerf rule | Generic ±0.05 to ±0.25 mm depending on machine [G2, G3]; taper | No heat. Frosted edge; pierce damage at small holes | Common | **Outline: yes. Holes: no** |
| **C. CNC milling / drilling** (or a manual mill with a rotary table or dividing head) | Spot drill, drill Ø1.5, ream Ø1.6. Ø1.6 reamers are standard tooling | 1.0 mm between drilled holes is routine (drilled from solid, no heat) | *Generic inferred:* ±0.01–0.02 mm on the reamed Ø; ±0.02–0.03 mm position in one setup | Clean, square, no HAZ. Small burr; deburr both faces | Any general machine shop. 15° indexing is classic rotary-table work | **Recommended for the holes** (and optionally the whole plate) |
| **D. Wire EDM** | Needs an EDM-drilled start hole per hole (11) | Fine | *Generic inferred:* ±0.005–0.01 mm | Recast layer only a few µm; no distortion. Can cut a stack of plates at once | Tool-and-die / EDM shops; less common than C but widely available in industrial areas | **Best quality**, highest cost per job. Good for the double-D |
| E. Photochemical etching | Generic rule: hole ≥ 110 % of t → 1.65 for 1.5 mm, at the limit [G4] | — | ±10 % of t → **±0.15 mm** [G4]. Maximum thickness is generally ≈ 2 mm [G5], and few shops etch 1.5 mm | Hour-glass hole wall (poor pin bearing) | Specialist | **Not suitable** |
| F. **Hybrid** (practical choice) | Laser or waterjet the outline and the double-D, leaving the 11 holes out (or undersized pilots only, if the machinist wants them). Then drill and ream all 11 holes plus the double-D (if the fit needs it) in one CNC setup, datumed on the double-D | ✓ | As C | As C | A laser shop plus any machine shop | **Recommended** |

### Answers to the specific questions

- **Is Ø1.6 practical?** Yes if drilled and reamed, or cut by EDM. Borderline by laser; no by waterjet or etching.
- **Minimum web:** 1.0 mm is acceptable for drilling and EDM, and below the generic laser and waterjet rules.
- **Heat distortion:** a concern only for laser-cut holes. Laser-cutting only the outline is harmless (it is far from the holes).
- **Is 1.5 mm stainless sensible?** Yes, for the drilled route (web 99 MPa at T_d). A thinner plate only makes sense to satisfy laser rules (§4), and laser tolerance would still be inadequate.
- **Are 2 mm holes easier?** As isolated holes, yes. On this pitch, no: the web halves (§2).
- **Obtainable locally?** A laser-cut outline and a machine-shop drilling job are both ordinary local jobs. This is generic process capability; no specific local vendor has been confirmed.
- **Instant-quote online laser services** would likely flag the 1.0 mm web on 1.5 mm material, per their published web rule [V1].

## 4. Question 3 — small geometry optimisation

| Lever | Result | Adopt? |
|---|---|---|
| Increase index radius | The window stops about 10.45 (band dy +12, tray skin). Within that, the web gains 0.26 mm/mm of r while the outer ligament loses 1 mm/mm. The balance point is **r 9.95–10.15 → about 1.0–1.05 / 1.0–1.05**, so r 10 is already optimal | **No, keep r 10** |
| Plate thickness 1.0–1.2 | Meets laser ratios: 1.0 gives hole 1.6 t and web 1.0 t. Web stress rises to 123 / 148 MPa at T_d (fine in 301). But laser tolerance (±0.1–0.2) still fails the 0° position, and the key bearing rises (below) | No; use the drilled route instead |
| Plate thickness 2.0 | Web stress 74 MPa at T_d and lower key bearing. Groove 3.0, stroke +0.5, pin bending +6 %. Holes are then < 1 t, which is fine for drilling | Optional. **Keep 1.5** (standard stock, adequate) |
| Hole Ø (pin + clearance) | Ø1.60 +0.04/0 on an m6 dowel gives 0.09–0.14 clearance and ±0.26–0.40° play, tolerant of grit. Tighter holes (1.55) halve the play but are less grit-tolerant | **1.60 +0.04/0** |
| Outer profile | Every plate point must fit the rotating groove, so R_OUT is capped at 11.75 all round, plus the floor flat and band cut-out. There is no local bulge room; the ±80° stop faces go on the plate's arc ends | Profile as described; R_OUT **11.75** (was ≤ 12) |
| **Keyed centre** | See below | **Change to double-D + M2 clamp screw** |
| Number of positions | 25° × 7 would give a 2.2 mm web even at Ø2, at a cost of 2.4 % worst-case cosine loss. 30° × 6 loses the 0° position. The C1b vernier needs two pins and two rows | **No, keep 11 × 15°**. Not needed once the holes are drilled |
| Counter-hole depth | 2 → 3 mm: PETG bearing at T_d drops from 21 to 14 MPa (hot handling 7 MPa). Stroke goes from 5 to 6; there is X room in the tray | **Yes** (small cassette detail) |

### Keyed centre

**Current roll pin (Ø1.5 in the Ø5 tip):**
- Structurally good: the contact runs out to r ≈ 4, so plate bearing is only 43 / 86 MPa.
- The cross-hole lies within the 1.5 mm plate plane, only about 0.5 mm from the pin end.
- The plate needs two 1.5-wide notches, which are laser features of about 1 × t.
- **Most important: it does not retain the plate axially.** Through-notches slide off the roll pin, so a separate retainer is needed anyway.

**Double-D (flats 0.75 deep, 3.5 A/F, 3.57 flat width):**
- Laser-, EDM- or mill-friendly large hole.
- The double-D shoulder locates the plate in −X, and an **M2 screw plus a Ø6 washer**, tapped into the pin end, clamps it in +X.
- One part replaces the roll pin and the missing retainer.
- The clamp also removes key play in service.
- Its cost is higher key bearing: **198 / 395 MPa (T_h / T_d)**. This rules out annealed 304 and requires a plate with **σy ≥ 500 MPa**. 301 ½-hard gives SF 1.9 at T_d.
- Tip torsion (conservative inscribed-rectangle model) is 69 / 138 MPa: SF 1.7 at T_d for a 303 pin.
- 1.0 mm flats (3.0 A/F) lower the bearing to 315 MPa but raise the torsion to 157 MPa and leave only 0.7 mm of wall around the M2 tap drill. **0.75 is the balance.**
- The screw head and washer sit in a hub pocket, r ≤ 3.5, in the outboard cheek, clear of the index-pin guide and spring at r ≥ 8.5.
- The pin tip then ends flush with the plate: 2.0 beyond the bracket face instead of 2.5.

## 5. Angular play and accuracy (what the plate tolerance actually controls)

**Free play per 0.01 mm of per-side clearance:**

| Interface | Play |
|---|---|
| Index hole at r 10 | 0.06° |
| Double-D key | 0.32° |
| Carriage single flat (w 3) | 0.38° |

**Consequences:**
- The precise plate sets the **0° bias** (stow alignment), but it cannot remove play at the small-radius interfaces.
- Play is not a stow problem: the slot lead-in can rotate the cassette within its play. It shows up as rattle and impact loading.
- The clamp screw removes key play.
- The carriage flat must be made zero-play (§9).

## 6. Corrections to the investigation (for the record)

1. **PETG inboard counter-hole bearing** (investigation §6 listed "clevis 7 / 14 MPa"). That figure was the 6 mm outboard guide. The 2 mm inboard counter-hole carries 10.5 / **21 MPa**; at hot conditions the handling SF is 1.4. **Fix: 3 mm depth** (7 / 14 MPa).
2. **Carriage anti-rotation flat** (investigation §5, §8, §13: "SF 2.9 handling / 1.4 design"). That used p = 6T/(w²L), which is only valid when the whole flat is preloaded into contact. With a clearance fit, only half the flat bears: **p = 12T/(w²L) = 21 / 42 MPa, SF 1.4 at handling, yields at T_d.** The true value lies in this range, depending on fit.
3. **Roll-pin key** does not retain the plate axially (§4).
4. **Plate outer radius** is 11.75, not 12, with a 0.25 radial groove running clearance (§1).

## 7. Recommendation — **D. KEEP Ø1.5 MM PIN + MINOR PLATE GEOMETRY CHANGE**

| Item | Specification |
|---|---|
| **Pin diameter** | **Ø1.5 mm** |
| **Pin material / type** | Hardened steel dowel, ISO 8734 (DIN 6325), m6, Ø1.5 × 16, chamfered entry. **Must be hardened; no stainless or soft substitute.** |
| **Plate material** | Stainless with **σy ≥ 500 MPa**: **301 ½-hard (ASTM A666)** preferred; 17-4PH (H1025–H1150) acceptable. **Annealed 304/316 not acceptable** (double-D key bearing) |
| **Plate thickness** | **1.5 mm** |
| **Hole diameter** | **Ø1.60 +0.04 / −0**, drilled and reamed (clearance 0.09–0.14; ±0.26–0.40° play) |
| **Index radius** | **10.0 mm**; hole centres at lid-frame −17.5 … +132.5° (index pin at cassette-frame 57.5°) |
| **Web between holes** | **≈ 1.0 mm** (1.01); minimum edge ligament ≈ 0.95 mm |
| **Outline** | R_OUT 11.75; floor flat at dz −5; band cut-out; ±80° stop faces on the arc ends (detail) |
| **Keyed centre** | Double-D, 3.50 A/F (0.75 mm flats on the Ø5 pin tip); M2 × 5 A2 screw plus a Ø6 washer into the pin end, with threadlocker. Replaces the roll pin |
| **Manufacturing process** | Hybrid: laser- or waterjet-cut outline (and double-D), then CNC (or rotary-table) **spot, drill and ream** the 11 holes in one setup, datumed on the double-D. Alternative: all wire EDM (stackable). **Not** laser-cut holes |
| **Tolerances to specify** | All 11 holes: true position **Ø0.06** (≈ ±0.03, about ±0.17° / ±0.34 mm at the far corner) relative to the double-D centre and flat datum. Hole Ø1.60 +0.04/0. Double-D A/F 3.50 +0.02/0 (plate), 3.50 −0.02/0 (pin). Pin-tip flats parallel to the carriage flat within 0.02 mm over the flat width (≈ 0.3°). Plate flatness 0.1. Deburr both faces; 0.1–0.2 edge break on the pin-entry side. Outline ±0.1 (laser grade is fine) |
| **Related detail changes** (proposed, not implemented) | Counter-hole 3 mm deep; stroke 6; pin tip extension 2.0; groove R 12.0 (1.5 mm skin kept) |

**Proposed parameter changes against the investigation's §12** (not added to `nomad.yaml`):

| Parameter | Change |
|---|---|
| SOLAR_INDEX_PLATE_OUTER_RADIUS | 12 → **11.75** |
| SOLAR_INDEX_GROOVE_RADIUS | **new, 12.0** |
| SOLAR_INDEX_COUNTERHOLE_DEPTH | 2 → **3** |
| SOLAR_INDEX_PIN_STROKE | 5 → **6** |
| SOLAR_HUB_PIN_TIP_EXTENSION | 2.5 → **2.0** |
| SOLAR_INDEX_KEY_PIN_DIAMETER | Replaced by **SOLAR_INDEX_KEY_ACROSS_FLATS 3.5** |

All other proposed values stand.

## 8. Sources

**Generic process guidance (published guides, not a supplier commitment):**
- [G1] RivCut, "Laser Cutting Tolerances: Steel, Aluminum, Stainless": fiber laser ±0.1 mm on 0.5–3 mm stainless; holes ≥ 1 × t; features ≥ 1 × t apart (heat); HAZ 0.1–0.2 mm. https://www.rivcut.com/blog/laser-cutting-tolerances
- [G2] Action Stainless, "Design for Waterjet Cutting": kerf 0.030–0.045"; features ≥ 1.5 × kerf. https://www.actionstainless.com/designing-parts-for-waterjet-cutting-kerf-taper-and-minimum-feature-size
- [G3] Waterjet tolerance ranges (±0.05 to ±0.25 mm) as summarised in search results from [Charles Day Steels](https://www.daysteel.co.uk/waterjet-cutting/tolerances/) and [Finepart](https://www.finepart.com/academy/waterjet-cutting-tolerances/). Not individually verified.
- [G4] VACCO, "Photo Chemical Etching Process": hole ≥ 110 % of t; tolerance ±10 % of t. https://vacco-etch.com/photo-etching-guide/
- [G5] Wikipedia, "Photochemical machining": thickness range up to ≈ 2 mm. https://en.wikipedia.org/wiki/Photochemical_machining

**Vendor-specific published data** (one vendor's rules; they do not imply what a local shop can do):
- [V1] SendCutSend, 304 stainless page (±0.005" laser; webs ≥ material thickness): https://sendcutsend.com/materials/stainless-steel/ ; minimum-geometry FAQ (waterjet minimum hole ≥ 0.070"): https://sendcutsend.com/faq/what-are-best-practices-for-minimum-geometry/
- [V2] 247TailorSteel, laser-cutting guidelines (stainless 1.25–1.5 mm: minimum hole 0.8 mm; ISO 9013 tolerances, e.g. ±0.2 mm): https://247tailorsteel.com/en/submission-guidelines/guidelines-for-laser-cutting

**Not researched; generic engineering knowledge (inferred):**
- CNC drill/ream and wire-EDM tolerances;
- material minimum yields;
- ISO 8734 hardness.

A local-shop DFM review is the confirming step.

## 9. Single biggest remaining risk

**The anti-rotation of the Ø5 hub pin in the printed PETG carriage**, not the plate. It is the last link in the lock's torque path, and a precise metal plate cannot compensate for it.

- **Strength:** under a clearance fit the PETG flat sees **21 MPa at handling and 42 MPa at T_d** (§6, item 2). That is below the SF-2 requirement: it yields at the design torque.
- **Play:** a 0.1 mm clearance on a 3 mm flat gives **±3.8° of free play**. That would rattle and impact-load the lock regardless of the ±0.03 mm plate tolerance.

**Mitigation, to decide at implementation (not done here):**
- a set screw (M2.5, heat-set insert, from the −Y side, clear of the cable at dy +3.5…+9.5) preloading the flat, which restores the 10.5 / 21 MPa best case and removes the play;
- or a deeper 0.75 flat (14.8 / 29.7 MPa);
- or a metal anti-rotation insert.

**Verify** in physical tests 2, 3 and 8 of the investigation's plan.

**Secondary risks:**
- Packaging is modeled in 2-D only; it needs the CAD/kernel window check before any persistent geometry.
- Availability of 301 ½-hard or 17-4PH 1.5 mm stock at the chosen shop.

---

Nothing is implemented. No production file, `nomad.yaml`, spec, FeatureScript, Onshape or Git change; no Onshape API calls. Awaiting the owner's decision.
