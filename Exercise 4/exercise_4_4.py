#get Schools and districts by name
schools = QgsProject.instance().mapLayersByName('Schools')[0]
districts = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]
#function for counting points in polygon
pointsInPolygon=processing.run("native:countpointsinpolygon", {'POLYGONS':districts,'POINTS':schools,'WEIGHT':'','CLASSFIELD':'','FIELD':'NUMPOINTS','OUTPUT':'TEMPORARY_OUTPUT'})
#access output and features
layer = pointsInPolygon['OUTPUT']
features = layer.getFeatures()

#loop and print features
for feature in features:
    name=feature.attribute('Stat_Name')
    count =feature.attribute('Number')
    print(f"{name}: {count}")
