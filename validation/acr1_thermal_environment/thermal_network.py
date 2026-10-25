"""Repeated ACR1 duty in a CAD-derived vacuum conduction/radiation network.

Twenty-four thermal nodes retain actual material masses. Diffuse-gray radiosity
includes internal reflections,Earth IR,finite-disc albedo,deep-space exchange and
uncertain host radiation. Explicit release events remove payload thermal links
and use the corresponding CAD radiation stage. No air cooling is present.
"""
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import root
from scipy.stats import qmc

HERE=Path(__file__).resolve().parent
SIGMA=5.670374419e-8
NN=24


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class ThermalNetwork:
    def __init__(self,inputs,environment,parameters,command,samples=4096,source_cases=None,regen_cell_V=2.9,cell_temperature_max_C=65):
        self.c=inputs;self.e=environment;self.p=parameters;self.command=command
        self.mesh=dict(np.load(HERE/'geometry/cad_mesh.npz'))
        self.C=self.mesh['heat_capacity']*parameters['heat_capacity_scale']
        self.period=2*np.pi*np.sqrt((inputs['earth_radius_m']+inputs['orbit_altitude_m'])**3/inputs['earth_mu_m3_s2'])
        self.host=environment['host_interface_C']+273.15
        self.release_order=[x for level in range(5,-1,-1) for x in [14+level,8+level]]
        cases=json.loads((HERE/'inputs/COUPLED_SHOT.json').read_text())['cases'] if source_cases is None else source_cases
        self.regen_cell_V=regen_cell_V
        self.cell_max_K=cell_temperature_max_C+273.15
        self.shot=next(x for x in cases if x['target_m_s']==command and x['adverse'] and x['inductance_H']==3e-6)
        budget=json.loads((HERE/'inputs/DESIGN_BUDGETS.json').read_text())['copper_thermal']
        hotspot=next(x for x in budget['cases'] if x['target_m_s']==command and x['adverse'] and x['L_H']==3e-6)
        baseline=json.loads((HERE/'inputs/COUPLED_SHOT.json').read_text())['cases']
        old=next(x for x in baseline if x['target_m_s']==command and x['adverse'] and x['inductance_H']==3e-6)
        integral_ratio=self.shot['conservative_phase_current_sq_with_ripple_A2s']/old['conservative_phase_current_sq_with_ripple_A2s']
        self.hotspot_increment=(hotspot['mesh_max_local_adiabatic_rise_K_observation']-hotspot['bulk_copper_rise_K_upper'])*integral_ratio
        self.hotspot_decay=budget['90mm_diffusion_time_s']
        fraction=environment['optical_fraction']
        self.alpha=np.full(NN,.16+fraction*(.88-.16));self.epsilon=np.full(NN,.03+fraction*(.88-.03))
        self.alpha[1]=.30+fraction*(.98-.30);self.epsilon[1]=.03+fraction*(.63-.03)
        self.alpha[2]=.6;self.epsilon[2]=.85
        self.alpha[4]=.4;self.epsilon[4]=.3
        self.alpha[8:20]=.3;self.epsilon[8:20]=.6
        # Unlocated electronics get no radiating geometry; these values therefore
        # confer no space-radiation cooling credit.
        self.stages=[]
        for stage in range(13):
            stem=f'radiation_{samples}' if stage==0 else f'radiation_s{stage:02d}_{samples}'
            path=HERE/'geometry'/(stem+'.npz')
            if not path.exists() and samples!=4096:
                stem='radiation_4096' if stage==0 else f'radiation_s{stage:02d}_4096';path=HERE/'geometry'/(stem+'.npz')
            g=dict(np.load(path));A=g['areas'];F=g['view_factors'];E=np.divide(g['earth_areas'],A,out=np.zeros(NN),where=A>0)
            escape=np.divide(g['escape_areas'],A,out=np.zeros(NN),where=A>0)
            block=parameters['host_replaces_Earth_view_fraction'];fh=block*E;fe=(1-block)*E;fs=escape-E
            ext=fe*environment['earth_IR_W_m2']+fh*SIGMA*self.host**4+fs*SIGMA*inputs['space_temperature_K']**4
            I=np.eye(NN);B=I-(1-self.epsilon)[:,None]*F;inv=np.linalg.inv(B)
            radiant=A[:,None]*(F-I)@inv@np.diag(self.epsilon)*SIGMA
            external=A*((F-I)@inv@((1-self.epsilon)*ext)+ext)
            # Solar/albedo diffuse reflections are separately conserved.
            solar_matrix=np.diag(A*self.alpha)@(F@np.linalg.solve(I-(1-self.alpha)[:,None]*F,np.diag(1-self.alpha))+I)
            ts=np.linspace(0,2*np.pi,721)
            beta=np.radians(environment['beta_deg']);bidx=min(int(np.searchsorted(g['beta'],beta,side='right'))-1,len(g['beta'])-2);bidx=max(bidx,0)
            w=(beta-g['beta'][bidx])/(g['beta'][bidx+1]-g['beta'][bidx])
            solar=(1-w)*g['solar'][bidx]+w*g['solar'][bidx+1];albedo=(1-w)*g['albedo'][bidx]+w*g['albedo'][bidx+1]
            proj=np.array([np.interp(ts,g['theta'],solar[:,j]) for j in range(NN)]).T
            alb=np.array([np.interp(ts,g['theta'],albedo[:,j]) for j in range(NN)]).T
            ratio=inputs['earth_radius_m']/(inputs['earth_radius_m']+inputs['orbit_altitude_m'])
            shadow=np.cos(ts)*np.cos(beta)<-np.sqrt(1-ratio**2)
            proj[shadow]=0
            Gsol=environment['solar_W_m2']*np.divide(proj+environment['albedo']*(1-block)*alb,A[None,:],out=np.zeros_like(proj),where=A[None,:]>0)
            Qsol=Gsol@solar_matrix.T
            L,edges=self.conduction(stage)
            self.stages.append(dict(A=A,F=F,ext_irradiance=ext,radiant=radiant,external=external,solar=Qsol,theta=ts,cond=L,edges=edges,
                                    inverse_radiance=inv,escape_areas=g['escape_areas'],geometry_file=str(path.relative_to(HERE))))
        feed=json.loads((HERE/'inputs/FEEDER_SIZING.json').read_text())['feed_cases'];lift=json.loads((HERE/'inputs/LIFT_SIZING.json').read_text())['cases']
        self.feed_W=24*max(x['motor_current_peak_A'] for x in feed)
        self.lift_W=24*max(x['current_peak_A'] for x in lift if x['gravity_m_s2']==0 and x['moving_mass_study_kg']==10 and x['resistance_N']<=100)

    def conduction(self,stage):
        p=self.p;edges=[]
        def add(a,b,g,why):edges.append(dict(a=a,b=b,G_W_K=float(g),basis=why))
        def series(*g):return 1/sum(1/x for x in g)
        h=p['interface_h_W_m2_K'];kg=p['gfrp_k_W_m_K'];ka=p['aluminium_k_W_m_K']
        add(1,2,series(kg*.27216/.002,h*.27216),'216actual7x90mm active copper sections onboth2mmGFRPfaces; seriescontact andthrough-thickness conduction')
        add(2,20,series(kg*(2*.002*1.74)/.03,h*(11*.012*.031)),'NarrowGFRP outerwing lateral conduction and11actual12x31mm support-arm contacts')
        support=7*ka*.000156/.110+7*ka*.000156/.070
        add(20,0,series(support,14*.2*(h/100)),'14actual16mm3mmwall tube supports; missing joint conductance scaled fromexplicit reference allocation')
        for bank in [21,22]:add(bank,0,series(2*ka*.000252/1.12,4*.2*(h/100)),'Twoactual24mm3mmwall bank columns perbank; contact allocation is not a measured bolted interface')
        add(23,0,series(4*ka*.000204/1.24,4*.2*(h/100)),'Fouractual20mm3mmwall lift columns; seriesunmeasured mounting contacts')
        add(4,3,series(p['magnet_k_W_m_K']*.06048/.008,h*.06048),'Two42x8x90mm magnet arrays seatagainst carrierplates; actualpreload/bond thermalcontact unknown')
        add(3,20,p['rolling_sled_track_conductance_W_K'],'Rolling/index interface sensitivity; no vacuum air conduction')
        add(5,3,series(ka*.000448/.008,h*.000448)+.01*(h/100),'Four14x8mm pallet feet andbounded parallelpin contact; noqualifiedcontact assumed')
        add(6,7,p['cells_electronics_conductance_W_K'],'Unlocatedcapacitor/cage/control coupling input,no invented surface area')
        add(7,0,p['electronics_mount_conductance_W_K'],'Unlocated7kg allowance thermalattachment sensitivity,not represented CAD')
        for payload in self.release_order[stage:]:add(payload,21 if payload<14 else 22,p['payload_stored_conductance_W_K'],'Nominalstored3U floor/keeper interface; rail/preload conductance is an unknown payload-ICD quantity')
        L=np.zeros((NN,NN))
        for e in edges:
            a,b,g=e['a'],e['b'],e['G_W_K'];L[a,a]-=g;L[b,b]-=g;L[a,b]+=g;L[b,a]+=g
        L[0,0]-=p['host_mount_conductance_W_K']
        L[7,7]-=p.get('electronics_direct_host_conductance_W_K',0)
        return L,edges

    def solar(self,t,stage):
        g=self.stages[stage];phase=(t%self.period)/self.period*720;i=min(int(phase),719);w=phase-i
        return g['solar'][i]*(1-w)+g['solar'][i+1]*w

    def continuous_heat(self,t,mission):
        Q=np.zeros(NN);Q[7]=1.1664+self.p['unallocated_standby_heat_W']
        if not mission:return Q
        interval=int(t//450)
        if 1<=interval<=12:Q[7]+=self.shot['cap_draw_J']*(1/self.p['charger_efficiency']-1)/450
        for k in range(12):
            rel=(k+1)*450;age=t-(rel-338);payload=self.release_order[k];bank=21 if payload<14 else 22
            if 0<=age<22 or 26<=age<146 or 186<=age<306 or 316<=age<338:Q[23]+=self.lift_W
            if 146<=age<186:Q[bank]+=self.feed_W
        return Q

    def rhs(self,t,y,stage=0,mission=False):
        T=y[:NN];g=self.stages[stage]
        qcond=g['cond']@T;qcond[0]+=self.p['host_mount_conductance_W_K']*self.host
        qcond[7]+=self.p.get('electronics_direct_host_conductance_W_K',0)*self.host
        # Conservative contact topology for the source custody sequence.
        if mission and stage<12:
            rel=(stage+1)*450;f=np.clip((t-(rel-192))/40,0,1);pnode=self.release_order[stage];bank=21 if pnode<14 else 22
            gb=self.p['payload_stored_conductance_W_K']*f;gp=self.p['payload_pallet_conductance_W_K']*f
            change=gb*(T[bank]-T[pnode]);qcond[pnode]-=change;qcond[bank]+=change
            change=gp*(T[5]-T[pnode]);qcond[pnode]+=change;qcond[5]-=change
        qsolar=self.solar(t,stage);qrad=g['radiant']@(T**4)+g['external'];qheat=self.continuous_heat(t,mission)
        dT=(qcond+qsolar+qrad+qheat)/self.C
        # Departedpayload temperature is stored only as its release enthalpy;
        # it neither remains onthe carrier norreceives a postdeparture rating.
        for p in self.release_order[:stage]:dT[p]=0
        host=self.p['host_mount_conductance_W_K']*(self.host-T[0])+self.p.get('electronics_direct_host_conductance_W_K',0)*(self.host-T[7])
        return np.r_[dT,qsolar.sum(),qrad.sum(),qheat.sum(),host]

    def step(self,t,y,h,stage=0,mission=False):
        k1=self.rhs(t,y,stage,mission);k2=self.rhs(t+h/2,y+h*k1/2,stage,mission)
        k3=self.rhs(t+h/2,y+h*k2/2,stage,mission);k4=self.rhs(t+h,y+h*k3,stage,mission)
        return y+h*(k1+2*k2+2*k3+k4)/6

    def storage_initial(self,dt):
        g=self.stages[0];mean_solar=g['solar'][:-1].mean(axis=0);constant=np.zeros(NN);constant[7]=1.1664+self.p['unallocated_standby_heat_W'];constant[0]+=self.p['host_mount_conductance_W_K']*self.host
        constant[7]+=self.p.get('electronics_direct_host_conductance_W_K',0)*self.host
        def f(T):return g['cond']@T+g['radiant']@(T**4)+g['external']+mean_solar+constant
        result=root(f,np.full(NN,self.host),jac=lambda T:g['cond']+g['radiant']*4*(T**3)[None,:],tol=1e-10)
        assert np.max(abs(f(result.x)))<1e-6,(result.message,np.max(abs(f(result.x))))
        mean=result.x;linear=(g['cond']+g['radiant']*4*(mean**3)[None,:])/self.C[:,None]
        forcing=np.fft.rfft(g['solar'][:-1]-mean_solar,axis=0)/720
        T=mean.copy();omega=2*np.pi/self.period
        for n in range(1,min(65,len(forcing))):
            response=np.linalg.solve(1j*n*omega*np.eye(NN)-linear,forcing[n]/self.C)
            T+=2*response.real
        # Verify the nonlinear periodicstorage state against actual forcing.
        worst=math.inf;cycles=0;y=np.r_[T,np.zeros(4)]
        for cycle in range(self.c['periodic_storage_max_orbits']):
            before=y[:NN].copy();now=0.
            while now<self.period-1e-8:
                h=min(dt,self.period-now);y=self.step(now,y,h);now+=h
            worst=float(np.max(abs(y[:NN]-before)));cycles=cycle+1
            if worst<self.c['periodic_storage_tolerance_K']:break
        assert worst<self.c['periodic_storage_tolerance_K'],worst
        return y[:NN],dict(mean_balance_max_residual_W=float(np.max(abs(f(mean)))),periodic_validation_orbits=cycles,periodic_orbit_max_delta_K=worst,
                          interpretation='Numericalperiodicpassivestorage condition,not an actual prelaunch temperature orauthorized wait duration.')

    def run(self,dt=10,history=False):
        T,storage=self.storage_initial(dt);y=np.r_[T,np.zeros(4)];initial=T.copy();stage=0;time=0.;released=[];records=[]
        minimum=T.copy();maximum=T.copy();local=0.;hotspot=max(T[1],T[1]+local);junction=-math.inf
        horizon=5400+self.period*self.c['postcampaign_orbits'];times=set([0.,horizon])
        for rel in np.arange(1,13)*450:
            times.update([float(rel+x) for x in [-338,-316,-312,-192,-152,-32,-22,0,17,450] if 0<=rel+x<=horizon])
        stops=sorted(times);pulse=np.arange(1,13)*450;energy_pulses=0.;energy_residual=0.;rad_balance=0.
        def sample():
            if history:records.append([time,*y[:NN],local,*y[NN:]])
        sample()
        for stop in stops[1:]:
            while time<stop-1e-8:
                h=min(dt,stop-time);y=self.step(time,y,h,stage,True);local*=math.exp(-h/self.hotspot_decay);time+=h
                minimum=np.minimum(minimum,y[:NN]);maximum=np.maximum(maximum,y[:NN]);hotspot=max(hotspot,y[1]+local)
                if history and (not records or time-records[-1][0]>=30):sample()
            if stage<12 and abs(stop-pulse[stage])<1e-7:
                ledger=self.shot['energy_ledger'];E=np.zeros(NN);E[1]=ledger['copper_J'];E[6]=ledger['bank_J'];E[7]=ledger['inverter_J']+ledger['auxiliary_J']
                E[3]=self.shot['mechanical_friction_dissipation_J']/2;E[20]=E[3]
                y[:NN]+=E/self.C;y[NN+2]+=E.sum();energy_pulses+=E.sum();local+=self.hotspot_increment
                maximum=np.maximum(maximum,y[:NN]);hotspot=max(hotspot,y[1]+local)
                node=self.release_order[stage]
                released.append(dict(slot=stage+1,t_s=time,node=node,payload_name=str(self.mesh['payload_names'][node-8]),temperature_C=float(y[node]-273.15),pallet_temperature_C=float(y[5]-273.15)))
                # A conservativecomponent screen,not a time-resolvedjunction
                # prediction: totalhotdevicepulse energy heats its allocated
                #6g package adiabatically; peakjunction-to-case uses catalogueR.
                peakI=self.shot['peak_phase_current_A'];V=32*self.regen_cell_V;ripple=V/(4*3e-6*40000);ron=.0097*2/10
                P=1.5*ron*peakI**2+ron*ripple**2/4+2*V*(peakI+ripple/2)*.0000002*40000+6
                hotshare=3*1.25**2/60;package_C=.006*800*self.p['heat_capacity_scale']
                junction=max(junction,float(y[7]-273.15+ledger['inverter_J']*hotshare/package_C+P*hotshare*.29))
                stage+=1;sample()
            residual=float(self.C@(y[:NN]-initial)-sum(y[NN:]));energy_residual=max(energy_residual,abs(residual))
            # Radiosity independently balancesincomingexternal minusescaping
            # IR power at the current state; internalradiation cannotcreateheat.
            g=self.stages[stage];T=y[:NN]
            J=g['inverse_radiance']@(self.epsilon*SIGMA*T**4+(1-self.epsilon)*g['ext_irradiance'])
            independent=float(g['A']@g['ext_irradiance']-g['escape_areas']@J)
            rad_balance=max(rad_balance,abs(float((g['radiant']@(T**4)+g['external']).sum())-independent))
        # Linearized extraelectronics-heat sensitivity is a requirement aid;
        # it does notinvent an actualcontrollerstandby dissipation.
        g=self.stages[12];jac=g['cond']+g['radiant']*4*(y[:NN]**3)[None,:]
        active=[i for i in range(NN) if i not in self.release_order]
        load=np.zeros(len(active));load[active.index(7)]=1
        response=np.linalg.solve(-jac[np.ix_(active,active)],load)
        sensitivity=float(response[active.index(6)])
        face_min=(14*23e-6*(minimum[3]-293.15)-8*7e-6*(maximum[4]-293.15)-3*17e-6*(maximum[1]-293.15)-2*50e-6*(maximum[2]-293.15))
        result=dict(environment=self.e,parameters=self.p,command_m_s=self.command,node_names=[str(x) for x in self.stages[0].get('node_names',[])],
                    storage=storage,temperature_min_C=(minimum-273.15).tolist(),temperature_max_C=(maximum-273.15).tolist(),
                    final_temperature_C=(y[:NN]-273.15).tolist(),copper_local_FE_screen_max_C=float(hotspot-273.15),
                    MOS_peak_junction_conservative_upper_C=junction,
                    selected_cell_catalogue_band_C=[-40,self.cell_max_K-273.15],cell_catalogue_band_screen_pass=bool(minimum[6]>=233.15 and maximum[6]<=self.cell_max_K),
                    copper_adverse100C_resistance_regime_screen_pass=bool(hotspot<=373.15),
                    MOS_junction_absolute_max_upper_bound_clear=bool(junction<=175),
                    magnet_reference_coefficient20to100C_valid=bool(minimum[4]>=293.15 and maximum[4]<=373.15),
                    magnet_grade_thermal_acceptance='No selectedgrade/BH(T),bond orcorrosioncoating limit is available; no universal80C orCurie acceptance is assigned.',
                    payload_releases=released,
                    conservative_local_magnetic_gap_thickness_change_mm=float(face_min),
                    extra_electronics_heat_to_cells_linearized_K_W=sensitivity,
                    first_order_unallocated_electronics_heat_margin_W=float((self.cell_max_K-maximum[6])/sensitivity),
                    integrated_energy_J=dict(absorbed_solar=float(y[NN]),net_IR_exchange=float(y[NN+1]),represented_generated_heat=float(y[NN+2]),host_conduction=float(y[NN+3])),
                    max_global_energy_balance_residual_J=energy_residual,max_independent_radiosity_balance_residual_W=rad_balance,
                    pulse_heat_total_J=energy_pulses,dt_s=dt,horizon_s=horizon)
        if history:result['history']=records
        return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--probe',action='store_true');p.add_argument('--no-uncertainty',action='store_true');args=p.parse_args()
    c=json.loads((HERE/'THERMAL_INPUTS.json').read_text());out=HERE/'results';out.mkdir(exist_ok=True);results=[]
    envs=c['environment_cases'][-1:] if args.probe else c['environment_cases']
    for e in envs:
        for command in c['heat_cases']['commands_m_s']:
            model=ThermalNetwork(c,e,copy.deepcopy(c['reference_parameters']),command);record=model.run(history=True)
            record['case_id']=e['id']+f'_{command}mps';record['node_names']=json.loads((HERE/'geometry/RADIATION_4096.json').read_text())['node_names']
            (out/(record['case_id']+'.json')).write_text(json.dumps(record,indent=2)+'\n');results.append({k:v for k,v in record.items() if k!='history'})
            print(json.dumps(dict(case=record['case_id'],cell_max_C=record['temperature_max_C'][6],copper_screen_C=record['copper_local_FE_screen_max_C'],magnet_max_C=record['temperature_max_C'][4],energy_residual_J=record['max_global_energy_balance_residual_J'])),flush=True)
    uncertainty=[]
    if not args.probe and not args.no_uncertainty:
        bands=c['uncertainty'];keys=[x for x in bands if isinstance(bands[x],list)];design=qmc.LatinHypercube(len(keys),seed=bands['seed']).random(bands['samples'])
        for index,row in enumerate(design):
            parameters=copy.deepcopy(c['reference_parameters']);env=copy.deepcopy(c['environment_cases'][-1])
            for key,q in zip(keys,row):
                lo,hi=bands[key];value=math.exp(math.log(lo)+q*math.log(hi/lo)) if lo>0 and key not in ['host_interface_C','optical_fraction','heat_capacity_scale'] else lo+q*(hi-lo)
                if key in ['host_interface_C','optical_fraction']:env[key]=value
                else:parameters[key]=value
            for command in c['heat_cases']['commands_m_s']:
                record=ThermalNetwork(c,env,parameters,command).run();record['sample']=index;uncertainty.append(record)
            print(f'Completeduncertaintyinput{index+1}/{len(design)}',flush=True)
    result=dict(study=c['study'],source_sha256=sha(__file__),inputs_sha256=sha(HERE/'THERMAL_INPUTS.json'),
                geometry_source_sha256=sha(HERE/'geometry/cad_mesh.npz'),cases=results,uncertainty=uncertainty,
                scope='Actualsource loss/material/CAD/duty-based environmental sensitivity; representative unknownconductance/finish/host/heat-capacity inputs are not qualification orreliability probabilities.')
    name='PROBE_RESULTS.json' if args.probe else 'THERMAL_RESULTS.json';(HERE/name).write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
