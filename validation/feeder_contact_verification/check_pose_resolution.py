"""Check full-B-rep separation within1um for residual sampled intersections."""
from pathlib import Path
import csv,json
import FreeCAD as App
import Part
from mechanism import shapes,State
H=Path(__file__).resolve().parent;d=json.loads((H/'NATIVE_POSE_AUDIT.json').read_text());results=[]
def posed(sh,xyz,q):
    s=sh.copy();s.translate(-s.Solids[0].CenterOfMass);s.Placement=App.Placement(App.Vector(*xyz),App.Rotation(q[1],q[2],q[3],q[0])).multiply(s.Placement);return s
for c in d['cases']:
    checks=[r for r in c['checks'] if r['positive_pairs']]
    if not checks:continue
    rows=list(csv.DictReader((H/'campaign_mm'/(c['case_id']+'.csv')).open()));L=113.5 if c['size']=='1U' else 340.5
    for check in checks:
        r=min(rows,key=lambda r:abs(float(r['time_s'])-check['time_s']));parts,_=shapes(L,State(gate=120,bolt=0));p=posed(parts['payload'],[float(r[k])*1000 for k in ['payload_x_m','payload_y_m','payload_z_m']],[float(r[k]) for k in ['qw','qx','qy','qz']]);p.translate(App.Vector(0,.001,0))
        fxyz=[float(r[k])*1000 for k in ['fork_x_m','fork_y_m','fork_z_m']];q=[float(r[k]) for k in ['fork_qw','fork_qx','fork_qy','fork_qz']]
        fc=parts['fork_front'].Solids[0].CenterOfMass;oldfc=parts['fork_body'].Solids[0].CenterOfMass
        parts['fork_body']=posed(parts['fork_body'],fxyz,q);parts['fork_front']=posed(parts['fork_front'],[fc.x+fxyz[0]-oldfc.x,float(r['front_y_m'])*1000,float(r['front_z_m'])*1000],q)
        rc=parts['sled_entry_bar'].Solids[0].CenterOfMass;parts['sled_entry_bar']=posed(parts['sled_entry_bar'],[rc.x,rc.y,rc.z+float(r['receiver_close_m'])*1000],[1,0,0,0])
        for i in [0,1]:parts['receiver_lock_pin_'+str(i)].translate(App.Vector(-float(r[f'pin{i}_withdraw_m'])*1000,0,0))
        volumes={n:p.common(s).Volume for n,s in parts.items() if n!='payload'}
        assert max(volumes.values())<1e-8,volumes
        results.append({'case_id':c['case_id'],'time_s':check['time_s'],'delta_mm':[0,.001,0],'maximum_remaining_pair_volume_mm3':max(volumes.values()),'original_positive_pairs':check['positive_pairs']})
(H/'POSE_RESOLUTION.json').write_text(json.dumps({'checks':results,'scope':'Full actual geometry at residual sampled states; a1umYtranslation removes all checked positive pairs. Actual raw poses remain unchanged in the primary audit. This bounds these residual sampled contacts only; it is not a continuous clearance certificate or a tolerance margin.'},indent=2)+'\n');print('Verified',len(results),'residual poses within1um')
