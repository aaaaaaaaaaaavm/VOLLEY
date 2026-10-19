"""Capture the actual FreeCAD Python-hosted Qt/Coin viewport; requires an X display.
Usage: python capture_native.py assembly.FCStd capture.png
No application chrome or geometry is composited. The source document is not saved.
"""

import sys, time
from PySide2 import QtWidgets, QtCore, QtGui

sys.path.extend(["/usr/lib/freecad/Mod/Part", "/usr/lib/freecad/Mod/PartDesign"])
import FreeCAD as App
import FreeCADGui as Gui

app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
Gui.showMainWindow()
import Part, PartGui

window = Gui.getMainWindow()
window.resize(1600, 1000)
d = App.openDocument(sys.argv[1])
Gui.activeDocument().activeView().viewAxonometric()
Gui.activeDocument().activeView().fitAll()
print("Native loaded objects", len(d.Objects), flush=True)
old = list(d.Objects)
for ob in old:
    if hasattr(ob, "Shape"):
        print(
            ob.Name,
            ob.Shape.Volume,
            ob.ViewObject.TypeId if ob.ViewObject else "no view",
            flush=True,
        )
        ob.ViewObject.Visibility = False
        fresh = d.addObject("Part::Feature", "Review_" + ob.Name)
        fresh.Label = ob.Label
        fresh.Shape = ob.Shape
        Gui.activeDocument().getObject(fresh.Name).show()
d.recompute()
for ob in d.Objects:
    if hasattr(ob, "ViewObject"):
        if "payload" in ob.Label.lower():
            ob.ViewObject.ShapeColor = (0.24, 0.48, 0.67)
            ob.ViewObject.Transparency = 25
        elif any(word in ob.Label.lower() for word in ["gate", "dog", "front"]):
            ob.ViewObject.ShapeColor = (0.8, 0.48, 0.14)
        else:
            ob.ViewObject.ShapeColor = (0.72, 0.75, 0.77)
for i in range(20):
    app.processEvents()
    time.sleep(0.1)
Gui.activeDocument().activeView().fitAll()
for i in range(10):
    app.processEvents()
    time.sleep(0.1)
for dock in window.findChildren(QtWidgets.QDockWidget):
    if "report" in dock.windowTitle().lower():
        dock.hide()
for i in range(8):
    app.processEvents()
    time.sleep(0.1)
app.primaryScreen().grabWindow(window.winId()).save(sys.argv[2])
print("Genuine FreeCAD application window captured")
