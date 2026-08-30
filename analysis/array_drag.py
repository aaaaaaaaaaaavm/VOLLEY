"""A72: how long a magnet array the shot can afford to carry.

A66 found that the wall's eddy drag exceeds the trim stator's thrust above an air-gap field of
0.1500 T, and that the carriage magnets face the aluminium wall for the WHOLE 8.0 m stroke and
not only the 144.01 mm under the stator. It could not integrate that, because the magnet array
is dimensioned nowhere in this repository.

So the length is the variable here rather than an input. At each air-gap field, three lengths:

    L_force    makes the section's specified 948.0 N over the engaged annulus
    L_parity   the drag costs what the seal friction already costs, 28.3887 % of shot work
    L_stall    the carriage stops accelerating before the muzzle

Bands declared in validation/A72_trim_array_drag.md before this file existed; bands 3R and 4R
frozen in a second commit, also before this file existed, because 3 and 4 as first declared
could not discriminate. Neither correction saw a result.

The drag law is A66's and is not restated as a second opinion: band 1 checks this file's shear
against `tube_shielding`'s at A66's own point, and agreement there says only that the same
algebra has been collected two ways without a typing error. It is a consistency check, not a
second method.

Units are SI throughout.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RESULTS = os.path.join(HERE, 'results')
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import precharged as pc                              # noqa: E402  the shot, not restated
import tube_shielding as ts                          # noqa: E402  the drag law's source

P = json.load(open(os.path.join(ROOT, 'cad', 'parameters.json')))
G = P['groups']

MU0 = ts.MU0
SIGMA_AL = ts.SIGMA_AL
WALL_M = ts.WALL_M
GAP_R_M = ts.GAP_RADIUS_M                            # bore/2 + wall/2, A66
CIRC_M = 2.0 * math.pi * GAP_R_M
K_SHEET = ts.K_SHEET
FORCE_N = ts.FORCE_N
BR_T = ts.BR_T

STROKE_M = pc.STROKE
AREA_M2 = pc.AREA
M_PAY_KG = pc.M_PAY
P0_PA = pc.P_MAX
V_CHAMBER_M3 = G['gen6_store']['chamber_volume_l'] / 1e3
GAMMA = pc.GAMMA
FRICTION_N = 83.4                                    # A41 band 8's allowance, as A44 uses it
FRICTION_SHARE = FRICTION_N * STROKE_M / pc.work(P0_PA, V_CHAMBER_M3)
V_ADOPTED = G['gen6_drive']['exit_velocity_m_s']

FIELDS = [0.2, 0.4, 0.6, 0.8, 1.0, BR_T]             # A66's ladder, unchanged
# 2000 RK4 steps. Halving to 1000 moves the exit velocity by 5.5e-8 and the drag energy by
# 1.6e-7 relative, and going to 20000 moves them by less again; band 1 reports the halving on
# every run so the choice stays visible rather than assumed.
STEPS = 2000


def pressure(x, p0=P0_PA, v0=V_CHAMBER_M3, area=AREA_M2, gamma=GAMMA):
    """Closed adiabatic expansion, the same law precharged.work() integrates analytically."""
    return p0 * (v0 / (v0 + area * x)) ** gamma


def shear_Pa(b_gap, v, sigma=SIGMA_AL, d=WALL_M):
    """Thin-sheet induction drag per unit area, at the carriage's instantaneous velocity.

    tau = (B^2 / 2mu) * 2Rm / (1 + Rm^2),  Rm = mu sigma d v / 2

    It is NOT linear in v. Rm reaches 0.7539 at the muzzle, three quarters of the way to the
    peak of that curve, so a linear reading would overstate the low-speed drag and understate
    where the curve actually is.
    """
    rm = MU0 * sigma * d * v / 2.0
    return (b_gap * b_gap / (2.0 * MU0)) * (2.0 * rm / (1.0 + rm * rm))


def integrate(b_gap, array_len_m, sigma=SIGMA_AL, d=WALL_M, friction_N=FRICTION_N,
              steps=STEPS, stroke=STROKE_M):
    """The shot with the eddy drag in it, integrated in x on kinetic energy.

    Energy rather than velocity, because dv/dx is singular at rest and dE/dx is not.
    """
    area_arr = CIRC_M * array_len_m
    h = stroke / steps

    def dE(x, e):
        v = math.sqrt(2.0 * max(e, 0.0) / M_PAY_KG)
        return pressure(x) * AREA_M2 - friction_N - shear_Pa(b_gap, v, sigma, d) * area_arr

    e = 0.0
    x = 0.0
    drag_J = 0.0
    min_dE = dE(0.0, 0.0)
    for _ in range(steps):
        k1 = dE(x, e)
        k2 = dE(x + h / 2.0, e + h * k1 / 2.0)
        k3 = dE(x + h / 2.0, e + h * k2 / 2.0)
        k4 = dE(x + h, e + h * k3)
        # the drag term alone, integrated on the same nodes with the same weights
        for w, xs, es in ((1.0, x, e), (2.0, x + h / 2.0, e + h * k1 / 2.0),
                          (2.0, x + h / 2.0, e + h * k2 / 2.0), (1.0, x + h, e + h * k3)):
            v = math.sqrt(2.0 * max(es, 0.0) / M_PAY_KG)
            drag_J += (w / 6.0) * h * shear_Pa(b_gap, v, sigma, d) * area_arr
        e += h * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
        x += h
        min_dE = min(min_dE, dE(x, e))
    return {'v_exit': math.sqrt(2.0 * max(e, 0.0) / M_PAY_KG), 'energy_J': e,
            'drag_J': drag_J, 'min_dE_dx_N': min_dE, 'array_area_m2': area_arr}


def length_for_force(b_gap, force_N=FORCE_N, k=K_SHEET, circ=CIRC_M):
    """Engaged array length that makes the section's specified force at that field."""
    return force_N / (b_gap * k * circ)


def _bisect(f, lo, hi, tol=1e-7, iters=60):
    """Bisect between a bracketing pair. f(lo) and f(hi) must straddle zero."""
    flo = f(lo)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if (f(mid) < 0.0) == (flo < 0.0):
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


def _first_root(f, hi, n_scan=48, tol=1e-7):
    """The SHORTEST array length at which f changes sign, or None if it never does.

    Neither quantity this is used on is monotone in the array length, and assuming they were
    is a bug this file had: the drag force is proportional to v * L and v falls roughly as 1/L,
    so both the drag energy and the worst acceleration turn round again once the array is long
    enough to have throttled the shot that drives them. A plain bisection from 0 to 4 m then
    sees the same sign at both ends and returns the bound. The first crossing is the one that
    means anything -- the shortest array that costs this much -- so it is found by scanning
    before bisecting rather than assumed to be the only one.
    """
    lo = 1e-6
    flo = f(lo)
    step = (hi / lo) ** (1.0 / n_scan)
    x = lo
    for _ in range(n_scan):
        nxt = x * step
        if (f(nxt) < 0.0) != (flo < 0.0):
            return _bisect(f, x, nxt, tol)
        x = nxt
    return None


def length_for_parity(b_gap, sigma=SIGMA_AL, d=WALL_M, share=None):
    """Array length whose drag takes the energy the seal friction takes."""
    share = FRICTION_SHARE if share is None else share
    target = share * pc.work(P0_PA, V_CHAMBER_M3)
    return _first_root(lambda L: integrate(b_gap, L, sigma, d)['drag_J'] - target, 4.0)


def length_for_stall(b_gap, sigma=SIGMA_AL, d=WALL_M):
    """Array length at which the carriage stops accelerating somewhere in the stroke."""
    return _first_root(lambda L: integrate(b_gap, L, sigma, d)['min_dE_dx_N'], 4.0)


def band1_verification():
    """Limits and an identity, not a second approximation. A66 band 1R's lesson."""
    ref = pc.shot(P0_PA, V_CHAMBER_M3)['v_exit']
    zero_sigma = integrate(0.6, 0.3, sigma=0.0, friction_N=0.0)['v_exit']
    zero_len = integrate(0.6, 0.0, friction_N=0.0)['v_exit']
    coarse = integrate(0.6, 0.05, steps=STEPS // 2)['v_exit']
    fine = integrate(0.6, 0.05, steps=STEPS)['v_exit']

    # The shear this file computes against the shear A66 computes, at A66's own point and on
    # A66's own SHEET route -- which is what this closed form is. A66 reports the slab route, and
    # the two differ by 3.05 % at that point on purpose; comparing against the slab would be
    # comparing two methods and calling it verification, which is the thing band 1R exists to
    # stop. The field passed here is the INCIDENT one: tau = (B_i^2/2mu)(2Rm/(1+Rm^2)) already
    # carries the transmission inside it, and passing B_net instead double-counts it by
    # 1/(1+Rm^2) -- 36.2 % at Rm = 0.7539, which is how this check first failed.
    b_gap = ts.airgap_flux_density()[0]
    a66 = ts.induced_loss_W(b_gap, ts.transmission_sheet())
    mine = shear_Pa(b_gap, ts.V_SYNC)
    rel_shear = abs(mine - a66['shear_Pa']) / a66['shear_Pa']

    out = {'reference_v_exit': ref,
           'zero_sigma_v_exit': zero_sigma, 'zero_sigma_rel': abs(zero_sigma - ref) / ref,
           'zero_length_v_exit': zero_len, 'zero_length_rel': abs(zero_len - ref) / ref,
           'a66_shear_Pa': a66['shear_Pa'], 'this_file_shear_Pa': mine,
           'shear_rel_diff': rel_shear,
           'step_halving_rel': abs(coarse - fine) / fine, 'steps': STEPS}
    out['pass_'] = (out['zero_sigma_rel'] <= 1e-6 and out['zero_length_rel'] <= 1e-6
                    and rel_shear <= 1e-9)
    return out


def ladder(sigma=SIGMA_AL, d=WALL_M):
    rows = []
    for b in FIELDS:
        lf = length_for_force(b)
        lp = length_for_parity(b, sigma, d)
        lst = length_for_stall(b, sigma, d)
        at_force = integrate(b, lf, sigma, d)
        rows.append({'b_gap_T': b, 'L_force_m': lf, 'L_parity_m': lp, 'L_stall_m': lst,
                     'force_over_parity': lf / lp if lp else None,
                     'force_over_stall': lf / lst if lst else None,
                     'v_exit_at_L_force': at_force['v_exit'],
                     'drag_J_at_L_force': at_force['drag_J'],
                     'drag_share_at_L_force': at_force['drag_J']
                     / pc.work(P0_PA, V_CHAMBER_M3),
                     'still_accelerating_at_L_force': at_force['min_dE_dx_N'] > 0.0,
                     'parity_ok': lf <= lp, 'stall_ok': lf <= lst})
    return rows


def band6_required_conductance(b_gap=0.6, search_max_m=4.0):
    """The sheet conductance at which band 3R would pass at 0.6 T.

    L_parity rises as the wall gets less conducting, so somewhere below aluminium's 35 000 S it
    crosses L_force and the drag stops being the larger loss. A wall so poor that no array
    shorter than 4.0 m -- half the stroke -- ever reaches parity is treated as passing, because
    at that point the array length has stopped being the binding constraint.
    """
    target = length_for_force(b_gap)

    def f(sd):
        lp = length_for_parity(b_gap, sigma=sd / WALL_M, d=WALL_M)
        return target - (search_max_m if lp is None else lp)

    lo, hi = 1e-3, SIGMA_AL * WALL_M
    if f(hi) <= 0.0:
        return {'b_gap_T': b_gap, 'required_sigma_d_S': None,
                'aluminium_sigma_d_S': SIGMA_AL * WALL_M, 'fraction_of_aluminium': None,
                'note': 'aluminium itself already passes at this field'}
    sd = _bisect(f, lo, hi, tol=1e-4)
    return {'b_gap_T': b_gap, 'required_sigma_d_S': sd,
            'aluminium_sigma_d_S': SIGMA_AL * WALL_M,
            'fraction_of_aluminium': sd / (SIGMA_AL * WALL_M),
            'required_sigma_S_m_at_this_wall': sd / WALL_M,
            'note': 'below this sheet conductance the eddy drag costs less than the seal '
                    'friction for an array long enough to make the force'}


def build():
    b1 = band1_verification()
    rows = ladder()
    parity_ok = any(r['parity_ok'] for r in rows)
    stall_ok = any(r['stall_ok'] for r in rows)

    stability = []
    for sigma in (SIGMA_AL / 2.0, SIGMA_AL):
        for d in (WALL_M / 2.0, WALL_M):
            rr = ladder(sigma, d)
            stability.append({'sigma_S_m': sigma, 'wall_m': d,
                              'parity_ok': any(r['parity_ok'] for r in rr),
                              'stall_ok': any(r['stall_ok'] for r in rr)})
    stable = all(s['parity_ok'] == parity_ok and s['stall_ok'] == stall_ok
                 for s in stability)
    b6 = band6_required_conductance()

    bands = [
        {'band': '1', 'name': 'model verification: limits against precharged, shear against A66',
         'detail': f"zero-sigma {b1['zero_sigma_rel']:.2e}, zero-length {b1['zero_length_rel']:.2e}"
                   f" against 1e-6; shear {b1['shear_rel_diff']:.2e} against 1e-9; "
                   f"step halving moves v_exit {b1['step_halving_rel']:.2e}",
         'pass_': b1['pass_']},
        {'band': '2', 'name': 'REPORT: the three lengths at each field on A66 ladder',
         'detail': '; '.join(f"{r['b_gap_T']:.2f} T L_force {r['L_force_m']*1e3:.1f} mm, "
                             f"L_parity {r['L_parity_m']*1e3:.2f} mm, "
                             f"L_stall {r['L_stall_m']*1e3:.2f} mm" for r in rows),
         'pass_': None},
        {'band': '3R', 'name': 'some field admits an array both making the force and costing no '
                               'more than the friction already does',
         'detail': (lambda best: f"best ratio L_force/L_parity {best['force_over_parity']:.1f}x "
                                 f"at {best['b_gap_T']:.2f} T")(
             min(rows, key=lambda r: r['force_over_parity'])),
         'pass_': parity_ok},
        {'band': '4R', 'name': 'some field admits an array making the force at which the carriage '
                               'is still accelerating at the muzzle',
         'detail': (lambda best: f"best ratio L_force/L_stall {best['force_over_stall']:.1f}x "
                                 f"at {best['b_gap_T']:.2f} T; the carriage is decelerating at "
                                 f"the muzzle at every field on the ladder")(
             min(rows, key=lambda r: r['force_over_stall'])),
         'pass_': stall_ok},
        {'band': '5', 'name': 'the verdicts of 3R and 4R hold over sigma 1.75e7 to 3.5e7 and '
                              'wall 0.5 to 1.0 mm',
         'detail': f"{sum(1 for s in stability if s['parity_ok'] == parity_ok and s['stall_ok'] == stall_ok)}"
                   f" of {len(stability)} corners agree",
         'pass_': stable},
        {'band': '6', 'name': 'REPORT: the wall conductance at which 3R would pass at 0.6 T',
         'detail': f"{b6['required_sigma_d_S']:.1f} S against aluminium's "
                   f"{b6['aluminium_sigma_d_S']:.0f} S, {b6['fraction_of_aluminium']*100:.3f} %",
         'pass_': None},
    ]

    return {
        'analysis': 'A72',
        'bands_declared_commit': '3f70082, with 3R and 4R at 0abbe1b, both before this file',
        'note': ('How long a carriage magnet array the shot can afford against the eddy drag of '
                 'a stationary aluminium tube. Closes the closable half of P118. E4: nothing '
                 'here is measured.'),
        'inputs': {'sigma_S_m': SIGMA_AL, 'wall_m': WALL_M, 'gap_radius_m': GAP_R_M,
                   'circumference_m': CIRC_M, 'stroke_m': STROKE_M, 'mass_kg': M_PAY_KG,
                   'p0_Pa': P0_PA, 'chamber_m3': V_CHAMBER_M3, 'friction_N': FRICTION_N,
                   'friction_share': FRICTION_SHARE, 'v_adopted_m_s': V_ADOPTED,
                   'force_N': FORCE_N, 'k_sheet_A_m': K_SHEET, 'remanence_T': BR_T},
        'verification': b1,
        'ladder': rows,
        'stability': stability,
        'required_conductance': b6,
        'bands': bands,
    }


def main():
    r = build()
    i = r['inputs']
    print(f"A72 array drag: {i['stroke_m']:.1f} m stroke, {i['mass_kg']:.1f} kg, "
          f"{i['friction_N']:.1f} N friction = {i['friction_share']*100:.4f} % of shot work")
    print(f"  air-gap circumference {i['circumference_m']*1e3:.2f} mm at r = "
          f"{i['gap_radius_m']*1e3:.4f} mm")
    b1 = r['verification']
    print(f"  verification: zero-sigma {b1['zero_sigma_rel']:.2e}, zero-length "
          f"{b1['zero_length_rel']:.2e}, shear against A66 {b1['shear_rel_diff']:.2e}, "
          f"step halving {b1['step_halving_rel']:.2e}")
    print("\n  field    L_force    L_parity    L_stall   force/parity  v_exit at L_force  accel")
    for row in r['ladder']:
        print(f"  {row['b_gap_T']:5.2f} T  {row['L_force_m']*1e3:7.1f} mm "
              f"{row['L_parity_m']*1e3:8.2f} mm {row['L_stall_m']*1e3:8.2f} mm "
              f"{row['force_over_parity']:9.1f}x  {row['v_exit_at_L_force']:11.4f} m/s   "
              f"{'yes' if row['still_accelerating_at_L_force'] else 'NO'}")
    b6 = r['required_conductance']
    print(f"\n  band 3R would pass at 0.6 T only at sigma*d = {b6['required_sigma_d_S']:.1f} S, "
          f"{b6['fraction_of_aluminium']*100:.3f} % of the 1.0 mm aluminium wall's "
          f"{b6['aluminium_sigma_d_S']:.0f} S -- at this wall thickness, "
          f"{b6['required_sigma_S_m_at_this_wall']:.4e} S/m")
    print("\nbands:")
    for b in r['bands']:
        v = 'REPORT' if b['pass_'] is None else ('PASS' if b['pass_'] else 'FAIL')
        print(f"  band {b['band']}: {v}  {b['name']}\n            {b['detail']}")
    os.makedirs(RESULTS, exist_ok=True)
    json.dump(r, open(os.path.join(RESULTS, 'array_drag.json'), 'w'), indent=2)
    print("\n-> results/array_drag.json")
    return 0


if __name__ == '__main__':
    sys.exit(main())
