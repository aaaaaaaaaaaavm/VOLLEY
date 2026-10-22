"""Numerical diagnostics: unchanged screens, endpoint and stage comparisons, impulse and work."""
from pathlib import Path
import csv,json,math
H=Path(__file__).resolve().parent
KPOS=['payload_x_m','payload_y_m','payload_z_m'];KVEL=['vx_m_s','vy_m_s','vz_m_s'];KW=['wx_rad_s','wy_rad_s','wz_rad_s'];KQ=['qw','qx','qy','qz']
def rows(p):return list(csv.DictReader(p.open()))
def qdiff(a,b):
 qa=[float(a[k]) for k in KQ];qb=[float(b[k]) for k in KQ]
 c=abs(sum(x*y for x,y in zip(qa,qb)))/math.sqrt(sum(x*x for x in qa)*sum(y*y for y in qb));return math.degrees(2*math.acos(min(1,c)))
def diff(a,b,ks,scale=1):return math.sqrt(sum((float(a[k])-float(b[k]))**2 for k in ks))*scale
def compare(ap,bp):
 a,b=rows(ap),rows(bp);am=json.loads(Path(str(ap)+'.metrics.json').read_text());bm=json.loads(Path(str(bp)+'.metrics.json').read_text())
 stages=[]
 for t in [0,1,3,5,6,7,8,9,10,11,12,12.5,14.5,16,20,26.5]:
  x=min(a,key=lambda r:abs(float(r['time_s'])-t));y=min(b,key=lambda r:abs(float(r['time_s'])-t))
  stages.append({'t_s':t,'COM_delta_mm':diff(x,y,KPOS,1000),'angle_delta_deg':qdiff(x,y),'velocity_delta_mm_s':diff(x,y,KVEL,1000),'angular_velocity_delta_rad_s':diff(x,y,KW),'a_velocity_mm_s':[1000*float(x[k]) for k in KVEL],'b_velocity_mm_s':[1000*float(y[k]) for k in KVEL]})
 impulse=[x-y for x,y in zip(am['contact_impulse_N_s'],bm['contact_impulse_N_s'])]
 return {'pair':[ap.stem,bp.stem],'stages':stages,'final_COM_target_pass':stages[-1]['COM_delta_mm']<=.05,'final_angle_target_pass':stages[-1]['angle_delta_deg']<=.05,'integrated_impulse_delta_N_s':impulse,'integrated_impulse_delta_norm_N_s':math.sqrt(sum(v*v for v in impulse)),'positive_work_relative_difference':abs(am['positive_mechanical_motor_work_J']/bm['positive_mechanical_motor_work_J']-1),'a_final_speed_mm_s':math.sqrt(sum(float(a[-1][k])**2 for k in KVEL))*1000,'b_final_speed_mm_s':math.sqrt(sum(float(b[-1][k])**2 for k in KVEL))*1000}
if __name__=='__main__':
 pairs=[('baseline/FCE12-02','baseline/FCE12-03'),('baseline/FCE12-05','baseline/FCE12-06'),('baseline/FCE12-05','baseline/FCE12-07'),('baseline/FCE12-05','runs/P3-250'),('runs/P3-250','runs/W3-250'),('runs/W3-250','runs/W3-125'),('runs/A3-250','runs/A3-125'),('runs/P3-250','runs/A3-250'),('runs/B3-250','runs/B3-125'),('runs/P3-250','runs/B3-250'),('runs/X3-250','runs/X3-125'),('runs/P3-250','runs/X3-250'),('baseline/FCE12-06','runs/X3-125')]
 result=[]
 for a,b in pairs:
  ap,bp=H/(a+'.csv'),H/(b+'.csv')
  if ap.exists() and bp.exists() and Path(str(ap)+'.metrics.json').exists() and Path(str(bp)+'.metrics.json').exists():result.append(compare(ap,bp))
 (H/'COMPARISONS.json').write_text(json.dumps({'criteria':{'COM_mm':.05,'angle_deg':.05,'work_relative':.01},'CAD':'FM06-R1 only; no FM07-R6 validity','comparisons':result},indent=2)+'\n')
 for r in result:print(r['pair'],'final_mm_deg',r['stages'][-1]['COM_delta_mm'],r['stages'][-1]['angle_delta_deg'],'vfinal_mm_s',r['a_final_speed_mm_s'],r['b_final_speed_mm_s'],'impulse_delta_Ns',r['integrated_impulse_delta_norm_N_s'],'workrel',r['positive_work_relative_difference'])
