"""FM08-R3: selected academic guided lead-screw feeder and common receiver.
Dimensions mm. Run PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3 build_selected.py
Nominal kinematic geometry, not manufacturing or flight qualification.
"""
from pathlib import Path
import FreeCAD as App, Part
import json,math,itertools,hashlib,csv,time,sys
H=Path(__file__).resolve().parent; O=H/'release';O.mkdir(exist_ok=True)
V=App.Vector
RHO={'aluminium':2.7e-6,'steel':7.85e-6,'polymer':1.41e-6,'payload':0.,'catalog_envelope':0.}
REV='FM08-R3'
CELL_CACHE={}
def box(d,p):return Part.makeBox(*d,V(*p))
def cyl(r,l,p,a=(0,1,0)):return Part.makeCylinder(r,l,V(*p),V(*a))
def union(ss):return ss[0].multiFuse(ss[1:]).removeSplitter() if len(ss)>1 else ss[0]
def row(n,s,m='aluminium',r='fixed',notes=''):
 assert s.isValid() and s.Volume>0,(n,s.isValid(),s.Volume)
 return {'name':n,'shape':s,'material':m,'role':r,'notes':notes}
def cell(fmt='3U',u=0,gate_open=False,front_open=False,side='south',offset=0):
 """Local payloadX datum maintained when north cells reflect acrossY50."""
 key=(fmt,u,gate_open,front_open,side,offset)
 if key in CELL_CACHE:return [{**q,'shape':q['shape'].copy()} for q in CELL_CACHE[key]]
 h=60 if side=='north' else 0; gx=160+h; rear=-200+u
 x0=227 if fmt=='1U' else 0; L=113.5 if fmt=='1U' else 340.5
 p=[]
 def add(*a,**k):p.append(row(*a,**k))
 add('Payload_'+fmt,box((L,100,100),(x0,rear,22)),'payload','payload','Public envelope surrogate;1U1.33kg/3U4kg nominal;6kg upper study')
 add('Cassette_floor',box((356.5,110,6),(-8,-210,14)))
 add('Transfer_bridge',box((356.5,90,6),(-8,-100,14)))
 for xx in [x0,332.5]:
  add('Corner_floor_rail_'+str(xx),box((8,198,2),(xx,-208,20)))
 for xx in [-6,342.5]:
  ss=[box((4,200,108),(xx,-208,20)),box((12,200,4),(xx if xx<0 else xx-8,-208,124))]
  add('Cassette_side_cap_'+str(xx),union(ss))
 add('Cassette_rear',box((356.5,4,108),(-8,-212,20)))
 if fmt=='1U':
  # This insert stays bolted to the cassette/bridge. No spacer is launched.
  ss=[box((2,198,108),(223,-208,20)),box((10,198,4),(223,-208,124))]
  add('Captive_fixed_1U_insert',union(ss),'aluminium','fixed_insert','Bolted fixed dimensional insert; never transfers or releases')
 # Retractable storage gate: bottom22closed,142open. 2mm payload-facing gap.
 sz=-104 if gate_open else 22
 add('Storage_gate',box((L+4,3,100),(x0-2,-80,sz)),'aluminium','gate','Vertical126mm downward travel through dedicated bridge slot, interlocked with receiver and fork position')
 # Twin guide shafts and overhead front support keep all static hardware above launch corridor.
 for xx in [-20,360]:
  add('Guide_shaft_'+str(xx),cyl(4,330,(xx,-250,gx)),'steel','fixed')
  for yy in [-250,70]:
   ss=[box((24,10,28),(xx-12,yy,gx-14))]
   sh=ss[0].cut(cyl(4,10,(xx,yy,gx))).removeSplitter()
   add('Guide_support_'+str(xx)+'_'+str(yy),sh,'aluminium','fixed','Nominal shaft support bore; fasteners and fits shown separately')
  # 0.10mm diametral running gap, not a precision/reliability claim.
  bush=cyl(8,30,(xx,rear-15,gx)).cut(cyl(4.05,30,(xx,rear-15,gx))).removeSplitter()
  add('Guide_bush_'+str(xx),bush,'polymer','moving','8.1mm bore;16mmOD;30mm length; plain-bush material assumption')
 for xx in [-20,360]:
  for yy in [-225,20]:add('Guide_hardstop_'+str(xx)+'_'+str(yy),cyl(7,5,(xx,yy,gx)).cut(cyl(4,5,(xx,yy,gx))).removeSplitter(),'steel','fixed','Positiveendcollar:5mmnominalmarginbeyondcommandedbearingpositions')
 # Overhead rails are supported only from storage-side posts, not through payload corridor.
 for xx in [-76,376]:
  add('Gantry_longitudinal_'+str(xx),box((8,360,8),(xx,-265,gx+20)))
  add('Gantry_rear_post_'+str(xx),box((8,12,gx+20),(xx,-265,0)))
 for yy in [-255,70]:
  add('Gantry_crossmember_'+str(yy),box((468,10,8),(-76,yy,gx+20)))
  for xx in [-20,360,-48]:
   add('Overhead_hanger_'+str(xx)+'_'+str(yy),box((8,10,14),(xx-4,yy,gx+6)))
 # Source-matched10x2 screw nominal major blank,8mm journal ends.
 ss=[cyl(5,330,(-48,-250,gx)),cyl(4,15,(-48,-265,gx)),cyl(4,15,(-48,80,gx))]
 add('SPT10x2M_screw_nominal',union(ss),'steel','drive','10x2lead;majorblank/root7.4mmloadmodel;threadcontact idealized')
 for yy in [-265,85]:
  bear=cyl(11,10,(-48,yy,gx)).cut(cyl(4,10,(-48,yy,gx))).removeSplitter()
  add('Screw_end_bearing_'+str(yy),bear,'steel','fixed','22mmOD8mmbore geometric bearing representation;catalograting not asserted')
  housing=box((30,12,30),(-63,yy-1,gx-15)).cut(cyl(11,12,(-48,yy-1,gx))).removeSplitter()
  add('Screw_bearing_housing_'+str(yy),housing)
  # Connect housing top to overhead rail; outside the moving nut span.
  add('Screw_hanger_'+str(yy),box((8,12,5),(-52,yy-1,gx+15)))
 add('Front_screw_roof_connection',box((8,26,8),(-52,70,gx+20)))
 add('Brake_bearing_coupler',cyl(4,10,(-48,-275,gx)),'steel','drive','Nominal8mmshaftadaptergap;brake5/6mmborecustomadapterfuture')
 # The nut outer form matches the capturedSB3700dimensions,thread form idealized.
 nut=cyl(9.55,19.1,(-48,rear-9.55,gx)).cut(cyl(5,19.1,(-48,rear-9.55,gx))).removeSplitter()
 add('SB3700_nut_nominal',nut,'polymer','moving','19.1mmODx19.1mmL;10x2 thread idealized;no thread manufacturing geometry')
 # One connected fork/frame, with rear pads transmitting controlled feed force.
 ss=[box((416.5,4,10),(-38,rear-5,gx-30)),
     box((L-16,2,6),(x0+8,rear-3,24)),box((L-16,2,6),(x0+8,rear-3,114))]
 for xx in [x0+8,x0+L-16]:
  ss.append(box((8,2,108),(xx,rear-6,24)))
  for zz in [24,114]:ss.append(box((8,5,6),(xx,rear-6,zz)))
  ss.append(box((8,5,gx-120),(xx,rear-6,120)))
 for xx in [-20,360]:
  ss.append(box((26,30,24),(xx-13,rear-15,gx-12)).cut(cyl(8,30,(xx,rear-15,gx))))
 ss += [box((44,20,20),(-60,rear-10,gx-10)),box((26,24,26),(-61,rear-12,gx-13)).cut(cyl(9.55,24,(-48,rear-12,gx)))]
 for xx in [-20,360]:ss.append(box((12,10,16),(xx-6,rear-10,gx-22)))
 # A rear pusher is used within the capped channel. The receiverfarstop
 # is provedclosed before this cell'sstoragegateopens. No frontforkgate,
 # pullingcapability or dynamically latched transferpose is assumed.
 frame=union(ss)
 for xx in [-20,360]:frame=frame.cut(cyl(8,50,(xx,rear-25,gx)))
 frame=frame.cut(cyl(9.55,50,(-48,rear-25,gx))).removeSplitter()
 add('Driven_pusher_frame',frame,'aluminium','moving','One connectedrear pusher;rail-contactpads;idealprismaticguide;push-onlycoasttransfer')
 # Storage launch restraint clevis with two6mmsteel pins. Pins never enter payload.
 for xx in [-92,390]:
  cy=-218
  backx=xx-20 if xx<0 else xx+14
  startx=xx-20 if xx<0 else xx-12
  fixed=union([box((32,12,8),(startx,cy-6,gx-36)),box((32,12,8),(startx,cy-6,gx-12)),box((6,12,gx-4),(backx,cy-6,0))])
  fixed=fixed.cut(cyl(3.1,32,(xx,cy,gx-36),(0,0,1))).removeSplitter()
  add('Restraint_clevis_'+str(xx),fixed)
  mz=gx-24
  ml=box((24,12,8),(xx-12,cy-6+u,mz)).cut(cyl(3.1,8,(xx,cy+u,mz),(0,0,1))).removeSplitter()
  add('Restraint_moving_lug_'+str(xx),ml,'aluminium','moving','8mm bearing length on6mm pin; ideal connected via external bracket')
  # A bolted strap connects lug to nut frame on left and guide frame on right.
  linkx=-92 if xx<0 else 360
  add('Restraint_lug_strap_'+str(xx),box((50 if xx<0 else 30,8,8),(linkx,cy-4+u,mz)),'aluminium','moving','Bolted strap mating faces; interface verification listed')
  pz=gx+4 if gate_open else gx-36
  add('Restraint_pin_'+str(xx),cyl(3,32,(xx,cy,pz),(0,0,1)),'steel','latch','6mm nominal;retracted40mm before feed;interlocked')
 for xx in [-44,360]:add('Restraint_lug_connector_'+str(xx),box((8,8,16),(xx,-216+u,gx-22)),'aluminium','moving')
 # Unite load-path lugs/straps into the fork to remove duplicate-volume joints.
 fr=next(q for q in p if q['name']=='Driven_pusher_frame')
 extra=[q for q in p if q['name'].startswith(('Restraint_moving_lug_','Restraint_lug_strap_','Restraint_lug_connector_'))]
 fr['shape']=union([fr['shape']]+[q['shape'] for q in extra])
 for xx in [-92,390]:fr['shape']=fr['shape'].cut(cyl(3.1,40,(xx,-218+u,gx-40),(0,0,1))).removeSplitter()
 for xx in [-20,360]:fr['shape']=fr['shape'].cut(cyl(8,50,(xx,rear-25,gx)))
 fr['shape']=fr['shape'].cut(cyl(9.55,50,(-48,rear-25,gx)))
 fr['shape']=fr['shape'].removeSplitter()
 assert len(fr['shape'].Solids)==1,('Disconnectedpusher',fmt,side)
 p=[q for q in p if q not in extra]
 # Catalog packages are honest envelopes; catalog masses remain a separate ledger.
 add('Motor_3242BX4_gear32GPT9_envelope',cyl(16,78.9,(-48,-388.9,gx)),'catalog_envelope','catalog','3242body44.2mm+32GPT9body34.7mm;shaft/flanges simplified')
 add('Brake_BXW01_envelope',cyl(20,35,(-48,-310,gx)),'catalog_envelope','catalog','0.12Nmstatic/0.2kgsource;40ODx35bboxfrom37ODx31.5source;adapter andspacequalification unverified')
 add('Controller_MC5005S_envelope',box((65,45,20),(50,-260,30)),'catalog_envelope','catalog','Source0.230kg;boundingboxstudy,thermal/connectorlayout notrated')
 for yy in [-204,-4]:add('Limit_sensor_'+str(yy),box((8,8,8),(385,yy,gx-10)),'catalog_envelope','sensor','Presence/home/end sensing functional requirement;not source-rated')
 # Cell mountplate includes ordinary mechanical interface holes.
 base=box((530,160,6),(-116,-278,-6))
 for xx in [-60,374]:
  for yy in [-260,-130]:base=base.cut(cyl(2.25,6,(xx,yy,-6),(0,0,1)))
 add('Cassette_mountplate',base.removeSplitter())
 for xx in [-8,332.5]:
  for yy in [-206,-138]:add('Floor_support_'+str(xx)+'_'+str(yy),box((16,16,14),(xx,yy,0)))
 for xx in [-60,374]:
  for yy in [-260,-130]:
   stand=box((16,16,134),(xx-8,yy-8,-140)).cut(box((12,12,134),(xx-6,yy-6,-140)))
   add('Adapter_standoff_'+str(xx)+'_'+str(yy),stand.removeSplitter(),'aluminium','fixed','Generic134mmhollowstandoff;mountplaneZ-140,connection/loadapprovalprovisional')
 fixed=[q for q in p if q['material']=='aluminium' and q['role'] in ['fixed','fixed_insert']]
 if '--diagnose' in sys.argv:
  for aa in p:
   if aa['name']=='Driven_pusher_frame':
    for bb in fixed:
     if aa['shape'].BoundBox.intersect(bb['shape'].BoundBox):
      vv=aa['shape'].common(bb['shape']).Volume
      if vv>1e-5:print('LOCAL_FRAME_HIT',bb['name'],vv,flush=True)
 fixed_shape=union([q['shape'] for q in fixed])
 fixed_shape=fixed_shape.cut(box((L+4.2,3.2,140),(x0-2.1,-80.1,-10))).removeSplitter()
 p=[q for q in p if q not in fixed]
 assert len(fixed_shape.Solids)==1,('Disconnectedfixedstructure',fmt,side,len(fixed_shape.Solids))
 p.append(row('Fixed_cassette_gantry',fixed_shape,'aluminium','fixed','Fused structural fabrication;no overlapping material at beam joints;source defines component dimensions'))
 for q in p:
  if side=='north':
   reflection=App.Matrix();reflection.A22=-1;reflection.A24=100
   q['shape']=q['shape'].transformGeometry(reflection) if abs(q['shape'].Placement.Rotation.Angle)>1e-12 else q['shape'].mirror(V(0,50,0),V(0,1,0))
  q['shape'].translate(V(offset,0,0))
 CELL_CACHE[key]=[{**q,'shape':q['shape'].copy()} for q in p]
 return p

def receiver(dock=0,fmt='3U',captured=True,launch=False,feed_side=None):
 p=[]
 def add(*a,**k):p.append(row(*a,**k))
 floor=box((364.5,110,6),(-12,-5,14))
 # Four shortYcapturetabs lower below payload-floor rail level during feeding.
 for xx in [5,235,320]:
  for yy in [-1,100]:floor=floor.cut(box((8.2,1.2,8),(xx-.1,yy-.1,13)))
 beams=[floor,box((364.5,5,8),(-12,-10,6)),box((364.5,5,8),(-12,105,6))]
 for xx in [-12,328.5]:
  beams.append(box((24,170,4),(xx,-35,10)))
  for yy in [-25,125]:
   shoe=box((24,30,14),(xx,yy-15,0)).cut(box((24,10.2,10.2),(xx,yy-5.1,-.1)))
   shoe=shoe.cut(box((24,20.2,4.2),(xx,yy-10.1,-.1))).removeSplitter()
   beams.append(shoe)
 # Belt clamp outrigger above the drive belt and below bridge floors.
 beams.append(box((24,50,4),(100,-45,10)))
 fused=union(beams)
 for xx in [5,235,320]:
  for yy in [-1,100]:fused=fused.cut(box((8.2,1.2,24),(xx-.1,yy-.1,0)))
 # Endstop/1Udatumslotspermitfullverticalretractionwithoutfloorpenetration.
 for xx,w in [(222.9,10.2),(334.4,12.2)]:fused=fused.cut(box((w,104.2,24),(xx,-2.1,0)))
 # Docking ears run below bridge floorlevel.
 for xx in [-4,344.5]:
  fused=fused.fuse(box((14,25,4),(xx-7,125,10))).fuse(box((14,14,14),(xx-7,135,-4)))
  fused=fused.cut(cyl(3.1,20,(xx,142,-5),(0,0,1)))
 add('Floor_carriage',fused.removeSplitter(),'aluminium','receiver','Supported linear-profile nominal channels;0.1mm sidegap;not a source-rated bearing')
 for xx in [0,235,324]:add('Floor_corner_rail_'+str(xx),box((8,100,2),(xx,0,20)),'polymer','receiver')
 # Aft3Uwall stays behind an ejecting payload, leading wall retracts fully belowfloor.
 for nm,x in [('aft',-6),('leading',342.5)]:
  dz=-134 if nm=='leading' and launch else 0
  wall=union([box((4,104,108),(x,-2,20+dz)),box((12,104,4),(x if x<0 else x-8,-2,124+dz))])
  wall=wall.cut(box((6,83,83),(x-1,8.5,30.5+dz))).removeSplitter()
  add(nm+'_corner_stop',wall,'aluminium','receiver_gate' if nm=='leading' else 'receiver','Leadingstopdown134mmbeforeLSMlaunch;topcap2mmnominalclearance')
 #1Urearstop retracts sideways out of3Upayload envelope,remaining captive.
 yy=0; iz=0 if fmt=='1U' else -134
 ins=union([box((2,104,108),(223,yy-2,20+iz)),box((10,104,4),(223,yy-2,124+iz))])
 ins=ins.cut(box((4,83,83),(222,8.5,30.5+iz))).removeSplitter()
 add('1U_retractable_aft_stop',ins,'aluminium','receiver_gate','134mmZretraction;activeonly1U;captivenotlaunched')
 for xx in [5,235,320]:
  for yy in [-1,100]:
   farstop=(feed_side=='south' and yy==100) or (feed_side=='north' and yy==-1)
   z=24 if captured or farstop else 12
   add('Y_capture_tab_'+str(xx)+'_'+str(yy),box((8,1,6),(xx,yy,z)),'steel','receiver_gate','12mmlift;Z24..30closedwithinassumed8.5mmcornerrailzone;closedbeforefeedforkrelease;belowfloorwhenopen')
 for label,yy in [('south',-44),('north',-40)]:
  dy=(-4 if label=='south' else 4) if launch else 0
  add('Index_clutch_jaw_'+label,box((20,2,6),(102,yy+dy,4)),'steel','receiver_gate','IndexbeltclutchopensbeforeLSM;idealtransmissionassumption,source-ratedclutchfuture')
 # Station-owned dockingpins engage these carriage bores only when indexed.
 for q in p:q['shape'].translate(V(dock,0,0))
 return p

def rail(dock=0):
 p=[]
 def add(*a,**k):p.append(row(*a,**k))
 for yy in [-25,125]:
  add('Profile_rail_'+str(yy),box((1600,10,6),(-150,yy-5,4)),'steel','rail','Geometric10x6profileblank;source/stiffnessstudy separate')
  add('Rail_support_'+str(yy),box((1600,20,4),(-150,yy-10,0)))
 for yy in [-25,125]:
  for xx in [-60,110,360,610,860,1110,1360,1440]:
   stand=box((16,16,140),(xx-8,yy-8,-140)).cut(box((12,12,140),(xx-6,yy-6,-140)))
   add('Rail_standoff_'+str(yy)+'_'+str(xx),stand.removeSplitter(),'aluminium','rail','250mmapproxsupportspacing;genericweldedfixture/studyinterfaceatZ-140')
 for yy in [-68,-42]:add('Receiver_drive_belt_'+str(yy),box((1540,2,6),(-120,yy,4)),'polymer','rail_drive','Toothed-beltpitch/tension/loadratingundetermined;nominalcloseddrivepath')
 for xx in [-120,1420]:add('Receiver_pulley_'+str(xx),cyl(12,6,(xx,-54,4),(0,0,1)),'aluminium','rail_drive')
 add('Receiver_motor32GPT59_envelope',cyl(16,87.3,(-120,-54,-132.3),(0,0,1)),'catalog_envelope','catalog','3242BX4+32GPT59.4:1sourceoption;adapter/harnessnotmodeled')
 add('Receiver_BXW05_brake_envelope',cyl(40,40,(-120,-54,-45),(0,0,1)),'catalog_envelope','catalog','2Nm,.8kg,13Wsource;80ODx40bboxconservative;12mmboreadapterrequired')
 add('Receiver_brake_pulley_shaft',cyl(6,9,(-120,-54,-5),(0,0,1)),'steel','rail_drive','12mmnominaladapterstub;key/couplingdesignfuture')
 for xx in [0,250,650,900]:
  for px in [-4,344.5]:
   sock=box((14,14,10),(xx+px-7,135,-20)).cut(cyl(3.1,10,(xx+px,142,-20),(0,0,1)))
   add('Dock_socket_'+str(xx)+'_'+str(px),sock,'aluminium','rail','6.2mmboregeometricdockinterface')
   pz=-20 if dock==xx else -56
   add('Station_dock_pin_'+str(xx)+'_'+str(px),cyl(3,32,(xx+px,142,pz),(0,0,1)),'steel','docking','Station-ownedpinretractsbelow-24mmbeforeindex/LSM;closedtop12mmbelowbridgefloor14mm')
 return p

CELLS=[('CellA_1U','1U',0,'south'),('CellB_3U','3U',250,'north'),('CellC_1U','1U',650,'south'),('CellD_3U','3U',900,'north')]
def assembly(active=None,u=0,phase='stored',launch=False,fmt='3U',dock=0):
 out=[]
 for cid,f,x,side in CELLS:
  isactive=cid==active
  advancing=u if isactive else 0
  gp=isactive and phase not in ['stored','launch','index']
  fp=isactive and phase in ['fork_release','return']
  for q in cell(f,advancing,gp,fp,side,x):
   if isactive and phase in ['launch','index'] and q['role']=='payload':continue
   if isactive and phase=='return' and q['role']=='payload':
    q['shape'].translate(V(0,(200-u)*(1 if side=='south' else -1),0))
   q['name']=cid+'__'+q['name'];out.append(q)
 feed_side=next((side for cid,f,x,side in CELLS if cid==active),None)
 for q in receiver(dock,fmt,phase in ['stored','captured','fork_release','return','index','launch'],launch,feed_side):q['name']='Receiver__'+q['name'];out.append(q)
 for q in rail(None if phase in ['launch','index'] else dock):q['name']='Common__'+q['name'];out.append(q)
 if active and phase in ['launch','index']:
  x0=227 if fmt=='1U' else 0;L=113.5 if fmt=='1U' else 340.5
  out.append(row('Receiver__Delivered_payload_'+fmt,box((L,100,100),(dock+x0,0,22)),'payload','payload'))
 return out

def massprops(items):
 ss=[]
 for q in items:
  rho=RHO[q['material']]
  for sh in q['shape'].Solids:
   if rho: ss.append((sh,rho,sh.Volume*rho,sh.CenterOfMass))
 mass=sum(t[2] for t in ss);cg=sum((t[3]*t[2] for t in ss),V())/mass
 I=[[0.]*3 for _ in range(3)]
 for sh,rho,m,c in ss:
  mat=sh.MatrixOfInertia;d=c-cg;dd=[d.x,d.y,d.z];d2=d.dot(d)
  for i in range(3):
   for j in range(3):I[i][j]+=(getattr(mat,'A'+str(i+1)+str(j+1))*rho+m*((d2 if i==j else 0)-dd[i]*dd[j]))*1e-6
 bb=items[0]['shape'].BoundBox
 for q in items[1:]:bb.add(q['shape'].BoundBox)
 return {'represented_material_mass_kg':mass,'represented_material_CG_mm':[cg.x,cg.y,cg.z],'represented_material_inertia_CG_kg_m2':I,'bounds_mm':[bb.XMin,bb.XMax,bb.YMin,bb.YMax,bb.ZMin,bb.ZMax],'box_volume_litre':bb.XLength*bb.YLength*bb.ZLength/1e6,'full_installed_mass_kg':None,'mass_boundary':'Customgeometrymaterialonly;payload/catalogpackagesexcluded;catalogledgerseparate;harness/fasteners/gateactuatorsnotcomplete'}

def export(stem,items):
 d=App.newDocument(stem);rows=[]
 for i,q in enumerate(items):
  obj=d.addObject('Part::Feature','Part'+str(i));obj.Label=q['name'];obj.Shape=q['shape']
  obj.addProperty('App::PropertyFloat','Density_kg_m3');obj.Density_kg_m3=RHO[q['material']]*1e9
  for prop,val in [('Material',q['material']),('Role',q['role']),('EvidenceBoundary',q['notes']),('Revision',REV)]:obj.addProperty('App::PropertyString',prop);setattr(obj,prop,val)
  rows.append({'name':q['name'],'material':q['material'],'role':q['role'],'volume_mm3':q['shape'].Volume,'material_mass_kg':q['shape'].Volume*RHO[q['material']],'notes':q['notes']})
 d.recompute();native=O/(stem+'.FCStd');step=O/(stem+'.step');d.saveAs(str(native));Part.export(d.Objects,str(step));sh=Part.read(str(step));assert sh.isValid()
 vol=sum(q['shape'].Volume for q in items);err=abs(sh.Volume-vol);assert err<max(.01,vol*1e-6),(stem,err)
 objdir=O/'obj';objdir.mkdir(exist_ok=True)
 objpath=objdir/(stem+'.obj');meta=[];vid=1
 with objpath.open('w') as f:
  f.write('# FM08-R3 true native BRep tessellation;unitsmm;not a solver screenshot\n')
  for q in items:
   vv,tt=q['shape'].tessellate(.6);f.write('o '+q['name']+'\n')
   for v in vv:f.write('v %.7f %.7f %.7f\n'%(v.x,v.y,v.z))
   for t in tt:f.write('f '+' '.join(str(vid+i) for i in t)+'\n')
   vid+=len(vv);meta.append({'name':q['name'],'role':q['role'],'material':q['material'],'vertex_count':len(vv),'triangle_count':len(tt)})
 (objdir/(stem+'.json')).write_text(json.dumps({'revision':REV,'units':'mm','native_sha256':hashlib.sha256(native.read_bytes()).hexdigest(),'parts':meta},indent=2)+'\n')
 App.closeDocument(d.Name)
 return {'native':native.name,'step':step.name,'parts':len(items),'step_solids':len(sh.Solids),'step_volume_error_mm3':err,'BOM':rows,'mass_properties':massprops(items),'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [native,step]}}

def audit(items,only_payload=False,include_catalog=False):
 hits=[];mind=1e99;minpair=None;tested=0
 for a,b in itertools.combinations(items,2):
  if only_payload and a['role']!='payload' and b['role']!='payload':continue
  if not include_catalog and (a['material']=='catalog_envelope' or b['material']=='catalog_envelope'):continue
  sa=a['shape'];sb=b['shape']
  if not sa.BoundBox.intersect(sb.BoundBox):continue
  tested+=1;vol=sa.common(sb).Volume
  if vol>1e-5:hits.append({'a':a['name'],'b':b['name'],'volume_mm3':vol})
 return {'tested_bounding_box_pairs':tested,'positive_volume_interferences':hits,'pass':not hits}

def main():
 st=time.perf_counter()
 states=[('FM08_R3_four_cell_stowed',None,0,'stored',False,'3U',0),('FM08_R3_four_cell_1U_seated','CellA_1U',200,'captured',False,'1U',0),('FM08_R3_four_cell_3U_seated','CellB_3U',200,'captured',False,'3U',250),('FM08_R3_four_cell_launch','CellB_3U',0,'launch',True,'3U',0),('FM08_R3_four_cell_midtransfer','CellB_3U',100,'transfer',False,'3U',250)]
 captures=[]
 for name,active,u,phase,launch,fmt,dock in states:
  pp=assembly(active,u,phase,launch,fmt,dock);cap=export(name,pp)
  # One complete inclusive audit; physical/payload subsets reuse the exact pair results.
  inc=audit(pp,False,True);nn={q['name']:q for q in pp}
  physical=[hit for hit in inc['positive_volume_interferences'] if nn[hit['a']]['material']!='catalog_envelope' and nn[hit['b']]['material']!='catalog_envelope']
  payload=[hit for hit in physical if nn[hit['a']]['role']=='payload' or nn[hit['b']]['role']=='payload']
  cap['static_interference_audit']={'positive_volume_interferences':physical,'pass':not physical,'scope':'Physical subset of same inclusive all-pair audit'}
  cap['payload_interference_audit']={'positive_volume_interferences':payload,'pass':not payload,'scope':'Payload subset of same inclusive all-pair audit'}
  cap['including_catalog_envelopes_audit']=inc;captures.append(cap)
  (O/(name+'.json')).write_text(json.dumps(cap,indent=2)+'\n');print(name,'exported',len(pp),'hits',len(cap['static_interference_audit']['positive_volume_interferences']),flush=True)
 # Independent-cell motion samples include gate-open,fullfeed,capture,return;all nominalonly.
 motion=[]
 for fmt in ['1U','3U']:
  for u in [0,25,50,75,100,125,150,175,200]:
   pp=cell(fmt,u,True,False)
   for q in receiver(0,fmt,False):q['name']='Receiver__'+q['name'];pp.append(q)
   r=audit(pp,True);r.update({'format':fmt,'feed_mm':u,'phase':'transfer','minimum_payload_side_clearance_design_mm':2,'minimum_payload_top_clearance_design_mm':2});motion.append(r)
   print('motion',fmt,u,len(r['positive_volume_interferences']),flush=True)
 summary={'revision':REV,'software':{'FreeCAD':'.'.join(App.Version()[:3]),'OCC':Part.OCC_VERSION},'builder_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'selected_architecture':'Independent guided lead-screw pushers, capped channels and one common belt-indexed receiver','design_basis':{'manifest':{'1U':2,'3U':2},'payload_mm':{'1U':[113.5,100,100],'3U':[340.5,100,100]},'feed_axis':'Y','launch_axis':'X','feed_stroke_mm':200,'feed_time_s':30,'receiver_docks_X_mm':[0,250,650,900],'receiver_index_travel_mm':900,'rail_length_mm':1600,'guide_shaft_diameter_mm':8,'guide_shaft_span_mm':330,'guide_bush_length_mm':30,'minimum_bush_end_margin_mm':35,'lead_screw':'SPT10x2M10x2nominal','nut':'SB370019.1ODx19.1Lnominal','screw_nominal_free_span_mm':350,'nominal_feed_condition':'Coast-only;nohostmaneuver;push-only;farstopclosedbeforestoragegateopens;settlingandcaptureproofbeforepusherretract','channel_transition_seam_mm':{'3U':6,'1U':8},'transition_seam_only_cap_support_mm':{'3U':94,'1U':92},'gate_slot_cap_gap_mm':3.2,'minimum_geometric_cap_support_length_mm':{'3U':90.8,'1U':88.8},'corner_contact_zone_Z_mm':[[24,30],[114,120]],'underfloor_mount_plane_Z_mm':-140,'guide_centres_X_mm':[-20,360],'payload_leading_X_mm':340.5,'payload_bottom_Z_mm':22,'nominal_X_top_clearance_mm':2,'fixed_1U_insert':'Cassette-mounted;noinsertlaunched'},'captures':captures,'motion_samples':motion,'limitations':['Nominalkinematicgeometry;nospaceorproviderqualification','Screwthreadsandrollingcontactsrepresentedbydiameterenvelopes;manufacturingfitsnotreleased','Catalogmotor/gear/brake/controlleroptionsseparatefromcustomCADmass;gateactuators/harness/fastenersnotcompletelyinstalled','ContactsolverposeconvergencefromFM06-R1doesnottransferandisnotclaimedaccepted','MotionresultsaredeclaredBRepsamplesandanalyticalscreens;nohardwarequalification'], 'elapsed_s':time.perf_counter()-st}
 (O/'GEOMETRY_REPORT.json').write_text(json.dumps(summary,indent=2)+'\n')
 print('complete',summary['elapsed_s'],flush=True)
if __name__=='__main__':main()
