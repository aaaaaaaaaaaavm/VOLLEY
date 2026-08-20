"""A56: the reservoir at the charge pressure ADR-034 adopted. P82.

Bands declared in validation/A56_reservoir_resized.md at HEAD~1, BEFORE this file existed.

WHY THIS EXISTS
---------------
ADR-034 dropped the charge pressure 50 -> 22.7258 bar and cut gas per shot by 54.55 %. The
reservoir did not move: parameters.json still carries 9.55 L, which A43 sized around 50 bar
refills. And the store mass ADR-034 quotes is A49's gas-ratio SCALING of A43's 5.38 kg, not a
sized store -- the ADR says so in its own falsifier 2.

WHAT A43 ESTABLISHED, AND THE QUESTION IT LEAVES
------------------------------------------------
A43's finding was not a volume. It was that the bottle does not warm back up: conduction through
stagnant nitrogen gives 17460 s against a 1200 s cadence, so the NO-RELAXATION figure is the
physically right end rather than merely the conservative one.

That argument is about the gas, not the pressure. But the time constant scales with the
reservoir's own size and the reservoir is about to get smaller, and a smaller bottle relaxes
faster. Whether it relaxes fast enough is band 4 and it is not obvious in advance.

THE SEARCH FLOOR WAS BINDING
----------------------------
reservoir_thermal.required() searches upward from 4.0 L, set when the answer was around 9 L. At
the new charge pressure it returns 4.0 L -- the floor itself. A search cannot see below its own
starting point, so this run lowers the floor and reports that it was binding (band 2).

Everything else is A43's model, imported rather than restated.

Run:  python3 analysis/reservoir_resized.py
"""
import json
import math
import os

import fill_window as fw
import reservoir_thermal as rt

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

FLOOR_L = 0.5e-3                  # A43's floor was 4.0e-3 and is binding at the new point
STEP_L = 0.01e-3                  # finer than A43's 0.05 L, since the answer is smaller
A43_NO_RELAX_L = 9.55             # the figure in parameters.json, from A43
P_SWEEP_BAR = (15.0, 20.0, 22.7258, 25.0, 30.0, 40.0, 50.0)
H_NO_RELAX = 0.0                  # A43's no-relaxation end: the one parameters.json carries
CHAMBER_KG, HARDWARE_KG = fw.CHAMBER_KG, fw.HARDWARE_KG
ADDED_BASE_KG = fw.ADDED_BASE_KG
PER_SAT_TUBE_KG = 1.1404          # A49's tube, carried so the per-satellite figure is comparable


def required(orifice_m2, h, p_charge, floor=FLOOR_L, step=STEP_L, vmax=rt.V_SEARCH_MAX):
    """A43's search, with the charge pressure explicit and a floor that is not binding."""
    old = fw.P_CHARGE
    fw.P_CHARGE = p_charge
    try:
        v = floor
        while v < vmax:
            _, failed, _ = rt.sequence(v, orifice_m2, h)
            if failed is None:
                return v
            v += step
        return None
    finally:
        fw.P_CHARGE = old


def at_pressure(p_charge, orifice_m2, h=H_NO_RELAX):
    """Required reservoir, the sequence it runs, and what the store then weighs."""
    v_res = required(orifice_m2, h, p_charge)
    if v_res is None:
        return None
    old = fw.P_CHARGE
    fw.P_CHARGE = p_charge
    try:
        seq, failed, t_min = rt.sequence(v_res, orifice_m2, h)
    finally:
        fw.P_CHARGE = old
    m_res = fw.P_STORE * v_res / (fw.R_GAS * fw.T0)
    vessel = fw.P_STORE * v_res / (fw.PV_OVER_W * 9.81)
    gas = v_res * fw.RHO_STORE
    store = CHAMBER_KG + vessel + gas + HARDWARE_KG
    tau_s = rt.tau(m_res, v_res, rt.conduction_h(v_res))
    return dict(p_charge_bar=p_charge / 1e5, reservoir_l=v_res * 1e3,
                vessel_kg=vessel, gas_kg=gas, chamber_kg=CHAMBER_KG,
                hardware_kg=HARDWARE_KG, store_kg=store,
                per_satellite_kg=(ADDED_BASE_KG + store + PER_SAT_TUBE_KG) / fw.N_MANIFEST,
                conduction_tau_s=tau_s, tau_over_cadence=tau_s / fw.CADENCE_S,
                t_min_K=t_min, last_fill_s=seq[-1]['fill_s'],
                shots=len(seq), failed=failed)


def main():
    orifice = math.pi * (1.0 / 2e3) ** 2          # A42's 1 mm orifice
    print(f"A56 reservoir resized. A43's floor was {4.0:.1f} L; this run searches from "
          f"{FLOOR_L*1e3:.2f} L in {STEP_L*1e3:.2f} L steps\n")

    a43 = at_pressure(50e5, orifice)
    now = at_pressure(fw.P_CHARGE, orifice)
    floor_a43 = required(orifice, H_NO_RELAX, fw.P_CHARGE, floor=4.0e-3, step=0.05e-3)

    print(f"{'':>26}{'A43, 50 bar':>14}{'adopted':>14}")
    for lab, key, fmt in (('reservoir L', 'reservoir_l', '14.3f'),
                          ('vessel kg', 'vessel_kg', '14.4f'),
                          ('gas kg', 'gas_kg', '14.4f'),
                          ('store kg', 'store_kg', '14.4f'),
                          ('per satellite kg', 'per_satellite_kg', '14.4f'),
                          ('conduction tau s', 'conduction_tau_s', '14.0f'),
                          ('tau / cadence', 'tau_over_cadence', '14.2f'),
                          ('min reservoir T K', 't_min_K', '14.1f'),
                          ('last fill s', 'last_fill_s', '14.3f')):
        print(f"  {lab:>24}{format(a43[key], fmt)}{format(now[key], fmt)}")
    print(f"\n  A43's 4.0 L floor at the adopted pressure returns "
          f"{floor_a43*1e3 if floor_a43 else float('nan'):.2f} L -- "
          f"{'BINDING' if floor_a43 and abs(floor_a43 - 4.0e-3) < 1e-9 else 'not binding'}")

    print(f"\nband 9, against charge pressure:")
    print(f"  {'bar':>10}{'reservoir L':>13}{'store kg':>10}{'per sat kg':>12}"
          f"{'tau/cadence':>13}{'min T K':>9}")
    sweep = []
    for pb in P_SWEEP_BAR:
        r = at_pressure(pb * 1e5, orifice)
        sweep.append(r)
        print(f"  {pb:10.4f}{r['reservoir_l']:13.3f}{r['store_kg']:10.4f}"
              f"{r['per_satellite_kg']:12.4f}{r['tau_over_cadence']:13.2f}{r['t_min_K']:9.1f}")

    bands = [
        ('1', "reproduces A43's 9.55 L at 50 bar within 2 %",
         f"{a43['reservoir_l']:.3f} L",
         abs(a43['reservoir_l'] - A43_NO_RELAX_L) / A43_NO_RELAX_L <= 0.02),
        ('2', 'the search floor is below the resolved answer at both pressures',
         f"floor {FLOOR_L*1e3:.2f} L against {now['reservoir_l']:.3f} and "
         f"{a43['reservoir_l']:.3f} L",
         FLOOR_L * 1e3 < min(now['reservoir_l'], a43['reservoir_l'])),
        ('3', 'required reservoir at 22.7258 bar <= 6.0 L',
         f"{now['reservoir_l']:.3f} L", now['reservoir_l'] <= 6.0),
        ('4', 'conduction tau still exceeds the 1200 s cadence by >= 5x',
         f"{now['tau_over_cadence']:.2f}x", now['tau_over_cadence'] >= 5.0),
        ('5', 'sized store <= the 4.10 kg ADR-034 quotes',
         f"{now['store_kg']:.4f} kg", now['store_kg'] <= 4.10),
        ('6', 'added mass per satellite <= 2.0 kg',
         f"{now['per_satellite_kg']:.4f} kg", now['per_satellite_kg'] <= 2.0),
        ('7', 'twelve charges complete, last fill inside the 10 s window',
         f"{now['shots']} shots, last fill {now['last_fill_s']:.3f} s",
         now['failed'] is None and now['shots'] == fw.N_MANIFEST
         and now['last_fill_s'] <= fw.WINDOW_S),
        ('8', 'minimum reservoir temperature above the 150 K floor',
         f"{now['t_min_K']:.1f} K", now['t_min_K'] > rt.T_FLOOR_K),
        ('9', 'REPORT: reservoir and store against charge pressure',
         f"{len(sweep)} points, {sweep[0]['reservoir_l']:.2f} to "
         f"{sweep[-1]['reservoir_l']:.2f} L", None),
    ]
    print('\nbands:')
    for n, band, value, ok in bands:
        mark = 'REPORT' if ok is None else ('PASS' if ok else 'FAIL')
        print(f'  {n}  {mark:6} {band}\n        {value}')

    out = dict(analysis='A56', bands_declared_commit='HEAD~1',
               note="A43's model imported unchanged: conduction-only, lumped reservoir, wall at "
                    "the structure temperature, ideal gas. Store uses A39's PV/W = 15000 m, which "
                    "A39's own run sheet says underestimates real 1.7 L / 200 bar vessels 4-6x -- "
                    "the absolute store mass is soft, the ratio between two pressures is firmer.",
               search_floor_l=FLOOR_L * 1e3, a43_floor_binding=bool(
                   floor_a43 and abs(floor_a43 - 4.0e-3) < 1e-9),
               a43_point=a43, adopted_point=now, pressure_sweep=sweep,
               bands=[dict(n=n, band=b, value=v,
                           verdict=('REPORT' if o is None else ('PASS' if o else 'FAIL')))
                      for n, b, v, o in bands])
    path = os.path.join(RESULTS, 'reservoir_resized.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, default=float)
        f.write('\n')
    print(f'\nwrote {path}')


if __name__ == '__main__':
    main()
