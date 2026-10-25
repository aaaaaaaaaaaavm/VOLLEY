"""Instrumented numerical audit of the production averaged shot model.

This checks implementation invariants and timestep sensitivity, not independent
electromagnetic physics or transistor switching. No analysis outputs are edited.
"""
from pathlib import Path
import hashlib, importlib.util, inspect, json, math, sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'analysis/coupled_shot.py'
source_bytes=source.read_bytes()
source_hash=hashlib.sha256(source_bytes).hexdigest()
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('coupled_shot_review_target',source)
model=importlib.util.module_from_spec(spec);spec.loader.exec_module(model)
code=inspect.getsource(model.simulate)
patches={
    "n=0\n": "n=0\n    audit=dict(max_cap_V=vc,max_terminal_V=vc,min_terminal_V=vc,max_power_budget_ratio=0.,max_regen_budget_ratio=0.,max_modulation_ratio=0.,limited_steps=0,regen_limited_steps=0,infeasible_zero_voltage_steps=0)\n",
    "if requested_power>budget or requested_power<minimum_dc_power:\n": "if requested_power>budget or requested_power<minimum_dc_power:\n            audit['limited_steps']+=1\n            audit['regen_limited_steps']+=int(requested_power<minimum_dc_power)\n            audit['infeasible_zero_voltage_steps']+=int(not minimum_dc_power<=source_power(0)<=budget)\n",
    "last_bank=ibank\n": "last_bank=ibank\n        audit['max_cap_V']=max(audit['max_cap_V'],vc)\n        audit['max_terminal_V']=max(audit['max_terminal_V'],terminal)\n        audit['min_terminal_V']=min(audit['min_terminal_V'],terminal)\n        audit['max_power_budget_ratio']=max(audit['max_power_budget_ratio'],p_dc/budget)\n        regen_floor=(32*2.9)*(vc-32*2.9)/Rsrc\n        if regen_floor<0:audit['max_regen_budget_ratio']=max(audit['max_regen_budget_ratio'],p_dc/regen_floor)\n        audit['max_modulation_ratio']=max(audit['max_modulation_ratio'],math.hypot(vq,omega*L*current)/(.95*terminal/math.sqrt(3)))\n",
    "moving_sled_kg=sled,": "audit=audit,moving_sled_kg=sled,",
}
for old,new in patches.items():
    assert code.count(old)==1,(old,code.count(old))
    code=code.replace(old,new)
namespace={'np':np,'math':math};exec(compile(code,str(source)+':instrumented','exec'),namespace)
simulate=namespace['simulate']
sled,dry,xs,ks,R,hashes=model.inputs()
coupled_bytes=(ROOT/'analysis/COUPLED_SHOT.json').read_bytes()
original=json.loads(coupled_bytes)
assert source_hash==hashlib.sha256(source.read_bytes()).hexdigest()
assert original['source_sha256']==source_hash
assert original['inputs_sha256']==hashes
snapshot=ROOT/'verification/coupled_shot_snapshots'/source_hash[:16]/hashes['home'][:16]
snapshot.mkdir(parents=True,exist_ok=True)
(snapshot/'coupled_shot.py').write_bytes(source_bytes)
(snapshot/'simulate_instrumented.py').write_text(code)
for tag,p in {'home':ROOT/'cad/release/VOLLEY_G5_ACR1_home.json',
    'force':ROOT/'analysis/FINITE_MOTOR.json','brake':ROOT/'analysis/ARREST_FORCE_MAP.json',
    'resistance':ROOT/'analysis/conduction/phase_A/h2/RESULT.json'}.items():
    raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==hashes[tag]
    (snapshot/(tag+'.json')).write_bytes(raw)
(snapshot/'COUPLED_SHOT.json').write_bytes(coupled_bytes)
rows=[]
for adverse in [False,True]:
    for L in sorted(set(r['inductance_H']for r in original['cases']if r['target_m_s']==3)):
        baseline=next(r for r in original['cases'] if r['target_m_s']==3 and r['adverse']==adverse and r['inductance_H']==L)
        refined=simulate(3,sled,dry,xs,ks,R,adverse,L,dt=5e-6)
        host=refined['reference_rest_host_kg'];mu=(sled+4)*host/(host+sled+4);mu_brake=sled*host/(host+sled)
        release=refined['release'];mechanical_work=(.5*(mu-mu_brake)*release['relative_speed_m_s']**2+.5*mu_brake*refined['stop_velocity_m_s']**2+refined['mechanical_friction_dissipation_J'])if release else None
        rows.append(dict(adverse=adverse,inductance_H=L,production_dt_s=baseline['dt_s'],audit_dt_s=refined['dt_s'],
            baseline_status=baseline['status'],refined_status=refined['status'],refined_declared_checks_pass=refined['all_declared_checks_pass'],
            refined_checks=refined['checks'],refined_peak_cell_terminal_or_internal_V=refined.get('maximum_cell_terminal_or_internal_V'),
            stop_position_change_mm=1000*(refined['stop_position_m']-baseline['stop_position_m']),
            peak_phase_current_change_A=refined['peak_phase_current_A']-baseline['peak_phase_current_A'],
            cap_draw_change_J=refined['cap_draw_J']-baseline['cap_draw_J'],
            refined_energy_residual_J=refined['energy_residual_J'],
            independent_reduced_mass_mechanical_work_J=mechanical_work,
            independent_mechanical_work_residual_J=None if mechanical_work is None else refined['energy_ledger']['mechanical_J']-mechanical_work,
            refined_release=release,refined_electrical_brake_command=refined.get('electrical_brake_command'),
            refined_stop_position_m=refined['stop_position_m'],
            refined_peak_phase_current_A=refined['peak_phase_current_A'],
            refined_peak_device_current_A=refined['peak_device_current_A'],
            refined_audit=refined['audit']))
        print(json.dumps(rows[-1]),flush=True)
report=dict(configuration_id='VOLLEY-G5-ACR1',scope='Independent implementation review and instrumented timestep audit of six 3m/s averaged-model cases only.',
    production_source_sha256=source_hash,production_output_sha256=hashlib.sha256(coupled_bytes).hexdigest(),input_sha256=hashes,snapshot_relative_path=str(snapshot.relative_to(ROOT)),
    reviewed_sled_mass_kg=sled,reviewed_dry_CAD_mass_kg=dry,
    equations_checked=[
        'Balanced peak phase convention: Pmotor=1.5*vq*iq, F=k*iq, eq=k*v/1.5, copper=1.5*R*iq^2.',
        'Field energy=0.75*L*iq^2; aggregate triangular PWM copper contribution=R*delta_i_pp^2/4.',
        'Thevenin root Ib=2*P/(Vc+sqrt(Vc^2-4*Rs*P)); source discharge dVc/dt=-Ib/C; Pmax=Vc^2/(4*Rs).',
        '32S2P 100F cells yield6.25F;32/2*11mohm yields176mohm;0.9*0.7 capacitance and2x ESR adverse factors match reference.',
        'Host and accelerated/braking reduced masses exclude the moving sled from host;4kg payload remains attached through current reversal and is removed from arrest at zero rear reaction.',
        'Independent motor-work balance:0.5*(mu_attached-mu_sled)*v_release^2+0.5*mu_sled*v_stop^2+friction_dissipation equals signed motor work.',
        'Regeneration terminal cap obeys Pdc>=Vlimit*(Vc-Vlimit)/Rsrc with Vlimit=32*2.9V; positive source-power cap is0.8*Vc^2/(4*Rsrc).',
        'Brake current reference divides remaining relative kinetic energy by trapezoidal integral k(x)dx through1.507m;3mm reserved inside1.510m allocation.',
        'Rds hot factor,10-way current sharing,25percent imbalance, triangular ripple peak,6W gate-drive allocation and source ESR loss match declared allocations.'
    ],
    reporting_findings=[
        'Peak capacitor and terminal bank voltages must be included when evaluating the cell-voltage gate.',
        'Inductance results are sampled sensitivity cases; a partial-inductance estimate is not a complete AC model.',
        'Voltage modulation uses previous terminal voltage; instrumented actual-terminal modulation ratio quantifies the algebraic lag.',
        'Release event is detected after an integration step and spatial arrest reserve includes the resulting discretization overshoot.',
        'This review is tied to the current home capture hashes and must refresh after final mechanical mass update.'
    ],cases=rows,
    summary=dict(all_refined_cases_pass=all(r['refined_declared_checks_pass']for r in rows),
        max_absolute_stop_position_change_mm=max(abs(r['stop_position_change_mm'])for r in rows),
        max_absolute_peak_current_change_A=max(abs(r['peak_phase_current_change_A'])for r in rows),
        max_absolute_energy_residual_J=max(abs(r['refined_energy_residual_J'])for r in rows),
        max_absolute_independent_mechanical_work_residual_J=max(abs(r['independent_mechanical_work_residual_J'])for r in rows),
        max_power_budget_ratio=max(r['refined_audit']['max_power_budget_ratio']for r in rows),
        max_fraction_of_ideal_SVPWM_voltage=max(.95*r['refined_audit']['max_modulation_ratio']for r in rows),
        source_limiter_zero_voltage_feasible=not any(r['refined_audit']['infeasible_zero_voltage_steps']for r in rows)),
    limitations=['Instrumented function shares production integration equations; no independent magnetic field or switching-physics validation is implied.','No overall assembly or hardware completion conclusion.'])
assert source_bytes==source.read_bytes()and coupled_bytes==(ROOT/'analysis/COUPLED_SHOT.json').read_bytes()
assert model.inputs()[-1]==hashes
(ROOT/'verification/COUPLED_SHOT_REVIEW.json').write_text(json.dumps(report,indent=2)+'\n')
