#!/usr/bin/env python3
"""Separate all-component current/PM reaction screen; frozen models remain untouched.

Per-array magnetostatic reciprocity: reaction on each PM source equals minus
volume-integrated J×B from that source on the winding. No AC/reaction/steel solve.
"""
from pathlib import Path
import hashlib,importlib.util,json,math,os,sys,time
os.environ.setdefault('MPLCONFIGDIR','/tmp/volley-sd-mpl');os.environ.setdefault('XDG_CACHE_HOME','/tmp/volley-sd-cache')
sys.dont_write_bytecode=True
import numpy as np
import magpylib as magpy
H=Path(__file__).resolve().parent;R=H.parents[1];S=R/'validation/acr1'
spec=importlib.util.spec_from_file_location('frozen_finite_motor',S/'analysis/finite_motor.py');model=importlib.util.module_from_spec(spec);spec.loader.exec_module(model)
p=json.loads((S/'cad/PARAMETERS.json').read_text());field=model.make_field(p);children=list(field.children)
arrays=[magpy.Collection(*(s.copy()for s in children if s.position[1]<0)),magpy.Collection(*(s.copy()for s in children if s.position[1]>0))]
phase_angles=np.array([0,-2*np.pi/3,2*np.pi/3]);phasors=np.exp(1j*phase_angles)
shots=json.loads((S/'analysis/COUPLED_SHOT.json').read_text());supported=[c for c in shots['cases']if c['target_m_s']in[1,2,3]];Imax=max(c['peak_phase_current_A']for c in supported)
receipts=[];start=time.monotonic()
def sums(points,directions,phases):
    result=np.zeros((2,3,3))
    for k,array in enumerate(arrays):
        for begin in range(0,len(points),2000):
            end=begin+2000;B=array.getB(points[begin:end]);force=-np.cross(directions[begin:end],B)
            for ph in range(3):result[k,ph]+=np.sum(force[phases[begin:end]==ph],axis=0)
    return result

def uniform(x,order,ret_order,cross_order):
    m=p['magnetic'];center=(p['launch']['home_aft_x']+sum(m['array_active_relative_x'])/2)/1000+x;nx,ny,nz=order;g=[np.polynomial.legendre.leggauss(n)for n in order];points=[];directions=[];phases=[]
    for i in range(m['stator_belts']):
        phase,sg=((0,1),(2,-1),(1,1),(0,-1),(2,1),(1,-1))[i%6];cx=(m['stator_x_start']+i*m['stator_pitch']+3.5)/1000-center
        for ix,wx in zip(*g[0]):
            for iy,wy in zip(*g[1]):
                for iz,wz in zip(*g[2]):
                    points.append([cx+.007*ix/2,.006*iy/2,.090*iz/2]);directions.append([0,0,sg*.090*wx*wy*wz/8]);phases.append(phase)
    ga,wa=np.polynomial.legendre.leggauss(ret_order);cg,cw=np.polynomial.legendre.leggauss(cross_order)
    for ph,offset,gap_y in [(0,0,-.0035),(2,1,0),(1,2,.0035)]:
        indices=list(range(offset,m['stator_belts'],3))
        for j,(i,k)in enumerate(zip(indices,indices[1:])):
            sg=(1 if j%2==0 else -1)*(-1 if ph==2 else 1);xi=(m['stator_x_start']+i*m['stator_pitch']+3.5)/1000-center;xk=(m['stator_x_start']+k*m['stator_pitch']+3.5)/1000-center;path=[(xi,0,sg*.045),(xi,0,sg*.0525),(xi,gap_y,sg*.0525),(xi,gap_y,sg*.0675),(xk,gap_y,sg*.0675),(xk,gap_y,sg*.0525),(xk,0,sg*.0525),(xk,0,sg*.045)]
            for aa,bb in zip(path,path[1:]):
                aa=np.array(aa);bb=np.array(bb);dl=(bb-aa)/2
                if np.linalg.norm(dl)==0:continue
                axis=int(np.argmax(abs(dl)));other=[d for d in range(3)if d!=axis]
                widths=[.003,.007]if axis==0 else[.007,.005]if axis==1 else[.007,.006 if aa[1]==0 and bb[1]==0 else .003]
                for gi,wi in zip(cg,cw):
                    for gj,wj in zip(cg,cw):
                        shift=np.zeros(3);shift[other[0]]=gi*widths[0]/2;shift[other[1]]=gj*widths[1]/2
                        for q,w in zip(ga,wa):points.append((aa+bb)/2+q*dl+shift);directions.append(w*dl*wi*wj/4);phases.append(ph)
    return sums(np.array(points),np.array(directions),np.array(phases))

def summarize(x,coeff,method,**extra):
    axial=coeff[:,:,0].sum(axis=0);pinch=(coeff[0,:,1]-coeff[1,:,1])/2;common=(coeff[0,:,1]+coeff[1,:,1])/2;Cx=axial@phasors;Cp=pinch@phasors;Cc=common@phasors;theta=np.pi/2-np.angle(Cx)
    record={'displacement_m':x,'method':method,'per_array_per_phase_field_XYZ_N_per_A':coeff.tolist(),'axial_amplitude_N_per_peak_A':float(abs(Cx)),'opposed_normal_amplitude_any_electrical_phase_N_per_peak_A':float(abs(Cp)),'normal_common_mode_amplitude_N_per_peak_A':float(abs(Cc)),'supported_max_phase_current_A':Imax,'opposed_normal_envelope_at_supported_current_N':float(abs(Cp)*Imax),'ideal_max_thrust_phase_opposed_normal_N':float(np.imag(np.exp(1j*theta)*Cp)*Imax),'phase_error_brackets':{str(error):{'max_abs_opposed_normal_N':float(max(abs(np.imag(np.exp(1j*(theta+np.deg2rad(sign*error)))*Cp))for sign in [-1,1])*Imax)}for error in [0,1,5,15,90]},'elapsed_s':time.monotonic()-start,**extra}
    receipts.append(record);print(json.dumps({k:record[k]for k in ['displacement_m','method','axial_amplitude_N_per_peak_A','opposed_normal_envelope_at_supported_current_N','ideal_max_thrust_phase_opposed_normal_N','elapsed_s']}),flush=True)
for x in [0.,.65,1.3,1.4,1.507]:summarize(x,uniform(x,(3,3,5),5,3),'uniform actual active bars + source return-path transverse quadrature',active_order=[3,3,5],return_order=5,return_cross_order=3)
summarize(.65,uniform(.65,(5,5,9),7,3),'refined uniform-bar/return quadrature',active_order=[5,5,9],return_order=7,return_cross_order=3)
# One actual FE-current station cross-check, matching the original scalar-X capture.
x=.65;center=(p['launch']['home_aft_x']+sum(p['magnetic']['array_active_relative_x'])/2)/1000+x;coeff=np.zeros((2,3,3));inputs=[]
for ph,(phase,h)in enumerate([('A',2),('B',3),('C',3)]):
    src=S/'analysis/conduction'/f'phase_{phase}'/f'h{h}';data=np.load(src/'solution.npz');receipt=json.loads((src/'RESULT.json').read_text());q=data['centroid_m'];j=data['J_A_m2_at1V']/receipt['current_at1V_A'];points=np.stack((q[:,0]-center,q[:,2],-q[:,1]),axis=1);directions=np.stack((j[:,0],j[:,2],-j[:,1]),axis=1)*data['element_volume_m3'][:,None]
    coeff[:,ph,:]=sums(points,directions,np.zeros(len(q),dtype=int))[:,0,:];inputs.append({'phase':phase,'solution_sha256':hashlib.sha256((src/'solution.npz').read_bytes()).hexdigest(),'result_sha256':hashlib.sha256((src/'RESULT.json').read_bytes()).hexdigest(),'linear_tetrahedra':len(q)})
summarize(.65,coeff,'actual connected phase DC FE-current centroid integration',current_inputs=inputs)
result={'configuration_id':'VOLLEY-G5-ACR1','study':'SD01 representative three-component current-induced PM reaction screen','records':receipts,'current_envelope_cases':18,'supported_max_phase_current_A':Imax,'field_axes':'X travel,Y gap,Z depth; CAD X=Xfield,Z=Yfield,Y=-Zfield','array_order':['negative-gap(bottom)','positive-gap(top)'],'normal_definition':'Positive opposed normal coefficient increases pinch:0.5*(bottom reactionY−top reactionY). Common mode reported separately.','method':'Per-array magnetostatic reciprocity: reaction on PM array = −integral(J×B_array)dV over winding; free-space prescribed cuboid sources, prescribed linear DC current.','limits':['Representative0/650/1300/1400/1507mm stations only; no full stroke/commutation/active-brake map or rigorous global envelope.','Source conduction centroid quadrature and current meshes unchanged; uniform bends/returns remain approximations.','AC skin/proximity, induced/reaction fields, conductive supports, cable currents, steel perturbation and calibrated controller phase errors omitted.','PM self-mutual3.01kN pinch remains DC and is not included as oscillatory current force.','No measured load, electromagnetic qualification or physical airgap/rating claim.'],'source_identities':{str(q.relative_to(R)):hashlib.sha256(q.read_bytes()).hexdigest()for q in [S/'analysis/finite_motor.py',S/'analysis/current_field_force.py',S/'cad/PARAMETERS.json',S/'analysis/COUPLED_SHOT.json']}}
(H/'CURRENT_NORMAL_FORCE.json').write_text(json.dumps(result,indent=2)+'\n')
