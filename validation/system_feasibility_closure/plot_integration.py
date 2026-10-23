"""Generate source-linked capacity and conditional mission figures."""
from pathlib import Path
import json,math,sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

H=Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.titlesize':10,
    'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':220,'svg.fonttype':'none'})
C=['#17628a','#c06a2c']

def save(fig,name):
    for ext in (('svg',) if '--svg-only' in sys.argv else ('png','svg','pdf')):fig.savefig(H/'figures'/f'{name}.{ext}',bbox_inches='tight')
    plt.close(fig)

def main():
    m=json.loads((H/'MISSION_RETARGET_SUMMARY.json').read_text())
    fig,axes=plt.subplots(1,2,figsize=(7.2,3.2),layout='constrained')
    for ax,n in zip(axes,(4,12)):
        v=[r for r in m['cases'] if r['count']==n and r['architecture']=='volley']
        ax.plot([r['allowance_kg'] for r in v],[r['fuel_used_kg'] for r in v],'-o',color=C[0],ms=4,label='Selected-feeder study')
        s=m['best_known_feasible_spring'][str(n)]
        if s:ax.axhline(s['fuel_used_kg'],ls='--',lw=1.2,color=C[1],label=f'Spring: best tested feasible f={s["fraction"]:g}')
        ax.set(xlabel='Assumed omitted-equipment allowance [kg]',ylabel='Host propellant used [kg]',title=f'{n} mixed-size releases')
        ax.set_xticks([10,25,50]);ax.grid(axis='y',alpha=.18);ax.legend(frameon=False,fontsize=7,loc='best')
    save(fig,'mission_mass_sensitivity')
    if (H/'NATIVE_REPLAY_CHECKS.json').exists():
        n=json.loads((H/'NATIVE_REPLAY_CHECKS.json').read_text())
        labels=['Force ±0.1%','Release speed ±0.1%','Initial X ±10 m','3U mass 4→6 kg']
        probes=['force_','shot_','initial_x_','payload3U6kg_']
        fig,ax=plt.subplots(figsize=(7.2,3.3),layout='constrained')
        for i,count in enumerate((4,12)):
            vals=[]
            for probe in probes:
                subset=[r for r in n['native_runs'] if r['category']=='sensitivity' and r['name'].startswith(str(count)+'_volley') and probe in r['name']]
                vals.append(max(r['max_payload_target_position_error_m'] for r in subset)/1000)
            ax.bar([x+(-.18 if i==0 else .18) for x in range(4)],vals,width=.34,color=C[i],label=f'{count} releases')
        ax.set(yscale='log',ylabel='Largest payload terminal position miss [km]',title='Frozen-command deterministic sensitivities; no feedback')
        ax.set_xticks(range(4),labels,fontsize=8);ax.grid(axis='y',alpha=.18);ax.legend(frameon=False)
        save(fig,'native_mission_sensitivity')
    a=json.loads((H/'TWELVE_ASSEMBLY_REPORT.json').read_text())
    bounds=a['captures'][0]['component_bounds_mm']
    fig,ax=plt.subplots(figsize=(7.2,2.5),layout='constrained')
    for name,b in bounds.items():
        if name.startswith('Common__Profile_rail_'):
            ax.add_patch(Rectangle((b[0]/1000,b[2]/1000),(b[1]-b[0])/1000,(b[3]-b[2])/1000,color='#444444'))
        if '__Payload_' in name:
            one=name.endswith('1U');color=C[0] if one else C[1]
            ax.add_patch(Rectangle((b[0]/1000,b[2]/1000),(b[1]-b[0])/1000,(b[3]-b[2])/1000,facecolor=color,edgecolor=color,alpha=.85))
            ax.text((b[0]+b[1])/2000,(b[2]+b[3])/2000,'1U' if one else '3U',ha='center',va='center',fontsize=7,color='white')
    for i,x in enumerate(a['stations_X_mm']):
        ax.plot([x/1000,x/1000],[.01,.09],color='#888888',lw=.8)
        ax.text(x/1000,-.29,str(i+1),ha='center',va='top',fontsize=7,color='#444444')
    ax.set(xlim=(-.17,4.07),ylim=(-.35,.40),xlabel='Launch/index axis X [m]',ylabel='Feed axis Y [m]',title='Twelve-cell capacity: stored payloads and shared rail (CAD-derived plan)')
    ax.set_aspect('equal',adjustable='box');ax.spines[['top','right']].set_visible(False)
    save(fig,'twelve_capacity_plan')

if __name__=='__main__':main()
