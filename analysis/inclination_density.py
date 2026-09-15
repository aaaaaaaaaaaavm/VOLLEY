"""A76: whether inclination through a variable atmosphere explains A75's residual.

A75 inverted E28's two GMAT reentries into uniform density scales of 1.9667 at 55.2 deg and
2.4443 at 9.6 deg, both at 350 km, agreeing to 1.2428x. A scalar cannot carry two values at one
altitude, and P79 names the candidate in writing: inclination, through a variable-density
atmosphere.

The two GMAT cases differ in exactly one input. validation/gmat/build_poem_campaign.py sets both
at 350 km, ECC 0, RAAN/AOP/TA 0, the same epoch, MSISE90, F107 = F107A = 150.0 and KP = 3.0. Only
INC_DEG differs. So a variable atmosphere explains the residual through inclination or not at all,
and there are two routes: the thermosphere's LATITUDE STRUCTURE, which the two orbits sample
differently, and the J2 NODAL RATE, which goes as cos i and sweeps them through the diurnal
density bulge at different speeds.

Bands declared in validation/A76_inclination_density_residual.md before this file existed.

WHAT THIS IS AND IS NOT
-----------------------
GMAT ran MSISE90. This runs NRLMSISE-00, because MSISE90 is not available in this environment and
its successor is. So a ratio agreeing with 1.2428x is a STRUCTURAL explanation of the residual and
not a second derivation of the two lifetimes. The absolute level stays where A75 left it.

Altitude is held at 350 km throughout. This does not integrate an orbit down and is not a decay
simulation. Holding altitude fixed is what isolates inclination, which is the only input the two
GMAT cases disagree on.

REPRODUCIBILITY
---------------
pymsis returns float32. The band 1 identity is therefore quoted at 1e-6 and observed near 2e-7,
which is the storage limit and not a tolerance chosen to pass. Every mean below is a plain
arithmetic mean over a fixed, deterministic sample grid, so there is no integrator state and no
step-size path dependence. The whole run takes about one second and two runs on this machine
are byte-identical, so it is IN the freshness gate rather than excluded from it, at a declared
per-file tolerance of 1e-6: pymsis returns float32, and the same Fortran built by another
compiler cannot be held below the storage precision of what it returns. pymsis is pinned in
requirements.txt; if it is absent this run fails loudly, which is the harmless failure mode
docs/REPRODUCTION_ENVIRONMENT.md distinguishes from the dangerous one.

THE SAMPLING DEFECT THIS FILE ALREADY HAD ONCE
----------------------------------------------
The first run sampled two revolutions per day, which set the step to exactly 12 h against a
diurnal density cycle and pinned the grid to a fixed pair of local solar times. Band 5 duly
reported local-time sampling contributing 1.0004x, which is what a blind grid reports, not what
the atmosphere does. The grid now walks every revolution in the window contiguously, so local
solar time advances by the orbit's own regression against the Sun and nothing is commensurate
with 24 h by construction. The faulted run is preserved at f65eab3 and is quoted in the run
sheet beside the corrected one.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, 'results')

MU = 3.986004418e14
RE = 6378137.0
J2 = 1.08262668e-3

# From validation/gmat/build_poem_campaign.py, unchanged.
ALT_KM = 350.0
F107 = F107A = 150.0
AP = 15.0                       # Kp 3.0 on the standard Kp-to-ap table
EPOCH = '2027-01-01T00:00:00'
CASES = [{'case': 'R2', 'inc_deg': 55.2, 'reentry_days': 36.0},
         {'case': 'R3', 'inc_deg': 9.6, 'reentry_days': 29.0}]

A75_RESIDUAL = 1.2428           # A75, the thing this run attacks
PRIMARY_WINDOW_D = 29.0         # the shorter observed lifetime; both fleets survived it
SENSITIVITY_WINDOW_D = 36.0
SAMPLES_PER_REV = 24
# Every revolution in the window is sampled, contiguously. The first run of this analysis took
# two revolutions per day instead, which put the sampling step at exactly 12 h against a diurnal
# density cycle and locked the grid onto a fixed pair of local solar times. That grid could not
# see the local-time mechanism band 5 is asked to report. Preserved at f65eab3.

# NRLMSISE-00's own total-mass-density identity: integer masses and 1.66e-24 g.
SPECIES_MASS = {'HE': 4, 'O': 16, 'N2': 28, 'O2': 32, 'AR': 40, 'H': 1, 'N': 14,
                'ANOMALOUS_O': 16}
AMU_KG_CM3_TO_KG_M3 = 1.66e-27
SSO_RATE_DEG_PER_DAY = 360.0 / 365.2422


def nodal_rate_rad_s(a_m, inc_deg, ecc=0.0):
    """J2 secular nodal regression. The one inclination-dependent term band 5 rests on."""
    n = math.sqrt(MU / a_m ** 3)
    return -1.5 * J2 * (RE / a_m) ** 2 * n * math.cos(math.radians(inc_deg)) / (1.0 - ecc ** 2) ** 2


def _geodetic(inc_deg, raan_rad, arg_lat_rad):
    """Sub-satellite latitude and longitude for a circular orbit, in an inertial frame."""
    i = math.radians(inc_deg)
    lat = math.asin(math.sin(i) * math.sin(arg_lat_rad))
    dlon = math.atan2(math.cos(i) * math.sin(arg_lat_rad), math.cos(arg_lat_rad))
    return math.degrees(lat), raan_rad + dlon


def sample_points(inc_deg, window_days, freeze_node, epoch=EPOCH):
    """Deterministic time/lat/lon grid over the window. No randomness, no integration."""
    import numpy as np
    a = RE + ALT_KM * 1e3
    n = math.sqrt(MU / a ** 3)
    period_s = 2.0 * math.pi / n
    rate = 0.0 if freeze_node else nodal_rate_rad_s(a, inc_deg)
    t0 = np.datetime64(epoch)

    n_rev = int(math.floor(window_days * 86400.0 / period_s))
    times, lats, lons = [], [], []
    for k in range(n_rev):
        t_rev = k * period_s
        for j in range(SAMPLES_PER_REV):
            t = t_rev + j * period_s / SAMPLES_PER_REV
            raan = rate * t
            lat, lon = _geodetic(inc_deg, raan, 2.0 * math.pi * j / SAMPLES_PER_REV)
            # Earth-fixed longitude: subtract Earth rotation so local solar time is right.
            lon_ef = math.degrees(lon) - 360.0 * (t / 86164.0905)
            times.append(t0 + np.timedelta64(int(round(t * 1e6)), 'us'))
            lats.append(lat)
            lons.append(((lon_ef + 180.0) % 360.0) - 180.0)
    return np.array(times), np.array(lats), np.array(lons)


def densities(inc_deg, window_days, freeze_node, epoch=EPOCH):
    """Returns (mean mass density, worst relative band-1 identity error over the grid)."""
    import numpy as np
    import pymsis
    V = pymsis.Variable
    times, lats, lons = sample_points(inc_deg, window_days, freeze_node, epoch)
    out = pymsis.calculate(times, lons, lats, np.full(lats.shape, ALT_KM),
                           np.full(lats.shape, F107), np.full(lats.shape, F107A),
                           [[AP] * 7] * len(lats), version=0)
    rho = out[:, V.MASS_DENSITY].astype(float)
    ident = np.zeros_like(rho)
    for name, m in SPECIES_MASS.items():
        ident += m * out[:, V[name]].astype(float)
    ident *= AMU_KG_CM3_TO_KG_M3
    worst = float(np.max(np.abs(ident - rho) / rho))
    return float(np.mean(rho)), worst


def latitude_contrast_diagnostic():
    """POST-HOC DIAGNOSTIC, NOT A BAND, added after the bands were evaluated.

    Band 4 failed at 1.0138 while the model's point-wise latitude gradient is far larger than
    that, which invites the suspicion that the averaging is broken. It is not. The gradient
    reverses sign with local solar time -- density rises towards the pole on the night side and
    falls towards it on the day side -- so an orbit that samples every local time averages most
    of the contrast away. This reports the contrast at fixed UT so the reader can see both facts
    at once. It is labelled a diagnostic because it was written after the run, and no band
    depends on it.
    """
    import numpy as np
    import pymsis
    V = pymsis.Variable
    lats = [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 55.0, 60.0]
    rows = []
    for hour in (0, 6, 12, 18):
        t = np.datetime64('2027-01-01T%02d:00' % hour)
        vals = []
        for lat in lats:
            o = pymsis.calculate(t, 0.0, lat, ALT_KM, F107, F107A, [[AP] * 7], version=0)[0]
            vals.append(float(o[V.MASS_DENSITY]))
        rows.append({'ut_hour': hour, 'latitude_deg': lats, 'density_kg_m3': vals,
                     'max_over_min': max(vals) / min(vals),
                     'sign_of_gradient_20_to_60_deg': 1 if vals[-1] > vals[2] else -1})
    return {'note': ('Point-wise latitude contrast at fixed UT. The gradient reverses sign with '
                     'local solar time, which is why orbit-averaging removes most of it and why '
                     'band 4 can fail at 1.0138 while these rows span tens of percent.'),
            'rows': rows}


def sso_inclination(a_m):
    """Inclination at which the implemented nodal rate equals the sun-synchronous rate."""
    target = math.radians(SSO_RATE_DEG_PER_DAY) / 86400.0
    lo, hi = 90.0, 120.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if nodal_rate_rad_s(a_m, mid) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def run():
    a = RE + ALT_KM * 1e3
    worst_identity = 0.0

    def mean(inc, window, freeze, epoch=EPOCH):
        nonlocal worst_identity
        m, w = densities(inc, window, freeze, epoch)
        worst_identity = max(worst_identity, w)
        return m

    primary = {}
    for freeze in (False, True):
        tag = 'frozen_node' if freeze else 'regressing_node'
        rows = {c['case']: mean(c['inc_deg'], PRIMARY_WINDOW_D, freeze) for c in CASES}
        primary[tag] = {'mean_density_kg_m3': rows,
                        'ratio_low_over_high_inclination': rows['R3'] / rows['R2']}

    ratio = primary['regressing_node']['ratio_low_over_high_inclination']
    frozen_ratio = primary['frozen_node']['ratio_low_over_high_inclination']

    sensitivity = {c['case']: mean(c['inc_deg'], SENSITIVITY_WINDOW_D, False) for c in CASES}
    sensitivity_ratio = sensitivity['R3'] / sensitivity['R2']

    quarters = []
    for ep in ('2027-01-01T00:00:00', '2027-04-01T00:00:00',
               '2027-07-01T00:00:00', '2027-10-01T00:00:00'):
        rows = {c['case']: mean(c['inc_deg'], PRIMARY_WINDOW_D, False, ep) for c in CASES}
        quarters.append({'epoch': ep, 'mean_density_kg_m3': rows,
                         'ratio': rows['R3'] / rows['R2']})

    lo_band, hi_band = A75_RESIDUAL ** 0.5, A75_RESIDUAL ** 1.5

    rate_89 = math.degrees(nodal_rate_rad_s(a, 89.0)) * 86400.0
    rate_91 = math.degrees(nodal_rate_rad_s(a, 91.0)) * 86400.0
    rate_90 = abs(math.degrees(nodal_rate_rad_s(a, 90.0)) * 86400.0)
    i_sso = sso_inclination(a)
    b6 = bool(rate_89 < 0.0 and rate_91 > 0.0 and rate_90 <= 1e-15 and 96.0 < i_sso < 98.0)

    bands = [
        {'band': '1',
         'name': "verification by identity: NRLMSISE-00 reproduces its own species sum",
         'detail': f"worst relative error over every sample point {worst_identity:.3e}, "
                   f"limit 1e-6",
         'pass_': bool(worst_identity <= 1e-6)},
        {'band': '2',
         'name': 'REPORT: time-averaged density at each inclination, regressing and frozen node',
         'detail': '; '.join(
             f"{tag}: 9.6 deg {primary[tag]['mean_density_kg_m3']['R3']:.6e}, "
             f"55.2 deg {primary[tag]['mean_density_kg_m3']['R2']:.6e}, "
             f"ratio {primary[tag]['ratio_low_over_high_inclination']:.4f}"
             for tag in ('regressing_node', 'frozen_node')),
         'pass_': None},
        {'band': '3',
         'name': 'direction: 9.6 deg is denser than 55.2 deg, at the window and all four quarters',
         'detail': f"primary ratio {ratio:.4f}; quarters " +
                   ', '.join(f"{q['epoch'][:7]} {q['ratio']:.4f}" for q in quarters),
         'pass_': bool(ratio > 1.0 and all(q['ratio'] > 1.0 for q in quarters))},
        {'band': '4',
         'name': "magnitude: the ratio lands inside A75's half-to-one-and-a-half log window",
         'detail': f"ratio {ratio:.4f} against [{lo_band:.4f}, {hi_band:.4f}] "
                   f"around A75's {A75_RESIDUAL}",
         'pass_': bool(lo_band <= ratio <= hi_band)},
        {'band': '5',
         'name': 'REPORT: attribution between latitude structure and local-time sampling',
         'detail': f"frozen node {frozen_ratio:.4f} is latitude structure alone; releasing the "
                   f"node gives {ratio:.4f}; local-time sampling therefore contributes "
                   f"{ratio / frozen_ratio:.4f}x",
         'pass_': None},
        {'band': '6',
         'name': 'guard on the nodal rate that band 5 rests on',
         'detail': f"89 deg {rate_89:+.6f} deg/day, 91 deg {rate_91:+.6f}, "
                   f"90 deg |{rate_90:.3e}|, sun-synchronous at {i_sso:.4f} deg",
         'pass_': b6},
    ]

    return {
        'analysis': 'A76',
        'bands_declared_commit': '94122ba, before this file existed',
        'note': ('Whether inclination through a variable-density atmosphere explains the 1.2428x '
                 'residual A75 left in P79. GMAT ran MSISE90; this runs NRLMSISE-00, so a match '
                 'is a structural explanation and not a second derivation of the two lifetimes. '
                 'Altitude is held at 350 km: this is not a decay simulation.'),
        'inputs': {'alt_km': ALT_KM, 'f107': F107, 'f107a': F107A, 'ap': AP, 'epoch': EPOCH,
                   'cases': CASES, 'a75_residual': A75_RESIDUAL,
                   'primary_window_days': PRIMARY_WINDOW_D,
                   'sensitivity_window_days': SENSITIVITY_WINDOW_D,
                   'samples_per_rev': SAMPLES_PER_REV,
                   'revolutions_sampled': 'every revolution in the window, contiguously',
                   'atmosphere': 'NRLMSISE-00 via pymsis version=0'},
        'primary': primary,
        'sensitivity_36_day_window': {'mean_density_kg_m3': sensitivity,
                                      'ratio': sensitivity_ratio},
        'quarterly_epochs': quarters,
        'nodal_rate_guard': {'deg_per_day_at_89': rate_89, 'deg_per_day_at_91': rate_91,
                             'abs_deg_per_day_at_90': rate_90,
                             'sun_synchronous_inclination_deg': i_sso,
                             'sun_synchronous_rate_deg_per_day': SSO_RATE_DEG_PER_DAY},
        'band_window': {'lo': lo_band, 'hi': hi_band},
        'post_hoc_diagnostic_not_a_band': latitude_contrast_diagnostic(),
        'bands': bands,
        'all_evaluable_bands_pass': all(b['pass_'] for b in bands if b['pass_'] is not None),
    }


def main():
    out = run()
    print(f"A76, {out['note'].split('.')[0]}\n")
    for b in out['bands']:
        verdict = 'REPORT' if b['pass_'] is None else ('PASS' if b['pass_'] else 'FAIL')
        print(f"  band {b['band']}  {verdict:6}  {b['name']}")
        print(f"            {b['detail']}")
    print(f"\n  evaluable bands all pass: {out['all_evaluable_bands_pass']}")
    os.makedirs(RESULTS, exist_ok=True)
    with open(os.path.join(RESULTS, 'inclination_density.json'), 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2)
        fh.write('\n')


if __name__ == '__main__':
    main()
