#!/usr/bin/env python3
"""Execute partial occupancy using the accepted finite-force solver and frozen targets."""
from concurrent.futures import ProcessPoolExecutor,as_completed
import hashlib,importlib.util,json,os,platform,sys,time
from pathlib import Path
import numpy,scipy
H=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('partial_mission',H/'model/mission_model.py')
model=importlib.util.module_from_spec(spec);spec.loader.exec_module(model)
TARGETS=json.loads((H/'model/TARGETS.json').read_text())

def worker(job):
    n,family,arch,fraction,narrow=job
    case={**TARGETS['families'][family], 'name':f'n{n}_{family}', 'shots':TARGETS['families'][family]['shots'][:n]}
    result=model.run(case,arch,fraction=fraction,step=60.,shared_narrow=narrow)
    model.export_case(result,H/'model/release'/(result['case_stem']+'.csv'))
    return {k:v for k,v in result.items() if k not in ['events','legs','deliveries']}

def main():
    jobs=[];defs=[]
    for n in [2,4]:
        for family in TARGETS['families']:
            defs.append(dict(payload_count=n,family=family,epoch=TARGETS['epoch_TAI'],
                initial_PV=TARGETS['initial_PV'],release_slots_s=TARGETS['release_times_s'][:n],
                evaluation_s=TARGETS['final_epoch_s'],shots=TARGETS['families'][family]['shots'][:n],
                host_target=TARGETS['families'][family]['host_target'],
                device_mass_boundary='Full unchanged twelve-cell ACR1 dry mass and full twelve-slot 72 kg spring proxy retained for every occupancy.'))
            for arch in ['gen5','spring_fixed2','spring_pretrim']:
                for fraction,narrow in ([(.35,True)] if arch=='gen5' else [(.35,True),(.35,False),(.45,False)]):
                    jobs.append((n,family,arch,fraction,narrow))
    (H/'CASE_DEFINITIONS.json').write_text(json.dumps(dict(study='ACR1-PARTIAL-OCCUPANCY-01',definitions=defs),indent=2)+'\n')
    (H/'model/CALIBRATION.json').write_text(json.dumps(model.CALIBRATION,indent=2)+'\n')
    rows=[]
    with ProcessPoolExecutor(max_workers=2) as pool:
        for f in as_completed([pool.submit(worker,j) for j in jobs]):rows.append(f.result())
    rows.sort(key=lambda x:x['case_stem'])
    (H/'SUMMARY.json').write_text(json.dumps(dict(study='ACR1-PARTIAL-OCCUPANCY-01',
        description='Executed same-size 3U partial occupancy, not mixed-size Gen6 or provider compatibility',
        runtime=dict(python=platform.python_version(),numpy=numpy.__version__,scipy=scipy.__version__),
        cases=rows,solver_thresholds=dict(targeting_position_m=.001,targeting_velocity_m_s=1e-6),
        common_evaluation_s=91800,force_limits_N=[1,5],fuel_budget_kg=20,
        source_pins=json.loads((H/'SOURCE_IDENTITIES.json').read_text())),indent=2)+'\n')
    print('Completed actual finite-force candidates:',len(rows),flush=True)

if __name__=='__main__':main()
