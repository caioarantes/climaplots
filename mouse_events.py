from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject, QgsPointXY
from qgis.gui import QgsVertexMarker
from qgis.PyQt.QtGui import QColor

# Função para lidar com o clique do mouse

def handleMouseDown(canvas, dlg, Markers, point, button):
    crsSrc = canvas.mapSettings().destinationCrs()
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
    except:
        pass

# Função chamada ao fechar o diálogo

def fun_fechou(canvas, Markers):
    Delete_Marker(canvas, Markers)
