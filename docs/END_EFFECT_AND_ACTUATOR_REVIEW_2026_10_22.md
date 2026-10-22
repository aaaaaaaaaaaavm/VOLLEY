# End-effect, actuator and orbital-service reference review

**22 October 2026.** Scope: two closely related actuator/end-effect works and one bounded orbital-service comparator using existing primary-source records.

## Access and review status

| Work | Actual access outcome | Review level |
|:--|:--|:--|
| Yamaguchi and Morishita, *End effects of Halbach field magnet-type linear motor*, [10.1002/eej.23450](https://doi.org/10.1002/eej.23450), *Electrical Engineering in Japan* 216(4), e23450 (2023) | Wiley PDF resolves to an abstract through the browser request; direct PDF request returns HTTP 403. OpenAlex's bronze-OA label did not produce access. The [coauthor's public upload](https://www.researchgate.net/publication/372823433_End_Effects_of_Halbach_Field_Magnet_Type_Linear_Motor) supplies the complete nine-page Japanese original, DOI [10.1541/ieejias.143.570](https://doi.org/10.1541/ieejias.143.570), pp. 570–578; PDF obtained, HTTP 200. | Japanese original obtained; selected methods/results/conclusion passages checked, with pp. 571 and 577 also visually inspected. No full English-translation review claimed. |
| Zhao, Yue, Yang and Zhu, *A High Thrust Density Voice Coil Actuator With a New Structure of Double Magnetic Circuits for CubeSat Deployers*, [10.1109/TIE.2021.3134060](https://doi.org/10.1109/TIE.2021.3134060), *IEEE TIE* 69(12), 13305–13315 (2022) | [UTS repository](https://opus.lib.uts.edu.au/handle/10453/167406) explicitly marks the item closed access. Its PDF link failed with HTTP 429 through the browser request. IEEE presents a JavaScript verification challenge; direct request returns HTTP 202 with an empty body. OpenAlex reports closed access and no OA full-text location. | Metadata and repository abstract only. No lawful open full text was located in this bounded search. |

The existing 2022/2025 feeder PDFs are different works. Access responses and reading-copy identities are preserved in the private research archive. The Japanese original is used for all page references below; no equivalence of translation pagination is assumed. Wiley's translation note points to the same original volume/pages but prints the journal-code spelling `ieejsmas`; J-STAGE and the original PDF use `ieejias`.

## Page/section evidence

| Source location | Evidence checked | Boundary for the present study |
|:--|:--|:--|
| Japanese original §2.2, p. 571; equations (1)–(23), pp. 571–572 | Surface-current field calculation is explicitly 2D, with infinite extent along z. | Not finite-width 3D verification. |
| §3.1–3.2, pp. 573–574; Figs. 6–7 | Field calculations are compared with 2D JMAG; periodic boundaries represent the infinite array. | Agreement tests the stated model. |
| §4, pp. 575–577; Figs. 13–16; §5, p. 578 | Ripple reduction requires integer magnetic-period length, air-core coils and energized coil coverage extending one pole pitch beyond each field end. | Conditional coil/field arrangement, not a universal correction factor. |
| §5, p. 578 | Hardware demonstration is future work. | No physical end-effect validation inherited. |
| Actuator repository abstract; full-text page/section unavailable | Authors report a double-magnetic-circuit VCA, equivalent-circuit/FEA comparison and prototype tests. | No verified force density, speed error, load/interface, EMC or qualification values. |

**Engineering implications:** retain the existing finite-3D force/end-effect check over actual entry, overlap, segmented handover and exit positions, including finite width and return conductors. Check real coil energization/phase coverage before applying ideal cancellation. The existing [surface-charge calculation](../analysis/results/gen5_finite_force_surface3d.json) remains a numerical study with shared geometry/material and ideal-phase assumptions. The cited paper supplies no VOLLEY correction or validation. These are applications to the existing check, not new acceptance criteria.

**Passive-spacecraft compatibility:** the actuator abstract does not establish whether its prototype requires payload changes, a carrier, particular contact features or a magnetic limit. Neither compatibility nor incompatibility with unchanged passive spacecraft can be inferred. Keep the source metadata-only until the full interface and test method are available. The separately reviewed 2025 storage device's housing grooves and iron patches remain attributed to that paper; they must not be assigned to this actuator article by association.

## Bounded orbital-service comparison

Use the existing [Gen6 public reference audit](GEN6_GO1_PUBLIC_REFERENCE_AUDIT.md), with its dated source checks, rather than expanding into a provider survey.

| Existing primary reference | Supported comparator role | Unsupported extension |
|:--|:--|:--|
| [D-Orbit ION launch/deployment service](https://dorbit.space/launch-deployment/) | Provider-described propulsion-enabled orbital transport plus commanded deployment with its own or third-party dispensers. | No usable host mass, thrust, Isp, duty cycle, trajectory, price or ICD values in the audited record; no endorsement or provider selection. |
| [NRCSD IDD, NR-NRCSD-S0003 Rev. –](https://s3vi.ndc.nasa.gov/ssri-kb/static/resources/Nanoracks-CubeSat-Deployer-NRCSD-IDD.pdf) | A documented mixed-size conventional dispenser/interface precedent. | Its ISS interface and 0.5–2.0 m/s survival condition do not specify ION's dispenser or justify the surrogate's imposed spring speed. |

The bounded service question is an ordinary dispenser on a maneuvering host versus VOLLEY on that same declared surrogate host, serving the existing four-payload manifest and common target states. The [CNR-01 study](../validation/native_campaign_review/README.md) supplies numerical prescribed-command comparisons; it is not a prediction of ION service. Its spring 2.5 m/s and VOLLEY 3–6 m/s are scenario inputs. Compare installed device/host burden, propulsion, power, chronology, targeting error and shared failure exposure under the existing criteria. Provider-specific fields remain unavailable; no market ranking, price advantage or universal inferiority of conventional deployment follows.

## Source identity and access boundary

The nine-page Japanese original reading copy has SHA-256 `4cd73cb449841d7bf5327cba827e0d7e5a0e13553ffa03a1c46e5110341f177e`. The copyright status was not established for redistribution, so the reading copy remains in the private archive. Public access links identify the source; no full English-translation review or closed actuator full-text access is claimed.
