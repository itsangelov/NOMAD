"""E-POWER research campaign calculator (research only, standard library, no side effects).

Reproduces every load, battery, solar, thermal and mass number in docs/E-POWER-RESEARCH-CAMPAIGN.md.
Run:  py prototypes/V1/epower_campaign_calc.py

Every input carries an evidence label, matching the dossier:
  MFR      manufacturer datasheet / product page / official documentation
  3P       independent third-party measurement (named in the dossier)
  3P-SEC   secondary third-party claim (method unclear; lowest weight)
  PVGIS    EU JRC PVGIS 5.3 model output (SARAH3/ERA5), Sofia 42.698 N 23.322 E
  CALC     arithmetic on labelled inputs
  ASSUMED  scenario assumption, chosen by this study and stated; never a measured value

Nothing here is a design decision. The runtime target and normal display brightness are owner decisions;
this script models them as scenarios.
"""
import math

# ------------------------------------------------------------------ component loads (W at the component)
# Raspberry Pi 5 8 GB board (incl. its PMIC), by workload. CNX values are wall measurements incl. adapter loss.
PI = {
    "idle":   (3.2, "3P Geerling 2024 (8 GB C1 idle); range 2.6 Tom's (with cooler) .. 3.6 CNX wall"),
    "normal": (4.0, "MFR 'typical bare-board active current' 0.8 A x 5.0 V; CNX video 5.5-6.8 W wall"),
    "high":   (8.8, "3P CNX stress, wall (Tom's 6.8 W board+cooler, Geerling 9.8 W)"),
    "worst":  (9.8, "3P Geerling stress-ng 8 GB; CNX multitask incl. USB SSD 15.9-16.8 W wall noted separately"),
}
NVME = {"idle": (0.05, "MFR SN740 512 GB avg active (MobileMark)"), "normal": (0.05, "MFR SN740 avg active"),
        "high": (2.0, "ASSUMED sustained I/O on PCIe 2.0 x1 (3P-SEC claims +1-2 W)"),
        "worst": (4.7, "MFR SN740 512 GB average maximum (Gen4 host) - upper bound")}
FAN = {"idle": (0.0, "MFR firmware: fan off below 50 C"), "normal": (0.15, "ASSUMED 30-50 % PWM"),
       "high": (0.5, "3P-SEC Active Cooler ~0.5 W"), "worst": (0.5, "3P-SEC Active Cooler ~0.5 W")}
GNSS = {"idle": (0.069, "MFR DAN-F10N tracking 21 mA x 3.3 V"), "normal": (0.069, "MFR tracking"),
        "high": (0.086, "MFR acquisition 26 mA x 3.3 V"), "worst": (0.086, "MFR acquisition")}
HID = {"idle": (0.15, "ASSUMED keyboard+trackpad (Perixx unpublished)"), "normal": (0.25, "ASSUMED"),
       "high": (0.25, "ASSUMED"), "worst": (1.0, "ASSUMED bound: 2 x 100 mA x 5 V declared-class devices")}

# Display systems: (logic W, backlight W at 100 % duty incl. LED-driver input, controller W, full-luminance nit)
DISPLAY = {
    "D-A AUO B101UAN01 + Beck BTC-mini-eDP": dict(
        logic=0.95, bl_full=2.5, ctrl_typ=1.12, ctrl_max=1.29, nit=380,
        src="MFR AUO B101UAN01.7 spec: PDD 0.95 W max, PLED 2.5 W max @380 nit (driver incl.); "
            "MFR Beck BTC-mini-eDP 1.12 W typ / 1.29 W max"),
    "D-W Winstar WF101NTYA4LNN0 + Beck BTC-mini + LED driver": dict(
        logic=1.0, bl_full=5.8 / 0.875, ctrl_typ=0.72, ctrl_max=1.25, nit=500,
        src="MFR Winstar: logic 1.0 W typ, LED string 29 V x 200 mA = 5.8 W; LED-driver efficiency 0.875 ASSUMED "
            "(0.85-0.90); MFR Beck BTC-mini 0.72 W typ / 1.25 W max"),
}
BRIGHT = {"low (25 % PWM)": 0.25, "mid (50 % PWM)": 0.50, "full (100 %)": 1.00}   # ASSUMED scenario levels


def display_w(d, duty, ctrl="typ"):
    """PWM dimming: average LED power scales with duty at fixed LED current (physics of PWM, not a vendor curve)."""
    return d["logic"] + d["bl_full"] * duty + (d["ctrl_typ"] if ctrl == "typ" else d["ctrl_max"])


SCEN = {  # (Pi/peripheral workload key, display duty, controller case)
    "LOW":    ("idle", 0.25, "typ"),
    "NORMAL": ("normal", 0.50, "typ"),
    "HIGH":   ("high", 1.00, "typ"),
    "WORST":  ("worst", 1.00, "max"),
}

# ------------------------------------------------------------------ conversion
ETA_5V = 0.90      # ASSUMED, inside MFR Pololu D36V50F5 80-95 % band
ETA_DISP = 0.92    # ASSUMED 12 V rail (buck from 4S 90-95 % MFR D36V50F12; boost 80-95 % MFR U3V70F12)
P_QUIESCENT = 0.10  # ASSUMED: 2 regulators 2-4 mA at ~14.4 V (MFR Pololu) + charger 17 uA + BMS 8-40 uA (MFR TI)


def scenario_loads(dkey):
    out = {}
    d = DISPLAY[dkey]
    for s, (wk, duty, cc) in SCEN.items():
        base = PI[wk][0] + NVME[wk][0] + FAN[wk][0] + GNSS[wk][0] + HID[wk][0]
        disp = display_w(d, duty, cc)
        batt = base / ETA_5V + disp / ETA_DISP + P_QUIESCENT
        out[s] = dict(base=base, disp=disp, load=base + disp, batt=batt,
                      loss=batt - base - disp)
    return out


# ------------------------------------------------------------------ cells (MFR datasheets)
CELLS = {
    "Molicel INR-21700-M65A (NMC/Si, v0.1 prelim.)": dict(wh=23.0, m=74.5, shape="cyl", d=21.55, l=70.21, v=3.6),
    "Samsung SDI INR21700-50E": dict(wh=4.9 * 3.63, m=69.5, shape="cyl", d=21.25, l=70.80, v=3.63),
    "Molicel INR-21700-P45B": dict(wh=16.2, m=70.0, shape="cyl", d=21.55, l=70.15, v=3.6),
    "LG INR18650 MJ1": dict(wh=3.5 * 3.635, m=49.0, shape="cyl", d=18.5, l=65.2, v=3.635),
    "A123 ANR26650M1-B (LiFePO4)": dict(wh=2.5 * 3.3, m=76.0, shape="cyl", d=26.0, l=65.0, v=3.3),
    "EEMB LP9051109 (LiPo pouch)": dict(wh=5.5 * 3.7, m=110.0, shape="pouch", t=9.3, w=51.5, l=111.0, v=3.7),
}
USABLE = 0.90      # ASSUMED usable window (cut-off above 2.5 V, top margin)
EOL = 0.80         # MFR Samsung 50E: >= 80 % capacity after 500 cycles (used as design end-of-life)
RESERVE = 0.10     # ASSUMED extra margin for estimate uncertainty / cold
PACK_MASS = 1.20   # ASSUMED holder, nickel, BMS, wiring, insulation
BAY = (90.0, 82.0, 30.0)      # nomad.yaml working BATTERY_BAY_* (reserve, D-007 proposed)
WALL, TOP = 1.5, 4.0          # ASSUMED holder wall per side; height allowance for strips/insulation/BMS


def bay_capacity(c):
    """Max cells in one bay: cylinders lie flat; returns (count, min spare mm across X/Y/Z)."""
    ix, iy, iz = BAY[0] - 2 * WALL, BAY[1] - 2 * WALL, BAY[2] - TOP
    best = (0, -99.0)
    if c["shape"] == "cyl":
        for ax, ay in ((ix, iy), (iy, ix)):           # cell axis along Y (82) or X (90)
            n_across, n_long, n_lay = int(ax // c["d"]), int(ay // c["l"]), int(iz // c["d"])
            n = n_across * n_long * n_lay
            if n:
                spare = min(ax - n_across * c["d"], ay - n_long * c["l"], iz - n_lay * c["d"])
                best = max(best, (n, spare))
    else:
        dims = (c["t"], c["w"], c["l"])
        import itertools
        for p in itertools.permutations(dims):
            n = int(ix // p[0]) * int(iy // p[1]) * int(iz // p[2])
            if n:
                spare = min(ix - int(ix // p[0]) * p[0], iy - int(iy // p[1]) * p[1], iz - int(iz // p[2]) * p[2])
                best = max(best, (n, spare))
    return best


# ------------------------------------------------------------------ solar (PVGIS 5.3, P108 = 9.92 Wp, loss=0, c-Si)
PV = {  # Wh/day at the panel, before the charger
    "ideal: 2-axis tracking, July mean": 78.1,
    "good: 35 deg south, Jun-Aug median (P50)": 56.0,     # mean of 51.9/60.6/60.8 (Jun/Jul/Aug P50)
    "annual mean, 35 deg south": 41.9,
    "winter typical: 35 deg south, Dec-Jan median": 18.6,  # mean of 15.3 / 21.8
    "poor: 35 deg south, Dec-Jan worst decile (P10)": 6.0,  # mean of 5.3 / 6.6
    "closed lid flat (building-integrated), Dec median": 10.7,
}
ETA_SOLAR = 0.85   # ASSUMED charge chain: MPPT tracking x converter (BQ25798 96.5 % peak MFR) x charge acceptance


# ------------------------------------------------------------------ thermal
RHO, CP = 1.13, 1007.0   # air at ~40 C (physical constants)


def airflow_cfm(p_w, dt_k):
    return p_w / (RHO * CP * dt_k) * 2118.88


# ------------------------------------------------------------------ report
def main():
    print("# E-POWER campaign calculator output\n")
    print(f"Assumptions: eta_5V {ETA_5V}, eta_display {ETA_DISP}, quiescent {P_QUIESCENT} W, usable {USABLE}, "
          f"EOL {EOL}, reserve {RESERVE}, pack mass x{PACK_MASS}, solar chain {ETA_SOLAR}\n")

    print("## 1. Display system power by brightness (W at the display subsystem input)\n")
    print("| Display system | low 25 % | mid 50 % | full 100 % | full, controller max | luminance at low/mid/full (nit) |")
    print("|---|---:|---:|---:|---:|---|")
    for k, d in DISPLAY.items():
        v = [display_w(d, f) for f in BRIGHT.values()]
        print(f"| {k} | {v[0]:.2f} | {v[1]:.2f} | {v[2]:.2f} | {display_w(d, 1.0, 'max'):.2f} | "
              f"{d['nit'] * 0.25:.0f} / {d['nit'] * 0.5:.0f} / {d['nit']:.0f} |")

    for dkey in DISPLAY:
        L = scenario_loads(dkey)
        print(f"\n## 2. System load scenarios — {dkey}\n")
        print("| Scenario | base-side load (Pi, NVMe, fan, GNSS, HID) | display | total at loads | conversion+quiescent loss | at battery |")
        print("|---|---:|---:|---:|---:|---:|")
        for s, r in L.items():
            print(f"| {s} | {r['base']:.2f} | {r['disp']:.2f} | {r['load']:.2f} | {r['loss']:.2f} | **{r['batt']:.2f}** |")

        print(f"\n### 2b. Battery energy for runtime scenarios — {dkey}\n")
        print("| Scenario | hours | theoretical (at loads) Wh | at battery (usable) Wh | design nominal Wh (/usable/EOL) | + reserve Wh | Ah @3.6 V (1S) | Ah @7.2 V (2S) | Ah @10.8 V (3S) | Ah @14.4 V (4S) | Ah @12.8 V (4S LFP) |")
        print("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
        for s in ("LOW", "NORMAL", "HIGH", "WORST"):
            for h in (4, 6, 8):
                r = L[s]
                th, ub = r["load"] * h, r["batt"] * h
                des = ub / USABLE / EOL
                res = des * (1 + RESERVE)
                print(f"| {s} | {h} | {th:.0f} | {ub:.0f} | {des:.0f} | {res:.0f} | {res/3.6:.1f} | {res/7.2:.1f} | "
                      f"{res/10.8:.1f} | {res/14.4:.1f} | {res/12.8:.1f} |")

    print("\n## 3. Cell options vs. the reserved bay (90 x 82 x 30 working)\n")
    print("| Cell | Wh/cell | g/cell | max cells in bay (layout) | min spare mm | max nominal Wh in bay | usable-at-EOL Wh in bay |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    for k, c in CELLS.items():
        n, sp = bay_capacity(c)
        print(f"| {k} | {c['wh']:.2f} | {c['m']:.1f} | {n} | {sp:.1f} | {n * c['wh']:.1f} | {n * c['wh'] * USABLE * EOL:.1f} |")

    print("\n## 2c. Architecture comparison (battery-side W; conversion efficiencies ASSUMED inside MFR bands)\n")
    arch = {  # (eta for 5 V loads, eta for display subsystem, extra quiescent W)
        "A single 5 V rail; display controller fed by 5->12 V boost": (0.90, 0.90 * 0.90, 0.06),
        "B separate rails: 5 V buck + 12 V buck/boost from battery": (0.90, 0.92, 0.10),
        "C 12 V intermediate bus, then 5 V from the bus": (0.93 * 0.90, 0.93, 0.10),
        "D 1S Pi-UPS-HAT style: 1S->5 V boost + 1S->12 V boost": (0.88, 0.88, 0.10),
    }
    print("| Architecture | NORMAL D-A | HIGH D-A | WORST D-A | NORMAL D-W | HIGH D-W |")
    print("|---|---:|---:|---:|---:|---:|")
    for name, (e5, ed, q) in arch.items():
        vals = []
        for dk, sk in ((0, "NORMAL"), (0, "HIGH"), (0, "WORST"), (1, "NORMAL"), (1, "HIGH")):
            dkk = list(DISPLAY)[dk]
            wk, duty, cc = SCEN[sk]
            base = PI[wk][0] + NVME[wk][0] + FAN[wk][0] + GNSS[wk][0] + HID[wk][0]
            disp = display_w(DISPLAY[dkk], duty, cc)
            vals.append(base / e5 + disp / ed + q)
        print(f"| {name} | " + " | ".join(f"{v:.2f}" for v in vals) + " |")
    worst = scenario_loads(list(DISPLAY)[1])["WORST"]["batt"]
    print(f"\nPeak battery current at WORST (D-W, {worst:.1f} W) at 3.0 V per Li-ion cell (near empty): "
          + ", ".join(f"{n}S {worst / (3.0 * n):.1f} A" for n in (1, 2, 3, 4)))

    print("\n## 4. Pack size per scenario (design nominal + reserve), cells / mass / bay fit\n")
    print("Bay capacity with one flat layer (90 x 82 x 30): 4 x 21700 -> M65A 92 Wh (preliminary datasheet, 0.8 mm side spare), "
          "50E 71 Wh (2.0 mm spare); 4 x 18650 MJ1 51 Wh; 3 x 26650 LFP 25 Wh.\n")
    print("| Scenario | display | h | design Wh | fits bay with 50E (<=71)? | fits with M65A (<=92)? | 21700 layers needed (M65A) | bay needed (mm, 1 layer = 21.55 + 4) | 4S cells (M65A) |")
    print("|---|---|---:|---:|---|---|---:|---|---:|")
    for dkey in DISPLAY:
        L = scenario_loads(dkey)
        for s in ("LOW", "NORMAL", "HIGH"):
            for h in (4, 6, 8):
                des = L[s]["batt"] * h / USABLE / EOL * (1 + RESERVE)
                n = math.ceil(des / 23.0)
                n4 = math.ceil(n / 4) * 4
                layers = math.ceil(n / 4)
                hbay = layers * 21.55 + TOP
                f50 = "fits (tight)" if des <= 71.1 else "no"
                f65 = "marginal" if des <= 92.0 else "no"
                print(f"| {s} | {dkey[:3]} | {h} | {des:.0f} | {f50} | {f65} | {layers} | 90 x 82 x {hbay:.0f} | {n4} |")

    print("\n### Cell counts and pack mass by chemistry (design nominal + reserve)\n")
    for dkey in DISPLAY:
        L = scenario_loads(dkey)
        print(f"\n### {dkey}\n")
        print("| Scenario | h | design Wh | M65A cells / kg | 50E cells / kg | MJ1 cells / kg | A123 LFP cells / kg | over 100 Wh (IATA approval)? |")
        print("|---|---:|---:|---|---|---|---|---|")
        for s in ("LOW", "NORMAL", "HIGH", "WORST"):
            for h in (4, 6, 8):
                des = L[s]["batt"] * h / USABLE / EOL * (1 + RESERVE)
                cols = []
                for ck in ("Molicel INR-21700-M65A (NMC/Si, v0.1 prelim.)", "Samsung SDI INR21700-50E",
                           "LG INR18650 MJ1", "A123 ANR26650M1-B (LiFePO4)"):
                    c = CELLS[ck]
                    n = math.ceil(des / c["wh"])
                    cols.append(f"{n} / {n * c['m'] * PACK_MASS / 1000:.2f}")
                print(f"| {s} | {h} | {des:.0f} | " + " | ".join(cols) + f" | {'yes' if des > 100 else 'no'} |")

    print("\n## 5. Solar into the battery (P108, Sofia, PVGIS, x solar-chain efficiency)\n")
    print("| Condition | panel Wh/day | into battery Wh/day |")
    print("|---|---:|---:|")
    for k, v in PV.items():
        print(f"| {k} | {v:.1f} | {v * ETA_SOLAR:.1f} |")

    print("\n## 6. Solar share of daily need (daily use = runtime hours, D-A display)\n")
    L = scenario_loads(list(DISPLAY)[0])
    print("| Scenario | h/day | need at battery Wh/day | ideal % | good % | annual mean % | winter typ % | poor % |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|")
    for s in ("LOW", "NORMAL", "HIGH"):
        for h in (4, 6, 8):
            need = L[s]["batt"] * h
            pv = [v * ETA_SOLAR / need * 100 for k, v in PV.items() if not k.startswith("closed")]
            print(f"| {s} | {h} | {need:.0f} | " + " | ".join(f"{p:.0f}" for p in pv) + " |")
    des_u = L["NORMAL"]["batt"] * 6
    print(f"\nDays of solar needed to replace ONE day of NORMAL 6 h use ({des_u:.0f} Wh at the battery, D-A):")
    for k, v in PV.items():
        print(f"  {k}: {des_u / (v * ETA_SOLAR):.1f} days")
    full = 92.0 * USABLE
    print(f"\nDays of solar to refill a full 92 Wh bay pack from empty ({full:.0f} Wh usable when new):")
    for k, v in PV.items():
        print(f"  {k}: {full / (v * ETA_SOLAR):.1f} days")
    for w in (30.0, 45.0, 60.0):
        print(f"USB-C PD charge of {full:.0f} Wh at {w:.0f} W input, 93 % chain (ASSUMED), no load: "
              f"{full / (w * 0.93):.1f} h (CC-CV taper adds time; charger limit 5 A MFR BQ25798)")

    print("\n## 7. Heat and airflow (base heat = base loads + 5 V conversion loss; ΔT internal vs outside air)\n")
    print("| State | base heat W | lid heat W (display system) | CFM for ΔT 10 K | CFM for ΔT 15 K |")
    print("|---|---:|---:|---:|---:|")
    for dkey in DISPLAY:
        for s, r in scenario_loads(dkey).items():
            base_heat = r["base"] / ETA_5V + P_QUIESCENT   # everything entering the base ends as heat
            print(f"| {s} ({dkey[:3]}) | {base_heat:.1f} | {r['disp'] / ETA_DISP:.1f} | {airflow_cfm(base_heat, 10):.2f} | {airflow_cfm(base_heat, 15):.2f} |")
    ch = 60.0 * (1 - 0.965) + 0.3   # charging at 60 W through a 96.5 %-class charger + I2R (ASSUMED 0.3 W)
    print(f"| CHARGING 60 W input (charger 96.5 % MFR peak + ~0.3 W cell I2R ASSUMED) | +{ch:.1f} | - | - | - |")
    a = 0.273 * 0.223 * 1000 * 0.9
    print(f"\nP108 absorbed at 1000 W/m2, absorptance 0.9 (ASSUMED as D-010 Phase 2): {a:.0f} W; "
          f"minus ~9 W electrical at best -> ~{a - 9:.0f} W heat at the leaf")

    print("\n## 8. Mass deltas vs D-010 Phase 2 placeholders (battery 0.26 kg, PE 0.08, compute power 0.03, "
          "display 0.15, controller 0.03)\n")
    print("| Battery case | pack kg (M65A) | pack kg (50E) | delta vs 0.26 kg placeholder (M65A / 50E) | total NOMAD (2.62 kg base case) |")
    print("|---|---:|---:|---:|---:|")
    L = scenario_loads(list(DISPLAY)[0])
    for s in ("NORMAL", "HIGH"):
        for h in (4, 6, 8):
            des = L[s]["batt"] * h / USABLE / EOL * (1 + RESERVE)
            mA = math.ceil(des / 23.0) * 74.5 * PACK_MASS / 1000
            mS = math.ceil(des / (4.9 * 3.63)) * 69.5 * PACK_MASS / 1000
            print(f"| {s} {h} h ({des:.0f} Wh) | {mA:.2f} | {mS:.2f} | {mA - 0.26:+.2f} / {mS - 0.26:+.2f} | "
                  f"{2.62 + mA - 0.26:.2f} / {2.62 + mS - 0.26:.2f} |")


if __name__ == "__main__":
    main()
