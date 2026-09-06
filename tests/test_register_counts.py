"""Current register counts must agree without changing the historical entries."""
from collections import Counter
import json
from pathlib import Path
import sys

import pytest
from hypothesis import given, strategies as st

import register_status as R


@given(st.lists(st.sampled_from(["LIVE", "CORRECTED", "CLOSED"]), max_size=200))
def test_rendering_counts_is_idempotent_and_preserves_surrounding_text(statuses):
    rows = [(f"P{i}", status) for i, status in enumerate(statuses)]
    tally = dict.fromkeys(("LIVE", "CORRECTED", "CLOSED"), 0)
    tally.update(Counter(statuses))
    counts = R.payload(rows, tally)
    text = f"Before\n{R.COUNTS_BEGIN}\nstale\n{R.COUNTS_END}\nHistorical entries\n"
    result = R.render_counts(text, counts)
    assert R.render_counts(result, counts) == result
    assert result.startswith("Before\n")
    assert result.endswith("\nHistorical entries\n")
    assert f"> {len(statuses)} numbered entries" in result
    for status in tally:
        assert f"> | `{status}` | {statuses.count(status)}" in result


@pytest.mark.parametrize("marker", [R.COUNTS_BEGIN, R.COUNTS_END])
@pytest.mark.parametrize("copies", [0, 2])
def test_missing_or_duplicate_count_markers_are_rejected(marker, copies):
    text = f"{R.COUNTS_BEGIN}\n{R.COUNTS_END}"
    text = text.replace(marker, marker * copies)
    with pytest.raises(ValueError, match="exactly once"):
        R.render_counts(text, {})


@pytest.mark.parametrize("fault", [None, "headline", "status", "duplicate_status"])
def test_register_gate_rejects_drift(tmp_path, monkeypatch, fault):
    text = Path(R.REGISTER).read_text(encoding="utf-8")
    counts = json.loads(Path(R.RESULT).read_text(encoding="utf-8"))
    if fault == "headline":
        text = text.replace(f"> {counts['total']} numbered entries", "> 0 numbered entries", 1)
    elif fault == "status":
        text = text.replace('> **Status:** `CLOSED`', '> **Status:** `LIVE`', 1)
    elif fault == "duplicate_status":
        line = '> **Status:** `CLOSED`'
        text = text.replace(line, line + '\n' + line, 1)
    register = tmp_path / "register.md"
    result = tmp_path / "counts.json"
    register.write_text(text, encoding="utf-8")
    result.write_text(json.dumps(counts), encoding="utf-8")
    monkeypatch.setattr(R, "REGISTER", str(register))
    monkeypatch.setattr(R, "RESULT", str(result))
    monkeypatch.setattr(sys, "argv", ["register_status.py", "--check"])
    if fault is None:
        R.main()
    else:
        with pytest.raises(SystemExit, match="stale"):
            R.main()
