"""Independent algebraic audit of the published Gen5 rated mass/energy values.

This script reads captured outputs but does not call the motor or mass model. It
checks identities that must hold at the reported operating point and records the
portion of gross electrical draw not itemized by the published energy terms.
Passing the identities does not verify electromagnetic force or hardware losses.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOTOR = ROOT / "analysis/results/motor_results.json"
MASS = ROOT / "analysis/results/mass_properties.json"
OUTPUT = ROOT / "analysis/results/rated_energy_mass_audit.json"
G0 = 9.80665
PAYLOAD_COUNT = 12
POWERED_STROKE_M = 1.3


def main() -> None:
    motor_raw, mass_raw = MOTOR.read_bytes(), MASS.read_bytes()
    motor, mass = json.loads(motor_raw), json.loads(mass_raw)
    shot, brake = motor["shot"], motor["regen"]
    speed = shot["v_exit"]
    duration = shot["t_ms"] / 1000
    payload_mass = (mass["loaded_kg"] - mass["dry_kg"]) / PAYLOAD_COUNT
    parts_sum = sum(float(part[1]) for part in mass["parts"])
    payload_ke = 0.5 * payload_mass * speed**2
    sled_ke = 0.5 * mass["sled_kg"] * speed**2
    constant_accel_stroke = speed * duration / 2
    gross_unallocated = (shot["E_drawn"] - shot["KE_payload"]
                         - brake["KE_sled_in"] - shot["Q_copper"] - shot["Q_esr"])
    brake_work = brake["F_brake"] * brake["s_m"]
    brake_recovery_balance = (brake["W_mech"] - brake["Q_aux"]
                              - brake["Q_converter"] - brake["Q_copper"]
                              - brake["Q_esr"] - brake["E_recovered"])
    checks = {
        "dry_rollup_difference_kg": parts_sum - mass["dry_kg"],
        "payload_ke_difference_J": payload_ke - shot["KE_payload"],
        "sled_ke_difference_J": sled_ke - brake["KE_sled_in"],
        "constant_accel_stroke_difference_m": constant_accel_stroke - POWERED_STROKE_M,
        "brake_work_difference_J": brake_work - brake["W_mech"],
        "brake_energy_split_difference_J": brake["KE_sled_in"] - brake["W_mech"] - brake["KE_to_brake"],
        "recovery_loss_balance_difference_J": brake_recovery_balance,
        "net_draw_difference_J": shot["E_drawn"] - brake["E_recovered"] - motor["E_drawn_net_J"],
    }
    bands = {
        "dry_rollup_difference_kg": 0.1,
        "payload_ke_difference_J": 0.1,
        "sled_ke_difference_J": 1.0,  # reported sled mass is rounded to 0.01 kg
        "constant_accel_stroke_difference_m": 0.003,
        "brake_work_difference_J": 0.1,
        "brake_energy_split_difference_J": 0.1,
        "recovery_loss_balance_difference_J": 0.1,
        "net_draw_difference_J": 0.1,
    }
    failed = [key for key, value in checks.items() if abs(value) > bands[key]]
    if failed:
        raise AssertionError(f"rated algebraic audit failed: {failed}")
    result = {
        "status": "PASS_ALGEBRA_ONLY_GROSS_LOSS_BUDGET_OPEN",
        "motor_sha256": hashlib.sha256(motor_raw).hexdigest(),
        "mass_sha256": hashlib.sha256(mass_raw).hexdigest(),
        "derived": {
            "dry_parts_sum_kg": parts_sum,
            "payload_mass_each_kg": payload_mass,
            "payload_ke_recalculated_J": payload_ke,
            "sled_ke_from_rounded_mass_J": sled_ke,
            "constant_accel_equivalent_stroke_m": constant_accel_stroke,
            "constant_accel_equivalent_g": speed / duration / G0,
            "brake_force_distance_work_J": brake_work,
            "gross_draw_unallocated_J": gross_unallocated,
            "gross_draw_unallocated_fraction": gross_unallocated / shot["E_drawn"],
        },
        "identity_residuals": checks,
        "predeclared_bands": bands,
        "unclosed": [
            "The 124.488 J gross-draw remainder is not itemized in the cited model output.",
            "These identities do not independently solve magnetic thrust, winding loss, bank ESR or brake transients.",
            "No supplier-backed installed power source, thermal test or physical shot exists.",
        ],
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"rated algebraic identities pass; {gross_unallocated:.3f} J gross draw unallocated")


if __name__ == "__main__":
    main()
