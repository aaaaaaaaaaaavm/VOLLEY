"""Source-backed motor/gear/controller options, with declared transmission assumptions.

No purchased assembly or installed mass is invented. Motor/gear efficiency,
custom transmission friction, joint adequacy and environmental compatibility
are separate gates. Run with system python3 after build_comparison.py.
"""
from pathlib import Path
import json,math,hashlib,csv,time
H=Path(__file__).resolve().parent;O=H/'release'
ACT=json.loads((H/'source/act01_parameters.json').read_text())
M=next(m for m in ACT['motors'] if m['id']=='3242G024BX4')
GEAR_URL='https://www.faulhaber.com/fileadmin/Import/Media/EN_32GPT_FMM.pdf'
CTRL_URL='https://www.faulhaber.com/fileadmin/Import/Media/EN_MC5005S_DFF.pdf'
BRAKE_URL='https://www.mikipulley-us.com/documents/Catalog/Catalog_Spring_Actuated_Brake.pdf'
GEARS=[
 {'ratio_nominal':3,'ratio':3.,'stages':1,'mass_kg':.115,'body_length_mm':26.3,'max_eta':.93,'continuous_torque_Nm':1.,'input_max_rpm':6500,'output_max_W':40,'input_inertia_kg_m2':410e-9},
 {'ratio_nominal':9,'ratio':9.,'stages':2,'mass_kg':.157,'body_length_mm':34.7,'max_eta':.89,'continuous_torque_Nm':3.,'input_max_rpm':6500,'output_max_W':21,'input_inertia_kg_m2':434e-9},
 {'ratio_nominal':14,'ratio':13.5,'stages':2,'mass_kg':.157,'body_length_mm':34.7,'max_eta':.89,'continuous_torque_Nm':3.,'input_max_rpm':10000,'output_max_W':21,'input_inertia_kg_m2':195e-9},
 {'ratio_nominal':30,'ratio':29.7,'stages':2,'mass_kg':.157,'body_length_mm':34.7,'max_eta':.89,'continuous_torque_Nm':3.,'input_max_rpm':10000,'output_max_W':21,'input_inertia_kg_m2':195e-9},
 {'ratio_nominal':59,'ratio':59.4,'stages':3,'mass_kg':.200,'body_length_mm':43.1,'max_eta':.80,'continuous_torque_Nm':5.,'input_max_rpm':11000,'output_max_W':14,'input_inertia_kg_m2':196e-9},
 {'ratio_nominal':108,'ratio':107.6625,'stages':3,'mass_kg':.200,'body_length_mm':43.1,'max_eta':.80,'continuous_torque_Nm':5.,'input_max_rpm':11000,'output_max_W':14,'input_inertia_kg_m2':196e-9},
]
BRAKES=[{'id':'BXW-01-10L','static_Nm':.12,'mass_kg':.2,'coil_24V_W':5.,'armature_release_s':.015},
        {'id':'BXW-02-10L','static_Nm':.25,'mass_kg':.3,'coil_24V_W':6.6,'armature_release_s':.015},
        {'id':'BXW-03-10L','static_Nm':.50,'mass_kg':.4,'coil_24V_W':9.,'armature_release_s':.025},
        {'id':'BXW-04-10L','static_Nm':1.,'mass_kg':.6,'coil_24V_W':11.5,'armature_release_s':.03},
        {'id':'BXW-05-10L','static_Nm':2.,'mass_kg':.8,'coil_24V_W':13.,'armature_release_s':.035}]

def screw_torque(F,mu=.15):
    # Thomson10x2 nominal sizing option; detailed CAD remains the earlier
    # Tr8 blank, so source/geometry matching is explicitly a failed gate.
    d=.009;lead=.002;alpha=math.radians(15)
    l=lead/(math.pi*d);f=mu/math.cos(alpha)
    return F*d/2*(l+f)/(1-f*l)+.015

def motion(s,T,t):
    a=4*s/T**2;v=2*s/T
    if t<=T/2:return .5*a*t*t,a*t,a
    dt=T-t
    return s-.5*a*dt*dt,a*dt,-a

def demand(kind,T,resistance=50,mass=7.5):
    rows=[]
    n=3;a_link=.2/(2*n*(math.sin(math.radians(70))-math.sin(math.radians(10))))
    for k in range(401):
        t=T*k/400
        if kind=='indexed_drum':
            q,v,a=motion(math.pi/2,T,t)
            # 3.2kgm2 study inertia,not a validated total installed bound. Measured
            # rotating CAD+payload tensor is emitted separately by geometry.
            tq=3.2*abs(a)+.5;omega=v;alpha=abs(a)
        else:
            stroke=.9 if kind=='common_rail' else .2
            q,v,a=motion(stroke,T,t)
            F=resistance+mass*abs(a)
            if kind in ('lead_screw','telescopic'):
                factor=2 if kind=='telescopic' else 1
                # Telescope drives middle stage over100mm and synchronizes
                # inner stage at2:1. Synchronizer hardware remains absent.
                tq=screw_torque(F*factor)
                omega=2*math.pi*(v/factor)/.002;alpha=2*math.pi*(abs(a)/factor)/.002
            elif kind=='pantograph':
                theta=math.asin(math.sin(math.radians(10))+q/(2*n*a_link))
                gain=n/math.tan(theta)
                tq=screw_torque(F*gain)
                vx=v/gain
                omega=2*math.pi*vx/.002
                # Derivative of input speed includes geometry acceleration.
                dtheta=v/(2*n*a_link*math.cos(theta))
                ax=a*math.tan(theta)/n+v*dtheta/(n*math.cos(theta)**2)
                alpha=2*math.pi*abs(ax)/.002
            else:
                R=.012
                if kind=='spring_dual_gate':F+=32.28
                tq=F*R;omega=v/R;alpha=abs(a)/R
        rows.append((t,tq,omega,alpha))
    return rows

def screen(kind,T,gear,eta=.5):
    rows=demand(kind,T,mass=10 if kind=='common_rail' else 7.5)
    peak={'motor_torque_Nm':0.,'motor_rpm':0.,'output_torque_Nm':0.,'output_W':0.,'required_current_A':0.}
    failed=set();min_voltage_margin=float('inf')
    for t,tq,w,a in rows:
        motorT=tq/(gear['ratio']*eta)+(M['rotor_inertia_kg_m2']+gear['input_inertia_kg_m2'])*a*gear['ratio']
        rpm=w*gear['ratio']*60/(2*math.pi)
        available=M['no_load_rpm']-M['slope_rpm_per_mNm']*motorT*1000
        min_voltage_margin=min(min_voltage_margin,available-rpm)
        if motorT>M['rated_torque_Nm']:failed.add('MOTOR_CONTINUOUS_TORQUE')
        if rpm>available:failed.add('24V_TORQUE_SPEED_LINE')
        if rpm>gear['input_max_rpm']:failed.add('GEAR_INPUT_SPEED')
        if tq>gear['continuous_torque_Nm']:failed.add('GEAR_CONTINUOUS_TORQUE')
        if tq*w>gear['output_max_W']:failed.add('GEAR_OUTPUT_POWER')
        if kind in ('lead_screw','pantograph','telescopic') and w*60/(2*math.pi)>1000:
            failed.add('NUT_ABOVE_PUBLISHED_1000RPM_SCREEN')
        peak['motor_torque_Nm']=max(peak['motor_torque_Nm'],motorT)
        peak['motor_rpm']=max(peak['motor_rpm'],rpm)
        peak['output_torque_Nm']=max(peak['output_torque_Nm'],tq)
        peak['output_W']=max(peak['output_W'],tq*w)
        peak['required_current_A']=max(peak['required_current_A'],motorT/M['kT_Nm_A']+M['no_load_current_A'])
    if peak['required_current_A']>5:failed.add('MC5005_CONTINUOUS_CURRENT')
    return {'candidate':kind,'time_s':T,'resistance_N':50,'moving_mass_study_kg':10 if kind=='common_rail' else 7.5,
            'gear_ratio':gear['ratio'],'gear_nominal_ratio':gear['ratio_nominal'],'assumed_gear_efficiency':eta,
            **peak,'minimum_voltage_line_speed_margin_rpm':min_voltage_margin,
            'failed_screens':sorted(failed),'conditional_motor_gear_screen_pass':not failed,
            'mechanism_or_flight_acceptance':False}

def choose(kind,allcases):
    passing=[c for c in allcases if c['candidate']==kind and c['conditional_motor_gear_screen_pass']]
    if not passing:return None
    # Prefer a published source mass first,then the fastest passing cycle.
    c=min(passing,key=lambda c:(next(g['mass_kg'] for g in GEARS if g['ratio']==c['gear_ratio']),c['time_s']))
    g=next(g for g in GEARS if g['ratio']==c['gear_ratio'])
    brake=next((b for b in BRAKES if b['static_Nm']>=c['output_torque_Nm']),None)
    return {'prototype_option_only':True,'screen':c,'motor':{'id':M['id'],'catalog_mass_kg':M['mass_kg'],'source':M['source_url']},
            'catalog_geometry_integrated_into_candidate_CAD':False,
            'gear':{**g,'id':'32GPT '+str(g['ratio_nominal'])+':1','source':GEAR_URL},
            'controller':{'id':'MC5005S RS/CO','catalog_mass_kg':.230,'continuous_A':5,'source':CTRL_URL},
            'brake_option':None if brake is None else {**brake,'source':BRAKE_URL,'dynamic_arrest_accepted':False,
                'shaft_interface_accepted':False,'armature_time_is_not_complete_system_response':True},
            'known_hardware_mass_option_kg':M['mass_kg']+g['mass_kg']+.230+(brake['mass_kg'] if brake else 0),
            'hardware_mass_complete':False,'missing':['Integratedmotor/gear/controller/brake packaging and actual shaft/flange interfaces','Motor mounting flange mass','Source gearbox efficiency lower bound at operating point',
              'Brake adapter/bore and support','Couplings and bearings','Sensors and harness','Gate and capture actuators',
              'Release spring/preload and plunger rating','Fasteners and thermal mounting','Flight environmental acceptance']}

def main():
    started=time.perf_counter();kinds=['lead_screw','spring_dual_gate','rack_pawl','indexed_drum','pantograph','telescopic','belt_shuttle','common_rail']
    cases=[screen(k,T,g) for k in kinds for T in [2,5,10,15,20,30,60,120] for g in GEARS]
    chosen={k:choose(k,cases) for k in kinds}
    summaries=[]
    for k in kinds[:-1]:
        option=chosen[k];local=1 if k=='indexed_drum' else 4
        known=local*option['known_hardware_mass_option_kg'] if option else None
        if k=='indexed_drum':
            # One additional extractor drive,not silently buried in indexer.
            extract=chosen['lead_screw'];known+=extract['known_hardware_mass_option_kg']
            drive_count=2
        else:known+=chosen['common_rail']['known_hardware_mass_option_kg'];drive_count=5
        summaries.append({'candidate':k,'primary_local_drive_count':local,'total_primary_drive_count':drive_count,
                          'source_backed_hardware_option_mass_subtotal_kg':known,
                          'all_primary_controllers_standby_power_W':drive_count*24*.06,
                          'controller_power_basis':'MC5005S RS/CO60mA at24V,source22C;primary controllers only,gate/control loads omitted',
                          'full_installed_mass_kg':None,'full_installed_CG_mm':None,'full_installed_inertia_kg_m2':None,
                          'all_mandatory_gates_pass':False,'downselect_eligible':False})
    result={'revision':'FDR09-ACT-R0','motor_basis':M,'gear_catalog_basis':{'url':GEAR_URL,'edition':'2026 Jul28',
             'published_efficiency_is_maximum':True,'assumed_efficiency_for_screen':.5,
             'actual_pairing':'Manufacturer drawing explicitly shows3242BX4 plus32GPT',
             'backlash_typical_deg':.6,'vacuum_options':'KL2/KL3 offered, ratings may differ; manufacturer confirmation required'},
            'sources':json.loads((H/'source/ACT01_SOURCES.json').read_text())+[json.loads((H/'source/NEW_SOURCE.json').read_text()),json.loads((H/'source/RATIOS_SOURCE.json').read_text())],
            'screen_conditions':'24V,manufacturer22C motor/gear data;50N assumed resistance;7.5kg local moving mass study,10kg common rail;triangular200mm local/900mm rail motion; gear eta0.5 assumed,not manufacturer guaranteed. Drum90deg index,J3.2kgm2 study inertia(not a validated installed bound) and0.5Nm disturbance. Continuous source torque/speed/power/current limits checked at401 time stations including rotor/gear input inertia.',
            'component_derating_limits':{'motor':'Published ambient22C data;no vacuum thermal,radiation,launch or mission duty qualification inferred.',
              'gearbox':'Standard-30..+120C;optionalKL2vacuum1e-5Pa at22C orKL3vacuum1e-9Pa at60C offered;manufacturer warns option ratings may differ. Source efficiency is a maximum,not a guaranteed lower bound.',
              'brake':'BXW catalog operating-10..+40C;this excludes the full-40..+80C study corners. Static friction torque is not a complete dynamic arrest rating;armature release time is not system response.',
              'nut':'SB3700 dynamic310N at500rpm,lubricated ambient;conservative155N screen to1000rpm;higher speed unsupported;82C max is not a flight/vacuum rating.',
              'controller':'MC5005S5A continuous,-40..+85C,60mA standby at24V (RS/CO). Mounting/cooling,phase/DC bus relationship,EMC and space suitability require integration review.'},
            'selected_prototype_options':chosen,'cases':cases,'system_hardware_subtotals':summaries,
            'remaining_mechanism_failures':{
             'lead_screw':'Catalog10x2/SB3700 sizing does not match originalTr8 blank CAD; revise screw/nut/cage and support interfaces before claiming installed actuator.',
             'spring_dual_gate':'15N minimum spring force cannot overcome20/50N assumed friction; spring material/fatigue and governor control remain open. Rewind motor option does not fix feed-force deficiency.',
             'rack_pawl':'Involute tooth mesh,axle/bearings,rack attachment bolts and rated indexing latch remain open.',
             'indexed_drum':'Index rotor/cell joints and rated lock absent; extractor transmission not modeled; no loaded continuous indexing clearance proof.',
             'pantograph':'Output linkage still disconnected from fork; screw/input clevis and sliding pivots absent. Source motor option is conditional on proposed transverse screw input.',
             'telescopic':'Stage law corrected to0,u/2,u. The proposed fork pad contacts inner tube but intersects outer/middle tubes (261/171mm3 atstowed);requires a slotted/end-flange connection redesign.2:1 synchronization,drive screw,end stop and bearing loads absent.20mm overlap is geometric only.',
             'belt_shuttle':'Belt type/strength,pretension,slip,shaft radial load and clamp bolts unresolved.',
             'common_rail':'BB64 new900mm docking motion;belt/drive coupling,position tolerance,independent arrest and dock latch not accepted.'},
            'generic_load_bounds':{'payload_upper_kg':6,'launch_study_25g_payload_force_N':6*25*9.80665,
                                   'not_a_provider_approved_environment':True},
            'no_selected_architecture':True,'elapsed_s':time.perf_counter()-started}
    (O/'ACTUATOR_SCREEN.json').write_text(json.dumps(result,indent=2)+'\n')
    print('actuator conditional screens',len(cases),'elapsed',result['elapsed_s'])
    for k,v in chosen.items():
        print(k,'NONE' if v is None else str((v['gear']['id'],v['screen']['time_s'],round(v['screen']['motor_torque_Nm'],5),round(v['screen']['motor_rpm'],1),v['known_hardware_mass_option_kg'])))

if __name__=='__main__':main()
