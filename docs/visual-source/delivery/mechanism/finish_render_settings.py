"""Apply final editorial render settings to the already baked scene."""
import bpy,sys,json,hashlib
from pathlib import Path
r=Path(sys.argv[sys.argv.index('--')+1]);p=r/'VOLLEY_ACR1_operating_cycle.blend';bpy.ops.wm.open_mainfile(filepath=str(p));s=bpy.context.scene
s.display.render_aa='FXAA';s.display.shading.show_shadows=False;s.display.shading.cavity_type='WORLD';s.display.shading.background_color=(.0056,.008,.0116)
s.world.color=(.0056,.008,.0116)
next_payload=next(o for o in s.objects if o.get('cad_name')=='Bank_south_L4_Stored_3U')
for frame,color in [(1,(.70,.73,.72,1)),(1560,(.70,.73,.72,1)),(1561,(.05,.62,.59,1)),(1680,(.05,.62,.59,1))]:
 next_payload.color=color;next_payload.keyframe_insert('color',frame=frame)
for fc in next_payload.animation_data.action.fcurves:
 if fc.data_path=='color':
  for point in fc.keyframe_points:point.interpolation='CONSTANT'
s.render.filepath='//frames/';bpy.ops.wm.save_as_mainfile(filepath=str(p),compress=True)
d=json.load(open(r/'ANIMATION_PROVENANCE.json'));d['source_script_sha256']=hashlib.sha256((r/'animate_mechanism.py').read_bytes()).hexdigest();d['render_settings']={'engine':'Blender 4.3.2 Workbench','antialiasing':'FXAA','cavity':'WORLD','shadows':False};(r/'ANIMATION_PROVENANCE.json').write_text(json.dumps(d,indent=2)+'\n')
for f in [25,517,817,1249,1345]:
 s.frame_set(f);s.render.filepath=str(r/f'final-preview-{f:04d}.jpg');bpy.ops.render.render(write_still=True)
