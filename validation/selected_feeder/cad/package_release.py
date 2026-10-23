"""Record the verified geometry payload; rendered illustrations are packaged separately."""
from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'release'
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

geometry = json.loads((OUT / 'GEOMETRY_REPORT.json').read_text())
motion = json.loads((OUT / 'MOTION_VERIFICATION.json').read_text())
parts = json.loads((OUT / 'PART_INDEX.json').read_text())
exchange = json.loads((ROOT / 'exchange/INDEPENDENT_STEP.json').read_text())
builder_hash = digest(ROOT / 'build_selected.py')
assert all(r['builder_sha256'] == builder_hash for r in [geometry, motion, parts])
assert len(geometry['captures']) == 5 and len(parts['parts']) == 9
assert all(c['parts'] == 154 and c['step_solids'] == 154 for c in geometry['captures'])
assert all(c['including_catalog_envelopes_audit']['pass'] for c in geometry['captures'])
assert all(c['pass'] for c in geometry['motion_samples'])
assert motion['case_count'] == 115 and motion['all_sampled_cases_pass']
assert exchange['all_checks_pass'] and len(exchange['exchanges']) == 5
for capture in geometry['captures']:
    for name, expected in capture['sha256'].items():
        assert digest(OUT / name) == expected, name
for capture in exchange['exchanges']:
    assert digest(OUT / capture['file']) == capture['sha256']

stowed = geometry['captures'][0]
summary = {
    'revision': geometry['revision'],
    'builder_sha256': builder_hash,
    'architecture': geometry['selected_architecture'],
    'complete_native_step_assembly_states': 5,
    'nominal_native_step_component_pairs': 9,
    'features_and_connected_solids_per_assembly': 154,
    'full_assembly_interference_audits_pass': True,
    'local_motion_cases': len(geometry['motion_samples']),
    'installed_motion_cases': motion['case_count'],
    'installed_motion_failed_cases': motion['failed_case_count'],
    'separate_step_imports_pass': True,
    'stowed_mass_properties': stowed['mass_properties'],
    'scope': 'Nominal academic kinematic design; discrete mechanism motion plus an exact rectangular payload translation corridor. Not loaded-fit, contact-load, manufacturing or flight qualification.',
    'geometry_report_sha256': digest(OUT / 'GEOMETRY_REPORT.json'),
    'motion_report_sha256': digest(OUT / 'MOTION_VERIFICATION.json'),
    'exchange_report_sha256': digest(ROOT / 'exchange/INDEPENDENT_STEP.json'),
}
(OUT / 'CAD_RELEASE_SUMMARY.json').write_text(json.dumps(summary, indent=2) + '\n')

accepted = [ROOT / p for p in ['README.md', 'build_selected.py', 'export_details.py',
            'verify_motion.py', 'package_release.py', 'build.log', 'motion.log', 'details.log']]
accepted += [ROOT / 'exchange' / p for p in ['readback_step.py', 'INDEPENDENT_STEP.json']]
accepted += [p for p in OUT.iterdir() if p.is_file() and p.suffix in ['.FCStd', '.step', '.json', '.csv']]
accepted += [p for p in (OUT / 'obj').iterdir() if p.is_file() and p.suffix in ['.obj', '.json']]
records = [{'path': str(p.relative_to(ROOT)), 'sha256': digest(p), 'bytes': p.stat().st_size}
           for p in sorted(set(accepted))]
manifest = {'revision': geometry['revision'], 'builder_sha256': builder_hash,
            'files': records, 'file_count': len(records),
            'excluded': ['private_history', '__pycache__', 'backups', 'temporary files',
                         'figures (rendered and packaged separately)']}
(ROOT / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({'files': len(records), 'manifest_sha256': digest(ROOT / 'MANIFEST.json'),
                  'summary_sha256': digest(OUT / 'CAD_RELEASE_SUMMARY.json')}, indent=2))
