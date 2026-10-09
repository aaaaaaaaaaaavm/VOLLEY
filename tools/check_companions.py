"""Check the pinned Gen5 result snapshot used by standalone academic repositories.

The paper and thesis have their own manuscripts, figures, CAD and limitations. Their
source snapshot is deliberately dated; a newer flagship commit need not silently
rewrite published academic claims. The five decisive common files are compared by
SHA-256 when local companion checkouts are available. Without those checkouts the
gate verifies only the flagship's pinned files and explicitly reports that limit.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "tools/companion_export.json"
COMPANIONS = ("VOLLEY-paper", "VOLLEY-thesis")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    record = json.loads(RECORD.read_text())
    pinned = record["pinned_common_files_sha256"]
    errors = []
    checked = []
    for name in ("VOLLEY", *COMPANIONS):
        repo = ROOT if name == "VOLLEY" else ROOT.parent / name
        if not repo.is_dir():
            continue
        checked.append(name)
        for rel, expected in pinned.items():
            path = repo / rel
            if not path.is_file():
                errors.append(f"{name}: missing {rel}")
            elif digest(path) != expected:
                errors.append(f"{name}: {rel} differs from the pinned Gen5 academic result")
    if errors:
        print("companion snapshot: FAIL\n  " + "\n  ".join(errors))
        return 1
    absent = set(COMPANIONS) - set(checked)
    print(f"companion snapshot: {len(pinned)} common files match in {', '.join(checked)}"
          + (f"; unavailable locally: {', '.join(sorted(absent))}" if absent else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
