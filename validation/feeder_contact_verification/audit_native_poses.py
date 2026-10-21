"""Independent full-B-rep checks of selected native FCE12 contact poses.

All original material is retained in this audit, including geometry excluded
from the numerical collision domain. Checks are discrete, not continuous proof.
"""
from pathlib import Path
import argparse,csv,hashlib,json,time
import FreeCAD as App
import Part
from mechanism import shapes, State
H=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--campaign',default='campaign_mm');p.add_argument('--follow',action='store_true');a=p.parse_args();C=H/a.campaign

def posed(shape,xyz,q):
    result=shape.copy();result.translate(-result.Solids[0].CenterOfMass)
    result.Placement=App.Placement(App.Vector(*xyz),App.Rotation(q[1],q[2],q[3],q[0])).multiply(result.Placement)
    return result

def near(a,b):
    return all(getattr(a,k+'Max')>=getattr(b,k+'Min')-1e-6 and getattr(b,k+'Max')>=getattr(a,k+'Min')-1e-6 for k in ['X','Y','Z'])

done=set();results=[]
out=H/'NATIVE_POSE_AUDIT.json'
while True:
    for rec in sorted(C.glob('*.record.json')):
        d=json.loads(rec.read_text());name=d['case_id']
        if name in done or d['label'] not in ['time_refinement','iteration_refinement']:continue
        L=113.5 if d['size']=='1U' else 340.5
        parts,_=shapes(L,State(gate=120,bolt=0));rows=list(csv.DictReader((C/(name+'.csv')).open()));checks=[]
        for t in [0,2,4,6,8,10,11,12,12.5,14.5,20,26.5]:
            r=min(rows,key=lambda v:abs(float(v['time_s'])-t))
            if abs(float(r['time_s'])-t)>.011:continue
            q=[float(r[k]) for k in ['qw','qx','qy','qz']]
            payload=posed(parts['payload'],[float(r[k])*1000 for k in ['payload_x_m','payload_y_m','payload_z_m']],q)
            fxyz=[float(r[k])*1000 for k in ['fork_x_m','fork_y_m','fork_z_m']];fq=[float(r[k]) for k in ['fork_qw','fork_qx','fork_qy','fork_qz']]
            current=dict(parts)
            current['fork_body']=posed(parts['fork_body'],fxyz,fq)
            fc=parts['fork_front'].Solids[0].CenterOfMass
            current['fork_front']=posed(parts['fork_front'],[fc.x+fxyz[0]-parts['fork_body'].Solids[0].CenterOfMass.x,float(r['front_y_m'])*1000,float(r['front_z_m'])*1000],fq)
            rc=parts['sled_entry_bar'].Solids[0].CenterOfMass
            current['sled_entry_bar']=posed(parts['sled_entry_bar'],[rc.x,rc.y,rc.z+float(r['receiver_close_m'])*1000],[1,0,0,0])
            for i in [0,1]:
                n='receiver_lock_pin_'+str(i);b=parts[n].copy();b.translate(App.Vector(-float(r[f'pin{i}_withdraw_m'])*1000,0,0));current[n]=b
            pairs=[]
            for n,sh in current.items():
                if n=='payload' or not near(payload.BoundBox,sh.BoundBox):continue
                common=payload.common(sh);volume=common.Volume
                if volume>1e-8:
                    bb=common.BoundBox
                    pairs.append({'component':n,'intersection_mm3':volume,'intersection_bounds_mm':[bb.XMin,bb.YMin,bb.ZMin,bb.XMax,bb.YMax,bb.ZMax]})
            checks.append({'time_s':float(r['time_s']),'positive_pairs':pairs,'total_intersection_mm3':sum(x['intersection_mm3'] for x in pairs)})
            print(name,t,'overlap',checks[-1]['total_intersection_mm3'],flush=True)
        done.add(name);results.append({'case_id':name,'size':d['size'],'dt_s':d['dt_s'],'source_csv_sha256':hashlib.sha256((C/(name+'.csv')).read_bytes()).hexdigest(),'checks':checks})
        out.write_text(json.dumps({'cases':results,'scope':'Twelve targeted times per completed nominal/refinement trace, original full native solids. Ideal-joint orientation/position reconstruction for auxiliary bodies is declared. Discrete evidence; not continuous nonpenetration or hardware tolerance acceptance.'},indent=2)+'\n')
    if not a.follow or (C/'RUNS.json').exists():break
    time.sleep(2)
