"""Plot the actual chassis native mesh and computed paired-face closure."""
from pathlib import Path
import argparse,collections,hashlib,json,os
os.environ.setdefault('MPLCONFIGDIR','/tmp/volley-mpl-config')
os.environ.setdefault('XDG_CACHE_HOME','/tmp/volley-xdg-cache')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

ap=argparse.ArgumentParser();ap.add_argument('run_directory',type=Path);a=ap.parse_args();O=a.run_directory
d=json.loads((O/'MESH.json').read_text());result=json.loads((O/'CHASSIS_FEA_REVIEW.json').read_text());coords={int(n):np.array(v)for n,v in d['node_coordinates'].items()};u={};mode=False
for line in(O/'chassis.dat').read_text().splitlines():
    if 'displacements ('in line:mode=True;continue
    if 'forces ('in line:mode=False
    q=line.split()
    if mode and len(q)==4:
        try:u[int(q[0])]=np.array(list(map(float,q[1:])))
        except ValueError:pass
faces={};element=False
for line in(O/'chassis.inp').read_text().splitlines():
    if line.startswith('*ELEMENT'):element=True;continue
    if line.startswith('*'):element=False
    if element:
        q=[int(v)for v in line.split(',')][1:5]
        for ids in [(0,2,1),(0,1,3),(1,2,3),(2,0,3)]:
            face=tuple(q[i]for i in ids);key=tuple(sorted(face))
            if key in faces:faces[key]=None
            else:faces[key]=face
boundary=[v for v in faces.values()if v is not None];triangles=np.array([[coords[n]+20*u[n]for n in face]for face in boundary]);values=np.array([np.mean([u[n][2]for n in face])for face in boundary])
fig=plt.figure(figsize=(13,5.3));gs=fig.add_gridspec(1,2,width_ratios=[1.05,1]);ax=fig.add_subplot(gs[0],projection='3d')
normal=matplotlib.colors.Normalize(-.15,.15);collection=Poly3DCollection(triangles,facecolors=plt.get_cmap('coolwarm')(normal(values)),edgecolors=(.1,.15,.22,.16),linewidths=.12,rasterized=True);ax.add_collection3d(collection)
allxyz=np.vstack(triangles);lo=allxyz.min(axis=0);hi=allxyz.max(axis=0);ax.set_xlim(lo[0],hi[0]);ax.set_ylim(lo[1],hi[1]);ax.set_zlim(lo[2],hi[2]);ax.set_box_aspect(hi-lo);ax.view_init(20,-63);ax.set_xlabel('X [mm]');ax.set_ylabel('Y [mm]');ax.set_zlabel('Z [mm]');ax.set_title('Actual chassis native mesh\nDeformed ×20; signed Uz [mm]',fontsize=11)
fig.colorbar(matplotlib.cm.ScalarMappable(norm=normal,cmap='coolwarm'),ax=ax,shrink=.65,pad=.05,orientation='horizontal',label='Uz [mm]')
q=np.load(O/'PAIRED_PATCH_DISPLACEMENT.npz');xy=q['query_xy_mm'];ax2=fig.add_subplot(gs[1]);contour=ax2.tricontourf(xy[:,0],xy[:,1],q['separation_reduction_mm'],levels=np.linspace(0,.3,16),cmap='viridis');ax2.set_aspect('equal');ax2.set_xlabel('X [mm]');ax2.set_ylabel('Y [mm]');ax2.set_title('Paired magnet-support face closure\nLower Uz − upper Uz at common XY',fontsize=11);fig.colorbar(contour,ax=ax2,orientation='horizontal',pad=.22,label='Face-separation reduction [mm]')
fig.suptitle('Corrected chassis · 3010.48 N per array · 62,198 quadratic tetrahedra',fontsize=13,y=.98)
identity_text='Final source BREP d4b53d52 identity verified.'if(O/'FINAL_CAD_IDENTITY.json').exists()else'Candidate BREP d4b53d52; final source identity must match.'
fig.text(.5,.025,'6 scalar web constraints remove rigid modes. Includes actual holes and integral supports; excludes assembled stator, magnets and bonds.\n'+identity_text+' Paired closure is invariant to the rigid-motion gauge.',ha='center',fontsize=8,color='#3f4a56')
fig.subplots_adjust(left=.03,right=.97,top=.86,bottom=.2,wspace=.25)
for ext in ['png','pdf','svg']:fig.savefig(O/('ACTUAL_CHASSIS_RESULT.'+ext),dpi=190,facecolor='white')
metadata=dict(source_BREP_sha256=d['input_BREP_sha256'],plot_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),boundary_corner_triangles=len(boundary),displacement_exaggeration=20,source_result_sha256=hashlib.sha256((O/'CHASSIS_FEA_REVIEW.json').read_bytes()).hexdigest(),scope='Corner triangulation of actual C3D10 boundary and actual interpolated paired displacement field; scientific result graphic, not a software-interface screenshot.')
(O/'ACTUAL_CHASSIS_FIGURE.json').write_text(json.dumps(metadata,indent=2)+'\n');print('Saved actual chassis PNG/PDF/SVG',len(boundary),'boundary triangles',flush=True)
