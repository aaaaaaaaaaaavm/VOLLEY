"""Properties of the host-reference model, checked over generated inputs.

Every rule here is a statement that must hold for ANY admissible input, not for the
reference point. The reference point already has thirty-five identities inside
host_reference.self_test(); these exist because P114 was a statement that happened to
be true at 500 km with a 1000 kg stage and false as a general claim, and nothing that
only evaluates the reference point can see that difference.

Ranges are chosen to stay inside the model's stated domain: low Earth orbit, and an
impulse far below escape, which single_impulse_apogee() rejects by design.
"""
import math

from hypothesis import given, settings, strategies as st

import host_reference as H

ALT = st.floats(min_value=200.0, max_value=2000.0, allow_nan=False, allow_infinity=False)
DV = st.floats(min_value=0.05, max_value=500.0, allow_nan=False, allow_infinity=False)
MASS = st.floats(min_value=400.0, max_value=3000.0, allow_nan=False, allow_infinity=False)
SLOW = settings(deadline=None, max_examples=150)


# --------------------------------------------------------------------------------
# P114: a manoeuvre is not an impulse
# --------------------------------------------------------------------------------
@SLOW
@given(ALT, DV)
def test_single_impulse_beats_the_same_dv_spent_as_a_transfer(alt, dv):
    """The distinction P114 lost, as a general rule rather than one worked case.

    One prograde impulse puts all of the budget into raising apogee. The same budget
    spent as a complete circular transfer pays for circularisation as well, so it
    cannot reach as high. Any claim that reads a two-impulse total as what one burn
    does violates this.
    """
    assert H.single_impulse_apogee(alt, dv)["apogee_rise_km"] > H.hohmann_raise_for_dv(alt, dv)


@SLOW
@given(ALT, DV)
def test_a_prograde_impulse_leaves_perigee_where_it_was(alt, dv):
    """Burning once does not move the altitude you burned at. The orbit is no longer
    circular, and reporting the apogee rise as an altitude change is the error."""
    assert H.single_impulse_apogee(alt, dv)["perigee_alt_km"] == alt


@SLOW
@given(ALT, DV)
def test_the_resulting_orbit_is_elliptical_and_bound(alt, dv):
    ecc = H.single_impulse_apogee(alt, dv)["ecc"]
    assert 0.0 <= ecc < 1.0


@SLOW
@given(ALT, DV, DV)
def test_apogee_rise_is_monotonic_in_dv(alt, a, b):
    lo, hi = sorted((a, b))
    if hi - lo < 1e-9:
        return
    assert (H.single_impulse_apogee(alt, lo)["apogee_rise_km"]
            < H.single_impulse_apogee(alt, hi)["apogee_rise_km"])


# --------------------------------------------------------------------------------
# The Hohmann relation and its inverse
# --------------------------------------------------------------------------------
@SLOW
@given(ALT, DV)
def test_the_hohmann_inversion_round_trips(alt, dv):
    """hohmann_raise_for_dv is a bisection. If it does not invert its own forward
    relation, every altitude in the mission cases is wrong by an unknown amount."""
    assert math.isclose(H.hohmann_raise(alt, H.hohmann_raise_for_dv(alt, dv)), dv, rel_tol=1e-6)


@SLOW
@given(ALT, st.floats(min_value=1.0, max_value=800.0))
def test_the_two_impulses_sum_to_the_total(alt, d_alt):
    dv1, dv2, total = H.hohmann_impulses(alt, d_alt)
    assert math.isclose(dv1 + dv2, total, rel_tol=1e-12)
    assert dv1 > 0 and dv2 > 0


# --------------------------------------------------------------------------------
# The rocket equation and its inverse
# --------------------------------------------------------------------------------
@SLOW
@given(DV, MASS)
def test_dv_from_burn_inverts_burn_time_for(dv, m0):
    assert math.isclose(H.dv_from_burn(H.burn_time_for(dv, m0), m0), dv, rel_tol=1e-9)


@SLOW
@given(DV, MASS)
def test_burn_duration_scales_inversely_with_thrust(dv, m0):
    """Doubling thrust halves the burn, exactly. This is why more thrust makes the
    minimum commandable impulse COARSER rather than finer, which is the direction
    a reader is most likely to get backwards."""
    assert math.isclose(H.burn_time_for(dv, m0, 20.0e3),
                        2.0 * H.burn_time_for(dv, m0, 40.0e3), rel_tol=1e-12)


@SLOW
@given(ALT, st.floats(min_value=0.05, max_value=30.0))
def test_plane_change_matches_the_closed_form(alt, deg):
    assert math.isclose(H.plane_change(alt, deg),
                        2.0 * H.circular_v(alt) * math.sin(math.radians(deg) / 2.0),
                        rel_tol=1e-12)
