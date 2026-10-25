"""Replay an immutable captured GMAT script against a caller-selected installation.

No captured source or raw result is edited. Runtime/output paths alone are
translated into a new script; original/translated identities and actual runtime
hashes are recorded separately. Supports GMAT_CONSOLE and GMAT_ROOT selectors.
"""
import argparse
import gzip
import hashlib
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def startup_copy(source,root,out):
    lines=[]
    for line in source.read_text().splitlines():
        match=re.match(r'^(\s*)([A-Z0-9_]+)(\s*=\s*)([^#]*)(.*)$',line)
        if not match:lines.append(line);continue
        prefix,key,eq,value,comment=match.groups();value=value.strip()
        if key=='OUTPUT_PATH':value=str(out)+'/'
        elif key=='LOG_FILE':value=str(out/'GmatLog.txt')
        elif value.startswith(('../','./')):value=str((root/'bin'/value).resolve())
        lines.append(prefix+key+eq+value+(' '+comment if comment else ''))
    return '\n'.join(lines)+'\n'


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--gmat',default=os.environ.get('GMAT_CONSOLE'),help='GmatConsole path or command; defaults to GMAT_CONSOLE')
    p.add_argument('--gmat-root',type=Path,default=os.environ.get('GMAT_ROOT'),help='Normal GMAT distribution root; defaults to GMAT_ROOT or executable parent-parent')
    p.add_argument('--gravity',type=Path,help='Optional alternative GRGM900C file; otherwise root/data/gravity/luna/grgm900c.cof')
    p.add_argument('--script',type=Path,default=Path('campaign_native/point_mass.script'),help='Captured script,relative to this package or absolute')
    p.add_argument('--output-dir',required=True,type=Path,help='New directory for translated source,startup,raw log,reports and receipt')
    args=p.parse_args()
    if not args.gmat:p.error('Supply --gmat or GMAT_CONSOLE for an installed GMAT R2026a console')
    selected=shutil.which(args.gmat) or args.gmat;gmat=Path(selected).expanduser().resolve()
    if not gmat.is_file():p.error('Selected GMAT console does not exist')
    root=Path(args.gmat_root).expanduser().resolve() if args.gmat_root else gmat.parent.parent
    gravity=args.gravity.expanduser().resolve() if args.gravity else root/'data/gravity/luna/grgm900c.cof'
    required=['bin/gmat_startup_file.txt','data/planetary_ephem/de/leDE1900.421',
              'data/planetary_coeff/SPICELunaCurrentKernel.bpc','data/planetary_coeff/SPICELunaFrameKernel.tf','data/time/tai-utc.dat']
    for name in required:
        if not (root/name).is_file():p.error(f'GMAT installation input missing:{root/name}')
    if not gravity.is_file():p.error('Selected lunar gravity file does not exist')
    source=args.script if args.script.is_absolute() else HERE/args.script
    source=source.resolve()
    if not source.is_file():p.error('Captured script does not exist')
    out=args.output_dir.expanduser().resolve()
    # Prevent this adapter from overwriting any accepted capture directory.
    protected=[HERE/name for name in ['native','disposal_native','campaign_native','campaign_disposal']]
    if any(out==x or out.is_relative_to(x) or x.is_relative_to(out) for x in protected):p.error('Output must be separate from all accepted capture directories')
    out.mkdir(parents=True,exist_ok=True)
    script=out/(source.stem+'.script')
    if script.exists():p.error('Translated script already exists; choose a new output directory to preserve prior run identity')
    original_sha=sha(source);text=source.read_text()
    def translate(match):
        value=match.group(1)
        if '/data/' in value and value.startswith('/'):
            suffix=value.split('/data/',1)[1]
            mapped=gravity if suffix.endswith('grgm900c.cof') else root/'data'/suffix
            return "'"+str(mapped)+"'"
        if value.startswith('/') and (value.endswith('.txt') or value.endswith('.csv')):
            return "'"+str(out/Path(value).name)+"'"
        return match.group(0)
    translated=re.sub(r"'([^']*)'",translate,text)
    # All absolute data/output paths must be mapped; a retained private path
    # would defeat the purpose of this portability adapter.
    for value in re.findall(r"'([^']*)'",translated):
        if value.startswith('/'):
            selected_path=Path(value)
            if not (selected_path.is_relative_to(root) or selected_path.is_relative_to(out) or selected_path==gravity):
                p.error('Captured script contains an unrecognized absolute path; refusing an incomplete translation')
    script.write_text(translated)
    startup=out/'gmat_startup_file.txt';startup.write_text(startup_copy(root/'bin/gmat_startup_file.txt',root,out))
    command=[str(gmat),'--startup_file',str(startup),'--logfile',str(out/'native_gmat.log'),'--run',str(script),'--exit']
    r=subprocess.run(command,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (out/'console.log').write_text(r.stdout)
    assert sha(source)==original_sha,'Original captured source was modified'
    reports=[]
    for report in out.glob('*.txt'):
        if report.name=='gmat_startup_file.txt':continue
        with gzip.open(report.with_suffix(report.suffix+'.gz'),'wb') as f:f.write(report.read_bytes())
        comparison=dict(path=report.name,sha256=sha(report),gzip_sha256=sha(report.with_suffix(report.suffix+'.gz')))
        captured=source.parent/(report.name+'.gz')
        if captured.is_file():
            with gzip.open(captured,'rb') as f:expected=hashlib.file_digest(f,'sha256').hexdigest()
            comparison['captured_decompressed_sha256']=expected
            comparison['identical_decompressed_output']=expected==comparison['sha256']
        reports.append(comparison)
    reference=json.loads((HERE/'native/SOURCE_IDENTITY.json').read_text())
    actual_data={name:sha(root/name) for name in required}
    runtime_identical=(sha(gmat)==reference['GMAT_binary_sha256'] and sha(gravity)==reference['gravity_file_sha256']
                       and all(actual_data[name]==reference['supporting_runtime_sha256'][name] for name in required if name!='bin/gmat_startup_file.txt'))
    receipt=dict(adapter_sha256=sha(__file__),captured_source_path=str(source.relative_to(HERE)) if source.is_relative_to(HERE) else str(source),
                 captured_source_sha256=original_sha,translated_source_sha256=sha(script),
                 selected_GMAT_binary_sha256=sha(gmat),selected_gravity_sha256=sha(gravity),selected_data_sha256=actual_data,
                 selected_runtime_matches_captured_core_inputs=runtime_identical,
                 translated_startup_sha256=sha(startup),original_sources_modified=False,
                 invocation=command,exit_code=r.returncode,mission_run_completed='Mission run completed' in r.stdout,
                 reports=reports,
                 interpretation='Path/startup adapter run. Original executed source identities remain unchanged. A changed runtime is recorded as changed evidence,not relabeled as the accepted capture.')
    (out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(dict(exit_code=r.returncode,mission_completed=receipt['mission_run_completed'],original_source_unchanged=True,
                          selected_runtime_matches_captured_core_inputs=runtime_identical,reports=len(reports),
                          identical_reports=sum(x.get('identical_decompressed_output',False) for x in reports)),indent=2))
    if r.returncode or not receipt['mission_run_completed']:raise SystemExit(1)


if __name__=='__main__':main()
