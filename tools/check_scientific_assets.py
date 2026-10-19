"""Verify released figure identities and basic editable-SVG structure.

This gate checks file/source identity, not scientific validity or visual quality.
"""
from pathlib import Path
import hashlib,json,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
def main():
    record=json.loads((ROOT/"docs/SCIENTIFIC_FIGURES.json").read_text())
    checked=0
    for figure in record["figures"]:
        for kind in ("sources","exports"):
            for name,expected in figure[kind].items():
                rel=Path(name)
                assert not rel.is_absolute() and ".." not in rel.parts,name
                path=ROOT/rel
                assert path.is_file(),f"Missing {kind}: {name}"
                assert hashlib.sha256(path.read_bytes()).hexdigest()==expected,f"Stale {kind}: {name}"
                if kind=="exports" and path.suffix==".svg":
                    svg=ET.fromstring(path.read_text())
                    assert svg.tag.endswith("svg") and svg.get("viewBox"),name
                    assert any(x.tag.endswith("text") for x in svg.iter()),f"No editable SVG text: {name}"
                checked+=1
        assert figure["evidence_class"] and figure["caption"] and figure["limitations"]
    print(f"PASS: {len(record['figures'])} released figure records, {checked} source/export identities; visual and engineering review remain separate")
if __name__=="__main__":main()
