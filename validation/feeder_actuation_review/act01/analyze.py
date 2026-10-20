"""ACT-01: torque-speed/load-path screen with independently sourced motor limits."""
from pathlib import Path
import json,math,itertools
import numpy as np
H=Path(__file__).resolve().parent;P=json.loads((H/'parameters.json').read_text())
lead=P['screw_lead_m'];diam=P['screw_pitch_diameter_assumed_m'];root=P['screw_root_m'];L=P['unsupported_screw_length_m']
helix=math.atan(lead/(math.pi*diam));density=7850;E=193e9
# Root-only inertia is a lower bound; multiply by2 as a declared sensitivity allowance.
shaft_mass=density*math.pi/4*root**2*L
Js=2*.5*shaft_mass*(root/2)**2
records=[]
for motor,mass,T,resist,mu,drag,ratio in itertools.product(P['motors'],P['moving_mass_kg'],P['transfer_time_s'],P['resistance_N'],P['thread_friction'],P['nut_drag_Nm'],P['gear_ratio']):
 a=4*P['stroke_m']/T**2;vmax=2*P['stroke_m']/T
 eff=math.tan(helix)/math.tan(helix+math.atan(mu/math.cos(math.radians(P['thread_half_angle_deg']))))
 dt=T/200;t=np.linspace(0,T,201);v=np.where(t<=T/2,a*t,a*(T-t));acc=np.where(t<T/2,a,-a)
 omega=v*2*math.pi/lead;alpha=acc*2*math.pi/lead
 force=resist+mass*acc
 torque_screw=force*lead/(2*math.pi*eff)+drag+Js*alpha
 eta=P['gear_efficiency_assumed'] if ratio>1 else 1.
 torque_motor=torque_screw/(ratio*eta)+motor['rotor_inertia_kg_m2']*alpha*ratio
 rpm=omega*ratio*60/(2*math.pi)
 available=motor['no_load_rpm']-motor['slope_rpm_per_mNm']*np.abs(torque_motor)*1000
 speed_pass=bool(np.all(rpm<=available));torque_pass=bool(np.max(np.abs(torque_motor))<=motor['rated_torque_Nm'])
 # Approximate equivalent drive current, not phase-current/control validation.
 current=np.abs(torque_motor)/motor['kT_Nm_A']+motor['no_load_current_A']
 # Trapezoidal quadrature avoids assumptions about unmodeled PWM/control losses.
 energy=float(np.trapezoid(current*motor['voltage_V'],t))
 screw_rpm=60*vmax/lead
 if screw_rpm<=500:nut_load=P['nut_basis']['catalog_dynamic_N_at500rpm'];nut_rating=True
 elif screw_rpm<=1000:nut_load=P['nut_basis']['catalog_dynamic_N_at500rpm']*.5;nut_rating=True
 else:nut_load=None;nut_rating=False
 nut_pass=bool(nut_rating and max(force)<=nut_load)
 # Simply supported Euler/first-bending limits; actual bearings must establish this boundary.
 A=math.pi*root**2/4;I=math.pi*root**4/64
 buckling=math.pi**2*E*I/L**2
 critical_rpm=60/(2*math.pi)*(math.pi/L)**2*math.sqrt(E*I/(density*A))
 records.append(dict(motor=motor['id'],moving_mass_kg=mass,time_s=T,resistance_N=resist,mu=mu,nut_drag_Nm=drag,ratio=ratio,
  efficiency=eff,max_force_N=float(max(force)),peak_motor_torque_Nm=float(max(abs(torque_motor))),peak_motor_rpm=float(max(rpm)),
  min_speed_margin_rpm=float(min(available-rpm)),catalog_continuous_torque_pass=torque_pass,catalog_voltage_speed_pass=speed_pass,
  nut_rating_available=nut_rating,nut_catalog_screen_pass=nut_pass,all_catalog_screens_pass=torque_pass and speed_pass and nut_pass,
  screw_peak_rpm=screw_rpm,screw80pctcritical_margin=.8*critical_rpm/screw_rpm,root_euler_buckling_margin=buckling/max(force),
  equivalent_current_peak_A=float(max(current)),input_energy_proxy_J=energy,
  direct_motor_thrust_overload_factor=float(max(force)/motor['axial_running_load_N'])))
report={'revision':P['revision'],'cases':records,'case_count':len(records),'passes':sum(r['all_catalog_screens_pass'] for r in records),
 'root_only_shaft_mass_kg':shaft_mass,'inertia_screen_kg_m2':Js,
 'primary_findings':['Directly carrying screw thrust through these motor bearings exceeds their running axial ratings in many cases;separate thrust-bearing load path is required.',
 '2s/5s/10s triangular200mm strokes need screw peaks6000/2400/1200rpm with2mm lead;catalog nut loads above1000rpm remain unestablished.',
 'Motor torque-speed success alone does not close nut load/lubrication,vacuum thermal,power-off holding or custody.',
 'No feeder downselect or installed hardware rating follows from a catalog-backed ground-drive sizing screen.']}
(H/'RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(len(records),'catalog-backed scenarios;',report['passes'],'pass all catalog screens;unestablished high-speed nut ratings retained')
