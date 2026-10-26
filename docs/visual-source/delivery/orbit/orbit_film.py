"""100-second continuously animated orbital/comparison chapter, 1280x720/24fps."""
from pathlib import Path
import argparse,hashlib,json,math,subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageFont
H=Path(__file__).resolve().parent
W,HEIGHT,FPS,DURATION=1280,720,24,20
BG='#11161c';FG='#f3f2eb';MUTED='#a6afb7';GRID='#2b3742';TEAL='#4dd9c0';GRAY='#a9b0b7';AMBER='#f3b65f';EARTH='#203a4b'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONTS={}
def font(size,bold=False):
    key=(size,bold)
    if key not in FONTS:FONTS[key]=ImageFont.truetype(BOLD if bold else FONT,size)
    return FONTS[key]
def text(d,pos,s,size=32,fill=FG,bold=False,anchor=None):d.text(pos,s,font=font(size,bold),fill=fill,anchor=anchor)
def line(d,points,fill,width=2):d.line(points,fill=fill,width=width,joint='curve')
def arrow(d,start,end,color=TEAL,width=5):
    line(d,[start,end],color,width);v=np.array(end,dtype=float)-start;v/=np.linalg.norm(v);n=np.array([-v[1],v[0]])
    p=np.array(end);d.polygon([tuple(p),tuple(p-18*v+8*n),tuple(p-18*v-8*n)],fill=color)
def satellite(d,x,y,color=TEAL,scale=1):
    w=10*scale;h=15*scale
    d.rounded_rectangle((x-w,y-h,x+w,y+h),radius=3*scale,fill=color)
    line(d,[(x-w,y),(x+w,y)],BG,2)
    line(d,[(x-w*.35,y-h),(x-w*.35,y+h)],BG,1)
def host(d,x,y,scale=1,burn=False):
    # Generic retained upper stage: no manufacturer-specific silhouette or interface.
    d.rounded_rectangle((x-60*scale,y-26*scale,x+40*scale,y+26*scale),radius=10*scale,fill='#61717e')
    d.polygon([(x+40*scale,y-26*scale),(x+62*scale,y-12*scale),(x+62*scale,y+12*scale),(x+40*scale,y+26*scale)],fill='#82919b')
    d.polygon([(x-60*scale,y-13*scale),(x-80*scale,y-21*scale),(x-80*scale,y+21*scale),(x-60*scale,y+13*scale)],fill=GRAY)
    line(d,[(x-12*scale,y-26*scale),(x-12*scale,y+26*scale)],'#28343e',max(1,int(3*scale)))
    if burn:d.polygon([(x-81*scale,y-14*scale),(x-124*scale,y),(x-81*scale,y+14*scale)],fill=AMBER)
def frame_base(chapter,title,subtitle):
    im=Image.new('RGB',(W,HEIGHT),BG);d=ImageDraw.Draw(im)
    text(d,(52,25),f'VOLLEY  /  ORBITAL DELIVERY  /  {chapter:02d}',22,MUTED,True)
    text(d,(52,70),title,42,FG,True)
    text(d,(52,126),subtitle,28,MUTED)
    line(d,[(52,655),(1228,655)],GRID,2)
    return im
def earth(d,cx,cy,scale):
    r=RE*scale
    d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=EARTH,outline='#3b5d70',width=2)
    # Reference-sphere meridians, not satellite imagery.
    for k in [-.5,0,.5]:
        xx=cx+k*r;hh=r*math.sqrt(1-k*k)
        line(d,[(xx,cy-hh),(xx,cy+hh)],'#2d4a5c',1)
    for k in [-.5,0,.5]:
        yy=cy+k*r;ww=r*math.sqrt(1-k*k)
        line(d,[(cx-ww,yy),(cx+ww,yy)],'#2d4a5c',1)
def xy(points,cx,cy,scale):return [(cx+float(x)*scale,cy-float(y)*scale) for x,y in points]
def orbit_circle(d,r,cx,cy,scale,color=GRAY,width=2):
    rr=r*scale;d.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),outline=color,width=width)
def metric(d,x,y,label,value,color=FG):
    text(d,(x,y),label,26,MUTED)
    text(d,(x,y+34),value,36,color,True)
def curve(ident):
    r=CASE[ident];a=r['semimajor_axis_m'];e=r['eccentricity']
    if a>0:
        E=np.linspace(0,2*np.pi,700)
        return np.c_[a*(np.cos(E)-e),a*np.sqrt(1-e*e)*np.sin(E)]
    return STATES[ident][TIMES<=7200,:2]

def scene1(t):
    im=BASE[0].copy();d=ImageDraw.Draw(im);cx,cy,scale=367,384,222/(RE+600000)
    earth(d,cx,cy,scale);orbit_circle(d,RE+500000,cx,cy,scale,GRAY,3);orbit_circle(d,R,cx,cy,scale,TEAL,3)
    line(d,xy(TRANSFER[:,:2],cx,cy,scale),AMBER,3)
    if t<4:
        theta=.8*(t-4);p=np.array([(RE+500000)*math.cos(theta),(RE+500000)*math.sin(theta)])
        burn=False
    elif t<16:
        i=int((t-4)/12*(len(TRANSFER)-1));p=TRANSFER[i,:2];burn=t<4.7
    else:
        theta=np.pi+(t-16)*.6;p=R*np.array([math.cos(theta),math.sin(theta)]);burn=t<16.7
    px,py=xy([p],cx,cy,scale)[0]
    # Point marker and tangential burn direction keep the physical orbital view unambiguous.
    d.ellipse((px-5,py-5,px+5,py+5),fill=FG)
    if burn:
        tangent=np.array([-p[1],p[0]])/np.linalg.norm(p)
        ex=px+tangent[0]*30;ey=py-tangent[1]*30
        line(d,[(px,py),(ex,ey)],AMBER,4)
        d.ellipse((ex-3,ey-3,ex+3,ey+3),fill=AMBER)
    text(d,(292,365),'EARTH',27,'#9bb8ca',True)
    state='500 km circular' if t<4 else 'Transfer ellipse • coast' if t<16 else '600 km circular'
    text(d,(75,613),state,32,TEAL if t>=16 else FG,True)
    x=783
    metric(d,x,194,'FIRST BURN',f"+{TRANSFER_INFO['first_burn_m_s']:.2f} m/s",AMBER)
    metric(d,x,297,'TRANSFER COAST',f"{TRANSFER_INFO['coast_seconds']/60:.2f} min")
    metric(d,x,400,'CIRCULARIZING BURN',f"+{TRANSFER_INFO['second_circularizing_burn_m_s']:.2f} m/s",TEAL)
    text(d,(x,516),'Two restarts, one plane',30,FG,True)
    text(d,(x,560),'Ideal impulsive example',27,MUTED)
    text(d,(52,675),'Generic upper-stage surrogate  •  No selected rocket or provider',24,MUTED)
    return im

def scene2(t):
    im=BASE[1].copy();d=ImageDraw.Draw(im)
    host(d,260,363,1.45,burn=False)
    line(d,[(350,337),(592,337)],GRAY,8);line(d,[(350,387),(592,387)],GRAY,8)
    progress=np.clip((t-3)/13,0,1);sx=567+180*progress
    satellite(d,sx,362,TEAL,1.15)
    arrow(d,(605,362),(796,362),TEAL,5)
    text(d,(94,221),'Generic upper-stage host',30,FG,True)
    text(d,(449,255),'Relative release vector',30,TEAL,True)
    text(d,(94,466),'Host maneuver + local tangential kick',31,FG,True)
    text(d,(94,516),'Same-plane example; direction is defined.',28,MUTED)
    text(d,(94,575),'Local interface schematic • not to scale',25,MUTED)
    metric(d,866,205,'EVALUATED POINTS', '1 / 2 / 3 m/s',TEAL)
    metric(d,866,323,'3 m/s EXAMPLE',f"{CASE['current3']['inertial_kick_m_s']:.5f} m/s",TEAL)
    text(d,(866,405),'payload inertial kick',27,MUTED)
    metric(d,866,469,'FINAL HOST RECOIL','0.01671 m/s',GRAY)
    text(d,(52,675),'Source-coupled modeled finite-host mapping  •  Retained sled and recoil included',24,MUTED)
    return im

def scene3(t):
    im=BASE[2].copy();d=ImageDraw.Draw(im)
    left,right,top,bottom=93,805,225,555
    def project(radial,along):return (right+along/900*(right-left),bottom-(radial+55)/75*(bottom-top))
    for along in [0,-300,-600,-900]:
        x,_=project(0,along);line(d,[(x,top),(x,bottom)],GRID,1);text(d,(x,bottom+10),str(along),24,MUTED,anchor='mt')
    for radial in [-50,-25,0]:
        _,y=project(radial,0);line(d,[(left,y),(right,y)],GRID,1);text(d,(left-10,y),str(radial),24,MUTED,anchor='rm')
    text(d,(116,603),'Along-track difference (km)',27,MUTED)
    text(d,(103,186),'Radial difference (km)',27,MUTED)
    limit=max(1,int(np.clip((t-1)/18,0,1)*(len(TIMES)-1)))
    for ident,col,width in [('spring1',GRAY,4),('current3',TEAL,5),('preset_match',FG,1)]:
        coords=RELATIVE[ident];points=[project(r,a) for r,a in coords[:limit+1:8]]
        if len(points)>1:line(d,points,col,width)
        x,y=project(*coords[limit]);d.ellipse((x-6,y-6,x+6,y+6),fill=col)
    text(d,(851,202),'Same host state',30,FG,True)
    text(d,(851,246),'ACR1 • 3 m/s command',26,TEAL,True)
    text(d,(851,285),'Spring example • 1 m/s',26,GRAY,True)
    text(d,(851,324),'Preset spring • matched',26,FG,True)
    metric(d,851,390,'COMMON EVALUATION',f'{TIMES[limit]/3600:4.1f} h')
    text(d,(851,488),'Preset matches the',29,FG)
    text(d,(851,528),'same ideal trajectory.',29,FG)
    text(d,(52,675),'Co-rotating position difference  •  Axes scaled independently  •  Example spring speed',24,MUTED)
    return im

def scene4(t):
    im=BASE[3].copy();d=ImageDraw.Draw(im);r=CASE['current3'];cx,cy=339,390;scale=210/R
    earth(d,cx,cy,scale);orbit_circle(d,R,cx,cy,scale,GRAY,3)
    line(d,xy(curve('current3'),cx,cy,scale),TEAL,3)
    period=r['period_minutes']*60;elapsed=(t/20)*period
    index=min(len(TIMES)-1,int(elapsed/86400*(len(TIMES)-1)))
    px,py=xy([STATES['current3'][index,:2]],cx,cy,scale)[0];satellite(d,px,py,TEAL,.65)
    text(d,(74,609),'Physical orbit scale',28,MUTED)
    # Independent radial zoom: 0..one orbital period,600..612 km.
    x0,x1,y0,y1=757,1205,466,245
    for alt in [600,605,610]:
        y=y0-(alt-600)/12*(y0-y1);line(d,[(x0,y),(x1,y)],GRID,1);text(d,(x0-9,y),str(alt),24,MUTED,anchor='rm')
    mask=TIMES<=period;times=TIMES[mask];alts=np.linalg.norm(STATES['current3'][mask,:2],axis=1)/1000-RE/1000
    points=[(x0+q/period*(x1-x0),y0-(a-600)/12*(y0-y1)) for q,a in zip(times,alts)]
    line(d,points,TEAL,4)
    alt=np.linalg.norm(STATES['current3'][index,:2])/1000-RE/1000
    x=x0+elapsed/period*(x1-x0);y=y0-(alt-600)/12*(y0-y1);d.ellipse((x-6,y-6,x+6,y+6),fill=FG)
    text(d,(757,190),'Altitude zoom (km)',30,FG,True)
    text(d,(757,486),'0',24,MUTED);text(d,(1109,486),'96.80 min',24,MUTED)
    text(d,(743,550),'600.00 × 610.82 km',33,TEAL,True)
    text(d,(743,592),'Ellipse • not a higher circle',28,FG)
    text(d,(52,675),f"Coast follows the ellipse  •  Circularization at apogee needs another +{r['extra_prograde_burn_at_apogee_to_circularize_m_s']:.3f} m/s burn",24,MUTED)
    return im

def scene5(t):
    im=BASE[4].copy();d=ImageDraw.Draw(im)
    ids=['illustrative_low','current3','historical16','future1000','future3500'];i=min(4,int(t/4));ident=ids[i];r=CASE[ident]
    colors=[GRAY,TEAL,GRAY,AMBER,AMBER];col=colors[i];local=(t%4)/4
    labels=[('0.2 m/s','Illustrative low-speed case','Outside evaluated 1–3 m/s'),
            ('3 m/s command','Current ACR1 example','Evaluated points: 1 / 2 / 3 m/s'),
            ('≈16 m/s','Historical periodic model','Not a current hardware rating'),
            ('1 km/s','Future kinematic research','Distinct hardware study required'),
            ('3.5 km/s','Beyond: escape branch','Positive orbital energy')]
    speed,title,bound=labels[i]
    points=curve(ident);maxr=max(np.linalg.norm(points,axis=1));scale=208/maxr;cx,cy=379,425
    earth(d,cx,cy,scale);line(d,xy(points,cx,cy,scale),col,3)
    target_time=(r['period_minutes']*60 if r['period_minutes'] is not None else 7200)*local
    n=min(len(TIMES)-1,int(target_time/86400*(len(TIMES)-1)));px,py=xy([STATES[ident][n,:2]],cx,cy,scale)[0]
    d.ellipse((px-6,py-6,px+6,py+6),fill=FG)
    text(d,(58,185),title,32,col,True)
    text(d,(780,608),'Orbit view • scale adapts',24,MUTED)
    x=780;text(d,(x,190),speed,43,col,True)
    text(d,(x,249),bound,25,MUTED)
    metric(d,x,310,'PERIGEE / APOGEE',f"600 / {r['apogee_altitude_km']:.1f} km" if r['apogee_altitude_km'] is not None else '600 km / unbound',col)
    metric(d,x,411,'ORBITAL PERIOD',f"{r['period_minutes']:.2f} min" if r['period_minutes'] is not None else 'No closed period')
    metric(d,x,512,'24 h PHASE (WRAPPED)',f"{r['phase_24h_wrapped_deg']:+.2f}°")
    text(d,(52,675),'Speed cases are separate  •  Future scenes depict kinematics, never current rail performance',24,MUTED)
    return im

SCENES=[scene1,scene2,scene3,scene4,scene5]
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--only',default='1,2,3,4,5');args=parser.parse_args()
    selected={int(x)-1 for x in args.only.split(',')}
    clips=H/'segments';clips.mkdir(exist_ok=True)
    posters=[]
    for j,fn in enumerate(SCENES):
        if j not in selected:continue
        output=clips/f'{j+1:02d}_orbit_chapter.mp4'
        command=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{HEIGHT}','-r',str(FPS),'-i','-',
                 '-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(output)]
        process=subprocess.Popen(command,stdin=subprocess.PIPE,stderr=(clips/f'{j+1:02d}_encode.log').open('w'))
        for index in range(DURATION*FPS):
            image=fn(index/FPS)
            # Subtle chapter seam; all intermediate animation remains native24fps.
            fade=min(1,index/6,(DURATION*FPS-1-index)/6)
            if fade<1:image=Image.blend(Image.new('RGB',(W,HEIGHT),BG),image,max(0,fade))
            process.stdin.write(image.tobytes())
            if index==8*FPS:
                image.save(clips/f'{j+1:02d}_poster.png')
        process.stdin.close();assert process.wait()==0
        print('Rendered',output.name,flush=True)
    (H/'concat.txt').write_text(''.join(f"file 'segments/{j+1:02d}_orbit_chapter.mp4'\n" for j in range(5)))
    subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(H/'concat.txt'),'-c','copy','-movflags','+faststart',str(H/'VOLLEY_orbit_comparison_100s.mp4')],check=True)
    posters=[Image.open(clips/f'{j+1:02d}_poster.png').convert('RGB') for j in range(5)]
    posters[0].save(H/'POSTER.png')
    sheet=Image.new('RGB',(1280,3*400),BG);d=ImageDraw.Draw(sheet)
    for j,p in enumerate(posters):
        thumb=p.resize((640,360),Image.Resampling.LANCZOS);x=(j%2)*640;y=(j//2)*400;sheet.paste(thumb,(x,y))
        text(d,(x+20,y+365),f'{j*20:02d}–{(j+1)*20:02d} s  /  Chapter {j+1}',22,MUTED)
    sheet.save(H/'CONTACT_SHEET.jpg',quality=94)
    print('PASS:5×20s segments;100s MP4;native1280×720/24fps;CRF20;no audio',flush=True)

P=json.loads((H/'PHYSICS_RESULTS.json').read_text());CASE={r['id']:r for r in P['cases']}
ARCHIVE=np.load(H/'TRAJECTORIES.npz');TIMES=ARCHIVE['times_s'];STATES={k:ARCHIVE[k] for k in CASE}
TRANSFER=ARCHIVE['transfer_states'];TRANSFER_INFO=P['host_transfer'];RE=P['constants']['reference_radius_m'];R=RE+600000
RELATIVE={}
theta=np.sqrt(P['constants']['mu_Earth_m3_s2']/R**3)*TIMES
for ident in ['spring1','current3','preset_match']:
    positions=STATES[ident][:,:2]
    radial=(positions[:,0]*np.cos(theta)+positions[:,1]*np.sin(theta)-R)/1000
    along=(-positions[:,0]*np.sin(theta)+positions[:,1]*np.cos(theta))/1000
    RELATIVE[ident]=np.c_[radial,along]
BASE=[frame_base(1,'First, move the carrier','The host supplies the large orbital change.'),
      frame_base(2,'Then, set the relative release','VOLLEY changes the local release vector; the host supplies maneuver authority.'),
      frame_base(3,'Compare the complete delivery policy','Same circular starting state, same plane, same 24-hour evaluation.'),
      frame_base(4,'A tangential kick creates an ellipse','Coasting and circularizing are different operations.'),
      frame_base(5,'Keep the speed cases distinct','Current evidence, historical models and future kinematics have separate roles.')]
if __name__=='__main__':main()
