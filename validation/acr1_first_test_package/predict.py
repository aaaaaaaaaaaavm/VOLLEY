"""Pre-test coupon/ground-rig predictions; does not execute an experiment.

Copyright (c) 2026 Adityavardhan Mishra. Uses the frozen ACR1 field function
without writing its inputs/outputs. Coupon geometry is a separately identified case.
"""
from pathlib import Path
import copy,hashlib,importlib.util,json,math,platform
import numpy as np
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/'acr1'
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def active(field,x,depth,order):
    g,w=np.polynomial.legendre.leggauss(order)
    points=np.stack(np.meshgrid(g,g,g,indexing='ij'),-1)
    points[...,0]=x+points[...,0]*.007/2
    points[...,1]*=.006/2;points[...,2]*=depth/2
    by=field.getB(points.reshape(-1,3))[:,1].reshape((order,)*3)
    return float(-np.einsum('ijk,i,j,k->',by,w,w,w)*depth/8)
def returns(field,x,order):
    g,w=np.polynomial.legendre.leggauss(order)
    # Field axes: X travel, Y gap, Z depth; CAD axes: X travel,Y depth,Z gap.
    paths=[np.array([[x,0,.040],[x,0,.090],[x+.100,0,.090],[x+.100,0,.005]]),
           np.array([[x+.100,0,-.005],[x+.100,0,-.090],[x,0,-.090],[x,0,-.040]])]
    answer=0.
    for path in paths:
        for a,b in zip(path,path[1:]):
            delta=(b-a)/2;points=(a+b)/2+g[:,None]*delta
            answer+=float(np.sum(np.cross(delta,field.getB(points))[:,0]*w))
    return answer

def main():
    d=json.loads((ROOT/'DEFINITION.json').read_text());p=json.loads((PARENT/'cad/PARAMETERS.json').read_text())
    spec=importlib.util.spec_from_file_location('acr1_field',PARENT/'analysis/finite_motor.py');model=importlib.util.module_from_spec(spec);spec.loader.exec_module(model)
    p=copy.deepcopy(p);p['magnetic']['blocks_per_array']=d['coupon']['blocks_per_array'];field=model.make_field(p)
    field_rows=[];force_rows=[]
    for x in [-20,-12,-4,4,12,20]:
        B=field.getB([x/1000,0,0]);field_rows.append({'x_mm':x,'B_normal_T':float(B[1]),'B_vector_field_axes_T':B.tolist()})
    for x in np.arange(-24,25,4):
        a=active(field,x/1000,.080,7);r=returns(field,x/1000,21);fine=active(field,x/1000,.080,11)+returns(field,x/1000,35)
        force_rows.append({'x_mm':int(x),'active_N_per_A':a,'return_N_per_A':r,'total_N_per_A':a+r,'fine_total_N_per_A':fine,'quadrature_change_N_per_A':abs(fine-a-r)})
    chosen=[min(force_rows,key=lambda r:r['fine_total_N_per_A']),max(force_rows,key=lambda r:r['fine_total_N_per_A'])]
    # Normal attraction is a free-space Maxwell-plane screen, not fixture strength proof.
    normal=[]
    for step in [.002,.001]:
        x=np.arange(-.12,.12000001,step);z=np.arange(-.15,.15000001,step);xx,zz=np.meshgrid(x,z,indexing='ij');q=np.c_[xx.ravel(),np.zeros(xx.size),zz.ravel()]
        B=field.getB(q).reshape(xx.shape+(3,));stress=(B[...,1]**2-B[...,0]**2-B[...,2]**2)/(2*4*math.pi*1e-7)
        force=float(np.trapezoid(np.trapezoid(stress,z,axis=1),x));normal.append({'plane_step_mm':step*1000,'force_each_array_N':force})
    normal_force=normal[-1]['force_each_array_N'];load=normal_force*d['fixture']['load_sensitivity_multiplier'];E=d['fixture']['plate_E_assumed_Pa'];I=.15*.012**3/12;plate_deflection=load*.13**3/(48*E*I)
    ground=d['ground_release'];mass=ground['carrier_mass_reference_kg'];v=ground['entry_speed_reference_m_s'];payload=ground['payload_mass_reference_kg'];drag=ground['payload_support_drag_max_N'];t=ground['post_release_record_duration_s']
    stop=mass*v*v/(2*ground['allocated_external_brake_force_N'][0]);payload_x=v*t-.5*(drag/payload)*t*t
    position_B_bound=max(abs(float(field.getB([r['x_mm']/1000+dx,0,0])[1])-r['B_normal_T']) for r in field_rows for dx in [-.0001,.0001])
    U_B=2*math.sqrt((.01/math.sqrt(3))**2+(position_B_bound/math.sqrt(3))**2+(.002/math.sqrt(3))**2)
    U_force=2*math.sqrt((.0005/math.sqrt(3))**2+(.001/math.sqrt(3))**2+(.0005/math.sqrt(3))**2)
    flight_time=.2/v
    U_v=2*v*math.sqrt((.001/math.sqrt(3)/.2)**2+2*(.0001/math.sqrt(3)/flight_time)**2)
    result={'package_id':d['package_id'],'prediction_only':True,'measurements':None,'definition_sha256':digest(ROOT/'DEFINITION.json'),'model_sha256':digest(Path(__file__)),'parent_field_source_sha256':digest(PARENT/'analysis/finite_motor.py'),'parent_parameters_sha256':digest(PARENT/'cad/PARAMETERS.json'),'software':{'python':platform.python_version(),'numpy':np.__version__,'magpylib':model.magpy.__version__},'field_scan':field_rows,'force_scan':force_rows,'force_stations_frozen_before_tests':chosen,'normal_attraction_screen':normal,'fixture_screen':{'load_multiplier':2,'load_each_plate_N':load,'plate_simple_beam_deflection_mm':plate_deflection*1000,'paired_plate_closure_mm':2*plate_deflection*1000,'per_corner_compression_N':load/4,'per_small_keeper_bolt_nominal_share_N':load/12,'scope':'Equal sharing and simple beam only; no joint, lip, contact-pressure or assembled proof test.'},'ground_counterpart':{'loaded_kinetic_energy_J':.5*(mass+payload)*v*v,'carrier_kinetic_energy_J':.5*mass*v*v,'nominal_carrier_stop_m':stop,'nominal_payload_travel_6s_m':payload_x,'initial_payload_aft_relative_m':.064,'nominal_relative_aft_coordinate_m':.064+payload_x-stop,'gravity_slide_drag_at_mu0p1_N':payload*9.80665*.1,'four_rail_elastic_displacement_at26p8635N_um':26.8635/51.81686746987951},'instrument_allocated_expanded_uncertainty':{'Hall_position_equivalent_bound_T':position_B_bound,'Hall_absolute_T':U_B,'force_absolute_N':U_force,'time_of_flight_speed_m_s_at0p2':U_v,'scope':'Allocation RSS of independent rectangular error terms, k=2; not instrument calibration or model uncertainty.'},'full_reference_bank_initial_energy_J':.5*6.25*86.4**2,'limits':['One wavelength instead of seven; no inheritance of full-stator phase coefficient.','Return-wire force modeled as a line; wire routing must match; current crowding/support magnetic perturbations unmeasured.','Rig instrument limits and tolerances are pre-test allocations, not measured properties.','Ground rolling/air-bearing support changes the physical boundary and does not validate six-DOF tip-off.']}
    (ROOT/'PREDICTIONS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'chosen_force_stations':chosen,'normal_force_each_array_N':normal_force,'fixture_paired_beam_closure_mm':2*plate_deflection*1000,'ground':result['ground_counterpart'],'instrument_allocations':result['instrument_allocated_expanded_uncertainty']},indent=2))
if __name__=='__main__':main()
