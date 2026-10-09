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
    "cad/parameters.json", "cad/BUILD.json", "cad/DIMENSIONS.md",
    "analysis/motor_model.py", "analysis/mass_properties.py", "analysis/astro.py",
    "analysis/results/motor_results.json", "analysis/results/mass_properties.json",
    "analysis/results/astro_results.json", "analysis/results/manifest_finite_burn.json",
    "analysis/results/phasing_reference.json", "docs/BASELINE.md",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    step = sorted((ROOT / "cad/step/gen5").glob("*_Gen5.step"))
    if len(step) != 8:
        raise SystemExit(f"expected eight Gen5 STEP parts; found {len(step)}")
    paths = [ROOT / name for name in SOURCES] + step
    missing = [str(p.relative_to(ROOT)) for p in paths if not p.is_file()]
    if missing:
        raise SystemExit(f"missing configuration inputs: {missing}")
    mass = json.loads((ROOT / "analysis/results/mass_properties.json").read_text())
    motor = json.loads((ROOT / "analysis/results/motor_results.json").read_text())
    result = {
        "configuration_id": "VOLLEY-GEN5-ACADEMIC-2026-10-09",
        "status": "COMPUTATIONAL_DESIGN_REVIEW_CANDIDATE",
        "evidence_class": "model_only_no_gen5_hardware_test",
        "design_scope": "3U, twelve-slot conceptual magazine, 1.5 m track, electromagnetic Gen5",
        "headline_model_values": {
            "dry_mass_kg": mass["dry_kg"],
            "sled_mass_kg": mass["sled_kg"],
            "exit_speed_m_s": motor["shot"]["v_exit"],
            "net_energy_J": motor["E_drawn_net_J"],
        },
        "files": {str(p.relative_to(ROOT)): digest(p) for p in paths},
        "exclusions": [
            "No approved integrated STEP assembly or manufacturing drawing set",
            "No provider-specific interface, qualified payload, hardware test or flight evidence",
            "No complete installed-system mass, tolerance, shock or thermal closure",
        ],
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"{result['configuration_id']}: {len(paths)} hashed inputs; {len(step)} STEP parts")


if __name__ == "__main__":
    main()
