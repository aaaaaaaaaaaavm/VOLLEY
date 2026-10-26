"""Compose readable editorial titles over actual Blender animation frames."""
from pathlib import Path
import argparse,json,subprocess,hashlib
from PIL import Image,ImageDraw,ImageFont
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).parent);ap.add_argument('--preview',action='store_true');args=ap.parse_args();R=args.root.resolve()
W,H=1280,720;BG='#11161c';INK='#f6f5f1';DIM='#c0c7cd';ACC='#55bfb4';GOLD='#efd199'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(n,b=False):return ImageFont.truetype(BOLD if b else FONT,n)
CHAPTERS=[
 (0,4,'01','Retain the inventory','Twelve 3U envelopes. Two independent six-cell banks.'),
 (4,10,'02','Retrieve the captive pallet','The lift grips the reusable pallet before carrier locks release.'),
 (10,16,'03','Index to the selected cell','The pallet rises to the source-cell loading plane.'),
 (16,25,'04','Feed one CubeSat','Storage keepers open. Guided lead-screw pusher advances 250 mm.'),
 (25,30,'05','Secure the transfer','Lift keepers retain the payload. Pusher retracts; cell gates close.'),
 (30,38,'06','Lower to the launch plane','Loaded lift moves from 830 mm to the 46 mm launch datum.'),
 (38,43,'07','Transfer custody to the sled','Carrier locks engage before the lift releases its pallet grips.'),
 (43,49,'08','Clear. Prove. Arm.','Lift clear. Pallet locked. Source and arrest path ready.'),
 (49,54,'09','Accelerate the loaded sled','1.300 m powered stroke. Evaluated commands: 1, 2 and 3 m/s.'),
 (54,58,'10','Release the CubeSat','The payload departs; the pallet remains attached to the sled.'),
 (58,65,'11','Arrest and return the carrier','210 mm arrest allocation. Retained carrier and pallet return.'),
 (65,70,'12','Index the next retained cell','Eleven payloads remain. Repeat the controlled sequence.'),
]
def chapter(t):return next(c for c in CHAPTERS if c[0]<=t<c[1])
def compose(im,t):
 im=im.convert('RGB');d=ImageDraw.Draw(im);a,b,n,title,text=chapter(min(t,69.999))
 # Fixed opaque bands reserve legible text space; geometry is intentionally framed below the header.
 d.rectangle((0,0,W,98),fill=BG);d.rectangle((0,610,W,H),fill=BG)
 d.text((36,18),'VOLLEY',font=font(18,True),fill=INK);d.text((180,21),'STORAGE → FEED → LAUNCH',font=font(13),fill=DIM)
 d.text((36,48),n,font=font(28,True),fill=ACC);d.text((94,47),title,font=font(30,True),fill=INK)
 d.text((36,622),text,font=font(21),fill=INK)
 note='CAD-derived operating-sequence animation • display timing edited'
 if 4<=t<46:note+=' • other cells / mounts hidden for clarity'
 d.text((36,664),note,font=font(14),fill=DIM)
 if 49<=t<58:d.text((920,20),'LAUNCH SHOWN SLOWLY',font=font(12,True),fill=ACC)
 # Inventory indicator counts the actually depicted first departure.
 d.text((1040,666),f'{12 if t<54 else 11} / 12 RETAINED',font=font(13),fill=ACC)
 d.line((36,704,1244,704),fill='#35434a',width=3);d.line((36,704,36+1208*t/70,704),fill=ACC,width=3)
 assert d.textlength(text,font=font(21))<1208,(title,'caption overflow')
 return im
def stamp(t):return f'{int(t//3600):02d}:{int(t%3600//60):02d}:{t%60:06.3f}'.replace('.',',')
transcript=[{'start_s':a,'end_s':b,'step':n,'title':title,'text':text,'evidence_class':'CAD-derived editorial animation; edited timing; current Gen5 ACR1 geometry'}for a,b,n,title,text in CHAPTERS]
(R/'transcript.json').write_text(json.dumps(transcript,indent=2)+'\n');(R/'transcript.txt').write_text('\n\n'.join(f'{a:02d}–{b:02d} s | {title}\n{text}'for a,b,n,title,text in CHAPTERS)+'\n')
(R/'captions.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{stamp(a).replace(",",".")} --> {stamp(b).replace(",",".")}\n{title}\n{text}'for a,b,n,title,text in CHAPTERS)+'\n')
if args.preview:
 thumbs=[]
 for file in sorted(R.glob('preview-*.jpg')):
  t=(int(file.stem.split('-')[-1])-1)/24;im=compose(Image.open(file),t);im.save(R/file.name.replace('preview-','review-'),quality=94);thumbs.append(im.resize((426,240)))
 grid=Image.new('RGB',(426*3,240*((len(thumbs)+2)//3)),BG)
 for i,im in enumerate(thumbs):grid.paste(im,((i%3)*426,(i//3)*240))
 grid.save(R/'CONTACT_SHEET.jpg',quality=92)
else:
 cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','24','-i','-','-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(R/'mechanism.mp4')]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 for f in range(1,1681):
  im=compose(Image.open(R/'frames'/f'{f:04d}.jpg'),(f-1)/24);proc.stdin.write(im.tobytes())
 proc.stdin.close();assert proc.wait()==0
 compose(Image.open(R/'frames/0049.jpg'),2).save(R/'poster.jpg',quality=94)
 print('ENCODED',R/'mechanism.mp4')
