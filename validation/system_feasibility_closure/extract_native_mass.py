"""Extract the conditional mission mass input from the actual native assembly."""
from pathlib import Path
import argparse,hashlib,importlib.util,json

H=Path(__file__).resolve().parent

def main(source,native):
    spec=importlib.util.spec_from_file_location('fm08_source',source)
    b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
    document=b.App.openDocument(str(native))
    items=[dict(name=o.Label,shape=o.Shape,material=o.Material,role=o.Role,notes=o.EvidenceBoundary)
           for o in document.Objects if hasattr(o,'Shape')]
    result=dict(study='CAP-12 represented material ledger from actual native assembly',
        source_sha256=hashlib.sha256(Path(source).read_bytes()).hexdigest(),
        native_sha256=hashlib.sha256(Path(native).read_bytes()).hexdigest(),
        captures=[dict(parts=len(items),mass_properties=b.massprops(items))],
        geometry_acceptance='Separate assembly interference/STEP report; mass extraction is not geometry acceptance')
    (H/'TWELVE_MASS_LEDGER.json').write_text(json.dumps(result,indent=2)+'\n')
    b.App.closeDocument(document.Name)
    print(result['captures'][0]['mass_properties']['represented_material_mass_kg'])

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--native',required=True);a=p.parse_args();main(a.source,a.native)
