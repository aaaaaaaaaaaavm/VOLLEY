"""A15 band 8, Case B: what a host plane-change manoeuvre costs, per degree.

WHY THIS NEEDS NO PROPAGATOR
----------------------------
Band 8 was recorded as not evaluated because "Case B is not generated". That framing made it
look like a missing GMAT run. It is not one. An impulsive plane change at a circular orbit is
closed form -- dv = 2*v*sin(di/2) -- and no integrator adds anything to it. The reason band 8
cannot become a capability claim is not that the number is unknown; it is that the number
belongs to the HOST, whose mass and control authority are undisclosed (E5). Those are different
kinds of missing, and only the second one is real.

So this computes the cost and leaves the disposition exactly where band 8 put it in advance:
REPORT, and VOID as a capability claim.

WHAT IT SHOWS
-------------
At POEM circular velocity the exchange rate is about 133 m/s per degree. VOLLEY's entire shot is
16.388 m/s. Spending all of it on plane change buys 0.123 deg, which is the same ceiling band 1
tested against GMAT and the same figure docs/KILL_CRITERIA.md section 7 already carries as
"plane change 0.12 deg, effectively nil".

The propellant column is a fraction of host wet mass, not a mass. With POEM's mass undisclosed
there is no kilogram figure to give, and inventing one is what E5 exists to prevent.

PROVENANCE
----------
MU and RE are imported from analysis/astro.py rather than restated, the rule build_scripts.py
already follows so the orbit definition cannot fork. Altitudes are the three A15 reference
cases. R2 and R3 remain UNVERIFIED inputs and are marked so here as they are everywhere else.

Run:  python3 validation/gmat/case_b_plane_change.py
"""
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'analysis'))

from astro import MU, RE  # noqa: E402  -- imported, not restated

RESULTS = os.path.join(ROOT, 'validation', 'results')

# The three A15 reference orbits. Provenance is carried with each so the unverified ones
# cannot be quoted as though they were traceable.
CASES = [
    ('R1', 450.0, 51.6, 'repo default, used by astro.py, A5 and A6'),
    ('R2', 350.0, 55.2, 'POEM-4-like. UNVERIFIED'),
    ('R3', 350.0, 9.6, 'POEM-3-like. UNVERIFIED'),
]

# Generic propulsion classes, by specific impulse. No product, vendor or programme is named:
# these are the textbook ranges, and the point of the column is the ratio, not a selection.
ISP_CLASSES = [('cold gas', 60.0), ('monopropellant', 220.0), ('bipropellant', 300.0)]

G0 = 9.80665
DV_SHOT = 16.388  # m/s, the rated shot -- docs/BASELINE.md
DI_GRID_DEG = [0.01, 0.02, 0.05, 0.1, 0.123, 0.2, 0.5, 1.0]


def v_circular(alt_km):
    return math.sqrt(MU / (RE + alt_km * 1e3))


def dv_plane_change(v, di_deg):
    """Impulsive plane change at a circular orbit. Exact, not a small-angle form."""
    return 2.0 * v * math.sin(math.radians(di_deg) / 2.0)


def di_for_dv(v, dv):
    """Inverse: the inclination change a given impulse can buy if it is all spent on plane."""
    return math.degrees(2.0 * math.asin(min(1.0, dv / (2.0 * v))))


def propellant_fraction(dv, isp):
    """Fraction of wet mass expended. A fraction, deliberately: host mass is undisclosed."""
    return 1.0 - math.exp(-dv / (isp * G0))


def main():
    out = {
        'analysis': 'A15',
        'band': 8,
        'question': 'host delta-v per degree of plane change',
        'disposition': 'REPORT; VOID as a capability claim',
        'disposition_declared': 'in advance, in the A15 band table',
        'void_reason': 'POEM mass and control authority are undisclosed (E5)',
        'method': 'closed form, dv = 2 v sin(di/2); no propagator involved',
        'dv_shot_m_s': DV_SHOT,
        'cases': [],
    }

    for name, alt_km, inc_deg, prov in CASES:
        v = v_circular(alt_km)
        rows = []
        for di in DI_GRID_DEG:
            dv = dv_plane_change(v, di)
            rows.append({
                'di_deg': di,
                'dv_m_s': dv,
                'shots_equivalent': dv / DV_SHOT,
                'propellant_fraction': {k: propellant_fraction(dv, isp)
                                        for k, isp in ISP_CLASSES},
            })
        out['cases'].append({
            'case': name,
            'alt_km': alt_km,
            'inc_deg': inc_deg,
            'provenance': prov,
            'v_circular_m_s': v,
            'dv_per_degree_m_s': dv_plane_change(v, 1.0),
            'di_from_one_shot_deg': di_for_dv(v, DV_SHOT),
            'grid': rows,
        })

    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, 'A15_caseB_plane_change.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)
        f.write('\n')

    for c in out['cases']:
        print(f"{c['case']}  {c['alt_km']:.0f} km  v = {c['v_circular_m_s'] / 1e3:.3f} km/s  "
              f"{c['dv_per_degree_m_s']:.1f} m/s per degree  "
              f"one shot buys {c['di_from_one_shot_deg']:.4f} deg")
    r1 = out['cases'][0]
    print(f"\nR1 grid, host delta-v against a {DV_SHOT} m/s shot:")
    for row in r1['grid']:
        print(f"  di {row['di_deg']:6.3f} deg -> {row['dv_m_s']:8.2f} m/s "
              f"= {row['shots_equivalent']:7.2f} shots")
    print(f"\nwrote {path}")


if __name__ == '__main__':
    main()
