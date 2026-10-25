"""Separate import of an immutable copied ACR1 native/STEP state capture.
Usage: python read_state_step.py SNAPSHOT_DIR STEM --expected-step-sha HASH
"""
from pathlib import Path
import argparse,json,hashlib,platform,time
import cadquery as cq,OCP
ap=argparse.ArgumentParser();ap.add_argument('snapshot',type=Path);ap.add_argument('stem');ap.add_argument('--expected-step-sha',required=True);a=ap.parse_args();p=a.snapshot/(a.stem+'.json');s=a.snapshot/(a.stem+'.step');mb=p.read_bytes();sb=s.read_bytes();m=json.loads(mb);digest=hashlib.sha256(sb).hexdigest();assert digest==a.expected_step_sha
start=time.perf_counter();sh=cq.importers.importStep(str(s)).val();solids=sh.Solids();v=sum(q.Volume()for q in solids);native=sum(q['volume_mm3']for q in m['BOM']);delta=abs(v-native);limit=max(.01,1e-6*native)
report={'configuration_id':m['configuration_id'],'state':m['state'],'scope':'Copied state serialization/BRep check only; no other motion/assembly completion inferred.','method':'SeparateCadQuery/OCPbinding and newerOpenCASCADEversion; samekernelfamily,notindependentkernelqualification.','software':{'Python':platform.python_version(),'CadQuery':cq.__version__,'OCP':OCP.__version__},'source_identity':{'builder_sha256':m['builder_sha256'],'parameters_sha256':m['parameters_sha256'],'native_json_sha256':hashlib.sha256(mb).hexdigest(),'step_sha256':digest,'native_FCStd_sha256':hashlib.sha256((a.snapshot/(a.stem+'.FCStd')).read_bytes()).hexdigest()},'native_parts':m['parts'],'native_solids':m['solids'],'imported_solids':len(solids),'valid':bool(sh.isValid()and all(q.isValid()for q in solids)),'native_volume_mm3':native,'imported_volume_mm3':v,'absolute_volume_difference_mm3':delta,'relative_volume_difference':delta/native,'volume_tolerance_mm3':limit,'inputs_unchanged':mb==p.read_bytes()and digest==hashlib.sha256(s.read_bytes()).hexdigest(),'wall_s':time.perf_counter()-start}
report['pass']=bool(report['valid']and len(solids)==m['solids']and delta<=limit and report['inputs_unchanged']);out=a.snapshot/'STEP_READBACK.json';out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True);assert report['pass']
signature_path=a.snapshot/'NATIVE_SOLID_SIGNATURES.json'
if signature_path.exists():
    import numpy as np
    from scipy.optimize import linear_sum_assignment
    signatures=json.loads(signature_path.read_text())
    assert signatures['source_sha256']==report['source_identity']['native_FCStd_sha256']
    native=[dict(name=o['name'],**q)for o in signatures['objects']for q in o['solids']]
    imported=[]
    for q in solids:
        b=q.BoundingBox();imported.append(dict(volume_mm3=q.Volume(),centre_mm=list(q.Center().toTuple()),bounds_mm=[b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax]))
    assert len(native)==len(imported)
    ca=np.array([q['centre_mm']for q in native]);cb=np.array([q['centre_mm']for q in imported]);va=np.array([q['volume_mm3']for q in native]);vb=np.array([q['volume_mm3']for q in imported])
    costs=np.linalg.norm(ca[:,None,:]-cb[None,:,:],axis=2)+100*abs(va[:,None]-vb[None,:])/np.maximum(1,va[:,None])
    ii,jj=linear_sum_assignment(costs);matches=[]
    for i,j in zip(ii,jj):
        n=native[i];q=imported[j]
        matches.append(dict(name=n['name'],native_solid_index=n['index'],volume_difference_mm3=q['volume_mm3']-n['volume_mm3'],centroid_difference_mm=float(np.linalg.norm(ca[i]-cb[j])),maximum_bounds_difference_mm=float(np.max(np.abs(np.array(n['bounds_mm'])-q['bounds_mm'])))))
    report['per_solid_diagnostic']=dict(method='One-to-one minimum-cost match by volume and centroid; diagnostics supplement aggregate serialization gate.',max_absolute_volume_difference_mm3=max(abs(r['volume_difference_mm3'])for r in matches),max_centroid_difference_mm=max(r['centroid_difference_mm']for r in matches),max_bounds_difference_mm=max(r['maximum_bounds_difference_mm']for r in matches),matches=matches)
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report['per_solid_diagnostic'].items()if k!='matches'}),flush=True)
