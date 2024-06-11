import arcpy 

# set workspace
arcpy.env.workspace = r'C:\Users\Bem\Downloads\exercise_arcpy.gdb'

#list all feature classes of type point and remove the active asset fc
fc_list = arcpy.ListFeatureClasses(feature_type='Point')
fc_list.remove('active_assets')

#get the needed fields and the fields for the cursor
cursor_fields = ["SHAPE@","status", "Type"]
assets = "active_assets"

#initialize the insert cursor
icur = arcpy.da.InsertCursor(assets, cursor_fields)
#iterate over the listet features
for fc in fc_list:
    scur = arcpy.da.SearchCursor(in_table=fc,field_names=cursor_fields)
    #initialize the searchCursur, if the status is active insert the row to the asset fc
    for row in scur:
        if row[1]=="active":
            icur.insertRow(row)

del icur

print("All Features copied")

