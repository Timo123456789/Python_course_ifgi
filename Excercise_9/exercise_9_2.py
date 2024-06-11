import arcpy
import arcpy.analysis

# set workspace
arcpy.env.workspace = r'C:\Users\Bem\Downloads\exercise_arcpy.gdb'

#acces the assets fc
assets = "active_assets"

#add a field which will be the input for the buffer distance

arcpy.management.AddField(assets, "buffer_distance", "TEXT")

#define a function that calculate the buffer distance
codeblock = """
def buffer_distance(type):
    if type == "mast":
        return "300 meters"
    if type == "mobile_antenna":
        return "50 meters"
    else:
        return '100 meters'"""

#use the defined function of the codeblock in the expression to retrive the buffer distance depending on the type
expression = "buffer_distance(!type!)"

#calcualte the Field
arcpy.management.CalculateField(assets, "buffer_distance", expression,"PYTHON3", codeblock)

#make a buffer analysis based on the buffer_distance field           
arcpy.analysis.Buffer(assets, "coverage", "buffer_distance")
