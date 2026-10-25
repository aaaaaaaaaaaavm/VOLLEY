#!/usr/bin/env python3
"""Run selected ACR1 examples in a disposable copy; accepted captures stay immutable."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys,tempfile,urllib.request
ROOT=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('example',choices=['interlocks','shot','mission','native'])
    ap.add_argument('--output',type=Path,required=True,help='New directory for reproduced output and source')
    ap.add_argument('--jars',type=Path,help='Orekit/Hipparchus jars matching mission/SOFTWARE_LOCK.json')
    ap.add_argument('--download-jars',action='store_true',help='Fetch locked Maven jars into output (native only)')
    a=ap.parse_args();out=a.output.resolve()
    if out.exists():ap.error('--output must be a new directory')
    out.mkdir(parents=True);work=out/'acr1';shutil.copytree(ROOT,work,ignore=shutil.ignore_patterns('__pycache__'))
    commands={'interlocks':'analysis/transfer_interlocks.py','shot':'analysis/coupled_shot.py','mission':'mission/mission_model.py','native':'mission/native_checks.py'}
    adapters=[]
    if a.example=='native':
        jars=a.jars.resolve()if a.jars else out/'jars'
        lock=json.loads((ROOT/'mission/SOFTWARE_LOCK.json').read_text())
        if a.download_jars:
            jars.mkdir(parents=True,exist_ok=True)
            for item in lock['artifacts']:
                urllib.request.urlretrieve(item['url'],jars/item['name'])
        for item in lock['artifacts']:
            p=jars/item['name']
            if not p.is_file()or hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:ap.error(f'missing or changed locked jar: {p}')
        script=work/commands[a.example];text=script.read_text();old='/workspace/volley-work/2026-10-18/jars/*'
        assert old in text;script.write_text(text.replace(old,str(jars/'*')))
        adapters.append('Replaced recorded jar-directory selector in scratch native_checks.py; force model and target data unchanged. Adapter changes source hash; frozen capture identity is not reasserted.')
    subprocess.run([sys.executable,str(work/commands[a.example])],cwd=work,check=True)
    receipt={'configuration_id':'VOLLEY-G5-ACR1','example':a.example,'command':[sys.executable,commands[a.example]],'adapters':adapters,'output':str(work),'scope':'Actual selected example run. No new physical validation or full-package rebuild inferred.'}
    (out/'REPRODUCTION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(f'Reproduction outputs: {work}')
if __name__=='__main__':main()
