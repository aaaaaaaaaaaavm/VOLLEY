#!/usr/bin/env python3
"""Verify SD01 native evidence, source preservation and stated conditional decisions."""
from pathlib import Path
import ast,hashlib,json,subprocess,sys
import numpy as np
from scipy.linalg import expm
H=Path(__file__).resolve().parent;R=H.parents[1]
def load(name):return json.loads((H/name).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 manifest=load('MANIFEST.json')
 for name,item in manifest['files'].items():
  p=(H/name).resolve();assert p.is_relative_to(H)and p.is_file(),name
  assert p.stat().st_size==item['bytes']and sha(p)==item['sha256'],f'Changed current SD01 capture: {name}'
 m=load('MODAL_RESULTS.json');i=load('MODAL_INPUT.json');d=load('RESPONSE_RESULTS.json');n=load('CURRENT_NORMAL_FORCE.json');c=load('PHYSICS_LIMIT_COMPARISON.json');b=np.load(H/'MODAL_BASIS.npz')
 assert i['native_nodes']==112519 and i['C3D10_elements']==62198 and i['accepted_static_hotspot_node']==2411
 deck=(H/'runs/free_free/modal.inp').read_text();assert '*BOUNDARY'not in deck and '*DENSITY\n2.7e-9\n'in deck and '*FREQUENCY\n46\n'in deck
 assert 'Job finished'in(H/'runs/free_free/SOLVER_STDOUT.txt').read_text()
 assert len(m['rigid_modes'])==6 and len(m['elastic_frequencies_Hz'])==40
 assert abs(m['elastic_frequencies_Hz'][0]-131.4105)<1e-4 and abs(m['elastic_frequencies_Hz'][-1]-2052.744)<.001
 assert m['stress_monitor_points']==148 and m['C3D10_stress_recovery_max_relative_component_error']<.005
 assert len(d['finite_cases'])==54 and all(q['positive_conditional_budget']for q in d['finite_cases'])
 assert min(q['steady_5pct_remaining_paired_budget_mm']for q in d['harmonic_design_limits'])<0,'Adverse sustained-harmonic result must remain visible'
 assert .28<c['fine_step_finite_paired_margin_mm']<.29 and 64<c['minimum_continuous_harmonic_normal_limit_N']<65
 assert len(n['records'])==7 and n['current_envelope_cases']==18 and c['frozen_scalar_X_reproduction_absolute_error_N_per_A']<1e-10
 assert c['representative_ideal_phase_max_absolute_normal_N']<c['minimum_continuous_harmonic_normal_limit_N']
 assert c['representative_5deg_phase_error_normal_N']<c['minimum_continuous_harmonic_normal_limit_N']<c['representative_15deg_phase_error_normal_N']
 assert c['FE_vs_refined_uniform_normal_relative_difference']<.001
 for name,expected in d['source_identities'].items():assert sha(R/name)==expected,f'Source changed: {name}'
 for name,expected in n['source_identities'].items():assert sha(R/name)==expected,f'Current/PM source changed: {name}'
 for name,expected in m['source_identities'].items():
  if name.startswith('modal.')or name=='SOLVER_STDOUT.txt':assert sha(H/'runs/free_free'/name)==expected,name
 figure=load('FIGURE_MANIFEST.json')
 for name,expected in figure['sources'].items():assert sha(H/name)==expected,name
 for row in figure['figures']:
  for name,expected in row['exports'].items():assert sha(H/name)==expected,name
 # Independent exact SDOF step-load solution checks the modal time integrator without rerunning the study.
 tree=ast.parse((H/'respond.py').read_text());fn=next(v for v in tree.body if isinstance(v,ast.FunctionDef)and v.name=='integrate');ns={'np':np,'expm':expm};exec(compile(ast.Module(body=[fn],type_ignores=[]),'integrator_check','exec'),ns)
 omega=2*np.pi*30.;zeta=.02;dt=.0005;t=np.arange(0,1+dt/2,dt);F=5.;q=ns['integrate'](np.array([omega]),zeta,np.full((1,len(t)),F),dt)[0];wd=omega*np.sqrt(1-zeta*zeta);exact=F/omega**2*(1-np.exp(-zeta*omega*t)*(np.cos(wd*t)+zeta*omega/wd*np.sin(wd*t)));assert np.max(np.abs(q-exact))<1e-11
 assert b['stress_modes'].shape==(148,40,6)and b['D_paired'].shape[1]==40
 text=subprocess.check_output(['pdftotext',str(H/'STRUCTURAL_DYNAMICS_REPORT.pdf'),'-'],text=True);assert '64.687'in text and '148 integration points'in text and '3kN oscillatory'not in text
 print(f'PASS: SD01 {len(manifest["files"])} file identities; native40 elastic+6rigid modes;148 stress monitors;54 finite cases and retained adverse harmonic;7 source-normal representatives; exact SDOF integration check; source physics preserved')
if __name__=='__main__':main()
