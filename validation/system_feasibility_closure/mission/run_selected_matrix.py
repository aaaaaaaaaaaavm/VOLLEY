"""Retarget matched campaigns against a captured partial feeder mass ledger.

Unmodeled equipment allowances are sensitivity inputs. No sum is promoted to
a verified complete installed mass. Twelve-cell coast windows conservatively
reserve the full worst-case feeder/index-return allocation.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import retarget_selected_mass as retarget

H=Path(__file__).resolve().parent


def main(four_report,twelve_report,catalog_reference):
    four=json.loads(Path(four_report).read_text())
    twelve=json.loads(Path(twelve_report).read_text())
    catalog=json.loads(Path(catalog_reference).read_text())
    cm4=four['mass_properties']['represented_material_mass_kg']
    cm12=twelve['captures'][0]['mass_properties']['represented_material_mass_kg']
    local=catalog['local']['known_hardware_mass_option_kg']
    receiver=catalog['receiver']['known_hardware_mass_option_kg']
    # The59.4:1 catalog option is the same motor/gear/controller/brake reference
    # used for the receiver. Count separately from zero-density CAD envelopes.
    ledger={4:dict(custom_material_kg=cm4,local_catalog_options_kg=4*local,
                   common_receiver_catalog_option_kg=receiver),
            12:dict(custom_material_kg=cm12,local_catalog_options_kg=12*local,
                    common_receiver_catalog_option_kg=receiver)}
    for n,v in ledger.items():
        v['represented_plus_catalog_options_kg']=sum(v.values())
        v['full_installed_mass_kg']=None
        v['not_in_ledger']=['completeLSM/coils/sled/pulsestore/inverter/chargingchain',
                           'gate/captureactuators,sensors,harness,fasteners,mounts',
                           'receiver/cell catalog mounting and environmental derating']
    jobs=[]
    for n in (4,12):
        fuel=10. if n==4 else 30.
        fraction=.35 if n==4 else .10
        jobs.append(dict(count=n,architecture='spring',device_kg=16.*n/4,
            fuel_kg=fuel,fraction=fraction,label=f'{n} / spring proxy / f={fraction:g}',allowance_kg=None))
        if n==12:
            for alternative in (.20,.35):
                jobs.append(dict(count=n,architecture='spring',device_kg=48.,fuel_kg=fuel,
                    fraction=alternative,label=f'12 / spring proxy / f={alternative:g}',allowance_kg=None))
        for allowance in (10.,25.,50.):
            jobs.append(dict(count=n,architecture='volley',
                device_kg=ledger[n]['represented_plus_catalog_options_kg']+allowance,
                fuel_kg=fuel,fraction=fraction,
                label=f'{n} / selected feeder + {allowance:g} kg allowance',allowance_kg=allowance))
    cases=[]
    for j in jobs:
        report,path=retarget.run_case(j['count'],j['architecture'],j['device_kg'],j['fuel_kg'],100.,60.,j['fraction'],5.)
        acc=max((math.sqrt(sum(z*z for z in e['force_N']))/min(e['before'][6],e['after'][6])
                 for e in report['events'] if e['kind']=='arc'),default=0.)
        coasts=[e['end_s']-e['start_s'] for e in report['events'] if e['kind']=='arc' and e['label']=='inter_window_coast']
        worst_handling=((2*20+30+30+8) if j['count']==4 else (2*77.77777777777777+30+30+8)) if j['architecture']=='volley' else None
        # The final recovery leg does not prepare another payload. Preparation
        # and each pre-release leg supply the finite coast windows counted here.
        usable=coasts[:j['count']]
        case={**j,'file':path.name,'peak_force_N':report['peak_force_N'],
              'fuel_used_kg':report['fuel_used_kg'],'fuel_remaining_kg':report['fuel_remaining_kg'],
              'feasible_in_declared_model':report['feasible_in_declared_model'],
              'max_host_acceleration_m_s2':acc,
              'assumed_feeder_allocation_s':worst_handling,
              'minimum_pre_release_interwindow_coast_s':min(usable),
              'coast_minus_feeder_allocation_s':min(usable)-worst_handling if worst_handling is not None else None,
              'feeder_allocation_fits_coast':min(usable)>=worst_handling if worst_handling is not None else None,
              'launch_charge_reset_allowance_is_not_complete':True,
              'pre_release_zero_force_guard_s':5.}
        if j['architecture']=='volley':assert case['feeder_allocation_fits_coast']
        cases.append(case)
    best_spring={}
    comparisons=[]
    for n in (4,12):
        feasible=[c for c in cases if c['count']==n and c['architecture']=='spring' and c['feasible_in_declared_model']]
        best_spring[n]=min(feasible,key=lambda c:c['fuel_used_kg']) if feasible else None
        if best_spring[n]:
            s=best_spring[n]
            for v in [c for c in cases if c['count']==n and c['architecture']=='volley']:
                saving=s['fuel_used_kg']-v['fuel_used_kg'];penalty=v['device_kg']-s['device_kg']
                comparisons.append(dict(count=n,volley_allowance_kg=v['allowance_kg'],
                    spring_reference_label=s['label'],spring_reference_fraction=s['fraction'],
                    propellant_used_saving_kg=saving,declared_device_dry_penalty_kg=penalty,
                    dry_penalty_minus_used_propellant_saving_kg=penalty-saving,
                    interpretation='Conditionalresourcecomparison;notoptimizedwetmass,costoractualinstalledsystem'))
    summary=dict(study='FBR-02 selected-feeder conditional mass and timing retarget',
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        input_identities={str(Path(p).name):hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in (four_report,twelve_report,catalog_reference)},
        mass_ledger=ledger,cases=cases,best_known_feasible_spring=best_spring,conditional_resource_comparisons=comparisons,
        assumptions=['300kgbasehost,Isp220s,J2pointmassforcefield',
          'samefullstatetargets/relativevectors/commonepochforbotharchitectures',
          'common100Nforceand10kgfour/30kgtwelvefuelstudyceilings;notproviderratings',
          'fourfraction0.35,twelveVOLLEYfraction0.10;springtwelvealso0.20/0.35sinceordinarydeployerdoesnotinheritVOLLEYhandlingtime',
          'allhave5spre-releaseand20spost-releasezeroforceguards',
          'selectedpusher/channelnominalfeedingisrestrictedtozeroforcecoast;nogeneralhostburnoverlapacceptance',
          'remainingcoastafterfeedercyclemustalsocovercharge,sledresetandmissionoperations',
          '10/25/50kgunmodeledequipmentallowancesaresensitivityinputs,notselectedinstalledhardware'],
        full_installed_system_or_mission_acceptance=False)
    (H.parent/'MISSION_RETARGET_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    print('FINISHED',len(cases),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--four-report',required=True);p.add_argument('--twelve-report',required=True);p.add_argument('--catalog-reference',required=True);a=p.parse_args()
    main(a.four_report,a.twelve_report,a.catalog_reference)
