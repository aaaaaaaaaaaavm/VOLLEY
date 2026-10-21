"""Exact rectilinear collision cells inside the declared guarded contact domain.

The full source geometry, mass, CG and inertia remain unchanged. Portions which
cannot reach a payload inside the existing X/Z domain guard are clipped away.
Moving receiver geometry includes its complete 12mm upward stroke. Nonplanar
material in the retained domain is rejected rather than approximated by a box.
"""
from pathlib import Path
import argparse, hashlib, itertools, json, shutil
import FreeCAD as App
import Part
from mechanism import shapes, State, B

H=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--output',default='geometry_volumetric');p.add_argument('--x-margin-mm',type=float,default=3);a=p.parse_args()
O=H/a.output;records=[]

def partition(sh):
    for face in sh.Faces:
        assert isinstance(face.Surface,Part.Plane),('nonplanar retained face',str(face.Surface))
        n=face.normalAt(0,0)
        assert max(abs(n.x),abs(n.y),abs(n.z))>1-1e-8,('non-orthogonal face',n)
    axes=[sorted(set(round(getattr(v.Point,k),7) for v in sh.Vertexes)) for k in ['x','y','z']]
    dims=[len(x)-1 for x in axes]
    occupied=set()
    for i,j,k in itertools.product(*(range(n) for n in dims)):
        mid=App.Vector(*[(axes[d][u]+axes[d][u+1])/2 for d,u in enumerate([i,j,k])])
        if sh.isInside(mid,1e-8,False):occupied.add((i,j,k))
    cells=[]
    while occupied:
        lo=min(occupied);hi=list(lo)
        for axis in [0,1,2]:
            while hi[axis]+1<dims[axis]:
                nxt=hi[axis]+1
                section=itertools.product(*(range(lo[d],hi[d]+1) if d!=axis else [nxt] for d in range(3)))
                if not all(q in occupied for q in section):break
                hi[axis]=nxt
        for q in itertools.product(*(range(lo[d],hi[d]+1) for d in range(3))):occupied.remove(q)
        lower=[axes[d][lo[d]] for d in range(3)];upper=[axes[d][hi[d]+1] for d in range(3)]
        cells.append((lower,[upper[d]-lower[d] for d in range(3)]))
    boxes=[B(dim,lo) for lo,dim in cells]
    total=sum(s.Volume for s in boxes)
    inside=sum(s.common(sh).Volume for s in boxes)
    assert abs(total-sh.Volume)<1e-4 and abs(inside-total)<1e-4,(sh.Volume,total,inside)
    return cells

for size,L in [('1U',113.5),('3U',340.5)]:
    src=H/'geometry_convex'/size;dst=O/size;dst.mkdir(parents=True,exist_ok=True)
    rows=[r.split('\t') for r in (src/'bodies.tsv').read_text().splitlines()]
    ss,_=shapes(L,State(gate=120,bolt=0));parts=[]
    for row in rows:
        name=row[0]
        if name=='payload':
            for f in row[12].split(','):shutil.copy2(src/f,dst/f)
            continue
        shape=ss[name]
        zlo=8 if name=='sled_entry_bar' else 14
        domain=B((L+2*a.x_margin_mm,1000,128-zlo),(-a.x_margin_mm,-500,zlo))
        retained=shape.common(domain).removeSplitter()
        cells=partition(retained) if retained.Volume>1e-8 else []
        center=shape.Solids[0].CenterOfMass
        files=[]
        for i,(lo,dim) in enumerate(cells):
            f=dst/f'box_{name}_{i:03d}.obj'
            with f.open('w') as out:
                for signs in itertools.product([0,1],repeat=3):
                    out.write('v %.15g %.15g %.15g\n'%tuple((lo[d]+dim[d]*signs[d]-getattr(center,['x','y','z'][d]))*.001 for d in range(3)))
                # Loader uses only the native box's 8 corners, not its triangle surface.
                for tri in [(1,2,4),(1,4,3),(5,7,8),(5,8,6),(1,5,6),(1,6,2),(3,4,8),(3,8,7),(1,3,7),(1,7,5),(2,6,8),(2,8,4)]:out.write('f %d %d %d\n'%tri)
            files.append(f.name)
        row[12]=','.join(files) if files else 'NONE'
        parts.append({'part':name,'retained_volume_mm3':retained.Volume,'original_volume_mm3':shape.Volume,'cell_count':len(cells),'cells':[{'lo_mm':lo,'size_mm':dim} for lo,dim in cells]})
    (dst/'bodies.tsv').write_text('\n'.join('\t'.join(r) for r in rows)+'\n')
    records.append({'size':size,'parts':parts});print(size,sum(x['cell_count'] for x in parts),'exact contact-domain boxes',flush=True)
shutil.copy2(H/'geometry_convex/PARTITION.json',O/'PAYLOAD_PARTITION.json')
(O/'MECHANISM_PARTITION.json').write_text(json.dumps({'source_CAD_sha256':hashlib.sha256((H/'mechanism.py').read_bytes()).hexdigest(),'contact_domain_mm':{'x':f'[-{a.x_margin_mm},L+{a.x_margin_mm}]','z':'[14,128] payload guard; receiver retained initial Z>=8 for its upward12mm stroke','y':'[-500,500]'},'method':'Orthogonal native B-rep partition by all axis-aligned vertex planes; midpoint occupancy and exact per-cell intersection-volume identity. Greedy merged cells have disjoint grid interiors. Full body mass and inertia are retained. Nonplanar retained geometry is rejected.','scope':'Only the FCE08 gate-already-open transfer/capture/withdraw subcycle. Geometry outside the guard is intentionally absent from collision; leaving the guard rejects the simulation. This representation cannot be used for unrestricted full-cycle motion.','configurations':records},indent=2)+'\n')
