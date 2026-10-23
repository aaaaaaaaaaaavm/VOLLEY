"""Reconcile represented moving material against the declared actuator studies."""
from pathlib import Path
import argparse,csv,hashlib,json

H=Path(__file__).resolve().parent

def main(four_report,feed_csv):
    r=json.loads(Path(four_report).read_text())
    out=[]
    for cid in ('CellA_1U','CellB_3U','CellC_1U','CellD_3U'):
        mass=sum(q['material_mass_kg'] for q in r['BOM'] if q['name'].startswith(cid+'__') and q['role'] in ('moving','moving_gate','moving_latch'))
        out.append(dict(cell=cid,represented_moving_custom_material_kg=mass,
            assumed_upper_payload_kg=6.,represented_plus_upper_payload_kg=mass+6.,
            actuator_moving_mass_study_kg=7.5,
            unallocated_headroom_to_study_mass_kg=7.5-mass-6.,
            complete_moving_installed_mass_accepted=False))
    receiver=sum(q['material_mass_kg'] for q in r['BOM'] if q['name'].startswith('Receiver__'))
    rows=list(csv.DictReader(Path(feed_csv).open()));v=max(abs(float(q['speed_mm_s']))/1000 for q in rows)
    result=dict(study='MMF-01 represented moving-mass and feed-energy flowdown',
        sources={Path(p).name:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in (four_report,feed_csv)},
        cell_subtotals=out,
        receiver=dict(represented_custom_material_kg=receiver,assumed_upper_payload_kg=6.,
            represented_plus_upper_payload_kg=receiver+6.,actuator_moving_mass_study_kg=10.,
            unallocated_headroom_to_study_mass_kg=10.-receiver-6.,complete_moving_installed_mass_accepted=False),
        coast_feed_energy=dict(prescribed_pusher_peak_speed_m_s=v,assumed_payload_upper_mass_kg=6.,
            ideal_payload_kinetic_energy_at_that_speed_J=.5*6*v*v,
            boundary='Conditionalenergyrequirementonly;noguaranteedpayloaddeceleration,contactpeak,coefficientofrestitutionorendstopacceptance'),
        limitations=['Gate/captureactuators,harness,fastenersandunmodeledmovinghardwaremustfitheadroomoractuatormodelrerun',
            '6kgisstatedpayloadupperstudy,notcustomerapproval','Pushercannotpull;zeroforcecoastandfarstopcontainmentrequired',
            'Idealkinematicenergydoesnotboundactualimpactunderunmodeleddisturbance,overspeedorcontinueddriveforce'])
    assert all(x['unallocated_headroom_to_study_mass_kg']>0 for x in out)
    assert result['receiver']['unallocated_headroom_to_study_mass_kg']>0
    (H/'MOVING_MASS_FLOWDOWN.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS representedmovingmaterial+6kgpayloadbelowdeclared7.5/10kgstudymasses;completeinstalledmovingmassnotaccepted')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--four-report',required=True);p.add_argument('--feed-csv',required=True);a=p.parse_args();main(a.four_report,a.feed_csv)
