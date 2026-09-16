"""Conservation, independent zero error and corruption controls for S6."""
import copy
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import combined_release_errors as cr

def event():
    return cr.ou.selected_campaign(cr.ou.load_s4())[2]["events"][0]

def test_zero_error_recovers_stored_nominal():
    e=event();n=cr.ou.nominal_record(e);r=cr.combined(e,n,[0]*6)
    assert np.linalg.norm(np.asarray(r["terminal_state"])-n["terminal_state"])<1e-9

def test_simultaneous_relative_errors_preserve_momentum():
    e=event();n=cr.ou.nominal_record(e)
    assert cr.combined(e,n,cr.WIDTHS)["momentum_residual_kg_m_s"]<=1e-9

def test_corrupt_mass_fails_before_propagation():
    e=copy.deepcopy(event());n=cr.ou.nominal_record(e)
    e["separation"]["retained_mass_kg"]+=1
    with pytest.raises(ValueError,match="mass accounting"):cr.combined(e,n,cr.WIDTHS)

def test_nonfinite_error_rejected():
    e=event();n=cr.ou.nominal_record(e)
    with pytest.raises(ValueError):cr.combined(e,n,[float("nan")]*6)

def test_freshness_distinguishes_state_roundoff_from_changed_inputs():
    original={"half_widths":list(cr.WIDTHS),"source_sha256":{"source":"original"},
        "cases":[{"event_index":0,"scale":1,"signs":[1]*6,"error_coordinates":list(cr.WIDTHS),
            "terminal_error_vector":[1.0,2.0,0.001,0.002],"mission_bands_passed":True}],"summaries":[]}
    rounded=copy.deepcopy(original)
    rounded["cases"][0]["terminal_error_vector"][0]+=5e-7
    assert cr.numerical_match(rounded,original)
    rounded["cases"][0]["terminal_error_vector"][2]+=1e-6
    assert not cr.numerical_match(rounded,original)
    changed=copy.deepcopy(original);changed["half_widths"][0]+=1e-10
    assert not cr.numerical_match(changed,original)
    changed=copy.deepcopy(original);changed["cases"][0]["error_coordinates"][0]+=1e-10
    assert not cr.numerical_match(changed,original)
    changed=copy.deepcopy(original);changed["source_sha256"]["source"]="changed"
    assert not cr.numerical_match(changed,original)
    changed=copy.deepcopy(original);changed["cases"][0]["mission_bands_passed"]=False
    assert not cr.numerical_match(changed,original)
