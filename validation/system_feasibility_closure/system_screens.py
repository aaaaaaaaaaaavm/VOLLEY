"""Conservation-based resource screens for the selected feeder programme.

All efficiencies, charging powers and host inertias are sensitivity inputs.
These calculations establish requirements; they do not establish achievable
motor speed, efficiency, thermal control or host compatibility.
"""
from pathlib import Path
import hashlib, json, math
from itertools import product

H=Path(__file__).resolve().parent
G0=9.80665
SIGMA=5.670374419e-8


def compute():
    energy=[]
    for n,mass,u,eta,power in product((4,12),(1.33,4.),(3.,6.,1000.),(.25,.5,.75),(25.,50.,100.)):
        M=300.
        alpha=M/(M+mass)
        E=.5*mass*alpha*u*u
        bus=n*E/eta
        energy.append(dict(payload_count=n,payload_kg_each=mass,relative_speed_m_s=u,
            retained_host_kg=M,assumed_net_efficiency=eta,assumed_charging_W=power,
            ideal_relative_energy_per_shot_J=E,bus_energy_lower_bound_J=bus,
            waste_heat_lower_bound_J=bus-n*E,charge_time_lower_bound_s=bus/power,
            source_and_catcher_losses_excluded=True))
    stroke=[]
    for m,u,s in product((1.33,4.),(3.,6.,1000.),(.08,.25,1.3)):
        alpha=300./(300.+m)
        stroke.append(dict(payload_kg=m,relative_speed_m_s=u,relative_stroke_m=s,
            constant_force_payload_acceleration_g=alpha*u*u/(2*s*G0),
            constant_force_payload_force_N=m*alpha*u*u/(2*s),
            peak_acceleration_is_lower_bound=True))
    torque=[]
    for m,u,b,I in product((1.33,4.),(3.,6.),(0.,.1,.5),(20.,100.,500.)):
        alpha=300./(300.+m); impulse=m*alpha*u
        torque.append(dict(payload_kg=m,relative_speed_m_s=u,
            assumed_force_axis_offset_m=b,assumed_host_inertia_kg_m2=I,
            angular_impulse_N_m_s=impulse*b,
            uncorrected_spin_increment_deg_s=impulse*b/I*180/math.pi))
    radiator=[]
    for u,eta,A,T in product((6.,1000.),(.25,.5,.75),(.25,1.,4.),(273.15,300.,323.15)):
        E=.5*4.*300./304.*u*u
        # A black deep-space sink and emissivity0.8 are explicit optimistic assumptions.
        # Solar/planet heating, conduction, views, hot/cold variation and radiator mass absent.
        Q=E*(1/eta-1)
        P=.8*SIGMA*A*T**4
        radiator.append(dict(relative_speed_m_s=u,assumed_efficiency=eta,
            assumed_radiator_area_m2=A,assumed_radiator_K=T,
            ideal_deep_space_net_radiation_W=P,
            per_shot_waste_heat_J=Q,ideal_minimum_rejection_time_s=Q/P))
    invariants={
        'zero_axis_offset_has_zero_point_mass_angular_impulse':all(x['angular_impulse_N_m_s']==0 for x in torque if x['assumed_force_axis_offset_m']==0),
        'all_bus_energy_ge_ideal_energy':all(x['bus_energy_lower_bound_J']>=x['payload_count']*x['ideal_relative_energy_per_shot_J'] for x in energy),
        'stroke_work_identity_relative_1e_minus12':all(abs(x['constant_force_payload_force_N']*x['relative_stroke_m']-.5*x['payload_kg']*300/(300+x['payload_kg'])*x['relative_speed_m_s']**2)/max(1,x['constant_force_payload_force_N']*x['relative_stroke_m'])<1e-12 for x in stroke),
        'compact_1km_s_25g_requirement_incompatible':all(x['constant_force_payload_acceleration_g']>25 for x in stroke if x['relative_speed_m_s']==1000),
    }
    assert all(invariants.values())
    return dict(study='SYS-01 selected-feeder programme resource requirements',
        evidence_class='ANALYTICAL_REQUIREMENT_AND_SENSITIVITY_SCREEN',
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        constants=dict(g0_m_s2=G0,stefan_boltzmann_W_m2_K4=SIGMA),
        assumptions=['retained host300kg is surrogate','3–6m/s are imposed study inputs, not measured or rated release capability',
        'net efficiency25/50/75percent, charging25/50/100W are assumed bands',
        'radiator emissivity0.8 and0K deep-space sink are optimistic analytic bounds',
        'payload acceleration is constant-force theoretical lower bound, not a qualified payload limit',
        'angular response is single-axis point impulse; actual host flexible/attitude behavior absent'],
        checks=invariants,energy_cases=energy,stroke_cases=stroke,host_angular_response=torque,
        optimistic_heat_rejection=radiator)


def main():
    result=compute()
    (H/'SYSTEM_SCREENS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(checks=result['checks'],counts={k:len(result[k]) for k in ('energy_cases','stroke_cases','host_angular_response','optimistic_heat_rejection')})))

if __name__=='__main__':main()
