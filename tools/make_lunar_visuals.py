"""Render C0-S2 stored evidence and concept line drawings. Adityavardhan Mishra."""
from pathlib import Path
import json, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Rectangle,FancyArrowPatch
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/assets/lunar'
D=json.loads((ROOT/'analysis/results/lunar_visual_design.json').read_text());R=D['assumptions']['moon_radius_km']
BG='#101e2b';FG='#e5eef3';TEAL='#33d6b2';ORANGE='#f1ae52';BLUE='#6facdf';RED='#f08078'
plt.rcParams.update({'figure.facecolor':BG,'axes.facecolor':BG,'savefig.facecolor':BG,'text.color':FG,'axes.labelcolor':FG,'xtick.color':FG,'ytick.color':FG,'axes.edgecolor':'#698090','font.family':'DejaVu Sans','font.size':11,'grid.color':'#304452','svg.fonttype':'none'})
def finish(fig,name,note):
    fig.text(.04,.025,note,color='#b7c7d1',fontsize=9);fig.savefig(OUT/(name+'.png'),dpi=160);fig.savefig(OUT/(name+'.svg'));plt.close(fig)
def curve(el):
    t=np.linspace(0,2*np.pi,721);p=el['a_km']*(1-el['e']**2);rad=p/(1+el['e']*np.cos(t));w=el['omega_rad'];return rad*np.cos(t+w),rad*np.sin(t+w)
# True-scale orbit overview with separate trim-change plot.
fig,axs=plt.subplots(1,3,figsize=(15,5));fig.subplots_adjust(bottom=.2,top=.79,wspace=.36)
fig.suptitle('One release changes the orbit. It does not maintain it.',fontsize=21,x=.04,ha='left')
for ax,ha in zip(axs,[100,1000,10000]):
    ax.add_patch(Circle((0,0),R,color='#70818c',alpha=.55))
    for u,color,style in [(0,BLUE,'-'),(2,ORANGE,'--'),(-2,TEAL,':')]:
        c=next(c for c in D['releases'] if c['staging_apo_km']==ha and c['apsis']=='perilune' and c['u_ms']==u)
        x,y=curve(c['payload']);ax.plot(x,y,color=color,ls=style,lw=1.8,label=f'{u:+g} m/s')
    ax.set_aspect('equal');ax.set_title(f'100 × {ha:,} km staging',fontsize=12);ax.set_xlabel('Moon-centered X (km)');ax.set_ylabel('Y (km)');ax.grid(alpha=.4);ax.legend(fontsize=8,loc='upper right')
finish(fig,'lunar_orbits','C0-S2 · True spatial scale; small release differences overlap. Two-body osculating orbits, not lifetime predictions.')
fig,axs=plt.subplots(1,2,figsize=(12,5.5));fig.subplots_adjust(bottom=.2,top=.8,wspace=.28);fig.suptitle('Small release authority. Orbit-dependent consequences.',fontsize=20,x=.04,ha='left')
for ha,col in zip([100,1000,10000],[BLUE,TEAL,ORANGE]):
    for ax,apsis,key,base in [(axs[0],'perilune','apo_km',ha),(axs[1],'apolune','peri_km',100)]:
        c=[x for x in D['releases'] if x['staging_apo_km']==ha and x['apsis']==apsis]
        ax.plot([x['u_ms'] for x in c],[x['payload'][key]-base for x in c],color=col,marker='o',label=f'100 × {ha:,} km')
for ax,title in zip(axs,['Perilune release: change in apolune','Apolune release: change in perilune']):
    ax.set_title(title,fontsize=12);ax.set_xlabel('Signed relative release speed (m/s)');ax.set_ylabel('Altitude change (km)');ax.grid(alpha=.4);ax.axhline(0,color=FG,lw=.5);ax.legend(fontsize=9)
finish(fig,'release_authority','4 kg payload / 300 kg retained host · Negative direction requires carrier repointing. No surface-clearance or lifetime guarantee.')
fig,axs=plt.subplots(1,2,figsize=(12,5.8));fig.subplots_adjust(bottom=.22,top=.8,wspace=.3);fig.suptitle('The carrier pays for reaching the Moon.',fontsize=22,x=.04,ha='left')
a=(6678.137+384400)/2;e=1-6678.137/a;t=np.linspace(0,np.pi,600);rad=a*(1-e*e)/(1+e*np.cos(t));axs[0].plot(rad*np.cos(t)/1000,rad*np.sin(t)/1000,color=TEAL,lw=2)
axs[0].scatter([0,-384.4],[0,0],color=[BLUE,ORANGE],s=[90,45]);axs[0].annotate('Earth',(0,0),xytext=(-35,18),textcoords='offset points');axs[0].annotate('Moon at encounter',(-384.4,0),xytext=(0,18),textcoords='offset points');axs[0].set_aspect('equal');axs[0].set_xlabel('Earth-centered X (1,000 km)');axs[0].set_ylabel('Y (1,000 km)');axs[0].set_title(f"Ideal transfer: {D['transfer']['time_days']:.2f} days",fontsize=12);axs[0].grid(alpha=.4)
x=np.arange(3);cap=np.array([s['capture_kms']*1000 for s in D['staging']]);cir=np.array([s['circularize_kms']*1000 for s in D['staging']]);axs[1].bar(x,cap,color=TEAL,label='Capture into staging');axs[1].bar(x,cir,bottom=cap,color=ORANGE,label='Then circularize at 100 km');axs[1].set_xticks(x,['100 × 100','100 × 1,000','100 × 10,000']);axs[1].set_ylabel('Ideal impulse (m/s)');axs[1].set_xlabel('Lunar staging altitudes (km)');axs[1].set_ylim(0,max(cap+cir)*1.3);axs[1].legend(fontsize=9);axs[1].set_title(f"Earth departure separately: {D['transfer']['departure_kms']*1000:.0f} m/s",fontsize=12)
finish(fig,'carrier_transfer','Conditional coplanar patched conics · Symbols not to scale; curve axes are. No finite burn, ephemeris targeting or disposal solution.')
fig,ax=plt.subplots(figsize=(10,5.8));fig.subplots_adjust(bottom=.23,top=.78);fig.suptitle('Launch-service contribution changes the mass problem.',fontsize=19,x=.04,ha='left')
rows=[r for r in D['budgets'] if r['payload_count']==4 and r['isp_s']==320];x=np.arange(3);w=.32
ax.bar(x-w/2,[r['arrival_wet_kg'] for r in rows],w,color=TEAL,label='Launcher supplies departure: mass at arrival')
ax.bar(x+w/2,[r['leo_wet_if_self_departure_kg'] for r in rows],w,color=ORANGE,label='Carrier supplies departure: mass in LEO')
ax.set_xticks(x,['100 × 100','100 × 1,000','100 × 10,000']);ax.set_xlabel('Lunar staging altitudes (km)');ax.set_ylabel('Required wet mass (kg)');ax.legend(fontsize=9)
finish(fig,'carrier_mass','Assumed 300 kg dry carrier + four 4 kg payloads; Isp 320 s; 200 m/s reserve allowance. No tank/structure mass iteration.')
# Engineering state schematic with correct +X stroke and retained pusher.
fig,axs=plt.subplots(3,1,figsize=(12,7));fig.subplots_adjust(top=.82,bottom=.16,hspace=.65);fig.suptitle('Charge. Isolate. Release. Retain the pusher.',fontsize=22,x=.04,ha='left')
for ax,(label,px,bx) in zip(axs,[('CHARGED / charger withdrawn',0,0),('SEPARATION / 80 mm stroke',80,80),('CAUGHT / 20 mm stopping envelope',100,140)]):
    ax.add_patch(Rectangle((-190,-30),660,8,color='#718594'));ax.add_patch(Rectangle((-185,-22),10,52,color=TEAL));ax.add_patch(Rectangle((px-8,-20),8,45,color=TEAL));ax.add_patch(Rectangle((bx,0),340.5,22,color=ORANGE))
    ax.plot([-170,px-8],[-10,-10],color=TEAL,lw=3);ax.add_patch(Rectangle((80,-22),20,10,fill=False,edgecolor=RED,lw=2))
    ax.text(-180,48,label,fontsize=11);ax.set_xlim(-200,510);ax.set_ylim(-35,70);ax.set_yticks([]);ax.set_xticks([0,100,340.5]);ax.set_xticklabels(['0','100','340.5']);ax.spines[['left','right','top']].set_visible(False)
axs[-1].set_xlabel('X from initial payload aft contact plane (mm)')
finish(fig,'cell_states','MC-L2 layout: 80 mm stroke; spring shown as force element, not manufactured coil. Final payload position is illustrative; catch dynamics remain open.')
# Allocation line diagram using boxes/lines, not an orbit trajectory.
fig,ax=plt.subplots(figsize=(12,6));fig.subplots_adjust(top=.79,bottom=.13);fig.suptitle('Shared transport. Independent release. Finite-life payloads.',fontsize=20,x=.04,ha='left');ax.set(xlim=(0,12),ylim=(0,6));ax.axis('off')
boxes=[(0,3.5,3.1,1.5,'CARRIER','Transfer · capture · navigation\nAttitude · power · disposal',BLUE),(4.3,3.5,3.1,1.5,'VOLLEY BANK','Retain · charge · sense\nIsolate · release · catch',TEAL),(8.6,3.5,3.1,1.5,'PAYLOAD FLEET','No onboard thrusters\nMission · tracking · end of life',ORANGE),(4.3,.5,3.1,1.6,'RELEASE AUTHORIZATION','Orbit and clearance estimate\nCell state + pointing + reserve',TEAL)]
for x,y,w,h,title,body,col in boxes:
    ax.add_patch(Rectangle((x,y),w,h,fill=False,edgecolor=col,lw=1.6));ax.text(x+.15,y+h-.4,title,color=col,fontsize=10,weight='bold');ax.text(x+.15,y+.55,body,fontsize=10,va='center')
for p,q in [((3.1,4.25),(4.3,4.25)),((7.4,4.25),(8.6,4.25)),((5.85,2.1),(5.85,3.5)),((1.55,3.5),(4.3,1.3))]:ax.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=16,color=FG))
finish(fig,'mission_allocation','Architecture allocation, not flight wiring. Payload attitude control must respect the strict no-thruster customer definition.')
# Browser source data derived exclusively from saved evidence.
(OUT/'mission_data.js').write_text('window.VOLLEY_LUNAR='+json.dumps(D,separators=(',',':'))+';\n')
print('Six engineering figures rendered as SVG and PNG; browser data written.')
