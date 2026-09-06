"""A13's original thresholds must respond to the quantities being tested."""
import copy
import json
import math
from pathlib import Path

import pytest
from hypothesis import given, strategies as st

import attitude_budget as A


ROWS = A.sweep()
SHOT = A.M_SAT * A.V_EXIT
RESULT = Path(A.RESULTS) / "attitude_budget.json"


def record():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_committed_record_passes_the_gate():
    assert A.check_result(record()) == []


@pytest.mark.parametrize("row", [1, 2, 3, 4, 5, 6])
def test_cached_verdict_after_an_input_change_is_caught(row):
    data = record()
    row500 = next(r for r in data["host_sweep"] if r["host_kg"] == 500)
    row200 = next(r for r in data["host_sweep"] if r["host_kg"] == 200)
    if row in (1, 2):
        move = row500["index" if row == 1 else "sled_return"]
        move["peak_linear_momentum_Ns"] = data["shot_impulse_Ns"]
    elif row in (3, 4):
        (row500 if row == 3 else row200)["sequential_peak_rate_deg_s"] = 0
    elif row == 5:
        row500["residual_rate_deg_s"] = 0.01
    else:
        row500["index"]["net_internal_momentum_change_Ns"] = SHOT
    assert A.check_result(data), "the gate accepted a verdict cached before its input changed"


def test_superseded_mass_description_is_caught():
    data = record()
    data["assumptions"]["deployer_inertia"] = "124.5 kg box at the 1.839 x 0.530 m envelope"
    assert A.check_result(data)


def test_changed_source_identity_is_caught():
    data = record()
    data["software"]["source_sha256"] = ""
    assert A.check_result(data)


def test_cached_summary_verdict_is_caught():
    data = record()
    data["verdict"] = "PASS"
    assert A.check_result(data)


@given(st.floats(min_value=0, max_value=1000, allow_nan=False, allow_infinity=False))
def test_rate_verdicts_follow_the_strict_original_bands(rate):
    rows = copy.deepcopy(ROWS)
    for row in rows:
        row["sequential_peak_rate_deg_s"] = rate
    bands = A.evaluate_bands(rows, SHOT)
    assert (bands[2]["verdict"] == "PASS") == (rate < 0.05)
    assert (bands[3]["verdict"] == "PASS") == (rate < 0.2)


@pytest.mark.parametrize("limit", [0.05, 0.2])
@pytest.mark.parametrize("direction", [-math.inf, 0, math.inf])
def test_exact_and_adjacent_rate_boundaries(limit, direction):
    rate = limit if direction == 0 else math.nextafter(limit, direction)
    rows = copy.deepcopy(ROWS)
    for row in rows:
        row["sequential_peak_rate_deg_s"] = rate
    band = A.evaluate_bands(rows, SHOT)[2 if limit == 0.05 else 3]
    assert (band["verdict"] == "PASS") == (rate < limit)


@given(st.floats(min_value=0, max_value=1000, allow_nan=False, allow_infinity=False))
def test_momentum_verdicts_follow_the_strict_original_bands(momentum):
    rows = copy.deepcopy(ROWS)
    row500 = next(r for r in rows if r["host_kg"] == 500)
    for name in ("index", "sled_return"):
        row500[name]["peak_linear_momentum_Ns"] = momentum
    bands = A.evaluate_bands(rows, SHOT)
    percent = 100 * momentum / SHOT
    assert (bands[0]["verdict"] == "PASS") == (percent < 10)
    assert (bands[1]["verdict"] == "PASS") == (percent < 20)


@given(st.floats(min_value=-1000, max_value=1000, allow_nan=False, allow_infinity=False))
def test_campaign_momentum_uses_the_magnitude_of_the_endpoint_change(change):
    rows = copy.deepcopy(ROWS)
    row500 = next(r for r in rows if r["host_kg"] == 500)
    row500["index"]["net_internal_momentum_change_Ns"] = change
    band = A.evaluate_bands(rows, SHOT)[5]
    total = abs(A.N_SHOTS * change)
    assert band["result_Ns"] == total
    assert (band["verdict"] == "PASS BY THE CLOSED INTERNAL CYCLE") == (
        total < 0.05 * row500["index"]["peak_linear_momentum_Ns"])


@pytest.mark.parametrize("rate", [0.01, -0.01, 1, math.inf, math.nan])
def test_no_settling_time_is_invented_for_an_unsettled_endpoint(rate):
    rows = copy.deepcopy(ROWS)
    next(r for r in rows if r["host_kg"] == 500)["residual_rate_deg_s"] = rate
    band = A.evaluate_bands(rows, SHOT)[4]
    assert band["result_s"] is None
    assert band["verdict"].startswith("VOID")


@given(mass=st.floats(0.001, 1000), distance=st.floats(0.001, 100),
       duration=st.floats(0.001, 1000), inertia=st.floats(0.001, 100000))
def test_closed_internal_move_has_no_endpoint_momentum(mass, distance, duration, inertia):
    moved = A.move(mass, distance, duration, inertia, n=51)
    assert moved["net_internal_momentum_change_Ns"] == 0
    assert moved["residual_body_rate_deg_s"] == 0
    assert moved["peak_body_rate_deg_s"] > 0
    assert moved["attitude_offset_deg"] < 0


@pytest.mark.parametrize("shot", [0, -1, math.nan, math.inf])
def test_invalid_shot_reference_is_rejected(shot):
    with pytest.raises(ValueError, match="positive and finite"):
        A.evaluate_bands(ROWS, shot)
