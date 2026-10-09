"""Independent algebraic audit of the published Gen5 rated mass/energy values.

This script reads captured outputs but does not call the motor or mass model. It
checks identities that must hold at the reported operating point and records the
portion of gross electrical draw not itemized by the published energy terms.
Passing the identities does not verify electromagnetic force or hardware losses.
The formerly unitemized gross remainder can be reconstructed from the historical
model's 95% converter efficiency, 200 W auxiliary load and forward-Euler step.
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
CONVERTER_EFFICIENCY = 0.95  # historical model assumption, not a selected device
AUXILIARY_POWER_W = 200.0     # historical model assumption
INTEGRATION_STEP_S = 1e-4
UNROUNDED_SLED_MASS_KG = 9.445


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
    moving_mass = payload_mass + UNROUNDED_SLED_MASS_KG
    n_steps = round(duration / INTEGRATION_STEP_S)
    dv_step = shot["F_cmd"] / moving_mass * INTEGRATION_STEP_S
    # motor_model.shot() updates v before evaluating F*v at each forward-Euler
    # step. Its electrical integral therefore includes this positive O(dt) term.
    integration_excess = 0.5 * moving_mass * n_steps * dv_step**2
    mechanical_reported = shot["KE_payload"] + brake["KE_sled_in"]
    converter_loss = (mechanical_reported + integration_excess) * (1 / CONVERTER_EFFICIENCY - 1)
    auxiliary_draw = AUXILIARY_POWER_W * duration
    gross_residual_after_model_terms = (gross_unallocated - converter_loss
                                        - auxiliary_draw - integration_excess)
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
        "gross_energy_after_model_terms_difference_J": gross_residual_after_model_terms,
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
        "gross_energy_after_model_terms_difference_J": 0.1,
    }
    failed = [key for key, value in checks.items() if abs(value) > bands[key]]
    if failed:
        raise AssertionError(f"rated algebraic audit failed: {failed}")
    result = {
        "status": "PASS_HISTORICAL_MODEL_ENERGY_ARITHMETIC_PHYSICAL_SOURCE_OPEN",
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
            "converter_loss_at_model_assumption_J": converter_loss,
            "auxiliary_draw_at_model_assumption_J": auxiliary_draw,
            "forward_euler_mechanical_excess_J": integration_excess,
            "gross_residual_after_model_terms_J": gross_residual_after_model_terms,
            "historical_model_steps": n_steps,
        },
        "identity_residuals": checks,
        "predeclared_bands": bands,
        "unclosed": [
            "The old 124.488 J compact-output remainder is accounted for by the model's 95% converter assumption, 200 W auxiliaries and Euler integration excess; it is not an unexplained hardware loss.",
            "The converter efficiency, auxiliary load and source rating are assumptions, not selected or independently verified components.",
            "These identities do not independently solve magnetic thrust, winding loss, bank ESR or brake transients.",
            "No supplier-backed installed power source, thermal test or physical shot exists.",
        ],
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"historical model energy ledger closes to {gross_residual_after_model_terms:.4f} J; physical source remains open")


if __name__ == "__main__":
    main()
