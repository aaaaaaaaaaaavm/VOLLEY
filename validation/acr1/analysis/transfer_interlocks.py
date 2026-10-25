"""Executable interlock specification for the ACR1 captive cradle transfer.

Proof inputs represent independent sensor evidence; issuing a command never
creates proof. This model checks sequencing logic, not installed electronics.
"""
from dataclasses import dataclass, replace
from pathlib import Path
import hashlib, json

ROOT=Path(__file__).resolve().parents[1]
# Every transition retains a mechanical boundary while the next is established.
STEPS=[
 ('STOWED','DOCK_EMPTY_LIFT',('host_coast','sled_home','sled_empty','bank_locked','path_clear','home_pin_engaged')),
 ('EMPTY_DOCKED','GRIP_PALLET',('dock_low_a','dock_low_b','pallet_empty_a','pallet_empty_b','home_pin_engaged')),
 ('PALLET_GRIPPED','UNLOCK_SLED_PALLET',('lift_grip_a','lift_grip_b','pallet_empty_a','pallet_empty_b')),
 ('PALLET_UNLOCKED','INDEX',('sled_pins_retracted_a','sled_pins_retracted_b','lift_grip_a','lift_grip_b','host_coast')),
 ('INDEXED','DOCK_SOURCE',('level_a','level_b','cradle_closed','source_retained')),
 ('DOCKED','OPEN_CELL',('dock_a','dock_b','far_boundary_closed','source_retained','host_coast')),
 ('CELL_OPEN','FEED',('dock_a','dock_b','cradle_closed','far_boundary_closed','host_coast')),
 ('FED','CAPTURE',('seated_a','seated_b','source_boundary_held','cradle_closed')),
 ('CAPTURED','RETRACT_PUSHER',('capture_a','capture_b','lift_grip_a','lift_grip_b')),
 ('PUSHER_CLEAR','LOCK_CELL',('pusher_home_a','pusher_home_b','capture_a','capture_b')),
 ('CELL_LOCKED','LOWER',('cell_locked_a','cell_locked_b','capture_a','capture_b','lift_grip_a','lift_grip_b','host_coast')),
 ('LOWERED','SEAT_PALLET',('dock_low_a','dock_low_b','sled_home','sled_caps_open','capture_a','capture_b')),
 ('SEATED','LOCK_PALLET',('seat_load_a','seat_load_b','lift_grip_a','lift_grip_b','home_pin_engaged')),
 ('PALLET_LOCKED','CLOSE_SLED',('pallet_locked_a','pallet_locked_b','cradle_closed','sled_fore_retained')),
 ('SLED_CAPTURED','OPEN_CRADLE',('sled_capture_a','sled_capture_b','pallet_locked_a','pallet_locked_b')),
 ('CRADLE_OPEN','RELEASE_LIFT_GRIPS',('cradle_keepers_open_a','cradle_keepers_open_b','pallet_locked_a','pallet_locked_b','sled_capture_a','sled_capture_b')),
 ('GRIPS_RELEASED','RAISE_EMPTY_LIFT',('lift_grips_clear_a','lift_grips_clear_b','pallet_locked_a','pallet_locked_b','host_coast')),
 ('LIFT_CLEAR','UNLOCK_CARRIER',('cradle_clear_a','cradle_clear_b','pallet_locked_a','pallet_locked_b','sled_capture_a','sled_capture_b')),
 ('CARRIER_UNLOCKED','ARM',('carrier_pin_clear_a','carrier_pin_clear_b','cradle_clear_a','cradle_clear_b','bank_locked','source_ready','brake_ready')),
 ('ARMED','LAUNCH',('host_coast','pallet_locked_a','pallet_locked_b','cradle_clear_a','cradle_clear_b','carrier_pin_clear_a','carrier_pin_clear_b','bank_locked','source_ready','brake_ready','launch_path_clear','mission_release_window_authorized')),
 ('FIRING','CONFIRM_RELEASE',('cam_open_a','cam_open_b','departure_a','departure_b','host_coast')),
 ('RELEASED','RETURN_EMPTY',('payload_clear_a','payload_clear_b','carrier_turnaround','pallet_locked_a','pallet_locked_b','cradle_clear_a','cradle_clear_b','source_ready')),
 ('RETURNED','LOCK_HOME',('home_encoder_a','home_encoder_b','pallet_empty_a','pallet_empty_b')),
 ('HOME','COMPLETE_CYCLE',('home_pin_engaged','pallet_empty_a','pallet_empty_b','bank_locked')),
]
PHASES=[s[0] for s in STEPS]+['COMPLETE']

@dataclass(frozen=True)
class State:
    phase:str='STOWED'
    power:bool=True
    fault:bool=False
    pulse_enabled:bool=False
    isolated:bool=False

def transition(s,event,proof=None):
    proof={} if proof is None else proof
    if event in ('POWER_LOSS','JAM','SENSOR_DISAGREEMENT','TIMEOUT','HOST_BURN'):
        return replace(s,power=False if event=='POWER_LOSS' else s.power,
                       fault=True,pulse_enabled=False),True
    if event=='RESTORE_POWER':return replace(s,power=True,pulse_enabled=False),True
    if event=='ISOLATE':
        # No automatic recovery of an obstructed or unlocated payload.
        ok=s.fault and s.power and all(proof.get(k,False) for k in
            ('supervisor','payload_positively_retained','cell_locked_a','cell_locked_b',
             'common_path_clear_a','common_path_clear_b','cradle_empty_a','cradle_empty_b'))
        return (replace(s,isolated=True,pulse_enabled=False),True) if ok else (s,False)
    if s.fault or not s.power or s.isolated:return s,False
    for i,(phase,command,required) in enumerate(STEPS):
        if event==command and s.phase==phase and all(proof.get(k,False) for k in required):
            return replace(s,phase=PHASES[i+1],pulse_enabled=command=='LAUNCH'),True
    return s,False

def verify():
    records=[];states=[State()];s=states[0]
    for phase,cmd,required in STEPS:
        assert s.phase==phase
        nxt,accepted=transition(s,cmd,{k:True for k in required})
        assert accepted
        s=nxt;states.append(s)
    for s in states:
        for fault in ['POWER_LOSS','JAM','SENSOR_DISAGREEMENT','TIMEOUT','HOST_BURN']:
            stopped,accepted=transition(s,fault)
            assert accepted and stopped.fault and not stopped.pulse_enabled
            for _,cmd,required in STEPS:
                _,allowed=transition(stopped,cmd,{k:True for k in required})
                assert not allowed
            _,allowed=transition(stopped,'ISOLATE',{})
            assert not allowed
            records.append(dict(test='fault_latch_and_no_unproved_recovery',phase=s.phase,fault=fault,passed=True))
    # A release command at every earlier phase must fail even with all proof inputs.
    allproof={k:True for _,_,req in STEPS for k in req}
    for s in states:
        _,allowed=transition(s,'LAUNCH',allproof)
        assert allowed==(s.phase=='ARMED')
        records.append(dict(test='launch_phase_guard',phase=s.phase,passed=True))
    # Independent hazard requirements are intentionally not derived from STEPS.
    # They detect a safety requirement accidentally omitted from the transition table.
    hazards=['host_coast','pallet_locked_a','pallet_locked_b','cradle_clear_a',
        'cradle_clear_b','carrier_pin_clear_a','carrier_pin_clear_b','bank_locked',
        'source_ready','brake_ready','launch_path_clear','mission_release_window_authorized']
    for missing in hazards:
        proof={**allproof,missing:False}
        _,allowed=transition(State(phase='ARMED'),'LAUNCH',proof)
        assert not allowed, ('Unsafe positive launch permission',missing)
        records.append(dict(test='independent_launch_hazard',missing_proof=missing,passed=True))
    for phase,cmd,needed in [('PALLET_GRIPPED','UNLOCK_SLED_PALLET',['lift_grip_a','lift_grip_b']),
        ('CRADLE_OPEN','RELEASE_LIFT_GRIPS',['pallet_locked_a','pallet_locked_b'])]:
        for missing in needed:
            _,allowed=transition(State(phase=phase),cmd,{**allproof,missing:False})
            assert not allowed, ('Custody lost',cmd,missing)
            records.append(dict(test='capture_before_release',command=cmd,missing_proof=missing,passed=True))
    result=dict(configuration_id='VOLLEY-G5-ACR1',model_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        accepted_nominal_commands=len(STEPS),tests=len(records),all_passed=all(r['passed'] for r in records),
        records=records,scope='Captive-pallet command/proof specification. pulse_enabled is positive-launch permission; active arrest/return has its own source-aware control. No measured sensor or hardware fault coverage.',
        hardware_dependencies=['Independent position and capture proof channels with disagreement detection',
            'Normally retained storage and captive cradle during power loss',
            'Passive cam opening over carrier aft1445..1495mm and proved departure before empty return',
            'Encoder-based release window, source inhibit and brake-ready proof',
            'No continuation around a failed cell without independently proved clear common path'])
    (ROOT/'analysis/TRANSFER_INTERLOCKS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['accepted_nominal_commands','tests','all_passed']}))

if __name__=='__main__':verify()
