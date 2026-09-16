# P92: clean-sheet Gen6 reference-architecture screen

Declared 2026-09-16 before `analysis/reference_architecture.py` exists. P92 and P113 remain open.

## Question

What architecture is worth carrying forward as the **clean-sheet Gen6 reference candidate** after S4, without pretending that a bounded orbital screen has selected flight hardware?

The decision is deliberately split in two. First choose a payload arrangement and release-cell concept that is physically compatible with the mission evidence and fault-isolation intent. Then use experiments and installed-system accounting to decide whether it deserves to close P92. A reference candidate is not a qualified design, provider accommodation, or a claim that competing mechanisms are impossible.

## Frozen inputs and study points

The current S4 result is an input, not a requirement: the best tested BOLLEY/Gen5/existing-Gen6 campaign used a 4.569852 m/s first release for one two-payload benchmark. S4 explicitly does not establish a global optimum, product minimum, or validated speed envelope.

Use a 4 kg payload as the reference cell. Evaluate the kinematic duty at 4.569852, 11.8, 16.029 and 29.009 m/s and at constant-acceleration screens of 5 g, 10 g and 25 g. The 25 g value is only a study ceiling; it is not asserted as a universal CubeSat qualification limit. Compute ideal payload energy `0.5*m*v^2`, constant-acceleration stroke `v^2/(2*a)`, acceleration time `v/a`, force `m*a`, average payload power `E/t` and terminal constant-force power `F*v`.

For the 4.569852 m/s S4 study point, also report stored input energy at 60, 70 and 80 percent release-path efficiency. These are sensitivity assumptions, not measured efficiencies.

## Architecture candidates

Keep payload arrangement separate from energy source.

Payload arrangements:

1. independent retained cells;
2. small banks with a shared local path;
3. one shared magazine/path.

Release concepts:

1. motor-charged mechanical accumulator with a latched short-stroke pusher;
2. direct short-stroke electromechanical pusher;
3. compact gas pusher;
4. existing long gas guide as the historical Gen6 comparator;
5. frozen Gen5 electromagnetic LSM as the historical electromagnetic comparator;
6. BOLLEY as a cooperative payload-interface path, not as evidence for an unmodified-payload VOLLEY cell.

## Hard screens

A clean-sheet VOLLEY reference candidate must satisfy all of these at concept level:

- **Unmodified payload boundary.** No required payload magnet, powered actuator, propellant system or proprietary active interface. Standard mechanical contact during retention/release is allowed. BOLLEY is reported separately because it intentionally relaxes this boundary.
- **Independent retention.** A blocked release path must not mechanically free another payload. A blocked cell should not mechanically strand unrelated independent cells. Shared power/control remains a common-mode risk and must be shown rather than hidden.
- **Programmable departure authority.** The concept must have a credible controllable variable that can set release energy/impulse before release. A fixed spring with timing only remains a mission comparator, not the programmable reference.
- **Compact S4-point geometry.** The 4 kg, 4.569852 m/s study point must fit within 0.25 m ideal constant-acceleration stroke at 5 g or greater. This is a clean-sheet packaging screen, not a provider envelope.
- **No eight-metre dependency.** The new reference candidate may not require the historical 8 m guide to achieve the S4 study point. The 8 m gas architecture remains in the trade with its published contact/tip-off evidence.
- **Safe post-release pusher state.** The architecture must contain a credible way to retain/catch its moving pusher after payload separation. The calculation may leave catcher sizing open, but may not silently discard the moving mass.
- **No inherited speed requirement.** 16.029, 29.009, 89.4 or 100–120 m/s may not be used as a requirement merely because an earlier generation or discussion used it.

## Comparison fields

Do not use a weighted score. For every candidate report: release-energy control variable; peak-power implication; active stroke implication; payload modification; blocked-path consequence; shared common modes; known evidence; known failure evidence; installed-mass state; contact/release uncertainty; and the decisive next evidence.

A candidate can be named the reference only when it passes every hard screen. Unknown installed mass, release repeatability, pusher catch dynamics, shock/tip-off, tolerance sensitivity, and life remain explicit open evidence. Unknowns do not become zeroes.

## Selection rule

Select the **minimum new mechanism** that passes the hard screens and removes a demonstrated architectural liability rather than adding another unverified subsystem. Prefer a concept whose peak release power can be supplied from stored energy charged slowly before release over one that requires the host electrical bus to source the full millisecond-scale mechanical power, unless evidence shows the direct-drive burden is acceptable.

This rule is intended to distinguish a reference candidate for the next calculations and coupons. It does not close P92.

## Required outputs

`analysis/reference_architecture.py` must generate:

- `analysis/results/reference_architecture.json` with all inputs, equations, kinematic duty rows, candidate dispositions and open evidence;
- `docs/GEN6_REFERENCE_ARCHITECTURE.md` with the decision and its limits;
- `figures/gen6_reference_cell.svg` showing functional allocation, not invented detailed hardware;
- `tests/test_reference_architecture.py` with independent formula checks, hard-screen checks and freshness/corruption checks.

The report must state what would falsify the selected reference candidate. The normal verification path must run a freshness check. No register status, frozen Gen5 baseline, provider compatibility or hardware-readiness claim changes merely because this screen passes.