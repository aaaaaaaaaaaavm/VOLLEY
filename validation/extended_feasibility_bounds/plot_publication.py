from pathlib import Path
import json,os
def make_figure(data, output_dir):
    """Recreate the captured plot from the same calculated values."""
    os.environ.setdefault("MPLCONFIGDIR", str(output_dir / ".mpl-cache"))
    M = data["inputs"]["retained_host_kg"]
    m = data["inputs"]["payload_kg"]
    G0 = data["inputs"]["g0_m_s2"]
    alpha = M / (M + m)
    capture = data["B1_capture_and_carrier_boundary"]["capture"]
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    speeds=[10**(3*j/149) for j in range(150)]
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'svg.fonttype':'none'})
    fig,axs=plt.subplots(1,2,figsize=(7.2,2.8),layout='constrained')
    for g,color in [(3,'#0072B2'),(10,'#D55E00'),(25,'#009E73')]:axs[0].loglog(speeds,[alpha*u*u/(2*g*G0) for u in speeds],label=f'{g} g study screen',color=color)
    for length,label in [(.08,'0.08 m historical cell'),(.25,'0.25 m compact screen'),(1.3,'1.3 m Gen5 acceleration zone')]:axs[0].axhline(length,color='#777777',lw=.7,ls=':');axs[0].text(1.12,length*1.08,label,fontsize=7,color='#444444')
    axs[0].axvline(1000,color='#333333',lw=.7,ls='--');axs[0].set(xlabel='Required relative speed [m/s]',ylabel='Ideal minimum relative stroke [m]',title='Release-stroke compatibility');axs[0].legend(loc='upper left',fontsize=7.3);axs[0].grid(True,which='both',alpha=.16)
    x=range(3);cap=[c['capture_m_s'] for c in capture];circ=[c['later_circularization_m_s'] for c in capture]
    axs[1].bar(x,cap,color='#D55E00',label='Capture into staging orbit');axs[1].bar(x,circ,bottom=cap,color='#009E73',label='Later circularization at 100 km');axs[1].set_xticks(list(x),['100 × 100','100 × 1,000','100 × 10,000']);axs[1].set(xlabel='Initial lunar staging altitudes [km]',ylabel='Ideal carrier impulse [m/s]',title='Common 100 km circular lunar target');axs[1].legend(loc='upper center',fontsize=7.2);axs[1].set_ylim(0,1020);axs[1].grid(axis='y',alpha=.16)
    fig.suptitle('Analytical release-stroke and lunar capture bounds',fontsize=11)
    for ext in ['png','pdf','svg']:fig.savefig(output_dir/('feasibility_bounds.'+ext),dpi=190)
    plt.close(fig)

R=Path(__file__).resolve().parent
make_figure(json.loads((R/'NUMERICAL_BOUNDS.json').read_text()),R)
