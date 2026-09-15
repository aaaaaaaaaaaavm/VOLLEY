# VOLLEY

**Programmable spacecraft departure from a controlled orbital host.**

I started VOLLEY with a question: how much of a satellite's initial orbital distribution can be handled by the system that releases it, before the satellite has to carry propulsion of its own?

I am developing an approach to satellite deployment in which a host supplies coarse orbital placement and a release mechanism supplies an individual departure condition. The intended service is controlled separation velocity, direction and timing across one payload or a manifest. Keeping the spacecraft mechanically and electrically unmodified is VOLLEY's design objective; the interfaces still have to earn that claim.

**Computational engineering programme. Nothing has been built, fired, measured, qualified or flown.**

[Current work](docs/PROGRAMME_EXECUTION.md#working-on-now--next--blocked) · [Engineering evidence](docs/GEN5_CLOSURE.md) · [CAD](cad/README.md) · [Open problems](OPEN_PROBLEMS.md) · [Workstreams](docs/CONTINUITY.md)

![Allocation of responsibility between host, deployment system and spacecraft](docs/assets/departure_roles.svg)

*Functional allocation, not a selected vehicle layout. Host services require a mission-specific agreement; departure control remains a design objective.*

## The job I want it to do

A secondary spacecraft starts from the position and velocity its launch service delivers. Its separation mechanism adds another initial condition. I want to find the missions where controlling that condition more deliberately is worth the hardware, energy and operational burden.

That could mean distributing a batch more quickly, reaching different orbital-energy targets, reducing repeated host manoeuvres, or providing repeatable low-tip-off separation. It could also mean discovering that an ordinary dispenser and a better release sequence already do the job.

The comparison therefore includes conventional springs, release timing, host manoeuvres, cooperative spacecraft interfaces and payload propulsion where it serves the same mission. Programmability has to produce a useful difference against a competent baseline.

My longer-term interest is inexpensive, repeatable spacecraft that can be produced and replenished in batches: individual satellites, temporary groups and larger constellations. VOLLEY asks what initial mobility can be shared outside those spacecraft. A three-to-six-year operating life is a mission hypothesis to model, including disposal uncertainty; it is not a timer built into a separation impulse.

## Where the orbital work happens

The proposed sequence starts with the primary mission and a retained, controlled host. Subject to the mission rules, the host establishes the departure geometry, the deployment system releases a payload, and the host recovers its attitude and prepares the next event. Resource and disposal reserves belong in the campaign from the beginning.

The host supplies navigation, attitude authority and any orbital manoeuvres. VOLLEY supplies the relative release impulse and its mechanical interface. After separation, the spacecraft follows the resulting trajectory and whatever capabilities it carries itself. VOLLEY cannot provide continuing stationkeeping, collision avoidance or formation maintenance once contact ends.

Release changes velocity at the release position. It cannot, by itself, place a propulsion-less satellite into an arbitrary different circular orbit. Direction, timing, host state and acceptable terminal-state error matter alongside speed. An orbit plot showing a higher apogee is only one part of that problem.

An active upper stage is a possible host, and its manoeuvring capability is also an alternative to extra deployer speed. The [host compatibility study](docs/HOST_COMPATIBILITY.md) separates public information, assumptions and missing interfaces for Skyroot and Agnikul. Neither launcher is established as compatible. An 8 m vehicle structure is not automatically an available 8 m deployment path.

## How the machine has changed

The project began in April 2021. Its [lineage](docs/LINEAGE.md) records how the mechanism changed as calculations exposed the cost of earlier choices.

| Configuration | What I investigated | What the evidence now means |
|---|---|---|
| **Gen5: frozen electromagnetic baseline** | Ironless double-sided Halbach linear synchronous motor, reusable magnet sled, shared magazine, pulse supply, brake and return | A reproducible comparison case and the manuscript baseline. The mass comparison failed; substantial physical uncertainties remain. |
| **Existing Gen6: gas-driven investigation** | Direct gas expansion along an approximately 8 m stage-integrated guide, with a proposed trim function | A candidate with unresolved contact/release dynamics and host accommodation. Electromagnetic trim is suspended. |
| **Next Gen6 selection: open** | Compact controllable release, independent retained bays, banks and the shared magazine under common mission requirements | No mechanism has won. The existing gas guide remains in the comparison with its results and failures intact. |

<table>
<tr>
<td width="50%"><img src="cad/renders/gen5/hero_open.png" alt="Gen5 electromagnetic assembly with enclosure open"></td>
<td width="50%"><img src="cad/renders/gen6/hero_open.png" alt="Existing gas-driven Gen6 architecture study"></td>
</tr>
<tr><td><b>Gen5 geometry.</b> Frozen electromagnetic comparison.</td><td><b>Existing Gen6 geometry.</b> Investigated gas architecture; not the selected redesign or a manufacturing release.</td></tr>
</table>

The [generation index](docs/GENERATIONS.md) preserves earlier configurations. [BOLLEY](https://github.com/aaaaaaaaaaaavm/BOLLEY) investigates a separate bargain: accepting a cooperative passive spacecraft interface in exchange for different deployment machinery. Its interface mass, magnetic environment and qualification burden remain in its accounting.

## What the evidence says

At the frozen Gen5 model point, the release velocity is **16.029 m/s**, net electrical-to-payload efficiency is **18.8%**, and dry system mass is **126.6 kg**. These are calculated outputs of one configuration, not product specifications. The [baseline](docs/BASELINE.md) owns the complete ledger and assumptions.

The failures matter just as much. Gen5 loses its 3U dispenser mass comparison. The original claim of a unique constellation-phasing advantage did not survive comparison with release timing. Guide/contact studies exposed model-form and geometry defects, so nominal numerical consistency cannot establish a credible exit-state envelope.

The mission work has progressed through three bounded studies:

| Study | What it adds | What remains outside its result |
|---|---|---|
| [Departure-state trade](docs/DEPARTURE_TRADE.md), 210 cases | Finite host recoil and assumed release authority | Complete campaign and installed-system benefit |
| [Sequential campaign](docs/CAMPAIGN_ALLOCATION.md), 180 cases | Host propagation, remaining manifest mass and propellant allocation | Full position/velocity targets and useful constellation performance |
| [Terminal-state timing](docs/TERMINAL_TIMING.md), 300 cases | Identical terminal position/velocity targets and release-time search for one payload | Multi-payload optimization and a demonstrated interior timing optimum |

In one common-energy campaign, the 11.8, 16.029 and 29.009 m/s screens all avoid host corrections. That case gives no reason to choose the highest speed. The assumed speed intervals are not measured operating envelopes; the true minimum controllable release velocity is still unknown.

[PROVENANCE](docs/PROVENANCE.md), the [run sheets](validation/README.md) and [figure index](docs/FIGURE_INDEX.md) identify sources and limits. Cross-solver agreement is an independent numerical check, not an experiment.

## What I am designing next

My leading candidate is a compact release cell with its own retention and exit path, sharing services across the manifest where that makes sense. Independent bays may sacrifice some shared-machine mass efficiency while reducing the number of payloads exposed to one blocked path. Shared power and control can still create common failures; independence has to be demonstrated through the architecture.

I will compare controlled stored-energy pushers, short-stroke electromechanical pushers and gas-driven mechanisms under the same requirements. Payload arrangement and energy source are separate decisions. Captive-pusher arrest, pressure containment, peak electrical power, thermal recovery, tolerances and fault response must all be charged to the candidate that needs them.

The priority is the complete mission comparison, then installed mass, envelope, campaign resources and failure exposure. A selected design must show where it helps and where conventional deployment is sufficient. P92 and P113 remain open until their decision requirements are met.

Scaling will be an architecture family. Very small spacecraft are sensitive to adapter overhead; larger spacecraft bring stronger interfaces, distributed force application and larger host reaction demands. I will start from the existing 4 kg/3U reference, then compare adjacent sizes and 2-, 4- and 12-payload arrangements. Enlarging CAD does not establish scaling.

A programmable ground separation-test system is also worth investigating: a controlled push profile, an instrumented surrogate, and measured velocity, tip-off and repeatability. It could resolve useful release physics before a flight product exists, provided gravity and test-support effects are accounted for.

## From analysis to a justified test article

The next useful endpoint is a specific release cell that another engineering team can inspect and build: requirements, load paths, selected parts, tolerances, complete mass and energy budgets, controls, drawings, assembly and inspection instructions, and a calibrated test plan with acceptance criteria declared beforehand.

Small discriminating experiments belong early when friction or contact behaviour decides which architecture survives. A complete simulation record cannot substitute for those measurements.

The [prototype programme](docs/PROTOTYPE_READINESS.md) defines the thirteen work packages. [Programme execution](docs/PROGRAMME_EXECUTION.md) shows what is now, next and externally blocked. [Mission and redesign](docs/workstreams/MISSION_AND_REDESIGN.md) and [engineering closure](docs/workstreams/ENGINEERING_CLOSURE.md) separate the next architecture work from the inherited backlog; [continuity](docs/CONTINUITY.md) records how their evidence meets.

## Reproduce

Use Python 3.12 or newer and a full-history clone. The companion provenance check needs the
recorded export commit in the local history.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt -r requirements-dev.txt
bash tools/verify_all.sh
```

Run from a clean committed checkout. The command checks repository consistency and the numerical
checks it lists; it does not rerun every external solver or certify the design. Missing checks
must remain visible. CAD and external solver setup are described in [CONTRIBUTING.md](docs/CONTRIBUTING.md)
and [tools/env-setup.sh](tools/env-setup.sh).

## The programme

| Repository | Role |
|---|---|
| **VOLLEY** | Flagship engineering record and unmodified-payload design objective |
| [BOLLEY](https://github.com/aaaaaaaaaaaavm/BOLLEY) | Sister project: passive spacecraft interfaces in exchange for different launcher machinery |
| [VOLLEY-paper](https://github.com/aaaaaaaaaaaavm/VOLLEY-paper) | Authored Gen5 manuscript and exported reproducibility evidence |
| [VOLLEY-thesis](https://github.com/aaaaaaaaaaaavm/VOLLEY-thesis) | Gen5 submission material and exported evidence |
| [VOLLEY-lab](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab) | Stopped alternatives and the conditions for reopening them |

The long-form account previously on this page remains in
[the preceding revision](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/67939b7cbef9e2414226f683ebc12f2b6bf01088/README.md).
It is a historical snapshot; the current evidence routes above govern present claims.

## Author and use

**Adityavardhan Mishra** · Mechanical Engineering, Symbiosis Institute of Technology, Pune.
Project begun April 2021. [adityavardhanmishr@gmail.com](mailto:adityavardhanmishr@gmail.com)

I welcome independent reproduction, design review and prototype collaboration. Please identify
the configuration and run when reporting a discrepancy.

[CC BY 4.0](LICENSE). See [NOTICE](NOTICE), [LICENSING.md](LICENSING.md) and [CITATION.cff](CITATION.cff)
for attribution and scope. Historical snapshots retain the terms under which they were released.
