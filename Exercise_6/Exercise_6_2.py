# Create a map canvas object
mc = iface.mapCanvas()

#get pools and district layer
pools = QgsProject.instance().mapLayersByName("public_swimming_pools")[0]
districts = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]
fields = pools.fields()

#acces provider
provider = pools.dataProvider()


#create and add district field to the layer
fld = QgsField("District", QVariant.String, len = 50)
provider.addAttributes([fld])
pools.updateFields()
print("Field district added to the layer")

# Reload the layer to reflect changes
pools = QgsProject.instance().mapLayersByName("public_swimming_pools")[0]
provider = pools.dataProvider()
fields = pools.fields()  # Re-acquire the fields after the update


# Getting access to the pool layers capabilities
capabilities = provider.capabilitiesString()
# Checking if the capabilty is part of the layer
if "Change Attribute Values" in capabilities:
    print("Features of this layer can be modified...")
    
    #iterate the pools features
    for feature in pools.getFeatures():
        
        # Get the id of the current feature
        feature_id = feature.id()
        
        # If the value of the current feature in the column "Type" has
        # the value "H" change it to "Hallenbad"
        if feature["Type"] == "H":
            
            # Create a dictionary with column and value to change
            attributes = {fields.indexOf("Type"):"Hallenbad"}
            
            # Use the changeAttributeValues methode from the provider to 
            provider.changeAttributeValues({feature_id:attributes})
            
        elif feature["Type"] == "F":
            
            # Create a dictionary with column and value to change
            attributes = {fields.indexOf("Type"):"Freibad"}
            provider.changeAttributeValues({feature_id:attributes})
        else:
            pass
        
        #iterate the district features
        for dfeat in districts.getFeatures():
            
            #get access to the geometry objects
            district_geom=dfeat.geometry()
            pool_geom = feature.geometry()
            
            #check for intersecting features and add the district name
            if district_geom.intersects(pool_geom):
                attributes = {fields.indexOf("District"):dfeat["Name"]}
                provider.changeAttributeValues({feature_id:attributes})
                continue
                
    
                
    print("all Features have been modified")

else:
    print("features of this layer cant be modified...")
    





