"""Fast mechanical collision diagnosis; explicitly excludes winding and is not acceptance."""
import json,time
import build_acr1 as b
state='home';t=time.perf_counter()
p=b.foundation()+b.track()+b.bank_mounts()+b.brake()
for side in [-1,1]:
 for level in range(6):p+=b.cell(side,level)
p+=b.sled(200,True,False)+b.cradle(190,True,0)
print('DIAGNOSTIC_MECHANICAL_PARTS',len(p),flush=True)
r=b.audit(p);r['scope']='Diagnostic mechanical subsets only; winding excluded; not final acceptance'
(b.OUT/'MECHANICAL_DIAGNOSTIC.json').write_text(json.dumps(r,indent=2)+'\n')
print('DONE',len(r['interferences']),time.perf_counter()-t,flush=True)
