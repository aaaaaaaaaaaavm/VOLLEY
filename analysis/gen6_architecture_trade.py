"""P92 clean-sheet architecture trade after P113-S4.

Criteria: validation/P92_architecture_trade.md, committed before this file.

This is deliberately not a weighted-score selector. It computes common release physics,
keeps payload arrangement separate from mechanism, carries only source-backed installed
facts, and returns UNDERDETERMINED when the repository does not yet contain enough evidence
to select hardware honestly.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import departure_trade

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "analysis" / "results" / "gen6_architecture_trade.json"
REPORT = ROOT / "docs" / "GEN6_ARCHITECTURE_TRADE.md"
FIGURE = ROOT / "figures" / "gen6_architecture_trade.svg"
CRITERIA = ROOT / "validation" / "P92_architecture_trade.md"
G0 = 9.80665
PAYLOAD_KG = 4.0
MANIFEST = 12


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path):
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def s4_common_speed(data):
    wanted = {"bolley_reference", "gen5_reference", "gen6_reference"}
    chosen = {}
    for sel in data["selections"]:
        if (sel["screen"] in wanted and sel["grid"] == "fine" and
                sel["policy"] == "enumerated" and sel["order"] == "either" and
                sel["status"] == "BEST_TESTED"):
            row = data["cases"][sel["case_index"]]
            candidate = row["candidates"][sel["candidate_index"]]
            chosen[sel["screen"]] = candidate["first_speed_m_s"]
    if set(chosen) != wanted:
        raise ValueError(f"missing S4 fine-grid selections: {chosen}")
    values = list(chosen.values())
    if max(values) - min(values) > 1e-9:
        raise ValueError(f"S4 screens do not share one first-release speed: {chosen}")
    return values[0], chosen


def duty(speed):
    return {
        "speed_m_s": speed,
        "payload_mass_kg": PAYLOAD_KG,
        "payload_kinetic_energy_J": 0.5 * PAYLOAD_KG * speed * speed,
        "payload_impulse_N_s": PAYLOAD_KG * speed,
        "ideal_stroke_at_10g_m": speed * speed / (2 * 10 * G0),
        "ideal_stroke_at_25g_m": speed * speed / (2 * 25 * G0),
        "mean_force_at_10g_N": PAYLOAD_KG * 10 * G0,
        "mean_force_at_25g_N": PAYLOAD_KG * 25 * G0,
    }


def arrangement_cases():
    banks = []
    for size in (2, 3, 4, 6):
        if MANIFEST % size == 0:
            banks.append({
                "bank_size": size,
                "bank_count": MANIFEST // size,
                "blocked_path_potentially_deliverable": MANIFEST - size,
                "blocked_path_stranded": size,
            })
    return {
        "independent_bays": {
            "paths": MANIFEST,
            "blocked_path_potentially_deliverable": MANIFEST - 1,
            "blocked_path_stranded": 1,
            "shared_command_power_loss_potentially_deliverable": 0,
            "safe_retention_after_fault": "UNKNOWN_UNTIL_RETENTION_DESIGN",
            "installed_mass_kg": None,
        },
        "independent_banks": {
            "sensitivity": banks,
            "shared_command_power_loss_potentially_deliverable": 0,
            "safe_retention_after_fault": "UNKNOWN_UNTIL_RETENTION_DESIGN",
            "installed_mass_kg": None,
        },
        "shared_magazine": {
            "paths": 1,
            "blocked_path_potentially_deliverable": 0,
            "blocked_path_stranded": MANIFEST,
            "shared_command_power_loss_potentially_deliverable": 0,
            "safe_retention_after_fault": "UNKNOWN_UNTIL_RETENTION_DESIGN",
            "installed_mass_kg": None,
        },
    }


def mechanism_cases(mass):
    return {
        "conventional_selected_spring": {
            "role": "competent baseline",
            "arrangements_allowed": ["independent_bays", "independent_banks", "shared_magazine"],
            "control_authority": "release timing plus selected/discrete spring condition; not assumed continuously variable",
            "installed_mass_kg": None,
            "payload_modification": False,
            "hard_blocker": None,
            "evidence": ["analysis/actuator_trade.py", "analysis/departure_trade.py"],
            "next_evidence": "source-backed current dispenser/spring mass and repeatability for the selected duty",
        },
        "programmable_stored_energy_pusher": {
            "role": "clean-sheet candidate",
            "arrangements_allowed": ["independent_bays", "independent_banks", "shared_magazine"],
            "control_authority": "conceptually adjustable; demonstrated range UNKNOWN",
            "installed_mass_kg": None,
            "payload_modification": False,
            "hard_blocker": None,
            "evidence": ["analysis/architecture_synthesis.py"],
            "next_evidence": "retention + adjustable store + pusher/arrest sizing at the S4 low-speed duty, with mass and reset burden",
        },
        "short_stroke_electromechanical_pusher": {
            "role": "clean-sheet candidate",
            "arrangements_allowed": ["independent_bays", "independent_banks", "shared_magazine"],
            "control_authority": "potentially continuous; no selected actuator or demonstrated envelope",
            "installed_mass_kg": None,
            "payload_modification": False,
            "hard_blocker": None,
            "evidence": ["analysis/actuator_trade.py"],
            "next_evidence": "force/stroke/current/thermal sizing for a compact direct pusher rather than the frozen Gen5 track",
        },
        "existing_gen6_gas_guide": {
            "role": "existing comparator",
            "arrangements_allowed": ["shared_magazine"],
            "control_authority": "29.009 m/s is a design-point result, not a validated control envelope",
            "installed_mass_kg": None,
            "payload_modification": False,
            "hard_blocker": "contact/release credibility and complete installed pressure-system burden unresolved",
            "evidence": ["docs/generations/GEN6.md", "validation/A67_guided_contact.md", "validation/A72_trim_array_drag.md", "validation/A74_tube_conductance_requirement.md"],
            "next_evidence": "correct P103/P108 contact model and close vessel/valve/support/consumable mass for the exact gas configuration",
        },
        "gen5_electromagnetic": {
            "role": "frozen comparator",
            "arrangements_allowed": ["shared_magazine"],
            "control_authority": "frozen model point 16.029 m/s; modelled dispersion is not measured precision",
            "installed_mass_kg": mass["dry_kg"],
            "loaded_mass_kg": mass["loaded_kg"],
            "payload_modification": False,
            "hard_blocker": "3U dispenser mass comparison fails",
            "evidence": ["analysis/results/mass_properties.json", "analysis/results/motor_results.json", "docs/BASELINE.md"],
            "next_evidence": "none for selection as new Gen6; retained as frozen comparator",
        },
        "bolley_cooperative_interface": {
            "role": "cooperative-payload comparator",
            "arrangements_allowed": ["independent_bays", "independent_banks", "shared_magazine"],
            "control_authority": "mission screen only; selected A9f/A5h drive still needs full installed closure",
            "installed_mass_kg": None,
            "payload_modification": True,
            "hard_blocker": "selected winding hot switching/protection, tolerances and complete installed mass remain open",
            "evidence": ["docs/BOLLEY_TRANSFER.md", "https://github.com/aaaaaaaaaaaavm/BOLLEY/blob/main/docs/CURRENT_REVIEW.md"],
            "next_evidence": "fresh A9f/A5h field/circuit/hot-loss/protection run plus packaged mass and payload-interface burden",
        },
    }


def build():
    s4 = load(ROOT / "analysis" / "results" / "manifest_timing.json")
    mass = load(ROOT / "analysis" / "results" / "mass_properties.json")
    s4_speed, s4_screens = s4_common_speed(s4)
    screens = departure_trade.INPUTS["maximum_speed_screens_m_s"]
    speeds = [
        ("s4_best_tested_first_release", s4_speed),
        ("bolley_reference", float(screens["bolley_reference"])),
        ("gen5_reference", float(screens["gen5_reference"])),
        ("gen6_reference", float(screens["gen6_reference"])),
    ]
    duties = {name: duty(v) for name, v in speeds}
    arrangements = arrangement_cases()
    mechanisms = mechanism_cases(mass)
    combinations = []
    for aname, arrangement in arrangements.items():
        for mname, mechanism in mechanisms.items():
            allowed = aname in mechanism["arrangements_allowed"]
            combinations.append({
                "arrangement": aname,
                "mechanism": mname,
                "configuration_valid": allowed,
                "installed_mass_kg": mechanism.get("installed_mass_kg") if allowed else None,
                "hard_blocker": mechanism.get("hard_blocker") if allowed else "NOT_THE_EXISTING_CONFIGURATION",
                "selection_state": ("REJECT_EXISTING_CONFIGURATION_MISMATCH" if not allowed else
                                    "REJECT_KNOWN_BLOCKER" if mechanism.get("hard_blocker") else
                                    "UNDERDETERMINED_INSTALLED_BURDEN"),
            })
    decisive = [
        "Size one adjustable stored-energy release cell at 4.569852 m/s and at the next mission-earned authority point; include retention, pusher, arrest/reset and installed mass.",
        "Size one compact electromechanical release cell to the same force/stroke duty; include current, power electronics, thermal recovery and moving-part arrest.",
        "Give independent bay, 2/3/4/6-payload bank and shared-magazine arrangements actual support/retention mass and envelope instead of topology alone.",
        "For the existing gas guide, correct P103/P108 contact/release physics and close the installed vessel/valve/support/consumable mass before it can compete on burden.",
        "For BOLLEY, close the selected A9f/A5h electrical path and complete packaged interface mass before treating its 11.8 m/s mission screen as installed capability.",
    ]
    paths = [
        "analysis/gen6_architecture_trade.py",
        "analysis/departure_trade.py",
        "analysis/results/manifest_timing.json",
        "analysis/results/mass_properties.json",
        "validation/P92_architecture_trade.md",
    ]
    return {
        "study": "P92-clean-sheet-architecture-trade",
        "status": "UNDERDETERMINED_FROM_CURRENT_EVIDENCE",
        "p92_disposition": "OPEN",
        "payload_mass_kg": PAYLOAD_KG,
        "manifest_payloads": MANIFEST,
        "s4_common_first_release_m_s": s4_speed,
        "s4_screen_values_m_s": s4_screens,
        "duty_screens": duties,
        "arrangements": arrangements,
        "mechanisms": mechanisms,
        "combined_architectures": combinations,
        "decisive_next_evidence": decisive,
        "interpretation": [
            "4.569852 m/s needs only about 41.8 J of payload kinetic energy and about 0.106 m ideal stroke at 10 g for the 4 kg reference payload.",
            "The repository therefore does not justify beginning the clean-sheet design with an 8 m guide or a 29 m/s requirement.",
            "No clean-sheet candidate has a source-backed complete installed burden, so P92 cannot be selected honestly yet.",
            "Fault topology favors smaller independent paths after a mechanical blockage, but shared command/power remains common-mode until explicitly separated.",
        ],
        "source_sha256": {p: digest(ROOT / p) for p in paths},
    }


def report(data):
    lines = [
        "# Gen6 clean-sheet architecture trade", "",
        "Generated by `analysis/gen6_architecture_trade.py`. Do not hand-edit.", "",
        "**P92 remains OPEN. Current evidence is sufficient to narrow the next work, not to select hardware.**", "",
        "[Frozen criteria](../validation/P92_architecture_trade.md) ·",
        "[Machine-readable result](../analysis/results/gen6_architecture_trade.json) ·",
        "[Programme](PROGRAMME_EXECUTION.md)", "",
        "![Architecture trade summary](../figures/gen6_architecture_trade.svg)", "",
        "## The first thing S4 changes", "",
        "For the 4 kg reference payload, the best tested S4 fine-grid campaign uses a",
        f"**{data['s4_common_first_release_m_s']:.6f} m/s** first release for the BOLLEY, Gen5 and existing Gen6 authority screens.",
        "That does not make this speed a product requirement. It does make a clean-sheet 29 m/s starting requirement indefensible.", "",
        "| Duty screen | Payload KE, J | Impulse, N·s | Ideal stroke at 10 g, m | Ideal stroke at 25 g, m |", "|---|---:|---:|---:|---:|",
    ]
    for name, d in data["duty_screens"].items():
        lines.append(f"| {name} ({d['speed_m_s']:.6f} m/s) | {d['payload_kinetic_energy_J']:.3f} | {d['payload_impulse_N_s']:.3f} | {d['ideal_stroke_at_10g_m']:.3f} | {d['ideal_stroke_at_25g_m']:.3f} |")
    lines += ["", "The 25 g column is a study sensitivity, not a universal CubeSat qualification limit.", "", "## Arrangement fault consequence, 12-payload reference", "", "| Arrangement | One blocked mechanical path | Shared command/power loss | Installed mass |", "|---|---|---|---|",
              "| Independent bays | 11 potentially deliverable, 1 stranded | 0 potentially deliverable unless services are separated | UNKNOWN |",
              "| Banks | 2/3/4/6-payload bank sensitivity: 10/9/8/6 potentially deliverable | 0 potentially deliverable unless services are separated | UNKNOWN |",
              "| Shared magazine/path | 0 potentially deliverable, 12 stranded | 0 potentially deliverable | UNKNOWN |", "",
              "This is consequence topology only. No reliability probability is invented.", "", "## Mechanism evidence", "", "| Candidate | Current role | Installed mass | Known blocker / reason it cannot be selected yet |", "|---|---|---:|---|" ]
    for name, m in data["mechanisms"].items():
        mass = "UNKNOWN" if m.get("installed_mass_kg") is None else f"{m['installed_mass_kg']:.1f} kg"
        blocker = m.get("hard_blocker") or m["next_evidence"]
        lines.append(f"| {name} | {m['role']} | {mass} | {blocker} |")
    lines += ["", "## Disposition", "", "There is no weighted score and no selected Gen6 mechanism.", "",
              "The clean-sheet candidates are underdetermined because their complete installed burdens do not yet exist in the record. The existing gas guide and Gen5 have known blockers; BOLLEY still carries cooperative-interface and electrical/package closure. Selecting a winner now would be presentation, not engineering.", "", "The smallest useful next work is therefore:", ""]
    for item in data["decisive_next_evidence"]:
        lines.append(f"- {item}")
    lines += ["", "A candidate earns P92 only after the required mission duty, installed burden and rejection reasons for alternatives are source-backed. A render does not close the decision.", ""]
    return "\n".join(lines)


def svg(data):
    duties = list(data["duty_screens"].items())
    max_e = max(d["payload_kinetic_energy_J"] for _, d in duties)
    bars = []
    y = 150
    colors = ["#3fd1c5", "#65adff", "#9b8cff", "#f2b65c"]
    for (name, d), color in zip(duties, colors):
        w = 650 * d["payload_kinetic_energy_J"] / max_e
        bars.append(f'<text x="70" y="{y}" fill="#eaf2ff" font-size="15">{name}</text>')
        bars.append(f'<rect x="410" y="{y-18}" width="{w:.1f}" height="24" rx="6" fill="{color}"/>')
        bars.append(f'<text x="{425+w:.1f}" y="{y}" fill="#91a5bd" font-size="13">{d["payload_kinetic_energy_J"]:.1f} J · {d["ideal_stroke_at_10g_m"]:.3f} m @ 10 g</text>')
        y += 58
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1500 520" role="img" aria-label="Gen6 architecture trade summary"><rect width="1500" height="520" rx="24" fill="#0b1220"/><g font-family="Inter,Segoe UI,sans-serif"><text x="55" y="58" fill="#eaf2ff" font-size="25" font-weight="700">GEN6 STARTS FROM MISSION DUTY, NOT MAXIMUM RELEASE SPEED</text><text x="55" y="88" fill="#91a5bd" font-size="15">4 kg reference payload · bar length = payload kinetic energy · stroke shown at 10 g</text>{''.join(bars)}<g transform="translate(70 400)"><rect width="1360" height="82" rx="14" fill="#101b2b" stroke="#25374c"/><text x="24" y="31" fill="#f2b65c" font-size="13" font-weight="700">P92: OPEN / UNDERDETERMINED</text><text x="24" y="57" fill="#eaf2ff" font-size="15">The low S4 duty makes a compact release cell worth sizing. Installed mass, retention/arrest, clearing time and fault isolation decide what wins.</text></g></g></svg>'''


def write_outputs(data):
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    FIGURE.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT.write_text(report(data), encoding="utf-8")
    FIGURE.write_text(svg(data), encoding="utf-8")


def check():
    data = build()
    expected = {
        RESULT: json.dumps(data, indent=2, sort_keys=True) + "\n",
        REPORT: report(data),
        FIGURE: svg(data),
    }
    bad = []
    for path, text in expected.items():
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            bad.append(str(path.relative_to(ROOT)))
    if bad:
        raise SystemExit("stale/missing architecture trade outputs: " + ", ".join(bad))
    print("P92 architecture trade outputs fresh")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        check()
    else:
        data = build()
        write_outputs(data)
        print(report(data))


if __name__ == "__main__":
    main()
