"""A75: whether the decay model is the wrong shape or just at the wrong level.

A50 band 1 failed: astro.py gives 70.6 days at 350 km where E28's own GMAT runs reentered at 36
and 29. P79 records the cause as a static atmosphere and asks for a variable-density model.

Before writing one, ask the cheaper question. astro.rho already carries a piecewise-exponential
table with its own scale heights, so its SHAPE in altitude is not flat. What it takes for activity
is a single multiplicative `scale`, and A50 ran at 1.0 without saying so. If one uniform scale
reproduces both GMAT cases and does not break the third, the defect is the LEVEL the model is
quoted at, not its form, and the repair is to quote a range.

Bands declared in validation/A75_decay_density_calibration.md before this file existed.

WHAT THIS IS AND IS NOT
-----------------------
GMAT is a second model. This is a calibration between two models and not a validation against
anything that happened. A9 remains the only specified run that would compare against a flown
object, and CelesTrak was re-tested from this environment on 2026-08-31 and is still refused by
the egress proxy under organisation policy. E4 stands.

astro.lifetime is imported and not restated. Band 1 checks the import is live by reproducing
A50's own published figures through it.

REPRODUCIBILITY, MEASURED RATHER THAN ASSUMED
---------------------------------------------
astro.lifetime advances in chunks of `k = int(min(50/|da|, 5000))` revolutions, and an int() of a
float is a step function -- a cross-machine difference in the last bits of `da` could in principle
flip it by one and change the trajectory discretely. That is the kind of hazard that made the
freshness gate compare numerically rather than byte-for-byte in the first place, so it was
measured instead of argued: perturbing the density scale by one, two and four ulp, and the
ballistic coefficient by one ulp, moves the 350 km lifetime by EXACTLY ZERO in all four cases.
The chunked advance quantises the answer, which is what makes it robust here. This run is
therefore in the freshness gate at the default tolerance rather than excluded from it.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, 'results')
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import astro                                          # noqa: E402  the model, not restated

BC_SAT = 61.0                                         # campaign_altitude.BC_SAT, unchanged
RE = astro.RE
DAYS_PER_YEAR = 365.25

# E28's runs, as A50 quotes them. Two fitting points at 350 km and one one-sided constraint.
GMAT_350 = [{'case': 'R2', 'inclination_deg': 55.2, 'reentry_days': 36.0},
            {'case': 'R3', 'inclination_deg': 9.6, 'reentry_days': 29.0}]
GMAT_450_SURVIVED_DAYS = 90.0
A50_350_DAYS = 70.6                                   # A50 band 1, published
SCALE_LO, SCALE_HI = 0.05, 200.0                      # the search interval, not a result


def life_days(alt_km, scale=1.0, bc=BC_SAT):
    return astro.lifetime(RE + alt_km * 1e3, 0.0, BC=bc, scale=scale) * DAYS_PER_YEAR


def scale_for(alt_km, target_days, lo=SCALE_LO, hi=SCALE_HI, iters=200, tol=1e-10):
    """The uniform density scale at which the model gives this lifetime at this altitude.

    Lifetime falls monotonically with density, so a plain bisection is safe here -- unlike the
    array-length searches in A72, where it was not, and the difference is stated rather than
    assumed: drag rises with density at every altitude in the table and nothing turns round.
    """
    f = lambda s: life_days(alt_km, s) - target_days           # noqa: E731
    flo = f(lo)
    if flo * f(hi) > 0.0:
        return None
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if (f(mid) < 0.0) == (flo < 0.0):
            lo = mid
        else:
            hi = mid
        if hi - lo < tol * max(hi, 1.0):
            break
    return 0.5 * (lo + hi)


def band1_verification():
    at350 = life_days(350.0, 1.0)
    at450 = life_days(450.0, 1.0)
    rel350 = abs(at350 - A50_350_DAYS) / A50_350_DAYS
    out = {'life_350_scale1_days': at350, 'a50_published_350_days': A50_350_DAYS,
           'rel_350': rel350, 'life_450_scale1_days': at450,
           'a50_band2_threshold_days': GMAT_450_SURVIVED_DAYS,
           'a50_band2_holds_at_scale1': at450 > GMAT_450_SURVIVED_DAYS}
    out['pass_'] = bool(rel350 <= 1e-3 and out['a50_band2_holds_at_scale1'])
    return out


def build():
    b1 = band1_verification()

    cases = []
    for c in GMAT_350:
        s = scale_for(350.0, c['reentry_days'])
        cases.append(dict(c, scale=s,
                          life_at_scale_days=life_days(350.0, s) if s else None))
    scales = [c['scale'] for c in cases if c['scale']]
    lo, hi = (min(scales), max(scales)) if scales else (None, None)
    spread = hi / lo if scales else None

    # The largest scale at which the 450 km case still survives the 90 days it survived.
    scale_450_limit = scale_for(450.0, GMAT_450_SURVIVED_DAYS)
    life_450_at_lo = life_days(450.0, lo) if lo else None
    life_450_at_hi = life_days(450.0, hi) if hi else None

    # A50 band 3: lifetime monotonically increasing in altitude, re-tested at both ends of the
    # calibrated band rather than only at scale 1.
    alts = [300.0, 350.0, 400.0, 450.0, 500.0, 600.0]
    monotone = {}
    for tag, s in (('lo', lo), ('hi', hi)):
        lives = [life_days(a, s) for a in alts]
        monotone[tag] = {'scale': s, 'alt_km': alts, 'life_days': lives,
                         'monotone': all(b > a for a, b in zip(lives, lives[1:]))}

    requoted = [{'alt_km': a,
                 'life_days_at_scale_lo': life_days(a, lo),
                 'life_days_at_scale_hi': life_days(a, hi),
                 'life_days_at_scale_1': life_days(a, 1.0)} for a in alts]

    bands = [
        {'band': '1', 'name': 'verification: the imported model reproduces A50 published figures',
         'detail': f"350 km {b1['life_350_scale1_days']:.4f} d against A50's "
                   f"{A50_350_DAYS} d, {b1['rel_350']:.2e}; 450 km "
                   f"{b1['life_450_scale1_days']:.1f} d clears 90",
         'pass_': b1['pass_']},
        {'band': '2', 'name': 'REPORT: the scale that reproduces each GMAT case',
         'detail': '; '.join(f"{c['case']} at {c['inclination_deg']:.1f} deg, "
                             f"{c['reentry_days']:.0f} d, needs scale {c['scale']:.4f}"
                             for c in cases)
                   + f"; the 450 km case permits up to {scale_450_limit:.4f}",
         'pass_': None},
        {'band': '3', 'name': 'one uniform scale explains both 350 km cases, within a factor of 2',
         'detail': f"{lo:.4f} to {hi:.4f}, spread {spread:.4f}x",
         'pass_': bool(spread is not None and spread <= 2.0)},
        {'band': '4', 'name': 'the calibrated scale does not break the 450 km evidence',
         'detail': f"450 km gives {life_450_at_hi:.1f} d at the harsher end of the band and "
                   f"{life_450_at_lo:.1f} d at the milder, against the 90 d it survived",
         'pass_': bool(life_450_at_hi is not None
                       and life_450_at_hi > GMAT_450_SURVIVED_DAYS)},
        {'band': '5', 'name': "A50's altitude monotonicity survives at both ends of the band",
         'detail': f"monotone at scale {lo:.4f}: {monotone['lo']['monotone']}; "
                   f"at {hi:.4f}: {monotone['hi']['monotone']}",
         'pass_': bool(monotone['lo']['monotone'] and monotone['hi']['monotone'])},
        {'band': '6', 'name': "REPORT: A50 durations re-quoted across the calibrated band",
         'detail': '; '.join(f"{r['alt_km']:.0f} km {r['life_days_at_scale_hi']:.1f} to "
                             f"{r['life_days_at_scale_lo']:.1f} d" for r in requoted),
         'pass_': None},
    ]

    return {
        'analysis': 'A75',
        'bands_declared_commit': 'fb681fd, before this file existed',
        'note': ('Whether astro.py decay disagreement with E28 GMAT runs is a level or a form '
                 'problem. GMAT is a second model: this is a calibration, not a validation. '
                 'A9 re-tested 2026-08-31 and CelesTrak is still refused. E4 stands.'),
        'inputs': {'bc_sat': BC_SAT, 'gmat_350': GMAT_350,
                   'gmat_450_survived_days': GMAT_450_SURVIVED_DAYS,
                   'a50_published_350_days': A50_350_DAYS,
                   'search_interval': [SCALE_LO, SCALE_HI]},
        'verification': b1,
        'cases': cases,
        'calibrated_band': {'scale_lo': lo, 'scale_hi': hi, 'spread': spread,
                            'scale_450_permits_up_to': scale_450_limit,
                            'life_450_at_scale_lo_days': life_450_at_lo,
                            'life_450_at_scale_hi_days': life_450_at_hi},
        'monotonicity': monotone,
        'requoted': requoted,
        'bands': bands,
    }


def main():
    r = build()
    b1 = r['verification']
    print("A75 decay density calibration, BC 61.0, against E28's own GMAT runs")
    print(f"  verification: 350 km at scale 1 is {b1['life_350_scale1_days']:.4f} d against "
          f"A50's {A50_350_DAYS} d ({b1['rel_350']:.2e}); 450 km is "
          f"{b1['life_450_scale1_days']:.1f} d")
    print()
    for c in r['cases']:
        print(f"  {c['case']} at {c['inclination_deg']:5.1f} deg reentered in "
              f"{c['reentry_days']:.0f} d -> uniform density scale {c['scale']:.4f}")
    cb = r['calibrated_band']
    print(f"\n  calibrated band {cb['scale_lo']:.4f} to {cb['scale_hi']:.4f}, "
          f"spread {cb['spread']:.4f}x")
    print(f"  the 450 km case surviving 90 d permits any scale up to "
          f"{cb['scale_450_permits_up_to']:.4f}")
    print(f"  at the calibrated band 450 km gives {cb['life_450_at_scale_hi_days']:.1f} to "
          f"{cb['life_450_at_scale_lo_days']:.1f} d")
    print("\n  altitude   at scale 1     re-quoted across the calibrated band")
    for q in r['requoted']:
        print(f"  {q['alt_km']:6.0f} km  {q['life_days_at_scale_1']:9.1f} d     "
              f"{q['life_days_at_scale_hi']:8.1f} to {q['life_days_at_scale_lo']:.1f} d")
    print("\nbands:")
    for b in r['bands']:
        v = 'REPORT' if b['pass_'] is None else ('PASS' if b['pass_'] else 'FAIL')
        print(f"  band {b['band']}: {v}  {b['name']}\n            {b['detail']}")
    os.makedirs(RESULTS, exist_ok=True)
    json.dump(r, open(os.path.join(RESULTS, 'decay_calibration.json'), 'w'), indent=2)
    print("\n-> results/decay_calibration.json")
    return 0


if __name__ == '__main__':
    sys.exit(main())
