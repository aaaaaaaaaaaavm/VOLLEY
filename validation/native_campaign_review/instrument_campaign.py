"""Derive an event-exporting copy without altering archived campaign physics."""
from pathlib import Path
import hashlib,difflib,json
H=Path(__file__).resolve().parent
P=H/'reference/run.py'
s=P.read_text();s=s[:s.index('    def host_state(t):')]
s=s.replace('"""Constructive matched four/twelve-release campaign and conditional clearance.','"""Event-export derivative of the constructed four/twelve-release campaign.')
s=s.replace('    def burn(delta, label):','''    events = [dict(t_s=0.0,kind="initial",payload=0,delta=[0.0]*3,
                   mass_before_kg=300+device+remaining+fuel,
                   mass_after_kg=300+device+remaining+fuel,payload_kg=0,
                   expected_host=s0.tolist(),target_final=reference.y[:,-1].tolist())]

    def burn(delta, label, event_time):''')
s=s.replace('''        fuel -= used
        burns.append''','''        expected_host=host.copy()
        expected_host[3:]+=delta
        events.append(dict(t_s=float(event_time),kind="burn",role=label,payload=0,
                           delta=delta.tolist(),mass_before_kg=total,
                           mass_after_kg=total-used,payload_kg=0,
                           expected_host=expected_host.tolist(),target_final=[0.0]*6))
        fuel -= used
        burns.append''')
s=s.replace('burn(needed - host[3:], "pre " + str(i + 1))','burn(needed - host[3:], "pre " + str(i + 1), t)')
s=s.replace('''        host = parent
        coast_end''','''        host = parent
        events.append(dict(t_s=float(t),kind="shot",payload=i+1,
                           delta=(u*tangent).tolist(),mass_before_kg=M,
                           mass_after_kg=M-m,payload_kg=m,
                           expected_host=host.tolist(),target_final=target.y[:,-1].tolist()))
        coast_end''')
s=s.replace('burn(vel - host[3:], "transfer " + str(i + 1))','burn(vel - host[3:], "transfer " + str(i + 1), coast_end)')
s=s.replace('burn(target_host[3:] - host[3:], "final host velocity restoration")','burn(target_host[3:] - host[3:], "final host velocity restoration", arrival)')
s+='''    return dict(count=N,strategy=strategy,initial_fuel_kg=initial_fuel,
                device_mass_proxy_kg=device,fuel_used_kg=initial_fuel-fuel,
                initial_host=events[0]["expected_host"],events=events,
                reference_host_final=reference.y[:,-1].tolist(),
                source_host_final=host_arcs[-1][2].y[:,-1].tolist(),shots=shots,burns=burns)
'''
assert s.count('def burn(')==1
assert all(x in s for x in ['events.append(dict(t_s=float(t)','event_time','return dict(count=N'])
(H/'export_campaign.py').write_text(s)
(H/'EVENT_EXPORT_DIFF.patch').write_text(''.join(difflib.unified_diff(P.read_text().splitlines(True),s.splitlines(True),fromfile='archived coupled run.py',tofile='event export derivative.py')))
(H/'EXPORT_SOURCE_IDENTITY.json').write_text(json.dumps({'upstream':'VOLLEY-lab/experiments/coupled-delivery-review/run.py','upstream_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'derived_sha256':hashlib.sha256(s.encode()).hexdigest(),'scope':'Same trajectory/root/recoil/rocket calculations; adds event logging and replaces later clearance/dense-output reporting. No original source or result changed.'},indent=2)+'\n')
