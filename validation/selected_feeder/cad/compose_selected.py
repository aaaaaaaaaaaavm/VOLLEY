"""Publication plates from identified native-CAD Blender renders.
The embedded raster views retain the geometry of their source states.
"""
from pathlib import Path
import sys,json,hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
H=Path(sys.argv[1]).resolve();O=H/'figures'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none','pdf.fonttype':42,'savefig.dpi':300})
exports=[]
def save(fig,stem):
 for ext in ['png','jpg','pdf','svg']:
  p=O/(stem+'.'+ext);fig.savefig(p,dpi=300,facecolor='white');exports.append({'path':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 plt.close(fig)
fig=plt.figure(figsize=(7.1,5.3));ax=fig.add_axes([0,.16,1,.72]);ax.imshow(plt.imread(O/'FM08_stowed.png'));ax.axis('off')
fig.text(.025,.95,'FM08-R3  |  Guided lead-screw feeder',fontsize=13,weight='bold',va='top')
fig.text(.025,.90,'Two 1U cells + two 3U cells · one indexed receiver',fontsize=10,va='top')
fig.text(.025,.115,'Blue: surrogate spacecraft   Orange: restraints   Grey: structure',fontsize=9)
fig.text(.025,.075,'Native CAD rendered in Blender Workbench; nominal stowed configuration.',fontsize=9)
fig.text(.025,.035,'Fixed 1U spacers remain in their cassettes. Geometry is an academic design.',fontsize=9)
save(fig,'FM08_assembly')
fig,axs=plt.subplots(2,2,figsize=(7.1,6.3));titles=['(a) Stored; receiver at home','(b) Prescribed 3U transfer','(c) Seated in the receiver','(d) Release interface clear']
phases=['stowed','midtransfer','3U_seated','launch']
for ax,phase,title in zip(axs.flat,phases,titles):
 ax.imshow(plt.imread(O/('FM08_detail_'+phase+'.png')));ax.axis('off');ax.set_title(title,loc='left',fontsize=10,pad=6)
fig.subplots_adjust(left=.01,right=.99,top=.89,bottom=.18,wspace=.02,hspace=.06)
fig.text(.02,.96,'FM08-R3  |  Transfer and release preparation',fontsize=12,weight='bold',va='top')
fig.text(.02,.13,'Cropped native CAD views; neighbouring structures may be truncated.',fontsize=9)
fig.text(.02,.085,'Prescribed states, without dynamic or time fidelity. The pusher commands',fontsize=9)
fig.text(.02,.05,'transfer; channel stops and required proofs define the delivery datum.',fontsize=9)
save(fig,'FM08_sequence')
# A labelled sequence of discrete views is intentionally not a simulated movie.
from PIL import Image,ImageDraw,ImageFont
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',25)
frames=[]
for phase,title in zip(phases,titles):
 im=Image.open(O/('FM08_detail_'+phase+'.png')).convert('RGB');im.thumbnail((1000,650));canvas=Image.new('RGB',(1000,750),'white');canvas.paste(im,((1000-im.width)//2,65))
 d=ImageDraw.Draw(canvas);d.text((18,12),title,font=font,fill='#20303b');d.text((18,707),'FM08-R3 | Native CAD poses; illustrative timing',font=font,fill='#20303b');frames.append(canvas)
p=O/'FM08_prescribed_sequence.gif';frames[0].save(p,save_all=True,append_images=frames[1:],duration=1100,loop=0);exports.append({'path':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(O/'PLATE_PROVENANCE.json').write_text(json.dumps({'revision':'FM08-R3','source_render_manifest_sha256':hashlib.sha256((O/'BLENDER_PROVENANCE.json').read_bytes()).hexdigest(),'composition_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'evidence_class':'Labeled technical plates of native-CAD render states; not solver screenshots or measured performance. GIF is discrete prescribed poses with illustrative timing.','exports':exports},indent=2)+'\n')
print('Created two publication plates and prescribed-view GIF from identified actual CAD renders.')
