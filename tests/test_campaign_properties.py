"""Properties of a propagated campaign, checked over generated inputs.

P116 was a rule that held nowhere and was checked nowhere: impulses were counted as
main-engine ignitions without asking whether the assumed engine could produce them.
The first two rules below forbid that in both directions, for any campaign rather than
for Case B and Case C.
"""
from hypothesis import given, settings, strategies as st

import host_reference as H

ALT = st.floats(min_value=300.0, max_value=1200.0, allow_nan=False, allow_infinity=False)
MASS = st.floats(min_value=400.0, max_value=3000.0, allow_nan=False, allow_infinity=False)
LEG_DV = st.floats(min_value=1.0, max_value=80.0, allow_nan=False, allow_infinity=False)
N_LEGS = st.integers(min_value=1, max_value=6)
SLOW = settings(deadline=None, max_examples=100)


def _legs(n, dv, alt, m, **kw):
    return H.propagate_campaign([dv] * n, alt, m, **kw)


# --------------------------------------------------------------------------------
# P116: an impulse the engine cannot produce is not an engine ignition
# --------------------------------------------------------------------------------
@SLOW
@given(N_LEGS, LEG_DV, ALT, MASS)
def test_every_main_engine_impulse_reaches_the_burn_floor(n, dv, alt, m):
    for leg in _legs(n, dv, alt, m):
        for side in ("first", "second"):
            if leg[f"{side}_assigned_to"] == H.MAIN_ENGINE:
                assert leg[f"burn_{side}_s"] >= leg["minimum_burn_s"]


@SLOW
@given(N_LEGS, LEG_DV, ALT, MASS)
def test_every_impulse_below_the_floor_is_assigned_away_from_the_engine(n, dv, alt, m):
    """The other direction. Together these two make P116 unrepresentable."""
    for leg in _legs(n, dv, alt, m):
        for side in ("first", "second"):
            if leg[f"burn_{side}_s"] < leg["minimum_burn_s"]:
                assert leg[f"{side}_assigned_to"] == H.AUXILIARY


# --------------------------------------------------------------------------------
# Sequential propagation: a campaign is not a multiplication
# --------------------------------------------------------------------------------
@SLOW
@given(N_LEGS, LEG_DV, ALT, MASS)
def test_each_leg_starts_where_the_previous_one_ended(n, dv, alt, m):
    legs = _legs(n, dv, alt, m)
    for a, b in zip(legs, legs[1:]):
        assert a["end_alt_km"] == b["start_alt_km"]


@SLOW
@given(N_LEGS, LEG_DV, ALT, MASS)
def test_a_propagated_campaign_reaches_at_least_the_naive_multiple(n, dv, alt, m):
    """The same total dv buys more altitude from a higher orbit, so repeating a leg
    reaches further than the first leg's raise times the leg count. The old scaling
    table published the multiplication and was 3.9 per cent low over eleven legs.
    The inequality is the direction of the approximation and must never invert."""
    legs = _legs(n, dv, alt, m)
    net = legs[-1]["end_alt_km"] - legs[0]["start_alt_km"]
    assert net >= n * legs[0]["raise_km"] - 1e-9


@SLOW
@given(N_LEGS, LEG_DV, ALT, MASS)
def test_campaign_duration_is_the_sum_of_the_legs(n, dv, alt, m):
    legs = _legs(n, dv, alt, m)
    p = H.pacing(legs)
    assert abs(p["summed_transfer_min"] - sum(l["transfer_min"] for l in legs)) < 1e-9
    if n > 1:
        assert p["summed_transfer_min"] >= n * legs[0]["transfer_min"] - 1e-9


@SLOW
@given(N_LEGS, LEG_DV, ALT, MASS)
def test_mass_falls_monotonically_and_never_goes_negative(n, dv, alt, m):
    legs = _legs(n, dv, alt, m)
    for leg in legs:
        assert leg["mass_after_kg"] < leg["mass_before_kg"]
        assert leg["mass_after_kg"] > 0.0
    for a, b in zip(legs, legs[1:]):
        assert a["mass_after_kg"] == b["mass_before_kg"]


# --------------------------------------------------------------------------------
# Monotonicity: the two knobs move executability in one direction only
# --------------------------------------------------------------------------------
def _non_executable(n, dv, alt, m, **kw):
    return H.campaign_executability(_legs(n, dv, alt, m, **kw), **kw)["non_executable_impulse_count"]


@SLOW
@given(N_LEGS, LEG_DV, ALT, MASS)
def test_raising_the_burn_floor_never_makes_a_case_more_executable(n, dv, alt, m):
    a = _non_executable(n, dv, alt, m, min_burn_s=0.5)
    b = _non_executable(n, dv, alt, m, min_burn_s=2.0)
    c = _non_executable(n, dv, alt, m, min_burn_s=8.0)
    assert a <= b <= c


@SLOW
@given(N_LEGS, LEG_DV, ALT, MASS)
def test_raising_thrust_never_makes_a_case_more_executable(n, dv, alt, m):
    """More thrust delivers the same dv in less time, so it pushes impulses BELOW the
    floor rather than above it. The intuition runs the other way and the model must
    not follow the intuition."""
    a = _non_executable(n, dv, alt, m, thrust_N=5.0e3)
    b = _non_executable(n, dv, alt, m, thrust_N=20.0e3)
    c = _non_executable(n, dv, alt, m, thrust_N=60.0e3)
    assert a <= b <= c


# --------------------------------------------------------------------------------
# The accounting closes on what was assigned
# --------------------------------------------------------------------------------
@SLOW
@given(N_LEGS, LEG_DV, ALT, MASS, st.booleans())
def test_ignition_accounting_closes_on_the_assignments(n, dv, alt, m, disposal):
    legs = _legs(n, dv, alt, m)
    a = H.restart_accounting(legs, disposal, True)
    me = sum((leg["first_assigned_to"] == H.MAIN_ENGINE)
             + (leg["second_assigned_to"] == H.MAIN_ENGINE) for leg in legs)
    aux = 2 * len(legs) - me
    assert a["main_engine_reposition_ignitions"] == me
    assert a["auxiliary_reposition_impulses"] == aux
    assert a["post_primary_main_engine_ignitions_required"] == me + a["disposal_main_engine_ignitions"]
    assert me + aux == 2 * len(legs)
