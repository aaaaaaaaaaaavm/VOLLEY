"""FDR09 local four-inventory comparison and explicit connection corrections.

Run with PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3 build_comparison.py
This is a local design study, not a flight or manufacturing release.
"""
from pathlib import Path
import sys, json, math, hashlib, time, itertools
import FreeCAD as App
import Part

H = Path(__file__).resolve().parent
sys.path.insert(0, str(H / 'source'))
import fdr08 as old
O = H / 'release'
O.mkdir(exist_ok=True)
V = App.Vector
B = old.block
DENSITY = old.DENSITY
REV = 'FDR09-R1-2026-10-22'
RAIL_CACHE = {}
PART_CACHE = {}


def revised_parts(candidate, L, u=0, phase='stowed', applied=None):
    """Replace the disconnected block with a guided, retractable arrest plunger.

    At stowed tooth gap -219..-218 the 0.8mm finger has 0.2mm forward
    backlash. Its lower face touches the rack root at Z31. The head stays
    clear of the rack teeth and a pocket removes its former fork overlap.
    Applied positions are only legitimate at the 2mm tooth pitch; arbitrary
    transfer positions keep it retracted. Spring and release actuator open.
    """
    key=(candidate,L,u,phase,applied)
    if key in PART_CACHE:
        return [{**q,'shape':q['shape'].copy()} for q in PART_CACHE[key]]
    p = old.parts(candidate, L, u, phase)
    names = {q['name']: q for q in p}
    if applied is None:
        applied = phase in ('stowed', 'reset', 'seated')
    fu = 0 if phase == 'seated' else u
    # The old seated pose resets the fork to home. Follow its datum explicitly.
    py = -219 + fu
    lift = 0 if applied else 4
    finger = B((8, .8, 3), (-60, py, 31 + lift))
    head = B((8, 3, 6), (-60, py - 1, 34 + lift))
    pawl = finger.fuse(head).removeSplitter()
    names['Spring_applied_pawl']['shape'] = pawl
    names['Spring_applied_pawl']['contact'] = (
        'FDR09 guided tooth-gap plunger, nominal applied contact; '
        'return spring, release actuator, preload, tooth strength and joint proof open'
    )
    frame = names['Driven_fork_frame']['shape']
    # Two guide cheeks extend the connected bearing housing. A 0.15mm
    # nominal side clearance is provided on the full 4mm lift envelope.
    cheeks = [B((2.85, 6, 11), (-63, py-2.5, 34)),
              B((2.85, 6, 11), (-51.85, py-2.5, 34))]
    frame = frame.multiFuse(cheeks).removeSplitter()
    guide_pocket = B((8.3, 3.3, 10.3), (-60.15, py-1.15, 33.85))
    frame = frame.cut(guide_pocket).removeSplitter()
    # Nominal side attachment pads establish a geometric drive contact.
    # Fasteners, seats/preload and load qualification remain required.
    if candidate == 'rack_pawl':
        pad = B((17, 12, 14), (-39, -228+fu, 66))
        frame = frame.fuse(pad).removeSplitter()
        names['Index_pinion_blank']['shape'].translate(V(0, 0, -1))
        names['Index_pinion_blank']['contact'] = 'Nominal tangent to tooth crest; involute mesh and bearings unresolved'
    if candidate == 'belt_shuttle':
        pad = B((18, 12, 6), (-40, -226+fu, 96))
        frame = frame.fuse(pad).removeSplitter()
    if candidate == 'telescopic':
        # Three nested tubes have TWO sliding interfaces. Their translations
        # are0,u/2,u; the old0,u/3,2u/3 lost one third of the commanded stroke.
        for i in range(3):
            names['Nested_stage_'+str(i)]['shape'].translate(V(0,i*fu/6,0))
        pad=B((20,12,18),(-42,-224+fu,66))
        frame=frame.fuse(pad).removeSplitter()
    assert frame.isValid() and len(frame.Solids) == 1, (candidate, len(frame.Solids))
    names['Driven_fork_frame']['shape'] = frame
    names['Driven_fork_frame']['contact'] += '; FDR09 integral plunger guide and architecture connection pads'
    for q in p:
        assert q['shape'].isValid() and q['shape'].Volume > 0, q['name']
    PART_CACHE[key]=[{**q,'shape':q['shape'].copy()} for q in p]
    return p


def mass_props(items):
    solids = []
    for q in items:
        rho = DENSITY[q['material']]
        if rho <= 0:
            continue
        for s in q['shape'].Solids:
            c = s.CenterOfMass
            solids.append((s, rho, rho*s.Volume, [c.x, c.y, c.z]))
    mass = sum(s[2] for s in solids)
    cg = [sum(s[2]*s[3][j] for s in solids)/mass for j in range(3)]
    inertia = [[0.]*3 for _ in range(3)]
    for s, rho, m, c in solids:
        mat=s.MatrixOfInertia
        d=[c[j]-cg[j] for j in range(3)];d2=sum(v*v for v in d)
        for i in range(3):
            for j in range(3):
                inertia[i][j] += (getattr(mat, 'A'+str(i+1)+str(j+1))*rho +
                    m*((d2 if i==j else 0)-d[i]*d[j]))*1e-6
    bb=items[0]['shape'].BoundBox
    for q in items[1:]:bb.add(q['shape'].BoundBox)
    return {'modeled_material_mass_kg':mass,'modeled_material_CG_mm':cg,
            'modeled_material_inertia_CG_kg_m2':inertia,
            'all_geometry_bounds_mm':[bb.XMin,bb.XMax,bb.YMin,bb.YMax,bb.ZMin,bb.ZMax],
            'all_geometry_box_litre':bb.XLength*bb.YLength*bb.ZLength/1e6}


def pair(items, a, b):
    nn={q['name']:q for q in items}
    sa=nn[a]['shape'];sb=nn[b]['shape']
    d=sa.distToShape(sb)[0]
    vol=sa.common(sb).Volume if sa.BoundBox.intersect(sb.BoundBox) else 0.
    return {'a':a,'b':b,'distance_mm':d,'penetration_mm3':vol,
            'status':'INTERFERENCE' if vol>1e-5 else ('CONTACT_ONLY_JOINT_UNPROVEN' if d<1e-5 else 'GAP')}


def native_export(stem, items):
    doc=App.newDocument(stem)
    rows=[]
    for i,q in enumerate(items):
        o=doc.addObject('Part::Feature','P'+str(i));o.Label=q['name'];o.Shape=q['shape']
        o.addProperty('App::PropertyString','MaterialBasis');o.MaterialBasis=q['material']
        o.addProperty('App::PropertyString','EvidenceBoundary');o.EvidenceBoundary=q.get('contact','')
        o.addProperty('App::PropertyString','Role');o.Role=q['role']
        rows.append({'name':q['name'],'role':q['role'],'material':q['material'],
                     'volume_mm3':q['shape'].Volume,
                     'modeled_material_mass_kg':q['shape'].Volume*DENSITY[q['material']],
                     'catalog_id':None,'catalog_mass_kg':None,
                     'mass_status':'UNCATALOGUED_NOT_ZERO' if q['material']=='envelope' else
                                   ('PAYLOAD_EXCLUDED' if q['material']=='payload' else 'CAD_DENSITY_ESTIMATE')})
    doc.recompute()
    paths=[O/(stem+'.FCStd'), O/(stem+'.step')]
    doc.saveAs(str(paths[0]));Part.export(doc.Objects,str(paths[1]))
    read=Part.read(str(paths[1]));assert read.isValid()
    vol0=sum(q['shape'].Volume for q in items)
    # STEP conversion of the helical NURBS spring changes volume at ~3e-8
    # relative; retain measured error against an explicit1ppm criterion.
    assert abs(read.Volume-vol0)<max(.01,vol0*1e-6),(stem,read.Volume,vol0)
    App.closeDocument(doc.Name)
    return {'stem':stem,'part_count':len(items),'step_solid_count':len(read.Solids),
            'step_valid':True,'step_volume_error_mm3':read.Volume-vol0,
            'BOM':rows,'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}


def item(name, shape, material='aluminium', role='fixed', contact='Custom geometry; fasteners/load/flight qualification open'):
    return {'name':name,'shape':shape,'material':material,'role':role,'contact':contact}


def passive_insert(y=-200):
    # Lightweight passive227mm spacer. Four longitudinal members transmit
    # load between common aft stop and1U surrogate corner pads. It stays
    # with the dedicated cell/1U package; it is not an orbital interchangeable
    # receiver insert. Positive lock and empty return still need acceptance.
    pieces=[]
    for yy in [y,y+92]:
        for zz in [22,114]:pieces.append(B((227,8,8),(0,yy,zz)))
    for xx in [0,223]:
        for zz in [22,118]:pieces.append(B((4,100,4),(xx,y,zz)))
        for yy in [y,y+96]:pieces.append(B((4,4,100),(xx,yy,22)))
    s=pieces[0].multiFuse(pieces[1:]).removeSplitter()
    assert s.isValid() and len(s.Solids)==1
    return item('Passive_1U_227mm_insert',s,role='passive_insert',
                contact='CustomAl surrogate-corner locator;1U leading faceX340.5,insert transfers/returns with dedicated1U;lock/load/ICD approval open')


def shared_rail(dock_x=0):
    """BB64 full rail integration geometry; not an extension of FM07 acceptance.

    Receiver docking positions0,250,650,900mm; total commanded travel900mm.
    Rails extend-150..1450mm to carry the3U sled at all positions.
    """
    if dock_x in RAIL_CACHE:
        return [{**q,'shape':q['shape'].copy()} for q in RAIL_CACHE[dock_x]]
    pp=[]
    for q in revised_parts('lead_screw',340.5,0,'stowed'):
        if q['name'].startswith(('Receiving_sled_floor','Receiver_side_gate','Receiver_clamp_')):
            q=dict(q);q['shape']=q['shape'].copy()
            if q['name']=='Receiving_sled_floor':q['shape']=B((364.5,110,4),(-12,-5,18))
            q['shape'].translate(V(dock_x,0,0));q['name']='Common_'+q['name'];q['cell_id']='common_receiver';pp.append(q)
    pp.append(item('Common_north_side_gate',B((364.5,2,108),(dock_x-12,102,142)),role='gate'))
    # Common longitudinal release/capture datum. The leading corner stops
    # retract vertically for release; aft stops are permanent. Both formats
    # have the same340.5mm outer feed package through their passive spacer.
    for side,xx in [('aft',-6),('leading',342.5)]:
        pieces=[B((4,104,4),(dock_x+xx,-2,22))]
        for yy in [0,92]:
            pieces.append(B((4,8,104),(dock_x+xx,yy,26)))
        s=pieces[0].multiFuse(pieces[1:]).removeSplitter()
        pp.append(item('Common_'+side+'_corner_stop',s,role='receiver' if side=='aft' else 'gate',
                       contact='Surrogate rail-corner end stop;2mm nominal axial clearance;leading stop release lift actuator/lock/rating open'))
    # The carriage end beams and guide housings are fused as one native solid.
    frame=B((364.5,110,4),(dock_x-12,-5,18))
    for xx in [dock_x-12,dock_x+328.5]:
        frame=frame.fuse(B((24,158,4),(xx,-29,14)))
        for yy in [-20,120]:
            shoe=B((24,18,16),(xx,yy-9,2)).cut(old.cyl(4.2,24,(xx,yy,10),(1,0,0)))
            frame=frame.fuse(shoe)
    # Dock tab and pin/guide clearance are represented rather than leaving
    # the old27mm stop-to-carriage disconnect.
    tab=B((16,35,4),(dock_x-20,127,14)).cut(old.cyl(2.1,4,(dock_x-12,156,14),(0,0,1)))
    frame=frame.fuse(tab)
    frame=frame.removeSplitter()
    assert len(frame.Solids)==1 and frame.isValid()
    pp=[q for q in pp if q['name']!='Common_Receiving_sled_floor']
    pp.append(item('Common_receiver_floor_carriage',frame,role='receiver'))
    for yy in [-20,120]:
        pp.append(item('Full_rail_shaft_'+str(yy),old.cyl(4,1600,(-150,yy,10),(1,0,0)),'steel'))
        for xx in [-150,250,650,1050,1438]:
            pp.append(item('Rail_mount_'+str(yy)+'_'+str(xx),B((12,12,6),(xx,yy-6,0))))
    # A full length independently arrestable rack is represented. Its own
    # actuated plunger, wiring, rating and positive docking function are open.
    rackcache=O/'full_rail_rack.brep'
    if rackcache.exists():
        rack=Part.Shape();rack.read(str(rackcache))
    elif (O/'lead_screw_four_inventory_stowed.FCStd').exists():
        d=App.openDocument(str(O/'lead_screw_four_inventory_stowed.FCStd'))
        rack=next(q.Shape.copy() for q in d.Objects if q.Label=='Full_rail_arrest_rack')
        App.closeDocument(d.Name);rack.exportBrep(str(rackcache))
    else:
        chunks=[]
        for start in range(0,1600,100):
            chunk=B((100,8,5),(-150+start,140,6))
            chunk=chunk.multiFuse([B((1,8,3),(-150+j,140,11)) for j in range(start,start+100,2)]).removeSplitter()
            chunks.append(chunk)
        rack=chunks[0].multiFuse(chunks[1:]).removeSplitter()
        rack.exportBrep(str(rackcache))
    pp.append(item('Full_rail_arrest_rack',rack,'steel'))
    for xx in [0,250,650,900]:
        mount=B((12,12,7.8),(xx-18,150,6)).cut(old.cyl(2.15,7.8,(xx-12,156,6),(0,0,1)))
        pp.append(item('Dock_stop_mount_'+str(xx),mount))
        # Retracted at unselected docks; extended at selected dock only.
        zz=6 if xx==dock_x else -6
        pp.append(item('Dock_pin_'+str(xx),old.cyl(2,16,(xx-12,156,zz),(0,0,1)),'steel','docking',
                       'Nominal pin envelope; deployment/seat/backlash/sensing not established'))
    # Long axis positioning uses a belt envelope; two custom pulley blanks
    # and source-sized motor+gear are sized in ACTUATOR_SCREEN.json.
    for xx in [-130,1430]:
        pp.append(item('Full_rail_pulley_'+str(xx),old.cyl(12,8,(xx,-44,10),(0,0,1))))
    for yy in [-56,-32]:
        pp.append(item('Full_rail_belt_'+str(yy),B((1560,1.5,8),(-130,yy,6)),'polymer','drive'))
    pp.append(item('Full_rail_drive_envelope',B((90,40,40),(-220,-64,14)),'envelope','unselected_actuator'))
    RAIL_CACHE[dock_x]=[{**q,'shape':q['shape'].copy()} for q in pp]
    return pp


def inventory(candidate):
    if candidate == 'indexed_drum':
        p=revised_parts(candidate,340.5,0,'stowed')
        p=[q for q in p if not q['name'].startswith(('Receiving_sled_floor','Receiver_side_gate','Receiver_clamp_'))]
        p.extend(q for q in shared_rail(0) if q['name'].startswith('Common_'))
        # All drum cells use the same3U outer carrier interface,with two
        # passive1U spacers. Rebuild the two former short cells explicitly.
        p=[q for q in p if not q['name'].startswith(('Other_cell_1_','Other_cell_3_'))]
        for i in [1,3]:
            module=revised_parts('lead_screw',340.5,0,'stowed')
            for q in module:
                if not q['name'].startswith(('Passive_payload','Cassette_','Stored_side_cap','Storage_gate')):continue
                q=dict(q)
                if q['material']=='payload':q['shape']=B((113.5,100,100),(227,-200,22))
                else:q['shape']=q['shape'].copy()
                q['shape'].rotate(V(0,-150,350),V(1,0,0),i*90)
                q['name']='Other_cell_'+str(i)+'_'+q['name'];p.append(q)
            q=passive_insert();q['shape'].rotate(V(0,-150,350),V(1,0,0),i*90)
            q['name']='Other_cell_'+str(i)+'_'+q['name'];p.append(q)
        for q in p:q['cell_id']='drum_shared' if not q['name'].startswith('Other_cell') else q['name'].split('_')[2]
        return p
    # Four fixed cassettes on opposite Y sides of the common X rail. North
    # cells rotate about their own longitudinal midpoint and common feed
    # centerY50; both sides deliver the passive payload toY0..100,Z22..122.
    cells=[('A_1U',113.5,0,False),('B_3U',340.5,250,True),
           ('C_1U',113.5,650,False),('D_3U',340.5,900,True)]
    pp=shared_rail(0)
    for name,L,x,flip in cells:
        module=revised_parts(candidate,340.5,0,'stowed')
        if L<200:
            for q in module:
                if q['material']=='payload':q['shape']=B((113.5,100,100),(227,-200,22))
            module.append(passive_insert())
        for q in module:
            if q['name'].startswith(('Receiving_sled_floor','Receiver_side_gate','Receiver_clamp_')):continue
            q=dict(q);s=q['shape'].copy()
            if flip:s.rotate(V(340.5/2,50,0),V(0,0,1),180)
            s.translate(V(x,0,0));q['shape']=s;q['name']=name+'__'+q['name'];q['cell_id']=name
            pp.append(q)
        for mx in [-12,340.5]:
            s=B((12,10,16),(mx,-210,0))
            if flip:s.rotate(V(340.5/2,50,0),V(0,0,1),180)
            s.translate(V(x,0,0));q=item(name+'__Cassette_mount_'+str(mx),s);q['cell_id']=name;pp.append(q)
    return pp


def connection_review(candidate):
    records=[]
    pairs=[('Driven_fork_frame','Guide_bearing_-34'),('Driven_fork_frame','Guide_bearing_-62'),
           ('Spring_applied_pawl','Power_off_capture_rack'),('Spring_applied_pawl','Driven_fork_frame')]
    if candidate=='lead_screw':pairs += [('Driven_fork_frame','Tr8_nut_blank')]
    if candidate=='rack_pawl':pairs += [('Driven_fork_frame','Driven_rack'),('Index_pinion_blank','Driven_rack')]
    if candidate=='belt_shuttle':pairs += [('Driven_fork_frame','Belt_carriage_clamp')]
    if candidate=='pantograph':pairs += [('Driven_fork_frame','Scissor_-110_2A'),('Driven_fork_frame','Scissor_-110_2B')]
    if candidate=='telescopic':pairs += [('Driven_fork_frame','Nested_stage_2'),('Nested_stage_0','Nested_stage_1'),('Nested_stage_1','Nested_stage_2')]
    if candidate=='spring_dual_gate':pairs += [('Driven_fork_frame','Captured_spring_wire')]
    for u,phase in [(0,'stowed'),(0,'transfer'),(25,'transfer'),(100,'transfer'),(175,'transfer'),(200,'transfer'),(200,'seated')]:
        pp=revised_parts(candidate,340.5,u,phase)
        records.append({'advance_mm':u,'phase':phase,'connections':[pair(pp,a,b) for a,b in pairs],
                        'unresolved_intersections':old.audit(pp)})
    # Jam/power-loss geometry: nearest following available gap, up to one
    # pitch later. It assumes the commanded plunger actually drops; it does
    # not assert release latency, return spring performance or dynamic arrest.
    fault=[]
    for u in [0,25,50,75,100,125,150,175,200]:
        snap=2*math.ceil(u/2)
        pp=revised_parts('lead_screw',340.5,snap,'transfer',True)
        fault.append({'fault_advance_mm':u,'applied_advance_mm':snap,
                      'pitch_only_extra_travel_mm':snap-u,
                      'pawl_rack':pair(pp,'Spring_applied_pawl','Power_off_capture_rack'),
                      'pawl_fork':pair(pp,'Spring_applied_pawl','Driven_fork_frame'),
                      'dynamic_or_hardware_acceptance':False})
    return {'nominal_stations':records,'power_loss_applied_geometry':fault,
            'continuous_motion_proven':False,'tolerance_loaded_fault_proven':False}


def main():
    started=time.perf_counter();out=[]
    selected=old.CANDIDATES
    if '--candidate' in sys.argv:
        selected=[sys.argv[sys.argv.index('--candidate')+1]]
        assert selected[0] in old.CANDIDATES
    for c in selected:
        previous=O/(c+'_carrier_R1_comparison.json')
        if previous.exists() and '--force' not in sys.argv:
            out.append(json.loads(previous.read_text()))
            print(c,'resumed completed evidence',flush=True)
            continue
        t=time.perf_counter();pp=inventory(c)
        payloads=[q for q in pp if q['material']=='payload']
        lengths=sorted(round(q['shape'].Volume/10000,5) for q in payloads)
        assert lengths==[113.5,113.5,340.5,340.5],(c,lengths)
        row={'candidate':c,'payload_manifest':{'1U':2,'3U':2},
             'payload_nominal_total_kg':10.66,'payload_upper_study_total_kg':16.0,
             'storage_cells':4,'receiving_ports_modeled':1,
             'local_feed_stations':1 if c=='indexed_drum' else 4,
             'rail_dock_positions_mm':[] if c=='indexed_drum' else [0,250,650,900],
             'full_rail_commanded_travel_mm':0 if c=='indexed_drum' else 900,
             'BB64_full_rail_integration_acceptance':False,
             'installed_boundary_complete':False,
             'boundary_status':'FOUR_CELLS_ONE_RECEIVER_MODELED_INSTALLED_COMPLETENESS_OPEN',
             'installed_mass_kg':None,'installed_CG_mm':None,'installed_inertia_kg_m2':None,
             'geometry_revision':REV,
             **mass_props(pp),**native_export(c+'_four_carrier_stowed_R1',pp)}
        print(c,'native four inventory complete',round(time.perf_counter()-t,2),flush=True)
        row['connection_motion_review']=connection_review(c)
        out.append(row)
        (O/(c+'_carrier_R1_comparison.json')).write_text(json.dumps(row,indent=2)+'\n')
        print(c,'evidence complete',round(time.perf_counter()-t,2),flush=True)
    if '--candidate' in sys.argv:
        return
    report={'revision':REV,'source_revision':'FDR08','software':{'FreeCAD':'.'.join(App.Version()[:3]),'OCC':Part.OCC_VERSION},
            'coordinate_units':'mm; mass kg; inertia kg m2',
            'comparison_boundary':'Four independently housed passive payloads,2x1U+2x3U,one common reusable receiver. Six fixed-cell concepts have four local feeds and a shared900mm-travel receiver on1600mm rails; indexed drum has four cells and one extraction port. Native custom-material subtotal includes represented storage/capture/transfer/receiver/rail/dock/mount geometry. Full installed boundary additionally requires complete actuators, transmissions, joints, fasteners, sensors, harness and control/power. Unmodeled mass is null.',
            'density_basis_kg_mm3':DENSITY,
            'important_limitation':'The new full rail/docking geometry is BB64 integration work,not an FM07 coupon qualification. Longitudinal positioning drive/clamp,full-motion tolerance and rated docking are unaccepted. Drum extraction transmission and index connection are absent. No complete installed mass or acceptance claim.',
            'changes':['Guided plunger tooth finger gives applied rack root/flank contact;4mm release lift instead of a permanent1mm disconnect.',
                       'Pawl guide pocket removes old pawl/fork positive-volume collision.',
                       'Rack/fork integral side pad closes geometric drive gap; pinion lowered1mm to tangent.',
                       'Belt clamp/fork integral side pad closes geometric drive gap.',
                       'Telescopic stage law corrected from0,u/3,2u/3 to0,u/2,u for200mm output;20mm minimum nominal overlap. Integral side pad contacts inner tube. Synchronization/stop/bearing loads remain open.'],
            'cases':out,'elapsed_s':time.perf_counter()-started,
            'no_downselect':True,'selected_architecture':None}
    (O/'COMPARISON.json').write_text(json.dumps(report,indent=2)+'\n')
    print('done',report['elapsed_s'],flush=True)

if __name__=='__main__':main()
