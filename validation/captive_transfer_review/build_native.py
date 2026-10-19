"""Build CT-01 in FreeCAD, verify exact solids and independent STEP readback."""
from pathlib import Path
import hashlib
import json
import itertools
import FreeCAD as App
import Part
from geometry import REVISION, boxes, cycle, interpolate

H=Path(__file__).resolve().parent
O=H/"release"
O.mkdir(exist_ok=True)
DENSITY={"aluminium":2.7e-6,"steel":7.85e-6,"payload":0}


def shapes(L,state):
    grouped={}
    for b in boxes(L,state):
        grouped.setdefault(b["name"],[]).append(b)
    parts=[]
    for name,items in grouped.items():
        ss=[Part.makeBox(*b["size"],App.Vector(*b["lo"])) for b in items]
        shape=ss[0].multiFuse(ss[1:]).removeSplitter() if len(ss)>1 else ss[0]
        assert shape.isValid() and len(shape.Solids)==1,(name,len(shape.Solids))
        parts.append((name,shape,items[0]["material"],items[0]["role"]))
    return parts


records=[]
for label,L in [("1U",113.5),("3U",340.5)]:
    states=cycle(L)
    native_checks=[]
    # Endpoints and midpoint B-rep checks independently exercise the slab audit.
    for k in range(len(states)-1):
        for f in [0,.5,1]:
            ss=shapes(L,interpolate(states[k][1],states[k+1][1],f))
            hits=[]
            for a,b in itertools.combinations(ss,2):
                if a[1].BoundBox.intersect(b[1].BoundBox):
                    volume=a[1].common(b[1]).Volume
                    if volume>1e-6:hits.append([a[0],b[0],volume])
            assert not hits,(label,k,f,hits)
            native_checks.append(dict(phase=states[k+1][0],fraction=f,penetrations=hits))
    for phase,state in states:
        doc=App.newDocument("CT01")
        components=[]
        for name,shape,material,role in shapes(L,state):
            obj=doc.addObject("Part::Feature","Component")
            obj.Label=name
            obj.Shape=shape
            obj.addProperty("App::PropertyString","MaterialBasis").MaterialBasis=material
            obj.addProperty("App::PropertyString","ModelRole").ModelRole=role
            components.append(obj)
        stem=f"CT01_{label}_{phase}"
        doc.recompute()
        doc.saveAs(str(O/(stem+".FCStd")))
        Part.export(components,str(O/(stem+".step")))
        reread=Part.read(str(O/(stem+".step")))
        assert reread.isValid() and len(reread.Solids)==len(components)
        expected=sum(x.Shape.Volume for x in components)
        assert abs(reread.Volume-expected)<max(1e-4,expected*1e-8)
        material=[dict(part=x.Label,volume_mm3=x.Shape.Volume,material=x.MaterialBasis,mass_kg=x.Shape.Volume*DENSITY[x.MaterialBasis],role=x.ModelRole) for x in components]
        total_mass=sum(x["mass_kg"] for x in material)
        cg=[sum(row["mass_kg"]*getattr(obj.Shape.Solids[0].CenterOfMass,axis) for obj,row in zip(components,material))/total_mass for axis in ["x","y","z"]]
        inertia=[[0.0]*3 for _ in range(3)]
        for obj,row in zip(components,material):
            rho=DENSITY[obj.MaterialBasis];mass=row["mass_kg"]
            solid=obj.Shape.Solids[0]
            c=solid.CenterOfMass;v=[c.x-cg[0],c.y-cg[1],c.z-cg[2]];r2=sum(t*t for t in v)
            for i in range(3):
                for j in range(3):
                    inertia[i][j]+=(getattr(solid.MatrixOfInertia,f"A{i+1}{j+1}")*rho+mass*((r2 if i==j else 0)-v[i]*v[j]))*1e-6
        records.append(dict(payload=label,phase=phase,parts=len(components),material_kg=total_mass,CG_material_mm=cg,inertia_material_kg_m2=inertia,
                            material_ledger=material,step_valid=True,step_volume_mm3=reread.Volume,
                            files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [O/(stem+".FCStd"),O/(stem+".step")]}))
        App.closeDocument(doc.Name)
    records[-1]["native_pose_checks"]=native_checks
# Separate tooth/bolt geometry records actual face contact in one stipulated pose.
doc=App.newDocument("ToothCoupon")
base=Part.makeBox(16,30,6)
teeth=[Part.makeBox(16,6,3,App.Vector(0,y,6)) for y in [0,10,20]]
rack=base.multiFuse(teeth).removeSplitter()
bolt=Part.makeBox(16,3,3,App.Vector(0,7,6))
assert rack.common(bolt).Volume<1e-8 and rack.distToShape(bolt)[0]<1e-8
for name,shape in [("thick_root_rack",rack),("engaged_square_bolt",bolt)]:
    ob=doc.addObject("Part::Feature","Component");ob.Label=name;ob.Shape=shape
doc.recompute();doc.saveAs(str(O/"arrest_contact_coupon.FCStd"))
Part.export(doc.Objects,str(O/"arrest_contact_coupon.step"))
read=Part.read(str(O/"arrest_contact_coupon.step"));assert read.isValid() and len(read.Solids)==2
App.closeDocument(doc.Name)
(O/"NATIVE_CAD.json").write_text(json.dumps(dict(revision=REVISION,cases=records,
    boundary="Material-only coupon; no purchased drive/actuator/latch/bearing/harness or source-rated joints. STEP and solids do not establish manufacture readiness.",
    software=dict(FreeCAD=".".join(App.Version()[:3]),OpenCascade=Part.OCC_VERSION),
    source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),H/"geometry.py"]},
    arrest_coupon=dict(face_contact_at_one_pose=True,positive_penetration_mm3=0,engagement_height_mm=3,root_section_mm=[16,6],
      boundary="Square bolt in one rack slot; no insertion spring, pivots, engagement delay, rated actuator, damping cartridge or attached load path.",
      files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [O/"arrest_contact_coupon.FCStd",O/"arrest_contact_coupon.step"]})),indent=2)+"\n")
print("Verified",len(records),"native+STEP states and 60 independent B-rep poses")
