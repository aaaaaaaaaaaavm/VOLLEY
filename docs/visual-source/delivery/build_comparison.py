"""Render a clearly schematic passive-canister/VOLLEY principle comparison."""
from pathlib import Path
import math,json,subprocess,argparse
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;OUT=P/'comparison';OUT.mkdir(exist_ok=True)
W,H=1280,720;BG='#11161c';PANEL='#1b2229';INK='#f6f5f1';DIM='#c0c7cd';ACC='#55bfb4';GRAY='#a9b2ba'
def font(n,b=False):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold'if b else'')+'.ttf',n)
def ramp(t,a,b):return min(1,max(0,(t-a)/(b-a)))
def spring(d,start,end,y,color):
 pts=[(start,y),(start+5,y)]
 for i in range(14):pts.append((start+5+(end-start-10)*(i+.5)/14,y+(-9 if i%2 else 9)))
 pts +=[(end-5,y),(end,y)];d.line(pts,fill=color,width=3)
def arrow(d,x,y,dx,color):
 d.line((x,y,x+dx,y),fill=color,width=3);d.polygon([(x+dx,y),(x+dx-10,y-5),(x+dx-10,y+5)],fill=color)
def frame(t):
 im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 d.text((36,22),'VOLLEY / DEPLOYMENT PRINCIPLES',font=font(17,True),fill=DIM)
 d.text((36,65),'Stored spring energy or a commanded powered stroke',font=font(34,True),fill=INK)
 for x,head in [(36,'PASSIVE CANISTER EXAMPLE'),(660,'VOLLEY / ACR1')]:
  d.rectangle((x,139,x+584,554),fill=PANEL);d.text((x+20,160),head,font=font(20,True),fill=GRAY if x==36 else ACC)
 # Generic P-POD-style spring/door drawing. It is not a supplier drawing or rating.
 x=62;y=302;open_=ramp(t,2,5);travel=190*ramp(t,5,10);cube_x=x+115+travel
 d.line((x+24,y-66,x+304,y-66),fill=GRAY,width=4);d.line((x+24,y+66,x+304,y+66),fill=GRAY,width=4);d.line((x+24,y-66,x+24,y+66),fill=GRAY,width=4)
 spring(d,x+28,x+110+min(travel,140),y,GRAY);d.line((x+110+min(travel,140),y-44,x+110+min(travel,140),y+44),fill=GRAY,width=4)
 d.rectangle((cube_x,y-40,cube_x+137,y+40),fill=GRAY,outline=INK,width=2)
 d.line((x+304,y+66,x+304+90*math.sin(math.pi/2*open_),y+66-132*math.cos(math.pi/2*open_)),fill=GRAY,width=5)
 d.text((58,412),'Open retention → spring extends → payload exits',font=font(20),fill=INK)
 d.text((58,452),'Separation energy is set before deployment.',font=font(20),fill=DIM)
 d.text((58,490),'Actual doors, speeds and interfaces vary by product.',font=font(16),fill=DIM)
 # Same explanatory scale on the right; edited timing, no force simulation.
 x=689;y=302;u=ramp(t,5,10);carrier=170*u if t<10 else 170*(1-ramp(t,12,17));payload=170*u if t<10 else 170+135*ramp(t,10,13)
 d.line((x+20,y+67,x+480,y+67),fill=GRAY,width=4)
 d.rectangle((x+60+carrier,y+33,x+224+carrier,y+61),fill='#76868f');d.rectangle((x+67+carrier,y+22,x+217+carrier,y+33),fill=ACC)
 d.rectangle((x+73+payload,y-61,x+210+payload,y+20),fill=ACC,outline=INK,width=2)
 arrow(d,x+60,y-95,170,ACC)
 d.text((682,412),'Select release command → accelerate → release',font=font(20),fill=INK)
 d.text((682,452),'Carrier and pallet brake and return.',font=font(20),fill=DIM)
 d.text((682,490),'Current modeled command points: 1 / 2 / 3 m/s.',font=font(18,True),fill=ACC)
 if t<10:head='Both release into a state already established by the host.'
 else:head='Host trims or a preset spring can match preplanned targets.'
 assert d.textlength(head,font=font(24,True))<1208
 d.text((36,588),head,font=font(24,True),fill=INK)
 d.text((36,635),'Principle schematics • not scaled CAD • edited timing • no supplier-specific or universal spring rating',font=font(17),fill=DIM)
 d.text((36,672),'Adjustable electromagnetic and mechanical separation systems also exist in prior art.',font=font(18),fill=DIM)
 return im
if __name__=='__main__':
 cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','24','-i','-','-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'comparison.mp4')]
 p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 for i in range(480):p.stdin.write(frame(i/24).tobytes())
 p.stdin.close();assert p.wait()==0
 for t in [1,6,12,18]:frame(t).save(OUT/f'review-{t:02d}.jpg',quality=94)
 (OUT/'captions.vtt').write_text('WEBVTT\n\n00:00:00.000 --> 00:00:10.000\nPassive canisters release stored spring energy; VOLLEY commands a powered stroke.\nBoth start from the host-established orbital state.\n\n00:00:10.000 --> 00:00:20.000\nHost trims or an ideal preset spring can match preplanned targets.\nActual deployer mechanisms and separation settings vary.\n')
 (OUT/'TRANSCRIPT.md').write_text('# Deployment-principle comparison\n\nThis20-second original schematic contrasts a representative spring-pusher canister/door sequence with a commanded powered carrier, retained pallet and recovery sequence. It is not a supplier drawing, catalog rating or hardware test. Current ACR1 modeled command points are1,2 and3m/s. Actual P-POD and other deployer designs vary. Prior adjustable separation systems are acknowledged. Both approaches depend on the host state; preset spring energy or host trims can match preplanned targets.\n')
 print('Rendered20-second comparison')
