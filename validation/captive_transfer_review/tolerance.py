"""Explicit local gap budgets; no assumed global assembly fit pass."""
from pathlib import Path
import json,math,hashlib,itertools
H=Path(__file__).resolve().parent;O=H/"release"
gaps={"fork_payload_X":1.5,"fork_payload_Y":1,"fork_payload_Z":2,
      "guide_shoe_X":1,"guide_shoe_Z":1,"guide_neck":1,"receiver_XY":1,
      "receiver_top":2,"storage_gate_slot":2}
rows=[]
for (name,nominal),angle,temp,deflection in itertools.product(gaps.items(),[.05,.1,.5],[-40,20,80],[0,.5,1.3]):
    alignment=200*math.tan(math.radians(angle))
    thermal=abs(temp-20)*200*abs(23e-6-12e-6)
    residual=nominal-.3-alignment-thermal-deflection
    rows.append(dict(interface=name,nominal_mm=nominal,alignment_deg=angle,temperature_C=temp,assumed_deflection_mm=deflection,
      manufacturing_total_mm=.3,alignment_mm=alignment,thermal_mm=thermal,remaining_mm=residual,positive_gap=residual>0))
d=dict(revision="CT-01-2026-10-19",cases=rows,negative_or_zero=sum(not r["positive_gap"] for r in rows),
   boundary="Common 200mm angular/thermal sensitivity applied conservatively to each local gap; not a GD&T datum stack. Deflections are sensitivity inputs, not predictions from actual assembly FEA. Payload envelope, material, mounts and actual thermal conditions unapproved.",
   source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(O/"TOLERANCE.json").write_text(json.dumps(d,indent=2)+"\n")
assert d["negative_or_zero"]>0
print(len(rows),"local gap sensitivities;",d["negative_or_zero"],"nonpositive")
