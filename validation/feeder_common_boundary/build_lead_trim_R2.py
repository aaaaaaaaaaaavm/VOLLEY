"""Smallest shared protrusion trim on the lead reference;no support acceptance."""
from pathlib import Path
import json,time,hashlib
import build_comparison as b
H=Path(__file__).resolve().parent;O=H/'release';started=time.perf_counter()
baseline=b.inventory('lead_screw');current=[{**q,'shape':q['shape'].copy()} for q in baseline]
cells={'A_1U':(0,False),'B_3U':(250,True),'C_1U':(650,False),'D_3U':(900,True)}
changes=[]
for q in current:
    if '__' not in q['name']:continue
    cell,name=q['name'].split('__',1);x,north=cells[cell]
    oldvol=q['shape'].Volume
    if name.startswith('Guide_shaft_') or name=='Power_off_capture_rack':
        box=b.B((4000,2000,2000),(-1000,110 if north else -2010,-1000))
        q['shape']=q['shape'].common(box).removeSplitter()
    elif name=='Tr8x2_screw_blank':
        box=b.B((4000,2000,2000),(-1000,101 if north else -2001,-1000))
        q['shape']=q['shape'].common(box).removeSplitter()
    elif name=='Screw_end_bearing_-10':
        q['shape'].translate(b.V(0,1 if north else -1,0))
    elif name=='Driven_fork_frame':
        # Guide cheeks added inR1 intruded into the existing8mm bearing seat.
        # Reopen that nominal seat;do not waive the16.176779mm3 interference.
        seat=b.old.cyl(8,18,(-62,-229,52))
        if north:seat.rotate(b.V(170.25,50,0),b.V(0,0,1),180)
        seat.translate(b.V(x,0,0))
        q['shape']=q['shape'].cut(seat).removeSplitter()
        assert len(q['shape'].Solids)==1
    else:continue
    assert q['shape'].isValid() and q['shape'].Volume>0
    changes.append({'part':q['name'],'old_volume_mm3':oldvol,'new_volume_mm3':q['shape'].Volume,
                    'material':q['material'],'mass_delta_kg':(q['shape'].Volume-oldvol)*b.DENSITY[q['material']]})

def sweep_hits(items):
    sweep=b.B((1240.5,100,100),(0,0,22));hits=[]
    for q in items:
        if q['name'].startswith('Common_'):continue
        if not sweep.BoundBox.intersect(q['shape'].BoundBox):continue
        v=sweep.common(q['shape']).Volume
        if v>1e-5:hits.append({'part':q['name'],'penetration_mm3':v,'material':q['material']})
    return hits

checks=[]
for u in [0,100,200]:
    pp=b.revised_parts('lead_screw',340.5,u,'transfer',True)
    nn={q['name']:q for q in pp}
    # Apply the same local trims to the native local contact check.
    for name in ['Guide_shaft_-34','Guide_shaft_-62','Power_off_capture_rack']:
        nn[name]['shape']=nn[name]['shape'].common(b.B((2000,1990,2000),(-1000,-2000,-1000))).removeSplitter()
    nn['Tr8x2_screw_blank']['shape']=b.old.cyl(4,439,(-48,-440,84))
    nn['Screw_end_bearing_-10']['shape'].translate(b.V(0,-1,0))
    nn['Driven_fork_frame']['shape']=nn['Driven_fork_frame']['shape'].cut(b.old.cyl(8,18,(-62,-229+u,52))).removeSplitter()
    checks.append({'feed_mm':u,'guide_bearing_axial_span_mm':[-229+u,-211+u],
         'guide_shaft_span_mm':[-440,-10],
         'guide_bearing_axial_overlap_mm':18,
         'guide_end_margin_at_this_position_mm':-10-(-211+u),
         'pawl_rack':b.pair(pp,'Spring_applied_pawl','Power_off_capture_rack'),
         'guide_bearing_housing':b.pair(pp,'Driven_fork_frame','Guide_bearing_-62'),
         'screw_front_bearing':b.pair(pp,'Tr8x2_screw_blank','Screw_end_bearing_-10'),
         'screw_front_bearing_axial_span_mm':[-11,-1],
         'screw_blank_span_mm':[-440,-1],
         'screw_front_bearing_axial_overlap_mm':10,
         'support_rating_accepted':False})
before=sweep_hits(baseline);after=sweep_hits(current)
native=b.native_export('lead_screw_four_carrier_trim_R2',current)
report={'revision':'FDR09-LEAD-TRIM-R2','reference_revision':'FDR09-R1-2026-10-22',
        'changes':changes,'guide_and_capture_rack_length_before_mm':450,
        'guide_and_capture_rack_length_after_mm':430,
        'screw_blank_length_before_mm':450,'screw_blank_length_after_mm':439,
        'front_screw_bearing_shift_toward_storage_mm':1,
        'guide_bearing_seat_relief':'Reopen8mm nominal bearing seat through added guide cheeks;R1 interference16.176779mm3 is retained inR1 evidence and removed only inR2.',
        'fullrail_payload_sweep_before':before,'fullrail_payload_sweep_after':after,
        'exact_nominal_payload_sweep_pass':not after,'feed_end_support_checks':checks,
        'material_properties':b.mass_props(current),'native':native,
        'not_accepted':['Screw/front bearing radial0.25mm clearance remains a modeled support gap;no actual rolling elements,rated bearing,housing or retained axial load path supplied.',
          'Guide end margin1mm at full feed is nominal only;rail retention,loaded deflection and tolerance are unqualified.',
          'This check clears the payload rectangular corridor only;full receiver carriage,actuator,gates,docking and tolerance sweeps remain open.',
          'All mandatory loaded/fault/return-custody/installed boundary gates remain failed/open;no selected architecture.',
          'Catalog10x2/SB3700 actuator option still does not matchTr8 nominal CAD;R2 is not an installed purchased actuator acceptance.'],
        'all_mandatory_acceptance_gates_pass':False,'elapsed_s':time.perf_counter()-started}
assert len(before)==8 and len(after)==0
assert all(c['pawl_rack']['distance_mm']<1e-5 and c['pawl_rack']['penetration_mm3']<1e-5 for c in checks)
assert all(c['guide_bearing_housing']['penetration_mm3']<1e-5 for c in checks)
(O/'LEAD_TRIM_R2.json').write_text(json.dumps(report,indent=2)+'\n')
print('R2 exact payload hits',len(before),'->',len(after),'elapsed',report['elapsed_s'],flush=True)
