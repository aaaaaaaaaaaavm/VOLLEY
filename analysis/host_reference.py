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


def restart_accounting(reposition_legs, needs_disposal_burn, impulses_per_leg=2):
    """Explicit restart schema. The generic count this replaced was ambiguous twice.

    An earlier revision exposed a single field `restarts` equal to the number of
    repositioning LEGS, while the prose counted the disposal burn as well. The two
    disagreed by one, and the ambiguity reached a published summary.

    Correcting the orbital model then exposed a second and larger error in the same
    field. A shell change from one circular orbit to another is a two-impulse Hohmann
    transfer, so one reposition leg is TWO ignitions, not one. Counting legs as
    ignitions understated what the engine would have to be qualified for by a factor of
    about two.

    Definitions:
        reposition_legs                 orbit changes the campaign performs
        impulses_per_leg                2 for a circular-to-circular Hohmann transfer
        reposition_ignitions            legs times impulses per leg
        disposal_ignitions              the controlled-disposal burn, 0 or 1, single
        post_primary_ignitions_required the load-bearing quantity: what the engine must
                                        be qualified for after primary separation
        contingency_ignitions_reserved  held back, not planned to be used
        ascent_starts_assumed           ILLUSTRATIVE. This reference case defines one
        total_engine_starts_nominal     ascent plus post-primary. Illustrative, because
                                        the ascent profile is a vehicle property
        igniter_cycles_nominal          at least one per start, more if a start retries
        full_engine_cycles_nominal      one thermal cycle per start
    """
    rep = reposition_legs * impulses_per_leg
    disposal = 1 if needs_disposal_burn else 0
    post = rep + disposal
    return {
        'reposition_legs': reposition_legs,
        'impulses_per_leg': impulses_per_leg,
        'reposition_ignitions': rep,
        'disposal_ignitions': disposal,
        'post_primary_ignitions_required': post,
        'contingency_ignitions_reserved': RESTART_CONTINGENCY,
        'ascent_starts_assumed': ASCENT_STARTS,
        'ascent_starts_are_illustrative': True,
        'total_engine_starts_nominal': ASCENT_STARTS + post,
        'igniter_cycles_nominal': ASCENT_STARTS + post,
        'full_engine_cycles_nominal': ASCENT_STARTS + post,
        'assumed_restart_budget': RESTARTS_PLANNED,
        'within_assumed_restart_budget': post <= RESTARTS_PLANNED,
        'shortfall_against_budget': max(0, post - RESTARTS_PLANNED),
    }


def pacing(n_legs, leg_raise_km):
    """Three declared pacing scenarios plus the one duration that is physical.

    `transfer_min` is the Hohmann half-period, burn one to burn two. That part is a
    two-body result. Everything else in this function is a scheduling assumption:
    navigation, attitude settling, safe separation, plume constraints, collision
    avoidance and host command rules all set the real pace, and none of them is
    computable from public data. The one-orbit case is illustrative and is not a
    lower bound.
    """
    period = orbit_period_min(REF_ALT_KM)
    transfer = hohmann_transfer_min(REF_ALT_KM, leg_raise_km) if leg_raise_km else 0.0
    return {
        'legs': n_legs,
        'orbit_period_min': period,
        'hohmann_transfer_min': transfer,
        'transfer_only_h': n_legs * transfer / 60.0,
        'coast_floor_h': n_legs * COAST_MIN / 60.0,
        'half_orbit_per_leg_h': n_legs * 0.5 * period / 60.0,
        'one_orbit_per_leg_h': n_legs * period / 60.0,
        'two_orbits_per_leg_h': n_legs * 2.0 * period / 60.0,
    }


def mission_cases():
    """Three post-primary campaigns, priced on the declared assumptions.

    Case A is the one that matters most to the architecture: it establishes that
    VOLLEY does not need a restartable host to exist at all.

    Each leg's dv is a TOTAL two-impulse budget for one shell change, so each leg is
    TWO ignitions of the sizes the leg records, not one. `restart_accounting` counts
    ignitions rather than legs for exactly that reason, and the two numbers differ by
    about a factor of two.
    """
    usable = USABLE_PROP_KG
    reserve = usable * DISPOSAL_FRACTION
    budget = usable - reserve

    def campaign(name, steps, batches, needs_disposal):
        m = STAGE_MASS_KG
        spent = 0.0
        legs = []
        for dv in steps:
            mp = propellant_for(dv, m, ISP_S)
            raise_km = hohmann_raise_for_dv(REF_ALT_KM, dv)
            dv1, dv2, _ = hohmann_impulses(REF_ALT_KM, raise_km)
            legs.append({
                'dv_total_ms': dv, 'propellant_kg': mp,
                'burn_if_single_s': mp / mass_flow(),
                'circular_raise_km': raise_km,
                'dv_first_ms': dv1, 'dv_second_ms': dv2,
                'burn_first_s': burn_time_for(dv1, m),
                'burn_second_s': burn_time_for(dv2, m),
                'mass_before_kg': m,
            })
            m -= mp
            spent += mp
        leg_raise = legs[0]['circular_raise_km'] if legs else 0.0
        return {
            'case': name,
            'batches': batches,
            'total_dv_ms': sum(steps),
            'propellant_kg': spent,
            'budget_kg': budget,
            'within_budget': spent <= budget,
            'margin_kg': budget - spent,
            'restart_accounting': restart_accounting(len(steps), needs_disposal),
            'pacing': pacing(len(steps), leg_raise),
            'legs': legs,
        }

    return [
        campaign('A, rapid deployment, no post-primary main-engine burn', [], 1, False),
        campaign('B, moderate distributed delivery', [20.0, 20.0, 20.0], 3, True),
        campaign('C, upper-bound sensitivity', [40.0] * 5, 5, True),
    ]


def reposition_scaling(n_sats=12):
    """Fixed-dv-per-reposition scaling. NOT an equal-mission batching comparison.

    Each row holds 20 m/s per reposition fixed, so a row with more repositions also
    buys more total orbital separation. The rows therefore do NOT deliver the same
    mission and cannot be read as one grouping being more efficient than another.

    What the table does show is how restart count, propellant and campaign duration
    scale with the number of distinct deployment states. A fair batching trade would
    hold the delivered orbital-state distribution constant and vary only the grouping,
    which needs a mission planner this repository does not have. That is P113.
    """
    dv_per_reposition = 20.0
    rows = []
    for n_batches in [n_sats, 4, 3, 2]:
        m = STAGE_MASS_KG
        spent = 0.0
        burns = n_batches - 1          # no reposition is needed before the first batch
        for _ in range(burns):
            mp = propellant_for(dv_per_reposition, m, ISP_S)
            m -= mp
            spent += mp
        raise_km = hohmann_raise_for_dv(REF_ALT_KM, dv_per_reposition)
        rows.append({
            'batches': n_batches,
            'satellites_per_batch': n_sats / n_batches,
            'reposition_legs': burns,
            'total_dv_ms': burns * dv_per_reposition,
            'propellant_kg': spent,
            'circular_raise_per_leg_km': raise_km,
            'cumulative_raise_km': burns * raise_km,
            'coast_floor_h': burns * COAST_MIN / 60.0,
            'one_orbit_per_leg_h': burns * orbit_period_min(REF_ALT_KM) / 60.0,
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

    # 19. Restart accounting: post-primary = repositions + disposal, every case.
    for c in mission_cases():
        a = c['restart_accounting']
        if a['post_primary_ignitions_required'] != (a['reposition_ignitions']
                                                    + a['disposal_ignitions']):
            fails.append(f"ignition accounting does not close for {c['case']}")
        if a['reposition_ignitions'] != (a['reposition_legs'] * a['impulses_per_leg']):
            fails.append(f"reposition ignitions do not match legs for {c['case']}")
        if a['total_engine_starts_nominal'] != (a['ascent_starts_assumed']
                                                + a['post_primary_ignitions_required']):
            fails.append(f"total start count does not close for {c['case']}")
        if len(c['legs']) != a['reposition_legs']:
            fails.append(f"leg count disagrees with the accounting for {c['case']}")

    # 20. Case A spends nothing. If it ever does, the case has stopped being case A.
    if mission_cases()[0]['propellant_kg'] != 0.0:
        fails.append('case A is not propellant-free')

    # 21. Case A needs no post-primary main-engine ignition at all.
    if mission_cases()[0]['restart_accounting']['post_primary_ignitions_required'] != 0:
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
        rows.append([
            c['case'],
            f"{a['reposition_legs']}",
            f"{a['reposition_ignitions']}",
            f"{a['post_primary_ignitions_required']}",
            f"{c['total_dv_ms']:.0f}",
            f"{c['propellant_kg']:.1f}",
            f"{c['margin_kg']:.1f}",
            'yes' if a['within_assumed_restart_budget']
            else f"NO, over by {a['shortfall_against_budget']}",
        ])
    return _tbl(['Case', 'Reposition legs', 'Reposition ignitions',
                 'Post-primary ignitions required', 'Total dv, m/s', 'Propellant, kg',
                 'Margin on the customer budget, kg',
                 'Inside the assumed 4-ignition budget'],
                ['---', '---:', '---:', '---:', '---:', '---:', '---:', '---'], rows)


def blk_restarts(res):
    c = next(x for x in res['mission_cases'] if x['case'].startswith('B'))
    a = c['restart_accounting']
    rows = [
        ['Reposition legs', f"{a['reposition_legs']}", 'no'],
        ['Ignitions per leg, circular to circular',
         f"{a['impulses_per_leg']}", 'two-body result, not a provider figure'],
        ['Reposition ignitions', f"{a['reposition_ignitions']}", 'no'],
        ['Disposal ignition', f"{a['disposal_ignitions']}", 'no'],
        ['Post-primary ignitions required',
         f"{a['post_primary_ignitions_required']}", 'no'],
        ['Assumed post-primary ignition budget', f"{a['assumed_restart_budget']}",
         'no, and this case needs more than it'],
        ['Contingency ignitions reserved',
         f"{a['contingency_ignitions_reserved']}", 'no'],
        ['Ascent starts, illustrative for this case', f"{a['ascent_starts_assumed']}",
         'no, and the ascent profile is a vehicle property'],
        ['Total engine starts, illustrative', f"{a['total_engine_starts_nominal']}", 'no'],
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
            f"{p['hohmann_transfer_min']:.1f}",
            f"{p['transfer_only_h']:.2f}",
            f"{p['coast_floor_h']:.2f}",
            f"{p['half_orbit_per_leg_h']:.1f}",
            f"{p['one_orbit_per_leg_h']:.1f}",
            f"{p['two_orbits_per_leg_h']:.1f}",
        ])
    return _tbl(['Case', 'Legs', 'Transfer arc per leg, min', 'Transfer arcs only, h',
                 'Assumed coast floor, h', 'Half-orbit per leg, h',
                 'One orbit per leg, h', 'Two orbits per leg, h'],
                ['---'] + ['---:'] * 7, rows)


def blk_scaling(res):
    rows = []
    for r in res['reposition_scaling']:
        rows.append([
            f"{r['batches']}",
            f"{r['satellites_per_batch']:.0f}",
            f"{r['reposition_legs']}",
            f"{r['total_dv_ms']:.0f}",
            f"{r['cumulative_raise_km']:.0f}",
            f"{r['propellant_kg']:.1f}",
            f"{r['one_orbit_per_leg_h']:.1f}",
        ])
    return _tbl(['Deployment states', 'Satellites per state', 'Reposition legs',
                 'Total dv, m/s', 'Cumulative circular raise, km', 'Propellant, kg',
                 'One orbit per leg, h'],
                ['---:'] * 7, rows)


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
        print('self-test: 25 identities hold')
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

    print("\nmission cases")
    for c in res['mission_cases']:
        a = c['restart_accounting']
        print(f"  {c['case']:52s} {a['reposition_legs']} leg(s), "
              f"{a['post_primary_ignitions_required']} post-primary ignition(s), "
              f"{c['propellant_kg']:6.1f} kg, budget "
              f"{'ok' if a['within_assumed_restart_budget'] else 'EXCEEDED'}")

    print(f"\nself-test: {'PASS' if not fails else 'FAIL'}")
    for f in fails:
        print(f"  {f}")

    os.makedirs(RESULTS, exist_ok=True)
    json.dump(res, open(os.path.join(RESULTS, 'host_reference.json'), 'w'), indent=2)
    print('\n-> results/host_reference.json')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(_main())
