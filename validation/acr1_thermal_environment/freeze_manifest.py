"""Freeze all package/report bytes; verification receipts are kept outside the hash cycle."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent
EXCLUDED={'PUBLIC_SOURCE_MANIFEST.json','CAPTURE_CHECKS.json'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 files=[p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in EXCLUDED]
 records=[dict(path=str(p.relative_to(P)),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(files)]
 report=P.parents[1]/'docs/ACR1_THERMAL_ENVIRONMENT.md';records.append(dict(path='../../docs/ACR1_THERMAL_ENVIRONMENT.md',bytes=report.stat().st_size,sha256=sha(report)))
 result=dict(study='ACR1-THERM-ENV-01',scope='Self-contained supplement and its public report. Original public ACR1 source identities pinned separately.',excluded_generated_receipts=sorted(EXCLUDED),files=records,count=len(records),total_bytes=sum(r['bytes'] for r in records))
 (P/'PUBLIC_SOURCE_MANIFEST.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(count=len(records),bytes=result['total_bytes'],manifest_sha256=sha(P/'PUBLIC_SOURCE_MANIFEST.json'))))
if __name__=='__main__':main()
