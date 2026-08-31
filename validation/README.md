# Validation plan

Independent cross-checks of the claims in `analysis/`. **73 run sheets, one row each, and every
file in this directory has a row.** All but the last have run; A73 is declared and executing.

> ### This index was nineteen rows short until 2026-08-30, and said so nowhere
>
> It opened by describing *"nineteen of the twenty-one below"* while the directory held 73 files.
> Fifteen run sheets written between A15 and A34 and every run from A66 onward were absent, so a
> reader taking this page as the index of the validation work would have missed A72's finding
> entirely. Nothing checked the table against the directory; the counts gate checks how many run
> sheets exist and never checked whether they were listed.
>
> The missing rows are added below and the header now states a number that can be recomputed from
> `ls`. The rows for A15 and A28 to A34 were written from those run sheets' own Result headings on
> the day the gap was found, seventeen days after the last of them ran, and they are shorter than
> the rows written at the time.

## Why it exists

This directory was written when `PROVENANCE.md` could point at only two cross-checks, the
Halbach field (analytic vs magpylib) and orbital decay (orbit-averaged vs Cowell RK4), both
internal, and the field one analytic-against-analytic, so not confirmation by a different
physical method (`OPEN_PROBLEMS.md` E2).

That has changed, and not uniformly in the project's favour. A1 put a meshed PDE solve
against K<sub>t</sub> and agreed to 0.03 % after correcting shared quadrature. A4 put CalculiX against the chassis and it passed.
A12 put two independent numerical methods against the array attraction and found the published
value 37 % high. And A5 failed: an independent propagator falsified an invariance claim
that was in the paper's own abstract.

What has still never happened is a measurement. Every row below is one model against
another model (E4). Each analysis closes a specific named item.

| # | Analysis | Tool | Closes | Status |
|---|---|---|---|---|
| A1 | Airgap field, 2-D magnetostatic | scikit-fem + gmsh (FEMM substituted) | E1 (2-D half), E2 (partly) | RUN 2026-07-29, verdict PARTIAL: K<sub>t</sub> agrees to 0.03 % after correcting shared quadrature, two bands missed with causes (P20, P21) |
| A4 | Sled chassis structural | CalculiX ccx 2.21 | P5, P8 | RUN 2026-07-28: as-drawn plate passes all three bands |
| A5 | Orbital lifetime and seeding | GMAT R2022a | E6, hardens x1.80 | RUN, verdict FAIL on invariance. See [`../docs/RESULTS.md`](../docs/RESULTS.md) |
| A9 | Decay rate against flown CubeSats (TLE history) | Space-Track + numpy | E6, against reality rather than another model | NOT RUN, blocked by network policy here and re-tested 2026-07-31. Candidate objects now shortlisted in the sheet, so this is an afternoon elsewhere |
| A6 | Conjunction probability | scipy 2-D Pc (CARA substituted) | P1, not closed | CORRECTED 2026-08-03: fixed-shape claim retracted; current slab bound 4.4e-5, two of five bands, three VOID, P1 open |
| A7 | Separation and tip-off | Project Chrono | E7-adjacent | SUPERSEDED 2026-08-20 by [A23](A23_tipoff_release.md) and [A34](A34_cradle_restitution.md), which answered it, ideal release 0 °/s, skew tolerance 50.6 µs, and the cradle rattle settles in 27.25 ms of a 146.4 ms stroke leaving *exactly zero* residual rate. A7 itself stays correctly unrun. A7-R RUN 2026-08-05 instead: Chrono is unavailable and the release mechanism is undefined, so the tolerance was computed rather than the rate, the full push may act unbalanced for only 50.7 µs before the 2 °/s band breaks |
| A8 | Pulse-power chain | ngspice / PySpice | E17 | RERUN 2026-08-05 as A8-R2 at the corrected point: six of six bands, exit velocity agrees to 0.016 % |
| A10 | Shot against a realistic bank ESR | `motor_model.shot()` | nothing; opened P26 | RERUN 2026-08-03: hard ceiling 68 mohm, five of six bands, one VOID |
| A11 | Regenerative recovery of sled energy | `motor_model.regen_brake()` | nothing; asks what R5 did not | RERUN 2026-08-03: 291.4 J recovered, eight of eight bands. Superseded as a current figure: that run integrated over the 240 mm section [ADR-030](../docs/adr/030-apply-the-depth-resolved-thrust-constant.md) removed. At the 39 mm that survives, recovery is 47.0 J, 3.9 % of the sled's energy (P97) |
| A12 | Inter-array attraction, two numerical methods | magpylib + surface Maxwell stress | P17 | CORRECTED 2026-08-03: extended stress plane 2680.0 N vs 2686.6 N volume force; five of five bands |
| A13 | Indexing and sled-return attitude disturbance | momentum bookkeeping | E24 | CORRECTED 2026-08-03: transient-rate rows 3/4 FAIL, row 7 VOID; ideal residual rate is zero and the cadence conclusion is superseded |
| A14 | EMI scoping: payload coupling and comms | `drive_electrical` + magpylib | advances E12; opened P34 | RUN 2026-08-05, verdict PARTIAL: six of eight bands, band 4 FAIL at 611x, band 5 VOID. The dominant term is the static magnet field, not the drive |
| A16 | Gen4 finite-stator thrust vs sled station | magpylib | E27 | RUN 2026-08-05: full-overlap thrust reproduces `F_cmd` to 0.000 %; Gen4 reaches 13.390 m/s, 81.7 % of Phase I, an upper bound |
| A17 | Ripple chirp through the track modes | scipy SDOF | E23; opened P36 | RUN 2026-08-05, verdict FAIL: 8.18x amplification at the fundamental crossing of the 109 Hz mode, and Q is not the variable that saves it |
| A18 | Brake, magnet eddy, fin transient, launch restraint, standoff | numpy + Miles | E20, E19, E26, E22, and E10's analysis half; opened P37 | RUN 2026-08-06: E19/E26/E22 pass, E20 passes only for a 0.4-0.5 T pole field, E10 FAILS at every Q |
| A20 | Reachable orbit envelope vs host Δv budget | numpy + `astro.py` | nothing; quantifies ADR-024, advances PII-6 | RUN 2026-08-10, verdict band 1 FAIL: the band named a two-burn Hohmann and its limit was computed for one burn. Band 3 caught a sign bug in the script. Host supplies 56 % of the altitude extent at 100 m/s |
| A21 | VOLLEY against springs, drag and cold gas, identical axes | numpy + `astro.py` | nothing; replaces the headline ratio | RUN 2026-08-10: seven of seven. 7.52x the lifetime extension of the fastest spring against 6.56x on velocity; mass parity at 1.062; cold gas wins at 3U by 7.5x, declared as a loss in advance. RE-RUN 2026-08-14 at the corrected operating point (P53): still seven of seven, at 7.33x, 6.41x, parity 1.062 and 8.3x |
| A22 | Retention gate resize against the random-vibration case | numpy + `phase1_closeout.e10` | P37, E10's analysis half | RUN 2026-08-10: six of six. 2 x D6 to 2 x D9 takes the margin at Q = 30 from −0.36 to +0.45 and keeps it positive across Q = 10-30, for 11 g |
| A23 | Tip-off at release, modelled rather than bounded | numpy rigid body | advances E7; opened P41 | RUN 2026-08-10: release is comfortable, it happens 12.2 ms into coast at zero force. The payload arrives in its cradle at 36-231 °/s, 18-115x the band, and nothing had modelled it |
| A24 | The payload ladder as a fixed-cell design, not a volume ratio | numpy + `payload_family.py` | ADR-025; opened P44 | RUN 2026-08-10: five of six, band 6 FAIL. 1U no longer closes kill criterion 1 (36/load, 2.125 kg, not 40/1.913); ThinSat and 12U do not fit at all, the 166 mm cassette width is a constraint written nowhere else. Band 6 missed at 0.508 % against 0.5 %: 720 ChipSats need 7.19 kg of shim hardware for 3.6 kg of payload |
| A25 | A flywheel energy store against P26 | numpy + `motor_model.py` | targets P26; opened P45 | RUN 2026-08-10: five of six, band 4 FAIL by 1.1 kg. Band 6, the point of the exercise, passes decisively: 35 mΩ against A10's 68 mΩ ceiling, 66 kW deliverable against 32.5 required. Needs no architecture change. Mass parity, not saving; the miss turns on one unsourced machine specific-mass figure |
| A2 | The 3-D field, and the depth assumption inside K<sub>t</sub> | numpy + magpylib | closes E1's 3-D half; opened P46 | RUN 2026-08-10: four of four run, band 4 (getdp FEM) NOT RUN so E2 stays open. The field was never 2-D, the *thrust integral* was. Resolving depth costs 4.42 % of K<sub>t</sub> (10.5386 to 10.5386), v_exit 16.029 to 16.029. Baseline not changed; computed and held. Band 1 caught a 57 % normalisation bug in the analysis; band 3 was badly chosen and measures numerical cancellation at 10⁻²⁰ T |
| A27 | Why a linear motor, and not a screw, rack or spring | numpy + `motor_model.py` | answers review item 18 | RUN 2026-08-10: screw disqualified by kinematics (49,164 rpm; DN 8.2x over, critical speed 37x under); rack fails on vacuum contact at 16.0 m/s; a ~1.8 kg spring works at 21.1 g and fails only on commandability. The motor is chosen for commandability, not performance |
| A35 | Every kilogram attributed to the requirement that causes it | `mass_properties.py`, no new physics | nothing; quantifies whether kill criterion 1 is reachable at all | RUN 2026-08-14: seven of seven. Energy arriving during the shot is the largest single driver at 28.1 %; an unmodified satellite costs nothing, which calibrates against the sibling repository's negative result. The lattice saturates at 29.94 %: 88.67 kg survives every deletion in every combination, 7.39 kg per satellite, so no architecture change closes kill criterion 1. *(The run sheet still prints the pre-A46 49.23 kg / 4.10 kg pair, P95.)* The prediction of >40 % for the pulse alone was wrong |
| A36 | Magazine density, the only lever A35 left on kill criterion 1 | numpy-free, `constraint_ledger.py` | opened P59 | RUN 2026-08-14: six of seven, band 4 FAIL. The N to ∞ limit is a healthy 0.954 kg/satellite, but 2.0 kg is first reached at N = 116, which no factorisation packages inside the track length. Largest that fits is N = 126 at 1.941 kg/sat on a 244.6 kg machine, 42-hour campaign. At N = 24 it is 4.330 kg, not the 2.05 estimated from A35 by naive division |
| A37 | The stage as the deployer, and A35's falsification test | numpy-free, `constraint_ledger.py` | advances P59; opened P60 | RUN 2026-08-14: six of eight, bands 4 and 8 FAIL. Of 126.56 kg, 29.75 is deleted by Gen6 physics, 43.33 is stage structure and 11.45 kg is added, all of it containment. Added mass per satellite is 1.608 kg on a small kick-stage class, so kill criterion 1 closes at 3U, with dry mass per satellite still crossing at 7.044 and both reported together. The store scales as v² and reaches 78.5 % of added mass at 8 m, so the binding constraint moves from mass to energy storage |
| A38 | Does A34's cradle closure survive the Gen6 operating point? | numpy-free, imports `cradle_restitution.py` | advances kill criterion 4; opened P61 | RUN 2026-08-14: five of six, band 1 FAIL. At 2.4x the offset moment the closure improves, settling 17.69 ms of 133.3 against 27.88 of 150.1, critical restitution 0.9462, residual still exactly zero. Tip-off's ceiling is 30.9 g, above the 25 g cap, so it does not bind and A37's window stands. Cost is preload, 81 to 202 N per contact. Band 1 caught A34's recorded figures being stale by 2.3 % against its own script |
| A39 | The energy store at metre-scale strokes | numpy-free | closed P60; settles A35's falsifier | RUN 2026-08-14: seven of seven. At 32.7 m/s a steel spring is 11.41 kg and busts the budget at 34.3 m/s; cold gas is 2.98 kg and busts it at 89.4, on a 1.71 L bottle for all twelve shots. Not energy density, a spring must be cocked twelve times and gas does not. A35's falsifier passes: 2.98 kg against 14.26. The binding constraint on velocity moves from mass to stroke length |
| A40 | The blowdown transient, and how velocity is commanded | numpy-free | opened P63; amends ADR-032 | RUN 2026-08-14: three of eight, bands 1, 3, 6, 7, 8 FAIL. A fixed orifice cannot hold force over a 2.18 m stroke, 4.7 g mean delivered against 25 needed, 14.16 m/s against a 30 m/s band. Flow area was never the problem (0.71 mm against a 10 mm limit); a fixed area cannot track a growing volume. A39's 2.98 kg assumed a regulator it never named. What survives: one 1.71 L bottle does run twelve shots at 4.5 % droop. Band 1 was a declaration error and is recorded as one |
| A41 | The pre-charged chamber: charge slowly, fire as a closed expansion | numpy-free | closed P63; specifies Gen6's store | RUN 2026-08-14: eight of eight. A 2 L chamber at 50 bar gives 30.54 m/s at 25 g on a 4.66 kg store, no regulator, no flow-rate problem. Added mass per satellite 1.343 kg against A37's 1.608, at a higher velocity. Velocity commanded by charge pressure at 0.499 % per 1 % against valve timing at 10.53 % per ms. All three stated predictions were wrong, on a run where every band passed |
| A42 | The fill window, and the gas a bottle cannot give back | numpy-free | opened P64; answers ADR-032's falsifier | RUN 2026-08-14: five of six, band 3 FAIL. Filling is 4.14 s through a 1 mm orifice and is not the constraint. A41's 6 L bottle runs out at shot seven of twelve, below the charge pressure it cannot fill a 50 bar chamber. Correction is bounded: 7.65 L isothermal, 11.25 L adiabatic, added mass per satellite 1.344-1.455 kg. The first prediction written before its run that held |
| A15 | A twelve-satellite campaign from POEM, propagated in GMAT | GMAT 2022a | P31, and it falsified an invariance claim in the paper's own abstract | RUN 2026-08-06, three cases. Band 4's prediction was wrong by 28x and band 6's coarse number by 5.7x, both corrected in place with the wrong values kept. R3 reaches 0.7315 deg against a 0.75 deg limit. P16's lifetime invariance is withdrawn and the ratio is quoted at a stated activity level |
| A21-R | Release timing as the free baseline for phase, and what survives it | numpy-free | reads A21's comparator claim against a baseline it never set | RUN 2026-08-14: six of six. *The published claim does not survive; the design does.* Phase separation is available from release timing alone, so the schedulability argument stands and the differential-velocity argument as published does not |
| A28 | The velocity loop, designed and tested for stability rather than assumed | python-control | P47, and it is why ADR-027 exists | RUN 2026-08-13: **four of six bands fail, and the published gain is unstable.** Bands 2, 3 and 5 were flagged in advance as able to fail and did, and band 4 failed unflagged. The loop is redesigned against margins rather than tuned |
| A29 | What air costs a ground test of exit velocity | OpenFOAM | the ground-test plan, before it is written rather than after | RUN 2026-08-13: the correction is 5.1 mm/s and two bands fail. Bands 3 and 4 point in opposite directions on tunnel size, which is the useful result: the test is not free and it is not impossible |
| A30 | Can an induction drive couple to what the satellite already has | numpy-free | PII-16, and rejects it | RUN 2026-08-13: **the rail is 22x too narrow and the drive is fine.** The entry criterion for PII-16 is not met at any pole pitch, so the architecture is rejected on geometry rather than on electromagnetics. Band 2 caught a bug in this analysis, which is why band 2 was declared |
| A31 | Does the plate stay in the gap | numpy-free | the plate drive's alignment question | RUN 2026-08-13: **it centres itself, and A30's thrust was 4.4x optimistic.** The restoring behaviour is decisive in the plate drive's favour and the thrust figure that motivated it is not |
| A32 | The entry transient and segment handover | numpy-free | the last band with a plausible chance of killing the plate drive | RUN 2026-08-13: **entry is a non-event; the segment joint is not.** Two independent models agree on entry. The handover across a segment boundary is where the remaining risk sits |
| A33 | The track's dynamic case | numpy-free | P36 | RUN 2026-08-13: six of six, and A17 was not underestimating. Band 3 is a negative result and is reported as one |
| A34 | Does the rattle settle before release | numpy-free | kill criterion 4 | RUN 2026-08-13: **it settles in 27 ms of a 146 ms stroke and leaves at zero.** The band was declared as able to fail and a failure would have been a design result; it passed |
| A45-R | The stage credit, re-read after the enclosure was itemised | numpy-free | re-reads A45 | RUN 2026-08-16: four of eight. Itemising the enclosure did not rescue the credit |
| A66 | What the drive tube costs the trim stator | numpy-free | P92, and opens P117 and P118 | RUN 2026-08-30: bands 1R, 4, 5 and 6 pass, 3 fails. The wall is 0.314 skin depths and still takes 19 % of the field, because the sheet magnetic Reynolds number decides it and the tube never moves. Band 1 as first declared could not have been passed by correct code and is withdrawn under ADR-037, with the failed run preserved at `af526a0`. The run then found that the wall takes more force than the stator makes above an air-gap field of 0.1500 T |
| A67 | The payload's guided contact state through the 8 m bore | numpy + scipy | P103, P108 | RUN 2026-08-22: six of nine. Bands 3, 5 and 7 fail and band 5 is the result: Gen6 misses the tip-off band by 7.4x |
| A68 | The contact law, verified, and the model-form uncertainty it carries | numpy-free | the contact law A67 assumed | RUN 2026-08-22: six of seven. Band 6 fails and it is the result: the model-form spread is 65.8 %. P111 corrected an attribution this run made to a paper that does not contain the relation |
| A69 | What shape the 8 m drive tube is actually in | scikit-fem | the centreline A67 assumed straight | RUN 2026-08-22: eight of eight. At 0 g the tube's own weight contributes exactly zero and thermal bow dominates. P110 later corrected the centreline itself, and P115 the conditioning of the solve behind it |
| A70 | Guided contact on a derived centreline and a verified contact law | numpy + scipy | re-runs A67 on A69's shape | RUN 2026-08-22: two of six pass and four are NOT EVALUABLE. *That is not a pass and it is not reported as one.* P110 then found the committed results file still holding the superseded numbers, which is why the freshness gate exists |
| A71 | A numerically converged guided-contact solution | numpy + scipy | the convergence A70 could not show | RUN 2026-08-22: two pass, three fail, three not evaluable. *The run did not converge, and that is the finding rather than a reason to withhold it* |
| A72 | How long a magnet array the shot can afford to carry | numpy-free, importing `precharged` and `tube_shielding` | the closable half of P118 | RUN 2026-08-30: bands 1 and 5 pass, 3R and 4R fail at every field by 6.8x to 44.7x. Bands 3 and 4 as first declared could not discriminate and were withdrawn **before the script existed**, which is ADR-037's rule applied early rather than late. At the array length the trim force needs, the eddy drag takes 71 % of shot work and the carriage leaves an 8.0 m tube at 0.47 to 3.30 m/s against an adopted 29.01 |
| A73 | The trim secondary derived for the annulus it is actually drawn as | magpylib, through `motor_model`'s own Lorentz integral | P117 | RUN 2026-08-30: band 1 passes on all three clauses, bands 3, 4 and 5 fail. The generalised integral reproduces `motor_model`'s own 10.5386 N per kA/m with a relative difference of exactly zero, and the curved model reproduces a flat array to 0.463 % at twenty wavelengths of radius. The section as drawn makes **56.91 N against the 948.0 N in `cad/parameters.json`**, 6.00 %, short by 16.7x -- 4.02x of it the interaction surface and 4.14x the fact that Gen5's winding lies between two arrays while Gen6's lies entirely outside one. Reaching 948.0 N needs 2399 mm of array against a 12.0 mm drawn piston |

| A43 | Does the reservoir warm back up between shots? | numpy-free | opened P66; sizes Gen6's reservoir | RUN 2026-08-16: seven of eight. Conduction through stagnant nitrogen gives a 17 460 s time constant against a 1200 s cadence, so the bottle does not warm back up and the no-relaxation figure is the physically right end, not merely the conservative one. 9.55 L; conduction estimate 8.95 L, isothermal limit 8.25 L. A42's 7.65 and 11.25 L are superseded |
| A44 | What Gen6's open-loop shot actually disperses to | numpy-free | drives ADR-033. *Superseded at ADR-034's stroke by [A55](A55_trim_authority.md): 3.9798 %. The result below is A44's own 2.18 m machine and reproduces exactly, `STROKE_A44` is frozen in the script* | RUN 2026-08-16: six of eight. 3σ of 1.113 % against Gen5's 0.0274 m/s, and 93.4 % of the variance is seal friction (P67). A fivefold better pressure transducer moves it 0.008 %, there is no instrumentation route to the product's central claim |
| A45-R2 | The stage credit at the store A56 actually sized | numpy-free | P68 stays CRITICAL; re-tests ADR-032 falsifier 1 | RUN 2026-08-20: four of eight, all five predictions held. A45 and A45-R both read the store as A43's 5.38 kg; A56 sized it at 3.1216. The allowance moves for the first time, break-even 8.4 % to 11.0 %, against ADR-032's declared 30 %. Full credit 1.4027 to 1.2145 kg/sat, hostile 3.2709 to 3.0827. *A 42 % lighter store moved the hostile reading 5.7 %: the store is not what is wrong with the mass case.* Band 8 found the project publishing three figures for one quantity, 1.403, 1.296 and 1.324, from three different stores, and names 1.2145 kg/sat canonical |
| A45 | What the stage credit is actually worth | numpy-free | opened P68; fires ADR-032's first falsifier | RUN 2026-08-16: five of eight. Break-even at 8.4 % of the credit, and 58.6 % of it is a skin on a vehicle nobody has agreed to lend. Added mass per satellite reads 1.403 to 3.271 kg depending on how hostilely the credit is read, and both ends are published everywhere |
| A46 | The enclosure, built up from the geometry instead of assumed | numpy-free | replaced P10's placeholder | RUN 2026-08-16: five of eight. 50.04 kg where an 8.00 kg placeholder stood, skins 32.82, frames 8.20, radiator 2.59, bay boxes 1.87, fasteners 4.55. Five derived lines, each tracing to a dimension in `parameters.json`. 42 kg, not the 20 the warning guessed at |
| A47 | Gen6's FMEA, against Gen5's and against a spring | numpy-free | quantifies E30 | RUN 2026-08-16: eight of eight. The architecture change buys +0.37 satellites at *r* = 0.99; a per-cell backup ejector buys +2.27, six times more, because it makes the drive satellite-forfeiting rather than manifest-forfeiting. Eight shared elements must survive every shot |
| A48 | The trim stage: how much correction, at what mass | numpy-free | adopted as ADR-033; opened P77 | RUN 2026-08-16: seven of eight. 37.7 J, 2.021 % of the shot, over 39.7 mm, for 0.340 kg. The precision Gen6 traded is recoverable. Band 5 was a declaration error, recorded as P76. The pulse store that feeds it is not weighed |
| A49 | The velocity, acceleration and stroke surface | numpy-free | adopted as ADR-034; opened P78 | RUN 2026-08-16: seven of nine. 14 points of 63 beat Gen6 on velocity, peak g and gas at once, every one of them at L = 8.0 m. Band 3 confirmed peak acceleration is independent of stroke, so stroke is an exchange rate rather than a performance knob. Band 6 failed: friction's share rises 9.75 % to 12.90 % across the sweep and 28.39 % at the chosen point |
| A50 | The campaign, with altitude as the free variable | numpy-free | opened P79; E28 stays open | RUN 2026-08-16: seven of nine. Satellite life 476.6 days at 450 km; three 50 km shells cost ~ 55 m/s. The 90-day plane spread moves 47.1° to 44.6° across 350-450 km while life changes 6.7x, so E28's central trade is not one, go higher. Band 1 failed: the static atmosphere gives 70.6 d at 350 km against E28's observed 29-36 |
| A51 | Power and efficiency, end to end at Gen6 | numpy-free | opened P80 | RUN 2026-08-16: seven of eight. 311.76 J/shot, ~0.26 W average, 36 W peak. Band 7 traced the repeatedly quoted "25-131 W" to `host_integrated.py`'s spring-winding figure, Gen6 has no spring and its reservoir is ground-filled. Corrected in seven files |
| A52 | Recoil and angular impulse at Gen6 | numpy-free | answers E29 | RUN 2026-08-16: seven of seven. 116.03 N·s per shot, 1.81x Gen5, 1407.9 N·s over the campaign, 0.653 kg of propellant to null. The interface requirement follows: the thrust line must pass within 10.7 mm of the host centre of mass, against Gen5's 19.5 mm |
| A53 | The per-cell backup ejector, designed rather than priced | numpy-free | opened P81 | RUN 2026-08-16: seven of eight. Band 7 fails by 40.4x: the ejector stores 4.5 J and clearing the 2.18 m sealed tube costs 181.8 J. Sized to clear, 8.713 kg, 2.129 kg per satellite, over the threshold. The failure is architectural, not conceptual; ADR-034's 8.0 m stroke makes it 148x |
| A56 | The reservoir at the charge pressure ADR-034 adopted | numpy-free | closed P82, opened P87; sizes the store | RUN 2026-08-19: eight of nine. 3.460 L and a 3.1216 kg store, against A43's 9.550 L and 5.3804 at 50 bar. The bottle falls 63.8 % where the gas falls 54.55 %, a lower target pressure lets it be drawn further down, a nonlinearity nobody had claimed. So ADR-034's 4.10 kg scaled estimate was pessimistic: a sized store comes in 24 % below it and falsifier 2 does not fire. A43's finding survives at 7.39x the cadence where it was 14.55x. Band 7 failed: the last fill takes 11.516 s against a 10 s window, and it fails at A43's point too, A42's 4.14 s is the *first* fill. P87 |
| A57 | Attitude rate and packaging on the stage, Gen6 | `stage_attitude.py`, importing A13's corrected model rather than reimplementing it | closes both remaining NEEDS SOURCE rows in `KILL_CRITERIA.md` | RUN 2026-08-22: seven of eight. Band 6 fails as declared, the rail is 200 mm over A37's usable acceleration length, and band 7 prices it at 1.2579 % of exit velocity. Attitude offset 0.1747° per shot at 300 kg, 2.33x Gen5's: deleting the mover increased it. Band 5 reported a momentum and refused a margin, and the script parses its own AST to prove it never reads a control authority (P94). Opened P99 and P100 |
| A65 | The per-cell ejector, re-asked against pyrotechnic gas generation | numpy-free | reopens P81, which A53 closed as architectural; opens P91 | RUN 2026-08-20: nine of ten. A53 failed band 7 by 148x because a spring stores 4.5 J and clearing the 8.0 m tube costs 667.2 J. A gas generator of the automotive restraint class delivers 2331.6 J at the smallest charge in the published range, after cooling to the tube's own 473 K ceiling, 3.49x. And the mass argument inverts: A53's tube-clearing spring re-crossed the kill criterion at 2.129 kg/sat; this is 1.6496, and A47 still returns 9.261 satellites. Band 4 misses A53's inherited 0.25 kg per-cell threshold at 0.4350 kg, 46.6 % of it a minimum-gauge steel plenum, not the pyrotechnic parts (P91). *A53 closed it as architectural; it was a store choice, which is A54's mistake exactly* |
| A64 | The pulse store, priced against pulsed-power capacitor technology | numpy-free | closed P86; answers ADR-033 falsifier 1 | RUN 2026-08-20: six of six. A54 named the gap as NEEDS SOURCE and this run fills it from published pulsed-power literature, 2000-2680 J/kg, metallised polypropylene. The constraint flips from power to energy: an EDLC must hold 723x the energy it delivers just to source the current; a pulse capacitor holds 1.00x. The store is 51-72 g against A54's 23-37 kg, 522x lighter, at 400 kW/kg against the 23.20 required. *A54 was correct in every calculation and wrong in its scope: it priced the only technology this repository had data for* |
| A63 | The steam design surface, which is the run A62 should have been | numpy-free | answers P90; corrects A62 | RUN 2026-08-20: eight of ten. A62's seal failure is corrected, 43 of 108 points sit inside filled PTFE's limit, so A61's specification survives steam. A62's aluminium failure is not, zero points reach 473 K, so the tube is steel at every steam design point. And that settles it: the steel penalty is 2.154 kg, larger than everything steam removes, giving −1.813 kg at the best point and 0 of 43 a saving. *The correction made it worse than A62 found, because a chamber chosen for steam is larger.* Conditional: if P85 chooses steel for reasons independent of the fluid, steam becomes +0.341 kg, a wash |
| A62 | Steam, with the water heated by being in space | numpy-free | screens a heated working fluid, which A39's trade never considered | RUN 2026-08-20: seven of ten. The heating works, 41.5 W, α/ε >= 7.6 inside the selective-coating class with no concentrator, a 23 cm square absorber, and it survives eclipse. The fluid is better, 101.98 % of nitrogen's work on 35.1 % of the charge mass, and the 200 bar COPV goes. Then the dryness requirement sets 550 K, which exceeds aluminium's 473 and filled PTFE's 533: the tube is forced to steel for −2.154 kg against a +0.869 kg store saving, net −1.285 kg before any absorber mass, and A61's 17.8 N seal specification, one day old, does not survive it |
| A61 | What the design requires of a seal, which it has never said | numpy-free | opened P89; specifies the seal | RUN 2026-08-20: six of nine. Inverts A41's open question and returns a specification: 17.8 N, 4.00 % of the piston pressure force, with the thermal case binding, not the control case (band 6). A41's allowance is 18.71 %, inside the elastomer O-ring range, so the project has been sized against the worst common class and nobody chose it. At 5.00 % the dispersion falls 3.980 to 0.905 % and the trim stage becomes unnecessary, deleting P86's requirement rather than meeting it. Band 5 found no friction makes the store affordable, 4.23 kg even at 1 %, confirming it is power-limited. The 16 mm stock bore is free: 0.00 % shift |
| A54 | Weighing the pulse chain ADR-033 named as its own falsifier | numpy-free | closed P77, opened P86; fires ADR-033 falsifier 1 | RUN 2026-08-19: one of eight. The trim stage asks for 93.3 % of the peak power and 93.3 % of the peak current of the whole chain ADR-032 deleted, the energy fell twenty times and the current fell seven percent, which is ADR-033's own sentence measured. An EDLC store sized from A10's ESR x C bracket weighs 23.44-37.36 kg against the 1.2328 kg section it feeds, holding 723-1152x the energy needed. No sheet current rescues it: the trade bottoms out at 10.755 kg. What it proves is narrower than impossible, any store that fits must deliver 23.2 kW/kg against Gen5's 4.72. Switch and conductors unpriced, so every mass is a lower bound |
| A55 | The dispersion and the trim authority, at the stroke ADR-034 adopted | numpy-free | closed P83 and P84; resized ADR-033 | RUN 2026-08-19: four of nine. Band 1 reproduced A44 to four decimals, and caught a bug in this run's own script first, a 200 bar full scale where A44 uses a fixed 50. At the adopted stroke 3σ goes 1.113 % to 3.980 % and the seal owns 98.7 % of the variance, so A48's section is 3.57x under-authority and resizes 39.7 to 144.01 mm, 0.340 to 1.2328 kg. Added mass per satellite 1.3987 kg, threshold unmoved. ADR-033's falsifier is not aggravated: peak power moves 2.8 %, because the section gets longer rather than harder to drive |
| A58 | The chamber, the tube and the seal across a campaign | numpy-free | opened P88, extended P85 | RUN 2026-08-19: six of eight. The bulk thermal case is comfortable, the tube warms 5-8 K over a campaign, the chamber recovers with a 7 s time constant against a 1200 s cadence, and the gas ends 135 K above condensation. The problem is the seal: 667.2 J arrives in it in five milliseconds at 2419 W, and a 2 g seal must shed 77.52 % of that during the stroke to stay within 50 K, a requirement on a component that exists in no file. Band 6 failed at 10.79 µm of differential clearance, which matching the two materials removes for free. Band 7 passed on a test declared wrong: it compared a definite input against an upper bound, and the sign of the net thermal load is undetermined |
| A59 | The drive tube as a beam, a column and a pressure vessel | numpy-free | opened P85; sizes the rail interface | RUN 2026-08-19: six of nine. Hoop stress is a non-issue at 13.9x margin, the tube is a column. Its Euler load unsupported is 19.9 N against the shot's own 445.86 N axial reaction, so it buckles by 45x and intermediate support is what makes the machine work at all. First mode 1.67 Hz against a 70 Hz target. Two independent criteria land on 1.0 m spacing, seven supports, which cost 99.7 g, so the prediction that they would eat ADR-034's mass saving was wrong. The real exposure is that nobody has said what the tube is made of: 1.140 kg in aluminium, 3.294 in steel, and A49 band 7 passes on one and fails on the other |
> Two entries above are document reviews rather than banded runs, and are filed in `docs/`
> because they declare no band: [`ICD_COMPLIANCE.md`](../docs/ICD_COMPLIANCE.md) (the launch
> interface permits 16.029 m/s; three worse requirements found) and
> [`FMEA.md`](../docs/FMEA.md) (nine of thirteen elements forfeit the manifest; the design
> needs r >= 0.99326 per element per cycle to beat a spring). Both came out of the external
> review recorded in [`REVIEW_RESPONSES.md`](../docs/REVIEW_RESPONSES.md).
| A19 | Sensitivity ranking of nine assumed inputs | numpy + the real pipeline | nothing; ranks the assumptions behind P29, P28, `STRUCTURAL_GAP` | RUN 2026-08-10, verdict band 1 FAIL: net efficiency has two different leaders depending on the metric, so both rankings are published. `v_exit` does not respond to bank ESR at all, nil, then total |

A10 and A11 are cross-checks of the model against its own physics rather than against an
external tool, which is a weaker class of check and is labelled as one. They are here because each
asks a question no external solver was going to be pointed at: whether the bank can source the
shot at all, and whether the sled's energy has to be thrown away. A12 is stronger than both,
its two methods share only the block model of the magnets, and A6 is weaker than any of them,
since both its geometry and its covariance come from inside this project.

> This table was wrong about A1 for a day, from 2026-07-30 to 2026-07-31: it said "specified,
> not run" while `OPEN_PROBLEMS.md` E1 and `docs/ROADMAP.md` both recorded A1 as run on
> 2026-07-29. The cause is worth keeping, because it is the reason A1 and A5 now carry their
> results inline. Both run sheets were pure specifications, with their outcomes living only in
> `OPEN_PROBLEMS.md`, `CHANGELOG.md` and `docs/RESULTS.md`, so a search of `validation/` for
> completed runs found A4, A8 and A10 and missed them. A run sheet that does not record its own
> result is not a record. A1 and A5 were written up on 2026-07-31 in the format A4, A8, A10 and
> A11 already used.

A2 (3-D field, end effects) and A3 are not specified here; A1 closes only the 2-D half of
E1, and the 3-D end effects still need a 3-D solver.

## The one rule that makes these tests rather than exercises

The acceptance band is declared before the analysis runs. Every run sheet in this
directory states its band up front, and each band is traceable to a current value in
`analysis/results/*.json`. A cross-check whose target is chosen after seeing the answer
proves nothing.

This is not hypothetical here. `docs/FEMM_Run_Sheet.md` was written against ⟨B⟩ ~ 0.62 T
across the winding gap; the winding-resolved model now computes 0.552 T, so that
sheet can no longer function as a test and is marked superseded. The replacement sheet
(`analysis/femm/FEMM_RUN_SHEET.md`) had the same problem in its stray-field targets,
they predated the P3 correction, and was fixed on 2026-07-27.

When a band is missed, the outcome is a new P-item, not a quietly widened band.

A field band must name which field, at which plane, as which quantity. Added 2026-08-10 from
P20, and it is aimed at A2 in particular. A1's array-surface band was declared against
`analytic_B0_surface_T` = 0.7714 T, the fundamental amplitude of a single array's ideal wave
at its own surface. Any measurement at that plane in a double-sided machine includes the
opposing array, worth `B0·exp(-k·GAP)` = 0.160 T there, so the correct double-sided reference is
0.9317 T, and the FEM's fundamental is 0.9312 T, a ratio of 0.9994. The row failed as
declared and the model was right. A raw peak at that plane reads 1.4641 T and is a third
quantity again, mesh-dependent, because the plane sits on the magnet face where block-corner
harmonics dominate and the field is formally singular at the corners.

So a band at a magnet surface needs two references named, not one: single-sided or
double-sided, and fundamental or raw peak. A1's sheet is left exactly as written, a band is
never edited after its run, and this is where the correction lives instead, so the next sheet
meets it without having to know to search the register for it.

And when a band cites an external document, record which document, which revision, and whether
a tighter comparator exists in the same family. Added 2026-07-31 after P30: A7's tip-off
band was set at 5 °/s from the external NRCSD-E, whose publisher calls that figure provisional,
while the internal NRCSD that has actually flown specifies 2 °/s. Nobody picked the easy number
on purpose, it is what happens when a band cites one source and nobody asks what else that source
set contains. A band may still be tightened before a run, which is how that one was fixed; it
may never be touched after one.

## Conventions

- Inputs come from what is already committed: `cad/step/gen3/*.step` (Gen3 is current,
  see `cad/README.md`), `cad/parameters.json`,
  `analysis/femm/emocd_cross_section.dxf`. Where a check needs an orbit or a constant, it
  imports from `analysis/*.py` rather than restating the value, see `gmat/build_scripts.py`.
- Outputs land in `validation/results/<analysis>.json` alongside the solver version,
  mesh size, and boundary conditions, the same way `analysis/results/*.json` works.
- A completed run gets a `CHANGELOG.md` entry with cause, before/after, and the P/E item
  it moves.
- `analysis/*.py` stays authoritative until a run closes the relevant item. Do not
  hand-edit a script to match an FEA result, record the discrepancy first, decide
  second.

## Licensing

Keep these tools external. CalculiX and Code_Aster are GPL, Elmer is LGPL, and this
repository is MIT, commit input decks and result JSON, never vendored solver code.
Orekit (Apache-2.0), Project Chrono (BSD-3) and pyleecan (Apache-2.0) are permissive.
NASA's CARA tools are MATLAB under a NASA open-source agreement; parts run under Octave,
and the licence should be read before anything is redistributed.
