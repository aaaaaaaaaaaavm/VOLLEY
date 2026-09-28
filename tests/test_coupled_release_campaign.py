"""Independent limits and fault controls for the coupled two-release screen."""
import copy
import json
import math
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'analysis'))
import coupled_release_campaign as s7


@pytest.fixture(scope='module')
def plans():
    return s7.plans()


def test_separation_energy_and_galilean_invariance():
    state = np.array([s7.ca.RE+450000, 0, 0, 7600.])
    mass = 310.
    p, h, d = s7.split(state, mass, [3., 4.], .001, .002)
    before = .5*mass*np.dot(state[2:], state[2:])
    after = .5*s7.M*np.dot(p[2:],p[2:])+.5*(mass-s7.M)*np.dot(h[2:],h[2:])
    expected = .5*s7.M*(mass-s7.M)/mass*np.dot(d['relative_velocity_m_s'],d['relative_velocity_m_s'])
    assert after-before == pytest.approx(expected, abs=2e-6)
    boost = np.array([100.,-200.]); moved = state.copy(); moved[2:] += boost
    pb, hb, _ = s7.split(moved, mass, [3.,4.], .001, .002)
    np.testing.assert_allclose(pb[2:]-p[2:], boost, atol=1e-10, rtol=0)
    np.testing.assert_allclose(hb[2:]-h[2:], boost, atol=1e-10, rtol=0)


def test_first_release_error_reaches_second_payload(plans):
    plan = plans[0]
    zero = next(s7.samples())
    perturbed = copy.deepcopy(zero); perturbed['errors'][4] = .1
    a = s7.run(plan, 'REPLAY', zero)
    b = s7.run(plan, 'REPLAY', perturbed)
    # Second release error is zero: this response must come from the first event.
    assert b['errors'][6:] == [0.,0.]
    assert s7.difference(a['second_arrival_state'],b['second_arrival_state'])['position_error_m'] > .001
    assert s7.difference(a['events'][1]['terminal_state'],b['events'][1]['terminal_state'])['position_error_m'] > .001


def test_navigation_does_not_retroactively_repair_first_payload(plans):
    e = next(s7.samples()); e['errors'][0] = 30.
    replay = s7.run(plans[0],'REPLAY',e)
    nav = s7.run(plans[0],'EXACT_NAV_REPLAN',e)
    assert nav['events'][0]['terminal_state'] == replay['events'][0]['terminal_state']
    assert nav['events'][0]['accepted'] == replay['events'][0]['accepted']
    if not nav['events'][0]['accepted']:
        assert not nav['accepted']


def test_mass_and_reserve_with_rocket_equation():
    y = s7.tt.initial(); mass=318.; fuel=10.
    state, after, remaining, _ = s7.burn(y,mass,fuel,[3.,4.])
    assert remaining == pytest.approx(fuel-mass*(1-math.exp(-5/s7.VE)),abs=1e-12)
    assert after-mass == pytest.approx(remaining-fuel,abs=1e-12)
    np.testing.assert_allclose(state[2:]-y[2:],[3.,4.])
    with pytest.raises(ValueError,match='PROPELLANT_RESERVE'):
        s7.burn(y,mass,fuel,[1000.,0.])


def test_invalid_and_corrupted_inputs(plans):
    p=copy.deepcopy(plans[0]); p['first']['separation']['retained_mass_kg'] += 1
    with pytest.raises(ValueError,match='CORRUPT_S4_MASS'):
        s7.run(p,'REPLAY',next(s7.samples()))
    e=next(s7.samples()); e['errors'][0]=float('nan')
    with pytest.raises(ValueError,match='FINITE_ERRORS'):
        s7.run(plans[0],'REPLAY',e)
    with pytest.raises(ValueError,match='UNKNOWN_POLICY'):
        s7.run(plans[0],'RESET_TO_NOMINAL',next(s7.samples()))
    with pytest.raises(ValueError,match='RELEASE_SPEED'):
        s7.split(s7.tt.initial(),310,[1,0],-2,0)


def test_corrupt_s4_source_hash_rejected(tmp_path, monkeypatch):
    data=json.loads(s7.ou.S4_PATH.read_text())
    data['source_sha256']['analysis/manifest_timing.py']='invalid'
    p=tmp_path/'s4.json'; p.write_text(json.dumps(data)); monkeypatch.setattr(s7.ou,'S4_PATH',p)
    with pytest.raises(ValueError,match='stale S4 source'):
        s7.plans()


def test_sample_identity_and_independent_release_signs():
    samples=list(s7.samples())
    assert len(samples)==209
    independent=[s for s in samples if s['family']=='independent_release_only']
    assert len({tuple(s['errors'][4:]) for s in independent})==16
    assert any(s['errors'][4]!=s['errors'][6] for s in independent)
    assert all(s['errors'][:4]==[0.]*4 for s in independent)


def test_independent_circular_limit():
    y=s7.tt.initial(); dt=900.; angle=math.sqrt(s7.ca.MU/y[0]**3)*dt
    reference=np.array([y[0]*math.cos(angle),y[0]*math.sin(angle),
                        -y[3]*math.sin(angle),y[3]*math.cos(angle)])
    for propagated in [s7.coast(y,dt),s7.rk4(y,dt,2.5)]:
        d=s7.difference(propagated,reference)
        assert d['position_error_m'] < .01
        assert d['velocity_error_m_s'] < 1e-5


def test_freshness_preserves_exact_inputs_and_verdicts():
    data={'study':'P113-S7','status':'x','open_items':['P113'],'inputs':{'band':10.},'source_sha256':{'a':'b'},
          'cases':[dict(screen='fixed_1',delay_s=0,policy='REPLAY',family='zero',scale=0,signs=[],errors=[0.]*8,
                        accepted=True,completed=True,stop=None,terminal_state=[1.,2.,3.,4.])],
          'verification':{'passed':True}}
    a=copy.deepcopy(data); a['cases'][0]['terminal_state'][0]+=1e-5
    assert s7.check_outputs(a,data)
    for key,value in [('errors',[1e-12]+[0.]*7),('accepted',False),('policy','EXACT_NAV_REPLAN')]:
        a=copy.deepcopy(data); a['cases'][0][key]=value
        assert not s7.check_outputs(a,data)
    a=copy.deepcopy(data); a['source_sha256']['a']='changed'
    assert not s7.check_outputs(a,data)


def test_report_survives_json_key_sorting():
    data=json.loads(s7.RESULT.read_text())
    reordered=copy.deepcopy(data)
    reordered['verification']['checks']=dict(reversed(list(data['verification']['checks'].items())))
    assert s7.report(reordered)==s7.report(data)
