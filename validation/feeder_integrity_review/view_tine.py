"""Capture genuine native Gmsh data views of the CalculiX actual-tine fixture."""
from pathlib import Path
import argparse,json,hashlib,time
import gmsh
from PIL import ImageGrab
p=argparse.ArgumentParser();p.add_argument('case_dir',type=Path);p.add_argument('output',type=Path);p.add_argument('--label',required=True);a=p.parse_args();a.output.parent.mkdir(parents=True,exist_ok=True)
values={};mode=False
for line in (a.case_dir/'unit.dat').read_text().splitlines():
 if 'displacements (' in line:mode=True;continue
 if 'forces (' in line or 'stresses (' in line:mode=False
 v=line.split()
 if mode and len(v)==4:
  try:values[int(v[0])]=float(v[3])
  except ValueError:pass
gmsh.initialize();gmsh.open(str(a.case_dir/'mesh.msh'))
name=gmsh.model.getCurrent();v=gmsh.view.add(a.label+' | U_z [mm/N] | 1 N | clamped root')
gmsh.view.addModelData(v,0,name,'NodeData',list(values),[[x] for x in values.values()],numComponents=1)
gmsh.option.setNumber('General.GraphicsWidth',1250);gmsh.option.setNumber('General.GraphicsHeight',820)
gmsh.option.setColor('General.Color.Background',255,255,255);gmsh.option.setColor('General.Color.Foreground',20,20,20);gmsh.option.setColor('General.Color.Text',20,20,20)
gmsh.option.setNumber('General.BackgroundGradient',0);gmsh.option.setNumber('General.Axes',3);gmsh.option.setNumber('General.Trackball',0)
gmsh.option.setNumber('General.RotationX',-65);gmsh.option.setNumber('General.RotationY',0);gmsh.option.setNumber('General.RotationZ',-25)
gmsh.option.setNumber('Mesh.VolumeEdges',0);gmsh.option.setNumber('Mesh.SurfaceEdges',0)
gmsh.view.option.setNumber(v,'IntervalsType',3);gmsh.view.option.setNumber(v,'NbIso',20);gmsh.view.option.setNumber(v,'Light',0);gmsh.view.option.setNumber(v,'ColormapNumber',23);gmsh.view.option.setNumber(v,'ShowScale',1)
gmsh.fltk.initialize();gmsh.graphics.draw()
for i in range(6):gmsh.fltk.wait(.2)
gmsh.write(str(a.output));gmsh.view.write(v,str(a.output.with_suffix('.msh')))
full=a.output.with_name(a.output.stem+'_application.png');ImageGrab.grab(xdisplay=None).save(full)
gmsh.finalize()
r={'viewer':'Gmsh4.14.1','solver':'CalculiX2.23','label':a.label,'image_role':'Genuine OpenGL viewport export plus complete native application screenshot; no synthetic software UI','field':'Native DAT nodal U_z in mm per1N transverse end load, undeformed actual tine mesh','load':'1N transverse end-face shear, fully clamped tine root; assumed aluminium E69GPa/nu0.33. Not actual fork/root flexibility, selected alloy or assembly/contact qualification.','source_files':{str(x.name):hashlib.sha256(x.read_bytes()).hexdigest() for x in [a.case_dir/'mesh.msh',a.case_dir/'unit.inp',a.case_dir/'unit.dat']},'images':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in [a.output,full]}}
a.output.with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n');print('NativeGmshcapture',a.output.name,flush=True)
