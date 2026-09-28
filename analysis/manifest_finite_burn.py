"""P113-S12: finite burns and retained-host accounting across twelve releases."""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import least_squares
import finite_burn_departure as fb
import manifest_timing as mt
import terminal_timing as tt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'analysis/results/manifest_finite_burn.json'
DOC = ROOT / 'docs/MANIFEST_FINITE_BURN.md'
N, PAYLOAD, DRY, FUEL, RESERVE, END = 12, 4., 300., 10., 2., 18000.
INITIAL_MASS = DRY + FUEL + N * PAYLOAD
WIDTHS = np.array([.1, .1, .0001, .0001, .0005, math.radians(.005)])


def target(index, time):
    radius = tt.initial()[0]
    rate = math.sqrt(mt.campaign.MU / radius**3)
    angle = rate*time + 5000*index/radius
    return np.array([radius*math.cos(angle), radius*math.sin(angle),
                     -radius*rate*math.sin(angle), radius*rate*math.cos(angle)])


def schedule(x, previous_angle, axis, duration=1200.):
    a, b, d1, d2 = map(float, x)
    initial = 0. if previous_angle is None else fb.slew(previous_angle, a) + fb.SETTLE
    final = fb.slew(b, math.atan2(axis[1], axis[0])) + fb.SETTLE
    gap = duration - initial - d1 - d2 - final
    return initial, gap, final, fb.slew(a, b) + fb.SETTLE


def split(y, speed, axis, error=(0., 0.)):
    if y[4] <= PAYLOAD or speed + error[0] <= 0:
        raise ValueError('INVALID_SEPARATION')
    a = math.atan2(axis[1], axis[0]) + error[1]
    rel = (speed+error[0])*np.array([math.cos(a), math.sin(a)])
    p = np.r_[y[:2], y[2:4]+(1-PAYLOAD/y[4])*rel, PAYLOAD]
    h = y.copy()
    h[2:4] -= PAYLOAD/y[4]*rel
    h[4] -= PAYLOAD
    momentum = float(np.linalg.norm(PAYLOAD*p[2:4]+h[4]*h[2:4]-y[4]*y[2:4]))
    speed_residual = float(np.linalg.norm(p[2:4]-h[2:4]-rel))
    return p, h, momentum, speed_residual


def evaluate(y, x, index, speed, thrust, axis, previous_angle, tight=False,
             error=(0., 0.), terminal=False):
    initial, gap, final, required = schedule(x, previous_angle, axis)
    a, b, d1, d2 = map(float, x)
    z0 = fb.propagate(y, initial, tight=tight)
    z1 = fb.propagate(z0, d1, thrust, a, tight=tight)
    z2 = fb.propagate(z1, max(0., gap), tight=tight)
    z3 = fb.propagate(z2, d2, thrust, b, tight=tight)
    z4 = fb.propagate(z3, final, tight=tight)
    p, h, momentum, relative = split(z4, speed, axis, error)
    fuel = h[4]-DRY-(N-index)*PAYLOAD
    dv = [fb.VE*math.log(z0[4]/z1[4]), fb.VE*math.log(z2[4]/z3[4])]
    perigee = min(mt.campaign.elements(z[:4])['perigee_m'] for z in (y,z0,z1,z2,z3,z4))
    violations = [max(0., required-gap)/10, max(0., RESERVE-fuel)*100,
                  max(0., dv[0]-100), max(0., dv[1]-100),
                  max(0., mt.campaign.RE+120000-perigee)/100]
    desired = target(index, index*1200.)
    residual = np.r_[(p[:2]-desired[:2])/10, (p[2:4]-desired[2:])/.01, violations]
    end = fb.propagate(p, END-index*1200., tight=tight) if terminal else p
    errors = tt.terminal_errors(end[:4], target(index, END if terminal else index*1200.))
    service = all(v <= 1e-7 for v in violations)
    mass_error = abs(y[4]-h[4]-PAYLOAD-thrust*(d1+d2)/fb.VE)
    return dict(parameters=np.asarray(x).tolist(), residual=residual.tolist(),
                payload_state=p.tolist(), host_state=h.tolist(), terminal_state=end[:4].tolist(),
                errors=errors, accepted=bool(service and errors['accepted']), service_pass=service,
                fuel_remaining_kg=fuel, fuel_used_kg=float(y[4]-z4[4]),
                initial_slew_settle_s=initial, interburn_available_s=gap,
                interburn_required_s=required, final_slew_settle_s=final,
                integrated_delta_v_m_s=dv, minimum_endpoint_perigee_m=perigee,
                momentum_residual_kg_m_s=momentum, relative_speed_residual_m_s=relative,
                mass_balance_residual_kg=mass_error)


def seeds(y, index, speed, thrust):
    shot = mt.shoot(y[:4], target(index, index*1200.)[:2], 1200.)
    candidates = []
    for arc in shot['arcs']:
        dv1 = np.asarray(arc['correction_m_s'])
        m1 = y[4]*math.exp(-np.linalg.norm(dv1)/fb.VE)
        try:
            sep = tt.separate(arc['arrival_state'], target(index,index*1200.)[2:], m1,
                              m1-DRY-(N-index+1)*PAYLOAD-RESERVE, (speed,speed))
        except ValueError as exc:
            arc['finite_burn_seed_rejection'] = str(exc)
            continue
        dv2 = np.asarray(sep['second_correction_m_s'])
        axis = np.asarray(sep['relative_velocity_m_s'])/speed
        x = np.array([math.atan2(dv1[1],dv1[0]),math.atan2(dv2[1],dv2[0]),
                      (y[4]-m1)*fb.VE/thrust,
                      (m1-sep['mass_after_second_kg'])*fb.VE/thrust])
        candidates.append((y[4]-sep['mass_after_second_kg'],x,axis))
    if not candidates:
        return None, shot
    return min(candidates,key=lambda c:c[0]), shot


def plan(y, index, speed, thrust, previous_angle):
    seed, impulse_searches = seeds(y,index,speed,thrust)
    if seed is None:
        return dict(index=index,selected=None,attempts=[],impulse_searches=impulse_searches,
                    reason='NO_ACCEPTED_IMPULSIVE_SEED')
    _, x, axis = seed
    duration_limit = min(450.,y[4]*(1-math.exp(-100/fb.VE))*fb.VE/thrust)
    lower = np.r_[x[:2]-math.pi,0.,0.]
    upper = np.r_[x[:2]+math.pi,duration_limit,duration_limit]
    attempts = []
    for offset in (0.,.05,-.05):
        z = np.clip(x,lower+1e-8,upper-1e-8)
        z[0] += offset
        z[1] -= offset
        try:
            sol = least_squares(lambda q:evaluate(y,q,index,speed,thrust,axis,previous_angle)['residual'],
                                z,bounds=(lower,upper),x_scale=[1,1,100,100],diff_step=1e-4,
                                xtol=1e-9,ftol=1e-9,gtol=1e-9,max_nfev=120)
            row = evaluate(y,sol.x,index,speed,thrust,axis,previous_angle,terminal=True)
            row.update(seed_offset_rad=offset,nfev=sol.nfev,solver_success=bool(sol.success))
        except (ValueError,FloatingPointError) as exc:
            row = dict(seed_offset_rad=offset,accepted=False,reason=str(exc))
        attempts.append(row)
    choices = [a for a in attempts if 'residual' in a]
    best = min(choices,key=lambda a:(not a['accepted'],sum(v*v for v in a['residual']))) if choices else None
    return dict(index=index,axis=axis.tolist(),selected=best,attempts=attempts,
                impulse_searches=impulse_searches)


def replay(stages,speed,thrust,errors=None,tight=False):
    errors = np.zeros(6) if errors is None else np.asarray(errors)
    y = np.r_[tt.initial()+errors[:4],INITIAL_MASS]
    angle = None
    rows = []
    for stage in stages:
        row = evaluate(y,stage['selected']['parameters'],stage['index'],speed,thrust,
                       stage['axis'],angle,tight=tight,error=errors[4:],terminal=True)
        rows.append(row)
        y = np.array(row['host_state'])
        angle = math.atan2(stage['axis'][1],stage['axis'][0])
        # Commanded attitude is unchanged; angle error is local release-axis calibration.
    fuel_used = sum(r['fuel_used_kg'] for r in rows)
    return dict(errors=errors.tolist(),deliveries=rows,
                accepted=bool(len(rows)==N and all(r['accepted'] for r in rows)),
                prefix_accepted=bool(rows and all(r['accepted'] for r in rows)),
                unserved_deliveries=N-len(rows),
                missed_deliveries=sum(not r['accepted'] for r in rows),
                final_host_mass_kg=float(y[4]),fuel_remaining_kg=float(y[4]-DRY-(N-len(rows))*PAYLOAD),
                total_mass_balance_residual_kg=abs(INITIAL_MASS-y[4]-len(rows)*PAYLOAD-fuel_used))


def campaign(speed,thrust):
    y = np.r_[tt.initial(),INITIAL_MASS]
    angle = None
    stages = []
    for index in range(1,N+1):
        stage = plan(y,index,speed,thrust,angle)
        stages.append(stage)
        chosen = stage['selected']
        print(f'S12 speed={speed:g} thrust={thrust:g} stage={index} accepted={bool(chosen and chosen["accepted"])}',flush=True)
        if not chosen or not chosen['accepted']:
            break
        y = np.array(chosen['host_state'])
        angle = math.atan2(stage['axis'][1],stage['axis'][0])
    completed = sum(bool(s['selected'] and s['selected']['accepted']) for s in stages)
    result = dict(speed_m_s=speed,thrust_N=thrust,stages=stages,completed_deliveries=completed,
                  unserved_deliveries=N-completed,accepted=completed==N,corners=[])
    if completed:
        prefix = stages[:completed]
        nominal = replay(prefix,speed,thrust)
        tight = replay(prefix,speed,thrust,tight=True)
        dp,dv = [],[]
        for a,b in zip(nominal['deliveries'],tight['deliveries']):
            delta = np.array(a['terminal_state'])-b['terminal_state']
            dp.append(float(np.linalg.norm(delta[:2])))
            dv.append(float(np.linalg.norm(delta[2:])))
        dm = abs(nominal['final_host_mass_kg']-tight['final_host_mass_kg'])
        result.update(nominal=nominal,convergence=dict(position_changes_m=dp,velocity_changes_m_s=dv,
                      host_mass_change_kg=dm,passed=max(dp)<=.01 and max(dv)<=1e-5 and dm<=1e-8))
        for signs in itertools.product((-1,1),repeat=6):
            result['corners'].append(replay(prefix,speed,thrust,WIDTHS*signs))
    return result


def verification(rows):
    events = [a for c in rows for s in c['stages'] for a in s['attempts'] if 'mass_balance_residual_kg' in a]
    histories = [h for c in rows for h in ([c['nominal']] if 'nominal' in c else [])+c['corners']]
    events += [a for h in histories for a in h['deliveries']]
    return dict(s11_identities=all(fb.checks().values()),
                event_accounting=bool(events) and all(a['mass_balance_residual_kg']<=1e-8 and
                    a['momentum_residual_kg_m_s']<=1e-6 and a['relative_speed_residual_m_s']<=1e-10 for a in events),
                manifest_accounting=all(h['total_mass_balance_residual_kg']<=1e-8 for h in histories),
                convergence=all(c['convergence']['passed'] for c in rows if 'convergence' in c),
                verified_prefix_count=sum('convergence' in c for c in rows),
                completed_manifest_verification_count=sum(c['accepted'] for c in rows))


def hashes():
    names = ['analysis/manifest_finite_burn.py','analysis/finite_burn_departure.py',
             'analysis/manifest_timing.py','analysis/terminal_timing.py','analysis/campaign_allocation.py',
             'analysis/host_reference.py','validation/P113_S12_manifest_finite_burn.md']
    return {n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names}


def report(d):
    lines = ['# Twelve-payload finite-burn campaign — P113-S12','', 'Adityavardhan Mishra · 26 September 2026','',
             'A matched reference screen carries finite burns, propellant, host recoil and the previous release attitude through twelve planned deliveries. Every scenario uses the same targets and release times. The host dry mass is held equal as a sensitivity, not an installed architecture comparison.','',
             '| Speed (m/s) | Thrust (N) | Delivered / 12 | Fuel used (kg) | Passing partial-history corners |',
             '|---:|---:|---:|---:|---:|']
    for c in d['cases']:
        fuel = sum(s['selected']['fuel_used_kg'] for s in c['stages'] if s['selected'] and s['selected']['accepted'])
        corners = f"{sum(h['prefix_accepted'] for h in c['corners'])} / 64" if c['corners'] else 'no accepted prefix'
        lines.append(f"| {c['speed_m_s']:g} | {c['thrust_N']:g} | {c['completed_deliveries']} | {fuel:.6f} | {corners} |")
    lines += ['', 'Fuel in incomplete campaigns counts only accepted deliveries; an unsuccessful search is retained but not executed. Each failed nominal leaves the remaining payloads unserved. A bounded search miss does not prove infeasibility.', '',
              'The 64 corners are deterministic signed error combinations, not a probability or a flight navigation covariance. Replay retains fixed commands and correlated calibration errors across all releases; it is not feedback navigation. Partial-history corners assess only delivered payloads; every complete mission still fails because payloads remain unserved. Numerical verification and mission acceptance are distinct.', '',
              'Limits: planar two-body gravity; assumed thrust and slew law; endpoint perigee guard only; no continuous collision/plume clearance, torque/momentum, flexible-body response, disposal, hardware accuracy or installed mass advantage is established.', '',
              '[Frozen criteria](../validation/P113_S12_manifest_finite_burn.md) · [All attempts and histories](../analysis/results/manifest_finite_burn.json)', '']
    return '\n'.join(lines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    if args.check:
        data = json.loads(OUT.read_text())
        assert data['source_sha256']==hashes(), 'STALE_SOURCE'
        assert DOC.read_text()==report(data), 'STALE_REPORT'
        assert data['verification']==verification(data['cases']), 'STALE_VERIFICATION'
    else:
        rows = []
        for speed,thrust in itertools.product((1.,2.),(1.,10.,100.)):
            rows.append(campaign(speed,thrust))
            data = dict(study='P113-S12',cases=rows,source_sha256=hashes(),
                        runtime=dict(numpy=np.__version__,scipy=scipy.__version__),
                        inputs=dict(payload_count=N,payload_kg=PAYLOAD,dry_kg=DRY,fuel_kg=FUEL,
                                    initial_mass_kg=INITIAL_MASS,terminal_time_s=END,
                                    release_interval_s=1200,target_arc_spacing_m=5000,
                                    uncertainty_widths=WIDTHS.tolist()),verification=verification(rows))
            OUT.write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
        DOC.write_text(report(data))
    assert len(data['cases'])==6, 'INCOMPLETE_CASE_MATRIX'
    assert all(v for k,v in data['verification'].items() if k not in ('completed_manifest_verification_count','verified_prefix_count')), data['verification']
    print(data['verification'])
