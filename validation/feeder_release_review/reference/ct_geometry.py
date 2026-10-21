"""CT-01 prescribed rectilinear feed cycle; dimensions are millimetres.

This coupon is a separate design hypothesis, not a replacement for FDR-08 or a
selected feeder. Constituent boxes describe nominal solid material; boxes with
the same name are fused into one part. Actuator internals/joints are not rated.
"""
from dataclasses import dataclass

REVISION = "CT-01-2026-10-19"


@dataclass(frozen=True)
class State:
    feed: float = 0
    storage_lift: float = 0
    receiver_lift: float = 120
    front_lift: float = 0
    payload_feed: float = 0
    payload_exit: float = 0


def cycle(length):
    return [
        ("stored_captive", State()),
        ("open_storage", State(storage_lift=120)),
        ("transfer", State(feed=200, storage_lift=120, payload_feed=200)),
        ("receiver_capture", State(feed=200, storage_lift=120, receiver_lift=0, payload_feed=200)),
        ("open_fork_front", State(feed=200, storage_lift=120, receiver_lift=0, front_lift=105, payload_feed=200)),
        ("fork_return", State(storage_lift=120, receiver_lift=0, front_lift=105, payload_feed=200)),
        ("close_storage", State(receiver_lift=0, front_lift=105, payload_feed=200)),
        ("reset_fork_front", State(receiver_lift=0, payload_feed=200)),
        ("release_receiver", State(payload_feed=200)),
        ("external_departure_surrogate", State(payload_feed=200, payload_exit=length+60)),
        ("empty_receiver_reset", State(receiver_lift=0, payload_feed=200, payload_exit=length+60)),
    ]


def boxes(length, state):
    out = []

    def add(name, dims, xyz, material="aluminium", role="fixed"):
        assert all(v > 0 for v in dims)
        out.append(dict(name=name, size=list(dims), lo=list(xyz), material=material, role=role))

    L, s = length, state
    y = -200+s.feed
    add("payload", (L,100,100), (s.payload_exit,-200+s.payload_feed,22), "payload", "payload")
    # A real through-slot admits the downward-retracting storage gate.
    add("support_floor", (L+24,117,6), (-12,-212,16))
    add("support_floor", (L+24,199,6), (-12,-87,16))
    for xx in [-12,L+3]:
        add("support_floor", (9,8,6), (xx,-95,16))
    for x in [-8,L+4]:
        add("cassette_L_"+str(x), (4,200,102), (x,-208,22))
        add("cassette_L_"+str(x), (17,200,4), (x-3,-208,124))
    add("rear_wall", (L+24,4,112), (-12,-216,22))
    # Gate is clear of the captive front barrier at the stored datum.
    add("storage_gate", (L+2,4,100), (-1,-93,22-s.storage_lift), "aluminium", "gate")
    # Two top retainers and eight corner dogs leave the central fork unobstructed.
    for x in [5,L-13]:
        add("receiver_top_"+str(x), (8,100,4), (x,0,124))
        for yy in [-2,101]:
            retract=(-20 if x==5 else 20)*s.receiver_lift/120
            add("receiver_y_dog_"+str((x,yy)), (8,1,8), (x+retract,yy,22), "steel", "receiver_lock")
    for x in [-2,L+1]:
        for yy in [10,82]:
            add("receiver_x_dog_"+str((x,yy)), (1,8,14), (x,yy,22+s.receiver_lift), "steel", "receiver_lock")
    # One connected fork body includes its guide carriage and overhead bridge.
    name = "fork_body"
    add(name, (L-40,3,109), (20,y-4,30), role="fork")
    # Rear corner lugs bound X travel without crossing the overhead cassette caps.
    add(name, (22.5,3,90), (-2.5,y-4,30), role="fork")
    add(name, (21.5,3,90), (L-20,y-4,30), role="fork")
    for x in [-2.5,L+1.5]:
        add(name, (1,9,90), (x,y-4,30), role="fork")
    # Top members occupy different X bands from the receiver retainers.
    for x in [25,L-33]:
        add(name, (8,104,4), (x,y-4,124), role="fork")
    add(name, (L+36,3,5), (-18,y-4,134), role="fork")
    for x in [-18,L+14]:
        add(name, (4,135,5), (x,y-26,134), role="fork")
    add(name, (L+36,4,5), (-18,y+105,134), role="fork")
    add(name, (30,12,5), (-44,y-26,134), role="fork")
    add(name, (6,12,72), (-44,y-26,62), role="fork")
    add(name, (22,16,4), (-60,y-24,62), role="fork")
    add(name, (4,16,11), (-60,y-24,55), role="fork")
    add(name, (14,16,10), (-65,y-24,45), role="fork")
    add("fork_front", (L-40,3,79), (20,y+101,60+s.front_lift), role="front_barrier")
    # Captive C rail: a 14x10 shoe inside a 16x12 channel with a 4mm neck.
    rail = "captive_guide"
    add(rail, (24,276,4), (-70,-238,40), "steel")
    for x in [-70,-50]:
        add(rail, (4,276,16), (x,-238,44), "steel")
    for x in [-66,-55]:
        add(rail, (5,276,4), (x,-238,56), "steel")
    # Geometric end blocks bound nominal travel, not an impact qualification.
    for yy in [-238,30]:
        add("end_block_"+str(yy), (16,8,12), (-66,yy,44), "steel")
    return out


def interpolate(a, b, f):
    return State(**{key:getattr(a,key)+(getattr(b,key)-getattr(a,key))*f for key in a.__dataclass_fields__})
