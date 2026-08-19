"""A54: weighing the pulse chain that feeds the trim stage. ADR-033's own first falsifier.

Bands declared in validation/A54_pulse_chain.md at HEAD~1, BEFORE this file existed.

WHY THIS EXISTS
---------------
P77. ADR-033 adopted the trim stage with its store unweighed and named that as falsifier 1 on the
same day: "pulse hardware scales with current, not energy, and nothing has weighed it. This is the
falsifier most likely to fire, and it is being adopted before it is answered."

A55 has since resized the section, so the requirement is 136.59 J at 28606 W into a 1.2328 kg
section rather than 37.7 J into 0.340 kg.

THE THING ADR-033 SAID WOULD DECIDE IT
--------------------------------------
ADR-032 deleted a chain peaking at 30.7 kW and 319.5 A. The resized trim asks for 28606 W. Force
per metre is fixed by A2's thrust constant and A1's sheet current, so a longer correction takes
LONGER rather than HARDER: the energy grows and the current does not. A store is sized by the
current.

NOTHING HERE IS INVENTED
------------------------
A10 established that ESR x C is roughly constant within a cell technology and bracketed it at
0.69-1.10 s. mass_properties.py carries one 32-cell 190 F string -- 5.94 F at 96 V -- at 6.50 kg.
That is a mass, a capacitance and an ESR bracket, all already in the record.

The switch and the conductors are NOT priced and no figure for either exists in this repository,
so every store mass below is a LOWER BOUND.

Run:  python3 analysis/pulse_chain.py
"""
import json
import math
import os

import precharged as pc
import trim_stage as ts

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

V_BUS = 96.0                     # sizing.py::capacitor_sizing
GEN5_PEAK_W = 30674.0            # 319.539 A x 96 V, motor_results.json I_peak
GEN5_PEAK_A = 319.539
STRING_F, STRING_KG, STRING_V = 5.94, 6.50, 96.0     # mass_properties.py, sizing.py
ESR_C_LO, ESR_C_HI = 0.69, 1.10                       # A10's bracket, seconds
ESR_LOSS_FRAC = 0.10             # the ESR may dissipate this share of the delivered energy
SHEET_SWEEP = tuple(range(10, 105, 5))                # kA/m
PER_SAT_BASE = 1.296             # A49/ADR-034, before the trim section


def requirement():
    """Energy, peak power and section, read back from A55 rather than restated."""
    d = json.load(open(os.path.join(RESULTS, 'trim_authority.json'), encoding='utf-8'))
    t = d['trim_adopted']
    return dict(energy_J=t['energy_J'], peak_W=t['peak_W'], section_m=t['section_m'],
                authority_m_s=t['authority_m_s'], mass_kg=t['mass_kg'],
                v_exit=d['adopted_point']['mean'])


def store_for_power(peak_W, esr_c, v_bus=V_BUS, loss_frac=ESR_LOSS_FRAC):
    """An EDLC bank sized so its ESR dissipates at most loss_frac of the delivered energy.

    Over a pulse of duration t = E/P at current I = P/V, the ESR burns I^2*R*t. Setting that
    to loss_frac*E gives R <= loss_frac * V^2 / P -- the energy cancels, which is the whole
    point: the store is sized by POWER, not by how much energy it holds.

    ESR x C is constant within the technology (A10), so the required capacitance follows.
    """
    r_max = loss_frac * v_bus ** 2 / peak_W
    c_needed = esr_c / r_max
    strings = c_needed / STRING_F
    return dict(esr_c_s=esr_c, r_max_ohm=r_max, C_F=c_needed, strings=strings,
                mass_kg=strings * STRING_KG,
                stored_J=0.5 * c_needed * v_bus ** 2,
                current_A=peak_W / v_bus)


def sweep_sheet(req):
    """Section mass and store mass against sheet current. Power ~ J, section ~ 1/J."""
    rows = []
    for kA_per_m in SHEET_SWEEP:
        force_per_m = ts.KT * (kA_per_m * 1e3) / 1e3
        section_m = req['energy_J'] / force_per_m
        peak_W = force_per_m * (req['v_exit'] + req['authority_m_s'])
        sect_kg = section_m * (ts.MAGNET_KG_PER_M + ts.STATOR_KG_PER_M)
        st_lo = store_for_power(peak_W, ESR_C_LO)
        st_hi = store_for_power(peak_W, ESR_C_HI)
        rows.append(dict(sheet_kA_per_m=kA_per_m, force_per_m_N=force_per_m,
                         section_m=section_m, section_kg=sect_kg, peak_W=peak_W,
                         current_A=peak_W / V_BUS,
                         store_kg_lo=st_lo['mass_kg'], store_kg_hi=st_hi['mass_kg'],
                         total_kg_lo=sect_kg + st_lo['mass_kg'],
                         total_kg_hi=sect_kg + st_hi['mass_kg'],
                         pct_stroke=section_m / pc.STROKE * 100.0))
    return rows


def main():
    req = requirement()
    print(f"A54 pulse chain. Requirement from A55: {req['energy_J']:.2f} J, "
          f"{req['peak_W']:.0f} W, {req['section_m']*1e3:.2f} mm, {req['mass_kg']:.4f} kg\n")

    pulse_s = req['energy_J'] / req['peak_W']
    cur = req['peak_W'] / V_BUS
    print(f"  at the {V_BUS:.0f} V bus: {cur:.1f} A over {pulse_s*1e3:.2f} ms")
    print(f"  against the chain ADR-032 deleted: {GEN5_PEAK_W:.0f} W, {GEN5_PEAK_A:.1f} A")
    print(f"  the trim asks for {req['peak_W']/GEN5_PEAK_W*100:.1f} % of its power and "
          f"{cur/GEN5_PEAK_A*100:.1f} % of its current\n")

    lo = store_for_power(req['peak_W'], ESR_C_LO)
    hi = store_for_power(req['peak_W'], ESR_C_HI)
    print(f"  EDLC store at A1's 90 kA/m, ESR budget {ESR_LOSS_FRAC*100:.0f} % of the shot:")
    print(f"    ESR must be <= {lo['r_max_ohm']*1e3:.2f} mohm")
    print(f"    C needed {lo['C_F']:.1f} to {hi['C_F']:.1f} F  "
          f"({lo['strings']:.2f} to {hi['strings']:.2f} strings)")
    print(f"    mass {lo['mass_kg']:.2f} to {hi['mass_kg']:.2f} kg, "
          f"against the {req['mass_kg']:.3f} kg section it feeds "
          f"({lo['mass_kg']/req['mass_kg']:.1f}x to {hi['mass_kg']/req['mass_kg']:.1f}x)")
    print(f"    it would hold {lo['stored_J']/1e3:.1f} to {hi['stored_J']/1e3:.1f} kJ "
          f"for a {req['energy_J']:.1f} J correction "
          f"({lo['stored_J']/req['energy_J']:.0f}x to {hi['stored_J']/req['energy_J']:.0f}x)\n")

    spec_p = req['peak_W'] / req['mass_kg']
    gen5_spec_p = GEN5_PEAK_W / STRING_KG
    print(f"  to fit inside the section's own mass a store needs "
          f"{spec_p/1e3:.2f} kW/kg and {req['energy_J']/req['mass_kg']:.1f} J/kg")
    print(f"  Gen5's own bank achieves {gen5_spec_p/1e3:.2f} kW/kg -> "
          f"{spec_p/gen5_spec_p:.2f}x required\n")

    rows = sweep_sheet(req)
    print(f"  {'kA/m':>6}{'force N/m':>11}{'section mm':>12}{'% stroke':>10}"
          f"{'peak W':>10}{'A':>7}{'sect kg':>9}{'store kg':>18}{'total kg':>18}")
    for r in rows:
        print(f"  {r['sheet_kA_per_m']:6d}{r['force_per_m_N']:11.1f}{r['section_m']*1e3:12.1f}"
              f"{r['pct_stroke']:10.3f}{r['peak_W']:10.0f}{r['current_A']:7.0f}"
              f"{r['section_kg']:9.3f}"
              f"{r['store_kg_lo']:9.3f}-{r['store_kg_hi']:<8.3f}"
              f"{r['total_kg_lo']:9.3f}-{r['total_kg_hi']:<8.3f}")

    best_lo = min(rows, key=lambda r: r['total_kg_lo'])
    best_hi = min(rows, key=lambda r: r['total_kg_hi'])
    under2 = [r for r in rows if r['total_kg_hi'] <= 2.0]
    per_sat = PER_SAT_BASE + best_hi['total_kg_hi'] / pc.N_MANIFEST

    print(f"\n  minimum at the optimistic end of A10's bracket: "
          f"{best_lo['sheet_kA_per_m']} kA/m, {best_lo['total_kg_lo']:.3f} kg")
    print(f"  minimum at the pessimistic end:                  "
          f"{best_hi['sheet_kA_per_m']} kA/m, {best_hi['total_kg_hi']:.3f} kg")
    print(f"  sheet currents where the pessimistic total is <= 2.0 kg: "
          f"{[r['sheet_kA_per_m'] for r in under2] or 'none'}")

    bands = [
        ('1', 'requirement reproduces A55 within 0.1 %',
         f"{req['energy_J']:.2f} J, {req['peak_W']:.0f} W, {req['section_m']*1e3:.2f} mm",
         abs(req['energy_J'] - 136.59) / 136.59 < 1e-3
         and abs(req['peak_W'] - 28606) / 28606 < 1e-3
         and abs(req['section_m'] * 1e3 - 144.01) / 144.01 < 1e-3),
        ('2', f'peak power <= 50 % of the {GEN5_PEAK_W/1e3:.1f} kW chain ADR-032 deleted',
         f"{req['peak_W']/GEN5_PEAK_W*100:.1f} %", req['peak_W'] <= 0.5 * GEN5_PEAK_W),
        ('3', 'EDLC store <= the section it feeds',
         f"{lo['mass_kg']:.2f}-{hi['mass_kg']:.2f} kg against {req['mass_kg']:.3f} kg",
         hi['mass_kg'] <= req['mass_kg']),
        ('4', f'required specific power <= {gen5_spec_p/1e3:.2f} kW/kg',
         f"{spec_p/1e3:.2f} kW/kg, {spec_p/gen5_spec_p:.2f}x", spec_p <= gen5_spec_p),
        ('5', 'some sheet current gives section + store <= 2.0 kg',
         f"{[r['sheet_kA_per_m'] for r in under2] or 'none'}", bool(under2)),
        ('6', 'added mass per satellite at that point <= 2.0 kg',
         f"{per_sat:.4f} kg", per_sat <= 2.0),
        ('7', 'the sized store holds <= 10x the correction energy',
         f"{lo['stored_J']/req['energy_J']:.0f}x to {hi['stored_J']/req['energy_J']:.0f}x",
         hi['stored_J'] <= 10 * req['energy_J']),
        ('8', 'REPORT: section and store against sheet current',
         f"minimum {best_hi['total_kg_hi']:.3f} kg at {best_hi['sheet_kA_per_m']} kA/m", None),
    ]
    print('\nbands:')
    for n, band, value, ok in bands:
        mark = 'REPORT' if ok is None else ('PASS' if ok else 'FAIL')
        print(f'  {n}  {mark:6} {band}\n        {value}')

    out = dict(analysis='A54', bands_declared_commit='HEAD~1',
               note='EDLC route only. Switch and conductors NOT priced -- every store mass '
                    'here is a LOWER BOUND. NEEDS SOURCE: pulse switch and conductor mass at '
                    '300 A; specific power of a film capacitor bank at this pulse duration.',
               requirement=req, pulse_s=pulse_s, current_A=cur,
               gen5_peak_W=GEN5_PEAK_W, gen5_peak_A=GEN5_PEAK_A,
               store_optimistic=lo, store_pessimistic=hi,
               required_specific_power_W_per_kg=spec_p,
               gen5_specific_power_W_per_kg=gen5_spec_p,
               sheet_sweep=rows, minimum_optimistic=best_lo, minimum_pessimistic=best_hi,
               under_2kg_kA_per_m=[r['sheet_kA_per_m'] for r in under2],
               added_mass_per_satellite_kg=per_sat,
               bands=[dict(n=n, band=b, value=v,
                           verdict=('REPORT' if o is None else ('PASS' if o else 'FAIL')))
                      for n, b, v, o in bands])
    path = os.path.join(RESULTS, 'pulse_chain.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, default=float)
        f.write('\n')
    print(f'\nwrote {path}')


if __name__ == '__main__':
    main()
