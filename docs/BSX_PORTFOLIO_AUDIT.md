# BSX repository audit, 2026-09-06

I audited the public portfolio against the current repository heads, with VOLLEY first. This is a record of what I checked, not a claim that every equation, dependency, source or hardware assumption is correct.

## Scope and evidence

| Repository | Checks and disposition |
|---|---|
| VOLLEY | Full local gate, 31 existing property/regression tests, result freshness, baseline and public claims. Repaired stale overview; reconciled four already-completed register entries; executed separately declared A24-R and A2-R. Gen5 has 11 computation items and three decisions left; Gen6 has 18 computation items. |
| VOLLEY-paper | Compared headline PDF values, checked page counts, corrected the abstract's acceleration wording and spring comparison, rebuilt Letter/A4 manuscripts, and regenerated the evidence payload. |
| VOLLEY-thesis | Same manuscript corrections and matching rebuilt PDF; regenerated the flagship evidence payload. |
| VOLLEY-lab | Repaired the route inventory for existing VLAB-B002/B003 entries; checked namespaces, links and generated figures. |
| BOLLEY | Repaired the stale result inventory and wired A9-A9f/A5f-A5h into the checker; executed A5h against its frozen bands; checked the four packaged CAD scopes, source/artifact hashes and injected failures. Nominal CAD only. |
| GatewayCX | 123 existing tests pass, including restart persistence, independent adapter, authenticated RPC and integrated replay. No new network interoperability claim is made by this audit. |
| engineering-evidence-toolkit | Six tests and repository verification pass: source hashes, finite result values and public links. |
| pulsed-linear-motor-design-lab | Seven tests and repository verification pass. Imported numerical reference evidence retains its original scope. |
| orbital-deployment-trade-study | Nine tests and repository verification pass. These are preliminary orbital and disturbance screens. |
| constraint-floor | Two existing tests pass. The additive attribution bound does not prove an optimum across all possible architectures. |
| spacecraft-separation-dynamics | Four tests pass after correcting apsis ordering for a direction-reversing impulse. |
| parametric-cad-evidence-pipeline | Four tests pass after adding parameter-digest, manifest-section, size and path-containment checks. |
| gatewaycx-bearer-sdk | Three tests pass after fitting the nominal conformance probe to small MTUs and rejecting invalid MTU types. |
| disruption-network-lab | Four tests pass after rejecting non-finite contact times and non-integral byte counts. The contact model still assumes no serialisation duration. |
| scientific-run-registry | Two existing tests pass for content-addressing and tamper detection. Concurrent writers were not exercised; this is not a transactional database. |
| aaaaaaaaaaaavm | Reconciled the spring comparison and linked the current review; kept the flagship profile template identical. |

Private non-portfolio repositories were inventoried through the connected account but were not included in the public code verification above. An empty repository has no executable material to verify.

## What closed and what did not

P37, P46, E29 and P95 had closing evidence already in the record; their dispositions were stale. A24-R newly closes P54's reference-literal defect while preserving original A24 failures. A2-R newly closes P55's depth-resolved lever computation. Neither changes the Gen5 operating point or the failed mass criterion.

A5h closes the declared nominal winding-CAD question only. Electrical implementation, packaged mass, switching losses, manufacturing details and hardware qualification remain separate BOLLEY tasks.

The remaining calculations, measurements, provider data and decisions are in [BSX_REVIEW.md](BSX_REVIEW.md). That generated list is the current handoff, and the repository gates require it to agree with the register.
