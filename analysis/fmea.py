"""
VOLLEY | FMEA: what each failure costs, and what per-element reliability the design needs.

WHY THIS EXISTS
---------------
E30 established the architecture's shape: a spring dispenser is twelve independent one-shot
mechanisms in parallel, VOLLEY is one mechanism in series with itself cycled twelve times. It
also established the two numbers that decide whether the trade is worth taking --

    per-shot p = 0.9347  to match a 0.99-reliable spring on DELIVERED ORBITAL LIFE
    per-shot p = 0.9985  to match it on SATELLITE COUNT

-- and then found that **nothing in the repository estimates p**. This file estimates it, and
enumerates what each failure actually costs.

WHAT THIS IS NOT
----------------
**Not a reliability prediction.** No element here has a measured failure rate, a qualification
history, or a cycle-life test behind it. Per-cycle reliabilities are PARAMETERS, swept rather
than asserted, and the useful output is the inverse question: given the architecture, what must
each element achieve for the design to beat a spring at all?

Anyone quoting a single p from this file is misusing it.
"""
import json
import os

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
N_SHOTS = 12
N_CASSETTES = 2
SHOTS_PER_CASSETTE = N_SHOTS // N_CASSETTES

# (element, scope, cycles over a campaign, what its failure costs, note)
#   scope 'shared'    -> failure forfeits every remaining shot
#   scope 'cassette'  -> failure forfeits the remaining shots of ONE cassette
#   scope 'shot'      -> failure costs exactly one satellite
ELEMENTS = [
    ("Sled chassis and rollers", "shared", 12, "all remaining",
     "One sled serves all twelve cells. No redundant sled, no manual release. Review item 22"),
    ("Stator winding", "shared", 12, "all remaining",
     "Segmented per paper.tex Sec.VII, so losing one segment degrades rather than stops. "
     "NOT credited below -- segmentation is stated, never analysed"),
    ("Power converter (SiC bridge)", "shared", 12, "all remaining",
     "No radiation or SEE qualification path exists. Review item 25"),
    ("Energy store (bank or flywheel)", "shared", 12, "all remaining",
     "P26: the bank cannot source the shot on purchasable parts. A25's flywheel adds a "
     "rotating mechanism"),
    ("Avionics and shot sequencer", "shared", 12, "all remaining", ""),
    ("Position sensing / commutation", "shared", 12, "all remaining",
     "A synchronous machine that loses position feedback cannot commutate"),
    ("Eddy brake", "shared", 12, "all remaining",
     "PROVISIONAL: pole plates lightened on structural reasoning alone, no magnetic sizing. "
     "P28. Failure may also eject the sled -- review item 23"),
    ("Sled return", "shared", 12, "all remaining", ""),
    ("Launch lock release", "shared", 1, "all",
     "One-shot, fires once. The only shared element that does not cycle"),
    ("Cassette follower drive", "cassette", 6, "six", ""),
    ("Escapement", "cassette", 6, "six", ""),
    ("Retention gate (2 x D9 pins)", "cassette", 6, "six",
     "A22 resized D6 -> D9 for the vibration case. Cycle life untested"),
    ("Individual release event", "shot", 1, "one", ""),
]


def campaign(r_shared, r_cassette, r_shot, n=N_SHOTS):
    """Expected satellites delivered, by simulating the serial structure directly.

    Shared elements must survive every shot up to and including the one being fired.
    Cassette elements must survive that cassette's own cycle count. A shot element failing
    costs only that satellite.
    """
    n_shared_cycling = sum(1 for e in ELEMENTS if e[1] == 'shared' and e[2] > 1)
    n_shared_once = sum(1 for e in ELEMENTS if e[1] == 'shared' and e[2] == 1)
    n_cassette = sum(1 for e in ELEMENTS if e[1] == 'cassette')
    n_shot = sum(1 for e in ELEMENTS if e[1] == 'shot')

    p_shared_per_shot = r_shared ** n_shared_cycling
    p_shared_once = r_shared ** n_shared_once
    p_cassette_per_cycle = r_cassette ** n_cassette
    p_shot_each = r_shot ** n_shot

    expected = 0.0
    for k in range(1, n + 1):
        cyc = (k + 1) // 2                       # cassettes alternate, so cycle index per cassette
        expected += (p_shared_once
                     * p_shared_per_shot ** k
                     * p_cassette_per_cycle ** cyc
                     * p_shot_each)
    p_eff = p_shared_per_shot * p_cassette_per_cycle ** 0.5 * p_shot_each
    return expected, p_eff


def required_element_r(target_expected, lo=0.9, hi=1.0):
    """Inverse question: what per-element per-cycle reliability reaches a target delivery?"""
    for _ in range(300):
        m = (lo + hi) / 2
        if campaign(m, m, m)[0] < target_expected:
            lo = m
        else:
            hi = m
    return hi


if __name__ == '__main__':
    print("SINGLE-FAILURE-LOSES-N\n")
    print(f"{'element':34s} {'scope':>9s} {'cycles':>7s}  costs")
    for name, scope, cycles, cost, note in ELEMENTS:
        print(f"{name:34s} {scope:>9s} {cycles:7d}  {cost}")
    shared = [e for e in ELEMENTS if e[1] == 'shared']
    print(f"\n{len(shared)} of {len(ELEMENTS)} elements forfeit the REMAINING MANIFEST on a "
          f"single failure.")
    print(f"A spring dispenser has ZERO such elements: every failure costs exactly one satellite.\n")

    print("EXPECTED DELIVERY vs per-element per-cycle reliability\n")
    print(f"{'r/element':>10s} {'p per shot':>11s} {'E[sats]':>9s} {'vs spring 0.99 (11.88)':>24s}")
    rows = []
    for r in (0.9999, 0.999, 0.995, 0.99, 0.98, 0.95):
        exp, p_eff = campaign(r, r, r)
        rows.append(dict(r=r, p_shot=p_eff, expected=exp))
        print(f"{r:10.4f} {p_eff:11.4f} {exp:9.3f} {exp-11.88:+24.3f}")

    # E30's two crossover targets, expressed back as per-element requirements.
    from reliability_architecture import lives, volley_expected, spring_expected
    base, spring_life, volley_life = lives()
    tgt_years = spring_expected(0.99) * spring_life / volley_life
    tgt_sats = spring_expected(0.99)
    r_years, r_sats = required_element_r(tgt_years), required_element_r(tgt_sats)
    print(f"\nE30's break-even, expressed as a per-element requirement:")
    print(f"  to match a 0.99 spring on DELIVERED LIFE  ({tgt_years:.2f} sats): "
          f"r >= {r_years:.5f} per element per cycle")
    print(f"  to match it on SATELLITE COUNT           ({tgt_sats:.2f} sats): "
          f"r >= {r_sats:.5f} per element per cycle")
    e_y, _ = campaign(r_years, r_years, r_years)
    print(f"\n  {len(shared)} shared elements x 12 cycles is {len(shared)*12} chances to fail.")
    print(f"  At r = {r_years:.5f} each element survives the campaign with probability "
          f"{r_years**12:.4f}.")

    os.makedirs(RESULTS, exist_ok=True)
    json.dump(dict(n_elements=len(ELEMENTS), n_shared=len(shared),
                   elements=[dict(name=n, scope=s, cycles=c, costs=k, note=t)
                             for n, s, c, k, t in ELEMENTS],
                   sweep=rows, required_r_delivered_life=r_years,
                   required_r_satellite_count=r_sats),
              open(os.path.join(RESULTS, 'fmea.json'), 'w'), indent=2)
    print("\n-> results/fmea.json")
