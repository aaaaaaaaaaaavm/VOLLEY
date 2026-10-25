"""Instrument the unchanged ACR1 averaged shot function for dense replay only."""
from pathlib import Path
import hashlib, json, time
import numpy as np

HERE = Path(__file__).resolve().parent
ACR1 = HERE.parent/'acr1'
src = ACR1/'analysis/coupled_shot.py'
original = src.read_text()
before = 'if trace and n%100==0:records.append([t,x,v,current,vc,terminal,ibank,phase])'
after = 'if trace:records.append([t,x,v,current,vc,terminal,ibank,0 if phase=="ACCEL" else 1,force,1 if attached else 0])'
assert original.count(before)==1
instrumented = original.replace(before,after)
namespace = {'__name__':'acr1_instrumented_replay','__file__':str(src)}
exec(compile(instrumented,str(src),'exec'),namespace)
sled,dry,xs,ks,resistance,input_hashes = namespace['inputs']()
records=[]
for adverse in [False,True]:
    started=time.monotonic()
    result=namespace['simulate'](3,sled,dry,xs,ks,resistance,adverse,20e-6,dt=5e-6,trace=True)
    trace=np.asarray(result.pop('trace'),dtype=float)
    name='adverse' if adverse else 'nominal'
    np.savez_compressed(HERE/f'source_{name}.npz',trace=trace)
    result['dense_trace_columns']=['time_s','relative_x_m','relative_v_m_s','phase_current_A','internal_V','terminal_V','bank_A','brake_phase','net_force_N','attached_before_event']
    result['dense_trace_rows']=len(trace)
    result['wall_s']=time.monotonic()-started
    result['case']=name
    records.append(result)
    print(name,len(trace),result['release'],flush=True)
record={'configuration_id':'VOLLEY-G5-ACR1','source_sha256':hashlib.sha256(original.encode()).hexdigest(),'instrumented_sha256':hashlib.sha256(instrumented.encode()).hexdigest(),'instrumentation_change':{'before':before,'after':after},'algorithm_changed':False,'dt_s':5e-6,'inputs_sha256':input_hashes,'cases':records,'interpretation':'Force-time replay input,not closed-loop contact/source coupling. Core files unchanged.'}
(HERE/'SOURCE_REPLAY.json').write_text(json.dumps(record,indent=2)+'\n')
