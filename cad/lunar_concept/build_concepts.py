"""Parametric packaging concepts, not released parts. Adityavardhan Mishra."""
from pathlib import Path
import json,hashlib
import cadquery as cq
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'cad/lunar_concept'; ASSET=ROOT/'docs/assets/lunar'
COLORS={'structure':'#bcc5c8','payload':'#df9b41','release':'#18b39a','charger':'#bd7396','services':'#477db4','keepout':'#cf6256'}

def box(size,center):return cq.Workplane('XY').box(*size).translate(center).val()
def cylx(radius,length,center):return cq.Workplane('YZ').circle(radius).extrude(length).translate((center[0]-length/2,center[1],center[2])).val()
def part(name,shape,role):return dict(name=name,shape=shape,role=role)
def cell(offset=(0,0,0),prefix='cell'):
    p=[]
    def add(name,shape,role):p.append(part(prefix+'_'+name,shape.translate(offset),role))
    add('mounting_deck',box((660,200,10),(120,0,-85)),'structure')
    for y in [-70,70]:
        add('frame_'+str(y),box((620,8,145),(120,y,-7.5)),'structure')
        add('guide_'+str(y),cylx(4,300,(-25,y,0)),'release')
    add('rear_spring_seat',box((10,120,110),(-180,0,0)),'release')
    add('pusher_charged',box((8,110,110),(-4,0,0)),'release')
    add('payload_proxy',box((340.5,100,100),(170.25,0,0)),'payload')
    # Cylindrical accumulator envelopes are deliberately not physical spring coils.
    for y in [-35,35]:add('spring_envelope_'+str(y),cylx(12,164,(-92,y,0)),'release')
    add('charger_motor_envelope',box((55,38,42),(-165,112,-30)),'charger')
    add('charger_screw_envelope',cylx(4,170,(-75,112,-30)),'charger')
    add('withdrawn_coupling',box((20,18,24),(-15,99,-30)),'charger')
    add('latch_envelope',box((20,22,24),(-14,-100,0)),'charger')
    for y in [-62,62]:add('catcher_envelope_'+str(y),box((20,12,30),(90,y,0)),'release')
    add('sensor_harness_zone',box((75,20,25),(30,105,-58)),'services')
    return p

def bank():
    p=[]
    for j,y in enumerate([-120,120]):
        for k,z in enumerate([-120,120]):p+=cell((0,y,z),f'cell_{j}_{k}')
    p.append(part('bank_interface',box((18,460,460),(-220,0,0)),'structure'))
    return p

def carrier():
    p=bank()
    p += [part('carrier_bus_placeholder',box((420,540,540),(-460,0,0)),'services'),part('tank_envelope',cylx(155,350,(-460,0,0)),'keepout')]
    # Outer bus and enclosed tank intentionally overlap as system envelopes.
    for y in [-690,690]:
        p.append(part('solar_wing_'+str(y),box((380,720,12),(-450,y,0)),'services'))
        for stripe in range(6):p.append(part(f'panel_grid_{y}_{stripe}',box((3,720,2),(-610+stripe*64,y,7)),'structure'))
    p += [part('engine_envelope',cylx(75,130,(-735,0,0)),'keepout'),part('radiator_envelope',box((360,8,250),(-460,278,0)),'structure'),part('antenna_envelope',cylx(65,18,(-390,0,330)),'services')]
    return p

def pallet():
    p=[part('payload_berth_proxy',box((800,650,650),(420,0,0)),'payload'),part('pallet',box((24,760,760),(-12,0,0)),'structure')]
    for y in [-290,290]:
        for z in [-290,290]:
            p += [part(f'push_point_{y}_{z}',cylx(30,80,(-65,y,z)),'release'),part(f'ascent_restraint_{y}_{z}',box((120,32,32),(35,y*1.18,z*1.18)),'charger')]
    return p

def mesh(p,explode=False):
    out=[]
    for i,c in enumerate(p):
        shape=c['shape']; shift=np.array([0.,0.,0.])
        if explode and c['role']=='payload':shift[0]=220
        if explode and c['role']=='charger':shift[1]=100
        if explode and 'spring' in c['name']:shift[2]=120
        vs,ts=shape.tessellate(1.,.25)
        vertices=np.array([[v.x,v.y,v.z] for v in vs])+shift
        out.append(dict(name=c['name'],role=c['role'],color=COLORS[c['role']],vertices=vertices.round(5).tolist(),triangles=[list(t) for t in ts]))
    return out

def render(data,name,caption):
    from matplotlib.colors import to_rgb
    yaw=np.radians(35);tilt=np.radians(24)
    transform=np.array([[np.cos(yaw),-np.sin(yaw),0],[-np.sin(yaw)*np.sin(tilt),-np.cos(yaw)*np.sin(tilt),np.cos(tilt)],[np.sin(yaw)*np.cos(tilt),np.cos(yaw)*np.cos(tilt),np.sin(tilt)]])
    parts=[(c,np.array(c['vertices'])@transform.T) for c in data]
    allv=np.vstack([v for c,v in parts]);lo=allv.min(axis=0);hi=allv.max(axis=0)
    width,height=1760,800;scale=min((width-60)/(hi[0]-lo[0]),(height-60)/(hi[1]-lo[1]))
    rgb=np.empty((height,width,3));rgb[:]=to_rgb('#101e2b');depth=np.full((height,width),-np.inf)
    for c,v in parts:
        screen=v.copy();screen[:,0]=(v[:,0]-(hi[0]+lo[0])/2)*scale+width/2;screen[:,1]=height/2-(v[:,1]-(hi[1]+lo[1])/2)*scale
        for ids in c['triangles']:
            t=screen[ids];normal=np.cross(v[ids[1]]-v[ids[0]],v[ids[2]]-v[ids[0]]);length=np.linalg.norm(normal)
            shade=.65+.35*abs(np.dot(normal/max(length,1e-12),np.array([.25,.65,.72])))
            x0=max(0,int(np.floor(t[:,0].min())));x1=min(width-1,int(np.ceil(t[:,0].max())))
            y0=max(0,int(np.floor(t[:,1].min())));y1=min(height-1,int(np.ceil(t[:,1].max())))
            den=(t[1,1]-t[2,1])*(t[0,0]-t[2,0])+(t[2,0]-t[1,0])*(t[0,1]-t[2,1])
            if abs(den)<1e-10 or x1<x0 or y1<y0:continue
            yy,xx=np.mgrid[y0:y1+1,x0:x1+1];xx=xx+.5;yy=yy+.5
            a=((t[1,1]-t[2,1])*(xx-t[2,0])+(t[2,0]-t[1,0])*(yy-t[2,1]))/den
            b=((t[2,1]-t[0,1])*(xx-t[2,0])+(t[0,0]-t[2,0])*(yy-t[2,1]))/den;cc=1-a-b
            z=a*t[0,2]+b*t[1,2]+cc*t[2,2];target=depth[y0:y1+1,x0:x1+1]
            mask=(a>=-1e-8)&(b>=-1e-8)&(cc>=-1e-8)&(z>target)
            target[mask]=z[mask];rgb[y0:y1+1,x0:x1+1][mask]=np.clip(np.array(to_rgb(c['color']))*shade,0,1)
    fig=plt.figure(figsize=(12,7),facecolor='#101e2b');ax=fig.add_axes([.04,.11,.92,.71]);ax.imshow(rgb);ax.axis('off')
    fig.text(.045,.92,caption,color='white',fontsize=21,weight='bold');fig.text(.045,.865,'PARAMETRIC CONCEPT  /  placeholder components  /  no hardware validation',color='#a5bac7',fontsize=10)
    fig.text(.045,.06,'Amber: payload    Teal: release path    Pink: charger/latch    Blue: carrier services',color='#c1d0d8',fontsize=10)
    fig.savefig(ASSET/(name+'.png'),dpi=160,facecolor=fig.get_facecolor());plt.close(fig)

def run():
    OUT.mkdir(exist_ok=True);ASSET.mkdir(parents=True,exist_ok=True)
    models={'mechanical_cell':cell(),'four_cell_bank':bank(),'lunar_carrier':carrier(),'large_payload_pallet':pallet()};checks=[];ledger=[];web={}
    for name,parts in models.items():
        assembly=cq.Assembly(name=name)
        for c in parts:assembly.add(c['shape'],name=c['name'],color=cq.Color(*[int(COLORS[c['role']][i:i+2],16)/255 for i in (1,3,5)]))
        assembly.save(str(OUT/(name+'.step')))
        compound=cq.Compound.makeCompound([p['shape'] for p in parts]);original=compound.BoundingBox()
        cq.exporters.export(compound,str(OUT/(name+'.stl')),tolerance=.8,angularTolerance=.25)
        imported=cq.importers.importStep(str(OUT/(name+'.step'))).val().BoundingBox()
        residual=max(abs(getattr(original,k)-getattr(imported,k)) for k in ['xlen','ylen','zlen'])
        valid=all(c['shape'].isValid() and c['shape'].Volume()>0 for c in parts)
        checks.append(dict(model=name,valid=valid,step_bbox_residual_mm=residual,pass_checks=valid and residual<=1e-4))
        for c in parts:ledger.append(dict(model=name,component=c['name'],role=c['role'],status='concept envelope; component selection and manufacturing dimensions unverified'))
        data=mesh(parts);web[name]=data;render(data,name,name.replace('_',' ').title())
    web['exploded_cell']=mesh(models['mechanical_cell'],True);render(web['exploded_cell'],'exploded_cell','Mechanical cell / exploded concept')
    (ASSET/'concept_meshes.js').write_text('window.VOLLEY_MODELS='+json.dumps(web,separators=(',',':'))+';\n')
    record=dict(units='mm',departure_axis='+X',model_scope='Packaging envelopes only; not mass, interference, structural or manufacturability closure',source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),checks=checks,components=ledger)
    (OUT/'manifest.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(checks,indent=2))
    if not all(c['pass_checks'] for c in checks):raise SystemExit('CAD artifact failure')
if __name__=='__main__':run()
