# ACR1 open C-frame: bounded stiffness and winding-clearance screen

**Method:** linear strip/C-frame sensitivity, E =70GPa assumed. This is not an assembled finite-element result.

HistoricalA12 supplies2686.6N;the actualA4 deck supplies3672N per opposed plate/array. The force is not halved between the two plates. A4 used titanium and two support lines, so its published stiffness pass does not transfer to the open single-web aluminium carrier.

| Geometry (plate/web;webinnerY) | Force / N | Plate bend / mm | Web rotation / mm | Total per-face closure / mm | Remaining1mmfacegap / mm |
|---|---:|---:|---:|---:|---:|
| Old open C,6/6,innerweb-48 | 2686.6 | 0.6593 | 0.5282 | 1.1907 | -0.1907 |
| Old open C,6/6,innerweb-48 | 3672.0 | 0.9011 | 0.7219 | 1.6274 | -0.6274 |
| First reinforcement,12/16,innerweb-48 | 2686.6 | 0.0824 | 0.0379 | 0.1219 | 0.8781 |
| First reinforcement,12/16,innerweb-48 | 3672.0 | 0.1126 | 0.0517 | 0.1666 | 0.8334 |
| Endturn clearance,12/16,innerweb-80 | 2686.6 | 0.2617 | 0.0783 | 0.3426 | 0.6574 |
| Endturn clearance,12/16,innerweb-80 | 3672.0 | 0.3576 | 0.1071 | 0.4682 | 0.5318 |
| Recommended,16/20,innerweb-80 | 2686.6 | 0.1104 | 0.0458 | 0.1581 | 0.8419 |
| Recommended,16/20,innerweb-80 | 3672.0 | 0.1509 | 0.0626 | 0.2161 | 0.7839 |
| Actual parameter capture | 2686.6 | 0.1104 | 0.0458 | 0.1581 | 0.8419 |
| Actual parameter capture | 3672.0 | 0.1509 | 0.0626 | 0.2161 | 0.7839 |

The closure includes web compression and first-order transverse shear in addition to the two tabulated bending terms. It is measured at the far edge of the90mmmagnetic patch. Both magnetic faces close inward;the reported residual is the gap on each face,not a combined two-face gap.

## Assumptions and limits

- Magnetic normal force uniform over336x90mm active patch; each upper/lower face carries fullforce.
- Independent Euler–Bernoulli plate strips, full active axial width336mm baseline;75%/50%effective-width cases expose load-spreading uncertainty.
- Web treated as straight beam under opposite plate-end couples; symmetric midpoint rotation; web axial compression and first-order plate shear included. Root inner-face plate flexibility plus web neutral-axis rotation is a declared approximate model.
- No NdFeB/bond composite stiffening credited. Longitudinal diaphragm/backstop restraint, detailed joints, support flexibility, dynamic loads, manufacturing stress and temperature-dependent properties are not assembled.
- Magnetic force heldfixed; attraction increases withclosure and current/sourceposition can change normalforce. No coupled pull-in/stability bound supplied.
- Positive residual under a declared case is a clearance screen,not restoration of the historicalA4total0.05mmband or any new precision rating.

## Actual captured parameters

Plate 16mm;web 20mm atY[-100, -80];nominal face-envelope gap1mm. Parameter SHA256 `5a9788f654688c4fad6a33cd61c3890332b817033f12e17263e97f6ffd0358a1`.

## Winding interface

A+,C-,B+,A-,C+,B- at8mmpitch:opposite-current samephasebars24mmapart. InterleavedphaseUreturns cannot shareoneplanarconductor layer; phase-separated Zlinks are required before anywidthfanout.

Capture actualCu/GFRPouterbbox independent of activepitchspan. Webinner-80 vs GFRPouter-78 gives2mmlateralnominal clearance. RaisedGFRPwingstart atY45 touchesmovingmagnetedgeY45 atZ6..7; start raisedwing/riser at|Y|47 and bridge atZ3..5 to preserve2mmlateralclearance; verifyactualBRep.

Minimumend/interface21mm2needsitsownJ,R,localthermal/contactassessment. No uniform42/70mm2currentrating inferred.

## Recommendation

Retain16mmplates(innerfaces±14,outerfaces±30)and20mmweb(innerY-80,outerY-100)as boundedcandidate beforefullstates. Same-revision normalforce/compliance and declared tolerance/thermal reserve must follow; no assembled stiffness acceptance granted.
