from pathlib import Path
import json,numpy as np,cadquery as cq
from scipy.optimize import linear_sum_assignment
H=Path(__file__).resolve().parent;d=json.loads((H/'NATIVE_SOLID_SIGNATURES.json').read_text());native=[dict(name=o['name'],**s)for o in d['objects']for s in o['solids']]
shape=cq.importers.importStep(str(H/'home_first_snapshot/VOLLEY_G5_ACR1_home.step')).val();step=[]
for s in shape.Solids():
 b=s.BoundingBox();step.append({'volume_mm3':s.Volume(),'centre_mm':list(s.Center().toTuple()),'bounds_mm':[b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax]})
assert len(native)==len(step)
a=np.array([q['centre_mm']for q in native]);b=np.array([q['centre_mm']for q in step]);va=np.array([q['volume_mm3']for q in native]);vb=np.array([q['volume_mm3']for q in step])
cost=np.linalg.norm(a[:,None,:]-b[None,:,:],axis=2)+100*abs(va[:,None]-vb[None,:])/np.maximum(1,va[:,None]);ii,jj=linear_sum_assignment(cost);results=[]
for i,j in zip(ii,jj):
 n=native[i];s=step[j];results.append({'name':n['name'],'solid_index':n['index'],'native_volume':n['volume_mm3'],'step_volume':s['volume_mm3'],'delta_mm3':s['volume_mm3']-n['volume_mm3'],'centroid_difference_mm':float(np.linalg.norm(a[i]-b[j])),'maximum_bbox_difference_mm':float(np.max(np.abs(np.array(n['bounds_mm'])-np.array(s['bounds_mm']))))})
results.sort(key=lambda x:abs(x['delta_mm3']),reverse=True)
(H/'VOLUME_DIAGNOSIS.json').write_text(json.dumps({'snapshot':'Firsthome0bf0b336','matches':results,'delta_sum_mm3':sum(q['delta_mm3']for q in results)},indent=2)+'\n')
for q in results[:18]:print(q)
