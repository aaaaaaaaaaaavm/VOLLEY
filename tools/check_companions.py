"""Verify current ACR1 packages and the separate historical five-file snapshot.

Current engineering files are pinned across validation/acr1 and each companion's
current/ package. Each available package manifest is checked against actual bytes.
The original five pins stay historical: archived paths are preferred in new
companions, with root paths supported in older clones. A present old clone must
still obtain the current ACR1 package before the current comparison can pass.

A flagship-only CI checkout explicitly reports unavailable companion comparisons.
This gate does not claim remote synchronization. The historical export_companion.py
cannot generate this current schema and must not overwrite the academic packages.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "tools/companion_export.json"
COMPANIONS = ("VOLLEY-paper", "VOLLEY-thesis")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contained(base: Path, relative: str) -> Path:
    path = (base / relative).resolve()
    if Path(relative).is_absolute() or not path.is_relative_to(base.resolve()):
        raise ValueError(f"manifest path escapes package: {relative}")
    return path


def verify_file(base: Path, relative: str, expected: str, label: str,
                errors: list[str], size: int | None = None) -> None:
    try:
        path = contained(base, relative)
        if not SHA256.fullmatch(expected):
            raise ValueError(f"invalid SHA256 for {relative}")
        if not path.is_file():
            errors.append(f"{label}: missing {relative}")
        elif digest(path) != expected:
            errors.append(f"{label}: SHA256 differs: {relative}")
        elif size is not None and path.stat().st_size != size:
            errors.append(f"{label}: byte count differs: {relative}")
    except (OSError, ValueError) as exc:
        errors.append(f"{label}: {exc}")


def sha_manifest(repo: Path, relative: str, errors: list[str]) -> dict[str, str]:
    """Read and verify the actual local SHA256 manifest, including unpinned files."""
    entries: dict[str, str] = {}
    label = f"{repo.name}/{relative}"
    try:
        manifest = contained(repo, relative)
        for line in manifest.read_text().splitlines():
            if not line.strip():
                continue
            expected, name = line.split("  ", 1)
            if name in entries:
                raise ValueError(f"duplicate manifest path: {name}")
            entries[name] = expected
            verify_file(manifest.parent, name, expected, label, errors)
        if not entries:
            raise ValueError("empty manifest")
    except (OSError, ValueError) as exc:
        errors.append(f"{label}: {exc}")
    return entries


def main_manifest(repo: Path, relative: str, configuration: str,
                  errors: list[str]) -> dict[str, str]:
    entries: dict[str, str] = {}
    label = f"{repo.name}/{relative}"
    try:
        manifest = contained(repo, relative)
        data = json.loads(manifest.read_text())
        if data["configuration_id"] != configuration:
            raise ValueError("configuration ID differs")
        for name, item in data["files"].items():
            entries[name] = item["sha256"]
            verify_file(manifest.parent, name, item["sha256"], label, errors,
                        size=item["bytes"])
        if not entries:
            raise ValueError("empty manifest")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"{label}: {exc}")
    return entries


def verify_facts(base: Path, checks: list[dict], label: str,
                 errors: list[str]) -> None:
    for check in checks:
        try:
            value = json.loads(contained(base, check["path"]).read_text())
            for key in check.get("keys", []):
                value = value[key]
            operation = check.get("operation", "equals")
            if operation == "length":
                value = len(value)
            elif operation == "supported_shot_cases":
                rows = [row for row in value if row["target_m_s"] in (1, 2, 3)]
                value = {"count": len(rows), "all_passed": all(
                    row["all_declared_checks_pass"] for row in rows)}
            elif operation != "equals":
                raise ValueError(f"unknown fact operation: {operation}")
            expected = check["expected"]
            if type(value) is not type(expected) or value != expected:
                errors.append(f"{label}: current fact differs: {check['path']} "
                              f"{check.get('keys', [])}")
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append(f"{label}: cannot check fact {check['path']}: {exc}")


def check_repository_set(root: Path, record: dict,
                         companion_paths: dict[str, Path] | None = None) -> dict:
    """Validate real repositories; explicit paths also permit isolated falsifiers."""
    result = {"errors": [], "checked": [], "absent": [],
              "historical_layout": {}, "manifest_entries": {}}
    errors = result["errors"]
    if record.get("schema_version") != 2 or not record.get("current_acr1"):
        errors.append("current ACR1 companion schema missing; do not regenerate it "
                      "with the historical exporter")
        return result
    current = record["current_acr1"]
    companions = companion_paths if companion_paths is not None else {
        name: root.parent / name for name in COMPANIONS}
    repositories = [("VOLLEY", root, False)]
    for name in COMPANIONS:
        repo = companions[name]
        if not repo.is_dir():
            result["absent"].append(name)
        else:
            repositories.append((name, repo, True))
    for name, repo, companion in repositories:
        result["checked"].append(name)
        history = repo
        if companion and (repo / record["historical_companion_prefix"]).is_dir():
            history = repo / record["historical_companion_prefix"]
        result["historical_layout"][name] = str(history.relative_to(repo)) or "."
        for relative, expected in record["pinned_common_files_sha256"].items():
            verify_file(history, relative, expected, f"{name} historical", errors)
        prefix = current["companion_prefix" if companion else "flagship_prefix"]
        try:
            base = contained(repo, prefix)
        except ValueError as exc:
            errors.append(f"{name}: {exc}")
            continue
        if not base.is_dir():
            errors.append(f"{name}: current ACR1 package missing: {prefix}; "
                          "historical checks do not establish current agreement")
            continue
        if companion:
            entries = sha_manifest(repo, current["companion_manifest"], errors)
            outer = sha_manifest(repo, current["companion_root_manifest"], errors)
            if current["companion_manifest"] not in outer:
                errors.append(f"{name}: root manifest does not identify current manifest")
            result["manifest_entries"][name] = {
                "current": len(entries), "outer": len(outer)}
        else:
            entries = main_manifest(repo, current["flagship_manifest"],
                                    current["configuration_id"], errors)
            result["manifest_entries"][name] = {"current": len(entries)}
        for relative, expected in current["files_sha256"].items():
            verify_file(base, relative, expected, f"{name} current ACR1", errors)
            if entries.get(relative) != expected:
                errors.append(f"{name}: current manifest does not pin {relative}")
        verify_facts(base, current["fact_checks"], name, errors)
    return result


def main() -> int:
    try:
        record = json.loads(RECORD.read_text())
        result = check_repository_set(ROOT, record)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"companion snapshot: FAIL: {exc}")
        return 1
    if result["errors"]:
        print("companion snapshot: FAIL\n  " + "\n  ".join(result["errors"]))
        return 1
    print(f"companion snapshot: PASS local {len(record['current_acr1']['files_sha256'])} "
          f"current ACR1 pins, {len(record['current_acr1']['fact_checks'])} fact checks "
          f"and {len(record['pinned_common_files_sha256'])} historical pins in "
          + ", ".join(result["checked"]))
    print("verified manifests: " + json.dumps(result["manifest_entries"], sort_keys=True))
    print("historical layouts: " + json.dumps(result["historical_layout"], sort_keys=True))
    if result["absent"]:
        print("NOT RUN: local companion comparison unavailable for "
              + ", ".join(result["absent"]) + "; no remote synchronization inferred")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
