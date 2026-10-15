"""NOMAD Virtual V1 preliminary BOM and staged-purchase totals (standard library, no side effects except --write).

  py prototypes/V1/v1_bom.py            print the BOM report
  py prototypes/V1/v1_bom.py --write    also (re)write prototypes/V1/V1_BOM.csv
  py prototypes/V1/v1_bom.py --check    exit 1 if V1_BOM.csv is not current

Source: prototypes/V1/v1_hardware.py (one record per item). Prices are approximate, as found (see v1_hardware SOURCES),
never fixed. Nothing has been ordered.
"""
import csv
import importlib.util
import io
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("v1_hardware", os.path.join(HERE, "v1_hardware.py"))
HWM = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(HWM)
HW = HWM.HW
CSV_PATH = os.path.join(HERE, "V1_BOM.csv")

USD_EUR = 0.86          # ASSUMED planning exchange rate (October 2026), not a quote
US_IMPORT = 1.30        # ASSUMED multiplier on US-listed prices for shipping + EU import VAT/handling (one order)
CONTINGENCY = 0.15      # ASSUMED: breakage, wrong part, spares, small hardware not listed
PLANNING_EST = {"DCTRL": (120.0, "EST planning figure; Beck price on request (quote required)")}
GROUP = {"compute": "electronics", "compute cooling": "electronics", "storage adapter": "electronics", "storage": "electronics",
         "display": "electronics", "display controller": "electronics", "display cable": "electronics",
         "display signal": "electronics", "keyboard": "electronics", "trackpad": "electronics", "GNSS": "electronics",
         "enclosure cooling": "electronics", "solar": "electronics", "battery cells": "electronics",
         "battery pack": "electronics", "charger / power path": "electronics", "5.1 V rail": "electronics",
         "12 V rail": "electronics", "power button": "electronics", "external USB": "electronics",
         "display-lid hinge": "mechanical", "solar-leaf hinge": "mechanical", "B1 stability": "mechanical",
         "fasteners": "mechanical", "harness": "mechanical", "printed structure": "mechanical",
         "power validation": "validation (bench only)", "bench": "validation (bench only)"}
GATE_NAME = {1: "Gate 1 - mechanical risk (hinge coupon, stay, print material)",
             2: "Gate 2 - envelope-critical HMI (display + controller, keyboard, trackpad, display hinges)",
             3: "Gate 3 - compute stack + GNSS + cooling (bench bring-up)",
             4: "Gate 4 - power validation (EVM, cells, regulators, solar panel)",
             5: "Gate 5 - integration build (custom power PCB, harness, final parts)"}


def eur(item_id, it):
    if it["price"] is None:
        p, src = PLANNING_EST[item_id]
        return p, src
    if it["cur"] == "USD":
        return it["price"] * USD_EUR * US_IMPORT, f"US${it['price']:.2f} x {USD_EUR} x {US_IMPORT} (import, ASSUMED)"
    return it["price"], it["price_src"]


def rows():
    out = []
    for k, it in HW.items():
        unit, basis = eur(k, it)
        out.append(dict(id=k, cls=it["cls"], gate=it["gate"], group=GROUP[it["role"]], description=it["name"],
                        manufacturer=it["mfr"], model=it["sku"], qty=it["qty"], unit_eur=round(unit, 2),
                        ext_eur=round(unit * it["qty"], 2), price_basis=basis, source=it["price_src"],
                        status=it["status"], availability=it["avail"]))
    return out


def csv_text(rs):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rs[0].keys()), lineterminator="\n")
    w.writeheader()
    for r in rs:
        w.writerow(r)
    return buf.getvalue()


def main(argv):
    rs = rows()
    text = csv_text(rs)
    if "--write" in argv:
        with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
            f.write(text)
    if "--check" in argv:
        cur = open(CSV_PATH, encoding="utf-8").read() if os.path.exists(CSV_PATH) else ""
        if cur != text:
            print("V1_BOM.csv is OUT OF DATE (run --write)")
            return 1
        print("V1_BOM.csv is current")
    print("# NOMAD Virtual V1 preliminary BOM (v1_bom.py)\n")
    print(f"EUR; USD items x {USD_EUR} x {US_IMPORT} (ASSUMED FX + import); prices approximate, as found; nothing ordered.\n")
    for cls in ("BUY", "FABRICATE", "SOURCE_LATER"):
        print(f"## {cls}\n")
        print("| Item | Manufacturer | Model / SKU | Qty | Unit EUR | Ext EUR | Gate | Status | Price basis |")
        print("|---|---|---|---:|---:|---:|---:|---|---|")
        for r in rs:
            if r["cls"] == cls:
                print(f"| {r['description']} | {r['manufacturer']} | {r['model']} | {r['qty']} | {r['unit_eur']:.2f} | "
                      f"{r['ext_eur']:.2f} | {r['gate']} | {r['status']} | {r['price_basis']} |")
        print()
    tot = {}
    for r in rs:
        tot[r["group"]] = tot.get(r["group"], 0) + r["ext_eur"]
    sub = sum(v for k, v in tot.items() if not k.startswith("validation"))
    print("## Totals (EUR, approximate)\n")
    for k, v in tot.items():
        print(f"- {k}: {v:.0f}")
    print(f"- prototype hardware + materials (excl. bench-only items): {sub:.0f}")
    print(f"- contingency {CONTINGENCY:.0%}: {sub * CONTINGENCY:.0f}")
    print(f"- **estimated V1 prototype cost: {sub * (1 + CONTINGENCY):.0f}** "
          f"(+ bench validation {tot.get('validation (bench only)', 0):.0f} = {sub * (1 + CONTINGENCY) + tot.get('validation (bench only)', 0):.0f})\n")
    print("## By purchase gate (EUR, incl. bench items, before contingency)\n")
    g = {}
    for r in rs:
        g[r["gate"]] = g.get(r["gate"], 0) + r["ext_eur"]
    run = 0.0
    for k in sorted(g):
        run += g[k]
        print(f"- {GATE_NAME[k]}: {g[k]:.0f} (cumulative {run:.0f})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
