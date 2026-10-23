#!/usr/bin/env python3
"""FM08-R3/FDR10 academic architecture selection and executable design screens.

This is an analytical/logic study. It does not calibrate contact dynamics,
certify installed hardware, or estimate a probability of mission success.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict, replace
from pathlib import Path
import csv, hashlib, json, math, random, sys

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
CAPTURE=ROOT/'catalog_reference.json'
PAR=ROOT/'PARAMETERS.json'
p=json.loads(PAR.read_text());old=json.loads(CAPTURE.read_text());motor=old['motor_basis']
assert p['gear_brake_static_torque_Nm']==old['brake_reference']['local']['static_torque_Nm']
assert p['receiver_brake_static_torque_Nm']==old['brake_reference']['receiver']['static_torque_Nm']
assert p['receiver_brake_catalog_mass_kg']==old['brake_reference']['receiver']['catalog_mass_kg']

WEIGHTS={'safety_and_fault_control':.35,'packaging_and_mass':.25,'positioning_and_custody':.20,'cycle_and_power':.10,'manufacturability':.10}
JUDGMENTS=[
 ('lead_screw',[8,6,8,6,8],['Reversible pusher motion with capped-channel containment and independently proved far/near receiver stops','Currentsource-backedreferencealready meets30s sizing screen','Fourlocaldrives and longreceiver increase installedburden']),
 ('rack_pawl',[7,7,7,8,7],['Positive engagement and compact reversible travel','Toothmesh,backlash,support and controlled anti-backdrive latch require detail','Runner-up retained;could win if lead-screw mass or contamination control dominates']),
 ('spring_dual_gate',[6,8,6,8,8],['Fast low-active-powertransfer and simple energy source','Existing15Nendforce fails50Nscreen;increasedpreload needs governedmotion andcustody','Gate sequencing and reliable rewind add mechanism burden']),
 ('belt_shuttle',[6,8,6,7,7],['Flexible packaging and low driveinertia','Elastic compliance,pretension,tooth skipand power-off retention require additional control','Less direct position custody than selected screw reference']),
 ('indexed_drum',[6,8,6,6,5],['Single feedport and inventoryindexing','Sharedindex fault can block entire manifest;large swept volume androtorlock','Installedextractor andpositiveindex interface remain conceptual']),
 ('telescopic',[6,7,6,5,5],['Potential compact retractedlength','Stage synchronization,overlap stiffness,and knownpadintersections complicateintegration','More slidinginterfaces andconcealedjams']),
 ('pantograph',[5,7,5,5,5],['Potential compactcollapsingstorage','Near-flat force amplification andmany pivots increase loads/backlash','Existingoutputdisconnection requires redesign;variablegeometryalignment'])
]

def selection():
 rows=[]
 for name,scores,reasons in JUDGMENTS:
  row={'candidate':name,'scores_0_to_10':dict(zip(WEIGHTS,scores)),
       'weighted_score_0_to_10':round(sum(w*s for w,s in zip(WEIGHTS.values(),scores)),3),
       'evidence_type':'Documented engineering judgment;not measured performance or reliability',
       'reasoning':reasons}
  rows.append(row)
 rows.sort(key=lambda r:r['weighted_score_0_to_10'],reverse=True)
 sensitivities=[]
 for label,w in [('equal', [.2]*5),('safety_emphasis',[.5,.15,.2,.05,.1]),('mass_emphasis',[.2,.45,.15,.1,.1]),('cycle_emphasis',[.2,.2,.15,.35,.1])]:
  rs=sorted([(name,round(sum(a*b for a,b in zip(w,score)),3)) for name,score,_ in JUDGMENTS],key=lambda x:x[1],reverse=True)
  sensitivities.append({'case':label,'weights':dict(zip(WEIGHTS,w)),'ranking':rs})
 # Vary every judgment score independently by +/-1;this is decision robustness,
 # not a probability that the mechanism works.
 rng=random.Random(20261023);wins={name:0 for name,_,_ in JUDGMENTS}
 for _ in range(10000):
  rs=[(name,sum(w*max(0,min(10,s+rng.uniform(-1,1))) for w,s in zip(WEIGHTS.values(),scores))) for name,scores,_ in JUDGMENTS]
  wins[max(rs,key=lambda x:x[1])[0]]+=1
 return {'revision':'D27-R2/FDR10','weights':WEIGHTS,'ranking':rows,'selected':'lead_screw','runner_up':'rack_pawl',
  'selection_class':'Controlled academic architecture selection subject to selected-design checks;not all-seven qualification',
  'supersession':'D27-R2 defines the selected academic design-study acceptance boundary dated 23 October 2026. Original FDR09 qualification-gate findings remain unchanged historical evidence.',
  'common_boundary':'Four fixedindependentlyretained cells,two1U+two3U,one reusable900mmindexedreceiver;200mm localtransfer;50Nstudyresistance;source24Vdrives;50N is assumed,not measured',
  'sensitivity':sensitivities,'score_perturbation_scenarios':10000,'score_perturbation_winner_counts':wins,
  'sensitivity_interpretation':'Smallscore margin and ranking reversals mean a transparent engineering choice,not a unique numerical optimum. Keep rack/pawl runner-up and revisit if measured inputs change.',
  'non_claims':['Scores are not probabilities or empiricalreliability','No architecture isflightqualified','PriorfailedCADdoes notbecomeacceptedthroughranking','SelectedR3geometry andscreenresultsare separate evidence']}

def screw_torque(F):
 d=p['screw_mean_diameter_mm']/1000;lead=p['screw_lead_mm']/1000
 tanlam=lead/(math.pi*d);fr=p['screw_mu_assumed']/math.cos(math.radians(p['screw_half_flank_angle_deg']))
 return F*d/2*(tanlam+fr)/(1-fr*tanlam)+p['bearing_drag_Nm_assumed']

def motion(stroke,T,t):
 a=4*stroke/T**2
 if t<=T/2:return .5*a*t*t,a*t,a
 u=T-t;return stroke-.5*a*u*u,a*u,-a

def drive_screen(kind,resistance,stroke_override_mm=None,time_override_s=None,moving_mass_override_kg=None):
 local=kind=='local_feed';stroke=p['feed_stroke_mm' if local else 'receiver_stroke_mm']/1000;T=p['feed_time_s' if local else 'receiver_time_s']
 if stroke_override_mm is not None:stroke=stroke_override_mm/1000
 if time_override_s is not None:T=time_override_s
 mass=p['local_moving_mass_kg' if local else 'receiver_moving_mass_kg']
 if moving_mass_override_kg is not None:mass=moving_mass_override_kg
 ratio=p['local_gear_ratio' if local else 'receiver_gear_ratio'];eta=p['gear_efficiency_assumed']
 gear=next(g for g in old['selected_prototype_options'].values() if g and g['gear']['ratio']==ratio)['gear']
 peaks=dict.fromkeys(['force_N','motor_torque_Nm','motor_rpm','output_torque_Nm','output_power_W','current_A','shaft_rpm'],0.)
 margin=float('inf');rows=[]
 for k in range(1001):
  t=T*k/1000;q,v,a=motion(stroke,T,t);F=resistance+mass*abs(a)
  if local:tq=screw_torque(F);omega=2*math.pi*v/(p['screw_lead_mm']/1000);alpha=2*math.pi*abs(a)/(p['screw_lead_mm']/1000)
  else:R=p['rack_reference_pinion_radius_mm' if kind=='rack_local_reference' else 'receiver_pulley_radius_mm']/1000;tq=F*R;omega=v/R;alpha=abs(a)/R
  mt=tq/(ratio*eta)+(motor['rotor_inertia_kg_m2']+gear['input_inertia_kg_m2'])*alpha*ratio
  rpm=omega*ratio*60/(2*math.pi);available=motor['no_load_rpm']-motor['slope_rpm_per_mNm']*mt*1000
  current=mt/motor['kT_Nm_A']+motor['no_load_current_A'];shaft=omega*60/(2*math.pi)
  values=[F,mt,rpm,tq,tq*omega,current,shaft]
  for key,val in zip(peaks,values):peaks[key]=max(peaks[key],val)
  margin=min(margin,available-rpm);rows.append({'t_s':t,'position_mm':q*1000,'speed_mm_s':v*1000,'force_N':F,'motor_torque_Nm':mt,'motor_rpm':rpm,'current_A':current})
 criteria={'motor_continuous_torque':peaks['motor_torque_Nm']<=motor['rated_torque_Nm'],'motor_torque_speed_line':margin>=0,
  'gear_input_speed':peaks['motor_rpm']<=gear['input_max_rpm'],'gear_continuous_torque':peaks['output_torque_Nm']<=gear['continuous_torque_Nm'],
  'gear_output_power':peaks['output_power_W']<=gear['output_max_W'],'controller_continuous_current':peaks['current_A']<=5,
  'nut_load_speed_screen':(peaks['force_N']<=155 and peaks['shaft_rpm']<=1000) if local else True}
 with (OUT/f'{kind}_{resistance:g}N.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
 return {'kind':kind,'resistance_N':resistance,'time_s':T,'stroke_mm':stroke*1000,'moving_mass_kg_assumed':mass,'gear_ratio':ratio,
  'assumed_efficiency':eta,'peaks':peaks,'minimum_torque_speed_margin_rpm':margin,'criteria':criteria,'all_declared_sizing_screens_pass':all(criteria.values()),
  'current_based_electrical_energy_bound_J':p['bus_voltage_V']*peaks['current_A']*T,
  'energy_bound_interpretation':'24V times peak modeled motor current times time;not measured busenergy or coupled inverterthermalprediction',
  'transmission':'Trapezoidal lead screw' if local else ('Hypothetical rack-and-pinion reference' if kind=='rack_local_reference' else 'Toothed belt / pulley / split clutch'),'manufacturer_reference_only':True}

def mechanics():
 E=p['steel_E_GPa_assumed']*1e9;L=p['screw_supported_span_mm']/1000;d=p['screw_root_diameter_mm']/1000
 I=math.pi*d**4/64;A=math.pi*d*d/4;Pcr=math.pi**2*E*I/L**2
 designF=p['adverse_axial_resistance_N']+p['local_moving_mass_kg']*4*(p['feed_stroke_mm']/1000)/p['feed_time_s']**2
 dp=p['restraint_pin_diameter_mm']/1000
 shear=p['restraint_pin_count']*p['restraint_shear_planes_per_pin']*math.pi*dp**2/4*p['assumed_allowable_pin_shear_MPa']*1e6
 bearing=p['lug_count']*dp*(p['lug_thickness_mm']/1000)*p['assumed_allowable_lug_bearing_MPa']*1e6
 loadrows=[]
 for g in p['provisional_acceleration_g']:
  F=p['payload_upper_mass_kg']*g*9.80665;Fr=p['retained_payload_and_carrier_study_kg']*g*9.80665
  loadrows.append({'g':g,'payload_force_N':F,'pin_static_capacity_N_assumed':shear,'pin_capacity_to_load':shear/F,'lug_bearing_capacity_N_assumed':bearing,'lug_capacity_to_load':bearing/F,'payload_and_carrier_mass_kg_assumed':p['retained_payload_and_carrier_study_kg'],'payload_and_carrier_force_N':Fr,'pin_capacity_to_payload_and_carrier_load':shear/Fr,'lug_capacity_to_payload_and_carrier_load':bearing/Fr})
 Ig=math.pi*(p['guide_diameter_mm']/1000)**4/64;Lg=p['guide_span_mm']/1000
 yaw=p['payload_half_length_mm']*math.tan(math.radians(p['relative_yaw_deg_assumed']))
 thermal=p['thermal_length_mm_assumed']*p['temperature_difference_K_assumed']*p['differential_CTE_um_mK_assumed']*1e-6
 lateral=[]
 for F in p['lateral_study_loads_N']:
  per=F/p['guide_count'];defl=per*Lg**3/(48*E*Ig)*1000
  stress=(per*Lg/4)*(p['guide_diameter_mm']/2000)/Ig/1e6
  total=p['manufacture_and_assembly_stack_mm_assumed']+yaw+thermal+defl
  margin=None if p['nominal_corridor_clearance_mm'] is None else p['nominal_corridor_clearance_mm']-total
  lateral.append({'total_side_load_N_assumed':F,'simply_supported_midspan_deflection_mm':defl,'bending_stress_MPa':stress,'yaw_consumption_mm':yaw,'differential_thermal_consumption_mm':thermal,'stack_total_mm':total,'nominal_clearance_mm':p['nominal_corridor_clearance_mm'],'remaining_clearance_mm':margin,'screen_pass':None if margin is None else margin>0})
 v=2*(p['feed_stroke_mm']/1000)/p['feed_time_s'];latencydist=v*p['sensor_stop_latency_s_assumed']*1000
 return {'screw':{'end_condition':'Both ends laterallysupported,pinned-pinnedEulerstudy K1;not a detailed bearingalignment model','euler_buckling_N':Pcr,'design_axial_N':designF,'buckling_capacity_to_load':Pcr/designF,'axial_stress_MPa':designF/A/1e6,'axial_shortening_mm':designF*L/(E*A)*1000},
  'restraint':{'basis':'Two6mmpins,twoshearplanes each,four5mmlugs;50MPaassumedallowables;payloadcontact/hostfastenersnotqualifiedbythisscreen','provisional_load_cases':loadrows},
  'guide_and_clearance':{'basis':'Simplysupportedsolidsteelroundguides;centralpointload shared equally. Conservativegeometryscreen;actualsupport/bearingstiffnessnotidentified','cases':lateral},
  'power_loss':{'maximum_feed_speed_mm_s':v*1000,'assumed_sensor_stop_latency_s':p['sensor_stop_latency_s_assumed'],'travel_during_assumed_sensor_latency_mm':latencydist,
  'moving_kinetic_energy_J':.5*p['local_moving_mass_kg']*v*v,
  'containment_strategy':'Normally engaged screw brake retains the rear pusher boundary; a continuous capped channel and receiver far stops contain possible payload drift. Stop and inhibit; supervised recovery only.',
  'interpretation':'These are prescribed pusher-motion references, not bounds on free-payload impact after a fault. No dynamic arrest distance, peak impact load, settling time or reliability is accepted by this study.'},
  'backdrive':{'self_locking_assumed':False,'reason':'Friction in space is unknown; screw friction is not a safety lock','ideal_frictionless_torque_at155N_Nm':155*(p['screw_lead_mm']/1000)/(2*math.pi),'catalog_static_brake_Nm':p['gear_brake_static_torque_Nm'],'static_brake_to_frictionless155N_ratio':p['gear_brake_static_torque_Nm']/(155*(p['screw_lead_mm']/1000)/(2*math.pi)),'receiver_reference_static_brake_Nm':p['receiver_brake_static_torque_Nm'],'receiver_100N_static_holding_demand_Nm':p['adverse_axial_resistance_N']*p['receiver_pulley_radius_mm']/1000,'receiver_static_capacity_to_100N_load':p['receiver_brake_static_torque_Nm']/(p['adverse_axial_resistance_N']*p['receiver_pulley_radius_mm']/1000),'receiver_holding_screen_pass':p['receiver_brake_static_torque_Nm']>=p['adverse_axial_resistance_N']*p['receiver_pulley_radius_mm']/1000}}

@dataclass(frozen=True)
class State:
 phase:str='STOWED'; payload:str='CELL'; gate_closed:bool=True
 rear_boundary_retained:bool=True; receiver_clamp:bool=False; docked:bool=False
 power:bool=True; fault:bool=False; inhibited:bool=True
 common_path_clear:bool=False; receiver_empty_proven:bool=False
 stored_cells_retained:bool=True; insert_fixed:bool=True
 discharged:bool=True; isolation:bool=False; released_count:int=0
 channel_closed:bool=True; far_stop_closed:bool=False; far_stop_proven:bool=False; payload_seated_proven:bool=False
 index_clutch_engaged:bool=True; clutch_engaged_proven:bool=True; clutch_disengaged_proven:bool=False; launch_module_stopped_proven:bool=True
 home_proven:bool=False; cell_index:int=0; released_total:int=0
 host_burn_active:bool=False; host_attitude_stable:bool=True; host_acceleration_m_s2:float=0.0
 host_off_guard_elapsed_s:float=p['host_off_guard_s']
 cell_status:tuple=('STORED','STORED','STORED','STORED')

def invariant(s):
 if s.released_count not in (0,1):return False
 if s.released_total!=s.cell_status.count('RELEASED'):return False
 if not s.fault and s.host_acceleration_m_s2>p['host_acceleration_limit_m_s2_assumed']:return False
 if s.clutch_engaged_proven and s.clutch_disengaged_proven:return False
 if s.phase=='ARMED' and (s.index_clutch_engaged or not s.clutch_disengaged_proven):return False
 if s.phase=='ARMED' and (s.host_burn_active or not s.host_attitude_stable or s.host_off_guard_elapsed_s<p['host_off_guard_s']):return False
 if not 0<=s.cell_index<=len(s.cell_status):return False
 if not s.stored_cells_retained or not s.insert_fixed:return False
 if s.payload=='CELL' and not(s.gate_closed or (s.channel_closed and s.far_stop_closed and s.far_stop_proven and s.rear_boundary_retained and s.docked)):return False
 if s.payload=='BRIDGE' and not(s.channel_closed and s.far_stop_closed and s.far_stop_proven and s.rear_boundary_retained):return False
 if s.payload=='BRIDGE' and not s.docked:return False
 if s.payload=='RECEIVER' and not(s.receiver_clamp or (s.channel_closed and s.far_stop_closed and s.far_stop_proven and s.docked)):return False
 if s.payload=='RELEASED' and (s.phase not in ('RELEASED','RETURNING','HOME','COMPLETE') or s.released_count!=1):return False
 if (s.fault or not s.power) and not s.inhibited:return False
 return True

NORMAL=['PROVE_PATH','PROVE_EMPTY','DOCK','CLOSE_FAR_STOP','PROVE_FAR_STOP','OPEN_GATE','FEED','PROVE_SEATED','CAPTURE','RETRACT','CLOSE_GATE','UNDOCK','CLUTCH_RELEASE','PROVE_DISENGAGED','ARM','RELEASE','PROVE_LAUNCH_STOPPED','CLUTCH_ENGAGE','PROVE_ENGAGED','RETURN_EMPTY','PROVE_RETURN_EMPTY','HOME_PROVED','RESET_NEXT']
FAULTS=['POWER_LOSS','JAM','SENSOR_DISAGREEMENT','TIMEOUT','DOUBLE_FEED_REQUEST','FALSE_EMPTY_SIGNAL','HOST_ACCEL_EXCEEDED','CLUTCH_SENSOR_DISAGREEMENT','FALSE_FAR_STOP_SIGNAL','SEATING_TIMEOUT']
ENVIRONMENT=['HOST_BURN_ON','HOST_BURN_OFF','WAIT_HOST_GUARD','PROVE_HOST_STABLE']
RECOVERY=['PROVE_RECOVERY_GATE_CLOSED','PROVE_RECOVERY_EMPTY','PROVE_RECOVERY_HOME','ISOLATE_CELL']

def step(s,event,supervisor=False,pathproof=False):
 if event=='HOST_BURN_ON':
  return replace(s,host_burn_active=True,host_attitude_stable=False,host_acceleration_m_s2=p['host_burn_logic_case_m_s2'],host_off_guard_elapsed_s=0.,fault=s.fault or not s.index_clutch_engaged or not s.gate_closed,inhibited=True if s.phase=='ARMED' or not s.index_clutch_engaged or not s.gate_closed else s.inhibited,phase='READY' if s.phase=='ARMED' else s.phase),True
 if event=='HOST_BURN_OFF':return replace(s,host_burn_active=False,host_acceleration_m_s2=0.,host_off_guard_elapsed_s=0. if s.host_burn_active else s.host_off_guard_elapsed_s),True
 if event=='WAIT_HOST_GUARD' and not s.host_burn_active:return replace(s,host_off_guard_elapsed_s=min(p['host_off_guard_s'],s.host_off_guard_elapsed_s+1.0)),True
 if event=='PROVE_HOST_STABLE' and not s.host_burn_active and s.host_off_guard_elapsed_s>=p['host_off_guard_s']:return replace(s,host_attitude_stable=True),True
 if event in FAULTS:
  return replace(s,fault=True,inhibited=True,power=False if event=='POWER_LOSS' else s.power,common_path_clear=False),True
 if event=='RESTORE_POWER':return replace(s,power=True,inhibited=True),True
 if event=='RECOVER':
  if s.fault and s.power and supervisor and pathproof and ((s.payload=='CELL' and s.gate_closed) or (s.payload=='RECEIVER' and s.receiver_clamp)):
   # A retained cell is isolated; a retained receiver mustfinishsupervisedreturn,
   # never autorun anothercell. No transfer bridge clearance is invented.
   return replace(s,fault=False,inhibited=True,isolation=True,common_path_clear=True),True
  return s,False
 if s.fault or not s.power:return s,False
 if event=='PROVE_RECOVERY_GATE_CLOSED' and s.isolation and s.payload=='CELL' and s.rear_boundary_retained:
  return replace(s,gate_closed=True),True
 if event=='PROVE_RECOVERY_EMPTY' and s.isolation and s.payload=='CELL' and not s.receiver_clamp:
  return replace(s,receiver_empty_proven=True),True
 if event=='PROVE_RECOVERY_HOME' and s.isolation and s.payload=='CELL' and s.gate_closed and s.receiver_empty_proven and s.common_path_clear:
  return replace(s,home_proven=True,docked=False),True
 if event=='ISOLATE_CELL' and s.isolation and s.payload=='CELL' and s.gate_closed and s.receiver_empty_proven and s.home_proven and s.common_path_clear and not s.docked:
  statuses=list(s.cell_status);statuses[s.cell_index]='ISOLATED'
  pending=[i for i,status in enumerate(statuses) if status=='STORED']
  if not pending:return replace(s,phase='COMPLETE',cell_status=tuple(statuses),cell_index=len(statuses)),True
  return replace(s,phase='STOWED',cell_status=tuple(statuses),cell_index=pending[0],isolation=False,released_count=0,common_path_clear=False,receiver_empty_proven=False,home_proven=False,rear_boundary_retained=True,receiver_clamp=False,inhibited=True),True
 if event=='PROVE_PATH' and s.phase=='STOWED':return replace(s,common_path_clear=True),True
 if event=='PROVE_EMPTY' and s.phase=='STOWED':return replace(s,receiver_empty_proven=True),True
 if event=='DOCK' and s.phase=='STOWED' and s.common_path_clear and s.receiver_empty_proven and not s.isolation:
  return replace(s,phase='DOCKED',docked=True),True
 if event=='CLOSE_FAR_STOP' and s.phase=='DOCKED' and s.docked and s.receiver_empty_proven:
  return replace(s,far_stop_closed=True,far_stop_proven=False),True
 if event=='PROVE_FAR_STOP' and s.phase=='DOCKED' and s.docked and s.far_stop_closed:
  return replace(s,far_stop_proven=True),True
 if event=='OPEN_GATE' and s.phase=='DOCKED' and s.docked and s.rear_boundary_retained and s.receiver_empty_proven and s.channel_closed and s.far_stop_closed and s.far_stop_proven and not s.host_burn_active:
  return replace(s,phase='GATE_OPEN',gate_closed=False),True
 if event=='FEED' and s.phase=='GATE_OPEN' and s.docked and s.rear_boundary_retained and s.channel_closed and s.far_stop_closed and s.far_stop_proven and not s.host_burn_active:
  return replace(s,phase='TRANSFER',payload='BRIDGE'),True
 if event=='PROVE_SEATED' and s.phase=='TRANSFER' and s.docked and s.channel_closed and s.far_stop_closed and s.far_stop_proven and not s.host_burn_active:
  return replace(s,phase='SEATED',payload='RECEIVER',payload_seated_proven=True),True
 if event=='CAPTURE' and s.phase=='SEATED' and s.docked and s.payload_seated_proven and s.far_stop_closed and s.far_stop_proven and not s.host_burn_active:
  # CAPTURE denotes independently proved near-tab closure, not merely a command.
  return replace(s,phase='CAPTURED',receiver_clamp=True),True
 if event=='RETRACT' and s.phase=='CAPTURED' and s.receiver_clamp:
  return replace(s,phase='RETRACTED',rear_boundary_retained=True),True
 if event=='CLOSE_GATE' and s.phase=='RETRACTED' and s.receiver_clamp:
  return replace(s,phase='CLOSED',gate_closed=True),True
 if event=='UNDOCK' and s.phase=='CLOSED' and s.gate_closed and s.receiver_clamp:
  return replace(s,phase='READY',docked=False),True
 if event=='CLUTCH_RELEASE' and s.phase=='READY' and s.receiver_clamp and s.gate_closed and not s.docked and not s.host_burn_active and s.host_attitude_stable and s.host_off_guard_elapsed_s>=p['host_off_guard_s']:
  return replace(s,index_clutch_engaged=False,clutch_engaged_proven=False,clutch_disengaged_proven=False),True
 if event=='PROVE_DISENGAGED' and s.phase=='READY' and not s.index_clutch_engaged:
  return replace(s,clutch_disengaged_proven=True,clutch_engaged_proven=False),True
 if event=='ARM' and s.phase=='READY' and s.gate_closed and s.receiver_clamp and s.common_path_clear and not s.isolation and not s.index_clutch_engaged and s.clutch_disengaged_proven and not s.host_burn_active and s.host_attitude_stable and s.host_off_guard_elapsed_s>=p['host_off_guard_s']:
  return replace(s,phase='ARMED',inhibited=False),True
 if event=='RELEASE' and s.phase=='ARMED' and not s.inhibited and s.receiver_clamp and s.gate_closed and s.common_path_clear and not s.index_clutch_engaged and s.clutch_disengaged_proven and not s.host_burn_active and s.host_attitude_stable and s.host_off_guard_elapsed_s>=p['host_off_guard_s']:
  statuses=list(s.cell_status);statuses[s.cell_index]='RELEASED'
  return replace(s,phase='RELEASED',payload='RELEASED',receiver_clamp=False,released_count=s.released_count+1,released_total=s.released_total+1,cell_status=tuple(statuses),receiver_empty_proven=False,home_proven=False,launch_module_stopped_proven=False,inhibited=True),True
 if event=='PROVE_LAUNCH_STOPPED' and s.phase=='RELEASED' and s.payload=='RELEASED':
  return replace(s,launch_module_stopped_proven=True),True
 if event=='CLUTCH_ENGAGE' and s.phase=='RELEASED' and s.launch_module_stopped_proven and s.payload=='RELEASED':
  return replace(s,index_clutch_engaged=True,clutch_engaged_proven=False,clutch_disengaged_proven=False),True
 if event=='PROVE_ENGAGED' and s.phase=='RELEASED' and s.index_clutch_engaged and s.launch_module_stopped_proven:
  return replace(s,clutch_engaged_proven=True,clutch_disengaged_proven=False),True
 if event=='RETURN_EMPTY' and s.phase=='RELEASED' and s.payload=='RELEASED' and s.gate_closed and s.inhibited and s.index_clutch_engaged and s.clutch_engaged_proven and s.launch_module_stopped_proven:
  return replace(s,phase='RETURNING',receiver_empty_proven=False,home_proven=False),True
 if event=='PROVE_RETURN_EMPTY' and s.phase=='RETURNING' and s.payload=='RELEASED' and not s.receiver_clamp:
  return replace(s,receiver_empty_proven=True),True
 if event=='HOME_PROVED' and s.phase=='RETURNING' and s.receiver_empty_proven and s.payload=='RELEASED':
  return replace(s,phase='HOME',home_proven=True,common_path_clear=True),True
 if event=='RESET_NEXT' and s.phase=='HOME' and s.home_proven and s.receiver_empty_proven and s.common_path_clear and s.gate_closed and s.inhibited and not s.isolation:
  pending=[i for i,status in enumerate(s.cell_status) if status=='STORED']
  if not pending:return replace(s,phase='COMPLETE',cell_index=len(s.cell_status)),True
  return replace(s,phase='STOWED',cell_index=pending[0],payload='CELL',rear_boundary_retained=True,receiver_clamp=False,released_count=0,receiver_empty_proven=False,home_proven=False,common_path_clear=False,far_stop_closed=False,far_stop_proven=False,payload_seated_proven=False),True
 return s,False

def logic_checks(manifest):
 N=len(manifest);initial=State(cell_status=('STORED',)*N)
 checks=[];snapshots=[];events=[];s=initial;manifest_sequences=[]
 # All four releases, returns and next-cell resets share one persistent state.
 for cell,size in enumerate(manifest):
  assert s.cell_index==cell and s.phase=='STOWED'
  case_events=[]
  for event in NORMAL:
   snapshots.append(s)
   s,allowed=step(s,event);assert allowed and invariant(s),(cell,event,s)
   case_events.append(event);events.append({'cell':cell+1,'event':event,'state':asdict(s)})
  assert s.released_total==cell+1
  manifest_sequences.append({'cell':cell+1,'size':size,'events':case_events,'cumulative_releases':s.released_total,'single_release':True})
 snapshots.append(s)
 assert s.phase=='COMPLETE' and s.released_total==N and s.cell_status==('RELEASED',)*N
 checks.append({'name':f'Persistent {N}-cell campaign with empty return and reset','cases':N,'pass':True,'scope':'One persistent state; every next-cell transition requires gate closure, returned receiver, empty proof, home proof and clear path'})
 tested=0;faultrecords=[]
 for base in snapshots[:-1]:
  for fault in FAULTS:
   fs,ok=step(base,fault);assert ok and invariant(fs)
   for command in NORMAL+RECOVERY:
    ns,allowed=step(fs,command);assert not allowed and ns==fs and invariant(ns)
    tested+=1
   restored,_=step(fs,'RESTORE_POWER');assert invariant(restored) and restored.fault and restored.inhibited
   for supervisor,pathproof in [(False,False),(True,False),(False,True)]:
    ns,allowed=step(restored,'RECOVER',supervisor,pathproof);assert not allowed and ns==restored
    tested+=1
   ns,allowed=step(restored,'RECOVER',True,True)
   if not ((restored.payload=='CELL' and restored.gate_closed) or (restored.payload=='RECEIVER' and restored.receiver_clamp)):assert not allowed and ns==restored
   else:assert allowed and ns.isolation and ns.inhibited and invariant(ns)
   faultrecords.append({'cell':base.cell_index+1,'phase':base.phase,'fault':fault,'retained_payload_location':fs.payload,'release_inhibited':fs.inhibited,'supervised_recovery_allowed':allowed,'remaining_path_rule':'A bridge jam or return fault requires supervised retrieval/rehome and fresh path/empty proof; no automatic clearance is created'})
 checks.append({'name':'Fault injection at every campaign phase including return','cases':len(faultrecords),'pass':True})
 checks.append({'name':'Unsafe commands and unsupervised recovery rejected','cases':tested,'pass':True})
 cross=0
 for base in snapshots:
  for event in NORMAL+FAULTS+RECOVERY+ENVIRONMENT+['RESTORE_POWER','RECOVER']:
   ns,ok=step(base,event);assert invariant(ns),(base,event,ns)
   if not ok:assert ns==base
   cross+=1
 checks.append({'name':'Every command applied at every campaign state','cases':cross,'pass':True})
 for _ in range(10):
  s,ok=step(s,'RELEASE');assert not ok and s.released_total==N
 checks.append({'name':'Repeated release cannot double feed','cases':10,'pass':True})
 unsafe=replace(initial,isolation=True,common_path_clear=True,receiver_empty_proven=True)
 assert not step(unsafe,'DOCK')[1]
 bridge=replace(initial,phase='TRANSFER',payload='BRIDGE',gate_closed=False,docked=True,far_stop_closed=True,far_stop_proven=True,fault=True)
 assert not step(bridge,'RECOVER',True,True)[1]
 checks.append({'name':'Failed-cell and bridge-isolation guards','cases':2,'pass':True})
 # Independently withhold each reset proof; no blind reset can move to nextcell.
 homes=[st for st in snapshots if st.phase=='HOME'];blind=0
 for home in homes:
  for field in ['home_proven','receiver_empty_proven','common_path_clear','gate_closed']:
   test=replace(home,**{field:False});ns,allowed=step(test,'RESET_NEXT');assert not allowed and ns==test
   blind+=1
 checks.append({'name':'Blind next-cell reset and missing proof rejection','cases':blind,'pass':True})
 false_empty=0
 for base in snapshots:
  if base.payload in ('BRIDGE','RECEIVER'):
   for command in ['PROVE_EMPTY','PROVE_RETURN_EMPTY','HOME_PROVED','RESET_NEXT']:
    ns,allowed=step(base,command);assert not allowed and ns==base
    false_empty+=1
 checks.append({'name':'Occupied receiver cannot be accepted as returned empty','cases':false_empty,'pass':True})
 # A securely retained failed cell can be isolated and the remaining three
 # cells processed on one persistent state, after explicit recovery proofs.
 iso=initial
 for event in ['PROVE_PATH','PROVE_EMPTY','SENSOR_DISAGREEMENT','RESTORE_POWER']:
  iso,allowed=step(iso,event);assert allowed and invariant(iso)
 iso,allowed=step(iso,'RECOVER',True,True);assert allowed and invariant(iso)
 assert not step(iso,'ISOLATE_CELL')[1]
 for event in RECOVERY:
  iso,allowed=step(iso,event);assert allowed and invariant(iso),(event,iso)
 assert iso.cell_status[0]=='ISOLATED' and iso.cell_index==1
 for cell in range(1,N):
  assert iso.cell_index==cell
  for event in NORMAL:
   iso,allowed=step(iso,event);assert allowed and invariant(iso)
 assert iso.phase=='COMPLETE' and iso.released_total==N-1 and iso.cell_status==('ISOLATED',)+('RELEASED',)*(N-1)
 checks.append({'name':'Verified-path failed-cell isolation then persistent remaining campaign','cases':1,'pass':True})
 # Coast-only payload transfer: empty docking may be safe under thrust,
 # but the storage gate cannot open until thrust is off. Seating is a sensor
 # proof; commanded pusher position is not taken as payload pose evidence.
 burn=initial;burn,allowed=step(burn,'HOST_BURN_ON');assert allowed
 for event in NORMAL[:5]:
  burn,allowed=step(burn,event);assert allowed and invariant(burn),(event,burn)
 assert burn.phase=='DOCKED' and burn.far_stop_proven and burn.host_burn_active
 assert not step(burn,'OPEN_GATE')[1] and not step(burn,'FEED')[1]
 burn,_=step(burn,'HOST_BURN_OFF')
 for _ in range(int(p['host_off_guard_s'])):burn,_=step(burn,'WAIT_HOST_GUARD')
 burn,_=step(burn,'PROVE_HOST_STABLE')
 for event in NORMAL[5:NORMAL.index('ARM')]:
  burn,allowed=step(burn,event);assert allowed and invariant(burn),(event,burn)
 burn,allowed=step(burn,'ARM');assert allowed
 unexpected,_=step(burn,'HOST_BURN_ON');assert unexpected.inhibited and unexpected.phase=='READY' and unexpected.fault
 assert not step(unexpected,'RELEASE')[1] and invariant(unexpected)
 burn,allowed=step(burn,'RELEASE');assert allowed and invariant(burn)
 checks.append({'name':'Coast-only transfer, far-stop proof and host-off launch interlock','cases':3,'pass':True})
 # An external burn restart resets the elapsed quiet-time proof. A stable
 # attitude bit cannot bypass the independently checked five-second clock.
 timing=replace(burn,phase='READY',payload='RECEIVER',receiver_clamp=True,released_count=0,released_total=0,cell_status=('STORED',)*N,host_attitude_stable=True,inhibited=True)
 for elapsed in [0.,p['host_off_guard_s']/2,p['host_off_guard_s']-1e-6]:
  early=replace(timing,host_off_guard_elapsed_s=elapsed)
  assert not step(early,'ARM')[1]
 restartable=replace(timing,index_clutch_engaged=True,clutch_engaged_proven=True,clutch_disengaged_proven=False)
 restarted,_=step(restartable,'HOST_BURN_ON');stopped,_=step(restarted,'HOST_BURN_OFF')
 assert stopped.host_off_guard_elapsed_s==0. and not step(stopped,'PROVE_HOST_STABLE')[1]
 assert not step(stopped,'ARM')[1]
 waited=stopped
 for _ in range(int(p['host_off_guard_s'])-1):
  waited,_=step(waited,'WAIT_HOST_GUARD');assert not step(waited,'PROVE_HOST_STABLE')[1] and not step(waited,'ARM')[1]
 waited,_=step(waited,'WAIT_HOST_GUARD');proved,ok=step(waited,'PROVE_HOST_STABLE');assert ok
 proved,allowed=step(proved,'CLUTCH_RELEASE');assert allowed
 proved,allowed=step(proved,'PROVE_DISENGAGED');assert allowed
 assert step(proved,'ARM')[1]
 checks.append({'name':'Five-second host-off guard, premature-arm rejection and restart reset','cases':10,'pass':True})
 clutch_cases=0
 for base in snapshots:
  if base.phase=='READY':
   if base.index_clutch_engaged or not base.clutch_disengaged_proven:
    assert not step(base,'ARM')[1];clutch_cases+=1
   wrong=replace(base,index_clutch_engaged=True,clutch_engaged_proven=True,clutch_disengaged_proven=False)
   assert not step(wrong,'PROVE_DISENGAGED')[1] and not step(wrong,'ARM')[1];clutch_cases+=1
  if base.phase=='RELEASED':
   for field in ['index_clutch_engaged','clutch_engaged_proven','launch_module_stopped_proven']:
    wrong=replace(base,**{field:False});assert not step(wrong,'RETURN_EMPTY')[1];clutch_cases+=1
 checks.append({'name':'Index-clutch disengagement before launch and proved engagement before return','cases':clutch_cases,'pass':True})
 containment_cases=0
 for base in snapshots:
  if base.phase=='DOCKED':
   for field in ['channel_closed','far_stop_closed','far_stop_proven']:
    wrong=replace(base,**{field:False});assert not step(wrong,'OPEN_GATE')[1];containment_cases+=1
  if base.phase=='TRANSFER':
   assert not step(base,'CAPTURE')[1] and not step(base,'RETRACT')[1];containment_cases+=1
  if base.phase=='SEATED':
   wrong=replace(base,payload_seated_proven=False);assert not step(wrong,'CAPTURE')[1];containment_cases+=1
 checks.append({'name':'Continuous containment, far-stop proof and sensed seating before capture','cases':containment_cases,'pass':True})
 return {'revision':'FDR10-LOGIC-R1','model':'Deterministic discrete-state interlock specification; not flight firmware or verified sensors','manifest':manifest,
  'nominal_sequence':events,'manifest_sequences':manifest_sequences,'final_campaign_state':asdict(s),'isolated_cell_campaign_final_state':asdict(iso),'fault_cases':faultrecords,'checks':checks,'assertion_case_count':sum(c['cases'] for c in checks),
  'all_assertions_pass':True,'host_operation_rule':{'payload_transfer':'Thrust-off/coast only. Storage gate cannot open under thrust; continuous capped channel and far-stop proof contain possible low-friction drift. Commanded pusher deceleration does not pull the satellite or establish its final pose.','launch':'Verified host burn OFF for >=5s and stable-attitude proof required; unexpected burn while armed inhibits release and resets the timer','guard_clock_model':'WAIT_HOST_GUARD advances an explicit one-second model tick while thrust is off; five consecutive ticks are required. Any restart resets elapsed time. This is a timed logic specification, not a flight clock implementation.','minimum_host_off_guard_s':p['host_off_guard_s'],'simulation_burn_case_m_s2':p['host_burn_logic_case_m_s2'],'host_acceleration_limit_m_s2_assumed':p['host_acceleration_limit_m_s2_assumed'],'base_resistance_N_assumed':p['base_axial_resistance_N_assumed']},'assumed_physical_contracts':['Continuous capped channel, fixed rear boundary and proved far receiver stops provide containment; near capture tabs close only after sensed seating. Pusher and normally engaged brake do not guarantee free-payload deceleration or pose.','Two independent position/path proof signals are truthful when agreement is accepted','Power loss inhibits release; the payload may coast within the contained transfer volume. Far-stop impacts, rebound and settling are not rated by the logic model.','Split-clutch limit proofs and external stopped-sled proof correspond to actual hardware state; launch dynamics are outside the feeder logic model','Control reset does not reset physical custody or assert path clearance without proof'],
  'fault_rule':'Any fault inhibits release and new feed. A failed cell remains isolated until independently proved common-path clearance and explicit supervised recovery. A bridge jam or return fault stops shared-path operations.',
  'limits':'No failure probability, hardware fault coverage, contact loads, friction distribution or sensor reliability is estimated. Common-cause false agreement and physical breakage remain hardware tests. Recovery after a return-phase fault requires supervised physical rehome and proof; normal automatic reset is prohibited.'}

def plots(sel,drives,mech):
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':200,'svg.fonttype':'none','pdf.fonttype':42,'ps.fonttype':42})
 names=[r['candidate'].replace('_',' ') for r in sel['ranking']];scores=[r['weighted_score_0_to_10'] for r in sel['ranking']]
 fig,ax=plt.subplots(figsize=(7,3.4));colors=['#164d68']+['#9ca9af']*6
 ax.barh(names[::-1],scores[::-1],color=colors[::-1]);ax.set_xlim(0,10);ax.set_xlabel('Weighted judgment score / 10')
 for i,s in enumerate(scores[::-1]):ax.text(s+.1,i,f'{s:.2f}',va='center',fontsize=9)
 ax.set_title('Feeder architecture trade — declared academic requirements',loc='left',fontsize=11)
 fig.text(.01,.01,'Safety 35% · Packaging 25% · Positioning 20% · Cycle/power 10% · Manufacture 10%\nEngineering judgments; scores do not measure reliability. FDR10 / D27-R2.',fontsize=8)
 fig.tight_layout(rect=(0,.10,1,1));fig.savefig(OUT/'feeder_trade.png');fig.savefig(OUT/'feeder_trade.svg');plt.close(fig)
 fig,axs=plt.subplots(1,2,figsize=(8,3.1))
 for ax,kind,label in zip(axs,['local_feed','common_receiver'],['200 mm local transfer','900 mm receiver indexing']):
  with (OUT/f'{kind}_50N.csv').open() as f:rs=list(csv.DictReader(f))
  ax.plot([float(r['t_s']) for r in rs],[float(r['position_mm']) for r in rs],color='#164d68',lw=1.8);ax.set_xlabel('Time / s');ax.set_ylabel('Position / mm');ax.set_title(label,loc='left',fontsize=10);ax.grid(axis='y',alpha=.18)
 fig.text(.01,.01,'Prescribed pusher/index kinematics; 50 N assumed resistance. Free-payload seating is sensed, not predicted.',fontsize=8)
 fig.tight_layout(rect=(0,.08,1,1));fig.savefig(OUT/'feeder_motion.png');fig.savefig(OUT/'feeder_motion.svg');plt.close(fig)

sel=selection();drives=[drive_screen(kind,F) for kind in ['local_feed','common_receiver'] for F in [p['nominal_axial_resistance_N'],p['adverse_axial_resistance_N']]];mech=mechanics();logic=logic_checks(p['manifest']);logic12=logic_checks(p['expanded_manifest'])
extended=[drive_screen('extended_receiver',F,p['expanded_receiver_stroke_mm'],p['expanded_receiver_time_s']) for F in [p['nominal_axial_resistance_N'],p['adverse_axial_resistance_N']]]
rack_reference=[drive_screen('rack_local_reference',F,p['feed_stroke_mm'],p['feed_time_s'],p['local_moving_mass_kg']) for F in [p['nominal_axial_resistance_N'],p['adverse_axial_resistance_N']]]
top3={'common_requirements':{'stroke_mm':p['feed_stroke_mm'],'time_s':p['feed_time_s'],'local_moving_mass_kg_assumed':p['local_moving_mass_kg'],'resistance_cases_N':[50,100],'source_motor':motor['id'],'gear_efficiency_assumed':p['gear_efficiency_assumed']},
 'lead_screw_cases':[r for r in drives if r['kind']=='local_feed'],
 'rack_reference_cases':rack_reference,'rack_interpretation':'Same motor family and 59.4 gearbox driving a12mmpitch-radius pinion. Conditional force/speed sizing only; tooth geometry,mesh,positive retention and installed support are not accepted by this calculation.',
 'spring_cases':[{'resistance_N':F,'old_end_force_N':15.,'old_force_to_demand_ratio':15/F,'end_force_shortfall_N':F-15.,'ideal_required_push_work_J':F*p['feed_stroke_mm']/1000,'minimum_new_end_force_N':F,'governor_requirement':'A resized spring must provide the full force floor over the stroke and limit motion to13.333mm/s under low resistance;storedenergy,captureandrewindlossesrequireseparatedesign.'} for F in [50.,100.]],
 'selection_interpretation':'All top-three architectures can be sized in principle. Lead screw is selected for direct reversible displacement and existing corrected guided CAD. The numerical screen alone does not establish a unique optimum.'}
(OUT/'TOP3_NUMERICAL.json').write_text(json.dumps(top3,indent=2)+'\n')
for name,obj in [('SELECTION.json',sel),('DRIVE_SCREENS.json',drives),('MECHANICS.json',mech),('SEQUENCE_FAULT_CHECKS.json',logic),('SEQUENCE_FAULT_CHECKS_12.json',logic12),('DRIVE_SCREENS_EXTENDED.json',extended)]:
 (OUT/name).write_text(json.dumps(obj,indent=2)+'\n')
if '--no-plots' not in sys.argv:plots(sel,drives,mech)
summary={'design_revision':p['design_revision'],'study_revision':p['study_revision'],'selected':'lead_screw','runner_up':'rack_pawl','ranking':[(r['candidate'],r['weighted_score_0_to_10']) for r in sel['ranking']],
 'nominal_drive_screens_pass':all(d['all_declared_sizing_screens_pass'] for d in drives if d['resistance_N']==p['nominal_axial_resistance_N']),
 'adverse_screens':[{k:d[k] for k in ['kind','resistance_N','criteria','all_declared_sizing_screens_pass']} for d in drives if d['resistance_N']==p['adverse_axial_resistance_N']],
 'logic_assertion_cases':logic['assertion_case_count'],'expanded_logic_assertion_cases':logic12['assertion_case_count'],'expanded_logic_pass':logic12['all_assertions_pass'],'expanded_drive_cases_pass':all(r['all_declared_sizing_screens_pass'] for r in extended),'logic_pass':logic['all_assertions_pass'],'geometry_signoff':'SeparateCAD/STEPpackage;mustbefinallylinkedbeforeacceptance',
 'contact_convergence':'OriginalFM06-R1Chronorigidcontactmodelremainsunconvergedandisnotusedforposeprecisionorpeakcontactloadacceptance',
 'parameters_sha256':hashlib.sha256(PAR.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'catalog_capture_sha256':hashlib.sha256(CAPTURE.read_bytes()).hexdigest()}
(OUT/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
