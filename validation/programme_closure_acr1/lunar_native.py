"""Generate/run native GMAT lunar perturbation cases; parse exact raw reports.

Use --gmat /path/to/GmatConsole --gravity /path/to/grgm900c.cof.
Default generates the source scripts; --run executes them. External runtime is
not vendored. Input identity is captured before execution.
"""
import argparse
import gzip
import hashlib
import json
import math
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def make_script(c, degree, speed, apo, gravity, output):
    mu = c['mu_moon_km3_s2']
    radius = c['reference_radius_km']
    ra, rp = radius + apo, radius + c['staging_perilune_km']
    a = (rp + ra) / 2
    v = math.sqrt(mu * (2 / ra - 1 / a))
    # Finite host split applies to a relative separation command. +u is prograde.
    v += c['retained_host_kg'] / (c['retained_host_kg'] + c['payload_kg']) * speed / 1000
    runtime_root=gravity.parents[2]
    # MJ2000Eq x-z plane, apolune at negative x. This plane is not asserted
    # to be polar relative to the lunar equator.
    return f"""% PCS-ACR1-01: independent lunar surrogate, not the LEO ACR1 mission.
SolarSystem.EphemerisSource = 'DE421';
SolarSystem.DEFilename = '{runtime_root/'planetary_ephem/de/leDE1900.421'}';
SolarSystem.EphemerisUpdateInterval = 0;
Luna.EquatorialRadius = 1737.4;
Luna.Flattening = 0;
Luna.PlanetarySpiceKernelName = {{'{runtime_root/'planetary_coeff/SPICELunaCurrentKernel.bpc'}'}};
Luna.FrameSpiceKernelName = {{'{runtime_root/'planetary_coeff/SPICELunaFrameKernel.tf'}'}};
Luna.RotationDataSource = 'SPICE';
Luna.SpiceFrameId = 'MOON_PA';
Create CoordinateSystem MoonFrame;
MoonFrame.Origin = Luna;
MoonFrame.Axes = MJ2000Eq;
Create Spacecraft Payload;
Payload.DateFormat = UTCGregorian;
Payload.Epoch = '{c['epoch_utc']}';
Payload.CoordinateSystem = MoonFrame;
Payload.DisplayStateType = Cartesian;
Payload.X = {-ra:.15g};
Payload.Y = 0;
Payload.Z = 0;
Payload.VX = 0;
Payload.VY = 0;
Payload.VZ = {-v:.15g};
Payload.DryMass = {c['payload_kg']};
Create ForceModel MoonForces;
MoonForces.CentralBody = Luna;
MoonForces.PrimaryBodies = {{Luna}};
MoonForces.PointMasses = {{Earth, Sun}};
MoonForces.Drag = None;
MoonForces.SRP = Off;
MoonForces.GravityField.Luna.Degree = {degree};
MoonForces.GravityField.Luna.Order = {degree};
MoonForces.GravityField.Luna.PotentialFile = '{gravity}';
MoonForces.RelativisticCorrection = Off;
Create Propagator MoonProp;
MoonProp.FM = MoonForces;
MoonProp.Type = PrinceDormand78;
MoonProp.InitialStepSize = 30;
MoonProp.Accuracy = 1e-12;
MoonProp.MinStep = 0.001;
MoonProp.MaxStep = 120;
MoonProp.MaxStepAttempts = 50;
MoonProp.StopIfAccuracyIsViolated = true;
Create ReportFile History;
History.Filename = '{output}';
History.WriteHeaders = true;
History.Precision = 16;
History.Add = {{Payload.ElapsedDays, Payload.Luna.RMAG, Payload.Luna.SMA, Payload.Luna.ECC}};
BeginMissionSequence;
Propagate MoonProp(Payload) {{Payload.Luna.RMAG = {radius}, Payload.ElapsedDays = {c['lifetime_days']}}};
"""


def parse_report(path, c):
    opener = gzip.open if path.suffix == '.gz' else open
    with opener(path, 'rt') as f:
        rows = []
        for line in f:
            try:
                vals = [float(x) for x in line.split()]
            except ValueError:
                continue
            if len(vals) == 4:
                rows.append(vals)
    if not rows:
        raise ValueError(f'No numeric rows: {path}')
    min_alt = min(x[1] - c['reference_radius_km'] for x in rows)
    # This is a sampled radius floor, not a guaranteed minimum between steps.
    complete = rows[-1][0] >= c['lifetime_days'] - 1e-7
    return dict(rows=len(rows), final_day=rows[-1][0],
                min_sampled_altitude_km=min_alt,
                final_sma_km=rows[-1][2], final_eccentricity=rows[-1][3],
                reaches_duration=complete,
                passes_declared_sampled_floor=complete and min_alt >= c['minimum_sampled_radius_margin_km'],
                samples_approximately_daily=[rows[min(range(len(rows)), key=lambda i:abs(rows[i][0]-d))] for d in range(c['lifetime_days']+1)])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gmat', required=True, type=Path)
    parser.add_argument('--gravity', required=True, type=Path)
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--one', action='store_true')
    args = parser.parse_args()
    c = json.loads((HERE/'study_inputs.json').read_text())['lunar']
    native = HERE/'native'; native.mkdir(exist_ok=True)
    identity = dict(generator_sha256=sha(__file__), inputs_sha256=sha(HERE/'study_inputs.json'),
                    GMAT_binary_sha256=sha(args.gmat), gravity_file_sha256=sha(args.gravity),
                    GMAT_version='R2026a; console build Mar 30 2026 10:09:27')
    runtime_root=args.gmat.parent.parent
    runtime_files=['bin/gmat_startup_file.txt','bin/libGmatBase.so.R2026a',
                   'bin/libGmatUtil.so.R2026a','data/planetary_ephem/de/leDE1900.421',
                   'data/planetary_coeff/SPICELunaCurrentKernel.bpc',
                   'data/planetary_coeff/SPICELunaFrameKernel.tf','data/time/tai-utc.dat']
    identity['supporting_runtime_sha256']={name:sha(runtime_root/name) for name in runtime_files}
    (native/'SOURCE_IDENTITY.json').write_text(json.dumps(identity, indent=2)+'\n')
    cases=[]
    for apo in c['staging_apolune_km']:
        for speed in c['release_relative_speeds_m_s']:
            for degree in c['gravity_degrees']:
                stem=f'apo{apo}_u{speed:+d}_d{degree}'
                script=native/(stem+'.script'); report=native/(stem+'.txt')
                source=make_script(c, degree, speed, apo, args.gravity, report)
                archive=report.with_suffix('.txt.gz')
                if archive.exists() and (not script.exists() or script.read_text()!=source):
                    raise RuntimeError(f'Cached report has different source: {stem}; reproduce in a separate package copy')
                script.write_text(source)
                receipt=native/(stem+'.receipt.json')
                expected=dict(script_sha256=sha(script),GMAT_binary_sha256=identity['GMAT_binary_sha256'],
                              gravity_file_sha256=identity['gravity_file_sha256'],
                              supporting_runtime_sha256=identity['supporting_runtime_sha256'])
                if archive.exists() and receipt.exists() and json.loads(receipt.read_text())!=expected:
                    raise RuntimeError(f'Cached report has different runtime: {stem}; reproduce in a separate package copy')
                if args.run and not report.with_suffix('.txt.gz').exists():
                    run=subprocess.run([str(args.gmat), '--run', str(script)], text=True,
                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    (native/(stem+'.log')).write_text(run.stdout)
                    if run.returncode or not report.exists() or 'Mission run completed' not in run.stdout:
                        raise RuntimeError(f'GMAT failure: {stem}; inspect native log')
                    with gzip.open(report.with_suffix('.txt.gz'), 'wb') as gz:
                        gz.write(report.read_bytes())
                    report.unlink()
                if archive.exists():
                    receipt.write_text(json.dumps(expected,indent=2)+'\n')
                    cases.append(dict(case=stem, apo_km=apo, relative_speed_m_s=speed, degree_order=degree,
                                      script_sha256=sha(script), report_sha256=sha(archive), **parse_report(archive,c)))
                if args.one:
                    break
            if args.one: break
        if args.one: break
    out=dict(study='PCS-LUNAR-NATIVE-01', source_identity=identity, criteria=c,
             limits=json.loads((HERE/'study_inputs.json').read_text())['limits'], cases=cases)
    (HERE/'LUNAR_NATIVE_RESULTS.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({x['case']:{k:x[k] for k in ['final_day','min_sampled_altitude_km','passes_declared_sampled_floor']} for x in cases},indent=2))


if __name__ == '__main__': main()
