"""Compose the four Blender STEP animation states into a review hero and share card.

Run after render_gen5_sequence.py. Inputs are its STEP-derived stage PNGs.
The two outputs are layout renders, not additional engineering evidence.
"""
from __future__ import annotations
import sys
from pathlib import Path
import bpy

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'cad/renders/sequence'
WHITE=(.90,.96,1,1);CYAN=(.34,.89,.85,1);DIM=(.59,.73,.82,1);AMBER=(1,.67,.36,1)
FONT_PATH=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
FONT_BOLD=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')


def emission(name,color=None,texture=None):
    m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear()
    out=n.new('ShaderNodeOutputMaterial');e=n.new('ShaderNodeEmission');e.inputs['Strength'].default_value=1
    if texture:
        img=n.new('ShaderNodeTexImage');img.image=bpy.data.images.load(str(texture),check_existing=True)
        m.node_tree.links.new(img.outputs['Color'],e.inputs['Color'])
    else:e.inputs['Color'].default_value=color
    m.node_tree.links.new(e.outputs[0],out.inputs['Surface'])
    return m

def plane(name,cx,cy,w,h,z,mat):
    bpy.ops.mesh.primitive_plane_add(size=2,location=(cx,cy,z));o=bpy.context.object;o.name=name;o.scale=(w/2,h/2,1)
    o.data.materials.append(mat);return o

def label(body,x,y,size,color=WHITE,bold=False):
    curve=bpy.data.curves.new(body[:20],type='FONT');curve.body=body;curve.size=size
    curve.font=bpy.data.fonts.load(str(FONT_BOLD if bold else FONT_PATH))
    o=bpy.data.objects.new(body[:20],curve);bpy.context.collection.objects.link(o)
    o.location=(x,y,.3);o.data.materials.append(emission(body[:16],color))
    return o

def base(width,height):
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=1
    s.cycles.use_denoising=False
    s.render.resolution_x=width;s.render.resolution_y=height;s.render.resolution_percentage=100
    s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
    s.view_settings.view_transform='Standard'
    bpy.ops.object.camera_add(location=(0,0,12));c=bpy.context.object;c.name='Layout camera';c.data.type='ORTHO';c.data.ortho_scale=12;c.rotation_euler=(0,0,0)
    s.camera=c
    plane('Navy background',0,0,12,12,-.4,emission('Navy',(.018,.045,.077,1)))
    return s

def hero():
    s=base(2400,1800)
    label('VOLLEY  /  GEN5 OPERATIONS',-5.4,3.93,.43,WHITE,True)
    label('One STEP-derived storyboard. Four intended states. No physical mechanism has been built.',-5.4,3.55,.18,DIM)
    paths=[OUT/f'step_{i:02d}.png' for i in range(1,5)]
    titles=['01  STORE','02  HANDOFF','03  ACCELERATE','04  DEPART']
    captions=['3U envelopes in side cassette · launch retention unresolved',
              'Lateral transfer is conceptual · actuator and contact unverified',
              'Sled and payload advance · modeled thrust, no rated motor',
              'Payload continues, sled arrests · separation and brake untested']
    for i,path in enumerate(paths):
        cx=-2.7 if i%2==0 else 2.7
        cy=1.95 if i<2 else -1.85
        plane(f'Panel border {i+1}',cx,cy,5.0,2.81,0,emission('Border',(.19,.34,.43,1)))
        plane(f'STEP stage {i+1}',cx,cy,4.9,2.756,.1,emission(f'Frame {i+1}',texture=path))
        y=.25 if i<2 else -3.45
        label(titles[i],cx-2.55,y,.23,CYAN,True)
        label(captions[i],cx-2.55,y-.23,.13,DIM)
    label('REFERENCE FIT FAILS  ·  FEED, RELEASE CONTACT AND ARREST ARE NOT VALIDATED',-5.4,-4.19,.165,AMBER,True)
    s.render.filepath=str(OUT/'gen5_operations_hero.png');bpy.ops.render.render(write_still=True)

def social():
    s=base(1200,630)
    plane('Right stage field',2.15,.08,7.15,4.025,0,emission('Stage image',texture=OUT/'step_03.png'))
    plane('Right upper text mask',2.15,1.78,7.15,.70,.16,emission('Upper mask',(.018,.045,.077,1)))
    plane('Right lower text mask',2.15,-1.64,7.15,.82,.16,emission('Lower mask',(.018,.045,.077,1)))
    plane('Left dark copy field',-2.85,.0,6.4,6.3,.08,emission('Copy field',(.018,.045,.077,1)))
    label('VOLLEY',-5.45,1.67,.78,WHITE,True)
    label('GEN5',-5.45,.95,.58,CYAN,True)
    label('COMPUTATIONAL',-5.45,.28,.265,WHITE,True)
    label('DESIGN REVIEW',-5.45,-.08,.265,WHITE,True)
    label('FIT + 3U MASS FAIL',-5.45,-1.15,.235,AMBER,True)
    label('STEP-derived concept motion',-5.45,-1.72,.18,DIM)
    label('No hardware built or measured',-5.45,-2.00,.18,DIM)
    s.render.filepath=str(OUT/'gen5_social_preview.png');bpy.ops.render.render(write_still=True)

if __name__=='__main__':
    if not all((OUT/f'step_{i:02d}.png').is_file() for i in range(1,5)):
        raise SystemExit('Render the sequence stages first')
    hero();social();print('wrote Gen5 operations hero and 1200x630 social preview')
