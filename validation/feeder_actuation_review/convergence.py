"""Analytic polynomial extrema/integrals cross-check the sampled drive screen.

Same governing equations, different evaluation method. This establishes numerical
consistency, not independent physical correlation or a second technical review.
"""
from pathlib import Path
import json,math
import numpy as np
from numpy.polynomial import polynomial as poly
H=Path(__file__).resolve().parent
data=json.loads((H/'INTEGRATED_DRIVE.json').read_text())
def roots(coeff):
    return [float(x.real) for x in poly.polyroots(coeff) if abs(x.imag)<1e-8 and 0<x.real<1]
checks=[];refinements=[]
for c in data['cases']:
    T=c['time_s'];eg=c['gear_efficiency_assumed'];es=c['screw_efficiency_assumed']
    K=.002/(2*math.pi*4.5*eg*es)
    constant=c['resistance_N']*K+c['output_drag_Nm']/(4.5*eg)
    gain=c['mass_kg']*K+data['total_rotating_input_inertia_kg_m2']*2*math.pi*4.5/.002
    q=np.array([constant,60, -180,120],float);q[1:]*=gain*.2/T**2
    splits=[0,*sorted(roots(q)),1]
    N=np.array([0,0,30,-60,30],float)*(.2/T*60/.002*4.5)
    maxima=[];integral=poly.polyint(q);absolute_integral=0.
    for lo,hi in zip(splits,splits[1:]):
        sign=1 if poly.polyval((lo+hi)/2,q)>=0 else -1
        P=poly.polyadd(N,20.4*1000*sign*q)
        points=[lo,hi,*[x for x in roots(poly.polyder(P)) if lo<x<hi]]
        maxima.extend(poly.polyval(x,P) for x in points)
        absolute_integral+=abs(poly.polyval(hi,integral)-poly.polyval(lo,integral))
    exact_torque=constant+gain*(10/math.sqrt(3))*.2/T**2
    exact_energy=24*T*(absolute_integral/.0414+.089)
    exact_speed_margin=5600-max(maxima)
    exact_pass=exact_torque<=.0418 and exact_speed_margin>=0 and c['peak_force_N']<354 and c['peak_motor_rpm']<8000
    assert exact_pass==c['ambient_catalogue_screen_pass']
    checks.append(dict(time_s=T,exact_peak_torque_Nm=exact_torque,exact_input_energy_proxy_J=exact_energy,exact_speed_curve_margin_rpm=exact_speed_margin,torque_relative_error=(exact_torque-c['peak_motor_torque_Nm'])/exact_torque,energy_relative_error=abs(exact_energy-c['input_energy_proxy_J'])/exact_energy,gate_agrees=True))
    if c['mass_kg']==7.5 and c['resistance_N'] in [5,50] and eg in [.65,.92] and es==.65 and c['output_drag_Nm']==0:
        for n in [101,201,401,801,1601]:
            u=np.linspace(0,1,n);torque=poly.polyval(u,q)
            energy=24*T*np.trapezoid(abs(torque)/.0414+.089,u)
            refinements.append(dict(time_s=T,resistance_N=c['resistance_N'],gear_efficiency_assumed=eg,samples=n,peak_torque_relative_error=abs(max(abs(torque))-exact_torque)/exact_torque,energy_relative_error=abs(energy-exact_energy)/exact_energy))
result=dict(study='IDR-01',method='Cubic torque roots and exact piecewise polynomial absolute integral; quartic speed+absolute-torque extrema.',cases=checks,refinements=refinements,max_801_torque_relative_error=max(x['torque_relative_error'] for x in checks),max_801_energy_relative_error=max(x['energy_relative_error'] for x in checks),all_gate_decisions_agree=True,boundary='Quasistatic catalogue equations only. Numerical exactness within this polynomial model does not establish actual current,temperature,load or performance.')
(H/'CONVERGENCE.json').write_text(json.dumps(result,indent=2)+'\n')
print(len(checks),'analytic gate cross-checks;',len(refinements),'refinement cases;max relative torque/energy error',result['max_801_torque_relative_error'],result['max_801_energy_relative_error'])
