"""Build the bounded feeder review from the captured results and figures."""

from pathlib import Path
import json, subprocess, re

H = Path(__file__).resolve().parent


def read(n):
    return json.loads((H / n).read_text())


cad = read("cad/NATIVE_CAD.json")
sweep = read("CONTINUOUS_SWEEPS.json")
physical = read("PHYSICAL_INTERLOCKS.json")
drive = read("INTEGRATED_DRIVE.json")
brake = read("BRAKE_REVIEW.json")
fit = read("FIT_BUDGET.json")
mass = read("METROLOGY.json")
sched = read("SCHEDULE.json")
control = read("CONTROLLER_REVIEW.json")
convergence=read('CONVERGENCE.json')
bytime = [
    (
        t,
        sum(
            r["ambient_catalogue_screen_pass"]
            for r in drive["cases"]
            if r["time_s"] == t
        ),
    )
    for t in [5, 10, 15, 20]
]
body = (
    rf"""# Feeder actuation and captive transfer review

**FM-02 / IDR-01 / FSR-01 · 20 October 2026**

This review develops a physically represented cassette-to-sled handoff, checks its prescribed rigid motion, and examines ambient drive and campaign-handling feasibility. It is a separate Gen6 research revision. The evaluated Gen5 configuration and its adverse findings are unchanged. No feeder architecture, space-rated actuator, manufacturing release or flight service is selected by this study.

## Main findings

| Evidence | Result | Interpretation |
|:--|:--|:--|
| Native geometry | {len(cad['poses'])} FreeCAD documents and STEP exchanges; {len(cad['motion'])} additional sampled poses | Valid single-solid components; no represented nominal penetration |
| Continuous geometry | {len(sweep['cases'])} prescribed translation phases; {sweep['total_penetrations']} positive-volume intersections | Nominal rigid-motion result; actual joints and loaded fits are unverified |
| Mechanical obstructions | {physical['verified_rigid_obstructions']} deliberate adverse-command checks | Inserted material obstructs the tested motions; strength and axial retention remain separate |
| Controller model | {control['total_cases']} truth/single-channel-fault combinations | No unsafe permission within the stated Boolean model; 26 shared-false-confirmation counterexamples remain |
| Integrated drive | {drive['passes']}/{drive['case_count']} ambient catalogue screens | A sourceable ground-drive candidate; efficiencies and friction remain assumptions |
| Fit sensitivity | {fit['nonpositive']}/{len(fit['cases'])} nonpositive residual gaps | No overall tolerance acceptance |
| Thermal sensitivity | {drive['thermal_failure_count']}/{len(drive['thermal_cases'])} above 125°C | Uncorrelated two-node model; no repeated-cycle or vacuum rating |
| Handling schedule | 11 of32 assumed cycles do not fit | Slow auxiliary motion fails later twelve-release coasts; faster assumptions fit, without component validation |

## Mechanical architecture

The passive payload surrogates are 113.5×100×100mm and 340.5×100×100mm, with nominal masses1.33/4kg. X is the launch direction, Y the 200mm lateral transfer and Z the deck normal. These envelopes do not establish compatibility with a particular spacecraft or provider.

The fork retains the payload while the storage gate opens120mm downward. A six-millimetre crossbolt enters an outboard gate lug. A fork-carried strip obstructs withdrawal of that bolt during transfer; an uninserted bolt also obstructs premature fork travel. Routing the lug on the opposite side of the drive avoids the earlier guide crossing. A local cassette bridge and receiver-port relief preserve represented connectivity and clear the sled bar. Their real stiffness and load margins remain unverified.

The receiver is now part of a connected, guided sled. Its entry dogs have8×6×8mm roots and retract12mm beneath the payload contact plane. Two three-millimetre crosspins engage the entry-frame stems at the open and closed positions. The pin-insertion and withdrawal phases are explicit. The fork front retracts65mm before withdrawal. The sequence then demonstrates80mm of captive sled translation and return **with the payload retained**. It does not simulate a launch, free separation, empty-sled return or complete reset after deployment.

![FM-02 prescribed handling states, projected from the actual STEP exchanges. The same axes and scale are used in each panel.](figures/step_sequence.png)

[Prescribed-pose animation](figures/prescribed_cycle.gif) · [Native 3U transfer assembly](cad/FM02_3U_transfer.FCStd) · [3U transfer STEP](cad/FM02_3U_transfer.step) · [1U transfer STEP](cad/FM02_1U_transfer.step)

The animation interpolates neither forces nor time. The complete native and exchange-file identities are recorded in `cad/NATIVE_CAD.json`; independent CadQuery/OpenCascade readback is in `cad/INDEPENDENT_STEP.json`.

## Clearance and mechanical holding

The sweep check establishes that each stipulated component movement is a translation by comparing endpoint solid overlap. Relative motion is then checked against the initial solid and the exact prisms of its boundary faces. This covers the prescribed continuous rigid translations rather than relying only on sampled frames. It uses a10⁻⁵mm³ penetration threshold and the declared kernel precision. It does not prove assembly constraint closure, finite clearance, flexibility, contact force or reliability.

The earlier closed fork crossmember crossed the tall receiver latch between sampled positions. Raising it produced new feed/capture crossings. An intermediate open U-frame cleared that rigid sequence but changed its stiffness. FM-02 instead uses the short underfloor latch and retains the closed fork frame. The superseded geometries and adverse results are preserved in Labs. No earlier failed check is presented as a pass.

![Genuine FreeCAD Qt/Coin view of the FM-02 3U transfer document. Blue denotes the passive payload envelope; orange identifies the represented gate and front barrier.](figures/FreeCAD_FM02_transfer.png)

![Native-CAD plan projection of the storage crossbolt, guide, gate wing and carried blocker. This is a projection, not a section or an approved drawing.](figures/interlock_plan.png)

The inserted receiver pins each obstruct a tested0.5mm movement away from either endpoint. The storage pin obstructs gate closure, and the carried strip obstructs a6mm withdrawal command at five transfer stations. These are rigid contact obstructions. Spring return, axial capture, release actuators, wear and actual force capacity are not implemented. If both receiver pins are withdrawn and a false close command is accepted, the dogs can strike a straddling payload. Both1U/3U counterexamples remain in `PHYSICAL_INTERLOCKS.json`.

## Drive candidate and equations

The earlier ACT-01 screen retains4,860 scenarios using three24V motor catalogues and the Thomson screw/nut reference. Its2/5/10s triangular strokes exceed the reviewed nut's established high-speed load domain. This is an unestablished rating, rather than proof of physical failure.

IDR-01 examines a different candidate: a FAULHABER32L...SB4.5:1 integrated geared ball screw with a3242...024BX4 motor and MC5005S CO ground controller. The actuator catalogue includes preloaded output bearings; it is available only with a mounted motor. A300mm screw option is considered because200mm screw length is not200mm usable travel. Reserving35.5mm for the nut envelope and15mm at each end leaves234.5mm nominal travel. Actual end limits and the longer screw's properties require supplier confirmation. This candidate is **not installed in the FM-02 CAD**, which retains the separate ACT-01 drive packaging.

The feed law is a quintic rest-to-rest translation:

$$x=s(10u^3-15u^4+6u^5),\qquad u=t/T.$$

It has zero endpoint velocity and acceleration, with finite jerk. The801-point torque calculation includes moving mass, imposed resistance, screw/gear efficiency bands, output drag and input-referred rotational inertia:

$$F=R+m\ddot x,\qquad \tau_m=\frac{{Fp}}{{2\pi i\eta_g\eta_s}}+\frac{{\tau_d}}{{i\eta_g}}+J\frac{{2\pi i}}{{p}}\ddot x.$$

Efficiencies below the catalogue maxima are study assumptions, not guaranteed lower bounds. The nominal reduction ratio is used. Controller/current-convention, encoder, wiring and closed-loop commissioning remain unverified. The motor's catalogue curve and continuous torque, actuator force/speed/power, and the same assumed resistance are screened together.

| Transfer duration [s] | Cases meeting declared ambient screens /243 |
|--:|--:|
"""
    + "".join(f"|{t}|{n}|\n" for t, n in bytime)
    + f"""

Independent polynomial extrema and piecewise absolute integrals reproduce all972 drive-screen decisions. Eighty refinement cases compare101–1601 samples. At801 samples, maximum relative peak-torque error is{convergence['max_801_torque_relative_error']:.3g} and input-energy-proxy error is{convergence['max_801_energy_relative_error']:.3g}. This checks the same equations by a different numerical method; it is not physical correlation or an external technical review.

![Drive numerical convergence against polynomial extrema and exact piecewise integrals. These errors do not include physical-model uncertainty.](figures/drive_convergence.png)

![Motor demand and a separate thermal sensitivity. Peak torque and speed are paired maxima; the actual screen checks the entire sampled trajectory. The thermal trace uses a60°C sink and an assumed50K/W housing path.](figures/drive_thermal.png)

The two-node thermal model reconstructs capacities from catalogue thermal constants. During each feed and equally loaded return it holds the maximum modeled electrical-input proxy at the winding. It is an upper heating envelope within that proxy model, not a bound on unknown PWM losses or an experimentally correlated motor model. Brake/controller/gear heating and radiation are absent. The candidate component temperature domains differ; no−40…80°C assembly compliance follows.

## Power loss, contact loads and tolerances

The compact BXR-LE candidate was rejected for moving-feeder stopping because its instruction manual limits it to holding. BXW-01-10L is a braking-use candidate. Its static torque is varied through assumed dynamic factors; its catalogue armature time is not treated as a complete application stopping time. It is not integrated into CAD or selected for flight.

For the direct-drive sensitivity, rotational inertia is reflected into an equivalent translational mass. During assumed delay, residual drive can accelerate the carriage; stopping work then balances the net brake force. Of576 cases,96 have no stopping solution because the assumed opposing brake torque does not exceed persistent drive torque;72 finite solutions exceed the proposed24mm travel allowance. A zero-drive slow-transfer subset has at most{brake['slow_zero_drive_max_runout_mm']:.3f}mm runout under these assumptions. Actual motor stall torque can exceed this brake's static rating, so a verified independent drive cutoff and an attached arrest load path remain necessary.

![Finite brake-runout sensitivities. The96 no-stop cases are retained in the data and are absent from finite-distance points. These are hypothetical dynamic torque/latency cases, not measured stopping results.](figures/stop_sensitivity.png)

Eighteen storage-pin load cases use actual modeled gate material volume,5/10/25g bands and0/50/200N additional actuator forces. A simply supported six-millimetre pin model supplies nominal bending, shear, bearing pressure and deflection. Steel stiffness is assumed; no alloy allowable, hole contact, bracket stiffness, impact or fatigue margin is approved.

The proposed datum basis is the sled mounting plane, launch-guide centreline and rear payload-stop datum. Local gap budgets retain manufacturing, angular, differential-thermal and unpredicted deflection bands. The0.2mm nominal storage-pin radial gap cannot absorb the common0.3mm manufacturing band. A correctly specified coaxial bore/reaming process is needed; widening functional holes alone is not an adequate correction.

![Local fit sensitivities. Boxes summarize a deterministic, unweighted study grid and are not confidence intervals. Nonpositive residuals are retained.](figures/fit_budget.png)

The represented feeder/sled material proxies, excluding payload, are{mass['configurations'][0]['without_payload_proxy_kg']:.3f}kg for1U and{mass['configurations'][1]['without_payload_proxy_kg']:.3f}kg for3U. Catalogue motor mass replaces its envelope density; other hardware uses declared homogeneous densities and simplified envelopes. Missing actuators, integrated drive/brake/controller, fasteners, wiring, launch locks and thermal hardware prevent an installed mass claim. Full proxy CG and tensors are in `METROLOGY.json`. These values must not be multiplied into a four/twelve-payload budget as if shared structures were resolved.

## Coupling to the mission timeline

FSR-01 reads the unchanged four/twelve VOLLEY-input FBR-01 schedules. An entire handling sequence is required to fit one zero-resultant-force coast,20s after a preceding release and10s before the next. Gate/bolt/receiver/front actuator speeds and verification times are explicit assumptions. Slow auxiliaries require103.0s; faster assumptions require74.5s. Four-release coasts fit both. Later twelve-release coasts provide92.182s, so the slow policy fails11 releases while the faster hypothesis fits. No actuator rating, carriage-indexing, attitude, initial-loading or recovery closure follows.

![Conditional twelve-release handling margins. The first preparation coast is longer. A positive bar is a scheduling allowance under stated actuator assumptions, not a demonstrated cycle.](figures/handling_margin.png)

## Engineering disposition

All seven feeder concepts remain unselected: captive lead screw, spring follower/two gates, rack/pawl, indexed drum/tray, segmented pantograph, telescope and belt/cable shuttle. FM-02 is a common custody/clearance research revision; IDR-01 is a ground-drive feasibility candidate. Neither supplies comparable installed hardware, complete contact/fault evidence and source-rated four/twelve-cell integration for every alternative. The safety-led trade cannot be closed by assigning a higher score to the most developed model.

The present record supports further ground-article design. It does not support a completed feeder, P-POD-like reliability, a rated launch speed or a flight-ready product. The decisive unclosed interfaces are pin axial retention and release actuation, the integrated drive/brake load path, actual toleranced joints, payload contact approval, loaded frame/contact analysis, complete deployment/reset, and installed multi-cell accommodation.

## Reproduction and source evidence

The standard-library checker verifies captured identities and independent mechanical identities:

```sh
python check_capture.py
```

The native builders require FreeCAD1.0/OpenCascade7.8; exchange readback uses CadQuery2.8/OpenCascade7.9. `SOFTWARE_LOCK.json` records the numerical environment. `MANIFEST.json` identifies the reviewed source, captures, logs and exports. Native CAD regeneration changes document metadata; exact release identities refer to the supplied files.

The Python numerical sequence is `integrated_drive.py`, `convergence.py`, `brake_review.py`, `fit_budget.py`, `controller.py` and `schedule.py`, followed by `plot.py` and `write_report.py`. Install the pinned `requirements-python.txt` for those calculations. In a Linux FreeCAD installation, run `build_native.py`, `check_sweeps.py`, `physical_interlocks.py`, `metrology.py` and `extract_views.py` with FreeCAD's Python libraries available. `check_step.py` uses the separately pinned CadQuery environment. `capture_native.py` and `build_drawings.py` require a real Qt display; they capture/export native application geometry. Regenerate the capture identities and manifest after a changed source or CAD file; a regenerated binary is not silently substituted into this reviewed snapshot.

Primary component references are the [FAULHABER motor catalogue](https://www.faulhaber.com/fileadmin/Import/Media/EN_3242_BX4_DFF.pdf), [32L SB catalogue](https://www.faulhaber.com/fileadmin/Import/Media/EN_32L_SB_FMM.pdf), [MC5005S catalogue](https://www.faulhaber.com/fileadmin/Import/Media/EN_MC5005S_DFF.pdf), [Thomson screw catalogue](https://www.thomsonlinear.com/downloads/screws/Neff_LeadScrews_bruk.pdf), [BXW-L manufacturer data](https://www.mikipulley.co.jp/en/electromagnetic-clutches-brakes/offbrakes/braking/bxw-l) and [BXR-LE instructions](https://www.mikipulley-us.com/documents/Manual/BXR-LE_Instruction_manual.pdf). Source editions, access failures and hashes are preserved in `SOURCES.json`. Manufacturer PDFs are cited rather than redistributed. Vacuum options do not establish an approved space assembly or preserve every standard-version rating.
"""
)
body = re.sub(r"(?<=\d)(?=(?:mm|kg|ms|rpm|N|s|g|°C|K/W)\b)", " ", body)
for word in [
    "for",
    "Both",
    "both",
    "The",
    "the",
    "with",
    "Of",
    "of",
    "require",
    "provide",
    "includes",
    "using",
    "at",
    "have",
    "and",
    "than",
    "force",
]:
    body = re.sub(r"\b" + word + r"(?=\d)", word + " ", body)
(H / "README.md").write_text(body)
header = '---\ntitle: "VOLLEY Gen6 — Feeder actuation and captive transfer"\ndate: "FM-02 / IDR-01 / FSR-01 · 20 October 2026"\ngeometry: margin=17mm\npapersize: a4\nfontsize: 10pt\nmainfont: DejaVu Sans\nheader-includes:\n - \\usepackage{placeins}\n - \\usepackage{graphicx}\n---\n\n'


def latex_figure(match):
    caption = match[1]
    for character in ["_", "%", "&", "#"]:
        caption = caption.replace(character, "\\" + character)
    return (
        "\\begin{figure}[htbp]\n\\centering\n\\includegraphics[width=\\linewidth,height=0.43\\textheight,keepaspectratio]{"
        + match[2]
        + "}\n\\caption{"
        + caption
        + "}\n\\end{figure}"
    )


pdfbody = re.sub(r"!\[([^\]]+)\]\(([^)]+)\)", latex_figure, body)
pdfbody = re.sub(r"\A# [^\n]+\n\n\*\*[^\n]+\*\*\n\n", "", pdfbody)
pdfbody = re.sub(r"(?m)^## ", lambda m: "\\FloatBarrier\n\n## ", pdfbody)
(H / "REPORT.md").write_text(header + pdfbody)
subprocess.run(
    [
        "pandoc",
        "REPORT.md",
        "--pdf-engine=xelatex",
        "-o",
        "FEEDER_ACTUATION_REVIEW.pdf",
        "-V",
        "colorlinks=true",
        "-V",
        "linkcolor=blue",
    ],
    cwd=H,
    check=True,
)
print("Captured-result README and review PDF built")
