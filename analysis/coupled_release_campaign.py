"""P113-S7: carry retained-host errors through a bounded two-release campaign."""
from __future__ import annotations

import argparse
import hashlib
import io
import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root

import campaign_allocation as ca
import manifest_timing as mt
import operational_uncertainty as ou
import terminal_timing as tt

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / 'analysis/results/coupled_release_campaign.json'
DOC = ROOT / 'docs/COUPLED_RELEASE_CAMPAIGN.md'
FIGURE = ROOT / 'figures/coupled_release_campaign.svg'
SCREENS = ('fixed_1', 'spring_screen', 'bolley_screen')
POLICIES = ('REPLAY', 'EXACT_NAV_REPLAN')
DELAYS = (0, 120)
WIDTHS = (0.1, 0.1, 0.0001, 0.0001, 0.0005, math.radians(0.005))
SCALES = (1, 2, 5)
M = tt.INPUTS['payload_kg']
T = tt.INPUTS['terminal_time_s']
VE = tt.INPUTS['isp_s'] * tt.G0
RESERVE = tt.INPUTS['reserve_kg']


def coast(y, dt, tight=False):
    y = ca.state_check(y)
    if not math.isfinite(dt) or dt < 0:
        raise ValueError('INVALID_COAST_TIME')
    if not dt:
        return y.copy()
    if ca.elements(y)['perigee_m'] < ca.RE + 120000:
        raise ValueError('HOST_PERIGEE_GUARD')
    def rhs(_, z):
        return np.r_[z[2:], -ca.MU*z[:2]/np.linalg.norm(z[:2])**3]
    sol = solve_ivp(rhs, (0, dt), y, method='DOP853',
                    rtol=2e-13 if tight else 1e-11,
                    atol=[1e-7, 1e-7, 1e-10, 1e-10] if tight else [1e-5, 1e-5, 1e-8, 1e-8])
    if not sol.success:
        raise ValueError('PROPAGATION_FAILED')
    return ca.state_check(sol.y[:, -1])


def invariant_drift(a, b):
    ea, eb = ca.elements(a), ca.elements(b)
    return {k: abs(eb[k]-ea[k])/abs(ea[k]) for k in ('energy', 'angular_momentum')}


def burn(state, mass, fuel, dv, reserve=RESERVE):
    y = ca.state_check(state).copy()
    dv = np.asarray(dv, dtype=float)
    if dv.shape != (2,) or not np.all(np.isfinite(dv)):
        raise ValueError('INVALID_BURN')
    if not all(math.isfinite(x) for x in (mass, fuel, reserve)) or not 0 <= reserve <= fuel < mass:
        raise ValueError('INVALID_MASS_OR_RESERVE')
    norm = float(np.linalg.norm(dv))
    after = mass*math.exp(-norm/VE)
    used = mass-after
    if fuel-used < reserve:
        raise ValueError('PROPELLANT_RESERVE')
    y[2:] += dv
    return y, after, fuel-used, {'delta_v_m_s': dv.tolist(), 'magnitude_m_s': norm,
            'mass_before_kg': mass, 'mass_after_kg': after, 'fuel_used_kg': used,
            'fuel_remaining_kg': fuel-used}


def split(state, mass, command, speed_error, angle_error):
    y = ca.state_check(state)
    u0 = np.asarray(command, dtype=float)
    if (u0.shape != (2,) or not np.all(np.isfinite(u0)) or not math.isfinite(mass)
            or mass <= M or not math.isfinite(speed_error) or not math.isfinite(angle_error)):
        raise ValueError('INVALID_SEPARATION')
    speed = float(np.linalg.norm(u0))
    if speed <= 0 or speed+speed_error <= 0:
        raise ValueError('NONPOSITIVE_RELEASE_SPEED')
    u = ou.rotate(u0/speed*(speed+speed_error), angle_error)
    host = np.r_[y[:2], y[2:]-M/mass*u]
    payload = np.r_[y[:2], y[2:]+(mass-M)/mass*u]
    residual = M*payload[2:]+(mass-M)*host[2:]-mass*y[2:]
    return payload, host, {'relative_velocity_m_s': u.tolist(),
        'momentum_residual_kg_m_s': float(np.linalg.norm(residual)),
        'relative_velocity_residual_m_s': float(np.linalg.norm(payload[2:]-host[2:]-u)),
        'ideal_payload_relative_energy_J': 0.5*M*float(np.dot(u, u)),
        'retained_mass_kg': mass-M}


def samples():
    yield {'family': 'zero', 'scale': 0, 'signs': [], 'errors': [0.]*8}
    for scale in SCALES:
        for signs in itertools.product((-1, 1), repeat=6):
            e = (np.asarray(WIDTHS)*scale*signs).tolist()
            yield {'family': 'shared_calibration', 'scale': scale, 'signs': list(signs),
                   'errors': e+e[4:6]}
    for signs in itertools.product((-1, 1), repeat=4):
        e = [0.]*4+[WIDTHS[4]*signs[0], WIDTHS[5]*signs[1],
                    WIDTHS[4]*signs[2], WIDTHS[5]*signs[3]]
        yield {'family': 'independent_release_only', 'scale': 1, 'signs': list(signs), 'errors': e}


def plans():
    data = ou.load_s4()
    result = []
    for screen in SCREENS:
        row = next(r for r in data['cases'] if r['screen'] == screen
                   and r['order'] == ['phase_5km', 'phase_25km']
                   and r['release_times_s'] == [1200, 3000])
        if not row['accepted'] or row['best_candidate_index'] is None:
            raise ValueError('MISSING_S4_REFERENCE')
        candidate = row['candidates'][row['best_candidate_index']]
        first, second = candidate['events']
        for delay in DELAYS:
            start = coast(first['separation']['host_state'], delay)
            duration = second['time_s']-first['time_s']-delay
            if not delay:
                arc = row['second_transfers'][candidate['second_transfer_index']]['arcs'][candidate['second_arc_index']]
                searches = []
            else:
                solution = mt.shoot(start, tt.target_state(second['target'], second['time_s'])[:2], duration)
                searches = solution['searches']
                if not solution['arcs']:
                    raise ValueError('DELAYED_NOMINAL_SEARCH_FAILED')
                arc = min(solution['arcs'], key=lambda a: np.linalg.norm(a['correction_m_s']))
            departure, mass, fuel, _ = burn(start, first['separation']['retained_mass_kg'],
                                           first['fuel_remaining_kg'], arc['correction_m_s'])
            arrival = coast(departure, duration)
            nominal_sep = tt.separate(arrival, tt.target_state(second['target'], second['time_s'])[2:],
                                      mass, fuel-RESERVE, tt.INPUTS['screens'][screen])
            result.append({'screen': screen, 'delay_s': delay, 'first': first, 'second': second,
                's4_total_fuel_kg': candidate['total_fuel_kg'], 'second_duration_s': duration,
                'second_transfer_command_m_s': arc['correction_m_s'],
                'nominal_departure_state': departure.tolist(), 'nominal_arrival_state': arrival.tolist(),
                'second_pre_release_command_m_s': nominal_sep['second_correction_m_s'],
                'second_release_command_m_s': nominal_sep['relative_velocity_m_s'],
                'nominal_searches': searches})
    return result


def replan(state, plan, tight=False):
    target = tt.target_state(plan['second']['target'], plan['second']['time_s'])[:2]
    def residual(v):
        return coast(np.r_[state[:2], v], plan['second_duration_s'], tight)[:2]-target
    guess = np.asarray(plan['nominal_departure_state'])[2:]
    sol = root(residual, guess, method='hybr', tol=1e-11)
    error = float(np.linalg.norm(residual(sol.x)))
    correction = sol.x-state[2:]
    diagnostic = {'solver_success': bool(sol.success), 'position_residual_m': error,
                  'evaluations': int(sol.nfev), 'message': str(sol.message)}
    if not sol.success or error > 0.001:
        return None, diagnostic, 'SEARCH_FAILED'
    if np.linalg.norm(correction) > 100:
        return None, diagnostic, 'TRANSFER_BURN_CEILING'
    return correction, diagnostic, None


def run(plan, policy, sample, tight=False):
    if policy not in POLICIES:
        raise ValueError('UNKNOWN_POLICY')
    e = np.asarray(sample['errors'], dtype=float)
    if e.shape != (8,) or not np.all(np.isfinite(e)):
        raise ValueError('EIGHT_FINITE_ERRORS_REQUIRED')
    out = {'screen': plan['screen'], 'delay_s': plan['delay_s'], 'policy': policy,
           **sample, 'completed': False, 'accepted': False, 'stop': None,
           'events': [], 'burns': [], 'coasts': []}
    first, second = plan['first'], plan['second']
    sep = first['separation']
    mass = float(sep['mass_after_second_kg'])
    if abs(mass-sep['retained_mass_kg']-M) > 1e-9:
        raise ValueError('CORRUPT_S4_MASS')
    nominal_payload = np.asarray(sep['payload_state'])
    nominal_host = np.asarray(sep['host_state'])
    if np.linalg.norm(nominal_payload[2:]-nominal_host[2:]-sep['relative_velocity_m_s']) > 1e-9:
        raise ValueError('CORRUPT_S4_RELATIVE_VELOCITY')
    radial, tangent = ou.basis(nominal_payload[:2])
    com = (M*nominal_payload[2:]+(mass-M)*nominal_host[2:])/mass
    y = np.r_[nominal_payload[:2]+e[0]*radial+e[1]*tangent,
              com+e[2]*radial+e[3]*tangent]
    fuel = first['fuel_remaining_kg']
    out['burns'] = [dict(kind='initial_transfer', time_s=0, **first['transfer_burn']),
        dict(kind='first_pre_release', time_s=first['time_s'],
             delta_v_m_s=sep['second_correction_m_s'], magnitude_m_s=sep['second_burn_magnitude_m_s'],
             mass_before_kg=sep['mass_before_second_kg'], mass_after_kg=mass,
             fuel_used_kg=sep['second_fuel_kg'], fuel_remaining_kg=fuel)]

    def propagate(z, dt, label):
        end = coast(z, dt, tight)
        out['coasts'].append({'segment': label, 'duration_s': dt,
                             'relative_invariant_drift': invariant_drift(z, end)})
        return end

    def record_payload(z, time, target, details, host):
        end = propagate(z, T-time, 'payload_'+str(len(out['events'])+1))
        out['events'].append({'time_s': time, 'target': target,
            'payload_state': z.tolist(), 'host_state': host.tolist(),
            'terminal_state': end.tolist(),
            **tt.terminal_errors(end, tt.target_state(target, T)), **details})

    try:
        p, host, details = split(y, mass, sep['relative_velocity_m_s'], e[4], e[5])
        record_payload(p, first['time_s'], first['target'], details, host)
        mass -= M
        state = propagate(host, plan['delay_s'], 'host_delay')
        out['transfer_start_state'] = state.tolist()
        if policy == 'REPLAY':
            correction = plan['second_transfer_command_m_s']
        else:
            correction, diagnostic, failure = replan(state, plan, tight)
            out['search'] = diagnostic
            if failure:
                out['stop'] = failure
                return finalize(out, mass, fuel)
        state, mass, fuel, b = burn(state, mass, fuel, correction)
        out['burns'].append(dict(kind='second_transfer', time_s=first['time_s']+plan['delay_s'], **b))
        state = propagate(state, plan['second_duration_s'], 'host_transfer')
        out['second_arrival_state'] = state.tolist()
        if policy == 'REPLAY':
            correction = plan['second_pre_release_command_m_s']
            command = plan['second_release_command_m_s']
        else:
            command_event = tt.separate(state, tt.target_state(second['target'], second['time_s'])[2:],
                mass, fuel-RESERVE, tt.INPUTS['screens'][plan['screen']])
            correction = command_event['second_correction_m_s']
            command = command_event['relative_velocity_m_s']
        state, mass, fuel, b = burn(state, mass, fuel, correction)
        out['burns'].append(dict(kind='second_pre_release', time_s=second['time_s'], **b))
        p, host, details = split(state, mass, command, e[6], e[7])
        record_payload(p, second['time_s'], second['target'], details, host)
        mass -= M
        out['completed'] = True
        out['accepted'] = all(ev['accepted'] for ev in out['events'])
        out['stop'] = None if out['accepted'] else 'TERMINAL_STATE_MISS'
    except ValueError as exc:
        out['stop'] = str(exc)
    return finalize(out, mass, fuel)


def finalize(out, mass, fuel):
    used = tt.INPUTS['fuel_kg']-fuel
    out.update(fuel_used_kg=used, fuel_remaining_kg=fuel, reserve_margin_kg=fuel-RESERVE,
               retained_mass_kg=mass, delivered=len(out['events']),
               total_host_delta_v_m_s=sum(b['magnitude_m_s'] for b in out['burns']),
               ideal_payload_relative_energy_J=sum(e['ideal_payload_relative_energy_J'] for e in out['events']),
               mass_bookkeeping_residual_kg=abs(mass-(tt.INPUTS['dry_mass_kg']+fuel+(2-len(out['events']))*M)))
    return out


def rk4(state, duration, max_step):
    """Independent fixed-step Cartesian two-body integrator for verification only."""
    z = np.array(state, dtype=float)
    steps = max(1, math.ceil(duration/max_step))
    h = duration/steps
    def f(a):
        x, y, vx, vy = a
        q = -ca.MU/(x*x+y*y)**1.5
        return np.array([vx, vy, q*x, q*y])
    for _ in range(steps):
        k1 = f(z); k2 = f(z+h*k1/2); k3 = f(z+h*k2/2); k4 = f(z+h*k3)
        z += h*(k1+2*k2+2*k3+k4)/6
    return z


def difference(a, b):
    d = np.asarray(a)-np.asarray(b)
    return {'position_error_m': float(np.linalg.norm(d[:2])),
            'velocity_error_m_s': float(np.linalg.norm(d[2:]))}


def verify(ps, cases):
    checks = {}
    zeros = [r for r in cases if r['family'] == 'zero' and not r['delay_s'] and r['policy'] == 'REPLAY']
    nominal = []
    for r in zeros:
        p = next(p for p in ps if p['screen'] == r['screen'] and not p['delay_s'])
        errors = [difference(ev['terminal_state'], ref['terminal_state'])
                  for ev, ref in zip(r['events'], (p['first'], p['second']))]
        nominal.append({'screen': r['screen'], 'errors': errors,
                        'fuel_difference_kg': abs(r['fuel_used_kg']-p['s4_total_fuel_kg'])})
    checks['s4_zero_reproduction'] = len(zeros) == 3 and all(len(r['errors']) == 2 and
        all(e['position_error_m'] <= .001 and e['velocity_error_m_s'] <= 1e-6 for e in r['errors'])
        and r['fuel_difference_kg'] <= 1e-8 for r in nominal)
    events = [ev for r in cases for ev in r['events']]
    checks['momentum'] = all(ev['momentum_residual_kg_m_s'] <= 1e-8 for ev in events)
    checks['relative_velocity'] = all(ev['relative_velocity_residual_m_s'] <= 1e-9 for ev in events)
    checks['mass_accounting'] = all(r['mass_bookkeeping_residual_kg'] <= 1e-9 for r in cases)
    checks['coast_invariants'] = all(max(c['relative_invariant_drift'].values()) <= 1e-8
                                     for r in cases for c in r['coasts'])
    checks['case_count'] = len(cases) == 2508
    checks['reserve'] = all(r['fuel_remaining_kg'] >= RESERVE for r in cases)
    independent = []
    for p in ps:
        if p['delay_s'] != 120:
            continue
        segments = [(p['first']['separation']['host_state'], 120),
                    (p['nominal_departure_state'], p['second_duration_s'])]
        for start, duration in segments:
            ref = coast(start, duration, True)
            coarse = difference(rk4(start, duration, 5), ref)
            fine = difference(rk4(start, duration, 2.5), ref)
            # Only demand monotonic reduction above the declared fine-band floors.
            converged = all(fine[k] <= coarse[k] or coarse[k] <= floor
                            for k, floor in [('position_error_m', 1e-5), ('velocity_error_m_s', 1e-8)])
            independent.append({'screen': p['screen'], 'duration_s': duration, 'coarse': coarse,
                                'fine': fine, 'converged': converged})
    checks['independent_rk4'] = all(r['fine']['position_error_m'] <= .01 and
        r['fine']['velocity_error_m_s'] <= 1e-5 and r['converged'] for r in independent)
    refinements = []
    for p in ps:
        for policy in POLICIES:
            for sample in [next(samples()), next(s for s in samples() if s['scale'] == 5 and all(x == 1 for x in s['signs']))]:
                normal = next(r for r in cases if r['screen'] == p['screen'] and r['delay_s'] == p['delay_s']
                    and r['policy'] == policy and all(r[k] == sample[k] for k in ('family', 'scale', 'signs')))
                tight = run(p, policy, sample, True)
                diffs = [difference(a['terminal_state'], b['terminal_state'])
                         for a, b in zip(normal['events'], tight['events'])]
                same = all(normal[k] == tight[k] for k in ('completed', 'accepted', 'stop', 'delivered'))
                refinements.append({'screen': p['screen'], 'delay_s': p['delay_s'], 'policy': policy,
                    'family': sample['family'], 'same_outcome': same, 'errors': diffs,
                    'fuel_difference_kg': abs(normal['fuel_used_kg']-tight['fuel_used_kg'])})
    checks['adaptive_refinement'] = all(r['same_outcome'] and r['fuel_difference_kg'] <= 1e-6 and
        all(d['position_error_m'] <= .01 and d['velocity_error_m_s'] <= 1e-5 for d in r['errors']) for r in refinements)
    circular = tt.initial(); duration = 1700.
    angle = math.sqrt(ca.MU/circular[0]**3)*duration
    exact = np.r_[ou.rotate(circular[:2], angle), ou.rotate(circular[2:], angle)]
    circ = difference(coast(circular, duration), exact)
    checks['circular_limit'] = circ['position_error_m'] <= .001 and circ['velocity_error_m_s'] <= 1e-6
    checks['zero_duration'] = bool(np.array_equal(coast(circular, 0), circular))
    p = ps[0]
    probe = {'family': 'coupling_probe', 'scale': 1, 'signs': [], 'errors': [0., 0., 0., 0., .1, 0., 0., 0.]}
    perturbed = run(p, 'REPLAY', probe)
    nominal_probe = run(p, 'REPLAY', next(samples()))
    response = difference(perturbed['second_arrival_state'], nominal_probe['second_arrival_state'])
    checks['first_error_reaches_second'] = response['position_error_m'] > .001
    return {'checks': checks, 'passed': all(checks.values()), 's4_reproduction': nominal,
            'independent_rk4': independent, 'adaptive_refinement': refinements,
            'circular_error': circ, 'first_error_second_arrival_response': response}


def summaries(cases):
    groups = {}
    for r in cases:
        key = (r['screen'], r['delay_s'], r['policy'], r['family'], r['scale'])
        groups.setdefault(key, []).append(r)
    out = []
    for key, rows in groups.items():
        out.append(dict(zip(('screen', 'delay_s', 'policy', 'family', 'scale'), key),
            attempted=len(rows), completed=sum(r['completed'] for r in rows),
            accepted=sum(r['accepted'] for r in rows),
            stops={stop: sum(r['stop'] == stop for r in rows) for stop in sorted({r['stop'] for r in rows if r['stop']})},
            second_position_error_m=max((r['events'][1]['position_error_m'] for r in rows if len(r['events']) == 2), default=None),
            second_velocity_error_m_s=max((r['events'][1]['velocity_error_m_s'] for r in rows if len(r['events']) == 2), default=None),
            max_fuel_used_kg=max(r['fuel_used_kg'] for r in rows),
            min_reserve_margin_kg=min(r['reserve_margin_kg'] for r in rows)))
    return out


def build():
    ps = plans()
    cases = []
    for p in ps:
        for policy in POLICIES:
            cases.extend(run(p, policy, s) for s in samples())
            print(f"S7 computed {p['screen']} delay={p['delay_s']} {policy}", flush=True)
    paths = ['analysis/coupled_release_campaign.py', 'analysis/results/manifest_timing.json',
             'analysis/manifest_timing.py', 'analysis/terminal_timing.py', 'analysis/campaign_allocation.py',
             'analysis/operational_uncertainty.py', 'analysis/host_reference.py',
             'validation/P113_S7_coupled_release_campaign.md']
    return {'study': 'P113-S7', 'status': 'BOUNDED_COUPLED_TWO_RELEASE_SCREEN',
            'open_items': ['P113', 'E5', 'P92'],
            'inputs': {'screens': list(SCREENS), 'policies': list(POLICIES), 'delays_s': list(DELAYS),
                'shared_half_widths': list(WIDTHS), 'scales': list(SCALES), 'reserve_kg': RESERVE,
                'navigation': 'exact state, no latency, ideal impulses', 'terminal_bands': [10., .01]},
            'source_sha256': {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},
            'plans': ps, 'cases': cases, 'summaries': summaries(cases), 'verification': verify(ps, cases)}


def report(d):
    lines = ['# Coupled release errors and navigation policy', '',
        'Generated by `analysis/coupled_release_campaign.py`. Do not hand-edit.', '',
        '**P113, E5 and P92 remain open. This is the first bounded N1 increment, not an operational campaign or hardware ranking.**', '',
        'Unlike S6, the actual retained-host state after the first release is carried through the coast, next transfer and second release. Both payloads must meet the existing 10 m and 0.01 m/s bands at 3600 s.', '',
        f"**{len(d['cases'])} attempted histories. Numerical verification: {'PASS' if d['verification']['passed'] else 'FAIL'}.** Every mission and search failure is retained in JSON.", '',
        '![Second-payload error comparison](../figures/coupled_release_campaign.svg)', '',
        '## Shared calibration bias: complete-campaign acceptance', '',
        '| Screen | Coast delay (s) | Policy | Box scale | Both delivered within bands | Worst second position error (m) | Worst second velocity error (m/s) | Max fuel used (kg) |',
        '|---|---:|---|---:|---:|---:|---:|---:|']
    for r in d['summaries']:
        if r['family'] != 'shared_calibration': continue
        fmt = lambda v: 'no second delivery' if v is None else f'{v:.6f}'
        lines.append(f"| {r['screen']} | {r['delay_s']} | {r['policy']} | {r['scale']} | {r['accepted']}/{r['attempted']} | {fmt(r['second_position_error_m'])} | {fmt(r['second_velocity_error_m_s'])} | {r['max_fuel_used_kg']:.6f} |")
    nominal = [r for r in d['summaries'] if r['family'] == 'zero' and r['policy'] == 'REPLAY']
    lines += ['', '## What changed when a coast was charged', '',
        '| Screen | Nominal fuel, no delay (kg) | Nominal fuel, 120 s delay (kg) | Added fuel (kg) |',
        '|---|---:|---:|---:|']
    for screen in SCREENS:
        a = next(r['max_fuel_used_kg'] for r in nominal if r['screen'] == screen and r['delay_s'] == 0)
        b = next(r['max_fuel_used_kg'] for r in nominal if r['screen'] == screen and r['delay_s'] == 120)
        lines.append(f'| {screen} | {a:.6f} | {b:.6f} | {b-a:.6f} |')
    lines += ['', 'Replanning reduces second-payload error in these sampled cases but cannot correct an already released first payload. Complete-campaign acceptance therefore does not follow from the improved second event alone. Retained local search failures also prevent a universal claim that replanning succeeds.', '',
        '## Independent release-only corners', '',
        '| Screen | Delay (s) | Policy | Complete accepted histories |', '|---|---:|---|---:|']
    for r in d['summaries']:
        if r['family'] == 'independent_release_only':
            lines.append(f"| {r['screen']} | {r['delay_s']} | {r['policy']} | {r['accepted']}/{r['attempted']} |")
    lines += ['', '## What the policies mean', '',
        'REPLAY applies the nominal inertial transfer, pre-release correction and release vector to the evolving actual host. EXACT_NAV_REPLAN observes the host exactly at transfer start and second release, re-solves the transfer and commands the pre-release correction using that state. It cannot repair the first payload after separation. Both policies retain the same release calibration bias.', '',
        'Common state errors are inserted once before the first release, in its nominal radial/tangential frame. The shared family uses 0.1 m per position axis, 0.0001 m/s per velocity axis, 0.0005 m/s speed bias and 0.005 degrees direction bias, scaled together. A separate 16-corner release-only family varies the two releases independently. Neither family is a covariance model or success probability.', '',
        'All three authority screens share targets, order and release times (1200/3000 s). Their first commands are frozen at the best S4 candidate for that schedule. The 120 s variant re-solves the nominal second transfer after a coast; it does not simply delay an unchanged command. The wider bolley_screen is an assumed authority interval, not demonstrated BOLLEY or current-cell performance.', '',
        '## Verification', '', '| Check | Result |', '|---|---|']
    for k, v in sorted(d['verification']['checks'].items()): lines.append(f"| {k} | {'PASS' if v else 'FAIL'} |")
    lines += ['', 'Independent fixed-step RK4, analytic circular motion, zero-error S4 reproduction, tighter adaptive reruns, momentum/relative-velocity/mass conservation and coast-only invariant checks are recorded in JSON. Local root failures remain failed searches, not proofs of an impossible mission.', '',
        '## Resource and safety boundary', '',
        'Each actual impulse is charged against the changing host mass with a protected 2 kg reserve. The output records burn and coast histories, fuel, delta-v and ideal payload-relative release kinetic energy. That energy is not actuator input, charger power or thermal loss. The protected reserve is not a calculated disposal solution.', '',
        'The 120 s coast is a scheduling assumption. It does not demonstrate plume clearance, collision avoidance, attitude settling or a minimum safe delay. Pre-release impulses are still instantaneous. No host control authority, sensor covariance, finite-burn error, installed-system advantage or hardware tolerance has been established.', '',
        '## Next gate', '',
        'Add realistic navigation/update error and finite attitude/burn/clearance/resource models before extending to four/twelve payloads and replenishment. Keep cislunar C0–C2 carrier/release requirements separate before freezing N2 dimensions. A useful control benchmark does not close N1.', '',
        '[Frozen criteria](../validation/P113_S7_coupled_release_campaign.md) · [Full histories](../analysis/results/coupled_release_campaign.json) · [Programme restart](RESTART_20260917.md)', '',
        'Reproduce: `python analysis/coupled_release_campaign.py --check`.', '']
    return '\n'.join(lines)


def figure(d):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    with plt.rc_context({'svg.hashsalt': 'P113-S7', 'font.family': 'DejaVu Sans'}):
        fig, axes = plt.subplots(1, 3, figsize=(12, 4.5), sharey=True)
        for ax, screen in zip(axes, SCREENS):
            for policy, color in zip(POLICIES, ('#ad6547', '#007d88')):
                for delay, style in zip(DELAYS, ('-', '--')):
                    rs = [r for r in d['summaries'] if r['screen'] == screen and r['policy'] == policy
                          and r['delay_s'] == delay and r['family'] == 'shared_calibration']
                    ax.plot([r['scale'] for r in rs], [r['second_position_error_m'] for r in rs],
                            style, marker='o', color=color, label=f'{policy}, {delay} s')
            ax.axhline(10, color='#777777', linewidth=.9, linestyle=':')
            ax.set_title(screen.replace('_', ' ')); ax.set_xlabel('Shared error-box multiplier')
            ax.set_xticks(SCALES); ax.grid(alpha=.2); ax.spines[['top', 'right']].set_visible(False)
        axes[0].set_ylabel('Worst sampled second-payload position error (m)')
        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc='lower center', ncol=2, fontsize=8, bbox_to_anchor=(.5,.04))
        fig.suptitle('First-release errors carried into the second delivery | P113-S7')
        fig.text(.5, .012, 'Exact navigation is an optimistic benchmark. Second-payload error alone is not full-campaign success.', ha='center', fontsize=8)
        fig.tight_layout(rect=[0,.17,1,.92])
        stream = io.StringIO(); fig.savefig(stream, format='svg', metadata={'Date': None}); plt.close(fig)
        return '\n'.join(line.rstrip() for line in stream.getvalue().splitlines())+'\n'


def numerical_match(a, b, path=()):
    if type(a) is not type(b): return False
    if isinstance(b, dict):
        return a.keys() == b.keys() and all(numerical_match(a[k], v, path+(k,)) for k, v in b.items())
    if isinstance(b, list):
        return len(a) == len(b) and all(numerical_match(x,y,path+(i,)) for i,(x,y) in enumerate(zip(a,b)))
    if isinstance(b, float):
        floor = 1e-9
        leaf = str(path[-1]) if path else ''
        if leaf.endswith('_kg'): floor = 1e-8
        if leaf in ('position_error_m', 'second_position_error_m', 'position_residual_m'): floor = 1e-4
        if leaf in ('velocity_error_m_s', 'second_velocity_error_m_s', 'magnitude_m_s', 'total_host_delta_v_m_s'): floor = 1e-7
        if len(path) >= 2 and isinstance(path[-1], int):
            field, index = path[-2:]
            if 'state' in str(field): floor = 1e-4 if index < 2 else 1e-7
            elif str(field).endswith('_m_s'): floor = 1e-7
        return math.isfinite(a) and math.isfinite(b) and math.isclose(a,b,rel_tol=1e-10,abs_tol=floor)
    return a == b


def check_outputs(stored, fresh):
    for key in ('study', 'status', 'open_items', 'inputs', 'source_sha256'):
        if stored.get(key) != fresh[key]: return False
    if stored.keys() != fresh.keys() or len(stored['cases']) != len(fresh['cases']): return False
    for a,b in zip(stored['cases'],fresh['cases']):
        if any(a[k] != b[k] for k in ('screen','delay_s','policy','family','scale','signs','errors','accepted','completed','stop')):
            return False
    # Root iteration counts are diagnostics, not physical results; keep success,
    # residuals and outcomes checked while allowing solver iteration roundoff.
    def normalized(d):
        if isinstance(d, dict): return {k: normalized(v) for k,v in d.items() if k not in ('evaluations','message')}
        if isinstance(d, list): return [normalized(v) for v in d]
        return d
    return numerical_match(normalized(stored),normalized(fresh))


def main():
    p = argparse.ArgumentParser(); p.add_argument('--check', action='store_true'); args = p.parse_args()
    d = build()
    if args.check:
        stored = json.loads(RESULT.read_text())
        stale = []
        if not check_outputs(stored,d): stale.append('numerical payload')
        if DOC.read_text() != report(stored): stale.append('report')
        if FIGURE.read_text() != figure(stored): stale.append('figure')
        if stale:
            raise SystemExit('P113-S7 outputs stale: '+', '.join(stale))
    else:
        RESULT.write_text(json.dumps(d,indent=2,sort_keys=True,allow_nan=False)+'\n')
        DOC.write_text(report(d)); FIGURE.write_text(figure(d))
    if not d['verification']['passed']:
        raise SystemExit('P113-S7 verification failed; retain results and diagnose')
    print('P113-S7: 2508 coupled histories; verification PASS; N1/P113/E5/P92 remain open')


if __name__ == '__main__': main()
