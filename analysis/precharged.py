"""
VOLLEY | The pre-charged chamber: charge slowly to a commanded pressure, fire as a closed
expansion.

WHY THIS EXISTS
---------------
P63. A40 killed the fixed orifice -- 4.7 g mean delivered where 25 is needed. It named three
repairs and chose none. This runs the third: charge a chamber over the sixty seconds already
spent indexing, then fire it as a closed adiabatic expansion. There is no flow-rate problem
by construction, which is the entire failure A40 found, and velocity becomes a function of
CHARGE PRESSURE rather than of a valve timed to a millisecond.

THE PREDICTION, AND WHY IT IS NOT THE BAND
------------------------------------------
Asked what A41 would find in A40, I said the seal. Checked before declaring: a 4 L chamber at
50 bar tolerates 1.67 mbar.L/s over the 1200 s inter-shot interval, against static seals at
1e-6. Wrong by six orders. Dynamic friction at 32 m/s permits 89 N on a 15.8 mm bore, also
comfortable. Both are bands 7 and 8 anyway -- a prediction is worth less when it is only
recorded after it survives.

What bites is the GAS BUDGET. A pre-charged chamber fills a large dead volume that only
partly expands and vents the rest, so twelve shots need 2400 bar.L against the 342 A39's
bottle holds. That is band 4, and the chamber volume is the design variable that cuts both
ways: bigger flattens the expansion and raises velocity, and costs gas proportionally.

Bands declared in validation/A41_precharged_chamber.md at 3d61bab, BEFORE this file existed.

Provenance: model output. Ideal gas, adiabatic closed expansion, vented residual, no gas
recovery, no temperature effect on charge, no fill-time check. Every omission is optimistic.
"""
import json
import math
import os

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
PARAMS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      'cad', 'parameters.json')

GAMMA, R_GAS, T0, RHO_STORE = 1.4, 296.8, 300.0, 235.0
BORE = 0.015805366135494582
AREA = math.pi * (BORE / 2.0) ** 2
M_PAY, G = 4.0, 9.81
N_MANIFEST = 12
P_STORE = 200e5

# A41's OWN declared point, frozen. main() reproduces A41 against these and must keep doing so.
STROKE_A41, G_CAP_A41 = 2.18, 25.0
P_MAX_A41 = M_PAY * G_CAP_A41 * G / AREA


def design_point():
    """The CURRENT design point, read from cad/parameters.json rather than declared here.

    ADR-034 moved the stroke to 8.0 m and the charge pressure to 22.73 bar in the parameter
    file, the CAD and eleven documents, and this module went on declaring 2.18 m and 25 g --
    so gen6_dispersion.py and trim_stage.py, which both read STROKE from here, spent three
    days answering a superseded question. Nothing compared the parameter file against the
    scripts, so every gate stayed green. That is P84, and ADR-015's rule is derive, never
    paste.
    """
    with open(PARAMS, encoding='utf-8') as f:
        g = json.load(f)['groups']
    d, s = g['gen6_drive'], g['gen6_store']
    return dict(stroke=d['stroke_mm'] / 1e3, g_cap=d['acceleration_g'],
                p_max=s['charge_pressure_bar'] * 1e5,
                chamber_m3=s['chamber_volume_l'] / 1e3)


_DP = design_point()
STROKE, G_CAP, P_MAX = _DP['stroke'], _DP['g_cap'], _DP['p_max']


def check_against_parameters(tol=1e-3):
    """FAIL if the design point here and in cad/parameters.json have drifted apart.

    This is the check that did not exist. make_baseline.py compares the scripts against
    their own outputs and build_gen6.py compares the CAD against the parameter file --
    nothing compared the parameter file against the analysis. P84.
    """
    dp = design_point()
    fails = []
    for name, got, want in (('stroke_m', STROKE, dp['stroke']),
                            ('acceleration_g', G_CAP, dp['g_cap']),
                            ('charge_pressure_Pa', P_MAX, dp['p_max'])):
        if abs(got - want) > tol * max(abs(want), 1e-12):
            fails.append(f'{name}: {got} against {want}')
    # the force the parameter file records must follow from the pressure it records
    with open(PARAMS, encoding='utf-8') as f:
        d = json.load(f)['groups']['gen6_drive']
    f_derived = dp['p_max'] * AREA
    if abs(f_derived - d['commanded_force_N']) > 0.5:
        fails.append(f"commanded_force_N: {f_derived:.3f} derived against {d['commanded_force_N']}")
    if abs(f_derived / M_PAY / G - dp['g_cap']) > 5e-3:
        fails.append(f"acceleration_g: {f_derived/M_PAY/G:.6f} derived against {dp['g_cap']}")
    return fails
PV_OVER_W = 15000.0                       # vessel figure of merit, A39
GAS_HARDWARE_KG = 1.5                     # A39's allowance, carried unchanged
BUDGET_KG = 12.55                         # A37: 2.0 kg/sat x 12, less the 11.45 kg base
SIGMA_ALLOW, SAFETY, WALL_MIN = 500e6, 2.0, 1.0e-3


def work(p0, v0, L=None):
    """Adiabatic work of a closed charge expanding through the swept volume.

    L defaults to the CURRENT stroke. Pass STROKE_A41 to reproduce A41.
    """
    L = STROKE if L is None else L
    r = v0 / (v0 + AREA * L)
    return p0 * v0 / (GAMMA - 1.0) * (1.0 - r ** (GAMMA - 1.0))


def shot(p0, v0, L=None):
    w = work(p0, v0, L)
    return dict(p0_bar=p0 / 1e5, chamber_l=v0 * 1e3, work_J=w,
                v_exit=math.sqrt(2.0 * w / M_PAY),
                a_peak_g=p0 * AREA / M_PAY / G,
                charge_barL=(p0 / 1e5) * (v0 * 1e3))


def vessel_kg(p, v):
    return p * v / (PV_OVER_W * G)


def chamber_kg(v0, p0=None):
    """A cylindrical chamber at the charge pressure, hoop-sized with a minimum wall."""
    p0 = P_MAX if p0 is None else p0
    r = (3.0 * v0 / (4.0 * math.pi)) ** (1.0 / 3.0)       # sphere-equivalent radius
    wall = max(WALL_MIN, p0 * r * SAFETY / SIGMA_ALLOW)
    return 4.0 * math.pi * r * r * wall * 7800.0


def store_mass(v0, p0=None, L=None):
    """Chamber + reservoir + gas + A39's hardware allowance, for a full manifest."""
    p0 = P_MAX if p0 is None else p0
    s = shot(p0, v0, L)
    res_barL = N_MANIFEST * s['charge_barL']
    res_m3 = res_barL / (P_STORE / 1e5) / 1e3
    return dict(chamber_kg=chamber_kg(v0, p0), reservoir_l=res_m3 * 1e3,
                vessel_kg=vessel_kg(P_STORE, res_m3), gas_kg=res_m3 * RHO_STORE,
                hardware_kg=GAS_HARDWARE_KG,
                total_kg=chamber_kg(v0, p0) + vessel_kg(P_STORE, res_m3)
                + res_m3 * RHO_STORE + GAS_HARDWARE_KG, **s)


def main():
    fails = check_against_parameters()
    print("design point against cad/parameters.json: "
          + ("OK" if not fails else "DRIFTED -- " + "; ".join(fails)))
    print(f"  current: {STROKE:.2f} m at {P_MAX/1e5:.4f} bar, {G_CAP:.4f} g peak")
    print(f"  A41's own: {STROKE_A41:.2f} m at {P_MAX_A41/1e5:.1f} bar, {G_CAP_A41:.0f} g")
    if fails:
        raise SystemExit(f"{len(fails)} design-point drift(s): {fails}")

    # A41's run sheet must stay reproducible. Its headline was a 2 L chamber at 50 bar giving
    # 30.54 m/s at 25 g on a 4.66 kg store. If this stops matching, a refactor broke a dated
    # result, which is worse than a stale constant.
    a41 = store_mass(2.0e-3, P_MAX_A41, STROKE_A41)
    a41_ok = (abs(a41['v_exit'] - 30.54) < 0.01 and abs(a41['a_peak_g'] - 25.0) < 0.01
              and abs(a41['total_kg'] - 4.66) < 0.01)
    print(f"  A41 reproduction: {a41['v_exit']:.2f} m/s at {a41['a_peak_g']:.2f} g on a "
          f"{a41['total_kg']:.2f} kg store -- {'OK' if a41_ok else 'BROKEN'}\n")
    if not a41_ok:
        raise SystemExit("A41 no longer reproduces from this module")
    print(f"charge pressure at the {G_CAP:.4f} g cap: {P_MAX/1e5:.4f} bar "
          f"(peak force {P_MAX*AREA:.0f} N)")
    print(f"constant-pressure ceiling, p0*A*L: {P_MAX*AREA*STROKE:.0f} J "
          f"-> {math.sqrt(2*P_MAX*AREA*STROKE/M_PAY):.2f} m/s\n")

    print(f"{'chamber L':>10s} {'v m/s':>7s} {'work J':>8s} {'res L':>7s} "
          f"{'gas kg':>7s} {'store kg':>9s}")
    sweep = []
    for v0_l in (0.5, 1, 2, 4, 8, 16, 32, 64):
        m = store_mass(v0_l / 1e3)
        sweep.append(m)
        print(f"{v0_l:10.1f} {m['v_exit']:7.2f} {m['work_J']:8.0f} {m['reservoir_l']:7.2f} "
              f"{m['gas_kg']:7.2f} {m['total_kg']:9.2f}")

    feasible = [m for m in sweep if m['v_exit'] >= 30.0 and m['total_kg'] <= BUDGET_KG]
    selected = min(feasible, key=lambda m: m['total_kg']) if feasible else \
        min((m for m in sweep if m['v_exit'] >= 30.0),
            key=lambda m: m['total_kg'], default=max(sweep, key=lambda m: m['v_exit']))

    # band 1: the large-chamber limit must approach the constant-pressure ceiling
    huge = work(P_MAX, 10.0)                     # 10 m3 of chamber
    ceiling = P_MAX * AREA * STROKE

    # band 5 and 6: commanding velocity by charge pressure
    v0 = selected['chamber_l'] / 1e3
    cmd = [shot(f * P_MAX, v0) for f in (0.3, 0.4, 0.5, 0.6, 0.7, 0.85, 1.0)]
    monotonic = all(cmd[i]['v_exit'] <= cmd[i + 1]['v_exit'] + 1e-12
                    for i in range(len(cmd) - 1))
    print("\ncommanding velocity by charge pressure:")
    for c in cmd:
        print(f"  {c['p0_bar']:6.1f} bar -> {c['v_exit']:6.2f} m/s")
    base = shot(P_MAX, v0)['v_exit']
    hi = shot(1.01 * P_MAX, v0)['v_exit']
    prec = abs(hi - base) / base * 100.0

    # bands 7 and 8: the prediction
    charge_mbarL = (P_MAX / 100.0) * (v0 * 1e3)
    leak_allow = 0.01 * charge_mbarL / 1200.0
    friction_allow = selected['work_J'] * (1 - 0.95 ** 2) / STROKE

    bands = [
        ('1', 'large-chamber limit approaches p0*A*L within 1 %',
         f"{huge:.0f} against {ceiling:.0f} J",
         abs(huge - ceiling) / ceiling <= 0.01),
        ('2', f'selected point >= 30 m/s at <= {G_CAP:.0f} g',
         f"{selected['v_exit']:.2f} m/s at {selected['a_peak_g']:.2f} g",
         selected['v_exit'] >= 30.0 and selected['a_peak_g'] <= G_CAP + 1e-6),
        ('3', f'total store <= {BUDGET_KG:.2f} kg',
         f"{selected['total_kg']:.2f} kg", selected['total_kg'] <= BUDGET_KG),
        ('4', 'the twelve-shot reservoir keeps band 3',
         f"{selected['reservoir_l']:.1f} L, {selected['gas_kg']:.2f} kg of gas",
         selected['total_kg'] <= BUDGET_KG),
        ('5', 'charge pressure spans 20 -> 30 m/s monotonically',
         f"{cmd[0]['v_exit']:.1f} -> {cmd[-1]['v_exit']:.1f} m/s, monotonic {monotonic}",
         monotonic and cmd[0]['v_exit'] <= 20.0 and cmd[-1]['v_exit'] >= 30.0),
        ('6', '+/-1 % charge pressure gives <= 1 % velocity error',
         f"{prec:.3f} %", prec <= 1.0),
        ('7', 'permissible leak >= 1e-4 mbar.L/s (the prediction)',
         f"{leak_allow:.4g} mbar.L/s", leak_allow >= 1e-4),
        ('8', 'friction budget >= 20 N for <= 5 % velocity loss',
         f"{friction_allow:.1f} N", friction_allow >= 20.0),
    ]
    print("\nbands:")
    for n, name, detail, ok in bands:
        print(f"  band {n}: {'PASS' if ok else 'FAIL'}  {name}\n            {detail}")

    out = dict(analysis='A41', bands_declared_commit='3d61bab',
               note='ideal gas, adiabatic closed expansion, vented residual. No gas recovery, '
                    'no temperature effect on charge, no fill-time check against the indexing '
                    'window, no valve/seal/fill-circuit design, A34 release residual unchecked. '
                    'Every omission is optimistic.',
               p_charge_max_Pa=P_MAX, constant_pressure_ceiling_J=ceiling,
               budget_kg=BUDGET_KG, sweep=sweep, selected=selected,
               command_sweep=cmd, precision_pct_per_pct=prec,
               leak_allow_mbarL_s=leak_allow, friction_allow_N=friction_allow,
               bands=[dict(band=n, name=nm, detail=d, pass_=ok)
                      for n, nm, d, ok in bands])
    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, 'precharged.json')
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2, default=float)
        fh.write('\n')
    print(f"\nwrote {path}")


if __name__ == '__main__':
    main()
