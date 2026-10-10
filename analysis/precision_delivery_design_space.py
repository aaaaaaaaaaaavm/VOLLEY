#!/usr/bin/env python3
"""P124: kinematic and two-body design-space screen for precision delivery.

This is an exact ideal-impulse/tangential-orbit calculation and a constant-
acceleration stroke bound, not a Gen5 motor model, payload qualification,
provider mission, or demonstrated command envelope. Standard library only.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "analysis/results/precision_delivery_design_space.json"
REPORT = ROOT / "validation/P124_precision_delivery_design_space.md"
FIGURE = ROOT / "figures/precision_delivery_design_space.svg"

MU = 3.986004418e14  # m^3/s^2, Earth standard gravitational parameter
EARTH_RADIUS_M = 6_378_137.0
ALTITUDE_M = 450_000.0
STROKE_M = 1.3
PAYLOAD_KG = 4.0
G0 = 9.80665
REFERENCE_SPEED_M_S = 12.448437098832297  # P118 ideal finite-force screen
HISTORICAL_SPEED_M_S = 16.029  # contradicted historical periodic-force result
HISTORICAL_3SIGMA_M_S = 0.0274  # historical model-only assumed uncertainty


def circular_speed(radius_m: float) -> float:
    return math.sqrt(MU / radius_m)


def axis_rise_for_tangential_increment(delta_v_m_s: float) -> float:
    radius = EARTH_RADIUS_M + ALTITUDE_M
    speed = circular_speed(radius) + delta_v_m_s
    inverse_axis = 2 / radius - speed * speed / MU
    if inverse_axis <= 0:
        raise ValueError("unbound state outside this screen")
    return 1 / inverse_axis - radius


def tangential_increment_for_axis_rise(rise_m: float) -> float:
    radius = EARTH_RADIUS_M + ALTITUDE_M
    if rise_m < 0:
        raise ValueError("this screen accepts nonnegative axis rises")
    return math.sqrt(MU * (2 / radius - 1 / (radius + rise_m))) - circular_speed(radius)


def stroke_load(speed_m_s: float, stroke_m: float = STROKE_M) -> dict:
    acceleration = speed_m_s * speed_m_s / (2 * stroke_m)
    return {
        "relative_speed_m_s": speed_m_s,
        "stroke_m": stroke_m,
        "minimum_constant_acceleration_g": acceleration / G0,
        "payload_kinetic_energy_j": 0.5 * PAYLOAD_KG * speed_m_s**2,
        "ideal_stroke_for_10g_m": speed_m_s**2 / (2 * 10 * G0),
        "ideal_stroke_for_20g_m": speed_m_s**2 / (2 * 20 * G0),
    }


def build() -> dict:
    radius = EARTH_RADIUS_M + ALTITUDE_M
    orbit_targets = []
    for rise_km in (1, 5, 10, 20, 28.8, 50):
        nominal_dv = tangential_increment_for_axis_rise(rise_km * 1000)
        for axis_tolerance_km in (0.1, 1.0):
            lower = tangential_increment_for_axis_rise(max(0, rise_km - axis_tolerance_km) * 1000)
            upper = tangential_increment_for_axis_rise((rise_km + axis_tolerance_km) * 1000)
            orbit_targets.append({
                "target_axis_rise_km": rise_km,
                "axis_tolerance_km": axis_tolerance_km,
                "ideal_tangential_increment_m_s": nominal_dv,
                "permitted_inertial_increment_m_s": [lower, upper],
                "smaller_side_velocity_margin_m_s": min(nominal_dv - lower, upper - nominal_dv),
            })
    loads = [stroke_load(v) for v in (2.5, 5.0, REFERENCE_SPEED_M_S,
                                     HISTORICAL_SPEED_M_S, 20.0, 50.0, 1000.0)]
    max_speeds = [{"load_limit_g": g, "max_ideal_speed_m_s": math.sqrt(2 * g * G0 * STROKE_M)}
                  for g in (5, 10, 20, 100)]
    ideal_rise = axis_rise_for_tangential_increment(REFERENCE_SPEED_M_S)
    historical_error_rise = (
        axis_rise_for_tangential_increment(HISTORICAL_SPEED_M_S + HISTORICAL_3SIGMA_M_S)
        - axis_rise_for_tangential_increment(HISTORICAL_SPEED_M_S - HISTORICAL_3SIGMA_M_S)
    ) / 2
    return {
        "evidence_class": "ideal kinematic and two-body sensitivity screen; no rated speed, precision, motor, host, payload compliance, or delivery service verified",
        "inputs": {
            "mu_m3_s2": MU, "earth_radius_m": EARTH_RADIUS_M, "altitude_m": ALTITUDE_M,
            "stroke_m": STROKE_M, "payload_kg": PAYLOAD_KG, "g0_m_s2": G0,
            "p118_ideal_speed_m_s": REFERENCE_SPEED_M_S,
            "historical_challenged_speed_m_s": HISTORICAL_SPEED_M_S,
            "historical_model_3sigma_speed_m_s": HISTORICAL_3SIGMA_M_S,
            "assumptions": ["circular starting orbit", "instantaneous prograde tangential inertial increment",
                            "no host recoil correction in orbit table", "no drag, J2, maneuvers or state covariance",
                            "constant acceleration along full usable stroke", "no feeder, brake or host loads"],
        },
        "circular_speed_m_s": circular_speed(radius),
        "orbit_targets": orbit_targets,
        "ideal_stroke_loads": loads,
        "ideal_speed_limits_for_load": max_speeds,
        "p118_ideal_speed_axis_rise_km_if_entirely_inertial_tangential": ideal_rise / 1000,
        "historical_model_only_3sigma_axis_halfwidth_m_if_tangential": historical_error_rise,
    }


def report(data: dict) -> str:
    rows = data["orbit_targets"]
    loads = data["ideal_stroke_loads"]
    lines = [
        "# P124 — precision-delivery design-space screen", "",
        "**Result type:** exact ideal two-body orbital-energy conversion and minimum constant-acceleration stroke screen. This is a *requirements aid*, not a Gen5 rated-performance result or evidence of command precision.", "",
        "The customer job is a specified payload state and tolerance at an agreed epoch. Release speed alone is not that service: host state, direction, recoil, navigation, timing, repeatability, collision avoidance and disposal matter. The table assumes a 450 km circular Earth orbit and a purely prograde *inertial* increment; a real commanded relative release needs host momentum and attitude treatment.", "",
        "## Orbital state sets the speed and accuracy problem", "",
        "| Ideal axis-rise target | Required inertial tangential increment | ±axis band | Smaller-side increment margin |", "|--:|--:|--:|--:|",
    ]
    for row in rows:
        lines.append(f"| {row['target_axis_rise_km']:.1f} km | {row['ideal_tangential_increment_m_s']:.3f} m/s | ±{row['axis_tolerance_km']:.1f} km | {row['smaller_side_velocity_margin_m_s']:.4f} m/s |")
    lines += [
        "", "The margins above allocate the **entire** semimajor-axis error to velocity magnitude. A real requirement must split that budget among host navigation, release vector, speed, epoch, propagation and tracking. It must also specify along-track/plane/perigee tolerances; semimajor axis alone is not precision delivery.", "",
        "## Stroke and payload-load screening", "",
        "| Relative speed | Minimum mean acceleration over 1.3 m | Payload kinetic energy at 4 kg | Ideal stroke at 10 g |", "|--:|--:|--:|--:|",
    ]
    for row in loads:
        lines.append(f"| {row['relative_speed_m_s']:.3f} m/s | {row['minimum_constant_acceleration_g']:,.1f} g | {row['payload_kinetic_energy_j']:,.0f} J | {row['ideal_stroke_for_10g_m']:,.2f} m |")
    lines += [
        "", "At the 1.3 m *full usable stroke* idealization, the 10 g ceiling permits only "
        f"{data['ideal_speed_limits_for_load'][1]['max_ideal_speed_m_s']:.2f} m/s; actual profiles may peak higher. A 1 km/s release of an ordinary 4 kg 3U payload would require "
        f"{loads[-1]['minimum_constant_acceleration_g']:,.0f} g and {loads[-1]['payload_kinetic_energy_j']/1e6:.1f} MJ payload kinetic energy over that stroke, or "
        f"{loads[-1]['ideal_stroke_for_10g_m']/1000:.2f} km at 10 g. These are kinematic necessities; conversion losses, magnetic force and brake energy increase the system burden. A 1 km/s-class goal cannot be inherited as a credible first Gen6 prototype requirement for an ordinary 3U on the Gen5 stroke.", "",
        f"P118's {REFERENCE_SPEED_M_S:.3f} m/s finite-force value is an *ideal motor-energy conversion*, not a demonstrated relative command. If it were entirely inertial and prograde from the reference orbit, it would yield {data['p118_ideal_speed_axis_rise_km_if_entirely_inertial_tangential']:.2f} km immediate semimajor-axis rise. Actual host recoil and preburn must be modeled before using that number in a mission.", "",
        f"The old {HISTORICAL_3SIGMA_M_S:.4f} m/s (3σ) simulated release dispersion would correspond to about {data['historical_model_only_3sigma_axis_halfwidth_m_if_tangential']:.1f} m of two-body axis halfwidth **only if** it transferred unchanged to the challenged {HISTORICAL_SPEED_M_S:.3f} m/s point and all error were tangential. It has not been measured or transferred to P118, and does not establish payload delivery accuracy.", "",
        "## Product and prototype decisions", "",
        "1. Derive a first Gen6 prototype's speed *and accuracy* requirements from a named customer state, tolerance, payload acceleration limit and host/provider interface. Use a lower-speed 3U engineering demonstrator until those are known. Keep 1 km/s as a separate long-range, payload-specific research question with a new stroke and load architecture.",
        "2. Set one common-epoch mission benchmark with springs plus competent host maneuvers and VOLLEY. Count installed mass, host resources and failures. The existing P123 one-event comparison is unfavorable to Gen5, and the sampled twelve-shot case does not close.",
        "3. Verify commanded range, direction and repeatability with a selected drive and mechanisms model; then test a calibrated physical prototype. Analytic orbital sensitivity is a requirement generator, not a measurement.", "",
        "![Ideal load and speed design space](../figures/precision_delivery_design_space.svg)", "",
        "Reproduce with `python3 analysis/precision_delivery_design_space.py`; `--check` verifies the committed result and figure. The JSON contains the constants, assumptions and unrounded numbers.", "",
    ]
    return "\n".join(lines)


def figure(data: dict) -> str:
    # Fixed-layout vector figure with coordinates determined entirely by the captured result.
    speeds = [x["relative_speed_m_s"] for x in data["ideal_stroke_loads"]]
    gvals = [x["minimum_constant_acceleration_g"] for x in data["ideal_stroke_loads"]]
    selected = list(zip(speeds[1:6], gvals[1:6]))
    xmin, xmax, ymin, ymax = 5.0, 55.0, 0.0, 125.0
    x = lambda v: 92 + (v - xmin) / (xmax - xmin) * 640
    y = lambda g: 432 - (g - ymin) / (ymax - ymin) * 315
    points = " ".join(f"{x(v):.1f},{y(v*v/(2*STROKE_M*G0)):.1f}" for v in range(5, 51))
    grid = "".join(f'<line x1="92" y1="{y(g):.1f}" x2="732" y2="{y(g):.1f}" stroke="#d6e0e6"/><text x="78" y="{y(g)+5:.1f}" text-anchor="end" fill="#586c7b" font-size="15">{g}</text>' for g in (0,20,40,60,80,100,120))
    ticks = "".join(f'<text x="{x(v):.1f}" y="457" text-anchor="middle" fill="#586c7b" font-size="15">{v}</text>' for v in (5,10,20,30,40,50))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 540" role="img" aria-label="Ideal acceleration needed for release speed over 1.3 metre stroke">
<rect width="900" height="540" fill="#f8fbfd"/><text x="48" y="51" font-family="Arial,sans-serif" font-size="27" font-weight="700" fill="#102b3c">Speed is constrained by payload load</text>
<text x="48" y="80" font-family="Arial,sans-serif" font-size="16" fill="#456173">Ideal constant acceleration over 1.3 m; 4 kg payload. Not a motor or qualification result.</text>
<g font-family="Arial,sans-serif">{grid}<line x1="92" y1="432" x2="732" y2="432" stroke="#324d60" stroke-width="2"/><line x1="92" y1="117" x2="92" y2="432" stroke="#324d60" stroke-width="2"/>{ticks}
<line x1="92" y1="{y(10):.1f}" x2="732" y2="{y(10):.1f}" stroke="#b6672c" stroke-dasharray="7 5" stroke-width="2"/>
<text x="748" y="{y(10)+5:.1f}" fill="#9b4f18" font-size="15">10 g example</text>
<polyline points="{points}" fill="none" stroke="#007f8e" stroke-width="4"/>
{''.join(f'<circle cx="{x(v):.1f}" cy="{y(g):.1f}" r="5" fill="#007f8e"/>' for v,g in selected)}
<text x="417" y="496" text-anchor="middle" fill="#27485b" font-size="17">relative release speed (m/s)</text>
<text transform="translate(29 274) rotate(-90)" text-anchor="middle" fill="#27485b" font-size="17">minimum mean acceleration (g)</text>
<rect x="80" y="507" width="12" height="12" fill="#007f8e"/><text x="102" y="518" fill="#456173" font-size="13">Ordinary 3U requires a mission-specific load limit. 1 km/s lies far beyond this plot.</text></g></svg>'''


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = build()
    for row in data["orbit_targets"]:
        error = axis_rise_for_tangential_increment(row["ideal_tangential_increment_m_s"])
        assert abs(error - row["target_axis_rise_km"] * 1000) < 1e-5
    assert abs(stroke_load(1000)["minimum_constant_acceleration_g"] - 39218.0) < 20
    raw = json.dumps(data, indent=2) + "\n"
    prose = report(data)
    graphic = figure(data)
    if args.check:
        if RESULT.read_text() != raw or REPORT.read_text() != prose or FIGURE.read_text() != graphic:
            raise SystemExit("P124 captured output stale")
        print("P124 result, report, figure and inverse identities PASS")
    else:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        FIGURE.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(raw)
        REPORT.write_text(prose)
        FIGURE.write_text(graphic)
        print("P124 generated")


if __name__ == "__main__":
    main()
