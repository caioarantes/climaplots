from qgis.core import QgsProject, QgsRasterLayer, QgsCoordinateReferenceSystem
from qgis.utils import iface
from qgis.core import QgsRasterLayer, QgsLayerTreeLayer, QgsColorRampShader, QgsStyle, QgsRasterShader, QgsSingleBandPseudoColorRenderer

print("Loading map_tools.py...")

def hybrid_function():
    """Adds a Google Hybrid XYZ tile layer to the QGIS project if it is not already present."""
    existing_layers = QgsProject.instance().mapLayers().values()
    layer_names = [layer.name() for layer in existing_layers]
    if "Google Hybrid" in layer_names:
        print("Google Hybrid layer already added.")
        return

    google_hybrid_url = "type=xyz&zmin=0&zmax=20&url=https://mt1.google.com/vt/lyrs%3Dy%26x%3D{x}%26y%3D{y}%26z%3D{z}"
    layer_name = "Google Hybrid"
    provider_type = "wms"

    try:
        # Create the XYZ tile layer
        google_hybrid_layer = QgsRasterLayer(google_hybrid_url, layer_name, provider_type)

        if google_hybrid_layer.isValid():
            # Add the layer to the project
            QgsProject.instance().addMapLayer(google_hybrid_layer, False)

            # Set the project CRS to EPSG:4326 (WGS 84)
            crs_4326 = QgsCoordinateReferenceSystem("EPSG:4326")
            QgsProject.instance().setCrs(crs_4326)

            # Adjust visibility and add to the layer tree
            google_hybrid_layer.setOpacity(1)
            root = QgsProject.instance().layerTreeRoot()
            root.addLayer(google_hybrid_layer)

            # Refresh the canvas and zoom to extent
            iface.mapCanvas().refresh()
            iface.mapCanvas().zoomToFullExtent()
            print(f"{layer_name} layer added successfully in EPSG:4326.")
        else:
            print(f"Failed to load {layer_name}. Invalid layer.")
    except Exception as e:
        print(f"Error loading {layer_name}: {e}")

