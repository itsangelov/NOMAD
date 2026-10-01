# Round C.1 — Compute Placement Study and Lid/Port Interaction Screen

**Purpose:** a neutral comparison of five compute placements for the base V0.1 (D-007 is still proposed). It does **not** choose, rank or decide anything.

**Model:** `CAD/tools/compute_placement_study.py`, using the Round C geometry (`base_v01_layout.py`) and `nomad.yaml` working values. Re-run with:

```bash
py CAD/tools/compute_placement_study.py
```

**Evidence levels:**
- *Modeled*: geometry arithmetic on working values.
- *Inferred*: engineering judgement.
- Nothing is physically tested or measured.
- Concept placements B–E are concept-level boxes, not checked against every boss or standoff (Round C concept A is fully checked).

**Status of the inputs:**

| Input | Standing |
|---|---|
| Keyboard 280 × 105 × 8, Pi 5 board 85 × 56 | provisional (spec target / product outline) |
| Body 301 × 235 × 40, Pi stack 30, envelope margin 4, lid 25, 135° max, hinge height 0, port zone Z 4–19, plugs 45 | **working estimates** |
| Component masses (Pi stack 0.10, battery 0.35, power electronics 0.08, compute power 0.03, GNSS 0.02 kg) | **placeholders** for a relative centre-of-mass comparison only |
| "Reasonable airflow" top plenum 5 mm (concept C variant) | **assumption** |

## 1. Stack-height budget (modeled)

| Pi stack height (working 30; inferred real ~25–28) | 25 | 28 | 30 |
|---|---|---|---|
| Palm-rest bay: panel + gap + sled + stack + gap + deck → body height | 34.0 | 37.0 | **39.0** |
| Under keyboard (below the keyboard tray) | 42.5 | 45.5 | **47.5** |
| Under keyboard + 5 mm top plenum | 47.5 | 50.5 | **52.5** |
| Under keyboard, tray cut out over the Pi (keyboard underside as ceiling) | 40.5 | 43.5 | **45.5** |

- Current working body height is 40.
- Free height today: 26.5 under the keyboard, 35 in the palm-rest bays.
- A rear bay (concept D) needs the body depth to grow from 235 to **276.5 (+41.5)**, so the 64 mm-deep Pi envelope fits behind the keyboard tray.

## 2. Concepts

**Representative placements:**
- **A (Round C / D-007):** Pi in the right palm-rest bay; battery in the left bay; power electronics under the keyboard, left; GNSS centre-left; compute power under the keyboard, right.
- **B:** exact mirror of A.
- **C:** Pi under the keyboard, centre-right, body height 47.5. Battery in the left bay (taller, because the body is taller); GNSS and compute power in the right bay.
- **D:** Pi in a rear bay behind the keyboard, body depth 276.5. Battery in the left bay (right bay free for a second pack); GNSS in the right bay.
- **E:** Pi in the right palm-rest bay; battery as a flat pack under the keyboard (left); power electronics under the keyboard, right; GNSS alone in the left palm-rest bay.

| # | Criterion | A right palm | B left palm | C under keyboard | D rear bay | E split |
|---|---|---|---|---|---|---|
| 1 | Body height required (stack 30) | 39.0 → **fits 40** | 39.0 → **fits 40** | **47.5** (45.5 with tray cut-out; 52.5 with plenum) | 39.0 → fits 40; **depth 276.5** | 39.0 → fits 40 |
| 2 | Battery reserve (modeled boxes) | 221 cm³ (one bay) | 221 cm³ | 299 cm³ (bay grows with height; right bay taken by GNSS + compute power) | 221 cm³ + second bay free (up to ~2 × 221) | 293 cm³ flat under keyboard (+~150 cm³ possible right of centre) |
| 3 | Keyboard / trackpad | none | none | typing surface 7.5 mm higher; Pi heat under the keyboard; tray cut-out variant thins keyboard support | none on position; deck grows behind the keyboard | none |
| 4 | Cooling path | front intake → duct → Pi → right-wall exhaust; heat under the right palm (2 mm under the deck) | mirror; exhaust on the left | bottom/side intake → under keyboard → side-wall exhaust; heat under the keys | rear or rear-side exhaust; rear exhaust aims into the lid/hinge region when open (recirculation risk, inferred); heat away from hands | as A; power electronics 9 mm from the Pi adds to right-half heat |
| 5 | Cable proxy (Manhattan XY from Pi centre: ports / display / keyboard / trackpad / compute power; sum) | 210 / 277 / 240 / 135 / 58; **920** | same as A (mirror) | 97 / 152 / 114 / 108 / 94; **564** | 33 / 98 / 106 / 210 / 167; **614** | 210 / 277 / 240 / 135 / 110; **972** |
| 6 | Port accessibility | rear panels via internal extensions (~210); zone Z ≤ 19 (lid screen, §3) | same, panels mirrored | same limits; shorter extensions (~97) | Pi can face the rear wall (~33), but its native USB stack tops out near Z ~26 (inferred), **above** the Z ≈ 19.9 lid-sweep limit, so it still needs extensions or a hinge/lid change | as A |
| 7 | Serviceability | Pi on sled, straight down through the main panel; battery door separate | same | same (Pi under keyboard, still through the main panel); taller bays | same through the main panel, but next to the hinge fasteners and the crowded rear zone | Pi as A; **battery door moves under the keyboard**, where the keyboard-tray standoffs sit today (needs re-layout, inferred) |
| 8 | GNSS gaps: to Pi / power electronics / compute power (placement-dependent) | 90 / **12.3** / 89 | same | 60 / 124 / **10** | 159 / 124 / 48 | 117 / 106 / 164 |
| 9 | Electronics centre of mass (placeholder masses): X; Y as a fraction of depth | −53; 0.30 | +53; 0.30 | −56; 0.33 | −54; 0.35 (of a 276.5-deep base) | −15; **0.52** (battery rearward) |
| 10 | Impact on D-006 hinge | none | none | +7.5 height raises the axis by 7.5 → lid low point +7.5 (relaxes the port conflict, §3) | lid footprint +41.5 deep (heavier lid, taller free edge when open); rear zone crowded under the hinge line | none |
| 11 | Major new risks | palm-rest heat; single-bay battery size; GNSS 12 mm from power electronics | as A, mirrored | thicker machine; keyboard heat; taller body not yet a decision | +41.5 depth (lid and base); exhaust recirculation near the hinge; rear zone congestion; native ports above the lid-sweep limit | rear-heavy electronics (tip-back margin, inferred); battery door under the keyboard; Pi and power electronics co-located |
| 12 | Major advantages | fits today's 40 × 235 envelope; fully checked in Round C; short compute-power link | same as A, exhaust side swapped (user/handedness preference, inferred) | frees both palm bays; shortest internal runs; heat away from palms | Pi next to the rear I/O and display exit; heat away from hands; both palm bays free | largest flat battery volume within 40 × 235; best GNSS isolation of the five placements |

**Notes:**
- A and B are geometrically identical; they differ only in external factors: exhaust side, port-panel side, handedness, and which palm is warmer.
- In every concept the GNSS gaps depend on where GNSS is put. The antenna location (GNSS_ANTENNA_KEEPOUT, TBD) matters more than the module location (inferred).
- The centre-of-mass figures are relative only. Tipping backward with the lid open depends on lid mass and angle, which are not modeled.

## 3. Lid / port interaction screen (modeled; the lid is not redesigned)

**Setup:**
- D-006 working hinge: axis on the base rear top edge (inset 0, height 0); closed gap 2.
- Rear port zone Z 4–19; external plug corridor 45 mm behind the rear face.
- Positive clearance = gap to the plug zone; negative = the lid passes through it.

| Lid thickness | Lid lowest Z in the plug corridor at 105° / 120° / 135° | Clearance to the plug zone at 135° | Highest port top allowed at 135° | Max opening angle for today's zone | Hinge height needed at 135° |
|---|---|---|---|---|---|
| 25 (working) | 33.0 / 26.5 / 20.9 | **+1.91** | 19.9 | 137.5° | 0 |
| 31.5 (B.1 V1) | 31.3 / 23.3 / 16.3 | **−2.69** | 15.3 | 126.5° | 2.2 |
| 42.5 (B.2 Concept C) | 28.5 / 17.8 / 8.5 | **−10.47** | 7.5 | 116.5° | 6.8 |

**The constraint the eventual lid architecture must satisfy** (axis inset 0 at height h; lid resting at H + G when closed; opening angle θ > 90°; plugs long enough to reach the lid's hinge-end corner):

```
z_low = H + h + (G + T − h) · cos θ_max   ≥   port-zone top + MIN_GAP
```

- **Today** (H 40, h 0, θ 135°, port top 19): G + T ≤ 28.3, so **lid thickness ≤ 26.3**.
- Each variable relaxes the constraint in a known direction:
  - a taller body (H) or higher hinge axis (h) raises the lid's low point;
  - a smaller maximum angle lowers the sweep;
  - lower ports lower the zone top.
- **Body height 47.5** (concept C): the 31.5 lid clears (+4.81); the 42.5 lid still does not (−2.97).
- **Plug length matters.** The lid's hinge-end face passes through Y 255, Z 20.0 at 135° for any thickness ≥ 31.5. So plugs that end within 20 mm of the rear face (right-angle plugs) keep **+0.71** clearance with the 31.5 and 42.5 lids (below MIN_GAP 1.0; +1.91 with the 25 lid); plugs within 15 mm keep **+4.24** for all three. Long straight plugs (45 mm) set the limits above.
- **Outside this screen:** side-wall ports avoid the rear sweep entirely. Their interaction with laterally deploying solar cassettes (D-004) is not screened yet.

## 4. Hard constraints vs current assumptions

| Hard constraints (accepted decisions / requirements / geometry) | Current assumptions (working, changeable) |
|---|---|
| D-003: keyboard and trackpad centred on the centreline, trackpad below | Body height 40, body depth 235 (formula), width 301 |
| D-006 *direction*: hinge axis at or near the base rear face | Hinge axis height 0 and inset 0 (TBD within D-006) |
| D-004: lateral solar deployment from the lid (constrains side ports and the lid, not the base layout) | Lid thickness 25; maximum angle 135° |
| Battery removable, never sealed; service without removing the keyboard or display; no structural electronics; screws/inserts, no glue | Pi stack 30 high, 4 mm envelope margin, GNSS not stacked |
| MIN_GAP as a *requirement* (its 1.0 value is working) | Port zone Z 4–19, plugs 45 long, rear I/O |
| Lid-sweep geometry for a given axis, thickness and angle (physics) | Battery 90 × 82 × 30; power electronics, GNSS and compute-power envelopes |
| Pi 5 board outline 85 × 56 and keyboard 280 × 105 × ≤ 8 (provisional, but tied to real or target parts) | Cooling duct 20, vent zones, placeholder masses |

## 5. Measurements that would most reduce uncertainty

1. **The real Pi 5 + Active Cooler + M.2 HAT+ + 2230 stack**: height, footprint and connector overhang (caliper). Decides whether C is feasible and the palm-bay margin (39.0 vs 40).
2. **Required lid thickness** (display module + controller + solar rail layer + back plate). Decides the rear-port constraint (§3).
3. **Hinge hardware axis position** (mechanism prototype). h relaxes the port constraint almost 1 : 1.
4. **Measured power budget → required battery energy → battery volume.** Decides whether 221 cm³ is enough or whether C, D or E volumes are needed.
5. **Sustained-load Pi temperature in a closed 35 mm bay**, and the deck surface temperature (simple box test). Decides whether palm-rest compute is acceptable.
6. **Plug types and lengths** for the intended ports (right-angle vs straight).
7. **Lid and base masses**, for a tip-back stability check at 105–135°.
8. **GNSS C/N0 with the Pi and a DC-DC converter running** at candidate separations.

## 6. Proposed next decision set (for the owner; nothing decided here)

**D-007 items that can safely stay provisional** (parametric, reversible, no architecture change):
- Envelope sizes (battery, power electronics, GNSS, compute power); boss, post and standoff positions and sizes.
- Tray and sled details; cable-corridor sections; cooling duct and vent-zone sizes.
- Port-panel width and X position; panel seam positions; wall/plate thicknesses.

**D-007 items that need architectural review:**
- Compute location (A–E).
- Battery location.
- GNSS as a separate module vs stacked.
- Rear vs side I/O, given D-006 and the lid screen.
- Whether BODY_HEIGHT (C) or BODY_DEPTH (D) may change.
- The open-bottom shell with a separate battery door as the service strategy.
- The trio of lid thickness, hinge axis height and maximum opening angle, which jointly sets the port constraint.

**Minimum decisions before building the persistent Base V0.1 Feature Studio:**
1. Compute location: one of A–E, or explicit acceptance of A as a *working placeholder*.
2. Battery location (follows from 1).
3. I/O policy: rear panels limited to Z ≤ 19 with lid thickness ≤ 26.3 (or a hinge/angle change), vs side I/O. Can also be accepted as a placeholder.
4. GNSS separate-module assumption.
5. Confirmation that BODY_HEIGHT / BODY_DEPTH stay at working 40 / 235 for V0.1, or the new working values.
6. That the persistent feature is a parametric envelope model regenerated from `nomad.yaml` (a placeholder, not a frozen design).

**Additional geometry studies that would help:**
- **Lid-architecture screen:** lid thickness (with the B.1/B.2 rail layer), hinge axis height and maximum angle against the §3 constraint.
- **Side-I/O variant of Round C**, including side plug zones vs deployed solar cassettes at 105–135° (D-004).
- **Tip-back stability model** once lid mass is estimated.
- **Re-run of this study with the measured Pi stack** (automatic: `PI_STACK_HEIGHT`).
- **Concept C tray-cut-out variant:** keyboard support stiffness over the opening.
- **Airflow-path sketch** for whichever compute bay is chosen (intake/exhaust areas vs vent zones).
- **Shell print split** for a ≤ 250 mm bed, if the print service needs it.
