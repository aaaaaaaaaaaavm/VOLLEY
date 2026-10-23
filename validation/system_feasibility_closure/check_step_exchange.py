"""Separate CadQuery/OCC import of the two actual twelve-cell STEP exports."""
from pathlib import Path
import hashlib,json,platform
import cadquery as cq
import OCP

H=Path(__file__).resolve().parent

def main():
    r=json.loads((H/'TWELVE_ASSEMBLY_REPORT.json').read_text())
    rows=[]
    for c in r['captures']:
        p=H/'cad_twelve'/c['step']
        imported=cq.importers.importStep(str(p))
        solids=imported.solids().vals();volume=sum(s.Volume() for s in solids)
        expected=sum(x['volume_mm3'] for x in c['BOM'])
        delta=abs(volume-expected)/expected
        valid=all(s.isValid() for s in solids)
        assert valid and len(solids)==c['step_solids'] and delta<1e-6,(p.name,valid,len(solids),delta)
        rows.append(dict(file=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
            valid=valid,solid_count=len(solids),expected_solid_count=c['step_solids'],
            imported_volume_mm3=volume,expected_BOM_volume_mm3=expected,
            relative_volume_difference=delta,pass_1ppm=True))
    report=dict(study='CAP-12 separate STEP import check',software=dict(Python=platform.python_version(),CadQuery=cq.__version__,OCP=getattr(OCP,'__version__','unreported')),
        checks=rows,scope='SeparateimportandBRepvalidity/serializationcheck;sameOCCkernelfamily,notphysicalvalidationorindependentkernelcertification')
    (H/'STEP_EXCHANGE_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS',len(rows),'twelve-cellSTEPimports')

if __name__=='__main__':main()
