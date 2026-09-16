"""P113-S6: simultaneous conditional release-error corners, not campaign closure."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import numpy as np
import operational_uncertainty as ou
import campaign_allocation as campaign

ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/"analysis/results/combined_release_errors.json"
DOC=ROOT/"docs/COMBINED_RELEASE_ERRORS.md"
WIDTHS=(0.1,0.1,0.0001,0.0001,0.0005,math.radians(0.005))
SCALES=(0,1,2,5)

def combined(event,nominal,errors):
    if len(errors)!=6 or not np.all(np.isfinite(errors)):
        raise ValueError("six finite error coordinates required")
    r,t=np.asarray(nominal["radial_basis"]),np.asarray(nominal["tangential_basis"])
    u=np.asarray(nominal["relative_velocity_m_s"])
    if np.linalg.norm(u)+errors[4]<=0:raise ValueError("release speed must remain positive")
    u1=ou.rotate(u/np.linalg.norm(u)*(np.linalg.norm(u)+errors[4]),errors[5])
    payload,host,residual=ou.reconstruct_mechanism_state(event,u1)
    common=np.r_[errors[0]*r+errors[1]*t,errors[2]*r+errors[3]*t]
    payload+=common;host+=common
    # The reconstruction is algebraically identical at zero; preserve stored
    # nominal bits to isolate propagation from an unnecessary COM round trip.
    if not any(errors):payload=np.asarray(nominal["payload_state"])
    end=campaign.coast(payload,ou.TERMINAL_TIME_S-event["time_s"])
    error=end-np.asarray(nominal["target_terminal_state"])
    return {"terminal_state":end.tolist(),"terminal_error_vector":error.tolist(),
        "position_error_m":float(np.linalg.norm(error[:2])),
        "velocity_error_m_s":float(np.linalg.norm(error[2:])),
        "momentum_residual_kg_m_s":residual}

def build():
    _,_,candidate=ou.selected_campaign(ou.load_s4())
    s5=json.loads(ou.OUTPUT_JSON.read_text())
    if ou.check_outputs(ou.build()):raise ValueError("fresh S5 evidence required")
    rows=[];summaries=[];zero_ok=True;linear_ok=True
    for i,event in enumerate(candidate["events"]):
        nominal=s5["events"][i]["nominal"]
        sensitivities=s5["events"][i]["sensitivities"]
        matrix=np.column_stack([s["position_sensitivity_vector_per_unit"]+
            s["velocity_sensitivity_vector_per_unit"] for s in sensitivities])
        for scale in SCALES:
            group=[]
            for signs in itertools.product((-1,1),repeat=6):
                errors=np.asarray(WIDTHS)*scale*signs
                d=combined(event,nominal,errors)
                linear=np.asarray(nominal["terminal_error_vector"])+matrix@errors
                difference=np.asarray(d["terminal_error_vector"])-linear
                mismatch={"position_error_m":float(np.linalg.norm(difference[:2])),
                    "velocity_error_m_s":float(np.linalg.norm(difference[2:]))}
                agreement=mismatch["position_error_m"]<=max(0.05,0.02*d["position_error_m"]) and mismatch["velocity_error_m_s"]<=max(0.00005,0.02*d["velocity_error_m_s"])
                if scale==1:linear_ok &= agreement
                if scale==0:
                    z=np.asarray(d["terminal_state"])-np.asarray(nominal["terminal_state"])
                    zero_ok &= bool(np.linalg.norm(z[:2])<=1e-6 and np.linalg.norm(z[2:])<=1e-9)
                d.update({"event_index":i,"scale":scale,"signs":list(signs),"error_coordinates":errors.tolist(),
                    "linear_direct_difference":mismatch,"linear_agreement":agreement,
                    "mission_bands_passed":d["position_error_m"]<=10 and d["velocity_error_m_s"]<=0.01})
                rows.append(d);group.append(d)
            summaries.append({"event_index":i,"scale":scale,"accepted_count":sum(d["mission_bands_passed"] for d in group),
                "position_error_m":max(d["position_error_m"] for d in group),
                "velocity_error_m_s":max(d["velocity_error_m_s"] for d in group),
                "linear_triangle_bound":{
                    "position_error_m":nominal["position_error_m"]+scale*sum(w*s["position_sensitivity_norm_per_unit"] for w,s in zip(WIDTHS,sensitivities)),
                    "velocity_error_m_s":nominal["velocity_error_m_s"]+scale*sum(w*s["velocity_sensitivity_norm_per_unit"] for w,s in zip(WIDTHS,sensitivities))}})
    sources=["analysis/combined_release_errors.py","analysis/results/operational_uncertainty.json",
        "analysis/results/manifest_timing.json","validation/P113_S6_combined_release_errors.md"]
    gap=candidate["events"][1]["time_s"]-candidate["events"][0]["time_s"]
    return {"study":"P113-S6","evidence":"CONDITIONAL_EVENT_CORNER_SCREEN","open_items":["P113","E5","P92"],
        "source_sha256":{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources},
        "half_widths":list(WIDTHS),"scales":list(SCALES),"case_count":len(rows),"cases":rows,"summaries":summaries,
        "reserve_headroom_s":{str(r):gap-r for r in (30,60,120,300)},
        "checks":{"zero_error_reproduction":zero_ok,"base_box_linear_agreement":linear_ok,
            "momentum":all(d["momentum_residual_kg_m_s"]<=1e-9 for d in rows),"case_count":len(rows)==512},
        "verification_passed":bool(zero_ok and linear_ok and len(rows)==512 and all(d["momentum_residual_kg_m_s"]<=1e-9 for d in rows))}

def report(d):
    lines=["# Combined release-error corners", "",
        "I combine six simultaneous error terms around each of the two stored S4 release events. Each event starts from its nominal host state. This is **conditional event evidence**, not a robust two-event campaign or a probability of success. P113, E5 and P92 remain open.", "",
        "The illustrative base box uses 0.1 m per host position axis, 0.0001 m/s per host velocity axis, 0.0005 m/s release-speed error and 0.005 degrees release-direction error. These are assumptions, not hardware requirements or provider capabilities.", "",
        f"**{d['case_count']} corners evaluated. Numerical verification: {'PASS' if d['verification_passed'] else 'FAIL'}.** Mission failures remain in the table and JSON.", "",
        "| Event | Box multiplier | Corners within 10 m / 0.01 m/s | Worst sampled position (m) | Worst sampled velocity (m/s) |",
        "|---|---:|---:|---:|---:|"]
    for r in d["summaries"]:
        lines.append(f"| {r['event_index']+1} | {r['scale']} | {r['accepted_count']}/64 | {r['position_error_m']:.6f} | {r['velocity_error_m_s']:.8f} |")
    lines += ["", "A corner maximum is only the maximum among the sampled corners. Nonlinear maxima inside or along the edges of the box are not excluded. The JSON separately reports the triangle-inequality envelope of the local linear model and direct-versus-linear discrepancies.", "",
        "## What remains to close", "",
        "First-event host error must be propagated through the second manoeuvre and release, with a declared navigation/control policy. Correlations, full manifest, pointing recovery, collision clearance, disposal reserve and provider resource limits remain absent. The 1,800 s nominal release gap exceeds the illustrative 300 s reserved interval by 1,500 s; this arithmetic is not proof of settling or safety.", "",
        "A release-cell repeatability target must be allocated together with common navigation and pointing errors. Increasing mechanical precision cannot remove a common host-state error. Reject or change the mission/error allocation if the required operational box cannot satisfy the terminal bands.", "",
        "[Frozen criteria](../validation/P113_S6_combined_release_errors.md) · [Every corner and source hash](../analysis/results/combined_release_errors.json) · [S5 sensitivities](OPERATIONAL_UNCERTAINTY.md)", "",
        "Reproduce: `python analysis/combined_release_errors.py --check`.", ""]
    return "\n".join(lines)

def main():
    p=argparse.ArgumentParser();p.add_argument("--check",action="store_true");a=p.parse_args();d=build()
    if a.check:
        stored=json.loads(RESULT.read_text())
        if not campaign.numerical_match(stored,d) or DOC.read_text()!=report(stored):raise SystemExit("P113-S6 outputs stale")
    else:
        RESULT.write_text(json.dumps(d,sort_keys=True,indent=2)+"\n");DOC.write_text(report(d))
    if not d["verification_passed"]:raise SystemExit("P113-S6 verification failed; retain evidence")
    print("P113-S6: 512 conditional corners; verification PASS; campaign closure remains open")

if __name__=="__main__":main()
