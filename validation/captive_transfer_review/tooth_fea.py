"""Native CalculiX mesh study: enlarged isolated tooth, assumed fixed root.

SI units. Uniform transverse force at z=3mm; E=200GPa, nu=.3 assumed steel.
An isolated linear elastic fixture is not pawl contact or an assembly margin.
"""
from pathlib import Path
import os,subprocess,json,math,hashlib

H=Path(__file__).resolve().parent;O=H/"release/tooth_fea";O.mkdir(parents=True,exist_ok=True)


def run(force,n):
    nx,ny,nz=2*n,n,n
    nodes={(i,j,k):1+i+(nx+1)*j+(nx+1)*(ny+1)*k for k in range(nz+1) for j in range(ny+1) for i in range(nx+1)}
    name=f"tooth_{round(force*1000)}mN_{nx}x{ny}x{nz}"
    lines=["*HEADING",name+"; isolated fixed root, no contact or allowable","*NODE"]
    for (i,j,k),nid in nodes.items():lines.append(f"{nid},{.016*i/nx:.12g},{.006*j/ny:.12g},{.003*k/nz:.12g}")
    lines.append("*ELEMENT,TYPE=C3D8I,ELSET=TOOTH")
    eid=0
    for k in range(nz):
        for j in range(ny):
            for i in range(nx):
                eid+=1
                corners=[(i,j,k),(i+1,j,k),(i+1,j+1,k),(i,j+1,k),(i,j,k+1),(i+1,j,k+1),(i+1,j+1,k+1),(i,j+1,k+1)]
                lines.append(str(eid)+","+",".join(str(nodes[c]) for c in corners))
    fixed=[nid for (i,j,k),nid in nodes.items() if k==0]
    lines.append("*NSET,NSET=ROOT")
    for t in range(0,len(fixed),16):lines.append(",".join(map(str,fixed[t:t+16])))
    lines += ["*NSET,NSET=ALLNODES,GENERATE",f"1,{len(nodes)},1","*MATERIAL,NAME=STEEL_ASSUMED","*ELASTIC","200000000000,0.3","*SOLID SECTION,ELSET=TOOTH,MATERIAL=STEEL_ASSUMED","*BOUNDARY","ROOT,1,3","*STEP","*STATIC","*CLOAD"]
    total=0
    for (i,j,k),nid in nodes.items():
        if k!=nz:continue
        f=force/nx/ny*(.5 if i in [0,nx] else 1)*(.5 if j in [0,ny] else 1)
        total+=f;lines.append(f"{nid},2,{f:.12g}")
    assert abs(total-force)<1e-8
    lines += ["*NODE PRINT,NSET=ALLNODES","U,RF","*EL PRINT,ELSET=TOOTH","S","*NODE FILE","U","*EL FILE","S","*END STEP"]
    p=O/name;p.with_suffix(".inp").write_text("\n".join(lines)+"\n")
    r=subprocess.run([os.environ.get("CCX","ccx"),"-i",name],cwd=O,capture_output=True,text=True)
    p.with_suffix(".log").write_text(r.stdout+r.stderr)
    assert r.returncode==0,r.stderr
    mode=None;u=[];stress=[];reaction=0
    for line in p.with_suffix(".dat").read_text().splitlines():
        if "displacements" in line:mode="u";continue
        if "forces" in line:mode="rf";continue
        if "stresses" in line:mode="s";continue
        v=line.split()
        try:
            if mode=="u" and len(v)==4:u.append(abs(float(v[2])))
            elif mode=="rf" and len(v)==4 and int(v[0]) in fixed:reaction+=float(v[2])
            elif mode=="s" and len(v)==8:
                xx,yy,zz,xy,xz,yz=map(float,v[2:]);stress.append(math.sqrt(.5*((xx-yy)**2+(yy-zz)**2+(zz-xx)**2)+3*(xy*xy+xz*xz+yz*yz)))
        except ValueError:pass
    assert u and stress
    assert abs(reaction+force)<force*1e-5,(reaction,force)
    return dict(case=name,elements=eid,nodes=len(nodes),force_N=force,max_uy_m=max(u),max_von_mises_MPa=max(stress)/1e6,root_reaction_y_N=reaction,
      files={p.with_suffix(ext).name:hashlib.sha256(p.with_suffix(ext).read_bytes()).hexdigest() for ext in [".inp",".dat",".frd",".log"]})


rows=[]
for f in [425.22496995827527,876.9]:
    group=[run(f,n) for n in [2,4,6]]
    group[-1]["last_displacement_relative_change"]=abs(group[-1]["max_uy_m"]-group[-2]["max_uy_m"])/group[-1]["max_uy_m"]
    group[-1]["last_peak_stress_relative_change"]=abs(group[-1]["max_von_mises_MPa"]-group[-2]["max_von_mises_MPa"])/group[-1]["max_von_mises_MPa"]
    rows+=group
(O/"RESULTS.json").write_text(json.dumps(dict(solver="CalculiX 2.23",cases=rows,geometry_mm=[16,6,3],material="Assumed steel E200GPa nu0.3; no selected allowable",
  boundary="Isolated short tooth with ideal fixed root and distributed top shear; sharp corners/constraint stresses can remain mesh-dependent. No pawl impact, root fillet, carrier joints, fatigue or assembly qualification.",source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2)+"\n")
print([(r["case"],r["max_von_mises_MPa"]) for r in rows])
