#!/usr/bin/env python3
"""P129: user-selected Gen6 mixed-size, common-epoch J2 mission screen.

The target trajectories and all hardware/host inputs are explicit surrogates.
This is a ballistic sensitivity screen, not a mission solution or product rating.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "analysis/results/gen6_mixed_mission.json"
REPORT = ROOT / "validation/P129_gen6_mixed_mission.md"
FIGURE = ROOT / "figures/gen6_mixed_mission.svg"

MU = 3.986004418e14
RE = 6_378_137.0
J2 = 1.08262668e-3
ALT = 500_000.0
SIDEREAL_YEAR = 365.2422 * 86400.0
G0 = 9.80665
HOST_DRY = 300.0
HOST_FUEL = 10.0
HOST_ISP = 220.0
VOLLEY_DEVICE = 30.0  # recoil sensitivity only; not a designed mass
SPRING_DEVICE = 16.0  # 2 x 2 kg 1U + 2 x 6 kg 3U; unquoted class proxy
SPRING_SPEED = 2.5
SHOT_TIMES = (0.0, 1200.0, 2400.0, 3600.0)
EPOCH = SHOT_TIMES[-1] + 86400.0
PAYLOADS = (("1U-A", 1.33, 3.0), ("3U-A", 4.0, 5.0),
            ("1U-B", 1.33, 7.0), ("3U-B", 4.0, 9.0))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def scale(a, x):
    return tuple(v * x for v in a)


def norm(a):
    return math.sqrt(sum(x * x for x in a))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def j2_acceleration(r):
    x, y, z = r
    radius = norm(r)
    q = z * z / (radius * radius)
    common = -MU / radius**3
    j = 1.5 * J2 * (RE / radius)**2
    return (common*x*(1-j*(5*q-1)), common*y*(1-j*(5*q-1)),
            common*z*(1-j*(5*q-3)))


def derivative(state):
    return state[3:] + j2_acceleration(state[:3])


def rk4(state, h):
    k1 = derivative(state)
    k2 = derivative(add(state, scale(k1, h/2)))
    k3 = derivative(add(state, scale(k2, h/2)))
    k4 = derivative(add(state, scale(k3, h)))
    return tuple(x+h*(a+2*b+2*c+d)/6 for x, a, b, c, d in zip(state, k1, k2, k3, k4))


def propagate(state, start, finish, step):
    if finish < start:
        raise ValueError("backward propagation is not used")
    n = max(1, math.ceil((finish-start)/step))
    h = (finish-start)/n
    for _ in range(n):
        state = rk4(state, h)
    return state


def sso_inclination():
    a = RE+ALT
    n = math.sqrt(MU/a**3)
    cos_i = -(2*math.pi/SIDEREAL_YEAR)/(1.5*J2*n*(RE/a)**2)
    if not -1 <= cos_i <= 1:
        raise ValueError("sun-synchronous inclination unavailable")
    return math.acos(cos_i)


def initial_state():
    i = sso_inclination()
    v = math.sqrt(MU/(RE+ALT))
    return (RE+ALT, 0.0, 0.0, 0.0, v*math.cos(i), v*math.sin(i))


def tangent(state):
    v = state[3:]
    return scale(v, 1/norm(v))


def semi_major_axis(state):
    r, v = state[:3], state[3:]
    return 1/(2/norm(r)-dot(v, v)/MU)


def reference(step):
    start = initial_state()
    events = [propagate(start, 0, t, step) for t in SHOT_TIMES]
    end = propagate(start, 0, EPOCH, step)
    targets = []
    for (name, mass, dv), t, state in zip(PAYLOADS, SHOT_TIMES, events):
        departure = state[:3]+add(state[3:], scale(tangent(state), dv))
        terminal = propagate(departure, t, EPOCH, step)
        targets.append(dict(name=name, payload_kg=mass, target_departure_inertial_increment_m_s=dv,
                            release_time_s=t, departure_state_si=departure,
                            target_state_at_epoch_si=terminal,
                            initial_axis_rise_km=(semi_major_axis(departure)-semi_major_axis(state))/1000,
                            along_track_at_epoch_km=dot(sub(terminal[:3], end[:3]), tangent(end))/1000))
    return events, end, targets


def terminal_error(state, target):
    return dict(position_3d_km=norm(sub(state[:3], target[:3]))/1000,
                velocity_3d_m_s=norm(sub(state[3:], target[3:])))


def simulate(kind, targets, step):
    device = VOLLEY_DEVICE if kind == "volley" else SPRING_DEVICE
    host = initial_state()
    current = 0.0
    fuel = HOST_FUEL
    remaining = sum(p[1] for p in PAYLOADS)
    shots = []
    for target in targets:
        t = target["release_time_s"]
        host = propagate(host, current, t, step)
        current = t
        mass = target["payload_kg"]
        total = HOST_DRY+device+remaining+fuel
        host_v = host[3:]
        local_t = tangent(host)
        burn = (0.0, 0.0, 0.0)
        if kind == "spring":
            # Best local instantaneous velocity match at the *actual* host position.
            # It cannot undo the host's displacement caused by previous burns.
            for _ in range(12):
                used = total*(1-math.exp(-norm(burn)/(HOST_ISP*G0)))
                mass_at_release = total-used
                burn = sub(sub(target["departure_state_si"][3:], host_v),
                           scale(local_t, SPRING_SPEED*(1-mass/mass_at_release)))
            used = total*(1-math.exp(-norm(burn)/(HOST_ISP*G0)))
            fuel -= used
            host_v = add(host_v, burn)
            total -= used
            speed = SPRING_SPEED
        else:
            used = 0.0
            speed = target["target_departure_inertial_increment_m_s"]/(1-mass/total)
        relative = scale(local_t, speed)
        payload = host[:3]+add(host_v, scale(relative, 1-mass/total))
        host = host[:3]+sub(host_v, scale(relative, mass/total))
        terminal = propagate(payload, t, EPOCH, step)
        error = terminal_error(terminal, target["target_state_at_epoch_si"])
        shots.append(dict(name=target["name"], release_time_s=t, relative_release_m_s=speed,
                          local_host_burn_m_s=norm(burn), fuel_used_kg=used,
                          departure_position_error_m=norm(sub(payload[:3], target["departure_state_si"][:3])),
                          departure_velocity_error_m_s=norm(sub(payload[3:], target["departure_state_si"][3:])),
                          terminal_error=error, terminal_state_si=terminal))
        remaining -= mass
    return dict(installed_device_study_kg=device, fuel_remaining_kg=fuel,
                total_host_burn_m_s=sum(s["local_host_burn_m_s"] for s in shots), shots=shots)


def build(step=10.0):
    events, end, targets = reference(step)
    volley = simulate("volley", targets, step)
    spring = simulate("spring", targets, step)
    return dict(evidence_class="SURROGATE_BALLISTIC_SCREEN_NOT_MATCHED_OPTIMIZED_CAMPAIGN_OR_HARDWARE_RESULT",
                provenance=dict(source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),
                assumptions=dict(orbit_altitude_km=ALT/1000, sso_inclination_deg=math.degrees(sso_inclination()),
                                 raan_deg=0, circular_start=True, propagator="Cartesian RK4 with central Earth and J2 only",
                                 integration_step_s=step, target_epoch_s=EPOCH,
                                 release_times_s=SHOT_TIMES, host_dry_kg=HOST_DRY,
                                 host_initial_fuel_kg=HOST_FUEL, host_isp_s=HOST_ISP,
                                 volley_device_study_kg=VOLLEY_DEVICE,
                                 spring_device_class_kg=SPRING_DEVICE,
                                 spring_release_m_s=SPRING_SPEED,
                                 target_definition="Four independent inertial tangential 3/5/7/9 m/s impulses from unperturbed host at fixed times; all terminal states propagated to common epoch"),
                reference_host_state_at_epoch_si=end, reference_host_states_at_release_si=events,
                targets=targets, cases=dict(volley_no_host_correction=volley,
                                           spring_ideal_local_host_burn=spring),
                exclusions=["target states are constructed surrogates, not customer-requested orbital slots",
                            "no optimized host guidance or correction burns to retarget later release positions",
                            "instantaneous burns/releases; no finite thrust, slew, duty cycle, collision or disposal",
                            "no drag, third bodies, gravity harmonics beyond J2, navigation covariance or tracking",
                            "device masses, 1U/3U payload masses, spring speed and host propulsion are unquoted study inputs",
                            "VOLLEY release 3/5/7/9 m/s is commanded-input scenario, not achieved mechanism range",
                            "spring comparator is a local velocity-matching policy, not the best possible campaign"])


def report(d, convergence):
    targets = d["targets"]
    volley = d["cases"]["volley_no_host_correction"]
    spring = d["cases"]["spring_ideal_local_host_burn"]
    lines = ["# P129 — Gen6 mixed-size full-state mission screen", "",
             "**Status:** user-selected service architecture with surrogate numeric inputs; ballistic requirements screen, not a solved customer mission or achieved VOLLEY release capability.", "",
             "The selected service is two ordinary passive 1U and two ordinary passive 3U spacecraft from a rideshare/OTV host, released within one orbit. Each should reach a distinct **position and velocity at one common epoch**, 24 hours after the last release. The target pattern varies both initial orbit energy and resulting along-track position while remaining in one plane. The buyer is hypothesized to be the host operator; no customer or provider has approved the case.", "",
             f"This numerical reference starts from a circular 500 km orbit at the first-order J2 sun-synchronous inclination ({d['assumptions']['sso_inclination_deg']:.3f}°). Four releases occur at 0/20/40/60 minutes; the epoch is 25 hours after the first release. Payload masses of 1.33/4/1.33/4 kg, a 300 kg base host, 10 kg fuel, 220 s Isp, a 30 kg VOLLEY *recoil study mass* and a 16 kg spring-class installed proxy are **assumptions, not selected hardware or supplier limits**.", "",
             "## Independent target construction", "",
             "For a reproducible full-state challenge, each target is generated by an inertial prograde 3/5/7/9 m/s impulse from an **unperturbed reference host** at the assigned time, followed by Cartesian J2 propagation to the common epoch. This construction is transparent but favors a prograde release topology; real service targets must come from a customer. It also does not prove that the specified 1U or 3U can tolerate a particular deployment system.", "",
             "| Payload | Mass | Trial inertial increment | Initial semimajor-axis rise | Along-track at common epoch vs reference host |", "|:--|--:|--:|--:|--:|"]
    for t in targets:
        lines.append(f"| {t['name']} | {t['payload_kg']:.2f} kg | {t['target_departure_inertial_increment_m_s']:.1f} m/s | {t['initial_axis_rise_km']:.2f} km | {t['along_track_at_epoch_km']:.1f} km |")
    lines += ["", "## Two deliberately limited policies", "",
              "The VOLLEY policy commands the recoil-corrected relative speed for each trial impulse but makes **no host correction** after recoil. The spring policy uses a fixed 2.5 m/s relative release and an optimistic instantaneous host burn at each actual release position to match the target *departure velocity*. It cannot reset a displaced host to the reference position. These are policy screens, **not optimized equal-capability mission plans**; neither terminal residual proves a winner.", "",
              "| Payload | VOLLEY relative command | VOLLEY terminal position / velocity miss | Spring host burn | Spring terminal position / velocity miss |", "|:--|--:|--:|--:|--:|"]
    for a, b in zip(volley["shots"], spring["shots"]):
        lines.append(f"| {a['name']} | {a['relative_release_m_s']:.3f} m/s | {a['terminal_error']['position_3d_km']:.3f} km / {a['terminal_error']['velocity_3d_m_s']:.4f} m/s | {b['local_host_burn_m_s']:.3f} m/s | {b['terminal_error']['position_3d_km']:.3f} km / {b['terminal_error']['velocity_3d_m_s']:.4f} m/s |")
    lines += ["", f"The spring policy spends {HOST_FUEL-spring['fuel_remaining_kg']:.3f} kg of its assumed initial 10 kg fuel in ideal local impulses; VOLLEY spends no host propellant in this policy but carries an assumed {VOLLEY_DEVICE:.1f} kg device versus {SPRING_DEVICE:.1f} kg for the spring class. Power, integration, reliability and payload-side costs are absent. A stronger optimizer may change either side and must be tried before claiming a service benefit.", "",
              f"Numerical check: halving the fixed RK4 step from 10 to 5 s changes the largest target terminal position by at most **{convergence['max_target_position_difference_m']:.2f} m** and velocity by **{convergence['max_target_velocity_difference_m_s']:.5f} m/s**. This measures time-step error only; it does not cover force-model error, drag or operational uncertainty.", "",
              "**G0 disposition remains partial.** Full target vectors are now explicit, but they are generated surrogates, and neither policy closes a provider-approved four-shot campaign. Next: name a public 1U/3U reference spacecraft and OTV interface, set meaningful state/collision/disposal tolerances, optimize both host-control policies on the same resource budget, and price installed burden. Keep the original four-identical-3U P128 as a separate historical screen.", "",
              "![Four mixed-size targets and terminal misses](../figures/gen6_mixed_mission.svg)", "",
              "Reproduce with `python3 analysis/gen6_mixed_mission.py`; `--check` verifies the captured data, report and figure within strict cross-runtime floating tolerance. No physical or customer validation is implied.", ""]
    return "\n".join(lines)


def figure(d):
    rows = d["targets"]
    v = d["cases"]["volley_no_host_correction"]["shots"]
    s = d["cases"]["spring_ideal_local_host_burn"]["shots"]
    marks = []
    for i, (t, a, b) in enumerate(zip(rows, v, s)):
        y = 128+55*i
        marks.append(f'<text x="25" y="{y}" font-size="15">{t["name"]}</text><rect x="110" y="{y-18}" width="{abs(t["along_track_at_epoch_km"])*0.1:.1f}" height="18" fill="#087e91"/><text x="380" y="{y}" font-size="14">{t["along_track_at_epoch_km"]:.1f} km</text><text x="570" y="{y}" font-size="14">{a["terminal_error"]["position_3d_km"]:.3f} / {b["terminal_error"]["position_3d_km"]:.3f} km</text>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="400" viewBox="0 0 1000 400">'
            '<rect width="100%" height="100%" fill="#f6f9fb"/>'
            '<text x="25" y="42" font-size="22" font-weight="bold">Gen6 · mixed-size, common-epoch mission screen</text>'
            '<text x="25" y="74" font-size="14">2 × 1U + 2 × 3U · 500 km SSO surrogate · four releases in one orbit</text>'
            '<text x="100" y="105" font-size="15" font-weight="bold">Target along-track shift</text>'
            '<text x="570" y="105" font-size="15" font-weight="bold">Terminal position miss: VOLLEY / spring policy</text>'
            +''.join(marks)+
            '<text x="25" y="370" font-size="13">Surrogate targets and unoptimized policies; misses do not establish service superiority.</text></svg>\n')


def equivalent(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(equivalent(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(equivalent(x, y) for x, y in zip(a, b))
    if isinstance(a, (int, float)) and not isinstance(a, bool) and isinstance(b, (int, float)) and not isinstance(b, bool):
        return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-3)
    return type(a) is type(b) and a == b


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = build()
    finer = build(5.0)
    convergence = dict(max_target_position_difference_m=max(norm(sub(a["target_state_at_epoch_si"][:3], b["target_state_at_epoch_si"][:3])) for a, b in zip(data["targets"], finer["targets"])),
                       max_target_velocity_difference_m_s=max(norm(sub(a["target_state_at_epoch_si"][3:], b["target_state_at_epoch_si"][3:])) for a, b in zip(data["targets"], finer["targets"])))
    data["time_step_convergence"] = convergence
    if convergence["max_target_position_difference_m"] >= 1.0 or convergence["max_target_velocity_difference_m_s"] >= 0.001:
        raise AssertionError("J2 propagation time-step screen does not resolve terminal target")
    if HOST_FUEL-finer["cases"]["spring_ideal_local_host_burn"]["fuel_remaining_kg"] > HOST_FUEL:
        raise AssertionError("fuel budget exceeded")
    if not 95 < data["assumptions"]["sso_inclination_deg"] < 100:
        raise AssertionError("SSO inclination outside expected range")
    result = json.dumps(data, indent=2)+"\n"
    prose, graphic = report(data, convergence), figure(data)
    if args.check:
        if not RESULT.exists() or not equivalent(data, json.loads(RESULT.read_text())):
            raise AssertionError("P129 result stale")
        if REPORT.read_text() != prose or FIGURE.read_text() != graphic:
            raise AssertionError("P129 report or figure stale")
        print("P129 mixed-size mission: data, report and figure current")
    else:
        RESULT.write_text(result)
        REPORT.write_text(prose)
        FIGURE.write_text(graphic)
        print("P129 mixed-size mission generated")


if __name__ == "__main__":
    main()
