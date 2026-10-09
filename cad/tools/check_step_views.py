"""Check that public STEP-derived JPEG labels retain exact source provenance."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RECORD = ROOT / "cad/renders/step_review/PROVENANCE.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    record = json.loads(RECORD.read_text())
    if "not measured hardware" not in record["evidence_class"]:
        raise SystemExit("STEP view evidence classification missing")
    for config in ("gen5_reference", "r1_candidate"):
        source = record["freecad_source"][config]
        document = ROOT / source["native_document"]
        if sha256(document) != source["native_document_sha256"]:
            raise SystemExit(f"native FreeCAD source changed: {document}")
        for name, digest in source["source_steps"]:
            if sha256(ROOT / name) != digest:
                raise SystemExit(f"source STEP changed: {name}")
    views = record["views"]
    if len(views) != 6 or len({v["file"] for v in views}) != 6:
        raise SystemExit("expected six distinct STEP review views")
    for view in views:
        image = ROOT / view["file"]
        if image.suffix.lower() != ".jpg" or not image.is_file():
            raise SystemExit(f"missing JPEG: {image}")
        data = image.read_bytes()
        if not data.startswith(b"\xff\xd8") or not data.endswith(b"\xff\xd9"):
            raise SystemExit(f"incomplete JPEG: {image}")
        if sha256(image) != view["sha256"]:
            raise SystemExit(f"STEP view changed without provenance update: {image}")
        if "STEP-DERIVED" not in view["status_on_image"]:
            raise SystemExit(f"evidence label missing: {image}")
        if not view["included_instances"]:
            raise SystemExit(f"empty model view: {image}")
    print("STEP view provenance: six JPEGs and every native/STEP source hash match")


if __name__ == "__main__":
    main()
