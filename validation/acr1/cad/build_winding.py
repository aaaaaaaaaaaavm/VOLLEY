"""Capture and verify the actual three phase conductors and stepped support boards."""
import json,time
import build_acr1 as b
t=time.perf_counter();p=b.winding();print('WINDING_PARTS',len(p),flush=True)
r=b.audit(p)
record=b.export(p,'winding');record['audit']=r
record['elapsed_s']=time.perf_counter()-t
(b.OUT/'WINDING_DIAGNOSTIC.json').write_text(json.dumps(record,indent=2)+'\n')
print('DONE',len(r['interferences']),record['elapsed_s'],flush=True)
