"""VOLLEY-G5-ACR1: integrated, parameter-controlled academic mechanical assembly.

FreeCAD Part geometry; original Gen5 and FM08 files are read-only references.
Units are millimetres. Geometric checks do not establish hardware qualification.
"""
from pathlib import Path
import argparse, hashlib, itertools, json, math, time
from functools import lru_cache
import FreeCAD as App
import Part

HERE = Path(__file__).resolve().parent
P = json.loads((HERE/'PARAMETERS.json').read_text())
OUT = HERE/'release'; OUT.mkdir(exist_ok=True)
V = App.Vector
L = P['launch']; M = P['magnetic']; S = P['storage']; C = P['cradle']
XA = L['home_aft_x'] + L['payload_aft_relative_x']; XF = XA + 340.5
RHO = P['materials_kg_m3']

def box(dx,dy,dz,x=0,y=0,z=0): return Part.makeBox(dx,dy,dz,V(x,y,z))
def cyl(r,h,x,y,z,axis=(0,0,1)): return Part.makeCylinder(r,h,V(x,y,z),V(*axis))
def join(items):
    items=list(items)
    if not items: return Part.Shape()
    return items[0].multiFuse(items[1:]).removeSplitter() if len(items)>1 else items[0]
def tube(dx,dy,h,t,x,y,z): return box(dx,dy,h,x,y,z).cut(box(dx-2*t,dy-2*t,h,x+t,y+t,z)).removeSplitter()
def translated(shape,x=0,y=0,z=0):
    s=shape.copy();s.translate(V(x,y,z));return s
def reflected(shape):
    a=App.Matrix();a.A22=-1
    s=shape.copy();s.transformShape(a);return s

def row(name,shape,material='aluminium',group='fixed',note='',assigned_mass=None):
    return dict(name=name,shape=shape,material=material,group=group,note=note,assigned_mass_kg=assigned_mass)

@lru_cache(maxsize=1)
def foundation():
    p=[]
    # A generic open mounting ladder. No provider or ESPA flange fit is claimed.
    rails=[tube(2250,30,40,3,0,y,-190) for y in [-620,590]]
    for x in [0,40,124,144,400,704.5,734.5,800,1200,1600,2000,2190,2210]: rails.append(box(20,1240,20,x,-620,-170))
    p.append(row('Host_mount_ladder',join(rails),note='Generic mounting datum Z=-150; provider load/interface approval separate'))
    return p

@lru_cache(maxsize=1)
def track():
    p=[]
    for side,zc in [(-1,0),(1,-40)]:
        y0=-146 if side<0 else 88
        beam=box(2250,22,60,0,y0,zc-40)
        # Actual open channel; it is not a solid longeron through the wheels.
        rr=[beam]
        for z0 in [zc+16,zc-24]:
            rr.append(box(2250,18,8,0,-126 if side<0 else 72,z0))
        p.append(row('Track_'+('minusY' if side<0 else 'plusY'),join(rr),'aluminium','track','Asymmetric guide datum; 1mm nominal wheel radial clearance'))
        for x in [40,400,800,1200,1600,2000,2190]:
            yy=-140 if side<0 else 92
            p.append(row(f'Track_support_{side}_{x}',tube(16,16,110+zc,3,x,yy,-150),'aluminium','track'))
    # Fixed stator support passes through the open +Y carrier side, between plates.
    supports=[]
    for x in range(240,1950,160):
        supports += [box(12,64,4,x,46,-11),box(12,12,29,x,98,-40)]
    fixed_support=join(supports)
    plus=next(q for q in p if q['name']=='Track_plusY')
    plus['shape']=join([plus['shape'],fixed_support])
    plus['note']+=';integral lateral stator support arms'
    return p

@lru_cache(maxsize=1)
def winding():
    """Three connected series paths:42mm2 active bars,21mm2 end-link necks."""
    import inspect
    key=hashlib.sha256(inspect.getsource(winding).encode()).hexdigest()[:20]
    cache=HERE/'.winding_cache'/key;cache.mkdir(parents=True,exist_ok=True)
    result=[]
    for phase,offset,zc in [('A',0,-3.5),('C',1,0),('B',2,3.5)]:
        indices=list(range(offset,216,3));pieces=[]
        for i in indices:pieces.append(box(7,90,6,230+8*i,-45,-3))
        for j,(i,k) in enumerate(zip(indices,indices[1:])):
            sign=(1 if j%2==0 else -1)*(-1 if phase=='C' else 1)
            conn=[]
            for n in [i,k]:
                x=230+8*n
                conn.append(box(7,10,6,x,45,-3))
                low=min(-3,zc-1.5);high=max(3,zc+1.5)
                conn.append(box(7,5,high-low,x,50,low))
                conn.append(box(7,16,3,x,55,zc-1.5))
            conn.append(box((k-i)*8+7,7,3,230+8*i,64,zc-1.5))
            if sign<0:conn=[reflected(q) for q in conn]
            pieces.extend(conn)
        print('FUSING_PHASE',phase,len(pieces),flush=True)
        stored=cache/('phase_'+phase+'.brep')
        if stored.exists():conductor=Part.read(str(stored))
        else:
            conductor=join(pieces);conductor.exportBrep(str(stored))
        print('PHASE_READY',phase,len(conductor.Solids),conductor.Volume,flush=True)
        record=row('Stator_phase_'+phase,conductor,'copper','stator',
                   '72 active7x6mm sections,71 flattened7x3mm Ulinks;21mm2 minimum interface/endlink section,0.5mm nominal interphase Zgap;Cseries initial direction reversed')
        record['collision_shapes']=pieces;result.append(record)
    # Stepped GFRP support boards keep the active face envelope at +/-5mm.
    for sign in [-1,1]:
        board=[box(1740,94,2,224,-47,3)]
        for y in [-78,47]:
            board += [box(1740,31,2,224,y,5),box(1740,2,4,224,-49 if y<0 else 47,3)]
        if sign<0:
            matrix=App.Matrix();matrix.A33=-1
            reflected_board=[]
            for q in board:
                s=q.copy();s.transformShape(matrix);reflected_board.append(s)
            board=reflected_board
        record=row('Stator_GFRP_board_'+str(sign),join(board),'insulator','stator_support','2mm active-face boards; stepped outer wings outsideabsY47')
        record['collision_shapes']=board;result.append(record)
    return result

@lru_cache(maxsize=32)
def sled(aft=200,caps_open=False,fore_open=False):
    p=[]; zf=L['payload_floor_z']; xa=aft+L['payload_aft_relative_x'];xf=xa+340.5
    fore_shift=max(0.,min(12.,12.*(aft-1445.)/50.))
    # The +Y side is open for the fixed stator load path. The thick -Y web joins both plates.
    top=L['carrier_top_plate_z'][1];bottom=L['carrier_bottom_plate_z'][0]
    body=[box(488,170,top-14,aft,-100,14),box(488,170,-14-bottom,aft,-100,bottom),box(488,20,top-bottom,aft,-100,bottom)]
    # Segmented raised seats leave two deliberate loading-tine windows.
    intervals=[(0,64),(124,220),(288,340.5)]
    for u,v in intervals:
        for y in [-50,42]:body.append(box(v-u,8,zf-top,xa+u,y,top))
    # Rear pushing load enters only designated rail-contact pads, above the stator.
    for y in [-56,50]:body.append(box(6,6,zf+108-top,xa-14,y,top))
    body.append(box(6,112,6,xa-14,-56,zf+102))
    for y in [-50,42]:
        for z in [zf+2,zf+92]:
            body += [box(12,14,6,xa-14,y-6 if y<0 else y,z),box(2,8,6,xa-2,y,z)]
    # Four outboard pillars support independently retracting upper capture caps.
    for u in [24,296.5]:
        for side in [-1,1]:
            y=60 if side>0 else -66
            body.append(box(20,6,zf+102-top,xa+u,y,top))
    # A declared reference-pin interface positively arrests the carrier at home.
    # The host must provide a retracting 6mm pin before launch; its installed
    # envelope is outside the carrier/track swept volume after retraction.
    body.append(box(12,20,12,aft+14,-100,30).cut(cyl(3.1,20,aft+20,-100,36,(0,1,0))))
    # Two front corner keepers retract laterally, without entering magnet or stator volumes.
    for side in [-1,1]:
        y=42 if side>0 else -50
        if fore_open:y+=side*12
        body.append(box(10,6,zf-top,xf+2,60 if side>0 else -66,top))
    from sled_latches import build as build_latches
    import sys
    latch_parts,latch_fixed,latch_bores=build_latches(sys.modules[__name__],xa,xf,zf,caps_open,fore_shift)
    p+=latch_parts;body+=latch_fixed
    for bore in latch_bores:body=[sh.cut(bore) if sh.BoundBox.intersect(bore.BoundBox) else sh for sh in body]
    # Wheel shafts are part of the actual structural load path; +Y is below the stator throat.
    for rel in [119,369]:
        for side,zc in [(-1,0),(1,-40)]:
            if side<0:body.append(box(12,16,14,aft+rel-6,-106,-14))
            else:body.append(box(12,12,14,aft+rel-6,58,-40))
            shaft=cyl(4,34,aft+rel,54 if side>0 else -124,zc,(0,1,0))
            p.append(row(f'Sled_axle_{rel}_{side}',shaft,'steel','sled'))
            wheel=cyl(15,16,aft+rel,70 if side>0 else -122,zc,(0,1,0)).cut(cyl(4.1,16,aft+rel,70 if side>0 else -122,zc,(0,1,0))).removeSplitter()
            p.append(row(f'Sled_wheel_{rel}_{side}',wheel,'steel','sled','8.2mm geometric bore; bearing realization separate'))
    for rel in [119,369]:
        for side,zc in [(-1,0),(1,-40)]:
            bore=cyl(4.1,38,aft+rel,52 if side>0 else -126,zc,(0,1,0))
            body=[sh.cut(bore) if sh.BoundBox.intersect(bore.BoundBox) else sh for sh in body]
    chassis=row('Sled_connected_chassis',join(body),'aluminium','sled','16mm open-C plates and20mmnegativeweb;actual axle bores;home lock6mm reference-pin interface at aft+20,Y-100..-80,Z36;host retracting pin required')
    chassis['collision_shapes']=body;p.append(chassis)
    for side in [-1,1]:
        for i in range(42):
            z=6 if side>0 else -14
            q=row(f'Magnet_{side}_{i:02d}',box(8,90,8,aft+76+8*i,-45,z),'ndfeb','sled_magnet','42 discrete 8mm blocks; 336mm active length; 2mm mounting-end margins')
            q['magnetization_angle_deg']=(90-i*60 if side>0 else 90+i*60)%360
            q['magnetization_axes']='angle in travel-X / gap-Z plane;inward-enhanced mirrored Halbach faces'
            p.append(q)
    return p

def payload(name,xa,cy,zf,group='payload'):
    return row(name,box(340.5,100,100,xa,cy-50,zf),'payload',group,
               'Public 3U envelope, 4kg assigned mass; actual payload/provider approval separate',4.0)

@lru_cache(maxsize=256)
def cell(side,level,advance=0,gate_open=False,omit_payload=False):
    fz=S['first_payload_floor_z']+level*S['level_pitch_z'];rear=-300+advance;p=[];fixed=[]
    def add(n,sh,mat='aluminium',group='cell_fixed',note='',mass=None):p.append(row(n,sh,mat,group,note,mass))
    # Mid-height side rails leave deliberate lower/upper pusher-arm slots.
    fixed.append(box(488.5,245,8,XA-74,-345,fz-8))
    for x in [XA-48,XA-20,XF+20]:fixed.append(box(28,112,8,x-14,-450,fz-8))
    fixed.append(box(28,157,8,XA-62,-495,fz-8))
    fixed.append(box(28,16,8,XA-62,-116,fz-8))
    for x in [XA-6,XF+2]:
        fixed += [box(4,230,74,x,-330,fz+14),box(14,230,6,x if x<XA else x-10,-330,fz+102),box(14,8,108,x if x<XA else x-10,-330,fz-0)]
    # Four storage keeper rods open outward in X, so they do not enter adjacent levels.
    for end in [-1,1]:
        gx=XA-70 if end<0 else XF+70
        fixed.append(box(16,12,110,gx-8,-202,fz-2))
        for dz in [5,95]:
            shift=end*40 if gate_open else 0
            if end<0:
                rod=cyl(2,84,XA-74+shift,-196,fz+dz,(1,0,0));finger=box(8,4,6,XA+2+shift,-198,fz+dz-3)
            else:
                rod=cyl(2,84,XF-10+shift,-196,fz+dz,(1,0,0));finger=box(8,4,6,XF-10+shift,-198,fz+dz-3)
            # Shaft guide bore is a designed assembly interface, not an intersecting proxy.
            fixed[-1]=fixed[-1].cut(cyl(2.1,18,gx-9,-196,fz+dz,(1,0,0)))
            add(f'Storage_keeper_{end}_{dz}',join([rod,finger]),'steel','cell_gate','40mm outward translation; normally locked actuation requirement')
    gz=fz+50
    # Side-mounted guides keep the complete pusher inside its own 100mm payload level.
    for x in [XA-20,XF+20]:
        add(f'Guide_shaft_{x}',cyl(5,330,x,-435,gz,(0,1,0)),'steel')
        for y in [-440,-110]:
            block=box(22,10,24,x-11,y,gz-12).cut(cyl(5.1,10,x,y,gz,(0,1,0)))
            fixed += [block,box(22,10,38,x-11,y,fz)]
        bush=cyl(8,30,x,rear-91,gz,(0,1,0)).cut(cyl(5.1,30,x,rear-91,gz,(0,1,0)))
        add(f'Guide_bush_{x}',bush,'polymer','cell_pusher')
    sx=XA-48
    screw=join([cyl(5,315,sx,-435,gz,(0,1,0)),cyl(4,20,sx,-455,gz,(0,1,0)),cyl(4,20,sx,-120,gz,(0,1,0))])
    add('Lead_screw_10x2',screw,'steel','cell_drive','Nominal shaft and journals; thread detail idealized')
    for y in [-445,-115]:
        bearing=cyl(11,8,sx,y,gz,(0,1,0)).cut(cyl(4.1,8,sx,y,gz,(0,1,0)))
        add('Screw_bearing_'+str(y),bearing,'steel')
        holder=box(28,12,30,sx-14,y-2,gz-15).cut(cyl(11.1,12,sx,y-2,gz,(0,1,0)))
        fixed += [holder,box(28,12,35,sx-14,y-2,fz)]
    nut=cyl(9.55,19.1,sx,rear-90,gz,(0,1,0)).cut(cyl(5.1,19.1,sx,rear-90,gz,(0,1,0)))
    add('Lead_nut_SB3700',nut,'polymer','cell_pusher')
    frame=box(380.5,4,96,XA-20,rear-18,fz+2).cut(box(356.5,6,80,XA-8,rear-19,fz+10))
    # Nut holder and its strap form a connected frame, with real bore clearances.
    holder=box(28,22,28,sx-14,rear-92,gz-14).cut(cyl(9.65,22,sx,rear-92,gz,(0,1,0)))
    arms=[]
    for x in [XA-20,XF+20]:
        arm=cyl(12,30,x,rear-91,gz,(0,1,0)).cut(cyl(8.1,30,x,rear-91,gz,(0,1,0)))
        outward=-1 if x<XA else 1
        bx=x-13.5 if outward<0 else x+13
        backx=x-13.5 if outward<0 else x+8
        frontx=x-13.5 if outward<0 else x-12
        arms += [arm,box(2 if outward<0 else 8,69,10,bx,rear-83,gz-5),
                 box(5.5 if outward<0 else 13,8,10,backx,rear-89,gz-5),
                 box(25.5 if outward<0 else 33,4,12,frontx,rear-18,gz-6)]
    frame=join([frame,holder,box(22,6,12,sx+14,rear-82,gz-6)]+arms)
    for x in [XA-20,XF+20]:
        frame=frame.cut(cyl(5.1,90,x,rear-92,gz,(0,1,0)))
        frame=frame.cut(cyl(8.1,30,x,rear-91,gz,(0,1,0)))
    for x in [XA,XF-8]:
        for z in [fz+2,fz+92]:frame=frame.fuse(box(8,14,6,x,rear-14,z))
    add('Pusher_frame',frame.removeSplitter(),'aluminium','cell_pusher','Guided push-only frame with corner-zone pads; no gravity feed')
    add('Brake_BXW01_reference',cyl(20,35,sx,-495,gz,(0,1,0)),'catalog','cell_catalog','0.12Nm source-backed brake envelope; adapter/space rating separate',.2)
    add('Motor_3242_gear9_reference',cyl(16,78.9,sx,-573.9,gz,(0,1,0)),'catalog','cell_catalog','3242BX4+32GPT9:1 envelope; sizing rerun for new stroke',.42)
    add('Drive_coupler',cyl(4,5,sx,-460,gz,(0,1,0)),'steel','cell_drive')
    mount=join([cyl(25,12,sx,-478,gz,(0,1,0)),box(50,12,35,sx-25,-478,fz)])
    mount=mount.cut(cyl(20.2,12,sx,-478,gz,(0,1,0)))
    fixed.append(mount)
    # The frame is a genuine fabrication; subtract the long keeper-guide bores first.
    add('Fixed_channel_frame',join(fixed),'aluminium','cell_fixed','Manufactured pusher-arm windows and separate longitudinal retention rails')
    if not omit_payload:p.append(payload('Stored_3U',XA,-250+advance,fz))
    prefix=f'Bank_{"south" if side<0 else "north"}_L{level}_'
    for q in p:
        if side>0:q['shape']=reflected(q['shape'])
        q['name']=prefix+q['name']
    return p

@lru_cache(maxsize=1)
def bank_mounts():
    pp=[]
    for side in [-1,1]:
        ss=[]
        for x in [XA-110,XF+110]:
            ss.append(tube(24,24,1120,3,x-12,side*360-12,-150))
        for level in range(6):
            z=180+130*level-16
            ss.append(box(584.5,24,8,XA-122,side*350-12,z))
        pp.append(row('Bank_mount_'+str(side),join(ss),'aluminium','bank_mount'))
    return pp

def cradle(floor=46,keepers_open=False,fork_withdraw=0,incoming_side=None):
    from cradle_acr1 import build
    import sys
    return build(sys.modules[__name__],floor,keepers_open,fork_withdraw,incoming_side)


def brake():
    """No auxiliary brake installed; arrest and return use the same LSM.

    Experimental unexcited pole/fin geometry is preserved only in
    archived_auxiliary_brake/build_acr1_experimental_brake.py.
    """
    return []

@lru_cache(maxsize=1)
def release_cams():
    pp=[]
    # 12/50 ramp; a 0.1mm nominal roller/track running clearance is modeled.
    points=[(1844.5,99.9),(1854.5,99.9),(1904.5,111.9),(2130,111.9),
            (2130,115.9),(1904.5,115.9),(1854.5,103.9),(1844.5,103.9)]
    wire=Part.makePolygon([V(x,y,56)for x,y in points]+[V(*points[0],56)])
    cam=Part.Face(wire).extrude(V(0,0,4))
    mounting=[cam,box(12,116,4,2000,110,52),box(12,6,202,2000,220,-150)]
    for side in [-1,1]:
        sh=join(mounting)
        if side<0:sh=reflected(sh)
        pp.append(row('Forekeeper_fixed_cam_'+str(side),sh,'steel','release_cam',
            '12mm spring keeper opening over aft1445..1495;5mm pre-release margin;holds open through aft1710 arrest;0.1mm nominal roller running clearance'))
    return pp

def assemble(state='home',cell_side=-1,level=5,feed=0,launch_x=None):
    # State sequence: stored -> feed -> captured -> lower -> handoff -> clear -> shot.
    source_floor=180+130*level
    z0=L['payload_floor_z']
    phase={'home':(190,True,0), 'feed':(source_floor,False,0), 'captured':(source_floor,False,0),
           'lower':(z0,False,0), 'handoff':(z0-3,True,0), 'withdrawn':(z0-3,True,150),
           'rise':(158,True,150),'reextend':(158,True,0),'clear':(190,True,0),
           'release':(190,True,0), 'arrest':(190,True,0)}
    floor,jaw_open,withdraw=phase[state]
    active=state!='home'
    pp=foundation()+track()+winding()+bank_mounts()+brake()+release_cams()
    for side in [-1,1]:
        for lev in range(6):
            selected=active and side==cell_side and lev==level
            adv=feed if selected and state=='feed' else (250 if selected and state=='captured' else 0)
            pp+=cell(side,lev,adv,selected and state in ['feed','captured'],selected and state not in ['feed'])
    aft=launch_x if launch_x is not None else (1500 if state=='release' else 1710 if state=='arrest' else 200)
    pp+=sled(aft,caps_open=state in ['home','feed','captured','lower'],fore_open=state in ['release','arrest'])
    pp+=cradle(floor,jaw_open,withdraw,cell_side if state=='feed' else None)
    if state in ['captured','lower','handoff','withdrawn','rise','reextend','clear','release']:
        payload_aft=XA if state not in ['release'] else XA+1300
        pp.append(payload('Transferred_3U',payload_aft,0,floor if state=='captured' else z0))
    return pp

def audit(items,changed_names=None):
    hits=[];tested=0;prepared={}
    for q in items:
        shapes=[]
        for sh in q.get('collision_shapes',[q['shape']]):
            bb=sh.BoundBox;bounds=(bb.XMin,bb.XMax,bb.YMin,bb.YMax,bb.ZMin,bb.ZMax)
            cuboid=abs(sh.Volume-bb.XLength*bb.YLength*bb.ZLength)<1e-6
            shapes.append((sh,bounds,cuboid))
        prepared[q['name']]=shapes
    for a,b in itertools.combinations(items,2):
        if changed_names is not None and a['name'] not in changed_names and b['name'] not in changed_names:continue
        if not a['shape'].BoundBox.intersect(b['shape'].BoundBox):continue
        tested+=1;vol=0
        for sa,ba,ca in prepared[a['name']]:
            for sb,bb,cb in prepared[b['name']]:
                overlap=[min(ba[1],bb[1])-max(ba[0],bb[0]),min(ba[3],bb[3])-max(ba[2],bb[2]),min(ba[5],bb[5])-max(ba[4],bb[4])]
                if min(overlap)<=1e-8:continue
                if ca and cb:
                    vol+=math.prod(overlap)
                else:vol+=sa.common(sb).Volume
        if vol>1e-5:
            hit=dict(a=a['name'],b=b['name'],volume_mm3=vol);hits.append(hit)
            print('INTERFERENCE',json.dumps(hit),flush=True)
    return dict(pass_all=not hits,tested_pairs=tested,interferences=hits)

def export(items,state):
    doc=App.newDocument('VOLLEY_G5_ACR1_'+state);bom=[]
    colors={'aluminium':(.68,.71,.74),'steel':(.35,.38,.42),'copper':(.77,.42,.2),'ndfeb':(.21,.24,.29),'payload':(.16,.29,.47),'catalog':(.28,.31,.34)}
    for q in items:
        ob=doc.addObject('Part::Feature',q['name']);ob.Label=q['name'];ob.Shape=q['shape']
        for k,val in [('Material',q['material']),('Subsystem',q['group']),('EvidenceNote',q['note'])]:ob.addProperty('App::PropertyString',k);setattr(ob,k,val)
        rho=RHO.get(q['material'],0);mass=q['assigned_mass_kg'] if q['assigned_mass_kg'] is not None else q['shape'].Volume*rho*1e-9
        ob.addProperty('App::PropertyFloat','Density_kg_m3');ob.Density_kg_m3=rho
        ob.addProperty('App::PropertyFloat','AssignedMass_kg');ob.AssignedMass_kg=mass
        if getattr(ob,'ViewObject',None) is not None:ob.ViewObject.ShapeColor=colors.get(q['material'],(.5,.5,.5))
        ss=q['shape'].Solids;volume=sum(s.Volume for s in ss)
        cg=sum((s.CenterOfMass*s.Volume for s in ss),V())/volume if volume else V()
        bom.append(dict(name=q['name'],material=q['material'],subsystem=q['group'],solids=len(ss),volume_mm3=volume,mass_kg=mass,CG_mm=[cg.x,cg.y,cg.z],note=q['note']))
    doc.recompute();stem='VOLLEY_G5_ACR1_'+state
    doc.saveAs(str(OUT/(stem+'.FCStd')))
    Part.export(doc.Objects,str(OUT/(stem+'.step')))
    data={'configuration_id':P['configuration_id'],'state':state,'builder_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'parameters_sha256':hashlib.sha256((HERE/'PARAMETERS.json').read_bytes()).hexdigest(),'parts':len(items),'solids':sum(len(q['shape'].Solids) for q in items),'BOM':bom,'scope':'Nominal academic assembly; no loaded or provider qualification'}
    App.closeDocument(doc.Name);return data

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--state',default='home');parser.add_argument('--level',type=int,default=5);parser.add_argument('--side',type=int,default=-1);parser.add_argument('--feed',type=float,default=0);parser.add_argument('--audit',action='store_true');parser.add_argument('--no-export',action='store_true');a=parser.parse_args()
    t=time.perf_counter();pp=assemble(a.state,a.side,a.level,a.feed);print('ASSEMBLED',a.state,len(pp),flush=True)
    data=export(pp,a.state) if not a.no_export else {'state':a.state,'parts':len(pp)}
    if a.audit:data['audit']=audit(pp);print('AUDIT',len(data['audit']['interferences']),flush=True)
    data['elapsed_s']=time.perf_counter()-t
    (OUT/('VOLLEY_G5_ACR1_'+a.state+'.json')).write_text(json.dumps(data,indent=2)+'\n')
    print('COMPLETE',data['elapsed_s'],flush=True)
if __name__=='__main__':main()
