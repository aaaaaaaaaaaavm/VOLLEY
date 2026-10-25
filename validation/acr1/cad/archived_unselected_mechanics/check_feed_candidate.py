"""Transient native diagnostic of bounded feed changes; does not mutate controlled source."""
import sys,types
from pathlib import Path
import build_acr1 as b
import cradle_acr1
source=Path(b.__file__).read_text()
source=source.replace('cyl(5,375,x,-435,gz','cyl(5,400,x,-435,gz').replace('for y in [-440,-70]:','for y in [-440,-45]:')
exec(compile(source,b.__file__,'exec'),b.__dict__)
s=Path(cradle_acr1.__file__).read_text()
s=s.replace('cy+fork_withdraw,z+4)','cy+fork_withdraw,z-26)')
s=s.replace('floor+10).cut(cyl(1.6,14,XA+u+4,cy+fork_withdraw,floor+10))','floor-28).cut(cyl(1.6,14,XA+u+4,cy+fork_withdraw,floor-28))')
s=s.replace(')+fork_withdraw,floor-2)]',')+fork_withdraw,floor-20)]')
s=s.replace('side*53.5+fork_withdraw,floor-10)','side*53.5+fork_withdraw,floor-40)')
exec(compile(s,cradle_acr1.__file__,'exec'),cradle_acr1.__dict__)
for side in [-1,1]:
 for level in [0,5]:
  for feed in [187.5,250]:
   floor=180+130*level
   p=b.cell(side,level,feed,True)+b.cradle(floor,False,0,side)
   print('CANDIDATE',side,level,feed,'HITS',len(b.audit(p)['interferences']),flush=True)
