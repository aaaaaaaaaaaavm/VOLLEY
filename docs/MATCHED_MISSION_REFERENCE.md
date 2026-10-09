# Matched reference mission comparison

**Reference screen, not a supplier quote, qualified mission or proof of global infeasibility.**
All options use 12 identical 4 kg spacecraft, the same 450 km circular starting
state, 300 kg base host, 10 kg fuel, 2 kg reserve and 220 s assumed host Isp.
Installed dispenser mass is added to host dry mass: a 72 kg class spring set
(6 kg per 3U × 12) or the 126.562 kg modeled Gen5 dry mass. The latter mixes
assumed components with a historical sled-volume input and is not measured.

## One release at a common epoch

The exact common target is a +16.029 m/s *inertial* tangential payload
increment, giving a 28.801 km immediate two-body
semi-major-axis rise. Momentum-conserving recoil is included; the host may make an
ideal pre-release burn. No burn time, stage restart or attitude constraint is applied
to this single-event calculation.

| Option | Relative release m/s | Installed device kg | Host preburn m/s | Ideal host propellant kg | Fuel left kg |
|:--|--:|--:|--:|--:|--:|
| Spring dispenser class | 2.500 | 72.000 | 13.552 | 2.693 | 7.307 |
| Gen5 finite-force ideal upper | 12.448 | 126.562 | 3.683 | 0.827 | 9.173 |
| Gen5 historical rated model | 16.029 | 126.562 | 0.132 | 0.030 | 9.970 |

The finite-force speed is an optimistic geometry-only upper bound; the
historical 16.029 m/s is contradicted by the finite-array screen and retained
only to show how the old assumption changes the comparison. The spring figure
is a class assumption, not an exact flight dispenser. The result does not price
power, risk, launch mass value, provider integration or payload propulsion hardware.

## Twelve-release finite-burn reference

The same existing P113-S12 optimizer is rerun with each installed device mass
included in host dry mass. Every case has the same 20-minute release cadence,
5 km target arc spacing and 18,000 s terminal epoch. Its 100 N thrust and
continuous restart/pointing assumptions are reference values, not a selected host.

| Option | Accepted prefix / 12 | First failing stage | 64-corner replay of accepted prefix |
|:--|--:|--:|:--|
| Spring dispenser class | 4 | 5 | 24/64 passing prefix corners |
| Gen5 finite-force ideal upper | 1 | 2 | 0/64 passing prefix corners |
| Gen5 historical rated model | 1 | 2 | 0/64 passing prefix corners |

An optimizer failure means **no accepted trajectory was found under these
seeds and constraints**. It does not prove that no trajectory exists. None of
these cases delivers all twelve. Higher relative release speed can make a short
spacing target harder, and the larger device increases host propellant burden.

![Matched reference comparison](../figures/matched_mission_reference.png)

## Open alternatives and decisions

- onboard propulsion: no named tank, thrust, pointing or installed mass
- orbital transport: no quoted service, provider trajectory or interface
- differential drag: cannot provide this immediate same-epoch target; long-deadline trade separate

A final paper comparator still needs a named provider/payload, validated
release operating range, real OTV/service terms, reliability, disposal and
same-epoch covariance. The present calculation is an honest matched *reference*,
not a commercial or flight advantage claim.

Reproduce: `python analysis/matched_mission_reference.py` in an environment with the declared dependencies.
Exact inputs, outputs and source hashes are in `analysis/results/matched_mission_reference.json`.
