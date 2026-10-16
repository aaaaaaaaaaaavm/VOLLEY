"""Hash the evaluated computational evidence without implying academic approval."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/GEN5_TECHNICAL_BASELINE.json"
PATHS = [
    "analysis/mass_properties.py", "analysis/motor_model.py", "analysis/astro.py",
    "analysis/gen5_finite_force_map.py", "analysis/gen5_finite_force_fem2d.py",
    "analysis/gen5_finite_force_surface3d.py", "analysis/gen5_finite_force_sensitivity.py",
    "analysis/gen5_finite_coupled_shot.py", "analysis/gen5_voltage_limited_screen.py",
    "analysis/gen5_release_arrest_bounds.py", "analysis/rated_energy_mass_audit.py",
    "analysis/matched_mission_reference.py", "analysis/manifest_finite_burn.py",
    "analysis/finite_burn_departure.py", "analysis/field_3d.py",
    "analysis/orbit_core.py", "analysis/gen5_evidence_audit.py",
    "analysis/gen5_lifetime_crosscheck.py", "analysis/rated_orbit_independent.py",
    "analysis/results/mass_properties.json", "analysis/results/motor_results.json",
    "analysis/results/gen5_mass_ledger.json", "analysis/results/gen5_lifetime_crosscheck.json",
    "analysis/results/rated_orbit_independent.json", "analysis/results/rated_energy_mass_audit.json",
    "analysis/results/gen5_finite_force_map.json", "analysis/results/gen5_finite_force_fem2d.json",
    "analysis/results/gen5_finite_force_surface3d.json", "analysis/results/gen5_finite_force_sensitivity.json",
    "analysis/results/gen5_finite_coupled_shot.json", "analysis/results/matched_mission_reference.json",
    "cad/parameters.json", "cad/build_gen5.py", "cad/build_review_assembly.py",
    "cad/REVIEW_ASSEMBLY.json", "cad/FREECAD_EXPORT.json", "cad/native/Gen5_Review.FCStd",
    "cad/GEN5_FULL_INTERFERENCE_AUDIT_2026_10_12.json",
    "cad/GEN5_INTERFERENCE_DISPOSITION.json", "cad/GEN5_INTERFERENCE_DISPOSITION.md",
    "docs/GEN5_MASS_AND_INTERFACE_LEDGER.md", "docs/GEN5_UNCERTAINTY_AND_ACCEPTANCE.md",
    "docs/GEN5_ORBIT_AND_MISSION_DISPOSITION.md", "docs/GEN5_STRUCTURAL_DISPOSITION.md",
    "docs/SOLVER_EVIDENCE_BOUNDARY.md", "validation/P133_gen5_evidence_audit.md",
    "validation/P134_gen5_lifetime_crosscheck.md", "validation/A15_poem_campaign.md",
    "validation/gmat/orbit_state.py", "validation/gmat/build_poem_campaign.py",
    "validation/gmat/parse_poem_campaign.py", "validation/gmat/test_orbit_state.py",
    "validation/gmat/evidence/A15_R1_NATIVE_CAPTURE.json",
    "validation/results/A15_R1_gmat_r2026a_review.json",
    "validation/results/A15_R1_FINE_WINDOW_RESULT.json",
    "figures/gen5_reconciled_mass.png", "figures/gen5_lifetime_numerical_check.png",
    "tools/plot_gen5_record.py",
]


def build():
    paths = PATHS + [str(p.relative_to(ROOT)) for p in sorted((ROOT / "cad/step/gen5").glob("*.step"))]
    records = {}
    for rel in paths:
        p = ROOT / rel
        records[rel] = {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "bytes": p.stat().st_size}
    return {"configuration_id": "VOLLEY-GEN5-EVALUATED-2026-10-16-R1",
            "status": "FROZEN_TECHNICAL_EVIDENCE_RECORD; ACADEMIC_SUBMISSION_APPROVAL_PENDING",
            "scope": "Twelve 4 kg 3U conceptual Gen5 payloads; evaluated adverse configuration",
            "geometry_changed_from_12_October": False,
            "hardware_build_or_test": False, "component_rated_release_speed": None,
            "exceptions": ["17 Gen5 solid intersections; 11 mm side-fit failure",
                           "historical 16.029 m/s periodic-force output challenged; ideal finite screen not a rating",
                           "126.561588 kg historical mass model; installed BOM and full inertia unavailable",
                           "no sampled twelve-shot matched campaign completes; not a global infeasibility proof",
                           "lifetime numerical agreement uses shared static atmosphere; actual lifetime unvalidated",
                           "release/contact, structural/thermal, magnetic compatibility and provider interfaces unverified",
                           "native solver and hardware validation gaps are listed in SOLVER_EVIDENCE_BOUNDARY",
                           "guide ruling, approved formatting, independent review and submission are separate gates",
                           "Gen6 R0/R2 and future speed/feeder/product proposals are excluded from Gen5 achieved results"],
            "files": records}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = build()
    if args.check:
        if json.loads(OUTPUT.read_text()) != data:
            raise SystemExit("FAIL: frozen Gen5 technical evidence changed; issue a reviewed revision")
    else:
        OUTPUT.write_text(json.dumps(data, indent=2) + "\n")
    print(f"PASS: {len(data['files'])} frozen technical files; academic approval remains pending")


if __name__ == "__main__":
    main()
