# Import modules
from qgis.core import QgsVectorLayer, QgsProject
from qgis.core import *
import os

# Supply path to qgis install location
QgsApplication.setPrefixPath(r"C:\Program Files\QGIS 3.34.5", True)

# Path to data and QGIS-project
#layer_path = r"C:\Users\Sven Harpering\sciebo\GIS-GK\GIS-GK_WS_23_24\GIS Data\Flughafen Muenchen - Datenlieferung I\WKA_Buffer.shp"
project_path = r"C:\Users\Bem\Downloads\myFirstProject.qgz"  # for QGIS version 3+
folder = r"C:\Users\Bem\Downloads\Muenster\Muenster"

 # Create QGIS instance and "open" the project
project = QgsProject.instance()
project.read(project_path)

for file in os.listdir(folder):
    if file.endswith('.shp'):
        basename = os.path.splitext(os.path.basename(file))[0]
        # Create layer
        layer = QgsVectorLayer(os.path.join(folder,file), basename, "ogr")

# Check if layer is valid
        if not layer.isValid():
            print("Error loading the layer!")
            continue
        
        # Add layer to project
        project.addMapLayer(layer)#
        print(f"Shapefile: {basename} added to the project")
    else:
        continue  
    
    # Save project
project.write()

print("All Layers added to project\nProject saved successfully!")