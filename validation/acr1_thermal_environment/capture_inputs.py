"""Copy exact accepted ACR1 inputs and capture thermal primary-source identities.

Government reference documents are retained. Manufacturer PDFs are read only to
record their hashes; no third-party PDF redistribution is assumed.
"""
import hashlib
import json
import shutil
import urllib.request
import urllib.error
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    dest=HERE/'inputs';dest.mkdir(exist_ok=True);sources=HERE/'sources';sources.mkdir(exist_ok=True)
    files=['analysis/COUPLED_SHOT.json','analysis/POWER_COMPONENT_REFERENCE.json','analysis/RESOURCE_LEDGER.json','analysis/DESIGN_BUDGETS.json',
           'analysis/FEEDER_SIZING.json','analysis/LIFT_SIZING.json','cad/PARAMETERS.json','cad/release/VOLLEY_G5_ACR1_home.json',
           'cad/build_acr1.py','cad/cradle_acr1.py','mission/MISSION_INPUTS.json',
           'analysis/coupled_shot.py','analysis/FINITE_MOTOR.json','analysis/ARREST_FORCE_MAP.json']
    manifest=[]
    for name in files:
        p=ROOT/'validation/acr1'/name;q=dest/('coupled_shot_production.py' if p.name=='coupled_shot.py' else p.name);shutil.copyfile(p,q)
        manifest.append(dict(path='inputs/'+q.name,original_public_path='validation/acr1/'+name,sha256=sha(q)))
    for phase,h in [('A','2'),('B','3'),('C','3')]:
        name=f'analysis/conduction/phase_{phase}/h{h}/RESULT.json';p=ROOT/'validation/acr1'/name;q=dest/f'CONDUCTION_PHASE_{phase}.json';shutil.copyfile(p,q)
        manifest.append(dict(path='inputs/'+q.name,original_public_path='validation/acr1/'+name,sha256=sha(q)))
    shutil.copyfile(ROOT/'tools/scientific.mplstyle',HERE/'scientific.mplstyle')
    (HERE/'INPUT_SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    references=[
      ('NASA_ARC_8070_1','https://www.nasa.gov/sites/default/files/atoms/files/std8070.1.pdf','NASA Ames ARC-STD-8070.1,18December2018,sections3.4.3.1.1/3.4.3.1.3','Government reference environmental bands1322/1367/1414Wm-2 andEarthIR234±7Wm-2; applicability is Ames missions,not universalVOLLEY compliance.',True),
      ('NASA_RP_1121','https://ntrs.nasa.gov/api/citations/19840015630/downloads/19840015630.pdf','NASA-RP-1121,JohnHenninger,April1984','Measured optical examples depend on surface preparation; unknown ACR1 finish is investigated,not silently assigned a qualified coating.',True),
      ('NASA_SST_THERMAL_2026','https://www.nasa.gov/smallsat-institute/sst-soa/thermal-control/','NASA SmallSpacecraftTechnology,chapter7,7May2026,sections7.1/7.2.3','Vacuum conduction/radiation balance; illustrative bolt conductances0.105–3.51W/K per listed screw/interface class,not actual ACR1 mounting acceptance.',True),
      ('NIST_G10CR','https://trc.nist.gov/cryogenics/materials/G-10%20CR%20Fiberglass%20Epoxy/G10CRFiberglassEpoxy_rev.htm','NIST CryogenicMaterialsPropertyDatabase,G10-CR,fits4–300K','At300K:normal conductivity0.607983W/mK,specific heat998.743J/kgK. Generic GFRP grade and hot-temperature extrapolation remain uncertain.',True),
      ('NASA_EARTH_GUIDELINES','https://ntrs.nasa.gov/api/citations/20020004360/downloads/20020004360.pdf','NASA/TM-2001-211221,Anderson etal,Guidelines forselection ofnearEarththermalparameters','Thermal-response-time dependent albedo/OLR guidance; our selected broad investigation band is not a percentile or provider-specific environment.',True),
      ('ARNOLD_N48M_REFERENCE','https://www.arnoldmagnetics.com/wp-content/uploads/2017/11/N48M-151021.pdf','Arnold N48M material sheet,Rev210802','Representative NdFeB specific heat0.11cal/gK≈460J/kgK;Br coefficient−0.12%/K over20–100C. This grade is not selected for ACR1; no universal magnet limit is assigned.',False)]
    components=json.loads((dest/'POWER_COMPONENT_REFERENCE.json').read_text())['sources']
    references+=[('EATON_TV_REFERENCE',components['eaton_tv']['url'],'Frozen Eaton TV source reference','Selected cell catalogue operation−40..65C; extended85C point requires2.5V/cell. No vacuum/space qualification follows.',False),
                 ('IRFP4668_REFERENCE',components['irfp4668']['url'],'Frozen Infineon IRFP4668 reference','Junction/case thermal resistance and absolute-temperature/current limits are distinct from mounting and flight acceptance.',False)]
    cache=Path('/tmp/volley-acr1-thermal-reference-cache');cache.mkdir(exist_ok=True);records=[]
    for key,url,version,use,public in references:
        try:raw=urllib.request.urlopen(url,timeout=60).read()
        except urllib.error.HTTPError as e:
            records.append(dict(id=key,url=url,accessed_utc='2026-10-25',version=version,use=use,download_status=f'HTTP{e.code}',
                                sha256=None,local_public_path=None,extraction_note='Primary page independently read through connected web source; no upstream byte hash is fabricated. Structured numeric fact capture retained separately.'))
            continue
        ext='.pdf' if raw.startswith(b'%PDF') else '.html'
        path=(sources if public else cache)/(key+ext);path.write_bytes(raw)
        records.append(dict(id=key,url=url,accessed_utc='2026-10-25',version=version,use=use,bytes=len(raw),sha256=sha(path),
                            local_public_path=str(path.relative_to(HERE)) if public else None,full_manufacturer_PDF_redistributed=False))
    (HERE/'PRIMARY_SOURCE_REGISTER.json').write_text(json.dumps(records,indent=2)+'\n')
    print('Captured accepted ACR1 inputs andprimary source outcomes')


if __name__=='__main__':main()
