"""Average dq/source model with finite force, host reaction and active arrest.

Peak phase-current convention matches finite_motor. PWM ripple is bounded in
loss/current checks rather than resolved as individual switching events. Source
and switch data are catalog references; board parasitics are design allocations.
"""
from pathlib import Path
import hashlib,json,math
import numpy as np

ROOT=Path(__file__).resolve().parents[1]

def inputs():
    paths={'home':ROOT/'cad/release/VOLLEY_G5_ACR1_home.json',
        'force':ROOT/'analysis/FINITE_MOTOR.json','brake':ROOT/'analysis/ARREST_FORCE_MAP.json',
        'resistance':ROOT/'analysis/conduction/phase_A/h2/RESULT.json'}
    raw={k:p.read_bytes()for k,p in paths.items()};d={k:json.loads(v)for k,v in raw.items()}
    moving=sum(q['mass_kg']for q in d['home']['BOM']if q['subsystem'].startswith('sled'))
    dry=sum(q['mass_kg']for q in d['home']['BOM']if q['subsystem']!='payload')
    rows=d['force']['stations'];b=d['brake']['stations']
    xs=np.r_[[r['displacement_m']for r in rows],[r['displacement_m']for r in b[1:]]]
    kt=np.r_[[r['with_return_N_per_A']for r in rows],[r['N_per_peak_A']for r in b[1:]]]
    return moving,dry,xs,kt,d['resistance']['resistance_ohm_at20C'],{k:hashlib.sha256(v).hexdigest()for k,v in raw.items()}

def simulate(target,sled,dry,xs,ks,R20,adverse=False,L=10e-6,dt=20e-6,trace=False):
    payload=4.;Mhost=500+dry-sled+44+7 #500kg reference bus;11stored payloads;7kg power/control allowance
    mu=(sled+payload)*Mhost/(Mhost+sled+payload)
    mu_brake=sled*Mhost/(Mhost+sled)
    C=6.25*(.9*.7 if adverse else 1);Rsrc=.176*(2 if adverse else 1)
    R=R20*(1+.00393*(80 if adverse else 30))+.002 #explicit2mohm phase lead/joint allowance
    kfactor=.90 if adverse else 1.;friction=10 if adverse else 5
    vc=86.4;current=x=v=t=0.;phase='ACCEL';release=None
    attached=True;command_transition=None;peak_payload_contact=0.;friction_work=0.
    ledger={k:0. for k in ['mechanical_J','copper_J','inverter_J','bank_J','auxiliary_J']}
    peak_i=peak_device=peak_bank=peak_vds=0.;records=[];status='TIME_LIMIT';last_bank=0.
    peak_cell_voltage=vc/32
    maximum_actual_modulation=0.
    integral_peak_current_sq=0.;integral_with_ripple_sq=0.
    # Field-integrated brake work / A remaining at each location.
    brake_x=np.array([z for z in xs if z>=1.3]);brake_k=np.array([ks[i]for i,z in enumerate(xs)if z>=1.3])
    rem=np.r_[np.cumsum(((brake_k[:-1]+brake_k[1:])/2*np.diff(brake_x))[::-1])[::-1],0]
    stop_target=1.507 #3mm control reserve within the fixed210mm mechanical allocation
    reserve_work=float(np.interp(stop_target,brake_x,rem))
    n=0
    time_limit=2*(1.3+.21)/max(target,.1)+1.
    while t<time_limit:
        k=float(np.interp(x,xs,ks));actual_k=k*kfactor
        if phase=='ACCEL':
            desired_acc=(target*target-v*v)/(2*max(1.3-x,.001))
            desired_acc=max(0,min(desired_acc,3*target*target/(2*1.3)))
            ref=(mu*desired_acc+friction)/k
        else:
            work=float(np.interp(x,brake_x,rem))-reserve_work
            ref=-(.5*mu_brake*v*v)/max(work,.0001)
        ref=max(-600,min(600,ref))
        omega=2*math.pi*v/.048;ke=actual_k/1.5
        terminal_previous=max(40,vc-last_bank*Rsrc)
        vmax=terminal_previous/math.sqrt(3)*.95
        qroom=math.sqrt(max(0,vmax*vmax-(omega*L*current)**2))
        qrequest=R*current+ke*v+L*(ref-current)/.00025
        vq=max(-qroom,min(qroom,qrequest))
        ripple=terminal_previous/(4*L*40000)
        # Hot Rds factor2,10parallel devices per position;60MOSFETs total.
        ron=.0097*2/10
        def source_power(q):
            mid=current+(q-R*current-ke*v)/L*dt/2
            inv=1.5*ron*mid*mid+ron*ripple*ripple/4+2*terminal_previous*(abs(mid)+ripple/2)*.0000002*40000+6
            return 1.5*q*mid+R*ripple*ripple/4+inv+50
        budget=.8*vc*vc/(4*Rsrc)
        # Limit regeneration by actual bank-terminal voltage, not endpoint charge.
        # Reducing |vq| slows current-energy recovery instead of assuming a dump load.
        terminal_charge_limit=32*2.9
        minimum_dc_power=terminal_charge_limit*(vc-terminal_charge_limit)/Rsrc
        requested_power=source_power(vq)
        if requested_power>budget or requested_power<minimum_dc_power:
            lo,hi=0.,1.
            for _ in range(14):
                mid=(lo+hi)/2
                if minimum_dc_power<=source_power(vq*mid)<=budget:lo=mid
                else:hi=mid
            vq*=lo
        di=(vq-R*current-ke*v)/L
        imid=current+di*dt/2
        motive=actual_k*imid
        force=(motive-friction if v>1e-8 else motive+friction if v< -1e-8
               else math.copysign(max(0,abs(motive)-friction),motive))
        effective=mu if attached else mu_brake
        if attached:peak_payload_contact=max(peak_payload_contact,payload*max(force,0)/(sled+payload))
        vn=v+force/effective*dt;xn=x+(v+vn)/2*dt
        p_cu=1.5*R*imid*imid+R*ripple*ripple/4
        integral_peak_current_sq+=imid*imid*dt
        integral_with_ripple_sq+=(abs(imid)+ripple/2)**2*dt
        p_inv=1.5*ron*imid*imid+ron*ripple*ripple/4+2*terminal_previous*(abs(imid)+ripple/2)*.0000002*40000+6
        p_aux=50.;p_dc=1.5*vq*imid+R*ripple*ripple/4+p_inv+p_aux
        disc=vc*vc-4*Rsrc*p_dc
        if disc<=0:status='SOURCE_POWER_LIMIT';break
        ibank=2*p_dc/(vc+math.sqrt(disc));terminal=vc-ibank*Rsrc
        maximum_actual_modulation=max(maximum_actual_modulation,
            math.hypot(vq,omega*L*current)/(terminal/math.sqrt(3)))
        last_bank=ibank
        ledger['mechanical_J']+=actual_k*imid*(xn-x)
        friction_work+=max(0,(motive-force)*(xn-x))
        ledger['copper_J']+=p_cu*dt;ledger['inverter_J']+=p_inv*dt
        ledger['bank_J']+=ibank*ibank*Rsrc*dt;ledger['auxiliary_J']+=p_aux*dt
        vc-=ibank/C*dt
        peak_cell_voltage=max(peak_cell_voltage,vc/32,terminal/32)
        current+=di*dt;x,v,t=xn,vn,t+dt
        peak_i=max(peak_i,abs(current));peak_bank=max(peak_bank,abs(ibank))
        device=(abs(current)+ripple/2)/10*1.25;peak_device=max(peak_device,device)
        # Explicit30nH commutation-loop and200ns fall-time allocation, not measured.
        peak_vds=max(peak_vds,terminal+(abs(current)+ripple/2)*30e-9/.2e-6)
        if trace and n%100==0:records.append([t,x,v,current,vc,terminal,ibank,phase])
        n+=1
        if phase=='ACCEL' and x>=1.3:
            command_transition=dict(time_s=t,position_m=x,relative_speed_m_s=v)
            phase='BRAKE'
        # The push-only rear contact releases when its normal reaction reaches0,
        # not instantaneously when the electrical braking command is issued.
        if phase=='BRAKE' and attached and force<=0:
            release=dict(time_s=t,relative_speed_m_s=v,
                position_m=x,
                payload_inertial_delta_v_m_s=Mhost/(Mhost+sled+payload)*v,
                host_recoil_before_arrest_m_s=-(sled+payload)/(Mhost+sled+payload)*v)
            attached=False
        if phase=='BRAKE' and not attached and v<=.005:status='STOPPED';break
        if x>1.511:status='ARREST_STROKE_EXCEEDED';break
        if vc<60:status='LOW_SOURCE_VOLTAGE';break
    drawn=.5*C*(86.4**2-vc**2);field_energy=.75*L*current*current
    residual=drawn-sum(ledger.values())-field_energy
    checks=dict(released=release is not None,stopped_inside_210mm=status=='STOPPED' and x<=1.51,
        release_speed=release is not None and abs(release['relative_speed_m_s']-target)<=.005,
        cam_open_before_release=release is not None and release['position_m']>=1.295,
        phase_current_limit=peak_i<=600.1,hot_device_current_with25pct_imbalance=peak_device<=92,
        allocated_switch_voltage=peak_vds<200,cell_charge_voltage=peak_cell_voltage<3,
        physical_modulation_limit=maximum_actual_modulation<=1,
        energy_balance=abs(residual)<max(.5,.01*abs(drawn)))
    return dict(target_m_s=target,adverse=adverse,inductance_H=L,dt_s=dt,status=status,
        moving_sled_kg=sled,reference_rest_host_kg=Mhost,release=release,stop_position_m=x,
        electrical_brake_command=command_transition,peak_payload_normal_reaction_N=peak_payload_contact,
        mechanical_friction_dissipation_J=friction_work,
        stop_velocity_m_s=v,time_s=t,cap_draw_J=drawn,cap_end_V=vc,field_energy_end_J=field_energy,
        diagnostic_time_limit_s=time_limit,
        energy_ledger=ledger,energy_residual_J=residual,peak_phase_current_A=peak_i,
        maximum_cell_terminal_or_internal_V=peak_cell_voltage,
        actual_modulation_peak=maximum_actual_modulation,nominal_modulation_command_fraction=.95,
        integral_phase_peak_current_sq_A2s=integral_peak_current_sq,
        conservative_phase_current_sq_with_ripple_A2s=integral_with_ripple_sq,
        peak_device_current_A=peak_device,peak_bank_current_A=peak_bank,allocated_peak_Vds_V=peak_vds,
        checks=checks,all_declared_checks_pass=all(checks.values()),trace=records)

def main():
    sled,dry,xs,ks,R,hashes=inputs();cases=[]
    for target in [1,2,3,4,4.5,6]:
        for adverse in [False,True]:
            for L in [3e-6,20e-6,100e-6]:
                row=simulate(target,sled,dry,xs,ks,R,adverse,L,trace=target==3 and not adverse and L==20e-6)
                cases.append(row);print(target,adverse,L,row['status'],row['all_declared_checks_pass'],flush=True)
    result=dict(configuration_id='VOLLEY-G5-ACR1',source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        inputs_sha256=hashes,sled_mass_from_home_capture_kg=sled,dry_CAD_mass_kg=dry,cases=cases,
        component_basis={'bank':'64 EatonTV1860-3R0107-R,32S2P,2.7V/group reference',
            'inverter':'Three half bridges,10IRFP4668PbF per switch position;UCC21520 isolated drivers',
            'source':'Catalog references, not space-qualified hardware acceptance'},
        boundaries=['Average dq model, not resolved transistor switching',
            'Active LSM arrest receives all braking credit; unexcited steel poles receive none',
            'STOPPED denotes the first low-speed turnaround before powered empty return; residual magnetic energy is retained in the ledger',
            'Regeneration terminal-voltage limit2.9V/cell is applied during the current ramp; absolute cell gate remains3V',
            '30nH loop,200ns transitions,2mohm phase lead/joint resistance and cooling are design allocations',
            'Magnetic-current reaction, detailed harness, nut life and physical fault qualification remain hardware development work',
            'Current home CAD is an engineering capture; mass values must refresh after mechanical acceptance'])
    (ROOT/'analysis/COUPLED_SHOT.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
