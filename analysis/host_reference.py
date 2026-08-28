"""
VOLLEY | Host-reference propulsion arithmetic for docs/HOST_REFERENCE_CASES.md.

WHAT THIS IS
------------
The host stage does the coarse orbital repositioning and VOLLEY does the fine
per-satellite release state (docs/MISSION_ARCHITECTURE.md section 2). Every number
below is on the host side of that line. Nothing here models the deployer.

The question this answers is not "can engine X fly VOLLEY". It is: given a stage
carrying a restartable main engine of a stated thrust class, how long are the burns
a distributed-delivery campaign needs, and does one engine cover the whole manoeuvre
range or only the top of it?

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
Two-body, impulsive-equivalent for the orbital results; constant thrust and constant
Isp for the propulsion results. No gravity loss, no steering loss, no throttle Isp
penalty, no shutdown transient. It is not a trajectory tool and must not be read as
one.

    mdot = F / (Isp * g0)                       mass flow, kg/s
    dv   = Isp * g0 * ln(m0 / mf)               rocket equation
    mp   = m0 * (1 - exp(-dv / (Isp * g0)))     propellant for a manoeuvre
    tb   = mp / mdot                            burn duration
    dv(t)= Isp * g0 * ln(m0 / (m0 - mdot * t))  what a burn of length t buys

FIVE QUANTITIES THAT ARE NOT THE SAME, AND WERE CONFLATED HERE ONCE
------------------------------------------------------------------
Corrected 2026-08-26, first publication of this file. An earlier revision computed
`dv / hohmann_total(10 km) * 10 km` and called the result an "equivalent altitude
step", then read it in prose as what a single burn does. Those are different
questions and the numbers differ by about a factor of two.

    1. one single prograde impulse   raises APOGEE and leaves perigee where it was
    2. total mission dv              the sum of every impulse in the campaign
    3. first Hohmann impulse         raises apogee to the target radius
    4. second Hohmann impulse        circularises there
    5. final circular altitude       what 3 and 4 together deliver

At 500 km a 40.3 m/s single burn raises apogee by 147.6 km. The same 40.3 m/s spent
as a complete two-impulse Hohmann raises the CIRCULAR altitude by 73.4 km. Both are
computed below, side by side, and neither is allowed to stand in for the other.

Provenance: model output, closed-form arithmetic plus one bisection. Nothing here is
measured and no launch provider has supplied any figure in it (E5).
"""
import inspect
import json
import math
import os
import re
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
ASCENT_STARTS = 1               # ILLUSTRATIVE. This reference case defines one ascent start
CAMPAIGN_H = 4.0                # VOLLEY ASSUMPTION. No public coast limit exists
DISPOSAL_FRACTION = 0.20        # VOLLEY ASSUMPTION
USABLE_PROP_KG = 150.0          # VOLLEY ASSUMPTION, post-primary usable propellant
REF_ALT_KM = 500.0              # VOLLEY ASSUMPTION, the altitude every orbital result is at

PROVENANCE = {
    'thrust_N': 'PUBLIC_CLASS_FIGURE, thrust condition not stated by the source',
    'propellant': 'PUBLIC, LOX/kerosene, from the turbopump design publication',
    'isp_s': 'VOLLEY_ASSUMPTION, no public figure exists',
    'stage_mass_kg': 'VOLLEY_ASSUMPTION, no public figure exists',
    'min_burn_s': 'VOLLEY_ASSUMPTION, no public figure exists',
    'coast_min': 'VOLLEY_ASSUMPTION, no public figure exists',
    'restarts_planned': 'VOLLEY_ASSUMPTION, no public engine restart rating exists',
    'ascent_starts': 'ILLUSTRATIVE, defined by this reference case, not a vehicle fact',
    'campaign_h': 'VOLLEY_ASSUMPTION, no public cryogenic coast limit exists',
    'disposal_fraction': 'VOLLEY_ASSUMPTION, a reserve policy and not a disposal guarantee',
    'usable_prop_kg': 'VOLLEY_ASSUMPTION',
    'ref_alt_km': 'VOLLEY_ASSUMPTION, chosen to match MISSION_ARCHITECTURE.md section 5',
}

# Sensitivity envelopes, all VOLLEY-declared.
STAGE_MASSES = [500.0, 1000.0, 2000.0, 3000.0]
DELTA_VS = [5.0, 10.0, 20.0, 40.0, 100.0]
ISPS = [285.0, 300.0, 320.0]
THRUSTS = [15.0e3, 20.0e3, 30.0e3]
BURN_TIMES = [0.5, 1.0, 2.0, 5.0]
MIN_BURNS = [0.5, 1.0, 2.0, 5.0]
THROTTLES = [1.00, 0.75, 0.50, 0.25, 0.10]
FINE_DVS = [2.5, 5.0, 10.0]
RESERVES = [0.10, 0.20, 0.30]

# From analysis/astro.py. Repeated rather than imported because astro.py pulls the whole
# motor model in on import, and this file must not depend on the deployer to run.
MU = 3.986004418e14
RE = 6378.137e3


# --------------------------------------------------------------------------------
# Propulsion
# --------------------------------------------------------------------------------
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


def thrust_for(dv, m0, burn_s, isp_s=ISP_S):
    """Thrust needed to deliver dv from m0 within burn_s, N.

    The inversion a propulsion engineer can answer directly: not "is 2 s too long"
    but "what thrust would the engine have to be able to hold, for this long, to
    command this manoeuvre at all".
    """
    return propellant_for(dv, m0, isp_s) * isp_s * G0 / burn_s


# --------------------------------------------------------------------------------
# Orbits, two-body, impulsive
# --------------------------------------------------------------------------------
def circular_v(alt_km):
    """Circular orbital speed, m/s."""
    return math.sqrt(MU / (RE + alt_km * 1e3))


def orbit_period_min(alt_km=REF_ALT_KM):
    """Circular orbital period, minutes."""
    a = RE + alt_km * 1e3
    return 2.0 * math.pi * math.sqrt(a ** 3 / MU) / 60.0


def single_impulse_apogee(alt_km, dv):
    """One prograde impulse from a circular orbit. Vis-viva, not a linear estimate.

    Perigee stays at the burn radius. Apogee rises. This is what a single main-engine
    burn actually does, and it is NOT a circular altitude change.
    """
    r0 = RE + alt_km * 1e3
    v = circular_v(alt_km) + dv
    eps = v * v / 2.0 - MU / r0                     # specific orbital energy
    if eps >= 0.0:
        raise ValueError('impulse is escape or hyperbolic')
    a = -MU / (2.0 * eps)
    ra = 2.0 * a - r0
    return {
        'dv_ms': dv,
        'sma_km': a / 1e3,
        'apogee_alt_km': (ra - RE) / 1e3,
        'apogee_rise_km': (ra - r0) / 1e3,
        'perigee_alt_km': alt_km,
        'ecc': (ra - r0) / (ra + r0),
    }


def hohmann_impulses(alt_km, d_alt_km):
    """Two-impulse coplanar circular-to-circular raise. Returns both impulses."""
    r1 = RE + alt_km * 1e3
    r2 = r1 + d_alt_km * 1e3
    a = 0.5 * (r1 + r2)
    dv1 = math.sqrt(MU * (2.0 / r1 - 1.0 / a)) - math.sqrt(MU / r1)
    dv2 = math.sqrt(MU / r2) - math.sqrt(MU * (2.0 / r2 - 1.0 / a))
    return abs(dv1), abs(dv2), abs(dv1) + abs(dv2)


def hohmann_raise(alt_km, d_alt_km):
    """Total two-impulse dv for a coplanar altitude change, m/s."""
    return hohmann_impulses(alt_km, d_alt_km)[2]


def hohmann_transfer_min(alt_km, d_alt_km):
    """Half the transfer-ellipse period: burn one to burn two, minutes.

    This is the one part of campaign pacing that is a physical duration rather than
    an operations assumption.
    """
    r1 = RE + alt_km * 1e3
    r2 = r1 + d_alt_km * 1e3
    a = 0.5 * (r1 + r2)
    return math.pi * math.sqrt(a ** 3 / MU) / 60.0


def hohmann_raise_for_dv(alt_km, dv_total, hi_km=5000.0):
    """Invert the Hohmann relation: what circular raise does a total dv budget buy?

    Solved by bisection rather than by scaling the 10 km case linearly. Over a 73 km
    raise the linear estimate is about 0.7 % low, which is small but is an error this
    file has no reason to carry.
    """
    if dv_total <= 0.0:
        return 0.0
    lo, hi = 0.0, hi_km
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if hohmann_raise(alt_km, mid) < dv_total:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def plane_change(alt_km, d_inc_deg):
    """Single-impulse inclination change at circular speed, m/s."""
    return 2.0 * circular_v(alt_km) * math.sin(math.radians(d_inc_deg) / 2.0)


# --------------------------------------------------------------------------------
# Tables
# --------------------------------------------------------------------------------
def burn_grid():
    """Burn duration and propellant for every (stage mass, dv, Isp) combination.

    `dv_ms` here is a TOTAL manoeuvre budget. It is not a single impulse, and the
    burn duration is what one continuous burn of that size would take.
    """
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


def thrust_sweep():
    """The declared 15 to 30 kN sensitivity, actually run.

    The main conclusion is about how coarse the smallest commandable manoeuvre is, and
    thrust is the parameter it should be most sensitive to. Declaring a sensitivity
    range and not sweeping it is how a sensitivity claim becomes decoration.
    """
    rows = []
    for F in THRUSTS:
        floor = dv_from_burn(MIN_BURN_S, STAGE_MASS_KG, F)
        row = {
            'thrust_N': F,
            'mass_flow_kg_s': mass_flow(F),
            'dv_floor_ref_ms': floor,
            'apogee_rise_at_floor_km':
                single_impulse_apogee(REF_ALT_KM, floor)['apogee_rise_km'],
            'hohmann_raise_at_floor_km': hohmann_raise_for_dv(REF_ALT_KM, floor),
            'burns': [],
        }
        for dv in [2.5, 5.0, 10.0, 20.0]:
            row['burns'].append({
                'dv_ms': dv,
                'burn_s': burn_time_for(dv, STAGE_MASS_KG, F),
            })
        rows.append(row)
    return rows


def minimum_impulse():
    """What the shortest credible burns buy, across the stage-mass envelope."""
    rows = []
    for m0 in STAGE_MASSES:
        for t in BURN_TIMES:
            dv = dv_from_burn(t, m0)
            rows.append({
                'stage_mass_kg': m0, 'burn_s': t, 'dv_ms': dv,
                'propellant_kg': mass_flow() * t,
                'apogee_rise_km':
                    single_impulse_apogee(REF_ALT_KM, dv)['apogee_rise_km'],
            })
    return rows


def granularity(fine_dv=5.0):
    """The manoeuvre the assumed minimum burn cannot go below, per stage mass.

    Five separate quantities, kept separate:

        dv_floor_ms                 the smallest single impulse the stage can command
        apogee_rise_at_floor_km     what that single impulse actually does to the orbit
        hohmann_raise_at_floor_km   the circular raise the same dv would buy as a
                                    COMPLETE two-impulse transfer
        burn_for_fine_total_s       one continuous burn delivering the whole fine
                                    manoeuvre budget
        burn_for_fine_first_s       the FIRST Hohmann impulse of that manoeuvre, which
                                    is the burn the engine actually has to command
    """
    rows = []
    target_km = hohmann_raise_for_dv(REF_ALT_KM, fine_dv)
    dv1, dv2, _ = hohmann_impulses(REF_ALT_KM, target_km)
    for m0 in STAGE_MASSES:
        dv_min = dv_from_burn(MIN_BURN_S, m0)
        rows.append({
            'stage_mass_kg': m0,
            'min_burn_s': MIN_BURN_S,
            'dv_floor_ms': dv_min,
            'apogee_rise_at_floor_km':
                single_impulse_apogee(REF_ALT_KM, dv_min)['apogee_rise_km'],
            'hohmann_raise_at_floor_km': hohmann_raise_for_dv(REF_ALT_KM, dv_min),
            'exceeds_fine_manoeuvre': dv_min > fine_dv,
            'overshoot_vs_fine_total': dv_min / fine_dv,
            'overshoot_vs_fine_first_impulse': dv_min / dv1,
            'burn_for_fine_total_s': burn_time_for(fine_dv, m0),
            'burn_for_fine_first_s': burn_time_for(dv1, m0),
            'burn_for_fine_second_s': burn_time_for(dv2, m0),
        })
    return rows


def fine_manoeuvres():
    """The small end of the range, split into the impulses an engine must command.

    Each row is a coplanar circular raise. `dv_total_ms` is the two-impulse budget;
    `dv_first_ms` and `dv_second_ms` are the two burns; the burn durations are what
    the reference stage would need for each one separately. This is the table the
    earlier revision got wrong by quoting the total as if it were one burn.
    """
    rows = []
    for d_alt in [5.0, 10.0, 25.0, 50.0]:
        dv1, dv2, tot = hohmann_impulses(REF_ALT_KM, d_alt)
        rows.append({
            'raise_km': d_alt,
            'dv_total_ms': tot,
            'dv_first_ms': dv1,
            'dv_second_ms': dv2,
            'burn_first_s': burn_time_for(dv1, STAGE_MASS_KG),
            'burn_second_s': burn_time_for(dv2, STAGE_MASS_KG),
            'transfer_min': hohmann_transfer_min(REF_ALT_KM, d_alt),
        })
    return rows


def thrust_and_burn_requirement():
    """What thrust the engine would need to command a small manoeuvre in one burn.

    Answers the question a propulsion engineer can act on: for each fine manoeuvre and
    each candidate minimum stable burn, what is the largest thrust that still lets the
    first Hohmann impulse fit inside that burn? Expressed as a fraction of the 20 kN
    class figure, so it reads directly as a required throttle depth.

    The throttle model holds Isp constant, which is optimistic: a real engine loses
    specific impulse when deeply throttled. That is stated rather than modelled.
    """
    rows = []
    for dv_target in FINE_DVS:
        target_km = hohmann_raise_for_dv(REF_ALT_KM, dv_target)
        dv1, _, _ = hohmann_impulses(REF_ALT_KM, target_km)
        for t in MIN_BURNS:
            F = thrust_for(dv1, STAGE_MASS_KG, t)
            rows.append({
                'fine_dv_total_ms': dv_target,
                'first_impulse_ms': dv1,
                'min_burn_s': t,
                'required_thrust_N': F,
                'fraction_of_class_thrust': F / THRUST_N,
            })
    return rows


def throttle_sensitivity():
    """Hypothetical throttle depths, and the manoeuvre floor each would reach.

    NOT a capability of any engine. Nothing public establishes a throttle envelope for
    the reference case, and this table exists to show what one would be worth.
    """
    rows = []
    for k in THROTTLES:
        F = THRUST_N * k
        dv = dv_from_burn(MIN_BURN_S, STAGE_MASS_KG, F)
        rows.append({
            'throttle_fraction': k,
            'thrust_N': F,
            'dv_floor_ms': dv,
            'apogee_rise_km':
                single_impulse_apogee(REF_ALT_KM, dv)['apogee_rise_km'],
            'hohmann_raise_km': hohmann_raise_for_dv(REF_ALT_KM, dv),
        })
    return rows


def disposal_budget(usable_kg=USABLE_PROP_KG, m0=STAGE_MASS_KG):
    """Reserve ring-fenced first, customer manoeuvres spend the remainder.

    The two dv figures are sequential, not independent. `customer_dv_ms` is what the
    customer allocation buys starting from the full stage mass; `reserve_dv_ms` is what
    the ring-fenced remainder buys AFTER the customer allocation has been spent, which
    is the mass state disposal actually happens at. Reading the reserve dv as a burn
    from initial mass would overstate it.
    """
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
            'mass_at_disposal_kg': m0 - customer,
        })
    return rows


MAIN_ENGINE = 'MAIN_ENGINE'
AUXILIARY = 'AUXILIARY_PROPULSION_REQUIRED'


def assign_impulse(dv, m0, thrust_N=THRUST_N, min_burn_s=MIN_BURN_S):
    """One impulse, and whether the baseline main engine can command it.

    The study declares a minimum stable useful burn and then has to honour it. A burn
    shorter than that floor is not a small burn, it is a burn the assumed engine does
    not have. Counting an ignition for it credits the engine with a manoeuvre it
    cannot perform, which is the defect P116 records.

    No throttle is credited here. `thrust_for` says what thrust WOULD be needed to
    stretch this impulse to the floor, and the throttle branch reads that separately.
    """
    burn = burn_time_for(dv, m0, thrust_N)
    ok = burn >= min_burn_s
    # A floor of zero admits everything, and the thrust that would stretch a burn to
    # zero seconds is unbounded. Report it as absent rather than divide by it.
    need = thrust_for(dv, m0, min_burn_s) if min_burn_s > 0.0 else None
    return {
        'dv_ms': dv,
        'mass_before_kg': m0,
        'burn_s': burn,
        'minimum_burn_s': min_burn_s,
        'executable_by_baseline_main_engine': ok,
        'assigned_to': MAIN_ENGINE if ok else AUXILIARY,
        'thrust_for_min_burn_N': need,
        'throttle_fraction_of_baseline': (need / thrust_N) if need is not None else None,
    }


def propagate_campaign(steps, start_alt_km=REF_ALT_KM, m0=STAGE_MASS_KG,
                       thrust_N=THRUST_N, min_burn_s=MIN_BURN_S):
    """A sequential campaign: every leg starts from the orbit the last one reached.

    The earlier revision solved every leg from REF_ALT_KM and multiplied one leg's
    altitude increment by the leg count. A Hohmann transfer of fixed TOTAL dv buys a
    larger altitude increment from a higher orbit, so repeating an identical dv does
    not repeat an identical raise, and the multiplication understates the campaign.
    Over eleven 20 m/s legs it understates it by 3.94 per cent.

    Mass propagates as well, which matters for executability rather than for the
    orbit: a lighter stage needs MORE dv to hold a burn to the minimum duration, so
    the smallest manoeuvre the engine can command grows as the campaign proceeds.
    """
    alt = start_alt_km
    m = m0
    legs = []
    for i, dv_total in enumerate(steps, 1):
        raise_km = hohmann_raise_for_dv(alt, dv_total)
        dv1, dv2, _ = hohmann_impulses(alt, raise_km)
        first = assign_impulse(dv1, m, thrust_N, min_burn_s)
        m_mid = m - propellant_for(dv1, m)
        second = assign_impulse(dv2, m_mid, thrust_N, min_burn_s)
        mp = propellant_for(dv1 + dv2, m)
        legs.append({
            'leg': i,
            'dv_total_ms': dv_total,
            'start_alt_km': alt,
            'end_alt_km': alt + raise_km,
            'raise_km': raise_km,
            'dv_first_ms': dv1,
            'dv_second_ms': dv2,
            'burn_first_s': first['burn_s'],
            'burn_second_s': second['burn_s'],
            'minimum_burn_s': min_burn_s,
            'first_assigned_to': first['assigned_to'],
            'second_assigned_to': second['assigned_to'],
            'executable_by_baseline_main_engine':
                first['executable_by_baseline_main_engine']
                and second['executable_by_baseline_main_engine'],
            'transfer_min': hohmann_transfer_min(alt, raise_km),
            'propellant_kg': mp,
            'mass_before_kg': m,
            'mass_after_kg': m - mp,
        })
        alt += raise_km
        m -= mp
    return legs


def campaign_executability(legs, thrust_N=THRUST_N, min_burn_s=MIN_BURN_S):
    """Roll the per-impulse verdicts up to the case, without softening them."""
    impulses = []
    for lg in legs:
        impulses.append((lg['dv_first_ms'], lg['burn_first_s'],
                         lg['first_assigned_to'], lg['mass_before_kg']))
        impulses.append((lg['dv_second_ms'], lg['burn_second_s'],
                         lg['second_assigned_to'],
                         lg['mass_before_kg'] - propellant_for(lg['dv_first_ms'],
                                                              lg['mass_before_kg'])))
    if not impulses:
        return {
            'all_main_engine_impulses_executable': True,
            'non_executable_impulse_count': 0,
            'total_manoeuvre_impulses': 0,
            'shortest_required_burn_s': None,
            'minimum_thrust_required_for_shortest_impulse_N': None,
            'throttle_fraction_required': None,
        }
    shortest = min(impulses, key=lambda r: r[1])
    need_N = (thrust_for(shortest[0], shortest[3], min_burn_s)
              if min_burn_s > 0.0 else None)
    bad = sum(1 for r in impulses if r[2] != MAIN_ENGINE)
    return {
        'all_main_engine_impulses_executable': bad == 0,
        'non_executable_impulse_count': bad,
        'total_manoeuvre_impulses': len(impulses),
        'shortest_required_burn_s': shortest[1],
        'minimum_thrust_required_for_shortest_impulse_N': need_N,
        'throttle_fraction_required': (need_N / thrust_N) if need_N is not None else None,
    }


def restart_accounting(legs, needs_disposal_burn, disposal_executable=True):
    """Ignition schema, split by which propulsion system actually performs each impulse.

    Two earlier revisions of this field were wrong in the same direction. The first
    exposed the number of repositioning LEGS while the prose counted the disposal burn
    too. The second counted every leg as one ignition when a circular-to-circular
    transfer is two.

    This revision fixes a third error of the same family, and it runs the other way.
    Impulses were counted as main-engine ignitions without asking whether the assumed
    engine could produce them. An impulse below the declared minimum burn is not a
    short main-engine ignition; it is not a main-engine ignition at all, and charging
    it to the engine's restart budget overstates what the engine is asked to do while
    hiding that it cannot do it. Counts are therefore split, and both halves are kept.
    """
    me = 0
    aux = 0
    aux_dv = 0.0
    for lg in legs:
        for key, dvk in (('first_assigned_to', 'dv_first_ms'),
                         ('second_assigned_to', 'dv_second_ms')):
            if lg[key] == MAIN_ENGINE:
                me += 1
            else:
                aux += 1
                aux_dv += lg[dvk]
    disposal = 1 if (needs_disposal_burn and disposal_executable) else 0
    disposal_aux = 1 if (needs_disposal_burn and not disposal_executable) else 0
    post = me + disposal
    return {
        'reposition_legs': len(legs),
        'impulses_per_leg': 2,
        'main_engine_reposition_ignitions': me,
        'auxiliary_reposition_impulses': aux,
        'auxiliary_reposition_dv_ms': aux_dv,
        'disposal_main_engine_ignitions': disposal,
        'disposal_auxiliary_impulses': disposal_aux,
        'post_primary_main_engine_ignitions_required': post,
        'contingency_main_engine_ignitions_reserved': RESTART_CONTINGENCY,
        'total_manoeuvre_impulses': 2 * len(legs) + (1 if needs_disposal_burn else 0),
        'total_propulsion_events': me + aux + disposal + disposal_aux,
        'ascent_starts_assumed': ASCENT_STARTS,
        'ascent_starts_are_illustrative': True,
        'total_main_engine_starts_nominal': ASCENT_STARTS + post,
        'igniter_cycles_nominal': ASCENT_STARTS + post,
        'full_engine_cycles_nominal': ASCENT_STARTS + post,
        'assumed_restart_budget': RESTARTS_PLANNED,
        'restart_budget_is_a_volley_assumption': True,
        'within_assumed_restart_budget': post <= RESTARTS_PLANNED,
        'shortfall_against_budget': max(0, post - RESTARTS_PLANNED),
    }


def pacing(legs):
    """Three declared pacing scenarios plus the one duration that is physical.

    `transfer_only_h` is now the SUM of each leg's own transfer arc, not one leg's arc
    multiplied by the leg count. The arc lengthens as the campaign climbs, so the
    multiplication understated an eleven-leg campaign by 4.1 per cent.

    Everything else here is a scheduling assumption. Navigation, attitude settling,
    safe separation, plume constraints, collision avoidance and host command rules all
    set the real pace, and none of them is computable from public data. The one-orbit
    case is illustrative and is not a lower bound.
    """
    n = len(legs)
    period = orbit_period_min(REF_ALT_KM)
    transfers = [lg['transfer_min'] for lg in legs]
    return {
        'legs': n,
        'orbit_period_min': period,
        'first_leg_transfer_min': transfers[0] if transfers else 0.0,
        'summed_transfer_min': sum(transfers),
        'transfer_only_h': sum(transfers) / 60.0,
        'coast_floor_h': n * COAST_MIN / 60.0,
        'half_orbit_per_leg_h': n * 0.5 * period / 60.0,
        'one_orbit_per_leg_h': n * period / 60.0,
        'two_orbits_per_leg_h': n * 2.0 * period / 60.0,
    }


def disposal_impulse(usable_kg=USABLE_PROP_KG, m0=STAGE_MASS_KG,
                     fraction=DISPOSAL_FRACTION, thrust_N=THRUST_N):
    """The controlled-disposal burn, at the mass state it actually happens at."""
    reserve = usable_kg * fraction
    customer = usable_kg - reserve
    m_at = m0 - customer
    dv = ISP_S * G0 * math.log(m_at / (m0 - usable_kg))
    return assign_impulse(dv, m_at, thrust_N)


def mission_cases():
    """Three post-primary campaigns, priced on the declared assumptions.

    Case A is the one that matters most to the architecture: it establishes that
    VOLLEY does not need a restartable host to exist at all.

    Cases B and C are NOT presented as executable baseline main-engine campaigns, and
    the earlier revision was wrong to present them as such. Each leg is a two-impulse
    transfer of about half its total dv per impulse, and at the reference point those
    impulses run 0.49 s and 0.94 s against a declared 2 s floor. The minimum-burn
    constraint binds before restart count does. See the branch tables for what can be
    commanded instead.
    """
    usable = USABLE_PROP_KG
    reserve = usable * DISPOSAL_FRACTION
    budget = usable - reserve
    disp = disposal_impulse()

    def campaign(name, steps, batches, needs_disposal):
        legs = propagate_campaign(steps, REF_ALT_KM, STAGE_MASS_KG)
        spent = sum(lg['propellant_kg'] for lg in legs)
        ex = campaign_executability(legs)
        return {
            'case': name,
            'batches': batches,
            'total_dv_ms': sum(steps),
            'propellant_kg': spent,
            'budget_kg': budget,
            'within_budget': spent <= budget,
            'margin_kg': budget - spent,
            'start_alt_km': REF_ALT_KM,
            'final_alt_km': legs[-1]['end_alt_km'] if legs else REF_ALT_KM,
            'net_circular_rise_km': (legs[-1]['end_alt_km'] - REF_ALT_KM) if legs else 0.0,
            'executability': ex,
            'disposal_burn_s': disp['burn_s'] if needs_disposal else None,
            'disposal_executable': disp['executable_by_baseline_main_engine']
                                   if needs_disposal else None,
            'restart_accounting': restart_accounting(
                legs, needs_disposal, disp['executable_by_baseline_main_engine']),
            'pacing': pacing(legs),
            'legs': legs,
        }

    return [
        campaign('A, rapid deployment, no post-primary main-engine burn', [], 1, False),
        campaign('B, moderate distributed delivery', [20.0, 20.0, 20.0], 3, True),
        campaign('C, upper-bound sensitivity', [40.0] * 5, 5, True),
    ]


def min_shell_step(alt_km, m0, thrust_N=THRUST_N, min_burn_s=MIN_BURN_S):
    """Smallest circular shell change whose BOTH impulses reach the minimum burn.

    The second impulse binds. It is slightly the smaller of the two and it fires at a
    lower mass, and burn duration falls with mass at fixed dv, so sizing on the first
    impulse alone would publish a step the engine could start and not finish.

    Solved by bisection on the raise. Monotone: a larger raise costs more dv per
    impulse, which lengthens both burns.
    """
    def burns(rk):
        dv1, dv2, _ = hohmann_impulses(alt_km, rk)
        m1 = m0 - propellant_for(dv1, m0)
        return burn_time_for(dv1, m0, thrust_N), burn_time_for(dv2, m1, thrust_N), dv1, dv2
    lo, hi = 1e-9, 4000.0
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        b1, b2, _, _ = burns(mid)
        if min(b1, b2) < min_burn_s:
            lo = mid
        else:
            hi = mid
    # Return the admissible side, not the midpoint. The midpoint can sit a fraction of
    # a float below the floor, and a step that fails its own criterion is not a step.
    rk = hi
    b1, b2, dv1, dv2 = burns(rk)
    return {
        'start_alt_km': alt_km,
        'mass_kg': m0,
        'raise_km': rk,
        'end_alt_km': alt_km + rk,
        'dv_total_ms': dv1 + dv2,
        'dv_first_ms': dv1,
        'dv_second_ms': dv2,
        'burn_first_s': b1,
        'burn_second_s': b2,
        'transfer_min': hohmann_transfer_min(alt_km, rk),
        'propellant_kg': propellant_for(dv1 + dv2, m0),
    }


def branch_main_engine_only():
    """BRANCH 1. What the baseline engine CAN command, under its own 2 s floor.

    Repeats the minimum admissible shell step until the customer propellant allocation
    is exhausted. The step is re-solved at every leg because both inputs move: the
    stage climbs, and it lightens, and a lighter stage needs more dv to hold a burn to
    the floor. The steps therefore grow, 150 km to 182 km over four legs.
    """
    budget = USABLE_PROP_KG * (1.0 - DISPOSAL_FRACTION)
    alt, m, spent = REF_ALT_KM, STAGE_MASS_KG, 0.0
    legs = []
    while len(legs) < 20:
        step = min_shell_step(alt, m)
        if spent + step['propellant_kg'] > budget:
            break
        spent += step['propellant_kg']
        step['leg'] = len(legs) + 1
        step['cumulative_propellant_kg'] = spent
        step['mass_after_kg'] = m - step['propellant_kg']
        legs.append(step)
        alt = step['end_alt_km']
        m -= step['propellant_kg']
    disp = disposal_impulse()
    me = 2 * len(legs)
    post = me + (1 if disp['executable_by_baseline_main_engine'] else 0)
    return {
        'legs': legs,
        'steps_within_customer_budget': len(legs),
        'customer_budget_kg': budget,
        'propellant_used_kg': spent,
        'propellant_margin_kg': budget - spent,
        'final_alt_km': alt,
        'net_circular_rise_km': alt - REF_ALT_KM,
        'summed_transfer_min': sum(l['transfer_min'] for l in legs),
        'main_engine_reposition_ignitions': me,
        'post_primary_main_engine_ignitions_required': post,
        'assumed_restart_budget': RESTARTS_PLANNED,
        'within_assumed_restart_budget': post <= RESTARTS_PLANNED,
        'legs_within_restart_budget': max(0, (RESTARTS_PLANNED - 1) // 2),
    }


def branch_main_plus_auxiliary():
    """BRANCH 2. Keep the Case B and C shells; assign each impulse to what can do it.

    No auxiliary capability is assumed. The branch states the demand an auxiliary
    system would have to meet, and names the provider datum that would settle whether
    a host has it. [P94](../OPEN_PROBLEMS.md#p94) already records that the host RCS
    authority A13 band 5 leans on is not established.
    """
    disp = disposal_impulse()
    rows = []
    for name, steps in (('B, moderate distributed delivery', [20.0] * 3),
                        ('C, upper-bound sensitivity', [40.0] * 5)):
        legs = propagate_campaign(steps, REF_ALT_KM, STAGE_MASS_KG)
        ra = restart_accounting(legs, True, disp['executable_by_baseline_main_engine'])
        rows.append({
            'case': name,
            'reposition_legs': len(legs),
            'main_engine_reposition_ignitions': ra['main_engine_reposition_ignitions'],
            'auxiliary_reposition_impulses': ra['auxiliary_reposition_impulses'],
            'auxiliary_dv_demand_ms': ra['auxiliary_reposition_dv_ms'],
            'disposal_main_engine_ignitions': ra['disposal_main_engine_ignitions'],
            'post_primary_main_engine_ignitions_required':
                ra['post_primary_main_engine_ignitions_required'],
            'within_assumed_restart_budget': ra['within_assumed_restart_budget'],
            'largest_auxiliary_impulse_ms': max(
                [lg['dv_first_ms'] for lg in legs] + [lg['dv_second_ms'] for lg in legs]),
            'provider_datum_required': 'host auxiliary or RCS dv authority and impulse '
                                       'size, P94. Not assumed here',
        })
    return rows


def branch_throttle():
    """BRANCH 3. Hypothetical throttle depth that would make B and C commandable.

    A sensitivity, and nothing else. No public source states that the reference engine
    throttles at all, and this branch must never be read as saying it does. It answers
    one question: if it did, how deep would it have to go to stretch these impulses to
    the declared 2 s floor.
    """
    rows = []
    for name, steps in (('B, moderate distributed delivery', [20.0] * 3),
                        ('C, upper-bound sensitivity', [40.0] * 5)):
        legs = propagate_campaign(steps, REF_ALT_KM, STAGE_MASS_KG)
        worst = None
        for lg in legs:
            for dv, m in ((lg['dv_first_ms'], lg['mass_before_kg']),
                          (lg['dv_second_ms'],
                           lg['mass_before_kg'] - propellant_for(lg['dv_first_ms'],
                                                                 lg['mass_before_kg']))):
                need = thrust_for(dv, m, MIN_BURN_S)
                if worst is None or need < worst[0]:
                    worst = (need, dv, m)
        need, dv, m = worst
        rows.append({
            'case': name,
            'representative_impulse_ms': dv,
            'mass_at_impulse_kg': m,
            'required_thrust_N': need,
            'fraction_of_baseline_thrust': need / THRUST_N,
            'required_throttle_depth_pct': 100.0 * need / THRUST_N,
            'inside_hypothetical_sweep': (need / THRUST_N) >= min(THROTTLES),
            'sweep_floor_pct': 100.0 * min(THROTTLES),
        })
    return rows


def reposition_scaling(n_sats=12):
    """Fixed-dv-per-reposition scaling, with the orbit propagated. NOT equal-mission.

    Each row holds 20 m/s per reposition fixed, so a row with more repositions also
    buys more total orbital separation. The rows therefore do NOT deliver the same
    mission and cannot be read as one grouping being more efficient than another. A
    fair batching trade would hold the delivered orbital-state distribution constant
    and vary only the grouping, which needs a mission planner this repository does not
    have. That is P113.

    The column that used to say "cumulative raise" was the first leg's raise times the
    leg count. It is now the propagated final circular altitude minus the initial one,
    which is a different and larger number: 415.5 km against 399.1 km over eleven legs.
    A multiplication is not a campaign.
    """
    dv_per_reposition = 20.0
    rows = []
    for n_batches in [n_sats, 4, 3, 2]:
        burns = n_batches - 1          # no reposition is needed before the first batch
        legs = propagate_campaign([dv_per_reposition] * burns, REF_ALT_KM, STAGE_MASS_KG)
        spent = sum(lg['propellant_kg'] for lg in legs)
        final = legs[-1]['end_alt_km'] if legs else REF_ALT_KM
        rows.append({
            'batches': n_batches,
            'satellites_per_batch': n_sats / n_batches,
            'reposition_legs': burns,
            'total_dv_ms': burns * dv_per_reposition,
            'initial_alt_km': REF_ALT_KM,
            'final_alt_km': final,
            'net_circular_rise_km': final - REF_ALT_KM,
            'propellant_kg': spent,
            'summed_transfer_min': sum(lg['transfer_min'] for lg in legs),
            'transfer_only_h': sum(lg['transfer_min'] for lg in legs) / 60.0,
            'coast_floor_h': burns * COAST_MIN / 60.0,
            'one_orbit_per_leg_h': burns * orbit_period_min(REF_ALT_KM) / 60.0,
            'main_engine_impulses': sum(
                (1 if lg['first_assigned_to'] == MAIN_ENGINE else 0)
                + (1 if lg['second_assigned_to'] == MAIN_ENGINE else 0) for lg in legs),
            'auxiliary_impulses': sum(
                (1 if lg['first_assigned_to'] != MAIN_ENGINE else 0)
                + (1 if lg['second_assigned_to'] != MAIN_ENGINE else 0) for lg in legs),
            'equal_mission': False,
        })
    return rows


def plane_change_check():
    """Re-derive MISSION_ARCHITECTURE.md section 5 rather than quoting it.

    `raise_10km_total_ms` is the TOTAL two-impulse cost. That is what section 5
    publishes and what the ratio is taken against, and the two impulses are given
    separately so the total can never be mistaken for one burn.
    """
    rows = []
    for alt in [350.0, 500.0, 700.0]:
        dv1, dv2, tot = hohmann_impulses(alt, 10.0)
        rows.append({
            'alt_km': alt,
            'v_circ_ms': circular_v(alt),
            'plane_1deg_ms': plane_change(alt, 1.0),
            'plane_0p1deg_ms': plane_change(alt, 0.1),
            'raise_10km_total_ms': tot,
            'raise_10km_first_ms': dv1,
            'raise_10km_second_ms': dv2,
            'ratio_1deg_to_10km': plane_change(alt, 1.0) / tot,
        })
    return rows


# --------------------------------------------------------------------------------
# Self-checks. These are arithmetic identities, not acceptance bands.
# --------------------------------------------------------------------------------
def identity_count():
    """How many numbered identities self_test() actually contains.

    Counted from the source rather than written down. The number was hardcoded at 25
    and stayed at 25 while identities were added, which is the same staleness the
    results-freshness gate exists to catch, one level up.
    """
    return len(re.findall(r'^    # \d+\.', inspect.getsource(self_test), re.M))


def self_test():
    """Every check here is a property the closed forms must satisfy identically."""
    fails = []

    def near(a, b, tol):
        return abs(a - b) <= tol

    # 1. Rocket equation and mass flow invert each other.
    tb = burn_time_for(20.0, 1000.0)
    if not near(dv_from_burn(tb, 1000.0), 20.0, 1e-9):
        fails.append('rocket equation and burn-time inverse disagree')

    # 2. Mass flow matches the definition of Isp.
    if not near(mass_flow() * ISP_S * G0, THRUST_N, 1e-6):
        fails.append('mass flow does not reproduce thrust')

    # 3. Burn time rises with stage mass at fixed dv.
    s = [burn_time_for(20.0, m) for m in STAGE_MASSES]
    if s != sorted(s):
        fails.append('burn time is not monotonic in stage mass')

    # 4. Propellant falls as Isp rises at fixed dv and mass.
    s = [propellant_for(20.0, 1000.0, i) for i in ISPS]
    if s != sorted(s, reverse=True):
        fails.append('propellant is not monotonic in Isp')

    # 5. dv from a burn rises with burn length.
    s = [dv_from_burn(t, 1000.0) for t in BURN_TIMES]
    if s != sorted(s):
        fails.append('dv is not monotonic in burn time')

    # 6. Thrust inversion reproduces the manoeuvre it was solved for.
    F = thrust_for(5.0, 1000.0, 2.0)
    if not near(dv_from_burn(2.0, 1000.0, F), 5.0, 1e-9):
        fails.append('thrust inversion does not reproduce its target dv')

    # --- orbital ---

    # 7. Zero impulse raises apogee by nothing.
    if not near(single_impulse_apogee(REF_ALT_KM, 0.0)['apogee_rise_km'], 0.0, 1e-9):
        fails.append('zero impulse does not give zero apogee rise')

    # 8. Single-burn apogee agrees with a direct vis-viva reconstruction: the speed at
    #    the computed apogee radius must satisfy vis-viva on the same ellipse, and
    #    angular momentum must be conserved between perigee and apogee.
    for dv in [1.0, 10.0, 40.3, 100.0]:
        r = single_impulse_apogee(REF_ALT_KM, dv)
        r0 = RE + REF_ALT_KM * 1e3
        ra = r['apogee_alt_km'] * 1e3 + RE
        a = r['sma_km'] * 1e3
        vp = circular_v(REF_ALT_KM) + dv
        va = math.sqrt(MU * (2.0 / ra - 1.0 / a))
        if not near(r0 * vp, ra * va, 1e-3):
            fails.append(f'angular momentum not conserved at dv={dv}')
        if not near(r['apogee_rise_km'], (ra - r0) / 1e3, 1e-9):
            fails.append(f'apogee rise inconsistent at dv={dv}')

    # 9. Apogee rise is monotonic in dv.
    s = [single_impulse_apogee(REF_ALT_KM, d)['apogee_rise_km']
         for d in [1.0, 5.0, 20.0, 50.0, 100.0]]
    if s != sorted(s):
        fails.append('apogee rise is not monotonic in dv')

    # 10. The two Hohmann impulses reproduce the total.
    for d_alt in [1.0, 10.0, 100.0, 500.0]:
        dv1, dv2, tot = hohmann_impulses(REF_ALT_KM, d_alt)
        if not near(dv1 + dv2, tot, 1e-12):
            fails.append(f'Hohmann impulses do not sum to the total at {d_alt} km')

    # 11. The Hohmann inversion round-trips: solve for a raise, evaluate it forward.
    for d_alt in [5.0, 10.0, 73.0, 300.0]:
        tot = hohmann_raise(REF_ALT_KM, d_alt)
        back = hohmann_raise_for_dv(REF_ALT_KM, tot)
        if not near(back, d_alt, 1e-6):
            fails.append(f'Hohmann inversion does not round-trip at {d_alt} km')

    # 12. A single impulse raises apogee by more than the same dv buys as a complete
    #     two-impulse circular raise. This is the distinction the file exists to keep,
    #     so it is asserted rather than assumed.
    for dv in [5.0, 20.0, 40.3, 81.1]:
        one = single_impulse_apogee(REF_ALT_KM, dv)['apogee_rise_km']
        two = hohmann_raise_for_dv(REF_ALT_KM, dv)
        if not one > two:
            fails.append(f'single-impulse apogee rise is not above the Hohmann raise '
                         f'at dv={dv}')

    # 13. Zero dv buys zero circular raise.
    if not near(hohmann_raise_for_dv(REF_ALT_KM, 0.0), 0.0, 1e-12):
        fails.append('zero dv does not give zero circular raise')

    # 14. The plane-change re-derivation agrees with MISSION_ARCHITECTURE.md section 5,
    #     whose 10 km figure is the TOTAL two-impulse cost.
    published = {350.0: (7697.0, 134.3, 5.71), 500.0: (7612.6, 132.9, 5.53),
                 700.0: (7504.3, 131.0, 5.30)}
    for r in plane_change_check():
        v, p1, h10 = published[r['alt_km']]
        if (not near(r['v_circ_ms'], v, 0.1) or not near(r['plane_1deg_ms'], p1, 0.1)
                or not near(r['raise_10km_total_ms'], h10, 0.01)):
            fails.append(f"plane-change table disagrees at {r['alt_km']:.0f} km")

    # 15. The two 10 km impulses are within 1 % of each other at these altitudes: a
    #     near-circular Hohmann splits almost evenly, so quoting the total as one burn
    #     overstates the required burn by about a factor of two.
    for r in plane_change_check():
        if not near(r['raise_10km_first_ms'], r['raise_10km_second_ms'],
                    0.01 * r['raise_10km_first_ms']):
            fails.append(f"10 km impulses are not near-equal at {r['alt_km']:.0f} km")

    # --- accounting ---

    # 16. Reserve accounting closes on every row.
    for r in disposal_budget():
        if not near(r['reserve_kg'] + r['customer_kg'], USABLE_PROP_KG, 1e-9):
            fails.append('disposal reserve accounting does not close')

    # 17. A larger reserve leaves less customer dv.
    s = [r['customer_dv_ms'] for r in disposal_budget()]
    if s != sorted(s, reverse=True):
        fails.append('customer dv does not fall as reserve rises')

    # 18. Customer and reserve dv are sequential, so they must sum to what the whole
    #     usable load would buy from the initial mass.
    whole = ISP_S * G0 * math.log(STAGE_MASS_KG / (STAGE_MASS_KG - USABLE_PROP_KG))
    for r in disposal_budget():
        if not near(r['customer_dv_ms'] + r['reserve_dv_ms'], whole, 1e-9):
            fails.append('customer and reserve dv do not compose')

    # 19. Restart accounting closes, and it closes on MAIN-ENGINE ignitions only.
    for c in mission_cases():
        a = c['restart_accounting']
        if a['post_primary_main_engine_ignitions_required'] != (
                a['main_engine_reposition_ignitions'] + a['disposal_main_engine_ignitions']):
            fails.append(f"ignition accounting does not close for {c['case']}")
        if (a['main_engine_reposition_ignitions'] + a['auxiliary_reposition_impulses']
                != a['reposition_legs'] * a['impulses_per_leg']):
            fails.append(f"assigned impulses do not match legs for {c['case']}")
        if a['total_main_engine_starts_nominal'] != (
                a['ascent_starts_assumed']
                + a['post_primary_main_engine_ignitions_required']):
            fails.append(f"total start count does not close for {c['case']}")
        if len(c['legs']) != a['reposition_legs']:
            fails.append(f"leg count disagrees with the accounting for {c['case']}")

    # 20. Case A spends nothing. If it ever does, the case has stopped being case A.
    if mission_cases()[0]['propellant_kg'] != 0.0:
        fails.append('case A is not propellant-free')

    # 21. Case A needs no post-primary main-engine ignition at all.
    if mission_cases()[0]['restart_accounting'][
            'post_primary_main_engine_ignitions_required'] != 0:
        fails.append('case A requires a post-primary restart')

    # 22. Every mission leg's two impulses reproduce the leg's total dv budget.
    for c in mission_cases():
        for leg in c['legs']:
            if not near(leg['dv_first_ms'] + leg['dv_second_ms'],
                        leg['dv_total_ms'], 1e-6):
                fails.append(f"leg impulses do not sum to the leg budget in {c['case']}")

    # 23. The scaling illustration is flagged as not delivering an equal mission.
    for r in reposition_scaling():
        if r['equal_mission']:
            fails.append('reposition scaling claims equal missions')

    # 24. Thrust sweep is monotonic: more thrust means a coarser floor at fixed burn.
    s = [r['dv_floor_ref_ms'] for r in thrust_sweep()]
    if s != sorted(s):
        fails.append('dv floor is not monotonic in thrust')

    # 25. Required thrust falls as the allowed burn lengthens.
    for dv in FINE_DVS:
        s = [r['required_thrust_N'] for r in thrust_and_burn_requirement()
             if r['fine_dv_total_ms'] == dv]
        if s != sorted(s, reverse=True):
            fails.append(f'required thrust is not monotonic in burn time at {dv} m/s')

    # 26. (A) An impulse marked main-engine executable must actually reach the floor.
    for c in mission_cases():
        for leg in c['legs']:
            for side, burn in (('first', leg['burn_first_s']),
                               ('second', leg['burn_second_s'])):
                if leg[side + '_assigned_to'] == MAIN_ENGINE and burn < MIN_BURN_S:
                    fails.append(f"{c['case']} leg {leg['leg']} {side} impulse is "
                                 f"assigned to the main engine below the burn floor")

    # 27. (B) An impulse below the floor must be assigned AWAY from the main engine.
    #     The two halves together forbid both directions of the P116 error.
    for c in mission_cases():
        for leg in c['legs']:
            for side, burn in (('first', leg['burn_first_s']),
                               ('second', leg['burn_second_s'])):
                if burn < MIN_BURN_S and leg[side + '_assigned_to'] == MAIN_ENGINE:
                    fails.append(f"{c['case']} leg {leg['leg']} {side} impulse is below "
                                 f"the floor and still charged to the main engine")

    # 28. (C) Sequential propagation: leg n ends where leg n+1 starts.
    for c in mission_cases():
        for a, b in zip(c['legs'], c['legs'][1:]):
            if not near(a['end_alt_km'], b['start_alt_km'], 1e-12):
                fails.append(f"{c['case']} does not propagate between legs")
    for row in reposition_scaling():
        pass

    # 29. (D) Net rise is the propagated final altitude minus the initial one, not a
    #     multiple of the first leg. This is the identity the old table violated.
    for c in mission_cases():
        if c['legs']:
            if not near(c['final_alt_km'] - c['start_alt_km'],
                        c['net_circular_rise_km'], 1e-9):
                fails.append(f"{c['case']} net rise does not close")
            naive = len(c['legs']) * c['legs'][0]['raise_km']
            if c['net_circular_rise_km'] < naive - 1e-9:
                fails.append(f"{c['case']} propagated rise is below the naive multiple, "
                             f"which inverts the known sign of the approximation")
    for r in reposition_scaling():
        if not near(r['final_alt_km'] - r['initial_alt_km'],
                    r['net_circular_rise_km'], 1e-9):
            fails.append('reposition scaling net rise does not close')

    # 30. (E) Pacing: the campaign transfer duration is the SUM of the legs' arcs.
    for c in mission_cases():
        if not near(c['pacing']['transfer_only_h'] * 60.0,
                    sum(l['transfer_min'] for l in c['legs']), 1e-9):
            fails.append(f"{c['case']} transfer time is not the sum of its legs")
        if len(c['legs']) > 1:
            naive = len(c['legs']) * c['legs'][0]['transfer_min']
            if c['pacing']['summed_transfer_min'] < naive - 1e-9:
                fails.append(f"{c['case']} summed transfer is below the naive multiple")

    # 31. (F) Main-engine ignition count equals impulses actually assigned to it, plus
    #     the disposal burn when the main engine performs it.
    for c in mission_cases():
        a = c['restart_accounting']
        assigned = sum((1 if l['first_assigned_to'] == MAIN_ENGINE else 0)
                       + (1 if l['second_assigned_to'] == MAIN_ENGINE else 0)
                       for l in c['legs'])
        if a['main_engine_reposition_ignitions'] != assigned:
            fails.append(f"{c['case']} main-engine count is not the assigned count")
        if a['post_primary_main_engine_ignitions_required'] != (
                assigned + a['disposal_main_engine_ignitions']):
            fails.append(f"{c['case']} post-primary count is not assigned plus disposal")

    # 32. (G) Auxiliary impulse count equals impulses assigned to auxiliary propulsion.
    for c in mission_cases():
        a = c['restart_accounting']
        aux = sum((1 if l['first_assigned_to'] != MAIN_ENGINE else 0)
                  + (1 if l['second_assigned_to'] != MAIN_ENGINE else 0)
                  for l in c['legs'])
        if a['auxiliary_reposition_impulses'] != aux:
            fails.append(f"{c['case']} auxiliary count is not the assigned count")
        if a['total_propulsion_events'] != (a['main_engine_reposition_ignitions'] + aux
                                            + a['disposal_main_engine_ignitions']
                                            + a['disposal_auxiliary_impulses']):
            fails.append(f"{c['case']} propulsion events do not close")

    # 33. (H) Relaxing the burn floor must not make a case LESS executable, and a
    #     floor of zero must make every impulse commandable.
    legs_b = propagate_campaign([20.0] * 3, REF_ALT_KM, STAGE_MASS_KG)
    strict = campaign_executability(legs_b)['non_executable_impulse_count']
    loose = campaign_executability(
        propagate_campaign([20.0] * 3, REF_ALT_KM, STAGE_MASS_KG, min_burn_s=0.0),
        min_burn_s=0.0)['non_executable_impulse_count']
    if loose > strict:
        fails.append('lowering the burn floor made a case less executable')
    if loose != 0:
        fails.append('a zero burn floor still rejects an impulse')

    # 34. (I) More thrust at a fixed floor makes a case LESS executable, because the
    #     same dv is delivered in less time. Less thrust makes it more executable.
    fewer = campaign_executability(
        propagate_campaign([20.0] * 3, REF_ALT_KM, STAGE_MASS_KG, thrust_N=2.0e3),
        thrust_N=2.0e3)['non_executable_impulse_count']
    more = campaign_executability(
        propagate_campaign([20.0] * 3, REF_ALT_KM, STAGE_MASS_KG, thrust_N=40.0e3),
        thrust_N=40.0e3)['non_executable_impulse_count']
    if not (fewer <= strict <= more):
        fails.append('executability is not monotonic in thrust')

    # 35. Branch 1 is admissible by construction: every impulse it publishes reaches
    #     the floor, and the binding one reaches it exactly.
    b1 = branch_main_engine_only()
    for leg in b1['legs']:
        if leg['burn_first_s'] < MIN_BURN_S or leg['burn_second_s'] < MIN_BURN_S:
            fails.append('branch 1 published a step below the burn floor')
        if not near(min(leg['burn_first_s'], leg['burn_second_s']), MIN_BURN_S, 1e-6):
            fails.append('branch 1 step is not the minimum admissible one')
    if b1['propellant_used_kg'] > b1['customer_budget_kg']:
        fails.append('branch 1 overspends the customer allocation')

    return fails


# --------------------------------------------------------------------------------
# Generated document blocks
# --------------------------------------------------------------------------------
# docs/HOST_REFERENCE_CASES.md is authored prose with generated tables inside it. Each
# table sits between a BEGIN and END marker and is written by the functions below.
# `--write-doc` regenerates every block in place; `--check-doc` regenerates them and
# compares the exact text.
#
# The earlier gate only asked whether each formatted number appeared SOMEWHERE in the
# file. That passes when a correct value sits beside the wrong label, and it passes
# when a stale value stays in its row while the correct one appears elsewhere. Block
# comparison catches both, because the label and the value are regenerated together.
DOC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   'docs', 'HOST_REFERENCE_CASES.md')

BEGIN = '<!-- HOST_REFERENCE:%s:BEGIN -->'
END = '<!-- HOST_REFERENCE:%s:END -->'


def _tbl(header, align, rows):
    out = ['| ' + ' | '.join(header) + ' |', '|' + '|'.join(align) + '|']
    out += ['| ' + ' | '.join(r) + ' |' for r in rows]
    return '\n'.join(out)


def blk_mass_flow(res):
    r = res['reference_point']
    return (f"At {r['thrust_N']/1e3:.0f} kN and an assumed {r['isp_s']:.0f} s, mass flow is "
            f"{res['mass_flow_kg_s']:.2f} kg/s.")


def blk_burn_grid(res):
    rows = []
    for m0 in STAGE_MASSES:
        cells = [f'{m0:.0f} kg']
        for dv in DELTA_VS:
            g = next(x for x in res['burn_grid']
                     if x['isp_s'] == ISP_S and x['stage_mass_kg'] == m0
                     and x['dv_ms'] == dv)
            cells.append(f"{g['burn_s']:.2f}")
        rows.append(cells)
    return _tbl(['Stage mass'] + [f'{d:.0f} m/s' for d in DELTA_VS],
                ['---:'] * (len(DELTA_VS) + 1), rows)


def blk_propellant_grid(res):
    rows = []
    for m0 in STAGE_MASSES:
        cells = [f'{m0:.0f} kg']
        for dv in DELTA_VS:
            g = next(x for x in res['burn_grid']
                     if x['isp_s'] == ISP_S and x['stage_mass_kg'] == m0
                     and x['dv_ms'] == dv)
            mp = g['propellant_kg']
            cells.append(f'{mp:.2f}' if mp < 10 else f'{mp:.1f}')
        rows.append(cells)
    return _tbl(['Stage mass'] + [f'{d:.0f} m/s' for d in DELTA_VS],
                ['---:'] * (len(DELTA_VS) + 1), rows)


def blk_isp_sensitivity(res):
    vals = []
    for isp in ISPS:
        g = next(x for x in res['burn_grid'] if x['isp_s'] == isp
                 and x['stage_mass_kg'] == STAGE_MASS_KG and x['dv_ms'] == 20.0)
        vals.append((isp, g['propellant_kg'], g['burn_s']))
    return _tbl(['Specific impulse', 'Propellant for a 20 m/s budget at 1000 kg',
                 'Burn duration if spent as one burn'],
                ['---:', '---:', '---:'],
                [[f'{i:.0f} s', f'{p:.2f} kg', f'{b:.2f} s'] for i, p, b in vals])


def blk_thrust_sweep(res):
    rows = []
    for r in res['thrust_sweep']:
        b = {x['dv_ms']: x['burn_s'] for x in r['burns']}
        rows.append([
            f"{r['thrust_N']/1e3:.0f} kN",
            f"{r['mass_flow_kg_s']:.2f}",
            f"{r['dv_floor_ref_ms']:.1f}",
            f"{r['apogee_rise_at_floor_km']:.0f}",
            f"{r['hohmann_raise_at_floor_km']:.0f}",
            f"{b[2.5]:.3f}", f"{b[5.0]:.3f}", f"{b[10.0]:.3f}", f"{b[20.0]:.3f}",
        ])
    return _tbl(['Thrust', 'Mass flow, kg/s', 'dv floor at 2 s, m/s',
                 'Apogee rise from that one burn, km',
                 'Circular raise if that dv were a full two-burn budget, km',
                 'Burn for 2.5 m/s, s', 'for 5 m/s', 'for 10 m/s', 'for 20 m/s'],
                ['---:'] * 9, rows)


def blk_minimum_burn(res):
    rows = []
    for r in res['granularity']:
        rows.append([
            f"{r['stage_mass_kg']:.0f} kg",
            f"{r['min_burn_s']:.0f} s",
            f"{r['dv_floor_ms']:.1f}",
            f"{r['apogee_rise_at_floor_km']:.1f}",
            f"{r['hohmann_raise_at_floor_km']:.1f}",
            f"{r['overshoot_vs_fine_total']:.1f}x",
            f"{r['overshoot_vs_fine_first_impulse']:.1f}x",
            f"{r['burn_for_fine_first_s']:.3f}",
        ])
    return _tbl(['Stage mass', 'Assumed minimum burn', 'Single-burn dv floor, m/s',
                 'Apogee rise from that burn, km',
                 'Circular raise the same dv would buy as a full two-burn transfer, km',
                 'Overshoot vs a 5 m/s total budget',
                 'Overshoot vs the first impulse of that budget',
                 'Burn the first impulse actually needs, s'],
                ['---:'] * 8, rows)


def blk_short_burns(res):
    rows = []
    for t in BURN_TIMES:
        cells = [f'{t:g} s']
        for m0 in STAGE_MASSES:
            r = next(x for x in res['minimum_impulse']
                     if x['stage_mass_kg'] == m0 and x['burn_s'] == t)
            cells.append(f"{r['dv_ms']:.1f}")
        rows.append(cells)
    return _tbl(['Burn'] + [f'{m:.0f} kg' for m in STAGE_MASSES],
                ['---:'] * (len(STAGE_MASSES) + 1), rows)


def blk_fine(res):
    rows = []
    for r in res['fine_manoeuvres']:
        rows.append([
            f"{r['raise_km']:.0f} km",
            f"{r['dv_total_ms']:.3f}",
            f"{r['dv_first_ms']:.3f}",
            f"{r['dv_second_ms']:.3f}",
            f"{r['burn_first_s']:.3f}",
            f"{r['burn_second_s']:.3f}",
            f"{r['transfer_min']:.1f}",
        ])
    return _tbl(['Circular raise at 500 km', 'Total dv, m/s', 'First impulse, m/s',
                 'Second impulse, m/s', 'First burn, s', 'Second burn, s',
                 'Transfer arc, min'],
                ['---:'] * 7, rows)


def blk_thrust_requirement(res):
    rows = []
    for dv in FINE_DVS:
        sub = [r for r in res['thrust_and_burn_requirement']
               if r['fine_dv_total_ms'] == dv]
        cells = [f'{dv:g} m/s total', f"{sub[0]['first_impulse_ms']:.3f}"]
        for t in MIN_BURNS:
            r = next(x for x in sub if x['min_burn_s'] == t)
            cells.append(f"{r['required_thrust_N']/1e3:.2f} kN "
                         f"({r['fraction_of_class_thrust']*100:.1f} %)")
        rows.append(cells)
    return _tbl(['Manoeuvre', 'First impulse, m/s']
                + [f'if minimum burn is {t:g} s' for t in MIN_BURNS],
                ['---:'] * (len(MIN_BURNS) + 2), rows)


def blk_throttle(res):
    rows = []
    for r in res['throttle_sensitivity']:
        rows.append([
            f"{r['throttle_fraction']*100:.0f} %",
            f"{r['thrust_N']/1e3:.1f} kN",
            f"{r['dv_floor_ms']:.1f}",
            f"{r['apogee_rise_km']:.1f}",
            f"{r['hohmann_raise_km']:.1f}",
        ])
    return _tbl(['Hypothetical throttle setting', 'Thrust', 'dv floor at 2 s, m/s',
                 'Apogee rise from that burn, km',
                 'Circular raise the same dv would buy as a full two-burn transfer, km'],
                ['---:'] * 5, rows)


def blk_mission_cases(res):
    rows = []
    for c in res['mission_cases']:
        a = c['restart_accounting']
        e = c['executability']
        if not e['total_manoeuvre_impulses']:
            verdict = 'not applicable, no post-primary burn'
        elif e['all_main_engine_impulses_executable']:
            verdict = 'yes'
        else:
            verdict = (f"NO, {e['non_executable_impulse_count']} of "
                       f"{e['total_manoeuvre_impulses']} below the burn floor")
        rows.append([
            c['case'],
            f"{a['reposition_legs']}",
            f"{a['main_engine_reposition_ignitions']}",
            f"{a['auxiliary_reposition_impulses']}",
            f"{c['total_dv_ms']:.0f}",
            f"{c['propellant_kg']:.1f}",
            f"{c['net_circular_rise_km']:.1f}",
            verdict,
        ])
    return _tbl(['Case', 'Reposition legs', 'Main-engine reposition ignitions',
                 'Auxiliary reposition impulses', 'Total dv, m/s', 'Propellant, kg',
                 'Net circular rise, km',
                 'Commandable by the baseline main engine?'],
                ['---', '---:', '---:', '---:', '---:', '---:', '---:', '---'], rows)


def blk_executability(res):
    rows = []
    for c in res['mission_cases']:
        for leg in c['legs']:
            for side in ('first', 'second'):
                rows.append([
                    c['case'].split(',')[0],
                    f"{leg['leg']}",
                    side,
                    f"{leg['dv_' + side + '_ms']:.3f}",
                    f"{leg['burn_' + side + '_s']:.3f}",
                    f"{leg['minimum_burn_s']:.1f}",
                    'yes' if leg[side + '_assigned_to'] == MAIN_ENGINE else 'no',
                    leg[side + '_assigned_to'],
                ])
    return _tbl(['Case', 'Leg', 'Impulse', 'dv, m/s', 'Burn, s', 'Floor, s',
                 'Reaches the floor?', 'Assigned to'],
                ['---', '---:', '---', '---:', '---:', '---:', '---', '---'], rows)


def blk_branches(res):
    b1 = res['branch_main_engine_only']
    rows = [[
        'Branch 1, main engine only',
        f"{b1['steps_within_customer_budget']} step(s) of "
        f"{b1['legs'][0]['raise_km']:.1f} to {b1['legs'][-1]['raise_km']:.1f} km",
        f"{b1['legs'][0]['dv_total_ms']:.1f} to {b1['legs'][-1]['dv_total_ms']:.1f}",
        f"{b1['post_primary_main_engine_ignitions_required']}",
        '0',
        f"{b1['propellant_used_kg']:.1f}",
        'yes, by construction',
    ]]
    for r in res['branch_main_plus_auxiliary']:
        rows.append([
            f"Branch 2, {r['case'].split(',')[0]}, main engine plus auxiliary",
            f"{r['reposition_legs']} leg(s) as specified",
            f"{r['auxiliary_dv_demand_ms']:.0f} to auxiliary",
            f"{r['post_primary_main_engine_ignitions_required']}",
            f"{r['auxiliary_reposition_impulses']}",
            '-',
            'main engine yes, auxiliary not established',
        ])
    for r in res['branch_throttle']:
        rows.append([
            f"Branch 3, {r['case'].split(',')[0]}, hypothetical throttle",
            f"{r['required_throttle_depth_pct']:.1f} % of baseline thrust",
            f"{r['representative_impulse_ms']:.2f} deepest impulse",
            '-',
            '-',
            '-',
            'only if the engine throttles, which no source states',
        ])
    return _tbl(['Branch', 'What it commands', 'dv, m/s',
                 'Post-primary main-engine ignitions', 'Auxiliary impulses',
                 'Propellant, kg', 'Executable under the declared floor?'],
                ['---', '---', '---', '---:', '---:', '---:', '---'], rows)


def blk_propagated(res):
    rows = []
    b1 = res['branch_main_engine_only']
    for leg in b1['legs']:
        rows.append([
            f"{leg['leg']}",
            f"{leg['start_alt_km']:.1f}",
            f"{leg['raise_km']:.1f}",
            f"{leg['end_alt_km']:.1f}",
            f"{leg['dv_first_ms']:.2f}",
            f"{leg['dv_second_ms']:.2f}",
            f"{leg['burn_first_s']:.3f}",
            f"{leg['burn_second_s']:.3f}",
            f"{leg['transfer_min']:.1f}",
            f"{leg['propellant_kg']:.2f}",
        ])
    return _tbl(['Leg', 'Start, km', 'Raise, km', 'End, km', 'dv 1, m/s', 'dv 2, m/s',
                 'Burn 1, s', 'Burn 2, s', 'Transfer, min', 'Propellant, kg'],
                ['---:'] * 10, rows)


def blk_restarts(res):
    c = next(x for x in res['mission_cases'] if x['case'].startswith('B'))
    a = c['restart_accounting']
    rows = [
        ['Reposition legs', f"{a['reposition_legs']}", 'no'],
        ['Impulses per leg, circular to circular',
         f"{a['impulses_per_leg']}", 'two-body result, not a provider figure'],
        ['Main-engine reposition ignitions',
         f"{a['main_engine_reposition_ignitions']}",
         'no. Every reposition impulse here is below the assumed burn floor'],
        ['Auxiliary reposition impulses required',
         f"{a['auxiliary_reposition_impulses']}", 'no, and no host RCS authority is '
         'established either, P94'],
        ['Auxiliary dv demand, m/s',
         f"{a['auxiliary_reposition_dv_ms']:.0f}", 'no'],
        ['Disposal ignition, main engine', f"{a['disposal_main_engine_ignitions']}", 'no'],
        ['Post-primary main-engine ignitions required',
         f"{a['post_primary_main_engine_ignitions_required']}", 'no'],
        ['Assumed post-primary ignition budget', f"{a['assumed_restart_budget']}",
         'no. VOLLEY_ASSUMPTION, not a provider figure'],
        ['Contingency main-engine ignitions reserved',
         f"{a['contingency_main_engine_ignitions_reserved']}", 'no'],
        ['Total manoeuvre impulses, all propulsion',
         f"{a['total_manoeuvre_impulses']}", 'no'],
        ['Ascent starts, illustrative for this case', f"{a['ascent_starts_assumed']}",
         'no, and the ascent profile is a vehicle property'],
        ['Total main-engine starts, illustrative',
         f"{a['total_main_engine_starts_nominal']}", 'no'],
        ['Igniter cycles, at least', f"{a['igniter_cycles_nominal']}",
         'three, on the ground, for the subsystem alone'],
        ['Full-engine thermal cycles', f"{a['full_engine_cycles_nominal']}", 'no'],
    ]
    return _tbl(['Count', 'Case B', 'Established by public evidence?'],
                ['---', '---:', '---'], rows)


def blk_pacing(res):
    rows = []
    for c in res['mission_cases']:
        p = c['pacing']
        if not p['legs']:
            continue
        rows.append([
            c['case'].split(',')[0],
            f"{p['legs']}",
            f"{p['first_leg_transfer_min']:.1f}",
            f"{p['summed_transfer_min']:.1f}",
            f"{p['transfer_only_h']:.2f}",
            f"{p['coast_floor_h']:.2f}",
            f"{p['half_orbit_per_leg_h']:.1f}",
            f"{p['one_orbit_per_leg_h']:.1f}",
            f"{p['two_orbits_per_leg_h']:.1f}",
        ])
    return _tbl(['Case', 'Legs', 'First leg arc, min', 'Summed arcs, min',
                 'Transfer arcs only, h', 'Assumed coast floor, h',
                 'Half-orbit per leg, h', 'One orbit per leg, h',
                 'Two orbits per leg, h'],
                ['---'] + ['---:'] * 8, rows)


def blk_scaling(res):
    rows = []
    for r in res['reposition_scaling']:
        rows.append([
            f"{r['batches']}",
            f"{r['satellites_per_batch']:.0f}",
            f"{r['reposition_legs']}",
            f"{r['total_dv_ms']:.0f}",
            f"{r['initial_alt_km']:.0f}",
            f"{r['final_alt_km']:.1f}",
            f"{r['net_circular_rise_km']:.1f}",
            f"{r['propellant_kg']:.1f}",
            f"{r['transfer_only_h']:.2f}",
            f"{r['one_orbit_per_leg_h']:.1f}",
        ])
    return _tbl(['Deployment states', 'Satellites per state', 'Reposition legs',
                 'Total host dv, m/s', 'Initial altitude, km',
                 'Final circular altitude, km', 'Net circular rise, km',
                 'Propellant, kg', 'Total transfer arc, h',
                 'Illustrative one orbit per leg, h'],
                ['---:'] * 10, rows)


def blk_disposal(res):
    rows = []
    for r in res['disposal_budget']:
        rows.append([
            f"{r['reserve_fraction']*100:.0f} %",
            f"{r['reserve_kg']:.1f}",
            f"{r['customer_kg']:.1f}",
            f"{r['customer_dv_ms']:.0f}",
            f"{r['mass_at_disposal_kg']:.0f}",
            f"{r['reserve_dv_ms']:.0f}",
        ])
    return _tbl(['Reserve', 'Reserve mass, kg', 'Customer mass, kg',
                 'Customer dv from full stage mass, m/s', 'Stage mass at disposal, kg',
                 'Reserve dv from that mass, m/s'],
                ['---:'] * 6, rows)


def blk_plane_change(res):
    rows = []
    for r in res['plane_change']:
        rows.append([
            f"{r['alt_km']:.0f} km",
            f"{r['v_circ_ms']:.1f}",
            f"{r['plane_1deg_ms']:.1f}",
            f"{r['plane_0p1deg_ms']:.1f}",
            f"{r['raise_10km_total_ms']:.2f}",
            f"{r['raise_10km_first_ms']:.2f}",
            f"{r['raise_10km_second_ms']:.2f}",
            f"{r['ratio_1deg_to_10km']:.1f}",
        ])
    return _tbl(['Altitude', 'Circular v, m/s', '1 degree of inclination, m/s',
                 '0.1 degree, m/s', '10 km raise, total, m/s', 'first impulse, m/s',
                 'second impulse, m/s', 'Ratio, 1 degree to 10 km'],
                ['---:'] * 8, rows)


BLOCKS = [
    ('MASS_FLOW', blk_mass_flow),
    ('BURN_GRID', blk_burn_grid),
    ('PROPELLANT_GRID', blk_propellant_grid),
    ('ISP_SENSITIVITY', blk_isp_sensitivity),
    ('THRUST_SWEEP', blk_thrust_sweep),
    ('MINIMUM_BURN', blk_minimum_burn),
    ('SHORT_BURNS', blk_short_burns),
    ('FINE_MANOEUVRES', blk_fine),
    ('THRUST_REQUIREMENT', blk_thrust_requirement),
    ('THROTTLE', blk_throttle),
    ('MISSION_CASES', blk_mission_cases),
    ('EXECUTABILITY', blk_executability),
    ('BRANCHES', blk_branches),
    ('PROPAGATED_CAMPAIGN', blk_propagated),
    ('RESTART_ACCOUNTING', blk_restarts),
    ('PACING', blk_pacing),
    ('REPOSITION_SCALING', blk_scaling),
    ('DISPOSAL', blk_disposal),
    ('PLANE_CHANGE', blk_plane_change),
]


def _span(text, tag):
    b, e = BEGIN % tag, END % tag
    i, j = text.find(b), text.find(e)
    if i < 0 or j < 0 or j < i:
        return None
    return i + len(b), j


def _safe(tag, fn, res):
    """Render one block, turning any failure into a readable message.

    A block function looks the reference point up inside a sweep list. Move a
    reference constant off its sweep and the lookup fails, so the failure is caught
    and reported here rather than surfacing as a traceback: a gate that crashes is
    harder to read than one that says which block broke and why.
    """
    try:
        return fn(res), None
    except Exception as exc:                                    # noqa: BLE001
        return None, (f'{tag}: cannot be generated, {type(exc).__name__}: {exc}. '
                      f'A reference constant has probably moved off its sweep list')


def render_doc(res, text):
    """Replace every generated block in `text`. Returns (new_text, problems)."""
    problems = []
    for tag, fn in BLOCKS:
        span = _span(text, tag)
        if span is None:
            problems.append(f'{tag}: block markers are missing from the document')
            continue
        body, err = _safe(tag, fn, res)
        if err:
            problems.append(err)
            continue
        i, j = span
        text = text[:i] + '\n' + body + '\n' + text[j:]
    return text, problems


def check_doc(res):
    """Regenerate every block and compare it against the document, exactly."""
    if not os.path.exists(DOC):
        return ['docs/HOST_REFERENCE_CASES.md is missing'], 0
    text = open(DOC, encoding='utf-8').read()
    problems = []
    for tag, fn in BLOCKS:
        span = _span(text, tag)
        if span is None:
            problems.append(f'{tag}: block markers are missing from the document')
            continue
        body, err = _safe(tag, fn, res)
        if err:
            problems.append(err)
            continue
        i, j = span
        have = text[i:j].strip('\n')
        want = body.strip('\n')
        if have != want:
            hl, wl = have.split('\n'), want.split('\n')
            for n, (a, b) in enumerate(zip(hl, wl)):
                if a != b:
                    problems.append(f'{tag}: line {n + 1} differs\n'
                                    f'      document: {a}\n'
                                    f'      script:   {b}')
                    break
            else:
                problems.append(f'{tag}: block has {len(hl)} lines, script gives '
                                f'{len(wl)}')
    return problems, len(BLOCKS)


def build():
    return {
        'constants': {'g0': G0, 'mu': MU, 're': RE},
        'reference_point': {
            'thrust_N': THRUST_N, 'isp_s': ISP_S, 'stage_mass_kg': STAGE_MASS_KG,
            'min_burn_s': MIN_BURN_S, 'coast_min': COAST_MIN,
            'restarts_planned': RESTARTS_PLANNED,
            'restart_contingency': RESTART_CONTINGENCY,
            'ascent_starts': ASCENT_STARTS,
            'campaign_h': CAMPAIGN_H, 'disposal_fraction': DISPOSAL_FRACTION,
            'usable_prop_kg': USABLE_PROP_KG, 'ref_alt_km': REF_ALT_KM,
        },
        'provenance': PROVENANCE,
        'mass_flow_kg_s': mass_flow(),
        'orbit_period_min_ref': orbit_period_min(),
        'burn_grid': burn_grid(),
        'thrust_sweep': thrust_sweep(),
        'minimum_impulse': minimum_impulse(),
        'granularity': granularity(),
        'fine_manoeuvres': fine_manoeuvres(),
        'thrust_and_burn_requirement': thrust_and_burn_requirement(),
        'throttle_sensitivity': throttle_sensitivity(),
        'disposal_budget': disposal_budget(),
        'mission_cases': mission_cases(),
        'disposal_impulse': disposal_impulse(),
        'branch_main_engine_only': branch_main_engine_only(),
        'branch_main_plus_auxiliary': branch_main_plus_auxiliary(),
        'branch_throttle': branch_throttle(),
        'reposition_scaling': reposition_scaling(),
        'plane_change': plane_change_check(),
        'self_test_failures': self_test(),
    }


def _main():
    res = build()
    fails = res['self_test_failures']

    if '--check-doc' in sys.argv:
        problems, n = check_doc(res)
        if problems:
            print(f'host reference: {len(problems)} generated block(s) disagree with '
                  f'the document\n')
            for p in problems:
                print(f'  {p}')
            return 1
        print(f'host reference: {n} generated blocks reproduce exactly in '
              f'docs/HOST_REFERENCE_CASES.md')
        return 0

    if '--write-doc' in sys.argv:
        text = open(DOC, encoding='utf-8').read()
        new, problems = render_doc(res, text)
        if problems:
            for p in problems:
                print(f'  {p}')
            return 1
        if new != text:
            open(DOC, 'w', encoding='utf-8').write(new)
            print(f'wrote {len(BLOCKS)} blocks into docs/HOST_REFERENCE_CASES.md')
        else:
            print('document already current')
        return 0

    if '--self-test' in sys.argv:
        if fails:
            print(f'self-test: {len(fails)} FAILURE(S)')
            for f in fails:
                print(f'  {f}')
            return 1
        print(f'self-test: {identity_count()} identities hold')
        return 0

    r = res['reference_point']
    print(f"host reference, {r['thrust_N']/1e3:.0f} kN class, "
          f"Isp {r['isp_s']:.0f} s ASSUMED, stage {r['stage_mass_kg']:.0f} kg ASSUMED")
    print(f"mass flow {res['mass_flow_kg_s']:.2f} kg/s, "
          f"reference altitude {r['ref_alt_km']:.0f} km\n")

    print("the minimum-burn floor, and the two orbital readings of it")
    print(f"{'stage kg':>9s} {'dv floor':>10s} {'apogee rise':>12s} "
          f"{'circular raise':>15s} {'burn for 1st impulse of 5 m/s':>31s}")
    for g in res['granularity']:
        print(f"{g['stage_mass_kg']:9.0f} {g['dv_floor_ms']:9.1f}  "
              f"{g['apogee_rise_at_floor_km']:10.1f} km "
              f"{g['hohmann_raise_at_floor_km']:12.1f} km "
              f"{g['burn_for_fine_first_s']:28.3f} s")

    print("\nthrust sweep, declared 15 to 30 kN")
    for t in res['thrust_sweep']:
        print(f"  {t['thrust_N']/1e3:4.0f} kN  mdot {t['mass_flow_kg_s']:5.2f} kg/s  "
              f"floor {t['dv_floor_ref_ms']:6.1f} m/s  "
              f"apogee +{t['apogee_rise_at_floor_km']:6.1f} km  "
              f"circular +{t['hohmann_raise_at_floor_km']:6.1f} km")

    print("\nfine manoeuvres, split into the impulses an engine must command")
    for f in res['fine_manoeuvres']:
        print(f"  {f['raise_km']:4.0f} km  total {f['dv_total_ms']:7.3f} m/s  "
              f"= {f['dv_first_ms']:6.3f} + {f['dv_second_ms']:6.3f}  "
              f"burns {f['burn_first_s']:.3f} s and {f['burn_second_s']:.3f} s  "
              f"transfer {f['transfer_min']:.1f} min")

    print("\nmission cases, with every impulse checked against the burn floor")
    for c in res['mission_cases']:
        a = c['restart_accounting']
        e = c['executability']
        print(f"  {c['case']:52s} {a['reposition_legs']} leg(s), "
              f"main-engine ignitions {a['post_primary_main_engine_ignitions_required']}, "
              f"auxiliary impulses {a['auxiliary_reposition_impulses']}, "
              f"{c['propellant_kg']:6.1f} kg")
        if e['total_manoeuvre_impulses']:
            print(f"    {'commandable' if e['all_main_engine_impulses_executable'] else 'NOT COMMANDABLE'}"
                  f" by the baseline engine: {e['non_executable_impulse_count']} of "
                  f"{e['total_manoeuvre_impulses']} impulses below the "
                  f"{res['reference_point']['min_burn_s']:.0f} s floor, shortest "
                  f"{e['shortest_required_burn_s']:.3f} s")

    b1 = res['branch_main_engine_only']
    print(f"\nbranch 1, main engine only: {b1['steps_within_customer_budget']} step(s) of "
          f"{b1['legs'][0]['raise_km']:.1f} km rising to {b1['legs'][-1]['raise_km']:.1f} km, "
          f"final {b1['final_alt_km']:.1f} km, {b1['propellant_used_kg']:.1f} kg, "
          f"{b1['post_primary_main_engine_ignitions_required']} post-primary ignitions "
          f"against an assumed budget of {b1['assumed_restart_budget']}")
    print("branch 2, main engine plus auxiliary")
    for r in res['branch_main_plus_auxiliary']:
        print(f"  {r['case']:38s} main-engine {r['post_primary_main_engine_ignitions_required']}, "
              f"auxiliary {r['auxiliary_reposition_impulses']} impulses, "
              f"{r['auxiliary_dv_demand_ms']:.0f} m/s auxiliary dv")
    print("branch 3, hypothetical throttle, NOT a claim about any engine")
    for r in res['branch_throttle']:
        print(f"  {r['case']:38s} {r['representative_impulse_ms']:6.2f} m/s needs "
              f"{r['required_thrust_N']/1e3:5.2f} kN, "
              f"{r['required_throttle_depth_pct']:.1f} % of baseline")

    print(f"\nself-test: {'PASS' if not fails else 'FAIL'}")
    for f in fails:
        print(f"  {f}")

    os.makedirs(RESULTS, exist_ok=True)
    json.dump(res, open(os.path.join(RESULTS, 'host_reference.json'), 'w'), indent=2)
    print('\n-> results/host_reference.json')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(_main())
