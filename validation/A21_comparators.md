# A21: VOLLEY against the alternatives, on identical axes

> ## Forward note, 2026-08-10: what this ratio does and does not govern
>
> **Nothing below is edited. Band 1 was declared before the run and it passed at 7.52×**, and a
> band is never rewritten after its run — the same rule that left A1's sheet untouched and put
> its correction elsewhere.
>
> **But 7.52× is a ratio of _gains_** (+61.8 % against +8.2 %). On **delivered orbital life** —
> total years, 2.111 against 1.412 at 450 km — the ratio is **1.495×**.
>
> **Use 1.495× for any risk-weighted comparison**, because a satellite the deployer never
> releases delivers nothing, and `docs/FMEA.md` shows this architecture forfeits satellites in
> ways a spring does not. **E30** records the correction and the reason it matters: 7.52× flatters
> in exactly the comparison a reviewer will make.

**Closes:** nothing. **Establishes** the competitive position on computed numbers rather than on
assertion, and removes a claim the repository cannot support.

> ## BANDS DECLARED 2026-08-10, BEFORE `analysis/comparators.py` EXISTS.
>
> Everything below the "Acceptance bands" heading is committed before the script is written.
> The script is absent at this commit and that absence is checkable.

## Result, 2026-08-10: seven of seven bands pass, and the headline changes

`analysis/comparators.py`, bands committed at `881c260` before it existed. Results in
`analysis/results/comparators.json`.

### The headline ratio was the weakest one available

| Δv | Lifetime multiplier | Extension over unboosted |
|---:|---:|---:|
| 1.0 m/s — spring, low end | ×1.0323 | +3.23 % |
| 2.0 m/s — typical spring | ×1.0653 | +6.53 % |
| 2.5 m/s — fastest published spring | ×1.0821 | +8.21 % |
| **16.388 m/s — VOLLEY** | **×1.6176** | **+61.76 %** |

| Framing | Ratio |
|---|---:|
| Velocity — what every document currently quotes | **6.56×** |
| **Lifetime extension, vs the fastest spring** | **7.52×** |
| **Lifetime extension, vs a typical spring** | **9.45×** |

**Band 1 passes at 7.52×**, so the headline moves. Lifetime extension is superlinear in Δv in
this regime, and quoting the velocity ratio has been **understating the machine by about 15 %**
against the hardest comparator and by 44 % against the ordinary one.

### The full comparison, on identical axes

| | Spring | **VOLLEY** | Differential drag | Cold-gas module |
|---|---|---|---|---|
| Δv | 2.5 m/s | **16.388 m/s** | 0 | 16.4 m/s |
| Lifetime extension | +8.2 % | **+61.8 %** | none | +61.8 % |
| **Designed differential** | **0** | **16.388 m/s**, to 0.027 m/s (3σ) | 0 | per satellite |
| 30° of phase | not by design | **1.38 d** | 25 d | 1.38 d |
| Deployer mass per 3U | 6.0 kg | **6.375 kg** | 0 | 0.85 kg on the satellite |
| Satellite carries | nothing | **nothing** | nothing, but needs attitude authority | 0.5–1.2 kg, pressure vessel, qualification, range safety |
| Host provides | one deploy signal | 150–300 W, serial link, firing window | nothing | nothing |
| Schedulable | — | **yes** | **no** | yes |
| Maturity | **TRL 9, thousands deployed** | **TRL 2–3, nothing measured** | flown on 12 satellites | COTS, flown |

### Band 3: the advantage with no ratio

**A spring's designed differential is exactly zero**, and that is not a small number — it is a
category. Every satellite gets the same nominal push; any spread is manufacturing scatter that
cannot be commanded, predicted per unit, or ordered.

Distribution needs a *difference*. So a spring-deployed fleet has one route to 30° of phase —
differential drag, at **25 days, unschedulable** — against VOLLEY's **1.38 days**, a factor of
**18.1×**. Band 6 passes.

### Band 4: mass parity, now computed rather than asserted

**6.375 kg per 3U satellite against a canisterised-class 6.0 kg — a ratio of 1.062, inside 7 %.**
`LANDSCAPE.md` already claimed parity; it is now measured. **A magazine-fed electromagnetic
launcher lands in the same kilograms-per-satellite class as a canister of springs**, while
delivering 7.5× the lifetime extension and a differential capability springs do not have.

### Band 5: the loss, declared in advance and confirmed

**At 3U a cold-gas module beats VOLLEY on mass by 7.5×** — 6.375 kg of shared deployer against
~0.85 kg carried by the satellite. This band was written to expect a loss of ≥ 5× *before the
run*, precisely so the result could not be framed away afterwards. It is consistent with
`KILL_CRITERIA.md` threat 1, which is crossed on this comparison.

**What the cold-gas module costs instead is the thing VOLLEY exists to avoid:** a pressure
vessel, a qualification campaign, range-safety review, and an attitude control system able to
point it. For the ~92 % of flown CubeSats with no propulsion, that trade was already declined.

### Band 7: the cost comparison returns NOT COMPUTED, deliberately

**There is no vendor quotation for any line of `analysis/cost.py`, and no price for any
alternative anywhere in this repository.** The band required the script to *emit* `NOT COMPUTED`
rather than simply not ask, so the gap is recorded in the output.

**Any claim that VOLLEY is cheaper than a transfer vehicle, a dispenser, or a propulsion module
is unsupported in both directions and is withdrawn.** Closing it needs **E3** — quotations — not
another analysis.

### What this sheet does not establish

It compares a **model** of VOLLEY against **published class figures** for things that have flown.
That is a weaker class of comparison than the table's symmetry suggests, and E4 stands: nothing
about VOLLEY here is measured. The 25-day differential-drag baseline is `astro.py`'s own model
output, **not** the flown 12-satellite result that `RELATED_WORK.md` records exists — that
substitution is not made because the source has not been retrieved (**E16**).

## Why this exists

The repository compares VOLLEY to alternatives in three places — `SUMMARY.md`, `LANDSCAPE.md`
and `MARKET.md` — and each uses **different axes and a different headline number**. None of them
computes the comparison; they quote it.

Two specific defects motivated this sheet:

1. **The headline ratio is the weakest one available.** Every document leads with *"6.6× the
   fastest published spring"*, which is a ratio of **velocities**. Nobody buys velocity. What a
   customer gets is orbital lifetime and phase separation, and lifetime extension is
   **superlinear** in Δv in this regime — so the velocity ratio *understates* the machine.
2. **One claim is unsupported in both directions.** Superiority over orbital transfer vehicles on
   cost and efficiency has been asserted informally. **There is no OTV price anywhere in this
   repository, and `analysis/cost.py` carries no vendor quotation on any line item.** Comparing
   21 % electrical-to-payload efficiency against a propellant mass fraction is a category error.
   This sheet is where that claim is withdrawn rather than quietly softened.

## What is compared, and on what axes

Four options for the same job — distributing a dozen propulsion-less CubeSats:

| Option | What it is |
|---|---|
| **Spring deployer** | P-POD class, canisterised, 1–2 m/s, one value for every satellite |
| **VOLLEY** | this machine |
| **Differential drag** | free, no hardware, flown on a 12-satellite constellation |
| **Cold-gas module** | 0.5–1.2 kg carried *by the satellite* |

Axes, applied identically to all four:

- Δv delivered, and **orbital lifetime multiplier** at that Δv
- **Designed differential** between satellites — the quantity distribution actually needs
- Time to 30° of phase separation
- Deployer or module mass **per satellite**
- What the **satellite** must carry, and what the **host** must provide
- Schedulability, and maturity

**Losses are computed and reported on the same footing as wins.** At 3U the cold-gas module beats
VOLLEY on mass by roughly 8×, and the spring beats it on maturity by TRL 9 against 2–3. A sheet
that omitted those would be a brochure.

## Acceptance bands

Declared before the script exists. Each is capable of failing.

| # | Question | Band | What a miss means |
|---|---|---|---|
| 1 | **Lifetime extension ratio**, VOLLEY against the fastest published spring at 2.5 m/s | **≥ 5×** | the headline claim of this sheet. Below 5× the lifetime framing is not clearly better than the velocity ratio and the sheet should keep quoting 6.6× |
| 2 | **Lifetime multiplier at 16.388 m/s** against `astro_results.json` | **×1.62 ± 0.02** | a fork between this script and `astro.py`, which is the P19 failure mode repeating |
| 3 | **Designed differential available to a spring deployer** | **exactly 0** | if the script returns non-zero, it is modelling manufacturing scatter as if it were commandable, which is the error this axis exists to prevent |
| 4 | **Deployer mass per 3U satellite**, VOLLEY against a canisterised dispenser at ~2 kg/U | **within ±25 %**, i.e. parity | the mass-parity claim. A miss in VOLLEY's favour is as interesting as a miss against |
| 5 | **Cold-gas module mass ratio at 3U** | **VOLLEY loses by ≥ 5×** | this is declared as a *loss* and must be reported as one. If the script shows VOLLEY winning at 3U, it disagrees with `KILL_CRITERIA.md` threat 1 and one of them is wrong |
| 6 | **Time to 30° of phase**, VOLLEY against differential drag | **≥ 10× faster** | the comparator `LANDSCAPE.md` calls the one that matters |
| 7 | **Any cost comparison against any competitor** | **must return NOT COMPUTED** | there is no quotation for VOLLEY and no price for any alternative. A number here would be invention, and the band exists to make its absence deliberate |

### Band 5 and band 7 are the two written to constrain the author rather than the machine

**Band 5 declares a loss in advance.** The cold-gas comparison is the one this project most wants
to avoid, `KILL_CRITERIA.md` threat 1 is crossed on it, and declaring the expected direction
before the run is what stops the result being framed away afterwards.

**Band 7 makes an absence checkable.** "Cheaper than an OTV" is the claim this sheet exists to
remove. Requiring the script to return `NOT COMPUTED` — rather than simply not asking — means the
gap is recorded in the output, and closing it needs **E3** (vendor quotations) rather than
another analysis.

### Band 1 is the one that changes the front door

If it passes, `SUMMARY.md`, `LANDSCAPE.md` and `MARKET.md` all change their headline from a
velocity ratio to a lifetime ratio. That is a documentation consequence declared before the
number is known.

## What happens at each outcome, fixed now

1. **Band 1 fails.** Keep 6.6× as the headline and record that the lifetime framing was tested
   and did not improve on it.
2. **Band 2 fails.** Stop. A fork between this script and `astro.py` invalidates everything else
   here.
3. **Band 3 fails.** The script is wrong. A spring cannot command a differential.
4. **Band 4 fails.** The mass-parity claim in `LANDSCAPE.md` is wrong and must be corrected in
   whichever direction the number points.
5. **Band 5 fails.** Either `KILL_CRITERIA.md` threat 1 or this script is wrong; resolve before
   publishing either.
6. **Band 6 fails.** The differential-drag comparison, which is the one an informed reviewer will
   raise, is weaker than claimed and `LANDSCAPE.md` must say so.

**No band may be widened after the run.**

## Provenance

Lifetime multipliers from `analysis/astro.py` by import. Deployer mass per satellite from
`analysis/payload_family.py`. The operating point from `motor_results.json`.

**Comparator figures are class figures, not quotations, and none names a manufacturer.** Spring
velocities are from published deployer interface documents; the ~2 kg/U dispenser figure and the
0.5–1.2 kg cold-gas range are published class ranges already used in `KILL_CRITERIA.md`. The
25-day differential-drag baseline is a **model output** of `astro.py`, not the flown result —
`RELATED_WORK.md` records that a flown 12-satellite result exists and should replace it, and that
substitution is **not** made here because the source has not been retrieved (**E16**).

Nothing in this sheet is measured. It compares a model of VOLLEY against published figures for
things that have flown, which is a weaker class of comparison than it looks and is labelled as one.
