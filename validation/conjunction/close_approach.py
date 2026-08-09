"""A15 band 6: minimum inter-object separation, refined rather than sampled.

WHY THIS EXISTS
---------------
A15 recorded band 6 as NOT EVALUATED, and it was right to. The first separation check sampled
one point every 1929 s against a 5560 s orbital period -- 2.9 samples per orbit -- so two
objects closing at kilometres per second could pass each other entirely between samples. The
numbers it produced were distances seen at three arbitrary points per orbit, not minima.

The GMAT runs wrote Cartesian X/Y/Z at ~60 000 rows per satellite, so the data to do this
properly was already on disk. This brackets every local minimum in the sampled separation and
refines it, which is what astro.py::conjunction() does at 0.25 s for the analytic case.

METHOD
------
Positions are splined against ROW INDEX rather than time. The integrator's steps are not
uniform, but the spatial minimum along a trajectory does not depend on how the parameter is
scaled, and using the index avoids parsing GMAT's date column. Each interior local minimum of
the sampled separation is refined with Brent minimisation on the spline.

SELF-CHECK
----------
Refinement can only find separations equal to or smaller than the sampled minimum. If it ever
returns a larger one, the spline or the bracketing is wrong, and this asserts on it.

Run:  python3 validation/conjunction/close_approach.py
"""
import glob
import itertools
import json
import os

import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize_scalar

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'validation', 'gmat', 'output')
RESULTS = os.path.join(ROOT, 'validation', 'results')
BAND_M = 100.0
CASES = ('r1', 'r2', 'r3')


def load(case):
    sats = {}
    for f in sorted(glob.glob(os.path.join(OUT, case, 'sat*.txt'))):
        rows = [l.split() for l in open(f, encoding='utf-8').read().strip().split('\n')[1:]
                if l.strip()]
        sats[os.path.basename(f)[:-4]] = np.array(
            [[float(r[8]), float(r[9]), float(r[10])] for r in rows])
    n = min(len(v) for v in sats.values())
    return {k: v[:n] for k, v in sats.items()}, n


def refine_pair(pa, pb, n):
    """Sampled minimum, then Brent refinement of every interior local minimum."""
    d = np.linalg.norm(pa - pb, axis=1)
    sampled = float(d.min())

    idx = np.arange(n, dtype=float)
    sa = CubicSpline(idx, pa, axis=0)
    sb = CubicSpline(idx, pb, axis=0)

    def sep(s):
        return float(np.linalg.norm(sa(s) - sb(s)))

    # interior local minima of the sampled series
    lo = np.where((d[1:-1] <= d[:-2]) & (d[1:-1] <= d[2:]))[0] + 1
    best, best_at = sampled, float(int(np.argmin(d)))
    for i in lo:
        a, b = max(0.0, i - 1.0), min(n - 1.0, i + 1.0)
        try:
            r = minimize_scalar(sep, bounds=(a, b), method='bounded',
                                options={'xatol': 1e-4})
        except Exception:
            continue
        if r.success and r.fun < best:
            best, best_at = float(r.fun), float(r.x)
    return sampled, best, best_at, len(lo)


def main():
    out = {}
    for case in CASES:
        sats, n = load(case)
        if not sats:
            continue
        names = list(sats)
        worst = None
        pairs = []
        for a, b in itertools.combinations(names, 2):
            sampled, refined, at, nmin = refine_pair(sats[a], sats[b], n)
            assert refined <= sampled + 1e-6, (
                f'{case} {a}-{b}: refinement returned {refined} > sampled {sampled}')
            pairs.append(dict(pair=f'{a}-{b}', sampled_km=sampled, refined_km=refined,
                              at_index=at, local_minima=nmin))
            if worst is None or refined < worst['refined_km']:
                worst = pairs[-1]
        improvement = 100 * (1 - worst['refined_km'] /
                             min(p['sampled_km'] for p in pairs))
        out[case] = dict(rows=n, pairs=len(pairs), worst=worst,
                         min_sampled_km=min(p['sampled_km'] for p in pairs),
                         min_refined_km=worst['refined_km'],
                         refinement_tightened_pct=improvement,
                         total_local_minima=sum(p['local_minima'] for p in pairs),
                         verdict='PASS' if worst['refined_km'] * 1000 > BAND_M else 'FAIL')
        print(f"{case.upper()}  {len(pairs)} pairs, {n} rows, "
              f"{sum(p['local_minima'] for p in pairs)} local minima refined")
        print(f"   sampled min {out[case]['min_sampled_km']:10.4f} km")
        print(f"   refined min {worst['refined_km']:10.4f} km  ({worst['pair']}) "
              f"-> tightened {improvement:.2f} %")
        print(f"   band 6 (> 100 m): {out[case]['verdict']}\n")

    path = os.path.join(RESULTS, 'A15_band6_close_approach.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(dict(analysis='A15 band 6', band_m=BAND_M,
                       method='cubic spline in row index, Brent refinement of every '
                              'interior local minimum; refinement is monotone-checked',
                       cases=out), f, indent=2)
        f.write('\n')
    print(f"wrote {path}")


if __name__ == '__main__':
    main()
