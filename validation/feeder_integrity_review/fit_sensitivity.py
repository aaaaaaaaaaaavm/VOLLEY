"""FM04 deterministic fit sensitivities. No invented manufacturing capability."""
from pathlib import Path
import json,math,itertools
H=Path(__file__).resolve().parent;out=[]
for tol_slot,tol_bar,angle,Tg,Tb,elastic_loss in itertools.product([.02,.05,.1],[.02,.05,.1],[0,.025,.05,.1,.25],[-100,0,100],[-100,0,100],[0,.02,.05]):
 slot=(12.1-tol_slot)*(1+23e-6*Tg);bar=(12+tol_bar)*(1+12e-6*Tb);a=math.radians(angle)
 residual=slot-bar/math.cos(a)-48*abs(math.tan(a))-2*elastic_loss
 out.append({'slot_width_minus_tolerance_mm':tol_slot,'bar_width_plus_tolerance_mm':tol_bar,'fixed_relative_angle_deg':angle,'guide_temperature_change_K':Tg,'bar_temperature_change_K':Tb,'extra_loss_each_side_mm':elastic_loss,'total_width_residual_mm':residual,'positive_parametric_fit':residual>0})
r={'revision':'FIT02','nominal':{'bar_width_mm':12,'guide_width_mm':12.1,'guide_length_mm':48},'cases':out,'boundary':'Deterministic worst-direction geometry sensitivities, not probability or pass rate for hardware. Manufacturing widths, independent guide/bar temperatures, assumed aluminium/steel CTE23/12ppm/K and elastic-loss bands are unverified inputs. The fixed relative angle is a conservative imposed alignment condition; actual two-guide/pin accommodation and deformation are not solved. No tolerance drawing, process capability or thermal qualification follows.'}
(H/'FIT_SENSITIVITY.json').write_text(json.dumps(r,indent=2)+'\n');print(len(out),'deterministic combinations;',sum(not t['positive_parametric_fit'] for t in out),'nonpositive, retained')
