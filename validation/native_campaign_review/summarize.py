"""Read native outputs; derive explicit metrology and thrust-time requirements."""
from pathlib import Path
import csv,json,math,hashlib,itertools
H=Path(__file__).resolve().parent;O=H/'full'
D=json.loads((O/'RESULTS.json').read_text());records=D['cases']
get=lambda case,probe,step=60:next(r for r in records if r['case']==case and r['probe']==probe and r['maximum_step_s']==step)
FAIR=['4_spring_10kg','4_volley_3_6_10kg','12_spring_20kg','12_volley_3_6_20kg']


def states(stem,kind):
    return list(csv.DictReader((O/(stem+'_'+kind+'.csv')).open()))


def difference(a,b,columns):
    return math.sqrt(sum((float(a[c])-float(b[c]))**2 for c in columns))


refinements=[]
for name in FAIR[2:]:
    base=f'{name}_nominal_step60';fine=f'{name}_nominal_step30'
    p,q=states(base,'payload'),states(fine,'payload')
    host0,host1=states(base,'host'),states(fine,'host')
    assert [x['payload'] for x in p]==[x['payload'] for x in q]
    refinements.append({'case':name,'max_payload_position_change_m':max(difference(a,b,['x_m','y_m','z_m']) for a,b in zip(p,q)),
       'max_payload_velocity_change_m_s':max(difference(a,b,['vx_m_s','vy_m_s','vz_m_s']) for a,b in zip(p,q)),
       'max_host_position_change_m':max(difference(a,b,['x_m','y_m','z_m']) for a,b in zip(host0,host1))})

categories={'release ±1%':['shot_plus_1pct','shot_minus_1pct'],'release +0.1%':['shot_plus_0p1pct'],
 'in-plane ±0.1°':['pitch_plus_0p1deg','pitch_minus_0p1deg'],'out-of-plane ±0.1°':['yaw_plus_0p1deg','yaw_minus_0p1deg'],
 'host burn ±0.1%':['burn_plus_0p1pct','burn_minus_0p1pct'],'shot delay +5ms':['shot_delay_5ms'],'shot delay +50ms':['shot_delay_50ms']}
sensitivity=[{'case':name,'category':category,'position_error_m':max(get(name,p)['max_payload_position_error_m'] for p in probes),
              'velocity_error_m_s':max(get(name,p)['max_payload_velocity_error_m_s'] for p in probes),
              'interpretation':'Maximum across the explicit signed probes and payloads; not a worst-case uncertainty bound'}
             for name in FAIR for category,probes in categories.items()]

metrology=[]
for speed,baseline_mm,length_error_mm,jitter_us,temperature_error_K in itertools.product([3,6,9],[50,100,200],[.005,.01,.05],[.1,1,10],[0,.1,1,10]):
    L=baseline_mm/1000;dt=L/speed;timestamp_bound=2*jitter_us*1e-6
    thermal_mm=23e-6*baseline_mm*temperature_error_K
    distance_bound=(length_error_mm+thermal_mm)/1000
    assert dt>timestamp_bound
    vlo=(L-distance_bound)/(dt+timestamp_bound);vhi=(L+distance_bound)/(dt-timestamp_bound)
    bound=max(speed-vlo,vhi-speed)
    metrology.append({'coasting_speed_m_s':speed,'baseline_mm':baseline_mm,'baseline_calibration_bound_mm':length_error_mm,
       'single_timestamp_bound_us':jitter_us,'residual_temperature_bound_K':temperature_error_K,'assumed_CTE_K':23e-6,
       'thermal_baseline_bound_mm':thermal_mm,'absolute_speed_bound_m_s':bound,'relative_speed_bound':bound/speed,
       'boundary':'Exact interval arithmetic for constant velocity and stipulated measurement bounds; detector,alignment,edge geometry,tip-off,calibration and installation errors otherwise unmodeled. Not a measured or rated instrument.'})

accuracy=[]
for name in FAIR:
    probe=get(name,'shot_plus_0p1pct');large=get(name,'shot_plus_1pct')
    ratio=10*probe['max_payload_position_error_m']/large['max_payload_position_error_m']
    for pos,vel in [(10,.01),(100,.1),(1000,1)]:
        fraction=.001*min(pos/probe['max_payload_position_error_m'],vel/probe['max_payload_velocity_error_m_s'])
        accuracy.append({'case':name,'illustrative_position_band_m':pos,'illustrative_velocity_band_m_s':vel,
          'linearized_common_release_bias_fraction':fraction,'linearity_ratio_0p1pct_vs_1pct':ratio,
          'boundary':'Illustrative common-epoch full-state box; not customer requirements. Linearization allocates the entire budget to a common release bias with other errors zero; no service acceptance or guarantee.'})

thrust=[]
for name in FAIR:
    event_rows=list(csv.DictReader((H/'events'/(name+'_events.csv')).open()))
    burns=[r for r in event_rows if r['kind']=='burn']
    for force in [.1,1,5,20,100]:
        durations=[(float(r['mass_before_kg'])-float(r['mass_after_kg']))*220*9.80665/force for r in burns]
        pre=[duration for duration,row in zip(durations,burns) if float(row['t_s'])<=3600]
        thrust.append({'case':name,'equivalent_resultant_thrust_N':force,'total_thrust_on_s':sum(durations),
            'thrust_on_before_final_release_s':sum(pre),'longest_single_burn_s':max(durations),
            'violates_3600s_pre_final_release_necessary_time':sum(pre)>3600,
            'violates_4200s_total_reference_recovery_time':sum(durations)>4200,
            'boundary':'Necessary total-time screen for one equivalent constant-thrust,Isp220s system using prescribed impulse fuel amounts. No finite-burn retargeting,coast/slew/plume scheduling or actual engine selection. Not ruled out is not feasible.'})

dynamic_metrology=[]
for speed,baseline_mm,acceleration,rate_error_deg_s in itertools.product([3,6],[50,100,200,300,500,900],[0,.001,.01],[0,.001,.01]):
    L=baseline_mm/1000
    # Comparison bounds on transit time with |a_relative| <= the stipulated limit.
    tmin=2*L/(speed+math.sqrt(speed**2+2*acceleration*L))
    tmax=2*L/(speed+math.sqrt(speed**2-2*acceleration*L))
    delta_length=(.01+23e-6*baseline_mm*.1)/1000
    delta_time=2*.1e-6
    instrument_bound=(L+delta_length)/(tmin-delta_time)-L/tmin
    mean_to_exit=acceleration*tmax/2
    frame_bound=math.radians(rate_error_deg_s)*.5
    bound=instrument_bound+mean_to_exit+frame_bound
    # Independent exact constant-acceleration corners exercise the conditional bound.
    for sign,length_sign,time_sign in itertools.product([-1,1],repeat=3):
        a=sign*acceleration
        duration=2*L/(speed+math.sqrt(speed**2+2*a*L))
        exit_speed=speed+a*duration
        measured=(L+length_sign*delta_length)/(duration+time_sign*delta_time)
        assert abs(measured-exit_speed)<=instrument_bound+mean_to_exit+1e-10
    dynamic_metrology.append({'coasting_entry_speed_m_s':speed,'baseline_mm':baseline_mm,
        'relative_acceleration_bound_m_s2':acceleration,'rate_uncertainty_deg_s':rate_error_deg_s,
        'lever_arm_m':.5,'baseline_calibration_bound_mm':.01,'timestamp_bound_us':.1,'temperature_bound_K':.1,
        'instrument_only_bound_m_s':instrument_bound,'mean_to_exit_bound_m_s':mean_to_exit,
        'frame_compensation_bound_m_s':frame_bound,'total_exit_speed_bound_m_s':bound,
        'relative_exit_speed_bound':bound/speed,
        'boundary':'Conditional one-dimensional monotonic transit plus stipulated frame-rate/lever-arm bound. Real optical edge,geometry,contact,attitude and calibration are unverified; no flight precision pass.'})

summary={'revision':'CNR-01-2026-10-19','native_case_count':len(records),'nominal_crosschecks':[get(name,'nominal') for name in FAIR],
 'refinement':refinements,'sensitivity':sensitivity,'metrology':metrology,'dynamic_metrology':dynamic_metrology,'accuracy_allocations':accuracy,'thrust_time':thrust,
 'source_identities':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [H/'CoupledEvents.java',H/'run_full_campaign.py',H/'export_campaign.py',Path(__file__)]},
 'boundary':'Native numerical consistency and prescribed-control sensitivity; no physical flight/velocity accuracy. Metrology and thrust screens use provisional inputs,not source-rated hardware.'}
(O/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print('Postprocessed',len(records),'native cases;',len(metrology),'metrology intervals;',len(thrust),'necessary thrust-time cases')
