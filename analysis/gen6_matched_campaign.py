#!/usr/bin/env python3
"""P130: fixed-time, matched full-state four-release J2 campaign.

Ideal instantaneous pre-release and post-release host burns are allowed for
both architectures. This is a constructive feasibility screen, not a global
optimum, hardware rating, or customer mission design.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import gen6_mixed_mission as p129

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "analysis/results/gen6_matched_campaign.json"
REPORT = ROOT / "validation/P130_gen6_matched_campaign.md"
FIGURE = ROOT / "figures/gen6_matched_campaign.svg"


def solve3(matrix, rhs):
    a = [list(row) + [rhs[i]] for i, row in enumerate(matrix)]
    for col in range(3):
        pivot = max(range(col, 3), key=lambda i: abs(a[i][col]))
        a[col], a[pivot] = a[pivot], a[col]
        if abs(a[col][col]) < 1e-9:
            raise ValueError("transfer shooting Jacobian singular")
        d = a[col][col]
        a[col] = [x / d for x in a[col]]
        for row in range(3):
            if row != col:
                d = a[row][col]
                a[row] = [x - d * y for x, y in zip(a[row], a[col])]
    return tuple(row[3] for row in a)


def transfer_departure_velocity(position, guess, start, finish, target_position, step):
    """Shoot a Cartesian J2 arc to the next *reference* release position."""
    velocity = guess
    evaluations = 0
    for _ in range(7):
        terminal = p129.propagate(position + velocity, start, finish, step)
        evaluations += 1
        residual = p129.sub(terminal[:3], target_position)
        if p129.norm(residual) < 1e-4:
            return velocity, terminal, evaluations
        columns = []
        for axis in range(3):
            bumped = list(velocity)
            bumped[axis] += 0.01
            end = p129.propagate(position + tuple(bumped), start, finish, step)
            evaluations += 1
            columns.append(p129.scale(p129.sub(end[:3], terminal[:3]), 100.0))
        jacobian = tuple(tuple(columns[j][i] for j in range(3)) for i in range(3))
        delta = solve3(jacobian, p129.scale(residual, -1.0))
        velocity = p129.add(velocity, delta)
    raise AssertionError("J2 transfer shooting did not converge")


def burn_propellant(total_mass, delta_v):
    return total_mass * (1 - math.exp(-delta_v / (p129.HOST_ISP * p129.G0)))


def case(kind, targets, reference_events, step, spring_speed=2.5,
         volley_device=30.0, spring_device=16.0):
    device = volley_device if kind == "volley" else spring_device
    fuel = p129.HOST_FUEL
    remaining = sum(p[1] for p in p129.PAYLOADS)
    host = p129.initial_state()
    shots = []
    burns = []
    for index, target in enumerate(targets):
        release_time = target["release_time_s"]
        desired = target["departure_state_si"]
        if p129.norm(p129.sub(host[:3], desired[:3])) > 1e-3:
            raise AssertionError("host is not at common target release position")
        mass = target["payload_kg"]
        before = p129.HOST_DRY + device + remaining + fuel
        reference_tangent = p129.tangent(reference_events[index])
        relative_speed = (target["target_departure_inertial_increment_m_s"]
                          / (1 - mass / before)) if kind == "volley" else spring_speed
        relative = p129.scale(reference_tangent, relative_speed)
        # Fuel used by the pre-release burn slightly changes the recoil fraction.
        used = 0.0
        for _ in range(12):
            after = before - used
            needed_host_velocity = p129.sub(desired[3:], p129.scale(relative, 1 - mass / after))
            delta = p129.sub(needed_host_velocity, host[3:])
            next_used = burn_propellant(before, p129.norm(delta))
            if abs(next_used-used) < 1e-13:
                used = next_used
                break
            used = next_used
        if used > fuel:
            raise AssertionError("insufficient fuel for pre-release burn")
        fuel -= used
        after = before - used
        needed_host_velocity = p129.sub(desired[3:], p129.scale(relative, 1 - mass / after))
        delta = p129.sub(needed_host_velocity, host[3:])
        burns.append(dict(event=f"pre {target['name']}", delta_v_m_s=p129.norm(delta), fuel_kg=used))
        payload = desired[:3] + p129.add(needed_host_velocity, p129.scale(relative, 1 - mass / after))
        host = desired[:3] + p129.sub(needed_host_velocity, p129.scale(relative, mass / after))
        terminal = p129.propagate(payload, release_time, p129.EPOCH, step)
        error = p129.terminal_error(terminal, target["target_state_at_epoch_si"])
        # Deterministic local perturbations; no distribution or navigation claim.
        radial = p129.scale(desired[:3], 1 / p129.norm(desired[:3]))
        pitch = math.radians(1.0)
        perturbations = {}
        for name, perturbation in (
            ("speed_plus_0p1_m_s", p129.scale(reference_tangent, 0.1 * (1-mass/after))),
            ("pitch_plus_1_deg", p129.scale(
                p129.add(p129.scale(reference_tangent, math.cos(pitch)-1),
                         p129.scale(radial, math.sin(pitch))), relative_speed * (1-mass/after))),
        ):
            perturbed = p129.propagate(payload[:3] + p129.add(payload[3:], perturbation),
                                        release_time, p129.EPOCH, step)
            perturbations[name] = p129.terminal_error(perturbed, terminal)
        shots.append(dict(name=target["name"], relative_speed_m_s=relative_speed,
                          preburn_delta_v_m_s=p129.norm(delta), terminal_error=error,
                          one_at_a_time_release_perturbations=perturbations))
        remaining -= mass
        if index + 1 < len(targets):
            next_time = targets[index+1]["release_time_s"]
            next_position = reference_events[index+1][:3]
            velocity, arrival, evaluations = transfer_departure_velocity(
                host[:3], host[3:], release_time, next_time, next_position, step)
            transfer_delta = p129.norm(p129.sub(velocity, host[3:]))
            total = p129.HOST_DRY + device + remaining + fuel
            used = burn_propellant(total, transfer_delta)
            if used > fuel:
                raise AssertionError("insufficient fuel for transfer burn")
            fuel -= used
            burns.append(dict(event=f"transfer to {targets[index+1]['name']}",
                              delta_v_m_s=transfer_delta, fuel_kg=used,
                              shooting_evaluations=evaluations,
                              arrival_position_error_m=p129.norm(p129.sub(arrival[:3], next_position))))
            host = arrival
    return dict(device_assumption_kg=device, fuel_used_kg=p129.HOST_FUEL-fuel,
                fuel_remaining_kg=fuel,
                total_host_delta_v_m_s=sum(b["delta_v_m_s"] for b in burns),
                maximum_host_burn_m_s=max(b["delta_v_m_s"] for b in burns),
                burns=burns, shots=shots)


def build(step=10.0):
    events, _, targets = p129.reference(step)
    volley = case("volley", targets, events, step)
    spring = case("spring", targets, events, step)
    sweep = []
    for spring_speed in (0.5, 1.0, 2.0, 2.5, 3.0):
        alt = case("spring", targets, events, step, spring_speed=spring_speed)
        sweep.append(dict(spring_speed_m_s=spring_speed, host_fuel_kg=alt["fuel_used_kg"],
                          total_host_delta_v_m_s=alt["total_host_delta_v_m_s"]))
    saved_fuel = spring["fuel_used_kg"]-volley["fuel_used_kg"]
    return dict(evidence_class="MATCHED_FULL_STATE_CONSTRUCTIVE_SURROGATE_NOT_OPTIMIZED_OR_HARDWARE_VALIDATED",
                provenance=dict(source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                                p129_source_sha256=hashlib.sha256(Path(p129.__file__).read_bytes()).hexdigest()),
                assumptions=dict(integration_step_s=step, dynamics="P129 Cartesian central Earth + J2 RK4",
                                 target_definition="P129 unperturbed-host prograde departure vectors at 0/20/40/60 min, common epoch 24h after final release",
                                 control_policy="fixed release times; one ideal pre-release burn at each event and one ideal post-release transfer burn between events; transfer shooting enforces reference release positions",
                                 host_dry_kg=p129.HOST_DRY, host_initial_fuel_kg=p129.HOST_FUEL,
                                 host_isp_s=p129.HOST_ISP, volley_device_assumption_kg=30.0,
                                 spring_device_assumption_kg=16.0, spring_nominal_speed_m_s=2.5,
                                 release_direction="reference-orbit prograde for both devices"),
                volley=volley, spring=spring, spring_speed_sensitivity=sweep,
                installed_mass_difference_assumed_kg=14.0,
                fuel_saved_by_volley_kg=saved_fuel,
                installed_plus_consumed_mass_difference_kg=14.0-saved_fuel,
                exclusions=["No global optimization over burn timing, release time, release direction or target assignment",
                            "Instantaneous host impulses and releases; no finite thrust, slew, thermal, power, pointing or structural constraints",
                            "3/5/7/9 m/s VOLLEY commands are hypothetical and exceed the 3–6 m/s first-article proposed range",
                            "The target construction favors prograde commanded release, so it is not an independent customer job",
                            "No tracking, covariance, drag, collision, recontact, disposal, reliability, cost or approved provider ICD",
                            "Device masses, spring speed, fuel capacity and host propulsion remain unsourced study assumptions"])


def report(data, convergence):
    v, s = data["volley"], data["spring"]
    rows = []
    for a, b in zip(v["shots"], s["shots"]):
        rows.append(f"| {a['name']} | {a['relative_speed_m_s']:.3f} | {b['relative_speed_m_s']:.3f} | {a['terminal_error']['position_3d_km']*1000:.4f} / {a['terminal_error']['velocity_3d_m_s']:.6f} | {b['terminal_error']['position_3d_km']*1000:.4f} / {b['terminal_error']['velocity_3d_m_s']:.6f} |")
    sensitivity = [f"| {x['spring_speed_m_s']:.1f} | {x['host_fuel_kg']:.4f} | {x['total_host_delta_v_m_s']:.3f} |" for x in data["spring_speed_sensitivity"]]
    perturbations = []
    for a, b in zip(v["shots"], s["shots"]):
        vp = a["one_at_a_time_release_perturbations"]
        sp = b["one_at_a_time_release_perturbations"]
        perturbations.append(f"| {a['name']} | {vp['speed_plus_0p1_m_s']['position_3d_km']:.2f} | {sp['speed_plus_0p1_m_s']['position_3d_km']:.2f} | {vp['pitch_plus_1_deg']['position_3d_km']:.2f} | {sp['pitch_plus_1_deg']['position_3d_km']:.2f} |")
    return "\n".join([
        "# P130 — matched four-release full-state campaign", "",
        "**Status:** constructive J2 surrogate with ideal instantaneous control. Both options reach the **same four full-state targets** at the P129 common epoch. This is not a global optimum, mission approval, or achieved mechanism capability.", "",
        "## Fairer control construction", "",
        "Starting with P129's identical payload, host, target, time and gravity inputs, both options use the **same permitted control schedule**: one ideal host burn immediately before each release and one ideal host transfer burn immediately after each release except the last. A three-axis J2 shooting calculation makes each subsequent host arrival coincide with the reference release position; the pre-release burn then gives the payload the target departure velocity, with ejection recoil and expended propellant included. This is a fixed-time feasible construction, not the fuel-minimum campaign or an operational guidance solution. It resolves P129's intentionally weak local-velocity spring comparison.", "",
        "| Payload | VOLLEY commanded relative m/s | Spring relative m/s | VOLLEY terminal position m / velocity m/s | Spring terminal position m / velocity m/s |",
        "|:--|--:|--:|--:|--:|", *rows, "",
        "| Assumed architecture | Host Δv sum | Host fuel consumed | Assumed installed device | Initial device + consumed fuel |",
        "|:--|--:|--:|--:|--:|",
        f"| Commanded VOLLEY | {v['total_host_delta_v_m_s']:.3f} m/s | {v['fuel_used_kg']:.4f} kg | 30 kg | {30+v['fuel_used_kg']:.4f} kg |",
        f"| Fixed 2.5 m/s spring | {s['total_host_delta_v_m_s']:.3f} m/s | {s['fuel_used_kg']:.4f} kg | 16 kg | {16+s['fuel_used_kg']:.4f} kg |", "",
        f"At these assumed masses, commanded release saves **{data['fuel_saved_by_volley_kg']:.4f} kg** of ideal host fuel but starts with **14 kg** more installed device. Its device-plus-consumed-fuel burden is **{data['installed_plus_consumed_mass_difference_kg']:.4f} kg higher**. This does **not** close a product benefit. Power, spacecraft impacts, cost and reliability are unpriced. The break-even installed-mass premium under this narrow fuel-only measure is no more than {data['fuel_saved_by_volley_kg']:.4f} kg, far below the assumed 14 kg premium.", "",
        "## Spring speed sensitivity", "",
        "The published NRCSD 0.5–2.0 m/s is an **ISS deployer payload-survival requirement**, not this hypothetical SSO spring's rating. The 2.5 m/s nominal value is a study input. This sweep tests input sensitivity without claiming that any named dispenser performs at each speed.", "",
        "| Fixed spring study speed, m/s | Host fuel, kg | Host Δv sum, m/s |", "|--:|--:|--:|", *sensitivity, "",
        "## One-at-a-time release error sensitivity", "",
        "With the nominal host burns held fixed, a **+0.1 m/s relative release-speed error** or a **+1° pitch error** is injected separately at each shot. The table gives 3-D position difference at the common epoch in km. These arbitrary perturbations are illustrative, not measured dispersions, probabilities, customer tolerances or a guidance covariance budget. They show why perfect mathematical terminal matching is not an accuracy claim.", "",
        "| Payload | VOLLEY +0.1 m/s | Spring +0.1 m/s | VOLLEY +1° | Spring +1° |", "|:--|--:|--:|--:|--:|", *perturbations, "",
        f"Halving RK4 step from 10 to 5 s changes the two case fuel totals by no more than {convergence['max_fuel_change_kg']:.8f} kg; maximum inter-release arrival position residual is {convergence['max_transfer_position_residual_m']:.6f} m, and all four terminal full-state residuals are below {convergence['max_terminal_position_residual_m']:.6f} m and {convergence['max_terminal_velocity_residual_m_s']:.9f} m/s. These are numerical checks, **not** guidance/navigation error bounds. The chosen 3–9 m/s surrogate release commands are unproven; 9 m/s is beyond the proposed 3–6 m/s single-dummy first article.", "",
        "The named [1U, 3U, dispenser and host-service references](../docs/GEN6_GO1_PUBLIC_REFERENCE_AUDIT.md) support only class context, not an applicable provider ICD. The comparison still needs independently specified customer states and tolerances, installed masses from a real design/BOM, finite-burn and attitude constraints, covariance, collision/disposal and an optimization over schedule and direction. Spring plus host can hit these four targets mathematically, so P129's large spring residuals must **not** be used as evidence of VOLLEY advantage.", "",
        "![Matched full-state campaign resource comparison](../figures/gen6_matched_campaign.svg)", "",
        "Reproduce with `python3 analysis/gen6_matched_campaign.py`; use `--check` for the captured report, figure and JSON. Input and source hashes are in the JSON.", ""
    ])


def figure(data):
    v, s = data["volley"], data["spring"]
    maxfuel = max(v["fuel_used_kg"], s["fuel_used_kg"])
    def bar(y, mass, fuel, label, color):
        x = 320
        scale = 13
        return (f'<text x="26" y="{y+19}" font-size="18">{label}</text>'
                f'<rect x="{x}" y="{y}" width="{mass*scale:.1f}" height="28" fill="{color}"/>'
                f'<rect x="{x+mass*scale:.1f}" y="{y}" width="{fuel*scale:.1f}" height="28" fill="#f1b447"/>'
                f'<text x="{x+(mass+fuel)*scale+12:.1f}" y="{y+19}" font-size="16">{mass+fuel:.2f} kg</text>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="350" viewBox="0 0 1000 350">'
            '<rect width="100%" height="100%" fill="#f6f9fb"/>'
            '<text x="26" y="46" font-size="24" font-weight="bold">Gen6 G0 · matched four-release surrogate</text>'
            '<text x="26" y="78" font-size="16">Both options reach identical four full-state targets with ideal host burns</text>'
            +bar(115, 30, v["fuel_used_kg"], "Commanded release", "#087e91")
            +bar(175, 16, s["fuel_used_kg"], "Fixed 2.5 m/s spring", "#53637c")+
            '<rect x="320" y="245" width="17" height="17" fill="#087e91"/><text x="345" y="259" font-size="14">Assumed installed device</text>'
            '<rect x="570" y="245" width="17" height="17" fill="#f1b447"/><text x="595" y="259" font-size="14">Ideal host fuel consumed</text>'
            '<text x="26" y="318" font-size="14">Surrogate assumptions · no actual device BOM, customer target, provider ICD or hardware demonstration</text></svg>\n')


def equivalent(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(equivalent(a[k], b[k]) for k in a)
    if isinstance(a, (tuple, list)) and isinstance(b, (tuple, list)):
        return len(a) == len(b) and all(equivalent(x, y) for x, y in zip(a, b))
    if isinstance(a, (int, float)) and not isinstance(a, bool) and isinstance(b, (int, float)) and not isinstance(b, bool):
        return math.isclose(a, b, rel_tol=1e-8, abs_tol=1e-5)
    return type(a) is type(b) and a == b


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data, finer = build(10), build(5)
    cases = (data["volley"], data["spring"], finer["volley"], finer["spring"])
    errors = [shot["terminal_error"] for case_data in cases for shot in case_data["shots"]]
    arrivals = [burn.get("arrival_position_error_m", 0) for case_data in cases for burn in case_data["burns"]]
    convergence = dict(max_fuel_change_kg=max(abs(data[k]["fuel_used_kg"]-finer[k]["fuel_used_kg"]) for k in ("volley", "spring")),
                       max_transfer_position_residual_m=max(arrivals),
                       max_terminal_position_residual_m=max(e["position_3d_km"]*1000 for e in errors),
                       max_terminal_velocity_residual_m_s=max(e["velocity_3d_m_s"] for e in errors))
    data["numerical_checks"] = convergence
    if (convergence["max_fuel_change_kg"] > 1e-4 or
            convergence["max_transfer_position_residual_m"] > 1e-3 or
            convergence["max_terminal_position_residual_m"] > 1e-3 or
            convergence["max_terminal_velocity_residual_m_s"] > 1e-6):
        raise AssertionError("matched campaign did not meet numerical residual checks")
    prose, graphic = report(data, convergence), figure(data)
    if args.check:
        if not RESULT.exists() or not equivalent(data, json.loads(RESULT.read_text())):
            raise AssertionError("P130 data stale")
        if REPORT.read_text() != prose or FIGURE.read_text() != graphic:
            raise AssertionError("P130 report or figure stale")
        print("P130 matched full-state campaign current")
    else:
        RESULT.write_text(json.dumps(data, indent=2)+"\n")
        REPORT.write_text(prose)
        FIGURE.write_text(graphic)
        print("P130 matched full-state campaign generated")


if __name__ == "__main__":
    main()
