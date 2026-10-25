#!/usr/bin/env python3
"""Check drawing/source identities, real projection coverage and accepted mass/budget values."""
from pathlib import Path
import csv,hashlib,json,math,subprocess,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
S=ROOT/'validation/acr1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
    manifest=read(HERE/'MANIFEST.json');capture=read(HERE/'PROJECTION_CAPTURE.json')
    for name,item in manifest['files'].items():
        path=(HERE/name).resolve();assert path.is_relative_to(HERE)and path.is_file(),name
        assert path.stat().st_size==item['bytes']and sha(path)==item['sha256'],f'Changed drawing/source: {name}'
    for name,expected in capture['source_identities'].items():assert sha(S/name)==expected,f'Frozen source changed: {name}'
    assert capture['source_unchanged_after_generation']
    for name,item in capture['projections'].items():
        assert item['visible_edge_count']>0,name
        assert item['objects']and len(set(item['objects']))==len(item['objects']),name
        assert item['curve_chord_deflection_mm']==.04,name
    assert capture['projections']['D02_section']['section_plane_X_mm']==400
    assert capture['envelope_mm']=={'X':[0.,2250.],'Y':[-620.,620.],'Z':[-190.,1158.9]}
    bom=list(csv.DictReader((HERE/'BOM_HOME.csv').open()));assert len(bom)==387
    assert math.isclose(sum(float(r['assigned_mass_kg'])for r in bom),197.55671970039353,abs_tol=1e-9)
    mass=read(HERE/'MASS_PROPERTIES.json');assert len(mass['states'])==8 and mass['unplaced_power_control_allowance_kg']==7
    assert mass['states']==read(S/'verification/MASS_CG_INERTIA_SUMMARY.json')['states']
    plans=list(csv.DictReader((HERE/'INSPECTION_PLAN.csv').open()));assert len(plans)==7 and all(r['actual_result']=='NOT_PERFORMED'for r in plans)
    for path in sorted(HERE.glob('D*.svg')):
        root=ET.parse(path).getroot();assert root.get('width')=='420mm'and root.get('height')=='297mm'
        assert root.get('viewBox')=='0 0 1680 1188'
        pdf=path.with_suffix('.pdf');data=pdf.read_bytes();assert data.startswith(b'%PDF-')and b'%%EOF'in data[-2048:]
        text=subprocess.check_output(['pdftotext',str(pdf),'-'],text=True)
        assert 'NOT A MANUFACTURING RELEASE'in text and 'VOLLEY-G5-ACR1'in text,pdf.name
        info=subprocess.check_output(['pdfinfo',str(pdf)],text=True)
        assert 'Pages:           1'in info and 'A3'in info,pdf.name
    combined=subprocess.check_output(['pdfinfo',str(HERE/'ACR1_DRAWING_SET.pdf')],text=True)
    assert 'Pages:           6'in combined and 'A3'in combined
    budget=read(S/'analysis/DESIGN_BUDGETS.json')
    annotations=(HERE/'D05_tolerance_assembly_inspection.svg').read_text()
    assert f"{budget['magnetic_face_budget']['minimum_individual_face_budget_mm']:.6f}"in annotations
    assert f"{budget['endwall_rigid_stack'][-1]['rigid_stack_residual_mm']:.6f}"in annotations
    assert len(list(HERE.glob('D*.svg')))==6 and len(capture['projections'])==7
    print(f'PASS:6 paired A3 outline sheets;7 actual TechDraw projections/section;387 BOM parts;8 accepted mass-property states;7 unperformed inspection rows;{len(manifest["files"])} file identities')
if __name__=='__main__':main()
