"""Derive bounded conductance/temperature corrections and verify derated duty.

Exactly two source configurations are assessed: immutable86.4V baseline and
separately identified78.4V candidate. The thermal-interface option is an explicit
allocation to a regulated host,not an invented installed strap orqualification.
"""
import copy
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

from thermal_network import HERE,ThermalNetwork,sha


def main():
    config=json.loads((HERE/'THERMAL_INPUTS.json').read_text());hot=config['environment_cases'][-1]
    base=copy.deepcopy(config['reference_parameters']);corner=copy.deepcopy(base)
    corner.update(host_mount_conductance_W_K=.1,electronics_mount_conductance_W_K=5,cells_electronics_conductance_W_K=.02,heat_capacity_scale=.8)
    variants=json.loads((HERE/'DERATED_SOURCE_RESULTS.json').read_text())
    contexts=dict(reference_hot=base,bounded_contact_corner=corner)
    memo={};trials=[]
    def run(context,G,Th,command,variant=False,history=False):
        key=(context,round(G,10),round(Th,10),command,variant,history)
        if key in memo:return memo[key]
        p=copy.deepcopy(contexts[context]);p['electronics_direct_host_conductance_W_K']=G
        e=copy.deepcopy(hot);e['host_interface_C']=Th
        model=ThermalNetwork(config,e,p,command,source_cases=variants['cases'] if variant else None,
                             regen_cell_V=2.47 if variant else 2.9,cell_temperature_max_C=85 if variant else 65)
        result=model.run(history=history);memo[key]=result
        trials.append(dict(context=context,direct_source_host_G_W_K=G,host_interface_C=Th,command_m_s=command,
                           variant='78.4V' if variant else '86.4V',cell_max_C=result['temperature_max_C'][6]))
        return result
    def maximum(context,G,Th,variant=False):return max(run(context,G,Th,u,variant)['temperature_max_C'][6] for u in [1,3])
    boundaries=[]
    for context in contexts:
        row=dict(context=context,parameters=contexts[context],unmodified_hot_max_C=maximum(context,0,50))
        for target in [65,60]:
            hi=1.
            while maximum(context,hi,50)>target and hi<32:hi*=2
            value=brentq(lambda G:maximum(context,G,50)-target,0,hi,xtol=5e-5)
            row[f'minimum_direct_source_host_G_for_{target}C_W_K']=value
        if maximum(context,0,-20)>65:
            row['maximum_host_interface_without_direct_strap_for65C_C']=None
            row['no_strap_interface_disposition']='No65Csolution inside the declared[-20,65]C interface investigation band; no colderhost is invented.'
        else:row['maximum_host_interface_without_direct_strap_for65C_C']=brentq(lambda T:maximum(context,0,T)-65,-20,65,xtol=.001)
        boundaries.append(row)
        print(json.dumps({k:v for k,v in row.items() if k!='parameters'}),flush=True)
    allocated_G=math.ceil(max(row['minimum_direct_source_host_G_for_60C_W_K'] for row in boundaries)*2)/2
    # One concrete,measurable series-path allocation. It is not an installedCAD
    # model. Copperfoil free length is constrained by the existing0.9kg thermal
    # plate budget,with allrealized joints included in measuredG acceptance.
    k=350.;bulkG=4*allocated_G;endG=4*allocated_G;padG=16*allocated_G
    pad_k=3.;pad_t=.00025;pad_A=padG*pad_t/pad_k;pad_A=max(.0025,pad_A)
    padG=pad_k*pad_A/pad_t;ends_mass=2*pad_A*.005*2700;pad_mass=2*pad_A*pad_t*3000;fasteners=.05
    copper_budget=.9-ends_mass-pad_mass-fasteners
    assert copper_budget>0
    max_length=math.sqrt(copper_budget*k/(8960*bulkG));length=min(.05,.9*max_length)
    cross=bulkG*length/k;cu_mass=8960*cross*length
    realized=1/(1/bulkG+2/endG+2/padG)
    allocation=dict(required_measured_sourceplate_to_regulated_host_G_W_K=allocated_G,
                    allocated_copper_bulk_G_W_K=bulkG,allocated_minimum_each_end_joint_G_W_K=endG,
                    pad_thickness_m=pad_t,pad_conductivity_allocation_W_m_K=pad_k,pad_each_area_m2=pad_A,pad_each_G_W_K=padG,
                    copper_conductivity_minimum_allocation_W_m_K=k,copper_free_length_m=length,copper_cross_section_m2=cross,
                    indicative_width_m=.1,indicative_total_foil_stack_thickness_m=cross/.1,
                    copper_mass_kg=cu_mass,Al_endblocks_mass_kg=ends_mass,allocated_fasteners_mass_kg=fasteners,pad_mass_kg=pad_mass,
                    total_allocated_path_mass_kg=cu_mass+ends_mass+fasteners+pad_mass,
                    current_thermal_plate_mass_allocation_kg=.9,remaining_thermal_plate_mass_allocation_kg=.9-cu_mass-ends_mass-fasteners-pad_mass,
                    calculated_series_path_G_W_K=realized,max_free_length_if_using_all_0p9kg_budget_m=max_length,
                    acceptance_context='Bothreferencehot anddeclaredcontactcorner are evaluated withregulatedhost<=50C. RequiredinstalledpathG is measuredincludingallends/pads; othercontacts,heatcapacity andrepresentedloads remain the statedcase inputs,not an unbounded qualification.',
                    source_scope='Provisionalreallocation insideunlocated0.9kg thermalplate allowance,not a frozenCAD/BOMchange. Width,ends androuting mustbeplaced andchecked against existingmechanism/ICD.',
                    contact_basis='Padconductivity is a conservativeallocation belowNASAlisted5–6Wm-1K-1 examples. EndjointG is a requiredmeasuredvalue,not a guaranteed bolted/TIMsupplier capability.')
    corrections=[];derated=[];combined=[]
    for context in contexts:
        limit=brentq(lambda T:maximum(context,allocated_G,T)-65,-20,65,xtol=.001)
        for command in [1,3]:
            row=run(context,allocated_G,50,command,history=True);row['context']=context;row['source_variant']='86.4V_with_allocated_thermal_path';row['maximum_host_interface_for65C_C']=limit
            corrections.append(row)
            row=run(context,0,50,command,variant=True,history=True);row['context']=context;row['source_variant']='78.4V_derated_no_added_path';derated.append(row)
            row=run(context,allocated_G,50,command,variant=True,history=True);row['context']=context;row['source_variant']='78.4V_derated_with_allocated_thermal_path';combined.append(row)
    result=dict(study='ACR1-THERM-CORRECTIONS-01',source_sha256=sha(__file__),thermal_solver_sha256=sha(HERE/'thermal_network.py'),
                thermal_inputs_sha256=sha(HERE/'THERMAL_INPUTS.json'),derated_source_sha256=sha(HERE/'DERATED_SOURCE_RESULTS.json'),
                boundaries=boundaries,provisional_strap_pad_allocation=allocation,
                corrected86p4V_cases=corrections,derated78p4V_cases=derated,combined78p4V_path_cases=combined,evaluation_receipts=trials,
                temperature_monitor_allocations=dict(standard65C_band_nominal_trip_C=60,derated85C_band_nominal_trip_C=80,
                  budget_K=dict(sensor_underread=1,hottest_cell_to_sensor_gradient=2,remaining_model_and_operating_margin=2),
                  interpretation='Designallocations toverify,not actualsensoraccuracy. Actualhottestcell mustremainwithin catalogueband undermeasured errors andtransients.'),
                original86p4V_captures_unchanged=True,
                remaining_acceptance=['Actualsourcebox placement,strap/plate routing,clamp/TIMpressure,conductance andheatload capacity ofregulated host interface.',
                  'RealcapacitorC/ESR imbalance andtemperature dependence,32group voltage sensing,charge/regeneration latency andovershoot.',
                  'Vacuumcompatibility,outgassing,contact wear/bonding,thermalcycling,hottestcell gradients andactual materials/finishes.',
                  'Noalternative qualifies the wholemachine orrevises the baseline without explicit configuration acceptance.'])
    (HERE/'THERMAL_CORRECTIONS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(allocated_G=allocated_G,series_G=realized,path_mass_kg=allocation['total_allocated_path_mass_kg'],
                          corrected_caps=[x['temperature_max_C'][6] for x in corrections],derated_caps=[x['temperature_max_C'][6] for x in derated],combined_caps=[x['temperature_max_C'][6] for x in combined]),indent=2))


if __name__=='__main__':main()
