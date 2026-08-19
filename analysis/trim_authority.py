"""A55: the dispersion and the trim authority, at the stroke ADR-034 actually adopted.

Bands declared in validation/A55_trim_authority.md at HEAD~1, BEFORE this file existed.

WHY THIS EXISTS
---------------
P83. A48 sized a 39.7 mm stator carrying +-0.323 m/s against A44's 1.113 % dispersion. Both were
computed over a 2.18 m stroke. ADR-034 took the stroke to 8.0 m and tripled the friction share
that owns 93.4 % of that dispersion -- 9.75 % to 28.39 % of shot work, A49 band 6, P78.

P84 is why nobody noticed: gen6_dispersion.py computes w_net = w - friction_N * pc.STROKE, and
pc.STROKE was still 2.18 m three days after the design point moved. That repair is committed
before this run.

THE QUESTION
------------
Does 39.7 mm of stator still cover +-3 sigma at the stroke that was adopted? And behind it:
ADR-033's first falsifier is that the pulse store weighs more than the 0.340 kg section it feeds,
and pulse hardware scales with CURRENT, not energy. If the authority has to grow, so does the
store nobody has weighed.

WHAT IS IMPORTED AND WHAT IS ADDED
----------------------------------
The work integral comes from precharged, the variance terms and the Monte-Carlo seed from
gen6_dispersion, and the trim geometry from trim_stage. Nothing is restated.

What is added is the STROKE as an explicit argument, so A44's point and the adopted point can be
computed by one model, and a sweep of the friction share so the authority requirement is a
function of the term nobody has measured rather than a single assumed value.

Run:  python3 analysis/trim_authority.py
"""
import json
import math
import os
import random

import precharged as pc
import gen6_dispersion as gd
import trim_stage as ts

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

V_CHAMBER = 2.0e-3
A44_STROKE, A44_P0 = 2.18, 50e5          # the point A44 and A48 were computed at
A48_AUTHORITY = 0.323                     # m/s, the section as built
A48_SECTION_M = 0.0397
FRICTION_SHARES = (0.0975, 0.15, 0.20, 0.2839, 0.35, 0.45, 0.60)


def v_exit(p0, m_pay, friction_N, L):
    """A41's work integral less the work friction takes out of the stroke, with L explicit."""
    w_net = pc.work(p0, V_CHAMBER, L) - friction_N * L
    return math.sqrt(2.0 * w_net / m_pay) if w_net > 0.0 else 0.0


def p_for_v(target, m_pay, friction_N, L):
    lo, hi = 1e5, 400e5
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if v_exit(mid, m_pay, friction_N, L) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def dispersion(p_cmd, L, friction_N=gd.FRICTION_N, sigma_p_fs=gd.SIGMA_P_FS,
               sigma_m=gd.SIGMA_M_REL, sigma_f=gd.SIGMA_F_REL, n=gd.N_MC, seed=gd.SEED):
    """gd.dispersion's model with the stroke and the friction force made explicit."""
    rng = random.Random(seed)
    vs = []
    for _ in range(n):
        # A44 references the transducer's full scale to gd.P_NOMINAL, a FIXED 50 bar, not to
        # the commanded pressure and not to the 200 bar store. Writing 200e5 here made the
        # pressure noise 4x too large and band 1 caught it -- which is what band 1 is for.
        p = p_cmd + rng.gauss(0.0, sigma_p_fs * gd.P_NOMINAL)
        m = pc.M_PAY * (1.0 + rng.gauss(0.0, sigma_m))
        f = friction_N * (1.0 + rng.gauss(0.0, sigma_f))
        vs.append(v_exit(p, m, f, L))
    mean = sum(vs) / len(vs)
    var = sum((v - mean) ** 2 for v in vs) / (len(vs) - 1)
    return mean, 3.0 * math.sqrt(var)


def one_term(p_cmd, L, which, friction_N=gd.FRICTION_N):
    """3 sigma with only one variance term live, for the attribution."""
    kw = dict(sigma_p_fs=0.0, sigma_m=0.0, sigma_f=0.0, friction_N=friction_N)
    kw['sigma_' + which] = {'p_fs': gd.SIGMA_P_FS, 'm': gd.SIGMA_M_REL,
                            'f': gd.SIGMA_F_REL}[which]
    return dispersion(p_cmd, L, **kw)[1]


def point(p0, L, friction_N=gd.FRICTION_N):
    """Everything A55 needs about one design point."""
    mean, s3 = dispersion(p0, L, friction_N)
    parts = {w: one_term(p0, L, w, friction_N) for w in ('p_fs', 'm', 'f')}
    tot = sum(v * v for v in parts.values())
    w_gross = pc.work(p0, V_CHAMBER, L)
    w_fric = friction_N * L
    return dict(p0_bar=p0 / 1e5, stroke_m=L, mean=mean, three_sigma=s3,
                three_sigma_pct=s3 / mean * 100.0,
                work_J=w_gross, friction_J=w_fric, friction_frac=w_fric / w_gross,
                var_share={k: (v * v / tot) for k, v in parts.items()})


def trim_for(pt, authority_k=1.0):
    """The section A48's model demands to cover k x 3 sigma at this point."""
    dv = authority_k * pt['three_sigma']
    force_per_m = ts.KT * ts.SHEET_A_PER_M / 1e3
    e = abs(ts.energy_to_trim(dv, pc.M_PAY, pt['mean']))
    L = ts.section_for(dv, pc.M_PAY, pt['mean'], force_per_m)
    return dict(authority_m_s=dv, energy_J=e, pct_of_shot=e / pt['work_J'] * 100.0,
                section_m=L, pct_stroke=L / pt['stroke_m'] * 100.0,
                peak_W=ts.peak_power(dv, pc.M_PAY, pt['mean'], force_per_m),
                mass_kg=L * (ts.MAGNET_KG_PER_M + ts.STATOR_KG_PER_M))


def main():
    a44 = point(A44_P0, A44_STROKE)
    now = point(pc.P_MAX, pc.STROKE)
    t44, tnow = trim_for(a44), trim_for(now)

    print(f"A55 trim authority. A44's point {A44_STROKE:.2f} m at {A44_P0/1e5:.0f} bar; "
          f"adopted {pc.STROKE:.1f} m at {pc.P_MAX/1e5:.4f} bar\n")
    print(f"{'':>22}{'A44 point':>14}{'adopted':>14}")
    for lab, key, fmt in (('exit velocity m/s', 'mean', '14.4f'),
                          ('3 sigma m/s', 'three_sigma', '14.5f'),
                          ('3 sigma %', 'three_sigma_pct', '14.4f'),
                          ('shot work J', 'work_J', '14.1f'),
                          ('friction work J', 'friction_J', '14.1f')):
        print(f"  {lab:>20}{format(a44[key], fmt)}{format(now[key], fmt)}")
    print(f"  {'friction share %':>20}{a44['friction_frac']*100:14.2f}"
          f"{now['friction_frac']*100:14.2f}")
    print(f"\n  variance owned by the seal: A44 {a44['var_share']['f']*100:.1f} %, "
          f"adopted {now['var_share']['f']*100:.1f} %")

    print(f"\n{'':>22}{'A44 point':>14}{'adopted':>14}")
    for lab, key, fmt in (('authority needed m/s', 'authority_m_s', '14.4f'),
                          ('section m', 'section_m', '14.5f'),
                          ('% of stroke', 'pct_stroke', '14.4f'),
                          ('energy J', 'energy_J', '14.2f'),
                          ('% of shot', 'pct_of_shot', '14.4f'),
                          ('peak W', 'peak_W', '14.0f'),
                          ('section mass kg', 'mass_kg', '14.4f')):
        print(f"  {lab:>20}{format(t44[key], fmt)}{format(tnow[key], fmt)}")

    per_sat = 1.296 + tnow['mass_kg'] / pc.N_MANIFEST     # A49's figure, plus the resized section

    print(f"\nband 9, authority against friction share (the sweep P67 decides):")
    print(f"  {'share %':>9}{'F N':>9}{'3 sigma %':>11}{'authority':>11}"
          f"{'section mm':>12}{'mass kg':>9}")
    sweep = []
    for share in FRICTION_SHARES:
        # the friction force that produces this share of shot work at the adopted stroke
        f_n = share * pc.work(pc.P_MAX, V_CHAMBER, pc.STROKE) / pc.STROKE
        p = point(pc.P_MAX, pc.STROKE, f_n)
        t = trim_for(p)
        sweep.append(dict(share=share, friction_N=f_n, **{k: p[k] for k in
                          ('mean', 'three_sigma', 'three_sigma_pct')},
                          **{('trim_' + k): v for k, v in t.items()}))
        print(f"  {share*100:9.2f}{f_n:9.1f}{p['three_sigma_pct']:11.4f}"
              f"{t['authority_m_s']:11.4f}{t['section_m']*1e3:12.2f}{t['mass_kg']:9.4f}")

    bands = [
        ('1', "reproduces A44's 1.113 % at 3 sigma within 2 % relative",
         f"{a44['three_sigma_pct']:.4f} %",
         abs(a44['three_sigma_pct'] - 1.113) / 1.113 <= 0.02),
        ('2', 'friction still owns >= 80 % of the variance at the adopted point',
         f"{now['var_share']['f']*100:.2f} %", now['var_share']['f'] >= 0.80),
        ('3', '3 sigma at the adopted point <= 2.0 %',
         f"{now['three_sigma_pct']:.4f} %", now['three_sigma_pct'] <= 2.0),
        ('4', f"A48's {A48_AUTHORITY} m/s section still covers +-3 sigma",
         f"needs {tnow['authority_m_s']:.4f} m/s, has {A48_AUTHORITY} "
         f"({tnow['authority_m_s']/A48_AUTHORITY:.2f}x)",
         tnow['authority_m_s'] <= A48_AUTHORITY),
        ('5', "section <= 15 % of the stroke (A48 band 3)",
         f"{tnow['pct_stroke']:.4f} %", tnow['pct_stroke'] <= 15.0),
        ('6', 'resized section mass <= 1.0 kg',
         f"{tnow['mass_kg']:.4f} kg", tnow['mass_kg'] <= 1.0),
        ('7', 'added mass per satellite with the resized section <= 2.0 kg',
         f"{per_sat:.4f} kg", per_sat <= 2.0),
        ('8', 'correction energy <= 5 % of the shot',
         f"{tnow['pct_of_shot']:.4f} %", tnow['pct_of_shot'] <= 5.0),
        ('9', 'REPORT: authority against friction share',
         f"{len(sweep)} points, {sweep[0]['trim_authority_m_s']:.4f} to "
         f"{sweep[-1]['trim_authority_m_s']:.4f} m/s", None),
    ]
    print('\nbands:')
    for n, band, value, ok in bands:
        mark = 'REPORT' if ok is None else ('PASS' if ok else 'FAIL')
        print(f'  {n}  {mark:6} {band}\n        {value}')

    out = dict(analysis='A55', bands_declared_commit='HEAD~1',
               a44_point=a44, adopted_point=now, trim_a44=t44, trim_adopted=tnow,
               a48_authority_m_s=A48_AUTHORITY, a48_section_m=A48_SECTION_M,
               added_mass_per_satellite_kg=per_sat, friction_sweep=sweep,
               bands=[dict(n=n, band=b, value=v,
                           verdict=('REPORT' if o is None else ('PASS' if o else 'FAIL')))
                      for n, b, v, o in bands])
    path = os.path.join(RESULTS, 'trim_authority.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, default=float)
        f.write('\n')
    print(f'\nwrote {path}')


if __name__ == '__main__':
    main()
