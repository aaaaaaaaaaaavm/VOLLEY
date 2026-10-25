"""Regularized partial-element inductance estimate for the three series paths.

The balanced current combination is divergence free because the modeled paths
share ideal source/star endpoints. Lead centre paths follow the allocated routing;
they are estimates until detailed harness geometry is released. This is not a
volumetric magnetostatic FEM or an AC-loss calculation.
"""
from pathlib import Path
import hashlib,json,math
import numpy as np

ROOT=Path(__file__).resolve().parents[1]

def paths(p):
    m=p['magnetic'];out=[]
    for phase,offset,gap in [('A',0,-.0035),('B',2,.0035),('C',1,0)]:
        ix=list(range(offset,m['stator_belts'],3));nodes=[];sections=[]
        def append(q,area):
            if nodes and np.linalg.norm(np.array(q)-nodes[-1])<1e-12:return
            if nodes:sections.append(area)
            nodes.append(np.array(q,float))
        first=(m['stator_x_start']+8*ix[0]+3.5)/1000
        sign=-1 if phase=='C' else 1
        startdepth=-sign*.045;route=-.075 if startdepth<0 else .115
        for q in [(.15,0,.14),(.15,gap,.14),(.15,gap,route),
                  (first,gap,route),(first,gap,startdepth),(first,0,startdepth)]:append(q,21e-6)
        for j,i in enumerate(ix):
            s=sign*(1 if j%2==0 else -1);x=(m['stator_x_start']+8*i+3.5)/1000
            append((x,0,s*.045),42e-6)
            if j==len(ix)-1:break
            xn=(m['stator_x_start']+8*ix[j+1]+3.5)/1000
            for q in [(x,0,s*.0525),(x,gap,s*.0525),(x,gap,s*.0675),
                      (xn,gap,s*.0675),(xn,gap,s*.0525),(xn,0,s*.0525),(xn,0,s*.045)]:append(q,21e-6)
        end=nodes[-1];route=-.075 if end[2]<0 else .115
        for q in [(end[0],gap,end[2]),(end[0],gap,route),(2.23,gap,route),
                  (2.23,gap,.14),(2.23,0,.14)]:append(q,21e-6)
        out.append((phase,nodes,sections))
    return out

def discretize(nodes,areas,step):
    x=[];dl=[];r=[]
    for a,b,area in zip(nodes,nodes[1:],areas):
        n=max(1,math.ceil(np.linalg.norm(b-a)/step));d=(b-a)/n
        for j in range(n):x.append(a+(j+.5)*d);dl.append(d);r.append(.7788*math.sqrt(area/math.pi))
    return np.array(x),np.array(dl),np.array(r)

def inductance(curves,step,rscale=1):
    panels=[discretize(n,a,step) for _,n,a in curves];L=np.zeros((3,3))
    for i,(x,dl,r) in enumerate(panels):
        for j in range(i,3):
            y,dq,s=panels[j];value=0.
            for k in range(0,len(x),160):
                distance=np.sum((x[k:k+160,None,:]-y[None,:,:])**2,axis=2)
                smoothing=rscale*rscale*(r[k:k+160,None]**2+s[None,:]**2)/2
                value+=float(np.sum((dl[k:k+160]@dq.T)/np.sqrt(distance+smoothing)))
            if i==j:
                ell=np.linalg.norm(dl,axis=1);rr=r*rscale
                exact=2*(ell*np.arcsinh(ell/rr)-np.sqrt(ell*ell+rr*rr)+rr)
                value+=float(np.sum(exact-ell*ell/rr))
            L[i,j]=L[j,i]=1e-7*value
    # Columns are orthonormal and span i_A+i_B+i_C=0.
    Q=np.array([[1/math.sqrt(2),1/math.sqrt(6)],[-1/math.sqrt(2),1/math.sqrt(6)],[0,-2/math.sqrt(6)]])
    balanced=Q.T@L@Q;ev=np.linalg.eigvalsh(balanced);assert ev[0]>0
    return dict(panel_step_m=step,radius_scale=rscale,panels=[len(t[0])for t in panels],
        partial_L_matrix_H=L.tolist(),balanced_effective_inductance_eigenvalues_H=ev.tolist())

def main():
    raw=(ROOT/'cad/PARAMETERS.json').read_bytes();p=json.loads(raw);curves=paths(p)
    cases=[inductance(curves,.01),inductance(curves,.005),inductance(curves,.005,.7)]
    result=dict(configuration_id=p['configuration_id'],CAD_parameter_sha256=hashlib.sha256(raw).hexdigest(),
        model_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),phase_order=['A','B','C'],cases=cases,
        convention='Balanced three-phase effective differential inductance; same peak-phase convention as force model',
        path_lengths_m={ph:sum(np.linalg.norm(b-a)for a,b in zip(n,n[1:]))for ph,n,_ in curves},
        uncertainty='Numerical refinement and radius sensitivity do not establish harness geometry, permeance or AC-loss accuracy.',
        limitations=['Ideal shared source/star endpoints for balanced-current field energy',
            'Estimated lead routing and21mm2 lead section, not a detailed harness CAD release',
            'Rectangular conductors represented by regularized current centrelines',
            'No skin/proximity, phase-imbalance, conductive-support eddies or permeability feedback'])
    (ROOT/'analysis/WINDING_INDUCTANCE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(cases))

if __name__=='__main__':main()
