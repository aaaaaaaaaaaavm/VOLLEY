"""Compose CAD-render captions and source-target markers outside the Blender scene."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'publication';OUT.mkdir(exist_ok=True)
fontfile='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
boldfile='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font=lambda size,bold=False:ImageFont.truetype(boldfile if bold else fontfile,size)
ivory='#f2f1eb';ink='#283339';muted='#5c6669';teal='#128f8a'
records=json.loads((ROOT/'POLISH_PROVENANCE.json').read_text())
shutil.copyfile(ROOT/'assembly_hero.png',OUT/'assembly_hero.png')
raw=Image.open(ROOT/'feeder_detail.png').convert('RGB')
card=Image.new('RGB',(1800,1650),ivory);card.paste(raw,(0,120));draw=ImageDraw.Draw(card)
draw.text((64,26),'GUIDED FEED / SOUTH BANK · LEVEL 5',font=font(32,True),fill=ink)
draw.text((64,72),'CAD-derived subassembly · payload envelope and fixed channel frame hidden',font=font(23),fill=muted)
view=next(v for v in records['views'] if v['id']=='feeder_detail')
for key,row in view['editorial_targets'].items():
 u,v=row['projected_uv'];x=int(u*raw.width);y=int((1-v)*raw.height)+120;r=24
 draw.ellipse((x-r,y-r,x+r,y+r),fill=ivory,outline=teal,width=3)
 draw.text((x,y),key,font=font(25,True),fill=teal,anchor='mm')
for i,label in enumerate(['10 × 2 lead-screw reference','Motor / gear + brake references','Guided pusher frame','Guide shaft']):
 x=64+(i%2)*860;y=1500+(i//2)*58
 draw.text((x,y),str(i+1).zfill(2),font=font(26,True),fill=teal)
 draw.text((x+58,y),label,font=font(25),fill=ink)
card.save(OUT/'feeder_detail_annotated.png')
board=Image.new('RGB',(2000,900),ivory);draw=ImageDraw.Draw(board)
draw.text((64,35),'ONE CAPTIVE PALLET. CONTROLLED CUSTODY.',font=font(40,True),fill=ink)
draw.text((64,96),'Four frozen CAD poses · the payload changes holder before launch',font=font(25),fill=muted)
items=[('sequence_01_home','01  HOME','Payload stored; pallet at carrier.'),('sequence_02_captured','02  CAPTURED','Payload and pallet held by lift.'),('sequence_03_handoff','03  HANDOFF','Receiving capture established.'),('sequence_04_clear','04  CLEAR','Lift raised; pallet stays locked.')]
for i,(filename,title,caption) in enumerate(items):
 x=64+i*476
 image=Image.open(ROOT/(filename+'.png')).convert('RGB');image=image.resize((444,518),Image.Resampling.LANCZOS);board.paste(image,(x,160))
 draw.text((x,702),title,font=font(27,True),fill=teal)
 draw.text((x,748),caption,font=font(20),fill=ink)
draw.text((64,824),'Focused view: other storage cells and host ladder hidden; distant rail cropped. No hardware geometry or pose edits.',font=font(22),fill=muted)
board.save(OUT/'operating_sequence.png')
for name in ['assembly_hero.png','feeder_detail_annotated.png','operating_sequence.png']:
 image=Image.open(OUT/name);image.save(OUT/(Path(name).stem+'.webp'),quality=94,method=6)
print(json.dumps({p.name:{'pixels':Image.open(p).size,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in OUT.iterdir() if p.suffix in ['.png','.webp']},indent=2))
