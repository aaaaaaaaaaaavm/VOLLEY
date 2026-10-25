#!/usr/bin/env python3
"""Bounded linear strip/C-frame sensitivity screen; not assembled FEA acceptance."""
from pathlib import Path
import json,math,hashlib,datetime,csv
R=Path(__file__).resolve().parent;P=R.parent/'cad/PARAMETERS.json'
raw=P.read_bytes();p=json.loads(raw);la=p['launch'];mg=p['magnetic']
E=70000.;nu=.33;G=E/(2*(1+nu));kappa=5/6
b=float(mg['blocks_per_array']*mg['block_pitch']);depth=float(mg['block_depth_y']);half=depth/2
web=la['carrier_negative_web_y'];root=float(max(web));tw=float(max(web)-min(web));t=float(la['carrier_top_plate_z'][1]-la['carrier_top_plate_z'][0]);inner=float(la['carrier_top_plate_z'][0]);gap=float(mg['array_inner_z']-max(mg['stator_z']))
CASES=[('Old open C,6/6,innerweb-48',6.,6.,-48.),('First reinforcement,12/16,innerweb-48',12.,16.,-48.),('Endturn clearance,12/16,innerweb-80',12.,16.,-80.),('Recommended,16/20,innerweb-80',16.,20.,-80.),('Actual parameter capture',t,tw,root)]
LOADS=[('A12 historical integrated-force sensitivity',2686.6),('A4 historical structural-load sensitivity',3672.)]
def evaluate(tp,ww,yr,F,fraction=1.):
 width=b*fraction;I=width*tp**3/12;Iw=width*ww**3/12
 a=-half-yr;z=half-yr;centre=yr-ww/2;moment_arm=-centre;rotation_arm=half-centre
 H=2*inner+tp;q=F/depth
 assert a>=0 and z>a
 # Cantilever point-load flexibility integrated over a uniform patch[a,z].
 bend=q/(6*E*I)*(z*(z**3-a**3)-(z**4-a**4)/4)
 # Opposite end couples bend the vertical web; symmetric midpoint orientation.
 theta=F*moment_arm*H/(2*E*Iw);rotation=theta*rotation_arm
 compression=F*H/(2*E*width*ww)
 shear=F*((a+z)/2)/(kappa*G*width*tp)
 close=bend+rotation+compression+shear
 return {'plate_thickness_mm':tp,'web_thickness_mm':ww,'web_inner_y_mm':yr,'effective_loaded_axial_width_mm':width,'axial_width_fraction':fraction,'force_per_array_and_plate_N':F,'uniform_patch_pressure_MPa':F/(width*depth),'load_patch_from_inner_web_mm':[a,z],
 'plate_bending_mm':bend,'web_rotation_per_face_rad':theta,'web_rotation_contribution_mm':rotation,'web_axial_compression_per_face_mm':compression,'plate_shear_contribution_mm':shear,'per_face_closure_mm':close,'two_face_closure_mm':2*close,'nominal_face_gap_mm':gap,'remaining_per_face_gap_mm':gap-close,
 'linear_fixed_web_remaining_gap_mm':gap-bend-shear,'plate_root_bending_stress_MPa':6*F*((a+z)/2)/(width*tp**2),'web_bending_plus_axial_stress_MPa':6*F*moment_arm/(width*ww**2)+F/(width*ww),'screen_clearance_positive':close<gap,
 'interpretation':'Linear idealized strip/C-frame sensitivity only. Positive residual is not an assembled FEM, nonlinear pull-in, fatigue, bond or flight margin.'}
rows=[]
for label,tp,ww,yr in CASES:
 for source,F in LOADS:
  for fraction in [1.,.75,.5]:rows.append({'case':label,'load_source':source,**evaluate(tp,ww,yr,F,fraction)})
actual=[r for r in rows if r['case']=='Actual parameter capture']
source_paths=[Path('/workspace/VOLLEY/validation/A12_inter_array_force.md'),Path('/workspace/VOLLEY/validation/results/A4_sled_structural.json')]
result={'analysis':'ACR1 C-frame linear closure and endturn interface screen','generated_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'parameter_sha256':hashlib.sha256(raw).hexdigest(),'source_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'actual_geometry_inputs':{'plate_thickness_mm':t,'web_y_mm':web,'web_thickness_mm':tw,'root_inner_y_mm':root,'nominal_magnet_to_stator_face_envelope_gap_mm':gap,'load_patch_axial_mm':b,'load_patch_y_mm':[-half,half],'material_E_MPa_assumed':E,'Poisson_ratio_assumed':nu},
 'source_interpretation':'A12adopted2686.6N;A4actual3672N(0.12MPaover340x90oldfootprint),eachforceactsoneachopposedarray/plate—notF/2. A4wasTiE113800MPaandtwowebsupportlines;itsFEApassdoesnottransfer to single-web aluminiumACR1. Bothforcesarehistoricalsensitivityinputs,notcurrentACR1forcepredictions.',
 'source_hashes':{str(x):hashlib.sha256(x.read_bytes()).hexdigest()for x in source_paths},
 'assumptions':['Magnetic normal force uniform over336x90mm active patch; each upper/lower face carries fullforce.','Independent Euler–Bernoulli plate strips, full active axial width336mm baseline;75%/50%effective-width cases expose load-spreading uncertainty.','Web treated as straight beam under opposite plate-end couples; symmetric midpoint rotation; web axial compression and first-order plate shear included. Root inner-face plate flexibility plus web neutral-axis rotation is a declared approximate model.','No NdFeB/bond composite stiffening credited. Longitudinal diaphragm/backstop restraint, detailed joints, support flexibility, dynamic loads, manufacturing stress and temperature-dependent properties are not assembled.','Magnetic force heldfixed; attraction increases withclosure and current/sourceposition can change normalforce. No coupled pull-in/stability bound supplied.','Positive residual under a declared case is a clearance screen,not restoration of the historicalA4total0.05mmband or any new precision rating.'],
 'comparisons':rows,'actual_capture_results':actual,
 'winding_geometry_review':{'active_bar_section_mm2':mg.get('active_copper_cross_section_mm2'),'endlink_minimum_section_mm2':mg.get('endlink_minimum_section_mm2'),'phase_layers_z_mm':mg.get('endlink_phase_z_mm'),'nominal_interphase_z_clearance_mm':mg.get('interphase_nominal_z_gap'),
 'path_topology':'A+,C-,B+,A-,C+,B- at8mmpitch:opposite-current samephasebars24mmapart. InterleavedphaseUreturns cannot shareoneplanarconductor layer; phase-separated Zlinks are required before anywidthfanout.',
 'clearance':'Capture actualCu/GFRPouterbbox independent of activepitchspan. Webinner-80 vs GFRPouter-78 gives2mmlateralnominal clearance. RaisedGFRPwingstart atY45 touchesmovingmagnetedgeY45 atZ6..7; start raisedwing/riser at|Y|47 and bridge atZ3..5 to preserve2mmlateralclearance; verifyactualBRep.',
 'rating_boundary':'Minimumend/interface21mm2needsitsownJ,R,localthermal/contactassessment. No uniform42/70mm2currentrating inferred.'},
 'recommendation':'Retain16mmplates(innerfaces±14,outerfaces±30)and20mmweb(innerY-80,outerY-100)as boundedcandidate beforefullstates. Same-revision normalforce/compliance and declared tolerance/thermal reserve must follow; no assembled stiffness acceptance granted.'}
(R/'CFRAME_SCREEN.json').write_text(json.dumps(result,indent=2)+'\n')
with (R/'CFRAME_COMPARISON.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
lines=['# ACR1 open C-frame: bounded stiffness and winding-clearance screen','', '**Method:** linear strip/C-frame sensitivity, E =70GPa assumed. This is not an assembled finite-element result.','', 'HistoricalA12 supplies2686.6N;the actualA4 deck supplies3672N per opposed plate/array. The force is not halved between the two plates. A4 used titanium and two support lines, so its published stiffness pass does not transfer to the open single-web aluminium carrier.','', '| Geometry (plate/web;webinnerY) | Force / N | Plate bend / mm | Web rotation / mm | Total per-face closure / mm | Remaining1mmfacegap / mm |','|---|---:|---:|---:|---:|---:|']
for r in rows:
 if r['axial_width_fraction']==1:lines.append(f"| {r['case']} | {r['force_per_array_and_plate_N']:.1f} | {r['plate_bending_mm']:.4f} | {r['web_rotation_contribution_mm']:.4f} | {r['per_face_closure_mm']:.4f} | {r['remaining_per_face_gap_mm']:.4f} |")
lines+=['','The closure includes web compression and first-order transverse shear in addition to the two tabulated bending terms. It is measured at the far edge of the90mmmagnetic patch. Both magnetic faces close inward;the reported residual is the gap on each face,not a combined two-face gap.','', '## Assumptions and limits','']+['- '+s for s in result['assumptions']]
lines+=['','## Actual captured parameters','',f"Plate {t:g}mm;web {tw:g}mm atY{web};nominal face-envelope gap{gap:g}mm. Parameter SHA256 `{result['parameter_sha256']}`.",'', '## Winding interface','',result['winding_geometry_review']['path_topology'],'',result['winding_geometry_review']['clearance'],'',result['winding_geometry_review']['rating_boundary'],'','## Recommendation','',result['recommendation'],'']
(R/'CFRAME_SCREEN.md').write_text('\n'.join(lines))
print(json.dumps({'parameters':result['actual_geometry_inputs'],'actual_fullwidth_cases':[{k:q[k]for k in ['force_per_array_and_plate_N','per_face_closure_mm','remaining_per_face_gap_mm']}for q in actual if q['axial_width_fraction']==1]},indent=2))
