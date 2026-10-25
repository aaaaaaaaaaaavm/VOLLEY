#!/usr/bin/env python3
"""Verify N5 pre-test packet/source identities; performs no experiment."""
from pathlib import Path
import csv,hashlib,json,math,re,sys
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[1]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    manifest=json.loads((ROOT/'MANIFEST.json').read_text());lock=json.loads((ROOT/'SPEC_LOCK.json').read_text());sources=json.loads((ROOT/'SOURCE_IDENTITIES.json').read_text())
    checked=0
    for name,h in manifest['files'].items():
        p=(ROOT/name).resolve();assert p.is_relative_to(ROOT) and p.is_file() and digest(p)==h,name;checked+=1
    for name,h in lock['pretest_files'].items():assert digest(ROOT/name)==h,name
    for row in sources['records']:assert digest(REPO/row['path'])==row['sha256'],row['path']
    d=json.loads((ROOT/'DEFINITION.json').read_text());a=json.loads((ROOT/'ACCEPTANCE_R1.json').read_text());p=json.loads((ROOT/'PREDICTIONS.json').read_text());g=json.loads((ROOT/'geometry/GEOMETRY_CHECK.json').read_text())
    assert not d['experiments_performed'] and not a['experiments_performed'] and p['prediction_only'] and p['measurements'] is None
    assert p['definition_sha256']==digest(ROOT/'DEFINITION.json') and p['model_sha256']==digest(ROOT/'predict.py')
    assert g['definition_sha256']==digest(ROOT/'DEFINITION.json') and g['builder_sha256']==digest(ROOT/'build_fixture.py')
    assert g['STEP_sha256']==digest(ROOT/'geometry/C01_coupon_fixture.step')
    step=(ROOT/'geometry/C01_coupon_fixture.step').read_bytes();assert step.startswith(b'ISO-10303-21;') and b'END-ISO-10303-21;' in step[-1024:]
    assert len(g['parts'])==53 and all(row['valid'] and row['volume_mm3']>0 for row in g['parts'])
    assert d['coupon']['blocks_per_array']==6 and d['coupon']['block_pitch_mm']==8 and d['coupon']['active_bar_depth_mm']==80
    assert [r['x_mm'] for r in p['force_stations_frozen_before_tests']]==a['C01_force']['x_stations_mm']
    assert max(r['quadrature_change_N_per_A'] for r in p['force_scan'])<1e-6
    u=p['instrument_allocated_expanded_uncertainty'];assert u['Hall_absolute_T']<=a['C01_field']['expanded_measurement_uncertainty_max_T'] and u['force_absolute_N']<=a['C01_force']['expanded_force_uncertainty_max_N'] and u['time_of_flight_speed_m_s_at0p2']<=a['C03_ground_release']['expanded_velocity_uncertainty_max_m_s']
    gp=p['ground_counterpart'];assert gp['loaded_kinetic_energy_J']<.5 and gp['nominal_carrier_stop_m']<.21 and gp['nominal_relative_aft_coordinate_m']>.5245
    m=d['ground_release']['carrier_mass_reference_kg'];v=.2;assert math.isclose(gp['carrier_kinetic_energy_J'],m*v*v/2,abs_tol=1e-12)
    assert math.isclose(gp['nominal_relative_aft_coordinate_m'],.064+.2*6-.5*(.1/4)*6**2-m*.2**2/(2*1.5),abs_tol=1e-12)
    vmax=.205+.002;mmax=a['C03_ground_release']['carrier_mass_kg'][1]
    assert .5*(mmax+4.005)*vmax*vmax<.5 and mmax*vmax*vmax/(2*1.5)+.005<.21
    e=d['static_electrical_limits'];assert e['compliance_max_V']*e['current_max_A']*e['pulse_max_s']+e['stored_output_energy_max_J']<=e['total_accounted_energy_ceiling_J']
    assert math.isclose(p['full_reference_bank_initial_energy_J'],23328,abs_tol=1e-6)
    for rel in ['templates/raw_timeseries.csv','templates/inspection.csv']:
        with (ROOT/rel).open() as f:assert len(list(csv.reader(f)))==1,rel
    template=json.loads((ROOT/'templates/run_record.json').read_text());assert template['template_only'] and not template['experiment_performed'] and template['measured_inputs'] is None
    with (ROOT/'BOM.csv').open() as f:
        rows=list(csv.reader(f));assert all(len(r)==6 for r in rows)
    for path in ROOT.rglob('*.md'):
        for raw in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',path.read_text()):
            target=raw.split('#',1)[0]
            if target and not target.startswith(('http:','https:','mailto:')):assert (path.parent/target).exists(),(path.name,target)
    result={'package_id':d['package_id'],'result':'PASS','packet_files_checked':checked,'parent_source_identities_checked':len(sources['records']),'pretest_lock_records':len(lock['pretest_files']),'valid_provisional_geometry_solids':53,'performed_experiments':0,'data_templates_empty':True,'scope':'Preparation identities, numerical consistency and framing; no physical build/test/qualification acceptance.'}
    (ROOT/'CHECK_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':
    try:main()
    except (AssertionError,ValueError,OSError) as exc:print('FAIL: N5 packet',exc,file=sys.stderr);raise SystemExit(1)
