from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject, QgsPointXY
from qgis.gui import QgsVertexMarker
from qgis.PyQt.QtGui import QColor

# Função para lidar com o clique do mouse

def handleMouseDown(canvas, dlg, Markers, point, button):
    # Only allow placing/updating markers when the plugin UI is on tab 0
    try:
        if hasattr(dlg, 'tabWidget') and dlg.tabWidget.currentIndex() != 0:
            return
    except Exception:
        # If anything goes wrong checking the tab, continue to avoid blocking UX
        pass

    crsSrc = canvas.mapSettings().destinationCrs()
    # Use modern CRS construction to avoid deprecation warnings
    try:
        # Preferred: create from EPSG id when API available
        crsDest = QgsCoordinateReferenceSystem.fromEpsgId(4326)
    except Exception:
        # Fallback: use textual CRS definition
        try:
            crsDest = QgsCoordinateReferenceSystem('EPSG:4326')
        except Exception:
            # Last resort: cast integer (older API)
            crsDest = QgsCoordinateReferenceSystem(4326)
    xform = QgsCoordinateTransform(crsSrc, crsDest, QgsProject.instance()) 
    newPoint = xform.transform(point)
    dlg.LongEdit.setText(str(round(newPoint.x(),4)))
    dlg.LatEdit.setText(str(round(newPoint.y(),4)))
    xform = QgsCoordinateTransform(crsSrc, crsSrc, QgsProject.instance())
    newPoint = xform.transform(point)
    Delete_Marker(canvas, Markers)
    m1 = QgsVertexMarker(canvas)
    m1.setCenter(QgsPointXY(newPoint.x(),newPoint.y()))
    m1.setColor(QColor(255,0, 0)) #(R,G,B)
    m1.setIconSize(12)
    m1.setIconType(QgsVertexMarker.ICON_X)
    m1.setPenWidth(4)
    Markers.append(m1)
    dlg.raise_()
    dlg.show()
    dlg.activateWindow()

# Função para deletar marcadores

def Delete_Marker(canvas, Markers):
    try:
        for mark in Markers:
            canvas.scene().removeItem(mark)
            canvas.refresh()
        # Clear the markers list to avoid holding stale references
        try:
            Markers.clear()
        except Exception:
            # If Markers is not a list-like, ignore
            pass
    except:
        pass

# Função chamada ao fechar o diálogo

def fun_fechou(canvas, Markers):
    Delete_Marker(canvas, Markers)
