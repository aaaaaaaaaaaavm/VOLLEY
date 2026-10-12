#!/usr/bin/env python3
"""FreeCAD B-rep mass/CG/inertia ledger for the unselected G1 envelope boxes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import FreeCAD as App

HERE = Path(__file__).resolve().parent
RELEASE = HERE / "release"
P = json.loads((HERE / "parameters.json").read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collect(kind):
    path=RELEASE/f"Gen6_G1_{kind}_Envelope.FCStd"
    doc=App.openDocument(str(path))
    rows=[]
    for obj in doc.Objects:
        if obj.TypeId!="Part::Box":continue
        if obj.MaterialProxy not in P["materials_density_kg_mm3"]:continue
        b=obj.Shape.BoundBox
        m=obj.Shape.Volume*P["materials_density_kg_mm3"][obj.MaterialProxy]
        rows.append(dict(part=obj.Name,mass_kg=m,
                         dimensions_m=[b.XLength/1000,b.YLength/1000,b.ZLength/1000],
                         center_start_m=[obj.Shape.CenterOfMass.x/1000,obj.Shape.CenterOfMass.y/1000,obj.Shape.CenterOfMass.z/1000],
                         moving=obj.Name.startswith(("Carrier_","PM_Armature","Copper_Armature"))))
    App.closeDocument(doc.Name)
    if not rows:raise AssertionError("native document has no material proxy boxes")
    return path,rows


def properties(rows,offset=0,payload=False):
    items=[]
    for row in rows:
        r=dict(row)
        r["center_m"]=list(r["center_start_m"])
        if r["moving"]:r["center_m"][0]+=offset
        items.append(r)
    if payload:
        items.append(dict(part="assigned inert dummy (not a weighed CAD solid)",mass_kg=P["payload_assigned_mass_kg"],
                          dimensions_m=[P["payload_length_3u"]/1000,P["payload_width"]/1000,P["payload_height"]/1000],
                          center_m=[(P["payload_start_x"]+P["payload_length_3u"]/2)/1000+offset,0,
                                    (P["payload_bottom_z"]+P["payload_height"]/2)/1000]))
    mass=sum(x["mass_kg"] for x in items)
    cg=[sum(x["mass_kg"]*x["center_m"][axis] for x in items)/mass for axis in range(3)]
    I=[[0.0]*3 for _ in range(3)]
    for x in items:
        m=x["mass_kg"]
        lx,ly,lz=x["dimensions_m"]
        dx,dy,dz=(x["center_m"][i]-cg[i] for i in range(3))
        diagonal=(m*(ly*ly+lz*lz)/12,m*(lx*lx+lz*lz)/12,m*(lx*lx+ly*ly)/12)
        for i,(local,other) in enumerate(zip(diagonal,(dy*dy+dz*dz,dx*dx+dz*dz,dx*dx+dy*dy))):
            I[i][i]+=local+m*other
        for i,j,product in ((0,1,dx*dy),(0,2,dx*dz),(1,2,dy*dz)):
            I[i][j]-=m*product
            I[j][i]-=m*product
    return dict(mass_kg=mass,cg_m=cg,inertia_about_cg_kg_m2=I)


def main():
    out=dict(evidence_class="FREECAD_RECTANGULAR_PROXY_MASS_PROPERTIES_NOT_INSTALLED_HARDWARE",
             method="FreeCAD exact box B-rep volume/center; declared density; rectangular local inertia plus parallel-axis theorem",
             parameters_sha256=sha(HERE/"parameters.json"),source_sha256=sha(Path(__file__)),candidates={})
    for kind in ("A","B"):
        path,rows=collect(kind)
        out["candidates"][kind]=dict(native_sha256=sha(path),parts=rows,
            dry_partial_start=properties(rows),
            loaded_assigned_dummy_start=properties(rows,payload=True),
            loaded_assigned_dummy_at_stroke_end=properties(rows,offset=P["stroke"]/1000,payload=True))
    out["exclusions"]=["All unrated drive/brake/source and other hardware excluded",
                       "The 4 kg payload is assigned mass in a uniform box, not a real spacecraft mass distribution",
                       "No launch-load deflection, installed mounting or actual dynamic trajectory"]
    path=RELEASE/"Gen6_G1_Partial_Mass_CG_Inertia.json"
    path.write_text(json.dumps(out,indent=2)+"\n")
    print(path)


if __name__=="__main__":main()
