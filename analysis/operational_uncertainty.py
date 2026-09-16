#!/usr/bin/env python3
"""P113-S5: deterministic local sensitivity around the accepted S4 campaign."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np

import campaign_allocation as campaign
import terminal_timing as terminal

ROOT = Path(__file__).resolve().parents[1]
S4_PATH = ROOT / "analysis/results/manifest_timing.json"
CRITERIA_PATH = ROOT / "validation/P113_S5_operational_uncertainty.md"
OUTPUT_JSON = ROOT / "analysis/results/operational_uncertainty.json"
OUTPUT_DOC = ROOT / "docs/OPERATIONAL_UNCERTAINTY.md"
OUTPUT_SVG = ROOT / "figures/operational_uncertainty.svg"
TERMINAL_TIME_S = terminal.INPUTS["terminal_time_s"]
POSITION_BAND_M = terminal.INPUTS["position_band_m"]
VELOCITY_BAND_M_S = terminal.INPUTS["velocity_band_m_s"]
PAYLOAD_KG = terminal.INPUTS["payload_kg"]
DEAD_TIME_MARKERS_S = (30, 60, 120, 300)
SMALL_POSITION_M = 1e-9
SMALL_VELOCITY_M_S = 1e-12

PERTURBATIONS = (
    ("common_position_radial_m", "common_position", "radial", 1.0),
    ("common_position_tangential_m", "common_position", "tangential", 1.0),
    ("common_velocity_radial_m_s", "common_velocity", "radial", 0.001),
    ("common_velocity_tangential_m_s", "common_velocity", "tangential", 0.001),
    ("release_speed_m_s", "release_speed", "release", 0.001),
    ("release_direction_rad", "release_direction", "release", math.radians(0.01)),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_s4() -> dict:
    data = json.loads(S4_PATH.read_text(encoding="utf-8"))
    if data.get("study") != "P113-S4":
        raise ValueError("unexpected S4 payload")
    for rel, expected in data.get("source_sha256", {}).items():
        path = ROOT / rel
        if not path.exists() or sha256(path) != expected:
            raise ValueError(f"stale S4 source: {rel}")
    return data


def selected_campaign(data: dict) -> tuple[dict, dict, dict]:
    matches = [s for s in data["selections"]
               if s["screen"] == "bolley_screen" and s["grid"] == "fine"
               and s["policy"] == "enumerated" and s["order"] == "either"]
    if len(matches) != 1 or matches[0]["status"] != "BEST_TESTED":
        raise ValueError("cannot identify accepted S4 BOLLEY-screen selection")
    selection = matches[0]
    row = data["cases"][selection["case_index"]]
    candidate = row["candidates"][selection["candidate_index"]]
    if not candidate.get("accepted") or len(candidate.get("events", [])) != 2:
        raise ValueError("selected S4 campaign is not an accepted two-event campaign")
    return selection, row, candidate


def basis(position) -> tuple[np.ndarray, np.ndarray]:
    p = np.asarray(position, dtype=float)
    if p.shape != (2,) or not np.all(np.isfinite(p)) or np.linalg.norm(p) <= 0:
        raise ValueError("finite nonzero planar position required")
    radial = p / np.linalg.norm(p)
    tangential = np.array([-radial[1], radial[0]])
    if abs(np.linalg.norm(radial) - 1.0) > 1e-12:
        raise ValueError("radial basis is not unit length")
    if abs(np.linalg.norm(tangential) - 1.0) > 1e-12:
        raise ValueError("tangential basis is not unit length")
    if abs(float(np.dot(radial, tangential))) > 1e-12:
        raise ValueError("local basis is not orthogonal")
    return radial, tangential


def rotate(vector, angle_rad: float) -> np.ndarray:
    v = np.asarray(vector, dtype=float)
    c, s = math.cos(angle_rad), math.sin(angle_rad)
    return np.array([c*v[0]-s*v[1], s*v[0]+c*v[1]])


def reconstruct_mechanism_state(event: dict, new_relative_velocity) -> tuple[np.ndarray, np.ndarray, float]:
    sep = event["separation"]
    payload = np.asarray(sep["payload_state"], dtype=float)
    host = np.asarray(sep["host_state"], dtype=float)
    if payload.shape != (4,) or host.shape != (4,):
        raise ValueError("invalid stored separation states")
    retained = float(sep["retained_mass_kg"])
    post = float(sep["mass_after_second_kg"])
    if not (math.isfinite(retained) and math.isfinite(post) and retained > 0
            and math.isclose(post, retained + PAYLOAD_KG, rel_tol=0.0, abs_tol=1e-9)):
        raise ValueError("corrupt separation mass accounting")
    u0 = np.asarray(sep["relative_velocity_m_s"], dtype=float)
    if u0.shape != (2,) or not np.all(np.isfinite(u0)) or np.linalg.norm(u0) <= 0:
        raise ValueError("corrupt relative-release vector")
    if np.linalg.norm((payload[2:] - host[2:]) - u0) > 1e-9:
        raise ValueError("stored separation states disagree with relative-release vector")
    com = (PAYLOAD_KG*payload[2:] + retained*host[2:]) / post
    u = np.asarray(new_relative_velocity, dtype=float)
    vp = com + retained/post*u
    vh = com - PAYLOAD_KG/post*u
    residual = float(np.linalg.norm(PAYLOAD_KG*vp + retained*vh - post*com))
    payload_new = np.r_[payload[:2], vp]
    host_new = np.r_[host[:2], vh]
    return payload_new, host_new, residual


def nominal_record(event: dict) -> dict:
    sep = event["separation"]
    payload = np.asarray(sep["payload_state"], dtype=float)
    release_time = float(event["time_s"])
    propagated = campaign.coast(payload, TERMINAL_TIME_S-release_time)
    stored = np.asarray(event["terminal_state"], dtype=float)
    reproduction_position_m = float(np.linalg.norm(propagated[:2]-stored[:2]))
    reproduction_velocity_m_s = float(np.linalg.norm(propagated[2:]-stored[2:]))
    if reproduction_position_m > 1e-6 or reproduction_velocity_m_s > 1e-9:
        raise ValueError("nominal S4 terminal state does not reproduce")
    target = terminal.target_state(event["target"], TERMINAL_TIME_S)
    error = propagated-target
    radial, tangential = basis(payload[:2])
    return {
        "target": event["target"], "release_time_s": release_time,
        "payload_state": payload.tolist(), "host_state": sep["host_state"],
        "relative_velocity_m_s": sep["relative_velocity_m_s"],
        "retained_mass_kg": sep["retained_mass_kg"],
        "mass_after_second_kg": sep["mass_after_second_kg"],
        "terminal_state": propagated.tolist(), "target_terminal_state": target.tolist(),
        "terminal_error_vector": error.tolist(),
        "position_error_m": float(np.linalg.norm(error[:2])),
        "velocity_error_m_s": float(np.linalg.norm(error[2:])),
        "reproduction_position_m": reproduction_position_m,
        "reproduction_velocity_m_s": reproduction_velocity_m_s,
        "radial_basis": radial.tolist(), "tangential_basis": tangential.tolist(),
    }


def perturb_state(event: dict, nominal: dict, family: str, axis: str, amount: float):
    state = np.asarray(nominal["payload_state"], dtype=float).copy()
    radial = np.asarray(nominal["radial_basis"], dtype=float)
    tangential = np.asarray(nominal["tangential_basis"], dtype=float)
    direction = radial if axis == "radial" else tangential
    momentum_residual = None
    host_state = None
    if family == "common_position":
        state[:2] += amount*direction
    elif family == "common_velocity":
        state[2:] += amount*direction
    elif family in ("release_speed", "release_direction"):
        u0 = np.asarray(nominal["relative_velocity_m_s"], dtype=float)
        if family == "release_speed":
            new_u = u0 + amount*u0/np.linalg.norm(u0)
        else:
            new_u = rotate(u0, amount)
        state, host_state, momentum_residual = reconstruct_mechanism_state(event, new_u)
    else:
        raise ValueError(f"unknown perturbation family {family}")
    terminal_state = campaign.coast(state, TERMINAL_TIME_S-float(event["time_s"]))
    target = np.asarray(nominal["target_terminal_state"], dtype=float)
    error = terminal_state-target
    return {
        "amount": amount, "payload_state": state.tolist(),
        "host_state": None if host_state is None else host_state.tolist(),
        "terminal_state": terminal_state.tolist(), "terminal_error_vector": error.tolist(),
        "position_error_m": float(np.linalg.norm(error[:2])),
        "velocity_error_m_s": float(np.linalg.norm(error[2:])),
        "momentum_residual_kg_m_s": momentum_residual,
    }


def sensitivity(event: dict, nominal: dict, name: str, family: str, axis: str, step: float) -> dict:
    plus = perturb_state(event, nominal, family, axis, step)
    minus = perturb_state(event, nominal, family, axis, -step)
    plus_half = perturb_state(event, nominal, family, axis, step/2)
    minus_half = perturb_state(event, nominal, family, axis, -step/2)
    y0 = np.asarray(nominal["terminal_state"], dtype=float)
    yp, ym = np.asarray(plus["terminal_state"]), np.asarray(minus["terminal_state"])
    yph, ymh = np.asarray(plus_half["terminal_state"]), np.asarray(minus_half["terminal_state"])
    full = (yp-ym)/(2*step)
    half = (yph-ymh)/step
    pos_sens = float(np.linalg.norm(full[:2]))
    vel_sens = float(np.linalg.norm(full[2:]))
    pos_sens_half = float(np.linalg.norm(half[:2]))
    vel_sens_half = float(np.linalg.norm(half[2:]))

    dp_plus, dp_minus = np.linalg.norm(yp[:2]-y0[:2]), np.linalg.norm(ym[:2]-y0[:2])
    dv_plus, dv_minus = np.linalg.norm(yp[2:]-y0[2:]), np.linalg.norm(ym[2:]-y0[2:])
    def symmetry(a, b, small):
        if max(a, b) <= small:
            return {"status":"NUMERICALLY_SMALL", "relative_difference":None, "passed":True}
        rel = abs(a-b)/max(a, b)
        return {"status":"CHECKED", "relative_difference":float(rel), "passed":bool(rel <= 0.05)}
    sym_pos, sym_vel = symmetry(dp_plus, dp_minus, SMALL_POSITION_M), symmetry(dv_plus, dv_minus, SMALL_VELOCITY_M_S)

    def convergence(a, b, small):
        if max(abs(a), abs(b)) <= small:
            return {"status":"NUMERICALLY_SMALL", "relative_difference":None, "passed":True}
        rel = abs(a-b)/max(abs(a), abs(b))
        return {"status":"CHECKED", "relative_difference":float(rel), "passed":bool(rel <= 0.02)}
    conv_pos = convergence(pos_sens, pos_sens_half, 1e-12)
    conv_vel = convergence(vel_sens, vel_sens_half, 1e-15)

    pos_margin = max(0.0, POSITION_BAND_M-float(nominal["position_error_m"]))
    vel_margin = max(0.0, VELOCITY_BAND_M_S-float(nominal["velocity_error_m_s"]))
    pos_allow = None if pos_sens <= 0 else pos_margin/pos_sens
    vel_allow = None if vel_sens <= 0 else vel_margin/vel_sens
    finite = [x for x in (pos_allow, vel_allow) if x is not None and math.isfinite(x)]
    allowance = min(finite) if finite else None
    momentum = [x["momentum_residual_kg_m_s"] for x in (plus, minus, plus_half, minus_half)
                if x["momentum_residual_kg_m_s"] is not None]
    momentum_pass = all(x <= 1e-9 for x in momentum)
    passed = sym_pos["passed"] and sym_vel["passed"] and conv_pos["passed"] and conv_vel["passed"] and momentum_pass
    return {
        "name": name, "family": family, "axis": axis, "step": step,
        "plus": plus, "minus": minus,
        "position_sensitivity_vector_per_unit": full[:2].tolist(),
        "velocity_sensitivity_vector_per_unit": full[2:].tolist(),
        "position_sensitivity_norm_per_unit": pos_sens,
        "velocity_sensitivity_norm_per_unit": vel_sens,
        "half_step_position_sensitivity_norm_per_unit": pos_sens_half,
        "half_step_velocity_sensitivity_norm_per_unit": vel_sens_half,
        "symmetry_position": sym_pos, "symmetry_velocity": sym_vel,
        "convergence_position": conv_pos, "convergence_velocity": conv_vel,
        "maximum_momentum_residual_kg_m_s": max(momentum) if momentum else None,
        "momentum_passed": momentum_pass,
        "position_margin_m": pos_margin, "velocity_margin_m_s": vel_margin,
        "position_allowance": pos_allow, "velocity_allowance": vel_allow,
        "local_linear_allowance": allowance,
        "allowance_label": "LOCAL_LINEAR_ALLOWANCE", "verification_passed": passed,
    }


def schedule_headroom(events: list[dict]) -> dict:
    times = [float(e["time_s"]) for e in events]
    if len(times) != 2 or not 0 < times[0] < times[1] < TERMINAL_TIME_S:
        raise ValueError("invalid selected release schedule")
    intervals = {
        "between_releases_s": times[1]-times[0],
        "first_release_to_terminal_s": TERMINAL_TIME_S-times[0],
        "second_release_to_terminal_s": TERMINAL_TIME_S-times[1],
    }
    return {
        "label":"SCHEDULE_HEADROOM_ONLY", "intervals":intervals,
        "markers_s":list(DEAD_TIME_MARKERS_S),
        "between_release_marker_pass":{str(m): bool(intervals["between_releases_s"] >= m) for m in DEAD_TIME_MARKERS_S},
        "interpretation":"timestamp headroom only; no slew, settling, thermal recovery or provider capability is modelled",
    }


def build() -> dict:
    s4 = load_s4()
    selection, row, candidate = selected_campaign(s4)
    events = candidate["events"]
    event_rows = []
    for index, event in enumerate(events):
        nominal = nominal_record(event)
        sensitivities = [sensitivity(event, nominal, *spec) for spec in PERTURBATIONS]
        event_rows.append({"event_index":index, "nominal":nominal, "sensitivities":sensitivities,
                           "verification_passed":all(s["verification_passed"] for s in sensitivities)})
    source_paths = [S4_PATH, CRITERIA_PATH, Path(__file__).resolve()]
    return {
        "study":"P113-S5", "status":"LOCAL_DETERMINISTIC_SENSITIVITY",
        "open_items":["P113","E5","P92"],
        "nominal_selection":selection,
        "nominal_order":row["order"], "nominal_release_times_s":row["release_times_s"],
        "terminal_bands":{"position_m":POSITION_BAND_M,"velocity_m_s":VELOCITY_BAND_M_S},
        "perturbation_steps":{name:step for name,_,_,step in PERTURBATIONS},
        "events":event_rows, "schedule_headroom":schedule_headroom(events),
        "source_sha256":{str(p.relative_to(ROOT)):sha256(p) for p in source_paths},
        "verification_passed":all(e["verification_passed"] for e in event_rows),
        "interpretation":"local deterministic sensitivity only; allowances are not hardware requirements or probability statements",
    }


def report(data: dict) -> str:
    lines = [
        "# Operational uncertainty around the S4 campaign", "",
        "Generated by `analysis/operational_uncertainty.py`. Do not hand-edit.", "",
        "**P113, E5 and P92 remain open. This is local deterministic sensitivity, not a probability of mission success or a hardware tolerance specification.**", "",
        f"The nominal case is the accepted S4 `{data['nominal_selection']['screen']}` fine-grid enumerated campaign, order `{data['nominal_order']}`, release times {data['nominal_release_times_s']} s. S4 uses this as a bounded comparator, not a flight requirement.", "",
        "![Terminal-state sensitivity](../figures/operational_uncertainty.svg)", "",
        "## One-at-a-time local linear allowances", "",
        "The values below use the remaining margin inside S3/S4's existing 10 m position and 0.01 m/s velocity bands. They are **LOCAL_LINEAR_ALLOWANCE** values only. They are not claimed navigation performance, mechanism accuracy or provider requirements.", "",
        "| Payload event | Perturbation | Position sensitivity | Velocity sensitivity | Local linear allowance | Verification |",
        "|---|---|---:|---:|---:|---|",
    ]
    for event in data["events"]:
        for s in event["sensitivities"]:
            unit = "rad" if s["name"] == "release_direction_rad" else "input unit"
            allowance = "—" if s["local_linear_allowance"] is None else f"{s['local_linear_allowance']:.6g} {unit}"
            lines.append(f"| {event['event_index']+1}: {event['nominal']['target']} | {s['name']} | {s['position_sensitivity_norm_per_unit']:.6g} m/unit | {s['velocity_sensitivity_norm_per_unit']:.6g} (m/s)/unit | {allowance} | {'PASS' if s['verification_passed'] else 'FAIL'} |")
    gaps = data["schedule_headroom"]["intervals"]
    lines += ["", "## Schedule headroom only", "",
              f"The two stored release epochs are separated by **{gaps['between_releases_s']:.0f} s**. The first and second releases have **{gaps['first_release_to_terminal_s']:.0f} s** and **{gaps['second_release_to_terminal_s']:.0f} s** remaining to the 3600 s terminal epoch.", "",
              "Study markers of 30, 60, 120 and 300 s are compared only to those timestamp gaps. Passing a marker does not establish host slew, settling, thermal recovery or manoeuvre capability. Those remain E5/provider inputs.", "",
              "## What this changes", "",
              "This run exposes which release-state terms consume the terminal-state bands fastest and therefore which quantities need explicit mission bounds before a release-cell tolerance is chosen. Common navigation error and mechanism-relative error remain separate in the ledger; a precise pusher cannot remove a common host-state error.", "",
              "The next campaign step is to combine declared navigation/pointing bounds and clearing/settling assumptions with the evolving-host campaign, then charge installed burden and failure topology. Do not convert these local linear allowances into hardware requirements without that step.", "",
              "## Verification", "",
              f"Overall declared numerical checks: **{'PASS' if data['verification_passed'] else 'FAIL'}**. The JSON retains positive/negative perturbations, half-step convergence, basis vectors, momentum residuals and source hashes.", "",
              "## Reproduce", "", "```bash", "python3 analysis/operational_uncertainty.py", "python3 analysis/operational_uncertainty.py --check", "python3 -m pytest tests/test_operational_uncertainty.py", "```", ""]
    return "\n".join(lines)


def svg(data: dict) -> str:
    rows = []
    for event in data["events"]:
        for s in event["sensitivities"]:
            rows.append((event["event_index"], s["name"], s["position_sensitivity_norm_per_unit"], s["velocity_sensitivity_norm_per_unit"]))
    width, height = 1280, 640
    left, top, chart_w, chart_h = 330, 90, 860, 450
    max_pos = max(r[2] for r in rows) or 1.0
    max_vel = max(r[3] for r in rows) or 1.0
    bar_h = chart_h / max(1, len(rows))
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
             '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#111827}.title{font-size:28px;font-weight:700}.label{font-size:12px}.axis{stroke:#94a3b8;stroke-width:1}.p{fill:#475569}.v{fill:#cbd5e1}</style>',
             '<text x="50" y="45" class="title">P113-S5 local terminal-state sensitivity</text>',
             '<text x="50" y="70" class="label">Bar lengths are normalized separately for position and velocity; no probability distribution is implied.</text>',
             f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+chart_h}" class="axis"/>']
    for i, (event_index, name, pos, vel) in enumerate(rows):
        y = top + i*bar_h + 2
        pw = 0.46*chart_w*pos/max_pos
        vw = 0.46*chart_w*vel/max_vel
        parts.append(f'<text x="50" y="{y+bar_h*0.55:.1f}" class="label">E{event_index+1} {name}</text>')
        parts.append(f'<rect x="{left}" y="{y:.1f}" width="{pw:.1f}" height="{bar_h*0.35:.1f}" class="p"/>')
        parts.append(f'<rect x="{left}" y="{y+bar_h*0.42:.1f}" width="{vw:.1f}" height="{bar_h*0.35:.1f}" class="v"/>')
    parts += [f'<text x="{left}" y="{top+chart_h+35}" class="label">dark: position sensitivity, max={max_pos:.6g} m/unit</text>',
              f'<text x="{left+430}" y="{top+chart_h+35}" class="label">light: velocity sensitivity, max={max_vel:.6g} (m/s)/unit</text>', '</svg>', '']
    return "\n".join(parts)


def serialized(data: dict) -> tuple[str, str, str]:
    return json.dumps(data, indent=2, sort_keys=True) + "\n", report(data), svg(data)


def numerical_match(actual, expected, path=(), step=1.0):
    """Reproducibility of computed leaves, separate from frozen physical bands.

    Position/velocity floors follow the S2/S3 policy. Central differences divide
    that coordinate noise by the declared step; comparisons retain exact schema,
    input steps and verdicts. Reports still reproduce the stored payload exactly.
    """
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        step = expected.get("step", step)
        return actual.keys() == expected.keys() and all(
            numerical_match(actual[k], v, path+(k,), step) for k, v in expected.items())
    if isinstance(expected, list):
        return len(actual) == len(expected) and all(
            numerical_match(a, b, path+(i,), step) for i, (a, b) in enumerate(zip(actual, expected)))
    if not isinstance(expected, float):
        return actual == expected
    field = path[-2] if isinstance(path[-1], int) else path[-1]
    atol, rtol = 1e-9, 1e-12
    if field in ("payload_state", "host_state", "terminal_state", "target_terminal_state", "terminal_error_vector"):
        atol = 1e-5 if path[-1] < 2 else 1e-7
    elif field in ("position_error_m", "position_margin_m", "reproduction_position_m"):
        atol = 1e-5
    elif field in ("velocity_error_m_s", "velocity_margin_m_s", "reproduction_velocity_m_s"):
        atol = 1e-7
    elif "sensitivity" in field:
        atol = 2*(1e-5 if "position" in field else 1e-7)/step
    elif field == "relative_difference":
        atol = 1e-5
    elif "allowance" in field:
        atol, rtol = 1e-10, 1e-5
    elif field in ("step", "amount", "retained_mass_kg", "mass_after_second_kg", "release_time_s"):
        return actual == expected
    return math.isfinite(actual) and math.isfinite(expected) and math.isclose(actual, expected, rel_tol=rtol, abs_tol=atol)


def check_outputs(data, root=ROOT):
    result_path = root / OUTPUT_JSON.relative_to(ROOT)
    try:
        stored = json.loads(result_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return [str(OUTPUT_JSON.relative_to(ROOT))]
    metadata = lambda d: {k: v for k, v in d.items() if k != "events"}
    if (not isinstance(stored, dict) or metadata(stored) != metadata(data)
            or not numerical_match(stored.get("events"), data["events"])):
        return [str(OUTPUT_JSON.relative_to(ROOT))]
    return [str(p.relative_to(ROOT)) for p, content in zip(
        (OUTPUT_DOC, OUTPUT_SVG), serialized(stored)[1:])
        if not (root/p.relative_to(ROOT)).exists()
        or (root/p.relative_to(ROOT)).read_text(encoding="utf-8") != content]


def write_or_check(check: bool) -> None:
    data = build()
    payloads = serialized(data)
    paths = (OUTPUT_JSON, OUTPUT_DOC, OUTPUT_SVG)
    if check:
        stale = check_outputs(data)
        if stale:
            raise SystemExit("stale P113-S5 outputs: " + ", ".join(stale))
        if not data["verification_passed"]:
            raise SystemExit("P113-S5 numerical verification bands failed; retain the failed run")
        print("P113-S5 outputs are fresh and declared numerical checks pass")
        return
    for path, text in zip(paths, payloads):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    if not data["verification_passed"]:
        raise SystemExit("P113-S5 generated with failed verification bands; inspect and retain the result")
    print("wrote P113-S5 operational-uncertainty evidence")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    write_or_check(args.check)


if __name__ == "__main__":
    main()
