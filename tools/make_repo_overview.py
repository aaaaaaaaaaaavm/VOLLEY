"""Generate the flagship README overview from committed results and the run-sheet register."""

from __future__ import annotations

import argparse
import json
import re
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BG, PANEL, INK, MUTED = "#07111b", "#0c1d2a", "#e8f0f7", "#8fa7ba"
CYAN, VIOLET, AMBER, RED, GREEN = "#38d6e8", "#9b8cff", "#ffb454", "#ff6b6b", "#61d6a3"


def txt(x: float, y: float, value: str, size: int, colour: str = INK, weight: int = 400,
        anchor: str = "start") -> str:
    return (
        f'<text x="{x}" y="{y}" fill="{colour}" font-family="Inter,Segoe UI,sans-serif" '
        f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>'
    )


def box(x: float, y: float, w: float, h: float, stroke: str = "#17384b", fill: str = PANEL,
        radius: int = 18) -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'


def load(name: str) -> dict:
    return json.loads((ROOT / "analysis" / "results" / name).read_text(encoding="utf-8"))


def validation_counts() -> tuple[int, int]:
    identifiers = []
    for path in (ROOT / "validation").glob("A*.md"):
        match = re.match(r"A(\d+)", path.name)
        if match:
            identifiers.append(int(match.group(1)))
    return len(identifiers), len(set(identifiers))


def render() -> str:
    shot = load("motor_results.json")["shot"]
    energy = load("sizing.json")["energy_closure"]
    run_sheets, analyses = validation_counts()
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">',
        f'<rect width="1600" height="900" fill="{BG}"/>',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#3f718c"/></marker></defs>',
        txt(72, 78, "VOLLEY · THE FLAGSHIP ENGINEERING RECORD", 24, CYAN, 700),
        txt(72, 124, "Command the release condition. Keep the spacecraft unmodified.", 35, INK, 650),
        txt(72, 162, "One mission, two architectures, and the evidence boundary between them.", 19, MUTED),
    ]

    stages = [
        ("HOST", "spent final stage", VIOLET),
        ("MAGAZINE", "12 × 3U", CYAN),
        ("COMMAND", "velocity per satellite", AMBER),
        ("RELEASE", "orbital energy changes", GREEN),
    ]
    for i, (title, subtitle, colour) in enumerate(stages):
        x, y = 72 + i * 382, 218
        out += [box(x, y, 326, 132, stroke=colour), txt(x + 26, y + 44, title, 15, colour, 700), txt(x + 26, y + 84, subtitle, 21, INK, 650)]
        if i < len(stages) - 1:
            out.append(f'<line x1="{x + 330}" y1="{y + 66}" x2="{x + 372}" y2="{y + 66}" stroke="#3f718c" stroke-width="3" marker-end="url(#arrow)"/>')

    cards = [
        (
            72, "GEN5 · FROZEN BASELINE", CYAN,
            [
                "self-contained Halbach LSM · 1.3 m acceleration",
                f"{shot['v_exit']:.3f} m/s · {shot['a_g']:.3f} g · {shot['t_ms']:.1f} ms",
                f"{shot['E_drawn'] / 1000:.3f} kJ gross · {energy['closure_pct']:.1f}% energy closure",
                "structural FEA · CFD · control design · second CAD implementation",
            ],
        ),
        (
            816, "GEN6 · CURRENT DESIGN TARGET", AMBER,
            [
                "stage-integrated cold gas · 8.0 m host-stage rail",
                "payload accelerated directly; duplicated machinery deleted",
                "trim stator suspended pending the seal result",
                "does not inherit Gen5 evidence; contact and provider interfaces remain open",
            ],
        ),
    ]
    for x, title, colour, lines in cards:
        y = 400
        out += [box(x, y, 708, 278, stroke=colour), txt(x + 30, y + 48, title, 17, colour, 700)]
        for row, line in enumerate(lines):
            out += [txt(x + 30, y + 98 + row * 43, "•", 20, colour, 700), txt(x + 58, y + 98 + row * 43, line, 17, INK if row < 3 else MUTED, 500)]

    out += [
        box(72, 728, 448, 98, stroke=CYAN, fill="#091720"),
        txt(100, 766, "DECLARED RECORD", 13, CYAN, 700),
        txt(100, 802, f"{run_sheets} run sheets · {analyses} analyses", 23, INK, 650),
        box(576, 728, 448, 98, stroke=RED, fill="#1b1116"),
        txt(604, 766, "PHYSICAL EVIDENCE", 13, RED, 700),
        txt(604, 802, "0 built · 0 fired · 0 measured", 23, INK, 650),
        box(1080, 728, 444, 98, stroke=AMBER, fill="#18160f"),
        txt(1108, 766, "MATURITY", 13, AMBER, 700),
        txt(1108, 802, "Phase I · TRL 2–3 design study", 23, INK, 650),
        txt(1494, 870, "MODEL OUTPUT UNLESS A SOURCE SAYS OTHERWISE", 15, MUTED, 650, "end"),
        "</svg>",
    ]
    return "\n".join(out) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = ROOT / "figures" / "V00_system_overview.svg"
    content = render()
    if args.check:
        if not output.exists() or output.read_text(encoding="utf-8") != content:
            raise SystemExit("stale generated file: figures/V00_system_overview.svg")
        print("overview current")
        return
    output.write_text(content, encoding="utf-8")
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
