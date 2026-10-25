"""ACR1 six-block Halbach / finite-belt Lorentz integral, in N per peak phase A.

Analytic free-space cuboid field. Current density is uniform within active copper.
The return-path centerline correction is reported separately from that volume
integral. Neither ideal phase optimization nor this field solution is a rated shot.
"""
from pathlib import Path
import hashlib, json, math, platform
import numpy as np
import magpylib as magpy

ROOT=Path(__file__).resolve().parents[1]
PARAM=ROOT/'cad/PARAMETERS.json'

def make_field(p):
    m=p['magnetic']; magnets=[]
    n=m['blocks_per_array']; pitch=m['block_pitch']/1000
    for side in [-1,1]:
        for i in range(n):
            angle=math.radians(90-side*i*60)
            magnets.append(magpy.magnet.Cuboid(
                polarization=[1.32*math.cos(angle),1.32*math.sin(angle),0],
                dimension=(pitch,m['block_thickness_z']/1000,m['block_depth_y']/1000),
                position=((i-(n-1)/2)*pitch,side*(m['array_inner_z']+m['block_thickness_z']/2)/1000,0)))
    return magpy.Collection(magnets)

def active_coefficients(field,p,displacement,order):
    m=p['magnetic'];l=p['launch'];nx,ny,nz=order
    gx,wx=np.polynomial.legendre.leggauss(nx)
    gy,wy=np.polynomial.legendre.leggauss(ny)
    gz,wz=np.polynomial.legendre.leggauss(nz)
    width=m['stator_bar_width_x']/1000
    thick=(m['active_copper_z'][1]-m['active_copper_z'][0])/1000
    depth=m['stator_active_depth_y']/1000
    centers=(m['stator_x_start']+np.arange(m['stator_belts'])*m['stator_pitch']+m['stator_bar_width_x']/2)/1000
    center=(l['home_aft_x']+sum(m['array_active_relative_x'])/2)/1000+displacement
    pts=np.empty((len(centers),nx,ny,nz,3))
    pts[...,0]=centers[:,None,None,None]+width*gx[None,:,None,None]/2-center
    pts[...,1]=thick*gy[None,None,:,None]/2
    pts[...,2]=depth*gz[None,None,None,:]/2
    by=field.getB(pts.reshape(-1,3))[:,1].reshape(len(centers),nx,ny,nz)
    # Integral dV / conductor cross-section: effective integral B dl in N/A.
    belt=np.einsum('ijkl,j,k,l->i',by,wx,wy,wz)*depth/8
    coeff=np.zeros(3)
    for i,v in enumerate(belt):
        ph,sg=((0,1),(2,-1),(1,1),(0,-1),(2,1),(1,-1))[i%6]
        coeff[ph]+=sg*v
    return coeff

def return_coefficients(field,p,displacement,order=5,cross_order=3):
    """Center-path integral with transverse averaging through rectangular sections.

    Piecewise uniform current flow at the bends is an explicit approximation;
    the final neck/joint distribution requires a conduction solution.
    """
    m=p['magnetic'];l=p['launch'];center=(l['home_aft_x']+sum(m['array_active_relative_x'])/2)/1000+displacement
    g,w=np.polynomial.legendre.leggauss(order);result=np.zeros(3)
    cg,cw=np.polynomial.legendre.leggauss(cross_order)
    for ph,offset,gap_y in [(0,0,-.0035),(2,1,0),(1,2,.0035)]:
        indices=list(range(offset,m['stator_belts'],3));samples=[];directions=[]
        for j,(i,k) in enumerate(zip(indices,indices[1:])):
            s=(1 if j%2==0 else -1)*(-1 if ph==2 else 1)
            xi=(m['stator_x_start']+i*m['stator_pitch']+3.5)/1000-center
            xk=(m['stator_x_start']+k*m['stator_pitch']+3.5)/1000-center
            path=[(xi,0,s*.045),(xi,0,s*.0525),(xi,gap_y,s*.0525),
                  (xi,gap_y,s*.0675),(xk,gap_y,s*.0675),
                  (xk,gap_y,s*.0525),(xk,0,s*.0525),(xk,0,s*.045)]
            for a,b in zip(path,path[1:]):
                a=np.array(a);b=np.array(b);dl=(b-a)/2
                if np.linalg.norm(dl)==0:continue
                axis=int(np.argmax(abs(dl)));other=[k for k in range(3) if k!=axis]
                if axis==0: widths=[.003,.007]
                elif axis==1: widths=[.007,.005]
                else: widths=[.007,.006 if a[1]==0 and b[1]==0 else .003]
                for gi,wi in zip(cg,cw):
                    for gj,wj in zip(cg,cw):
                        shift=np.zeros(3);shift[other[0]]=gi*widths[0]/2;shift[other[1]]=gj*widths[1]/2
                        samples.extend((a+b)/2+g[:,None]*dl+shift)
                        directions.extend(w[:,None]*dl*wi*wj/4)
        B=field.getB(np.array(samples))
        result[ph]=np.cross(np.array(directions),B)[:,0].sum()*-1
    return result

def amplitude(coeff):
    phases=np.array([0,-2*np.pi/3,2*np.pi/3])
    return float(abs(np.sum(coeff*np.exp(1j*phases))))

def main():
    raw_params=PARAM.read_bytes();raw_source=Path(__file__).read_bytes()
    p=json.loads(raw_params);field=make_field(p)
    (ROOT/'analysis/FINITE_MOTOR_INPUT.json').write_bytes(raw_params)
    stroke=p['launch']['powered_travel']/1000
    positions=np.linspace(0,stroke,27);rows=[]
    for x in positions:
        coeff=active_coefficients(field,p,float(x),(3,3,5))
        ret=return_coefficients(field,p,float(x))
        rows.append(dict(displacement_m=float(x),active_N_per_A=amplitude(coeff),
            with_return_N_per_A=amplitude(coeff+ret),
            active_phase_coeff_N_per_A=coeff.tolist(),return_phase_coeff_N_per_A=ret.tolist()))
        print('STATION',round(float(x),4),round(rows[-1]['active_N_per_A'],6),flush=True)
    convergence=[]
    for x in [0,.65,1.3]:
        coarse=amplitude(active_coefficients(field,p,x,(3,3,5)))
        fine=amplitude(active_coefficients(field,p,x,(5,5,9)))
        return_coarse=return_coefficients(field,p,x,5,1)
        return_fine=return_coefficients(field,p,x,7,3)
        convergence.append(dict(x_m=x,coarse_N_per_A=coarse,fine_N_per_A=fine,
            relative_change=abs(fine-coarse)/fine,
            endturn_line_coeff_N_per_A=return_coarse.tolist(),
            endturn_transverse_averaged_coeff_N_per_A=return_fine.tolist(),
            total_endturn_refined_N_per_A=amplitude(active_coefficients(field,p,x,(5,5,9))+return_fine)))
    result=dict(configuration_id=p['configuration_id'],cad_parameters_sha256=hashlib.sha256(raw_params).hexdigest(),
        model_sha256=hashlib.sha256(raw_source).hexdigest(),
        convention='Balanced three-phase peak phase current; N/A at independently optimized electrical phase',
        field_axes='Xtravel,Ygap,Zdepth; CAD Xtravel,Zgap,Ydepth',
        magnets=dict(blocks_per_array=p['magnetic']['blocks_per_array'],block_pitch_mm=8,
            wavelength_mm=48,polarization_T=1.32,top_angle_deg='90-60*i',bottom_angle_deg='90+60*i'),
        software=dict(python=platform.python_version(),numpy=np.__version__,magpylib=magpy.__version__),
        stations=rows,quadrature_convergence=convergence,
        active_work_J_per_A=float(np.trapezoid([r['active_N_per_A'] for r in rows],positions)),
        limitations=['Analytic cuboid source shares its field law with prior work; not independent FEM',
            'Return correction averages rectangular sections along a center path; corner current crowding and true joints require a conduction solution',
            'No steel-support field perturbation, mutual inductance, phase-current dynamics or temperature dependence',
            'No speed rating without same-revision mass, source, controller and braking analysis'])
    (ROOT/'analysis/FINITE_MOTOR.json').write_text(json.dumps(result,indent=2)+'\n')
    print('COMPLETE',result['active_work_J_per_A'],flush=True)

if __name__=='__main__':main()
