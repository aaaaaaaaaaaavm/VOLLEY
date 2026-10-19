"""Reader report and figures generated from the captured numerical/native data."""
from pathlib import Path
import json,hashlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

H=Path(__file__).resolve().parent;O=H/"release";F=O/"figures";F.mkdir(exist_ok=True)
load=lambda p:json.loads((O/p).read_text())
D=load("STOP_DYNAMICS.json");T=load("TOLERANCE.json");G=load("CONTINUOUS_GEOMETRY.json");N=load("NATIVE_CAD.json");I=load("INTERLOCKS.json");FE=load("tooth_fea/RESULTS.json")
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"axes.spines.top":False,"axes.spines.right":False,"svg.fonttype":"none","pdf.fonttype":42,"figure.dpi":150})


def save(fig,stem):
    fig.tight_layout()
    for ext in ["png","svg","pdf"]:fig.savefig(F/(stem+"."+ext),bbox_inches="tight",metadata={"Creator":"VOLLEY engineering study"})
    plt.close(fig)


fig,ax=plt.subplots(figsize=(7.3,3.5))
for assist,color in [(0,"#286489"),(50,"#a94f21")]:
    rows=[r for r in D["cases"] if r["assist_N"]==assist]
    ax.scatter([r["speed_m_s"]+(r["delay_s"]-.02)*.2 for r in rows],[r["total_runout_mm"] for r in rows],s=10,alpha=.35,color=color,label=f"{assist} N assisting force")
ax.axhline(24,color="black",linestyle="--",linewidth=1,label="24 mm proposed allowance")
ax.set(xlabel="Initial transfer speed [m/s]; points offset by response delay",ylabel="Calculated total runout [mm]",title="Conditional arrest: delay, tooth phase and compression")
ax.legend(fontsize=8);save(fig,"stop_runout")

fig,axs=plt.subplots(1,2,figsize=(8.5,3.4))
for force,color in [(425.22496995827527,"#286489"),(876.9,"#a94f21")]:
    rows=[r for r in FE["cases"] if r["force_N"]==force]
    axs[0].plot([r["elements"] for r in rows],[1e6*r["max_uy_m"] for r in rows],"o-",color=color,label=f"{force:.1f} N")
    axs[1].plot([r["elements"] for r in rows],[r["max_von_mises_MPa"] for r in rows],"o-",color=color)
axs[0].set(xlabel="C3D8I elements",ylabel="Maximum transverse displacement [µm]")
axs[1].set(xlabel="C3D8I elements",ylabel="Maximum integration-point von Mises [MPa]")
axs[0].legend();fig.suptitle("Enlarged isolated tooth — fixed-root fixture, unconverged peak stress")
save(fig,"tooth_mesh")

views=load("STEP_EDGES.json")
fig,axs=plt.subplots(2,2,figsize=(9,7))
for ax,v in zip(axs.flat,views[:4]):
    for edge in v["edges"]:
        q=np.array(edge);ax.plot(q[:,1],q[:,2],color="#334e5c",linewidth=.45)
    ax.set_aspect("equal");ax.set(xlabel="Feed Y [mm]",ylabel="Normal Z [mm]",title=v["stem"].replace("CT01_3U_","").replace("_"," "))
    ax.set_xlim(-250,130);ax.set_ylim(-110,255)
fig.suptitle("CT-01 · 3U STEP side projections · prescribed poses")
save(fig,"step_sequence")
from PIL import Image
with Image.open(F/"step_sequence.png") as im:im.convert("RGB").save(F/"step_sequence.jpg",quality=94)

sub=[r for r in D["cases"] if r["assist_N"]==0 and r["speed_m_s"]<=.08 and r["delay_s"]<=.02]
native_mass={r["payload"]:r["material_kg"] for r in N["cases"] if r["phase"]=="stored_captive"}
text=f'''---
title: "VOLLEY Gen6 — captive-transfer correction"
date: "19 October 2026 · CT-01"
geometry: margin=18mm
fontsize: 10pt
mainfont: DejaVu Sans
---

# Scope and disposition

CT-01 is a separately versioned nominal transfer-coupon investigation. It does not select a feeder, replace the frozen evaluated Gen5, or repair every FDR-08 candidate. The seven feeder alternatives remain in the earlier equal-boundary trade. This study addresses the common custody geometry and a separate compliant-arrest sizing hypothesis.

The prescribed rectilinear cycle now has continuous interference evidence. Positive retention after a real actuator/sensor fault, loaded clearances, actual joint ratings and integration with a moving launcher sled remain unresolved. The external-departure phase is imposed motion; it is not an electromagnetic launch simulation.

# Controlled configuration

Public-envelope surrogates: 1U length 113.5 mm and 3U length 340.5 mm, each 100 × 100 mm cross-section; 200 mm lateral transfer. Feed is Y, nominal departure is X and normal is Z. A captive C guide supports a connected overhead fork, front/rear barriers, rear corner lugs and top retainers. Receiver locks and its top retainers occupy separate bands from the fork. No supplier-approved passive-spacecraft contact interface is claimed.

The storage gate retracts **downward by 120 mm through an actual floor slot**. This removes the crossing with the overhead fork but creates an explicit under-deck accommodation requirement: the open gate extends to Z = −98 mm while the floor underside is Z = 16 mm. Receiver Y dogs retract laterally by 20 mm; their X stop counterparts retract upward by 120 mm. These motions require actuator, guide, latch and mechanical interlock design. Native solids do not substitute for those joints.

Modeled material is {native_mass['1U']:.3f} kg for the 1U coupon and {native_mass['3U']:.3f} kg for 3U, excluding payload, source-rated drives, actuators, purchased bearings, sensors, wiring, fasteners and host interface. Native volume-derived CG and inertia are recorded for all 22 states; these are not installed system properties or a fair seven-feeder mass ranking.

# Continuous geometry and custody

The sequence is stored/captive → storage gate retracted → transfer → receiver capture → front barrier raised → fork return → storage gate closed → fork reset. Receiver release requires independently verified external sled custody. The subsequent X translation and empty-receiver reset are explicit boundary surrogates.

For each represented axis-aligned constituent, both bounds vary linearly over phase time. Positive-volume intersection requires overlap in all axes at the same instant. Intersecting those strict time intervals provides a continuous prescribed-translation test, rather than endpoint or time-grid clearance. Same-part constituents are fused, and deliberate shared contact faces are not treated as positive penetration. This is exact for the stated primitive geometry; it excludes rotations, compliance and actual actuator linkages.

{G['continuous_phase_cases']} continuous 1U/3U phase cases report {G['penetration_count']} positive penetrations. FreeCAD/OpenCascade independently checked 60 endpoint/midpoint poses. Twenty-two native FCStd and 22 STEP states plus a separate contact coupon were created; STEP readback verifies valid solids and total material volume. Small-gap contact, tolerance and loaded motion remain separate questions.

![Independent STEP side projections; nominal prescribed geometry](release/figures/step_sequence.png)

The native application capture below shows the stored FreeCAD document in a Python-hosted Qt/Coin viewer. Colour distinguishes the payload and moving gates; no application interface or geometry is composited. The native document is not saved by the capture process.

![Genuine FreeCAD viewport of CT-01 receiver-capture pose; conceptual interfaces remain unrated](release/FreeCAD_CT01_receiver.png)

# Fault logic and retained counterexamples

The executable guard model checks {len(I['guard_cases'])} combinations around opening the fork, returning it and unlocking the receiver. Other cells cannot advance while shared-path proof is invalid. This verifies requirements under truthful physical indications; it is not a real electrical implementation.

Three counterexamples remain: a false receiver-locked indication permits unsafe fork opening; a power-failed storage gate can close onto a straddling payload unless physically inhibited; and unlocking without actual sled custody loses the defined retention chain. They require independent retention verification, mechanical hold-open/holding design and a real receiver-to-sled interface. Logical guards alone do not resolve them.

# Local tolerance sensitivity

{len(T['cases'])} gap screens apply 0.30 mm combined manufacturing allowance, angular error over 200 mm, differential CTE over −40/20/80°C, and 0/0.5/1.3 mm assumed deflections. {T['negative_or_zero']} cases have nonpositive residual clearance. This is a conservative local sensitivity, not a GD&T assembly solution. The smallest nominal guide/receiver gaps are 1 mm. Neither nominal nonpenetration nor a selected favorable angular case establishes loaded fit.

# Conditional compliant arrest

The proposed square rack root grows from the earlier 8 × 1 mm section to 16 × 6 mm, at 3 mm contact height. A separate STEP/FreeCAD coupon has one square bolt in actual face contact with a tooth; insertion, preload and the attachment load path are not implemented. This geometry is not yet connected to the moving fork.

After an assumed catch, the model solves m q̈ + c q̇ + k q = F. Free travel includes response latency and tooth phase. The 972 cases span 2.83/5.5/7.5 kg moving mass, 0.04/0.08/0.20 m/s, 5/20/50 ms assumed delay, 2/10 mm tooth phase, 8/16/32 kN/m stiffness, 0/80/160 Ns/m damping and 0/50 N assisting force. The 7.5 kg bound is provisional; installed moving hardware must be rechecked.

Maximum calculated runout is {D['max_total_runout_mm']:.2f} mm; {D['compliance_failures']} cases exceed 12 mm compression and {D['runout_failures']} exceed 24 mm total allowance. Maximum compression force is {D['max_peak_force_N']:.2f} N under this linear model. Unmodeled pawl impact can produce different peaks. Energy balance and an independent undamped compression bound are checked; halving the selected worst-case time step changes compression by {D['refinement_compression_change_mm']:.3g} mm.

The restricted, **unvalidated operating hypothesis** of speed ≤0.08 m/s, response ≤20 ms and removal of assisting force has {len(sub)} cases, with maximum runout {max(r['total_runout_mm'] for r in sub):.2f} mm. This is a candidate requirement for a 5 s or slower transfer, not a rated operating envelope. The persistent-force cases show why passive spring-driven and powered drives cannot share an assumed safe-stop result.

![Calculated runout, including failed assumptions](release/figures/stop_runout.png)

# Native tooth fixture analysis

CalculiX 2.23 ran six C3D8I cases for the 16 × 6 × 3 mm isolated tooth at 425.225 N and 876.9 N. Steel E = 200 GPa and ν = 0.3 are assumptions. The lower face is fully fixed and transverse load is distributed over the top face. Reaction force balances are checked. The last mesh has 432 elements; at 876.9 N, maximum displacement is {FE['cases'][-1]['max_uy_m']*1e6:.3f} µm and maximum integration-point von Mises stress is {FE['cases'][-1]['max_von_mises_MPa']:.2f} MPa.

Last-mesh displacement changes by {FE['cases'][-1]['last_displacement_relative_change']*100:.2f}% and peak stress by {FE['cases'][-1]['last_peak_stress_relative_change']*100:.2f}%. Peak stress is **not converged**; no selected alloy allowable, strength margin or qualified tooth follows. Sharp roots, contact, fillets, pins, attached rack support, rebound, fatigue and impact remain absent. The short block also limits the slender-beam approximation. Raw INP/DAT/FRD/logs are included.

![Actual native fixture mesh study; no strength qualification](release/figures/tooth_mesh.png)

# Verification status and next design actions

| Finding | Current disposition |
|:--|:--|
| Overhead storage gate crosses fork in motion | Corrected in CT-01 prescribed geometry by downward gate and floor slot; under-deck fit unapproved. |
| Receiver locks cross fork overhead member | Corrected in CT-01 prescribed geometry by separate lateral/vertical lock motions. Actual guides and latches remain open. |
| Fork custody and withdrawal only shown as snapshots | Continuous nominal rectilinear cycle checked; actual contact and actuator mechanism remain open. |
| Earlier thin tooth and unengaged pawl | Larger isolated root/face-contact coupon analyzed; no integrated, rated retention mechanism. |
| Stop travel after power loss | Broad candidate envelope fails; a restricted drive-removed hypothesis is identified for validation. |
| False latch indication / gate falling onto payload | Physical counterexamples retained; controller model is insufficient. |
| Loaded clearance | Adverse local sensitivities fail; actual datum stack and assembly FEA required. |
| Four/twelve-cell integration | Not supplied by this single-cell coupon. |

# Reproduction

Use FreeCAD 1.0/OpenCascade 7.8.1 system Python for build_native.py and extract_views.py. Run audit.py, stop_dynamics.py, interlocks.py, tolerance.py and report.py in Python with NumPy, SciPy and Matplotlib. Set CCX to CalculiX 2.23 for tooth_fea.py. Captured evidence can be checked without native solvers using check_capture.py. Exact source/output hashes accompany the release. This report is generated; edit its generator and rebuild.
'''
(H/"README.md").write_text(text)
print("CT-01 figures and reader report generated")
