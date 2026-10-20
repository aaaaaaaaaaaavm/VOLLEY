"""Two-confirmation controller requirements with fault injection.

Confirmations are modeled Boolean observations. The model cannot establish
physical independence, wiring safety, timing, or actual latch positions.
"""

from pathlib import Path
import itertools, json

H = Path(__file__).parent
preconditions = {
    "open_storage": {"fork_captive": True, "fork_home": True, "sled_docked": True},
    "feed": {
        "gate_open_locked": True,
        "fork_captive": True,
        "sled_docked": True,
        "receiver_open_locked": True,
        "path_proved": True,
    },
    "capture_receiver": {
        "payload_seated": True,
        "fork_captive": True,
        "sled_docked": True,
    },
    "open_fork": {
        "receiver_captive": True,
        "payload_seated": True,
        "sled_docked": True,
    },
    "withdraw_fork": {
        "receiver_captive": True,
        "sled_docked": True,
        "fork_front_open": True,
    },
    "close_storage": {"fork_home": True, "receiver_captive": True},
    "move_sled": {
        "receiver_captive": True,
        "fork_home": True,
        "gate_closed_locked": True,
        "path_proved": True,
    },
    "reset": {"fork_home": True, "path_proved": True, "supervised_reset": True},
}


def permits(action, observations, power=True, fault_latched=False):
    return (
        power
        and not fault_latched
        and all(
            observations[name] == (value, value)
            for name, value in preconditions[action].items()
        )
    )


summary = []
counterexamples = []
for action, conditions in preconditions.items():
    names = list(conditions)
    tested = 0
    for truth_tuple in itertools.product([False, True], repeat=len(names)):
        truth = dict(zip(names, truth_tuple))
        obs = {n: (truth[n], truth[n]) for n in names}
        safe = all(truth[n] == v for n, v in conditions.items())
        for fault_name in [None, *names]:
            for channel in ([0] if fault_name is None else [0, 1]):
                indicated = dict(obs)
                if fault_name is not None:
                    a = list(indicated[fault_name])
                    a[channel] = not a[channel]
                    indicated[fault_name] = tuple(a)
                allowed = permits(action, indicated)
                assert not allowed or safe
                assert not permits(action, indicated, power=False)
                assert not permits(action, indicated, fault_latched=True)
                tested += 1
        if not safe:
            # Two observations with one shared false premise still defeat the guard.
            false = [n for n in names if truth[n] != conditions[n]]
            if len(false) == 1:
                indicated = dict(obs)
                indicated[false[0]] = (conditions[false[0]],) * 2
                assert permits(action, indicated)
                counterexamples.append(
                    dict(
                        action=action,
                        common_cause_false_confirmation=false[0],
                        unsafe_permission=True,
                    )
                )
    summary.append(
        dict(
            action=action,
            requirements=conditions,
            truth_and_single_channel_fault_cases=tested,
        )
    )
out = dict(
    revision="FM-02",
    actions=summary,
    total_cases=sum(x["truth_and_single_channel_fault_cases"] for x in summary),
    common_cause_counterexamples=counterexamples,
    fault_policy="Any jam,timeout,disagreement or unexpected occupancy latches campaign inhibit. Failed cell stays restrained; remaining cells require supervised reset and a newly proved common path.",
    boundary="Finite Boolean requirements verification. Neither actual sensors nor their independence/contact coverage are implemented. Power loss does not itself provide mechanical containment.",
)
(H / "CONTROLLER_REVIEW.json").write_text(json.dumps(out, indent=2) + "\n")
print(
    out["total_cases"],
    "controller combinations;",
    len(counterexamples),
    "common-cause counterexamples retained",
)
