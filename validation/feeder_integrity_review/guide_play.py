"""Rigid receiver rocking screen with finite guide overlap and radial pin clearance.
2-D Y/Z section, frictionless contacts, no elastic deformation or joint qualification.
Independent half-plane clipping + constrained search; mm/radians.
"""
from pathlib import Path
import json,math,itertools
import numpy as np
from scipy.optimize import minimize
H=Path(__file__).resolve().parent

def clip(poly,z,bottom):
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  ia=(a[1]>=z if bottom else a[1]<=z);ib=(b[1]>=z if bottom else b[1]<=z)
  if ia:out.append(a)
  if ia!=ib:
   u=(z-a[1])/(b[1]-a[1]);out.append([a[0]+u*(b[0]-a[0]),z])
 return out

def points(v,lo,hi):
 theta,dy,dz=v;c,s=math.cos(theta),math.sin(theta)
 return [[dy+y*c-z*s,dz+y*s+z*c] for y,z in [(-6,lo),(6,lo),(6,hi),(-6,hi)]]
def constraints(v,gap,lower,upper,stem_lower,stem_upper,pingap):
 p=clip(clip(points(v,stem_lower,stem_upper),lower,True),upper,False)
 if not p:return np.array([-1,-1,-1])
 return np.array([min(t[0] for t in p)+6+gap,6+gap-max(t[0] for t in p),pingap**2-v[1]**2-v[2]**2])
rows=[]
from scipy.optimize import brentq,minimize_scalar
for rev,gap,lower,upper,sl,su in [('FM03',.2,-8,8,-48,22),('FM04',.05,-40,8,-48,22)]:
 span=upper-lower;mid=(upper+lower)/2
 limit=brentq(lambda a:12/math.cos(a)+span*math.tan(a)-12-2*gap,0,.1,xtol=1e-14)
 for direction,pingap in itertools.product([-1,1],[.1,.15,.2]):
  def solution(a):
   t=math.tan(a);nn=1+t*t
   free=gap-6*(1/math.cos(a)-1)-span*abs(t)/2
   lo=max(mid*t-free,-pingap*math.sqrt(nn));hi=min(mid*t+free,pingap*math.sqrt(nn))
   assert lo<=hi+1e-10
   proj=min(max(direction*pingap,lo),hi)
   dy=proj/nn+direction*abs(t)*math.sqrt(max(0,pingap**2-proj**2/nn))/math.sqrt(nn)
   dz=(proj-dy)/t if abs(t)>1e-12 else 0.
   return [a,dy,dz]
  def excursion(v):
   a,dy,dz=v;return dy+9.5*(math.cos(a)-1)-30*math.sin(a)
  grid=np.linspace(-limit,limit,2001);values=[direction*excursion(solution(a)) for a in grid];i=int(np.argmax(values))
  candidates=[solution(grid[i]),solution(-limit),solution(limit),solution(0.)]
  if 0<i<len(grid)-1:
   opt=minimize_scalar(lambda a:-direction*excursion(solution(a)),bounds=(grid[i-1],grid[i+1]),method='bounded',options={'xatol':1e-14});candidates.append(solution(opt.x))
  v=max(candidates,key=lambda v:direction*excursion(v))
  poly=clip(clip(points(v,sl,su),lower,True),upper,False)
  residual=constraints(v,gap,lower,upper,sl,su,pingap)
  assert min(residual)>-1e-9,(rev,v,residual)
  rows.append({'revision':rev,'direction':direction,'radial_pin_clearance_mm':pingap,'guide_side_gap_mm':gap,'guide_Z_mm':[lower,upper],'theta_deg':float(v[0]*180/math.pi),'pin_center_offset_YZ_mm':v[1:],'dog_corner_Y_excursion_mm':float(excursion(v)),'guide_clearances_mm':residual[:2].tolist(),'pin_radius_residual_mm':float(pingap-math.hypot(*v[1:])),'absolute_angular_limit_deg':limit*180/math.pi,'search_grid_points':2001})
out={'method':'Finite rigid stem polygon clipped by guide overlap, unilateral wall limits and pin-centre radial disk. Exact strip width gives angular limit; analytic disk/strip extrema in pin offset, followed by2001angle stations and bounded scalar refinement. Independent polygon clipping checks final feasibility. Deterministic geometry sensitivity, not a statistically bounded tolerance distribution.','reference_corner_local_YZ_mm':[9.5,30.],'cases':rows,'boundary':'Rigid ideal slot/pin section only. Assumed pin radial gaps and exact nominal slot widths; no manufacturing stack, out-of-plane motion, flexible pin/guide/bar, preload, friction, wear, launch loading or actuator proof. FM03 originally had only16mm guide overlap. FM04 has48mm overlap. No assembled stiffness or strength pass.'}
(H/'GUIDE_PLAY.json').write_text(json.dumps(out,indent=2)+'\n')
for r in rows:print(r['revision'],r['direction'],r['radial_pin_clearance_mm'],r['theta_deg'],r['dog_corner_Y_excursion_mm'])
