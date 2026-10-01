# B1 hinge hardware, second pass: TorqMaster small families

One published configuration fits B1 better than SB-254 geometrically: **SB-188-SB-261, torque band -6**. It has the same Ø7.11 barrel, but it is balanced, 33.8 mm long instead of 52.3, its flags reach 12.7 mm instead of about 43, and it uses M3 holes. The cost is torque headroom: band -6 is 0.96–1.13 N·m, a minimum safety factor of 1.16 against 0.83, and no higher balanced band is published for that housing.

Two further findings apply to every candidate:
- No barrel larger than Ø6.0 can meet all three B1 targets at once (flush with the lid edge, 1 mm panel clearance, 4.5 mm rim). Every candidate found forces a compromise.
- With the axis at z 69, both flag sets sit 1.2–1.6 mm below the panel underside. A standard M3 screw head does not fit there.

This was research only: no repo, YAML, FeatureScript, Onshape or Git changes. Labels used: **PUB** = manufacturer-published, **INF** = my reading of a drawing, **CALC** = my arithmetic. Nothing has been physically tested. Conversions: 1 in = 25.4 mm, 1 lb·in = 0.11298 N·m.

Terms used throughout:
- **Barrel OD:** outer diameter of the friction housing.
- **Shaft OD:** the rotating shaft.
- **Leaf thickness:** thickness of the steel flag.
- **Mounting-face height:** distance from the axis to the flag face.
- **Envelope:** barrel plus flags.

## 1. Candidate table

| Candidate | Barrel OD | Shaft OD | Length (axial) | Flags (closed state) | Holes | Axis to flag | Torque bands (N·m) | Balance | Status / 3D |
|---|---|---|---|---|---|---|---|---|---|
| **SB-188-SB-254** (Type-1) | Ø7.11 (INF, family housing; not dimensioned on this drawing) | Ø4.78 (INF, family) | 52.3 overall; 0.76 shaft ends | 2 fixed outer flags 11.4 wide + 1 rotating centre flag 25.7 wide; reach ≈ 43; t 1.14 | 8 × Ø4.29 (M4) + 8 × Ø3.25 (M3); first row 11.4 from axis, rows 7.9 apart | 4.06 to the leaf mid-plane (INF), so faces at 3.49 / 4.64 | L 0.56–0.93 · **M 0.96–1.36** · **H 1.36–1.69** | Balanced (PUB) | Stock; title block says "USED ON: CUSTOM"; **no IGES listed** |
| SB-188-SB-202 (Type-1) | **Ø7.11** (R/Ø .28, dimensioned) | Ø4.78 (INF) | 52.3 | 4 flags 7.11 wide, reach 26.2, t 1.14 | 8 × Ø3.25 (M3); 11.4 / 19.3 from axis | 4.06 (as SB-254) | CCW: L 0.56–1.02 · M 1.02–1.36 · H 1.36–1.69; other direction not given | Product page says unbalanced; drawing shows both "CW = CCW" and "CW < CCW" | Stock; IGES available |
| **SB-188-SB-261** (Type-2) | **Ø7.11** (R .14, dimensioned) | Ø4.78 (INF) | **33.8** overall; housing ≈ 30.7 (CALC); 1.52 shaft ends | **4 flags (2 fixed + 2 rotating), each 7.37 wide, reach 12.7, t 1.14**; configurations A–D (A = all four flags parallel, matching B1 closed) | 4 × Ø3.51 (M3), one per flag, **7.87 from axis**; axial pitch 7.37 / 9.40 | ".14": flag tangent to barrel (INF); faces 3.56 / 4.70 | -1 0.11–0.28 … -5 0.79–0.96 · **-6 0.96–1.13** | **Balanced** (PUB) | Stock ("immediate delivery, volume restricted, no tooling charge"); IGES available |
| SB-188-SB-263 / 264 (Type-2) | Ø7.11 (R .14) | Ø4.78 (INF) | 33.8 | Same flags, but **grouped**: fixed pair at one end, rotating pair at the other (14.7 mm each) | 4 × Ø3.51, 7.87 from axis | As SB-261 | High direction (CCW) -7 1.19–1.36; low direction ≈ 65 % = 0.77–0.88 (CALC from the catalogue's "approx. 35 % less") | Unbalanced | Stock; IGES available |
| SB-188-SB-260 (Type-2) | Ø7.11 | Ø4.78 (INF) | 33.8 | Fixed and rotating flags in opposite directions as drawn | 4 × Ø3.51 | As SB-261 | Same as 263/264 | Unbalanced | Stock; IGES available |
| SB-188-CF-103 / 104 (Type-2, CF) | Ø7.11 (R .14) | **Ø4.78 (Ø .188, dimensioned)** | 43.7 overall, including the shaft paddle | Fixed flags tangent (t 1.14, hole 7.87 from axis); **rotating member is a 2.03 × 8.89 paddle centred on the axis**, 20.8 long axially | 2 × Ø3.51 fixed + 2 × Ø3.18 in the paddle at 8.1 pitch | Fixed flag tangent; paddle on the axis | Maximum 1.13 (10 lb·in); bands not published | Balanced | Stock; IGES available |
| **SB-200-SB-103** (also 104 / 113) | **Ø7.62** (R .15, dimensioned) | Not dimensioned | 40.1 overall (SB-104: 42.7); 2 leaves × 19.05; 0.76 shaft ends | 1 fixed + 1 rotating leaf, both on the same side as drawn; reach 14.7, t 1.14, R .07 joggle | SB-103: 4 × Ø3.20 (M3); SB-104 / 113: Ø4.37 (M4); 10.4 from axis, 9.9–10.0 pitch | ".17" to a leaf face; which face is ambiguous (3.18–4.32 or 4.32–5.46) | -4 0.96–1.24 · **-5 1.24–1.70** | **Balanced** (PUB) | Stock; IGES available |
| ZE-188-CF-114 / CF-214 | **Ø8.13** (R .16) | Ø4.78 | 43.7 / 66.0 | Zinc foot, mounting face 3.30 below axis; rotating paddle on axis | Ø3.05 / Ø3.0 | Foot face 3.30 | Dash numbers -4 … -20 have **no units**; product pages say 1–8 and 1–14 lb·in | Balanced or unbalanced | Exceeds Ø8; reference only |

**Common data for all rows:**
- Life: 30,000+ cycles (PUB); the SB-188 datasheet chart shows 80,000 cycles.
- Rotation: 360° with no stops (PUB).
- Material: not stated; every drawing says "MATERIAL N/A".
- Finish: black oxide standard on SB-188, SB-188 Type-2 and SB-200.
- Corrosion: "corrosion protection available", unspecified for the SB families. ZE/ZC list nickel-plated bands, stainless shafts, e-coat and powder coat.
- **No temperature range published for any of them.**
- **No radial, axial or moment load capacity published for any of them.**
- REACH and RoHS marks on the SB-254 and SB-261 datasheets.

**Rejected on torque:**
- **SB-188 Type-1:** SB-101/102, 103/104, 108/109, 111/112, 118, 119/120, 121/122, CF-105 and KN-101 all top out at 0.85 N·m or less.
- **SB-188 Type-2:** SB-115/116, SB-117 and CF-101 all fail. CF-101's low direction is 65 % of 12 lb·in, about 0.88 N·m at best.
- **Other families:** SB-156 (1–4 lb·in), ZC-188 (3–8 lb·in, closed housing), and ZE-188-SB / SA (1–4 lb·in).
- SB-231 and SB-252 (5–15 lb·in) are unbalanced with the same length as SB-202; I did not read their drawings.

## 2. B1 fit calculations (CALC)

Baseline from the hinge-line study: axis (y 3, z 69); panel z 67–71; rim = 11.5 − panel edge; lid back (leaf underside) z 61; leaf top z 73.

| Barrel | Panel edge at axis y 3 | Rim left | Barrel beyond lid edge | Flush option (axis y = r): panel / rim | Keep rim 4.5 (panel 7): axis / protrusion | Ø6 sleeve to panel (at axis y 3) | Barrel top z |
|---|---|---|---|---|---|---|---|
| Ø7.11 (SB-188 all) | **7.56** | 3.94 | 0.56 | 8.11 / 3.39 | 2.44 / 1.11 | 1.56 (Ø5: 2.06) | 72.56 |
| Ø7.62 (SB-200) | 7.81 | 3.69 | 0.81 | 8.62 / 2.88 | 2.19 / 1.62 | 1.81 | 72.81 |
| Ø8.13 (ZE-188) | 8.06 | 3.44 | 1.06 | 9.13 / 2.37 | 1.94 / 2.13 | 2.06 | **73.06** (0.06 above leaf top) |

- **General constraint:** being flush, having 1 mm clearance and keeping the 4.5 mm rim together require 2r + 1 ≤ 7, so a barrel of **Ø6.0 or less**. Every candidate forces the owner to relax one of the three.
- **Cable sleeve:** a sleeve of Ø6 or less is never the governing part. Axially, the sleeve must clear the shaft-end protrusion: 1.52 mm on Type-2, 0.76 mm on Type-1 and SB-200.

**Mounting space (INF/CALC):**
- **Flags must sit under the panel.** Tangent flags can only lie horizontally toward +y in the closed state; the other directions leave the lid edge, cross the leaf top, or enter the lid core. That places them at about z 64.3–65.5 (Type-1/2) or 64.7–65.8 (SB-200, depending on how ".17" is referenced).
- **Every hole is behind the panel edge:**

  | Hinge | First hole at y | Flag ends at y |
  |---|---|---|
  | SB-261 | 10.9 | 15.7 |
  | SB-200-103 | 13.4 | 17.7 |
  | SB-254 / SB-202 | 14.4 | 46 / 29 |
- **Headroom to the panel underside is 1.5–1.6 mm** (SB-200: 1.2–2.3). An ISO 7380 M3 head (1.65 mm) does not fit for either flag set. This applies to **every candidate**, so it does not separate them.
- Possible changes: lower the axis to about z 68.4 (−0.6 mm) for 2.15 mm of headroom; use rivets or wafer heads; or fasten where the leaf frame rises above the flags (outside the panel footprint). Any of these is an approval-gated B1 change, and lowering the axis means re-running the leaf-core and plug checks.
- **Lid-side flags:** need a printed pad about 3.3 mm above the lid back. An insert in pad plus skin (about 5.8 mm of material) must not reach the foil.
- **Axial length per hinge:**

  | Hinge | Per hinge | Two hinges |
  |---|---|---|
  | SB-261 | 33.8 | 67.6 |
  | SB-200-103 | 40.1 | 80.3 |
  | SB-254 | 52.3 | 104.6 |

  SB-261's shorter length frees 18.5 mm per hinge along x for the cable's 12 mm-radius exit.
- **CF-103/104 does not help:** its rotating paddle is centred on the axis, so it sweeps at least r 4.56 relative to the lid, plus whatever clamps it. That is effectively a barrel larger than Ø9 over a 20.8 mm length.

**Torque at the likely operating point** (the lowest band whose minimum is at least 0.83). Deployment force is at the panel far edge with a 227.6 mm lever; gravity shifts it by up to ±2.2 N.

| Configuration | Per hinge | SF minimum (vs 0.83) | Pair | Deployment force | Pair vs 0.49 gravity |
|---|---|---|---|---|---|
| SB-261-6 | 0.96–1.13 | 1.16 | 1.92–2.26 | 8.4–9.9 N | 3.9 |
| SB-254-M / H | 0.96–1.36 / 1.36–1.69 | 1.16 / 1.63 | 1.92–2.71 / 2.71–3.39 | 8.4–11.9 / 11.9–14.9 N | 3.9 / 5.5 |
| SB-200-103-4 / -5 | 0.96–1.24 / 1.24–1.70 | 1.16 / 1.50 | 1.92–2.49 / 2.49–3.39 | 8.4–10.9 / 10.9–14.9 N | 3.9 / 5.1 |
| SB-202-M (CCW only) | 1.02–1.36 | 1.23 (other direction unknown) | 2.03–2.71 | 8.9–11.9 N | 4.2 |
| SB-263/264-7, low direction | ≈ 0.77–0.88 | **0.93** | — | — | fails |

Absolute range across the shortlist: 0.96 (minimum) to 1.70 (maximum) N·m per hinge.

## 3. Shortlist (factual, no order implied)

- **SB-188-SB-261-6.**
  - Fits better than SB-254: same barrel, 18.5 mm shorter, compact M3 flags, balanced, configuration A matches B1 closed.
  - Remaining questions: thin torque margin (SF 1.16, no higher balanced band published) and which flags are fixed or rotating in A–D.
  - IGES is available.
- **SB-188-SB-254-M / H** (reference).
  - Torque headroom up to 1.69.
  - Long (52.3) with 43 mm flags; no IGES listed.
- **SB-200-SB-103-4 / -5.**
  - Balanced with headroom to 1.70; 2 × M3 per leaf; 40.1 mm long.
  - Costs: Ø7.62 means about +0.25 mm on the panel edge or rim versus SB-188; the ".17" reference and the shaft OD are unconfirmed.
  - IGES is available.
- **Semi-custom question, not a published part:** SB-263/264 grouped-flag geometry in **balanced** torque at 0.96 minimum or higher, or an SB-261 band above 10 lb·in.

**Special investigation result.** The catalogue does state "ability to mix and match housings & shafts / adapters" and offers semi-custom builds "using standard parts from our in-house library". But no published Type-2 configuration shows balanced torque above 10.0 lb·in. The Type-2 series lists 0.5–6.0 lb·in for single and 1.0–12.0 for double hinges, and the 12.0 appears only as the high direction of unbalanced parts. **A better-than-SB-261 torque in the SB-188 Type-2 interface is plausible but unproven, and only TorqMaster can confirm it.**

SB-202 is excluded from the shortlist: it is the same length as SB-254 and its torque balance is ambiguous.

## 4. Questions for TorqMaster

1. Barrel OD with tolerance for SB-188 Type-1, Type-2 and SB-200; shaft OD (SB-200 is not dimensioned); shaft-end protrusion.
2. SB-261 and SB-200-SB-103 drawings: is the ".14" / ".17" flag dimension to the inner face, the outer face or the mid-plane?
3. SB-261 configurations A–D: which flags are fixed and which rotate? Is 190° of travel free of flag interference in configuration A?
4. Can SB-261 be supplied balanced at 10–12 lb·in, or with a tighter band (for example 9.5–10.0)? Can SB-263/264 be supplied balanced, and in which bands?
5. SB-202: is it balanced or unbalanced? Low-direction torque for each band of SB-202, SB-260 and SB-263/264.
6. Materials (housing/bands, shaft, flags, hardness) and finish options. What exactly is "corrosion protection" for the SB families (nickel bands, stainless shaft)? Suitability for outdoor humidity and dust.
7. Operating and storage temperature range, and torque variation with temperature.
8. Static radial, axial and flag-bending (moment) capacity, and allowable shock load. **None of these are published.**
9. Torque over life: drift across 30,000 cycles, test angle and speed, breakaway versus running torque, springback and backlash in degrees.
10. Flag options: two holes per flag, M3 countersink or PEM studs, other hole positions, thicker flags. Is there a low-profile fastening option for 1.5 mm headroom?
11. IGES/STEP for SB-254 (none listed).
12. Price at 4–10 and about 100 units; lead time; MOQ/NRE for semi-custom; shipping to Bulgaria; EU distributor; HS code; REACH/RoHS declarations.

## 5. Recommendation: A, contact TorqMaster

The remaining selectors are vendor-only facts: balanced bands above 10 lb·in in the Type-2 housing, which flags rotate, load ratings, material and temperature. CAD cannot answer them.

One owner decision is needed regardless of vendor: which of the three B1 targets to relax for a Ø7.11–7.62 barrel, and how to fasten flags in the 1.5 mm under-panel headroom.

After TorqMaster replies, option B (scratch CAD of SB-261 and SB-200-SB-103 from their published IGES) is the logical next step. It needs your approval.

## Report
- **COMPLETED:** read the TorqMaster drawings and pages for SB-188 Type-1, Type-2, SB-200 and ZE-188.
- **CURRENT MODEL:** unchanged.
- **ASSUMPTIONS:** the drawings' ".14", ".16" and ".17" references are interpreted as stated above (INF); the 0.83 N·m per hinge and 0.49 N·m gravity figures come from the Phase 2 calculations.
- **PROBLEMS:** no load, material or temperature data published; SB-254 has no IGES; the Ø6.0 geometric limit; the under-panel headroom.
- **NEXT ACTION:** send the questions in section 4.
- **APPROVAL REQUIRED:** contacting the vendor; the B1 constraint relaxation; any CAD work.