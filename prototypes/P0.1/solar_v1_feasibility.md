# P0.1 Round B.1: V1 Solar Layout Feasibility Pass

**Status: modeled, P0.1 working geometry. V1 is NOT chosen.** This pass asks one question: can V1 physically exist as a sensible printed lid while preserving the D-004 motion?

## Method

- **Model:** `CAD/tools/solar_v1_feasibility.py`, the exact prism model from Round B extended with:
  - the display bezel frame and lid walls, with side-wall openings modeled per side
  - the hub bracket: in V1 the tilt axis lies in the rail layer, so a bracket has to join the pin to the cassette's inboard end, rising through a slot in the top of the rail
  - a provisional protected cable envelope, rolling service loops, and a routing search to the hinge side
  - the thicker lid on the D-004 rear-face hinge
- **Provisional what-if constants** (not in `nomad.yaml`; not a wire or hardware selection): cable envelope Ø6, service-loop bend radius 20, bracket length 10, PETG E = 2000 MPa for a rough plate estimate.
- **States:**
  - lid 0°, 105° and 135°
  - left/right slide extensions 0–1 in quarter steps, in every combination
  - deployed tilt 0, ±15, ±30, ±45, ±60 and ±75°
- **Requirements:** clearance ≥ MIN_GAP (1.0) everywhere; the table at z = 0.
- **Two configurations:**
  - **V1 as specified** (Round B values).
  - **V1 + minimal fixes:** the smallest changes that clear every failure found in V1 as specified.
- **Onshape cross-check:** one scratch run (9 API requests) rebuilt the V1 core skeleton (cassette, pin, carriage, rail, display, base) with the production builder in six states. It matched the model exactly: `S:-z49.1 D:-z49.1 a:-z6.5 b:-z-17.3 c:-z38.5 d:-z28.5` (no overlapping pairs; minimum heights above the table).

## Findings (modeled; structural statements are inferred unless stated)

### Failures in V1 as specified
1. **Pin and cable don't fit together.** A protected cable must run beside the Ø5 pin (it can't sit above it, where it would hit the other stowed cassette). It sits 3.5–9.5 mm from the axis. That exceeds the 12 mm carriage by 3.5 mm and the pin bracket by 7 mm.
2. **The carriage isn't retained.** The rail's top slot has to pass the bracket (10.6 mm), which leaves a 0.7 mm lip each side over a 12 mm carriage. That is not a sensible retaining rail.
3. **No room for the cable at the tilt joint.** The cable crosses the rotating joint off-axis and sweeps ±75°. Its zone needs about 8 mm between the lid wall and the bracket; the 5 mm deploy clearance leaves it 2 mm inside the side wall.
4. **One cable can't reach the hinge.** The two staggered rails, 1 mm apart, form a continuous barrier across the whole rail layer. The front-side cassette's cable cannot reach the hinge side, and there is only 3.5 mm under the rail layer beside the display, against the 8 mm the cable needs.

### V1 + minimal fixes (lid stays 31.5 mm; only Y widths and the deploy clearance change)
- Bracket encloses pin and cable side by side: 17 mm. Slot 17.6 mm; carriage 22.6 × 8 (2.5 mm retaining lips); rail envelope 27.6 × 13.
- An 8 mm cable corridor between the staggered rails.
- Deploy clearance 5 → 8 mm, so travel becomes 158 mm, the link 11.5 mm, and the rail 198 mm long.
- **Result:** no slide, stowed or deployed collisions at any lid angle; both cables route to the hinge side; the tilt-joint cable zone clears everything by ≥ 1.0 mm.

### Structure
- **Side wall** (each side): a 202 × 10 mm cassette slot plus a 16.5–19 mm wide notch for the bracket, pin and cable, running from z 6.5 up into the slot.
- **What's left of each side wall:**
  - two 16.5 mm end posts
  - a lower strip z 0–19, cut down to 6.5 mm over the notch
  - nothing above the slot except the 2.5 mm back-plate edge
- **Rail-to-side-wall joint:** almost lost to the notch; 2.5 mm (as specified) or 8.6 mm (fixed) of the rail width remains at the wall.
- **Where the rails can mount instead:**
  - on pads fused down to the bezel frame beside the display (x 117.5–147, about 30 mm long), which is exactly where the deployed carriage carries its load
  - by fusing the left and right rails into one central cross-beam
- **Back plate:** spans the 202 mm cassette bay with no possible internal ribs. A rough beam estimate gives 0.22 mm per N, so it touches the cassettes (1 mm) at about **4.5 N**. **Highly questionable as drawn**; it needs a thicker or externally ribbed plate.
- **Printing:** the cassette bay is a closed 296 × 202 × 10 mm tunnel. Printed as one piece, the lid needs unremovable support or 200 mm bridges. A **two-piece lid** (rear shell with back plate + front frame with bezel and rails) makes each piece printable flat *(inferred)*.

### Display and electronics
- Display 235 × 150 × 5. The rail layer runs **1 mm above the display back over most of the display**, so the display's own board, connector or FPC must fit inside the 5 mm envelope. *(risk: SKU unknown)*
- **Space left in the rail layer (13 mm tall):**
  - as specified: rear zone 296 × 49.5, front zone 296 × 49.5 (the front zone has no route to the hinge)
  - with fixes: 296 × 35.4 in each zone
- **Provisional display-controller keep-out:** the rear-zone remainder, 296 × 35.4 × 13 mm, next to the hinge. This is **not a controller size**; the controller is unknown. A controller taller than 13 mm, or not fitting there, has to go in the base.

### Solar kinematics
- **Travel:** 155 mm required (158 with the fix). A single carriage in its own half of the lid gives only 106.5 mm, so the rails must cross the centreline (by 48–51 mm).
- **Stowed clearances:** cassette to cassette 1.0, cassette to back plate 1.0, cassette to rails 1.0, rails to display 1.0. The rails are 1.0 mm apart as specified, 8.0 mm with the fix.
- **Deployed:** the cassette clears the lid and base by 5 mm (8 mm with the fix).
- **Tilt:**
  - Lid 105° and 135°: every index position from −75° to +75° clears the table; at 135° the minimum is 9–10 mm, at −30…−45°.
  - Lid closed: ±30° is the limit (4–6 mm above the table); ±45° reaches 17–21 mm below it.

### Whole device and hinge
- With the D-006 rear-face hinge and the 31.5 mm lid, the lid clears the base by at least 1.41 mm over the full 0–135° sweep.
- Rear overhang: 93.2 mm at 105°, 189.9 mm at 135°.
- Closed stack height: 73.5 mm (base 40 + gap 2 + lid 31.5).
- Deployed span: 606 mm (612 mm with the fix).

## Model output

```

==================== V1 as specified ====================
lid T 31.5: display z 0-5; rail layer z 6-19; cassette z 20-28; back plate z 29-31.5
rails: R y 118-135, L y 100-117 (gap 1); hub axes y 126.5 / 108.5, z 12.5; carriage 12 x 8; rail env 17 x 13
travel S 155 (deploy clearance 5), link 8.5, rail x -48..147 (length 195; own-half available carriage travel 106.5)
carriage capture: rail top slot 10.6 (bracket 10 + 2x0.3) vs carriage 12 -> retaining lip 0.70 per side
pin + cable side by side: cable y +3.5..+9.5 from axis; exceeds carriage by 3.5, exceeds bracket (with wall) by 7.0  -> DOES NOT FIT
right side wall (y 0-235 x z 0-29, 2.5 thick): cassette slot y 16.5-218.5 x z 19.0-29.0; bracket/pin/cable notch y 120.5-137.0 from z 6.5 up into the slot
   remaining: end posts 16.5 and 16.5 wide (full height); lower strip z 0-19.0 reduced to z 0-6.5 over the notch (16.5 wide); nothing above the slot except the back plate edge (2.5); wall left inside the rail's Y band for a rail-to-wall joint: 2.5 of 17
left side wall (y 0-235 x z 0-29, 2.5 thick): cassette slot y 16.5-218.5 x z 19.0-29.0; bracket/pin/cable notch y 98.0-114.5 from z 6.5 up into the slot
   remaining: end posts 16.5 and 16.5 wide (full height); lower strip z 0-19.0 reduced to z 0-6.5 over the notch (16.5 wide); nothing above the slot except the back plate edge (2.5); wall left inside the rail's Y band for a rail-to-wall joint: 2.5 of 17
back plate: 2.5 thick, clear span 202 across the cassette bay (no internal ribs possible); rough estimate 0.223 mm per N at centre -> touches cassettes (1 mm) at ~4.5 N
service loops (bend R 20, cable 6): LR y 136-182, x -88..147; LL y 53-99
free rail-layer space (height 13): rear zone y 183-232.5 (49.5 x 296); front zone y 2.5-52 (49.5 x 296)
cable routing to hinge side (rail layer): right OK, left BLOCKED; free height under rail layer beside display 3.5 (cable needs 8)
slide/stowed violations: ZL-s15 -2.00, ZL-s16 -2.00, ZL-s17 -2.00, ZL-s19 -2.00, S15-ZR -2.00, S17-ZR -2.00, S19-ZR -2.00, S20-ZR -2.00, ZL-s14 -1.01, S18-ZR -1.01, ZL-s18 -1.00, S16-ZR -1.00, Nt-ZL +0.88, Ns-ZR +0.88
stowed clearances: CL-CR 1.00, CR-Wb 1.00, CR-RR 1.00, CR-RL 1.00, CL-RR 1.00, RL-RR 1.00, D-RL 1.00, D-RR 1.00, QR-RL 4.50, D-QR 2.50, D-KR 3.50
lid   0.0 deployed, tilt: solar min z (! = below table): +0:45 +15:34 -15:34 +30:6 -30:6 +45:-17! -45:-17! +60:-36! -60:-36! +75:-49! -75:-49!
lid 105.0 deployed, tilt: solar min z (! = below table): +0:49 +15:54 -15:49 +30:66 -30:55 +45:82 -45:66 +60:103 -60:82 +75:126 -75:102
lid 135.0 deployed, tilt: solar min z (! = below table): +0:31 +15:48 -15:17 +30:68 -30:10 +45:91 -45:10 +60:63 -60:16 +75:39 -75:29
deployed minimum clearances (all lid angles and tilts, right side): cassette-KR 8.51, cassette-Ns 7.50, cassette-Nt 273.00, cassette-RR 8.50, cassette-Wb 5.00, cassette-base 5.00, cassette-lid side wall 5.00, pin-Ns 7.50, pin-Nt 264.61, pin-Wb 14.00, pin-base 12.00, pin-lid side wall 3.50, hub bracket-Ns 8.05, hub bracket-Nt 273.02, hub bracket-Wb 9.02, hub bracket-base 8.95, hub bracket-lid side wall 5.00, cable run-Ns 7.00, cable run-Nt 224.61, cable run-Wb 13.50, cable run-base 11.50, cable run-lid side wall 1.00, cable twist zone-KR 1.50, cable twist zone-Ns 0.88, cable twist zone-Nt 266.00, cable twist zone-RR 1.50, cable twist zone-Wb 7.22, cable twist zone-base 5.22, cable twist zone-lid side wall -2.00
rear-face hinge with lid 31.5: min lid/base clearance over 0-135 = 1.41 at 135 deg; rear overhang/max height 105: 93.2/266.5, 135: 189.9/204.8; closed stack 73.5

==================== V1 + minimal fixes ====================
lid T 31.5: display z 0-5; rail layer z 6-19; cassette z 20-28; back plate z 29-31.5
rails: R y 121.5-149.1, L y 85.9-113.5 (gap 8); hub axes y 131.8 / 103.2, z 12.5; carriage 22.6 x 8; rail env 27.6 x 13
travel S 158 (deploy clearance 8), link 11.5, rail x -51..147 (length 198; own-half available carriage travel 106.5)
carriage capture: rail top slot 17.6 (bracket 17 + 2x0.3) vs carriage 22.6 -> retaining lip 2.50 per side
pin + cable side by side: cable y +3.5..+9.5 from axis; exceeds carriage by 0.0, exceeds bracket (with wall) by 0.0  -> FITS
right side wall (y 0-235 x z 0-29, 2.5 thick): cassette slot y 16.5-218.5 x z 19.0-29.0; bracket/pin/cable notch y 125.8-144.8 from z 6.5 up into the slot
   remaining: end posts 16.5 and 16.5 wide (full height); lower strip z 0-19.0 reduced to z 0-6.5 over the notch (19.0 wide); nothing above the slot except the back plate edge (2.5); wall left inside the rail's Y band for a rail-to-wall joint: 8.6 of 27.6
left side wall (y 0-235 x z 0-29, 2.5 thick): cassette slot y 16.5-218.5 x z 19.0-29.0; bracket/pin/cable notch y 90.2-109.2 from z 6.5 up into the slot
   remaining: end posts 16.5 and 16.5 wide (full height); lower strip z 0-19.0 reduced to z 0-6.5 over the notch (19.0 wide); nothing above the slot except the back plate edge (2.5); wall left inside the rail's Y band for a rail-to-wall joint: 8.6 of 27.6
back plate: 2.5 thick, clear span 202 across the cassette bay (no internal ribs possible); rough estimate 0.223 mm per N at centre -> touches cassettes (1 mm) at ~4.5 N
service loops (bend R 20, cable 6): LR y 150.1-196.1, x -91..147; LL y 38.9-84.9
free rail-layer space (height 13): rear zone y 197.1-232.5 (35.4 x 296); front zone y 2.5-37.9 (35.4 x 296)
cable routing to hinge side (rail layer): right OK, left OK; free height under rail layer beside display 3.5 (cable needs 8)
slide/stowed violations: none
stowed clearances: CL-CR 1.00, CR-Wb 1.00, CR-RR 1.00, CR-RL 1.00, CL-RR 1.00, RL-RR 8.00, D-RL 1.00, D-RR 1.00, QR-RL 13.30, D-QR 2.50, D-KR 3.50
lid   0.0 deployed, tilt: solar min z (! = below table): +0:45 +15:32 -15:32 +30:4 -30:4 +45:-21! -45:-21! +60:-41! -60:-41! +75:-54! -75:-54!
lid 105.0 deployed, tilt: solar min z (! = below table): +0:49 +15:54 -15:49 +30:64 -30:55 +45:80 -45:65 +60:99 -60:81 +75:118 -75:100
lid 135.0 deployed, tilt: solar min z (! = below table): +0:31 +15:46 -15:16 +30:66 -30:9 +45:86 -45:9 +60:58 -60:14 +75:32 -75:28
deployed minimum clearances (all lid angles and tilts, right side): cassette-KR 11.50, cassette-Ns 10.50, cassette-Nt 276.00, cassette-RR 11.50, cassette-Wb 8.00, cassette-base 8.00, cassette-lid side wall 8.00, pin-Ns 7.50, pin-Nt 264.61, pin-Wb 14.00, pin-base 12.00, pin-lid side wall 3.50, hub bracket-Ns 10.50, hub bracket-Nt 276.00, hub bracket-Wb 8.34, hub bracket-base 8.16, hub bracket-lid side wall 8.00, cable run-Ns 7.00, cable run-Nt 224.61, cable run-Wb 13.50, cable run-base 11.50, cable run-lid side wall 3.00, cable twist zone-KR 4.50, cable twist zone-Ns 3.57, cable twist zone-Nt 269.00, cable twist zone-RR 4.50, cable twist zone-Wb 7.29, cable twist zone-base 5.32, cable twist zone-lid side wall 1.00
rear-face hinge with lid 31.5: min lid/base clearance over 0-135 = 1.41 at 135 deg; rear overhang/max height 105: 93.2/266.5, 135: 189.9/204.8; closed stack 73.5
```
