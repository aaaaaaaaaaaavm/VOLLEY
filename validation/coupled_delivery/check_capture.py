"""Check bounded campaign captures and preserve failed fuel countercases."""

from pathlib import Path
import json, hashlib

H = Path(__file__).resolve().parent
O = H / "release"
d = json.loads((O / "RESULTS.json").read_text())
r = json.loads((O / "RESERVE_CASES.json").read_text())
f = json.loads((O / "REFINEMENT.json").read_text())
assert len(d["cases"]) == 6 and len(r["cases"]) == 3 and len(f["cases"]) == 6
failed = [c for c in d["cases"] if c.get("status") == "FAILED"]
assert (
    len(failed) == 1 and failed[0]["count"] == 12 and failed[0]["strategy"] == "spring"
)
for c in d["cases"] + r["cases"]:
    if "fuel_used_kg" not in c:
        continue
    assert c["fuel_used_kg"] < c["initial_fuel_kg"]
    assert c["maximum_terminal_position_residual_m"] < 0.001
    assert all(x["momentum_identity_residual_kg_m_s"] < 1e-7 for x in c["shots"])
    assert all(
        x.get("passes", x.get("passes_conditional_20m_screen", False))
        for x in c["clearance"]
    )
    if c["strategy"] == "volley_3_6":
        assert 3 <= c["maximum_release_m_s"] <= 6
    if c["count"] == 12 and c["strategy"] == "spring":
        assert c["initial_fuel_kg"] == 20
for c in f["cases"]:
    if c["status"] == "COMPUTED":
        assert abs(c["fuel_change_kg"]) < 1e-7
for name, sha in json.loads((H / "MANIFEST.json").read_text())["files"].items():
    assert hashlib.sha256((H / name).read_bytes()).hexdigest() == sha, name
print(
    "PASS:6 campaign cases,3 reserve countercases,6 refinement cases and exact hashes. Conditional point-center screen is not flight clearance."
)
