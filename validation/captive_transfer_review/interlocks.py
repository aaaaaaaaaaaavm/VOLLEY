"""Executable custody/sequence requirements with deliberate counterexamples.

Physical gate positions are assumed observable; this checks a controller model,
not a verified electrical design or real sensor fault coverage.
"""
from pathlib import Path
import hashlib,json,itertools
from geometry import REVISION,State,cycle

H=Path(__file__).resolve().parent;O=H/"release"


def permits(action,s,external_support=False,path_proved=True):
    seated=abs(s.payload_feed-200)<1e-9
    receiver=seated and s.receiver_lift==0
    fork_captive=s.front_lift==0 and abs(s.feed-s.payload_feed)<1e-9
    if action=="open_storage":return fork_captive and s.feed==0
    if action=="transfer":return fork_captive and s.storage_lift==120 and s.receiver_lift==120 and path_proved
    if action=="receiver_capture":return seated and s.feed==200 and fork_captive
    if action=="open_fork_front":return receiver and s.feed==200
    if action=="fork_return":return receiver and s.front_lift==105
    if action=="close_storage":return s.feed==0 and receiver
    if action=="reset_fork_front":return s.feed==0 and receiver
    if action=="release_receiver":return s.feed==0 and external_support and path_proved
    if action=="external_departure_surrogate":return external_support and s.receiver_lift==120 and path_proved
    if action=="empty_receiver_reset":return s.payload_exit>0
    raise ValueError(action)


def run():
    phases=cycle(340.5);nominal=[];faults=[]
    for (old,s),(action,next_s) in zip(phases,phases[1:]):
        # External custody is a required unimplemented hardware interface.
        ext=action in ["release_receiver","external_departure_surrogate"]
        assert permits(action,s,ext)
        nominal.append(dict(action=action,allowed=True,external_support_required=ext))
    # Evaluate all combinations of the prerequisites for the dangerous transitions.
    for feed,payload,front,receiver,path,ext in itertools.product([0,100,200],[0,100,200],[0,105],[0,120],[False,True],[False,True]):
        s=State(feed=feed,payload_feed=payload,front_lift=front,receiver_lift=receiver,storage_lift=120)
        for action in ["open_fork_front","fork_return","release_receiver"]:
            allowed=permits(action,s,ext,path)
            safe={"open_fork_front":payload==200 and receiver==0 and feed==200,
                  "fork_return":payload==200 and receiver==0 and front==105,
                  "release_receiver":feed==0 and ext and path}[action]
            assert not allowed or safe
            faults.append(dict(action=action,feed_mm=feed,payload_feed_mm=payload,front_mm=front,receiver_mm=receiver,path_proved=path,external_custody=ext,allowed=allowed))
    # A false indication can defeat the modeled guard. Preserve, do not suppress.
    real=State(feed=200,payload_feed=200,receiver_lift=120,storage_lift=120)
    indicated=State(feed=200,payload_feed=200,receiver_lift=0,storage_lift=120)
    assert not permits("open_fork_front",real) and permits("open_fork_front",indicated)
    # Clear proof reset: a jam invalidates the shared path, regardless of cell number.
    jammed=State(storage_lift=120)
    assert not permits("transfer",jammed,path_proved=False)
    d=dict(revision=REVISION,nominal=nominal,guard_cases=faults,
       counterexamples=[dict(fault="False receiver-locked indication",consequence="Controller can open fork before actual receiver capture",required="Independent physical retention verification, sensor diagnostics and common-cause analysis"),
        dict(fault="Power loss while storage gate is straddled",consequence="Uncontrolled gate closure can strike payload",required="Mechanical hold-open interlock or independently rated holding actuator"),
        dict(fault="Receiver unlock without real sled custody",consequence="Nominal geometric clearance does not provide continuous load restraint",required="Implement and verify actual receiver-to-sled custody interface")],
       blocked_other_cells_until_safe_path=True,
       boundary="Exhaustive finite prerequisite combinations, not proof of complete hardware reliability, real sensor truth, latencies or mechanical holding.",
       source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (O/"INTERLOCKS.json").write_text(json.dumps(d,indent=2)+"\n")
    print(len(faults),"guard combinations;3 physical counterexamples retained")
    return d


if __name__=="__main__":run()
