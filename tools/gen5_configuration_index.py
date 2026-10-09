"""Generate a reviewable Gen5 configuration inventory from committed design inputs.

This is a file provenance record, not a manufacturing release or a validity certificate.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/GEN5_CONFIGURATION_INDEX.json"

SOURCES = [
    "cad/parameters.json", "cad/BUILD.json", "cad/DIMENSIONS.md", "cad/BOM.md",
    "cad/build_review_assembly.py", "cad/REVIEW_ASSEMBLY.json",
    "cad/freecad_export_review.py", "cad/FREECAD_EXPORT.json",
    "cad/native/Gen5_Review.FCStd", "cad/GEN5_CAD_REVIEW.pdf",
    "analysis/motor_model.py", "analysis/mass_properties.py", "analysis/astro.py",
    "analysis/rated_orbit_independent.py", "analysis/results/rated_orbit_independent.json",
    "analysis/rated_energy_mass_audit.py", "analysis/results/rated_energy_mass_audit.json",
    "analysis/results/motor_results.json", "analysis/results/mass_properties.json",
    "analysis/results/astro_results.json", "analysis/results/manifest_finite_burn.json",
    "analysis/results/phasing_reference.json", "docs/BASELINE.md",
    "validation/P115_rated_orbit_cartesian.md", "validation/P116_gen5_assembly_packaging.md",
    "validation/P117_rated_energy_mass_audit.md", "reports/GEN5_COMPUTATIONAL_REVIEW.pdf",
    "analysis/gen5_finite_force_map.py", "analysis/results/gen5_finite_force_map.json",
    "validation/P118_gen5_finite_force_map.md",
    "analysis/gen5_finite_force_fem2d.py", "analysis/results/gen5_finite_force_fem2d.json",
    "validation/P119_gen5_finite_force_fem2d.md",
    "analysis/gen5_finite_coupled_shot.py", "analysis/results/gen5_finite_coupled_shot.json",
    "validation/P120_gen5_finite_coupled_shot.md",
    "analysis/matched_mission_reference.py", "analysis/results/matched_mission_reference.json",
    "docs/MATCHED_MISSION_REFERENCE.md",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    step = sorted(p for p in (ROOT / "cad/step/gen5").glob("*_Gen5.step")
                  if "Review_Assembly" not in p.name)
    if len(step) != 8:
        raise SystemExit(f"expected eight Gen5 STEP parts; found {len(step)}")
    review_assembly = ROOT / "cad/step/gen5/VOLLEY_Review_Assembly_Gen5.step"
    freecad_parts = sorted((ROOT / "cad/step/freecad_gen5").glob("*_FreeCAD_Gen5.step"))
    if len(freecad_parts) != 8:
        raise SystemExit(f"expected eight FreeCAD-exported STEP parts; found {len(freecad_parts)}")
    freecad_assembly = ROOT / "cad/step/gen5/VOLLEY_Review_Assembly_FreeCAD_Gen5.step"
    paths = [ROOT / name for name in SOURCES] + step + freecad_parts + [review_assembly, freecad_assembly]
    missing = [str(p.relative_to(ROOT)) for p in paths if not p.is_file()]
    if missing:
        raise SystemExit(f"missing configuration inputs: {missing}")
    mass = json.loads((ROOT / "analysis/results/mass_properties.json").read_text())
    motor = json.loads((ROOT / "analysis/results/motor_results.json").read_text())
    finite = json.loads((ROOT / "analysis/results/gen5_finite_force_map.json").read_text())
    fem = json.loads((ROOT / "analysis/results/gen5_finite_force_fem2d.json").read_text())
    bank = json.loads((ROOT / "analysis/results/gen5_finite_coupled_shot.json").read_text())
    result = {
        "configuration_id": "VOLLEY-GEN5-ACADEMIC-2026-10-09",
        "status": "COMPUTATIONAL_DESIGN_REVIEW_CANDIDATE",
        "evidence_class": "model_only_no_gen5_hardware_test",
        "design_scope": "3U, twelve-slot conceptual magazine, 1.5 m release station on 1.8 m structural longerons, electromagnetic Gen5",
        "headline_model_values": {
            "dry_mass_kg": mass["dry_kg"],
            "sled_mass_kg": mass["sled_kg"],
            "exit_speed_m_s": motor["shot"]["v_exit"],
            "net_energy_J": motor["E_drawn_net_J"],
        },
        "headline_status": "Historical periodic-force speed is challenged by the finite-array/stator screen; no accepted performance rating",
        "finite_geometry_finding": {
            "ideal_work_J": finite["ideal_finite_stator_work_J"],
            "ideal_phase_geometry_only_speed_m_s": finite["ideal_finite_stator_exit_upper_m_s"],
            "independent_3d_force_fem": False,
        },
        "independent_2d_fem_screen": {
            "ideal_work_J": fem["runs"][-1]["work_J"],
            "mesh_size_m": fem["runs"][-1]["dx_m"],
            "omits_magnet_depth_end_effects": True,
        },
        "conditional_finite_force_bank_screen": {
            "full_winding_gross_draw_J": bank["branches"][0]["result"]["gross_capacitor_draw_J"],
            "selected_winding_and_inverter": False,
        },
        "files": {str(p.relative_to(ROOT)): digest(p) for p in paths},
        "exclusions": [
            "The reference STEP assembly fails a side-fed packaging screen; no approved assembly or manufacturing drawing set",
            "No provider-specific interface, qualified payload, hardware test or flight evidence",
            "No complete installed-system mass, tolerance, shock or thermal closure",
        ],
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"{result['configuration_id']}: {len(paths)} hashed inputs; {len(step)} source plus {len(freecad_parts)} FreeCAD STEP parts")


if __name__ == "__main__":
    main()
