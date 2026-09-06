"""A2-R: rederive my velocity levers at each geometry's depth-resolved field."""
import argparse
import json
import math
from pathlib import Path
import motor_model as mm
import velocity_levers as vl
ROOT=Path(__file__).resolve().parents[1]
RESULTS=ROOT/'analysis/results'
OUTPUT=RESULTS/'velocity_levers_depth.json'
def calculate():
    geometries={}
    old=(mm.TH,mm.GAP,mm.WIND_THICK)
    try:
        for name,th,gap,wind in [('baseline',.008,.012,.010),('magnet_6mm',.006,.012,.010),('magnet_5mm',.005,.012,.010),('two_layer',.008,.022,.020)]:
            mm.TH,mm.GAP,mm.WIND_THICK=th,gap,wind
            k9=float(mm.thrust_constant(nx=240,ny=9,nz=9)[0])
            k15=float(mm.thrust_constant(nx=240,ny=9,nz=15)[0])
            difference=abs(k9/k15-1)
            geometries[name]={'magnet_thickness_m':th,'gap_m':gap,'winding_thickness_m':wind,'kt_9':k9,'kt_15':k15,'depth_relative_difference':difference,
                              'pass':math.isfinite(k9) and math.isfinite(k15) and min(k9,k15)>0 and difference<=.005}
    finally: mm.TH,mm.GAP,mm.WIND_THICK=old
    baseline=json.loads((RESULTS/'motor_results.json').read_text())['Kt_N_per_kA']/1000
    error=abs(geometries['baseline']['kt_9']/baseline-1)
    rows=vl.levers({name:r['kt_9'] for name,r in geometries.items()})
    checks={'geometry_convergence':all(x['pass'] for x in geometries.values()),'baseline_reference':error<=.001,'all_original_rows':len(rows)==len(vl.LEVERS)==10}
    return {'run':'A2-R','declaration_commit':'e0a3cf611824efe19d045cab4fc73dcdfaa7abca','evidence':'Lorentz-integral quadrature and modelled lever trade; no measured or independent 3-D thrust validation',
            'geometries':geometries,'baseline_relative_difference':error,'checks':checks,'pass':all(checks.values()),'levers':rows}
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args();result=calculate()
    if args.check:
        expected=json.loads(OUTPUT.read_text())
        def equal(a,b):
            if type(a) is bool or type(b) is bool: return a is b
            if isinstance(a,(int,float)) and isinstance(b,(int,float)):
                return math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-12)
            if isinstance(a,dict) and isinstance(b,dict):
                return a.keys()==b.keys() and all(equal(a[k],b[k]) for k in a)
            if isinstance(a,list) and isinstance(b,list):
                return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
            return a==b
        if not equal(expected,result): raise SystemExit('A2-R results do not reproduce')
    else:
        OUTPUT.write_text(json.dumps(result,indent=2)+'\n')
        if result['pass']:
            (RESULTS/'velocity_levers.json').write_text(json.dumps({'levers':result['levers'],'string_esr_mohm':[vl.STRING_ESR_LO,vl.STRING_ESR_HI]},indent=2)+'\n')
            vl.write_doc(result['levers'])
    print(json.dumps({k:v for k,v in result.items() if k!='levers'},indent=2))
if __name__=='__main__':main()
