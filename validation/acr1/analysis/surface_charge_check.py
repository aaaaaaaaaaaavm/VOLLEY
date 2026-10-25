"""Independent magnetic surface-charge quadrature for the ACR1 active force.

The calculated field does not call Magpylib. That library supplies only the
comparison field, allowing a source implementation cross-check under shared
uniform-magnetization/free-space assumptions.
"""
from pathlib import Path
import hashlib,json,math
import numpy as np
import finite_motor as reference

ROOT=Path(__file__).resolve().parents[1]

def sources(p,order):
    m=p['magnetic'];g,w=np.polynomial.legendre.leggauss(order);faces=[]
    width=m['block_pitch']/1000;thick=m['block_thickness_z']/1000;n=m['blocks_per_array']
    for side in [-1,1]:
        yc=side*(m['array_inner_z']/1000+thick/2)
        for i in range(n):
            xc=(i-(n-1)/2)*width;angle=math.radians(90-side*i*60)
            for axis,pol in [('x',1.32*math.cos(angle)),('y',1.32*math.sin(angle))]:
                if abs(pol)<1e-12:continue
                for sign in [-1,1]:
                    if axis=='x':sx=np.full(order,xc+sign*width/2);sy=yc+g*thick/2;span=thick
                    else:sx=xc+g*width/2;sy=np.full(order,yc+sign*thick/2);span=width
                    faces.append((sx,sy,sign*pol*span*w/(8*math.pi)))
    return faces

def field_by(points,faces,depth):
    result=np.zeros(len(points))
    for start in range(0,len(points),1500):
        q=points[start:start+1500];high=depth/2-q[:,2,None];low=-depth/2-q[:,2,None]
        by=np.zeros(len(q))
        for sx,sy,c in faces:
            dx=q[:,0,None]-sx;dy=q[:,1,None]-sy;rho=dx*dx+dy*dy
            assert np.min(rho)>1e-20
            integral=(high/np.sqrt(rho+high*high)-low/np.sqrt(rho+low*low))/rho
            by+=np.sum(c*dy*integral,axis=1)
        result[start:start+len(q)]=by
    return result

def force(p,faces,x,order=(3,3,5)):
    m=p['magnetic'];l=p['launch'];nx,ny,nz=order
    gx,wx=np.polynomial.legendre.leggauss(nx);gy,wy=np.polynomial.legendre.leggauss(ny);gz,wz=np.polynomial.legendre.leggauss(nz)
    width=m['stator_bar_width_x']/1000;thick=.006;depth=m['stator_active_depth_y']/1000
    centers=(m['stator_x_start']+np.arange(m['stator_belts'])*m['stator_pitch']+m['stator_bar_width_x']/2)/1000
    centre=(l['home_aft_x']+sum(m['array_active_relative_x'])/2)/1000+x
    pts=np.empty((len(centers),nx,ny,nz,3))
    pts[...,0]=centers[:,None,None,None]+width*gx[None,:,None,None]/2-centre
    pts[...,1]=thick*gy[None,None,:,None]/2;pts[...,2]=depth*gz[None,None,None,:]/2
    by=field_by(pts.reshape(-1,3),faces,depth).reshape(len(centers),nx,ny,nz)
    integral=np.einsum('ijkl,j,k,l->i',by,wx,wy,wz)*depth/8
    phase=np.array([0,-2*np.pi/3,2*np.pi/3]);coefficient=0j
    for i,value in enumerate(integral):
        ph,sg=((0,1),(2,-1),(1,1),(0,-1),(2,1),(1,-1))[i%6]
        coefficient+=sg*value*np.exp(1j*phase[ph])
    return abs(coefficient)

def main():
    raw=(ROOT/'cad/PARAMETERS.json').read_bytes();p=json.loads(raw);analytic=reference.make_field(p);rows=[]
    for order in [10,16]:
        faces=sources(p,order)
        for x in [0,.65,1.3,1.51]:
            calculated=float(force(p,faces,x));baseline=reference.amplitude(reference.active_coefficients(analytic,p,x,(3,3,5)))
            rows.append(dict(face_order=order,x_m=x,surface_charge_N_per_A=calculated,
                analytic_cuboid_N_per_A=baseline,relative_difference=abs(calculated-baseline)/baseline))
            print(order,x,calculated,baseline,flush=True)
    result=dict(configuration_id=p['configuration_id'],method='Independent source-face quadrature with exact depth integration',
        CAD_parameter_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        reference_source_sha256=hashlib.sha256(Path(reference.__file__).read_bytes()).hexdigest(),cases=rows,
        limitations=['Shared uniform NdFeB polarization1.32T, air/permeability assumptions and current geometry',
            'Checks active-copper force component; return contribution has a separate approximate integration',
            'Not a physical magnetic test or a nonlinear3D FEM solution'])
    (ROOT/'analysis/SURFACE_CHARGE_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
    (ROOT/'analysis/SURFACE_CHARGE_INPUT.json').write_bytes(raw)

if __name__=='__main__':main()
