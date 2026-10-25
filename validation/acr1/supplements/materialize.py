#!/usr/bin/env python3
"""Verify/reassemble the exact ACR1 raw solver archive and safely restore its 60 files.

Standard library only. --verify-only never extracts. --output restores into a
scratch directory, retaining matching files and refusing every nonmatching file.
"""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,os,stat,sys,tempfile,zipfile
ROOT=Path(__file__).resolve().parents[1]
BLOCK=1024*1024

def hash_stream(stream):
    h=hashlib.sha256();size=0
    while True:
        chunk=stream.read(BLOCK)
        if not chunk:break
        h.update(chunk);size+=len(chunk)
    return h.hexdigest(),size

def identity(path):
    with path.open('rb') as f:return hash_stream(f)

def checked_name(name):
    p=PurePosixPath(name)
    if not name or '\\'in name or '\x00'in name or p.is_absolute()or ':'in p.parts[0]or any(q in ('','..','.')for q in name.split('/')):
        raise ValueError(f'Unsafe archive member: {name!r}')
    return p

def destination(base,name):
    p=checked_name(name);target=base.joinpath(*p.parts)
    if not target.resolve().is_relative_to(base):raise ValueError(f'Archive path escapes output: {name}')
    current=target
    while current!=base:
        if current.is_symlink():raise ValueError(f'Symlink in output path: {name}')
        current=current.parent
    return target

def matches(path,item):
    return path.is_file()and identity(path)==(item['sha256'],item['bytes'])

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--verify-only',action='store_true',help='Verify parts, full ZIP and all member hashes without extracting')
    ap.add_argument('--output',type=Path,help='Scratch directory receiving archive-relative paths')
    a=ap.parse_args()
    if a.verify_only and a.output:ap.error('--verify-only and --output are mutually exclusive')
    if not a.verify_only and not a.output:ap.error('pass --verify-only or --output <scratch-directory>')
    record=json.loads((ROOT/'SUPPLEMENT_ASSETS.json').read_text())
    files=record['files'];parts=record['distribution']['parts']
    if len(parts)!=2 or [p['order']for p in parts]!=[1,2]:raise ValueError('Expected two ordered byte parts')
    for name in files:checked_name(name)
    # TemporaryFile avoids writing a large combined ZIP into the repository.
    with tempfile.TemporaryFile()as archive:
        full_hash=hashlib.sha256();total=0
        for part in parts:
            rel=checked_name(part['path']);path=ROOT.joinpath(*rel.parts).resolve()
            if not path.is_relative_to(ROOT):raise ValueError('Part escapes package')
            actual=identity(path)
            if actual!=(part['sha256'],part['bytes'])or actual[1]>=30000000:raise ValueError(f'Part identity/size mismatch: {part["path"]}')
            with path.open('rb')as source:
                while True:
                    chunk=source.read(BLOCK)
                    if not chunk:break
                    archive.write(chunk);full_hash.update(chunk);total+=len(chunk)
        if total!=record['bytes']or full_hash.hexdigest()!=record['sha256']:raise ValueError('Combined archive identity mismatch')
        archive.seek(0)
        with zipfile.ZipFile(archive)as z:
            entries=z.infolist();names=[i.filename for i in entries]
            if len(names)!=len(set(names))or set(names)!=set(files):raise ValueError('Archive members differ from the exact file manifest')
            # Inspect all paths/types and verify all decompressed contents before any output write.
            for info in entries:
                checked_name(info.filename);mode=(info.external_attr>>16)&0o170000
                if info.is_dir()or mode not in (0,stat.S_IFREG)or info.flag_bits&1:raise ValueError(f'Unsupported archive type/encryption: {info.filename}')
                item=files[info.filename]
                if info.file_size!=item['bytes']:raise ValueError(f'Uncompressed size mismatch: {info.filename}')
                with z.open(info)as source:actual=hash_stream(source)
                if actual!=(item['sha256'],item['bytes']):raise ValueError(f'Member identity mismatch: {info.filename}')
            written=reused=0
            if a.output:
                supplied=a.output.expanduser().absolute()
                if supplied.is_symlink():raise ValueError('Output root must not be a symlink')
                base=supplied.resolve()
                if base.exists()and not base.is_dir():raise ValueError('Output root is not a directory')
                targets={name:destination(base,name)for name in files}
                # A conflict anywhere aborts before extraction creates any file.
                for name,target in targets.items():
                    if target.exists()and not matches(target,files[name]):raise ValueError(f'Refusing to overwrite nonmatching existing file: {target}')
                    for parent in target.parents:
                        if parent==base:break
                        if parent.exists()and not parent.is_dir():raise ValueError(f'Output parent is not a directory: {parent}')
                base.mkdir(parents=True,exist_ok=True)
                for name,target in targets.items():
                    target=destination(base,name)
                    if target.exists():reused+=1;continue
                    target.parent.mkdir(parents=True,exist_ok=True)
                    # Same-directory temporary + exclusive hard-link commit never replaces a destination.
                    temp_name=None
                    try:
                        with tempfile.NamedTemporaryFile(dir=target.parent,prefix='.acr1-restore-',delete=False)as tmp:
                            temp_name=Path(tmp.name)
                            with z.open(name)as source:
                                while True:
                                    chunk=source.read(BLOCK)
                                    if not chunk:break
                                    tmp.write(chunk)
                        if not matches(temp_name,files[name]):raise ValueError(f'Extracted member changed: {name}')
                        destination(base,name) # recheck containment/symlinks before exclusive commit
                        try:os.link(temp_name,target);written+=1
                        except FileExistsError:
                            if matches(target,files[name]):reused+=1
                            else:raise ValueError(f'Destination appeared with nonmatching content: {target}')
                    finally:
                        if temp_name is not None:temp_name.unlink(missing_ok=True)
                for name,target in targets.items():
                    if not matches(target,files[name]):raise ValueError(f'Final destination identity mismatch: {name}')
    print(json.dumps({'status':'PASS','parts_verified':2,'archive_bytes':total,'archive_sha256':record['sha256'],'member_identities_verified':len(files),'files_written':written,'matching_files_retained':reused,'mode':'verify_only'if a.verify_only else'restored'},indent=2))

if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError,zipfile.BadZipFile)as e:raise SystemExit(f'FAIL: {e}')
