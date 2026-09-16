"""Independent checks for P113-S5 local operational uncertainty."""
from __future__ import annotations

import copy
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
SPEC = importlib.util.spec_from_file_location("operational_uncertainty", ROOT / "analysis/operational_uncertainty.py")
ou = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ou)


def selected_events():
    data = ou.load_s4()
    _, _, candidate = ou.selected_campaign(data)
    return candidate["events"]


def test_local_basis_is_orthonormal():
    for event in selected_events():
        r, t = ou.basis(event["separation"]["payload_state"][:2])
        assert np.linalg.norm(r) == pytest.approx(1.0, abs=1e-12)
        assert np.linalg.norm(t) == pytest.approx(1.0, abs=1e-12)
        assert float(np.dot(r, t)) == pytest.approx(0.0, abs=1e-12)


def test_nominal_terminal_state_reproduces():
    for event in selected_events():
        nominal = ou.nominal_record(event)
        assert nominal["reproduction_position_m"] <= 1e-6
        assert nominal["reproduction_velocity_m_s"] <= 1e-9


def test_mechanism_reconstruction_preserves_momentum_and_relative_velocity():
    for event in selected_events():
        sep = event["separation"]
        u = np.asarray(sep["relative_velocity_m_s"], dtype=float)
        changed = u + 0.001*u/np.linalg.norm(u)
        payload, host, residual = ou.reconstruct_mechanism_state(event, changed)
        assert residual <= 1e-9
        assert np.linalg.norm((payload[2:]-host[2:])-changed) <= 1e-12


def test_corrupt_mass_is_rejected():
    event = copy.deepcopy(selected_events()[0])
    event["separation"]["retained_mass_kg"] += 1.0
    with pytest.raises(ValueError, match="mass accounting"):
        ou.reconstruct_mechanism_state(event, event["separation"]["relative_velocity_m_s"])


def test_corrupt_relative_vector_is_rejected():
    event = copy.deepcopy(selected_events()[0])
    event["separation"]["relative_velocity_m_s"][0] += 0.1
    with pytest.raises(ValueError, match="relative-release vector"):
        ou.reconstruct_mechanism_state(event, event["separation"]["relative_velocity_m_s"])


def test_corrupt_terminal_state_is_rejected():
    event = copy.deepcopy(selected_events()[0])
    event["terminal_state"][0] += 1.0
    with pytest.raises(ValueError, match="does not reproduce"):
        ou.nominal_record(event)


def test_declared_symmetry_convergence_and_momentum_bands():
    data = ou.build()
    assert data["verification_passed"]
    for event in data["events"]:
        assert event["verification_passed"]
        for s in event["sensitivities"]:
            assert s["symmetry_position"]["passed"]
            assert s["symmetry_velocity"]["passed"]
            assert s["convergence_position"]["passed"]
            assert s["convergence_velocity"]["passed"]
            assert s["momentum_passed"]
            if s["maximum_momentum_residual_kg_m_s"] is not None:
                assert s["maximum_momentum_residual_kg_m_s"] <= 1e-9


def test_direction_step_is_declared_in_radians():
    steps = dict((name, step) for name, _, _, step in ou.PERTURBATIONS)
    assert steps["release_direction_rad"] == pytest.approx(math.radians(0.01), rel=0, abs=1e-16)


def test_schedule_headroom_is_only_timestamp_arithmetic():
    result = ou.schedule_headroom(selected_events())
    assert result["label"] == "SCHEDULE_HEADROOM_ONLY"
    gap = result["intervals"]["between_releases_s"]
    for marker in ou.DEAD_TIME_MARKERS_S:
        assert result["between_release_marker_pass"][str(marker)] is (gap >= marker)


def test_generated_outputs_are_fresh():
    data = ou.build()
    expected = ou.serialized(data)
    paths = (ou.OUTPUT_JSON, ou.OUTPUT_DOC, ou.OUTPUT_SVG)
    for path, text in zip(paths, expected):
        assert path.exists(), f"missing generated output {path.relative_to(ROOT)}"
        assert path.read_text(encoding="utf-8") == text
    stored = json.loads(ou.OUTPUT_JSON.read_text(encoding="utf-8"))
    assert stored["source_sha256"] == data["source_sha256"]
