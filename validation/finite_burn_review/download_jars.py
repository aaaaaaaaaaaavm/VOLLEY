"""Fetch the exact public Java dependencies recorded in SOFTWARE_LOCK.json."""
from pathlib import Path
import hashlib,json,urllib.request
H=Path(__file__).resolve().parent;O=H/'jars';O.mkdir(exist_ok=True)
for item in json.loads((H/'SOFTWARE_LOCK.json').read_text())['artifacts']:
    target=O/item['name']
    if not target.exists():
        with urllib.request.urlopen(item['url'],timeout=60) as response:
            data=response.read()
        if hashlib.sha256(data).hexdigest()!=item['sha256']:
            raise RuntimeError('Dependency hash mismatch: '+item['name'])
        temporary=target.with_suffix('.part');temporary.write_bytes(data);temporary.replace(target)
    if hashlib.sha256(target.read_bytes()).hexdigest()!=item['sha256']:
        raise RuntimeError('Cached dependency hash mismatch: '+item['name'])
    print('Verified',item['name'])
