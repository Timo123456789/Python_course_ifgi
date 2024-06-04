"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterField, 
                       QgsProject, 
                       QgsFeatureRequest,
                       QgsVectorLayer,
                       QgsDistanceArea,
                       QgsUnitTypes,
                       QgsMapSettings,
                       QgsMapRendererParallelJob)
from qgis import processing
from qgis.utils import iface
from PyQt5.QtWidgets import QMessageBox
import os



class Create_City_District_Profile(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """
    
    

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.
    
    
    #define input and output variables
    DISTRICT = 'District'
    pools_or_schools = "Pools or schools"
    PDF_OUTPUT = 'Path to PDF output'

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return Create_City_District_Profile()
        
        
    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'createcitydistrictprofile'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Create City District Profile')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Profile Creator')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'profilecreator'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("This algorithm takes your selected input district and calculates statistics returned as a pdf report")
        
    
    #function for sorting the districts alphabetical for the input list
    def sorted_districts(self):
        #district layer
        districts = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0] 
        request = QgsFeatureRequest()

        #Clause for Ordering
        nameClause = QgsFeatureRequest.OrderByClause("Name", ascending = True)
        orderby = QgsFeatureRequest.OrderBy([nameClause])
        request.setOrderBy(orderby)

        #get the features and make a List
        features = districts.getFeatures(request)
        district_names = [feature["Name"] for feature in features]
        
        return district_names
            
    
    #define characteritics of the tool parameters
    def initAlgorithm(self, config=None):
        
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        
        # We add the input vector features source. It can have any kind of
        # geometry.
        from qgis.core import QgsProcessingParameterEnum,QgsProcessingParameterFileDestination
        self.addParameter(
            QgsProcessingParameterEnum(
                self.DISTRICT,  # The internal parameter name
                self.tr('Name des Disticts'),  # The displayed name in the interface
                self.sorted_districts(),  # The list of strings from which to choose
                defaultValue="No District selected",   # Default value, index of the options list
                 optional=False
            ))
            
        self.addParameter(
            QgsProcessingParameterEnum(
                self.pools_or_schools,  # The internal parameter name
                self.tr('Include information about pools or schools'),  # The displayed name in the interface
                ["pools", "schools"],  # The list of strings from which to choose
                defaultValue="pools",   # Default value, index of the options list
                 optional=False
            ))

        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.PDF_OUTPUT,  # The internal parameter name
                self.tr('PDF Path'),  # The displayed name in the interface
                fileFilter = "PDF files (.PDF)" #filter only pdf
            ))

    #function for selecting the selected district
    def select_district(self, district_name):
        districts = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]
        expression = f"\"Name\" = '{district_name}'"
        districts.selectByExpression(expression, QgsVectorLayer.SetSelection)
        selected_district = districts.selectedFeatures()[0]
        
        return selected_district

    #function for calculating the area in sqkm of the selected district
    def calculate_area(self, district_name):
        
        selected_district=self.select_district(district_name)
        #initialize a distance area class define ellipsoid and crs
        d = QgsDistanceArea()
        d.setEllipsoid("ETRS89")
        d.setSourceCrs(QgsProject.instance().crs(), QgsProject.instance().transformContext())
        
        #get geometry and calculate area
        geom = selected_district.geometry()
        area = round(d.measureArea(geom)/1e6, 2)
        return area
        
    
    #function to count the intersecting households
    def get_households(self, district_name):
        #get relevant features
        district = self.select_district(district_name)
        households_layer = QgsProject.instance().mapLayersByName("House_Numbers")[0]
        household_features = households_layer.getFeatures()

        #count housholds that intersect with the selected districts
        household_count = 0
        district_geom = district.geometry()
        for feature in household_features:
            if district_geom.contains(feature.geometry()):
                household_count += 1

        return household_count
        
    
    #count parcels in a selcted district
    def get_parcels(self, district_name):
        #get relevant layers
        district = self.select_district(district_name)
        parcels = QgsProject.instance().mapLayersByName("Muenster_Parcels")[0]
        parcels_features = parcels.getFeatures()

        #count the parcels that intersect the geometry of the selected district
        parcels_count = 0
        district_geom = district.geometry()
        for feature in parcels_features:
            if district_geom.intersects(feature.geometry()):
                parcels_count += 1

        return parcels_count
        
        
    
    #function to count the number of schools or pools based on the input
    def get_schools_or_pools(self, district_name, schools_or_pools):
        district = self.select_district(district_name)
        
        #if pools selcected count pools
        if schools_or_pools == "pools":
            pools =QgsProject.instance().mapLayersByName("public_swimming_pools")[0]
            pools_features = pools.getFeatures()
        
            pools_count = 0
            district_geom = district.geometry()
            for feature in pools_features:
                if district_geom.intersects(feature.geometry()):
                    pools_count += 1
            
            #if no pools in this district return a string
            if pools_count == 0:
                return "No Pools in this district"

            return pools_count
        
        #if schools selcetd count number of schools
        else:
            schools =QgsProject.instance().mapLayersByName("Schools")[0]
            schools_features = schools.getFeatures()
        
            schools_count = 0
            district_geom = district.geometry()
            for feature in schools_features:
                if district_geom.intersects(feature.geometry()):
                    schools_count += 1
            
            if schools_count == 0:
                return "No Schools in this district"

            return schools_count
            
    
    #function to create the map
    def get_map(self,district_name):
        #select the district and zoom to the feature
        import time
        districts = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]
        district = self.select_district(district_name)
        bbox = districts.boundingBoxOfSelected()
        iface.mapCanvas().setExtent(bbox)
        iface.mapCanvas().refresh()

        #set processing to sleep for 5 seconds so the zoom has enough time
        time.sleep(5)

        # Create output path for the image in project directory
        picturePath = os.path.join(QgsProject.instance().homePath(), "image.png")
        iface.mapCanvas().saveAsImage(picturePath)

        
        return picturePath
        
    
    #function to count the types of schools or pools in a district for the graph
    def count_feature_types(self, schools_or_pools, district_name):
        geom = self.select_district(district_name).geometry()
        
        #if pools selcted count the pools
        if schools_or_pools == "pools":
            layer = QgsProject.instance().mapLayersByName("public_swimming_pools")[0]
            #create a dict
            type_count = {}
            
            #if there is an intersection get the type of the pool if it already exits in dict add plus 1
            for feature in layer.getFeatures():
                if geom.intersects(feature.geometry()):
                    attr_value = feature["Type"]
                    if attr_value in type_count:
                        type_count[attr_value] += 1
                    else:
                        type_count[attr_value] = 1
                
            return type_count
        
        #same process if schools are selected
        else:
            layer = QgsProject.instance().mapLayersByName("Schools")[0]
            type_count = {}
            
            for feature in layer.getFeatures():
                if geom.intersects(feature.geometry()):
                    attr_value = feature["SchoolType"]
                    if attr_value in type_count:
                        type_count[attr_value] += 1
                    else:
                        type_count[attr_value] = 1
                
            
           
            return type_count
            
            
    
    #plot the schools or pools
    def plot_type_distribution(self, data, title="Type Distribution"):
        import matplotlib.pyplot as plt
        
        #size
        fig, ax = plt.subplots(figsize=(10, 5))  
        types = list(data.keys())
        counts = list(data.values())
        
        #data
        types = list(data.keys())
        counts = list(data.values())
        
        #design
        ax.bar(types, counts, color='blue')
        ax.set_xlabel('Types')
        ax.set_ylabel('Counts')
        ax.set_title(title)
        ax.set_xticklabels(types, rotation=45)
        
        #output
        plt.tight_layout()
        path = os.path.join(QgsProject.instance().homePath(), "output.png")
        fig.savefig(path)  # Speichert das Diagramm als PNG-Datei

    
        return path 

        

    #function to create the pdf
    def create_pdf(self, pdf_output, district_name, parent, area, household_number, parcels, schools_or_pools, schools_or_pools_number, picture_path):
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Image
        from reportlab.lib.units import inch

        
        #create texts and image objects to insert in the pdf later
        doc = SimpleDocTemplate(pdf_output, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        #texts
        header = Paragraph(f"<b>District Report for {district_name}</b>", styles["Title"])
        parent_text = Paragraph(f"Parent District: {parent}", styles["Normal"])
        area_text = Paragraph(f"Size: {area} square kilometers", styles["Normal"])
        household_text = Paragraph(f"Number of Housholds: {household_number}", styles["Normal"])
        parcels_text =Paragraph(f"Number of Parcels {parcels}", styles["Normal"])
        schools_or_pools_text = Paragraph(f"Number of {schools_or_pools}: {schools_or_pools_number}", styles["Normal"])
        
        #images
        im = Image(picture_path, 3*inch, 3*inch)
        diagramm = Image(self.plot_type_distribution(self.count_feature_types(schools_or_pools, district_name)), 4*inch, 3*inch)
        


        #append the content to the story list the order of append is important for the order in the pdf 
        story.append(header)
        story.append(Spacer(1, 12))
        story.append(im)
        story.append(Spacer(1, 12))
        story.append(parent_text)
        story.append(area_text)
        story.append(household_text)
        story.append(parcels_text)
        story.append(schools_or_pools_text)
        story.append(Spacer(1, 12))
        story.append(diagramm)

        doc.build(story)
        
        
        return pdf_output

        

    #main algorithm to create the pdf
    def processAlgorithm(self, parameters, context, feedback):
        #get all the imputs
        district_index = self.parameterAsInt(parameters, self.DISTRICT, context)
        district_name = self.sorted_districts()[district_index]
        include_option = self.parameterAsEnum(parameters, self.pools_or_schools, context)
        pdf_output = self.parameterAsFileOutput(parameters, self.PDF_OUTPUT, context)
        
        #create variables with the important infos for the parameters of the pdf function
        schools_or_pools = "pools" if include_option == 0 else "schools"
        parent = self.select_district(district_name)["P_District"]
        area = self.calculate_area(district_name)
        household_number=self.get_households(district_name)
        parcels = self.get_parcels(district_name)
        schools_or_pools_number = self.get_schools_or_pools(district_name, schools_or_pools)
        picture_path = self.get_map(district_name)
        diagramm_path = self

        #push some info to the console
        feedback.pushInfo(f"Processing district: {district_name}")
        feedback.pushInfo(f"Option selected: {schools_or_pools}")
        feedback.pushInfo(f"PDF will be saved to: {pdf_output}")

        # Create PDF
        pdf_path = self.create_pdf(pdf_output, district_name, parent, area, household_number, parcels, schools_or_pools, schools_or_pools_number, picture_path)

        return {self.PDF_OUTPUT: pdf_path}
