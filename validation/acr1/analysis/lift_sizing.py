"""ACR1 synchronized Tr16x4 lift with selected catalog 20:1 gearbox reference."""
from pathlib import Path
import hashlib,json,math
ROOT=Path(__file__).resolve().parents[1]
CAT=ROOT/'sources/feeder_catalog_reference.json'
RATIOS=ROOT/'sources/faulhaber_ratios.txt'

def main():
    raw=(ROOT/'cad/PARAMETERS.json').read_bytes();p=json.loads(raw)
    source=(ROOT/'cad/cradle_acr1.py').read_bytes()
    cat=json.loads(CAT.read_text());motor=cat['motor_basis']
    stroke=(p['storage']['first_payload_floor_z']+5*p['storage']['level_pitch_z']-p['launch']['payload_floor_z'])/1000
    duration=120.;lead=.004;ratio=19.8;eta_screw=.42;eta_gear=.50
    # Conservative explicit study diameter; not inferred from a smooth 16mm CAD rod.
    root=.011;span=1.120;E=200e9;critical=math.pi**2*E*(math.pi*root**4/64)/span**2
    # Two stage catalog inertia upper value =195gmm2. Includes motor rotor.
    J=motor['rotor_inertia_kg_m2']+195e-9
    drag=.015 # Nm at common screw-drive output; separate adverse allowance.
    results=[]
    for moving_mass in [10,20,30]:
        for resistance in [50,100]:
            for gravity in [0,9.80665]:
                rows=[]
                for i in range(1001):
                    u=i/1000
                    v=stroke/duration*(30*u*u-60*u**3+30*u**4)
                    a=stroke/duration**2*(60*u-180*u*u+120*u**3)
                    force=resistance+moving_mass*(gravity+a)
                    tout=force*lead/(2*math.pi*eta_screw)+drag
                    alpha=a*2*math.pi*ratio/lead
                    torque=tout/(ratio*eta_gear)+J*alpha
                    rpm=v/lead*60*ratio
                    rows.append((force,torque,rpm,motor['no_load_rpm']-motor['slope_rpm_per_mNm']*torque*1000-rpm,tout))
                force=max(r[0]for r in rows);torque=max(r[1]for r in rows)
                checks={'motor_continuous_torque':torque<=motor['rated_torque_Nm'],
                    'torque_speed_margin':min(r[3]for r in rows)>=0,
                    'gear_10000rpm_limit':max(r[2]for r in rows)<=10000,
                    'gear_continuous_3Nm':max(r[4]for r in rows)<=3,
                    'screw_buckling_factor_2_equal_share':critical/(force/2)>=2}
                results.append(dict(moving_mass_study_kg=moving_mass,resistance_N=resistance,
                    gravity_m_s2=gravity,axial_force_total_peak_N=force,motor_torque_peak_Nm=torque,
                    motor_rpm_peak=max(r[2]for r in rows),torque_speed_margin_rpm=min(r[3]for r in rows),
                    current_peak_A=motor['no_load_current_A']+torque/motor['kT_Nm_A'],
                    screw_euler_factor_equal_share=critical/(force/2),
                    checks=checks,pass_declared_screens=all(checks.values())))
    out=dict(configuration_id=p['configuration_id'],CAD_parameter_sha256=hashlib.sha256(raw).hexdigest(),
        cradle_source_sha256=hashlib.sha256(source).hexdigest(),model_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        ratio_source_sha256=hashlib.sha256(RATIOS.read_bytes()).hexdigest(),
        reference=dict(motor='3242G024BX4',gear='32GPT20:1 nominal,19.8:1 exact',gear_mass_kg=.157,
            motor_mass_kg=.179,gear_body_length_mm=34.7,motor_gear_length_mm=78.9,
            sources=[cat['motor_basis']['source_url'],'https://www.faulhaber.com/fileadmin/Import/Media/EN_32GPT_FMM.pdf',
                'https://www.faulhaber.com/fileadmin/Import/Media/EN_GEARHEADS_REDUCTION_RATIOS.pdf']),
        assumptions=dict(stroke_mm=stroke*1000,time_s=duration,screw_lead_mm=lead*1000,
            root_diameter_study_mm=root*1000,supported_span_mm=span*1000,steel_E_Pa=E,
            screw_efficiency=eta_screw,gear_efficiency=eta_gear,common_output_drag_Nm=drag,
            rotor_and_gear_inertia_kg_m2=J,phase='quintic rest-to-rest',holding_brake_static_Nm=2,
            equal_load_sharing='Twin mechanically synchronized screws; skew/load imbalance requires sensitivity'),
        screw_euler_N_each=critical,cases=results,
        mass_basis='Actual cradle+pallet+payload7.573043kg is below the conservative10kg lowest sizing case. See RESOURCE_LEDGER.json;10/20/30kg cases retain allowance and load sensitivity.',
        interpretation='Coast operation is the reference. Ground gravity cases are separate handling sensitivities; a failed case is not a hidden operational rating.',
        no_claims=['Catalog space qualification','Nut load/life acceptance','Brake dynamic arrest','Measured transmission efficiency','Measured synchronization accuracy'])
    (ROOT/'analysis/LIFT_SIZING.json').write_text(json.dumps(out,indent=2)+'\n')
    (ROOT/'analysis/LIFT_SIZING_INPUT.json').write_bytes(raw)
    print(json.dumps(dict(stroke_mm=stroke*1000,peak_motor_rpm=results[0]['motor_rpm_peak'],
        coast_pass=sum(r['pass_declared_screens'] for r in results if r['gravity_m_s2']==0),
        coast_cases=sum(r['gravity_m_s2']==0 for r in results),
        ground_pass=sum(r['pass_declared_screens'] for r in results if r['gravity_m_s2']>0),
        ground_cases=sum(r['gravity_m_s2']>0 for r in results))))

if __name__=='__main__':main()
