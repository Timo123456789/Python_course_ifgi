import csv


#create new csv
with open(r'C:\Users\Bem\Downloads\SchoolReport.csv', 'w', newline='') as csvfile:
    #write in csv
    csvwriter = csv.writer(csvfile, delimiter=';')
    
    # Write the header row
    csvwriter.writerow(['Name', 'X', 'Y'])
    
    #get Layer by name and the first Layer in the returned List
    layers = QgsProject.instance().mapLayersByName("Schools")
    layer = layers[0]
    #iterater over features
    features = layer.getFeatures()
    for feature in features:
        #get geometry and Name
        coords = feature.geometry().asPoint()
        name = feature["Name"]
        #write to file
        csvwriter.writerow([name, coords.x(), coords.y()])