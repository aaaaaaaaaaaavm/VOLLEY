"""Conditional compliant arrest sizing; no actual brake or pawl timing claim.

After an assumed catch: m q''+c q'+k q=F_assist; q(0)=0,
q'(0)=v_contact. Before catch, latency and tooth phase permit free travel.
Force is kq+cq' on compression. Catch/rebound/latch mechanics require validation.
"""
from pathlib import Path
import hashlib
import itertools
import json
import numpy as np
from scipy.integrate import solve_ivp

H=Path(__file__).resolve().parent
O=H/"release"
O.mkdir(exist_ok=True)


def case(mass,speed,delay,pitch,k,c,assist,step=.001):
    # Constant assisting load during both latency/pitch travel and compression.
    a=assist/mass
    drift_delay=speed*delay+.5*a*delay**2
    v_after=speed+a*delay
    v_contact=(v_after**2+2*a*pitch)**.5
    free=drift_delay+pitch
    def rhs(t,y):return [y[1],(assist-c*y[1]-k*y[0])/mass]
    def stopped(t,y):return y[1]
    stopped.terminal=True;stopped.direction=-1
    sol=solve_ivp(rhs,[0,1],[0,v_contact],rtol=1e-10,atol=1e-12,max_step=step,events=stopped,dense_output=True)
    assert sol.t_events[0].size,"No first compression stop"
    end=float(sol.t_events[0][0]);times=np.linspace(0,end,1001)
    q,v=sol.sol(times)
    force=k*q+c*v
    compression=float(q[-1]);peak=float(force.max())
    diss=float(np.trapezoid(c*v*v,times))
    stored=.5*k*compression**2
    input_energy=.5*mass*v_contact**2+assist*compression
    # Independent undamped energy solution gives a compression upper bound.
    undamped=(assist+(assist**2+k*mass*v_contact**2)**.5)/k
    assert compression<=undamped+1e-8
    assert abs(diss+stored-input_energy)<max(1e-6,input_energy*2e-5)
    # Thick-root proposal, with explicit nominal static formulas and Kt band.
    nominal=6*peak*3/(16*6**2)
    return dict(mass_kg=mass,speed_m_s=speed,delay_s=delay,tooth_phase_m=pitch,k_N_m=k,c_Ns_m=c,assist_N=assist,
        free_travel_mm=1000*free,compression_mm=1000*compression,total_runout_mm=1000*(free+compression),
        first_stop_s=end,peak_compression_force_N=peak,elastic_energy_J=stored,dissipation_J=diss,
        energy_residual_J=diss+stored-input_energy,undamped_compression_bound_mm=1000*undamped,
        nominal_tooth_root_bending_MPa=nominal,Kt3_tooth_bending_MPa=3*nominal,
        within_12mm_compliance=compression<=.012,within_24mm_total_runout=free+compression<=.024)


def run():
    rows=[case(*p) for p in itertools.product([2.83,5.5,7.5],[.04,.08,.2],[.005,.02,.05],[.002,.01],[8000,16000,32000],[0,80,160],[0,50])]
    worst=max(rows,key=lambda x:x["total_runout_mm"])
    refined=case(*[worst[k] for k in ["mass_kg","speed_m_s","delay_s","tooth_phase_m","k_N_m","c_Ns_m","assist_N"]],step=.0005)
    assert abs(refined["compression_mm"]-worst["compression_mm"])<1e-5
    result=dict(revision="CT-01-2026-10-19",cases=rows,count=len(rows),
      max_total_runout_mm=max(x["total_runout_mm"] for x in rows),max_peak_force_N=max(x["peak_compression_force_N"] for x in rows),
      compliance_failures=sum(not x["within_12mm_compliance"] for x in rows),runout_failures=sum(not x["within_24mm_total_runout"] for x in rows),
      max_Kt3_bending_MPa=max(x["Kt3_tooth_bending_MPa"] for x in rows),
      refinement_compression_change_mm=abs(refined["compression_mm"]-worst["compression_mm"]),
      boundary="Assumed catch, square cantilever root, linear spring/damper and assisting force. No actual pawl engagement, damping, material allowable, contact peak, bearing/pin, rebound retention or load-path qualification. The compliance module is not yet integrated into CT-01 geometry.",
      source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (O/"STOP_DYNAMICS.json").write_text(json.dumps(result,indent=2)+"\n")
    print({k:v for k,v in result.items() if k not in ["cases","boundary","source_sha256"]})
    return result


if __name__=="__main__":run()
