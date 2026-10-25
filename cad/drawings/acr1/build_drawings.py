#!/usr/bin/env python3
"""CAD-derived A3 outline/interface drawings from immutable ACR1 native states.

Run with a Python configured to import FreeCAD 1.0.0, Part and TechDraw.
Inkscape exports the editable SVG sheets to PDF; no accepted CAD is rewritten.
"""
from pathlib import Path
import csv,hashlib,html,json,math,subprocess,sys,time
try:
    import FreeCAD as App
    import Part
except ImportError:
    sys.path.append('/usr/lib/freecad-python3/lib')
    import FreeCAD as App
    import Part
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
SOURCE=ROOT/'validation/acr1'
W,H=1680,1188
INK='#172631';MUTED='#526572';ACCENT='#176d89'

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads((SOURCE/p).read_text())
def esc(s):return html.escape(str(s))
def text(x,y,s,size=17,fill=INK,weight=400):return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}">{esc(s)}</text>'
def line(x1,y1,x2,y2,color=INK,width=1.3,dash=None):return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"'+(f' stroke-dasharray="{dash}"'if dash else'')+'/>'
def dimh(a,b,y,label):
    x1,y1=a;x2,y2=b
    return [line(x1,y1,x1,y+7,MUTED,.8),line(x2,y2,x2,y+7,MUTED,.8),line(x1,y,x2,y,MUTED,.9),line(x1-5,y+5,x1+5,y-5),line(x2-5,y+5,x2+5,y-5),text((x1+x2)/2-45,y-10,label,16)]
def dimv(a,b,x,label):
    x1,y1=a;x2,y2=b
    return [line(x1,y1,x+7,y1,MUTED,.8),line(x2,y2,x+7,y2,MUTED,.8),line(x,y1,x,y2,MUTED,.9),line(x-5,y1+5,x+5,y1-5),line(x-5,y2+5,x+5,y2-5),text(x+10,(y1+y2)/2,label,16)]
def base(number,title):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="297mm" viewBox="0 0 {W} {H}">','<rect width="1680" height="1188" fill="white"/>','<g font-family="DejaVu Sans, sans-serif">','<rect x="26" y="26" width="1628" height="1136" fill="none" stroke="#172631" stroke-width="2"/>',text(52,64,'VOLLEY-G5-ACR1',23,ACCENT,700),text(52,97,title,24,INK,700),text(52,124,'OUTLINE / PRELIMINARY ENGINEERING — dimensions in mm; no general manufacturing tolerance assigned',15,MUTED),line(26,140,1654,140),line(26,1080,1654,1080),text(48,1111,f'{number}  |  Revision A  |  25 October 2026  |  A3 landscape',16,INK,700),text(48,1138,'Source: frozen ACR1 native geometry and paired BOM/verification. Do not scale; stated dimensions govern.',15,MUTED),text(1190,1111,'Academic engineering outline',16),text(1190,1138,'NOT A MANUFACTURING RELEASE',16,INK,700)]
def finish(parts,path):
    path.write_text('\n'.join(parts+['</g></svg>'])+'\n')
    subprocess.run(['inkscape',str(path),'--export-type=pdf','--export-filename='+str(path.with_suffix('.pdf'))],check=True,capture_output=True)
def note(parts,x,y,rows,size=17,step=27):
    for n,s in enumerate(rows):parts.append(text(x,y+n*step,s,size))

p=read('cad/PARAMETERS.json');home=SOURCE/'cad/release/VOLLEY_G5_ACR1_home.FCStd';source_before=digest(home)
doc=App.openDocument(str(home));objects={o.Label:o for o in doc.Objects if hasattr(o,'Shape')and not o.Shape.isNull()}
import TechDraw
assert len(objects)==387
shape=Part.Compound([o.Shape for o in objects.values()]);bb=shape.BoundBox
PROJECTIONS={}

def project(key,names,view,box,parts,title,section=None):
    """Exact TechDraw HLR then <=0.04 mm curve chord approximation in source units."""
    selected=[objects[n].Shape for n in names]
    compound=Part.Compound(selected)
    if section is not None:
        x=section
        wire=Part.makePolygon([App.Vector(x,-2000,-2000),App.Vector(x,2000,-2000),App.Vector(x,2000,2000),App.Vector(x,-2000,2000),App.Vector(x,-2000,-2000)])
        plane=Part.Face(wire);edges=[]
        for s in selected:edges.extend(s.section(plane).Edges)
        assert edges,'Empty native section'
        compound=Part.Compound(edges)
    matrix=App.Matrix()
    if view=='side':matrix.A11=1;matrix.A12=0;matrix.A13=0;matrix.A21=0;matrix.A22=0;matrix.A23=1;matrix.A31=0;matrix.A32=-1;matrix.A33=0
    elif view=='end':matrix.A11=0;matrix.A12=1;matrix.A13=0;matrix.A21=0;matrix.A22=0;matrix.A23=1;matrix.A31=1;matrix.A32=0;matrix.A33=0
    compound=compound.transformGeometry(matrix)
    if section is None:
        projected=TechDraw.project(compound,App.Vector(0,0,1));visible=Part.Compound([q for q in projected[:2]if not q.isNull()]);edges=visible.Edges
    else:edges=compound.Edges
    assert edges
    bounds=Part.Compound(edges).BoundBox;x,y,w,h=box
    candidates=[1,2,2.5,4,5,8,10,12.5,15,20,25]
    denom=next(v for v in candidates if bounds.XLength*4/v<=w-100 and bounds.YLength*4/v<=h-90)
    scale=4/denom;ox=x+(w-bounds.XLength*scale)/2-bounds.XMin*scale;oy=y+(h+bounds.YLength*scale)/2+bounds.YMin*scale
    parts.append(text(x+10,y+20,f'{title}  |  scale 1:{denom:g}',16,ACCENT,700))
    pts=[]
    for e in edges:
        vertices=e.discretize(Deflection=.04)
        if len(vertices)<2:continue
        points=' '.join(f'{ox+v.x*scale:.3f},{oy-v.y*scale:.3f}'for v in vertices)
        pts.append(f'<polyline points="{points}" fill="none" stroke="{INK}" stroke-width="0.75"/>')
    parts.extend(pts)
    PROJECTIONS[key]={'source_native':str(home.relative_to(ROOT)),'source_sha256':source_before,'objects':names,'view':view,'section_plane_X_mm':section,'visible_edge_count':len(edges),'curve_chord_deflection_mm':.04,'scale_denominator':denom,'projected_bounds_mm':[bounds.XMin,bounds.XMax,bounds.YMin,bounds.YMax]}
    return lambda a,b:(ox+a*scale,oy-b*scale)

allnames=list(objects)
# D01 assembly envelope: complete accepted home geometry, no surrogate sketch substituted.
s=base('D01','General arrangement — complete home-state envelope')
top=project('D01_top',allnames,'top',(55,155,1070,500),s,'PLAN: +Z projection')
s.extend(dimh(top(bb.XMin,bb.YMin),top(bb.XMax,bb.YMin),650,f'{bb.XLength:.1f} overall X'))
s.extend(dimv(top(bb.XMin,bb.YMin),top(bb.XMin,bb.YMax),65,f'{bb.YLength:.1f} overall Y'))
side=project('D01_side',allnames,'side',(55,695,1070,350),s,'SIDE: X-Z projection')
s.extend(dimv(side(bb.XMin,bb.ZMin),side(bb.XMin,bb.ZMax),65,f'{bb.ZLength:.1f} overall Z'))
note(s,1155,198,['Home envelope from native BRep:',f'X  {bb.XMin:.1f} to {bb.XMax:.1f}',f'Y  {bb.YMin:.1f} to {bb.YMax:.1f}',f'Z  {bb.ZMin:.1f} to {bb.ZMax:.1f}','', '12 × 4 kg 3U envelope surrogates','2 fixed banks × 6 levels','', 'Projected home: 387 connected parts','Powered travel: 1300','Carrier aft X: 200 → 1500','Arrest allocation: 210','Rail X: 0 → 2250','','Reference mounting plane Z = -150','Generic host ladder included.','No provider hole-pattern approval.'],16)
finish(s,HERE/'D01_general_arrangement.svg')
# D02 exact transverse cut through motor active region.
motor=[n for n in allnames if any(q in n for q in ['Sled_connected_chassis','Stator','Phase_','Halbach','Magnet'])]
if len(motor)<5:motor=[n for n in allnames if n.startswith('Motor')or'stator'in n.lower()or'magnet'in n.lower()or n=='Sled_connected_chassis']
motor += [n for n in ['Track_minusY','Track_plusY']if n not in motor]
print('motor objects',len(motor),flush=True)
s=base('D02','Motor section and launch datums')
end=project('D02_section',motor,'end',(65,165,910,690),s,'SECTION A-A at X = 400',section=400)
s.extend(dimv(end(45,6),end(45,-6),920,'12.0'))
s.extend(dimv(end(30,5),end(30,-5),830,'10.0'))
s.extend(dimv(end(15,3),end(15,-3),740,'6.0'))
note(s,1010,185,['Nominal transverse stack (Z):','Upper magnet inner face   +6','Upper GFRP outer face     +5','Upper copper face        +3','Lower copper face        -3','Lower GFRP outer face    -5','Lower magnet inner face  -6','','Each magnet/package face gap: 1','Copper active thickness: 6','GFRP: 2 each active face','Active bar: 7 × 6 = 42 mm²','Return minimum: 7 × 3 = 21 mm²','','These are CAD nominal dimensions.','Airgap budget is on sheet D05.','No blanket fit/flatness grade set.'],16)
note(s,75,912,['Active magnet X relative to carrier aft: 76 to 412 (336 active; 340 mounting envelope).','Home active X: 276 to 612. Release active X: 1576 to 1912.','216 stator belts at 8 pitch: X 230 to 1958; end allowance 46 at home/release.','Payload floor Z = 46. Carrier top plate Z = 14 to 30; bottom plate Z = -30 to -14.','Native rails: -Y bounds Y -146 to -108, Z -40 to 24; +Y bounds Y 46 to 110, Z -80 to -7.'],17,28)
finish(s,HERE/'D02_motor_section.svg')
# D03 actual one-cell hardware and indexed lift in the home assembly.
cell=[n for n in allnames if n.startswith('Bank_south_L0_')]
lift=[n for n in allnames if n.startswith('Lift_')or n.startswith('Cradle_')or n=='Captive_payload_pallet']
s=base('D03','Cassette feed and lift interfaces')
project('D03_cell',cell,'top',(55,170,800,600),s,'South bank level 0: PLAN')
project('D03_lift',lift,'side',(870,170,730,600),s,'Lift/pallet: SIDE')
note(s,70,820,['Cell floors Z: 180, 310, 440, 570, 700, 830 (pitch 130).','Payload 340.5 × 100 × 100; channel side/top clearance 2.','Cell centers Y = ±250; feed stroke 250 in 40 s (study).','Guides Ø10; span 330. Screw Ø10, lead 2, study root Ø7.4.','South guide Y = -435 to -105; front journal -120 to -100.'],16,30)
note(s,880,820,['Lift docking floor Z = 46; highest floor 830 → travel 784.','Twin screw nominal Ø16, lead 4; study root Ø11.','Fixed screw axes Y = -200 and +220.','Reference gearbox ratio 19.8; maximum lift time 120 s.','Reference actuator envelopes do not define supplier flanges.'],16,30)
finish(s,HERE/'D03_feed_lift_interfaces.svg')
# D04 retained pallet / actual sled interfaces.
sled=[n for n in allnames if n.startswith('Sled_')or n.startswith('Pallet_')or n=='Captive_payload_pallet']
s=base('D04','Sled, captive pallet and custody interfaces')
project('D04_top',sled,'top',(65,175,1000,390),s,'Retained sled/pallet: PLAN')
project('D04_side',sled,'side',(65,600,1000,380),s,'Retained sled/pallet: SIDE')
note(s,1110,190,['Carrier home aft X = 200.','Carrier nominal length 488.','Full home assembly X:','168 to 714.5 with pallet hardware.','','Pallet lock relative X: 40 / 468','Lock axis Y = -90','Carrier shaft bore Ø6.2','Stem Ø6; entry round bore Ø7','Entry key slot 13 × 5','Bayonet stroke 12; rotation 90°','','Lift grip X: 178 / 704.5','Grip pin Ø6; bore Ø6.2','Grip withdrawal stroke Y: 26','','Pallet feet Z = 30 to 38','Payload rail contact Z = 46','Flight clearance nominal 0.5'],16,29)
note(s,70,1014,['Custody: land → close capture caps/lockpins → insert/rotate both bayonets → prove → open keepers → withdraw grips → raise clear.'],16)
finish(s,HERE/'D04_pallet_sled_interfaces.svg')
# D05 tolerances and inspection allocations from frozen budgets.
budget=read('analysis/DESIGN_BUDGETS.json');s=base('D05','Datum, tolerance-budget and assembly inspection notes')
note(s,65,188,['PROJECT REFERENCE DATUMS (preliminary; no supplier datum scheme assigned)', 'A: generic mounting plane Z = -150. B: launch direction +X. C: launcher median plane Y = 0.', 'Dimensions are basic CAD nominal values. A general ± tolerance or GD&T release is not assigned.'],18,33)
s.append(line(55,285,1625,285))
note(s,65,328,['MAGNET/PACKAGE INDIVIDUAL-FACE STACK — declared allocation, not a measured fit', 'Nominal 1.000 − FE paired closure 0.371778/2 − guide centring 0.200 − flatness 0.150', '− assembly 0.150 − differential thermal 0.050 = 0.264111 mm residual per face.', 'FE closure uses the declared 130% load screen; load/material/mesh limits remain in the source report.'],18,34)
note(s,65,510,['CRADLE ENDWALL STACK — each nominal axial gap 0.500', 'Machining allocation 0.100 + docking allocation 0.100; differential CTE assumption 12 µm/(m·K).', '340.5 mm reference length: residual 0.300000 / 0.218280 / 0.136560 / 0.054840 mm', 'at differential temperature 0 / 20 / 40 / 60 K. Elastic contacts need later correlation.'],18,34)
note(s,65,690,['ASSEMBLY AND INSPECTION SEQUENCE', '1  Identify each part against BOM_HOME.csv and frozen native labels; verify material class and mass assignment.', '2  Establish project mounting and rail datums; inspect rail straightness/parallelism within the allocated stack.', '3  Assemble insulated stator and sled; inspect both face gaps over home-to-release travel before energizing.', '4  Verify cassette guide/channel clearance, screw support alignment and each of twelve prescribed transfer routes.', '5  Land pallet; inspect caps, lockpins, both bayonet/grip overlaps and capture-before-release order.', '6  Inspect cam opening/running clearances and full cradle withdrawal; execute powerless/manual custody checks.', '7  Record as-built dimensions, exceptions and inspection instrument calibration before a hardware test release.'],17,38)
note(s,65,1030,['Acceptance checklist: INSPECTION_PLAN.csv. No inspection, material certification, torque or physical test is recorded here.'],16)
finish(s,HERE/'D05_tolerance_assembly_inspection.svg')
# D06 exact accepted mass/CG/inertia ledger, with separate allowance.
mass=read('verification/MASS_CG_INERTIA_SUMMARY.json');groups=mass['states'][0]['groups'];dry=groups['dry_native_assembly'];loaded=groups['loaded_native_assembly'];sledmass=read('analysis/RESOURCE_LEDGER.json')['moving_sled_with_pallet_kg']
s=base('D06','Mass properties, material classes and fabrication boundary')
note(s,65,190,[f'HOME native assembly: 387 parts; loaded {loaded["mass_kg"]:.6f} kg = dry {dry["mass_kg"]:.6f} + payload 48.000000.',f'Represented dry CG (mm): X {dry["CG_m"][0]*1000:.6f}; Y {dry["CG_m"][1]*1000:.6f}; Z {dry["CG_m"][2]*1000:.6f}.',f'Loaded native CG (mm): X {loaded["CG_m"][0]*1000:.6f}; Y {loaded["CG_m"][1]*1000:.6f}; Z {loaded["CG_m"][2]*1000:.6f}.',f'Retained sled with pallet: {sledmass:.6f} kg. Mission device: 156.556720 kg; loaded device: 204.556720 kg.','Extra 7.000 kg power/control allowance has NO assigned position and is excluded from CAD CG/inertia.'],18,35)
note(s,65,420,['Represented dry inertia about its own CG [kg·m²], full tensor, source sign convention:'],18)
for i,row in enumerate(dry['inertia_about_CG_kg_m2']):s.append(text(150,465+i*37,'[ '+'    '.join(f'{v: .9f}'for v in row)+' ]',22))
note(s,65,625,['Materials are assigned density classes; no alloy temper, coating, bond specification or supplier certification is assigned.', 'Aluminium 2700; steel 7850; copper 8960; NdFeB 7500; polymer 1410; insulator 1800 kg/m³.', 'Catalog/payload envelope mass distributions remain approximate; see exact per-group source boundaries.', 'BOM_HOME.csv contains all native part labels, assigned masses, CG coordinates, volumes and source notes.', 'MASS_PROPERTIES.json retains all eight native-state accepted group CG/inertia records.'],18,36)
note(s,65,865,['PRELIMINARY FABRICATION ROUTE', 'Frame/pallet: stock machining and joint/inspection planning remain to be detailed from the owned solid model.', 'Copper phases: preserve connected topology, minimum return section and insulation gaps; joining/insulation process unselected.', 'Guides, screws, bearings, brakes and actuators: source envelope/reference only where catalog interfaces are unselected.', 'No fastener torque, interference fit, vacuum material compatibility or supplier acceptance is invented by these sheets.'],17,35)
finish(s,HERE/'D06_mass_materials.svg')
# Machine-readable drawing inputs and exact paired ledger exports.
metadata=read('cad/release/VOLLEY_G5_ACR1_home.json')
with (HERE/'BOM_HOME.csv').open('w',newline='')as f:
    wr=csv.writer(f);wr.writerow(['name','material_class','subsystem','solids','volume_mm3','assigned_mass_kg','CG_X_mm','CG_Y_mm','CG_Z_mm','source_note'])
    for row in metadata['BOM']:wr.writerow([row['name'],row['material'],row['subsystem'],row['solids'],row['volume_mm3'],row['mass_kg'],*row['CG_mm'],row.get('note','')])
(HERE/'MASS_PROPERTIES.json').write_text(json.dumps({'configuration_id':'VOLLEY-G5-ACR1','source_sha256':digest(SOURCE/'verification/MASS_CG_INERTIA_SUMMARY.json'),'states':mass['states'],'unplaced_power_control_allowance_kg':7,'scope':'Accepted native group properties; no spatial mass properties for the separate allowance.'},indent=2)+'\n')
with (HERE/'INSPECTION_PLAN.csv').open('w',newline='')as f:
    wr=csv.writer(f);wr.writerow(['id','feature','source_nominal_or_budget','proposed_inspection','acceptance_basis','actual_result'])
    for row in [('I01','assembly envelope','2250 × 1240 × 1348.9 mm home','datum-referenced coordinate inspection','nominal CAD outline; no general tolerance assigned'),('I02','magnet/package faces','1 mm nominal each;0.264111 mm allocated residual','noncontact gap map through travel','source face stack; as-built/load validation required'),('I03','cradle endwalls','0.5 mm each','dimensional stack and docking repeatability capture','0.1 machining +0.1 docking allocations; temperature table D05'),('I04','cassette channel','2 mm side/top nominal','gauged surrogate sweep each12 routes','include guide deflection/manufacturing/yaw/thermal budget'),('I05','pallet and grip','Ø6 pins;Ø6.2 bores;12 mm bayonet stroke;90deg rotation','dimensional and positive-custody sequence inspection','nominal fit only; actual tolerances/interfaces require release'),('I06','supplier interfaces','reference envelopes;hardware_selected flags retained','supplier drawing and as-built interface match','external confirmation pending; no invented bolt/flange fit'),('I07','mass/materials','native BOM149.556720 kg dry +7kg allowance','weigh installed parts;record material certifications','as-built ledger supersedes modeled density/envelope assumptions')]:wr.writerow([*row,'NOT_PERFORMED'])
assert digest(home)==source_before
capture={'configuration_id':'VOLLEY-G5-ACR1','revision':'A','drawing_role':'Academic outline and preliminary interface/inspection package; not manufacturing authorization','reuse_audit':'Existing cad/ drawings and Gen5/Gen6 section sheets are different revisions. No current ACR1 engineering-outline sheets existed; frozen current solids and accepted budgets/ledgers reused.','geometry_method':'FreeCAD native BRep read only; TechDraw exact hidden-line projection; visible edges discretized with <=0.04mm source deflection. D02 is a true native planar section at X400.','native_version':App.Version(),'inkscape_version':subprocess.check_output(['inkscape','--version'],text=True).strip(),'source_identities':{n:digest(SOURCE/n)for n in ['cad/release/VOLLEY_G5_ACR1_home.FCStd','cad/release/VOLLEY_G5_ACR1_home.step','cad/release/VOLLEY_G5_ACR1_home.json','cad/PARAMETERS.json','analysis/DESIGN_BUDGETS.json','verification/MASS_CG_INERTIA_SUMMARY.json','analysis/RESOURCE_LEDGER.json']},'envelope_mm':{'X':[bb.XMin,bb.XMax],'Y':[bb.YMin,bb.YMax],'Z':[bb.ZMin,bb.ZMax]},'projections':PROJECTIONS,'source_unchanged_after_generation':True,'material_basis':'Density classes from frozen parameters only; no alloy/temper or physical material certification assigned.','tolerance_basis':'Explicit existing design allocations from DESIGN_BUDGETS, not supplier or measured manufacturing limits.'}
(HERE/'PROJECTION_CAPTURE.json').write_text(json.dumps(capture,indent=2)+'\n');App.closeDocument(doc.Name)
print('Created six paired A3 SVG/PDF drawings and BOM/mass/inspection/projection records',flush=True)

subprocess.run(['pdfunite',*[str(q)for q in sorted(HERE.glob('D*.pdf'))],str(HERE/'ACR1_DRAWING_SET.pdf')],check=True)
files={q.name:{'bytes':q.stat().st_size,'sha256':digest(q)}for q in sorted(HERE.iterdir())if q.is_file()and q.name!='MANIFEST.json'}
(HERE/'MANIFEST.json').write_text(json.dumps({'configuration_id':'VOLLEY-G5-ACR1','drawing_revision':'A','scope':'Six source-derived academic outline/interface sheets and preliminary manufacturing/inspection notes; no manufacturing release','files':files},indent=2)+'\n')
