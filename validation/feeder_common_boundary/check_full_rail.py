"""Exact900mm translating payload envelope vs parked four-cell geometry."""
from pathlib import Path
import json,time
import build_comparison as b
H=Path(__file__).resolve().parent;O=H/'release';started=time.perf_counter();cases=[]
for candidate in b.old.CANDIDATES:
    if candidate=='indexed_drum':
        rotor=[]
        for q in b.inventory(candidate):
            if q['name'].startswith(('Other_cell_','Passive_payload','Cassette_floor','Cassette_rear','Stored_side_cap','Storage_gate','Drum_axle','Drum_rotor')):rotor.append(q)
        inertias={};masses={}
        for label in ['nominal','upper']:
            J=0.;mass=0.
            for q in rotor:
                s=q['shape']
                if q['material']=='payload':
                    short=s.Volume/10000<200
                    m=(1.33 if short else 4.) if label=='nominal' else (2. if short else 6.)
                    rho=m/s.Volume
                else:rho=b.DENSITY[q['material']];m=rho*s.Volume
                for solid in s.Solids:
                    c=solid.CenterOfMass;ms=rho*solid.Volume
                    J+=(solid.MatrixOfInertia.A11*rho+ms*((c.y+150)**2+(c.z-350)**2))*1e-6
                mass+=m
            inertias[label]=J;masses[label]=mass
        cases.append({'candidate':candidate,'longitudinal_docking_required':False,
                      'rotating_CAD_material_plus_payload_inertia_about_X_kg_m2':inertias,
                      'rotating_CAD_material_plus_payload_mass_kg':masses,
                      'payload_inertia_basis':'Uniform surrogate boxes at envelope centers,1.33/4kg nominal and2/6kg upper;actual spacecraftCG/tensor not supplied. This is not installed inertia.',
                      'missing_rotating_hardware_and_joint_inertia':True,
                      'full_rotation_and_extraction_clearance_accepted':False,
                      'required_next_correction':'Model extractor transmission,index lock/cell load paths and loaded continuous90deg index sweep'})
        continue
    pp=b.inventory(candidate)
    # The maximal3U transport covers every1U envelope (leading datum340.5).
    # Constant attitude,nominal payload only; park all local feeders at home.
    sweep=b.B((1240.5,100,100),(0,0,22))
    hits=[]
    for q in pp:
        if q['name'].startswith('Common_'):continue
        if not sweep.BoundBox.intersect(q['shape'].BoundBox):continue
        vol=sweep.common(q['shape']).Volume
        if vol>1e-5:
            bb=q['shape'].BoundBox
            hits.append({'part':q['name'],'material':q['material'],'penetration_mm3':vol,
                         'part_bounds_mm':[bb.XMin,bb.XMax,bb.YMin,bb.YMax,bb.ZMin,bb.ZMax],
                         'status':'HARD_NOMINAL_PAYLOAD_COLLISION_NO_WAIVER'})
    cases.append({'candidate':candidate,'longitudinal_docking_required':True,
                  'dock_positions_mm':[0,250,650,900],'commanded_travel_mm':900,
                  'guide_rail_length_mm':1600,'payload_sweep_bounds_mm':[0,1240.5,0,100,22,122],
                  'method':'ExactB-rep swept rectangular passive3U payload envelope alongX;includes all4 parked cassette/feed geometries.1U envelopes lie within this maximal envelope.',
                  'intersections':hits,'nominal_payload_corridor_pass':not hits,
                  'full_carriage_gate_docking_and_tolerance_motion_proven':False,
                  'minimum_corrections':['Trim both transverse guide shafts AND capture rack20mm from450 to430mm,endingY-10 instead of+10 (north mirrorY110 instead of90);last moving bearing spans[-29,-11]and applied pawl finger[-19,-18.2]at200mm feed so nominal1mm bearing end margin remains. LeadR2 implements this and checks payload corridor;re-run loaded guide/end retention before acceptance.',
                    'Lead-screw blank likewise endsY+10 and crosses corridor;trim/rework screw/support/coupling toend at or beforeY0 with rated end support. Current catalog10x2 sizing must be reconciled withTr8 CAD.',
                    'Belt front pulley/return arcs protrude into corridor;relocate/re-route their full swept envelope outsideY0..100,Z22..122 and verify clamp travel/tension. No relocation is accepted here.',
                    'Retract dock pins and common side/release barriers in the prescribed travel sequence;prove carrier,insert lock and full carriage clearance,not payload envelope alone.']})
    print(candidate,'fullrail exact payload hits',len(hits),flush=True)
result={'revision':'BB64-RAIL-R1-DEVELOPMENT_FINDING','no_common_rail_acceptance':True,
        'case_count':len(cases),'cases':cases,'elapsed_s':time.perf_counter()-started,
        'scope':'Existing fullrail integration dependency only. This does not extend FM07 coupon acceptance or select a new architecture.'}
(O/'FULL_RAIL_SWEEP.json').write_text(json.dumps(result,indent=2)+'\n')
