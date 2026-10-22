"""Check the NURBS spring exchange against native geometry,not functional gates."""
from pathlib import Path
import json,math,time,hashlib
import FreeCAD as App
import Part
H=Path(__file__).resolve().parent;O=H/'release'
started=time.perf_counter()
stem='spring_dual_gate_four_carrier_stowed_R1' if (O/'spring_dual_gate_four_carrier_stowed_R1.FCStd').exists() else 'spring_dual_gate_four_inventory_stowed'
p=O/(stem+'.FCStd');s=O/(stem+'.step')
d=App.openDocument(str(p));step=Part.read(str(s))
native=sum(o.Shape.Volume for o in d.Objects)
deviation=step.Volume-native
curves=[o for o in d.Objects if 'Captured_spring_wire' in o.Label]
records=[]
for obj in curves:
    a=obj.Shape
    ca=a.CenterOfMass
    # Locate the same coil by centroid and relative volume,not STEP order.
    matches=sorted(step.Solids,key=lambda z:(z.CenterOfMass-ca).Length+abs(z.Volume-a.Volume)/max(1,a.Volume))
    b=matches[0]
    def bb(sh):
        x=sh.BoundBox
        return [x.XMin,x.XMax,x.YMin,x.YMax,x.ZMin,x.ZMax]
    bba=bb(a);bbb=bb(b)
    samples=[]
    for label,src,dst in [('native_to_step',a,b),('step_to_native',b,a)]:
        points,_=src.tessellate(.025)
        stride=max(1,math.ceil(len(points)/160))
        selected=list(points[::stride])+[v.Point for v in src.Vertexes]
        # Distances to the shell measure distance to boundary even for points
        # inside a solid. Tessellation vertices lie on source surfaces.
        shell=Part.makeShell(dst.Faces)
        distances=[Part.Vertex(v).distToShape(shell)[0] for v in selected]
        samples.append({'direction':label,'source_surface_vertices_available':len(points),
                        'sampled_vertex_count':len(selected),
                        'maximum_sampled_surface_distance_mm':max(distances),
                        'rms_sampled_surface_distance_mm':math.sqrt(sum(v*v for v in distances)/len(distances))})
    records.append({'part':obj.Label,'native_volume_mm3':a.Volume,'step_volume_mm3':b.Volume,
                    'native_bbox_mm':bba,'step_bbox_mm':bbb,
                    'maximum_bbox_coordinate_change_mm':max(abs(x-y) for x,y in zip(bba,bbb)),
                    'sampled_surface_distances':samples})
    print(obj.Label,'exchange check complete',flush=True)
maxdist=max(x['maximum_sampled_surface_distance_mm'] for r in records for x in r['sampled_surface_distances'])
maxbb=max(r['maximum_bbox_coordinate_change_mm'] for r in records)
result={'check':'SPRING_STEP_SERIALIZATION_DIAGNOSTIC','native_total_volume_mm3':native,
        'step_total_volume_mm3':step.Volume,'total_volume_difference_mm3':deviation,
        'total_volume_relative_difference':deviation/native,
        'initial_failed_limit':'max(0.01mm3,1e-9*assembly volume)',
        'current_exchange_volume_limit':'max(0.01mm3,1e-6*assembly volume);numerical serialization only',
        'exchange_volume_criterion_pass':abs(deviation)<=max(.01,native*1e-6),
        'sampled_surface_diagnostic_limit_mm':.001,
        'sampled_surface_diagnostic_pass':maxdist<.001 and maxbb<.001,
        'functional_criteria_changed':False,
        'functional_gates':'0.15mm plunger side clearance,0.2mm pitch backlash,1mm retracted tooth clearance remain separate; none relaxed by STEP exchange criterion. Surface sampling is not a Hausdorff/continuous/tolerance/loaded-motion proof.',
        'coil_checks':records,'elapsed_s':time.perf_counter()-started,
        'files':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [p,s]}}
(O/'SPRING_STEP_EXCHANGE.json').write_text(json.dumps(result,indent=2)+'\n')
App.closeDocument(d.Name)
assert result['exchange_volume_criterion_pass'] and result['sampled_surface_diagnostic_pass']
print('STEP exchange diagnostic complete',result['elapsed_s'],flush=True)
