"""Package editable film inputs without recursive release hashes or review screenshots."""
from pathlib import Path
import zipfile
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent
with zipfile.ZipFile(ROOT/'downloads/VOLLEY_ACR1_film_sources.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for p in sorted(HERE.rglob('*')):
  if p.is_file()and p.suffix in ['.py','.json','.csv','.md','.cjs','.txt']and '__pycache__'not in str(p)and p.name not in ['SITE_QA.json','FINAL_FILM_QA.json','SCENE_PACKAGE_MANIFEST.json','ARCHIVE_PRIVACY_REVIEW.json','FINAL_ASSET_IDENTITY_REVIEW.json','PUBLIC_METADATA_QA.json']:
   z.write(p,str(p.relative_to(ROOT)))
 for p in sorted([*(ROOT/'assets/acr1').iterdir(),*(ROOT/'assets/acr1/supplements').iterdir()]):
  if p.is_file()and p.suffix in ['.jpg','.png','.json']and p.name!='ASSET_REGISTER.json':z.write(p,str(p.relative_to(ROOT)))
print('Packaged editable source:',(ROOT/'downloads/VOLLEY_ACR1_film_sources.zip').stat().st_size,'bytes')
