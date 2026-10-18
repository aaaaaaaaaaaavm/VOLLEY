"""Check captured native histories and generate a standalone orbit evidence summary."""
from pathlib import Path
import argparse
import hashlib
import json
import math
import numpy as np
from scipy.integrate import solve_ivp

ROOT=Path(__file__).resolve().parent
MU=3.986004418e14; RE=6378137.; J2=1.08262668e-3


def acceleration(p,j2=False):
 r=np.linalg.norm(p);a=-MU*p/r**3
 if j2:
  q=5*(p[2]/r)**2
  a+=1.5*J2*MU*RE**2/r**5*p*np.array([q-1,q-1,q-3])
 return a


def load_orekit(name):
 return np.genfromtxt(ROOT/name,delimiter=',',names=True,dtype=None,encoding='utf8')


def load_gmat(name):
 rows=[]
 for line in (ROOT/name).read_text().splitlines():
  if line and line[0].isdigit():rows.append([float(s) for s in line.split()])
 a=np.array(rows)
 if a.shape!=(1441,9) or np.any(np.diff(a[:,0])<=0):raise ValueError('Invalid GMAT time history')
 return a


def analyze():
 coarse=load_orekit('orekit_60s.csv');fine=load_orekit('orekit_30s.csv')
 result={'orekit_version':'13.1.6','gmat_version':'R2026a','epoch':'2026-09-29 00:00:00 TAI','duration_s':86400,'output_step_s':60,'cases':[],'cross_code':[],
 'assumptions':{'initial_altitude_m':450000,'inclination_deg':51.6,'payload_kg':4,'remaining_host_kg':300,'mu_m3_s2':MU,'equatorial_radius_m':RE,'j2':J2,'speeds':'Prescribed relative separation inputs; not achieved motor ratings','force_axis':'Orekit J2 about fixed GCRF z; GMAT degree-2/order-0 uses its Earth-fixed gravity configuration'},
 'limitations':['One-day prescribed-state numerical propagation, not coupled sequential host deployment','No drag, SRP, third bodies, actual release error, conjunction probability or validated atmospheric lifetime','J2 configurations differ in pole/frame treatment and gravity constants; residual is a model/configuration difference, not an isolated integrator error','Thresholds were not preregistered before exploratory runs; report observed residuals, not a qualification pass']}
 for model in ('two_body','J2'):
  for speed in (0.,2.5,12.448437,16.029):
   mask=(fine['model']==model)&(fine['relative_speed_m_s']==speed)
   f=fine[mask];c=coarse[mask]
   pos=np.stack([f[k] for k in ('x_m','y_m','z_m')],axis=1)
   vel=np.stack([f[k] for k in ('vx_m_s','vy_m_s','vz_m_s')],axis=1)
   old=np.stack([c[k] for k in ('x_m','y_m','z_m')],axis=1)
   y0=np.r_[pos[0],vel[0]]
   def rhs(t,y):return np.r_[y[3:],acceleration(y[:3],model=='J2')]
   sol=solve_ivp(rhs,(0,86400),y0,method='DOP853',t_eval=f['t_s'],rtol=1e-12,atol=1e-7,max_step=30)
   if not sol.success:raise ValueError(sol.message)
   error=np.linalg.norm(sol.y[:3].T-pos,axis=1)
   r=np.linalg.norm(pos,axis=1);energy=.5*np.sum(vel**2,axis=1)-MU/r
   if model=='J2':energy+=MU*J2*RE**2/r**3*.5*(3*(pos[:,2]/r)**2-1)
   hz=np.cross(pos,vel)[:,2]
   result['cases'].append({'model':model,'relative_speed_m_s':speed,'payload_inertial_dv_m_s':300/304*speed,'max_refinement_position_m':float(np.linalg.norm(old-pos,axis=1).max()),'max_scipy_position_difference_m':float(error.max()),'max_relative_energy_drift':float(np.max(np.abs((energy-energy[0])/energy[0]))),'max_relative_hz_drift':float(np.max(np.abs((hz-hz[0])/hz[0]))),'initial_semimajor_axis_m':float(f['a_m'][0]),'initial_eccentricity':float(f['e'][0])})
  g=load_gmat('gmat_'+model+'.txt');f=fine[(fine['model']==model)&(fine['relative_speed_m_s']==16.029)]
  p=np.stack([f[k] for k in ('x_m','y_m','z_m')],axis=1);v=np.stack([f[k] for k in ('vx_m_s','vy_m_s','vz_m_s')],axis=1)
  # GMAT accumulated stop times differ slightly from the ideal 60-second grid.
  # First-order epoch alignment is accurate to < micrometre at these offsets.
  dt=g[:,0]-f['t_s'];aligned=p+v*dt[:,None]
  diff=np.linalg.norm(g[:,1:4]*1000-aligned,axis=1)
  result['cross_code'].append({'model':model,'max_position_difference_m':float(diff.max()),'terminal_position_difference_m':float(diff[-1]),'max_epoch_alignment_s':float(np.abs(dt).max()),'same_force_configuration':False,'note':'Central gravitational constants differ slightly (GMAT 398600.4415 vs Orekit 398600.4418 km^3/s^2).' if model=='two_body' else 'Different Earth pole/gravity definitions; do not interpret as matched-force numerical validation.'})
 g=load_gmat('gmat_two_body.txt');n=load_orekit('orekit_gmat_mu.csv')
 p=np.stack([n[k] for k in ('x_m','y_m','z_m')],axis=1);v=np.stack([n[k] for k in ('vx_m_s','vy_m_s','vz_m_s')],axis=1)
 aligned=p+v*(g[:,0]-n['t_s'])[:,None];difference=np.linalg.norm(g[:,1:4]*1000-aligned,axis=1)
 result['matched_central_gravity']={'mu_m3_s2':398600441500000.,'max_position_difference_m':float(difference.max()),'terminal_position_difference_m':float(difference[-1]),'force_boundary':'Identical central gravity constant and numerical initial Cartesian state; output epochs aligned','not_established':'J2 frame harmonization, atmospheric lifetime, coupled host dynamics, hardware accuracy'}
 result['source_hashes']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'OrbitEvidence.java',ROOT/'orekit_60s.csv',ROOT/'orekit_30s.csv',ROOT/'gmat_two_body.txt',ROOT/'gmat_J2.txt',ROOT/'orekit_gmat_mu.csv']}
 return result


def main():
 parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args();d=analyze();body=json.dumps(d,indent=2,sort_keys=True)+'\n';path=ROOT/'ORBIT_RESULTS.json'
 if args.check:
  if json.loads(path.read_text())!=d:raise SystemExit('Captured orbit evidence changed; regenerate and review')
  print('PASS: eight native Orekit cases, two GMAT histories, convergence and conservation recomputed')
 else:path.write_text(body);print(json.dumps(d['cross_code'],indent=2))
if __name__=='__main__':main()
