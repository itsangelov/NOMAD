"""E-POWER-002 power-architecture calculator (virtual engineering, standard library, no side effects).

Reproduces every number in docs/E-POWER-002-POWER-ARCHITECTURE.md.
Run:  py prototypes/V1/epower_architecture_calc.py

Loads are imported from the E-POWER research-campaign calculator (epower_campaign_calc.py), so both stay consistent.
Evidence labels as in the dossier: MFR / 3P / CALC / ASSUMED / UNKNOWN. Key MFR inputs added here:
  TI BQ25798 datasheet SLUSDV2C (rev. June 2026): VBUS 3.6-24 V (VAC/VBUS abs max 30 V), VBAT <= 18.8 V,
    input current <= 3.3 A, charge <= 5 A, battery discharge <= 6 A RMS continuous / 10 A peak (1 s),
    IBAT_OCP 9.3 A, RBATFET 11 mOhm, 96.5 % (16 V battery, 3 A, from 20 V), PROG defaults 4S: 1 A / VSYSMIN 12 V / 16.8 V.
  TI BQ77915 datasheet: 3-5S standalone protector, 50 mA balancing; variant 01: OV 4.25 V, UV 2.8 V,
    OCD1 35 mV, OCD2 60 mV, SCD 120 mV, OCC 20 mV (across Rsense), OTC 50 C, UTC 0 C.
  Molicel INR-21700-M65A v0.1: 23.0 Wh min / 23.4 typ, 74.5 g max, DC impedance 25 mOhm (50 % SOC), charge 0-60 C.
  Littelfuse MINI 0297010.WXNV: 10 A, 32 V DC, 1 kA breaking capacity, 7.42 mOhm cold resistance.
Nothing here selects a part; the baseline is an engineering recommendation for the next phase.
"""
import importlib.util
import math
import os
import sys

sys.dont_write_bytecode = True          # keep the repository free of __pycache__
_here = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("epower_campaign_calc", os.path.join(_here, "epower_campaign_calc.py"))
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)

DA = "D-A AUO B101UAN01 + Beck BTC-mini-eDP"
DW = "D-W Winstar WF101NTYA4LNN0 + Beck BTC-mini + LED driver"


def loads(dkey, scen):
    """(5 V-rail load W, 12 V-rail display load W) for a campaign scenario."""
    wk, duty, cc = C.SCEN[scen]
    v5 = C.PI[wk][0] + C.NVME[wk][0] + C.FAN[wk][0] + C.GNSS[wk][0] + C.HID[wk][0]
    return v5, C.display_w(C.DISPLAY[dkey], duty, cc)


# ------------------------------------------------------------------ cells (MFR)
CELLS = {
    "M65A": dict(name="Molicel INR-21700-M65A (v0.1 preliminary)", wh=23.0, wh_typ=23.4, ah=6.4, m=74.5, d=21.55,
                 l=70.21, dcir=0.025, i_cont=26.0, chg_t=(0, 60)),
    "50E": dict(name="Samsung SDI INR21700-50E", wh=4.9 * 3.63, wh_typ=4.9 * 3.63, ah=4.9, m=69.5, d=21.25, l=70.80,
                dcir=0.025, i_cont=9.8, chg_t=(0, 45)),            # 50E DCIR not extracted: 25 mOhm ASSUMED
}
V_FULL, V_NOM, V_CUT, V_UV = 4.20, 3.60, 3.20, 2.80   # per cell: charge, nominal, system cutoff (ASSUMED), BMS UV (BQ7791501)
USABLE, EOL, RESERVE = C.USABLE, C.EOL, C.RESERVE

# ------------------------------------------------------------------ architectures (4 cells fit the bay; 3S uses 3)
# eta5/eta12: conversion efficiencies ASSUMED inside MFR bands (Pololu D36V50F5 buck 80-95 %, S18V20F12 buck-boost
# 80-90 %, U3V70F12 boost 80-95 %); eta_chg: charger from 20 V PD (BQ25798 96.5 % at 16 V/3 A from 20 V, MFR).
ARCH = {
    "A 1S4P": dict(s=1, p=4, five="boost 3.0-4.2 -> 5.1 V (5 A, ~25 W)", eta5=0.87, twelve="boost -> 12 V", eta12=0.87,
                   eta_chg=0.90, conv=2),
    "B 2S2P": dict(s=2, p=2, five="buck 5.6-8.4 -> 5.1 V (dropout near empty at 5 A)", eta5=0.92, twelve="boost -> 12 V",
                   eta12=0.90, eta_chg=0.93, conv=2),
    "C 3S1P": dict(s=3, p=1, five="buck 9-12.6 -> 5.1 V", eta5=0.91, twelve="buck-boost (9-12.6 straddles 12 V)",
                   eta12=0.87, eta_chg=0.95, conv=2),
    "D 4S1P": dict(s=4, p=1, five="buck 12-16.8 -> 5.1 V", eta5=0.90, twelve="buck-boost (SYS 12-16.8 V)", eta12=0.88,
                   eta_chg=0.965, conv=2),
}
R_PATH = 0.011 + 0.0074 + 0.010 + 0.003 + 0.010   # BATFET + MINI fuse + 2 protection FETs + Rsense + wiring/connector (ASSUMED except BATFET, fuse MFR)
P_Q = 0.06                                       # W: regulators 2-4 mA + ~1 mA at the bus, charger 17 uA, BMS 8 uA (MFR, at ~14 V)
BQ_CONT, BQ_PEAK, BQ_OCP, BQ_VBAT = 6.0, 10.0, 9.3, 18.8


def pack_r(a, cell):
    return a["s"] * cell["dcir"] / a["p"]


def batt_power(a, v5, v12):
    return v5 / a["eta5"] + v12 / a["eta12"] + P_Q


def batt_current(a, cell, p_b, v_cell):
    """Battery current incl. I2R in the pack and path (solve P = V*I - I^2*R by fixed-point)."""
    v = a["s"] * v_cell
    r = pack_r(a, cell) + R_PATH
    i = p_b / v
    for _ in range(20):
        i = p_b / (v - i * r)
    return i, i * i * r


def fmt(x, n=2):
    return f"{x:.{n}f}"


def main():
    cell = CELLS["M65A"]
    print("# E-POWER-002 architecture calculator output\n")
    print(f"Per-cell voltages: full {V_FULL}, nominal {V_NOM}, system cutoff {V_CUT} (ASSUMED), BMS UV {V_UV} (BQ7791501). "
          f"Path resistance {R_PATH * 1000:.1f} mOhm, quiescent {P_Q} W. Usable {USABLE}, EOL {EOL}, reserve {RESERVE}.\n")

    # -------------------------------------------------- 1. architecture comparison
    print("## 1. Architecture comparison (M65A cells; loads from the campaign calculator)\n")
    print("| Arch | cells | V full / nom / cutoff / BMS-UV | nominal Wh | usable new / EOL Wh | 5 V stage | 12 V stage | "
          "P_batt NORMAL D-A / WORST D-W (W) | I_batt NORMAL D-A @nom (A) | I_batt WORST D-W @cutoff / @BMS-UV (A) | vs BQ25798 6 A cont / 10 A peak | heat NORMAL D-A / WORST D-W @cutoff (W) |")
    print("|---|---:|---|---:|---|---|---|---|---:|---:|---|---|")
    rows = {}
    for k, a in ARCH.items():
        n = a["s"] * a["p"]
        e_nom = n * cell["wh"]
        v5n, v12n = loads(DA, "NORMAL")
        v5w, v12w = loads(DW, "WORST")
        pbn, pbw = batt_power(a, v5n, v12n), batt_power(a, v5w, v12w)
        i_n, loss_n = batt_current(a, cell, pbn, V_NOM)
        i_c, loss_c = batt_current(a, cell, pbw, V_CUT)
        i_w, loss_w = batt_current(a, cell, pbw, V_UV)
        heat_n = (pbn - v5n - v12n) + loss_n
        heat_w = (pbw - v5w - v12w) + loss_c
        ok = "OK" if i_w <= BQ_CONT else ("exceeds 6 A continuous" + (" and OCP 9.3 A" if i_c > BQ_OCP else "") +
                                          (" (at cutoff too)" if i_c > BQ_CONT else ""))
        rows[k] = dict(n=n, e=e_nom, i_n=i_n, i_w=i_w, heat_n=heat_n, heat_w=heat_w, pbn=pbn, pbw=pbw)
        print(f"| {k} | {n} | {a['s'] * V_FULL:.1f} / {a['s'] * V_NOM:.1f} / {a['s'] * V_CUT:.1f} / {a['s'] * V_UV:.1f} | "
              f"{e_nom:.1f} | {e_nom * USABLE:.1f} / {e_nom * USABLE * EOL:.1f} | {a['five']} ({a['eta5']}) | "
              f"{a['twelve']} ({a['eta12']}) | {pbn:.2f} / {pbw:.2f} | {i_n:.2f} | {i_c:.2f} / {i_w:.2f} | {ok} | {heat_n:.2f} / {heat_w:.2f} |")
    print("\nHIGH D-W (22.1 W) at 3.0 V/cell, 1S: " + f"{22.1 / 3.0:.1f} A (> 6 A continuous)")

    # -------------------------------------------------- 2. baseline pack
    a = ARCH["D 4S1P"]
    print("\n## 2. Baseline pack: 4S1P 21700\n")
    print("| Item | M65A (preliminary) | 50E (mature) |")
    print("|---|---|---|")
    for label, f in [
        ("cells / arrangement", lambda c: "4 / 4S1P"),
        ("V full / nominal / cutoff / BMS-UV", lambda c: f"{4 * V_FULL:.1f} / {4 * V_NOM:.1f} / {4 * V_CUT:.1f} / {4 * V_UV:.1f} V"),
        ("nominal Wh (rated min / typ)", lambda c: f"{4 * c['wh']:.1f} / {4 * c['wh_typ']:.1f}"),
        ("usable Wh new (x0.90)", lambda c: f"{4 * c['wh'] * USABLE:.1f}"),
        ("usable Wh end of life (x0.80)", lambda c: f"{4 * c['wh'] * USABLE * EOL:.1f}"),
        ("cell mass / pack mass est. (x1.20)", lambda c: f"{4 * c['m']:.0f} g / {4 * c['m'] * C.PACK_MASS:.0f} g"),
        ("pack DC resistance (cells)", lambda c: f"{4 * c['dcir'] * 1000:.0f} mOhm"),
        ("cell continuous limit", lambda c: f"{c['i_cont']} A"),
        ("cell charge window", lambda c: f"{c['chg_t'][0]}-{c['chg_t'][1]} C"),
    ]:
        print(f"| {label} | {f(CELLS['M65A'])} | {f(CELLS['50E'])} |")
    # prospective short circuit
    r_sc = 4 * cell["dcir"] + R_PATH
    print(f"\nProspective pack short-circuit current (DC impedance + path, CALC): {4 * 4.2 / r_sc:.0f} A at full charge "
          f"(MINI fuse breaking capacity 1 kA MFR; NANO2 0451 only 50 A)")

    # -------------------------------------------------- 3. runtime
    print("\n## 3. Runtime model (baseline D 4S1P)\n")
    print("| Display | Case | load W (5 V + 12 V) | battery-side W | conversion + path loss W | energy needed Wh | "
          "usable new / EOL (M65A) | runtime new / EOL (M65A) h | usable new / EOL (50E) | runtime new / EOL (50E) h | meets? (EOL, +10 % reserve, M65A / 50E) |")
    print("|---|---|---:|---:|---:|---:|---|---|---|---|---|")
    for dk in (DA, DW):
        for scen, hrs in (("NORMAL", 4), ("NORMAL", 6), ("NORMAL", 8), ("HIGH", 0.25), ("HIGH", 1), ("HIGH", 4),
                          ("WORST", 0.25), ("WORST", 1)):
            v5, v12 = loads(dk, scen)
            pb = batt_power(a, v5, v12)
            _, loss = batt_current(a, cell, pb, V_NOM)
            pb_total = pb + loss
            need = pb_total * hrs
            res = []
            for ck in ("M65A", "50E"):
                c = CELLS[ck]
                un, ue = 4 * c["wh"] * USABLE, 4 * c["wh"] * USABLE * EOL
                res.append((un, ue, un / pb_total, ue / pb_total, ue >= need * (1 + RESERVE)))
            tag = {"NORMAL": "normal", "HIGH": "high sustained", "WORST": "worst"}[scen]
            hh = f"{hrs:g} h" if hrs >= 1 else f"{hrs * 60:.0f} min"
            print(f"| {dk[:3]} | {tag} {hh} | {v5 + v12:.2f} | {pb_total:.2f} | {pb_total - v5 - v12:.2f} | {need:.1f} | "
                  f"{res[0][0]:.1f} / {res[0][1]:.1f} | {res[0][2]:.1f} / {res[0][3]:.1f} | {res[1][0]:.1f} / {res[1][1]:.1f} | "
                  f"{res[1][2]:.1f} / {res[1][3]:.1f} | {'yes' if res[0][4] else 'no'} / {'yes' if res[1][4] else 'no'} |")

    # -------------------------------------------------- 4. USB-C PD sizing
    print("\n## 4. USB-C PD input sizing (BQ25798: input <= 3.3 A, charge <= 5 A; charge target 3.2 A ~0.5C ASSUMED)\n")
    print("| PD contract | usable input W (I <= 3.3 A) | after charger (x0.965) | charge W while NORMAL D-A | charge W while WORST D-W | "
          "charge current @15.5 V (NORMAL) | time 0->90 % usable (CC, NORMAL running) |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    full = 4 * cell["wh"] * USABLE
    p_norm = batt_power(a, *loads(DA, "NORMAL"))
    p_worst = batt_power(a, *loads(DW, "WORST"))
    for name, v, i in (("15 V 3 A (45 W)", 15, 3.0), ("20 V 2.25 A (45 W)", 20, 2.25), ("20 V 3 A (60 W)", 20, 3.0),
                       ("20 V 3.25 A (65 W)", 20, 3.25), ("20 V 5 A (100 W, e-marked cable)", 20, 5.0)):
        pin = v * min(i, 3.3)
        pout = pin * 0.965
        cn = pout - p_norm
        cw = pout - p_worst
        ich = min(cn / 15.5, 3.2)
        print(f"| {name} | {pin:.1f} | {pout:.1f} | {cn:.1f} | {cw:.1f} | {ich:.2f} A | "
              f"{full * 0.9 / (ich * 15.5):.1f} h |")
    print("\nCharge at 5 V 3 A (non-PD Type-C / fallback): 15 W input -> "
          f"{15 * 0.90 - p_norm:.1f} W left for charging while NORMAL (eta 0.90 ASSUMED at 5 V in).")

    # -------------------------------------------------- 5. solar
    print("\n## 5. P108 on the charger input\n")
    voc, vmp, imp = 20.45, 17.34, 0.570
    kv = -0.0030    # ASSUMED Voc temperature coefficient per K (typical c-Si; Voltaic does not publish)
    for t in (-20, 0, 25, 45, 65):
        print(f"  cell temp {t:>4} C: Voc ~{voc * (1 + kv * (t - 25)):.1f} V")
    print(f"  Vmp/Voc at STC = {vmp / voc:.3f} -> BQ25798 VOC_PCT 0.8125 ({0.8125 * voc:.1f} V) or 0.875 ({0.875 * voc:.1f} V)")
    print(f"  Vmp hot (65 C, scaled from Voltaic 6 V panel data, INFERRED) ~{vmp * 5.3 / 5.71:.1f} V vs 4S full 16.8 V -> "
          "buck-boost needed near full charge")
    print(f"  Max solar input current {imp:.2f} A (Imp) -> reverse-polarity Schottky loss ~{0.4 * imp:.2f} W; ideal-diode FET ~0.01 W")
    print("  VAC OVP setting 00 = 26 V (MFR, min 25.2 V) > Voc cold ~23 V; abs max 30 V")

    # -------------------------------------------------- 6. heat per converter
    print("\n## 6. Power-electronics heat (baseline D 4S1P, D-A unless stated)\n")
    print("| State | 5 V buck in/out/heat | 12 V buck-boost in/out/heat | charger in/out/heat | pack + path I2R | total PE + pack heat |")
    print("|---|---|---|---|---:|---:|")

    def state(label, dk, scen, chg_in=0.0):
        v5, v12 = loads(dk, scen)
        p5i, p12i = v5 / a["eta5"], v12 / a["eta12"]
        h5, h12 = p5i - v5, p12i - v12
        if chg_in:
            out = chg_in * a["eta_chg"]
            hc = chg_in - out
            ichg = max(0.0, (out - (p5i + p12i)) / 15.5)
            i2r = ichg ** 2 * (4 * cell["dcir"] + R_PATH)
            chg = f"{chg_in:.1f} / {out:.1f} / {hc:.2f}"
        else:
            hc = 0.0
            _, i2r = batt_current(a, cell, p5i + p12i + P_Q, V_NOM)
            chg = "- / - / 0"
        print(f"| {label} | {p5i:.2f} / {v5:.2f} / {h5:.2f} | {p12i:.2f} / {v12:.2f} / {h12:.2f} | {chg} | {i2r:.2f} | "
              f"{h5 + h12 + hc + i2r + P_Q:.2f} |")

    state("NORMAL (D-A)", DA, "NORMAL")
    state("NORMAL (D-W)", DW, "NORMAL")
    state("HIGH (D-A)", DA, "HIGH")
    state("WORST (D-W)", DW, "WORST")
    state("NORMAL + charging, 60 W PD (D-A)", DA, "NORMAL", 60.0)
    state("NORMAL + charging, 45 W PD (D-A)", DA, "NORMAL", 45.0)
    state("WORST + charging, 60 W PD (D-W)", DW, "WORST", 60.0)

    # -------------------------------------------------- 7. physical fit
    print("\n## 7. Physical fit (ASSUMED build allowances)\n")
    bay = C.BAY
    for ck in ("M65A", "50E"):
        c = CELLS[ck]
        tight = (4 * c["d"] + 2 * 0.6, c["l"] + 2 * 1.7 + 4.0, c["d"] + 2 * 0.6 + 5.0)
        holder = (4 * c["d"] + 3 * 1.0 + 2 * 1.2, c["l"] + 2 * 1.7 + 4.0 + 2 * 1.2, c["d"] + 2 * 1.2 + 5.0)
        for lab, dims in (("tight build (cells bonded, wraps + fish paper, BMS on top)", tight),
                          ("holder build (1.0 mm ribs, 1.2 mm walls)", holder)):
            spare = [bay[i] - dims[i] for i in range(3)]
            verdict = "fits" if min(spare) >= 4.0 else ("tight (fits, < 2 mm per side somewhere)" if min(spare) >= 0 else "does NOT fit")
            print(f"  {ck} {lab}: {dims[0]:.1f} x {dims[1]:.1f} x {dims[2]:.1f} mm vs bay {bay[0]:.0f} x {bay[1]:.0f} x {bay[2]:.0f} "
                  f"-> spare {spare[0]:+.1f} / {spare[1]:+.1f} / {spare[2]:+.1f} mm: {verdict}")
            if min(spare) < 2.0:
                need = [max(bay[i], dims[i] + 2.0) for i in range(3)]
                print(f"      bay needed for >= 1 mm clearance per side: {need[0]:.1f} x {need[1]:.1f} x {need[2]:.1f} mm")
    pe = [("charger board (BQ25798 + inductor + 2 back-to-back FET pairs + caps), EST", 35, 30, 7),
          ("12 V buck-boost (Pololu S18V20F12 MFR size)", 43, 21, 10),
          ("MINI blade fuse holder (PCB), EST", 20, 10, 12),
          ("solar input protection (ideal-diode FET + TVS) + connector landing, EST", 20, 15, 8),
          ("harness landing / test points, EST", 15, 15, 8)]
    area = sum(w * d for _, w, d, _ in pe)
    print(f"\n  Power-electronics reserve 90 x 45 x 20 = {90 * 45} mm2 floor area:")
    for n_, w, d, h in pe:
        print(f"    {n_}: {w} x {d} x {h} mm = {w * d} mm2")
    print(f"    total ~{area} mm2 = {area / (90 * 45) * 100:.0f} % of the floor; tallest {max(h for *_, h in pe)} mm <= 20 mm")
    print("  Not in this reserve: 5 V buck (Pololu D36V50F5 25.4 x 25.4 x 9.5) -> COMPUTE_POWER reserve 50 x 30 x 15; "
          "BMS on the pack; PD sink (TPS25751, 6 x 4 mm) beside the USB-C receptacle on the rear port panel.")

    # -------------------------------------------------- 8. planning cost
    print("\n## 8. Planning-level cost (one unit, 2026-10-02, USD unless noted; see document for links)\n")
    bom = [("4 x Molicel M65A (NKON, incl. VAT)", 4 * 9.75 * 1.17, "EUR 9.75 each ~ USD (x1.17 ASSUMED FX)"),
           ("BQ25798RQMR (DigiKey)", 5.20, ""), ("TPS25751DREFR (DigiKey)", 2.99, ""), ("BQ7791501PWR (DigiKey)", 2.05, ""),
           ("Littelfuse 0297010.WXNV MINI 10 A (DigiKey)", 0.39, "+ holder (EST USD 1-3)"),
           ("GCT USB4105-GF-A USB-C receptacle (DigiKey)", 0.80, "current rating to verify"),
           ("Molex Micro-Fit 3.0 2-pos housing 0436450200 (DigiKey)", 0.39, "+ contacts/header (EST USD 2)"),
           ("Pololu D36V50F5 5 V 5.5 A (pololu.com)", 39.95, ""), ("Pololu S18V20F12 12 V (pololu.com)", 29.95, ""),
           ("passives, FETs, inductor, NTC, PCB, nickel strip, insulation, wire (EST)", 40.0, "EST, not sourced")]
    tot = 0.0
    for n_, p, note in bom:
        tot += p
        print(f"  {n_}: {p:.2f} {note}")
    print(f"  TOTAL (planning, excl. P108 and shipping/VAT on US items): ~USD {tot:.0f}")


if __name__ == "__main__":
    main()
