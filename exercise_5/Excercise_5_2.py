parent = iface.mainWindow()
sCoords, bOK = QInputDialog.getText(parent, "Coordinates", "Enter coordinates as latitude, longitude", text = "51.96066,7.62476")
x = float(sCoords.split(",")[0])
y = float(sCoords.split(",")[1])

crsSource = QgsCoordinateReferenceSystem(4326)
crsTarget = QgsCoordinateReferenceSystem(25832)
transformation = QgsCoordinateTransform(crsSource, crsTarget, QgsProject.instance())

point=QgsPointXY(y,x)
pointTo = transformation.transform(point)

districts = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]

point_geom = QgsGeometry.fromPointXY(pointTo)
int_list=[]

for feature in districts.getFeatures():
    district_geom = feature.geometry()
    if point_geom.intersects(district_geom):
        int_list.append(feature)
        QMessageBox.information(parent, "Intersection", f"Point intersects with {feature['Name']}!")
    else:
        continue
    
if int_list == []:
    QMessageBox.information(parent, "Intersection", f"No intersection, try again Looser!")
        
        
