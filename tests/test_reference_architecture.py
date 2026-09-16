from __future__ import annotations
import importlib.util
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('reference_architecture', ROOT/'analysis/reference_architecture.py')
mod = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(mod)

def data():
    return mod.build()

def test_s4_reference_physics_independent():
    d = data()
    r = next(x for x in d['duty'] if x['speed_mps'] == 4.569852 and x['acceleration_g'] == 10.0)
    m, v, a = 4.0, 4.569852, 10.0*9.80665
    assert math.isclose(r['ideal_payload_energy_J'], 0.5*m*v*v, rel_tol=0, abs_tol=1e-12)
    assert math.isclose(r['ideal_stroke_m'], v*v/(2*a), rel_tol=0, abs_tol=1e-12)
    assert math.isclose(r['acceleration_time_s'], v/a, rel_tol=0, abs_tol=1e-12)
    assert math.isclose(r['constant_force_N'], m*a, rel_tol=0, abs_tol=1e-12)
    assert r['ideal_stroke_m'] < 0.25

def test_high_speed_points_are_not_compact_inherited_requirements():
    d = data()
    r16 = next(x for x in d['duty'] if x['speed_mps'] == 16.029 and x['acceleration_g'] == 25.0)
    r29 = next(x for x in d['duty'] if x['speed_mps'] == 29.009 and x['acceleration_g'] == 25.0)
    assert r16['ideal_stroke_m'] > 0.5
    assert r29['ideal_stroke_m'] > 1.7

def test_reference_passes_concept_hard_screens():
    d = data()
    ref = next(x for x in d['release_concepts'] if x['disposition'] == 'REFERENCE')
    assert ref['name'] == 'motor-charged mechanical accumulator'
    assert ref['payload_modification'] is False
    assert ref['eight_metre_dependency'] is False
    assert ref['independent_cell_compatible'] is True
    assert 'catcher' in ref['pusher_catch_concept']

def test_long_guide_and_bolley_do_not_sneak_into_unmodified_reference():
    d = data()
    long_guide = next(x for x in d['release_concepts'] if x['name'] == 'existing long gas guide')
    bolley = next(x for x in d['release_concepts'] if x['name'] == 'BOLLEY cooperative interface')
    assert long_guide['eight_metre_dependency'] is True
    assert long_guide['disposition'] != 'REFERENCE'
    assert bolley['payload_modification'] is True
    assert bolley['disposition'] != 'REFERENCE'

def test_independent_cell_failure_boundary_is_explicit():
    d = data()
    arrangement = next(x for x in d['payload_arrangements'] if x['disposition'] == 'REFERENCE')
    assert arrangement['name'] == 'independent retained cells'
    assert 'unrelated cells' in arrangement['blocked_path']
    assert 'shared' in arrangement['shared_common_modes']

def test_stored_energy_sensitivity_is_energy_over_efficiency():
    d = data()
    ideal = 0.5*4.0*4.569852**2
    stored = d['s4_point']['stored_input_energy_J']
    assert math.isclose(stored['60pct'], ideal/0.60, rel_tol=0, abs_tol=1e-12)
    assert math.isclose(stored['70pct'], ideal/0.70, rel_tol=0, abs_tol=1e-12)
    assert math.isclose(stored['80pct'], ideal/0.80, rel_tol=0, abs_tol=1e-12)

def test_generated_outputs_are_fresh():
    generated = mod.render(data())
    for path, expected in generated.items():
        assert path.exists()
        if path.suffix == '.json':
            assert json.loads(path.read_text()) == json.loads(expected.decode())
        else:
            assert path.read_bytes() == expected

def test_result_keeps_p92_open_and_falsifiers():
    d = data()
    assert d['status'] == 'REFERENCE_SELECTED_P92_OPEN'
    assert len(d['falsifiers']) >= 5
    assert 'installed mass and envelope for all candidates' in d['open_evidence']
