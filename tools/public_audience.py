"""Check public text and source containers for private workflow material."""
from __future__ import annotations
import re
import shutil
import subprocess
from pathlib import Path
from zipfile import ZipFile, BadZipFile

REVIEW_TEXT={'.md','.txt','.html','.htm','.tex','.json','.xml','.csv','.svg','.vtt','.cff','.rels'}
ARCHIVES={'.zip','.docx','.pptx'}
MONTH=r'(?:January|February|March|April|May|June|July|August|September|October|November|December)'
DAY=r'(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)'
CHECKS=[
 (re.compile(r'https://(?:docs|drive)\.google\.com/(?:document/d|file/d|drive/folders|spreadsheets/d)/[A-Za-z0-9_-]+',re.I),'private-storage link; use an approved public source or public repository artifact'),
 (re.compile(r'\b(?:freeze|release cutoff|final-year cutoff|deadline|release target)\b[^.\n]{0,100}(?:\b'+DAY+r'\b|\b\d{1,2}\s+'+MONTH+r'\b)',re.I),'personal schedule'),
 (re.compile(r'\b(?:private\s+(?:work\s+index|task\s+tracker)|weekly\s+usage|doomscroll(?:ing)?)\b',re.I),'internal project or conversation material'),
 (re.compile(r'\b(?:simulated|hypothetical)\s+(?:college\s+)?(?:panel|judge|reviewer)\s+(?:read|score|rating)',re.I),'private reviewer rehearsal'),
 (re.compile(r'\b(?:send|sent|email)\b[^.\n]{0,60}\b(?:professor|project guide|coauthor)\b',re.I),'private correspondence'),
 (re.compile(r'\b(?:grading target|grade target|hypothetical score)\b',re.I),'private grading target'),
]

def inspect_text(text: str,label: str)->list[str]:
 raw_links=[f'{label}: private-storage link in source or attributes'] if CHECKS[0][0].search(text) else []
 # Rendered text makes markup boundaries visible without joining separate paragraphs.
 text=re.sub(r'</(?:p|div|section|h[1-6])\s*>','\n',text,flags=re.I)
 text=re.sub(r'<[^>]+>',' ',text)
 errors=list(raw_links)
 for n,line in enumerate(text.splitlines(),1):
  for pattern,reason in CHECKS:
   if pattern.search(line):errors.append(f'{label}:{n}: {reason}')
 return errors

def inspect_pdf(raw:bytes,label:str)->list[str]:
 tool=shutil.which('pdftotext')
 if tool is None:return [f'{label}: install poppler-utils for mandatory PDF audience inspection']
 try:
  result=subprocess.run([tool,'-layout','-','-'],input=raw,capture_output=True,timeout=60)
 except (OSError,subprocess.TimeoutExpired):return [f'{label}: PDF text extraction failed']
 if result.returncode:return [f'{label}: PDF text extraction failed']
 errors=inspect_text(result.stdout.decode('utf-8',errors='replace'),label)
 info=shutil.which('pdfinfo')
 if info is None:return errors+[f'{label}: install poppler-utils for PDF hyperlink inspection']
 try:
  links=subprocess.run([info,'-url','-'],input=raw,capture_output=True,timeout=60)
 except (OSError,subprocess.TimeoutExpired):return errors+[f'{label}: PDF hyperlink extraction failed']
 if links.returncode:return errors+[f'{label}: PDF hyperlink extraction failed']
 return errors+inspect_text(links.stdout.decode('utf-8',errors='replace'),label+' hyperlinks')

def audit_publication(root:Path,paths:list[str])->list[str]:
 errors=[]
 for name in paths:
  p=root/name
  if not p.is_file():continue
  if p.suffix.lower() in REVIEW_TEXT:
   errors.extend(inspect_text(p.read_text(errors='replace'),name))
  elif p.suffix.lower()=='.pdf':
   errors.extend(inspect_pdf(p.read_bytes(),name))
  elif p.suffix.lower() in ARCHIVES:
   try:
    with ZipFile(p) as z:
     for info in z.infolist():
      if Path(info.filename).suffix.lower()=='.pdf':
       errors.extend(inspect_pdf(z.read(info),name+'!'+info.filename))
      if Path(info.filename).suffix.lower() in REVIEW_TEXT|{'.py','.js','.cjs'}:
       if info.file_size>10_000_000:
        errors.append(f'{name}!{info.filename}: oversized text member requires separate audience review');continue
       errors.extend(inspect_text(z.read(info).decode('utf-8',errors='replace'),name+'!'+info.filename))
   except BadZipFile:errors.append(f'{name}: invalid source/document container')
 return errors
