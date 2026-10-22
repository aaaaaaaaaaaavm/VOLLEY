"""Common3U receiver and1U passive locator,nominal surrogate contact evidence."""
from pathlib import Path
import json,time
import build_comparison as b
H=Path(__file__).resolve().parent;O=H/'release'
records=[];started=time.perf_counter()
for cls,L,x in [('3U',340.5,0),('1U',113.5,227)]:
    pp=[q for q in b.shared_rail(0) if q['name'].startswith('Common_')]
    seated={q['name']:q for q in b.revised_parts('lead_screw',340.5,200,'seated')}
    for q in pp:
        if q['name'].startswith('Common_Receiver_clamp'):
            q['shape']=seated[q['name'][7:]]['shape'].copy()
        # During clamp capture the fork barriers are still engaged. Side
        # gates stay open until fork reset; closing them now intersects the
        # old FDR fork,so that invalid simultaneous pose is not commanded.
    pp.append(b.item('Passive_'+cls+'_payload',b.B((L,100,100),(x,0,22)),'payload','payload','Passive fixed surrogate envelope,no actual spacecraftICD approval'))
    if cls=='1U':pp.append(b.passive_insert(0))
    fork=b.revised_parts('lead_screw',340.5,200,'transfer')
    for q in fork:
        if q['name'] in ['Driven_fork_frame','Fork_front_barrier']:pp.append(q)
    contacts=[]
    for q in pp:
        if q['name'].startswith('Common_Receiver_clamp'):
            target='Passive_1U_227mm_insert' if cls=='1U' and '_5_' in q['name'] else 'Passive_'+cls+'_payload'
            contacts.append(b.pair(pp,q['name'],target))
    payload=next(q for q in pp if q['role']=='payload')
    leading=payload['shape'].BoundBox.XMax
    insert=next((q for q in pp if q['role']=='passive_insert'),None)
    rec={'class':cls,'satellite_length_mm':L,'satellite_X_min_mm':x,'satellite_leading_datum_X_mm':leading,
         'same_common_fork_width_mm':340.5,'same_common_clamp_X_mm':[5,327.5],
         'pose':'CLAMPS_CAPTURED_FORK_STILL_ENGAGED_SIDE_GATES_OPEN',
         'surrogate_clamp_contacts':contacts,
         'unresolved_intersections':b.old.audit(pp),
         'insert_mass_properties':None if insert is None else b.mass_props([insert]),
         'insert_to_satellite':None if insert is None else b.pair(pp,insert['name'],payload['name']),
         'native':b.native_export('Common_receiver_'+cls+'_insert_R1',pp),
         'axial_free_travel_each_direction_mm':2,
         'functional_acceptance':False,
         'open':['Dedicated insert must remain positively captive through release and empty return;lock not rated',
                 'Leading corner stop lift,lock,actuator and release sequence unaccepted',
                 'Contact surfaces are approved-design surrogates only;actual spacecraftICD pending',
                 'Thermal,tolerance,loaded contact and arbitrary-attitude custody unaccepted']}
    assert leading==340.5
    records.append(rec)
    print(cls,'insert/common receiver evidence complete',flush=True)
(O/'INSERT_INTERFACE.json').write_text(json.dumps({'revision':'FDR09-INSERT-R1','cases':records,
    'same_release_datum':True,'one_common_receiver':True,'insert_change_mechanism_required':False,
    'operating_concept':'Each1U has a dedicated passive locator in a3U outer feed package. Locator transfers with1U,remains captive in common receiver during satellite release,and returns to its dedicated cassette;no active onboard insert changer is assumed. This operating concept requires positive lock/return proof.',
    'elapsed_s':time.perf_counter()-started},indent=2)+'\n')
