"""Freeze this public package and its scientific figure/source inventory."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    families=[
      dict(stem='lunar_independent_disposal',generator='complete_studies.py',data=['STUDY_RESULTS.json'],
           role='Finite engine-only disposal and explicitly different launch-delivery energy boundaries; declared surrogate,not a supplier orqualified lunar system.'),
      dict(stem='lunar_release_lifetime',generator='build_report.py',data=['LUNAR_NATIVE_RESULTS.json'],
           role='18actual signed-release native30day lunar coasts; sampled spherical-altitude floor and20/40-degree sensitivity,not terrain/lifetime qualification.'),
      dict(stem='lunar_campaign_resources',generator='campaign_report.py',data=['CAMPAIGN_RESULTS.json','campaign/T5_R20_searched.json','CAMPAIGN_NATIVE_RESULTS.json','CAMPAIGN_DISPOSAL_RESULTS.json'],
           role='Finite-source/attitude campaign mass,propellant,rate andmatched policy histories; source-calibrated imposed release,not a physical pulse/contact validation.')]
    inventory=[]
    for row in families:
        outputs={str(Path('figures')/(row['stem']+'.'+ext)):sha(HERE/'figures'/(row['stem']+'.'+ext)) for ext in ['svg','png','pdf']}
        inventory.append(dict(**row,generator_sha256=sha(HERE/row['generator']),
                              source_data_sha256={name:sha(HERE/name) for name in row['data']},output_sha256=outputs,
                              style='scientific.mplstyle',style_sha256=sha(HERE/'scientific.mplstyle'),image_kind='Scientific plot from actual numerical outputs,no synthesized software interface'))
    (HERE/'FIGURE_SOURCE_INVENTORY.json').write_text(json.dumps(dict(study='PCS-ACR1-01',figures=inventory),indent=2)+'\n')
    files={}
    for path in sorted(HERE.rglob('*')):
        if path.is_file() and path.name!='MANIFEST.json' and '__pycache__' not in path.parts:
            files[str(path.relative_to(HERE))]=dict(bytes=path.stat().st_size,sha256=sha(path))
    result=dict(study='PCS-ACR1-01',scope='Package-local source,inputs,actual output captures,figures,flowdown andverification; controlling repository summaries are tracked by their publication packages.',files=files)
    (HERE/'MANIFEST.json').write_text(json.dumps(result,indent=2)+'\n')
    print(f'Frozen {len(files)} package files,{sum(x["bytes"] for x in files.values())} bytes')


if __name__=='__main__':main()
