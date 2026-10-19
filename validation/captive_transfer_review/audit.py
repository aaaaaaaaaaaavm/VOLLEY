"""Exact simultaneous interval test for translating axis-aligned boxes.

For each axis, separation is linear in phase fraction. Intersect the open time
intervals with positive penetration in all three axes. No sampling substitutes
for this continuous prescribed-motion calculation. Curved/contact motion absent.
"""
from pathlib import Path
import hashlib
import json
import itertools
from geometry import REVISION, boxes, cycle

HERE=Path(__file__).resolve().parent
OUT=HERE/"release"


def positive_interval(a0,a1,b0,b1):
    lower,upper=0.0,1.0
    for axis in range(3):
        # a_lo < b_hi AND b_lo < a_hi, strictly (touching is not penetration).
        for c,d in [(b0["lo"][axis]+b0["size"][axis]-a0["lo"][axis],
                      b1["lo"][axis]-b0["lo"][axis]-a1["lo"][axis]+a0["lo"][axis]),
                     (a0["lo"][axis]+a0["size"][axis]-b0["lo"][axis],
                      a1["lo"][axis]-a0["lo"][axis]-b1["lo"][axis]+b0["lo"][axis])]:
            if abs(d)<1e-12:
                if c<=1e-10: return None
            elif d>0: lower=max(lower,-c/d)
            else: upper=min(upper,-c/d)
    return [max(0,lower),min(1,upper)] if upper-lower>1e-10 else None


def run():
    results=[]
    for label,L in [("1U",113.5),("3U",340.5)]:
        phases=cycle(L)
        for (n0,s0),(n1,s1) in zip(phases,phases[1:]):
            p0,p1=boxes(L,s0),boxes(L,s1)
            collisions=[]; pairs=0
            for i,j in itertools.combinations(range(len(p0)),2):
                if p0[i]["name"]==p0[j]["name"]:continue
                pairs+=1
                interval=positive_interval(p0[i],p1[i],p0[j],p1[j])
                if interval:collisions.append(dict(parts=[p0[i]["name"],p0[j]["name"]],fraction=interval))
            results.append(dict(payload=label,phase=n1,start=n0,primitive_pairs=pairs,penetrations=collisions))
    # Deliberate geometric defect must be detected without hitting a sample time.
    a0=dict(lo=[0,0,0],size=[.01,1,1]);a1=dict(lo=[1,0,0],size=a0["size"])
    b=dict(lo=[.5545,0,0],size=[.001,1,1])
    assert positive_interval(a0,a1,b,b) is not None
    for t in [0,.5,1]:
        sampled=dict(lo=[t,0,0],size=a0["size"])
        assert positive_interval(sampled,sampled,b,b) is None
    total=sum(len(x["penetrations"]) for x in results)
    report=dict(revision=REVISION,method="simultaneous open interval slab inequalities; linear translation only",cases=results,
                continuous_phase_cases=len(results),penetration_count=total,
                boundary="Nominal prescribed rectangular geometry; fused same-part constituents excluded. No contact force, actuator linkage, tolerance, elastic or hardware qualification.",
                source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE/"geometry.py",Path(__file__)]})
    OUT.mkdir(exist_ok=True)
    (OUT/"CONTINUOUS_GEOMETRY.json").write_text(json.dumps(report,indent=2)+"\n")
    print(f"{len(results)} continuous phase cases; {total} penetrating primitive pairs")
    for c in results:
        if c["penetrations"]:print(c)
    return report


if __name__=="__main__":
    assert run()["penetration_count"]==0
