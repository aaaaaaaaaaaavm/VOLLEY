"""Adverse commands tested against real FM-02 B-rep geometry.

Positive intersection is the deliberate mechanical obstruction in these fault
tests. It is not counted as a nominal motion pass or a strength qualification.
"""

from pathlib import Path
from dataclasses import replace
import json
from mechanism import shapes, State, REVISION

H = Path(__file__).parent
out = []
for label, L in [("1U", 113.5), ("3U", 340.5)]:
    # Pin already inserted: gate closure is physically blocked by its bore.
    ss, _ = shapes(L, State(gate=119.5, bolt=0))
    v = ss["storage_gate"].common(ss["gate_crossbolt"]).Volume
    assert v > 0
    out.append(
        dict(
            payload=label,
            fault="gate_closes_with_bolt_inserted",
            command_mm=0.5,
            obstruction_mm3=v,
            nominal_radial_lost_motion_mm=0.2,
        )
    )
    # A travelling fork obstructs pin-head withdrawal before gate engagement is lost.
    for feed in [7, 50, 100, 150, 200]:
        ss, _ = shapes(L, State(feed=feed, gate=120, bolt=6, payload_feed=feed))
        v = ss["fork_body"].common(ss["gate_crossbolt"]).Volume
        assert v > 0, (label, feed, v)
        out.append(
            dict(
                payload=label,
                fault="bolt_withdrawal_during_transfer",
                feed_mm=feed,
                withdraw_command_mm=6,
                obstruction_mm3=v,
                lug_width_mm=10,
                full_withdrawal_needed_mm=29,
            )
        )
    # An uninserted pin obstructs the fork before the payload reaches the gate.
    ss, _ = shapes(L, State(feed=6, gate=120, bolt=32, payload_feed=6))
    v = ss["fork_body"].common(ss["gate_crossbolt"]).Volume
    assert v > 0
    out.append(
        dict(
            payload=label,
            fault="feed_without_inserted_bolt",
            feed_mm=6,
            obstruction_mm3=v,
            payload_to_gate_nominal_mm=1,
        )
    )
    for position, attempt in [("open", 11.5), ("closed", 0.5)]:
        ss, _ = shapes(L, State(receiver=attempt, receiver_pin=0))
        for i in [0, 1]:
            v = ss["sled_entry_bar"].common(ss["receiver_lock_pin_" + str(i)]).Volume
            assert v > 0
            out.append(
                dict(
                    payload=label,
                    fault="receiver_moves_from_locked_" + position,
                    independently_retained_pin=i,
                    obstruction_mm3=v,
                    attempt_mm=0.5,
                )
            )
    # Counterexample: if both locks are physically withdrawn, false commands can
    # still drive the entry dogs into a straddling payload. Retain common cause.
    ss, _ = shapes(
        L,
        State(
            feed=150, gate=120, bolt=0, receiver=0, receiver_pin=12, payload_feed=150
        ),
    )
    v = ss["payload"].common(ss["sled_entry_bar"]).Volume
    assert v > 0
    out.append(
        dict(
            payload=label,
            fault="both_receiver_locks_withdrawn_and_bar_closes_on_straddling_payload",
            unresolved=True,
            penetration_mm3=v,
        )
    )
r = dict(
    revision=REVISION,
    cases=out,
    verified_rigid_obstructions=sum("obstruction_mm3" in x for x in out),
    retained_counterexamples=sum(x.get("unresolved", False) for x in out),
    boundary="Rigid positions. Inserted receiver pins obstruct each endpoint independently; axial pin retention, release actuators, springs, force, wear and sensor qualification remain unimplemented. A shared false release of both pins defeats the geometric hold.",
)
(H / "PHYSICAL_INTERLOCKS.json").write_text(json.dumps(r, indent=2) + "\n")
print(
    r["verified_rigid_obstructions"],
    "physical obstruction checks;",
    r["retained_counterexamples"],
    "receiver counterexamples retained",
)
