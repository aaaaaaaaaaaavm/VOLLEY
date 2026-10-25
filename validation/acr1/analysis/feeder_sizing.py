"""Same-configuration analytical feeder sizing; dimensions read from live CAD.

These are sizing calculations with declared environmental/resistance assumptions,
not supplier approval, assembled load testing, or a manufacturing tolerance proof.
"""
from pathlib import Path
import csv, hashlib, json, math

ROOT = Path(__file__).resolve().parents[1]
CAD = ROOT / 'cad/PARAMETERS.json'
CATALOG = ROOT/'sources/feeder_catalog_reference.json'

def calculate():
    raw_params=CAD.read_bytes();raw_catalog=CATALOG.read_bytes()
    p = json.loads(raw_params); cat = json.loads(raw_catalog)
    s = p['storage']; motor = cat['motor_basis']
    gear = cat['selected_prototype_options']['lead_screw']['gear']
    d = s['feed_stroke']/1000; duration = s['nominal_feed_time_s']
    lead = s['local_screw_lead']/1000
    # Deliberately below the catalog maximum efficiency; no vacuum efficiency claim.
    eta_screw, eta_gear, moving_mass = .42, .50, 7.5
    E = 200e9; span = s['local_guide_span']/1000
    root = s['local_screw_root_diameter']/1000
    screw_I = math.pi*root**4/64
    buckling = math.pi**2*E*screw_I/span**2
    rows=[]; summaries=[]
    for resistance in [25,50,100,155]:
        case=[]
        for i in range(1001):
            u=i/1000
            x=d*(10*u**3-15*u**4+6*u**5)
            v=d/duration*(30*u**2-60*u**3+30*u**4)
            a=d/duration**2*(60*u-180*u**2+120*u**3)
            axial=resistance+moving_mass*a
            tout=axial*lead/(2*math.pi*eta_screw)
            torque=tout/(gear['ratio']*eta_gear)
            rpm=v/lead*60*gear['ratio']
            available=motor['no_load_rpm']-motor['slope_rpm_per_mNm']*torque*1000
            case.append(dict(resistance_N=resistance,time_s=u*duration,position_mm=x*1000,
                velocity_mm_s=v*1000,acceleration_m_s2=a,axial_N=axial,
                motor_torque_Nm=torque,motor_rpm=rpm,
                torque_speed_margin_rpm=available-rpm,
                motor_current_A=motor['no_load_current_A']+torque/motor['kT_Nm_A']))
        rows.extend(case)
        peak=lambda key:max(r[key] for r in case)
        checks=dict(motor_torque=peak('motor_torque_Nm')<=motor['rated_torque_Nm'],
            torque_speed=min(r['torque_speed_margin_rpm'] for r in case)>=0,
            gear_speed=peak('motor_rpm')<=gear['input_max_rpm'],
            nut_catalog_500rpm=peak('motor_rpm')/gear['ratio']<=500 and peak('axial_N')<=310,
            buckling_factor_2=buckling/peak('axial_N')>=2)
        summaries.append(dict(resistance_N=resistance,motor_rpm_peak=peak('motor_rpm'),
            motor_torque_peak_Nm=peak('motor_torque_Nm'),motor_current_peak_A=peak('motor_current_A'),
            torque_speed_margin_rpm=min(r['torque_speed_margin_rpm'] for r in case),
            euler_factor=buckling/peak('axial_N'),checks=checks,pass_declared_screens=all(checks.values())))
    guide_d=s['local_guide_diameter']/1000; guide_I=math.pi*guide_d**4/64
    guides=[]
    # Stack values are explicit sensitivity allocations, not measured tolerances.
    yaw=p['manifest']['payload_mm'][0]/2*math.tan(math.radians(.1))
    manufacturing=.30; thermal=200*40*12e-6
    for force in [10,25,50,100]:
        defl=(force/2)*span**3/(48*E*guide_I)*1000
        remaining=s['channel_side_clearance']-manufacturing-yaw-thermal-defl
        guides.append(dict(transverse_total_N=force,deflection_mm=defl,
            allocated_manufacturing_mm=manufacturing,yaw_mm=yaw,thermal_mm=thermal,
            remaining_side_clearance_mm=remaining,positive_margin=remaining>0))
    result=dict(configuration_id=p['configuration_id'],cad_parameter_sha256=hashlib.sha256(raw_params).hexdigest(),
        model_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        catalog_sha256=hashlib.sha256(raw_catalog).hexdigest(),
        assumptions=dict(profile='quintic rest-to-rest',moving_mass_study_kg=moving_mass,
            screw_efficiency=eta_screw,gear_efficiency=eta_gear,steel_E_Pa=E,
            guide_end_condition='simply supported; equal sharing between two shafts',
            motor_catalog_environment='catalog reference, no space qualification implied'),
        stroke_mm=d*1000,duration_s=duration,screw_euler_N=buckling,
        feed_cases=summaries,guide_clearance_sensitivity=guides,
        scope_conditions=['Actual CAD pusher plus4kg payload lies within7.5kg moving-mass sizing allowance; see RESOURCE_LEDGER.json',
            'Guide clearances use declared alignment, thermal and load allocations, not manufactured measurements',
            'Integrated lift, pallet and lock geometry is verified in cad/release; lift sizing is in LIFT_SIZING.json',
            'Catalog references do not confer vacuum qualification or hardware reliability'])
    out=ROOT/'analysis'; out.mkdir(exist_ok=True)
    (out/'FEEDER_SIZING_INPUT.json').write_bytes(raw_params)
    (out/'FEEDER_SIZING.json').write_text(json.dumps(result,indent=2)+'\n')
    with (out/'FEEDER_PROFILES.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    print(json.dumps(dict(cases=summaries,guide_cases=guides),indent=2))

if __name__=='__main__': calculate()
