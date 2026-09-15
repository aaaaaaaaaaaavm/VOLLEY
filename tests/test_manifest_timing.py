"""Coupled two-payload state, conservation and selection checks for P113-S4."""
import copy
import json
import math

import numpy as np
import pytest
import manifest_timing as m
from test_campaign_allocation import kepler


@pytest.fixture(scope='module')
def data():
    return m.build()


def independent(state, seconds):
    y = np.asarray(state, dtype=float)
    r, v = y[:2], y[2:]
    radius = np.linalg.norm(r)
    ev = ((np.dot(v, v)-m.single.MU/radius)*r-np.dot(r, v)*v)/m.single.MU
    if np.linalg.norm(ev) < 1e-10:
        theta = math.sqrt(m.single.MU/radius**3)*seconds
        rot = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
        return np.r_[rot@r, rot@v]
    return kepler(y, seconds)


def test_case_count_transfer_propagation_and_conservation(data):
    assert len(data['cases']) == 100
    assert len(data['selections']) == 60
    assert any(not row['accepted'] for row in data['cases'])
    for row in data['cases']:
        for arc in row['first_transfer']['arcs']:
            expected = independent(arc['initial_state'], row['release_times_s'][0])
            got = np.asarray(arc['arrival_state'])
            assert np.linalg.norm(expected[:2]-got[:2]) <= .05
            assert np.linalg.norm(expected[2:]-got[2:]) <= 5e-5
            assert arc['position_error_m'] <= .001
        for transfer in row['second_transfers']:
            for arc in transfer['arcs']:
                expected = independent(arc['initial_state'], transfer['duration_s'])
                got = np.asarray(arc['arrival_state'])
                assert np.linalg.norm(expected[:2]-got[:2]) <= .05
                assert np.linalg.norm(expected[2:]-got[2:]) <= 5e-5
                assert arc['position_error_m'] <= .001
        for candidate in row['candidates']:
            if not candidate['accepted']:
                continue
            assert len(candidate['events']) == 2
            first, last = candidate['events']
            for event in [first, last]:
                expected = independent(event['separation']['payload_state'],
                                       m.INPUTS['terminal_time_s']-event['time_s'])
                got = np.asarray(event['terminal_state'])
                assert np.linalg.norm(expected[:2]-got[:2]) <= .05
                assert np.linalg.norm(expected[2:]-got[2:]) <= 5e-5
                assert event['terminal_errors']['position_error_m'] <= 10
                assert event['terminal_errors']['velocity_error_m_s'] <= .01
                sep = event['separation']
                assert sep['momentum_residual_kg_m_s'] <= 1e-6
                assert sep['relative_velocity_residual_m_s'] <= 1e-9
                transfer = event['transfer_burn']
                expected_mass = transfer['mass_before_kg']*math.exp(
                    -transfer['magnitude_m_s']/(m.INPUTS['isp_s']*m.single.G0))
                assert transfer['mass_after_kg'] == pytest.approx(expected_mass, abs=1e-9)
            final_sep = last['separation']
            # Initial mass is 300 kg dry + 10 kg fuel + two 4 kg payloads.
            # After both payloads depart, retained mass is dry + remaining fuel.
            assert final_sep['retained_mass_kg'] == pytest.approx(
                310-candidate['total_fuel_kg'], abs=1e-9)
            assert last['fuel_remaining_kg'] >= m.INPUTS['reserve_kg']-1e-9
            assert candidate['total_fuel_kg'] <= 8+1e-9


def test_second_leg_starts_from_retained_host_not_reset(data):
    checked = 0
    for row in data['cases']:
        for candidate in row['candidates']:
            if not candidate['accepted']:
                continue
            first = candidate['events'][0]
            transfer = row['second_transfers'][candidate['second_transfer_index']]
            arc = transfer['arcs'][candidate['second_arc_index']]
            retained = np.asarray(first['separation']['host_state'])
            correction = np.asarray(arc['correction_m_s'])
            initial_state = np.asarray(arc['initial_state'])
            assert np.linalg.norm(initial_state[:2]-retained[:2]) <= 1e-9
            assert np.linalg.norm(initial_state[2:]-(retained[2:]+correction)) <= 1e-9
            assert transfer['start_state'] == pytest.approx(retained.tolist(), abs=1e-9)
            # Negative control: the retained host is not silently the original circular state.
            if np.linalg.norm(retained-m.single.initial()) > 1e-3:
                assert not np.allclose(initial_state, np.r_[m.single.initial()[:2], m.single.initial()[2:]+correction], atol=1e-9)
                checked += 1
    assert checked > 0


def test_translated_noncircular_shoot_uses_supplied_state():
    base = m.single.initial().copy()
    start = base + np.array([1250., -830., 9., -4.])
    desired = independent(start, 750)[:2]
    solution = m.shoot(start, desired, 750)
    assert solution['arcs']
    assert np.asarray(solution['start_state']) == pytest.approx(start, abs=1e-12)
    assert min(np.linalg.norm(np.asarray(a['correction_m_s'])) for a in solution['arcs']) <= 1e-5


def test_exhaustive_selection_and_nested_controls(data):
    orders = ['either']+['then'.join(o) for o in __import__('itertools').permutations(m.INPUTS['manifest_targets'])]
    for selected in data['selections']:
        choices = []
        for row_index, row in enumerate(data['cases']):
            if row['screen'] != selected['screen']:
                continue
            if selected['order'] != 'either' and 'then'.join(row['order']) != selected['order']:
                continue
            if selected['grid'] == 'coarse' and not all(t in m.INPUTS['coarse_times_s'] for t in row['release_times_s']):
                continue
            for candidate_index, candidate in enumerate(row['candidates']):
                if candidate['accepted'] and (selected['policy'] != 'local_only' or candidate['local_first_speed']):
                    choices.append((candidate['total_fuel_kg'], *row['release_times_s'], tuple(row['order']),
                                    row_index, candidate_index))
        winner = min(choices) if choices else None
        assert selected['order'] in orders
        if winner is None:
            assert selected['case_index'] is None and selected['fuel_kg'] is None
        else:
            assert selected['fuel_kg'] == winner[0]
            assert selected['case_index'] == winner[-2]
            assert selected['candidate_index'] == winner[-1]
    for screen in m.INPUTS['screens']:
        for order in orders:
            for policy in ['enumerated', 'local_only']:
                coarse = next(s for s in data['selections'] if s['screen']==screen and s['order']==order
                              and s['policy']==policy and s['grid']=='coarse')
                fine = next(s for s in data['selections'] if s['screen']==screen and s['order']==order
                            and s['policy']==policy and s['grid']=='fine')
                if coarse['fuel_kg'] is not None:
                    assert fine['fuel_kg'] <= coarse['fuel_kg']+1e-12
        enum = next(s for s in data['selections'] if s['screen']==screen and s['order']=='either'
                    and s['policy']=='enumerated' and s['grid']=='fine')
        local = next(s for s in data['selections'] if s['screen']==screen and s['order']=='either'
                     and s['policy']=='local_only' and s['grid']=='fine')
        assert enum['case_index'] is not None, f'{screen} has no complete successful campaign'
        if local['fuel_kg'] is not None:
            assert enum['fuel_kg'] <= local['fuel_kg']+1e-12


def test_refusals_and_partial_failure_controls(monkeypatch):
    good_order = m.INPUTS['manifest_targets']
    for order in [[good_order[0], good_order[0]], ['unknown', good_order[1]]]:
        with pytest.raises(ValueError):
            m.validate(order, [600, 1200], [1, 1], 2)
    for times in [[1200, 600], [600, 600], [0, 600], [600, 3600], [600, float('nan')]]:
        with pytest.raises(ValueError):
            m.validate(good_order, times, [1, 1], 2)
    for interval in [[0, 1], [2, 1], [1, float('inf')], [1]]:
        with pytest.raises(ValueError):
            m.validate(good_order, [600, 1200], interval, 2)
    for reserve in [-1, 11, float('nan')]:
        with pytest.raises(ValueError):
            m.validate(good_order, [600, 1200], [1, 1], reserve)
    with pytest.raises(ValueError, match='PROPELLANT_RESERVE_TRANSFER'):
        m.burn(318, 2, [20, 0], 2)

    class Failed:
        success = False
        x = np.array([0., 0.])
    monkeypatch.setattr(m, 'root', lambda *a, **k: Failed())
    failed = m.shoot(m.single.initial(), m.single.target_state('phase_5km', 600)[:2], 600)
    assert not failed['arcs']
    assert len(failed['searches']) == 3
    assert all(not s['accepted'] for s in failed['searches'])


def test_freshness_tolerance_material_corruption_and_determinism(data, tmp_path):
    expected = m.outputs(data)
    assert m.outputs(m.build()) == expected
    assert m.check_outputs(tmp_path, expected) == ['analysis/results/manifest_timing.json']
    for name, content in expected.items():
        dest = tmp_path/name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content)
    assert m.check_outputs(tmp_path, expected) == []
    result_path = tmp_path/'analysis/results/manifest_timing.json'
    tiny = copy.deepcopy(data)
    next(c for r in tiny['cases'] for c in r['candidates'] if c['accepted'])['total_fuel_kg'] += 1e-10
    result_path.write_text(json.dumps(tiny))
    assert m.check_outputs(tmp_path, expected) == []
    broken = copy.deepcopy(data)
    next(c for r in broken['cases'] for c in r['candidates'] if c['accepted'])['total_fuel_kg'] += .01
    result_path.write_text(json.dumps(broken))
    assert m.check_outputs(tmp_path, expected) == ['analysis/results/manifest_timing.json']
    result_path.write_text('[]')
    assert m.check_outputs(tmp_path, expected) == ['analysis/results/manifest_timing.json']
