# Round E — Solar Hub / Pin Load Sanity Check (F3 Option B baseline)

**Status:** analysis only. No CAD, FeatureScript, Onshape, parameter or Git change.

**Baseline:** the implemented F3 Option B geometry, as in the repository (`e_lid_layout.py` evaluated from `nomad.yaml`).

**Evidence levels:**
- Geometry: *modeled*.
- Masses, loads and stresses: *inferred* (hand calculations, stated assumptions, no FEA, nothing tested).

**Conclusion: A — KEEP CURRENT DESIGN.**

## 1. Geometry used (right cassette, deployed; left is mirrored)

| Item | Value |
|---|---|
| Tilt axis | along X, at Y 131.8, Z 57.5 (lid frame) |
| Hub pin | Ø5, fixed in the carriage. It exits the carriage at X 147 (deployed) and spans the 11.5 mm link to the bracket |
| Hub bracket bore | X 158.5–168.5: **engagement L = 10 mm**, wall 2.5 all round (bracket Z 52.5–63, 17 wide) |
| Cassette | X 158.5–306 (147.5), Y 17.5–217.5 (200), Z 63–71 (8) |
| Centre of mass (assumed at the envelope centre) | X 232.25, Y 117.5, Z 67 |

**Lever arms:**

| Lever | mm |
|---|---|
| Centre of mass (CoG) to bore mid-length (X 163.5) | **68.75** |
| Outboard edge to bore mid-length | **142.5** |
| CoG to pin root (carriage face) | **85.25** |
| Outboard edge to pin root | **159.0** |
| CoG offset from the tilt axis, perpendicular | √(14.3² + 9.5²) = **17.2** |
| Far corner to the tilt axis | **114.3** |

The lid hinge axis is parallel to X, so X stays horizontal in every lid pose. The full weight therefore always acts perpendicular to the pin, and the gravity bending case below holds at every lid angle and tilt.

## 2. Cassette mass (inferred; the panel is not selected)

**Printed tray** (PETG 1.27 g/cm³, near-solid thin sections):

| Component | Mass |
|---|---|
| 1.2 mm back skin | 45 g |
| 1.6 mm × 8 mm perimeter | 11 g |
| Three 6 × 1.2 ribs | 5 g |
| Hub bracket | 2 g |
| Panel retention lip | 5 g |
| **Tray total** | **≈ 70 g** |

**Panel options** (≈ 190 × 140 mm active area):

| Panel type | Areal mass | Mass |
|---|---|---|
| Flexible ETFE laminate | ~2.5 kg/m² | ≈ 65 g |
| Epoxy / PET on PCB | ~3.6 kg/m² | ≈ 95 g |
| Glass laminate | ~9 kg/m² | ≈ 240 g |

**Other items:** wiring and connector about 10 g; index / latch / insert hardware about 5–15 g.

| Case | Total |
|---|---|
| Light (ETFE) | ≈ 0.15 kg |
| **Nominal** (ETFE / epoxy) | **≈ 0.20 kg** |
| **Design upper bound** (glass panel) | **0.35 kg** |

All checks below use the upper bound (0.35 kg, W = 3.43 N) unless stated.

## 3. Gravity

**Pin bending (perpendicular to the axis):**
- M = W · L_CoG.
- At the bore: **101 / 135 / 236 N·mm** for 0.15 / 0.20 / 0.35 kg.
- At the pin root: 125 / 167 / 293 N·mm.

**Torque about the tilt axis:**
- T = W · r⊥, at most 3.43 × 17.2 = **59 N·mm** (34 N·mm nominal).
- This torque is carried by the index lock, not by the pin's bending strength.

**Is gravity significant?** Not for strength:
- sustained bore bearing is 2.9 MPa, about 10 % of the short-term allowable;
- pin bending stress is 24 MPa, about 12 % of the weakest metal considered.

Gravity matters only for long-term creep and droop (§6).

## 4. Handling load case (the single accidental case)

**F = 5 N (≈ 0.5 kgf) at the cassette's outboard corner, perpendicular to the panel, added to the 0.35 kg weight in the same direction.**

**Why 5 N:**
- Tilting a detented cassette by hand, or a light accidental brush while it is deployed, is a fingertip or palm load. Typical deliberate control-operating forces are about 1–5 N; 5 N is the top of that range.
- Loads well above this are abuse, or a gust large enough that the stated procedure (stow the wings) applies.
- The worst lever (outboard edge) and the heaviest panel are stacked on top of it. The acceptance requirement is SF ≥ 2 against *conservative printed* allowables. Together these cover occasional overshoot.
- The retired 10 N case is also shown for reference: nothing reaches its allowable even then.

**Resulting loads:**

| Quantity | Value |
|---|---|
| Moment at the bore mid-length | M_b = 3.43 × 68.75 + 5 × 142.5 = **949 N·mm** |
| Moment at the pin root | M_r = 3.43 × 85.25 + 5 × 159.0 = **1088 N·mm** |
| Shear | V = 8.43 N |
| Torque about the axis (to the index lock) | T = 5 × 114.3 + 59 = **630 N·mm** |

## 5. Pin, Ø5 metal

Material is not selected. D-004 and the CLAUDE.md rules require a **metal** pin; it is not evaluated as plastic.

**Section properties:** Z = πd³/32 = 12.27 mm³; A = 19.6 mm²; Zp = πd³/16 = 24.5 mm³.

| Stress | Equation | Value |
|---|---|---|
| Bending at the root | σ = M_r / Z | **88.6 MPa** |
| Transverse shear | τ = 4V / 3A | **0.57 MPa** (negligible) |
| Torsion, only if the pin carries the index torque | τ = T / Zp | 25.7 MPa |
| Combined | σ_vM = √(σ² + 3τ²) | **99 MPa** |

**Safety factor on yield for the combined case:**

| Pin material | Yield (MPa) | SF |
|---|---|---|
| Annealed 304 stainless (weakest plausible metal) | 205 | **2.1** |
| 6061-T6 aluminium | 275 | 2.8 |
| Cold-drawn 303 stainless | 415 | 4.2 |
| Hardened steel dowel | ~1000 | ≥ 10 |

**Deflection:** slope over the 11.5 mm free span is 1.8 mrad, which is 0.25 mm at the cassette tip. Negligible.

**Verdict:** adequate in any common metal. Only plastic pins are excluded, and they already are.

## 6. Printed PETG hub bracket (bore Ø5, L = 10, wall t = 2.5)

**Model: rigid pin in a short bore under a moment.**
- Peak bearing: p_max = V/(dL) + 6M_b/(dL²).
- End reaction on each half-length: F_e = 1.5 M_b / L + V/2, acting over L_e = L/2 = 5 mm.
- At the inboard end, the pin bears on the wall **under** the pin. That load returns to the bracket body through the two 2.5 mm side ligaments, as in a pin-loaded lug.

**Assumed design allowables** (printed PETG, conservative, below typical datasheet values):

| Allowable | MPa |
|---|---|
| Short-term bearing | 30 |
| Tension, in-layer | 35 |
| Tension, across layers | 20 |
| Shear, in-layer | 15 |
| Shear, across layers | 10 |
| Sustained (creep, warm) bearing | 8 |
| Sustained shear | 4 |

| Check (0.35 kg + 5 N) | Stress | SF (favourable / unfavourable layer orientation) |
|---|---|---|
| Peak bearing at the bore end | 11.6 MPa | **2.6** |
| Tear-out of the under-pin wall: F_e / (2 · t · L_e), F_e = 146 N | 5.9 MPa | **2.5** / **1.7** |
| Net tension in the side ligaments, nominal: F_e / (2 · t · L_e) | 5.9 MPa | **5.9** / **3.4** |
| Net tension with an elastic hole Kt ≈ 2.5 (peak) | 14.6 MPa | 2.4 / **1.4** |
| Sustained gravity only (0.35 kg), bearing | 2.9 MPa | **2.8** |
| Sustained gravity only (0.35 kg), tear-out (F_e 37 N) | 1.5 MPa | 2.7 |

**At nominal mass (0.20 kg + 5 N):** p_max 10.3 MPa, F_e 131 N, so every SF is about 12 % higher.

**Reference only (retired 10 N case, 0.35 kg):** p_max 20.2 MPa, bearing SF 1.5. Still below the allowable.

**Layer orientation:**
- **Favourable (bore axis vertical in the print):** the loads stay in-plane within the layers.
- **Unfavourable:** a tray printed flat, panel side down, loads the side ligaments *across* the layers.
- The one sub-2 value, SF 1.4, is the *elastic peak* with the heavy panel, the full 5 N, and the unfavourable orientation all stacked. On a nominal (net-section) basis the same case has SF 3.4.

**Wall bending:** the 2.5 mm under-pin wall is not a free plate. It is part of a closed ring backed by the side ligaments, so the lug checks above govern.

## 7. Is 10 mm of bore engagement enough?

Solving p_max(L) = allowable / SF for the design case (0.35 kg + 5 N):

| Criterion | Required L |
|---|---|
| Bearing 30 MPa, SF 2.0 | **8.8 mm** |
| Bearing 30 MPa, SF 1.5 | 7.6 mm |
| Bearing 20 MPa (extra-pessimistic), SF 2.0 | 10.8 mm |

**The current 10 mm is adequate:** 14 % more than the SF-2 requirement, and a 2.6 SF on peak bearing.

The 20 mm bore suggested in the F3 investigation (O1) came from the 10 N case. It is **not required** under realistic loads.

## 8. Rest of the load path (quick check)

**Carriage, deployed moment 1256 N·mm:**
- pin bearing in the carriage (walls 3.5 below, 2.0 above): 3.8 MPa at 20 mm embedment, 0.9 MPa at 40 mm;
- lip reaction about 47 N, lip bending about 5.7 MPa.

Comfortable margins.

## 9. Conclusion — **A. KEEP CURRENT DESIGN**

**Adequacy (inferred):**
- The Ø5 metal pin, the 2.5 mm-wall bracket and the 10 mm bore are adequate for the realistic cases.
- Gravity with any plausible panel is minor: bearing SF ≈ 2.8 sustained and ≥ 10 short-term.
- The 5 N handling case holds SF ≥ 2 on bearing, tear-out, net section and pin yield in the favourable print orientation, and SF ≥ 1.7 on nominal checks in the worst orientation.

**No geometry change.** This is not a hardware change either; the pin stays "metal" as already specified.

**F3 Option B stays locked. Move on to the next NOMAD subsystem.**

**Assumptions recorded for later detailing (not design changes):**
1. The pin must be metal (any common stainless, steel or 6061 aluminium dowel is adequate), as D-004 already requires.
2. **Index lock input:** it must hold up to about **0.63 N·m** about the tilt axis (handling case), plus 0.06 N·m from gravity. The printed gears must not carry this torque, as already stated in D-004.
3. **Bracket printing:** at least 4 perimeters and solid infill around the bore. If the bracket is integral with a flat-printed tray, the across-layer case above applies (still adequate).

## 10. Remaining uncertainty

| Item | Effect | How to close |
|---|---|---|
| Panel mass (not selected) | Checked up to 0.35 kg; glass is the upper bound | Recheck when a panel is chosen |
| **Temperature:** a sun-heated panel can reach about 60–70 °C near a PETG bracket (Tg ≈ 80 °C) | Strength and creep resistance could drop about 40–50 %: short-term SF ≈ 1.4, sustained SF ≈ 1.5 | Hot hang/creep check in the next physical round |
| Printed-strength scatter (layer adhesion, print settings) | Allowables are assumed | Coupon or bracket pull test in the next physical round |
| Bore/pin fit clearance and pin axial retention | Not designed. Play gives droop and impact loads, not static overload | Detail design (bushing or fit decision) |
| Index lock design | Not designed. It carries the 0.63 N·m | Next solar detailing step |
| Centre of mass assumed at the envelope centre | ±10 % on the gravity moment; small against the handling moment | Actual cassette design |
