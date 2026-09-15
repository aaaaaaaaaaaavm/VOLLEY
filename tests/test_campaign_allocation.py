"""Independent Kepler propagation, conservation and failure controls for P113-S2."""
import math

import numpy as np
import pytest
from scipy.optimize import newton

import campaign_allocation as c


def initial():
    r = c.RE + 450000
    return np.array([r, 0., 0., math.sqrt(c.MU/r)])


def kepler(state, dt):
    """Elliptic elements and eccentric anomaly, independent of integrated acceleration."""
    r, v = state[:2], state[2:]
    radius = np.linalg.norm(r)
    energy = np.dot(v, v)/2-c.MU/radius
    a = -c.MU/(2*energy)
    ev = ((np.dot(v, v)-c.MU/radius)*r-np.dot(r, v)*v)/c.MU
    e = np.linalg.norm(ev)
    p = ev/e
    q = np.array([-p[1], p[0]])
    E0 = math.atan2(np.dot(r, v)/(e*math.sqrt(c.MU*a)), (1-radius/a)/e)
    n = math.sqrt(c.MU/a**3)
    M = E0-e*math.sin(E0)+n*dt
    E = newton(lambda x: x-e*math.sin(x)-M, M,
               fprime=lambda x: 1-e*math.cos(x), tol=1e-13)
    pos = a*((math.cos(E)-e)*p+math.sqrt(1-e*e)*math.sin(E)*q)
    vel = n*a/(1-e*math.cos(E))*(-math.sin(E)*p+math.sqrt(1-e*e)*math.cos(E)*q)
    return np.r_[pos, vel]


def test_circular_period_and_coast_integrals():
    y = initial()
    period = 2*math.pi*math.sqrt(y[0]**3/c.MU)
    z = c.coast(y, period)
    assert np.linalg.norm(z[:2]-y[:2]) <= .01
    assert np.linalg.norm(z[2:]-y[2:]) <= 1e-5
    for kick in [-20, 10, 40]:
        start = y.copy()
        start[3] += kick
        a = c.elements(start)
        for dt in [600, 3600]:
            got = c.coast(start, dt)
            other = kepler(start, dt)
            assert np.linalg.norm(got[:2]-other[:2]) <= .05
            assert np.linalg.norm(got[2:]-other[2:]) <= 5e-5
            tight = c.coast(start, dt, rtol=1e-12)
            assert np.linalg.norm(got[:2]-tight[:2]) <= .05
            b = c.elements(got)
            for key in ['energy', 'angular_momentum']:
                assert abs(b[key]/a[key]-1) <= 1e-9


def test_all_campaign_events_and_accounting():
    data = c.build()
    assert len(data['cases']) == 180
    assert any(not row['completed'] for row in data['cases'])
    assert any(row['completed'] and row['manifest']==12 for row in data['cases'])
    for row in data['cases']:
        assert row['completed'] == (row['delivered']==row['manifest'])
        assert row['fuel_remaining_kg'] >= 2-1e-9
        initial_mass = 310+4*row['manifest']
        assert initial_mass-row['delivered']*4-row['propellant_used_kg'] == pytest.approx(
            row['final_retained_mass_kg'], abs=1e-9)
        assert row['burn_count'] <= row['burn_limit']
        for e in row['events']:
            assert abs(e['achieved_a_m']-e['target_a_m']) <= .01
            assert e['momentum_residual_kg_m_s'] <= 1e-6
            assert e['relative_speed_residual_m_s'] <= 1e-9
            expected = e['mass_before_kg']*math.exp(-abs(e['host_correction_m_s'])/(220*c.G0))
            assert e['mass_after_burn_kg'] == pytest.approx(expected, abs=1e-9)
            assert e['mass_after_burn_kg']-4 == pytest.approx(e['retained_mass_kg'], abs=1e-9)


def test_no_burn_and_failed_release_has_no_side_effect():
    y = initial()
    target = y.copy()
    target[3] += (1-4/314)*1.5
    a = c.elements(target)['a_m']
    e = c.release(y, 314, 4, 0, 220, a, [.5, 2])
    assert abs(e['host_correction_m_s']) <= 1e-8
    assert e['relative_speed_m_s'] == pytest.approx(1.5, abs=1e-8)
    assert e['retained_mass_kg'] == 310
    original = y.copy()
    with pytest.raises(ValueError, match='PROPELLANT_RESERVE'):
        c.release(y, 314, 4, 0, 220, c.RE+500000, [1, 1])
    assert np.array_equal(y, original)
    failed = c.campaign(12, 600, 'COMMON_ENERGY', [1, 1], 0)
    assert failed['delivered'] == 0
    assert failed['propellant_used_kg'] == 0
    assert failed['stopping_reason'] == 'BURN_COUNT_LIMIT'


def test_invalid_inputs_and_guard():
    y = initial()
    for dt in [-1, float('nan'), float('inf')]:
        with pytest.raises(ValueError):
            c.coast(y, dt)
    for state in [[1, 2], [0, 0, 1, 2], [float('nan'), 0, 0, 1]]:
        with pytest.raises(ValueError):
            c.coast(state, 600)
    low = y.copy()
    low[3] -= 300
    with pytest.raises(ValueError, match='HOST_PERIGEE_GUARD'):
        c.coast(low, 600)
    args = [y, 314, 4, 8, 220, c.RE+460000, [.5, 2]]
    for i, value in [(1, 4), (2, 0), (3, -1), (3, 310), (4, 0), (5, float('nan')),
                     (6, [2, 1]), (6, [0, 2])]:
        invalid = args.copy()
        invalid[i] = value
        with pytest.raises(ValueError):
            c.release(*invalid)
    with pytest.raises(ValueError, match='TARGET_ENERGY_UNAVAILABLE'):
        c.release(y, 314, 4, 8, 220, 1000, [1, 1])
    for n, spacing, mission, count in [(0, 600, 'COMMON_ENERGY', 12),
                                     (1, 0, 'COMMON_ENERGY', 12),
                                     (1, 600, 'UNKNOWN', 12),
                                     (1, 600, 'COMMON_ENERGY', -1)]:
        with pytest.raises(ValueError):
            c.campaign(n, spacing, mission, [1, 1], count)


def test_propagation_failure_is_not_a_result(monkeypatch):
    class Failed:
        success = False
    monkeypatch.setattr(c, 'solve_ivp', lambda *a, **k: Failed())
    with pytest.raises(ValueError, match='PROPAGATION_FAILED'):
        c.coast(initial(), 600)


def test_freshness_and_retained_failures(tmp_path):
    data = c.build()
    rendered = c.outputs(data)
    assert rendered == c.outputs(c.build())
    assert len(c.check_outputs(tmp_path, rendered)) == 3
    for path, content in rendered.items():
        dest = tmp_path/path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content)
    assert c.check_outputs(tmp_path, rendered) == []
    path = tmp_path/'analysis/results/campaign_allocation.json'
    path.write_text('corrupted\n')
    assert c.check_outputs(tmp_path, rendered) == ['analysis/results/campaign_allocation.json']
    assert path.read_text() == 'corrupted\n'


def test_portable_numeric_freshness_does_not_accept_material_drift(tmp_path):
    import copy
    import json
    original = c.build()
    perturbed = copy.deepcopy(original)
    row = next(r for r in perturbed['cases'] if r['propellant_used_kg'] > 0)
    row['propellant_used_kg'] += 1e-10
    for path, content in c.outputs(perturbed).items():
        dest = tmp_path/path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content)
    expected = c.outputs(original)
    assert c.check_outputs(tmp_path, expected) == []
    row['propellant_used_kg'] += .01
    path = tmp_path/'analysis/results/campaign_allocation.json'
    path.write_text(json.dumps(perturbed))
    assert c.check_outputs(tmp_path, expected) == ['analysis/results/campaign_allocation.json']
    path.write_text('[]')
    assert c.check_outputs(tmp_path, expected) == ['analysis/results/campaign_allocation.json']
    assert not c.numerical_match(True, 1)
    assert not c.numerical_match(float('nan'), 0.)
    assert not c.numerical_match({'a': 1.}, {'b': 1.})


def test_cartesian_freshness_uses_units_without_relaxing_decisions():
    # The same micrometre perturbation is accepted on either side of an axis crossing.
    for x in [0., 1., 500000.]:
        a = {'host_state': [x, 6000000., 0., 7600.]}
        b = {'host_state': [x+1e-6, 6000000., 1e-8, 7600.]}
        assert c.numerical_match(a, b)
        b['host_state'][0] += .01
        assert not c.numerical_match(a, b)
    assert c.numerical_match({'position_error_m': .0001134847994889407},
                             {'position_error_m': .00011390616641796057})
    assert not c.numerical_match({'position_error_m': 0.}, {'position_error_m': .01})
    assert not c.numerical_match({'fuel_kg': 1.}, {'fuel_kg': 1.000001})
    assert not c.numerical_match({'accepted': True}, {'accepted': False})
    assert not c.numerical_match({'payload_state': [1., 1., 0., 1.]},
                                 {'payload_state': [1., 1., .001, 1.]})


def test_scalar_velocity_freshness_retains_physical_and_discrete_checks():
    # GitHub run 34928809087: the vector policy omitted norms with the same units.
    observed = [('second_burn_magnitude_m_s', .514326376982996, .5143263781868894),
                ('velocity_error_m_s', 8.46841394399364e-8, 8.74078291464722e-8)]
    for field, stored, runner in observed:
        assert c.numerical_match({field: stored}, {field: runner})
        assert not c.numerical_match({field: stored}, {field: stored+1e-6})
    for field in ['first_burn_magnitude_m_s', 'total_host_delta_v_m_s',
                  'delta_v_m_s', 'host_correction_m_s']:
        assert c.numerical_match({field: 0.}, {field: 1e-8})
        assert not c.numerical_match({field: 0.}, {field: 1e-6})
    # Do not extend the velocity budget to conservation residuals or propellant.
    for field in ['relative_velocity_residual_m_s', 'momentum_residual_kg_m_s', 'fuel_kg']:
        assert not c.numerical_match({field: 0.}, {field: 1e-8})
    assert not c.numerical_match({'accepted': False}, {'accepted': True})
