# Hardware — NOMAD V1

Component selections and their status. Update this file when a SKU is locked or a part is measured.

The architecture is B1 (D-010). Requirement status by subsystem is in `v1-requirements.md`.

| Component | Candidate / target | Status | Key constraints |
|---|---|---|---|
| Computer | Raspberry Pi 5, 8 GB | selected | ~85 × 56 mm board; needs active cooling |
| NVMe adapter | Raspberry Pi M.2 HAT+ | candidate | Stacks on the Pi |
| SSD | 500–512 GB NVMe, 2230 preferred | not selected | |
| Display | 10.1" IPS 1920×1200 16:10, ≥400 nit, matte, HDMI, non-touch, ≤6 W | not selected | Reserve controller, cable exit, bezel and hinge interface |
| Display hinges | Rear-face hinge direction (D-006, provisional); B1 needs ~1.6 N·m each with a φ-max stop (CALC) | not selected | Shared cable pass with the solar cable |
| Keyboard | Ultra-low-profile wired USB HID, ~280×105 mm, ≤8 mm, no battery/wireless | not selected | |
| Trackpad | Perixx PERIPAD-501 II | candidate | ~86 × 75 × 13 mm; flexible mounting region |
| GNSS | SparkFun GNSS Flex pHAT / DAN-F10N | candidate | External antenna, PPS, Linux support; antenna away from noise |
| Solar panel | Voltaic P108: 273 × 223 × 4, 328 g, 18 V, 9.5–10.9 W (VENDOR) | candidate | Fits the B1 leaf; single US vendor; temperature rating to confirm |
| Solar-leaf hinges | TorqMaster SB-188-SB-261-6, ×2: band -6, 0.96–1.13 N·m, balanced (PUB) | candidate (current selection; physical validation required) | SF ≈ 1.16 vs 0.83 N·m required; load, material and temperature unpublished; coupon in `prototypes/B1_SB261/` |
| Heat-set inserts (B1 hinge rail) | Ruthex RX-M3x5.7 (lid); M2.5 × 4, OD 3.55 (e.g. PartsBuilt PBX-TI-M25-4L35W-4PK) (leaf) | candidate | Standard 4.6-OD M2.5 inserts must not be used at the leaf |
| Stay | 2 stainless flats 3 × 16, M4 shoulder-screw pivots (D-010 Phase 2) | concept | Mandatory for B1; design TBD |
| Power modules | Ready-made DC/DC, battery management, solar charge controller | TBD | |
| Battery | TBD from measured consumption | TBD | Removable, serviceable |
| Fasteners | M2.5, M3 with heat-set inserts | provisional | |
