"""ACR1 same-input synthetic mission comparison, derived from FBR target.py.

Uses its captured J2/DOP853 arc implementation, finite force and Isp mass flow.
All new writes are confined to this mission directory.
"""
from pathlib import Path
import csv,hashlib,importlib.util,json,math,sys,time
import numpy as np
from scipy.optimize import root

H=Path(__file__).resolve().parent;ROOT=H.parent
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('captured_fbr_arc',H/'provenance/target.py');reference=importlib.util.module_from_spec(spec);spec.loader.exec_module(reference)
arc=reference.arc
MU,RE,J2,ISP,G0=reference.MU,reference.RE,reference.J2,reference.ISP,reference.G0
CAD_DEVICE=149.5567197004;GEN5_DEVICE=CAD_DEVICE+7.;SPRING_DEVICE=72.;SLED=13.127805767068676;PAYLOAD=4.
BUS_DRY=480.;PROPELLANT=20.;INITIAL_WET_BUS=BUS_DRY+PROPELLANT
TIMES=np.arange(1,13)*450.;LAST=float(TIMES[-1]);FINAL=LAST+86400.;PRE_GUARD=5.;POST_GUARD=20.;LOADING_COAST=400.
RADIUS=RE+500000.;PERIOD=2*np.pi*np.sqrt(RADIUS**3/MU)
SUN_RATE=2*np.pi/(365.2422*86400.)
INCLINATION=np.arccos(-SUN_RATE/(1.5*np.sqrt(MU/RADIUS**3)*J2*(RE/RADIUS)**2))
INITIAL=np.array([RADIUS,0,0,0,np.sqrt(MU/RADIUS)*np.cos(INCLINATION),np.sqrt(MU/RADIUS)*np.sin(INCLINATION)])

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def calibration():
    p=ROOT/'analysis/COUPLED_SHOT.json';d=json.loads(p.read_text());rows=sorted([r for r in d['cases']if not r['adverse']and r['inductance_H']==20e-6 and r['target_m_s']in[1,2,3]],key=lambda r:r['target_m_s'])
    assert len(rows)==3 and all(r['all_declared_checks_pass']for r in rows)
    return np.array([r['target_m_s']for r in rows]),np.array([r['release']['relative_speed_m_s']for r in rows]),dict(source_relative_path=str(p.relative_to(ROOT)),source_sha256=sha(p),production_model_sha256=d['source_sha256'],nominal_inductance_H=20e-6,reference_rows=rows)

COMMANDS,MEASURED,CALIBRATION=calibration()

def make_targets():
    """Targets do not use either device mass, recoil mapping or force schedule."""
    families={}
    for name,kicks in [('uniform_2',np.full(12,2.)),('alternating_1_3',np.tile([1.,3.],6))]:
        shots=[]
        for i,(t,q)in enumerate(zip(TIMES,kicks),1):
            chief=arc(INITIAL,0,float(t));r=chief[:3];v=chief[3:];radial=r/np.linalg.norm(r);normal=np.cross(r,v);normal/=np.linalg.norm(normal);along=np.cross(normal,radial)
            desired=chief.copy();desired[3:]+=q*along;target=arc(desired,float(t),FINAL)
            shots.append(dict(payload=i,t=float(t),m=PAYLOAD,q_m_s=float(q),direction=along.tolist(),chief_release=chief.tolist(),desired_release=desired.tolist(),target=target.tolist()))
        families[name]=dict(name=name,shots=shots,initial=INITIAL.tolist(),host_target=arc(INITIAL,0,FINAL).tolist())
    d=dict(study='G5-MISSION-01',construction='Chief J2 coast from common500km nominal SSO. At each fixed release epoch, add synthetic +along-track1/2/3m/s inertial velocity increment to chief PV. Propagate that full PV under J2 to the common24h-after-last-release epoch. No architecture mass or thrust authority enters target construction.',epoch_TAI='2026-10-24T00:00:00',initial_PV=INITIAL.tolist(),nominal_altitude_m=500000.,first_order_J2_SSO_inclination_deg=float(np.degrees(INCLINATION)),Kepler_period_s=float(PERIOD),release_times_s=TIMES.tolist(),final_epoch_s=FINAL,families=families)
    (H/'TARGETS.json').write_text(json.dumps(d,indent=2)+'\n');return d

def separation(architecture,shot,mass):
    q=shot['q_m_s'];direction=np.array(shot['direction'])
    if architecture=='gen5':
        rest=mass-PAYLOAD-SLED
        requested_measured=q*mass/rest
        command=float(np.interp(requested_measured,MEASURED,COMMANDS));measured=float(np.interp(command,COMMANDS,MEASURED))
        speed=measured*rest/(mass-PAYLOAD)
        return speed*direction,dict(command_m_s=command,measured_release_m_s=measured,retained_rest_kg=rest,reusable_sled_kg=SLED,mapping='u_sep=measured_release*(Mbefore−payload−sled)/(Mbefore−payload)')
    if architecture=='spring_fixed2':speed=2.
    elif architecture=='spring_pretrim':speed=q*mass/(mass-PAYLOAD)
    else:raise ValueError(architecture)
    return speed*direction,dict(command_m_s=speed,measured_release_m_s=None,retained_rest_kg=None,reusable_sled_kg=0.,mapping='Frozen per-payload relative separation speed; no reusable moving sled',ground_pretrim_energy_J=.5*PAYLOAD*(mass-PAYLOAD)/mass*speed**2)

def leg(s,a,b,target,architecture,shot,fraction,step,shared_narrow=False):
    guard=PRE_GUARD if shot else 0.;end=b-guard;duration=end-a
    d=min(fraction*duration,(duration-LOADING_COAST)/2)if(architecture=='gen5'or shared_narrow)and shot else fraction*duration
    assert d>0,(a,b,d)
    times=[a,a+d,end-d,end];dt=b-a
    def goal(mass):
        vgoal=np.array(target[3:]).copy()
        if shot:
            u,_=separation(architecture,shot,mass);vgoal-=(1-PAYLOAD/mass)*u
        return vgoal
    end0=arc(s,a,b,step=step);dr=np.array(target[:3])-end0[:3];dv=goal(s[6])-end0[3:6]
    mat=np.array([[d*(dt-d/2),d*(guard+d/2)],[d,d]])/s[6];seed=np.linalg.solve(mat,np.stack([dr,dv])).reshape(6)
    def propagate(x):
        z=arc(s,a,times[1],x[:3],step);z=arc(z,times[1],times[2],step=step);z=arc(z,times[2],end,x[3:],step);return arc(z,end,b,step=step)
    def residual(x):
        z=propagate(x);return np.r_[(z[:3]-target[:3])/dt,z[3:6]-goal(z[6])]
    sol=root(residual,seed,method='hybr',options={'xtol':1e-9,'eps':1e-6});z=propagate(sol.x);r=residual(sol.x)
    return dict(end=z,force=sol.x.reshape(2,3),times=times,coast_s=times[2]-times[1],position_residual_m=float(np.linalg.norm(r[:3])*dt),velocity_residual_m_s=float(np.linalg.norm(r[3:])),root_success=bool(sol.success),root_message=str(sol.message),evaluations=int(sol.nfev),targeting_pass=bool(np.linalg.norm(r[:3])*dt<.001 and np.linalg.norm(r[3:])<1e-6))

def run(family,architecture,fraction=.35,step=60.,shared_narrow=False):
    started=time.monotonic();device=GEN5_DEVICE if architecture=='gen5'else SPRING_DEVICE;s=np.r_[INITIAL,INITIAL_WET_BUS+device+12*PAYLOAD];initial=s.copy();now=0.;events=[];deliveries=[];legs=[];trajectory=[]
    def segment(a,b,F,label):
        nonlocal s
        if b-a<1e-9:return
        before=s.copy();sol=arc(s,a,b,F,step,True);s=sol.y[:,-1]
        events.append(dict(kind='arc',start_s=a,end_s=b,force_N=list(F),before=before.tolist(),after=s.tolist(),label=label))
        for t in np.linspace(a,b,max(2,int((b-a)/30)+1)):trajectory.append([float(t),*map(float,sol.sol(t))])
    for i,shot in enumerate(family['shots']+[None]):
        end=shot['t']if shot else float(PERIOD)
        if now>0:segment(now,now+POST_GUARD,np.zeros(3),'post_release_guard');now+=POST_GUARD
        target=np.array(shot['desired_release'])if shot else arc(INITIAL,0,end,step=step)
        found=leg(s,now,end,target,architecture,shot,fraction,step,shared_narrow);legs.append({k:(v.tolist()if isinstance(v,np.ndarray)else v)for k,v in found.items()if k!='end'})
        if not found['targeting_pass']:break
        ts=found['times'];Fs=found['force'];segment(ts[0],ts[1],Fs[0],'first_force_window');segment(ts[1],ts[2],np.zeros(3),'loading_coast'if shot and architecture=='gen5'else'inter_window_coast');segment(ts[2],ts[3],Fs[1],'second_force_window')
        if shot:
            segment(ts[3],end,np.zeros(3),'pre_release_zero_force_guard');before=s.copy();M=s[6];u,release=separation(architecture,shot,M);child=s[:6].copy();child[3:]+=(1-PAYLOAD/M)*u;parent=s[3:6]-PAYLOAD/M*u
            momentum=PAYLOAD*child[3:]+(M-PAYLOAD)*parent-M*s[3:6];terminal=arc(child,end,FINAL,step=step);goal=np.array(shot['target']);s[3:6]=parent;s[6]-=PAYLOAD
            deliveries.append(dict(payload=shot['payload'],release_s=end,child_state=child.tolist(),target=goal.tolist(),terminal_state=terminal.tolist(),position_error_m=float(np.linalg.norm(terminal[:3]-goal[:3])),velocity_error_m_s=float(np.linalg.norm(terminal[3:]-goal[3:])),momentum_error_kg_m_s=float(np.linalg.norm(momentum)),u_sep_m_s=u.tolist(),mass_before_kg=M,**release))
            events.append(dict(kind='shot',start_s=end,end_s=end,payload=shot['payload'],payload_mass_kg=PAYLOAD,u_m_s=u.tolist(),before=before.tolist(),after=s.tolist(),target=goal.tolist(),**release))
        now=end
    completed=len(deliveries)==12 and len(legs)==13 and all(q['targeting_pass']for q in legs)
    if completed:segment(now,FINAL,np.zeros(3),'final_host_coast')
    used=initial[6]-s[6]-len(deliveries)*PAYLOAD;peak=max((np.linalg.norm(F)for q in legs for F in q['force']),default=0.)
    r=dict(study='G5-MISSION-01',family=family['name'],architecture=architecture,fraction=fraction,max_step_s=step,source_sha256=sha(__file__),targets_sha256=sha(H/'TARGETS.json'),calibration_source_sha256=CALIBRATION['source_sha256'],initial_time_s=0.,initial_state=initial.tolist(),initial_bus_dry_kg=BUS_DRY,initial_propellant_kg=PROPELLANT,initial_bus_wet_kg=INITIAL_WET_BUS,device_retained_dry_kg=device,payload_total_kg=48.,final_time_s=FINAL,final_host_target=family['host_target'],final_host_state=s.tolist(),legs=legs,events=events,deliveries=deliveries,completed_targeting=completed,fuel_used_kg=float(used),fuel_remaining_kg=float(PROPELLANT-used),peak_force_N=float(peak),fuel_limit_pass=bool(used<=PROPELLANT),host_position_error_m=float(np.linalg.norm(s[:3]-family['host_target'][:3]))if completed else None,host_velocity_error_m_s=float(np.linalg.norm(s[3:6]-family['host_target'][3:]))if completed else None,minimum_loading_coast_s=min([q['coast_s']for q in legs[:12]])if architecture=='gen5'else None,elapsed_s=time.monotonic()-started)
    r['authority_results']={str(limit):dict(force_limit_N=limit,force_limit_pass=bool(peak<=limit),feasible_in_declared_candidate=bool(completed and used<=PROPELLANT and peak<=limit))for limit in [1.,5.]}
    r['shared_narrow_window_policy']=bool(shared_narrow or architecture=='gen5');r['spring_loading_coast_required']=False
    stem=case_stem(r);r['case_stem']=stem;out=H/'release';out.mkdir(exist_ok=True);(out/(stem+'.json')).write_text(json.dumps(r,indent=2)+'\n');np.savetxt(out/(stem+'_trajectory.csv'),trajectory,delimiter=',',header='t_s,x_m,y_m,z_m,vx_m_s,vy_m_s,vz_m_s,mass_kg',comments='')
    print(json.dumps(dict(case=stem,completed=completed,peak_force_N=peak,fuel_used_kg=used,host_error_m=r['host_position_error_m'],elapsed_s=r['elapsed_s'])),flush=True);return r

def case_stem(r):
    return f"{r['family']}_{r['architecture']}_f{r['fraction']:g}"+('_shared_narrow'if r.get('shared_narrow_window_policy')and r['architecture']!='gen5'else'')

def export_case(r,path):
    with Path(path).open('w')as f:
        w=csv.writer(f);w.writerow(['start_s','end_s','kind','payload','payload_mass_kg','fx_or_ux','fy_or_uy','fz_or_uz','mass_after_kg','rx','ry','rz','vx','vy','vz','target_rx','target_ry','target_rz','target_vx','target_vy','target_vz','label','architecture','measured_release_m_s','reusable_sled_kg'])
        w.writerow([0,0,'initial',0,0,0,0,0,r['initial_state'][6],*r['initial_state'][:6],*r['final_host_target'],'initial',r['architecture'],0,0])
        for e in r['events']:w.writerow([e['start_s'],e['end_s'],e['kind'],e.get('payload',0),e.get('payload_mass_kg',0),*e.get('force_N',e.get('u_m_s',[0,0,0])),e['after'][6],*e['after'][:6],*e.get('target',[0]*6),e.get('label','shot'),r['architecture'],e.get('measured_release_m_s')or 0,e.get('reusable_sled_kg',0)])

if __name__=='__main__':
    d=make_targets();(H/'CALIBRATION.json').write_text(json.dumps(CALIBRATION,indent=2)+'\n');results=[]
    for family in d['families'].values():
        for arch in ['gen5','spring_fixed2','spring_pretrim']:
            for fraction,narrow in ([(.35,True)]if arch=='gen5'else[(.35,True),(.35,False),(.45,False)]):
                r=run(family,arch,fraction,shared_narrow=narrow);export_case(r,H/'release'/(r['case_stem']+'.csv'));results.append({k:v for k,v in r.items()if k not in ['legs','events','deliveries']})
    summary=dict(study='G5-MISSION-01',cases=results,construction=d['construction'],force_authority_cases_N=[1,5],spring_fixed_speed_basis='Declared neutral2m/s midpoint class assumption; no vendor quote.',spring_pretrim_basis='Analytical per-payload separation energy compensates predictable finite-host recoil for requested targetkick; table frozen after planning before native replay. It supplies no inflightretasking.',Gen5_coast_allocation_s=400,declared_worst_cycle_s=355,common_pre_post_guards_s=[5,20],limitations=['Two-window policies and sampled fractions are constructed candidates, not global optima.','Bounded candidate failure at a force ceiling is not a global infeasibility proof.','Fixed-axis J2 without drag or third bodies; constant inertial force and Isp220s surrogate host hardware.','Synthetic target families are not customer requirements or an orbital safety/conjunction assessment.'])
    (H/'MISSION_COMPARISON.json').write_text(json.dumps(summary,indent=2)+'\n')
