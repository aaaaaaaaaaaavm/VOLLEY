"""Reintroduce each defect this repository has actually shipped, and require a gate to
catch it.

Every case below was found by review, fixed, and then verified once by hand in a
throwaway script. That verification proved the fix on the day and protected nothing
afterwards. These are the same injections, kept.

A test here fails if the DEFECT stops being caught, which is the opposite of the usual
direction and the reason each one asserts on a non-empty failure list.
"""
import json
import os
import shutil

import pytest

import host_reference as H
import check_links
import check_results_fresh as fresh


# --------------------------------------------------------------------------------
# P116, both directions
# --------------------------------------------------------------------------------
def test_charging_the_engine_for_a_burn_it_cannot_do_is_caught(monkeypatch):
    """The P116 defect exactly: assign every impulse to the main engine regardless of
    whether it reaches the declared minimum burn."""
    original = H.assign_impulse

    def always_main(dv, m0, thrust_N=H.THRUST_N, min_burn_s=H.MIN_BURN_S):
        r = original(dv, m0, thrust_N, min_burn_s)
        r["assigned_to"] = H.MAIN_ENGINE
        r["executable_by_baseline_main_engine"] = True
        return r

    monkeypatch.setattr(H, "assign_impulse", always_main)
    fails = H.self_test()
    assert fails, "the self-test accepted an impulse below the burn floor as an ignition"
    assert any("below the burn floor" in f or "still charged" in f for f in fails)


def test_a_multiplied_campaign_duration_is_caught(monkeypatch):
    """Pacing reverted to the first leg's arc times the leg count."""
    original = H.pacing

    def naive(legs):
        r = original(legs)
        if legs:
            r["summed_transfer_min"] = len(legs) * legs[0]["transfer_min"]
            r["transfer_only_h"] = r["summed_transfer_min"] / 60.0
        return r

    monkeypatch.setattr(H, "pacing", naive)
    fails = H.self_test()
    assert fails, "the self-test accepted a multiplied campaign duration"
    assert any("sum of its legs" in f for f in fails)


def test_a_campaign_that_does_not_propagate_is_caught(monkeypatch):
    """Every leg solved from the reference altitude again, which is what the scaling
    table did before it was corrected."""
    original = H.propagate_campaign

    def flat(steps, start_alt_km=H.REF_ALT_KM, m0=H.STAGE_MASS_KG,
             thrust_N=H.THRUST_N, min_burn_s=H.MIN_BURN_S):
        legs = original(steps, start_alt_km, m0, thrust_N, min_burn_s)
        for leg in legs:
            leg["start_alt_km"] = start_alt_km
            leg["end_alt_km"] = start_alt_km + leg["raise_km"]
        return legs

    monkeypatch.setattr(H, "propagate_campaign", flat)
    fails = H.self_test()
    assert fails, "the self-test accepted a campaign that never leaves its start orbit"
    assert any("propagate" in f for f in fails)


def test_hiding_the_auxiliary_impulses_is_caught(monkeypatch):
    """Zero the auxiliary count so the split no longer adds up to the leg count."""
    original = H.restart_accounting

    def miscount(legs, needs_disposal_burn, disposal_executable=True):
        r = original(legs, needs_disposal_burn, disposal_executable)
        r["auxiliary_reposition_impulses"] = 0
        return r

    monkeypatch.setattr(H, "restart_accounting", miscount)
    fails = H.self_test()
    assert fails, "the self-test accepted an accounting that drops the auxiliary half"


def test_the_self_test_passes_when_nothing_is_broken():
    """The control. Without it the four tests above would pass on a self-test that
    always fails, which would prove nothing."""
    assert H.self_test() == []


def test_the_identity_count_is_counted_not_written_down():
    """It printed "25 identities hold" while self_test() held more, because the number
    was a literal in the print statement. Recomputed here with an independent count of
    the numbered comments, which must agree."""
    import inspect
    import re as _re

    src = inspect.getsource(H.self_test)
    independent = len(_re.findall(r"^\s{4}# \d+\.", src, _re.M))
    assert independent >= 35
    assert H.identity_count() == independent


# --------------------------------------------------------------------------------
# The document gate: exact block comparison
# --------------------------------------------------------------------------------
def test_a_value_edited_inside_a_generated_block_is_caught(tmp_path, monkeypatch):
    """P114's second surface was a correct value beside a wrong label. The gate now
    regenerates each table and compares exact text. This mutates a copy of the real
    document, never the file in the working tree."""
    copy = tmp_path / "doc.md"
    shutil.copy(H.DOC, copy)
    text = copy.read_text(encoding="utf-8")
    assert "| 40.3 |" in text
    copy.write_text(text.replace("| 40.3 |", "| 30.2 |", 1), encoding="utf-8")
    monkeypatch.setattr(H, "DOC", str(copy))
    problems, _ = H.check_doc(H.build())
    assert problems, "the document gate accepted an edited value inside a generated block"


def test_a_removed_block_marker_is_caught(tmp_path, monkeypatch):
    copy = tmp_path / "doc.md"
    shutil.copy(H.DOC, copy)
    text = copy.read_text(encoding="utf-8")
    copy.write_text(text.replace("<!-- HOST_REFERENCE:MASS_FLOW:END -->", "", 1), encoding="utf-8")
    monkeypatch.setattr(H, "DOC", str(copy))
    problems, _ = H.check_doc(H.build())
    assert problems, "the document gate accepted a document with a marker removed"


# --------------------------------------------------------------------------------
# The freshness gate: numeric, not byte-for-byte
# --------------------------------------------------------------------------------
def _results(name):
    with open(os.path.join(fresh.RESULTS, name), encoding="utf-8") as fh:
        return json.load(fh)


def test_freshness_tolerates_one_ulp_and_catches_real_drift():
    """Byte identity is not a property two machines share; P115 and the run-45 failure
    both came from asserting it. The gate must tolerate the last bit and still catch
    the staleness it exists for, which was a factor of 15.6."""
    a = _results("host_reference.json")
    import copy as _copy

    same = _copy.deepcopy(a)
    same["mass_flow_kg_s"] = a["mass_flow_kg_s"] * (1.0 + 2.2e-16)
    assert fresh.differing(a, same, rtol=1e-9, name="host_reference.json") == []

    drifted = _copy.deepcopy(a)
    drifted["mass_flow_kg_s"] = a["mass_flow_kg_s"] * 15.6
    assert fresh.differing(a, drifted, rtol=1e-9, name="host_reference.json")


def test_freshness_catches_a_flipped_verdict_and_a_removed_key():
    a = _results("tube_centreline.json")
    import copy as _copy

    flipped = _copy.deepcopy(a)
    flipped["bands"][6]["pass_"] = not flipped["bands"][6]["pass_"]
    assert fresh.differing(a, flipped, rtol=1e-7, name="tube_centreline.json")

    pruned = _copy.deepcopy(a)
    del pruned["bands"][6]["detail"]
    assert fresh.differing(a, pruned, rtol=1e-7, name="tube_centreline.json")


# --------------------------------------------------------------------------------
# The link gate: $B paths in the issue-seeding script
# --------------------------------------------------------------------------------
def test_a_dead_path_in_the_issue_seeder_is_caught(tmp_path, monkeypatch):
    """docs/PHASE_II.md became docs/VAULT.md across twenty-one files and this one was
    missed, in a file the link gate excluded, so nothing could see it."""
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools" / "seed_issues.sh").write_text(
        'file "x" "y" "See [docs/PHASE_II.md]($B/docs/PHASE_II.md) PII-4."\n', encoding="utf-8")
    monkeypatch.setattr(check_links, "ROOT", str(tmp_path))
    assert check_links.check_seed_paths() == ["docs/PHASE_II.md"]


def test_a_live_path_in_the_issue_seeder_passes(tmp_path, monkeypatch):
    (tmp_path / "tools").mkdir()
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "VAULT.md").write_text("x", encoding="utf-8")
    (tmp_path / "tools" / "seed_issues.sh").write_text(
        'file "x" "y" "See [docs/VAULT.md]($B/docs/VAULT.md) PII-4."\n', encoding="utf-8")
    monkeypatch.setattr(check_links, "ROOT", str(tmp_path))
    assert check_links.check_seed_paths() == []


def test_the_real_seed_script_has_no_dead_paths():
    assert check_links.check_seed_paths() == []
