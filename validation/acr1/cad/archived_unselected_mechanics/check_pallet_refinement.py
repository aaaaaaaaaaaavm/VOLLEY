"""Transient check of final material/lock refinements; controlled files are unchanged."""
from pathlib import Path
import build_acr1 as b,cradle_acr1
s=Path(b.__file__).read_text().replace('cyl(6.9,80,x,-90,-35)','cyl(3.1,80,x,-90,-35)').replace('lift=(26 if pallet_locked else 0)','lift=(12 if pallet_locked else 0)').replace('start=-6+lift','start=8+lift')
exec(compile(s,b.__file__,'exec'),b.__dict__)
s=Path(cradle_acr1.__file__).read_text().replace('box(20,20,14,x-10,-10,floor-12)','box(20,20,11.5,x-10,-10,floor-12)')
exec(compile(s,cradle_acr1.__file__,'exec'),cradle_acr1.__dict__)
pallet=b.pallet(46);cr=b.cradle(46,False);sat=b.payload('SAT',b.XA,0,46)
for stroke,turn in [(0,0),(4,0),(8,0),(12,0),(12,30),(12,60),(12,90)]:
 print('LOCK',stroke,turn,'HITS',len(b.audit(b.sled(200,False,pallet_locked=False,pallet_lock_lift=stroke,pallet_lock_turn=turn)+pallet+cr+[sat])['interferences']),flush=True)
carrier=b.sled(1500,False)+b.pallet(46,1500)
for travel in [0,25,50,75,90,100,110,125,150,250,400,600]:
 sat=b.payload('Escaping_3U',1564+travel,0,46)
 print('ESCAPE',travel,'HITS',len(b.audit(carrier+[sat],{sat['name']})['interferences']),flush=True)
