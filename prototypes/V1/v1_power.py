"""NOMAD Virtual V1 power, battery, solar and energy model (standard library, no side effects).

Run:  py prototypes/V1/v1_power.py            print the V1 power report (docs/V1-VIRTUAL-INTEGRATION.md s.3-6)
Import: states(), pack(), runtime(), daily(), heat_split() are used by CAD/tools/v1_integration.py (thermal).

What is new versus E-POWER-002 (whose calculators are imported unchanged, so nothing is duplicated):
  - V1 hardware (prototypes/V1/v1_hardware.py): display G101UAN01.0 (power modelled as the D-A AUO family, ASSUMED),
    controller in the BASE, Sunon 30 mm enclosure fan on the 5.1 V rail (not through the Pi USB budget).
  - Heat split base / lid for the thermal model.
  - Representative-day energy and solar balance.
Labels: MFR / 3P / CALC / ASSUMED / UNKNOWN as in the E-POWER dossiers. Nothing here is measured.
"""
import importlib.util
import os
import sys

sys.dont_write_bytecode = True
_here = os.path.dirname(os.path.abspath(__file__))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(_here, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


C = _load("epower_campaign_calc")        # loads, PV yields (E-POWER research campaign)
A = _load("epower_architecture_calc")    # 4S1P architecture, cells, efficiencies (E-POWER-002)
HW = _load("v1_hardware").HW

DKEY = A.DA                               # AUO eDP family + Beck BTC-mini-eDP (G101UAN01.0 power = B101UAN01.7, ASSUMED)
ARCH = A.ARCH["D 4S1P"]                   # baseline (E-POWER-002)

# Enclosure fan (Sunon MF30100V1, 0.6 W rated at 5 V, MFR); duty by state ASSUMED (thermostatic, GPIO PWM/switch)
# speed fraction by state ASSUMED (thermostatic on internal air); power = max(0.05, 0.6 W x speed^3) (fan laws, ASSUMED)
FAN_SPEED = {"LOW": 0.35, "NORMAL": 0.50, "HIGH": 1.0, "WORST": 1.0}
ENC_FAN = {"idle": (0.05, "ASSUMED 35 % speed: 0.6 W MFR x 0.35^3, min 0.05 W electronics"),
           "normal": (0.08, "ASSUMED 50 % speed: 0.6 W MFR x 0.5^3"),
           "high": (0.60, "MFR rated 0.6 W at 100 %"), "worst": (0.60, "MFR rated")}
OFF_W = 0.01 / ARCH["eta5"] + A.P_Q       # Pi halted with POWER_OFF_ON_HALT=1 (0.01 W MFR) + regulator/charger/BMS quiescent; 12 V rail disabled


def states():
    """Per state: 5 V rail W, 12 V rail W, controller W (part of 12 V), battery-side W, I2R W, currents (M65A pack)."""
    out = {}
    cell = A.CELLS["M65A"]
    for s, (wk, duty, cc) in C.SCEN.items():
        v5_items = {"Pi 5": C.PI[wk][0], "NVMe": C.NVME[wk][0], "Active Cooler": C.FAN[wk][0], "GNSS": C.GNSS[wk][0],
                    "keyboard + trackpad": C.HID[wk][0], "enclosure fan": ENC_FAN[wk][0]}
        d = C.DISPLAY[DKEY]
        disp_panel = d["logic"] + d["bl_full"] * duty
        ctrl = d["ctrl_typ"] if cc == "typ" else d["ctrl_max"]
        v5 = sum(v5_items.values())
        v12 = disp_panel + ctrl
        pb = A.batt_power(ARCH, v5, v12)
        i_nom, i2r = A.batt_current(ARCH, cell, pb, A.V_NOM)
        i_cut, _ = A.batt_current(ARCH, cell, pb, A.V_CUT)
        out[s] = dict(v5_items=v5_items, v5=v5, panel=disp_panel, ctrl=ctrl, v12=v12, load=v5 + v12, pb=pb, i2r=i2r,
                      total=pb + i2r, i_nom=i_nom, i_cut=i_cut,
                      conv5=v5 / ARCH["eta5"] - v5, conv12=v12 / ARCH["eta12"] - v12)
    return out


def pack(cell_key="M65A"):
    c = A.CELLS[cell_key]
    e = 4 * c["wh"]
    return dict(cell=c["name"], nominal=e, usable=e * A.USABLE, eol=e * A.USABLE * A.EOL, mass_cells=4 * c["m"],
                v=(4 * A.V_FULL, 4 * A.V_NOM, 4 * A.V_CUT, 4 * A.V_UV))


def runtime(state, cell_key="M65A"):
    st, p = states()[state], pack(cell_key)
    return p["usable"] / st["total"], p["eol"] / st["total"]


def meets(state, hours, cell_key="M65A"):
    st, p = states()[state], pack(cell_key)
    return p["eol"] >= st["total"] * hours * (1 + A.RESERVE)


DAY = [("NORMAL", 6.0), ("HIGH", 1.0)]    # ASSUMED representative field day; remainder of 24 h is OFF


def daily(profile=DAY):
    st = states()
    on_h = sum(h for _, h in profile)
    wh = sum(st[s]["total"] * h for s, h in profile) + OFF_W * (24 - on_h)
    return wh, on_h


def heat_split(state, charging_w=0.0):
    """Heat (W) by zone. Controller and all converters are in the base (V1 layout); only the panel heats the lid.
    charging_w: input power while charging (adds charger loss + pack I2R at 3.2 A, E-POWER-002 s.10 method)."""
    st = states()[state]
    base = st["v5"] + st["ctrl"] + st["conv5"] + st["conv12"] + st["i2r"] + A.P_Q
    lid = st["panel"]
    chg = 0.0
    if charging_w:
        p_in = charging_w
        to_batt = p_in * ARCH["eta_chg"] - st["pb"]           # NVDC: load first, remainder charges
        i_chg = min(3.2, max(0.0, to_batt) / (4 * A.V_NOM))
        r = A.pack_r(ARCH, A.CELLS["M65A"]) + A.R_PATH
        chg = p_in * (1 - ARCH["eta_chg"]) + i_chg ** 2 * r
    zones = {
        "compute bay (Pi stack, Active Cooler, enclosure fan)": st["v5_items"]["Pi 5"] + st["v5_items"]["NVMe"]
        + st["v5_items"]["Active Cooler"] + st["v5_items"]["enclosure fan"],
        "under-keyboard (controller, 5 V buck, 12 V reg, GNSS, HID share)": st["ctrl"] + st["conv5"] + st["conv12"]
        + st["v5_items"]["GNSS"] + st["v5_items"]["keyboard + trackpad"],
        "power board + pack (I2R, quiescent, charging)": st["i2r"] + A.P_Q + chg,
    }
    return dict(base=base + chg, lid=lid, zones=zones, charging=chg)


SOLAR_BEST_HOUR = 10.84    # W, PVGIS best single hour 2018-2023 at 35 deg (E-POWER research campaign s.11)


def solar_table():
    need_normal_day = states()["NORMAL"]["total"] * 6.0
    day_wh, _ = daily()
    rows = []
    for k, v in C.PV.items():
        into = v * C.ETA_SOLAR
        rows.append((k, v, into, into / need_normal_day, into / day_wh))
    return rows, need_normal_day, day_wh


def main():
    st = states()
    print("# NOMAD Virtual V1 power model (v1_power.py)\n")
    print(f"Display: {HW['DISPLAY']['mfr']} {HW['DISPLAY']['sku']} + {HW['DCTRL']['mfr']} {HW['DCTRL']['sku']} "
          f"(power = AUO B101UAN01.7 MFR values, ASSUMED for G101UAN01.0). Architecture {ARCH['s']}S{ARCH['p']}P, "
          f"eta5 {ARCH['eta5']}, eta12 {ARCH['eta12']}, quiescent {A.P_Q} W, path {A.R_PATH * 1000:.1f} mOhm.\n")
    print("## Power budget by state (W; CALC from MFR / 3P / ASSUMED inputs)\n")
    print("| Load | rail | LOW | NORMAL | HIGH | WORST | source |")
    print("|---|---|---:|---:|---:|---:|---|")
    keys = list(st["LOW"]["v5_items"])
    srcs = {"Pi 5": C.PI, "NVMe": C.NVME, "Active Cooler": C.FAN, "GNSS": C.GNSS, "keyboard + trackpad": C.HID,
            "enclosure fan": ENC_FAN}
    for k in keys:
        print(f"| {k} | 5.1 V | " + " | ".join(f"{st[s]['v5_items'][k]:.2f}" for s in st) + f" | {srcs[k]['normal'][1]} |")
    print("| display panel (logic + LED, PWM 25/50/100/100 %) | 12 V | " + " | ".join(f"{st[s]['panel']:.2f}" for s in st)
          + " | AUO B101UAN01.7 MFR (proxy, ASSUMED) |")
    print("| display controller | 12 V | " + " | ".join(f"{st[s]['ctrl']:.2f}" for s in st) + " | Beck MFR typ / max |")
    print("| **load total** | | " + " | ".join(f"**{st[s]['load']:.2f}**" for s in st) + " | |")
    print("| 5 V conversion loss | | " + " | ".join(f"{st[s]['conv5']:.2f}" for s in st) + " | eta 0.90 ASSUMED |")
    print("| 12 V conversion loss | | " + " | ".join(f"{st[s]['conv12']:.2f}" for s in st) + " | eta 0.88 ASSUMED |")
    print("| quiescent | | " + " | ".join(f"{A.P_Q:.2f}" for _ in st) + " | MFR-based |")
    print("| pack + path I2R (nominal V) | | " + " | ".join(f"{st[s]['i2r']:.2f}" for s in st) + " | CALC |")
    print("| **at the battery** | | " + " | ".join(f"**{st[s]['total']:.2f}**" for s in st) + " | CALC |")
    print("| battery current at nominal / cutoff (A) | | " + " | ".join(f"{st[s]['i_nom']:.2f} / {st[s]['i_cut']:.2f}" for s in st)
          + " | CALC (BQ25798 6 A continuous) |")
    print(f"\nOff (halted, POWER_OFF_ON_HALT=1, 12 V rail disabled): {OFF_W:.3f} W at the battery (CALC)\n")

    print("## Battery and runtime (4S1P, usable x0.90, end of life x0.80; 'meets' = EOL >= need x 1.10)\n")
    print("| Cell | nominal Wh | usable new / EOL Wh | cells g | NORMAL new / EOL h | HIGH new / EOL h | WORST new / EOL h | 6 h NORMAL | 4 h NORMAL |")
    print("|---|---:|---|---:|---|---|---|---|---|")
    for ck in ("M65A", "50E"):
        p = pack(ck)
        rn, rh, rw = runtime("NORMAL", ck), runtime("HIGH", ck), runtime("WORST", ck)
        print(f"| {p['cell']} | {p['nominal']:.1f} | {p['usable']:.1f} / {p['eol']:.1f} | {p['mass_cells']:.0f} | "
              f"{rn[0]:.1f} / {rn[1]:.1f} | {rh[0]:.1f} / {rh[1]:.1f} | {rw[0]:.1f} / {rw[1]:.1f} | "
              f"{'meets' if meets('NORMAL', 6, ck) else 'NOT met'} | {'meets' if meets('NORMAL', 4, ck) else 'NOT met'} |")
    p = pack()
    need6 = st["NORMAL"]["total"] * 6 * (1 + A.RESERVE)
    print(f"\nNORMAL 6 h with 10 % reserve needs {need6:.1f} Wh at end of life; M65A gives {p['eol']:.1f} Wh "
          f"(margin {p['eol'] - need6:+.1f} Wh, {100 * (p['eol'] / need6 - 1):+.0f} %). Conversion + I2R share at NORMAL: "
          f"{100 * (st['NORMAL']['total'] - st['NORMAL']['load']) / st['NORMAL']['total']:.1f} % of battery energy.")
    print(f"Fragility (audit 2026-10-06): the 6 h target fails if the NORMAL load at the battery exceeds "
          f"{p['eol'] / 6.6:.2f} W, i.e. only {p['eol'] / 6.6 - st['NORMAL']['total']:.2f} W above this model "
          "(Pi 'typical' 4.0 W and display at 50 % PWM are the weak inputs; measure at the compute gate).\n")

    wh, on_h = daily()
    print("## Representative day (ASSUMED profile: 6 h NORMAL + 1 h HIGH, rest off)\n")
    print(f"Daily energy at the battery: **{wh:.1f} Wh** ({on_h:.0f} h on). M65A pack (new / EOL usable "
          f"{p['usable']:.1f} / {p['eol']:.1f} Wh) = {p['usable'] / wh:.2f} / {p['eol'] / wh:.2f} such days without charging.\n")

    rows, need_n, day = solar_table()
    print("## Solar (P108, Sofia, PVGIS 5.3, charge chain 0.85 ASSUMED; E-POWER campaign data, not re-run)\n")
    print("| Condition | panel Wh/day | into battery Wh/day | share of a 6 h NORMAL day | share of the representative day |")
    print("|---|---:|---:|---:|---:|")
    for k, v, into, f1, f2 in rows:
        print(f"| {k} | {v:.1f} | {into:.1f} | {100 * f1:.0f} % | {100 * f2:.0f} % |")
    best = SOLAR_BEST_HOUR * C.ETA_SOLAR
    print(f"\nSimultaneous operation: best single hour {SOLAR_BEST_HOUR} W at the panel -> {best:.1f} W into the system vs "
          f"NORMAL {st['NORMAL']['total']:.1f} W at the battery: solar can at best roughly match NORMAL load for short "
          f"midday periods (CALC); on average it replenishes, it never carries HIGH ({st['HIGH']['total']:.1f} W). "
          "The NVDC charger supplies the system first and charges with any remainder.\n")

    print("## Charging from USB-C PD (E-POWER-002 method)\n")
    for pin in (45.0, 60.0):
        p_av = pin * ARCH["eta_chg"] - st["NORMAL"]["pb"]
        i = min(3.2, p_av / (4 * A.V_NOM))
        print(f"- {pin:.0f} W contract while NORMAL: {p_av:.1f} W available to charge -> {i:.2f} A; "
              f"0 -> 90 % usable (CC only) ~{p['usable'] / (i * 4 * A.V_NOM):.1f} h")
    print()
    print("## Heat by zone (W, CALC; all electrical input becomes heat)\n")
    print("| State | base total | lid (panel) | compute bay | under-keyboard | power board + pack |")
    print("|---|---:|---:|---:|---:|---:|")
    for s in ("LOW", "NORMAL", "HIGH", "WORST"):
        h = heat_split(s)
        z = list(h["zones"].values())
        print(f"| {s} | {h['base']:.2f} | {h['lid']:.2f} | {z[0]:.2f} | {z[1]:.2f} | {z[2]:.2f} |")
    for s, w in (("NORMAL", 60.0), ("HIGH", 60.0)):
        h = heat_split(s, w)
        print(f"| {s} + charging {w:.0f} W | {h['base']:.2f} | {h['lid']:.2f} | | | {list(h['zones'].values())[2]:.2f} |")


if __name__ == "__main__":
    main()
