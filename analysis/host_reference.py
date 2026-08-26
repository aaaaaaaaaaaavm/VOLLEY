"""
VOLLEY | Host-reference propulsion arithmetic for docs/HOST_REFERENCE_CASES.md.

WHAT THIS IS
------------
The host stage does the coarse orbital repositioning and VOLLEY does the fine
per-satellite release state (docs/MISSION_ARCHITECTURE.md section 2). Every number
below is on the host side of that line. Nothing here models the deployer.

The question this answers is not "can engine X fly VOLLEY". It is: given a stage
carrying a restartable main engine of a stated thrust class, how long are the burns
a distributed-delivery campaign actually needs, and does one engine cover the whole
manoeuvre range or only the top of it?

EVERY INPUT IS A DECLARED VOLLEY REFERENCE ASSUMPTION EXCEPT WHERE MARKED PUBLIC
-------------------------------------------------------------------------------
The thrust class and the propellant family are public data for the first reference
case. Specific impulse, stage mass, minimum burn, restart count, coast interval and
disposal reserve are NOT. They are reference assumptions chosen by this project so
that the arithmetic has somewhere to start, and they carry no provider's name.
`PROVENANCE` below records which is which, and the JSON carries it into the document
so a reader never has to guess.

MODEL
-----
Impulsive-equivalent, constant thrust, constant Isp, no gravity loss, no steering
loss, no throttling. For manoeuvres of a few tens of m/s at these burn durations the
finite-burn correction is small, and a first-order model is the honest resolution for
inputs this soft. It is not a trajectory tool and must not be read as one.

    mdot = F / (Isp * g0)                       mass flow, kg/s
    dv   = Isp * g0 * ln(m0 / mf)               rocket equation
    mp   = m0 * (1 - exp(-dv / (Isp * g0)))     propellant for a manoeuvre
    tb   = mp / mdot                            burn duration
    dv(t)= Isp * g0 * ln(m0 / (m0 - mdot * t))  what a burn of length t buys

Disposal reserve is removed FIRST. Customer manoeuvres spend what is left, which is
the only ordering that cannot end a campaign with no way to dispose of the stage
(docs/MISSION_ARCHITECTURE.md section 7).

Provenance: model output, closed-form arithmetic, no solver. Nothing here is measured
and no launch provider has supplied any figure in it (E5).
"""
import json
import math
import os
import sys

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

G0 = 9.80665                    # CODATA standard gravity, exact by definition

# --------------------------------------------------------------------------------
# The reference point. Read PROVENANCE before quoting any of it.
# --------------------------------------------------------------------------------
THRUST_N = 20.0e3               # PUBLIC (class figure), condition unstated by the source
ISP_S = 300.0                   # VOLLEY ASSUMPTION. No public Isp exists for the case engine
STAGE_MASS_KG = 1000.0          # VOLLEY ASSUMPTION. No public stage mass exists
MIN_BURN_S = 2.0                # VOLLEY ASSUMPTION. No public minimum stable burn exists
COAST_MIN = 10.0                # VOLLEY ASSUMPTION. No public restart interval exists
RESTARTS_PLANNED = 4            # VOLLEY ASSUMPTION. No public restart rating exists
RESTART_CONTINGENCY = 1         # VOLLEY ASSUMPTION
CAMPAIGN_H = 4.0                # VOLLEY ASSUMPTION. No public coast limit exists
DISPOSAL_FRACTION = 0.20        # VOLLEY ASSUMPTION
USABLE_PROP_KG = 150.0          # VOLLEY ASSUMPTION, post-primary usable propellant

PROVENANCE = {
    'thrust_N': 'PUBLIC_CLASS_FIGURE, thrust condition not stated by the source',
    'propellant': 'PUBLIC, LOX/kerosene',
    'isp_s': 'VOLLEY_ASSUMPTION, no public figure exists',
    'stage_mass_kg': 'VOLLEY_ASSUMPTION, no public figure exists',
    'min_burn_s': 'VOLLEY_ASSUMPTION, no public figure exists',
    'coast_min': 'VOLLEY_ASSUMPTION, no public figure exists',
    'restarts_planned': 'VOLLEY_ASSUMPTION, no public figure exists',
    'campaign_h': 'VOLLEY_ASSUMPTION, no public figure exists',
    'disposal_fraction': 'VOLLEY_ASSUMPTION',
    'usable_prop_kg': 'VOLLEY_ASSUMPTION',
}

# Sensitivity envelopes, all VOLLEY-declared.
STAGE_MASSES = [500.0, 1000.0, 2000.0, 3000.0]
DELTA_VS = [5.0, 10.0, 20.0, 40.0, 100.0]
ISPS = [285.0, 300.0, 320.0]
BURN_TIMES = [0.5, 1.0, 2.0, 5.0]
RESERVES = [0.10, 0.20, 0.30]

# From analysis/astro.py. Repeated rather than imported because astro.py pulls the whole
# motor model in on import, and this file must not depend on the deployer to run.
MU = 3.986004418e14
RE = 6378.137e3


def mass_flow(thrust_N=THRUST_N, isp_s=ISP_S):
    """Propellant mass flow, kg/s."""
    return thrust_N / (isp_s * G0)


def propellant_for(dv, m0, isp_s=ISP_S):
    """Propellant consumed by a manoeuvre of dv from initial mass m0, kg."""
    return m0 * (1.0 - math.exp(-dv / (isp_s * G0)))


def burn_time_for(dv, m0, thrust_N=THRUST_N, isp_s=ISP_S):
    """Duration of a constant-thrust burn delivering dv from m0, seconds."""
    return propellant_for(dv, m0, isp_s) / mass_flow(thrust_N, isp_s)


def dv_from_burn(t, m0, thrust_N=THRUST_N, isp_s=ISP_S):
    """What a burn of length t buys from initial mass m0, m/s."""
    mp = mass_flow(thrust_N, isp_s) * t
    if mp >= m0:
        raise ValueError('burn consumes the whole stage')
    return isp_s * G0 * math.log(m0 / (m0 - mp))


def circular_v(alt_km):
    """Circular orbital speed, m/s."""
    return math.sqrt(MU / (RE + alt_km * 1e3))


def hohmann_raise(alt_km, d_alt_km):
    """Two-impulse coplanar altitude change, total dv, m/s."""
    r1 = RE + alt_km * 1e3
    r2 = r1 + d_alt_km * 1e3
    a = 0.5 * (r1 + r2)
    dv1 = math.sqrt(MU * (2.0 / r1 - 1.0 / a)) - math.sqrt(MU / r1)
    dv2 = math.sqrt(MU / r2) - math.sqrt(MU * (2.0 / r2 - 1.0 / a))
    return abs(dv1) + abs(dv2)


def plane_change(alt_km, d_inc_deg):
    """Single-impulse inclination change at circular speed, m/s."""
    return 2.0 * circular_v(alt_km) * math.sin(math.radians(d_inc_deg) / 2.0)


# --------------------------------------------------------------------------------
# Tables
# --------------------------------------------------------------------------------
def burn_grid():
    """Burn duration and propellant for every (stage mass, dv, Isp) combination."""
    rows = []
    for isp in ISPS:
        for m0 in STAGE_MASSES:
            for dv in DELTA_VS:
                mp = propellant_for(dv, m0, isp)
                rows.append({
                    'isp_s': isp, 'stage_mass_kg': m0, 'dv_ms': dv,
                    'propellant_kg': mp,
                    'burn_s': mp / mass_flow(THRUST_N, isp),
                    'propellant_fraction': mp / m0,
                })
    return rows


def minimum_impulse():
    """What the shortest credible burns buy, across the stage-mass envelope."""
    rows = []
    for m0 in STAGE_MASSES:
        for t in BURN_TIMES:
            rows.append({
                'stage_mass_kg': m0, 'burn_s': t,
                'dv_ms': dv_from_burn(t, m0),
                'propellant_kg': mass_flow() * t,
            })
    return rows


def granularity(fine_dv=5.0):
    """The manoeuvre the assumed minimum burn cannot go below, per stage mass.

    This is the result that decides whether one engine covers the whole manoeuvre
    range: if the smallest burn the stage can command already overshoots the smallest
    manoeuvre the mission wants, the main engine is the wrong actuator for that end.

    `min_burn_for_fine_s` inverts the question into the form a provider can answer:
    not "is 2 s too long" but "what minimum stable burn would this stage need in
    order to command a 5 m/s manoeuvre on the main engine at all".
    """
    rows = []
    ten_km = hohmann_raise(500.0, 10.0)
    for m0 in STAGE_MASSES:
        dv_min = dv_from_burn(MIN_BURN_S, m0)
        rows.append({
            'stage_mass_kg': m0,
            'min_burn_s': MIN_BURN_S,
            'dv_floor_ms': dv_min,
            'altitude_step_km': dv_min / ten_km * 10.0,
            'exceeds_fine_manoeuvre': dv_min > fine_dv,
            'overshoot_factor': dv_min / fine_dv,
            'min_burn_for_fine_s': burn_time_for(fine_dv, m0),
        })
    return rows


def orbit_period_min(alt_km=500.0):
    """Orbital period, minutes. The real pace of a phasing campaign."""
    a = RE + alt_km * 1e3
    return 2.0 * math.pi * math.sqrt(a ** 3 / MU) / 60.0


def disposal_budget(usable_kg=USABLE_PROP_KG, m0=STAGE_MASS_KG):
    """Reserve removed first, customer manoeuvres spend what is left."""
    rows = []
    for f in RESERVES:
        reserve = usable_kg * f
        customer = usable_kg - reserve
        rows.append({
            'reserve_fraction': f,
            'reserve_kg': reserve,
            'customer_kg': customer,
            'customer_dv_ms': ISP_S * G0 * math.log(m0 / (m0 - customer)),
            'reserve_dv_ms': ISP_S * G0 * math.log((m0 - customer) / (m0 - usable_kg)),
        })
    return rows


def mission_cases():
    """Three post-primary campaigns, priced on the declared assumptions.

    Case A is the one that matters most to the architecture: it establishes that
    VOLLEY does not need a restartable host to exist at all.
    """
    usable = USABLE_PROP_KG
    reserve = usable * DISPOSAL_FRACTION
    budget = usable - reserve

    def campaign(name, steps, batches):
        m = STAGE_MASS_KG
        spent = 0.0
        legs = []
        for dv in steps:
            mp = propellant_for(dv, m, ISP_S)
            legs.append({'dv_ms': dv, 'propellant_kg': mp,
                         'burn_s': mp / mass_flow(), 'mass_before_kg': m})
            m -= mp
            spent += mp
        return {
            'case': name,
            'restarts': len(steps),
            'batches': batches,
            'total_dv_ms': sum(steps),
            'propellant_kg': spent,
            'budget_kg': budget,
            'within_budget': spent <= budget,
            'margin_kg': budget - spent,
            'coast_floor_h': (len(steps) * COAST_MIN) / 60.0,
            'one_orbit_pacing_h': len(steps) * orbit_period_min() / 60.0,
            'legs': legs,
        }

    return [
        campaign('A, rapid deployment, no post-primary restart', [], 1),
        campaign('B, moderate distributed delivery', [20.0, 20.0, 20.0], 3),
        campaign('C, upper-bound sensitivity', [40.0, 40.0, 40.0, 40.0, 40.0], 5),
    ]


def batch_trade(n_sats=12):
    """One burn per satellite against 2, 3 and 4 batches, at the same shell spacing.

    The comparison is deliberately unfair to batching in one respect: it holds the
    per-burn dv fixed, so more burns means more total dv AND more restarts. That is
    the real trade, because the shells are what the customer buys and the burns are
    what the stage pays.
    """
    dv_per_burn = 20.0
    rows = []
    for n_batches in [n_sats, 4, 3, 2]:
        m = STAGE_MASS_KG
        spent = 0.0
        burns = n_batches - 1          # no burn is needed before the first batch
        for _ in range(burns):
            mp = propellant_for(dv_per_burn, m, ISP_S)
            m -= mp
            spent += mp
        rows.append({
            'batches': n_batches,
            'satellites_per_batch': n_sats / n_batches,
            'restarts': burns,
            'total_dv_ms': burns * dv_per_burn,
            'propellant_kg': spent,
            'coast_time_h': burns * COAST_MIN / 60.0,
        })
    return rows


def plane_change_check():
    """Re-derive MISSION_ARCHITECTURE.md section 5 rather than quoting it."""
    rows = []
    for alt in [350.0, 500.0, 700.0]:
        rows.append({
            'alt_km': alt,
            'v_circ_ms': circular_v(alt),
            'plane_1deg_ms': plane_change(alt, 1.0),
            'plane_0p1deg_ms': plane_change(alt, 0.1),
            'raise_10km_ms': hohmann_raise(alt, 10.0),
            'ratio_1deg_to_10km': plane_change(alt, 1.0) / hohmann_raise(alt, 10.0),
        })
    return rows


# --------------------------------------------------------------------------------
# Self-checks. These are arithmetic identities, not acceptance bands.
# --------------------------------------------------------------------------------
def self_test():
    """Every check here is a property the closed forms must satisfy identically."""
    fails = []

    # 1. Rocket equation and mass flow invert each other.
    dv, m0 = 20.0, 1000.0
    tb = burn_time_for(dv, m0)
    if abs(dv_from_burn(tb, m0) - dv) > 1e-9:
        fails.append('rocket equation and burn-time inverse disagree')

    # 2. Mass flow matches the definition of Isp.
    if abs(mass_flow() * ISP_S * G0 - THRUST_N) > 1e-6:
        fails.append('mass flow does not reproduce thrust')

    # 3. Burn time rises with stage mass at fixed dv.
    tb_series = [burn_time_for(20.0, m) for m in STAGE_MASSES]
    if tb_series != sorted(tb_series):
        fails.append('burn time is not monotonic in stage mass')

    # 4. Propellant falls as Isp rises at fixed dv and mass.
    mp_series = [propellant_for(20.0, 1000.0, i) for i in ISPS]
    if mp_series != sorted(mp_series, reverse=True):
        fails.append('propellant is not monotonic in Isp')

    # 5. dv from a burn rises with burn length.
    dv_series = [dv_from_burn(t, 1000.0) for t in BURN_TIMES]
    if dv_series != sorted(dv_series):
        fails.append('dv is not monotonic in burn time')

    # 6. Reserve accounting closes: reserve + customer == usable, every row.
    for r in disposal_budget():
        if abs(r['reserve_kg'] + r['customer_kg'] - USABLE_PROP_KG) > 1e-9:
            fails.append('disposal reserve accounting does not close')

    # 7. A larger reserve leaves less customer dv.
    cdv = [r['customer_dv_ms'] for r in disposal_budget()]
    if cdv != sorted(cdv, reverse=True):
        fails.append('customer dv does not fall as reserve rises')

    # 8. The plane-change re-derivation agrees with MISSION_ARCHITECTURE.md section 5.
    published = {350.0: (7697.0, 134.3, 5.71), 500.0: (7612.6, 132.9, 5.53),
                 700.0: (7504.3, 131.0, 5.30)}
    for r in plane_change_check():
        v, p1, h10 = published[r['alt_km']]
        if (abs(r['v_circ_ms'] - v) > 0.1 or abs(r['plane_1deg_ms'] - p1) > 0.1
                or abs(r['raise_10km_ms'] - h10) > 0.01):
            fails.append(f"plane-change table disagrees at {r['alt_km']:.0f} km")

    # 9. The inverted minimum burn reproduces the manoeuvre it was solved for.
    for r in granularity():
        if abs(dv_from_burn(r['min_burn_for_fine_s'], r['stage_mass_kg']) - 5.0) > 1e-9:
            fails.append('inverted minimum burn does not reproduce 5 m/s')

    # 10. Case A spends nothing. If it ever does, the case has stopped being case A.
    if mission_cases()[0]['propellant_kg'] != 0.0:
        fails.append('case A is not propellant-free')

    return fails



# --------------------------------------------------------------------------------
# Document check
# --------------------------------------------------------------------------------
DOC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   'docs', 'HOST_REFERENCE_CASES.md')


def doc_figures(res):
    """Every computed figure the document publishes, formatted as the document writes it.

    docs/HOST_REFERENCE_CASES.md is authored prose with tables in it, not a generated
    file, so its numbers are typed. A number typed once is a number that drifts the first
    time a constant moves, which is P84, P96, P97, P101 and P102 in this repository's own
    register. This is the cheap guard: every figure below must appear in the document.
    """
    f = []
    f.append(('mass flow', f"{res['mass_flow_kg_s']:.2f}"))
    for r in res['burn_grid']:
        if r['isp_s'] == ISP_S:
            f.append(('burn %g kg %g m/s' % (r['stage_mass_kg'], r['dv_ms']),
                      f"{r['burn_s']:.2f}"))
            mp = r['propellant_kg']
            f.append(('propellant %g kg %g m/s' % (r['stage_mass_kg'], r['dv_ms']),
                      f"{mp:.2f}" if mp < 10 else f"{mp:.1f}"))
    for r in res['minimum_impulse']:
        f.append(('dv from %gs at %g kg' % (r['burn_s'], r['stage_mass_kg']),
                  f"{r['dv_ms']:.1f}"))
    for r in res['granularity']:
        f.append(('dv floor at %g kg' % r['stage_mass_kg'], f"{r['dv_floor_ms']:.1f}"))
        f.append(('altitude step at %g kg' % r['stage_mass_kg'],
                  f"{r['altitude_step_km']:.0f}"))
        f.append(('overshoot at %g kg' % r['stage_mass_kg'], f"{r['overshoot_factor']:.1f}"))
        f.append(('burn for 5 m/s at %g kg' % r['stage_mass_kg'],
                  f"{r['min_burn_for_fine_s']:.2f}"))
    for r in res['disposal_budget']:
        f.append(('reserve %g%%' % (r['reserve_fraction'] * 100), f"{r['reserve_kg']:.1f}"))
        f.append(('customer %g%%' % (r['reserve_fraction'] * 100), f"{r['customer_kg']:.1f}"))
        f.append(('customer dv %g%%' % (r['reserve_fraction'] * 100),
                  f"{r['customer_dv_ms']:.0f}"))
        f.append(('reserve dv %g%%' % (r['reserve_fraction'] * 100),
                  f"{r['reserve_dv_ms']:.0f}"))
    for c in res['mission_cases']:
        tag = c['case'].split(',')[0]
        f.append((f'case {tag} propellant', f"{c['propellant_kg']:.1f}"))
        f.append((f'case {tag} margin', f"{c['margin_kg']:.1f}"))
        if c['restarts']:
            f.append((f'case {tag} orbit pacing', f"{c['one_orbit_pacing_h']:.1f}"))
    for r in res['batch_trade']:
        f.append(('batch %d propellant' % r['batches'], f"{r['propellant_kg']:.1f}"))
        f.append(('batch %d dv' % r['batches'], f"{r['total_dv_ms']:.0f}"))
    for r in res['plane_change']:
        f.append(('v_circ %g km' % r['alt_km'], f"{r['v_circ_ms']:.1f}"))
        f.append(('1 deg %g km' % r['alt_km'], f"{r['plane_1deg_ms']:.1f}"))
        f.append(('10 km raise %g km' % r['alt_km'], f"{r['raise_10km_ms']:.2f}"))
    f.append(('orbit period', f"{res['orbit_period_min_500km']:.1f}"))
    return f


def check_doc(res):
    """Return the figures the document does not carry."""
    if not os.path.exists(DOC):
        return ['docs/HOST_REFERENCE_CASES.md is missing']
    text = open(DOC, encoding='utf-8').read()
    return [f'{name}: {val} is not in the document'
            for name, val in doc_figures(res) if val not in text]


def build():
    return {
        'constants': {'g0': G0, 'mu': MU, 're': RE},
        'reference_point': {
            'thrust_N': THRUST_N, 'isp_s': ISP_S, 'stage_mass_kg': STAGE_MASS_KG,
            'min_burn_s': MIN_BURN_S, 'coast_min': COAST_MIN,
            'restarts_planned': RESTARTS_PLANNED,
            'restart_contingency': RESTART_CONTINGENCY,
            'campaign_h': CAMPAIGN_H, 'disposal_fraction': DISPOSAL_FRACTION,
            'usable_prop_kg': USABLE_PROP_KG,
        },
        'provenance': PROVENANCE,
        'mass_flow_kg_s': mass_flow(),
        'burn_grid': burn_grid(),
        'minimum_impulse': minimum_impulse(),
        'granularity': granularity(),
        'disposal_budget': disposal_budget(),
        'mission_cases': mission_cases(),
        'batch_trade': batch_trade(),
        'plane_change': plane_change_check(),
        'orbit_period_min_500km': orbit_period_min(),
        'self_test_failures': self_test(),
    }


if __name__ == '__main__':
    res = build()
    fails = res['self_test_failures']

    if '--check-doc' in sys.argv:
        missing = check_doc(res)
        if missing:
            print(f'host reference: {len(missing)} figure(s) not in the document\n')
            for m in missing:
                print(f'  {m}')
            sys.exit(1)
        print(f'host reference: {len(doc_figures(res))} figures agree with '
              f'docs/HOST_REFERENCE_CASES.md')
        sys.exit(0)
    print(f"host reference, {THRUST_N/1e3:.0f} kN class, Isp {ISP_S:.0f} s ASSUMED, "
          f"stage {STAGE_MASS_KG:.0f} kg ASSUMED")
    print(f"mass flow {res['mass_flow_kg_s']:.2f} kg/s\n")

    print(f"{'stage kg':>9s} {'min burn':>9s} {'dv floor':>9s} {'altitude step':>15s}"
          f" {'x 5 m/s':>9s} {'burn for 5 m/s':>15s}")
    for r in res['granularity']:
        print(f"{r['stage_mass_kg']:9.0f} {r['min_burn_s']:8.1f}s "
              f"{r['dv_floor_ms']:8.1f} m/s {r['altitude_step_km']:12.0f} km "
              f"{r['overshoot_factor']:9.1f} {r['min_burn_for_fine_s']:14.2f}s")

    print(f"\nburn duration at Isp {ISP_S:.0f} s ASSUMED:")
    print(f"{'stage kg':>9s}" + ''.join(f"{dv:>10.0f}" for dv in DELTA_VS) + '  m/s')
    for m0 in STAGE_MASSES:
        line = f"{m0:9.0f}"
        for dv in DELTA_VS:
            line += f"{burn_time_for(dv, m0):9.2f}s"
        print(line)

    print("\nmission cases:")
    for c in res['mission_cases']:
        print(f"  {c['case']:48s} {c['restarts']} restart(s)  "
              f"{c['propellant_kg']:6.1f} kg  margin {c['margin_kg']:6.1f} kg")

    print("\nbatch trade, 12 satellites, 20 m/s per reposition:")
    for r in res['batch_trade']:
        print(f"  {r['batches']:2d} batches  {r['restarts']:2d} restarts  "
              f"{r['total_dv_ms']:5.0f} m/s  {r['propellant_kg']:6.1f} kg  "
              f"{r['coast_time_h']:4.1f} h coast")

    print(f"\nself-test: {'PASS' if not fails else 'FAIL'}")
    for f in fails:
        print(f"  {f}")

    os.makedirs(RESULTS, exist_ok=True)
    json.dump(res, open(os.path.join(RESULTS, 'host_reference.json'), 'w'), indent=2)
    print('\n-> results/host_reference.json')
