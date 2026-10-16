# Gen5 and widened R1 interference disposition

The evaluated geometry is preserved. Every nonzero pair in the exact-solid census is classified below. None is accepted as a clearance pass or as proven intentional contact. No geometry repair is made by this disposition. The separate Gen6 R2/R0 models cannot clear Gen5.

| Configuration | Pair | Intersection mm³ | Classification | Correction |
|:--|:--|--:|:--|:--|
| evaluated_gen5 | Track / Sled | 82982.934 | confirmed moving geometry conflict | New rail corridor, bearing gaps and deflected sweep; rerun dynamics/mass/brake. |
| evaluated_gen5 | Interface_ESPA / Track | 70425.000 | unresolved adapter proxy intersection | Replace with parametric adapter, explicit datum, cutouts and verified load path. |
| evaluated_gen5 | Track / Magazine_S | 32915.000 | confirmed packaging failure | Separate wider or rearranged configuration, with complete new budgets. |
| evaluated_gen5 | Track / Magazine_P | 32915.000 | confirmed packaging failure | Separate wider or rearranged configuration, with complete new budgets. |
| evaluated_gen5 | Interface_ESPA / Stator | 12600.000 | unresolved adapter proxy intersection | Replace with parametric adapter, explicit datum, cutouts and verified load path. |
| evaluated_gen5 | Interface_ESPA / Enclosure | 10228.546 | unresolved adapter proxy intersection | Replace with parametric adapter, explicit datum, cutouts and verified load path. |
| evaluated_gen5 | Stator / Sled | 6300.000 | confirmed moving geometry conflict | Redesign backstop/contact and coil keep-out in a separately numbered revision. |
| evaluated_gen5 | Magazine_S / Payload_S03 | 6193.785 | unresolved payload accommodation intersection | Define keep-outs, permitted rails, pitch and tolerance; verify every stored envelope. |
| evaluated_gen5 | Magazine_P / Payload_P03 | 6193.785 | unresolved payload accommodation intersection | Define keep-outs, permitted rails, pitch and tolerance; verify every stored envelope. |
| evaluated_gen5 | Magazine_S / Payload_S04 | 5940.457 | unresolved payload accommodation intersection | Define keep-outs, permitted rails, pitch and tolerance; verify every stored envelope. |
| evaluated_gen5 | Magazine_P / Payload_P04 | 5940.457 | unresolved payload accommodation intersection | Define keep-outs, permitted rails, pitch and tolerance; verify every stored envelope. |
| evaluated_gen5 | Magazine_S / Payload_S02 | 5703.500 | unresolved payload accommodation intersection | Define keep-outs, permitted rails, pitch and tolerance; verify every stored envelope. |
| evaluated_gen5 | Magazine_S / Payload_S05 | 5703.500 | unresolved payload accommodation intersection | Define keep-outs, permitted rails, pitch and tolerance; verify every stored envelope. |
| evaluated_gen5 | Magazine_S / Payload_S06 | 5703.500 | unresolved payload accommodation intersection | Define keep-outs, permitted rails, pitch and tolerance; verify every stored envelope. |
| evaluated_gen5 | Magazine_P / Payload_P02 | 5703.500 | unresolved payload accommodation intersection | Define keep-outs, permitted rails, pitch and tolerance; verify every stored envelope. |
| evaluated_gen5 | Magazine_P / Payload_P05 | 5703.500 | unresolved payload accommodation intersection | Define keep-outs, permitted rails, pitch and tolerance; verify every stored envelope. |
| evaluated_gen5 | Magazine_P / Payload_P06 | 5703.500 | unresolved payload accommodation intersection | Define keep-outs, permitted rails, pitch and tolerance; verify every stored envelope. |
| unselected_wide_r1 | Track / Sled | 82982.934 | confirmed moving geometry conflict | New rail corridor, bearing gaps and deflected sweep; rerun dynamics/mass/brake. |
| unselected_wide_r1 | Interface_ESPA / Track | 70425.000 | unresolved adapter proxy intersection | Replace with parametric adapter, explicit datum, cutouts and verified load path. |
| unselected_wide_r1 | Interface_ESPA / Stator | 12600.000 | unresolved adapter proxy intersection | Replace with parametric adapter, explicit datum, cutouts and verified load path. |
| unselected_wide_r1 | Interface_ESPA / Wide_Enclosure_R1 | 10228.546 | unresolved adapter proxy intersection | Replace with parametric adapter, explicit datum, cutouts and verified load path. |
| unselected_wide_r1 | Stator / Sled | 6300.000 | confirmed moving geometry conflict | Redesign backstop/contact and coil keep-out in a separately numbered revision. |

Source: [exact pair census](GEN5_FULL_INTERFERENCE_AUDIT_2026_10_12.json), [classification JSON](GEN5_INTERFERENCE_DISPOSITION.json), [source builder](build_gen5.py). Finite overlap alone cannot determine a physical contact law, allowable strain or provider acceptance. All corrections require a new geometry revision and dependent model verification.
