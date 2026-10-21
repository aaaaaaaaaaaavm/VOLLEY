"""Partition the FM06 payload into nine convex solids with disjoint interiors.

The core and four rounded rails are unchanged. Rail material outside the core is
partitioned by the core's Y/Z planes. Each cell is an intersection of a convex
rounded prism with half-spaces. Collision hulls inscribe the curved surfaces;
their discretization requires a separate refinement check.
"""
from pathlib import Path
import hashlib
import json
import shutil
import argparse
import itertools
import FreeCAD as App
import Part
from mechanism import shapes, State, B

H = Path(__file__).resolve().parent
p = argparse.ArgumentParser()
p.add_argument('--deflection-mm',type=float,default=.005)
p.add_argument('--output',default='geometry_convex')
a=p.parse_args()
O=H/a.output
records=[]
for size,L in [('1U',113.5),('3U',340.5)]:
    src=H/'geometry_mesh'/size;dst=O/size
    shutil.copytree(src,dst,dirs_exist_ok=True)
    actual=shapes(L,State(gate=120,bolt=0))[0]['payload']
    center=actual.Solids[0].CenterOfMass
    core=B((L,99,99),(0,-199.5,23.1))
    cells=[core]
    for ry in [0,91.5]:
        for rz in [0,91.5]:
            rail=B((L,8.5,8.5),(0,-200+ry,22.6+rz))
            rail=rail.makeFillet(1.,[e for e in rail.Edges if abs(e.Length-L)<1e-6])
            zlo=22.6 if rz==0 else 122.1
            cells.append(rail.common(B((L+2,102,.5),(-1,-201,zlo))).removeSplitter())
            ylo=-200 if ry==0 else -100.5
            cells.append(rail.common(B((L+2,.5,99),(-1,ylo,23.1))).removeSplitter())
    assert len(cells)==9 and all(c.isValid() and len(c.Solids)==1 for c in cells)
    union=cells[0].multiFuse(cells[1:]).removeSplitter()
    missing=actual.cut(union).Volume;extra=union.cut(actual).Volume
    overlaps=[cells[i].common(cells[j]).Volume for i,j in itertools.combinations(range(9),2)]
    assert max([missing,extra]+overlaps)<1e-5,(missing,extra,max(overlaps))
    files=[];pieces=[]
    for i,cell in enumerate(cells):
        vertices,faces=cell.tessellate(a.deflection_mm)
        f=dst/f'payload_cell_{i:02d}.obj'
        with f.open('w') as out:
            for v in vertices:
                out.write('v %.15g %.15g %.15g\n'%tuple((getattr(v,k)-getattr(center,k))*.001 for k in ['x','y','z']))
            for tri in faces: out.write('f %d %d %d\n'%tuple(j+1 for j in tri))
        cell.exportStep(str(dst/f'payload_cell_{i:02d}.step'))
        files.append(f.name);pieces.append({'index':i,'volume_mm3':cell.Volume,'vertices':len(vertices),'triangles':len(faces),'obj_sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
    rows=[r.split('\t') for r in (src/'bodies.tsv').read_text().splitlines()]
    for r in rows:
        if r[0]=='payload':r[12]=','.join(files)
    (dst/'bodies.tsv').write_text('\n'.join('\t'.join(r) for r in rows)+'\n')
    records.append({'size':size,'missing_volume_mm3':missing,'extra_volume_mm3':extra,'maximum_pair_overlap_mm3':max(overlaps),'pieces':pieces})
    print(size,'nine material-equivalent disjoint convex cells',flush=True)
(O/'PARTITION.json').write_text(json.dumps({'CAD':'FM06-R1 unchanged','CAD_sha256':hashlib.sha256((H/'mechanism.py').read_bytes()).hexdigest(),'deflection_mm':a.deflection_mm,'construction':'Core box plus intersections of convex filleted rail prisms with non-overlapping external core-plane slabs. Shared boundaries permitted; positive interior overlap rejected. Homogeneous payload mass/inertia preserved from full native solid, not summed from collision hulls.','configurations':records},indent=2)+'\n')
