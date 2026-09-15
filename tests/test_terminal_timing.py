"""Full-state negative controls and independent elliptic propagation for P113-S3."""
import copy
import json
import math

import numpy as np
import pytest
import terminal_timing as t
from test_campaign_allocation import kepler


@pytest.fixture(scope='module')
def data():
    return t.build()


def independent(state, seconds):
    y = np.asarray(state)
    r, v = y[:2], y[2:]
    radius = np.linalg.norm(r)
    ev = ((np.dot(v, v)-t.MU/radius)*r-np.dot(r, v)*v)/t.MU
    if np.linalg.norm(ev) < 1e-10:
        theta = math.sqrt(t.MU/radius**3)*seconds
        rot = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
        return np.r_[rot@r, rot@v]
    return kepler(y, seconds)


def test_all_accepted_arcs_and_delivery_events(data):
    assert len(data['cases']) == 300
    assert len(data['transfers']) == 60
    transfers = {(r['target'], r['release_time_s']): r for r in data['transfers']}
    for transfer in data['transfers']:
        for arc in transfer['arcs']:
            expected = independent(arc['initial_state'], transfer['release_time_s'])
            got = np.asarray(arc['arrival_state'])
            assert np.linalg.norm(expected[:2]-got[:2]) <= .05
            assert np.linalg.norm(expected[2:]-got[2:]) <= 5e-5
            assert arc['position_error_m'] <= .001
    for row in data['cases']:
        for candidate in row['candidates']:
            if not candidate['accepted']:
                continue
            event = candidate['event']
            expected = independent(event['payload_state'], 3600-row['release_time_s'])
            got = np.asarray(candidate['terminal_state'])
            assert np.linalg.norm(expected[:2]-got[:2]) <= .05
            assert np.linalg.norm(expected[2:]-got[2:]) <= 5e-5
            assert candidate['position_error_m'] <= 10
            assert candidate['velocity_error_m_s'] <= .01
            assert event['momentum_residual_kg_m_s'] <= 1e-6
            assert event['relative_velocity_residual_m_s'] <= 1e-9
            after_first = 314*math.exp(-candidate['first_burn_magnitude_m_s']/(220*t.G0))
            assert after_first == pytest.approx(event['mass_before_second_kg'], abs=1e-9)
            post = after_first*math.exp(-event['second_burn_magnitude_m_s']/(220*t.G0))
            assert post == pytest.approx(event['mass_after_second_kg'], abs=1e-9)
            assert event['retained_mass_kg'] == pytest.approx(314-4-candidate['total_fuel_kg'], abs=1e-9)
            assert candidate['total_fuel_kg'] <= 8+1e-9
            arc = transfers[(row['target'], row['release_time_s'])]['arcs'][candidate['arc_index']]
            assert candidate['first_burn_magnitude_m_s'] == pytest.approx(np.linalg.norm(arc['initial_correction_m_s']))
    for target in t.INPUTS['targets']:
        assert all(any(r['accepted'] and r['target']==target and r['screen']==s for r in data['cases'])
                   for s in t.INPUTS['screens']), 'Reference search criterion 5 failed'


def test_known_boundaries():
    y = t.initial()
    for kick in [[0., 0.], [10., 5.]]:
        start = np.r_[y[:2], y[2:]+kick]
        desired = independent(start, 900)[:2]
        solution = t.shoot(desired, 900)
        assert solution['arcs']
        assert any(np.linalg.norm(np.array(a['initial_correction_m_s'])-kick) <= 1e-6 for a in solution['arcs'])


def test_energy_agreement_cannot_hide_phase_or_velocity_error():
    y = t.target_state('phase_5km', 3600)
    rot = np.array([[math.cos(.01), -math.sin(.01)], [math.sin(.01), math.cos(.01)]])
    wrong_phase = np.r_[rot@y[:2], rot@y[2:]]
    assert t.campaign.elements(y)['energy'] == pytest.approx(t.campaign.elements(wrong_phase)['energy'])
    assert not t.terminal_errors(wrong_phase, y)['accepted']
    wrong_velocity = np.r_[y[:2], -y[2:]]
    assert not t.terminal_errors(wrong_velocity, y)['accepted']


def test_selection_exhaustive_and_nested_grid(data):
    for s in data['selections']:
        eligible = [r for r in data['cases'] if r['target']==s['target'] and r['screen']==s['screen']
                    and r['accepted'] and (s['grid']=='fine_150s' or r['release_time_s']%300==0)]
        if eligible:
            best = sorted(eligible, key=lambda r:(r['best']['total_fuel_kg'], r['release_time_s']))[0]  # noqa: FURB192
            assert s['release_time_s'] == best['release_time_s']
            assert s['fuel_kg'] == best['best']['total_fuel_kg']
        else:
            assert s['fuel_kg'] is None
    for name in t.INPUTS['targets']:
        for screen in t.INPUTS['screens']:
            coarse, fine = [s for s in data['selections'] if s['target']==name and s['screen']==screen]
            if coarse['fuel_kg'] is not None:
                assert fine['fuel_kg'] <= coarse['fuel_kg']


def test_refusals_and_solver_failure(monkeypatch):
    for time in [0, -1, float('nan')]:
        with pytest.raises(ValueError):
            t.shoot([t.RE+450000, 0], time)
    with pytest.raises(ValueError):
        t.shoot([1], 300)
    with pytest.raises(ValueError):
        t.target_state('unknown', 300)
    y = t.initial()
    with pytest.raises(ValueError, match='PROPELLANT_RESERVE'):
        t.separate(y, y[2:]+[0, 20], 314, 0, [1, 1])
    for interval in [[0, 1], [2, 1], [1, float('inf')]]:
        with pytest.raises(ValueError):
            t.separate(y, y[2:], 314, 8, interval)
    def failed(*args, **kwargs):
        raise ValueError('injected solver failure')
    monkeypatch.setattr(t, 'root', failed)
    solution = t.shoot(y[:2], 300)
    assert not solution['arcs']
    assert len(solution['searches']) == 3
    assert all(not s['accepted'] for s in solution['searches'])


def test_freshness_material_corruption_and_determinism(data, tmp_path):
    expected = t.outputs(data)
    assert t.outputs(t.build()) == expected
    assert len(t.check_outputs(tmp_path, expected)) == 3
    for name, content in expected.items():
        dest = tmp_path/name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content)
    assert t.check_outputs(tmp_path, expected) == []
    path = tmp_path/'analysis/results/terminal_timing.json'
    broken = copy.deepcopy(data)
    next(r for r in broken['cases'] if r['accepted'])['best']['total_fuel_kg'] += .01
    path.write_text(json.dumps(broken))
    assert t.check_outputs(tmp_path, expected) == ['analysis/results/terminal_timing.json']
    assert json.loads(path.read_text()) == broken
    path.write_text('[]')
    assert t.check_outputs(tmp_path, expected) == ['analysis/results/terminal_timing.json']
