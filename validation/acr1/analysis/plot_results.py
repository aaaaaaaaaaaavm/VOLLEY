"""Scientific figures from ACR1 numerical outputs; no rendered hardware claims."""
from pathlib import Path
import csv,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from finite_motor import make_field

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'figures';OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
    'axes.spines.right':False,'axes.labelsize':10,'legend.frameon':False,'savefig.facecolor':'white'})

def save(fig,name):
    fig.savefig(OUT/(name+'.png'),dpi=200,bbox_inches='tight')
    fig.savefig(OUT/(name+'.pdf'),bbox_inches='tight');plt.close(fig)

def force_map():
    d=json.loads((ROOT/'analysis/FINITE_MOTOR.json').read_text());rows=d['stations']
    fig,ax=plt.subplots(figsize=(7.2,3.7))
    x=[r['displacement_m']for r in rows]
    ax.plot(x,[r['active_N_per_A']for r in rows],color='#1c567a',lw=1.8,label='Active copper: volume integral')
    ax.plot(x,[r['with_return_N_per_A']for r in rows],color='#ad6837',lw=1.5,ls='--',label='Including approximate return paths')
    ax.set(xlim=(0,1.3),ylim=(0,1.6),xlabel='Carrier displacement from home (m)',ylabel='Force coefficient (N per peak phase A)')
    ax.set_xticks([0,.25,.5,.75,1,1.3]);ax.grid(axis='y',alpha=.17);ax.legend(loc='lower left',fontsize=9)
    fig.text(.12,-.03,'Analytic cuboid field; independently optimized phase. Current dynamics and thermal limits evaluated separately.',fontsize=8)
    save(fig,'finite_force_coefficient')

def field_section():
    p=json.loads((ROOT/'analysis/FINITE_MOTOR_INPUT.json').read_text());field=make_field(p)
    xs=np.linspace(-.175,.175,351);gap=np.linspace(-.006,.006,81)
    xx,yy=np.meshgrid(xs,gap);pts=np.stack([xx.ravel(),yy.ravel(),np.zeros(xx.size)],axis=1)
    by=field.getB(pts)[:,1].reshape(xx.shape)
    fig,ax=plt.subplots(figsize=(8,3))
    im=ax.pcolormesh(xx*1000,yy*1000,by,cmap='RdBu_r',vmin=-.85,vmax=.85,shading='auto',rasterized=True)
    ax.axhline(5,color='black',lw=.7,ls='--');ax.axhline(-5,color='black',lw=.7,ls='--')
    ax.axhline(3,color='#353535',lw=.65);ax.axhline(-3,color='#353535',lw=.65)
    ax.set(xlabel='Position relative to array centre (mm)',ylabel='Gap coordinate (mm)',ylim=(-6,6))
    fig.colorbar(im,ax=ax,label='Normal flux density, B (T)',pad=.025)
    fig.text(.12,-.06,'Mid-depth section. Solid lines: copper faces. Dashed lines: active insulation faces. Magnet faces at ±6 mm.',fontsize=8)
    save(fig,'magnetic_gap_section')

def feed_profile():
    with (ROOT/'analysis/FEEDER_PROFILES.csv').open()as f:rows=[r for r in csv.DictReader(f) if float(r['resistance_N'])==100]
    t=np.array([float(r['time_s']) for r in rows]);fig,axes=plt.subplots(1,3,figsize=(10,3))
    for ax,key,label in zip(axes,['position_mm','velocity_mm_s','motor_current_A'],['Travel (mm)','Speed (mm/s)','Modeled motor current (A)']):
        ax.plot(t,[float(r[key]) for r in rows],color='#1c567a',lw=1.7)
        ax.set(xlabel='Time (s)',ylabel=label,xlim=(0,40));ax.grid(alpha=.16)
        if key=='motor_current_A':ax.set_ylim(0,.6)
    fig.tight_layout();fig.text(.065,-.07,'250 mm quintic command; 100 N prescribed axial resistance. Catalog motor and declared transmission efficiencies.',fontsize=8)
    save(fig,'feeder_transfer_profile')

if __name__=='__main__':
    force_map();field_section();feed_profile()
    print('Created three source-derived PNG/PDF figure pairs.')
