"""Fit conditional feeder cycles into unchanged finite-burn coast intervals."""

from pathlib import Path
import json, hashlib

H = Path(__file__).parent
P = H / "inputs"
P.mkdir(exist_ok=True)
assumptions = {
    "slow_auxiliaries": dict(
        feed_s=20,
        return_s=20,
        gate_mm_s=10,
        bolt_mm_s=5,
        receiver_mm_s=5,
        front_mm_s=10,
        verification_s=6,
    ),
    "faster_auxiliaries": dict(
        feed_s=20,
        return_s=20,
        gate_mm_s=20,
        bolt_mm_s=10,
        receiver_mm_s=10,
        front_mm_s=20,
        verification_s=6,
    ),
}
out = []
for p in sorted(P.glob("*volley*.json")):
    data = json.loads(p.read_text())
    events = data["events"]
    shots = [e for e in events if e["kind"] == "shot"]
    for i, shot in enumerate(shots):
        previous = -900 if i == 0 else shots[i - 1]["start_s"] + 20
        eligible = []
        for e in events:
            if e["kind"] == "arc" and sum(abs(x) for x in e["force_N"]) < 1e-10:
                start = max(previous, e["start_s"])
                end = min(shot["start_s"] - 10, e["end_s"])
                if end > start:
                    eligible.append([start, end])
        coast = max(eligible, key=lambda x: x[1] - x[0]) if eligible else [0, 0]
        for name, a in assumptions.items():
            # Open/close storage,insert/withdraw its bolt,open/close fork front;
            # two receiver pin moves and one receiver-bar move precede shot.
            duration = (
                a["feed_s"]
                + a["return_s"]
                + 240 / a["gate_mm_s"]
                + 64 / a["bolt_mm_s"]
                + 36 / a["receiver_mm_s"]
                + 24 / a["front_mm_s"]
                + a["verification_s"]
            )
            available = coast[1] - coast[0]
            out.append(
                dict(
                    input=p.name,
                    release_index=i + 1,
                    release_s=shot["start_s"],
                    policy=name,
                    zero_force_coast_s=coast,
                    available_s=available,
                    required_assumed_s=duration,
                    margin_s=available - duration,
                    conditional_fit=available >= duration,
                )
            )
r = dict(
    revision="FSR-02",
    input_sha256={
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in P.glob("*volley*.json")
    },
    policies=assumptions,
    cases=out,
    boundary="Scheduling requirement screen using unchanged FBR-01 event commands. Whole handling cycle must fit one zero-force coast,20s after a previous release and10s before next shot. FM04 front travel is12mm each way; the201mm feed/return is still assumed20s each. Feed/auxiliary durations are assumptions, not rated actuator performance. Initial cell loading, carriage indexing, attitude slews, monitoring and recovery are excluded; no full campaign readiness follows.",
)
(H / "SCHEDULE.json").write_text(json.dumps(r, indent=2) + "\n")
print(
    len(out),
    "conditional handling schedules;",
    sum(not x["conditional_fit"] for x in out),
    "do not fit",
)
