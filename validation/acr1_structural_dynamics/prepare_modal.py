#!/usr/bin/env python3
"""New free-free chassis modal deck from the exact accepted mesh/deck."""
from pathlib import Path
import argparse,hashlib,json
import numpy as np
H=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--raw',type=Path,required=True);ap.add_argument('--modes',type=int,default=46);ap.add_argument('--hotspot-node',type=int,required=True);a=ap.parse_args()
source=a.raw/'verification/chassis_fea/d4b53d520c1bc0d3_h8'
meta=json.loads((source/'MESH.json').read_text());text=(source/'chassis.inp').read_text()
assert hashlib.sha256((source/'chassis.inp').read_bytes()).hexdigest()=='e62f404781d0ad7e43897daa2e98c3af21eabb639ecfd435ac51b0db1b8d9255'
model=text.split('*BOUNDARY')[0];assert '*DENSITY'not in model
model=model.replace('*SOLID SECTION','*DENSITY\n2.7e-9\n*SOLID SECTION')
watch=sorted(int(n)for n in meta['nodal_forces_N']);elements=[];active=False
for line in text.splitlines():
 if line.startswith('*ELEMENT'):active='C3D10'in line;continue
 if line.startswith('*'):active=False
 if active:elements.append([int(q)for q in line.split(',')if q.strip()])
coords={int(n):np.array(v)for n,v in meta['node_coordinates'].items()}
centres=np.array([np.mean([coords[n]for n in e[1:5]],axis=0)for e in elements]);selected=set()
for point in [[200,-90,0],[214,-90,0],[300,-90,0],[446,-90,0],[600,-90,0],[670,-90,0],[446,40,22],[446,40,-22],[280,40,22],[610,40,-22],[250,50,140],[546,50,140]]:
 for i in np.argsort(np.linalg.norm(centres-np.array(point),axis=1))[:3]:selected.add(elements[int(i)][0])
selected.update(e[0]for e in elements if a.hotspot_node in e[1:])
watch=sorted(set(watch)|{n for e in elements if e[0]in selected for n in e[1:]})
model+='*NSET,NSET=PATCH\n'+'\n'.join(','.join(str(n)for n in watch[i:i+16])for i in range(0,len(watch),16))+'\n'
ordered=sorted(selected)
model+='*ELSET,ELSET=MONITOR\n'+'\n'.join(','.join(str(n)for n in ordered[i:i+16])for i in range(0,len(ordered),16))+'\n'
model+='*STEP\n*FREQUENCY\n'+str(a.modes)+'\n*NODE PRINT,NSET=PATCH\nU\n*EL PRINT,ELSET=MONITOR\nS\n*END STEP\n'
out=H/'runs/free_free';out.mkdir(parents=True,exist_ok=True);(out/'modal.inp').write_text(model)
record={'configuration_id':'VOLLEY-G5-ACR1','study':'SD01 free-free actual bare-chassis modal screen','source_deck_sha256':hashlib.sha256((source/'chassis.inp').read_bytes()).hexdigest(),'source_mesh_sha256':hashlib.sha256((source/'MESH.json').read_bytes()).hexdigest(),'source_BREP_sha256':meta['input_BREP_sha256'],'native_nodes':meta['nodes'],'C3D10_elements':meta['C3D10_elements'],'density_tonne_mm3':2.7e-9,'E_MPa':70000,'nu':.33,'removed_constraints':meta['constraints'],'requested_modes_including_rigid':a.modes,'patch_node_count':len(watch),'patch_nodes':watch,'stress_monitor_elements':sorted(selected),'accepted_static_hotspot_node':a.hotspot_node,'monitor_refinement':'Includes every element incident to actual accepted global nodal static stress hotspot, plus original web/plate/keeper monitors.','constraint_boundary':'Free-free bare chassis. Accepted static 3-2-1 rigid-motion gauge removed. Full sled/pallet/payload/joint/host attachments excluded.','units':'N,mm,s,tonne,MPa','source_preservation':'Accepted source deck/mesh read only.'}
(H/'MODAL_INPUT.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({k:record[k]for k in ['native_nodes','C3D10_elements','requested_modes_including_rigid','patch_node_count','stress_monitor_elements']}))
