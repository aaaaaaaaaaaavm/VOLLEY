"""Genuine FreeCAD TechDraw reference sheets, with dimensions from actual pins.

Not a manufacturing release: alloy, fits, finish and axial retention are not
approved. Requires a Qt display; exported pages are not synthetic screenshots.
"""

from pathlib import Path
import sys, time, json, hashlib

sys.path.extend(["/usr/share/freecad/Mod/PartDesign", "/usr/share/freecad/Mod/Part"])
from PySide2 import QtWidgets
import FreeCAD as App

app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
import FreeCADGui as Gui

Gui.showMainWindow()
import Part, PartGui, TechDraw, TechDrawGui

H = Path(__file__).resolve().parent
D = H / "drawings"
D.mkdir(exist_ok=True)
Gui.showMainWindow()
template = D / "reference_template.svg"
template.write_text(
    """<svg xmlns="http://www.w3.org/2000/svg" xmlns:freecad="https://www.freecad.org/wiki/index.php?title=Svg_Namespace" width="297mm" height="210mm" viewBox="0 0 297 210">
<rect x="10" y="10" width="277" height="190" fill="none" stroke="black" stroke-width="0.5"/>
<path d="M10 166H287M170 166V200M245 166V200M170 183H287" fill="none" stroke="black" stroke-width="0.25"/>
<g font-family="DejaVu Sans" font-size="3.5"><text x="15" y="174" freecad:editable="title"><tspan>REFERENCE GEOMETRY</tspan></text>
<text x="15" y="182">VOLLEY · All dimensions in mm</text><text x="15" y="190">NOT FOR MANUFACTURE · NO APPROVAL REPRESENTED</text>
<text x="175" y="174" freecad:editable="number"><tspan>FM-02</tspan></text><text x="175" y="191">Review revision ·20October2026</text>
<text x="250" y="174" freecad:editable="scale"><tspan>Scale3:1</tspan></text><text x="250" y="191" freecad:editable="sheet"><tspan>1/2</tspan></text></g></svg>""",
    encoding="utf-8",
)
source = App.openDocument(str(H / "cad/FM02_3U_transfer.FCStd"))
objects = {o.Label: o.Shape.copy() for o in source.Objects}
App.closeDocument(source.Name)
doc = App.newDocument("FM02_ReferenceDrawings")
records = []
for i, (name, title, notes) in enumerate(
    [
        (
            "gate_crossbolt",
            "FM-02-G01 · Storage-gate crossbolt",
            [
                "Shaft diameter6; length48",
                "Head diameter10; length6",
                "Overall length54; quantity1",
                "Provisional steel; alloy and finish unselected",
                "Axial capture and actuator interface incomplete",
            ],
        ),
        (
            "receiver_lock_pin_0",
            "FM-02-R01 · Receiver lock pin",
            [
                "Shaft diameter3; length14",
                "Head diameter5; length2",
                "Overall length16; quantity2",
                "Provisional steel; alloy and finish unselected",
                "Spring/actuator and axial capture incomplete",
            ],
        ),
    ]
):
    shape = objects[name]
    bb = shape.BoundBox
    shape.translate(App.Vector(-bb.XMin, -bb.Center.y, -bb.Center.z))
    ob = doc.addObject("Part::Feature", "Pin")
    ob.Label = name
    ob.Shape = shape
    page = doc.addObject("TechDraw::DrawPage", "Sheet")
    temp = doc.addObject("TechDraw::DrawSVGTemplate", "Template")
    temp.Template = str(template)
    page.Template = temp
    temp.EditableTexts = {
        "title": title,
        "number": "FM-02-" + str(i + 1),
        "scale": "Scale3:1",
        "sheet": str(i + 1) + "/2",
    }
    view = doc.addObject("TechDraw::DrawViewPart", "Longitudinal")
    view.Source = [ob]
    view.Direction = (0, 0, 1)
    page.addView(view)
    view.X = 105
    view.Y = 115
    view.ScaleType = "Custom"
    view.Scale = 3
    end = doc.addObject("TechDraw::DrawViewPart", "End")
    end.Source = [ob]
    end.Direction = (1, 0, 0)
    page.addView(end)
    end.X = 235
    end.Y = 115
    end.ScaleType = "Custom"
    end.Scale = 3
    note = doc.addObject("TechDraw::DrawViewAnnotation", "GeometryNotes")
    note.Text = notes
    note.TextSize = 3.5
    page.addView(note)
    note.X = 80
    note.Y = 65
    doc.recompute()
    # Nominal dimensions are listed in the annotation. No unresolved dimension
    # feature or manufacturing tolerance is released with these reference views.
    doc.recompute()
    for j in range(10):
        app.processEvents()
        time.sleep(0.1)
    svg = D / ("FM02_reference_pin_" + str(i + 1) + ".svg")
    pdf = svg.with_suffix(".pdf")
    TechDrawGui.exportPageAsSvg(page, str(svg))
    TechDrawGui.exportPageAsPdf(page, str(pdf))
    records.append(
        dict(
            part=name,
            measured_overall_mm=shape.BoundBox.XLength,
            files={
                p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [svg, pdf]
            },
        )
    )
doc.recompute()
doc.saveAs(str(D / "FM02_ReferenceDrawings.FCStd"))
(D / "DRAWING_RECORD.json").write_text(
    json.dumps(
        dict(
            revision="FM-02",
            software="FreeCAD1.0 TechDraw",
            sheets=records,
            source_sha256=hashlib.sha256(
                (H / "cad/FM02_3U_transfer.FCStd").read_bytes()
            ).hexdigest(),
            boundary="Reference geometry sheets, not approved manufacturing drawings. Dimensions are nominal model dimensions; no alloy, fit, finish, preload, actuator or inspection release.",
        ),
        indent=2,
    )
    + "\n"
)
print("Two native TechDraw reference sheets exported", flush=True)
