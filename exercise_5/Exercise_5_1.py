mc = iface.mapCanvas()
da = QgsDistanceArea()
#districts Layer
districts = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]
schools = QgsProject.instance().mapLayersByName("Schools")[0]
request = QgsFeatureRequest()

#Clause for Ordering
nameClause = QgsFeatureRequest.OrderByClause("Name", ascending = True)
orderby = QgsFeatureRequest.OrderBy([nameClause])
request.setOrderBy(orderby)

#get the features and make a List
features = districts.getFeatures(request)
district_names = [feature["Name"] for feature in features]

#initialize Window
parent = iface.mainWindow()
sDistrict, bOk = QInputDialog.getItem(parent, "District Names", "Select District: ",district_names)

#if user canceled selected
if not bOk:
    QMessageBox.warning(parent, "Schools", "User cancelled")
else:
    #initialize the list
    intersecting_schools = []
    
    #select district by name
    districts.selectByExpression(f"\"Name\" = '{sDistrict}'", QgsVectorLayer.SetSelection)
    selected_features = districts.selectedFeatures()
    
    #iterate features of district and schools and get geom object
    for feature in selected_features: 
        district_geom=feature.geometry()
        centroid = district_geom.centroid()
        for sfeature in schools.getFeatures():
            school_geom=sfeature.geometry()
            #check for overlap and append to list
            if district_geom.intersects(school_geom):
                xS = sfeature.geometry().get().x()
                yS = sfeature.geometry().get().y()
                xD = centroid.get().x()
                yD = centroid.get().y()
                distance=da.measureLine([QgsPointXY(xS,yS),QgsPointXY(xD,yD)])/1000
                intersecting_schools.append(f"{sfeature['Name']},{sfeature['SchoolType']}\nDistance to City Center: {distance:.2f} km")
    #sort List
    intersecting_schools.sort()
    mc.zoomToSelected()
    if intersecting_schools:
        QMessageBox.information(parent, f"schools in {sDistrict}", "\n\n".join(intersecting_schools))
    else:
        QMessageBox.information(parent, "No Schools", f"No schools found in '{sDistrict}'.")
        
    




