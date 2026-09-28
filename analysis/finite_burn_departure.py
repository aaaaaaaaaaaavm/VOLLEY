"""P113-S11: bounded planar finite-burn shooting with explicit slew time."""
import argparse,hashlib,itertools,json,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares
import terminal_timing as tt
import campaign_allocation as ca
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/results/finite_burn_departure.json'
DOC=ROOT/'docs/FINITE_BURN_DEPARTURE.md'
VE=tt.INPUTS['isp_s']*tt.G0
W=314.; RATE=math.radians(.5); ACCEL=math.radians(.05); SETTLE=30.


def slew(a,b):
    d=abs(math.atan2(math.sin(b-a),math.cos(b-a)))
    return 2*math.sqrt(d/ACCEL) if d<=RATE*RATE/ACCEL else d/RATE+RATE/ACCEL


def propagate(y,dt,F=0.,angle=0.,tight=False,mu=ca.MU):
    if dt<0 or not math.isfinite(dt) or F<0:raise ValueError('INVALID_SEGMENT')
    y=np.asarray(y,dtype=float)
    if not dt:return y.copy()
    if y[4]-F*dt/VE<=0:raise ValueError('NEGATIVE_MASS')
    unit=np.array([math.cos(angle),math.sin(angle)])
    def rhs(t,z):
        return np.r_[z[2:4],-mu*z[:2]/np.linalg.norm(z[:2])**3+F/z[4]*unit,-F/VE]
    s=solve_ivp(rhs,[0,dt],y,method='DOP853',rtol=2e-13 if tight else 2e-11,
        atol=[1e-7,1e-7,1e-10,1e-10,1e-11] if tight else [1e-5,1e-5,1e-8,1e-8,1e-9])
    if not s.success:raise ValueError('PROPAGATION_FAILURE')
    return s.y[:,-1]


def seed(time,u,F):
    d=json.loads((ROOT/'analysis/results/terminal_timing.json').read_text())
    row=next(r for r in d['transfers'] if r['target']=='phase_5km' and r['release_time_s']==time)
    arc=row['arcs'][0];dv1=np.array(arc['initial_correction_m_s']);mass=W*math.exp(-np.linalg.norm(dv1)/VE)
    sep=tt.separate(arc['arrival_state'],tt.target_state('phase_5km',time)[2:],mass,mass-304-2,(u,u))
    dv2=np.array(sep['second_correction_m_s']);axis=np.array(sep['relative_velocity_m_s'])/u
    burntime1=(W-mass)*VE/F;burntime2=(mass-sep['mass_after_second_kg'])*VE/F
    return np.array([math.atan2(dv1[1],dv1[0]),math.atan2(dv2[1],dv2[0]),burntime1,burntime2]),axis,dict(
        initial_delta_v_m_s=dv1.tolist(),second_delta_v_m_s=dv2.tolist(),fuel_kg=W-sep['mass_after_second_kg'])


def evaluate(x,time,u,F,axis,tight=False,terminal=False):
    a,b,d1,d2=map(float,x);release_angle=math.atan2(axis[1],axis[0]);turn=slew(b,release_angle)
    start2=time-turn-SETTLE-d2;gap=start2-d1;required=slew(a,b)+SETTLE
    y0=np.r_[tt.initial(),W];y1=propagate(y0,d1,F,a,tight)
    y2=propagate(y1,max(0.,gap),tight=tight);y3=propagate(y2,d2,F,b,tight)
    y4=propagate(y3,turn+SETTLE,tight=tight)
    m=y4[4];payload=y4[:4].copy();payload[2:]+=(1-4/m)*u*axis
    host=y4[:4].copy();host[2:]-=4/m*u*axis
    desired=tt.target_state('phase_5km',time)
    endpoint_perigee=min(ca.elements(y[:4])['perigee_m'] for y in (y0,y1,y2,y3,y4))
    dv1=VE*math.log(W/y1[4]);dv2=VE*math.log(y2[4]/m)
    violation=[max(0,required-gap)/10,max(0,306-m)*100,max(0,dv1-100),max(0,dv2-100),max(0,ca.RE+120000-endpoint_perigee)/100]
    residual=np.r_[(payload[:2]-desired[:2])/10,(payload[2:]-desired[2:])/.01,violation]
    errors=tt.terminal_errors(payload,desired)
    if terminal:
        end=propagate(np.r_[payload,4.],3600-time,tight=tight)[:4];errors=tt.terminal_errors(end,tt.target_state('phase_5km',3600))
    else:end=None
    return dict(parameters=x.tolist(),residual=residual.tolist(),fuel_used_kg=W-m,fuel_remaining_kg=m-304,
        first_burn_s=d1,second_burn_s=d2,second_burn_start_s=start2,
        first_to_second_available_s=gap,first_to_second_required_s=required,
        final_slew_s=turn,settle_s=SETTLE,minimum_endpoint_perigee_m=endpoint_perigee,
        integrated_delta_v_m_s=[dv1,dv2],service_pass=all(v<=1e-7 for v in violation),
        accepted=bool(errors['accepted'] and all(v<=1e-7 for v in violation)),errors=errors,
        terminal_state=end.tolist() if end is not None else None,payload_release_state=payload.tolist(),
        momentum_residual_kg_m_s=float(np.linalg.norm(4*payload[2:]+(m-4)*host[2:]-m*y4[2:4])))


def campaign(time,u,F):
    x,axis,impulse=seed(time,u,F)
    # One burn cannot exceed its declared duration or ideal impulse bound.
    maxduration=min(450.,W*(1-math.exp(-100/VE))*VE/F)
    lower=np.array([x[0]-math.pi,x[1]-math.pi,0,0]);upper=np.array([x[0]+math.pi,x[1]+math.pi,maxduration,maxduration])
    replay=evaluate(x,time,u,F,axis,terminal=True) if max(x[2:])<=maxduration else dict(accepted=False,reason='IMPULSE_EQUIVALENT_BURN_EXCEEDS_DURATION_OR_IMPULSE_BOUND',unclipped_parameters=x.tolist())
    base=np.clip(x,lower+1e-8,upper-1e-8);attempts=[]
    for delta in (0,.05,-.05):
        z=base.copy();z[0]+=delta;z[1]-=delta
        try:
            s=least_squares(lambda q:evaluate(q,time,u,F,axis)['residual'],z,bounds=(lower,upper),
                x_scale=[1,1,100,100],diff_step=1e-4,xtol=1e-9,ftol=1e-9,gtol=1e-9,max_nfev=120)
            row=evaluate(s.x,time,u,F,axis,terminal=True);row.update(seed_offset_rad=delta,nfev=s.nfev,solver_success=bool(s.success))
            attempts.append(row)
        except (ValueError,FloatingPointError) as exc:attempts.append(dict(seed_offset_rad=delta,accepted=False,reason=str(exc)))
    choices=[a for a in attempts if 'errors' in a]
    selected=min(choices,key=lambda a:(not a['accepted'],sum(v*v for v in a['residual']))) if choices else None
    numerical=None
    if selected:
        tight=evaluate(np.array(selected['parameters']),time,u,F,axis,tight=True,terminal=True)
        e=np.array(tight['terminal_state'])-selected['terminal_state']
        numerical=dict(position_m=float(np.linalg.norm(e[:2])),velocity_m_s=float(np.linalg.norm(e[2:])),passed=bool(np.linalg.norm(e[:2])<=.01 and np.linalg.norm(e[2:])<=1e-5))
    return dict(release_time_s=time,speed_m_s=u,thrust_N=F,axis=axis.tolist(),impulsive_reference=impulse,
        replay=replay,attempts=attempts,selected=selected,verification=numerical)


def checks():
    y=np.array([1e7,0,0,0,314.]);F=10.;dt=20
    r=propagate(y,dt,F,0,True,mu=0);expected=VE*math.log(y[4]/(y[4]-F*dt/VE))
    start=np.r_[tt.initial(),W];dv=1.;errors=[]
    for thrust in (1e4,1e5):
        duration=W*(1-math.exp(-dv/VE))*VE/thrust
        end=propagate(start,duration,thrust,math.pi/2,tight=True)
        instant=start.copy();instant[3]+=dv;instant[4]*=math.exp(-dv/VE)
        expected_state=propagate(instant,duration,tight=True)
        errors.append(float(np.linalg.norm(end[:4]-expected_state[:4])))
    return dict(rocket_identity=abs(r[2]-expected)<1e-8,mass_identity=abs(r[4]-(W-F*dt/VE))<1e-9,
        zero_duration=bool(np.array_equal(propagate(y,0),y)),impulse_limit=errors[1]<errors[0]/5,
        zero_slew=slew(0,0)==0,triangular_slew=abs(slew(0,ACCEL)-2)<1e-10,
        trapezoidal_slew=abs(slew(0,math.pi)-(math.pi/RATE+RATE/ACCEL))<1e-10)


def report(d):
    out=['# Finite-duration host burns and slew-constrained departure','','Adityavardhan Mishra · 17 September 2026','',
        'I replace two ideal impulses with integrated fixed-thrust arcs and mass flow. Every case includes two rest-to-rest slew budgets and settling; the initial attitude is pre-positioned. The assumed planar actuator law is not flight ADCS or a three-axis rigid-body solution.','',
        '| Release (s) | Speed (m/s) | Thrust (N) | Replay | Replan | Fuel used (kg) | Terminal position (m) |','|---:|---:|---:|---|---|---:|---:|']
    for r in d['cases']:
        s=r['selected'];out.append(f"| {r['release_time_s']} | {r['speed_m_s']:g} | {r['thrust_N']:g} | {'pass' if r['replay']['accepted'] else 'fail'} | {'pass' if s and s['accepted'] else 'no accepted result'} | {s['fuel_used_kg'] if s else float('nan'):.6f} | {s['errors']['position_error_m'] if s else float('nan'):.6f} |")
    out+=['','Each result retains three bounded search attempts and explicit burn, slew, fuel and endpoint-perigee accounting. A failed bounded search is not proof that no trajectory exists. Full twelve-payload replanning, navigation uncertainty, physical attitude torque/momentum, plume clearance, flexible dynamics and disposal remain open.','',
        'The release speeds are mission assumptions. P92-S5 supplies separate force-law candidates; it does not establish the accuracy or installed burden required by this mission.','',
        f"Numerical verification: {'PASS' if all(d['verification'].values()) else 'FAIL'}. Physical mission acceptance uses unchanged 10 m / 0.01 m/s terminal bands and 2 kg reserve.",'',
        '[Criteria](../validation/P113_S11_finite_burn.md) · [Complete attempts](../analysis/results/finite_burn_departure.json)','']
    return '\n'.join(out)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
    paths=['analysis/finite_burn_departure.py','analysis/terminal_timing.py','analysis/campaign_allocation.py','analysis/host_reference.py','analysis/results/terminal_timing.json','validation/P113_S11_finite_burn.md']
    hashes={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in paths}
    if args.check:
        d=json.loads(OUT.read_text());assert d['source_sha256']==hashes and DOC.read_text()==report(d),'stale artifacts';assert all(checks().values())
    else:
        rows=[]
        for t,u,F in itertools.product((1200,1800),(1.,2.),(1.,10.,100.)):
            rows.append(campaign(t,u,F));print(t,u,F,rows[-1]['selected']['accepted'] if rows[-1]['selected'] else None,flush=True)
        v={k:bool(value) for k,value in checks().items()};v['tight_propagation']=all(r['verification'] and r['verification']['passed'] for r in rows)
        d=dict(study='P113-S11',cases=rows,verification=v,source_sha256=hashes)
        OUT.write_text(json.dumps(d,sort_keys=True,indent=2)+'\n');DOC.write_text(report(d))
    print(d['verification']);assert all(d['verification'].values())
