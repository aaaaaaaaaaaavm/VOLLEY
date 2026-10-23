"""Generate explicitly bounded GMAT lunar coast experiments; no mission certification."""
from pathlib import Path
import json
import math

ROOT = Path(__file__).resolve().parent
GMAT = Path('/workspace/volley-work/runtime-gmat/GMAT/R2026a')
RADIUS = 1737.4
MU = 4902.79996708864  # GRGM900C header, converted from m^3/s^2 to km^3/s^2
EPOCH = '23 Oct 2026 00:00:00.000'  # TAI, a prescribed screening epoch


def deck(name, apogee_km=100, degree=20, max_step=120, days=(7, 30, 90, 180),
         gravity='grgm900c.cof', inclination=90, third_bodies=True):
    rp, ra = RADIUS + 100, RADIUS + apogee_km
    semi_major = (rp + ra) / 2
    speed = math.sqrt(MU * (2 / rp - 1 / semi_major))
    angle = math.radians(inclination)
    columns = ['Sat.ElapsedSecs', 'Sat.LunaMJ2000Eq.X', 'Sat.LunaMJ2000Eq.Y',
               'Sat.LunaMJ2000Eq.Z', 'Sat.LunaMJ2000Eq.VX', 'Sat.LunaMJ2000Eq.VY',
               'Sat.LunaMJ2000Eq.VZ', 'Sat.Luna.RMAG', 'Sat.Luna.SMA',
               'Sat.Luna.ECC', 'Sat.Luna.RadPer', 'Sat.Luna.RadApo']
    lines = [
        '% Provisional native lunar coast. Units: km, km/s, seconds, degrees.',
        '% Initial plane is specified relative to MJ2000Eq, not asserted to be lunar-polar.',
        "SolarSystem.EphemerisSource = 'DE421';",
        f"SolarSystem.DEFilename = '{GMAT / 'data/planetary_ephem/de/leDE1900.421'}';",
        'SolarSystem.EphemerisUpdateInterval = 0;',
        'Earth.NutationUpdateInterval = 0;',
        f"Earth.EopFileName = '{GMAT / 'data/planetary_coeff/eopc04_08.62-now'}';",
        'Earth.Mu = 398600.435507;',
        'Sun.Mu = 132712440017.99;',
        f'Luna.Mu = {MU:.15g};', f'Luna.EquatorialRadius = {RADIUS};', 'Luna.Flattening = 0;',
        f"Luna.PlanetarySpiceKernelName = {{'{GMAT / 'data/planetary_coeff/SPICELunaCurrentKernel.bpc'}'}};",
        f"Luna.FrameSpiceKernelName = {{'{GMAT / 'data/planetary_coeff/SPICELunaFrameKernel.tf'}'}};",
        "Luna.RotationDataSource = 'SPICE';", "Luna.SpiceFrameId = 'MOON_PA';",
        'Create CoordinateSystem LunaMJ2000Eq;', 'LunaMJ2000Eq.Origin = Luna;',
        'LunaMJ2000Eq.Axes = MJ2000Eq;',
        'Create Spacecraft Sat;', 'Sat.DateFormat = TAIGregorian;', f"Sat.Epoch = '{EPOCH}';",
        'Sat.CoordinateSystem = LunaMJ2000Eq;', 'Sat.DisplayStateType = Cartesian;',
        f'Sat.X = {rp:.16g};', 'Sat.Y = 0;', 'Sat.Z = 0;', 'Sat.VX = 0;',
        f'Sat.VY = {speed * math.cos(angle):.16g};', f'Sat.VZ = {speed * math.sin(angle):.16g};',
        'Sat.DryMass = 300;', 'Sat.SRPArea = 0;', 'Sat.DragArea = 0;',
        'Create ForceModel MoonForces;', 'MoonForces.CentralBody = Luna;',
        'MoonForces.PrimaryBodies = {Luna};',
        'MoonForces.PointMasses = {Earth, Sun};' if third_bodies else 'MoonForces.PointMasses = {};',
        'MoonForces.Drag = None;', 'MoonForces.SRP = Off;',
        'MoonForces.RelativisticCorrection = Off;', 'MoonForces.ErrorControl = RSSStep;',
        f'MoonForces.GravityField.Luna.Degree = {degree};',
        f'MoonForces.GravityField.Luna.Order = {degree};',
        f"MoonForces.GravityField.Luna.PotentialFile = '{GMAT / 'data/gravity/luna' / gravity}';",
        'MoonForces.GravityField.Luna.TideModel = None;',
        'Create Propagator Coast;', 'Coast.FM = MoonForces;', 'Coast.Type = PrinceDormand78;',
        f'Coast.InitialStepSize = {min(60, max_step)};', 'Coast.Accuracy = 1e-11;',
        'Coast.MinStep = 0.001;', f'Coast.MaxStep = {max_step};',
        'Coast.MaxStepAttempts = 50;', 'Coast.StopIfAccuracyIsViolated = true;',
        'Create ReportFile History Checkpoints Configuration;',
        f"History.Filename = '{ROOT / 'runs' / (name + '.csv')}';",
        'History.Precision = 16;', 'History.FixedWidth = false;', "History.Delimiter = ',';",
        'History.WriteHeaders = true;', 'History.Add = {' + ', '.join(columns) + '};',
        f"Checkpoints.Filename = '{ROOT / 'runs' / (name + '_checkpoints.csv')}';",
        'Checkpoints.Precision = 16;', 'Checkpoints.FixedWidth = false;',
        "Checkpoints.Delimiter = ',';", 'Checkpoints.WriteHeaders = true;',
        f"Configuration.Filename = '{ROOT / 'runs' / (name + '_configuration.script')}';",
        'BeginMissionSequence;',
        'Write SolarSystem Luna Earth Sun LunaMJ2000Eq MoonForces Coast Sat {Style = Script, MessageWindow = false, ReportFile = Configuration};',
        'Write Luna.Mu Luna.EquatorialRadius Earth.Mu Earth.EquatorialRadius Earth.Flattening Earth.NutationUpdateInterval Sun.Mu {Style = Verbose, MessageWindow = false, ReportFile = Configuration};',
    ]
    for index, day in enumerate(days):
        if index:
            lines.append(f'If Sat.ElapsedSecs >= {days[index-1] * 86400 - .01:.2f};')
        # GMAT interprets an ElapsedSecs stop as duration from this Propagate start.
        # The reported Sat.ElapsedSecs still uses the mission's initial epoch.
        duration = day - (days[index-1] if index else 0)
        lines.append(f'Propagate Coast(Sat) {{Sat.ElapsedSecs = {duration * 86400}, Sat.Luna.RMAG = {RADIUS}, StopTolerance = 1e-6}};')
        lines.append('Report Checkpoints ' + ' '.join(columns) + ';')
    lines += ['EndIf;' for _ in range(len(days)-1)]
    path = ROOT / 'decks' / (name + '.script')
    path.write_text('\n'.join(lines) + '\n')
    return {'name': name, 'deck': str(path), 'initial_periapsis_altitude_km': 100,
            'initial_apogee_altitude_km': apogee_km, 'inclination_MJ2000Eq_deg': inclination,
            'degree_order': degree, 'max_step_s': max_step, 'requested_days': list(days),
            'gravity_file': gravity, 'Earth_Sun_point_masses': third_bodies,
            'initial_state_km_km_s': [rp, 0, 0, 0, speed * math.cos(angle), speed * math.sin(angle)],
            'reference_lunar_mu_km3_s2': MU, 'reference_spherical_radius_km': RADIUS,
            'epoch_TAI_Gregorian': EPOCH, 'impact_stop_radius_km': RADIUS}


if __name__ == '__main__':
    pilot = deck('pilot_circular_d20_s120_7d', days=(7,))
    (ROOT / 'pilot-case.json').write_text(json.dumps(pilot, indent=2) + '\n')
    print(pilot['deck'])
