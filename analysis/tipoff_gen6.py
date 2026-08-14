"""
VOLLEY | Does A34's cradle closure survive the Gen6 operating point?

WHY THIS EXISTS
---------------
A34 closed kill criterion 4's open half on 2026-08-13, and closed it well: the rattle settles
in 27.25 ms of a 146.4 ms powered stroke, the residual rate at force removal is exactly zero
for every clearance A23 tabulated, and critical restitution is 0.9261 against a published
aluminium range of 0.3-0.7.

Every one of those numbers was computed at the Gen5 operating point.

A37 moves it. With no mover the payload takes the whole push at the 25 g cap -- 981 N instead
of 413 -- so the offset moment goes from 28.92 N.m to about 68.7, a factor of 2.4 on the term
that drives the entire A34 result.

This is the P19 and P53 pattern, which this project has now recorded twice: an analysis that
closed at one point and was left standing while the point moved underneath it. The difference
is that this point has NOT moved yet. Checking before adopting is the whole discipline.

Nothing here edits A34. Its closed forms are IMPORTED, not restated, so the two cannot fork;
band 1 drives them at the Gen5 point and requires A34's own answer back.

Bands declared in validation/A38_tipoff_at_gen6.md at 4e4bd58, BEFORE this file existed.

Provenance: model output, on A34's model. Restitution is swept, not measured, and the cradle
mechanism still does not exist -- both limitations carry forward unchanged.
"""
import json
import math
import os

import cradle_restitution as cr
import motor_model as mm

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

G = 9.81
G_CAP = 25.0                 # payload qualification cap, the A37 design point
M_SAT = 4.0
A34_SETTLE_MS = 27.25        # A34's published result at Gen5, for the band 1 regression
A34_E_CRIT = 0.9261
A34_PRELOAD_N = 85.0
PRELOAD_LIMIT_N = 250.0
STROKE_WINDOW_M = 2.18       # the long end of A37's feasible window; the shortest stroke time


def point(a_g, stroke_m):
    """Everything band 2-6 needs, at an acceleration and an acceleration length."""
    a = a_g * G
    v = math.sqrt(2 * a * stroke_m)
    F_payload = M_SAT * a
    M = F_payload * cr.COM_OFFSET
    alpha = M / cr.I_PAYLOAD
    return dict(a_g=a_g, stroke_m=stroke_m, v_exit=v, F_payload_N=F_payload,
                moment_Nm=M, alpha_rad_s2=alpha,
                t_powered_s=v / a,
                preload_N=cr.preload_for_no_liftoff(M))


def worst(p, e):
    """Worst settling and worst residual across every clearance A23 tabulated."""
    settle, resid, arrive = [], [], []
    for c_mm in cr.CLEARANCES_MM:
        w0 = cr.arrival_rate(c_mm / 1e3, p['alpha_rad_s2'])
        arrive.append(math.degrees(w0))
        settle.append(cr.settle_time(w0, p['alpha_rad_s2'], e))
        resid.append(math.degrees(
            cr.residual_rate(w0, p['alpha_rad_s2'], e, p['t_powered_s'])))
    return max(arrive), max(settle), max(resid)


def critical_e(p, lo=0.0, hi=0.9999):
    """Largest restitution whose settling still completes inside the powered stroke."""
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if worst(p, mid)[1] <= p['t_powered_s']:
            lo = mid
        else:
            hi = mid
    return lo


def main():
    # --- band 1: drive A34's own forms at the Gen5 point and require A34's answer back ---
    F5, M5, alpha5 = cr.moment_and_alpha()
    shot5 = mm.shot(mm.thrust_constant()[0])
    g5 = dict(a_g=shot5['a_g'], stroke_m=mm.ACCEL_ZONE, v_exit=shot5['v_exit'],
              F_payload_N=F5, moment_Nm=M5, alpha_rad_s2=alpha5,
              t_powered_s=(shot5['t_ms'] - cr.COAST_MS) / 1e3,
              preload_N=cr.preload_for_no_liftoff(M5))
    _, settle5, _ = worst(g5, cr.E_ALUMINIUM)
    ecrit5 = critical_e(g5)

    g6 = point(G_CAP, STROKE_WINDOW_M)
    arrive6, settle6, resid6 = worst(g6, cr.E_ALUMINIUM)
    ecrit6 = critical_e(g6)

    print("                              Gen5 (A34)      Gen6 (A37 window)")
    for label, k, fmt in (('acceleration, g', 'a_g', '%.2f'),
                          ('payload force, N', 'F_payload_N', '%.0f'),
                          ('offset moment, N.m', 'moment_Nm', '%.2f'),
                          ('angular accel, rad/s2', 'alpha_rad_s2', '%.0f'),
                          ('exit velocity, m/s', 'v_exit', '%.2f'),
                          ('powered stroke, ms', 't_powered_s', '%.1f'),
                          ('preload, N per contact', 'preload_N', '%.1f')):
        a = g5[k] * (1e3 if k == 't_powered_s' else 1)
        b = g6[k] * (1e3 if k == 't_powered_s' else 1)
        print(f"  {label:26s} {fmt % a:>12s} {fmt % b:>18s}")
    _, _, resid5 = worst(g5, cr.E_ALUMINIUM)
    arrive5 = worst(g5, cr.E_ALUMINIUM)[0]
    print(f"  {'worst arrival, deg/s':26s} {arrive5:12.1f} {arrive6:18.1f}")
    print(f"  {'settling at e=0.7, ms':26s} {settle5*1e3:12.2f} {settle6*1e3:18.2f}")
    print(f"  {'residual at release, deg/s':26s} {resid5:12.4f} {resid6:18.4f}")
    print(f"  {'critical restitution':26s} {ecrit5:12.4f} {ecrit6:18.4f}")

    # --- band 6: the acceleration ceiling tip-off imposes, over A37's window ---
    ceiling = None
    for tenth in range(10, 1001):
        g = tenth / 10.0
        p = point(g, STROKE_WINDOW_M)
        _, s, r = worst(p, cr.E_ALUMINIUM)
        if not (r < cr.TIPOFF_BAND and s <= p['t_powered_s']
                and critical_e(p) >= 0.80 and p['preload_N'] <= PRELOAD_LIMIT_N):
            ceiling = (tenth - 1) / 10.0
            break
    else:
        ceiling = 100.0
    print(f"\n  acceleration ceiling imposed by tip-off: {ceiling:.1f} g "
          f"(the qualification cap is {G_CAP:.0f} g)")

    bands = [
        ('1', 'model reproduces A34 at the Gen5 point, within 1 %',
         f"settle {settle5*1e3:.2f} against {A34_SETTLE_MS} ms, "
         f"e* {ecrit5:.4f} against {A34_E_CRIT}",
         abs(settle5 * 1e3 - A34_SETTLE_MS) / A34_SETTLE_MS <= 0.01
         and abs(ecrit5 - A34_E_CRIT) / A34_E_CRIT <= 0.01),
        ('2', f'residual at force removal < {cr.TIPOFF_BAND} deg/s, every clearance',
         f"worst {resid6:.4f} deg/s", resid6 < cr.TIPOFF_BAND),
        ('3', 'settling completes inside the powered stroke at e = 0.7',
         f"{settle6*1e3:.2f} ms of {g6['t_powered_s']*1e3:.1f} ms",
         settle6 <= g6['t_powered_s']),
        ('4', 'critical restitution >= 0.80, A34 threshold unrelaxed',
         f"{ecrit6:.4f}", ecrit6 >= 0.80),
        ('5', f'preload <= {PRELOAD_LIMIT_N:.0f} N per contact',
         f"{g6['preload_N']:.1f} N against A34's {A34_PRELOAD_N:.0f}",
         g6['preload_N'] <= PRELOAD_LIMIT_N),
        ('6', f'tip-off ceiling >= {G_CAP:.0f} g',
         f"{ceiling:.1f} g", ceiling >= G_CAP),
    ]
    print("\nbands:")
    for n, name, detail, ok in bands:
        print(f"  band {n}: {'PASS' if ok else 'FAIL'}  {name}\n            {detail}")

    out = dict(analysis='A38', bands_declared_commit='4e4bd58',
               note='A34 is imported, not restated; its bands are untouched and its result '
                    'stands at the point it was declared for. Restitution swept not measured; '
                    'the cradle mechanism still does not exist.',
               gen5=g5, gen6=g6, e_aluminium=cr.E_ALUMINIUM,
               gen5_settle_ms=settle5 * 1e3, gen5_e_crit=ecrit5,
               gen6_worst_arrival_deg_s=arrive6, gen6_settle_ms=settle6 * 1e3,
               gen6_residual_deg_s=resid6, gen6_e_crit=ecrit6,
               tipoff_ceiling_g=ceiling, qualification_cap_g=G_CAP,
               bands=[dict(band=n, name=nm, detail=d, pass_=ok)
                      for n, nm, d, ok in bands])
    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, 'tipoff_gen6.json')
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2, default=float)
        fh.write('\n')
    print(f"\nwrote {path}")


if __name__ == '__main__':
    main()
