"""Independent limits and energy identities for the mechanical screen."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import reference_cell_mechanics as cell

def test_force_integral_and_catcher_partition():
    for r in (0,0.25,0.5,0.75):
        d=cell.case(4,0.25,4.5,0.16,r,2)
        x=np.linspace(0,0.16,101)
        force=d["stiffness_n_m"]*(d["initial_compression_m"]-x)-2
        assert np.trapezoid(force,x)==pytest.approx(0.5*4.25*4.5**2,abs=1e-9)
        assert d["catcher_energy_j"]==pytest.approx(0.5*0.25*4.5**2)

def test_zero_preload_requires_twice_constant_force_stroke():
    speed=4.5
    d=cell.case(4,0.25,speed,speed**2/(10*cell.G),0,0)
    assert d["peak_net_acceleration_g"]==pytest.approx(10,abs=1e-12)
    assert cell.case(4,0.25,speed,speed**2/(20*cell.G),0,0)["peak_net_acceleration_g"]==pytest.approx(20)

def test_exit_contact_failure_is_retained():
    assert "CONTACT_ASSUMPTION_FAILS_AT_EXIT" in cell.case(4,0.25,4.5,0.24,0,2)["rejection_reasons"]

@pytest.mark.parametrize("ratio",[-0.1,1,1.1])
def test_invalid_spring_ratio_rejected(ratio):
    with pytest.raises(ValueError):cell.case(4,0.25,4.5,0.16,ratio,0)

def test_declared_grid_and_provenance():
    d=cell.build()
    assert len(d["cases"])==144 and d["verification_passed"]
    assert d["open_items"]==["P92"]
