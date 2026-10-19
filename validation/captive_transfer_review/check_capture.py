"""Check exact captured evidence and decisive independent invariants."""
from pathlib import Path
import hashlib,json,math,itertools
from audit import positive_interval
from geometry import boxes,cycle
from interlocks import permits

H=Path(__file__).resolve().parent;O=H/"release"
load=lambda n:json.loads((O/n).read_text())
G=load("CONTINUOUS_GEOMETRY.json");N=load("NATIVE_CAD.json");D=load("STOP_DYNAMICS.json");I=load("INTERLOCKS.json")
for d in [G,N]:
    for name,sha in d["source_hashes"].items():assert hashlib.sha256((H/name).read_bytes()).hexdigest()==sha,name
for filename,source in [("STOP_DYNAMICS.json","stop_dynamics.py"),("INTERLOCKS.json","interlocks.py"),("TOLERANCE.json","tolerance.py"),("tooth_fea/RESULTS.json","tooth_fea.py")]:
    assert load(filename)["source_sha256"]==hashlib.sha256((H/source).read_bytes()).hexdigest(),source
assert len(N["cases"])==22 and G["continuous_phase_cases"]==20 and G["penetration_count"]==0
for label,L in [("1U",113.5),("3U",340.5)]:
    sequence=cycle(L)
    for (_,a),(_,b) in zip(sequence,sequence[1:]):
        p,q=boxes(L,a),boxes(L,b)
        for i,j in itertools.combinations(range(len(p)),2):
            if p[i]["name"]!=p[j]["name"]:assert positive_interval(p[i],q[i],p[j],q[j]) is None
for r in N["cases"]:
    assert r["step_valid"] and math.isclose(sum(p["mass_kg"] for p in r["material_ledger"]),r["material_kg"],abs_tol=1e-10)
    assert all(r["inertia_material_kg_m2"][i][i]>0 for i in range(3))
    for name,sha in r["files"].items():assert hashlib.sha256((O/name).read_bytes()).hexdigest()==sha,name
for name,sha in N["arrest_coupon"]["files"].items():assert hashlib.sha256((O/name).read_bytes()).hexdigest()==sha
assert D["count"]==972 and D["runout_failures"]>0 and len(I["guard_cases"])==432 and len(I["counterexamples"])==3
subset=[r for r in D["cases"] if r["speed_m_s"]<=.08 and r["delay_s"]<=.02 and r["assist_N"]==0]
assert len(subset)==216 and all(r["within_12mm_compliance"] and r["within_24mm_total_runout"] for r in subset)
assert any(not r["within_24mm_total_runout"] for r in D["cases"] if r["assist_N"]==50 and r["speed_m_s"]<=.08 and r["delay_s"]<=.02)
F=load("tooth_fea/RESULTS.json");assert len(F["cases"])==6
for r in F["cases"]:
    assert abs(r["root_reaction_y_N"]+r["force_N"])<1e-5*r["force_N"]
    for name,sha in r["files"].items():assert hashlib.sha256((O/"tooth_fea"/name).read_bytes()).hexdigest()==sha,name
for name,sha in json.loads((H/"MANIFEST.json").read_text())["files"].items():
    assert hashlib.sha256((H/name).read_bytes()).hexdigest()==sha,name
print("PASS CT-01: continuous prescribed geometry, independent native captures, conditional stop failures, custody counterexamples and exact evidence hashes. No hardware acceptance.")
