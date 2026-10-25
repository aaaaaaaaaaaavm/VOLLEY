"""Native MuJoCo bounded ACR1 release/arrest contact replay.

Six-DOF uniform-box payload; finite host/carrier translation; rotations and
transverse guide motion of host/carrier idealized. Electrical force is replayed,
not recomputed from the perturbed contact trajectory. Contact coefficients are
declared sensitivities, not measured material properties.
"""
from pathlib import Path
import argparse, csv, hashlib, json, math, time
import numpy as np
import mujoco as mj

HERE=Path(__file__).resolve().parent
ACR1=HERE.parent/'acr1'
MP=4.0
DIMS=np.array([.3405,.1,.1])
INERTIA=MP/12*np.array([.1**2+.1**2,.3405**2+.1**2,.3405**2+.1**2])

def quat(roll,pitch,yaw):
    r,p,y=np.radians([roll,pitch,yaw])/2
    return np.array([math.cos(r)*math.cos(p)*math.cos(y)+math.sin(r)*math.sin(p)*math.sin(y),
                     math.sin(r)*math.cos(p)*math.cos(y)-math.cos(r)*math.sin(p)*math.sin(y),
                     math.cos(r)*math.sin(p)*math.cos(y)+math.sin(r)*math.cos(p)*math.sin(y),
                     math.cos(r)*math.cos(p)*math.sin(y)-math.sin(r)*math.sin(p)*math.cos(y)])

def surfaces(keeper_shift=12,rear_mask='all'):
    # Exact rectangular contact members from build_acr1.sled, cradle_acr1.pallet
    # and sled_latches.build, in carrier-local mm coordinates. Circular drive,
    # screw and follower members outside this payload corridor are omitted.
    out=[]
    def box(name,lo,size,source):
        out.append(dict(name=name,lo_mm=list(lo),size_mm=list(size),source=source))
    xa=64.;zf=46.;xf=xa+340.5
    box('base_top',[0,-100,14],[488,170,16],'build_acr1.sled top plate;remote bores outside payload corridor')
    box('base_bottom',[0,-100,-30],[488,170,16],'build_acr1.sled bottom plate;remote bores outside payload corridor')
    box('base_web',[0,-100,-30],[488,20,60],'build_acr1.sled negative web;remote bores outside payload corridor')
    for u,v in [(0,64),(124,220),(288,340.5)]:
        for y in [-50,42]:box(f'seat_{u}_{y}',[xa+u,y,30],[v-u,8,16],'build_acr1.sled raised seats')
    for u in [90,230]:
        box(f'pallet_slat_{u}',[xa+u,-50,38],[24,100,6],'cradle_acr1.pallet slat')
        for y in [-50,42]:box(f'pallet_{u}_{y}',[xa+u,y,44],[24,8,2],'cradle_acr1.pallet top rail pads')
    box('pallet_crossbar',[-32,-10,38],[546.5,20,6],'cradle_acr1.pallet axial crossbar')
    for u in [70,270]:
        box(f'pallet_cross_{u}',[xa+u-3,-55.5,38],[14,111,6],'cradle_acr1.pallet cross strip')
        for y in [-50,42]:box(f'pallet_foot_{u}_{y}',[xa+u-3,y,30],[14,8,8],'cradle_acr1.pallet foot')
    for x in [-22,504.5]:box(f'pallet_grip_{x}',[x-10,-10,34],[20,20,11.5],'cradle_acr1.pallet grip end;upper face0.5mm below payload;hole stays below upper face')
    for x in [40,468]:box(f'pallet_keystrip_{x}',[x-8,-99.5,38],[16,99.5,6],'cradle_acr1.pallet lock strip;key bore outside payload corridor')
    for y in [-50,42]:
        for z in [48,138]:
            if rear_mask=='single' and (y!=42 or z!=138):continue
            box(f'rear_pad_{y}_{z}',[62,y,z],[2,8,6],'build_acr1.sled designated rear rail-contact pads')
            box(f'rear_support_{y}_{z}',[50,y-6 if y<0 else y,z],[12,14,6],'build_acr1.sled rear pad support')
    for u in [24,296.5]:
        for side in [-1,1]:
            box(f'pillar_{u}_{side}',[xa+u,60 if side>0 else -66,30],[20,6,118],'build_acr1.sled outboard cap pillar')
            box(f'cap_{u}_{side}',[xa+u,42 if side>0 else -66,148],[20,24,6],'sled_latches.build closed capture cap;2mm upper gap')
            box(f'capneck_{u}_{side}',[xa+u+6,62 if side>0 else -68,152],[8,6,12],'sled_latches.build cap neck;bores outside nearest surface')
            box(f'guide_{u}_{side}',[xa+u,58 if side>0 else -154,142],[20,96,6],'sled_latches.build fixed cap rail')
            for tag,size,x,y,z in [('lower_lip',[25,8,2],xa+u-5,61,146),('web',[4,8,26],xa+u-5,61,142),('upper_lip',[25,8,2],xa+u-5,61,166)]:
                box(f'guide_{tag}_{u}_{side}',[x,y if side>0 else -y-size[1],z],size,'sled_latches.build fixed cap guide rectangular members')
    for side in [-1,1]:
        shift=keeper_shift if side>0 else 12
        box(f'forekeeper_{side}',[xf+2,42+shift if side>0 else -50-shift,50],[6,8,8],'sled_latches.build keeper rectangular contact tab')
        box(f'forepost_{side}',[xf+2,60 if side>0 else -66,30],[10,6,16],'build_acr1.sled fore support;below payload excepttop')
    return out

def build(case,dt,iterations,solver,k,damping,representation='box'):
    src=json.loads((HERE/'SOURCE_REPLAY.json').read_text())
    original=next(x for x in src['cases'] if x['case']==case.get('source','nominal'))
    ms=original['moving_sled_kg'];mh=original['reference_rest_host_kg']
    geom=surfaces(case.get('keeper_shift_mm',12),case.get('rear_mask','all'))
    mu=case.get('mu',0)
    pieces=[]
    for g in geom:
        lo=np.array(g['lo_mm'])/1000;size=np.array(g['size_mm'])/1000
        pos=lo+size/2
        if representation=='split' and g['name'].startswith(('rear_pad','seat','pallet')):
            # Same exact union; partition changes contact manifold only.
            axis=1 if g['name'].startswith('rear_pad') else 0
            for sgn in [-1,1]:
                halfsize=size.copy();halfsize[axis]/=2
                mid=pos.copy();mid[axis]+=sgn*size[axis]/4
                pieces.append(f'<geom name="{g["name"]}_{sgn}" pos="{" ".join(map(str,mid))}" size="{" ".join(map(str,halfsize/2))}"/>')
        else:pieces.append(f'<geom name="{g["name"]}" pos="{" ".join(map(str,pos))}" size="{" ".join(map(str,size/2))}"/>')
    xml=f'''<mujoco model="ACR1_bounded_release">
      <compiler angle="radian" inertiafromgeom="false"/>
      <option timestep="{dt}" gravity="0 0 0" integrator="implicitfast" solver="{solver}" cone="elliptic" iterations="{iterations}" tolerance="1e-12">
        <flag energy="enable"/>
      </option>
      <default><joint damping="0" armature="0" frictionloss="0"/><geom type="box" density="0" friction="{mu} 0 0" condim="3" solref="{-k} {-damping}" solimp="0.95 0.95 0.001 0.5 2" margin="0" gap="0"/></default>
      <worldbody>
        <body name="host"><joint name="host_x" type="slide" axis="1 0 0"/><inertial pos="0 0 0" mass="{mh}" diaginertia="1 1 1"/>
          <body name="carrier" pos="0.2 0 0"><joint name="relative_x" type="slide" axis="1 0 0"/><inertial pos="0 0 0" mass="{ms}" diaginertia="1 1 1"/>
            {''.join(pieces)}
          </body>
        </body>
        <body name="payload"><freejoint name="payload_free"/><inertial pos="0 0 0" mass="4" diaginertia="{' '.join(map(str,INERTIA))}"/><geom name="payload_box" size="0.17025 0.05 0.05" rgba="0.18 0.4 0.6 1"/></body>
      </worldbody></mujoco>'''
    model=mj.MjModel.from_xml_string(xml);data=mj.MjData(model)
    if case.get('disable_contact',False):model.opt.disableflags |= mj.mjtDisableBit.mjDSBL_CONTACT
    return model,data,original,geom,xml

def run(case,dt=50e-6,iterations=100,solver='Newton',k=1e6,damping=2000,representation='box',save=True):
    started=time.monotonic()
    model,data,original,geom,xml=build(case,dt,iterations,solver,k,damping,representation)
    source=np.load(HERE/f'source_{case.get("source","nominal")}.npz')['trace']
    tstart=round((original['release']['time_s']-.001)/5e-6)*5e-6
    x0=float(np.interp(tstart,source[:,0],source[:,1]));v0=float(np.interp(tstart,source[:,0],source[:,2]))
    ms=original['moving_sled_kg'];mh=original['reference_rest_host_kg'];mt=mh+ms+MP
    data.qpos[0]=-(ms+MP)/mt*x0;data.qpos[1]=x0
    data.qvel[0]=-(ms+MP)/mt*v0;data.qvel[1]=v0
    carrier_x=.2+data.qpos[0]+x0
    q=quat(case.get('roll_deg',0),case.get('pitch_deg',0),case.get('yaw_deg',0))
    rot=np.empty(9);mj.mju_quat2Mat(rot,q);rot=rot.reshape(3,3)
    ext=np.abs(rot)@(DIMS/2)
    # Ensure perturbed boxes start outside rear pad/floor, not with accidental
    # numerical overlap. These are declared initial-state gaps, not tolerances.
    dx=max(0,ext[0]-DIMS[0]/2)+case.get('initial_aft_gap_m',0)
    dz=max(0,ext[2]-DIMS[2]/2)+case.get('initial_z_gap_m',0)
    data.qpos[2:5]=[carrier_x+.064+.17025+dx,case.get('y_offset_m',0),.096+dz]
    data.qpos[5:9]=q
    data.qvel[2:5]=[mh/mt*v0,case.get('vy_m_s',0),case.get('vz_m_s',0)]
    data.qvel[5:8]=np.radians(case.get('initial_omega_deg_s',[0,0,0]))
    data.time=tstart
    mj.mj_forward(model,data)
    bid=mj.mj_name2id(model,mj.mjtObj.mjOBJ_BODY,'payload')
    pg=mj.mj_name2id(model,mj.mjtObj.mjOBJ_GEOM,'payload_box')
    bodyvel=np.zeros(6)
    def state():
        mj.mj_objectVelocity(model,data,mj.mjtObj.mjOBJ_BODY,bid,bodyvel,0)
        R=data.xmat[bid].reshape(3,3)
        linear=bodyvel[3:].copy();omega=bodyvel[:3].copy()
        H=R@np.diag(INERTIA)@R.T@omega
        T=.5*mh*data.qvel[0]**2+.5*ms*(data.qvel[0]+data.qvel[1])**2+.5*MP*np.dot(linear,linear)+.5*np.dot(omega,H)
        return linear,omega,H,T
    initial_position=data.qpos[2:5].copy()
    vel0,w0,H0,T0=state();P0=mh*data.qvel[0]+ms*(data.qvel[0]+data.qvel[1])+MP*vel0[0]
    initial_overlap=min([c.dist for c in data.contact[:data.ncon]]+[0])
    if initial_overlap < -1e-7:raise ValueError(f'Initial overlap {initial_overlap} in {case}')
    impulse=np.zeros(3);angimpulse=np.zeros(3);motorwork=0.;rows=[];maxsolver=0;maxpenetration=0.;peakforce=0.;native_force_error=0.
    solver_budget_steps=0;max_termination_gradient=0.
    contacts_by_group={};post_source_impulse={};rear_times=[];engaged=False;unloads=[];recontact_after_unload=[];last_rear=False
    nstep=round(.35/dt);duration=nstep*dt
    cf=np.zeros(6);warn0=[int(x.number) for x in data.warning]
    for n in range(nstep):
        t=data.time
        # Recorded force is the force applied over the interval ending at its
        # timestamp; interpolate on interval centres and sample engine midpoint.
        force=float(np.interp(t+dt/2,source[:,0]-2.5e-6,source[:,8],left=source[0,8],right=0))
        data.qfrc_applied[:]=0;data.qfrc_applied[1]=force
        pre_vrel=data.qvel[1]
        mj.mj_step1(model,data)
        pre_vel,pre_w,_,_=state()
        mj.mj_step2(model,data)
        total_f=np.zeros(3);total_t=np.zeros(3);rear=False;active_groups=set()
        for i in range(data.ncon):
            c=data.contact[i]
            if pg not in [c.geom1,c.geom2]:continue
            mj.mj_contactForce(model,data,i,cf)
            f=c.frame.reshape(3,3).T@cf[:3]
            if c.geom1==pg:f=-f
            other=c.geom2 if c.geom1==pg else c.geom1
            name=mj.mj_id2name(model,mj.mjtObj.mjOBJ_GEOM,other)
            group=('rear' if name.startswith('rear') else 'floor' if name.startswith(('seat','pallet')) else 'keeper' if name.startswith('forekeeper') else 'cap' if name.startswith('cap') else 'other')
            magnitude=float(np.linalg.norm(f))
            total_f+=f;total_t+=np.cross(c.pos-data.xpos[bid],f)
            maxpenetration=max(maxpenetration,max(0,-c.dist));peakforce=max(peakforce,magnitude)
            if magnitude>1e-6:
                active_groups.add(group);contacts_by_group[group]=contacts_by_group.get(group,0)+magnitude*dt
                if t>=original['release']['time_s']:post_source_impulse[group]=post_source_impulse.get(group,0)+magnitude*dt
                if group=='rear':rear=True;rear_times.append(t)
        impulse+=total_f*dt;angimpulse+=total_t*dt
        native_force_error=max(native_force_error,float(np.linalg.norm(total_f-data.qfrc_constraint[2:5])))
        if rear:engaged=True
        if engaged and last_rear and not rear:unloads.append(t)
        if unloads and rear and not last_rear:recontact_after_unload.append(t)
        last_rear=rear
        motorwork+=force*.5*(pre_vrel+data.qvel[1])*dt
        maxsolver=max(maxsolver,int(np.max(data.solver_niter)))
        if int(np.max(data.solver_niter))>=iterations:solver_budget_steps+=1
        gradients=np.asarray(data.solver.gradient)
        stride=len(gradients)//len(data.solver_niter)
        for island,count in enumerate(data.solver_niter):
            if count>0:max_termination_gradient=max(max_termination_gradient,float(gradients[island*stride+min(int(count)-1,stride-1)]))
        if n%max(1,round(.0005/dt))==0:
            mj.mj_forward(model,data)
            vel,w,H,T=state()
            rows.append([data.time,*data.qpos[2:5],*data.qpos[5:9],*vel,*np.degrees(w),data.qpos[1],data.qvel[1],len(active_groups),force,maxpenetration])
    mj.mj_forward(model,data)
    vel,w,H,T=state();P=mh*data.qvel[0]+ms*(data.qvel[0]+data.qvel[1])+MP*vel[0]
    qfinal=data.qpos[5:9].copy();angle=2*math.acos(min(1,abs(float(np.dot(q,qfinal)))))
    payload_aft_from_carrier=data.qpos[2]-(.2+data.qpos[0]+data.qpos[1])-(np.abs(data.xmat[bid].reshape(3,3))@(DIMS/2))[0]
    result={'case':case,'dt_s':dt,'solver':solver,'iterations':iterations,'direct_stiffness_s_minus2':k,'direct_damping_s_minus1':damping,'constant_solimp':.95,'representation':representation,'native_version':mj.__version__,'tstart_s':tstart,'duration_s':duration,'tend_s':data.time,'source_release_s':original['release']['time_s'],'source_stop_s':original['time_s'],'source_release_inertial_kick_m_s':original['release']['payload_inertial_delta_v_m_s'],'payload_final_position_m':data.qpos[2:5].tolist(),'payload_final_quaternion_wxyz':qfinal.tolist(),'payload_final_velocity_m_s':vel.tolist(),'payload_final_omega_deg_s':np.degrees(w).tolist(),'orientation_change_deg':math.degrees(angle),'payload_inertial_kick_difference_m_s':float(vel[0]-original['release']['payload_inertial_delta_v_m_s']),'final_payload_aft_relative_carrier_m':float(payload_aft_from_carrier),'rear_contact_first_s':min(rear_times) if rear_times else None,'rear_contact_last_s':max(rear_times) if rear_times else None,'rear_unload_events_s':unloads,'rear_recontact_events_s':recontact_after_unload,'contact_absolute_impulse_by_group_Ns':contacts_by_group,'post_source_release_absolute_impulse_by_group_Ns':post_source_impulse,'max_overlap_m':maxpenetration,'peak_contact_force_N_unrated':peakforce,'initial_overlap_m':initial_overlap,'initial_gap_adjustment_m':{'x':dx,'z':dz},'conservation':{'total_x_momentum_initial_kg_m_s':P0,'total_x_momentum_residual_kg_m_s':P-P0,'payload_linear_impulse_residual_Ns':(MP*(vel-vel0)-impulse).tolist(),'payload_angular_impulse_residual_Nms':(H-H0-angimpulse).tolist(),'native_generalized_vs_contact_force_max_N':native_force_error,'kinetic_energy_change_J':T-T0,'motor_work_J':motorwork,'kinetic_minus_motor_work_J':T-T0-motorwork,'energy_scope':'Difference includes unmeasured contact regularization,damping/friction and integration error;not automatically numerical error.'},'solver_max_iterations_used':maxsolver,'native_warning_increments':[int(x.number)-w for x,w in zip(data.warning,warn0)],'wall_s':time.monotonic()-started,'limitations':['Open-loop source force replay,not perturbed electrical feedback','Ideal host/carrier X guides;no host attitude/side compliance','Uniform4kg340.5×100×100mm payload surrogate','Contact regularization/friction/damping unmeasured sensitivities','Final1ms before source release through arrest and0.35s window;powered return and feeder capture excluded','Primitive collision surfaces are a documented CAD subset;no complete manufactured model']}
    result.update({'solver_full_budget_steps':solver_budget_steps,'max_native_termination_gradient':max_termination_gradient,'payload_initial_position_m':initial_position.tolist(),'payload_initial_velocity_m_s':vel0.tolist(),'payload_initial_omega_deg_s':np.degrees(w0).tolist(),'freeflight_position_residual_m':(data.qpos[2:5]-initial_position-vel0*duration).tolist(),'exact_inertia_kg_m2':INERTIA.tolist()})
    stem=f'{case["id"]}_{round(dt*1e6,3):g}us_{solver}{iterations}_k{k:g}_b{damping:g}_{representation}'
    if save:
        (HERE/'runs').mkdir(exist_ok=True)
        (HERE/'runs'/f'{stem}.json').write_text(json.dumps(result,indent=2)+'\n')
        (HERE/'runs'/f'{stem}.xml').write_text(xml)
        with (HERE/'runs'/f'{stem}.csv').open('w',newline='') as f:
            out=csv.writer(f);out.writerow(['time_s','x_m','y_m','z_m','qw','qx','qy','qz','vx_m_s','vy_m_s','vz_m_s','wx_deg_s','wy_deg_s','wz_deg_s','carrier_relative_x_m','carrier_relative_v_m_s','active_groups','source_net_force_N','max_overlap_sofar_m']);out.writerows(rows)
    return result

CASES=[
 {'id':'freeflight','mu':0,'disable_contact':True,'initial_z_gap_m':.0005,'initial_omega_deg_s':[1,1,1],'vy_m_s':.002},
 {'id':'aligned','mu':0},
 {'id':'offset','mu':.1,'y_offset_m':.0005,'initial_z_gap_m':.0002},
 {'id':'yaw','mu':.1,'yaw_deg':.1,'initial_z_gap_m':.0002},
 {'id':'pitch','mu':.1,'pitch_deg':.1},
 {'id':'rates','mu':.1,'initial_z_gap_m':.0005,'initial_omega_deg_s':[1,1,1],'vy_m_s':.002},
 {'id':'one_rear_pad','mu':.1,'rear_mask':'single'},
 {'id':'half_keeper','mu':.1,'keeper_shift_mm':6},
 {'id':'source_adverse','mu':.1,'source':'adverse'},
]
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--case',default='aligned');parser.add_argument('--dt-us',type=float,default=50);parser.add_argument('--iterations',type=int,default=100);parser.add_argument('--solver',default='Newton');parser.add_argument('--stiffness',type=float,default=1e6);parser.add_argument('--damping',type=float,default=2000);parser.add_argument('--representation',default='box');args=parser.parse_args()
    case=next(c for c in CASES if c['id']==args.case)
    r=run(case,args.dt_us/1e6,args.iterations,args.solver,args.stiffness,args.damping,args.representation)
    print(json.dumps(r,indent=2))
