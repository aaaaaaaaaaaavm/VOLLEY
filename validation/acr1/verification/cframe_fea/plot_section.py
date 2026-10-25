"""Scientific section view from actual C3D10 mesh and CCX nodal displacements."""
from pathlib import Path
import json,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from matplotlib.collections import LineCollection
H=Path(__file__).resolve().parent;O=H/'h8';meta=json.loads((O/'MESH.json').read_text());coords={int(n):np.array(x)for n,x in meta['node_coordinates'].items()};u={};mode=False
for line in(O/'cframe.dat').read_text().splitlines():
 if 'displacements (' in line:mode=True;continue
 if 'forces (' in line:mode=False
 q=line.split()
 if mode and len(q)==4:
  try:u[int(q[0])]=np.array(list(map(float,q[1:])))
  except ValueError:pass
els=[];mode=False
for line in(O/'cframe.inp').read_text().splitlines():
 if line.startswith('*'):mode=line.startswith('*ELEMENT');continue
 if mode:els.append([int(v)for v in line.split(',')][1:])
faces=[]
for e in els:
 for ix in [[0,1,2,4,5,6],[0,1,3,4,8,7],[1,2,3,5,9,8],[0,2,3,6,9,7]]:
  f=[e[j]for j in ix]
  if all(abs(coords[n][0])<1e-7 for n in f):
   a,b,c,ab,bc,ca=f;faces.extend([[a,ab,ca],[ab,b,bc],[ca,bc,c],[ab,bc,ca]])
assert faces
nodes=sorted({n for tri in faces for n in tri});idx={n:i for i,n in enumerate(nodes)};tri=np.array([[idx[n]for n in t]for t in faces]);xy=np.array([[coords[n][1],coords[n][2]]for n in nodes]);disp=np.array([[u[n][1],u[n][2]]for n in nodes]);normal=-disp[:,1]
# Display the actual X-midspan upper-quarter slice plus the Z-symmetry reflection.
mirror=xy.copy();mirror[:,1]*=-1;md=disp.copy();md[:,1]*=-1
allxy=np.vstack([xy,mirror]);alld=np.vstack([disp,md]);alltri=np.vstack([tri,tri+len(nodes)]);color=np.r_[normal,normal]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'svg.fonttype':'none','pdf.fonttype':42,'ps.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(1,2,figsize=(9.2,3.4));scale=20
for axis in ax:axis.set_aspect('equal');axis.set_xlim(-112,82);axis.set_ylim(-40,40);axis.set_xlabel('CAD Y / mm');axis.set_ylabel('CAD Z / mm')
segments=np.array([[allxy[t[0]],allxy[t[1]]]for t in alltri]+[[allxy[t[1]],allxy[t[2]]]for t in alltri]+[[allxy[t[2]],allxy[t[0]]]for t in alltri])
ax[0].add_collection(LineCollection(segments,colors='#6f7c82',linewidths=.22));ax[0].set_title('(a) Actual C3D10 section mesh',loc='left',fontsize=10)
for y in [-40,-20,0,20,40]:
 ax[0].annotate('',xy=(y,7),xytext=(y,14),arrowprops={'arrowstyle':'-|>','color':'#a44d28','lw':.8})
 ax[0].annotate('',xy=(y,-7),xytext=(y,-14),arrowprops={'arrowstyle':'-|>','color':'#a44d28','lw':.8})
deformed=allxy+scale*alld;triang=mtri.Triangulation(deformed[:,0],deformed[:,1],alltri)
image=ax[1].tripcolor(triang,color,shading='gouraud',cmap='cividis',vmin=-.005,vmax=.18)
# Exact undeformed outline, not an independently generated specimen image.
outline=np.array([[-100,-30],[70,-30],[70,-14],[-80,-14],[-80,14],[70,14],[70,30],[-100,30],[-100,-30]])
ax[1].plot(outline[:,0],outline[:,1],color='#737373',lw=.6,ls='--');ax[1].set_title(f'(b) Inward displacement; shape ×{scale}',loc='left',fontsize=10)
cax=fig.add_axes([.90,.29,.018,.44]);cbar=fig.colorbar(image,cax=cax);cbar.set_label('Inward displacement / mm',fontsize=8);cbar.ax.tick_params(labelsize=8)
fig.suptitle('Isolated C-section FEM — midspan Y–Z section',x=.06,ha='left',fontsize=12)
fig.text(.06,.04,'CalculiX 2.23 · E = 70 GPa, ν = 0.33 · 3010.48 N per array, uniformly redistributed\nMagnetic-face maximum 0.1441 mm; free-edge maximum 0.1778 mm. Isolated model; no flight qualification.',fontsize=8)
fig.subplots_adjust(left=.07,right=.86,bottom=.25,top=.84,wspace=.36)
for suffix in ['png','svg','pdf']:fig.savefig(H/('CFRAME_SECTION.'+suffix),dpi=220)
print('Source section subtriangles',len(alltri),'actual3Dnodes',meta['nodes'],'deformation scale',scale)
