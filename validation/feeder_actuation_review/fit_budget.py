"""Declared datum/temperature sensitivities, separate from nominal interference."""

from pathlib import Path
import itertools, math, json

H = Path(__file__).parent
rows = []
for label, L in [("1U", 113.5), ("3U", 340.5)]:
    interfaces = [
        ("receiver_Y_to_payload", 0.5, L / 2, 100, 11e-6),
        ("receiver_X_to_payload", 1, 50, L, 11e-6),
        ("top_rail_to_payload", 2, 100, 100, 11e-6),
        ("fork_rear_to_payload", 3, 100, 100, 11e-6),
        ("gate_crossbolt_radial", 0.2, 35, 35, 11e-6),
        ("cassette_arch_to_fork", 2, 100, 100, 0),
    ]
    for (
        (name, gap, lever, thermal_length, dalpha),
        angle,
        temp,
        deflection,
    ) in itertools.product(interfaces, [0.05, 0.1, 0.5], [-40, 20, 80], [0, 0.2, 0.5]):
        manufacturing = 0.3
        alignment = lever * math.tan(math.radians(angle))
        thermal = abs(temp - 20) * thermal_length * dalpha
        residual = gap - manufacturing - alignment - thermal - deflection
        rows.append(
            dict(
                payload=label,
                interface=name,
                nominal_gap_mm=gap,
                manufacturing_stack_assumed_mm=manufacturing,
                datum_rotation_assumed_deg=angle,
                rotation_lever_mm=lever,
                alignment_loss_mm=alignment,
                temperature_C=temp,
                thermal_length_mm=thermal_length,
                CTE_mismatch_assumed_per_K=dalpha,
                thermal_loss_mm=thermal,
                unpredicted_deflection_band_mm=deflection,
                residual_mm=residual,
                positive=residual > 0,
            )
        )
out = dict(
    revision="FM-02",
    datum_definition={
        "A": "sled lower mounting plane",
        "B": "launch-guide centreline; orientation about A",
        "C": "rear payload-stop Xdatum",
    },
    cases=rows,
    nonpositive=sum(not x["positive"] for x in rows),
    boundary="Proposed datum sensitivity, not an issued GD&T drawing or actual predicted assembly deformation. Uniform0.3mm error stack is an assumed study band; it is not the actual pin/hole fit specification. In particular the0.2mm pin radial gap cannot absorb this band. Matched bore alignment/reaming and verified manufacturing process are required; no global fit pass.",
)
(H / "FIT_BUDGET.json").write_text(json.dumps(out, indent=2) + "\n")
print(len(rows), "fit sensitivities;", out["nonpositive"], "nonpositive")
