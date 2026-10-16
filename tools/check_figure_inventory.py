"""Verify the exact images and source documents in the reviewed figure inventory."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
record = json.loads((ROOT / 'docs/GEN5_ACADEMIC_FIGURES.json').read_text())
for item in record['figures']:
    path = ROOT / item['path']
    if hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
        raise SystemExit('FAIL: reviewed image changed: ' + item['path'])
for rel, expected in record['document_sha256'].items():
    if hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() != expected:
        raise SystemExit('FAIL: figure source document changed: ' + rel)
print(f"PASS: {len(record['figures'])} reviewed image identities and source documents")
