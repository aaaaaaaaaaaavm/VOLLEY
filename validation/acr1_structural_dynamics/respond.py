#!/usr/bin/env python3
"""Conditional finite-shot/slot-sweep response in the genuine native modal basis.

DC pinch remains preload. Normal ripple/damping/mass distribution are explicit
study brackets, never measured inputs or a component-rated forcing claim.
"""
from pathlib import Path
import csv,hashlib,json,os
os.environ.setdefault('MPLCONFIGDIR','/tmp/volley-sd-mpl');os.environ.setdefault('XDG_CACHE_HOME','/tmp/volley-sd-cache')
import numpy as np
from scipy.linalg import expm,eigh
H=Path(__file__).resolve().parent;R=H.parents[1];S=R/'validation/acr1'
b=np.load(H/'MODAL_BASIS.npz');native=json.loads((H/'MODAL_RESULTS.json').read_text());shot=json.loads((S/'analysis/COUPLED_SHOT.json').read_text());principal=next(c for c in shot['cases']if c['trace']);trace=principal['trace'];F0=3010.4806312835844;w0=b['omega_rad_s'];gn=b['G_normal_per_N'];gx=b['G_axial_per_N'];D=b['D_paired'];stress=b['stress_modes'];tstop=principal['time_s'];duration=tstop+.4
map1=json.loads((S/'analysis/FINITE_MOTOR.json').read_text())['stations'];map2=json.loads((S/'analysis/ARREST_FORCE_MAP.json').read_text())['stations'];xs=np.r_[[q['displacement_m']for q in map1],[q['displacement_m']for q in map2[1:]]];ks=np.r_[[q['with_return_N_per_A']for q in map1],[q['N_per_peak_A']for q in map2[1:]]]
source_time=np.r_[0,[r[0]for r in trace],tstop];source_x=np.r_[0,[r[1]for r in trace],principal['stop_position_m']];source_i=np.r_[0,[r[3]for r in trace],0];source_fx=source_i*np.interp(source_x,xs,ks)
Fpeak=float(np.max(np.abs(source_fx)));fractions=[.001,.01,.05];damping=[.005,.02,.05];masses=[('bare_chassis',1.),('uniform_retained_sled_mass',13.127805767068676/native['bare_chassis_mass_kg']),('uniform_sled_plus4kg_payload_mass',17.127805767068676/native['bare_chassis_mass_kg'])];Kmag=500.
# Conservative face budget retains all original static/thermal allocations plus an explicit modal convergence reserve.
static_base=1.3*float(np.max(b['accepted_static_closure_mm']));alloc_per_face=.2+.15+.15+.05;modal_reserve=1.3*native['static_compliance_convergence'][-1]['max_spatial_error_against_accepted_static_mm'];available=2-static_base-2*alloc_per_face-modal_reserve
idx=sorted(set([int(np.argmax(b['accepted_static_closure_mm'])),*np.argmax(np.abs(D),axis=0).tolist(),*np.linspace(0,len(D)-1,24).astype(int).tolist()]))
controls=D[idx]
def vm(s):return np.sqrt(.5*((s[...,0]-s[...,1])**2+(s[...,1]-s[...,2])**2+(s[...,2]-s[...,0])**2)+3*np.sum(s[...,3:]**2,axis=-1))
Sstatic=b['accepted_static_monitor_stress_MPa'];svm=float(np.max(vm(Sstatic)))
def integrate(omega,zeta,forcing,dt):
 n=len(omega);count=forcing.shape[1];A=np.zeros((n,2,2));B0=np.zeros((n,2));B1=np.zeros((n,2))
 for j,w in enumerate(omega):
  M=np.array([[0,1,0,0],[-w*w,-2*zeta*w,1,0],[0,0,0,1],[0,0,0,0]],float);E=expm(M*dt);A[j]=E[:2,:2];B0[j]=E[:2,2]-E[:2,3]/dt;B1[j]=E[:2,3]/dt
 state=np.zeros((n,2));q=np.zeros((n,count))
 for i in range(count-1):
  state=np.einsum('nij,nj->ni',A,state)+B0*forcing[:,i,None]+B1*forcing[:,i+1,None];q[:,i+1]=state[:,0]
 return q

def run(alpha,zeta,dt=1e-4,count=40,save=False):
 t=np.arange(0,duration+dt/2,dt);x=np.interp(t,source_time,source_x);fx=np.interp(t,source_time,source_fx,right=0);env=np.abs(fx)/Fpeak
 K=np.diag(w0[:count]**2)-Kmag*np.outer(gn[:count],gn[:count]);ev,V=eigh(K);assert np.min(ev)>0;omega=np.sqrt(ev/alpha);gnt=V.T@gn[:count];gxt=V.T@gx[:count];Dt=D[:,:count]@V;Ct=controls[:,:count]@V;St=np.einsum('pjc,jk->pkc',stress[:,:count,:],V);stressmax=np.max(vm(St),axis=0) # mode max over monitored integration points
 assert stressmax.shape==(count,)
 dmax=np.max(np.abs(Dt),axis=0);qax=integrate(omega,zeta,gxt[:,None]*fx[None,:]/alpha,dt);rows=[];curves={}
 for pitch in [.008,.048]:
  unit=F0*env*np.sin(2*np.pi*x/pitch);qn=integrate(omega,zeta,gnt[:,None]*unit[None,:]/alpha,dt)
  for frac in fractions:
   q=qax+frac*qn;bound=dmax@np.abs(q);control=Ct@q;observed=np.max(control,axis=0);stressbound=stressmax@np.abs(q)
   rows.append({'uniform_mass_scale':float(alpha),'damping_ratio':zeta,'spatial_pitch_mm':pitch*1000,'normal_ripple_fraction_of_DC':frac,'normal_ripple_peak_N':float(np.max(np.abs(frac*unit))),'finite_incremental_paired_closure_bound_mm':float(np.max(bound)),'finite_control_point_incremental_closure_mm':float(np.max(observed)),'time_of_control_peak_s':float(t[np.argmax(observed)]),'paired_remaining_budget_mm':float(available-np.max(bound)),'conditional_individual_face_residual_mm':float((available-np.max(bound))/2),'monitor_dynamic_vonMises_increment_bound_MPa':float(np.max(stressbound)),'monitor_combined_DC1p3_vonMises_bound_MPa':float(1.3*svm+np.max(stressbound)),'positive_conditional_budget':bool(available>np.max(bound)),'elastic_modes':count,'dt_s':dt})
   if save and pitch==.008 and frac==.05:curves={'time_s':t,'axial_force_N':fx,'position_m':x,'normal_ripple_N':frac*unit,'paired_closure_increment_bound_mm':bound,'control_point_incremental_closure_mm':observed,'conditional_paired_remaining_mm':available-bound,'monitor_dynamic_stress_bound_MPa':stressbound}
 # Steady harmonic sensitivity is a separate continuous dwell, not the finite shot result.
 fgrid=np.unique(np.r_[np.linspace(1,500,1400),omega/(2*np.pi)]);fgrid=fgrid[fgrid<=500];Omega=2*np.pi*fgrid;den=w0[:count] # transformed stiffness frequencies must use feedback-adjusted eigenvalues
 h=gnt[:,None]/(ev[:,None]-alpha*Omega[None,:]**2+1j*2*zeta*np.sqrt(ev[:,None]*alpha)*Omega[None,:]);transfer=dmax@np.abs(h);peak=int(np.argmax(transfer));limit=available/(F0*transfer[peak]);harm={'uniform_mass_scale':float(alpha),'damping_ratio':zeta,'frequency_sweep_Hz':[1,500],'maximum_paired_compliance_bound_mm_per_N':float(transfer[peak]),'peak_frequency_Hz':float(fgrid[peak]),'allowable_normal_ripple_fraction_for_existing_budget':float(limit),'normal_ripple_limit_N':float(F0*limit),'steady_5pct_remaining_paired_budget_mm':float(available-.05*F0*transfer[peak]),'classification':'Continuous-harmonic sensitivity/design limit; no measured ripple/damping or physical rating.'}
 return rows,harm,curves,{'frequency_Hz':fgrid,'transfer_mm_per_N_bound':transfer}
rows=[];harmonic=[];chosen={};sweeps={}
for label,alpha in masses:
 for z in damping:
  out,h,c,sweep=run(alpha,z,save=label=='uniform_sled_plus4kg_payload_mass'and z==.005)
  for q in out:q['mass_case']=label
  h['mass_case']=label;rows.extend(out);harmonic.append(h)
  if c:chosen=c;sweeps=sweep
# Concrete remaining numerical checks: nested modal basis and timestep refinement at the adverse declared bracket.
convergence=[]
for count,dt in [(20,1e-4),(30,1e-4),(40,1e-4),(40,5e-5)]:
 out,_,_,_=run(masses[-1][1],.005,dt,count)
 q=next(v for v in out if v['spatial_pitch_mm']==8 and v['normal_ripple_fraction_of_DC']==.05);convergence.append({'modes':count,'dt_s':dt,'paired_closure_bound_mm':q['finite_incremental_paired_closure_bound_mm'],'control_closure_mm':q['finite_control_point_incremental_closure_mm']})
with(H/'FINITE_CASES.csv').open('w',newline='')as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with(H/'SOURCE_SHOT_FORCE.csv').open('w',newline='')as f:
 w=csv.writer(f);w.writerow(['time_s','position_m','phase_peak_current_A','reconstructed_axial_motor_force_N']);w.writerows(zip(source_time,source_x,source_i,source_fx))
np.savez_compressed(H/'RESPONSE_CURVES.npz',**chosen,**sweeps)
result={'configuration_id':'VOLLEY-G5-ACR1','study':'SD01 conditional source-shot and structural modal response','source_shot_case':'3m/s,nominal,20microhenry','source_trace_spacing_s':.002,'peak_reconstructed_axial_motor_force_N':Fpeak,'DC_normal_force_each_array_N':F0,'DC_classification':'Permanent-magnet mutual attraction retained as static preload; not a 3kN oscillatory load.','normal_force_brackets':{'fractions':fractions,'pitches_mm':[8,48],'envelope':'fraction × DC force × |source axial force|/peak × sin(2pi source position/pitch)','evidence':'Sensitivity only. No calibrated current-dependent normal force or measured ripple spectrum.'},'damping_ratios':damping,'mass_sensitivity':'Uniform density scaling to bare chassis/retained sled/retained sled+4kg payload totals; not actual discrete attachment modes or a bound over all distributions.','magnetic_stiffness_sensitivity_N_mm':Kmag,'magnetic_stiffness_basis':'Rounded500N/mm opposing-gap stiffness sensitivity above largest recorded secant over0..0.8mm per-face closures; not a certified slope bound. Applied rank-one energy-conjugate normal coupling.','available_paired_budget_before_dynamic_mm':float(available),'original_static_1p3_pair_closure_mm':static_base,'original_allocations_each_face_mm':alloc_per_face,'additional_modal_convergence_reserve_mm':float(modal_reserve),'finite_cases':rows,'harmonic_design_limits':harmonic,'response_convergence':convergence,'all_finite_brackets_positive':all(r['positive_conditional_budget']for r in rows),'basis_boundary':'40 native elastic modes on one actual C3D10 mesh. Native mechanical geometric-prestress stiffness and assembly/host/stator dynamics excluded.','airgap_boundary':'Paired face closure is gauge invariant. Individual residual divides the paired budget under the original centring allocation; independent moving stator/support dynamics and as-built centring remain unverified.','stress_boundary':f"Accepted native global nodal extrapolated DC peak is in MODAL_RESULTS. Response stresses bound {native['stress_monitor_points']} declared monitor integration points, including the element incident to the actual accepted static hotspot; not a global dynamic stress/yield/fatigue qualification.",'source_identities':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [S/'analysis/COUPLED_SHOT.json',S/'analysis/FINITE_MOTOR.json',S/'analysis/ARREST_FORCE_MAP.json',S/'analysis/DESIGN_BUDGETS.json',H/'MODAL_BASIS.npz']}}
(H/'RESPONSE_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'finite_cases':len(rows),'all_finite_brackets_positive':result['all_finite_brackets_positive'],'worst_finite_case':min(rows,key=lambda r:r['paired_remaining_budget_mm']),'harmonic_minimum_ripple_limit_fraction':min(r['allowable_normal_ripple_fraction_for_existing_budget']for r in harmonic),'response_convergence':convergence},indent=2))
