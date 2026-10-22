"""Verify the restricted R5-to-R6 change; export native geometry and STEP."""
from pathlib import Path
import dataclasses
import hashlib
import importlib.util
import itertools
import json
import sys
import FreeCAD as App
import Part
from mechanism import shapes, cycle, State, REVISION

H = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('r5_reference', H/'reference_r5/mechanism.py')
old = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = old
spec.loader.exec_module(old)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
old_text = (H/'reference_r5/mechanism.py').read_text()
expected = old_text.replace('REVISION = "FM07-R5"', 'REVISION = "FM07-R6-CANDIDATE"').replace(
    'B((2, 82, 18), (L + 1 + xx, 10, 22))',
    'B((2, 82, 17.75), (L + 1 + xx, 10, 22.25))')
assert expected == (H/'mechanism.py').read_text(), 'Unexpected source changes'

def diff(a,b):
    v=a.common(b).Volume
    return abs(a.Volume-v)+abs(b.Volume-v)

records=[]
contact=[]
for size,L in [('1U',113.5),('3U',340.5)]:
    for name,state in cycle(L):
        if name not in ['exit_unlocked','exit_open','empty_carrier_home','exit_closed']:
            continue
        ss,meta=shapes(L,state)
        original,_=old.shapes(L,state)
        gate=ss['sled_front_stop']
        prior=original['sled_front_stop']
        removed=prior.cut(gate)
        assert gate.isValid() and len(gate.Solids)==1
        assert gate.cut(prior).Volume<1e-5
        assert abs(removed.Volume-41)<1e-5
        unchanged_errors={n:diff(ss[n],original[n]) for n in ss if n!='sled_front_stop'}
        assert max(unchanged_errors.values())<1e-5
        overlaps=[]
        for a,b in itertools.combinations(ss,2):
            if not ss[a].BoundBox.intersect(ss[b].BoundBox):continue
            v=ss[a].common(ss[b]).Volume
            if v>1e-5:overlaps.append(dict(a=a,b=b,intersection_mm3=v))
        assert not overlaps, overlaps
        doc=App.newDocument('R6')
        for n,shape in ss.items():
            ob=doc.addObject('Part::Feature','Component');ob.Label=n;ob.Shape=shape
        doc.Label='VOLLEY '+REVISION+' '+size+' '+name
        doc.recompute()
        p=H/'cad'/('FM07_R6_'+size+'_'+name+'.FCStd');p.parent.mkdir(exist_ok=True)
        doc.saveAs(str(p));step=p.with_suffix('.step');Part.export(doc.Objects,str(step))
        q=Part.read(str(step))
        volume=sum(s.Volume for s in ss.values())
        assert q.isValid() and len(q.Solids)==len(ss) and abs(q.Volume-volume)<0.001
        if name=='exit_unlocked':
            part=H/'cad'/('FM07_R6_'+size+'_exit_gate.step');gate.exportStep(str(part))
            records.append(dict(kind='part',size=size,file=part.relative_to(H).as_posix(),
                                volume_mm3=gate.Volume,solids=1,sha256=sha(part)))
        records.append(dict(kind='assembly',size=size,pose=name,components=len(ss),
                            source_volume_mm3=volume,removed_volume_mm3=removed.Volume,
                            removed_material_mass_kg=removed.Volume*1e-9*7850,
                            removed_CG_mm=[sum(s.Volume*getattr(s.CenterOfMass,k) for s in removed.Solids)/removed.Volume for k in ['x','y','z']],
                            subset_verified=True,max_unchanged_part_difference_mm3=max(unchanged_errors.values()),
                            pair_intersections=overlaps,
                            files={f.relative_to(H).as_posix():sha(f) for f in [p,step]}))
        App.closeDocument(doc.Name)
    for angle in [0,.01,.05,.1,.25,.5,.6,1,2,5]:
        st=State(receiver=0,payload_feed=200,sled=80,exit_pin_withdraw=22,exit_gate_deg=angle)
        ss,_=shapes(L,st);oo,_=old.shapes(L,st)
        contact.append(dict(size=size,angle_deg=angle,
                            r5_gap_mm=oo['sled_front_stop'].distToShape(oo['sled_body'])[0],
                            r6_gap_mm=ss['sled_front_stop'].distToShape(ss['sled_body'])[0],
                            r5_intersection_mm3=oo['sled_front_stop'].common(oo['sled_body']).Volume,
                            r6_intersection_mm3=ss['sled_front_stop'].common(ss['sled_body']).Volume))
    print(size,'native delta/export checked',flush=True)
out=dict(revision=REVISION,source_change_whitelist_verified=True,
         source_sha256={str(p.relative_to(H)):sha(p) for p in [H/'mechanism.py',H/'reference_r5/mechanism.py',Path(__file__)]},
         software=dict(FreeCAD=list(App.Version()),OCC=Part.OCC_VERSION),
         records=records,contact_comparison=contact,
         boundary='Nominal rigid geometry. Material removal preserves previous nonpenetration under unchanged motions; no load, tolerance, actuator or D27 acceptance. Density-based mass delta is not an installed-system mass.')
(H/'DELTA_AND_EXPORT.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS:',len([r for r in records if r['kind']=='assembly']),'assemblies, 2 gate parts')
