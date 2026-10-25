"""Finite lunar host campaign with exact split, fuel, inertia and attitude recovery.

Release is the accepted ACR1 post-arrest point-event map. This is an operational
campaign model, not a physical six-DOF contact/pulse qualification. Finite attitude
preparation, free drift, angular-momentum removal, body-axis propulsion, custody
time, and source/propellant budgets are explicitly counted.
"""
import copy
import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.spatial.transform import Rotation

HERE=Path(__file__).resolve().parent
G0=9.80665


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def par(r):return np.dot(r,r)*np.eye(3)-np.outer(r,r)
def norm(v):return float(np.linalg.norm(v))
def unit(v):return np.asarray(v)/norm(v)
def fcurve(s):return 10*s**3-15*s**4+6*s**5
def dfcurve(s):return 30*s**2-60*s**3+30*s**4
def ddfcurve(s):return 60*s-180*s**2+120*s**3


def qdot(q,omega):
    xyz=q[:3];w=q[3]
    return .5*np.r_[w*omega+np.cross(omega,xyz),-np.dot(omega,xyz)]


class Campaign:
    def __init__(self,config,authority,step=30):
        self.c=config;self.a=authority;self.step=step
        self.l=json.loads((HERE/'study_inputs.json').read_text())['lunar']
        self.mu=self.l['mu_moon_km3_s2']*1e9;self.radius=self.l['reference_radius_km']*1000
        origin=np.array(config['core_CG_reference_in_ACR1_CAD_m'])
        sig=json.loads((HERE/'inputs/SIGNATURES_home.json').read_text())
        self.manifest=[]
        for o in sig['objects']:
            if '_Stored_3U' in o['name']:
                self.manifest.append(dict(id=o['name'],r=np.array(o['solids'][0]['centre_mm'])/1000-origin,
                                          command=config['manifest_commands_m_s_by_level'][int(o['name'].split('_L')[1][0])]))
        self.manifest.sort(key=lambda x:x['id'])
        sig=json.loads((HERE/'inputs/SIGNATURES_release.json').read_text())
        self.release_r=next(np.array(o['solids'][0]['centre_mm'])/1000-origin for o in sig['objects'] if o['name']=='Transferred_3U')
        self.moving=json.loads((HERE/'inputs/RESOURCE_LEDGER.json').read_text())['moving_sled_with_pallet_kg']
        coupled=json.loads((HERE/'inputs/COUPLED_SHOT.json').read_text())['cases']
        self.cal={u:next(x for x in coupled if x['target_m_s']==u and not x['adverse'] and x['inductance_H']==20e-6) for u in [1,2,3]}
        self.source_energy={u:max(x['cap_draw_J'] for x in coupled if x['target_m_s']==u) for u in [1,2,3]}
        self.child_I=np.diag([4*(.1**2+.1**2)/12,4*(.3405**2+.1**2)/12,4*(.3405**2+.1**2)/12])
        self.Icore=np.array(config['core_inertia_about_reference_kg_m2'],dtype=float)*authority['inertia_scale']
        ra=self.radius+config['staging_apolune_km']*1000;rp=self.radius+config['staging_perilune_km']*1000
        self.initial=np.array([-ra,0,0,0,0,-math.sqrt(self.mu*(2/ra-2/(rp+ra)))])
        self.times=np.arange(1,13)*config['release_spacing_s']
        self.chief=solve_ivp(lambda t,y:np.r_[y[3:],-self.mu*y[:3]/norm(y[:3])**3],[0,self.times[-1]],self.initial,
                             method='DOP853',rtol=2e-12,atol=1e-8,max_step=60,dense_output=True)
        self.targets=[]
        for t in self.times:
            state=self.chief.sol(t);normal=unit(np.cross(state[:3],state[3:]));along=unit(np.cross(normal,state[:3]))
            self.targets.append((along,normal))

    def mass_props(self,remaining,prop):
        total=self.c['core_dry_mass_kg']+prop+4*len(remaining)
        total_first=sum((4*self.manifest[i]['r'] for i in remaining),start=np.zeros(3))
        center=total_first/total
        inertia=self.Icore.copy()
        for i in remaining:inertia+=self.child_I+4*par(self.manifest[i]['r'])
        inertia-=total*par(center)
        assert np.linalg.eigvalsh(inertia).min()>0
        return total,center,inertia

    def target_rotation(self,slot,sign,roll):
        along,normal=self.targets[slot];x=sign*along;z=normal if roll==0 else -normal;y=np.cross(z,x)
        return Rotation.from_matrix(np.stack([x,y,z],axis=1))

    def run(self,policy,failed_slot=None,blocked=False):
        self.remaining=list(range(12));self.now=0.;self.state=np.r_[self.initial,self.c['initial_propellant_kg'],[0,0,0,1],[0,0,0]]
        self.events=[];self.history=[];self.release_records=[];self.failures=[];self.peak_torque=0.;self.peak_rate=0.;self.source_J=0.;self.hold_J=0.
        self.main_prop=0.;self.attitude_prop=0.;self.momentum_residuals=[];self.angular_residuals=[];self.native_events=[]
        initial_mass=self.mass_props(self.remaining,self.state[6])[0]
        success=True
        for slot,(pid,sign,roll) in enumerate(policy):
            target=self.target_rotation(slot,sign,roll)
            before=self.now
            if slot:
                self.arc(self.c['post_release_guard_s'],'post_release_guard')
                self.brake()
                previous=self.release_records[-1]
                if previous['released']:
                    self.slew(Rotation.from_quat(previous['release_quaternion_xyzw']),'restore_release_axis')
                    self.main_burn(previous['host_recoil_delta_v_m_s'])
            self.slew(target,'prepare_next_release')
            prep_time=self.now-before
            deadline=float(self.times[slot])-self.c['zero_force_loading_coast_s']-self.c['pre_release_guard_s']
            if self.now>deadline+1e-7:
                self.failures.append(dict(slot=slot+1,reason='Finite recovery/slew misses400s zero-force loading coast',
                                          preparation_end_s=self.now,latest_preparation_end_s=deadline,
                                          excess_s=self.now-deadline,remaining_payloads=len(self.remaining)))
                success=False;break
            if pid not in self.remaining:raise ValueError('Duplicate release policy')
            # Any spare pre-loading time is also a true zero-force coast.
            self.arc(deadline-self.now,'pre_loading_slack')
            hold=self.hold_requirement(pid)
            if hold['peak_torque_N_m']>self.a['torque_N_m']:
                self.failures.append(dict(slot=slot+1,reason='Bounded transport attitude-hold torque exceeds authority',**hold));success=False;break
            self.arc(self.c['zero_force_loading_coast_s'],'zero_force_loading',
                     attitude_mass_use=hold['propellant_kg'])
            self.arc(self.c['pre_release_guard_s'],'pre_release_guard')
            failed=(failed_slot==slot+1)
            record=self.release(pid,sign,roll,failed)
            record['recovery_and_preparation_elapsed_s']=prep_time
            record['transport_hold']=hold
            record['coast_requirement_s']=self.c['zero_force_loading_coast_s']
            self.release_records.append(record)
            if failed and blocked:
                self.failures.append(dict(slot=slot+1,reason='Modeled unresolved shared-path capture fault: inhibit all subsequent releases',remaining_payloads=len(self.remaining)))
                success=False;break
            if self.state[6]<self.c['independent_disposal_propellant_floor_kg']:
                self.failures.append(dict(slot=slot+1,reason='Independent disposal reserve violated'));success=False;break
        if self.release_records:
            self.arc(self.c['post_release_guard_s'],'final_post_release_guard');self.brake()
            previous=self.release_records[-1]
            if previous['released']:
                self.slew(Rotation.from_quat(previous['release_quaternion_xyzw']),'final_restore_release_axis')
                self.main_burn(previous['host_recoil_delta_v_m_s'])
        rate_pass=self.peak_rate<=math.radians(self.a['rate_deg_s'])*(1+1e-7)
        torque_pass=self.peak_torque<=self.a['torque_N_m']*(1+1e-7)
        bound_pass=all(x['payload_osculating_perilune_altitude_m']>20000 for x in self.release_records if x['released'])
        released=sum(x['released'] for x in self.release_records)
        authority_pass=rate_pass and torque_pass
        record=dict(study='PCS-LUNAR-CAMPAIGN-01',authority=self.a,policy=[dict(payload=self.manifest[i]['id'],index=i,sign=s,roll_deg=r) for i,s,r in policy],
                    completed_attempts=len(self.release_records),released_payloads=released,
                    retained_payloads=len(self.remaining),retained_payload_ids=[self.manifest[i]['id'] for i in self.remaining],
                    initial_mass_kg=initial_mass,final_mass_kg=self.mass_props(self.remaining,self.state[6])[0],
                    final_propellant_kg=float(self.state[6]),main_propellant_used_kg=self.main_prop,
                    attitude_propellant_used_kg=self.attitude_prop,
                    source_draw_J=self.source_J,balance_energy_J=1.1664*self.now,
                    elapsed_s=self.now,peak_rate_deg_s=math.degrees(self.peak_rate),peak_torque_N_m=self.peak_torque,
                    rate_pass=rate_pass,torque_pass=torque_pass,useful_osculating_floor_pass=bound_pass,
                    independent_disposal_reserve_pass=bool(self.state[6]>=8),
                    mass_closure_residual_kg=initial_mass-self.mass_props(self.remaining,self.state[6])[0]-4*released-self.main_prop-self.attitude_prop,
                    max_linear_momentum_residual_kg_m_s=max(self.momentum_residuals,default=0),
                    max_angular_momentum_residual_kg_m2_s=max(self.angular_residuals,default=0),
                    nominal_full_manifest_pass=bool(success and released==12 and authority_pass and bound_pass and self.state[6]>=8),
                    failures=self.failures,releases=self.release_records,events=self.events,
                    final_host_state=self.state.tolist(),native_events=self.native_events,
                    history=self.history,
                    interpretation='Finite bounded-host point-release campaign; each result is conditional on declared thrust/torque/rate/inertia/transport allocations. No provider or physical pulse/contact acceptance follows.')
        return record

    def inertia(self,prop):return self.mass_props(self.remaining,prop)[2]

    def append_samples(self,sol,label,attitude=None):
        for t in np.linspace(sol.t[0],sol.t[-1],max(65 if attitude is not None else 2,int((sol.t[-1]-sol.t[0])/20)+1)):
            y=sol.sol(t)
            if attitude is not None:y=attitude(t,y)
            R=Rotation.from_quat(y[7:11]);w=R.apply(np.linalg.solve(self.inertia(y[6]),R.inv().apply(y[11:14])))
            self.peak_rate=max(self.peak_rate,norm(w))
            self.history.append(dict(t_s=float(t),phase=label,position_m=y[:3].tolist(),velocity_m_s=y[3:6].tolist(),propellant_kg=float(y[6]),quaternion_xyzw=y[7:11].tolist(),angular_momentum_inertial_N_m_s=y[11:14].tolist(),angular_rate_deg_s=math.degrees(norm(w))))

    def arc(self,duration,label,F=None,torque=None,attitude_mass_use=0.):
        if duration<1e-9:return
        start=self.now;before=self.state.copy();F=np.zeros(3) if F is None else np.asarray(F);torque=np.zeros(3) if torque is None else np.asarray(torque)
        mdot_main=norm(F)/(G0*self.c['main_Isp_s']);mdot_acs=norm(torque)/(self.c['attitude_couple_lever_arm_m']*G0*self.c['attitude_Isp_s'])+attitude_mass_use/duration
        def rhs(t,y):
            R=Rotation.from_quat(y[7:11]);wb=np.linalg.solve(self.inertia(y[6]),R.inv().apply(y[11:14]));wi=R.apply(wb)
            mass=self.mass_props(self.remaining,y[6])[0]
            return np.r_[y[3:6],-self.mu*y[:3]/norm(y[:3])**3+F/mass,-mdot_main-mdot_acs,qdot(y[7:11],wi),torque]
        sol=solve_ivp(rhs,[start,start+duration],before,method='DOP853',rtol=2e-11,atol=1e-9,max_step=min(self.step,max(duration/4,.02)),dense_output=True)
        assert sol.success
        self.state=sol.y[:,-1];self.state[7:11]/=norm(self.state[7:11]);self.now+=duration
        self.main_prop+=mdot_main*duration;self.attitude_prop+=mdot_acs*duration
        self.peak_torque=max(self.peak_torque,norm(torque));self.append_samples(sol,label)
        self.events.append(dict(kind='arc',phase=label,start_s=start,end_s=self.now,force_inertial_N=F.tolist(),torque_inertial_N_m=torque.tolist(),before=before.tolist(),after=self.state.tolist()))
        self.native_events.append(dict(kind='arc',phase=label,start_s=start,end_s=self.now,force_inertial_N=F.tolist(),propellant_after_kg=float(self.state[6])))

    def brake(self):
        H=self.state[11:14].copy();h=norm(H)
        if h<1e-11:self.state[11:14]=0;return
        self.arc(h/self.a['torque_N_m'],'finite_angular_momentum_brake',torque=-unit(H)*self.a['torque_N_m'])
        self.state[11:14]=0

    def slew(self,target,label):
        current=Rotation.from_quat(self.state[7:11]);rot=(target*current.inv()).as_rotvec();angle=norm(rot)
        if angle<1e-10:self.state[7:11]=target.as_quat();return
        axis=rot/angle;I=self.inertia(self.state[6])
        # Evaluate the full anisotropic Euler torque for a unit-duration quintic.
        # Torque scales as1/T². A0.1% time margin covers the dense sampling of
        # its smooth peak; actual coupled fuel-dependent torque is checked below.
        unit_torques=[]
        for s in np.linspace(0,1,257):
            Rs=Rotation.from_rotvec(axis*angle*fcurve(s))*current
            wb=Rs.inv().apply(axis*angle*dfcurve(s));ab=Rs.inv().apply(axis*angle*ddfcurve(s))
            unit_torques.append(norm(I@ab+np.cross(wb,I@wb)))
        A=max(unit_torques)
        duration=max(math.sqrt(A/self.a['torque_N_m'])*1.001,1.875*angle/math.radians(self.a['rate_deg_s']))
        start=self.now;before=self.state.copy();lever=self.c['attitude_couple_lever_arm_m'];ce=G0*self.c['attitude_Isp_s']
        def attitude(t,prop):
            s=np.clip((t-start)/duration,0,1);R=Rotation.from_rotvec(axis*angle*fcurve(s))*current
            omega=axis*angle*dfcurve(s)/duration;alpha=axis*angle*ddfcurve(s)/duration**2
            mass,center,Ib=self.mass_props(self.remaining,prop);wb=R.inv().apply(omega);ab=R.inv().apply(alpha)
            tau=Ib@ab+np.cross(wb,Ib@wb)
            for _ in range(4):
                mdot=-norm(tau)/(lever*ce);tau=Ib@ab+np.cross(wb,Ib@wb)+par(center)@wb*mdot
            return R,omega,R.apply(tau),R.apply(Ib@wb)
        def rhs(t,y):
            _,_,tau,_=attitude(t,y[6])
            return np.r_[y[3:6],-self.mu*y[:3]/norm(y[:3])**3,-norm(tau)/(lever*ce)]
        sol=solve_ivp(rhs,[start,start+duration],self.state[:7],method='DOP853',rtol=2e-11,atol=1e-10,max_step=min(self.step,duration/16),dense_output=True)
        def expanded(t,y):
            R,w,tau,H=attitude(t,y[6]);self.peak_torque=max(self.peak_torque,norm(tau));self.peak_rate=max(self.peak_rate,norm(w))
            return np.r_[y,R.as_quat(),H]
        self.attitude_prop+=before[6]-sol.y[6,-1]
        self.state=np.r_[sol.y[:,-1],target.as_quat(),np.zeros(3)];self.now+=duration
        self.append_samples(sol,label,expanded)
        self.events.append(dict(kind='finite_slew',phase=label,start_s=start,end_s=self.now,angle_deg=math.degrees(angle),before=before.tolist(),after=self.state.tolist(),torque_limit_N_m=self.a['torque_N_m'],rate_limit_deg_s=self.a['rate_deg_s']))
        self.native_events.append(dict(kind='arc',phase=label,start_s=start,end_s=self.now,force_inertial_N=[0,0,0],propellant_after_kg=float(self.state[6])))

    def hold_requirement(self,pid):
        r=self.manifest[pid]['r'];home=self.release_r-np.array([1.3,0,0]);mid=r.copy();mid[1]=home[1]
        peak=0.;impulse=0.;hmax=0.
        for a,b,duration in [(r,mid,40),(mid,home,120)]:
            samples=np.linspace(0,1,257);torques=[]
            for s in samples:
                pos=a+(b-a)*fcurve(s);vel=(b-a)*dfcurve(s)/duration;acc=(b-a)*ddfcurve(s)/duration**2
                torque=7.5730430711591*np.cross(pos,acc);internalH=7.5730430711591*np.cross(pos,vel)
                torques.append(norm(torque));hmax=max(hmax,norm(internalH))
            peak=max(peak,max(torques));impulse+=float(np.trapezoid(torques,samples))*duration
        self.peak_torque=max(self.peak_torque,peak)
        prop=impulse/(self.c['attitude_couple_lever_arm_m']*G0*self.c['attitude_Isp_s'])
        return dict(peak_torque_N_m=peak,absolute_torque_impulse_N_m_s=impulse,propellant_kg=prop,internal_transport_angular_momentum_bound_N_m_s=hmax,
                    scope='7.573kg payload/cradle kinematic upper envelope; rest-to-rest zero net angular impulse,finite ACS couple counters internal angular momentum; no native contact validation.')

    def main_burn(self,recoil):
        dv=norm(recoil)
        if dv<1e-12:return
        axis=Rotation.from_quat(self.state[7:11]).apply([1,0,0]);direction=unit(-np.asarray(recoil))
        assert norm(axis-direction)<1e-7
        M=self.mass_props(self.remaining,self.state[6])[0];ce=G0*self.c['main_Isp_s'];prop=M*(-math.expm1(-dv/ce));duration=prop*ce/self.c['main_thrust_N']
        self.arc(duration,'finite_body_axis_recoil_recovery',F=axis*self.c['main_thrust_N'])

    def release(self,pid,sign,roll,failed):
        before=self.state.copy();R=Rotation.from_quat(before[7:11]);m0,center_before,I0=self.mass_props(self.remaining,before[6])
        command=self.manifest[pid]['command'];cal=self.cal[command]
        measured=cal['release']['relative_speed_m_s'];u=measured*(m0-4-self.moving)/(m0-4)
        record=dict(slot=len(self.release_records)+1,t_s=self.now,payload=self.manifest[pid]['id'],sign=sign,roll_deg=roll,command_m_s=command,calibrated_relative_speed_m_s=u,
                    released=not failed,release_quaternion_xyzw=before[7:11].tolist(),before_mass_kg=m0,source_draw_J=self.source_energy[command],before_host_state=before.tolist())
        self.source_J+=self.source_energy[command]
        if failed:
            record.update(host_recoil_delta_v_m_s=[0,0,0],after_mass_kg=m0,after_host_state=self.state.tolist(),failure='Pre-command cell isolation/retention surrogate; no successful ejection,not a demonstrated physical fault-clearing capability.')
            return record
        remaining=[i for i in self.remaining if i!=pid];mp,center_parent,Ip=self.mass_props(remaining,before[6])
        relbody=self.release_r-center_parent;relinertial=R.apply(relbody);U=R.apply([u,0,0]);reduced=4*mp/m0
        rp=before[:3]-4/m0*relinertial;rc=before[:3]+mp/m0*relinertial
        vp=before[3:6]-4/m0*U;vc=before[3:6]+mp/m0*U
        # Release starts with zero rigid-body rate after controlled loading.
        assert norm(before[11:14])<1e-7
        Hparent=-reduced*np.cross(relinertial,U)
        momentum=mp*vp+4*vc-m0*before[3:6]
        Hsplit=Hparent+np.cross(rp-before[:3],mp*(vp-before[3:6]))+np.cross(rc-before[:3],4*(vc-before[3:6]))
        self.momentum_residuals.append(norm(momentum));self.angular_residuals.append(norm(Hsplit))
        self.remaining=remaining;self.state[:3]=rp;self.state[3:6]=vp;self.state[11:14]=Hparent
        rnorm=norm(rc);h=np.cross(rc,vc);energy=np.dot(vc,vc)/2-self.mu/rnorm;a=-self.mu/(2*energy);ecc=norm(np.cross(vc,h)/self.mu-rc/rnorm);peri=a*(1-ecc)-self.radius
        qchief=self.chief.sol(self.now);position_chief_error=norm(rc-qchief[:3]);velocity_kick=vc-qchief[3:6]
        record.update(after_mass_kg=mp,host_recoil_delta_v_m_s=(-4/m0*U).tolist(),payload_state=np.r_[rc,vc].tolist(),
                      payload_osculating_perilune_altitude_m=float(peri),payload_state_vs_coasting_chief_position_m=position_chief_error,
                      payload_state_vs_coasting_chief_velocity_m_s=velocity_kick.tolist(),after_host_state=self.state.tolist(),
                      after_inertia_about_CG_kg_m2=Ip.tolist(),after_CG_in_body_reference_m=center_parent.tolist(),
                      angular_momentum_after_N_m_s=Hparent.tolist(),after_rate_deg_s=math.degrees(norm(np.linalg.solve(Ip,R.inv().apply(Hparent)))),
                      linear_momentum_residual_kg_m_s=norm(momentum),angular_momentum_residual_kg_m2_s=norm(Hsplit))
        self.native_events.append(dict(kind='release',t_s=self.now,payload=self.manifest[pid]['id'],payload_state=np.r_[rc,vc].tolist(),
                                      parent_position_jump_m=(rp-before[:3]).tolist(),parent_velocity_jump_m_s=(vp-before[3:6]).tolist(),
                                      remaining_payloads=len(self.remaining),propellant_kg=float(self.state[6])))
        return record


def beam_search(model):
    """Finite 12-level beam search over cell order,sign and roll choices."""
    width=model.c['search']['beam_width'];initialR=Rotation.identity();Imax=np.linalg.eigvalsh(model.Icore).max();rate=math.radians(model.a['rate_deg_s']);torque=model.a['torque_N_m']
    beam=[(0.,(),tuple(range(12)),0,initialR)]
    evaluated=0
    for slot in range(12):
        candidates=[]
        for cost,policy,left,nplus,current in beam:
            for pid in left:
                for sign in [-1,1]:
                    if nplus+(sign==1)>6 or slot-nplus+(sign==-1)>6:continue
                    for roll in [0,180]:
                        target=model.target_rotation(slot,sign,roll);theta=norm((target*current.inv()).as_rotvec())
                        bound=max(math.sqrt(Imax*(5.773503*theta+1.875**2*theta**2)/torque),1.875*theta/rate)
                        # Slot geometry penalizes large off-axis impulse/recovery.
                        center=sum((model.manifest[i]['r']*4 for i in left),start=np.zeros(3))/(300+4*len(left))
                        lever=norm(np.cross(model.release_r-center,[1,0,0]));u=model.manifest[pid]['command']
                        impulse=4*u*lever
                        nextcost=cost+bound+impulse/torque
                        candidates.append((nextcost,policy+((pid,sign,roll),),tuple(i for i in left if i!=pid),nplus+(sign==1),target));evaluated+=1
        candidates.sort(key=lambda x:(x[0],x[1]));beam=candidates[:width]
    return list(beam[0][1]),dict(method='12-level beam search,finite order/sign/roll candidates',width=width,evaluated_candidates=evaluated,best_proxy_seconds=beam[0][0],global_optimum_claim=False)


def compact(record):return {k:v for k,v in record.items() if k not in ['history','events','native_events']}


def main():
    config=json.loads((HERE/'campaign_inputs.json').read_text());out=HERE/'campaign';out.mkdir(exist_ok=True)
    authorities=config['authority_cases'];base=Campaign(config,authorities[3]);best,search=beam_search(base)
    alternating=[(i,1 if k%2==0 else -1,0) for k,i in enumerate(range(12))]
    grouped=[(i,1 if k<6 else -1,0) for k,i in enumerate(range(12))]
    policies={'searched':best,'alternating_baseline':alternating,'grouped_baseline':grouped}
    results=[];full=[]
    for authority in authorities:
        for name,policy in policies.items():
            record=Campaign(config,authority).run(policy);record['policy_name']=name;results.append(compact(record))
            (out/(authority['id']+'_'+name+'.json')).write_text(json.dumps(record,indent=2)+'\n')
            if authority['id']=='T5_R20' and name=='searched':full.append(record)
    selected=full[0]
    for label,blocked in [('pre_command_isolated_cell_failure',False),('unresolved_shared_path_failure',True)]:
        record=Campaign(config,authorities[3]).run(best,failed_slot=6,blocked=blocked);record['policy_name']=label
        results.append(compact(record));(out/(label+'.json')).write_text(json.dumps(record,indent=2)+'\n')
    fine=Campaign(config,authorities[3],step=15).run(best)
    verify=dict(source_sha256=sha(__file__),inputs_sha256=sha(HERE/'campaign_inputs.json'),
                max_momentum_residual_kg_m_s=max(x['max_linear_momentum_residual_kg_m_s'] for x in results),
                max_angular_residual_kg_m2_s=max(x['max_angular_momentum_residual_kg_m2_s'] for x in results),
                max_mass_closure_residual_kg=max(abs(x['mass_closure_residual_kg']) for x in results),
                half_max_step_final_position_difference_m=norm(np.array(selected['final_host_state'][:3])-np.array(fine['final_host_state'][:3])),
                half_max_step_final_velocity_difference_m_s=norm(np.array(selected['final_host_state'][3:6])-np.array(fine['final_host_state'][3:6])),
                half_max_step_propellant_difference_kg=abs(selected['final_propellant_kg']-fine['final_propellant_kg']))
    summary=dict(study='PCS-LUNAR-CAMPAIGN-01',configuration=config,search=search,verification=verify,
                 source_input_sha256={p.name:sha(p) for p in [HERE/'study_inputs.json',HERE/'inputs/COUPLED_SHOT.json',HERE/'inputs/SIGNATURES_home.json',HERE/'inputs/SIGNATURES_release.json',HERE/'inputs/RESOURCE_LEDGER.json']},
                 selected_native_replay_case='T5_R20_searched',cases=results)
    (HERE/'CAMPAIGN_RESULTS.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(dict(verification=verify,selected_released=selected['released_payloads'],selected_pass=selected['nominal_full_manifest_pass'],selected_failures=selected['failures'],cases=[dict(authority=x['authority']['id'],policy=x['policy_name'],released=x['released_payloads'],passed=x['nominal_full_manifest_pass'],propellant=x['final_propellant_kg']) for x in results]),indent=2))


if __name__=='__main__':main()
