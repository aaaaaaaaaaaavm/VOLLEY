# Smaller payloads, and what they actually change

VOLLEY is designed around a 3U CubeSat. This file asks what happens if it carries something else:
chipsats, PocketQubes, ThinSats, TubeSats, 1U, or the larger CubeSat classes.

The answer is the opposite of the intuition, and it matters. Smaller payloads do not make the
machine faster. They make it economically viable, which is the more urgent problem.

> Generated. The tables below are written by `analysis/payload_family.py` from
> `analysis/results/payload_family.json`. Do not hand-edit them; change the script and re-run it.
> They were typed by hand until 2026-07-31, and the packing counts were wrong.

---

## The velocity question, settled first

A lighter payload should mean more acceleration for the same force. It does not, because the
sled is most of the moving mass. And scaling the sled down does not help either, because array
length sets thrust and sled mass together: a shorter array is a lighter sled *and* a weaker motor.

<!-- PAYLOAD-TABLES-START -->

### Velocity, which barely moves

| Payload | Mass | Moving mass with the 9.445 kg sled | Acceleration | Exit velocity |
|---|---|---|---|---|
| ChipSat / femtosat | 0.005 kg | 9.45 kg | 14.3 g | 19.1 m/s |
| PocketQube 1P | 0.250 kg | 9.70 kg | 14.0 g | 18.9 m/s |
| ThinSat | 0.280 kg | 9.72 kg | 13.9 g | 18.8 m/s |
| PocketQube 3P | 0.750 kg | 10.20 kg | 13.3 g | 18.4 m/s |
| TubeSat | 0.750 kg | 10.20 kg | 13.3 g | 18.4 m/s |
| 1U CubeSat | 1.330 kg | 10.78 kg | 12.6 g | 17.9 m/s |
| 3U CubeSat | 4.000 kg | 13.45 kg | 10.1 g | 16.0 m/s |
| 6U CubeSat | 8.000 kg | 17.45 kg | 7.8 g | 14.1 m/s |
| 12U CubeSat | 12.000 kg | 21.45 kg | 6.3 g | 12.7 m/s |

### Deployer mass per customer, which moves by a factor of thirty

| Payload | Envelope, mm | Per load | Deployer kg per satellite | |
|---|---|---|---|---|
| ChipSat / femtosat | 35 x 35 x 2.5 | 13322 | 0.010 | beyond the mechanism |
| PocketQube 1P | 50 x 50 x 50 | 326 | 0.388 | beyond the mechanism |
| ThinSat | 114 x 114 x 25.4 | 123 | 1.029 |  |
| PocketQube 3P | 50 x 50 x 150 | 108 | 1.172 |  |
| TubeSat | 88 x 88 x 127 | 41 | 3.088 |  |
| 1U CubeSat | 100 x 100 x 100 | 40 | 3.165 |  |
| 3U CubeSat | 340 x 100 x 100 | 12 | 10.550 |  |
| 6U CubeSat | 340 x 200 x 100 | 6 | 21.100 |  |
| 12U CubeSat | 340 x 200 x 200 | 3 | 42.200 |  |

### Shortening the magnet array, which buys nothing

| Array length | K<sub>t</sub> | Sled mass | Force | Acceleration, 3U | Exit velocity |
|---|---|---|---|---|---|
| 340 mm | 10.54 | 9.45 kg | 1328 N | 10.1 g | 16.0 m/s |
| 240 mm | 7.44 | 7.18 kg | 937 N | 8.5 g | 14.8 m/s |
| 150 mm | 4.65 | 5.15 kg | 586 N | 6.5 g | 12.9 m/s |

<!-- PAYLOAD-TABLES-END -->

Removing 99.9 % of the payload buys 19 % more velocity. Pairing a light sled with a light
payload recovers most of that and no more: a 150 mm sled with a PocketQube gives about 11.8 g and
17.3 m/s. A great deal of algebra for 0.8 m/s.

> The velocity ceiling is set by the acceleration limit, not by mass. It stays at
> 25.3 m/s over the 1.30 m zone for every class here, and reaching it needs the same levers
> regardless of what is being launched. See [`VELOCITY_CEILING.md`](VELOCITY_CEILING.md).
> *This line used to call the ceiling "a payload qualification property". The 25 g it is computed
> at is a limit this design chose, not one any standard sets, P98.*

The sled mass scaling is crude: it assumes chassis mass scales with array length plus a fixed
end-structure overhead, which describes the current chassis rather than a redesign. A genuinely
minimal sled for a 0.25 kg payload has not been designed and would not look like a scaled copy of
this one.

---

## What smaller payloads actually change

The deployer's mass is fixed. The number of customers it carries is not, and
[`KILL_CRITERIA.md`](KILL_CRITERIA.md) threat 1 is the one that decides whether VOLLEY has a
reason to exist. Against a cold-gas module at 0.5 to 1.2 kg giving the same 16.5 m/s, the 3U
configuration loses by about 8x at 10.547 kg per satellite, and the PocketQube configuration
wins, at 0.388 kg volumetric and 0.440 kg on A24's designed cell. That is the entire
commercial argument, and it turns on payload class rather than on any machine parameter.

> Corrected 2026-08-22, [P101](../OPEN_PROBLEMS.md). This sentence read *"wins by 2 to 5x at
> 0.236 kg"*, a figure computed against a 76.5 kg rollup. The current values are above.
> The multiplier is deliberately not restated: it was a ratio against a cold-gas module quoted
> as a range, and re-deriving it here would put a number in a document that no results file holds.
> NEEDS SOURCE: the PocketQube-against-cold-gas multiplier at the current rollup.

### How the packing counts are computed, because they used to be wrong

A raw volume ratio says the magazine holds 21 3U satellites. It holds 12. The difference
is septa, follower plates, the escapement, the gate and the drive bay, none of which a volume
ratio knows about.

So the model is calibrated instead of asserted: packing efficiency is set so the 3U case
returns the twelve the machine is actually laid out for, and the same 56.2 % is applied to every
other class. This file previously carried a raw volumetric bound with a note that "realistic
packing is likely 40 to 60 %", and then quoted the unadjusted numbers anyway. PocketQube 1P was
published here as 546 per load and 0.14 kg per satellite; calibrated, it is 326 and, at the
rollup of the day, 0.236 kg. The conclusion survives, it still beats the cold-gas comparator,
and the old figure should not be quoted. *Both mass figures in this paragraph are the 2026-07-31
record of a packing correction, not current: the count of 326 stands, and the per-satellite figure
is now 0.388 kg in the table above (P101).*

### Superseded by A24: the ladder is now a design

> Read [`validation/A24_fixed_cell_manifest.md`](../validation/A24_fixed_cell_manifest.md) and
> [ADR-025](adr/025-fixed-cell-manifest.md) before quoting anything above. The tables on this
> page remain the *volumetric* answer, generated by `payload_family.py` and kept because the
> comparison between the two is the point. The designed answer, from
> `analysis/cell_manifest.py`, is different in three places that matter:
>
> | Class | Here (volumetric) | A24 (designed cell) |
> |---|---:|---:|
> | ThinSat | 123 per load | NOT ACCOMMODATED, 114 mm exceeds the 100 mm cell section in two axes |
> | 12U | 3 per load | NOT ACCOMMODATED, needs 200 mm in both section axes; the cassette is 166 mm wide |
> | 1U | 40 per load, 3.165 kg | 36 per load, 3.517 kg, over the 2 kg threshold |
> | TubeSat | 41 per load, 3.088 kg | 24 per load, 5.275 kg, over the threshold |
>
> Threat 1 still closes, on the PocketQube classes at 0.440 and 1.319 kg. It no longer closes
> on 1U, which is the rung this repository had been leaning on.
>
> > Corrected 2026-08-22, [P101](../OPEN_PROBLEMS.md). Every figure in this box divided a dry
> > mass of 76.5 kg, and the rollup has read 126.6 kg since
> > [A46](../validation/A46_enclosure_buildup.md) on 2026-08-16. `cell_manifest.py` reads the
> > rollup live and had simply never been re-run, so its committed results file was stale at
> > 84.5 kg and this box was stale at 76.5. Both columns are re-quoted above at the current
> > rollup. The counts, the arrangements and the two refusals are geometry and did not move.
> > *1U was over the threshold at 2.125 kg and it is further over at 3.517.* The conclusion did
> > not change; the margin did.

### Four things that must be read with those numbers

1. They are still volumetric. Calibration fixes the average, not the geometry. A24 has
since built the fixed-cell design and it refuses three classes these tables count, see above.
No cassette layout exists for any class except 3U, and no insert exists in CAD for any class.

2. Hundreds of satellites is a different machine from twelve. The campaign thermal case
(24.4 kJ over twelve shots), the bank recharge duty, and the escapement cycle life were all sized
for twelve. A magazine of hundreds needs those re-derived, not scaled. The bank is already the
binding problem at twelve shots (P26). Classes exceeding 200 per load are flagged in the table for
exactly this reason, and the chipsat row is a volumetric statement rather than a proposal.

3. The feed mechanism is built around CubeSat corner rails. The cradle, the escapement and
the retention gate all engage the CDS rail interface. PocketQubes, ThinSats and TubeSats have
different interfaces, so a smaller class needs its own cassette, cradle and gate. That is real
mechanical design, not a parameter change.

4. Qualification loads are not established for any class here, small or otherwise. The 25 g
ceiling is a requirement this design set on itself; it does not come from the CubeSat Design
Specification, which publishes no universal quasi-static level and defers test levels to the launch
provider, and it does not come from GEVS, which specifies a random-vibration spectrum whose
`g_rms` is not a quasi-static equivalent (P98). PocketQube, ThinSat and TubeSat standards are
less mature still and have not been checked against any published document for this file. The
accelerations in the table above, to 14.0 g at PocketQube 1P, are what the machine delivers, not
what any payload is qualified to accept. Compatibility is a payload-specific structural question
and needs an integration review nobody has done.

---

## What this implies for the programme

A small-payload variant attacks the only threat that is currently crossed, and it does so
without touching the velocity, the field model or the control loop, all of which are the
best-validated parts of the design.

It is also honest about what it does not do. It does not make the machine faster, it does not fix
the envelope (P9), and it does not fix the bank (P26). It changes who the machine is for.

Not adopted, and not costed as a design. This file establishes that payload class is the
dominant term in the mass-per-satellite argument. Turning that into a variant means a cassette, a
cradle, a gate, and a re-derived thermal and power case for hundreds of shots. That is a
programme decision, and the numbers above exist so it can be made against evidence.

---

## Sources

- Form factors: PocketQube and CubeSat Design Specification published dimensions; TubeSat from
  the published kit specification; ThinSat from its published envelope; chipsat masses from the
  Sprite class
- Payload masses are typical flight masses, not qualification maxima, the CDS allows 2 kg
  for a 1U and 12 kg for a 6U, and using those would make the ladder look worse, not better
- Cassette geometry: `cad/parameters.json`, `groups.magazine`
- Sled mass, thrust constant and exit velocity: `analysis/motor_model.py`
- Deployer dry mass: `analysis/mass_properties.py`, which excludes enclosure, radiator and
  avionics (P10), so every kg-per-satellite figure here is optimistic
- Cold-gas module masses: published COTS ranges, not a quotation
