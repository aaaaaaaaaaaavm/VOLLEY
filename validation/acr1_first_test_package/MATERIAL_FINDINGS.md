# Material differences preserved by N5-R1

| Finding | Test-packet disposition |
|:--|:--|
| Legacy bench wavelength uses four 12 mm blocks; ACR1 uses six 8 mm blocks and 60° increments. | C01 has a new one-period model and marked polarity map. No legacy field/thrust band is silently inherited. |
| The complete current loop matters: the modeled return contributes about −0.00522 / +0.00889 N/A at the two force stations. | Build and model the defined loop and terminal gap; bound source-lead bias. The active-bar force alone is not the load-cell prediction. |
| Legacy B4/thermal text credits an auxiliary eddy brake; ACR1 arrest is active LSM control. | C03 uses a separately calibrated external bench brake for a low-energy kinematic counterpart. It does not validate LSM arrest or revive the auxiliary brake. |
| The nominal ACR1 bank stores 23.328 kJ. | It is excluded from C01. The first coupon has a ≤2 J accounted source boundary, with separate limits for compliance, current, pulse duration and stored output energy. |
| Ordinary 1g sliding at illustrative μ=0.1 imposes about 3.923 N on the 4 kg dummy. | C03 requires measured drag including uncertainty ≤0.1 N. Without that support the proposed slow egress model is invalid; report the constraint rather than treating a tabletop release as microgravity. |
| The source four-rail stiffness gives only 0.518 µm axial compression at 26.8635 N. | C02 custody metrology cannot establish that stiffness or the elastic-energy tip-off bound. The separate compliance experiment requires submicrometre metrology and identified interfaces. |
| The release supplement's half-open keeper catches the payload; fault attitude/rate changes with solver/contact representation. | Only disabled-drive missing-proof/inhibit demonstrations are included. No dynamic obstructed-release test or precise fault tip-off acceptance is inferred. |
| Several source ground-gravity lift cases fail while low-mass coast sizing cases pass. | First C02 rig fixes receiver level. Full vertical ground lifting needs its own load/motion checks and actual holding mechanism. |
| Eaton's standard cell window ends at 65°C; the 85°C catalog point requires 2.5 V/cell. | No full-bank hot operation is included. Actual package placement/contact, thermal limits and derating must be resolved before any later environmental claim. |
| The C01 53-solid STEP and beam calculation omit certified joints, guards, gantry and complete C02/C03 supports. | They are provisional fixture definition, with explicit load/inspection gates. They are not a manufacturing or physical-test release. |

All findings concern the applicable configuration or test boundary. The completed ACR1 computational results and ED1 editorial issue retain their identities.
