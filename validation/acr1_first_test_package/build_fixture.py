"""Provisional C01 fixture geometry derived from ACR1 dimensions; not a build release."""
from pathlib import Path
import hashlib,json,math,platform
import cadquery as cq
ROOT=Path(__file__).resolve().parent
D=json.loads((ROOT/'DEFINITION.json').read_text())
OUT=ROOT/'geometry';OUT.mkdir(exist_ok=True)
parts=[]
def add(name,shape,material):parts.append((name,shape,material))
def box(l,w,h,x,y,z):return cq.Workplane('XY').box(l,w,h).val().translate((x,y,z))
def tube(od,inner,length,x,y,z):
 a=cq.Solid.makeCylinder(od/2,length,cq.Vector(x,y,z),cq.Vector(0,0,1));b=cq.Solid.makeCylinder(inner/2,length,cq.Vector(x,y,z),cq.Vector(0,0,1));return a.cut(b)
# Gap is CAD Z; source field uses Y as its gap coordinate.
xs=[(i-2.5)*8 for i in range(6)]
for side in [-1,1]:
 plate=box(160,150,12,0,0,side*20)
 for x in [-65,65]:
  for y in [-60,60]:plate=plate.cut(cq.Solid.makeCylinder(4.25,14,cq.Vector(x,y,side*20-7),cq.Vector(0,0,1)))
 for y in [-52,52]:
  for x in xs:plate=plate.cut(cq.Solid.makeCylinder(1.6,14,cq.Vector(x,y,side*20-7),cq.Vector(0,0,1)))
 add(f'Plate_{side}',plate,'aluminium reference; grade/allowables unselected')
 for i,x in enumerate(xs):add(f'Magnet_{side}_{i}',box(8,90,8,x,0,side*10),'NdFeB; Br1.32T model input, grade/certificate unselected')
 for y in [-50,50]:
  lip=box(56,14,3,0,y,side*4.5)
  for x in xs:lip=lip.cut(cq.Solid.makeCylinder(1.6,5,cq.Vector(x,math.copysign(52,y),side*4.5-2.5),cq.Vector(0,0,1)))
  add(f'Keeper_lip_{side}_{y}',lip,'aluminium reference; no joint proof implied')
  for i,x in enumerate(xs):add(f'Keeper_spacer_{side}_{y}_{i}',tube(6,3.2,8,x,math.copysign(52,y),6 if side>0 else -14),'nonmagnetic spacer allocation')
for x in [-65,65]:
 for y in [-60,60]:add(f'Corner_spacer_{x}_{y}',tube(12,8.5,28,x,y,-14),'nonmagnetic compression spacer allocation')
x=-20
add('Force_bar_at_minus20mm',box(7,80,6,x,0,0),'copper')
# Measured force includes the loop. Terminal break is at far return; feed leads allocated.
points=[(x,40,0),(x,90,0),(x+100,90,0),(x+100,5,0)]
points2=[(x+100,-5,0),(x+100,-90,0),(x,-90,0),(x,-40,0)]
for j,path in enumerate([points,points2]):
 for i,(a,b) in enumerate(zip(path,path[1:])):
  start=cq.Vector(*a);delta=cq.Vector(*b)-start
  add(f'Return_wire_{j}_{i}',cq.Solid.makeCylinder(math.sqrt(1/math.pi),delta.Length,start,delta.normalized()),'copper wire area1mm2 allocation')
assembly=cq.Assembly(name='C01_PROVISIONAL_NO_BUILD_RELEASE')
for name,shape,material in parts:assembly.add(shape,name=name)
assembly.save(str(OUT/'C01_coupon_fixture.step'))
rows=[{'part':name,'material_basis':material,'valid':shape.isValid(),'volume_mm3':shape.Volume(),'bounds_mm':{'xmin':shape.BoundingBox().xmin,'xmax':shape.BoundingBox().xmax,'ymin':shape.BoundingBox().ymin,'ymax':shape.BoundingBox().ymax,'zmin':shape.BoundingBox().zmin,'zmax':shape.BoundingBox().zmax}} for name,shape,material in parts]
assert all(r['valid'] and r['volume_mm3']>0 for r in rows)
result={'software':{'cadquery':cq.__version__,'python':platform.python_version()},'status':'PROVISIONAL geometry; no load/build/test authorization','definition_sha256':hashlib.sha256((ROOT/'DEFINITION.json').read_bytes()).hexdigest(),'builder_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'STEP_sha256':hashlib.sha256((OUT/'C01_coupon_fixture.step').read_bytes()).hexdigest(),'parts':rows,'omissions':['Fastener thread/head/nut details and certified grades','Load-cell gantry and electrical isolation/insulation','Probe stage and actual lead connectors','Protective guard and magnet insertion tooling','Complete C02/C03 mechanism fixtures'],'drawing_axes':'CAD X travel, Y magnet depth, Z gap; field model X travel,Y gap,Z depth'}
(OUT/'GEOMETRY_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
# Source-linked vector drawing, shared dimensions with the generated STEP.
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="850" viewBox="0 0 1200 850"><rect width="1200" height="850" fill="white"/><g font-family="DejaVu Sans,sans-serif" fill="#152b3a"><text x="35" y="40" font-size="22" font-weight="bold">C01 one-period magnetic coupon fixture · provisional R1</text><text x="35" y="68" font-size="15">mm · CAD X travel / Y depth / Z gap · controlled ACR1 block dimensions, new bench supports</text><text x="35" y="98" font-size="17" fill="#9a3c1c">NO BUILD OR LOAD RELEASE · geometry and analytical screen only</text></g><g stroke="#234b63" stroke-width="2" fill="none"><rect x="70" y="170" width="480" height="450"/><rect x="208" y="260" width="144" height="270"/><rect x="202" y="239" width="168" height="42"/><rect x="202" y="509" width="168" height="42"/></g>'''
for i in range(1,6):svg+=f'<line x1="{208+i*24}" y1="260" x2="{208+i*24}" y2="530" stroke="#526675"/>'
for x0 in [115,505]:
 for y0 in [215,575]:svg+=f'<circle cx="{x0}" cy="{y0}" r="12.75" fill="none" stroke="#234b63" stroke-width="2"/>'
svg+='''<g font-family="DejaVu Sans,sans-serif" font-size="15" fill="#152b3a"><text x="70" y="145">PLAN: 160 × 150 × 12 plate, each side</text><text x="70" y="648">4 × Ø8.5 at X±65 / Y±60</text><text x="70" y="675">12 × Ø3.2 keeper holes per plate: X −20..20, pitch8; Y±52</text><text x="70" y="702">6 magnets/array: 8 × 90 × 8; array48 × 90</text><text x="70" y="729">Keeper lips56 × 14 × 3, |Y|43..57; 6 spacers/lip, height8</text></g><g stroke="#234b63" stroke-width="2"><rect x="710" y="280" width="380" height="30" fill="#b8cad6"/><rect x="710" y="410" width="380" height="30" fill="#b8cad6"/><rect x="820" y="310" width="140" height="24" fill="#bcc3c8"/><rect x="820" y="386" width="140" height="24" fill="#bcc3c8"/><rect x="872" y="347" width="36" height="26" fill="#bf8357"/></g><g font-family="DejaVu Sans,sans-serif" font-size="15" fill="#152b3a"><text x="710" y="245">SECTION: opposing inner magnet faces Z±6</text><text x="710" y="475">Gap12 ±0.1 under loaded inspection</text><text x="710" y="505">Plate inner faces Z±14; corner spacers length28</text><text x="710" y="535">Active bar7 × 80 × 6; insulated, force-decoupled support</text><text x="710" y="565">Return wire≥1 mm², |Y|90 / Xbar+100</text><text x="710" y="595">Magnetization: top90−60i°, bottom90+60i°</text><text x="710" y="625">Angles in source X/gap plane; mark each block before insertion</text><text x="35" y="790">Source: DEFINITION.json + build_fixture.py · STEP: C01_coupon_fixture.step · bolts, gantry, guards and certified joint design omitted</text><text x="35" y="820">C02/C03 use the controlled ACR1 cell/pallet/keeper geometry; their added ground supports require separate fixture definition.</text></g></svg>'''
(OUT/'C01_fixture_drawing.svg').write_text(svg)
print('Valid provisional STEP solids:',len(rows))
if __name__=='__main__':pass
