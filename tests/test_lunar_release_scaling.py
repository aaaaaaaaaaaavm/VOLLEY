"""Independent limiting cases for the ideal lunar requirements screen."""
import math
import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
import lunar_release_scaling as lunar


def test_circular_period_and_radius():
    radius=lunar.R+100000
    speed=math.sqrt(lunar.MU/radius)
    e=lunar.elements(radius,speed)
    assert e['periapsis_altitude_km']==pytest.approx(100,abs=1e-8)
    assert e['apoapsis_altitude_km']==pytest.approx(100,abs=1e-8)
    assert e['period_s']==pytest.approx(2*math.pi*radius/speed,rel=1e-12)


def test_escape_and_surface_crossing_are_not_safe_orbits():
    radius=lunar.R+100000
    escape=lunar.elements(radius,1.01*math.sqrt(2*lunar.MU/radius))
    assert not escape['bound'] and escape['apoapsis_altitude_km'] is None
    crossing=lunar.elements(radius,.8*math.sqrt(lunar.MU/radius))
    assert crossing['bound'] and not crossing['above_reference_surface']


def test_equal_mass_and_large_host_momentum_limits():
    assert lunar.split(4,4,2)==(1,-1)
    p,h=lunar.split(100,300,4)
    assert p==3 and h==-1
    p,h=lunar.split(1,1e12,2)
    assert p==pytest.approx(2,rel=1e-10)
    with pytest.raises(ValueError): lunar.split(-1,300,2)


def test_rocket_equation_small_burn_limit():
    x=1e-6
    assert lunar.fraction(x,220)==pytest.approx(x/(lunar.G*220),rel=1e-9)
    assert lunar.fraction(0,220)==0
    with pytest.raises(ValueError): lunar.fraction(-1,220)
