"""GP-011 mass properties from an immutable native state plus its paired BOM.

System Python/FreeCAD; this does not reconstruct catalog internal mass layouts.
"""
from pathlib import Path
import argparse,hashlib,json,math,sys
sys.path.append('/usr/lib/freecad/lib')
import FreeCAD as App

def digest(raw):return hashlib.sha256(raw).hexdigest()

def group(rows):
    mass=sum(r['mass_kg']for r in rows)
    if not rows:return dict(part_count=0,mass_kg=0,CG_m=None,inertia_about_CG_kg_m2=None,parts=[])
    assert mass>0
    cg=[sum(r['mass_kg']*r['CG_m'][i]for r in rows)/mass for i in range(3)]
    inertia=[[0.]*3 for _ in range(3)]
    for r in rows:
        offset=[r['CG_m'][i]-cg[i]for i in range(3)];rr=sum(x*x for x in offset)
        for i in range(3):
            for j in range(3):
                inertia[i][j]+=r['inertia_about_part_CG_kg_m2'][i][j]+r['mass_kg']*((rr if i==j else 0)-offset[i]*offset[j])
    return dict(part_count=len(rows),mass_kg=mass,CG_m=cg,inertia_about_CG_kg_m2=inertia,
        uniform_envelope_approximation_mass_kg=sum(r['mass_kg']for r in rows if r['mass_distribution_basis']=='Uniform catalog/payload envelope approximation'),parts=[r['name']for r in rows])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('snapshot',type=Path);ap.add_argument('stem');ap.add_argument('--source-manifest',type=Path);a=ap.parse_args()
    meta=a.snapshot/(a.stem+'.json');native=a.snapshot/(a.stem+'.FCStd');step=a.snapshot/(a.stem+'.step')
    meta_raw=meta.read_bytes();native_raw=native.read_bytes();d=json.loads(meta_raw)
    bom=d['BOM'];assert len(bom)==len({r['name']for r in bom})
    doc=App.openDocument(str(native));objects={}
    for obj in doc.Objects:
        if not hasattr(obj,'Shape')or obj.Shape.isNull():continue
        assert obj.Label not in objects,obj.Label
        objects[obj.Label]=obj
    assert set(objects)=={r['name']for r in bom},dict(native_only=list(set(objects)-{r['name']for r in bom}),bom_only=list({r['name']for r in bom}-set(objects)))
    rows=[]
    for row in bom:
        shape=objects[row['name']].Shape
        assert len(shape.Solids)==1,(row['name'],len(shape.Solids))
        # Exact reflected parts can be a Compound wrapper around their one solid.
        shape=shape.Solids[0];volume=shape.Volume;mass=row['mass_kg']
        assert volume>0 and math.isfinite(mass)and mass>=0,row['name']
        assert abs(volume-row['volume_mm3'])<=max(.01,1e-9*volume),row['name']
        cg=list(shape.CenterOfMass);assert max(abs(cg[i]-row['CG_mm'][i])for i in range(3))<1e-6,row['name']
        geometric=shape.MatrixOfInertia
        tensor=[[getattr(geometric,'A'+str(i+1)+str(j+1))*mass/volume*1e-6 for j in range(3)]for i in range(3)]
        assert all(math.isfinite(v)for r in tensor for v in r)
        approx=row['material']in ['catalog','payload']
        rows.append(dict(name=row['name'],subsystem=row['subsystem'],material=row['material'],mass_kg=mass,
            native_volume_mm3=volume,effective_assigned_density_kg_m3=mass/volume*1e9,
            CG_m=[v*.001 for v in cg],inertia_about_part_CG_kg_m2=tensor,
            mass_distribution_basis='Uniform catalog/payload envelope approximation'if approx else'Uniform native material density over actual solid geometry',
            note=row.get('note','')))
    App.closeDocument(doc.Name)
    transferred=[r for r in rows if r['subsystem']=='payload'and r['name']=='Transferred_3U']
    sled=[r for r in rows if r['subsystem'].startswith('sled')]
    cradle=[r for r in rows if r['subsystem'].startswith('cradle')]
    pallet=[r for r in rows if r['name']=='Captive_payload_pallet']
    def union(*groups):return list({r['name']:r for members in groups for r in members}.values())
    groups=dict(loaded_native_assembly=group(rows),dry_native_assembly=group([r for r in rows if r['subsystem']!='payload']),
        payload_total=group([r for r in rows if r['subsystem']=='payload']),moving_sled_hardware=group(sled),moving_cradle_hardware=group(cradle))
    if pallet:
        groups['carrier_pallet_hardware']=group(pallet)
        groups['cradle_structure_excluding_carrier_pallet']=group([r for r in cradle if r['name']!='Captive_payload_pallet'])
        groups['sled_structure_excluding_carrier_pallet']=group([r for r in sled if r['name']!='Captive_payload_pallet'])
        groups['cradle_plus_carrier_pallet']=group(union(cradle,pallet))
        groups['sled_plus_carrier_pallet']=group(union(sled,pallet))
    if transferred:
        groups['transferred_payload']=group(transferred)
        groups['sled_plus_transferred_payload']=group(sled+transferred)
        groups['cradle_plus_transferred_payload']=group(cradle+transferred)
        if pallet:
            groups['cradle_plus_carrier_pallet_plus_transferred_payload']=group(union(cradle,pallet,transferred))
            groups['sled_plus_carrier_pallet_plus_transferred_payload']=group(union(sled,pallet,transferred))
    subsystems={s:group([r for r in rows if r['subsystem']==s])for s in sorted({r['subsystem']for r in rows})}
    source_identity=dict(ledger_script_sha256=digest(Path(__file__).read_bytes()),native_FCStd_sha256=digest(native_raw),paired_BOM_json_sha256=digest(meta_raw),builder_sha256=d['builder_sha256'],parameters_sha256=d['parameters_sha256'])
    if step.exists():source_identity['paired_STEP_sha256']=digest(step.read_bytes())
    if a.source_manifest:
        manifest_raw=a.source_manifest.read_bytes();source_identity['source_manifest_sha256']=digest(manifest_raw)
        (a.snapshot/'MASS_LEDGER_SOURCE_MANIFEST.json').write_bytes(manifest_raw)
    assert meta_raw==meta.read_bytes()and native_raw==native.read_bytes()
    report=dict(configuration_id=d['configuration_id'],state=d['state'],requirement='GP-011',source_identity=source_identity,
        method='Native FreeCAD Shape.MatrixOfInertia about each shapeCG scaled by assigned_BOM_mass/native_volume*1e-6; full3x3 parallel-axis aggregation about each groupCG.',
        coordinate_system='Native CAD global axes: X travel, Y transverse, Z vertical. CG in m; inertia tensors in kg*m^2. Off-diagonal entries are inertia tensor entries, including their sign.',
        convention_check='Translated2x4x6mm box: native48mm3, inertia208/160/80mm5 aboutCG independent of translation; checked before final capture.',
        native_parts=len(objects),BOM_parts=len(bom),zero_assigned_mass_parts=[r['name']for r in rows if r['mass_kg']==0],
        groups=groups,subsystems=subsystems,parts=rows,
        boundaries=[
            'All native shape objects match one BOM part; all assigned masses are reported, including any zero values.',
            'Catalog and payload internal mass layouts are unknown; their assigned masses are distributed uniformly over their native envelope solids.',
            'The total is the modeled deployer assembly, excluding the separate500kg reference bus and7kg power/control mass allowance; no CG/inertia is assigned to unlocated allowances.',
            'Payload and pallet union groups are unique mathematical unions at the captured pose. They do not assert simultaneous attachment to both mechanisms. One named Captive_payload_pallet is sled_pallet in home/shot poses and cradle_pallet in lifted poses; lock hardware remains sled hardware.',
            'Material density, catalog mass and payload mass are design inputs; this is computed CAD mass propagation, not a measurement.'
        ])
    out=a.snapshot/'MASS_CG_INERTIA.json';out.write_text(json.dumps(report,indent=2)+'\n')
    (a.snapshot/'MASS_CG_INERTIA.sha256').write_text(digest(out.read_bytes())+'  MASS_CG_INERTIA.json\n')
    print(json.dumps(dict(state=d['state'],groups={k:{z:v for z,v in q.items()if z!='parts'}for k,q in groups.items()},zero_assigned_mass_parts=report['zero_assigned_mass_parts'],report_sha256=digest(out.read_bytes())),indent=2),flush=True)

if __name__=='__main__':main()
