"""Check that isolated load-study solids correspond to the current CAD material."""
from pathlib import Path
import hashlib,json
import FreeCAD as App
import Part
H=Path(__file__).resolve().parent;out=[]
for size in ['1U','3U']:
    current=H/'parts'/('FM06_'+size+'_sled_entry_bar.step')
    fixture=H/'receiver/fea/FM06'/(size+'_sled_entry_bar.step')
    a=Part.read(str(current)).Solids[0];b=Part.read(str(fixture)).Solids[0]
    shift=a.CenterOfMass-b.CenterOfMass;b.translate(shift)
    difference=a.cut(b).Volume+b.cut(a).Volume
    out.append({'part':size+'_receiver','current_sha256':hashlib.sha256(current.read_bytes()).hexdigest(),'fixture_sha256':hashlib.sha256(fixture.read_bytes()).hexdigest(),'fixture_alignment_translation_mm':[shift.x,shift.y,shift.z],'symmetric_volume_difference_mm3':difference})
    assert difference<1e-5,(size,difference)
    fork=Part.read(str(H/'parts'/('FM06_'+size+'_fork_body.step')))
    tine=Part.read(str(H/'tine/tine.step'))
    missing=tine.cut(fork).Volume
    out.append({'part':size+'_tine','fixture_sha256':hashlib.sha256((H/'tine/tine.step').read_bytes()).hexdigest(),'fixture_material_missing_from_current_fork_mm3':missing})
    assert missing<1e-5,(size,'tine',missing)
(H/'COMPONENT_GEOMETRY_LINEAGE.json').write_text(json.dumps({'checks':out,'boundary':'Rigid material-geometry correspondence only. The isolated fixtures omit current guide/pin contacts, roots and frame compliance; identical component shape does not transfer assembled stiffness or qualification.'},indent=2)+'\n')
print('Receiver/tine material lineage checked against current reference STEP files')
