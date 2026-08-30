# tests

Two kinds of check, and neither replaces a run sheet.

**Properties.** `test_orbital_properties.py` and `test_campaign_properties.py` state rules
that must hold for *any* admissible input, and hypothesis generates the inputs. The
reference point already has thirty-five identities inside `host_reference.self_test()`.
Those check one altitude and one stage mass. [P114](../OPEN_PROBLEMS.md#p114) was a claim
that happens to be true at 500 km on a 1000 kg stage and is false as a general statement,
and nothing that only evaluates the reference point can tell those apart.

**Regressions.** `test_regressions.py` reintroduces every defect this repository has
actually shipped and requires a gate to catch it. Each of these was verified once by hand
on the day it was fixed, in a throwaway script. That proved the fix and protected nothing
afterwards, which is how [P114](../OPEN_PROBLEMS.md#p114) and
[P116](../OPEN_PROBLEMS.md#p116) came to be the same mistake twice: a quantity computed
correctly, then used to answer a question it does not answer.

A regression test here fails when the **defect stops being caught**, so each one asserts
that a failure list is non-empty. `test_the_self_test_passes_when_nothing_is_broken` is the
control; without it the others would pass against a self-test that always fails.

## What this does not do

It does not check physics against reality. Nothing in this repository does. Bands in
`validation/` are where a model meets a criterion declared before the script existed, and
that remains the only place a claim is earned.

It does not replace `--check-doc`. Prose is still unchecked, and the generated blocks are
twelve per cent of `docs/HOST_REFERENCE_CASES.md`.

## Running

    python3 -m pytest                    # the suite, as verify_all.sh and CI run it
    python3 -m pytest tests/test_regressions.py -v

The suite is mutation-checked. Halving the apogee rise, inverting the burn-floor
comparison, disabling sequential propagation and perturbing burn duration by one per cent
each turn it red.
