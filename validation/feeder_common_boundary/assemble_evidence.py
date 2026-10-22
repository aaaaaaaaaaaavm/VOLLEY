"""Assemble the four-inventory source/CAD comparison without an architecture score."""
from pathlib import Path
import json,csv,hashlib,math,time
H=Path(__file__).resolve().parent;O=H/'release'

def main():
    cad=json.loads((O/'COMPARISON.json').read_text())
    act=json.loads((O/'ACTUATOR_SCREEN.json').read_text())
    rail=json.loads((O/'FULL_RAIL_SWEEP.json').read_text())
    inserts=json.loads((O/'INSERT_INTERFACE.json').read_text())
    trim=json.loads((O/'LEAD_TRIM_R2.json').read_text())
    rail_by={r['candidate']:r for r in rail['cases']}
    assert cad['revision']=='FDR09-R1-2026-10-22'
    byact={r['candidate']:r for r in act['system_hardware_subtotals']}
    rows=[];gates=[];bom=[]
    for r in cad['cases']:
        name=r['candidate'];a=byact[name]
        nominal=r['connection_motion_review']['nominal_stations']
        fault=r['connection_motion_review']['power_loss_applied_geometry']
        pawl_good=all(x['pawl_rack']['distance_mm']<1e-5 and x['pawl_rack']['penetration_mm3']<1e-5 for x in fault)
        collisions=sum(len(x['unresolved_intersections']) for x in nominal)
        payload_collisions=sum(sum(c['payload_involved'] for c in x['unresolved_intersections']) for x in nominal)
        option=act['selected_prototype_options'][name]
        hardware=a['source_backed_hardware_option_mass_subtotal_kg']
        rows.append({'candidate':name,'cells':4,'common_receivers':1,
            'modeled_custom_material_kg':r['modeled_material_mass_kg'],
            'catalog_hardware_option_subtotal_kg':hardware,
            'partial_dry_option_subtotal_kg':r['modeled_material_mass_kg']+hardware,
            'conditional_listed_hardware_lower_bound_kg':hardware,
            'full_installed_dry_mass_kg':None,'full_installed_CG_mm':None,'full_installed_inertia_kg_m2':None,
            'local_option_cycle_s':option['screen']['time_s'],
            'local_option_gear':option['gear']['id'],
            'nominal_local_payload_intersection_count':payload_collisions,
            'all_unresolved_local_intersection_count':collisions,
            'applied_pawl_nominal_contact':pawl_good,'downselect_eligible':False})
        rows[-1]['fullrail_payload_collision_count']=len(rail_by[name].get('intersections',[]))
        rowg={'candidate':name,'gates':{
            'four_payload_manifest':{'status':'PASS_GEOMETRY_ONLY','evidence':'Exactly2x113.5mm and2x340.5mm passive envelopes in native four-cell assembly'},
            'one_common_receiver_count':{'status':'PASS_COUNT_ONLY','evidence':'One receiver modeled;full receiver/two-sided dock adaptation unaccepted'},
            'applied_pawl_rack_contact':{'status':'PASS_NOMINAL_GEOMETRY_ONLY' if pawl_good else 'FAIL','evidence':'Nine fault stations snapped to next2mm tooth gap;zero nominal interference; no spring/response/load proof'},
            'complete_installed_boundary':{'status':'OPEN','evidence':'Catalog motor/gear/controller/brake option masses available;gate drives,capture spring,bearings,mounts,fasteners,sensors,harness and rated joints remain incomplete'},
            'full_motion':{'status':'OPEN','evidence':'Seven nominal local stations/nine applied-fault stations;continuous nonlinear/index/docking motion unproven'},
            'local_parts_interference':{'status':'FAIL_NOMINAL_INTERFERENCE' if collisions else 'PASS_SAMPLED_GEOMETRY_ONLY',
                'evidence':{'retained_intersection_count_across_stations':collisions,
                    'shared_R1_guide_bearing_housing_interference_mm3':16.176779,
                    'telescopic_pad_interference_stowed_mm3':[261,171] if name=='telescopic' else None,
                    'lead_R2_housing_relief_is_not_an_all_seven_R1_correction':True}},
            'common_receiver_docking_or_drum_rotation':{'status':'FAIL_NOMINAL_SWEEP' if name!='indexed_drum' else 'OPEN','evidence':rail_by[name]},
            '1U_insert_and_common_release_datum':{'status':'PASS_NOMINAL_CONTACT_ONLY_RETURN_CUSTODY_OPEN','evidence':'Two0.1859328kg passive inserts;1U payloadX227..340.5,3UX0..340.5. Same four clamp locations contact both packages;positive insert capture during launch and empty return not rated.'},
            'tolerance':{'status':'FAIL_STUDY_CORNER','evidence':'3U2mm side clearance minus0.3mm manufacture,0.5deg alignment and60K differentialAl/steel proxy gives negative margin;payloadICD/CTE and fullrail survey remain open'},
            'loaded_fault_custody':{'status':'OPEN','evidence':'Positive nominal applied rack contact is not rated capture;25g upper3U payload force1471N and dynamic contact law/rated restraints remain unaccepted'},
            'source_motor_gear_option':{'status':'PASS_CONDITIONAL_STUDY_ONLY','evidence':option['screen']},
            'architecture_specific':{'status':'FAIL_OR_OPEN','evidence':act['remaining_mechanism_failures'][name]},
            'D27_selection':{'status':'BLOCKED','evidence':'Mandatory acceptance gates remain failed/open;no preliminary freeze or selected architecture'}},
            'all_mandatory_acceptance_gates_pass':False}
        gates.append(rowg)
        for p in r['BOM']:
            bom.append({'candidate':name,'part':p['name'],'quantity':1,
                        'mass_basis':p['mass_status'],
                        'mass_kg':p['modeled_material_mass_kg'] if p['material'] not in ('envelope','payload') else None,
                        'source':'Native B-rep volume*density' if p['material'] not in ('envelope','payload') else '',
                        'installed_geometry_or_rating_verified':False})
        drives=[('local_'+name,option,1 if name=='indexed_drum' else 4)]
        if name=='indexed_drum':drives.append(('extractor',act['selected_prototype_options']['lead_screw'],1))
        else:drives.append(('BB64_common_rail',act['selected_prototype_options']['common_rail'],1))
        for label,opt,count in drives:
            for typ in ['motor','gear','controller','brake_option']:
                p=opt[typ]
                if p is None:continue
                mass=p.get('catalog_mass_kg',p.get('mass_kg'))
                bom.append({'candidate':name,'part':label+' '+p['id'],'quantity':count,
                            'mass_basis':'CATALOG_PROTOTYPE_OPTION_NOT_INSTALLED_ASSEMBLY',
                            'mass_kg':mass,'source':p['source'],
                            'installed_geometry_or_rating_verified':False})
        for missing in ['Gate opening/latching actuators','Arrest-plunger return spring/release actuator',
                        'Position and dock sensors','Complete bearings/couplings/motor flange/brake adapters',
                        'Fasteners and retention/preload features','Harness/connectors/power distribution',
                        'Flight thermal/structure/EMC provisions','Approved payload and launcher interfaces']:
            bom.append({'candidate':name,'part':missing,'quantity':None,'mass_basis':'UNRESOLVED_NOT_ZERO',
                        'mass_kg':None,'source':None,'installed_geometry_or_rating_verified':False})
    tol=[]
    for L in [113.5,340.5]:
        for theta in [.1,.5]:
            for T in [-40,20,80]:
                thermal=L*abs(T-20)*(23e-6-12e-6)
                skew=L*math.sin(math.radians(theta))
                margin=2-.3-skew-thermal
                tol.append({'payload_length_mm':L,'alignment_deg':theta,'temperature_C':T,
                            'nominal_side_clearance_mm':2,'combined_manufacturing_mm':.3,
                            'differential_thermal_proxy_mm':thermal,'alignment_projection_mm':skew,
                            'residual_clearance_study_mm':margin,'positive_study_margin':margin>0,
                            'actual_payload_material_or_flight_acceptance':False})
    final={'revision':'FDR09-DEVELOPMENT_FINDINGS','status':'SEVEN_CONCEPT_STUDY_NOT_D27_DOWNSELECT',
           'mission_context':'Generic maneuvering OTV/500kmSSO;provisional mounts. No provider environment or payloadICD approval inferred.',
           'manifest':{'1U':2,'3U':2,'separate_12_study_not_included':True},
           'boundary':cad['comparison_boundary'],'partial_mass_warning':'Custom CAD material subtotal plus catalog hardware OPTION masses. Catalog options are not integrated/qualified. Missing masses remain null;these are not full installed dry mass,CG or inertia. Listed hardware alone is a conditional lower bound IF these exact option quantities are adopted;custom CAD subtotal is not a certified installed lower bound because unresolved intersections and rework can change material.',
           'comparison':rows,'mandatory_gates':gates,'tolerance_study':tol,
           'weights':{'safety':.35,'fit_mass':.25,'position':.20,'cycle_power':.10,'manufacture':.10},
           'weighted_scores':None,'selected_architecture':None,
           'score_reason':'Mandatory gates are incomplete;ordinal or partial-mass rankings would not establish an eligible architecture.',
           'hardware_BOM':bom,'fullrail_sweep':rail,'insert_interface':inserts,'bounded_lead_correction_R2':trim,
           'component_derating_limits':act['component_derating_limits'],
           'source_CAD':'COMPARISON.json','source_actuation':'ACTUATOR_SCREEN.json'}
    (O/'REVIEW.json').write_text(json.dumps(final,indent=2)+'\n')
    with (O/'COMPARISON.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    with (O/'BOM.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(bom[0]));w.writeheader();w.writerows(bom)
    table=['| Concept | Custom CAD kg | Catalog option kg | Partial subtotal kg | Local cycle option s | Eligibility |',
           '|---|---:|---:|---:|---:|---|']
    for r in rows:table.append('| '+r['candidate']+' | '+f"{r['modeled_custom_material_kg']:.3f} | {r['catalog_hardware_option_subtotal_kg']:.3f} | {r['partial_dry_option_subtotal_kg']:.3f} | {r['local_option_cycle_s']} | BLOCKED |")
    text='''# Seven feeder development comparison —22October2026\n\nFour payloads(2x1U+2x3U),one reusable receiver. Six fixed-cell concepts have four local feeds and a shared900mm docking rail;drum has one indexing drive and requires a separate extractor. This removes the old four-cell-versus-one-cell inventory error. Full installed mass,CG and inertia remain unestablished.\n\n'''+ '\n'.join(table)+'''

The partial subtotal adds represented custom material to source-backed motor/gear/controller/brake options. It omits unresolved installed items and is not an architecture ranking. Source hardware CG/inertia are not published; custom-only native mass properties appear inCOMPARISON.json. Different cycle options are conditional operating points,not a common accepted cycle requirement.

The corrected arrest plunger reaches the rack root/flank with no nominal penetration and has1mm retracted tooth clearance. Its guide has0.15mm nominal side clearance and0.2mm forward tooth backlash. Spring preload,release response,rated tooth load and joint retention remain open. Rack/belt drive pads establish geometric contact only. Telescopic tube travel is corrected to0,u/2,u,with20mm minimum overlap;its synchronization and loaded stops remain open.

The0.1859328kg passive1U locator is included twice in every native inventory and locates1U leading faceX340.5. The insert travels with its dedicated1U and must remain captive through release and empty return;lock/return proof remains open. Shared fork and four clamp contacts have zero nominal penetration in the checked capture pose. Initial simultaneous side-gate/fork collision is retained in source/INSERT_INTERFACE_initial_failed_pose.json;the corrected capture snapshot keeps side gates open until fork reset.

The spring follower still fails20/50N resistance at its15N end force. The pantograph output linkage remains disconnected. Drum extraction/index joints and continuous indexing clearance remain unproven. The BB64 fullrail receiver/docking model is separate integration work;the FM07 coupon does not establish its acceptance. The exact900mm payload sweep FAILS at parked guide shafts/capture racks for all six fixed-cell concepts;lead-screw blanks and belt front pulley/return arcs add collisions. FULL_RAIL_SWEEP.json records exact parts,materials,volumes and minimum corrections. The3U0.5degree tolerance corner has negative study clearance. All seven remain blocked forD27;no preliminary freeze or selected baseline is asserted.

Reproduction:PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3 build_comparison.py;python3 actuator_screen.py;PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3 check_step_exchange.py;python3 assemble_evidence.py. The build resumes completed per-candidate evidence;--force regenerates all candidates. STEP exchange uses a1ppm numerical volume criterion;functional clearance criteria remain separate. The initial stricter spring exchange failure is preserved inlogs/build_initial_step_threshold_failure.log andSPRING_STEP_EXCHANGE.json records surface/bbox diagnostics.
'''
    (O/'READ_ME.md').write_text(text)
    manifest={str(p.relative_to(H)):hashlib.sha256(p.read_bytes()).hexdigest() for p in H.rglob('*')
              if p.is_file() and p.suffix in ('.py','.json','.csv','.FCStd','.step','.pdf','.md') and p.name!='MANIFEST.json'}
    (O/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('assembled7-candidate development review,BOM,tolerance table,source hashes')

if __name__=='__main__':main()
