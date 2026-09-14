"""P113-S1: optimistic single-event reach, not integrated mission feasibility.

Run sheet: validation/P113_S1_departure_trade.md, committed before this script.
No solver for release contact or host operations is hidden inside this allocation.
"""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

from host_reference import G0, MU, RE

ROOT = Path(__file__).resolve().parents[1]
INPUTS = {
    "reference_altitudes_km": [450, 500],
    "opposite_apsis_offsets_km": [-100, -50, 0, 10, 50, 100, 200],
    "retained_host_masses_kg": [100, 300, 1000],
    "payload_mass_kg": 4,
    "host_budgets_m_s": [0, 2, 10, 30, 100],
    "assumed_minimum_relative_speed_m_s": 0.5,
    "maximum_speed_screens_m_s": {
        "spring_reference": 2, "bolley_reference": 11.8,
        "gen5_reference": 16.029, "gen6_reference": 29.009,
        "exploratory_100": 100, "exploratory_120": 120,
    },
    "stroke_m": 8, "assumed_acceleration_ceiling_g": 25,
}
TOL = 1e-10


def finite(*values):
    if not all(math.isfinite(x) for x in values):
        raise ValueError("inputs must be finite")


def required_increment(alt_km, opposite_km, circular_destination=False):
    """Signed tangential impulse from a circular orbit to a specified apsis pair."""
    finite(alt_km, opposite_km)
    if min(alt_km, opposite_km) <= 0:
        raise ValueError("positive above-surface altitudes required")
    if circular_destination and alt_km != opposite_km:
        raise ValueError("a single event cannot change position to a different circle")
    r, other = RE + alt_km * 1000, RE + opposite_km * 1000
    a = (r + other) / 2
    return math.sqrt(MU * (2 / r - 1 / a)) - math.sqrt(MU / r)


def allocate(d, budget, retained_mass, payload_mass, minimum, maximum):
    """Find a witness in the intersection of reachable |u| and assumed speed range."""
    finite(d, budget, retained_mass, payload_mass, minimum, maximum)
    if budget < 0 or min(retained_mass, payload_mass, minimum) <= 0 or maximum < minimum:
        raise ValueError("invalid mass, budget or release interval")
    fraction = retained_mass / (retained_mass + payload_mass)
    lower = max(0, abs(d) - budget) / fraction
    upper = (abs(d) + budget) / fraction
    speed = max(minimum, lower)
    covered = speed <= min(maximum, upper) + TOL
    result = {"kinematic_screen_covered": covered,
              "required_relative_magnitude_interval_m_s": [lower, upper]}
    if covered:
        u = math.copysign(speed, d)
        h = d - fraction * u
        result.update(relative_speed_m_s=u, host_impulse_m_s=h,
                      payload_increment_m_s=h + fraction * u,
                      retained_host_increment_m_s=h - (1 - fraction) * u)
    return result


def stroke_bound(speed, acceleration_g, stroke):
    finite(speed, acceleration_g, stroke)
    if speed < 0 or acceleration_g <= 0 or stroke <= 0:
        raise ValueError("invalid kinematic-bound inputs")
    return {"speed_m_s": speed,
            "ideal_minimum_stroke_m": speed ** 2 / (2 * acceleration_g * G0),
            "mean_acceleration_over_stroke_g": speed ** 2 / (2 * stroke * G0)}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build():
    rows = []
    for alt, offset, mass, budget in itertools.product(
            INPUTS["reference_altitudes_km"], INPUTS["opposite_apsis_offsets_km"],
            INPUTS["retained_host_masses_kg"], INPUTS["host_budgets_m_s"]):
        d = required_increment(alt, alt + offset)
        screens = {name: allocate(d, budget, mass, INPUTS["payload_mass_kg"],
                                 INPUTS["assumed_minimum_relative_speed_m_s"], cap)
                   for name, cap in INPUTS["maximum_speed_screens_m_s"].items()}
        if screens["spring_reference"]["kinematic_screen_covered"]:
            interpretation = "SPRING_REFERENCE_COVERS_DEPARTURE_STATE"
        elif any(s["kinematic_screen_covered"] for s in screens.values()):
            interpretation = "CONDITIONAL_REACH_EXTENSION"
        else:
            interpretation = "UNCOVERED"
        rows.append({"reference_altitude_km": alt, "opposite_apsis_offset_km": offset,
                     "retained_host_mass_kg": mass, "host_budget_m_s": budget,
                     "required_payload_increment_m_s": d,
                     "interpretation": interpretation, "screens": screens})
    paths = ["analysis/departure_trade.py", "analysis/host_reference.py",
             "validation/P113_S1_departure_trade.md"]
    return {"study": "P113-S1", "status": "MODEL_OUTPUT_NOT_HARDWARE_VALIDATION",
            "open_items": ["P113", "E5"], "inputs": INPUTS,
            "assumptions": ["instantaneous tangential host burn and release at one position",
                            "continuous signed host control and reversible release direction",
                            "optimistic continuous speed screens; no established operating envelopes",
                            "no campaign, cost, installed mass, reliability or collision clearance verdict"],
            "source_sha256": {p: digest(ROOT / p) for p in paths},
            "input_sha256": hashlib.sha256(json.dumps(INPUTS, sort_keys=True).encode()).hexdigest(),
            "cases": rows,
            "stroke_bounds": [stroke_bound(v, INPUTS["assumed_acceleration_ceiling_g"],
                                            INPUTS["stroke_m"])
                              for v in [29.009, 89.4, 100, 120]]}


def report(data):
    lines = ["# Host impulse versus departure speed", "",
             "Generated by `analysis/departure_trade.py`. Do not hand-edit.", "",
             "**P113-S1 is a single-event kinematic screen. P113 and E5 remain open.**", "",
             "A covered cell is not a feasible mission. Every speed interval, including the",
             "0.5 m/s minimum, is an optimistic assumption, not a validated control envelope.",
             "Neither provider supplied inputs. Gen5, Gen6 and BOLLEY are not reselected here.", "",
             "[Criteria](../validation/P113_S1_departure_trade.md) ·",
             "[Full results](../analysis/results/departure_trade.json) ·",
             "[Provider study](HOST_COMPATIBILITY.md)", "",
             "## One common departure position", "",
             "The target keeps one apsis at the circular starting altitude. Positive offsets",
             "raise the opposite apsis; negative offsets lower it. These are not new circular",
             "destination orbits. Host impulse is an instantaneous signed allocation at release,",
             "not a precomputed manoeuvre to a different shell.", "",
             "The retained host includes the deployer and remaining manifest. Momentum is",
             "conserved; relative release speed is not equated to inertial payload delta-v.", "",
             "## 450 km reference, 300 kg retained host, 4 kg payload", "",
             "The columns below ask only whether the **assumed 0.5–2 m/s spring interval**",
             "can reach the exact target with the indicated continuously adjustable host budget.",
             "A no is not a recommendation for a larger deployer. A yes establishes no resource advantage.", "",
             "| Opposite-apsis offset, km | Payload increment, m/s | B=0 | B=2 | B=10 | B=30 | B=100 |",
             "|---|---:|---|---|---|---|---|"]
    for offset in INPUTS["opposite_apsis_offsets_km"]:
        rows = [r for r in data["cases"] if r["reference_altitude_km"] == 450
                and r["retained_host_mass_kg"] == 300 and r["opposite_apsis_offset_km"] == offset]
        cells = ["yes" if r["screens"]["spring_reference"]["kinematic_screen_covered"] else "no"
                 for r in rows]
        lines.append(f"| {offset:+} | {rows[0]['required_payload_increment_m_s']:+.4f} | " + " | ".join(cells) + " |")
    lines += ["", "The zero-offset/B=0 no is intentional: nonzero tangential separation cannot",
              "exactly preserve the original circular state without compensation. Radial release,",
              "orbital tolerances and time-dependent clearance are outside this screen.", "",
              "## What higher speed costs even before mechanism losses", "",
              "Ideal constant-acceleration lower bounds at the assumed 25 g ceiling; average",
              "acceleration over 8 m is not peak acceleration. No payload qualification is implied.", "",
              "| Relative speed, m/s | Minimum stroke at 25 g, m | Mean acceleration over 8 m, g |",
              "|---:|---:|---:|"]
    for row in data["stroke_bounds"]:
        lines.append(f"| {row['speed_m_s']:.3f} | {row['ideal_minimum_stroke_m']:.3f} | {row['mean_acceleration_over_stroke_g']:.3f} |")
    lines += ["", "89.4 m/s is a historical store trade boundary, not a demonstrated Gen6 speed.",
              "100 and 120 m/s are exploratory points, not adopted requirements.", "",
              "## What still determines whether the machine deserves to exist", "",
              "Finite burns and minimum impulse bit; sequential release timing; changing mass",
              "properties; pointing, tip-off and velocity uncertainty; restart and coast limits;",
              "installed mass and occupied volume; safe clearance and recontact; remaining-manifest",
              "fault exposure; propellant, power and disposal reserve. None is closed by reach alone.", "",
              "The next comparison must hold complete mission targets and time windows fixed and",
              "price these burdens for conventional release, host-assisted release, VOLLEY, BOLLEY",
              "and payload propulsion where permitted. Do not infer a manifest crossover here.", "",
              "## Reproduce", "", "```bash", "python3 analysis/departure_trade.py",
              "python3 analysis/departure_trade.py --check",
              "python3 -m pytest tests/test_departure_trade.py", "```", ""]
    return "\n".join(lines)


def outputs(data):
    return {"analysis/results/departure_trade.json": json.dumps(data, indent=2, sort_keys=True) + "\n",
            "docs/DEPARTURE_TRADE.md": report(data)}


def check_outputs(root, rendered):
    return [name for name, content in rendered.items()
            if not (root / name).is_file() or (root / name).read_text() != content]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = outputs(build())
    if args.check:
        stale = check_outputs(ROOT, rendered)
        print("departure trade: " + ("STALE " + ", ".join(stale) if stale else "current; P113/E5 remain open"))
        return int(bool(stale))
    for name, content in rendered.items():
        (ROOT / name).write_text(content)
    print("departure trade: wrote JSON and review; P113/E5 remain open")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
