"""NOMAD Virtual V1 hardware catalogue (data only, standard library, no side effects).

One record per physical item in the Virtual V1 build. It is the single source for the V1 integration model
(CAD/tools/v1_integration.py: envelopes, masses), the power model (prototypes/V1/v1_power.py) and the BOM
(prototypes/V1/v1_bom.py). Created 2026-10-06 (Virtual V1 sprint). Nothing here was bought, weighed or measured.

Evidence labels (as E-POWER-001):
  MFR    manufacturer datasheet / manual / official product page
  MFR-DWG manufacturer drawing ("approximate, for reference")
  3P     third-party (distributor / panel database / reseller); lower weight, conflicts noted
  REPO   existing NOMAD record (already sourced there)
  CALC   arithmetic on labelled inputs
  EST    engineering estimate (never presented as a measurement)
  UNKNOWN not published / not found

Status (docs/v1-requirements.md scheme):
  SELECTED      owner selection already recorded
  CANDIDATE     current V1 candidate (provisional; not bought, not physically verified)
  PROVISIONAL   engineering placeholder chosen to allow progress (generic part, spec given)
  SPEC          custom part defined by a specification (no fake SKU)

BOM classes: BUY (exact catalogue part), FABRICATE (NOMAD makes it), SOURCE_LATER (spec known, supplier/SKU open).
Prices: approximate, as found on the date given; currencies as found; never fixed. EUR conversion in v1_bom.py.
Gate: purchase gate of the staged purchase plan (docs/V1-VIRTUAL-INTEGRATION.md section 18).
"""

SOURCES = {
    "PI-BRIEF": "Raspberry Pi 5 product brief RP-008348-DS (E-POWER-001 S1); mechanical drawing (S22)",
    "PI-DOC": "Raspberry Pi documentation, power supply / fan (E-POWER-001 S2, S3)",
    "PR1": "BerryBase DE, incl. VAT, 2026-10-01 (E-POWER research campaign PR1)",
    "COOLER": "Raspberry Pi Active Cooler product brief (E-POWER-001 S7)",
    "M2HAT": "Raspberry Pi M.2 HAT+ product brief (E-POWER-001 S9)",
    "RPSSD": "Raspberry Pi SSD product brief (E-POWER-001 S10); list price US$45 (512 GB), press coverage 2024",
    "G101": "AUO G101UAN01.0 distributor pages: slw-ele.com/g101uan01-0.html (380 nit, eDP 2-lane, -20..70 C, "
            "WLED 50 000 h, 394 pcs stock, MOQ 1, US$50-200 est., 2026-10-06); andesource.com (-10..60 C operating, "
            "-20..60 C storage); outline 228.22 x 148.32 x 5.35 and 229.9 x 150.5 x 4.15 in two 3P listings. "
            "AUO datasheet not obtained (distributor download exists) - 3P data only",
    "B101": "AUO B101UAN01.7 spec v0.8 (E-POWER research campaign D2): eDP 4-lane, 0.95 W logic max, 2.5 W LED max",
    "BECK": "Beck BTC-mini-eDP datasheet Rev.0 2025-05-20 (E-POWER research campaign C1)",
    "PERIBOARD416": "Perixx PERIBOARD-416 user manual, downloads.perixx.com/manuals/PERIBOARD-416_.pdf (read 2026-10-06)",
    "PERIPAD501II": "Perixx PERIPAD-501 II manual (E-POWER research campaign K1); PERIPAD-501 product page (E-POWER-001 S24)",
    "SFE-GNSS": "SparkFun GNSS Flex pHAT - DAN-F10N GPS-29491 product page (read 2026-10-06): US$74.95, in stock",
    "UBLOX": "u-blox DAN-F10N product page (E-POWER-001 S15)",
    "SUNON": "Sunon MF30100V1-1000U-A99 distributor data (RS 2025392, Future Electronics), read 2026-10-06",
    "SOUTHCO": "Southco E6 constant-torque hinge catalogue e6-ct.en.pdf (read 2026-10-06); RS Online BE "
               "E6-10-216-50 EUR 39.38 excl. VAT, 38 mm long (2026-10-06)",
    "SB261": "prototypes/B1_SB261 (TorqMaster published data + IGES)",
    "P108": "Voltaic P108 product page (E-POWER-001 S20): US$45.00, out of stock, expected back 2026-10-12",
    "NKON": "NKON NL 21700 category, incl. VAT, 2026-10-02 (E-POWER-002 section 13)",
    "M65A": "Molicel INR-21700-M65A datasheet v0.1 (preliminary) (E-POWER-002)",
    "DIGIKEY": "DigiKey qty-1 prices 2026-10-02 (E-POWER-002 section 13)",
    "POLOLU": "Pololu product pages 4091 / 2577 (E-POWER-002 section 13)",
    "TI-EVM": "TI USB-PD-CHG-EVM-01 (BQ25798 + TPS25751), ti.com/tool/USB-PD-CHG-EVM-01; US$149 distributor (2026-10-06)",
    "E002": "docs/E-POWER-002-POWER-ARCHITECTURE.md",
    "D010": "prototypes/P0.1/d010/d010_solar_architecture_phase2.md",
    "INSERTS": "prototypes/B1_SB261 (Ruthex RX-M3x5.7; M2.5 x 4 OD 3.55 inserts)",
}

# fields: id -> dict(
#   name, mfr, sku, qty, role, status, cls (BUY/FABRICATE/SOURCE_LATER), gate,
#   dims (w, d, h) mm and dims_src, mass_g (per unit) and mass_src,
#   elec (text), iface (text), mount (text), temp (text),
#   price (per unit, number or None), cur ("EUR"/"USD"), price_src, avail (text), notes)
HW = {
    # ------------------------------------------------------------------ compute
    "PI5": dict(name="Single-board computer", mfr="Raspberry Pi Ltd", sku="Raspberry Pi 5, 8 GB", qty=1,
                role="compute", status="SELECTED", cls="BUY", gate=3,
                dims=(85.0, 56.0, 17.0), dims_src="MFR-DWG board 85 x 56; height to the USB stack top EST",
                mass_g=46.0, mass_src="EST (not published)",
                elec="5.1 V supply, 5 A recommended; 0.8 A typical active (MFR); 3.2 W idle / 9.8 W stress (3P)",
                iface="2x USB 3.0, 2x USB 2.0, GbE, 2x micro-HDMI, USB-C power, PCIe FPC, 40-pin GPIO, fan JST-SH, J2 power button",
                mount="4x M2.5 on 58 x 49, hole Ø2.7, 3.5 from edges (MFR-DWG)", temp="0..70 C (MFR)",
                price=184.90, cur="EUR", price_src="PR1", avail="in stock (BerryBase)",
                notes="EEPROM PSU_MAX_CURRENT=5000 and POWER_OFF_ON_HALT=1 required (E-POWER-002)"),
    "COOLER": dict(name="Pi 5 Active Cooler", mfr="Raspberry Pi Ltd", sku="Raspberry Pi Active Cooler", qty=1,
                   role="compute cooling", status="CANDIDATE", cls="BUY", gate=3,
                   dims=(63.5, 42.5, 13.7), dims_src="MFR-DWG (interpreted, E-POWER-001 ‡)", mass_g=25.0, mass_src="EST",
                   elec="5 V PWM fan from the Pi fan header; current not published (~0.5 W, 3P-SEC)",
                   iface="4-pin JST-SH", mount="2 push pins into Pi 5 holes", temp="(Pi)",
                   price=5.90, cur="EUR", price_src="PR1", avail="in stock", notes="1.09 CFM, 8000 rpm (MFR)"),
    "M2HAT": dict(name="M.2 HAT+ (Standard)", mfr="Raspberry Pi Ltd", sku="Raspberry Pi M.2 HAT+", qty=1,
                  role="storage adapter", status="CANDIDATE", cls="BUY", gate=3,
                  dims=(65.0, 56.5, 1.6), dims_src="MFR-DWG (interpreted); 16 mm stacking header supplied", mass_g=15.0,
                  mass_src="EST", elec="PCIe 2.0 x1; <= 3 A to the M.2 device", iface="16-pin 0.5 mm FPC, M key 2230/2242",
                  mount="on the 16 mm stacking header + 4 standoffs over the Active Cooler", temp="0..50 C AMBIENT (MFR) - sets the internal-air limit",
                  price=12.50, cur="EUR", price_src="PR1", avail="in stock", notes=""),
    "SSD": dict(name="NVMe SSD 512 GB, M.2 2230", mfr="Raspberry Pi Ltd", sku="Raspberry Pi SSD 512GB", qty=1,
                role="storage", status="CANDIDATE", cls="BUY", gate=3,
                dims=(22.0, 30.0, 2.15), dims_src="MFR-DWG (0.8 PCB + 1.35 components)", mass_g=3.0, mass_src="EST",
                elec="3.3 V; power not published (SN740 reference 0.05 W avg active, <= 4.7 W max)", iface="PCIe Gen3 NVMe 1.4",
                mount="M.2 screw on the HAT+", temp="0..70 C (MFR)", price=45.0, cur="USD", price_src="RPSSD",
                avail="list price; EU stock not checked", notes="2230 preferred (CMP-2)"),
    # ------------------------------------------------------------------ display
    "DISPLAY": dict(name="10.1 in 1920x1200 eDP panel (industrial)", mfr="AUO", sku="G101UAN01.0", qty=1,
                    role="display", status="CANDIDATE", cls="BUY", gate=2,
                    dims=(229.9, 150.5, 5.35), dims_src="3P envelope = max of two listings (228.22 x 148.32 x 5.35; 229.9 x 150.5 x 4.15); "
                    "active 216.81 x 135.50 (AUO 10.1 WUXGA family, 3P)",
                    mass_g=170.0, mass_src="EST (3P quotes ~170 g for related AUO 10.1 WUXGA modules; B101UAN01.7 is 140 g max MFR)",
                    elec="eDP 2-lane; 3.3 V logic; integrated LED driver (family, 3P); POWER UNKNOWN - modelled as B101UAN01.7 "
                         "(0.95 W logic, 2.5 W LED at full) ASSUMED",
                    iface="30-pin eDP (position on the panel back to confirm from the datasheet)",
                    mount="no mounting ears (tablet-class module): retained by the lid bezel lip + back clamp ribs, foam pads",
                    temp="3P conflict: -20..70 C (slw-ele) vs -10..60 C operating / -20..60 C storage (andesource)",
                    price=110.0, cur="USD", price_src="G101", avail="394 pcs at one distributor, MOQ 1 (3P)",
                    notes="380-410 nit (3P). Surface (glare/AG) UNKNOWN: matte film if glossy. Chosen over B101UAN01.7 because "
                          "B101UAN01.7 is eDP 4-lane (outside the BTC-mini-eDP 1-2 lane range) and has 12 000 h LED life, 0..60 C"),
    "DCTRL": dict(name="HDMI -> eDP display controller", mfr="Beck Elektronik", sku="BTC-mini-eDP (STD 12 V)", qty=1,
                  role="display controller", status="CANDIDATE", cls="BUY", gate=2,
                  dims=(80.0, 70.0, 9.8), dims_src="MFR (80 x 70, 9.8 mm total height)", mass_g=33.0, mass_src="MFR",
                  elec="12 V +-5 % (11.4-12.6 V); 1.10 / 1.12 / 1.29 W active, 0.13-0.16 W sleep (MFR)",
                  iface="HDMI 1.4a in; eDP 1-2 lane out; backlight PWM/enable; I2C / DDC-CI brightness",
                  mount="4 holes (pattern from the Beck drawing, TBD) on standoffs, in the base under the keyboard",
                  temp="0..60 C (MFR)", price=None, cur="EUR", price_src="BECK", avail="UNKNOWN - quote required (Nuremberg, DE)",
                  notes="Panel-specific firmware/cable configuration must be confirmed by Beck for G101UAN01.0. "
                        "Fallback: RTD2556-class HDMI->eDP board (reseller data only)"),
    "EDP_CABLE": dict(name="eDP micro-coax cable, 30-pin, ~380 mm, through the display hinge", mfr="(panel/controller-specific)",
                      sku="SPEC: 30-pin I-PEX-class both ends, 2-lane, 380 mm +-20", qty=1, role="display cable",
                      status="SPEC", cls="SOURCE_LATER", gate=2, dims=(12.0, 380.0, 1.2), dims_src="EST", mass_g=12.0,
                      mass_src="EST", elec="eDP 2-lane + panel power + backlight", iface="", mount="taped / clipped in the lid core",
                      temp="", price=20.0, cur="EUR", price_src="EST", avail="Beck or panel distributor", notes=""),
    "HDMI_CABLE": dict(name="micro-HDMI to HDMI flat cable, internal, ~200 mm", mfr="(generic FPV-type kit)",
                       sku="SPEC: micro-HDMI (Type D) right-angle to HDMI (Type A), FPC ribbon, 200 mm", qty=1,
                       role="display signal", status="PROVISIONAL", cls="SOURCE_LATER", gate=2, dims=(15.0, 200.0, 8.0),
                       dims_src="EST", mass_g=15.0, mass_src="EST", elec="HDMI 1.4", iface="", mount="", temp="",
                       price=12.0, cur="EUR", price_src="EST", avail="common", notes=""),
    # ------------------------------------------------------------------ input
    "KEYBOARD": dict(name="Wired mini scissor keyboard, 78 keys (US) / 79 (EU)", mfr="Perixx", sku="PERIBOARD-416", qty=1,
                     role="keyboard", status="CANDIDATE", cls="BUY", gate=2,
                     dims=(285.0, 117.0, 16.0), dims_src="MFR manual 285*117*16 mm", mass_g=332.0, mass_src="MFR manual 332 +-5 g",
                     elec="USB bus-powered; current not published (ASSUMED in v1_power.py)",
                     iface="USB-C receptacle on the keyboard; detachable USB-C->A (1.8 m) and C->C (1.0 m) cables supplied",
                     mount="clamped in the keyboard tray (no screw points published); 4 printed hold-downs",
                     temp="0..40 C operating (MFR manual)", price=35.0, cur="EUR", price_src="EST", avail="Perixx stores (not checked)",
                     notes="Replaces the 280 x 105 x <= 8 target (no wired keyboard found <= 8 mm, E-POWER-001 C4). "
                           "Detachable cable allows a short internal USB-C->A lead"),
    "TRACKPAD": dict(name="USB touchpad", mfr="Perixx", sku="PERIPAD-501 II", qty=1, role="trackpad", status="CANDIDATE",
                     cls="BUY", gate=2, dims=(86.0, 75.0, 13.0), dims_src="MFR manual 86 x 75 x 13 (published, not measured)",
                     mass_g=90.0, mass_src="EST", elec="USB bus-powered; current not published",
                     iface="USB-A fixed cable (~1.6 m on PERIPAD-501): coil the excess in the trackpad bay",
                     mount="clamped in the trackpad tray", temp="UNKNOWN", price=30.0, cur="EUR", price_src="EST",
                     avail="UNKNOWN: not listed on the Perixx stores (E-POWER-001 C5)",
                     notes="If unobtainable, PERIPAD-506 (135 x 116 x 14) needs a base re-layout (+41 mm depth): owner"),
    # ------------------------------------------------------------------ GNSS
    "GNSS": dict(name="GNSS Flex pHAT with DAN-F10N (L1/L5, internal patch)", mfr="SparkFun", sku="GPS-29491", qty=1,
                 role="GNSS", status="CANDIDATE", cls="BUY", gate=3,
                 dims=(65.0, 30.0, 16.0), dims_src="pHAT 65 x 30 (Raspberry Pi pHAT format, EST); module 34 x 44 (MFR page); "
                 "patch 20 x 20 x 8 (MFR page); height EST", mass_g=15.0, mass_src="EST",
                 elec="3.3 V from the GPIO header; 21 mA tracking, 26 mA acquisition, 100 mA inrush (MFR)",
                 iface="UART (GPIO14/15) + PPS + 3V3/GND via a 6-wire harness (not stacked); U.FL; USB-C; Qwiic; microSD",
                 mount="4x M2.5 standoffs (supplied) on the base floor, rear strip",
                 temp="-40..85 C (u-blox module)", price=74.95, cur="USD", price_src="SFE-GNSS", avail="in stock",
                 notes="No GLONASS. Patch needs a non-metallic sky window (rear deck strip). External antenna option via U.FL"),
    # ------------------------------------------------------------------ cooling
    "FAN": dict(name="Axial fan 30 x 30 x 10 mm, 5 V (enclosure exhaust)", mfr="Sunon", sku="MF30100V1-1000U-A99", qty=1,
                role="enclosure cooling", status="CANDIDATE", cls="BUY", gate=3,
                dims=(30.0, 30.0, 10.0), dims_src="MFR (distributor data)", mass_g=8.0, mass_src="EST",
                elec="5 V, 0.6 W rated, 138 mA max (MFR); 2-wire: switched/PWM by a logic FET from a Pi GPIO",
                iface="2-wire lead", mount="2 screws / snap frame on the right side wall", temp="-10..70 C (MFR)",
                price=9.0, cur="EUR", price_src="EST (RS 2025392, price not read)", avail="RS / Future (stock not checked)",
                notes="5.5 CFM free air (MFR); static pressure not read; in-system flow ASSUMED 50 % of free air. A 40 mm fan "
                      "(NF-A4x10) does not fit the 35 mm internal height when wall-mounted"),
    # ------------------------------------------------------------------ hinges / mechanics
    "LID_HINGE": dict(name="Constant-torque hinge, medium, symmetric", mfr="Southco", sku="E6-10-216-50 (1.8 N·m)", qty=2,
                      role="display-lid hinge", status="CANDIDATE", cls="BUY", gate=2,
                      dims=(38.0, 40.0, 10.0), dims_src="MFR catalogue: 38 long; 4x Ø4.5 holes, pattern 28 x 17.8 (transcribed "
                      "from the catalogue drawing text, INFERRED); open width ~40 and barrel Ø10 INFERRED", mass_g=20.0, mass_src="EST",
                      elec="", iface="", mount="4x M4 per hinge (2 per leaf) into M4 heat-set inserts (base corner block, lid hinge band)",
                      temp="UNKNOWN (not on the catalogue page)", price=39.38, cur="EUR", price_src="SOUTHCO",
                      avail="RS Online", notes="Aluminium alloy, black; 20 000 cycles within +-20 % of static torque; "
                      "max static radial load 155 N (MFR). Torque variant set by v1_integration.py hinge check"),
    "LEAF_HINGE": dict(name="Friction hinge (B1 solar leaf)", mfr="TorqMaster", sku="SB-188-SB-261-6", qty=2,
                       role="solar-leaf hinge", status="CANDIDATE", cls="BUY", gate=1, dims=(33.8, 25.4, 7.11),
                       dims_src="REPO (IGES / published)", mass_g=10.0, mass_src="EST", elec="", iface="",
                       mount="F-R-R-F: lid M3 inserts RX-M3x5.7; leaf M2.5 x 4 OD 3.55 inserts (REPO)",
                       temp="UNPUBLISHED", price=15.0, cur="EUR", price_src="EST (TorqMaster quote required)",
                       avail="TorqMaster", notes="SF ~1.16 on torque (REPO) - first physical gate"),
    "STAY": dict(name="Rear outrigger stay arms", mfr="NOMAD", sku="SPEC: 2x stainless 1.4301 flat 3 x 16 x 130, M4 shoulder pivots, detent",
                 qty=1, role="B1 stability", status="SPEC", cls="FABRICATE", gate=1, dims=(16.0, 130.0, 3.0),
                 dims_src="D-010 Phase 2 s.11", mass_g=105.0, mass_src="EST (D010)", elec="", iface="", mount="M4 shoulder screws into "
                 "inserts in the rear corner blocks", temp="", price=12.0, cur="EUR", price_src="EST", avail="", notes="mandatory for B1"),
    # ------------------------------------------------------------------ solar
    "PANEL": dict(name="Solar panel 9.92 W, 18 V, ETFE on FR4", mfr="Voltaic Systems", sku="P108", qty=1, role="solar",
                  status="CANDIDATE", cls="BUY", gate=4, dims=(274.0, 223.0, 4.0), dims_src="MFR", mass_g=328.0, mass_src="MFR",
                  elec="9.92 Wp; Voc 20.45 V; Vmp 17.34 V; Imp 0.57 A (MFR)", iface="3.5 x 1.1 mm plug, 50 cm (re-terminated)",
                  mount="seated in the leaf frame rebate", temp="UNPUBLISHED", price=45.0, cur="USD", price_src="P108",
                  avail="out of stock (expected back 2026-10-12)", notes=""),
    # ------------------------------------------------------------------ battery and power
    "CELL": dict(name="Li-ion 21700 cell", mfr="Molicel", sku="INR-21700-M65A", qty=4, role="battery cells",
                 status="CANDIDATE", cls="BUY", gate=4, dims=(21.55, 21.55, 70.21), dims_src="MFR (preliminary v0.1)",
                 mass_g=74.5, mass_src="MFR max", elec="6.4 Ah, 23.0 Wh min; 26 A continuous; 25 mOhm DC; charge 0-60 C (MFR prelim.)",
                 iface="", mount="in the pack holder", temp="charge 0..60 C", price=9.75, cur="EUR", price_src="NKON",
                 avail="NKON (NL)", notes="Preliminary datasheet. Fallback Samsung 50E (71 Wh pack, 4 h minimum only). "
                 "Buy matched cells + 1 spare when the cell decision is made"),
    "PACK": dict(name="4S1P battery pack assembly", mfr="NOMAD / pack builder",
                 sku="SPEC: 4S1P 21700, holder-type, nickel strip, on-pack protector BMS, NTC, 10 A MINI fuse, Micro-Fit 3.0 lead",
                 qty=1, role="battery pack", status="SPEC", cls="FABRICATE", gate=4, dims=(91.6, 80.0, 28.9),
                 dims_src="CALC E-POWER-002 s.11.1 (holder build with M65A)", mass_g=60.0,
                 mass_src="EST pack hardware only (holder, strip, BMS, wire, insulation); cells counted separately",
                 elec="16.8 / 14.4 / 12.8 V (full / nominal / cutoff); 92 Wh nominal (M65A)", iface="keyed latching P+ P- NTC",
                 mount="in its own bay behind the battery door, foam-preloaded", temp="BMS charge inhibit outside 0..45 C",
                 price=25.0, cur="EUR", price_src="EST (holder, nickel, BMS PCB + parts, fuse + holder, connector)",
                 avail="build or professional pack assembler", notes="Spot-welded by a competent assembler; never soldered to cells"),
    "PWR_PCB": dict(name="Power board: USB-C PD sink + NVDC buck-boost charger + MPPT input + protection", mfr="NOMAD (custom)",
                    sku="SPEC: TI BQ25798RQMR + TPS25751DREFR + USB4105-GF-A + solar input ideal-diode/TVS + I2C header",
                    qty=1, role="charger / power path", status="SPEC", cls="FABRICATE", gate=5, dims=(80.0, 40.0, 12.0),
                    dims_src="EST (E-POWER-002 s.11.2 charger area 35 x 30 + PD + input protection)", mass_g=25.0, mass_src="EST",
                    elec="USB-C PD 20 V 3 A preferred / 45 W min (VAC1); P108 VOC-MPPT (VAC2); charge 3.2 A; 4S",
                    iface="USB-C (left wall), solar in, pack, SYS out, I2C to the Pi, button QON",
                    mount="4x M2.5 on standoffs, under the keyboard (left)", temp="", price=60.0, cur="EUR",
                    price_src="EST: ICs US$5.20 + 2.99 + 0.80 (DIGIKEY) + passives/FETs ~US$25 + 5-pc PCB fab ~EUR 25",
                    avail="", notes="Bench validation on the TI EVM first (gate 4)"),
    "EVM": dict(name="Charger + PD evaluation module (bench validation)", mfr="Texas Instruments", sku="USB-PD-CHG-EVM-01",
                qty=1, role="power validation", status="CANDIDATE", cls="BUY", gate=4, dims=(0, 0, 0), dims_src="not installed",
                mass_g=0.0, mass_src="not installed", elec="BQ25798 + TPS25751, 2-4S", iface="", mount="bench only", temp="",
                price=149.0, cur="USD", price_src="TI-EVM", avail="distributors", notes="Validates PD, MPPT and 4S charging before the custom PCB"),
    "BUCK5": dict(name="5 V 5.5 A step-down regulator (Pi rail)", mfr="Pololu", sku="D36V50F5 (#4091)", qty=1,
                  role="5.1 V rail", status="CANDIDATE", cls="BUY", gate=4, dims=(25.4, 25.4, 9.5), dims_src="MFR",
                  mass_g=8.0, mass_src="EST", elec="5.5-50 V in; 5 V +-4 %, 5.5 A; 80-95 %", iface="solder pads",
                  mount="on the power standoffs (compute-power zone)", temp="", price=39.95, cur="USD", price_src="POLOLU",
                  avail="Pololu", notes="5.0 V nominal vs Pi 5.1 V: verify the drop at 5 A (E-POWER-002 E2-R03)"),
    "BB12": dict(name="12 V buck-boost regulator (display controller rail)", mfr="Pololu", sku="S18V20F12 (#2577)", qty=1,
                 role="12 V rail", status="CANDIDATE", cls="BUY", gate=4, dims=(43.0, 21.0, 10.0), dims_src="MFR", mass_g=7.0,
                 mass_src="EST", elec="2.9-32 V in; 12 V ~2 A; 80-90 %", iface="solder pads", mount="on the power board",
                 temp="", price=29.95, cur="USD", price_src="POLOLU", avail="Pololu", notes=""),
    "BUTTON": dict(name="Momentary panel push-button, 12 mm, sealed", mfr="(generic, IP67 class)",
                   sku="SPEC: 12 mm panel, momentary NO, IP67, 50 mA", qty=1, role="power button", status="PROVISIONAL",
                   cls="SOURCE_LATER", gate=5, dims=(14.0, 25.0, 14.0), dims_src="EST", mass_g=5.0, mass_src="EST",
                   elec="Pi 5 J2 power button + charger QON (ship-mode exit) via diodes", iface="2-wire", mount="left wall",
                   temp="", price=5.0, cur="EUR", price_src="EST", avail="common", notes=""),
    "USB_EXT": dict(name="USB 3.0 A panel-mount extension, 0.3 m", mfr="(generic)", sku="SPEC: USB 3.0 A male to panel-mount A female, 0.3 m",
                    qty=2, role="external USB", status="PROVISIONAL", cls="SOURCE_LATER", gate=5, dims=(20.0, 300.0, 8.0),
                    dims_src="EST", mass_g=15.0, mass_src="EST", elec="", iface="", mount="front-right wall, 2 screws each",
                    temp="", price=7.0, cur="EUR", price_src="EST", avail="common", notes=""),
    # ------------------------------------------------------------------ consumables / mechanical
    "INSERTS": dict(name="Heat-set inserts, screws, M4 hinge inserts, feet", mfr="Ruthex + generic", sku="SPEC: RX-M3x5.7, M2.5x4 OD3.55, M4 inserts, "
                    "M2.5/M3/M4 screws, 4 rubber feet 4 mm", qty=1, role="fasteners", status="PROVISIONAL", cls="SOURCE_LATER",
                    gate=1, dims=(0, 0, 0), dims_src="", mass_g=40.0, mass_src="EST", elec="", iface="", mount="", temp="",
                    price=30.0, cur="EUR", price_src="EST", avail="", notes=""),
    "WIRING": dict(name="Wire, connectors, sleeving, thermal pads, low-e foil tape", mfr="(generic)",
                   sku="SPEC: silicone 18/22 AWG, 2 x 0.5 mm2 solar lead, JST-PH/XH, Micro-Fit 3.0, PET sleeve, foil tape",
                   qty=1, role="harness", status="PROVISIONAL", cls="SOURCE_LATER", gate=5, dims=(0, 0, 0), dims_src="",
                   mass_g=45.0, mass_src="EST", elec="", iface="", mount="", temp="", price=35.0, cur="EUR", price_src="EST",
                   avail="", notes=""),
    "PETG": dict(name="PETG filament (base, lid core, trays)", mfr="(any reputable)", sku="SPEC: PETG 1.75 mm, 1 kg", qty=2,
                 role="printed structure", status="PROVISIONAL", cls="SOURCE_LATER", gate=1, dims=(0, 0, 0), dims_src="",
                 mass_g=0.0, mass_src="counted in the printed parts", elec="", iface="", mount="", temp="", price=25.0,
                 cur="EUR", price_src="EST", avail="", notes="2 kg covers parts + supports + coupons + one reprint (v1_integration print mass)"),
    "ASA": dict(name="ASA filament (sun-exposed: leaf frame, lid back shell)", mfr="(any reputable)", sku="SPEC: ASA 1.75 mm, 1 kg",
                qty=1, role="printed structure", status="PROVISIONAL", cls="SOURCE_LATER", gate=1, dims=(0, 0, 0), dims_src="",
                mass_g=0.0, mass_src="counted in the printed parts", elec="", iface="", mount="", temp="", price=28.0, cur="EUR",
                price_src="EST", avail="", notes=""),
    "PSU27": dict(name="Official 27 W USB-C PSU (bench bring-up only)", mfr="Raspberry Pi Ltd", sku="27W USB-C PSU", qty=1,
                  role="bench", status="CANDIDATE", cls="BUY", gate=3, dims=(0, 0, 0), dims_src="not installed", mass_g=0.0,
                  mass_src="not installed", elec="5.1 V 5 A", iface="", mount="", temp="", price=12.40, cur="EUR",
                  price_src="PR1", avail="in stock", notes="Lets the compute stack be tested before the power system exists"),
}
