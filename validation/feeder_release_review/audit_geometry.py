"""Native solid validity and all-pair checks for each full reference-cycle pose."""

from pathlib import Path
import dataclasses, hashlib, itertools, json
import FreeCAD as App
import Part
from mechanism import shapes, cycle, interpolate, REVISION

H = Path(__file__).resolve().parent
out = []
for size, L in [("1U", 113.5), ("3U", 340.5)]:
    states = cycle(L)
    checks = []
    for name, state in states:
        ss, meta = shapes(L, state)
        invalid = []
        collisions = []
        for n, s in ss.items():
            if not s.isValid() or len(s.Solids) != 1:
                invalid.append(
                    {"part": n, "valid": s.isValid(), "solids": len(s.Solids)}
                )
        for a, b in itertools.combinations(ss, 2):
            ba, bb = ss[a].BoundBox, ss[b].BoundBox
            if any(
                getattr(ba, k + "Max") < getattr(bb, k + "Min") - 1e-6
                or getattr(bb, k + "Max") < getattr(ba, k + "Min") - 1e-6
                for k in ["X", "Y", "Z"]
            ):
                continue
            volume = ss[a].common(ss[b]).Volume
            if volume > 1e-5:
                collisions.append({"a": a, "b": b, "volume_mm3": volume})
        checks.append(
            {
                "pose": name,
                "state": dataclasses.asdict(state),
                "invalid": invalid,
                "collisions": collisions,
            }
        )
        print(size, name, "invalid", len(invalid), "collisions", collisions, flush=True)
    # Additional rotary exit-door positions; these are sampled, not a continuous certificate.
    for angle in range(5, 90, 5):
        from mechanism import State

        state = State(
            receiver=0,
            payload_feed=200,
            sled=80,
            exit_pin_withdraw=22,
            exit_gate_deg=angle,
        )
        ss, _ = shapes(L, state)
        pairs = []
        for b in ss:
            if b == "sled_front_stop":
                continue
            vol = ss["sled_front_stop"].common(ss[b]).Volume
            if vol > 1e-5:
                pairs.append({"a": "sled_front_stop", "b": b, "volume_mm3": vol})
        checks.append(
            {
                "pose": f"exit_angle_{angle}",
                "state": dataclasses.asdict(state),
                "invalid": [],
                "collisions": pairs,
            }
        )
        print(size, "angle", angle, pairs, flush=True)
    out.append({"size": size, "checks": checks})
    (H / "GEOMETRY_AUDIT.json").write_text(
        json.dumps(
            {
                "revision": REVISION,
                "CAD_source_sha256": hashlib.sha256(
                    (H / "mechanism.py").read_bytes()
                ).hexdigest(),
                "configurations": out,
                "boundary": "Exact nominal B-rep checks at listed full-cycle and rotary samples. No tolerance/load/contact or continuous rotary-clearance acceptance.",
            },
            indent=2,
        )
        + "\n"
    )
