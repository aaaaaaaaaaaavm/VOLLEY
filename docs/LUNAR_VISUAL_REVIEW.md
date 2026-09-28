# Lunar-first visual and mission review

> **Architecture disposition, 2026-09-28:** The separate motor-charged spring-cell bank is withdrawn as VOLLEY's next architecture. It is retained here only as a dated study. Any selection or current-reference wording below describes the former decision and is superseded. A reusable shared launch path with sequential loading is the open design objective; no speed envelope is validated. See [current status](NEXT_GENERATION_STATUS.md).


Adityavardhan Mishra · 17 September 2026 · C0-S2

**Status: concept review and ideal numerical screen. No flight design or useful
lunar lifetime demonstrated.** [Interactive local website](lunar.html).

## Decision

Carry the independent motor-charged mechanical cell into the lunar concept, with
the carrier retaining transfer, capture and recovery propulsion. Do not add a
lunar-only propulsion or electromagnetic subsystem to the current MC-L2 coupon.
The four-cell lunar bus is a packaging hypothesis. No selected provider, engine,
service orbit, flight-rated cell or dry-mass closure exists.

A propulsionless payload has no onboard thrusters, including attitude jets.
Non-propulsive attitude control is allowed if the mission can meet its pointing
and momentum-management needs. Mission-limited replenishment is the customer
hypothesis; it is not permission to abandon failed spacecraft. Useful lifetime,
tracking, communications, collision response and end of life constrain that
customer base. A delivery mechanism does not replace those spacecraft functions.

## Connected ideal transfer

The source model uses an Earth-centered transfer ellipse from a 300 km circular
orbit to a circular coplanar Moon at 384400 km. The Moon must have the ideal
initial phase shown below. This is a conditional geometry, not an epoch-selected
trajectory or a finite sphere-of-influence boundary match.

| Computed quantity | C0-S2 result |
|---|---:|
| Earth departure impulse | 3106.427 m/s |
| Transfer time | 4.979865 days |
| Moon initial phase ahead of departure radius | 114.694802 deg |
| Transfer apogee speed | 188.186 m/s |
| Circular Moon speed | 1018.303 m/s |
| Implied lunar arrival v-infinity | 830.117 m/s |

Earlier C0-S1 arrival speeds were separate assumptions. C0-S2 connects the ideal
transfer's implied arrival speed to the capture calculation. It still omits
finite thrust, launch date, inclination, targeting corrections and Earth/Moon
force overlap. No low-thrust trajectory follows from this impulse screen.

| Staging altitude | Capture impulse | Later circularization at 100 km | Period |
|---|---:|---:|---:|
| 100 × 100 km | 821.239 m/s | 0.000 m/s | 1.963 h |
| 100 × 1,000 km | 667.769 m/s | 153.470 m/s | 2.727 h |
| 100 × 10,000 km | 306.644 m/s | 514.596 m/s | 13.938 h |

Capture plus subsequent same-perilune circularization equals direct circular
capture in this model. A high ellipse saves initial capture impulse only if its
orbit is itself useful, or the later mission justifies a different evolution.

## Carrier mass sensitivity

Assumed retained dry carrier 300 kg; four 4 kg payloads; Isp 320 s. A separate
200 m/s budget allowance is carried for subsequent operations. It is not a
calculated disposal burn. The two columns refer to different mission phases.
The payloads remain attached throughout this budget, so it does not credit mass
reductions from sequential release. It is not a completed campaign budget.

| Staging altitude | Wet mass at lunar arrival if launcher supplies departure | Wet mass in LEO if carrier supplies departure |
|---|---:|---:|
| 100 × 100 km | 437.54 kg | 1177.41 kg |
| 100 × 1,000 km | 416.66 kg | 1121.21 kg |
| 100 × 10,000 km | 371.37 kg | 999.33 kg |

All 18 mass cases are in the result JSON, including Isp 220 s and 1/12 payload
manifests. Holding dry mass fixed while propellant grows is a screening
assumption. Tankage, thrust, burn duration, restartability, coast power and
thermal design can invalidate the apparent mass solution.

## Release authority

At perilune of a 100 × 1000 km lunar orbit, the 2 m/s relative-release case gives
payload delta-v 1.973684 m/s and signed carrier recoil
-0.026316 m/s. Its ideal payload orbit becomes
100.000 × 1015.114 km.
These are departure-condition changes, not sustained stationkeeping authority.

For relative speed u, retained host M and payload m, the ideal impulsive split is
Δv_payload = M u/(M+m), Δv_host = -m u/(M+m). The conic follows from
specific energy ε = v²/2 - μ/r, a = -μ/(2ε) and the eccentricity vector.
Capture uses sqrt(v_inf² + 2μ/r_p) minus the target orbit's perilune speed.
Mass follows m_initial = m_final exp(Δv/(g0 Isp)). Units are explicit in the source.
The release split omits finite-duration pusher/catcher dynamics; MC-L2's dedicated
mechanism model remains the source for that mechanism, not this orbit screen.

## Model index and geometry status

| Model | What can be used | What is still a placeholder |
|---|---|---|
| mechanical_cell.step | Named component envelopes, +X departure, 80 mm MC-L2 stroke reference | Springs, latch, actual charger disengagement, guide fits, restraint, catcher |
| four_cell_bank.step | Four independent cell envelopes on 240 mm transverse pitch | Bank pitch selection, host adapter, harness, thermal and structural closure |
| lunar_carrier.step | Relative placement of bank and carrier services | Entire bus, tank, engine, radiator, antenna and solar wings |
| large_payload_pallet.step | Pallet plus four nominal push-point locations | Real satellite ICD, synchronization, flexible load path and mass rating |

Files are under cad/lunar_concept; each assembly also has an STL and the generator
is included. STEP carries named components and colors. STL is a triangulated
reference in mm and does not retain assembly semantics. These are not native
Fusion timelines. The tank and bus are overlapping system envelopes by design;
there is no interference-clearance certification. Do not derive installed mass
from placeholder solid volumes. No full spring coils or selected flight parts
are represented. Exploded views are presentation offsets only.

## Lunar engineering sequence after this screen

1. Declare a useful mission: sensor/relay duty, coverage, pointing, data return,
   allowed eclipse and duration. Keep 7/30/90/180-day cases as study durations until
   a customer requirement exists. An NRHO or frozen-orbit label is not selection.
2. Obtain a documented lunar harmonic gravity model, frame/normalization and
   epoch ephemerides. Converge gravity degree/order and integrator tolerances;
   include Earth/Sun gravity, radiation pressure, eclipses and terrain clearance.
   Cross-check a reference orbit before trusting a lifetime sweep.
3. Sweep staging orbit orientation, release point and finite release/navigation
   error distributions. Report impact, escape, useful coverage and conjunction
   limits for each case. Keep failures and correlate uncertainty assumptions.
4. Couple 1/4/12 release histories to actual evolving host mass, CG/inertia,
   finite capture/trim burns, attitude recovery and service budgets. Include jam,
   partial/no release, missed burn and depleted-resource cases.
5. Solve separate payload and carrier end-of-life cases. Do not turn the 200 m/s
   allowance into a disposal claim. Reject the propulsionless mission if no useful
   and defensible delivery/lifetime/end-of-life box survives.
6. Apply surviving requirements to hardware deltas and a matched conventional
   deployer comparison. Detailed lunar flight hardware waits for those results.

## Near-term reuse and future growth

Reuse the cell's interface philosophy, retained pusher, isolated charger and
independent restraint. Verify thermal-vacuum friction, spring dwell/creep,
contamination, radiation-sensitive electronics, thermal distortion and longer
coast duty. Reserve mount datums, sensor access and thermal interfaces in the
current coupon; do not bolt speculative flight services onto the bench article.

A future dedicated OTV can carry mixed cassettes and load-bearing pallets, but
larger payloads increase recoil, force path and tip-off obligations. The larger
pallet rendering establishes no payload capacity. Multi-destination delivery
requires carrier burns and resource accounting; on-orbit reloading and reuse
are separate far-future concepts. None is current prototype completion.

## Verification and sources

42 release cases, 18 mass-budget cases. All declared numerical checks pass.
The independent half-period position residual is 0.00005005 m;
tighter integration changes it by 0.00004880 m.
Energy relative drift is 6.66e-11.
Numerical consistency does not validate model completeness or physical hardware.
The local explorer passes data/control checks with stubbed graphics; actual
browser, WebGL and mobile-layout verification remains pending because no browser
is installed and the download timed out. Static engineering images were inspected.
An initial JSON boolean serialization defect is retained in validation/failures;
it did not change any physical criteria. Source and criteria hashes are in
analysis/results/lunar_visual_design.json.

Reproduce from the repository with the scientific/CAD dependencies installed:

```bash
python analysis/lunar_visual_design.py
python cad/lunar_concept/build_concepts.py
python tools/make_lunar_visuals.py
python tools/make_lunar_review.py
```

[JPL DE440 astrodynamic parameters](https://ssd.jpl.nasa.gov/astro_par.html)
supply the Earth/Moon GM values. [NASA CAPSTONE](https://www.nasa.gov/mission/capstone/)
is context for a distinct lunar orbit demonstration, not evidence that VOLLEY's
candidate orbits are stable or that propulsionless operation is established.
Sources accessed 17 September 2026. Reference radii, distances, masses and duty
choices are declared assumptions in [C0-S2](../validation/C0_S2_lunar_visual_design.md).
