"""Print-oriented figures from captured solver data; no synthetic orbit artwork."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

ROOT=Path(__file__).resolve().parent
COLORS=['#555555','#0072B2','#D55E00','#009E73']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.titlesize':11,'axes.labelsize':10,'legend.fontsize':9,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':False,'figure.facecolor':'white','axes.facecolor':'white','savefig.facecolor':'white','svg.fonttype':'none','svg.hashsalt':'volley-orbit-evidence','pdf.fonttype':42})

def save(fig,name,caption):
 fig.text(.02,.018,caption,fontsize=8,color='#333333',va='bottom')
 fig.subplots_adjust(left=.10,right=.97,bottom=.24,top=.89,wspace=.34)
 for kind in ('png','svg','pdf'):
  fig.savefig(ROOT/'figures'/f'{name}.{kind}',dpi=200,metadata={'Creator':'Matplotlib','Date':None} if kind=='svg' else {'Creator':'Matplotlib'})
 path=ROOT/'figures'/f'{name}.svg'
 path.write_text('\n'.join(line.rstrip()for line in path.read_text().splitlines())+'\n')
 plt.close(fig)

def main():
 data=np.genfromtxt(ROOT/'orekit_30s.csv',delimiter=',',names=True,dtype=None,encoding='utf8');d=json.loads((ROOT/'ORBIT_RESULTS.json').read_text())
 fig,axes=plt.subplots(1,2,figsize=(11,4.5))
 base=data[(data['model']=='J2')&(data['relative_speed_m_s']==0)]
 bp=np.stack([base[k]for k in ('x_m','y_m','z_m')],axis=1);bv=np.stack([base[k]for k in ('vx_m_s','vy_m_s','vz_m_s')],axis=1)
 h=np.cross(bp,bv);rad=bp/np.linalg.norm(bp,axis=1)[:,None];along=np.cross(h/np.linalg.norm(h,axis=1)[:,None],rad)
 for i,speed in enumerate((0,2.5,12.448437,16.029)):
  a=data[(data['model']=='J2')&(data['relative_speed_m_s']==speed)];p=np.stack([a[k]for k in ('x_m','y_m','z_m')],axis=1)
  label=f'{speed:g} m/s relative input';first=a['t_s']<=5700
  axes[0].plot(a['t_s'][first]/60,(np.linalg.norm(p,axis=1)[first]-6378137)/1000,color=COLORS[i],ls=[':', '--','-.','-'][i],label=label,lw=1.5)
  if speed:axes[1].plot(a['t_s']/3600,np.sum((p-bp)*along,axis=1)/1000,color=COLORS[i],ls=[':', '--','-.','-'][i],lw=1.5,label=label)
 axes[0].set(xlabel='Time since release (min)',ylabel='Geocentric altitude above 6378.137 km sphere (km)',title='a  Radial excursion over the first orbit')
 axes[1].set(xlabel='Time since release (h)',ylabel='Displacement projected onto reference T axis (km)',title='b  Difference from a no-impulse reference')
 axes[0].legend(frameon=False,fontsize=8);axes[1].axhline(0,color='.75',lw=.6)
 save(fig,'release_history','Orekit 13.1.6, fixed-axis J2; 4 kg payload and 300 kg remaining host. Inputs are prescribed, not measured speeds.\nT is the reference local along-track axis; this is not a delivery-error budget or a completed mission campaign.')
 fig,axes=plt.subplots(1,2,figsize=(11,4.5))
 for model,ax in zip(('two_body','J2'),axes):
  g=np.array([[float(x)for x in line.split()]for line in (ROOT/f'gmat_{model}.txt').read_text().splitlines()if line and line[0].isdigit()])
  names=['orekit_30s.csv','orekit_gmat_mu.csv'] if model=='two_body' else ['orekit_30s.csv']
  for j,name in enumerate(names):
   o=np.genfromtxt(ROOT/name,delimiter=',',names=True,dtype=None,encoding='utf8');o=o[(o['model']==model)&(o['relative_speed_m_s']==16.029)]
   p=np.stack([o[k]for k in ('x_m','y_m','z_m')],axis=1);v=np.stack([o[k]for k in ('vx_m_s','vy_m_s','vz_m_s')],axis=1);p+=v*(g[:,0]-o['t_s'])[:,None]
   err=np.linalg.norm(g[:,1:4]*1000-p,axis=1)
   ax.plot(g[:,0]/3600,err/(1000 if model=='J2' else 1),color=COLORS[j+1],ls='-' if j else '--',lw=1.5,label=('Same central gravity constant' if j else 'Original constants') if model=='two_body' else 'Different gravity/frame setups')
  ax.set_xlabel('Time since release (h)');ax.legend(frameon=False,loc='upper left',fontsize=8)
 axes[0].set(ylabel='Position difference (m)',title='a  Central-gravity comparison')
 axes[1].set(ylabel='Position difference (km)',title='b  J2 setup difference remains unresolved')
 save(fig,'solver_comparison','Native GMAT R2026a versus Orekit 13.1.6; identical prescribed initial Cartesian state, 16.029 m/s relative input.\nElapsed output epochs are aligned. The J2 comparison is not a matched-force validation; its residual must not be hidden.')
 hist=np.genfromtxt(ROOT/'gmat_archive_sampled.csv',delimiter=',',names=True);close=np.genfromtxt(ROOT/'gmat_close_approach.csv',delimiter=',',names=True)
 fig,axes=plt.subplots(1,2,figsize=(11,4.5))
 times=np.unique(hist['day']);spans=[]
 for t in times:
  angles=np.sort(hist['raan_deg'][hist['day']==t]%360);gaps=np.diff(np.r_[angles,angles[0]+360]);spans.append(360-max(gaps))
 axes[0].plot(times,spans,color=COLORS[1],lw=1.6);axes[0].set(xlabel='Time from 1 January 2027 (day)',ylabel='Smallest circular RAAN span (deg)',title='a  Archived twelve-orbit plane spread')
 axes[1].plot(close[close.dtype.names[0]]/3600,close['separation_m'],color=COLORS[1],lw=1.2)
 i=np.argmin(close['separation_m']);x=close[close.dtype.names[0]][i]/3600;y=close['separation_m'][i]
 axes[1].plot(x,y,'o',color=COLORS[2],ms=4);axes[1].annotate(f'Sampled minimum\n{y:.2f} m',xy=(x,y),xytext=(.05,.76),textcoords='axes fraction',arrowprops={'arrowstyle':'-','color':'.35'},fontsize=9)
 axes[1].set(xlabel='Hours after 00:00 UTC, 9 January 2027 (h)',ylabel='Satellite 11–12 separation (m)',title='b  Focused closest-approach window')
 zoom=axes[1].inset_axes([.58,.52,.37,.36])
 t=close[close.dtype.names[0]];near=np.abs(t-t[i])<=20
 zoom.plot(t[near]-t[i],close['separation_m'][near],'-o',color=COLORS[1],ms=3,lw=.8)
 zoom.plot(2.44712956,180.285836,'o',mfc='white',mec=COLORS[2],ms=4)
 zoom.set(xlabel='From sampled minimum (s)',ylabel='Distance (m)',ylim=(150,900));zoom.tick_params(labelsize=7);zoom.xaxis.label.set_size(7);zoom.yaxis.label.set_size(7)
 axes[1].ticklabel_format(useOffset=False,axis='x');axes[1].xaxis.set_major_locator(MaxNLocator(4))
 save(fig,'archived_campaign','GMAT R2026a archived R1: preloaded post-release orbits, not a coupled host campaign. The left plot is downsampled.\nThe 190.15 m sampled minimum and 180.29 m linear interpolation do not establish continuous clearance or collision probability.')
 fig,axes=plt.subplots(1,2,figsize=(11,4.5))
 cases=[c for c in d['cases'] if c['relative_speed_m_s']>0]
 labels=[f"{c['model'].replace('_',' ')}\n{c['relative_speed_m_s']:.3f}"for c in cases]
 for ax,key,title in [(axes[0],'max_refinement_position_m','a  60 s versus 30 s integration limit'),(axes[1],'max_scipy_position_difference_m','b  Independent SciPy DOP853 implementation')]:
  ax.bar(range(6),[c[key]*1e6 for c in cases],color=[COLORS[1]]*3+[COLORS[2]]*3,width=.6);ax.set_xticks(range(6),labels,fontsize=7);ax.set(ylabel='Maximum one-day position difference (µm)',title=title);ax.set_xlabel('Force model and relative release input (m/s)')
 save(fig,'numerical_checks','Same force equations and constants; eight Orekit histories including no-impulse cases. These are numerical checks.\nSmall integration residuals do not bound release dispersion, atmosphere error, host navigation error or flight performance.')
 print('Four technical figure sets generated as PNG, editable SVG and PDF')
if __name__=='__main__':main()
