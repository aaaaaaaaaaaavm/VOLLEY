#!/usr/bin/env python3
"""Separate CadQuery/OCP exchange check of the supplied FM08-R3 STEP files.

Usage: python readback_step.py PATH_TO_CAD_RELEASE [--output PATH]
This checks serialization and BRep validity. It does not qualify fit or motion.
"""
from pathlib import Path
import argparse, hashlib, json, math, platform, time
import cadquery as cq
import OCP
ap=argparse.ArgumentParser();ap.add_argument('cad_release',type=Path);ap.add_argument('--expected-count',type=int,default=5);ap.add_argument('--output',type=Path,default=Path(__file__).with_name('INDEPENDENT_STEP.json'));args=ap.parse_args()
started=time.perf_counter();folder=args.cad_release
native_path=folder/'GEOMETRY_REPORT.json';native_bytes=native_path.read_bytes();native=json.loads(native_bytes)
pairs=[]
for name in ['stowed','1U_seated','3U_seated','launch','midtransfer']:
 paired=folder/('FM08_R3_four_cell_'+name+'.json');raw=paired.read_bytes();pairs.append((paired,raw,json.loads(raw)))
assert len(pairs)==args.expected_count,'Incomplete expected-state capture'
records=[]
for paired,paired_bytes,capture in pairs:
 path=folder/capture['step'];before=hashlib.sha256(path.read_bytes()).hexdigest()
 assert before==capture['sha256'][path.name],'STEP does not match its paired native capture'
 obj=cq.importers.importStep(str(path)).val();solids=obj.Solids()
 volume=sum(s.Volume() for s in solids)
 expected_volume=sum(row['volume_mm3'] for row in capture['BOM'])
 error=abs(volume-expected_volume)
 criterion=max(.01,1e-6*expected_volume)
 valid=obj.isValid() and all(s.isValid() for s in solids)
 after=hashlib.sha256(path.read_bytes()).hexdigest()
 box=obj.BoundingBox()
 record={'file':path.name,'sha256':before,'same_file_before_after':before==after,'paired_native_capture':paired.name,'paired_capture_sha256':hashlib.sha256(paired_bytes).hexdigest(),'paired_capture_unchanged':paired_bytes==paired.read_bytes(),
 'valid':bool(valid),'solids':len(solids),'native_solids':capture['step_solids'],
 'volume_mm3':volume,'native_sum_part_volume_mm3':expected_volume,'absolute_volume_difference_mm3':error,
 'relative_volume_difference':error/expected_volume,'allowed_absolute_volume_difference_mm3':criterion,
 'bounds_mm':[box.xmin,box.xmax,box.ymin,box.ymax,box.zmin,box.zmax]}
 record['pass']=bool(valid and len(solids)==capture['step_solids'] and expected_volume>0 and error<=criterion and before==after and record['paired_capture_unchanged'])
 records.append(record);print(json.dumps(record),flush=True)
 args.output.with_name('PARTIAL_READBACK.json').write_text(json.dumps(records,indent=2)+'\n')
# GEOMETRY_REPORT also receives later motion metadata; paired captures are the immutable expected records.
report={'revision':'FM08-R3-STEP-READBACK-R0','method':'Separate CadQuery/OCP import compared with native FreeCAD volume/solid-count records. Both use the OpenCASCADE kernel family; this is not independent-kernel certification or functional acceptance.',
 'software':{'Python':platform.python_version(),'CadQuery':cq.__version__,'OCP':OCP.__version__},
 'native_software':native['software'],'criteria':'BRep valid; native STEP solid count equal; sum-of-solids volume difference <=max(0.01mm3,1e-6*native volume). Numerical serialization only; motion, tolerance and loaded clearances remain separate.',
 'native_geometry_report_sha256_at_start':hashlib.sha256(native_bytes).hexdigest(),'aggregate_metadata_changed_during_check':native_bytes!=native_path.read_bytes(),'exchanges':records,
 'expected_capture_count':args.expected_count,'all_checks_pass':bool(len(records)==args.expected_count and all(r['pass'] for r in records)),'elapsed_s':time.perf_counter()-started}
args.output.write_text(json.dumps(report,indent=2)+'\n')
assert report['all_checks_pass']
print(json.dumps({'files':len(records),'result':'PASS','software':report['software'],'elapsed_s':report['elapsed_s']},indent=2))
