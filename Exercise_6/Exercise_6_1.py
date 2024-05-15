import csv

# Create a map canvas object
mc = iface.mapCanvas()

#set up the Layer and initilize provider
uri = "polygon?crs=EPSG:25832&field=Standard_land_value:integer&field=type:string&field=district:string&index=yes"
layer = QgsVectorLayer(uri, "Land_values", "memory")
provider =layer.dataProvider()


#open and read the file and lines
file = open(r"C:\Users\Bem\Downloads\Data for Session 6\Data for Session 6\standard_land_value_muenster.csv")
lines = file.readlines()

#iterate the rows
for row in lines[1:]:
    
    #split by semicolon to extract column
    rows_split = row.split(";")
    feature =  QgsFeature(layer.fields())
    #add the attributes
    feature.setAttributes([rows_split[0], rows_split[1], rows_split[2]])
    
    #format the wkt and add the geom to the layer
    wkt_format = rows_split[3].replace("\n", "")
    wkt = QgsGeometry.fromWkt(wkt_format)
    feature.setGeometry(wkt)
    
    #add all the features
    provider.addFeatures([feature])
    print("Feature added")
    
#add layer to project
QgsProject().instance().addMapLayer(layer)  
    


    
    
    
    
