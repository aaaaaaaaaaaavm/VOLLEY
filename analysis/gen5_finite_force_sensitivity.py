"""P122 deterministic geometry/material sensitivity of the P121 ideal force screen.

These are adopted scenarios, not measured tolerances or probability bounds.
The calculation retains ideal phase and omits the electrical and release chain.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import motor_model as mm
from gen5_finite_force_surface3d import belt_geometry, charged_lines, force_at

ROOT = Path(__file__).resolve().parents[1]
P121 = ROOT / "analysis/results/gen5_finite_force_surface3d.json"
PARAM = ROOT / "cad/parameters.json"
OUT = ROOT / "analysis/results/gen5_finite_force_sensitivity.json"
REPORT = ROOT / "validation/P122_gen5_finite_force_sensitivity.md"
FIG = ROOT / "figures/gen5_finite_force_sensitivity.png"


def run_case(name: str, gap_m: float, depth_offset_m: float, positions: np.ndarray, belts: np.ndarray) -> dict:
    faces = charged_lines(16, gap_m=gap_m)
    forces = np.array([force_at(float(s), faces, belts, depth_offset_m=depth_offset_m)
                       for s in positions])
    work = float(np.trapezoid(forces, positions))
    return dict(name=name, gap_m=gap_m, depth_offset_m=depth_offset_m,
                nominal_radial_clearance_each_side_m=(gap_m-mm.WIND_THICK)/2,
                ideal_work_J=work,
                ideal_speed_conversion_m_s=math.sqrt(2*work/(mm.M_SAT+mm.M_SLED)),
                forces_N=forces.tolist())


def calculate() -> dict:
    reference = json.loads(P121.read_text())
    positions = np.linspace(0, mm.ACCEL_ZONE, 53)
    belts = belt_geometry()
    cases = [run_case(name, gap, offset, positions, belts)
             for name, gap, offset in (
                 ("nominal_12mm_gap", .012, 0.0),
                 ("gap_14mm", .014, 0.0),
                 ("gap_16mm", .016, 0.0),
                 ("depth_offset_5mm", .012, .005),
                 ("depth_offset_10mm", .012, .010))]
    baseline = cases[0]["ideal_work_J"]
    if abs(baseline-reference["runs"][1]["ideal_work_J"]) > 1e-6:
        raise ValueError("nominal P122 force does not reproduce the P121 16-node case")
    for case in cases:
        case["work_ratio_to_nominal"] = case["ideal_work_J"] / baseline
    br_cases = [dict(remanence_multiplier=factor,
                     ideal_work_J=baseline*factor,
                     ideal_speed_conversion_m_s=math.sqrt(2*baseline*factor/(mm.M_SAT+mm.M_SLED)))
                for factor in (0.90, 1.0, 1.10)]
    mass_cases = [dict(moving_mass_multiplier=factor,
                       ideal_speed_conversion_m_s=math.sqrt(2*baseline/((mm.M_SAT+mm.M_SLED)*factor)))
                  for factor in (0.90, 1.0, 1.10)]
    return dict(status="DETERMINISTIC_SCENARIO_SWEEP_NOT_TOLERANCE_OR_PERFORMANCE_RATING",
                method="P121 3-D surface-charge field and finite-belt force; 16-node face quadrature; 25 mm stations; ideal phase",
                software_versions=dict(python=platform.python_version(), numpy=np.__version__),
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                p121_source_sha256=hashlib.sha256((ROOT/"analysis/gen5_finite_force_surface3d.py").read_bytes()).hexdigest(),
                p121_result_sha256=hashlib.sha256(P121.read_bytes()).hexdigest(),
                parameters_sha256=hashlib.sha256(PARAM.read_bytes()).hexdigest(),
                positions_m=positions.tolist(), cases=cases,
                remanence_cases=br_cases, moving_mass_cases=mass_cases,
                caveats=["Scenario ranges are illustrative and are not supplier or manufacturing tolerances",
                         "Gap changes hold conductor position/thickness fixed; real structure and insulation unmodeled",
                         "Depth offset shifts the stator active copper relative to the magnets, not the whole host",
                         "Remanence scaling assumes the linear ironless model",
                         "No winding voltage/current dynamics, contact, brake, host or measured release"])


def report(d: dict) -> str:
    c = d["cases"]
    return "\n".join([
        "# P122 — Gen5 finite-force scenario sensitivity", "",
        "**Evidence class: deterministic ideal-field scenarios, not measured tolerances, probabilities or a motor rating.**", "",
        "P121's independently implemented depth-resolved 3-D surface-charge method is",
        "rerun at five geometry cases. The nominal 12 mm magnet-face gap leaves only 1 mm",
        "radial clearance on each side of the modeled 10 mm winding. Widening that gap or",
        "offsetting the copper along the 90 mm depth changes the ideal integrated work.",
        "The 16-node face quadrature and 25 mm station grid are taken from P121's checked",
        "numerical convergence. These are **illustrative perturbations**, not as-built bounds.", "",
        "| Scenario | Gap | Depth offset | Nominal radial clearance/side | Ideal work | Speed conversion |",
        "|:--|--:|--:|--:|--:|--:|",
        *[f"| {x['name'].replace('_',' ')} | {1000*x['gap_m']:.0f} mm | {1000*x['depth_offset_m']:.0f} mm | "
          f"{1000*x['nominal_radial_clearance_each_side_m']:.0f} mm | {x['ideal_work_J']:.1f} J | "
          f"{x['ideal_speed_conversion_m_s']:.3f} m/s |" for x in c], "",
        f"A 14 mm gap changes work by {100*(c[1]['work_ratio_to_nominal']-1):+.1f}% and a 16 mm gap",
        f"by {100*(c[2]['work_ratio_to_nominal']-1):+.1f}% relative to the nominal geometry.",
        f"A 5 mm depth offset changes work by {100*(c[3]['work_ratio_to_nominal']-1):+.1f}%",
        f"and a 10 mm offset by {100*(c[4]['work_ratio_to_nominal']-1):+.1f}%.", "",
        "Because the ironless model is linear, ±10% *assumed* remanence changes ideal work",
        f"to {d['remanence_cases'][0]['ideal_work_J']:.1f}–{d['remanence_cases'][2]['ideal_work_J']:.1f} J.",
        "An illustrative ±10% moving-mass range changes only the work-to-speed conversion,",
        f"giving {d['moving_mass_cases'][2]['ideal_speed_conversion_m_s']:.3f}–"
        f"{d['moving_mass_cases'][0]['ideal_speed_conversion_m_s']:.3f} m/s at nominal work.",
        "These ranges are not a statistical confidence interval; no supplier or tolerance",
        "distribution has been selected.", "",
        "![Ideal finite-force sensitivity scenarios](../figures/gen5_finite_force_sensitivity.png)", "",
        "The 16.029 m/s historical periodic result remains challenged. This sweep does not",
        "supply an achievable revised speed because current rise, commutation, thermal change,",
        "magnet tolerances, friction and release contact remain unsolved. A provider/payload",
        "interface and physical measurements are still required for product readiness.", "",
        "Reproduce with `python analysis/gen5_finite_force_sensitivity.py`; `--check`",
        "compares a fresh run to this JSON and prose. P121 and geometry hashes are recorded",
        "in the result.", "",
    ])


def plot(d: dict) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.0), dpi=150)
    cases = d["cases"]
    names = ["Nominal", "+2 mm gap", "+4 mm gap", "+5 mm depth", "+10 mm depth"]
    speeds = [case["ideal_speed_conversion_m_s"] for case in cases]
    colors = ["#006d77", "#57989b", "#9dc9ca", "#a35b32", "#d39154"]
    axes[0].barh(names[::-1], speeds[::-1], color=colors[::-1])
    axes[0].set(xlabel="Ideal work-to-speed conversion (m/s)",
                title="Illustrative geometry scenarios")
    axes[0].set_xlim(0, max(speeds)*1.13)
    for i, value in enumerate(speeds[::-1]):
        axes[0].text(value+.12, i, f"{value:.2f}", va="center", fontsize=8)
    for case, name, color in zip(cases[:3], names[:3], colors[:3]):
        axes[1].plot(d["positions_m"], case["forces_N"], label=name, color=color, lw=1.9)
    axes[1].set(xlabel="Sled displacement (m)", ylabel="Ideal forward force (N)",
                title="Magnet-face gap effect")
    axes[1].grid(alpha=.2)
    axes[1].legend(fontsize=8)
    fig.suptitle("Gen5 3-D finite-force sensitivity — scenarios, not tolerances", fontsize=12)
    fig.tight_layout()
    fig.savefig(FIG, metadata={"Software": "VOLLEY P122 ideal-field scenario model"})
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = calculate()
    rendered = json.dumps(result, indent=2) + "\n"
    prose = report(result)
    if args.check:
        fresh = OUT.exists() and OUT.read_text() == rendered and REPORT.exists() and REPORT.read_text() == prose
        print("P122 current" if fresh else "P122 STALE")
        return 0 if fresh else 1
    OUT.write_text(rendered)
    REPORT.write_text(prose)
    plot(result)
    print("P122 sensitivity scenarios captured")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
