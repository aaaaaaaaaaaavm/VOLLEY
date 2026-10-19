"""RPL-01 limited orbital reload interface feasibility, SI units unless named.

Hypothetical cooperative preloaded cartridges; no rendezvous or robot claim.
Independent energy/momentum/load identities and adverse insertion fits retained.
"""
from pathlib import Path
import itertools,json,math,hashlib
H=Path(__file__).resolve().parent;O=H/"release";O.mkdir(exist_ok=True)


def run():
    captures=[];fits=[]
    for mass,speed,stroke,rate in itertools.product([5,15,40],[.01,.05,.1,.2],[.005,.01,.02],[0,1,5]):
        host=300;reduced=mass*host/(mass+host)
        # Slender-body pitch inertia surrogate, not actual cartridge/servicer inertia.
        inertia=mass*(.3645**2+.14**2)/12
        energy=.5*reduced*speed**2+.5*inertia*math.radians(rate)**2
        impulse=reduced*speed
        mean=energy/stroke
        captures.append(dict(cartridge_kg=mass,relative_m_s=speed,assumed_stopping_m=stroke,pitch_rate_deg_s=rate,
          reduced_mass_kg=reduced,energy_J=energy,mean_energy_force_N=mean,linear_impulse_Ns=impulse,
          host_delta_v_m_s=impulse/host,launch_load_25g_N=mass*25*9.80665,
          force_exceeds_sensitivity_N={str(n):mean>n for n in [25,100,500]}))
        assert math.isclose(.5*mass*(speed-impulse/mass)**2+.5*host*(impulse/host)**2+.5*reduced*speed**2,.5*mass*speed**2,abs_tol=1e-12)
    for offset,angle,clearance in itertools.product([.5,2,4],[.1,.25,.5,1],[3,5,10]):
        # Worst additive lateral offset, full length angle, 0.30 manufacture +0.20 thermal.
        consumed=offset+364.5*math.sin(math.radians(angle))+.3+.2
        fits.append(dict(offset_mm=offset,angle_deg=angle,radial_clearance_mm=clearance,
          consumed_mm=consumed,remaining_mm=clearance-consumed,positive_gap=consumed<clearance))
    d=dict(revision="RPL-01-2026-10-19",capture_cases=captures,insertion_cases=fits,
      max_energy_J=max(x["energy_J"] for x in captures),max_mean_force_N=max(x["mean_energy_force_N"] for x in captures),
      fit_failures=sum(not x["positive_gap"] for x in fits),baseline_disposition="NO_GO_FOR_OPERATIONAL_REPLENISHMENT_CLAIM",
      boundary="Limited cooperative-cartridge concept and requirements. No servicer trajectory, robotics, physical capture/contact, docking stability, flight loads qualification, customer/provider ICD or replenishment hardware exists.",
      source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (O/"RESULTS.json").write_text(json.dumps(d,indent=2)+"\n")
    return d


if __name__=="__main__":
    d=run();print(len(d["capture_cases"]),"capture sensitivities,",len(d["insertion_cases"]),"fits,",d["fit_failures"],"failed fits")
