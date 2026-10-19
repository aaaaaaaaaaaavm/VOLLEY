"""Captured limited concept integrity; negative integration result retained."""
from pathlib import Path
import json,hashlib,math
H=Path(__file__).resolve().parent
d=json.loads((H/"release/RESULTS.json").read_text())
assert hashlib.sha256((H/"analyze.py").read_bytes()).hexdigest()==d["source_sha256"]
assert len(d["capture_cases"])==108 and len(d["insertion_cases"])==36 and d["fit_failures"]==18
assert d["baseline_disposition"]=="NO_GO_FOR_OPERATIONAL_REPLENISHMENT_CLAIM"
for r in d["capture_cases"]:
    assert math.isclose(r["mean_energy_force_N"]*r["assumed_stopping_m"],r["energy_J"],rel_tol=1e-12)
    assert math.isclose(r["host_delta_v_m_s"]*300,r["linear_impulse_Ns"],rel_tol=1e-12)
for r in d["insertion_cases"]:assert r["positive_gap"]==(r["remaining_mm"]>0)
for name,sha in json.loads((H/"MANIFEST.json").read_text())["files"].items():assert hashlib.sha256((H/name).read_bytes()).hexdigest()==sha,name
print("PASS RPL-01:108 capture/36 fit sensitivities,18 failed fits, bounded no-go and exact evidence hashes")
