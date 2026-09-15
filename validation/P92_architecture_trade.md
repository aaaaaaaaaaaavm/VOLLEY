# P92 clean-sheet architecture trade: criteria before implementation

**Scope:** Gen6 redesign / P92.  
**Configuration state:** mechanism selection reopened. Gen5 electromagnetic hardware and the existing stage-integrated gas guide are comparators, not incumbents.  
**Evidence class:** computation and documented engineering evidence only. Nothing in this run can create hardware, provider accommodation or qualification evidence.

This run exists because the mission studies have stopped supporting “more release speed” as a useful architecture objective. P113-S4 adds a second payload without resetting the host and shows that, on its fine grid, the BOLLEY, Gen5 and existing Gen6 authority screens all reach the same best tested ideal host-fuel result with a 4.569852 m/s first release. That is not a universal optimum. It is enough to require the next mechanism comparison to start from mission duty rather than from the highest velocity a previous machine happened to produce.

The trade must keep **payload arrangement** separate from **release mechanism**. An independent bay can use more than one actuator family; a gas or electromechanical actuator does not imply a shared magazine. Combining those decisions before comparing them would pre-select the answer.

## Candidate set

### Payload arrangement

1. **Independent retained bays:** one payload path per bay; services may still be shared.
2. **Independent banks:** several smaller shared paths, each serving a subset of the manifest.
3. **Shared magazine/path:** one common handling and release path serving the manifest sequentially.

### Release mechanism / interface

1. **Conventional selected spring + timing:** competent baseline, not a straw man.
2. **Programmable stored-energy captive pusher:** adjustable mechanical energy with positive retention and arrest/reset burden charged to the design.
3. **Short-stroke electromechanical pusher:** motor/voice-coil/linear-actuator family sized to the selected duty, not the frozen Gen5 track.
4. **Existing stage-integrated gas guide:** current Gen6 comparator with its actual guide/contact/pressure-system assumptions and failures retained.
5. **Gen5 electromagnetic system:** frozen comparison case only.
6. **BOLLEY cooperative interface:** spacecraft-side passive interface charged to the architecture; Fluxrelay/Fluxframe/Fluxpiston evidence must not be mixed.

A candidate may be added only if its configuration and evidence sources are named before its result is interpreted.

## Common duty screens

For the 4 kg / 3U reference payload, calculate the same basic release physics at:

- **4.569852 m/s:** S4 fine-grid first-release result for the best tested campaign. Study point only.
- **11.8 m/s:** common-energy mission screen already used in S1/S2 comparisons.
- **16.029 m/s:** frozen Gen5 output. Comparator, not requirement.
- **29.009 m/s:** existing gas-guide design point. Comparator, not requirement.

For each speed report payload kinetic energy, impulse and ideal constant-acceleration stroke at 10 g and 25 g. The 25 g value is a study ceiling already used in the programme, **not a universal CubeSat qualification limit**. No operating interval, including 0.5 m/s, is treated as demonstrated controllability.

The trade must also expose the scaling law for adjacent payload masses rather than silently scaling 3U CAD.

## Installed-system accounting

For every mechanism/arrangement combination, report these fields separately. Unknown values remain `UNKNOWN`; they are never replaced by a guessed score.

- dedicated dry mass
- payload-specific adapter/interface mass
- occupied envelope and required stroke/guide length
- stored or drawn energy per release
- consumables per release and per campaign
- peak force / acceleration duty
- moving mass that must be arrested
- thermal recovery or recharge/fill requirement
- host reaction impulse / attitude-recovery consequence
- retention and inhibit hardware
- sensors, control and power electronics
- support structure / pressure containment / magnetic shielding where applicable
- clearing/settling time before the next release
- reset/rearm requirement
- successfully deliverable payload count after one blocked mechanical path
- successfully deliverable payload count after shared command/power loss
- payload modification or lost spacecraft resource required

Existing evidence may populate a field only when its configuration matches the candidate. A favorable number from Gen5, the gas guide or one BOLLEY branch cannot be transferred to another geometry without a new validation path.

## Fault topology

Run at least these two fault cases for every arrangement:

1. **one blocked mechanical release path**;
2. **loss of shared command/power service**.

The result is the number of payloads that remain safely retained and the number that remain potentially deliverable. “Independent bay” is not allowed to imply electrical or command independence unless the architecture actually supplies it.

No probability or reliability score may be invented. This is consequence topology, not a probabilistic reliability model.

## Comparison rule

There is **no weighted score**.

A candidate can be rejected only by one of the following:

- it cannot meet a declared mission duty without violating a declared physical/interface limit;
- an existing run has already falsified the exact configuration and the failure still applies;
- its installed burden is source-backed and is strictly dominated by another candidate that supplies the same required mission authority and fault consequence;
- it requires a payload/host interface that violates the stated mission hypothesis and no cooperative variant is being evaluated.

If the ranking depends on an unknown mass, friction coefficient, actuator force, clearing time, provider limit, switching loss, tolerance or other missing quantity, the result is **UNDERDETERMINED** and the output must name the smallest calculation, supplier datum or experiment capable of deciding it.

## Acceptance bands

The run passes only if all are true:

1. Every candidate is identified by configuration and evidence source; no favorable cross-configuration borrowing occurs.
2. Arrangement and mechanism are represented as separate dimensions before combined architectures are discussed.
3. The four common duty screens are computed from the same equations and payload mass for every candidate.
4. Installed-system fields are source-backed or explicitly `UNKNOWN`; no fabricated mass, cost, reliability or efficiency enters the comparison.
5. Conventional spring + timing, host manoeuvre authority and cooperative BOLLEY remain visible baselines wherever they can perform the same mission job.
6. Blocked-path and shared-service fault consequences are reported without invented probabilities.
7. Existing Gen5 mass failure, gas-guide contact/release limits and suspended trim evidence remain visible where applicable.
8. The output states whether P92 is selectable from current evidence. If not, it names the minimum decisive evidence needed and leaves P92 open.
9. No result calls 4.569852, 11.8, 16.029 or 29.009 m/s a product requirement merely because it appears in a prior study.
10. Re-running from the committed inputs reproduces the machine-readable result and report without manual edits.

## P92 disposition rule

P92 closes only if one architecture can be selected without an unresolved hard blocker in its required mission duty **and** the losing alternatives have dated, source-backed rejection reasons. A preference, a render, a lower actuator mass alone, or a green numerical test is not enough.

If the current record cannot support that decision, this run passes by proving the decision is underdetermined and identifying the decisive next evidence. That is preferable to selecting Gen6 by aesthetic preference.
