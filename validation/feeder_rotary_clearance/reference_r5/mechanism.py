"""FM07 reference: captive pins and a hinged forward exit restraint.

Millimetres, native FreeCAD solids. This is a geometry development revision;
source-rated actuation, strength, actual contact and four-cell integration are
separate analyses. It does not modify the evaluated Gen5 configuration.
"""

from dataclasses import dataclass
import FreeCAD as App
import Part
import fm06
from fm06 import B, C, fuse

REVISION = "FM07-R5"


@dataclass(frozen=True)
class State(fm06.State):
    exit_gate_deg: float = 0
    exit_pin_withdraw: float = 0
    departure: float = 0


def shapes(L, s):
    base = fm06.State(**{k: getattr(s, k) for k in fm06.State.__dataclass_fields__})
    ss, meta = fm06.shapes(L, base)
    xx = s.sled
    for x in [5, L - 13]:
        # The existing2.5mm-radius pin head remains inside a closed cup.
        # The stem and rear shaft pass through smaller bores; neither permits
        # the head to leave the assembly in either axial direction.
        cup = C(4.5, 20, (x - 21 + xx, -10, 0), (1, 0, 0))
        cup = cup.cut(C(2.6, 17, (x - 20 + xx, -10, 0), (1, 0, 0)))
        cup = cup.cut(C(1.65, 4, (x - 3 + xx, -10, 0), (1, 0, 0)))
        cup = cup.cut(C(0.85, 3, (x - 22 + xx, -10, 0), (1, 0, 0)))
        ss["sled_body"] = ss["sled_body"].fuse(cup).removeSplitter()
    for i, x in enumerate([5, L - 13]):
        tail = C(0.75, 20, (x - 25 + xx - s.receiver_pin, -10, 0), (1, 0, 0))
        ss["receiver_lock_pin_" + str(i)] = (
            ss["receiver_lock_pin_" + str(i)].fuse(tail).removeSplitter()
        )

    # Exit door swings clockwise into an outboardY corridor. The full-open
    # plate remains outboard of the nominal payload Y[0, 100] corridor.
    px = L + 9.5 + xx
    py = -12
    door = fuse(
        [
            B((2, 82, 18), (L + 1 + xx, 10, 22)),
            B((2, 24, 4), (px - 1, -12, 30)),
            B((8, 4, 4), (L + 1 + xx, 8, 30)),
            B((6, 8, 4), (px - 3, -10, 30)),
            C(3, 22, (px, py, 20), (0, 0, 1)),
        ]
    )
    door = door.cut(C(1.65, 42, (px, py, 9), (0, 0, 1)))
    door = door.cut(C(1.15, 30, (px, -4.5, 10), (0, 0, 1))).removeSplitter()
    door.rotate(App.Vector(px, py, 0), App.Vector(0, 0, 1), -s.exit_gate_deg)
    ss["sled_front_stop"] = door
    meta["sled_front_stop"] = ("steel", "exit_gate")

    bracket = fuse(
        [
            B((12, 14, 8), (px - 6, -19, 10)),
            B((12, 14, 6), (px - 6, -19, 44)),
            B((12, 2, 26), (px - 6, -19, 18)),
        ]
    )
    bracket = bracket.cut(C(1.65, 42, (px, py, 9), (0, 0, 1)))
    clearance = fuse(
        [
            C(1.85, 27, (px, -4.5, -10), (0, 0, 1)),
            C(1.15, 20, (px, -4.5, 17), (0, 0, 1)),
            C(0.6, 5, (px, -4.5, -15), (0, 0, 1)),
        ]
    )
    pin_guide = B((6, 6, 12), (px - 3, -7.5, 16)).cut(clearance)
    pin_cup = C(3.5, 30, (px, -4.5, -12), (0, 0, 1)).cut(clearance)
    bracket = bracket.cut(clearance)
    body = ss["sled_body"].cut(clearance)
    ss["sled_body"] = body.multiFuse([bracket, pin_guide, pin_cup]).removeSplitter()
    shaft = fuse(
        [
            C(1.5, 42.4, (px, py, 8.8), (0, 0, 1)),
            C(3, 1.6, (px, py, 8.2), (0, 0, 1)),
            C(3, 1.6, (px, py, 50.2), (0, 0, 1)),
        ]
    )
    ss["exit_hinge_pin"] = shaft
    meta["exit_hinge_pin"] = ("steel", "sled")
    z = -s.exit_pin_withdraw
    lock = fuse(
        [
            C(1, 20, (px, -4.5, 16 + z), (0, 0, 1)),
            C(1.75, 2, (px, -4.5, 14 + z), (0, 0, 1)),
            C(0.5, 26, (px, -4.5, -12 + z), (0, 0, 1)),
        ]
    )
    ss["exit_lock_pin"] = lock
    meta["exit_lock_pin"] = ("steel", "exit_lock_pin")
    ss["payload"].translate(App.Vector(s.departure, 0, 0))
    return ss, meta


def cycle(L):
    rows = [
        (n, State(**{k: getattr(s, k) for k in fm06.State.__dataclass_fields__}))
        for n, s in fm06.cycle()[:-1]
    ]
    common = dict(receiver=0, payload_feed=200, sled=80)
    rows += [
        ("exit_unlocked", State(**common, exit_pin_withdraw=22)),
        ("exit_open", State(**common, exit_pin_withdraw=22, exit_gate_deg=90)),
        (
            "payload_clear",
            State(**common, exit_pin_withdraw=22, exit_gate_deg=90, departure=L + 150),
        ),
        (
            "empty_carrier_home",
            State(
                receiver=0,
                payload_feed=200,
                exit_pin_withdraw=22,
                exit_gate_deg=90,
                departure=L + 230,
            ),
        ),
        (
            "exit_closed",
            State(
                receiver=0, payload_feed=200, exit_pin_withdraw=22, departure=L + 230
            ),
        ),
        ("exit_locked", State(receiver=0, payload_feed=200, departure=L + 230)),
        (
            "receiver_unlock_empty",
            State(receiver=0, receiver_pin=12, payload_feed=200, departure=L + 230),
        ),
        (
            "receiver_open_empty",
            State(receiver=12, receiver_pin=12, payload_feed=200, departure=L + 230),
        ),
        ("ready_empty", State(receiver=12, payload_feed=200, departure=L + 230)),
    ]
    return rows


def interpolate(a, b, f):
    return State(
        **{
            k: getattr(a, k) + (getattr(b, k) - getattr(a, k)) * f
            for k in State.__dataclass_fields__
        }
    )
