#!/usr/bin/env python3
"""One-event mass and fuel screen for the Gen5 matched reference.

Evidence class: deterministic algebraic sensitivity, not a complete campaign,
motor rating, provider mission, or launch-mass quote. Uses only Python stdlib.
The published 10 kg fixed-fuel case is kept separate from the hypothetical
one-event case whose fuel load is resized with the same 2 kg reserve.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P122 = ROOT / "analysis/results/gen5_finite_force_sensitivity.json"
SNAPSHOT = ROOT / "analysis/results/gen5_one_event_mass_screen.json"

PAYLOAD_KG = 4.0
COUNT = 12
HOST_BASE_DRY_KG = 300.0
FIXED_FUEL_KG = 10.0
RESERVE_KG = 2.0
ISP_S = 220.0
G0_M_S2 = 9.80665
TARGET_M_S = 16.029
SPRING_DEVICE_KG = 72.0
SPRING_RELEASE_M_S = 2.5
GEN5_DEVICE_KG = 126.562
GEN5_FINITE_RELEASE_M_S = 12.448437098832297


def bisect(function, low: float, high: float) -> float:
    """Return a bracketed root after 100 deterministic bisection steps."""
    if function(low) > 0 or function(high) < 0:
        raise ValueError("root is not bracketed")
    for _ in range(100):
        middle = (low + high) / 2
        if function(middle) > 0:
            high = middle
        else:
            low = middle
    return (low + high) / 2


def event(release_m_s: float, device_kg: float, fuel_kg: float) -> dict:
    """One ideal preburn and recoil-corrected release at the common target."""
    initial_kg = HOST_BASE_DRY_KG + device_kg + COUNT * PAYLOAD_KG + fuel_kg
    exhaust_m_s = ISP_S * G0_M_S2

    def target_residual(burn_m_s: float) -> float:
        release_mass_kg = initial_kg * math.exp(-burn_m_s / exhaust_m_s)
        payload_increment = burn_m_s + (
            1 - PAYLOAD_KG / release_mass_kg
        ) * release_m_s
        return payload_increment - TARGET_M_S

    burn_m_s = bisect(target_residual, 0.0, TARGET_M_S + release_m_s)
    used_kg = initial_kg * (1 - math.exp(-burn_m_s / exhaust_m_s))
    return {
        "preburn_m_s": burn_m_s,
        "propellant_used_kg": used_kg,
        "target_residual_m_s": target_residual(burn_m_s),
    }


def one_event_fuel_load(release_m_s: float, device_kg: float) -> float:
    """Re-solve initial fuel, including its effect on preburn mass."""
    return bisect(
        lambda fuel: fuel - RESERVE_KG
        - event(release_m_s, device_kg, fuel)["propellant_used_kg"],
        RESERVE_KG,
        30.0,
    )


def parity_device_mass(release_m_s: float, spring_fuel_kg: float) -> float:
    """Device mass giving equal device-plus-one-event-fuel mass."""
    spring_proxy_kg = SPRING_DEVICE_KG + spring_fuel_kg
    return bisect(
        lambda device: device
        + one_event_fuel_load(release_m_s, device)
        - spring_proxy_kg,
        0.0,
        200.0,
    )


def build() -> dict:
    cases = json.loads(P122.read_text())["cases"]
    spring_fixed = event(SPRING_RELEASE_M_S, SPRING_DEVICE_KG, FIXED_FUEL_KG)
    gen5_fixed = event(GEN5_FINITE_RELEASE_M_S, GEN5_DEVICE_KG, FIXED_FUEL_KG)
    spring_fuel = one_event_fuel_load(SPRING_RELEASE_M_S, SPRING_DEVICE_KG)
    gen5_fuel = one_event_fuel_load(GEN5_FINITE_RELEASE_M_S, GEN5_DEVICE_KG)
    rows = []
    for case in cases:
        speed = case["ideal_speed_conversion_m_s"]
        required_fuel = one_event_fuel_load(speed, GEN5_DEVICE_KG)
        rows.append({
            "case": case["name"],
            "ideal_release_conversion_m_s": speed,
            "one_event_loaded_fuel_kg": required_fuel,
            "gen5_minus_spring_device_plus_fuel_kg":
                GEN5_DEVICE_KG + required_fuel
                - SPRING_DEVICE_KG - spring_fuel,
        })
    return {
        "evidence_class": "deterministic one-event reference algebra; not a motor rating, twelve-release campaign, provider mission, or hardware validation",
        "inputs": {
            "payload_kg": PAYLOAD_KG,
            "payload_count": COUNT,
            "host_base_dry_kg": HOST_BASE_DRY_KG,
            "fixed_fuel_kg": FIXED_FUEL_KG,
            "reserve_kg": RESERVE_KG,
            "host_isp_s": ISP_S,
            "target_inertial_increment_m_s": TARGET_M_S,
            "spring_device_kg": SPRING_DEVICE_KG,
            "spring_release_m_s": SPRING_RELEASE_M_S,
            "gen5_modeled_device_kg": GEN5_DEVICE_KG,
            "gen5_ideal_finite_release_conversion_m_s": GEN5_FINITE_RELEASE_M_S,
        },
        "fixed_10kg_fuel": {
            "spring": spring_fixed,
            "gen5_ideal_finite_force": gen5_fixed,
            "propellant_saving_kg":
                spring_fixed["propellant_used_kg"]
                - gen5_fixed["propellant_used_kg"],
            "device_dry_mass_penalty_kg": GEN5_DEVICE_KG - SPRING_DEVICE_KG,
        },
        "hypothetical_resized_one_event_fuel": {
            "reserve_kg": RESERVE_KG,
            "spring_loaded_fuel_kg": spring_fuel,
            "gen5_loaded_fuel_kg": gen5_fuel,
            "gen5_minus_spring_device_plus_fuel_kg":
                GEN5_DEVICE_KG + gen5_fuel
                - SPRING_DEVICE_KG - spring_fuel,
            "gen5_device_mass_for_proxy_parity_kg":
                parity_device_mass(GEN5_FINITE_RELEASE_M_S, spring_fuel),
        },
        "p122_ideal_geometry_cases": rows,
    }


def compare_snapshot(expected: object, actual: object, name: str = "root") -> None:
    """Check the committed result numerically, allowing platform roundoff."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict) or set(expected) != set(actual):
            raise AssertionError(f"{name}: result fields changed")
        for key, value in expected.items():
            compare_snapshot(value, actual[key], f"{name}.{key}")
    elif isinstance(expected, list):
        if not isinstance(actual, list) or len(expected) != len(actual):
            raise AssertionError(f"{name}: result length changed")
        for index, value in enumerate(expected):
            compare_snapshot(value, actual[index], f"{name}[{index}]")
    elif isinstance(expected, (int, float)) and not isinstance(expected, bool):
        if not isinstance(actual, (int, float)) or not math.isclose(
                float(expected), float(actual), rel_tol=1e-9, abs_tol=1e-8):
            raise AssertionError(f"{name}: committed number changed")
    elif expected != actual:
        raise AssertionError(f"{name}: committed value changed")


def check(result: dict) -> None:
    compare_snapshot(json.loads(SNAPSHOT.read_text()), result)
    fixed = result["fixed_10kg_fuel"]
    resized = result["hypothetical_resized_one_event_fuel"]
    if abs(fixed["spring"]["propellant_used_kg"] - 2.6926385533602684) > 1e-9:
        raise AssertionError("spring case no longer matches the published reference")
    if abs(fixed["gen5_ideal_finite_force"]["propellant_used_kg"]
           - 0.8266008413645523) > 1e-9:
        raise AssertionError("Gen5 case no longer matches the published reference")
    if abs(resized["spring_loaded_fuel_kg"] - 4.659252629533221) > 1e-6:
        raise AssertionError("spring fuel sizing changed")
    if abs(resized["gen5_loaded_fuel_kg"] - 2.8146858679616855) > 1e-6:
        raise AssertionError("Gen5 fuel sizing changed")
    if abs(resized["gen5_device_mass_for_proxy_parity_kg"]
           - 73.93198489552128) > 1e-6:
        raise AssertionError("device parity threshold changed")
    if len(result["p122_ideal_geometry_cases"]) != 5:
        raise AssertionError("P122 case count changed")
    for row in result["p122_ideal_geometry_cases"]:
        if row["gen5_minus_spring_device_plus_fuel_kg"] <= 0:
            raise AssertionError("one-event mass proxy verdict changed")
    for option in ("spring", "gen5_ideal_finite_force"):
        if abs(fixed[option]["target_residual_m_s"]) > 1e-10:
            raise AssertionError("event target did not close")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    if args.check:
        check(result)
        print("one-event mass screen: committed result, reference identities and five P122 cases PASS")
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
