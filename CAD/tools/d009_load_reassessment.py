"""D-009 load reassessment (NON-PRODUCTION, read-only): the index-lock load path including the transverse reaction of
the pin-tip index force, which the hub load check and the anti-rotation check treated as a pure torque.

Model (inferred; hand statics, no FEA):
- Cassette = rigid body on the pin through the 10 mm PETG hub-bracket bore (X 0.5-10.5, centre 5.5).
- External loads on the cassette: user force P at an outboard corner (panel normal, X 148, lever to the tilt axis 114.3
  for the far corner) and the weight W (0.35 kg, at X 74.25, any direction), both x2 at the design case.
- Internal pair: the cassette's index pin pushes the index plate (on the pin tip, X 11.75) with F = T / r (r 10),
  tangential at the index-pin angle; the cassette gets -F at the same X.
- Statics: the bore carries V = P + W - F and M = 142.5 P + 68.75 W - 6.25 F (vectors); the pin carries +F at X 11.75
  and the bore loads. F cancels in the pin moment inboard of the bore (checked numerically below): the pin ROOT is
  unaffected; the BORE and the pin inside / just outboard of the bore are.
- Bore pressure: the hub load check's rigid-pin / linear model p = V/(dL) + 6M/(dL^2); tear-out and ligament tension as
  in that check (F_e = 1.5 M / L + V / 2 over L/2, wall 2.5).
Usage: py CAD/tools/d009_load_reassessment.py
"""
import math
import sys

import e_lid_layout as el

W_KG = 0.35
G = 9.81
P_HANDLING = 5.0                 # N at the outboard corner (hub load check s.4)
X_P, X_W, X_BC = 148.0, 74.25, 5.5
X_ROOT = -11.0
D, L = 5.0, 10.0                 # bore
Z_R, ZP_R = math.pi * D ** 3 / 32, math.pi * D ** 3 / 16
Z_DD, ZT_DD = 6.6, 12.9          # double-D A/F 3.0 (anti-rotation check s.5.1)
SY = {"303": 415.0, "17-4 H1025": 1000.0, "301h": 758.0, "dowel_hard": 1000.0}
PETG = {"bearing": (30.0, 15.0), "shear_in": 15.0, "shear_across": 10.0, "tens_in": 35.0, "tens_across": 20.0}


def rot(v, a):
    c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
    return (c * v[0] - s * v[1], s * v[0] + c * v[1])


def add(*vs):
    return (sum(v[0] for v in vs), sum(v[1] for v in vs))


def sc(k, v):
    return (k * v[0], k * v[1])


def norm(v):
    return math.hypot(*v)


def case_vectors(env, k, far=True, tilt=0.0, grav_dir=None):
    """Force vectors (lid frame, YZ) for load level k (1 handling, 2 design, 4 acceptance) at a tilt. Returns
    (P, W, F, T). The far corner is on the -u side of the axis (114.3 from the CY0 edge)."""
    u = rot((1.0, 0.0), tilt)
    n = rot((0.0, 1.0), tilt)
    lever = 114.3 if far else 85.7
    w_mag = k * W_KG * G
    t_grav = k * W_KG * G * math.hypot(14.3, 9.5)         # upper bound of the gravity torque (hub load check s.3)
    p_mag = k * P_HANDLING
    s = -1.0 if far else 1.0                              # corner on -u (far) or +u (near)
    P = sc(s * p_mag, n)                                  # corner at s*lever*u: positive torque needs P = s|P| n
    T = p_mag * lever + t_grav
    f_dir = rot((0.0, 1.0), env["SOLAR_INDEX_PIN_ANGLE"] + tilt)   # tangential (CCW) at the index pin
    F = sc(T / env["SOLAR_INDEX_RADIUS"], f_dir)
    Wv = sc(w_mag, grav_dir) if grav_dir else (0.0, 0.0)
    return P, Wv, F, T


def bore_loads(P, Wv, F):
    V = add(P, Wv, sc(-1, F))
    M = add(sc(X_P - X_BC, P), sc(X_W - X_BC, Wv), sc(-(el_xc() - X_BC), F))
    return V, M


def el_xc():
    return 11.75


def pin_moment(P, Wv, F, x):
    """Internal pin bending moment (as a force-direction vector x arm) at section x, from the loads outboard of x:
    +F at the plate and the bore distribution (linear model), all transverse loads on the pin."""
    V, M = bore_loads(P, Wv, F)
    # pin receives from the cassette at the bore: force V_p = P + W - F ... as a distributed linear load equivalent to
    # force V_p at X_BC and moment M_p about X_BC; build q(x) = a + b (x - X_BC) over [0.5, 10.5]
    Vp, Mp = V, M
    a = (Vp[0] / L, Vp[1] / L)
    b = (12 * Mp[0] / L ** 3, 12 * Mp[1] / L ** 3)
    x0, x1 = X_BC - L / 2, X_BC + L / 2
    m = sc(max(0.0, el_xc() - x), F) if x < el_xc() else (0.0, 0.0)
    lo = max(x, x0)
    if lo < x1:
        n = 200
        for i in range(n):
            xs = lo + (x1 - lo) * (i + 0.5) / n
            dx = (x1 - lo) / n
            q = add(a, sc(xs - X_BC, b))
            m = add(m, sc((xs - x) * dx, q))
    return m


def main():
    env = el.evaluate()[0]
    print("D-009 load reassessment (NON-PRODUCTION; inferred hand statics; geometry unchanged)")
    r, dpin, tpl = env["SOLAR_INDEX_RADIUS"], env["SOLAR_INDEX_PIN_DIAMETER"], env["SOLAR_INDEX_PLATE_THICKNESS"]
    hole = env["SOLAR_INDEX_HOLE_DIAMETER"]
    wf = 2 * math.sqrt(2.5 ** 2 - (2.5 - (5 - env["SOLAR_HUB_PIN_KEY_ACROSS_FLATS"]) / 2) ** 2)
    print(f"geometry: index r {r:g} at {env['SOLAR_INDEX_PIN_ANGLE']:g} deg, plate X {env['PX0']:g}-{env['PX1']:g} (centre {el_xc()}), "
          f"bore X 0.5-10.5 (centre {X_BC}), root X {X_ROOT}; |cos(index force, panel normal)| = "
          f"{abs(math.cos(math.radians(env['SOLAR_INDEX_PIN_ANGLE']))):.3f}")

    # --- statics check: the index force cancels in the pin moment inboard of the bore
    Pv, Wv, Fv, T = case_vectors(env, 2, True, 30.0, (0.0, -1.0))
    for x in (X_ROOT, 0.0, 0.5):
        with_f = pin_moment(Pv, Wv, Fv, x)
        without = pin_moment(Pv, Wv, (0.0, 0.0), x)
        print(f"check: pin moment at X {x:+g} with / without the index force: {norm(with_f):.2f} / {norm(without):.2f} N.mm")

    rows = []
    for tag, k in (("handling (0.35 kg + 5 N)", 1), ("design T_d", 2), ("acceptance 2 x T_d", 4)):
        worst = {}
        for far in (True, False):
            for tilt in range(-75, 76, 15):
                for g10 in range(0, 360, 15):
                    gd = rot((1.0, 0.0), g10)
                    Pv, Wv, Fv, T = case_vectors(env, k, far, float(tilt), gd)
                    V, M = bore_loads(Pv, Wv, Fv)
                    V0, M0 = bore_loads(Pv, Wv, (0.0, 0.0))
                    for key, val in (("V", norm(V)), ("M", norm(M)), ("V0", norm(V0)), ("M0", norm(M0))):
                        worst[key] = max(worst.get(key, 0.0), val)
                    pm = max(norm(pin_moment(Pv, Wv, Fv, x / 10)) for x in range(5, 106, 5))
                    worst["pin_bore"] = max(worst.get("pin_bore", 0.0), pm)
                    worst["T"] = max(worst.get("T", 0.0), T)
                    worst["root"] = max(worst.get("root", 0.0), norm(pin_moment(Pv, Wv, Fv, X_ROOT)))
        rows.append((tag, k, worst))

    for tag, k, w in rows:
        T = w["T"]
        F = T / r
        print(f"\n== {tag}: T {T / 1000:.3f} N.m (far-corner push, gravity worst of 24 directions, tilts -75..75), index force F {F:.0f} N")
        out = []
        # hub pin
        sig_root, tau_r = w["root"] / Z_R, T / ZP_R
        out.append(("hub pin root (round, bending + torsion)", math.sqrt(sig_root ** 2 + 3 * tau_r ** 2), SY["303"], "303",
                    f"M {w['root']:.0f} N.mm (unchanged by F: exact statics)"))
        out.append(("hub pin inside the bore (max, round)", math.sqrt((w['pin_bore'] / Z_R) ** 2 + 3 * tau_r ** 2), SY["303"], "303",
                    f"M {w['pin_bore']:.0f} N.mm"))
        out.append(("hub pin at the plate / double-D start X 11", math.sqrt((F * 0.75 / Z_DD) ** 2 + 3 * (T / ZT_DD) ** 2), SY["303"], "303",
                    f"M {F * 0.75:.0f} N.mm"))
        out.append(("hub pin inboard double-D (torsion only)", math.sqrt(3) * T / ZT_DD, SY["303"], "303", ""))
        # PETG bracket
        for lab, V, M in (("with index reaction", w["V"], w["M"]), ("previous model (pure torque)", w["V0"], w["M0"])):
            p = V / (D * L) + 6 * M / (D * L * L)
            fe = 1.5 * M / L + V / 2
            te = fe / (2 * 2.5 * 5)
            out.append((f"bracket bore bearing, {lab}", p, PETG["bearing"][0], "PETG RT (hot /2)", f"V {V:.0f} N, M {M:.0f} N.mm"))
            out.append((f"bracket tear-out under the pin, {lab}", te, PETG["shear_in"], "PETG in-layer (across-layer 10)", f"F_e {fe:.0f} N"))
            out.append((f"bracket ligament tension, Kt 2.5 peak, {lab}", 2.5 * te, PETG["tens_in"], "PETG in-layer (across-layer 20)", ""))
        # index pin / plate / keys
        Lsp = 0.5 + tpl + 0.5 + 2 * 1.0
        Mi = F * (Lsp / 4 - tpl / 8)
        out.append(("index pin bending (double shear span)", Mi / (math.pi * dpin ** 3 / 32), SY["dowel_hard"], "hardened dowel", ""))
        out.append(("index pin shear", F / (2 * math.pi * dpin ** 2 / 4), 0.58 * SY["dowel_hard"], "hardened dowel", ""))
        web = 2 * r * math.sin(math.radians(7.5)) - hole
        out.append(("index plate bearing", F / (dpin * tpl), SY["301h"], "301 1/2-hard", ""))
        out.append(("index plate web bending", (F * hole / 8) / (tpl * web ** 2 / 6), SY["301h"], "301 1/2-hard", ""))
        key_t = 6 * T / (tpl * wf * wf)
        key_tf = key_t + F / (wf * tpl)
        out.append(("tip key edge pressure, torque only (previous)", key_t, SY["301h"], "301 1/2-hard", ""))
        out.append(("tip key edge pressure + transverse index force on one flat", key_tf, SY["301h"], "301 1/2-hard", ""))
        out.append(("index plate key-hole bearing from F", F / (D * tpl), SY["301h"], "301 1/2-hard", ""))
        out.append(("anti-rotation plate key (torque only; F does not reach it)", 6 * T / (1.5 * wf * wf), SY["301h"], "301 1/2-hard", ""))
        e = math.hypot(5.0, 2.5)
        Fd = T / e
        for kk in (1000.0, 2500.0):
            beta = (kk / (4 * 193000.0 * math.pi * 3 ** 4 / 64)) ** 0.25
            out.append((f"carriage PETG under the dowel, bound (k {kk:g})", Fd * beta / 3, PETG["bearing"][0], "PETG RT (hot /2)", f"dowel {Fd:.0f} N"))
        out.append(("carriage pin bearing (28.4 embed, root moment)", w["root"] * 6 / (D * 28.4 ** 2) + k * 8.43 / (D * 28.4), PETG["bearing"][0], "PETG RT", ""))
        out.append(("M2 retention screws (axial: 100 N stow / deploy impact; transverse carried by the keys)", 100.0 / 2.07, 450.0, "A2-70", ""))
        for name, s, allow, mat, note in out:
            print(f"   {name}: {s:.1f} MPa -> SF {allow / s:.2f} ({mat}) {note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
