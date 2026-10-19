"""Extract true STEP edges for labeled orthographic review figures."""
from pathlib import Path
import json,hashlib
import FreeCAD as App
import Part
H=Path(__file__).resolve().parent;O=H/"release"
out=[]
for stem in ["CT01_3U_stored_captive","CT01_3U_transfer","CT01_3U_receiver_capture","CT01_3U_fork_return","arrest_contact_coupon"]:
    p=O/(stem+".step");s=Part.read(str(p));assert s.isValid()
    out.append(dict(stem=stem,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),edges=[[[v.x,v.y,v.z] for v in e.discretize(Number=2)] for e in s.Edges]))
(O/"STEP_EDGES.json").write_text(json.dumps(out,separators=(",",":"))+"\n")
