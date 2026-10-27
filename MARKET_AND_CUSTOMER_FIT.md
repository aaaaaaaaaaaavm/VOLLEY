# Market and spacecraft fit — ACR1 evidence review

**Updated 25 October 2026.** The current reference is [VOLLEY-G5-ACR1](validation/acr1/README.md): twelve 4 kg 3U surrogates, 1–3 m/s supported computational commands and a generic maneuvering host. This is a completed computational study and an input to customer discovery. No customer requirement, quotation, host agreement or product-market fit has been established.

## Current engineering and mission boundary

| Item | Current reference | Meaning for a prospective buyer |
|---|---:|---|
| Represented dry CAD mass | 149.5567197 kg | Includes the generic mounting ladder; provider adapter/reinforcement remains unspecified. |
| Separate power/control allocation | 7 kg | Explicit allowance, not a supplier-complete installation or spatial CAD inertia. |
| Dry study device | 156.5567197 kg | 13.0463933 kg allocated per carried spacecraft over twelve payloads. |
| Manifest and loaded device | 12 × 4 kg; 204.5567197 kg | Current architecture is twelve 3U envelopes. |
| Nominal represented bounding dimensions | 2250 × 1240 × 1348.9 mm | About 3.763 m³ bounding volume; host access, adapters, tolerances and departure keep-outs are additional requirements. |
| Powered launch stroke | 1300 mm | Retained-carrier launch and active arrest must be assessed together. |
| Supported command range | 1–3 m/s | Calculated carrier–host release speed; finite-host mapping means this is not identical to payload inertial kick. |

The [same-target mission comparison](validation/acr1/mission/MISSION_REPORT.md) uses a 500 kg wet bus, 20 kg of propellant counted within that bus, 220 s Isp and 1 N/5 N force ceilings. Both alternatives carry the same twelve 4 kg payloads from a nominal 500 km SSO state to common terminal full-state targets. VOLLEY retains its current device mass. The spring reference retains a declared 12 × 6 kg = 72 kg device-class assumption, giving an **84.5567197 kg device penalty** for VOLLEY. The 6 kg is assumed dispenser mass per payload, not spacecraft mass or a supplier quotation.

| Preplanned target family | Host ceiling | VOLLEY propellant | Ideal ground-pretrimmed spring |
|---|---:|---:|---:|
| Uniform 2 m/s | 1 or 5 N | 0.052443 kg | 0.052443 kg |
| Alternating 1/3 m/s | 1 N | No tested pass | 0.075002 kg |
| Alternating 1/3 m/s | 5 N | 0.289874 kg | 0.053645 kg |

The sampled fixed-2 spring uses 0.046957 kg for uniform targets. No tested fixed-2 alternating candidate meets either ceiling; this is a bounded policy result, not global infeasibility. Ideal pretrim is a strong preplanned benchmark: it selects payload-specific separation energy before flight and closes both families. The current cases establish **no propellant or initial wet-mass advantage** for VOLLEY over that benchmark.

In-flight recommanding is the proposed additional capability. Its value requires a real late-change requirement, approved payload limits, navigation and host authority, operations and a matched alternative. The present targets were known before planning; these cases do not demonstrate a retasking advantage.

## Buyer and evidence

The candidate economic buyer is an organization responsible for delivering a manifest to agreed orbital states: an OTV/carrier operator, rideshare integrator or constellation operator purchasing integrated delivery. A bus manufacturer may set the payload interface without purchasing the deployer. These roles are hypotheses.

The combined market thesis (internal background study) and independent business-case check (internal background study) were reread on 25 October. They support investigating repeat production, replenishment and individualized delivery. They explicitly do not establish willingness to pay. Broad launch counts and production examples are not a serviceable VOLLEY market.

| Candidate job | What must be true to make VOLLEY useful | Current decision |
|---|---|---|
| Twelve-payload preplanned distribution | Lower total resources or a required capability relative to calibrated springs plus host maneuvers | No advantage found in the tested common-state families; retain the conventional benchmark. |
| Late change to one or several destinations after integration | The requested change fits 1–3 m/s commanded release and approved host operations, and alternatives impose greater supported burden | Candidate discovery case; no actual customer requirement or retasking campaign demonstrated. |
| Safe separation from a suitable orbit | Buyer needs an approved departure corridor and interface | A qualified conventional dispenser is the control case; extra release authority may have no value. |
| Initial distribution of low-propulsion spacecraft | Shared delivery removes a real spacecraft or operations burden while preserving avoidance and disposal obligations | Conditional; no blanket propulsionless-fleet or lifetime benefit claim. |
| Mixed 1U/3U batch or smaller spacecraft | A separately evaluated carrier, payload interface and manifest meet the service requirement | Future Gen6 work. ACR1's twelve 3U configuration is not a mixed-size product. |

[MinXSS](https://arxiv.org/pdf/1508.05354) is a published 3U example with 3.5112 kg reported design mass; ACR1 uses a separate 4 kg surrogate. SwissCube is a named public 1U size/mass example for future work. Neither is a customer, an approved payload or evidence of magnetic, contact or shock compatibility. See the [dated source cards](validation/reference_interfaces_acr1/SOURCE_CARDS.json).

## Competent alternatives and public fit

The [EXOpod Nova manual, Rev. 1.2, June 2024](https://www.exolaunch.com/documents/EXOpod_Nova_User_Manual_June_2024.pdf) gives four independent 3U slots in a 12U S4 pod and 13.32 kg ±5% bare pod mass. Three provide twelve slots and **39.96 kg bare mass**, excluding adapters and fasteners. ACR1 exceeds that bare boundary by 116.5967197 kg before installed additions are normalized. This newly checked product datum does not replace the frozen mission's 72 kg assumption or create a new fuel result. Mounts, harnesses, sequencer, thermal provisions, failure exposure and mission-specific spring velocity remain in the comparison.

The [host reference review](docs/REFERENCE_INTERFACES_ACR1.md) provides four dated architectures:

- **POEM-like spent stage:** flown hosted experiments and services; no ACR1 accommodation or repeated post-passivation translational authority established.
- **D-Orbit ION:** relevant commercial orbital transport and customized deployment service; usable installation envelope, host budget and price are unknown here.
- **Electron Kick Stage:** a flown maneuvering small-launch reference; the unchanged loaded ACR1 unit fails the documented standard nominal mass/envelope screen. Custom expanded services require a new screen.
- **Generic ACR1 host:** the declared computational basis, with no provider approval or real bus selected.

An OTV is a relevant buyer and a competent alternative. Host movement followed by conventional separation can deliver different payload destinations; the service is not limited to one shared velocity change. The current comparison represents that alternative using the same surrogate host, not an invented ION propulsion budget or quote.

## Evidence needed for a commercial decision

For one actual or recent mission, record the payer and integration approver; payload class/count and approved loads/fields; initial and target full states with tolerances; deadline and late-change scenario; host power, navigation, thrust, restart/slew and disposal resources; current alternative and quote; and the financial or operational loss that release recommanding could avoid. No provider contact is authorized by this record.

A positive case requires the supported avoided cost or paid delivery value to exceed extra installed hardware, integration, host resources, operations and expected loss. No term has a defensible quotation here. Public launch starting prices and industry counts cannot supply VOLLEY revenue, savings or breakeven.

The linked payload-family analysis (internal background study), mission-fit note (internal background study) and ANYA-class study (internal background study) were also reread. Their historical masses, 16.029/29.009 m/s points, packing counts and engine/stage assumptions are not current ACR1 ratings. The 5–50 m/s market hypothesis and 1 km/s research objective are future studies, not achieved command ranges. [Source review and criterion recommendations](validation/reference_interfaces_acr1/SOURCE_REVIEW_AND_CRITERIA.json) identify the remaining D/H/L work.
