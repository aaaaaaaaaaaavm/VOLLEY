# A21: VOLLEY against the alternatives, on identical axes

**Closes:** nothing. **Establishes** the competitive position on computed numbers rather than on
assertion, and removes a claim the repository cannot support.

> ## BANDS DECLARED 2026-08-10, BEFORE `analysis/comparators.py` EXISTS.
>
> Everything below the "Acceptance bands" heading is committed before the script is written.
> The script is absent at this commit and that absence is checkable.

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
