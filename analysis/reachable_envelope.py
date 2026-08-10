"""A20: the delivery envelope of a VOLLEY-equipped spent stage, against a host delta-v budget.

Bands declared in validation/A20_reachable_envelope.md at 881c260, before this file existed.

THE QUESTION
------------
docs/CONCEPT.md claims a spent stage carrying VOLLEY can reposition between altitude shells on
its own RCS and deliver satellites to each. That claim contains a budget nobody has stated,
because POEM-class propellant and control authority are undisclosed (E5). So this is parametric
in the one missing number: given a host delta-v budget, what can twelve satellites reach?

THREE MECHANISMS, NOT INTERCHANGEABLE
-------------------------------------
    host repositioning   costs RCS propellant     -> altitude shells
    VOLLEY's shot        costs 2.56 kJ of power   -> along-track velocity difference
    differential J2      costs nothing            -> RAAN separation over the campaign

Plane change is EXCLUDED and is not reported as reachable at any budget. Band 4 computes the
trade anyway, so the exclusion is demonstrated rather than asserted.

Run:  python3 analysis/reachable_envelope.py
"""
import json
import math
import os

import astro

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

DV_BUDGETS = (0.0, 25.0, 50.0, 100.0, 200.0, 400.0)   # m/s of host RCS
BASE_ALT_KM = 450.0
SHELL_STEP_KM = 50.0
N_SATS = 12
CAMPAIGN_DAYS = 90.0
INC_DEG = 51.6


def hohmann_dv(alt1_km, alt2_km):
    """Two-burn transfer between circular orbits. Total delta-v, both burns."""
    r1, r2 = astro.RE + alt1_km * 1e3, astro.RE + alt2_km * 1e3
    v1, v2 = math.sqrt(astro.MU / r1), math.sqrt(astro.MU / r2)
    a_t = 0.5 * (r1 + r2)
    dv1 = abs(math.sqrt(astro.MU * (2 / r1 - 1 / a_t)) - v1)
    dv2 = abs(v2 - math.sqrt(astro.MU * (2 / r2 - 1 / a_t)))
    return dv1 + dv2


def shells_reachable(budget, step_km=SHELL_STEP_KM):
    """Shells visited by walking outward from the base altitude until the budget runs out.

    One-way: the stage does not return, it deorbits at the end. Each leg is charged in full.
    """
    shells, spent, alt = [BASE_ALT_KM], 0.0, BASE_ALT_KM
    while True:
        leg = hohmann_dv(alt, alt + step_km)
        if spent + leg > budget:
            break
        spent += leg
        alt += step_km
        shells.append(alt)
    return shells, spent


def plane_change_deg(budget, alt_km=BASE_ALT_KM):
    """Inclination the whole budget would buy if spent on plane change instead. Band 4."""
    v = math.sqrt(astro.MU / (astro.RE + alt_km * 1e3))
    return math.degrees(2.0 * math.asin(min(1.0, budget / (2.0 * v))))


def raan_spread_deg(shells, dv_shot, days=CAMPAIGN_DAYS):
    """RAAN spread from differential nodal regression across the delivered fleet.

    Nodes regress as a^-3.5 cos(i), so satellites left at different semi-major axes separate
    in RAAN for free. Uses astro.py's own J2 rate rather than restating it.
    """
    def raan_rate(a, e, inc_deg):
        n = math.sqrt(astro.MU / a ** 3)
        p = a * (1 - e * e)
        return -1.5 * n * astro.J2 * (astro.RE / p) ** 2 * math.cos(math.radians(inc_deg))

    rates = []
    for alt in shells:
        for sign in (+1, -1):          # prograde and retrograde shots at each shell
            a, e = astro.boosted_elements(alt * 1e3, sign * dv_shot)[:2]
            rates.append(raan_rate(a, e, INC_DEG))
    span = (max(rates) - min(rates)) * days * 86400.0
    return abs(math.degrees(span))


def altitude_extent_km(shells, dv_shot):
    """Highest apogee minus lowest perigee across the delivered fleet.

    astro.boosted_elements returns e = 1 - r0/a, which is NEGATIVE for a retrograde burn
    (a < r0). The two apsides a(1+e) and a(1-e) then arrive swapped, and binning them by
    formula rather than by magnitude puts retrograde perigees into the apogee list. That
    under-reported the extent by ~57 km on the first run of this script; take min and max of
    the pair instead of trusting the sign.
    """
    apo, per = [], []
    for alt in shells:
        for sign in (+1, -1):
            a, e = astro.boosted_elements(alt * 1e3, sign * dv_shot)[:2]
            r_hi, r_lo = max(a * (1 + e), a * (1 - e)), min(a * (1 + e), a * (1 - e))
            apo.append((r_hi - astro.RE) / 1e3)
            per.append((r_lo - astro.RE) / 1e3)
    return max(apo) - min(per)


def main():
    with open(os.path.join(RESULTS, 'motor_results.json'), encoding='utf-8') as f:
        dv_shot = json.load(f)['shot']['v_exit']

    leg50 = hohmann_dv(BASE_ALT_KM, BASE_ALT_KM + SHELL_STEP_KM)

    rows = []
    for budget in DV_BUDGETS:
        shells, spent = shells_reachable(budget)
        ext = altitude_extent_km(shells, dv_shot)
        raan = raan_spread_deg(shells, dv_shot)
        # Band 6: how much of the altitude extent is the host's doing rather than VOLLEY's?
        volley_only = altitude_extent_km([BASE_ALT_KM], dv_shot)
        host_frac = (ext - volley_only) / ext if ext else 0.0
        rows.append(dict(
            dv_budget_m_s=budget, shells=shells, n_shells=len(shells), dv_spent_m_s=spent,
            altitude_extent_km=ext, raan_spread_deg=raan,
            volley_only_extent_km=volley_only, host_fraction_of_extent=host_frac,
            inclination_if_spent_on_plane_deg=plane_change_deg(budget),
            sats_per_shell=N_SATS / len(shells)))

    at100 = next(r for r in rows if r['dv_budget_m_s'] == 100.0)
    at400 = next(r for r in rows if r['dv_budget_m_s'] == 400.0)
    at0 = next(r for r in rows if r['dv_budget_m_s'] == 0.0)

    bands = {
        '1_hohmann_50km': dict(value_m_s=leg50, band='10-20 m/s',
                               passed=10.0 <= leg50 <= 20.0),
        '2_shells_at_100': dict(value=at100['n_shells'], band='>= 4',
                                passed=at100['n_shells'] >= 4),
        '3_extent_at_100': dict(value_km=at100['altitude_extent_km'], band='>= 250 km',
                                passed=at100['altitude_extent_km'] >= 250.0),
        '4_inclination_at_400': dict(value_deg=at400['inclination_if_spent_on_plane_deg'],
                                     band='<= 3.5 deg',
                                     passed=at400['inclination_if_spent_on_plane_deg'] <= 3.5),
        '5_raan_at_zero_budget': dict(value_deg=at0['raan_spread_deg'], band='>= 5 deg',
                                      passed=at0['raan_spread_deg'] >= 5.0),
        '6_host_fraction_at_100': dict(value=at100['host_fraction_of_extent'],
                                       band='REPORT, no pass/fail', verdict='REPORT'),
    }

    print(f"A20 reachable envelope. VOLLEY shot {dv_shot:.3f} m/s, base {BASE_ALT_KM:.0f} km, "
          f"{CAMPAIGN_DAYS:.0f}-day campaign\n")
    print(f"  one 50 km Hohmann leg costs {leg50:.2f} m/s\n")
    print(f"  {'host dv':>9}{'shells':>8}{'spent':>9}{'alt extent':>12}"
          f"{'RAAN spread':>13}{'host frac':>11}{'incl if plane':>15}")
    for r in rows:
        print(f"  {r['dv_budget_m_s']:9.0f}{r['n_shells']:8d}{r['dv_spent_m_s']:9.1f}"
              f"{r['altitude_extent_km']:12.1f}{r['raan_spread_deg']:13.1f}"
              f"{r['host_fraction_of_extent']*100:10.1f}%"
              f"{r['inclination_if_spent_on_plane_deg']:15.3f}")

    print("\nbands:")
    for k, v in bands.items():
        mark = v.get('passed')
        print(f"  {k:26} {'PASS' if mark else ('REPORT' if mark is None else 'FAIL')}  {v}")

    out = dict(analysis='A20', bands_declared_commit='881c260',
               parametric_in='host delta-v budget; POEM-class propellant undisclosed (E5)',
               plane_change='EXCLUDED; reported only to demonstrate the exclusion',
               dv_shot_m_s=dv_shot, hohmann_50km_m_s=leg50,
               campaign_days=CAMPAIGN_DAYS, rows=rows, bands=bands)
    path = os.path.join(RESULTS, 'reachable_envelope.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, default=float)
        f.write('\n')
    print(f"\nwrote {path}")


if __name__ == '__main__':
    main()
