"""
VOLLEY | Series-versus-parallel: what the architecture costs in delivered satellites.

THE CRITICISM THIS ANSWERS
--------------------------
A spring dispenser is twelve INDEPENDENT one-shot mechanisms in PARALLEL. One failure costs
one satellite. VOLLEY is one mechanism in SERIES with itself, cycled twelve times, shared by
the whole manifest: the sled, the stator, the bank, the sequencer and the brake all serve
every shot, and the escapement and gate cycle twelve times each.

**VOLLEY converts twelve one-shot parallel mechanisms into one twelve-cycle series mechanism.**
That is a real and unfavourable structural change and no amount of component quality removes it.

WHAT IS COMPUTED
----------------
If the shared chain survives each shot with probability p and a failure at shot k forfeits
every satellite from k onward, expected delivery is sum_{k=1..12} p^k -- which falls away from
12p much faster than a spring's independent 12q.

Then the same comparison on DELIVERED ORBITAL LIFE, because a satellite the deployer never
releases delivers nothing, and one it does release delivers more than a spring's would.

Provenance: model output. **p is not estimated here and is not known** -- no FMEA, fault tree
or parts count exists for this design. That absence is the finding, and is logged as E30.
"""
import json
import os

import astro
import motor_model as mm

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
N_SHOTS = 12
ALT = 450e3
V_RATED = mm.operating_point()['v_exit']


def lives():
    base = astro.lifetime(astro.RE + ALT, 0.0)
    a, e = astro.boosted_elements(ALT, V_RATED)
    volley = astro.lifetime(abs(a), abs(e))
    a, e = astro.boosted_elements(ALT, 2.5)
    spring = astro.lifetime(abs(a), abs(e))
    return base, spring, volley


def volley_expected(p, n=N_SHOTS):
    """Shared serial chain: failure at shot k forfeits shots k..n."""
    return sum(p ** k for k in range(1, n + 1))


def spring_expected(q, n=N_SHOTS):
    """Independent parallel chains: each failure costs exactly one satellite."""
    return n * q


def crossover(metric, q_spring=0.99):
    """Per-shot p at which VOLLEY matches a q-reliable spring on `metric`."""
    base, spring, volley = lives()
    tgt = (spring_expected(q_spring) * (spring if metric == 'years' else 1.0))
    lo, hi = 0.0, 1.0
    for _ in range(200):
        m = (lo + hi) / 2
        val = volley_expected(m) * (volley if metric == 'years' else 1.0)
        if val < tgt:
            lo = m
        else:
            hi = m
    return hi


if __name__ == '__main__':
    base, spring, volley = lives()
    print(f"orbital life at {ALT/1e3:.0f} km: unboosted {base:.3f} yr, "
          f"spring(2.5 m/s) {spring:.3f}, VOLLEY({V_RATED:.3f}) {volley:.3f}")
    print(f"reward per DELIVERED satellite: {volley/spring:.3f}x\n")
    print(f"{'p or q':>8s} {'VOLLEY sats':>12s} {'spring sats':>12s} "
          f"{'VOLLEY yr':>10s} {'spring yr':>10s} {'ratio':>7s}")
    rows = []
    for p in (0.999, 0.99, 0.98, 0.95, 0.935, 0.90, 0.85, 0.80):
        vn, sn = volley_expected(p), spring_expected(p)
        vy, sy = vn * volley, sn * spring
        print(f"{p:8.3f} {vn:12.3f} {sn:12.3f} {vy:10.3f} {sy:10.3f} {vy/sy:7.3f}")
        rows.append(dict(p=p, volley_sats=vn, spring_sats=sn, volley_years=vy,
                         spring_years=sy, ratio=vy / sy))

    c_years, c_sats = crossover('years'), crossover('sats')
    print(f"\nTo match a 0.99-reliable spring:")
    print(f"  on DELIVERED ORBITAL LIFE  VOLLEY needs per-shot p = {c_years:.4f}")
    print(f"  on SATELLITE COUNT         VOLLEY needs per-shot p = {c_sats:.4f}")
    print(f"\nThe gap between those two numbers is the risk/reward ratio.")

    os.makedirs(RESULTS, exist_ok=True)
    json.dump(dict(base_yr=base, spring_yr=spring, volley_yr=volley,
                   reward_per_satellite=volley / spring, n_shots=N_SHOTS,
                   crossover_p_years=c_years, crossover_p_satellites=c_sats,
                   rows=rows),
              open(os.path.join(RESULTS, 'reliability_architecture.json'), 'w'), indent=2)
    print("\n-> results/reliability_architecture.json")
