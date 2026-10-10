#!/usr/bin/env python3
"""Necessary one-event mass bounds for a Gen5 successor concept.

These bounds are algebraic consequences of the P123 reference. They do not
predict the mass, speed, safety, or mission performance of a new architecture.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P123 = ROOT / "analysis/results/gen5_one_event_mass_screen.json"
LEDGER = ROOT / "analysis/results/mass_properties.json"
SNAPSHOT = ROOT / "analysis/results/gen5_architecture_bounds.json"

ENCLOSURE_PREFIXES = (
    "Enclosure skins",
    "Enclosure frames",
    "Radiator (",
    "Equipment-bay boxes",
    "Fasteners and brackets (A46",
)
STUDY_ECONOMIC_SCREEN_KG_PER_3U = 2.0


def build() -> dict:
    p123 = json.loads(P123.read_text())
    ledger = json.loads(LEDGER.read_text())
    inputs = p123["inputs"]
    resized = p123["hypothetical_resized_one_event_fuel"]
    count = inputs["payload_count"]
    reserve = inputs["reserve_kg"]
    spring_device = inputs["spring_device_kg"]
    spring_fuel = resized["spring_loaded_fuel_kg"]
    gen5_device = inputs["gen5_modeled_device_kg"]
    ideal_speed_parity_device = resized["gen5_device_mass_for_proxy_parity_kg"]

    # A nonnegative host burn cannot reduce loaded fuel below its reserve.
    # Hence this maximum device mass is an optimistic NECESSARY condition
    # for one-event device-plus-fuel parity, regardless of launch speed.
    spring_device_plus_fuel = spring_device + spring_fuel
    absolute_parity_device = spring_device_plus_fuel - reserve

    enclosure_rows = [
        {"item": name, "modeled_kg": mass}
        for name, mass, _ in ledger["parts"]
        if any(name.startswith(prefix) for prefix in ENCLOSURE_PREFIXES)
    ]
    if len(enclosure_rows) != len(ENCLOSURE_PREFIXES):
        raise ValueError("enclosure ledger group changed; review the bound")
    enclosure_mass = sum(row["modeled_kg"] for row in enclosure_rows)

    return {
        "evidence_class": "necessary bound on the P123 one-event reference, not an achievable redesign or campaign result",
        "source_results": [
            "analysis/results/gen5_one_event_mass_screen.json",
            "analysis/results/mass_properties.json",
        ],
        "spring_device_plus_one_event_fuel_kg": spring_device_plus_fuel,
        "common_fuel_reserve_kg": reserve,
        "maximum_gen5_device_for_one_event_parity_even_with_zero_burn_kg":
            absolute_parity_device,
        "gen5_current_modeled_device_kg": gen5_device,
        "minimum_current_one_event_mass_proxy_deficit_kg":
            gen5_device - absolute_parity_device,
        "parity_device_at_p118_ideal_speed_kg": ideal_speed_parity_device,
        "additional_device_mass_allowance_from_perfect_speed_kg":
            absolute_parity_device - ideal_speed_parity_device,
        "enclosure_related_rows": enclosure_rows,
        "enclosure_related_modeled_kg": enclosure_mass,
        "remaining_deficit_after_impossible_zero_enclosure_kg":
            gen5_device - enclosure_mass - absolute_parity_device,
        "study_economic_screen_kg_per_3u": STUDY_ECONOMIC_SCREEN_KG_PER_3U,
        "study_economic_screen_total_kg_for_manifest":
            STUDY_ECONOMIC_SCREEN_KG_PER_3U * count,
        "absolute_parity_device_kg_per_3u": absolute_parity_device / count,
    }


def compare(expected: object, actual: object, name: str = "root") -> None:
    if isinstance(expected, dict):
        if not isinstance(actual, dict) or set(expected) != set(actual):
            raise AssertionError(f"{name}: fields changed")
        for key, value in expected.items():
            compare(value, actual[key], f"{name}.{key}")
    elif isinstance(expected, list):
        if not isinstance(actual, list) or len(expected) != len(actual):
            raise AssertionError(f"{name}: length changed")
        for index, value in enumerate(expected):
            compare(value, actual[index], f"{name}[{index}]")
    elif isinstance(expected, (int, float)) and not isinstance(expected, bool):
        if not isinstance(actual, (int, float)) or not math.isclose(
            float(expected), float(actual), rel_tol=1e-10, abs_tol=1e-8
        ):
            raise AssertionError(f"{name}: numeric result changed")
    elif expected != actual:
        raise AssertionError(f"{name}: value changed")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    if args.check:
        compare(json.loads(SNAPSHOT.read_text()), result)
        assert result["minimum_current_one_event_mass_proxy_deficit_kg"] > 0
        assert result["remaining_deficit_after_impossible_zero_enclosure_kg"] > 0
        print("Gen5 necessary one-event architecture bounds: committed result PASS")
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
