"""Nominal component STEP/native exports from the selected controlled builder."""
import json,hashlib
from pathlib import Path
import build_selected as b
out=b.O; details=[]
pp=b.cell('3U',0,False,False)
want=['Driven_pusher_frame','SPT10x2M_screw_nominal','SB3700_nut_nominal','Guide_bush_-20','Storage_gate','Restraint_pin_-92']
for q in pp:
 if q['name']not in want:continue
 details.append(b.export('FM08_R3_part_'+q['name'].replace('-','m'),[q]))
for q in b.receiver(0,'3U',True,False):
 if q['name']not in ['Floor_carriage','leading_corner_stop','1U_retractable_aft_stop']:continue
 details.append(b.export('FM08_R3_part_receiver_'+q['name'],[q]))
(out/'PART_INDEX.json').write_text(json.dumps({'revision':b.REV,'builder_sha256':hashlib.sha256(Path(b.__file__).read_bytes()).hexdigest(),'parts':details,'scope':'Nominal geometric component references;thread/race/fit/fastener details are not a manufacturing release'},indent=2)+'\n')
print('PARTS',len(details),flush=True)
