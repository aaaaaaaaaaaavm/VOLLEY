# ADR-032: Gen6 is a stage-integrated, payload-direct, gas-driven deployer

**Status:** Accepted · **Date:** 2026-08-14 · **Supersedes:** the Gen6 definition in
[ADR-029](029-phase-one-closes-on-gen5.md) and [`../GEN6_ARCHITECTURE.md`](../GEN6_ARCHITECTURE.md) ·
**Rests on:** A35, A36, A37, A38, A39

## Context

**Gen6 has meant something different since 2026-08-13.** ADR-029 set the target as *a linear
induction drive on a passive aluminium mover* — no magnets, a 0.6 kg shuttle, an arrest of 82 J
instead of 1938. It carried nine measured bands and an unsized remainder larger than that.

**Five runs on 2026-08-14 replaced it, and not one of them set out to.** Each was aimed at a
different question and the answers compounded:

| | | |
|---|---|---|
| **A35** | Every kilogram attributed to the requirement causing it | **49.23 kg — 58.2 % — survives every requirement deletion in all 64 corners.** The pulse is the largest single driver at 28.1 %, the mover second at 13.6 %, and an unmodified satellite costs **nothing** |
| **A36** | Magazine density, the divisor A35 named | **Band 4 FAIL.** 2 kg is reached at N = 116, which does not package. The containment floor is **0.954 kg/satellite** |
| **A37** | The stage as the deployer rather than its mounting surface | **29.75 kg deleted, 43.33 kg becomes stage structure, 11.45 kg added.** Added mass per satellite **1.608 kg** on a small kick-stage class |
| **A38** | Does A34's cradle closure survive 2.4× the moment? | **It improves.** Settling 27.88 → 17.69 ms, residual still zero, and tip-off's ceiling is **30.9 g** against a 25 g cap |
| **A39** | The store, at metre-scale strokes | **Cold gas at 2.98 kg** against a spring's 11.41, on one 1.71 L bottle for all twelve shots |

## Decision

**Gen6 is the payload accelerated directly, by gas, along a rail the host stage provides.**

| | Gen5 | **Gen6** |
|---|---|---|
| What moves | 9.445 kg sled + payload | **payload only** |
| Energy source | supercapacitor bank, ~17 kW for 162 ms | **one 1.71 L gas bottle for the manifest** |
| Structure | 84.5 kg of deployer | **the spent stage** |
| Acceleration | 10.07 g of a 25 g allowance | **25 g** — tip-off permits 30.9 |
| Arrest | eddy brake, 1.16 kJ per shot | **nothing to arrest** |
| Added hardware | — | **11.45 kg containment + ~3 kg store** |

**Four things are deleted rather than improved:** the mover, the pulse-power chain, the brake and
the return stroke. **P26** — the bank no commercial string can source, the largest live defect this
project has carried — is not solved. It ceases to exist.

### What each run contributes to the decision, and what it does not

**A35 says the mover was never the mass.** 9.445 kg of 84.5 is 11 %, and deleting it barely moves
dry mass. **But it is 70 % of accelerated mass**, which is why the force falls from 3297 N to
**981 N** at the 25 g cap with no sled — *below* the 1328 N Gen5 already commands. **The mover
costs a lot and weighs little**, and that distinction is the whole architecture.

**A37 says the stage supplies what remains**, with every credited item naming the subsystem that
provides it. **43.33 kg is the least-examined number in this decision** and the first thing a
referee should attack.

**A39 says the store is gas, and the reason is not energy density.** A spring must be cocked twelve
times: 7.13 kg of store drags **4.28 kg of wind mechanism**. Gas separates the store from the
actuator, so re-arming is a valve. **The spring's problem was never storing the energy.**

## What this costs, stated rather than absorbed

> ### Amended 2026-08-14 by A40, the same day. The fluid system has now been modelled once and it failed.
>
> The paragraph below said the fluid system was unpriced. **[A40](../../validation/A40_blowdown_transient.md)
> priced the simplest version of it — a fixed orifice fed from the bottle — and it delivers
> 4.7 g mean where 25 is needed, reaching 14.16 m/s against a 30 m/s band.**
>
> **A39's 2.98 kg assumed 50 bar held at the piston throughout, which is a regulator it never
> named.** So this decision now rests explicitly on a component inside A39's **1.5 kg** allowance
> for "piston, seals, regulator and valving" — the largest guess in that run. **P63.**
>
> **The decision is not withdrawn.** One 1.71 L bottle does run twelve shots with 4.5 % droop, and
> flow area was never the problem — 0.71 mm against a 10 mm limit. What is unresolved is how the
> pressure is held, and the repair this points at is a **pre-charged chamber** fired as a closed
> expansion, which removes the flow-rate question entirely and commands velocity by charge pressure.
> **That is a different machine and it needs its own bands.**
>
> ### Resolved the same day by A41, and the store is now specified
>
> **[A41](../../validation/A41_precharged_chamber.md), eight of eight bands.** A **2 litre chamber
> at 50 bar**, charged over the indexing window and fired as a closed adiabatic expansion, gives
> **30.54 m/s at 25 g on a 4.66 kg store** — against A39's regulated 2.98 kg estimate and A40's
> fixed-orifice 14.16 m/s.
>
> **There is no regulator.** P63 is closed by deleting the component rather than pricing it.
>
> | | |
> |---|---:|
> | Chamber / charge | **2 L at 50 bar** |
> | Reservoir | 6 L at 200 bar, 1.41 kg of gas |
> | Store total | **4.66 kg** |
> | **Added mass per satellite** | **1.343 kg**, against A37's 1.608 and a 2.0 threshold |
> | Velocity precision | **0.499 % per 1 % of charge**, against valve timing at 10.53 % per ms |
>
> **The expansion ratio is the binding variable, not the pressure.** Velocity saturates toward a
> 2139 J constant-pressure ceiling while gas grows linearly with chamber volume, so 2 L → 4 L buys
> 1.0 m/s and costs 3.2 kg.

**A fluid system nobody has sized.** Filling a 0.43 litre swept volume in a **133 ms** stroke is
roughly **3 L/s** through a regulator. A39 models none of it. **Gas removes a mass problem and
hands back a fluid-system problem**, and that trade is accepted here with its second half unpriced.

**A cradle mechanism that does not exist**, now at **202 N per contact** instead of 81, which must
still release inside A34's ≤ 1 N residual. Passing A38 band 5 is not the same as that being easy.

**A stage nobody has agreed to lend.** Availability is priced in no run. A different stage each
launch multiplies the interface problem rather than solving it, and keeping a stage alive and
manoeuvring past passivation is a regulatory conversation this project has not had.

**And the honest reading of the propellant.** The residuals a stage carries are its disposal burn.
**Gen6 does not spend them** — A39's charge budget is 25–131 W, which is solar — and the
altitude-shell repositioning in [ADR-024](024-last-mile-delivery-conops.md) is therefore an option
a host may decline without Gen6 failing.

## What this does not change

**Kill criterion 1 is not declared met.** A37 band 5 gives **1.608 kg/satellite** on a second
numerator argued on its merits; **dry mass per satellite still crosses at 7.042 kg** and both are
reported together wherever either appears. **P59 stays LIVE.** The threshold has not moved and
will not.

**Kill criterion 4 is not declared passed.** A38 establishes that raising the acceleration does not
make tip-off worse. It remains *modelled, not demonstrated*, on a mechanism that does not exist.

**Nothing here is measured.** Forty-six analyses, one hundred and seven register entries, and no hardware.
`docs/PROVENANCE.md` says so and continues to.

## Alternatives, and why not

**Gen5 as it stands.** Kill criterion 1 crossed 3.5×, a bank that cannot be bought, an envelope
44 % over. It remains the **measured baseline** and the record of what a self-contained deployer
costs.

**The induction-drive Gen6 of ADR-029.** Superseded, not refuted: A30 killed its rail-drive variant
on a measured transverse edge factor of 0.0253, and A35 then showed the mover it optimised was 11 %
of the mass. **Its nine bands stand as declared.**

**BOLLEY's cooperative interface.** Modifying the satellite costs **nothing** on A35's ledger,
because the sled is caused by the *mover* choice and not by the *unmodified* requirement. And once
modification is on the table the customer compares against putting propulsion on the satellite,
which manoeuvres repeatedly where one impulse does not. **The unmodified-satellite constraint was
the moat, and BOLLEY is the evidence for that rather than the alternative to it.**

## Falsifiers

**This decision is wrong if any of these turns out true:**

1. ~~**The 43.33 kg stage credit is optimistic by more than 30 %.**~~ **This falsifier has fired,
   2026-08-16, and its threshold was wrong.** [A45](../../validation/A45_stage_credit.md) put the
   real break-even at **16.5 %** — the 30 % figure predates A43 settling the store at 5.38 kg.
   **The credit's largest single item, 8.00 kg of enclosure, radiator and packaged avionics, is
   P10 — a mass this repository records as never itemised — and at 18.5 % of the credit it fires
   the falsifier on its own.** A hostile reading of all seven items gives **3.108 kg per
   satellite** against 1.403 at the full credit. **A37 band 5 fails retrospectively and is not
   edited; kill criterion 1 is crossed on both numerators.** The honest figure to publish is the
   range, not its lower end. **P68.**
   **Re-run as A45-R after A46 itemised the enclosure: the break-even halved again to 8.4 %**,
   because the credit grew to **85.36 kg — 67.4 % of the machine** — while the 7.17 kg allowance
   did not. **The enclosure alone is 58.6 % of the credit.**
2. ~~**The blowdown transient needs a regulator that weighs more than the store it feeds.**~~
   **Retired 2026-08-14 by A41.** There is no regulator: a pre-charged chamber removes the
   flow-rate problem by construction. The store is **4.66 kg**, not the 2.98 A39 estimated, and it
   still fits. **Replaced by a narrower falsifier:** *a 2 L chamber cannot be filled to 50 bar
   inside the inter-shot window*, which A41 did not check. **A42 answered it: 4.14 s through a
   1 mm orifice, against a 10 s window. Not the constraint.** What A42 found instead is that
   A41's reservoir is sized on gas the bottle cannot give back — **P64**, a store correction of
   about 1.3 kg that leaves added mass per satellite at 1.34–1.46 kg.
   **Amended 2026-08-16 by [A43](../../validation/A43_reservoir_thermal.md), which closed P64 and
   moved it the other way.** Conduction through stagnant nitrogen gives a **17 460 s** time
   constant against a **1200 s** cadence, so the bottle does not re-equilibrate: infrared passes
   straight through a homonuclear diatomic and free fall removes convection. **The design
   reservoir is 9.55 L and added mass per satellite is 1.403 kg.** Both of A42's bracket
   endpoints proved unreproducible — **P66**.
3. **No launch provider will keep a stage alive past passivation** on terms that do not require
   spending its disposal propellant.
4. **The unread voice-coil deployer (P57)** already claims the programmable-velocity result on a
   direct-drive linear machine, in which case the contribution is the stage integration and the
   gas store, not the velocity control.
