"""
A34: does the payload's cradle rattle settle before the force is removed?

Bands declared in validation/A34_cradle_restitution.md at 77d45bb, BEFORE this file existed.

THE PROBLEM
-----------
A23 found the payload's centre of mass sits 70 mm off the thrust line, so the push applies a
28.92 N.m moment and 688 rad/s^2 of angular acceleration. The cradle holds it with clearance,
so it crosses that clearance and arrives at 36-231 deg/s -- 18 to 115x the 2 deg/s tip-off
band. A23 stopped there, because whether the rebound has settled by release "depends on a
restitution model this project does not have".

A body bouncing in a clearance under constant acceleration is the bouncing-ball problem. Each
impact returns a fraction e of the approach rate; the flight after impact k lasts 2 e^k w0/alpha;
the series sums to

    t_settle = (2 w0 / alpha) * e / (1 - e)

finite for every e < 1. So it always settles. The question is only whether it settles before
the force is removed -- after that alpha = 0, nothing further settles, and whatever rate
survives is what the satellite leaves with.

Provenance: model output. Restitution is SWEPT, not measured. E4 stands.
"""
import json
import math
import os

import numpy as np

import motor_model as mm

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

# All three imported from A23 rather than restated.
I_PAYLOAD = 0.042           # kg.m^2, 3U about its own transverse axis
COM_OFFSET = 0.070          # m, centre of mass off the thrust line
TIPOFF_BAND = 2.0           # deg/s, the flown NRCSD figure, P30
# THE LEVER THAT TAKES UP THE CLEARANCE IS NOT THE ONE THAT APPLIES THE MOMENT.
# The moment arm is the 70 mm centre-of-mass offset. The clearance is taken up at the cradle
# CONTACTS, which sit at the payload's ends, so a rotation theta about the centre moves them
# by (half length) * theta. The first run of this file used 70 mm for both and came out
# 56 % high on arrival rate and 143 % high on preload -- band 1 caught it.
CONTACT_LEVER = 0.3405 / 2  # m, half the 3U length
COAST_MS = 12.2             # ms of zero-force coast before release
CLEARANCES_MM = (0.05, 0.10, 0.25, 0.50, 1.00, 2.00)
E_RANGE = (0.1, 0.3, 0.5, 0.7, 0.9)
E_ALUMINIUM = 0.7           # top of the published aluminium-on-aluminium range


def moment_and_alpha(F=None):
    F = mm.shot(mm.thrust_constant()[0])['F_cmd'] * 0.9 / 0.9 if F is None else F
    # A23 uses the per-payload share of the commanded force; take it from the shot directly.
    F_payload = mm.M_SAT * mm.shot(mm.thrust_constant()[0])['a_g'] * 9.81
    M = F_payload * COM_OFFSET
    return F_payload, M, M / I_PAYLOAD


def arrival_rate(clearance_m, alpha, lever=CONTACT_LEVER):
    """Angular rate on first contact after crossing the clearance.

    The clearance is a linear gap at the contact; the angle available is gap/lever.
    theta = 0.5 alpha t^2  ->  t = sqrt(2 theta / alpha),  omega = alpha t.
    """
    theta = clearance_m / lever
    return math.sqrt(2 * theta * alpha)


def settle_time(w0, alpha, e):
    """Total time from first impact until bouncing stops."""
    if e >= 1.0:
        return float('inf')
    return (2 * w0 / alpha) * e / (1 - e)


def residual_rate(w0, alpha, e, t_available):
    """Angular rate at the instant force is removed.

    Walk the bounce series: flight k lasts 2 e^(k+1) w0 / alpha and starts at rate e^(k+1) w0.
    If the force is removed mid-flight, that flight's rate is what survives; if the series has
    completed, the payload is resting on the stop and the rate is zero.
    """
    t = 0.0
    w = w0
    for _ in range(10000):
        w *= e
        flight = 2 * w / alpha
        if t + flight > t_available:
            return w                      # still airborne when the force goes
        t += flight
        if w < 1e-9:
            break
    return 0.0


def preload_for_no_liftoff(M, lever=CONTACT_LEVER):
    """Contact force that reacts the offset moment so the payload never leaves its seat.

    Two contacts a half-length either side of the centre react the moment as a couple.
    """
    return M / (2 * lever)


if __name__ == '__main__':
    F_payload, M, alpha = moment_and_alpha()
    shot = mm.shot(mm.thrust_constant()[0])
    t_powered = (shot['t_ms'] - COAST_MS) / 1e3

    print("A34: does the cradle rattle settle before release?\n")
    print(f"payload {mm.M_SAT} kg at {shot['a_g']:.2f} g -> {F_payload:.1f} N, "
          f"{COM_OFFSET*1e3:.0f} mm off the thrust line")
    print(f"moment  {M:.2f} N.m / I {I_PAYLOAD} kg.m2 = {alpha:.0f} rad/s2")
    print(f"levers  moment arm {COM_OFFSET*1e3:.0f} mm; cradle contacts at "
          f"{CONTACT_LEVER*1e3:.1f} mm -- these are NOT the same lever")
    print(f"stroke  {shot['t_ms']:.1f} ms, of which {COAST_MS} ms is zero-force coast "
          f"-> {t_powered*1e3:.1f} ms powered\n")

    # ---- Band 1: reproduce A23's arrival rates. ----
    a23 = {0.05: 36.5}                     # the published row this sheet checks against
    print(f"{'clearance':>10} {'arrival':>10} {'A23':>8}")
    rows = []
    for c in CLEARANCES_MM:
        w = arrival_rate(c / 1e3, alpha)
        rows.append(dict(clearance_mm=c, arrival_deg_s=math.degrees(w)))
        ref = f"{a23[c]:8.1f}" if c in a23 else "        "
        print(f"{c:9.2f}mm {math.degrees(w):8.1f} d/s {ref}")
    w_check = math.degrees(arrival_rate(0.05e-3, alpha))
    e1 = 100 * abs(w_check - a23[0.05]) / a23[0.05]
    print(f"\nBAND 1  0.05 mm arrival {w_check:.2f} vs A23's {a23[0.05]} deg/s "
          f"-> {e1:.2f} %   (band <= 5 %)")

    # ---- Bands 2, 3, 4: settling and residual. ----
    worst_c = max(CLEARANCES_MM)
    w0_worst = arrival_rate(worst_c / 1e3, alpha)
    print(f"\n{'e':>5} {'settle ms':>10} {'residual, worst clearance':>26}")
    sweep = []
    for e in E_RANGE:
        ts = settle_time(w0_worst, alpha, e)
        wr = residual_rate(w0_worst, alpha, e, t_powered)
        sweep.append(dict(e=e, settle_ms=ts * 1e3, residual_deg_s=math.degrees(wr)))
        print(f"{e:5.1f} {ts*1e3:9.3f} {math.degrees(wr):22.4f} d/s")

    ts_al = settle_time(w0_worst, alpha, E_ALUMINIUM)
    print(f"\nBAND 2  settling at e = {E_ALUMINIUM} on the {worst_c} mm clearance: "
          f"{ts_al*1e3:.2f} ms   (band < {t_powered*1e3:.1f} ms powered stroke)")

    worst_res = max(math.degrees(residual_rate(arrival_rate(c / 1e3, alpha), alpha,
                                               E_ALUMINIUM, t_powered))
                    for c in CLEARANCES_MM)
    print(f"BAND 3  residual rate at force removal, worst over every clearance, "
          f"e = {E_ALUMINIUM}: {worst_res:.4f} deg/s   (band < {TIPOFF_BAND})")

    lo, hi = 0.0, 0.999999
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if settle_time(w0_worst, alpha, mid) < t_powered:
            lo = mid
        else:
            hi = mid
    e_star = lo
    print(f"BAND 4  critical restitution, above which it does not settle in time: "
          f"e* = {e_star:.4f}   (band >= 0.80)")

    # ---- Band 5: the preload. ----
    pre = preload_for_no_liftoff(M)
    print(f"BAND 5  preload to prevent lift-off: {pre:.1f} N per contact "
          f"(A23 states > 85 N)   (band within 20 %)")
    e5 = 100 * abs(pre - 85.0) / 85.0

    b = {
        '1': ("arrival rate reproduces A23 within 5 %", f"{e1:.2f} %", bool(e1 <= 5.0)),
        '2': (f"settles inside the {t_powered*1e3:.1f} ms powered stroke at e = {E_ALUMINIUM}",
              f"{ts_al*1e3:.2f} ms", bool(ts_al < t_powered)),
        '3': (f"residual rate at force removal < {TIPOFF_BAND} deg/s",
              f"{worst_res:.4f} deg/s", bool(worst_res < TIPOFF_BAND)),
        '4': ("critical restitution e* >= 0.80", f"{e_star:.4f}", bool(e_star >= 0.80)),
        '5': ("preload within 20 % of A23's 85 N", f"{pre:.1f} N", bool(e5 <= 20.0)),
    }
    print("\nbands:")
    npass = 0
    for kk in sorted(b):
        name, detail, ok = b[kk]
        npass += ok
        print(f"  band {kk}: {'PASS' if ok else 'FAIL'}  {name}\n            {detail}")
    print(f"\n{npass} of {len(b)} bands pass.")

    os.makedirs(RESULTS, exist_ok=True)
    json.dump(dict(I_payload=I_PAYLOAD, com_offset_m=COM_OFFSET, F_payload_N=F_payload,
                   moment_Nm=M, alpha_rad_s2=alpha, t_powered_ms=t_powered * 1e3,
                   coast_ms=COAST_MS, arrival=rows, restitution_sweep=sweep,
                   e_critical=e_star, settle_at_e07_ms=ts_al * 1e3,
                   residual_worst_deg_s=worst_res, preload_N=pre,
                   restitution="SWEPT, NOT MEASURED. No coupon test exists. E4 stands.",
                   bands=[dict(band=kk, name=b[kk][0], detail=b[kk][1], passed=b[kk][2])
                          for kk in sorted(b)]),
              open(os.path.join(RESULTS, 'cradle_restitution.json'), 'w'), indent=2)
    print("-> results/cradle_restitution.json")
