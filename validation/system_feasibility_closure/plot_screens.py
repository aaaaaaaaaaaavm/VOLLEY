"""Source-linked scientific figures; no synthesized application interfaces."""
from pathlib import Path
import json,sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

H=Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.titlesize':10,
 'axes.labelsize':9,'xtick.labelsize':8,'ytick.labelsize':8,'legend.fontsize':8,
 'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':220,'svg.fonttype':'none'})
colors=['#17628a','#c06a2c','#575757']

def save(fig,name):
    for ext in (('svg',) if '--svg-only' in sys.argv else ('png','svg','pdf')):fig.savefig(H/'figures'/f'{name}.{ext}',bbox_inches='tight')
    plt.close(fig)

def main():
    s=json.loads((H/'SYSTEM_SCREENS.json').read_text())
    n=json.loads((H/'LUNAR_NAVIGATION_SENSITIVITY.json').read_text())
    fig,ax=plt.subplots(1,2,figsize=(7.2,3.0),layout='constrained')
    for eta,c in zip((.25,.5,.75),colors):
        v=[r for r in s['energy_cases'] if r['payload_count']==12 and r['payload_kg_each']==4 and r['assumed_net_efficiency']==eta and r['assumed_charging_W']==50]
        ax[0].plot([r['relative_speed_m_s'] for r in v],[r['charge_time_lower_bound_s']/60 for r in v],'-o',ms=3,color=c,label=f'Assumed efficiency {eta:.0%}')
    ax[0].set(xscale='log',yscale='log',xlabel='Relative release speed [m/s]',ylabel='Charging-time lower bound [min]',title='(a) Twelve independent 4 kg shots; 50 W')
    ax[0].set_xticks([3,6,1000],[3,6,1000]);ax[0].legend(loc='upper left',frameon=False)
    rows=[r for r in s['stroke_cases'] if r['payload_kg']==4 and r['relative_stroke_m']==1.3]
    ax[1].plot([r['relative_speed_m_s'] for r in rows],[r['constant_force_payload_acceleration_g'] for r in rows],'-o',ms=3,color=colors[0])
    ax[1].axhline(25,color=colors[1],ls='--',lw=1,label='25 g study screen')
    ax[1].set(xscale='log',yscale='log',xlabel='Relative release speed [m/s]',ylabel='Minimum peak payload acceleration [g]',title='(b) 1.3 m constant-force stroke; 4 kg')
    ax[1].set_xticks([3,6,1000],[3,6,1000]);ax[1].legend(frameon=False,loc='upper left')
    for a in ax:a.grid(axis='y',alpha=.18)
    save(fig,'resource_requirements')
    fig,ax=plt.subplots(figsize=(7.2,4.0))
    for band,c,label in zip(('tight_study_band','middle_study_band','wide_study_band'),colors,('10 m / 0.01 m/s / 0.01° / 0.1%','100 m / 0.1 m/s / 0.1° / 1%','1 km / 1 m/s / 1° / 5%')):
        rows=[r for r in n['cases'] if r['assumed_band']['name']==band]
        ax.plot([r['staging_apoapsis_km'] for r in rows],[r['finite_sample'][-1]['std_periapsis_altitude_m']/1000 for r in rows],'-o',color=c,ms=4,label=label)
    ax.set(xscale='log',yscale='log',xlabel='Host staging apoapsis altitude [km]',ylabel='Payload periapsis standard deviation [km]',title='Assumed lunar release uncertainty bands; two-body osculating orbit')
    ax.set_xticks([100,1000,10000],[100,1000,10000]);ax.grid(axis='y',alpha=.18)
    fig.legend(*ax.get_legend_handles_labels(),title='Assumed 1σ position / velocity / pointing / relative speed',frameon=False,
        loc='lower center',bbox_to_anchor=(.53,.005),ncol=1,columnspacing=1.2,handlelength=2.)
    fig.subplots_adjust(left=.10,right=.99,top=.89,bottom=.36)
    save(fig,'lunar_navigation_sensitivity')

if __name__=='__main__':main()
