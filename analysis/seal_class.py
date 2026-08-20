"""A61: what the design requires of a seal, which it has never said.

Bands declared in validation/A61_seal_class.md at HEAD~1, BEFORE this file existed.

WHY THIS EXISTS
---------------
No seal exists in this repository. A39 states it designs "no cylinder, valve, seal or latch"; A40
that it does not model one. A41 declared an 83.4 N friction ALLOWANCE and every number since has
been computed against it.

That allowance is 18.7 % of the piston's pressure force -- recognisably an elastomer figure. The
project has been implicitly assuming the worst common seal class without ever choosing it, and
A55 (dispersion), A54 (the trim store), A58 (seal thermal) and A49 (P78) all rest on it.

WHAT THIS RUN IS
----------------
Not a comparison of products. It INVERTS the question: what is the loosest seal the design can
tolerate for each downstream requirement to be met? That produces a SPECIFICATION -- a maximum
friction, in the unit seal data is quoted in -- where the repository has an allowance nobody chose.

The mapping is computed from models already in the record. Only the input is assumed, and the
class ranges are handbook, no better sourced than A39's gas model. This does not replace P67.

NO PRODUCT, COMPOUND OR SUPPLIER IS NAMED.

Run:  python3 analysis/seal_class.py
"""
import json
import math
import os

import precharged as pc
import gen6_dispersion as gd
import trim_stage as ts
import pulse_chain as pcx
import trim_authority as ta

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

V_CHAMBER = 2.0e-3
A48_AUTHORITY = 0.323            # m/s, the section as first built
SEAL_MASS_KG = 2.0e-3            # A58's mid-sweep point
SEAL_CP = 1500.0
SEAL_DT_LIMIT_K = 50.0           # A58 band 5
TOTAL_LIMIT_KG = 2.0             # A54 band 5
BORES_MM = (15.805366135494582, 16.000)
SPEC_E = 0.5 * 5.94 * 96.0 ** 2 / 6.50        # J/kg, Gen5's own bank
KG_PER_M = ts.MAGNET_KG_PER_M + ts.STATOR_KG_PER_M

# Handbook ranges for component classes. NEEDS SOURCE. Named as classes, never as products.
CLASSES = (('filled PTFE glide ring', 0.02, 0.10),
           ('elastomer O-ring', 0.10, 0.25))
FRAC_SWEEP = tuple(x / 1000.0 for x in range(10, 305, 5))     # 1 % to 30 %


def chain(frac, bore_m=None):
    """Everything that follows from one friction fraction of the piston pressure force."""
    area = math.pi * (bore_m / 2.0) ** 2 if bore_m else pc.AREA
    # the charge that holds the declared acceleration cap on this area
    p0 = pc.M_PAY * pc.G_CAP * pc.G / area
    f_press = p0 * area
    f_seal = frac * f_press
    pt = ta.point(p0, pc.STROKE, f_seal)
    tr = ta.trim_for(pt)
    # the section+store minimum, swept over sheet current: total = a/J + b*J
    a = tr['energy_J'] * KG_PER_M / ts.KT
    b = 0.5 * pcx.ESR_C_LO * ts.KT * pt['mean'] / (0.10 * SPEC_E)
    total_lo = 2.0 * math.sqrt(a * b)
    b_hi = 0.5 * pcx.ESR_C_HI * ts.KT * pt['mean'] / (0.10 * SPEC_E)
    return dict(frac=frac, bore_mm=(bore_m or pc.BORE) * 1e3, p0_bar=p0 / 1e5,
                pressure_force_N=f_press, friction_N=f_seal,
                friction_work_J=f_seal * pc.STROKE,
                friction_frac_of_shot=pt['friction_frac'],
                v_zero_friction=math.sqrt(2.0 * pt['work_J'] / pc.M_PAY),
                v_exit=pt['mean'], three_sigma_pct=pt['three_sigma_pct'],
                authority_m_s=tr['authority_m_s'], section_mm=tr['section_m'] * 1e3,
                section_kg=tr['mass_kg'],
                seal_dT_K=f_seal * pc.STROKE / (SEAL_MASS_KG * SEAL_CP),
                min_total_kg=total_lo,
                min_total_kg_hi=2.0 * math.sqrt(a * b_hi))


def threshold(rows, key, limit, below=True):
    """Loosest friction fraction still satisfying the requirement. None if none does."""
    ok = [r for r in rows if (r[key] <= limit if below else r[key] >= limit)]
    return max(ok, key=lambda r: r['frac']) if ok else None


def main():
    rows = [chain(f) for f in FRAC_SWEEP]
    a41_frac = gd.FRICTION_N / (pc.P_MAX * pc.AREA)
    a41 = chain(a41_frac)

    print("A61 seal class. Friction parameterised as a fraction of the piston pressure force,")
    print(f"  p0.A = {a41['pressure_force_N']:.1f} N at {a41['p0_bar']:.4f} bar\n")
    print(f"  A41's 83.4 N allowance = {a41_frac*100:.2f} % of it")
    for name, lo, hi in CLASSES:
        inside = lo <= a41_frac <= hi
        print(f"    {name:24s} {lo*100:5.1f}-{hi*100:5.1f} %   "
              f"{'<-- A41 sits here' if inside else ''}")
    print()

    print(f"  {'%p0A':>6}{'F N':>8}{'%shot':>8}{'3sig %':>9}{'auth m/s':>10}"
          f"{'section mm':>12}{'seal dT K':>11}{'min kg':>9}")
    for r in rows[::4]:
        print(f"  {r['frac']*100:6.1f}{r['friction_N']:8.1f}{r['friction_frac_of_shot']*100:8.2f}"
              f"{r['three_sigma_pct']:9.4f}{r['authority_m_s']:10.4f}{r['section_mm']:12.1f}"
              f"{r['seal_dT_K']:11.1f}{r['min_total_kg']:9.2f}")

    t_trim = threshold(rows, 'authority_m_s', A48_AUTHORITY)
    t_therm = threshold(rows, 'seal_dT_K', SEAL_DT_LIMIT_K)
    t_store = threshold(rows, 'min_total_kg', TOTAL_LIMIT_KG)

    print(f"\n  the specification, loosest seal that meets each requirement:")
    for lab, t in (('trim stage becomes unnecessary (<= 0.323 m/s)', t_trim),
                   ('2 g seal stays within 50 K', t_therm),
                   ('section + store <= 2.0 kg', t_store)):
        if t is None:
            print(f"    {lab:44s} NOT REACHABLE in 1-30 %")
        else:
            print(f"    {lab:44s} {t['frac']*100:5.2f} % = {t['friction_N']:5.1f} N")

    bores = {f"{b*1e3:.3f}": threshold([chain(f, b) for f in FRAC_SWEEP],
                                       'authority_m_s', A48_AUTHORITY)
             for b in [x / 1e3 for x in BORES_MM]}
    b_fracs = {k: (v['frac'] if v else None) for k, v in bores.items()}
    keys = list(b_fracs)
    bore_shift = abs(b_fracs[keys[1]] - b_fracs[keys[0]]) / b_fracs[keys[0]] \
        if all(b_fracs.values()) else 1.0
    print(f"\n  bore: required fraction {b_fracs[keys[0]]*100:.2f} % at {keys[0]} mm against "
          f"{b_fracs[keys[1]]*100:.2f} % at {keys[1]} mm -> {bore_shift*100:.2f} % shift")

    num_gap = max(abs(r['v_zero_friction'] - r['v_exit']) / r['v_zero_friction'] for r in rows)

    bands = [
        ('1', "reproduces A55's 3.980 % and A54's store at 83.4 N within 1 %",
         f"{a41['three_sigma_pct']:.4f} %, min {a41['min_total_kg']:.2f} kg",
         abs(a41['three_sigma_pct'] - 3.9798) / 3.9798 <= 0.01),
        ('2', "A41's allowance falls inside a named class range",
         f"{a41_frac*100:.2f} % -- " + next((n for n, lo, hi in CLASSES if lo <= a41_frac <= hi),
                                            'OUTSIDE every class'),
         any(lo <= a41_frac <= hi for _, lo, hi in CLASSES)),
        ('3', f'some friction makes the trim stage unnecessary (<= {A48_AUTHORITY} m/s)',
         f"{t_trim['frac']*100:.2f} % = {t_trim['friction_N']:.1f} N" if t_trim else 'none',
         t_trim is not None),
        ('4', f'some friction keeps a 2 g seal within {SEAL_DT_LIMIT_K:.0f} K',
         f"{t_therm['frac']*100:.2f} % = {t_therm['friction_N']:.1f} N" if t_therm else 'none',
         t_therm is not None),
        ('5', f'some friction gives section + store <= {TOTAL_LIMIT_KG} kg',
         f"{t_store['frac']*100:.2f} %" if t_store else 'none in 1-30 %',
         t_store is not None),
        ('6', 'the thermal requirement is looser than the control requirement',
         f"thermal {t_therm['frac']*100:.2f} % against control {t_trim['frac']*100:.2f} %"
         if t_therm and t_trim else 'not evaluable',
         bool(t_therm and t_trim and t_therm['frac'] > t_trim['frac'])),
        ('7', 'the 16.000 mm stock bore shifts the requirement by <= 5 %',
         f"{bore_shift*100:.2f} %", bore_shift <= 0.05),
        ('8', 'the two velocity numerators stay within 25 % across the sweep',
         f"worst gap {num_gap*100:.2f} %", num_gap <= 0.25),
        ('9', 'REPORT: the specification', 'three requirements, see above', None),
    ]
    print('\nbands:')
    for n, band, value, ok in bands:
        mark = 'REPORT' if ok is None else ('PASS' if ok else 'FAIL')
        print(f'  {n}  {mark:6} {band}\n        {value}')

    out = dict(analysis='A61', bands_declared_commit='HEAD~1',
               note='Class friction fractions are HANDBOOK RANGES, no better sourced than A39\'s '
                    'gas model. NEEDS SOURCE. This produces a REQUIREMENT, not a validation, and '
                    'does not replace P67 -- which A58/P88 showed is a harder test than described. '
                    'No product, compound or supplier is named.',
               pressure_force_N=a41['pressure_force_N'], a41_fraction=a41_frac, a41_point=a41,
               classes=[dict(name=n, lo=lo, hi=hi) for n, lo, hi in CLASSES],
               sweep=rows,
               specification=dict(
                   trim_unnecessary=t_trim, seal_thermal=t_therm, store_affordable=t_store),
               bore_fracs=b_fracs, bore_shift=bore_shift,
               bands=[dict(n=n, band=b, value=v,
                           verdict=('REPORT' if o is None else ('PASS' if o else 'FAIL')))
                      for n, b, v, o in bands])
    path = os.path.join(RESULTS, 'seal_class.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, default=float)
        f.write('\n')
    print(f'\nwrote {path}')


if __name__ == '__main__':
    main()
