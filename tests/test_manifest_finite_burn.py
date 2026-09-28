"""Regressions for sequential mass and attitude bookkeeping."""
import math
import sys
from pathlib import Path

import numpy as np
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
import manifest_finite_burn as model


def test_release_changes_retained_mass_and_conserves_momentum():
    y=np.r_[model.tt.initial(),model.INITIAL_MASS]
    for _ in range(model.N):
        before=y.copy()
        payload,y,momentum,relative=model.split(y,2.,[.6,.8],(.0005,.0001))
        assert y[4]==before[4]-model.PAYLOAD
        assert momentum<=1e-6 and relative<=1e-10
        assert np.allclose(payload[:2],y[:2])
    assert y[4]==model.DRY+model.FUEL


def test_only_first_attitude_can_be_prepositioned():
    x=np.array([0.,.1,10.,10.]);axis=[1.,0.]
    first=model.schedule(x,None,axis)
    following=model.schedule(x,math.pi,axis)
    assert first[0]==0.
    assert following[0]==pytest.approx(model.fb.slew(math.pi,0.)+model.fb.SETTLE)
    assert following[1]==pytest.approx(first[1]-following[0])


def test_sequential_burn_accounting_does_not_count_payload_as_fuel():
    y=np.r_[model.tt.initial(),model.INITIAL_MASS]
    x=np.array([0.,.1,10.,20.]);axis=[1.,0.]
    previous=None;total=0.
    for index in range(1,4):
        row=model.evaluate(y,x,index,2.,10.,axis,previous)
        total+=10.*30./model.fb.VE
        expected=model.FUEL-total
        assert row['fuel_remaining_kg']==pytest.approx(expected,abs=1e-9)
        assert row['mass_balance_residual_kg']<=1e-8
        y=np.array(row['host_state']);previous=0.
    assert y[4]==pytest.approx(model.INITIAL_MASS-3*model.PAYLOAD-total,abs=1e-9)


def test_partial_replay_never_claims_full_manifest_acceptance():
    assert model.replay([],2.,10.)['accepted'] is False
    assert model.replay([],2.,10.)['unserved_deliveries']==12


def test_targets_have_declared_arc_spacing():
    a=model.target(1,18000.);b=model.target(2,18000.)
    angle=math.atan2(a[0]*b[1]-a[1]*b[0],np.dot(a[:2],b[:2]))
    assert angle*np.linalg.norm(a[:2])==pytest.approx(5000.,abs=1e-7)
    assert np.dot(a[:2],a[2:])==pytest.approx(0.,abs=1e-4)


def test_invalid_release_speed_rejected():
    with pytest.raises(ValueError,match='INVALID_SEPARATION'):
        model.split(np.r_[model.tt.initial(),358.],1.,[1.,0.],(-1.,0.))
