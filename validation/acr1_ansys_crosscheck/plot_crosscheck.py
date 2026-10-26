"""Replot the captured native-result-derived field in a separate output directory."""
from pathlib import Path
import argparse,csv,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    rows=np.genfromtxt(ROOT/'extracted/closure_samples_h4p5.csv',delimiter=',',names=True);s=json.loads((ROOT/'ACR1_STATIC_CROSSCHECK.json').read_text())
    plt.rcParams.update({'font.size':12,'svg.fonttype':'none','pdf.fonttype':42})
    fig,axes=plt.subplots(1,2,figsize=(14,4.6),layout='constrained')
    color=axes[0].tricontourf(rows['x_mm'],rows['y_mm'],rows['closure_quadratic_mm'],levels=np.linspace(.03,.30,19),cmap='viridis')
    fig.colorbar(color,ax=axes[0],label='Paired closure (mm)');axes[0].set(xlabel='X (mm)',ylabel='Y (mm)',title='Primary h = 4.5 mm: common-XY closure',aspect='equal')
    cut=rows[np.abs(rows['y_mm']-45)<1e-5];cut=np.sort(cut,order='x_mm')
    axes[1].plot(cut['x_mm'],cut['closure_quadratic_mm'],color='#17364c',label='ANSYS native-derived field')
    axes[1].scatter([446],[s['reference_closure_mm']],color='#ad5b2c',label='CalculiX reference at (446, 45)',zorder=3)
    axes[1].set(xlabel='X (mm)',ylabel='Paired closure (mm)',title='Boundary profile at Y = 45 mm');axes[1].grid(alpha=.2);axes[1].legend(fontsize=9)
    fig.suptitle('ACR1 chassis: matched 3.01048 kN opposed-patch load')
    for ext in ['png','pdf','svg']:fig.savefig(a.output/('ACR1_ANSYS_crosscheck_regenerated.'+ext),dpi=180)
    plt.close(fig)
if __name__=='__main__':main()
