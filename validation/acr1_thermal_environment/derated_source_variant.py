"""Run the unchanged ACR1 production equations with explicit derating inputs.

The original source file is copied byte-for-byte. An audited AST adapter exposes
only its two initial-voltage literals and regenerative-limit literal as inputs;
restoring those three literals must reproduce the complete original AST exactly.
No equation,current/stroke/force/timing/energy gate ororiginal capture is edited.
"""
import ast
import copy
import hashlib
import json
import tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class VoltageParameters(ast.NodeTransformer):
    def __init__(self):self.in_simulate=False;self.changes=[]
    def visit_FunctionDef(self,node):
        previous=self.in_simulate;self.in_simulate=node.name=='simulate';result=self.generic_visit(node);self.in_simulate=previous;return result
    def visit_Constant(self,node):
        if self.in_simulate and isinstance(node.value,float) and node.value in [86.4,2.9]:
            name='THERMAL_INITIAL_BANK_V' if node.value==86.4 else 'THERMAL_REGEN_CELL_V'
            self.changes.append(dict(line=node.lineno,original_literal=node.value,parameter=name))
            return ast.copy_location(ast.Name(id=name,ctx=ast.Load()),node)
        return node


class RestoreParameters(ast.NodeTransformer):
    def visit_Name(self,node):
        values=dict(THERMAL_INITIAL_BANK_V=86.4,THERMAL_REGEN_CELL_V=2.9)
        return ast.copy_location(ast.Constant(value=values[node.id]),node) if node.id in values else node


def main():
    source=HERE/'inputs/coupled_shot_production.py';original=source.read_text();tree=ast.parse(original);parameterize=VoltageParameters();adapted=parameterize.visit(copy.deepcopy(tree));ast.fix_missing_locations(adapted)
    assert len(parameterize.changes)==3
    restored=RestoreParameters().visit(copy.deepcopy(adapted))
    same=ast.dump(tree,include_attributes=False)==ast.dump(restored,include_attributes=False);assert same
    out=HERE/'derated_source';out.mkdir(exist_ok=True)
    scratch_inputs={
      'cad/release/VOLLEY_G5_ACR1_home.json':'VOLLEY_G5_ACR1_home.json',
      'analysis/FINITE_MOTOR.json':'FINITE_MOTOR.json',
      'analysis/ARREST_FORCE_MAP.json':'ARREST_FORCE_MAP.json',
      'analysis/conduction/phase_A/h2/RESULT.json':'CONDUCTION_PHASE_A.json'}
    with tempfile.TemporaryDirectory(prefix='volley-acr1-derated-source-') as tmp:
        root=Path(tmp);script=root/'analysis/coupled_shot.py';script.parent.mkdir();script.write_bytes(source.read_bytes())
        for target,name in scratch_inputs.items():
            dest=root/target;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((HERE/'inputs'/name).read_bytes())
        scope=dict(__name__='captured_acr1_voltage_variant',__file__=str(script),THERMAL_INITIAL_BANK_V=78.4,THERMAL_REGEN_CELL_V=2.47)
        exec(compile(adapted,str(script),'exec'),scope)
        moving,dry,xs,ks,resistance,hashes=scope['inputs']();cases=[]
        for command in [1,2,3]:
            for adverse in [False,True]:
                for inductance in [3e-6,20e-6,100e-6]:
                    row=scope['simulate'](command,moving,dry,xs,ks,resistance,adverse,inductance,trace=False)
                    row['derated_catalogue_checks']=dict(cell_maximum_2p5V=row['maximum_cell_terminal_or_internal_V']<=2.5,
                                                        regenerative_control_2p47V=row['maximum_cell_terminal_or_internal_V']<=2.47+1e-10)
                    row['all_derated_checks_pass']=row['all_declared_checks_pass'] and all(row['derated_catalogue_checks'].values())
                    cases.append(row)
                    print(command,adverse,inductance,row['status'],row['all_derated_checks_pass'],row['maximum_cell_terminal_or_internal_V'],flush=True)
        assert sha(script)==sha(source)
    nominal_headroom=.5*6.25*(80**2-78.4**2);adverse_headroom=.5*(6.25*.9*.7)*(80**2-78.4**2)
    protection_headroom=.5*(6.25*.9*.7)*(79.04**2-78.4**2)
    inductive_gate=.75*100e-6*600**2;mechanical_arrest=.5*moving*3**2
    result=dict(study='ACR1-SOURCE-DERATED-78P4-01',configuration='Separatelyidentified hot-temperaturecandidate,not a revision to frozenACR1',
                original_source_sha256=sha(source),adapter_sha256=sha(__file__),original_AST_restored_identically=same,
                runtime_parameter_accesses=parameterize.changes,initial_bank_V=78.4,series_groups=32,initial_cell_command_V=2.45,
                regenerative_control_bank_V=79.04,regenerative_control_cell_V=2.47,absolute_catalogue_bank_V=80,absolute_catalogue_cell_V=2.5,
                catalogue_max_temperature_C=85,production_current_and_stroke_and_energy_gates_unchanged=True,
                source_input_sha256=hashes,source_scratch_input_sha256={name:sha(HERE/'inputs'/name) for name in scratch_inputs.values()},
                cases=cases,all18supported_cases_pass=all(x['all_derated_checks_pass'] for x in cases),
                initial_to_absolute_bank_energy_headroom_J=dict(nominal=nominal_headroom,adverse=adverse_headroom),
                adverse_initial_to_regen_control_energy_headroom_J=protection_headroom,
                maximum_inductance_current_gate_energy_J=inductive_gate,nominal3mps_retained_sled_kinetic_arrest_energy_J=mechanical_arrest,
                headroom_scope='Storedenergybound only,not a substitute forinstantaneous terminalvoltage/current/regeneration tests.600A/100uH and3m/s energy bounds are compared conservatively.',
                per_group_30mV_maximum_allowance_budget_V=dict(cell_group_imbalance=.01,voltage_sensing_error=.005,control_latency_and_overshoot=.005,unresolved_fast_interconnect_transient=.01),
                sensing_and_charge_requirements=['2.45V/group initial charge command;2.47V/group regenerative command ceiling;2.5V/group catalogue absolute at85C.',
                  'The30mV/group allowance budget mustbeverified per32parallelgroup,not from bankaverage. Values are design allocations,not measured accuracy.',
                  'Temperature inhibit mustaccount forsensor error andhottest-cell/package gradient below85C; no65C/85C flightqualification is implied.',
                  'Balancing,cellC/ESR variation,lead inductance,switching overshoot,delay,reset andfault current mustbemeasured onthe actualcircuit.'],
                no_baseline_source_or_capture_modified=True)
    (HERE/'DERATED_SOURCE_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    (out/'PARAMETER_ADAPTER_RECORD.json').write_text(json.dumps({k:result[k] for k in ['original_source_sha256','adapter_sha256','original_AST_restored_identically','runtime_parameter_accesses','initial_bank_V','regenerative_control_bank_V','absolute_catalogue_bank_V']},indent=2)+'\n')
    print(json.dumps(dict(all18pass=result['all18supported_cases_pass'],nominal_headroom_J=nominal_headroom,adverse_headroom_J=adverse_headroom,adverse_control_headroom_J=protection_headroom),indent=2))


if __name__=='__main__':main()
